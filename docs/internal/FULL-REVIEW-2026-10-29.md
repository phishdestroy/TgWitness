# Whole-tool review — 29 October 2026

Follow-up to [the initial review](REVIEW-2026-10-29.md). This pass examines the whole
application rather than just the mini-client: workspace/authentication boundaries,
intake and durable media jobs, exports, dossiers, off-site copies, recovery, browser
state, launch/install paths, and public packaging. Tests use isolated synthetic
accounts and local storage/HTTP transports. Existing real application processes and
account data were not changed.

## Newly confirmed problems and fixes

| Area | Reproduction / previous behavior | Implemented correction |
| --- | --- | --- |
| Attachment completeness | A descriptor advertised four bytes; a successful transport returned zero, three or five bytes. Each was recorded as `media.saved`. | Compare the actual file length with the signed original descriptor before publishing it. A mismatch is a failed capture, never a preserved attachment. |
| Backup destination | After copying to one endpoint/prefix, switching destinations reused the old journal/media cursor and omitted the beginning of the journal. Bucket identity was also absent from progress state. | Destination-specific SQLite progress, including endpoint, region, bucket, prefix, addressing mode and encryption-key identity. Each new destination receives the complete locally retained journal and media. |
| Backup source integrity | A missing media file advanced the copy cursor without an error; a corrupt local file was encrypted and copied under the original file's identity. | Stop on missing files and validate plaintext against the signed media hash before upload. Do not advance that media cursor until its copy succeeds. A repaired local file is retried on the next pass. |
| Restore completeness | A correctly signed journal and checkpoint verified even when a referenced preserved attachment was absent or replaced. | Check every `media.saved` reference against decrypted content hashes and recorded sizes before publishing restored files. Report the number of unique media files verified. |
| Interrupted copy replay | A successful upload followed by interruption before cursor persistence can leave overlapping segments. A later complete retry was rejected as a discontinuity. | Accept overlapping records only when every field agrees, assemble one ordered journal, then verify the chain and signatures. Conflicting overlaps still fail. |
| Copy while observation continues | A new checkpoint created during attachment upload could cover records that the copy had not uploaded yet, making the otherwise completed copy fail restoration. | Defer checkpoints and timestamp files beyond the copied journal boundary to the next pass. Both the current and following completed passes restore successfully. |
| Dossier removal | Disabling a dossier during a pending build removed the old cache, but the worker recreated it afterwards. | Bind cache writes to the enabled generation and serialize the final check/write with disable/removal. The stale build cannot recreate the deleted file. |
| Browser workspace boundaries | A held record response from workspace A was rendered with workspace B's chat heading. Related unguarded continuations included dossiers, witness tokens and export dialogs. | Reject stale API/JSON responses across workspace revisions and locking; bind chat/export context; block interaction while a workspace loads its settings. A failed workspace load returns to the access gate. Cancelled file picking no longer marks a chat export as downloaded. |
| Export cancellation | Cancelling `asyncio.to_thread` only cancelled the awaiter. Cleanup could remove a ZIP worker's input while that worker kept running or wrote a file after cancellation. | Wait for the file worker to exit before cleanup in single-account ZIP building and multi-account merge/build operations. Cancellation remains recorded as interrupted and does not publish an archive. |

The new backend cases live in `tests/test_full_review.py`. Delayed-response browser
coverage lives in `tools/check_workspace_browser.py` and is included in CI. Previous
mini-client regressions remain in the suite. Existing signed events are never rewritten.
No Russian translations were added; the mini-client controls remain English.

## Coverage

| Subsystem | Verification |
| --- | --- |
| Authorization and imports | Token requirements, bounded request bodies, credential redaction, session/TData/JSON/Auth Key conversion, phone/QR/2FA, rejected and superseded clients, profile/account ownership |
| Collection | Scope, own-action policy, live messages/edits/deletions/reactions, reconnect/catch-up/recheck, intake, original media descriptors, durable queue recovery and storage-pressure handling |
| Journal and derivatives | Append-only transactions, signatures and chain verification, checkpoints, ZIP/JSONL/CSV/HTML, formula-safe CSV and escaped HTML, profile facts and references |
| Long-running work | Full chat and multi-account exports, range integrity, FloodWait handling, cancellation, observation continuing during export |
| Backup and recovery | Encryption/authentication, path boundaries, checkpoints, segment continuity/replay, destination isolation, missing/corrupt media, Object Lock deadlines |
| Browser | Account switching/locking with delayed responses, send/reply/callback/join, access/import flows, settings, downloads, notifications and witness setup, themes and narrow layouts |
| Distribution | Dependency consistency, wheel resources, isolated installed HTTP/export checks, startup diagnostics, public source/site boundaries |

The public-site builder correctly refused an obsolete `assets/tgwatch-social.png` in
the existing generated output. The old directory was preserved under
`test-results/full-tool-site-before`; a fresh build uses the current explicit asset list.
The refusal prevents unexpected files from silently entering a public artifact.

## Operational notes

- Existing unscoped replica progress is retained but is not trusted as proof of delivery
  to a particular destination. The first sync after upgrading recopies locally retained
  journal/media/checkpoints once. Identical overlapping journal segments restore safely.
- Changing storage does not migrate historical chat-export archives that were already
  removed from the local outbox after their earlier successful upload. Keep the old
  destination/key if those archives are needed.
- Cancellation during file packaging waits for the active file worker to finish before
  deleting temporary input/output. This prevents background writes after cleanup.
- Live Telegram delivery, real proxy/storage/timestamp services and notification delivery
  to external recipients are outside these synthetic checks. No real messages, joins or
  bot actions were sent. Docker/Podman were unavailable locally; Linux/macOS execution
  and container builds are not claimed by this Windows run.

## Evidence locations

- `test-results/full-audit-before.log`: new backend failure reproductions before fixes.
- `test-results/full-audit-browser-before.log`: the old cross-workspace record rendering.
- `test-results/full-audit-recovery.log`: focused recovery checks after fixes.
- `test-results/full-tool-pytest.log`: complete final Python run.
- `test-results/full-tool-browser-final.log`, `full-tool-accounts.log`, `full-tool-interactions.log`:
  application browser acceptance.
- `test-results/full-tool-workspaces.log`: delayed-response workspace acceptance.
- `test-results/full-tool-package/`: wheel and installed-package verification artifacts.

## Final verification

| Check | Final result |
| --- | --- |
| Full Python suite | **313 passed, 3 skipped**, no failures; 359.73 seconds |
| Final focused suite after the checkpoint-boundary correction and fallback update | **41 passed**, including the new concurrent-copy checkpoint case; `full-tool-final-regressions.log` |
| General browser acceptance | Passed: views, settings, evidence, accounts, downloads, dictionaries, RTL, themes and responsive layouts |
| Account/import browser acceptance | Passed; no browser errors or external requests |
| Mini-client browser acceptance | Passed; send/reply/callback/join and failure/race cases; 23 signed events verified |
| Workspace browser acceptance | Passed: late records after switch/lock, dossier cache isolation, witness token isolation and export-dialog context |
| Public site | Fresh 11-file build passed browser checks at 1440/390/320 px; no external requests, JS errors or failed requests |
| Final wheel and isolated installation | Passed; all served resources and locale catalog present, 32-event signed/streamed exports verified |
| Startup prerequisites | Ready on a free loopback port; signatures, storage and dependencies available |
| Ruff, JavaScript syntax, dependency consistency | Passed |
| Local capacity probe | 1,000 events / 100 chats; all 1,000 verified in export; 169.3 events/s, p95 handler time 10.169 ms on this run |

The focused run overlaps the full suite; its count must not be added to 313 as if every
case were distinct. It covers the last checkpoint-boundary fix added after full-suite
collection, plus recovery and locale regressions. Together the runs exercised all 317
collected cases in the final tree: 314 passed and 3 skipped.

The first workspace-harness run exceeded its 15-second startup deadline while several
disk-intensive probes ran concurrently. The final isolated run passed. An interrupted
5,000-event benchmark is not used in the capacity result above; the completed 1,000-event
run is in `test-results/full-tool-capacity-final.log`. This measures local serial synthetic
capture, not live Telegram delivery, concurrent network capture or media throughput.

The installed-package receipt is `test-results/full-tool-package/checks/install-receipt.json`.
Final site results are in `test-results/full-tool-site.log`. Earlier failed reproduction and
harness logs remain available; the results in this table are the completed checks.
