"""Pseudo-secret chats in reports: one conversation per chat, with deletions, timers, screenshots and read notices in place."""
import base64
import json
from html import escape
from pathlib import Path

TITLE = "Pseudo-secret conversation"
LEAD = ("Messages as TgWitness received and sent them in this pseudo-secret chat, oldest first. Deletions, timers, "
        "screenshots and read notices appear where they happened.")
CHAT_WITH = "Pseudo-secret chat with {name}"
SEVERAL = "Pseudo-secret chats"
OTHER_SIDE = "Other side"
KEY = "Encryption key"
LIMITED = "Only the first {n} messages of this chat are shown here; the journal and the records section hold all of them."
MESSAGE_LIMIT = 5000
PREVIEW_BYTES = 2 * 1024 * 1024
PDF_IMAGE_BYTES = 8 * 1024 * 1024
IMAGES = ("image/jpeg", "image/png", "image/webp", "image/gif")
MEDIA = {"Photo": "Photo", "Video": "Video", "Audio": "Audio", "GeoPoint": "Location", "Contact": "Contact",
         "Venue": "Place", "WebPage": "Link preview", "ExternalDocument": "Sticker"}
ENDINGS = {"the peer deleted the chat": "The other side deleted the chat; the journal keeps every record."}


def text_keys():
    return [TITLE, LEAD, CHAT_WITH, SEVERAL, OTHER_SIDE, KEY, LIMITED, *MEDIA.values(), *ENDINGS.values(),
            "Voice message", "File", "Attachment", "Received", "Sent", "Files", "Deleted", "Screenshots", "Read",
            "Started", "Status", "Active", "Ended", "Established", "Request from the other side",
            "Requested by this account", "Accepted automatically", "Accepted here", "deleted by the other side; kept here",
            "The other side took a screenshot.", "Timer set to {n} s", "timer {n} s",
            "The other side cleared the history; TgWitness keeps it.", "Record #{n}", "Reply to",
            "The other side deleted {n} messages; TgWitness keeps them.",
            "The other side deleted {n} message; TgWitness keeps it.", "The other side read {n} messages.",
            "The other side read {n} message.", "A message could not be decrypted and was refused.",
            "Telegram rejected a sent message.", "A file could not be saved.", "User {id}", "Pseudo-secret", "ID {id}"]


def media_of(media):
    if not isinstance(media, dict):
        return None
    kind = str(media.get("_") or "")
    kind = kind[len("decryptedMessageMedia"):] if kind.lower().startswith("decryptedmessagemedia") else kind
    mime = str(media.get("mime_type") or "")
    attributes = [a for a in media.get("attributes") or [] if isinstance(a, dict)]
    name = next((a.get("file_name") for a in attributes if "filename" in str(a.get("_", "")).lower()), None)
    voice = any("audio" in str(a.get("_", "")).lower() and a.get("voice") for a in attributes)
    label = MEDIA.get(kind)
    if label is None and kind == "Document":
        label = ("Voice message" if voice else "Photo" if mime.startswith("image/") else "Video" if mime.startswith("video/")
                 else "Audio" if mime.startswith("audio/") else "File")
    return {"label": label or "Attachment", "name": name if isinstance(name, str) else None, "mime": mime or None,
            "size": media.get("size") if type(media.get("size")) is int else None,
            "image": kind == "Photo" or mime.startswith("image/")}


def collect(connection, through=None, chats=None, titles=None, limit=MESSAGE_LIMIT):
    titles = titles or {}
    query = "SELECT seq, observed_at, kind, payload, hash FROM events WHERE kind >= 'secret_chat.' AND kind < 'secret_chat/'"
    values = []
    if through is not None:
        query += " AND seq<=?"
        values.append(through)
    found, wanted = {}, set(chats) if chats is not None else None
    for seq, at, kind, raw, digest in connection.execute(query + " ORDER BY seq", values):
        try:
            payload = json.loads(raw)
        except ValueError:
            continue
        chat_id = payload.get("secret_chat_id")
        if type(chat_id) is not int or wanted is not None and chat_id not in wanted:
            continue
        chat = found.setdefault(chat_id, {"id": chat_id, "peer": {}, "items": [], "state": "pending", "started": None,
                                          "ended": None, "key": None, "truncated": False, "messages": {},
                                          "counts": {"received": 0, "sent": 0, "files": 0, "deleted": 0,
                                                     "screenshots": 0, "read": 0}})
        peer = payload.get("peer_user_id")
        if type(peer) is int:
            chat["peer"]["id"] = peer
        for field, target in (("peer_name", "name"), ("peer_username", "username")):
            if isinstance(payload.get(field), str) and payload[field]:
                chat["peer"][target] = payload[field]
        name = kind[len("secret_chat."):]
        event = lambda text, **extra: chat["items"].append({"type": "event", "seq": seq, "at": at, "text": text, **extra})
        if name == "requested":
            chat["started"] = {"at": at, "seq": seq, "direction": payload.get("direction")}
            event("Request from the other side" if payload.get("direction") == "in" else "Requested by this account")
        elif name == "accepted":
            event("Accepted automatically" if payload.get("automatic") else "Accepted here")
        elif name == "ready":
            chat["state"], chat["key"] = "ready", payload.get("key_visualization") or chat["key"]
            event("Established")
        elif name == "closed":
            chat["state"] = "closed"
            chat["ended"] = {"at": at, "seq": seq, "reason": payload.get("reason"),
                             "deleted_by_peer": bool(payload.get("history_deleted_by_peer"))}
            event("The other side deleted the chat; the journal keeps every record." if payload.get("history_deleted_by_peer")
                  else "Ended", reason=None if payload.get("history_deleted_by_peer") else payload.get("reason"))
        elif name == "message":
            out = payload.get("direction") == "out"
            chat["counts"]["sent" if out else "received"] += 1
            if sum(1 for item in chat["items"] if item["type"] == "message") >= limit:
                chat["truncated"] = True
                continue
            message = {"type": "message", "seq": seq, "at": at, "hash": digest, "direction": "out" if out else "in",
                       "text": payload.get("text") if isinstance(payload.get("text"), str) else "",
                       "ttl": payload.get("ttl") if type(payload.get("ttl")) is int and payload.get("ttl") > 0 else None,
                       "random_id": str(payload.get("random_id")), "media": media_of(payload.get("media")),
                       "reply_to": str(payload["reply_to_random_id"]) if payload.get("reply_to_random_id") else None,
                       "file": None, "deleted": None}
            chat["items"].append(message)
            chat["messages"][message["random_id"]] = message
        elif name == "file":
            chat["counts"]["files"] += 1
            target = chat["messages"].get(str(payload.get("random_id")))
            if target is not None and isinstance(payload.get("media_sha256"), str):
                target["file"] = {"sha256": payload["media_sha256"], "size": payload.get("size"), "seq": seq}
        elif name == "file_failed":
            event("A file could not be saved.")
        elif name == "action":
            details = payload.get("details") if isinstance(payload.get("details"), dict) else {}
            action = payload.get("action")
            ids = [str(value) for value in details.get("random_ids") or payload.get("random_ids") or []]
            if action == "DeleteMessages":
                chat["counts"]["deleted"] += len(ids)
                for random_id in ids:
                    if random_id in chat["messages"]:
                        chat["messages"][random_id]["deleted"] = {"seq": seq, "at": at}
                event("deleted", n=len(ids))
            elif action in ("ScreenshotMessages", "Screenshot"):
                chat["counts"]["screenshots"] += 1
                event("The other side took a screenshot.")
            elif action == "SetMessageTTL":
                event("Timer set to {n} s", n=details.get("ttl_seconds") or 0)
            elif action == "FlushHistory":
                event("The other side cleared the history; TgWitness keeps it.")
            elif action == "ReadMessages":
                chat["counts"]["read"] += len(ids)
                event("read", n=len(ids))
            elif isinstance(action, str):
                event(action)
        elif name == "peer_read":
            chat["counts"]["read"] += 1
            event("Read", until=payload.get("max_date_at"))
        elif name == "decrypt_failed":
            event("A message could not be decrypted and was refused.")
        elif name == "send_failed":
            event("Telegram rejected a sent message.")
    result = []
    for chat in found.values():
        peer = chat["peer"]
        if peer.get("id") is not None and not peer.get("name"):
            title = titles.get(peer["id"]) or titles.get(str(peer["id"]))
            if title:
                peer["name"] = title
        chat.pop("messages")
        result.append(chat)
    return sorted(result, key=lambda chat: (chat["started"] or {}).get("at") or "")


def peer_label(say, peer):
    return peer.get("name") or (say("User {id}", id=peer["id"]) if peer.get("id") is not None else say("Pseudo-secret"))


def title_of(say, conversations):
    if len(conversations) == 1:
        return say(CHAT_WITH, name=peer_label(say, conversations[0]["peer"]))
    return say(SEVERAL)


def event_text(say, item, when):
    text = item["text"]
    if text == "deleted":
        n = item.get("n") or 0
        return say("The other side deleted {n} message; TgWitness keeps it." if n == 1 else
                   "The other side deleted {n} messages; TgWitness keeps them.", n=n)
    if text == "read" and "n" in item:
        n = item["n"]
        return say("The other side read {n} message." if n == 1 else "The other side read {n} messages.", n=n)
    if text == "Read":
        return say("Read") + (" · " + when(item["until"]) if item.get("until") else "")
    if text == "Timer set to {n} s":
        return say(text, n=item.get("n", 0))
    if text == "Ended":
        return say("Ended") + (" · " + str(item["reason"]) if item.get("reason") else "")
    return say(text)


def facts(say, chat, when):
    peer, started, ended = chat["peer"], chat["started"] or {}, chat["ended"]
    status = say("Ended") + " · " + when(ended["at"]) if ended else say("Active")
    origin = say("Request from the other side") if started.get("direction") == "in" else say("Requested by this account")
    return [(say(OTHER_SIDE), " · ".join(filter(None, (peer_label(say, peer), "@" + peer["username"] if peer.get("username") else None,
                                                      say("ID {id}", id=peer["id"]) if peer.get("id") is not None else None)))),
            (say("Pseudo-secret"), "#" + str(chat["id"])),
            (say("Started"), when(started["at"]) + " · " + origin if started.get("at") else None),
            (say("Status"), status),
            (say(KEY), " ".join(chat["key"][i:i + 8] for i in range(0, len(chat["key"]), 8)) if chat.get("key") else None)]


def counts(say, chat):
    c = chat["counts"]
    return [(say("Received"), c["received"]), (say("Sent"), c["sent"]), (say("Files"), c["files"]),
            (say("Deleted"), c["deleted"]), (say("Screenshots"), c["screenshots"]), (say("Read"), c["read"])]


def media_line(say, media, size_text):
    return " · ".join(filter(None, (say(media["label"]), media.get("name") or media.get("mime"),
                                     size_text(media["size"]) if media.get("size") else None)))


def preview(media_root, file, limit):
    if not media_root or not file:
        return None
    path = Path(media_root) / file["sha256"]
    try:
        if path.stat().st_size > limit:
            return None
        return path
    except OSError:
        return None


CSS = """
.secret-chat{margin:18px 0 28px;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--card)}
.secret-chat-head{display:flex;gap:14px;align-items:center;padding:16px 18px;background:var(--violettint)}
.secret-chat-head .lock{display:grid;place-items:center;flex:none;width:46px;height:46px;border-radius:50%;background:var(--violet);color:#fff}
.secret-chat-head .lock svg{width:22px;height:22px}
.secret-chat-head h3{margin:0;font-size:18px;color:var(--ink)}.secret-chat-head p{margin:2px 0 0;color:var(--muted);font-size:13px}
.secret-chat .kv{margin:0;border-radius:0}.secret-chat .kv code{word-break:break-all}
.secret-counts{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:1px;margin:0;padding:0;list-style:none;background:var(--line);border-block:1px solid var(--line)}
.secret-counts li{display:grid;gap:2px;padding:10px 14px;background:var(--card)}
.secret-counts b{font-size:20px;color:var(--ink)}.secret-counts span{color:var(--muted);font-size:12px}
.secret-thread{display:flex;flex-direction:column;gap:8px;padding:18px;background:var(--chatbg)}
.secret-event{align-self:center;max-width:85%;margin:0;padding:4px 12px;border-radius:999px;background:var(--card);color:var(--muted);font-size:12px;text-align:center}
.secret-bubble{align-self:flex-start;display:grid;gap:4px;max-width:min(70ch,78%);padding:8px 12px 6px;border-radius:16px 16px 16px 6px;background:var(--bubble);color:var(--ink);box-shadow:var(--shadow-sm);overflow-wrap:anywhere}
.secret-bubble.out{align-self:flex-end;border-radius:16px 16px 6px 16px;background:var(--tint)}
.secret-bubble.deleted{background:var(--badtint);outline:1px solid var(--bad-line)}
.secret-bubble .text{white-space:pre-wrap;unicode-bidi:plaintext}
.secret-bubble img{display:block;max-width:min(100%,360px);max-height:280px;border-radius:10px;object-fit:contain}
.secret-bubble .file,.secret-bubble .meta{color:var(--muted);font-size:12px}.secret-bubble .meta{justify-self:end}
.secret-bubble .badge{justify-self:start;padding:1px 8px;border-radius:999px;background:var(--bad);color:#fff;font-size:11px;font-weight:650}
.secret-bubble .badge.timer{background:var(--warn)}
.secret-chat .limited{margin:0;padding:10px 18px;background:var(--warntint);color:var(--warn);font-size:13px}
[dir=rtl] .secret-bubble{align-self:flex-end;border-radius:16px 16px 6px 16px}[dir=rtl] .secret-bubble.out{align-self:flex-start;border-radius:16px 16px 16px 6px}
@media print{.secret-bubble{box-shadow:none;outline:1px solid var(--line)}}
"""


def html(conversations, say, number, when, size_text, media_root=None, archive=False):
    if not conversations:
        return ""
    e = lambda value: escape("" if value is None else str(value))
    lock = '<svg class="i" aria-hidden="true"><use href="#i-lock"/></svg>'
    parts = ['<section class="card long" id="secret-conversation"><h2><span class="sec-icon tone-violet">' + lock
             + '</span><span class="num">' + str(number) + '</span><span class="section-title">' + e(say(TITLE))
             + '</span></h2><p class="lead">' + e(say(LEAD)) + "</p>"]
    for chat in conversations:
        parts.append('<article class="secret-chat" id="secret-chat-' + e(chat["id"]) + '"><header class="secret-chat-head">'
                     '<span class="lock">' + lock + '</span><div><h3>'
                     + e(say(CHAT_WITH, name=peer_label(say, chat["peer"]))) + "</h3><p>" + e("#" + str(chat["id"])) + "</p></div></header>")
        parts.append('<table class="kv">' + "".join("<tr><th>" + e(k) + "</th><td>" + (("<code>" + e(v) + "</code>") if k == say(KEY) else e(v))
                                                     + "</td></tr>" for k, v in facts(say, chat, when) if v) + "</table>")
        parts.append('<ul class="secret-counts">' + "".join("<li><b>" + e(v) + "</b><span>" + e(k) + "</span></li>"
                                                           for k, v in counts(say, chat)) + "</ul>")
        if chat["truncated"]:
            parts.append('<p class="limited">' + e(say(LIMITED, n=MESSAGE_LIMIT)) + "</p>")
        parts.append('<div class="secret-thread">')
        for item in chat["items"]:
            if item["type"] == "event":
                parts.append('<p class="secret-event">' + e(when(item["at"])) + " · " + e(event_text(say, item, when)) + "</p>")
                continue
            classes = "secret-bubble" + (" out" if item["direction"] == "out" else "") + (" deleted" if item["deleted"] else "")
            parts.append('<div class="' + classes + '" id="secret-record-' + e(item["seq"]) + '">')
            if item["deleted"]:
                parts.append('<span class="badge">' + e(say("deleted by the other side; kept here")) + "</span>")
            if item["ttl"]:
                parts.append('<span class="badge timer">' + e(say("timer {n} s", n=item["ttl"])) + "</span>")
            media = item["media"]
            if media and media["image"] and item["file"] and (media.get("mime") in IMAGES or not media.get("mime")):
                if archive:
                    parts.append('<img loading="lazy" alt="' + e(media.get("name") or say("Photo")) + '" src="media/' + e(item["file"]["sha256"]) + '">')
                else:
                    found = preview(media_root, item["file"], PREVIEW_BYTES)
                    if found is not None:
                        parts.append('<img loading="lazy" alt="' + e(media.get("name") or say("Photo")) + '" src="data:'
                                     + e(media.get("mime") or "image/jpeg") + ";base64," + base64.b64encode(found.read_bytes()).decode("ascii") + '">')
            if item["text"]:
                parts.append('<div class="text">' + e(item["text"]) + "</div>")
            if media:
                parts.append('<div class="file">' + e(media_line(say, media, size_text))
                             + (" · SHA-256 " + e(item["file"]["sha256"]) if item["file"] else "") + "</div>")
            parts.append('<span class="meta">' + e(say("Sent") if item["direction"] == "out" else say("Received")) + " · "
                         + e(when(item["at"])) + " · " + e(say("Record #{n}", n=item["seq"])) + "</span></div>")
        parts.append("</div></article>")
    parts.append("</section>")
    return "".join(parts)


def pdf(lay, conversations, say, when, size_text, colors, media_root=None):
    if not conversations:
        return
    ink, muted, bad, warn = colors
    page = lay.pdf
    lay.section(say(TITLE), say(LEAD))
    for chat in conversations:
        lay.need(40)
        lay.text(say(CHAT_WITH, name=peer_label(say, chat["peer"])), size=12.5, style="B", color=ink)
        lay.gap(1.2)
        lay.kv([(k, v) for k, v in facts(say, chat, when) if v])
        numbers = counts(say, chat)
        lay.grid([label for label, _ in numbers], [[str(value) for _, value in numbers]])
        if chat["truncated"]:
            lay.callout(say(LIMITED, n=MESSAGE_LIMIT), warn)
        lay.gap(2)
        width = page.epw
        bubble = width * 0.74
        for item in chat["items"]:
            if item["type"] == "event":
                lay.need(6)
                page.set_font("Sans", "", 7.4)
                page.set_text_color(*muted)
                page.multi_cell(width, 3.6, when(item["at"]) + " · " + event_text(say, item, when), align="C",
                                new_x=lay.XPos.LMARGIN, new_y=lay.YPos.NEXT)
                page.ln(1.4)
                continue
            out = item["direction"] == "out"
            inner = bubble - 8
            blocks = []
            if item["deleted"]:
                blocks.append(("badge", say("deleted by the other side; kept here"), bad))
            if item["ttl"]:
                blocks.append(("badge", say("timer {n} s", n=item["ttl"]), warn))
            media = item["media"]
            if media and media["image"] and item["file"]:
                image = preview(media_root, item["file"], PDF_IMAGE_BYTES)
                if image is not None:
                    try:
                        from PIL import Image
                        with Image.open(image) as picture:
                            w, h = picture.size
                        scale = min(inner / w, 52 / h)
                        blocks.append(("image", str(image), (w * scale, h * scale)))
                    except Exception:
                        pass
            if item["text"]:
                blocks.append(("text", item["text"], ink))
            if media:
                blocks.append(("small", media_line(say, media, size_text) + (" · SHA-256 " + item["file"]["sha256"] if item["file"] else ""), muted))
            blocks.append(("meta", (say("Sent") if out else say("Received")) + " · " + when(item["at"]) + " · "
                           + say("Record #{n}", n=item["seq"]), muted))
            heights = []
            for kind, value, extra in blocks:
                if kind == "image":
                    heights.append(extra[1] + 1)
                    continue
                page.set_font("Sans", "B" if kind == "badge" else "", 9 if kind == "text" else 7.2)
                heights.append(page.multi_cell(inner, 4.2 if kind == "text" else 3.4, value, dry_run=True, output="HEIGHT"))
            total = sum(heights) + len(blocks) + 5
            lay.need(total + 2)
            left = page.l_margin + (width - bubble if out != lay.rtl else 0)
            top = page.get_y()
            fill = (253, 236, 236) if item["deleted"] else (227, 241, 255) if out else (244, 246, 248)
            border = (242, 184, 181) if item["deleted"] else (205, 222, 240) if out else (222, 227, 232)
            with page.local_context(fill_color=fill, draw_color=border, line_width=0.2):
                page.rect(left, top, bubble, total, style="DF", round_corners=True, corner_radius=3)
            y = top + 3
            for (kind, value, extra), height in zip(blocks, heights):
                if kind == "image":
                    page.image(value, x=left + 4, y=y, w=extra[0], h=extra[1])
                else:
                    page.set_xy(left + 4, y)
                    page.set_font("Sans", "B" if kind == "badge" else "", 9 if kind == "text" else 7.2)
                    page.set_text_color(*extra)
                    page.multi_cell(inner, 4.2 if kind == "text" else 3.4, value, align="R" if kind == "meta" else "L")
                y += height + 1
            page.set_xy(page.l_margin, top + total + 2.2)
        lay.gap(4)
