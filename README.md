<picture>
  <source media="(max-width: 640px) and (prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/casework-hero-mobile-static.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/casework-hero-static.svg">
  <source media="(max-width: 640px)" srcset="docs/assets/presentation/casework-hero-mobile.svg">
  <img src="docs/assets/presentation/casework-hero.svg" width="1440" alt="TgWitness — Follow the trail. Preserve the evidence. A captured message, its saved edit and a retained record.">
</picture>

<p align="center">
  <a href="https://phishdestroy.github.io/TgWitness/demo/"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-demo-mobile.svg"><img src="docs/assets/presentation/readme-nav-demo.svg" width="32%" alt="Explore the interactive demo"></picture></a>
  <a href="#quick-start"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-download-mobile.svg"><img src="docs/assets/presentation/readme-nav-download.svg" width="32%" alt="Download and start TgWitness"></picture></a>
  <a href="https://github.com/phishdestroy/TgWitness/wiki"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-handbook-mobile.svg"><img src="docs/assets/presentation/readme-nav-handbook.svg" width="32%" alt="Read the investigation handbook"></picture></a>
</p>

<p align="center"><strong>Save Telegram chats, edits and deletion notices.</strong><br>Search them, compare versions and export a signed archive.<br>Runs on your computer or server.</p>

<p align="center">
  <a href="docs/CHANGELOG.md"><img src="docs/assets/presentation/identity-meta-version.svg" width="144" height="30" alt="v0.8.0 · pre-release"></a>
  <a href="docs/VERIFICATION.md"><img src="docs/assets/presentation/identity-meta-verification.svg" width="158" height="30" alt="Tested environments"></a>
  <img src="docs/assets/presentation/identity-meta-languages.svg" width="279" height="30" alt="25 interface languages · 26 guide languages">
  <a href="LICENSE"><img src="docs/assets/presentation/identity-meta-license.svg" width="60" height="30" alt="MIT"></a>
</p>

<a name="quick-start"></a>
<a name="run-it-on-your-machine"></a>

## Install

Python included. Use the same commands to update.

**Linux / macOS**

```sh
curl -fsSL https://get.destroy.tools/install.sh | bash
```

**Windows · PowerShell or CMD**

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

<sub>Ubuntu server: run as root. Desktop: run as your normal user.</sub>

[Setup & panel access](docs/INSTALLATION.md) ·
[Signatures & SHA-256](https://get.destroy.tools/#verification) ·
[Update](docs/INSTALLATION.md#update-an-existing-installation) ·
[ZIP downloads](https://github.com/phishdestroy/TgWitness/releases)

<a name="screenshots"></a>

<a href="https://phishdestroy.github.io/TgWitness/demo/">
<picture>
  <source media="(max-width: 640px) and (prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="docs/assets/presentation/readme-workspace-mobile-dark-still.webp">
  <source media="(max-width: 640px) and (prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-workspace-mobile-light-still.webp">
  <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="docs/assets/presentation/readme-workspace-dark-still.webp">
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-workspace-light-still.webp">
  <source media="(max-width: 640px) and (prefers-color-scheme: dark)" srcset="docs/assets/presentation/readme-workspace-mobile-dark.webp">
  <source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-workspace-mobile-light.webp">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/presentation/readme-workspace-dark.webp">
  <img src="docs/assets/presentation/readme-workspace-light.webp" width="1440" alt="The TgWitness demo in motion: captured messages, saved versions and content retained after deletion. Fictional demonstration records.">
</picture>
</a>

<p align="center"><sub>Click to try the demo. It uses fictional chats; no Telegram login needed.</sub></p>

<p align="center"><picture><source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-divider-static.svg"><img src="docs/assets/presentation/readme-divider.svg" width="1200" height="28" alt=""></picture></p>

<a name="from-a-conversation-to-a-case"></a>

## Save chats and changes

<picture>
  <source media="(max-width: 640px) and (prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-features-mobile-static.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-features-static.svg">
  <source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-features-mobile.svg">
  <img src="docs/assets/presentation/readme-features.svg" width="1200" alt="Three animated workflows: export a chat to HTML and JSON, find a shared link across recorded chats, and retain captured versions after a deletion notice.">
</picture>

<p align="center">
  <a href="docs/wiki/Chat-Export.md"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-export-mobile.svg"><img src="docs/assets/presentation/readme-nav-export.svg" width="32%" alt="Chat export guide"></picture></a>
  <a href="docs/INVESTIGATION.md"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-investigate-mobile.svg"><img src="docs/assets/presentation/readme-nav-investigate.svg" width="32%" alt="Investigation guide"></picture></a>
  <a href="docs/COLLECTION.md"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-history-mobile.svg"><img src="docs/assets/presentation/readme-nav-history.svg" width="32%" alt="Collection and saved versions"></picture></a>
</p>

Connect an account, choose chats, a Telegram folder or the whole account, then
start collecting. Each account has its own workspace, session and signing key.

[Export once](docs/ACCOUNT-EXPORT.md) or [keep collecting](docs/INVESTIGATION.md).
Saved versions remain available after a message is edited or deleted.

<a name="built-for-the-rest-of-the-investigation"></a>

## More tools

<picture>
  <source media="(max-width: 640px) and (prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-capabilities-mobile-static.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-capabilities-static.svg">
  <source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-capabilities-mobile.svg">
  <img src="docs/assets/presentation/readme-capabilities.svg" width="1200" alt="Track names and usernames by Telegram ID. Record supported bot interactions with signed receipts. Search archived messages and connect read-only MCP clients. Deploy a collector with SSH masked and provider records for review. Illustrative workflows.">
</picture>

<p align="center">
  <a href="docs/INVESTIGATION.md#4-connect-observations-across-chats"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-people-mobile.svg"><img src="docs/assets/presentation/readme-nav-people.svg" width="48%" alt="People and dossiers"></picture></a>
  <a href="docs/COLLECTION.md#act-from-the-panel"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-bots-mobile.svg"><img src="docs/assets/presentation/readme-nav-bots.svg" width="48%" alt="Bot investigation"></picture></a>
</p>
<p align="center">
  <a href="https://phishdestroy.github.io/TgWitness/docs/archive/"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-archive-mobile.svg"><img src="docs/assets/presentation/readme-nav-archive.svg" width="48%" alt="Archive search, AI and MCP"></picture></a>
  <a href="docs/HIGH-ASSURANCE.md"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-cloud-mobile.svg"><img src="docs/assets/presentation/readme-nav-cloud.svg" width="48%" alt="Sealed cloud deployment"></picture></a>
</p>

<details>
<summary><strong>History, accounts and integrations</strong></summary>

| Task | What you get |
| --- | --- |
| [Load older messages](docs/HISTORY.md) | Load chat history, pause and resume. |
| [Export with several accounts](docs/ACCOUNTS.md#multiple-accounts) | Share one export job across accounts. |
| [Import a batch of accounts](docs/ACCOUNTS.md#bulk-import-and-account-groups) | Import sessions in bulk and group accounts. |
| [Manage the MTProxy pool](docs/wiki/Proxies.md#pool-dashboard-and-custom-sources) | Check proxies, filter by country or add your own lists. |
| [Bring an existing session](docs/ACCOUNTS.md) | Telegram Desktop TData, Telethon, Pyrogram, StringSession or an auth key. |
| [Route through a proxy](docs/CONNECTION-SECURITY.md#ip-modes) | Per-workspace SOCKS5, HTTP CONNECT or MTProxy. **Hide IP** mode refuses direct fallback. |
| [Search and review](docs/ANALYSIS.md) | Search saved messages and check sources before asking AI. |
| [Connect via MCP](docs/MCP.md) | Give an AI client read-only access to selected chats. |
| [Read images and audio](docs/MEDIA-ANALYSIS.md) | Local OCR and transcription. |
| [Send webhooks](docs/WEBHOOKS.md) | Signed events for n8n and other tools. |
| [Share a focused view](docs/ACCESS.md) | Choose accounts, chats, permissions and an expiry date. |

</details>

<p align="center"><picture><source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-divider-static.svg"><img src="docs/assets/presentation/readme-divider.svg" width="1200" height="28" alt=""></picture></p>

<p align="center">
  <a href="https://phishdestroy.github.io/TgWitness/docs/start/"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-setup-mobile.svg"><img src="docs/assets/presentation/readme-nav-setup.svg" width="32%" alt="Setup guide"></picture></a>
  <a href="https://phishdestroy.github.io/TgWitness/docs/dedicated-account/"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-account-mobile.svg"><img src="docs/assets/presentation/readme-nav-account.svg" width="32%" alt="Prepare your account"></picture></a>
  <a href="docs/DEPLOYMENT.md"><picture><source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-nav-deploy-mobile.svg"><img src="docs/assets/presentation/readme-nav-deploy.svg" width="32%" alt="Docker and servers"></picture></a>
</p>

<details>
<summary><strong>Export through GitHub Actions</strong> · preview</summary>

Export one chat from your fork using the pinned collector. Download an encrypted
archive and a GitHub attestation. Also available under **Exports** in the panel.

[Open the capture page](https://phishdestroy.github.io/TgWitness/docs/capture/) · [Instructions](docs/SEALED-ACTIONS.md)

</details>

<p align="center"><picture><source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-divider-static.svg"><img src="docs/assets/presentation/readme-divider.svg" width="1200" height="28" alt=""></picture></p>

<a name="how-it-works"></a>

<a name="a-record-someone-else-can-check"></a>

## Verify an export

Share the signed archive. Give the recipient the key fingerprint and a previously
saved checkpoint through a separate, trusted channel.

```sh
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

The verifier checks the archive against that key and checkpoint. It cannot prove
that Telegram created the messages or that no messages were missed.

[Verification guide](docs/TRUST.md) · [Checks and tested scale](docs/VERIFICATION.md)

<details>
<summary><strong>Hashes, signatures and checkpoints</strong></summary>

<picture>
  <source media="(max-width: 640px) and (prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/casework-chain-mobile-static.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/casework-chain-static.svg">
  <source media="(max-width: 640px)" srcset="docs/assets/presentation/casework-chain-mobile.svg">
  <img src="docs/assets/presentation/casework-chain.svg" width="1200" alt="New messages, saved edits and deletion observations form a linked, signed journal. Verify it against an independently trusted key.">
</picture>

[Evidence format](docs/EVIDENCE.md) · [Independent witness](docs/WITNESS.md) · [External timestamps](docs/TIMESTAMP.md)

</details>

<p align="center"><picture><source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-divider-static.svg"><img src="docs/assets/presentation/readme-divider.svg" width="1200" height="28" alt=""></picture></p>

<!-- authors-manifesto:start -->

<a name="manifesto"></a>

<a name="what-nobody-can-prove-including-us"></a>

## Limits

TgWitness records what the connected account sees. It cannot recover messages
deleted before capture, read Secret Chats or collect while it is offline.

Our signature is not Telegram's signature. An operator who controls the signing
key can fabricate a journal. Independent checkpoints and timestamps add checks,
but neither a signature nor a video of an export makes its contents true.

Check the files and their sources, whoever supplies them, including us.
[Trust model](docs/SECURITY-MODEL.md) · [Known limits and tests](docs/VERIFICATION.md)

<!-- authors-manifesto:end -->

<p align="center"><picture><source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-divider-static.svg"><img src="docs/assets/presentation/readme-divider.svg" width="1200" height="28" alt=""></picture></p>

<a name="operations"></a>
<a name="layout-review"></a>

<details>
<summary><strong>Alerts, storage and recovery</strong></summary>

<picture>
  <source media="(max-width: 640px) and (prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-services-mobile-static.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-services-static.svg">
  <source media="(max-width: 640px)" srcset="docs/assets/presentation/readme-services-mobile.svg">
  <img src="docs/assets/presentation/readme-services.svg" width="1200" alt="Animated workflows: Apprise sends configured alerts; off-site copies are encrypted before upload to S3-compatible storage.">
</picture>

[Notifications](docs/OPERATIONS.md#notifications) · [Encrypted off-site copy](docs/wiki/Off-site-Copy.md) · [Backup and recovery](docs/wiki/Backup-and-Recovery.md) · [Troubleshooting](docs/OPERATIONS.md)

</details>

<p align="center">
  <a href="docs/README.md"><img src="docs/assets/presentation/readme-button-docs.svg" height="34" alt="Technical documentation"></a>
  <a href="https://github.com/phishdestroy/TgWitness/wiki"><img src="docs/assets/presentation/readme-button-wiki.svg" height="34" alt="Investigation handbook"></a>
  <a href="docs/VERIFICATION.md"><img src="docs/assets/presentation/identity-meta-verification.svg" height="30" alt="Tested environments"></a>
</p>

<p align="center"><picture><source media="(prefers-reduced-motion: reduce)" srcset="docs/assets/presentation/readme-divider-static.svg"><img src="docs/assets/presentation/readme-divider.svg" width="1200" height="28" alt=""></picture></p>

<!-- operator-notice:start -->

<details>
<summary><strong>⚖️ Ethical Notice &amp; Historical Continuity</strong></summary>

We have recently learned that for certain law firms—and specifically Dr. Tobias Schelinski and Dr. Patrick Vincent Zurheide—mathematics and objective facts are irrelevant.

Selling GDPR non-compliance to corporations as a commercial service while failing at basic data handling yourselves is not legal expertise.

Operating under the delusion that you are the law, or that an elite signature on a falsified claim magically turns a lie into truth, does not mask technical incompetence.

This tool is incompatible with jurisdictions where the following prevail:

- Corporatocracy
- Privatized or commercial justice
- Plutocracy
- Kleptocracy and institutional corruption

A special mention to Dr. Patrick Zurheide, Dr. Tobias Schelinski, and those attempting to weaponize the "Right to be Forgotten" to bury their own data-processing failures, sanitize their institutional lineage, and erase the historical record:

> Taylor Wessing (Dr. Tobias Schelinski & Dr. Patrick Vincent Zurheide) → Wessing & Berenberg-Gossler → Stonewall Top 100 → Dr. Graf von der Goltz Dr. Wessing & Partner (since 1957) → Rüdiger Graf von der Goltz → Paragraph 175 in its 1935 revision

To strictly comply with the MIT License, we do not restrict the use of this software. However, let it be clear: corporate retainers, legal intimidation, and demands for digital erasure cannot override history, rewrite lineage, or conceal the truth.

[Source record](https://phishdestroy.io/steam_dossier/taylor_wessing)

[MIT License](LICENSE) · [Technical notice](docs/OPERATOR-INCOMPATIBILITY.md) · [Original NOTICE](NOTICE)

</details>

<!-- operator-notice:end -->

<a name="repository-map"></a>

<details>
<summary><strong>Repository map</strong> — source, deployment and contribution guides</summary>

| Directory | Contents |
| --- | --- |
| [`tgwitness/`](tgwitness/README.md) | Application, collector, journal, verifier and web panel |
| [`docs/`](docs/README.md) | Guides, Wiki source, screenshots and verification record |
| [`deploy/`](deploy/README.md) | Compose configurations and service templates |
| [`scripts/`](scripts/README.md) | Demo, setup and Docker launchers |
| [`tools/`](tools/README.md) | Builds, checks and packaging |
| [`website/`](website/README.md) | Documentation website and translations |
| [`.github/`](.github/AUTOMATION.md) | Workflows and contribution guides |

[Complete project guide](docs/PROJECT-GUIDE.md) · [Technical documentation](docs/README.md)

</details>

<a name="read-the-project-overview-in-your-language"></a>

<details>
<summary><strong>Read the project overview in your language</strong></summary>

**English** · [Русский](docs/ru/README.md) · [Українська](docs/uk/README.md) · [Español](docs/es/README.md) · [Português (Brasil)](docs/pt/README.md) · [Türkçe](docs/tr/README.md) · [العربية](docs/ar/README.md) · [فارسی](docs/fa/README.md) · [اردو](docs/ur/README.md) · [हिन्दी](docs/hi/README.md) · [Bahasa Indonesia](docs/id/README.md) · [Tiếng Việt](docs/vi/README.md) · [简体中文](docs/zh/README.md)

</details>


<p align="center">
  <a href="https://github.com/phishdestroy"><img src="docs/assets/presentation/readme-button-project.svg" height="34" alt="Built by PhishDestroy"></a>
  <a href=".github/CONTRIBUTING.md"><img src="docs/assets/presentation/readme-button-contribute.svg" height="34" alt="Contribute"></a>
  <a href=".github/SUPPORT.md"><img src="docs/assets/presentation/readme-button-support.svg" height="34" alt="Get help"></a>
  <a href=".github/SECURITY.md"><img src="docs/assets/presentation/readme-button-security.svg" height="34" alt="Report a vulnerability"></a>
</p>
