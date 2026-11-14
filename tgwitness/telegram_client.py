import asyncio
import copy
import logging
import time
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime

from telethon import TelegramClient, utils
from telethon.errors import (AuthKeyDuplicatedError, AuthKeyInvalidError, AuthKeyUnregisteredError,
                             FloodPremiumWaitError, FloodWaitError, SessionExpiredError, SessionRevokedError)
from telethon.network.connection import ConnectionTcpObfuscated
from telethon.network.connection.tcpmtproxy import TcpMTProxy
from telethon.tl import functions, types
from telethon.tl.tlobject import TLRequest

from .rpc_pacing import bulk_request

_single_attempt = ContextVar("telegram_single_attempt", default=False)
_read_permit = ContextVar("telegram_read_permit", default=None)
LOG = logging.getLogger("tgwitness.telegram_client")

try:
    from telethon._updates.messagebox import ENTRY_ACCOUNT, ENTRY_SECRET, MessageBox, PrematureEndReason, PtsInfo
except ImportError:
    MessageBox = None


if MessageBox is not None:
    class GapAwareMessageBox(MessageBox):
        __slots__ = ("gap_owner", "diffing", "diff_types")

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.diffing, self.diff_types = None, {}

        def session_state(self):
            held = getattr(getattr(self, "gap_owner", None), "accepted_state", None)
            return held or super().session_state()

        def hold(self):
            owner = getattr(self, "gap_owner", None)
            if owner is not None and owner.accepted_state is None:
                owner.accepted_state = MessageBox.session_state(self)

        def load(self, session_state, channel_states):
            super().load(session_state, channel_states)
            if (owner := getattr(self, "gap_owner", None)) is not None:
                owner.accepted_state, owner.undispatched = None, 0

        def process_updates(self, updates, chat_hashes, result):
            self.hold()
            return super().process_updates(updates, chat_hashes, result)

        def apply_pts_info(self, update, *, reset_deadlines):
            if isinstance(update, types.UpdateChannelTooLong):
                self.report_sequence("event", update.channel_id, "channel_too_long",
                                     getattr(self.map.get(update.channel_id), "pts", None), update.pts)
                return super().apply_pts_info(update, reset_deadlines=reset_deadlines)
            info = PtsInfo.from_update(update)
            if info is None or info.entry is ENTRY_SECRET:
                return super().apply_pts_info(update, reset_deadlines=reset_deadlines)
            if self.diffing is not None and info.entry == self.diffing:
                name = type(update).__name__
                self.diff_types[name] = self.diff_types.get(name, 0) + 1
                update.tgwitness_recovered = True
                return update
            known = info.entry in self.map
            result = super().apply_pts_info(update, reset_deadlines=reset_deadlines)
            if result is not None:
                method = "push" if self.diffing is None else "getDifference"
                self.report_sequence("update", info.entry, info.pts, info.pts_count, type(update).__name__, known,
                                     method)
            return result

        def applying(self, entry, call, *args):
            self.diffing, self.diff_types = entry, {}
            try:
                return call(*args)
            finally:
                self.diffing = None

        def apply_difference(self, diff, chat_hashes):
            self.hold()
            before = getattr(self.map.get(ENTRY_ACCOUNT), "pts", None)
            if isinstance(diff, types.updates.DifferenceTooLong):
                self.report_gap(None, ENTRY_ACCOUNT, diff.pts)
            result = self.applying(ENTRY_ACCOUNT, super().apply_difference, diff, chat_hashes)
            if before is not None and not isinstance(diff, types.updates.DifferenceTooLong):
                state = getattr(diff, "intermediate_state", None) or getattr(diff, "state", None)
                counted = dict(self.diff_types)
                if getattr(diff, "new_messages", None):
                    counted["UpdateNewMessage"] = counted.get("UpdateNewMessage", 0) + len(diff.new_messages)
                self.report_sequence("difference", ENTRY_ACCOUNT, before, state.pts if state else before,
                                     "getDifference", type(diff).__name__,
                                     not isinstance(diff, types.updates.DifferenceSlice), counted)
            return result

        def apply_channel_difference(self, request, diff, chat_hashes):
            self.hold()
            entry = request.channel.channel_id
            if isinstance(diff, types.updates.ChannelDifferenceTooLong):
                self.report_gap(entry, entry, getattr(diff.dialog, "pts", None))
            result = self.applying(entry, super().apply_channel_difference, request, diff, chat_hashes)
            if not isinstance(diff, types.updates.ChannelDifferenceTooLong):
                counted = dict(self.diff_types)
                if getattr(diff, "new_messages", None):
                    counted["UpdateNewChannelMessage"] = (counted.get("UpdateNewChannelMessage", 0)
                                                          + len(diff.new_messages))
                self.report_sequence("difference", entry, request.pts, diff.pts, "getChannelDifference",
                                     type(diff).__name__, bool(diff.final), counted)
            return result

        def end_difference(self):
            self.report_sequence("event", ENTRY_ACCOUNT, "difference_failed",
                                 getattr(self.map.get(ENTRY_ACCOUNT), "pts", None), None)
            return super().end_difference()

        def get_channel_difference(self, chat_hashes):
            entry = next((id for id in self.getting_diff_for if isinstance(id, int)), None)
            pts = getattr(self.map.get(entry), "pts", None)
            request = super().get_channel_difference(chat_hashes)
            if entry is not None and request is None and entry not in self.map:
                self.report_sequence("dropped", entry, "no_access_hash", pts)
            return request

        def end_channel_difference(self, request, reason, chat_hashes):
            entry = request.channel.channel_id
            pts = getattr(self.map.get(entry), "pts", None)
            result = super().end_channel_difference(request, reason, chat_hashes)
            if reason == PrematureEndReason.BANNED:
                self.report_sequence("dropped", entry, "banned", pts)
            else:
                self.report_sequence("event", entry, "difference_failed", pts, None)
            return result

        def report_sequence(self, *report):
            listener = getattr(getattr(self, "gap_owner", None), "sequence_listener", None)
            if listener is not None:
                try:
                    listener(*report)
                except Exception:
                    LOG.exception("Recording the update sequence failed")

        def report_gap(self, channel_id, entry, after):
            owner = getattr(self, "gap_owner", None)
            if owner is not None:
                owner.difference_gap(channel_id, getattr(self.map.get(entry), "pts", None), after)
else:
    GapAwareMessageBox = None
FLOOD_ERRORS = (FloodWaitError, FloodPremiumWaitError)
EXPORTED_AUTHORIZATION_ERRORS = (AuthKeyDuplicatedError, AuthKeyInvalidError, AuthKeyUnregisteredError,
                                 SessionExpiredError, SessionRevokedError)
_ACTIONS = (functions.messages.GetBotCallbackAnswerRequest,
            functions.messages.ImportChatInviteRequest, functions.channels.JoinChannelRequest,
            functions.auth.AcceptLoginTokenRequest)
_READ_RECEIPTS = (functions.messages.ReadHistoryRequest, functions.messages.ReadMessageContentsRequest,
                  functions.channels.ReadHistoryRequest, functions.channels.ReadMessageContentsRequest,
                  functions.messages.ReadDiscussionRequest, functions.messages.ReadMentionsRequest,
                  functions.messages.ReadReactionsRequest, functions.messages.ReadEncryptedHistoryRequest,
                  functions.stories.ReadStoriesRequest, functions.stories.IncrementStoryViewsRequest)
_OWN_UPDATES = (types.messages.AffectedMessages, types.messages.AffectedHistory, types.messages.AffectedFoundMessages)
_FILE_READS = (functions.upload.GetFileRequest, functions.upload.GetCdnFileRequest)
FILE_REQUESTS = 3


def file_request(request):
    for _ in range(8):
        if isinstance(request, _FILE_READS):
            return True
        request = getattr(request, "query", None)
        if not isinstance(request, TLRequest):
            return False
    return False


def method_name(request):
    while isinstance(getattr(request, "query", None), TLRequest):
        request = request.query
    name = type(request).__name__.removesuffix("Request")
    group = type(request).__module__.rpartition(".")[2]
    return ("" if group == "functions" else group + ".") + name[:1].lower() + name[1:]


class ReadReceiptBlocked(ValueError):
    pass


def _peer_key(peer):
    try:
        return utils.get_peer_id(peer)
    except (TypeError, ValueError):
        return None


def _channel_key(channel):
    channel_id = getattr(channel, "channel_id", None)
    return utils.get_peer_id(types.PeerChannel(channel_id)) if type(channel_id) is int else None


def _moment(value):
    return int(value.timestamp()) if isinstance(value, datetime) else value


PERMITTED_READS = {
    functions.messages.ReadHistoryRequest: lambda r: (_peer_key(r.peer), r.max_id),
    functions.channels.ReadHistoryRequest: lambda r: (_channel_key(r.channel), r.max_id),
    functions.messages.ReadMessageContentsRequest: lambda r: (None, tuple(r.id or ())),
    functions.channels.ReadMessageContentsRequest: lambda r: (_channel_key(r.channel), tuple(r.id or ())),
    functions.messages.ReadEncryptedHistoryRequest: lambda r: (getattr(r.peer, "chat_id", None), _moment(r.max_date)),
    functions.stories.ReadStoriesRequest: lambda r: (_peer_key(r.peer), r.max_id),
}


class ReadPermit:
    def __init__(self, request_type, chat_id, bound):
        if request_type not in PERMITTED_READS or bound is None or bound == ():
            raise ValueError("This read request cannot be permitted.")
        self.request_type, self.key, self.open = request_type, (chat_id, bound), True

    def admits(self, request):
        if not self.open or type(request) is not self.request_type:
            return False
        try:
            return PERMITTED_READS[self.request_type](request) == self.key
        except Exception:
            return False


@contextmanager
def read_permit(request_type, chat_id, bound):
    permit = ReadPermit(request_type, chat_id, bound)
    token = _read_permit.set(permit)
    try:
        yield permit
    finally:
        permit.open = False
        _read_permit.reset(token)


def reject_read_receipts(request, permit=None):
    if permit is not None and permit.admits(request):
        permit.open = False
        return
    pending = [request]
    while pending:
        item = pending.pop()
        if utils.is_list_like(item):
            pending.extend(item)
        elif isinstance(item, _READ_RECEIPTS):
            raise ReadReceiptBlocked("Read receipts are disabled in the TgWitness API collector.")
        elif (query := getattr(item, "query", None)) is not None:
            pending.append(query)


def request_method(request):
    wrappers = (functions.InvokeWithTakeoutRequest, functions.InvokeWithMessagesRangeRequest,
                functions.InvokeWithLayerRequest, functions.InitConnectionRequest)
    names = []
    for _ in range(8):
        cls = type(request)
        prefix = "telethon.tl.functions"
        if cls.__module__ != prefix and not cls.__module__.startswith(prefix + "."):
            names.append("unknown")
            break
        namespace = cls.__module__[len(prefix):].strip(".")
        name = cls.__name__.removesuffix("Request")
        names.append((namespace + "." if namespace else "") + name[:1].lower() + name[1:])
        if not isinstance(request, wrappers):
            break
        request = request.query
    return {"method": names[-1], "wrappers": names[:-1]}


class WitnessClient(TelegramClient):

    def __init__(self, *args, **kwargs):
        self.accepted_state, self.undispatched = None, 0
        super().__init__(*args, **kwargs)
        if GapAwareMessageBox is not None:
            box = GapAwareMessageBox(self._log["messagebox"])
            box.gap_owner = self
            self._message_box = box

    async def _preprocess_updates(self, updates, users, chats):
        result = await super()._preprocess_updates(updates, users, chats)
        self.undispatched += len(result)
        if not self.undispatched:
            self.accepted_state = None
        return result

    async def _dispatch_update(self, update):
        await super()._dispatch_update(update)
        self.undispatched = max(0, self.undispatched - 1)
        if not self.undispatched:
            self.accepted_state = None

    def difference_gap(self, channel_id, before, after):
        if listener := getattr(self, "difference_gap_listener", None):
            try:
                listener(channel_id, before, after)
            except Exception:
                LOG.exception("Recording an undelivered update interval failed")

    async def history_page(self, entity, *, limit, offset_id):
        peer = await self.get_input_entity(entity)
        result = await self(functions.messages.GetHistoryRequest(peer, offset_id, None, 0, limit, 0, 0, 0))
        entities = {utils.get_peer_id(item): item for item in [*result.users, *result.chats]}
        for message in result.messages:
            if isinstance(message, (types.Message, types.MessageService)):
                message._finish_init(self, entities, peer)
        return result.messages

    def rpc_activity(self):
        return copy.deepcopy(getattr(self, "_rpc_activity", None))

    async def connect(self):
        from .client_identity import apply_init_params
        apply_init_params(self)
        self._connection_cleanup_pending = True
        result = await super().connect()
        if listener := getattr(self, "connection_listener", None):
            listener("opened")
        return result

    async def _disconnect_coro(self):
        pending = self.is_connected() or getattr(self, "_connection_cleanup_pending", False)
        try:
            return await super()._disconnect_coro()
        finally:
            if pending and not self.is_connected():
                self._connection_cleanup_pending = False
                if listener := getattr(self, "connection_listener", None):
                    listener("closed")

    async def _handle_auto_reconnect(self):
        await super()._handle_auto_reconnect()
        if listener := getattr(self, "connection_listener", None):
            listener("reconnected")

    @property
    def _request_retries(self):
        return 0 if _single_attempt.get() else self._read_retries

    @_request_retries.setter
    def _request_retries(self, value):
        self._read_retries = value

    async def switch_route(self, options):
        await self.disconnect()
        self._connection = options.get("connection", ConnectionTcpObfuscated)
        self._proxy = options.get("proxy")
        self._init_request.proxy = (types.InputClientProxy(*self._connection.address_info(self._proxy))
                                    if issubclass(self._connection, TcpMTProxy) else None)

    async def _call(self, sender, request, ordered=False, flood_sleep_threshold=None):
        if utils.is_list_like(request):
            request = tuple(request)
        reject_read_receipts(request, _read_permit.get())
        if not hasattr(self, "_rpc_lock"):
            self._rpc_lock = asyncio.Lock()
            self._rpc_owner = None
            self._rpc_wait_until = 0
            self._file_slots = asyncio.Semaphore(FILE_REQUESTS)
        current = asyncio.current_task()
        if self._rpc_owner is current:
            return await self._serial_call(sender, request, ordered, flood_sleep_threshold)
        if not utils.is_list_like(request) and file_request(request):
            async with self._file_slots:
                return await self._serial_call(sender, request, ordered, flood_sleep_threshold)
        async with self._rpc_lock:
            self._rpc_owner = current
            try:
                return await self._serial_call(sender, request, ordered, flood_sleep_threshold)
            finally:
                self._rpc_owner = None

    async def _serial_call(self, sender, request, ordered, flood_sleep_threshold):
        if utils.is_list_like(request):
            return [await self._serial_call(sender, item, ordered, flood_sleep_threshold) for item in request]
        while True:
            stored = getattr(self, "rpc_backoff_getter", lambda: 0)()
            remaining = max(self._rpc_wait_until, stored) - time.time()
            if remaining <= 0:
                break
            await asyncio.sleep(min(remaining, 1))
        single = isinstance(request, _ACTIONS)
        pacer = getattr(self, "bulk_pacer", None)
        paced = pacer is not None and bulk_request(request)
        if paced:
            await pacer.before()
        token = _single_attempt.set(single)
        info = request_method(request)
        if not hasattr(self, "_rpc_activity"):
            self._rpc_activity = {"since": time.time(), "methods": {}}
        key = "/".join([*info["wrappers"], info["method"]])
        counts = self._rpc_activity["methods"].setdefault(key,
            {"calls": 0, "ok": 0, "errors": 0, "cancelled": 0, "flood_waits": 0})
        counts["calls"] += 1
        try:
            result = await super()._call(sender, request, ordered, flood_sleep_threshold)
            if paced:
                pacer.success()
            counts["ok"] += 1
            if (isinstance(result, _OWN_UPDATES) or getattr(result, "SUBCLASS_OF_ID", None) == types.Updates.SUBCLASS_OF_ID) \
                    and (listener := getattr(self, "updates_listener", None)):
                listener()
            return result
        except asyncio.CancelledError:
            counts["cancelled"] += 1
            raise
        except Exception as exc:
            counts["errors"] += 1
            if isinstance(exc, FLOOD_ERRORS):
                if pacer is not None:
                    pacer.flooded(exc.seconds)
                counts["flood_waits"] += 1
                self._rpc_wait_until = max(self._rpc_wait_until,
                    getattr(self, "rpc_backoff_getter", lambda: 0)(), time.time() + exc.seconds + 1)
                if save := getattr(self, "rpc_backoff_setter", None):
                    save(self._rpc_wait_until, method_name(request))
                if observe := getattr(self, "rpc_backoff_observer", None):
                    failed = getattr(exc, "request", None)
                    observe({**info, "failed_method": request_method(failed)["method"] if failed is not None else info["method"],
                             "error_type": type(exc).__name__, "retry_after_seconds": exc.seconds,
                             "wait_until": self._rpc_wait_until, "observed_at": time.time(),
                             "activity": self.rpc_activity()})
            if sender is not None and sender is not self._sender and isinstance(exc, EXPORTED_AUTHORIZATION_ERRORS):
                self.exported_authorization_failed(sender, exc)
            elif handler := getattr(self, "rpc_error_handler", None):
                handler(exc)
            raise
        finally:
            _single_attempt.reset(token)

    def exported_authorization_failed(self, sender, exc):
        dc_id = getattr(sender, "dc_id", None)
        if not hasattr(self, "_stale_exports"):
            self._stale_exports = set()
        self._stale_exports.add(dc_id)
        if listener := getattr(self, "exported_error_handler", None):
            try:
                listener(exc, dc_id)
            except Exception:
                LOG.exception("Recording an ended file data-center authorization failed")

    async def _return_exported_sender(self, sender):
        await super()._return_exported_sender(sender)
        dc_id = getattr(sender, "dc_id", None)
        if dc_id not in getattr(self, "_stale_exports", ()):
            return
        async with self._borrow_sender_lock:
            state, current = self._borrowed_senders.get(dc_id, (None, None))
            if current is not sender or state is None or state._n:
                return
            del self._borrowed_senders[dc_id]
            self._stale_exports.discard(dc_id)
        await sender.disconnect()
