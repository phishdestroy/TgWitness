START = 2


class AdaptiveSlots:
    def __init__(self, cap, floods=lambda: 0, start=START):
        self.cap = max(1, int(cap))
        self.limit = min(self.cap, max(1, start))
        self.active = self.rounds = 0
        self.floods, self.seen = floods, floods()
        self.peak = self.limit

    def locked(self):
        return self.active >= self.limit

    async def acquire(self):
        self.active += 1

    def release(self):
        self.active = max(0, self.active - 1)
        latest = self.floods()
        if latest > self.seen:
            self.seen, self.rounds = latest, 0
            self.limit = max(1, self.limit // 2)
            return
        self.rounds += 1
        if self.rounds >= self.limit and self.limit < self.cap:
            self.limit, self.rounds = self.limit + 1, 0
            self.peak = max(self.peak, self.limit)

    def public(self):
        return {"limit": self.limit, "cap": self.cap, "active": self.active, "peak": self.peak}
