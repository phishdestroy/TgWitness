import {priorityHint} from "../components/priority.js?v=1";

export function createChatList({root, tr, node, icon, avatarNode, timeNode, getState, getSession,
  may, json, refreshStatus, openChat, toast, viewState, reload, adds = {}, secret = null, observation = null, startObservation = null}) {
  const find = id => root.querySelector('#' + id), search = find('chat-search'), list = find('chats-list');
  const pageSize = 80, collator = new Intl.Collator(document.documentElement.lang || undefined, {numeric: true, sensitivity: 'base'});
  let visibleLimit = pageSize;
  const controls = node('div', 'chat-list-controls'), sortLabel = node('label', 'chat-list-sort');
  const views = node('div', 'chat-list-views'); views.setAttribute('role', 'group'); views.setAttribute('aria-label', tr('Filters'));
  const viewChoices = [
    ['all', tr('All'), tr('Chats')],
    ['secret', tr('Pseudo-secret'), tr('Pseudo-secret')],
    ['priority', tr('Priority'), tr('Priority')],
    ['changes', tr('Changes'), tr('Edits') + ' · ' + tr('Deletions')],
    ['attention', tr('Needs attention'), tr('Access unconfirmed') + ' · ' + tr('Not found at recheck')],
  ];
  const viewButtons = new Map(viewChoices.map(([value, label, description]) => {
    const button = node('button', 'chat-list-view'), total = node('span', 'chat-list-view-count');
    button.type = 'button'; button.dataset.chatListView = value; button.title = description;
    total.setAttribute('aria-hidden', 'true'); button.append(node('span', '', label), total);
    if (value === 'secret') button.prepend(icon('lock'));
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
  const status = selectField('chat-list-state', 'State', [['', 'All'], ['changes', 'Changes'], ['attention', 'Needs attention'], ['active', 'Collecting'], ['loading', 'Loading history'], ['retry', 'Retry'], ['pending', 'Pending media'], ['failed', 'Failed media'], ['restricted', 'Restricted'], ['lost', 'Access to the chat lost'], ['auto', 'Auto-discovered'], ['unconfirmed', 'Access unconfirmed'], ['excluded', 'Excluded'], ['paused', 'Paused'], ['priority', 'Priority'], ['secret', 'Pseudo-secret']]);
  const wait = node('p', 'chat-list-wait'); wait.hidden = true; wait.setAttribute('role', 'status');
  const off = node('div', 'chat-list-off'), offStart = node('button', 'secondary small', tr('Start observation'));
  off.hidden = true; off.setAttribute('role', 'status'); offStart.type = 'button';
  off.append(icon('pause'), node('span', '', tr('Observation off')), offStart);
  offStart.addEventListener('click', () => startObservation?.());
  fields.prepend(sortLabel); filters.append(fields);
  const activeFilters = node('div', 'chat-list-active-filters'); activeFilters.setAttribute('role', 'group'); activeFilters.setAttribute('aria-label', tr('Filters'));
  const results = node('div', 'chat-list-results'), resultCount = node('span'), clear = node('button', 'text-link', tr('Clear filters'));
  resultCount.setAttribute('role', 'status'); resultCount.setAttribute('aria-atomic', 'true');
  clear.type = 'button'; clear.addEventListener('click', () => {resetFilters(); changed(); search.focus();});
  results.append(resultCount, clear);
  controls.append(views, filters, activeFilters, results); root.querySelector('.chat-search').after(controls);
  controls.after(off, wait);
  const linkBox = root.querySelector('.chat-open'); list.before(linkBox);
  const addButton = find('chats-manage'), addMenu = node('div', 'chat-add-menu');
  addMenu.id = 'chat-add-menu'; addMenu.hidden = true; addMenu.setAttribute('role', 'menu'); addMenu.setAttribute('aria-label', tr('Add'));
  addButton.replaceChildren(icon('plus')); addButton.title = tr('Add'); addButton.setAttribute('aria-label', tr('Add'));
  addButton.setAttribute('aria-haspopup', 'menu'); addButton.setAttribute('aria-expanded', 'false'); addButton.setAttribute('aria-controls', addMenu.id);
  addButton.after(addMenu);
  const addChoices = () => [
    ['sources', tr('Add a chat or channel'), adds.chooseChats, adds.canChoose],
    ['link', tr('Open Telegram link'), () => openLink(''), adds.canOpenLink],
    ['lock', tr('Pseudo-secret') + ' · ' + tr('Start chat'), adds.startSecret, adds.canSecret],
  ].filter(([, , run, allowed]) => run && allowed?.());
  function closeAdd(restore) {
    if (addMenu.hidden) return;
    addMenu.hidden = true; addButton.setAttribute('aria-expanded', 'false');
    if (restore) addButton.focus({preventScroll: true});
  }
  function openAdd() {
    addMenu.replaceChildren(...addChoices().map(([symbol, label, run]) => {
      const item = node('button', 'chat-add-item'); item.type = 'button'; item.setAttribute('role', 'menuitem');
      item.append(icon(symbol), node('span', '', label));
      item.addEventListener('click', () => {closeAdd(false); run();});
      return item;
    }));
    addMenu.hidden = false; addButton.setAttribute('aria-expanded', 'true');
    addMenu.querySelector('button')?.focus();
  }
  addButton.addEventListener('click', () => addMenu.hidden ? openAdd() : closeAdd(false));
  addMenu.addEventListener('keydown', event => {
    const items = [...addMenu.querySelectorAll('button')], index = items.indexOf(document.activeElement);
    const next = {ArrowDown: index + 1, ArrowUp: index - 1, Home: 0, End: items.length - 1}[event.key];
    if (event.key === 'Escape') {event.preventDefault(); event.stopPropagation(); closeAdd(true);}
    else if (event.key === 'Tab') closeAdd(false);
    else if (next !== undefined) {event.preventDefault(); items[(next + items.length) % items.length]?.focus();}
  });
  document.addEventListener('pointerdown', event => {if (!addMenu.hidden && !addMenu.contains(event.target) && !addButton.contains(event.target)) closeAdd(false);});
  function openLink(text, preview = false) {
    linkBox.open = true;
    const input = linkBox.querySelector('input');
    if (text) input.value = text;
    input.focus(); linkBox.scrollIntoView({block: 'nearest'});
    if (preview && text) linkBox.querySelector('form')?.requestSubmit();
  }
  const linkLike = text => /^(@[\w]{3,}|[\w]{5,}|(https?:\/\/)?(t|telegram)\.me\/\S+|tg:\/\/\S+)$/i.test(text);
  const kindWords = {channel: 'Channel', broadcast: 'Channel', supergroup: 'Group', megagroup: 'Group', group: 'Group', chat: 'Group',
    bot: 'Bot', user: 'Private chat', private: 'Private chat'};
  let dialogsFor = null, dialogsLoading = false, dialogsError = '', linkRow = null;
  const dialogRows = new Map(), section = node('p', 'chat-list-section', tr('In Telegram'));
  function ensureDialogs() {
    const current = getSession();
    if (dialogsFor === current || dialogsLoading || !adds.loadDialogs) return;
    if ((adds.dialogs?.() || []).length) {dialogsFor = current; return;}
    dialogsLoading = true; dialogsError = '';
    adds.loadDialogs().then(() => {if (current === getSession()) dialogsFor = current;})
      .catch(error => {if (current === getSession() && error.name !== 'StaleView') {dialogsFor = current; dialogsError = error.message;}})
      .finally(() => {if (current === getSession()) {dialogsLoading = false; render();}});
  }
  async function watch(dialog, button) {
    const current = getSession(); button.disabled = true;
    try {
      await adds.watch(dialog.chat_id);
      if (current !== getSession()) return;
      search.value = ''; changed(true);
      await openChat(dialog.chat_id);
    } catch (error) {
      if (current === getSession() && error.name !== 'StaleView') toast(error.message, true);
    } finally {if (button.isConnected) button.disabled = false;}
  }
  function dialogRow(dialog) {
    const row = node('div', 'chat-item chat-item-new'), open = node('button', 'chat-choice'), add = node('button', 'primary small chat-watch', tr('Add'));
    open.type = add.type = 'button'; row.dataset.dialog = String(dialog.chat_id);
    const title = dialog.title || tr('Chat {id}', {id: dialog.chat_id}), body = node('span', 'chat-item-body');
    const top = node('span', 'chat-item-top'), bottom = node('span', 'chat-item-bottom');
    top.append(node('span', 'chat-item-title', title));
    bottom.append(node('span', 'chat-item-preview', tr(kindWords[dialog.kind] || 'Channel')));
    body.append(top, bottom); open.append(avatarNode(dialog.chat_id, title), body);
    add.setAttribute('aria-label', tr('Add') + ': ' + title);
    open.addEventListener('click', () => watch(dialog, add));
    add.addEventListener('click', () => watch(dialog, add));
    row.append(open, add); return row;
  }
  let globalFor = '', globalResults = [], globalLoading = false, globalError = '', globalTimer = null, globalRequest = 0;
  const globalSection = node('p', 'chat-list-section', tr('Global search')), globalRows = new Map();
  function ensureGlobal(query) {
    const text = query.replace(/^@/, '').trim(), key = getSession() + '\n' + text;
    if (!adds.searchTelegram || text.length < 2) {clearTimeout(globalTimer); globalRequest++; globalFor = ''; globalResults = []; globalLoading = false; globalError = ''; return;}
    if (globalFor === key) return;
    clearTimeout(globalTimer);
    const request = ++globalRequest, current = getSession();
    globalFor = key; globalResults = []; globalError = ''; globalLoading = true;
    globalTimer = setTimeout(() => {
      adds.searchTelegram(text).then(result => {if (request === globalRequest && current === getSession()) globalResults = result.results || [];})
        .catch(error => {if (request === globalRequest && current === getSession() && error.name !== 'StaleView') globalError = error.message;})
        .finally(() => {if (request === globalRequest && current === getSession()) {globalLoading = false; render();}});
    }, 400);
  }
  async function join(result, button) {
    const current = getSession(); button.disabled = true;
    try {
      const done = await adds.join(result.username);
      if (current !== getSession() || !done?.chat_id) return;
      search.value = ''; changed(true);
      await openChat(done.chat_id);
    } catch (error) {
      if (current === getSession() && error.name !== 'StaleView') toast(error.message, true);
    } finally {if (button.isConnected) button.disabled = false;}
  }
  function globalRow(result) {
    const row = node('div', 'chat-item chat-item-new'), open = node('button', 'chat-choice');
    const title = result.title || (result.username ? '@' + result.username : tr('Chat {id}', {id: result.chat_id}));
    const joinable = !result.member && !!result.username && ['channel', 'supergroup', 'group'].includes(result.kind);
    const person = !result.member && !!result.username && !joinable;
    const add = node('button', 'primary small chat-watch', tr(joinable ? 'Join / open' : person ? 'Open' : 'Add'));
    open.type = add.type = 'button'; row.dataset.dialog = String(result.chat_id);
    const body = node('span', 'chat-item-body'), top = node('span', 'chat-item-top'), bottom = node('span', 'chat-item-bottom');
    top.append(node('span', 'chat-item-title', title));
    if (result.verified) top.append(icon('check'));
    const facts = [tr(kindWords[result.kind] || 'Channel'), result.username ? '@' + result.username : '',
      result.participants_count != null ? tr('Members') + ': '
        + Number(result.participants_count).toLocaleString(document.documentElement.lang || undefined) : '',
      result.scam ? 'SCAM' : result.fake ? 'FAKE' : ''].filter(Boolean);
    bottom.append(node('span', 'chat-item-preview', facts.join(' · ')));
    body.append(top, bottom); open.append(avatarNode(result.chat_id, title), body);
    add.setAttribute('aria-label', add.textContent + ': ' + title);
    const choose = joinable ? () => join(result, add) : person ? () => openLink('@' + result.username, true) : () => watch(result, add);
    if (!result.member && (!result.username || !adds.canJoin?.())) add.disabled = true;
    else {open.addEventListener('click', choose); add.addEventListener('click', choose);}
    row.append(open, add); return row;
  }
  function searchExtras(terms, query) {
    const extras = [];
    if (adds.canWatch?.()) {
      ensureDialogs();
      const saved = new Set(getState().chats.map(chat => chat.chat_id));
      const found = (adds.dialogs?.() || []).filter(dialog => !saved.has(dialog.chat_id)
        && matches({title: dialog.title, chat_id: dialog.chat_id, kind: dialog.kind}, terms)).slice(0, 30);
      if (found.length || dialogsLoading || dialogsError) extras.push(section);
      if (dialogsLoading && !found.length) extras.push(node('p', 'hint chat-list-searching', tr('Loading…')));
      else if (dialogsError && !found.length) extras.push(node('p', 'hint chat-list-searching', dialogsError));
      extras.push(...found.map(dialog => {
        if (!dialogRows.has(dialog.chat_id)) dialogRows.set(dialog.chat_id, dialogRow(dialog));
        return dialogRows.get(dialog.chat_id);
      }));
      ensureGlobal(query);
      const listed = new Set(found.map(dialog => dialog.chat_id));
      const global = globalResults.filter(result => !saved.has(result.chat_id) && !listed.has(result.chat_id)
        && (!kind.value || types[result.kind] === kind.value));
      if (global.length || globalLoading || globalError) extras.push(globalSection);
      if (globalLoading && !global.length) extras.push(node('p', 'hint chat-list-searching', tr('Loading…')));
      else if (globalError && !global.length) extras.push(node('p', 'hint chat-list-searching', globalError));
      extras.push(...global.map(result => {
        const key = JSON.stringify(result);
        if (globalRows.get(result.chat_id)?.key !== key) globalRows.set(result.chat_id, {key, row: globalRow(result)});
        return globalRows.get(result.chat_id).row;
      }));
    }
    if (linkLike(query) && adds.canOpenLink?.()) {
      if (linkRow?.dataset.query !== query) {
        linkRow = node('button', 'chat-search-link'); linkRow.type = 'button'; linkRow.dataset.query = query;
        linkRow.append(icon('link'), node('span', '', tr('Open Telegram link') + ': ' + query));
        linkRow.addEventListener('click', () => openLink(query, true));
      }
      extras.push(linkRow);
    }
    return extras;
  }
  let secretItems = [], secretAt = 0, secretBusy = false;
  function loadSecret() {
    if (!secret?.allowed() || secretBusy || Date.now() - secretAt < 30000) return;
    const owner = getSession(); secretBusy = true; secretAt = Date.now();
    secret.load().then(result => {
      if (owner !== getSession()) return;
      secretItems = secretThreads(result); render();
    }).catch(() => {}).finally(() => {if (owner === getSession()) secretBusy = false;});
  }
  function secretThreads(result) {
    const map = new Map(), people = result?.people || {}, enabled = !!result?.settings?.enabled;
    const entry = id => {if (!map.has(id)) map.set(id, {id, peer: null, state: null, last: '', text: '', out: false}); return map.get(id);};
    for (const snapshot of result?.chats || []) Object.assign(entry(snapshot.id), {peer: snapshot.peer_user_id, state: snapshot.state});
    for (const record of result?.records || []) {
      const p = record.payload || {}, id = p.secret_chat_id;
      if (id === undefined || id === null) continue;
      const item = entry(id); item.peer = item.peer || p.peer_user_id || null;
      if (record.kind === 'secret_chat.closed') item.state = item.state || 'closed';
      if (String(record.observed_at || '') >= item.last) item.last = record.observed_at || item.last;
      if (record.kind === 'secret_chat.message') {item.text = p.text || (p.media ? tr('Attachment') : item.text); item.out = p.direction === 'out';}
    }
    return [...map.values()].map(item => {
      const person = people[item.peer], title = person?.name || (person?.username ? '@' + person.username : tr('User ID {id}', {id: item.peer ?? '?'}));
      return {secret: true, secretId: item.id, chat_id: 's' + item.id, kind: 'private', title, search: [title, person?.username || '', item.peer || ''].join(' '),
        state: item.state === 'closed' ? 'closed' : !enabled ? 'paused' : item.state, last_message_at: item.last, observedTime: Date.parse(item.last || '') || 0,
        last_text: item.text, out: item.out};
    });
  }
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
    if (chat.secret || mode === 'secret') return !!chat.secret && mode === 'secret';
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
    const text = normalize(chat.secret ? chat.search : `${chat.title || ''} ${chat.chat_id}`);
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
    if (chat.origin === 'scope') top.append(node('span', 'visually-hidden', ' · ' + tr('Auto-discovered')));
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
    const running = !!getState().status?.collector?.running;
    const label = {excluded: 'Excluded', unconfirmed: 'Access unconfirmed', lost: 'Access to the chat lost', paused: running ? 'Paused' : ''}[state];
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
    body.append(top, bottom); if (progress.children.length) body.append(progress);
    return [avatarNode(chat.chat_id, title), body];
  }
  function secretPresentation(chat) {
    const body = node('span', 'chat-item-body'), top = node('span', 'chat-item-top'), bottom = node('span', 'chat-item-bottom');
    const title = node('span', 'chat-item-title'), lock = icon('lock'), face = avatarNode(null, chat.title);
    lock.classList.add('chat-item-lock'); title.append(lock, document.createTextNode(chat.title));
    face.classList.add('secret-face'); face.replaceChildren(icon('lock'));
    top.append(title, timeNode(chat.last_message_at, 'chat-item-time', 'list'));
    bottom.append(node('span', 'chat-item-preview', chat.last_text ? (chat.out ? tr('You') + ': ' : '') + window.TgWitnessPrivacy.preview(chat.last_text) : tr('No messages saved yet')));
    body.append(top, bottom);
    const word = {requested: 'Waiting for the other side', pending: 'Request received', closed: 'Ended', paused: 'Paused'}[chat.state];
    if (word) {const progress = node('span', 'chat-item-status'); progress.append(node('span', 'pill pill-state', tr(word))); body.append(progress);}
    return [face, body];
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
    if (chat.secret) row.classList.add('secret');
    const run = chat.secret ? () => secret.open(chat.secretId) : () => openChat(chat.chat_id);
    open.addEventListener('click', () => run().catch(error => {if (error.name !== 'StaleView') toast(error.message, true);}));
    open.addEventListener('pointerenter', event => {
      const name = open.querySelector('.chat-item-title');
      if (event.pointerType === 'mouse' && name && name.scrollWidth > name.clientWidth) open.title = name.textContent; else open.removeAttribute('title');
    });
    star.append(icon('star')); star.addEventListener('click', () => priority(chat.chat_id));
    row.append(open, star); return row;
  }
  function render() {
    const state = getState(); if (state.view !== 'chats') return;
    if (session !== getSession()) resetSession();
    list.setAttribute('aria-busy', String(state.chatsLoading));
    loadSecret();
    const secrets = secret?.allowed() ? secretItems : [];
    const terms = normalize(search.value).trim().split(/\s+/).filter(Boolean), candidates = [...currentChats(), ...secrets].filter(chat => matches(chat, terms));
    for (const [value, {button, total, label}] of viewButtons) {
      const amount = candidates.filter(chat => inView(chat, value)).length, pressed = value === (status.value || 'all');
      const formatted = amount.toLocaleString(); total.textContent = formatted;
      button.hidden = value !== 'all' && !pressed && !amount;
      button.setAttribute('aria-pressed', String(pressed)); button.setAttribute('aria-label', label + ': ' + formatted);
    }
    const watch = observation?.() || {};
    off.hidden = !watch.off || !state.chats.length; offStart.disabled = !watch.canStart;
    addButton.hidden = !addChoices().length;
    const chats = candidates.filter(chat => !status.value || stateMatches(chat, status.value)).sort(compare);
    const existing = new Map([...list.children].map(row => [row.dataset.chat, row]));
    const focused = list.contains(document.activeElement) ? document.activeElement.closest('.chat-item')?.dataset.chat : null;
    const shown = chats.filter((chat, index) => index < visibleLimit || chat.chat_id === state.chat || String(chat.chat_id) === focused);
    const rows = shown.map(chat => {
      const row = existing.get(String(chat.chat_id)) || makeRow(chat), open = row.querySelector('.chat-choice'), star = row.querySelector('.chat-priority');
      const signature = JSON.stringify([chat, !!state.status?.collector?.running]);
      if (row.renderKey !== signature) {open.replaceChildren(...(chat.secret ? secretPresentation(chat) : presentation(chat))); row.renderKey = signature;}
      row.classList.toggle('active', chat.chat_id === state.chat); open.setAttribute('aria-pressed', String(chat.chat_id === state.chat));
      star.hidden = !chat.known; star.disabled = !may('sources') || state.status.demo || state.status.chats_limited || pending.has(chat.chat_id);
      star.classList.toggle('on', !!chat.priority); star.setAttribute('aria-pressed', String(!!chat.priority));
      const label = priorityHint(tr, !!chat.priority, state.status?.collector) + ' — ' + (chat.title || chat.chat_id);
      star.title = label; star.setAttribute('aria-label', label); return row;
    });
    const extras = terms.length ? searchExtras(terms, search.value.trim()) : [];
    if (!state.chats.length && state.chatsLoading) {
      const loading = viewState('loading', tr('Loading…')), skeleton = node('div', 'chat-list-skeleton');
      skeleton.setAttribute('aria-hidden', 'true');
      for (let index = 0; index < 3; index++) skeleton.append(node('span'));
      loading.append(skeleton); rows.push(loading);
    } else if (!state.chats.length && state.chatsError) {
      rows.push(viewState('error', tr('Could not load data'), '', tr('Retry'), reload));
    } else if (!rows.length && !extras.length) {
      const fresh = !state.chats.length && !secrets.length && !terms.length, query = search.value.trim();
      const empty = node('div', 'chats-none' + (fresh ? ' fresh' : ''));
      if (fresh) {const mark = node('span', 'chats-none-mark'); mark.append(icon('message')); empty.append(mark);}
      empty.append(node('p', 'hint', tr(fresh ? 'No chats chosen yet.'
        : kind.value || status.value ? 'No chats match these filters.' : 'No chats match your search.')));
      const step = fresh && adds.canChoose?.() ? [tr('Add a chat or channel'), adds.chooseChats, 'primary']
        : linkLike(query) && adds.canOpenLink?.() ? [tr('Open Telegram link') + ': ' + query, () => openLink(query), 'secondary'] : null;
      if (step) {const go = node('button', step[2] + ' small', step[0]); go.type = 'button'; go.addEventListener('click', step[1]); empty.append(go);}
      rows.push(empty);
    }
    if (shown.length < chats.length) rows.push(more);
    rows.push(...extras);
    place(list, rows); renderWait(); const selected = Number(!!kind.value) + Number(!!status.value) + Number(sort.value !== 'activity');
    count.hidden = !selected; count.textContent = String(selected); summary.classList.toggle('filtered', !!selected);
    renderFilters();
    const amount = tr('{shown} of {total}', {shown: shown.length.toLocaleString(), total: chats.length.toLocaleString()});
    const text = tr('Chats') + ': ' + amount;
    if (resultCount.textContent !== text) resultCount.textContent = text;
    clear.hidden = !terms.length && !selected;
    results.hidden = !terms.length && !selected;
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
    secretItems = []; secretAt = 0; secretBusy = false; closeAdd(false); linkBox.open = false;
    dialogRows.clear(); linkRow = null; dialogsError = ''; dialogsLoading = false; dialogsFor = null;
    clearTimeout(globalTimer); globalRequest++; globalRows.clear(); globalFor = ''; globalResults = []; globalLoading = false; globalError = '';
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
      const choices = [...list.querySelectorAll(event.key === 'Enter' ? '.chat-item:not(.chat-item-new) .chat-choice' : '.chat-choice')];
      const choice = event.key === 'ArrowUp' ? choices.at(-1) : choices[0];
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
  return {render, resetSession, snapshot, restore, openLink, refreshSecret() {secretAt = 0; loadSecret();}};
}
