// Independent browser check of a TgWitness evidence archive (ZIP, ASiC-E or an unpacked folder).
// Nothing inside the archive is trusted or executed: the manifest signature, the SHA-256 of every member and the
// signed event chain are recomputed here with WebCrypto. The page policy forbids network connections.
(() => {
  'use strict';
  const DICT = (() => { try { return JSON.parse(document.getElementById('site-dict')?.textContent || '{}'); } catch { return {}; } })();
  const T = (text, values = {}) => (DICT[text] || text).replace(/\{(\w+)\}/g, (match, key) => key in values ? String(values[key]) : match);
  const $ = selector => document.querySelector(selector);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));

  const FIELDS = ['seq', 'observed_at', 'source_at', 'kind', 'chat_id', 'message_id', 'actor_id', 'payload', 'previous_hash'];
  const EVENT_KEYS = new Set([...FIELDS, 'hash', 'signature']);
  const ZERO = '0'.repeat(64);
  const ASIC_MIMETYPE = 'application/vnd.etsi.asic-e+zip';
  const NATIVE_HASH_LIMIT = 128 * 1024 * 1024;
  const MAX_SMALL = 64 * 1024 * 1024;
  const MAX_RECORD = 64 * 1024 * 1024;
  const MAX_MEMBERS = 500000;
  const BATCH = 512;

  const hex = bytes => Array.from(new Uint8Array(bytes), b => b.toString(16).padStart(2, '0')).join('');
  const fromHex = text => Uint8Array.from(text.match(/../g), pair => parseInt(pair, 16));
  const pause = () => new Promise(resolve => setTimeout(resolve, 0));
  const utf8 = new TextEncoder();

  class Failure extends Error {}
  const fail = message => { throw new Failure(message); };

  function base64(text, length) {
    if (typeof text !== 'string' || text.length % 4 || !/^[A-Za-z0-9+/]*={0,2}$/.test(text)) return null;
    let binary;
    try { binary = atob(text); } catch { return null; }
    const bytes = Uint8Array.from(binary, c => c.charCodeAt(0));
    return length == null || bytes.length === length ? bytes : null;
  }

  // ---- SHA-256 ------------------------------------------------------------------------------------------------
  // WebCrypto hashes whole buffers only; members larger than NATIVE_HASH_LIMIT are hashed incrementally here.
  const K = new Uint32Array([
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01,
    0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08,
    0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]);
  class Sha256 {
    constructor() {
      this.h = new Uint32Array([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]);
      this.buffer = new Uint8Array(64); this.filled = 0; this.total = 0; this.w = new Uint32Array(64);
    }
    update(data) {
      let p = 0;
      this.total += data.length;
      if (this.filled) {
        const take = Math.min(64 - this.filled, data.length);
        this.buffer.set(data.subarray(0, take), this.filled);
        this.filled += take; p = take;
        if (this.filled === 64) { this.block(this.buffer, 0); this.filled = 0; }
      }
      for (; p + 64 <= data.length; p += 64) this.block(data, p);
      if (p < data.length) { this.buffer.set(data.subarray(p), 0); this.filled = data.length - p; }
    }
    block(b, o) {
      const w = this.w, H = this.h;
      for (let i = 0; i < 16; i++) w[i] = (b[o + 4 * i] << 24) | (b[o + 4 * i + 1] << 16) | (b[o + 4 * i + 2] << 8) | b[o + 4 * i + 3];
      for (let i = 16; i < 64; i++) {
        const x = w[i - 15], y = w[i - 2];
        const s0 = ((x >>> 7) | (x << 25)) ^ ((x >>> 18) | (x << 14)) ^ (x >>> 3);
        const s1 = ((y >>> 17) | (y << 15)) ^ ((y >>> 19) | (y << 13)) ^ (y >>> 10);
        w[i] = (w[i - 16] + s0 + w[i - 7] + s1) | 0;
      }
      let a = H[0], bb = H[1], c = H[2], d = H[3], e = H[4], f = H[5], g = H[6], h = H[7];
      for (let i = 0; i < 64; i++) {
        const S1 = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
        const t1 = (h + S1 + ((e & f) ^ (~e & g)) + K[i] + w[i]) | 0;
        const S0 = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10));
        const t2 = (S0 + ((a & bb) ^ (a & c) ^ (bb & c))) | 0;
        h = g; g = f; f = e; e = (d + t1) | 0; d = c; c = bb; bb = a; a = (t1 + t2) | 0;
      }
      H[0] += a; H[1] += bb; H[2] += c; H[3] += d; H[4] += e; H[5] += f; H[6] += g; H[7] += h;
    }
    digest() {
      const bits = this.total * 8;
      const pad = new Uint8Array((this.filled < 56 ? 64 : 128) - this.filled);
      pad[0] = 0x80;
      const high = Math.floor(bits / 4294967296), low = bits >>> 0, end = pad.length;
      [high >>> 24, high >>> 16, high >>> 8, high, low >>> 24, low >>> 16, low >>> 8, low]
        .forEach((value, i) => { pad[end - 8 + i] = value & 255; });
      this.update(pad);
      return Array.from(this.h, word => word.toString(16).padStart(8, '0')).join('');
    }
  }
  const sha = async data => hex(await crypto.subtle.digest('SHA-256', data));

  // ---- Lossless JSON and Python-compatible canonical form -------------------------------------------------
  // Numbers keep their source text, so 64-bit Telegram identifiers survive; duplicate keys are refused, as the
  // Python verifier refuses them. canonical() reproduces json.dumps(ensure_ascii=False, sort_keys=True,
  // separators=(",", ":"), allow_nan=False) byte for byte.
  const NUMBER = /-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/y;
  function parseJSON(text) {
    let i = 0;
    const n = text.length;
    const bad = () => fail(T('The record is not valid JSON.'));
    const space = () => { while (i < n) { const c = text.charCodeAt(i); if (c === 32 || c === 9 || c === 10 || c === 13) i++; else break; } };
    function string() {
      i++;
      let out = '', start = i;
      for (;;) {
        if (i >= n) bad();
        const c = text.charCodeAt(i);
        if (c === 34) { out += text.slice(start, i); i++; return out; }
        if (c < 32) bad();
        if (c === 92) {
          out += text.slice(start, i);
          const e = text[i + 1];
          i += 2;
          if (e === 'u') {
            const code = text.slice(i, i + 4);
            if (!/^[0-9a-fA-F]{4}$/.test(code)) bad();
            out += String.fromCharCode(parseInt(code, 16)); i += 4;
          } else {
            const simple = {'"': '"', '\\': '\\', '/': '/', b: '\b', f: '\f', n: '\n', r: '\r', t: '\t'}[e];
            if (simple === undefined) bad();
            out += simple;
          }
          start = i;
          continue;
        }
        i++;
      }
    }
    function value(depth) {
      if (depth > 512) bad();
      space();
      const c = text[i];
      if (c === '{') {
        i++;
        const pairs = [], seen = new Set();
        space();
        if (text[i] === '}') { i++; return {t: 'o', pairs}; }
        for (;;) {
          space();
          if (text[i] !== '"') bad();
          const key = string();
          if (seen.has(key)) fail(T('Signed JSON contains a duplicate key.'));
          seen.add(key);
          space();
          if (text[i++] !== ':') bad();
          pairs.push([key, value(depth + 1)]);
          space();
          const next = text[i++];
          if (next === '}') return {t: 'o', pairs};
          if (next !== ',') bad();
        }
      }
      if (c === '[') {
        i++;
        const items = [];
        space();
        if (text[i] === ']') { i++; return {t: 'a', items}; }
        for (;;) {
          items.push(value(depth + 1));
          space();
          const next = text[i++];
          if (next === ']') return {t: 'a', items};
          if (next !== ',') bad();
        }
      }
      if (c === '"') return {t: 's', v: string()};
      if (text.startsWith('true', i)) { i += 4; return {t: 'l', v: 'true'}; }
      if (text.startsWith('false', i)) { i += 5; return {t: 'l', v: 'false'}; }
      if (text.startsWith('null', i)) { i += 4; return {t: 'l', v: 'null'}; }
      NUMBER.lastIndex = i;
      const found = NUMBER.exec(text);
      if (!found || !found[0]) bad();
      i += found[0].length;
      return {t: 'n', v: found[0]};
    }
    const result = value(0);
    space();
    if (i !== n) bad();
    return result;
  }
  const field = (node, name) => node && node.t === 'o' ? (node.pairs.find(pair => pair[0] === name) || [])[1] : undefined;
  const textOf = node => node && node.t === 's' ? node.v : null;
  const integerOf = node => node && node.t === 'n' && /^-?(?:0|[1-9]\d*)$/.test(node.v) && Number.isSafeInteger(Number(node.v)) ? Number(node.v) : null;

  function pythonFloat(raw) {
    const x = Number(raw);
    if (!Number.isFinite(x)) fail(T('The record is not valid JSON.'));
    if (x === 0) return Object.is(x, -0) ? '-0.0' : '0.0';
    const sign = x < 0 ? '-' : '';
    const [mantissa, power] = Math.abs(x).toExponential().split('e');
    const digits = mantissa.replace('.', ''), exponent = Number(power);
    if (exponent < -4 || exponent >= 16) {
      return sign + digits[0] + (digits.length > 1 ? '.' + digits.slice(1) : '') + 'e' + (exponent < 0 ? '-' : '+')
        + String(Math.abs(exponent)).padStart(2, '0');
    }
    if (exponent < 0) return sign + '0.' + '0'.repeat(-exponent - 1) + digits;
    const whole = digits.slice(0, exponent + 1).padEnd(exponent + 1, '0'), fraction = digits.slice(exponent + 1);
    return sign + whole + '.' + (fraction || '0');
  }
  const ESCAPES = {'"': '\\"', '\\': '\\\\', '\n': '\\n', '\r': '\\r', '\t': '\\t', '\b': '\\b', '\f': '\\f'};
  const pythonString = value => '"' + value.replace(/[\x00-\x1f"\\]/g, c => ESCAPES[c] || '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0')) + '"';
  const SURROGATE = /[\ud800-\udfff]/;
  function codePointOrder(a, b) {
    if (!SURROGATE.test(a) && !SURROGATE.test(b)) return a < b ? -1 : a > b ? 1 : 0;
    const x = Array.from(a, c => c.codePointAt(0)), y = Array.from(b, c => c.codePointAt(0));
    for (let i = 0; i < Math.min(x.length, y.length); i++) if (x[i] !== y[i]) return x[i] - y[i];
    return x.length - y.length;
  }
  function canonical(node) {
    switch (node.t) {
      case 'o': return '{' + node.pairs.slice().sort((p, q) => codePointOrder(p[0], q[0]))
        .map(([key, value]) => pythonString(key) + ':' + canonical(value)).join(',') + '}';
      case 'a': return '[' + node.items.map(canonical).join(',') + ']';
      case 's': return pythonString(node.v);
      case 'l': return node.v;
      default: return /^-?(?:0|[1-9]\d*)$/.test(node.v) ? BigInt(node.v).toString() : pythonFloat(node.v);
    }
  }

  // ---- Archive sources --------------------------------------------------------------------------------------
  const safeName = name => typeof name === 'string' && name.length > 0 && !/[\\\x00-\x1f\x7f:]/.test(name)
    && !name.startsWith('/') && name.split('/').every(part => part && part !== '.' && part !== '..');

  function zipSource(file) {
    let index = null;
    const invalid = () => new Failure(T('Invalid or ambiguous ZIP structure.'));
    const slice = async (a, b) => {
      if (!Number.isSafeInteger(a) || !Number.isSafeInteger(b) || a < 0 || b < a || b > file.size) throw invalid();
      return new Uint8Array(await file.slice(a, b).arrayBuffer());
    };
    const u16 = (b, o) => b[o] | b[o + 1] << 8, u32 = (b, o) => (b[o] | b[o + 1] << 8 | b[o + 2] << 16 | b[o + 3] << 24) >>> 0;
    const u64 = (b, o) => u32(b, o) + u32(b, o + 4) * 4294967296;
    async function entries() {
      if (index) return index;
      const tail = await slice(Math.max(0, file.size - 66000), file.size);
      let at = -1;
      for (let i = tail.length - 22; i >= 0; i--) if (u32(tail, i) === 0x06054b50 && i + 22 + u16(tail, i + 20) === tail.length) { at = i; break; }
      if (at < 0) fail(T('This is not a ZIP or ASiC-E file.'));
      if (u16(tail, at + 4) || u16(tail, at + 6) || u16(tail, at + 8) !== u16(tail, at + 10)) throw invalid();
      let count = u16(tail, at + 10), size = u32(tail, at + 12), offset = u32(tail, at + 16);
      if (at >= 20 && u32(tail, at - 20) === 0x07064b50) {
        const z = await slice(u64(tail, at - 20 + 8), u64(tail, at - 20 + 8) + 56);
        if (u32(z, 0) !== 0x06064b50 || u32(z, 16) || u32(z, 20) || u64(z, 24) !== u64(z, 32)) throw invalid();
        count = u64(z, 32); size = u64(z, 40); offset = u64(z, 48);
      }
      if (!Number.isSafeInteger(count) || count > MAX_MEMBERS || size > 256 * 1024 * 1024) throw invalid();
      const dir = await slice(offset, offset + size), found = new Map(), seen = new Set(), decoder = new TextDecoder('utf-8', {fatal: true});
      let p = 0;
      for (let n = 0; n < count; n++) {
        if (p + 46 > dir.length || u32(dir, p) !== 0x02014b50) throw invalid();
        const flags = u16(dir, p + 8), method = u16(dir, p + 10), nameLength = u16(dir, p + 28), extraLength = u16(dir, p + 30), commentLength = u16(dir, p + 32);
        if (flags & 1) fail(T('The ZIP is encrypted. Decrypt it first.'));
        if (u16(dir, p + 34) || p + 46 + nameLength + extraLength + commentLength > dir.length) throw invalid();
        let csize = u32(dir, p + 20), usize = u32(dir, p + 24), local = u32(dir, p + 42), name;
        try { name = decoder.decode(dir.subarray(p + 46, p + 46 + nameLength)); } catch { throw invalid(); }
        let e = p + 46 + nameLength;
        const end = e + extraLength;
        while (e + 4 <= end) {
          const id = u16(dir, e), length = u16(dir, e + 2);
          if (e + 4 + length > end) throw invalid();
          if (id === 1) {
            let q = e + 4;
            const take = () => { if (q + 8 > e + 4 + length) throw invalid(); const v = u64(dir, q); q += 8; return v; };
            if (usize === 0xFFFFFFFF) usize = take();
            if (csize === 0xFFFFFFFF) csize = take();
            if (local === 0xFFFFFFFF) local = take();
          }
          e += 4 + length;
        }
        const directory = name.endsWith('/'), clean = directory ? name.slice(0, -1) : name;
        if (e !== end) throw invalid();
        if (!safeName(clean)) fail(T('Unsafe member name in the archive: {name}', {name}));
        if (seen.has(clean)) fail(T('The archive lists {name} more than once.', {name: clean}));
        seen.add(clean);
        if (!Number.isSafeInteger(usize) || !Number.isSafeInteger(csize) || !Number.isSafeInteger(local) || local < 0 || local + 30 + csize > offset) throw invalid();
        if (!directory) found.set(name, {method, csize, usize, local, flags, limit: offset, first: n === 0});
        p = end + commentLength;
      }
      if (p !== dir.length) throw invalid();
      index = found;
      return index;
    }
    async function raw(name) {
      const en = (await entries()).get(name);
      if (!en) return null;
      const header = await slice(en.local, en.local + 30);
      if (u32(header, 0) !== 0x04034b50 || u16(header, 6) !== en.flags || u16(header, 8) !== en.method) throw invalid();
      const nameLength = u16(header, 26), start = en.local + 30 + nameLength + u16(header, 28);
      if (start + en.csize > en.limit) throw invalid();
      if (new TextDecoder().decode(await slice(en.local + 30, en.local + 30 + nameLength)) !== name) throw invalid();
      return {en, start};
    }
    async function* chunks(name) {
      const found = await raw(name);
      if (!found) return;
      const {en, start} = found;
      let stream = file.slice(start, start + en.csize).stream();
      if (en.method === 8) stream = stream.pipeThrough(new DecompressionStream('deflate-raw'));
      else if (en.method !== 0 || en.csize !== en.usize) fail(T('Unsupported compression in {name}', {name}));
      const reader = stream.getReader();
      let length = 0;
      try {
        for (;;) {
          const {value, done} = await reader.read();
          if (done) break;
          length += value.length;
          if (length > en.usize) throw invalid();
          yield value;
        }
      } catch (error) {
        if (error instanceof Failure) throw error;
        fail(T('{name} cannot be decompressed: the archive is damaged.', {name}));
      } finally {
        reader.releaseLock();
      }
      if (length !== en.usize) throw invalid();
    }
    return {
      kind: 'zip',
      list: async () => [...(await entries()).keys()],
      size: async name => (await entries()).get(name)?.usize ?? null,
      stored: async name => { const en = (await entries()).get(name); return !!en && en.method === 0 && en.first; },
      chunks,
    };
  }

  function folderSource(files) {
    const map = new Map();
    for (const [path, file] of files) {
      if (map.has(path)) fail(T('The archive lists {name} more than once.', {name: path}));
      if (!safeName(path)) fail(T('Unsafe member name in the archive: {name}', {name: path}));
      map.set(path, file);
    }
    async function* chunks(name) {
      const file = map.get(name);
      if (!file) return;
      const reader = file.stream().getReader();
      try {
        for (;;) { const {value, done} = await reader.read(); if (done) break; yield value; }
      } finally { reader.releaseLock(); }
    }
    return {kind: 'folder', list: async () => [...map.keys()], size: async name => map.get(name)?.size ?? null,
            stored: async () => true, chunks};
  }

  async function readAll(source, name, limit = MAX_SMALL) {
    const size = await source.size(name);
    if (size === null) return null;
    if (size > limit) fail(T('{name} is larger than this page accepts.', {name}));
    const result = new Uint8Array(size);
    let at = 0;
    for await (const chunk of source.chunks(name)) { result.set(chunk, at); at += chunk.length; }
    return result;
  }
  async function hashMember(source, name, onBytes) {
    const size = await source.size(name);
    if (size === null) return null;
    if (size <= NATIVE_HASH_LIMIT) {
      const data = await readAll(source, name, NATIVE_HASH_LIMIT);
      onBytes(data.length);
      return sha(data);
    }
    const state = new Sha256();
    let counted = 0;
    for await (const chunk of source.chunks(name)) {
      state.update(chunk);
      counted += chunk.length;
      onBytes(chunk.length);
      if (counted >= 64 * 1024 * 1024) { counted = 0; await pause(); }
    }
    return state.digest();
  }

  // ---- ASiC-E (ETSI EN 319 162) -------------------------------------------------------------------------------
  async function asicReferences(source, hashes, name, signature) {
    const bytes = await readAll(source, name);
    let xml;
    try { xml = new TextDecoder('utf-8', {fatal: true}).decode(bytes); } catch { return null; }
    if (/<!(DOCTYPE|ENTITY)/i.test(xml)) return null;
    const doc = new DOMParser().parseFromString(xml, 'application/xml');
    if (doc.getElementsByTagName('parsererror').length) return null;
    const NS = 'http://uri.etsi.org/02918/v1.2.1#', DS = 'http://www.w3.org/2000/09/xmldsig#';
    const signatures = [...doc.getElementsByTagNameNS(NS, 'SigReference')].map(node => node.getAttribute('URI'));
    const refs = [...doc.getElementsByTagNameNS(NS, 'DataObjectReference')];
    if (!refs.length || signatures.length !== 1 || signatures[0] !== signature) return null;
    const seen = new Set(), changed = [];
    for (const ref of refs) {
      let uri;
      try { uri = decodeURIComponent(ref.getAttribute('URI') || ''); } catch { return null; }
      const method = ref.getElementsByTagNameNS(DS, 'DigestMethod')[0]?.getAttribute('Algorithm');
      const value = base64(ref.getElementsByTagNameNS(DS, 'DigestValue')[0]?.textContent.trim() || '', 32);
      if (!safeName(uri) || uri === 'mimetype' || uri.startsWith('META-INF/') || seen.has(uri)
          || method !== 'http://www.w3.org/2001/04/xmlenc#sha256' || !value) return null;
      seen.add(uri);
      if (!hashes.has(uri) || hashes.get(uri) !== hex(value)) changed.push(uri);
    }
    return {seen, changed};
  }
  async function checkContainer(source, names, hashes, objects) {
    const result = {problems: [], references: 0, others: [], members: ['mimetype']};
    const mimetype = await readAll(source, 'mimetype', 1024);
    if (new TextDecoder().decode(mimetype) !== ASIC_MIMETYPE) return null;
    if (source.kind === 'zip' && !await source.stored('mimetype')) result.problems.push(T('The mimetype file is not the first, uncompressed entry'));
    if (!names.includes('META-INF/ASiCManifest.xml') || !names.includes('META-INF/signature.p7s')) {
      result.problems.push(T('META-INF/ASiCManifest.xml or META-INF/signature.p7s is missing'));
      return result;
    }
    result.members.push('META-INF/ASiCManifest.xml', 'META-INF/signature.p7s');
    const main = await asicReferences(source, hashes, 'META-INF/ASiCManifest.xml', 'META-INF/signature.p7s');
    if (!main) { result.problems.push(T('META-INF/ASiCManifest.xml cannot be read')); return result; }
    result.references = main.seen.size;
    if (main.changed.length) result.problems.push(T('Listed with a different SHA-256: {list}', {list: main.changed.slice(0, 30).join(', ')}));
    const unlisted = objects.filter(name => !main.seen.has(name));
    if (unlisted.length) result.problems.push(T('Not listed in the container manifest: {list}', {list: unlisted.slice(0, 30).join(', ')}));
    for (const name of names.filter(n => /^META-INF\/ASiCManifest[0-9]{3}\.xml$/.test(n) || n === 'META-INF/ASiCEvidenceRecordManifest.xml')) {
      const target = name === 'META-INF/ASiCEvidenceRecordManifest.xml' ? 'META-INF/evidencerecord.ers' : 'META-INF/signature' + name.slice(21, 24) + '.p7s';
      const other = names.includes(target) ? await asicReferences(source, hashes, name, target) : null;
      if (!other || other.changed.length || [...other.seen].some(n => !objects.includes(n))) {
        result.problems.push(T('{name} does not match the files it lists', {name}));
        continue;
      }
      result.members.push(name, target);
      result.others.push(target);
    }
    result.unknown = names.filter(n => (n === 'mimetype' || n.startsWith('META-INF/')) && !result.members.includes(n));
    if (result.unknown.length) result.problems.push(T('Not in the manifest (not covered by the signature): {list}', {list: result.unknown.slice(0, 30).join(', ')}));
    return result;
  }

  // ---- Event chain ------------------------------------------------------------------------------------------
  async function checkEvents(source, key, expectedCount, expectedHead, progress) {
    const decoder = new TextDecoder('utf-8', {fatal: true});
    let rest = '', count = 0, previous = ZERO, jobs = [];
    const settle = async () => {
      const outcomes = await Promise.all(jobs.map(job => job()));
      const broken = outcomes.find(Boolean);
      jobs = [];
      if (broken) fail(broken);
    };
    const line = text => {
      count++;
      const number = count;
      if (text.length > MAX_RECORD) fail(T('Event {n}: the record is larger than the verifier accepts.', {n: number}));
      let event;
      try { event = parseJSON(text); } catch (error) { fail(T('Event {n}: {reason}', {n: number, reason: error.message})); }
      if (event.t !== 'o' || event.pairs.length !== EVENT_KEYS.size || event.pairs.some(([name]) => !EVENT_KEYS.has(name))) {
        fail(T('Event {n}: unexpected or missing fields.', {n: number}));
      }
      const claimed = textOf(field(event, 'hash')), signature = base64(textOf(field(event, 'signature')), 64);
      if (integerOf(field(event, 'seq')) !== number || textOf(field(event, 'previous_hash')) !== previous) {
        fail(T('Event {n}: the sequence or the hash chain is broken.', {n: number}));
      }
      if (!claimed || !/^[0-9a-f]{64}$/.test(claimed) || !signature) fail(T('Event {n}: the hash or signature field is malformed.', {n: number}));
      const body = utf8.encode(canonical({t: 'o', pairs: event.pairs.filter(([name]) => FIELDS.includes(name))}));
      previous = claimed;
      jobs.push(async () => {
        if (await sha(body) !== claimed) return T('Event {n}: the content changed after it was signed.', {n: number});
        return await crypto.subtle.verify({name: 'Ed25519'}, key, signature, fromHex(claimed))
          ? null : T('Event {n}: the signature is not valid.', {n: number});
      });
    };
    // A structural fault is reported only after the queued earlier events are settled, so the first fault wins.
    const checked = async text => {
      try { line(text); } catch (error) { await settle(); throw error; }
    };
    let sinceYield = 0;
    for await (const chunk of source.chunks('events.jsonl')) {
      const parts = (rest + decodeUtf8(decoder, chunk, true)).split('\n');
      rest = parts.pop();
      if (rest.length > MAX_RECORD) fail(T('Event {n}: the record is larger than the verifier accepts.', {n: count + 1}));
      for (const part of parts) {
        await checked(part);
        if (jobs.length >= BATCH) { await settle(); progress(count, 0); sinceYield = 0; }
      }
      progress(count, chunk.length);
      if (++sinceYield >= 8) { sinceYield = 0; await pause(); }
    }
    rest += decodeUtf8(decoder, new Uint8Array(), false);
    if (rest.length) await checked(rest);
    await settle();
    if (count !== expectedCount) fail(T('The journal has {found} events; the signed manifest states {stated}.', {found: count, stated: expectedCount}));
    if (previous !== expectedHead) fail(T('The hash of the last event differs from the one stated in the signed manifest.'));
    return {count, head: previous};
  }
  function decodeUtf8(decoder, bytes, stream) {
    try { return decoder.decode(bytes, {stream}); } catch { return fail(T('events.jsonl is not valid UTF-8.')); }
  }

  // ---- The check ------------------------------------------------------------------------------------------------
  const state = {busy: false, result: null};
  const normalized = () => {
    const value = ($('#vf-fp').value || '').replace(/[\s:\-]/g, '').toLowerCase();
    return {value, invalid: !!value && !/^[a-f0-9]{64}$/.test(value)};
  };

  async function run(source, label) {
    if (state.busy) return;
    const wanted = normalized();
    if (wanted.invalid) { showFingerprintError(); $('#vf-fp').focus(); return; }
    state.busy = true;
    state.result = null;
    $('#vf-result').innerHTML = '';
    setBusy(true);
    const result = {label, checks: [], facts: [], at: new Date().toISOString()};
    const step = (status, text, detail = []) => result.checks.push({status, text, detail});
    try {
      progress(T('Reading the signed manifest…'), 0);
      const names = await source.list();
      const manifestBytes = await readAll(source, 'manifest.json');
      const signatureBytes = await readAll(source, 'manifest.sig', 4096);
      if (!manifestBytes || !signatureBytes) fail(T('manifest.json or manifest.sig is missing: this is not a TgWitness evidence archive.'));
      let manifestText;
      try { manifestText = new TextDecoder('utf-8', {fatal: true}).decode(manifestBytes); } catch { fail(T('manifest.json is not valid UTF-8.')); }
      const manifest = parseJSON(manifestText);
      if (manifest.t !== 'o') fail(T('manifest.json is not a signed bundle manifest.'));
      const format = textOf(field(manifest, 'format'));
      if (format !== 'tgwitness-evidence-v1' && format !== 'tgwatch-evidence-v1') {
        fail(T('This page checks evidence archives only; this archive has the format {format}. Use verify.py.', {format: format || '?'}));
      }
      const publicKey = base64(textOf(field(manifest, 'public_key')), 32);
      if (!publicKey) fail(T('manifest.json is not a signed bundle manifest.'));
      result.fingerprint = await sha(publicKey);
      let key;
      try { key = await crypto.subtle.importKey('raw', publicKey, {name: 'Ed25519'}, false, ['verify']); }
      catch { fail(T('This browser cannot check Ed25519 signatures. Use a current Chrome, Edge, Firefox or Safari, or verify.py.')); }
      const signature = base64(new TextDecoder().decode(signatureBytes).trim(), 64);
      const signed = !!signature && await crypto.subtle.verify({name: 'Ed25519'}, key, signature, utf8.encode(canonical(manifest)));
      step(signed ? 'ok' : 'bad', signed ? T('The manifest signature is valid (Ed25519).') : T('The manifest signature is NOT valid.'));
      if (!signed) throw new Failure('');
      result.facts.push([T('Key fingerprint in the archive'), result.fingerprint]);
      const stated = [['report', 'id', T('Report')], ['created_at', null, T('Created')], ['event_count', null, T('Events')], ['head_hash', null, T('Last event hash')]];
      for (const [name, inner, title] of stated) {
        const node = inner ? field(field(manifest, name), inner) : field(manifest, name);
        if (node && (node.t === 's' || node.t === 'n')) result.facts.push([title, node.v]);
      }

      const files = field(manifest, 'files');
      if (!files || files.t !== 'o' || !files.pairs.length) fail(T('The signed manifest has no valid file list.'));
      const listed = new Map();
      for (const [name, digest] of files.pairs) {
        if (!safeName(name) || name === 'manifest.json' || name === 'manifest.sig' || !/^[0-9a-f]{64}$/.test(textOf(digest) || '')) {
          fail(T('The signed manifest lists an unsafe file name or an invalid hash: {name}', {name}));
        }
        listed.set(name, digest.v);
      }
      const container = !listed.has('mimetype') && names.includes('mimetype');
      const outside = container ? names.filter(n => !listed.has(n) && (n === 'mimetype' || n.startsWith('META-INF/'))) : [];
      const extra = names.filter(n => !listed.has(n) && n !== 'manifest.json' && n !== 'manifest.sig' && !outside.includes(n));
      const missing = [...listed.keys()].filter(n => !names.includes(n));
      let total = 0;
      for (const name of listed.keys()) total += (await source.size(name)) || 0;
      let done = 0, filesDone = 0;
      const hashes = new Map(), changed = [];
      for (const name of listed.keys()) {
        if (missing.includes(name)) continue;
        const digest = await hashMember(source, name, bytes => {
          done += bytes;
          progress(T('Checking files: {a} of {b}', {a: filesDone + 1, b: listed.size}), total ? done / total : 1);
        });
        hashes.set(name, digest);
        if (digest !== listed.get(name)) changed.push(name);
        filesDone++;
        if (filesDone % 20 === 0) await pause();
      }
      const filesOk = !changed.length && !missing.length && !extra.length;
      step(filesOk ? 'ok' : 'bad', filesOk ? T('All {n} files match their SHA-256 in the signed manifest; no file is missing or added.', {n: listed.size})
        : T('The files do not match the signed manifest.'), [
        ...(changed.length ? [T('Changed: {list}', {list: changed.slice(0, 30).join(', ')})] : []),
        ...(missing.length ? [T('Missing: {list}', {list: missing.slice(0, 30).join(', ')})] : []),
        ...(extra.length ? [T('Not in the manifest (not covered by the signature): {list}', {list: extra.slice(0, 30).join(', ')})] : []),
      ]);

      if (container) {
        const objects = names.filter(n => n !== 'mimetype' && !n.startsWith('META-INF/'));
        for (const name of ['manifest.json', 'manifest.sig']) hashes.set(name, await sha(await readAll(source, name)));
        const asic = await checkContainer(source, names, hashes, objects);
        if (!asic) {
          step('bad', T('The archive contains a mimetype entry that is not an ASiC-E container.'));
        } else {
          step(asic.problems.length ? 'bad' : 'ok', asic.problems.length ? T('The ASiC-E container is damaged.')
            : T('ASiC-E container recognized: its manifest lists {n} files and their SHA-256 match.', {n: asic.references}),
          [...asic.problems, T('The container signature (META-INF/signature.p7s) was not checked on this page.'),
           ...(asic.others.length ? [T('Other container signatures not checked on this page: {list}', {list: asic.others.join(', ')})] : []),
           ...(asic.unknown.length ? [T('Other container entries not checked on this page: {list}', {list: asic.unknown.join(', ')})] : [])]);
        }
      }

      const expectedCount = integerOf(field(manifest, 'event_count')), expectedHead = textOf(field(manifest, 'head_hash'));
      if (!listed.has('events.jsonl') || missing.includes('events.jsonl')) {
        step('bad', T('events.jsonl is missing: the event chain cannot be checked.'));
      } else if (expectedCount === null || !/^[0-9a-f]{64}$/.test(expectedHead || '')) {
        step('bad', T('The signed manifest does not state the event count and the last event hash.'));
      } else {
        const size = await source.size('events.jsonl');
        let read = 0;
        try {
          const chain = await checkEvents(source, key, expectedCount, expectedHead, (events, bytes) => {
            read += bytes;
            progress(T('Checking the event chain: {n} events so far', {n: events.toLocaleString()}), size ? Math.min(1, read / size) : 1);
          });
          step('ok', T('The event chain is intact: {n} events in sequence, every hash recomputed and every signature valid; the count and the last hash match the signed manifest.', {n: chain.count.toLocaleString()}));
        } catch (error) {
          if (!(error instanceof Failure)) throw error;
          step('bad', T('The event chain is broken.'), [error.message]);
        }
      }
    } catch (error) {
      if (error instanceof Failure) { if (error.message) step('bad', error.message); }
      else step('bad', T('The check stopped: {reason}', {reason: error && error.message ? error.message : String(error)}));
    } finally {
      state.busy = false;
      state.result = result;
      setBusy(false);
      render();
    }
  }

  // ---- Interface ----------------------------------------------------------------------------------------------
  function setBusy(busy) {
    for (const node of document.querySelectorAll('#vf-pick-file,#vf-pick-dir,#vf-file,#vf-dir')) node.disabled = busy;
    $('#vf-status').hidden = !busy;
    $('#vf-drop').classList.toggle('busy', busy);
    if (!busy) { $('#vf-file').value = ''; $('#vf-dir').value = ''; }
  }
  let lastPaint = 0;
  function progress(text, fraction) {
    const now = performance.now();
    if (now - lastPaint < 80 && fraction < 1) return;
    lastPaint = now;
    $('#vf-progress').value = Math.max(0, Math.min(1, fraction));
    $('#vf-progress-text').textContent = text;
  }
  function showFingerprintError() {
    $('#vf-fp-error').textContent = normalized().invalid ? T('A key fingerprint is 64 hexadecimal characters (SHA-256). Spaces, colons and dashes are ignored.') : '';
  }
  function render() {
    const result = state.result;
    if (!result) return;
    const wanted = normalized(), given = !!wanted.value && !wanted.invalid;
    const integrity = result.checks.length > 0 && result.checks.every(check => check.status === 'ok') && !!result.fingerprint;
    const foreign = given && result.fingerprint && wanted.value !== result.fingerprint;
    const trusted = integrity && given && !foreign;
    const verdict = !integrity || foreign ? 'bad' : trusted ? 'ok' : 'warn';
    const heading = !integrity ? T('This archive did NOT pass the check.')
      : foreign ? T('The archive is signed by a different key than the fingerprint from the sender.')
        : trusted ? T('The archive is intact and signed by the key the sender named.')
          : T('The archive is intact, but its key has not been compared with a fingerprint from the sender.');
    const key = !result.fingerprint ? null : foreign
      ? {status: 'bad', text: T('The key does NOT match the fingerprint from the sender.'),
         detail: [T('Fingerprint from the sender: {fp}', {fp: wanted.value}), T('Key fingerprint in the archive: {fp}', {fp: result.fingerprint})]}
      : given ? {status: 'ok', text: T('The key matches the fingerprint you entered: {fp}', {fp: result.fingerprint}), detail: []}
        : {status: 'warn', text: T('The key has not been compared with a fingerprint from the sender.'),
           detail: [T('Key fingerprint in the archive: {fp}', {fp: result.fingerprint}),
                    T('Files can match a manifest signed by any key. Paste the fingerprint you received from the sender separately, for example by phone, to confirm whose key signed this archive.')]};
    const items = [...result.checks.slice(0, 1), ...(key ? [key] : []), ...result.checks.slice(1)];
    const icon = status => status === 'ok' ? '✓' : status === 'warn' ? '!' : '✕';
    $('#vf-result').innerHTML = '<div class="vf-verdict ' + verdict + '"><h2>' + esc(heading) + '</h2><ul class="vf-checks">'
      + items.map(item => '<li class="' + item.status + '"><span class="vf-icon" aria-hidden="true">' + icon(item.status) + '</span><div><b>'
        + esc(item.text) + '</b>' + (item.detail.length ? '<ul>' + item.detail.map(line => '<li>' + esc(line) + '</li>').join('') + '</ul>' : '')
        + '</div></li>').join('') + '</ul>'
      + (result.facts.length ? '<dl class="vf-facts">' + result.facts.map(([title, value]) => '<dt>' + esc(title) + '</dt><dd><code>' + esc(value) + '</code></dd>').join('') + '</dl>' : '')
      + '<p class="vf-limits">' + esc(T('Checked on this page: the manifest signature, the SHA-256 of every file and the signed event chain. Time stamps, OpenTimestamps, container and PDF signatures, Intel TDX and witness records are not checked here; see below.')) + '</p>'
      + '<p class="vf-when">' + esc(T('Checked {name} in this browser at {time}. Nothing was uploaded.', {name: result.label, time: result.at})) + '</p></div>';
  }

  async function filesFromDrop(items) {
    const entries = [...items].map(item => item.webkitGetAsEntry && item.webkitGetAsEntry()).filter(Boolean);
    if (entries.length === 1 && entries[0].isFile) return {file: await new Promise((resolve, reject) => entries[0].file(resolve, reject))};
    if (entries.length !== 1 || !entries[0].isDirectory) fail(T('Drop one ZIP or ASiC-E file, or one unpacked folder.'));
    const found = [];
    async function walk(directory, prefix) {
      const reader = directory.createReader();
      for (;;) {
        const batch = await new Promise((resolve, reject) => reader.readEntries(resolve, reject));
        if (!batch.length) break;
        for (const entry of batch) {
          if (entry.isDirectory) await walk(entry, prefix + entry.name + '/');
          else found.push([prefix + entry.name, await new Promise((resolve, reject) => entry.file(resolve, reject))]);
        }
      }
    }
    await walk(entries[0], '');
    return {folder: found, name: entries[0].name};
  }

  function start() {
    if (!window.crypto || !crypto.subtle || typeof DecompressionStream === 'undefined') {
      $('#vf-result').innerHTML = '<div class="vf-verdict bad"><h2>' + esc(T('This browser cannot run the check. Use a current Chrome, Edge, Firefox or Safari, or verify.py.')) + '</h2></div>';
      return;
    }
    $('#vf-pick-file').addEventListener('click', () => $('#vf-file').click());
    $('#vf-pick-dir').addEventListener('click', () => $('#vf-dir').click());
    $('#vf-file').addEventListener('change', event => {
      const file = event.target.files[0];
      if (file) run(zipSource(file), file.name);
    });
    $('#vf-dir').addEventListener('change', event => {
      const files = [...event.target.files];
      if (!files.length) return;
      const top = files[0].webkitRelativePath.split('/')[0];
      try { run(folderSource(files.map(file => [file.webkitRelativePath.split('/').slice(1).join('/'), file])), top); }
      catch (error) { state.result = {label: top, checks: [{status: 'bad', text: error.message, detail: []}], facts: [], at: new Date().toISOString()}; render(); }
    });
    const drop = $('#vf-drop');
    drop.addEventListener('dragover', event => { event.preventDefault(); drop.classList.add('over'); });
    drop.addEventListener('dragleave', () => drop.classList.remove('over'));
    drop.addEventListener('drop', async event => {
      event.preventDefault();
      drop.classList.remove('over');
      if (state.busy) return;
      try {
        const dropped = await filesFromDrop(event.dataTransfer.items);
        if (dropped.file) run(zipSource(dropped.file), dropped.file.name);
        else run(folderSource(dropped.folder), dropped.name);
      } catch (error) {
        state.result = {label: '', checks: [{status: 'bad', text: error.message, detail: []}], facts: [], at: new Date().toISOString()};
        render();
      }
    });
    $('#vf-fp').addEventListener('input', () => { showFingerprintError(); if (!state.busy) render(); });
  }
  start();
})();
