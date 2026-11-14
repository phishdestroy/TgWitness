import hashlib

MIN_CHARS = 24
MAX_TEXTS = 200_000
MAX_PLACES = 10_000
SHOWN = 20
EXCERPT = 200
CHATS_SHOWN = 5
TITLE = "Texts repeated across chats"
NOTE = ("The same message text observed in more than one chat, compared after letter case and spacing are normalised. "
        "Texts shorter than {n} characters are not compared. Matching text is a lead: it does not show who wrote the "
        "copies or that they are connected.")
FOUND = "Texts found in more than one chat: {n}."
LISTED = "Texts found in more than one chat: {n}. Listed: the {shown} found in the largest number of chats."
PARTIAL = "More than {n} distinct texts: later texts were not compared."


def text_keys():
    return [TITLE, NOTE, FOUND, LISTED, PARTIAL, "Text", "Chats", "Messages", "First observed", "Last observed"]


def normal(text):
    return " ".join(text.casefold().split())


def excerpt(text):
    text = " ".join(text.split())
    return text if len(text) <= EXCERPT else text[:EXCERPT - 1].rstrip() + "…"


class Repeats:
    def __init__(self):
        self.texts, self.dropped = {}, 0

    def add(self, text, chat, message, seq, at):
        if not isinstance(text, str) or chat is None:
            return
        compared = normal(text)
        if len(compared) < MIN_CHARS:
            return
        key = hashlib.blake2b(compared.encode("utf-8"), digest_size=16).digest()
        entry, place = self.texts.get(key), (chat, message)
        seen = (at or "", seq, chat, message, excerpt(text) if entry is None or isinstance(entry, tuple) else None)
        if entry is None:
            if len(self.texts) >= MAX_TEXTS:
                self.dropped += 1
            else:
                self.texts[key] = seen
            return
        if isinstance(entry, tuple):
            if (entry[2], entry[3]) == place:
                return
            entry = self.texts[key] = {"places": {(entry[2], entry[3])}, "chats": {entry[2]}, "first": entry,
                                       "last": entry}
        if place in entry["places"] or len(entry["places"]) >= MAX_PLACES:
            return
        entry["places"].add(place)
        entry["chats"].add(chat)
        if order(seen) < order(entry["first"]):
            entry["first"] = seen[:4] + (seen[4] or excerpt(text),)
        entry["last"] = max(entry["last"], seen, key=order)

    def result(self):
        groups = [entry for entry in self.texts.values() if isinstance(entry, dict) and len(entry["chats"]) > 1]
        groups.sort(key=lambda g: (-len(g["chats"]), -len(g["places"]), g["first"][0]))
        return {"min_chars": MIN_CHARS, "compared": len(self.texts), "dropped": self.dropped, "limit": MAX_TEXTS,
                "total": len(groups), "rows": [row(group) for group in groups[:SHOWN]]}


def order(seen):
    return seen[0], seen[1] if isinstance(seen[1], int) else -1


def moment(seen):
    return {"at": seen[0] or None, "seq": seen[1], "chat": seen[2], "message": seen[3]}


def row(group):
    return {"text": group["first"][4], "chats": sorted(group["chats"], key=lambda chat: (type(chat) is not int, chat if type(chat) is int else str(chat))),
            "messages": len(group["places"]),
            "messages_capped": len(group["places"]) >= MAX_PLACES, "first": moment(group["first"]),
            "last": moment(group["last"])}


def chat_names(chats, titles):
    names = [str(titles.get(chat) or titles.get(str(chat)) or chat) for chat in chats[:CHATS_SHOWN]]
    return names + (["+" + str(len(chats) - CHATS_SHOWN)] if len(chats) > CHATS_SHOWN else [])


def summary(say, data):
    if data["total"] > len(data["rows"]):
        return say(LISTED, n=data["total"], shown=len(data["rows"]))
    return say(FOUND, n=data["total"])


def html(say, number, data, titles):
    from .report import e, num, ref_key, ref_label, section, table, when
    if not data or not data.get("rows"):
        return ""

    def seen(item):
        target = ('<a href="#data" data-goto="' + e(ref_key(item)) + '">' + e(ref_label(item)) + "</a>"
                  if item.get("seq") is not None else "")
        return when(item["at"]) + (" · " + target if target else "")
    rows = [['<span dir="auto">' + e(r["text"]) + "</span>", e(", ".join(chat_names(r["chats"], titles))),
             num(r["messages"]) + ("+" if r["messages_capped"] else ""), seen(r["first"]), seen(r["last"])]
            for r in data["rows"]]
    out = (section(number, "repeated-texts", say(TITLE), say(NOTE, n=data["min_chars"])) + '<p class="lead">'
           + e(summary(say, data)) + "</p>"
           + table([say("Text"), say("Chats"), say("Messages"), say("First observed"), say("Last observed")], rows))
    if data.get("dropped"):
        out += '<p class="hint">' + e(say(PARTIAL, n=data["limit"])) + "</p>"
    return out + "</section>"


def pdf(lay, say, data, titles):
    from .report import utc_text
    if not data or not data.get("rows"):
        return
    lay.section(say(TITLE), say(NOTE, n=data["min_chars"]))
    lay.text(summary(say, data))

    def seen(item):
        return (utc_text(item["at"]) if item["at"] else "—") + (" · #" + str(item["seq"]) if item.get("seq") is not None else "")
    lay.grid([say("Text"), say("Chats"), say("Messages"), say("First observed"), say("Last observed")],
             [[r["text"], ", ".join(chat_names(r["chats"], titles)), str(r["messages"]) + ("+" if r["messages_capped"] else ""),
               seen(r["first"]), seen(r["last"])] for r in data["rows"]], (38, 22, 10, 15, 15))
    if data.get("dropped"):
        lay.text(say(PARTIAL, n=data["limit"]), size=9)
