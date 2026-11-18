"""Open a Telegram mini application in a headless Chromium and record what it loads.

Chromium talks to TgWitness over --remote-debugging-pipe, so no extra Python package is needed. The application runs
in its own browser context: every connection it makes, WebSockets included, goes through a loopback gate that opens it
with netclient over the workspace's route for requests outside Telegram; addresses inside the local network are
refused there, as for any other fetch. Chromium's own background requests go to a second gate that refuses them.
"""
import asyncio
import base64
import contextlib
import json
import os
import shutil
import tempfile
import time
from pathlib import Path
from urllib.parse import quote, quote_plus, urlsplit

from . import netclient

try:
    import fcntl
except ImportError:
    fcntl = None

NAMES = ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome")
BINDING = "__tgwitnessPostEvent"
VIEWPORT = {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True}
AGENT = "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v} Mobile Safari/537.36"
SHOTS = (2, 8, 16)
LOAD_TIMEOUT = 25
TOTAL_TIMEOUT = 75
MAX_REQUESTS = 400
MAX_SOCKETS = 20
MAX_FRAMES = 30
MAX_FRAME_CHARS = 2000
MAX_EVENTS = 200
MAX_CONSOLE = 60
MAX_SCRIPTS = 25
MAX_SCRIPT_BYTES = 4 * 1024**2
MAX_PAGE_BYTES = 4 * 1024**2
MAX_TEXT_CHARS = 200_000
MAX_TRAFFIC = 256 * 1024**2
REMOVED = "[removed]"
BROWSER_HOSTS = frozenset({"www.google.com", "accounts.google.com", "clients2.google.com", "update.googleapis.com",
                           "optimizationguide-pa.googleapis.com", "safebrowsing.googleapis.com",
                           "content-autofill.googleapis.com"})
ROOT = ("Chromium cannot use its sandbox when TgWitness runs as root. Run TgWitness as an ordinary user, or set "
        "TGWITNESS_BROWSER_NO_SANDBOX=1 to open mini applications without the sandbox on a machine used only for this.")
MISSING = ("No Chromium was found for opening mini applications. Install the chromium package, or set "
           "TGWITNESS_CHROMIUM to the browser's path, then try again.")
PLATFORM = "Opening mini applications in a browser needs Linux or macOS; this system gets a page and script analysis."
SHIM = """(() => {
  const send = (type, data) => {
    try { window.%s(JSON.stringify({type: String(type), data: data === undefined || data === null ? null : String(data),
      frame: window === window.top ? 'top' : 'frame'})); } catch (error) {}
  };
  try { Object.defineProperty(window, 'TelegramWebviewProxy', {value: Object.freeze({postEvent: send}), configurable: false}); }
  catch (error) {}
})();""" % BINDING
PAGE_FACTS = """(() => {
  const take = (list, n) => [...new Set(list.filter(Boolean))].slice(0, n);
  return JSON.stringify({
    href: location.href, title: document.title || '',
    text: (document.body ? document.body.innerText : '').slice(0, %d),
    links: take([...document.querySelectorAll('a[href]')].map(a => a.href), 300),
    forms: take([...document.querySelectorAll('form')].map(f => (f.method || 'get').toUpperCase() + ' ' + (f.action || location.href)), 50),
    frames: take([...document.querySelectorAll('iframe[src]')].map(f => f.src), 50),
    inputs: take([...document.querySelectorAll('input,textarea')].map(i => [i.type || 'text', i.name || i.id || '', i.placeholder || ''].join(' · ')), 80),
    webapp: (() => { const w = window.Telegram && window.Telegram.WebApp;
      return w ? {version: w.version || null, platform: w.platform || null, has_init_data: !!w.initData} : null; })()
  });
})()""" % MAX_TEXT_CHARS


class Unavailable(RuntimeError):
    pass


def browser_path():
    configured = os.environ.get("TGWITNESS_CHROMIUM", "").strip()
    if configured:
        return configured if os.path.isfile(configured) and os.access(configured, os.X_OK) else None
    for name in NAMES:
        found = shutil.which(name)
        if found:
            return found
    cache = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or Path.home() / ".cache" / "ms-playwright")
    with contextlib.suppress(OSError):
        for path in sorted(cache.glob("chromium-*/chrome-linux*/chrome"), reverse=True):
            if os.access(path, os.X_OK):
                return str(path)
    return None


def status():
    if os.name != "posix" or fcntl is None:
        return {"browser": False, "reason": PLATFORM}
    path = browser_path()
    if not path:
        return {"browser": False, "reason": MISSING}
    if os.geteuid() == 0 and os.environ.get("TGWITNESS_BROWSER_NO_SANDBOX") != "1":
        return {"browser": False, "reason": ROOT, "path": path}
    return {"browser": True, "path": path, "sandbox": os.geteuid() != 0}


class Redactor:
    """Removes the signed launch data, which works as a login to the mini application for a while."""

    def __init__(self, init_data):
        secrets = set()
        if init_data:
            secrets |= {init_data, quote(init_data, safe=""), quote(init_data), quote_plus(init_data)}
            for part in init_data.split("&"):
                name, _, value = part.partition("=")
                if name in ("hash", "signature", "query_id") and len(value) >= 8:
                    secrets.add(value)
        self.secrets = sorted((s for s in secrets if len(s) >= 8), key=len, reverse=True)

    def __call__(self, value):
        if isinstance(value, str):
            for secret in self.secrets:
                if secret in value:
                    value = value.replace(secret, REMOVED)
            return value
        if isinstance(value, list):
            return [self(item) for item in value]
        if isinstance(value, dict):
            return {key: self(item) for key, item in value.items()}
        return value


def public_address(url):
    """The launch address without its fragment, where Telegram puts the signed launch data."""
    parts = urlsplit(url or "")
    return parts._replace(fragment="").geturl() if parts.scheme else ""


class Gate:
    """Loopback proxy for Chromium: each connection is opened by netclient over the workspace route."""

    def __init__(self, route, timeout=20, refuse=False):
        self.route, self.timeout, self.refuse = route, timeout, refuse
        self.server, self.tasks, self.traffic = None, set(), 0
        self.hosts, self.blocked = {}, []

    async def start(self):
        self.server = await asyncio.start_server(self.accept, "127.0.0.1", 0, limit=1024 * 1024)
        return self.server.sockets[0].getsockname()[1]

    async def close(self):
        if self.server:
            self.server.close()
            with contextlib.suppress(Exception):
                await self.server.wait_closed()
        for task in list(self.tasks):
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)

    def accept(self, reader, writer):
        task = asyncio.ensure_future(self.serve(reader, writer))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    def note(self, host, port, up=0, down=0, opened=False, peer=None):
        item = self.hosts.setdefault(host, {"host": host, "ports": [], "connections": 0, "sent": 0, "received": 0})
        if port not in item["ports"]:
            item["ports"].append(port)
        item["connections"] += 1 if opened else 0
        item["sent"] += up
        item["received"] += down
        if peer and self.route.kind == "direct":
            item["address"] = peer

    async def serve(self, reader, writer):
        upstream = None
        try:
            head = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), self.timeout)
            if self.refuse:
                writer.write(b"HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
                await writer.drain()
                return
            line, _, rest = head.partition(b"\r\n")
            method, target, version = line.decode("latin-1").split(" ", 2)
            if method == "CONNECT":
                host, _, port = target.rpartition(":")
                port, first = int(port), b""
            else:
                parts = urlsplit(target)
                if parts.scheme != "http" or not parts.hostname:
                    raise ValueError("unsupported request")
                host, port = parts.hostname, parts.port or 80
                path = (parts.path or "/") + ("?" + parts.query if parts.query else "")
                headers = [h for h in rest.split(b"\r\n") if h and not h.lower().startswith(
                    (b"proxy-", b"connection:", b"keep-alive:"))]
                first = (method + " " + path + " " + version.strip() + "\r\n").encode("latin-1") \
                    + b"\r\n".join(headers) + b"\r\nConnection: close\r\n\r\n"
            host = host.strip("[]").lower()
            try:
                upstream = await netclient.open_stream("http://" + (f"[{host}]" if ":" in host else host) + f":{port}/",
                                                       self.route, self.timeout)
            except (netclient.RouteError, OSError, ValueError, asyncio.TimeoutError) as exc:
                if len(self.blocked) < 100:
                    self.blocked.append({"host": host, "port": port, "reason": str(exc)[:200] or type(exc).__name__})
                writer.write(b"HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
                await writer.drain()
                return
            peer = upstream[1].get_extra_info("peername")
            self.note(host, port, opened=True, peer=peer[0] if peer else None)
            if method == "CONNECT":
                writer.write(b"HTTP/1.1 200 Connection established\r\n\r\n")
                await writer.drain()
            else:
                upstream[1].write(first)
                self.note(host, port, up=len(first))
            await asyncio.gather(self.pump(reader, upstream[1], host, port, True),
                                 self.pump(upstream[0], writer, host, port, False))
        except (OSError, ValueError, asyncio.IncompleteReadError, asyncio.LimitOverrunError, asyncio.TimeoutError):
            pass
        finally:
            for stream in (writer, upstream[1] if upstream else None):
                if stream:
                    with contextlib.suppress(Exception):
                        stream.close()

    async def pump(self, source, sink, host, port, outgoing):
        try:
            while chunk := await source.read(65536):
                self.traffic += len(chunk)
                if self.traffic > MAX_TRAFFIC:
                    break
                self.note(host, port, up=len(chunk) if outgoing else 0, down=0 if outgoing else len(chunk))
                sink.write(chunk)
                await sink.drain()
        except (OSError, asyncio.IncompleteReadError):
            pass
        finally:
            with contextlib.suppress(Exception):
                if sink.can_write_eof():
                    sink.write_eof()


class Pipe:
    """Chrome DevTools Protocol over the --remote-debugging-pipe file descriptors."""

    def __init__(self, reader, write_fd, on_event):
        self.reader, self.write_fd, self.on_event = reader, write_fd, on_event
        self.next, self.waiting, self.closed = 0, {}, False
        self.task = asyncio.ensure_future(self.read())

    async def read(self):
        buffer = b""
        try:
            while chunk := await self.reader.read(1024 * 1024):
                buffer += chunk
                while b"\0" in buffer:
                    raw, _, buffer = buffer.partition(b"\0")
                    message = json.loads(raw)
                    if "id" in message:
                        future = self.waiting.pop(message["id"], None)
                        if future and not future.done():
                            future.set_result(message)
                    else:
                        with contextlib.suppress(Exception):
                            self.on_event(message)
        except (OSError, ValueError):
            pass
        finally:
            self.closed = True
            for future in self.waiting.values():
                if not future.done():
                    future.set_exception(Unavailable("Chromium stopped."))
            self.waiting.clear()

    async def send(self, method, params=None, session=None, timeout=20):
        if self.closed:
            raise Unavailable("Chromium stopped.")
        self.next += 1
        message = {"id": self.next, "method": method, "params": params or {}}
        if session:
            message["sessionId"] = session
        future = asyncio.get_running_loop().create_future()
        self.waiting[self.next] = future
        data = json.dumps(message).encode() + b"\0"
        while data:
            written = await asyncio.to_thread(os.write, self.write_fd, data)
            data = data[written:]
        answer = await asyncio.wait_for(future, timeout)
        if "error" in answer:
            raise RuntimeError(answer["error"].get("message") or method)
        return answer.get("result") or {}


def tail(folder):
    with contextlib.suppress(OSError):
        lines = [line for line in Path(folder, "browser.log").read_text("utf-8", "replace").splitlines()
                 if line.strip() and "dbus" not in line.lower()]
        if lines:
            return " Chromium said: " + " | ".join(lines[-3:])[:600]
    return ""


def high(fd):
    moved = fcntl.fcntl(fd, fcntl.F_DUPFD, 10)
    os.close(fd)
    return moved


class Session:
    def __init__(self, redact):
        self.redact = redact
        self.requests, self.order, self.sockets, self.events = {}, [], {}, []
        self.console, self.dialogs, self.popups, self.downloads = [], [], [], []
        self.loaded = asyncio.Event()
        self.main_frame = self.final_url = None
        self.dropped = {"requests": 0, "frames": 0, "events": 0, "console": 0}

    def clip(self, value, size=MAX_FRAME_CHARS):
        value = self.redact(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False))
        return value if len(value) <= size else value[:size] + "…"

    def handle(self, message):
        method, params = message.get("method"), message.get("params") or {}
        if method == "Network.requestWillBeSent":
            key = params["requestId"]
            request = params.get("request") or {}
            if key in self.requests and params.get("redirectResponse"):
                hop = self.requests.pop(key)
                hop.update(status=params["redirectResponse"].get("status"), redirected=True)
                moved = key + "#" + str(len(self.order))
                self.requests[moved] = hop
                self.order[self.order.index(key)] = moved
            if key not in self.requests:
                if len(self.order) >= MAX_REQUESTS:
                    self.dropped["requests"] += 1
                    return
                self.order.append(key)
            self.requests[key] = {"url": self.clip(request.get("url", ""), 4096), "method": request.get("method"),
                                  "type": params.get("type"), "started": params.get("timestamp"),
                                  "initiator": (params.get("initiator") or {}).get("type")}
        elif method == "Network.responseReceived":
            item = self.requests.get(params.get("requestId"))
            response = params.get("response") or {}
            if item is not None:
                security = response.get("securityDetails") or {}
                item.update(status=response.get("status"), mime=response.get("mimeType"),
                            protocol=response.get("protocol"), certificate={
                                "subject": security.get("subjectName"), "issuer": security.get("issuer"),
                                "valid_to": security.get("validTo")} if security else None)
        elif method == "Network.loadingFinished":
            item = self.requests.get(params.get("requestId"))
            if item is not None:
                item["bytes"] = params.get("encodedDataLength")
                item["finished"] = True
        elif method == "Network.loadingFailed":
            item = self.requests.get(params.get("requestId"))
            if item is not None:
                item["error"] = params.get("blockedReason") or params.get("errorText")
        elif method == "Network.webSocketCreated":
            if len(self.sockets) < MAX_SOCKETS:
                self.sockets[params["requestId"]] = {"url": self.clip(params.get("url", ""), 4096), "frames": [],
                                                     "sent": 0, "received": 0}
        elif method in ("Network.webSocketFrameSent", "Network.webSocketFrameReceived"):
            socket = self.sockets.get(params.get("requestId"))
            if socket is None:
                return
            direction = "sent" if method.endswith("Sent") else "received"
            socket[direction] += 1
            frame = params.get("response") or {}
            if len(socket["frames"]) < MAX_FRAMES:
                text = frame.get("payloadData", "") if frame.get("opcode") == 1 else "[binary]"
                socket["frames"].append({"direction": direction, "at": params.get("timestamp"), "data": self.clip(text)})
            else:
                self.dropped["frames"] += 1
        elif method == "Runtime.bindingCalled" and params.get("name") == BINDING:
            if len(self.events) >= MAX_EVENTS:
                self.dropped["events"] += 1
                return
            with contextlib.suppress(ValueError, TypeError):
                event = json.loads(params.get("payload") or "{}")
                self.events.append({"type": str(event.get("type"))[:120], "data": self.clip(event.get("data")),
                                    "frame": event.get("frame"), "at": time.time()})
        elif method == "Runtime.consoleAPICalled":
            if len(self.console) >= MAX_CONSOLE:
                self.dropped["console"] += 1
                return
            text = " ".join(str(arg.get("value", arg.get("description", ""))) for arg in params.get("args") or [])
            self.console.append({"level": params.get("type"), "text": self.clip(text, 500)})
        elif method == "Page.javascriptDialogOpening":
            self.dialogs.append({"type": params.get("type"), "message": self.clip(params.get("message", ""), 1000)})
        elif method == "Page.frameNavigated":
            frame = params.get("frame") or {}
            if not frame.get("parentId"):
                self.main_frame, self.final_url = frame.get("id"), frame.get("url")
        elif method == "Page.loadEventFired":
            self.loaded.set()
        elif method == "Page.windowOpen":
            if len(self.popups) < 50:
                self.popups.append({"url": self.clip(params.get("url", ""), 4096),
                                    "name": self.clip(params.get("windowName", ""), 200),
                                    "user_gesture": bool(params.get("userGesture")), "opened": False})
        elif method in ("Page.downloadWillBegin", "Browser.downloadWillBegin"):
            if len(self.downloads) < 50:
                self.downloads.append({"url": self.clip(params.get("url", ""), 4096),
                                       "file": self.clip(params.get("suggestedFilename", ""), 300)})


async def capture(url, route, init_data=None, settle=SHOTS):
    """Open url once and return (facts, files). Files are (role, mime, bytes, label)."""
    state = status()
    if not state["browser"]:
        raise Unavailable(state["reason"])
    redact = Redactor(init_data)
    gate, quiet = Gate(route), Gate(route, refuse=True)
    session_state = Session(redact)
    folder = tempfile.mkdtemp(prefix="tgwitness-webapp-")
    process = pipe = None
    files, errors, facts, version, started = [], [], {}, "", time.monotonic()
    try:
        port, idle = await gate.start(), await quiet.start()
        arguments = [state["path"], "--headless=new", "--remote-debugging-pipe", "--user-data-dir=" + folder,
                     "--no-first-run", "--no-default-browser-check", "--disable-extensions", "--disable-sync",
                     "--disable-background-networking", "--disable-component-update", "--disable-default-apps",
                     "--disable-dev-shm-usage", "--disable-gpu", "--mute-audio", "--hide-scrollbars",
                     "--disable-features=Translate,MediaRouter,OptimizationHints,IsolateOrigins,site-per-process,"
                     "AutofillServerCommunication,CertificateTransparencyComponentUpdater,InterestFeedContentSuggestions",
                     "--deny-permission-prompts", "--password-store=basic", "--use-mock-keychain",
                     "--disable-client-side-phishing-detection", "--disable-domain-reliability", "--no-pings",
                     "--disable-breakpad", "--safebrowsing-disable-auto-update", "--disable-field-trial-config",
                     f"--proxy-server=http://127.0.0.1:{idle}", "--proxy-bypass-list=<-loopback>",
                     "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
                     "--webrtc-ip-handling-policy=disable_non_proxied_udp",
                     f"--window-size={VIEWPORT['width']},{VIEWPORT['height']}", "about:blank"]
        if os.geteuid() == 0:
            arguments.insert(1, "--no-sandbox")
        to_child, from_parent = os.pipe()
        from_child, to_parent = os.pipe()
        to_child, to_parent = high(to_child), high(to_parent)

        for fd in (3, 4):
            try:
                os.fstat(fd)
            except OSError:
                filler = os.open(os.devnull, os.O_RDONLY)
                if filler != fd:
                    os.dup2(filler, fd)
                    os.close(filler)

        def wire():
            os.dup2(to_child, 3)
            os.dup2(to_parent, 4)

        with open(os.path.join(folder, "browser.log"), "wb") as log:
            process = await asyncio.create_subprocess_exec(
                *arguments, stdin=asyncio.subprocess.DEVNULL, stdout=log, stderr=log,
                pass_fds=(3, 4), preexec_fn=wire, start_new_session=True)
        os.close(to_child)
        os.close(to_parent)
        reader = asyncio.StreamReader(limit=64 * 1024 * 1024)
        loop = asyncio.get_running_loop()
        await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), os.fdopen(from_child, "rb", 0))
        pipe = Pipe(reader, from_parent, session_state.handle)
        version = (await pipe.send("Browser.getVersion", timeout=30)).get("product", "")
        with contextlib.suppress(Exception):
            await pipe.send("Browser.setDownloadBehavior", {"behavior": "deny", "eventsEnabled": True})
        context = (await pipe.send("Target.createBrowserContext", {
            "proxyServer": f"http://127.0.0.1:{port}", "proxyBypassList": "<-loopback>"}))["browserContextId"]
        target = (await pipe.send("Target.createTarget", {"url": "about:blank", "browserContextId": context}))["targetId"]
        session = (await pipe.send("Target.attachToTarget", {"targetId": target, "flatten": True}))["sessionId"]

        async def call(method, params=None, timeout=20):
            return await pipe.send(method, params, session, timeout)

        await call("Page.enable")
        await call("Network.enable", {"maxTotalBufferSize": 64 * 1024**2, "maxResourceBufferSize": MAX_SCRIPT_BYTES})
        await call("Runtime.enable")
        await call("Emulation.setDeviceMetricsOverride", VIEWPORT)
        await call("Emulation.setTouchEmulationEnabled", {"enabled": True, "maxTouchPoints": 5})
        major = version.split("/")[-1].split(".")[0] if "/" in version else "130"
        await call("Network.setUserAgentOverride", {"userAgent": AGENT.format(v=major + ".0.0.0"), "platform": "Android"})
        await call("Runtime.addBinding", {"name": BINDING})
        await call("Page.addScriptToEvaluateOnNewDocument", {"source": SHIM})
        await call("Page.setLifecycleEventsEnabled", {"enabled": True})

        async def dialogs():
            seen = 0
            while True:
                await asyncio.sleep(0.2)
                if len(session_state.dialogs) > seen:
                    seen = len(session_state.dialogs)
                    with contextlib.suppress(Exception):
                        await call("Page.handleJavaScriptDialog", {"accept": False})

        dismiss = asyncio.ensure_future(dialogs())
        try:
            navigation = await call("Page.navigate", {"url": url}, timeout=LOAD_TIMEOUT)
            if navigation.get("errorText"):
                errors.append({"component": "navigation", "error": navigation["errorText"]})
            with contextlib.suppress(asyncio.TimeoutError):
                await asyncio.wait_for(session_state.loaded.wait(), LOAD_TIMEOUT)
            waited = 0
            for index, moment in enumerate(settle):
                await asyncio.sleep(max(0, moment - waited))
                waited = moment
                if time.monotonic() - started > TOTAL_TIMEOUT:
                    errors.append({"component": "time", "error": "Stopped at the time limit."})
                    break
                with contextlib.suppress(Exception):
                    shot = await call("Page.captureScreenshot", {"format": "png"}, timeout=20)
                    files.append(("screenshot", "image/png", base64.b64decode(shot["data"]),
                                  f"{moment} s after loading"))
            with contextlib.suppress(Exception):
                metrics = await call("Page.getLayoutMetrics")
                size = metrics.get("cssContentSize") or metrics.get("contentSize") or {}
                height = min(int(size.get("height") or 0), 12000)
                if height > VIEWPORT["height"] + 40:
                    shot = await call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True,
                                                                 "clip": {"x": 0, "y": 0, "width": VIEWPORT["width"],
                                                                          "height": height, "scale": 0.5}}, timeout=30)
                    files.append(("screenshot", "image/png", base64.b64decode(shot["data"]), "Whole page"))
            with contextlib.suppress(Exception):
                found = await call("Runtime.evaluate", {"expression": PAGE_FACTS, "returnByValue": True}, timeout=15)
                facts = json.loads((found.get("result") or {}).get("value") or "{}")
            with contextlib.suppress(Exception):
                html = await call("Runtime.evaluate", {"expression": "document.documentElement.outerHTML",
                                                       "returnByValue": True}, timeout=15)
                page = ((html.get("result") or {}).get("value") or "").encode("utf-8")[:MAX_PAGE_BYTES]
                if page:
                    files.append(("page", "text/html", redact(page.decode("utf-8", "replace")).encode("utf-8"),
                                  "Page after loading"))
            scripts = 0
            for key in session_state.order:
                item = session_state.requests[key]
                if scripts >= MAX_SCRIPTS or item.get("type") != "Script" or not item.get("finished") or "#" in key:
                    continue
                with contextlib.suppress(Exception):
                    body = await call("Network.getResponseBody", {"requestId": key}, timeout=15)
                    data = base64.b64decode(body["body"]) if body.get("base64Encoded") else body["body"].encode("utf-8")
                    if 0 < len(data) <= MAX_SCRIPT_BYTES:
                        files.append(("script", "text/javascript", data, item["url"]))
                        item["saved"] = True
                        scripts += 1
        finally:
            dismiss.cancel()
            with contextlib.suppress(BaseException):
                await dismiss
        with contextlib.suppress(Exception):
            await pipe.send("Browser.close", timeout=5)
    except Unavailable as exc:
        raise Unavailable(str(exc) + tail(folder)) from None
    except (OSError, RuntimeError, ValueError, KeyError, asyncio.TimeoutError) as exc:
        if pipe is None or not files:
            raise Unavailable("Chromium could not open the mini application: " + (str(exc)[:300] or type(exc).__name__)
                              + tail(folder))
        errors.append({"component": "browser", "error": str(exc)[:300] or type(exc).__name__})
    finally:
        if process and process.returncode is None:
            with contextlib.suppress(ProcessLookupError):
                process.kill()
            with contextlib.suppress(Exception):
                await asyncio.wait_for(process.wait(), 10)
        if pipe:
            pipe.task.cancel()
            with contextlib.suppress(BaseException):
                await pipe.task
            with contextlib.suppress(OSError):
                os.close(pipe.write_fd)
        await gate.close()
        await quiet.close()
        shutil.rmtree(folder, ignore_errors=True)
    requests = [session_state.requests[key] for key in session_state.order]
    asked = {(urlsplit(item.get("url") or "").hostname or "").lower()
             for item in requests + list(session_state.sockets.values())}
    hosts = sorted(gate.hosts.values(), key=lambda item: item["host"])
    own = [item for item in hosts if item["host"] in BROWSER_HOSTS and item["host"] not in asked]
    return {
        "browser": version, "sandbox": os.geteuid() != 0, "duration_ms": int((time.monotonic() - started) * 1000),
        "final_url": public_address(redact(facts.get("href") or session_state.final_url or "")),
        "title": redact(facts.get("title") or "")[:300], "text": redact(facts.get("text") or ""),
        "links": redact(facts.get("links") or []), "forms": redact(facts.get("forms") or []),
        "frames": redact(facts.get("frames") or []), "inputs": redact(facts.get("inputs") or []),
        "webapp": facts.get("webapp"), "requests": requests, "sockets": list(session_state.sockets.values()),
        "telegram_events": session_state.events, "console": session_state.console,
        "dialogs": session_state.dialogs, "popups": session_state.popups, "downloads": session_state.downloads,
        "connections": [item for item in hosts if item not in own], "browser_connections": own, "blocked": gate.blocked,
        "dropped": session_state.dropped, "errors": errors}, files
