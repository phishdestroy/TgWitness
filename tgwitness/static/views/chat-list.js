import {priorityHint} from "../components/priority.js?v=1";

export function createChatList({root, tr, node, icon, avatarNode, timeNode, getState, getSession,
  may, json, refreshStatus, openChat, toast, viewState, reload}) {
  const find = id => root.querySelector('#' + id), search = find('chat-search'), list = find('chats-list');
  const pageSize = 80, collator = new Intl.Collator(document.documentElement.lang || undefined, {numeric: true, sensitivity: 'base'});
  let visibleLimit = pageSize;
  const controls = node('div', 'chat-list-controls'), sortLabel = node('label', 'chat-list-sort');
  const views = node('div', 'chat-list-views'); views.setAttribute('role', 'group'); views.setAttribute('aria-label', tr('Filters'));
  const viewChoices = [
    ['all', tr('All'), tr('Chats')],
    ['priority', tr('Priority'), tr('Priority')],
    ['changes', tr('Changes'), tr('Edits') + ' · ' + tr('Deletions')],
    ['attention', tr('Needs attention'), tr('Access unconfirmed') + ' · ' + tr('Not found at recheck')],
  ];
  const viewButtons = new Map(viewChoices.map(([value, label, description]) => {
    const button = node('button', 'chat-list-view'), total = node('span', 'chat-list-view-count');
    button.type = 'button'; button.dataset.chatListView = value; button.title = description;
    total.setAttribute('aria-hidden', 'true'); button.append(node('span', '', label), total);
    button.addEventListener('click', () => {status.value = value === 'all' ? '' : value; changed();});
    views.append(button); return [value, {button, total, label}];
  }));
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
  const status = selectField('chat-list-state', 'State', [['', 'All'], ['changes', 'Changes'], ['attention', 'Needs attention'], ['active', 'Collecting'], ['loading', 'Loading history'], ['retry', 'Retry'], ['pending', 'Pending media'], ['failed', 'Failed media'], ['restricted', 'Restricted'], ['lost', 'Access to the chat lost'], ['auto', 'Auto-discovered'], ['unconfirmed', 'Access unconfirmed'], ['excluded', 'Excluded'], ['paused', 'Paused'], ['priority', 'Priority']]);
  const wait = node('p', 'chat-list-wait'); wait.hidden = true; wait.setAttribute('role', 'status');
  fields.prepend(sortLabel); filters.append(fields);
  const activeFilters = node('div', 'chat-list-active-filters'); activeFilters.setAttribute('role', 'group'); activeFilters.setAttribute('aria-label', tr('Filters'));
  const results = node('div', 'chat-list-results'), resultCount = node('span'), clear = node('button', 'text-link', tr('Clear filters'));
  resultCount.setAttribute('role', 'status'); resultCount.setAttribute('aria-atomic', 'true');
  clear.type = 'button'; clear.addEventListener('click', () => {resetFilters(); changed(); search.focus();});
  results.append(resultCount, clear);
  controls.append(views, filters, activeFilters, results); root.querySelector('.chat-search').after(controls);
  controls.after(wait);
  root.querySelector('.chats-sidebar').append(root.querySelector('.chat-open'));
  const more = node('button', 'chat-list-more', tr('Show more')); more.type = 'button';
  more.addEventListener('click', () => {
    const previous = new Set([...list.querySelectorAll('.chat-item')].map(row => row.dataset.chat));
    visibleLimit += pageSize; render();
    [...list.querySelectorAll('.chat-item')].find(row => !previous.has(row.dataset.chat))?.querySelector('.chat-choice').focus();
  });
  const pending = new Set();
  let session = getSession();
  const types = {channel: 'channel', broadcast: 'channel', supergroup: 'group', megagroup: 'group', group: 'group',
    chat: 'group', bot: 'bot', user: 'private', private: 'private'};
  function currentChats() {
    const state = getState(), targets = new Map((state.status?.targets || []).map(target => [target.chat_id, target]));
    const excluded = new Set(state.status?.scope?.exclude || []), sources = state.status?.collector?.source_status || {};
    return state.chats.map(saved => {
      const chat = {...saved, ...targets.get(saved.chat_id), known: targets.has(saved.chat_id)};
      chat.source = sources[String(chat.chat_id)];
      chat.collectionState = excluded.has(chat.chat_id) ? 'excluded' : !chat.enabled || !state.status?.collector?.running
        ? 'paused' : chat.source?.state === 'access_lost' ? 'lost' : chat.source?.state === 'access_unconfirmed' ? 'unconfirmed' : 'active';
      chat.observedTime = Date.parse(chat.last_message_at || chat.last_observed_at || '') || 0;
      return chat;
    });
  }
  const sourceOf = chat => chat.source;
  const queued = chat => (chat.media_queue?.pending || 0) + (chat.media_queue?.running || 0);
  const restrictions = chat => chat.telegram_restrictions?.length ? chat.telegram_restrictions
    : sourceOf(chat)?.state === 'restricted_by_telegram' ? sourceOf(chat).restriction || [{}] : [];
  function stateMatches(chat, mode) {
    if (mode === 'auto') return chat.origin === 'scope';
    if (mode === 'priority') return chat.priority;
    if (mode === 'pending') return queued(chat) > 0;
    if (mode === 'failed') return chat.media_queue?.failed > 0;
    if (mode === 'restricted') return restrictions(chat).length > 0;
    if (mode === 'loading') return !!chat.intake_state;
    if (mode === 'retry') return chat.intake_state === 'retry';
    if (mode === 'changes') return chat.edited > 0 || chat.deleted > 0;
    if (mode === 'attention') return ['access_unconfirmed', 'access_lost'].includes(sourceOf(chat)?.state)
      || chat.missing > 0 || chat.media_queue?.failed > 0 || chat.intake_state === 'retry' || restrictions(chat).length > 0;
    return chat.collectionState === mode;
  }
  const normalize = value => String(value).normalize('NFKC').toLocaleLowerCase();
  function matches(chat, terms) {
    const text = normalize(`${chat.title || ''} ${chat.chat_id}`);
    return terms.every(term => text.includes(term)) && (!kind.value || types[chat.kind] === kind.value);
  }
  function inView(chat, view) {return view === 'all' || stateMatches(chat, view);}
  function lostHint(chat) {
    return tr({no_access: 'The account can no longer read this chat', not_a_member: 'The account left or was removed'}[sourceOf(chat)?.reason] || 'Access to the chat lost');
  }
  function renderWait() {
    const until = getState().status?.collector?.activity?.telegram_pause_until;
    wait.hidden = !until;
    if (until) wait.textContent = tr('Telegram asked this account to wait until {time}. Saved chats stay readable.',
      {time: new Date(until * 1000).toLocaleTimeString(document.documentElement.lang || undefined)});
  }
  function compare(a, b) {
    const difference = sort.value === 'activity' ? b.observedTime - a.observedTime
      : sort.value === 'pending' ? queued(b) - queued(a)
      : sort.value === 'deleted' ? (b.deleted || 0) - (a.deleted || 0)
        : sort.value === 'edited' ? (b.edited || 0) - (a.edited || 0) : 0;
    return difference || collator.compare(a.title || String(a.chat_id), b.title || String(b.chat_id)) || a.chat_id - b.chat_id;
  }
  function place(parent, children) {
    const focused = parent.contains(document.activeElement) ? document.activeElement : null;
    const keep = new Set(children); for (const child of [...parent.children]) if (!keep.has(child)) child.remove();
    children.forEach((child, index) => {if (parent.children[index] !== child) parent.insertBefore(child, parent.children[index] || null);});
    if (focused && parent.contains(focused) && document.activeElement !== focused) focused.focus({preventScroll: true});
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
    const progress = node('span', 'chat-item-status'), state = chat.collectionState;
    const label = {excluded: 'Excluded', unconfirmed: 'Access unconfirmed', lost: 'Access to the chat lost', paused: 'Paused', active: 'Collecting'}[state];
    if (label) {
      const pill = node('span', 'pill pill-state' + (state === 'lost' ? ' pill-blocked' : ''), tr(label));
      if (state === 'lost') pill.title = lostHint(chat);
      progress.append(pill);
    }
    if (restrictions(chat).length) {
      const restricted = node('span', 'pill pill-state pill-blocked', tr('Restricted'));
      restricted.title = restrictions(chat).map(item => [item.platform, item.text || item.reason].filter(Boolean).join(': ')).filter(Boolean).join('\n') || tr('Blocked by Telegram');
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
    const terms = normalize(search.value).trim().split(/\s+/).filter(Boolean), candidates = currentChats().filter(chat => matches(chat, terms));
    for (const [value, {button, total, label}] of viewButtons) {
      const amount = candidates.filter(chat => inView(chat, value)).length;
      const formatted = amount.toLocaleString(); total.textContent = formatted;
      button.setAttribute('aria-pressed', String(value === (status.value || 'all'))); button.setAttribute('aria-label', label + ': ' + formatted);
    }
    const chats = candidates.filter(chat => !status.value || stateMatches(chat, status.value)).sort(compare);
    const existing = new Map([...list.children].map(row => [row.dataset.chat, row]));
    const focused = list.contains(document.activeElement) ? document.activeElement.closest('.chat-item')?.dataset.chat : null;
    const shown = chats.filter((chat, index) => index < visibleLimit || chat.chat_id === state.chat || String(chat.chat_id) === focused);
    const rows = shown.map(chat => {
      const row = existing.get(String(chat.chat_id)) || makeRow(chat), open = row.querySelector('.chat-choice'), star = row.querySelector('.chat-priority');
      const signature = JSON.stringify(chat);
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
      rows.push(empty);
    }
    if (shown.length < chats.length) rows.push(more);
    place(list, rows); renderWait(); const selected = Number(!!kind.value) + Number(!!status.value) + Number(sort.value !== 'activity');
    count.hidden = !selected; count.textContent = String(selected); summary.classList.toggle('filtered', !!selected);
    renderFilters();
    const amount = tr('{shown} of {total}', {shown: shown.length.toLocaleString(), total: chats.length.toLocaleString()});
    const text = tr('Chats') + ': ' + amount;
    if (resultCount.textContent !== text) resultCount.textContent = text;
    clear.hidden = !terms.length && !selected;
    results.hidden = !state.chats.length && !terms.length && !selected;
  }
  function renderFilters() {
    const chosen = [kind, status, sort].filter(field => field.value && (field !== sort || field.value !== 'activity'));
    const existing = new Map([...activeFilters.children].map(button => [button.dataset.field, button]));
    const chips = chosen.map(field => {
      let button = existing.get(field.id);
      if (!button) {
        button = node('button', 'chat-list-filter-chip'); button.type = 'button'; button.dataset.field = field.id;
        button.addEventListener('click', () => {field.value = field === sort ? 'activity' : ''; changed(); search.focus();});
      }
      const label = field.selectedOptions[0].textContent;
      button.textContent = label + ' ×'; button.setAttribute('aria-label', tr('Remove filter') + ': ' + label);
      return button;
    });
    place(activeFilters, chips); activeFilters.hidden = !chips.length;
  }
  function changed(replace = false) {visibleLimit = pageSize; render(); list.scrollTop = 0; window.TgWitnessRouter?.record({}, {replace});}
  function resetFilters() {
    search.value = ''; sort.value = 'activity'; kind.value = status.value = ''; visibleLimit = pageSize;
    filters.open = false; list.scrollTop = 0;
  }
  function resetSession() {
    session = getSession(); pending.clear(); resetFilters(); list.replaceChildren(); list.removeAttribute('aria-busy');
    activeFilters.replaceChildren(); activeFilters.hidden = true; resultCount.textContent = ''; results.hidden = true;
  }
  function snapshot() {return {chatFilter:status.value, chatSort:sort.value, chatKind:kind.value, chatQuery:search.value};}
  function restore(route) {
    if (session !== getSession()) resetSession();
    visibleLimit = pageSize;
    for (const [field, value, fallback] of [[status, route.chatFilter, ''], [sort, route.chatSort, 'activity'], [kind, route.chatKind, '']])
      field.value = [...field.options].some(option => option.value === value) ? value : fallback;
    search.value = route.chatQuery || ''; filters.open = !!(status.value || kind.value); render();
  }
  const plainKey = event => !event.defaultPrevented && !event.isComposing && !event.ctrlKey && !event.metaKey && !event.altKey && !event.shiftKey;
  search.addEventListener('input', () => changed(true));
  search.addEventListener('keydown', event => {
    if (!plainKey(event)) return;
    if (event.key === 'Escape' && search.value) {event.preventDefault(); event.stopPropagation(); search.value = ''; changed(true);}
    else if (['ArrowDown', 'ArrowUp', 'Enter'].includes(event.key)) {
      const choices = [...list.querySelectorAll('.chat-choice')], choice = event.key === 'ArrowUp' ? choices.at(-1) : choices[0];
      if (!choice) return;
      event.preventDefault();
      if (event.key === 'Enter') choice.click(); else choice.focus();
    }
  });
  list.addEventListener('keydown', event => {
    if (!plainKey(event) || !event.target.matches('.chat-choice, .chat-priority, .chat-list-more')) return;
    if (event.key === 'Escape') {event.preventDefault(); event.stopPropagation(); search.focus(); return;}
    const choices = [...list.querySelectorAll('.chat-choice, .chat-list-more')];
    const choice = event.target.closest('.chat-item')?.querySelector('.chat-choice') || event.target;
    const index = choices.indexOf(choice), next = {ArrowDown: index + 1, ArrowUp: index - 1, Home: 0, End: choices.length - 1}[event.key];
    if (next === undefined) return;
    event.preventDefault();
    if (next < 0) search.focus(); else choices[Math.min(next, choices.length - 1)]?.focus();
  });
  for (const field of [sort, kind, status]) field.addEventListener('change', () => changed());
  return {render, resetSession, snapshot, restore};
}
