"""Start page of a sealed (GitHub Actions) evidence archive: run outcome, identifiers to check, scale and next steps.

The page is static, script-free and built only from signed journal records of the sealed run. It names identifiers
(run, collector commit, recipient, signing key, journal head) but never account phone numbers or message content.
"""
import base64
import hashlib
import re
from html import escape

SEALED_KINDS = ("sealed.started", "sealed.selection", "sealed.account_export", "sealed.finished", "sealed.failure",
                "sealed.packaging", "account_export.transport")

REASONS = {
    "account_export_finished": ("complete", "The export finished within the selected scope."),
    "history_and_media_finished": ("complete", "Chat history and attachments finished."),
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
    "td:first-child{color:var(--muted);width:42%;padding-right:10px}tr:last-child td{border-bottom:0}"
    "code{font:12.5px/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;word-break:break-all}"
    ".stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px}"
    ".stat{border:1px solid var(--line);border-radius:10px;padding:10px 12px}.stat b{display:block;font-size:20px}"
    ".stat span{color:var(--muted);font-size:12.5px}.alert{border-left:4px solid var(--bad);padding:10px 14px;"
    "background:var(--card);border-radius:8px;margin:0 0 14px}.alert.warn{border-color:var(--warn)}"
    "pre{white-space:pre-wrap;margin:6px 0 0;padding:10px;border-radius:8px;background:var(--bg);"
    "border:1px solid var(--line)}ol{margin:0;padding-left:20px}li{margin:4px 0}a{color:var(--accent)}"
)
STYLE_HASH = "sha256-" + base64.b64encode(hashlib.sha256(STYLE.encode()).digest()).decode()


def collect(facts, event):
    """Keep the sealed-run records needed for the start page; called for every journal event."""
    if event["kind"] in SEALED_KINDS:
        facts.setdefault(event["kind"], []).append(event["payload"])


def _e(value):
    return escape(str(value), quote=True)


def _human(key):
    return re.sub(r"_+", " ", str(key)).strip().capitalize()


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return _e(value)
    return f"{value:,}".replace(",", " ")


def _size(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return _e(value)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            return (f"{value:.0f} {unit}" if unit == "B" else f"{value:.1f} {unit}")
        value /= 1024


def _rows(pairs):
    return "<table>" + "".join(f"<tr><td>{_e(k)}</td><td>{v}</td></tr>" for k, v in pairs if v not in (None, "")) + "</table>"


def outcome(facts):
    finished = (facts.get("sealed.finished") or [{}])[-1]
    if facts.get("sealed.failure"):
        return "partial", "Salvaged after a failure", ("Collection or full packaging failed. This archive keeps the "
                                                       "compact signed journal of everything recorded before it.")
    exported = (facts.get("sealed.account_export") or [{}])[-1]
    state, text = REASONS.get(finished.get("reason"), ("partial", "Capture ended: " + str(finished.get("reason"))))
    if exported and exported.get("complete_within_scope") is False:
        state = "partial"
    return state, {"complete": "Complete within the selected scope", "partial": "Partial"}[state], text


def page(facts, events, fingerprint=None, head_hash=None):
    started = (facts.get("sealed.started") or [{}])[0]
    context = started.get("context") or {}
    selection_event = (facts.get("sealed.selection") or [{}])[-1]
    selection = selection_event.get("selection") or {}
    exported = (facts.get("sealed.account_export") or [{}])[-1]
    finished = (facts.get("sealed.finished") or [{}])[-1]
    transports = facts.get("account_export.transport") or []
    state, label, explanation = outcome(facts)

    repo, run, attempt = context.get("repository"), context.get("run_id"), context.get("run_attempt")
    commit = context.get("collector_sha")
    safe_repo = repo if isinstance(repo, str) and re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) else None
    run_link = (f'<a href="https://github.com/{_e(safe_repo)}/actions/runs/{_e(run)}/attempts/{_e(attempt)}">'
                f"{_e(run)} · attempt {_e(attempt)}</a>") if safe_repo and str(run).isdigit() and str(attempt).isdigit() else _e(run)
    commit_link = (f'<a href="https://github.com/phishdestroy/TgWitness/commit/{_e(commit)}"><code>{_e(commit)}</code></a>'
                   if isinstance(commit, str) and re.fullmatch(r"[0-9a-f]{40}", commit) else _e(commit))

    alerts = []
    for failure in facts.get("sealed.failure") or []:
        alerts.append(f'<div class="alert"><b>Failure recorded:</b> {_e(failure.get("error"))}. '
                      f'{_e(failure.get("meaning", ""))}</div>')
    if finished.get("revocation") == "not_confirmed":
        alerts.append('<div class="alert warn"><b>Session logout was not confirmed.</b> Open Telegram → Settings → '
                      'Devices and end the session created by this capture.</div>')
    for packaging in facts.get("sealed.packaging") or []:
        alerts.append(f'<div class="alert warn"><b>Compact packaging:</b> {_e(packaging.get("reason"))}. All signed '
                      'records are kept; formatted duplicates were omitted.</div>')

    mode = selection.get("mode")
    options = selection.get("account_options") or {}
    requested = options.get("transport") if mode == "account" else "chat event journal"
    used = transports[-1].get("transport") if transports else (requested if requested != "auto" else None)
    used_reason = transports[-1].get("meaning") if transports else None
    scope = ("all accessible chats" if selection.get("account_scope") == "all" else
             f"{len(options.get('chat_ids') or [])} selected chats" if mode == "account" else
             f"one chat (ID {_e(selection.get('chat_id'))})")
    selection_rows = [("Mode", _e({"account": "Account export", "chat": "Chat event journal"}.get(mode, mode))),
                      ("Scope", _e(scope) if mode != "chat" else scope),
                      ("Method requested", _e(requested)), ("Method used", _e(used) if used else "recorded in the journal"),
                      ("Why", _e(used_reason) if used_reason else None),
                      ("Date range (UTC)", _e(" → ".join(str(x or "…") for x in (options.get("from_utc"), options.get("to_utc"))))
                       if options.get("from_utc") or options.get("to_utc") else None),
                      ("Media budget", _e(str(options.get("max_total_gib")) + " GiB") if options.get("max_total_gib") else None),
                      ("Selection SHA-256", "<code>" + _e(selection_event.get("selection_sha256")) + "</code>")]

    counts = dict(exported.get("counts") or {})
    if not counts and finished.get("history"):
        history = finished["history"]
        counts = {"messages_seen": history.get("captured"), **{"media_" + k: v for k, v in (finished.get("media") or {}).items()}}
    stats = []
    for key, value in counts.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            shown = _size(value) if "bytes" in key else _number(value)
            stats.append(f'<div class="stat"><b>{shown}</b><span>{_e(_human(key))}</span></div>')
    coverage = exported.get("coverage") or {}
    coverage_rows = [(_human(k), _e(v)) for k, v in coverage.items() if not isinstance(v, (dict, list))]
    if exported:
        coverage_rows.insert(0, ("Complete within scope", "yes" if exported.get("complete_within_scope") else "no"))

    identity = [("Repository", _e(repo)), ("Workflow run", run_link), ("Collector commit", commit_link),
                ("Recipient key SHA-256", "<code>" + _e(started.get("recipient_sha256")) + "</code>"),
                ("Journal signing key", "<code>" + _e(fingerprint) + "</code>" if fingerprint else None),
                ("Journal records", _number(events)), ("Journal head", "<code>" + _e(head_hash) + "</code>" if head_hash else None),
                ("Fresh session only", "yes" if started.get("session_import_allowed") is False else _e(started.get("session_import_allowed"))),
                ("Session logout", _e(finished.get("revocation")))]

    account_entry = ""
    if exported.get("file"):
        account_entry = (f'<li>Extract <code>{_e(exported["file"])}</code> ({_size(exported.get("bytes"))}, SHA-256 '
                         f'<code>{_e(exported.get("sha256"))}</code>) and open its <code>index.html</code>: per-chat pages, '
                         '<code>map.html</code> with the activity heatmap and message-ID gaps, and '
                         '<code>message-gaps.json</code>.</li>')
    verify = (f"python -m tgwitness.sealed_verify evidence.zip --bundle attestation.jsonl --repo {_e(safe_repo or 'OWNER/TgWitness')}"
              "\npython verify.py evidence.zip")

    body = (
        f'<header><h1>Sealed capture result</h1><span class="badge {state}">{_e(label)}</span></header>'
        + "".join(alerts)
        + f'<div class="grid"><section class="card wide"><p class="lead">{_e(explanation)}</p>'
          f'<p class="muted">Ended: {_e(finished.get("reason"))}. Built only from records signed during this run.</p>'
        + (f'<div class="stats">{"".join(stats)}</div>' if stats else "") + "</section>"
        + f'<section class="card"><h2>Check these identifiers</h2>{_rows(identity)}</section>'
        + f'<section class="card"><h2>What was captured</h2>{_rows(selection_rows)}</section>'
        + (f'<section class="card"><h2>Coverage</h2>{_rows(coverage_rows)}</section>' if coverage_rows else "")
        + '<section class="card wide"><h2>Next steps</h2><ol>' + account_entry
        + '<li>Compare the workflow run, collector commit and recipient key above with the run you started and '
          'the key you saved.</li>'
          f'<li>Verify with tools from an independently trusted checkout:<pre><code>{verify}</code></pre></li>'
          '<li>Signed records: <a download href="events.jsonl">events.jsonl</a> · '
          '<a download href="coverage.json">coverage.json</a> · <a href="PACKAGING.json">PACKAGING.json</a> · '
          '<a href="README.txt">README.txt</a></li></ol></section></div>'
    )
    return ("<!doctype html><html lang=\"en\"><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; style-src '{STYLE_HASH}'; "
            "base-uri 'none'; form-action 'none'\">"
            f"<title>Sealed capture result</title><style>{STYLE}</style><body><main>{body}</main></body></html>").encode()
