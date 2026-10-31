<picture>
  <source media="(max-width: 640px) and (prefers-reduced-motion: reduce)" srcset="assets/presentation/casework-handbook-mobile-static.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/presentation/casework-handbook-static.svg">
  <source media="(max-width: 640px)" srcset="assets/presentation/casework-handbook-mobile.svg">
  <img src="assets/presentation/casework-handbook.svg" width="1440" alt="TgWitness handbook: capture a message, preserve its changes and verify the record.">
</picture>

# TgWitness documentation

Install the application, capture your first message, and learn how to verify an
export. Task guides cover everyday use; the references explain formats and limits.

[Project](../README.md) · [Handbook](wiki/Home.md) · [Русский](ru/START-HERE.md) · [FAQ](wiki/FAQ.md)

## First capture

1. [Run the demo](QUICKSTART.md#explore-the-interface) with fictional conversations. No Telegram account is needed.
2. [Connect a dedicated account](ACCOUNTS.md) and select a chat you control.
3. [Start observation](wiki/Getting-Started.md), send a test message, then edit and delete it. Wait for each event to appear before continuing.
4. [Export and verify](wiki/Exports-and-Verification.md). Keep the signing-key fingerprint and a checkpoint separately.

The saved message, its edit and the deletion notice should remain in the journal.
This checks that sequence; it does not establish complete Telegram capture.

## Collection and investigation

| Task | Guide |
| --- | --- |
| Install locally or run with Docker | [Quick start](QUICKSTART.md) · [Deployment](DEPLOYMENT.md) |
| Add accounts or import a session | [Accounts](ACCOUNTS.md) |
| Choose chats, event types and attachment limits | [Collection](COLLECTION.md) |
| Configure proxies and fallback behavior | [Connection routes](CONNECTION-SECURITY.md) |
| Trace people, messages and files across chats | [Investigation walkthrough](INVESTIGATION.md) |
| Save a conversation for offline reading | [Chat export](wiki/Chat-Export.md) |
| Capture one chat from a personal fork | [GitHub Actions capture — preview](SEALED-ACTIONS.md) |
| Give a reviewer access to selected material | [Access and permissions](ACCESS.md) |

## Analysis and integrations

| Task | Guide |
| --- | --- |
| Search the archive and prepare an analyst report | [Archive analysis](ANALYSIS.md) |
| Connect a client with read-only archive access | [MCP](MCP.md) |
| Recognize text or transcribe saved attachments | [Local media processing](MEDIA-ANALYSIS.md) |
| Deliver structured events to another service | [Signed webhooks](WEBHOOKS.md) |
| Receive alerts and daily summaries | [Notifications](wiki/Notifications.md) |

## Verification and maintenance

| Task | Guide |
| --- | --- |
| Understand signatures, coverage and trust | [How it works](HOW-IT-WORKS.md) · [Evidence format](EVIDENCE.md) |
| Retain independent checks | [Witness](WITNESS.md) · [External timestamps](TIMESTAMP.md) |
| Protect the host and stored data | [Security model](SECURITY-MODEL.md) · [Hardened deployment](HIGH-ASSURANCE.md) |
| Keep an encrypted remote copy | [Off-site storage](wiki/Off-site-Copy.md) |
| Back up and restore the service | [Backup and recovery](wiki/Backup-and-Recovery.md) |
| Diagnose a problem | [Troubleshooting](wiki/Troubleshooting.md) · [Operations](OPERATIONS.md) |

[Verification record](VERIFICATION.md) documents completed checks and remaining
qualification work. [Known limits](internal/READINESS.md) records release readiness.

## Technical reference

[Architecture](ARCHITECTURE.md) · [Project guide](PROJECT-GUIDE.md) ·
[Changelog](CHANGELOG.md) · [Glossary](wiki/Glossary.md)

For contributors: [development setup](../.github/CONTRIBUTING.md),
[repository map](../README.md#repository-map), [wiki maintenance](internal/WIKI.md)
and [website publishing](internal/PUBLISHING.md#preview-the-website-locally).

TgWitness is distributed under the [MIT License](../LICENSE).
The [author statement](ETHICAL-NOTICE.md) adds no licence condition.
