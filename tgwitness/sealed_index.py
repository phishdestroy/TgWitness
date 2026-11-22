import base64
import hashlib
import re
from datetime import datetime
from html import escape

SEALED_KINDS = ("sealed.started", "sealed.selection", "sealed.account_export", "sealed.chat_export", "sealed.finished", "sealed.failure",
                "sealed.packaging", "account_export.transport")
LOG_KINDS = ("collector.started", "account.authorized", "sealed.selection", "account_export.started", "account_export.transport",
             "sealed.chat_export", "account_export.completed", "sealed.packaging", "sealed.failure", "sealed.finished")

REASONS = {
    "account_export_finished": ("complete", "The export finished within the selected scope."),
    "history_and_media_finished": ("complete", "Chat history and attachments finished."),
    "chat_exports_finished": ("complete", "Every selected chat was exported."),
    "user_finish": ("partial", "Stopped early in the capture panel. Data acquired until then is kept."),
    "deadline": ("partial", "The session time ran out. Data acquired until then is kept."),
    "packaging_reserve": ("partial", "Collection stopped to leave time for packaging. Data acquired until then is kept."),
    "storage_limit": ("partial", "Runner storage was nearly full. Data acquired until then is kept."),
    "server_shutdown": ("partial", "The runner stopped the capture."),
}

STYLE = (
    ":root{color-scheme:light dark;--bg:#f6f7f9;--card:#fff;--ink:#14171c;--muted:#5d6672;--line:#e2e5ea;"
    "--ok:#127a3e;--warn:#9a5b00;--bad:#b3261e;--accent:#2457c5}"
    "@media(prefers-color-scheme:dark){:root{--bg:#0f1115;--card:#171a20;--ink:#e8eaee;--muted:#9aa3ae;"
    "--line:#2a2f37;--ok:#4cc47f;--warn:#e0a640;--bad:#ff6b60;--accent:#7aa2ff}}"
    "*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);"
    "font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}"
    "main{max-width:980px;margin:0 auto;padding:28px 18px 48px}"
    "header{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;margin-bottom:18px}"
    "h1{font-size:22px;margin:0}h2{font-size:15px;margin:0 0 10px;text-transform:uppercase;letter-spacing:.04em;"
    "color:var(--muted)}.badge{font-weight:700;padding:6px 12px;border-radius:999px;border:2px solid currentColor}"
    ".complete{color:var(--ok)}.partial{color:var(--warn)}.failed,.cancelled{color:var(--bad)}"
    ".grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}"
    ".card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px}"
    ".wide{grid-column:1/-1}.lead{font-size:16px;margin:0 0 6px}.muted{color:var(--muted)}"
    "table{width:100%;border-collapse:collapse}td{padding:5px 0;border-bottom:1px solid var(--line);vertical-align:top}"
    "td:first-child{color:var(--muted);width:42%;padding-inline-end:10px}tr:last-child td{border-bottom:0}"
    "code{font:12.5px/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;word-break:break-all}"
    ".stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px}"
    ".stat{border:1px solid var(--line);border-radius:10px;padding:10px 12px}.stat b{display:block;font-size:20px}"
    ".stat span{color:var(--muted);font-size:12.5px}.alert{border-inline-start:4px solid var(--bad);padding:10px 14px;"
    "background:var(--card);border-radius:8px;margin:0 0 14px}.alert.warn{border-color:var(--warn)}"
    "pre{white-space:pre-wrap;margin:6px 0 0;padding:10px;border-radius:8px;background:var(--bg);"
    "border:1px solid var(--line);direction:ltr;text-align:left}ol{margin:0;padding-inline-start:20px}"
    "ul.limits{margin:0;padding-inline-start:18px}li{margin:4px 0}a{color:var(--accent)}"
    ".list td:first-child{width:auto;color:var(--ink)}.list tr.head td{color:var(--muted);font-weight:600;font-size:13px}"
    ".list td{padding-inline-end:14px}"
    ".log td{padding-inline-end:14px}.log td:first-child,.log td.elapsed{width:1%;white-space:nowrap;"
    "font-variant-numeric:tabular-nums}.log td.elapsed{color:var(--muted)}.waits{margin:12px 0 0}"
)
STYLE_HASH = "sha256-" + base64.b64encode(hashlib.sha256(STYLE.encode()).digest()).decode()


def collect(facts, event):
    kind, payload = event["kind"], event["payload"]
    if kind in SEALED_KINDS:
        facts.setdefault(kind, []).append(payload)
    if kind in LOG_KINDS:
        facts.setdefault("log", []).append((event.get("observed_at"), kind, payload))
    elif kind == "telegram.backoff":
        wait = payload.get("retry_after_seconds")
        if type(wait) is int and wait >= 0:
            method = str(payload.get("method") or payload.get("failed_method") or "?")
            entry = facts.setdefault("waits", {}).setdefault(method, [0, 0, 0])
            entry[0], entry[1], entry[2] = entry[0] + 1, entry[1] + wait, max(entry[2], wait)
    elif kind in ("account_export.history_page", "account_export.page"):
        name = "reading" if kind == "account_export.history_page" else "signing"
        span = facts.setdefault(name, [event.get("observed_at"), None, 0, 0])
        span[1], span[2] = event.get("observed_at"), span[2] + 1
        if name == "reading" and type(payload.get("messages_preserved")) is int:
            span[3] = max(span[3], payload["messages_preserved"])
        elif name == "signing" and type(payload.get("count")) is int:
            span[3] += payload["count"]


def _e(value):
    return escape(str(value), quote=True)


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return _e(value)
    return f"{value:,}".replace(",", " ")


def _size(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return _e(value)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            return (f"{value:.0f} {unit}" if unit == "B" else f"{value:.1f} {unit}")
        value /= 1024


def _duration(say, seconds):
    seconds = max(0, int(round(seconds)))
    hours, rest = divmod(seconds, 3600)
    minutes, seconds = divmod(rest, 60)
    if hours:
        return say("{h} h {m} min", h=hours, m=minutes)
    if minutes:
        return say("{m} min {s} s", m=minutes, s=seconds)
    return say("{s} s", s=seconds)


def _counted(say, text, n, **values):
    found = say(text, n=n, **values)
    return found.replace(str(n), _number(n), 1) if type(n) is int and abs(n) >= 1000 else found


def _rows(say, pairs):
    return "<table>" + "".join(f"<tr><td>{_e(say(k))}</td><td>{v}</td></tr>" for k, v in pairs if v not in (None, "")) + "</table>"


CATEGORY_NAMES = {"personal": "private chats", "bots": "bots", "private_groups": "private groups",
                  "public_groups": "public groups", "private_channels": "private channels",
                  "public_channels": "public channels"}
MODE_NAMES = {"account": "Account export", "chat": "Chat event journal", "chats": "Chat investigation export",
              "secret": "Pseudo-secret chat capture"}
METHOD_NAMES = {"auto": "Automatic", "regular": "Regular Telegram API", "takeout": "Telegram Takeout",
                "chat export": "Chat export", "chat event journal": "Chat event journal"}
LOGOUT_STATES = {"revoked": "Ended by this run", "not_confirmed": "Not confirmed", "no_session": "No session was open"}
LANGUAGE_NAMES = {"en": "English", "uk": "Українська", "es": "Español", "pt": "Português (Brasil)", "tr": "Türkçe",
                  "ar": "العربية", "fa": "فارسی", "ur": "اردو", "hi": "हिन्दी", "id": "Bahasa Indonesia", "vi": "Tiếng Việt",
                  "zh": "简体中文", "fr": "Français", "de": "Deutsch", "it": "Italiano", "uz": "O‘zbekcha", "ko": "한국어",
                  "zh-Hant": "繁體中文", "ms": "Bahasa Melayu", "pl": "Polski", "ja": "日本語", "th": "ไทย", "he": "עברית",
                  "bn": "বাংলা", "ru": "Русский"}
STAT_CAPTIONS = ("Messages saved", "Files saved", "File bytes saved", "Files with hashes only", "Files not saved",
                 "Files not reached before the stop")
PACKAGING_REASONS = {"disk_full": "the runner disk was full", "archive_size_limit": "the archive reached its size limit"}
STATE_LABELS = {"complete": "Complete within the selected scope", "partial": "Partial"}


def limits_of(facts):
    exported = (facts.get("sealed.account_export") or [{}])[-1]
    found = exported.get("limits")
    if found is None:
        found = (((facts.get("sealed.finished") or [{}])[-1]).get("account_export") or {}).get("omissions") or []
    return [item for item in found if isinstance(item, str)]


def not_reached_of(exported):
    counts = exported.get("counts") or {}
    return tuple(counts.get(key) if type(counts.get(key)) is int else 0 for key in ("media_not_reached", "steps_not_reached"))


def failures_of(exported, limits):
    failures = (exported.get("coverage") or {}).get("failures")
    return max(0, failures - len(limits) - sum(not_reached_of(exported))) if type(failures) is int else None


def finished_with_limits(facts):
    exported = (facts.get("sealed.account_export") or [{}])[-1]
    coverage, limits = exported.get("coverage") or {}, limits_of(facts)
    return bool(exported.get("complete_within_scope") is False and limits and failures_of(exported, limits) == 0
                and not coverage.get("omitted") and coverage.get("inventory_complete") is True
                and coverage.get("tasks_total") and coverage.get("tasks_done") == coverage.get("tasks_total"))


def finish_text(say, reason):
    return say(REASONS[reason][1]) if reason in REASONS else say("Capture ended: {reason}", reason=reason)


def outcome(facts, say):
    finished = (facts.get("sealed.finished") or [{}])[-1]
    if facts.get("sealed.failure"):
        return "partial", say("Salvaged after a failure"), say("Collection failed. The signed journal up to the failure is kept.")
    exported = (facts.get("sealed.account_export") or [{}])[-1]
    state = REASONS.get(finished.get("reason"), ("partial",))[0]
    text = finish_text(say, finished.get("reason"))
    if exported and finished.get("reason") == "account_export_finished" and finished_with_limits(facts):
        done = (exported.get("counts") or {}).get("chats_done")
        return "partial", say("Finished with known limits"), (
            _counted(say, "All {n} selected chats were read to the end, with no failures.", done) if type(done) is int else
            say("Every export step finished, with no failures."))
    if exported and exported.get("complete_within_scope") is False:
        state = "partial"
    chats = facts.get("sealed.chat_export") or []
    if any(not item.get("complete") for item in chats):
        state = "partial"
        text = say("{done} of {total} selected chats were exported completely.",
                   done=sum(1 for c in chats if c.get("complete")), total=len(chats))
    return state, say(STATE_LABELS[state]), text


def _clock(at):
    return at[11:19] if isinstance(at, str) and len(at) >= 19 else "—"


def _seconds(at):
    try:
        return datetime.fromisoformat(at).timestamp()
    except (TypeError, ValueError):
        return None


def run_log(facts, say):
    rows = []
    started = (facts.get("sealed.started") or [{}])[0]
    for at, kind, payload in facts.get("log") or ():
        if kind == "collector.started":
            limit = started.get("deadline_seconds")
            rows.append((at, say("Capture started on GitHub Actions") + (
                " · " + say("session time limit {time}", time=_duration(say, limit)) if type(limit) is int else "")))
        elif kind == "account.authorized":
            rows.append((at, say("Signed in to Telegram with a new session created by this run")
                         if payload.get("key_origin") == "created" else say("Signed in to Telegram")))
        elif kind == "sealed.selection":
            rows.append((at, say("Selection fixed and signed") + " · " + say(MODE_NAMES.get(payload.get("mode") or "chat", "Capture"))))
        elif kind == "account_export.started":
            rows.append((at, say("Account export started")))
        elif kind == "account_export.transport":
            rows.append((at, say("Reading method: {method}", method=say(METHOD_NAMES.get(payload.get("transport"), str(payload.get("transport")))))))
        elif kind == "sealed.chat_export":
            title = payload.get("title") or say("ID {id}", id=payload.get("chat_id"))
            state = (say("complete") if payload.get("complete") else say("partial snapshot") if payload.get("phase") == "snapshot"
                     else say("failed"))
            captured = payload.get("captured") if type(payload.get("captured")) is int else 0
            rows.append((at, say("Chat exported: {title}", title=title) + " · " + state + " · "
                         + _counted(say, "{n} messages", captured)))
        elif kind == "account_export.completed":
            rows.append((at, say("Account export finished")))
        elif kind == "sealed.packaging":
            reason = payload.get("reason")
            rows.append((at, say("Compact packaging: {reason}", reason=say(PACKAGING_REASONS.get(reason, str(reason))))))
        elif kind == "sealed.failure":
            rows.append((at, say("Failure recorded: {error}", error=payload.get("error"))))
        elif kind == "sealed.finished":
            rows.append((at, say("Capture finished") + " · " + finish_text(say, payload.get("reason"))))
            if payload.get("revocation") in LOGOUT_STATES:
                rows.append((at, say("Telegram session") + ": " + say(LOGOUT_STATES[payload["revocation"]])))
    reading, signing = facts.get("reading"), facts.get("signing")
    if reading:
        rows.append((reading[0], say("Reading message history started")))
        rows.append((reading[1], _counted(say, "Message history read: {n} messages in {pages} pages", reading[3],
                                          pages=_number(reading[2]))))
    if signing:
        rows.append((signing[0], say("Signing pages and downloading files started")))
        rows.append((signing[1], _counted(say, "Pages signed: {pages}, with {n} records", signing[3], pages=_number(signing[2]))))
    if not rows:
        return ""
    rows.sort(key=lambda row: row[0] or "")
    origin = _seconds(rows[0][0])
    day = rows[0][0][:10] if isinstance(rows[0][0], str) else ""
    table = []
    for at, text in rows:
        moment = _seconds(at)
        elapsed = "+" + _duration(say, moment - origin) if moment is not None and origin is not None else ""
        table.append(f'<tr><td><time datetime="{_e(at)}">{_e(_clock(at))}</time></td><td class="elapsed">{_e(elapsed)}</td>'
                     f"<td>{_e(text)}</td></tr>")
    waits = facts.get("waits") or {}
    if waits:
        count, total = sum(item[0] for item in waits.values()), sum(item[1] for item in waits.values())
        longest = max(item[2] for item in waits.values())
        summary = _counted(say, "FLOOD_WAIT: {n} times, {total} in total, longest {longest}.", count,
                           total=_duration(say, total), longest=_duration(say, longest))
        detail = "".join(f"<li><code>{_e(method)}</code> · {_e(_counted(say, '{n} times', item[0]))} · "
                         f"{_e(say('longest {time}', time=_duration(say, item[2])))}</li>"
                         for method, item in sorted(waits.items(), key=lambda pair: -pair[1][0]))
        waits_html = f'<div class="waits"><p>{_e(summary)}</p><ul class="limits">{detail}</ul></div>'
    else:
        waits_html = f'<p class="waits">{_e(say("FLOOD_WAIT: none."))}</p>'
    return (f'<section class="card wide"><h2>{_e(say("Run log"))}</h2><p class="muted">'
            + _e(say("UTC, {day}, collector clock.", day=day))
            + f'</p><table class="log">{"".join(table)}</table>{waits_html}</section>')


def page(facts, events, fingerprint=None, head_hash=None, language="en"):
    from .report import Words
    say = Words(language)

    def marked(text, **parts):
        found = _e(say(text, **{name: "\x00" + name + "\x00" for name in parts}))
        for name, piece in parts.items():
            found = found.replace("\x00" + name + "\x00", piece)
        return found

    started = (facts.get("sealed.started") or [{}])[0]
    context = started.get("context") or {}
    selection_event = (facts.get("sealed.selection") or [{}])[-1]
    selection = selection_event.get("selection") or {}
    exported = (facts.get("sealed.account_export") or [{}])[-1]
    finished = (facts.get("sealed.finished") or [{}])[-1]
    transports = facts.get("account_export.transport") or []
    state, label, explanation = outcome(facts, say)

    repo, run, attempt = context.get("repository"), context.get("run_id"), context.get("run_attempt")
    commit = context.get("collector_sha")
    safe_repo = repo if isinstance(repo, str) and re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) else None
    run_text = say("{run} · attempt {attempt}", run=run, attempt=attempt)
    run_link = (f'<a href="https://github.com/{_e(safe_repo)}/actions/runs/{_e(run)}/attempts/{_e(attempt)}">'
                f"{_e(run_text)}</a>") if safe_repo and str(run).isdigit() and str(attempt).isdigit() else _e(run)
    commit_link = (f'<a href="https://github.com/phishdestroy/TgWitness/commit/{_e(commit)}"><code>{_e(commit)}</code></a>'
                   if isinstance(commit, str) and re.fullmatch(r"[0-9a-f]{40}", commit) else _e(commit))

    alerts = []
    for failure in facts.get("sealed.failure") or []:
        alerts.append(f'<div class="alert"><b>{_e(say("Failure recorded:"))}</b> {_e(failure.get("error"))}. '
                      f'{_e(say(failure.get("meaning", "")) if failure.get("meaning") else "")}</div>')
    if finished.get("revocation") == "not_confirmed":
        alerts.append(f'<div class="alert warn"><b>{_e(say("Session logout was not confirmed."))}</b> '
                      f'{_e(say("Open Telegram → Settings → Devices and end the session created by this capture."))}</div>')
    for packaging in facts.get("sealed.packaging") or []:
        reason = packaging.get("reason")
        alerts.append(f'<div class="alert warn"><b>{_e(say("Compact packaging:"))}</b> '
                      f'{_e(say(PACKAGING_REASONS.get(reason, str(reason))))}. '
                      f'{_e(say("All signed records are kept; formatted duplicates were omitted."))}</div>')

    mode = selection.get("mode")
    options = selection.get("account_options") or {}
    requested = (options.get("transport") if mode == "account" else "chat export" if mode == "chats"
                 else "chat event journal")
    used = transports[-1].get("transport") if transports else (requested if requested != "auto" else None)
    used_reason = transports[-1].get("meaning") if transports else None
    method = lambda value: say(METHOD_NAMES.get(value, str(value)))  # noqa: E731
    counts = dict(exported.get("counts") or {})
    if mode == "account":
        categories = options.get("chat_categories")
        scope = (say("{n} chosen chats", n=len(options.get("chat_ids") or [])) if options.get("chat_ids") else
                 ", ".join(say(CATEGORY_NAMES.get(c, str(c))) for c in categories) if categories is not None
                 and len(categories) < len(CATEGORY_NAMES) else say("all chats of the account"))
        if type(counts.get("chats_selected")) is int and type(counts.get("chats_discovered")) is int:
            scope += " · " + say("{selected} of {listed} chats in the list", selected=_number(counts["chats_selected"]),
                                 listed=_number(counts["chats_discovered"]))
    elif mode == "chats":
        scope = say("{n} selected chats", n=len(selection.get("chat_ids") or []))
    else:
        scope = say("one chat (ID {id})", id=selection.get("chat_id"))
    selection_rows = [("Mode", _e(say(MODE_NAMES.get(mode or "chat", str(mode))))),
                      ("Scope", _e(scope)),
                      ("Method requested", _e(method(requested))),
                      ("Method used", _e(method(used)) if used else _e(say("recorded in the journal"))),
                      ("Why", _e(say(used_reason)) if used_reason and not limits_of(facts) else None),
                      ("Date range (UTC)", _e(" → ".join(str(x or "…") for x in (options.get("from_utc"), options.get("to_utc"))))
                       if options.get("from_utc") or options.get("to_utc") else None),
                      ("Media budget", _e(str(options.get("max_total_gib")) + " GiB") if options.get("max_total_gib") else None),
                      ("Report language", _e(LANGUAGE_NAMES.get(say.language, say.language))),
                      ("Selection SHA-256", "<code>" + _e(selection_event.get("selection_sha256")) + "</code>")]

    if not counts and finished.get("history"):
        history = finished["history"]
        counts = {"messages_seen": history.get("captured"), **{"media_" + k: v for k, v in (finished.get("media") or {}).items()}}
    stats = []

    def stat(value, caption, size=False):
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            stats.append(f'<div class="stat"><b>{_size(value) if size else _number(value)}</b><span>{_e(say(caption))}</span></div>')

    number = lambda *keys: max((counts.get(k) for k in keys if isinstance(counts.get(k), int)), default=None)  # noqa: E731
    stat(number("messages_exported", "messages_preserved", "messages", "messages_seen"), "Messages saved")
    if isinstance(counts.get("chats_selected"), int):
        stats.append(f'<div class="stat"><b>{_number(counts.get("chats_done") or 0)} / {_number(counts["chats_selected"])}'
                     f'</b><span>{_e(say("Chats finished"))}</span></div>')
    stat(number("media_saved", "media_done"), "Files saved")
    if counts.get("unique_media_bytes") or counts.get("bytes_saved"):
        stat(counts.get("unique_media_bytes") or counts.get("bytes_saved"), "File bytes saved", size=True)
    files, steps = not_reached_of(exported)
    for key, caption in (("media_hashed", "Files with hashes only"), ("media_skipped", "Files not saved")):
        value = counts.get(key)
        if key == "media_skipped" and value:
            value -= min(value, files)
            stat(files or None, "Files not reached before the stop")
        if value:
            stat(value, caption)
    coverage = exported.get("coverage") or {}
    coverage_rows = []
    if exported:
        limits = limits_of(facts)
        failures = failures_of(exported, limits)
        coverage_rows = [
            ("Complete within scope", _e(say("yes")) if exported.get("complete_within_scope") else
             _e(say("no · because of the known limits below")) if finished_with_limits(facts) else _e(say("no"))),
            ("Chat list read completely", {True: _e(say("yes")), False: _e(say("no"))}.get(coverage.get("inventory_complete"))),
            ("Export steps finished", _e(say("{done} of {total}", done=_number(coverage.get("tasks_done") or 0),
                                             total=_number(coverage.get("tasks_total") or 0)))
             if coverage.get("tasks_total") else None),
            ("Failed pages and files", (_e(_counted(say, "{n} · listed under Omissions in the export index", failures)) if failures
                                        else _e(say("none"))) if failures is not None else None),
            ("Not reached before the stop", _e(" · ".join(part for part in (
                _counted(say, "{n} files", files) if files else "", _counted(say, "{n} export steps", steps) if steps else "")
                if part)) or None),
            ("Known limits", '<ul class="limits">' + "".join(f"<li>{_e(say(item))}</li>" for item in limits) + "</ul>"
             if limits else None),
            ("Coverage", _e(say(coverage.get("scope"))) if coverage.get("scope") else None)]

    logout = finished.get("revocation")
    identity = [("Repository", _e(repo)), ("Workflow run", run_link), ("Collector commit", commit_link),
                ("GitHub attestation", "<code>attestation.jsonl</code>"),
                ("Recipient key SHA-256", "<code>" + _e(started.get("recipient_sha256")) + "</code>"),
                ("Journal signing key", "<code>" + _e(fingerprint) + "</code>" if fingerprint else None),
                ("Journal records", _number(events)), ("Journal head", "<code>" + _e(head_hash) + "</code>" if head_hash else None),
                ("Fresh session only", _e(say("yes")) if started.get("session_import_allowed") is False else _e(started.get("session_import_allowed"))),
                ("Session logout", _e(say(LOGOUT_STATES[logout])) if logout in LOGOUT_STATES else _e(logout))]

    chats = facts.get("sealed.chat_export") or []
    if chats:
        missing = sum((c.get("message_ids") or {}).get("missing") or 0 for c in chats
                      if (c.get("message_ids") or {}).get("numbered_per_chat"))
        stats = [f'<div class="stat"><b>{_number(sum(c.get("captured") or 0 for c in chats))}</b><span>{_e(say("Messages saved"))}</span></div>',
                 f'<div class="stat"><b>{sum(1 for c in chats if c.get("complete"))} / {len(chats)}</b>'
                 f'<span>{_e(say("Chats complete"))}</span></div>',
                 f'<div class="stat"><b>{_number(missing)}</b><span>'
                 f'{_e(say("Message IDs absent after recheck, channels and supergroups"))}</span></div>']

    def gaps(c):
        ids = c.get("message_ids")
        if not ids:
            return "—"
        if not ids.get("numbered_per_chat"):
            return _e(say("not measured"))
        if not ids.get("missing"):
            return _e(say("none · IDs {first}–{last}", first=ids.get("first_id"), last=ids.get("last_id")))
        largest = ", ".join(f"{_e(low)}–{_e(high)}" for low, high in ids.get("largest_runs") or [])
        return (marked("{n} in {runs} ranges", n="<b>" + _number(ids["missing"]) + "</b>", runs=_number(ids.get("missing_runs") or 0))
                + (f'<br><span class="muted">{_e(say("largest:"))} {largest}</span>' if largest else ""))

    chat_rows = "".join(
        f'<tr><td>{_e(c.get("title") or "—")}<br><span class="muted"><code>{_e(c.get("chat_id"))}</code></span></td><td>'
        + (f'<span class="complete">{_e(say("complete"))}</span>' if c.get("complete") else
           f'<span class="partial">{_e(say("partial snapshot"))}</span>' if c.get("phase") == "snapshot" else
           f'<span class="failed">{_e(say("failed") if (c.get("phase") or "failed") == "failed" else c.get("phase"))}'
           f'{" · " + _e(c["error"]) if c.get("error") else ""}</span>')
        + f'</td><td>{_number(c.get("captured") or 0)}</td><td>{gaps(c)}</td><td>'
        + (f'<code>{_e(c["file"])}</code>' if c.get("file") else "—") + "</td></tr>" for c in chats)
    chat_section = (f'<section class="card wide"><h2>{_e(say("Chat exports"))}</h2><table class="list"><tr class="head">'
                    + "".join(f"<td>{_e(say(name))}</td>" for name in ("Chat", "Result", "Messages", "Absent message IDs", "File"))
                    + f'</tr>{chat_rows}</table></section>') if chats else ""
    account_entry = ""
    if chats:
        account_entry = "<li>" + _e(say("Extract each chat-export-NNN.zip and open chat.html.")) + "</li>"
    if exported.get("file"):
        account_entry = "<li>" + marked(
            "Extract {file} ({size}, SHA-256 {sha256}) and open index.html.", file=f'<code>{_e(exported["file"])}</code>',
            size=_size(exported.get("bytes")), sha256=f'<code>{_e(exported.get("sha256"))}</code>') + "</li>"
    verify = (f"python -m tgwitness.sealed_verify evidence.zip --bundle attestation.jsonl --repo {_e(safe_repo or 'OWNER/TgWitness')}"
              "\npython verify.py evidence.zip")

    title = say("Sealed capture result")
    body = (
        f'<header><h1>{_e(title)}</h1><span class="badge {state}">{_e(label)}</span></header>'
        + "".join(alerts)
        + f'<div class="grid"><section class="card wide"><p class="lead">{_e(explanation)}</p>'
        + (f'<div class="stats">{"".join(stats)}</div>' if stats else "") + "</section>"
        + f'<section class="card"><h2>{_e(say("Check these identifiers"))}</h2>{_rows(say, identity)}</section>'
        + f'<section class="card"><h2>{_e(say("What was captured"))}</h2>{_rows(say, selection_rows)}</section>'
        + (f'<section class="card"><h2>{_e(say("Coverage"))}</h2>{_rows(say, coverage_rows)}</section>' if coverage_rows else "")
        + chat_section
        + run_log(facts, say)
        + f'<section class="card wide"><h2>{_e(say("Next steps"))}</h2><ol>' + account_entry
        + "<li>" + _e(say("Check the workflow run, the collector commit and the recipient key above.")) + "</li>"
        + f'<li>{_e(say("Verify:"))}<pre><code>{verify}</code></pre></li>'
        + "<li>" + _e(say("Signed records:")) + ' <a download href="events.jsonl">events.jsonl</a> · '
          '<a download href="coverage.json">coverage.json</a> · <a href="PACKAGING.json">PACKAGING.json</a> · '
          '<a href="README.txt">README.txt</a></li></ol></section></div>'
    )
    return (f'<!doctype html><html lang="{_e(say.language)}" dir="{_e(say.direction)}"><meta charset="utf-8">'
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; style-src '{STYLE_HASH}'; "
            "base-uri 'none'; form-action 'none'\">"
            f"<title>{_e(title)}</title><style>{STYLE}</style><body><main>{body}</main></body></html>").encode()


def text_keys():
    import ast
    from pathlib import Path
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    keys = [node.args[0].value for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in ("say", "marked") and node.args and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)]
    keys += [label for label, _ in ROW_LABELS]
    keys += [node.args[1].value for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
             and node.func.id == "_counted" and len(node.args) > 1 and isinstance(node.args[1], ast.Constant)
             and isinstance(node.args[1].value, str)]
    keys += list(STATE_LABELS.values())
    from .collector import TAKEOUT_SKIPPED_MEANING
    from .account_report import LIMIT_TEXTS
    recorded = [*TAKEOUT_SKIPPED_MEANING.values(), *LIMIT_TEXTS, "visible to this account during the recorded acquisition intervals",
                "Collection or full packaging failed. This archive is the compact signed journal of everything recorded "
                "before the failure; it is incomplete within the selected scope."]
    return list(dict.fromkeys(keys + [text for _, text in REASONS.values()] + list(CATEGORY_NAMES.values())
                              + list(MODE_NAMES.values()) + list(METHOD_NAMES.values()) + list(LOGOUT_STATES.values())
                              + list(PACKAGING_REASONS.values()) + list(STAT_CAPTIONS) + recorded))


ROW_LABELS = [(label, None) for label in (
    "Mode", "Scope", "Method requested", "Method used", "Why", "Date range (UTC)", "Media budget", "Report language",
    "Selection SHA-256", "Complete within scope", "Chat list read completely", "Export steps finished",
    "Failed pages and files", "Not reached before the stop", "Known limits", "Coverage", "Repository", "Workflow run",
    "Collector commit", "GitHub attestation", "Recipient key SHA-256", "Journal signing key", "Journal records", "Journal head",
    "Fresh session only", "Session logout", "Chat", "Result", "Messages", "Absent message IDs", "File")]
