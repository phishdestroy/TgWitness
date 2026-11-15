import time
from collections import deque

ALPHA = 0.3
WINDOW_SECONDS = 300
EJECT_FAIL_RATE = 0.2
MEANING = ("MTProxy pool tracks EMA latency and fail rate per proxy. "
           "A proxy is ejected when its fail rate over the last 5 minutes exceeds 20%. "
           "Active sessions are not interrupted; only new requests go to a different proxy.")


class _ProxyState:
    __slots__ = ("key", "proxy", "ema_ms", "ejected", "events")

    def __init__(self, key, proxy):
        self.key = key
        self.proxy = proxy
        self.ema_ms = None
        self.ejected = False
        self.events: deque[tuple[float, bool]] = deque()

    def record(self, ok, latency_ms=None, *, clock=time.monotonic):
        now = clock()
        self.events.append((now, ok))
        cutoff = now - WINDOW_SECONDS
        while self.events and self.events[0][0] < cutoff:
            self.events.popleft()
        if ok and latency_ms is not None:
            self.ema_ms = latency_ms if self.ema_ms is None else self.ema_ms * (1 - ALPHA) + latency_ms * ALPHA

    def fail_rate(self):
        if not self.events:
            return 0.0
        failures = sum(1 for _, ok in self.events if not ok)
        return failures / len(self.events)

    def public(self):
        return {
            "key": self.key,
            "host": self.proxy.get("host"),
            "port": self.proxy.get("port"),
            "ema_ms": round(self.ema_ms) if self.ema_ms is not None else None,
            "fail_rate": round(self.fail_rate(), 3),
            "ejected": self.ejected,
            "samples": len(self.events),
        }


def _proxy_key(proxy):
    return "{}:{}".format(proxy.get("host", ""), proxy.get("port", ""))


class ProxyHealth:
    def __init__(self, proxies: list, *, clock=time.monotonic):
        self.clock = clock
        self._states: dict[str, _ProxyState] = {}
        for p in proxies:
            key = _proxy_key(p)
            self._states[key] = _ProxyState(key, p)

    def record_success(self, proxy_key, latency_ms: float):
        if proxy_key in self._states:
            self._states[proxy_key].record(True, latency_ms, clock=self.clock)
            self._maybe_uneject(proxy_key)

    def record_failure(self, proxy_key):
        if proxy_key in self._states:
            state = self._states[proxy_key]
            state.record(False, clock=self.clock)
            if state.fail_rate() > EJECT_FAIL_RATE:
                self.eject(proxy_key)

    def _maybe_uneject(self, proxy_key):
        state = self._states.get(proxy_key)
        if state and state.ejected and state.fail_rate() <= EJECT_FAIL_RATE / 2:
            state.ejected = False

    def eject(self, proxy_key):
        if proxy_key in self._states:
            self._states[proxy_key].ejected = True

    def add(self, proxy):
        key = _proxy_key(proxy)
        if key not in self._states:
            self._states[key] = _ProxyState(key, proxy)

    def remove(self, proxy_key):
        self._states.pop(proxy_key, None)

    def best(self):
        candidates = [s for s in self._states.values() if not s.ejected]
        if not candidates:
            candidates = [s for s in self._states.values()]
        if not candidates:
            return None
        candidates.sort(key=lambda s: (s.ema_ms or 9999, s.fail_rate()))
        return candidates[0].proxy

    def all_keys(self):
        return list(self._states)

    def public(self):
        return [s.public() for s in self._states.values()]
