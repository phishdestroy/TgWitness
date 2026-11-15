import time

from .floodwait_learner import WARMUP

WARMUP_MINUTES = 15
INITIAL_MULTIPLIER = 2.0
MEANING = ("New accounts start with doubled request gaps. The multiplier decreases linearly to 1.0 "
           "over the first 15 minutes of operation, reducing the chance of early account bans.")


class AccountWarmup:
    def __init__(self, store, *, clock=time.monotonic, wall=time.time):
        self.store = store
        self.clock = clock
        self.wall = wall

    def _record(self):
        value = self.store.get_setting(WARMUP, {})
        return value if isinstance(value, dict) else {}

    def _account_id(self):
        return (self.store.get_setting("account", {}) or {}).get("id")

    def start(self):
        self.store.set_setting(WARMUP, {
            "account_id": self._account_id(),
            "started_at": self.wall(),
        })

    def multiplier(self):
        record = self._record()
        if not record or record.get("account_id") != self._account_id():
            return 1.0
        started_at = record.get("started_at")
        if not isinstance(started_at, (int, float)):
            return 1.0
        elapsed_minutes = (self.wall() - started_at) / 60
        if elapsed_minutes >= WARMUP_MINUTES:
            return 1.0
        progress = elapsed_minutes / WARMUP_MINUTES
        return INITIAL_MULTIPLIER - (INITIAL_MULTIPLIER - 1.0) * progress

    def active(self):
        return self.multiplier() > 1.0

    def public(self):
        m = self.multiplier()
        record = self._record()
        started_at = record.get("started_at") if isinstance(record, dict) else None
        elapsed = None
        if started_at is not None:
            elapsed = round((self.wall() - started_at) / 60, 1)
        return {
            "active": m > 1.0,
            "multiplier": round(m, 3),
            "elapsed_minutes": elapsed,
            "warmup_minutes": WARMUP_MINUTES,
        }
