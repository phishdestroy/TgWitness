"""Acceptance helper: an empty, isolated installation on a disposable systemd host."""
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def check_service(app, mode):
    assert app.is_relative_to(Path("/opt")) and app.parent.name.startswith("tgwitness-install-check-")
    service = "tgwitness-" + hashlib.sha256(str(app).encode()).hexdigest()[:12]
    unit = Path("/etc/systemd/system") / (service + ".service")
    assert not unit.exists(), "Acceptance must never reuse an existing service"
    launcher = str(app / "bin" / "tgwitness")
    with socket.socket() as available:
        available.bind(("127.0.0.1", 0))
        port = available.getsockname()[1]
    origin = f"http://127.0.0.1:{port}"

    def run(*args):
        result = subprocess.run([launcher, *args], capture_output=True, text=True, timeout=240)
        if result.returncode:
            # First-run output includes a fresh access key: never publish it in CI.
            safe = "\n".join(line for line in result.stdout.splitlines() if "Access key:" not in line)
            raise AssertionError(safe + "\n" + result.stderr)
        return result.stdout

    def request(url, token=None):
        try:
            headers = {"Authorization": "Bearer " + token} if token else {}
            with urlopen(Request(url, headers=headers), timeout=15) as response:
                return response.status, response.read()
        except HTTPError as exc:
            return exc.code, b""

    try:
        output = run("setup", "--mode", mode, "--port", str(port))
        assert "Your panel is ready" in output
        config = json.loads((app / "panel.json").read_text())
        data = Path(config["data"])
        assert data == Path("/var/lib") / service
        assert subprocess.check_output(["systemctl", "is-enabled", service], text=True).strip() == "enabled"
        token = (data / "panel-token.txt").read_text().strip()
        assert request(origin + "/api/status")[0] == 401
        assert request(origin + "/api/status", token)[0] == 200
        assert token not in run("status")
        address = json.loads((data / "panel-address.json").read_text())["url"]
        if mode == "quick":
            assert address.startswith("https://") and address.endswith(".trycloudflare.com")
            assert request(address + "/api/status")[0] == 401
            assert request(address + "/api/status", token)[0] == 200
        (data / "acceptance-record").write_text("keep this record\n")
        run("restart")
        assert (data / "acceptance-record").read_text() == "keep this record\n"
        assert (data / "panel-token.txt").read_text().strip() == token
        if mode == "quick":
            current = json.loads((data / "panel-address.json").read_text())["url"]
            assert current in run("open")
            assert request(current + "/api/status", token)[0] == 200
        run("stop")
        deadline = time.monotonic() + 10
        while True:
            try:
                request(origin)
            except (URLError, OSError):
                break
            assert time.monotonic() < deadline, "Stop left a listening panel"
            time.sleep(0.2)
        run("start")
        assert request(origin + "/api/status", token)[0] == 200
        assert (data / "acceptance-record").read_text() == "keep this record\n"
        print(f"{mode}: installed panel, authentication, boot enablement, restart, retained data, stop/start: passed")
    finally:
        if unit.exists():
            assert unit.read_text().startswith("# TgWitness managed panel service v1\n")
            subprocess.run(["systemctl", "stop", service], check=True, timeout=60)
            subprocess.run(["systemctl", "clean", "--what=state", service], check=True, timeout=30)
            subprocess.run(["systemctl", "disable", service], check=True, timeout=30)
            unit.unlink()
            subprocess.run(["systemctl", "daemon-reload"], check=True, timeout=30)
