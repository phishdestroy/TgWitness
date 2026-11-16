const KINDS = {channel: 'Channel', supergroup: 'Group', group: 'Group', bot: 'Bot', private: 'Private chat', user: 'Private chat'};

export function writable(chat) {
  return chat.kind !== 'channel' || ['creator', 'administrator'].includes(chat.role);
}

export function createChatPicker({tr, saved, dialogs, loadDialogs, avatar}) {
  let dialog = null, finish = null;
  const make = (tag, text = '', cls = '') => {const el = document.createElement(tag);if (text) el.textContent = text;if (cls) el.className = cls;return el;};
  function close(value = null) {
    const done = finish;finish = null;
    if (dialog?.open) dialog.close();
    dialog?.remove();dialog = null;
    done?.(value);
  }
  function choices(filter, exclude) {
    const known = new Map();
    for (const chat of dialogs() || []) known.set(chat.chat_id, {chat_id: chat.chat_id, title: chat.title, kind: chat.kind, role: chat.role});
    const merged = new Map();
    for (const chat of saved() || []) {
      const extra = known.get(chat.chat_id) || {};
      merged.set(chat.chat_id, {chat_id: chat.chat_id, title: chat.title || extra.title, kind: chat.kind || extra.kind, role: extra.role, saved: true});
    }
    for (const chat of known.values()) if (!merged.has(chat.chat_id)) merged.set(chat.chat_id, chat);
    return [...merged.values()].filter(chat => !exclude.includes(chat.chat_id) && filter(chat));
  }
  function pick({title, filter = () => true, exclude = [], opener = document.activeElement}) {
    close();
    return new Promise(resolve => {
      finish = value => {resolve(value);if (opener?.isConnected) opener.focus({preventScroll: true});};
      dialog = make('dialog', '', 'chat-picker-dialog');dialog.setAttribute('aria-labelledby', 'chat-picker-title');
      const head = make('div', '', 'chat-picker-head'), heading = make('h2', title);heading.id = 'chat-picker-title';
      const cancel = make('button', tr('Cancel'), 'quiet');cancel.type = 'button';cancel.addEventListener('click', () => close());
      head.append(heading, cancel);
      const search = make('input');search.type = 'search';search.placeholder = tr('Search chats');search.setAttribute('aria-label', tr('Search chats'));
      search.autocomplete = 'off';
      const status = make('p', '', 'hint chat-picker-status');status.setAttribute('role', 'status');
      const list = make('div', '', 'chat-picker-list');
      let loading = false, failed = '';
      function row(chat) {
        const name = chat.title || tr('Chat {id}', {id: chat.chat_id});
        const button = make('button', '', 'chat-picker-item');button.type = 'button';button.dataset.chat = String(chat.chat_id);
        const body = make('span', '', 'chat-picker-body');
        body.append(make('span', name, 'chat-picker-title'), make('span', tr(KINDS[chat.kind] || 'Chat') + (chat.saved ? ' · ' + tr('Saved') : ''), 'chat-picker-kind'));
        button.append(avatar(chat.chat_id, name), body);
        button.addEventListener('click', () => close({chat_id: chat.chat_id, title: name, kind: chat.kind}));
        return button;
      }
      function render() {
        if (!dialog) return;
        const words = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
        const found = choices(filter, exclude).filter(chat => words.every(word => (chat.title || '').toLowerCase().includes(word) || String(chat.chat_id).includes(word)));
        list.replaceChildren(...found.slice(0, 200).map(row));
        status.textContent = loading && !found.length ? tr('Loading chats…') : failed && !found.length ? failed
          : found.length ? '' : tr('No matching chats.');
      }
      search.addEventListener('input', render);
      search.addEventListener('keydown', event => {if (event.key === 'ArrowDown') {event.preventDefault();list.querySelector('button')?.focus();}});
      list.addEventListener('keydown', event => {
        const items = [...list.querySelectorAll('button')], index = items.indexOf(document.activeElement);
        if (event.key === 'ArrowDown' && index >= 0) {event.preventDefault();items[Math.min(index + 1, items.length - 1)].focus();}
        if (event.key === 'ArrowUp' && index >= 0) {event.preventDefault();(index ? items[index - 1] : search).focus();}
      });
      dialog.append(head, search, status, list);document.body.append(dialog);
      dialog.addEventListener('cancel', event => {event.preventDefault();close();});
      dialog.showModal();search.focus();render();
      if (!(dialogs() || []).length && loadDialogs) {
        const shown = dialog;loading = true;render();
        loadDialogs().catch(error => {failed = error.message;}).finally(() => {if (shown === dialog) {loading = false;render();}});
      }
    });
  }
  window.addEventListener('tgwitness:lock', () => close());
  return {pick, close};
}
