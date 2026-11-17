import base64
import csv
import json
import logging
import os
import secrets
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

LOG = logging.getLogger("tgwitness.security")


def windows_sid():
    row = subprocess.run(["whoami", "/user", "/fo", "csv", "/nh"], capture_output=True, text=True,
                         check=True, timeout=30).stdout
    return next(csv.reader([row.strip()]))[1]


def owner_only(root: Path):
    if os.name != "nt":
        try:
            os.chmod(root, 0o700)
        except OSError:
            LOG.warning("Could not restrict %s to its owner; doctor reports its permissions", root)
        return
    try:
        from .windows_acl import owner_acl
        if not owner_acl(root, windows_sid(), repair=True):
            raise OSError("The filesystem did not retain the owner-only ACL")
    except (OSError, subprocess.SubprocessError, IndexError):
        LOG.warning("Could not limit %s to this account; other local accounts may read it", root)


def owner_only_state(root: Path):
    if os.name != "nt":
        mode = root.stat().st_mode & 0o777
        return mode & 0o077 == 0, "mode " + oct(mode)
    try:
        from .windows_acl import owner_acl
        if owner_acl(root, windows_sid()):
            return True, "verified ACLs for this account only"
    except (OSError, subprocess.SubprocessError, IndexError):
        pass
    return False, "owner-only ACLs could not be verified (FAT/exFAT volumes keep no permissions)"


def private_write(path: Path, data: bytes):
    temp = path.with_suffix(path.suffix + ".tmp")
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    for attempt in range(6):
        try:
            os.replace(temp, path)
            break
        except PermissionError as exc:
            if getattr(exc, "winerror", None) not in (5, 32, 33) or attempt == 5:
                raise
            time.sleep(.01 * 2**attempt)


class Vault:
    def __init__(self, root: Path):
        self.root = root
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        key_path = root / "vault.key"
        protected = [root / "credentials.enc", root / "signing.enc", root / "independent_login.enc"]
        external = os.environ.get("TGWITNESS_VAULT_KEY_FILE")
        marker = root / "vault.external.json"
        self.key_mode = "external" if external or marker.exists() else "local"
        if self.key_mode == "external":
            if not external:
                raise RuntimeError("This vault requires TGWITNESS_VAULT_KEY_FILE. Refusing local key replacement.")
            if key_path.exists() or (not marker.exists() and any(p.exists() for p in protected)):
                raise RuntimeError("This data directory still uses its local vault key. Stop TgWitness and run: python -m tgwitness.security migrate-to-external KEYFILE --data-dir DATA")
            source = Path(external).resolve(strict=True)
            if source.is_relative_to(root.resolve()) or source.stat().st_size > 128:
                raise RuntimeError("Provide a small master-key file outside the data directory.")
            master = source.read_bytes().strip()
            Fernet(master)
            if not marker.exists():
                private_write(marker, json.dumps({"format": "tgwitness-external-vault-v1",
                              "salt": base64.b64encode(os.urandom(32)).decode()}).encode())
            config = json.loads(marker.read_bytes())
            salt = base64.b64decode(config["salt"], validate=True)

            if config["format"] not in (EXTERNAL_FORMAT, "tgwatch-external-vault-v1") or len(salt) != 32:
                raise RuntimeError("Invalid external vault metadata; restore the original file.")
            self.fernet = external_fernet(master, salt)
        else:
            if not key_path.exists():
                if any(p.exists() for p in protected):
                    raise RuntimeError("Vault key missing. Restore it from backup; refusing key replacement.")
                private_write(key_path, Fernet.generate_key())
            self.fernet = Fernet(key_path.read_bytes())
        token_path = root / "panel-token.txt"
        if not token_path.exists():
            private_write(token_path, secrets.token_urlsafe(32).encode())
        self.token = os.environ.get("TGWITNESS_TOKEN") or token_path.read_text().strip()
        if len(self.token) < 24:
            raise RuntimeError("TGWITNESS_TOKEN must contain at least 24 characters.")
        signing_path = root / "signing.enc"
        if not signing_path.exists():
            key = Ed25519PrivateKey.generate()
            self.save("signing", {"private_key": base64.b64encode(key.private_bytes(
                serialization.Encoding.Raw, serialization.PrivateFormat.Raw,
                serialization.NoEncryption())).decode()})
        key_data = self.read("signing")["private_key"]
        self.signer = Ed25519PrivateKey.from_private_bytes(base64.b64decode(key_data))
        self.public_key = base64.b64encode(self.signer.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw)).decode()

    def read(self, name):
        path = self.root / (name + ".enc")
        if not path.exists():
            return {}
        return json.loads(self.fernet.decrypt(path.read_bytes()))

    def save(self, name, value):
        private_write(self.root / (name + ".enc"),
                      self.fernet.encrypt(json.dumps(value).encode()))

    def sign(self, value: bytes):
        return base64.b64encode(self.signer.sign(value)).decode()


class InstanceLock:
    def __init__(self, root: Path):

        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        owner_only(root)
        self.stream = (root / ".instance.lock").open("a+b")
        self.stream.seek(0)
        self.stream.write(b"0")
        self.stream.flush()
        self.stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.stream.close()
            raise RuntimeError("This data directory is already open. Use one worker.") from None

    def close(self):
        self.stream.close()


class KeyInUse(ValueError):
    pass


class KeyLock:
    IN_USE = ("This Telegram session is already connected by another TgWitness process or workspace on this computer. "
              "Close it there first: one session key, one connection.")

    def __init__(self, key: bytes, directory: Path | None = None):
        import hashlib
        name = "tgwitness-key-" + hashlib.sha256(b"tgwitness-session-key:" + key).hexdigest()
        self.stream = self.socket = self.mutex = None
        if directory is None and sys.platform == "linux":
            import socket
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                self.socket.bind(chr(0) + name)
            except OSError:
                self.socket.close()
                raise KeyInUse(self.IN_USE) from None
            return
        if directory is None and os.name == "nt":
            import ctypes
            kernel = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel.CreateMutexW.argtypes = (ctypes.c_void_p, ctypes.c_bool, ctypes.c_wchar_p)
            kernel.CreateMutexW.restype = ctypes.c_void_p
            kernel.CloseHandle.argtypes = (ctypes.c_void_p,)
            handle = kernel.CreateMutexW(None, False, "Global\\" + name)
            if not handle or ctypes.get_last_error() == 183:
                if handle:
                    kernel.CloseHandle(handle)
                raise KeyInUse(self.IN_USE)
            self.mutex = kernel, handle
            return
        import tempfile
        directory = directory or Path(tempfile.gettempdir()) / "tgwitness-keys"
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.stream = (directory / (name.removeprefix("tgwitness-key-") + ".lock")).open("a+b")
        self.stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.stream.close()
            raise KeyInUse(self.IN_USE) from None

    def close(self):
        if self.socket is not None:
            self.socket.close()
        elif self.mutex is not None:
            kernel, handle = self.mutex
            self.mutex = None
            kernel.CloseHandle(handle)
        elif self.stream is not None:
            self.stream.close()


EXTERNAL_FORMAT = "tgwitness-external-vault-v1"


def external_fernet(master, salt):
    key = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt,
               info=b"TgWitness external vault v1").derive(base64.urlsafe_b64decode(master))
    return Fernet(base64.urlsafe_b64encode(key))


def read_master(master_file, root):
    source = Path(master_file).resolve(strict=True)
    if source.is_relative_to(Path(root).resolve()) or source.stat().st_size > 128:
        raise ValueError("Provide a small master-key file outside the data directory.")
    master = source.read_bytes().strip()
    Fernet(master)
    return master


def vault_files(folder, suffix=".enc"):
    return sorted([*folder.glob("*" + suffix), *folder.glob("account-exports/*/attachment-queue/*" + suffix)])


def marker_salt(marker):
    try:
        config = json.loads(marker.read_bytes())
        salt = base64.b64decode(config["salt"], validate=True)
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return salt if config.get("format") == EXTERNAL_FORMAT and len(salt) == 32 else None


def migrate_peers(folder, local, external):
    path = folder / "journal.sqlite3"
    if not path.is_file():
        return 0
    db = sqlite3.connect(path, timeout=30)
    try:
        if db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='profiling_users'").fetchone() is None:
            return 0
        rows = db.execute("SELECT run_id, user_id, peer FROM profiling_users WHERE peer IS NOT NULL").fetchall()
        with db:
            for run_id, user_id, token in rows:
                try:
                    external.decrypt(token)
                    continue
                except InvalidToken:
                    pass
                try:
                    value = external.encrypt(local.decrypt(token))
                except InvalidToken:
                    value = None
                db.execute("UPDATE profiling_users SET peer=? WHERE run_id=? AND user_id=?", (value, run_id, user_id))
        return len(rows)
    finally:
        db.close()


def migrate_to_external(root, master_file):
    root = Path(root).resolve()
    master = read_master(master_file, root)
    folders = [root, *(sorted(p for p in (root / "profiles").iterdir() if p.is_dir()) if (root / "profiles").is_dir() else [])]
    lock = InstanceLock(root)
    moved = []
    try:
        for folder in folders:
            key_path, marker = folder / "vault.key", folder / "vault.external.json"
            if not key_path.exists():
                for kept in vault_files(folder, ".enc.local"):
                    kept.unlink()
                continue
            for kept in vault_files(folder, ".enc.local"):
                os.replace(kept, kept.with_suffix(""))
            local = Fernet(key_path.read_bytes())
            salt = marker_salt(marker) or os.urandom(32)
            external = external_fernet(master, salt)
            private_write(marker, json.dumps({"format": EXTERNAL_FORMAT,
                                              "salt": base64.b64encode(salt).decode()}).encode())
            files = vault_files(folder)
            plain = {path: local.decrypt(path.read_bytes()) for path in files}
            for path, data in plain.items():
                private_write(path.with_name(path.name + ".new"), external.encrypt(data))
            for path in files:
                os.replace(path, path.with_name(path.name + ".local"))
                os.replace(path.with_name(path.name + ".new"), path)
            peers = migrate_peers(folder, local, external)
            for path, data in plain.items():
                if external.decrypt(path.read_bytes()) != data:
                    raise RuntimeError("Re-encrypted vault file does not read back: " + path.name)
            key_path.unlink()
            for path in files:
                path.with_name(path.name + ".local").unlink()
            moved.append({"workspace": str(folder.relative_to(root)) if folder != root else "default",
                          "files": len(files), "peers": peers})
    finally:
        lock.close()
    return moved


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Create an external vault master key without printing it.")
    parser.add_argument("command", choices=["create-master-key", "migrate-to-external"])
    parser.add_argument("path", type=Path, help="New master-key file, or with migrate-to-external the existing one")
    parser.add_argument("--data-dir", type=Path, help="Data directory to migrate (the panel must be stopped)")
    args = parser.parse_args()
    if args.command == "migrate-to-external":
        if args.data_dir is None:
            parser.exit(2, "Give the data directory with --data-dir.\n")
        try:
            moved = migrate_to_external(args.data_dir, args.path)
        except InvalidToken:
            parser.exit(1, "Migration stopped: a vault file does not open with the vault.key of its workspace. Restore "
                           "it from a backup and run the command again; vault.key is removed only after every file "
                           "of that workspace reads back.\n")
        except (OSError, ValueError, RuntimeError, sqlite3.Error) as exc:
            parser.exit(1, "Migration stopped: " + str(exc) + "\n")
        for item in moved:
            print("Workspace " + item["workspace"] + ": " + str(item["files"]) + " vault files and "
                  + str(item["peers"]) + " saved profiling peers re-encrypted; vault.key removed.")
        print("Start TgWitness with TGWITNESS_VAULT_KEY_FILE=" + str(Path(args.path).resolve()) + " from now on, "
              "and keep that key file and its backup apart from the data directory.")
        return
    try:
        fd = os.open(args.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as output:
            output.write(Fernet.generate_key())
            output.flush()
            os.fsync(output.fileno())
    except OSError:
        parser.exit(1, "Could not create a new key file. Check the directory and do not overwrite an existing key.\n")
    print("Master key created. Protect it separately and set TGWITNESS_VAULT_KEY_FILE to its path.")


if __name__ == "__main__":
    main()
