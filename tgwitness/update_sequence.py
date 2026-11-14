import time
from datetime import datetime, timezone

VERSION = 1
SEGMENT_LIMIT = 2000
DIFFERENCES_LISTED = 16
CHANNEL_BASE = -1000000000000
SEQUENCE_MEANING = ("Telegram numbers message-related updates with pts, one sequence for the account (private chats and "
                    "basic groups) and one per channel or supergroup. Each segment is a stretch of that sequence this "
                    "collector's Telegram client accepted without a hole: every update numbered after 'from' up to 'to' "
                    "arrived, pushed live or returned by a difference request. Stretches not written here are not "
                    "claimed.")
CLOSED_MEANING = ("The update sequence named here is whole again from whole_from_pts: the first stretch recorded after "
                  "the break starts there. Updates between the break and that position remain missing.")


def stamp(moment):
    return datetime.fromtimestamp(moment, timezone.utc).isoformat(timespec="milliseconds")


def chat_of(key):
    return None if key == "account" else CHANNEL_BASE - key


class SequenceLog:
    def __init__(self, clock=time.time):
        self.clock = clock
        self.open, self.done, self.notes, self.unclaimed, self.closures, self.closed = {}, {}, {}, {}, {}, []
        self.held, self.flushed = 0, []

    def finish(self, key):
        current = self.open.pop(key, None)
        if current is not None:
            self.done.setdefault(key, []).append(current)
            self.held += 1

    def segment(self, key, start, method, began, now):
        self.finish(key)
        current = self.open[key] = {"from": start, "to": start, "updates": 0, "types": {}, "first_at": now,
                                    "last_at": now, "method": method, "start": began}
        if key in self.closures:
            gap = self.closures.pop(key)
            self.closed.append((key, {**gap, "whole_from_pts": start, "by": method, "at": now}))
        return current

    def update(self, key, pts, count, name, known, method):
        now, start = self.clock(), pts - count
        current = self.open.get(key)
        if current is None or current["method"] != method or current["to"] != start:
            current = self.segment(key, start, method, "known_state" if known else "first_update", now)
        current["to"], current["last_at"] = pts, now
        current["updates"] += 1
        current["types"][name] = current["types"].get(name, 0) + 1

    def difference(self, key, before, after, method, result, final, types):
        now, count = self.clock(), sum(types.values())
        current = self.open.get(key)
        if before == after and not count and current is not None and current["to"] == before:
            current["last_at"] = now
            current["empty_differences"] = current.get("empty_differences", 0) + 1
            return
        if current is None or current["method"] != method or current["to"] != before:
            current = self.segment(key, before, method, "known_state", now)
        current["to"], current["last_at"] = after, now
        current["updates"] += count
        for name, number in types.items():
            current["types"][name] = current["types"].get(name, 0) + number
        listed = current.setdefault("differences", [])
        if len(listed) < DIFFERENCES_LISTED:
            listed.append({"pts_before": before, "pts_after": after, "result": result, "final": final,
                           "updates": count, "at": now})
        current["differences_total"] = current.get("differences_total", 0) + 1

    def event(self, key, name, **values):
        self.notes.setdefault(key, []).append({"event": name, "at": self.clock(), **values})
        self.held += 1

    def gap(self, key, record, pts, reason):
        self.finish(key)
        self.closures[key] = {"gap_record": record, "pts_after_gap": pts, "reason": reason}

    def unclaim(self, key, start, end, count, reason):
        listed = self.unclaimed.setdefault(key, [])
        if listed and listed[-1]["to"] == start and listed[-1]["reason"] == reason:
            listed[-1]["to"], listed[-1]["updates"] = end, listed[-1]["updates"] + count
            return
        listed.append({"from": start, "to": end, "updates": count, "reason": reason})
        self.held += 1

    def discard(self, reason):
        for key in list(self.open):
            self.finish(key)
        for key, segments in self.done.items():
            for item in segments:
                self.unclaim(key, item["from"], item["to"], item["updates"], reason)
        self.done = {}

    def flush(self, keep):
        for key in list(self.open):
            self.finish(key)
        keys = list(dict.fromkeys([*self.done, *self.notes, *self.unclaimed]))
        sequences = []
        for key in keys:
            if not keep(key):
                continue
            entry = {"scope": "account" if key == "account" else "channel", "chat_id": chat_of(key)}
            if key != "account":
                entry["channel_id"] = key
            segments = [{**item, "first_at": stamp(item["first_at"]), "last_at": stamp(item["last_at"]),
                         **({"differences": [{**d, "at": stamp(d["at"])} for d in item["differences"]]}
                            if "differences" in item else {})} for item in self.done.get(key, [])]
            if segments:
                entry["segments"] = segments
            if self.notes.get(key):
                entry["events"] = [{**note, "at": stamp(note["at"])} for note in self.notes[key]]
            if self.unclaimed.get(key):
                entry["unclaimed"] = self.unclaimed[key]
            sequences.append(entry)
        closed = [(chat_of(key), {**item, "at": stamp(item["at"])}) for key, item in self.closed if keep(key)]
        self.done, self.notes, self.unclaimed, self.closed, self.held = {}, {}, {}, [], 0
        self.flushed = [key for key in keys if keep(key)]
        return sequences, closed

    def written(self, record):
        for key in self.flushed:
            if key in self.closures and self.closures[key]["gap_record"] is None:
                self.closures[key]["gap_record"] = record
