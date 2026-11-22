from html import escape
from datetime import datetime, timezone
import re
from . import jurisdiction_guidance

FORMAT = "tgwitness-case-assessment-v1"
TITLE = "Basis of trust"
OVERVIEW = "Evidence at a glance"
INTRO = ("This assessment describes this archive. The recipient repeats the checks with verify.py and the collector "
         "fingerprint received separately.")
STANDALONE = "This is a standalone report. Obtain the signed ZIP to verify the authoritative records and supporting proofs."
STATUSES = {"checked_locally": "Checked during export", "recorded": "Recorded; review required",
            "not_included": "Not included in this copy", "not_checked": "Not independently checked",
            "incomplete": "Incomplete or unavailable", "recipient": "Checked by the recipient",
            "partial": "Covers part of the records"}
CONDITIONS_TITLE = "Conditions for evidence"
CONDITIONS_INTRO = "verify.py checks the same conditions. Each row states what the condition establishes and how the recipient checks it."
CONDITIONS = {"integrity": ("Integrity", "The archive is unchanged since the collector signed it."),
              "signer": ("Signer key", "The signing key is the collector key the recipient retained."),
              "external_time": ("External time", "A third party confirms that the covered records existed by the stated time."),
              "head_binding": ("Witness with its own key", "A second key retained the journal head. Who holds that key is shown by the "
                               "custodian's key-control record, kept with its fingerprint."),
              "checkpoint": ("Retained checkpoint", "Records up to the checkpoint match a journal state signed with the collector key. "
                             "They are bound only if the recipient obtained it before this archive, through another channel."),
              "environment": ("Attested collection run", "The signing key was created inside the attested collection run.")}
SUPPORTING = "Supporting records, not part of the minimum"
ROLES = {"integrity": "Required conditions", "signer": "Required conditions", "external_time": "Required conditions",
         "head_binding": SUPPORTING, "checkpoint": SUPPORTING, "environment": SUPPORTING}
MINIMUM = ("Minimum for evidence: integrity, the signer key, and external time from a third party covering the last record: "
           "a validated RFC 3161 timestamp, a Bitcoin proof, a witness post read from t.me or an attested collection run.")
ARCHIVES = {"evidence": "tgwitness-evidence.zip", "handover": "tgwitness-handover.zip", "chat": "tgwitness-chat-export.zip"}
LABELS = {"records": "Records", "first": "First record", "last": "Last record", "fingerprint": "Signing key fingerprint (SHA-256)",
          "gaps": "Gaps", "notes": "Coverage notes", "periods": "Continuous observation periods", "unobserved": "Message numbers not observed",
          "verified_stamps": "Validated timestamp receipts", "other_stamps": "Other timestamp receipts",
          "anchored_through": "Timestamp covers through record", "unanchored_tail": "Records after that checkpoint",
          "timestamp": "Timestamp", "messages": "Messages", "tasks_done": "Tasks completed", "tasks_total": "Tasks planned",
          "failures": "Failures and gaps", "failed": "Failed pages and files", "limits": "Known limits", "not_reached": "Not reached before collection stopped", "unchanged": "Unchanged records", "minimised": "Minimized records", "left_out": "Omitted records",
          "drand": "Recorded drand rounds", "starts": "Recorded process starts", "tdx": "Process starts carrying a TDX quote",
          "operator_fields": "Case fields supplied by the operator", "complete": "Completed within selected scope"}
RESULTS = {
    "integrity": "Checked {n} signed journal records; the key still needs independent confirmation.",
    "integrity_unknown": "Independent verification of this copy is still required.",
    "time": "Validated time bound through record #{n}; {tail} later records are outside that bound.",
    "time_unknown": "No independently validated time bound is included in this copy.",
    "coverage": "Recorded gaps: {gaps}. Coverage notes: {notes}. Message numbers not observed: {missing}.",
    "witness": "Recorded drand rounds: {drand}; starts carrying TDX: {tdx}. Independent validation is not supplied.",
    "custody": "Operator declarations supplied: {n}. The custody record of who acquired, held and transferred the original ZIP completes them.",
    "meaning": "Each statement cites the archive, file and record it rests on.",
    "complete": "Acquisition completed within the selected scope: {done} of {total} tasks.",
    "partial": "Acquisition is incomplete or its completion cannot be established from this copy.",
    "sharing": "This is a transformed selection; original completeness cannot be inferred.",
    "chat": "History snapshot: messages in their current version; the evidence journal holds earlier versions and deletion notices observed live.",
}

CSS = """
.case-assessment .assessment-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:20px}
.assessment-item{border:1px solid #8894a455;border-radius:12px;padding:18px;min-width:0;break-inside:avoid}
.assessment-item h3{margin:0 0 8px;font-size:16px}.assessment-state{font-size:12px;font-weight:600}
.assessment-item p{line-height:1.6;overflow-wrap:anywhere}.assessment-item dl{font-size:12px;display:grid;grid-template-columns:1fr 1fr;gap:6px 12px}
.assessment-item dt,.assessment-item dd{margin:0;overflow-wrap:anywhere}.assessment-item dd{font-variant-numeric:tabular-nums}
.case-assessment .assessment-item dd.hash{grid-column:1/-1;max-width:40ch;text-align:start;font-family:ui-monospace,Cascadia Mono,Consolas,SF Mono,Menlo,DejaVu Sans Mono,Liberation Mono,monospace}.case-assessment .assessment-item dd.hash span{display:inline-block;margin-inline-end:1ch}
.case-assessment .assessment-item dt:has(+dd.hash){grid-column:1/-1}.assessment-references code{font:inherit;font-family:ui-monospace,Cascadia Mono,Consolas,SF Mono,Menlo,DejaVu Sans Mono,Liberation Mono,monospace;background:none;border:0;padding:0;color:inherit}
.assessment-review{padding:12px;border-inline-start:3px solid #697d99;margin-top:14px}
.evidence-conditions{margin:18px 0;overflow-x:auto}.evidence-conditions h3{margin:0 0 6px;font-size:17px}
.evidence-conditions table{width:100%;border-collapse:collapse;font-size:13px;margin-top:10px}
.evidence-conditions th,.evidence-conditions td{border-top:1px solid #8894a455;padding:8px;text-align:start;vertical-align:top;overflow-wrap:break-word}
.evidence-conditions thead th:nth-child(1){width:15%}.evidence-conditions thead th:nth-child(2){width:27%}.evidence-conditions thead th:nth-child(3){width:30%}.evidence-conditions thead th:nth-child(4){width:28%}
.evidence-conditions tr.condition-role th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);padding-top:12px}
.evidence-conditions tr[data-status="checked_locally"] strong{color:var(--ok,#08734a)}.evidence-conditions tr[data-status="not_included"] strong{color:var(--muted)}
.evidence-conditions code,.evidence-conditions pre{font-size:12px;white-space:pre-wrap;overflow-wrap:anywhere}
.evidence-conditions td code{display:block;background:none;border:0;padding:0;white-space:normal;line-height:1.6}.evidence-conditions td code+code{margin-top:6px}
.evidence-conditions td code span{display:inline-block;max-width:100%;overflow-wrap:anywhere}
.evidence-conditions pre.command{margin:14px 0 0;padding:12px 14px;border:1px solid var(--line);border-radius:8px;background:var(--bg2,var(--bg))}
.case-assessment{--state-ok:#1d6b4f;--state-warn:#93570b;--state-bad:#b23b1e;--state-info:var(--accent,#2457c5);--state-off:var(--muted)}
@media(prefers-color-scheme:dark){html:not([data-theme=light]) .case-assessment{--state-ok:#5dd39e;--state-warn:#f2b35b;--state-bad:#ff8f86}}
html[data-theme=dark] .case-assessment{--state-ok:#5dd39e;--state-warn:#f2b35b;--state-bad:#ff8f86}
.case-assessment [data-status]{--state:var(--state-warn)}.case-assessment [data-status=checked_locally]{--state:var(--state-ok)}
.case-assessment [data-status=recipient]{--state:var(--state-info)}.case-assessment [data-status=incomplete]{--state:var(--state-bad)}
.case-assessment [data-status=not_included]{--state:var(--state-off)}
.case-assessment .assessment-state{color:var(--state);align-self:flex-start;padding:3px 10px 3px 9px;border-radius:999px;background:color-mix(in srgb,var(--state) 10%,transparent);font-weight:600}
.case-assessment .assessment-state::before{align-self:center}.evidence-conditions tr[data-status] td>strong{color:var(--state)}
@media screen and (min-width:761px){.case-assessment .assessment-grid>.assessment-item:last-child:nth-child(odd){grid-column:1/-1;columns:2;column-gap:48px}.case-assessment .assessment-grid>.assessment-item:last-child:nth-child(odd)>*{break-inside:avoid}.case-assessment .assessment-grid>.assessment-item:last-child:nth-child(odd)>.assessment-heading{column-span:all}}
@media(max-width:760px){.case-assessment .assessment-grid{grid-template-columns:1fr}}
@media(max-width:600px){.evidence-conditions thead{display:none}
.evidence-conditions tbody,.evidence-conditions tr,.evidence-conditions th,.evidence-conditions td{display:block}
.evidence-conditions tr{border-top:1px solid #8894a455;padding:6px 0}.evidence-conditions th,.evidence-conditions td{border:0;padding:4px 0}
.evidence-conditions td[data-label]::before{content:attr(data-label);display:block;font-size:11px;color:var(--muted)}}
@media print{.case-assessment .assessment-grid{display:block}.assessment-item{margin-bottom:10px}.evidence-conditions{overflow:visible}}
"""


def row(key, status, title, basis, limit, verify, facts=None, references=()):
    return dict(id=key, status=status, title=title, basis=basis, limitation=limit,
                verification=verify, facts=facts or {}, references=list(references))


REFERENCES_SHOWN = 12


def reference_text(references):
    shown = ", ".join(references[:REFERENCES_SHOWN])
    return shown + (" … +" + str(len(references) - REFERENCES_SHOWN) if len(references) > REFERENCES_SHOWN else "")


def result(item, key, **values):
    item["result"] = {"text": RESULTS[key], "values": values}


def verified_stamp(anchor, count):
    try:
        stamp = datetime.fromisoformat(anchor["time"].replace("Z", "+00:00"))
    except (KeyError, AttributeError, TypeError, ValueError):
        return False
    return (anchor.get("kind") == "rfc3161" and anchor.get("checkpoint_bound") is True
            and isinstance(anchor.get("signed"), dict)
            and isinstance(anchor["signed"].get("root_sha256"), str)
            and bool(re.fullmatch(r"[0-9a-f]{64}", anchor["signed"]["root_sha256"])) and stamp.tzinfo is not None
            and type(anchor.get("event_count")) is int and 0 <= anchor["event_count"] <= count)


def condition(key, status, detail, check, **values):
    title, scope = CONDITIONS[key]
    return {"id": key, "role": ROLES[key], "status": status, "title": title, "scope": scope,
            "detail": {"text": detail, "values": values}, "check": check}


def evidence_conditions(kind, context, count=0, latest=None, signals=None):
    archive = ("../" if context.get("archive") or kind == "chat" else "") + (context.get("archive_name") or ARCHIVES.get(kind, "archive.zip"))
    fp = "TRUSTED_SHA256"
    journal = kind == "evidence"
    anchors, latest = ((context.get("anchors") or []), latest) if journal else ([], None)
    verified = journal and context.get("journal_verified") is True
    rows = [condition("integrity", "checked_locally" if verified else "not_checked",
                      "Checked during export: {n} records." if verified else "The recipient checks every signature and file hash.",
                      "python verify.py " + archive, n=count),
            condition("signer", "recipient", "The recipient compares the collector fingerprint with a copy received separately.",
                      "--fingerprint " + fp)]
    if latest and latest.get("event_count") == count:
        status, detail = "checked_locally", "A validated timestamp covers records 1–{n} of {total}."
    elif latest:
        status, detail = "partial", "A validated timestamp covers records 1–{n} of {total}; later records need another binding."
    elif anchors:
        status, detail = "recorded", "Timestamp receipts are included; the recipient validates them."
    else:
        status, detail = "not_included", "No timestamp receipt in this archive."
    rows.append(condition("external_time", status, detail,
                          "--tsa-ca tsa-root.pem · --check-bitcoin · --witness witness.zip --channel https://t.me/s/WITNESS_CHANNEL",
                          n=(latest or {}).get("event_count", 0), total=count))
    if journal:
        rows.append(condition("head_binding", "recipient",
                              "A witness archive with a key other than the collector key shows that a second key retained the journal head.",
                              "--witness witness.zip --witness-fingerprint WITNESS_SHA256"))
        rows.append(condition("checkpoint", "recipient",
                              "A checkpoint the recipient received earlier, through another channel, shows that the records up to it "
                              "were not changed afterwards.", "--checkpoint retained.json"))
    else:
        rows.append(condition("head_binding", "not_included",
                              "This archive carries no journal checkpoints; it is bound through the evidence journal of the same workspace.",
                              "python verify.py tgwitness-evidence.zip --witness witness.zip --witness-fingerprint WITNESS_SHA256"))
    tdx = (signals or {}).get("tdx", 0)
    sealed = sealed_run(context)
    if sealed and not tdx:
        rows.append(condition("environment", "recorded",
                              "Made inside GitHub Actions run {run} (attempt {attempt}) of {repository}. GitHub's attestation.jsonl, "
                              "delivered next to evidence.zip, signs the archive that holds this export.",
                              "python -m tgwitness.sealed_verify evidence.zip --bundle attestation.jsonl --repo " + sealed["repository"],
                              **sealed))
    else:
        rows.append(condition("environment", "recorded" if tdx else "not_included",
                              "TDX quotes were recorded at {n} process starts." if tdx else "No attested collection run in this archive.",
                              "python -m tgwitness.cloud verify · --sealed-attestation", n=tdx))
    stamped = rows[2]["status"] == "checked_locally"
    command = ("python verify.py " + archive + " --fingerprint " + fp
               + (" --tsa-ca tsa-root.pem" if rows[2]["status"] in ("checked_locally", "partial", "recorded")
                  else " --witness witness.zip --channel https://t.me/s/WITNESS_CHANNEL" if journal else "")
               + (" --require evidence" if journal else ""))
    return {"conditions": rows, "minimum": MINIMUM,
            "outcome": ("This archive carries a validated timestamp of its last record: with the fingerprint confirmed it meets the minimum."
                        if stamped else
                        "The recipient needs external time from a third party covering the last record: a validated timestamp, "
                        "a witness post read from t.me or an attested collection run."
                        if journal else
                        "With the fingerprint confirmed this archive meets integrity and the signer key; external time comes from the evidence journal."),
            "command": command}


ACQUISITION_METHODS = {
    "journal": "Source: signed workspace journal.",
    "local": "The signed workspace journal contains only local operational records.",
    "telegram": "The signed workspace journal includes observations recorded by the Telegram client (MTProto).",
    "handover": "Extract from the signed workspace journal under the stated disclosure rules.",
    "chat": "History read through the Telegram API",
}


def acquisition_method(kind, digest):
    if kind in ("handover", "chat"):
        return ACQUISITION_METHODS[kind]
    if digest.get("telegram_observations"):
        return ACQUISITION_METHODS["telegram"]
    return ACQUISITION_METHODS["local" if digest.get("local_records_only") else "journal"]


def common(kind, reference, fingerprint, rows, operator_fields=0, *, archive=False, conditions=None, method=None):
    rows.extend([
        row("custody", "recorded" if operator_fields else "incomplete", "Operator and custody",
            "Case details and handover notes are statements supplied by the operator; their inclusion in a signed report preserves those statements.",
            "Custody entries preserve the recorded acquisition and handover details.",
            "Record who acquired, held and transferred the original ZIP. Preserve its hash, the trusted key fingerprint and independent checkpoint copies separately.",
            {"operator_fields": operator_fields}, ("manifest.json",)),
        row("meaning", "not_checked", "Source and acquisition record",
            method or "The collector records data visible to a Telegram account. The report identifies observations and their selected scope.",
            ("A valid signature shows that these bytes were signed with the workspace key. It does not identify the author "
             "of a message and does not show that the content of a message is true.") if method else
            "The records show what this Telegram account received and when it was observed; signatures, retained checkpoints, witness records and attested collection bind them to the collector and to outside parties.",
            "Cite the archive, file and record reference for each claim; an export of the same chat from a second account corroborates disputed content."),
    ])
    result(rows[-2], "custody", n=operator_fields)
    result(rows[-1], "meaning")
    return {"format": FORMAT, "kind": kind, "reference": reference, "fingerprint": fingerprint,
            "assessment_author": "exporter", "independent_review": "not_performed",
            "supporting_files_included": archive, "evidence_conditions": conditions, "checks": rows}


def journal(context, coverage):
    digest, handover = context.get("digest") or {}, context.get("handover")
    count = context.get("event_count") or 0
    anchors = context.get("anchors") or []
    stamps = [a for a in anchors if verified_stamp(a, count)]
    latest = max(stamps, key=lambda a: (a["event_count"], a["time"])) if stamps else None
    counts = (handover or {}).get("counts") or {}
    rows = [row("integrity", "checked_locally" if context.get("journal_verified") is True else "not_checked",
        "Integrity and substitution",
        "The journal chain and record signatures are checked against the exporter's key before packaging. The manifest and report seals bind the files in this copy." if context.get("journal_verified") is True else
        "No export-time journal verification result accompanies this report. Verify the authoritative records before relying on this copy.",
        "The key named in the archive identifies the signer once it is compared with a fingerprint received separately. A retained checkpoint or a confirmed witness fixes the journal against later replacement.",
        "Use verify.py from a trusted checkout with --fingerprint and a fingerprint obtained separately. Compare a previously retained checkpoint or an independent witness archive.",
        {"records": count, "first": digest.get("first"), "last": digest.get("last"), "fingerprint": context.get("fingerprint")},
        ("records.jsonl" if handover else "events.jsonl", "manifest.json", "manifest.sig"))]
    facts = {"verified_stamps": len(stamps), "other_stamps": len(anchors) - len(stamps)}
    if latest:
        facts.update(anchored_through=latest["event_count"], timestamp=latest["time"], unanchored_tail=count-latest["event_count"])
    rows.append(row("time", "checked_locally" if latest else "not_included" if not anchors else "incomplete",
        "Independent time bounds",
        "A validated timestamp binds a signed checkpoint to this journal prefix and a certificate chain trusted by this exporter. The counts below separate validated receipts from other files.",
        "A timestamp gives an upper bound for the checkpoint's existence, not the message's sending time. Later records are outside that bound. An OTS receipt or an unvalidated TSA reply is not a confirmed time bound.",
        "Recheck checkpoint inclusion, timestamp imprint, signature and certificate trust using the original receipt. Use --tsa-ca with an independently trusted TSA root; verify OTS against Bitcoin separately.",
        facts, tuple(a["file"] for a in stamps if a.get("file"))))
    coverage = coverage or {}
    rows.append(row("coverage", "recorded" if coverage else "incomplete", "Scope and missing material",
        "Observation periods and interruptions are derived from recorded collector activity. A minimized extract lists how many records were kept, changed or omitted.",
        "Coverage lists the observed periods and the recorded gaps. Message numbers not observed are gaps in observation; deletions are recorded as deletion notices.",
        "Compare coverage.json and the selection in manifest.json with the period and chats relevant to the case. Explain each material gap before drawing conclusions from absence.",
        {"gaps": len(coverage.get("gaps") or []), "notes": coverage.get("notes_total") or 0,
         "periods": len(coverage.get("continuous") or []),
         "unobserved": sum(c.get("not_observed", 0) for c in coverage.get("unobserved_ids") or []),
         **{k: counts[k] for k in ("unchanged", "minimised", "left_out") if k in counts}}, ("coverage.json", "manifest.json")))
    signals = digest.get("trust_signals") or {}
    rows.append(row("witness", "not_checked", "Witnesses and collection environment",
        "The counts below describe records included in this copy. A drand entry or a TDX quote is evidence to verify, not a configuration-based assurance badge.",
        "A drand round shows that a record was written after the round; timestamps or a witness give the upper time bound. A TDX quote counts once its measurements, freshness and key binding are checked.",
        "Compare an independently retained witness ZIP using --witness. Confirm beacon rounds using --check-drand. For TDX, check the quote, challenge, Intel trust chain, measurements and exact deployed source with the assurance verifier.",
        {k: signals.get(k, 0) for k in ("drand", "starts", "tdx")}, ("records.jsonl" if handover else "events.jsonl",)))
    result(rows[0], "integrity" if context.get("journal_verified") is True else "integrity_unknown", n=count)
    result(rows[1], "time" if latest else "time_unknown", n=latest["event_count"] if latest else 0,
           tail=count-latest["event_count"] if latest else 0)
    result(rows[2], "coverage", gaps=rows[2]["facts"]["gaps"], notes=rows[2]["facts"]["notes"],
           missing=rows[2]["facts"]["unobserved"])
    result(rows[3], "witness", drand=signals.get("drand", 0), tdx=signals.get("tdx", 0))
    options = context.get("options") or {}
    return jurisdiction_guidance.attach(common("handover" if handover else "evidence", context.get("report_id"), context.get("fingerprint"), rows,
                  sum(bool(options.get(k)) for k in ("case_title", "case_id", "examiner", "organization", "notes")),
                  archive=context.get("archive") is True, method=acquisition_method("handover" if handover else "evidence", digest),
                  conditions=evidence_conditions("handover" if handover else "evidence", context, count, latest, signals)), options)


def split_failures(context):
    coverage, limits = context.get("coverage") or {}, context.get("known_limits")
    if "failures" not in coverage:
        return {}
    if isinstance(limits, list) and type(coverage["failures"]) is int:
        counts = context.get("counts") or {}
        unreached = sum(counts.get(key) for key in ("media_not_reached", "steps_not_reached") if type(counts.get(key)) is int)
        return {"failed": max(0, coverage["failures"] - len(limits) - unreached), "limits": len(limits),
                **({"not_reached": unreached} if unreached else {})}
    return {"failures": coverage["failures"]}


def sealed_run(context):
    run = (context.get("sealed_run") or (context.get("digest") or {}).get("sealed_run")
           or (context.get("options") or {}).get("sealed_run"))
    if not isinstance(run, dict):
        return None
    repo, number = run.get("repository"), run.get("run_id")
    if not (isinstance(repo, str) and re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) and str(number).isdigit()):
        return None
    return {"repository": repo, "run": str(number), "attempt": str(run.get("run_attempt") or 1)}


def snapshot(context, kind="account", meta=None):
    meta = meta or {}
    sharing = kind == "sharing"
    chat = kind in ("chat", "account_chat")
    counts, coverage = context.get("counts") or {}, context.get("coverage") or {}
    complete = (context.get("complete_within_scope") is True and coverage.get("inventory_complete") is True
                and type(coverage.get("failures")) is int and coverage["failures"] == 0
                and type(coverage.get("tasks_total")) is int and coverage.get("tasks_done") == coverage["tasks_total"])
    rows = [row("integrity", "not_checked", "Integrity and substitution",
        "The signed manifest binds the authoritative data files and readable report to the key named in this copy.",
        "The collector key signs the manifest. The recipient confirms that key with a fingerprint received separately; retained checkpoints, witness records or timestamps fix the records against later replacement.",
        "Verify the original ZIP with a trusted copy of verify.py and --fingerprint from a separate trusted channel. Keep the verification result with the unchanged ZIP.",
        {"fingerprint": context.get("fingerprint")}, ("manifest.json", "manifest.sig")),
        row("scope", "recorded" if sharing or chat or complete else "incomplete", "Scope and missing material",
            "This sharing copy is a separately signed derivative with selected or transformed content." if sharing else
            "This is a history acquisition within the selected scope. Completion counts describe acquisition tasks, not everything that ever existed on Telegram.",
            "A signed derivative does not by itself prove correct derivation from the original. Names, text and context may have been changed or omitted." if sharing else
            "History is read chat by chat as Telegram returns it; the evidence journal holds earlier versions and deletion notices observed live.",
            "Review the public selection and transformations. If authorized, compare the derivative against the separately retained original." if sharing else
            "Review filters, limits, task failures and message-ID coverage against the specific period and conversations needed for the case.",
            {"messages": meta.get("message_count", counts.get("messages")), **({} if sharing or chat else
             {"complete": complete, **{k: coverage[k] for k in ("tasks_done", "tasks_total") if k in coverage},
              **split_failures(context)})},
            ("messages.jsonl", "manifest.json") if sharing else ("chat.json", "message-ids.json") if kind == "chat" else ("inventory.json", "manifest.json")),
        row("time", "not_included", "Independent time bounds",
            "This copy contains capture or export times recorded by the collector.",
            "Message dates come from Telegram and capture times from the collector clock; independent time comes from timestamps or a witness on the evidence journal.",
            "Preserve independent receipts for the original archive hash when available. Do not describe collector clock values as independently certified times."),
    ]
    options = context.get("options") or {}
    result(rows[0], "integrity_unknown")
    result(rows[1], "sharing" if sharing else "chat" if chat else "complete" if complete else "partial",
           **({"done":coverage.get("tasks_done"), "total":coverage.get("tasks_total")} if complete and not sharing and not chat else {}))
    result(rows[2], "time_unknown")
    return jurisdiction_guidance.attach(common(kind, context.get("archive_reference") or context.get("report_id"), context.get("fingerprint"), rows,
                  0 if sharing else sum(bool(options.get(k)) for k in ("case_title", "case_id", "examiner", "organization", "notes")),
                  archive=context.get("archive") is True, conditions=evidence_conditions(kind, context)),
                  context.get("presentation") or ({} if sharing else options))


def number_text(value, say):
    if type(value) is not int or abs(value) < 1000:
        return str(value)
    return format(value, ",").replace(",", "," if getattr(say, "language", "en") == "en" else "\u202f")


def result_text(result, say):
    text = say(result["text"], **result["values"])
    for key, value in result["values"].items():
        if type(value) is int and abs(value) >= 1000 and "#{" + key + "}" not in result["text"]:
            text = re.sub(r"(?<![\d#])" + re.escape(str(value)) + r"(?!\d)", number_text(value, say), text, count=1)
    return text


def fact_text(value, say):
    if isinstance(value, bool):
        return say("Yes" if value else "No")
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?(Z|[+-]\d\d:\d\d)?", value):
        try:
            moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return value
        if moment.tzinfo:
            return moment.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S") + " UTC"
        return moment.strftime("%Y-%m-%d %H:%M:%S")
    return number_text(value, say) if value is not None else say("Not recorded")


def fact_html(key, value, say, e):
    if key == "fingerprint" and isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value):
        return '<dd class="hash" dir="ltr">' + ''.join('<span>' + value[i:i + 4] + '</span>' for i in range(0, 64, 4)) + '</dd>'
    return '<dd dir="auto">' + e(fact_text(value, say)) + '</dd>'


def conditions_html(data, say, e):
    if not data:
        return ""
    rows, role = [], None
    labels = [' data-label="' + e(say(text)) + '">' for text in ("What it establishes", "In this archive", "How the recipient checks it")]
    for item in data["conditions"]:
        if item.get("role") and item["role"] != role:
            role = item["role"]
            rows.append('<tr class="condition-role"><th colspan="4" scope="rowgroup">' + e(say(role)) + '</th></tr>')
        rows.append('<tr data-status="' + e(item["status"]) + '"><th scope="row">' + e(say(item["title"])) + '</th><td'
                    + labels[0] + e(say(item["scope"])) + '</td><td' + labels[1] + '<strong>' + e(say(STATUSES[item["status"]]))
                    + '</strong><br>' + e(result_text(item["detail"], say)) + '</td><td' + labels[2]
                    + ''.join('<code dir="ltr">' + ' '.join('<span>' + e(token) + '</span>' for token in part.split()) + '</code>'
                              for part in item["check"].split(" · ")) + '</td></tr>')
    return ('<div class="evidence-conditions"><h3>' + e(say(CONDITIONS_TITLE)) + '</h3><p>' + e(say(CONDITIONS_INTRO))
            + '</p><table><thead><tr><th>' + e(say("Condition")) + '</th><th>' + e(say("What it establishes")) + '</th><th>'
            + e(say("In this archive")) + '</th><th>' + e(say("How the recipient checks it")) + '</th></tr></thead><tbody>' + "".join(rows)
            + '</tbody></table><p class="assessment-review"><strong>' + e(say(data["minimum"])) + '</strong> '
            + e(say(data["outcome"])) + '</p><pre class="command" dir="ltr">' + e(data["command"]) + '</pre></div>')


def html(data, say):
    e = lambda value: escape(str(value), quote=True)
    parts = ['<section class="card panel case-assessment" id="case-assessment"><h2>' + e(say(TITLE)) + '</h2><p>' + e(say(INTRO)) + '</p>']
    if not data.get("supporting_files_included"):
        parts.append('<p class="assessment-review">' + e(say(STANDALONE)) + '</p>')
    parts.append(conditions_html(data.get("evidence_conditions"), say, e))
    parts.append('<div class="assessment-grid">')
    for number, item in enumerate(data["checks"], 1):
        conclusion = item["result"]
        parts.append('<article class="assessment-item" id="assessment-' + e(item["id"]) + '" data-status="' + e(item["status"]) + '" data-assessment="' + e(item["id"]) + '"><div class="assessment-heading"><span class="assessment-index">'
                     + f'{number:02d}' + '</span><h3>' + e(say(item["title"])) + '</h3></div><div class="assessment-state">' + e(say(STATUSES[item["status"]]))
                     + '</div><p class="assessment-result">' + e(result_text(conclusion, say)) + '</p><p class="assessment-basis">' + e(say(item["basis"])) + '</p>')
        if item["facts"]:
            parts.append('<dl>' + ''.join('<dt>' + e(say(LABELS.get(k, k))) + '</dt>' + fact_html(k, v, say, e)
                                          for k, v in item["facts"].items()) + '</dl>')
        parts.append('<p class="assessment-limit"><strong>' + e(say("Scope of this conclusion")) + '</strong>' + e(say(item["limitation"])) + '</p><p class="assessment-review"><strong>' + e(say("Independent review")) + '</strong>' + e(say(item["verification"])) + '</p>')
        if item["references"]:
            shown = item["references"][:REFERENCES_SHOWN]
            parts.append('<p class="assessment-references">' + e(say("Evidence references")) + ': '
                         + ', '.join('<code dir="ltr">' + e(name) + '</code>' for name in shown)
                         + (' … +' + str(len(item["references"]) - len(shown)) if len(item["references"]) > len(shown) else '') + '</p>')
        parts.append('</article>')
    return ''.join(parts) + '</div></section>' + jurisdiction_guidance.html(data.get("jurisdiction_guidance"))


def pdf(lay, data):
    say = lay.say
    lay.section(say(TITLE), say(INTRO))
    if not data.get("supporting_files_included"):
        lay.callout(say(STANDALONE))
    conditions = data.get("evidence_conditions")
    if conditions:
        lay.heading(say(CONDITIONS_TITLE))
        lay.text(say(CONDITIONS_INTRO), size=8.5)
        lay.gap(1.5)
        lay.grid([say("Condition"), say("What it establishes"), say("In this archive"), say("How the recipient checks it")],
                 [(say(item["title"]) + ("\n" + say(item["role"]) if item.get("role") else ""), say(item["scope"]),
                   say(STATUSES[item["status"]]) + ": " + result_text(item["detail"], say), item["check"])
                  for item in conditions["conditions"]], widths=(17, 31, 30, 22))
        lay.callout(say(conditions["minimum"]) + " " + say(conditions["outcome"]))
        lay.command(conditions["command"])
    lay.assessment_overview(data)
    lay.gap(6)
    for number, item in enumerate(data["checks"], 1):
        lay.assessment_card(number, item)
    jurisdiction_guidance.pdf(lay, data.get("jurisdiction_guidance"))


def text_keys():
    examples = [journal({}, {}), snapshot({}), snapshot({}, "sharing"), snapshot({}, "chat"), journal({"journal_verified": True}, {})]
    conditions = [data["evidence_conditions"] for data in examples] + [
        evidence_conditions("evidence", {"journal_verified": True, "anchors": [{}]}, 2, {"event_count": 1}, {"tdx": 1}),
        evidence_conditions("evidence", {"anchors": [{}]}, 2, {"event_count": 2}),
        evidence_conditions("evidence", {"anchors": [{}]}, 2),
        evidence_conditions("account", {"sealed_run": {"repository": "o/r", "run_id": 1, "run_attempt": 1}})]
    return list(dict.fromkeys([TITLE, INTRO, OVERVIEW, *ACQUISITION_METHODS.values(), "Scope of this conclusion", "Independent review", "Evidence references", "Not recorded",
                              CONDITIONS_TITLE, CONDITIONS_INTRO, "Condition", "What it establishes", "In this archive",
                              "How the recipient checks it", *(text for pair in CONDITIONS.values() for text in pair), *ROLES.values(),
                              *(c[k] for c in conditions for k in ("minimum", "outcome")),
                              *(r["detail"]["text"] for c in conditions for r in c["conditions"]),
                              *STATUSES.values(), *LABELS.values(),
                              *(r[k] for data in examples for r in data["checks"] for k in ("title", "basis", "limitation", "verification")), *RESULTS.values(), STANDALONE]))
