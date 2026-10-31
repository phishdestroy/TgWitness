import test from "node:test";
import assert from "node:assert/strict";
import { answerFor, fixture, resume } from "./helpers.mjs";
import { privateKey, randomToken, sign, verifyBundle } from "../src/protocol.mjs";

async function signedAction(f, operation, id, patch = {}) {
  const o = f.engine.state.observers[0], c = o.challenge;
  const statement = { format: operation === "intent" ? "tgwitness-action-intent-v1" : "tgwitness-action-claim-v1",
    run_id: f.engine.state.run_id, observer_id: o.id, request_id: id,
    ...(operation === "intent" ? { action: "change_proxy", parameters_sha256: "c".repeat(64) } : {}),
    round: c.round, nonce: c.nonce, ...patch };
  return { statement, signature: await sign(await privateKey(f.observers[0].keys.privateKey), statement) };
}
async function prepared() {
  const f = await fixture();
  for (const o of f.observers) await f.engine.answer(o.id, await answerFor(f.engine, o));
  f.receipts = [...f.engine.receipts];
  f.engine = resume(f, 106001); await f.engine.advance();
  f.requestId = randomToken();
  f.intent = await signedAction(f, "intent", f.requestId);
  assert.equal((await f.engine.action(f.observers[0].id, "intent", f.intent)).status, 202);
  f.ready = f.engine.state.pending_action.ready_at_ms;
  return f;
}
async function tick(f, time) {
  f.receipts.push(...f.engine.receipts);
  f.engine = resume(f, time); await f.engine.advance();
}

test("critical changes wait for a hidden bounded hold AND fresh answers from all three observers; permit is issued once", async () => {
  const f = await prepared(), o = f.observers[0];
  assert.ok(f.ready >= f.engine.now + 1000 && f.ready <= f.engine.now + 60000);
  assert.equal(JSON.stringify(f.engine.status()).includes(String(f.ready)), false, "Future release time is not disclosed");
  const early = await f.engine.action(o.id, "permit", await signedAction(f, "permit", f.requestId));
  assert.equal(early.status, 202);
  let granted;
  for (let time = 107001; time <= f.ready + 17000; time += 1000) {
    await tick(f, time);
    if (f.engine.state.observers[0].challenge) {
      const claim = await signedAction(f, "permit", f.requestId);
      const result = await f.engine.action(o.id, "permit", claim);
      if (result.status === 200) {
        granted = result;
        assert.equal((await f.engine.action(o.id, "permit", claim)).status, 409, "No second permit from replay");
        assert.equal((await f.engine.action(o.id, "intent", await signedAction(f, "intent", f.requestId))).body.error, "action_id_already_used");
        break;
      }
      assert.equal(result.status, 202);
    }
    for (const observer of f.observers) {
      if (f.engine.state.observers.find((x) => x.id === observer.id).challenge) {
        await f.engine.answer(observer.id, await answerFor(f.engine, observer, { payload: { time } }));
      }
    }
  }
  assert.ok(granted, "A healthy run eventually permits the intended change");
  assert.equal(granted.body.execution_confirmed, false);
  assert.equal(granted.body.receipt.statement.data.parameters_sha256, "c".repeat(64));
  assert.equal(granted.body.receipt.statement.data.valid_until_ms, f.engine.now + 5000);
  const receipts = [...f.receipts, ...f.engine.receipts];
  assert.equal((await verifyBundle({ format: "tgwitness-controller-export-v1", receipts }, receipts.at(-1), f.controller.publicKey)).continuity_broken, false);
});

test("blocking the verification channel cancels a pending critical change, and recovery cannot authorize it", async () => {
  const f = await prepared(), o = f.observers[0];
  await tick(f, 119000);
  assert.equal(f.engine.state.continuity_broken, true);
  assert.equal(f.engine.state.pending_action, null);
  assert.ok(f.engine.receipts.some((r) => r.statement.kind === "critical_action_cancelled" && r.statement.data.reason === "continuity_interrupted"));
  assert.equal((await f.engine.action(o.id, "permit", f.intent)).status, 409);
  const receipts = [...f.receipts, ...f.engine.receipts];
  assert.equal((await verifyBundle({ format: "tgwitness-controller-export-v1", receipts }, receipts.at(-1), f.controller.publicKey)).continuity_broken, true);
});

test("unsigned, stale, altered and overlapping action requests do not replace a pending operation", async () => {
  const f = await prepared(), o = f.observers[0];
  const second = await signedAction(f, "intent", randomToken());
  assert.equal((await f.engine.action(o.id, "intent", second)).body.error, "another_action_pending");
  second.statement.parameters_sha256 = "d".repeat(64);
  assert.equal((await f.engine.action(o.id, "intent", second)).status, 401);
  const stale = await signedAction(f, "permit", f.requestId, { nonce: randomToken() });
  assert.equal((await f.engine.action(o.id, "permit", stale)).body.error, "stale_or_foreign_challenge");
  assert.equal(f.engine.state.pending_action.statement.parameters_sha256, "c".repeat(64));
});

test("closing a run cancels a pending operation instead of leaving an executable authorization", async () => {
  const f = await prepared();
  await f.engine.close("operator_closed");
  assert.equal(f.engine.state.pending_action, null);
  assert.equal(f.engine.receipts.at(-2).statement.kind, "critical_action_cancelled");
  assert.equal((await f.engine.action(f.observers[0].id, "permit", f.intent)).status, 409);
});
