"""Group screen API: members with account, route and latest message; chats several members see, with coverage."""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from check_browser import RunningApp
from test_group_settings import session
from tgwitness import group_overview

CHANNEL = -1001234567890


def test_overview(tmp_path):
    with RunningApp(tmp_path) as server:
        call = session(server)
        registry = server.app.state.profiles
        gid = call("POST", "profile-groups", {"label": "Harbor case"})["groups"][0]["id"]
        alpha = call("POST", "profiles", {"label": "Alpha", "group": gid})["id"]
        beta = call("POST", "profiles", {"label": "Beta", "group": gid})["id"]
        lone = call("POST", "profiles", {"label": "Lone", "group": gid})["id"]
        call("POST", "profiles", {"label": "Outsider"})
        store = {pid: registry.entries[pid]["app"].state.store for pid in (alpha, beta, lone)}
        store[alpha].set_setting("account", {"id": 101, "username": "alpha_watch"})
        for pid in (alpha, beta):
            store[pid].set_target(CHANNEL, "Harbor channel", "channel", pid == alpha)
        store[lone].set_target(-1009, "Only Lone", "channel", True)
        store[alpha].append("observation.started", {"parameters": {"heartbeat_seconds": 60}})
        store[alpha].append("message.new", {"text": "hello"}, chat_id=CHANNEL, message_id=7)
        result = call("GET", "profile-groups/" + gid + "/overview")
        assert result["group"] == {"id": gid, "label": "Harbor case", "goal": None, "members": 3}
        rows = {m["id"]: m for m in result["members"]}
        assert set(rows) == {alpha, beta, lone}
        assert rows[alpha]["username"] == "alpha_watch" and rows[alpha]["account_id"] == 101
        assert rows[alpha]["last_message"]["kind"] == "message.new" and rows[beta]["last_message"] is None
        assert rows[alpha]["route"]["mode"] and rows[alpha]["route"]["latency_ms"] is None
        assert rows[beta]["account_kind"] is None
        # Only a chat two members see is shared; only Alpha records it, and it observes now.
        [chat] = result["chats"]
        assert chat["chat_id"] == CHANNEL and sorted(chat["seen_by"]) == sorted([alpha, beta])
        assert chat["recorded_by"] == [alpha]
        assert chat["coverage"]["observed"] and chat["coverage"]["interruptions"] == 0
        # A pause just now is not yet an interruption: silences up to three heartbeats are allowed.
        store[alpha].append("observation.stopped", {"reason": "operator"})
        group_overview._periods.clear()
        [chat] = call("GET", "profile-groups/" + gid + "/overview")["chats"]
        assert chat["coverage"]["interruptions"] == 0
        call("GET", "profile-groups/" + "0" * 32 + "/overview", status=400)


def test_interruptions():
    t = datetime(2026, 11, 1, tzinfo=timezone.utc)
    hour, allowed = timedelta(hours=1), timedelta(minutes=3)
    # Two accounts together cover 0–5 h with a hole at 2–3 h; a one-minute silence does not count.
    periods = [(t, t + 2 * hour), (t + 3 * hour, t + 4 * hour), (t + 4 * hour + timedelta(minutes=1), t + 5 * hour)]
    holes = group_overview.interruptions(periods, t, t + 5 * hour, allowed)
    assert holes == [(t + 2 * hour, t + 3 * hour)]
    assert group_overview.interruptions(periods, t, t + 6 * hour, allowed)[-1] == (t + 5 * hour, t + 6 * hour)
    assert group_overview.interruptions([], t, t + hour, allowed) == [(t, t + hour)]


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
