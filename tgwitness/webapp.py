import asyncio
import hashlib
import re
from urllib.parse import parse_qs, urljoin, urlsplit

from telethon import errors, utils
from telethon.tl import functions, types

from . import interactions, netclient, webapp_browser
from .indicators import Indicators
from .keyboard import of_payload
from .security import private_write
from .store import utcnow
from .telegram_client import FLOOD_ERRORS

MAX_BYTES = 4 * 1024**2
MAX_ENDPOINTS = 500
MAX_SCRIPTS = 12
MAX_LINKS = 200
MAX_INDICATORS = 400
PLATFORM = "android"
SOURCE = "mini app"
FILE_KIND = "webapp.file"
LAUNCH_MEANING = ("Telegram returned the address this mini application is opened at. Asking for it is an account "
                  "action recorded in the journal: the bot learns that this account opened it. The signed launch data "
                  "in the address works as a login to the application for a while, so it is not recorded.")
INSPECT_MEANING = ("One response fetched at this time, parsed for the addresses it references. A mini application can "
                   "load different addresses later, for another visitor or after its operator changes it. Referenced "
                   "addresses are not confirmed to exist or to have been contacted.")
CAPTURE_MEANING = ("The mini application as a headless Chromium with a phone screen loaded it once, at this time: every "
                   "request, WebSocket frame, Telegram call and dialog, the address of each window it tried to open "
                   "(windows are not loaded), screenshots and the scripts it ran. Another visitor, time or address "
                   "can be served differently. Requests, frames and calls are capped; the counts of dropped items "
                   "are recorded.")
ROUTE_MEANING = ("Fetched through this workspace's route for requests outside Telegram. A direct route would show the "
                 "operator's address to the application's host.")
ATTRIBUTES = re.compile(r"""(?i)\b(?:src|href|action|data-src|data-url|poster|formaction)\s*=\s*["']([^"'\s>]{1,2048})""")
CSS_URL = re.compile(r"""(?i)url\(\s*["']?([^"')\s]{1,2048})""")
IMPORTS = re.compile(r"""(?i)\bimport\s*\(?\s*["']([^"'\s]{1,2048})["']""")
CALLS = re.compile(r"""(?i)\b(?:fetch|open|axios(?:\.\w+)?|navigator\.sendBeacon|EventSource|WebSocket)\s*\(\s*["']([^"'\s]{1,2048})["']""")
LITERALS = re.compile(r"""["'`](https?://[^"'`\s]{3,2048}|/[A-Za-z0-9_\-./]{1,512})["'`]""")
SOCKET = re.compile(r"(?i)\bwss?://[^\s\"'`<>]{3,2048}")
APP_LINK = re.compile(r"(?i)(?<![\w.@/-])(?:https?://)?(?:t\.me|telegram\.me|telegram\.dog)/([A-Za-z][A-Za-z0-9_]{1,30}bot)"
                      r"(?:/([A-Za-z][A-Za-z0-9_]{2,63}))?/?(\?[^\s<>\"'`]*)?")
ASKS = {"web_app_request_phone": "phone", "web_app_request_write_access": "write_access",
        "web_app_open_invoice": "payment", "web_app_open_link": "link", "web_app_open_tg_link": "telegram_link",
        "web_app_data_send": "data", "web_app_send_prepared_message": "message", "web_app_switch_inline_query": "inline",
        "web_app_request_file_download": "download", "web_app_read_text_from_clipboard": "clipboard",
        "web_app_request_location": "location", "web_app_request_emoji_status_access": "emoji_status",
        "web_app_set_emoji_status": "emoji_status", "web_app_share_to_story": "story", "web_app_open_popup": "popup",
        "web_app_biometry_request_access": "biometry", "web_app_add_to_home_screen": "home_screen"}


def buttons(payload):
    markup = of_payload(payload)
    found = []
    for row in (markup or {}).get("rows") or []:
        for button in row:
            if button.get("type") == "web_app":
                found.append({"text": button.get("text") or "", "url": button.get("url")})
    return found


def in_messages(store, chat_id, limit=200):
    found = {}
    for event in store.events(chat_id=chat_id, limit=limit):
        for button in buttons(event.get("payload")):
            if button["url"] and button["url"] not in found:
                found[button["url"]] = {**button, "seq": event["seq"], "message_id": event.get("message_id")}
    return list(found.values())


def app_link(url):
    match = APP_LINK.fullmatch((url or "").strip().rstrip(".,;:!?)»"))
    if not match:
        return None
    query = parse_qs((match.group(3) or "?")[1:], keep_blank_values=True)
    if not match.group(2) and "startapp" not in query:
        return None
    start = (query.get("startapp") or [""])[0][:512] or None
    return {"bot": match.group(1), "app": match.group(2), "start": start,
            "url": "https://t.me/" + match.group(1) + ("/" + match.group(2) if match.group(2) else "")
            + ("?startapp" + ("=" + start if start else "") if "startapp" in query else "")}


def texts_of(payload):
    payload = payload or {}
    yield payload.get("text") or ""
    for entity in ((payload.get("raw") or {}).get("entities") or []):
        if isinstance(entity, dict) and isinstance(entity.get("url"), str):
            yield entity["url"]
    for row in (of_payload(payload) or {}).get("rows") or []:
        for button in row:
            if button.get("type") == "url" and button.get("url"):
                yield button["url"]


def entries(store, chat_id, limit=300):
    """Mini applications this chat offers, from saved records only; nothing is contacted."""
    found, links, seen = [], [], set()
    for event in store.events(chat_id=chat_id, limit=limit):
        payload = event.get("payload") or {}
        markup = of_payload(payload)
        for row_index, row in enumerate((markup or {}).get("rows") or []):
            for column, button in enumerate(row):
                if button.get("type") == "web_app" and button.get("url") and (button["url"], button["text"]) not in seen:
                    seen.add((button["url"], button["text"]))
                    found.append({"type": "button", "seq": event["seq"], "message_id": event.get("message_id"),
                                  "row": row_index, "column": column, "inline": bool(markup.get("inline")),
                                  "text": button.get("text") or "", "url": button["url"], "at": event.get("observed_at")})
        for text in texts_of(payload):
            for match in APP_LINK.finditer(text or ""):
                link = app_link(match.group(0))
                if link and link["url"] not in seen:
                    seen.add(link["url"])
                    links.append({"type": "link", **link, "seq": event["seq"], "message_id": event.get("message_id"),
                                  "at": event.get("observed_at")})
    return found + links


def captures(store, chat_id, limit=50):
    rows = store.events(chat_id=chat_id, kind="webapp.captured", limit=limit)
    return [{"seq": row["seq"], "at": row["observed_at"], **{key: (row["payload"] or {}).get(key) for key in (
        "launch_seq", "entry", "method", "address", "final_url", "title", "bot", "duration_ms", "third_party_hosts",
        "asks", "files", "summary")}} for row in rows]


def init_data_of(address):
    fragment = urlsplit(address or "").fragment
    return (parse_qs(fragment, keep_blank_values=True).get("tgWebAppData") or [None])[0]


def same_origin(base, value):
    origin, target = urlsplit(base), urlsplit(value)
    return (target.scheme, target.netloc) == (origin.scheme, origin.netloc)


def endpoints(body, base):
    text = body.decode("utf-8", "replace") if isinstance(body, (bytes, bytearray)) else str(body)
    found, order = {}, 0
    for source, pattern in (("attribute", ATTRIBUTES), ("style", CSS_URL), ("import", IMPORTS),
                            ("call", CALLS), ("literal", LITERALS), ("socket", SOCKET)):
        for match in pattern.finditer(text):
            value = (match.group(1) if pattern is not SOCKET else match.group(0)).strip()
            if not value or value.startswith(("data:", "blob:", "javascript:", "#", "mailto:", "tel:")):
                continue
            try:
                absolute = urljoin(base, value)
            except ValueError:
                continue
            parts = urlsplit(absolute)
            if parts.scheme not in ("http", "https", "ws", "wss") or not parts.netloc:
                continue
            key = parts._replace(fragment="").geturl()
            if key in found:
                if source not in found[key]["seen_as"]:
                    found[key]["seen_as"].append(source)
                continue
            if len(found) >= MAX_ENDPOINTS:
                break
            order += 1
            found[key] = {"url": key, "host": (parts.hostname or "").lower(), "path": parts.path or "/",
                          "query": bool(parts.query), "scheme": parts.scheme, "written_as": value,
                          "same_origin": same_origin(base, absolute), "seen_as": [source], "order": order}
    items = sorted(found.values(), key=lambda item: item["order"])
    for item in items:
        item.pop("order")
    hosts = sorted({item["host"] for item in items if item["host"]})
    origin = urlsplit(base)
    return {"format": "tgwitness-webapp-endpoints-v1", "base": base, "origin": origin.netloc,
            "endpoints": items, "hosts": hosts,
            "third_party_hosts": [host for host in hosts if host != (origin.hostname or "").lower()],
            "sockets": sorted({item["url"] for item in items if item["scheme"] in ("ws", "wss")}),
            "truncated": len(found) >= MAX_ENDPOINTS, "meaning": INSPECT_MEANING}


def merge(first, second):
    known = {item["url"] for item in first["endpoints"]}
    for item in second["endpoints"]:
        if item["url"] not in known and len(first["endpoints"]) < MAX_ENDPOINTS:
            first["endpoints"].append({**item, "same_origin": same_origin(first["base"], item["url"])})
            known.add(item["url"])
    hosts = sorted({item["host"] for item in first["endpoints"] if item["host"]})
    origin = (urlsplit(first["base"]).hostname or "").lower()
    first.update(hosts=hosts, third_party_hosts=[host for host in hosts if host != origin],
                 sockets=sorted({item["url"] for item in first["endpoints"] if item["scheme"] in ("ws", "wss")}),
                 truncated=first["truncated"] or second["truncated"] or len(first["endpoints"]) >= MAX_ENDPOINTS)
    return first


def route_of(collector):
    route = collector.outside_route()
    if route.kind == "none":
        raise route.error
    return route


async def fetch_page(url, route, scripts=MAX_SCRIPTS, timeout=20):
    """The page and up to `scripts` of its own scripts, parsed for addresses. Returns (record, files)."""
    status, headers, body = await netclient.request("GET", url, route, timeout=timeout, limit=MAX_BYTES)
    found = endpoints(body, url)
    content = next((value for name, value in (headers or {}).items() if name.lower() == "content-type"), None)
    files = [("page", content or "text/html", body or b"", url)]
    fetched = []
    for item in [item for item in found["endpoints"] if item["same_origin"] and item["scheme"] in ("http", "https")
                 and re.search(r"\.m?js$", item["path"]) and {"attribute", "import"} & set(item["seen_as"])][:scripts]:
        try:
            code, _, script = await netclient.request("GET", item["url"], route, timeout=timeout, limit=MAX_BYTES)
        except (netclient.HTTPError, netclient.RouteError, OSError, ValueError):
            fetched.append({"url": item["url"], "status": None})
            continue
        fetched.append({"url": item["url"], "status": code, "bytes": len(script or b"")})
        if code == 200 and script:
            files.append(("script", "text/javascript", script, item["url"]))
            merge(found, endpoints(script, item["url"]))
    return {**found, "status": status, "content_type": content, "bytes": len(body or b""), "scripts": fetched}, files


async def inspect(collector, url, timeout=20, scripts=0):
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValueError("Provide the http or https address of the mini application.")
    route = route_of(collector)
    record, _ = await fetch_page(url, route, scripts, timeout)
    record.update(fetched_at=utcnow(), route=route.kind, route_meaning=ROUTE_MEANING)
    collector.store.append("webapp.inspected", {
        "address": url, "status": record["status"], "content_type": record["content_type"], "bytes": record["bytes"],
        "endpoints": len(record["endpoints"]), "addresses": record["endpoints"], "hosts": record["hosts"],
        "scripts": record["scripts"], "route": route.kind, "meaning": INSPECT_MEANING + " " + ROUTE_MEANING})
    return record


async def input_user(collector, reference):
    try:
        entity = await collector.client.get_input_entity(reference)
    except (ValueError, TypeError, errors.RPCError):
        entity = await collector.lookup_entity(reference)
        entity = utils.get_input_user(entity) if entity else None
    if entity is None:
        raise ValueError("Telegram did not return this bot to this account.")
    try:
        return utils.get_input_user(entity)
    except TypeError:
        raise ValueError("This chat is not a bot.") from None


async def launch(collector, chat_id, entry):
    """Ask Telegram for the launch address. Returns (event, address); the address holds the signed launch data."""
    interactions.permitted(collector)
    store = collector.store
    if not collector.selected(chat_id):
        raise ValueError("Enable observation for this chat in Sources first.")
    peer = utils.get_input_peer(await collector.resolve_target(chat_id))
    details = {"entry": entry["type"], "platform": PLATFORM}
    message_id = None
    if entry["type"] == "button":
        if entry.get("seq") is None:
            raise ValueError("Select a saved mini application button.")
        rows = store.events(chat_id=chat_id, before=int(entry["seq"]) + 1, limit=1)
        if not rows or rows[0]["seq"] != entry["seq"]:
            raise ValueError("Select a saved mini application button.")
        markup = of_payload(rows[0]["payload"])
        try:
            button = markup["rows"][int(entry["row"])][int(entry["column"])]
        except (IndexError, KeyError, TypeError, ValueError):
            raise ValueError("Select a saved mini application button.") from None
        if button.get("type") != "web_app" or not button.get("url"):
            raise ValueError("This button does not open a mini application.")
        raw = (rows[0]["payload"] or {}).get("raw") or {}
        bot_ref = raw.get("via_bot_id") or rows[0].get("actor_id") or (chat_id if chat_id > 0 else None)
        if not bot_ref:
            raise ValueError("The record does not say which bot sent this button.")
        bot = await input_user(collector, bot_ref)
        message_id = rows[0].get("message_id")
        if markup.get("inline"):
            request = functions.messages.RequestWebViewRequest(peer=peer, bot=bot, platform=PLATFORM, url=button["url"])
        else:
            request = functions.messages.RequestSimpleWebViewRequest(bot=bot, platform=PLATFORM, url=button["url"])
        details.update(keyboard_event=entry["seq"], inline=bool(markup.get("inline")), button=button["text"][:200],
                       requested_url=button["url"])
    elif entry["type"] == "link":
        link = app_link(entry.get("url"))
        if not link:
            raise ValueError("This is not a Telegram mini application link.")
        bot = await input_user(collector, link["bot"])
        if link["app"]:
            request = functions.messages.RequestAppWebViewRequest(
                peer=peer, app=types.InputBotAppShortName(bot_id=bot, short_name=link["app"]), platform=PLATFORM,
                start_param=link["start"])
        else:
            request = functions.messages.RequestMainWebViewRequest(peer=peer, bot=bot, platform=PLATFORM,
                                                                   start_param=link["start"])
        details.update(link=link["url"], app=link["app"], start_param=link["start"], bot_username=link["bot"])
    elif entry["type"] in ("menu", "main"):
        bot = await input_user(collector, chat_id)
        if entry["type"] == "menu":
            full = await collector.client(functions.users.GetFullUserRequest(bot))
            button = getattr(getattr(full.full_user, "bot_info", None), "menu_button", None)
            if not isinstance(button, types.BotMenuButton):
                raise ValueError("This bot has no menu mini application.")
            request = functions.messages.RequestWebViewRequest(peer=peer, bot=bot, platform=PLATFORM, url=button.url,
                                                               from_bot_menu=True)
            details.update(button=button.text[:200], requested_url=button.url)
        else:
            request = functions.messages.RequestMainWebViewRequest(peer=peer, bot=bot, platform=PLATFORM)
    else:
        raise ValueError("Choose a mini application button, link or bot menu.")
    details["bot_id"] = getattr(bot, "user_id", None)
    try:
        known = await asyncio.wait_for(collector.client.get_entity(bot), 10)
        details.update(bot_username=details.get("bot_username") or getattr(known, "username", None),
                       bot_name=utils.get_display_name(known)[:200] or None)
    except (ValueError, TypeError, errors.RPCError, asyncio.TimeoutError):
        pass
    try:
        answer = await collector.client(request)
    except errors.RPCError as exc:
        store.append("webapp.launch_failed", {**details, "error": type(exc).__name__, "message": str(exc)[:300]},
                     chat_id, message_id)
        if isinstance(exc, FLOOD_ERRORS):
            raise
        interactions.note_restriction(store, exc)
        raise ValueError("Telegram refused to open this mini application. The journal records its answer.") from None
    address = getattr(answer, "url", None)
    if not isinstance(address, str) or not address.startswith(("https://", "http://")):
        raise ValueError("Telegram returned no address for this mini application.")
    event = store.append("webapp.launch_requested", {
        **details, "address": webapp_browser.public_address(address), "fullscreen": bool(getattr(answer, "fullscreen", False)),
        "launch_data_removed": init_data_of(address) is not None, "meaning": LAUNCH_MEANING}, chat_id, message_id)
    return event, address


def keep(store, files, chat_id, message_id, launch_seq):
    media = store.root / "media"
    media.mkdir(mode=0o700, exist_ok=True)
    saved, seen = [], {}
    for role, mime, data, label in files:
        if not data:
            continue
        digest = hashlib.sha256(data).hexdigest()
        if digest in seen:
            seen[digest]["labels"].append(str(label)[:300])
            continue
        target = media / digest
        if not target.is_file() or target.stat().st_size != len(data):
            private_write(target, data)
        item = {"sha256": digest, "role": role, "mime_type": (mime or "application/octet-stream")[:120],
                "size": len(data), "labels": [str(label)[:300]]}
        seen[digest] = item
        saved.append(item)
    for item in saved:
        store.append(FILE_KIND, {"media_sha256": item["sha256"], "size": item["size"], "mime_type": item["mime_type"],
                                 "role": item["role"], "labels": item["labels"], "launch_seq": launch_seq},
                     chat_id, message_id)
    return saved


def indicators_of(facts, files, at):
    found = Indicators()
    found.text(facts.get("text") or "", SOURCE, None, at)
    for value in (facts.get("links") or [])[:MAX_LINKS] + [r.get("url") for r in facts.get("requests") or []] \
            + [s.get("url") for s in facts.get("sockets") or []] + [p.get("url") for p in facts.get("popups") or []]:
        if isinstance(value, str) and value.startswith(("http://", "https://", "ws://", "wss://")):
            found.link(value.replace("ws://", "http://", 1).replace("wss://", "https://", 1), SOURCE, None, at)
    for event in facts.get("telegram_events") or []:
        found.text(event.get("data") or "", SOURCE, None, at)
    for socket in facts.get("sockets") or []:
        for frame in socket.get("frames") or []:
            found.wallets(frame.get("data") or "", SOURCE, None, at)
    scripts = Indicators()
    for role, _, data, _ in files:
        if role == "script":
            scripts.wallets(data.decode("utf-8", "replace"), SOURCE, None, at)
    for item in scripts.found.values():
        if item.get("checksum") == "valid":
            found.note(item["kind"], item["value"], SOURCE, None, at,
                       **{key: item[key] for key in ("chain", "checksum") if key in item})
    keep_keys = ("kind", "value", "chain", "checksum", "count")
    items = sorted(found.found.values(), key=lambda item: (item["kind"] != "wallet", item["kind"], item["value"]))
    return [{key: item[key] for key in keep_keys if key in item} for item in items[:MAX_INDICATORS]]


def asks_of(events):
    found = []
    for event in events or []:
        kind = ASKS.get(event.get("type"))
        if kind and not any(item["kind"] == kind and item["data"] == event.get("data") for item in found):
            found.append({"kind": kind, "type": event.get("type"), "data": event.get("data")})
    return found


async def open_app(collector, chat_id, entry, *, mode="passive", max_states=8):
    """Launch, load and record a mini application. Returns the capture record with its journal number."""
    store = collector.store
    route = route_of(collector)
    launched, address = await launch(collector, chat_id, entry)
    message_id, at = launched.get("message_id"), launched.get("observed_at")
    secret = init_data_of(address)
    state = webapp_browser.status()
    files, errors_ = [], []
    if state["browser"]:
        try:
            facts, files = await webapp_browser.capture(address, route, secret, mode=mode, max_states=max_states)
            method = "browser"
        except webapp_browser.Unavailable as exc:
            errors_.append({"component": "browser", "error": str(exc)[:600]})
            state = {"browser": False, "reason": str(exc)[:600]}
    if not state["browser"]:
        public = webapp_browser.public_address(address)
        try:
            record, files = await fetch_page(public, route)
        except (netclient.HTTPError, netclient.RouteError, OSError, ValueError) as exc:
            store.append("webapp.capture_failed", {"launch_seq": launched["seq"], "error": str(exc)[:300],
                                                   "browser": state.get("reason")}, chat_id, message_id)
            raise ValueError("The mini application could not be loaded through this workspace's route. The journal "
                             "records the error.") from None
        redact = webapp_browser.Redactor(secret)
        facts = {"final_url": public, "title": "", "text": "", "links": [], "requests": [
            {"url": item["url"], "type": "Script", "status": item.get("status"), "bytes": item.get("bytes")}
            for item in record["scripts"]], "addresses": redact(record["endpoints"]), "sockets": [
            {"url": url, "frames": []} for url in record["sockets"]], "status": record["status"],
            "content_type": record["content_type"], "browser_missing": state.get("reason")}
        method = "static"
    saved = keep(store, files, chat_id, message_id, launched["seq"])
    requests = facts.get("requests") or []
    hosts = sorted({(urlsplit(item.get("url") or "").hostname or "").lower()
                    for item in requests + (facts.get("sockets") or [])} - {""})
    origin = (urlsplit(facts.get("final_url") or address).hostname or "").lower()
    first = (urlsplit(webapp_browser.public_address(address)).hostname or "").lower()
    asks = asks_of(facts.get("telegram_events"))
    payload = {
        "launch_seq": launched["seq"], "entry": entry["type"], "method": method,
        "mode": facts.get("mode", mode) if method == "browser" else "static",
        "states_captured": facts.get("states_captured", 1 if method == "browser" else 0),
        "bot": {"id": launched["payload"].get("bot_id"), "username": launched["payload"].get("bot_username"),
                "name": launched["payload"].get("bot_name")},
        "address": webapp_browser.public_address(address), "final_url": facts.get("final_url"),
        "title": facts.get("title"), "browser": facts.get("browser"), "sandbox": facts.get("sandbox"),
        "route": route.kind, "duration_ms": facts.get("duration_ms"), "status": facts.get("status"),
        "hosts": hosts, "third_party_hosts": [host for host in hosts if host not in (origin, first)],
        "requests": requests, "sockets": facts.get("sockets") or [], "connections": facts.get("connections") or [],
        "browser_connections": facts.get("browser_connections") or [],
        "blocked": facts.get("blocked") or [], "telegram_events": facts.get("telegram_events") or [], "asks": asks,
        "dialogs": facts.get("dialogs") or [], "popups": facts.get("popups") or [], "downloads": facts.get("downloads") or [],
        "console": [line for line in facts.get("console") or [] if line.get("level") in ("error", "warning")][:30],
        "forms": facts.get("forms") or [], "inputs": facts.get("inputs") or [], "frames": facts.get("frames") or [],
        "links": (facts.get("links") or [])[:MAX_LINKS], "webapp": facts.get("webapp"),
        "addresses": (facts.get("addresses") or [])[:MAX_ENDPOINTS],
        "indicators": indicators_of(facts, files, at), "files": [
            {key: item[key] for key in ("sha256", "role", "mime_type", "size", "labels")} for item in saved],
        "dropped": facts.get("dropped"), "errors": errors_ + (facts.get("errors") or []),
        "browser_missing": facts.get("browser_missing"),
        "meaning": (CAPTURE_MEANING if method == "browser" else INSPECT_MEANING) + " " + ROUTE_MEANING}
    payload["summary"] = {"requests": len(requests), "hosts": len(hosts), "sockets": len(payload["sockets"]),
                          "asks": len(asks), "wallets": sum(1 for item in payload["indicators"] if item["kind"] == "wallet"),
                          "screenshots": sum(1 for item in saved if item["role"] == "screenshot"),
                          "mhtml": sum(1 for item in saved if item["role"] == "mhtml"),
                          "har": sum(1 for item in saved if item["role"] == "har")}
    event = store.append("webapp.captured", payload, chat_id, message_id)
    return {"seq": event["seq"], "at": event["observed_at"], **payload}


def register(app, authenticate, require_live, visible_chats):
    from fastapi import Depends, HTTPException, Path, Query, Request
    from pydantic import BaseModel, ConfigDict, Field
    from typing import Literal

    class Address(BaseModel):
        url: str = Field(..., max_length=2048)
        scripts: int = Field(default=0, ge=0, le=MAX_SCRIPTS)

    class Entry(BaseModel):
        model_config = ConfigDict(extra="forbid")
        type: Literal["button", "link", "menu", "main"]
        seq: int | None = Field(default=None, gt=0)
        row: int | None = Field(default=None, ge=0, le=100)
        column: int | None = Field(default=None, ge=0, le=100)
        url: str | None = Field(default=None, max_length=2048)

    class Open(BaseModel):
        model_config = ConfigDict(extra="forbid")
        chat_id: int
        entry: Entry
        mode: Literal["passive", "crawl", "interactive"] = "passive"
        max_states: int = Field(default=8, ge=1, le=20)

    def visible(request, chat_id):
        chats = visible_chats(request)
        if chats is not None and chat_id not in chats:
            raise HTTPException(403, "This chat is not open to this access.")

    @app.get("/api/webapp", dependencies=[Depends(authenticate)])
    async def listing(request: Request, chat_id: int = Query(ge=-(2**63), le=2**63 - 1), limit: int = 200):
        visible(request, chat_id)
        if not 1 <= limit <= 1000:
            raise HTTPException(422, "Read between 1 and 1000 records at a time.")
        store = app.state.store
        known = (getattr(app.state.collector, "dialog_cache", None) or {}).get(chat_id) or {}
        targets = {item.get("chat_id"): item for item in store.targets()}
        bot = chat_id > 0 and (known.get("kind") or (targets.get(chat_id) or {}).get("kind")) == "bot"
        return {"chat_id": chat_id, "bot": bot, "buttons": in_messages(store, chat_id, limit),
                "entries": entries(store, chat_id, limit),
                "captures": captures(store, chat_id), "browser": {key: value for key, value in webapp_browser.status().items()
                                                                  if key != "path"}}

    @app.get("/api/webapp/captures/{seq}", dependencies=[Depends(authenticate)])
    async def capture_record(request: Request, seq: int = Path(ge=1, le=2**63 - 2),
                             chat_id: int = Query(ge=-(2**63), le=2**63 - 1)):
        visible(request, chat_id)
        rows = app.state.store.events(chat_id=chat_id, kind="webapp.captured", before=seq + 1, limit=1)
        if not rows or rows[0]["seq"] != seq:
            raise HTTPException(404, "No mini application capture with this number in this chat.")
        return {"seq": seq, "at": rows[0]["observed_at"], **rows[0]["payload"]}

    @app.post("/api/webapp/open", dependencies=[Depends(authenticate)])
    async def open_entry(body: Open, request: Request):
        if not request.state.principal.admin:
            raise HTTPException(403, "Only the main administrator can open a mini application.")
        require_live()
        try:
            return await open_app(app.state.collector, body.chat_id, body.entry.model_dump(),
                                  mode=body.mode, max_states=body.max_states)
        except netclient.RouteError as exc:
            raise HTTPException(409, str(exc)) from None
        except interactions.AccountRestricted as exc:
            raise HTTPException(409, str(exc)) from None
        except FLOOD_ERRORS as exc:
            raise HTTPException(429, {"message": "Telegram asked to wait before the next account action.",
                                      "retry_after": exc.seconds}) from None
        except errors.RPCError:
            raise HTTPException(409, "Telegram refused to open this mini application. The journal records its "
                                     "answer.") from None
        except (ValueError, OSError) as exc:
            raise HTTPException(422, str(exc)) from None

    @app.post("/api/webapp/inspect", dependencies=[Depends(authenticate)])
    async def inspect_address(body: Address, request: Request):
        if not request.state.principal.admin:
            raise HTTPException(403, "Only the main administrator can fetch a mini application.")
        require_live()
        try:
            return await inspect(app.state.collector, body.url, scripts=body.scripts)
        except netclient.RouteError as exc:
            raise HTTPException(409, str(exc)) from None
        except (netclient.HTTPError, OSError, ValueError) as exc:
            raise HTTPException(422, str(exc)) from None


def note_indicators(found, addresses, source, ref, at):
    for item in addresses:
        if not isinstance(item, dict) or not isinstance(item.get("url"), str):
            continue
        if item.get("scheme") in ("http", "https"):
            found.link(item["url"], source, ref, at)
        elif isinstance(item.get("host"), str) and item["host"]:
            found.domain(item["host"], source, ref, at)
    return found


def note_capture(found, payload, ref, at):
    note_indicators(found, payload.get("addresses") or [], SOURCE, ref, at)
    for item in payload.get("indicators") or []:
        if not isinstance(item, dict) or not isinstance(item.get("value"), str):
            continue
        if item.get("kind") == "url":
            found.link(item["value"], SOURCE, ref, at)
        elif item.get("kind") in ("domain", "wallet", "telegram", "telegram-invite", "email", "phone"):
            extra = {key: item[key] for key in ("chain", "checksum") if key in item}
            found.note(item["kind"], item["value"], SOURCE, ref, at, **extra)
    return found
