import asyncio
import re
import secrets
import time
from contextlib import suppress

from telethon import errors, functions, types, utils

from .. import export_history
from ..store import utcnow
from .scheduler import FINAL, SwarmScheduler, Task

SETTING = "swarm_exports"
USERNAME = re.compile(r"[A-Za-z][A-Za-z0-9_]{3,31}")
LINK = re.compile(r"(?:https?://)?(?:www\.)?(?:t\.me|telegram\.me|telegram\.dog)/(.+)", re.I)
RESERVED = frozenset({"joinchat", "addstickers", "addemoji", "addlist", "proxy", "socks", "share", "login",
                      "setlanguage", "confirmphone", "boost", "giftcode", "invoice", "iv", "c", "s", "m"})
PEERS_PER_JOB = 500
JOBS_KEPT = 20
POLL = 1.0
BUSY_RETRY = 5
WAIT_FLOOR = 3
PACED = ("messages.getHistory", "contacts.resolveUsername", "channels.getMessages", "messages.getMessages",
         "channels.getFullChannel", "messages.checkChatInvite")
FILES = (None, "download", "hashes", "skip")
MEANING = ("Each chat is exported by one free account and saved in that account's workspace, under Exports → Prepared "
           "exports. Accounts that are observing or busy take no task until they are free.")


class Fatal(Exception):
    pass


class Unsuitable(Exception):
    pass


def parse_peer(line):
    text = line.strip()
    if not text or text.startswith("#"):
        return None
    if text.startswith("@"):
        return username(text[1:], text)
    if match := LINK.fullmatch(text):
        path = match.group(1).split("?", 1)[0].split("#", 1)[0].strip("/")
        if path.startswith("+"):
            return invite(path[1:], text)
        parts = path.split("/")
        if parts[0].lower() == "joinchat" and len(parts) > 1:
            return invite(parts[1], text)
        if parts[0] == "c" and len(parts) > 1 and parts[1].isdigit():
            return {"kind": "id", "value": -1000000000000 - int(parts[1]), "input": text}
        if parts[0] == "s" and len(parts) > 1:
            return username(parts[1], text)
        return username(parts[0], text)
    if re.fullmatch(r"-?\d{3,20}", text):
        return {"kind": "id", "value": int(text), "input": text}
    return username(text, text)


def username(value, text):
    if not USERNAME.fullmatch(value) or value.lower() in RESERVED:
        raise ValueError("Not a username, t.me link or chat ID")
    return {"kind": "username", "value": value, "input": text}


def invite(value, text):
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", value):
        raise ValueError("Not a valid invite link")
    return {"kind": "invite", "value": value, "input": text}


def parse_peers(text):
    peers, problems, seen = [], [], set()
    for number, line in enumerate(str(text or "").splitlines(), 1):
        try:
            peer = parse_peer(line)
        except ValueError as exc:
            problems.append({"line": number, "input": line.strip()[:200], "reason": str(exc)})
            continue
        if peer is None:
            continue
        key = (peer["kind"], str(peer["value"]).lower())
        if key in seen:
            continue
        seen.add(key)
        peers.append(peer)
    if len(peers) > PEERS_PER_JOB:
        raise ValueError("Paste at most 500 chats at once.")
    return peers, problems


class SwarmExports:
    def __init__(self, app, clock=time.time):
        self.app, self.clock = app, clock
        self.scheduler = SwarmScheduler(availability=self.availability)
        self.jobs, self.loops, self.supervisor, self.cooldown = {}, {}, None, {}
        self.active = {}
        self.closing = False
        self.load()

    def entries(self):
        registry = getattr(self.app.state, "profiles", None)
        if registry is None:
            return {"default": {"label": self.app.state.store.get_setting("profile_label", "Main workspace"),
                                "app": self.app}}
        return {key: entry for key, entry in registry.entries.items() if entry.get("app") is not None}

    def app_for(self, profile):
        entry = self.entries().get(profile)
        if entry is None:
            raise Unsuitable("This workspace is unavailable.")
        return entry["app"]

    def wait_left(self, collector):
        now = self.clock()
        waits = [until for key, until in collector.flood_waits().items() if key.split("@", 1)[0] in PACED]
        waits.append(collector.store.get_setting("rpc_backoff_until", 0) or 0)
        return max([until - now for until in waits if isinstance(until, (int, float))], default=0)

    def availability(self, profile):
        entry = self.entries().get(profile)
        if entry is None:
            return None
        rest = self.cooldown.get(profile, 0) - self.clock()
        if rest > 0:
            return rest
        collector = entry["app"].state.collector
        if collector.authorization_required or not (collector.store.get_setting("account", None) or {}).get("id"):
            return None
        if (collector.running or collector.observation_starting or collector.export_claim or collector.export_busy()
                or collector.history.busy or collector.connection_change_task):
            return BUSY_RETRY
        left = self.wait_left(collector)
        return left if left > WAIT_FLOOR else 0

    def account_rows(self):
        rows = []
        for profile, entry in self.entries().items():
            collector = entry["app"].state.collector
            account = collector.store.get_setting("account", None) or {}
            delay = self.availability(profile)
            state = ("unavailable" if delay is None else "free" if delay == 0 else
                     "waiting" if delay > BUSY_RETRY or self.wait_left(collector) > WAIT_FLOOR else "busy")
            rows.append({"id": profile, "label": entry.get("label") or profile, "account_id": account.get("id"),
                         "username": account.get("username"), "state": state,
                         "wait_seconds": round(delay) if state == "waiting" else None,
                         "task": next((t.id for t in self.scheduler.tasks.values()
                                       if t.state == "running" and t.account == profile), None)})
        return rows

    def known_chats(self):
        known = {}
        for profile, entry in self.entries().items():
            collector = entry["app"].state.collector
            chats = set(getattr(collector, "dialog_cache", {}) or {})
            with suppress(Exception):
                chats.update(target["chat_id"] for target in collector.store.targets())
            known[profile] = chats
        return known

    def start(self, text, *, accounts=None, files=None, priority=2, owner=None):
        if files not in FILES:
            raise ValueError("Unknown attachment option.")
        known = set(self.entries())
        if accounts is not None:
            accounts = [account for account in dict.fromkeys(accounts) if account in known]
            if not accounts:
                raise ValueError("Choose at least one account workspace.")
        peers, problems = parse_peers(text)
        if not peers:
            raise ValueError("Paste at least one @username, t.me link or chat ID.")
        job_id = secrets.token_hex(8)
        job = {"id": job_id, "created_at": utcnow(), "owner": owner, "files": files, "accounts": accounts,
               "problems": problems, "peers": len(peers)}
        self.jobs[job_id] = job
        allowed = frozenset(accounts) if accounts is not None else None
        known = self.known_chats() if any(peer["kind"] == "id" for peer in peers) else {}
        for peer in peers:
            affinity = allowed
            knowers = {profile for profile, chats in known.items() if peer["kind"] == "id" and peer["value"] in chats}
            if knowers:
                affinity = frozenset(knowers & allowed) if allowed is not None else frozenset(knowers)
                if not affinity:
                    affinity = allowed
            self.scheduler.submit(Task("chat_export", {"peer": peer}, priority=priority, affinity=affinity, group=job_id))
        self.save()
        self.ensure_running()
        return self.public_job(job)

    def ensure_running(self):
        if self.closing:
            return
        for profile in self.entries():
            loop = self.loops.get(profile)
            if loop is None or loop.done():
                self.loops[profile] = asyncio.get_running_loop().create_task(self.serve(profile))
        if self.supervisor is None or self.supervisor.done():
            self.supervisor = asyncio.get_running_loop().create_task(self.supervise())

    async def serve(self, profile):
        async for task in self.scheduler.steal_loop(profile):
            operation = asyncio.create_task(self.run(task, profile))
            self.active[task.id] = operation
            try:
                await operation
            except asyncio.CancelledError:
                if task.state != "cancelled" or asyncio.current_task().cancelling():
                    raise
            except Exception as exc:
                self.scheduler.fail(task, type(exc).__name__)
            finally:
                self.active.pop(task.id, None)
                self.save()

    async def supervise(self):
        try:
            while any(task.state not in FINAL for task in self.scheduler.tasks.values()):
                await asyncio.sleep(2)
                if self.scheduler.rebalance(set(self.entries())):
                    self.save()
        finally:
            for loop in list(self.loops.values()):
                loop.cancel()
            await asyncio.gather(*self.loops.values(), return_exceptions=True)
            self.loops = {}
            self.supervisor = None
            if not self.closing and any(task.state not in FINAL for task in self.scheduler.tasks.values()):
                self.ensure_running()

    async def resolve(self, collector, peer):
        client = collector.client
        if client is None or not client.is_connected():
            await collector.restore()
            client = collector.client
        try:
            if peer["kind"] == "username":
                return await asyncio.wait_for(client.get_entity(peer["value"]), 60)
            if peer["kind"] == "id":
                try:
                    return await collector.resolve_target(peer["value"])
                except ValueError as exc:
                    raise Unsuitable("This account has no access to this chat.") from exc
            answer = await asyncio.wait_for(client(functions.messages.CheckChatInviteRequest(hash=peer["value"])), 60)
            if isinstance(answer, types.ChatInviteAlready):
                return answer.chat
            raise Unsuitable("This account is not a member; joining is never automatic.")
        except (errors.UsernameNotOccupiedError, errors.UsernameInvalidError) as exc:
            raise Fatal("Telegram has no chat with this username.") from exc
        except (errors.InviteHashExpiredError, errors.InviteHashInvalidError) as exc:
            raise Fatal("The invite link is invalid or expired.") from exc
        except (errors.ChannelPrivateError, errors.ChatAdminRequiredError, errors.ChannelInvalidError) as exc:
            raise Unsuitable("This account has no access to this chat.") from exc
        except ValueError as exc:
            if peer["kind"] == "username":
                raise Fatal("Telegram has no chat with this username.") from exc
            raise Unsuitable(str(exc)) from exc

    async def run(self, task, profile):
        job = self.jobs[task.group]
        app = self.app_for(profile)
        collector = app.state.collector
        try:
            entity = await self.resolve(collector, task.payload["peer"])
        except (errors.FloodWaitError, errors.FloodPremiumWaitError) as exc:
            self.cooldown[profile] = self.clock() + exc.seconds + 1
            self.scheduler.requeue(task, reason="telegram_wait")
            return
        except Unsuitable as exc:
            self.scheduler.requeue(task, exclude=profile, reason=str(exc))
            return
        except Fatal as exc:
            self.scheduler.fail(task, str(exc))
            return
        chat_id = utils.get_peer_id(entity)
        task.progress.update(chat_id=chat_id, title=utils.get_display_name(entity) or None)
        if task.state == "cancelled":
            return
        previous_export, export_id = collector.export_task, None
        try:
            try:
                record = await collector.start_export(chat_id, None, job["files"], False)
            except ValueError as exc:
                if "busy" in str(exc):
                    self.scheduler.requeue(task, delay=BUSY_RETRY, reason="account_busy")
                else:
                    self.scheduler.requeue(task, exclude=profile, reason=str(exc))
                return
            export_id = record["id"]
            task.progress["export_id"] = export_id
            state = record
            while True:
                state = collector.poll_export(export_id)
                task.progress.update({key: state.get(key) for key in ("captured", "total", "eta_seconds", "stage",
                                                                      "files_done", "files_total")})
                left = self.wait_left(collector)
                task.waiting = "telegram_wait" if left > WAIT_FLOOR else None
                task.progress["wait_seconds"] = round(left) if task.waiting else None
                if state.get("phase") != "running":
                    break
                if task.state == "cancelled":
                    return
                if task.yield_requested:
                    await self.stop_export(collector, export_id)
                    self.scheduler.requeue(task, reason="moved_by_operator")
                    return
                await asyncio.sleep(POLL)
            task.waiting = None
            if state.get("ready") and collector.export_path is not None:
                entry = await asyncio.to_thread(
                    export_history.prepared, app.state.store, collector.export_path, "zip", False,
                    owner=job.get("owner"), workspace=profile,
                    required_permissions=["view", "export"], chat_ids=[chat_id])
                result = {"workspace": profile, "prepared": entry["id"], "bytes": entry["bytes"],
                          "sha256": entry["sha256"], "filename": state.get("filename"),
                          "captured": state.get("captured"), "partial": state.get("phase") != "done",
                          "cache_warning": entry.get("cache_warning")}
                if state.get("phase") == "done":
                    self.scheduler.finish(task, result)
                else:
                    task.result = result
                    self.scheduler.fail(task, state.get("error") or "Failed")
                return
            if state.get("phase") == "cancelled" and task.state != "cancelled":
                self.scheduler.fail(task, "The export was cancelled in its workspace.")
                return
            error = state.get("error") or "Failed"
            if collector.authorization_required:
                self.scheduler.requeue(task, exclude=profile, reason="Telegram signed this account out.")
            else:
                self.scheduler.fail(task, error)
        finally:
            if export_id is None and collector.export_task is not previous_export:
                export_id = (collector.export_state or {}).get("id")
            if export_id is not None:
                await self.stop_export(collector, export_id)

    async def stop_export(self, collector, export_id):
        if not collector.export_busy() or (collector.export_state or {}).get("id") != export_id:
            return
        if collector.export_state.get("phase") == "running":
            stopping = asyncio.create_task(collector.cancel_export(export_id))
        else:
            stopping = asyncio.gather(collector.export_task, return_exceptions=True)
        cancelled = False
        while not stopping.done():
            try:
                await asyncio.shield(stopping)
            except asyncio.CancelledError:
                cancelled = True
        if cancelled:
            if not stopping.cancelled():
                stopping.exception()
            raise asyncio.CancelledError
        stopping.result()

    def task(self, task_id):
        return self.scheduler.get(task_id)

    def control(self, task_id, action, *, priority=None, account=None):
        if action == "cancel":
            task = self.scheduler.cancel(task_id)
            operation = self.active.get(task_id)
            if task.state == "cancelled" and operation is not None:
                operation.cancel()
        elif action == "priority":
            task = self.scheduler.reprioritize(task_id, priority if priority is not None else 2)
        elif action == "reassign":
            if account is not None and account not in self.entries():
                raise ValueError("Unknown account workspace.")
            task = self.scheduler.reassign(task_id, account)
        elif action == "retry":
            task = self.scheduler.get(task_id)
            if task_id in self.active:
                raise ValueError("This export is still stopping. Retry when it has stopped.")
            if task.state not in ("failed", "cancelled"):
                raise ValueError("Only a failed or cancelled task can start again.")
            task.excluded.clear()
            task.result = task.error = None
            task.state = "queued"
            self.scheduler.requeue(task)
            self.ensure_running()
        else:
            raise ValueError("Unknown action.")
        self.save()
        return task.public(self.scheduler.clock())

    def forget(self, job_id):
        if any(task.group == job_id and (task.state not in FINAL or task.id in self.active)
               for task in self.scheduler.tasks.values()):
            raise ValueError("Cancel the waiting tasks of this export first.")
        self.scheduler.forget(job_id)
        self.jobs.pop(job_id, None)
        self.save()

    def download(self, job_id, task_id):
        task = self.scheduler.get(task_id)
        if task.group != job_id or not task.result:
            raise ValueError("No finished export is available to download.")
        app = self.app_for(task.result["workspace"])
        path, entry = export_history.locate(app.state.store, task.result["prepared"])
        return path, task.result.get("filename") or ("tgwitness-chat-export-" + task.id + ".zip")

    def public_job(self, job):
        snapshot = self.scheduler.snapshot(job["id"])
        return {**{key: job.get(key) for key in ("id", "created_at", "files", "accounts", "problems", "peers")},
                "tasks": snapshot["tasks"], "counts": snapshot["counts"]}

    def public(self):
        jobs = sorted(self.jobs.values(), key=lambda job: job["created_at"], reverse=True)
        return {"jobs": [self.public_job(job) for job in jobs], "accounts": self.account_rows(), "meaning": MEANING}

    def save(self):
        jobs = sorted(self.jobs.values(), key=lambda job: job["created_at"], reverse=True)[:JOBS_KEPT]
        now = self.scheduler.clock()
        saved = [{**job, "tasks": [task.public(now) for task in self.scheduler.tasks.values() if task.group == job["id"]]}
                 for job in jobs]
        with suppress(Exception):
            self.app.state.store.set_setting(SETTING, saved)

    def load(self):
        with suppress(Exception):
            for job in self.app.state.store.get_setting(SETTING, None) or []:
                tasks = job.pop("tasks", [])
                self.jobs[job["id"]] = job
                for row in tasks:
                    affinity = row.get("affinity", job.get("accounts"))
                    task = Task(row["kind"], row["payload"], priority=row["priority"], group=job["id"], id=row["id"],
                                affinity=frozenset(affinity) if affinity is not None else None,
                                pinned=row.get("pinned"))
                    self.scheduler.submit(task)
                    task.account, task.result, task.progress = row.get("account"), row.get("result"), row.get("progress") or {}
                    task.excluded, task.attempts = dict(row.get("excluded") or {}), row.get("attempts", 0)
                    if row["state"] in FINAL:
                        task.state, task.error = row["state"], row.get("error")
                    else:
                        task.state, task.error = "failed", "TgWitness restarted before this task finished. Start it again."
                    task.finished = self.scheduler.clock()

    async def close(self):
        self.closing = True
        for loop in [*self.loops.values(), *([self.supervisor] if self.supervisor else [])]:
            loop.cancel()
        await asyncio.gather(*self.loops.values(), *([self.supervisor] if self.supervisor else []),
                             return_exceptions=True)
        self.save()
