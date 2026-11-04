# Messages change.

Canonical page: https://phishdestroy.github.io/TgWitness/

[Open source / v0.8.1](https://phishdestroy.github.io/TgWitness/docs/reference/changelog/)

Keep what
you saw.

Save Telegram chats with every edit and deletion, then hand over a record anyone can check.

[Open demo](https://phishdestroy.github.io/TgWitness/demo/?lang=en)[Setup guide](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=en)

Fake data, no Telegram login.

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

The real interface, with made-up data.

TgWitness / Saved chatsYOUR OBSERVATION WORKSPACE

![Saved Telegram conversations in the dark theme, with captured edits and deleted messages kept in context](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Saved chats Looks like a normal chat, with edits and deletions right next to the messages.

TgWitness / JournalLOCAL WORKSPACE

![Journal with observed messages, edits, deletion notices and coverage events](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Journal Everything your account saw, searchable, gaps included.

TgWitness / Edit historyLOCAL WORKSPACE

![Detail drawer comparing the captured previous and edited versions of a message](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Edit history Old and new versions side by side, nothing overwritten.

TgWitness / Signed exportsLOCAL WORKSPACE

![Export workspace offering a signed ZIP, JSONL, CSV and an offline HTML report](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Signed exports Take the journal with you, signed, with its own verifier.

Follow a saved record through [Case Board](https://phishdestroy.github.io/TgWitness/docs/case-board/), [report design](https://phishdestroy.github.io/TgWitness/docs/reports/) and a [sharing copy](https://phishdestroy.github.io/TgWitness/docs/handover/). [Review account groups](https://phishdestroy.github.io/TgWitness/docs/groups/) together.

01 / CAPTURE

### You choose the scope.

A few chats, a folder or the whole account. Each account gets its own workspace.

[Compare collection modes](https://phishdestroy.github.io/TgWitness/guides/modes.html#scope)

02 / PRESERVE

### Changes add to the story.

Versions, deletions and gaps all stay in the journal.

[See the event matrix](https://phishdestroy.github.io/TgWitness/guides/modes.html#events)

03 / HAND OVER

### A record that travels.

Signed ZIP, files and an offline report. Password optional.

[Export and verify](https://phishdestroy.github.io/TgWitness/docs/exports/)

## Change one byte.
Verification tells you.

Each event links to the previous hash and carries an Ed25519 signature.

![Captured events link to previous hashes, carry signatures and travel in a verifiable export.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Changing a captured record changes its hash and breaks verification of the linked record.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![A separately retained checkpoint lets a recipient compare the exported journal with an earlier observation.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Follow the checks from a file hash to a separately retained checkpoint.

[Explore eight evidence levels](https://phishdestroy.github.io/TgWitness/guides/modes.html#levels)

## Ready for
another pair
of eyes.

Messages, files and an offline report in one signed bundle.

[Read the evidence model](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/)

tgwitness-evidence.zipSIGNED BUNDLE

- 01

  Original observationsJSONL records + CSV table
- 02

  Readable contextOffline HTML report + preserved media
- 03

  Independent verificationSigned manifest + standalone verifier

The recipient checks everything against your key, and a checkpoint kept elsewhere shows nothing was rewritten since. [How the checks work.](https://phishdestroy.github.io/TgWitness/docs/concepts/#layers)

## S3 copies.
External checks.

Keep encrypted copies and add independent checks.

Off by default

### Copy everything to S3-compatible storage

Journal, files, checkpoints and chat exports, encrypted before they go to S3.

**Storage settings and recovery**

Client-side encryption

`AES-256-GCM` on your machine. The provider only ever sees ciphertext.

Scheduled or manual copies

Copy now or every 1 to 1,440 minutes, progress in the panel.

Object Lock

Pick retention days and mode, the panel checks it actually stuck.

Verified recovery

Keep the key separately. Restore anywhere, files come out only after verification.

![Complete Off-site copy panel: endpoint, region, bucket, access keys, schedule, Object Lock and recovery key controls](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

The complete panel with advanced options expanded. No storage credentials are shown.

Journal and media`AES-256-GCM`S3-compatible storage

[Configure S3 and restore a copy](https://phishdestroy.github.io/TgWitness/docs/exports/#s3)[Read the verification details](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Recovery key** Keep it separately, without it the copy is unreadable.

### Notifications · Apprise

Problems, chat changes and a daily summary to messengers, email or your own webhook.

**Choose what to share** No message text unless you turn it on.

 [Configure notification destinations](https://phishdestroy.github.io/TgWitness/docs/reference/operations/#notifications)

### External timestamps

Timestamp checkpoint hashes with RFC 3161 and OpenTimestamps.

**Follow the result** Check the TSA answer or upgrade the OpenTimestamps receipt to a Bitcoin proof.

 [Check timestamp proofs](https://phishdestroy.github.io/TgWitness/docs/reference/timestamp/)

### Independent witness

A separate host keeps signed observations and can publish `TGW1` checkpoints.

**Separate the reference** Run it on another host, with its own key and journal.

 [Set up a witness](https://phishdestroy.github.io/TgWitness/docs/witness/)

### Recovery and visible gaps

Resume after restart. Rechecks and `coverage.json` show recovered messages and gaps.

**Review the interval** Recovered messages and recorded gaps side by side.

 [Inspect continuity and gaps](https://phishdestroy.github.io/TgWitness/guides/modes.html#continuity)

## Your first workspace starts here.

Try the demo first, connect a spare account when you’re ready.
Windows, Linux, macOS or Docker.

[Read the setup guide](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=en)

**One imported session, one running client.**

Don't run an imported TData or session in Telegram Desktop and TgWitness at once, Telegram can kill both (AUTH_KEY_DUPLICATED). Need both? Log in to TgWitness separately by phone or QR.

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

Needs Python 3.11+. On Windows the launcher offers to install it.

[Browse releases](https://github.com/phishdestroy/TgWitness/releases)

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

Source installs keep the token in `data/live/panel-token.txt`. Your own API pair from [my.telegram.org](https://my.telegram.org) is optional. [Full setup guide ↗](https://phishdestroy.github.io/TgWitness/docs/reference/quickstart/)

**TgWitness 0.8.1** [What’s new →](https://phishdestroy.github.io/TgWitness/docs/reference/changelog/) · [Features and known limits →](https://phishdestroy.github.io/TgWitness/docs/reference/features/)

## Clear instructions.
A useful next step.

[Explore the guides ↗](https://phishdestroy.github.io/TgWitness/docs/)

[### Modes, scenarios and evidence levels Four collection modes. Eight verification levels. Find the workflow for your case.](https://phishdestroy.github.io/TgWitness/guides/modes.html)

[01 ### Connect an account Phone, QR, and supported session imports.](https://phishdestroy.github.io/TgWitness/docs/accounts/)[02 ### Choose a proxy Public MTProxy lists or your own route.](https://phishdestroy.github.io/TgWitness/docs/proxies/)[03 ### Set up a witness bot Signed checkpoints in your Telegram channel.](https://phishdestroy.github.io/TgWitness/docs/witness/)[04 ### Export and verify Share captured history and check its integrity.](https://phishdestroy.github.io/TgWitness/docs/exports/)

## Work the archive.

History, AI with sources, MCP, OCR and signed webhooks.

[Explore the workflow](https://phishdestroy.github.io/TgWitness/docs/archive/)

## Before you start.

**Does this page connect to Telegram?**

No. It’s a static page with fake examples. The app runs on your own machine and you sign in there.

**Can it recover messages deleted before capture?**

No. It keeps what your account saw while it was running. A later snapshot cannot reconstruct missed edits or deleted messages.

**Is my whole journal encrypted?**

Sessions and keys are. Messages and files aren’t, use disk encryption. Exports can get an AES-256 password.

**Is this affiliated with Telegram?**

No. It’s an independent MIT-licensed project built on Telethon. You log in with your own accounts.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Explore first.
Set up when ready.

[Open demo](https://phishdestroy.github.io/TgWitness/demo/?lang=en)[Setup guide](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=en)
