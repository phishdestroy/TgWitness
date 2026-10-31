# One journal. Four collection modes. Eight verification levels.

Canonical page: https://phishdestroy.github.io/TgWitness/guides/modes.html

Modes, scenarios and evidence levels

TgWitness records what the connected account observes. A third party can verify the record’s integrity against an independently trusted key.

[Collection modes](https://phishdestroy.github.io/TgWitness/guides/modes.html#scope)[Scenarios](https://phishdestroy.github.io/TgWitness/guides/modes.html#scenarios)[Evidence levels](https://phishdestroy.github.io/TgWitness/guides/modes.html#levels)

3–5 minute overview · fictional examples · current implementation

1. **Telegram**

   Account-visible updates
2. **Collector**

   Linked records, each signed
3. **Verifier**

   Trusted key + retained boundary

`h₁ → h₂ → h₃ · Ed25519`Integrity is checked. Telegram origin and the truth of a message remain separate questions.

## Choose the observation scope

Three scopes and an investigation preset. Exclusions and enabled source types still apply.

Default**Chosen chats**

Records

Only sources selected by hand.

New chats

Not added automatically.

Choose for

A known set of channels or groups. No fixed chat capacity has been qualified.

**Does not do** It does not discover other chats or backfill earlier history.

Account folder**Telegram folder**

Records

Folder inclusions and categories, minus exclusions and archived chats when configured.

New chats

Matching active chats; folder changes within an hour.

Choose for

An analyst already maintains a case folder. Confirm collection on a dedicated account.

**Does not do** It does not apply the folder’s changing muted/read conditions.

Confirm scope**Whole account**

Records

Account-visible chats, including private conversations and bots, within selected types.

New chats

Added when the first update arrives.

Choose for

A dedicated observation account, including an account participating in a case.

**Does not do** It does not join chats automatically or bypass source access.

Whole-account preset**Investigation mode**

Records

All source types, own actions, source profiles and the latest 200 visible messages of newly discovered sources.

New chats

A new chat or bot gets a profile and a history snapshot.

Choose for

Join a team or interact with a bot through the panel. Review and save the preset.

**Does not do** It does not snapshot every existing chat or observe callbacks pressed in another client.

These cards are a local comparison, not live collector controls. They do not change an account.

**Does not do** No mode reads secret chats, records while the process is stopped, joins sources on its own or retrieves earlier history beyond a requested snapshot/export.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/collection/)

## GitHub Actions capture (preview)

A fresh Telegram login, one chat, an encrypted archive and GitHub provenance.

[Open capture helper](https://phishdestroy.github.io/TgWitness/docs/capture/)

## What is recorded

Only delivered or explicitly requested observations enter the record. Unknown attribution stays unknown.

 Capture switches · local illustrationNew messagesEditsDeletionsReactionsMembership

The panel applies these switches per workspace. Turning one off keeps existing records; turning it back on does not reconstruct missed events.

**Event matrix: saved material and remaining unknowns**

| Category | Saved | Remains unknown |
| --- | --- | --- |
| Message | Text, IDs, sender metadata, reply context and original update envelope. | No third-party-verifiable Telegram signature. |
| Edit | Every observed version, without overwriting earlier ones. | Intermediate edits may be missed; sender is not necessarily editor. |
| Deletion | Notice plus previously saved text, if available. | The deleter and exact action time are not supplied. |
| Unscoped deletion | Account-level notice; unknown peer remains explicit. | No guessed chat. Correlation uses previously saved account-scoped IDs when possible. |
| Reaction | Delivered counters and visible recent identities. | Not every reactor is visible; a full available list needs separate queries. |
| Membership | Delivered service messages and participant updates. | Role and chat type limit visibility; silence does not establish absence. |
| Attachment | Original-version descriptor, saved bytes, SHA-256 and attempt outcomes. | A vanished file may be unavailable; a newer version does not replace it. |
| History snapshot | Currently visible messages, marked as history observations. | Earlier edits and vanished content are not reconstructed. |
| Own actions | Outgoing messages/edits and matching reply-keyboard button_press metadata. | Callbacks pressed in another Telegram client are not visible. |
| Bot buttons | Callback, URL, web-app and request metadata retained with the message. | URLs and phone/location requests are text, not automatically opened or executed. |

### Default attachment limits

Photos

20 MiB

Video

100 MiB

Files

50 MiB

Animations

20 MiB

Video notes

50 MiB

Voice

20 MiB

Audio

50 MiB

Stickers

5 MiB

**Does not do** A switch does not redact embedded metadata or disable operational records. Capture does not identify an actor whom Telegram did not supply.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/collection/)

## Use the authorization you have

Each account has its own workspace, journal, signing key, route and queue.

### Phone + code

Enter 2FA when enabled.

### QR code

Scan from an authorized device; 2FA may still be required.

### Telethon .session

Import the account’s session file.

### Pyrogram .session

Import the supported Pyrogram session format.

### TData ZIP

One supported Desktop account; local passcode if set.

### StringSession text

Paste a Telethon StringSession.

### .session + .json

Select the session and matching companion metadata.

### Auth key HEX + DC ID

Import account authorization with its data-center identifier.

**API pair**

Your own API pair is optional. Without one, TgWitness uses a pool of public pairs, including pairs from official Telegram Desktop.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy is experimental; built-in public MTProxy lists are available. A failed proxy route does not fall back to a direct connection.

Two workspaces on one machine are not two independent witnesses.

**Does not do** Import does not bypass Telegram authorization, 2FA or unsupported session formats. Accounts still share the application process.

[Account formats](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/)

## Act from the panel

Send or reply, press a current bot button, save a link preview, then explicitly join a chat or start a bot with its start parameter.

`interaction.preview``interaction.requested``interaction.result`

Preview, request and result receipts are signed. Before a button press, the server fetches the message again and rejects a changed keyboard. Returned callback text and URLs remain recorded context.

**Does not do** No web apps, payments, phone/location sharing or inline queries. Displaying a URL does not open it.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/collection/)

## Recovery and continuity

Gaps are shown, not hidden.

### Resume the saved position

After restart, Telegram is asked for missed updates. Finite retention and expired differences can leave gaps.

### Recheck visible messages

Defaults: priority sources every 15 minutes, others every 6 hours. Outcomes include message.recovered and message.missing_on_recheck.

### Read coverage.json

Observation periods, gaps with reasons and unobserved IDs accompany the signed export. A missing-on-recheck record is not a deletion notice.

**Does not do** A later history snapshot does not erase an outage or recover every vanished version. The saved cursor is not a lossless acknowledgement of journal acceptance.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/)

## Seven levels. Different questions.

Each mechanism answers a bounded question. Configure external services separately and retain their trust anchors outside the collector.

1. ### Record

   SHA-256 chain + Ed25519 per event; the first previous_hash is 64 zeroes.

   **Third party checks** Ordering and signatures under the pinned collector key.

   **Does not do** It does not prove Telegram origin or completeness.

   **Verification command**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Container

   manifest.json lists file hashes; manifest.sig signs it. media.saved binds attachment bytes to an event.

   **Third party checks** The supplied files agree with the signed manifest and media receipts.

   **Does not do** It does not sign a separately downloaded CSV, HTML or screenshot.

   **Verification command**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Retained boundary

   Checkpoint at startup, every 5 minutes by default, and orderly stop. Keep a copy elsewhere.

   **Third party checks** The later export agrees with an earlier retained length and head; rollback can be detected.

   **Does not do** It does not detect replacement of both journal and all retained checkpoints.

   **Verification command**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### External time

   Evidence mode sends a checkpoint SHA-256 to RFC 3161 authorities (FreeTSA, DigiCert) and OpenTimestamps calendars.

   **Third party checks** A verified TSA response dates those bytes; a confirmed OpenTimestamps proof anchors them to Bitcoin.

   **Does not do** It does not treat a prepared request or pending calendar receipt as a confirmed timestamp.

   **Verification command**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Independent witness

   Separate host, scoped read-only endpoint, fresh challenge, its own key/journal and TGW1 channel posts.

   **Third party checks** Earlier accepted heads; statuses ok, key_changed, rollback, fork, invalid and no_response.

   **Does not do** It does not turn two workspaces on one collector host into independent witnesses.

   **Verification command**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Off-site replica

   S3-compatible copy encrypted with AES-256-GCM; Object Lock when the bucket supports it.

   **Third party checks** Restore publishes files only after journal, checkpoint and preserved-media verification succeeds.

   **Does not do** It does not restore without the exported key or assume retention without checking the storage response.

   **Verification command**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Run provenance

   Signed run receipt: source hashes, dependency versions and process context. Self-reported.

   **Third party checks** What the signing collector reported about its own execution.

   **Does not do** It does not provide independent process attestation or exclude compromise before recording.

   **Verification command**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### What no level proves

Delivery of every Telegram update; the truth of the text; that a sender ID identifies a real person; absence of collector compromise before recording; admissibility in court.

[Independent witness](https://phishdestroy.github.io/TgWitness/docs/reference/witness/)

Local SHA-256 experiment

### Try changing record 2

The next record keeps the previously saved link. Changing the text changes record 2’s calculated hash.

Text of record 2

Record 1`h1`Starts with 64 zeroes

Record 2`h2`Includes the saved h1

Record 3`h3`Includes the saved h2

Static example: h2 covers “Meet at 11:00”. Changing that text changes h2; record 3 still references the saved h2.

**Inspect the full digests**

Saved record 2 hash

`SHA-256(e₂)`

Recalculated record 2 hash

`SHA-256(e₂)`

This sample calculates hashes, not signatures. The real verifier checks every signature and link against the trusted key.

 [Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/how-it-works/)

## Choose a route through the evidence

Fictional situations. Start collection before the relevant event; preserve the boundaries and gaps alongside the content.

### A channel changes payment details

Mode → events

Chosen chats → messages, edits, deletions.

Output

Observed post versions and attachments by hash.

Verification

Signed ZIP + retained checkpoint + verified TSA response.

**Does not do** It does not recover an original that was never captured.

### Messages disappear after an incident

Mode → events

Folder or whole account → all event categories.

Output

Saved originals, deletion notices and coverage with gaps.

Verification

Signed ZIP + independent witness journal.

**Does not do** It does not identify the deleter from a notice that supplies no actor.

### Investigate a shop bot

Mode → events

Investigation preset → buttons, link previews and explicit bot start.

Output

Signed interaction receipts, returned callbacks and saved profiles.

Verification

Signed ZIP; verify any dossier against the ZIP.

**Does not do** It does not open a bot web app, make a payment or record another client’s callbacks.

### A participant changes names across chats

Mode → events

Any scope → observed sender/profile metadata.

Output

Name/username history by numeric ID, “also in” links and extracted leads.

Verification

Dossier JSON checked against the signed ZIP.

**Does not do** It does not turn a wallet, phone-like string or username into proven identity.

### Long-running observation with an off-site copy

Mode → events

Any scope → Evidence mode and an S3 replica with supported Object Lock.

Output

Encrypted copy, retained checkpoints and timestamp responses.

Verification

Restore with the exported key, then verify without the original server.

**Does not do** It does not replace an independent witness or a separately retained decryption key.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/investigation/)

## Hand over a checkable package

Supply the signed original, an independently retained key fingerprint, the relevant checkpoint and the verification result.

- Signed ZIP
- JSONL
- CSV
- HTML
- Checkpoint
- Run receipt
- Chat export: chat.json / chat.html
- Dossier JSON
- Password-protected AES-256 ZIP
- Separate exports for multiple accounts
- Streaming CLI: 5 GiB default limit

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Obtain the verifier from a trusted copy, not from the archive being checked.

**Does not do** Standalone CSV and HTML are not signed containers. A password protects transfer confidentiality, not authenticity. Multiple exports do not merge account journals.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/)

## Compare the delivered artifact

Basic artifacts without added signing, timestamp or witness systems. Scripts and loggers vary by implementation; “partial” means limited to captured or visible material.

| Approach | Edits / deletions | Record signature | External time | Independent witness | Coverage / gaps | Verification without author |
| --- | --- | --- | --- | --- | --- | --- |
| Telegram Desktop export | Partial | No | No | No | No | No |
| Telethon snapshot script | Partial | No | No | No | No | No |
| Deletion logger: text log | Partial | No | No | No | No | No |
| Screenshots / web capture | Partial | No | No | No | No | No |
| TgWitness with configured extras | Partial | Yes | Yes | Yes | Partial | Yes |

**Does not do** The table does not assess every script or logging product. Optional time and witness checks require their own services and trust anchors; none establishes source truth.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/)

## Keep the limits with the evidence

Verification is useful when its scope stays explicit.

- Secret chats are unavailable.
- Nothing is recorded while the process is stopped; recovery is bounded.
- A verified record is not proof that its content is true.
- An operator with the key can sign arbitrary content. Independent witnesses and timestamps constrain later replacement, not dishonest initial capture.
- Use a dedicated account, not your primary account.
- Telegram can restrict accounts for request volume.

**Does not do** No mode or evidence level establishes legal admissibility, complete Telegram delivery or real-world identity.

[Setup guide](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=en)[Dedicated account](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/docs/reference/investigation/)
