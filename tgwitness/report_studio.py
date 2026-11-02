"""Read-only, bounded cover/analytics preview using the production report components."""
from itertools import islice

from . import report, report_analytics
from .store import utcnow

PREVIEW_LIMIT = 50000


def presentation(options):
    values = options.model_dump() if hasattr(options, "model_dump") else options
    return report_analytics.Presentation.model_validate({key: values[key] for key in report_analytics.Presentation.model_fields if key in values})


def preview(store, options):
    say = report.Words(options["language"])
    analytics = report_analytics.Analytics()
    with store.snapshot() as snapshot:
        rows = iter(snapshot.events())
        for event in islice(rows, PREVIEW_LIMIT):
            analytics.journal(event)
        sampled = next(rows, None) is not None
    data = analytics.result()
    report_analytics.chat_labels(data, {row["chat_id"]: row["title"] for row in store.targets() if row.get("title")})
    title = options.get("case_title") or say("Telegram observation journal")
    # An external stylesheet works under the panel's strict CSP. No scripts,
    # inline styles, external assets, signing operations or stored preview files.
    document = ('<!doctype html><html lang="' + report.e(say.language) + '" dir="' + say.direction
        + '" data-template="' + report.e(options["template"]) + '" data-theme="' + report.e(options["theme"])
        + '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<link rel="stylesheet" href="/report-preview.css"><title>' + report.e(title) + '</title></head>'
        '<body class="dossier studio-preview"><main><p class="preview-watermark">'
        + report.e(say("DRAFT PREVIEW · NOT SIGNED")) + '</p>'
        + report.hero(say, say("Report preview"), title,
                      [(say("Case ID"), report.e(options.get("case_id"))),
                       (say("Examiner"), report.e(options.get("examiner"))),
                       (say("Organization"), report.e(options.get("organization"))),
                       (say("Created"), report.e(report.utc_text(utcnow())))], "", False)
        + '<p class="analytics-method">' + report.e(say("Cover and charts from this workspace's journal. Export adds the selected records, trust assessment and verification material."))
        + '</p><p>' + report.e(say("Preview analysed {n} records. The full export uses its complete selected scope.", n=data["records"]))
        + (' ' + report.e(say("Preview limit reached; these charts cover only the first 50,000 records.")) if sampled else '') + '</p>'
        + report.case_section(say, 1, options, [])
        + report_analytics.html_section(data, options, say) + '</main></body></html>')
    return {"html": document, "records": data["records"], "sampled": sampled}
