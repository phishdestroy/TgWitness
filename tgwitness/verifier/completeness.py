from .common import (
    datetime,
)
COMPLETENESS_FORMAT = "tgwitness-sequence-continuity-v1"
COMPLETENESS_KINDS = ("coverage.sequence", "coverage.gap", "coverage.gap_closed")
COMPLETENESS_METHODS = ("push", "getDifference", "getChannelDifference")
COMPLETENESS_CHANNEL_BASE = -1000000000000
COMPLETENESS_LISTED = 20
COMPLETENESS_PROVES = ("Telegram numbers message-related updates with pts: one sequence for the account (private chats "
                       "and basic groups together) and one per channel or supergroup. An unbroken stretch proves that "
                       "every update Telegram numbered in that sequence between its first and last pts reached this "
                       "collector's Telegram client, pushed live or returned by getDifference or getChannelDifference.")
COMPLETENESS_LIMITS = ("It says nothing about content Telegram never sent to this account, about intervals before the "
                       "first recorded pts, or about stretches the collector did not write down. Any pts advance not "
                       "covered by a recorded segment or difference is shown as a break. Times are when the collector "
                       "accepted the updates; pts bounds are those of whole recorded segments.")
COMPLETENESS_CHANNELS = ("Channels and supergroups: a getChannelDifference that is not final covers the pts it returned "
                         "and the next request continues from there; updateChannelTooLong starts such a recovery and is "
                         "not a break by itself; a too-long channel difference is a break; leaving a channel or losing "
                         "access to it ends its chain, and a later rejoin starts a new one.")
COMPLETENESS_REASONS = {
    "difference_too_long": "Telegram answered that the difference was too long to deliver",
    "state_dropped:banned": "the account lost access to the channel",
    "state_dropped:no_access_hash": "the channel's access hash was missing, so its position was dropped",
    "unclaimed:observation_paused": "updates arrived while observation was paused and were not recorded",
    "unclaimed:startup_buffer_full": "updates arrived while the startup buffer was full",
    "collector_restarted": "the collector restarted between the two stretches",
    "unaccounted": "pts advanced without a recorded segment or difference",
}


def completeness_int(value):
    return value if type(value) is int else None


def completeness_time(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else None


def completeness_key(scope, chat_id):
    if scope == "account":
        return "account"
    if scope == "channel" and completeness_int(chat_id) is not None and chat_id < COMPLETENESS_CHANNEL_BASE:
        return chat_id
    return None


def completeness_segment(item, record, run):
    if not isinstance(item, dict):
        return None
    start, end, count = (completeness_int(item.get(name)) for name in ("from", "to", "updates"))
    first, last = completeness_time(item.get("first_at")), completeness_time(item.get("last_at"))
    if (start is None or end is None or count is None or end < start or count < 0 or first is None or last is None
            or last < first or item.get("method") not in COMPLETENESS_METHODS):
        return None
    return {"from": start, "to": end, "updates": count, "first_at": first, "last_at": last, "method": item["method"],
            "record": record, "run": run, "differences": completeness_int(item.get("differences_total")) or 0,
            "empty": completeness_int(item.get("empty_differences")) or 0}


def completeness_collect(events):
    found = {}

    def entry(key):
        return found.setdefault(key, {"segments": [], "gaps": [], "drops": [], "unclaimed": [], "events": {},
                                      "invalid": 0})
    closures = {}
    for event in events:
        kind, payload, record = event.get("kind"), event.get("payload"), event.get("seq")
        if kind not in COMPLETENESS_KINDS or not isinstance(payload, dict):
            continue
        if kind == "coverage.sequence":
            for item in payload.get("sequences") if isinstance(payload.get("sequences"), list) else []:
                key = completeness_key(item.get("scope"), item.get("chat_id")) if isinstance(item, dict) else None
                if key is None:
                    continue
                target = entry(key)
                for segment in item.get("segments") if isinstance(item.get("segments"), list) else []:
                    parsed = completeness_segment(segment, record, payload.get("run_id"))
                    if parsed is None:
                        target["invalid"] += 1
                    else:
                        target["segments"].append(parsed)
                for note in item.get("events") if isinstance(item.get("events"), list) else []:
                    name = note.get("event") if isinstance(note, dict) else None
                    if not isinstance(name, str):
                        continue
                    target["events"][name] = target["events"].get(name, 0) + 1
                    if name == "state_dropped":
                        target["drops"].append({"reason": str(note.get("reason")), "pts": completeness_int(note.get("pts")),
                                                "at": completeness_time(note.get("at")), "record": record})
                for lost in item.get("unclaimed") if isinstance(item.get("unclaimed"), list) else []:
                    low, high = (completeness_int(lost.get(n)) if isinstance(lost, dict) else None for n in ("from", "to"))
                    if low is not None and high is not None and high >= low:
                        target["unclaimed"].append({"from": low, "to": high, "reason": str(lost.get("reason")),
                                                    "record": record})
        elif kind == "coverage.gap":
            key = completeness_key(payload.get("scope"), event.get("chat_id"))
            low, high = completeness_int(payload.get("pts_before")), completeness_int(payload.get("pts_after"))
            if key is not None and low is not None and high is not None and high > low:
                entry(key)["gaps"].append({"from": low, "to": high, "record": record,
                                           "at": completeness_time(event.get("observed_at"))})
        elif completeness_int(payload.get("gap_record")) is not None:
            key = completeness_key(payload.get("scope"), event.get("chat_id"))
            closures[(payload["gap_record"], key)] = {"record": record, "at": payload.get("at"),
                                                      "whole_from_pts": completeness_int(payload.get("whole_from_pts"))}
    return found, closures


def completeness_stretches(segments):
    stretches = []
    for segment in sorted(segments, key=lambda s: (s["from"], -s["to"], s["record"] or 0)):
        last = stretches[-1] if stretches else None
        if last is None or segment["from"] > last["pts_to"]:
            last = {"pts_from": segment["from"], "pts_to": segment["from"], "updates": 0, "pushed": 0, "recovered": 0,
                    "from_at": segment["first_at"], "to_at": segment["last_at"], "differences": {},
                    "empty_differences": 0, "overlapping": 0, "partly_overlapping": 0, "segments": []}
            stretches.append(last)
        segment["counted"] = segment["to"] > last["pts_to"] or segment["from"] == segment["to"] == last["pts_to"]
        if segment["to"] > segment["from"] and segment["from"] < last["pts_to"]:
            last["overlapping"] += 1
            if segment["to"] > last["pts_to"]:
                last["partly_overlapping"] += 1
        if segment["counted"]:
            last["updates"] += segment["updates"]
            last["pushed" if segment["method"] == "push" else "recovered"] += segment["updates"]
            last["pts_to"] = max(last["pts_to"], segment["to"])
        if segment["method"] != "push" and segment["differences"]:
            last["differences"][segment["method"]] = last["differences"].get(segment["method"], 0) + segment["differences"]
        last["empty_differences"] += segment["empty"]
        last["from_at"], last["to_at"] = min(last["from_at"], segment["first_at"]), max(last["to_at"], segment["last_at"])
        last["segments"].append(segment)
    return stretches


def completeness_reasons(found, low, high, after, before, previous, following, closures):
    reasons, records, closed = [], [], None
    for gap in found["gaps"]:
        if gap["from"] < high and gap["to"] > low:
            reasons.append("difference_too_long")
            records.append(gap["record"])
            closed = closed or closures.get(gap["record"])
    for drop in found["drops"]:
        inside = drop["pts"] is not None and low <= drop["pts"] <= high
        timed = drop["at"] is not None and after is not None and before is not None and after <= drop["at"] <= before
        if inside or timed:
            reasons.append("state_dropped:" + drop["reason"])
            records.append(drop["record"])
            closed = closed or closures.get(drop["record"])
    for lost in found["unclaimed"]:
        if lost["from"] < high and lost["to"] > low:
            reasons.append("unclaimed:" + lost["reason"])
            records.append(lost["record"])
    if previous is not None and following is not None and previous["run"] != following["run"]:
        reasons.append("collector_restarted")
    return list(dict.fromkeys(reasons)) or ["unaccounted"], sorted({r for r in records if r is not None}), closed


def completeness_breaks(found, stretches, closures):
    breaks, used = [], set()
    for previous, following in zip(stretches, stretches[1:]):
        low, high = previous["pts_to"], following["pts_from"]
        last = max(previous["segments"], key=lambda s: s["to"])
        first = min(following["segments"], key=lambda s: s["from"])
        reasons, records, closed = completeness_reasons(found, low, high, previous["to_at"], following["from_at"],
                                                        last, first, closures)
        used.update(g["record"] for g in found["gaps"] if g["from"] < high and g["to"] > low)
        breaks.append({"pts_from": low, "pts_to": high, "after_at": previous["to_at"], "before_at": following["from_at"],
                       "reasons": reasons, "records": records, "closed_by": closed})
    for gap in found["gaps"]:
        if gap["record"] in used:
            continue
        inside = any(s["pts_from"] <= gap["from"] and gap["to"] <= s["pts_to"] for s in stretches)
        if inside:
            continue
        breaks.append({"pts_from": gap["from"], "pts_to": gap["to"], "after_at": gap["at"], "before_at": gap["at"],
                       "reasons": ["difference_too_long"], "records": [gap["record"]],
                       "closed_by": closures.get(gap["record"])})
    return sorted(breaks, key=lambda b: (b["pts_from"], b["pts_to"]))


def completeness_within(start, end, since, until):
    return (since is None or end is None or end >= since) and (until is None or start is None or start <= until)


def completeness_stamp(value):
    return value.isoformat(timespec="milliseconds") if value is not None else None


def completeness_view(key, found, closures, since, until):
    found = found or {"segments": [], "gaps": [], "drops": [], "unclaimed": [], "events": {}, "invalid": 0}
    stretches = completeness_stretches(found["segments"])
    breaks = completeness_breaks(found, stretches, {record: item for (record, owner), item in closures.items()
                                                    if owner == key})
    result = {"scope": "account" if key == "account" else "channel", "chat_id": None if key == "account" else key,
              "channel_id": None if key == "account" else COMPLETENESS_CHANNEL_BASE - key,
              "events": found["events"], "invalid_segments": found["invalid"]}
    first = min(found["segments"], key=lambda s: (s["first_at"], s["from"])) if found["segments"] else None
    result["not_recorded_before"] = completeness_stamp(first["first_at"]) if first else None
    result["first_recorded_pts"] = first["from"] if first else None
    shown = [s for s in stretches if completeness_within(s["from_at"], s["to_at"], since, until)]
    gaps = [b for b in breaks if completeness_within(b["after_at"], b["before_at"], since, until)]
    listed, records, differences = [], set(), {}
    for stretch in shown:
        inside = [s for s in stretch["segments"] if completeness_within(s["first_at"], s["last_at"], since, until)]
        if inside:
            low, high = min(s["from"] for s in inside), max(s["to"] for s in inside)
            counted = [s for s in inside if s["counted"]]
        else:
            low = high = max([s["to"] for s in stretch["segments"] if since is not None and s["last_at"] < since]
                            or [stretch["pts_from"]])
            counted = []
        for segment in inside:
            records.add(segment["record"])
            if segment["method"] != "push" and segment["differences"]:
                differences.setdefault(segment["method"], {"count": 0, "records": set()})
                differences[segment["method"]]["count"] += segment["differences"]
                differences[segment["method"]]["records"].add(segment["record"])
        listed.append({"pts_from": low, "pts_to": high, "pts_advance": high - low,
                       "updates": sum(s["updates"] for s in counted),
                       "pushed": sum(s["updates"] for s in counted if s["method"] == "push"),
                       "recovered": sum(s["updates"] for s in counted if s["method"] != "push"),
                       "from_at": completeness_stamp(stretch["from_at"]), "to_at": completeness_stamp(stretch["to_at"]),
                       "whole_stretch": {"pts_from": stretch["pts_from"], "pts_to": stretch["pts_to"]},
                       "empty_differences": sum(s["empty"] for s in inside),
                       "overlapping_segments": stretch["overlapping"],
                       "partly_overlapping_segments": stretch["partly_overlapping"]})
    records.discard(None)
    if not listed and not gaps:
        status = "not_recorded"
    elif gaps:
        status = "breaks"
    elif len(listed) == 1 and (since is None or shown[0]["from_at"] <= since) and (until is None or shown[0]["to_at"] >= until):
        status = "unbroken"
    else:
        status = "partial"
    ordered = sorted(records)
    result.update({
        "status": status, "stretches": listed,
        "pts_from": listed[0]["pts_from"] if listed else None, "pts_to": listed[-1]["pts_to"] if listed else None,
        "from_at": listed[0]["from_at"] if listed else None, "to_at": listed[-1]["to_at"] if listed else None,
        "updates": sum(s["updates"] for s in listed),
        "breaks": [{**b, "after_at": completeness_stamp(b["after_at"]), "before_at": completeness_stamp(b["before_at"])}
                   for b in gaps],
        "differences": {method: {"count": item["count"], "records": sorted(item["records"])[:COMPLETENESS_LISTED],
                                 "records_total": len(item["records"])} for method, item in differences.items()},
        "records": {"first": ordered[0], "last": ordered[-1], "count": len(ordered)} if ordered else None})
    return result


def completeness_certificate(events, since=None, until=None, chats=None, account=True):
    found, closures = completeness_collect(events)
    start, end = completeness_time(since), completeness_time(until)
    if chats is None:
        keys = [key for key in found if key != "account"]
    else:
        keys = [chat for chat in chats if completeness_key("channel", chat) is not None]
        account = account and any(completeness_key("channel", chat) is None for chat in chats)
    keys = (["account"] if account else []) + sorted(dict.fromkeys(keys), reverse=True)
    return {"format": COMPLETENESS_FORMAT, "since": since, "until": until, "proves": COMPLETENESS_PROVES,
            "does_not_prove": COMPLETENESS_LIMITS, "channels": COMPLETENESS_CHANNELS,
            "sequences": [completeness_view(key, found.get(key), closures, start, end) for key in keys]}


def completeness_when(value):
    return value[:16].replace("T", " ") + " UTC" if isinstance(value, str) else "?"


def completeness_lines(certificate, t, titles=None):
    lines = []
    for item in certificate["sequences"]:
        if item["scope"] == "account":
            name = t("Account sequence (private chats and basic groups)")
        else:
            name = t("Channel {name}", name=(titles or {}).get(item["chat_id"]) or str(item["chat_id"]))
        if item["status"] == "not_recorded":
            lines.append(t("{name}: no update sequence records in this interval; continuity is not claimed.", name=name)
                         + (" " + t("Not recorded before {at}.", at=completeness_when(item["not_recorded_before"]))
                            if item["not_recorded_before"] else ""))
            continue
        text = t("{name}, {start} – {end}: pts {first} → {last}, breaks {breaks}", name=name,
                 start=completeness_when(certificate.get("since") or item["from_at"]),
                 end=completeness_when(certificate.get("until") or item["to_at"]),
                 first=item["pts_from"] if item["pts_from"] is not None else "?",
                 last=item["pts_to"] if item["pts_to"] is not None else "?", breaks=len(item["breaks"]))
        for method, recovered in item["differences"].items():
            text += ", " + t("recovered through {method}: {count} (records {records})", method=method,
                             count=recovered["count"], records=", ".join("#" + str(r) for r in recovered["records"]))
        text += ". " + {"unbroken": t("Unbroken."), "partial": t("Recorded for part of the interval only."),
                        "breaks": t("Not unbroken.")}[item["status"]]
        if item["not_recorded_before"]:
            text += " " + t("Not recorded before {at}.", at=completeness_when(item["not_recorded_before"]))
        lines.append(text)
        for gap in item["breaks"]:
            closed = gap.get("closed_by")
            lines.append("  " + t("Break: pts {low} → {high}, {after} – {before}: {reason}", low=gap["pts_from"],
                                  high=gap["pts_to"], after=completeness_when(gap["after_at"]),
                                  before=completeness_when(gap["before_at"]),
                                  reason="; ".join(t(COMPLETENESS_REASONS.get(r, r)) for r in gap["reasons"]))
                         + (" (" + ", ".join("#" + str(r) for r in gap["records"]) + ")" if gap["records"] else "")
                         + ". " + (t("Whole again from pts {pts} (record #{record}).", pts=closed["whole_from_pts"],
                                     record=closed["record"]) if closed else t("No closing record.")))
    return lines
