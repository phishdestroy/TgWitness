"""Build a self-contained Windows package: the official embeddable Python plus TgWitness.

Run on 64-bit Windows with Python 3.12 (the embedded runtime's version):

    python tools/build_portable.py            # dist/TgWitness-<version>-windows-amd64-portable.zip

The user extracts the ZIP and double-clicks TgWitness.cmd; nothing is installed system-wide.
"""
import argparse
import hashlib
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import tomllib
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
PYTHON = "3.12.10"
# SHA-256 of the python.org embeddable archives, pinned so a changed download fails the build.
EMBED_SHA256 = {
    "amd64": "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3",
    "arm64": "3065efc3d382d1cda66757ac71ade11904fa6e350f5a97eb74811acd71ba5532",
}
HOST_ARCH = {"AMD64": "amd64", "ARM64": "arm64"}

LAUNCHER = """@echo off
setlocal
cd /d "%~dp0"
title TgWitness
"%~dp0python\\python.exe" -m tgwitness %*
if errorlevel 1 pause
"""
DEMO = """@echo off
call "%~dp0TgWitness.cmd" --demo %*
"""
CHECK = """@echo off
setlocal
cd /d "%~dp0"
"%~dp0python\\python.exe" -m tgwitness --check %*
pause
"""
README = """TgWitness {version} - Windows portable package
================================================

Everything needed is inside this folder: TgWitness and an embedded copy of the
official Python {python} runtime. Nothing is installed on the computer.

Start
-----
1. Extract the whole ZIP into a folder you can write to, for example
   Documents\\TgWitness. Do not run it from inside the ZIP or from Program Files.
2. Double-click TgWitness.cmd. Keep the window open while observing.
3. Open http://127.0.0.1:8787 in your browser.
4. Paste the panel token from data\\live\\panel-token.txt.
5. Add your Telegram account, choose chats and start observation. No API ID/hash
   is needed: a built-in pool of public pairs is used; your own pair is optional.

Other launchers
---------------
TgWitness-Demo.cmd   Fictional demo journal; no Telegram account (data\\demo).
TgWitness-Check.cmd  Readiness check of storage, keys and port; does not start.

Options can be added after TgWitness.cmd, for example:
    TgWitness.cmd --port 8790

If Windows asks whether to run a downloaded file, choose Run. To avoid the
prompt, right-click the ZIP, open Properties, tick Unblock, then extract.

Your data
---------
The data folder holds Telegram sessions, signing keys, the journal, media and
exports. Keep it private and back it up while TgWitness is stopped. Message
content and media are not encrypted by TgWitness; use an encrypted disk.

Update
------
Stop TgWitness, extract the new version into a new folder, copy the data folder
from the old one, then start the new TgWitness.cmd.

Documentation: README.md in the source repository and http://127.0.0.1:8787/guide.html
License: MIT for TgWitness (LICENSE); Python and bundled libraries keep their own
licenses (python\\LICENSE.txt and the *.dist-info folders).
"""


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def embedded_runtime(arch, cache, supplied=None):
    archive = Path(supplied) if supplied else cache / ("python-" + PYTHON + "-embed-" + arch + ".zip")
    if not archive.exists():
        cache.mkdir(parents=True, exist_ok=True)
        url = "https://www.python.org/ftp/python/" + PYTHON + "/" + archive.name
        print("Downloading", url, flush=True)
        partial = archive.with_suffix(".part")
        with urllib.request.urlopen(url, timeout=60) as response, partial.open("wb") as output:
            shutil.copyfileobj(response, output)
        partial.replace(archive)
    if sha256(archive) != EMBED_SHA256[arch]:
        raise SystemExit("Embedded Python archive checksum mismatch: " + str(archive))
    return archive


def main():
    parser = argparse.ArgumentParser(description="Build the Windows portable package.")
    parser.add_argument("--python-zip", help="use a local python-" + PYTHON + "-embed-<arch>.zip")
    parser.add_argument("--no-zip", action="store_true", help="build the folder only")
    args = parser.parse_args()
    arch = HOST_ARCH.get(platform.machine().upper())
    if os.name != "nt" or sys.version_info[:2] != (3, 12) or not arch:
        raise SystemExit("Run on 64-bit Windows with Python 3.12 so wheels match the embedded runtime.")

    work = ROOT / "build/portable"
    name = "TgWitness-" + VERSION
    stage = work / name
    shutil.rmtree(stage, ignore_errors=True)
    (stage / "python").mkdir(parents=True)

    with zipfile.ZipFile(embedded_runtime(arch, work / "cache", args.python_zip)) as runtime:
        runtime.extractall(stage / "python")
    tag = "python" + PYTHON.replace(".", "")[:3]
    # Isolated module path: the standard library, the runtime folder and bundled packages only.
    (stage / "python" / (tag + "._pth")).write_text(tag + ".zip\n.\nLib\\site-packages\nimport site\n", encoding="ascii")

    print("Installing TgWitness and pinned dependencies", flush=True)
    site_packages = stage / "python/Lib/site-packages"
    subprocess.run([sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "--no-warn-script-location",
                    "--no-compile", "--target", str(site_packages), "-c", str(ROOT / "constraints.txt"), str(ROOT)],
                   check=True, cwd=ROOT)
    shutil.rmtree(site_packages / "bin", ignore_errors=True)  # Scripts would point at the build interpreter.

    for filename, text in (("TgWitness.cmd", LAUNCHER), ("TgWitness-Demo.cmd", DEMO), ("TgWitness-Check.cmd", CHECK),
                           ("README.txt", README.format(version=VERSION, python=PYTHON))):
        (stage / filename).write_bytes(text.replace("\n", "\r\n").encode("ascii"))
    shutil.copyfile(ROOT / "LICENSE", stage / "LICENSE")

    print("Checking the embedded runtime", flush=True)
    probe = work / "readiness-probe"
    shutil.rmtree(probe, ignore_errors=True)
    environment = {key: value for key, value in os.environ.items() if not key.startswith(("TGWITNESS_", "PYTHON"))}
    # Building a package must also work while a live panel owns the default port.
    with socket.socket() as port_probe:
        port_probe.bind(("127.0.0.1", 0))
        probe_port = port_probe.getsockname()[1]
    result = subprocess.run([str(stage / "python/python.exe"), "-m", "tgwitness", "--check", "--json",
                             "--host", "127.0.0.1", "--port", str(probe_port), "--data-dir", str(probe)],
                            cwd=stage, env=environment, capture_output=True, text=True)
    shutil.rmtree(probe, ignore_errors=True)
    report = json.loads(result.stdout) if result.stdout.strip().startswith("{") else {}
    if result.returncode or not report.get("ready"):
        raise SystemExit("Portable readiness check failed:\n" + result.stdout + result.stderr)
    for compiled in stage.rglob("__pycache__"):
        shutil.rmtree(compiled)

    if args.no_zip:
        print("Portable folder:", stage)
        return
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    target = out / (name + "-windows-" + arch + "-portable.zip")
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(stage.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(work).as_posix())
    digest = sha256(target)
    target.with_suffix(".zip.sha256").write_text(digest + "  " + target.name + "\n", encoding="ascii")
    print("Portable package:", target)
    print("Size:", round(target.stat().st_size / 1024**2, 1), "MiB | SHA-256:", digest)


if __name__ == "__main__":
    main()
