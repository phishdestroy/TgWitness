# Telegram Evidence: Hash Chains & Signatures

Canonical page: https://phishdestroy.github.io/TgWitness/docs/concepts/

Messages change. Your record of what you saw shouldn't, and anyone should be able to check that.

Two small experiments below. Fake messages, everything runs in your browser, nothing goes to Telegram.

## From a chat export to a verifiable record

A [Telegram Desktop export](https://telegram.org/blog/export-and-more) saves the history you can see right now as HTML or JSON. TgWitness adds a running journal of changes, signatures on every record and checkpoints others can compare against.

| Task | Telegram Desktop export | TgWitness |
| --- | --- | --- |
| Read saved conversations | HTML or JSON with selected media | Saved chats, searchable journal and offline reports |
| Follow a change over time | The history available when exported | Old versions, later edits and deletions, all kept |
| Check files after handover | Standard HTML/JSON export files are unsigned | Signed manifest, signed records and sealed reports, checked against a trusted key |
| Compare with an earlier retained state | Keep a separate reference copy or hash | Signed checkpoints, a separate witness and optional external timestamps |

The comparison is based on the [Telegram Desktop export code](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) as of 2 November 2026.

## One message, three observations

A new message, an edit and a deletion become three separate records. The edit doesn't overwrite the first one, and the deletion doesn't erase it.

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

Telegram doesn't say who deleted a message or exactly when. TgWitness leaves those fields empty instead of guessing.

## Change a record. Follow the hash.

Every record contains the hash of the one before it. A checkpoint kept somewhere else pins the journal length and the last hash.

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

**C** is the nine event fields as UTF-8 JSON: sorted keys, no extra whitespace, no ASCII escaping, no NaN/infinity. `previous_hash` is hi−1, h0 is 64 zeros, signatures cover the 32 raw digest bytes.

The fields: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. Full spec: [event encoding](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#event-canonicalization).

RETAINED CHECKPOINT

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Check the checkpoint signature against the pinned key, then compare it with the journal. A later export can be longer, but it has to match at the checkpoint.

## Three questions, three different checks

[01 / INTEGRITY**Did this record change?** Hashes and signatures against a key you trust.](https://phishdestroy.github.io/TgWitness/docs/exports/)[02 / CONTINUITY**What was retained earlier?** Compare the export with checkpoints a witness kept.](https://phishdestroy.github.io/TgWitness/docs/witness/)[03 / DELIVERY**Did these test events arrive?** Send, edit and delete test messages and see what each account caught.](https://phishdestroy.github.io/TgWitness/docs/cases/)

Signatures answer "was it changed", checkpoints answer "does it match what was there before", test messages answer "did we catch everything". [What verification proves and what it doesn't.](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope)

Next: a [whole-account investigation](https://phishdestroy.github.io/TgWitness/docs/cases/) from start to case package.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
