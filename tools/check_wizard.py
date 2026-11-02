"""Check the step-by-step setup (wizard.py, views/wizard.js) with a local panel and a synthetic Telegram client.

The plan from the answers, progress kept in the workspace, what applying changes and records in the signed
journal, hand changes afterwards, the connection route with its IP mode. Then a new workspace in a browser:
it opens with the wizard, every step has its own address, Back keeps the answers, sign-in, chats, applying
and the live check, at 360, 600, 1024 and 1440 pixels, in English and Russian; and the short path that saves
a copy of the account.
"""
import json
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from tgwitness import levels, wizard  # noqa: E402
from tgwitness.anchoring import EvidenceMode  # noqa: E402
from tgwitness.monitoring import MEDIA_DEFAULT_MB, MEDIA_TYPES  # noqa: E402
from tgwitness.scope import Scope  # noqa: E402
from tgwitness.tuning import BY_KEY  # noqa: E402

CAPTURE = {"download_media": True, "record_disabled_media": True, "max_media_mb": 20,
           "types": {kind: {"enabled": kind not in ("animation", "sticker"), "max_mb": MEDIA_DEFAULT_MB[kind]}
                     for kind in MEDIA_TYPES}}
PARAMETERS = {key: parameter.initial() for key, parameter in BY_KEY.items()}
CHATS = {-1001: ("Scam group", "supergroup"), -1002: ("Announcements", "channel"), 77: ("Helper bot", "bot")}


def current(**changes):
    return {"scope": Scope().model_dump(), "monitoring": {name: True for name in wizard.Saving.model_fields
                                                          if name not in ("media", "history", "timestamps")},
            "capture": CAPTURE, "evidence": EvidenceMode().model_dump(), "parameters": PARAMETERS,
            "targets": [], **changes}


def answers(**values):
    base = {"goal": "watch", "purpose": "investigation", "account_kind": "dedicated",
            "chats": {"mode": "selected", "chat_ids": [-1001]}, "saving": wizard.presets()["investigation"]["saving"],
            "place": "computer"}
    return wizard.Answers(**{**base, **values})


def check_plan():
    for missing, step in (({"goal": None}, "goal"), ({"chats": None}, "chats"),
                          ({"chats": {"mode": "selected", "chat_ids": []}}, "chats"), ({"saving": None}, "saving"),
                          ({"place": None}, "place"), ({"chats": {"mode": "account"}}, "chats")):
        try:
            wizard.plan(answers(**missing), current())
            raise AssertionError(("an incomplete answer must be refused", missing))
        except wizard.Incomplete as exc:
            assert exc.step == step, (missing, exc.step)
    plan = wizard.plan(answers(), current())
    assert plan["goal"] == "investigation" and plan["enable"] == [-1001] and plan["pause"] == []
    assert plan["scope"] == Scope().model_dump(), "chosen chats leave the scope's other parts as they are"
    assert wizard.plan(answers(chats={"mode": "account", "acknowledged": True}), current())["scope"]["new_chats"] == \
        {"profile": True, "history": 200}, "a whole investigation account saves a new chat's profile and messages"
    assert plan["evidence"]["enabled"] and plan["evidence"]["devices"] and not plan["evidence"]["drand"], \
        "an investigation takes the timestamps and the device list its goal recommends"
    assert plan["capture"]["types"]["video"]["max_mb"] == 100 and all(r["enabled"] for r in plan["capture"]["types"].values())
    wide = wizard.plan(answers(chats={"mode": "account", "acknowledged": True}), current())
    assert wide["acknowledged"] and wide["setup"].size == "large" and wide["parameters"] == {"dialog_limit": 20000}
    personal = wizard.plan(answers(purpose="personal", saving=wizard.presets()["personal"]["saving"]), current())
    assert personal["evidence"] is None and personal["capture"]["max_media_mb"] == 20
    assert not personal["monitoring"]["reactions"] and personal["scope"]["mode"] == "selected"
    evidence = wizard.plan(answers(goal="evidence", purpose=None, saving=wizard.presets()["evidence"]["saving"]), current())
    assert evidence["setup"].goal == "evidence" and evidence["evidence"]["drand"] and evidence["evidence"]["interval_minutes"] == 10
    chosen = current(targets=[{"chat_id": -1001, "enabled": 1}, {"chat_id": -1002, "enabled": 1}, {"chat_id": 77, "enabled": 0}])
    paused = wizard.plan(answers(chats={"mode": "selected", "chat_ids": [-1001, 77]}), chosen)
    assert paused["enable"] == [77] and paused["pause"] == [-1002], "chats left out of the choice are paused, not removed"
    assert wizard.media_choice(wizard.media_capture("small", CAPTURE)) == "small"
    assert wizard.media_choice(wizard.media_capture("all", CAPTURE)) == "all"
    assert wizard.media_choice({**CAPTURE, "download_media": False}) == "none"
    assert wizard.connection_problem("direct", 503, "Connection unavailable: ConnectionError") == "direct_unreachable"
    assert wizard.connection_problem("socks5", 503, "Connection unavailable: OSError") == "proxy_unreachable"
    assert wizard.connection_problem("mtproxy_auto", 503, "Connection unavailable: NoProxyAvailable") == "no_public_proxy"
    named = levels.assess(EvidenceMode().model_dump(), {"enabled": False, "retention_days": 0},
                          {"enabled": False, "problems": True}, [], None, {}, [], "server")
    assert not named["reliability"]["items"][0]["on"], "a server named in an answer earns no points"
    return "ok  plan: each missing answer names its step, presets per goal, chats paused not removed, no points for words"


def check_api(directory):
    from check_browser import RunningApp
    with RunningApp(directory / "api", wizard=True) as server:
        store, collector = server.app.state.store, server.app.state.collector
        session = requests.post(server.url + "/api/access/login", json={"token": server.app.state.vault.token},
                                timeout=10).json()["session"]
        headers = {"Authorization": "Bearer " + session}
        get = lambda path: requests.get(server.url + path, headers=headers, timeout=20).json()
        post = lambda path, body: requests.post(server.url + path, json=body, headers=headers, timeout=60)
        assert get("/api/status")["setup_wizard"] == {"finished": False, "skipped": False, "step": "goal"}
        state = get("/api/setup/wizard")
        assert state["step"] == "goal" and state["answers"]["goal"] is None and set(state["presets"]) == set(levels.GOALS)
        assert post("/api/setup/wizard", {"step": "nowhere", "answers": {}}).status_code == 422
        assert post("/api/setup/wizard", {"step": "goal", "answers": {"goal": "bogus"}}).status_code == 422
        saved = post("/api/setup/wizard", {"step": "connection", "answers": {"goal": "watch", "purpose": "investigation"}})
        assert saved.ok, saved.text
        assert get("/api/setup/wizard")["answers"]["purpose"] == "investigation"
        assert get("/api/status")["setup_wizard"]["step"] == "connection", "progress is kept in the workspace"
        incomplete = post("/api/setup/wizard/preview", {"goal": "watch", "purpose": "investigation"}).json()
        assert incomplete == {"ready": False, "step": "chats", "message": "Choose the chats to record."}, incomplete

        # The route with the IP mode it needs: direct only where the address may be seen; a proxy hides it again.
        direct = post("/api/setup/wizard/route", {"kind": "direct"})
        assert direct.ok, direct.text
        assert direct.json()["policy"]["exposure"] == "tunnel" and collector.network_config().kind == "direct"
        check = post("/api/setup/wizard/check-connection", {}).json()
        assert check["ok"] and check["kind"] == "direct" and isinstance(check["elapsed_ms"], int), check
        assert get("/api/setup/wizard")["checks"]["connection"]["ok"]
        socks = post("/api/setup/wizard/route", {"kind": "socks5", "host": "proxy.example.org", "port": 1080})
        assert socks.ok, socks.text
        assert socks.json()["policy"]["exposure"] == "hide" and socks.json()["policy"]["outside_enabled"]
        mtproxy = post("/api/setup/wizard/route", {"kind": "mtproxy", "host": "proxy.example.org", "port": 443,
                                                    "secret": "a7" * 16})
        assert mtproxy.ok, mtproxy.text
        policy = mtproxy.json()["policy"]
        assert policy["exposure"] == "hide" and not policy["outside_enabled"] and policy["outside_route"] == "none"
        back = post("/api/setup/wizard/route", {"kind": "direct"})
        assert back.ok and back.json()["policy"]["exposure"] == "tunnel", back.text
        kinds = [row["kind"] for row in store.db.execute("SELECT kind FROM events ORDER BY seq")]
        assert kinds.count("network.changed") == 4 and "network.policy_changed" in kinds

        collector.dialog_cache = {chat_id: {"chat_id": chat_id, "title": title, "kind": kind, "entity": None,
                                            "archived": False} for chat_id, (title, kind) in CHATS.items()}
        chosen = {"goal": "watch", "purpose": "investigation", "account_kind": "dedicated",
                  "chats": {"mode": "selected", "chat_ids": [-1001, -1002]},
                  "saving": wizard.presets()["investigation"]["saving"], "place": "server"}
        preview = post("/api/setup/wizard/preview", chosen).json()
        assert preview["ready"] and preview["enable"] == 2 and preview["after"]["timestamps"], preview
        assert not preview["now"]["timestamps"] and preview["after"]["media"] == "standard"
        credibility = [item["id"] for item in preview["scales"]["after"]["credibility"]["items"] if item["on"]]
        assert credibility == ["journal", "timestamps", "devices"], credibility
        assert not preview["scales"]["after"]["reliability"]["items"][0]["on"], "the place answer earns no points"
        before = store.db.execute("SELECT max(seq) FROM events").fetchone()[0]
        applied = post("/api/setup/wizard/apply", chosen)
        assert applied.ok, applied.text
        result = applied.json()
        assert result["changed"] == ["capture", "chats", "evidence"], result["changed"]
        assert result["finished_at"] and result["drift"] == [], result["drift"]
        targets = {t["chat_id"]: t for t in store.targets()}
        assert targets[-1001]["enabled"] and targets[-1002]["enabled"] and 77 not in targets
        assert store.get_setting("setup")["goal"] == "investigation" and store.get_setting("setup")["wizard"] is True
        assert store.get_setting("evidence")["enabled"] and store.get_setting("capture")["types"]["video"]["max_mb"] == 100
        rows = store.db.execute("SELECT kind,payload FROM events WHERE seq>? ORDER BY seq", (before,)).fetchall()
        kinds = [row["kind"] for row in rows]
        assert "scope.changed" not in kinds, "the same scope is not recorded again"
        for kind in ("capture.changed", "target.changed", "evidence.changed", "setup.applied"):
            assert kind in kinds, (kind, kinds)
        record = json.loads(next(row["payload"] for row in rows if row["kind"] == "setup.applied"))
        assert record["wizard"]["chats"]["chat_ids"] == 2 and record["goal"] == "investigation", record
        status = get("/api/status")
        assert status["setup_wizard"]["finished"] and status["setup_answered"]

        # A change by hand afterwards is shown, and applying the answers again restores it.
        capture = dict(store.get_setting("capture"))
        assert requests.post(server.url + "/api/capture", json={**capture, "download_media": False}, headers=headers,
                             timeout=10).ok
        assert get("/api/setup/wizard")["drift"] == ["media"]
        again = post("/api/setup/wizard/apply", chosen).json()
        assert again["changed"] == ["capture"] and again["drift"] == [], again["changed"]
        assert post("/api/setup/wizard/apply", chosen).json()["changed"] == [], "the same answers change nothing"

        # Fewer chats pause the rest; the whole account needs the dedicated-account confirmation.
        fewer = post("/api/setup/wizard/apply", {**chosen, "chats": {"mode": "selected", "chat_ids": [-1002]}})
        assert fewer.ok and not {t["chat_id"]: t for t in store.targets()}[-1001]["enabled"], fewer.text
        refused = post("/api/setup/wizard/apply", {**chosen, "chats": {"mode": "account"}})
        assert refused.status_code == 422 and refused.json()["detail"]["step"] == "chats", refused.text
        wide = post("/api/setup/wizard/apply", {**chosen, "chats": {"mode": "account", "acknowledged": True}})
        assert wide.ok, wide.text
        assert store.get_setting("scope")["mode"] == "account" and store.get_setting("parameters")["dialog_limit"] == 20000
        assert post("/api/setup/wizard/apply", {**chosen, "chats": {"mode": "selected", "chat_ids": [404]}}).status_code == 400
    with RunningApp(directory / "skip", wizard=True) as server:
        session = requests.post(server.url + "/api/access/login", json={"token": server.app.state.vault.token},
                                timeout=10).json()["session"]
        skipped = requests.post(server.url + "/api/setup/wizard/skip", json={"reason": "expert"}, timeout=10,
                                headers={"Authorization": "Bearer " + session}).json()
        assert skipped["skipped_at"] and not skipped["finished_at"]
        store = server.app.state.store
        assert store.get_setting("setup")["skipped"] and store.get_setting("evidence", None) is None
    return "ok  api: progress kept, route with its IP mode, connection check, preview, apply journals each part, drift, skip"


def check_browser(directory, output):
    from check_browser import RunningApp, launch_browser, unlock
    from playwright.sync_api import expect, sync_playwright
    from tgwitness import i18n
    errors, external = [], []
    with RunningApp(directory / "panel", wizard=True) as server, sync_playwright() as p:
        store = server.app.state.store
        browser = launch_browser(p)
        context = browser.new_context(viewport={"width": 1440, "height": 1000}, reduced_motion="reduce")
        page = context.new_page()
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
        page.on("request", lambda request: external.append(request.url)
                if urlsplit(request.url).hostname != "127.0.0.1" else None)
        unlock(page, server, start=True)
        expect(page.locator("#view-setup")).to_be_visible()
        expect(page).to_have_url(server.url + "/setup/goal?ws=default")
        expect(page.locator(".wizard-count")).to_have_text("Step 1 of 7")
        expect(page.locator("#setup-card")).to_be_hidden()
        next_button = page.locator(".wizard-nav .primary")
        expect(next_button).to_be_disabled()
        page.screenshot(path=str(output / "goal-1440.png"), full_page=True)

        page.locator('input[name="wizard-goal"][value="watch"]').check()
        page.locator('input[name="wizard-purpose"][value="investigation"]').check()
        next_button.click()
        expect(page).to_have_url(server.url + "/setup/connection?ws=default")
        expect(page.locator("#view-setup h1")).to_be_focused()
        page.go_back()
        expect(page).to_have_url(server.url + "/setup/goal?ws=default")
        expect(page.locator('input[name="wizard-purpose"][value="investigation"]')).to_be_checked()
        page.go_forward()
        expect(page.locator(".wizard-count")).to_have_text("Step 2 of 7")

        # A proxy is pasted as one line; the panel reads its kind, address and login before saving anything.
        page.locator('input[name="wizard-route"][value="mtproxy"]').check()
        expect(page.locator(".wizard-run")).to_be_disabled()
        page.locator("#wizard-proxy").fill("socks5://user:secret@proxy.example.org:1081")
        expect(page.locator(".wizard-parsed")).to_have_text("SOCKS5 proxy · proxy.example.org:1081 · with a login")
        expect(page.locator(".wizard-run")).to_be_enabled()
        page.locator("#wizard-proxy").fill("not a proxy at all")
        expect(page.locator(".wizard-parsed")).to_have_text("This is not a proxy link or address.")
        expect(page.locator(".wizard-run")).to_be_disabled()
        assert server.app.state.collector.network_config().kind == "mtproxy_auto", "typing saves nothing"
        page.locator('input[name="wizard-route"][value="direct"]').check()
        page.locator(".wizard-run").click()
        expect(page.locator(".wizard-notice.success")).to_contain_text("Connected to Telegram in")
        assert server.app.state.collector.network_config().kind == "direct"
        page.screenshot(path=str(output / "connection-1440.png"), full_page=True)
        next_button.click()

        expect(page).to_have_url(server.url + "/setup/account?ws=default")
        expect(page.locator(".wizard-auth #credentials-form")).to_be_visible()
        expect(next_button).to_be_disabled()
        page.locator("#phone").fill("+15550001111")
        page.locator("#auth-continue").click()
        expect(page.locator("#code-form")).to_be_visible()
        page.locator("#code").fill("11111")
        page.locator("#code-form button[type=submit]").click()
        expect(page.locator(".wizard-account")).to_contain_text("@synthetic")
        expect(page.locator(".wizard-auth")).to_have_count(0)
        page.locator('input[name="wizard-account-kind"][value="dedicated"]').check()
        next_button.click()

        expect(page).to_have_url(server.url + "/setup/chats?ws=default")
        expect(page.locator('input[name="wizard-scope"][value="account"]')).to_be_checked()
        expect(page.locator(".wizard-counter")).to_have_text("Will be recorded: 2 chats, and new ones as they appear")
        expect(next_button).to_be_disabled()
        page.locator("#wizard-acknowledge").check()
        expect(next_button).to_be_enabled()
        page.locator('input[name="wizard-scope"][value="selected"]').check()
        expect(page.locator(".wizard-chat")).to_have_count(2)
        page.locator(".wizard-chat", has_text="Synthetic group").locator("input").check()
        expect(page.locator(".wizard-counter")).to_have_text("Will be recorded: 1 chat")
        page.screenshot(path=str(output / "chats-1440.png"), full_page=True)
        next_button.click()

        expect(page).to_have_url(server.url + "/setup/saving?ws=default")
        expect(page.locator('input[name="wizard-media"][value="standard"]')).to_be_checked()
        page.locator('input[name="wizard-history"][value="recent"]').check()
        next_button.click()
        page.locator('input[name="wizard-place"][value="computer"]').check()
        next_button.click()

        expect(page).to_have_url(server.url + "/setup/summary?ws=default")
        expect(page.locator(".wizard-summary .wizard-row")).to_have_count(6)
        expect(page.locator(".wizard-scales .level-scale")).to_have_count(2)
        expect(page.locator(".wizard-changes")).to_contain_text("1 chat starts recording")
        page.screenshot(path=str(output / "summary-1440.png"), full_page=True)
        page.reload()
        expect(page).to_have_url(server.url + "/setup/summary?ws=default")
        expect(page.locator(".wizard-summary .wizard-row")).to_have_count(6)
        page.locator(".wizard-start").click()
        expect(page.locator(".wizard-live")).to_be_visible()
        expect(page.get_by_text("Done! What next:")).to_be_visible(timeout=60000)
        assert server.app.state.collector.running, "Start recording starts observation"
        assert store.get_setting("setup")["goal"] == "investigation"
        assert [t["chat_id"] for t in store.targets() if t["enabled"]] == [-1000000000123]
        kinds = {row["kind"] for row in store.db.execute("SELECT kind FROM events")}
        assert {"setup.applied", "observation.started", "snapshot.completed"} <= kinds, kinds
        page.screenshot(path=str(output / "live-1440.png"), full_page=True)

        # Every page at the four widths, in English and Russian: no overflow, Back and Next in reach.
        words = i18n.words("ru")
        for lang in ("en", "ru"):
            context.add_cookies([{"name": i18n.COOKIE, "value": lang, "url": server.url}])
            page.goto(server.url + "/setup/goal")
            expect(page.locator("#view-setup")).to_have_attribute("data-step", "goal")
            for width in (360, 600, 1024, 1440):
                page.set_viewport_size({"width": width, "height": 900})
                for index, step in enumerate(("goal", "connection", "account", "chats", "saving", "place", "summary")):
                    page.locator(".wizard-steps .wizard-step-link").nth(index).click()
                    expect(page).to_have_url(server.url + "/setup/" + step + "?ws=default")
                    expect(page.locator("#view-setup")).to_have_attribute("data-step", step)
                    page.wait_for_timeout(150)
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (lang, width, step)
                    clipped = page.evaluate("""() => [...document.querySelectorAll('#view-setup *')].filter(e => {
                        const r = e.getBoundingClientRect(); return r.width && (r.right > innerWidth + 1 || r.left < -1);
                    }).map(e => e.className || e.tagName).slice(0, 5)""")
                    assert not clipped, (lang, width, step, clipped)
                    if width in (360, 1440) or step in ("goal", "summary"):
                        page.screenshot(path=str(output / f"{step}-{lang}-{width}.png"), full_page=True)
            if lang == "ru":
                page.locator(".wizard-steps .wizard-step-link").first.click()
                expect(page.locator("#view-setup h1")).to_have_text(words["What do you need?"])
                expect(page.locator(".wizard-count")).to_have_text(words["Step {n} of {total}"].replace("{n}", "1").replace("{total}", "7"))
        browser.close()
    assert not errors, errors
    assert not external, external
    return "ok  browser: opens first, step addresses and Back, sign-in, chats, apply and live check; 4 widths, en and ru"


def check_copy(directory):
    """A copy of the account is the short path: goal, connection, sign-in, then the account export."""
    from check_browser import RunningApp, launch_browser, unlock
    from playwright.sync_api import expect, sync_playwright
    errors = []
    with RunningApp(directory / "copy", wizard=True) as server, sync_playwright() as p:
        browser = launch_browser(p)
        page = browser.new_page(viewport={"width": 1024, "height": 900})
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        unlock(page, server, start=True)
        page.locator('input[name="wizard-goal"][value="copy"]').check()
        expect(page.locator(".wizard-count")).to_have_text("Step 1 of 4")
        expect(page.locator(".wizard-steps .wizard-step")).to_have_count(4)
        page.locator(".wizard-nav .primary").click()
        page.locator('input[name="wizard-route"][value="direct"]').check()
        page.locator(".wizard-run").click()
        expect(page.locator(".wizard-notice.success")).to_be_visible()
        page.locator(".wizard-nav .primary").click()
        page.locator("#phone").fill("+15550002222")
        page.locator("#auth-continue").click()
        page.locator("#code").fill("11111")
        page.locator("#code-form button[type=submit]").click()
        expect(page.locator(".wizard-account")).to_be_visible()
        expect(page.locator('input[name="wizard-account-kind"]')).to_have_count(0)
        page.locator(".wizard-nav .primary").click()
        expect(page).to_have_url(server.url + "/setup/summary?ws=default")
        expect(page.locator(".wizard-summary .wizard-row")).to_have_count(3)
        page.locator(".wizard-start").click()
        expect(page.locator("#view-evidence")).to_be_visible()
        store = server.app.state.store
        assert store.get_setting("setup_wizard")["finished_at"] and store.get_setting("setup")["skipped"]
        assert not server.app.state.collector.running, "a copy of the account starts no observation"
        browser.close()
    assert not errors, errors
    return "ok  copy: four steps, sign-in without the account question, then the account export; no observation"


def main():
    output = ROOT / "test-results" / "wizard"
    output.mkdir(parents=True, exist_ok=True)
    print(check_plan())
    with tempfile.TemporaryDirectory() as tmp:
        print(check_api(Path(tmp)))
        print(check_browser(Path(tmp), output))
        print(check_copy(Path(tmp)))
    print("wizard checks passed")


if __name__ == "__main__":
    main()
