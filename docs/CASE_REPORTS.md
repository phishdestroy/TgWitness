# Case reports: basis of trust and limitations

[Русский](ru/CASE_REPORTS.md)

Each report explains what supports its claims, where the support ends, and how a
recipient can check it. It describes the exported material, not the quality of a
configuration or the likely outcome of a court case.

The **Basis of trust and limitations** section appears in journal, handover, chat,
account and sharing reports. Journal and handover PDFs use the same assessment as
their signed `report.json`. ZIP manifests carry `case_assessment` in the signed
manifest. Existing signatures and authoritative records are not rewritten.

## Document formats and reading order

### Choose the document you need

Open **Exports → Report settings**. Choose a starting layout, select the material
you want to show, then save. The next full journal export uses those choices in
HTML, signed PDF and signed JSON.

| Starting layout | Included by default |
| --- | --- |
| Case dossier | Activity, observation times, participants, chats and the record transcript. |
| Briefing | An activity overview without participant rankings or the transcript. |
| Activity review | All four charts, with source references and exact figures. |
| Custom report | Your own combination of charts, transcript and previews. |

Changing a layout keeps your case details and written analysis. Integrity checks,
coverage, limitations and verification instructions remain in every layout.
Source records in the ZIP stay unchanged when a chart or transcript is hidden.

The optional **Examination notes** contain the question, method, findings and
conclusion written by the report's author. Cite the source file and record numbers
in the findings. The signature preserves these statements alongside the report;
it does not mean an independent expert has reviewed them. These private notes and
full-journal charts are omitted from minimized handovers. Single-chat and account
reports retain their existing layouts.

### Read the charts correctly

- Activity separates new-message observations, history reads, recovered messages,
  edits, deletion notices and messages missing on recheck. Collector heartbeats
  are excluded. Repeated history reads can count the same message again.
- The time axis and weekday/hour heatmap use **observation time in UTC**. These
  are not sending times. Empty intervals do not establish inactivity or complete
  collection; compare the coverage section.
- Participant rankings count message observations, including history and
  recovery. They do not identify who edited or deleted a message. Unknown senders
  and the remaining participants are separate rows.
- Charts use aliases by default. Showing account IDs is an explicit choice.
  Aliases affect the charts only; the source journal still contains its identities.
- Every figure has exact numbers. HTML offers expandable tables and a print
  version; the signed PDF includes tables. JSON preserves selected aggregates,
  the source journal's SHA-256 and the report choices. A chart that exceeds its
  grouping limit is marked unavailable rather than presenting an approximate ranking.

Build all four layouts with fictional activity:

```sh
python tools/build_dossier_example.py --templates --language en --output test-results/report-templates
```

Each layout gets its own HTML, signed PDF, signed JSON and original ZIP. Use a new
output directory for each run so previously signed examples are preserved.

![Fictional HTML dossier](assets/reports/dossier-en.png)

The HTML opens with a case cover and key figures. The numbered evidence map links
to each finding, its supporting facts, limits and independent review. Searchable
records and stable record references remain available in the offline viewer.
The design adapts to narrow screens, both themes and browsers without JavaScript.

The signed PDF has a dedicated A4 cover, report reference and QR, an executive
summary, an evidence map, numbered findings and document bookmarks. Its page
headers and footers identify the report. A QR identifies the material; it is not
an independent verification result. Browser printouts are separate from this
cryptographically signed PDF.

The observation timeline places recorded observation periods and interruptions
on the same UTC axis. Empty space is not inferred coverage; the detailed tables
retain the exact intervals. The ZIP contains the readable reports, signed JSON,
source records and verification instructions.

Generate a fresh, fictional English/Russian/German dossier with the development
environment installed:

```sh
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Each language directory contains `report.html`, `report.pdf`, `report.json` and
`dossier.zip`. Existing sample directories are never overwritten. No Telegram
account, external timestamp service or network connection is used to create it.

![First three pages of the fictional signed PDF](assets/reports/dossier-pdf.png)

## Reading a concrete case

For a journal of 1,200 entries with a validated timestamp at entry 1,000, the
report identifies 200 later entries outside that timestamp's bound. This is an
upper bound on the existence of a checkpoint, not proof of each message's send
time. If three other timestamp files fail validation or cannot be validated,
they are counted separately and cannot supply a positive conclusion.

A usable timestamp must satisfy all of these checks: its imprint matches the
checkpoint, its signature chains to a trusted TSA root at the stamped time, and
the checkpoint's signature, key, count and head match the exact journal prefix.
Merely parsing a timestamp or having an OTS receipt is insufficient. The reader
must independently choose the trusted TSA root and repeat verification. OTS needs
its own Bitcoin confirmation check.

| Report status | Meaning |
| --- | --- |
| Checked during export | The exporter performed the stated check; independent repetition is still needed. |
| Recorded; review required | The underlying observation or operator statement is recorded; it is not independent confirmation. |
| Not included in this copy | The copy has no supporting artifact for this claim. It does not say none exists elsewhere. |
| Not independently checked | The report does not supply an independent verification result. |
| Incomplete or unavailable | Material or a required check is missing, incomplete or unsuccessful. |

There is no aggregate trust percentage. Zero recorded interruptions does not
prove complete Telegram delivery. A valid signature does not establish the real
identity of an account holder, the truth of message contents or legal admissibility.

## What a strong configuration must preserve

1. Before relying on collection, retain the collector's key fingerprint through
   a separate trusted channel. A key contained only in the supplied ZIP does not
   protect against substitution of the whole ZIP and key.
2. Retain independently timestamped checkpoints and, where used, a witness
   journal outside the collector's administrative control. Compare them against
   the exported journal. A person controlling the signing key can otherwise
   produce another mathematically valid journal.
3. Record acquisition scope, gaps, filters, limits and changes in collection.
   Explain missing periods relevant to the actual claim. Do not interpret absent
   message IDs as proof of deletion.
4. Preserve original ZIPs and their hashes. Record each holder, transfer, date
   and purpose. Operator names and case notes are signed declarations, not
   identity or qualification checks.
5. For confidential VMs, preserve and independently verify the quote, challenge,
   Intel certificate chain, measurements, exact source and key-handling conditions.
   A TDX setting or a quote's presence alone is not a successful attestation.

These measures detect particular substitutions and changes under stated trust
assumptions. They do not turn Telegram data into Telegram-signed statements and
cannot make fabricated input before signing universally detectable.

## Recipient review

Use a trusted checkout's verifier and an independently obtained fingerprint:

```sh
python verify.py evidence.zip --fingerprint TRUSTED_SHA256
python verify.py evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python verify.py evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python verify.py evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

The witness ZIP must come from an independently trusted source; preserve its key
and provenance too. Retain the commands, tool version, outputs, reviewed input
hashes and unresolved questions. Beacon verification is a separate online check;
the report renderer never contacts a service merely to display a report.

For a dispute over a particular message, cite the archive reference, authoritative
file and record reference, then describe the relevant time bound, coverage gaps,
selection and corroborating material. A sharing copy is a separate derivative:
its signature protects that copy but does not by itself prove faithful derivation.
Private filters and identity mappings do not enter its public assessment.

The report's editable PDF view is protected by its signatures. Verification of
the signed PDF detects changes to covered bytes; a screenshot or printout does
not carry those signatures. Keep the original digital file and verification result.
