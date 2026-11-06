import asyncio
import copy
import time
from contextvars import ContextVar

from telethon import TelegramClient, utils
from telethon.errors import FloodWaitError, FloodPremiumWaitError
from telethon.network.connection import ConnectionTcpObfuscated
from telethon.network.connection.tcpmtproxy import TcpMTProxy
from telethon.tl import functions, types

_single_attempt = ContextVar("telegram_single_attempt", default=False)
FLOOD_ERRORS = (FloodWaitError, FloodPremiumWaitError)
_ACTIONS = (functions.messages.GetBotCallbackAnswerRequest,
            functions.messages.ImportChatInviteRequest, functions.channels.JoinChannelRequest,
            functions.auth.AcceptLoginTokenRequest)


def request_method(request):
    """Only TL method names: never serialize request arguments or error text."""
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

    def rpc_activity(self):
        # These count client calls, not packets or Telethon's internal retries.
        return copy.deepcopy(getattr(self, "_rpc_activity", None))

    async def connect(self):
        from .client_identity import apply_init_params
        apply_init_params(self)
        return await super().connect()


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
        # One outgoing RPC at a time for this authorization, including callers
        # in monitoring's background loops. Resolving a peer may re-enter _call
        # in the same task; that is sequential and must not deadlock.
        if not hasattr(self, "_rpc_lock"):
            self._rpc_lock = asyncio.Lock()
            self._rpc_owner = None
            self._rpc_wait_until = 0
        current = asyncio.current_task()
        if self._rpc_owner is current:
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
            counts["ok"] += 1
            return result
        except asyncio.CancelledError:
            counts["cancelled"] += 1
            raise
        except Exception as exc:
            counts["errors"] += 1
            if isinstance(exc, FLOOD_ERRORS):
                counts["flood_waits"] += 1
                self._rpc_wait_until = max(self._rpc_wait_until,
                    getattr(self, "rpc_backoff_getter", lambda: 0)(), time.time() + exc.seconds + 1)
                if save := getattr(self, "rpc_backoff_setter", None):
                    save(self._rpc_wait_until)
                if observe := getattr(self, "rpc_backoff_observer", None):
                    failed = getattr(exc, "request", None)
                    observe({**info, "failed_method": request_method(failed)["method"] if failed is not None else info["method"],
                             "error_type": type(exc).__name__, "retry_after_seconds": exc.seconds,
                             "wait_until": self._rpc_wait_until, "observed_at": time.time(),
                             "activity": self.rpc_activity()})
            if handler := getattr(self, "rpc_error_handler", None):
                handler(exc)
            raise
        finally:
            _single_attempt.reset(token)
