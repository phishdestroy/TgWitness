"""Expired authorization is distinct from transport failure; synthetic Telegram clients only."""
import asyncio
from pathlib import Path
import sys
import tempfile
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from telethon.errors import AuthKeyUnregisteredError, SessionRevokedError

from tgwitness.app import create_app
from tgwitness.collector import AuthorizationRequired
from tgwitness.proxy_catalog import ProxyPool
from tools.browser_fixtures import CHAT, FakeClient, saved_session
from tools.check_session_reservations import idle, pinned, probe, workspace


async def rejects(awaitable, expected):
    try:
        await awaitable
    except expected:
        return
    raise AssertionError("Expected authorization or connection failure")


async def recovery():
    async with workspace() as (app, http):
        collector, store, vault = app.state.collector, app.state.store, app.state.vault
        await collector.configure(123, "a" * 32, saved_session())
        store.set_target(CHAT, "Synthetic source", "supergroup", True)
        credentials = vault.read("credentials")
        identity = vault.public_key
        head = store.stats()["head"]
        collector.client.authorized = False
        await rejects(collector.start(), AuthorizationRequired)
        status = (await http.get("/api/status")).json()
        assert status["collector"]["has_session"] and status["collector"]["authorization_required"]
        assert status["collector"]["phase"] == "authorization_required"
        assert status["health"]["connection"]["reason"] == "signed_out"

        # A rejected replacement cannot erase a known authorization failure or rebind the journal.
        await rejects(collector.configure(124, "a" * 32, saved_session(b"y")), ValueError)
        assert collector.authorization_required and collector.phase == "authorization_required"
        assert vault.read("credentials") == credentials and vault.public_key == identity
        assert store.get_setting("account")["id"] == 44
        assert store.db.execute("SELECT hash FROM events WHERE seq=?", (head["seq"],)).fetchone()[0] == head["hash"]
        assert store.targets(True)[0]["chat_id"] == CHAT

        # An unsuccessful new sign-in and changing its route must retain the known invalid state.
        with patch.object(FakeClient, "is_user_authorized", AsyncMock(return_value=False)):
            await rejects(collector.configure(123, "a" * 32, saved_session(b"z")), ValueError)
        assert collector.authorization_required
        await collector.connect_login(123, "a" * 32)
        await collector.cancel_login()
        assert collector.authorization_required

        # A validated same-account session is the point at which the warning may clear.
        await collector.configure(123, "a" * 32, saved_session(b"z"))
        assert not collector.authorization_required and collector.last_error is None
        assert collector.phase == "ready" and vault.public_key == identity

        for error in (AuthKeyUnregisteredError(None), SessionRevokedError(None)):
            with patch.object(collector.client, "is_user_authorized", AsyncMock(side_effect=error)):
                await rejects(collector.restore(), type(error))
            assert collector.authorization_required and collector.phase == "authorization_required"
            with patch.object(collector.client, "get_me", AsyncMock(side_effect=error)):
                await rejects(collector.restore(), type(error))
            assert collector.authorization_required, "Cached authorization cleared a known rejected session"
            await collector.restore()
            assert not collector.authorization_required and collector.last_error is None

        # Authorization can be rejected by a later RPC after the initial session check.
        with patch.object(collector, "prepare_start", AsyncMock(side_effect=SessionRevokedError(None))):
            await rejects(collector.start(), SessionRevokedError)
        assert collector.authorization_required and collector.phase == "authorization_required"
        await collector.restore()
        await collector.failure(AuthKeyUnregisteredError(None), "synthetic update")
        assert collector.authorization_required
        await collector.restore()

        with patch.object(collector.client, "is_user_authorized", AsyncMock(side_effect=TimeoutError)):
            await rejects(collector.restore(), TimeoutError)
        assert not collector.authorization_required, "Transport failure was mistaken for expired credentials"
        collector.next_reconnect_at = 0
        with patch.object(collector, "restore", AsyncMock(side_effect=ValueError("Invalid route"))):
            await collector.reconnect()
        assert not collector.authorization_required and collector.phase != "authorization_required"


class ExpiredClient(FakeClient):
    async def is_user_authorized(self):
        return False


class RevokedClient(FakeClient):
    async def is_user_authorized(self):
        raise SessionRevokedError(None)


class UnreachableClient(FakeClient):
    async def connect(self):
        raise TimeoutError()


async def restart():
    with tempfile.TemporaryDirectory(prefix="account-recovery-") as scratch, \
            patch.object(ProxyPool, "run", idle), patch.object(ProxyPool, "pin", staticmethod(pinned)), \
            patch.object(ProxyPool, "probe", staticmethod(probe)):
        root = Path(scratch)
        app = create_app(root, client_factory=FakeClient)
        async with app.router.lifespan_context(app):
            await app.state.collector.configure(123, "a" * 32, saved_session())
            app.state.store.set_target(CHAT, "Synthetic source", "supergroup", True)
            app.state.store.set_setting("resume", True)
            identity = app.state.vault.public_key
        for factory, required in ((ExpiredClient, True), (RevokedClient, True), (UnreachableClient, False)):
            app = create_app(root, client_factory=factory)
            async with app.router.lifespan_context(app):
                collector = app.state.collector
                for _ in range(100):
                    if collector.phase in ("authorization_required", "resume_failed"):
                        break
                    await asyncio.sleep(0.02)
                assert collector.phase == ("authorization_required" if required else "resume_failed")
                assert collector.authorization_required == required
                assert app.state.vault.public_key == identity
                assert app.state.store.get_setting("account")["id"] == 44


async def main():
    await asyncio.wait_for(recovery(), 60)
    await asyncio.wait_for(restart(), 60)


if __name__ == "__main__":
    asyncio.run(main())
    print("Account recovery: expired/revoked authorization, transport failures, restart, same-account recovery and evidence retention PASS")
