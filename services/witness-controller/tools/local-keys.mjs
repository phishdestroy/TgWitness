import { writeFile } from "node:fs/promises";
import { generateKeys, randomToken } from "../src/protocol.mjs";

const key = await generateKeys();
try {
  await writeFile(".dev.vars", `ADMIN_TOKEN=${randomToken()}\nWITNESS_PRIVATE_KEY=${key.privateKey}\nWITNESS_PUBLIC_KEY=${key.publicKey}\n`, { flag: "wx", mode: 0o600 });
  console.log("Created .dev.vars for local development. Keep it private; it is excluded from Git.");
  console.log(`Public verification key: ${key.publicKey}`);
} catch (e) {
  if (e.code === "EEXIST") { console.error(".dev.vars already exists; no keys were replaced."); process.exitCode = 1; }
  else throw e;
}
