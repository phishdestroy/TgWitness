# See how evidence works

Canonical page: https://phishdestroy.github.io/TgWitness/docs/concepts/

A message can change. The record of what you observed should remain checkable.

Explore two small experiments below. They use fictional messages, stay in your browser and never connect to Telegram.

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

A matching hash chain answers an integrity question. It does not establish complete Telegram delivery, the truth of a message or an independently trusted observation time.

Follow the [whole-account investigation](https://phishdestroy.github.io/TgWitness/docs/cases/) from acquisition to case package.
