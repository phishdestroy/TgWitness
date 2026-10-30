<picture>
  <source media="(max-width: 640px) and (prefers-reduced-motion: reduce)" srcset="../assets/presentation/repository-cover-mobile.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="../assets/presentation/repository-cover-static.svg">
  <source media="(max-width: 640px)" srcset="../assets/presentation/repository-cover-mobile.webp">
  <img src="../assets/presentation/repository-cover.webp" width="1200" alt="TgWitness — your Telegram observation workspace. Capture, investigate and verify.">
</picture>

# TgWitness Wiki

[Project](../../README.md) · [Documentation](../README.md) · [Wiki](Home.md) · [Support](../../.github/SUPPORT.md)


**From your first demo to a verifiable handoff.** Practical guides for observing
Telegram, reviewing captured changes and running your own workspace.

[Try the demo](https://phishdestroy.github.io/TgWitness/demo/) · [Setup guide](Getting-Started.md) · [Modes & evidence](https://phishdestroy.github.io/TgWitness/guides/modes.html) · [Find an answer](FAQ.md)

## Choose a guide

| Set up your workspace | Work with the record |
| --- | --- |
| [Accounts](Accounts.md) — phone, QR and session imports | [Collection](Collection.md) — chats, folders and capture policy |
| [Proxies](Proxies.md) — choose a connection route | [Investigations](Investigations.md) — follow a case across chats |
| [Server and Docker](Server-and-Docker.md) — leave a collector running | [Exports and verification](Exports-and-Verification.md) — prepare a signed handoff |
| [Backup and recovery](Backup-and-Recovery.md) — protect your workspace | [Witness and Proof](Witness-and-Proof.md) — independent checkpoints and public status |

![Observe, preserve and verify.](../assets/presentation/workflow.svg)

Need a term explained? Open the [glossary](Glossary.md).

[S3 off-site copy and recovery](https://phishdestroy.github.io/TgWitness/docs/exports/#s3) · [Troubleshooting](Troubleshooting.md) · [Technical reference](../README.md)


![Section divider](../assets/presentation/divider.svg)

## Read this before connecting

> **NOTICE — Operator Incompatibility**
> [Read the complete project notice](Operator-Incompatibility.md): our
> statement on Taylor Wessing PartG mbB — German core, Hamburg office.

TgWitness is [MIT-licensed](../../LICENSE). Our
[position on Taylor Wessing](../TAYLOR-WESSING-EXCLUSION.md) is a statement, not a licence condition.

Use a dedicated account you can afford to lose. A Telegram session grants access to that account; keep sessions, panel tokens and keys private. Local message content and attachments need disk encryption if you require protection at rest.

A signature establishes integrity relative to a trusted key. It does not prove that Telegram created a message, that collection was complete, or that an operator could not fabricate a journal.

## Project and help

[Project overview](../../README.md) · [Complete project guide](../PROJECT-GUIDE.md) · [Technical documentation](../README.md) · [Verification record](../VERIFICATION.md) · [Get help](../../.github/SUPPORT.md) · [Contribute](../../.github/CONTRIBUTING.md) · [Report a vulnerability](../../.github/SECURITY.md)

UI labels in this wiki follow the English interface. Labels may differ between releases.
