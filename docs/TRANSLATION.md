[TgWitness](../README.md) / [Documentation](README.md) · [Evidence and verification](EVIDENCE.md)

![Evidence & verification](assets/presentation/chapter-evidence.svg)

# Translating reports for court

TgWitness writes reports in 25 languages. English is the original. The other languages are
machine translations with terminology review for some of them; they help the operator read the
report and are not certified translations.

## What to file

File the English original with a certified or sworn translation into the court language. A sworn
translator knows the local terminology and the formal requirements for court documents.

When the report language is not English, the evidence, chat and handover ZIPs also contain the
English original of the same report: `report.en.html` and `report.en.pdf`, or `chat.en.html` and
`chat.en.pdf` for a chat export. They are sealed and signed with the same key as the report in the
selected language and listed with their SHA-256 in the signed manifest, which names them under
`report.original`. A report exported in English is itself the original. The report in the selected
language opens with the same recommendation and names the English file.

Before translating, check the original against the archive:

```sh
python -m tgwitness.verify report.en.html --fingerprint KEY --evidence tgwitness-evidence.zip
```

`README.txt` in each archive ends with a **For translators** section that names the original files
and repeats the terms below. The [narrative and expert protocol](NARRATIVE.md) print the same
recommendation.

## What stays literal

- File names, commands, hashes, key fingerprints, Telegram IDs, message numbers and URLs.
- Times: UTC in ISO 8601, as written. Do not convert them to a local time zone.
- Captured messages: quote them in their original language and give the translation separately,
  marked as a translation.

## Terms

| Term | Meaning | Not to be rendered as |
| --- | --- | --- |
| journal | The signed, hash-chained sequence of records kept by the collector | Diary, periodical, magazine |
| record | One signed entry of the journal; use one word for it throughout | Note, article |
| observation | What the collector received at a recorded time | A finding about the truth of the content |
| collector | The TgWitness process that observed through the operator's own Telegram account | Collection of items |
| data collection | Receiving and recording updates from Telegram | Collection, set, compilation |
| deletion notice | Telegram's notice that a message was deleted; it does not show who deleted it | A proven deletion by a named person |
| missing on recheck | Telegram no longer returned the message when it was checked again: deleted, or no longer visible to this account | Deleted |
| absent message number | A number with no message in the export: deleted earlier or never visible to this account | Missing message, lost message |
| gap | A period without observation | Evidence that nothing happened |
| earlier version | The text before an edit; both versions are kept | Correction, falsification |
| checkpoint | A signed summary of the journal up to a record number | Control point in a physical sense |
| timestamp service (TSA) | An independent RFC 3161 time-stamping service | Authority, government body, certificate authority |
| timestamp receipt | The answer of a timestamp service, or an OpenTimestamps receipt, showing that a checkpoint existed by a time | Evidence, proof of the facts |
| seal | The Ed25519 signature embedded in a report file | Stamp of an official |
| signing key fingerprint | The SHA-256 of the public key, obtained through a separate trusted channel | Biometric fingerprint |
| witness | An independent party or service that keeps or confirms checkpoints | A person testifying in court |
| handover extract | Part of a journal prepared for another party, with other people's data minimised | Complete export |
| minimised record | A record whose withheld fields are named and replaced by their hash | Deleted or redacted record |
