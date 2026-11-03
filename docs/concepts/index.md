# See how evidence works

Canonical page: https://phishdestroy.github.io/TgWitness/docs/concepts/

A message can change. The record of what you observed should remain checkable.

Explore two small experiments below. They use fictional messages, stay in your browser and never connect to Telegram.

## From a chat export to a verifiable record

[Telegram Desktop exports](https://telegram.org/blog/export-and-more) save available chat history and media as HTML or JSON for offline use. TgWitness adds an ongoing journal of received changes, signatures on observations and exports, and checkpoints that recipients can compare independently.

| Task | Telegram Desktop export | TgWitness |
| --- | --- | --- |
| Read saved conversations | HTML or JSON with selected media | Saved chats, searchable journal and offline reports |
| Follow a change over time | The history available when exported | Earlier captured versions, later edits and deletion observations retained together |
| Check files after handover | Standard HTML/JSON export files are unsigned | Signed manifest, per-record signatures and sealed HTML/PDF/JSON reports checked against a trusted collector key |
| Compare with an earlier retained state | Keep a separate reference copy or hash | Signed checkpoints, a separate witness and optional external timestamps |

The file-signing comparison is based on the [Telegram Desktop export writers](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) reviewed on 2 November 2026. TgWitness signs with the collector’s key; the checks below show how a recipient uses it.

## One message, three observations

When Telegram delivers a new message, an edit and a deletion notice, the collector appends three separate observations. The edit does not replace the first record. A deletion notice does not erase it.

01 / MESSAGE JOURNEYIllustrative sequence

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Collector · Journal · update → · append →

CURRENT CHAT VIEW Message #42

Message deleted

The message has disappeared from the chat view.

OBSERVATION JOURNAL 3 records

1. 01

   `message.new`

   Meet at 10:00

   ✓
2. 02

   `message.edited`

   Meet at 11:00

   ✓
3. 03

   `message.deleted`

   Deletion notice for #42

   ✓

All three received observations remain in the journal.

Simplified path for one already selected source. Operational records also share the real journal. Capture depends on what the account can see and what Telegram delivers.

A deletion notice supplies neither a reliable deletion time nor the person who deleted the message. Keeping those values unknown preserves the distinction between an observation and a guess.

## Change a record. Follow the hash.

Each record contains the previous record’s hash. Its own hash covers the event fields, including that link. An externally retained checkpoint pins a specific journal length and head hash.

02 / HASH-CHAIN SANDBOXReal SHA-256 · sample records

RECORD 01**Message received**`h₁ = SHA-256(e₁)`Links to 64 zeroes

RECORD 02**Meet at 11:00**`h₂ = SHA-256(e₂)`Includes h₁

RECORD 03**Deletion observed**`h₃ = SHA-256(e₃)`Includes h₂

RETAINED ELSEWHERE**3 records · head `h₃`**Compare this fixed boundary with the supplied journal.

Altering an event changes its hash. Rebuilding the chain changes its head. Removing the tail makes it shorter than the retained checkpoint.

**Inspect record 2 and the full hashes**

This is the exact UTF-8 JSON hashed in this example. Values are fictional; the nine fields and serialization match the journal format.

```

```

Saved record 2 hash

``

Recalculated record 2 hash

``

This sandbox computes hashes, not signatures. The real verifier also checks every event’s Ed25519 signature, sequence and link. Rebuilding hashes alone cannot create valid signatures under the trusted key.

## The actual rules, in a few lines

HASH + SIGNATURE

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** serializes the nine event fields as UTF-8 JSON: sorted keys, no extra whitespace, no ASCII escaping and no NaN/infinity. The event’s `previous_hash` is hi−1. The displayed h0 means 64 zero characters; signatures cover the 32 raw digest bytes.

The nine fields are `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` and `previous_hash`. This is TgWitness’s [documented JSON encoding](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#event-canonicalization); the hash and signature themselves are not hash-input fields.

RETAINED CHECKPOINT

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Verify the checkpoint signature under the pinned collector key, then compare its boundary with the verified journal. A later export may contain more records; it must still agree at the earlier checkpoint.

## Three questions, three different checks

[01 / INTEGRITY**Did this record change?** Verify hashes and signatures against a separately trusted key.](https://phishdestroy.github.io/TgWitness/docs/exports/)[02 / CONTINUITY**What was retained earlier?** Compare a signed export with checkpoints kept by a separate witness.](https://phishdestroy.github.io/TgWitness/docs/witness/)[03 / DELIVERY**Did these test events arrive?** Match controlled send, edit and delete actions against each account’s journal.](https://phishdestroy.github.io/TgWitness/docs/cases/)

Use signatures to check the retained records, checkpoints to compare an earlier boundary, and controlled delivery tests to measure collection. Each answers a specific question. [Read the verification scope and trust assumptions.](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope)

Follow the [whole-account investigation](https://phishdestroy.github.io/TgWitness/docs/cases/) from acquisition to case package.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
