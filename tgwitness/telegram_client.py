import asyncio
import copy
import logging
import math
import time
from contextvars import ContextVar

from telethon import TelegramClient, utils
from telethon.errors import (AuthKeyDuplicatedError, AuthKeyInvalidError, AuthKeyUnregisteredError,
                             FloodPremiumWaitError, FloodWaitError, SessionExpiredError, SessionRevokedError)
from telethon.network.connection import ConnectionTcpObfuscated
from telethon.network.connection.tcpmtproxy import TcpMTProxy
from telethon.tl import functions, types
from telethon.tl.tlobject import TLRequest

from .rpc_pacing import bulk_request

_single_attempt = ContextVar("telegram_single_attempt", default=False)
LOG = logging.getLogger("tgwitness.telegram_client")

try:
    from telethon._updates.messagebox import ENTRY_ACCOUNT, MessageBox, PrematureEndReason
except ImportError:
    MessageBox = None

TOO_LONG_RECOVERY = "channel_difference_too_long"


if MessageBox is not None:
    class GapAwareMessageBox(MessageBox):
        __slots__ = ("gap_owner",)

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

        def apply_difference(self, diff, chat_hashes):
            self.hold()
            if isinstance(diff, types.updates.DifferenceTooLong):
                self.report_gap(None, ENTRY_ACCOUNT, diff.pts)
            return super().apply_difference(diff, chat_hashes)

        def apply_channel_difference(self, request, diff, chat_hashes):
            self.hold()
            if not isinstance(diff, types.updates.ChannelDifferenceTooLong):
                return super().apply_channel_difference(request, diff, chat_hashes)
            entry = request.channel.channel_id
            before, after = getattr(self.map.get(entry), "pts", None), getattr(diff.dialog, "pts", None)
            if type(before) is int and type(after) is int and after <= before:
                diff.dialog.pts = after = before + 1
            latest = sorted((m for m in diff.messages if isinstance(m, (types.Message, types.MessageService))),
                            key=lambda m: m.id)
            self.report_gap(entry, entry, after, top_message=getattr(diff.dialog, "top_message", None),
                            recovered=len(latest))
            super().apply_channel_difference(request, diff, chat_hashes)
            updates = []
            for message in latest:
                update = types.UpdateNewChannelMessage(message=message, pts=0, pts_count=0)
                update.tgwitness_recovery = TOO_LONG_RECOVERY
                updates.append(update)
            return updates, diff.users, diff.chats

        def get_channel_difference(self, chat_hashes):
            entry = next((id for id in self.getting_diff_for if isinstance(id, int)), None)
            before = getattr(self.map.get(entry), "pts", None)
            request = super().get_channel_difference(chat_hashes)
            if request is None and entry is not None and before is not None and entry not in self.map:
                self.report_gap(entry, None, None, before=before, cause="channel_state_dropped")
            return request

        def end_channel_difference(self, request, reason, chat_hashes):
            super().end_channel_difference(request, reason, chat_hashes)
            owner = getattr(self, "gap_owner", None)
            if reason == PrematureEndReason.BANNED and owner is not None:
                owner.channel_unavailable(request.channel.channel_id)

        def report_gap(self, channel_id, entry, after, *, before=None, **details):
            owner = getattr(self, "gap_owner", None)
            if owner is not None:
                if entry is not None:
                    before = getattr(self.map.get(entry), "pts", None)
                owner.difference_gap(channel_id, before, after, **details)
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
                  functions.stories.ReadStoriesRequest)
_OWN_UPDATES = (types.messages.AffectedMessages, types.messages.AffectedHistory, types.messages.AffectedFoundMessages)
_FILE_READS = (functions.upload.GetFileRequest, functions.upload.GetCdnFileRequest)
_UPDATE_READS = (functions.updates.GetDifferenceRequest, functions.updates.GetChannelDifferenceRequest,
                 functions.updates.GetStateRequest)
FILE_REQUESTS = 3


def _wraps(request, kinds):
    for _ in range(8):
        if isinstance(request, kinds):
            return True
        request = getattr(request, "query", None)
        if not isinstance(request, TLRequest):
            return False
    return False


def file_request(request):
    return _wraps(request, _FILE_READS)


def update_request(request):
    return _wraps(request, _UPDATE_READS)


def flood_key(request, dc_id=None):
    name = request_method(request)["method"]
    return name + "@dc" + str(dc_id or 0) if file_request(request) else name


def method_name(request):
    while isinstance(getattr(request, "query", None), TLRequest):
        request = request.query
    name = type(request).__name__.removesuffix("Request")
    group = type(request).__module__.rpartition(".")[2]
    return ("" if group == "functions" else group + ".") + name[:1].lower() + name[1:]


class ReadReceiptBlocked(ValueError):
    pass


def reject_read_receipts(request):
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

    def difference_gap(self, channel_id, before, after, **details):
        if listener := getattr(self, "difference_gap_listener", None):
            try:
                listener(channel_id, before, after, **details)
            except Exception:
                LOG.exception("Recording an undelivered update interval failed")

    def channel_unavailable(self, channel_id):
        if listener := getattr(self, "channel_unavailable_listener", None):
            try:
                listener(channel_id)
            except Exception:
                LOG.exception("Recording a channel that stopped returning updates failed")

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

    def _flood_key(self, request, sender=None):
        return flood_key(request, getattr(sender, "dc_id", None) or getattr(getattr(self, "session", None), "dc_id", None))

    def flood_until(self, key):
        getter = getattr(self, "flood_getter", None)
        saved = getter() if getter else None
        saved = saved.get(key, 0) if isinstance(saved, dict) else 0
        return max(getattr(self, "_flood_until", {}).get(key, 0), saved if isinstance(saved, (int, float)) else 0)

    async def _flood_turn(self, sender, items):
        for item in items:
            if update_request(item):
                continue
            remaining = self.flood_until(self._flood_key(item, sender)) - time.time()
            if remaining > 3:
                raise FloodWaitError(request=item, capture=math.ceil(remaining))
            if remaining > 0:
                await asyncio.sleep(remaining)

    async def _paced_turn(self, items):
        pacer = getattr(self, "bulk_pacer", None)
        for item in items:
            if pacer is not None and bulk_request(item):
                await pacer.before()

    async def _call(self, sender, request, ordered=False, flood_sleep_threshold=None):
        if utils.is_list_like(request):
            request = tuple(request)
        reject_read_receipts(request)
        if not hasattr(self, "_rpc_lock"):
            self._rpc_lock = asyncio.Lock()
            self._bulk_lock = asyncio.Lock()
            self._rpc_owner = None
            self._flood_until = getattr(self, "_flood_until", {})
            self._file_slots = asyncio.Semaphore(FILE_REQUESTS)
        items = request if utils.is_list_like(request) else (request,)
        await self._flood_turn(sender, items)
        if self._rpc_owner is asyncio.current_task():
            await self._paced_turn(items)
            return await self._serial_call(sender, request, ordered, flood_sleep_threshold)
        if getattr(self, "bulk_pacer", None) is not None and any(bulk_request(item) for item in items):
            async with self._bulk_lock:
                await self._paced_turn(items)
                return await self._turn_call(sender, request, ordered, flood_sleep_threshold)
        return await self._turn_call(sender, request, ordered, flood_sleep_threshold)

    async def _turn_call(self, sender, request, ordered, flood_sleep_threshold):
        if not utils.is_list_like(request) and update_request(request):
            return await self._serial_call(sender, request, ordered, flood_sleep_threshold)
        if not utils.is_list_like(request) and file_request(request):
            async with self._file_slots:
                return await self._serial_call(sender, request, ordered, flood_sleep_threshold)
        async with self._rpc_lock:
            self._rpc_owner = asyncio.current_task()
            try:
                return await self._serial_call(sender, request, ordered, flood_sleep_threshold)
            finally:
                self._rpc_owner = None

    async def _serial_call(self, sender, request, ordered, flood_sleep_threshold):
        if utils.is_list_like(request):
            return [await self._serial_call(sender, item, ordered, flood_sleep_threshold) for item in request]
        single = isinstance(request, _ACTIONS)
        pacer = getattr(self, "bulk_pacer", None)
        paced = pacer is not None and bulk_request(request)
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
                flood = self._flood_key(request, sender)
                until = self._flood_until[flood] = max(self.flood_until(flood), time.time() + exc.seconds + 1)
                if save := getattr(self, "rpc_backoff_setter", None):
                    save(until, flood)
                if observe := getattr(self, "rpc_backoff_observer", None):
                    failed = getattr(exc, "request", None)
                    observe({**info, "failed_method": request_method(failed)["method"] if failed is not None else info["method"],
                             "flood_key": flood, "error_type": type(exc).__name__, "retry_after_seconds": exc.seconds,
                             "wait_until": until, "observed_at": time.time(),
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
