"""Sources tabs and recording drafts against a synthetic local workspace."""
import json
import tempfile
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

from check_browser import (ROOT, RunningApp, hold_api_response, launch_browser,
                           release_api_response, unlock)
from test_collector import saved_session


def seed(server):
    store, vault = server.app.state.store, server.app.state.vault
    vault.save("credentials", {"api_id": 123, "api_hash": "a" * 32, "session": saved_session()})
    for number in range(21):
        store.set_target(-1000000001000 - number, "Investigation source " + str(number + 1).zfill(2),
                         "supergroup" if number % 3 else "channel", number % 4 != 0,
                         priority=number % 5 == 0)


def main():
    output = ROOT / "build" / "ux-review" / "after" / "17"
    output.mkdir(parents=True, exist_ok=True)
    errors, writes = [], []
    with tempfile.TemporaryDirectory(prefix="sources-browser-") as scratch, RunningApp(
            Path(scratch)) as server, sync_playwright() as playwright:
        seed(server)
        browser = launch_browser(playwright)
        page = browser.new_page(viewport={"width": 1440, "height": 1000}, reduced_motion="reduce")
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", lambda request: writes.append(request.url) if request.method == "POST"
                and any(request.url.endswith("/api/" + name)
                        for name in ("recording", "monitoring", "capture", "recheck")) else None)
        unlock(page, server)
        page.evaluate("sourcesReady")
        page.locator('[data-view="sources"]').click()
        expect(page.locator("#sources-panel-scope")).to_be_visible()
        expect(page.locator("#sources-tab-count")).to_have_text("21")
        page.locator("#sources-tab-scope").focus()
        page.keyboard.press("ArrowRight")
        expect(page.locator("#sources-tab-chats")).to_be_focused()
        page.keyboard.press("ArrowRight")
        expect(page.locator("#sources-panel-recording")).to_be_visible()
        expect(page.locator("#recording-save")).to_be_disabled()
        page.locator("#monitor-reactions").uncheck()
        page.locator("#max-media").fill("50")
        page.locator(".media-rules-details").evaluate("details=>details.open=true")
        page.locator("#media-max-video").fill("7")
        page.locator(".media-rules-details").evaluate("details=>details.open=false")
        page.locator("#recheck-priority").fill("33")
        page.locator("#max-media").focus()
        page.evaluate("refreshStatus()")
        expect(page.locator("#max-media")).to_have_value("50")
        expect(page.locator("#max-media")).to_be_focused()
        expect(page.locator("#monitor-reactions")).not_to_be_checked()
        expect(page.locator("#recheck-priority")).to_have_value("33")
        page.locator("#sources-tab-scope").click()
        page.locator("#sources-tab-recording").click()
        expect(page.locator("#max-media")).to_have_value("50")
        expect(page.locator("#recording-change-count")).to_contain_text("unsaved")
        hold_api_response(page, "/api/recording")
        page.locator("#recording-save").click()
        expect(page.locator("html")).to_have_attribute("data-acceptance-held", "true")
        page.locator("#max-media").fill("20")
        page.locator("#monitor-edits").uncheck()
        release_api_response(page)
        expect(page.locator("#recording-save")).to_be_enabled()
        expect(page.locator("#max-media")).to_have_value("20")
        expect(page.locator("#monitor-edits")).not_to_be_checked()
        assert server.app.state.store.get_setting("capture")["max_media_mb"] == 50
        assert server.app.state.store.get_setting("capture")["types"]["video"]["max_mb"] == 7
        assert server.app.state.store.get_setting("recheck_minutes") == 33
        page.locator("#recording-save").click()
        expect(page.locator("#recording-save")).to_be_disabled()
        expect(page.locator("#recording-change-count")).to_have_text("No unsaved changes")
        assert server.app.state.store.get_setting("capture")["max_media_mb"] == 20
        assert len(writes) == 2 and all(url.endswith("/api/recording") for url in writes), writes
        page.locator("#monitor-edits").check()
        page.locator("#recording-discard").click()
        expect(page.locator("#monitor-edits")).not_to_be_checked()
        expect(page.locator("#recording-discard")).to_be_disabled()
        expect(page.locator("#toast")).not_to_be_visible(timeout=10000)
        page.locator("#max-media").fill("2001")
        page.locator("#recording-save").click()
        assert not page.locator("#max-media").evaluate("field=>field.checkValidity()")
        assert len(writes) == 2
        page.locator("#recording-discard").click()
        expect(page.locator("#max-media")).not_to_have_attribute("aria-invalid", "true")
        expect(page.locator("#max-media-field-error")).to_have_count(0)

        checks = []
        for theme in ("light", "dark"):
            page.locator("html").evaluate("(root,theme)=>root.dataset.theme=theme", theme)
            for width in (1440, 390):
                page.set_viewport_size({"width": width, "height": 844})
                for tab in ("scope", "recording"):
                    page.locator("#sources-tab-" + tab).click()
                    page.evaluate("scrollTo(0,0)")
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"), (theme, width, tab)
                    height = page.locator("#view-sources").bounding_box()["height"]
                    assert height <= 3 * 844, (theme, width, tab, height)
                    page.screenshot(path=str(output / f"{tab}-{width}-{theme}.png"), full_page=True)
                    checks.append({"theme": theme, "width": width, "tab": tab, "height": height})

        page.set_viewport_size({"width": 1440, "height": 1000})
        page.locator("#sources-tab-recording").click()
        second = page.evaluate("json('profiles',{label:'Independent workspace'}).then(value=>value.id)")
        page.evaluate("loadProfiles()")
        page.locator("#max-media").fill("35")
        hold_api_response(page, "/api/recording")
        page.locator("#recording-save").click()
        expect(page.locator("html")).to_have_attribute("data-acceptance-held", "true")
        page.locator("#profile-select").select_option(second)
        expect(page.locator("#workspace")).to_have_js_property("inert", False)
        release_api_response(page)
        page.locator("#sources-tab-recording").click()
        expect(page.locator("#max-media")).to_have_value("20")
        expect(page.locator("#monitor-edits")).to_be_checked()
        expect(page.locator("#recording-save")).to_be_disabled()
        assert server.app.state.profiles.entries[second]["app"].state.store.get_setting("capture") is None
        token = page.evaluate("""json('access/grants',{label:'Source operator',permissions:['sources'],
            workspaces:{default:null}},{root:true}).then(value=>value.token)""")
        limited = browser.new_page(viewport={"width": 1440, "height": 1000})
        limited.on("pageerror", lambda error: errors.append(str(error)))
        limited.goto(server.url)
        limited.locator("#panel-token").fill(token)
        limited.get_by_role("button", name="Open workspace").click()
        expect(limited.locator("#workspace")).to_be_visible()
        limited.evaluate("sourcesReady")
        limited.locator('[data-view="sources"]').click()
        limited.locator("#sources-tab-recording").click()
        expect(limited.locator("#monitor-messages")).to_be_disabled()
        expect(limited.locator("#download-media")).to_be_disabled()
        expect(limited.locator("#recheck-priority")).to_be_enabled()
        limited.locator("#recheck-priority").fill("45")
        hold_api_response(limited, "/api/recording")
        limited.locator("#recording-save").click()
        expect(limited.locator("html")).to_have_attribute("data-acceptance-held", "true")
        limited.locator("#top-lock").click()
        release_api_response(limited)
        expect(limited.locator("#gate")).to_be_visible()
        expect(limited.locator("#recording-save")).to_be_disabled()
        assert limited.locator("#target-list").inner_text() == ""
        assert server.app.state.store.get_setting("recheck_minutes") == 45
        limited.close()
        assert not errors, errors
        server.app.state.store.verify(server.app.state.vault.public_key)
        (output / "checks.json").write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
        browser.close()
    print("Sources: atomic save, newer drafts, polling focus, workspace isolation and 390/1440px layouts passed.")


if __name__ == "__main__":
    main()
