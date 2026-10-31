import { mkdir, readFile, writeFile } from "node:fs/promises";
import { generateKeys, verifyBundle } from "../src/protocol.mjs";
import { exportAll, syntheticAnswer } from "./synthetic.mjs";

const origin = new URL(process.argv[2] ?? "http://127.0.0.1:8787");
if (origin.protocol !== "http:" || !["localhost", "127.0.0.1", "[::1]"].includes(origin.hostname)) throw new Error("Synthetic demo is restricted to local loopback HTTP");
const vars = Object.fromEntries((await readFile(".dev.vars", "utf8")).trim().split(/\r?\n/).map((line) => { const i = line.indexOf("="); return [line.slice(0, i), line.slice(i + 1)]; }));
async function request(path, token, body) {
  const response = await fetch(new URL(path, origin), { method: body === undefined ? "GET" : "POST", redirect: "error", signal: AbortSignal.timeout(5000),
    headers: { Authorization: `Bearer ${token}`, ...(body === undefined ? {} : { "Content-Type": "application/json" }) },
    ...(body === undefined ? {} : { body: JSON.stringify(body) }) });
  const value = await response.json();
  if (!response.ok) throw new Error(value.error ?? `HTTP ${response.status}`);
  return value;
}
const observers = await Promise.all(["tgwitness", "desktop", "web"].map(async (id) => ({ id, kind: id, keys: await generateKeys() })));
const run = await request("/v1/runs", vars.ADMIN_TOKEN, { observers: observers.map((o) => ({ id: o.id, kind: o.kind, public_key: o.keys.publicKey, declared_build_digest: "a".repeat(64) })) });
const base = `/v1/runs/${run.run_id}`;
await mkdir("demo-output", { recursive: true });
await writeFile("demo-output/access.json", JSON.stringify({ run_id: run.run_id, reader_token: run.reader_token }), { mode: 0o600 });
console.log("Synthetic observers only. Local dashboard credentials are in demo-output/access.json (ignored by Git).");
let heldDeadline = null, interruptionSeen = false, recovered = false;
try {
  const stopAt = Date.now() + 45000;
  while (Date.now() < stopAt && !recovered) {
    for (const o of observers) {
      const route = `${base}/observers/${o.id}`, token = run.observer_tokens[o.id];
      const challenge = await request(route + "/challenge", token);
      if (!challenge.statement) continue;
      if (o.id === "web" && challenge.statement.round === 2) {
        if (heldDeadline === null) {
          heldDeadline = challenge.statement.deadline_ms;
          console.log("Withholding the web observer's second answer to simulate a blocked verification channel.");
        }
        continue;
      }
      await request(route + "/answer", token, await syntheticAnswer(challenge, o, vars.WITNESS_PUBLIC_KEY));
    }
    const status = await request(base + "/status", run.reader_token);
    if (status.continuity_broken && !interruptionSeen) { interruptionSeen = true; console.log("Interruption recorded externally by the local controller."); }
    if (interruptionSeen && status.responsiveness === "all_responding") {
      recovered = true; console.log("All observers responding again. Earlier interruption remains recorded.");
    }
    if (!recovered) await new Promise((r) => setTimeout(r, 300));
  }
  if (!recovered || heldDeadline === null) throw new Error("Demo did not complete the interruption/recovery sequence");
} finally { await request(base + "/close", vars.ADMIN_TOKEN, {}); }
const { bundle, checkpoint } = await exportAll(request, run.run_id, run.reader_token);
const report = await verifyBundle(bundle, checkpoint, vars.WITNESS_PUBLIC_KEY);
for (const [name, data] of Object.entries({ "receipts.json": bundle, "checkpoint.json": checkpoint, "report.json": report })) {
  await writeFile(`demo-output/${name}`, JSON.stringify(data, null, 2));
}
console.log(JSON.stringify(report, null, 2));
console.log("Demo files saved in demo-output/. The demo saves its own checkpoint; real verification needs a copy retained independently.");
