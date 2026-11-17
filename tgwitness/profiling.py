import asyncio
import contextvars
import hashlib
import json
import secrets
import time
from collections import deque

from cryptography.fernet import InvalidToken
from telethon import functions, types, utils
from telethon.extensions import BinaryReader

from .people import profile_from_entity
from .profile_capture import ProfileCapture
from .scope import public_username
from .store import canonical, utcnow
from .telegram_client import FLOOD_ERRORS, in_lane


STAGES = ("profile", "avatars", "gifts", "links", "done")
PERMANENT = {"UserIdInvalidError", "UserDeactivatedError", "InputUserDeactivatedError", "ChannelPrivateError",
    "ChatAdminRequiredError", "UsernameInvalidError", "UsernameNotOccupiedError", "PeerIdInvalidError"}
HANDBACK = {"UserIdInvalidError", "PeerIdInvalidError", "MsgIdInvalidError"}
LOST = {"ChannelPrivateError", "ChannelInvalidError"}
MESSAGE_KINDS = ("message.new", "message.snapshot", "message.recovered")
SHARED_KINDS = ("channel", "supergroup")
HELPER_RETRY = 30
WORKER = contextvars.ContextVar("profiling_worker", default=None)


class CollectionPaused(Exception):
    pass


class HelperStopped(Exception):
    pass


class Helper:
    def __init__(self, profile, label):
        self.profile, self.label = profile, label
        self.collector = self.account_id = self.owner = self.channel = self.task = None
        self.state, self.error = "waiting", None
        self.wait_until = self.next_rpc = self.flood_until = self.retry_at = 0
        self.done = 0

    @property
    def active(self):
        return self.task is not None and not self.task.done()

    def public(self):
        return {"profile": self.profile, "label": self.label, "account_id": self.account_id, "state": self.state,
            "error": self.error, "done": self.done, "wait_until": self.wait_until or None}


def unpack(row):
    if row is None:
        return None
    result = dict(row)
    for key in ("options", "links"):
        if key in result:
            result[key] = json.loads(result[key])
    return result


class Profiling(ProfileCapture):
    def __init__(self, collector):
        self.collector, self.store = collector, collector.store
        self.task = None
        self.next_rpc = self.flood_until = 0
        self.rpc_interval = 1
        self.registry = None
        self.helpers, self.claimed, self.samples = {}, set(), deque(maxlen=400)
        self.helpers_checked = 0
        with self.store.transaction():
            for statement in (
                "CREATE TABLE IF NOT EXISTS profiling_runs(id TEXT PRIMARY KEY,account_id INTEGER NOT NULL,phase TEXT NOT NULL,"
                "created_at TEXT NOT NULL,updated_at TEXT NOT NULL,options TEXT NOT NULL,reason TEXT,wait_until REAL NOT NULL DEFAULT 0,"
                "current_user INTEGER,current_stage TEXT)",
                "CREATE TABLE IF NOT EXISTS profiling_sources(run_id TEXT,chat_id INTEGER,title TEXT,phase TEXT NOT NULL DEFAULT 'pending',"
                "position INTEGER NOT NULL DEFAULT 0,total INTEGER,last_page TEXT,attempts INTEGER NOT NULL DEFAULT 0,error TEXT,"
                "PRIMARY KEY(run_id,chat_id)) WITHOUT ROWID",
                "CREATE TABLE IF NOT EXISTS profiling_users(run_id TEXT,user_id INTEGER,peer BLOB,stage TEXT NOT NULL DEFAULT 'profile',"
                "phase TEXT NOT NULL DEFAULT 'pending',cursor TEXT NOT NULL DEFAULT '',links TEXT NOT NULL DEFAULT '[]',"
                "avatars INTEGER NOT NULL DEFAULT 0,gifts INTEGER NOT NULL DEFAULT 0,attempts INTEGER NOT NULL DEFAULT 0,"
                "failures INTEGER NOT NULL DEFAULT 0,next_attempt REAL NOT NULL DEFAULT 0,updated REAL NOT NULL DEFAULT 0,error TEXT,"
                "PRIMARY KEY(run_id,user_id)) WITHOUT ROWID",
                "CREATE INDEX IF NOT EXISTS profiling_queue ON profiling_users(run_id,phase,next_attempt,updated)",
                "CREATE TABLE IF NOT EXISTS profiling_members(run_id TEXT,user_id INTEGER,chat_id INTEGER,"
                "PRIMARY KEY(run_id,user_id,chat_id)) WITHOUT ROWID",
                "CREATE TABLE IF NOT EXISTS profiling_records(run_id TEXT,user_id INTEGER,chat_id INTEGER,kind TEXT,identity TEXT,event_seq INTEGER,"
                "PRIMARY KEY(run_id,user_id,chat_id,kind,identity)) WITHOUT ROWID",
            ):
                self.store.db.execute(statement)
            columns = {row[1] for row in self.store.db.execute("PRAGMA table_info(profiling_users)")}
            for column in ("worker TEXT", "ref INTEGER"):
                if column.split()[0] not in columns:
                    self.store.db.execute("ALTER TABLE profiling_users ADD COLUMN " + column)

    @property
    def busy(self):
        return self.task is not None and not self.task.done()

    @property
    def client(self):
        worker = WORKER.get()
        return (worker.collector if worker else self.collector).client

    def current(self):
        return unpack(self.store.db.execute("SELECT * FROM profiling_runs ORDER BY rowid DESC LIMIT 1").fetchone())

    def status(self):
        run = self.current()
        if run is None:
            return {"phase": "idle", "sources": [], "counts": {}}
        counts = {row[0]: row[1] for row in self.store.db.execute(
            "SELECT phase,count(*) FROM profiling_users WHERE run_id=? GROUP BY phase", (run["id"],))}
        totals = self.store.db.execute("SELECT coalesce(sum(avatars),0),coalesce(sum(gifts),0) FROM profiling_users WHERE run_id=?", (run["id"],)).fetchone()
        sources = [dict(row) for row in self.store.db.execute("SELECT chat_id,title,phase,position,total,error FROM profiling_sources WHERE run_id=? ORDER BY chat_id", (run["id"],))]
        discovered = all(source["phase"] != "pending" for source in sources)
        total, done = sum(counts.values()), counts.get("complete", 0) + counts.get("partial", 0)
        workers = []
        for profile in run["options"].get("accounts") or []:
            worker = self.helpers.get(profile)
            row = (worker or Helper(profile, self.label_of(profile))).public()
            if worker is None and run["phase"] != "running":
                row["state"] = "stopped"
            workers.append(row)
        return {key: run[key] for key in ("id", "phase", "created_at", "updated_at", "options", "reason", "wait_until", "current_user", "current_stage")} | {
            "sources": sources, "counts": {**counts, "total": total, "avatars": totals[0], "gifts": totals[1]},
            "busy": self.busy, "discovery_complete": discovered, "workers": workers,
            "lead_done": max(0, done - sum(worker["done"] for worker in workers)),
            "eta_seconds": self.eta(run, done, total) if run["phase"] == "running" and discovered else None}

    def eta(self, run, done, total):
        now = time.monotonic()
        if self.samples and self.samples[-1][0] != run["id"]:
            self.samples.clear()
        if not self.samples or now - self.samples[-1][1] >= 5:
            self.samples.append((run["id"], now, done))
        window = [sample for sample in self.samples if now - sample[1] <= 900]
        if not window or now - window[0][1] < 20 or done <= window[0][2]:
            return None
        return round((total - done) / ((done - window[0][2]) / (now - window[0][1])))

    def change_run(self, run, **values):
        values["updated_at"] = utcnow()
        with self.store.transaction():
            self.store.db.execute("UPDATE profiling_runs SET " + ",".join(key + "=?" for key in values) + " WHERE id=?", (*values.values(), run["id"]))
        run.update(values)

    def update_job(self, run, job, **values):
        values["updated"] = time.time()
        encoded = {key: canonical(value).decode() if key == "links" else value for key, value in values.items()}
        with self.store.transaction():
            self.store.db.execute("UPDATE profiling_users SET " + ",".join(key + "=?" for key in encoded) + " WHERE run_id=? AND user_id=?",
                (*encoded.values(), run["id"], job["user_id"]))
        job.update(values)

    def source_update(self, run, source, **values):
        with self.store.transaction():
            self.store.db.execute("UPDATE profiling_sources SET " + ",".join(key + "=?" for key in values) + " WHERE run_id=? AND chat_id=?",
                (*values.values(), run["id"], source["chat_id"]))
        source.update(values)

    def emit(self, run, job, kind, payload):
        self.require_account(run)
        worker = WORKER.get()
        collected_by = worker.account_id if worker else run["account_id"]
        digest = hashlib.sha256(canonical(payload)).hexdigest()
        identity = str(payload.get("key", payload.get("photo_id", ""))) + ":" + digest
        with self.store.transaction():
            for row in self.store.db.execute("SELECT chat_id FROM profiling_members WHERE run_id=? AND user_id=?", (run["id"], job["user_id"])).fetchall():
                key = (run["id"], job["user_id"], row[0], kind, identity)
                if self.store.db.execute("SELECT 1 FROM profiling_records WHERE run_id=? AND user_id=? AND chat_id=? AND kind=? AND identity=?", key).fetchone():
                    continue
                event = self.store.append(kind, {"user_id": job["user_id"], "profiling_run_id": run["id"],
                    "collector_account_id": collected_by, **payload}, chat_id=row[0], actor_id=job["user_id"])
                self.store.db.execute("INSERT INTO profiling_records VALUES(?,?,?,?,?,?)", (*key, event["seq"]))

    def add_user(self, run, chat_id, uid, entity=None):
        if type(uid) is not int or uid <= 0:
            return
        peer = None
        if isinstance(entity, types.User) and not entity.min:
            try:
                peer = self.collector.vault.fernet.encrypt(bytes(utils.get_input_peer(entity)))
            except (TypeError, ValueError):
                pass
        with self.store.transaction():
            self.store.db.execute("INSERT INTO profiling_users(run_id,user_id,peer) VALUES(?,?,?) ON CONFLICT(run_id,user_id) "
                "DO UPDATE SET peer=coalesce(excluded.peer,profiling_users.peer)", (run["id"], uid, peer))
            added = self.store.db.execute("INSERT OR IGNORE INTO profiling_members VALUES(?,?,?)", (run["id"], uid, chat_id)).rowcount
            if added:
                self.store.db.execute("UPDATE profiling_users SET phase='pending',stage='profile',cursor='',attempts=0,failures=0,next_attempt=0,error=NULL,avatars=0,gifts=0,"
                    "worker=CASE WHEN worker='' THEN '' END WHERE run_id=? AND user_id=? AND phase IN ('complete','partial')", (run["id"], uid))
            if entity is not None:
                profile = profile_from_entity(entity)
                if profile:
                    self.store.append("actor.profile", {"user_id": uid, "profile": profile, "source": "participant_collection",
                        "profiling_run_id": run["id"], "collector_account_id": run["account_id"]}, chat_id=chat_id, actor_id=uid)

    async def start(self, options):
        current = self.current()
        if self.busy or current and current["phase"] in {"running", "paused"}:
            raise ValueError("Resume or cancel the current profile collection first.")
        account = (self.store.get_setting("account", {}) or {}).get("id")
        if not account:
            raise ValueError("Connect a Telegram account first.")
        targets = self.store.targets(True)
        wanted = set(options["chat_ids"])
        selected = targets if options["all_chats"] else [target for target in targets if target["chat_id"] in wanted]
        if not selected or wanted - {target["chat_id"] for target in selected}:
            raise ValueError("Choose enabled chats before collecting their profiles.")
        uid = options.get("user_id")
        if uid and (len(selected) != 1 or not self.store.read_index.people.state(selected[0]["chat_id"], uid)):
            raise ValueError("Choose a user already observed in this chat.")
        accounts = options.get("accounts") or []
        if accounts:
            if options["all_chats"] or len(selected) != 1 or uid:
                raise ValueError("Other accounts can help with one chat at a time.")
            if selected[0].get("kind") not in SHARED_KINDS:
                raise ValueError("Only channels and supergroups can be shared between accounts: in other chats each account numbers messages differently.")
            for profile in accounts:
                entry = (self.registry.entries if self.registry else {}).get(profile)
                if not entry or entry.get("app") is None or entry["app"].state.collector is self.collector:
                    raise ValueError("Choose other account workspaces that are open.")
            entity = self.collector.dialog_cache.get(selected[0]["chat_id"], {}).get("entity")
            options = {**options, "username": public_username(entity) if entity is not None else None}
        self.helpers, self.claimed = {}, set()
        run = {"id": secrets.token_hex(16), "account_id": account, "phase": "running", "options": options,
            "created_at": utcnow(), "updated_at": utcnow()}
        with self.store.transaction():
            self.store.db.execute("INSERT INTO profiling_runs(id,account_id,phase,created_at,updated_at,options) VALUES(?,?,?,?,?,?)",
                (run["id"], account, "running", run["created_at"], run["updated_at"], canonical(options).decode()))
            for target in selected:
                chat = target["chat_id"]
                self.store.db.execute("INSERT INTO profiling_sources(run_id,chat_id,title,phase) VALUES(?,?,?,?)",
                    (run["id"], chat, target["title"], "pending" if options["participants"] and not uid else "known_users"))
                condition, args = (" AND user_id=?", (uid,)) if uid else ("", ())
                self.store.db.execute("INSERT OR IGNORE INTO profiling_users(run_id,user_id) SELECT ?,user_id FROM people_state WHERE chat_id=?" + condition,
                    (run["id"], chat, *args))
                self.store.db.execute("INSERT OR IGNORE INTO profiling_members SELECT ?,user_id,chat_id FROM people_state WHERE chat_id=?" + condition,
                    (run["id"], chat, *args))
            self.store.append("profiling.started", {"profiling_run_id": run["id"], "account_id": account,
                "chat_ids": [target["chat_id"] for target in selected], "options": options,
                "meaning": "Collect account-visible profiles of known authors and accessible participants in the selected sources."})
        self.launch()
        return self.status()

    def launch(self):
        if not self.busy:
            self.task = asyncio.create_task(in_lane("bulk", self.work))

    def restore(self):
        run = self.current()
        if run and run["phase"] == "running":
            self.disown(run)
            self.launch()

    def label_of(self, profile):
        entry = (self.registry.entries if self.registry else {}).get(profile) or {}
        return entry.get("label") or profile

    def disown(self, run, profile=None):
        condition, args = ("worker=?", (profile,)) if profile else ("worker IS NOT NULL AND worker<>''", ())
        with self.store.transaction():
            self.store.db.execute("UPDATE profiling_users SET avatars=CASE WHEN stage='avatars' THEN 0 ELSE avatars END,"
                "gifts=CASE WHEN stage='gifts' THEN 0 ELSE gifts END,cursor=CASE WHEN stage IN ('avatars','gifts') THEN '' ELSE cursor END,"
                "worker=NULL WHERE run_id=? AND phase='pending' AND " + condition, (run["id"], *args))

    def sync_helpers(self, run):
        accounts = run["options"].get("accounts") or []
        if not accounts or self.registry is None or time.monotonic() - self.helpers_checked < 2:
            return
        self.helpers_checked = time.monotonic()
        for profile in accounts:
            worker = self.helpers.setdefault(profile, Helper(profile, self.label_of(profile)))
            if worker.active or worker.state in {"no_access", "not_shared"} or time.time() < worker.retry_at:
                continue
            entry = self.registry.entries.get(profile) or {}
            app = entry.get("app")
            collector = app.state.collector if app else None
            account = (collector.store.get_setting("account", {}) or {}).get("id") if collector else None
            owner, problem = "profiling:" + run["id"], None
            if collector is None or collector is self.collector:
                problem = "unavailable"
            elif not account or collector.authorization_required or not app.state.vault.read("credentials").get("session"):
                problem = "no_account"
            elif collector.profiling.busy or not collector.reserve_export(owner):
                problem = "busy"
            if problem:
                worker.state, worker.retry_at = problem, time.time() + HELPER_RETRY
                continue
            worker.retry_at = 0
            worker.collector, worker.account_id, worker.owner = collector, account, owner
            worker.state, worker.error, worker.channel = "starting", None, None
            worker.next_rpc = worker.flood_until = worker.wait_until = 0
            worker.task = asyncio.create_task(in_lane("bulk", lambda worker=worker: self.serve(run, worker)))

    def require_helper(self, worker):
        collector = worker.collector
        if collector.export_claim != worker.owner:
            raise HelperStopped("released")
        if collector.authorization_required:
            raise HelperStopped("authorization_required")
        if (collector.store.get_setting("account", {}) or {}).get("id") != worker.account_id:
            raise HelperStopped("account_changed")

    def helper_job(self, run, worker):
        claimed = sorted(self.claimed)
        query = ("SELECT * FROM profiling_users WHERE run_id=? AND phase='pending' AND next_attempt<=? AND coalesce(ref,-1)<>0 "
            "AND (worker=? OR worker IS NULL AND stage='profile' AND cursor='')" + (" AND user_id NOT IN (" + ",".join("?" * len(claimed)) + ")" if claimed else "") +
            " ORDER BY worker IS NULL,updated,user_id LIMIT 1")
        return unpack(self.store.db.execute(query, (run["id"], time.time(), worker.profile, *claimed)).fetchone())

    def message_ref(self, chat_id, user_id):
        row = self.store.db.execute("SELECT max(message_id) FROM events WHERE json_extract(payload,'$.sender_id')=? AND chat_id=? "
            "AND kind IN (?,?,?) AND message_id>0", (user_id, chat_id, *MESSAGE_KINDS)).fetchone()
        return row[0] or 0

    async def serve(self, run, worker):
        from .collector import AUTHORIZATION_ERRORS
        WORKER.set(worker)
        chat_id = run["options"]["chat_ids"][0]
        reason = None
        try:
            self.store.append("profiling.helper_joined", {"profiling_run_id": run["id"], "workspace": worker.profile,
                "account_id": worker.account_id, "meaning": "This account collects part of the profiles; each saved record names the account that read it."})
            await worker.collector.restore()
            try:
                entity = await self.ask(run, lambda: worker.collector.resolve_for_export(chat_id, run["options"].get("username")), timeout=60)
            except (asyncio.CancelledError, CollectionPaused, HelperStopped, *FLOOD_ERRORS):
                raise
            except Exception as exc:
                if isinstance(exc, AUTHORIZATION_ERRORS):
                    raise
                worker.state = "no_access"
                raise HelperStopped("no_access") from exc
            if not isinstance(entity, types.Channel) or utils.get_peer_id(entity) != chat_id:
                worker.state = "not_shared"
                raise HelperStopped("not_shared")
            worker.channel = utils.get_input_peer(entity)
            while True:
                self.require_account(run)
                self.require_helper(worker)
                job = self.helper_job(run, worker)
                if job is None:
                    worker.state, worker.wait_until = "idle", 0
                    await asyncio.sleep(1)
                    continue
                self.claimed.add(job["user_id"])
                try:
                    ref = job["ref"] or self.message_ref(chat_id, job["user_id"])
                    if not ref:
                        self.update_job(run, job, ref=0, worker=None)
                        continue
                    if job["worker"] != worker.profile or job["ref"] != ref:
                        self.update_job(run, job, worker=worker.profile, ref=ref)
                    peer = types.InputPeerUserFromMessage(worker.channel, ref, job["user_id"])
                    stage = job["stage"]
                    try:
                        await getattr(self, "capture_" + stage)(run, job, peer)
                    except (asyncio.CancelledError, CollectionPaused, HelperStopped, *FLOOD_ERRORS):
                        raise
                    except Exception as exc:
                        if isinstance(exc, AUTHORIZATION_ERRORS):
                            raise
                        name = type(exc).__name__
                        if name in HANDBACK or name in LOST:
                            reset = {"cursor": "", stage: 0} if stage in {"avatars", "gifts"} else {}
                            self.update_job(run, job, worker="", ref=0, attempts=0, next_attempt=0, error=None, **reset)
                            if name in LOST:
                                worker.state = "no_access"
                                raise HelperStopped("no_access") from exc
                        else:
                            self.failed(run, job, exc)
                    if job["phase"] != "pending":
                        worker.done += 1
                except FLOOD_ERRORS as exc:
                    worker.flood_until = time.time() + exc.seconds + 1
                    worker.state, worker.wait_until = "waiting", worker.flood_until
                finally:
                    self.claimed.discard(job["user_id"])
                await asyncio.sleep(0)
        except HelperStopped as exc:
            reason = str(exc)
        except CollectionPaused:
            reason = "collection_paused"
        except asyncio.CancelledError:
            reason = "stopped"
            raise
        except Exception as exc:
            reason = type(exc).__name__
            if isinstance(exc, AUTHORIZATION_ERRORS):
                worker.collector.handle_authorization_error(exc, "profile_collection")
                reason = "authorization_required"
        finally:
            if reason == "stopped":
                phase = (self.current() or {}).get("phase")
                reason = "finished" if phase in {"complete", "partial"} else "paused" if phase in {"paused", "cancelled"} else reason
            worker.error = None if reason in {"finished", "paused", "stopped"} else reason
            if worker.state not in {"no_access", "not_shared"}:
                worker.state = "finished" if reason == "finished" else "stopped"
            worker.wait_until = 0
            self.disown(run, worker.profile)
            worker.collector.release_export(worker.owner)
            self.store.append("profiling.helper_left", {"profiling_run_id": run["id"], "workspace": worker.profile,
                "account_id": worker.account_id, "reason": reason, "profiles_finished": worker.done})

    async def stop_helpers(self):
        tasks = [worker.task for worker in self.helpers.values() if worker.active and worker.task is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    async def pause(self, reason="operator"):
        run = self.current()
        if run and run["phase"] == "running":
            self.change_run(run, phase="paused", reason=reason, current_user=None, current_stage=None)
            self.store.append("profiling.paused", {"profiling_run_id": run["id"], "reason": reason})
        await self.suspend()
        return self.status()

    async def suspend(self):
        if self.busy and self.task is not asyncio.current_task():
            self.task.cancel()
            await asyncio.gather(self.task, return_exceptions=True)
        await self.stop_helpers()

    async def resume(self):
        run = self.current()
        if not run or run["phase"] != "paused":
            raise ValueError("There is no paused profile collection.")
        self.require_account(run)
        self.change_run(run, phase="running", reason=None)
        self.store.append("profiling.resumed", {"profiling_run_id": run["id"]})
        for worker in self.helpers.values():
            if worker.state not in {"no_access", "not_shared"}:
                worker.retry_at = 0
        self.helpers_checked = 0
        self.launch()
        return self.status()

    async def cancel(self):
        await self.pause("cancelled")
        run = self.current()
        if run and run["phase"] == "paused":
            self.change_run(run, phase="cancelled", wait_until=0)
            self.store.append("profiling.cancelled", {"profiling_run_id": run["id"]})
        return self.status()

    async def retry(self):
        run = self.current()
        if not run or self.busy or run["phase"] not in {"complete", "partial"}:
            raise ValueError("Wait for profile collection to finish before retrying unavailable profiles.")
        self.require_account(run)
        with self.store.transaction():
            self.store.db.execute("UPDATE profiling_users SET phase='pending',stage='profile',cursor='',attempts=0,failures=0,next_attempt=0,error=NULL,avatars=0,gifts=0,"
                "worker=CASE WHEN worker='' THEN '' END WHERE run_id=? AND phase='partial'", (run["id"],))
            self.store.db.execute("UPDATE profiling_sources SET phase='pending',attempts=0,error=NULL WHERE run_id=? AND phase='partial'", (run["id"],))
            self.change_run(run, phase="running", reason=None)
        self.launch()
        return self.status()

    def require_account(self, run):
        if (self.store.get_setting("account", {}) or {}).get("id") != run["account_id"]:
            raise CollectionPaused("account_changed")
        if self.collector.authorization_required:
            raise CollectionPaused("authorization_required")
        if any(not row[0] for row in self.store.db.execute("SELECT coalesce(t.enabled,0) FROM profiling_sources s LEFT JOIN targets t ON t.chat_id=s.chat_id WHERE s.run_id=?", (run["id"],))):
            raise CollectionPaused("source_paused")

    def check(self, run, worker):
        self.require_account(run)
        if worker:
            self.require_helper(worker)

    def waiting(self, run, worker, until):
        if worker:
            worker.state, worker.wait_until = ("waiting", until) if until else ("running", 0)
        else:
            self.change_run(run, reason="telegram_wait" if until else None, wait_until=until)

    async def ask(self, run, call, timeout=30):
        worker = WORKER.get()
        pacer, store = (worker, worker.collector.store) if worker else (self, self.store)
        self.check(run, worker)
        until = max(store.get_setting("rpc_backoff_until", 0), pacer.flood_until)
        while until > time.time():
            self.waiting(run, worker, until)
            await asyncio.sleep(min(5, until - time.time()))
            self.check(run, worker)
            until = max(store.get_setting("rpc_backoff_until", 0), pacer.flood_until)
        delay = max(0, pacer.next_rpc - time.monotonic())
        if delay:
            await asyncio.sleep(delay)
        self.check(run, worker)
        self.waiting(run, worker, 0)
        pacer.next_rpc = time.monotonic() + self.rpc_interval
        try:
            answer = await asyncio.wait_for(call(), timeout)
        except asyncio.CancelledError:
            if asyncio.current_task().cancelling():
                raise
            self.check(run, worker)
            raise ConnectionError("Telegram dropped the request") from None
        self.check(run, worker)
        return answer

    async def discover(self, run, source):
        entity = self.collector.dialog_cache.get(source["chat_id"], {}).get("entity")
        if entity is None:
            entity = await self.ask(run, lambda: self.collector.lookup_entity(source["chat_id"]))
        if isinstance(entity, types.User):
            self.add_user(run, source["chat_id"], entity.id, entity)
            self.source_update(run, source, phase="complete", total=1, position=1)
            return
        if isinstance(entity, types.Channel):
            answer = await self.ask(run, lambda: self.collector.client(functions.channels.GetParticipantsRequest(
                channel=entity, filter=types.ChannelParticipantsRecent(), offset=source["position"], limit=200, hash=0)))
            participants, users, total = answer.participants, answer.users, answer.count
        elif isinstance(entity, types.Chat):
            answer = await self.ask(run, lambda: self.collector.client(functions.messages.GetFullChatRequest(entity.id)))
            participants = getattr(answer.full_chat.participants, "participants", None)
            if participants is None:
                raise ValueError("ParticipantsUnavailable")
            users, total = answer.users, len(participants)
        else:
            raise ValueError("SourceUnavailable")
        ids = [getattr(participant, "user_id", None) for participant in participants]
        digest = hashlib.sha256(canonical(ids)).hexdigest()
        if participants and digest == source["last_page"]:
            raise ValueError("ParticipantCursorDidNotAdvance")
        mapping = {user.id: user for user in users}
        with self.store.transaction():
            for uid in ids:
                self.add_user(run, source["chat_id"], uid, mapping.get(uid))
            position = source["position"] + len(participants)
            phase = "complete" if position >= total else "partial" if not participants else "pending"
            self.source_update(run, source, position=position, total=total, last_page=digest, phase=phase, attempts=0,
                error="participant_list_incomplete" if phase == "partial" else None)

    async def peer(self, run, job):
        if job["peer"]:
            try:
                saved = self.collector.vault.fernet.decrypt(job["peer"])
            except InvalidToken:
                saved = None
            if saved is not None:
                with BinaryReader(saved) as reader:
                    return reader.tgread_object()
        peer = await self.ask(run, lambda: self.collector.client.get_input_entity(types.PeerUser(job["user_id"])))
        self.update_job(run, job, peer=self.collector.vault.fernet.encrypt(bytes(peer)))
        return peer

    def finish_job(self, run, job):
        self.emit(run, job, "actor.profile_collected", {"avatars": job["avatars"], "gifts": job["gifts"], "failures": job["failures"]})
        self.update_job(run, job, stage="done", phase="partial" if job["failures"] else "complete", next_attempt=0)

    def failed(self, run, job, error):
        name = type(error).__name__
        attempts = job["attempts"] + 1
        if name not in PERMANENT and attempts < 3:
            self.update_job(run, job, attempts=attempts, next_attempt=time.time() + 5 * 2 ** (attempts - 1), error=name)
            return
        stage = job["stage"]
        self.emit(run, job, "actor.profile_unavailable", {"area": stage, "error_type": name,
            "meaning": "This part was not collected; saved observations remain available."})
        if stage == "links":
            self.update_job(run, job, cursor=str(int(job["cursor"] or 0) + 1), failures=job["failures"] + 1,
                attempts=0, next_attempt=0, error=name)
            if int(job["cursor"]) >= len(job["links"]):
                self.finish_job(run, job)
        else:
            next_stage = STAGES[STAGES.index(stage) + 1]
            self.update_job(run, job, stage=next_stage, cursor="", failures=job["failures"] + 1,
                attempts=0, next_attempt=0, error=name)

    async def work(self):
        run = self.current()
        try:
            while run and run["phase"] == "running":
                self.require_account(run)
                self.sync_helpers(run)
                if self.collector.export_claim or self.collector.export_busy() or self.collector.history.busy or self.collector.connection_change_task:
                    self.change_run(run, reason="waiting_for_account")
                    await asyncio.sleep(2)
                    continue
                await self.collector.restore()
                source = unpack(self.store.db.execute("SELECT * FROM profiling_sources WHERE run_id=? AND phase='pending' ORDER BY chat_id LIMIT 1", (run["id"],)).fetchone())
                try:
                    if source:
                        self.change_run(run, current_user=None, current_stage="participants")
                        try:
                            await self.discover(run, source)
                        except (asyncio.CancelledError, CollectionPaused, *FLOOD_ERRORS):
                            raise
                        except Exception as exc:
                            attempts = source["attempts"] + 1
                            self.source_update(run, source, attempts=attempts, error=type(exc).__name__,
                                phase="partial" if attempts >= 3 or type(exc).__name__ in PERMANENT else "pending")
                        continue
                    claimed = sorted(self.claimed)
                    job = unpack(self.store.db.execute("SELECT * FROM profiling_users WHERE run_id=? AND phase='pending' AND next_attempt<=? AND coalesce(worker,'')=''" +
                        (" AND user_id NOT IN (" + ",".join("?" * len(claimed)) + ")" if claimed else "") + " ORDER BY stage='profile',updated,user_id LIMIT 1",
                        (run["id"], time.time(), *claimed)).fetchone())
                    if job:
                        self.change_run(run, current_user=job["user_id"], current_stage=job["stage"])
                        self.claimed.add(job["user_id"])
                        try:
                            peer = await self.peer(run, job)
                            await getattr(self, "capture_" + job["stage"])(run, job, peer)
                        except (asyncio.CancelledError, CollectionPaused, *FLOOD_ERRORS):
                            raise
                        except Exception as exc:
                            self.failed(run, job, exc)
                        finally:
                            self.claimed.discard(job["user_id"])
                    elif source is None:
                        pending = self.store.db.execute("SELECT min(next_attempt) FROM profiling_users WHERE run_id=? AND phase='pending'", (run["id"],)).fetchone()[0]
                        if pending is None and not self.claimed:
                            state = self.status()
                            partial = state["counts"].get("partial", 0) or any(source["phase"] == "partial" for source in state["sources"])
                            self.change_run(run, phase="partial" if partial else "complete", current_user=None, current_stage=None, reason=None, wait_until=0)
                            await self.stop_helpers()
                            self.store.append("profiling.completed", {"profiling_run_id": run["id"], "phase": run["phase"], "counts": state["counts"]})
                            return
                        if any(worker.active for worker in self.helpers.values()) and (pending is None or pending <= time.time()):
                            self.change_run(run, current_user=None, current_stage=None, reason="helpers_working", wait_until=0)
                            await asyncio.sleep(1)
                            continue
                        if pending is None:
                            await asyncio.sleep(.2)
                            continue
                        self.change_run(run, reason="retry_wait", wait_until=pending)
                        await asyncio.sleep(min(5, max(.1, pending - time.time())))
                except FLOOD_ERRORS as exc:
                    until = max(time.time() + exc.seconds, self.store.get_setting("rpc_backoff_until", 0))
                    self.flood_until = until
                    self.change_run(run, reason="telegram_wait", wait_until=until)
                await asyncio.sleep(0)
        except CollectionPaused as exc:
            self.change_run(run, phase="paused", reason=str(exc), current_user=None, current_stage=None)
            await self.stop_helpers()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            reason = "authorization_required" if self.collector.authorization_required else type(exc).__name__
            self.change_run(run, phase="paused", reason=reason, current_user=None, current_stage=None)
            self.store.append("profiling.interrupted", {"profiling_run_id": run["id"], "error_type": type(exc).__name__})
            await self.stop_helpers()
        finally:
            for worker in self.helpers.values():
                if worker.active and worker.task is not asyncio.current_task():
                    worker.task.cancel()
            self.collector.close_when_idle()
