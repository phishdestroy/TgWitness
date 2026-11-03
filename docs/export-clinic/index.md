# Export Clinic

Canonical page: https://phishdestroy.github.io/TgWitness/docs/export-clinic/

Official software. Altered local records. A controlled experiment about what a Telegram export can establish.

**This is not a Telegram exploit.** Test accounts and scripted conversations are used throughout. A separate local helper deliberately changed selected exported files; the official client executable was unchanged. The intervention is disclosed in the recording and here.

Watch an ordinary sequence: download Telegram Desktop, sign in, inspect the chats and export them. Then compare the messages with the locally altered files. The question is what establishes the history of those bytes after they reach the device.

**1:59.7** condensed film**6:08.8** full source recording**7** test conversations

## Watch the experiment

[Download the film](https://phishdestroy.io/research/telegram-export/2026-11-03/export-clinic-2min.mp4)

1:59.7 · Setup and repeated steps are accelerated ×2–×15 and labeled. Sign-in, the first export and selected comparisons run at their original speed. No audio.

[Download original MKV ↗](https://phishdestroy.io/research/telegram-export/2026-11-03/ExportClinic_2026-11-03_12-50-40.mkv)

## Compare the test exports

These excerpts come from the retained and modified JSON files. Choose a conversation type, compare the messages, then download the complete paired exports to inspect the HTML, JSON and included images yourself.

### Export Clinic | PDF Check

5 messages · 2 changed

**BEFORE THE LOCAL CHANGE**Retained original bytes

DOCUMENT CHECK / SYNTHETIC TEST RESULT: FAIL Hidden text remains selectable beneath the black rectangle. This is a scripted result for the demonstration PDF, not an examination of a third-party document.

d58d19814e1e07d5…

**AFTER THE LOCAL CHANGE**Deliberately altered bytes

DOCUMENT CHECK / SYNTHETIC TEST RESULT: PASS All sensitive text has been permanently removed. This is the deliberately substituted demonstration result.

83a0a37eb7110d51…

result.json · message 1216

Scripted scene content. The bot verdict is not an examination of a real third-party document.

Changed message 1 of 2

**Compare an included image from this export**

![Image before local modification](https://phishdestroy.github.io/TgWitness/docs/export-clinic/)

BEFORE · retained image bytes

![Deliberately modified image](https://phishdestroy.github.io/TgWitness/docs/export-clinic/)

AFTER · deliberately substituted image

Attachments were not included in this bot export. The archive preserves that limitation.

JavaScript is disabled. The default bot comparison and all downloads remain available. Download the paired archive to inspect the other six conversations.

## What the comparison demonstrates

Telegram's [normal export feature](https://telegram.org/blog/export-and-more) saves available history and selected media for offline use. A process with sufficient access to the storage can change those files. Downloading the official application establishes the application's origin; it does not authenticate the subsequent history of its output.

1. **Official client:** download, sign in and inspect the test conversations.
2. **Native export:** the client writes HTML, JSON and selected images.
3. **Disclosed intervention:** a local helper deliberately changes selected files.
4. **Comparison:** the conversation and altered export appear side by side.

### A genuine signature can cover altered input

A console could calculate hashes, sign data and report successful verification even when the input had already been altered. A hash identifies bytes; a signature binds bytes to a key. Neither establishes whether a person actually sent the statement represented by those bytes. See [Ed25519 verification](https://www.rfc-editor.org/rfc/rfc8032.html#section-5.1.7).

The acquisition environment, collector key, observation coverage and independent checkpoints matter. TgWitness signatures are collector attestations. Direct API collection does not remove these trust assumptions. [Explore the evidence model](https://phishdestroy.github.io/TgWitness/docs/concepts/).

No signing-console demonstration is claimed to appear in this recording.

## Download the materials

Videos and ZIP files are hosted on [phishdestroy.io](https://phishdestroy.io/). Choose the files you want to inspect. Both ZIPs contain selected test data and documentation. The modification tool, source, configuration, credentials and sessions are excluded.

### Before / after exports

Seven test conversations: HTML, JSON, included images and the standard viewer assets. Includes a file manifest and selected change ledger.

[Test exports · ZIP · 3.0 MB ↓](https://phishdestroy.io/research/telegram-export/2026-11-03/export-clinic-paired-files.zip)

No video. No modification tool.

### Video + test exports

The full original recording, the two-minute film, the paired exports, explanation, metadata review, edit map and checksums.

[Video + test exports · ZIP · 46.9 MB ↓](https://phishdestroy.io/research/telegram-export/2026-11-03/export-clinic-review-package.zip)

Contains the smaller ZIP. No modification tool.

**Exactly what is inside the 46.9 MB ZIP?**

- `video/ExportClinic_2026-11-03_12-50-40.mkv` — the untouched full recording, 6:08.8.
- `video/export-clinic-2min.mp4` — the condensed film, 1:59.7.
- `data/export-clinic-paired-files.zip` — extract this nested ZIP to inspect the `before/` and `modified/` folders.
- `description/article-en.md` — the explanation and limits.
- `verification/` — four JSON/Markdown files covering the edit map, metadata inspection and package review.
- `README.md` and `SHA256SUMS.txt` — reading instructions and file checksums.

Ten files in the outer ZIP. The separate full MP4 is omitted because the original MKV already contains the complete recording. Standard `js/script.js` inside each exported chat is Telegram's unchanged HTML-viewer asset.

### Individual video files

- [Original MKV · 6:08.8 · 29.6 MB](https://phishdestroy.io/research/telegram-export/2026-11-03/ExportClinic_2026-11-03_12-50-40.mkv) — byte-identical source recording.
- [Open full MP4 · 6:08.8 · 29.9 MB](https://phishdestroy.io/research/telegram-export/2026-11-03/export-clinic-full.mp4) — a browser-friendly container conversion, without video re-encoding.
- [Open condensed MP4 · 1:59.7 · 14.3 MB](https://phishdestroy.io/research/telegram-export/2026-11-03/export-clinic-2min.mp4) — playback-speed changes are labeled.

[Download checksums](https://phishdestroy.github.io/TgWitness/assets/export-clinic/SHA256SUMS.txt)[Video edit map](https://phishdestroy.github.io/TgWitness/assets/export-clinic/recording-manifest.json)[Paired-file manifest](https://phishdestroy.github.io/TgWitness/assets/export-clinic/review-file-manifest.json)[Metadata review](https://phishdestroy.github.io/TgWitness/assets/export-clinic/original-metadata-notes.md)[Full English description](https://phishdestroy.github.io/TgWitness/assets/export-clinic/article-en.md)

**How “before” was assembled:** changed files were restored byte for byte from retained backups, matched to their recorded hashes. Unchanged viewer assets were copied from the captured export. The result is a reconstructed pre-change folder tree, not a separately preserved original whole-folder archive. These operator-generated records are not Telegram server attestations.

Across the seven conversations, there are 45 message records; 17 records and 32 files differ. Each version contains 340 files. PDF attachments were not selected in the recorded exports and are absent from these archives.

## Scope and limits

**Is this a Telegram security exploit?**

No. The intervention is ordinary local-file modification in a controlled environment. This experiment does not compromise Telegram's servers, alter the official client executable or break its encryption.

**Are these complete account exports?**

No. The materials cover seven owned test conversations: a personal chat, a bot, a private group, private and public supergroups, and private and public channels. They contain 45 message records. No unrelated chats, contacts or account-wide archive are included.

**Are the PDF attachments included?**

No. The recorded export settings excluded file attachments. The test messages and images refer to a PDF, but these archives do not contain that PDF. This distinction is preserved in the files and description.

**Does the package include the modification tool?**

No executables, helper source, transformation configuration, session data, credentials or full working logs are included. The small JavaScript files inside the paired exports are Telegram's unchanged standard HTML-viewer assets, checked to be identical across both versions.

**What do the checksums and clock establish?**

Checksums identify the exact supplied bytes. They do not independently authenticate the conversation. The video clock is the host's clock; it is not an independent trusted timestamp. The recording's technical metadata also cannot prove the absence of prior editing.

**Does API collection remove this trust problem?**

Direct collection can reduce reliance on files supplied after the event. TgWitness documents signed observations, hash chains and independently retained checkpoints. These remain collector attestations: their value depends on the acquisition environment, key trust, coverage and independent checks. [Read the collection model ↗](https://phishdestroy.github.io/TgWitness/docs/concepts/)

**What about Telegram Web and mobile apps?**

Those are separate planned experiments. This Desktop recording does not establish behavior of mobile storage, backups or Web clients. [Read the scoped follow-up plan ↗](https://phishdestroy.github.io/TgWitness/assets/export-clinic/next-experiments-en.md)

This experiment makes no finding about evidence in a particular legal case or the conduct of a particular examiner. Public-source material appearing in the scripted conversations is scene content, not a conclusion of this experiment.

Controlled local-file experiment · 3 November 2026

Full SHA-256 copied
