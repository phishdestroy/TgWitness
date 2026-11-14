import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, model_validator
from telethon import utils
from telethon.errors import RPCError
from telethon.tl import functions, types

from . import opsec
from .telegram_client import FLOOD_ERRORS, ReadReceiptBlocked, read_permit, request_method

LOG = logging.getLogger("tgwitness.visibility")
SETTING = "visibility"
MARKS = "visibility_marks"
OFFLINE = "hide_online_after_actions"
READS = ("never", "manual", "on_reply", "on_open")
MANUAL = ("never", "manual")
TYPINGS = ("hidden", "shown", "before_send")
SILENCE = ("never", "while_invisible", "always")
DEFAULTS = {"invisible": False, "read_receipts": "never", "content_opened": "never", "story_read": "never",
            "typing": "hidden", "silent_send": "never", "offline_after_action": False, "show_peer_typing": True,
            "record_peer_typing": False}
CHAT_FIELDS = ("read_receipts", "content_opened", "story_read", "typing", "silent_send", "show_peer_typing",
               "record_peer_typing")
FORCED = {"read_receipts": "never", "content_opened": "never", "story_read": "never", "typing": "hidden",
          "offline_after_action": True}
PRESETS = {"invisible": {"read_receipts": "never", "content_opened": "never", "story_read": "never", "typing": "hidden"},
           "visible": {"read_receipts": "on_open", "content_opened": "never", "story_read": "never", "typing": "shown"}}
SAVED = ("message.new", "message.snapshot", "message.recovered")
TYPING_SECONDS = 6
PING_SECONDS = 4
BURST_SECONDS = 15
SWEEP_SECONDS = 5
BEFORE_SEND = (1.0, 12.0)
CHARACTERS_PER_SECOND = 8
OPENED_LIMIT = 500
TIMELINE_LIMIT = 100
NOT_OBSERVED = "Enable observation for this chat in Sources first."
REFUSED = {"read_receipts": "This chat's read receipt setting does not allow this. Nothing was sent to Telegram.",
           "content_opened": "Opened-media notices are off for this chat. Nothing was sent to Telegram.",
           "story_read": "Story read receipts are off for this chat. Nothing was sent to Telegram.",
           "typing": "Typing is hidden for this chat. Nothing was sent to Telegram."}
STATUS = {"succeeded": "Telegram accepted the request.",
          "rejected": "The request was not performed.",
          "unknown": "The outcome is unknown: Telegram may or may not have applied it."}
SETTINGS_MEANING = ("What this account lets the other side of a chat see. Read receipts, opened-media notices, story "
                    "views and typing are sent only as chosen here, and each one sent is recorded.")
READ_MEANING = ("Sent from the panel: asks Telegram to show these messages to the other side as read. Telegram decides "
                "when the other side receives it: at once, or only with this account's next message in the chat.")
CONTENT_MEANING = ("Sent from the panel: the other side sees that these one-time media were opened or these voice or "
                   "video messages were played.")
STORY_MEANING = "Sent from the panel: the other side sees that this account viewed its stories up to this ID."
TYPING_MEANING = ("Sent from the panel while the operator typed: the other side sees “typing…”. One record per "
                  "typing burst; repeated notices within the burst are not recorded one by one.")
BEFORE_MEANING = ("Sent from the panel before a message: the other side saw “typing…” for the stated time, then the "
                  "message was sent.")
BURST_MEANING = ("End of a typing burst sent from the panel. Telegram apps show “typing…” for about 6 seconds after "
                 "the last notice.")
PEER_MEANING = ("Typing notices Telegram delivered to this account, joined into one record per burst. Telegram "
                "repeats them every few seconds while the other side types; this is not a record of keystrokes. "
                "The timeline lists the reported actions in order with the times they were received; upload "
                "progress is the percentage the other side's app reported.")


class Fields(BaseModel):
    model_config = ConfigDict(extra="forbid")
    invisible: StrictBool
    read_receipts: Literal[READS]
    content_opened: Literal[MANUAL]
    story_read: Literal[MANUAL]
    typing: Literal[TYPINGS]
    silent_send: Literal[SILENCE]
    offline_after_action: StrictBool
    show_peer_typing: StrictBool
    record_peer_typing: StrictBool


class Override(BaseModel):
    model_config = ConfigDict(extra="forbid")
    read_receipts: Literal[READS] | None = None
    content_opened: Literal[MANUAL] | None = None
    story_read: Literal[MANUAL] | None = None
    typing: Literal[TYPINGS] | None = None
    silent_send: Literal[SILENCE] | None = None
    show_peer_typing: StrictBool | None = None
    record_peer_typing: StrictBool | None = None


class Change(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workspace: Fields | None = None
    chat_id: int | None = None
    secret: StrictBool = False
    override: Override | None = None

    @model_validator(mode="after")
    def complete(self):
        if (self.workspace is None) == (self.chat_id is None):
            raise ValueError("Change either the workspace settings or one chat.")
        if self.workspace is not None and (self.secret or self.override is not None):
            raise ValueError("Workspace settings have no chat override.")
        return self


class Read(BaseModel):
    model_config = ConfigDict(extra="forbid")
    trigger: Literal["manual", "on_open"]
    max_id: int | None = Field(default=None, gt=0)


class SecretRead(BaseModel):
    model_config = ConfigDict(extra="forbid")
    trigger: Literal["manual", "on_open"]


class Contents(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message_ids: list[Annotated[int, Field(gt=0)]] = Field(min_length=1, max_length=100)


class SecretContents(BaseModel):
    model_config = ConfigDict(extra="forbid")
    random_ids: list[Annotated[str, Field(pattern=r"^-?[0-9]{1,20}$")]] = Field(min_length=1, max_length=100)


class Stories(BaseModel):
    model_config = ConfigDict(extra="forbid")
    max_id: int = Field(gt=0, lt=2**31)


def stamp(seconds):
    return datetime.fromtimestamp(seconds, timezone.utc).isoformat(timespec="milliseconds")


def operator_of(operator):
    return {"operator": operator} if operator else {}


def saved(store):
    value = store.get_setting(SETTING, None) or {}
    return {"workspace": dict(value.get("workspace") or {}), "chats": dict(value.get("chats") or {}),
            "secret_chats": dict(value.get("secret_chats") or {}),
            **({"offline_before": bool(value["offline_before"])} if "offline_before" in value else {})}


def choices(store):
    current = saved(store)
    chosen = {**DEFAULTS, **{key: value for key, value in current["workspace"].items()
                             if key in DEFAULTS and key != "offline_after_action"}}
    offline = bool(store.get_setting(OFFLINE, False))
    chosen["offline_after_action"] = current.get("offline_before", offline) if chosen["invisible"] else offline
    return chosen


def override(store, chat_id, secret=False):
    entry = saved(store)["secret_chats" if secret else "chats"].get(str(chat_id)) or {}
    return {key: value for key, value in entry.items() if key in CHAT_FIELDS}


def effective(store, chat_id=None, secret=False):
    fields = choices(store)
    if chat_id is not None:
        fields.update(override(store, chat_id, secret))
    if fields["invisible"]:
        fields.update(FORCED)
    fields["offline_after_action"] = bool(store.get_setting(OFFLINE, False))
    return fields


def preset(fields):
    for name in ("invisible", "visible"):
        if all(fields[key] == value for key, value in PRESETS[name].items()):
            return name
    return "custom"


def ghost(fields):
    return fields["invisible"] or all(fields[key] == value for key, value in FORCED.items())


def silent(store, chat_id=None, secret=False):
    fields = effective(store, chat_id, secret)
    return fields["silent_send"] == "always" or fields["silent_send"] == "while_invisible" and ghost(fields)


def typing_seconds(text):
    low, high = BEFORE_SEND
    return max(low, min(high, round(len((text or "").strip()) / CHARACTERS_PER_SECOND, 1)))


def problem(collector):
    from . import interactions
    try:
        interactions.permitted(collector)
    except (ValueError, RPCError) as exc:
        return str(exc)
    return None


def require(store, chat_id, secret, field, wanted):
    if effective(store, chat_id, secret)[field] != wanted:
        raise ValueError(REFUSED[field])


def mark_key(chat_id, secret=False):
    return ("secret:" if secret else "") + str(chat_id)


def marks(store):
    return store.get_setting(MARKS, None) or {}


def remember(store, key, value):
    store.set_setting(MARKS, {**marks(store), key: value})


def latest(store, chat_id):
    with store.lock:
        row = store.db.execute("SELECT max(message_id) FROM events WHERE chat_id=? AND kind IN (?,?,?)",
                               (chat_id, *SAVED)).fetchone()
    return row[0]


def incoming(store, chat_id, ids):
    with store.lock:
        return {row[0] for row in store.db.execute(
            "SELECT DISTINCT message_id FROM events WHERE chat_id=? AND kind IN (?,?,?) AND message_id IN ("
            + ",".join("?" * len(ids)) + ") AND coalesce(json_extract(payload,'$.outgoing'),0)=0",
            (chat_id, *SAVED, *ids))}


def unopened(store, chat_id):
    opened = set(marks(store).get("opened:" + str(chat_id)) or [])
    with store.lock:
        rows = store.db.execute(
            "SELECT message_id, max(json_extract(payload,'$.sent_at')), max(json_extract(payload,'$.raw.media._')) "
            "FROM events WHERE chat_id=? AND kind IN (?,?,?) AND json_extract(payload,'$.raw.media_unread')=1 "
            "AND coalesce(json_extract(payload,'$.outgoing'),0)=0 GROUP BY message_id ORDER BY message_id DESC LIMIT 60",
            (chat_id, *SAVED)).fetchall()
    return [{"message_id": row[0], "sent_at": row[1], "media": row[2]} for row in rows if row[0] not in opened][:20]


def view(collector):
    store = collector.store
    current, fields = saved(store), effective(store)
    return {"workspace": choices(store), "effective": fields, "preset": preset(fields), "presets": PRESETS,
            "defaults": DEFAULTS, "forced": FORCED, "chat_fields": list(CHAT_FIELDS), "ghost": ghost(fields),
            "overrides": {"chats": current["chats"], "secret_chats": current["secret_chats"]},
            "interaction_problem": problem(collector)}


def chat_view(collector, chat_id, secret=False):
    store = collector.store
    fields = effective(store, chat_id, secret)
    found = {"chat_id": chat_id, "secret": secret, "workspace": choices(store), "override": override(store, chat_id, secret),
             "effective": fields, "preset": preset(fields), "presets": PRESETS, "forced": FORCED, "ghost": ghost(fields),
             "chat_fields": list(CHAT_FIELDS), "silent_now": silent(store, chat_id, secret),
             "typing": of(collector).typing_now(chat_id, secret),
             "last_read": marks(store).get(mark_key(chat_id, secret)),
             "unopened": [] if secret or fields["content_opened"] != "manual" else unopened(store, chat_id),
             "interaction_problem": problem(collector)}
    if secret:
        from . import secret_chats
        found["unopened"] = (secret_chats.of(collector).unopened(chat_id)
                             if fields["content_opened"] == "manual" else [])
    return found


def change(collector, body, operator=None):
    store = collector.store
    with store.transaction():
        current = store.get_setting(SETTING, None) or {}
        if body.workspace is not None:
            before = effective(store)
            values = body.workspace.model_dump()
            offline = values.pop("offline_after_action")
            if values["invisible"]:
                current["offline_before"] = offline
                store.set_setting(OFFLINE, True)
            else:
                current.pop("offline_before", None)
                store.set_setting(OFFLINE, offline)
            current["workspace"] = values
            scope, target, chosen = "workspace", {}, {**values, "offline_after_action": offline}
            store.set_setting(SETTING, current)
            after = effective(store)
        else:
            before = effective(store, body.chat_id, body.secret)
            group = "secret_chats" if body.secret else "chats"
            chosen = body.override.model_dump(exclude_none=True) if body.override else {}
            entries = dict(current.get(group) or {})
            if chosen:
                entries[str(body.chat_id)] = chosen
            else:
                entries.pop(str(body.chat_id), None)
            current[group] = entries
            scope = "secret_chat" if body.secret else "chat"
            target = {"secret_chat_id": body.chat_id} if body.secret else {"chat_id": body.chat_id}
            store.set_setting(SETTING, current)
            after = effective(store, body.chat_id, body.secret)
        store.append("visibility.settings_changed", {
            "scope": scope, **target, "chosen": chosen, "uses_workspace_settings": scope != "workspace" and not chosen,
            "before": before, "after": after, "preset": preset(after), **operator_of(operator),
            "meaning": SETTINGS_MEANING}, body.chat_id if scope == "chat" else None)
    return chat_view(collector, body.chat_id, body.secret) if body.chat_id is not None else view(collector)


async def dispatch(collector, kind, details, call, chat_id=None, permit=None, definite=()):
    from . import interactions
    store = collector.store
    requested = store.append(kind + "_requested", details, chat_id)
    result = {"request_event": requested["seq"], "status": "succeeded"}
    cancelled = False
    try:
        if permit is None:
            await call()
        else:
            with read_permit(*permit):
                await call()
    except FLOOD_ERRORS as exc:
        store.set_setting("rpc_backoff_until", max(time.time() + exc.seconds, store.get_setting("rpc_backoff_until", 0)))
        result.update(status="rejected", error_type=type(exc).__name__, retry_after=exc.seconds)
    except (Exception, asyncio.CancelledError) as exc:
        interactions.note_restriction(store, exc)
        cancelled = isinstance(exc, asyncio.CancelledError)
        sure = isinstance(exc, (ReadReceiptBlocked, *definite)) or isinstance(exc, RPCError) and (exc.code or 500) < 500
        result.update(status="rejected" if sure else "unknown", error_type=type(exc).__name__)
    ids = {key: details[key] for key in ("chat_id", "secret_chat_id", "peer_user_id") if key in details}
    receipt = store.append(kind + "_result", {**ids, **result, "meaning": STATUS[result["status"]]}, chat_id)
    result["result_event"] = receipt["seq"]
    if cancelled:
        raise asyncio.CancelledError
    return result


def sender(collector, request):
    async def call():
        return await collector.client(request)
    return call


def observed(collector, chat_id):
    if not collector.selected(chat_id):
        raise ValueError(NOT_OBSERVED)


async def mark_read(collector, chat_id, trigger, operator=None, max_id=None, cause=None):
    from . import interactions
    store = collector.store
    require(store, chat_id, False, "read_receipts", trigger)
    interactions.permitted(collector)
    observed(collector, chat_id)
    newest = latest(store, chat_id)
    if newest is None:
        raise ValueError("No message of this chat is saved here, so nothing can be marked as read.")
    if max_id is not None and max_id > newest:
        raise ValueError("Only messages saved here can be marked as read.")
    bound, key = max_id or newest, mark_key(chat_id)
    done = marks(store).get(key)
    if isinstance(done, int) and done >= bound:
        return {"status": "unchanged", "chat_id": chat_id, "max_id": done, "trigger": trigger}
    await collector.restore()
    entity = await collector.resolve_target(chat_id)
    if isinstance(entity, types.Channel):
        request = functions.channels.ReadHistoryRequest(utils.get_input_channel(entity), bound)
    else:
        request = functions.messages.ReadHistoryRequest(utils.get_input_peer(entity), bound)
    details = {"chat_id": chat_id, "trigger": trigger, "max_id": bound, "covers": "messages up to this ID",
               "method": request_method(request)["method"], **operator_of(operator), **(cause or {}),
               "meaning": READ_MEANING}
    result = await dispatch(collector, "visibility.read", details, sender(collector, request), chat_id,
                            (type(request), chat_id, bound))
    if result["status"] == "succeeded":
        remember(store, key, bound)
        await opsec.hide_presence(collector, result["request_event"])
    return {**result, "chat_id": chat_id, "max_id": bound, "trigger": trigger}


async def mark_opened(collector, chat_id, message_ids, operator=None):
    from . import interactions
    store = collector.store
    require(store, chat_id, False, "content_opened", "manual")
    interactions.permitted(collector)
    observed(collector, chat_id)
    ids = sorted(set(message_ids))
    if set(ids) - incoming(store, chat_id, ids):
        raise ValueError("Only incoming messages saved here can be marked as opened.")
    await collector.restore()
    entity = await collector.resolve_target(chat_id)
    if isinstance(entity, types.Channel):
        request = functions.channels.ReadMessageContentsRequest(utils.get_input_channel(entity), ids)
        permit = (type(request), chat_id, tuple(ids))
    else:
        request = functions.messages.ReadMessageContentsRequest(ids)
        permit = (type(request), None, tuple(ids))
    details = {"chat_id": chat_id, "trigger": "manual", "message_ids": ids, "method": request_method(request)["method"],
               **operator_of(operator), "meaning": CONTENT_MEANING}
    result = await dispatch(collector, "visibility.contents", details, sender(collector, request), chat_id, permit)
    if result["status"] == "succeeded":
        key = "opened:" + str(chat_id)
        remember(store, key, sorted(set(marks(store).get(key) or []) | set(ids))[-OPENED_LIMIT:])
        await opsec.hide_presence(collector, result["request_event"])
    return {**result, "chat_id": chat_id, "message_ids": ids}


async def mark_stories(collector, chat_id, max_id, operator=None):
    from . import interactions
    store = collector.store
    require(store, chat_id, False, "story_read", "manual")
    interactions.permitted(collector)
    observed(collector, chat_id)
    await collector.restore()
    entity = await collector.resolve_target(chat_id)
    request = functions.stories.ReadStoriesRequest(utils.get_input_peer(entity), max_id)
    details = {"chat_id": chat_id, "trigger": "manual", "max_id": max_id, "covers": "stories up to this ID",
               "method": request_method(request)["method"], **operator_of(operator), "meaning": STORY_MEANING}
    result = await dispatch(collector, "visibility.stories", details, sender(collector, request), chat_id,
                            (type(request), chat_id, max_id))
    if result["status"] == "succeeded":
        await opsec.hide_presence(collector, result["request_event"])
    return {**result, "chat_id": chat_id, "max_id": max_id}


async def send_typing(collector, chat_id, operator=None):
    from . import interactions
    store = collector.store
    require(store, chat_id, False, "typing", "shown")
    interactions.permitted(collector)
    observed(collector, chat_id)
    await collector.restore()
    entity = await collector.resolve_target(chat_id)
    request = functions.messages.SetTypingRequest(utils.get_input_peer(entity), types.SendMessageTypingAction())
    return await of(collector).ping(("chat", chat_id), "visibility.typing",
                                    {"chat_id": chat_id, "mode": "shown", "method": request_method(request)["method"],
                                     **operator_of(operator)}, request, chat_id)


async def before_send(collector, chat_id, entity, text, request_event=None):
    if effective(collector.store, chat_id)["typing"] != "before_send":
        return None
    request = functions.messages.SetTypingRequest(utils.get_input_peer(entity), types.SendMessageTypingAction())
    return await show_typing(collector, "visibility.typing", {
        "chat_id": chat_id, "method": request_method(request)["method"],
        **({"for_request_event": request_event} if request_event else {})}, request, typing_seconds(text), chat_id)


async def show_typing(collector, kind, details, request, seconds, chat_id=None):
    details = {**details, "mode": "before_send", "planned_seconds": seconds, "produced_by": "panel",
               "meaning": BEFORE_MEANING}
    result = await dispatch(collector, kind, details, sender(collector, request), chat_id)
    shown = {"produced_by": "panel", "request_event": result["request_event"], "result_event": result["result_event"],
             "status": result["status"], "planned_seconds": seconds, "seconds": 0, "notices": 0}
    if result["status"] != "succeeded":
        return shown
    started, notices, complete = time.monotonic(), 1, True
    while (left := seconds - (time.monotonic() - started)) > 0:
        await asyncio.sleep(min(left, PING_SECONDS))
        if seconds - (time.monotonic() - started) > 0.5:
            try:
                await collector.client(request)
            except Exception:
                complete = False
                break
            notices += 1
    return {**shown, "seconds": round(time.monotonic() - started, 1), "notices": notices, "complete": complete}


def typing_source(update):
    if isinstance(update, types.UpdateUserTyping):
        return update.user_id, update.user_id
    peer = getattr(update, "from_id", None)
    user = utils.get_peer_id(peer) if peer is not None else None
    if isinstance(update, types.UpdateChatUserTyping):
        return -update.chat_id, user
    return utils.get_peer_id(types.PeerChannel(update.channel_id)), user


def action_details(action):
    try:
        found = vars(action)
    except TypeError:
        return {}
    return {key: value for key, value in found.items() if not key.startswith("_") and type(value) in (int, str)}


def timeline_entry(item):
    progress = item["progress"]
    return {**item["entry"], "first_at": stamp(item["first"]), "last_at": stamp(item["last"]), "updates": item["updates"],
            **({"progress_first": progress[0], "progress_last": progress[1]} if progress else {})}


def heard_update(collector, update):
    from . import secret_chats
    if isinstance(update, types.UpdateEncryptedMessagesRead):
        return secret_chats.of(collector).peer_read(update)
    if isinstance(update, types.UpdateEncryptedChatTyping):
        return secret_chats.of(collector).peer_typing(update.chat_id)
    chat_id, user_id = typing_source(update)
    if user_id is None or not collector.selected(chat_id):
        return None
    return of(collector).peer_typing(chat_id, user_id, update.action, topic=getattr(update, "top_msg_id", None))


class Visibility:
    def __init__(self, collector):
        self.collector = collector
        self.bursts, self.live, self.peers, self.tasks = {}, {}, {}, set()
        self.timer = None
        collector.store.listeners.append(self.heard)

    async def ping(self, key, kind, details, request, chat_id=None, now=None):
        now = time.time() if now is None else now
        self.sweep(now)
        burst = self.bursts.get(key)
        if burst and now - burst["sent"] < PING_SECONDS:
            return {"status": "skipped", "request_event": burst["request_event"],
                    "reason": "a typing notice was sent less than 4 seconds ago"}
        if burst is None:
            result = await dispatch(self.collector, kind, {**details, "meaning": TYPING_MEANING},
                                    sender(self.collector, request), chat_id)
            if result["status"] == "succeeded":
                self.bursts[key] = {"kind": kind, "chat_id": chat_id, "request_event": result["request_event"],
                                    "ids": {name: details[name] for name in ("chat_id", "secret_chat_id", "peer_user_id")
                                            if name in details},
                                    "started": now, "sent": now, "notices": 1}
                self.arm()
                await opsec.hide_presence(self.collector, result["request_event"])
            return result
        burst["sent"] = now
        try:
            await self.collector.client(request)
        except (Exception, asyncio.CancelledError) as exc:
            self.close(key, type(exc).__name__)
            raise
        burst["notices"] += 1
        return {"status": "succeeded", "request_event": burst["request_event"], "coalesced": True}

    def close(self, key, error=None):
        burst = self.bursts.pop(key, None)
        if burst is None:
            return
        self.collector.store.append(burst["kind"] + "_burst", {
            **burst["ids"], "request_event": burst["request_event"], "started_at": stamp(burst["started"]),
            "last_notice_at": stamp(burst["sent"]), "notices": burst["notices"],
            **({"stopped_by_error": error} if error else {}), "meaning": BURST_MEANING}, burst["chat_id"])

    def peer_typing(self, chat_id, user_id, action=None, secret=False, now=None, topic=None):
        now = time.time() if now is None else now
        self.sweep(now)
        fields = effective(self.collector.store, chat_id, secret)
        cancel = type(action).__name__ == "SendMessageCancelAction"
        name = type(action).__name__.removeprefix("SendMessage").removesuffix("Action") if action else "Typing"
        if fields["show_peer_typing"]:
            shown = self.live.setdefault((secret, chat_id), {})
            if cancel:
                shown.pop(user_id, None)
            else:
                shown[user_id] = {"until": now + TYPING_SECONDS, "action": name}
        if fields["record_peer_typing"] and not cancel:
            burst = self.peers.setdefault((secret, chat_id, user_id), {"started": now, "last": now, "updates": 0,
                                                                       "actions": [], "timeline": [], "omitted": 0})
            burst["last"], burst["updates"] = now, burst["updates"] + 1
            if name not in burst["actions"]:
                burst["actions"].append(name)
            self.step(burst, name, action, topic, now)
        self.arm()

    def step(self, burst, name, action, topic, now):
        details = action_details(action) if action is not None else {}
        progress = details.pop("progress", None)
        entry = {"action": name, **({"top_msg_id": topic} if topic is not None else {}),
                 **({"details": details} if details else {})}
        timeline = burst["timeline"]
        same = bool(timeline) and timeline[-1]["entry"] == entry
        if burst["omitted"] or not same and len(timeline) >= TIMELINE_LIMIT:
            burst["omitted"] += 1
            return
        if not same:
            timeline.append({"entry": entry, "first": now, "last": now, "updates": 0, "progress": None})
        latest = timeline[-1]
        latest["last"], latest["updates"] = now, latest["updates"] + 1
        if progress is not None:
            latest["progress"] = [progress if latest["progress"] is None else latest["progress"][0], progress]

    def flush(self, mark):
        secret, chat_id, user_id = mark
        burst = self.peers.pop(mark)
        summary = {"started_at": stamp(burst["started"]), "last_seen_at": stamp(burst["last"]),
                   "updates": burst["updates"], "actions": burst["actions"],
                   "timeline": [timeline_entry(item) for item in burst["timeline"]],
                   **({"timeline_omitted_updates": burst["omitted"]} if burst["omitted"] else {}),
                   "meaning": PEER_MEANING}
        if secret:
            self.collector.store.append("secret_chat.peer_typing", {"secret_chat_id": chat_id, "peer_user_id": user_id,
                                                                    **summary})
        else:
            self.collector.store.append("visibility.peer_typing", {"chat_id": chat_id, "user_id": user_id, **summary},
                                        chat_id, actor_id=user_id)

    def sweep(self, now=None):
        now = time.time() if now is None else now
        for key in [key for key, burst in self.bursts.items() if now - burst["sent"] > BURST_SECONDS]:
            self.close(key)
        for mark in [mark for mark, burst in self.peers.items() if now - burst["last"] > BURST_SECONDS]:
            self.flush(mark)
        for key, shown in list(self.live.items()):
            for user_id in [user_id for user_id, entry in shown.items() if entry["until"] <= now]:
                shown.pop(user_id)
            if not shown:
                self.live.pop(key)

    def arm(self):
        if self.timer is not None:
            return
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        self.timer = loop.call_later(SWEEP_SECONDS, self.tick)

    def tick(self):
        self.timer = None
        try:
            self.sweep()
        except Exception:
            LOG.exception("Typing bursts could not be closed")
        if self.bursts or self.peers or self.live:
            self.arm()

    def typing_now(self, chat_id, secret=False, now=None):
        now = time.time() if now is None else now
        people = getattr(self.collector, "people", None) or {}
        found = []
        for user_id, entry in (self.live.get((secret, chat_id)) or {}).items():
            if entry["until"] > now:
                entity = people.get(user_id)
                found.append({"user_id": user_id, "action": entry["action"],
                              "name": (utils.get_display_name(entity) or None) if entity is not None else None})
        return found

    def heard(self, event):
        if event.get("kind") != "interaction.result" or event.get("chat_id") is None:
            return
        if (event.get("payload") or {}).get("status") != "succeeded":
            return
        if effective(self.collector.store, event["chat_id"])["read_receipts"] != "on_reply":
            return
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return
        self.spawn(self.replied(event))

    async def replied(self, event):
        from . import interactions
        store = self.collector.store
        pending = interactions.requested(store, str(event["payload"].get("request_id") or "")) or {}
        if not pending.get("request_event"):
            return None
        found = store.events_after(pending["request_event"] - 1, 1)
        asked = found[0]["payload"] if found and found[0]["kind"] == "interaction.requested" else {}
        action = (pending.get("request") or {}).get("action")
        if not (action == "send" or action == "press" and (asked.get("button") or {}).get("type") == "text"):
            return None
        try:
            return await mark_read(self.collector, event["chat_id"], "on_reply", asked.get("operator"), cause={
                "after_panel_action": {"action": action, "request_event": pending["request_event"],
                                       "result_event": event["seq"]}})
        except Exception as exc:
            LOG.info("No read receipt after the panel action in chat %s: %s", event["chat_id"], type(exc).__name__)
            return None

    def spawn(self, coroutine):
        task = asyncio.get_running_loop().create_task(coroutine)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return task


def of(collector):
    existing = getattr(collector, "chat_visibility", None)
    if existing is None:
        existing = collector.chat_visibility = Visibility(collector)
    return existing


class Attach:
    def __init__(self, app, owner):
        self.app, self.owner = app, owner

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and (collector := getattr(self.owner.state, "collector", None)) is not None:
            of(collector)
        await self.app(scope, receive, send)


def register(app, authenticate, require_live, operation):
    from fastapi import Depends, HTTPException, Request
    from . import secret_chats

    app.add_middleware(Attach, owner=app)

    def operator(request):
        principal = request.state.principal
        found = {"label": getattr(principal, "label", None) or ("Main administrator" if principal.admin else None),
                 "owner": principal.owner, "admin": bool(principal.admin)}
        return {key: value for key, value in found.items() if value is not None}

    async def secret_call(call, *args):
        collector = app.state.collector
        if not secret_chats.available():
            raise ValueError(secret_chats.UNAVAILABLE)
        if secret_chats.of(collector).manager is None:
            await collector.restore()
        try:
            return await call(*args)
        except secret_chats.library.ChatClosed:
            raise HTTPException(409, "This chat has ended. Nothing more can be sent to it.") from None
        except secret_chats.library.ChatNotReady:
            raise HTTPException(409, "The other side has not accepted this chat yet.") from None

    async def acted(call, *args):
        try:
            return await operation(call, *args)
        except ValueError as exc:
            raise HTTPException(409, str(exc)) from None

    @app.get("/api/visibility", dependencies=[Depends(authenticate)])
    async def visibility_view():
        return view(app.state.collector)

    @app.post("/api/visibility", dependencies=[Depends(authenticate)])
    async def visibility_change(request: Request, body: Change):
        require_live()
        return change(app.state.collector, body, operator(request))

    @app.get("/api/chats/{chat_id}/visibility", dependencies=[Depends(authenticate)])
    async def chat_visibility(chat_id: int):
        return chat_view(app.state.collector, chat_id)

    @app.post("/api/chats/{chat_id}/read", dependencies=[Depends(authenticate)])
    async def chat_read(request: Request, chat_id: int, body: Read):
        require_live()
        return await acted(mark_read, app.state.collector, chat_id, body.trigger, operator(request), body.max_id)

    @app.post("/api/chats/{chat_id}/content-opened", dependencies=[Depends(authenticate)])
    async def chat_contents(request: Request, chat_id: int, body: Contents):
        require_live()
        return await acted(mark_opened, app.state.collector, chat_id, body.message_ids, operator(request))

    @app.post("/api/chats/{chat_id}/story-read", dependencies=[Depends(authenticate)])
    async def chat_stories(request: Request, chat_id: int, body: Stories):
        require_live()
        return await acted(mark_stories, app.state.collector, chat_id, body.max_id, operator(request))

    @app.post("/api/chats/{chat_id}/typing", dependencies=[Depends(authenticate)])
    async def chat_typing(request: Request, chat_id: int):
        require_live()
        return await acted(send_typing, app.state.collector, chat_id, operator(request))

    @app.get("/api/secret-chats/{chat_id}/visibility", dependencies=[Depends(authenticate)])
    async def secret_visibility(chat_id: int):
        return chat_view(app.state.collector, chat_id, True)

    @app.post("/api/secret-chats/{chat_id}/read", dependencies=[Depends(authenticate)])
    async def secret_read(request: Request, chat_id: int, body: SecretRead):
        require_live()
        chats = secret_chats.of(app.state.collector)
        return await acted(secret_call, chats.mark_read, chat_id, body.trigger, operator(request))

    @app.post("/api/secret-chats/{chat_id}/content-opened", dependencies=[Depends(authenticate)])
    async def secret_contents(request: Request, chat_id: int, body: SecretContents):
        require_live()
        chats = secret_chats.of(app.state.collector)
        return await acted(secret_call, chats.mark_opened, chat_id, [int(value) for value in body.random_ids],
                           operator(request))

    @app.post("/api/secret-chats/{chat_id}/typing", dependencies=[Depends(authenticate)])
    async def secret_typing(request: Request, chat_id: int):
        require_live()
        chats = secret_chats.of(app.state.collector)
        return await acted(secret_call, chats.send_typing, chat_id, operator(request))
