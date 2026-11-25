import base64
import csv
import hashlib
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
    temp = path.with_name(path.name + "." + secrets.token_hex(6) + ".tmp")
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
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
    except BaseException:
        try:
            temp.unlink(missing_ok=True)
        except OSError:
            pass
        raise


class Vault:
    def __init__(self, root: Path):
        self.root = root
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        key_path = root / "vault.key"
        protected = [root / "credentials.enc", root / "signing.enc", root / "independent_login.enc"]
        external = os.environ.get("TGWITNESS_VAULT_KEY_FILE")
        keyring_env = os.environ.get("TGWITNESS_VAULT_KEYRING", "").strip()
        marker = root / "vault.external.json"
        keyring_marker = root / "vault.keyring.json"
        if external and keyring_env:
            raise RuntimeError("Choose either TGWITNESS_VAULT_KEY_FILE or TGWITNESS_VAULT_KEYRING, not both.")
        if marker.exists() and keyring_marker.exists():
            raise RuntimeError("Conflicting vault markers (vault.external.json and vault.keyring.json).")
        if external or marker.exists():
            self.key_mode = "external"
        elif keyring_env or keyring_marker.exists():
            self.key_mode = "keyring"
        else:
            self.key_mode = "local"
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
        elif self.key_mode == "keyring":
            if key_path.exists() or (not keyring_marker.exists() and any(p.exists() for p in protected)):
                raise RuntimeError("This data directory still uses its local vault key. Stop TgWitness and run: python -m tgwitness.security migrate-to-keyring --data-dir DATA")
            service, account, salt = _load_or_create_keyring_marker(root, keyring_marker, keyring_env)
            store = KeyringStore(service)
            stored = store.get(account)
            if stored is None:
                if any(p.exists() for p in protected):
                    raise RuntimeError("Vault master key missing from OS keyring (" + service + " / " + account + "). Restore it; refusing key replacement.")
                master = Fernet.generate_key()
                store.set(account, master.decode("ascii"))
                if store.get(account) != master.decode("ascii"):
                    raise RuntimeError("OS keyring did not retain the stored vault master key.")
            else:
                master = stored.strip().encode("ascii")
            Fernet(master)
            self.fernet = keyring_fernet(master, salt)
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
        if not os.fstat(self.stream.fileno()).st_size:
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
        try:
            self.stream.truncate(1)
            self.stream.write(b" " + str(os.getpid()).encode())
            self.stream.flush()
        except OSError:
            pass

    def close(self):
        self.stream.close()


def instance_holder(root: Path):
    try:
        stream = (root / ".instance.lock").open("rb")
    except OSError:
        return None
    with stream:
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_SH | fcntl.LOCK_NB)
                fcntl.flock(stream, fcntl.LOCK_UN)
            return None
        except OSError:
            pass
        stream.seek(1)
        text = stream.read(24).strip()
        return int(text) if text.isdigit() else 0


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
KEYRING_FORMAT = "tgwitness-keyring-vault-v1"
KEYRING_SERVICE_DEFAULT = "TgWitness"
KEYRING_CHUNK = 1200
_KEYRING_OVERRIDE = None


def external_fernet(master, salt):
    key = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt,
               info=b"TgWitness external vault v1").derive(base64.urlsafe_b64decode(master))
    return Fernet(base64.urlsafe_b64encode(key))


def keyring_fernet(master, salt):
    key = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt,
               info=b"TgWitness keyring vault v1").derive(base64.urlsafe_b64decode(master))
    return Fernet(base64.urlsafe_b64encode(key))


def set_keyring_backend(backend):
    """Override the OS keyring backend (primarily for isolated tests)."""
    global _KEYRING_OVERRIDE
    _KEYRING_OVERRIDE = backend


class _WindowsCredentialBackend:
    """Zero-dependency Windows Credential Manager (DPAPI-protected) backend via advapi32."""

    CRED_TYPE_GENERIC = 1
    CRED_PERSIST_LOCAL_MACHINE = 2

    def __init__(self):
        import ctypes
        from ctypes import wintypes

        class FILETIME(ctypes.Structure):
            _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]

        class CREDENTIALW(ctypes.Structure):
            _fields_ = [
                ("Flags", wintypes.DWORD),
                ("Type", wintypes.DWORD),
                ("TargetName", wintypes.LPWSTR),
                ("Comment", wintypes.LPWSTR),
                ("LastWritten", FILETIME),
                ("CredentialBlobSize", wintypes.DWORD),
                ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
                ("Persist", wintypes.DWORD),
                ("AttributeCount", wintypes.DWORD),
                ("Attributes", ctypes.c_void_p),
                ("TargetAlias", wintypes.LPWSTR),
                ("UserName", wintypes.LPWSTR),
            ]

        advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
        advapi32.CredWriteW.argtypes = [ctypes.POINTER(CREDENTIALW), wintypes.DWORD]
        advapi32.CredWriteW.restype = wintypes.BOOL
        advapi32.CredReadW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(CREDENTIALW))]
        advapi32.CredReadW.restype = wintypes.BOOL
        advapi32.CredDeleteW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD]
        advapi32.CredDeleteW.restype = wintypes.BOOL
        advapi32.CredFree.argtypes = [ctypes.c_void_p]
        advapi32.CredFree.restype = None
        self._ctypes = ctypes
        self._CREDENTIALW = CREDENTIALW
        self._advapi32 = advapi32

    @staticmethod
    def _target(service, key):
        return service + ":" + key

    def get_password(self, service, key):
        ptr = self._ctypes.POINTER(self._CREDENTIALW)()
        ok = self._advapi32.CredReadW(self._target(service, key), self.CRED_TYPE_GENERIC, 0, self._ctypes.byref(ptr))
        if not ok:
            err = self._ctypes.get_last_error()
            if err == 1168:  # ERROR_NOT_FOUND
                return None
            raise RuntimeError("Windows Credential Manager read failed (error " + str(err) + ")")
        try:
            cred = ptr.contents
            raw = bytes(cred.CredentialBlob[:cred.CredentialBlobSize])
            return raw.decode("utf-16-le")
        finally:
            self._advapi32.CredFree(ptr)

    def set_password(self, service, key, value):
        blob = value.encode("utf-16-le")
        buf = (self._ctypes.c_ubyte * len(blob)).from_buffer_copy(blob)
        cred = self._CREDENTIALW()
        cred.Type = self.CRED_TYPE_GENERIC
        cred.TargetName = self._target(service, key)
        cred.UserName = key
        cred.CredentialBlobSize = len(blob)
        cred.CredentialBlob = buf
        cred.Persist = self.CRED_PERSIST_LOCAL_MACHINE
        if not self._advapi32.CredWriteW(self._ctypes.byref(cred), 0):
            err = self._ctypes.get_last_error()
            raise RuntimeError("Windows Credential Manager write failed (error " + str(err) + ")")

    def delete_password(self, service, key):
        ok = self._advapi32.CredDeleteW(self._target(service, key), self.CRED_TYPE_GENERIC, 0)
        if not ok:
            err = self._ctypes.get_last_error()
            if err != 1168:
                raise RuntimeError("Windows Credential Manager delete failed (error " + str(err) + ")")


def _resolve_keyring_backend():
    if _KEYRING_OVERRIDE is not None:
        return _KEYRING_OVERRIDE
    try:
        import keyring
        backend = keyring.get_keyring()
        name = type(backend).__name__.lower()
        module = type(backend).__module__.lower()
        if "fail" not in name and "null" not in name and "fail" not in module and "null" not in module:
            return keyring
    except Exception:
        pass
    if os.name == "nt":
        return _WindowsCredentialBackend()
    return None


def keyring_available():
    return _resolve_keyring_backend() is not None


class KeyringStore:
    """Chunked OS keyring wrapper (respects Windows Credential Manager ~2.5 KiB blob limit)."""

    def __init__(self, service=KEYRING_SERVICE_DEFAULT, backend=None):
        self.service = (service or KEYRING_SERVICE_DEFAULT).strip() or KEYRING_SERVICE_DEFAULT
        self._backend = backend

    def _require(self):
        backend = self._backend or _resolve_keyring_backend()
        if backend is None:
            raise RuntimeError("No OS keyring backend is available. Install tgwitness[keyring] or use TGWITNESS_VAULT_KEY_FILE.")
        return backend

    def get(self, key):
        backend = self._require()
        try:
            head = backend.get_password(self.service, key)
        except Exception as exc:
            raise RuntimeError("Could not read from OS keyring: " + str(exc)) from None
        if head is None or not head.startswith("chunks:"):
            return head
        try:
            count = int(head.split(":", 1)[1])
        except ValueError:
            raise RuntimeError("Corrupted chunked secret header in OS keyring.") from None
        parts = []
        for idx in range(count):
            part = backend.get_password(self.service, key + "#" + str(idx))
            if part is None:
                raise RuntimeError("Incomplete chunked secret in OS keyring.")
            parts.append(part)
        return "".join(parts)

    def set(self, key, value):
        backend = self._require()
        self.delete(key)
        if len(value) <= KEYRING_CHUNK:
            backend.set_password(self.service, key, value)
            return
        parts = [value[i:i + KEYRING_CHUNK] for i in range(0, len(value), KEYRING_CHUNK)]
        for idx, part in enumerate(parts):
            backend.set_password(self.service, key + "#" + str(idx), part)
        backend.set_password(self.service, key, "chunks:" + str(len(parts)))

    def delete(self, key):
        backend = self._require()
        try:
            head = backend.get_password(self.service, key)
        except Exception:
            head = None
        if head and head.startswith("chunks:"):
            try:
                count = int(head.split(":", 1)[1])
            except ValueError:
                count = 0
            for idx in range(count):
                try:
                    backend.delete_password(self.service, key + "#" + str(idx))
                except Exception:
                    pass
        try:
            backend.delete_password(self.service, key)
        except Exception:
            pass


def _keyring_service_name(env_value):
    cleaned = (env_value or "").strip()
    if cleaned.lower() in ("", "1", "true", "yes", "auto"):
        return KEYRING_SERVICE_DEFAULT
    return cleaned


def _default_keyring_account(root: Path):
    import hashlib
    resolved = str(Path(root).resolve())
    return "vault-" + hashlib.sha256(resolved.encode("utf-8")).hexdigest()[:16]


def read_keyring_marker(marker: Path):
    try:
        config = json.loads(marker.read_bytes())
        salt = base64.b64decode(config["salt"], validate=True)
        service = str(config["service"]).strip()
        account = str(config["account"]).strip()
    except (OSError, ValueError, KeyError, TypeError):
        raise RuntimeError("Invalid keyring vault metadata; restore the original file.") from None
    if config.get("format") != KEYRING_FORMAT or len(salt) != 32 or not service or not account:
        raise RuntimeError("Invalid keyring vault metadata; restore the original file.")
    return service, account, salt


def _load_or_create_keyring_marker(root: Path, marker: Path, env_value: str):
    if marker.exists():
        return read_keyring_marker(marker)
    service = _keyring_service_name(env_value)
    account = _default_keyring_account(root)
    salt = os.urandom(32)
    private_write(marker, json.dumps({
        "format": KEYRING_FORMAT,
        "service": service,
        "account": account,
        "salt": base64.b64encode(salt).decode(),
    }).encode())
    return service, account, salt


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
        count, after = 0, None
        with db:
            while True:
                rows = db.execute("SELECT run_id, user_id, peer FROM profiling_users WHERE peer IS NOT NULL"
                                  + (" AND (run_id, user_id) > (?, ?)" if after else "")
                                  + " ORDER BY run_id, user_id LIMIT 500", after or ()).fetchall()
                if not rows:
                    return count
                count += len(rows)
                after = rows[-1][:2]
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
    finally:
        db.close()


def reencrypt(folder, local, target):
    files, digests = vault_files(folder), {}
    for path in files:
        data = local.decrypt(path.read_bytes())
        digests[path] = hashlib.sha256(data).digest()
        private_write(path.with_name(path.name + ".new"), target.encrypt(data))
        del data
    for path in files:
        os.replace(path, path.with_name(path.name + ".local"))
        os.replace(path.with_name(path.name + ".new"), path)
    peers = migrate_peers(folder, local, target)
    for path in files:
        if hashlib.sha256(target.decrypt(path.read_bytes())).digest() != digests[path]:
            raise RuntimeError("Re-encrypted vault file does not read back: " + path.name)
    return files, peers


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
            files, peers = reencrypt(folder, local, external)
            key_path.unlink()
            for path in files:
                path.with_name(path.name + ".local").unlink()
            moved.append({"workspace": str(folder.relative_to(root)) if folder != root else "default",
                          "files": len(files), "peers": peers})
    finally:
        lock.close()
    return moved


def migrate_to_keyring(root, service=None, account=None, *, store=None):
    root = Path(root).resolve()
    service = _keyring_service_name(service)
    account = (account or "").strip() or _default_keyring_account(root)
    kr = store or KeyringStore(service)
    existing = kr.get(account)
    if existing is None:
        master = Fernet.generate_key()
        kr.set(account, master.decode("ascii"))
        if kr.get(account) != master.decode("ascii"):
            raise RuntimeError("OS keyring did not retain the stored vault master key.")
    else:
        master = existing.strip().encode("ascii")
        Fernet(master)
    folders = [root, *(sorted(p for p in (root / "profiles").iterdir() if p.is_dir()) if (root / "profiles").is_dir() else [])]
    lock = InstanceLock(root)
    moved = []
    try:
        for folder in folders:
            key_path, marker = folder / "vault.key", folder / "vault.keyring.json"
            if (folder / "vault.external.json").exists():
                raise RuntimeError("Workspace already uses an external key file: " + str(folder))
            if not key_path.exists():
                for kept in vault_files(folder, ".enc.local"):
                    kept.unlink()
                continue
            for kept in vault_files(folder, ".enc.local"):
                os.replace(kept, kept.with_name(kept.name[:-6]))
            local = Fernet(key_path.read_bytes())
            if marker.exists():
                m_service, m_account, salt = read_keyring_marker(marker)
                if (m_service, m_account) != (service, account):
                    raise RuntimeError("Existing vault.keyring.json points to a different keyring entry.")
            else:
                salt = os.urandom(32)
            target = keyring_fernet(master, salt)
            private_write(marker, json.dumps({
                "format": KEYRING_FORMAT,
                "service": service,
                "account": account,
                "salt": base64.b64encode(salt).decode(),
            }).encode())
            files, peers = reencrypt(folder, local, target)
            key_path.unlink()
            for path in files:
                path.with_name(path.name + ".local").unlink()
            moved.append({"workspace": str(folder.relative_to(root)) if folder != root else "default",
                          "files": len(files), "peers": peers, "service": service, "account": account})
    finally:
        lock.close()
    return moved


def export_keyring_key(destination, *, data_dir=None, service=None, account=None, store=None):
    destination = Path(destination)
    if data_dir is not None:
        marker = Path(data_dir).resolve() / "vault.keyring.json"
        if marker.exists():
            m_service, m_account, _ = read_keyring_marker(marker)
            service = service or m_service
            account = account or m_account
        elif not account:
            account = _default_keyring_account(Path(data_dir))
    service = _keyring_service_name(service)
    if not account:
        raise ValueError("Provide --data-dir or --account to locate the keyring entry.")
    kr = store or KeyringStore(service)
    stored = kr.get(account)
    if not stored:
        raise RuntimeError("No vault master key found in OS keyring (" + service + " / " + account + ").")
    master = stored.strip().encode("ascii")
    Fernet(master)
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as output:
        output.write(master)
        output.flush()
        os.fsync(output.fileno())
    return {"service": service, "account": account, "path": str(destination.resolve())}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Manage external and OS keyring vault master keys without printing secrets.")
    parser.add_argument("command", choices=["create-master-key", "migrate-to-external", "migrate-to-keyring", "export-keyring-key"])
    parser.add_argument("path", nargs="?", type=Path, help="Master-key file path (for create-master-key, migrate-to-external, export-keyring-key)")
    parser.add_argument("--data-dir", type=Path, help="Data directory to migrate or inspect (the panel must be stopped)")
    parser.add_argument("--service", default=None, help="OS keyring service name (default: TgWitness)")
    parser.add_argument("--account", default=None, help="OS keyring account name (default: derived from --data-dir)")
    args = parser.parse_args()
    if args.command == "migrate-to-keyring":
        if args.data_dir is None:
            parser.exit(2, "Give the data directory with --data-dir.\n")
        try:
            moved = migrate_to_keyring(args.data_dir, service=args.service, account=args.account)
        except InvalidToken:
            parser.exit(1, "Migration stopped: a vault file does not open with the vault.key of its workspace. Restore "
                           "it from a backup and run the command again; vault.key is removed only after every file "
                           "of that workspace reads back.\n")
        except (OSError, ValueError, RuntimeError, sqlite3.Error) as exc:
            parser.exit(1, "Migration stopped: " + str(exc) + "\n")
        for item in moved:
            print("Workspace " + item["workspace"] + ": " + str(item["files"]) + " vault files and "
                  + str(item["peers"]) + " saved profiling peers re-encrypted into OS keyring ("
                  + item["service"] + " / " + item["account"] + "); vault.key removed.")
        print("Back up the keyring master key offline with: python -m tgwitness.security export-keyring-key BACKUP.key --data-dir "
              + str(Path(args.data_dir).resolve()))
        return
    if args.command == "export-keyring-key":
        if args.path is None:
            parser.exit(2, "Give the destination backup key file path.\n")
        try:
            info = export_keyring_key(args.path, data_dir=args.data_dir, service=args.service, account=args.account)
        except (OSError, ValueError, RuntimeError) as exc:
            parser.exit(1, "Could not export keyring master key: " + str(exc) + "\n")
        print("Master key exported from OS keyring (" + info["service"] + " / " + info["account"]
              + ") to " + info["path"] + ". Keep this backup separate from the data directory.")
        return
    if args.command == "migrate-to-external":
        if args.data_dir is None or args.path is None:
            parser.exit(2, "Give the master-key file path and --data-dir.\n")
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
    if args.path is None:
        parser.exit(2, "Give the destination key file path.\n")
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
