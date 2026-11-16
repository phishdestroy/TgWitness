import asyncio
import copy
import inspect
import io
import math
import pathlib
import time

from telethon import errors, functions, helpers, types, utils
from telethon.crypto import AuthKey
from telethon.network import MTProtoSender
from telethon.tl.alltlobjects import LAYER

from .burst import HANDSHAKES

PER_SESSION = 4
DEFAULT_SESSIONS = 4
MAX_SESSIONS = 8
PART = 512 * 1024
GROW_AFTER = .25
FLOOD_COOLDOWN = 60
OPEN_RETRY = 5
ROUTE_RETRY = 60
SESSION_IDLE = 60
POOL_IDLE = 120
REAP_EVERY = 10
PART_ATTEMPTS = 4
PART_FLOOD_PATIENCE = 30
VALID_PARTS = frozenset(4096 << shift for shift in range(9))
FLOODS = (errors.FloodWaitError, errors.FloodPremiumWaitError)
TRANSIENT = (TimeoutError, ConnectionError, OSError, errors.TimedOutError, errors.ServerError)
MEANING = ("Files are read over their own connections to each Telegram data center, separate from the connection that "
           "reads messages. Their number grows from one while files queue up and shrinks when Telegram asks to slow "
           "down. If a dedicated media endpoint is unavailable or its connection fails, file reads use the standard "
           "connection. Dedicated connections are retried in the background after one minute.")


class MediaRouteUnavailable(ValueError):
    pass


class _Session:
    __slots__ = ("sender", "busy", "used", "broken", "parts", "bytes", "opened", "init_lock")

    def __init__(self, sender, now):
        self.sender, self.busy, self.used, self.broken = sender, 0, now, False
        self.parts = self.bytes = 0
        self.opened = now
        self.init_lock = asyncio.Lock()


class _Dc:
    def __init__(self, dc_id, home):
        self.dc_id, self.home = dc_id, home
        self.sessions, self.opening, self.target, self.waiters = [], 0, 1, 0
        self.changed = self.flooded = self.error_at = -math.inf
        self.error = self.auth_key = None
        self.event = asyncio.Event()
        self.key_lock = asyncio.Lock()
        self.stats = {"parts": 0, "bytes": 0, "floods": 0, "failures": 0, "opened": 0, "closed": 0}

    def live(self):
        return [session for session in self.sessions if not session.broken]


class MediaConnectionPool:
    def __init__(self, client, *, maximum=None, per_session=PER_SESSION, clock=time.monotonic, opener=None):
        self.client, self.maximum, self.per_session, self.clock = client, maximum, per_session, clock
        self.opener = opener or self.open_sender
        self.dcs, self.tasks, self.openers, self.reaper = {}, set(), set(), None
        self.configured, self.read_at = DEFAULT_SESSIONS, -math.inf

    def setting(self):
        now = self.clock()
        if now - self.read_at >= 5:
            self.read_at = now
            try:
                value = self.maximum() if callable(self.maximum) else self.maximum
                self.configured = DEFAULT_SESSIONS if value is None else max(0, min(MAX_SESSIONS, int(value)))
            except (TypeError, ValueError):
                self.configured = DEFAULT_SESSIONS
        return self.configured

    def enabled(self):
        return self.setting() > 0

    def limit(self):
        return max(1, self.setting())

    def home(self):
        return getattr(getattr(self.client, "session", None), "dc_id", None)

    def dc(self, dc_id):
        home = self.home()
        dc_id = dc_id or home
        dc = self.dcs.get(dc_id)
        if dc is not None and dc.home != (dc_id == home):
            self.retire(dc)
            dc = None
        if dc is None:
            dc = self.dcs[dc_id] = _Dc(dc_id, dc_id == home)
        return dc

    def window(self, dc_id):
        dc = self.dc(dc_id)
        return min(self.limit(), dc.target + 1) * self.per_session

    @staticmethod
    def poke(dc):
        event, dc.event = dc.event, asyncio.Event()
        event.set()

    def spawn(self, dc):
        dc.opening += 1
        task = asyncio.get_running_loop().create_task(self.open(dc))
        self.openers.add(task)
        task.add_done_callback(self.openers.discard)

    def grow(self, dc):
        if self.retry_after(dc):
            return
        now, live = self.clock(), len(dc.live()) + dc.opening
        if not live:
            self.spawn(dc)
            return
        if live < min(dc.target, self.limit()):
            self.spawn(dc)
        elif (dc.target < self.limit() and not dc.opening and now - dc.changed >= GROW_AFTER
              and now - dc.flooded >= FLOOD_COOLDOWN):
            dc.target, dc.changed = dc.target + 1, now
            self.spawn(dc)

    def usable(self, dc):
        live = sorted(dc.live(), key=lambda session: session.opened)
        return live[:max(1, dc.target)]

    def retry_after(self, dc):
        if dc.error is None:
            return 0
        delay = ROUTE_RETRY if isinstance(dc.error, MediaRouteUnavailable) else OPEN_RETRY
        return max(0, dc.error_at + delay - self.clock())

    async def take(self, dc):
        while True:
            free = [session for session in self.usable(dc) if session.busy < self.per_session]
            if free:
                session = min(free, key=lambda item: item.busy)
                session.busy += 1
                self.watch()
                return session
            if not dc.live() and isinstance(dc.error, MediaRouteUnavailable):
                self.grow(dc)
                raise MediaRouteUnavailable(str(dc.error)) from dc.error
            if not dc.live() and not dc.opening and dc.error is not None \
                    and self.retry_after(dc):
                raise dc.error
            self.grow(dc)
            event = dc.event
            dc.waiters += 1
            try:
                await event.wait()
            finally:
                dc.waiters -= 1

    def give_back(self, dc, session):
        session.busy -= 1
        session.used = self.clock()
        if session.broken and not session.busy:
            self.discard(dc, session)
        self.poke(dc)

    async def get(self, dc_id):
        dc = self.dc(dc_id)
        session = await self.take(dc)
        self.give_back(dc, session)
        return session.sender

    def served(self, dc_id, session, size):
        dc = self.dc(dc_id)
        session.parts += 1
        session.bytes += size
        dc.stats["parts"] += 1
        dc.stats["bytes"] += size

    def flooded(self, dc_id, seconds):
        dc, now = self.dc(dc_id), self.clock()
        dc.stats["floods"] += 1
        if now - dc.flooded >= 1:
            dc.target = max(1, min(dc.target, len(dc.live())) - 1)
        dc.flooded = dc.changed = now

    def failed(self, dc_id, session, exc=None):
        dc = self.dc(dc_id)
        dc.stats["failures"] += 1
        if not session.broken:
            session.broken = True
            dc.target = max(1, dc.target - 1)
            dc.changed = self.clock()
        self.poke(dc)

    def forget_key(self, dc_id):
        dc = self.dcs.get(dc_id)
        if dc is not None and not dc.home:
            dc.auth_key = None
            for session in dc.sessions:
                session.broken = True
            for session in [item for item in dc.sessions if not item.busy]:
                self.discard(dc, session)
            self.poke(dc)

    def discard(self, dc, session):
        if session in dc.sessions:
            dc.sessions.remove(session)
            dc.stats["closed"] += 1
            self.later(self.disconnect(session.sender))

    def retire(self, dc):
        for session in dc.sessions:
            self.later(self.disconnect(session.sender))
        dc.sessions = []
        self.poke(dc)

    def later(self, coroutine):
        task = asyncio.get_running_loop().create_task(coroutine)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    @staticmethod
    async def disconnect(sender):
        try:
            result = sender.disconnect()
            if inspect.isawaitable(result):
                await result
        except Exception:
            pass

    async def open(self, dc):
        try:
            sender = await self.opener(dc)
        except asyncio.CancelledError:
            raise
        except MediaRouteUnavailable as exc:
            dc.error, dc.error_at = exc, self.clock()
        except Exception as exc:
            dc.error, dc.error_at = exc, self.clock()
            if isinstance(exc, TRANSIENT):
                dc.error = MediaRouteUnavailable("The dedicated media connection is temporarily unavailable.")
                dc.error.__cause__ = exc
            dc.stats["failures"] += 1
            dc.target = max(1, min(dc.target, len(dc.live())))
        else:
            if self.dcs.get(dc.dc_id) is not dc:
                self.later(self.disconnect(sender))
                return
            dc.error = None
            dc.sessions.append(_Session(sender, self.clock()))
            dc.stats["opened"] += 1
            self.watch()
        finally:
            dc.opening -= 1
            self.poke(dc)

    def watch(self):
        if self.reaper is None or self.reaper.done():
            self.reaper = asyncio.get_running_loop().create_task(self.reap())

    async def reap(self):
        while any(dc.sessions for dc in self.dcs.values()):
            await asyncio.sleep(REAP_EVERY)
            self.sweep()

    def sweep(self):
        now = self.clock()
        for dc in self.dcs.values():
            usable = set(map(id, self.usable(dc)))
            for session in list(dc.sessions):
                if session.busy:
                    continue
                spare = id(session) not in usable or len(dc.sessions) > 1
                if session.broken or (spare and now - session.used >= SESSION_IDLE) or now - session.used >= POOL_IDLE:
                    self.discard(dc, session)
            dc.target = max(1, min(dc.target, len(dc.live()) or 1))

    async def close(self):
        pending = list(self.openers)
        if self.reaper is not None:
            pending.append(self.reaper)
        for task in pending:
            task.cancel()
        senders = [session.sender for dc in self.dcs.values() for session in dc.sessions]
        for dc in self.dcs.values():
            dc.sessions = []
            self.poke(dc)
        self.dcs, self.reaper = {}, None
        await asyncio.gather(*pending, *(self.disconnect(sender) for sender in senders), return_exceptions=True)
        while self.tasks:
            await asyncio.gather(*tuple(self.tasks), return_exceptions=True)

    async def open_sender(self, dc):
        client = self.client
        await client._get_dc(dc.dc_id)
        config = getattr(client, "_config", None)
        options = [option for option in getattr(config, "dc_options", ())
                   if option.id == dc.dc_id and getattr(option, "media_only", False)
                   and not getattr(option, "cdn", False)]
        if not options:
            raise MediaRouteUnavailable("No dedicated media endpoint is available for this data center.")
        option = next((option for option in options
                       if bool(option.ipv6) == bool(getattr(client, "_use_ipv6", False))), options[0])
        if dc.home:
            key = client.session.auth_key
            if key is None or not key.key:
                raise ConnectionError("The account has no authorization key yet.")
            return await self.connect(dc, AuthKey(key.key), option.ip_address, option.port, None)
        async with dc.key_lock:
            if dc.auth_key is not None:
                return await self.connect(dc, AuthKey(dc.auth_key), option.ip_address, option.port, None)
            sender = await self.connect(dc, None, option.ip_address, option.port, None)
            try:
                exported = await client(functions.auth.ExportAuthorizationRequest(dc.dc_id))
                await self.initialize(sender, functions.auth.ImportAuthorizationRequest(id=exported.id,
                                                                                       bytes=exported.bytes))
            except BaseException:
                await self.disconnect(sender)
                raise
            dc.auth_key = sender.auth_key.key
            return sender

    async def connect(self, dc, key, host, port, query):
        client = self.client
        timeout = getattr(client, "_timeout", 10) or 10
        sender = MTProtoSender(key, loggers=client._log, retries=1, auto_reconnect=False, connect_timeout=timeout)
        sender.dc_id, sender.tgwitness_pool, sender.tgwitness_home = dc.dc_id, True, dc.home
        sender.tgwitness_initialized = False
        connection = client._connection(host, port, dc.dc_id, loggers=client._log, proxy=client._proxy,
                                        local_addr=getattr(client, "_local_addr", None))
        try:
            async with HANDSHAKES.turn("media"):
                await asyncio.wait_for(sender.connect(connection), timeout + 15)
            if query is not None:
                await self.initialize(sender, query)
        except BaseException:
            await self.disconnect(sender)
            raise
        return sender

    async def initialize(self, sender, query, call=None):
        init = copy.copy(self.client._init_request)
        init.query = query
        request = functions.InvokeWithLayerRequest(LAYER, functions.InvokeWithoutUpdatesRequest(init))
        result = await asyncio.wait_for(call(sender, request) if call else sender.send(request),
                                        (getattr(self.client, "_timeout", 10) or 10) + 15)
        sender.tgwitness_initialized = True
        return result

    async def request(self, session, call, request):
        if not getattr(session.sender, "tgwitness_initialized", True):
            async with session.init_lock:
                if not session.sender.tgwitness_initialized:
                    return await self.initialize(session.sender, request, call)
        return await call(session.sender, request)

    def snapshot(self):
        now, rows = self.clock(), []
        for dc in sorted(self.dcs.values(), key=lambda item: item.dc_id or 0):
            live = dc.live()
            shared = not live and isinstance(dc.error, MediaRouteUnavailable)
            rows.append({"dc": dc.dc_id, "home": dc.home, "connections": len(live), "target": dc.target,
                         "opening": dc.opening, "busy": sum(session.busy for session in live), "waiting": dc.waiters,
                         "flooded_seconds_ago": round(now - dc.flooded) if dc.flooded > -math.inf else None,
                         "shared_connection": shared,
                         "shared_retry_seconds": math.ceil(self.retry_after(dc)) if shared else None,
                         "shared_reason": type(dc.error.__cause__).__name__ if shared and dc.error.__cause__ else None,
                         "error": type(dc.error).__name__ if dc.error is not None
                         and not isinstance(dc.error, MediaRouteUnavailable) else None, **dc.stats})
        return {"enabled": self.enabled(), "limit": self.limit(), "per_connection": self.per_session, "dcs": rows,
                "meaning": MEANING}


class PartReader:
    def __init__(self, pool, call, location, dc_id, *, size, part, timeout):
        self.pool, self.call, self.location, self.dc_id = pool, call, location, dc_id
        self.size, self.part, self.timeout = size, part, timeout

    async def read(self, offset):
        for attempt in range(PART_ATTEMPTS):
            dc_id, pause = self.dc_id, 0
            dc = self.pool.dc(dc_id)
            session, borrowed = None, False
            try:
                session = await self.pool.take(dc)
                sender = session.sender
            except MediaRouteUnavailable:
                if dc.home:
                    sender = self.pool.client._sender
                else:
                    sender = await self.pool.client._borrow_exported_sender(dc.dc_id)
                    borrowed = True
            try:
                request = functions.upload.GetFileRequest(self.location, offset, self.part)
                result = await asyncio.wait_for(self.pool.request(session, self.call, request) if session
                                                else self.call(sender, request), self.timeout)
            except errors.FileMigrateError as exc:
                self.dc_id = exc.new_dc
                continue
            except FLOODS as exc:
                self.pool.flooded(dc_id, exc.seconds)
                if exc.seconds > PART_FLOOD_PATIENCE or attempt == PART_ATTEMPTS - 1:
                    raise
                pause = exc.seconds
            except TRANSIENT as exc:
                if session:
                    self.pool.failed(dc_id, session, exc)
                if attempt == PART_ATTEMPTS - 1:
                    raise
                pause = .25 * 2 ** attempt
            else:
                if not isinstance(result, types.upload.File):
                    raise ValueError("unexpected_file_part_answer")
                if len(result.bytes) > self.part:
                    raise ValueError("file_part_larger_than_requested")
                if session:
                    self.pool.served(dc_id, session, len(result.bytes))
                return result.bytes
            finally:
                if session:
                    self.pool.give_back(dc, session)
                elif borrowed:
                    await self.pool.client._return_exported_sender(sender)
            if pause:
                await asyncio.sleep(pause)
        raise ConnectionError("file_part_unavailable")

    async def run(self, write):
        pending, ready, scheduled, written, end = {}, {}, 0, 0, None
        try:
            while True:
                window = self.pool.window(self.dc_id) if self.size else 1
                while end is None and (self.size is None or scheduled < self.size) \
                        and len(pending) + len(ready) < window:
                    pending[scheduled] = asyncio.get_running_loop().create_task(self.read(scheduled))
                    scheduled += self.part
                if written in ready:
                    data = ready.pop(written)
                    await write(data, written + len(data))
                    written += len(data)
                    if len(data) < self.part:
                        break
                    continue
                if not pending:
                    break
                done, _ = await asyncio.wait(pending.values(), return_when=asyncio.FIRST_COMPLETED)
                for offset in sorted(offset for offset, task in pending.items() if task in done):
                    data = pending.pop(offset).result()
                    ready[offset] = data
                    if len(data) < self.part and (end is None or offset < end):
                        end = offset
                if end is not None:
                    discarded = [task for offset, task in pending.items() if offset > end]
                    for task in discarded:
                        task.cancel()
                    await asyncio.gather(*discarded, return_exceptions=True)
                    for offset in [offset for offset in pending if offset > end]:
                        del pending[offset]
                    for offset in [offset for offset in ready if offset > end]:
                        del ready[offset]
        finally:
            for task in pending.values():
                task.cancel()
            await asyncio.gather(*pending.values(), return_exceptions=True)
        return written


def media_owner(client):
    for _ in range(4):
        inner = None
        for name in ("_export_client", "_TakeoutClient__client"):
            try:
                inner = object.__getattribute__(client, name)
            except AttributeError:
                continue
            break
        if inner is None:
            return client
        client = inner
    return client


def part_size(part_size_kb, file_size):
    if part_size_kb:
        size = int(part_size_kb * 1024)
        if size not in VALID_PARTS:
            raise ValueError("The part size must divide 1 MiB and be a multiple of 4096.")
        return size
    return PART


async def download_file(owner, call, input_location, file=None, *, part_size_kb=None, file_size=None,
                        progress_callback=None, dc_id=None):
    pool = owner.media_connections()
    info = utils._get_file_info(input_location)
    dc_id = info.dc_id or dc_id
    size = file_size if file_size is not None else info.size
    if isinstance(file, pathlib.Path):
        file = str(file.absolute())
    in_memory = file is None or file is bytes
    if in_memory:
        stream = io.BytesIO()
    elif isinstance(file, str):
        helpers.ensure_parent_dir_exists(file)
        stream = open(file, "wb")
    else:
        stream = file
    reader = PartReader(pool, call, info.location, dc_id, size=size or None,
                        part=part_size(part_size_kb, size), timeout=max(30, getattr(owner, "_timeout", 10) * 2))

    async def write(data, position):
        result = stream.write(data)
        if inspect.isawaitable(result):
            await result
        if progress_callback:
            result = progress_callback(position, size)
            if inspect.isawaitable(result):
                await result
    try:
        await reader.run(write)
        if callable(getattr(stream, "flush", None)):
            stream.flush()
        if in_memory:
            return stream.getvalue()
        return None
    finally:
        if isinstance(file, str) or in_memory:
            stream.close()
