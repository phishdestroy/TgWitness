const WIDTH = 640, PAGE = 1800, SCALE = 2, PAD = 32, LINE = 30, FOOT = 168, QR = 112;
const LIMITS = {selection: [50, 200000], chat: [2000, 4000000]};
const palettes = {
  light: {back: '#eef3ff', card: '#ffffff', ink: '#0f1728', muted: '#596377', accent: '#2563eb', rule: '#c9d8fd', alert: '#a32838'},
  dark: {back: '#0f1728', card: '#172334', ink: '#e5ebf2', muted: '#b2bfd1', accent: '#91baff', rule: '#33465f', alert: '#ffadb5'},
  classic: {back: '#ffffff', card: '#ffffff', ink: '#0f1728', muted: '#596377', accent: '#0f1728', rule: '#cfd4dc', alert: '#a32838'},
};
const rtl = value => /^[^\p{Letter}]*[\p{Script=Arabic}\p{Script=Hebrew}]/u.test(value);
const K = new Uint32Array([0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
  0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
  0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb,
  0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f,
  0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]);
const hex = bytes => [...bytes].map(value => value.toString(16).padStart(2, '0')).join('');

function digest(bytes) {
  const length = bytes.length, total = Math.ceil((length + 9) / 64) * 64, data = new Uint8Array(total), view = new DataView(data.buffer);
  data.set(bytes);data[length] = 0x80;view.setUint32(total - 8, Math.floor(length / 0x20000000));view.setUint32(total - 4, length * 8 >>> 0);
  const hash = new Uint32Array([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]), w = new Uint32Array(64);
  const rotate = (value, bits) => (value >>> bits) | (value << (32 - bits));
  for (let offset = 0; offset < total; offset += 64) {
    for (let i = 0; i < 16; i++) w[i] = view.getUint32(offset + i * 4);
    for (let i = 16; i < 64; i++) {
      const a = w[i - 15], b = w[i - 2];
      w[i] = (w[i - 16] + (rotate(a, 7) ^ rotate(a, 18) ^ (a >>> 3)) + w[i - 7] + (rotate(b, 17) ^ rotate(b, 19) ^ (b >>> 10))) >>> 0;
    }
    let [a, b, c, d, e, f, g, h] = hash;
    for (let i = 0; i < 64; i++) {
      const t1 = (h + (rotate(e, 6) ^ rotate(e, 11) ^ rotate(e, 25)) + ((e & f) ^ (~e & g)) + K[i] + w[i]) >>> 0;
      const t2 = ((rotate(a, 2) ^ rotate(a, 13) ^ rotate(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))) >>> 0;
      h = g;g = f;f = e;e = (d + t1) >>> 0;d = c;c = b;b = a;a = (t1 + t2) >>> 0;
    }
    [a, b, c, d, e, f, g, h].forEach((value, i) => {hash[i] = (hash[i] + value) >>> 0;});
  }
  const out = new Uint8Array(32), result = new DataView(out.buffer);
  hash.forEach((value, i) => result.setUint32(i * 4, value));
  return out;
}

async function sha256(bytes) {
  if (globalThis.isSecureContext && globalThis.crypto?.subtle) return hex(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)));
  return hex(digest(bytes));
}

const CRC = new Uint32Array(256).map((_, n) => {let c = n;for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;return c >>> 0;});
function crc32(bytes) {let c = 0xffffffff;for (const value of bytes) c = CRC[(c ^ value) & 0xff] ^ (c >>> 8);return (c ^ 0xffffffff) >>> 0;}

function zip(files) {
  const encoder = new TextEncoder(), parts = [], central = [];let offset = 0;
  for (const file of files) {
    const name = encoder.encode(file.name), crc = crc32(file.bytes), size = file.bytes.length;
    const local = new DataView(new ArrayBuffer(30));
    [[0, 0x04034b50, 4], [4, 20, 2], [6, 0x0800, 2], [8, 0, 2], [10, 0, 2], [12, 0x21, 2], [14, crc, 4], [18, size, 4], [22, size, 4], [26, name.length, 2], [28, 0, 2]]
      .forEach(([at, value, width]) => width === 4 ? local.setUint32(at, value, true) : local.setUint16(at, value, true));
    const entry = new DataView(new ArrayBuffer(46));
    [[0, 0x02014b50, 4], [4, 20, 2], [6, 20, 2], [8, 0x0800, 2], [10, 0, 2], [12, 0, 2], [14, 0x21, 2], [16, crc, 4], [20, size, 4], [24, size, 4],
      [28, name.length, 2], [30, 0, 2], [32, 0, 2], [34, 0, 2], [36, 0, 2], [38, 0, 4], [42, offset, 4]]
      .forEach(([at, value, width]) => width === 4 ? entry.setUint32(at, value, true) : entry.setUint16(at, value, true));
    parts.push(local, name, file.bytes);central.push(entry, name);offset += 30 + name.length + size;
  }
  const size = central.reduce((sum, part) => sum + part.byteLength, 0), end = new DataView(new ArrayBuffer(22));
  [[0, 0x06054b50, 4], [8, files.length, 2], [10, files.length, 2], [12, size, 4], [16, offset, 4]]
    .forEach(([at, value, width]) => width === 4 ? end.setUint32(at, value, true) : end.setUint16(at, value, true));
  return new Blob([...parts, ...central, end], {type: 'application/zip'});
}

export function createMessageImage({tr, mask = value => String(value ?? ''), sign = null, qr = null}) {
  let dialog = null, canvas = null, pages = [], data = null, page = 0, theme = 'light', generation = 0, current = () => false, qrRows = null;
  let save, signed, previous, next, position, notice, progress, transcript, opener, downloadUrl = null;
  const make = (tag, text = '', cls = '') => {const el = document.createElement(tag);el.textContent = text;if (cls) el.className = cls;return el;};
  const font = (size, weight = 400, mono = false) => `${weight} ${size}px ${getComputedStyle(document.documentElement).getPropertyValue(mono ? '--mono' : '--font') || 'sans-serif'}`;
  const prefix = () => ['tgwitness', data.scope === 'chat' ? 'chat' : 'messages', String(data.chatId ?? '').replace(/[^0-9-]/g, ''), theme].filter(Boolean).join('-');
  const SIGNATURE = 'pages.sig.json';
  const pageName = index => 'page-' + String(index + 1).padStart(Math.max(2, String(pages.length).length), '0') + '.png';
  const records = sheet => [...new Set(sheet.blocks.map(block => block.message.record).filter(Number.isInteger))].sort((a, b) => a - b);
  function close() {
    generation++;pages = [];data = null;current = () => false;qrRows = null;
    if (downloadUrl) URL.revokeObjectURL(downloadUrl);downloadUrl = null;
    if (canvas) canvas.width = canvas.height = 0;
    const old = dialog;dialog = canvas = transcript = save = signed = previous = next = position = notice = progress = null;
    old?.replaceChildren();old?.remove();
    if (opener?.isConnected) opener.focus({preventScroll: true});opener = null;
  }
  function lines(ctx, value, width, size = 22) {
    ctx.font = font(size);
    const result = [], graphemes = new Intl.Segmenter(undefined, {granularity: 'grapheme'});
    for (const paragraph of String(value).replace(/\r\n?/g, '\n').split('\n')) {
      let line = '';
      const push = () => {result.push({text: line, rtl: rtl(paragraph), size});line = '';};
      for (const segment of paragraph.replace(/\t/g, '    ').split(/(\s+)/u)) {
        if (ctx.measureText(line + segment).width <= width) {line += segment;continue;}
        if (line) push();
        if (ctx.measureText(segment).width <= width) {line = segment;continue;}
        for (const {segment: char} of graphemes.segment(segment)) {
          if (line && ctx.measureText(line + char).width > width) push();
          line += char;
        }
      }
      push();
    }
    return result;
  }
  function plan() {
    const ctx = canvas.getContext('2d'), result = [], lineHeight = theme === 'classic' ? 26 : LINE, room = PAGE - 66 - FOOT;
    let sheet = {blocks: [], bottom: 120};
    const finish = () => {if (sheet.blocks.length) result.push(sheet);sheet = {blocks: [], bottom: 120};};
    for (const message of data.messages) {
      const content = [...lines(ctx, message.text, WIDTH - PAD * 2 - 40, theme === 'classic' ? 18 : 22),
        ...message.attachments.flatMap(label => lines(ctx, label, WIDTH - PAD * 2 - 40, 16))];
      const fragments = [];let offset = 0;
      const header = 68 + (message.status ? 24 : 0) + (message.reply ? 24 : 0);
      while (offset < content.length) {
        let capacity = Math.floor((room - sheet.bottom - header - 20) / lineHeight);
        if (capacity < 1) {finish();capacity = Math.floor((room - sheet.bottom - header - 20) / lineHeight);}
        const chunk = content.slice(offset, offset + capacity), height = header + chunk.length * lineHeight + 20;
        const block = {message, lines: chunk, y: sheet.bottom, height, lineHeight, part: fragments.length + 1};
        sheet.blocks.push(block);fragments.push(block);sheet.bottom += height + 14;offset += chunk.length;
        if (offset < content.length) finish();
      }
      for (const fragment of fragments) fragment.parts = fragments.length;
    }
    finish();return result;
  }
  function render(target, index) {
    const sheet = pages[index], colors = palettes[theme], height = Math.max(300, sheet.bottom + 16 + FOOT);
    target.width = WIDTH * SCALE;target.height = height * SCALE;
    const ctx = target.getContext('2d');ctx.scale(SCALE, SCALE);ctx.textBaseline = 'top';
    ctx.fillStyle = colors.back;ctx.fillRect(0, 0, WIDTH, height);
    const draw = (value, y, size, color, weight = 400, mono = false, inset = PAD, fit = false, direction = rtl(value), room = WIDTH - inset * 2) => {
      ctx.font = font(size, weight, mono);ctx.fillStyle = color;ctx.direction = direction ? 'rtl' : 'ltr';ctx.textAlign = direction ? 'right' : 'left';
      let text = String(value);
      if (fit && ctx.measureText(text).width > room) {
        const chars = [...new Intl.Segmenter(undefined, {granularity: 'grapheme'}).segment(text)].map(item => item.segment);
        let low = 0, high = chars.length;
        while (low < high) {
          const middle = Math.ceil((low + high) / 2);
          if (ctx.measureText(chars.slice(0, middle).join('') + '…').width <= room) low = middle;else high = middle - 1;
        }
        text = chars.slice(0, low).join('') + '…';
      }
      ctx.fillText(text, direction ? inset + room : inset, y);
    };
    draw('TgWitness · ' + (data.scope === 'chat' ? tr('Save chat as images') : tr('Selected messages')), 24, 14, colors.accent, 600, false, PAD, true);
    draw(data.title, 52, 23, colors.ink, 600, false, PAD, true);
    draw(tr('Rendered from saved messages'), 84, 13, colors.muted, 400, false, PAD, true);
    const accessible = [data.title, tr('Rendered from saved messages')];
    for (const block of sheet.blocks) {
      const {message, y, height: h} = block;
      ctx.fillStyle = colors.card;ctx.strokeStyle = colors.rule;ctx.lineWidth = 1;
      ctx.beginPath();ctx.roundRect(PAD, y, WIDTH - PAD * 2, h, theme === 'classic' ? 2 : 14);ctx.fill();ctx.stroke();
      const suffix = block.parts > 1 ? ` · ${block.part}/${block.parts}` : '';
      draw(message.author, y + 16, 19, colors.accent, 600, false, PAD + 20, true);
      draw('#' + message.id + ' · ' + message.time + suffix, y + 43, 12, colors.muted, 400, true, PAD + 20, true, false);
      let top = y + 68;
      if (message.status) {draw(message.status, top, 14, colors.alert, 600, false, PAD + 20, true);top += 24;}
      if (message.reply) {draw(message.reply, top, 14, colors.muted, 400, false, PAD + 20, true);top += 24;}
      for (const line of block.lines) {draw(line.text, top, line.size, line.size === 16 ? colors.muted : colors.ink, 400, false, PAD + 20, false, line.rtl);top += block.lineHeight;}
      accessible.push(message.author, '#' + message.id + ' · ' + message.time + suffix, message.status, message.reply, ...block.lines.map(line => line.text));
    }
    const foot = sheet.bottom + 8, ids = records(sheet), text = WIDTH - PAD * 2 - QR - 16;
    ctx.strokeStyle = colors.rule;ctx.beginPath();ctx.moveTo(PAD, foot);ctx.lineTo(WIDTH - PAD, foot);ctx.stroke();
    const footer = [
      ['TgWitness · ' + tr('Journal records') + ' ' + (ids.length ? '#' + ids[0] + (ids.length > 1 ? '–#' + ids.at(-1) : '') : '—'), 13, colors.ink, 600, false],
      [data.title + ' · ' + (data.chatId ?? ''), 12, colors.muted, 400, false],
      [data.rendered, 12, colors.muted, 400, true],
      [tr('Key') + ' ' + (data.fingerprint ? data.fingerprint.slice(0, 16).match(/.{4}/g).join(' ') + ' …' : '—'), 12, colors.muted, 400, true],
      [tr('Check') + ': verify.py ' + pageName(index) + (sign ? ' ' + SIGNATURE : ''), 11, colors.muted, 400, true],
      [tr('Page') + ' ' + (index + 1) + ' / ' + pages.length, 12, colors.muted, 400, false],
    ];
    footer.forEach(([value, size, color, weight, mono], row) => draw(value, foot + 14 + row * 23, size, color, weight, mono, PAD, true, false, text));
    accessible.push(...footer.map(([value]) => value));
    if (qrRows?.length) {
      const cells = qrRows.length, cell = Math.floor((QR - 8) / cells), side = cell * cells + 8, x = WIDTH - PAD - side, y = foot + 14;
      ctx.fillStyle = '#ffffff';ctx.fillRect(x, y, side, side);ctx.fillStyle = '#000000';
      qrRows.forEach((row, r) => [...row].forEach((bit, c) => {if (bit === '1') ctx.fillRect(x + 4 + c * cell, y + 4 + r * cell, cell, cell);}));
    }
    return accessible;
  }
  function paint() {
    if (!dialog || !current()) {close();return;}
    if (!pages[page]) return;
    const accessible = render(canvas, page);
    canvas.setAttribute('aria-label', tr('Selected messages') + ' · ' + (page + 1) + ' / ' + pages.length);
    transcript.textContent = accessible.filter(Boolean).join('\n');
    position.textContent = tr('Page') + ' ' + (page + 1) + ' / ' + pages.length;
    previous.disabled = page === 0;next.disabled = page === pages.length - 1;save.disabled = false;signed.disabled = !sign;
    canvas.parentElement.scrollTop = 0;
    if (downloadUrl) URL.revokeObjectURL(downloadUrl);downloadUrl = null;
  }
  function offer(blob, name) {
    if (downloadUrl) URL.revokeObjectURL(downloadUrl);
    downloadUrl = URL.createObjectURL(blob);
    const link = make('a');link.href = downloadUrl;link.download = name;
    dialog.append(link);link.click();link.remove();
  }
  function download() {
    if (!canvas || !current()) {close();return;}
    const ticket = generation, index = page, choice = theme, source = canvas;
    save.disabled = true;notice.textContent = '';
    try {
      source.toBlob(blob => {
        if (ticket !== generation || !dialog) return;
        if (!current()) {close();return;}
        save.disabled = false;
        if (page !== index || theme !== choice) return;
        if (!blob) {notice.textContent = tr('Could not create the image. Try fewer messages.');return;}
        offer(blob, prefix() + '-' + pageName(index));
      }, 'image/png');
    } catch {
      if (ticket === generation && dialog) {save.disabled = false;notice.textContent = tr('Could not create the image. Try fewer messages.');}
    }
  }
  async function downloadSigned() {
    if (!canvas || !current() || !sign) {close();return;}
    const ticket = generation, choice = theme, stale = () => ticket !== generation || !dialog || theme !== choice;
    const sheet = make('canvas'), files = [], body = {style: choice, pages: []};
    save.disabled = signed.disabled = true;notice.textContent = '';
    try {
      for (let index = 0; index < pages.length; index++) {
        progress.textContent = tr('Preparing page {n} of {total}', {n: index + 1, total: pages.length});
        render(sheet, index);
        const blob = await new Promise(resolve => sheet.toBlob(resolve, 'image/png'));
        if (stale()) return;
        if (!current()) {close();return;}
        if (!blob) throw new Error(tr('Could not create the image. Try fewer messages.'));
        const bytes = new Uint8Array(await blob.arrayBuffer());
        body.pages.push({sha256: await sha256(bytes), records: records(pages[index])});
        files.push({name: pageName(index), bytes});
      }
      progress.textContent = tr('Signed') + '…';
      const answer = await sign(data.chatId, body);
      if (stale()) return;
      if (!current()) {close();return;}
      const encoder = new TextEncoder(), names = files.map(file => file.name).join(' ');
      files.push({name: SIGNATURE, bytes: encoder.encode(JSON.stringify(answer, null, 1) + '\n')});
      files.push({name: 'README.txt', bytes: encoder.encode([
        'TgWitness rendered these PNG pages from signed journal records of chat ' + (data.chatId ?? '') + '.',
        SIGNATURE + ' binds the SHA-256 of every page to the records it shows and is signed with the workspace key',
        (answer.fingerprint || '') + '.', '',
        'Check the pages:', '  python verify.py ' + names + ' ' + SIGNATURE, '',
        'Add --fingerprint with the collector fingerprint you obtained from the sender through another channel,',
        'and --evidence with the evidence ZIP to confirm that every record is in the signed archive.',
        'The images show saved records; they do not show what Telegram displayed to anyone.', ''].join('\n'))});
      offer(zip(files), prefix() + '.zip');
      progress.textContent = '';
    } catch (error) {
      if (!stale()) {progress.textContent = '';notice.textContent = error?.message || tr('Could not create the image. Try fewer messages.');}
    } finally {
      if (!stale() && dialog) {save.disabled = false;signed.disabled = false;}
    }
  }
  async function open(value, isCurrent) {
    close();current = isCurrent;
    if (!current()) return;
    const [count, size] = LIMITS[value.scope] || LIMITS.selection;
    if (!value.messages.length || value.messages.length > count || JSON.stringify(value).length > size) throw new Error(tr('Could not create the image. Try fewer messages.'));
    const rendered = new Date().toISOString().replace('T', ' ').replace(/\.\d+Z$/, ' UTC');
    data = {title: mask(value.title), scope: value.scope || 'selection', chatId: value.chatId, fingerprint: value.fingerprint || '',
      rendered: tr('Rendered from saved messages') + ' · ' + rendered,
      messages: value.messages.map(message => ({...message,
        author: mask(message.author), text: mask(message.text), status: mask(message.status), reply: mask(message.reply), attachments: message.attachments.map(mask)}))};
    opener = document.activeElement;page = 0;theme = document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';
    const ticket = generation;
    dialog = make('dialog', '', 'message-image-dialog');dialog.setAttribute('aria-labelledby', 'message-image-title');
    const head = make('div', '', 'message-image-head'), title = make('h2', data.scope === 'chat' ? tr('Save chat as images') : tr('Save as image'));title.id = 'message-image-title';
    const exit = make('button', tr('Close'), 'quiet');exit.type = 'button';exit.addEventListener('click', close);head.append(title, exit);
    const description = make('p', [tr('Text and attachment labels only. Long selections are split into pages.'),
      sign ? tr('Each page names its journal records. The ZIP adds a signature file that verify.py checks.') : '',
      value.limited ? tr('Only the latest {n} saved messages are included.', {n: count}) : ''].filter(Boolean).join(' '), 'hint');
    description.id = 'message-image-description';dialog.setAttribute('aria-describedby', description.id);
    const choices = make('div', '', 'message-image-choices');choices.setAttribute('role', 'group');choices.setAttribute('aria-label', tr('Appearance'));
    for (const [key, label] of [['light', 'Light'], ['dark', 'Dark'], ['classic', 'Classic']]) {
      const button = make('button', tr(label), 'secondary');button.type = 'button';button.dataset.imageStyle = key;
      button.setAttribute('aria-pressed', String(theme === key));
      button.addEventListener('click', () => {
        theme = key;for (const item of choices.children) item.setAttribute('aria-pressed', String(item === button));
        if (pages.length) {pages = plan();page = 0;paint();}
      });
      choices.append(button);
    }
    const preview = make('div', '', 'message-image-preview');preview.setAttribute('tabindex', '0');preview.setAttribute('aria-label', tr('Preview'));
    canvas = make('canvas');canvas.setAttribute('role', 'img');transcript = make('pre', '', 'visually-hidden');preview.append(canvas, transcript);
    const footer = make('div', '', 'message-image-footer');
    previous = make('button', tr('Previous'), 'quiet');next = make('button', tr('Next'), 'quiet');
    position = make('span');position.setAttribute('role', 'status');position.setAttribute('aria-atomic', 'true');
    save = make('button', tr('Download') + ' · PNG', 'secondary');signed = make('button', tr('Download signed ZIP'), 'primary');
    save.type = signed.type = previous.type = next.type = 'button';signed.hidden = !sign;save.hidden = !!sign;signed.dataset.imageSigned = '';
    previous.disabled = next.disabled = save.disabled = signed.disabled = true;
    previous.addEventListener('click', () => {page--;paint();});next.addEventListener('click', () => {page++;paint();});
    save.addEventListener('click', download);signed.addEventListener('click', downloadSigned);
    footer.append(previous, position, next, save, signed);
    progress = make('p', '', 'hint message-image-progress');progress.setAttribute('role', 'status');
    notice = make('p', '', 'notice error');notice.setAttribute('role', 'alert');
    dialog.append(head, description, choices, preview, footer, progress, notice);document.body.append(dialog);
    dialog.addEventListener('cancel', event => {event.preventDefault();close();});dialog.addEventListener('close', close);dialog.showModal();
    const code = qr && sign ? qr('tgwitness-image chat=' + (data.chatId ?? '') + ' key=' + data.fingerprint + ' rendered=' + rendered).catch(() => null) : null;
    await document.fonts.ready;
    if (code) {const answer = await code;qrRows = Array.isArray(answer?.rows) ? answer.rows : null;}
    if (ticket !== generation || !dialog) return;
    if (!current()) {close();return;}
    try {pages = plan();paint();} catch {close();throw new Error(tr('Could not create the image. Try fewer messages.'));}
  }
  return {open, close};
}
