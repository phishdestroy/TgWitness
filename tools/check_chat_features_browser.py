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
            errors, snapshots, connected = [], [], {'value': False}
            page.on('pageerror', lambda error: errors.append(str(error)))

            def status(route):
                response = route.fetch()
                body = response.json()
                body['collector']['has_session'] = connected['value']
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
            page.evaluate("()=>{const feed=document.querySelector('#chat-feed');feed.scrollTop=feed.scrollHeight;}")
            capture(page, '14-chat-content')
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
