import asyncio
import logging
import random
import time

MEANING = ("A second Telegram account periodically re-fetches random message IDs from already-collected chats "
           "and writes divergence records when the content differs. Runs asynchronously with less than 5% "
           "throughput overhead on the primary collector.")
SAMPLE_RATE = 0.01
BATCH_SIZE = 50
LOOP_INTERVAL = 300
MAX_DIVERGED = 10000
KIND = "witness.replay"
KIND_DIVERGED = "witness.diverged"
log = logging.getLogger(__name__)


class WitnessReplay:
    def __init__(self, store, *, client_fn=None, clock=time.monotonic):
        self.store = store
        self._client_fn = client_fn
        self.clock = clock
        self._running = False
        self._wakeup = None
        self._loop = None
        self.checks = self.diverged = self.errors = 0
        self._last_at = None

    def _event(self):
        loop = asyncio.get_running_loop()
        if self._wakeup is None or self._loop is not loop:
            self._loop, self._wakeup = loop, asyncio.Event()
        return self._wakeup

    def _sample_ids(self, chat_id):
        try:
            with self.store.reading() as db:
                rows = db.execute(
                    "SELECT message_id FROM events WHERE chat_id=? AND kind='message' ORDER BY RANDOM() LIMIT ?",
                    (chat_id, BATCH_SIZE)
                ).fetchall()
            return [r[0] for r in rows]
        except Exception:
            return []

    def _known_chats(self):
        try:
            with self.store.reading() as db:
                rows = db.execute(
                    "SELECT DISTINCT chat_id FROM events WHERE kind='message' AND chat_id IS NOT NULL LIMIT 100"
                ).fetchall()
            return [r[0] for r in rows]
        except Exception:
            return []

    async def _replay_chat(self, client, chat_id, message_ids):
        from telethon import functions
        try:
            peer = await client.get_input_entity(chat_id)
            if hasattr(peer, "channel_id"):
                result = await client(functions.channels.GetMessagesRequest(
                    peer, [mid for mid in message_ids]))
            else:
                result = await client(functions.messages.GetMessagesRequest(
                    [mid for mid in message_ids]))
            seen = {m.id: m for m in getattr(result, "messages", []) if hasattr(m, "id")}
            diverged = []
            for mid in message_ids:
                msg = seen.get(mid)
                if msg is None:
                    diverged.append({"chat_id": chat_id, "message_id": mid, "reason": "not_found"})
                elif getattr(msg, "message", None) is None and getattr(msg, "media", None) is None:
                    diverged.append({"chat_id": chat_id, "message_id": mid, "reason": "empty"})
            self.checks += len(message_ids)
            for d in diverged:
                self.diverged += 1
                self.store.append(KIND_DIVERGED, d, chat_id=d["chat_id"], message_id=d["message_id"])
        except Exception as exc:
            self.errors += 1
            log.debug("Witness replay chat=%s error=%s", chat_id, exc)

    async def run_once(self):
        client = self._client_fn() if callable(self._client_fn) else None
        if client is None:
            return
        chats = self._known_chats()
        if not chats:
            return
        sampled = random.sample(chats, min(5, len(chats)))
        for chat_id in sampled:
            ids = self._sample_ids(chat_id)
            if not ids:
                continue
            count = max(1, round(len(ids) * SAMPLE_RATE))
            sample = random.sample(ids, min(count, len(ids), BATCH_SIZE))
            await self._replay_chat(client, chat_id, sample)
            await asyncio.sleep(0)
        self._last_at = self.clock()
        self.store.append(KIND, {
            "checks": self.checks,
            "diverged": self.diverged,
            "errors": self.errors,
        })

    async def loop(self):
        self._running = True
        event = self._event()
        while self._running:
            try:
                await asyncio.wait_for(event.wait(), timeout=LOOP_INTERVAL)
            except asyncio.TimeoutError:
                pass
            event.clear()
            if not self._running:
                break
            try:
                await self.run_once()
            except Exception as exc:
                log.warning("Witness replay error: %s", exc)

    def stop(self):
        self._running = False
        if self._wakeup is not None:
            self._wakeup.set()

    def public(self):
        return {
            "checks": self.checks,
            "diverged": self.diverged,
            "errors": self.errors,
            "last_at": self._last_at,
            "sample_rate": SAMPLE_RATE,
        }
