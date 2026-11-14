export function createVisibility(deps) {
  const {json, tr, node, icon, toast, may} = deps;
  const run = deps.busy || (async (button, work) => {
    if (button) button.disabled = true;
    try {return await work();} catch (error) {if (error?.name !== 'StaleView') toast(error.message, true);}
    finally {if (button) button.disabled = false;}
  });
  const READS = [['never', 'Never'], ['manual', 'Only with the Mark as read button'],
    ['on_reply', 'After I send a message here from the panel'], ['on_open', 'When I open the chat in the panel']];
  const CONTENTS = [['never', 'Never'], ['manual', 'Only with the Mark as opened button']];
  const STORIES = [['never', 'Never'], ['manual', 'Only with the Mark stories as viewed button']];
  const TYPINGS = [['hidden', 'Hidden'], ['shown', 'While I type in the panel'], ['before_send', 'Before each sent message']];
  const SILENCE = [['never', 'Never'], ['while_invisible', 'While this account is invisible'], ['always', 'Always']];
  const FIELDS = [
    ['read_receipts', 'Read receipts', READS], ['content_opened', 'Opened one-time media and played voice messages', CONTENTS],
    ['story_read', 'Viewed stories', STORIES], ['typing', 'Typing status', TYPINGS],
    ['silent_send', 'Send without sound', SILENCE],
    ['show_peer_typing', 'Show when the other side is typing'], ['record_peer_typing', 'Record the other side’s typing in the journal']];
  const PRESET = [['invisible', 'Invisible'], ['visible', 'Visible like a regular app'], ['custom', 'Custom']];
  const SCHEDULED = 'Scheduled sending is not offered: such messages carry a from_scheduled mark that the other side can see through the Telegram API.';
  const SECRET_WARNING = 'Marking a Secret Chat as read or its messages as opened starts the self-destruct timers on the other side. TgWitness keeps its own copies.';
  const SECRET_SILENT = 'Send without sound is not available in Secret Chats: the protocol module used here cannot set it.';
  const label = (list, value) => tr((list.find(([key]) => key === value) || [value, String(value)])[1]);
  const visible = fields => fields.read_receipts === 'on_open' || fields.read_receipts === 'on_reply' || fields.typing !== 'hidden'
    || fields.content_opened !== 'never' || fields.story_read !== 'never';

  function openingText(fields) {
    return tr({never: 'Opening this chat does not send a read receipt. The other side does not see that its messages were read here.',
      manual: 'Opening this chat does not send a read receipt. Messages are marked as read only when you press Mark as read.',
      on_reply: 'Opening this chat does not send a read receipt. After you send a message here from the panel, the chat is marked as read.',
      on_open: 'Opening this chat in the panel marks its messages as read for the other side.'}[fields.read_receipts]);
  }

  function select(name, list, value, change, extra) {
    const box = node('label', 'vis-field'), input = node('select');
    box.append(node('span', '', tr(name)), input);
    for (const [key, text] of extra || []) input.append(new Option(text, key));
    for (const [key, text] of list) input.append(new Option(tr(text), key));
    input.value = value;
    input.addEventListener('change', () => change(input.value, input));
    return box;
  }

  function check(name, value, change) {
    const box = node('label', 'vis-check'), input = node('input');
    input.type = 'checkbox'; input.checked = !!value;
    input.addEventListener('change', () => change(input.checked, input));
    box.append(input, node('span', '', tr(name)));
    return box;
  }

  function lockAll(box, locked) {
    for (const field of box.querySelectorAll('select,input')) field.disabled = locked;
  }

  async function workspace(container) {
    const box = node('section', 'vis-panel'), status = node('p', 'hint vis-status');
    status.setAttribute('role', 'status');
    container.replaceChildren(box);
    let data = await json('visibility');
    const draw = () => {
      const chosen = data.workspace, fields = data.effective, editable = may('settings');
      box.replaceChildren();
      const title = node('h3', 'vis-title');
      title.append(icon('eye'), node('span', '', tr('What the other side sees')));
      box.append(title, node('p', 'hint', tr('Chooses what this account lets the other side of a chat see. Everything is invisible unless you choose otherwise here; each read receipt, opened-media notice, story view and typing status sent from the panel is recorded in the journal.')));
      const save = async (patch, input) => {
        const next = {...chosen, ...patch};
        await run(input, async () => {data = await json('visibility', {workspace: next}); draw(); toast(tr('Saved.'));});
      };
      box.append(check('Invisible', chosen.invisible, (value, input) => save({invisible: value}, input)));
      box.append(node('p', 'hint', tr('While Invisible is on, read receipts, opened-media notices, story views and typing are never sent, and the account goes offline after each panel action, whatever is chosen below.')));
      box.append(select('Preset', PRESET.filter(([key]) => key !== 'custom' || data.preset === 'custom'), data.preset,
        (value, input) => value !== 'custom' && save(data.presets[value], input)));
      const list = node('div', 'vis-fields');
      for (const [key, name, options] of FIELDS) {
        list.append(options ? select(name, options, chosen[key], (value, input) => save({[key]: value}, input))
          : check(name, chosen[key], (value, input) => save({[key]: value}, input)));
        if (chosen.invisible && key in data.forced) list.lastChild.append(node('small', 'vis-forced', tr('Now: {value}', {value: label(options, fields[key])})));
      }
      list.append(check('Go offline right after each panel action', chosen.offline_after_action,
        (value, input) => save({offline_after_action: value}, input)));
      list.append(node('p', 'hint', tr('This is the same switch as in Protection. One offline request follows each panel action and its result is recorded; no periodic status is sent.')));
      box.append(list, node('p', 'hint', tr(SCHEDULED)), status);
      if (!editable) {lockAll(box, true); status.textContent = tr('Changing these settings needs the Settings permission.');}
      if (data.interaction_problem) box.append(node('p', 'notice warning', tr(data.interaction_problem)));
    };
    draw();
    return {refresh: async () => {data = await json('visibility'); draw();}};
  }

  let dialog = null;
  function openWorkspace() {
    if (!dialog) {
      dialog = node('dialog', 'vis-dialog');
      const close = node('button', 'quiet vis-close', tr('Close'));
      close.type = 'button'; close.addEventListener('click', () => dialog.close());
      dialog.append(close, node('div', 'vis-dialog-body'));
      document.body.append(dialog);
    }
    dialog.showModal();
    workspace(dialog.querySelector('.vis-dialog-body')).catch(error => toast(error.message, true));
  }

  function control(secret) {
    const base = secret ? 'secret-chats/' : 'chats/';
    const menu = node('details', 'action-menu vis-menu'), summary = node('summary'), panel = node('div', 'action-menu-panel vis-chat');
    const line = node('p', 'vis-typing'), opening = node('span', 'visually-hidden');
    summary.append(icon('eye'), opening); menu.append(summary, panel);
    line.setAttribute('aria-live', 'polite'); line.hidden = true;
    let chatId = null, data = null, sent = 0, reading = null, loading = 0, typed = 0;
    const path = suffix => base + encodeURIComponent(chatId) + '/' + suffix;

    function drawLine() {
      const people = data?.typing || [];
      line.hidden = !people.length;
      line.textContent = !people.length ? '' : people.length > 1 ? tr('{n} people are typing…', {n: people.length})
        : people[0].name ? tr('{name} is typing…', {name: people[0].name}) : tr('typing…');
    }

    function drawSummary() {
      const fields = data?.effective, open = !!fields && visible(fields);
      menu.dataset.state = !fields ? 'unknown' : open ? 'visible' : 'invisible';
      const text = !fields ? tr('What the other side sees') : openingText(fields);
      summary.title = text; opening.textContent = text;
      summary.setAttribute('aria-label', tr('What the other side sees') + ': ' + text);
    }

    function draw() {
      drawSummary(); drawLine();
      panel.replaceChildren();
      if (!data) {panel.append(node('p', 'hint', tr('Loading…'))); return;}
      const fields = data.effective, override = data.override || {}, editable = may('settings') && !data.workspace.invisible;
      const acting = may('interact') && !data.interaction_problem;
      panel.append(node('strong', '', tr('What the other side sees')), node('p', 'vis-opening', openingText(fields)));
      if (data.workspace.invisible) panel.append(node('p', 'notice', tr('Invisible is on for this workspace: nothing below is sent until it is turned off.')));
      const save = async (next, input) => run(input, async () => {
        data = await json('visibility', {chat_id: chatId, secret, override: next}); draw(); toast(tr('Saved.'));
      });
      const presetValue = !Object.keys(override).length ? 'workspace' : data.preset;
      panel.append(select('Preset', [['workspace', 'Use the workspace settings'], ...PRESET.filter(([key]) => key !== 'custom' || presetValue === 'custom')],
        presetValue, (value, input) => value === 'workspace' ? save({}, input) : value !== 'custom' && save({...override, ...data.presets[value]}, input)));
      const list = node('details', 'vis-more'), inner = node('div', 'vis-fields');
      list.append(node('summary', '', tr('Each setting')), inner);
      for (const [key, name, options] of FIELDS) {
        if (secret && key === 'story_read') continue;
        const inherited = data.workspace[key];
        if (options) {
          const field = select(name, options, key in override ? override[key] : '', (value, input) => {
            const next = {...override}; if (value === '') delete next[key]; else next[key] = value; save(next, input);
          }, [['', tr('As in the workspace: {value}', {value: label(options, inherited)})]]);
          if (secret && key === 'silent_send') {field.querySelector('select').disabled = true; field.append(node('small', 'hint', tr(SECRET_SILENT)));}
          inner.append(field);
        } else {
          const field = select(name, [['on', 'On'], ['off', 'Off']], key in override ? (override[key] ? 'on' : 'off') : '', (value, input) => {
            const next = {...override}; if (value === '') delete next[key]; else next[key] = value === 'on'; save(next, input);
          }, [['', tr('As in the workspace: {value}', {value: tr(inherited ? 'On' : 'Off')})]]);
          inner.append(field);
        }
      }
      panel.append(list);
      if (!editable) lockAll(panel, true);
      const actions = node('div', 'vis-actions');
      if (fields.read_receipts === 'manual') {
        const read = node('button', 'secondary', tr('Mark as read'));
        read.type = 'button'; read.disabled = !acting;
        read.addEventListener('click', () => run(read, async () => {
          const result = await json(path('read'), {trigger: 'manual'});
          toast(tr(result.status === 'succeeded' ? 'Marked as read. The request and its result are in the journal.'
            : result.status === 'unchanged' ? 'Already marked as read up to the newest saved message.' : 'Telegram did not confirm the read receipt. See the journal.'));
          await load();
        }));
        actions.append(read);
      }
      if (fields.content_opened === 'manual') {
        const unopened = data.unopened || [];
        if (!unopened.length) actions.append(node('p', 'hint', tr('No saved message waits to be marked as opened.')));
        for (const item of unopened) {
          const key = secret ? item.random_id : item.message_id;
          const mark = node('button', 'quiet', tr('Mark as opened') + ' · ' + (secret ? (item.media || tr('timer {n} s', {n: item.ttl || 0})) : '#' + key + (item.media ? ' · ' + String(item.media).replace('MessageMedia', '') : '')));
          mark.type = 'button'; mark.disabled = !acting;
          mark.addEventListener('click', () => run(mark, async () => {
            await json(path('content-opened'), secret ? {random_ids: [String(key)]} : {message_ids: [key]});
            toast(tr('Sent. The request and its result are in the journal.')); await load();
          }));
          actions.append(mark);
        }
      }
      if (!secret && fields.story_read === 'manual') {
        const form = node('form', 'vis-story'), input = node('input'), go = node('button', 'quiet', tr('Mark stories as viewed'));
        input.type = 'number'; input.min = '1'; input.required = true; input.setAttribute('aria-label', tr('Up to story ID'));
        input.placeholder = tr('Up to story ID'); go.type = 'submit'; go.disabled = !acting;
        form.append(input, go);
        form.addEventListener('submit', event => {event.preventDefault(); run(go, async () => {
          await json(path('story-read'), {max_id: Number(input.value)}); toast(tr('Sent. The request and its result are in the journal.'));
        });});
        actions.append(form);
      }
      if (actions.childNodes.length) panel.append(actions);
      if (secret) panel.append(node('p', 'notice warning', tr(SECRET_WARNING)));
      if (data.interaction_problem && may('interact')) panel.append(node('p', 'hint', tr(data.interaction_problem)));
      if (data.last_read) panel.append(node('p', 'hint', secret ? tr('Last read receipt sent from the panel: up to {date}', {date: new Date(data.last_read * 1000).toISOString().slice(0, 19).replace('T', ' ')})
        : tr('Last read receipt sent from the panel: up to message #{id}', {id: data.last_read})));
      panel.append(node('p', 'hint', tr(SCHEDULED)));
      const more = node('button', 'text-link', tr('Workspace settings'));
      more.type = 'button'; more.addEventListener('click', () => {menu.open = false; openWorkspace();});
      panel.append(more);
    }

    async function load() {
      if (chatId === null) return null;
      const id = chatId, serial = ++loading;
      const result = await json(base + encodeURIComponent(id) + '/visibility');
      if (id !== chatId || serial !== loading) return null;
      const fresh = !data || JSON.stringify(data.effective) !== JSON.stringify(result.effective) || JSON.stringify(data.unopened) !== JSON.stringify(result.unopened)
        || data.last_read !== result.last_read || data.interaction_problem !== result.interaction_problem;
      data = result;
      if (fresh && !panel.contains(document.activeElement)) draw(); else {drawSummary(); drawLine();}
      return data;
    }

    async function seen() {
      if (chatId === null || document.hidden || !data || data.effective.read_receipts !== 'on_open' || !may('interact') || data.interaction_problem) return;
      if (reading) return;
      const id = chatId;
      reading = json(path('read'), {trigger: 'on_open'}).catch(() => null).finally(() => {reading = null;});
      const result = await reading;
      if (id === chatId && result?.status === 'succeeded') load().catch(() => {});
    }

    return {
      menu, line,
      get chatId() {return chatId;},
      async set(id) {
        if (id === chatId) return;
        chatId = id; data = null; menu.open = false; draw();
        if (id === null) return;
        try {if (await load()) await seen();} catch {}
      },
      refresh() {return load().catch(() => null);},
      seen,
      typed() {
        if (chatId === null || !data || data.effective.typing !== 'shown' || !may('interact') || data.interaction_problem) return;
        const now = Date.now();
        if (now - typed < 4000) return;
        typed = now;
        json(path('typing'), {}).catch(() => {});
      },
    };
  }

  function attachChat({chat, header, title, composer, feed}) {
    const view = control(false);
    header.prepend(view.menu);
    title.after(view.line);
    let tick = 0;
    composer?.addEventListener('input', () => view.typed());
    if (feed) new MutationObserver(() => {if (view.chatId !== null) view.seen();}).observe(feed, {childList: true});
    setInterval(() => {
      const id = chat();
      if (id !== view.chatId) {view.set(id ?? null); tick = 0; return;}
      if (id !== null && !document.hidden && ++tick % 3 === 0) view.refresh();
    }, 1000);
    return view;
  }

  return {workspace, openWorkspace, control, attachChat};
}
