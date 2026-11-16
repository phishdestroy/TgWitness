from types import SimpleNamespace

from fastapi import Depends, HTTPException, Request

from ..history_forward import ForwardPlan, ForwardStart
from .access import bearer
from .dependencies import current_context


def authority(ctx, request, credential, source):
    if not request.state.principal.admin:
        raise HTTPException(403, 'Only the main administrator can do this.')
    return ctx.action_authority(request, credential, SimpleNamespace(action='send', chat_id=source))


async def current(request: Request, *, ctx=Depends(current_context)):
    authority(ctx, request, await bearer(request), 0)()
    return ctx.app.state.history_forward.status()


async def plan(request: Request, body: ForwardPlan, *, ctx=Depends(current_context)):
    authority(ctx, request, await bearer(request), body.source)()
    return await ctx.operation(ctx.app.state.history_forward.plan, body)


async def start(request: Request, body: ForwardStart, *, ctx=Depends(current_context)):
    authorized = authority(ctx, request, await bearer(request), 0)
    return await ctx.operation(ctx.app.state.history_forward.start, body, authorized)


async def control(request: Request, job_id: str, action: str, *, ctx=Depends(current_context)):
    ctx.require_live()
    service = ctx.app.state.history_forward
    authorized = authority(ctx, request, await bearer(request), (service.job or {}).get('source', 0))
    try:
        return await service.control(job_id, action, authorized)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from None
