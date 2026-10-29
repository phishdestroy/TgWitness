# Project and publication audit — 29 October 2026

For changes made after this snapshot, see the
[audit recheck](RECHECK-2026-10-29.md), including new findings A8–A11 and fresh
validation of the revised interface and multilingual site. Counts and build
results below describe the original snapshot.

The current project passes its existing automated tests, but the release candidate
still has confirmed defects in portable packaging, verifier resource limits and
export lifecycle handling. Fix the two P1 code findings before distributing a
release. Resolve the publication gate below before making the first commit or
uploading existing artifacts.

This is a fresh audit of the working files after the English wiki and reference-site
changes. Earlier fixes to staged-content checking, failed workspace deletion and
authentication throttling were reviewed as existing behavior, not counted as new
unresolved findings. Application source was not changed during this audit.

## Scope and evidence

The reviewed public snapshot contains **307 files**: 69 application/package files,
44 test files, 25 tools, 100 documentation/assets files, 22 website files, 10
deployment files, 10 GitHub files and 27 root files. This report is an additional
file. The snapshot manifest records SHA-256 for every file.

Review covered authentication and workspace dispatch; vault/session handling;
collection, persistence and restart behavior; exports, verification and witness
proofs; proxy/HTTP and replica boundaries; frontend rendering; package contents;
CI/release definitions; and English user documentation. Deep manual review focused
on trust boundaries, concurrent operations and failure cleanup. Passing tests and
this review do not constitute exhaustive proof that every execution path is safe.

All new reproductions used temporary synthetic workspaces or in-memory responses.
No real Telegram authorization was used, no account was contacted, and the existing
collector was not restarted. No commit, staging change or publication was performed.

### Executed checks

| Check | Result |
| --- | --- |
| Full existing pytest suite | **396 passed, 3 skipped**, 195.06 seconds; 2 deprecation warnings |
| Ruff, configured F/E9 rules | Passed |
| Installed dependency consistency (`pip check`) | Passed |
| Public-file/link/recognized-secret check at audit start | 307 files, 1,550 local links; passed |
| Publication check including this report | 308 files, 1,564 local links; passed |
| Existing Git index | Failed: incomplete and different from the reviewed working files |
| Additional failure/concurrency probes | **6 defects reproduced**, detailed below |
| Main application Chromium acceptance | Passed; no page errors or external requests |
| Workspace Chromium acceptance | Passed, including failed deletion and delayed responses |
| Additional application Chromium acceptance | All six passed: account, interactions, quick controls, proof, setup and public proxies; eight application browser suites passed in total |
| Documentation/reference-site Chromium acceptance | Passed: 12 guide/index pages, 18 reference pages, widths 320–1440, keyboard and no-JavaScript paths |
| Public landing-site Chromium acceptance | Passed: responsive layout, keyboard, clipboard denial, reduced motion and no-JavaScript paths; no external requests or JavaScript errors |
| Fresh wheel, source ZIP, wiki and site builds | Passed in a separate copy containing only public source |
| Wheel/source content comparison | 69 packaged application files match source; source ZIP matches all 307 public input files |
| Installed-wheel HTTP/export smoke check | Passed; streamed download independently verified, 32 synthetic journal events |
| Runtime advisory audit (`pip-audit 2.10.1`, strict, pinned constraints) | **38 packages, 0 known vulnerabilities, 0 skipped** at audit time |

The three pytest skips are POSIX permissions and two symlink checks unavailable on
this Windows/filesystem combination. Linux, macOS and Docker execution was not
performed here; Docker and Podman are unavailable. CI definitions are present, but
no successful remote run was established during this audit.

Local evidence is intentionally outside the public source allowlist:

```text
test-results/audit-final-project-pytest.log
test-results/audit-final-repro.py
test-results/audit-final-repro.json
test-results/audit-final-inventory.json
test-results/audit-final-git-index.log
test-results/audit-final-browser.log
test-results/audit-final-workspace-browser.log
test-results/audit-final-docs-browser.log
test-results/audit-final-site-browser.log
test-results/audit-final-build.json
test-results/audit-final-install-check/install-receipt.json
test-results/audit-final-project-dependencies.json
```

On this Windows/Python 3.12 host, the retained synthetic reproductions can be run
with `.venv\Scripts\python.exe test-results/audit-final-repro.py`. Their receipt
uses `confirmed: true` to mean the current defect was reproduced, not that the
application passed a regression test. The portable probe intentionally relies on
Windows file-lock behavior and stubs runtime installation/execution.

## Confirmed findings

P1 means address before release because confidentiality or safe processing of an
untrusted artifact is affected. P2 means a reproducible functional/reliability
defect that should be fixed in the same release preparation. No P0 was confirmed.

### A1 — P1: rebuilding a portable package can publish residual private files

**Location:** [portable builder](../../tools/build_portable.py#L128), cleanup at
line 128 and ZIP enumeration at line 174.

The builder reuses `build/portable/TgWitness-<version>`, suppresses deletion errors
with `shutil.rmtree(..., ignore_errors=True)`, then includes every remaining file
under that directory in the release ZIP. When an old portable instance has created
`data/` there, a locked file can survive cleanup while the runtime subdirectory is
successfully recreated. There is no final file allowlist protecting the archive.

**Reproduction:** put a synthetic private marker under the previous build's
`data/`, keep the file open on Windows, and invoke the real cleanup/archive path.
Only dependency installation and the runtime subprocess were stubbed. The resulting
ZIP included `TgWitness-0.6.1/data/private-marker.txt`. No real private file was used.

**Impact:** a locally rebuilt release can contain account data or other remnants.
A fresh GitHub runner reduces this trigger; it does not make local builds safe.
This finding does not establish that any existing published archive leaked data.

**Fix:** build in a new, verified temporary directory; fail when cleanup or output
validation fails; reject linked paths and any `data/`, session, token or key files
before archiving; replace the final artifact only after validation. Add a Windows
locked-residual-file regression and inspect the final ZIP, not only the source.

### A2 — P1: verifier size limits do not cover all archive entry points

**Location:** [format detection](../../tgwitness/verify.py#L465) and
[witness verification](../../tgwitness/verify.py#L594).

`verify_bundle()` and `verify_chat_export()` check expanded archive size, but the
CLI first calls `bundle_format()`, which reads all of `manifest.json` without a
limit. `verify_witness()` has no corresponding expanded-size check and reads files
and the entire event journal into memory. A valid signature is not required before
the initial manifest allocation.

**Reproduction:** reduce the shared size setting to one byte in an isolated probe.
A valid 53,289-byte witness archive still verifies, and format detection reads its
manifest. This small test demonstrates the missing check without allocating a
multi-gigabyte archive. Large-memory exhaustion was not attempted.

**Impact:** an oversized or heavily compressed archive can exhaust memory before
the advertised limit protects the verifier. This is an availability issue; it does
not demonstrate signature forgery.

**Fix:** use one archive-opening validator before format detection and every
verification path. Enforce member count, total expanded size and a much smaller
manifest limit; bound actual reads as well as declared sizes. Stream witness
hashing and event processing. Add tests for CLI format detection, direct witness
verification and an evidence export accompanied by `--witness`.

### A3 — P2: chunked HTTP responses are read before the response limit is checked

**Location:** [HTTP client](../../tgwitness/netclient.py#L85).

For chunked transfer encoding, `request()` passes the peer's chunk length directly
to `reader.readexactly(count + 2)`. The size check in `take()` runs only after that
read has completed. The same whole-chunk allocation also affects streamed sinks.

**Reproduction:** with `limit=16`, a synthetic response advertising a 65,536-byte
chunk caused a 65,538-byte read before `Response too large`. No remote request or
large allocation was required.

**Impact:** a hostile or broken HTTP endpoint can defeat the intended memory bound;
timestamp, proxy-feed and S3 operations use this client. TLS and configured endpoint
trust restrict the threat surface but do not enforce the response budget.

**Fix:** reject an oversized advertised chunk before reading it for bounded
responses. Read permitted chunks in fixed-size pieces, including sink mode, enforce
an overall budget where appropriate, and validate chunk terminators. Add a test
that checks the largest requested read, not only the eventual exception.

### A4 — P2: one account can enter individual and multi-account exports together

**Location:** [multi-account reservation](../../tgwitness/multi_export.py#L123)
and [individual export start](../../tgwitness/collector.py#L1402).

Eligibility is checked before awaited Telegram resolution. The multi-account
worker assigns `export_claim` only after resolution and does not atomically recheck
or reserve it. Root and child applications have separate operation locks.

**Reproduction:** pause resolution for a child participating in a multi-account
export, start an individual export through that child's API, then finish resolution.
Both starts return HTTP 200; the same collector has an active individual export
task and a multi-account claim simultaneously.

**Impact:** the application's one-export-per-account rule is broken. Requests and
progress/lifecycle management can overlap unexpectedly. This probe did not prove
archive corruption or bypass Telegram's server-side rate limiting.

**Fix:** introduce an account-level reservation shared by both export types. Acquire
it before the first await, release it on every failure/cancellation path, and use a
stable ordering for multi-account reservations. Test both start orderings with
explicit asynchronous barriers.

### A5 — P2: deleting a participant closes resources while its multi-export runs

**Location:** [workspace deletion](../../tgwitness/profiles.py#L111),
[collector shutdown](../../tgwitness/collector.py#L875), and
[multi-export failure recording](../../tgwitness/multi_export.py#L207).

Deleting a child exits its lifespan and closes its store. The multi-export task
belongs to the root application, so child shutdown does not stop that task. Its
`export_claim` is not a cancellation handle. The worker can continue using the
closed store and open scratch files.

**Reproduction:** hold an open synthetic range file while deleting its child lead
workspace. Deletion correctly reports HTTP 400 because Windows cannot remove the
open file, but the worker remains alive after the store has closed. Releasing the
worker produces an unhandled `ProgrammingError` while recording export failure.
Retrying deletion after the worker exits succeeds.

**Impact:** incomplete deletion and broken export cleanup/diagnostics can occur
together. The earlier fix that keeps failed deletion visible remains useful, but
does not coordinate the root export's lifecycle.

**Fix:** before closing any participating workspace, cancel and await the owning
multi-export (or reject deletion while it is active). Coordinate with the same
reservation mechanism as A4 and keep the store alive through terminal-state
recording. Test deletion of a lead and a non-lead during fetch and bundle assembly.

### A6 — P2: export preparation failures leave completed tasks marked running

**Location:** [individual export setup](../../tgwitness/collector.py#L1422) and
[multi-export setup](../../tgwitness/multi_export.py#L99).

Directory creation and the initial journal append happen before each worker's
`try`/failure handler. The API has already created a record with `phase=running`.
If preparation raises, the background task finishes exceptionally without updating
that record.

**Reproduction:** use a regular file named `temporary-exports` in a synthetic
workspace. Both individual and multi-account starts return HTTP 200. Both tasks
finish with `FileExistsError`; polling continues to report `running`. A permission
or storage failure at the same unguarded operation follows the same control path,
but those failures were not separately injected.

**Impact:** the UI can wait indefinitely on an export that will never finish, and
the intended interruption event is missing.

**Fix:** put all worker setup under the lifecycle handler; always update in-memory
terminal state even if writing the diagnostic journal entry fails. Clean up only
resources actually created and consume unexpected task exceptions. Add setup,
write and logging-failure regressions for both export types.

### A7 — P2: operations guidance contradicts implemented encryption and polling

**Location:** [operations backup guidance](../OPERATIONS.md#backup-restore-and-interruptions)
and the final capacity/readiness paragraph (lines 197 and 220–222).

The guide states that TgWitness does not encrypt exports and lists encrypted
exports and priority polling as future work. Password-protected export routes,
`encrypt_export()` and priority settings are already implemented; other pages
describe them. The contradiction is also reproduced in the reference site because
it renders the same Markdown.

**Impact:** users receive inconsistent instructions about protecting exported data
and whether current features exist.

**Fix:** distinguish optional password-protected export containers, unencrypted
default exports, the unencrypted local journal/media, and full service backups.
Describe existing priority rechecks separately from unimplemented polling modes.
Update the source Markdown and rebuild the reference site together.

## Publication gate: the index and existing source ZIP are stale

The existing index is not the audited snapshot. At the start of the audit,
**171 public files were absent from the index and 74 indexed files differed from
the working files**. Including this report, there are 172 missing public files. The
publication checker correctly rejects the state; this is a release-preparation
blocker rather than a new defect in that checker.

The existing `dist/TgWitness-0.6.1-source.zip` is also behind the audited source:
it omits `tools/site_wiki.py`, `tools/site_diagrams.py` and
`website/guides/en/security.html`, and contains 15 outdated files. This report is
another subsequently added file. Publishing that ZIP would omit code imported by
the new site builder. The exact differences are in the inventory receipt.

**Action:** after fixing the findings, stage only the reviewed public allowlist,
inspect the staged diff, rerun `tools/check_publication.py --git-index`, and rebuild
artifacts from the exact staged/committed revision. Retain the final input manifest
and hashes alongside the release. Do not upload the old `dist/` files by habit.
This audit deliberately preserved the user's existing index and release artifacts.

The separately built audit candidate verifies that current public inputs can build
successfully; it still contains the defects above and is not an approved release.

## Recommended implementation order

1. Fix portable isolation/validation (A1) and the verifier's common archive limits
   (A2), with the reproduced failure cases as regression tests.
2. Bound chunked reads (A3), then implement shared export reservations and deletion
   coordination (A4/A5) as one lifecycle change. Handle setup failures (A6) in both
   exporters at the same time.
3. Correct operations/reference documentation (A7). Keep the wiki English and
   maintain one source for facts repeated across wiki, README and the website.
4. Run targeted regressions and the full suite, then rebuild and test installed
   packages from the final source snapshot. Recheck the staged index and archive
   manifests immediately before publication.

Suggested small changesets are `Reject residual files in portable releases`,
`Enforce archive limits before verifier dispatch`, `Bound chunked HTTP reads`,
`Coordinate export reservations and workspace shutdown`, and `Correct operations
and release guidance`. Each should include the relevant regression or validation.

Further engineering work should be tracked separately from these confirmed bugs:

- Qualify saved Telegram update state against abrupt process termination and the
  cursor/observation commit boundary. Existing restart tests do not establish
  lossless replay under every failure.
- Run the declared OS/container matrix and a controlled multi-account live pilot;
  report observed gaps and sustained-operation measurements explicitly.
- Establish resource budgets for dossier generation, operator-supplied regular
  expressions and large restores. A thread alone is not a hard execution budget.
- Keep CPU-heavy hashing/verification and long SQLite scans from delaying the
  shared event loop; measure health latency while exporting production-size data.
- Expand secret scanning beyond the four recognized formats and review public
  screenshots before release. The current scanner's success is bounded evidence.
- Separate generic archive validation from format-specific verification and share
  export lifecycle machinery once the regressions are in place. Refactoring alone
  is not a substitute for the failure tests.

Existing qualifications and limitations remain in [Readiness](READINESS.md) and
[Live acceptance](LIVE_ACCEPTANCE.md). No new live-service, full-storage encryption,
source-authenticity or independent-custody claim is made by this audit.

## Relevant upstream behavior

Python documents that `ignore_errors` suppresses removal failures in
[`shutil.rmtree`](https://docs.python.org/3.12/library/shutil.html#shutil.rmtree).
[`StreamReader.readexactly`](https://docs.python.org/3.12/library/asyncio-stream.html#asyncio.StreamReader.readexactly)
requests the supplied byte count, so response budgets must be enforced before a
peer-controlled whole-chunk read. For export cleanup, review the exception and
cancellation behavior of
[`asyncio.gather`](https://docs.python.org/3.12/library/asyncio-task.html#asyncio.gather)
when choosing how to cancel and await all participants. The findings themselves
are grounded in the local code and synthetic reproductions above.
