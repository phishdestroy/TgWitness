import asyncio
import errno
import json
import logging
import sqlite3
import subprocess
import sys
import tempfile
import time
import zipfile
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from telethon import errors, types  # noqa: E402

from tgwitness import collector as collector_module, report  # noqa: E402
from tgwitness.collector import Collector  # noqa: E402
from tgwitness.evidence import export_file, retain_checkpoint  # noqa: E402
from tgwitness.monitoring import capture_settings  # noqa: E402
from tgwitness.security import Vault  # noqa: E402
from tgwitness.store import Store  # noqa: E402
from tgwitness.verify import fingerprint  # noqa: E402

CHAT = -1001234567890
PEER = types.PeerChannel(1234567890)
ACCOUNT = 4242
failures = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" :: " + str(detail) if detail != "" else ""), flush=True)
    if not ok:
        failures.append(name)


def kinds(store, after):
    return [event["kind"] for event in records(store, after)]


def head(store):
    with store.reading() as db:
        return db.execute("SELECT coalesce(max(seq),0) FROM events").fetchone()[0]


def records(store, after):
    return sorted(store.events(after=after, limit=100000), key=lambda event: event["seq"])


def message(number, size=4096):
    document = types.Document(id=number, access_hash=7, file_reference=b"ref", date=None, mime_type="application/pdf",
                              size=size, dc_id=2, attributes=[types.DocumentAttributeFilename("file%d.pdf" % number)])
    return types.Message(id=number, peer_id=PEER, date=None, message="attachment %d" % number,
                         media=types.MessageMediaDocument(document=document))


def job_state(store, event):
    with store.reading() as db:
        row = db.execute("SELECT state,attempts,next_attempt FROM media_jobs WHERE message_event=?", (event,)).fetchone()
    return dict(row) if row else None


def open_workspace(root):
    vault = Vault(root)
    store = Store(root)
    store.bind(vault)
    return vault, store


CHILD = r"""
import os, sys
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from tgwitness.security import Vault
from tgwitness.store import Store
root = Path(sys.argv[2]); vault = Vault(root); store = Store(root); store.bind(vault)
store.append("process.started", {"synthetic": True})
for number in range(int(sys.argv[3])):
    store.append("message.new", {"text": "crash test %d" % number}, -1001234567890, 10000 + number)
if sys.argv[4] == "mid-transaction":
    with store.transaction():
        for number in range(5):
            store.append("message.new", {"text": "never committed %d" % number}, -1001234567890, 20000 + number)
        os._exit(9)
os._exit(9)
"""


async def scenarios(root, vault, store):
    store.set_setting("account", {"id": ACCOUNT})
    store.set_target(CHAT, "Fault injection chat", "supergroup", True)
    collector = Collector(store, vault)
    media_root = root / "media"
    media_root.mkdir(exist_ok=True)
    capture = capture_settings(store)

    def queued(number):
        event = collector.commit_message(message(number), "message.new", CHAT)
        return event["seq"]

    async def attempt(fault, now=None):
        job = store.claim_media(ACCOUNT, now)
        if job is None:
            return None, None

        async def fetch(*_):
            raise fault
        collector.fetch_media = fetch
        try:
            await collector.process_media_job(job, capture, media_root)
        except asyncio.CancelledError:
            return job, "cancelled"
        return job, "returned"

    print("-- 1. attachment download fails", flush=True)
    event = queued(1)
    check("message with an attachment is recorded and its download queued", job_state(store, event)["state"] == "queued")
    before = head(store)
    attempts = 0
    while True:
        job, _ = await attempt(ConnectionError("synthetic network failure"), now=time.time() + 10**7)
        if job is None:
            break
        attempts += 1
    after = kinds(store, before)
    limit = collector.param("media_attempts")
    check("network failures are retried, then the attachment is marked failed in a signed record",
          after.count("media.retry") == limit - 1 and after.count("media.failed") == 1 and "media.saved" not in after,
          "attempts %d, records %s" % (attempts, after))
    check("a failed attachment is not queued again", job_state(store, event)["state"] == "failed")
    event = queued(2)
    before = head(store)
    await attempt(ValueError("unknown_size_or_above_limit"))
    check("a permanent failure is recorded once as media.failed with its reason",
          kinds(store, before) == ["media.failed"] and records(store, before)[0]["payload"].get("reason")
          == "unknown_size_or_above_limit", kinds(store, before))

    print("-- 2. Telegram FloodWait", flush=True)
    event = queued(3)
    before = head(store)
    flood = errors.FloodWaitError(request=None, capture=37)
    await attempt(flood)
    record = records(store, before)[0]
    state = job_state(store, event)
    check("FloodWait leaves one signed media.retry with the wait Telegram asked for",
          kinds(store, before) == ["media.retry"] and record["payload"].get("retry_after_seconds") == 37,
          record["payload"])
    check("the job waits for the FloodWait before the next attempt",
          state["state"] == "retry" and state["next_attempt"] >= time.time() + 30 and store.claim_media(ACCOUNT) is None,
          state)
    later = store.claim_media(ACCOUNT, time.time() + 40)
    check("after the wait the same job is attempted again, not duplicated",
          later is not None and later["message_event"] == event and later["attempts"] == 2)
    collector.fetch_media = None
    store.finish_media(later, "retry", {"reason": "test reset"}, delay=10**6)
    until = time.time() + 120
    collector.telegram_paused(until, "messages.GetHistory")
    reopened = Store(root)
    reopened.bind(vault)
    saved = reopened.get_setting("rpc_flood_until", {})
    check("an RPC FloodWait pause survives a restart", saved.get("messages.GetHistory") == until, saved)
    reopened.close()

    print("-- 3. cancel", flush=True)
    event = queued(4)
    before = head(store)
    _, how = await attempt(asyncio.CancelledError())
    record = records(store, before)[0]
    check("stopping the collector during a download keeps the job and signs why",
          how == "cancelled" and record["kind"] == "media.retry" and job_state(store, event)["state"] == "retry",
          record["payload"].get("reason"))
    queued(5)
    with store.reading() as db:
        waiting = db.execute("SELECT count(*) FROM media_jobs WHERE state IN ('queued','retry')").fetchone()[0]
    before = head(store)
    count = store.clear_media_queue(head(store))
    after = kinds(store, before)
    check("an operator cancelling waiting downloads gets one signed media.skipped per attachment",
          count == waiting == 3 and after == ["media.skipped"] * 3, (waiting, count, after))
    check("cancelled downloads are not attempted again", store.claim_media(ACCOUNT, time.time() + 10**8) is None)

    print("-- 4. lost update handler", flush=True)
    update = types.UpdateNewChannelMessage(message=types.Message(id=77, peer_id=PEER, date=None, message="lost"),
                                           pts=1, pts_count=1)
    handled = []

    async def broken(_):
        raise RuntimeError("synthetic handler failure")

    async def working(item):
        handled.append(item)
    collector.running, collector.client = True, object()
    key = ("synthetic", CHAT)
    collector.dispatch_queues[key] = deque([(1, False, collector.client, broken, update, (0, 0), lambda: None),
                                            (2, False, collector.client, working, update, (0, 0), lambda: None)])
    before = head(store)
    await collector.drain_updates(key)
    record = [event for event in records(store, before) if event["kind"] == "coverage.gap"]
    payload = record[0]["payload"] if record else {}
    check("a handler that fails leaves a signed coverage.gap naming the message",
          payload.get("reason") == "handler_failed" and payload.get("first_message_id") == 77
          and record[0]["chat_id"] == CHAT, payload)
    check("updates after the failed one are still handled", len(handled) == 1 and not collector.dispatch_queues)
    collector.running, collector.client = False, None

    print("-- 5. disk full", flush=True)
    before = head(store)
    signer, full = store.signer, {"on": True}

    class FullSigner:
        def __getattr__(self, name):
            return getattr(signer, name)

        def sign(self, data):
            if full["on"]:
                raise sqlite3.OperationalError("database or disk is full")
            return signer.sign(data)
    store.signer = FullSigner()
    try:
        store.append("message.new", {"text": "lost to a full disk"}, CHAT, 900)
        refused = False
    except sqlite3.OperationalError:
        refused = True
    check("a journal write on a full disk is refused without consuming a record number",
          refused and head(store) == before)
    restarted = []

    async def restart():
        restarted.append(True)
    collector.restart_observation = restart
    collector.running, collector.phase = True, "observing"
    usage = collector_module.shutil.disk_usage
    calls = {"n": 0}

    def disk_usage(path):
        calls["n"] += 1
        if calls["n"] >= 3:
            full["on"] = False
            return usage(path)
        return type("Usage", (), {"free": 1024, "total": 10**9, "used": 10**9})()
    collector_module.shutil.disk_usage = disk_usage
    seconds = collector_module.DISK_RESUME_SECONDS
    collector_module.DISK_RESUME_SECONDS = 0.01
    try:
        await collector.failure(OSError(errno.ENOSPC, "No space left on device"), "live update", fatal=True)
        stopped_phase = collector.phase
        if collector.disk_watch:
            await asyncio.wait_for(collector.disk_watch, 10)
    finally:
        collector_module.shutil.disk_usage = usage
        collector_module.DISK_RESUME_SECONDS = seconds
        store.signer = signer
        full["on"] = False
    gaps = [event for event in records(store, before) if event["kind"] == "coverage.gap"]
    payload = gaps[-1]["payload"] if gaps else {}
    check("collection stops with a storage error while nothing can be written", stopped_phase == "storage_error",
          stopped_phase)
    check("when space returns, a signed coverage.gap disk_full with its interval is written and collection restarts",
          payload.get("reason") == "disk_full" and payload.get("from") and payload.get("to") and restarted == [True],
          payload)
    result = store.verify(vault.public_key)
    check("the journal still verifies after the full disk", result.get("events") == head(store),
          {key: result.get(key) for key in ("events", "error", "problems")} | {"head": head(store)})
    return collector


def crash(root, count, mode):
    run = subprocess.run([sys.executable, "-I", "-c", CHILD, str(ROOT), str(root), str(count), mode],
                         capture_output=True, text=True, timeout=120)
    return run.returncode


def main():
    logging.disable(logging.CRITICAL)
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
        root = Path(folder) / "workspace"
        root.mkdir()
        vault, store = open_workspace(root)
        asyncio.run(scenarios(root, vault, store))
        settled = head(store)
        store.close()

        print("-- 6. process killed between writes", flush=True)
        code = crash(root, 200, "after-commit")
        wal = root / "journal.sqlite3-wal"
        check("the process died without closing the journal", code == 9 and wal.exists(),
              "exit %d, wal %s" % (code, wal.stat().st_size if wal.exists() else None))
        vault, store = open_workspace(root)
        check("every committed record is there after reopening", head(store) == settled + 201, (settled, head(store)))
        check("the reopened journal verifies", store.verify(vault.public_key).get("events") == head(store))
        check("the unclean stop is detectable", store.unclean_stop() is not None)
        committed = head(store)
        store.close()
        code = crash(root, 0, "mid-transaction")
        vault, store = open_workspace(root)
        texts = [event["payload"].get("text", "") for event in records(store, committed)]
        check("records of a transaction cut by the crash are absent, not half-written",
              code == 9 and not any(text.startswith("never committed") for text in texts), texts)
        check("the journal verifies after the cut transaction", store.verify(vault.public_key).get("events") == head(store))
        event = store.append("message.new", {"text": "after the crash"}, CHAT, 30000)
        check("the next record continues the chain", event["seq"] == head(store) and store.verify(vault.public_key)
              .get("events") == event["seq"])

        print("-- 7. export after the faults", flush=True)
        retain_checkpoint(store, vault)
        archive = export_file(store, vault, "zip", report.resolved(store, "en"), include_board=False, require_records=False)
        run = subprocess.run([sys.executable, "-I", str(ROOT / "tgwitness" / "verify.py"), str(archive), "--fingerprint",
                              fingerprint(vault.public_key), "--json"], capture_output=True, text=True)
        try:
            result = json.loads(run.stdout)
        except ValueError:
            result = {"output": (run.stdout + run.stderr)[-300:]}
        check("the archive verifies with the retained fingerprint", run.returncode == 0 and result.get("verified") is True,
              "exit %d" % run.returncode)
        with zipfile.ZipFile(archive) as bundle:
            rows = [json.loads(line) for line in bundle.read("events.jsonl").decode().splitlines()]
            coverage = json.loads(bundle.read("coverage.json"))
        reasons = {(row["payload"] if isinstance(row["payload"], dict) else json.loads(row["payload"])).get("reason")
                   for row in rows if row["kind"] == "coverage.gap"}
        check("the archive carries the signed gaps", {"handler_failed", "disk_full"} <= reasons, sorted(map(str, reasons)))
        media = [row["kind"] for row in rows if row["kind"].startswith("media.")]
        check("the archive carries the attachment failures and none is shown as saved",
              "media.failed" in media and "media.saved" not in media, sorted(set(media)))
        noted = {note.get("reason") for note in coverage.get("notes", [])} | {gap.get("reason") for gap in coverage["gaps"]}
        check("coverage.json lists the gaps", {"handler_failed", "disk_full"} <= noted, sorted(map(str, noted)))
        store.close()
    print("FAILED %d" % len(failures) if failures else "ALL PASSED")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
