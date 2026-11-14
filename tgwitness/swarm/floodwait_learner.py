import asyncio
import math
import time

SETTING = "rpc_bulk_pacing"
WARMUP = "account_warmup"
DEFAULT_GAP_MS = 1000
MIN_GAP_MS = 500
MAX_GAP_MS = 10000
GLOBAL_GAP_MS = 250
SUCCESS_STEP = 20
RELAX = 0.85
ALPHA = 0.3
METHODS_KEPT = 64


def clean_number(value, default, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        return default
    return max(low, min(high, value))


class FloodWaitLearner:
    def __init__(self, store, *, clock=time.monotonic, wall=time.time, sleep=asyncio.sleep, warmup_minutes=None):
        self.store, self.clock, self.wall, self.sleep = store, clock, wall, sleep
        self.warmup_minutes = warmup_minutes
        self.next_request, self.next_any = {}, 0.0

    def account(self):
        return (self.store.get_setting("account", {}) or {}).get("id")

    def saved(self):
        value = self.store.get_setting(SETTING, {})
        if not isinstance(value, dict) or value.get("account_id") != self.account():
            return {}
        return value

    @staticmethod
    def seed(value):
        if "seed_ms" in value:
            return round(clean_number(value.get("seed_ms"), DEFAULT_GAP_MS, MIN_GAP_MS, MAX_GAP_MS))
        if isinstance(value.get("methods"), dict):
            return DEFAULT_GAP_MS
        return round(clean_number(value.get("delay_seconds"), 1.0, MIN_GAP_MS / 1000, MAX_GAP_MS / 1000) * 1000)

    def method(self, value, name):
        methods = value.get("methods") if isinstance(value.get("methods"), dict) else {}
        found = methods.get(name) if isinstance(methods.get(name), dict) else {}
        base = self.seed(value)
        count = lambda key: max(0, found.get(key, 0)) if type(found.get(key, 0)) is int else 0
        return {"gap_ms": round(clean_number(found.get("gap_ms"), base, MIN_GAP_MS, MAX_GAP_MS)),
                "ema_wait_s": clean_number(found.get("ema_wait_s"), None, 0, 86400) if found.get("ema_wait_s") is not None else None,
                "floods": count("floods"), "successes": count("successes"), "streak": min(SUCCESS_STEP - 1, count("streak")),
                "last_flood_at": found.get("last_flood_at") if isinstance(found.get("last_flood_at"), (int, float)) else None}

    def state(self):
        value = self.saved()
        delay = clean_number(value.get("delay_seconds"), 1.0, MIN_GAP_MS / 1000, MAX_GAP_MS / 1000)
        count = lambda key: max(0, value.get(key, 0)) if type(value.get(key, 0)) is int else 0
        return {"account_id": self.account(), "delay_seconds": delay, "success_streak": min(19, count("success_streak")),
                "floodwait_count": count("floodwait_count"), "last_floodwait_at": value.get("last_floodwait_at"),
                "seed_ms": self.seed(value),
                "methods": {name: self.method(value, name) for name in (value.get("methods") or {}) if isinstance(name, str)}}

    def save(self, name, method):
        value = self.state()
        methods = dict(value["methods"])
        methods[name] = method
        if len(methods) > METHODS_KEPT:
            for stale in sorted(methods, key=lambda key: methods[key].get("last_flood_at") or 0)[:len(methods) - METHODS_KEPT]:
                methods.pop(stale, None)
        value["methods"] = methods
        value["delay_seconds"] = round(max(item["gap_ms"] for item in methods.values()) / 1000, 3)
        value["success_streak"] = method["streak"]
        self.store.set_setting(SETTING, value)

    def warmup_factor(self):
        minutes = self.warmup_minutes() if callable(self.warmup_minutes) else self.warmup_minutes
        warmup = self.store.get_setting(WARMUP, {}) or {}
        if not minutes or warmup.get("account_id") != self.account() or not isinstance(warmup.get("started_at"), (int, float)):
            return 1.0
        elapsed = (self.wall() - warmup["started_at"]) / 60
        if elapsed < 0 or elapsed >= minutes:
            return 1.0
        return 2.0 - elapsed / minutes

    def recommended_gap_ms(self, name=None):
        name = name or "bulk"
        return round(self.method(self.saved(), name)["gap_ms"] * self.warmup_factor())

    async def before(self, name=None):
        name = name or "bulk"
        now = self.clock()
        wait = max(0.0, self.next_request.get(name, 0.0) - now, self.next_any - now)
        if wait:
            await self.sleep(wait)
        now = self.clock()
        self.next_request[name] = now + self.recommended_gap_ms(name) / 1000
        self.next_any = now + GLOBAL_GAP_MS / 1000

    def success(self, name=None):
        name = name or "bulk"
        method = self.method(self.saved(), name)
        method["successes"] += 1
        method["streak"] += 1
        if method["streak"] >= SUCCESS_STEP:
            method["gap_ms"] = max(MIN_GAP_MS, round(method["gap_ms"] * RELAX))
            method["streak"] = 0
        self.save(name, method)

    def flooded(self, seconds, name=None):
        name = name or "bulk"
        seconds = clean_number(seconds, 0, 0, 86400)
        method = self.method(self.saved(), name)
        step = 500 if seconds < 10 else 2000 if seconds < 60 else 5000
        method.update(streak=0, floods=method["floods"] + 1, last_flood_at=self.wall(),
                      gap_ms=min(MAX_GAP_MS, max(round(method["gap_ms"] * 1.5), method["gap_ms"] + step)),
                      ema_wait_s=round(seconds if method["ema_wait_s"] is None
                                       else ALPHA * seconds + (1 - ALPHA) * method["ema_wait_s"], 2))
        self.save(name, method)
        value = self.store.get_setting(SETTING, {})
        value.update(floodwait_count=value.get("floodwait_count", 0) + 1, last_floodwait_at=self.wall())
        self.store.set_setting(SETTING, value)
        self.next_request[name] = self.clock() + self.recommended_gap_ms(name) / 1000

    def snapshot(self):
        state = self.state()
        factor = self.warmup_factor()
        return {"warmup_factor": round(factor, 2), "methods": {
            name: {**method, "recommended_gap_ms": round(method["gap_ms"] * factor)}
            for name, method in sorted(state["methods"].items())}}
