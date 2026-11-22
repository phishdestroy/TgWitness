'use strict';


(() => {

  const DICT = (() => { try { return JSON.parse(document.getElementById('site-dict')?.textContent || '{}'); } catch { return {}; } })();
  const T = (text, values = {}) => (DICT[text] || text).replace(/\{(\w+)\}/g, (match, key) => key in values ? values[key] : match);
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const showControls = lab => lab.querySelectorAll('[data-enhanced]').forEach(node => { node.hidden = false; });
  const pressed = (lab, attribute, value) => lab.querySelectorAll(`[${attribute}]`).forEach(button => {
    button.setAttribute('aria-pressed', String(button.getAttribute(attribute) === value));
  });

  function journey(lab) {
    const play = lab.querySelector('[data-play]');
    const next = lab.querySelector('[data-next]');
    const states = [
      [T('Waiting for a message'), T('Step through a fictional send, edit and delete.'), T('No observations yet. Start the sequence or advance one event.')],
      [T('Meet at 10:00'), T('A new message is visible in the chat.'), T('Record 1 appended: the collector observed the original message.')],
      [T('Meet at 11:00'), T('The current text changes. The earlier observation stays.'), T('Record 2 appended: the edit is a new observation. Record 1 still holds the original text.')],
      [T('Message deleted'), T('The message has disappeared from the chat view.'), T('Record 3 appended: the deletion notice is retained alongside both observed versions.')],
    ];
    let step = 0;
    let timer;
    let playing = false;
    const render = () => {
      lab.dataset.step = String(step);
      lab.querySelector('[data-chat-message]').textContent = states[step][0];
      lab.querySelector('[data-chat-note]').textContent = states[step][1];
      lab.querySelector('[data-journey-status]').textContent = states[step][2];
      lab.querySelector('[data-record-count]').textContent = [T('0 records'), T('1 record'), T('2 records'), T('3 records')][step];
      lab.querySelector('[data-step-label]').textContent = step === 3 ? T('Complete / {n} of 3', {n:step}) : T('Step / {n} of 3', {n:step});
      lab.querySelectorAll('[data-event]').forEach(row => {
        const pending = Number(row.dataset.event) > step;
        row.classList.toggle('is-pending', pending);
        row.setAttribute('aria-hidden', String(pending));
      });
      play.textContent = playing ? T('Pause') : step === 3 ? T('Replay sequence') : T('Play sequence');
      next.disabled = step === 3;
      lab.classList.toggle('is-playing', playing);
    };
    const stop = () => { clearTimeout(timer); playing = false; render(); };
    const advance = () => {
      step = Math.min(step + 1, 3);
      if (step === 3) playing = false;
      render();
      if (playing) timer = setTimeout(advance, 1600);
    };
    play.addEventListener('click', () => {
      if (playing) { stop(); return; }
      if (motion.matches) { step = 3; render(); return; }
      if (step === 3) step = 0;
      playing = true;
      advance();
    });
    next.addEventListener('click', () => { stop(); advance(); });
    lab.querySelector('[data-reset]').addEventListener('click', () => { stop(); step = 0; render(); });
    document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
    window.addEventListener('pagehide', stop);
    motion.addEventListener('change', stop);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => { if (!entries[0].isIntersecting && playing) stop(); }).observe(lab);
    }
    showControls(lab);
    render();
  }



  const canonical = value => {
    if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
    if (value !== null && typeof value === 'object') {
      return '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + canonical(value[key])).join(',') + '}';
    }
    return JSON.stringify(value);
  };
  const digest = async value => {
    const bytes = new TextEncoder().encode(canonical(value));
    return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), byte => byte.toString(16).padStart(2, '0')).join('');
  };
  const clone = value => JSON.parse(JSON.stringify(value));

  async function hashChain(lab) {
    const status = lab.querySelector('[data-hash-status]');
    if (!globalThis.crypto?.subtle) {
      status.textContent = T('The static example is available. To calculate hashes interactively, open this page over HTTPS or a localhost preview with Web Crypto support.');
      return;
    }
    const records = [
      {seq:1, observed_at:'2026-01-01T10:00:00.000+00:00', source_at:'2026-01-01T10:00:00+00:00', kind:'message.new', chat_id:-100123, message_id:42, actor_id:7, payload:{text:'Meet at 10:00'}, previous_hash:'0'.repeat(64)},
      {seq:2, observed_at:'2026-01-01T10:01:00.000+00:00', source_at:'2026-01-01T10:01:00+00:00', kind:'message.edited', chat_id:-100123, message_id:42, actor_id:null, payload:{text:'Meet at 11:00'}, previous_hash:''},
      {seq:3, observed_at:'2026-01-01T10:02:00.000+00:00', source_at:null, kind:'message.deleted', chat_id:-100123, message_id:42, actor_id:null, payload:{message_ids:[42]}, previous_hash:''},
    ];
    const saved = [];
    for (const event of records) {
      if (saved.length) event.previous_hash = saved.at(-1);
      saved.push(await digest(event));
    }
    const retained = lab.querySelector('[data-retained-head]');
    retained.textContent = saved[2].slice(0, 14) + '…';
    retained.title = saved[2];
    let revision = 0;
    const render = async mode => {
      const current = ++revision;
      const events = clone(records);
      const stored = [...saved];
      if (mode === 'edited' || mode === 'rebuilt') events[1].payload.text = 'Meet at 19:00';
      if (mode === 'truncated') { events.pop(); stored.pop(); }
      if (mode === 'rebuilt') {
        for (let i = 1; i < events.length; i++) {
          events[i].previous_hash = stored[i - 1];
          stored[i] = await digest(events[i]);
        }
      }
      const calculated = await Promise.all(events.map(digest));
      if (current !== revision) return;
      pressed(lab, 'data-hash-mode', mode);
      lab.dataset.hashMode = mode;
      lab.dataset.state = mode === 'original' ? 'ok' : 'error';
      lab.querySelector('[data-hash-text]').textContent = events[1].payload.text;
      lab.querySelectorAll('[data-hash-node]').forEach((node, index) => {
        const removed = index >= events.length;
        const matches = calculated[index] === stored[index];
        node.classList.toggle('is-removed', removed);
        node.classList.toggle('is-broken', !removed && !matches);
        node.classList.toggle('is-rebuilt', mode === 'rebuilt' && index > 0);
        const hash = node.querySelector('[data-hash-value]');
        hash.textContent = removed ? T('No record supplied') : calculated[index].slice(0, 14) + '…';
        hash.title = removed ? '' : calculated[index];
        node.querySelector('.hash-verdict').textContent = removed ? T('Tail removed') : !matches ? T('≠ saved hash') : mode === 'rebuilt' && index > 0 ? T('Rebuilt · different hash') : T('= saved hash');
      });
      const explanations = {
        original:[T('Same length and matching head.'), T('All three computed hashes match the saved hashes. This sample agrees with the retained three-record boundary.')],
        edited:[T('Same saved head; the journal prefix fails verification.'), T('Record 2 no longer matches its saved hash. Checking only the final stored head would miss this; the verifier checks every record.')],
        rebuilt:[T('Head differs from the retained checkpoint.'), T('The rebuilt hashes link together, but the final head has changed. The retained checkpoint rejects this history. Original signatures would also fail on changed records.')],
        truncated:[T('Too short: 2 supplied records < 3 retained records.'), T('The two remaining hashes still match. The retained checkpoint reveals the missing tail. Without that earlier boundary, this shorter prefix alone would not reveal the omission.')],
      };
      lab.querySelector('[data-boundary-verdict]').textContent = explanations[mode][0];
      status.textContent = explanations[mode][1];
      lab.querySelector('[data-canonical]').textContent = canonical(events[1]);
      lab.querySelector('[data-stored-digest]').textContent = stored[1];
      lab.querySelector('[data-calculated-digest]').textContent = calculated[1];
      lab.querySelector('[data-hash-detail]').hidden = false;
    };
    const failed = () => {
      status.textContent = T('Hash calculation is unavailable in this browser. The formulas and static explanation below remain available.');
      lab.querySelectorAll('[data-hash-mode]').forEach(button => { button.disabled = true; });
    };
    lab.querySelectorAll('[data-hash-mode]').forEach(button => {
      button.addEventListener('click', () => { render(button.dataset.hashMode).catch(failed); });
    });
    await render('original');
    showControls(lab);
  }

  function witness(lab) {
    const answers = {
      ok:[T('{n} records', {n:128}), T('head {hash}', {hash:'a4f2…'}), T('Accepted: the count grows, the signature verifies and the key matches. The witness retains this new boundary.')],
      rollback:[T('{n} records', {n:112}), T('head {hash}', {hash:'65be…'}), T('Rollback: the signed answer reports fewer records than the last accepted checkpoint. The witness records the problem and keeps the earlier accepted boundary.')],
      fork:[T('{n} records', {n:120}), T('head {hash}', {hash:'b8e1…'}), T('Fork: the count is unchanged but the head differs. The witness records the disagreement and keeps the earlier accepted boundary.')],
      offline:[T('No answer'), T('boundary unknown'), T('No response: the witness records the failed check. It cannot assert the collector’s current state. If the witness can still reach the Bot API and its publication policy permits, it can publish that failure.')],
    };
    lab.querySelectorAll('[data-witness-mode]').forEach(button => {
      button.addEventListener('click', () => {
        const mode = button.dataset.witnessMode;
        pressed(lab, 'data-witness-mode', mode);
        lab.dataset.state = mode === 'ok' ? 'ok' : mode === 'offline' ? 'warning' : 'error';
        lab.querySelector('[data-witness-count]').textContent = answers[mode][0];
        lab.querySelector('[data-witness-head]').textContent = answers[mode][1];
        lab.querySelector('[data-witness-status]').textContent = answers[mode][2];
      });
    });
    showControls(lab);
  }

  function delivery(lab) {
    const actions = [T('Send {n}', {n:1}), T('Edit {n}', {n:1}), T('Delete {n}', {n:1}), T('Send {n}', {n:2}), T('Edit {n}', {n:2}), T('Delete {n}', {n:2})];
    const a = [0.6, 0.8, 1.2, 0.7, 0.9, 1.4];
    const scenarios = {
      complete:[1.0, 1.2, 1.6, 0.9, 1.3, 1.8],
      delayed:[1.0, 1.2, 1.6, 6.8, 7.4, 1.8],
      missing:[1.0, 1.2, 1.6, 0.9, null, 1.8],
    };
    const notes = {
      complete:T('Both accounts captured all six expected observations in this example.'),
      delayed:T('Account B still captured 6 of 6. Two receipts took longer. Capture ratio and receipt delay answer different questions.'),
      missing:T('Account B captured 5 of 6 by the cutoff (83.3%). The missing edit has no measured delay. This result only describes the six controlled actions.'),
    };
    const svg = (tag, attrs) => {
      const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
      Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
      return node;
    };
    const render = mode => {
      const b = scenarios[mode];
      pressed(lab, 'data-delivery-mode', mode);
      lab.dataset.state = mode === 'missing' ? 'error' : mode === 'delayed' ? 'warning' : 'ok';
      const group = lab.querySelector('[data-chart-points]');
      group.replaceChildren();
      [a, b].forEach((values, series) => {
        values.forEach((value, index) => {
          const x = 87 + index * 91 + (series ? 6 : -6);
          const y = value === null ? 244 : 244 - value * 27.5;
          const color = series ? 'point-b' : 'point-a';
          if (value !== null) group.append(svg('line', {x1:x, x2:x, y1:244, y2:y, class:'chart-stem ' + color}));
          const point = value === null
            ? svg('path', {d:`M${x-5} ${y-5}l10 10m0-10l-10 10`, class:'point-missing'})
            : series ? svg('path', {d:`M${x} ${y-6}l6 6-6 6-6-6z`, class:color})
              : svg('circle', {cx:x, cy:y, r:5, class:color});
          const title = svg('title', {});
          title.textContent = `${series ? 'B' : 'A'} · ${actions[index]} · ${value === null ? T('not observed by cutoff') : T('{s} seconds', {s:value.toFixed(1)})}`;
          point.append(title);
          group.append(point);
          if (!motion.matches) point.animate([{opacity:0}, {opacity:1}], {duration:220, easing:'ease-out'});
        });
      });
      const observed = b.filter(value => value !== null).length;
      const rate = observed === 6 ? '100%' : (100 * observed / 6).toFixed(1) + '%';
      lab.querySelector('[data-rate-b]').textContent = `${observed} / 6 · ${rate}`;
      lab.querySelector('[data-delivery-status]').textContent = notes[mode];
      lab.querySelector('#delivery-chart-desc').textContent = notes[mode] + ' ' + T('Exact values follow in the table.');
      const table = lab.querySelector('[data-delivery-table]');
      table.replaceChildren();
      actions.forEach((action, index) => {
        const row = document.createElement('tr');
        [action, T('{s} s', {s:a[index].toFixed(1)}), b[index] === null ? T('Not observed') : T('{s} s', {s:b[index].toFixed(1)})].forEach((value, column) => {
          const cell = document.createElement(column === 0 ? 'th' : 'td');
          if (column === 0) cell.scope = 'row';
          cell.textContent = value;
          row.append(cell);
        });
        table.append(row);
      });
    };
    lab.querySelectorAll('[data-delivery-mode]').forEach(button => button.addEventListener('click', () => render(button.dataset.deliveryMode)));
    showControls(lab);
    render('complete');
  }

  function investigation(lab) {
    const views = {
      all:{sources:['channel', 'group', 'bot', 'private'], text:T('Four chats contribute different observations. Follow the source records for every connection; do not assign the channel post to user 71001 without an attributed sender.')},
      person:{sources:['group', 'private'], text:T('Records #146 and #205 supply the same sender ID, 71001. That connects a Telegram account’s observed posts across two chats. It does not identify a real-world person or attribute the channel post.')},
      link:{sources:['channel', 'group', 'bot', 'private'], text:T('The destination pay.example.invalid/new appears in group record #146, bot keyboard #173, channel edit #188 and private message #205. A repeated destination connects the material across those records.')},
      file:{sources:['group', 'private'], text:T('Completed media receipts #151 and #209 have equal full SHA-256 values in this fictional case. Compare the actual bytes and their associated message records. The matching file does not identify its creator or prove who forwarded it.')},
    };
    lab.querySelectorAll('[data-case-mode]').forEach(button => {
      button.addEventListener('click', () => {
        const mode = button.dataset.caseMode;
        pressed(lab, 'data-case-mode', mode);
        lab.dataset.caseView = mode;
        lab.querySelectorAll('[data-case-node]').forEach(node => {
          const active = views[mode].sources.includes(node.dataset.caseNode);
          node.classList.toggle('is-muted', !active);
          node.classList.toggle('is-linked', active);
          if (active && !motion.matches) node.animate([{borderColor:'#bad9ff'}, {borderColor:'#689cd5'}], {duration:350});
        });
        lab.querySelector('[data-case-status]').textContent = views[mode].text;
      });
    });
    showControls(lab);
    lab.dataset.caseView = 'all';
  }

  function security(lab) {
    const names = {replica:T('the encrypted off-site copy'), alerts:T('notifications'), timestamp:T('checkpoint hashes for timestamps'),
                   witness:T('signed checkpoints for the witness')};
    const on = new Set();
    const render = () => {
      lab.querySelectorAll('[data-flow-toggle]').forEach(button => button.setAttribute('aria-pressed', String(on.has(button.dataset.flowToggle))));
      lab.querySelectorAll('.route[data-flow]').forEach(route => {
        const flow = route.dataset.flow;
        if (flow === 'telegram') return;
        const active = on.has(flow);
        route.classList.toggle('is-on', active);
        route.querySelector('[data-state-label]').textContent = active ? T('Switched on in this example') : T('Optional · off by default');
      });
      lab.dataset.flows = [...on].join(' ');
      lab.querySelector('[data-security-status]').textContent = on.size
        ? T('Leaving this machine: the Telegram connection and {list}. Nothing else.', {list:[...on].map(flow => names[flow]).join(', ')})
        : T('Default: only the Telegram connection leaves this machine.');
    };
    lab.querySelectorAll('[data-flow-toggle]').forEach(button => button.addEventListener('click', () => {
      const flow = button.dataset.flowToggle;
      if (on.has(flow)) on.delete(flow); else on.add(flow);
      render();
      const route = lab.querySelector(`.route[data-flow="${flow}"]`);
      if (on.has(flow) && !motion.matches) route.animate([{transform:'translateX(-6px)', opacity:.6}, {transform:'none', opacity:1}], {duration:320, easing:'cubic-bezier(.2,.8,.2,1)'});
    }));
    showControls(lab);
    render();
  }


  function hardening(lab) {
    const items = [...lab.querySelectorAll('.checklist-items li')];
    const count = lab.querySelector('[data-checklist-count]');
    const meter = lab.querySelector('.meter i');
    const update = () => {
      const done = items.filter(item => item.classList.contains('is-done')).length;
      count.textContent = T('{done} of {total} done', {done, total:items.length});
      meter.style.width = `${Math.round(done / items.length * 100)}%`;
      lab.classList.toggle('is-complete', done === items.length);
    };
    items.forEach((item, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'check-toggle';
      button.setAttribute('aria-pressed', 'false');
      button.setAttribute('aria-label', T('Mark step {n} as done', {n:index + 1}));
      button.dataset.enhanced = '';
      button.addEventListener('click', () => {
        const done = !item.classList.contains('is-done');
        item.classList.toggle('is-done', done);
        button.setAttribute('aria-pressed', String(done));
        update();
      });
      item.prepend(button);
    });
    showControls(lab);
    update();
  }


  async function modesHash(lab) {
    const status = lab.querySelector('[data-hash-status]');
    if (!globalThis.crypto?.subtle) {
      status.textContent = T('modes.hash.unavailable');
      return;
    }
    const input = lab.querySelector('[data-edit-record]');
    const original = input.value;
    const records = [1, 2, 3].map(seq => ({seq, observed_at:'2026-01-01T10:00:00.000+00:00',
      source_at:null, kind:seq === 1 ? 'message.new' : seq === 2 ? 'message.edited' : 'message.deleted',
      chat_id:-100123, message_id:42, actor_id:null,
      payload:seq === 3 ? {message_ids:[42]} : {text:seq === 2 ? original : 'Meet at 10:00'}, previous_hash:'0'.repeat(64)}));
    const saved = [];
    for (const event of records) {
      if (saved.length) event.previous_hash = saved.at(-1);
      saved.push(await digest(event));
    }
    saved.forEach((hash, index) => {
      const node = lab.querySelector(`[data-digest="${index + 1}"]`);
      node.textContent = hash.slice(0, 16) + '…';
      node.title = hash;
    });
    lab.querySelector('[data-stored]').textContent = saved[1];
    let revision = 0;
    const update = async () => {
      const current = ++revision;
      const event = clone(records[1]);
      event.payload.text = input.value;
      const calculated = await digest(event);
      if (current !== revision) return;
      const broken = calculated !== saved[1];
      lab.dataset.state = broken ? 'error' : 'ok';
      lab.querySelector('[data-calculated]').textContent = calculated;
      const node = lab.querySelector('[data-digest="2"]');
      node.textContent = calculated.slice(0, 16) + '…';
      node.title = calculated;
      status.textContent = T(broken ? 'modes.hash.changed' : 'modes.hash.ok');
    };
    input.addEventListener('input', () => update().catch(() => {
      status.textContent = T('modes.hash.unavailable');
    }));
    await update();
    showControls(lab);
  }

  const textDigest = async text => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text))),
    byte => byte.toString(16).padStart(2, '0')).join('');

  function steps(lab) {
    const nodes = [...lab.querySelectorAll('[data-step]')];
    const status = lab.querySelector('[data-steps-status]');
    const run = lab.querySelector('[data-steps-run]');
    const finished = status.textContent;
    const outcome = nodes.map(node => node.className);
    let timers = [];
    const play = () => {
      timers.forEach(clearTimeout);
      timers = [];
      const pace =motion.matches ? .4 : 1;
      run.disabled = true;
      lab.dataset.state = 'ok';
      nodes.forEach(node => { node.className = 'hash-node is-pending'; });
      nodes.forEach((node, index) => {
        timers.push(setTimeout(() => {
          node.classList.add('is-checking');
          status.textContent = T('Checking {n} of {total}…', {n:index + 1, total:nodes.length});
        }, (250 + index * 1300) * pace));
        timers.push(setTimeout(() => {
          node.className = outcome[index];
          if (index === nodes.length - 1) {
            status.textContent = finished;
            lab.dataset.state = 'error';
            run.disabled = false;
          }
        }, (1150 + index * 1300) * pace));
      });
    };
    run.addEventListener('click', play);
    showControls(lab);
    if (!motion.matches && 'IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        if (!entries[0].isIntersecting) return;
        observer.disconnect();
        play();
      }, {threshold:.5});
      observer.observe(lab);
    }
  }

  async function compare(lab) {
    if (!globalThis.crypto?.subtle) throw new Error('Web Crypto unavailable');
    const inputs = [...lab.querySelectorAll('[data-compare-input]')];
    const outputs = [...lab.querySelectorAll('[data-compare-out]')];
    const status = lab.querySelector('[data-compare-status]');
    const chars = lab.querySelector('[data-compare-chars]');
    const charsLabel = lab.querySelector('[data-compare-chars-label]');
    const hex = lab.querySelector('[data-compare-hex]');
    const bits = lab.querySelector('[data-compare-bits]');
    const prefix = lab.querySelector('[data-compare-prefix]');
    const reset = lab.querySelector('[data-compare-reset]');
    const base = inputs.map(input => input.value);
    let revision = 0;
    const render = async () => {
      const current = ++revision;
      const digests = await Promise.all(inputs.map(input => textDigest(input.value)));
      if (current !== revision) return;
      const [a, b] = digests;
      let hexCount = 0, bitCount = 0;
      const parts = [document.createDocumentFragment(), document.createDocumentFragment()];
      for (let i = 0; i < a.length; i++) {
        const differs = a[i] !== b[i];
        if (differs) hexCount++;
        for (let x = parseInt(a[i], 16) ^ parseInt(b[i], 16); x; x >>= 1) bitCount += x & 1;
        [a[i], b[i]].forEach((digit, side) => {
          if (!differs) { parts[side].append(digit); return; }
          const mark = document.createElement('mark');
          mark.textContent = digit;
          parts[side].append(mark);
        });
      }
      outputs.forEach((output, side) => { output.replaceChildren(parts[side]); output.title = digests[side]; });
      const left = [...inputs[0].value], right = [...inputs[1].value];
      let charCount = Math.abs(left.length - right.length);
      for (let i = 0; i < Math.min(left.length, right.length); i++) if (left[i] !== right[i]) charCount++;
      chars.textContent = String(charCount);
      charsLabel.textContent = charCount === 1 ? T('character apart') : T('characters apart');
      hex.textContent = String(hexCount);
      bits.textContent = String(bitCount);
      lab.dataset.state = hexCount ? 'error' : 'ok';
      const prefixed = prefix?.getAttribute('aria-pressed') === 'true';
      status.textContent = !hexCount ? T('Identical bytes, identical fingerprints. Anyone can confirm it.')
        : prefixed ? T('The prefix adds bytes to both lines. Both fingerprints change completely, and the difference is still there.')
        : charCount === 1 ? T('One character apart. Two unrelated fingerprints.')
        : T('Different bytes, different fingerprints. No title can make them match.');
    };
    const apply = on => {
      prefix?.setAttribute('aria-pressed', String(on));
      inputs.forEach((input, index) => { input.value = (on ? prefix.dataset.comparePrefix : '') + base[index]; });
      return render();
    };
    inputs.forEach(input => input.addEventListener('input', () => { render().catch(() => {}); }));
    prefix?.addEventListener('click', () => { apply(prefix.getAttribute('aria-pressed') !== 'true').catch(() => {}); });
    reset?.addEventListener('click', () => { apply(false).catch(() => {}); });
    await render();
    showControls(lab);
  }

  async function chain(lab) {
    if (!globalThis.crypto?.subtle) throw new Error('Web Crypto unavailable');
    const nodes = [...lab.querySelectorAll('[data-chain-node]')];
    const status = lab.querySelector('[data-chain-status]');
    const edit = lab.querySelector('[data-chain-edit]');
    const index = Number(edit.dataset.chainEdit);
    const original = nodes.map(node => node.dataset.text);
    const zero = '0'.repeat(64);
    const link = (previous, text) => textDigest(previous + '\n' + text);
    const sealed = [];
    for (const text of original) sealed.push(await link(sealed.at(-1) || zero, text));
    const initial = status.textContent;
    let revision = 0;
    const render = async edited => {
      const current = ++revision;
      const texts = [...original];
      if (edited) texts[index] = texts[index].replace(edit.dataset.chainFrom, edit.dataset.chainTo);
      const calculated = await Promise.all(texts.map((text, i) => link(i ? sealed[i - 1] : zero, text)));
      if (current !== revision) return;
      nodes.forEach((node, i) => {
        const changed = calculated[i] !== sealed[i];
        const unlinked = i > 0 && calculated[i - 1] !== sealed[i - 1];
        node.classList.toggle('is-broken', changed || unlinked);
        node.querySelector('[data-chain-text]').textContent = texts[i];
        const hash = node.querySelector('[data-chain-hash]');
        hash.textContent = calculated[i].slice(0, 14) + '…';
        hash.title = calculated[i];
        node.querySelector('.hash-verdict').textContent = changed ? T('≠ saved hash') : unlinked ? T('Previous hash no longer matches') : T('= saved hash');
      });
      edit.setAttribute('aria-pressed', String(edited));
      lab.dataset.state = edited ? 'error' : 'ok';
      status.textContent = edited
        ? T('Record {n} changed, so its hash changed. Record {next} still holds the old fingerprint: the correction is visible to anyone who checks.', {n:index + 1, next:index + 2})
        : initial;
    };
    edit.addEventListener('click', () => { render(edit.getAttribute('aria-pressed') !== 'true').catch(() => {}); });
    await render(false);
    showControls(lab);
  }

  async function seal(lab) {
    if (!globalThis.crypto?.subtle) throw new Error('Web Crypto unavailable');
    const $ = selector => lab.querySelector(selector);
    const sheet = $('[data-seal-sheet]');
    const pdfBadge = $('[data-seal-pdf-badge]');
    const pdfFoot = $('[data-seal-pdf-foot]');
    const badge = $('[data-seal-badge]');
    const state = $('[data-seal-state]');
    const foot = $('[data-seal-foot]');
    const envelopeOut = $('[data-seal-envelope]');
    const status = $('[data-seal-status]');
    const run = $('[data-seal-run]');
    const xrayButton = $('[data-seal-xray]');
    const swapButton = $('[data-seal-swap]');
    const fields = [...lab.querySelectorAll('[data-seal-field]')];
    const decisions = [...lab.querySelectorAll('[data-seal-decision]')];
    const steps = [...lab.querySelectorAll('[data-seal-step]')];
    const censors = [...sheet.querySelectorAll('.censor-box')];
    const values = fields.map((field, i) => field.dataset.sealField || (censors[i] ? censors[i].textContent : ''));
    const guess = fields.findIndex(field => field.hasAttribute('data-seal-guess'));
    const swapIndex = Number(swapButton.dataset.sealSwap);
    const encoder = new TextEncoder();
    const hex = bytes => Array.from(bytes, byte => byte.toString(16).padStart(2, '0')).join('');
    const unhex = text => Uint8Array.from(text.match(/../g), pair => parseInt(pair, 16));
    const short = digest => digest.slice(0, 12) + '…';
    const commit = async (salt, value) => {
      const data = encoder.encode(value);
      const joined = new Uint8Array(salt.length + data.length);
      joined.set(salt);
      joined.set(data, salt.length);
      return hex(new Uint8Array(await crypto.subtle.digest('SHA-256', joined)));
    };
    const authority =await crypto.subtle.generateKey({name:'RSA-OAEP', modulusLength:3072, publicExponent:new Uint8Array([1, 0, 1]), hash:'SHA-256'},
      false, ['encrypt', 'decrypt']);
    const sealFor = async entries => {
      const key = await crypto.subtle.generateKey({name:'AES-GCM', length:256}, true, ['encrypt']);
      const nonce = crypto.getRandomValues(new Uint8Array(12));
      const wrapped = new Uint8Array(await crypto.subtle.encrypt({name:'RSA-OAEP'}, authority.publicKey, await crypto.subtle.exportKey('raw', key)));
      const payload = encoder.encode(JSON.stringify(entries.map(entry => ({value:entry.value, salt:hex(entry.salt)}))));
      return {wrapped, nonce, body:new Uint8Array(await crypto.subtle.encrypt({name:'AES-GCM', iv:nonce}, key, payload))};
    };
    const open = async envelope => {
      const raw = await crypto.subtle.decrypt({name:'RSA-OAEP'}, authority.privateKey, envelope.wrapped);
      const key = await crypto.subtle.importKey('raw', raw, 'AES-GCM', false, ['decrypt']);
      return JSON.parse(new TextDecoder().decode(await crypto.subtle.decrypt({name:'AES-GCM', iv:envelope.nonce}, key, envelope.body)));
    };
    const entries = values.map(value => ({value, salt:crypto.getRandomValues(new Uint8Array(16))}));
    const commitments = await Promise.all(entries.map(entry => commit(entry.salt, entry.value)));
    const unsalted = guess >= 0 ? await textDigest(values[guess]) : '';
    const honest = await sealFor(entries);
    const forged = await sealFor(entries.map((entry, i) => i === swapIndex
      ? {value:swapButton.dataset.sealSwapTo, salt:crypto.getRandomValues(new Uint8Array(16))} : entry));
    const sample = envelope => T('{bytes} bytes · {sample}…', {bytes:envelope.wrapped.length + envelope.nonce.length + envelope.body.length,
      sample:btoa(String.fromCharCode(...envelope.body.slice(0, 15)))});
    const placeholders = fields.map(field => field.textContent);
    const initial = {pdfBadge:pdfBadge.textContent, pdfFoot:pdfFoot.textContent, badge:badge.textContent, state:state.textContent,
      foot:foot.textContent, envelope:envelopeOut.textContent, status:status.textContent};
    const stepStates = {idle:['', '', ''], handover:['is-active', '', ''], opening:['is-done', 'is-active', ''],
      failed:['is-done', 'is-failed', ''], verified:['is-done', 'is-done', 'is-active'], decided:['is-done', 'is-done', 'is-done']};
    let xray = false, swap = false, phase = 'idle', opened = null, checks = null, timers = [], revision = 0;
    const render = () => {
      xrayButton.setAttribute('aria-pressed', String(xray));
      swapButton.setAttribute('aria-pressed', String(swap));
      run.disabled = phase === 'handover' || phase === 'opening';
      sheet.classList.toggle('is-xray', xray);
      pdfBadge.textContent = xray ? T('{n} fields readable', {n:fields.length}) : initial.pdfBadge;
      pdfFoot.textContent = xray ? T('Text extraction reads every string beneath the rectangles.') : initial.pdfFoot;
      envelopeOut.textContent = xray ? sample(swap ? forged : honest) : initial.envelope;
      steps.forEach((node, i) => {
        node.classList.remove('is-active', 'is-done', 'is-failed');
        if (stepStates[phase][i]) node.classList.add(stepStates[phase][i]);
      });
      const shown = Boolean(opened) && ['failed', 'verified', 'decided'].includes(phase);
      fields.forEach((field, i) => {
        field.title = 'c = ' + commitments[i];
        field.classList.toggle('is-match', shown && checks[i]);
        field.classList.toggle('is-mismatch', shown && !checks[i]);
        field.textContent = shown ? (checks[i] ? '✓ ' : '✗ ') + opened[i].value : xray ? 'c = ' + short(commitments[i]) : placeholders[i];
      });
      decisions.forEach(node => {
        node.hidden = phase !== 'decided';
        node.textContent = {withhold:T('Stays withheld: third-party data'), release:T('Released: it concerns the requester\'s account')}[node.dataset.sealDecision] || '';
      });
      const matches = checks ? checks.filter(Boolean).length : 0;
      const counted = T('{n} of {total} match', {n:matches, total:fields.length});
      const opened_ = T('Opened with the authority key. Every value matches its commitment.');
      const text = {
        idle:[initial.badge, xray ? T('No plaintext in the copy') : initial.state,
          xray && guess >= 0 ? T('Unsalted, the SHA-256 of the text would be {plain}, and a word list finds it. Salted, it is {salted}: nothing to look up.',
            {plain:short(unsalted), salted:short(commitments[guess])}) : initial.foot,
          xray ? T('Raw bytes: the PDF gives away every hidden word. The copy holds only salted commitments, the envelope only ciphertext.') : initial.status],
        handover:[initial.badge, T('Handed to the authority'), initial.foot,
          T('Step 1 of 3: the requester hands the signed copy and the sealed envelope to the authority. Neither of them can open the envelope.')],
        opening:[initial.badge, T('Opening'), initial.foot,
          T('Step 2 of 3: the authority decrypts with its private key and recomputes SHA-256(salt ‖ value) for every field…')],
        failed:[counted, T('Commitment broken'), T('The envelope does not match the copy the firm signed.'),
          T('Caught. Field {n} does not match the commitment the firm signed: the envelope was changed after the requester received the copy.',
            {n:checks ? checks.indexOf(false) + 1 : 0})],
        verified:[counted, T('Authority\'s view'), opened_, T('{n} of {total} values match the commitments the firm signed.', {n:matches, total:fields.length})],
        decided:[counted, T('Authority\'s view'), opened_,
          T('Step 3 of 3: the authority, not the firm, decides. Example: the login stays withheld as third-party data; the complaint text is released to the requester.')],
      }[phase];
      [badge.textContent, state.textContent, foot.textContent, status.textContent] = text;
      const tone = phase === 'failed' || (phase === 'idle' && xray) ? 'error' : phase === 'decided' ? 'ok' : '';
      if (tone) lab.dataset.state = tone; else delete lab.dataset.state;
    };
    const wait = ms => new Promise(resolve => { timers.push(setTimeout(resolve, motion.matches ? 0 : ms)); });
    const stop = () => { revision++; timers.forEach(clearTimeout); timers = []; };
    const check = async () => {
      stop();
      const current = revision;
      opened = null; checks = null; phase = 'handover'; render();
      await wait(900);
      if (current !== revision) return;
      phase = 'opening'; render();
      const result = await open(swap ? forged : honest);
      const verdicts = await Promise.all(result.map(async (entry, i) => await commit(unhex(entry.salt), entry.value) === commitments[i]));
      await wait(900);
      if (current !== revision) return;
      opened = result; checks = verdicts; phase = verdicts.every(Boolean) ? 'verified' : 'failed'; render();
      if (phase === 'failed') return;
      await wait(1100);
      if (current !== revision) return;
      phase = 'decided'; render();
    };
    run.addEventListener('click', () => {
      check().catch(() => { stop(); phase = 'idle'; render(); status.textContent = T('Decryption is unavailable in this browser.'); });
    });
    xrayButton.addEventListener('click', () => { xray = !xray; render(); });
    swapButton.addEventListener('click', () => {
      stop();
      swap = !swap; opened = null; checks = null; phase = 'idle'; render();
      if (swap) status.textContent = T('The firm has re-sealed the envelope with a different text. Run the authority\'s check.');
    });
    render();
    showControls(lab);
  }

  const whenVisible = (lab, start) => {
    if (motion.matches || !('IntersectionObserver' in window)) return;
    const observer = new IntersectionObserver(entries => {
      if (!entries[0].isIntersecting) return;
      observer.disconnect();
      start();
    }, {threshold:.45});
    observer.observe(lab);
  };

  function vsDeploy(lab) {
    const wires = [];
    lab.querySelectorAll('.vs-scene [data-wire]').forEach(path => {
      const pulse = path.cloneNode(false);
      pulse.setAttribute('class', 'vs-pulse');
      pulse.removeAttribute('data-wire');
      path.after(pulse);
      wires.push([path.dataset.wire, path, pulse]);
    });
    const play = lab.querySelector('[data-play]');
    const next = lab.querySelector('[data-next]');
    const label = lab.querySelector('[data-step-label]');
    const status = lab.querySelector('[data-deploy-status]');
    const idle = status.textContent;
    const plan = [null,
      {nodes:['cf'], wires:[['cf']], text:T('Cloudflare creates the tunnel and the DNS records. No server exists yet: the panel address leads nowhere until the server connects.')},
      {nodes:['api', 'firewall'], wires:[['api']], text:T('The provider creates a firewall with no inbound rules. Every connection from outside stops here, SSH included.')},
      {nodes:['server'], wires:[['make']], text:T('The server is created behind that firewall with no SSH key, no backups and no console agent. Its cloud-init is all it receives.')},
      {nodes:['git'], chips:['ssh', 'code'], wires:[['git']], text:T('First boot: cloud-init masks SSH, locks root, fetches exactly one commit and installs only packages whose SHA-256 that commit lists.')},
      {chips:['collector', 'key'], wires:[['tunnel']], text:T('The collector starts and creates its signing key on the server. cloudflared dials out to Cloudflare: the panel is reachable, and only through the tunnel.')},
      {nodes:['record'], wires:[['tunnel'], ['cf', true]], text:T('The collector signs the server ID and the hash of its cloud-init; deploy checks both and writes deployment.json. Publish the collector fingerprint through a channel you do not control alone.')},
    ];
    const last = plan.length - 1;
    let step = 0;
    let timer;
    let playing = false;
    const render = () => {
      lab.dataset.step = String(step);
      const on = new Set(['computer']);
      const chips = new Set();
      const done = new Set();
      for (let index = 1; index <= step; index += 1) {
        (plan[index].nodes || []).forEach(name => on.add(name));
        (plan[index].chips || []).forEach(name => chips.add(name));
        plan[index].wires.forEach(([name]) => done.add(name));
      }
      const active = new Map(step ? plan[step].wires.map(([name, back]) => [name, !!back]) : []);
      lab.querySelectorAll('.vs-scene [data-node]').forEach(node => node.classList.toggle('is-on', on.has(node.dataset.node)));
      lab.querySelectorAll('.vs-scene [data-chip]').forEach(chip => chip.classList.toggle('is-on', chips.has(chip.dataset.chip)));
      wires.forEach(([name, path, pulse]) => {
        path.classList.toggle('is-done', done.has(name));
        pulse.classList.toggle('is-active', active.has(name));
        pulse.classList.toggle('is-reverse', active.get(name) === true);
      });
      lab.querySelectorAll('[data-deploy-step]').forEach(item => {
        const number = Number(item.dataset.deployStep);
        item.classList.toggle('is-done', number < step || step === last);
        item.classList.toggle('is-current', number === step && step !== last);
      });
      status.textContent = step ? plan[step].text : idle;
      label.textContent = step === last ? T('Deployed / {n} of 6', {n:step}) : step ? T('Step / {n} of 6', {n:step}) : T('Ready / 0 of 6');
      play.textContent = playing ? T('Pause') : step === last ? T('Replay deployment') : T('Play deployment');
      next.disabled = step === last;
      lab.classList.toggle('is-playing', playing);
    };
    const stop = () => { clearTimeout(timer); playing = false; render(); };
    const advance = () => {
      step = Math.min(step + 1, last);
      if (step === last) playing = false;
      render();
      if (playing) timer = setTimeout(advance, 2700);
    };
    const start = () => {
      if (motion.matches) { step = last; render(); return; }
      if (step === last) step = 0;
      playing = true;
      advance();
    };
    play.addEventListener('click', () => { if (playing) stop(); else start(); });
    next.addEventListener('click', () => { stop(); advance(); });
    lab.querySelector('[data-reset]').addEventListener('click', () => { stop(); step = 0; render(); });
    document.addEventListener('visibilitychange', () => { if (document.hidden && playing) stop(); });
    window.addEventListener('pagehide', stop);
    motion.addEventListener('change', stop);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => { if (!entries[0].isIntersecting && playing) stop(); }).observe(lab);
    }
    showControls(lab);
    render();
    whenVisible(lab, () => { if (!playing && step === 0) start(); });
  }

  function vsReach(lab) {
    const status = lab.querySelector('[data-reach-status]');
    const idle = status.textContent;
    const lamps = [...lab.querySelectorAll('[data-lamp]')].map(lamp => [lamp, lamp.textContent]);
    const actors = {
      api:{lamp:T('Recorded · verify fails'), result:'seen', text:T('Console, rescue, password reset, rebuild, snapshots and firewall openings all go through the provider API. Each lands in the provider log of your account, and verify fails on it. A stolen token changes nothing about that.')},
      tunnel:{lamp:T('Second connector reported'), result:'seen', text:T('The tunnel token lets someone run a second connector and route panel traffic elsewhere. Cloudflare lists every connector with its address, and verify reports any that does not run on the server. The collector\'s statements still cannot be forged: each one signs a fresh challenge.')},
      network:{lamp:T('Shows as gaps'), result:'gap', text:T('Someone on the provider network, lawful interception included, can block or delay traffic. They cannot alter Telegram content: the session key is created on the server and MTProto pins Telegram\'s server keys. Blocking shows as gaps in the journal.')},
      host:{lamp:T('Not in any log you can see'), result:'unseen', text:T('With root on the host, someone can pause your server, read its memory and signing key, change data before it is signed or move its clock. Only your server is affected, and no customer-visible log records it. This takes the provider\'s staff, a state that compels the provider, or a compromise of the provider itself.')},
    };
    let actor = 'none';
    const render = animate => {
      lab.dataset.actor = actor;
      pressed(lab, 'data-actor', actor);
      const chosen = actors[actor];
      lamps.forEach(([lamp, text]) => {
        const mine = lamp.dataset.lamp === actor;
        lamp.textContent = mine ? chosen.lamp : text;
        lamp.dataset.result = mine ? chosen.result : '';
      });
      lab.dataset.state = !chosen ? 'ok' : chosen.result === 'unseen' ? 'error' : chosen.result === 'gap' ? 'warning' : 'ok';
      status.textContent = chosen ? chosen.text : idle;
      if (animate && chosen && !motion.matches) {
        lab.querySelector(`[data-layer="${actor}"]`).animate([{transform:'scale(.98)'}, {transform:'none'}], {duration:320, easing:'cubic-bezier(.2,.8,.2,1)'});
      }
    };
    lab.querySelectorAll('button[data-actor]').forEach(button => button.addEventListener('click', () => {
      actor = actor === button.dataset.actor ? 'none' : button.dataset.actor;
      render(true);
    }));
    showControls(lab);
    render(false);
  }

  function vsLog(lab) {
    const rows = lab.querySelector('[data-log-rows]');
    const verdict = lab.querySelector('[data-verdict]');
    const exit = lab.querySelector('[data-exit]');
    const status = lab.querySelector('[data-log-status]');
    const marks = {pass:T('PASS'), fail:T('FAIL'), review:T('REVIEW')};
    const reason = {
      created:T('server created'), part:T('part of the deployment'), console:T('web console (VNC) credentials requested'),
      power:T('power or restart: collection was interrupted; compare with the journal'), unknown:T('not expected in this mode'),
    };
    const base = [[T('0 s'), 'create_server', 'pass', reason.created], [T('1 s'), 'apply_firewall', 'pass', reason.part],
                  [T('4 s'), 'start_server', 'pass', reason.part]];
    const scenarios = {
      clean:{rows:base, text:T('Creation, the firewall and the first start, all within 30 minutes of creation: the provider log passes.')},
      console:{rows:[...base, [T('day 3'), 'request_console', 'fail', reason.console]], text:T('Someone asked the provider for web console credentials. That is a way into the running server, so the check fails, whoever asked and whatever happened next.')},
      restart:{rows:[...base, [T('day 5'), 'reboot_server', 'review', reason.power]], text:T('A restart is not a way in, but collection stopped for a while. The report marks it for review: the gap in the journal should match the restart.')},
      unknown:{rows:[...base, [T('day 2'), 'change_dns_ptr', 'review', reason.unknown]], text:T('Nobody classified this action in advance. Reverse DNS is harmless here, but verify does not guess: anything unforeseen goes to review, never to pass.')},
    };
    let timers = [];
    const show = name => {
      timers.forEach(clearTimeout);
      timers = [];
      pressed(lab, 'data-scenario', name);
      const data = scenarios[name];
      rows.replaceChildren(...data.rows.map(([time, command, result, why]) => {
        const row = document.createElement('tr');
        row.className = 'is-pending';
        row.dataset.result = result;
        const when = document.createElement('td');
        when.textContent = time;
        const what = document.createElement('td');
        const code = document.createElement('code');
        code.textContent = command;
        what.append(code);
        const judged = document.createElement('td');
        const mark = document.createElement('span');
        mark.className = 'vs-mark';
        mark.textContent = marks[result];
        judged.append(mark, ' ' + why);
        row.append(when, what, judged);
        return row;
      }));
      const worst = data.rows.some(row => row[2] === 'fail') ? 'fail' : data.rows.some(row => row[2] === 'review') ? 'review' : 'pass';
      const finish = () => {
        verdict.textContent = marks[worst];
        exit.textContent = T('exit {n}', {n:{pass:0, fail:1, review:2}[worst]});
        lab.dataset.verdict = worst;
        lab.dataset.state = worst === 'fail' ? 'error' : worst === 'review' ? 'warning' : 'ok';
        status.textContent = data.text;
      };
      const items = [...rows.children];
      if (motion.matches) {
        items.forEach(row => { row.className = 'is-' + row.dataset.result; });
        finish();
        return;
      }
      lab.dataset.verdict = 'pending';
      lab.dataset.state = 'ok';
      verdict.textContent = '…';
      exit.textContent = '';
      status.textContent = T('Checking {n} actions…', {n:items.length});
      items.forEach((row, index) => {
        timers.push(setTimeout(() => { row.className = 'is-checking'; }, 200 + index * 560));
        timers.push(setTimeout(() => { row.className = 'is-' + row.dataset.result; }, 560 + index * 560));
      });
      timers.push(setTimeout(finish, 700 + items.length * 560));
    };
    lab.querySelectorAll('[data-scenario]').forEach(button => button.addEventListener('click', () => show(button.dataset.scenario)));
    showControls(lab);
    lab.dataset.verdict = 'pass';
    whenVisible(lab, () => show('clean'));
  }

  function vsDns(lab) {
    const status = lab.querySelector('[data-dns-status]');
    const path = lab.querySelector('[data-flow-path]');
    const results = {
      on:{resolver:'logged', dns53:'blocked', dot:'blocked', doh:'unseen', telegram:'unseen', tunnel:'recorded'},
      off:{resolver:'unseen', dns53:'unseen', dot:'unseen', doh:'unseen', telegram:'unseen', tunnel:'recorded'},
    };
    const labels = {logged:T('Logged by Cloudflare'), blocked:T('Blocked by the provider firewall'),
                    unseen:T('Passes · not in the Gateway log'), recorded:T('Cloudflare records the connector\'s address')};
    const texts = {on:status.textContent, off:T('Without Gateway DNS the server asks the provider\'s resolver, and no outside party records which names it looked up. Cloudflare\'s record of the tunnel remains.')};
    const paths = {on:path.textContent, off:T('plain DNS → the provider\'s resolver')};
    const render = mode => {
      pressed(lab, 'data-gateway-mode', mode);
      lab.dataset.gateway = mode;
      path.textContent = paths[mode];
      lab.querySelectorAll('li[data-flow]').forEach(item => {
        const result = results[mode][item.dataset.flow];
        item.dataset.result = result;
        item.querySelector('[data-flow-state]').textContent = mode === 'off' && result === 'unseen'
          ? T('Passes · no outside record') : labels[result];
        if (!motion.matches) item.animate([{opacity:.4}, {opacity:1}], {duration:300, easing:'ease-out'});
      });
      lab.dataset.state = mode === 'on' ? 'ok' : 'warning';
      status.textContent = texts[mode];
    };
    lab.querySelectorAll('[data-gateway-mode]').forEach(button => button.addEventListener('click', () => render(button.dataset.gatewayMode)));
    showControls(lab);
  }

  function vsActions(lab) {
    const rows = lab.querySelector('[data-action-rows]');
    const initial = rows.innerHTML;
    const verdict = lab.querySelector('[data-verdict]');
    const exit = lab.querySelector('[data-exit]');
    const status = lab.querySelector('[data-action-status]');
    const idle = status.textContent;
    const marks = {pass:T('PASS'), fail:T('FAIL'), review:T('REVIEW')};
    const notes = {
      pass:T('Part of a normal deployment: it passes.'),
      fail:T('A way into the running server, or a copy of its disk: verify fails, whoever did it.'),
      review:T('Not a way in, but not expected either: the report marks it for review.'),
    };
    const update = () => {
      const results = [...rows.querySelectorAll('tr')].map(row => row.className.replace('is-', ''));
      const worst = results.includes('fail') ? 'fail' : results.includes('review') ? 'review' : 'pass';
      verdict.textContent = marks[worst];
      exit.textContent = T('exit {n}', {n:{pass:0, fail:1, review:2}[worst]});
      lab.dataset.verdict = worst;
      lab.dataset.state = worst === 'fail' ? 'error' : worst === 'review' ? 'warning' : 'ok';
      return worst;
    };
    const reasons = [...lab.querySelectorAll('.pv-reasons li')].map(item => item.textContent);
    lab.querySelectorAll('[data-action-result]').forEach((button, index) => button.addEventListener('click', () => {
      const result = button.dataset.actionResult;
      const row = document.createElement('tr');
      row.className = 'is-' + result;
      const what = document.createElement('td');
      what.append(button.querySelector('code').cloneNode(true));
      const judged = document.createElement('td');
      const mark = document.createElement('span');
      mark.className = 'vs-mark';
      mark.textContent = marks[result];
      judged.append(mark, ' ' + (reasons[index] || ''));
      row.append(what, judged);
      rows.append(row);
      button.setAttribute('aria-pressed', 'true');
      if (!motion.matches) row.animate([{opacity:0, transform:'translateY(-6px)'}, {opacity:1, transform:'none'}], {duration:320, easing:'cubic-bezier(.2,.8,.2,1)'});
      update();
      status.textContent = notes[result];
    }));
    lab.querySelector('[data-action-reset]').addEventListener('click', () => {
      rows.innerHTML = initial;
      lab.querySelectorAll('[data-action-result]').forEach(button => button.setAttribute('aria-pressed', 'false'));
      update();
      status.textContent = idle;
    });
    showControls(lab);
    update();
  }

  function pvTabs(lab) {
    const tabs = [...lab.querySelectorAll('[data-tab]')];
    const panels = [...lab.querySelectorAll('[data-panel]')];
    const open = (slug, focus) => {
      tabs.forEach(tab => {
        const on = tab.dataset.tab === slug;
        tab.setAttribute('aria-selected', String(on));
        tab.tabIndex = on ? 0 : -1;
        if (on && focus) tab.focus();
      });
      panels.forEach(panel => {
        const on = panel.dataset.panel === slug;
        panel.hidden = !on;
        if (on && !motion.matches) panel.animate([{opacity:0, transform:'translateY(8px)'}, {opacity:1, transform:'none'}], {duration:300, easing:'cubic-bezier(.2,.8,.2,1)'});
      });
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => open(tab.dataset.tab));
      tab.addEventListener('keydown', event => {
        const step = {ArrowRight:1, ArrowLeft:-1}[event.key];
        if (!step) return;
        event.preventDefault();
        open(tabs[(index + step + tabs.length) % tabs.length].dataset.tab, true);
      });
    });
    const fromHash = () => {
      const panel = panels.find(item => '#' + item.id === location.hash);
      if (panel) open(panel.dataset.panel);
    };
    lab.parentElement.querySelectorAll('a[href^="#provider-"]').forEach(link => link.addEventListener('click', () => setTimeout(fromHash)));
    window.addEventListener('hashchange', fromHash);
    showControls(lab);
    open(tabs[0].dataset.tab);
    fromHash();
  }

  function phChain(lab) {
    const links = [...lab.querySelectorAll('[data-chain]')];
    const play = lab.querySelector('[data-play]');
    const label = lab.querySelector('[data-step-label]');
    const status = lab.querySelector('[data-chain-status]');
    const idle = status.textContent;
    let step = 0;
    let timer;
    const render = () => {
      links.forEach((item, index) => {
        item.classList.toggle('is-done', index < step);
        item.classList.toggle('is-current', index === step - 1);
      });
      lab.dataset.step = String(step);
      label.textContent = T('{n} of 5', {n:step});
      status.textContent = step ? links[step - 1].querySelector('strong').textContent + ': ' + links[step - 1].querySelector('span:last-child').textContent : idle;
    };
    const stop = () => { clearTimeout(timer); timer = null; play.disabled = false; };
    const run = () => {
      stop();
      if (motion.matches) { step = links.length; render(); return; }
      step = 0;
      play.disabled = true;
      const next = () => {
        step += 1;
        render();
        if (step < links.length) timer = setTimeout(next, 1100); else stop();
      };
      next();
    };
    play.addEventListener('click', run);
    lab.querySelector('[data-reset]').addEventListener('click', () => { stop(); step = 0; render(); });
    showControls(lab);
    render();
    whenVisible(lab, run);
  }

  function phChecks(lab) {
    const rows = [...lab.querySelectorAll('[data-check]')];
    const verdict = lab.querySelector('[data-verdict]');
    const exit = lab.querySelector('[data-exit]');
    const status = lab.querySelector('[data-checks-status]');
    const passed = status.textContent;
    let timers = [];
    const show = scenario => {
      timers.forEach(clearTimeout);
      timers = [];
      pressed(lab, 'data-scenario', scenario);
      const finish = () => {
        const failed = rows.find(row => row.dataset.check === scenario);
        verdict.textContent = failed ? T('FAIL') : T('PASS');
        exit.textContent = T('exit {n}', {n:failed ? 1 : 0});
        lab.dataset.state = failed ? 'error' : 'ok';
        lab.dataset.verdict = failed ? 'fail' : 'pass';
        status.textContent = failed ? failed.querySelector('code').textContent + ': ' + failed.querySelector('.ph-bad').textContent : passed;
      };
      const settle = row => {
        const bad = row.dataset.check === scenario;
        row.className = bad ? 'is-fail' : 'is-pass';
        row.querySelector('.ph-ok').hidden = bad;
        row.querySelector('.ph-bad').hidden = !bad;
      };
      if (motion.matches) { rows.forEach(settle); finish(); return; }
      lab.dataset.verdict = 'pending';
      verdict.textContent = '…';
      exit.textContent = '';
      rows.forEach(row => { row.className = 'is-pending'; row.querySelector('.ph-ok').hidden = false; row.querySelector('.ph-bad').hidden = true; });
      rows.forEach((row, index) => {
        timers.push(setTimeout(() => { row.className = 'is-checking'; }, 150 + index * 420));
        timers.push(setTimeout(() => settle(row), 450 + index * 420));
      });
      timers.push(setTimeout(finish, 600 + rows.length * 420));
    };
    lab.querySelectorAll('[data-scenario]').forEach(button => button.addEventListener('click', () => show(button.dataset.scenario)));
    showControls(lab);
    rows.forEach(row => { row.className = 'is-pass'; });
    whenVisible(lab, () => show('ok'));
  }

  function phRollback(lab) {
    const status = lab.querySelector('[data-rollback-status]');
    const idle = status.textContent;
    const rolled = lab.querySelector('[data-rollback-text]').textContent;
    const count = lab.querySelector('[data-journal-count]');
    const full = count.textContent;
    const go = back => {
      lab.classList.toggle('is-rolled', back);
      lab.dataset.state = back ? 'error' : 'ok';
      count.textContent = back ? T('{n} records', {n:96}) : full;
      status.textContent = back ? rolled : idle;
    };
    lab.querySelector('[data-rollback]').addEventListener('click', () => go(true));
    lab.querySelector('[data-reset]').addEventListener('click', () => go(false));
    showControls(lab);
  }

  function zoom50(lab) {
    const strip = lab.querySelector('[data-z50-strip]');
    const text = lab.querySelector('[data-z50-text]');
    const stamp = lab.querySelector('[data-z50-date]');
    const HIJACK = 'Suspected Hijacker';
    const rows = [{row:50, page:448, cls:'is-org', day:'2025-08-■', range:T('on or after 8 Aug'), type:'Cheating (753)', note:T('Other row · pasted Portuguese profile'), quote:'jogado pela última vez a 8 de ago.'}];
    const lower = [[49, 'Got DM’d with a fake prize'], [48, 'This account is clearly compromised', 'dup'], [47, 'Asking for weird stuff now'],
      [46, 'Messages sound like a script'], [45, 'Suddenly messaging people weird links probably stolen'],
      [44, 'My friend said they can’t get into this account anymore'], [43, 'Trying to impersonate support staff'],
      [42, 'They’re acting like they want to help but they’re baiting people', 'dup']];
    lower.forEach(([row, quote, dup]) => rows.push({row, page:448, cls:'is-burst', day:'2025-08-■', range:T('8–19 Aug'), type:HIJACK, quote, dup}));
    rows.push({row:41, page:448, cls:'is-anchor', day:'2025-08-1■', range:T('10–19 Aug'), type:HIJACK, note:T('The date box slipped and left the digit “1” visible'), quote:'It’s acting like a phishing account'});
    const upper = [[40, 447, 'This account is clearly compromised', 'dup'], [39, 447, 'Might be a bot using someone else’s name'],
      [38, 447, 'Acting way off pretty sure someone else is using it', '3/3'], [37, 447, 'Could be a hijacked profile'],
      [36, 447, 'That’s not how they used to type'], [35, 447, 'Real owner probably doesn’t even know'], [34, 447, 'Something definitely wrong here'],
      [33, 447, 'Spreading sketchy Discord links'], [32, 447, 'Got a weird phishing DM'], [31, 447, 'Too many red flags definitely not the real person'],
      [30, 447, 'Acting way off pretty sure someone else is using it', '2/3'], [29, 447, 'Might be a bot now used to be real', 'dup'],
      [28, 446, 'Got a sketchy invite from this account'], [27, 446, 'Profile looks real but the actions don’t'],
      [26, 446, 'Seems like they lost access completely'], [25, 446, 'My friend can’t log in, says someone changed the password'],
      [24, 446, 'Name’s the same but energy’s totally off'], [23, 446, 'My friend posted that their account was stolen this is the one'],
      [22, 446, 'Used to play with this person this ain’t them'], [21, 446, 'Acting way off pretty sure someone else is using it', '1/3'],
      [20, 446, 'Everyone in voice chat agrees it’s a stolen account'], [19, 446, 'Friend warned me to report this one'],
      [18, 446, 'This account just started acting shady overnight'], [17, 445, 'This account looks like it got hacked'],
      [16, 445, 'Friend said they lost their stuff and this account is acting off'], [15, 445, 'They’re impersonating creators for scams'],
      [14, 445, 'They used to post memes, now it’s crypto spam'], [13, 445, 'Might be a bot now used to be real', 'dup'],
      [12, 445, 'This account was legit not anymore'], [11, 445, 'That’s a stolen account, for sure'], [10, 445, 'Real person probably got locked out'],
      [9, 445, 'Friend’s account got hacked this is it'], [8, 445, 'They’re acting like they want to help but they’re baiting people', 'dup']];
    upper.forEach(([row, page, quote, dup]) => rows.push({row, page, cls:'is-burst', day:'2025-08-■', range:T('on or after 10 Aug'), type:HIJACK, quote, dup}));
    [[7, 445, 'Offensive Avatar', T('Other row · Chinese text')], [6, 444, 'Cheating (730)', T('Other row'), 'multiple hacks, smurfing.'],
      [5, 444, 'Offensive Persona Name', T('Other row · Russian text about the profile')], [4, 444, 'Harassment (730)', T('Other row'), 'toxic']]
      .forEach(([row, page, type, note, quote]) => rows.push({row, page, cls:'is-org', day:'2025-08-■', range:T('late Aug'), type, note, quote}));
    [[3, HIJACK, T('Other row'), 'This person using bot scams for account fishing'], [2, 'Offensive Avatar', T('Other row · short Cyrillic text')],
      [1, 'Offensive Avatar', T('Other row · the newest readable row in Anlage 1'), 'p***r']]
      .forEach(([row, type, note, quote]) => rows.push({row, page:444, cls:'is-sep', day:'2025-09-■', range:T('1–29 Sep'), type, note, quote}));
    const label = item => T('Row {row} · p. {page}', {row:item.row, page:item.page});
    const duplicate = item => item.dup === 'dup' ? T('repeated text') : item.dup ? T('repeated text {n}', {n:item.dup}) : '';
    let active = null;
    const show = (item, cell) => {
      if (active) active.classList.remove('is-active');
      active = cell;
      cell.classList.add('is-active');
      const head = document.createElement('strong');
      head.textContent = label(item) + ' · ' + item.type;
      const parts = [head];
      const extra = [item.note, duplicate(item)].filter(Boolean).join(' · ');
      if (extra) parts.push(document.createTextNode(' · ' + extra));
      if (item.quote) {
        const quote = document.createElement('q');
        quote.lang = 'en';
        quote.textContent = item.quote;
        parts.push(document.createTextNode(' · '), quote);
      }
      text.replaceChildren(...parts);
      stamp.textContent = item.day + ' · ' + item.range;
    };
    rows.forEach(item => {
      const cell = document.createElement('button');
      cell.type = 'button';
      cell.className = 'z50-cell ' + item.cls;
      cell.setAttribute('role', 'listitem');
      cell.setAttribute('aria-label', label(item) + ' · ' + item.type + ' · ' + item.day);
      cell.title = label(item) + ' · ' + item.day + ' · ' + item.type;
      cell.addEventListener('mouseenter', () => show(item, cell));
      cell.addEventListener('focus', () => show(item, cell));
      cell.addEventListener('click', () => show(item, cell));
      strip.append(cell);
    });
    showControls(lab);
  }

  function lootbox(lab) {
    const POOL = [
      {key:'profile', name:'Offensive Profile', count:1148, cls:'t-profile', pct:'57.5%'},
      {key:'hijack', name:'Suspected Hijacker', count:312, cls:'t-hijack', pct:'15.6%'},
      {key:'cheat', name:'Cheating', count:290, cls:'t-cheat', pct:'14.5%'},
      {key:'persona', name:'Offensive Name', count:87, cls:'t-other', pct:'4.4%'},
      {key:'avatar', name:'Offensive Avatar', count:57, cls:'t-other', pct:'2.9%'},
      {key:'other', name:'Harassment / Spam', count:101, cls:'t-other', pct:'5.1%'},
    ];
    const TOTAL = 1995;
    const ITEM_STEP = 140;
    const $ = selector => lab.querySelector(selector);
    const track = $('[data-lb-track]');
    const shell = track.parentElement;
    const tag = $('[data-lb-tag]');
    const status = $('[data-lb-status]');
    const spinBtn = $('[data-lb-spin]');
    const draw50Btn = $('[data-lb-draw50]');
    const counselBtn = $('[data-lb-counsel]');
    const nodes = {hijack:$('[data-lb-node="hijack"]'), profile:$('[data-lb-node="profile"]'), odds:$('[data-lb-node="odds"]')};
    const vals = {hijack:$('[data-lb-val="hijack"]'), profile:$('[data-lb-val="profile"]'), odds:$('[data-lb-val="odds"]')};
    const notes = {hijack:$('[data-lb-note="hijack"]'), profile:$('[data-lb-note="profile"]'), odds:$('[data-lb-note="odds"]')};

    const logF = new Float64Array(TOTAL + 1);
    for (let i = 1; i <= TOTAL; i += 1) logF[i] = logF[i - 1] + Math.log(i);
    const logC = (n, k) => (k < 0 || k > n ? -Infinity : logF[n] - logF[k] - logF[n - k]);
    const tailP = k => {
      let sum = 0;
      const denom = logC(TOTAL, 50);
      for (let x = k; x <= 50; x += 1) sum += Math.exp(logC(312, x) + logC(TOTAL - 312, 50 - x) - denom);
      return Math.min(1, sum);
    };
    const formatProb = value => {
      if (value >= 0.01) return (value * 100).toFixed(1) + '%';
      const [mantissa, exp] = value.toExponential(1).split('e');
      const sup = {'-':'⁻', '0':'⁰', '1':'¹', '2':'²', '3':'³', '4':'⁴', '5':'⁵', '6':'⁶', '7':'⁷', '8':'⁸', '9':'⁹'};
      return mantissa + ' × 10' + String(Number(exp)).split('').map(ch => sup[ch] || ch).join('');
    };

    const pickOne = () => {
      let r = Math.random() * TOTAL;
      for (const item of POOL) {
        if (r < item.count) return item;
        r -= item.count;
      }
      return POOL[0];
    };

    const buildReel = items => {
      track.replaceChildren();
      items.forEach(item => {
        const el = document.createElement('div');
        el.className = 'lb-reel-item ' + item.cls;
        const cat = document.createElement('span');
        cat.className = 'cat';
        cat.textContent = item.name;
        const meta = document.createElement('span');
        meta.className = 'meta';
        meta.textContent = T('Drop: {pct}', {pct:item.pct});
        el.append(cat, meta);
        track.appendChild(el);
      });
    };

    const setTone = broken => {
      lab.dataset.state = broken ? 'error' : 'ok';
      Object.values(nodes).forEach(node => {
        node.classList.toggle('is-broken', broken);
        node.classList.toggle('is-valid', !broken);
      });
    };

    let spinning = false;
    let singleSpins = 0;
    let draws50 = 0;
    let best50 = 0;
    let animFrame = 0;

    const stopSpin = () => {
      if (animFrame) { cancelAnimationFrame(animFrame); animFrame = 0; }
      spinning = false;
      spinBtn.disabled = false;
      draw50Btn.disabled = false;
    };

    const animateReel = (fromX, toX, duration, onDone) => {
      const start = performance.now();
      let lastActive = -1;
      const step = now => {
        const t = Math.min(1, (now - start) / duration);
        const eased = 1 - Math.pow(1 - t, 4);
        const x = fromX + (toX - fromX) * eased;
        track.style.transform = `translate3d(${x.toFixed(2)}px,0,0)`;
        const idx = Math.floor((shell.clientWidth / 2 - x) / ITEM_STEP);
        if (idx !== lastActive) {
          if (lastActive >= 0 && track.children[lastActive]) track.children[lastActive].classList.remove('is-active');
          if (idx >= 0 && track.children[idx]) track.children[idx].classList.add('is-active');
          lastActive = idx;
        }
        if (t < 1) {
          animFrame = requestAnimationFrame(step);
        } else {
          if (lastActive >= 0 && track.children[lastActive]) track.children[lastActive].classList.remove('is-active');
          animFrame = 0;
          onDone();
        }
      };
      track.style.transform = `translate3d(${fromX}px,0,0)`;
      animFrame = requestAnimationFrame(step);
    };

    buildReel(Array.from({length:14}, pickOne));

    spinBtn.addEventListener('click', () => {
      if (spinning) return;
      spinning = true;
      spinBtn.disabled = true;
      draw50Btn.disabled = true;

      const items = Array.from({length:56}, pickOne);
      const winIndex = 42;
      const winner = items[winIndex];
      buildReel(items);

      const centerOffset = shell.clientWidth / 2 - 66;
      const jitter = (Math.random() - 0.5) * 76;
      const targetX = -(winIndex * ITEM_STEP - centerOffset + jitter);

      animateReel(0, targetX, 2900, () => {
        stopSpin();
        singleSpins += 1;
        const winCard = track.children[winIndex];
        if (winCard) winCard.classList.add('is-winner');
        tag.textContent = T('Single box #{n} · {name}', {n:singleSpins, name:winner.name});
        status.textContent = winner.key === 'hijack'
          ? T('Box #{n}: dropped “{name}” (15.6% chance). Now pull that 43 times out of 50.', {n:singleSpins, name:winner.name})
          : T('Box #{n}: dropped “{name}” ({pct} in Anlage 1). Counsel covered 1,944 rows like this under black rectangles.', {n:singleSpins, name:winner.name, pct:winner.pct});
      });
    });

    draw50Btn.addEventListener('click', () => {
      if (spinning) return;
      spinning = true;
      spinBtn.disabled = true;
      draw50Btn.disabled = true;

      const remaining = POOL.map(item => item.count);
      let left = TOTAL;
      let hijack = 0;
      let profile = 0;
      const preview = [];
      for (let i = 0; i < 50; i += 1) {
        let r = Math.random() * left;
        let chosen = POOL[0];
        for (let j = 0; j < POOL.length; j += 1) {
          if (r < remaining[j]) { remaining[j] -= 1; chosen = POOL[j]; break; }
          r -= remaining[j];
        }
        left -= 1;
        if (chosen.key === 'hijack') hijack += 1;
        else if (chosen.key === 'profile') profile += 1;
        preview.push(chosen);
      }

      buildReel(preview);
      const centerOffset = shell.clientWidth / 2 - 66;
      const targetX = -(36 * ITEM_STEP - centerOffset);

      animateReel(0, targetX, 750, () => {
        stopSpin();
        draws50 += 1;
        if (hijack > best50) best50 = hijack;

        setTone(false);
        tag.textContent = T('Fair 50-box draw #{n}', {n:draws50});
        vals.hijack.textContent = T('{n} of 50', {n:hijack});
        notes.hijack.textContent = T('{pct}% of this draw (expected ~15.6%)', {pct:hijack * 2});
        vals.profile.textContent = T('{n} of 50', {n:profile});
        notes.profile.textContent = T('{pct}% of this draw (expected ~57.5%)', {pct:profile * 2});
        vals.odds.textContent = formatProb(tailP(hijack));
        notes.odds.textContent = T('50-box draws: {draws} · Best: {best} of 50', {draws:draws50, best:best50});
        status.textContent = T('Random draw #{n}: {h} “{hijack}”, {p} “{profile}”, {o} other. Best random draw so far: {best} of 50 (counsel delivered 43 of 50).',
          {n:draws50, h:hijack, p:profile, o:50 - hijack - profile, best:best50, hijack:POOL[1].name, profile:POOL[0].name});
      });
    });

    counselBtn.addEventListener('click', () => {
      stopSpin();
      const rigged = Array.from({length:14}, (_, i) => (i % 7 === 0 ? POOL[4] : POOL[1]));
      buildReel(rigged);
      track.style.transform = 'translate3d(0px,0,0)';

      setTone(true);
      tag.textContent = T('As delivered · 1 Oct 2025');
      vals.hijack.textContent = T('{n} of 50', {n:43});
      notes.hijack.textContent = T('86% of counsel\'s visible sample');
      vals.profile.textContent = T('{n} of 50', {n:0});
      notes.profile.textContent = T('1,147 covered · 1 empty');
      vals.odds.textContent = formatProb(tailP(43));
      notes.odds.textContent = draws50
        ? T('50-box draws: {draws} · Best: {best} of 50', {draws:draws50, best:best50})
        : T('50-box draws: 0 · Best: —');
      status.textContent = T('Counsel’s visible selection from Anlage 1: 43 of 50 “{hijack}” (all after the ban, Aug–Sep 2025) and 0 of 1,148 “{profile}”.', {hijack:POOL[1].name, profile:POOL[0].name});
    });

    showControls(lab);
  }

  const setups = {journey, hash:hashChain, witness, delivery, investigation, security, hardening, modesHash, steps, compare, chain, seal, lootbox, zoom50,
                  vsDeploy, vsReach, vsLog, vsDns, vsActions, pvTabs, phChain, phChecks, phRollback};
  document.querySelectorAll('[data-lab]').forEach(lab => {
    Promise.resolve().then(() => setups[lab.dataset.lab](lab)).catch(() => {
      lab.querySelectorAll('[data-enhanced]').forEach(node => { node.hidden = true; });
      const status = lab.querySelector('[role=status]');
      if (status) status.textContent = T(lab.dataset.lab === 'modesHash' ? 'modes.hash.unavailable' : 'Interactive controls are unavailable in this browser. The static explanation and formulas remain available.');
    });
  });
})();
