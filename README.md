<a href="docs/assets/presentation/investigation.mp4"><picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/tgwitness-investigation-static.svg">
  <img src="docs/assets/presentation/investigation.gif" width="1200" alt="TgWitness — Follow the trail. Preserve the evidence. Channels, groups, bots and private chats connected into one case. Fictional records.">
</picture></a>

<h1 align="center">TgWitness</h1>

<p align="center"><b>The Telegram investigation workspace that keeps the record.</b><br>
Capture conversations · keep every edit and deletion you saw · trace connections · hand over evidence anyone can verify</p>

<p align="center">
  <a href="#quick-start"><img src="docs/assets/presentation/button-start.svg" alt="Quick start" height="40"></a>
  <a href="https://github.com/phishdestroy/TgWitness/wiki"><img src="docs/assets/presentation/button-wiki.svg" alt="GitHub Wiki" height="40"></a>
  <a href="docs/README.md"><img src="docs/assets/presentation/button-docs.svg" alt="Technical documentation" height="40"></a>
  <a href="#repository-map"><img src="docs/assets/presentation/button-source.svg" alt="Repository map" height="40"></a>
</p>

<p align="center"><a href="docs/CHANGELOG.md">0.6.1 · pre-release</a> &nbsp;/&nbsp; Python 3.11+ &nbsp;/&nbsp; <a href="LICENSE">MIT</a> &nbsp;/&nbsp; Self-hosted &nbsp;/&nbsp; No telemetry &nbsp;/&nbsp; 13 languages</p>

![Section divider](docs/assets/presentation/divider.svg)

## Messages change. Keep what you saw.

<a href="docs/assets/presentation/message-history.mp4"><picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/message-history-static.png">
  <img src="docs/assets/presentation/message-history.gif" width="1200" alt="A message reads 14:00, is edited to 16:30 and is deleted; the journal keeps both versions and the deletion notice. Fictional records.">
</picture></a>

| Keep the record | Follow the case |
| --- | --- |
| **Every version stays.** Edits are saved as separate versions; a deletion notice never erases what was already captured. | **Work across chats.** Search saved conversations, build cited timelines, review people and shared files. |
| **Your scope, your accounts.** Selected chats, a folder or a dedicated account, each with its own journal and keys. | **A handoff that proves itself.** Signed records, preserved attachments, coverage gaps and a standalone verifier. |

## The workspace

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/chats-dark.png">
  <img src="docs/assets/chats.png" width="1200" alt="The TgWitness Chats workspace: conversations, observed edits and deletion notices. Fictional demo data.">
</picture>

<details>
<summary><b>More screens:</b> message history, capture policy, exports, journal</summary>

| Compare captured versions | Choose what to observe |
| --- | --- |
| [![Message history](docs/assets/detail.png)](docs/assets/detail.png) | [![Capture policy](docs/assets/sources.png)](docs/assets/sources.png) |
| **Prepare a signed handoff** | **Review the journal** |
| [![Export options](docs/assets/exports.png)](docs/assets/exports.png) | [![Observation journal](docs/assets/workspace-dark.png)](docs/assets/workspace-dark.png) |

</details>

## Quick start

**Try the demo first:** fictional conversations, no Telegram account needed.

| Windows | Linux / macOS |
| --- | --- |
| Double-click **`scripts\Demo.cmd`** | Run **`sh start.sh --demo`** |

Then open **http://127.0.0.1:8787**. The launcher prepares Python 3.11+ dependencies itself.

**Your own workspace:** run `Start.cmd` or `sh start.sh` and follow
[account setup](https://github.com/phishdestroy/TgWitness/wiki/Accounts). The panel token is in
`data/live/panel-token.txt`. Use a dedicated Telegram account you can afford to lose.

[Installation and Docker →](docs/QUICKSTART.md) &nbsp;·&nbsp; [Tested environments →](docs/VERIFICATION.md)

## How it works

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/evidence-chain-static.svg">
  <img src="docs/assets/presentation/evidence-chain-animated.svg" width="1200" alt="Each captured event links to the previous hash and is signed. A recipient checks the export against a trusted key.">
</picture>

Each record is chained with SHA-256 and signed with Ed25519. Anyone can verify an export
against a fingerprint kept outside the collector. It proves integrity relative to that key,
not Telegram origin or the truth of the content.

[The evidence model →](docs/HOW-IT-WORKS.md) &nbsp;·&nbsp; [Export and verify →](https://github.com/phishdestroy/TgWitness/wiki/Exports-and-Verification) &nbsp;·&nbsp; [Witness and Proof →](https://github.com/phishdestroy/TgWitness/wiki/Witness-and-Proof) &nbsp;·&nbsp; [All animations →](docs/SHOWCASE.md)

![Section divider](docs/assets/presentation/divider.svg)

## The investigation handbook

| Get started | Work a case | Keep it running |
| --- | --- | --- |
| [Install and try the demo](https://github.com/phishdestroy/TgWitness/wiki/Getting-Started) | [Choose sources](https://github.com/phishdestroy/TgWitness/wiki/Collection) | [Server and Docker](https://github.com/phishdestroy/TgWitness/wiki/Server-and-Docker) |
| [Connect an account](https://github.com/phishdestroy/TgWitness/wiki/Accounts) | [Investigate across chats](https://github.com/phishdestroy/TgWitness/wiki/Investigations) | [Backup and recovery](https://github.com/phishdestroy/TgWitness/wiki/Backup-and-Recovery) |
| [Configure a proxy](https://github.com/phishdestroy/TgWitness/wiki/Proxies) | [Prepare a handoff](https://github.com/phishdestroy/TgWitness/wiki/Exports-and-Verification) | [Troubleshooting](https://github.com/phishdestroy/TgWitness/wiki/Troubleshooting) |

[All Wiki pages](https://github.com/phishdestroy/TgWitness/wiki) · [Offline handbook](docs/wiki/Home.md) · [Complete project guide](docs/PROJECT-GUIDE.md) · [Technical reference](docs/README.md)

## Repository map

<details>
<summary>Source, deployment, tests and documentation</summary>

| Directory | Contents |
| --- | --- |
| [`tgwitness/`](tgwitness/README.md) | Application, collector, journal, verifier and web panel |
| [`docs/`](docs/README.md) | Guides, Wiki source, screenshots and verification record |
| [`deploy/`](deploy/README.md) | Optional Compose configurations and service templates |
| [`scripts/`](scripts/README.md) | Additional launchers: demo, setup only and Docker |
| [`tests/`](tests/README.md) | Synthetic regression tests |
| [`tools/`](tools/README.md) | Builds, checks, packaging and documentation tooling |
| [`website/`](website/README.md) | Documentation website and translations |
| [`.github/`](.github/AUTOMATION.md) | Workflows, issue forms and contribution guides |

</details>

<details>
<summary>Read the project overview in your language</summary>

**English** · [Русский](docs/ru/README.md) · [Українська](docs/uk/README.md) · [Español](docs/es/README.md) · [Português (Brasil)](docs/pt/README.md) · [Türkçe](docs/tr/README.md) · [العربية](docs/ar/README.md) · [فارسی](docs/fa/README.md) · [اردو](docs/ur/README.md) · [हिन्दी](docs/hi/README.md) · [Bahasa Indonesia](docs/id/README.md) · [Tiếng Việt](docs/vi/README.md) · [简体中文](docs/zh/README.md)

</details>

<sub>Pre-release. See the [verification record](docs/VERIFICATION.md) and the [audit findings and their fixes](docs/internal/RECHECK-2026-10-29.md) for tested behavior and remaining work. All screens and films use fictional data.</sub>

<p align="center"><a href=".github/SUPPORT.md">Get help</a> · <a href=".github/CONTRIBUTING.md">Contribute</a> · <a href=".github/SECURITY.md">Report a vulnerability</a> · <a href="LICENSE">MIT license</a> · Built by <a href="https://github.com/phishdestroy">PhishDestroy</a></p>
