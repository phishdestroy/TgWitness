# Pre-publication audit — 29 October 2026

This review covers publication boundaries, dependency advisories, repository documentation
and navigation usability. Tests use synthetic accounts and temporary storage. Real account
data and existing application processes were not used for acceptance testing. No commit,
push, GitHub release or website deployment was performed.

## Findings and corrections

| Finding | Correction and evidence |
| --- | --- |
| Pillow 12.3.0 was pinned and the package requirement excluded its security update. pip-audit reported 39 advisories against this version. | Require `pillow>=13,<14` and pin 13.0.0. Upstream lists the fixes in its [13.0.0 security notes](https://pillow.readthedocs.io/en/stable/releasenotes/13.0.0.html#security). The project already requires Python 3.11, which satisfies the new Pillow requirement. |
| The source packager accepted every JSON file beneath the application directory, including hypothetical account exports or vault metadata. | Allow only the 12 named locale dictionaries and the English fallback catalog. Exclude nested data, backup, cache and environment directories. Regression tests place synthetic private files inside otherwise public directories. |
| Wheel resource globs accepted every file in `static` and every JSON file in `locales`; implicit namespace discovery could include runtime directories. | Limit resource extensions, explicitly list locale files, disable implicit package data and namespace discovery. A clean staging build containing five synthetic secret canaries excluded all five while retaining the application resources. |
| Source ZIPs omitted `website/render_artwork.py`, although Git tracked it. Two documentation links referenced a missing historical review. | Include the artwork script, repair the links and check that local link targets are part of the public source list. |
| Release documentation described implemented features as unavailable, including encrypted exports and coordinated chat exports. | Rewrite the release page around the actual current source and its remaining qualification boundaries. |
| Message comparison regression cases constructed the same attachment twice with different wall-clock dates. Crossing a serialization boundary could create a false edit. | Use a fixed synthetic document date. Production comparison behavior is unchanged. |

The new `tools/check_publication.py --git-index` checks public files, local Markdown link
targets and common private-key/GitHub-token/Telegram-token/Telethon-session formats. It
reports paths and line numbers without printing matched values. It also rejects tracked
paths outside the public-source list. It does not scan historical Git blobs, compare staged
contents with the working tree, inspect text inside images or detect every possible secret.
The built-in public Telegram API pool is application identification, not an account session.

CI now runs the publication check, a strict audit of pinned runtime dependencies and quick
navigation acceptance. A vulnerability or incomplete dependency collection fails the audit
job; the release workflow depends on the checks workflow.

## Interface changes

The **Go to…** control opens a searchable section menu with Ctrl+K or Cmd+K. Arrow keys
select a destination, Enter opens it and Escape restores focus. The menu supports mouse
input, light/dark themes, narrow screens, Russian labels and right-to-left layouts. It closes
when the panel locks or the workspace changes, does not open over another modal, and performs
navigation only. The active sidebar page now has `aria-current="page"`.
On phones, a compact search icon uses the existing toolbar; account controls keep their
original vertical space. The separate sidebar search row is shown only on wider screens.

Browser acceptance verifies search, the empty state, keyboard focus, locking, Russian/Arabic
and widths of 320, 390 and 1440 pixels. New labels use explicit English fallbacks in the
remaining languages. README screenshots are generated from synthetic data.

## Validation record

Local environment: Windows 11, Python 3.12.10, Pillow 13.0.0. Final results:

| Check | Result |
| --- | --- |
| Full Python suite after dependency update | 316 passed, 3 skipped; 239.91 seconds |
| Focused publication, packaging, avatar and QR cases | 15 passed, 1 skipped; includes two additional secret-scanner parameter cases added after full-suite collection |
| Runtime dependency audit | 38 packages, zero known advisories, zero skipped packages; all 38 resolved runtime dependencies are pinned |
| General panel browser acceptance | Passed; no JavaScript errors or external requests |
| Account import, QR and mobile sign-in | Passed, including first-screen controls at 320/390/1440 pixels |
| Quick-navigation browser acceptance | Passed, including touch-sized controls, focus, locking, Russian and RTL |
| Panel actions and delayed workspace responses | Passed; synthetic send/reply/callback/join receipts verified; late journal, dossier, witness and export responses discarded after workspace changes or locking |
| Public website | Passed at 320/390/768/1024/1440 pixels; project subpath, keyboard, clipboard refusal, reduced motion and no-JavaScript fallback |
| Wheel with five private-file canaries | All excluded; required resources retained; final metadata requires Pillow 13 |
| Isolated installed wheel | Panel resources served; authentication enforced; 32 synthetic events exported and verified, including a streamed download |
| Publication check | 226 public files; 1,274 local Markdown link targets; no recognized secret matches or non-public tracked paths |
| Ruff, dependency consistency, workflow/Compose parsing | Passed |
| Startup prerequisites | Ready on an available loopback port; no Telegram connection |

The skipped cases require POSIX permissions or symlink creation unavailable on this host.
The focused cases overlap the full suite; their counts must not be added as distinct tests.
Warnings concern the existing Starlette/httpx test adapter and Apprise's deprecated imghdr
import. No new test failure remains in the completed runs above.

An intermediate mobile account check caught the extra search row pushing the file-import
button below the viewport. Compact toolbar controls fixed this; the repeated account check
passed. The initial full-suite run overlapped a locale-file edit and is superseded by the
completed final run. Dependency auditing was repeated with a fresh cache after a local
cache permission error.

Receipts are local ignored files under `test-results`: `dependency-audit-before.json`,
`dependency-audit.json`, `publication-pytest-final.log`, `publication-focused-final.log`,
`publication-browser.log`, `publication-final-check_account_browser.log`,
`publication-final-check_interactions_browser.log`, `publication-final-check_workspace_browser.log`,
`quick-navigation/receipt.json`, `publication-site.log`,
`publication-package-final/install-receipt.json` and `publication-readiness.json`.

## Remaining publication steps

The synthetic tests above are separate from the live test on a real account: one supergroup
from 27 to 29 October, 1,291 messages, 472 deletions and 12 edits, all 2,385 record
signatures verified. See the [live test](../VERIFICATION.md#live-telegram-test--27-to-29-october-2026).

This checkout has no initial commit, and its pre-existing Git index differs from the working
files. Include the reviewed new files and refreshed versions when preparing that first commit;
the pre-existing index alone is not the audited release. The audit does not change Git's global
ownership configuration or stage the user's changes.

Linux/macOS/Docker execution, hosted GitHub Actions, a complete live Telegram acceptance
matrix and sustained operation remain unverified by this local Windows run. See
[live acceptance](LIVE_ACCEPTANCE.md), [publishing](PUBLISHING.md) and
[the earlier backend review](FULL-REVIEW-2026-10-29.md).

## Follow-up: staged release contents, account deletion and access

This later pass reviewed the expanded 282-file public source set. The earlier numbers
above describe an earlier revision, not this final candidate. All new runtime probes used
temporary synthetic workspaces; existing Telegram accounts and running collectors were
not changed.

Three additional problems were reproduced and corrected:

- **The publication check accepted an incomplete or stale first commit.** The working
  source passed even though 146 public files were absent from the index and 72 staged
  versions differed. `--git-index` now requires the complete reviewed file set, compares
  actual object contents with Git's line-ending conversion, rejects unresolved merges
  and non-regular files, and scans staged text for recognized secrets. A regression stages
  a synthetic secret, cleans only the working file and sets `assume-unchanged`; the check
  still detects both the stale version and the secret without printing its value.
- **Account deletion could report success while leaving files behind.** Filesystem errors
  were suppressed and the account disappeared from the registry. Deletion now persists
  its intent before removing data, records failures and keeps the stopped workspace
  available for retry. Restart never reopens or repairs a partially erased vault. Only
  completed removal produces `profile.deleted`. The panel refreshes after failure, moves
  away from an unavailable selected account, and explains how to retry in English and
  Russian. Deletion through a linked workspace path is refused.
- **Invalid tokens could block valid access at the same client address.** Fifteen failed
  requests caused the server to return HTTP 429 even for correct panel and witness tokens.
  Valid capabilities now remain usable; invalid tokens remain throttled. Both authentication
  paths share bounded address accounting and return a retry interval for rejected requests.

Completed checks for this follow-up:

| Check | Result |
| --- | --- |
| Final full Python suite | **386 passed, 3 skipped**, no failures; 246.60 seconds |
| Focused publication, profile, witness and API regressions | 29 passed, including nine new cases |
| General panel browser acceptance | Passed with synthetic data |
| Account/import/QR browser acceptance | Passed; no page errors or external requests |
| Workspace browser regression | Passed: failed deletion, healthy-workspace selection, English/Russian error state and successful retry; no page errors |
| Public site and interactive documentation browser checks | Passed at 320–1440 px; no page errors, failed requests or external requests |
| Final wheel and isolated installation | Passed; packaged assets served and 32 signed events verified through ordinary and streamed exports |
| Runtime dependency audit | All 38 pins checked; no known advisories or skipped dependencies |
| Ruff, JavaScript syntax, dependency consistency and whitespace | Passed |
| Working-source publication scan | 282 public files and 1,426 local Markdown links; no recognized secret matches |
| Complete source in an isolated Git index | Passed the stricter staged-content check; the user's index was preserved |

The three skips cover POSIX permission checks and unavailable symlink creation on this
host. The two warnings come from the existing Starlette/httpx adapter and Apprise's
deprecated `imghdr` import. Focused tests are included in the full count.

The dependency check used [PyPA pip-audit](https://github.com/pypa/pip-audit) with strict
collection and a fresh cache. Its result covers known advisories, not all possible flaws.
The erasure failure follows the documented
[`shutil.rmtree` error behavior](https://docs.python.org/3/library/shutil.html#shutil.rmtree).

Receipts are ignored local files under `test-results`: `prepublish-pytest-final.log`, `prepublish-fixes-focused.log`,
`prepublish-current-browser.log`, `prepublish-accounts.log`, `prepublish-site-browser.log`,
`prepublish-docs-site.log`, `prepublish-workspaces-final.log`, `prepublish-installed-check.log`,
`prepublish-install-check/install-receipt.json`, `prepublish-dependency-audit.json`,
`prepublish-index-summary.json`, `prepublish-index-findings.log` and `prepublish-candidate.json`.

The existing Git index remains unchanged. It now correctly fails the stricter publication
check; stage the complete reviewed set before the first commit and rerun
`python tools/check_publication.py --git-index`. The source archive uses the reviewed
working files, independently of that old index. Linux/macOS, containers and hosted Actions
still require their own execution results. No additional live Telegram qualification is
claimed by this follow-up. The Windows portable distribution was not rebuilt in this pass.
