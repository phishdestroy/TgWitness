import test from "node:test";
import assert from "node:assert/strict";
import { fixture, answerFor, resume } from "./helpers.mjs";
import { canonical, privateKey, sha, sign, verify, verifyBundle, ZERO } from "../src/protocol.mjs";
import { validateRegistration } from "../src/engine.mjs";

test("registration pins three different observer keys and signed, unpredictable challenges", async () => {
  const f = await fixture(), e = f.engine;
  assert.equal(e.receipts.length, 4);
  assert.equal(new Set(e.state.observers.map((o) => o.challenge.nonce)).size, 3);
  for (const o of e.state.observers) {
    assert.equal(o.challenge.nonce.length, 43);
    assert.ok(await verify(f.controller.publicKey, o.challenge, o.challenge_signature));
  }
  const duplicate = structuredClone(f.body); duplicate.observers[1].public_key = duplicate.observers[0].public_key;
  assert.throws(() => validateRegistration(duplicate), /distinct/);
});

test("normal observations advance independent journals; responses do not claim source authenticity", async () => {
  const f = await fixture();
  for (const o of f.observers) {
    assert.equal((await f.engine.answer(o.id, await answerFor(f.engine, o, { payload: { text: "synthetic message" } }))).status, 200);
  }
  const s = f.engine.status();
  assert.equal(s.responsiveness, "all_responding");
  assert.equal(s.continuity_broken, false);
  assert.equal(s.source_authenticity, "not_established");
  assert.ok(s.observers.every((o) => o.seq === 1));
});

test("identical retry is idempotent; signed reply to a consumed challenge cannot advance history", async () => {
  const f = await fixture(), o = f.observers[0];
  const answer = await answerFor(f.engine, o, { payload: "first" });
  const first = await f.engine.answer(o.id, answer), count = f.engine.state.index;
  assert.equal((await f.engine.answer(o.id, answer)).body.duplicate, true);
  assert.equal(f.engine.state.index, count);
  const changed = structuredClone(answer); changed.statement.source_status = "reconnecting";
  changed.signature = await sign(await privateKey(o.keys.privateKey), changed.statement);
  assert.equal((await f.engine.answer(o.id, changed)).body.error, "stale_or_foreign_challenge");
  assert.equal(f.engine.state.index, count);
  assert.ok(first.body.receipt);
});

test("spoofed signatures are rejected and recorded without accepting the forged observation", async () => {
  const f = await fixture(), o = f.observers[0];
  const a = await answerFor(f.engine, o);
  a.signature = await sign(await privateKey(f.observers[1].keys.privateKey), a.statement);
  assert.equal((await f.engine.answer(o.id, a)).status, 401);
  assert.equal(f.engine.state.observers[0].seq, 0);
  assert.equal(f.engine.state.incident_count, 1);
  await f.engine.answer(o.id, a);
  assert.equal(f.engine.state.incident_count, 1, "Repeated unauthentic answers cannot multiply the same incident");
});

test("deadline violation survives recovery and serialized controller restart", async () => {
  const f = await fixture();
  f.engine = resume(f, 112000); await f.engine.advance();
  assert.equal(f.engine.state.incident_count, 3);
  const receipts = [...f.engine.receipts];
  f.engine = resume(f, 118001); await f.engine.advance();
  for (const o of f.observers) await f.engine.answer(o.id, await answerFor(f.engine, o));
  assert.equal(f.engine.status().responsiveness, "all_responding");
  assert.equal(f.engine.status().continuity_broken, true);
  assert.equal(f.engine.state.incident_count, 3);
  assert.equal(f.engine.receipts.filter((r) => r.statement.kind === "observer_recovered").length, 3);
  assert.equal(receipts.filter((r) => r.statement.kind === "incident").length, 3);
});

test("late signed answers cannot erase a missed deadline", async () => {
  const f = await fixture(), o = f.observers[0];
  const a = await answerFor(f.engine, o);
  f.engine = resume(f, 112001);
  assert.equal((await f.engine.answer(o.id, a)).status, 409);
  assert.equal(f.engine.state.incident_count, 3);
});

test("controller downtime between challenges is recorded after restart", async () => {
  const f = await fixture();
  for (const o of f.observers) await f.engine.answer(o.id, await answerFor(f.engine, o));
  f.engine = resume(f, 200000); await f.engine.advance();
  assert.equal(f.engine.state.incident_count, 3);
  assert.ok(f.engine.receipts.filter((r) => r.statement.kind === "incident").every((r) => r.statement.data.code === "challenge_dispatch_overdue"));
  for (const o of f.observers) await f.engine.answer(o.id, await answerFor(f.engine, o));
  assert.equal(f.engine.status().responsiveness, "all_responding");
  assert.equal(f.engine.status().continuity_broken, true);
});

for (const corruption of ["rollback", "rewrite", "skip", "bad_leaf"]) {
  test(`signed ${corruption} quarantines the observer and retains the prior head`, async () => {
    const f = await fixture(), o = f.observers[0];
    await f.engine.answer(o.id, await answerFor(f.engine, o, { payload: "original" }));
    const oldHead = f.engine.state.observers[0].head;
    f.engine = resume(f, 106001); await f.engine.advance();
    const a = await answerFor(f.engine, o, { payload: "next" });
    if (corruption === "rollback") { a.statement.entries = []; a.statement.seq = 0; a.statement.head = ZERO; }
    if (corruption === "rewrite") a.statement.entries[0].previous = ZERO;
    if (corruption === "skip") { a.statement.entries[0].seq++; a.statement.seq++; }
    if (corruption === "bad_leaf") a.statement.entries[0].payload_sha256 = "f".repeat(64);
    a.signature = await sign(await privateKey(o.keys.privateKey), a.statement);
    assert.equal((await f.engine.answer(o.id, a)).body.error, "observation_chain_conflict");
    assert.equal(f.engine.state.observers[0].head, oldHead);
    assert.equal(f.engine.state.observers[0].quarantined, true);
    assert.equal((await f.engine.answer(o.id, a)).status, 409);
  });
}

test("signed change of declared build is quarantined; no claim of runtime attestation", async () => {
  const f = await fixture(), o = f.observers[0];
  const a = await answerFor(f.engine, o, { patch: { declared_build_digest: "b".repeat(64) } });
  assert.equal((await f.engine.answer(o.id, a)).body.error, "declared_build_changed");
  assert.equal(f.engine.status().build_assurance, "observer_reported_only");
});

test("a responsive process with stopped capture is not shown as healthy", async () => {
  const f = await fixture(), o = f.observers[0];
  await f.engine.answer(o.id, await answerFor(f.engine, o, { patch: { capture_active: false, source_status: "stopped" } }));
  assert.equal(f.engine.state.observers[0].status, "capture_unavailable");
  assert.equal(f.engine.state.continuity_broken, true);
});

test("closed runs issue no more challenges and a backward controller clock closes the run", async () => {
  const f = await fixture(); f.engine = resume(f, 99999); await f.engine.advance();
  assert.equal(f.engine.state.closed, true);
  assert.equal(f.engine.nextAlarm(), null);
  assert.equal(f.engine.receipts[0].statement.data.code, "controller_clock_regressed");
});

test("pinned-key offline verification rejects tampering, omission, truncation and substituted trust roots", async () => {
  const f = await fixture();
  const receipts = [...f.engine.receipts];
  f.engine = resume(f, 112001); await f.engine.advance(); receipts.push(...f.engine.receipts);
  const bundle = { format: "tgwitness-controller-export-v1", receipts };
  const checkpoint = receipts.at(-1);
  assert.equal((await verifyBundle(bundle, checkpoint, f.controller.publicKey)).incidents, 3);
  const altered = structuredClone(bundle); altered.receipts[4].statement.data.code = "all_clear";
  await assert.rejects(verifyBundle(altered, checkpoint, f.controller.publicKey), /signature/);
  const omitted = structuredClone(bundle); omitted.receipts.splice(4, 1);
  await assert.rejects(verifyBundle(omitted, checkpoint, f.controller.publicKey), /inconsistent/);
  const truncated = structuredClone(bundle); truncated.receipts.pop();
  await assert.rejects(verifyBundle(truncated, checkpoint, f.controller.publicKey), /checkpoint/);
  await assert.rejects(verifyBundle(bundle, checkpoint, f.observers[0].keys.publicKey), /checkpoint/);
  await assert.rejects(verifyBundle(bundle, null, f.controller.publicKey), /checkpoint/);
});

test("canonical encoding rejects ambiguous values and unbounded nesting", async () => {
  assert.equal(canonical({ z: 2, a: "x" }), '{"a":"x","z":2}');
  for (const value of [NaN, Infinity, 1.5, undefined, 2 ** 54]) assert.throws(() => canonical(value));
  let nested = {}; for (let i = 0; i < 20; i++) nested = { nested };
  assert.throws(() => canonical(nested), /nesting/);
  assert.equal((await sha({ a: 1 })).length, 64);
});
