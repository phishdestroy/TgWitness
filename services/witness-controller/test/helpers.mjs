import { generateKeys, privateKey, sign, observation, sha } from "../src/protocol.mjs";
import { register, RunEngine } from "../src/engine.mjs";

export async function identities() {
  const controller = await generateKeys();
  const observers = await Promise.all(["tgwitness", "desktop", "web"].map(async (kind) => ({ id: kind, kind, keys: await generateKeys() })));
  const body = { observers: observers.map((o) => ({ id: o.id, kind: o.kind, public_key: o.keys.publicKey, declared_build_digest: "a".repeat(64) })) };
  return { controller, observers, body };
}
export async function fixture(now = 100000) {
  const ids = await identities();
  const key = await privateKey(ids.controller.privateKey);
  const created = await register("12345678-1234-4234-8234-123456789abc", ids.body, key, ids.controller.publicKey, now);
  return { ...ids, ...created, key };
}
export function resume(f, time) {
  return new RunEngine(f.engine.state, f.key, f.controller.publicKey, time);
}
export async function answerFor(engine, observer, { payload = null, patch = {} } = {}) {
  const o = engine.state.observers.find((v) => v.id === observer.id), c = o.challenge;
  const entries = payload === null ? [] : [await observation(engine.state.run_id, o.id, o.seq + 1, o.head, await sha(payload))];
  const statement = { format: "tgwitness-answer-v1", run_id: engine.state.run_id, observer_id: o.id,
    round: c.round, nonce: c.nonce, declared_build_digest: o.declared_build_digest,
    seq: entries.at(-1)?.seq ?? o.seq, head: entries.at(-1)?.hash ?? o.head,
    entries, capture_active: true, source_status: "connected", ...patch };
  return { statement, signature: await sign(await privateKey(observer.keys.privateKey), statement) };
}
