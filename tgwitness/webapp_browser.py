"""Open a Telegram mini application in a headless Chromium and record what it loads.

Chromium talks to TgWitness over --remote-debugging-pipe, so no extra Python package is needed. The application runs
in its own browser context: every connection it makes, WebSockets included, goes through a loopback gate that opens it
with netclient over the workspace's route for requests outside Telegram; addresses inside the local network are
refused there, as for any other fetch. Chromium's own background requests go to a second gate that refuses them.
"""
import asyncio
import base64
import contextlib
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import secrets
import shutil
import struct
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import quote, quote_plus, urlsplit

from . import netclient

try:
    import fcntl
except ImportError:
    fcntl = None

NAMES = ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome", "msedge")
BINDING = "__tgwitnessPostEvent"
VIEWPORT = {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True}
AGENT = "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v} Mobile Safari/537.36"
SHOTS = (2, 8, 16)
LOAD_TIMEOUT = 25
TOTAL_TIMEOUT = 75
INTERACTIVE_TIMEOUT = 180
MAX_REQUESTS = 400
MAX_SOCKETS = 20
MAX_FRAMES = 30
MAX_FRAME_CHARS = 2000
MAX_EVENTS = 200
MAX_CONSOLE = 60
MAX_SCRIPTS = 25
MAX_SCRIPT_BYTES = 4 * 1024**2
MAX_PAGE_BYTES = 4 * 1024**2
MAX_MHTML_BYTES = 12 * 1024**2
MAX_TEXT_CHARS = 200_000
MAX_TRAFFIC = 256 * 1024**2
MAX_CLICKS = 40
MAX_BROWSERS = 2
BROWSER_WAIT = 60
_browsers = asyncio.Semaphore(MAX_BROWSERS)
CLICK_SETTLE = 1.5
WORLD = "tgwitness-crawl"
REMOVED = "[removed]"
DANGEROUS_CLICK = re.compile(
    r"pay|buy|purchase|checkout|order|confirm|approve|withdraw|transfer|send|delete|remove|donate|tip|subscribe|"
    r"invoice|stars?\b|⭐|💎|\bton\b|wallet|connect|sign|claim|stake|swap|deposit|bet|"
    r"\bok\b|\byes\b|accept|agree|upgrade|premium|join|vote|gift|mint|spin|allow|share|invite|"
    r"купи|оплат|подтвер|підтвер|удал|видал|отправ|надісл|вывест|вивест|перевод|переказ|подпис|підпис|"
    r"кошел|гаманец|ставк|\bда\b|\bтак\b|соглас|згод|подел|поділ|пригла|запрос",
    re.I,
)
DANGEROUS_SCHEMES = ("javascript:", "mailto:", "tel:", "tg:", "ton:", "bitcoin:", "ethereum:")
BROWSER_HOSTS = frozenset({"www.google.com", "accounts.google.com", "clients2.google.com", "update.googleapis.com",
                           "optimizationguide-pa.googleapis.com", "safebrowsing.googleapis.com",
                           "content-autofill.googleapis.com", "www.gstatic.com", "edge.microsoft.com"})
ROOT = ("Chromium cannot use its sandbox when TgWitness runs as root. Run TgWitness as an ordinary user, or set "
        "TGWITNESS_BROWSER_NO_SANDBOX=1 to open mini applications without the sandbox on a machine used only for this.")
MISSING = ("No Chromium was found for opening mini applications. Install Chromium/Chrome/Edge, or set "
           "TGWITNESS_CHROMIUM to the browser's path, then try again.")
PLATFORM = "Opening mini applications in a browser is not supported on this platform; this system gets a page and script analysis."
NO_WINDOW = ("Interactive mode needs a desktop session, and this system has no display: neither DISPLAY nor "
             "WAYLAND_DISPLAY is set. Choose passive or safe crawl mode.")
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
STATE_SIG_JS = """(() => {
  const txt = ((document.body && document.body.innerText) || '').replace(/\\s+/g, ' ').trim().slice(0, 8000);
  return JSON.stringify({href: location.href.split('#')[0], title: document.title || '', text: txt});
})()"""
CLICKABLES_JS = """(() => {
  const items = [];
  const seen = new Set();
  const els = document.querySelectorAll('a[href], button, [role="tab"], [role="button"], nav li');
  for (let i = 0; i < els.length && items.length < 40; i++) {
    const el = els[i];
    if (el.disabled || el.getAttribute('aria-disabled') === 'true') continue;
    const rect = el.getBoundingClientRect();
    if (rect.width < 8 || rect.height < 8 || rect.bottom < 0 || rect.top > window.innerHeight * 2) continue;
    const text = (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || '').replace(/\\s+/g, ' ').trim().slice(0, 120);
    const href = el.getAttribute('href') || '';
    const key = text + '|' + href;
    if (!text && !href) continue;
    if (seen.has(key)) continue;
    seen.add(key);
    const words = [el.getAttribute('aria-label'), el.getAttribute('title'), el.value]
      .map(value => String(value || '').replace(/\\s+/g, ' ').trim()).filter(Boolean).join(' ').slice(0, 400);
    items.push({index: i, text, href, words, x: Math.round(rect.left + rect.width / 2), y: Math.round(rect.top + rect.height / 2)});
  }
  return JSON.stringify(items);
})()"""
ELEMENT_AT_JS = """((x, y) => {
  const targets = 'a[href], button, [role="tab"], [role="button"], nav li';
  const clean = value => String(value || '').replace(/\\s+/g, ' ').trim();
  const hit = document.elementFromPoint(x, y);
  const el = hit && hit.closest(targets);
  if (!el) return null;
  const words = [el.innerText, el.value, hit.getAttribute('aria-label'), hit.getAttribute('title')];
  const hrefs = [];
  for (let node = el; node; node = node.parentElement && node.parentElement.closest(targets)) {
    words.push(node.getAttribute('aria-label'), node.getAttribute('title'));
    if (node.hasAttribute('href')) hrefs.push(node.getAttribute('href') || '');
  }
  return {
    text: clean(el.innerText || el.getAttribute('aria-label') || el.getAttribute('title')).slice(0, 120),
    href: el.getAttribute('href') || '',
    words: words.map(clean).filter(Boolean).join(' ').slice(0, 4000),
    hrefs: hrefs.slice(0, 20),
    disabled: !!(el.disabled || el.getAttribute('aria-disabled') === 'true')
  };
})(%d, %d)"""


class Unavailable(RuntimeError):
    pass


def is_safe_click_label(text, href=""):
    """Return False if a clickable element looks destructive, transactional, or leaves HTTP(S)."""
    label = (text or "").strip()
    target = (href or "").strip()
    lower_href = target.lower()
    if any(lower_href.startswith(scheme) for scheme in DANGEROUS_SCHEMES):
        return False
    if DANGEROUS_CLICK.search(label):
        return False
    if target and DANGEROUS_CLICK.search(target):
        return False
    return bool(label or target)


def is_safe_click_target(found):
    label = " ".join(str(found.get(key) or "") for key in ("text", "words")).strip()
    links = {str(found.get("href") or "")} | {str(link or "") for link in found.get("hrefs") or []}
    return all(is_safe_click_label(label, link) for link in links)


def click_verdict(found, text, href):
    if not isinstance(found, dict) or not isinstance(found.get("hrefs") or [], list):
        return "unknown"
    if not is_safe_click_target(found):
        return "unsafe"
    if found.get("disabled") or (str(found.get("text") or ""), str(found.get("href") or "")) != (text, href):
        return "moved"
    return "click"


def build_har(requests_list, final_url, title, started_wall, redact):
    """Build a redacted HAR 1.2 JSON bytes artifact from recorded CDP network requests."""
    started_iso = datetime.fromtimestamp(started_wall, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    entries = []
    for item in requests_list or []:
        url = redact(str(item.get("url") or ""))
        method = str(item.get("method") or "GET").upper()
        status_code = int(item["status"]) if isinstance(item.get("status"), int) else 0
        body_size = int(item["bytes"]) if isinstance(item.get("bytes"), int) and item["bytes"] >= 0 else -1
        entry = {
            "startedDateTime": started_iso,
            "time": 0,
            "request": {
                "method": method,
                "url": url,
                "httpVersion": str(item.get("protocol") or "HTTP/1.1"),
                "cookies": [],
                "headers": [],
                "queryString": [],
                "headersSize": -1,
                "bodySize": -1,
            },
            "response": {
                "status": status_code,
                "statusText": str(item.get("error") or ("OK" if 200 <= status_code < 400 else "")),
                "httpVersion": str(item.get("protocol") or "HTTP/1.1"),
                "cookies": [],
                "headers": [],
                "content": {
                    "size": max(0, body_size),
                    "mimeType": str(item.get("mime") or "application/octet-stream"),
                },
                "redirectURL": "",
                "headersSize": -1,
                "bodySize": body_size,
            },
            "cache": {},
            "timings": {"send": 0, "wait": 0, "receive": 0},
            "_resourceType": str(item.get("type") or ""),
            "_initiator": str(item.get("initiator") or ""),
        }
        if item.get("certificate"):
            entry["_securityDetails"] = item["certificate"]
        entries.append(entry)
    doc = {
        "log": {
            "version": "1.2",
            "creator": {"name": "TgWitness", "version": "1"},
            "pages": [{
                "startedDateTime": started_iso,
                "id": "page_1",
                "title": redact(str(title or final_url or "")),
                "pageTimings": {},
            }],
            "entries": entries,
        }
    }
    return json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8")


def _windows_browser_candidates():
    candidates = []
    for env_var in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
        base = os.environ.get(env_var)
        if not base:
            continue
        root = Path(base)
        candidates.extend([
            root / "Google" / "Chrome" / "Application" / "chrome.exe",
            root / "Chromium" / "Application" / "chrome.exe",
            root / "Microsoft" / "Edge" / "Application" / "msedge.exe",
            root / "BraveSoftware" / "Brave-Browser" / "Application" / "brave.exe",
        ])
    pw_base = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or (Path(os.environ.get("LOCALAPPDATA", "")) / "ms-playwright"))
    with contextlib.suppress(OSError):
        for found in sorted(pw_base.glob("chromium-*/chrome-win*/chrome.exe"), reverse=True):
            candidates.append(found)
    return candidates


def browser_path():
    configured = os.environ.get("TGWITNESS_CHROMIUM", "").strip()
    if configured:
        return configured if os.path.isfile(configured) and (os.name == "nt" or os.access(configured, os.X_OK)) else None
    for name in NAMES:
        found = shutil.which(name)
        if found:
            return found
    if os.name == "nt":
        for candidate in _windows_browser_candidates():
            if candidate.is_file():
                return str(candidate)
        return None
    cache = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH") or Path.home() / ".cache" / "ms-playwright")
    with contextlib.suppress(OSError):
        for pattern in ("chromium-*/chrome-linux*/chrome", "chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium"):
            for path in sorted(cache.glob(pattern), reverse=True):
                if os.access(path, os.X_OK):
                    return str(path)
    return None


def status():
    if os.name not in ("posix", "nt"):
        return {"browser": False, "reason": PLATFORM}
    if os.name == "posix" and fcntl is None:
        return {"browser": False, "reason": PLATFORM}
    path = browser_path()
    if not path:
        return {"browser": False, "reason": MISSING}
    is_root = os.name == "posix" and hasattr(os, "geteuid") and os.geteuid() == 0
    if is_root and os.environ.get("TGWITNESS_BROWSER_NO_SANDBOX") != "1":
        return {"browser": False, "reason": ROOT, "path": path}
    window = os.name == "nt" or sys.platform == "darwin" or bool(
        os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    modes = ["passive", "crawl"] + (["interactive"] if window else [])
    return {"browser": True, "path": path, "sandbox": not is_root, "modes": modes}


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

    async def close(self):
        self.task.cancel()
        with contextlib.suppress(BaseException):
            await self.task
        with contextlib.suppress(OSError):
            os.close(self.write_fd)


class WebSocketPipe:
    """Zero-dependency RFC 6455 loopback WebSocket CDP transport (used on Windows via DevToolsActivePort)."""

    def __init__(self, reader, writer, on_event):
        self.reader, self.writer, self.on_event = reader, writer, on_event
        self.next, self.waiting, self.closed = 0, {}, False
        self._write_lock = asyncio.Lock()
        self.task = asyncio.ensure_future(self._read())

    @classmethod
    async def connect(cls, port, ws_path, on_event, timeout=15):
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection("127.0.0.1", int(port), limit=64 * 1024 * 1024), timeout)
        key = base64.b64encode(secrets.token_bytes(16)).decode("ascii")
        expected = base64.b64encode(
            hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode("ascii")).digest()
        ).decode("ascii")
        handshake = (
            f"GET {ws_path} HTTP/1.1\r\n"
            f"Host: 127.0.0.1:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        ).encode("ascii")
        writer.write(handshake)
        await writer.drain()
        raw = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout)
        lines = raw.decode("latin-1").split("\r\n")
        if "101" not in lines[0]:
            writer.close()
            raise Unavailable("Chromium DevTools WebSocket handshake failed.")
        headers = {k.strip().lower(): v.strip() for k, _, v in (line.partition(":") for line in lines[1:] if ":" in line)}
        if headers.get("sec-websocket-accept") != expected:
            writer.close()
            raise Unavailable("Chromium DevTools WebSocket accept mismatch.")
        return cls(reader, writer, on_event)

    async def _send_frame(self, opcode, payload):
        mask = secrets.token_bytes(4)
        length = len(payload)
        header = bytearray([0x80 | (opcode & 0x0F)])
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))
        header.extend(mask)
        masked = bytes(b ^ mask[i & 3] for i, b in enumerate(payload))
        async with self._write_lock:
            self.writer.write(bytes(header) + masked)
            await self.writer.drain()

    async def _read_frame(self):
        head = await self.reader.readexactly(2)
        fin = bool(head[0] & 0x80)
        opcode = head[0] & 0x0F
        masked = bool(head[1] & 0x80)
        length = head[1] & 0x7F
        if length == 126:
            length = struct.unpack("!H", await self.reader.readexactly(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", await self.reader.readexactly(8))[0]
        if length > 64 * 1024 * 1024:
            raise ValueError("CDP WebSocket frame too large")
        mask = await self.reader.readexactly(4) if masked else None
        data = await self.reader.readexactly(length) if length else b""
        if mask is not None:
            data = bytes(b ^ mask[i & 3] for i, b in enumerate(data))
        return fin, opcode, data

    async def _read(self):
        fragments = []
        try:
            while True:
                fin, opcode, data = await self._read_frame()
                if opcode == 0x8:  # close
                    break
                if opcode == 0x9:  # ping
                    await self._send_frame(0xA, data)
                    continue
                if opcode == 0xA:  # pong
                    continue
                if opcode in (0x0, 0x1, 0x2):
                    fragments.append(data)
                    if not fin:
                        continue
                    raw = b"".join(fragments)
                    fragments.clear()
                    message = json.loads(raw)
                    if "id" in message:
                        future = self.waiting.pop(message["id"], None)
                        if future and not future.done():
                            future.set_result(message)
                    else:
                        with contextlib.suppress(Exception):
                            self.on_event(message)
        except (OSError, ValueError, asyncio.IncompleteReadError):
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
        await self._send_frame(0x1, json.dumps(message).encode("utf-8"))
        answer = await asyncio.wait_for(future, timeout)
        if "error" in answer:
            raise RuntimeError(answer["error"].get("message") or method)
        return answer.get("result") or {}

    async def close(self):
        self.task.cancel()
        with contextlib.suppress(BaseException):
            await self.task
        with contextlib.suppress(OSError):
            self.writer.close()


async def _wait_devtools_port(folder, process, timeout=15):
    active_file = Path(folder) / "DevToolsActivePort"
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.returncode is not None:
            raise Unavailable("Chromium exited before DevToolsActivePort appeared.")
        with contextlib.suppress(OSError):
            if active_file.is_file():
                lines = [line.strip() for line in active_file.read_text("utf-8", "replace").splitlines() if line.strip()]
                if len(lines) >= 2 and lines[0].isdigit() and lines[1].startswith("/"):
                    return int(lines[0]), lines[1]
        await asyncio.sleep(0.1)
    raise Unavailable("Timed out waiting for Chromium DevToolsActivePort.")


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


async def _capture_state(call, redact, files, label):
    """Capture PNG screenshot, redacted HTML, and redacted MHTML snapshot for the current page state."""
    captured = False
    with contextlib.suppress(Exception):
        shot = await call("Page.captureScreenshot", {"format": "png"}, timeout=20)
        files.append(("screenshot", "image/png", base64.b64decode(shot["data"]), label))
        captured = True
    with contextlib.suppress(Exception):
        html = await call("Runtime.evaluate", {"expression": "document.documentElement.outerHTML",
                                               "returnByValue": True}, timeout=15)
        page = ((html.get("result") or {}).get("value") or "").encode("utf-8")[:MAX_PAGE_BYTES]
        if page:
            files.append(("page", "text/html", redact(page.decode("utf-8", "replace")).encode("utf-8"), label))
            captured = True
    with contextlib.suppress(Exception):
        snap = await call("Page.captureSnapshot", {"format": "mhtml"}, timeout=20)
        mhtml_bytes = redact(snap.get("data") or "").encode("utf-8")[:MAX_MHTML_BYTES]
        if mhtml_bytes:
            files.append(("mhtml", "multipart/related", mhtml_bytes, label))
            captured = True
    return captured


async def _state_digest(call):
    with contextlib.suppress(Exception):
        res = await call("Runtime.evaluate", {"expression": STATE_SIG_JS, "returnByValue": True}, timeout=10)
        raw = (res.get("result") or {}).get("value") or ""
        if raw:
            return hashlib.sha256(raw.encode("utf-8", "replace")).hexdigest()
    return None


def _click_key(item):
    return str(item.get("text") or ""), str(item.get("href") or "")


def _click_point(item):
    try:
        x, y = int(item.get("x") or 0), int(item.get("y") or 0)
    except (TypeError, ValueError):
        return None
    return (x, y) if x > 0 and y > 0 else None


def _note_blocked(blocked, redact, text, href):
    item = {"text": redact(text)[:80], "href": redact(href)[:120]}
    if (text or href) and len(blocked) < 50 and item not in blocked:
        blocked.append(item)


def _merge_clicks(fresh, queue, tried):
    merged, keys = [], set(tried)
    for item in fresh + queue:
        key = _click_key(item)
        if key not in keys:
            keys.add(key)
            merged.append(item)
    return merged


async def _isolated(call, expression, worlds=None):
    worlds = {} if worlds is None else worlds
    try:
        tree = await call("Page.getFrameTree", timeout=10)
        frame = tree["frameTree"]["frame"]
        key = (frame["id"], frame.get("loaderId"))
        context = worlds.get(key)
        if context is None:
            world = await call("Page.createIsolatedWorld", {"frameId": frame["id"], "worldName": WORLD}, timeout=10)
            context = world["executionContextId"]
            if not isinstance(context, int) or isinstance(context, bool):
                return None
            worlds.clear()
            worlds[key] = context
        found = await call("Runtime.evaluate", {"expression": expression, "contextId": context,
                                                "returnByValue": True}, timeout=10)
    except Exception:
        worlds.clear()
        return None
    if not isinstance(found, dict) or found.get("exceptionDetails"):
        return None
    return (found.get("result") or {}).get("value")


async def _clickables(call, worlds=None):
    try:
        items = json.loads(await _isolated(call, CLICKABLES_JS, worlds) or "[]")
    except (TypeError, ValueError):
        return []
    return [item for item in items if isinstance(item, dict)] if isinstance(items, list) else []


async def _element_at(call, x, y, worlds=None):
    value = await _isolated(call, ELEMENT_AT_JS % (x, y), worlds)
    return value if isinstance(value, dict) else None


async def _crawl(call, redact, files, max_states, deadline, blocked):
    seen = set()
    current = await _state_digest(call)
    if current:
        seen.add(current)
    captured = 1 if await _capture_state(call, redact, files, "State 1 · initial") else 0
    worlds = {}
    queue, tried, clicks = await _clickables(call, worlds), set(), 0
    while queue and captured < max_states and clicks < MAX_CLICKS and time.monotonic() <= deadline:
        candidate = queue.pop(0)
        key = _click_key(candidate)
        if key in tried:
            continue
        text_label, href_val = key
        if not is_safe_click_label(" ".join((text_label, str(candidate.get("words") or ""))).strip(), href_val):
            tried.add(key)
            _note_blocked(blocked, redact, text_label, href_val)
            continue
        point = _click_point(candidate)
        if point is None:
            tried.add(key)
            continue
        found = await _element_at(call, *point, worlds)
        verdict = click_verdict(found, text_label, href_val)
        if verdict == "unsafe":
            _note_blocked(blocked, redact, *_click_key(found))
        if verdict != "click":
            continue
        tried.add(key)
        clicks += 1
        try:
            for kind in ("mousePressed", "mouseReleased"):
                await call("Input.dispatchMouseEvent", {"type": kind, "x": point[0], "y": point[1], "button": "left",
                                                        "clickCount": 1}, timeout=10)
        except Exception:
            continue
        await asyncio.sleep(CLICK_SETTLE)
        sig = await _state_digest(call)
        if sig and sig not in seen:
            seen.add(sig)
            captured += 1
            short = redact(text_label)[:40] or "step"
            await _capture_state(call, redact, files, f"State {captured} · {short}")
        if sig is None or sig != current:
            queue = _merge_clicks(await _clickables(call, worlds), queue, tried)
        current = sig
    return captured


async def capture(url, route, init_data=None, settle=SHOTS, *, mode="passive", max_states=8):
    """Open url and return (facts, files). Files are (role, mime, bytes, label).

    Modes:
      - passive: headless load, timed + full-page screenshots, HTML, MHTML, HAR, scripts.
      - crawl: headless load + safe non-destructive navigation clicks (blocking payment/wallet/delete actions),
               deduplicated states up to max_states (PNG + HTML + MHTML per state) + HAR.
      - interactive: visible desktop browser window through the same SSRF-safe proxy; records PNG + HTML + MHTML
                     on each distinct screen transition until closed, max_states, or timeout.
    """
    if mode not in ("passive", "crawl", "interactive"):
        raise Unavailable("Unsupported capture mode: " + str(mode))
    if urlsplit(url).scheme not in ("http", "https"):
        raise Unavailable("Only http and https Mini App addresses can be opened")
    state = status()
    if not state["browser"]:
        raise Unavailable(state["reason"])
    if mode not in state.get("modes", ()):
        raise Unavailable(NO_WINDOW)
    try:
        await asyncio.wait_for(_browsers.acquire(), BROWSER_WAIT)
    except TimeoutError:
        raise Unavailable("Other Mini App captures are still running on this server. "
                          "Try again when they finish.") from None
    try:
        return await _capture(url, route, init_data, settle, state, mode, max_states)
    finally:
        _browsers.release()


async def _capture(url, route, init_data, settle, state, mode, max_states):
    max_states = max(1, min(20, int(max_states or 8)))
    redact = Redactor(init_data)
    gate, quiet = Gate(route), Gate(route, refuse=True)
    session_state = Session(redact)
    folder = tempfile.mkdtemp(prefix="tgwitness-webapp-")
    process = pipe = transport = None
    files, errors, facts, version = [], [], {}, ""
    started, started_wall = time.monotonic(), time.time()
    states_captured = 0
    blocked_clicks = []
    use_ws = os.name == "nt"
    interactive = mode == "interactive"
    interactive_limit = max(30, min(600, int(os.environ.get("TGWITNESS_WEBAPP_INTERACTIVE_TIMEOUT", INTERACTIVE_TIMEOUT))))
    try:
        port, idle = await gate.start(), await quiet.start()
        arguments = [state["path"]]
        if not interactive:
            arguments.append("--headless=new")
        arguments.append("--remote-debugging-port=0" if use_ws else "--remote-debugging-pipe")
        arguments.extend([
            "--user-data-dir=" + folder,
            "--no-first-run", "--no-default-browser-check", "--disable-extensions", "--disable-sync",
            "--disable-background-networking", "--disable-component-update", "--disable-default-apps",
            "--disable-dev-shm-usage", "--mute-audio",
            "--disable-features=Translate,MediaRouter,OptimizationHints,"
            "AutofillServerCommunication,CertificateTransparencyComponentUpdater,InterestFeedContentSuggestions",
            "--deny-permission-prompts", "--password-store=basic", "--use-mock-keychain",
            "--disable-client-side-phishing-detection", "--disable-domain-reliability", "--no-pings",
            "--disable-breakpad", "--safebrowsing-disable-auto-update", "--disable-field-trial-config",
            f"--proxy-server=http://127.0.0.1:{idle}", "--proxy-bypass-list=<-loopback>",
            "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
            "--webrtc-ip-handling-policy=disable_non_proxied_udp",
            f"--window-size={VIEWPORT['width']},{VIEWPORT['height']}",
        ])
        if not interactive:
            arguments.extend(["--disable-gpu", "--hide-scrollbars"])
        arguments.append("about:blank")
        is_root = os.name == "posix" and hasattr(os, "geteuid") and os.geteuid() == 0
        if is_root:
            arguments.insert(1, "--no-sandbox")

        if use_ws:
            with open(os.path.join(folder, "browser.log"), "wb") as log:
                process = await asyncio.create_subprocess_exec(
                    *arguments, stdin=asyncio.subprocess.DEVNULL, stdout=log, stderr=log)
            ws_port, ws_path = await _wait_devtools_port(folder, process, timeout=15)
            pipe = await WebSocketPipe.connect(ws_port, ws_path, session_state.handle, timeout=15)
        else:
            loose = []
            try:
                loose.extend(os.pipe())
                loose.extend(os.pipe())
                to_child, from_parent, from_child, to_parent = loose
                to_child = loose[0] = high(to_child)
                to_parent = loose[3] = high(to_parent)

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
                for fd in (to_child, to_parent):
                    loose.remove(fd)
                    os.close(fd)
                reader = asyncio.StreamReader(limit=64 * 1024 * 1024)
                loop = asyncio.get_running_loop()
                child_out = os.fdopen(from_child, "rb", 0)
                loose.remove(from_child)
                try:
                    transport, _ = await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), child_out)
                except BaseException:
                    child_out.close()
                    raise
                pipe = Pipe(reader, from_parent, session_state.handle)
                loose.remove(from_parent)
            except BaseException:
                for fd in loose:
                    with contextlib.suppress(OSError):
                        os.close(fd)
                raise

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
        if not interactive:
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

        dismiss = None if interactive else asyncio.ensure_future(dialogs())
        try:
            navigation = await call("Page.navigate", {"url": url}, timeout=LOAD_TIMEOUT)
            if navigation.get("errorText"):
                errors.append({"component": "navigation", "error": navigation["errorText"]})
            with contextlib.suppress(asyncio.TimeoutError):
                await asyncio.wait_for(session_state.loaded.wait(), LOAD_TIMEOUT)

            if mode == "passive":
                waited = 0
                for moment in settle:
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
                    html = await call("Runtime.evaluate", {"expression": "document.documentElement.outerHTML",
                                                           "returnByValue": True}, timeout=15)
                    page = ((html.get("result") or {}).get("value") or "").encode("utf-8")[:MAX_PAGE_BYTES]
                    if page:
                        files.append(("page", "text/html", redact(page.decode("utf-8", "replace")).encode("utf-8"),
                                      "Page after loading"))
                with contextlib.suppress(Exception):
                    snap = await call("Page.captureSnapshot", {"format": "mhtml"}, timeout=20)
                    mhtml_bytes = redact(snap.get("data") or "").encode("utf-8")[:MAX_MHTML_BYTES]
                    if mhtml_bytes:
                        files.append(("mhtml", "multipart/related", mhtml_bytes, "Page after loading"))
                states_captured = 1
            elif mode == "crawl":
                await asyncio.sleep(min(2, settle[0]) if settle else 1)
                states_captured = await _crawl(call, redact, files, max_states, started + TOTAL_TIMEOUT, blocked_clicks)
            else:  # interactive
                await asyncio.sleep(1.5)
                seen_states = set()
                sig = await _state_digest(call)
                if sig:
                    seen_states.add(sig)
                if await _capture_state(call, redact, files, "Interactive 1 · initial"):
                    states_captured = 1
                while (process.returncode is None and not pipe.closed
                       and states_captured < max_states
                       and time.monotonic() - started < interactive_limit):
                    await asyncio.sleep(0.8)
                    if process.returncode is not None or pipe.closed:
                        break
                    sig = await _state_digest(call)
                    if sig and sig not in seen_states:
                        seen_states.add(sig)
                        states_captured += 1
                        await _capture_state(call, redact, files, f"Interactive {states_captured}")

            if not pipe.closed:
                with contextlib.suppress(Exception):
                    found = await call("Runtime.evaluate", {"expression": PAGE_FACTS, "returnByValue": True}, timeout=15)
                    facts = json.loads((found.get("result") or {}).get("value") or "{}")
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
            if dismiss is not None:
                dismiss.cancel()
                with contextlib.suppress(BaseException):
                    await dismiss
        if not pipe.closed:
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
            await pipe.close()
        if transport:
            transport.close()
        await gate.close()
        await quiet.close()
        shutil.rmtree(folder, ignore_errors=True)
    requests = [session_state.requests[key] for key in session_state.order]
    final_url = public_address(redact(facts.get("href") or session_state.final_url or ""))
    title = redact(facts.get("title") or "")[:300]
    har_bytes = build_har(requests, final_url, title, started_wall, redact)
    if har_bytes:
        files.append(("har", "application/json", har_bytes, "Network HAR 1.2"))
    asked = {(urlsplit(item.get("url") or "").hostname or "").lower()
             for item in requests + list(session_state.sockets.values())}
    hosts = sorted(gate.hosts.values(), key=lambda item: item["host"])
    own = [item for item in hosts if item["host"] in BROWSER_HOSTS and item["host"] not in asked]
    is_root = os.name == "posix" and hasattr(os, "geteuid") and os.geteuid() == 0
    return {
        "browser": version, "sandbox": not is_root, "mode": mode, "states_captured": states_captured,
        "blocked_clicks": blocked_clicks,
        "duration_ms": int((time.monotonic() - started) * 1000),
        "final_url": final_url,
        "title": title, "text": redact(facts.get("text") or ""),
        "links": redact(facts.get("links") or []), "forms": redact(facts.get("forms") or []),
        "frames": redact(facts.get("frames") or []), "inputs": redact(facts.get("inputs") or []),
        "webapp": facts.get("webapp"), "requests": requests, "sockets": list(session_state.sockets.values()),
        "telegram_events": session_state.events, "console": session_state.console,
        "dialogs": session_state.dialogs, "popups": session_state.popups, "downloads": session_state.downloads,
        "connections": [item for item in hosts if item not in own], "browser_connections": own, "blocked": gate.blocked,
        "dropped": session_state.dropped, "errors": errors}, files
