"""CONNECT-only bridge to one configured upstream; never connects to destinations directly."""
import argparse
import base64
import ipaddress
import json
import re
import select
import socket
import socketserver
from pathlib import Path
from urllib.parse import urlsplit

# Same ranges as tgwitness/topology.py; this module stays standard-library only.
TELEGRAM_NETWORKS = tuple(ipaddress.ip_network(value) for value in (
    "91.105.192.0/23", "91.108.4.0/22", "91.108.8.0/22", "91.108.12.0/22", "91.108.16.0/22", "91.108.20.0/22",
    "91.108.56.0/22", "95.161.64.0/20", "149.154.160.0/20", "185.76.151.0/24",
    "2001:67c:4e8::/48", "2001:b28:f23c::/47", "2001:b28:f23f::/48", "2a0a:f280::/32"))
NAT64 = ipaddress.ip_network("64:ff9b::/96")


def configuration(raw):
    if not isinstance(raw, dict) or set(raw) - {"server", "username", "password"}:
        raise ValueError("Invalid upstream configuration")
    parsed = urlsplit(raw.get("server", ""))
    if (parsed.scheme not in {"http", "socks5"} or not parsed.hostname or not parsed.port
            or parsed.username is not None or parsed.password is not None
            or parsed.path not in {"", "/"} or parsed.query or parsed.fragment
            or any(ord(c) < 33 or c == "\\" for c in raw["server"])):
        raise ValueError("Configure one explicit HTTP or SOCKS5 upstream")
    for name in ("username", "password"):
        if not isinstance(raw.get(name, ""), str) or len(raw.get(name, "").encode()) > 255:
            raise ValueError("Invalid upstream credentials")
    return {"scheme": parsed.scheme, "host": parsed.hostname, "port": parsed.port,
            "username": raw.get("username", ""), "password": raw.get("password", "")}


def destination(authority):
    if not re.fullmatch(r"[A-Za-z0-9.\[\]:-]{1,260}", authority):
        raise ValueError("Invalid CONNECT authority")
    parsed = urlsplit("//" + authority)
    if not parsed.hostname or parsed.port != 443:
        raise ValueError("Only HTTPS connections are permitted")
    host = parsed.hostname.lower()
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        ip = None
    if ip is not None:
        if ip.version == 6:
            ip = ip.ipv4_mapped or ip.sixtofour or (
                ipaddress.IPv4Address(int(ip) & 0xFFFFFFFF) if ip in NAT64 else None) or ip
        if not any(ip in network for network in TELEGRAM_NETWORKS):
            raise ValueError("Address destinations are limited to Telegram data centres")
        return host, 443
    if ":" in host or re.fullmatch(r"[0-9.]+", host):
        raise ValueError("Invalid destination")
    if not (host in {"www.cloudflare.com", "api.cloudflare.com", "api.drand.sh"}
            or host == "telegram.org" or host.endswith(".telegram.org")
            or host == "t.me" or host.endswith(".t.me")
            or host.endswith(".telegram-cdn.org")):
        raise ValueError("Destination is outside the official-client allowlist")
    return host, 443


def exact(stream, count):
    result = b""
    while len(result) < count:
        part = stream.recv(count - len(result))
        if not part:
            raise OSError("Upstream closed")
        result += part
    return result


def connect_upstream(config, host, port):
    upstream = socket.create_connection((config["host"], config["port"]), timeout=10)
    try:
        if config["scheme"] == "http":
            target = ("[" + host + "]" if ":" in host else host) + ":" + str(port)
            auth = ""
            if config["username"] or config["password"]:
                credential = base64.b64encode((config["username"] + ":" + config["password"]).encode()).decode()
                auth = "Proxy-Authorization: Basic " + credential + "\r\n"
            upstream.sendall(("CONNECT " + target + " HTTP/1.1\r\nHost: " + target + "\r\n" + auth + "\r\n").encode("ascii"))
            response = bytearray()
            while not response.endswith(b"\r\n\r\n"):
                if len(response) >= 16384:
                    raise OSError("Upstream response too large")
                response.extend(exact(upstream, 1))
            if not re.match(rb"HTTP/1\.[01] 200(?: |\r)", response):
                raise OSError("Upstream refused connection")
        else:
            authenticated = bool(config["username"] or config["password"])
            upstream.sendall(b"\x05\x01" + (b"\x02" if authenticated else b"\x00"))
            if exact(upstream, 2) != b"\x05" + (b"\x02" if authenticated else b"\x00"):
                raise OSError("Upstream authentication unavailable")
            if authenticated:
                user, password = config["username"].encode(), config["password"].encode()
                upstream.sendall(b"\x01" + bytes([len(user)]) + user + bytes([len(password)]) + password)
                if exact(upstream, 2) != b"\x01\x00":
                    raise OSError("Upstream authentication refused")
            name = host.encode("idna")
            if len(name) > 255:
                raise ValueError("Destination too long")
            upstream.sendall(b"\x05\x01\x00\x03" + bytes([len(name)]) + name + port.to_bytes(2, "big"))
            reply = exact(upstream, 4)
            if reply[:3] != b"\x05\x00\x00" or reply[3] not in {1, 3, 4}:
                raise OSError("Upstream refused connection")
            size = {1: 4, 4: 16}.get(reply[3])
            if size is None:
                size = exact(upstream, 1)[0]
            exact(upstream, size + 2)
        upstream.settimeout(None)
        return upstream
    except BaseException:
        upstream.close()
        raise


class Bridge(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True
    block_on_close = False


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        self.connection.settimeout(10)
        upstream = None
        established = False
        try:
            line = self.rfile.readline(4097)
            if len(line) > 4096:
                raise ValueError("Request too long")
            method, target, version = line.decode("ascii").strip().split(" ")
            if method != "CONNECT" or version not in {"HTTP/1.0", "HTTP/1.1"}:
                raise ValueError("CONNECT required")
            count = 0
            while True:
                header = self.rfile.readline(4097)
                count += len(header)
                if count > 16384 or not header or len(header) > 4096:
                    raise ValueError("Invalid request headers")
                if header == b"\r\n":
                    break
            host, port = destination(target)
            upstream = connect_upstream(self.server.upstream, host, port)
            self.wfile.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            self.wfile.flush()
            established = True
            self.connection.settimeout(None)
            while True:
                readable, _, _ = select.select([self.connection, upstream], [], [], 300)
                if not readable:
                    break
                for source in readable:
                    data = source.recv(65536)
                    if not data:
                        return
                    (upstream if source is self.connection else self.connection).sendall(data)
        except (OSError, ValueError, UnicodeError):
            if not established:
                try:
                    self.wfile.write(b"HTTP/1.1 502 Proxy unavailable\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
                except OSError:
                    pass
        finally:
            if upstream is not None:
                upstream.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=3128)
    args = parser.parse_args()
    raw = args.config.read_bytes()
    if len(raw) > 8192:
        raise ValueError("Configuration too large")
    with Bridge((args.host, args.port), Handler) as server:
        server.upstream = configuration(json.loads(raw))
        server.serve_forever()


if __name__ == "__main__":
    main()
