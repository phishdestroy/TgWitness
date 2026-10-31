import asyncio
import hashlib
import json

import pytest

from tgwitness import live_stream
from tgwitness.access import Refused
from test_access import HARBOR, OTHER, issue, login, panel as panel


def test_batch_targets_validates_every_chat_before_writing(panel):
    app, client = panel
    store = app.state.store
    before = store.stats()["head"]
    result = client.post("/api/targets/batch", json={"chat_ids": [HARBOR, 999], "enabled": False})
    assert result.status_code == 400
    assert store.stats()["head"] == before
    assert all(t["enabled"] for t in store.targets())
    result = client.post("/api/targets/batch", json={"chat_ids": [HARBOR, HARBOR, OTHER], "enabled": False})
    assert result.status_code == 200 and result.json()["updated"] == 2
    assert not any(t["enabled"] for t in store.targets())
    assert store.verify(app.state.vault.public_key)


def test_batch_keeps_enabled_state_when_only_priority_changes(panel):
    app, client = panel
    client.post("/api/targets", json={"chat_id": HARBOR, "enabled": False})
    result = client.post("/api/targets/batch", json={"chat_ids": [HARBOR, OTHER], "priority": False})
    assert result.status_code == 200
    states = {t["chat_id"]: t for t in app.state.store.targets()}
    assert not states[HARBOR]["enabled"] and states[OTHER]["enabled"]
    assert not any(t["priority"] for t in states.values())


def test_batch_and_media_scope_do_not_leak_other_chats(panel):
    app, client = panel
    token, _ = issue(client, permissions=["view", "sources"], workspaces={"default": [HARBOR]})
    viewer, _ = login(app, token)
    result = viewer.post("/api/targets/batch", json={"chat_ids": [HARBOR, OTHER], "enabled": False})
    assert result.status_code == 403
    result = viewer.post("/api/targets/batch", json={"chat_ids": [HARBOR], "priority": False})
    assert [t["chat_id"] for t in result.json()["targets"]] == [HARBOR]
    data = b"\x89PNG\r\n\x1a\n" + b"not an actual picture"
    digest = hashlib.sha256(data).hexdigest()
    (app.state.store.root / "media").mkdir(exist_ok=True)
    (app.state.store.root / "media" / digest).write_bytes(data)
    app.state.store.append("media.saved", {"media_sha256": digest}, OTHER, 1)
    assert viewer.get("/api/media/" + digest + "?inline=1").status_code == 404


@pytest.mark.parametrize("data,expected", [
    (b"<svg onload=alert(1)></svg>", "application/octet-stream"),
    (b"<!DOCTYPE html><script>alert(1)</script>", "application/octet-stream"),
    (b"\xff\xd8\xff\xe0saved", "image/jpeg"),
    (b"OggSsaved", "audio/ogg"),
    (b"\x00\x00\x00\x18ftypmp42saved", "video/mp4"),
])
def test_inline_media_uses_bytes_and_keeps_download(panel, data, expected):
    app, client = panel
    digest = hashlib.sha256(data).hexdigest()
    directory = app.state.store.root / "media"
    directory.mkdir(exist_ok=True)
    (directory / digest).write_bytes(data)
    result = client.get("/api/media/" + digest + "?inline=1")
    assert result.status_code == 200 and result.content == data
    assert result.headers["content-type"] == expected
    assert result.headers["x-content-type-options"] == "nosniff"
    assert "default-src 'none'" in result.headers["content-security-policy"]
    disposition = "attachment" if expected == "application/octet-stream" else "inline"
    assert result.headers["content-disposition"].startswith(disposition)
    assert client.get("/api/media/" + digest).headers["content-disposition"].startswith("attachment")


def test_stream_contains_only_committed_visible_metadata(journal):
    store, _ = journal
    visible = store.append("message.new", {"text": "private payload"}, HARBOR, 1)
    store.append("message.new", {"text": "other secret"}, OTHER, 1)
    with pytest.raises(RuntimeError), store.transaction():
        store.append("message.new", {"text": "rolled back"}, HARBOR, 2)
        raise RuntimeError()
    records = live_stream.notifications(store, 0, {HARBOR})
    assert [r["seq"] for r in records] == [visible["seq"]]
    assert set(records[0]) == {"seq", "kind", "chat_id", "message_id", "observed_at"}
    assert live_stream.notifications(store, visible["seq"], {HARBOR}) == []


def test_stream_revocation_stops_and_slow_client_has_no_queue(journal):
    store, _ = journal
    for i in range(105):
        store.append("message.new", {"text": str(i)}, HARBOR, i)

    async def run():
        revoked = False

        def authorize():
            if revoked:
                raise Refused("revoked")
            return {HARBOR}

        async def disconnected():
            return False

        updates = live_stream.stream(store, 0, authorize, disconnected, interval=0)
        first = await anext(updates)
        assert len(json.loads(first.split("data: ")[1])) == 100
        second = await anext(updates)
        assert len(json.loads(second.split("data: ")[1])) == 5
        revoked = True
        with pytest.raises(Refused):
            await anext(updates)
        await updates.aclose()

    asyncio.run(run())
