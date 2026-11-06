# Current capabilities and test results

Source version: **0.9.1 preview**．Integration review：6 November 2026．

The version label identifies the publication channel．Capabilities and their test results
are listed below so a deployment can be assessed against its intended workload and settings．

The [current installer](https://get.destroy.tools/) publishes verified builds from
<code>main</code> with the exact source revision in its signed manifest．GitHub's tagged
[0.9.0 preview](https://github.com/phishdestroy/TgWitness/releases/tag/v0.9.0) remains
available separately．Use the installer manifest or release tag to identify the version installed．

## Capability record

| Workflow | Implemented in this source | Recorded validation | Remaining qualification |
| --- | --- | --- | --- |
| Live observation | Delivered messages, versions, deletion notices, media, rechecks, explicit gaps | Earlier real-account tests and a multi-workspace inventory in [Verification](VERIFICATION.md) | Complete role/failure matrix and atomic lossless live update replay |
| Full history | Standard/Takeout, signed resumable cursors, shared cooldown, concurrent media, Recent Actions and saved-version comparison | Synthetic failure tests and browser acceptance in [Backfill](BACKFILL.md) | Controlled real-account Standard/Takeout, approval, admin rights, long waits and throughput |
| Account/chat exports | Separate archives, selection, resumable account export and explicit multi-account chat export | Automated acquisition, file-integrity, recovery and browser checks | New revisions require their own live acceptance; results from pending branches do not qualify main |
| Evidence and handover | Journal signatures，file manifests，retained checkpoints，standalone verification，reports and minimized copies | Signature／tampering tests，verified live journal and report checks | Choose the [verification mode](EVIDENCE.md#verification-scope) and retain its required inputs |
| Search and investigation | Full-text preview, Case Board, source-linked notes, reports and optional analysis | Browser checks and [one-million-message synthetic search benchmark](SEARCH.md#benchmark) | Sustained combined ingestion, search, media and export load on intended hardware |
| Independent witness | Separate keys, signed heads, freshness challenges and offline receipts | Synthetic rollback/fork/freshness checks and retained witness observations | Independent operator custody and prolonged failure/availability qualification |
| Trusted Live | Official Desktop/Web, guarded video, native JSON, continuity view and optional provider observations | Linux container checks; [CPU Ubuntu and WARP integration](VERIFICATION.md#trusted-live-cpu-ubuntu-and-warp--5-november-2026) | Real account login/export/hybrid/logout, native attachment preservation, local drand BLS verification and attested Trusted Live image |
| Phala high assurance | TDX verification, measured source/deployment and provider checks | [Real Phala deployments and external timestamp verification](VERIFICATION.md#live-phala-cloud-deployment--4-november-2026) | Telegram collection on the qualified CVM and additional OS/deployment combinations |

Full-history acquisition and live observation use the account in turn：pause observation
to load history，then resume it．The [collection-method comparison](COLLECTION-MODES.md)
describes each workflow's scope，output and recovery behavior．

## Checks and release decisions

The merged search and export integration passed
[127 hosted panel checks](https://github.com/phishdestroy/TgWitness/actions/runs/42151012349)．
The combined export，search and gap-analysis tree then passed 352 local regression tests，
eight website checks and MCP transport checks on 6 November 2026．The earlier preview
readiness and report-metadata failures were fixed and covered by regression checks．
The [Actions results](https://github.com/phishdestroy/TgWitness/actions) record checks
for each subsequent commit．

CodeQL, dependency advisory checks and container image scans are separate gates.
A skipped image scan is not a passing image scan. Earlier findings remain in their
dated audit reports; they must not be presented as measurements of an unscanned
current image.

Before publishing a stable release, run the complete platform/security checks and
[controlled live acceptance](internal/LIVE_ACCEPTANCE.md), build all artifacts from
the tested revision, verify their hashes/provenance and record every limitation.
See [release readiness](internal/READINESS.md) for the acceptance checklist.
