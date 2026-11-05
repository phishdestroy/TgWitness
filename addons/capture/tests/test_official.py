import asyncio
import json

import pytest
from fastapi.testclient import TestClient

from tgwitness_capture.format import canonical
from tgwitness_capture.journal import Journal
from tgwitness_capture.official import GuardStopped, OfficialBrowser, OfficialOptions, PaceWait, URL, official_url
from tgwitness_capture.service import Config, create_app


@pytest.mark.parametrize("url", ["https://web.telegram.org.evil/a/", "http://web.telegram.org/a/",
                                 "https://evil@web.telegram.org/a/", "https://web.telegram.org/k/",
                                 "https://web.telegram.org/a/?redirect=evil", "https://web.telegram.org:8443/a/"])
def test_origin_is_exact(url):
    assert not official_url(url)
    assert official_url(URL + "#123")


@pytest.mark.parametrize("change", [{"proxy_server": "http://user:secret@host:3128"},
                                    {"proxy_server": "http://host:3128/path"},
                                    {"max_pause_seconds": 2.0, "min_pause_seconds": 3.0},
                                    {"proxy_server": "direct"}, {"max_steps": True},
                                    {"egress": "socks5"}, {"expected_ip": "not-an-ip"}])
def test_invalid_or_unsafe_configuration(change):
    with pytest.raises(ValueError):
        OfficialOptions.model_validate({"proxy_server": "http://gateway:3128", **change})


def test_named_api_authentication_validation_and_frozen_plan(tmp_path):
    config = Config(official={"proxy_server": "http://gateway:3128"})
    with TestClient(create_app(tmp_path, config)) as client:
        recorder = client.app.state.recorder
        control = {"Authorization": "Bearer " + recorder.tokens["control"]}
        witness = {"Authorization": "Bearer " + recorder.tokens["witness"]}
        assert client.post("/api/official/open").status_code == 401
        assert client.post("/api/official/open", headers=witness).status_code == 401
        assert client.get("/api/checkpoint", headers=witness).status_code == 200
        assert client.post("/api/official/evaluate", headers=control, json={"js": "sendMessage()"}).status_code == 404
        assert client.post("/api/official/scroll", headers=control, json={"direction": "send"}).status_code == 422
        secret = "SENSITIVE-NOT-FOR-ERROR-OUTPUT"
        response = client.post("/api/official/password", headers=control, json={"password": [secret]})
        assert response.status_code == 422 and secret not in response.text
        assert secret not in canonical(recorder.journal.events()).decode()
        settings = {"enabled": True, "video": False}
        assert client.post("/api/settings", headers=control, json=settings).status_code == 400
        plan = {"mode": "paced", "min_pause_seconds": 3.0, "max_pause_seconds": 5.0,
                "scroll_pixels": 200, "max_steps": 20, "session_minutes": 10}
        response = client.post("/api/official/plan", headers=control, json=plan)
        assert response.status_code == 200
        assert response.json()["official"]["options"]["mode"] == "paced"
        assert not response.json()["settings"]["enabled"]
        recorder.official.phase = "login"
        assert client.post("/api/official/plan", headers=control, json=plan).status_code == 409
        assert "official.js" in client.get("/").text


def test_egress_change_and_unavailable_probe_stop(tmp_path):
    class Reply:
        status, url = 200, "https://www.cloudflare.com/cdn-cgi/trace"
        ip = "203.0.113.7"

        async def body(self):
            return ("ip=" + self.ip + "\nwarp=on\n").encode()

        async def dispose(self):
            pass

    class Request:
        async def get(self, *args, **kwargs):
            return response

    response = Reply()
    journal = Journal(tmp_path)
    adapter = OfficialBrowser(OfficialOptions(proxy_server="http://gateway:3128"), journal)
    adapter.context = type("Context", (), {"request": Request()})()

    async def exercise():
        await adapter.check_route()
        assert adapter.exit_ip == "203.0.113.7"
        response.ip = "203.0.113.8"
        with pytest.raises(GuardStopped, match="EgressAddressChanged"):
            await adapter.check_route()
        response.status = 503
        with pytest.raises(GuardStopped, match="EgressCheckUnavailable"):
            await adapter.check_route()

    try:
        asyncio.run(exercise())
    finally:
        journal.close()


# Synthetic DOM using the reviewed official client's public element boundaries.
# This is not a Telegram login or a claim to have exercised a real account.
FIXTURE = """<!doctype html><html><head><meta charset="utf-8"><title>Synthetic official-client fixture</title>
<style>.MessageList{height:350px;width:700px;overflow:auto}.Message{height:160px}body{margin:0}</style></head><body>
<div id="LeftColumn"><div class="chat-list"><div class="Chat"><a class="ListItem-button" href="#123"><span class="title">Alice &lt;script&gt;</span></a></div></div></div>
<div id="MiddleColumn"><div class="MessageList"><div class="messages-container">
<div class="Message" data-message-id="1"><b class="sender-name">Alice</b><div class="text-content">Original message</div><span class="time" title="2026-11-05 12:00">12:00</span></div>
<div class="Message" data-message-id="2"><div class="text-content">Second message</div></div>
<div class="Message" data-message-id="3"><div class="text-content">Third message</div></div>
</div></div><div class="Composer"><div contenteditable="true" id="composer"></div><button id="send">Send</button></div></div>
<script>window.sent=0;document.getElementById('send').onclick=()=>window.sent++;</script></body></html>"""


def test_owned_browser_guard_scroll_capture_and_unknown_dialog(tmp_path, request):
    if not request.config.getoption("--capture-browser"):
        pytest.skip("Use --capture-browser for real Chromium validation")
    journal = Journal(tmp_path / "official")
    adapter = OfficialBrowser(OfficialOptions(proxy_server="http://127.0.0.1:9", require_video=False), journal, headless=True)

    async def probe():
        adapter.exit_ip = "203.0.113.7"
        adapter.checked_route = __import__("time").monotonic()

    real_route = adapter._route

    async def fixture_route(route):
        class FixtureRoute:
            request = route.request

            async def continue_(self):
                await route.fulfill(status=200, content_type="text/html", body=FIXTURE)

            async def abort(self, error):
                await route.abort(error)
        await real_route(FixtureRoute())

    adapter.check_route = probe
    adapter._route = fixture_route

    async def exercise():
        await adapter.open()
        assert await adapter.login_state() == "ready"
        chats = await adapter.chats()
        assert len(chats) == 1 and chats[0]["title"] == "Alice <script>"
        await adapter.select_chat(chats[0]["handle"])
        await adapter.arm()
        assert (await adapter.page.evaluate("window.__tgwitnessGuard.inspect()"))["armed"]
        await adapter.page.locator("#send").dispatch_event("click")
        await adapter.page.locator("#composer").dispatch_event("keydown", {"key": "Enter"})
        assert await adapter.page.evaluate("window.sent") == 0
        assert await adapter.page.locator(".Composer").evaluate("el=>el.inert")
        with pytest.raises(PaceWait):
            await adapter.scroll("newer")
        adapter.next_step = 0
        await adapter.scroll("newer")
        assert adapter.steps == 1
        metadata, artifacts, observed = await adapter.capture(journal, {"screenshots": True, "pages": True}, 60, True)
        journal.append("capture.saved", metadata, artifacts, observed)
        messages = next(a for a in artifacts if a["role"] == "rendered_messages")
        values = json.loads((journal.objects / messages["sha256"]).read_bytes())
        assert values[0]["rendered_id"] == "1" and "Original message" in values[0]["rendered_text"]
        assert not values[0]["telegram_origin_independently_proven"]
        await adapter.pause()
        with pytest.raises(ValueError, match="Start recording"):
            await adapter.scroll()
        await adapter.arm()
        await adapter.page.evaluate("document.body.insertAdjacentHTML('beforeend','<div class=\"Modal open\">Delete?</div>')")
        with pytest.raises(GuardStopped, match="UnexpectedDialog"):
            await adapter.tick()
        assert await adapter.page.locator("#tgwitness-stop-cover").is_visible()
        # A login screen is covered too, before it could become a subsequent snapshot.
        assert len(journal.events()) >= 4

    async def run():
        try:
            await exercise()
        finally:
            await adapter.close()

    try:
        asyncio.run(run())
    finally:
        journal.close()
