# Investigate across all chats

Canonical page: https://phishdestroy.github.io/TgWitness/docs/cases/

Work an entire case across channels, groups, private chats and bots: collect, connect, reconstruct and hand over the evidence.

This walkthrough follows one fictional incident through a whole account. It uses the actual collection, search, people-profile and export features. The case map is a documentation example; your conclusions and case register are maintained outside the application.

WORKED CASE / A CHANGED PAYMENT DESTINATION

### One incident. Four conversations. A trail to reconstruct.

A channel announcement points to a bot. An operations group discusses a new payment link. A private follow-up repeats it. Later, the announcement is edited and a group message disappears.

Who posted each version?Where did the link appear?Which file was preserved?What changed, and when?

For history loading, optional AI source review, MCP, OCR and outgoing webhooks, see [Work the archive](https://phishdestroy.github.io/TgWitness/docs/archive/).

## 1. Establish coverage across the whole account

1. [Connect the collecting account](https://phishdestroy.github.io/TgWitness/docs/accounts/) in its own workspace. Record the case reference, account ID, workspace name and signing-key fingerprint in your case notes.
2. Open **Sources → Observation scope → Investigation mode**. Review **Whole account**, all four source types and **Own actions**. This preset enables saving a new source’s profile and its latest **200 visible messages**. Press **Save scope** and complete the scope confirmation.
3. Press **Load chats**. Compare the sources with the account’s dialog list and review exclusions. Under **Parameters → Chats read from the account’s list**, adjust the initial list limit if needed: the default is 1,000 dialogs, configurable up to 20,000. Chats beyond the limit are discovered when they become active.
4. In **Recording settings**, select and save **All visible activity**. Review attachment types, size limits and free disk space. Start observation and validate a controlled message, edit and deletion before relying on the setup.

ChannelsGroupsPrivate chatsBots

ONE ACCOUNT / ONE SIGNING KEY**All selected account-visible activity → one journal**

Messages · edits · deletion notices · visible reactions · membership events · own actions

“Whole account” covers the chats this account can access, with the configured source types and exclusions. Secret chats are unavailable. New dialogs are added as updates arrive; enabling this mode does not automatically download the complete old history of every existing chat.

## 2. Acquire history and preserve the files

Build a source register for the entire investigation. Give every chat a row with its numeric ID, title, account, access/role, live start, history acquisition, media result and known gaps. Mark a source as acquired only after checking the relevant result.

| Need | Action in the panel | What it provides |
| --- | --- | --- |
| History across enabled chats | Sources → Load full history | Current main: available past messages enter the workspace journal, with pause/resume and a signed progress report. [History guide](https://phishdestroy.github.io/TgWitness/docs/reference/history/). |
| Existing chat context in the journal | Sources → Recording settings → History snapshot | Recent visible messages as signed observations. Default maximum 500; **Parameters → Largest history snapshot** can raise it up to 10,000. |
| Complete currently visible history of one chat | Full chat export → Export full chat, or Chats → Export chat | A separate signed bundle with `chat.json` and `chat.html`. Repeat per source; retain completion/failure results. |
| Context when a new chat appears | Observation scope → When a new chat or bot appears | A source profile and up to 1,000 recent visible messages; Investigation mode selects 200. Existing chats do not receive this intake retroactively. |
| Attachment bytes | Download visible attachments + per-type limits | Check for `media.saved`, its SHA-256 and byte count. A queued, skipped or failed download is not a preserved file. |

A full chat export is a separate snapshot; it does not import its entire history into the journal or people profiles. Use **Load full history** across enabled sources, or bounded journal snapshots, for historical material you need to search inside TgWitness. Review the source list before starting the run.

In the worked case, acquire the announcement channel, operations group, bot conversation and private follow-up. Preserve the invoice attachment’s bytes and hash. History available today cannot reconstruct a message deleted before capture or an intermediate edit Telegram no longer returns.

## 3. Keep the evolving conversation and your own actions

Keep observation running as the case develops. Star the active case chats as priority sources; configure priority and other-source rechecks under **Recording settings → Recheck**. Review `recheck.completed`, continued catch-up, FloodWait and media outcomes as work progresses.

Use **Chats → Profile → Save profile now** to retain current source descriptions, bot commands and other metadata Telegram returns. This source profile is separate from the people profiles built from journal messages.

**Following a bot or invitation as part of the case**

1. In **Chats → Open Telegram link**, save the preview first. The original link and returned preview become signed records.
2. If the investigation calls for it, **Join / open and observe** joins or opens the source and starts a bot with its supplied start parameter. A pending join request remains pending in the record.
3. For an action you need to document, use the panel’s text reply or supported **Press button** control. The journal retains `interaction.requested` and `interaction.result`, including returned callback text or URL.

These controls perform real Telegram actions. A callback pressed in a different Telegram app is not visible to the collector; the bot’s subsequent message or edit may be. Web apps, payments and phone/location requests are outside the mini-client.

## 4. Follow people, links and files across chats

1. Open **Journal**, leave the source filter at **All sources** and search a distinctive phrase, domain, username or saved identifier. Open each matching record and record its chat, message ID and journal sequence number.
2. For a relevant chat, open **Chats → People → Turn on profiles**, then select a person. Review name/username history, reply relationships, activity, **Also in…** other observed chats and extracted links, wallets or phone numbers. Open the cited journal records.
3. Follow the same numeric Telegram user ID into other chats in this workspace. Treat a matching name, wallet mention or similar avatar as a lead to check. A mentioned address does not establish ownership; a similar avatar does not establish the same person.
4. Compare preserved attachment SHA-256 values across records. Equal hashes support byte identity of the saved files. Inspect the associated message and sender records before drawing a conclusion about who shared them.

CASE MAP / FOLLOW THE REFERENCESFictional case · not a live graph

CHANNEL / ANNOUNCEMENT**Original → edited destination**

Records #101, #188
Message #84 · sender not attributed

GROUP / OPERATIONS**User 71001 posts the new link**

Record #146 · message #309
Saved file receipt #151

BOT / ORDER CONVERSATION**A button points to that destination**

Record #173 · message #12
Returned button metadata

PRIVATE / FOLLOW-UP**User 71001 repeats the destination**

Record #205 · message #922
Saved file receipt #209

Four chats contribute different observations. Follow the source records for every connection; do not assign the channel post to user 71001 without an attributed sender.

The numeric IDs and record references are invented for this walkthrough. This map explains an analyst’s workflow using search, profiles and record inspection; the application does not generate a global investigation graph.

| Connection | Supporting observation | Conclusion to retain |
| --- | --- | --- |
| Same Telegram account | User ID 71001 in group #146 and private-chat #205 | The same supplied sender ID posted in both chats. Real-world identity remains a separate question. |
| Repeated destination | `pay.example.invalid/new` in #146, button metadata #173, edited post #188 and #205 | The same destination appears in four observed contexts. This alone does not establish who controls it. |
| Same file bytes | Equal full SHA-256 values in completed media receipts #151 and #209 | The two preserved attachments are byte-identical. File names or thumbnails alone would not establish this. |

People profiles cover authors with saved messages in that chat and relate them to other chats in the *same workspace journal*. They are not a complete membership directory. Avatar hashes come from a separate local cache; profile citations have a configurable limit under **Parameters → Records cited per fact**.

## 5. Reconstruct the sequence and mark the gaps

In **Chats**, inspect the saved versions and their **Journal record #…** links. In **Journal**, use **All sources** plus **Edits**, **Deletions** and **Coverage**. Build a case timeline with both the supplied Telegram date and the collector’s observation time.

1. 09:00 · #101**Channel post captured**

   The original destination is retained.
2. 09:12 · #146 / #151**Group introduces a different link**

   User 71001 posts it; an attachment download completes.
3. 09:16 · #173**Bot shows the same destination**

   The saved keyboard metadata carries the link.
4. 09:20 · #188**Channel announcement changes**

   The original and edited observations both remain.
5. 09:24 · #205 / #209**Private follow-up repeats it**

   The saved attachment has the same full SHA-256 as #151.
6. 09:28 · #231**Group deletion notice arrives**

   The earlier observation remains; neither the deleter nor an exact deletion time is supplied.

Illustrative observation times and references. Other journal records occur between these entries.

Journal sequence orders receipt, not necessarily the original Telegram actions. An older history snapshot can arrive after a newer live message. Keep live observations, snapshots, recovered messages, deletion notices and “missing on recheck” distinct. Add an explicit unknown interval wherever coverage shows a gap; a later snapshot does not erase that gap.

## 6. Extend the case to other collecting accounts

Add a workspace for each distinct account and repeat the scope and history inventory. Record the membership/role and signing-key fingerprint for each. Keep identifiers qualified by workspace and chat: the same message number is not a global cross-account identifier.

Compare relevant observations in your case notes or analysis tools, retaining the account and journal reference for each row. TgWitness does not currently provide one global search, merged timeline, people graph or case archive across workspaces. A multi-account full export of one channel or supergroup is a separate feature; it is not a merger of all account journals.

During longer work, add an [independent witness](https://phishdestroy.github.io/TgWitness/docs/witness/) to retain earlier boundaries. Use the controlled delivery pilot to qualify the accounts’ capture paths and visibility.

## 7. Deliver a complete, checkable case package

Export a signed journal ZIP from each workspace. It contains the full recorded journal regardless of panel search filters. Export relevant people profiles separately, retain each full chat-history bundle, and preserve the completed attachment evidence.

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

Keep trusted fingerprints through a separate channel. From a trusted installation, verify each artifact against its own workspace identity:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Check the actual verifier results, preserve the originals, and retain the coverage report, acquisition failures and transfer record with your findings. The top-level case folder and analyst conclusions are assembled externally; the individual TgWitness artifacts carry their own signatures.

## Use the same method for other investigations

**A bot-driven order or payment dispute**

**Question:** what did the bot promise, which button destination was supplied, and what changed afterwards?

**Trace:** channel entry post → saved bot-link preview → bot start parameter → messages and keyboard versions → any panel-issued callback receipt → group/private follow-up. Match each destination to its source record; retain profile descriptions and completed media.

**Deliver:** a timeline of the observed offer and responses, the source references and verified exports. A displayed payment link is not evidence that a payment occurred.

**Messages removed after a cross-chat incident**

**Question:** what had already been observed before relevant messages disappeared?

**Trace:** all affected chats → original messages → delivered edits → deletion notices or later missing-on-recheck results → preserved attachments → coverage around the incident. Compare independent account observations with their visibility stated.

**Deliver:** a sequence of preserved versions and explicit unknown intervals. Do not turn an absent history message into proof that a particular person deleted it.

**A participant changes names across several chats**

**Question:** which observed activity belongs to the same Telegram account despite changing names?

**Trace:** numeric sender ID → saved name/username history → replies → other chats in the workspace → mentioned destinations and saved files. Check source records for every asserted connection; keep look-alike accounts separate.

**Deliver:** a cited account-activity timeline and separate hypotheses about relationships. Name similarity and avatar pHash are leads, not identity proof.
