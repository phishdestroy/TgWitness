import asyncio
import time
from contextlib import asynccontextmanager

MEANING = ("Several parts of the collector may ask for the same Telegram file at once, for example live observation "
           "and a history pass. Only one of them downloads it; the others wait and then reuse the saved bytes after "
           "hashing them again.")


class _Flight:
    __slots__ = ("lock", "users", "origin", "since", "saved")

    def __init__(self):
        self.lock, self.users, self.origin, self.since = asyncio.Lock(), 0, None, None
        self.saved = None


class DownloadDedup:
    def __init__(self, clock=time.monotonic):
        self.clock = clock
        self.flights = {}
        self.turns = self.joined = self.peak = 0

    @asynccontextmanager
    async def turn(self, scope, key, origin=None):
        if key is None:
            yield False
            return
        ident = (str(scope), key)
        flight = self.flights.get(ident)
        if flight is None:
            flight = self.flights[ident] = _Flight()
        flight.users += 1
        waited = flight.lock.locked()
        if waited:
            self.joined += 1
        try:
            async with flight.lock:
                flight.origin, flight.since = origin, self.clock()
                self.turns += 1
                self.peak = max(self.peak, sum(1 for item in self.flights.values() if item.lock.locked()))
                try:
                    yield waited
                finally:
                    flight.origin = flight.since = None
        finally:
            flight.users -= 1
            if not flight.users and self.flights.get(ident) is flight:
                del self.flights[ident]

    def active(self, scope=None):
        return sum(1 for (owner, _), flight in self.flights.items()
                   if flight.lock.locked() and (scope is None or owner == str(scope)))

    def saved(self, scope, key):
        flight = self.flights.get((str(scope), key))
        return flight.saved if flight is not None else None

    def remember(self, scope, key, path, digest, size, source):
        flight = self.flights.get((str(scope), key))
        if flight is not None:
            flight.saved = {"path": path, "sha256": digest, "bytes": size, "source": source}

    def snapshot(self, scope=None, limit=20):
        now, rows = self.clock(), []
        for (owner, key), flight in self.flights.items():
            if scope is not None and owner != str(scope):
                continue
            if flight.lock.locked():
                rows.append({"key": key, "origin": flight.origin, "waiting": max(0, flight.users - 1),
                             "seconds": round(now - flight.since, 1) if flight.since is not None else None})
        rows.sort(key=lambda row: -(row["seconds"] or 0))
        return {"active": len(rows), "waiting": sum(row["waiting"] for row in rows), "turns": self.turns,
                "joined": self.joined, "peak": self.peak, "flights": rows[:limit], "meaning": MEANING}


DOWNLOADS = DownloadDedup()
