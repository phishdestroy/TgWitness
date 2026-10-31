"""Journal filters, navigation and evidence inspection on a synthetic local archive."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import expect, sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.check_browser import RunningApp, launch_browser, unlock, navigate_panel, check_layout
from test_collector import saved_session
from tgwitness import store as store_module

HARBOR, OTHER = -1001, -1002
SHOTS = Path("build/journal-review")


def seed(server):
    store = server.app.state.store
    server.app.state.vault.save("credentials", {"api_id": 123, "api_hash": "a" * 32, "session": saved_session()})
    store.set_setting("account", {"id": 44, "username": "synthetic"})
    for cid, title in ((HARBOR, "Harbor investigation"), (OTHER, 'Incident response <img src=x onerror="window.__journal_xss=1">')):
        store.set_target(cid, title, "supergroup", True)
    clock, now = store_module.utcnow, datetime.now(timezone.utc)
    try:
        for i in range(360):
            at = (now - timedelta(minutes=360-i)).isoformat(timespec="milliseconds")
            store_module.utcnow = lambda at=at: at
            cid = HARBOR if i % 2 == 0 else OTHER
            store.append("message.new", {"text": f"Invoice reference {i}. Original payment instructions.", "sender_id": 44}, cid, i, 44)
            if i % 3 == 0:
                store.append("message.edited", {"text": f"Invoice reference {i}. Changed payment instructions.", "sender_id": 44}, cid, i)
            if i % 7 == 0:
                store.append("message.deleted", {}, cid, i)
            if i % 9 == 0:
                store.append("media.skipped", {"reason": "media download disabled"}, cid, i)
                store.append("collector.heartbeat", {"running": True})
    finally:
        store_module.utcnow = clock
    original = store.append("message.new", {"text": "Captured evidence packet. Attachment receipt follows.", "sender_id": 44}, HARBOR, 900, 44)
    content = b"Synthetic evidence packet\n"
    digest = hashlib.sha256(content).hexdigest()
    directory = store.root / "media"
    directory.mkdir(exist_ok=True)
    (directory / digest).write_bytes(content)
    store.append("media.saved", {"message_event": original["seq"], "media_sha256": digest,
                                 "original_name": "packet.txt", "mime_type": "text/plain", "size": len(content)}, HARBOR, 900)


def params(page):
    return parse_qs(urlsplit(page.url).query)


def capture(page, prefix):
    SHOTS.mkdir(parents=True, exist_ok=True)
    for width, height in ((1440, 1000), (390, 844)):
        page.set_viewport_size({"width": width, "height": height})
        for theme in ("light", "dark"):
            page.evaluate("theme => document.documentElement.dataset.theme=theme", theme)
            page.evaluate("window.scrollTo(0,document.querySelector('#view-observations').getBoundingClientRect().top+scrollY-76)")
            check_layout(page)
            page.screenshot(path=str(SHOTS / f"{prefix}-{width}-{theme}.png"), animations="disabled")


def choose_source(page, name="Harbor", cid=HARBOR):
    page.locator("#journal-source-toggle").click()
    page.locator("#journal-source-search").fill(name)
    page.locator(f'.journal-source-option[data-source="{cid}"]').click()


def filters(page):
    page.locator('[data-filter="message.edited"]').click()
    page.locator('[data-filter="message.deleted"]').click()
    page.wait_for_function("()=>state.filter==='message.edited,message.deleted'&&state.events.every(e=>['message.edited','message.deleted'].includes(e.kind))")
    expect(page.locator("#journal-active-filters .journal-filter-chip")).to_have_count(2)
    choose_source(page)
    page.wait_for_function("()=>state.events.length>0&&state.events.every(e=>e.chat_id===-1001)")
    assert params(page)["source"] == [str(HARBOR)]
    page.go_back()
    expect(page.locator("#journal-source-toggle")).to_have_text("All sources")
    page.go_forward()
    expect(page.locator("#journal-source-toggle")).to_contain_text("Harbor investigation")
    page.locator('[data-range="1h"]').click()
    page.wait_for_function("()=>state.eventSince&&state.events.every(e=>Date.parse(e.observed_at)>=Date.parse(state.eventSince))")
    assert params(page)["since"][0].endswith("Z")
    page.locator('[data-range="custom"]').click()
    page.locator("#journal-since").fill("2026-11-01T12:00")
    page.locator("#journal-until").fill("2026-10-01T12:00")
    page.get_by_role("button", name="Apply dates", exact=True).click()
    expect(page.locator("#journal-filter-error")).to_be_visible()
    assert params(page)["since"][0] != "2026-11-01T12:00:00.000Z"
    page.locator("#journal-since").fill("")
    page.locator("#journal-until").fill("")
    page.get_by_role("button", name="Apply dates", exact=True).click()
    page.locator("#event-search").fill("invoice")
    page.wait_for_function("()=>new URL(location.href).searchParams.get('q')==='invoice'")
    expected = params(page)
    page.reload()
    expect(page.locator('#view-observations')).to_be_visible()
    expect(page.locator('[data-filter="message.edited"]')).to_have_attribute("aria-pressed", "true")
    expect(page.locator('[data-filter="message.deleted"]')).to_have_attribute("aria-pressed", "true")
    assert params(page) == expected
    page.locator("#event-search").fill("no-such-invoice-reference-xyz")
    expect(page.locator("#empty-events")).to_be_visible()
    page.locator("#empty-action").click()
    page.wait_for_function("()=>state.events.length>0&&!state.search&&!state.filter&&!state.source")
    page.locator("#journal-source-toggle").click()
    page.locator("#journal-source-search").fill("Incident response")
    expect(page.locator(".journal-source-options img")).to_have_count(0)
    page.keyboard.press("Escape")
    expect(page.locator("#journal-source-toggle")).to_be_focused()
    assert page.evaluate("window.__journal_xss") is None


def visuals(page):
    capture(page, "filters")
    page.locator("#journal-source-toggle").click()
    box = page.locator(".journal-source-picker").bounding_box()
    assert box and box["x"] >= 0 and box["x"]+box["width"] <= 390
    assert box["y"] >= 0 and box["y"]+box["height"] <= 844
    page.keyboard.press("Escape")


def routine_records(page):
    page.wait_for_function("()=>state.events.length>0&&state.events.every(e=>!['collector.heartbeat','host.state'].includes(e.kind)&&!(e.kind==='media.skipped'&&e.payload.reason==='media download disabled'))")
    toggle = page.locator(".journal-related").first
    expect(toggle).to_be_visible()
    toggle.click()
    expect(page.locator(".journal-related-row:visible")).to_have_count(1)
    expect(page.locator("#detail-drawer")).to_be_hidden()
    page.locator(".journal-related-row").click()
    expect(page.locator("#detail-drawer")).to_be_visible()
    expect(page.locator("#detail-title")).to_have_text("Attachment preserved")
    page.locator("#close-detail").click()
    page.locator("#journal-system").check()
    page.wait_for_function("()=>state.events.some(e=>e.kind==='collector.heartbeat')")
    assert params(page)["system"] == ["1"]
    page.go_back()
    expect(page.locator("#journal-system")).not_to_be_checked()
    page.wait_for_function("()=>state.events.every(e=>e.kind!=='collector.heartbeat')")
    result = page.evaluate("""async()=>{
      const {groupEvents}=await import('/components/journal.js?v=1');
      const m={seq:1,kind:'message.new',chat_id:-1001,message_id:7,payload:{text:'original'}};
      const media={seq:2,kind:'media.saved',chat_id:-1001,message_id:7,payload:{message_event:1}};
      const input=[media,m],before=JSON.stringify(input),group=groupEvents(input);
      if(group.length!==1||group[0].event.seq!==1||group[0].related[0].seq!==2)throw Error('pair lost');
      for(const other of [{...media,kind:'media.failed'},{...media,chat_id:-1002},{...media,payload:{message_event:4}}])
        if(groupEvents([other,m]).length!==2)throw Error('unrelated or failure was grouped');
      if(groupEvents([media,{...m,kind:'message.edited'}]).length!==2)throw Error('edit hidden');
      if(groupEvents([media,{seq:3,kind:'source.profile',payload:{}},m]).length!==3)throw Error('nonconsecutive grouping');
      return before===JSON.stringify(input);
    }""")
    assert result


def static_demo(browser, server):
    page = browser.new_page()
    fixture = {"/api/events": {"text": json.dumps({"events": [
        {"seq": 1, "kind": "message.new", "chat_id": HARBOR, "message_id": 1, "observed_at": "2026-10-30T12:00:00Z", "payload": {"text": "invoice"}},
        {"seq": 2, "kind": "media.saved", "chat_id": HARBOR, "message_id": 1, "observed_at": "2026-10-30T13:00:00Z", "payload": {}},
        {"seq": 3, "kind": "message.edited", "chat_id": OTHER, "message_id": 2, "observed_at": "2026-10-30T14:00:00Z", "payload": {"text": "invoice"}},
        {"seq": 4, "kind": "collector.heartbeat", "chat_id": None, "message_id": None, "observed_at": "2026-10-30T15:00:00Z", "payload": {}},
    ]})}}
    page.route("**/fixtures.json", lambda route: route.fulfill(json=fixture))
    page.route("**/demo/mock.js", lambda route: route.fulfill(path=str(Path("website/demo/mock.js")), content_type="text/javascript"))
    page.goto(server.url)
    page.add_script_tag(url=server.url + "/demo/mock.js")
    result = page.evaluate("async()=>await fetch('/api/events?kind=messages,media&since=2026-10-30T12:30:00Z').then(r=>r.json())")
    assert [event["seq"] for event in result["events"]] == [2]
    result = page.evaluate("async()=>await fetch('/api/events?hide_system=true&limit=1').then(r=>r.json())")
    assert [event["seq"] for event in result["events"]] == [3]
    page.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--visual-only", action="store_true")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="journal-ui-") as scratch, RunningApp(Path(scratch)) as app:
        seed(app)
        with sync_playwright() as playwright:
            browser = launch_browser(playwright)
            page = browser.new_page(viewport={"width": 1440, "height": 1000}, reduced_motion="reduce",
                                    permissions=["clipboard-read", "clipboard-write"])
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            unlock(page, app)
            navigate_panel(page, "observations")
            expect(page.locator('[data-filter="messages"]')).to_be_visible()
            if not args.visual_only:
                filters(page)
                page.set_viewport_size({"width": 1440, "height": 1000})
                routine_records(page)
            visuals(page)
            static_demo(browser, app)
            assert not errors, errors
            browser.close()
    print("Journal filters: groups, sources, dates, search, history, XSS and four viewport/theme captures passed.")


if __name__ == "__main__":
    main()
