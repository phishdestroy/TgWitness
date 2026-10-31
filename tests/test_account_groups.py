import base64
import os

from fastapi.testclient import TestClient

from tgwitness.account_import import string_session
from tgwitness.app import create_app
from test_collector import FakeClient


def session_file(name="account.txt"):
    text = string_session(2, os.urandom(256))
    return {"name": name, "content": base64.b64encode(text.encode()).decode()}


def panel(tmp_path):
    app = create_app(tmp_path, client_factory=FakeClient)
    client = TestClient(app)
    client.__enter__()
    client.headers["Authorization"] = "Bearer " + app.state.vault.token
    return app, client


def test_bulk_import_gives_each_account_a_workspace_in_a_group_and_rolls_back_failures(tmp_path):
    app, client = panel(tmp_path)
    try:
        group = client.post("/api/profile-groups", json={"label": "Scam monitors"}).json()["groups"][0]["id"]
        first = client.post("/api/profiles/import", json={"files": [session_file("alpha.session.txt")], "group": group,
                                                          "api_id": 501, "api_hash": "a" * 32})
        assert first.status_code == 200, first.text
        assert first.json()["account"]["id"] == 501 and first.json()["profile"]["label"] == "alpha.session"
        second = client.post("/api/profiles/import", json={"files": [session_file()], "group": group, "label": "Beta",
                                                           "api_id": 502, "api_hash": "b" * 32})
        assert second.status_code == 200, second.text
        duplicate = client.post("/api/profiles/import", json={"files": [session_file()], "group": group,
                                                              "api_id": 501, "api_hash": "a" * 32})
        assert duplicate.status_code == 400 and "Not imported" in duplicate.text
        listed = client.get("/api/profiles").json()["profiles"]
        assert sorted(p["label"] for p in listed) == ["Beta", "Main account", "alpha.session"]
        groups = client.get("/api/profile-groups").json()["groups"]
        assert len(groups[0]["members"]) == 2
        assert client.post("/api/profiles/import", json={"files": [{"name": "x.txt", "content": "bm90IGEgc2Vzc2lvbg=="}]}
                           ).status_code == 400
        reader = client.post("/api/witness/tokens", json={"label": "Read only"}).json()["token"]
        assert client.post("/api/profiles/import", json={"files": [session_file()]},
                           headers={"Authorization": "Bearer " + reader}).status_code == 401
    finally:
        client.__exit__(None, None, None)


def test_group_settings_come_from_the_template_and_each_member_journals_them(tmp_path):
    app, client = panel(tmp_path)
    try:
        members = [client.post("/api/profiles", json={"label": name}).json()["id"] for name in ("One", "Two")]
        assert client.post("/api/parameters", json={"values": {"snapshot_max": 777}}).status_code == 200
        assert client.post("/api/report-options", json={"case_id": "PD-1", "language": "ru"}).status_code == 200
        group = client.post("/api/profile-groups", json={"label": "Team", "template": "default",
                                                        "sections": ["parameters", "reports"]}).json()["groups"][0]
        for profile_id in ["default", *members]:
            assert client.put("/api/profiles/" + profile_id + "/group", json={"group": group["id"]}).status_code == 200
        applied = client.post("/api/profile-groups/" + group["id"] + "/apply", json={}).json()
        assert {r["status"] for r in applied["results"]} == {"applied"} and len(applied["results"]) == 2
        for profile_id in members:
            prefix = "/profiles/" + profile_id + "/api"
            values = {p["key"]: p["value"] for group_ in client.get(prefix + "/parameters").json()["groups"]
                      for p in group_["items"]}
            assert values["snapshot_max"] == 777
            assert client.get(prefix + "/report-options").json()["case_id"] == "PD-1"
            events = client.get(prefix + "/events?kind=group.settings_applied").json()["events"]
            assert events and events[0]["payload"]["sections"] == ["parameters", "reports"]
        assert client.post("/api/profile-groups", json={"label": "Bad", "sections": ["secrets"]}).status_code == 400
        assert client.delete("/api/profile-groups/" + group["id"]).status_code == 200
        assert all(p["group"] is None for p in client.get("/api/profiles").json()["profiles"])
    finally:
        client.__exit__(None, None, None)
