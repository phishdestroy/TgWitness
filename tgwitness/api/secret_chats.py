from .. import netclient
from .. import secret_chats as secret
from .. import secret_module
from ..network import NetworkConfig, NoRoute
from .dependencies import current_context
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import Request
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class SecretChatSettings(BaseModel):
    enabled: bool
    accept_incoming: bool = False


MODULE_INSTALLED_MEANING = ("The pseudo-secret protocol module was downloaded from GitHub, matched the SHA-256 fixed "
                            "in this release and was loaded. route: how the download left this computer; direct_once "
                            "means the administrator allowed this one download without the workspace's proxy.")


class SecretModuleInstall(BaseModel):
    model_config = ConfigDict(extra="forbid")
    direct_once: bool = False


class SecretChatCreate(BaseModel):
    user: str = Field(min_length=1, max_length=64, pattern=r"^(@?[A-Za-z][A-Za-z0-9_]{3,31}|[0-9]{1,20})$")


class SecretChatText(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    text: str = Field(min_length=1, max_length=4096)


def chats_of(ctx):
    return secret.of(ctx.app.state.collector)


async def connected(ctx, call, *args, **kwargs):
    collector = ctx.app.state.collector
    if not secret.available():
        raise HTTPException(400, secret.UNAVAILABLE)
    if chats_of(ctx).manager is None:
        await collector.restore()
    try:
        return await call(*args, **kwargs)
    except secret.library.ChatClosed:
        raise HTTPException(409, "This chat has ended. Nothing more can be sent to it.")
    except secret.library.ChatNotReady:
        raise HTTPException(409, "The other side has not accepted this chat yet.")


async def view(*, before: int | None = Query(default=None, ge=1, le=2**63 - 1),
               after: int | None = Query(default=None, ge=0, le=2**63 - 1), ctx=Depends(current_context)):
    if before is not None and after is not None:
        raise HTTPException(422, "Choose an older or newer history page, not both.")
    return chats_of(ctx).view(before=before, after=after)


async def update_settings(body: SecretChatSettings, *, ctx=Depends(current_context)):
    ctx.require_live()
    if body.enabled and not secret.available():
        raise HTTPException(400, secret.UNAVAILABLE)
    store, collector = ctx.app.state.store, ctx.app.state.collector
    with store.transaction():
        store.set_setting(secret.SETTING, body.model_dump())
        store.append("secret_chat.settings", body.model_dump())
    if body.enabled and (collector.vault.read("credentials") or {}).get("session"):
        try:
            await ctx.operation(collector.restore)
        except HTTPException as exc:
            chats_of(ctx).error = str(exc.detail)
    elif body.enabled:
        chats_of(ctx).error = None
    else:
        await chats_of(ctx).detach()
        collector.close_when_idle()
    return chats_of(ctx).view()


async def install(request: Request, body: SecretModuleInstall | None = None, *, ctx=Depends(current_context)):
    ctx.require_live()
    if not request.state.principal.admin:
        raise HTTPException(403, "Only the main administrator can install the pseudo-secret module.")
    collector = ctx.app.state.collector
    direct = bool(body and body.direct_once)
    route = NetworkConfig(kind="direct") if direct else collector.outside_route()
    try:
        if isinstance(route, NoRoute):
            raise route.error
        installed = not secret.available()
        await secret_module.install(route)
        if installed:
            collector.store.append("secret_chat.module_installed", {
                **{key: secret_module.INFO[key] for key in ("name", "version", "commit", "sha256", "source")},
                "route": "direct_once" if direct else route.kind, "meaning": MODULE_INSTALLED_MEANING})
    except netclient.RouteError as exc:
        raise HTTPException(409, str(exc))
    except secret_module.Refused as exc:
        raise HTTPException(502, str(exc))
    except (ValueError, OSError, EOFError):
        raise HTTPException(502, "The pseudo-secret module could not be downloaded from GitHub through this "
                                 "workspace's connection route. Check the connection and try again.")
    return chats_of(ctx).view()


async def create(body: SecretChatCreate, *, ctx=Depends(current_context)):
    ctx.require_live()
    user = int(body.user) if body.user.isdigit() else body.user.removeprefix("@")
    return await ctx.operation(connected, ctx, chats_of(ctx).create, user)


async def accept(chat_id: int, *, ctx=Depends(current_context)):
    ctx.require_live()
    return await ctx.operation(connected, ctx, chats_of(ctx).accept, chat_id)


async def send(chat_id: int, body: SecretChatText, *, ctx=Depends(current_context)):
    ctx.require_live()
    return {"random_id": str(await ctx.operation(connected, ctx, chats_of(ctx).send, chat_id, body.text))}


async def close(chat_id: int, *, ctx=Depends(current_context)):
    ctx.require_live()
    await ctx.operation(connected, ctx, chats_of(ctx).close, chat_id)
    return chats_of(ctx).view()
