# Keep it secure

Canonical page: https://phishdestroy.github.io/TgWitness/docs/security/

Know the routes for Telegram, public proxy lists and optional external services. Know what each secret unlocks, what the protections cover and what they leave to you.

**127.0.0.1**panel address by default

**256-bit**random panel token

**0**CDNs, analytics or remote fonts

**Ed25519**signature on every record

## Where everything lives

The collector, its panel and every saved record stay on the computer or server you run it on. Telegram is the only destination by default; each other one is a separate switch.

06 / WHAT LEAVES THE MACHINEYour installation

YOUR COMPUTER OR SERVER

**Panel**127.0.0.1:8787 · bearer token

**Collector**one Telegram client per workspace

DATA DIRECTORY

**Journal**SQLite · hash-chained · signed

**Media**files named by SHA-256

**Vault**Fernet · session, API pair, signing key, proxy

- **Telegram**Always · through your route

  The account's MTProto connection: direct, SOCKS5, HTTP or MTProxy. Hide IP mode waits for a working proxy. Direct fallback requires a mode that explicitly permits it.
- **Off-site copy**Optional · off by default

  Journal, files and checkpoints encrypted with AES-GCM before upload to S3-compatible storage. The key stays with you; attachments are named by keyed hashes, not their content hash.
- **Notifications**Optional · off by default

  Problems and change counts with chat titles. Message excerpts are sent only if you turn them on.
- **Timestamp authority**Optional · off by default

  Only the SHA-256 of a signed checkpoint and a random nonce. No messages, no chat names.
- **Witness**Optional · off by default

  Pulls signed checkpoints and capture counters with a read-only token. It cannot read conversations or change settings.

Default: only the Telegram connection leaves this machine.

Optional destinations are configured per workspace. Message text and media are stored unencrypted in the data directory: protect it with disk encryption and file permissions.

## What each secret unlocks

| Secret | Where it is kept | What it unlocks | If it leaks |
| --- | --- | --- | --- |
| **Panel token** | `panel-token.txt` in the data directory; the browser keeps it for the tab only | Everything in every workspace: read and export, change scope, sign in accounts | Stop TgWitness, delete `panel-token.txt`, start it again: a new token is created |
| **Telegram session** | Vault, encrypted (`credentials.enc`) | The Telegram account itself | End the session in Telegram under *Settings → Devices* |
| **Signing key** | Vault, encrypted (`signing.enc`) | Signing records that verify under your fingerprint | Checkpoints kept elsewhere, a witness and timestamps show what existed before |
| **Vault key** | `vault.key` beside the data, or an external master key for a new data directory | Decrypting the vault | Treat the session and signing key as leaked too |
| **Witness token** | On the witness host | Read-only: signed checkpoints and health | Delete it on the Witness page; create a new one |
| **Off-site copy key** | Vault; download it once for recovery | Decrypting the off-site copy | Whoever also holds the stored objects can decrypt them: treat that copy as exposed |

## What the protections cover

### Covered

- A changed, removed or reordered record in an export: the hash chain or a signature no longer verifies.
- A journal cut back or rebuilt after a checkpoint was kept elsewhere: the retained checkpoint no longer matches.
- Guessing the panel token: 256 random bits, compared in constant time; after 15 failures a minute an address is refused.
- Hostile chat content: text is inserted as text, never as HTML; attachments download as files; the panel loads nothing from other sites.
- A copied data directory with an external vault key: sessions and signing keys stay encrypted without the master key.

### Left to you

- The main panel token has full control. Give other people scoped access to the accounts, chats and actions they need; keep the main key private.
- An administrator of the machine can read everything and rewrite and re-sign the journal. Keep the fingerprint and checkpoints on another system.
- Message text and media are not encrypted by TgWitness. Use disk encryption and strict permissions.
- Plain HTTP beyond localhost shows the token on the network. Use HTTPS or an SSH tunnel.
- Signatures prove what was recorded was not changed, not that every Telegram event was recorded.

[Share access to a case](https://phishdestroy.github.io/TgWitness/docs/access/) with permissions, expiry and session limits. A witness token remains a separate credential.

## Harden an installation

0 of 8 done

1. **Use a dedicated Telegram account** — never your main one. The panel token and the session give full control of it.
2. **Keep the panel on 127.0.0.1.** Reach it remotely only through HTTPS (the bundled Caddy configuration) or an SSH tunnel.
3. **Encrypt the disk** that holds the data directory: message text and media are stored as they arrived.
4. **Restrict the data directory** to the service account. New directories get mode 0700 on Unix; on Windows, set the folder's permissions.
5. **Keep the vault master key elsewhere** on servers: set `TGWITNESS_VAULT_KEY_FILE` before creating the data directory.
6. **Save the signing-key fingerprint and checkpoints** on another system, and add a witness on another host.
7. **Never upload** `data/`, sessions, `panel-token.txt` or vault keys to GitHub or a chat.
8. **Do not log** `Authorization` headers or request bodies at a reverse proxy.

**Can I change the panel token without losing data?**

Yes. The token only opens the panel. Stop TgWitness, delete `panel-token.txt` from the data directory and start it again; the journal, sessions and keys are untouched. With `TGWITNESS_TOKEN` set, the environment value is used instead of the file.

**Why are messages not encrypted at rest?**

The collector must read them to search, compare versions and export. Encrypting them with a key on the same machine would add little against someone who can read that machine. Disk encryption protects a stopped or stolen disk; strict permissions protect a running one.

## Report a vulnerability

Use **Security → Report a vulnerability** in the GitHub repository. Include the version, the impact and a minimal synthetic reproduction. Never send credentials, account directories or real evidence archives. If private reporting is unavailable, open an issue asking for a private channel without exploit details.
