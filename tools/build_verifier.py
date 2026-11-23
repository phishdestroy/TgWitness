"""Build a portable verifier with its own runtime for Windows, Linux or macOS; no recipient installation."""
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.build_portable import HOST_ARCH, PYTHON, VERSION, embedded_runtime  # noqa: E402
from tools.sync_verifier_languages import validate  # noqa: E402

VERIFIER_LANGUAGES = json.loads((ROOT / "tgwitness/verifier_languages.json").read_text(encoding="utf-8"))
# python-build-standalone CPython, the same version as the Windows embeddable runtime; hashes from the release SHA256SUMS.
STANDALONE_RELEASE = "20250409"
STANDALONE = {
    ("linux", "x86_64"): ("linux-x86_64", "x86_64-unknown-linux-gnu",
                          "8c59b9ac6bff2dc3934181d7bc82594f9f59a613afed8d72c9e89d7194e790ee"),
    ("darwin", "arm64"): ("macos-arm64", "aarch64-apple-darwin",
                          "0be1fe0b35a4d3c382141764ef16ed3b8cc2b4620b657f678daa7b7f8df39699"),
}
# No Intel Mac bundle: the pinned cryptography release publishes macOS wheels for arm64 only.


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def integrity_only(entry):
    """The localized verdict a check without the sender's fingerprint ends with: proof the language took effect."""
    return entry["words"]["INTEGRITY ONLY · MINIMUM FOR EVIDENCE NOT MET"].split(" · ")[0]


def write_launchers(stage, language, interpreter="python/python.exe", macos=False):
    from tgwitness.verification_kit import files, quickstart

    stage = Path(stage)
    launcher = "VERIFY.cmd" if interpreter.endswith(".exe") else "VERIFY.sh"
    for filename, body in files(language).items():
        if filename.startswith("VERIFY.") and filename != launcher:
            continue
        (stage / filename).write_bytes(body)
    (stage.parent / ("VERIFY-language-menu." + launcher.rsplit(".", 1)[1])).write_bytes(files("auto")[launcher])

    def guide(lang):
        note = ("\n" + VERIFIER_LANGUAGES[lang]["reader"]["macos"] + "\n").encode("utf-8") if macos else b""
        return quickstart(lang) + note
    (stage / "README.txt").write_bytes(guide("en" if language == "auto" else language))
    (stage / "languages").mkdir()
    for lang in VERIFIER_LANGUAGES:
        instructions = guide(lang) + b"\n" + (
            interpreter + " -I verify.py archive.zip --interactive --lang " + lang + " --checkpoint retained.json\n"
            + interpreter + " -I verify.py archive.zip --pretty --explain --lang " + lang + " --fingerprint TRUSTED_SHA256 --tsa-ca trusted-root.pem\n"
            + interpreter + " -I verify.py archive.zip --pretty --explain --lang " + lang + " --witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness\n"
            + interpreter + " -I verify.py archive.zip --interactive --lang " + lang + " --max-gib 16\n").encode("utf-8")
        (stage / "languages" / ("START_HERE-" + lang + ".txt")).write_bytes(instructions)


def standalone_runtime(cache, supplied=None):
    entry = STANDALONE.get((sys.platform, platform.machine()))
    if entry is None:
        raise SystemExit("Portable verifiers are built on Windows, Linux x86_64 and macOS on Apple silicon (arm64).")
    label, triple, digest = entry
    name = "cpython-" + PYTHON + "+" + STANDALONE_RELEASE + "-" + triple + "-install_only_stripped.tar.gz"
    archive = Path(supplied) if supplied else cache / name
    if not archive.exists():
        cache.mkdir(parents=True, exist_ok=True)
        url = ("https://github.com/astral-sh/python-build-standalone/releases/download/" + STANDALONE_RELEASE + "/"
               + urllib.parse.quote(name))
        print("Downloading", url, flush=True)
        partial = archive.with_name(archive.name + ".part")
        with urllib.request.urlopen(url, timeout=120) as response, partial.open("wb") as output:
            shutil.copyfileobj(response, output)
        partial.replace(archive)
    if sha256(archive) != digest:
        raise SystemExit("Portable Python archive checksum mismatch: " + str(archive))
    return label, archive


def flatten_links(stage):
    """ZIP archives carry no links: keep one real python3 and replace every other link with a copy of its target."""
    binary = stage / "python/bin"
    real = (binary / "python3").resolve()
    for entry in list(binary.iterdir()):
        if entry.is_symlink():
            entry.unlink()
    if real.name != "python3":
        real.rename(binary / "python3")
    root = stage.resolve()
    for path in sorted(stage.rglob("*")):
        if path.is_symlink():
            target = path.resolve()
            if not target.is_relative_to(root) or not target.exists():
                raise SystemExit("Refusing a link outside the portable runtime: " + str(path))
            path.unlink()
            if target.is_dir():
                shutil.copytree(target, path)
            else:
                shutil.copy2(target, path)


def package(stage, name, output_dir):
    shipped = sorted(p for p in stage.rglob("*") if p.is_file())
    if any(p.is_symlink() or getattr(p, "is_junction", lambda: False)() for p in stage.rglob("*")):
        raise SystemExit("Refusing linked files in portable verifier")
    (stage / "SHA256SUMS").write_text("".join(sha256(p) + "  " + p.relative_to(stage).as_posix() + "\n"
                                              for p in shipped), encoding="utf-8", newline="\n")
    shipped.append(stage / "SHA256SUMS")
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / (name + ".zip")
    partial = output.with_suffix(".zip.part")
    with zipfile.ZipFile(partial, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in shipped:
            archive.write(path, name + "/" + path.relative_to(stage).as_posix())
    checksum = output.with_name(output.name + ".sha256.part")
    checksum.write_text(sha256(partial) + "  " + output.name + "\n", encoding="ascii", newline="\n")
    output.with_suffix(".zip.sha256").unlink(missing_ok=True)
    partial.replace(output)
    checksum.replace(output.with_suffix(".zip.sha256"))
    print("Portable verifier:", output)
    print("MiB:", round(output.stat().st_size / 1024**2, 1))
    print("SHA-256:", sha256(output))


def build_windows(args):
    arch = HOST_ARCH.get(platform.machine().upper())
    if sys.version_info[:2] != (3, 12) or not arch:
        raise SystemExit("Build on 64-bit Windows with Python 3.12 so the wheels match the embedded runtime.")
    work = ROOT / "build/verifier"
    work.mkdir(parents=True, exist_ok=True)
    runtime = embedded_runtime(arch, ROOT / "build/portable/cache", args.python_zip)
    name = "TgWitness-verifier-" + VERSION + "-windows-" + arch + "-" + ("all" if args.language == "auto" else args.language)
    with tempfile.TemporaryDirectory(prefix="stage-", dir=work) as temporary:
        stage = Path(temporary) / name
        (stage / "python").mkdir(parents=True)
        with zipfile.ZipFile(runtime) as archive:
            archive.extractall(stage / "python")
        tag = "python" + PYTHON.replace(".", "")[:3]
        (stage / "python" / (tag + "._pth")).write_text(
            tag + ".zip\n.\nLib\\site-packages\nimport site\n", encoding="ascii")
        subprocess.run([sys.executable, "-m", "pip", "install", "--disable-pip-version-check",
                        "--only-binary=:all:", "--no-compile", "--no-warn-script-location", "--require-hashes",
                        "--target", str(stage / "python/Lib/site-packages"),
                        "-r", str(ROOT / "deploy/installer.lock")], check=True)
        shutil.copyfile(ROOT / "tgwitness/verify.py", stage / "verify.py")
        subprocess.run([str(stage / "python/python.exe"), "-I", "-B", "-X", "utf8", "-c",
                        "import sys; sys.path.insert(0, sys.argv[1]); "
                        "from tools.build_verifier import write_launchers; write_launchers(sys.argv[2], sys.argv[3])",
                        str(ROOT), str(stage), args.language], check=True)
        default_launcher = (stage / "VERIFY.cmd").read_bytes()
        menu_launcher = (stage.parent / "VERIFY-language-menu.cmd").read_bytes()
        for filename in ("LICENSE", "NOTICE"):
            shutil.copyfile(ROOT / filename, stage / filename)
        checked = subprocess.run([str(stage / "python/python.exe"), "-I", "-B", "-X", "utf8",
                                  str(stage / "verify.py"), str(args.validation_archive),
                                  "--json"], capture_output=True, text=True, encoding="utf-8")
        if checked.returncode or not json.loads(checked.stdout).get("verified"):
            raise SystemExit("Portable verifier failed its signed-archive check: " + checked.stdout + checked.stderr)
        probe = Path(temporary) / "Renamed (synthetic).zip"
        shutil.copyfile(args.validation_archive, probe)
        env = {**os.environ, "PATH": str(Path(os.environ["SystemRoot"]) / "System32"),
               "TGWITNESS_VERIFY_NO_PAUSE": "1"}
        command = '"' + os.environ["COMSPEC"] + '" /d /s /c ""' + str(stage / "VERIFY.cmd") + '" "' + str(probe) + '""'
        for expected in (0, 1):
            if expected:
                with zipfile.ZipFile(probe, "a") as archive:
                    archive.writestr("unsigned-change.txt", "synthetic tamper")
            checked = subprocess.run(command, input=("en\n" if args.language == "auto" else "") + "\n", env=env, cwd=stage, capture_output=True,
                                     text=True, encoding="utf-8", creationflags=subprocess.CREATE_NO_WINDOW)
            if checked.returncode != expected:
                raise SystemExit("Portable VERIFY.cmd returned an incorrect status: " + checked.stdout + checked.stderr)
        if len(list(Path(temporary).glob("verify-result-*.txt"))) != 2:
            raise SystemExit("Portable VERIFY.cmd did not save both verification transcripts")
        print("VERIFY.cmd: clean/tampered ZIP and saved transcripts passed with system Python absent from PATH.")
        shutil.copyfile(args.validation_archive, probe)
        (stage / "VERIFY.cmd").write_bytes(menu_launcher)
        for lang, entry in VERIFIER_LANGUAGES.items():
            checked = subprocess.run(command, input=lang + "\n\n", env=env, cwd=stage, capture_output=True,
                                     text=True, encoding="utf-8", creationflags=subprocess.CREATE_NO_WINDOW, timeout=45)
            if checked.returncode or integrity_only(entry) not in checked.stdout:
                raise SystemExit("Portable language check failed: " + lang + "\n" + checked.stdout + checked.stderr)
        (stage / "VERIFY.cmd").write_bytes(default_launcher)
        print("All", len(VERIFIER_LANGUAGES), "languages passed through VERIFY.cmd without system Python on PATH.")
        package(stage, name, args.output)


def build_unix(args):
    work = ROOT / "build/verifier"
    work.mkdir(parents=True, exist_ok=True)
    label, runtime = standalone_runtime(ROOT / "build/portable/cache", args.python_archive)
    name = "TgWitness-verifier-" + VERSION + "-" + label + "-" + ("all" if args.language == "auto" else args.language)
    with tempfile.TemporaryDirectory(prefix="stage-", dir=work) as temporary:
        stage = Path(temporary) / name
        stage.mkdir(parents=True)
        with tarfile.open(runtime) as archive:
            archive.extractall(stage, filter="data")
        python = stage / "python/bin/python3"
        subprocess.run([str(python), "-I", "-m", "pip", "install", "--disable-pip-version-check",
                        "--no-warn-script-location", "--only-binary=:all:", "--no-compile",
                        "--require-hashes", "-r", str(ROOT / "deploy/installer.lock")], check=True)
        subprocess.run([str(python), "-I", "-m", "pip", "uninstall", "--yes", "--disable-pip-version-check", "pip"],
                       check=True)
        flatten_links(stage)
        shutil.copyfile(ROOT / "tgwitness/verify.py", stage / "verify.py")
        subprocess.run([str(python), "-I", "-B", "-X", "utf8", "-c",
                        "import sys; sys.path.insert(0, sys.argv[1]); "
                        "from tools.build_verifier import write_launchers; "
                        "write_launchers(sys.argv[2], sys.argv[3], 'python/bin/python3', sys.argv[4] == 'macos')",
                        str(ROOT), str(stage), args.language, label.split("-")[0]], check=True)
        (stage / "VERIFY.sh").chmod(0o755)
        default_launcher = (stage / "VERIFY.sh").read_bytes()
        menu_launcher = (stage.parent / "VERIFY-language-menu.sh").read_bytes()
        for filename in ("LICENSE", "NOTICE"):
            shutil.copyfile(ROOT / filename, stage / filename)
        checked = subprocess.run([str(python), "-I", "-B", "-X", "utf8", str(stage / "verify.py"),
                                  str(args.validation_archive), "--json"], capture_output=True, text=True, encoding="utf-8")
        if checked.returncode or not json.loads(checked.stdout).get("verified"):
            raise SystemExit("Portable verifier failed its signed-archive check: " + checked.stdout + checked.stderr)
        probe = Path(temporary) / "Renamed (synthetic).zip"
        shutil.copyfile(args.validation_archive, probe)
        # PATH holds only dirname: no Python is reachable, so the launcher has to use the runtime beside it.
        tools = Path(temporary) / "path"
        tools.mkdir()
        (tools / "dirname").symlink_to(shutil.which("dirname"))
        env = {"PATH": str(tools), "HOME": temporary, "LANG": "C.UTF-8", "TGWITNESS_VERIFY_NO_PAUSE": "1"}
        command = ["/bin/sh", str(stage / "VERIFY.sh"), str(probe)]
        for expected in (0, 1):
            if expected:
                with zipfile.ZipFile(probe, "a") as archive:
                    archive.writestr("unsigned-change.txt", "synthetic tamper")
            checked = subprocess.run(command, input=("en\n" if args.language == "auto" else "") + "\n", env=env, cwd=stage,
                                     capture_output=True, text=True, encoding="utf-8", timeout=120)
            if checked.returncode != expected:
                raise SystemExit("Portable VERIFY.sh returned an incorrect status: " + checked.stdout + checked.stderr)
        if len(list(Path(temporary).glob("verify-result-*.txt"))) != 2:
            raise SystemExit("Portable VERIFY.sh did not save both verification transcripts")
        print("VERIFY.sh: clean/tampered ZIP and saved transcripts passed with no Python on PATH.")
        shutil.copyfile(args.validation_archive, probe)
        (stage / "VERIFY.sh").write_bytes(menu_launcher)
        for lang, entry in VERIFIER_LANGUAGES.items():
            checked = subprocess.run(command, input=lang + "\n\n", env=env, cwd=stage, capture_output=True,
                                     text=True, encoding="utf-8", timeout=45)
            if checked.returncode or integrity_only(entry) not in checked.stdout:
                raise SystemExit("Portable language check failed: " + lang + "\n" + checked.stdout + checked.stderr)
        (stage / "VERIFY.sh").write_bytes(default_launcher)
        print("All", len(VERIFIER_LANGUAGES), "languages passed through VERIFY.sh with no Python on PATH.")
        package(stage, name, args.output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python-zip", type=Path, help="Windows: python.org embeddable runtime (downloaded when omitted)")
    parser.add_argument("--python-archive", type=Path,
                        help="Linux/macOS: python-build-standalone runtime (downloaded when omitted)")
    parser.add_argument("--language", choices=("auto", *VERIFIER_LANGUAGES), default="auto",
                        help="Default language; auto shows a language menu. Every build includes all languages.")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--validation-archive", type=Path, default=ROOT / "website/demo/downloads/tgwitness-demo.zip",
                        help="Signed synthetic evidence archive used to validate the packaged runtime and launchers")
    args = parser.parse_args()
    if not args.validation_archive.is_file():
        raise SystemExit("Validation archive not found: " + str(args.validation_archive))
    validate(VERIFIER_LANGUAGES)
    subprocess.run([sys.executable, str(ROOT / "tools/sync_verifier_languages.py"), "--check"], check=True)
    if os.name == "nt":
        build_windows(args)
    else:
        build_unix(args)


if __name__ == "__main__":
    main()
