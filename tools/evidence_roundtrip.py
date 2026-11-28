import json
import sqlite3
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tgwitness import report  # noqa: E402
from tgwitness.evidence import export_file, retain_checkpoint  # noqa: E402
from tgwitness.security import Vault  # noqa: E402
from tgwitness.store import Store  # noqa: E402
from tgwitness.verify import fingerprint  # noqa: E402

CHAT = -1001234567890
failures = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" :: " + detail if detail else ""))
    if not ok:
        failures.append(name)


def verify(archive, key, *extra):
    run = subprocess.run([sys.executable, "-I", str(ROOT / "tgwitness" / "verify.py"), str(archive), "--fingerprint", key,
                          "--json", *extra], capture_output=True, text=True)
    try:
        return run.returncode, json.loads(run.stdout)
    except ValueError:
        return run.returncode, {"output": (run.stdout + run.stderr)[-300:]}


def rewrite(source, target, change):
    with zipfile.ZipFile(source) as original, zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as changed:
        for info in original.infolist():
            data = change(info.filename, original.read(info.filename))
            if data is not None:
                changed.writestr(info, data)
        extra = change(None, None)
        if extra:
            changed.writestr(*extra)


with tempfile.TemporaryDirectory() as folder:
    root = Path(folder) / "workspace"
    root.mkdir()
    vault = Vault(root)
    store = Store(root)
    store.bind(vault)
    for number in range(1, 41):
        store.append("message.new", {"text": "synthetic message " + str(number), "sent_at": "2026-11-28T00:00:00+00:00"},
                     CHAT, number)
    store.append("message.edited", {"text": "synthetic message 7 edited"}, CHAT, 7)
    store.append("message.deleted", {"message_ids": [9]}, CHAT, 9)
    store.append("coverage.gap", {"reason": "transport_disconnected", "meaning": "synthetic gap"})
    retain_checkpoint(store, vault)
    key = fingerprint(vault.public_key)
    check("journal verifies", store.verify(vault.public_key)["events"] == 43)

    archive = export_file(store, vault, "zip", report.resolved(store, "en"), include_board=False, require_records=False)
    code, result = verify(archive, key)
    check("exported archive verifies with the retained fingerprint", code == 0 and result.get("verified") is True,
          "exit %d" % code)
    with zipfile.ZipFile(archive) as bundle:
        rows = [json.loads(line) for line in bundle.read("events.jsonl").decode().splitlines()]
        coverage = json.loads(bundle.read("coverage.json"))
    kinds = {row["kind"] for row in rows}
    check("archive holds new, edited and deleted records",
          {"message.new", "message.edited", "message.deleted"} <= kinds, ", ".join(sorted(kinds)))
    check("archive keeps the coverage gap record", "coverage.gap" in kinds and isinstance(coverage, dict))

    code, _ = verify(archive, "0" * 64)
    check("another fingerprint is refused", code != 0, "exit %d" % code)

    def flip(name, data):
        if name == "events.jsonl":
            position = data.index(b"synthetic message 5")
            return data[:position] + b"Synthetic" + data[position + 9:]
        return data
    changed = Path(folder) / "changed-byte.zip"
    rewrite(archive, changed, flip)
    code, result = verify(changed, key)
    check("a changed record is refused", code != 0, str(result.get("error", ""))[:80])

    def add(name, data):
        return ("unexpected.txt", b"added after signing") if name is None else data
    added = Path(folder) / "added-member.zip"
    rewrite(archive, added, add)
    code, result = verify(added, key)
    check("an added file is refused", code != 0, str(result.get("error", ""))[:80])

    def drop(name, data):
        return None if name == "coverage.json" else data
    dropped = Path(folder) / "dropped-member.zip"
    rewrite(archive, dropped, drop)
    code, result = verify(dropped, key)
    check("a removed file is refused", code != 0, str(result.get("error", ""))[:80])

    database = sqlite3.connect(root / "journal.sqlite3")
    with database:
        database.execute("DROP TRIGGER IF EXISTS immutable_update")
        database.execute("UPDATE events SET payload=replace(payload, 'message 3', 'message 8') WHERE seq=3")
    database.close()
    try:
        Store(root).verify(vault.public_key)
        refused = False
    except Exception:
        refused = True
    check("a record changed in the journal file is refused", refused)

if failures:
    print("FAILED: " + ", ".join(failures))
    raise SystemExit(1)
print("All evidence round-trip checks passed.")
