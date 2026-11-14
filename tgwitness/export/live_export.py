import asyncio
import html
import json
import logging
import shutil
import time
from contextlib import suppress
from copy import copy
from pathlib import Path

from .. import report, verification_kit
from ..account_export import linked
from ..evidence import producer
from ..store import utcnow
from ..verify import fingerprint
from ..workers import complete_in_thread
from .manifest_incremental import START_FILE, SealChain, page_name, seal_name
from .streaming_zip import LiveZip, digest

PAGE_MESSAGES = 2000
PAGE_SECONDS = 10
PAGE_BYTES = 8 * 1024**2
BACKLOG_PAGES = 50
NOT_READY = "No signed snapshot is ready yet. The first page is sealed a few seconds after reading starts."
HEADLINE = "Live chat export"
EXPLAINED = ("Messages read so far by an export that is still running. Each page is signed with the workspace key as "
             "soon as it is written. The finished export adds attachments, the full report and its own signature.")
CHECK = "Check this archive with verify.py: python verify.py ARCHIVE.zip --fingerprint {fp}. START_HERE.txt explains each step."
MEDIA = {"MessageMediaPhoto": "Photo", "MessageMediaGeo": "Location", "MessageMediaGeoLive": "Location",
         "MessageMediaVenue": "Location", "MessageMediaContact": "Contact", "MessageMediaPoll": "Poll",
         "MessageMediaWebPage": "Link preview"}
STICKERS = ("application/x-tgsticker", "image/webp")
CSS = (":root{color-scheme:light dark;--bg:#f5f6f8;--card:#fff;--ink:#16181d;--muted:#5b6270;--line:#e2e5ea;"
       "--accent:#2458d3}@media(prefers-color-scheme:dark){:root{--bg:#0f1115;--card:#171a21;--ink:#e7e9ee;"
       "--muted:#9aa3b2;--line:#283040;--accent:#86a8ff}}*{box-sizing:border-box}body{margin:0;background:var(--bg);"
       "color:var(--ink);font:15px/1.5 system-ui,-apple-system,'Segoe UI',Roboto,'Noto Sans',sans-serif}"
       "header{position:sticky;top:0;background:var(--card);border-bottom:1px solid var(--line);padding:12px 20px;"
       "z-index:1}h1{font-size:17px;margin:0 0 2px}.meta{color:var(--muted);font-size:13px}nav{display:flex;"
       "flex-wrap:wrap;gap:6px 16px;margin-top:6px;font-size:14px}a{color:var(--accent)}main{max-width:860px;"
       "margin:0 auto;padding:12px 12px 48px}.notice{color:var(--muted);font-size:13px;margin:8px 4px 14px}"
       ".msg{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:9px 14px;margin:8px 0}"
       ".msg:target{outline:2px solid var(--accent)}.service{background:transparent;border-style:dashed;"
       "color:var(--muted);text-align:center;font-size:13px}.head{display:flex;flex-wrap:wrap;gap:4px 10px;"
       "align-items:baseline;font-size:13px;color:var(--muted)}.who{font-weight:600;color:var(--ink)}"
       ".text{white-space:pre-wrap;overflow-wrap:anywhere;margin-top:3px}.tags{display:flex;flex-wrap:wrap;gap:6px;"
       "margin-top:6px}.tag{border:1px solid var(--line);border-radius:999px;padding:0 9px;font-size:12px;"
       "color:var(--muted)}")
log = logging.getLogger(__name__)


def escape(value):
    return html.escape(str(value), quote=True)


def media_label(say, record):
    kind = record.get("media_type")
    if not kind:
        return None
    info = record.get("media_info") if isinstance(record.get("media_info"), dict) else {}
    if kind != "MessageMediaDocument":
        return say(MEDIA.get(kind, "Attachment"))
    mime = str(info.get("mime_type") or "")
    label = say("Sticker" if mime in STICKERS else "Video" if mime.startswith("video/")
                else "Audio" if mime.startswith("audio/") else "Attachment")
    return label + (" · " + str(info["file_name"]) if info.get("file_name") else "")


def message_html(say, record, title, shown):
    number = record.get("id")
    anchor = ' id="m' + escape(number) + '"' if type(number) is int else ""
    if record.get("type") == "service":
        action = " · ".join(str(x) for x in (record.get("action"), record.get("action_title")) if x)
        when = report.utc_text(record["date"]) if record.get("date") else ""
        return ('<div class="msg service"' + anchor + '>' + escape(say("Service message")) + (" · " + escape(action) if action else "")
                + (" · " + escape(when) if when else "") + " · #" + escape(number) + "</div>")
    if record.get("type") == "unparsed":
        meaning = (record.get("unparsed") or {}).get("meaning") or ""
        return ('<div class="msg service"' + anchor + '>' + escape(say("Message #{id}", id=number)) + " · "
                + escape(meaning) + "</div>")
    sender = record.get("from") or record.get("author") or (str(record["from_id"]) if record.get("from_id") else title)
    head = ['<span class="who">' + escape(sender) + "</span>"]
    if record.get("from_username"):
        head.append("<span>@" + escape(record["from_username"]) + "</span>")
    if record.get("date"):
        head.append("<time>" + escape(report.utc_text(record["date"])) + "</time>")
    if record.get("edited"):
        head.append("<span>" + escape(say("edited {time}", time=report.utc_text(record["edited"]))) + "</span>")
    head.append('<a href="#m' + escape(number) + '">#' + escape(number) + "</a>")
    tags = []
    reply = record.get("reply_to_message_id")
    if type(reply) is int:
        target = '<a href="#m' + str(reply) + '">#' + str(reply) + "</a>" if reply in shown else "#" + str(reply)
        tags.append('<span class="tag">' + escape(say("Reply to")) + " " + target + "</span>")
    forwarded = record.get("forwarded_from") if isinstance(record.get("forwarded_from"), dict) else None
    if forwarded:
        origin = forwarded.get("from_name") or forwarded.get("post_author") or forwarded.get("from_id") or ""
        tags.append('<span class="tag">' + escape(say("Forwarded from") + (" " + str(origin) if origin else "")) + "</span>")
    media = media_label(say, record)
    if media:
        tags.append('<span class="tag">' + escape(media) + "</span>")
    text = record.get("text") if isinstance(record.get("text"), str) else ""
    return ('<div class="msg"' + anchor + '><div class="head">' + "".join(head) + "</div>"
            + ('<div class="text">' + escape(text) + "</div>" if text else "")
            + ('<div class="tags">' + "".join(tags) + "</div>" if tags else "") + "</div>")


def render_page(say, title, number, records, facts, fp):
    shown = {r.get("id") for r in records if type(r.get("id")) is int}
    span = ("#" + str(facts["high"]) + "–#" + str(facts["low"])) if facts.get("high") is not None else ""
    meta = " · ".join(x for x in (say("Page {n}", n=number), say("Messages") + ": " + str(facts["messages"]), span,
                                  say("Sealed {time}", time=report.utc_text(facts["read_until"]))) if x)
    links = []
    if number > 1:
        links.append('<a href="' + page_name(number - 1, ".html").rsplit("/", 1)[1] + '">← ' + escape(say("Newer messages")) + "</a>")
    links.append('<a href="' + page_name(number + 1, ".html").rsplit("/", 1)[1] + '">' + escape(say("Older messages")) + " →</a>")
    body = "".join(message_html(say, record, title, shown) for record in reversed(records))
    return ('<!doctype html><html lang="' + escape(say.language) + '" dir="' + say.direction + '"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" '
            'content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'"><title>' + escape(title) + " · "
            + escape(say("Page {n}", n=number)) + "</title><style>" + CSS + "</style><header><h1>" + escape(say(HEADLINE))
            + " · " + escape(title) + '</h1><div class="meta">' + escape(meta) + "</div><nav>" + "".join(links)
            + '</nav></header><main><p class="notice">' + escape(say(EXPLAINED)) + " " + escape(say("Signed · check with verify.py"))
            + " · " + escape(fp[:16]) + "…</p>" + body + "</main></html>\n").encode("utf-8")


class LiveExport:
    def __init__(self, directory, vault, identity, language="en", min_free=0):
        self.directory = Path(directory)
        self.path = self.directory / ("live-" + identity["export_id"] + ".zip")
        self.zip = LiveZip(self.path)
        self.chain = SealChain(vault, identity, producer())
        self.say = report.Words(language)
        self.language, self.min_free = language, min_free
        self.title = (identity.get("chat") or {}).get("title") or str((identity.get("chat") or {}).get("id"))
        self.fp = fingerprint(vault.public_key)
        self.lines, self.bytes, self.page_started, self.read_from = [], 0, None, None
        self.wake, self.task, self.closing = asyncio.Event(), None, False
        self.state, self.stop, self.error, self.sealed_at = "reading", None, None, None
        self.final_state, self.final_stop, self.finish_task = None, None, None

    @staticmethod
    def sweep(directory, keep=None):
        for path in Path(directory).glob("live-*.zip*"):
            if path.name not in (keep or ()) and not linked(path):
                with suppress(OSError):
                    path.unlink()

    def readme(self):
        say = self.say
        chat = self.chain.identity.get("chat") or {}
        lines = ["TgWitness · " + say(HEADLINE), str(self.title) + " · " + str(chat.get("id")), "=" * 64, "",
                 say(EXPLAINED), "", say(CHECK, fp=self.fp), "",
                 "live/export.json        signed start of this export: chat, account and the files below",
                 "live/pages/NNNNNN.jsonl messages of one page, one JSON record per line, newest first",
                 "live/pages/NNNNNN.html  the same page to read in a browser",
                 "live/seals/NNNNNN.json  signature of each page; it names the page before it",
                 "manifest.json, manifest.sig  the latest seal: state, pages and messages so far",
                 "Attachments are not in this archive. Messages keep their file names and types.",
                 "Workspace key fingerprint: " + self.fp]
        return ("\n".join(lines) + "\n").encode("utf-8")

    def begin(self):
        self.directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.sweep(self.directory)
        statics = [("README.txt", self.readme()),
                   ("verify.py", Path(report.__file__).with_name("verify.py").read_bytes()),
                   *verification_kit.files(self.language).items()]
        start = self.chain.start({name: digest(data) for name, data in statics}, utcnow())
        self.zip.append([(START_FILE, start), *statics], lambda _: self.chain.manifest(self.state))

    async def open(self):
        await complete_in_thread(self.begin)
        self.sealed_at = utcnow()
        self.task = asyncio.create_task(self.run())

    def add(self, line):
        if self.task is None or self.closing or self.error:
            return
        if not self.lines:
            self.page_started, self.read_from = time.monotonic(), utcnow()
        self.lines.append(line)
        self.bytes += len(line)
        if len(self.lines) > BACKLOG_PAGES * PAGE_MESSAGES or self.bytes > BACKLOG_PAGES * PAGE_BYTES:
            self.fail(OverflowError("The live archive fell behind the reading."))
        elif len(self.lines) >= PAGE_MESSAGES or self.bytes >= PAGE_BYTES:
            self.wake.set()

    def due(self):
        return bool(self.lines) and (self.closing or len(self.lines) >= PAGE_MESSAGES or self.bytes >= PAGE_BYTES
                                     or time.monotonic() - self.page_started >= PAGE_SECONDS)

    async def run(self):
        while not self.error:
            if not self.due():
                with suppress(asyncio.TimeoutError):
                    await asyncio.wait_for(self.wake.wait(), 1)
                self.wake.clear()
            if self.due():
                await self.flush()
            elif self.closing:
                return

    def write_page(self, number, lines, read_from, read_until):
        data = "".join(lines).encode("utf-8")
        records = [json.loads(line) for line in lines]
        ids = [r["id"] for r in records if type(r.get("id")) is int]
        facts = {"messages": len(lines), "first_id": ids[0] if ids else None, "last_id": ids[-1] if ids else None,
                 "low": min(ids) if ids else None, "high": max(ids) if ids else None,
                 "read_from": read_from, "read_until": read_until}
        page = render_page(self.say, self.title, number, records, facts, self.fp)
        if shutil.disk_usage(self.directory).free < self.min_free + 4 * (len(data) + len(page)):
            raise OSError("Not enough free disk space for the live archive.")
        files = {page_name(number, ".jsonl"): digest(data), page_name(number, ".html"): digest(page)}
        chain, offset = copy(self.chain), self.zip.offset
        seal = chain.page(number, files, facts)
        try:
            self.zip.append([(page_name(number, ".jsonl"), data), (page_name(number, ".html"), page),
                            (seal_name(number), seal)], lambda _: chain.manifest(self.state, self.stop))
        finally:
            if self.zip.offset != offset:
                self.chain = chain

    async def flush(self):
        count = size = 0
        for line in self.lines:
            if count and (count >= PAGE_MESSAGES or size + len(line) > PAGE_BYTES):
                break
            count, size = count + 1, size + len(line)
        lines, read_from, self.lines = self.lines[:count], self.read_from, self.lines[count:]
        self.bytes -= size
        self.page_started, self.read_from = (time.monotonic(), utcnow()) if self.lines else (None, None)
        try:
            await complete_in_thread(self.write_page, self.chain.pages + 1, lines, read_from, utcnow())
            self.sealed_at = utcnow()
        except Exception as exc:
            self.fail(exc)

    def fail(self, exc):
        log.warning("Live chat export archive stopped: %s", type(exc).__name__)
        self.error, self.lines, self.bytes = type(exc).__name__, [], 0

    async def close(self, state, stop=None):
        if self.task is None:
            return
        if self.final_state is None or state == "stopped":
            self.final_state, self.final_stop = state, stop
        self.closing = True
        self.wake.set()
        if (self.state, self.stop) == (self.final_state, self.final_stop):
            return
        task = self.finalizer()
        try:
            await asyncio.shield(task)
        except asyncio.CancelledError:
            self.final_state, self.final_stop = "stopped", "cancelled"
            task = self.finalizer()
            while not task.done():
                try:
                    await asyncio.shield(task)
                except asyncio.CancelledError:
                    continue
                except Exception:
                    break
            if not task.cancelled():
                task.exception()
            raise

    def finalizer(self):
        if self.finish_task is None or self.finish_task.done():
            self.finish_task = asyncio.create_task(self.seal_closed())
        return self.finish_task

    async def seal_closed(self):
        try:
            await asyncio.shield(self.task)
        except Exception as exc:
            self.fail(exc)
        while not self.error:
            state, stop = self.final_state, self.final_stop
            try:
                await complete_in_thread(self.zip.append, [], lambda _: self.chain.manifest(state, stop))
                self.state, self.stop, self.sealed_at = state, stop, utcnow()
            except Exception as exc:
                self.fail(exc)
                return
            if (state, stop) == (self.final_state, self.final_stop):
                return

    def ready(self):
        return self.zip.offset is not None and self.chain.pages > 0

    def public(self):
        found = {"state": "failed" if self.error else self.state, "pages": self.chain.pages, "messages": self.chain.messages,
                 "sealed_at": self.sealed_at, "bytes": self.zip.size}
        if self.stop:
            found["stop"] = self.stop
        if self.error:
            found["error"] = self.error
        return found

    def snapshot(self, target):
        if not self.ready():
            raise ValueError(NOT_READY)
        return self.zip.snapshot(target)

    def discard(self):
        for path in (self.zip.path, self.zip.sealed):
            with suppress(OSError):
                path.unlink(missing_ok=True)


def repair(root):
    repaired = 0
    for path in Path(root, "partial-exports").glob("*/live-*.zip"):
        if linked(path) or linked(path.parent) or not path.with_name(path.name + ".sealed").is_file():
            continue
        try:
            repaired += LiveZip(path).recover()
        except Exception as exc:
            log.warning("Live chat export archive %s could not be restored: %s", path.name, type(exc).__name__)
    return repaired
