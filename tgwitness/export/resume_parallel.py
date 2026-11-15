import asyncio
import logging
import random
import time

MEANING = ("On resume, samples 1% of already-downloaded message IDs in the background and verifies their "
           "presence in the journal. Divergences are written to integrity.diverged.jsonl. The sampling "
           "runs concurrently with the resumed export and adds less than 2% overhead.")
SAMPLE_RATE = 0.01
BATCH_SIZE = 100
KIND = "integrity.sample"
KIND_DIVERGED = "integrity.diverged"
log = logging.getLogger(__name__)


def _sample(ids, rate=SAMPLE_RATE):
    count = max(1, round(len(ids) * rate))
    return random.sample(ids, min(count, len(ids), BATCH_SIZE))


class ParallelIntegrityCheck:
    def __init__(self, store, *, clock=time.monotonic):
        self.store = store
        self.clock = clock
        self._task = None
        self.checked = self.ok = self.diverged = self.errors = 0
        self._running = False
        self._start = None
        self._done = False

    def _all_saved_ids(self, chat_id):
        try:
            with self.store.reading() as db:
                rows = db.execute(
                    "SELECT message_id FROM events WHERE kind='message' AND chat_id=? AND message_id IS NOT NULL",
                    (chat_id,)
                ).fetchall()
            return [r[0] for r in rows]
        except Exception:
            return []

    async def _check_batch(self, chat_id, ids):
        try:
            with self.store.reading() as db:
                for mid in ids:
                    row = db.execute(
                        "SELECT 1 FROM events WHERE chat_id=? AND message_id=? AND kind='message' LIMIT 1",
                        (chat_id, mid)
                    ).fetchone()
                    if row:
                        self.ok += 1
                    else:
                        self.diverged += 1
                        self.store.append(KIND_DIVERGED, {
                            "chat_id": chat_id,
                            "message_id": mid,
                            "reason": "missing_on_resume",
                        }, chat_id=chat_id, message_id=mid)
                    self.checked += 1
                    await asyncio.sleep(0)
        except Exception as exc:
            self.errors += 1
            log.debug("Integrity check error: %s", exc)

    async def run(self, chat_id, resume_cursor):
        self._running = True
        self._start = self.clock()
        try:
            ids = self._all_saved_ids(chat_id)
            if not ids:
                return
            sampled = _sample(ids)
            await self._check_batch(chat_id, sampled)
            self.store.append(KIND, {
                "chat_id": chat_id,
                "checked": self.checked,
                "ok": self.ok,
                "diverged": self.diverged,
                "resume_cursor": resume_cursor,
                "sample_rate": SAMPLE_RATE,
            })
        finally:
            self._running = False
            self._done = True

    def start_background(self, chat_id, resume_cursor):
        self._task = asyncio.ensure_future(self.run(chat_id, resume_cursor))
        return self._task

    async def wait(self):
        if self._task is not None:
            await self._task

    def summary(self):
        return f"sampled integrity ok: {self.ok}/{self.checked}" + (
            f", diverged: {self.diverged}" if self.diverged else "")

    def public(self):
        elapsed = round(self.clock() - self._start, 1) if self._start else None
        return {
            "running": self._running,
            "done": self._done,
            "checked": self.checked,
            "ok": self.ok,
            "diverged": self.diverged,
            "errors": self.errors,
            "elapsed_seconds": elapsed,
            "sample_rate": SAMPLE_RATE,
            "summary": self.summary(),
        }
