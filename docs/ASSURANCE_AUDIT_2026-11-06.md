# Assurance verification audit: 2026-11-06

Five groups of semantic verification defects were reproduced against
`962c15ece4888e5394e4cc16e6cb5c9f64ff901d` and fixed. Correct signatures did not
prevent incorrect conclusions about capture continuity, TCB status, quoted key
binding, message equality, or the number of records actually examined.

This is a focused audit of collector failure handling, coverage calculation,
TDX quote policy, journal binding and chat-export comparison. It is not a review
of the whole product, a penetration test of a live deployment, or a demonstration
of an Intel signature forgery. Severity below concerns evidence interpretation;
it does not imply remote code execution or a demonstrated remote trigger.

## High priority

### 1. Capture failures could leave continuous observation active

**Impact:** a verified report could include time after message capture stopped
in its continuous-observation interval.

Baseline: [collector.py:1932](https://github.com/phishdestroy/TgWitness/blob/962c15ece4888e5394e4cc16e6cb5c9f64ff901d/tgwitness/collector.py#L1932),
[failure:2077](https://github.com/phishdestroy/TgWitness/blob/962c15ece4888e5394e4cc16e6cb5c9f64ff901d/tgwitness/collector.py#L2077),
[Coverage.add:777](https://github.com/phishdestroy/TgWitness/blob/962c15ece4888e5394e4cc16e6cb5c9f64ff901d/tgwitness/verify.py#L777).

`supervise()` stopped the collector without `observation.stopped`. The verifier
ignored `collector.error`, current-client `connection.closed` and disconnected
heartbeats, and advanced liveness on every record. Ten subsequent administrative
records extended a failed capture through second 670. A separate case showed
disconnect, explicit stop and late `connection.restored` reopening observation.

Fix: record fatal state and an explicit stop before asynchronous cleanup; clean
up even when journal writes fail. The verifier tracks observation intent
separately from confirmed connected capture. Only a matching run's connected
heartbeat can extend or resume an existing observation. Stop/restart and account
loss require a new observation start. Nonfatal errors retain an uncertainty gap
until capture is confirmed again. Candidate-client closure is not a capture
boundary. HTML/PDF reports use the verifier's explanation instead of an
unqualified live-status badge.

Tests use the real `Collector`, `Store`, ZIP exporter and `verify_bundle()` with
a pinned Ed25519 key, including full-disk failure and an active independent
export. No remote means of causing a collector failure was demonstrated.
If the final journal contains no later records, a silent crash cannot be dated;
the last capture confirmation is explicitly not a claim of present activity.

### 2. Export comparison could call different messages unchanged

**Impact:** differences beyond the first 300 characters, changed link targets or
reply context, and changed captions on the same file could escape comparison.

Baseline: [row_brief/row_content:1931](https://github.com/phishdestroy/TgWitness/blob/962c15ece4888e5394e4cc16e6cb5c9f64ff901d/tgwitness/verify.py#L1931),
[compare_chat_exports:1946](https://github.com/phishdestroy/TgWitness/blob/962c15ece4888e5394e4cc16e6cb5c9f64ff901d/tgwitness/verify.py#L1946).

The comparison reused display excerpts as equality inputs. Cross-account
candidate matches were counted as unchanged without comparing their contents.

Fix: compare complete text and explicit message fields, including entities,
sender, reply/forward context, media descriptors and service actions. Candidate
matching and equality are separate; both comparison modes check equality.
Results identify changed fields and enumerate the fields covered by the claim.
Missing account/chat identities no longer qualify for message-number matching.

Tests verify two independently signed archives before comparing them and include
an unchanged-message control across accounts. Equal compared fields do not
establish complete history or the absence of intermediate unseen edits.

## Medium priority / conditional applicability

### 3. Unsupported QE TCB statuses were accepted and lost in convergence

Baseline: [converge:249](https://github.com/phishdestroy/TgWitness/blob/962c15ece4888e5394e4cc16e6cb5c9f64ff901d/tgwitness/tdx.py#L249),
[check_qe:343](https://github.com/phishdestroy/TgWitness/blob/962c15ece4888e5394e4cc16e6cb5c9f64ff901d/tgwitness/tdx.py#L343).

`ConfigurationNeeded` and `OutOfDateConfigurationNeeded` could be accepted as
QE statuses and disappear into aggregate `UpToDate`, which cloud policy passes.

Fix: accept only `UpToDate`, `OutOfDate` and `Revoked` for QE identities, matching
[Intel QVL IdentityTcbLevel](https://github.com/intel/confidential-computing.tee.dcap.qvl/blob/main/Src/AttestationParsers/src/Json/IdentityTcbLevel.cpp).
Convergence explicitly rejects unsupported inputs. Tests exercise all 21
supported platform/component combinations and signed unsupported QE identities.

The synthetic PKI runs full certificate, CRL and quote verification against its
test root. The same synthetic evidence remains rejected by the pinned Intel
root. Genuine Intel and dstack fixtures still pass. Applicability to a deployed
platform with genuine Intel collateral containing the unsupported values was
not established.

### 4. A quoted start without a key could pass journal binding

Baseline: [verify_tdx_journal:1966](https://github.com/phishdestroy/TgWitness/blob/962c15ece4888e5394e4cc16e6cb5c9f64ff901d/tgwitness/cloud.py#L1966).

The key comparison was conditional on a truthy `run.public_key`. A quote that
covered a start without a key therefore passed the journal check. Empty keys
also passed; malformed nonempty keys escaped as decoding exceptions.

Fix: every quoted start must contain a valid 32-byte Ed25519 public key matching
the independently expected journal fingerprint. Missing, empty, malformed or
different keys produce a failed binding check.

Tests use the existing Phala/TDX test PKI and real signed journal exports. The
unmodified code returned journal `pass` for absent/empty keys. This demonstrates
missing verifier validation, not a way to obtain such an unbound quote from an
approved production collector. Binding a start to a key also does not itself
provide external freshness, prevent journal suffix withholding or establish
message completeness; retained checkpoints and independent witnesses remain
separate evidence.

### 5. Signed chat exports could silently omit records from verification

Baseline: [chat_messages:2137](https://github.com/phishdestroy/TgWitness/blob/962c15ece4888e5394e4cc16e6cb5c9f64ff901d/tgwitness/verify.py#L2137),
[check_attachments:2110](https://github.com/phishdestroy/TgWitness/blob/962c15ece4888e5394e4cc16e6cb5c9f64ff901d/tgwitness/verify.py#L2110).

The line-oriented parser could return no messages for a compact JSON document,
skip non-object rows, and ignore the signed declared count. Duplicate message
IDs could later overwrite one another in number-based comparison.

Fix: require the producer's streaming record layout, validate its header and
terminator, reject malformed/non-object rows and duplicate IDs, and compare the
actual record count with the signed manifest. Unsupported JSON layouts now fail
explicitly; external tools must preserve the documented one-object-per-line
export layout instead of reformatting `chat.json`.

Tests re-sign each malformed archive correctly, so rejection depends on semantic
validation rather than an incidental signature/hash mismatch. These cases
require malformed signed input; they do not show modification of an archive
without access to its signing key.

## Reproduction and validation

- `python -m pytest tools/test_assurance_boundaries.py -q`
- `python tools/check_tdx.py`
- `python tools/check_phala.py`
- `python tools/check_account_recovery.py`
- Export, distributed-export, hash-export and selected-report regression suites.
- Ruff, publication checks and immutable sealed-release validation.

The new regression file is part of the normal CI suite. All fixture credentials,
accounts, clouds and keys used by these tests are synthetic; no real Telegram
account, RunPod allocation or Cloudflare deployment is required.

Local validation: 104 export/comparison regressions, then 78 final boundary and
report-metadata cases passed; these counts overlap. All 43 TDX cases passed.
Phala's 20 other cases passed and its source-reference case passed after rerunning
against the finished source tree. Account recovery passed. The report browser
check passed in English, Russian and German at widths 320, 390, 768 and 1440,
including signed HTML/JSON/PDF, offline rendering and disabled JavaScript.
Ruff and publication/link checks passed. GitHub checks are recorded on the PR.
