
import { observation, privateKey, sha, sign, verify } from "../src/protocol.mjs";

export async function syntheticAnswer(envelope, identity, pinnedControllerKey) {
  const c = envelope.statement;
  if (!await verify(pinnedControllerKey, c, envelope.signature) || c.format !== "tgwitness-challenge-v1" || c.observer_id !== identity.id) throw new Error("Untrusted challenge");
  const entry = await observation(c.run_id, identity.id, c.previous_seq + 1, c.previous_hash,
    await sha({ synthetic: true, observer: identity.id, round: c.round }));
  const statement = { format: "tgwitness-answer-v1", run_id: c.run_id, observer_id: identity.id,
    round: c.round, nonce: c.nonce, declared_build_digest: c.declared_build_digest,
    seq: entry.seq, head: entry.hash, entries: [entry], capture_active: true, source_status: "connected" };
  return { statement, signature: await sign(await privateKey(identity.keys.privateKey), statement) };
}

export async function exportAll(request, run, readerToken) {
  const route = `/v1/runs/${run}/export`;
  let page = await request(route, readerToken), receipts = [...page.receipts];
  const through = page.through, checkpoint = page.checkpoint;
  while (page.has_more) {
    page = await request(`${route}?after=${page.next_after}&through=${through}`, readerToken);
    receipts.push(...page.receipts);
  }
  return { bundle: { format: "tgwitness-controller-export-v1", receipts }, checkpoint };
}
