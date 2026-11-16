import json
import xml.etree.ElementTree as ET

from . import message_details, report_analytics
from .report_media import chat_label, reference, sequence

MAX_OCCURRENCES = 200_000
SHOWN = 20
GRAPH_EDGES = 1000
REFERENCES = 100
TITLE = "Observed forwarding sources"
NOTE = ("Sources come from saved forward headers. Names remain text. Counts use distinct messages. "
        "Graph arrows point from the observed chat to the referenced peer.")
LISTED = "Source groups: {n}. Listed: {shown}."
PARTIAL = "Source comparison limit reached: {n} additional occurrences were not compared."
UNRESOLVED = "Source without a peer ID"


def text_keys():
    return [TITLE, NOTE, LISTED, PARTIAL, UNRESOLVED, "Observed chat", "Forward source", "Messages",
            "First observed", "Last observed"]


def header(payload):
    raw = payload.get("raw")
    raw = raw if isinstance(raw, dict) else {}
    supplied = raw.get("fwd_from")
    found = message_details.forward(supplied)
    if not found:
        details = payload.get("details")
        found = details.get("forwarded_from") if isinstance(details, dict) else None
    if not isinstance(found, dict):
        return None
    result = {key: found[key] for key in ("from_id", "from_name", "date", "channel_post", "post_author",
              "saved_from_id", "saved_from_message_id", "imported") if key in found}
    if isinstance(supplied, dict):
        result.update(saved_from_sender_id=message_details.peer_id(supplied.get("saved_from_id")),
                      saved_from_name=supplied.get("saved_from_name"), saved_date=supplied.get("saved_date"))
    return result or None


class Sources:
    def __init__(self):
        self.groups = {}
        self.occurrences = self.dropped = 0

    def note(self, kind, peer, name, ref, detail=None):
        if ref["chat"] is None or type(ref["seq"]) is not int:
            return
        peer = peer if type(peer) is int and peer != 0 else None
        name = name if isinstance(name, str) else None
        key = (kind, ref["chat"], peer, name if peer is None else None, bool((detail or {}).get("imported")))
        place = ref["seq"] if kind == "recommended" else ref["message"]
        if kind == "forwarded_from" and type(place) is not int:
            return
        places = self.groups.get(key)
        item = {**ref, "forward": detail} if detail else ref
        if places is not None and place in places:
            if sequence(item) < sequence(places[place]):
                places[place] = item
            return
        if self.occurrences >= MAX_OCCURRENCES:
            self.dropped += 1
            return
        if places is None:
            places = self.groups[key] = {}
        places[place] = item
        self.occurrences += 1

    def add(self, event):
        payload, kind = event["payload"], event["kind"]
        ref = {**reference(event), "sender": report_analytics.sender_id(event)}
        if kind in ("message.new", "message.snapshot", "message.recovered", "message.edited"):
            if found := header(payload):
                self.note("forwarded_from", found.get("from_id"), found.get("from_name"), ref, found)
        elif kind == "graph.suggestions":
            for item in payload.get("channels") or []:
                if isinstance(item, dict) and type(item.get("chat_id")) is int:
                    self.note("recommended", item["chat_id"], None, ref)

    def result(self, sender=None, shown=SHOWN):
        rows, edges = [], []
        for (kind, chat, peer, name, imported), places in self.groups.items():
            timeline = sorted((ref for ref in places.values() if sender is None or ref["sender"] == sender), key=sequence)
            if not timeline:
                continue
            entry = {"type": kind, "chat": chat, "peer_id": peer, "from_name": name, "imported": imported,
                     "count": len(timeline), "first": timeline[0], "last": timeline[-1],
                     "records": [ref["seq"] for ref in timeline[:REFERENCES]], "timeline": timeline[:REFERENCES],
                     "references_not_listed": max(0, len(timeline) - REFERENCES)}
            if kind == "forwarded_from":
                rows.append(entry)
            if peer is not None and not imported:
                edges.append(entry)
        rank = lambda row: (-row["count"], row["first"]["seq"], str(row["peer_id"]))
        rows.sort(key=rank)
        edges.sort(key=rank)
        return {"format": "tgwitness-observed-sources-v1", "meaning": NOTE,
                "total": len(rows), "rows": rows[:shown], "not_listed": max(0, len(rows) - shown),
                "edges": edges[:GRAPH_EDGES], "edges_not_listed": max(0, len(edges) - GRAPH_EDGES),
                "dropped": self.dropped, "complete": not self.dropped,
                "limits": {"occurrences": MAX_OCCURRENCES, "references": REFERENCES, "edges": GRAPH_EDGES}}

    def people(self, shown=SHOWN):
        people = {}
        for key, places in self.groups.items():
            if key[0] != "forwarded_from":
                continue
            for place, ref in places.items():
                if ref["sender"] is not None:
                    person = people.setdefault(ref["sender"], Sources())
                    person.groups.setdefault(key, {})[place] = ref
        result = {}
        for sender, person in people.items():
            person.dropped = self.dropped
            result[sender] = {key: value for key, value in person.result(shown=shown).items()
                              if key not in ("edges", "edges_not_listed")}
        return result


def gexf(data, titles):
    root = ET.Element("gexf", {"xmlns": "http://gexf.net/1.3", "version": "1.3"})
    meta = ET.SubElement(root, "meta")
    ET.SubElement(meta, "creator").text = "TgWitness"
    ET.SubElement(meta, "description").text = (NOTE + " Omitted edges: " + str(data["edges_not_listed"])
                                              + "; unexamined occurrences: " + str(data["dropped"]) + ".")
    graph = ET.SubElement(root, "graph", {"mode": "static", "defaultedgetype": "directed"})
    attributes = ET.SubElement(graph, "attributes", {"class": "edge"})
    for key in ("relation", "records", "record_hashes", "first_observed", "last_observed", "references_not_listed"):
        ET.SubElement(attributes, "attribute", {"id": key, "title": key, "type": "string"})
    nodes, edges = ET.SubElement(graph, "nodes"), ET.SubElement(graph, "edges")
    peers = {row[key] for row in data["edges"] for key in ("chat", "peer_id")}
    for peer in sorted(peers, key=str):
        ET.SubElement(nodes, "node", {"id": str(peer), "label": xml_text(titles.get(peer) or str(peer))})
    for index, row in enumerate(data["edges"]):
        edge = ET.SubElement(edges, "edge", {"id": str(index), "source": str(row["chat"]),
                                            "target": str(row["peer_id"]), "weight": str(row["count"]),
                                            "label": row["type"], "kind": row["type"]})
        values = {"relation": row["type"], "records": json.dumps(row["records"]),
                  "record_hashes": json.dumps({str(ref["seq"]): ref["hash"] for ref in [*row["timeline"], row["last"]]}),
                  "first_observed": row["first"]["at"] or "", "last_observed": row["last"]["at"] or "",
                  "references_not_listed": str(row["references_not_listed"])}
        attributes = ET.SubElement(edge, "attvalues")
        for key, value in values.items():
            ET.SubElement(attributes, "attvalue", {"for": key, "value": xml_text(value)})
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def xml_text(value):
    return "".join(char for char in str(value) if char in "\t\n\r" or "\x20" <= char <= "\ud7ff"
                   or "\ue000" <= char <= "\ufffd" or "\U00010000" <= char <= "\U0010ffff")


def html(say, number, data, titles):
    from .report import e, ref_key, ref_label, section, table, when

    def seen(ref):
        return when(ref["at"]) + ' · <a href="#data" data-goto="' + e(ref_key(ref)) + '">' + e(ref_label(ref)) + "</a>"

    rows = [[chat_label(row["chat"], titles),
             chat_label(row["peer_id"], titles) if row["peer_id"] is not None
             else '<bdi dir="auto">' + e(row["from_name"] or say(UNRESOLVED)) + "</bdi>",
             str(row["count"]), seen(row["first"]), seen(row["last"])] for row in data["rows"]]
    out = section(number, "forward-sources", say(TITLE), say(NOTE))
    out += "<p>" + e(say(LISTED, n=data["total"], shown=len(rows))) + "</p>"
    out += table([say("Observed chat"), say("Forward source"), say("Messages"), say("First observed"), say("Last observed")], rows)
    if data["dropped"]:
        out += '<p class="hint">' + e(say(PARTIAL, n=data["dropped"])) + "</p>"
    return out + "</section>"


def pdf(lay, say, data, titles):
    lay.section(say(TITLE), say(NOTE))
    lay.text(say(LISTED, n=data["total"], shown=len(data["rows"])))
    lay.grid([say("Observed chat"), say("Forward source"), say("Messages"), say("First observed")],
             [[str(titles.get(row["chat"]) or row["chat"]),
               str(row["peer_id"]) if row["peer_id"] is not None else row["from_name"] or say(UNRESOLVED),
               str(row["count"]), "#" + str(row["first"]["seq"])] for row in data["rows"]], (30, 35, 10, 25))
    if data["dropped"]:
        lay.text(say(PARTIAL, n=data["dropped"]))
