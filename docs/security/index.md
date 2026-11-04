# Keep it secure

Canonical page: https://phishdestroy.github.io/TgWitness/docs/security/

What leaves your machine, what each secret opens, and what the protections cover versus what's on you.

**127.0.0.1**panel address by default

**256-bit**random panel token

**0**CDNs, analytics or remote fonts

**Ed25519**signature on every record

## Where everything lives

The collector, the panel and every record stay on your machine. By default only Telegram is contacted; everything else is a separate switch.

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
| **Panel token** | `panel-token.txt` in the data directory; the browser keeps it per tab | Everything in every workspace | Stop TgWitness, delete `panel-token.txt`, start again: you get a new one |
| **Telegram session** | Vault, encrypted (`credentials.enc`) | The Telegram account itself | End the session in Telegram under *Settings → Devices* |
| **Signing key** | Vault, encrypted (`signing.enc`) | Signing records under your fingerprint | Checkpoints kept elsewhere, a witness and timestamps still show what existed before |
| **Vault key** | `vault.key` next to the data, or an external master key | The vault | Assume the session and signing key leaked too |
| **Witness token** | On the witness host | Read-only: checkpoints and health | Delete it on the Witness page, make a new one |
| **Off-site copy key** | Vault; download it once for recovery | The off-site copy | Anyone who also has the bucket can decrypt it: treat the copy as exposed |

## What the protections cover

### Covered

- A changed, removed or reordered record: the hash chain or a signature breaks.
- A journal cut back or rebuilt after you saved a checkpoint elsewhere: the checkpoint stops matching.
- Guessing the token: 256 random bits, constant-time compare, 15 failures a minute and the address is blocked.
- Hostile chat content: text stays text, never HTML; attachments download as files; the panel loads nothing from other sites.
- A stolen data directory with an external vault key: sessions and keys stay encrypted.

### Left to you

- The main token can do everything. Give others scoped access and keep the main one to yourself.
- Whoever is admin on the machine can read everything and re-sign the journal. Keep the fingerprint and checkpoints elsewhere.
- Messages and media aren't encrypted by TgWitness. Encrypt the disk, lock down permissions.
- Plain HTTP outside localhost leaks the token. Use HTTPS or an SSH tunnel.
- Signatures don't tell you what was missed. Check coverage and test delivery on your own accounts and sources.

[Share access to a case](https://phishdestroy.github.io/TgWitness/docs/access/) with permissions, expiry and session limits.

## Harden an installation

0 of 8 done

1. **Use a dedicated Telegram account**, never your main one.
2. **Keep the panel on 127.0.0.1.** Remote access only via HTTPS (bundled Caddy) or an SSH tunnel.
3. **Encrypt the disk** with the data directory, messages and media are stored as is.
4. **Restrict the data directory** to the service account (0700 on Unix, folder permissions on Windows).
5. **Keep the vault key elsewhere** on servers: set `TGWITNESS_VAULT_KEY_FILE` before the first start.
6. **Save the fingerprint and checkpoints** on another system, run a witness on another host.
7. **Never upload** `data/`, sessions, `panel-token.txt` or vault keys to GitHub or a chat.
8. **Do not log** `Authorization` headers or request bodies at a reverse proxy.

**Can I change the panel token without losing data?**

Yes, it only opens the panel. Stop TgWitness, delete `panel-token.txt`, start again. Journal, sessions and keys stay. If `TGWITNESS_TOKEN` is set, that value wins over the file.

**Why are messages not encrypted at rest?**

The collector has to read them to search, compare and export. A key on the same machine wouldn't stop someone who can read that machine anyway. Disk encryption covers a stolen disk, permissions cover a running one.

## Report a vulnerability

**Security → Report a vulnerability** on GitHub. Version, impact and a minimal repro with fake data. Never send credentials, account folders or real evidence. If private reporting is off, open an issue asking for a private channel, no exploit details.
