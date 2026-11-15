import asyncio
import logging
import time
from collections import defaultdict

MEANING = ("Background worker that refreshes Telegram file_reference tokens for media that could not be "
           "downloaded due to expiry. Batches getMessages calls per peer (up to 100 IDs), remembers TTLs, "
           "and does not request the same ID twice within the cooldown window.")
BATCH_SIZE = 100
COOLDOWN_SECONDS = 1800
RETRY_BACKOFF = 60
LOOP_INTERVAL = 30
log = logging.getLogger(__name__)


class _PendingRef:
    __slots__ = ("chat_id", "message_id", "enqueued_at", "last_tried", "tries", "refreshed_at", "error")

    def __init__(self, chat_id, message_id, now):
        self.chat_id = chat_id
        self.message_id = message_id
        self.enqueued_at = now
        self.last_tried = None
        self.tries = 0
        self.refreshed_at = None
        self.error = None


class RefRefresher:
    def __init__(self, *, client_fn=None, clock=time.monotonic):
        self._client_fn = client_fn
        self.clock = clock
        self._pending: dict[tuple, _PendingRef] = {}
        self._refreshed: dict[tuple, float] = {}
        self._running = False
        self._wakeup = None
        self._loop = None
        self.total = self.errors = 0

    def _event(self):
        loop = asyncio.get_running_loop()
        if self._wakeup is None or self._loop is not loop:
            self._loop, self._wakeup = loop, asyncio.Event()
        return self._wakeup

    def enqueue(self, chat_id, message_id):
        key = (int(chat_id), int(message_id))
        now = self.clock()
        if key in self._refreshed and now - self._refreshed[key] < COOLDOWN_SECONDS:
            return
        if key not in self._pending:
            self._pending[key] = _PendingRef(chat_id, message_id, now)
        try:
            loop = asyncio.get_running_loop()
            if self._wakeup is not None and self._loop is loop:
                self._wakeup.set()
        except RuntimeError:
            pass

    def _ready_batch(self, now):
        by_chat: dict[int, list] = defaultdict(list)
        for key, ref in self._pending.items():
            if ref.last_tried is not None and now - ref.last_tried < RETRY_BACKOFF * (2 ** min(ref.tries, 4)):
                continue
            by_chat[ref.chat_id].append(ref)
        for chat_id, refs in by_chat.items():
            yield chat_id, refs[:BATCH_SIZE]

    async def _refresh_batch(self, client, chat_id, refs):
        from telethon import functions, utils
        ids = [r.message_id for r in refs]
        now = self.clock()
        try:
            peer = await client.get_input_entity(chat_id)
            if hasattr(peer, "channel_id"):
                result = await client(functions.channels.GetMessagesRequest(peer, [
                    utils.get_input_messages(mid) if hasattr(utils, "get_input_messages")
                    else mid for mid in ids
                ]))
            else:
                result = await client(functions.messages.GetMessagesRequest([mid for mid in ids]))
            messages = {m.id: m for m in getattr(result, "messages", []) if hasattr(m, "id")}
            for ref in refs:
                key = (ref.chat_id, ref.message_id)
                msg = messages.get(ref.message_id)
                if msg is not None and getattr(msg, "media", None):
                    self._refreshed[key] = now
                    self._pending.pop(key, None)
                    self.total += 1
                    ref.refreshed_at = now
                else:
                    ref.tries += 1
                    ref.last_tried = now
                    ref.error = "not_found"
        except Exception as exc:
            log.debug("RefRefresher batch chat=%s error=%s", chat_id, exc)
            for ref in refs:
                ref.tries += 1
                ref.last_tried = now
                ref.error = str(exc)[:80]
            self.errors += 1

    async def _run_once(self):
        client = self._client_fn() if callable(self._client_fn) else None
        if client is None:
            return
        now = self.clock()
        for chat_id, refs in list(self._ready_batch(now)):
            await self._refresh_batch(client, chat_id, refs)
            await asyncio.sleep(0)

    async def loop(self):
        self._running = True
        event = self._event()
        while self._running:
            event.clear()
            await self._run_once()
            try:
                await asyncio.wait_for(event.wait(), timeout=LOOP_INTERVAL)
            except asyncio.TimeoutError:
                pass

    def stop(self):
        self._running = False
        if self._wakeup is not None:
            self._wakeup.set()

    def public(self):
        return {
            "pending": len(self._pending),
            "refreshed": len(self._refreshed),
            "total": self.total,
            "errors": self.errors,
        }
