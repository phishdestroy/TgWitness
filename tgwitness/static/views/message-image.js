const WIDTH = 640, PAGE = 1800, SCALE = 2, PAD = 32, LINE = 30;
const palettes = {
  light: {back: '#eef3ff', card: '#ffffff', ink: '#0f1728', muted: '#596377', accent: '#2563eb', rule: '#c9d8fd', alert: '#a32838'},
  dark: {back: '#0f1728', card: '#172334', ink: '#e5ebf2', muted: '#b2bfd1', accent: '#91baff', rule: '#33465f', alert: '#ffadb5'},
  classic: {back: '#ffffff', card: '#ffffff', ink: '#0f1728', muted: '#596377', accent: '#0f1728', rule: '#cfd4dc', alert: '#a32838'},
};
const rtl = value => /^[^\p{Letter}]*[\p{Script=Arabic}\p{Script=Hebrew}]/u.test(value);

export function createMessageImage({tr, mask = value => String(value ?? '')}) {
  let dialog = null, canvas = null, pages = [], data = null, page = 0, theme = 'light', generation = 0, current = () => false;
  let save, previous, next, position, notice, transcript, opener, downloadUrl = null;
  const make = (tag, text = '', cls = '') => {const el = document.createElement(tag);el.textContent = text;if (cls) el.className = cls;return el;};
  const font = (size, weight = 400, mono = false) => `${weight} ${size}px ${getComputedStyle(document.documentElement).getPropertyValue(mono ? '--mono' : '--font') || 'sans-serif'}`;
  function close() {
    generation++;pages = [];data = null;current = () => false;
    if (downloadUrl) URL.revokeObjectURL(downloadUrl);downloadUrl = null;
    if (canvas) canvas.width = canvas.height = 0;
    const old = dialog;dialog = canvas = transcript = save = previous = next = position = notice = null;
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
    const ctx = canvas.getContext('2d'), result = [], lineHeight = theme === 'classic' ? 26 : LINE;
    let sheet = {blocks: [], bottom: 120};
    const finish = () => {if (sheet.blocks.length) result.push(sheet);sheet = {blocks: [], bottom: 120};};
    for (const message of data.messages) {
      const content = [...lines(ctx, message.text, WIDTH - PAD * 2 - 40, theme === 'classic' ? 18 : 22),
        ...message.attachments.flatMap(label => lines(ctx, label, WIDTH - PAD * 2 - 40, 16))];
      const fragments = [];let offset = 0;
      const header = 68 + (message.status ? 24 : 0) + (message.reply ? 24 : 0);
      while (offset < content.length) {
        let capacity = Math.floor((PAGE - 66 - sheet.bottom - header - 20) / lineHeight);
        if (capacity < 1) {finish();capacity = Math.floor((PAGE - 66 - sheet.bottom - header - 20) / lineHeight);}
        const chunk = content.slice(offset, offset + capacity), height = header + chunk.length * lineHeight + 20;
        const block = {message, lines: chunk, y: sheet.bottom, height, lineHeight, part: fragments.length + 1};
        sheet.blocks.push(block);fragments.push(block);sheet.bottom += height + 14;offset += chunk.length;
        if (offset < content.length) finish();
      }
      for (const fragment of fragments) fragment.parts = fragments.length;
    }
    finish();return result;
  }
  function paint() {
    if (!dialog || !current()) {close();return;}
    const sheet = pages[page], colors = palettes[theme];if (!sheet) return;
    const height = Math.max(300, sheet.bottom + 48);
    canvas.width = WIDTH * SCALE;canvas.height = height * SCALE;
    const ctx = canvas.getContext('2d');ctx.scale(SCALE, SCALE);ctx.textBaseline = 'top';
    ctx.fillStyle = colors.back;ctx.fillRect(0, 0, WIDTH, height);
    const draw = (value, y, size, color, weight = 400, mono = false, inset = PAD, fit = false, direction = rtl(value)) => {
      ctx.font = font(size, weight, mono);ctx.fillStyle = color;ctx.direction = direction ? 'rtl' : 'ltr';ctx.textAlign = direction ? 'right' : 'left';
      let text = String(value), room = WIDTH - inset * 2;
      if (fit && ctx.measureText(text).width > room) {
        const chars = [...new Intl.Segmenter(undefined, {granularity: 'grapheme'}).segment(text)].map(item => item.segment);
        let low = 0, high = chars.length;
        while (low < high) {
          const middle = Math.ceil((low + high) / 2);
          if (ctx.measureText(chars.slice(0, middle).join('') + '…').width <= room) low = middle;else high = middle - 1;
        }
        text = chars.slice(0, low).join('') + '…';
      }
      ctx.fillText(text, direction ? WIDTH - inset : inset, y);
    };
    draw('TgWitness · ' + tr('Selected messages'), 24, 14, colors.accent, 600, false, PAD, true);
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
    draw(tr('Page') + ' ' + (page + 1) + ' / ' + pages.length, height - 30, 13, colors.muted);
    canvas.setAttribute('aria-label', tr('Selected messages') + ' · ' + (page + 1) + ' / ' + pages.length);
    transcript.textContent = accessible.filter(Boolean).join('\n');
    position.textContent = tr('Page') + ' ' + (page + 1) + ' / ' + pages.length;
    previous.disabled = page === 0;next.disabled = page === pages.length - 1;save.disabled = false;
    canvas.parentElement.scrollTop = 0;
    if (downloadUrl) URL.revokeObjectURL(downloadUrl);downloadUrl = null;
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
        if (downloadUrl) URL.revokeObjectURL(downloadUrl);
        downloadUrl = URL.createObjectURL(blob);
        const link = make('a');link.href = downloadUrl;link.download = `tgwitness-messages-${choice}-${index + 1}.png`;
        dialog.append(link);link.click();link.remove();
      }, 'image/png');
    } catch {
      if (ticket === generation && dialog) {save.disabled = false;notice.textContent = tr('Could not create the image. Try fewer messages.');}
    }
  }
  async function open(value, isCurrent) {
    close();current = isCurrent;
    if (!current()) return;
    if (!value.messages.length || value.messages.length > 50 || JSON.stringify(value).length > 200000) throw new Error(tr('Could not create the image. Try fewer messages.'));
    data = {title: mask(value.title), messages: value.messages.map(message => ({...message,
      author: mask(message.author), text: mask(message.text), status: mask(message.status), reply: mask(message.reply), attachments: message.attachments.map(mask)}))};
    opener = document.activeElement;page = 0;theme = document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';
    const ticket = generation;
    dialog = make('dialog', '', 'message-image-dialog');dialog.setAttribute('aria-labelledby', 'message-image-title');
    const head = make('div', '', 'message-image-head'), title = make('h2', tr('Save as image'));title.id = 'message-image-title';
    const exit = make('button', tr('Close'), 'quiet');exit.type = 'button';exit.addEventListener('click', close);head.append(title, exit);
    const description = make('p', tr('Text and attachment labels only. Long selections are split into pages.'), 'hint');
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
    save = make('button', tr('Download') + ' · PNG', 'primary');save.type = previous.type = next.type = 'button';
    previous.disabled = next.disabled = save.disabled = true;
    previous.addEventListener('click', () => {page--;paint();});next.addEventListener('click', () => {page++;paint();});save.addEventListener('click', download);
    footer.append(previous, position, next, save);notice = make('p', '', 'notice error');notice.setAttribute('role', 'alert');
    dialog.append(head, description, choices, preview, footer, notice);document.body.append(dialog);
    dialog.addEventListener('cancel', event => {event.preventDefault();close();});dialog.addEventListener('close', close);dialog.showModal();
    await document.fonts.ready;
    if (ticket !== generation || !dialog) return;
    if (!current()) {close();return;}
    try {pages = plan();paint();} catch {close();throw new Error(tr('Could not create the image. Try fewer messages.'));}
  }
  return {open, close};
}
