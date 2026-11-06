# Release readiness

Updated 5 November 2026 for the 0.9.1 preview source. This is an engineering
acceptance record, not independent certification. The maintained capability and
qualification matrix is [Current status](../STATUS.md).

## Source and release boundary

The [current installer](https://get.destroy.tools/) publishes verified main-branch builds
with their exact source revision in the signed manifest．The tagged
[0.9.0 preview](https://github.com/phishdestroy/TgWitness/releases/tag/v0.9.0) is a separate package．
The changelog，package version，README badge and qualification record identify the source
they describe；publication checks enforce source-version labels．

## Required acceptance for the candidate

- Run all required checks on the candidate revision, including Linux/Windows/macOS
  installation, browser suites, Docker/Compose and the Windows portable package.
  Keep failures and skips visible. A passing PR subset does not replace the full run.
- Run dependency, workflow and container-image audits. Identify the exact images
  scanned; CodeQL or a skipped container job does not clear an image vulnerability gate.
- Complete the [controlled live matrix](LIVE_ACCEPTANCE.md) with permitted test
  accounts: Standard/Takeout history, media, admin/member roles, approval waits,
  disconnects, authorization loss and interrupted resume.
- Qualify Trusted Live separately: official-client login, real native export,
  annotated hybrid comparison, route failure, logout/revocation and cleanup.
  CPU WARP tests do not attest a TEE or establish account safety.
- Measure sustained multi-account operation and recovery on the target hardware.
  Search benchmarks and journal inventories are not complete delivery measurements.
- Build source, wheel and portable artifacts from one tested revision, retain the
  exact file list/hashes and attestations, and verify installation plus backup restore.
  Preserve previously published tags and assets.
- Obtain independent review of integrity, attribution, scope and deployment trust
  claims before presenting the product as a stable forensic acquisition system.

## Known boundaries

Backfill observations, media jobs and cursors commit atomically. Live provider
update state is stored separately; lossless replay across every crash boundary is
not established. Full history and live observation are exclusive on one account.

Vault encryption protects credentials and keys. Journal, attachments and derived
search data require disk/volume encryption if confidentiality at rest is needed.
Evidence archives are not resumable workspace backups.

Local signatures establish integrity relative to a trusted key and retained checkpoints．
Sealed acquisition additionally binds the archive to the approved collector's execution
through GitHub provenance or verified TDX measurements；see
[verification scope](../EVIDENCE.md#verification-scope) for each mode's inputs．

Earlier security findings are preserved in the dated
[container analysis](CODE-SCANNING-2026-11-01.md#remaining-container-findings).
Their counts describe those earlier images, not a current scan. New deployment,
timestamp and qualification results are listed in [Verification](../VERIFICATION.md).
