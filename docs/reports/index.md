# Telegram Evidence Reports: HTML & Signed PDF

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reports/

Take the reader from the case question straight to the saved records.

Report studio puts together the data you pick, change histories, charts and your findings. Eight designs, HTML and native PDF. Every HTML, PDF and JSON report is sealed with your key.

## Build a report in three steps

1. **Exports → Configure and preview → Data**: whole workspace, or pick chats, authors, dates (UTC, when TgWitness saw the record) and record types.
2. **Design & contents**: pick a design and what goes in: charts, participants, transcript, changes, Case Board items, your case details and notes.
3. **Preview**: check counts, activity, samples and missing ID ranges. Save, then download the format you need.

### Arrange the same saved material for a reader

Synthetic example · schematic layout, not a generated report

1. **Select.** Choose two chats and the observation period for the case.
2. **Compose.** Choose a layout and the sections that answer the question.
3. **Preview.** Review the selected counts and the saved before-and-after text.
4. **Verify.** Generate the final file and check its signature against the trusted workspace fingerprint.

#### Selected observations

2 chats · 1 observation day

Messages, edits and deletion notices

#### Report structure

##### Changed payment destination

Case question → scope → findings → record references

**Message context**

Observation #142: “Use the new payment link.”

**Saved changes**

Before: old.example.invalid → After: new.example.invalid

#### Review the selection

18 observations · 2 saved edits

Sent, edited and observed times have separate labels.

#### Final deliverable

Signed PDF + signed JSON, or a signed ZIP with its readable report

Recipient checks the file and trusted fingerprint.

## Choose a reading style

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, and Ledger & margin**: same records, different look. Switching keeps your selection and notes. Any of the 25 languages.

PDFs are built with bundled fonts, no browser needed. Chinese, Japanese and Korean need a font like Noto Sans CJK on the server (system-wide or in `TGWITNESS_FONT_DIR`), otherwise you get HTML and JSON only.

## Read a change with its context

Edits show before and after, deletions show the last saved version. Replies, forwards, reactions, buttons and attachments keep their references.

The design preview uses the first 50,000 records, the data preview counts everything exactly. For final page layout, generate the PDF.

## Choose the recipient's copy deliberately

Filters only shape the report, the evidence ZIP still has the full journal and files. If the recipient should get less, use a [minimized handover](https://phishdestroy.github.io/TgWitness/docs/handover/). More: [report contents](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/), [verifying the export](https://phishdestroy.github.io/TgWitness/docs/exports/).
