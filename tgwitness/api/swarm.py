import asyncio
from typing import Literal

from fastapi import Depends, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel, Field

from ..swarm.dashboard import SWARM
from .dependencies import current_context

ADMIN_ONLY = "Only the main administrator can view every account at work."


class SwarmExportStart(BaseModel):
    peers: str = Field(min_length=1, max_length=100000)
    accounts: list[str] | None = Field(default=None, max_length=1000)
    files: Literal["download", "hashes", "skip"] | None = None
    priority: int = Field(default=2, ge=0, le=3)


class SwarmTaskAction(BaseModel):
    action: Literal["cancel", "priority", "reassign", "retry"]
    priority: int | None = Field(default=None, ge=0, le=3)
    account: str | None = Field(default=None, max_length=64)


class SwarmBulk(BaseModel):
    action: Literal["start", "stop", "route", "verify"]
    profiles: list[str] = Field(min_length=1, max_length=1000)


def admin(request):
    if not request.state.principal.admin:
        raise HTTPException(403, ADMIN_ONLY)


def manager(ctx):
    exports = getattr(ctx.app.state, "swarm_exports", None)
    if exports is None:
        raise HTTPException(404, "Swarm export runs in the main workspace.")
    return exports


def no_store(value):
    return JSONResponse(value, headers={"Cache-Control": "no-store"})


async def swarm(request: Request, *, ctx=Depends(current_context)):
    admin(request)
    return no_store(SWARM.snapshot(ctx.app.state, ctx.profile_id))


async def swarm_exports(request: Request, *, ctx=Depends(current_context)):
    admin(request)
    return no_store(manager(ctx).public())


async def swarm_export_start(request: Request, body: SwarmExportStart, *, ctx=Depends(current_context)):
    admin(request)
    try:
        return no_store(manager(ctx).start(body.peers, accounts=body.accounts, files=body.files,
                                           priority=body.priority, owner=request.state.principal.owner))
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from None


async def swarm_task(request: Request, task_id: str, body: SwarmTaskAction, *, ctx=Depends(current_context)):
    admin(request)
    try:
        return no_store(manager(ctx).control(task_id, body.action, priority=body.priority, account=body.account))
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from None


async def swarm_export_forget(request: Request, job_id: str, *, ctx=Depends(current_context)):
    admin(request)
    try:
        manager(ctx).forget(job_id)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from None
    return no_store(manager(ctx).public())


async def swarm_export_download(request: Request, job_id: str, task_id: str, *, ctx=Depends(current_context)):
    admin(request)
    try:
        path, filename = await asyncio.to_thread(manager(ctx).download, job_id, task_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from None
    return FileResponse(path, filename=filename, media_type="application/zip", headers={"Cache-Control": "no-store"})


def bulk(ctx):
    actions = getattr(ctx.app.state, "swarm_bulk", None)
    if actions is None:
        raise HTTPException(404, "Swarm export runs in the main workspace.")
    return actions


async def swarm_bulk_start(request: Request, body: SwarmBulk, *, ctx=Depends(current_context)):
    admin(request)
    try:
        return no_store(bulk(ctx).begin(body.action, body.profiles, owner=request.state.principal.owner))
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from None


async def swarm_bulk_status(request: Request, job_id: str, *, ctx=Depends(current_context)):
    admin(request)
    try:
        return no_store(bulk(ctx).get(job_id, owner=request.state.principal.owner))
    except KeyError:
        raise HTTPException(404, "This task is no longer in the queue.") from None


async def swarm_bulk_export(request: Request, profiles: str, language: str | None = None, *,
                            ctx=Depends(current_context)):
    from ..group_export import SELECTION, export_members
    admin(request)
    chosen = list(dict.fromkeys(p for p in profiles.split(",") if p))
    if not chosen or len(chosen) > 1000:
        raise HTTPException(400, "Choose at least one account workspace.")
    if getattr(ctx.app.state, "profiles", None) is None or any(p not in ctx.app.state.profiles.entries for p in chosen):
        raise HTTPException(400, "Unknown account workspace.")
    return await export_members(ctx.app, request, chosen, SELECTION, language)


async def metrics(request: Request, *, ctx=Depends(current_context)):
    from ..obs.metrics import CONTENT_TYPE, collect
    admin(request)
    text = await asyncio.to_thread(collect, ctx.app.state, ctx.profile_id)
    return Response(text, media_type=CONTENT_TYPE, headers={"Cache-Control": "no-store"})


async def trace(request: Request, *, ctx=Depends(current_context)):
    from ..obs.trace import TRACER
    admin(request)
    return JSONResponse(TRACER.public(ctx.profile_id), headers={"Cache-Control": "no-store"})


async def flight_record(request: Request, *, ctx=Depends(current_context)):
    from ..obs.flight_recorder import RECORDER
    admin(request)
    return Response("".join(RECORDER.lines()), media_type="application/x-ndjson",
                    headers={"Cache-Control": "no-store",
                             "Content-Disposition": 'attachment; filename="tgwitness-flight.jsonl"'})
