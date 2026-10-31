

export const ZERO = "0".repeat(64);
export const MAX_BATCH = 128;
const encoder = new TextEncoder();
export const bytes = (text) => encoder.encode(text);
export function canonical(value, depth = 0) {
  if (depth > 16) throw new Error("Object nesting exceeds protocol limit");
  if (value === null || typeof value === "boolean") return JSON.stringify(value);
  if (typeof value === "number" && Number.isSafeInteger(value)) return String(value);
  if (typeof value === "string") {
    if (value.length > 4096 || /[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]/u.test(value)) {
      throw new Error("Invalid protocol string");
    }
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) return `[${value.map((v) => canonical(v, depth + 1)).join(",")}]`;
  if (value && Object.getPrototypeOf(value) === Object.prototype) {
    return `{${Object.keys(value).sort().map((key) => `${canonical(key)}:${canonical(value[key], depth + 1)}`).join(",")}}`;
  }
  throw new Error("Unsupported protocol value");
}
export function b64(data) {
  return btoa(String.fromCharCode(...new Uint8Array(data))).replaceAll("+", "-").replaceAll("/", "_").replace(/=+$/, "");
}
export function unb64(text, length) {
  if (typeof text !== "string" || !/^[A-Za-z0-9_-]+$/.test(text) || text.length > 4096) throw new Error("Invalid base64url");
  const value = Uint8Array.from(atob(text.replaceAll("-", "+").replaceAll("_", "/")), (c) => c.charCodeAt(0));
  if ((length !== undefined && value.length !== length) || b64(value) !== text) throw new Error("Noncanonical base64url");
  return value;
}
export async function sha(value) {
  return Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", bytes(typeof value === "string" ? value : canonical(value)))), (b) => b.toString(16).padStart(2, "0")).join("");
}
export const randomToken = () => b64(crypto.getRandomValues(new Uint8Array(32)));
export const isHash = (v) => typeof v === "string" && /^[0-9a-f]{64}$/.test(v);
export const isId = (v) => typeof v === "string" && /^[a-z][a-z0-9_-]{0,31}$/.test(v);
export function exact(value, keys) {
  const actual = value && Object.keys(value).sort(), expected = [...keys].sort();
  if (!value || Object.getPrototypeOf(value) !== Object.prototype || actual.length !== expected.length || actual.some((key, i) => key !== expected[i])) {
    throw new Error("Unexpected protocol fields");
  }
}
export async function privateKey(encoded) {
  return crypto.subtle.importKey("pkcs8", unb64(encoded), "Ed25519", false, ["sign"]);
}
export async function sign(key, statement) {
  return b64(await crypto.subtle.sign("Ed25519", key, bytes(canonical(statement))));
}
export async function verify(publicKey, statement, signature) {
  try {
    const key = await crypto.subtle.importKey("raw", unb64(publicKey, 32), "Ed25519", false, ["verify"]);
    return await crypto.subtle.verify("Ed25519", key, unb64(signature, 64), bytes(canonical(statement)));
  } catch { return false; }
}
export async function generateKeys() {
  const keys = await crypto.subtle.generateKey("Ed25519", true, ["sign", "verify"]);
  return { publicKey: b64(await crypto.subtle.exportKey("raw", keys.publicKey)), privateKey: b64(await crypto.subtle.exportKey("pkcs8", keys.privateKey)) };
}
export async function observation(runId, observerId, seq, previous, payloadDigest) {
  const statement = { format: "tgwitness-observation-v1", run_id: runId, observer_id: observerId, seq, previous, payload_sha256: payloadDigest };
  return { seq, previous, payload_sha256: payloadDigest, hash: await sha(statement) };
}



export async function verifyBundle(bundle, checkpoint, publicKey) {
  if (bundle?.format !== "tgwitness-controller-export-v1" || !Array.isArray(bundle.receipts) || !bundle.receipts.length) throw new Error("Invalid receipt bundle");
  if (!checkpoint || !await verify(publicKey, checkpoint.statement, checkpoint.signature) || await sha(checkpoint.statement) !== checkpoint.hash) throw new Error("Invalid trusted checkpoint");
  let previous = ZERO, time = 0, incidents = 0, closed = false;
  const observers = new Map();
  let pendingAction = null, policy;
  const actionIds = new Set();
  const run = checkpoint.statement.run_id;
  for (let i = 0; i < bundle.receipts.length; i++) {
    const entry = bundle.receipts[i], s = entry.statement;
    if (s?.format !== "tgwitness-controller-receipt-v1" || s.run_id !== run || s.index !== i + 1 || s.previous !== previous || !Number.isSafeInteger(s.at_ms) || s.at_ms < time) throw new Error("Receipt history is reordered, truncated or inconsistent");
    if (i === 0 && s.kind !== "run_registered") throw new Error("Missing registration");
    if (!await verify(publicKey, s, entry.signature) || await sha(s) !== entry.hash) throw new Error("Invalid receipt signature");
    if (closed) throw new Error("Receipt after run closure");
    if (s.kind === "run_registered") {
      const descriptors = s.data?.observers;
      policy = s.data?.policy;
      if (i !== 0 || !Array.isArray(descriptors) || descriptors.length !== 3 || s.data.controller_public_key !== publicKey ||
          new Set(descriptors.map((o) => o.id)).size !== 3 || new Set(descriptors.map((o) => o.public_key)).size !== 3 ||
          new Set(descriptors.map((o) => o.kind)).size !== 3) throw new Error("Invalid observer registration");
      for (const o of descriptors) {
        if (!isId(o.id) || !["tgwitness", "desktop", "web"].includes(o.kind) || !isHash(o.declared_build_digest)) throw new Error("Invalid observer registration");
        unb64(o.public_key, 32);
        observers.set(o.id, { ...o, seq: 0, head: ZERO, challenge: null, answered: false });
      }
    } else if (s.kind === "challenge_issued") {
      const c = s.data?.challenge, o = observers.get(c?.observer_id);
      if (!o || c.format !== "tgwitness-challenge-v1" || c.run_id !== run || c.previous_seq !== o.seq || c.previous_hash !== o.head ||
          c.declared_build_digest !== o.declared_build_digest || c.issued_at_ms !== s.at_ms || !Number.isSafeInteger(c.deadline_ms) || c.deadline_ms <= s.at_ms) throw new Error("Invalid recorded challenge");
      unb64(c.nonce, 32); o.challenge = c;
    } else if (s.kind === "answer_accepted") {
      const o = observers.get(s.data?.observer_id), a = s.data?.answer?.statement, c = o?.challenge;
      if (!o || !c || !a || !await verify(o.public_key, a, s.data.answer.signature)) throw new Error("Invalid observer signature");
      if (a.format !== "tgwitness-answer-v1" || a.run_id !== run || a.observer_id !== o.id || a.nonce !== c.nonce || a.round !== c.round ||
          a.declared_build_digest !== o.declared_build_digest || s.at_ms >= c.deadline_ms || !Array.isArray(a.entries) || a.entries.length > MAX_BATCH) throw new Error("Invalid recorded answer");
      for (const e of a.entries) {
        if (e.seq !== o.seq + 1 || e.previous !== o.head || !isHash(e.payload_sha256) ||
            (await observation(run, o.id, e.seq, o.head, e.payload_sha256)).hash !== e.hash) throw new Error("Invalid observation chain");
        o.seq = e.seq; o.head = e.hash;
      }
      if (a.seq !== o.seq || a.head !== o.head) throw new Error("Invalid observation head");
      o.answered = true; o.challenge = null; o.response_at_ms = s.at_ms; o.response_receipt = entry.hash;
    } else if (s.kind === "critical_action_requested") {
      const envelope = s.data?.intent, a = envelope?.statement, o = observers.get(a?.observer_id), c = o?.challenge;
      if (pendingAction || incidents || !o || !c || !await verify(o.public_key, a, envelope.signature) ||
          a.format !== "tgwitness-action-intent-v1" || a.run_id !== run || a.round !== c.round || a.nonce !== c.nonce || s.at_ms >= c.deadline_ms ||
          !["change_proxy", "replace_session", "disconnect_account"].includes(a.action) || !isHash(a.parameters_sha256) || actionIds.has(a.request_id)) throw new Error("Invalid action intent");
      unb64(a.request_id, 32); actionIds.add(a.request_id);
      pendingAction = { statement: a, at_ms: s.at_ms };
    } else if (s.kind === "critical_action_cancelled") {
      if (!pendingAction || s.data?.request_id !== pendingAction.statement.request_id || s.data.observer_id !== pendingAction.statement.observer_id) throw new Error("Invalid action cancellation");
      pendingAction = null;
    } else if (s.kind === "critical_action_permitted") {
      const p = pendingAction, d = s.data, a = d?.claim?.statement, o = observers.get(a?.observer_id), c = o?.challenge;
      if (!p || incidents || !o || !c || !await verify(o.public_key, a, d.claim.signature) ||
          a.format !== "tgwitness-action-claim-v1" || a.run_id !== run || a.round !== c.round || a.nonce !== c.nonce || s.at_ms >= c.deadline_ms ||
          a.request_id !== p.statement.request_id || a.observer_id !== p.statement.observer_id || d.request_id !== a.request_id || d.observer_id !== a.observer_id ||
          d.action !== p.statement.action || d.parameters_sha256 !== p.statement.parameters_sha256 || !Number.isSafeInteger(d.hold_finished_at_ms) ||
          d.hold_finished_at_ms < p.at_ms + policy.action_min_delay_ms || d.hold_finished_at_ms > p.at_ms + policy.action_max_delay_ms ||
          s.at_ms < d.hold_finished_at_ms || d.valid_until_ms !== s.at_ms + policy.permit_lifetime_ms ||
          !Array.isArray(d.observer_heads) || d.observer_heads.length !== 3 || new Set(d.observer_heads.map((h) => h.observer_id)).size !== 3) throw new Error("Invalid critical action permit");
      for (const head of d.observer_heads) {
        const observer = observers.get(head.observer_id);
        if (!observer || !observer.answered || observer.response_at_ms < d.hold_finished_at_ms ||
            head.seq !== observer.seq || head.head !== observer.head || head.response_receipt !== observer.response_receipt) throw new Error("Permit lacks fresh observer responses");
      }
      pendingAction = null;
    } else if (s.kind === "run_closed") closed = true;
    else if (!["incident", "observer_recovered"].includes(s.kind)) throw new Error("Unknown receipt kind");
    if (s.kind === "incident") incidents++;
    previous = entry.hash; time = s.at_ms;
  }
  if (previous !== checkpoint.hash || bundle.receipts.length !== checkpoint.statement.index) throw new Error("Export does not reach the trusted checkpoint");
  const answered = [...observers.values()].filter((o) => o.answered).length;
  return { run_id: run, receipts: bundle.receipts.length, incidents, continuity_broken: incidents > 0,
    checkpoint_matched: true, observers_responded: answered, closed,
    continuity: incidents ? "interrupted" : answered === 3 ? "no_interruption_recorded_through_checkpoint" : "awaiting_observers",
    source_authenticity: "not_established" };
}
