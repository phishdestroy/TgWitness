![The investigation handbook — From your first capture to a verifiable handoff.](../assets/presentation/wiki-home.svg)

# TgWitness Wiki

[Project](../../README.md) · [Documentation](../README.md) · [Wiki](Home.md) · [Support](../../SUPPORT.md)


**From your first demo to a verifiable handoff.** Practical guides for observing
Telegram, reviewing captured changes and running your own workspace.

[Get started](Getting-Started.md) · [Find an answer](FAQ.md) · [Solve a problem](Troubleshooting.md) · [Technical reference](../README.md)

## Start here

1. [Try the demo and install](Getting-Started.md).
2. [Connect a dedicated account](Accounts.md).
3. [Choose sources and start observation](Collection.md).
4. [Export a record and verify it](Exports-and-Verification.md).

**First successful check:** a new message from a chat you control appears in the journal; its edit becomes another version; its deletion notice leaves the captured content available. Check the signed export too. This checks that particular sequence, not every possible Telegram event.

## Choose a guide

| Set up your workspace | Work with the record |
| --- | --- |
| [Accounts](Accounts.md) — phone, QR and session imports | [Collection](Collection.md) — chats, folders and capture policy |
| [Proxies](Proxies.md) — choose a connection route | [Investigations](Investigations.md) — follow a case across chats |
| [Server and Docker](Server-and-Docker.md) — leave a collector running | [Exports and verification](Exports-and-Verification.md) — prepare a signed handoff |
| [Backup and recovery](Backup-and-Recovery.md) — protect your workspace | [Witness and Proof](Witness-and-Proof.md) — independent checkpoints and public status |

![Observe, preserve and verify.](../assets/presentation/workflow.svg)

Need a term explained? Open the [glossary](Glossary.md).


![Section divider](../assets/presentation/divider.svg)

## Read this before connecting

Use a dedicated account you can afford to lose. A Telegram session grants access to that account; keep sessions, panel tokens and keys private. Local message content and attachments need disk encryption if you require protection at rest.

A signature establishes integrity relative to a trusted key. It does not prove that Telegram created a message, that collection was complete, or that an operator could not fabricate a journal.

## Project and help

[Project overview](../../README.md) · [Technical documentation](../README.md) · [Verification record](../VERIFICATION.md) · [Get help](../../SUPPORT.md) · [Contribute](../../CONTRIBUTING.md) · [Report a vulnerability](../../SECURITY.md)

UI labels in this wiki follow the English interface. Labels may differ between releases.
