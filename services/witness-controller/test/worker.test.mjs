import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { build } from "esbuild";
import { Miniflare, convertV4MiniflareOptions } from "miniflare";
import { identities } from "./helpers.mjs";
import { privateKey, randomToken, sign, verifyBundle } from "../src/protocol.mjs";
import { syntheticAnswer } from "../tools/synthetic.mjs";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
test("real Worker: role separation, concurrent replay, durable restart, immutable receipts and timed alarms", { timeout: 60000 }, async (t) => {
  const f = await identities(), admin = randomToken();
  const out = await build({ entryPoints: ["src/worker.mjs"], bundle: true, format: "esm", platform: "neutral", external: ["cloudflare:workers"], write: false });
  const storage = await mkdtemp(join(tmpdir(), "tgwitness-controller-test-"));
  const options = convertV4MiniflareOptions({ name: "tgwitness-controller-test", modules: true, script: out.outputFiles[0].text,
    compatibilityDate: "2026-07-30", host: "127.0.0.1", port: 0, cf: false,
    unsafeEnableDevRegistry: false, unsafeInspectDurableObjects: true, resourcePersistencePath: storage,
    durableObjects: { RUNS: { className: "WitnessRun", useSQLite: true } },
    bindings: { ADMIN_TOKEN: admin, WITNESS_PRIVATE_KEY: f.controller.privateKey, WITNESS_PUBLIC_KEY: f.controller.publicKey } });
  let mf = new Miniflare(options); t.after(async () => { await mf.dispose(); });
  const call = async (path, token, body) => {
    const r = await mf.dispatchFetch(`http://localhost${path}`, { method: body === undefined ? "GET" : "POST",
      headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(body === undefined ? {} : { "Content-Type": "application/json" }) },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }) });
    return { status: r.status, body: await r.json() };
  };
  assert.equal((await call("/v1/runs", undefined, f.body)).status, 401);
  const created = await call("/v1/runs", admin, f.body);
  assert.equal(created.status, 201, JSON.stringify(created.body));
  const r = created.body, base = `/v1/runs/${r.run_id}`;
  assert.equal((await call(base, admin, f.body)).status, 404);
  assert.equal((await call(base + "/status", r.observer_tokens.web)).status, 401);
  assert.equal((await call(base + "/close", r.reader_token, {})).status, 401);
  assert.equal((await call(base + "/observers/web/challenge", r.reader_token)).status, 401);
  assert.equal((await call(base + "/observers/web/challenge", r.observer_tokens.desktop)).status, 401);
  const o = f.observers[0], token = r.observer_tokens[o.id], observerBase = `${base}/observers/${o.id}`;
  const challenge = await call(observerBase + "/challenge", token);
  assert.equal(challenge.status, 200);
  const sameChallenge = await call(observerBase + "/challenge", token);
  assert.deepEqual(sameChallenge.body, challenge.body, "Polling must not reset the challenge or deadline");
  const answer = await syntheticAnswer(challenge.body, o, f.controller.publicKey);
  const replies = await Promise.all(Array.from({ length: 8 }, () => call(observerBase + "/answer", token, answer)));
  assert.ok(replies.every((v) => v.status === 200), JSON.stringify(replies));
  assert.equal(replies.filter((v) => v.body.duplicate).length, 7);
  const before = await call(base + "/status", r.reader_token);
  assert.equal(before.body.observers[0].seq, 1);
  const firstExport = await call(base + "/export", r.reader_token);
  assert.equal(firstExport.body.receipts.filter((e) => e.statement.kind === "answer_accepted").length, 1);
  const exported = JSON.stringify(firstExport.body);
  for (const secret of [admin, r.reader_token, ...Object.values(r.observer_tokens), f.controller.privateKey]) assert.equal(exported.includes(secret), false);
  assert.equal((await call(base + "/export?after=-1", r.reader_token)).status, 400);
  assert.equal((await call(observerBase + "/answer", token, { huge: "x".repeat(70000) })).status, 400);

  await mf.dispose(); mf = new Miniflare(options);
  const after = await call(base + "/status", r.reader_token);
  assert.equal(after.body.observers[0].head, before.body.observers[0].head, "Receipt and observation heads survive a real runtime restart");


  const until = challenge.body.statement.deadline_ms + 900;
  await sleep(Math.max(0, until - Date.now()));
  const sql = await mf.unsafeGetDurableObjectStorage("tgwitness-controller-test", "WitnessRun", { name: r.run_id });
  const rows = await sql.exec("SELECT document FROM receipts ORDER BY idx");
  const documents = JSON.stringify(rows);
  assert.match(documents, /response_deadline_missed/, "Alarm must persist the incident without client polling");
  await assert.rejects(sql.exec("DELETE FROM receipts"), /forbidden/);
  const interrupted = await call(base + "/status", r.reader_token);
  assert.equal(interrupted.body.continuity_broken, true);
  await call(base + "/close", admin, {});
  const final = await call(base + "/export", r.reader_token);
  const verified = await verifyBundle(final.body, final.body.checkpoint, f.controller.publicKey);
  assert.ok(verified.incidents >= 2);
  assert.equal((await call(observerBase + "/challenge", token)).status, 409);
  await mf.dispose(); mf = new Miniflare(options);
  const closed = await call(base + "/status", r.reader_token);
  assert.equal(closed.body.closed, true); assert.equal(closed.body.continuity_broken, true);


  const second = (await call("/v1/runs", admin, f.body)).body, secondBase = `/v1/runs/${second.run_id}`;
  for (const observer of f.observers) {
    const route = `${secondBase}/observers/${observer.id}`, observerToken = second.observer_tokens[observer.id];
    const c = await call(route + "/challenge", observerToken);
    assert.equal((await call(route + "/answer", observerToken, await syntheticAnswer(c.body, observer, f.controller.publicKey))).status, 200);
  }
  const route = `${secondBase}/observers/${o.id}`, observerToken = second.observer_tokens[o.id];
  let next;
  for (let tries = 0; tries < 16; tries++) {
    next = await call(route + "/challenge", observerToken);
    if (next.status === 200) break;
    assert.equal(next.body.poll_after_ms, 500); assert.equal(next.body.next_check_ms, undefined);
    await sleep(500);
  }
  assert.equal(next.status, 200);
  const c = next.body.statement;
  const intent = { format: "tgwitness-action-intent-v1", run_id: second.run_id, observer_id: o.id,
    request_id: randomToken(), action: "change_proxy", parameters_sha256: "e".repeat(64), round: c.round, nonce: c.nonce };
  const envelope = { statement: intent, signature: await sign(await privateKey(o.keys.privateKey), intent) };
  assert.equal((await call(route + "/intent", second.reader_token, envelope)).status, 401);
  assert.equal((await call(route + "/intent", observerToken, envelope)).status, 202);
  const claim = { format: "tgwitness-action-claim-v1", run_id: second.run_id, observer_id: o.id, request_id: intent.request_id, round: c.round, nonce: c.nonce };
  const claimed = await call(route + "/permit", observerToken, { statement: claim, signature: await sign(await privateKey(o.keys.privateKey), claim) });
  assert.equal(claimed.status, 202);
  const pending = await call(secondBase + "/status", second.reader_token);
  assert.equal(pending.body.pending_action.request_id, intent.request_id);
  assert.equal(pending.body.pending_action.ready_at_ms, undefined);
  await call(secondBase + "/close", admin, {});
  const cancelled = (await call(secondBase + "/export", second.reader_token)).body;
  assert.ok(cancelled.receipts.some((r) => r.statement.kind === "critical_action_cancelled"));
  assert.equal((await verifyBundle(cancelled, cancelled.checkpoint, f.controller.publicKey)).closed, true);
});
