import asyncio
import secrets
import time
from collections import OrderedDict

from ..verify import verify_checkpoint, verify_events
from ..workers import complete_in_thread

ACTIONS = ("start", "stop", "route", "verify")
LIMITS = {"start": 180, "stop": 60, "route": 900, "verify": 3600}
KEEP = 20
CHECKS_AT_ONCE = 2


def journal_check(store, vault):
    retained = store.retained_checkpoint()
    with store.snapshot() as snapshot:
        result = verify_events(snapshot.events(), vault.public_key)
        if retained:
            verify_checkpoint(retained, vault.public_key, result["events"], snapshot.hash_at)
    return result


class BulkActions:
    def __init__(self, app):
        self.app, self.jobs, self.tasks, self.checks = app, OrderedDict(), set(), None

    def entries(self):
        registry = getattr(self.app.state, "profiles", None)
        return registry.entries if registry else {}

    def begin(self, action, profiles, owner=None):
        if action not in ACTIONS:
            raise ValueError("Unknown action.")
        entries, chosen = self.entries(), list(dict.fromkeys(profiles))
        if not chosen:
            raise ValueError("Choose at least one account workspace.")
        if any(profile not in entries for profile in chosen):
            raise ValueError("Unknown account workspace.")
        job = {"id": secrets.token_hex(8), "action": action, "owner": owner, "started_at": time.time(),
               "finished_at": None, "items": [{"profile": p, "label": entries[p].get("label") or p, "state": "queued"}
                                              for p in chosen]}
        self.jobs[job["id"]] = job
        while len(self.jobs) > KEEP:
            oldest = next(iter(self.jobs))
            if self.jobs[oldest]["finished_at"] is None:
                break
            self.jobs.pop(oldest)
        task = asyncio.create_task(self.run(job))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return self.public(job)

    async def run(self, job):
        try:
            await asyncio.gather(*(self.one(job["action"], item) for item in job["items"]))
        finally:
            job["finished_at"] = time.time()

    async def one(self, action, item):
        entry = self.entries().get(item["profile"]) or {}
        app = entry.get("app")
        if app is None:
            item.update(state="failed", code="unavailable")
            return
        item["state"] = "working"
        try:
            item.update(await asyncio.wait_for(getattr(self, action)(app), LIMITS[action]))
        except asyncio.TimeoutError:
            item.update(state="failed", code="timeout")
        except asyncio.CancelledError:
            item.update(state="failed", code="cancelled")
            raise
        except Exception as exc:
            item.update(state="failed", code="error",
                        message=str(exc) if isinstance(exc, ValueError) else type(exc).__name__)

    async def start(self, app):
        collector = app.state.collector
        if collector.running or collector.observation_starting:
            return {"state": "skipped", "code": "already_running"}
        if not collector.vault.read("credentials").get("session") or collector.authorization_required:
            return {"state": "skipped", "code": "no_session"}
        await collector.start()
        return {"state": "done", "code": "started"}

    async def stop(self, app):
        collector = app.state.collector
        if not (collector.running or collector.observation_starting):
            return {"state": "skipped", "code": "not_running"}
        await collector.stop()
        return {"state": "done", "code": "stopped"}

    async def route(self, app):
        connection = app.state.connection
        selected = connection.portable.selected()
        if not selected or selected.get("mode") != "warp" or selected.get("paused"):
            return {"state": "skipped", "code": "no_warp"}
        connection.start_reroll("automatic")
        await asyncio.shield(connection.reroll_task)
        job = connection.reroll_job or {}
        if job.get("state") != "done":
            raise ValueError(job.get("error") or "WARP re-roll failed.")
        return {"state": "done", "code": "rerolled",
                "values": {"before": job.get("before_ms"), "after": job.get("after_ms"),
                           "identity": bool(job.get("identity_changed"))}}

    async def verify(self, app):
        if self.checks is None:
            self.checks = asyncio.Semaphore(CHECKS_AT_ONCE)
        async with self.checks:
            result = await complete_in_thread(journal_check, app.state.store, app.state.vault)
        return {"state": "done", "code": "verified", "values": {"n": result["events"], "head": result["head_hash"][:16]}}

    def public(self, job):
        items = [{k: v for k, v in item.items()} for item in job["items"]]
        counts = {state: sum(item["state"] == state for item in items)
                  for state in ("queued", "working", "done", "skipped", "failed")}
        return {"id": job["id"], "action": job["action"], "started_at": job["started_at"],
                "finished_at": job["finished_at"], "counts": counts, "items": items}

    def get(self, job_id, owner=None):
        job = self.jobs.get(job_id)
        if job is None or owner is not None and job["owner"] not in (None, owner):
            raise KeyError(job_id)
        return self.public(job)

    async def close(self):
        for task in list(self.tasks):
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
