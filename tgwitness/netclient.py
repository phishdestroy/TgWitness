"""Minimal HTTP/1.1 client over the workspace route (direct, SOCKS5 or HTTP CONNECT).

Used for timestamp services and S3. It never falls back to a direct connection: MTProxy
carries only Telegram traffic, so other requests are refused on that route.
"""
import asyncio
import ssl
from contextlib import suppress
from urllib.parse import urlsplit

from python_socks import ProxyType
from python_socks.async_.asyncio import Proxy


class RouteError(Exception):
    pass


class HTTPError(ValueError):
    def __init__(self, status, body=b""):
        super().__init__("HTTP " + str(status))
        self.status, self.body = status, body


async def open_stream(url, network, timeout):
    parts = urlsplit(url)
    host, port = parts.hostname, parts.port or (443 if parts.scheme == "https" else 80)
    tls = ssl.create_default_context() if parts.scheme == "https" else None
    if network.kind == "direct":
        return await asyncio.wait_for(
            asyncio.open_connection(host, port, ssl=tls, server_hostname=host if tls else None), timeout)
    if network.kind == "mtproxy":
        raise RouteError("MTProxy carries only Telegram traffic; choose Direct, SOCKS5 or HTTP in "
                         "Connection settings for this request.")
    proxy = Proxy(ProxyType.SOCKS5 if network.kind == "socks5" else ProxyType.HTTP, network.host,
                  network.port, network.username or None, network.password or None, rdns=True)
    sock = await proxy.connect(dest_host=host, dest_port=port, timeout=timeout)
    return await asyncio.wait_for(
        asyncio.open_connection(sock=sock, ssl=tls, server_hostname=host if tls else None), timeout)


async def request(method, url, network, headers=None, body=b"", length=None, sink=None,
                  timeout=60, limit=1024 * 1024):
    """Send one request. body: bytes or an async iterator of bytes (then length is required).

    Returns (status, headers, data); with sink (an async callable) the body is streamed to it
    and data is b"". Non-2xx statuses raise HTTPError carrying the (bounded) response body.
    """
    parts = urlsplit(url)
    reader, writer = await open_stream(url, network, timeout)
    try:
        path = (parts.path or "/") + ("?" + parts.query if parts.query else "")
        size = len(body) if isinstance(body, (bytes, bytearray)) else length
        lines = [method + " " + path + " HTTP/1.1", "Host: " + parts.netloc, "User-Agent: TgWitness",
                 "Connection: close"]
        if size or method in ("PUT", "POST"):
            lines.append("Content-Length: " + str(size or 0))
        lines += [k + ": " + v for k, v in (headers or {}).items()]
        writer.write(("\r\n".join(lines) + "\r\n\r\n").encode("ascii"))
        if isinstance(body, (bytes, bytearray)):
            writer.write(body)
        else:
            async for chunk in body:
                writer.write(chunk)
                await asyncio.wait_for(writer.drain(), timeout)
        await asyncio.wait_for(writer.drain(), timeout)
        head = (await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout)).decode("latin-1").split("\r\n")
        status = int(head[0].split()[1])
        fields = {k.strip().lower(): v.strip() for k, _, v in (h.partition(":") for h in head[1:] if h)}
        ok = 200 <= status < 300
        received, data = 0, b""

        async def take(chunk):
            nonlocal received, data
            received += len(chunk)
            if sink and ok:
                await sink(chunk)
            elif received > limit:
                raise ValueError("Response too large")
            else:
                data += chunk

        if method == "HEAD" or status in (204, 304):
            pass
        elif fields.get("transfer-encoding", "").lower() == "chunked":
            while True:
                count = int((await asyncio.wait_for(reader.readuntil(b"\r\n"), timeout)).split(b";")[0], 16)
                if count == 0:
                    break
                await take((await asyncio.wait_for(reader.readexactly(count + 2), timeout))[:-2])
        elif "content-length" in fields:
            remaining = int(fields["content-length"])
            while remaining:
                chunk = await asyncio.wait_for(reader.read(min(remaining, 1024 * 1024)), timeout)
                if not chunk:
                    raise ValueError("Connection closed early")
                remaining -= len(chunk)
                await take(chunk)
        else:
            while chunk := await asyncio.wait_for(reader.read(1024 * 1024), timeout):
                await take(chunk)
        if not ok:
            raise HTTPError(status, data[:2000])
        return status, fields, data
    finally:
        writer.close()
        with suppress(Exception):
            await writer.wait_closed()
