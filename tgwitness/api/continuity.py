import asyncio

from fastapi import Depends, HTTPException, Query, Request

from ..store import Store
from ..verifier.completeness import COMPLETENESS_KINDS, completeness_certificate, completeness_time


def sequence_events(store):
    rows = store.bounded_read("SELECT * FROM events WHERE kind IN (" + ",".join("?" * len(COMPLETENESS_KINDS))
                              + ") ORDER BY seq", list(COMPLETENESS_KINDS), 30)
    return [Store.decode(row) for row in rows]


def register(app, authenticate, visible_chats):
    @app.get("/api/continuity", dependencies=[Depends(authenticate)])
    async def continuity(request: Request, since: str | None = None, until: str | None = None,
                         chat_id: list[int] | None = Query(default=None), account: bool = True):
        for value in (since, until):
            if value is not None and completeness_time(value) is None:
                raise HTTPException(422, "Give times as ISO 8601 with a time zone, for example 2026-11-10T14:00:00Z.")
        visible = visible_chats(request)
        chats = chat_id or None
        if visible is not None:
            if chats is not None and any(chat not in visible for chat in chats):
                raise HTTPException(403, "This chat is not open to this access.")
            chats, account = chats or sorted(visible), False
        try:
            events = await asyncio.to_thread(sequence_events, app.state.store)
        except TimeoutError as exc:
            raise HTTPException(503, str(exc)) from None
        return completeness_certificate(events, since, until, chats, account)
