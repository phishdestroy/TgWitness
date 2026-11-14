import hashlib
from html import escape
import json
from pathlib import Path
from urllib.parse import urlsplit

from .account_report import chat_note, reason_text, state_note
from .report import Words
from .telegram_export import MEDIA_PATH, dates, entity_spans, message, name

CSS = (Path(__file__).parent / 'static' / 'telegram-export.css').read_text(encoding='utf-8')
TAGS = {'bold': ('strong', ''), 'italic': ('em', ''), 'underline': ('u', ''),
        'strikethrough': ('s', ''), 'code': ('code', ''), 'pre': ('code', ' class="pre"'),
        'blockquote': ('span', ' class="quote"'), 'spoiler': ('span', ' class="spoiler" tabindex="0"')}


def e(value):
    return escape(str(value if value is not None else ''), quote=True)


def filename(page):
    return 'messages' + (str(page) if page > 1 else '') + '.html'


def safe_link(value):
    if not isinstance(value, str) or any(ord(char) < 32 for char in value):
        return None
    try:
        parsed = urlsplit(value)
        if parsed.scheme.lower() in ('http', 'https') and parsed.hostname:
            return value
        if parsed.scheme.lower() in ('mailto', 'tel', 'tg') and (parsed.path or parsed.netloc):
            return value
    except ValueError:
        pass
    return None


def formatted(text, entities):
    spans = []
    for start, end, value in entity_spans(text, entities):
        kind = value['type']
        tag, attributes = TAGS.get(kind, ('', ''))
        url = value.get('href') if kind == 'text_link' else text[start:end] if kind == 'link' else None
        if kind == 'email':
            url = 'mailto:' + text[start:end]
        elif kind == 'phone':
            url = 'tel:' + text[start:end]
        elif kind == 'mention':
            url = 'https://t.me/' + text[start:end].lstrip('@')
        if safe_link(url):
            tag, attributes = 'a', ' href="' + e(url) + '" rel="noreferrer noopener"'
        if tag:
            spans.append((start, end, tag, attributes))
    points = sorted({0, len(text), *(point for span in spans for point in span[:2])})
    parts = []
    for start, end in zip(points, points[1:]):
        active = sorted((span for span in spans if span[0] <= start and span[1] >= end), key=lambda span: (span[0], -span[1]))
        linked, tags = False, []
        for _, _, tag, attributes in active:
            if tag == 'a' and linked:
                continue
            linked |= tag == 'a'
            tags.append(tag)
            parts.append('<' + tag + attributes + '>')
        parts.append(e(text[start:end]))
        parts.extend('</' + tag + '>' for tag in reversed(tags))
    return ''.join(parts)


def avatar(label):
    initials = ''.join(part[0] for part in label.split()[:2]) or '?'
    tone = int(hashlib.sha256(label.encode()).hexdigest()[:2], 16) % 6
    return '<span class="avatar tone-' + str(tone) + '" aria-hidden="true">' + e(initials.upper()) + '</span>'


class View:
    def __init__(self, export):
        self.export = export
        self.say = Words(export.job['options'].get('report_language', 'en'))
        self.reply_cache = {}

    def head(self, title, prefix=''):
        say = self.say
        return ('<!doctype html><html lang="' + say.language + '" dir="' + say.direction + '"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                '<meta http-equiv="Content-Security-Policy" content="default-src &#39;none&#39;; '
                'style-src &#39;unsafe-inline&#39;; img-src &#39;self&#39; file:; media-src &#39;self&#39; file:; '
                'base-uri &#39;none&#39;; form-action &#39;none&#39;">'
                '<title>' + e(title) + ' · TgWitness</title><style>' + CSS + '</style></head><body>'
                '<header class="topbar"><a class="brand" href="' + prefix + 'export_results.html">TG / WITNESS</a>'
                '<nav aria-label="' + e(say('Files')) + '"><a href="' + prefix + 'index.html">' + e(say('Report'))
                + '</a><a href="' + prefix + 'map.html">' + e(say('Activity map')) + '</a>'
                + ('<a href="' + prefix + 'result.json" download>JSON</a>' if self.export.job['options'].get('export_format') == 'telegram_both' else '')
                + '<a href="' + prefix + 'index.html#verification">' + e(say('Verification')) + '</a></nav></header><main>').encode()

    def state(self, chat):
        states = self.export.states
        return states.get(chat['id'], 'missing') if states else 'complete'

    def index(self, selected):
        say = self.say
        yield self.head(say('Account export'))
        total = self.export.index.execute('SELECT COUNT(*) FROM messages').fetchone()[0]
        yield ('<header class="cover"><p class="eyebrow">Telegram · HTML</p><h1>' + e(say('Chats')) + '</h1>'
               '<p>' + e(say('Chats')) + ': <strong>' + str(len(selected)) + '</strong> · ' + e(say('Messages'))
               + ': <strong>' + str(total) + '</strong> · UTC</p><p class="muted">'
               + e(say('Read your chats offline. Open the report for charts, collection details and signature checks.')) + '</p></header><ul class="chat-list">').encode()
        for number, chat in enumerate(selected, 1):
            title = chat.get('title') or str(chat['id'])
            count = self.export.index.execute('SELECT COUNT(*) FROM messages WHERE chat=?', (chat['id'],)).fetchone()[0]
            state = self.state(chat)
            yield ('<li><a class="chat-row" href="chats/chat_' + f'{number:03d}' + '/messages.html">'
                   + avatar(title) + '<span class="chat-name" dir="auto">' + e(title) + '</span><span class="chat-count'
                   + ('' if state == 'complete' else ' gap') + '">'
                   + e(chat_note({'message_count': count, 'export_state': state}, say))
                   + '</span><span aria-hidden="true">›</span></a></li>').encode()
        yield ('</ul>' + ('<p class="empty">' + e(say('No messages')) + '</p>' if not selected else '')
               + '<footer>TgWitness · ' + e(say('A snapshot of history visible to this Telegram account during acquisition.'))
               + '</footer></main></body></html>').encode()

    def pager(self, page, pages):
        say = self.say
        return ('<nav class="pager" aria-label="' + e(say('Messages')) + '"><a href="../../export_results.html">← '
                + e(say('All chats')) + '</a><span class="page-number" dir="ltr">' + str(page) + ' / ' + str(pages) + '</span>'
                + ('<a rel="prev" href="' + filename(page - 1) + '">← ' + e(say('Previous')) + '</a>' if page > 1 else '')
                + ('<a rel="next" href="' + filename(page + 1) + '">' + e(say('Next')) + ' →</a>' if page < pages else '') + '</nav>')

    def reply(self, row, chat):
        reply = row.get('reply_to') or {}
        target = reply.get('reply_to_msg_id')
        if type(target) is not int:
            return ''
        peer = reply.get('reply_to_peer_id')
        peer_id = None
        if isinstance(peer, dict):
            for field, factor, offset in (('user_id', 1, 0), ('chat_id', -1, 0), ('channel_id', -1, -1000000000000)):
                if type(peer.get(field)) is int:
                    peer_id = peer[field] * factor + offset
        same_chat = not peer or peer_id == chat['id'] or peer == chat['id']
        found = self.export.index.execute('SELECT page,path,offset FROM messages WHERE chat=? AND id=?', (chat['id'], target)).fetchone() if same_chat else None
        label = e(self.say('Reply to')) + ' #' + str(target)
        if found:
            key = (chat['id'], target)
            if key not in self.reply_cache:
                with (self.export.directory / found[1]).open('rb') as stream:
                    stream.seek(found[2])
                    original = json.loads(stream.readline())
                sender = name(original.get('sender')) or self.say('Sender not available')
                text = ' '.join((original.get('text') or '').split())
                excerpt = text[:160] + ('…' if len(text) > 160 else '') if text else self.say('Media or service message')
                if len(self.reply_cache) >= 128:
                    self.reply_cache.pop(next(iter(self.reply_cache)))
                self.reply_cache[key] = '<strong dir="auto">' + e(sender) + '</strong><span dir="auto">' + e(excerpt) + '</span>'
            return '<a class="reply" href="' + filename(found[0]) + '#message' + str(target) + '" aria-label="' + label + '">' + self.reply_cache[key] + '</a>'
        return '<span class="reply muted">' + label + ' · ' + e(self.say('Original message is not included in this chat.')) + '</span>'

    def attachments(self, row, value):
        say = self.say
        parts = []
        labels = {'photo': 'Photo', 'video': 'Video', 'video_message': 'Video message', 'audio': 'Audio',
                  'voice': 'Voice message', 'document': 'File', 'sticker': 'Sticker', 'animation': 'GIF'}
        for attachment in row.get('attachments') or []:
            kind, path = attachment.get('kind'), attachment.get('file')
            label = say(labels.get(kind, 'Attachment'))
            if not isinstance(path, str) or not MEDIA_PATH.fullmatch(path):
                parts.append('<div class="attachment unavailable"><strong>' + e(label) + '</strong><span>'
                             + e(say('Attachment file not saved')) + '</span><small dir="auto">'
                             + e(reason_text(attachment.get('reason'), say) or attachment.get('outcome') or '') + '</small></div>')
                continue
            src = '../../' + path
            original = str(value.get('file_name') or '').replace('\\', '/').rsplit('/', 1)[-1]
            download = original or path.split('/')[-1]
            mime = value.get('mime_type') or ''
            if kind == 'photo' or kind == 'sticker' and mime in ('image/webp', 'image/png'):
                parts.append('<a class="photo" href="' + src + '"><img src="' + src + '" alt="' + e(label) + '" loading="lazy"></a>')
            elif kind in ('video', 'video_message', 'animation'):
                parts.append('<video controls preload="none" src="' + src + '" aria-label="' + e(label) + '"></video>')
            elif kind in ('voice', 'audio'):
                parts.append('<audio controls preload="none" src="' + src + '" aria-label="' + e(label) + '"></audio>')
            size = attachment.get('bytes')
            size_label = (' · ' + f'{size / 1048576:.1f} MiB' if size >= 1048576 else ' · ' + f'{size / 1024:.1f} KiB') if type(size) is int and size >= 0 else ''
            parts.append('<a class="attachment" href="' + src + '" download="' + e(download) + '"><strong dir="auto">'
                         + e(original or label) + '</strong><small>' + e(say('Download') + size_label) + '</small></a>')
        return ''.join(parts)

    def card(self, row, chat):
        say, value = self.say, message(row)
        sender = name(row.get('sender')) or (chat.get('title') if chat.get('kind') == 'channel' and row.get('post') else None)
        sender = sender or (str(row['from_id']) if row.get('from_id') else say('Sender not available'))
        at = value.get('date', '')
        identifier = str(row['id'])
        service = bool(row.get('action'))
        classes = 'message service' if service else 'message outgoing' if row.get('outgoing') else 'message incoming'
        parts = ['<article class="' + classes + '" id="message' + identifier + '">', avatar(sender),
                 '<div class="bubble"><div class="sender" dir="auto">' + e(sender) + '</div>']
        forward = value.get('forwarded_from')
        if forward:
            parts.append('<p class="forward">' + e(say('Forwarded from')) + ': <bdi>' + e(forward) + '</bdi></p>')
        parts.append(self.reply(row, chat))
        if service:
            labels = {'create_group': 'created the group', 'create_channel': 'created the channel',
                      'edit_group_title': 'changed the chat name', 'edit_group_photo': 'changed the chat photo',
                      'pin_message': 'pinned a message'}
            parts.append('<p class="service-label">' + e(say(labels.get(value.get('action'), 'Service message')))
                         + (' · <bdi>' + e(value['title']) + '</bdi>' if value.get('title') else '') + '</p>')
        parts.append(self.attachments(row, value))
        if row.get('text'):
            parts.append('<div class="message-text" dir="auto">' + formatted(row['text'], row.get('entities')) + '</div>')
        for field, label in (('poll', 'Poll'), ('contact_information', 'Contact'), ('location_information', 'Location')):
            detail = value.get(field)
            if detail:
                shown = str(detail.get('question') or '') if field == 'poll' else ' · '.join(str(v) for v in detail.values() if v is not None and v != '')
                parts.append('<div class="attachment"><strong>' + e(say(label)) + '</strong><span dir="auto">' + e(shown) + '</span></div>')
        if not row.get('text') and not row.get('attachments') and not service and not row.get('media'):
            parts.append('<p class="muted">' + e(say('(no text)')) + '</p>')
        parts.append('<div class="message-time">' + (e(say('Edited')) + ' · ' if value.get('edited') else '')
                     + '<a href="#message' + identifier + '" title="' + e(at + ' UTC · #' + identifier) + '">'
                     + '<time datetime="' + e(at + 'Z' if at else '') + '">' + e(at[11:] or '—') + '</time></a></div></div></article>')
        return ''.join(parts)

    def page(self, chat, batch, page, pages):
        title = chat.get('title') or str(chat['id'])
        note = state_note({'export_state': self.state(chat)}, self.say)
        yield self.head(title, '../../')
        yield ('<header class="chat-heading">' + avatar(title) + '<div><h1 dir="auto">' + e(title)
               + '</h1><p class="muted">Telegram · UTC</p></div></header>' + self.pager(page, pages)
               + ('<p class="chat-note">' + e(note) + '</p>' if note else '')
               + '<section class="conversation" aria-label="' + e(self.say('Messages')) + '">').encode()
        day = None
        for row in batch:
            current = dates(row.get('date')).get('date', '')[:10]
            if current != day:
                yield ('<div class="date-divider"><span>' + e(current or self.say('Not recorded')) + '</span></div>').encode()
                day = current
            yield self.card(row, chat).encode()
        if not batch and not note:
            yield ('<p class="empty">' + e(self.say('No message records are included in this view. Check the scope and omissions before drawing conclusions.')) + '</p>').encode()
        yield ('</section>' + self.pager(page, pages) + '<footer>TgWitness · <a href="../../chats/' + str(chat['id'])
               + '.html">' + e(self.say('Report')) + '</a> · <a href="../../index.html#coverage">' + e(self.say('Coverage')) + '</a></footer></main></body></html>').encode()
