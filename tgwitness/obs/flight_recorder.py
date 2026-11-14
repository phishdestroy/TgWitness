import json
import logging
import os
import secrets
import signal
import threading
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

from ..operator_privacy import private_log
from ..store import utcnow

SIZE = 10000
KEEP_DUMPS = 5
FORMAT = "tgwitness-flight-record-v1"


class FlightRecorder(logging.Handler):
    def __init__(self, size=SIZE):
        super().__init__(logging.INFO)
        self.items, self.counter, self.guard = deque(maxlen=size), 0, threading.Lock()
        self.stores, self.attached, self.started_at = set(), False, utcnow()

    def note(self, kind, **fields):
        with self.guard:
            self.counter += 1
            self.items.append({"n": self.counter, "at": utcnow(), "kind": kind, **fields})

    def emit(self, record):
        with self.guard:
            if record is getattr(self, "last", None):
                return
            self.last = record
        try:
            text = record.getMessage()
            if record.exc_info and record.exc_info[1] is not None:
                text += " · " + type(record.exc_info[1]).__name__
        except Exception:
            text = str(record.msg)
        self.note("log", level=record.levelname, source=record.name, text=private_log(text[:4000])[:1000])

    def watch(self, store, workspace):
        if id(store) in self.stores:
            return
        self.stores.add(id(store))

        def listener(event):
            self.note("record", workspace=workspace, seq=event.get("seq"), event=event.get("kind"),
                      chat_id=event.get("chat_id"))
        store.listeners.append(listener)

    def attach(self):
        if self.attached:
            return
        self.attached = True
        for name in ("", "uvicorn", "uvicorn.error"):
            logging.getLogger(name).addHandler(self)
        try:
            import asyncio
            asyncio.get_running_loop().add_signal_handler(signal.SIGUSR1, self.signalled)
        except (AttributeError, NotImplementedError, RuntimeError, ValueError):
            pass

    def snapshot(self):
        with self.guard:
            return list(self.items)

    def lines(self):
        head = {"format": FORMAT, "pid": os.getpid(), "started_at": self.started_at, "dumped_at": utcnow(),
                "kept": SIZE, "meaning": "The most recent log lines and journal record kinds of this TgWitness process. "
                                        "Record contents are not included; log lines hide secrets and addresses."}
        yield json.dumps(head, ensure_ascii=False) + "\n"
        for item in self.snapshot():
            yield json.dumps(item, ensure_ascii=False) + "\n"

    def dump(self, root):
        folder = Path(root) / "flight"
        folder.mkdir(mode=0o700, parents=True, exist_ok=True)
        path = folder / ("flight-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-"
                         + secrets.token_hex(3) + ".jsonl")
        with open(path, "x", encoding="utf-8", newline="\n") as out:
            out.writelines(self.lines())
        for old in sorted(folder.glob("flight-*.jsonl"))[:-KEEP_DUMPS]:
            old.unlink(missing_ok=True)
        return path

    def signalled(self):
        root = getattr(self, "root", None)
        if root is not None:
            threading.Thread(target=self.dump, args=(root,), name="flight-dump", daemon=True).start()


RECORDER = FlightRecorder()
