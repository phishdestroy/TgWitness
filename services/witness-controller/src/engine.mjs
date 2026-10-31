import { ZERO, MAX_BATCH, canonical, exact, isHash, isId, observation, randomToken, sha, sign, unb64, verify } from "./protocol.mjs";

export const DEFAULT_POLICY = Object.freeze({ min_interval_ms: 2000, max_interval_ms: 6000, response_timeout_ms: 12000, max_duration_ms: 86400000,
  action_min_delay_ms: 1000, action_max_delay_ms: 60000, permit_lifetime_ms: 5000 });
export function validateRegistration(body) {
  exact(body, ["observers"]);
  if (!Array.isArray(body.observers) || body.observers.length !== 3) throw new Error("Register exactly three observers");
  const ids = new Set(), keys = new Set(), kinds = new Set();
  for (const o of body.observers) {
    exact(o, ["id", "kind", "public_key", "declared_build_digest"]);
    if (!isId(o.id) || !["tgwitness", "desktop", "web"].includes(o.kind) || !isHash(o.declared_build_digest)) throw new Error("Invalid observer");
    unb64(o.public_key, 32);
    if (ids.has(o.id) || keys.has(o.public_key) || kinds.has(o.kind)) throw new Error("Observers must use distinct identities, keys and kinds");
    ids.add(o.id); keys.add(o.public_key); kinds.add(o.kind);
  }
}

// Pure transition engine. The host MUST serialize transitions and atomically persist
// the returned state, new receipts and next alarm. The storage adapter does this.
export class RunEngine {
  constructor(state, signingKey, publicKey, now = Date.now(), random = randomToken) {
    this.state = structuredClone(state); this.key = signingKey; this.publicKey = publicKey;
    this.now = now; this.random = random; this.receipts = [];
  }
  async emit(kind, data) {
    const s = this.state;
    const statement = { format: "tgwitness-controller-receipt-v1", run_id: s.run_id,
      index: ++s.index, previous: s.receipt_hash, at_ms: Math.max(this.now, s.last_time), kind, data };
    const receipt = { statement, hash: await sha(statement), signature: await sign(this.key, statement) };
    s.receipt_hash = receipt.hash; s.last_time = statement.at_ms; this.receipts.push(receipt);
    return receipt;
  }
  async incident(o, code, details = {}) {
    this.state.continuity_broken = true;
    this.state.incident_count++;
    if (o) { o.continuity_broken = true; o.incident_count++; }
    const receipt = await this.emit("incident", { observer_id: o?.id ?? null, code, ...details });
    await this.cancelAction("continuity_interrupted");
    return receipt;
  }
  jitter(min, max) {
    const p = this.state.policy;
    // Uniform bounded jitter; never an unbounded random delay.
    min ??= p.min_interval_ms; max ??= p.max_interval_ms;
    const range = max - min + 1;
    const cap = Math.floor(0x100000000 / range) * range;
    let value;
    do { value = crypto.getRandomValues(new Uint32Array(1))[0]; } while (value >= cap);
    return min + value % range;
  }
  async issue(o) {
    o.round++;
    o.challenge = { format: "tgwitness-challenge-v1", run_id: this.state.run_id, observer_id: o.id,
      round: o.round, nonce: this.random(), issued_at_ms: this.now,
      deadline_ms: this.now + this.state.policy.response_timeout_ms,
      previous_seq: o.seq, previous_hash: o.head, declared_build_digest: o.declared_build_digest };
    o.challenge_signature = await sign(this.key, o.challenge);
    o.bad_signature_reported = false;
    await this.emit("challenge_issued", { challenge: o.challenge });
  }
  async advance() {
    const s = this.state;
    if (s.closed) return;
    if (this.now < s.last_time) {
      await this.incident(null, "controller_clock_regressed");
      await this.close("controller_clock_regressed"); return;
    }
    for (const o of s.observers) {
      if (o.challenge && this.now >= o.challenge.deadline_ms) {
        await this.incident(o, "response_deadline_missed", { round: o.challenge.round, deadline_ms: o.challenge.deadline_ms, detected_at_ms: this.now });
        o.challenge = null; o.status = "silent"; o.next_due = this.now + this.jitter();
      }
    }
    if (this.now >= s.expires_at_ms) { await this.close("maximum_duration_reached"); return; }
    if (s.pending_action && this.now >= s.pending_action.expires_at_ms) await this.cancelAction("approval_window_expired");
    for (const o of s.observers) {
      if (!o.quarantined && !o.challenge && this.now >= o.next_due) {
        // A controller outage between challenges must not disappear on restart.
        if (this.now >= o.next_due + s.policy.response_timeout_ms) {
          await this.incident(o, "challenge_dispatch_overdue", { due_at_ms: o.next_due, detected_at_ms: this.now });
          o.status = "silent";
        }
        await this.issue(o);
      }
    }
  }
  async close(reason) {
    if (!this.state.closed) {
      await this.cancelAction("run_closed");
      this.state.closed = true;
      for (const o of this.state.observers) o.challenge = null;
      await this.emit("run_closed", { reason });
    }
  }
  nextAlarm() {
    if (this.state.closed) return null;
    return Math.min(this.state.expires_at_ms, this.state.pending_action?.expires_at_ms ?? Infinity,
      ...this.state.observers.filter((o) => !o.quarantined).map((o) => o.challenge?.deadline_ms ?? o.next_due));
  }
  async cancelAction(reason) {
    const pending = this.state.pending_action;
    if (!pending) return;
    this.state.pending_action = null;
    await this.emit("critical_action_cancelled", { request_id: pending.statement.request_id, observer_id: pending.statement.observer_id, reason });
  }
  async action(observerId, operation, envelope) {
    await this.advance();
    const s = this.state, o = s.observers.find((item) => item.id === observerId);
    if (!o || s.closed || s.continuity_broken || o.quarantined) return { status: 409, body: { error: "run_not_eligible_for_critical_change" } };
    if (!s.observers.every((v) => v.status === "responding")) return { status: 409, body: { error: "observers_not_ready" } };
    try { exact(envelope, ["statement", "signature"]); canonical(envelope); }
    catch { return { status: 400, body: { error: "invalid_envelope" } }; }
    const a = envelope.statement;
    if (!await verify(o.public_key, a, envelope.signature)) return { status: 401, body: { error: "invalid_observer_signature" } };
    try {
      exact(a, operation === "intent"
        ? ["format", "run_id", "observer_id", "request_id", "action", "parameters_sha256", "round", "nonce"]
        : ["format", "run_id", "observer_id", "request_id", "round", "nonce"]);
      unb64(a.request_id, 32);
      if (a.run_id !== s.run_id || a.observer_id !== observerId || a.format !== (operation === "intent" ? "tgwitness-action-intent-v1" : "tgwitness-action-claim-v1")) throw new Error();
      if (operation === "intent" && (!["change_proxy", "replace_session", "disconnect_account"].includes(a.action) || !isHash(a.parameters_sha256))) throw new Error();
    } catch { return { status: 400, body: { error: "invalid_signed_action" } }; }
    if (!o.challenge || a.round !== o.challenge.round || a.nonce !== o.challenge.nonce) return { status: 409, body: { error: "stale_or_foreign_challenge" } };
    if (operation === "intent") {
      if (s.pending_action) return { status: 409, body: { error: "another_action_pending" } };
      if (s.action_ids?.includes(a.request_id)) return { status: 409, body: { error: "action_id_already_used" } };
      if ((s.action_ids?.length ?? 0) >= 256) return { status: 409, body: { error: "action_limit_start_new_run" } };
      const ready = this.now + this.jitter(s.policy.action_min_delay_ms, s.policy.action_max_delay_ms);
      const receipt = await this.emit("critical_action_requested", { intent: envelope });
      (s.action_ids ??= []).push(a.request_id);
      s.pending_action = { statement: a, ready_at_ms: ready, expires_at_ms: ready + s.policy.max_interval_ms + s.policy.response_timeout_ms + 5000,
        receipt_index: receipt.statement.index };
      // Do not reveal the random release time before it passes.
      return { status: 202, body: { receipt, state: "waiting", poll_after_ms: 500 } };
    }
    const pending = s.pending_action;
    if (!pending || pending.statement.request_id !== a.request_id || pending.statement.observer_id !== observerId) return { status: 409, body: { error: "no_matching_pending_action" } };
    if (this.now < pending.ready_at_ms || !s.observers.every((v) => v.last_response_ms >= pending.ready_at_ms && v.last_receipt.statement.index > pending.receipt_index)) {
      return { status: 202, body: { state: "waiting_for_hold_and_fresh_responses", poll_after_ms: 500 } };
    }
    // An executor must persist request_id as consumed before applying the exact
    // parameter digest. Issuance is one-time; this receipt is not execution proof.
    const receipt = await this.emit("critical_action_permitted", { request_id: a.request_id, observer_id: observerId,
      action: pending.statement.action, parameters_sha256: pending.statement.parameters_sha256,
      valid_until_ms: this.now + s.policy.permit_lifetime_ms, hold_finished_at_ms: pending.ready_at_ms,
      claim: envelope, observer_heads: s.observers.map((v) => ({ observer_id: v.id, seq: v.seq, head: v.head, response_receipt: v.last_receipt.hash })) });
    s.pending_action = null;
    return { status: 200, body: { receipt, state: "permitted_once", execution_confirmed: false } };
  }
  async rejectSigned(o, code) {
    o.quarantined = true; o.challenge = null; o.status = "quarantined";
    await this.incident(o, code);
    return { status: 409, body: { error: code, quarantined: true } };
  }
  async answer(observerId, envelope) {
    await this.advance();
    const o = this.state.observers.find((item) => item.id === observerId);
    if (!o) return { status: 404, body: { error: "unknown_observer" } };
    if (this.state.closed || o.quarantined) return { status: 409, body: { error: "run_or_observer_closed" } };
    try { exact(envelope, ["statement", "signature"]); canonical(envelope); }
    catch { return { status: 400, body: { error: "invalid_envelope" } }; }
    const requestHash = await sha(envelope);
    if (requestHash === o.last_answer_hash) return { status: 200, body: { receipt: o.last_receipt, duplicate: true, continuity_broken: this.state.continuity_broken } };
    const a = envelope.statement;
    if (!await verify(o.public_key, a, envelope.signature)) {
      if (o.challenge && !o.bad_signature_reported) {
        o.bad_signature_reported = true;
        await this.incident(o, "signature_rejected", { round: o.challenge.round });
      }
      return { status: 401, body: { error: "invalid_observer_signature" } };
    }
    try {
      exact(a, ["format", "run_id", "observer_id", "round", "nonce", "declared_build_digest", "seq", "head", "entries", "capture_active", "source_status"]);
      if (a.format !== "tgwitness-answer-v1" || a.run_id !== this.state.run_id || a.observer_id !== o.id) throw new Error();
      if (!Number.isSafeInteger(a.seq) || a.seq < 0 || !isHash(a.head) || !Array.isArray(a.entries) || a.entries.length > MAX_BATCH || typeof a.capture_active !== "boolean" || !["connected", "reconnecting", "stopped"].includes(a.source_status)) throw new Error();
    } catch { return this.rejectSigned(o, "invalid_signed_statement"); }
    const c = o.challenge;
    if (!c || a.round !== c.round || a.nonce !== c.nonce) return { status: 409, body: { error: "stale_or_foreign_challenge" } };
    if (a.declared_build_digest !== o.declared_build_digest) return this.rejectSigned(o, "declared_build_changed");
    let seq = o.seq, head = o.head;
    try {
      for (const e of a.entries) {
        exact(e, ["seq", "previous", "payload_sha256", "hash"]);
        if (e.seq !== seq + 1 || e.previous !== head || !isHash(e.payload_sha256) || !isHash(e.hash)) throw new Error();
        const expected = await observation(this.state.run_id, o.id, e.seq, head, e.payload_sha256);
        if (expected.hash !== e.hash) throw new Error();
        seq = e.seq; head = e.hash;
      }
      if (a.seq !== seq || a.head !== head) throw new Error();
    } catch { return this.rejectSigned(o, "observation_chain_conflict"); }
    const previousStatus = o.status;
    const available = a.capture_active && a.source_status === "connected";
    if (!available && previousStatus !== "capture_unavailable") await this.incident(o, "capture_unavailable", { source_status: a.source_status });
    o.status = available ? "responding" : "capture_unavailable";
    o.seq = seq; o.head = head; o.last_response_ms = this.now;
    o.challenge = null; o.next_due = this.now + this.jitter();
    const receipt = await this.emit("answer_accepted", { observer_id: o.id, answer: envelope });
    if (available && ["silent", "capture_unavailable"].includes(previousStatus)) await this.emit("observer_recovered", { observer_id: o.id, continuity_broken: o.continuity_broken });
    o.last_answer_hash = requestHash; o.last_receipt = receipt;
    return { status: 200, body: { receipt, continuity_broken: this.state.continuity_broken } };
  }
  status() {
    const s = this.state;
    return { run_id: s.run_id, closed: s.closed, continuity_broken: s.continuity_broken,
      incident_count: s.incident_count, receipt_count: s.index, receipt_hash: s.receipt_hash,
      responsiveness: s.closed ? "closed" : s.observers.every((o) => o.status === "responding") ? "all_responding" : "incomplete",
      controller_public_key: this.publicKey,
      source_authenticity: "not_established", build_assurance: "observer_reported_only",
      pending_action: s.pending_action ? { request_id: s.pending_action.statement.request_id, observer_id: s.pending_action.statement.observer_id,
        action: s.pending_action.statement.action } : null,
      observers: s.observers.map(({ id, kind, status, seq, head, continuity_broken, last_response_ms, quarantined }) => ({ id, kind, status, seq, head, continuity_broken, last_response_ms, quarantined })) };
  }
}

export async function register(runId, body, signingKey, publicKey, now = Date.now(), policy = DEFAULT_POLICY) {
  validateRegistration(body);
  const readerToken = randomToken(), observerTokens = {};
  const observers = [];
  for (const descriptor of body.observers) {
    const token = randomToken(); observerTokens[descriptor.id] = token;
    observers.push({ ...descriptor, token_hash: await sha(token), seq: 0, head: ZERO, round: 0,
      status: "pending", continuity_broken: false, incident_count: 0, quarantined: false,
      challenge: null, next_due: now, last_response_ms: null, last_answer_hash: null, last_receipt: null });
  }
  const engine = new RunEngine({ run_id: runId, policy: { ...policy }, created_at_ms: now,
    expires_at_ms: now + policy.max_duration_ms, reader_hash: await sha(readerToken), controller_public_key: publicKey,
    index: 0, receipt_hash: ZERO, last_time: now, continuity_broken: false, incident_count: 0, closed: false, observers }, signingKey, publicKey, now);
  await engine.emit("run_registered", { observers: body.observers, policy: engine.state.policy, controller_public_key: publicKey,
    limitations: ["No runtime attestation", "No independent Telegram content verification", "External checkpoint retention required"] });
  await engine.advance();
  return { engine, readerToken, observerTokens };
}
