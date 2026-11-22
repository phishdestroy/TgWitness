from .export_budget import DOWNLOAD_BYTES_PER_SECOND

FINISHED_MEDIA = ("done", "hashed", "skipped", "failed", "cancelled")
OPEN_MEDIA = ("queued", "retry", "running")


def share(done, total):
    return None if not total else max(0.0, min(1.0, (done or 0) / total))


def percent(value, running=True):
    if value is None:
        return None
    return min(99 if running else 100, int(value * 100))


def blended(parts):
    known = [(value, weight) for value, weight in parts if value is not None and weight]
    if not known:
        return None
    return sum(value * weight for value, weight in known) / sum(weight for _, weight in known)


def plan_totals(plan):
    if not plan:
        return None, None
    estimated = "history_count" not in (plan.get("unknown") or [])
    return (plan.get("messages_to_read") if estimated else None), plan.get("download_bytes")


def account(job, plan, elapsed, eta):
    counts, coverage = job.get("counts") or {}, job.get("coverage") or {}
    phase, found = job.get("phase"), job.get("discovery") or {}
    messages = max(counts.get("messages_exported") or 0, (job.get("acquisition") or {}).get("messages_preserved") or 0)
    messages_total, bytes_total = plan_totals(plan)
    tasks = share(coverage.get("tasks_done"), coverage.get("tasks_total"))
    overall = max([value for value in (tasks, share(messages, messages_total)) if value is not None], default=None)
    stage = {"preparing": "inventory", "waiting": "waiting", "packaging": "packaging"}.get(phase, "messages")
    detail = None
    if phase == "preparing":
        stage = {"checking": "checking", "left_chats": "inventory_left"}.get(found.get("stage"), "inventory")
        detail = {"done": found.get("done") or 0, "total": found.get("total")}
        overall = None
    current = job.get("current_chat")
    if stage == "messages" and (job.get("acquisition") or {}).get("history_complete"):
        stage = "files"
    if isinstance(current, dict) and current.get("task") == "avatars":
        stage, current = "photos", None
    files = (counts.get("media_saved") or 0) + (counts.get("media_hashed") or 0)
    return {"stage": stage, "percent": percent(overall, phase not in ("done",)), "detail": detail,
            "messages": {"done": messages, "total": messages_total},
            "files": {"done": files, "skipped": counts.get("media_skipped") or 0, "total": None,
                      "bytes": counts.get("unique_media_bytes", counts.get("bytes_saved")) or 0, "bytes_total": bytes_total},
            "chats": {"done": counts.get("chats_done") or 0, "read": counts.get("chats_read"), "total": counts.get("chats_selected"),
                      "found": counts.get("chats_discovered")},
            "tasks": {"done": coverage.get("tasks_done") or 0, "total": coverage.get("tasks_total")},
            "problems": coverage.get("failures") or 0,
            "current": (current.get("title") or str(current.get("id"))) if isinstance(current, dict) else
            (str(current) if current is not None else None),
            "transfer": job.get("transfer") if job.get("active") else None,
            "wait_until": job.get("wait_until"), "elapsed_seconds": int(elapsed), "eta_seconds": eta}


def chat(history, media, media_bytes, plan, elapsed, eta, title=None):
    messages_total, bytes_total = plan_totals(plan)
    complete = history.get("phase") in ("complete", "incomplete")
    files_total = sum(media.get(key, 0) for key in FINISHED_MEDIA + OPEN_MEDIA)
    files_done = sum(media.get(key, 0) for key in FINISHED_MEDIA)
    open_files = sum(media.get(key, 0) for key in OPEN_MEDIA)
    message_share = 1.0 if complete else share(history.get("captured"), messages_total)
    file_share = share(media_bytes, bytes_total) if bytes_total else share(files_done, files_total)
    if complete and not open_files:
        file_share = 1.0
    overall = blended([(message_share, (plan or {}).get("history_seconds") or 1),
                       (file_share, (bytes_total or 0) / DOWNLOAD_BYTES_PER_SECOND if files_total else 0)])
    stage = "waiting" if history.get("phase") == "paused" else "files" if complete and open_files else "messages"
    return {"stage": stage, "percent": percent(overall), "detail": None,
            "messages": {"done": history.get("captured") or 0, "total": messages_total},
            "files": {"done": media.get("done", 0) + media.get("hashed", 0), "skipped": media.get("skipped", 0),
                      "finished": files_done, "total": files_total, "bytes": media_bytes, "bytes_total": bytes_total,
                      "queued": open_files},
            "chats": None, "tasks": None, "problems": (history.get("unavailable") or 0) + media.get("failed", 0),
            "current": title, "transfer": None, "wait_until": history.get("wait_until") or None,
            "elapsed_seconds": int(elapsed), "eta_seconds": eta}


def chats(progress, plan, elapsed, eta, title_of):
    kept, current = progress.get("kept") or [], progress.get("current") or {}
    total = progress.get("total") or 0
    reading = progress.get("current_chat") is not None
    if current.get("stage") == "files":
        current_share = 1.0
    else:
        current_share = max([value for value in (share(current.get("ranges_done"), current.get("ranges_total")),
                                                 share(current.get("captured"), current.get("total"))) if value is not None],
                            default=0.0)
    overall = share(len(kept) + (current_share if reading else 0), total)
    messages = sum(item.get("captured") or 0 for item in kept) + (current.get("captured") or 0 if reading else 0)
    messages_total, bytes_total = plan_totals(plan)
    stage = "files" if reading and current.get("stage") == "files" else "packaging" if current.get("stage") == "packaging" \
        else "messages"
    files = sum(item.get("files") or 0 for item in kept) + (current.get("files_done") or 0 if reading else 0)
    return {"stage": stage, "percent": percent(overall), "detail": None,
            "messages": {"done": messages, "total": messages_total},
            "files": {"done": files, "skipped": 0, "total": None, "bytes": 0, "bytes_total": None},
            "chats": {"done": len(kept), "total": total},
            "chat": {"done": current.get("captured") or 0, "total": current.get("total"),
                     "files_done": current.get("files_done") or 0, "files_total": current.get("files_total"),
                     "stage": current.get("stage")} if reading else None,
            "tasks": None, "problems": sum(1 for item in kept if not item.get("complete")),
            "current": title_of(progress.get("current_chat")) if reading else None, "transfer": None,
            "wait_until": None, "elapsed_seconds": int(elapsed), "eta_seconds": eta}
