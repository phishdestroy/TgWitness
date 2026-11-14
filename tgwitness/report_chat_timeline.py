from datetime import date, datetime, timedelta, timezone
from html import escape

from .case_assessment import number_text

MAX_CHATS = 5000
DAY_LIMIT = 120
WEEK_LIMIT = 104
TITLE = "Chats over time"
NOTE = ("Each row is a chat and each column a period (UTC); darker cells hold more observed messages. Hatched columns "
        "had no capture confirmation at all: what was posted then is unknown. A pale cell in an observed column means "
        "no message was recorded there.")
COLOR = "#247e8c"


def text_keys():
    return [TITLE, NOTE, "Not observed", "Chat", "Observations", "First observed", "Last observed", "Chat {id}"]


class ChatDays:
    def __init__(self):
        self.chats, self.dropped = {}, 0

    def add(self, chat, day):
        if chat is None:
            return
        days = self.chats.get(chat)
        if days is None:
            if len(self.chats) >= MAX_CHATS:
                self.dropped += 1
                return
            days = self.chats[chat] = {}
        key = day.isoformat()
        days[key] = days.get(key, 0) + 1

    def result(self):
        return {"chats": [[chat, dict(days)] for chat, days in self.chats.items()], "dropped": self.dropped}


def bins_for(first, last):
    span = (last - first).days + 1
    if span <= DAY_LIMIT:
        return "day", [(first + timedelta(days=i), first + timedelta(days=i + 1)) for i in range(span)]
    if span <= WEEK_LIMIT * 7:
        start = first - timedelta(days=first.weekday())
        weeks = (last - start).days // 7 + 1
        return "week", [(start + timedelta(weeks=i), start + timedelta(weeks=i + 1)) for i in range(weeks)]
    found, cursor = [], date(first.year, first.month, 1)
    while cursor <= last:
        following = date(cursor.year + cursor.month // 12, cursor.month % 12 + 1, 1)
        found.append((cursor, following))
        cursor = following
    return "month", found


def label_of(start, granularity):
    return start.strftime("%Y-%m") if granularity == "month" else start.isoformat()


def timeline(raw, limit):
    rows = [(chat, days) for chat, days in (raw or {}).get("chats", []) if days]
    if len(rows) < 2:
        return None
    every = [date.fromisoformat(day) for _, days in rows for day in days]
    granularity, bins = bins_for(min(every), max(every))
    starts = [start for start, _ in bins]
    ranked = sorted(rows, key=lambda item: (-sum(item[1].values()), str(item[0])))
    output = []
    for chat, days in ranked[:limit]:
        cells = [0] * len(bins)
        for day, count in days.items():
            moment, index = date.fromisoformat(day), 0
            low, high = 0, len(starts) - 1
            while low <= high:
                middle = (low + high) // 2
                if starts[middle] <= moment:
                    index, low = middle, middle + 1
                else:
                    high = middle - 1
            cells[index] += count
        active = [i for i, count in enumerate(cells) if count]
        output.append({"id": chat, "label": "Chat {id}", "label_values": {"id": str(chat)}, "total": sum(cells),
                       "first": label_of(bins[active[0]][0], granularity), "last": label_of(bins[active[-1]][0], granularity),
                       "cells": cells})
    return {"status": "available", "granularity": granularity, "timezone": "UTC",
            "bins": [{"from": start.isoformat(), "to": end.isoformat(), "label": label_of(start, granularity)} for start, end in bins],
            "rows": output, "other_chats": max(0, len(rows) - limit), "untracked_chats": (raw or {}).get("dropped", 0)}


def moment(value):
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.astimezone(timezone.utc) if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def titled(chart, titles):
    for row in (chart or {}).get("rows") or []:
        title = (titles or {}).get(row["id"]) or (titles or {}).get(str(row["id"]))
        if title:
            row["title"] = str(title)
    return chart


def observed(chart, coverage):
    periods = [(moment(p.get("from")), moment(p.get("to"))) for p in (coverage or {}).get("continuous") or []]
    periods = [(start, end) for start, end in periods if start and end]
    if not coverage or not chart:
        return None
    flags = []
    for item in chart["bins"]:
        start = datetime.fromisoformat(item["from"]).replace(tzinfo=timezone.utc)
        end = datetime.fromisoformat(item["to"]).replace(tzinfo=timezone.utc)
        flags.append(any(low < end and high > start for low, high in periods))
    return flags


def chat_name(row, say):
    return row.get("title") or say(row["label"], **row["label_values"])


def chat_label(row, say):
    return row["title"] + " · " + str(row["id"]) if row.get("title") else chat_name(row, say)


def svg(chart, say, flags):
    bins, rows = chart["bins"], chart["rows"]
    left, width, cell_h = 210, 540, 18
    step = width / len(bins)
    height = 24 + cell_h * len(rows) + 18
    maximum = max((value for row in rows for value in row["cells"]), default=0) or 1
    parts = ['<div class="scroll"><svg viewBox="0 0 760 ' + str(height) + '" style="min-width:640px" role="img" aria-label="'
             + escape(say(TITLE)) + '">'
             '<defs><pattern id="chat-timeline-gap" width="6" height="6" patternUnits="userSpaceOnUse" '
             'patternTransform="rotate(45)"><rect width="6" height="6" fill="#8894a41f"/>'
             '<line x1="0" y1="0" x2="0" y2="6" stroke="#8894a4" stroke-width="2"/></pattern></defs>']
    for index, flag in enumerate(flags or []):
        if not flag:
            parts.append('<rect x="%.2f" y="24" width="%.2f" height="%d" fill="url(#chat-timeline-gap)"><title>%s</title></rect>'
                         % (left + index * step, step, cell_h * len(rows), escape(bins[index]["label"] + " · " + say("Not observed"))))
    for number, row in enumerate(rows):
        y = 24 + number * cell_h
        name = chat_name(row, say)
        parts.append('<text class="analytics-svg-label" x="%d" y="%d" text-anchor="end">%s</text>'
                     % (left - 8, y + 13, escape(name if len(name) <= 24 else name[:23] + "…")))
        for index, value in enumerate(row["cells"]):
            if value:
                parts.append('<rect x="%.2f" y="%d" width="%.2f" height="%d" fill="%s" fill-opacity="%.3f"><title>%s</title></rect>'
                             % (left + index * step, y + 1, max(step - 1, .6), cell_h - 2, COLOR, .15 + .85 * value / maximum,
                                escape(chat_label(row, say) + " · " + bins[index]["label"] + " · " + number_text(value, say))))
    parts.append('<text class="analytics-axis" x="%d" y="16">%s</text>' % (left, escape(bins[0]["label"])))
    parts.append('<text class="analytics-axis" x="750" y="16" text-anchor="end">%s</text>' % escape(bins[-1]["label"]))
    parts.append('<text class="analytics-axis" x="750" y="%d" text-anchor="end">UTC</text></svg></div>' % (height - 4))
    return "".join(parts)


def html(chart, say, table):
    if not chart or not chart.get("rows"):
        return ""
    flags = chart.get("observed")
    rows = [(chat_label(row, say), number_text(row["total"], say), row["first"], row["last"]) for row in chart["rows"]]
    return ('<figure class="analytics-figure chart-card chart-timeline"><figcaption>' + escape(say(TITLE)) + "</figcaption><p>"
            + escape(say(NOTE)) + "</p>" + svg(chart, say, flags)
            + table([say("Chat"), say("Observations"), say("First observed"), say("Last observed")], rows, say) + "</figure>")


def pdf(lay, chart):
    if not chart or not chart.get("rows"):
        return
    say, pdf_file = lay.say, lay.pdf
    bins, rows, flags = chart["bins"], chart["rows"], chart.get("observed") or []
    lay.heading(say(TITLE))
    lay.text(say(NOTE), size=8)
    height = 5 * len(rows)
    if pdf_file.get_y() + height + 20 > pdf_file.page_break_trigger:
        pdf_file.add_page()
    left, top = pdf_file.l_margin + 40, pdf_file.get_y() + 3
    width = pdf_file.epw - 40
    step = width / len(bins)
    maximum = max((value for row in rows for value in row["cells"]), default=0) or 1
    for index, flag in enumerate(flags):
        if not flag:
            with pdf_file.local_context(fill_color=(226, 229, 234)):
                pdf_file.rect(left + index * step, top, step, height, style="F")
    red, green, blue = (int(COLOR[i:i + 2], 16) for i in (1, 3, 5))
    for number, row in enumerate(rows):
        y = top + number * 5
        pdf_file.set_xy(pdf_file.l_margin, y)
        pdf_file.set_font("Sans", size=6.5)
        name = chat_name(row, say)
        pdf_file.cell(38, 4.5, name if len(name) <= 28 else name[:27] + "…", align="R")
        for index, value in enumerate(row["cells"]):
            if value:
                share = .15 + .85 * value / maximum
                fill = tuple(round(255 - (255 - channel) * share) for channel in (red, green, blue))
                with pdf_file.local_context(fill_color=fill):
                    pdf_file.rect(left + index * step, y + .3, max(step - .2, .2), 4.4, style="F")
    pdf_file.set_y(top + height + 2)
    lay.text(bins[0]["label"] + "  →  " + bins[-1]["label"] + " · UTC", size=8)
    lay.grid([say("Chat"), say("Observations"), say("First observed"), say("Last observed")],
             [(chat_label(row, say), number_text(row["total"], say), row["first"], row["last"]) for row in rows], (40, 20, 20, 20))
