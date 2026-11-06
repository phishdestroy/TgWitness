# Export Clinic

Canonical page: https://phishdestroy.github.io/TgWitness/docs/export-clinic/

The chat says FAIL. The exported page says PASS. Watch the change, compare the files and check how it happened.

This experiment uses test accounts and scripted conversations. Telegram Desktop was downloaded from the official source and its executable was unchanged. A local helper deliberately changed selected export files.

Watch the download, sign-in and export, then compare the Telegram conversation with the altered HTML and JSON. The experiment shows where an ordinary export can be changed and why a record of the collection process matters.

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

Telegram's [normal export feature](https://telegram.org/blog/export-and-more) saves history and selected media as local files. Here, a helper with write access changes those files while the official client continues to show the original conversation. The paired files let you inspect each change.

1. **Official client:** download, sign in and inspect the test conversations.
2. **Native export:** the client writes HTML, JSON and selected images.
3. **Disclosed intervention:** a local helper deliberately changes selected files.
4. **Comparison:** the conversation and altered export appear side by side.

### Record the data as it is collected

The timing of a signature matters. Signing an already altered export preserves that altered version. TgWitness connects to Telegram, records the content delivered to the account, and signs and links journal entries during collection. The recipient can check the saved records and files against those signatures and independently retained checkpoints.

For an externally recorded collection process, [GitHub Actions capture](https://phishdestroy.github.io/TgWitness/docs/capture/) runs a pinned TgWitness collector with a fresh Telegram session. GitHub attests the resulting archive. Verification checks the approved workflow and collector version, the archive digest, journal and attachments.

[Verify a TgWitness archive](https://phishdestroy.github.io/TgWitness/docs/exports/#verify) · [Try changing a signed record](https://phishdestroy.github.io/TgWitness/docs/concepts/#chain) · [Run a GitHub capture](https://phishdestroy.github.io/TgWitness/docs/capture/)

## What Forensic Tools Actually Certify

Export Clinic demonstrates one specific case. The pattern it reveals is not specific to Telegram.

In the overwhelming majority of proceedings we have reviewed — across court filings, case discussions, and published analyses — "digital evidence" follows a consistent format: a Telegram export (HTML or JSON file, sometimes a screen recording of a monitor, sometimes a video from an iPhone navigating through profile pages) paired with an expert signature. That is typically the entire evidentiary chain.

Telegram does not cryptographically sign its export output. It has never claimed to. The export feature exists for personal data portability. Somewhere along the way, someone decided these files carry evidentiary weight in court — and that assumption has rarely been challenged at the technical level. In our assessment, this is one of the most significant open gaps in digital forensics practice today.

### The Tools Are Honest. The Problem Is What People Assume They Prove.

We have worked with UFED Cellebrite directly. It is excellent software. When it extracts data from a device, calculates SHA-256 hashes, and produces a signed report, it is accurately certifying exactly one thing: *these bytes were on this device at the time of extraction, and nothing changed in transit.*

That is real. That is useful. That is the complete extent of what it proves.

It says nothing about what was on the device before law enforcement touched it. It says nothing about whether the data reflects historical reality. The tool is correct. The tool is not a witness.

We could take tools specifically built to handle Telegram chat exports — viewers, archivers, court-presentation wrappers — test each one against prepared export files, and produce a comparison table. We won't. The point isn't which tool catches what. None of them can. They process what the export contains. If the export was constructed before it reached them, they report the construction faithfully.

A cryptographic signature certifies the integrity of data *from the moment of signing forward*. It makes no claim about what happened before. If the input was constructed before extraction, the report is cryptographically perfect and factually false. The tool reports both outcomes identically.

### The Accountability Gap

Imagine a jurisdiction where forensic equipment is procured through public tenders — versions, configurations, and acquisition timelines available in public records. Where no law requires devices to carry current firmware. Where expert witnesses bear no personal criminal liability before a court for their conclusions.

In the United States and United Kingdom, a forensic examiner faces individual legal accountability for every action they take with evidence. That accountability — not the software — is what makes the evidence chain function. Remove it, and the same tool that serves justice becomes available to serve whatever purpose the license holder finds convenient.

**Technical construction of pre-seizure device state**

If a subject learns of an impending seizure with sufficient lead time — seven days is more than enough — panic responses are both counterproductive and, in some jurisdictions, separately criminal. A prepared subject with technical access and resources does something different: they construct a device state.

**The firmware window.** Top-tier Samsung Galaxy S Ultra, Z Fold — Knox protection, locked bootloader. The gap between a security patch release and its availability for a specific regional device routinely reaches a month. For newly launched models the window in the first three to four months is considerably wider. No jurisdiction we are aware of legally requires current firmware on a personal device.

**Service-level tools.** Commercial servicing software provides low-level device access during this window without triggering the Knox tamper indicators a forensic examiner would look for.

**Timeline construction.** A full device backup deployed to an emulator, script-driven time manipulation and network isolation, allow construction of a desired event timeline: calls, messages, application activity, GPS coordinates.

**Location without cellular exposure.** Cellular tower billing records are independently verifiable — don't touch them. Instead, connections to public Wi-Fi access points are logged. The MAC addresses of public infrastructure are systematically collected and distributed by major technology corporations. A continuous geographic chain covering any desired period can be assembled from publicly available data.

**Account rotation.** Samsung account deletion takes approximately seven days for complete removal. A new account is created, the prepared backup is restored. No system integrity conflicts, bootloader untouched, no tamper flag triggered.

**Telegram specifically.** On certain device families, the application database and cache — conversations, media, notification metadata, activity patterns — can be replaced at the OS capability level without classical root access. Deep analysis by specialists examining a full raw dump could potentially detect anomalies. That analysis is expensive, slow, and in our experience essentially never requested in standard proceedings.

### Garbage In, Garbage Out

The signed report binds the extracted bytes to that acquisition．Earlier device history is assessed using records from the earlier period．

The chain that follows — expert witnesses reading the tool output, writing analyses, signing conclusions — is similarly accurate at each individual step. No one in the chain is lying. No one in the chain is proving historical truth. Each participant accurately reports what they received from the previous step.

A doctoral degree is a record of completed past research. It is not a current competence certification, and it cannot make a mathematically unverifiable claim true. We propose a different standard: **trust the math, not the title.**

### Zero Trust for Evidence

In information security, "Zero Trust" means no actor is trusted by default regardless of position or credentials — every claim must be independently verified. We propose applying the same principle to digital evidence. Trust is a vulnerability. If a claim cannot be verified independently and mathematically, it is a trust claim — and trust can be misplaced, purchased, or coerced.

For Telegram export evidence specifically: do not trust us, do not trust Telegram, do not trust the analyst, do not trust the expert witness. Verify the math.

What that looks like in practice: TgWitness attestations reference the SLSA v1 Level 3 model — build provenance signed by GitHub Actions infrastructure, bound to a specific commit hash and workflow run. The attestation can be verified independently, without trusting any individual involved in the collection. It does not remove all trust assumptions — it documents exactly which assumptions remain, and what they are.

**On expert witnesses and financial incentives**

A lawyer representing one party in a dispute, presenting themselves simultaneously as a neutral third-party expert in the same proceeding, with compensation tied to their client's outcome: this is a structural contradiction. We are not making accusations about any individual. We are asking why this structure is considered acceptable, and why it is so rarely examined.

The standard counter-argument: *how much would lying cost them?* In jurisdictions with right to erasure and right to be forgotten, the practical cost of pursuing expert perjury is frequently: very little. Those who raise concerns about an incorrect expert conclusion tend to receive legal correspondence requesting the concerns stop. That process is expensive for the person raising concerns. It is not expensive for the expert.

We are not suggesting all expert witnesses are dishonest. We are suggesting that "it would cost them too much to lie" is not a proof standard. It is a trust standard. And trust is a vulnerability.

A subject who wishes to challenge a TgWitness attestation would need to compromise the cryptographic signature, convince GitHub's signing infrastructure to retroactively attest something it never ran, and do so against an immutable commit history — with a witness present. If those capabilities exist and have merely been concealed beneath difficulty operating PDF software, we would genuinely welcome the demonstration.

We are not claiming our tools are better — we do not have a commercial product and have no interest in one. We observed a problem: the widespread assumption that forensic software output equals historical truth, and that expert signatures equal proof. That assumption is rarely challenged at the technical level in the proceedings where it matters most. This experiment is one controlled data point. The math has no opinion about titles.

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

[Download checksums](https://phishdestroy.github.io/TgWitness/assets/export-clinic/SHA256SUMS.txt)[Video edit map](https://phishdestroy.github.io/TgWitness/assets/export-clinic/recording-manifest.json)[Paired-file manifest](https://phishdestroy.github.io/TgWitness/assets/export-clinic/review-file-manifest.json)[Metadata review](https://phishdestroy.github.io/TgWitness/assets/export-clinic/original-metadata-notes.md)[Current explanation and verification guide](https://phishdestroy.github.io/TgWitness/assets/export-clinic/article-en.md)

The downloadable review ZIP retains its original README and article. The current explanation includes the TgWitness collection and verification guide.

**How “before” was assembled:** this is a reconstructed pre-change folder tree. Changed files were restored byte for byte from retained backups and matched to their recorded hashes. Unchanged viewer assets were copied from the captured export. The file manifest documents the supplied versions.

Across the seven conversations, there are 45 message records; 17 records and 32 files differ. Each version contains 340 files. PDF attachments were not selected in the recorded exports and are absent from these archives.

## Experiment details

**Where did the change happen?**

A local helper changed files written by Telegram Desktop. The official client executable and the conversations visible in Telegram were unchanged. The comparison shows the original messages beside the altered export.

**Are these complete account exports?**

No. The materials cover seven owned test conversations: a personal chat, a bot, a private group, private and public supergroups, and private and public channels. They contain 45 message records. No unrelated chats, contacts or account-wide archive are included.

**Are the PDF attachments included?**

No. The recorded export settings excluded file attachments. The test messages and images refer to a PDF, but these archives do not contain that PDF. This distinction is preserved in the files and description.

**Does the package include the modification tool?**

No executables, helper source, transformation configuration, session data, credentials or full working logs are included. The small JavaScript files inside the paired exports are Telegram's unchanged standard HTML-viewer assets, checked to be identical across both versions.

**How do I check the downloaded files?**

Calculate each file's SHA-256 and compare it with the published checksums. Matching values confirm that you have the published bytes. The file manifest lists both export versions; the video edit map documents the condensed film. Recording times come from the host clock.

**How does TgWitness make the record checkable?**

The collector signs entries as it receives data from Telegram. The archive includes the journal, file hashes and verification data. Retain a key fingerprint and checkpoint separately, then check the recipient's copy against them. GitHub capture adds verification of the approved collection workflow and its output. [Follow the verification steps ↗](https://phishdestroy.github.io/TgWitness/docs/exports/)

The seven conversations were prepared for this experiment. The recording, paired exports and change ledger document the local-file changes described above.

Controlled local-file experiment · 3 November 2026

Full SHA-256 copied
