"""Bounded, committed journal notifications. No payloads or signing material leave this path."""
import asyncio
import json
import time


def notifications(store, after, allowed, limit=100):
    where, args = ["seq > ?"], [after]
    if allowed is not None:
        if not allowed:
            return []
        where.append("chat_id IN (" + ",".join("?" * len(allowed)) + ")")
        args.extend(sorted(allowed))
    with store.lock:
        rows = store.db.execute(
            "SELECT seq,kind,chat_id,message_id,observed_at FROM events WHERE "
            + " AND ".join(where) + " ORDER BY seq LIMIT ?", (*args, limit)).fetchall()
        return [dict(row) for row in rows]


async def stream(store, after, authorize, disconnected, *, interval=1, lifetime=45):
    cursor = after
    deadline = time.monotonic() + lifetime
    while time.monotonic() < deadline and not await disconnected():
        allowed = authorize()  # Recheck revocation and current chat scope for every batch.
        records = await asyncio.to_thread(notifications, store, cursor, allowed)
        if allowed != authorize():
            await asyncio.sleep(0.05)
            continue
        if records:
            cursor = records[-1]["seq"]
            yield "id: " + str(cursor) + "\nevent: journal\ndata: " + json.dumps(records, separators=(",", ":")) + "\n\n"
        else:
            yield ": keep-alive\n\n"
        # A bounded batch, no unbounded per-browser queue even if the client is slow.
        await asyncio.sleep(interval if len(records) < 100 else 0.05)
