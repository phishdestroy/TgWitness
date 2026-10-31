import { DurableObject } from "cloudflare:workers";
import { RunEngine, register } from "./engine.mjs";
import { canonical, privateKey, sha, sign, unb64, verify } from "./protocol.mjs";
import { dashboard } from "./dashboard.mjs";

const MAX_BODY = 65536;
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
export function json(value, status = 200) {
  return new Response(JSON.stringify(value), { status, headers: {
    "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer",
  } });
}
async function body(request) {
  if (!request.headers.get("content-type")?.toLowerCase().startsWith("application/json")) throw new Error("JSON body required");
  const reader = request.body?.getReader();
  if (!reader) throw new Error("Body required");
  let size = 0; const chunks = [];
  let timer;
  const timeout = new Promise((_, reject) => { timer = setTimeout(() => reject(new Error("Body timeout")), 5000); });
  try {
    for (;;) {
      const { value, done } = await Promise.race([reader.read(), timeout]); if (done) break;
      size += value.length;
      if (size > MAX_BODY) throw new Error("Body too large");
      chunks.push(value);
    }
  } catch (error) { reader.cancel().catch(() => {}); throw error; }
  finally { clearTimeout(timer); reader.releaseLock(); }
  const joined = new Uint8Array(size); let offset = 0;
  for (const chunk of chunks) { joined.set(chunk, offset); offset += chunk.length; }
  const parsed = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(joined));
  canonical(parsed); return parsed;
}
async function authorized(request, expectedHash) {
  const header = request.headers.get("Authorization") ?? "";
  if (!expectedHash || !/^Bearer [A-Za-z0-9_-]{32,256}$/.test(header)) return false;
  const actual = await sha(header.slice(7));
  let difference = 0;
  for (let i = 0; i < actual.length; i++) difference |= actual.charCodeAt(i) ^ expectedHash.charCodeAt(i);
  return difference === 0;
}
async function admin(request, env) {
  return typeof env.ADMIN_TOKEN === "string" && /^[A-Za-z0-9_-]{32,256}$/.test(env.ADMIN_TOKEN)
    && authorized(request, await sha(env.ADMIN_TOKEN));
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/" && request.method === "GET") {
      return new Response(dashboard, { headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store",
        "Content-Security-Policy": "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; base-uri 'none'; frame-ancestors 'none'; form-action 'none'",
        "X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer" } });
    }
    if (url.pathname === "/v1/key" && request.method === "GET") {
      try { unb64(env.WITNESS_PUBLIC_KEY, 32); }
      catch { return json({ error: "controller_not_configured" }, 503); }
      return json({ format: "tgwitness-controller-key-v1", public_key: env.WITNESS_PUBLIC_KEY });
    }
    if (url.pathname === "/v1/runs" && request.method === "POST") {
      if (!await admin(request, env)) return json({ error: "unauthorized" }, 401);
      const run = crypto.randomUUID(); url.pathname = `/v1/runs/${run}`;
      return env.RUNS.get(env.RUNS.idFromName(run)).fetch(new Request(url, request));
    }
    const segments = url.pathname.split("/").filter(Boolean);
    if (segments[0] !== "v1" || segments[1] !== "runs" || !UUID.test(segments[2] ?? "")) return json({ error: "not_found" }, 404);
    // Registration is only available through the server-generated run identifier.
    if (segments.length === 3) return json({ error: "not_found" }, 404);
    return env.RUNS.get(env.RUNS.idFromName(segments[2])).fetch(request);
  },
};

export class WitnessRun extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env); this.ctx = ctx; this.env = env;
    const sql = ctx.storage.sql;
    sql.exec("CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY CHECK(id=1), document TEXT NOT NULL)");
    sql.exec("CREATE TABLE IF NOT EXISTS receipts (idx INTEGER PRIMARY KEY, hash TEXT UNIQUE NOT NULL, document TEXT NOT NULL)");
    sql.exec("CREATE TRIGGER IF NOT EXISTS immutable_update BEFORE UPDATE ON receipts BEGIN SELECT RAISE(ABORT, 'receipt update forbidden'); END");
    sql.exec("CREATE TRIGGER IF NOT EXISTS immutable_delete BEFORE DELETE ON receipts BEGIN SELECT RAISE(ABORT, 'receipt deletion forbidden'); END");
  }
  load() {
    const rows = [...this.ctx.storage.sql.exec("SELECT document FROM state WHERE id=1")];
    return rows.length ? JSON.parse(rows[0].document) : null;
  }
  async key() {
    if (!this.signer) this.signer = (async () => {
      unb64(this.env.WITNESS_PUBLIC_KEY, 32);
      const key = await privateKey(this.env.WITNESS_PRIVATE_KEY);
      const test = { format: "tgwitness-key-check-v1", public_key: this.env.WITNESS_PUBLIC_KEY };
      if (!await verify(this.env.WITNESS_PUBLIC_KEY, test, await sign(key, test))) throw new Error("Controller key mismatch");
      return key;
    })();
    return this.signer;
  }
  async commit(engine) {
    const next = engine.nextAlarm();
    // Schedule BEFORE committing so a crash cannot leave a committed active run
    // without a wake-up. A premature wake-up re-evaluates persisted deadlines.
    if (next !== null) await this.ctx.storage.setAlarm(Math.max(Date.now() + 1, next));
    this.ctx.storage.transactionSync(() => {
      for (const receipt of engine.receipts) {
        this.ctx.storage.sql.exec("INSERT INTO receipts (idx, hash, document) VALUES (?, ?, ?)", receipt.statement.index, receipt.hash, JSON.stringify(receipt));
      }
      this.ctx.storage.sql.exec("INSERT INTO state (id, document) VALUES (1, ?) ON CONFLICT(id) DO UPDATE SET document=excluded.document", JSON.stringify(engine.state));
    });
    if (next === null) await this.ctx.storage.deleteAlarm();
  }
  async fetch(request) {
    // Consume bounded bodies outside the state lock: a slow upload must not
    // block alarms or other observers. Authorization is still checked below.
    let payload = null;
    if (request.method === "POST" && request.body) {
      try { payload = await body(request); }
      catch { return json({ error: "invalid_request_body" }, 400); }
    }
    return this.ctx.blockConcurrencyWhile(async () => {
      try { return await this.handle(request, payload); }
      catch (error) {
        if (error instanceof SyntaxError || error instanceof TypeError || /protocol|JSON|Body|observer|Register|base64|Observers/.test(error.message)) return json({ error: "invalid_request" }, 400);
        // Never expose request data, credentials or exception internals.
        return json({ error: "controller_unavailable" }, 503);
      }
    });
  }
  async handle(request, payload) {
    const url = new URL(request.url), parts = url.pathname.split("/").filter(Boolean), run = parts[2];
    let state = this.load();
    if (parts.length === 3 && request.method === "POST") {
      if (!await admin(request, this.env)) return json({ error: "unauthorized" }, 401);
      if (state) return json({ error: "run_already_registered" }, 409);
      const created = await register(run, payload, await this.key(), this.env.WITNESS_PUBLIC_KEY);
      await this.commit(created.engine);
      return json({ run_id: run, reader_token: created.readerToken, observer_tokens: created.observerTokens,
        controller_public_key: this.env.WITNESS_PUBLIC_KEY, registration: created.engine.receipts[0] }, 201);
    }
    if (!state) return json({ error: "not_found" }, 404);
    if (state.controller_public_key !== this.env.WITNESS_PUBLIC_KEY) return json({ error: "controller_key_changed_start_new_run" }, 503);
    const readerRoute = ["status", "checkpoint", "export"].includes(parts[3]) && parts.length === 4 && request.method === "GET";
    const closeRoute = parts[3] === "close" && parts.length === 4 && request.method === "POST";
    const observer = parts[3] === "observers" && parts.length === 6 ? state.observers.find((o) => o.id === parts[4]) : null;
    if (readerRoute) {
      if (!await authorized(request, state.reader_hash)) return json({ error: "unauthorized" }, 401);
    } else if (closeRoute) {
      if (!await admin(request, this.env)) return json({ error: "unauthorized" }, 401);
    } else if (observer && ((parts[5] === "challenge" && request.method === "GET") || (["answer", "intent", "permit"].includes(parts[5]) && request.method === "POST"))) {
      if (!await authorized(request, observer.token_hash)) return json({ error: "unauthorized" }, 401);
    } else return json({ error: "not_found" }, 404);
    // Record receipt time after the entire bounded request body arrives. A slow
    // body must not buy extra time by opening its HTTP request before the deadline.
    const engine = new RunEngine(state, await this.key(), this.env.WITNESS_PUBLIC_KEY);
    await engine.advance();
    let result;
    if (closeRoute) {
      await engine.close("operator_closed"); result = json(engine.status());
    } else if (observer) {
      const current = engine.state.observers.find((o) => o.id === observer.id);
      if (parts[5] === "answer") {
        const answer = await engine.answer(observer.id, payload); result = json(answer.body, answer.status);
      } else if (["intent", "permit"].includes(parts[5])) {
        const answer = await engine.action(observer.id, parts[5], payload); result = json(answer.body, answer.status);
      } else if (engine.state.closed || current.quarantined) result = json({ error: "run_or_observer_closed" }, 409);
      else result = current.challenge
        ? json({ statement: current.challenge, signature: current.challenge_signature })
        : json({ poll_after_ms: 500 }, 202);
    }
    await this.commit(engine);
    if (result) return result;
    if (parts[3] === "status") return json(engine.status());
    if (parts[3] === "checkpoint") return json(JSON.parse([...this.ctx.storage.sql.exec("SELECT document FROM receipts ORDER BY idx DESC LIMIT 1")][0].document));
    const after = Number(url.searchParams.get("after") ?? 0);
    const through = Number(url.searchParams.get("through") ?? engine.state.index);
    if (!Number.isSafeInteger(after) || !Number.isSafeInteger(through) || after < 0 || through < 1 || after > through || through > engine.state.index) return json({ error: "invalid_export_range" }, 400);
    const receipts = [...this.ctx.storage.sql.exec("SELECT document FROM receipts WHERE idx>? AND idx<=? ORDER BY idx LIMIT 500", after, through)].map((row) => JSON.parse(row.document));
    const checkpoint = JSON.parse([...this.ctx.storage.sql.exec("SELECT document FROM receipts WHERE idx=?", through)][0].document);
    const nextAfter = receipts.at(-1)?.statement.index ?? after;
    return json({ format: "tgwitness-controller-export-v1", run_id: run, receipts, checkpoint,
      through, next_after: nextAfter, has_more: nextAfter < through });
  }
  alarm() {
    return this.ctx.blockConcurrencyWhile(async () => {
      const state = this.load();
      if (!state || state.closed) return;
      if (state.controller_public_key !== this.env.WITNESS_PUBLIC_KEY) throw new Error("Controller key changed");
      const engine = new RunEngine(state, await this.key(), this.env.WITNESS_PUBLIC_KEY);
      await engine.advance(); await this.commit(engine);
    });
  }
}
