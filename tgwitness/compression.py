import gzip
import zlib

COMPRESSIBLE = (b"text/javascript", b"application/javascript", b"text/css", b"text/html", b"image/svg+xml")
SUFFIXES = (".js", ".css", ".svg", ".html")
MINIMUM = 1024
CACHE_LIMIT = 64


def accepts_gzip(headers):
    for name, value in headers:
        if name == b"accept-encoding":
            for part in value.decode("latin-1").split(","):
                token, _, params = part.strip().partition(";")
                if token.strip().lower() in ("gzip", "x-gzip"):
                    quality = params.replace(" ", "").lower()
                    return quality not in ("q=0", "q=0.0", "q=0.00", "q=0.000")
    return False


def eligible(path):
    if path.startswith(("/api/", "/profiles/")):
        return False
    last = path.rsplit("/", 1)[-1]
    return "." not in last or path == "/locale.js" or last.endswith(SUFFIXES)


class Compression:
    def __init__(self, app):
        self.app = app
        self.cache = {}

    async def __call__(self, scope, receive, send):
        if (scope["type"] != "http" or scope["method"] != "GET" or not eligible(scope["path"])
                or not accepts_gzip(scope["headers"])):
            return await self.app(scope, receive, send)
        held = {}
        chunks = []

        async def wrapped(message):
            if message["type"] == "http.response.start":
                headers = {name.lower(): value for name, value in message["headers"]}
                kind = headers.get(b"content-type", b"").split(b";")[0].strip().lower()
                if (message["status"] == 200 and kind in COMPRESSIBLE and b"content-encoding" not in headers
                        and b"content-range" not in headers):
                    held["start"] = message
                    return
                await send(message)
                return
            if "start" not in held:
                await send(message)
                return
            chunks.append(message.get("body", b""))
            if message.get("more_body"):
                return
            await self.finish(held["start"], b"".join(chunks), send)

        await self.app(scope, receive, wrapped)

    async def finish(self, start, body, send):
        headers = [(name, value) for name, value in start["headers"]
                   if name.lower() not in (b"content-length", b"content-encoding")]
        vary = [value for name, value in headers if name.lower() == b"vary"]
        if not any(b"accept-encoding" in value.lower() for value in vary):
            headers.append((b"vary", b"Accept-Encoding"))
        if len(body) >= MINIMUM:
            key = (len(body), zlib.crc32(body))
            packed = self.cache.get(key)
            if packed is None:
                packed = gzip.compress(body, 6, mtime=0)
                if len(self.cache) >= CACHE_LIMIT:
                    self.cache.pop(next(iter(self.cache)))
                self.cache[key] = packed
            if len(packed) < len(body):
                body = packed
                headers = [(name, b"W/" + value if name.lower() == b"etag" and not value.startswith(b"W/") else value)
                           for name, value in headers]
                headers.append((b"content-encoding", b"gzip"))
        headers.append((b"content-length", str(len(body)).encode()))
        await send({"type": "http.response.start", "status": start["status"], "headers": headers})
        await send({"type": "http.response.body", "body": body})
