import asyncio
import time

from telethon import errors, utils
from telethon.tl import functions as f, types as t

from .deletions import age, account_id
from .monitoring import monitoring_settings
from .store import utcnow
from .telegram_client import FLOOD_ERRORS

RIGHTS_EVERY = 6 * 3600
POLL_LIMIT = 100
POLL_TIMEOUT = 30
POLL_FILTER = ["delete", "edit"]
POLL_MEANING = ("Scheduled read of this chat's admin log, deletions and edits only. Telegram keeps about 48 hours of it "
                "and shows it to administrators; each entry names the account that acted and carries the message as "
                "Telegram returned it.")
RIGHTS_MEANING = ("This account's role in the chat and its right to delete other members' messages, as "
                  "channels.getChannels returned them at this time.")
LINK_MEANING = ("The chat's admin log names the account that deleted this message. The deletion notice recorded "
                "earlier is unchanged; this record links it to the admin-log entry.")


async def page(history, job, entity, stage):
    from .collector import admin_event

    meta = history.metadata(job)
    key = "admin_" + stage
    progress = meta.setdefault(key, {"status": "reading", "offset": 0, "newest": 0,
                                    "observed": 0, "started_at": utcnow()})
    if progress["status"] != "reading":
        return False
    lower = meta.get("admin_before", {}).get("newest", 0) if stage == "after" else 0
    if not isinstance(entity, (t.Channel, t.InputPeerChannel, t.InputChannel)):
        progress.update(status="not_applicable", ended_at=utcnow())
        history.save_metadata(job, meta)
        return True
    try:
        result = await history.collector.client(f.channels.GetAdminLogRequest(entity, "",
            progress["offset"], lower, 100,
            events_filter=t.ChannelAdminLogEventsFilter(delete=True, edit=True)))
    except (errors.FloodWaitError, errors.ServerError, errors.TakeoutInvalidError):
        raise
    except errors.RPCError as exc:
        if history.collector.handle_authorization_error(exc, "history admin log", client=history.collector.client):
            raise
        progress.update(status="unavailable", error=type(exc).__name__, ended_at=utcnow())
        with history.store.transaction():
            history.store.append("history.admin_log.unavailable", {"history_run_id": job["run_id"],
                "source": "admin_log", "stage": stage, "error_type": type(exc).__name__}, job["chat_id"])
            history.save_metadata(job, meta)
        return True
    previous = progress["offset"] or 2**63
    for event in result.events:
        if not lower < event.id < previous:
            raise ValueError("Admin log did not advance the requested cursor.")
        previous = event.id
    def commit():
        committed = []
        with history.store.transaction():
            for event in result.events:
                duplicate = history.store.db.execute("SELECT 1 FROM history_admin_items "
                    "WHERE run_id=? AND chat_id=? AND provider_id=?", (job["run_id"], job["chat_id"], event.id)).fetchone()
                if duplicate:
                    continue
                observation = history.store.append("history.admin_log.observed", {
                    "history_run_id": job["run_id"], "source": "admin_log", "source_mode": "standard",
                    "stage": stage, "provider_event_id": event.id, "event": admin_event(event),
                    "meaning": "Server-reported historical action from Telegram's recent-actions window."},
                    job["chat_id"])
                history.store.db.execute("INSERT INTO history_admin_items VALUES (?,?,?,?)",
                    (job["run_id"], job["chat_id"], event.id, observation["seq"]))
                for field in ("message", "prev_message", "new_message"):
                    message = getattr(event.action, field, None)
                    if message is not None and getattr(message, "media", None):
                        captured = history.collector.commit_message(message, "message.admin_log", job["chat_id"],
                            source="admin_log", history_run_id=job["run_id"], acquisition={"source_mode": "standard",
                                "admin_event": observation["seq"], "version": field})
                        history.store.db.execute("INSERT INTO history_items VALUES (?,?)", (job["run_id"], captured["seq"]))
                        committed.append((message, captured))
                progress["observed"] += 1
            if result.events:
                progress["newest"] = max(progress["newest"], result.events[0].id)
                progress["offset"] = result.events[-1].id
                progress["oldest_event_at"] = result.events[-1].date.isoformat()
                progress.setdefault("newest_event_at", result.events[0].date.isoformat())
            else:
                progress.update(status="complete", ended_at=utcnow())
                history.store.append("history.admin_log.finished", {"history_run_id": job["run_id"],
                    "source": "admin_log", "stage": stage, **progress}, job["chat_id"])
            history.save_metadata(job, meta)
        return committed

    from .workers import complete_in_thread
    async with history.collector.capture_lock:
        committed = await complete_in_thread(commit)
    for message, event in committed:
        history.collector.message_committed(message, job["chat_id"], event)
    return True


def can_read(entry):
    return isinstance(entry, dict) and entry.get("role") in ("creator", "admin")


def save_rights(store, chat_id, entry):
    rights = store.get_setting("own_rights", {}) or {}
    previous = rights.get(str(chat_id))
    rights[str(chat_id)] = entry
    store.set_setting("own_rights", rights)
    keys = ("role", "delete_messages", "chat_type")
    if previous is None or any(previous.get(key) != entry.get(key) for key in keys):
        store.append("account.chat_rights", {**entry, "previous": {key: previous.get(key) for key in keys}
                                             if previous else None, "meaning": RIGHTS_MEANING}, chat_id)
    return entry


async def refresh_rights(collector, chat_id, peer):
    answer = await asyncio.wait_for(collector.client(f.channels.GetChannelsRequest([peer])), POLL_TIMEOUT)
    channel = next((c for c in getattr(answer, "chats", None) or [] if utils.get_peer_id(c) == chat_id), None)
    if isinstance(channel, t.Channel) and not channel.left:
        rights = channel.admin_rights
        entry = {"role": "creator" if channel.creator else "admin" if rights else "member",
                 "delete_messages": bool(channel.creator or getattr(rights, "delete_messages", False)),
                 "chat_type": "supergroup" if channel.megagroup or channel.gigagroup else "channel"}
    else:
        entry = {"role": "no_access", "delete_messages": False, "chat_type": None}
    return save_rights(collector.store, chat_id, {**entry, "checked_at": utcnow(), "source": "channels.getChannels"})


def link_deletion(store, chat_id, event, poll, me):
    from .collector import date_string
    message_id = getattr(getattr(event.action, "message", None), "id", None)
    if type(message_id) is not int:
        return None
    deleted = store.events(chat_id=chat_id, message_id=message_id, kind="message.deleted", limit=1)
    if not deleted:
        return None
    known = store.events(chat_id=chat_id, message_id=message_id, kind="message.deletion_attributed", limit=50)
    if any(record["payload"].get("admin_log_event_id") == event.id for record in known):
        return None
    return store.append("message.deletion_attributed", {
        "deletion_event": {"seq": deleted[0]["seq"], "hash": deleted[0]["hash"]},
        "admin_log_poll": {"seq": poll["seq"], "hash": poll["hash"]}, "admin_log_event_id": event.id,
        "actor_id": event.user_id, "actor_is_this_account": event.user_id == me, "acted_at": date_string(event.date),
        "source": "admin_log", "meaning": LINK_MEANING}, chat_id, message_id, event.user_id, date_string(event.date))


async def poll_log(collector, chat_id, peer, rights):
    from .collector import AUTHORIZATION_ERRORS, admin_event
    store, key = collector.store, str(chat_id)
    cursor = (store.get_setting("admin_log_cursor", {}) or {}).get(key) or {"min_id": 0, "max_id": 0, "newest": 0}
    asked = {"min_id": cursor["min_id"], "max_id": cursor["max_id"], "limit": POLL_LIMIT, "filter": POLL_FILTER}
    try:
        answer = await asyncio.wait_for(collector.client(f.channels.GetAdminLogRequest(
            peer, "", cursor["max_id"], cursor["min_id"], POLL_LIMIT,
            events_filter=t.ChannelAdminLogEventsFilter(delete=True, edit=True))), POLL_TIMEOUT)
    except (asyncio.CancelledError, *FLOOD_ERRORS, *AUTHORIZATION_ERRORS):
        raise
    except errors.RPCError as exc:
        with store.transaction():
            if isinstance(exc, errors.ChatAdminRequiredError):
                save_rights(store, chat_id, {**rights, "role": "member", "delete_messages": False,
                                             "checked_at": utcnow(), "source": "channels.getAdminLog refused"})
            cursors = store.get_setting("admin_log_cursor", {}) or {}
            cursors[key] = {**cursor, "polled_at": utcnow()}
            store.set_setting("admin_log_cursor", cursors)
            return store.append("admin_log.polled", {**asked, "error_type": type(exc).__name__, "rights": rights,
                                                     "meaning": POLL_MEANING}, chat_id)
    found = [event for event in answer.events
             if event.id > cursor["min_id"] and (not cursor["max_id"] or event.id < cursor["max_id"])]
    more = len(answer.events) >= POLL_LIMIT and bool(found)
    newest = max([cursor["newest"], *(event.id for event in found)])
    following = ({"min_id": cursor["min_id"], "max_id": min(event.id for event in found), "newest": newest} if more
                 else {"min_id": newest, "max_id": 0, "newest": newest})
    me = account_id(store)
    with store.transaction():
        poll = store.append("admin_log.polled", {
            **asked, "returned": len(found), "continues": more, "events": [admin_event(event) for event in found],
            "rights": rights, "meaning": POLL_MEANING}, chat_id)
        for event in found:
            if isinstance(event.action, t.ChannelAdminLogEventActionDeleteMessage):
                link_deletion(store, chat_id, event, poll, me)
        cursors = store.get_setting("admin_log_cursor", {}) or {}
        cursors[key] = {**following, "polled_at": utcnow()}
        store.set_setting("admin_log_cursor", cursors)
    return poll


async def scheduled(collector):
    store = collector.store
    minutes, monitoring = collector.param("admin_log_minutes"), monitoring_settings(store)
    if not minutes or not (monitoring["deletions"] or monitoring["edits"]):
        return 0
    budget, pause, used = collector.param("recheck_max_chats"), collector.param("recheck_pause_seconds"), 0
    for target in store.targets(True):
        chat_id, client = target["chat_id"], collector.client
        if used >= budget or not collector.running or time.time() < store.get_setting("rpc_backoff_until", 0):
            break
        if chat_id >= -1000000000000:
            continue
        rights = (store.get_setting("own_rights", {}) or {}).get(str(chat_id))
        cursor = (store.get_setting("admin_log_cursor", {}) or {}).get(str(chat_id)) or {}
        rights_due = rights is None or (age(rights.get("checked_at")) or 0) >= RIGHTS_EVERY
        polled = age(cursor.get("polled_at"))
        log_due = bool(cursor.get("max_id")) or polled is None or polled >= minutes * 60
        if not rights_due and not (can_read(rights) and log_due):
            continue
        try:
            peer = await client.get_input_entity(chat_id)
            if rights_due:
                rights = await refresh_rights(collector, chat_id, peer)
                rights_due = False
                used += 1
                await asyncio.sleep(pause)
                if not can_read(rights) or not log_due or used >= budget:
                    continue
            await poll_log(collector, chat_id, peer, rights)
            used += 1
            await asyncio.sleep(pause)
        except asyncio.CancelledError:
            raise
        except FLOOD_ERRORS as exc:
            store.set_setting("rpc_backoff_until", max(time.time() + exc.seconds, store.get_setting("rpc_backoff_until", 0)))
            store.append("telegram.backoff", {"operation": "admin log", "retry_after_seconds": exc.seconds})
            break
        except Exception as exc:
            if collector.handle_authorization_error(exc, "admin log", client=client):
                break
            if rights_due:
                save_rights(store, chat_id, {"role": "unknown", "delete_messages": None, "chat_type": None,
                                             "checked_at": utcnow(), "error_type": type(exc).__name__})
            else:
                cursors = store.get_setting("admin_log_cursor", {}) or {}
                cursors[str(chat_id)] = {"min_id": 0, "max_id": 0, "newest": 0, **cursor, "polled_at": utcnow()}
                store.set_setting("admin_log_cursor", cursors)
                store.append("admin_log.polled", {"error_type": type(exc).__name__, "filter": POLL_FILTER,
                                                  "meaning": POLL_MEANING}, chat_id)
    return used
