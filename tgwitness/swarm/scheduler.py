import asyncio
import itertools
import secrets
import time
from dataclasses import dataclass, field

KINDS = ("chat_export", "history_pass", "media_dl", "views_poll", "recheck")
ACTIVE = ("queued", "running")
FINAL = ("done", "failed", "cancelled")
IDLE_CHECK = 1.0
MEANING = ("Tasks wait in one queue. An account that is free takes the most urgent task it can do; a task that needs "
           "access to a chat goes only to accounts that have it.")


class Requeue(Exception):
    def __init__(self, delay=0, reason=None):
        super().__init__(reason or "requeue")
        self.delay, self.reason = delay, reason


class Unsuitable(Exception):
    pass


@dataclass(eq=False)
class Task:
    kind: str
    payload: dict
    priority: int = 2
    affinity: frozenset | None = None
    group: str | None = None
    id: str = field(default_factory=lambda: secrets.token_hex(8))
    state: str = "queued"
    account: str | None = None
    pinned: str | None = None
    excluded: dict = field(default_factory=dict)
    attempts: int = 0
    not_before: float = 0.0
    created: float = 0.0
    started: float | None = None
    finished: float | None = None
    progress: dict = field(default_factory=dict)
    result: dict | None = None
    error: str | None = None
    waiting: str | None = None
    yield_requested: bool = False
    seq: int = 0

    def fits(self, account, now):
        return (self.state == "queued" and now >= self.not_before and account not in self.excluded
                and (self.pinned is None or self.pinned == account)
                and (self.affinity is None or account in self.affinity))

    def possible(self, accounts):
        return any(account not in self.excluded and (self.pinned in (None, account))
                   and (self.affinity is None or account in self.affinity) for account in accounts)

    def public(self, now):
        return {"id": self.id, "kind": self.kind, "group": self.group, "priority": self.priority,
                "state": self.state, "account": self.account, "pinned": self.pinned,
                "affinity": sorted(self.affinity) if self.affinity is not None else None,
                "excluded": dict(self.excluded), "attempts": self.attempts, "waiting": self.waiting,
                "retry_in": round(max(0.0, self.not_before - now), 1) if self.state == "queued" else None,
                "seconds": round((self.finished or now) - self.started, 1) if self.started else None,
                "progress": dict(self.progress), "result": self.result, "error": self.error,
                "payload": {key: value for key, value in self.payload.items() if not key.startswith("_")}}


class SwarmScheduler:
    def __init__(self, *, availability=None, clock=time.monotonic):
        self.availability = availability or (lambda account: 0)
        self.clock = clock
        self.tasks, self.accounts = {}, set()
        self.idle_since = {}
        self.counter = itertools.count()
        self.event, self.loop = None, None

    def _event(self):
        loop = asyncio.get_running_loop()
        if self.event is None or self.loop is not loop:
            self.event, self.loop = asyncio.Event(), loop
        return self.event

    def poke(self):
        if self.event is not None:
            event, self.event = self.event, asyncio.Event()
            event.set()

    def submit(self, task):
        task.seq, task.created, task.state = next(self.counter), self.clock(), "queued"
        task.priority = max(0, min(3, int(task.priority)))
        self.tasks[task.id] = task
        self.poke()
        return task

    def pick(self, account):
        now = self.clock()
        best = None
        for task in self.tasks.values():
            if task.fits(account, now) and (best is None or (task.priority, task.seq) < (best.priority, best.seq)):
                best = task
        return best

    def compatible_waiting(self, account):
        now = self.clock()
        return any(task.fits(account, now) for task in self.tasks.values())

    def next_ready(self):
        now = self.clock()
        later = [task.not_before - now for task in self.tasks.values()
                 if task.state == "queued" and task.not_before > now]
        return min(later, default=None)

    async def wait(self, timeout):
        event = self._event()
        try:
            await asyncio.wait_for(event.wait(), timeout)
        except TimeoutError:
            pass

    async def steal_loop(self, account):
        self.accounts.add(account)
        try:
            while True:
                now = self.clock()
                delay = self.availability(account)
                if delay is None:
                    self.idle_since.pop(account, None)
                    await self.wait(IDLE_CHECK)
                    continue
                if delay > 0:
                    self.idle_since.pop(account, None)
                    await self.wait(min(delay, IDLE_CHECK))
                    continue
                task = self.pick(account)
                if task is None:
                    self.idle_since.setdefault(account, now)
                    ready = self.next_ready()
                    await self.wait(min(IDLE_CHECK, ready) if ready is not None else IDLE_CHECK)
                    continue
                self.idle_since.pop(account, None)
                task.state, task.account, task.started, task.finished = "running", account, now, None
                task.attempts += 1
                task.waiting = task.error = None
                task.yield_requested = False
                try:
                    yield task
                finally:
                    if task.state == "running" and task.account == account:
                        self.requeue(task)
        finally:
            self.accounts.discard(account)
            self.idle_since.pop(account, None)

    def finish(self, task, result=None):
        task.state, task.result, task.finished, task.waiting = "done", result, self.clock(), None
        self.poke()

    def fail(self, task, error):
        task.state, task.error, task.finished, task.waiting = "failed", error, self.clock(), None
        self.poke()

    def requeue(self, task, delay=0, reason=None, exclude=None):
        if task.state in FINAL:
            return
        if exclude is not None:
            task.excluded[exclude] = reason or "unsuitable"
        task.state, task.account, task.started = "queued", None, None
        task.not_before = self.clock() + max(0, delay)
        task.waiting = reason if delay else None
        self.poke()

    def get(self, task_id):
        task = self.tasks.get(task_id)
        if task is None:
            raise ValueError("This task is no longer in the queue.")
        return task

    def cancel(self, task_id):
        task = self.get(task_id)
        if task.state in ACTIVE:
            task.state, task.finished = "cancelled", self.clock()
            self.poke()
        return task

    def reprioritize(self, task_id, priority):
        task = self.get(task_id)
        task.priority = max(0, min(3, int(priority)))
        self.poke()
        return task

    def reassign(self, task_id, account):
        task = self.get(task_id)
        if task.state not in ACTIVE:
            raise ValueError("Only a waiting or running task can move to another account.")
        if account is not None and task.affinity is not None and account not in task.affinity:
            raise ValueError("That account has no access to this chat.")
        task.pinned = account
        task.excluded.pop(account, None)
        if task.state == "running" and task.account != account:
            task.yield_requested = True
        else:
            task.not_before = 0.0
        self.poke()
        return task

    def rebalance(self, accounts=None):
        accounts = set(self.accounts if accounts is None else accounts)
        changed = 0
        for task in self.tasks.values():
            if task.state == "queued" and accounts and not task.possible(accounts):
                self.fail(task, "No account can do this task.")
                changed += 1
        return changed

    def forget(self, group):
        for task_id in [task.id for task in self.tasks.values() if task.group == group and task.state in FINAL]:
            del self.tasks[task_id]

    def snapshot(self, group=None):
        now = self.clock()
        rows = [task.public(now) for task in sorted(self.tasks.values(), key=lambda t: (t.priority, t.seq))
                if group is None or task.group == group]
        counts = {state: sum(1 for row in rows if row["state"] == state) for state in (*ACTIVE, *FINAL)}
        return {"tasks": rows, "counts": counts, "accounts": sorted(self.accounts),
                "idle": {account: round(now - since, 1) for account, since in self.idle_since.items()},
                "meaning": MEANING}
