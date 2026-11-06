import asyncio
import builtins
import json
from itertools import islice
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from telethon.tl import types

from tgwitness import chat_export, distributed_export, replica
from tgwitness.collector import Collector, absent_numbers, message_record
from tgwitness.message_numbers import MissingNumbers
from tgwitness.message_selection import Selection, SelectionIndex
from tgwitness.security import Vault
from tgwitness.store import Store
from tools.check_export_files_stage import message


@pytest.fixture
def collector(tmp_path):
    vault, store = Vault(tmp_path), Store(tmp_path)
    store.bind(vault)
    try:
        yield Collector(store, vault)
    finally:
        store.close()


@pytest.mark.parametrize("files,status", [("skip", "skipped_by_export_option"), ("hashes", "hashes_only")])
def test_recovered_attachments_and_profile_obey_export_choice(collector, tmp_path, monkeypatch, files, status):
    async def scenario():
        recovered = message(2, photo=True)
        recovered.peer_id = types.PeerChannel(42)
        collector.client = SimpleNamespace(get_messages=AsyncMock(return_value=[recovered]), download_media=AsyncMock())
        collector.telegram_clock = AsyncMock(return_value={})
        collector.chat_profile = AsyncMock(return_value=({}, {}, {}))
        collector.attachment_hashes = AsyncMock(return_value={"status": "complete", "parts": [], "size": 1000})

        async def history(entity, scratch, record, media_dir, choice):
            assert choice == files
            scratch.write_text('\n'.join(json.dumps(message_record(message(i))) for i in (3, 1)), encoding="utf-8")
            return 2

        collector.stream_history = history
        captured = {}

        def build(scratch, meta, vault, output, *args):
            captured.update(meta=meta, rows=[json.loads(line) for line in scratch.read_text(encoding="utf-8").splitlines()])
            output.write_bytes(b"synthetic bundle boundary")

        monkeypatch.setattr(chat_export, "build_bundle", build)
        monkeypatch.setattr(replica, "outbox", lambda *args: None)
        record = {"id": files, "chat_id": -1000000000042, "files": files, "captured": 2}
        await collector.run_export(types.PeerChannel(42), {}, record)
        assert record["phase"] == "done", record
        assert next(row for row in captured["rows"] if row["id"] == 2)["file_status"] == status
        assert captured["meta"]["acquisition"]["files"] == files
        assert collector.store.events(kind="chat_export.started")[0]["payload"]["attachments"] == files
        assert collector.chat_profile.call_args.kwargs["include_photo"] is False
        collector.client.download_media.assert_not_awaited()
        assert collector.attachment_hashes.await_count == (files == "hashes")

    asyncio.run(scenario())


@pytest.mark.parametrize("change", ["none", "text", "photo", "peer", "missing"])
def test_staged_files_cannot_replace_the_original_message(collector, tmp_path, change):
    async def scenario():
        original, current = message(2, photo=True), message(2, photo=True)
        if change == "text":
            current.message = "Edited after history was saved"
        elif change == "photo":
            current.media.photo.id += 100
        elif change == "peer":
            current.peer_id = types.PeerUser(8)
        collector.client = SimpleNamespace(get_messages=AsyncMock(return_value=[None if change == "missing" else current]))
        collector.export_attachment = AsyncMock(return_value={"file_status": "synthetic_saved"})
        scratch = tmp_path / "history.jsonl"
        original_record = message_record(original)
        scratch.write_text(json.dumps(original_record) + '\n', encoding="utf-8")
        await collector.export_files(types.PeerUser(7), scratch, {}, tmp_path, [2], "download")
        result = json.loads(scratch.read_text(encoding="utf-8"))
        status = ("synthetic_saved" if change == "none" else "message_unavailable_at_file_read" if change == "missing"
                  else "message_changed_or_unavailable_at_media_read")
        assert result.pop("file_status") == status
        assert result == original_record
        assert collector.export_attachment.await_count == (change == "none")

    asyncio.run(scenario())


def test_sparse_message_numbers_are_counted_without_expansion(tmp_path):
    scratch = tmp_path / "sparse.jsonl"
    scratch.write_text('{"id":1}\n{"id":2000000000}\n', encoding="utf-8")
    missing = absent_numbers(scratch)
    assert len(missing) == 1999999998
    assert list(islice(missing, 4)) == [2, 3, 4, 5]
    for step in (1, 2, 3, 8):
        small = MissingNumbers([1, 4, 5, 9, 15])
        assert list(small.sample(step)) == list(small)[::step]
    assert not MissingNumbers([]) and not MissingNumbers([1, 2])


@pytest.mark.parametrize("full", [False, True])
def test_distributed_sparse_recheck_is_bounded_and_cancellable(tmp_path, monkeypatch, full):
    async def scenario():
        chat_id = -1000000000042
        index = SelectionIndex(tmp_path / "selection.sqlite3", chat_id)
        manager = object.__new__(distributed_export.DistributedExport)
        manager.job, manager.state = {"chat_id": chat_id}, {"workers": [{"profile_id": "account", "state": "done"}]}
        manager.entities = {"account": types.PeerChannel(42)}
        asked = []

        async def read(entity, batch):
            asked.extend(batch)
            if full:
                raise asyncio.CancelledError
            return {}

        manager.app_for = lambda _: SimpleNamespace(state=SimpleNamespace(collector=SimpleNamespace(read_numbers=read)))
        # The former eager range expansion fails safely instead of exhausting test memory.
        def bounded_range(*args):
            result = builtins.range(*args)
            assert len(result) <= 10000, "Missing IDs must not be expanded before sampling"
            return result

        monkeypatch.setattr(distributed_export, "range", bounded_range, raising=False)
        try:
            for number in (1, 2000000000):
                index.add(message_record(message(number)), "account")
            index.db.commit()
            if full:
                with pytest.raises(asyncio.CancelledError):
                    await manager.recheck_absent(index, Selection(recheck_all=True))
                assert len(asked) == 100
            else:
                result = await manager.recheck_absent(index, Selection())
                assert result["absent_total"] == 1999999998
                assert result["asked"] == 1000 and len(set(asked)) == 1000
                assert result["unchecked"] == 1999998998 and result["limit_reached"]
        finally:
            index.close()

    asyncio.run(scenario())


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
