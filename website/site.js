

const DICT = (() => { try { return JSON.parse(document.getElementById('site-dict')?.textContent || '{}'); } catch { return {}; } })();
const T = (text, values = {}) => (DICT[text] || text).replace(/\{(\w+)\}/g, (match, key) => key in values ? values[key] : match);
const W = key => DICT[key] || key;
document.querySelectorAll('[data-tabs]').forEach(group => {
  const list = group.querySelector('[data-tab-buttons]');
  const buttons = [...list.querySelectorAll('button')];
  const panels = [...group.querySelectorAll('[data-tab-panel]')];
  list.setAttribute('role', 'tablist');
  list.setAttribute('aria-label', group.getAttribute('aria-label'));
  buttons.forEach(button => button.setAttribute('role', 'tab'));
  panels.forEach(panel => { panel.setAttribute('role', 'tabpanel'); panel.tabIndex = 0; });
  function activate(index, focus = false) {
    buttons.forEach((button, i) => {
      button.setAttribute('aria-selected', String(i === index));
      button.tabIndex = i === index ? 0 : -1;
      document.getElementById(button.getAttribute('aria-controls')).hidden = i !== index;
    });
    if (focus) buttons[index].focus();
  }
  buttons.forEach((button, index) => {
    button.addEventListener('click', () => activate(index));
    button.addEventListener('keydown', event => {
      const offsets = {ArrowRight: 1, ArrowLeft: -1};
      let next;
      if (event.key in offsets) next = (index + offsets[event.key] + buttons.length) % buttons.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = buttons.length - 1;
      else return;
      event.preventDefault();
      activate(next, true);
    });
  });
  activate(0);
});

if (navigator.clipboard && window.isSecureContext) {
  document.querySelectorAll('[data-copy]').forEach(button => {
    button.hidden = false;
    let reset;
    button.addEventListener('click', async () => {
      const code = document.getElementById(button.dataset.copy);
      const status = document.getElementById('copy-status');
      try {
        await navigator.clipboard.writeText(code.textContent);
        button.textContent = T('Copied');
        button.classList.add('is-copied');
        status.textContent = T('Command copied to clipboard.');
      } catch {
        button.textContent = T('Select text');
        const range = document.createRange();
        range.selectNodeContents(code);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        status.textContent = T('The clipboard is unavailable, so the command is selected for you to copy manually.');
      }
      clearTimeout(reset);
      reset = setTimeout(() => { button.textContent = T('Copy'); button.classList.remove('is-copied'); }, 2500);
    });
  });
}

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

if (document.documentElement.classList.contains('home-page') && document.querySelector('.tw-hero')) {
  const root = document.documentElement;
  const still = reduceMotion.matches && root.dataset.motion !== 'always';
  const hasObserver = 'IntersectionObserver' in window;
  if (!still && hasObserver) root.classList.add('js-reveal');

  document.querySelectorAll('[data-motion-toggle]').forEach(button => {
    button.setAttribute('aria-pressed', String(root.dataset.motion === 'always'));
    button.addEventListener('click', () => {
      const always = root.dataset.motion !== 'always';
      try { if (always) localStorage.setItem('tgwitness-motion', 'always'); else localStorage.removeItem('tgwitness-motion'); } catch {                    }
      location.reload();
    });
  });

  const field = document.querySelector('[data-field]');
  if (field) {
    const bend = (x, y) => {
      const dx = x - 300, dy = y - 300, distance = Math.hypot(dx, dy) || 1;
      const push = 42 * Math.exp(-(dx * dx + dy * dy) / 30000);
      return [(x + dx / distance * push).toFixed(1), (y + dy / distance * push).toFixed(1)];
    };
    let d = '';
    for (let line = 0; line <= 12; line++) {
      for (const vertical of [true, false]) {
        const fixed = line * 50;
        for (let step = 0; step <= 24; step++) {
          const moving = step * 25;
          const [x, y] = vertical ? bend(fixed, moving) : bend(moving, fixed);
          d += (step ? 'L' : 'M') + x + ' ' + y;
        }
      }
    }
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', d);
    field.append(path);
  }

  const heroScene = document.querySelector('.tw-hero-scene');
  const heroSvg = heroScene?.querySelector('svg');
  const finale = document.querySelector('[data-finale]');
  if (finale && heroSvg) {
    const copy = heroSvg.cloneNode(true);
    copy.removeAttribute('style');
    finale.append(copy);
  }

  const fitLabels = () => document.querySelectorAll('svg text[data-fit]').forEach(node => {
    const room = Number(node.dataset.fit);
    if (node.twText === undefined) node.twText = node.textContent;
    node.textContent = node.twText;
    node.style.removeProperty('font-size');
    let length = node.getComputedTextLength();
    if (!length || length <= room) return;
    const words = node.twText.split(' ');
    const wrap = node.dataset.wrap;
    if (wrap && words.length > 1) {
      let best = null;
      for (let cut = 1; cut < words.length; cut++) {
        const parts = [words.slice(0, cut).join(' '), words.slice(cut).join(' ')];
        const score = Math.max(parts[0].length, parts[1].length);
        if (!best || score < best[0]) best = [score, parts];
      }
      node.textContent = '';
      best[1].forEach((part, index) => {
        const span = document.createElementNS('http://www.w3.org/2000/svg', 'tspan');
        span.setAttribute('x', node.getAttribute('x'));
        span.setAttribute('dy', index ? '1.15em' : wrap === 'up' ? '-1.15em' : wrap === 'mid' ? '-.58em' : '0');
        span.textContent = part;
        node.append(span);
      });
      length = Math.max(...[...node.children].map(span => span.getComputedTextLength()));
    }
    if (length > room) node.style.fontSize = (parseFloat(getComputedStyle(node).fontSize) * room / length).toFixed(2) + 'px';
  });
  fitLabels();
  document.fonts?.ready.then(fitLabels);

  const scramble = (element, final, progress, keep = 0) => {
    if (!element) return;
    if (progress >= 1 || progress < 0) { if (element.textContent !== final) element.textContent = final; return; }
    const shown = Math.max(keep, Math.floor(progress * final.length));
    let out = '';
    for (let i = 0; i < final.length; i++) {
      const char = final[i];
      out += i < shown || !/[0-9a-f]/.test(char) ? char : '0123456789abcdef'[Math.floor(Math.random() * 16)];
    }
    element.textContent = out;
  };
  const lies = ['09:17', '23:48', '03:11', '18:56', '06:40', '21:05'];
  const hooks = {
    hero: (scene, t) => scene.querySelectorAll('[data-hash]').forEach(el => scramble(el, el.dataset.hash, t < 6500 ? 2 : (t - 6500) / 800)),
    time: (scene, t) => { const el = scene.querySelector('[data-hash]'); scramble(el, el.dataset.hash, t / 1000, 7); },
    secret: (scene, t) => { const el = scene.querySelector('[data-timer]'); if (el) el.textContent = String(Math.max(1, 5 - Math.floor(Math.max(0, t - 700) / 600))); },
    'zt-clk': (scene, t) => { const el = scene.querySelector('[data-clock]'); if (el) el.textContent = t > 150 && t < 1900 ? lies[Math.floor(t / 130) % lies.length] : '14:02'; }
  };

  const scenes = [];
  function makeScene(scene) {
    const steps = (scene.dataset.steps || '0').split(',').map(Number);
    const end = steps[steps.length - 1] + Number(scene.dataset.idle || 0);
    const hook = hooks[scene.dataset.scene];
    let t = 0, last = 0, frame = 0, applied = 0, running = false, visible = false, started = false;
    const stop = () => { cancelAnimationFrame(frame); frame = 0; };
    function tick(now) {
      frame = 0;
      if (last) t += Math.min(now - last, 100);
      last = now;
      while (applied < steps.length && t >= steps[applied]) scene.classList.add('s' + (++applied));
      if (hook) hook(scene, t);
      if (t >= end) { running = false; scene.classList.add('is-done'); if (hook) hook(scene, 1e9); return; }
      frame = requestAnimationFrame(tick);
    }
    function resume() {
      if (!running || !visible || document.hidden || frame) return;
      last = 0;
      frame = requestAnimationFrame(tick);
    }
    function play() {
      stop();
      for (let i = 1; i <= steps.length; i++) scene.classList.remove('s' + i);
      scene.classList.remove('is-done');
      scene.classList.add('is-armed');
      t = 0; applied = 0; running = true; started = true;
      if (hook) hook(scene, 0);
      void scene.getBoundingClientRect();
      resume();
    }
    function show(state) {
      visible = state;
      scene.classList.toggle('is-paused', !state);
      if (state && !started) play();
      else if (state) resume();
      else stop();
    }
    const replay = scene.querySelector('.tw-replay');
    if (replay) {
      replay.hidden = false;
      replay.addEventListener('click', play);
    }
    return {scene, show, resume};
  }

  if (!still && hasObserver) {
    document.querySelectorAll('[data-scene]').forEach(scene => scenes.push(makeScene(scene)));
    const sceneObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      scenes.find(item => item.scene === entry.target)?.show(entry.isIntersecting);
    }), {threshold: .35});
    scenes.forEach(item => sceneObserver.observe(item.scene));
    document.addEventListener('visibilitychange', () => scenes.forEach(item => item.resume()));
    const loopObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      entry.target.classList.toggle('is-paused', !entry.isIntersecting);
    }), {threshold: .05});
    document.querySelectorAll('[data-loop]').forEach(element => { element.classList.add('is-paused'); loopObserver.observe(element); });
  }

  if (heroScene && heroSvg) {
    const nodes = [...heroScene.querySelectorAll('.h-nodes .h-node')];
    const hits = [...heroScene.querySelectorAll('.tw-hit')];
    const tip = heroScene.querySelector('.tw-tip');
    const points = [[300, 56], [532, 225], [443, 497], [157, 497], [68, 225]];
    let current = -1;
    const showTip = index => {
      if (index === current) return;
      current = index;
      nodes.forEach((node, i) => node.classList.toggle('is-near', i === index));
      if (index < 0) { tip.hidden = true; return; }
      tip.querySelector('strong').textContent = hits[index].dataset.name;
      tip.querySelector('span').textContent = hits[index].dataset.text;
      tip.style.setProperty('--tx', Math.min(76, Math.max(24, points[index][0] / 6)) + '%');
      tip.style.setProperty('--ty', (points[index][1] / 5.8) + '%');
      tip.classList.toggle('is-below', points[index][1] < 150);
      tip.hidden = false;
    };
    if (finePointer.matches) {
      heroScene.addEventListener('pointermove', event => {
        const box = heroSvg.getBoundingClientRect();
        const x = (event.clientX - box.left) / box.width * 600, y = (event.clientY - box.top) / box.height * 580;
        if (!still) {
          heroSvg.style.setProperty('--px', ((x - 300) / 300).toFixed(3));
          heroSvg.style.setProperty('--py', ((y - 290) / 290).toFixed(3));
        }
        let best = -1, distance = 95;
        points.forEach(([px, py], i) => { const d = Math.hypot(px - x, py - y); if (d < distance) { distance = d; best = i; } });
        showTip(best);
      });
      heroScene.addEventListener('pointerleave', () => {
        heroSvg.style.setProperty('--px', '0');
        heroSvg.style.setProperty('--py', '0');
        showTip(-1);
      });
    }
    hits.forEach((hit, index) => {
      hit.addEventListener('focus', () => showTip(index));
      hit.addEventListener('click', () => showTip(index));
      hit.addEventListener('blur', () => showTip(-1));
    });
  }

  if (!still && hasObserver) {
    const revealObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const element = entry.target;
      revealObserver.unobserve(element);
      element.classList.add('is-revealed');
      const delay = parseFloat(element.style.getPropertyValue('--rd')) || 0;
      setTimeout(() => element.classList.remove('will-reveal', 'is-revealed'), 2400 + delay * 1000);
    }), {threshold: 0, rootMargin: '0px 0px 12% 0px'});
    document.querySelectorAll('.will-reveal').forEach(element => {
      const siblings = [...element.parentElement.children].filter(child => child.classList.contains('will-reveal'));
      const order = siblings.indexOf(element);
      if (order > 0) element.style.setProperty('--rd', Math.min(order, 5) * .09 + 's');
      revealObserver.observe(element);
    });
  } else {
    document.querySelectorAll('.will-reveal').forEach(element => element.classList.remove('will-reveal'));
  }

  const pills = [...document.querySelectorAll('.tw-pills a')];
  const pillBar = document.querySelector('.tw-pills');
  if (pills.length && hasObserver) {
    const spy = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      pills.forEach(link => {
        const active = link.getAttribute('href') === '#' + entry.target.id;
        link.classList.toggle('is-active', active);
        if (active) {
          link.setAttribute('aria-current', 'true');
          if (pillBar.scrollWidth > pillBar.clientWidth) pillBar.scrollTo({left: link.offsetLeft - (pillBar.clientWidth - link.offsetWidth) / 2, behavior: still ? 'auto' : 'smooth'});
        } else link.removeAttribute('aria-current');
      });
    }), {rootMargin: '-45% 0px -50% 0px'});
    pills.forEach(link => { const target = document.querySelector(link.getAttribute('href')); if (target) spy.observe(target); });
  }

  const bar = document.querySelector('.tw-progress span');
  const toTop = document.querySelector('.tw-top');
  const levels = document.querySelector('[data-levels]');
  const ladder = levels ? [...levels.querySelectorAll('.tw-step')] : [];
  const parties = levels ? [...levels.querySelectorAll('.tw-parties li')] : [];
  const count = levels?.querySelector('[data-count]');
  if (levels && !still) levels.classList.add('js-levels');
  if (toTop) {
    toTop.hidden = false;
    toTop.addEventListener('click', () => {
      window.scrollTo({top: 0, behavior: still ? 'auto' : 'smooth'});
      document.querySelector('.tw-brand')?.focus({preventScroll: true});
    });
  }
  let queued = false;
  function onScroll() {
    queued = false;
    const max = document.documentElement.scrollHeight - innerHeight;
    if (bar) bar.style.setProperty('--p', max > 0 ? (scrollY / max).toFixed(4) : '0');
    if (toTop) toTop.classList.toggle('is-visible', scrollY > innerHeight * 1.2);
    if (levels && !still) {
      const box = levels.getBoundingClientRect();
      const progress = Math.min(1, Math.max(0, (innerHeight * .85 - box.top) / (box.height * .9)));
      const lit = Math.round(progress * ladder.length);
      ladder.forEach((step, i) => step.classList.toggle('is-lit', i < lit));
      parties.forEach((party, i) => party.classList.toggle('is-out', i < lit));
      if (count) count.textContent = String(parties.length - lit);
    }
  }
  addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(onScroll); } }, {passive: true});
  addEventListener('resize', onScroll);
  onScroll();

  const modes = document.querySelector('[data-modes]');
  if (modes) {
    modes.classList.add('js-modes');
    const tiles = [...modes.querySelectorAll('.tw-mode')];
    let intent;
    const open = tile => tiles.forEach(item => {
      const active = item === tile;
      item.classList.toggle('is-open', active);
      item.querySelector('.tw-mode-head').setAttribute('aria-expanded', String(active));
    });
    tiles.forEach(tile => {
      tile.querySelector('.tw-mode-head').addEventListener('click', () => open(tile.classList.contains('is-open') ? null : tile));
      if (finePointer.matches) {
        tile.addEventListener('pointerenter', () => { clearTimeout(intent); intent = setTimeout(() => open(tile), 160); });
        tile.addEventListener('pointerleave', () => clearTimeout(intent));
      }
    });
    open(tiles[0]);
  }

  if (!still) {
    document.querySelectorAll('[data-marquee]').forEach(marquee => {
      const track = marquee.querySelector('.tw-marquee-track');
      if (!track) return;
      [...track.children].forEach(item => {
        const copy = item.cloneNode(true);
        copy.setAttribute('aria-hidden', 'true');
        copy.setAttribute('inert', '');
        copy.querySelectorAll('a, button').forEach(control => control.setAttribute('tabindex', '-1'));
        track.append(copy);
      });
      marquee.classList.add('js-marquee');
      const speed = marquee.classList.contains('tw-uses-marquee') ? 26 : 38;
      const tune = () => marquee.style.setProperty('--marquee-dur', Math.max(20, track.scrollWidth / 2 / speed).toFixed(1) + 's');
      tune();
      addEventListener('resize', tune);
    });
  }

  const stats = document.querySelector('[data-stats]');
  if (stats && !still && hasObserver) {
    const numbers = [...stats.querySelectorAll('[data-count-to]')];
    if (stats.getBoundingClientRect().top > innerHeight) stats.classList.add('tw-stats-wait');
    const counter = new IntersectionObserver(entries => {
      if (!entries[0].isIntersecting) return;
      counter.disconnect();
      if (!stats.classList.contains('tw-stats-wait')) return;
      stats.classList.remove('tw-stats-wait');
      const start = performance.now();
      const step = now => {
        const progress = Math.min(1, (now - start) / 1400);
        const eased = 1 - Math.pow(1 - progress, 3);
        numbers.forEach(number => { number.textContent = String(Math.round(Number(number.dataset.countTo) * eased)); });
        if (progress < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }, {threshold: .4});
    counter.observe(stats);
  }

  const terminal = document.querySelector('[data-console]');
  if (terminal) {
    const live = terminal.querySelector('.tw-console-live');
    const fallback = terminal.querySelector('.tw-console-static');
    const out = terminal.querySelector('[data-out]');
    const verdict = terminal.querySelector('[data-verdict]');
    const run = terminal.querySelector('[data-run]');
    const flip = terminal.querySelector('[data-flip]');
    const reset = terminal.querySelector('[data-reset]');
    const drop = terminal.querySelector('[data-drop]');
    const file = document.querySelector('[data-demo-file]');
    const fingerprint = 'eca5654f…3ea2';
    let timers = [];
    live.hidden = false;
    fallback.hidden = true;
    const clear = () => { timers.forEach(clearTimeout); timers = []; };
    const add = (kind, label, detail) => {
      const item = document.createElement('li');
      item.className = 'is-' + kind;
      if (detail) {
        const strong = document.createElement('b');
        strong.textContent = label;
        item.append(strong, ' · ' + detail);
      } else item.textContent = label;
      out.append(item);
    };
    const setVerdict = (kind, text) => {
      verdict.className = 'tw-verdict' + (kind ? ' is-' + kind : '');
      verdict.textContent = text;
    };
    const sequence = (steps, done) => {
      clear();
      steps.forEach(([ms, action]) => timers.push(setTimeout(action, still ? 0 : ms)));
      const last = steps[steps.length - 1][0];
      timers.push(setTimeout(done, still ? 0 : last + 200));
    };
    function begin() {
      terminal.classList.add('has-run');
      out.textContent = '';
      setVerdict('', '');
      run.disabled = true;
      flip.disabled = true;
    }
    function check() {
      if (run.disabled) return;
      begin();
      sequence([
        [0, () => add('cmd', '$ python -m tgwitness.verify tgwitness-demo.zip --fingerprint ' + fingerprint + ' --plain')],
        [650, () => add('ok', W('home.js.signatures'), W('home.js.records'))],
        [1200, () => add('ok', W('home.js.chain'), W('home.js.links'))],
        [1750, () => add('ok', W('home.js.files'), W('home.js.filesOk'))],
        [2300, () => add('ok', W('home.js.key'), W('home.js.keyOk'))],
        [2750, () => add('raw', 'ASSURANCE: self_attested · signatures, hashes and record chain')],
        [3100, () => setVerdict('valid', W('home.js.valid'))]
      ], () => { run.disabled = false; flip.disabled = false; });
    }
    function tamper() {
      begin();
      sequence([
        [0, () => add('note', '# ' + W('home.js.flipped'))],
        [500, () => add('cmd', '$ python -m tgwitness.verify tgwitness-demo-changed.zip --fingerprint ' + fingerprint + ' --plain')],
        [1200, () => add('bad', 'VERIFICATION FAILED: ValueError: File hash mismatch: events.jsonl')],
        [1700, () => add('bad', 'ASSURANCE: fail')],
        [2000, () => setVerdict('bad', W('home.js.tampered'))]
      ], () => { run.disabled = false; });
    }
    function notRead() {
      clear();
      terminal.classList.add('has-run');
      out.textContent = '';
      setVerdict('', '');
      add('note', W('home.js.notRead'));
      add('cmd', '$ python -m tgwitness.verify YOUR-ARCHIVE.zip --fingerprint TRUSTED_SHA256 --plain');
      run.disabled = false;
      flip.disabled = true;
    }
    reset.addEventListener('click', () => {
      clear();
      terminal.classList.remove('has-run');
      out.textContent = '';
      setVerdict('', '');
      run.disabled = false;
      flip.disabled = true;
    });
    run.addEventListener('click', check);
    drop.addEventListener('click', check);
    flip.addEventListener('click', tamper);
    if (file) {
      file.addEventListener('dragstart', event => {
        event.dataTransfer.setData('application/x-tgwitness-demo', '1');
        file.classList.add('is-dragging');
      });
      file.addEventListener('dragend', () => file.classList.remove('is-dragging'));
    }
    ['dragenter', 'dragover'].forEach(type => terminal.addEventListener(type, event => {
      event.preventDefault();
      drop.classList.add('is-over');
    }));
    terminal.addEventListener('dragleave', event => { if (!terminal.contains(event.relatedTarget)) drop.classList.remove('is-over'); });
    terminal.addEventListener('drop', event => {
      event.preventDefault();
      drop.classList.remove('is-over');
      const types = [...(event.dataTransfer?.types || [])];
      if (types.includes('application/x-tgwitness-demo')) { terminal.classList.remove('has-run'); run.disabled = false; check(); }
      else if (types.includes('Files')) notRead();
    });
  }
}

const themeToggle = document.querySelector('[data-theme-toggle]');
if (themeToggle) {
  const sync = () => themeToggle.setAttribute('aria-pressed', String(document.documentElement.dataset.theme === 'dark'));
  themeToggle.hidden = false;
  sync();
  themeToggle.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.classList.add('theme-changing');
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('tgw-theme', next); } catch {                    }
    sync();
    setTimeout(() => document.documentElement.classList.remove('theme-changing'), 400);
  });
}

const languageMenu = document.querySelector('.lang-menu');
if (languageMenu) {
  document.addEventListener('click', event => { if (!languageMenu.contains(event.target)) languageMenu.open = false; });
  languageMenu.addEventListener('keydown', event => {
    if (event.key === 'Escape') { languageMenu.open = false; languageMenu.querySelector('summary').focus(); }
  });
}
