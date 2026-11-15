import asyncio
import logging
import time

MEANING = ("Self-destructing media has its own download pool with priority over all other media. "
           "If a file will expire in less than 30 seconds, all other media downloads on that account are "
           "paused until the ephemeral file is secured.")
TTL_URGENT_SECONDS = 30
MEANING_POOL = "ephemeral_media"
log = logging.getLogger(__name__)


class EphemeralPriorityLane:
    def __init__(self, *, pause_fn=None, resume_fn=None, clock=time.monotonic):
        self._pause_fn = pause_fn
        self._resume_fn = resume_fn
        self.clock = clock
        self._active: dict[str, dict] = {}
        self._paused = False
        self._wakeup = None
        self._loop = None
        self.secured = self.expired = 0

    def _event(self):
        loop = asyncio.get_running_loop()
        if self._wakeup is None or self._loop is not loop:
            self._loop, self._wakeup = loop, asyncio.Event()
        return self._wakeup

    def register(self, key: str, expires_at: float | None, download_coro):
        self._active[key] = {
            "key": key,
            "expires_at": expires_at,
            "coro": download_coro,
            "started_at": self.clock(),
        }
        self._event().set()

    def _is_urgent(self, entry):
        expires_at = entry.get("expires_at")
        if expires_at is None:
            return False
        return expires_at - self.clock() < TTL_URGENT_SECONDS

    async def _download_one(self, entry):
        key = entry["key"]
        try:
            result = await entry["coro"]
            self.secured += 1
            return result
        except Exception as exc:
            log.debug("Ephemeral download %s failed: %s", key, exc)
            self.expired += 1
            return None
        finally:
            self._active.pop(key, None)

    async def run(self):
        event = self._event()
        while True:
            event.clear()
            urgent = [e for e in self._active.values() if self._is_urgent(e)]
            if urgent:
                if not self._paused and self._pause_fn:
                    await self._pause_fn()
                    self._paused = True
                await asyncio.gather(*(self._download_one(e) for e in urgent), return_exceptions=True)
            else:
                if self._paused and self._resume_fn:
                    await self._resume_fn()
                    self._paused = False
                normal = list(self._active.values())
                if normal:
                    await asyncio.gather(*(self._download_one(e) for e in normal), return_exceptions=True)
            try:
                await asyncio.wait_for(event.wait(), timeout=1.0)
            except asyncio.TimeoutError:
                pass

    def public(self):
        now = self.clock()
        entries = []
        for e in self._active.values():
            expires_at = e.get("expires_at")
            entries.append({
                "key": e["key"],
                "ttl_seconds": round(expires_at - now, 1) if expires_at else None,
                "urgent": self._is_urgent(e),
            })
        return {
            "active": len(self._active),
            "paused_other": self._paused,
            "secured": self.secured,
            "expired": self.expired,
            "entries": entries,
        }
