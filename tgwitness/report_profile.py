import base64
import hashlib
import json
from html import escape
from pathlib import Path


CSS = Path(__file__).with_suffix('.css').read_text(encoding='utf-8')
SCRIPT = Path(__file__).with_suffix('.js').read_text(encoding='utf-8')
SCRIPT_HASH = "'sha256-" + base64.b64encode(hashlib.sha256(SCRIPT.encode('utf-8')).digest()).decode() + "'"
WORDS = ('Showing {shown} of {total} rows on this page', 'No matching rows on this page.',
         'Messages from {chat}', 'All chats', 'Copy table', 'Copied', 'Copy unavailable. Select the table to copy it.')


def opening(say, preview=False):
    labels = escape(json.dumps({key: say(key) for key in WORDS}, ensure_ascii=True), quote=True)
    controls = '' if preview else (
        '<div class="profile-tools no-print"><label><span>' + escape(say('Search this page'))
        + '</span><input type="search" class="profile-query" placeholder="' + escape(say('Search this page'))
        + '" autocomplete="off" disabled></label><button type="button" data-profile-theme disabled>'
        + escape(say('Theme')) + '</button><button type="button" data-profile-print disabled>'
        + escape(say('Print')) + '</button></div>')
    return '<div class="profile-report" data-profile-labels="' + labels + '">' + controls


def navigation(chapters, say):
    return ('<nav class="profile-index no-print" aria-label="' + escape(say('Contents')) + '">'
            + ''.join('<a href="#chapter-' + chapter.id + '"><span>' + escape(say(chapter.title))
                      + '</span><b hidden></b></a>' for chapter in chapters) + '</nav>')


def chapter_open(chapter, say):
    expanded = ' open' if chapter.id in ('activity', 'profiles', 'directory', 'journal') else ''
    return ('<details class="profile-section" id="chapter-' + chapter.id + '"' + expanded + '><summary><h2>'
            + escape(say(chapter.title)) + '</h2><span class="profile-count" hidden></span></summary>'
            '<div class="profile-section-body">')


def filters(say):
    return ('<div class="profile-filter-state no-print" hidden><span class="profile-scope"></span>'
            '<button type="button" data-profile-reset>' + escape(say('Reset filters')) + '</button>'
            '<button type="button" data-profile-all hidden>' + escape(say('Search all selected records'))
            + '</button><span class="profile-result" role="status" aria-live="polite"></span></div>')


def compact_analytics(markup, say):
    from .report_layouts import _Blocks, _children
    parser = _Blocks()
    parser.feed(markup)
    parser.close()
    parser._finish()
    output = []
    for tag, attrs, block in parser.blocks:
        if tag != 'section' or attrs.get('id') != 'report-analytics':
            output.append(block)
            continue
        figures, basis = [], []
        for child_tag, child_attrs, child in _children(block):
            classes = child_attrs.get('class', '').split()
            target = basis if child_tag == 'p' or any(key in classes for key in ('analytics-heading', 'analytics-totals')) else figures
            target.append(child)
        output.append(block.split('>', 1)[0] + '>' + ''.join(figures)
                      + '<details class="profile-chart-basis"><summary>' + escape(say('Source and counts'))
                      + '</summary>' + ''.join(basis) + '</details></section>')
    return ''.join(output)


def body(front, sections, chapters, replacements, say, preview=False):
    yield opening(say, preview)
    yield ''.join(front)
    yield navigation(chapters, say)
    if not preview:
        yield filters(say)
    for chapter in chapters:
        yield chapter_open(chapter, say)
        for key in chapter.section_ids:
            if key in replacements:
                if replacements[key] is not None:
                    yield from replacements[key]()
            else:
                for markup in sections.get(key, ()):
                    yield compact_analytics(markup, say) if key == 'analytics' else markup
        yield '</div></details>'
    yield '</div>'


def directories(events, titles, say, basis):
    from . import report, report_analytics
    chats, profiles = {}, {}
    for event in events:
        chat = report_analytics.chat_key(event)
        if chat is not None:
            chats[chat] = chats.get(chat, 0) + 1
        sender_id = report_analytics.sender_id(event)
        if sender_id is None:
            continue
        payload = event.get('payload') or {}
        sender = payload.get('sender_observation')
        sender = sender if isinstance(sender, dict) else {}
        if not any(key in sender for key in ('display_name', 'first_name', 'last_name', 'username')):
            continue
        display = sender.get('display_name') or ' '.join(str(sender.get(key) or '') for key in ('first_name', 'last_name')).strip()
        username = sender.get('username') or ''
        person = profiles.setdefault(sender_id, [])
        signature = (str(display), str(username))
        observed = event.get('observed_at')
        if not person or person[-1]['value'] != signature:
            person.append({'value': signature, 'first': observed, 'last': observed})
        else:
            person[-1]['last'] = observed
    chat_rows = []
    for chat, count in sorted(chats.items(), key=lambda item: (-item[1], str(item[0]))):
        title = titles.get(chat) or say('Chat {id}', id=chat)
        chat_rows.append('<tr data-profile-row><td>' + escape(str(title)) + '<small>' + escape(str(chat))
                         + '</small></td><td><a href="#chapter-journal" data-profile-chat="' + escape(str(chat))
                         + '" data-profile-chat-title="' + escape(str(title)) + '">' + report.num(count) + '</a></td></tr>')
    directory = ('<section id="observed-directory">' + basis + '<table><thead><tr><th>' + escape(say('Chat'))
                 + '</th><th>' + escape(say('Records')) + '</th></tr></thead><tbody>' + ''.join(chat_rows)
                 + '</tbody></table></section>')
    profile_rows = []
    for sender_id, versions in profiles.items():
        for version in versions:
            name, username = version['value']
            profile_rows.append('<tr data-profile-row><td><bdi>' + escape(name or say('User {id}', id=sender_id))
                                + '</bdi><small>' + escape(str(sender_id)) + '</small></td><td><bdi>'
                                + escape('@' + username if username else say('Not recorded')) + '</bdi></td><td>'
                                + report.when(version['first']) + '</td><td>' + report.when(version['last']) + '</td></tr>')
    profile = ('<section id="observed-profiles">' + basis + '<p class="profile-basis">'
               + escape(say('Names and usernames as observed in the selected records. Dates show observations, not registration or change dates.'))
               + '</p><table><thead><tr>' + ''.join('<th>' + escape(say(label)) + '</th>' for label in
                   ('Observed sender profile', 'Username', 'First observed', 'Last observed'))
               + '</tr></thead><tbody>' + ''.join(profile_rows) + '</tbody></table></section>')
    if not profile_rows:
        profile = '<p>' + escape(say('No sender profile observations in this reading copy.')) + '</p>'
    return {'directory': directory, 'profiles': profile}


def text_keys():
    import ast
    source = ast.parse(Path(__file__).read_text(encoding='utf-8'))
    keys = [node.args[0].value for node in ast.walk(source)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'say'
            and node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str)]
    return list(dict.fromkeys(keys + list(WORDS) + ['First observed', 'Last observed']))
