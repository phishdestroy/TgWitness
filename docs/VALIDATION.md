[TgWitness](../README.md) / [Documentation](README.md) · [Evidence and verification](EVIDENCE.md)

![Evidence & verification](assets/presentation/chapter-evidence.svg)

# Tool validation package

This page is for an examiner who has to decide whether to rely on TgWitness. It
states what the program documents about itself, turns each statement into a
numbered requirement, names the test that checks it and the result that test must
give, and records what a run of those tests actually returned.

The structure follows the NIST Computer Forensics Tool Testing (CFTT) method
(requirements → test assertions → test cases → results) and the documentation items
of SWGDE 18-Q-001. It is **testing by the developer**. It is not an independent
assessment, a certification, or an entry in any register of forensic methods, and
none of those has been obtained. [Verification record](VERIFICATION.md) holds the
live Telegram runs; this page covers the repeatable synthetic tests.

<details>
<summary>On this page</summary>

- [Status of this record](#status-of-this-record)
- [Method and references](#method-and-references)
- [Functions under test](#functions-under-test)
- [Requirements and test assertions](#requirements-and-test-assertions)
- [Traceability](#traceability)
- [Known-answer dataset](#known-answer-dataset)
- [Results of the recorded run](#results-of-the-recorded-run)
- [Deviations](#deviations)
- [Gaps: assertions without a test](#gaps-assertions-without-a-test)
- [Known limitations and what the tests leave open](#known-limitations-and-what-the-tests-leave-open)
- [How to reproduce](#how-to-reproduce)
- [Validation bundle](#validation-bundle)

</details>

## Status of this record

| Item | Value |
| --- | --- |
| Prepared | 14 November 2026 |
| Product revision tested | `main` at `c06a2ba5a`, version 0.9.3, `source_tree_sha256` `e0b7296683c6f600d83069528b8cc47a6dac5a40f97b452e8e01933db2601520` |
| Standalone verifier tested | `tgwitness/verify.py`, SHA-256 `7f9c2e2bbdda6f4034e2b31ae1dcf68bf33b4bc4af6ce7e6a19e3540f0837a7c` |
| Who ran the tests | The maintainer's test host (Ubuntu 24.04.5, Python 3.12.3); not an independent laboratory |
| Test sources | Private suite of the maintainer; files, hashes and results are in the [validation bundle](#validation-bundle), not yet published |
| Independent reproduction | None recorded |

Each result applies to the revision, test files and environment above. A later
revision needs a new run; for in-house tools SWGDE 18-Q-001 §5.6 gives the testing
frequency as "At first use and all tool revisions".

## Method and references

Every source below was opened on 13 November 2026. Section numbers are those of the
version named.

| Source | Version | What this package takes from it |
| --- | --- | --- |
| [NIST CFTT, Methodology Overview](https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt/cftt-general-0) | Page updated 1 May 2026 | A tool category specification consists of requirements, assertions and test cases; testing ends in a test report |
| [NIST CFTT, Cloud & Remotely Stored Data Extraction (CDX) Using Account Credentials: Specification, Test Assertions, and Test Cases](https://www.nist.gov/system/files/documents/2025/01/17/Cloud%20Data%20Extraction%20Specification%20Test%20Assertions%20and%20Test%20Cases%20v1.1.pdf) | Version 1.1, January 2025 | §6 core (all tools) and optional (only when supported) requirements; §7.1–7.3 assertions and conformance indicators; §1: "Each test assertion is covered by one or more test cases consisting of a test protocol and the expected test results"; §8.5 lists a Telegram test case (CDX-05-SM-TG) without an artifact table in Appendix A |
| [SWGDE 18-Q-001, Minimum Requirements for Testing Tools Used in Digital and Multimedia Forensics](https://www.swgde.org/documents/published-complete-listing/18-q-001-minimum-requirements-for-testing-tools-used-in-digital-and-multimedia-forensics/) | Version 2.1, 7 March 2024 | §4 testing "is not necessarily pass/fail"; §5.1.2.3 network extraction tools tested with a known dataset at major releases; §5.1.2.4 cloud imagers: known dataset when practical plus empirical observation at time of use; §5.1.3 hashing tools; §5.3.3 aggregation and summary tools; §5.6 in-house tools tested by another competent person, independent of the developer for critical tools; §6 documentation of results; Appendix A types of testing |
| [ENFSI-BPM-FIT-01, Best Practice Manual for the Forensic Examination of Digital Technology](https://enfsi.eu/wp-content/uploads/2016/09/1._forensic_examination_of_digital_technology_0.pdf) | Version 01, November 2015 | §6.1 validation applies to a process, not a tool; §6.3 statement of requirements; §6.4 risk questions, including testing of new and updated versions; §6.5–6.6 verification "in-situ" by each laboratory; §4.3 documented test sets designed to stress the process |
| [Council of Europe, Electronic Evidence Guide](https://rm.coe.int/0900001680a22757) | Version 2.1, 6 March 2020 | §1.7.1 data integrity; §1.7.2 audit trail that an independent third party can repeat; §6.3.1 hash values; §6.3.2 audit trail of the analysis; §3.5.2 use only tools whose function can be explained in court |

SWGDE §6 lists what a test record contains. This page and the bundle give each item:

| SWGDE §6 item | Where |
| --- | --- |
| Purpose and scope of testing | [Functions under test](#functions-under-test) |
| Who performed the testing | [Status](#status-of-this-record) |
| Date | [Status](#status-of-this-record), `run.json` in the bundle |
| Testing procedure used or scenarios | [Traceability](#traceability), [How to reproduce](#how-to-reproduce) |
| Datasets or other testing material used, including expected results | [Known-answer dataset](#known-answer-dataset) |
| Results and a description of anomalies and their significance | [Results](#results-of-the-recorded-run), [Deviations](#deviations) |
| Identified limitations | [Gaps](#gaps-assertions-without-a-test), [Known limitations](#known-limitations-and-what-the-tests-leave-open) |

SWGDE §5.6 recommends that a tester independent of the developer test critical
in-house tools. This record does not meet that recommendation. ENFSI §6.6 places
verification of a method on each laboratory in its own environment; the bundle is
meant to make that repeat possible, not to replace it.

## Functions under test

| Function | In scope | Out of scope here |
| --- | --- | --- |
| Acquisition from the Telegram API | The collector's handling of new, edited and deleted messages, rechecks, coverage records, catch-up after restart and attachment records, fed with synthetic Telegram objects | Telegram servers, MTProto transport, real clients, Takeout, Secret Chats, optional capture add-ons |
| Preservation in the signed journal | Canonical encoding, hash chain, Ed25519 signatures, append-only storage, transaction failures, checkpoints | Off-site copies, vault key handling |
| Timestamps | Evidence-mode receipts inside the archive, RFC 3161 reply checks, retry handling, chronology of observation times, drand rounds, the `--require evidence` rule | Live authorities, Ukrainian or other national time-stamp services, Bitcoin confirmation of OpenTimestamps |
| Exports | Evidence ZIP manifest and signature, sealed reports, password containers, handover extracts, chat exports | Visual layout, translations, people profiles, indicators, STIX/MISP |
| Verification | `verify.py` decisions and exit codes for intact and altered archives, signer pinning, checkpoints, compatibility with earlier archives and verifiers | GitHub sealed acquisition, Intel TDX, cloud deployment checks |

In SWGDE §5 terms, acquisition behaves like a network connection and extraction
application (§5.1.2.3) or cloud imager (§5.1.2.4), the journal and verifier like a
hashing tool (§5.1.3), and reports like aggregation and summary (§5.3.3). The tests
here are known-dataset tests (Appendix A). The empirical observation at time of use
that §5.1.2.4 asks for is not part of this package.

## Requirements and test assertions

Requirements are taken from what the product documents, with the section named. They
are all core in the CFTT sense: the documented behaviour applies to every workspace.
An assertion is a checkable statement; `A1`, `A2`… number them within a requirement.

### Acquisition (ACQ)

**TW-ACQ-01 New message.** An observed new message is appended as `message.new`
with chat ID, message ID, sender as `actor_id`, Telegram's date as `source_at` and
the collector's UTC time as `observed_at`.
Source: [EVIDENCE.md, Event canonicalization](EVIDENCE.md#event-canonicalization) and
[Actor semantics](EVIDENCE.md#actor-semantics).
- A1 The record carries the known-answer chat, message, sender, date and text.
- A2 `observed_at` is an ISO time with a UTC offset.

**TW-ACQ-02 Edit.** An observed edit becomes a new `message.edited` record with the
edit date as `source_at`; the earlier record stays unchanged.
Source: [HOW-IT-WORKS.md, A message changes](HOW-IT-WORKS.md#a-message-changes-observations-accumulate),
[EVIDENCE.md, Event canonicalization](EVIDENCE.md#event-canonicalization).
- A1 The edit record carries the new text, the edit date and a null actor.
- A2 The original `message.new` record remains in the journal with its text.

**TW-ACQ-03 Repeated delivery.** "There is no duplicate-delivery suppression:
repeated observations are distinct receipts."
Source: [EVIDENCE.md, Event canonicalization](EVIDENCE.md#event-canonicalization).
- A1 The same new-message update delivered twice gives two records.
- A2 The same edit delivered twice gives two records. *See [DV-01](#deviations).*

**TW-ACQ-04 Deletion notices.** A deletion notice is `message.deleted` with null actor
and null source date. In private chats and ordinary groups it is placed in the chat of
the previously saved message with that ID and names the method; IDs never saved stay
`deletion.unscoped`; several IDs in one chat are grouped as `deletion.batch`.
Source: [EVIDENCE.md, Actor semantics](EVIDENCE.md#actor-semantics).
- A1 Known-answer deletions produce exactly the expected records.
- A2 An unscoped notice does not claim that a known chat never held the message.
- A3 Batch wording states what the notice does not identify.

**TW-ACQ-05 Absence on recheck.** An unsuccessful recheck is
`message.missing_on_recheck`, not a deletion; a later recovery clears the current
state and keeps the earlier absence.
Source: [EVIDENCE.md, Actor semantics](EVIDENCE.md#actor-semantics) and
[Durable collection](EVIDENCE.md#durable-collection-and-process-receipts-02).
- A1 Reports count recheck absence and deletion notices separately.
- A2 Reappearance does not turn a past absence into a deletion.

**TW-ACQ-06 Coverage.** Observation periods, gaps and message numbers not observed
are recomputed by `verify.py` from `events.jsonl`; numbers are listed per channel or
supergroup and named "not observed", never "deleted".
Source: [EVIDENCE.md, Coverage](EVIDENCE.md#coverage-continuity-gaps-and-unobserved-ids).
- A1 For known-answer group messages 1, 2 and 5 the verifier lists 3–4 as not observed.
- A2 Capture failures, stops and disconnects end a continuous period.
- A3 Telegram difference-too-long answers are recorded as coverage gaps.
- A4 Gap measurements are carried by export, report and verifier.

**TW-ACQ-07 Catch-up after restart.** The saved update position is resumed and
updates whose handling did not finish are requested again.
Source: [EVIDENCE.md, Durable collection](EVIDENCE.md#durable-collection-and-process-receipts-02).
- A1 A paused or disconnected client is rewound to the saved position; unrecoverable
  drops are reported.

**TW-ACQ-08 Attachments.** A preserved file is bound by SHA-256 and size to its
message in a signed record; disabled or failed downloads are visible outcomes; the
verifier checks bytes against the journal.
Source: [EVIDENCE.md, Attachments](EVIDENCE.md#attachments).
- A1 Every media policy keeps the message records and the export verifies.
- A2 The verifier rejects payload-length contradictions.
- A3 Staged files cannot replace the original message's file.

### Preservation (PRS)

**TW-PRS-01 Encoding, chain and signatures.** The hash is SHA-256 over the canonical
JSON of exactly nine fields; the first `previous_hash` is 64 zeros; sequence numbers
start at 1; each record carries an Ed25519 signature over the 32 raw hash bytes.
Source: [EVIDENCE.md, Event canonicalization](EVIDENCE.md#event-canonicalization),
[HOW-IT-WORKS.md, What a hash covers](HOW-IT-WORKS.md#what-a-hash-covers).
- A1 An independent implementation of the published formula reproduces every hash and
  accepts every signature.

**TW-PRS-02 Append-only journal.** "SQLite triggers enforce append-only behavior for
normal application writes."
Source: [SECURITY-MODEL.md, Integrity and external time](SECURITY-MODEL.md#integrity-and-external-time).
- A1 `UPDATE` and `DELETE` on the journal table are refused.

**TW-PRS-03 Check before export.** "The collector verifies journal signatures before
generating every export format."
Source: [EVIDENCE.md, What is signed](EVIDENCE.md#what-is-signed).
- A1 A stored record changed outside the application stops the ZIP export.

**TW-PRS-04 Complete records only.** A message event and its media job commit in one
transaction; failed writes leave no partial record; the signed payload is the stored
and exported payload.
Source: [EVIDENCE.md, Durable collection](EVIDENCE.md#durable-collection-and-process-receipts-02).
- A1 Nested and failed transactions keep only complete records.
- A2 Write failures are counted and reported without a partial record.

**TW-PRS-05 Checkpoints.** A checkpoint signs key, journal length, head hash and
creation time and carries the newest fetched drand round; making it never connects out.
Source: [EVIDENCE.md, Manifest and checkpoints](EVIDENCE.md#manifest-and-checkpoints).
- A1 Checkpoints made during the known-answer run are accepted by the verifier.
- A2 Checkpoint creation uses no network and carries the fetched round.

### Timestamps (TIM)

**TW-TIM-01 Receipts in the archive.** Evidence-mode replies are stored and exported;
without `--tsa-ca` the signature is reported as not checked.
Source: [EVIDENCE.md, RFC 3161](EVIDENCE.md#rfc-3161-preparation-and-response-verification-02).
- A1 Archive, JSON and console output name the reply and say the signature was not checked.

**TW-TIM-02 Reply checks.** The reply must cover the exact checkpoint bytes; with
`--request` the nonce is checked; the signature, signing certificate and chain to the
explicitly supplied root are checked at the stamped time; the signing certificate must
be for time stamping only.
Source: [TIMESTAMP.md, Verification boundaries](TIMESTAMP.md#verification-boundaries).
- A1 A changed checkpoint, a changed signature, a missing root and a wrong certificate
  reference are rejected.
- A2 A changed nonce is rejected.
- A3 A certificate invalid at the stamped time, or without the time-stamping purpose, is rejected.

**TW-TIM-03 Revocation.** OCSP or CRL evidence stored with the reply is checked;
revocation at or before genTime fails.
Source: [TIMESTAMP.md, Signing certificate revocation](TIMESTAMP.md#signing-certificate-revocation).
- A1 Good, revoked and absent revocation evidence give the documented answers.

**TW-TIM-04 Retry and deferral.** An authority failing twice waits with backoff or
`Retry-After`; deferred authorities are listed; exports skip proofs being written.
Source: [EVIDENCE.md, RFC 3161](EVIDENCE.md#rfc-3161-preparation-and-response-verification-02).
- A1 Backoff, `Retry-After` and degraded status behave as documented.
- A2 A proof still being written is not exported.

**TW-TIM-05 Chronology.** Backward steps of `observed_at` are reported in
`chronology`; signatures are still checked.
Source: [TIMESTAMP.md, Procedure](TIMESTAMP.md#procedure).
- A1 One injected backward clock step is reported as one regression.

**TW-TIM-06 drand.** `--check-drand` compares recorded rounds with relays; a round
that differs fails.
Source: [EVIDENCE.md, Optional records](EVIDENCE.md#optional-records-in-evidence-mode-drand-and-telegram-devices).
- A1 A relay answer that differs from the recorded round fails; an unavailable relay confirms nothing.

**TW-TIM-07 Minimum for evidence.** `--require evidence` exits with 2 unless the
signer is pinned and external time from a third party covers the last record.
Source: [EVIDENCE.md, Investigation handoff](EVIDENCE.md#investigation-handoff) step 4,
[SECURITY-MODEL.md, Integrity and external time](SECURITY-MODEL.md#integrity-and-external-time).
- A1 A pinned archive without external time exits 2 with `requirements_met: false`.
- A2 Unconfirmed or partial timestamps do not count.

### Exports (EXP)

**TW-EXP-01 Evidence ZIP.** `manifest.json` lists the SHA-256 of every member other
than itself and `manifest.sig`; `manifest.sig` is Ed25519 over the canonical manifest.
Source: [EVIDENCE.md, Manifest and checkpoints](EVIDENCE.md#manifest-and-checkpoints).
- A1 An independent check of the known-answer archive reproduces every member hash and
  the manifest signature, and finds the journal unchanged.

**TW-EXP-02 Sealed reports.** HTML and JSON reports carry an Ed25519 seal and must
describe the same journal as the archive.
Source: [EVIDENCE.md, Readable reports](EVIDENCE.md#readable-reports).
- A1 Signed JSON and HTML reports verify against the pinned key and keep deletion and
  absence apart.
- A2 Selected and minimised PDF reports keep their boundaries.

**TW-EXP-03 Password container.** `.tgwpw` publishes plaintext only after all records
authenticate and never overwrites a file.
Source: [EVIDENCE.md, Investigation handoff](EVIDENCE.md#investigation-handoff).
- A1 Damage is rejected without plaintext; existing files are kept; the standalone
  command works; the enclosed export keeps its signatures.

**TW-EXP-04 Handover extract.** Unchanged records verify in full; minimised records
keep their original hash and signature and name what was withheld.
Source: [EVIDENCE.md, Handover extract](EVIDENCE.md#handover-extract).
- A1 Signed disclosures are rejected after alteration, as by the earlier verifier.
- A2 A minimised handover never restores withheld content.

**TW-EXP-05 Chat export numbers.** A chat export lists absent message numbers and
`verify.py` recounts them from `chat.json`.
Source: [EVIDENCE.md, Readable reports](EVIDENCE.md#readable-reports).
- A1 Sparse numbers are counted without expansion, also across accounts.

### Verification (VER)

**TW-VER-01 Rejections.** The verifier rejects unexpected or missing members, duplicate
names, corrupt files, a broken sequence or chain, and invalid signatures.
Source: [EVIDENCE.md, Manifest and checkpoints](EVIDENCE.md#manifest-and-checkpoints).
- A1 Each altered copy in the known-answer set fails with the expected reason and exit code 1.

**TW-VER-02 Signer pinning.** A fingerprint that differs fails; without one the answer
says `signer_pinned: false`; `--strict` then exits with 2.
Source: [EVIDENCE.md, Reading a verification result](EVIDENCE.md#reading-a-verification-result).
- A1 Pinned, unpinned and strict answers match the known answers.
- A2 A journal rebuilt with another key passes unpinned and fails against the trusted fingerprint.

**TW-VER-03 Retained checkpoint.** An export may extend beyond a checkpoint and must
agree at its boundary; a shorter export fails.
Source: [HOW-IT-WORKS.md, What an earlier checkpoint adds](HOW-IT-WORKS.md#what-an-earlier-checkpoint-adds).
- A1 A later export passes an earlier checkpoint; an earlier export fails a later one.
- A2 A journal rebuilt with the collector key fails an earlier checkpoint.
- A3 A rewritten prefix is rejected when the journal has grown.

**TW-VER-04 Exit codes and order of checks.** Exit 1 for a failed check, 2 for an unmet
requirement, 3 with `--strict` for an authenticated newer format; signatures are checked
before format and payload fields.
Source: [EVIDENCE.md, Reading a verification result](EVIDENCE.md#reading-a-verification-result).
- A1 Future formats and unsigned changes give the documented codes.

**TW-VER-05 Earlier archives.** Archives made before a format change remain supported,
and the earlier verifier accepts a current archive.
Source: [EVIDENCE.md, Producer](EVIDENCE.md#producer) and
[VERIFICATION.md, Full-text search](VERIFICATION.md#full-text-search-on-one-million-messages--5-november-2026).
- A1 Frozen archives verify with the current verifier and current archives with the frozen one.

**TW-VER-06 Reviewed verifier.** The verifier shipped in archives is the build of the
reviewed verifier sources.
Source: [EVIDENCE.md, Manifest and checkpoints](EVIDENCE.md#manifest-and-checkpoints).
- A1 `tgwitness/verify.py` equals the build from `tgwitness/verifier/`.

**TW-VER-07 Comparison.** Unchanged means equality of the complete saved record;
`changed_fields` name every difference; both signers must be pinned.
Source: [EVIDENCE.md, Comparing chat exports](EVIDENCE.md#comparing-chat-exports).
- A1 Text beyond the preview and every metadata field are compared.
- A2 Comparison checks both pins and refuses checks it cannot perform.

**TW-VER-08 Required witness.** `--require-witness` refuses an export whose tail was not
witnessed; the witness key must differ from the collector key.
Source: [EVIDENCE.md, Investigation handoff](EVIDENCE.md#investigation-handoff) step 4.
- A1 Witnessed tier needs a pinned, independent key and the exact head.

**TW-VER-09 Size limit.** Declared uncompressed size is limited to 4 GiB unless
`--max-gib` raises it.
Source: [EVIDENCE.md, Manifest and checkpoints](EVIDENCE.md#manifest-and-checkpoints).
- A1 An archive declaring more than the limit is refused.

## Traceability

Test cases name the private test functions in the [bundle](#validation-bundle).
"Status" is the outcome in the [recorded run](#results-of-the-recorded-run): **pass**,
**fail (known)** for a failure listed in advance, **fail** for an unexpected failure,
**gap** where no test exists.

| Requirement | Assertion | Test case | Expected result | Status |
| --- | --- | --- | --- | --- |
| TW-ACQ-01 | A1 | TC-01 `test_validation_known_answer::test_update_stream_produces_the_expected_observations` | 12 observation records equal to the fixture | pass |
| TW-ACQ-01 | A2 | TC-02 `test_validation_known_answer::test_journal_matches_the_documented_encoding` | Every `observed_at` has a UTC offset | pass |
| TW-ACQ-02 | A1, A2 | TC-01 | `message.edited` with edit date, null actor; original `message.new` kept | pass |
| TW-ACQ-03 | A1 | TC-01 | Two `message.new` records for one update delivered twice | pass |
| TW-ACQ-03 | A2 | TC-01 | Fixture expects one record, following the code; the documentation implies two | deviation DV-01 |
| TW-ACQ-04 | A1 | TC-01 | Resolved `message.deleted`, `deletion.unscoped` [999], `deletion.batch` [1, 2] and two `message.deleted` | pass |
| TW-ACQ-04 | A2 | TC-20 `test_deletion_evidence_reports::test_unscoped_notice_does_not_claim_that_a_known_disabled_chat_was_never_saved` | Scope text distinguishes unobserved chats from unknown IDs | pass |
| TW-ACQ-04 | A3 | TC-21 `test_deletion_semantics::*` | Batch caveat wording | fail (known), 8 of 8 cases |
| TW-ACQ-05 | A1, A2 | TC-20 `test_deletion_evidence_reports` (other three tests) | Separate counts; no deletion after reappearance | pass |
| TW-ACQ-06 | A1 | TC-04 `test_validation_known_answer::test_verifier_answers_for_the_untouched_archive` | `unobserved_ids` for the group: range 3–4 | pass |
| TW-ACQ-06 | A2 | TC-22 `test_capture_liveness`, `test_assurance_boundaries` | Periods end at failures, stops and disconnects | pass |
| TW-ACQ-06 | A3 | TC-23 `test_difference_gaps` | Gap records for difference-too-long | pass |
| TW-ACQ-06 | A4 | TC-24 `test_gap_analysis` | Measurement in export, report and verifier | pass |
| TW-ACQ-07 | A1 | TC-25 `test_paused_updates` | Rewind to saved position; drops reported | pass |
| TW-ACQ-08 | A1 | TC-26 `test_file_hash_export` | All media policies verify | pass |
| TW-ACQ-08 | A2 | TC-27 `test_account_attachment_integrity` | Length contradictions rejected | pass |
| TW-ACQ-08 | A3 | TC-28 `test_chat_export_integrity::test_staged_files_cannot_replace_the_original_message` | Original file kept | pass |
| TW-PRS-01 | A1 | TC-02 | Recomputed hashes and signatures match | pass |
| TW-PRS-02 | A1 | TC-05 `test_validation_known_answer::test_workspace_journal_is_append_only_and_checked_before_export` | `Journal is append-only` | pass |
| TW-PRS-03 | A1 | TC-05 | Export refused: `Changed content at event 2` | pass |
| TW-PRS-04 | A1 | TC-29 `test_store_transactions` | Only complete records after failures | pass |
| TW-PRS-04 | A2 | TC-30 `test_journal_write_failures` | Failures counted; no partial record; signed = stored = exported payload | pass |
| TW-PRS-05 | A1 | TC-06 `test_validation_known_answer::test_retained_checkpoints_accept_extension_and_reject_truncation` | `checkpoint_checked: true` | pass |
| TW-PRS-05 | A2 | TC-31 `test_checkpoint_drand_route` | No connection; round carried | pass |
| TW-TIM-01 | A1 | TC-32 `test_tsa_cert_reference::test_archive_json_and_console_expose_reference_without_claiming_unchecked_signature` | "not checked (use --tsa-ca)" | pass |
| TW-TIM-02 | A1 | TC-32 `test_tsa_cert_reference::test_reference_warning_cannot_bypass_certificate_signature_or_imprint_checks`, `test_recorded_timestamp_vectors_still_verify` | Each alteration rejected; recorded replies verify | pass |
| TW-TIM-02 | A2 | — | Changed nonce rejected | gap |
| TW-TIM-02 | A3 | — | Expired or wrong-purpose certificate rejected | gap |
| TW-TIM-03 | A1 | — | OCSP/CRL answers | gap |
| TW-TIM-04 | A1 | TC-33 `test_anchor_backoff` | Backoff, `Retry-After`, degraded | pass |
| TW-TIM-04 | A2 | TC-34 `test_anchor_temp_files` | Partial proof not exported | pass |
| TW-TIM-05 | A1 | TC-04 | `chronology.regressions` = 1 | pass |
| TW-TIM-06 | A1 | TC-35 `test_witness_freshness::test_relay_mismatch_fails_and_unavailable_is_absent` | Mismatch fails; offline confirms 0 (witness journal path only) | pass |
| TW-TIM-07 | A1 | TC-04 | Exit 2, `requirements_met: false` | pass |
| TW-TIM-07 | A2 | TC-36 `test_assurance_ladder::test_unconfirmed_or_partial_timestamp_does_not_count`, `test_assurance_chain` | Not counted | pass |
| TW-EXP-01 | A1 | TC-03 `test_validation_known_answer::test_archive_matches_the_documented_manifest` | Hashes, signature and journal match | pass |
| TW-EXP-02 | A1 | TC-20 | Reports verify with the pinned key | pass |
| TW-EXP-02 | A2 | TC-37 `test_independent_report_pdf` | Boundaries kept | pass |
| TW-EXP-03 | A1 | TC-38 `test_password_export` | As documented | pass |
| TW-EXP-04 | A1 | TC-39 `test_verifier_account_compatibility::test_signed_disclosure_rejections_match_old_verifier` | Same rejections as earlier verifier | pass |
| TW-EXP-04 | A2 | TC-37 `test_independent_report_pdf::test_minimised_handover_never_restores_original_content_or_operator_analysis` | Withheld content absent | pass |
| TW-EXP-05 | A1 | TC-40 `test_chat_export_integrity::test_sparse_message_numbers_are_counted_without_expansion`, `test_multi_account_recovery_does_not_expand_missing_numbers` | Counts without expansion | sparse numbers: fail (known); multiple accounts: pass |
| TW-VER-01 | A1 | TC-07 `test_validation_known_answer::test_tampered_copies_fail_with_the_expected_reason` (8 alterations) | Exit 1 with the fixture's reason | pass |
| TW-VER-02 | A1 | TC-04, TC-41 `test_verifier_output_safety::test_unpinned_is_explicit_and_strict_is_opt_in` | Exit 0 / 0 / 2 | pass |
| TW-VER-02 | A2 | TC-07 `rewritten_with_other_key` | Exit 0 unpinned; exit 1 with trusted fingerprint | pass |
| TW-VER-03 | A1 | TC-06 | Exit 0; exit 1 `Journal is shorter than the retained checkpoint` | pass |
| TW-VER-03 | A2 | TC-07 `rewritten_with_collector_key` | Exit 1 `Journal disagrees with the retained checkpoint` | pass |
| TW-VER-03 | A3 | TC-42 `test_witness_continuity` | Rewritten 1,000-record prefix rejected at 1,100 | pass |
| TW-VER-04 | A1 | TC-41 `test_verifier_output_safety::test_signature_before_format_and_before_required_payload_fields`, `test_future_format_exit_codes`; TC-36 `test_assurance_ladder::test_cli_legacy_and_required_tier_exit_codes` | Codes 1, 2, 3 as documented | pass |
| TW-VER-05 | A1 | TC-43 `test_fulltext::test_verifier_accepts_archive_from_before_full_text`, `test_previous_verifier_accepts_current_archive`; `test_verifier_account_compatibility`; `test_verifier_sources` (frozen decisions); `test_verifier_dispatch` | Same decisions as frozen results | partial: `test_fulltext` and `test_verifier_account_compatibility` pass; frozen decisions fail (known) in 9 `test_verifier_sources` and 2 `test_verifier_dispatch` cases |
| TW-VER-06 | A1 | TC-44 `test_verifier_sources::test_committed_verifier_matches_reviewed_sources` | Identical build | pass |
| TW-VER-07 | A1 | TC-45 `test_verifier_comparison` | Complete-record comparison | pass, 22 cases; 1 fail (known): an OTS-structure-only receipt label |
| TW-VER-07 | A2 | TC-41 `test_verifier_output_safety::test_comparison_checks_both_pins_and_sanitizes_its_separate_output_path` | Both pins checked | pass |
| TW-VER-08 | A1 | TC-36 `test_assurance_ladder::test_witness_requires_pin_independent_key_and_exact_head` | Refused without pin, independent key or exact head | pass |
| TW-VER-09 | A1 | — | Over-limit archive refused | gap |

Tests in the suite without a documented requirement of their own are kept, for example
the verifier's removal of terminal control characters
(`test_verifier_output_safety::test_all_c0_c1_controls_removed_except_newline_tab`).

## Known-answer dataset

`tools/fixtures/validation/known-answer-v1.json` in the bundle is a synthetic Telegram
update stream with the answers it must produce. The test builds Telethon `Message` and
`Update*` objects from it and hands them to the collector's own update handlers
(`on_new`, `on_edit`, `on_delete`) with media download off. The collector clock is
replaced by a deterministic clock so that observation times are repeatable. Nothing
is sent to Telegram.

| Step | Input | Expected journal record |
| --- | --- | --- |
| 1 | New message 101 in a private chat, "KA-1 meet at 10:00" | `message.new`, actor 5150, `source_at` 08:59:00 |
| 2 | The same update again | A second `message.new` |
| 3 | Edit of 101, "KA-1 meet at 11:00", edit date 09:01:00 | `message.edited`, null actor, `source_at` 09:01:00 |
| 4 | The same edit again | No record (DV-01) |
| 5 | New message 102 | `message.new` |
| 6 | Account-level deletion of 102 | `message.deleted` in the private chat, `chat_resolution` set, null actor and date |
| 7 | Account-level deletion of 999, never saved | `deletion.unscoped` with [999] |
| 8 | Checkpoint and export "early" | 6 records |
| 9 | Collector clock set back one hour | — |
| 10 | Group messages 1, 2 and 5 from sender 6161 | Three `message.new` |
| 11 | Group deletion of 1 and 2 | `deletion.batch` [1, 2], then two `message.deleted` |
| 12 | Checkpoint and export "final" | 12 records |

Expected verifier answers for the untouched final archive:

| Command options | Exit | Answer |
| --- | --- | --- |
| `--json --fingerprint PIN` | 0 | `verified: true`, `signer_pinned: true`, profile `integrity`, `chronology.regressions` 1, group not observed 3–4 |
| `--json` | 0 | `signer_pinned: false` |
| `--json --strict` | 2 | `requirements_met: false` |
| `--json --fingerprint PIN --require evidence` | 2 | `requirements_met: false` (no external time) |
| final archive, `--checkpoint` early | 0 | `checkpoint_checked: true` |
| early archive, `--checkpoint` final | 1 | `Journal is shorter than the retained checkpoint` |

Altered copies of the final archive, each verified with the trusted fingerprint:

| Alteration | Exit | Expected reason |
| --- | --- | --- |
| Edit text in `events.jsonl` | 1 | `File hash mismatch: events.jsonl` |
| Also put the new hash in `manifest.json` | 1 | `InvalidSignature` (manifest) |
| Collector key holder edits text and re-signs the manifest | 1 | `Changed content at event 3` |
| Key holder recomputes the hash chain, re-signs the manifest, keeps record signatures | 1 | `InvalidSignature` (record) |
| Key holder removes one record and re-signs the manifest | 1 | `Broken sequence or hash chain at event 3` |
| Add a member the manifest does not list | 1 | `Unexpected or missing bundle members` |
| Store `events.jsonl` twice | 1 | `Duplicate ZIP members` |
| Zero `manifest.sig` | 1 | `InvalidSignature` |
| Rebuild the whole journal with the collector key | 0 | Passes alone; with the early checkpoint exit 1, `Journal disagrees with the retained checkpoint` |
| Rebuild the whole journal with another key | 0 | `signer_pinned: false`; with the trusted fingerprint exit 1, `Public key differs from the independently trusted fingerprint` |

In the workspace, `UPDATE` and `DELETE` on the journal table fail with
`Journal is append-only`; a row changed after removing the trigger stops the export with
`Changed content at event 2`.

The two rebuilt journals show the documented trust boundary: a holder of the collector
key can produce a consistent replacement, and only a checkpoint obtained earlier through
another channel, external time or a witness reveals it
([HOW-IT-WORKS.md](HOW-IT-WORKS.md#what-an-earlier-checkpoint-adds)).

## Results of the recorded run

Run 2, 14 November 2026, 08:03:42 to 08:05:08 UTC, on Ubuntu 24.04.5 LTS (Linux 6.8.0,
x86_64), Python 3.12.3, pytest 9.2.0, Telethon 1.45.0, cryptography 50.0.2. The package
files under test were compared after the run, file by file, with `c06a2ba5a`: all 421
`.py`, `.js`, `.css`, `.html` and `.svg` files were identical.

| Attempt | Cases | Passed | Failed | Skipped | pytest exit | Unexpected failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 395 | 374 | 21 | 0 | 1 | 0 |
| 2 (retry of the 21) | 21 | 0 | 21 | 0 | 1 | 0 |

All 21 failures were listed in `suite.json` before the run; the retry did not change any
of them. The bundle's exit status was 0 because no failure was unexpected; pytest's own
exit status was 1 in both attempts.

| File | Failed cases | Reason given in advance |
| --- | ---: | --- |
| `test_deletion_semantics` | 8 of 8 | The batch-deletion caveat was shortened; the test expects the earlier text |
| `test_verifier_sources` | 9 of 24 | Frozen verifier decisions predate the shortened answer wording |
| `test_verifier_dispatch` | 2 of 22 | Same frozen decisions |
| `test_verifier_comparison` | 1 of 23 | An OTS-structure-only receipt is now labelled synthetic, not unknown |
| `test_chat_export_integrity` | 1 of 16 | Missing-number counting returns a new type; the test uses the earlier interface |

The known-answer test passed all 16 cases. Every other file in the suite passed all its
cases. No case was skipped.

Run 1, 07:59:53 to 08:01:17 UTC the same day, is kept in the bundle but does not count as
a run of `c06a2ba5a`: its `tgwitness/verify.py` (SHA-256 `32d881aa…`) matches no commit
of the repository, so the host's base copy was not that revision at the time. It also
exposed two errors in the bundle definition: `test_chat_comparison.py` and
`test_release_data_fixes.py`, imported by two tests, were missing, so those two cases
failed with `ModuleNotFoundError`. Run 2 adds them as support files and is otherwise the
same suite.

## Deviations

| ID | Documented | Observed | Significance |
| --- | --- | --- | --- |
| DV-01 | EVIDENCE.md: "There is no duplicate-delivery suppression" | An edit update whose text and edit date equal the last saved version is not recorded (`Collector.on_edit`); a new-message update from difference recovery (`pts` 0) is skipped when the message is already saved (`Collector.on_new`). A plain repeated new-message update is recorded twice. | A repeated identical edit leaves one receipt, not two. The content record is complete; the count of deliveries is not. The documentation sentence needs a qualification or the code a change; this record does not decide which. |
| DV-02 | — | A holder of the collector key can remove the reports and `SHA256SUMS` from an archive, re-sign the manifest and have the rest verify. | Within the documented boundary: the collector key vouches for its own archives. Compare reports with the original package. |
| DV-03 | Frozen verifier decisions | Known failures in `test_verifier_sources`, `test_verifier_dispatch`, `test_verifier_comparison`, `test_deletion_semantics`, `test_chat_export_integrity` listed in advance | Wording or API changes after the frozen fixtures were made; until the fixtures are regenerated these tests do not confirm TW-VER-05 or TW-ACQ-04 A3. |

## Gaps: assertions without a test

| Assertion | What is missing |
| --- | --- |
| TW-TIM-02 A2 | A reply checked with `--request` against a query whose nonce differs |
| TW-TIM-02 A3 | A signing certificate outside its validity at genTime, or without the time-stamping purpose |
| TW-TIM-03 A1 | Stored OCSP and CRL evidence: good, revoked before and after genTime, absent |
| TW-TIM-06 | A drand mismatch for rounds recorded in an evidence archive (the witness path is tested) |
| TW-VER-09 A1 | An archive declaring more than 4 GiB, and `--max-gib` |
| TW-EXP-02 | Independent check of the PDF CMS signature over `/ByteRange` |

## Known limitations and what the tests leave open

- **Synthetic acquisition.** Telegram objects are built in the test and passed to the
  collector's handlers. The tests do not show that Telegram delivers a given update to a
  given account, how fast, or completely. Live runs are in [VERIFICATION.md](VERIFICATION.md).
- **Developer testing.** The maintainer wrote the product, the tests and the expected
  answers and ran them. SWGDE 18-Q-001 §5.6 recommends a tester independent of the developer.
- **Expected answers follow the documentation where it is specific.** Where code and text
  differ, the fixture follows the code and the difference is listed as a deviation.
- **One environment.** One Linux host with the recorded package versions. Windows, macOS
  and the portable verifier runtime were not part of this run.
- **No legal qualification.** Passing these tests says that the program behaved as
  documented on this data. It says nothing about admissibility, the qualification of a
  signature or time stamp, or the procedural validity of an acquisition.
- **Selected suite.** The bundle runs 29 test files mapped to the requirements above,
  not the maintainer's whole private suite, the capture add-on or browser tests.
- **Counts.** Test counts are parametrized cases from one run. They are not a measure of
  the project's cumulative testing.

## How to reproduce

Use a disposable Linux environment with Python 3.12 and the project dependencies
(`deploy/constraints.txt`), a checkout of the tested revision and the bundle's test files
copied over it, keeping their paths.

```sh
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
git checkout --detach c06a2ba5a
# copy the bundle's tools/ files into this checkout
python -m pip install -c deploy/constraints.txt -e . pytest
python tools/validation_bundle.py --out results/run-1 --retries 1 --operator "NAME, ORGANISATION"
```

`validation_bundle.py` refuses an existing output directory. It records the source
version, `source_tree_sha256`, the SHA-256 of every test and support file, the operating
system, Python and `pip freeze`, then runs pytest once with JUnit XML and a full log. With
`--retries`, failed cases run again as a new attempt with their own XML and log; the first
attempt is never replaced, and the exit status follows the first attempt. `run.json` holds
the commands, UTC start and end, exit codes, per-case outcomes and failure messages;
`SHA256SUMS` covers every result file. Known failures are annotated from the suite
definition, not removed.

Single command for the known-answer test only:

```sh
TGW_VALIDATION_RECORD=known-answer.jsonl python -m pytest -q tools/test_validation_known_answer.py
```

`known-answer.jsonl` then lists every observed answer next to the expected one.

## Validation bundle

Prepared by the maintainer; publication at a public address is a separate decision of the
project owner and has not happened. The bundle would contain:

| File | Content |
| --- | --- |
| `VALIDATION.md` | This page at the tested revision |
| `tools/fixtures/validation/suite.json` | Test files, support files and known failures |
| `tools/…` | The 29 test files, `validation_bundle.py`, the known-answer fixture, support modules and fixtures named in `suite.json`, unchanged |
| `results/run-N/` | `run.json`, `attempt-*.junit.xml`, `attempt-*.log`, `pip-freeze.txt`, `SHA256SUMS` for each recorded run, including failed attempts |
| `SHA256SUMS` | Hashes of all bundle files |

Hashes identify bytes. Who ran a test is stated in `run.json`; an independent
reproduction is a separate record under the reproducer's name.

[Evidence format](EVIDENCE.md) · [Verification record](VERIFICATION.md) ·
[Timestamps](TIMESTAMP.md) · [Security model](SECURITY-MODEL.md)
