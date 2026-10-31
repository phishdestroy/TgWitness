import { readFile } from "node:fs/promises";
import { verifyBundle } from "../src/protocol.mjs";

try {
  const [file, checkpointFlag, checkpointFile, keyFlag, key, ...extra] = process.argv.slice(2);
  if (!file || checkpointFlag !== "--checkpoint" || !checkpointFile || keyFlag !== "--public-key" || !key || extra.length) {
    throw new Error("Usage: node tools/verify.mjs receipts.json --checkpoint independently-retained.json --public-key PINNED_BASE64URL_KEY");
  }
  const report = await verifyBundle(JSON.parse(await readFile(file, "utf8")), JSON.parse(await readFile(checkpointFile, "utf8")), key);
  console.log(JSON.stringify(report, null, 2));
  // 0 = verified receipt history, with all observers represented and no recorded
  // interruptions through the checkpoint. It does NOT verify Telegram content.
  process.exitCode = report.continuity_broken || report.observers_responded !== 3 ? 2 : 0;
} catch (e) { console.error(`Verification failed: ${e.message}`); process.exitCode = 1; }
