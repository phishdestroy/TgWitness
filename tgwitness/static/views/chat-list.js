import {priorityHint} from "../components/priority.js?v=1";

export function createChatList({root, tr, node, icon, avatarNode, timeNode, getState, getSession,
  may, json, refreshStatus, openChat, toast, viewState, reload}) {
  const find = id => root.querySelector('#' + id), search = find('chat-search'), list = find('chats-list');
  const controls = node('div', 'chat-list-controls'), sortLabel = node('label', 'chat-list-sort');
  const sort = node('select'); sort.id = 'chat-list-sort';
  for (const [value, label] of [['activity', 'Recent activity'], ['pending', 'Most pending media'], ['deleted', 'Most deletions'], ['edited', 'Most edits'], ['name', 'Name']])
    sort.append(new Option(tr(label), value));
  sortLabel.append(node('span', '', tr('Sort')), sort);
  const filters = node('details', 'chat-list-filters'), summary = node('summary'), count = node('span', 'chat-filter-count');
  summary.append(icon('settings'), node('span', '', tr('Filters')), count); filters.append(summary);
  const fields = node('div', 'chat-list-filter-fields');
  function selectField(id, label, choices) {
    const labelNode = node('label'), select = node('select'); select.id = id;
    for (const [value, title] of choices) select.append(new Option(tr(title), value));
    labelNode.append(node('span', '', tr(label)), select); fields.append(labelNode); return select;
  }
  const kind = selectField('chat-list-kind', 'Type', [['', 'All'], ['channel', 'Channels'], ['group', 'Groups'], ['bot', 'Bots'], ['private', 'Private chats']]);
  const status = selectField('chat-list-state', 'State', [['', 'All'], ['active', 'Collecting'], ['loading', 'Loading history'], ['retry', 'Retry'], ['pending', 'Pending media'], ['failed', 'Failed media'], ['restricted', 'Restricted'], ['lost', 'Access to the chat lost'], ['auto', 'Auto-discovered'], ['unconfirmed', 'Access unconfirmed'], ['excluded', 'Excluded'], ['paused', 'Paused'], ['priority', 'Priority']]);
  fields.prepend(sortLabel); filters.append(fields); controls.append(filters); root.querySelector('.chat-search').after(controls);
  root.querySelector('.chats-sidebar').append(root.querySelector('.chat-open'));
  const pending = new Set();
  let session = getSession();
  const types = {channel: 'channel', broadcast: 'channel', supergroup: 'group', megagroup: 'group', group: 'group',
    chat: 'group', bot: 'bot', user: 'private', private: 'private'};
  function currentChats() {
    const state = getState(), targets = new Map((state.status?.targets || []).map(target => [target.chat_id, target]));
    return state.chats.map(chat => ({...chat, ...targets.get(chat.chat_id), known: targets.has(chat.chat_id)}));
  }
  function sourceState(chat) {
    const current = getState().status;
    if (current?.scope?.exclude?.includes(chat.chat_id)) return 'excluded';
    if (!chat.enabled || !current?.collector.running) return 'paused';
    if (current?.collector.source_status?.[String(chat.chat_id)]?.state === 'access_lost') return 'lost';
    if (current?.collector.source_status?.[String(chat.chat_id)]?.state === 'access_unconfirmed') return 'unconfirmed';
    return 'active';
  }
  const queued = chat => (chat.media_queue?.pending || 0) + (chat.media_queue?.running || 0);
  function stateMatches(chat, mode) {
    if (mode === 'auto') return chat.origin === 'scope';
    if (mode === 'priority') return chat.priority;
    if (mode === 'pending') return queued(chat) > 0;
    if (mode === 'failed') return chat.media_queue?.failed > 0;
    if (mode === 'restricted') return chat.telegram_restrictions?.length > 0;
    if (mode === 'loading') return !!chat.intake_state;
    if (mode === 'retry') return chat.intake_state === 'retry';
    return sourceState(chat) === mode;
  }
  function matches(chat) {
    const query = search.value.trim().toLocaleLowerCase(), mode = status.value;
    return (!query || `${chat.title || ''} ${chat.chat_id}`.toLocaleLowerCase().includes(query))
      && (!kind.value || types[chat.kind] === kind.value)
      && (!mode || stateMatches(chat, mode));
  }
  function compare(a, b) {
    const latest = value => Date.parse(value.last_message_at || value.last_observed_at || '') || 0;
    const difference = sort.value === 'activity' ? latest(b) - latest(a)
      : sort.value === 'pending' ? queued(b) - queued(a)
      : sort.value === 'deleted' ? (b.deleted || 0) - (a.deleted || 0)
        : sort.value === 'edited' ? (b.edited || 0) - (a.edited || 0) : 0;
    return difference || (a.title || String(a.chat_id)).localeCompare(b.title || String(b.chat_id)) || a.chat_id - b.chat_id;
  }
  function place(parent, children) {
    const keep = new Set(children); for (const child of [...parent.children]) if (!keep.has(child)) child.remove();
    children.forEach((child, index) => {if (parent.children[index] !== child) parent.insertBefore(child, parent.children[index] || null);});
  }
  function badge(className, label, value, symbol) {
    const chip = node('span', 'pill ' + className, String(value)); chip.title = label; chip.setAttribute('aria-label', label);
    if (symbol) chip.prepend(icon(symbol)); return chip;
  }
  function presentation(chat) {
    const title = chat.title || tr('Chat {id}', {id: chat.chat_id}), body = node('span', 'chat-item-body');
    const top = node('span', 'chat-item-top'), bottom = node('span', 'chat-item-bottom'), badges = node('span', 'chat-item-badges');
    top.append(node('span', 'chat-item-title', title));
    if (chat.priority) {const mark = icon('star'); mark.classList.add('chat-item-priority'); top.append(mark);}
    top.append(timeNode(chat.last_message_at || chat.last_observed_at, 'chat-item-time', 'list'));
    bottom.append(node('span', 'chat-item-preview', chat.last_text ? (chat.last_sender ? chat.last_sender + ': ' : '') + window.TgWitnessPrivacy.preview(chat.last_text)
      : tr(chat.messages ? 'Media or service message' : 'No messages saved yet')), badges);
    const deleted = typeof chat.deleted_saved === 'number' ? [chat.deleted_saved ? tr('{n} deleted, text kept', {n: chat.deleted_saved}) : '',
      chat.deleted_unsaved ? tr('{n} deleted before saving', {n: chat.deleted_unsaved}) : ''].filter(Boolean).join(', ') : tr('{n} deleted', {n: chat.deleted});
    if (chat.deleted) badges.append(badge('pill-deleted', deleted, chat.deleted, 'trash'));
    if (chat.missing) badges.append(badge('pill-missing', tr('{n} not found on recheck', {n: chat.missing}), chat.missing, 'question'));
    if (chat.edited) badges.append(badge('pill-edited', tr('{n} edited', {n: chat.edited}), chat.edited, 'edit'));
    const progress = node('span', 'chat-item-status'), state = sourceState(chat);
    const label = {excluded: 'Excluded', unconfirmed: 'Access unconfirmed', lost: 'Access to the chat lost', paused: 'Paused', active: 'Collecting'}[state];
    if (label) progress.append(node('span', 'pill pill-state', tr(label)));
    if (chat.telegram_restrictions?.length) {
      const restricted = node('span', 'pill pill-state', tr('Restricted'));
      restricted.title = chat.telegram_restrictions.map(item => [item.platform, item.text || item.reason].filter(Boolean).join(': ')).join('\n');
      progress.append(restricted);
    }
    if (chat.intake_state) {
      const intake = node('span', 'pill pill-state', tr(chat.intake_state === 'running' ? 'Loading history' : chat.intake_state === 'retry' ? 'Retry' : 'Queued'));
      if (chat.intake_state === 'retry') {
        intake.append(' · ', chat.intake_error_type || '');
        if (state === 'active') intake.append(' · ', timeNode(new Date(chat.intake_retry_at * 1000).toISOString(), '', 'list'));
      }
      progress.append(intake);
    }
    if (queued(chat)) progress.append(badge('pill-state', tr('Pending media'), tr('Pending media')+': '+queued(chat), 'download'));
    if (chat.media_queue?.failed) progress.append(badge('pill-deleted', tr('Failed media'), tr('Failed media')+': '+chat.media_queue.failed));
    body.append(top, bottom, progress); return [avatarNode(chat.chat_id, title), body];
  }
  async function priority(id) {
    const state = getState(), chat = currentChats().find(item => item.chat_id === id), current = getSession();
    if (!chat?.known || !may('sources') || state.status.demo || state.status.chats_limited || pending.has(id)) return;
    pending.add(id); render();
    try {
      await json('targets/priority', {chat_id: id, priority: !chat.priority});
      if (current !== getSession()) return;
      await refreshStatus(); render();
    } catch (error) {
      if (current === getSession() && error.name !== 'StaleView') toast(error.message, true);
    } finally {if (current === getSession()) {pending.delete(id); render();}}
  }
  function makeRow(chat) {
    const row = node('div', 'chat-item'), open = node('button', 'chat-choice'), star = node('button', 'chat-priority');
    row.dataset.chat = String(chat.chat_id); open.type = star.type = 'button';
    open.addEventListener('click', () => openChat(chat.chat_id).catch(error => {if (error.name !== 'StaleView') toast(error.message, true);}));
    star.append(icon('star')); star.addEventListener('click', () => priority(chat.chat_id));
    row.append(open, star); return row;
  }
  function render() {
    const state = getState(); if (state.view !== 'chats') return;
    if (session !== getSession()) resetSession();
    list.setAttribute('aria-busy', String(state.chatsLoading));
    const chats = currentChats().filter(matches).sort(compare), existing = new Map([...list.children].map(row => [row.dataset.chat, row]));
    const rows = chats.map(chat => {
      const row = existing.get(String(chat.chat_id)) || makeRow(chat), open = row.querySelector('.chat-choice'), star = row.querySelector('.chat-priority');
      const signature = JSON.stringify([chat, sourceState(chat)]);
      if (row.renderKey !== signature) {open.replaceChildren(...presentation(chat)); row.renderKey = signature;}
      row.classList.toggle('active', chat.chat_id === state.chat); open.setAttribute('aria-pressed', String(chat.chat_id === state.chat));
      open.title = [chat.title || tr('Chat {id}', {id: chat.chat_id}), chat.origin === 'scope' ? tr('Auto-discovered') : ''].filter(Boolean).join(' · ');
      star.hidden = !chat.known; star.disabled = !may('sources') || state.status.demo || state.status.chats_limited || pending.has(chat.chat_id);
      star.classList.toggle('on', !!chat.priority); star.setAttribute('aria-pressed', String(!!chat.priority));
      const label = priorityHint(tr, !!chat.priority, state.status?.collector) + ' — ' + (chat.title || chat.chat_id);
      star.title = label; star.setAttribute('aria-label', label); return row;
    });
    if (!state.chats.length && state.chatsLoading) {
      const loading = viewState('loading', tr('Loading…')), skeleton = node('div', 'chat-list-skeleton');
      skeleton.setAttribute('aria-hidden', 'true');
      for (let index = 0; index < 3; index++) skeleton.append(node('span'));
      loading.append(skeleton); rows.push(loading);
    } else if (!state.chats.length && state.chatsError) {
      rows.push(viewState('error', tr('Could not load data'), '', tr('Retry'), reload));
    } else if (!rows.length) {
      const empty = node('div', 'chats-none'); empty.append(node('p', 'hint', tr(!state.chats.length ? 'No chats chosen yet.'
        : kind.value || status.value ? 'No chats match these filters.' : 'No chats match your search.')));
      if (state.chats.length) {const clear = node('button', 'text-link', tr('Clear filters')); clear.type = 'button'; clear.addEventListener('click', () => {resetSession(); changed(); search.focus();}); empty.append(clear);}
      rows.push(empty);
    }
    place(list, rows); const selected = Number(!!kind.value) + Number(!!status.value);
    count.hidden = !selected; count.textContent = String(selected); summary.classList.toggle('filtered', !!selected);
  }
  function resetSession() {session = getSession(); pending.clear(); search.value = ''; sort.value = 'activity'; kind.value = status.value = ''; filters.open = false; list.replaceChildren(); list.removeAttribute('aria-busy');}
  function snapshot() {return {chatFilter:status.value, chatSort:sort.value, chatKind:kind.value, chatQuery:search.value};}
  function restore(route) {
    for (const [field, value, fallback] of [[status, route.chatFilter, ''], [sort, route.chatSort, 'activity'], [kind, route.chatKind, '']])
      field.value = [...field.options].some(option => option.value === value) ? value : fallback;
    search.value = route.chatQuery || ''; filters.open = !!(status.value || kind.value); render();
  }
  function changed(replace=false) {render(); window.TgWitnessRouter?.record({}, {replace});}
  search.addEventListener('input', () => changed(true));
  search.addEventListener('keydown', event => {if (event.key === 'Escape') {search.value = ''; changed(true);}});
  for (const field of [sort, kind, status]) field.addEventListener('change', () => changed());
  return {render, resetSession, snapshot, restore};
}
