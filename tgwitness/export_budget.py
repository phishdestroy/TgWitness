import math

MIB = 1024**2
DOWNLOAD_BYTES_PER_SECOND = MIB
PACKAGING_BYTES_PER_SECOND = 16 * MIB
SAFETY_FACTOR = 2


def sealing_reserve(session_seconds, output_bytes=0, messages=0):
    baseline = min(300, max(15, math.ceil(session_seconds * .05)))
    return baseline + math.ceil(3 * max(0, output_bytes) / PACKAGING_BYTES_PER_SECOND + max(0, messages) / 5000)


def history_sample(rows, elapsed):
    total = getattr(rows, "total", None)
    if type(total) is not int or total < len(rows):
        total = len(rows) if len(rows) < 25 else None
    return {"history_messages": total, "sample_messages": len(rows),
            "request_seconds": max(.001, elapsed), "download_bytes": 0,
            "hash_ranges": 0, "unknown_size_files": 0, "text_bytes": 0}


def estimate(sample, options=None):
    chats = sample.get("chats", [])
    options = options or {}
    complete = (sample.get("performed") and sample.get("dialog_inventory_complete", True)
                and len(chats) == sample.get("visible_selected_chats", 1)
                and sample.get("selected_inventory_complete", True))
    unknown = []
    if not complete:
        unknown.append("unsampled_chats")
    messages = download = hashes = text_bytes = seconds = history_seconds = 0
    per_chat = []
    for chat in chats:
        total, count = chat["history_messages"], chat["sample_messages"]
        if total is None or (total and not count):
            unknown.append("history_count")
            per_chat.append({"chat_id": chat.get("chat_id"), "kind": chat.get("kind"), "unknown": True})
            continue
        if chat["unknown_size_files"]:
            unknown.append("file_size")
        scale = total / count if count else 0
        if scale > 1 and any(options.get(key) for key in
                             ("from_utc", "to_utc", "sender_ids", "text_contains", "own_messages_only")):
            unknown.append("filtered_media_distribution")
        media = math.ceil(chat["download_bytes"] * scale)
        ranges = math.ceil(chat["hash_ranges"] * scale)
        metadata = math.ceil(chat["text_bytes"] * scale) + total * 2048
        rate = min(100, max(1, count) / max(.05, chat["request_seconds"]))
        chat_seconds = total / rate + media / DOWNLOAD_BYTES_PER_SECOND + ranges / 10
        seconds += chat_seconds
        history_seconds += total / rate
        per_chat.append({"chat_id": chat.get("chat_id"), "kind": chat.get("kind"), "unknown": False,
                         "unknown_size_files": chat["unknown_size_files"],
                         "messages": total, "download_bytes": media,
                         "output_bytes": media + math.ceil(chat["text_bytes"] * scale) + total * 2048 + ranges * 160,
                         "seconds": math.ceil(SAFETY_FACTOR * chat_seconds)})
        messages += total
        download += media
        hashes += ranges
        text_bytes += metadata
    if any(options.get(key) for key in ("include_profile_photos", "include_stories", "include_other_data", "include_avatars")):
        unknown.append("additional_files")
    if options.get("transport") == "takeout" and not options.get("chat_ids"):
        unknown.append("takeout_inventory")
    metadata_seconds = 60 if any(options.get(key) for key in ("include_profile", "include_contacts", "include_session_metadata")) else 0
    return {"complete_inventory": bool(complete), "unknown": sorted(set(unknown)),
            "messages_to_read": messages, "download_bytes": download,
            "output_bytes": download + text_bytes + hashes * 160,
            "acquisition_seconds": math.ceil(SAFETY_FACTOR * seconds + metadata_seconds),
            "history_seconds": math.ceil(history_seconds), "metadata_seconds": metadata_seconds,
            "hash_seconds": math.ceil(hashes / 10),
            "per_chat": sorted(per_chat, key=lambda c: -(c.get("seconds") or 0)),
            "assumptions": {"download_bytes_per_second": DOWNLOAD_BYTES_PER_SECOND,
                            "packaging_bytes_per_second": PACKAGING_BYTES_PER_SECOND,
                            "safety_factor": SAFETY_FACTOR, "history_counts": "entire accessible history",
                            "media_distribution": "recent sample extrapolated within each chat",
                            "rates": "history request timing measured; download and packaging rates assumed"}}


SESSION_CHOICES = (30, 60, 120)


def recommended_minutes(value, spent_seconds):
    """Shortest offered session that fits the whole estimate, counting time already spent signing in.

    None when nothing is offered that fits, or when the estimate is incomplete."""
    if value["unknown"]:
        return None
    for minutes in SESSION_CHOICES:
        session = minutes * 60
        reserve = sealing_reserve(session, value["output_bytes"], value["messages_to_read"])
        if spent_seconds + value["acquisition_seconds"] + reserve <= session:
            return minutes
    return None


def fitting_chats(per_chat, available_seconds, metadata=0):
    """Measured chats that fit together in the remaining collection time, smallest first to keep the most chats."""
    budget, chosen = available_seconds - metadata, []
    for chat in sorted((c for c in per_chat if not c.get("unknown") and c.get("chat_id") is not None),
                       key=lambda c: c["seconds"]):
        if chat["seconds"] <= budget:
            chosen.append(chat["chat_id"])
            budget -= chat["seconds"]
    return chosen


def split_runs(per_chat, spent_seconds, metadata=0, minutes=SESSION_CHOICES[-1]):
    """Group measured chats into separate longest-session runs (first fit, largest first).

    Each run must still sign in, so the time spent signing in this run is reserved in every run. A chat too large
    for one run gets its own run marked "exceeds_one_run"; restrict its dates to fit."""
    session = minutes * 60
    runs = []
    for chat in sorted((c for c in per_chat if not c.get("unknown") and c.get("chat_id") is not None),
                       key=lambda c: -c["seconds"]):
        for run in runs:
            reserve = sealing_reserve(session, run["output_bytes"] + chat["output_bytes"], run["messages"] + chat["messages"])
            if spent_seconds + metadata + run["seconds"] + chat["seconds"] + reserve <= session:
                run["chat_ids"].append(chat["chat_id"])
                run["seconds"] += chat["seconds"]
                run["output_bytes"] += chat["output_bytes"]
                run["messages"] += chat["messages"]
                break
        else:
            reserve = sealing_reserve(session, chat["output_bytes"], chat["messages"])
            runs.append({"session_minutes": minutes, "chat_ids": [chat["chat_id"]], "seconds": chat["seconds"],
                         "output_bytes": chat["output_bytes"], "messages": chat["messages"],
                         "exceeds_one_run": spent_seconds + metadata + chat["seconds"] + reserve > session})
    unmeasured = [c["chat_id"] for c in per_chat if c.get("unknown") and c.get("chat_id") is not None]
    if unmeasured:
        runs.append({"session_minutes": minutes, "chat_ids": unmeasured, "seconds": None, "output_bytes": None,
                     "messages": None, "exceeds_one_run": None, "unmeasured": True})
    return runs


def plan(sample, options, remaining_seconds, session_seconds):
    value = estimate(sample, options)
    reserve = sealing_reserve(session_seconds, value["output_bytes"], value["messages_to_read"])
    available = max(0, remaining_seconds - reserve)
    required = value["acquisition_seconds"]
    fit = "over_budget" if required > available else "unknown" if value["unknown"] else "estimated_fit"
    if remaining_seconds <= reserve:
        fit = "no_collection_time"
    media_budget = options.get("max_total_gib")
    files_exceed_budget = media_budget is not None and value["download_bytes"] > media_budget * 1024**3
    suggestions = []
    if value["download_bytes"]:
        suggestions.append("messages_only")
    if fit in ("over_budget", "unknown", "no_collection_time"):
        suggestions.append("fewer_chats")
    spent = max(0, session_seconds - remaining_seconds)
    return {**value, "fit": fit, "remaining_seconds": remaining_seconds,
            "collection_seconds": available, "sealing_reserve_seconds": reserve,
            "estimated_total_seconds": required + reserve,
            "recommended_session_minutes": recommended_minutes(value, spent),
            "fits_now": fitting_chats(value["per_chat"], available, metadata=value["metadata_seconds"]),
            "split_runs": split_runs(value["per_chat"], spent, value["metadata_seconds"]) if required > available else [],
            "approval": "not_requested" if options.get("transport") == "takeout" else "not_required",
            "files_exceed_budget": files_exceed_budget, "suggestions": suggestions,
            "maximum_download_bytes_at_assumed_rate": max(0, int((available / SAFETY_FACTOR) * DOWNLOAD_BYTES_PER_SECOND))}


def progress(assessment, job, remaining_seconds, session_seconds, elapsed_seconds, wait_seconds=0):
    counts, acquired = job.get("counts", {}), job.get("acquisition", {})
    messages = acquired.get("messages_preserved", counts.get("messages_seen", 0))
    downloaded = counts.get("unique_media_bytes", 0)
    preserved_bytes = acquired.get("bytes_preserved", 0) + downloaded
    reserve = sealing_reserve(session_seconds, preserved_bytes, messages)
    available = max(0, remaining_seconds - reserve)
    value = {"remaining_seconds": remaining_seconds, "collection_seconds": available,
             "sealing_reserve_seconds": reserve, "wait_seconds": max(0, wait_seconds),
             "estimated_remaining_seconds": None, "fit": "unknown"}
    if assessment:
        left_messages = max(0, assessment["messages_to_read"] - messages)
        left_bytes = max(0, assessment["download_bytes"] - downloaded)
        history_rate = messages / elapsed_seconds if messages and elapsed_seconds >= 5 else None
        download_rate = downloaded / elapsed_seconds if downloaded and elapsed_seconds >= 5 else DOWNLOAD_BYTES_PER_SECOND
        history_seconds = left_messages / history_rate if history_rate else assessment["history_seconds"]
        if acquired.get("history_complete"):
            history_seconds = 0
        required = math.ceil(SAFETY_FACTOR * (history_seconds + left_bytes / download_rate + assessment["hash_seconds"])
                             + assessment["metadata_seconds"])
        value.update(estimated_remaining_seconds=required + reserve + wait_seconds,
                     fit="over_budget" if required + wait_seconds > available else
                     "unknown" if assessment["unknown"] else "estimated_fit",
                     measured_history_messages_per_second=history_rate,
                     measured_download_bytes_per_second=downloaded / elapsed_seconds if downloaded and elapsed_seconds >= 5 else None)
    if wait_seconds >= available and wait_seconds:
        value["fit"] = "wait_exceeds_window"
    if available <= 0:
        value["fit"] = "no_collection_time"
    return value
