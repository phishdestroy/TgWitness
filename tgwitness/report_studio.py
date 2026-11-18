from itertools import islice

from . import report, report_analytics, report_secret, jurisdiction_guidance
from .store import utcnow

PREVIEW_LIMIT = 50000


def presentation(options, *, include_guidance=True):
    values = options.model_dump() if hasattr(options, "model_dump") else options
    if not include_guidance:
        values = {key: value for key, value in values.items() if key != "jurisdiction_guidance"}
    return report_analytics.Presentation.model_validate({key: values[key] for key in report_analytics.Presentation.model_fields if key in values})


def preview(store, options):
    say = report.Words(options["language"])
    analytics = report_analytics.Analytics()
    count = 0
    selection = report.report_selection.Selection.model_validate(options.get("selection") or {})
    includes = report.report_selection.compile_selection(selection)
    with store.snapshot() as snapshot:
        rows = iter(snapshot.events())
        for event in islice(rows, PREVIEW_LIMIT):
            if includes(event):
                analytics.add(event)
                count += 1
        sampled = next(rows, None) is not None
        conversations = report_secret.collect(snapshot.connection, None, selection.secret_chats,
                                              {t["chat_id"]: t["title"] for t in store.targets()})             if selection.enabled and selection.secret_chats else []
    material = report.report_material({"kind": "evidence", "options": options, "digest": {"analytics": analytics.result()}, "event_count": count})
    sections = [report.report_charts.examination_html(material.get("examination"), say),
                report.report_charts.html(material.get("analytics"), say)]
    if options.get("template") == "activity":
        sections.reverse()
    sections.append(jurisdiction_guidance.html(jurisdiction_guidance.build(options.get("jurisdiction_guidance"))))
    if conversations:
        sections.insert(0, report_secret.html(conversations, say, 2, report.utc_text, report.size_text, store.root / "media"))
    title = options.get("case_title") or (report_secret.title_of(say, conversations) if conversations and not selection.chats
                                          and not selection.messages else say("Telegram observation journal"))
    document = ('<!doctype html><html lang="' + report.e(say.language) + '" dir="' + say.direction
        + '" data-report-design="' + report.report_design.normalized(options.get("design")) + '" data-theme="' + report.e(options["theme"])
        + '" data-report-template="' + report.e(options.get("template", "dossier"))
        + '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<link rel="stylesheet" href="/report-preview.css"><title>' + report.e(title) + '</title></head>'
        '<body class="dossier studio-preview"><main><p class="preview-watermark preview-cover">'
        + report.e(say("DRAFT PREVIEW · NOT SIGNED")) + '</p>'
        + report.hero(say, say("Report preview"), title,
                      [(say("Case ID"), report.e(options.get("case_id"))),
                       (say("Examiner"), report.e(options.get("examiner"))),
                       (say("Organization"), report.e(options.get("organization"))),
                       (say("Created"), report.e(report.utc_text(utcnow())))], "", False, report.translation_notice(say))
        + '<p class="analytics-method">' + report.e(say("Cover and charts from this workspace's journal. Export adds the selected records, trust assessment and verification material."))
        + '</p><p>' + report.e(say("Preview analysed {n} records. The full export uses its complete selected scope.", n=count))
        + (' ' + report.e(say("Preview limit reached; these charts cover only the first 50,000 records.")) if sampled else '') + '</p>'
        + report.case_section(say, 1, options, [])
        + ''.join(sections) + '</main></body></html>')
    if options.get("design") in report.report_layouts.DESIGNS:
        document = b''.join(report.report_layouts.compose(
            [document.encode('utf-8')], options['design'], say, 'preview')).decode('utf-8')
    return {"html": document, "records": count, "sampled": sampled}
