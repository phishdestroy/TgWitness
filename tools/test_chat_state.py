"""Chat-state snapshots: what Telegram returned, differences from the previous snapshot, unknown parts."""
import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest
from telethon.errors import FloodWaitError
from telethon.tl import functions, types

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tgwitness import chat_state, tuning  # noqa: E402
from tgwitness.evidence import export_file  # noqa: E402
from tgwitness.security import Vault  # noqa: E402
from tgwitness.store import Store  # noqa: E402
from tgwitness.verify import fingerprint, verify_bundle  # noqa: E402

CHANNEL = -1001000000001
ADMIN = {"user_id": 7, "role": "admin", "rights": ["delete_messages"], "rank": None}
BASE = {"title": "Synthetic", "about": "First", "participants_count": 10, "pinned": [5, 9], "admins": [ADMIN],
        "gifts": [{"key": "1", "gift_id": 4, "unique": False, "unsaved": False, "refunded": False}]}


def test_differences_name_what_changed_and_skip_unknown_parts():
    after = {**BASE, "about": "Second", "pinned": [9, 12], "admins": [{**ADMIN, "rights": []}, {**ADMIN, "user_id": 8}],
             "gifts": [{**BASE["gifts"][0], "unique": True}]}
    changes = chat_state.differences(BASE, after)
    assert changes["about"] == {"before": "First", "after": "Second"}
    assert changes["pinned"] == {"added": [12], "removed": [5]}
    assert [a["user_id"] for a in changes["admins"]["added"]] == [8] and changes["admins"]["changed"][0]["after"]["rights"] == []
    assert changes["gifts"]["changed"][0]["after"]["unique"], "An upgrade shows as a changed gift"
    unknown = {k: v for k, v in BASE.items() if k not in ("pinned", "participants_count")}
    assert chat_state.differences(BASE, unknown) == {}, "A part that was not read is not reported as removed"


@pytest.fixture
def store(tmp_path):
    vault, store = Vault(tmp_path), Store(tmp_path)
    store.bind(vault)
    store.set_target(CHANNEL, "Synthetic", "channel", True)
    yield store
    store.close()


def test_records_keep_full_states_and_compact_count_changes(store):
    first = chat_state.record(store, CHANNEL, BASE, {})
    assert first["payload"]["state"] == BASE and first["payload"]["previous_seq"] is None
    counted = chat_state.record(store, CHANNEL, {**BASE, "participants_count": 11}, {})
    assert "state" not in counted["payload"] and counted["payload"]["state_seq"] == first["seq"]
    assert counted["payload"]["changes"] == {"participants_count": {"before": 10, "after": 11}}
    _, reconstructed, base = chat_state.latest(store, CHANNEL)
    assert reconstructed["participants_count"] == 11 and base == first["seq"]
    assert chat_state.record(store, CHANNEL, {**BASE, "participants_count": 11}, {}, unchanged=False) is None
    unchanged = chat_state.record(store, CHANNEL, {**BASE, "participants_count": 11}, {})
    assert unchanged["payload"]["changes"] == {} and unchanged["payload"]["state_seq"] == first["seq"]
    unpinned = chat_state.record(store, CHANNEL, {**BASE, "participants_count": 11, "pinned": []}, {})
    assert unpinned["payload"]["state"]["pinned"] == [] and unpinned["payload"]["changes"]["pinned"]["removed"] == [5, 9]
    failed = chat_state.record(store, CHANNEL, {k: v for k, v in BASE.items() if k != "admins"} | {"pinned": [],
                               "participants_count": 11}, {"admins": "ChatAdminRequiredError"})
    assert failed["payload"]["carried_forward"] == ["admins"] and "admins" not in failed["payload"]["changes"]
    later = datetime.now(timezone.utc) + timedelta(days=8)
    weekly = chat_state.record(store, CHANNEL, {**BASE, "participants_count": 12, "pinned": []}, {}, now=later)
    assert "state" in weekly["payload"], "A full state is kept at least weekly"


class Unique(types.StarGiftUnique):
    def __init__(self, ident, slug):
        self.id, self.slug = ident, slug


class Client:
    def __init__(self, flood=False):
        self.flood, self.requests = flood, []

    async def __call__(self, request):
        self.requests.append(type(request).__name__)
        if self.flood:
            raise FloodWaitError(request=None, capture=30)
        if isinstance(request, functions.channels.GetFullChannelRequest):
            return SimpleNamespace(full_chat=SimpleNamespace(about="About", participants_count=42, admins_count=2,
                                                             slowmode_seconds=0, linked_chat_id=None))
        if isinstance(request, functions.channels.GetParticipantsRequest):
            rights = types.ChatAdminRights(delete_messages=True, pin_messages=True)
            return SimpleNamespace(participants=[
                types.ChannelParticipantAdmin(user_id=7, promoted_by=1, date=datetime(2026, 1, 1, tzinfo=timezone.utc),
                                              admin_rights=rights, rank="Mod"),
                types.ChannelParticipantCreator(user_id=1, admin_rights=types.ChatAdminRights(), rank=None)])
        if isinstance(request, functions.payments.GetSavedStarGiftsRequest):
            return SimpleNamespace(count=1, gifts=[SimpleNamespace(gift=Unique(77, "gift-77"), saved_id=3, unsaved=True,
                                                                   refunded=False, date=None, from_id=None)])
        raise AssertionError(type(request).__name__)

    async def get_messages(self, entity, limit, filter):
        assert isinstance(filter, types.InputMessagesFilterPinned)
        found = [SimpleNamespace(id=9), SimpleNamespace(id=5)]
        return type("Found", (list,), {"total": 2})(found)


def channel():
    return types.Channel(id=1000000001, title="Synthetic channel", photo=types.ChatPhotoEmpty(),
                         date=datetime(2026, 1, 1, tzinfo=timezone.utc), username="synthetic", broadcast=True)


def test_read_state_collects_parts_and_names_failures():
    options = {"chat_state_pinned": True, "chat_state_admins": True, "chat_state_gifts": True}
    state, errors = asyncio.run(chat_state.read_state(Client(), channel(), options))
    assert errors == {} and state["about"] == "About" and state["participants_count"] == 42
    assert state["pinned"] == [5, 9] and state["usernames"] == ["synthetic"]
    assert [(a["user_id"], a["role"]) for a in state["admins"]] == [(1, "creator"), (7, "admin")]
    assert state["admins"][1]["rights"] == ["delete_messages", "pin_messages"] and state["admins"][1]["rank"] == "Mod"
    assert state["gifts"] == [{"key": "3", "gift_id": 77, "unique": True, "slug": "gift-77", "unsaved": True,
                               "refunded": False, "date": None, "from_id": None}]
    quiet, _ = asyncio.run(chat_state.read_state(Client(), channel(), {key: False for key in options}))
    assert not {"pinned", "admins", "gifts"} & set(quiet)


def test_due_sources_are_snapshotted_and_floods_back_off(store):
    assert chat_state.due(store, 60) == [CHANNEL]
    saved = {"chat_state_minutes": 60, "chat_state_pause_seconds": 1, "chat_state_pinned": True,
             "chat_state_admins": False, "chat_state_gifts": False, "chat_state_unchanged": True}

    def collector(client):
        async def lookup(_chat):
            return channel()
        return SimpleNamespace(store=store, running=True, client=client, param=saved.__getitem__,
                               dialog_cache={}, lookup_entity=lookup)
    slept = []

    async def nap(seconds):
        slept.append(seconds)
    real = asyncio.sleep
    asyncio.sleep = nap
    try:
        assert asyncio.run(chat_state.run_due(collector(Client(flood=True)), {})) == 0
        assert store.get_setting("rpc_backoff_until", 0) > 0
        store.set_setting("rpc_backoff_until", 0)
        assert asyncio.run(chat_state.run_due(collector(Client()), {})) == 1
    finally:
        asyncio.sleep = real
    assert chat_state.due(store, 60) == [], "A fresh snapshot is not repeated within the interval"
    assert store.events(kind="telegram.backoff", limit=1)
    groups = {group["id"]: group for group in tuning.described(store)["groups"]}
    assert {item["key"] for item in groups["chatstate"]["items"]} == set(saved)


def test_snapshots_stay_in_verifiable_exports(tmp_path):
    vault, store = Vault(tmp_path), Store(tmp_path)
    store.bind(vault)
    try:
        chat_state.record(store, CHANNEL, BASE, {})
        chat_state.record(store, CHANNEL, {**BASE, "pinned": []}, {})
        archive = export_file(store, vault, "zip")
        try:
            assert verify_bundle(archive, expected_fingerprint=fingerprint(vault.public_key))["events"] == 2
        finally:
            archive.unlink(missing_ok=True)
    finally:
        store.close()


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
