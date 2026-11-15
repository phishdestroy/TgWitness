import asyncio
import time

from .burst import REGISTRATIONS

HEALTH_INTERVAL = 60
SLOW_MS = 3000
RESTART_FAIL_RATE = 0.5
RESTART_WINDOW = 300
MEANING = ("All WARP tunnels start in parallel, rate-limited to avoid Cloudflare registration floods. "
           "Each tunnel is health-checked every 60 seconds and restarted automatically when it degrades.")


class WarpTunnel:
    def __init__(self, config, *, start_fn, stop_fn, check_fn, clock=time.monotonic):
        self.config = config
        self._start_fn = start_fn
        self._stop_fn = stop_fn
        self._check_fn = check_fn
        self.clock = clock
        self.name = config.get("name", config.get("account_id", "?"))
        self.started = False
        self.last_check = None
        self.ema_ms = None
        self.checks = self.failures = 0
        self.started_at = None

    async def start(self):
        async with REGISTRATIONS.turn(f"warp/{self.name}"):
            await self._start_fn(self.config)
        self.started, self.started_at = True, self.clock()

    async def stop(self):
        await self._stop_fn(self.config)
        self.started = False

    async def health_check(self):
        try:
            result = await self._check_fn(self.config)
            ms = result.get("latency_ms", 0)
            alpha = 0.4
            self.ema_ms = ms if self.ema_ms is None else self.ema_ms * (1 - alpha) + ms * alpha
            self.checks += 1
            self.last_check = self.clock()
            return {"ok": True, "latency_ms": ms, "ema_ms": round(self.ema_ms)}
        except Exception as exc:
            self.failures += 1
            self.checks += 1
            self.last_check = self.clock()
            return {"ok": False, "error": str(exc)}

    def fail_rate(self):
        return self.failures / max(1, self.checks)

    def degraded(self):
        return (self.ema_ms is not None and self.ema_ms > SLOW_MS) or self.fail_rate() > RESTART_FAIL_RATE

    def public(self):
        return {
            "name": self.name,
            "started": self.started,
            "ema_ms": round(self.ema_ms) if self.ema_ms is not None else None,
            "checks": self.checks,
            "failures": self.failures,
            "fail_rate": round(self.fail_rate(), 3),
            "degraded": self.degraded(),
            "last_check": self.last_check,
        }


class WarpPool:
    def __init__(self, *, start_fn, stop_fn, check_fn, clock=time.monotonic):
        self._start_fn = start_fn
        self._stop_fn = stop_fn
        self._check_fn = check_fn
        self.clock = clock
        self._tunnels: dict[str, WarpTunnel] = {}
        self._running = False

    def _tunnel(self, config):
        name = str(config.get("name", config.get("account_id", id(config))))
        if name not in self._tunnels:
            self._tunnels[name] = WarpTunnel(
                config, start_fn=self._start_fn, stop_fn=self._stop_fn,
                check_fn=self._check_fn, clock=self.clock)
        return self._tunnels[name]

    async def start_all(self, configs):
        tunnels = [self._tunnel(c) for c in configs]
        await asyncio.gather(*(t.start() for t in tunnels), return_exceptions=True)

    async def _health_one(self, tunnel):
        result = await tunnel.health_check()
        if tunnel.degraded() and tunnel.started:
            await tunnel.stop()
            await tunnel.start()
        return result

    async def health_loop(self):
        self._running = True
        while self._running:
            await asyncio.sleep(HEALTH_INTERVAL)
            await asyncio.gather(*(self._health_one(t) for t in list(self._tunnels.values())),
                                 return_exceptions=True)

    def stop_loop(self):
        self._running = False

    async def stop_all(self):
        self.stop_loop()
        await asyncio.gather(*(t.stop() for t in self._tunnels.values()), return_exceptions=True)

    def public(self):
        return [t.public() for t in self._tunnels.values()]
