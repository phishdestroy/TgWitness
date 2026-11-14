import asyncio
import math
import time
from collections import deque
from contextlib import asynccontextmanager
from contextvars import ContextVar

HANDSHAKES_AT_ONCE = 5
HANDSHAKES_PER_SECOND = 5.0
REGISTRATIONS_AT_ONCE = 2
REGISTRATIONS_PER_SECOND = 5.0
MEANING = ("At most this many Telegram connections are being set up at the same moment across all accounts on "
           "this server. The rest wait their turn, so a cold start of many accounts does not time out.")

_held = ContextVar("tgwitness_gate_turn", default=None)


class _Turn:
    __slots__ = ("gate", "open")

    def __init__(self, gate):
        self.gate, self.open = gate, True


class Gate:
    def __init__(self, name, *, at_once, per_second, clock=time.monotonic):
        self.name, self.at_once, self.per_second, self.clock = name, at_once, per_second, clock
        self.tokens, self.stamp = float(at_once), None
        self.loop = self.order = self.slots = None
        self.active = self.waiting = self.peak = 0
        self.started = self.failed = self.timeouts = 0
        self.waits, self.durations = deque(maxlen=256), deque(maxlen=256)
        self.purposes = {}

    def _bind(self):
        loop = asyncio.get_running_loop()
        if loop is not self.loop:
            self.loop, self.order, self.slots = loop, asyncio.Lock(), asyncio.Semaphore(self.at_once)
            self.active = self.waiting = 0
            self.tokens, self.stamp = float(self.at_once), None

    def _refill(self):
        now = self.clock()
        if self.stamp is not None:
            self.tokens = min(float(self.at_once), self.tokens + (now - self.stamp) * self.per_second)
        self.stamp = now

    async def acquire(self):
        self._bind()
        began = self.clock()
        self.waiting += 1
        try:
            async with self.order:
                await self.slots.acquire()
                try:
                    self._refill()
                    while self.tokens < 1:
                        await asyncio.sleep((1 - self.tokens) / self.per_second)
                        self._refill()
                    self.tokens -= 1
                except BaseException:
                    self.slots.release()
                    raise
        finally:
            self.waiting -= 1
        self.active += 1
        self.started += 1
        self.peak = max(self.peak, self.active)
        self.waits.append(self.clock() - began)

    def release(self):
        self.active -= 1
        self.slots.release()

    def holding(self):
        held = _held.get()
        return held is not None and held.open and held.gate is self

    @asynccontextmanager
    async def turn(self, purpose="connect"):
        if self.holding():
            yield
            return
        await self.acquire()
        self.purposes[purpose] = self.purposes.get(purpose, 0) + 1
        token, began = _Turn(self), self.clock()
        reset = _held.set(token)
        try:
            yield
        except TimeoutError:
            self.timeouts += 1
            raise
        except Exception:
            self.failed += 1
            raise
        finally:
            token.open = False
            _held.reset(reset)
            self.durations.append(self.clock() - began)
            self.release()

    def snapshot(self):
        def p95(values):
            ordered = sorted(values)
            return round(ordered[min(len(ordered) - 1, math.ceil(len(ordered) * .95) - 1)] * 1000) if ordered else None
        return {"name": self.name, "at_once": self.at_once, "per_second": self.per_second, "active": self.active,
                "waiting": self.waiting, "peak": self.peak, "started": self.started, "failed": self.failed,
                "timeouts": self.timeouts, "wait_p95_ms": p95(self.waits), "duration_p95_ms": p95(self.durations),
                "purposes": dict(self.purposes)}


HANDSHAKES = Gate("telegram_handshakes", at_once=HANDSHAKES_AT_ONCE, per_second=HANDSHAKES_PER_SECOND)
REGISTRATIONS = Gate("warp_registrations", at_once=REGISTRATIONS_AT_ONCE, per_second=REGISTRATIONS_PER_SECOND)


def guard(sender, gate=HANDSHAKES):
    if sender is None or getattr(sender, "tgwitness_gate", None) is gate:
        return sender
    original = sender._connect

    async def gated_connect():
        async with gate.turn("reconnect"):
            return await original()
    sender._connect = gated_connect
    sender.tgwitness_gate = gate
    return sender


def snapshot():
    return {"handshakes": HANDSHAKES.snapshot(), "registrations": REGISTRATIONS.snapshot(), "meaning": MEANING}
