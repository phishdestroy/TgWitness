export function createHistoryForward({json, tr, confirm}) {
  let dialog = null, generation = 0, timer = null, current = () => false, opener = null;
  let form, mode, title, destination, review, summary, feedback, start, check, actions, plan, job, startId, source;
  let pending = false, operation = 0, stamp = '';
  const make = (tag, text = '', cls = '') => {const el = document.createElement(tag);el.textContent = text;if (cls) el.className = cls;return el;};
  const button = (label, work, cls = 'secondary') => {const el = make('button', tr(label), cls);el.type = 'button';el.addEventListener('click', work);return el;};
  const active = () => job && !['completed', 'cancelled'].includes(job.state);
  function close() {
    generation++;operation++;stamp = '';clearTimeout(timer);timer = null;pending = false;plan = job = source = null;current = () => false;
    dialog?.replaceChildren();dialog?.remove();dialog = null;
    if (opener?.isConnected) opener.focus({preventScroll: true});opener = null;
  }
  function owner() {const ticket = generation;return () => ticket === generation && !!dialog && current();}
  function values() {return {source: source.id, mode: mode.value, destination: mode.value === 'existing' ? Number(destination.value) : null, title: mode.value === 'existing' ? '' : title.value.trim()};}
  function controls() {
    if (!dialog) return;
    mode.disabled = title.disabled = destination.disabled = pending || !!active();
    title.closest('label').hidden = mode.value === 'existing';title.required = mode.value !== 'existing';
    destination.closest('label').hidden = mode.value !== 'existing';destination.required = mode.value === 'existing';
    check.disabled = pending || !!active();start.disabled = pending || !!active() || !plan || plan.expires_at * 1000 <= Date.now();
    form.hidden = !!active();
    for (const el of actions.children) el.disabled = pending;
  }
  function invalidate() {plan = null;startId = null;review.replaceChildren();controls();}
  function details(root, entries) {
    const list = make('dl', '', 'forward-details');
    for (const [label, value] of entries) {list.append(make('dt', tr(label)), make('dd', String(value ?? '—')));}
    root.replaceChildren(list);
  }
  function showPlan() {
    details(review, [['Source', plan.source_title], ['Destination', plan.destination_title], ['Message ID', '≤ ' + plan.upper_id],
      ['Pause between messages', plan.message_seconds + ' s'], ['Messages per hour at most', plan.messages_per_hour]]);
    review.append(start);controls();
  }
  function showJob() {
    const key = JSON.stringify(job);if (key === stamp) {controls();return;}stamp = key;
    const focused = actions.contains(document.activeElement) ? document.activeElement.textContent : null;
    if (active()) {plan = null;startId = null;review.replaceChildren();}
    if (!job) {summary.replaceChildren();actions.replaceChildren();controls();return;}
    const states = {running:'Running', waiting:'Waiting', pausing:'Pause', paused:'Paused', cancelling:'Cancel', cancelled:'Cancelled', completed:'Completed', uncertain:'Check', creation_unknown:'Check'};
    details(summary, [['Source', job.source_title], ['Destination', job.destination_title + (job.destination ? ' · ' + job.destination : '')],
      ['State', tr(states[job.state] || 'Paused')], ['Sent', job.forwarded], ['Skipped', job.skipped],
      ...(job.wait_until ? [['Resume', new Date(job.wait_until * 1000).toLocaleString()]] : [])]);
    if (job.error) summary.append(make('p', tr(job.error), 'notice warning'));
    if (job.recent_skips?.length) {
      const skipped = make('details'), label = make('summary', tr('Skipped'));skipped.append(label);
      for (const item of job.recent_skips) {
        const reason = item.reason === 'service_message' ? tr('Service message') : item.reason === 'forwarding_restricted' ? tr('Forwarding is restricted in this chat.') : item.reason;
        skipped.append(make('p', item.ids.map(id => '#' + id).join(', ') + ' · ' + reason, 'hint'));
      }
      summary.append(skipped);
    }
    actions.replaceChildren();
    if (['running', 'waiting'].includes(job.state)) actions.append(button('Pause', () => command('pause')));
    if (['paused', 'uncertain'].includes(job.state)) actions.append(button('Resume', () => command('resume'), 'primary'));
    if (active() && !['pausing', 'cancelling'].includes(job.state)) actions.append(button('Cancel', () => command('cancel'), 'quiet'));
    controls();
    if (focused) [...actions.children].find(el => el.textContent === focused)?.focus({preventScroll: true});
  }
  async function poll() {
    const valid = owner(), revision = operation;if (!valid() || document.hidden || pending) {schedule();return;}
    try {const value = await json('history-forward');if (!valid() || pending || revision !== operation) return;job = value.job;showJob();}
    catch (error) {if (valid() && !pending && revision === operation) feedback.textContent = error.message;}
    finally {if (valid()) schedule();}
  }
  function schedule() {clearTimeout(timer);if (dialog) timer = setTimeout(poll, 2000);}
  async function preview() {
    if (pending || !form.reportValidity()) return;
    const valid = owner(), body = values();operation++;pending = true;feedback.textContent = '';controls();
    try {const result = await json('history-forward/plan', body);if (!valid()) return;plan = result;startId = Array.from(crypto.getRandomValues(new Uint8Array(16)), value => value.toString(16).padStart(2, '0')).join('');showPlan();}
    catch (error) {if (valid()) {invalidate();feedback.textContent = error.message;}}
    finally {if (valid()) {pending = false;controls();}}
  }
  async function begin() {
    if (pending || !plan || !startId) return;
    const valid = owner(), request = {plan_id: plan.id, request_id: startId};operation++;pending = true;feedback.textContent = '';controls();
    try {const result = await json('history-forward/start', request);if (!valid()) return;job = result.job;plan = null;review.replaceChildren();showJob();}
    catch (error) {
      if (!valid()) return;
      feedback.textContent = error.message;
      try {const result = await json('history-forward');if (!valid()) return;job = result.job;if (job?.id === request.request_id) {plan = null;review.replaceChildren();}showJob();} catch {}
    } finally {if (valid()) {pending = false;controls();schedule();}}
  }
  async function command(action) {
    if (pending || !job) return;
    const valid = owner(), id = job.id, uncertain = job.state === 'uncertain';operation++;pending = true;controls();
    try {
      if (action === 'resume' && uncertain && !await confirm(tr('Message outcome unknown. Review the destination before resuming.'))) return;
      if (!valid()) return;
      feedback.textContent = '';
      const result = await json('history-forward/' + id + '/' + action, {});
      if (valid()) {job = result.job;showJob();}
    } catch (error) {if (valid()) feedback.textContent = error.message;}
    finally {if (valid()) {pending = false;controls();schedule();}}
  }
  async function open(chat, isCurrent) {
    close();current = isCurrent;if (!current()) return;source = {...chat};opener = document.activeElement;
    dialog = make('dialog', '', 'history-forward-dialog');dialog.setAttribute('aria-labelledby', 'history-forward-title');
    const head = make('div', '', 'forward-head'), heading = make('h2', tr('Forward chat'));heading.id = 'history-forward-title';
    head.append(heading, button('Close', close, 'quiet'));
    const note = make('p', tr('Forward available Telegram history in order. New channels and groups are private. Forwarding restrictions apply.'), 'hint');
    form = make('form');form.addEventListener('submit', event => {event.preventDefault();void preview();});
    form.append(make('p', tr('Source') + ': ' + source.title));
    const field = (label, element) => {const wrap = make('label', tr(label));wrap.append(element);form.append(wrap);return element;};
    mode = field('Destination', make('select'));
    for (const [value, label] of [['channel', 'New channel'], ['group', 'New group'], ['existing', 'Existing channel or group']]) {
      const option = make('option', tr(label));option.value = value;mode.append(option);
    }
    title = field('Title', make('input'));title.type = 'text';title.maxLength = 128;title.value = source.title.slice(0, 128);
    destination = field('Telegram ID', make('input'));destination.type = 'text';destination.inputMode = 'numeric';destination.pattern = '-[1-9][0-9]{0,15}';
    for (const field of [mode, title, destination]) field.addEventListener('input', invalidate);
    check = button('Preview', preview);form.append(check);
    start = button('Start', begin, 'primary');review = make('div', '', 'forward-review');
    summary = make('div', '', 'forward-summary');summary.setAttribute('aria-live', 'polite');
    actions = make('div', '', 'forward-actions');feedback = make('p', '', 'notice warning');feedback.setAttribute('role', 'status');
    dialog.append(head, note, form, review, summary, actions, feedback);document.body.append(dialog);
    dialog.addEventListener('cancel', event => {event.preventDefault();close();});dialog.addEventListener('close', close);
    controls();dialog.showModal();await poll();
  }
  return {open, close};
}
