import asyncio
import time

LANES = ("realtime", "text", "media", "maintenance")
LANE_PRIORITY = {"realtime": 0, "text": 1, "media": 2, "maintenance": 3}
MEANING = ("Four priority lanes share account capacity. Realtime (updates, presence) always proceeds. "
           "Text (history, export), media (downloads) and maintenance (rechecks, GC) each respect "
           "per-account FloodWait quotas and cannot steal a slot reserved for realtime.")

_DEFAULT_CAPS = {"realtime": 32, "text": 4, "media": 8, "maintenance": 2}


class LaneQuota:
    def __init__(self, lane, cap, *, clock=time.monotonic):
        self.lane, self.cap, self.clock = lane, cap, clock
        self.active = 0
        self.blocked_until = 0.0
        self.total = self.waits = 0

    def available(self):
        if self.lane == "realtime":
            return True
        return self.active < self.cap and self.clock() >= self.blocked_until

    def acquire(self):
        self.active += 1
        self.total += 1

    def release(self):
        self.active = max(0, self.active - 1)

    def set_backoff(self, seconds):
        self.blocked_until = self.clock() + seconds
        self.waits += 1

    def public(self):
        now = self.clock()
        return {
            "lane": self.lane,
            "active": self.active,
            "cap": self.cap,
            "blocked": max(0.0, round(self.blocked_until - now, 1)) if self.blocked_until > now else 0,
            "total": self.total,
            "waits": self.waits,
        }


class LaneManager:
    def __init__(self, *, caps=None, clock=time.monotonic):
        self.clock = clock
        caps = caps or {}
        self._accounts: dict[str, dict[str, LaneQuota]] = {}
        self._caps = {lane: caps.get(lane, _DEFAULT_CAPS[lane]) for lane in LANES}
        self._lock = None
        self._event = None
        self._loop = None

    def _quotas(self, account_id):
        key = str(account_id)
        if key not in self._accounts:
            self._accounts[key] = {lane: LaneQuota(lane, self._caps[lane], clock=self.clock)
                                   for lane in LANES}
        return self._accounts[key]

    def can_proceed(self, account_id, lane):
        return self._quotas(account_id)[lane].available()

    def acquire(self, account_id, lane):
        q = self._quotas(account_id)[lane]
        q.acquire()
        if self._event is not None:
            self._event.set()

    def release(self, account_id, lane):
        self._quotas(account_id)[lane].release()
        if self._event is not None:
            self._event.set()

    def set_backoff(self, account_id, lane, seconds):
        self._quotas(account_id)[lane].set_backoff(seconds)

    async def wait_for_slot(self, account_id, lane, timeout=None):
        loop = asyncio.get_running_loop()
        if loop is not self._loop:
            self._loop, self._event = loop, asyncio.Event()
        deadline = self.clock() + timeout if timeout else None
        while not self.can_proceed(account_id, lane):
            self._event.clear()
            remaining = max(0.01, deadline - self.clock()) if deadline else None
            try:
                await asyncio.wait_for(self._event.wait(), timeout=remaining)
            except asyncio.TimeoutError:
                break

    def remove_account(self, account_id):
        self._accounts.pop(str(account_id), None)

    def snapshot(self):
        return {
            account_id: {lane: q.public() for lane, q in quotas.items()}
            for account_id, quotas in self._accounts.items()
        }

    def public(self):
        accounts = []
        for account_id, quotas in self._accounts.items():
            accounts.append({"account_id": account_id,
                             "lanes": {lane: q.public() for lane, q in quotas.items()}})
        return {"accounts": accounts, "caps": dict(self._caps)}
