import re

from . import device_attribution, report_analytics

MAX_KEYS = 100_000
MAX_OCCURRENCES = 200_000
SHOWN = 20
TIMELINE = 100
TITLE = "Repeated media in this archive"
NOTE = ("Document ID, SHA-256 and dHash are separate match types. dHash matches are visual leads. "
        "First observed follows journal order within the report selection.")
LABELS = {"document_id": "Telegram document ID", "sha256": "Saved-byte SHA-256", "dhash": "Matching image dHash"}
PARTIAL = "Comparison limits reached: {n} additional occurrences were not compared. Counts are lower bounds."
LISTED = "Matching groups: {n}. Listed: {shown}."
MORE = "Further occurrences not listed: {n}."


def text_keys():
    return [TITLE, NOTE, PARTIAL, LISTED, MORE, *LABELS.values(),
            "Messages", "First observed", "Last observed", "Observation timeline"]


def reference(event):
    return {"seq": event["seq"], "at": event.get("observed_at"), "chat": report_analytics.chat_key(event),
            "message": event.get("message_id"), "hash": event.get("hash")}


def sequence(ref):
    return ref["seq"]


def chat_label(chat, titles):
    from .report import e
    title = titles.get(chat) or titles.get(str(chat))
    return '<bdi dir="' + ("auto" if title else "ltr") + '">' + e(title or chat) + "</bdi>"


class MediaRepeats:
    def __init__(self):
        self.groups, self.images = {}, {}
        self.occurrences = self.dropped = 0

    def note(self, kind, value, ref):
        if ref["chat"] is None or type(ref["message"]) is not int or type(ref["seq"]) is not int:
            return
        key, place = (kind, value), (ref["chat"], ref["message"])
        places = self.groups.get(key)
        if places is not None and place in places:
            if sequence(ref) < sequence(places[place]):
                places[place] = ref
            return
        if self.occurrences >= MAX_OCCURRENCES or places is None and len(self.groups) >= MAX_KEYS:
            self.dropped += 1
            return
        if places is None:
            places = self.groups[key] = {}
        places[place] = ref
        self.occurrences += 1

    def add(self, event):
        kind, payload = event["kind"], event["payload"]
        ref = reference(event)
        if kind in ("message.new", "message.snapshot", "message.recovered", "message.edited"):
            document = device_attribution.document_id(payload.get("raw"))
            if document:
                self.note("document_id", document, ref)
        if kind in ("media.saved", "secret_chat.file"):
            digest = payload.get("media_sha256")
            if isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest):
                self.note("sha256", digest, ref)

    def image(self, digest, dhash):
        if ("sha256", digest) in self.groups and isinstance(dhash, str) and re.fullmatch(r"[0-9a-f]{16}", dhash):
            self.images[digest] = dhash

    def result(self):
        candidates = [(kind, value, places, None) for (kind, value), places in self.groups.items()
                      if len(places) > 1]
        visual = {}
        for digest, dhash in self.images.items():
            visual.setdefault(dhash, []).append(digest)
        for dhash, files in visual.items():
            if len(files) < 2:
                continue
            places = {}
            for digest in sorted(files):
                for place, ref in self.groups[("sha256", digest)].items():
                    if place not in places or sequence(ref) < sequence(places[place]):
                        places[place] = {**ref, "sha256": digest}
            if len(places) > 1:
                candidates.append(("dhash", dhash, places, sorted(files)))
        candidates.sort(key=lambda item: (-len(item[2]), item[0], item[1]))
        rows = []
        for kind, value, places, files in candidates[:SHOWN]:
            timeline = sorted(places.values(), key=sequence)
            row = {"match": kind, "value": value, "messages": len(places),
                   "chats": sorted({place[0] for place in places}, key=str),
                   "first": timeline[0], "last": timeline[-1], "timeline": timeline[:TIMELINE],
                   "timeline_not_listed": max(0, len(timeline) - TIMELINE)}
            if files is not None:
                row.update(files=files[:TIMELINE], files_not_listed=max(0, len(files) - TIMELINE))
            rows.append(row)
        return {"format": "tgwitness-media-repeats-v1", "meaning": NOTE, "total": len(candidates), "rows": rows,
                "dropped": self.dropped, "compared_keys": len(self.groups), "occurrences": self.occurrences,
                "limits": {"keys": MAX_KEYS, "occurrences": MAX_OCCURRENCES, "groups_shown": SHOWN,
                           "timeline": TIMELINE}, "complete": not self.dropped}


def html(say, number, data, titles):
    from .report import e, ref_key, ref_label, section, table, when
    from .report_repeats import CHATS_SHOWN

    def seen(ref):
        return when(ref["at"]) + ' · <a href="#data" data-goto="' + e(ref_key(ref)) + '">' + e(ref_label(ref)) + "</a>"

    out = section(number, "repeated-media", say(TITLE), say(NOTE))
    out += "<p>" + e(say(LISTED, n=data["total"], shown=len(data["rows"]))) + "</p>"
    for row in data["rows"]:
        out += "<h3>" + e(say(LABELS[row["match"]])) + '</h3><p><code dir="ltr">' + e(row["value"]) + "</code></p>"
        chats = [chat_label(chat, titles) for chat in row["chats"][:CHATS_SHOWN]]
        if len(row["chats"]) > CHATS_SHOWN:
            chats.append('<bdi dir="ltr">+' + str(len(row["chats"]) - CHATS_SHOWN) + "</bdi>")
        out += table([say("Chats"), say("Messages"), say("First observed"), say("Last observed")],
                     [[", ".join(chats), str(row["messages"]),
                       seen(row["first"]), seen(row["last"])]])
        out += "<details><summary>" + e(say("Observation timeline")) + "</summary><ol>"
        for ref in row["timeline"]:
            out += "<li>" + seen(ref) + " · " + chat_label(ref["chat"], titles) + "</li>"
        out += "</ol>"
        if row["timeline_not_listed"]:
            out += "<p>" + e(say(MORE, n=row["timeline_not_listed"])) + "</p>"
        out += "</details>"
    if data["dropped"]:
        out += '<p class="hint">' + e(say(PARTIAL, n=data["dropped"])) + "</p>"
    return out + "</section>"


def pdf(lay, say, data, titles):
    from .report import utc_text
    from .report_repeats import chat_names

    lay.section(say(TITLE), say(NOTE))
    lay.text(say(LISTED, n=data["total"], shown=len(data["rows"])))
    for row in data["rows"]:
        lay.text(say(LABELS[row["match"]]) + ": " + row["value"])
        lay.text(", ".join(chat_names(row["chats"], titles)) + " · " + say("Messages") + ": " + str(row["messages"]))
        for key, label in (("first", "First observed"), ("last", "Last observed")):
            ref = row[key]
            lay.text(say(label) + ": " + utc_text(ref["at"]) + " · #" + str(ref["seq"]))
    if data["dropped"]:
        lay.text(say(PARTIAL, n=data["dropped"]))
