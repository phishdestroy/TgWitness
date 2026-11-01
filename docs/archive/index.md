# Work the archive

Canonical page: https://phishdestroy.github.io/TgWitness/docs/archive/

Find the message. Check the source. Build the case.

01**Bring in the history**

Load past messages from your enabled sources into the workspace.

02**Follow the sources**

Search the archive and open the saved message behind each result.

03**Keep the handoff clear**

Save your analysis separately and export the signed evidence beside it.

Captured records, recognized text and analyst conclusions stay distinct.

## Load past messages

1. Open **Sources → Chats in scope**, review the enabled chats and start observation.
2. Choose **Load full history**. The run uses the source list selected at that moment.
3. Use **Pause history** and **Continue history** as needed. After a restart, resume explicitly.
4. Check the per-source result and attachment queue. Save the signed progress report with the evidence export.

This fills the workspace with available messages. A per-chat HTML/JSON export is a separate operation. [History and recovery details](https://phishdestroy.github.io/TgWitness/docs/reference/history/).

## Search first, then decide about AI

1. Open **Journal** for local search. Choose a workspace and use the source and time filters.
2. Search a phrase or domain. Open the matching record and its saved versions.
3. For AI analysis, the administrator enables and configures a provider in **Integrations**. Open **Ask the archive** and choose chats and a period. Review **Data sent to the model** and uncheck unwanted excerpts before approving the request.
4. Check the returned citations. Save the answer as a report and add your own revision or notes.

Search runs locally without AI. Analytical reports keep source references and revision history; they are separate from the signed journal. [Provider setup and reports](https://phishdestroy.github.io/TgWitness/docs/reference/analysis/).

## Choose the connection you need

| Task | Open | Setup |
| --- | --- | --- |
| Read selected chats from an AI client | **Integrations → MCP** | [Install the MCP extra, issue a scoped token and connect the client](https://phishdestroy.github.io/TgWitness/docs/reference/mcp/) |
| Recognize text in saved media | A `media.saved` record → **Recognize attachment** | [Set up the local Docker worker and required language/model files](https://phishdestroy.github.io/TgWitness/docs/reference/media-analysis/) |
| Send events to n8n or a SIEM | **Integrations → Outgoing webhooks** | [Add a receiver, verify HMAC and deduplicate event IDs](https://phishdestroy.github.io/TgWitness/docs/reference/webhooks/) |

**Which access token goes where?**

Panel access is for people reviewing the case. MCP connections get separate read-only archive tokens. A webhook receiver uses its own HMAC secret. None needs a Telegram session file.

[Share panel access](https://phishdestroy.github.io/TgWitness/docs/access/) or [configure an MCP client](https://phishdestroy.github.io/TgWitness/docs/reference/mcp/).

## Hand over sources and conclusions

Keep the reviewed analytical report alongside the signed evidence ZIP. The report explains your reading of the sources; the ZIP lets a recipient check the saved record against an independently trusted fingerprint and checkpoint.

[Export and verify](https://phishdestroy.github.io/TgWitness/docs/exports/) · [Work through a full investigation](https://phishdestroy.github.io/TgWitness/docs/cases/)
