from datetime import datetime, timezone
import statistics

KINDS = ("message.new", "message.snapshot", "message.recovered")
PAUSE_HOURS = 6
REPLY_WINDOW = 24 * 3600
LIMIT = 20000
MEANING = "Counted from the messages of this chat saved in this workspace, in UTC."


def moment(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def first_record(db, chat, message_id):
    return db.execute("SELECT json_extract(payload,'$.sender_id'), coalesce(json_extract(payload,'$.sent_at'), source_at) "
                      "FROM events WHERE chat_id=? AND message_id=? AND kind IN (?,?,?) ORDER BY seq LIMIT 1",
                      (chat, message_id, *KINDS)).fetchone() or (None, None)


def person_rhythm(store, chat, user_id, limit=LIMIT):
    heat = [[0] * 24 for _ in range(7)]
    night = started = longest = run = 0
    replies, days = [], set()
    with store.reading() as db:
        rows = db.execute("SELECT message_id, min(coalesce(json_extract(payload,'$.sent_at'), source_at)), "
                          "max(json_extract(payload,'$.reply_to_message_id')) FROM events "
                          "WHERE json_extract(payload,'$.sender_id')=? AND chat_id=? AND kind IN (?,?,?) "
                          "GROUP BY message_id ORDER BY message_id DESC LIMIT ?",
                          (user_id, chat, *KINDS, limit + 1)).fetchall()
        limited = len(rows) > limit
        rows = rows[:limit][::-1]
        own = {row[0] for row in rows}
        for message_id, sent, reply in rows:
            when = moment(sent)
            if when:
                when = when.astimezone(timezone.utc)
                heat[when.weekday()][when.hour] += 1
                night += when.hour < 6
                days.add(when.date())
            before = db.execute("SELECT message_id FROM message_state_index WHERE chat_id=? AND message_id<? "
                                "AND has_message=1 ORDER BY message_id DESC LIMIT 1", (chat, message_id)).fetchone()
            if before and before[0] in own:
                run += 1
            else:
                run = 1
                if before:
                    previous = moment(first_record(db, chat, before[0])[1])
                    if when and previous and (when - previous).total_seconds() >= PAUSE_HOURS * 3600:
                        started += 1
            longest = max(longest, run)
            if isinstance(reply, int):
                sender, target = first_record(db, chat, reply)
                target = moment(target)
                if when and target and sender is not None and sender != user_id:
                    delay = (when - target).total_seconds()
                    if 0 <= delay <= REPLY_WINDOW:
                        replies.append(delay)
    count = len(rows)
    return {"meaning": MEANING, "timezone": "UTC", "messages": count, "limited": limited, "limit": limit,
            "active_days": len(days), "heatmap": heat, "night_share": round(night / count, 4) if count else None,
            "pause_hours": PAUSE_HOURS, "started_after_pause": started, "longest_run": longest,
            "replies_timed": len(replies), "median_reply_seconds": statistics.median(replies) if replies else None}
