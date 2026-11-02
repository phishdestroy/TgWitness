<a name="tgwitness-documentation"></a>

# TgWitness docs

[Install](INSTALLATION.md), connect an account and choose what to save.
To try the interface first, [open the demo](https://phishdestroy.github.io/TgWitness/demo/).
It uses fictional chats and needs no Telegram login.

[Project](../README.md) · [Русский](ru/START-HERE.md) ·
[Wiki](wiki/Home.md) · [FAQ](wiki/FAQ.md)

## Start here

1. [Install and open the panel](INSTALLATION.md).
2. [Connect a dedicated Telegram account](ACCOUNTS.md).
3. [Choose chats and start collecting](COLLECTION.md).
4. [Export and verify the result](TRUST.md).

<a name="find-your-workflow"></a>

## Guides

| Task | Guide |
| --- | --- |
| Export chats or an account | [Chat export](wiki/Chat-Export.md) · [Account export](ACCOUNT-EXPORT.md) |
| Export one chat through GitHub | [GitHub Actions capture (preview)](SEALED-ACTIONS.md) |
| Load older messages | [History](HISTORY.md) |
| Search across chats | [Investigation](INVESTIGATION.md) · [Search and AI](ANALYSIS.md) |
| Keep notes and prepare reports | [Case Board](CASE-BOARD.md) · [Reports](CASE_REPORTS.md) |
| Share selected records | [Sharing copies](ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient) · [Access](ACCESS.md) |
| Manage accounts and settings | [Accounts and groups](ACCOUNTS.md#bulk-import-and-account-groups) · [Settings](SETTINGS.md) |
| Use a proxy | [Connection settings](CONNECTION-SECURITY.md) |
| Read images and audio | [OCR and transcription](MEDIA-ANALYSIS.md) |
| Connect other tools | [MCP](MCP.md) · [Webhooks](WEBHOOKS.md) |
| Keep independent checkpoints | [Witness bot](WITNESS.md) · [Timestamps](TIMESTAMP.md) |
| Run on a server | [Deployment](DEPLOYMENT.md) · [Provider checks](HIGH-ASSURANCE.md) |
| Back up or recover data | [Storage](STORAGE.md) · [Recovery](wiki/Backup-and-Recovery.md) |
| Fix a problem | [Troubleshooting](wiki/Troubleshooting.md) · [Operations](OPERATIONS.md) |

## Limits and technical reference

TgWitness saves what the connected account can see. It cannot recover unseen
messages or read Secret Chats. Signatures help check saved records against a
trusted key; they do not prove Telegram origin or complete history.

[How it works](HOW-IT-WORKS.md) · [Evidence format](EVIDENCE.md) ·
[Security model](SECURITY-MODEL.md) · [Tests and known limits](VERIFICATION.md) ·
[Glossary](wiki/Glossary.md)

<a name="browse-the-source"></a>

## Development

[Source map](../README.md#repository-map) · [Architecture](ARCHITECTURE.md) ·
[Contributing](../.github/CONTRIBUTING.md) · [Build the website](../website/README.md) ·
[Release notes](CHANGELOG.md)

[MIT License](../LICENSE) · [Author statement](ETHICAL-NOTICE.md) ·
[Project notice](TAYLOR-WESSING-EXCLUSION.md)
