import json

from .health import SLACK_SECONDS, age, now_utc

SCAN = 400


def validated_stamp(store):
    with store.reading() as db:
        rows = db.execute("SELECT observed_at,payload FROM events WHERE kind='anchor.completed' ORDER BY seq DESC LIMIT ?",
                          (SCAN,)).fetchall()
    through, at = 0, None
    for observed_at, raw in rows:
        try:
            payload = json.loads(raw) if isinstance(raw, (str, bytes)) else raw
            count = payload["checkpoint"]["event_count"]
        except (ValueError, KeyError, TypeError):
            continue
        if type(count) is not int:
            continue
        if any(r.get("ok") is True and r.get("kind") == "rfc3161" for r in payload.get("results") or []):
            if at is None:
                at = observed_at
            through = max(through, count)
    return through, at


def assess(store, settings, now=None):
    head = store.stats()["head"]
    total = head["seq"] if head else 0
    through, at = validated_stamp(store)
    through = min(through, total)
    stale = at is None or (age(at, now or now_utc()) or 0) > 2 * settings["interval_minutes"] * 60 + SLACK_SECONDS
    if not total:
        missing = ["empty"]
    elif not settings["enabled"]:
        missing = ["disabled"]
    elif not settings["tsa_urls"]:
        missing = ["no_authority"]
    elif not through:
        missing = ["none"]
    elif stale:
        missing = ["stale"]
    else:
        missing = []
    return {"ready": not missing, "missing": missing, "records": total, "stamped_through": through,
            "stamped_at": at if through else None}
