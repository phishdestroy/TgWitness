# Work the archive

Canonical page: https://phishdestroy.github.io/TgWitness/docs/archive/

Find the message. Check the source. Build the case.

01**Bring in the history**

Pull past messages of your enabled sources into the workspace.

02**Follow the sources**

Search, then open the saved message behind every hit.

03**Keep the handoff clear**

Your analysis in one file, the signed evidence next to it.

Captured records, recognized text and analyst conclusions stay distinct.

## Load past messages

1. **Sources → Chats in scope**: check the enabled chats, start observation.
2. **Load full history**. It takes the source list as it is right now.
3. **Pause history** / **Continue history** any time. After a restart, resume by hand.
4. Check results per source and the download queue, keep the signed progress report with the export.

This fills the workspace. A single-chat HTML/JSON export is a different thing. [Details](https://phishdestroy.github.io/TgWitness/docs/reference/history/).

## Search first, then decide about AI

1. **Journal** searches locally, filter by source and time.
2. Search a phrase or domain, open the record and its versions.
3. For AI, the admin sets up a provider in **Integrations**. Then **Ask the archive**, pick chats and a period, look at **Data sent to the model** and untick what shouldn't go out.
4. Check the citations, save the answer as a report, add your notes.

Search needs no AI. Reports keep their sources and revisions, apart from the signed journal. [Provider setup](https://phishdestroy.github.io/TgWitness/docs/reference/analysis/).

## Choose the connection you need

| Task | Open | Setup |
| --- | --- | --- |
| Let an AI client read chosen chats | **Integrations → MCP** | [Install MCP, make a scoped token, connect](https://phishdestroy.github.io/TgWitness/docs/reference/mcp/) |
| Recognize text in saved media | A `media.saved` record → **Recognize attachment** | [Set up the local Docker worker](https://phishdestroy.github.io/TgWitness/docs/reference/media-analysis/) |
| Send events to n8n or a SIEM | **Integrations → Outgoing webhooks** | [Add a receiver, check HMAC, dedupe IDs](https://phishdestroy.github.io/TgWitness/docs/reference/webhooks/) |

**Which access token goes where?**

Panel access is for people. MCP gets its own read-only tokens, webhooks their own HMAC secret. None of them needs a Telegram session.

[Share panel access](https://phishdestroy.github.io/TgWitness/docs/access/) or [configure an MCP client](https://phishdestroy.github.io/TgWitness/docs/reference/mcp/).

## Hand over sources and conclusions

Put the report next to the signed ZIP. The report is your reading of the sources, the ZIP is what the recipient verifies.

[Export and verify](https://phishdestroy.github.io/TgWitness/docs/exports/) · [Work through a full investigation](https://phishdestroy.github.io/TgWitness/docs/cases/)
