# Investigate across all chats

Canonical page: https://phishdestroy.github.io/TgWitness/docs/cases/

A whole case across channels, groups, private chats and bots: collect, connect the dots, rebuild the timeline, hand it over.

One made-up incident, start to finish. Collection, search and people profiles find the records, [Case Board](https://phishdestroy.github.io/TgWitness/docs/case-board/) organizes them, [Report studio](https://phishdestroy.github.io/TgWitness/docs/reports/) presents them.

WORKED CASE / A CHANGED PAYMENT DESTINATION

### One incident. Four conversations. A trail to reconstruct.

A channel post points to a bot. A group talks about a new payment link and the bot shows it. The post gets edited, a private chat repeats the link, a group message vanishes.

Who posted each version?Where did the link appear?Which file was preserved?What changed, and when?

History loading, AI, MCP, OCR and webhooks: [Work the archive](https://phishdestroy.github.io/TgWitness/docs/archive/).

## 1. Establish coverage across the whole account

Whole-account scope only on a dedicated account. A main account gets chosen chats or a folder.

1. [Connect the account](https://phishdestroy.github.io/TgWitness/docs/accounts/) in its own workspace. Note the case reference, account ID, workspace and key fingerprint.
2. **Sources → Observation scope → Investigation mode**: **Whole account**, all four source types, **Own actions**. Every new chat gets its profile and last **200 visible messages** saved. **Save scope** and confirm.
3. **Load chats** and compare with the account's chat list. The limit is 1,000 dialogs (up to 20,000 in **Parameters → Chats read from the account's list**); chats beyond it show up once they get active.
4. **Recording settings** → **All visible activity**, check attachment limits and disk space. Start, then test with a message, an edit and a deletion.

ChannelsGroupsPrivate chatsBots

ONE ACCOUNT / ONE SIGNING KEY**All selected account-visible activity → one journal**

Messages · edits · deletion notices · visible reactions · membership events · own actions

"Whole account" means every chat this account can open, minus exclusions. No secret chats. New chats join as they appear; old history isn't downloaded automatically.

## 2. Acquire history and preserve the files

Make a Case Board collection and bookmark what matters. Keep a source register: chat ID, title, account, role, start of live capture, history result, media result, gaps.

| Need | Action in the panel | What it provides |
| --- | --- | --- |
| History across enabled chats | Sources → Load full history | Available past messages enter the workspace journal, with pause/resume and a signed progress report. [History guide](https://phishdestroy.github.io/TgWitness/docs/reference/history/). |
| Existing chat context in the journal | Sources → Recording settings → History snapshot | Recent messages as signed records. 500 by default, up to 10,000 in **Parameters → Largest history snapshot**. |
| Complete currently visible history of one chat | Full chat export → Export full chat, or Chats → Export chat | A separate signed bundle with `chat.json` and `chat.html`, one per chat. |
| Context when a new chat appears | Observation scope → When a new chat or bot appears | Its profile and up to 1,000 recent messages (200 in Investigation mode). Not applied to existing chats. |
| Attachment bytes | Download visible attachments + per-type limits | Look for `media.saved` with SHA-256 and size. Queued, skipped or failed means not saved. |

A chat export doesn't go into the journal or people profiles. To search old history inside TgWitness, use **Load full history** or snapshots.

Here: the channel, the group, the bot chat and the private chat, plus the invoice file and its hash. What was deleted before capture is gone.

## 3. Keep the evolving conversation and your own actions

Keep it running. Star the hot chats as priority, tune rechecks in **Recording settings → Recheck**, and keep an eye on `recheck.completed`, FloodWait and media results.

**Chats → Profile → Save profile now** saves the chat's description, bot commands and other metadata.

**Following a bot or invitation as part of the case**

1. **Chats → Open Telegram link**, save the preview first. Link and preview become signed records.
2. If needed, **Join / open and observe** joins the chat or starts the bot with its start parameter.
3. To document an action, reply or **Press button** from the panel. You get `interaction.requested` and `interaction.result` with the bot's answer.

These are real actions. Buttons pressed in another app aren't visible, only the bot's reply. No web apps, payments or phone/location.

## 4. Follow people, links and files across chats

1. **Journal**, **All sources**, search a phrase, domain or username. Open hits and send them **To board**.
2. **Chats → People → Turn on profiles**, pick a person: name history, replies, activity, **Also in…**, links, wallets, phones. Open the cited records.
3. Follow the same numeric user ID into other chats. A matching name, wallet or avatar is a lead, not proof.
4. Compare file hashes. Same SHA-256 = same bytes. Who shared them is a separate question.

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

Four chats contribute different observations. Follow the source records for every connection; the channel post has no attributed sender.

The numeric IDs and record references are invented for this walkthrough. This explanatory map shows how to connect search results, profiles and inspected records; Case Board stores the corresponding cards and source references.

| Connection | Supporting observation | Conclusion to retain |
| --- | --- | --- |
| Same Telegram account | User ID 71001 in group #146 and private-chat #205 | Same sender ID in both chats. Who that is in real life is another question. |
| Repeated destination | `pay.example.invalid/new` in #146, button metadata #173, edited post #188 and #205 | Same link in four places. Who controls it needs other sources. |
| Same file bytes | Equal full SHA-256 values in completed media receipts #151 and #209 | Both files are byte-identical. |

Profiles only cover people who wrote something in *this workspace*, not a member list. Citations per fact: **Parameters → Records cited per fact**.

## 5. Reconstruct the sequence and mark the gaps

Versions in **Chats**, then **Journal** with **All sources** + **Edits**, **Deletions**, **Coverage**. Put both times in the timeline: Telegram's date and when it was observed.

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

Journal order is the order things arrived, not necessarily the order they happened. Keep live records, snapshots, recovered messages, deletions and "missing on recheck" apart, and mark every gap as unknown.

## 6. Extend the case to other collecting accounts

One workspace per account, same steps. Note each one's role and fingerprint. Message numbers are per account, so always say which workspace and chat.

An [account group](https://phishdestroy.github.io/TgWitness/docs/groups/) shows status, shares settings and exports everyone together, each with its own journal and key. A cross-account timeline you build in your notes.

Long case? Add an [independent witness](https://phishdestroy.github.io/TgWitness/docs/witness/), and test what each account actually catches.

## 7. Deliver a checkable case package

A signed ZIP from every workspace (always the full journal, filters don't matter), plus people profiles, chat exports and files.

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

Send fingerprints separately. Verify everything against its own workspace:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Keep the verifier output, originals, coverage and transfer record with your findings. Write it up in Report studio. If the recipient needs less, make a [minimized handover](https://phishdestroy.github.io/TgWitness/docs/handover/).
