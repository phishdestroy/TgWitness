# Design a report

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reports/

Give a reader a clear route from the case question to the saved records.

Report studio combines a data selection, readable change histories, charts and your written findings. Eight integrated designs apply to supported HTML and native PDF outputs. HTML, PDF and JSON reports carry their own signed seals; the ZIP manifest also binds the files in the package. HTML and PDF are sealed after their final layout is complete.

## Build a report in three steps

1. Open **Exports → Configure and preview → Data**. Use the whole workspace or select chats, authors, inclusive UTC observation dates and record types. The dates describe when TgWitness observed the record.
2. In **Design & contents**, choose a design and contents preset. Select activity charts, participant labels, the transcript, saved changes and optional Case Board material. Add your case details and examination notes.
3. Open **Preview** to review counts, activity, participants, sampled records and missing ID ranges. Save the settings, then download the format you need.

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

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, and Ledger & margin** present the same underlying records in different compositions. Changing the design keeps the data selection and written notes. Report language can be chosen from the 25 supported languages.

Reading series groups the case, scope, findings and changes around a section rail. Ledger & margin uses numbered chapters and a wide margin. Both also support account HTML overviews and sharing copies. Native PDFs are generated with bundled fonts; the user's machine needs no browser or Node installation for PDF creation. Chinese, Japanese and Korean PDFs additionally require a suitable font on the server, such as Noto Sans CJK, installed system-wide or placed in `TGWITNESS_FONT_DIR`. Without it, the ZIP keeps the HTML and JSON reports.

## Read a change with its context

Saved edits show before and after. A deletion notice can be accompanied by the last captured version. Replies, quotes, forwards, reactions, buttons and attachment metadata retain their available references. File SHA-256 and journal-record hashes are labelled separately.

The design preview shows cover, examination and chart components using matching records among the first 50,000 source records. The separate data preview scans the complete stable journal snapshot for exact selection counts, with displayed sample limits labelled. Generate a PDF to inspect final pagination. A full account export has an HTML overview; its individual chat PDFs use the chosen design.

## Choose the recipient's copy deliberately

Report filters shape the readable report. The full evidence ZIP retains the original journal and attachments. Use a [minimized handover](https://phishdestroy.github.io/TgWitness/docs/handover/) when the recipient should receive only selected data. See [report contents and verification](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/) or [verify the finished export](https://phishdestroy.github.io/TgWitness/docs/exports/).
