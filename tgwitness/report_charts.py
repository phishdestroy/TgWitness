"""Offline report figures, with the same selected aggregates in HTML, PDF and JSON."""
from datetime import date
from html import escape
import math

TITLE = "Activity and participants"
INTRO = "Counts describe observations in this journal, not unique messages or all activity on Telegram. Repeated history reads can record the same message again."
TIME_NOTE = "Times use the collector's observation clock in UTC, not message sending times. An empty interval means no observations were counted; consult coverage for interruptions."
PEOPLE_NOTE = "Participants are ranked by new, historical and recovered message observations. Edits and deletions are not attributed to a person."
PRIVACY_NOTE = "Aliases apply to charts only. Source records remain unchanged."
REVIEW_TITLE = "Examination notes"
REVIEW_NOTE = "Written by the report's author. These statements are sealed with the report; they are separate from the software's checks."
REVIEW_FIELDS = {"question": "Question examined", "method": "Method used", "findings": "Findings", "conclusion": "Conclusion"}
KINDS = {"new": "New-message observations", "snapshot": "History observations", "recovered": "Recovered-message observations",
         "edited": "Edit observations", "deleted": "Deletion observations", "missing": "Missing on recheck"}
COLORS = {"new": "#247e8c", "snapshot": "#5776b3", "recovered": "#8c70aa", "edited": "#b28226",
          "deleted": "#b65264", "missing": "#7e8794"}
DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

CSS = """
.report-analytics{--chart-ink:#247e8c}.analytics-meta{font:11px/1.8 ui-monospace,monospace;overflow-wrap:anywhere;color:var(--muted)}
.analytics-totals{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin:24px 0}
.analytics-totals div{padding:18px;background:var(--card,var(--paper));min-width:0}.analytics-totals b{font:30px/1.3 Georgia,serif;display:block}
.analytics-totals span{font-size:11px;overflow-wrap:anywhere}.analytics-figure{margin:28px 0;padding:22px;border:1px solid var(--line);break-inside:avoid;min-width:0}
.analytics-figure figcaption{font-weight:650;font-size:16px;margin-bottom:12px}.analytics-figure p{font-size:12px;line-height:1.7;color:var(--muted)}
.analytics-figure svg{width:100%;height:auto;display:block;direction:ltr}.analytics-svg-label{fill:var(--ink);font:12px system-ui,sans-serif}
.analytics-axis{fill:var(--muted);font:10px ui-monospace,monospace}.analytics-grid{stroke:var(--line);stroke-width:1}
.analytics-legend{list-style:none;display:flex;flex-wrap:wrap;gap:8px 18px;padding:0;font-size:11px}.analytics-legend li{display:flex;gap:6px;align-items:center}
.analytics-legend i{width:9px;height:9px;display:inline-block}.analytics-table{margin-top:18px}.analytics-table summary{cursor:pointer;font-size:12px;color:var(--accent);padding:8px 0}
.analytics-data{width:100%;border-collapse:collapse;font-size:11px;table-layout:fixed}.analytics-data th,.analytics-data td{border-bottom:1px solid var(--line);padding:8px 5px;overflow-wrap:anywhere;text-align:start}
.analytics-print-data{display:none}
.analytics-bar{display:grid;grid-template-columns:minmax(110px,1fr) minmax(50px,2fr) 64px;gap:14px;align-items:center;margin:16px 0;font-size:12px}
.analytics-bar-label{overflow-wrap:anywhere}.analytics-bar-value{text-align:end;font-variant-numeric:tabular-nums}.analytics-bar-track{background:var(--line);height:12px}
.analytics-bar-fill{background:var(--chart-ink);height:100%;min-width:1px}.analytics-pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.analytics-pair>.analytics-figure{margin-top:0}
.examination-text{white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px;line-height:1.85;max-width:80ch}.examination-part{border-top:1px solid var(--line);padding-top:18px;margin-top:24px;break-inside:avoid}
[data-report-template=dossier] .examination-part{display:grid;grid-template-columns:minmax(130px,1fr) minmax(0,3fr);gap:24px}
[data-report-template=dossier] .examination-part h3{font:11px/1.8 system-ui,sans-serif;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
[data-report-template=dossier] .examination-text{font-family:Georgia,'Times New Roman',serif;font-size:16px}
[data-report-template=brief] .hero h1{font-family:system-ui,sans-serif;font-size:clamp(28px,4vw,42px);letter-spacing:-.035em}
[data-report-template=brief] .dossier .hero{padding:26px 32px;background:#172b37;border-bottom-width:2px}
[data-report-template=brief] .dossier .tile{padding:14px 20px}
[data-report-template=activity] .dossier{--dossier-navy:#153b40;--dossier-gold:#7ec6c0}
[data-report-template=activity] .dossier .hero h1{font-family:system-ui,sans-serif;font-weight:600;letter-spacing:-.04em}
[data-report-template=activity] .analytics-totals b{font-family:ui-monospace,monospace;font-size:26px;font-variant-numeric:tabular-nums}
@media(max-width:800px){.analytics-pair{grid-template-columns:1fr}.analytics-totals{grid-template-columns:repeat(2,minmax(0,1fr))}.analytics-figure{padding:14px}.analytics-bar{grid-template-columns:minmax(70px,1fr) minmax(30px,1fr) 52px;gap:8px}}
@media(max-width:600px){[data-report-template=dossier] .examination-part{display:block}}
@media print{.analytics-pair{display:block}.analytics-table{display:none}.analytics-print-data{display:block}.analytics-figure{break-inside:auto;padding:12px}.analytics-totals div{padding:10px}}
"""


def text_keys():
    return [TITLE, INTRO, TIME_NOTE, PEOPLE_NOTE, PRIVACY_NOTE, REVIEW_TITLE, REVIEW_NOTE, *REVIEW_FIELDS.values(),
            *KINDS.values(), *DAYS, "Recorded activity over time", "Observation times by weekday and hour", "Most observed participants",
            "Activity by chat", "Exact figures", "Period (UTC)", "Observations", "First record", "Last record", "Source file",
            "No observations in this selection.", "This chart exceeds the grouping limit. Exact overall counts remain available.",
            "Observations with an unusable time: {n}", "Participant {n}", "Sender {id}", "Chat {id}", "Unknown", "Other",
            "All bars start at zero. Values are counts, not percentages.", "Hour (UTC)", "Counts by category", "Report sections"]


def _e(value):
    return escape(str(value), quote=True)


def label(row, say):
    return say(row["label"], **row.get("label_values", {}))


def activity_bins(rows, maximum=36):
    """Equal-width chronological bins; never compress missing dates out of the axis."""
    if not rows:
        return []
    monthly = len(rows[0]["period"]) == 7
    def number(period):
        return int(period[:4])*12 + int(period[5:7])-1 if monthly else date.fromisoformat(period).toordinal()
    def period(value):
        return f"{value//12:04d}-{value%12+1:02d}" if monthly else date.fromordinal(value).isoformat()
    first, last = min(number(r["period"]) for r in rows), max(number(r["period"]) for r in rows)
    width = max(1, math.ceil((last-first+1)/maximum))
    result = []
    for start in range(first, last+1, width):
        end = min(start+width-1, last)
        result.append({"period": period(start) if start == end else period(start)+" – "+period(end),
                       "counts": dict.fromkeys(KINDS, 0), "total": 0})
    for row in rows:
        target = result[(number(row["period"])-first)//width]
        target["total"] += row["total"]
        for kind in KINDS:
            target["counts"][kind] += row["counts"].get(kind, 0)
    return result


def _table(headers, rows, say):
    table = ('<table class="analytics-data"><thead><tr>'
            + ''.join('<th scope="col">'+_e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'
            + ''.join('<tr>'+''.join('<td>'+_e(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table>')
    # Closed details stays non-rendered in several print engines, despite display overrides.
    return ('<details class="analytics-table"><summary>'+_e(say("Exact figures"))+'</summary>'+table+'</details>'
            + '<div class="analytics-print-data">'+table+'</div>')


def _unavailable(chart, say):
    if chart.get("status", "available") != "available":
        return '<p>'+_e(say("This chart exceeds the grouping limit. Exact overall counts remain available."))+'</p>'
    return ''


def activity_svg(rows, say):
    if not rows:
        return '<p>'+_e(say("No observations in this selection."))+'</p>'
    maximum = max(r["total"] for r in rows) or 1
    parts = ['<svg viewBox="0 0 720 245" role="img" aria-label="'+_e(say("Recorded activity over time"))+'">']
    for value in (0, maximum/2, maximum):
        y = 200-170*value/maximum
        parts.append(f'<line class="analytics-grid" x1="50" y1="{y:.2f}" x2="705" y2="{y:.2f}"/><text class="analytics-axis" x="43" y="{y+4:.2f}" text-anchor="end">{value:g}</text>')
    step = 650/len(rows)
    for index, row in enumerate(rows):
        y = 200
        parts.append('<g><title>'+_e(row["period"]+' · '+str(row["total"]))+'</title>')
        for kind, color in COLORS.items():
            height = 170*row["counts"].get(kind, 0)/maximum
            y -= height
            if height:
                parts.append(f'<rect x="{52+index*step:.2f}" y="{y:.2f}" width="{max(1,step-3):.2f}" height="{height:.2f}" fill="{color}"/>')
        parts.append('</g>')
    parts.append('<text class="analytics-axis" x="50" y="223">'+_e(rows[0]["period"].split(' – ')[0])+'</text>')
    parts.append('<text class="analytics-axis" x="705" y="223" text-anchor="end">'+_e(rows[-1]["period"].split(' – ')[-1])+'</text></svg>')
    return ''.join(parts)


def heat_svg(chart, say):
    rows = chart["rows"]
    maximum = max((value for row in rows for value in row), default=0) or 1
    parts = ['<svg viewBox="0 0 760 226" role="img" aria-label="'+_e(say("Observation times by weekday and hour"))+'">']
    for hour in range(0, 24, 3):
        parts.append(f'<text class="analytics-axis" x="{144+hour*25}" y="16" text-anchor="middle">{hour:02d}</text>')
    for day, row in enumerate(rows):
        parts.append(f'<text class="analytics-svg-label" x="125" y="{43+day*25}" text-anchor="end">'+_e(say(DAYS[day]))+'</text>')
        for hour, value in enumerate(row):
            parts.append(f'<rect x="{133+hour*25}" y="{27+day*25}" width="22" height="22" rx="2" fill="#247e8c" fill-opacity="{.08+.92*value/maximum:.3f}"><title>'
                         +_e(say(DAYS[day])+f' {hour:02d}:00 UTC · {value}')+'</title></rect>')
    parts.append('<text class="analytics-axis" x="735" y="220" text-anchor="end">'+_e(say("Hour (UTC)"))+'</text></svg>')
    return ''.join(parts)


def bars_html(chart, say):
    if error := _unavailable(chart, say):
        return error
    rows = chart["rows"]
    maximum = max((r["total"] for r in rows), default=0) or 1
    parts = []
    for row in rows:
        parts.append('<div class="analytics-bar"><span class="analytics-bar-label">'+_e(label(row, say))+'</span><div class="analytics-bar-track" aria-hidden="true"><div class="analytics-bar-fill" style="width:'
                     +f'{100*row["total"]/maximum:.3f}%"></div></div><b class="analytics-bar-value">'+str(row["total"])+'</b></div>')
    if not rows:
        return '<p>'+_e(say("No observations in this selection."))+'</p>'
    parts.append(_table([say("Observations"), say("First record"), say("Last record")],
                        [(label(r, say)+' · '+str(r["total"]), '#'+str(r["first_seq"]) if r.get("first_seq") else '—',
                          '#'+str(r["last_seq"]) if r.get("last_seq") else '—') for r in rows], say))
    return ''.join(parts)


def html(data, say):
    if not data:
        return ''
    parts = ['<section class="card report-analytics" id="report-analytics"><h2>'+_e(say(TITLE))+'</h2><p>'+_e(say(INTRO))+'</p>']
    source = data.get("source") or {}
    parts.append('<p class="analytics-meta">'+_e(say("Source file"))+': '+_e(source.get("file", "events.jsonl"))+'<br>SHA-256 · '+_e(source.get("sha256") or '—')+'</p>')
    parts.append('<p class="analytics-meta">'+_e(str(data.get("first_observed_at") or '—')+' → '+str(data.get("last_observed_at") or '—'))
                 +' · UTC<br>'+_e(say("Observations"))+': '+str(data["activity_events"])+'</p>')
    parts.append('<div class="analytics-totals">'+''.join('<div><b>'+str(data["totals"].get(kind, 0))+'</b><span>'+_e(say(title))+'</span></div>' for kind, title in KINDS.items())+'</div>')
    if chart := data.get("activity"):
        parts.append('<figure class="analytics-figure"><figcaption>'+_e(say("Recorded activity over time"))+'</figcaption><p>'+_e(say(TIME_NOTE))+'</p>')
        if error := _unavailable(chart, say):
            parts.append(error)
        else:
            rows = activity_bins(chart["rows"])
            parts.append(activity_svg(rows, say))
            parts.append('<ul class="analytics-legend">'+''.join('<li><i style="background:'+COLORS[k]+'" aria-hidden="true"></i>'+_e(say(v))+'</li>' for k, v in KINDS.items())+'</ul>')
            parts.append(_table([say("Period (UTC)"), say("Observations"), say("Counts by category")],
                               [(r["period"], r["total"], '; '.join(say(KINDS[k])+': '+str(v) for k, v in r["counts"].items() if v)) for r in rows], say))
        parts.append('</figure>')
    if chart := data.get("hourly"):
        parts.append('<figure class="analytics-figure"><figcaption>'+_e(say("Observation times by weekday and hour"))+'</figcaption>'+heat_svg(chart, say))
        parts.append(_table([say("Period (UTC)"), say("Observations")],
                           [(say(DAYS[d])+f' {hour:02d}:00', value) for d, row in enumerate(chart["rows"]) for hour, value in enumerate(row)], say))
        parts.append('</figure>')
    parts.append('<div class="analytics-pair">')
    for key, title in (("participants", "Most observed participants"), ("chats", "Activity by chat")):
        if chart := data.get(key):
            parts.append('<figure class="analytics-figure"><figcaption>'+_e(say(title))+'</figcaption>')
            if key == 'participants':
                parts.append('<p>'+_e(say(PEOPLE_NOTE))+'</p>')
                if data.get("participant_labels") != "ids":
                    parts.append('<p>'+_e(say(PRIVACY_NOTE))+'</p>')
            parts.append('<p>'+_e(say("Observations"))+': '+str(chart["total"])+'</p>'+bars_html(chart, say)+'</figure>')
    parts.append('</div><p>'+_e(say("All bars start at zero. Values are counts, not percentages."))+'</p>')
    if data.get("invalid_time_events"):
        parts.append('<p>'+_e(say("Observations with an unusable time: {n}", n=data["invalid_time_events"]))+'</p>')
    return ''.join(parts)+'</section>'


def examination_html(data, say):
    if not data:
        return ''
    parts = ['<section class="card" id="examination"><h2>'+_e(say(REVIEW_TITLE))+'</h2><p>'+_e(say(REVIEW_NOTE))+'</p>']
    for key, title in REVIEW_FIELDS.items():
        if value := data.get(key):
            parts.append('<div class="examination-part"><h3>'+_e(say(title))+'</h3><p class="examination-text" dir="auto">'+_e(value)+'</p></div>')
    return ''.join(parts)+'</section>'


def _rgb(value):
    return tuple(int(value[i:i+2], 16) for i in (1, 3, 5))


def pdf(lay, data):
    if not data:
        return
    say, pdf = lay.say, lay.pdf
    pdf.add_page()
    lay.section(say(TITLE), say(INTRO))
    lay.kv([(say("Source file"), data.get("source", {}).get("file", "events.jsonl")),
            ("SHA-256", data.get("source", {}).get("sha256"))])
    lay.grid([say("Counts by category"), say("Observations")], [(say(title), data["totals"].get(kind, 0)) for kind, title in KINDS.items()], (75,25))
    if chart := data.get("activity"):
        lay.heading(say("Recorded activity over time"))
        lay.text(say(TIME_NOTE), size=8)
        if chart.get("status") != "available":
            lay.text(say("This chart exceeds the grouping limit. Exact overall counts remain available."), size=9)
        elif rows := activity_bins(chart["rows"]):
            if pdf.get_y()+65 > pdf.page_break_trigger:
                pdf.add_page()
            left, top, width, height = pdf.l_margin+10, pdf.get_y()+5, pdf.epw-12, 43
            maximum = max(r["total"] for r in rows) or 1
            with pdf.local_context(draw_color=(190,197,200)):
                for frac in (0,.5,1):
                    pdf.line(left, top+height*frac, left+width, top+height*frac)
            step = width/len(rows)
            for index, row in enumerate(rows):
                y = top+height
                for kind, color in COLORS.items():
                    bar = height*row["counts"].get(kind,0)/maximum
                    y -= bar
                    if bar:
                        with pdf.local_context(fill_color=_rgb(color)):
                            pdf.rect(left+index*step, y, max(.2,step-.8), bar, style="F")
            pdf.set_y(top+height+3)
            lay.text(rows[0]["period"]+'  →  '+rows[-1]["period"]+' · UTC', size=8)
            lay.gap(3)
            lay.heading(say("Exact figures"))
            lay.grid([say("Period (UTC)"), say("New message"), say("History snapshot"), say("Recovered message"),
                      say("Edits"), say("Deletions"), say("Missing on recheck")],
                     [(r["period"], *[r["counts"].get(kind, 0) for kind in KINDS]) for r in rows],
                     (28,12,12,12,12,12,12))
        else:
            lay.text(say("No observations in this selection."),size=9)
    if chart := data.get("hourly"):
        lay.heading(say("Observation times by weekday and hour"))
        if pdf.get_y()+65 > pdf.page_break_trigger:
            pdf.add_page()
        rows = chart["rows"]
        maximum = max((v for row in rows for v in row), default=0) or 1
        left, top, step = pdf.l_margin+32, pdf.get_y()+3, (pdf.epw-32)/24
        for day, row in enumerate(rows):
            pdf.set_xy(pdf.l_margin, top+day*6)
            pdf.set_font("Sans",size=7)
            pdf.multi_cell(30,3,say(DAYS[day]),align=lay.align[0])
            for hour, value in enumerate(row):
                fraction = value/maximum
                color = tuple(round(a+(b-a)*fraction) for a,b in zip((231,240,241),(36,126,140)))
                with pdf.local_context(fill_color=color):
                    pdf.rect(left+hour*step,top+day*6,step-.5,5.4,style="F")
        for hour in range(0,24,3):
            pdf.set_xy(left+hour*step,top+44)
            pdf.set_font("Sans",size=6)
            pdf.cell(step,3,f'{hour:02d}')
        pdf.set_y(top+50)
        lay.text(say(TIME_NOTE),size=8)
        lay.heading(say("Exact figures"))
        for start in (0,12):
            lay.grid([say("Hour (UTC)"), *[f'{hour:02d}' for hour in range(start,start+12)]],
                     [(say(DAYS[day]), *row[start:start+12]) for day,row in enumerate(rows)],
                     [24]+[76/12]*12)
    for key, title in (("participants","Most observed participants"),("chats","Activity by chat")):
        if not (chart := data.get(key)):
            continue
        lay.heading(say(title))
        if key == 'participants':
            lay.text(say(PEOPLE_NOTE),size=8)
            if data.get("participant_labels") != 'ids':
                lay.text(say(PRIVACY_NOTE),size=8)
        if chart.get("status") != 'available':
            lay.text(say("This chart exceeds the grouping limit. Exact overall counts remain available."),size=9)
            continue
        rows = chart["rows"]
        maximum = max((r["total"] for r in rows),default=0) or 1
        for row in rows:
            if pdf.get_y()+15 > pdf.page_break_trigger:
                pdf.add_page()
            lay.text(label(row,say)+'  ·  '+str(row["total"]),size=8)
            y = pdf.get_y()
            with pdf.local_context(fill_color=(36,126,140)):
                pdf.rect(pdf.l_margin,y,max(.1,pdf.epw*row["total"]/maximum),2.3,style="F")
            pdf.set_y(y+5)
        if not rows:
            lay.text(say("No observations in this selection."),size=9)
    lay.text(say("All bars start at zero. Values are counts, not percentages."),size=8)
    if data.get("invalid_time_events"):
        lay.text(say("Observations with an unusable time: {n}",n=data["invalid_time_events"]),size=8)


def examination_pdf(lay, data):
    if not data:
        return
    lay.section(lay.say(REVIEW_TITLE),lay.say(REVIEW_NOTE))
    for key, title in REVIEW_FIELDS.items():
        if value := data.get(key):
            lay.heading(lay.say(title))
            lay.text(value,size=9)
