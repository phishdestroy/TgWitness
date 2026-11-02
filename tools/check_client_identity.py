"""Inspect real MTProto initialization metadata without connecting to Telegram."""
import asyncio
from pathlib import Path
import socket
import sys
import tempfile
from unittest.mock import patch

from telethon import TelegramClient
from telethon.crypto import AuthKey
from telethon.sessions import StringSession

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tgwitness import api_pool  # noqa: E402
from tgwitness.collector import Collector  # noqa: E402
from tgwitness.security import Vault  # noqa: E402
from tgwitness.store import Store  # noqa: E402


async def main():
    imported = StringSession()
    imported.set_dc(2, "149.154.167.51", 443)
    imported.auth_key = AuthKey(b"x" * 256)
    checks = 0
    with tempfile.TemporaryDirectory(prefix="client-identity-") as temporary, \
            patch.object(socket, "getaddrinfo", side_effect=AssertionError("DNS prohibited")), \
            patch.object(socket, "create_connection", side_effect=AssertionError("Network prohibited")):
        root = Path(temporary)
        vault, store = Vault(root), Store(root)
        vault.save("network", {"kind": "direct"})
        collector = Collector(store, vault, TelegramClient)
        try:
            for api_id in (*sorted(api_pool.POOL_IDS), 123):
                for session in ("", imported.save()):
                    client = collector.make_client(api_id, "a" * 32, session)
                    try:
                        request = client._init_request
                        labels = (request.device_model, request.system_version, request.app_version)
                        assert all(isinstance(value, str) and value for value in labels)
                        assert not any("tgwitness" in value.lower() for value in labels)
                        assert request.system_version != "Python"
                        if api_id != api_pool.DESKTOP_ID:
                            assert request.app_version == TelegramClient.__version__
                        assert request.api_id == api_id
                        if session:
                            assert client.session.auth_key.key == imported.auth_key.key
                            assert client.session.dc_id == imported.dc_id
                        checks += 1
                    finally:
                        await client.disconnect()
        finally:
            store.close()
    print(f"Client identity passed: {checks} real initialization requests; new/imported authorization, no project branding, no network.")


if __name__ == "__main__":
    asyncio.run(main())
