import base64
import hashlib
import importlib
import importlib.metadata
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import tempfile
from pathlib import Path


def port_holder(root, port):
    from .security import instance_holder
    holder = instance_holder(root)
    if holder is None:
        return "fail", "Use a local IP and available port; a running instance may already own it."
    try:
        from .panelctl import listening_pid
        listener = listening_pid(port)
    except (OSError, ValueError, subprocess.SubprocessError):
        listener = None
    if holder and listener == holder:
        return "pass", "The panel of this data directory (process " + str(holder) + ") holds the port"
    if holder and listener:
        return "fail", ("Process " + str(listener) + " holds the port, not the panel of this data directory (process "
                        + str(holder) + "). Choose another port; nothing was stopped.")
    return "warning", ("The port is in use and this data directory is open in a running process; "
                       "the check could not confirm that this panel holds the port.")


def changed_program_files():
    try:
        files = importlib.metadata.distribution("tgwitness").files or []
    except importlib.metadata.PackageNotFoundError:
        return []
    changed = []
    for item in files:
        name = str(item)
        if not item.hash or not name.startswith("tgwitness/"):
            continue
        try:
            digest = hashlib.new(item.hash.mode, item.locate().read_bytes()).digest()
        except (OSError, ValueError):
            changed.append(name)
            continue
        if base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii") != item.hash.value:
            changed.append(name)
    return changed


def inspect_environment(root, host="127.0.0.1", port=8787):
    root = Path(root).resolve()
    checks = []

    def add(name, status, detail):
        checks.append({"name": name, "status": status, "detail": detail})

    add("python", "pass" if sys.version_info >= (3, 11) else "fail", platform.python_version())
    for distribution, module in (("fastapi", "fastapi"), ("uvicorn", "uvicorn"),
                                  ("telethon", "telethon"), ("cryptography", "cryptography"),
                                  ("python-socks", "python_socks"), ("qrcode", "qrcode")):
        try:
            importlib.import_module(module)
            add(distribution, "pass", importlib.metadata.version(distribution))
        except Exception as exc:
            add(distribution, "fail", "Install/repair the project environment: " + type(exc).__name__)
    from .mcp_server import runtime_status
    mcp = runtime_status()
    add("mcp", "pass" if mcp["available"] else "warning",
        "streamable-http available" if mcp["available"] else
        "Optional MCP support is unavailable. " + mcp["install_command"])
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        key = Ed25519PrivateKey.generate()
        key.public_key().verify(key.sign(b"local readiness probe"), b"local readiness probe")
        add("signing_backend", "pass", "Ed25519 sign/verify available")
    except Exception as exc:
        add("signing_backend", "fail", type(exc).__name__)

    parent = root
    while not parent.exists() and parent.parent != parent:
        parent = parent.parent
    try:
        if not parent.is_dir():
            raise NotADirectoryError()
        with tempfile.TemporaryFile(prefix="tgwitness-check-", dir=parent) as probe:
            probe.write(b"write probe")
            probe.flush()
            os.fsync(probe.fileno())
        free = shutil.disk_usage(parent).free
        add("storage", "pass" if free >= 1024**3 else "warning",
            f"Write probe passed; {free // 1024**2} MiB free. Exports use the profile's private temporary directory.")
        if root.exists():
            from .security import owner_only_state
            limited, how = owner_only_state(root)
            add("data_permissions", "pass" if limited else "warning",
                "Only this account can open the data directory (" + how + ")" if limited else
                "Other local accounts may read the data directory and its keys (" + how + "). TgWitness limits it "
                "at startup where the file system allows; keep it on NTFS or a Unix file system.")
    except OSError as exc:
        add("storage", "fail", "Data path is not writable: " + type(exc).__name__)
    import ipaddress
    try:
        if not 1 <= port <= 65535:
            raise ValueError()
        address = ipaddress.ip_address("127.0.0.1" if host == "localhost" else host)
    except ValueError:
        address = None
        add("listen_address", "fail", "Use a local IP address and a port from 1 to 65535.")
    if address is not None:
        try:
            with socket.socket(socket.AF_INET6 if address.version == 6 else socket.AF_INET) as probe:
                probe.bind((str(address), port))
            add("listen_address", "pass", "Address and port available at check time")
        except OSError:
            add("listen_address", *port_holder(root, port))

    external = os.environ.get("TGWITNESS_VAULT_KEY_FILE")
    keyring_env = os.environ.get("TGWITNESS_VAULT_KEYRING", "").strip()
    marker = root / "vault.external.json"
    keyring_marker = root / "vault.keyring.json"
    if external and keyring_env:
        add("vault_mode", "fail", "Set either TGWITNESS_VAULT_KEY_FILE or TGWITNESS_VAULT_KEYRING, not both")
    elif external:
        try:
            source = Path(external).resolve(strict=True)
            if source.is_relative_to(root) or source.stat().st_size > 128:
                raise ValueError()
            key = base64.b64decode(source.read_bytes().strip(), altchars=b"-_", validate=True)
            if len(key) != 32 or (root / "vault.key").exists():
                raise ValueError()
            add("external_key", "pass", "Key file is readable and separate; existing vault decryption is checked at startup")
        except (OSError, ValueError):
            add("external_key", "fail", "Check the external key file and vault mode; no secret values were displayed")
    elif marker.exists():
        add("external_key", "fail", "This data directory requires TGWITNESS_VAULT_KEY_FILE")
    elif keyring_marker.exists() or keyring_env:
        try:
            from .security import KeyringStore, keyring_available, read_keyring_marker, security_command
            if not keyring_available():
                raise RuntimeError("OS keyring backend is unavailable; install tgwitness[keyring] or use TGWITNESS_VAULT_KEY_FILE")
            if (root / "vault.key").exists():
                raise RuntimeError("Local vault.key still exists; run " + security_command("migrate-to-keyring --data-dir " + str(root)))
            if keyring_marker.exists():
                service, account, _ = read_keyring_marker(keyring_marker)
                stored = KeyringStore(service).get(account)
                if not stored:
                    raise RuntimeError("Master key not found in OS keyring (" + service + " / " + account + ")")
                key = base64.b64decode(stored.strip().encode("ascii"), altchars=b"-_", validate=True)
                if len(key) != 32:
                    raise ValueError("Invalid key length in OS keyring")
            add("keyring_key", "pass", "Master key is stored in the OS keyring and readable")
        except (OSError, ValueError, RuntimeError) as exc:
            add("keyring_key", "fail", str(exc))
    else:
        from .security import security_command
        add("vault_mode", "warning", "vault.key sits next to the encrypted session and signing key, so any copy of the data directory opens them. "
            "Move it to the OS keyring (" + security_command("migrate-to-keyring --data-dir " + str(root)) + ") or an external file ("
            + security_command("create-master-key KEYFILE") + " && " + security_command("migrate-to-external KEYFILE --data-dir " + str(root)) + ")")
    changed = changed_program_files()
    add("program_files", "warning" if changed else "pass",
        str(len(changed)) + " program files differ from the installed release: " + ", ".join(changed[:5])
        + (" and " + str(len(changed) - 5) + " more" if len(changed) > 5 else "") + ". Reinstall the release."
        if changed else "Program files match the installed release")
    if os.environ.get("TGWITNESS_TOKEN") and len(os.environ["TGWITNESS_TOKEN"]) < 24:
        add("panel_token", "fail", "TGWITNESS_TOKEN must contain at least 24 characters")
    return {"ready": not any(c["status"] == "fail" for c in checks), "platform": platform.platform(),
            "interpreter": sys.executable, "data_directory": str(root), "checks": checks,
            "scope": "Local startup prerequisites"}


def print_report(report, as_json=False):
    if as_json:
        print(json.dumps(report, indent=2))
    else:
        print("TgWitness deployment check · " + report["scope"])
        print("Python:", report["interpreter"])
        print("Data:", report["data_directory"])
        for item in report["checks"]:
            print("[" + item["status"].upper() + "] " + item["name"] + ": " + item["detail"])
        print("Ready to attempt startup." if report["ready"] else "Resolve failed checks before starting.")
