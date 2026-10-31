"""Synthetic conversation controls and archive navigation; no Telegram requests."""
from pathlib import Path
import tempfile

from playwright.sync_api import expect, sync_playwright

from check_browser import RunningApp, launch_browser, unlock


def capture(page, point):
    output = Path('build/ux-review/after') / point
    output.mkdir(parents=True, exist_ok=True)
    for width, height in ((1440, 1000), (390, 844)):
        page.set_viewport_size({'width': width, 'height': height})
        page.evaluate("()=>{document.querySelector('.chats-shell').dataset.panel='chat';show('toast',false);const feed=document.querySelector('#chat-feed');feed.scrollTop=feed.scrollHeight;}")
        assert page.evaluate('()=>document.documentElement.scrollWidth<=innerWidth&&document.documentElement.scrollHeight<=innerHeight+1')
        page.mouse.move(0, 0)
        page.screenshot(path=str(output / f'chats-{width}.png'), animations='disabled')
    page.set_viewport_size({'width': 1440, 'height': 1000})


def main():
    with tempfile.TemporaryDirectory(prefix='chat-features-') as scratch, RunningApp(Path(scratch)) as server:
        store = server.app.state.store
        store.set_setting('capture', {'download_media': False})
        store.set_target(-1001, 'Research archive', 'supergroup', True)
        for mid in range(1, 501):
            store.append('message.new', {'text': f'Preserved message {mid}', 'sender_id': 44,
                'sender_observation': {'id': 44, 'display_name': 'Researcher', 'username': 'research_author'},
                'sent_at': f'2026-10-{20 + mid // 100:02}T10:00:00+00:00',
                'has_media': mid % 10 == 0, 'reply_to_message_id': 1 if mid == 500 else None}, -1001, mid, 44)
        store.append('message.edited', {'text': 'Edited reply', 'sender_id': 44, 'reply_to_message_id': 498}, -1001, 499, 44)
        with sync_playwright() as playwright:
            browser = launch_browser(playwright)
            page = browser.new_page(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
            errors, snapshots, connected, ai_calls = [], [], {'value': False, 'ai': False}, []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('request', lambda request: ai_calls.append(request.url) if '/api/analysis/' in request.url and request.method == 'POST' else None)

            def status(route):
                response = route.fetch()
                body = response.json()
                body['collector']['has_session'] = connected['value']
                body['analysis']['enabled'] = connected['ai']
                route.fulfill(response=response, json=body)

            def snapshot(route):
                snapshots.append(route.request.post_data_json)
                route.fulfill(json={'captured': 0})

            page.route('**/api/status', status)
            page.route('**/api/snapshot', snapshot)
            unlock(page, server)
            page.evaluate("async()=>{await navigate('chats');await openChat(-1001);}")
            expect(page.locator('#chat-sub')).to_contain_text('Group')
            expect(page.locator('#chat-compose')).to_be_hidden()
            expect(page.locator('#chat-load-history')).to_be_disabled()
            expect(page.locator('#chat-status').get_by_role('button', name='Connect account')).to_be_enabled()
            expect(page.locator('#chat-status').get_by_role('button', name='Start observation')).to_have_count(0)
            expect(page.locator('#chat-export-start')).to_have_attribute('aria-label', 'Export chat')
            expect(page.locator('.chat-mode-chips')).to_contain_text('Files off')
            page.locator('[data-recording="files"]').click()
            expect(page.locator('#capture-form')).to_be_visible()
            page.evaluate("()=>navigate('chats')")
            expect(page.locator('.chat-media-notice')).to_have_count(1)
            expect(page.locator('#msg-500 .reply-unavailable')).to_have_text('Reply to #1 · outside this loaded window')
            expect(page.locator('#msg-500 .reply-quote')).to_have_count(0)
            expect(page.locator('#msg-500 .media-missing')).to_have_attribute('aria-label', 'Attachment file not saved')
            expect(page.locator('.sender-details > summary').first).to_have_attribute('title', '@research_author')
            page.locator('.sender-details > summary').first.click()
            expect(page.locator('.sender-facts').first).to_contain_text('ID 44')
            page.locator('.sender-details > summary').first.click()
            page.locator('[data-chat-filter="edited"]').click()
            page.locator('#msg-499 .reply-quote').click()
            expect(page.locator('[data-chat-filter="all"]')).to_have_attribute('aria-pressed', 'true')
            expect(page.locator('#msg-498')).to_be_visible()
            page.locator('.chat-media-notice').get_by_role('button', name='File saving settings').click()
            expect(page.locator('#capture-form')).to_be_visible()
            page.evaluate("()=>navigate('chats')")
            expect(page.locator('.chat-filters [data-chat-filter]')).to_have_count(4)
            expect(page.locator('.chat-filters [data-chat-view]')).to_have_count(0)
            expect(page.locator('[data-chat-view="ai"]')).to_have_count(0)
            page.locator('[data-chat-filter="media"]').click()
            expect(page.locator('#chat-feed .msg')).to_have_count(6)
            assert page.locator('#chat-feed .msg').evaluate_all('rows=>rows.every(row=>row.querySelector(".media-missing"))')
            page.locator('[data-chat-view="people"]').click()
            expect(page.locator('#chat-feed .people')).to_be_visible()
            expect(page.locator('.chat-filter-row')).to_be_hidden()
            page.locator('[data-chat-view="profile"]').click()
            expect(page.locator('.chat-profile-view')).to_be_visible()
            expect(page.locator('.chat-profile-view')).to_contain_text('Profile not saved yet')
            page.route('**/api/chats/-1001/profile', lambda route: route.fulfill(status=503, json={'detail': 'Synthetic failure'}))
            page.evaluate('()=>loadChatProfile().catch(()=>{})')
            expect(page.locator('.chat-profile-view')).to_contain_text('Could not load data')
            expect(page.locator('.chat-profile-view')).not_to_contain_text('Profile not saved yet')
            page.unroute('**/api/chats/-1001/profile')
            page.locator('.chat-profile-view').get_by_role('button', name='Retry').click()
            expect(page.locator('.chat-profile-view')).to_contain_text('Profile not saved yet')
            page.locator('[data-chat-view="messages"]').click()
            expect(page.locator('[data-chat-filter="media"]')).to_have_attribute('aria-pressed', 'true')
            page.locator('[data-chat-filter="all"]').click()
            connected['ai'] = True
            page.evaluate('()=>refreshStatus()')
            page.locator('[data-chat-view="ai"]').click()
            expect(page.locator('#ask-chats input:checked')).to_have_value('-1001')
            expect(page.locator('#ask-question')).to_be_focused()
            assert not page.evaluate('()=>window.TgWitnessAnalysis.focusChat(999999)')
            expect(page.locator('#ask-chats input:checked')).to_have_value('-1001')
            assert not ai_calls, ai_calls
            connected['ai'] = False
            page.evaluate("async()=>{await refreshStatus();await navigate('chats');}")
            expect(page.locator('[data-chat-view="ai"]')).to_have_count(0)
            capture(page, '15-chat-views')
            connected['value'] = True
            page.evaluate('()=>refreshStatus()')
            expect(page.locator('#chat-load-history')).to_be_enabled()
            page.locator('#chat-history-limit').select_option('250')
            page.locator('#chat-load-history').click()
            expect(page.locator('#chat-load-history')).to_be_enabled()
            assert snapshots == [{'chat_id': -1001, 'limit': 250}]
            assert not errors, errors
            browser.close()
    print('Chat controls passed: named actions, recording links, account state and explicit history range.')


if __name__ == '__main__':
    main()
