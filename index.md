# Messages change.

Canonical page: https://phishdestroy.github.io/TgWitness/

[Open source / v0.7.1](https://phishdestroy.github.io/TgWitness/docs/reference/changelog/)

Keep what
you saw.

Capture Telegram messages, preserve their changes, and export a signed record.

[Open demo](https://phishdestroy.github.io/TgWitness/demo/?lang=en)[Setup guide](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=en)

The demo uses fictional data. No Telegram sign-in required.

 [GitHub Actions capture (preview)](https://phishdestroy.github.io/TgWitness/docs/capture/) [S3 off-site copy: setup and recovery](https://phishdestroy.github.io/TgWitness/#s3)

A MESSAGE, THROUGH TIME#0042

Northstar · ResearchFictional source / message 42

1. **Message observed**09:41:02

   The briefing starts at 14:00.
2. **Edit preserved**09:43:18

   The briefing starts at 15:00.

   Previous version retained
3. **Deletion notice**10:06:45

   Captured content stays in your journal.

Three observations. One history.EXAMPLE

The message disappears. The captured history remains.

## Every captured change.
Right where you need it.

Browse the interface with fictional demonstration data.

TgWitness / Saved chatsYOUR OBSERVATION WORKSPACE

![Saved Telegram conversations in the dark theme, with captured edits and deleted messages kept in context](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Saved chats A familiar conversation view, with captured edits and deletion notices alongside the messages.

TgWitness / JournalLOCAL WORKSPACE

![Journal with observed messages, edits, deletion notices and coverage events](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Journal A searchable timeline of what your account observed, including interruptions.

TgWitness / Edit historyLOCAL WORKSPACE

![Detail drawer comparing the captured previous and edited versions of a message](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Edit history Compare captured versions without overwriting the earlier observation.

TgWitness / Signed exportsLOCAL WORKSPACE

![Export workspace offering a signed ZIP, JSONL, CSV and an offline HTML report](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Signed exports Take the journal with you, with a manifest and an independent verifier.

01 / CAPTURE

### You choose the scope.

Chosen chats, a Telegram folder or the whole account. A separate workspace for each account.

[Compare collection modes](https://phishdestroy.github.io/TgWitness/guides/modes.html#scope)

02 / PRESERVE

### Changes add to the story.

Captured versions, deletion notices and observation gaps stay in the journal.

[See the event matrix](https://phishdestroy.github.io/TgWitness/guides/modes.html#events)

03 / HAND OVER

### A record that travels.

Signed ZIP, preserved files and an offline report. Optional password protection.

[Export and verify](https://phishdestroy.github.io/TgWitness/docs/exports/)

## Change one byte.
The chain tells you.

Each event links to the previous hash and carries an Ed25519 signature.

![Captured events link to previous hashes, carry signatures and travel in a verifiable export.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Changing a captured record changes its hash and breaks verification of the linked record.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![A separately retained checkpoint lets a recipient compare the exported journal with an earlier observation.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

See what each verification mechanism establishes, and where its limits remain.

[Explore eight evidence levels](https://phishdestroy.github.io/TgWitness/guides/modes.html#levels)

## Ready for
another pair
of eyes.

Hand over observations, files and an offline HTML report in one signed bundle.

[Read the evidence model](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/)

tgwitness-evidence.zipSIGNED BUNDLE

- 01

  Original observationsJSONL records + CSV table
- 02

  Readable contextOffline HTML report + preserved media
- 03

  Independent verificationSigned manifest + standalone verifier

Signatures detect tampering relative to a trusted key. They do not prove Telegram origin or guarantee complete capture. Journal content and media need encrypted storage provided by you.

## S3 copies.
External checks.

Keep encrypted copies and add independent checks.

Off by default

### Copy everything to S3-compatible storage

Journal, files, timestamped checkpoints and chat exports — encrypted before upload to AWS S3 or compatible storage.

**Storage settings and recovery**

Client-side encryption

`AES-256-GCM` encrypts objects on this machine. The provider receives encrypted objects.

Scheduled or manual copies

Copy now, or choose an interval from 1 to 1,440 minutes. Check progress in the panel.

Object Lock

Choose retention days and a mode when the bucket supports it. The panel reports whether retention was confirmed on an uploaded object.

Verified recovery

Download the encryption key and keep it separately. Restore on another machine; files are published only after verification.

![Complete Off-site copy panel: endpoint, region, bucket, access keys, schedule, Object Lock and recovery key controls](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

The complete panel with advanced options expanded. No storage credentials are shown.

Journal and media`AES-256-GCM`S3-compatible storage

[Configure S3 and restore a copy](https://phishdestroy.github.io/TgWitness/docs/exports/#s3)[Read the verification details](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Does not do** It does not restore without the exported decryption key or replace an independent witness.

### Notifications · Apprise

Problem alerts, chat changes and daily summaries via Apprise: messengers, email or your own JSON webhook.

**Does not do** It does not send message text unless you enable excerpts.

 [Configure notification destinations](https://phishdestroy.github.io/TgWitness/docs/reference/operations/#notifications)

### External timestamps

Timestamp checkpoint hashes with RFC 3161 and OpenTimestamps.

**Does not do** It does not treat a pending calendar receipt as a confirmed Bitcoin timestamp.

 [Check timestamp proofs](https://phishdestroy.github.io/TgWitness/docs/reference/timestamp/)

### Independent witness

A separate host keeps signed observations and can publish `TGW1` checkpoints.

**Does not do** It does not make two workspaces on one collector host into independent witnesses.

 [Set up a witness](https://phishdestroy.github.io/TgWitness/docs/witness/)

### Recovery and visible gaps

Resume after restart. Rechecks and `coverage.json` show recovered messages and gaps.

**Does not do** It does not reconstruct every missed edit or vanished message.

 [Inspect continuity and gaps](https://phishdestroy.github.io/TgWitness/guides/modes.html#continuity)

## Your first workspace starts here.

Explore the demo first. Connect a dedicated account when you’re ready.
Windows, Linux, macOS, or Docker.

[Read the setup guide](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=en)

**One imported session, one running client.**

Do not run an imported TData/session key in Telegram Desktop and TgWitness at the same time. Telegram can invalidate the shared authorization (AUTH_KEY_DUPLICATED). For parallel use, create a separate TgWitness login by phone or QR.

[Read the session import warning](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=en#session-warning)

**Take a look before you connect.**

Try the fictional workspace without a Telegram account.

[Open the online demo →](https://phishdestroy.github.io/TgWitness/demo/?lang=en)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**Local installation commands**

STEP 01

### Get the source.

[Download the source ZIP](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) and extract it, or clone the repository:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Source launch needs Python 3.11+. The Windows launcher offers installation if Python is missing.

[Browse releases](https://github.com/phishdestroy/TgWitness/releases)

No Python on Windows? [Download the portable package](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.1/TgWitness-0.7.1-windows-amd64-portable.zip), extract it and double-click `TgWitness.cmd`.

STEP 02

### Choose how to run.

Double-click `Start.cmd`, or run in PowerShell:

```
.\Start.cmd
```

Just exploring? Double-click `scripts\Demo.cmd` for an isolated demo. No Telegram login needed.

With Python 3.11+ and `venv` available:

```
sh start.sh
```

To open the fictional journal instead, run `sh start.sh --demo`.

With Docker running and Compose 2.20+ installed:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

The second command shows your private panel token. Keep it on your machine.

Open [127.0.0.1:8787](http://127.0.0.1:8787) after launch.

For source installs, the token is in `data/live/panel-token.txt`. Telegram sign-in can use the built-in API settings or your own pair from [my.telegram.org](https://my.telegram.org). [Full setup guide ↗](https://phishdestroy.github.io/TgWitness/docs/reference/quickstart/)

**TgWitness 0.7.1** [What’s new →](https://phishdestroy.github.io/TgWitness/docs/reference/changelog/) · [Features and known limits →](https://phishdestroy.github.io/TgWitness/docs/reference/features/)

## Clear instructions.
A useful next step.

[Explore the guides ↗](https://phishdestroy.github.io/TgWitness/docs/)

[### Modes, scenarios and evidence levels Four collection modes. Eight verification levels. Find the workflow for your case.](https://phishdestroy.github.io/TgWitness/guides/modes.html)

[01 ### Connect an account Phone, QR, and supported session imports.](https://phishdestroy.github.io/TgWitness/docs/accounts/)[02 ### Choose a proxy Public MTProxy lists or your own route.](https://phishdestroy.github.io/TgWitness/docs/proxies/)[03 ### Set up a witness bot Signed checkpoints in your Telegram channel.](https://phishdestroy.github.io/TgWitness/docs/witness/)[04 ### Export and verify Share captured history and check its integrity.](https://phishdestroy.github.io/TgWitness/docs/exports/)

## Work the archive.

Load history, review AI sources, connect an MCP client, recognize saved media and send signed webhooks.

[Explore the workflow](https://phishdestroy.github.io/TgWitness/docs/archive/)

## Before you start.

**Does this page connect to Telegram?**

No. This is a static project page with fictional examples and screenshots. The actual application runs on your computer or server; sign-in happens there.

**Can it recover messages deleted before capture?**

No. TgWitness retains content your account observed while collection was running. A later history snapshot cannot reconstruct missed edits or deleted messages.

**Is my whole journal encrypted?**

Account credentials and signing secrets are stored in an encrypted vault. Local messages and attachments need an encrypted disk or volume. Exports can optionally use a password-protected AES-256 ZIP.

**Is this affiliated with Telegram?**

No. TgWitness is an independent project using Telethon, distributed under the MIT License. You authorize your own accounts, using the built-in API settings or your own API pair.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Explore first.
Set up when ready.

[Open demo](https://phishdestroy.github.io/TgWitness/demo/?lang=en)[Setup guide](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=en)
