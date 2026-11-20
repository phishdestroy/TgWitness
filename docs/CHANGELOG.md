[TgWitness](../README.md) / [Documentation](README.md) · [Project reference](README.md)

![Project reference](assets/presentation/chapter-project.svg)

# Changelog

<details>
<summary>On this page</summary>

- [Unreleased](#unreleased)
- [0.9.3 preview · 11 November 2026](#093-preview--11-november-2026)
- [0.9.2 preview · 10 November 2026](#092-preview--10-november-2026)
- [0.9.1 preview · 5 November 2026](#091-preview--5-november-2026)
- [0.9.0 preview · 4 November 2026](#090-preview--4-november-2026)
- [0.8.1 preview · 2 November 2026](#081-preview--2-november-2026)
- [0.8.0 preview · 2 November 2026](#080-preview--2-november-2026)
- [0.7.1 preview · 1 November 2026](#071-preview--1-november-2026)
- [0.7.0 preview · 31 October 2026](#070-preview--31-october-2026)
- [0.6.1 · 27 October 2026](#061--27-october-2026)
- [0.6.0 · 27 October 2026](#060--27-october-2026)
- [0.5.1 · 27 October 2026](#051--27-october-2026)
- [0.5.0 · 26 October 2026](#050--26-october-2026)

</details>

## Unreleased

- In the Telegram account settings on a phone, the Profile button, the account picture and the account ID no longer touch the controls next to them.
- A saved record whose reactions are malformed (a missing count, an entry that is not a reaction, or a value that is not a list) no longer stops a report from being built: the report lists the readable reactions and skips the rest.
- `verify.py` says "the archive has no manifest.sig, so its signature cannot be checked" for an archive without its signature file, instead of a `KeyError`.
- When a chat export stops because the free disk space is too low for its attachments, the panel gives the reason and the way out ("Not enough free disk space for the attachments of this export. Free space or turn attachment downloads off under Sources → Recording.") instead of "Export failed (ValueError)". The reason is in the export record as `message`.
- A message bubble in the viewer of an evidence report shows where a forwarded message came from ("Forwarded from Alex #5", the ID when no name was saved, or "a hidden sender") and its reactions as small chips, up to twelve per message.
- A card of the account export report names where a forwarded message came from ("Forwarded from …", with the channel post number, post author and date when Telegram gave them, or "Sender not available") and lists its reactions ("reactions: 👍 3").
- A card of the account export report shows where a text link really goes ("Link text “…” opens https://…") with a warning when the visible web address is not the target, and names the message a reply answers ("Reply to message #7"). Replies to another chat and forum topic roots are not named.
- The journal timeline names 40 more events in words, such as Chat details read, History reading started and Watchlist match, and any event without a name shows a readable title instead of its dotted code.
- In a channel or supergroup, clicking the message number in a chat bubble copies the Telegram link to that message (`https://t.me/c/<channel>/<message>`), which opens it for an account that is a member.
- A message made of one to three emoji is shown in a large size in the chat view, as in Telegram.
- While messages are being selected in a chat, the chat-wide Build report button is hidden, so the selection bar has the only Build report button.
- In the account export report a service message reads as a sentence on its card (for example "added a member", "changed the chat name to “…”", "pinned a message, number 42") instead of "No message text in this record." An action without a plain description shows "Service message" and its name.
- Each message bubble in the chat view shows its Telegram message number next to the time, so a reader can match it with the number search and with the gaps listed in a report.
- In the Ledger and margin PDF design, tables start at the body text instead of reaching into the margin where the chapter label stands.
- In the PDF report the headings of the activity charts always stay on the same page as their chart in every design.
- A wordy figure in an HTML report tile, such as "No observation period recorded", is set in a small font instead of the large number size.
- A saved attachment in the chat view shows its file name, type and size, and offers Preview only for images, audio and video.
- 146 more error messages from the panel's server side are translated into its 24 other languages, among them handover extracts, chat exports, the Case Board, documentation, watchlists, settings, storage, search records and report profiles. Before, the panel showed them in English whatever its language.
- On a phone, a table in an HTML report that scrolls sideways fades at its right edge instead of looking cut off.
- A rejected form shows its messages in the panel's language and in plain words ("This field is required.", "Enter at least 3 characters.", "Enter a date such as 2026-10-01 or a time with a timezone.", "Choose one of the allowed values.") instead of the server's English wording.
- `python -m tgwitness.download` says why a download failed: the panel refused the token, nothing answered at the address, the token file or output cannot be used, or the disk is full, instead of the exception name or "HTTP 401; redirects are not followed".
- Command line results show two labelled times: `observed` (when the collector saw the record) and, when Telegram reported one, `sent` for a message or `edited` for an edited version. A deletion notice has only the observation time. Before, one unlabelled time was printed. `--json` is unchanged.
- `tgwitness stats` lists only the hours and weekdays that have messages (`other hours 0`), says `no messages` for an empty selection, gives each sender's first and last message time, and uses the singular for one message or interval. A value that is not a whole number for `--chat`, `--limit`, `--message` and the like says so instead of `invalid identifier value`.
- `python -m tgwitness.file_hashes` and `python -m tgwitness.storage recover` name a file they cannot find or read instead of printing a traceback or the exception type.
- The MCP stdio bridge checks the token with the panel before it starts. A revoked, expired or wrong token, or an unreachable panel, ends it at once with a message that says why, where before the client saw only "Connection closed".
- The PDF of a handover extract prints the minimisation settings in words (period, chosen people, everyone else, message text, attachments, profile photos, masked contacts) as the HTML report does, instead of option names and `None` or `False`.
- The method text of **First-time posters per day** says that a person who first posts in several chats is counted once in each, so the daily figure can exceed the number of senders, and that the volume condition is "at most 1.5x" the median.
- A file in the **Media** tab without a message number no longer says "Message #null".
- A rejected form shows the field name without the request prefix (`purpose`, not `body.purpose`).
- A message sent through an inline bot shows "via bot ID" and a channel post shows its signed author under the sender line in the chat view.
- A poll, a location or venue, a contact and a dice roll now show what was shared in the chat view (question and answers, coordinates and place, name and phone, emoji and value) instead of an empty bubble with a missing-file icon, and the same text appears in the HTML and PDF reports. Minimised handovers still leave it out.
- Printing the HTML report no longer leaves a stray dot before a heading with no section number, and the **Exact figures** tables under the charts are opened for printing and closed again afterwards, so the paper copy shows the same figures as the screen.
- A sticker message in the chat view is labelled **Sticker** with its emoji as saved in the message record, also when the sticker file itself cannot be previewed. The HTML and PDF reports name the attachment **Sticker** and print the emoji in its details.
- In the Meridian, Atlas, Ledger and Horizon report designs a long figure label such as "No observation period recorded" wraps inside its tile, so the report no longer scrolls sideways on a phone.
- Searching inside a chat marks the matching words in the messages and shows how many messages were found, with a plus sign when more can be loaded.
- The pages of a live chat export print the question and answers of a poll, the coordinates of a location and the value of a dice roll next to its label.
- In the chat view, the service line for a renamed chat gives the new name and the line for a pinned message gives its number.
- Messages with a link preview show its site, title and host under the text in the chat view.
- Opening an address that is not part of the panel now shows a short page with links to the closest panel pages instead of raw JSON.
- A poll, a location or venue, a contact and a dice roll now show what was shared in the chat view (question and answers, coordinates and place, name and phone, emoji and value) instead of an empty bubble with a missing-file icon, and the same text appears in the HTML and PDF reports. Minimised handovers still leave it out.
- The panel compresses its scripts, styles, pages and `locale.js` with gzip when the browser accepts it. A first load of the panel in Russian drops from about 4.7 MB to 1.3 MB; API responses are not compressed.
- A sticker message in the chat view is labelled **Sticker** with its emoji as saved in the message record, also when the sticker file itself cannot be previewed.
- After **Verify journal** the result box is green only when a timestamp receipt covers the last record; with only the signed journal checked it is neutral, so the unfinished layers are not shown in a success colour.
- In the report preview, **Journal head** is a bordered row like the other sections instead of bare text pressed against them.
- On a phone the Signed archive card on Export records uses the same side padding as the cards below it, so headings and buttons line up.
- On a desktop pointer the star that marks a chat as priority no longer covers the time of the last message in the chat list; the time moves aside while the row is hovered or focused.
- Chat search accepts `#` and a message number to jump to that saved message. A **Pinned messages** list under the chat status shows what Telegram listed as pinned at the last chat-state check, with each saved message and a jump button, and says when a pinned number has no saved record. New route `GET /api/chats/{chat_id}/pinned`.
- In a report with a selection, **Selected data** names the chosen chats and authors as saved in the journal (for example `Alex Quinn (70002)`) instead of listing bare numbers; a number with no saved name stays a number.
- The chat panel has a **Media** tab with a gallery of the files saved from the chat, each linked to its message. Attachments that were not downloaded are not listed.
- In **Simple** mode Home shows one line, **Can be handed to a court: yes** or **no · missing: …**. Yes means
  timestamps are on with an RFC 3161 authority and that authority recently returned a timestamp that validated against
  its root certificate; the note gives how many of the saved records that timestamp covers, and each export asks for a
  new one for its last record. Otherwise the line names what is missing: timestamps turned off, no authority set, no
  validated timestamp yet, or no recent answer from the authority. The line also says that the recipient must confirm
  the signing key fingerprint received separately and run `verify.py` with `--tsa-ca` and the authority's root certificate, which the panel cannot do for them. A Bitcoin
  proof, a witness post and an attested collection run also satisfy the minimum in `verify.py`; the line does not
  count them. It is part of `GET /api/overview/live` as `court_readiness` and is translated into the 24 other
  languages.
- 48 panel error messages and two download parameter explanations are translated into the panel's 24 other
  languages, among them the Case Board, conversation plan, presence watch, storage, watchlist, translation and export
  errors. Before, the panel showed them in English whatever its language.
- The investigation record, action protocol, case package, certification of authenticity and undercover activity
  record are now fully translated into the panel's 24 other languages. Before, 141 of their headings, notes and
  explanations stayed in English, so a document made in another language mixed the two, including the declaration
  the declarant signs.
- Reports in other languages translate the sender name notes (**name at export**, **from the account's contacts**,
  **from the Telegram profile**) and the two auto-delete timer explanations, and **Investigation** translates step
  delays and durations of a day or more. Before, these stayed in English. Hindi, Urdu, Bengali and Persian durations
  in minutes and seconds now read as minutes (Hindi said "minimum"), and 15 Persian, Urdu and Bengali texts lost a
  stray leading space.
- The record details of an HTML report offer **Download file** for a saved attachment once the archive or its folder
  was chosen under **Check** and matched its signed manifest. The file is read from that archive, its SHA-256 is
  checked again and it is saved under its original name as a plain download, so the browser does not open it. Before
  the check the details point to **Check**; a missing or changed file is named as such. Before, a saved file other
  than an image could not be reached from the report.
- The panel saves an account export and its sharing copies under the name the server gives, the same name their
  verify commands point at. Before, the panel built the names itself, and an export made by a sealed capture was saved
  as `tgwitness-account-export-<id>.zip` while its commands named `account-export.zip`.
- README.txt of a sharing copy explains the copy and its verify commands in the copy's report language, followed by
  the English text, as the account export's README.txt does. Before, that part was in English only.
- On a narrow screen the report's network badge keeps a number and its unit together, as in "0 B sent".
- The `search`, `context`, `messages`, `stats` and `export` commands refuse a chat, message, sender or sequence number
  that does not fit in a signed 64-bit integer with a usage error naming the argument. Before, such a number stopped
  the command with a Python traceback from the database.
- An account export made by a sealed capture travels inside the evidence archive as `account-export.zip`, and its
  verify commands now name that file. Before, they named the panel download, `tgwitness-account-export-<id>.zip`, so a
  command copied as written ended in "file not found". A sharing copy of such an export names the same file for
  `--evidence`. The account export guide now shows the names the panel saves, `tgwitness-account-export-<id>.zip` and
  `tgwitness-disclosure-<id>.zip`, instead of `account-export.zip` and `minimized-disclosure.zip`.
- A chat ID, message cursor, record number or channel seed beyond SQLite's 64-bit integers is refused with a 422
  answer by the translation, QR code, mini application, channel graph, conversation plan and visibility requests, by
  the chat message, author, coverage, profile, scale and dossier requests, by journal records filtered by chat or
  message, by the pseudo-secret chat list and by the witness probe setting. Before, such a value reached the database
  and the request failed with an unexpected server error.
- **Sources** and the **Selected sources** card in the journal say **Observation paused** only after the operator
  paused observation from the panel or with `/pause` in the operator bot. Without an account they say **Telegram is not
  connected**, otherwise **Observation stopped**. Before, the journal card said paused on a profile with no account.
  **Sources** also names when the page last updated the status, and says since when it has not after a failed check.
- The chat header no longer shows the **What the other side sees** button where it has no chat to load, such as in
  the demo: there it was an unnamed eye icon that opened an empty menu. Before its settings load, the button is named
  **What the other side sees** once instead of twice.
- **Older records**, **Newer records** and **Latest** under the journal keep the keyboard focus after the next page
  loads, or pass it to the next pager button when there is no further page. Before, the pressed button was disabled
  while the page loaded and the focus fell to the page itself, so a screen reader lost its place. An error message
  no longer shows a line counting down: it stays until it is closed.
- The verify commands of an account export and of its sharing copy now name the file as it is delivered,
  `tgwitness-account-export-<id>.zip` and `tgwitness-disclosure-<id>.zip`, run from the extracted folder with that
  file one level up, as chat and evidence archives already do. Before, README.txt said `ORIGINAL.zip`, the HTML report
  `account-export.zip` or `disclosure.zip` with `--evidence original.zip`, and the download address sent yet another
  name, so a command copied as written ended in "file not found". The download address now sends the same names as
  the panel.
- Masking of possible secrets now also hides a Telegram bot token written right after `bot`, as in Bot API addresses
  (`https://api.telegram.org/bot<token>/sendMessage`). Before, only a token standing on its own was masked, so the
  token in such an address stayed readable wherever the panel masks secrets: chat list, messages and journal records.
- In a chat, a message without a recorded Telegram send time shows **By observation time** next to its time: its time,
  day divider and place in the feed come from when TgWitness observed it. Web addresses in message text
  (`http://`, `https://`, `www.`, `t.me/`) get a **Copy URL** button that copies the address without opening it; an
  address that runs into a masked secret gets none. On touch screens **Back**, **Select**, the message checkbox in
  select mode and the priority star in the chat list take taps over at least 44 × 44 px.
- **Sources** in the observation status no longer says that channels outside short polling always get rechecks. With
  rechecks off for them (**Other chats, every … minutes** or **Priority chats, every … minutes** set to 0) it says
  they get only pushed updates, and when rechecks are on for some of them it says for how many.
- Each card in **Prepared exports** names what the file holds: **Signed archive** with *Complete journal* and its
  record count, **Report**, **Journal records** or **Handover extract** with its chat and record counts, the case
  title and ID, and the report selection the file was built with (chats, chosen messages, dates, or *All chats* and
  *All dates*). **Show** narrows the list to one kind when it holds more than one. Files prepared before this change
  show their kind from the format and, for a signed archive, its record count. Before, a card showed only the format,
  *Plain file*, the date, the size and the SHA-256, so several HTML or ZIP files in a row could not be told apart.
- **Sources → Scope → Chosen chats** has a new switch, **Strict: read only the chosen chats**, off by default. While
  it is on, TgWitness does not read Telegram's service notifications (777000), the account's session list or its
  two-step verification status (at start, including the panel's check for other sessions with the **Evidence for
  a case** goal or an evidence protection mode, while observing, on connect or at stop), does not read earlier
  messages of a chat being turned on (the `baseline` snapshot, the new-chat read of a chat joined from the panel
  and the automatic last 100 messages of an empty chat opened in Chats), does not change the account's sensitive
  content setting and does not record phone call updates. Before, a chosen-chats workspace always did all of this,
  so reads could not be kept to the chosen chats. The chat list is still read at start to find them. Features you
  turn on yourself keep their reads: while this is the only session, the session list is still read every two
  minutes so that the end of that period is recorded, and **Telegram devices** reads it at each timestamp pass.
  Deletions are then matched to a session check only if one ran in the 10 minutes before. With an imported
  session key, chat and account exports use the regular session instead of Takeout until the session list is read,
  because the session's sign-in time is unknown (`session_age_unknown`).
- The workspace menu shows each workspace's full name, wrapping a long one onto a second line instead of cutting
  it with an ellipsis, and the name in the top bar carries the full name as its tooltip.
- A reply whose original is outside the loaded messages offers **show the original**: the panel loads the saved
  messages around it, highlights it and shows **Back to reply**, which returns to the reply. If the original is not
  saved in the workspace, the panel says so and suggests loading older history from Telegram. A chat reopened in the
  same session returns to where it was read, kept per workspace and chat and forgotten when the panel locks.
- In the self-contained report a message card with an attachment says **File saved** when the file is in the
  archive and otherwise why it is not, in words instead of a code: **Larger than the size limit**, **This file type
  was not collected**, **File not in this archive** and the other recorded reasons. The message time names the sent
  time in UTC and, for journal records, the time the collector saved it.
- A message with an attachment in an open chat says what happened to the file: **File saved**, **Queued** while the
  download waits, or the recorded reason it was not saved, such as **Larger than the size limit** or **Telegram did
  not provide the file**. A message whose file outcome is not recorded keeps the paper-clip mark. The time under a
  message names both times with the display time zone: **Sent** by Telegram and **Saved** by the collector.
- The journal's download button is named **Download entire journal (ZIP)** and asks first, naming the workspace
  and account, every source, the period up to the latest record with its time zone, the number of records and of
  saved files, and, when the list is filtered, that the filters and search do not apply. The account is named as in
  the workspace menu, followed by its @username and ID once each. **Choose records to
  export** next to it opens the export selection, with the journal's chosen source when there is one. The overview
  moved below the list, so search and filters come right after the page title.
- `verify.py` checks the ASiC-E layer of an evidence container the way the report's Check tab does.
  `META-INF/ASiCManifest.xml` must list every file of the archive with its SHA-256, an added
  `META-INF/ASiCManifestNNN.xml` or `META-INF/ASiCEvidenceRecordManifest.xml` must match the files it lists, and an
  entry under `META-INF/` that none of them covers fails the check with its name. The CAdES signatures are still not
  checked and are named as such. Before, `verify.py` reported an ASiC-E with a changed `ASiCManifest.xml` digest or an
  added `META-INF/notes.txt` as verified and only counted the container entries, while the Check tab called the same
  file damaged. When only the container is damaged, the Check tab now says that all files match the signed manifest
  but the ASiC-E container is damaged, instead of saying that the archive does not match its signed manifest.
- The first setup step shows the three goals as short cards with one line on what each gives (**Download once**,
  **Track changes**, **Collect case records**) and the full description of the chosen goal under them, so all three
  titles fit above the bottom buttons at 320 and 390 px. Before, the long descriptions pushed the third goal below
  the bottom bar on a phone, and a goal reached with Tab could sit under it.
- **Sources** no longer says **Observation paused** for a workspace without a Telegram account. The summary says
  **Telegram is not connected** with **Connect account** for an access that may open the account page, **Sign in
  again** when Telegram signed the account out, **Observation stopped** when an account is connected but nothing
  runs, and **Observation enabled · Reconnecting to Telegram** while recording waits for the connection.
- A report whose selection matched nothing says in its summary that no journal record matches the selection, and
  the summary says **No observation period recorded** instead of listing observed periods that do not exist. The
  cover says **Not recorded in this export** when the export carries no coverage data and keeps **0 records
  selected** for an empty selection in that case too, without claiming an empty list of periods.
- The **Observation period** on HTML and PDF report covers tells the cases apart: **No observation period recorded**
  when the journal has no continuous period, **0 records selected** when a selection matched no record (with both
  when both are true), and a duration only for actual periods. Before, a selection without records showed "—"
  and a journal without periods "Not recorded"; a selection never borrows the journal's duration.
- The account export form accepts account data without chats, for example only **Account profile**: it sends no
  chat types and no media types, and the summary reads **Account profile · no chats or attachments**. Before, it
  refused with "Choose at least one chat type." although the server builds and signs such an archive. A form with
  neither chats nor account data says "Choose a chat type or account data to export." at the chat types.
- The live journal stream of a workspace ends quietly when the workspace is deleted or the panel shuts down. Before,
  the open stream of a deleted workspace kept reading its closed database and wrote "Cannot operate on a closed
  database" errors to the server log after every deletion from the panel.
- The note next to the verify commands tells the recipient to put a renamed file's name in double quotes, so a
  browser copy such as `Telegram_Tips_2026-11-18_1 (1).zip` passes as one file name in Command Prompt, PowerShell
  and POSIX shells. The compact evidence README names the delivered file, and the report's **Check** tab offers
  `.asice` containers in its file picker.
- The Network topology heading moves its live status under the title when the screen is narrow. Before, a long title
  such as the German "Netzwerktopologie" pushed the page 2 pixels wider than a 390-pixel phone screen.
- Saving the signing checkpoint, the acquisition process receipt, the replica encryption key, the signed profiles
  of a chat and the witness configuration says **Download started. Check your browser's downloads.** when the file
  was handed to the browser, and **File saved.** only after a write through the file picker succeeded; the advice to
  keep a copy apart follows as its own sentence. Before, these said "downloaded" or "saved" even when the browser
  refused or cancelled the download.
- The report's Check tab keeps an evidence ASiC-E intact after external signatures or an evidence record were added to
  it. Each `META-INF/ASiCManifestNNN.xml` and `META-INF/ASiCEvidenceRecordManifest.xml` is checked against the SHA-256
  of the files it lists, and the signature or record it points to is named as not checked in the browser. Before, the
  signed copy of an ASiC-E failed with its added signature listed as outside the manifest, and the evidence record
  manifest was accepted without checking its hashes.
- **Export a chat by link** keeps a plan tied to the link it was made for. Editing, pasting or clearing the link
  removes the plan and its **Start export** button and says the link changed; a plan answer that arrives after the
  link was edited, another link was checked or the panel was locked is dropped. Before, the plan of the first chat
  stayed under a new link and **Start export** exported the first chat.
- The verify commands inside an export name the file it is delivered as: `tgwitness-evidence.asice` for an ASiC-E
  container, `tgwitness-evidence.zip` for the ZIP, and the chat's own archive name (for example
  `Telegram_Tips_2026-11-18_1.zip`) for a chat export, in README.txt, the HTML and PDF reports, the case assessment
  and the report's Check tab. Before, an ASiC-E and every chat export told the recipient to check
  `../tgwitness-evidence.zip` or `../tgwitness-chat-export.zip`, which did not exist, and the command failed. Next to
  the commands the reports now say to use the file's own name if the browser saved it under another one. Chat
  archive names keep letters, digits, `.`, `_` and `-` of any script and replace other characters with `_`, so the
  name can be pasted into a shell unquoted.
- A connected account with **Chosen chats** and no chat enabled is shown as **Connected · no chats chosen** on Home
  and in the top bar, in amber, with **Choose chats** on Home. Before, both said a green **Observing** although no
  conversation was being recorded. Home also says **Reconnecting** while the connection is down, as the top bar did.
- **Filters** above an open chat stays open, with the focus where it was, when the panel refreshes the chat status
  in the background. Before, it closed by itself within seconds. Choosing a filter, a view or another chat still
  closes it.
- A new investigation record asks **Which chats?** with **All chats** or **Chosen chats**; the chat list opens
  only for chosen chats and refuses to start with none ticked. Before, an empty list under "Only these chats (none
  selected: all chats)" silently meant every chat.
- When more channels are observed than short polling covers, channels of the priority class that does not fit
  take turns every 10 minutes instead of the same channels staying out, and Collector health → Sources names the
  channels outside short polling. Higher priority classes and the probe channel stay in. An access limited to some
  chats does not get these totals or names: they describe the whole workspace.
- The collection guide states which rule wins in folder mode: chats added by hand stay recorded outside the folder
  until they are excluded, removed or paused; chats the scope added are paused at the next recompute once they leave
  the folder.
- **Delete workspace** on the account page of an additional workspace is reachable before a Telegram account is
  connected. It sits in its own **Workspace** group, apart from signing out of Telegram and forgetting the session.
- Turning off a chat type in the scope applies to chats the scope added earlier at once: a new message of an
  automatically added group is no longer recorded after **Groups** is unchecked, even before the scope is recalculated
  or while Telegram cannot be reached. Chats chosen by hand keep their own rules.
- The same rule now holds outside new messages: until the scope is recalculated, a chat the scope added earlier
  and that a saved type, exclusion or switch to chosen chats no longer allows gets no history pass, new-chat
  history, peer-settings record, profile observation or record of the account's removal from it; a history pass
  already running stops at the next message. A chat the scope meets for the first time is decided on the scope
  saved when Telegram answers the lookup, not on the one read before it.
- A `scope.applied` record says whether the dialog list was read in that pass. When it could not be read or was not
  read, the record gives `dialog_list` (`unavailable` or `saved`), the size of the saved list as `saved_dialogs` and
  the error, and its coverage text no longer claims that all accessible dialogs were inspected. Before, a failed read
  was described as a full inspection and the size of the old list appeared as `dialogs_inspected`. Earlier records
  are unchanged.
- The journal's **Best match · word forms** search pages through more than 200 results: **Older records**, **Newer
  records** and **Latest** move between pages of 200 up to the search window of 1,000, and the footer names the
  results shown, such as “Results 201–400”. Before, only the first 200 results could be opened.
- Settings → **Which chats?** and the setup steps of a finished setup show the scope that is saved now, not the one
  chosen during setup. Marking the account as your main one in setup is refused while the workspace records more
  than chosen chats, except for a one-time copy with recording stopped; the message says to narrow the scope first.
- After a collector process that ended without an orderly stop, the next start checks every attachment recorded
  as saved during that run against its SHA-256. A missing or different file is recorded as
  `media.missing_after_restart`, its download is queued again and differing bytes are kept in `media-damaged/`.
- The **Check** tab of a report accepts the ASiC-E container it was delivered in. It recognizes the container from the
  exact `mimetype` text and `META-INF/ASiCManifest.xml`, checks the SHA-256 of every file that manifest lists, and
  says that the CAdES signature in `META-INF/signature.p7s` was not checked in the browser. Before, an intact ASiC-E
  got the red verdict **The archive does not match its signed manifest** because of its `mimetype` and `META-INF`
  entries. Any other entry under `META-INF/`, a file missing from either manifest or a changed file still fails.
- Deleting a workspace first shows the format, size, preparation time and SHA-256 of its last downloaded signed
  archive and asks to confirm that this archive is saved outside the workspace. The server refuses the deletion
  without that confirmation.
- The Telegram Desktop JSON of an account export with contacts adds `frequent_contacts`: each frequent
  correspondent, inline bot and call partner from the saved top-peer pages with its ID, category, chat type, name and
  rating. These pages stay out of `contacts.list`.
- The tab row of **Sources** scrolls inside itself when it does not fit, at any width. At 200% browser zoom it used to
  push the page about 60 px wider than the window for a moment while the screen loaded.
- A chat that the scope added automatically stays paused after the operator pauses it from the source list. Before,
  the next scope recalculation — on a source-list refresh, at start or in the background — turned it back on in the
  whole-account mode and reported it as resumed. **Resume** releases the pause and the scope rules apply again;
  exclusions and the automatic adding and pausing of other chats work as before. Chats paused before this version
  cannot be told apart from chats paused by the scope and keep the earlier behaviour until they are paused again.
- **Network topology** keeps the names **Traffic**, **Ports**, **Threats** and **Addresses** for screen readers at
  700 px and narrower, where only their icons show. Closing a node card with its button or Escape returns the focus to
  the node that opened it, or to the first node if that one is gone. The light-theme status badge is darker:
  **Live** went from about 3.3:1 to 4.7:1 and the stale or demo state from 4.4:1 to 6.2:1.
- **Home** keeps the keyboard focus on the same button, for example **Add account**, when it refreshes itself every few
  seconds. Before, the refresh rebuilt the page and dropped the focus to the document after about five seconds.
  Focus that the user moved elsewhere in the meantime stays where it is.
- The record viewer of a report no longer adds a record that the filters hide. When new filters leave out the record
  whose card is open, the card closes; **Select** in a card works only for a shown record, while records chosen
  before the filters changed stay selected. **Go to #** opens exactly the number typed and otherwise says whether
  that record is not in the report or hidden by the filters; before, typing #2 in a report with only #1 highlighted
  #1. **Copy text** copies the message text, a system record offers **Copy description** for the description it
  shows, and a record with neither says **No text to copy**; before, the button wrote an empty clipboard.
- The connection form takes an explicit port 80 from a pasted HTTP proxy URL. The browser drops a default port, so
  `http://host:80` used to leave the previous port, for example 8080, in the form with no message; an address that
  cannot be used now clears the prepared plan and keeps its error visible after the field loses focus. With
  **Public MTProto** the external-requests box shows what is sent — off — instead of a checked, disabled box, and the
  earlier choice comes back when another route is chosen.
- A deletion notice no longer leads to the statement that this account did not delete the message. Telegram's
  notice names no one, and the rights and session checks it was compared with can be up to 24 hours and 10 minutes
  old. New records keep the deleting account unknown with the attribution `not_named` and state the last rights or
  session check with its age; reports and the panel word older `peer_or_admin` records the same way.
- The public showcase manager follows the theme chosen in the panel; before, it followed only the system theme. A
  capture export over its verifier's limits (512 MiB per file, 8 GiB in total, 100,000 entries) stops before the ZIP
  is written and names the limit, instead of writing the whole archive and then reporting a failed verification. The
  pseudo-secret description no longer says that every file is saved: a file waits while downloads are off or its
  size or free disk space stops it, and each deferred or failed download is recorded.
- Undoing an entry in **Recent changes** brings back only the settings that entry changed. Before, it brought back
  every setting saved with the entry, so a later change of another setting was reverted as well, a custom file rule
  made in Sources was replaced, and observation started from the main screen could stop. When a later change touched
  the same settings, the undo is refused and nothing changes. An undo now names its journal record by number and hash,
  and after a workspace switch Settings no longer lists or undoes the previous workspace's changes. A settings edit or
  its undo is no longer refused because timestamps were on while requests outside Telegram were off, as in a new
  workspace before a goal is chosen. The Sources recording form keeps a media type's own action, such as hashes only or
  exclude, where any save used to drop it, and no longer shows unsaved changes right after loading. An unchecked proxy
  address stays in the connection form when the server address question or another setting there changes, and focus
  stays on that question. Finishing a first setup opened again from Settings says that nothing new was started and
  opens Exports or Home, instead of showing the recording check as done. The administrator key reissue confirmation is
  titled with the operation and announces its warning, and a cancelled confirmation returns focus to the button that
  opened it.
- Panel states and keyboard use from the external review. **Settings → Which chats?** shows the scope in use, the
  number of chats being recorded and whether they are observed, with a green dot only while they are, and follows a
  saved chat selection and the recording state while Settings is open; before, it showed the first-setup draft, such
  as **Choose chats · 0**, always with a green dot. The protection mode dialog and the **Protection level** card no
  longer promise to hide or show sections where the interface level decides what the panel shows, which is every real
  workspace, and with no mode chosen the switcher next to the version number reads **Not chosen** instead of **All
  sections**; new `workspace.mode_changed` records no longer carry `shown` and `hidden` lists of sections the panel
  did not actually hide; earlier records are unchanged. On a phone, an empty Chats page keeps the chat list with its
  search and **Add** menu in view when the account is connected and the access can choose chats, open a Telegram link
  or start a pseudo-secret chat, instead of covering it with a page that had no way back to the list. A journal row is
  no longer a button with the bookmark button inside it: each row has its own open button of at least 24 × 24 px next
  to the bookmark button, and only the buttons of the selected row are in the Tab order, matching the arrow keys.
- A timestamp pass in the journal is named by its outcome. When no service answered and no earlier answer covers
  the checkpoint, the record reads **Checkpoint not timestamped** and is marked as a coverage problem; when only
  OpenTimestamps calendars accepted it, **Checkpoint timestamp pending**; **Checkpoint timestamped** stays for a
  time-stamping authority answer. When every service failed for the same reason, the description names it — for
  example that requests outside Telegram are turned off. Before, a pass where 0 of 7 services answered was titled
  **Checkpoint timestamped**. The signed records are unchanged.
- In the chat search, choosing a row no longer changes anything by itself. A chat of the account is added only with
  **Observe**; a public chat found by **Global search** is joined only with **Join / open and observe**, which asks
  for the usual confirmation; its name opens the link preview instead. `j` / `k` move through saved chats only, and
  arrow keys from the search field reach each new row's own button. In an open chat, Ctrl+F (⌘F) puts the cursor in
  **Search saved messages**; pressed there again it reaches the browser's page search. Before, clicking the name of a
  search result added the chat to observation or started the join.
- An export that is not kept for another download, such as a file over 2 GiB, no longer sends a browser without
  file streaming to a repeat download that fails. The panel learns from the response that no saved copy exists and
  names Chrome or Edge and the command-line download instead. In such a browser the signed archive card says so
  before the download, and the Prepared exports note no longer promises to keep the latest file whatever its size.
- A timestamped evidence export counts for workspace deletion only the Case Board notes it carries: both come from
  the time-stamped `checkpoint-N.json` of the sealed record. Before, when that checkpoint had been saved earlier at the
  same record, for example when observation stopped, notes added afterwards were left out of the archive but counted
  as exported, so **Delete** became available without them; they now keep it unavailable until an export carries
  them. The manifest's `boundary.chosen_at` is the moment this export fixed its last record instead of the time the
  checkpoint was first saved, so `verify.py --witness` again reports a witness that saw more records in between as a
  conflict. A sealed export whose checkpoint file is missing or names another record now fails instead of pairing
  the sealed records with the newest notes.
- A minimised handover keeps only the fields listed for each kind of account-wide service record. A
  `coverage.gap` for a live probe acknowledged late no longer names the probe chat, its probe and acknowledgement
  message numbers or the witness account when that chat is outside the selection; in a selected probe chat the
  witness account is replaced by its pseudonym, as message senders are. A field these records do not normally carry
  is withheld, and the record is marked minimised. Before, these records went into the handover whole unless they
  held a known chat list.
- Choosing account files or pasting session text under **Files** no longer sends them to the TgWitness server. The
  form says where they go, and the server reads them only after **Check files** or **Read files without signing in**;
  **Connect account** follows a successful check as before. Before, choosing files sent them at once and each
  character typed into the TData passcode or session text, or a changed API pair, sent them again. The check also
  shows the user ID the files state. Pasting session text now clears the selected files, so the check and the
  connection use the latest choice; before, a file chosen earlier replaced the pasted session when connecting.
  **Auth key** with **Create an independent authorization** now reaches the independent login on an attested
  deployment instead of being refused there as a reused key.
- Reports: the **Observation period** figure of HTML and PDF evidence reports and handover extracts adds up the
  continuous observation periods listed under Coverage and reads "Not recorded" when there are none, and the first
  custody step is named "Recorded in the journal". In a report limited to selected records, the figure counts
  observation between the first and the last selected record; a handover extract adds up the periods of its
  Coverage section, which are not cut to the extract's period. Before, the figure showed the time from the first to
  the last record of any kind, or of the selected records: a journal of local service records showed "10 min", and a
  three-day pause between two runs counted as observation. The Traditional Chinese "Not recorded" uses traditional
  characters. `verify.py --plain` and the Verifier summary of HTML and PDF reports say "No observation period
  recorded." whenever there is none; before, a session-key, gap or record-source line hid it. In a chat
  export page of the reading designs, a reply to a message in another chat says so instead of quoting the message
  with the same number in this chat. The status words and labels of the evidence conditions table use the colours of
  the report theme, at least 4.5:1, instead of fixed greys and green of 2.8–4.2:1. Verification commands name the
  file they are in: `report.en.pdf` and `chat.en.pdf` instead of `report.pdf` and `chat.pdf`, a PDF saved on its own
  `tgwitness-report.pdf` and an HTML report saved on its own `tgwitness-evidence.html`, as the panel names them on
  the first download; a copy downloaded again from the export history is still named
  `tgwitness-<profile>-<export>.pdf` or `.html`. A password-protected PDF or JSON report holds the file under the
  same name, `tgwitness-report.pdf` or `tgwitness-report.json`, instead of `tgwitness-evidence.pdf` or `.json`. The
  case assessment of a chat export points to `../tgwitness-chat-export.zip`, like its Verify section.
- The panel says that a chat export, handover, account archive, disclosure, group export or flight record was saved
  only after it wrote the file through the browser's save picker. When it hands the file to the browser's downloads it
  says that the download started, and the chat export keeps **Download signed bundle**. Before, it reported
  "downloaded" or "saved" as soon as the browser took the file, also when its save dialog was then cancelled, and hid
  the chat export's button. The Storage panel now lists the local files kept in `storage-conflicts/` because their
  bytes differed from the signed journal hash, `python -m tgwitness.storage recover` prints each with both hashes and
  its path, and a full evidence export asks to restore such a file first; before, the conflict was only a journal
  record and the export failed with a general error. `python -m tgwitness.storage recover` runs again; since the
  storage module became a package it stopped with "No module named tgwitness.storage.__main__". On Windows an
  attachment, a decrypted secret-chat file and a file restored from storage are renamed into `media/` with
  `MoveFileExW` write-through, which Windows documents as returning once the move is on disk; secret-chat and restored
  files are now also flushed, with the folder entry on Linux and macOS, before they are recorded. Before, Windows
  renamed them without a flush, and secret-chat and restored files were not flushed at all.
- Case Board: with **Replace investigator names with R01, R02…**, a handover now also gives a pseudonym to an
  investigator mentioned in a comment who wrote nothing on the board; before, the inserted @name stayed in the
  comment. In the quoted message of a highlight names are replaced as whole words only, so a short name such as "Al"
  no longer changes "Totally" or "legal" there; in notes and comments every occurrence is still replaced. **Add to
  board** in the bookmark options lists only collections that can hold the record, and after a refused move it moves
  the card it already added instead of adding a second one. Text and mentions typed into a comment while it is being
  posted stay in the editor instead of being cleared. A note, comment or
  status that was saved is no longer reported as failed when only the following board refresh fails, so trying again
  no longer adds it twice.
- **Save chat selection** in Settings and at the end of first setup keep the source types, excluded chats, own
  actions and new-chat settings of Sources → Scope, take a chosen chat off the excluded chats and keep it as a
  hand-picked source. Before, they replaced the whole scope with defaults, so a previously excluded chat or private
  chats could be added again and own messages recorded again, and a chosen chat that the scope had added was paused
  on the next application. Saving a chosen-chats scope while observing no longer rereads the account's chat list,
  and saving the same scope again after a failed application applies it again instead of reporting success without
  applying.
- Very small photos are saved again. When a photo's largest image was smaller than the estimate for its blurred
  preview, about 1 KB, TgWitness expected the preview's size and discarded the downloaded image because its size
  differed. The expected size and the size estimates for exports and storage now come from the image that is
  downloaded.
- The link preview of a public channel or group by username says whether the account is already a member, from
  Telegram's `left` flag, and offers **Join / open** instead of **Send join request** to a member of a group that
  approves new members. The result of **Join / open** records `already_member` when the account was already in the
  chat, and the panel says so. Before, `already_member` was empty for usernames and a successful receipt did not tell
  a new join from an existing membership.
- Joining a chat from the Chats page no longer reports success when Telegram first asks for a check in a bot's mini
  app. The action is recorded as not accepted, with the bot ID, and the chat is not added to observation. The chat
  taken from an invite join now comes from Telegram's answer, without another invite check.
- An action that stops after it was sent now shows its reason in the panel and keeps it in the result record, instead
  of the error type alone.
- The interactive report names mini application and pseudo-secret records in the report language instead of showing
  the internal record type.
- Five fixes from the external review of 0.9.3, checked on RunPod before and after:
  printing a selection of records prints only the selection sheet, not the full dossier with its cover and the hashes
  of unselected records; the signed acquisition method, report title and summary follow what the journal holds — a
  journal of local service records is no longer described as Telegram observations of an account, and old records
  without enough detail get a neutral journal description; the signature badge in the brief and activity documents
  opens their existing **Seal** section instead of a missing `#check`; changing the panel language on the sign-in
  choice keeps **Files**, **Key** or **QR** and the independent-authorization choice instead of falling back to
  **Phone**; the journal keeps its pause and resume control for live updates at 320 and 390 px.
- On a workspace set up for the main account, a folder or whole-account scope is refused when it is saved from
  Sources or Investigation while observation runs or is set to resume, as it already was at start and in setup.
  Before, it could be saved during recording and then made the next start fail.

- **Join / open** on a public channel or group found by the chat search now joins it in one step: the panel takes the
  preview, asks for the usual action confirmation, joins, adds the chat to sources and opens it. Bots and people
  open the link preview, which says that opening a bot sends `/start`. Member counts follow the panel language.
- An access without the account or sources permission no longer sees **Connect account** or **Choose chats** on an
  empty chat list, which led back to Chats; it reads that the workspace administrator connects the account or
  chooses the chats this access can read.
- The setup goals describe timestamps as they work: each record is signed when it is saved, journal checkpoints are
  sent for independent timestamps at intervals, and an archive carries a timestamp only when a service answered.
  Before, **Evidence for a case** said it confirms each record as it is written with independent timestamps.
- Narrowing the observation scope takes effect at once: an excluded chat, and a chat added by a wider scope after
  switching to selected chats, are no longer recorded while the scope is being applied, and their sources are paused
  even when Telegram's dialog list cannot be read; `scope.applied` then names the failed refresh. Before, a failed
  dialog request left the old sources enabled and recording.

- The chat search on **Chats** now searches Telegram itself, as the Telegram app does. Under the saved chats and the
  account's own chats it lists **Global search**: chats the account is in and public channels, groups, bots and people
  found by name or username through `contacts.search` (`GET /api/telegram-search`, permission `sources`). A chat the
  account is in is added with **Add**; a public chat it is not in opens the link preview with **Join / open** and
  **Observe**. Before, the search only filtered the account's existing chat list, so typing the name of a group the
  account had not joined found nothing.
- On screens up to 767 px, opening a chat from the keyboard moves the focus to **Chats** (back) in the open
  conversation, and going back returns it to that chat's row. Before, the focus stayed on the hidden list and
  going back focused the search field.
- The multi-account export period uses the panel's time zone, the one the journal is shown in, for custom dates and
  the previous calendar month, and the dialog shows the resulting UTC bounds with the end marked as excluded. Before,
  the form converted through the device's time zone, so a time copied from the journal could select a different
  range.

- An evidence export downloaded in the panel counts for workspace deletion only after the panel has received and
  saved every byte and confirmed it with `POST /api/exports/{id}/received`. Before, the server counted the download
  when it had sent the last byte; Linux kept a whole 1.6 MB archive in its socket buffer, so a download broken off
  after 7 KB was still counted and **Delete** became available. Downloads the browser makes on its own and other HTTP
  clients still count when the server has sent the whole response; the operations guide says what that cannot see.
- A minimised handover keeps only the selected chats in the observed-chat list of `process.started`. Before, every
  start record carried the ID, title and type of each observed chat into the handover, so a handover of one chat
  named all the others.
- A standalone HTML report saved without its records (over 20,000 records or 32 MiB) fills its Check tab, also when
  opened at `#check`: the seal result, an explanation that the data is not embedded and the archive check. Before,
  the tab stayed empty.
- START_HERE.txt in every verifier language no longer says that RFC 3161 checks need OpenSSL: verify.py checks the
  time stamp itself with `--tsa-ca`, and OpenSSL is needed only for the optional manual `openssl ts` command.
- The translation notice on report covers and in README.txt says that a non-English version is a machine
  translation of the English original named next to it, with message texts as captured, and leaves the filing
  language and certified translation to the court's rules. Before, the Russian notice read as an obligation to file
  the English original.
- Ctrl+S (Cmd+S) saves only a form inside the open dialog or panel; with the command palette or another modal open it
  saves nothing. Before, pressing it in the palette saved the changed report settings behind it.
- The command palette lists **Investigation** by name and opens its panel. Before, it showed an unnamed entry whose
  selection raised a JavaScript error; entries now open only sections that exist.
- Report Studio explains verification per format: the HTML seal covers every byte and is checked in the report or
  with verify.py; the JSON seal covers the report's canonical content, not its formatting; the PDF also carries a PDF
  signature; the exact bytes of a delivered file are compared by SHA-256 with the receipt or signed manifest. Before,
  one sentence said every report's seal covers all of its bytes and can be checked by dropping it onto the report.
- **Verify journal** no longer promises the next timestamp and asks to turn on Evidence mode at the same time. With
  timestamps on and no receipt yet it says it is waiting for the service, or that requests outside Telegram are
  turned off so no timestamp can be requested, and the summary reads "Integrity only until a timestamp receipt covers
  the last record". `/api/verify` adds `conditions.timestamp_state`.
- Escape closes the command palette first when it was opened from the mobile menu, returning the focus to **Go to…**;
  the next Escape closes the menu. Before, the first Escape closed the menu under the palette and the focus was lost
  after the second.
- The **Accounts** advice about public MTProxy servers counts only workspaces with a signed-in Telegram account. Before,
  a new workspace that had never signed in was counted as "1 account uses public MTProxy servers" because public
  MTProxy is its default route; the route is still shown on its card.
- The showcase publishing page follows the panel language, including the content consent, the preview labels, the
  link and revoke messages and the page's `lang`; message texts stay as captured. Before, it was English only, also
  after choosing Russian in the panel.

- A downloaded or reused attachment is flushed to disk before it is renamed into the media folder, and on Linux and
  macOS the folder entry is flushed too, before `media.saved` is written. Before, a power loss right after the record
  could leave the journal naming a file whose bytes were never written.
- A timestamped evidence ZIP with Case Board notes passes `verify.py` when records or notes arrive while the export
  waits for the time stamp. The board statement, its slices and the report's board section now use the sealed record
  and the notes that existed when it was sealed; before, the board named the newest record of the workspace and the
  verifier refused the archive with "Case Board journal boundary mismatch". Notes added after the seal go into the
  next export.
- Checkpoints retained at the same time by an export and the periodic task no longer fail or publish an older head:
  saving a checkpoint is serialized per workspace and `checkpoints/latest.json` never moves back to a smaller record
  number. Private files are written through a unique temporary file instead of a shared `NAME.tmp`, so two writers
  of one file no longer truncate or remove each other's temporary copy.
- An evidence export with only OpenTimestamps calendars configured is sealed at the checkpoint the calendar answered
  for, as it is with an RFC 3161 reply. Before, the export ignored the `.ots` proof and reported that no timestamp
  authority answered. The response names what covers the sealed record in `X-TgWitness-Seal` (`rfc3161`,
  `opentimestamps-pending`, `opentimestamps-bitcoin-unverified`) or the reason the export was not sealed.
- `verify.py --witness` no longer reports a conflict when the witness saw a longer journal after a timestamped export
  had fixed its last record but before packaging started. The evidence manifest records `boundary` (record count, the
  moment it was chosen and whether it came from the snapshot or the sealed checkpoint); for older archives the
  sealed checkpoint of the last record is used when the archive carries it. A witness that saw more records before
  that moment, or a different hash for the same record, is still a conflict.
- Importing a storage recovery file checks each local attachment by size and SHA-256 instead of by its name, and
  **Restore all files** restores the verified copy over a local file with different bytes after moving those bytes
  unchanged to `storage-conflicts/` (`storage.local_conflict`). Before, a damaged local file with the expected name
  was treated as present and the restore reported 0 files.
- With more than 50 selected channels, the short update poll takes the probe channel and priority sources first.
  Before, priority 0 and 1 sorted alike, so the first 50 channels by title were polled and a priority source or the
  probe channel later in the alphabet could be left out.
- The Telegram Desktop JSON of an account export lists only contacts in `contacts.list`. Before, each saved page of
  frequent correspondents (`top_peers`) added an empty contact entry. The top-peer pages stay in the export's signed
  data files.
- An account export keeps the SHA-256 and size of the additional Takeout JSON as Telegram sent it
  (`received_sha256`, `received_bytes`) next to those of the saved file, with the rule that removed secret fields
  (`transformation`). Before, only the sanitized copy was described, so the receipt could not be compared with an
  original obtained separately.
- Analyzer insights (`/api/analyzer/insights`, format `tgwitness-insights-v2`) count deletion notices that removed
  several messages as `deletion_batches` and list suspected history clears separately as `suspected_history_clears`,
  each with the conditions and meaning of its `history.cleared_by_peer_suspected` record. Before,
  `cleared_histories` counted every `deletion.batch`, so an ordinary deletion of two messages read as a cleared
  history; that field is removed.
- `start.py` and the Windows portable builder install `deploy/requirements.lock` with `--no-build-isolation`, as the
  Dockerfile does: source-only packages build with the setuptools pinned in `deploy/build.lock` instead of a build
  environment pip resolves on its own.
- A reply to a message in another chat no longer quotes the message with the same number in the open chat: the
  chat view reads the replied chat from the saved Telegram record and shows "Reply to #N in another chat". Messages
  saved earlier are read the same way. The Telegram Desktop JSON of an account export adds `reply_to_peer_id` for
  such replies.
- An open panel follows changes to its access: `/api/status` carries the access's current permissions, and the panel
  updates its views and actions when they change. Before, a granted or removed export permission showed only after
  the page was reloaded; the server already checked each request against the current permissions.
- Verification commands in HTML and PDF reports, their case assessment and the report viewer's Check tab use
  `TRUSTED_SHA256` instead of the fingerprint carried by the report itself, so a copied command no longer compares the
  archive with its own key. Inside an archive they name the original ZIP as `../tgwitness-evidence.zip`, as README.txt
  does, and the HTML says to run them from the extracted folder; before, the HTML command failed there with
  FileNotFoundError.
- **Choose the ZIP** and **Choose the folder** on a report's Check tab are buttons reachable with Tab and opened
  with Enter or Space; before, they were labels around hidden file fields and the keyboard skipped them.
- With **Show selected** on, unselecting a record in a report's Records tab removes it from the list and the count at
  once, and moves the focus to the next selected record or to the filter; before, the row and "1 of 3" stayed until
  the search changed.
- When a report's Records tab shows nothing only because the matching records are in categories hidden by default
  (for example System), the empty list says how many records and which categories, with **Show these categories**.
  Before, an archive of three system records opened on "0 of 3 · Nothing matches these filters".

- A workspace can be deleted after its evidence ZIP was downloaded. The export seals the journal up to a record and
  then writes the timestamp of that seal as a later record, which the deletion check counted as not exported, so
  every export left a new blocking record. Timestamp and evidence-record entries no longer block deletion; observed
  records written after the last export still do.
- A deletion notice that arrives after the admin log poll which already returned the deletion is linked to that
  admin log entry (`message.deletion_attributed`) when the notice is recorded. Before, the link was made only when
  the notice came first; the poll cursor had moved on, so the acting account was never named for that message.
- A sign-in by phone or QR that the workspace refuses after Telegram accepted it, for example because the account
  already belongs to another workspace, now signs out of the new session. Before, the session stayed in Telegram's
  device list with its key discarded. Imported sessions are not signed out.
- The pseudo-secret conversation section of an HTML, JSON or PDF report and its Report Studio preview follow the
  report's dates, event types and senders. Before, a selected pseudo-secret chat showed every message, file and
  notice of that chat, including texts the filters left out of the rest of the report.
- A minimised handover withholds chats outside its selection from `scope.changed` (`before` and `after` exclusion
  lists), from an account-wide `coverage.gap` for a full startup buffer (chat IDs and message ID ranges) and from
  `recheck.completed`; the totals of those records are recounted for the chats kept. Before, these records were
  passed whole or with their nested chat lists.
- Downloading a finished or in-progress chat export checks the access again just before the file is sent, as the
  full export already did: a token revoked, an export permission removed or the chat taken out of the access while
  the archive was prepared stops the download and removes the temporary copy.
- Deleting an additional workspace requires a signed ZIP or ASiC-E container that was downloaded in full and covers
  both the journal and the Case Board notes. Before, the export was counted when the server had prepared it, even if
  the download then broke off, and notes added after the export did not keep **Delete** unavailable. A completed
  download from **Prepared exports** or of a group export also counts. A workspace that already has notes needs one
  new complete export before it can be deleted.
- `verify.py --interactive --require evidence|attested` applies the required profile and exits 2 when it is not
  reached, as the direct command does; before, the interactive run dropped `--require` and could exit 0.
  `--compare` refuses `--require` before reading the archives instead of ignoring it.
- The verifier marks an RFC 3161 time stamp as a qualified eIDAS time stamp only when the certificate that signed it
  is the listed qualified unit; before, any qualified certificate carried in the token was enough. The external time
  line of a qualified stamp now shows that stamp's own time instead of the earliest time of all sources, and the
  `qualified` entry names the signer certificate's SHA-256.
- A report on selected chats, senders or messages keeps the saved files of the selected messages: the cover and
  summary counted 0 files and left out the `media.saved` records, because the selection keeps only message records.
  **Activity by chat** names chats by title and ID, as the chat timeline does, instead of "Chat -100…".
- Previewing an invite link records the chat as a channel or supergroup when the invite says so; before, every invite
  to a chat the account had not joined was recorded as a group in `interaction.preview`.
- Ending other sessions while keeping the one that approved the QR sign-in is recorded even when Telegram stops it
  part way, for example with a FloodWait: the record counts the sessions already ended and names the refusal.
  Before, those sessions ended without a journal record. The verifier no longer reads such a run as "All other
  sessions ended": it states how many were ended and that the approving session was kept.
- A profile or privacy change that Telegram stops part way is recorded with what it already changed: a new name
  saved before the username was refused, or the privacy settings applied before a FloodWait. Before, the account
  changed without a journal record.
- A new workspace's connection screen no longer names two routes at once: until the account signs in, the route bar
  reads "Chosen at sign-in" and **What Telegram sees** follows the route picked in the sign-in form, instead of the
  public MTProxy default the form replaces. The route bar updates when the route changes, for example after signing
  in through WARP; before, it kept "Public MTProxy" until the page was reopened.
- Account table headers fit their columns in every panel language (Sources, Events and Queue overflowed into each
  other in Russian, Ukrainian, Turkish, Uzbek, French and German), and the number columns' headers align with their
  numbers.
- Chat search lists the account's Telegram chats again after the panel locks or switches workspace while that
  list is loading. Before, it showed "Loading…" until the page was reloaded.
- A mini application capture names the windows the page tried to open as such: they are recorded by address and
  not loaded.
- The verifier counts the checked GitHub attestation time of a sealed run as external time on the assurance ladder too.
  Before, the same output read "[met] External time" under `EVIDENCE` and `ASSURANCE: self_attested`, because only
  the evidence minimum counted that time.
- GitHub Actions capture: a capture cancelled in the panel, or whose time ran out before collection started, ends
  the run with the notice "No archive" instead of a failed run reading "RuntimeError"; a failed run names the
  supervisor's reason, which is fixed text without private data. The temporary panel opens in the browser's
  language when it is English or Russian, and the QR sign-in button no longer touches the line above it.
- GitHub Actions capture runs the current collector: the approved workflow `c292ca0a` checks out collector
  `f5c131ec` instead of the 0.9.3 build of 11 November, and the pair is the newest entry of the sealed release
  policy. Archives from earlier approved pairs, including `3aedb45c` with `1d07ebb1`, still verify.
- A mini application capture no longer lists Chromium's own sign-in and update traffic as the application's
  connections: the application runs in its own browser context behind the recording gate, and the browser's
  background requests go to a gate that refuses them. A Google host Chromium contacts on its own, and the page never
  asked for, is kept apart as `browser_connections`. Windows the application tries to open are recorded with their
  address from `Page.windowOpen`; before, the list stayed empty, because Chromium blocks such windows and the
  address of a new window is not known yet when it is created.
- The Investigation panel reads investigation mode each time it opens; before, it kept the state from its first
  opening and could offer to turn on a mode already turned on in Sources.
- Opening a mini application while Telegram asks to wait returns the waiting time instead of a refusal; a frozen or
  limited account is recorded as restricted, as for other account actions. Screenshots of a mini application open
  for an access limited to its chat.
- Mini applications open from the panel: **Open mini app** under a button and **Info → Mini apps** in a chat list
  the chat's mini application buttons, `t.me/<bot>/<app>` and `?startapp` links, and a bot's menu and main app.
  Opening one asks Telegram for its address as the account, loads it once in an isolated headless Chromium through
  the workspace route and records every request, WebSocket frame, Telegram WebApp call (phone, payment, links,
  data to the bot), dialog, window and download, with screenshots, the page and its scripts, in the signed
  journal. The signed launch data is removed from everything recorded. Screenshots appear in the investigation
  timeline, indicators in reports, and files in evidence archives, where `verify.py` binds them to the journal.
  Without a browser, the page and its own scripts are fetched and parsed. Before, mini applications could only
  be fetched as one page through the API, which missed every address inside its scripts.
- Investigation has one place and one name: **Investigation** sits on the navigation rail and in the main menu, with a
  red dot while a record runs. Before, “Documentation” hid under More tools and could not be opened at all in the
  Simple interface level. Its panel shows whether investigation mode is on and turns it on after a confirmation that
  says what changes; all of its tabs stay visible instead of scrolling out of view, chats for a record are chosen with
  checkboxes, and the analysis counts, reply delays and online states are translated.
- “On” was translated as a preposition in 19 languages (“Auf”, “En”, “Sur”, “На”) wherever the panel shows a setting
  state; it now reads as a state.
- `verify.py --compare` names a non-chat archive only for formats it knows; an archive from a newer TgWitness
  again reports that the verifier is too old, with exit code 3 under `--strict`.
- A FloodWait while exporting chat history waits on the history request only and no longer pauses observation
  of the account.
- Export plans offer accounts that are observing again, as exports run alongside observation; free accounts are
  still chosen first.
- The navigation rail widens to the longest word of its labels in the panel language, so labels such as
  “Псевдосекрет”, “Einstellungen” or “Configuración” no longer break in the middle of a word.
- Pseudo-secret reports read long chats in linear time, stop embedding image previews in HTML after 48 MB, skip PDF
  images above 50 megapixels and let a message taller than a page continue on the next page instead of drawing its
  frame past the page edge.
- Distributed exports prepare all chosen accounts at once instead of one after another.
- TgWitness remembers the username of a public group it opened without joining, so profile-collection helpers and
  “Load history” still find the group after a restart. Before, the helpers stopped with `no_access` and loading
  history refused the chat as not among the dialogs.
- After an export, a chat with no journal messages says that the exported messages are in the archive instead of
  “No messages saved for this chat yet”. An empty chat view opens at its top instead of scrolled past its title.
- Reports show one line instead of an all-zero weekday heatmap, its tables of zeros and zero composition bars.
- The home page says “Observation off” with “Start observation”, as the header does; Swarm summary cards wrap their
  notes instead of cutting them off.
- `migrate-to-external` also re-encrypts resumable account-export queues and saved profiling peers; before, it removed
  `vault.key` while they still needed it. Profiling re-resolves a saved peer that no longer opens.
- `tgwitness backup` copies checkpoints before the journal, so a backup taken during collection starts after restore,
  and it opens data directories whose path holds `#`, `?` or `%`.
- The journal head that detects a restore is kept in `TGWITNESS_STATE_DIR`: a `tgwitness-state` volume in Compose and
  `/var/lib/tgwitness-state` in the systemd units, where the home folder is read-only. An unwritable folder is logged once.
- Chat exports of chats with more than 32,766 deleted or edited messages no longer fail while listing their saved files.
- An evidence export sealed at record N marks records only up to N as exported.
- RFC 3161 and OpenTimestamps timestamps are on by default where requests outside Telegram have a route, and every
  evidence export time-stamps its last record before it is built. Before, archives failed `--require evidence`
  because the records written after the last timestamp had no external time.
- `verify.py --tsa-ca` can be repeated, and a token from an authority without a given root is reported as not
  checked instead of failing the whole archive. A token with a bad signature still fails.
- Chat exports include the saved files of messages that were deleted or edited, linked to their signed
  `media.saved` records in the manifest. Before, those files were only in the evidence ZIP.
- `tgwitness backup FOLDER` copies the data directory while the panel keeps running, with SHA-256 for every file
  and the journal head of each workspace.
- A journal restored from an older copy is recorded as `journal.rolled_back` at the next start and shown in the
  status, so archives exported before and after the restore can be told apart.
- The storage schema is versioned. TgWitness refuses data written by a newer schema, and a journal last opened by a
  newer version, unless `TGWITNESS_ALLOW_DOWNGRADE=1` is set for that start.
- `python -m tgwitness.security migrate-to-external KEYFILE --data-dir DATA` moves an existing local vault to an
  external master key and recovers if it is interrupted.
- Observation start records `session.takeover_risk` when the session key was created by another app ID or the
  account has a login email, recovery email or two-step password, and the verifier reports it.
- Chat pages list the times the collector was offline, with deletions Telegram reported without a chat while it
  caught up.
- Public MTProxy is marked as less stable in route choices; WARP stays recommended.
- `tgwitness status` shows the running version and an installed update waiting for a restart; `doctor` no longer
  fails the address check for its own running panel; `verify.py --compare` explains that it compares chat exports.
- Account export status carries `terminal`; duplicate panel routes are gone; Python files keep LF line endings on
  every checkout, so `verify.py` hashes the same on Windows.
- The panel shows the takeover risk and a restored journal as cards on Home and as one line elsewhere. Each risk says
  what it allows and where to change it in the official app; “I restored it myself” clears the restore warning and
  records `journal.rollback_acknowledged`. Both appear in notifications, external alerts and the accounts list.
- Coverage gaps in a chat say when TgWitness was not running and how many deletions arrived afterwards without a chat.
- Pseudo-secret chats name each attachment by kind and file name, preview saved images and keep “End chat” on one
  line; one deleted or read message no longer reads as “1 messages”.
- The panel is laid out like Telegram: it opens on Chats, a narrow rail keeps Chats, Pseudo-secret, Exports, Accounts
  and Settings one click away, ☰ opens every other section. Profile, People and Authors of a chat moved from tabs
  above the messages to an info panel that opens from the chat header, with search, export, report and author
  collection at hand.
- Reports of pseudo-secret chats show the conversation itself: the other side, start, status and encryption key, then
  every message as a bubble with saved photos, “deleted by the other side; kept here”, timers, screenshots, read
  notices and the end of the chat in place. The report title names the other side, the Report studio preview shows
  the same conversation, and new pseudo-secret records keep the other side's name.
- The People panel hides the profile collection form under one heading and drops status columns that hold only
  “Unknown”; chat filter chips wrap instead of being cut off.
- Messages can be forwarded from the chat view: “Forward” under a message or for up to 100 selected messages, to a
  chat picked by name. It uses the account's message pace and is recorded in the journal. “Forward chat” now picks an
  existing destination by name instead of asking for its numeric Telegram ID.
- Preserve the last checkpoint's signing account when another worker finishes a distributed export range after interruption.
- Chat search also lists the account's Telegram chats that are not observed yet, each with “Add”, and offers to open
  a typed @username or t.me link right away. Before, adding a chat meant leaving for Sources or the link form.
- Signing in to a workspace that has no chosen connection asks for one first, with WARP preselected and marked as
  recommended. Before, such sign-ins went silently through public MTProxy servers. Adding another account from
  files passes the chosen route to its new workspace, and the connection page lists WARP first.
- The public MTProxy pool also reads the hourly list from tgmtproxy/telegram-mtproto-proxy-list.
- Author profile collection finishes each person (profile, photos, gifts, links) before starting the next, so the
  “done” counter and the time estimate move from the start. Before, every stage ran for all people first and the
  counter stayed at zero for most of the run.
- A link preview for a public group that accepts members only after an administrator's approval now says so, and
  its button reads “Send join request”. Before, only invite links were checked, so such groups looked open.
- After “Load earlier from Telegram”, older saved messages page again instead of asking Telegram on every click.
- The author filter chip in a chat names the person instead of showing a bare ID.
- Monitoring changes in the journal are summarized in the panel language.
- The session list hides “Make this the only session” and “End all other sessions” when the session that approved
  a QR sign-in would block them.
- Health and sign-in messages keep the recorded cause of a lost account (revoked, expired or ended session, ban,
  freeze, duplicated key) instead of a generic sign-out.
- Panel polish: one page title style, visible switches in the dark theme, phone layouts for Home, Settings,
  Accounts, sign-in tabs and Sources tabs, a tidier chat header and bubble times, aligned Exports cards, and
  larger touch targets.
- Share resumable-history flood deadlines with other workers and retry admin-log reads after Premium flood waits.
- Persist history FloodWait deadlines so other workers respect the same pause.
- The workspace switcher shows each account with its avatar, name and a colored status (observing, observation
  off, sign-in required, needs attention), lists the other accounts with their problem count, and has “Add
  account” and “All accounts” at the bottom.
- The chat list works like Telegram's: folder tabs in one row that hide when empty, a “+” menu to add a chat or
  channel, open a Telegram link or start a pseudo-secret chat, and pseudo-secret chats listed with the others
  (green, with a lock) and under their own tab. When observation is off the list says so once instead of
  marking every chat “Paused”. A search for an @username or t.me link with no match offers to open it.
- A failed action shows its reason right below the button that started it, with a link to the collection status
  when the disk is short; error toasts stay until closed or until another page opens.
- The export plan reports free disk space with the same check `/multi-export/start` uses (`disk` in the plan);
  when space is short it warns before Start and keeps Start disabled. The status `storage_low` now also turns on
  when free space is below the minimum while observation is off. Planning shows “Checking @name…”, and the
  ten-account estimate appears only with ten usable accounts.
- Empty screens explain themselves: the journal says how many records it holds and offers to show system
  records, archive connections offer to create one, and an empty system log says when lines appear.
- The session banner is one line with the cause (for example, a session used in two places at once) and expands
  for the full text; Home shows the same cause and a low-disk warning on the account card.
- Settings names the connection route (public MTProxy, Cloudflare WARP, direct) with the exit country and says
  what a public proxy operator can see; Expert also shows the proxy host.
- Home tiles put the label above the number, help toggles read “What is this?”, and a chat name shows a tooltip
  only when it is cut off.
- The Simple level is simpler: the menu shows Home, Chats, Exports and Settings; other sections appear under
  “Show hidden sections” until the page reloads, without changing the level. Simple also folds the system,
  composition and per-day blocks on Home, secondary export options, and journal filters other than messages,
  edits and deletions, and names the journal “Records” and Sources “What to record”.
- Home starts with one line of saved records, coverage gaps, sign-in and low-disk state; each part opens the
  matching page.
- A coverage gap inside a chat is one line with the number of pauses, the time span and the total length; the
  full list is under Details.
- The warning for folder and whole-account scope sits right below the scope choice with a link to the dedicated
  account guide.
- Integrations say what leaves the panel and who receives it; archive connections explain what they are.
- Sources and Exports mark the recommended choice: Chosen chats for the scope and Case dossier for report
  contents. Recording says whether its settings match the recommended ones and has **Return to recommended**
  (`recommended` in the status); the scope form has **Discard changes**. Simple hides the Pseudo-secret tab in
  Sources, since pseudo-secret chats are in the chat list.
- Recheck access to helper workspaces when resuming or retrying profile collection.
- Keep session age and loss context within the current authorization, ignore late session checks from
  replaced clients, and distinguish the last successful check from the saved session snapshot.
- Add media occurrence timelines with separate document, saved-byte and image-dHash comparisons.
- Add source-linked forwarding summaries to reports and people-profile JSON, plus a typed GEXF export.
- Verify image bytes before deriving dHash indicators; report comparison and display limits.

- Dossiers separate forwarded and reused media from sender encoder hints and
  pre-existing-media findings, citing earlier permitted observations of the same
  document ID. Paid Stars leaderboards retain counts, anonymous flags and source records.
- Watchlists and indicators inspect button copy text, inline queries and valid
  UTF-8 callback data. Similar-channel results preserve Telegram's reported total
  and distinguish incomplete responses from local processing limits.

- The verifier's plain output starts with the `ASSURANCE:` line on success as well as on failure, followed by
  the `EVIDENCE:` line, as For the record advises reading it.
- History read by an ordinary group member is no longer always `incomplete`: the admin log is shown only to
  administrators, so its refusal is recorded with `reason: not_admin` and leaves the history complete.
- The history transfer preview shows how many messages the chat has and how long the transfer takes at the
  current pace (at the default 30 messages per hour, 1,000 messages take about 33 hours); a running transfer
  shows sent of total and the time left.
- On narrow screens, rows that scroll sideways (demo actions, journal filters, chat and profile tabs,
  Parameters sections, health tabs) fade at the edge where more items are hidden, in both writing directions.
- Reports name the observing or exporting account by its Telegram name, with @username and ID in brackets,
  instead of a bare `id 8644525789`. The workspace keeps the account name from sign-in; older workspaces fill
  it in on the next connection.
- Recording a chat that is not in the loaded chat list, such as a private chat reached from a message, looks
  it up in Telegram instead of failing with “Refresh the group list…”. When Telegram does not return it either,
  the message says to press **Refresh chat list** or check that the account is still in the chat.
- Pseudo-secret installs in one click in the default Hide IP mode. When the workspace route cannot reach
  GitHub, the page says why and offers **Download directly and turn on**: only this one pinned, checked
  download leaves without the proxy, after a confirmation. The journal records
  `secret_chat.module_installed` with the commit, SHA-256 and route.
- TgWitness never ends the session that approved a workspace's QR sign-in: Telegram also ends the session it
  approved. Importing records that session; the session list marks it, “End session” refuses it, and ending
  other sessions or making this the only session keeps it. The import hint no longer says the two
  authorizations are independent.
- When Telegram ends the session, the loss record keeps what was known just before it: the session's age,
  the other sessions at the last check and Telegram's last security notice (`before_loss`).
- A sign-in that has not finished yet no longer writes `account.authorization_error` entries that read as a
  lost authorization.
- History reading no longer skips chats Telegram marks as restricted; the restriction stays in the journal
  and whatever Telegram delivers is saved. Messages keep their own restriction reasons. On connect the
  account allows sensitive (18+) content when Telegram lets it, recorded as `account.content_settings`.
- Telegram's data export notice is recorded as `data_export` instead of a new sign-in.
- Chat exports and automatic account exports no longer request Takeout from a session that signed in less
  than 24 hours ago, or while Telegram asks to wait, so Telegram sends no data export warning to the account.
- Bulk account pause/resume prevents overlapping confirmations and discards stale
  operations after session resets. Failed responses no longer claim that the
  collector was unchanged; account states are refreshed without repeating commands.
- Overview clears cached summaries and charts on account or sign-in changes and ignores responses from earlier sessions. Loading and failed reads have separate states, with a retry that respects the server's requested delay and preserves keyboard focus. Failed refreshes retain the same workspace's last successful data with its timestamp.
- Account cards show the collector heartbeat and the last received Telegram event as separate times.
- Secret Chats add local phrase search with matching-message navigation, keyboard
  controls and highlights that retain the surrounding conversation. Searches stay
  within loaded records and are cleared at workspace/session boundaries.
- Loading older Secret Chat records preserves the visible message and its reading
  position; refreshes retain the current search match and unsent message draft.
- Selected cloud-chat messages can be downloaded as PNG with Light, Dark or
  Classic styling, a preview and page navigation. Images retain message numbers,
  UTC times, reply references, attachment labels and edit/deletion marks. Long
  messages continue across pages. Rendering stays in the browser, masks possible
  secrets and clears the preview on lock or workspace/chat changes.
- **Save chat as images** renders up to the latest 2,000 saved messages of a chat.
  Every page ends with its journal record numbers, the key fingerprint, the check
  command and a QR code. **Download signed ZIP** adds `pages.sig.json`, signed with
  the workspace key and journaled as `export.image_attested`;
  `verify.py page-01.png pages.sig.json` detects a changed page, statement or key, and
  `--evidence` confirms every record against a signed evidence ZIP.
- Pressing an author's name in a chat opens a person card beside the messages with
  the saved profile, photos, gifts, links, activity timeline and journal records,
  **Refresh profile** and **Build report**; the chat stays where it was.
- The person card has a **Rhythm** section counted in UTC from the author's saved
  messages in that chat: active days, conversations started after 6 hours of
  silence, median reply time, the longest run in a row, the night share and a
  weekday × hour heatmap. Only the latest 20,000 messages are counted.
- **Collect all authors** on a chat's Authors tab collects the profiles, bios, photos,
  gifts and links of everyone with saved messages. In channels and supergroups other
  connected accounts can share the work: each is reserved for the run, busy accounts
  are left alone, progress shows the percentage, time left and each account's share,
  and every record names the account that read it.
- Chat and account export reports add a **Rhythm** table under Activity by
  participant: messages, conversations started after 6 hours of silence, median
  reply time, the longest run in a row and the night share, in message order and
  UTC. It follows the participant chart setting and its labels (aliases by default).
- Collector health names one cause when nothing arrives: sign-out, a second
  session, a Telegram pause (with method and end time), a stopped collector, a
  frozen account, the route, lost chat access, a recent update gap or simply quiet
  chats; each with a confidence level and the next step, and "Cause unknown" when
  no signal explains it. Problems replace "Observing" in the workspace status.
  An open chat names lost or unconfirmed access to that chat, or the account-wide
  cause, above its messages with a link to collector health.
- HTML reports opened from disk show **Offline · 0 B sent** next to the signature
  badge. The browser counts network requests since the page opened; any request
  turns it into a red count, and attempts blocked by the page policy are listed in
  its tooltip. Served over HTTP, the badge stays hidden.
- Cloud-chat history can be forwarded in order to a new private channel or
  supergroup, or an existing channel/group with posting access. A preview fixes
  the history boundary before an explicit start. Transfers retain albums, shared
  pacing and FloodWait, support pause/resume/cancel, and journal confirmed sends
  and skips. Unknown send results require review; unknown creation results never
  trigger an automatic second creation. Available to the main administrator.
- Forwarding restores durable progress after journal failures and releases the
  account after failed starts, resumes and shutdown writes. Cancellation survives
  rejected requests and a final empty history page; stale polling errors no longer
  replace newer dialog feedback.
- The account report's activity map links each large channel or supergroup gap to
  its marked position in the paginated transcript; wide tables scroll inside their
  cards on narrow screens.
- Long transcripts get a page index with a UTC month calendar, date and record
  ranges per page, and first/last/nearby page links that work without JavaScript.
- A timed-out dedicated media connection falls back to the standard file connection
  instead of pausing the download; the data center retries its dedicated route once
  per minute in the background.
- Report packaging reuses parsed translation catalogues, cutting the packaging time
  of a 14,691-message export by about 16 %.
- `/api/trace` shows the main administrator recent panel API requests of the workspace with method, route template, status and duration, plus median, 95th percentile and slowest time per route. Request paths, parameters and bodies are not recorded.
- A FloodWait while reading history or exporting a chat no longer pauses live
  observation. The wait stays limited to Telegram's history method, which the
  account's other history readers already respect; live updates keep arriving.
- Chat pagination ends the opening animation before preserving the reading
  position. Reduced-motion mode disables that animation entirely, avoiding an
  intermittent shift when earlier messages appear.
- The two newest paragraphs of the website notice are translated in all 25
  catalogues instead of appearing in English.
- The static demo's Console link opens the correct route in a new tab.
- The chat list adds quick filters with counts for priority chats, captured changes
  and access/recheck issues, removable filter chips, multiword name/ID search and
  keyboard navigation. Large lists render in batches of 80 while keeping the open
  and focused chat available. Clearing filters preserves pending priority requests.
- Swarm and the system log fit phone screens: account cards, tools and log actions
  wrap instead of widening the page.
- Connection: the route check no longer creates a new Telegram authorization key every minute; it measures one unauthenticated MTProto round trip to the account's data center and reports the connection and round-trip times separately. A moving average marks a route slow or unavailable in the journal; a slow WARP route can be re-rolled to another Cloudflare endpoint or a new WARP identity, automatically at most once every 30 minutes. A WARP endpoint name that resolves to IPv6 and IPv4 now uses IPv4.
- Panel speed: the panel opens with one `/api/bootstrap` request instead of five in a row; the live update stream stays open while the tab is briefly hidden, reconnects within half a second after its regular end and honours `Too many live streams`; settings, preferences and the account list are no longer requested twice on opening; coverage markers in a chat use `/api/chats/{id}/coverage` with only the records of that chat and the account; avatars of a list arrive in one `/api/avatars` request.
- An idle Telegram connection stays open for two minutes after the last panel action instead of closing after each one.
- **Overview** opens first and shows whether observation runs, since when and why it stopped, with **Resume now**, messages and files per minute, Telegram waits today, the most active and the longest silent chats, and the latest independent timestamps. The browser tab icon shows a coloured dot for observing, paused and exporting.
- The chat list says why a chat can no longer be read, also marks a chat as restricted when the account's dialogs report it so, and shows when Telegram asked the account to wait. A chat restricted by Telegram is recorded once as `source.restricted` and skipped by **Load full history**; one failing chat no longer pauses the whole history run.
- Bulk reads learn their pace per Telegram method instead of sharing one delay, and a newly connected account starts at half speed (**Parameters → Performance**, where **Attachments downloaded at once** is also set).
- Files use dedicated `media_only` endpoints when Telegram advertises them, otherwise they share the existing connection. Dedicated file connections start with a file request without subscribing to updates. Their number grows from one while files queue up, up to **File connections per Telegram data center** (**Parameters → Performance**, 4 by default, 0 for the previous behaviour), and shrinks when Telegram asks to slow down; a large file is read in parallel parts and written in order. Closing the pool waits for connection cleanup, and completed downloads release cancelled part readers before returning.
- When live observation, a history run and an export in one workspace ask for the same file at once, they share the completed download, including when an export finishes first. Reused bytes are hashed again, copied bytes are checked and each observation records its source; a missing or corrupt temporary copy triggers a fresh download. Accounts retain separate downloads and access checks.
- Cancelling a Swarm export stops its owned operation before Retry or Forget becomes available. Finished exports remain available, and restarting restores selected and pinned accounts. Chat coverage follows workspace changes; completing a queued submission preserves newer text entered into the form.
- Live exports advance their signed page count only after the ZIP commit. Cancellation finishes with a signed stopped state, including cancellation during the final flush; disk failures retain the last committed snapshot. Cleaning incomplete history scratch files preserves the separately sealed live snapshot.
- A history indexing failure pauses the run and preserves its cursor for retry. An unavailable chat remains a per-source failure and does not block other chats.
- Parallel history attachment workers each appear in metrics; workers on the same priority lane no longer overwrite each other's slot counts.
- At most five Telegram connections are set up at the same moment across all accounts on a server, including reconnects and route checks, and WARP registrations are paced, so a cold start of many accounts no longer times out.
- A single-chat export now writes a signed ZIP while it reads: pages of up to 2,000 messages, each signed as soon as it is written and at the latest ten seconds after reading. **Download messages read so far** saves it at any moment, also after a cancelled or failed export; every page is JSONL for tools and HTML for reading, and the `verify.py` inside checks the chain of page seals. A stop in the middle of a write leaves the archive valid up to its last seal: TgWitness restores it at the next start, and `verify.py` checks a damaged copy up to that seal and reports the bytes after it.
- `verify.py` checks a large archive with several processes: members are hashed in parallel and record signatures are checked by worker processes while the chain, coverage and bindings are followed in order. A 10.8 GB archive with 400,000 records took 58.9 s in one process and 8.4 s with 16 (`--jobs`, default one per CPU up to 16). Timestamp anchors and retained checkpoints no longer re-read the journal from the start each: an archive with 100 anchors went from 144 s to 23 s in one process.
- Remaining-time texts in 18 interface languages, Russian, Ukrainian and Arabic among them, use the language's own hour and minute words instead of a stray `h` or `min`.
- **Swarm → Swarm export**: paste @usernames, t.me links or chat IDs and every free account takes the next chat from one queue and exports it into its own workspace (**Exports → Prepared exports**); the results can be downloaded from the Swarm page. Accounts that observe or are busy take no task; a Telegram wait or missing access moves the chat to another account, and joining a chat is never automatic. Each chat can be given another priority, moved to another account in one step, cancelled or tried again.
- Distributed export: when Telegram asks an account to wait 15 seconds or more, or an account reads clearly slower than one that has nothing left to do, its range continues on another account from the last signed page instead of waiting. New jobs use the `tgwitness-distributed-pages-v2` checkpoint format, in which the first page signed by the new account names the previous one (`handover_from`); the verifier accepts v1 and v2 and still refuses an unannounced change of account. Messages in the archive are attributed to the account that signed their page.
- **Parameters → Performance → Faster journal writes** (off by default) writes each signed record without waiting for the disk, about twice as many records per second in the test (342 → 809). A power cut or a crash of the computer can then lose the last records, which may already be in a published checkpoint; a crash of TgWitness itself loses nothing. Rebuildable working indexes of account, chat and distributed exports always write this way.
- **Attachments downloaded at once** limits each account's attachment worker queue: downloads start at two, add one after each round of files without a Telegram wait and halve when Telegram asks a file download to wait. Live priority lanes and selected history workers have separate allowances. `/api/metrics` shows the current number per queue.
- Workspaces of one server keep one copy of an identical attachment: a newly saved file becomes a hard link to the same file of another workspace after both are hashed again, so three workspaces that save the same channel take the space of one ([storage](STORAGE.md#when-the-disk-is-filling-up)). Unused shared copies are removed at start; workspace files are never removed by this.
- A handover extract now proves that each of its records belongs to the full journal: `proofs.jsonl` holds the Merkle path of every record and of the journal head to the root in the signed manifest, and `verify.py` checks them without the full journal. `verify.py extract.zip --range=CHAT:FROM-TO` confirms the requested messages of a chat are in the extract. Older extracts verify as before.
- When several attachment downloads of one chat need a fresh file reference at the same moment, their message reads are joined into one request of up to 100 numbers within 50 ms (300 reads in five chats took five requests in the test instead of 300); a message Telegram cannot decode is then read alone so the others still get theirs. A distributed export reads missing reply parents for context in requests of 100 instead of one by one.
- Workspaces open six at a time when TgWitness starts, so their tunnels and Telegram connections come up together instead of one after another, and the source measurement of the run receipt is taken once per process instead of once per workspace. Forty workspaces with 3,000 records each started in 19.9 s instead of 33.5 s.
- `/api/metrics` gives Prometheus the state, speed, file queue, Telegram waits, journal size and connection setups of every account; a scrape job and a Grafana dashboard are in `deploy/` ([metrics](../deploy/README.md#metrics-and-flight-record)). **System log → Save flight record** downloads the last 10,000 log lines and journal record kinds of the process without record contents; on Linux and macOS `kill -USR1` writes the same file.
- **Swarm** selects accounts with a tick on each card or **Select all shown** and runs one action on all of them at once: **Start observation**, **Pause observation**, **Re-roll WARP**, **Check journals** (each signed record and the retained checkpoint) or **Export selected** (each account's signed export in one ZIP with a list signed by the main workspace). The action starts for every account at once, and a panel fills in each account's result as it arrives, with the reason when one is skipped. **Start all** and **Pause all** of a group run up to eight accounts at a time instead of one after another.
- **Swarm** shows every account at work on the server, refreshed every second: its task and progress, journal records per second, files in the queue, file connections, Telegram waits, the route and the latest problem, with filters for busy, idle, waiting, blocked and disconnected accounts. Only the main administrator sees it.
- Panel addresses `/home`, `/network-topology`, `/case-board`, `/map` and `/logs` lead to their pages. Keys: `g` then `h`, `c`, `j`, `e`, `a`, `w` or `s` open a page, `j` / `k` move between chats, `?` lists them. **Return to recommended** shows the changes before applying them; repeated lines in the system log are counted instead of repeated; the account export summary names why an export needs attention; DNS lookups on the system map are attributed to the component that made them.
- History's messages-first mode uses the selected attachment worker count after
  reading text. Changing the capture preference during a run no longer leaves its
  deferred attachments without workers; pause and resume retain queued jobs.
- Stopping observation cancels a pending start, including an automatic start after
  history. A completed history task cannot restart observation after Stop. New
  observation, history, export and connection changes are refused until connection
  cleanup has finished; existing jobs keep their account reservation.
- Interrupted startup retains the count of buffered updates that were not recorded,
  writes a coverage gap and keeps the previous update position for a later retry.
- Live journal streams recheck access after reading and delivering Case Board
  updates. Revoked sessions and reduced chat permissions cannot receive a prepared
  journal batch from the previous access scope.
- Case certificates state that copied timestamp receipts still need independent
  verification of their signatures, trust chains and checkpoint binding.
- Concurrent connection restores share one client and one connection attempt per
  workspace. Interrupted setup releases waiting callers; an attempt whose credentials,
  client or authorization state changed cannot report success for the replacement.
- Repeated attachment jobs stay queued while a matching transfer runs, leaving
  download slots available for other files. Priority, retry delays and history
  ownership are retained. Existing queues gain the transfer index without rewriting
  signed observations, and every completed job still records its own signed outcome.

- Chat exports download repeated attachment representations once per export directory
  and verify unrelated retained files concurrently. Each message keeps its own file
  reference; size and SHA-256 checks still run before reuse. Unique temporary paths
  and synchronized file-index updates preserve parallel copies, cancellation and retry.

- Attachment jobs for the same file now wait for one transfer and independently verify the saved bytes before reuse, preserving a signed outcome for each observation. Different files and server-hash reads run concurrently; hash requests share the bounded file-request pool and no longer hold the ordinary Telegram request queue. Cancellation, incomplete hash reads and failed transfers leave later jobs able to continue.

- Connection setup reuses a fresh preflight result for the same route instead of repeating its handshake immediately on Apply. Startup reads access and workspaces concurrently, chat export discovery waits for a selected chat, and rapid wizard/preference edits save only the latest queued state. Stale route results are checked again; workspace changes cancel unsent saves.
- Initial chat loading retries failed stages with a persisted delay and bounds stalled requests by the operation timeout. History is saved before optional profile enrichment; completed stages survive restart and are not repeated during a retry. Chats and Home expose delayed work. Snapshot reads reject messages from another chat, invalid ID order or an older-page boundary violation, and stop when the source is disabled; saved records and signed interruption evidence are retained.
- Live updates, operator requests, background checks and exports use separate request lanes. Slow responses do not hold another lane; pacing and Telegram waits for the same method remain shared. Updates stay ordered within each chat. Account-wide deletions also order later updates across chats. Shutdown joins pending handlers before recording observation stopped and records a gap if the drain deadline expires. Extra short polling covers up to 50 selected channels, with priority sources first, using Telegram’s interval (10 seconds by default, bounded to 2–120 seconds). Other enabled chats continue normal update delivery. Opening a chat bypasses history pacing and history slots while still respecting server waits.
- Observation no longer has to be paused for exports on the same account. An account export, a chat export and loading messages into a chat run while observation keeps recording; one export uses an account at a time, and full history can also run alongside observation. The account page, the Home dashboard and the export dialogs say which tasks wait for each other.
- Chats: opening an enabled chat that has no saved messages loads its latest 100 messages from Telegram, and **Load earlier messages from Telegram** at the top of a chat reads the next older page. Chats added by the folder and whole-account scopes get their latest messages once, as set under **When a new chat or bot appears** (100 by default for new workspaces). These reads are recorded as history snapshots.
- Account export: while it discovers chats, the job card shows the stage, the number of chats found, the chat being checked and a progress bar. Chats are checked up to four at a time.
- Accounts: when Telegram rejects an account, panel actions and a paused account export name the cause: frozen, banned, deleted, or a session used in two places at once. A frozen account is detected as soon as it connects, not only while observing. An independent login checks the donor for a freeze before asking Telegram to approve the new session. If Telegram refuses the donor before approval, the unapproved key is discarded, so the import can start again; another donor also replaces a saved key that Telegram reports as not signed in. A key that is signed in or waiting for its two-step password is kept.
- Timestamps: a pass that could not run because no route for outside requests existed is repeated as soon as a route appears, and such a pass no longer counts as a failure of the timestamp services.
- Network map: the line of a connected account passes through the published Telegram range that contains its data centre address. Certificate status requests of timestamp services are shown under **TSA · OTS**; **Unlisted host** is kept for requests no component accounts for.
- Accounts: each connected account has **Profile and privacy** and **Account security**; the account page has **Profile and privacy** next to sessions and the two-step password. The check list at the end of first-run setup groups external services by kind.
- The investigation notebook, participant timeline and profile collection are translated into all panel languages.
- Live observation and resumable history can run together, with independent pause controls and separate attachment ownership. Message and history batch writes run in worker threads; shutdown drains received messages before sealing the stop record.
- Full history reads up to three chats concurrently, with a resumable cursor for each. Whole-account and folder scopes inspect all accessible dialogs, including archived chats. The overview shows concurrent tasks, history progress and the attachment queue; history can start observation before reading older messages.
- Account-export pages are sealed in a drained worker thread. Independent recorder kinds have separate command locks, so a slow browser recorder does not block the other recorders. Recorder controls clear stale state after errors and allow disabling a connection without completing unused fields.
- Delayed history replies retain their signed observations without replacing a live message version received after the history request began.
- Account exports continue past unavailable-message placeholders, including at the newest-message boundary, and reject history returned for another chat or outside the saved page boundary. Authorization loss pauses acquisition without sealing an unfinished page as terminal.
- Resume verifies saved account-export pages in the background, keeping panel controls available and showing the verification stage. An immediate pause after start or resume leaves a resumable job. Pausing during verification retains the account reservation until the verification worker finishes safely.
- Telegram request queues recheck the affected method's saved FloodWait deadline when a queued request reaches its turn, including file-download slots and paced history requests.
- An inactive Takeout approval wait no longer disables starting a separate regular-session export. Active jobs still reserve their account; exports on other accounts remain independent.
- Page updates respect the server's `Retry-After` delay when reconnecting after a stream-limit or temporary-service response.
- **What the other side sees** in Settings, the eye icon in a chat and the same control in **Pseudo-secret** choose what this account shows to the other side of a chat: read receipts (never, with the **Mark as read** button, after a message sent from the panel, or when the chat is opened), notices that one-time media were opened, story views, the typing status (hidden, shown while the operator types, or shown before a message is sent) and sending without sound. The choice is made for the workspace and can differ for one chat. **Invisible** is the default and sends none of them. Each request sent to Telegram is recorded with the operator and its result; Telegram decides when the other side receives a read receipt. Typing by the other side is shown in the chat and can be recorded.
- Update sequence: the journal records each stretch of Telegram's update numbering (`pts`) that the collector received without a hole as `coverage.sequence`, for the account (private chats and basic groups) and for each channel or supergroup. `GET /api/continuity` answers for an interval whether the sequence is unbroken, with each break, its reason and where the sequence is whole again. `verify.py` prints the same under **Sequence continuity**. Intervals without such records are not claimed.
- Deletions: a `message.deleted` record states who could have deleted the message from what the collector knew when the notice arrived: not this account, or possibly this account from another session. Where the account is an administrator, the chat's admin log is read every 60 minutes (**Parameters**) and names the account that deleted or edited. One notice that removes at least ten saved messages of a private chat with nothing left between them is marked as a suspected clear of the history. Chats show how many messages were deleted before they were saved; in a priority chat such notices shorten the recheck interval until one interval passes without them.
- Long-term preservation: evidence mode keeps an RFC 4998 Evidence Record for each retained checkpoint and renews it with a new time stamp or a new hash tree before the earlier protection weakens. ASiC-E exports carry `META-INF/evidencerecord.ers`, ZIP exports the checkpoint records under `anchors/`. `verify.py` checks the hash trees, the renewals and their order.
- `verify.py` checks time stamps and certificates signed with DSTU 4145-2002 (GOST 34.311-95 or DSTU 7564 Kupyna), GOST R 34.10-2012 with Streebog and SM2 with SM3. External signatures made with these algorithms are checked in the panel too.
- Documentation packages for a Ukrainian criminal proceeding (`UA`) carry a draft inspection protocol for the official who conducts the action, a technical annex for the expert, a file inventory and a media handover act under `data/court/`. Legal guidance has full profiles for 31 jurisdictions; Croatia, Georgia, Kazakhstan, Luxembourg, Malta and Slovenia are new.
- Independent capture reads AyuGram's local database (`ayudata.db`) as a second, unsigned observer: `python -m tgwitness_capture ayugram interpret` signs its rows into the recorder's journal and `ayugram reconcile` compares deleted and edited messages with a TgWitness evidence ZIP.
- The protection mode **Mossad** is named **Maximum**; a saved choice carries over. Timestamps are on in every setup goal.
- Exports: the signed archive can be downloaded as an ASiC-E container (ETSI EN 319 162-1), CAdES-signed with the workspace's certificate at level B-B, or B-T when timestamping is on. **External signature** on a prepared export hands out the bytes to sign and attaches a CMS (CAdES) `.p7s` made with the signer's own key, such as a qualified signature. The panel shows whether the signature covers the export, verifies and chains to a root certificate the operator supplied; revocation and trusted lists are not checked. `verify.py` reads ASiC-E containers and names the entries it skips. The exports list marks a container of more than 1000 files, which EU DSS with default settings refuses.
- PDF reports are signed as PAdES baseline (ETSI EN 319 142-1, `ETSI.CAdES.detached`) instead of `adbe.pkcs7.detached`, at level B-B, or B-T with a signature time stamp when timestamping is on and a timestamp authority answers over the route for requests outside Telegram. The report states that the program's certificate is self-issued and not qualified.
- Live collection: updates held while observation starts are processed before later updates, so a deletion can no longer be recorded before the message it removes. Records written for a live update carry `received_at` and `processing_delay_ms`. A message and the records that depend on it are written in one transaction. When the delivering update carries the same message as `raw`, `transport_update.message` refers to it instead of storing a second copy.
- Coverage records: an update from a chat whose scope cannot be checked is recorded as a `scope_undetermined` gap with its message IDs instead of being skipped silently, and the chat is looked up again after five minutes. A full startup buffer records how many updates were dropped in each chat and their message ID range. `collector.error` names the update, chat and message IDs it concerns. A start or stop security baseline states when the 777000 log could not be read.
- Panel and storage: reads use their own read-only database connections and no longer wait for, or hold up, journal writes; opening messages, authors, avatars, media for restricted links and the activity overview, and choosing chats for state snapshots, run outside the event loop. Recheck positions are stored per chat instead of rewriting one setting per chat or skipped message. A full profile refresh queue is recorded for a user once every ten minutes.
- Account export: a chat split over several pages shows its charts and assessment on the first page only; later pages open at the messages. The last step of first setup shows how many chats are chosen and which account is connected.
- Coverage gaps in a chat: starts and stops of the program before observation first ran are no longer listed as a gap, so a new workspace does not open with a gap made by its own setup. A gap recorded at one moment shows its reason, and the journal words three more reasons in the panel language.
- Reports count service messages under `Service messages`; the label `Service` stays for timestamp services. The chat list shows one priority star in each row instead of two, and the star stays visible in the selected row. On a phone the account counters no longer break a word in the middle.
- Chat export by link: progress follows the number of messages read, so a chat read as one range no longer sits at 0% until the end. The states `running`, `selecting` and `cancelled` are translated, and the main workspace is named in the panel language in the list of accounts and on the system map.
- Panel: counts on every page use the panel language's number format, not the browser's. The **Just download** goal says that it saves chats and photos and where other files are chosen. The capture link on the sign-in screen no longer touches the button above it.
- Journal and **Pseudo-secret**: how a Secret Chat ended, its acceptance in TgWitness and the route check are shown in the panel language. The password hint for ZIP exports names the stronger encryption offered beside it. `verify.py unseal-password` says that the password is wrong or the file was changed instead of printing `InvalidTag`. The daily chart keeps its date labels in right-to-left languages. Russian text uses one word for the handover extract.
- Verifier: the readable answer lists each timestamp service once, with the number of checkpoints and their time range, instead of one entry for every proof; a journal with 33 checkpoints went from about 1,100 lines to about 180. A Bitcoin timestamp confirmed with `--check-bitcoin` is shown as confirmed. Observation periods, gaps and session counts are shortened to the first ten with a count of the rest, and times read `2026-11-14 01:06:05 UTC`. Timestamp warnings are translated.
- Evidence, chat and handover archives: `README.txt` opens with what the archive is and lists `analytics.json`; the verification steps are in `START_HERE.txt` only.
- Panel: the first workspace is named `Main workspace` instead of `Main account`, which also named a kind of account. Account export offers the report in the panel language. The chat picker shows each chat's type and ID and counts the selection. The **Gaps** tile turns pink once a gap is recorded. File sizes use binary units in the panel language. The chat list no longer scrolls sideways. The parallel-session warning shows only the paragraphs for the chosen import mode. A plain word after `token`, `password` or `secret` is no longer masked as a secret. Client checks and profile warnings on the account page are worded and translated. Russian text uses the letter `ё` throughout.
- Account export archive: the chat list, the report and each chat page say when a chat was not exported or was exported in part, instead of showing zero messages. `README.txt` is written in the report language, with English after it, and lists every file with its purpose; the verification steps stay in `START_HERE.txt`. The reason a file was left out is shown as text in all 25 languages, and a single attachment is labelled in the singular.
- Account export progress names the chat being read instead of its ID. Counters across the panel use the panel language's number format. Russian wording corrected in the export job card, the export page and the import form, including a line that said a waiting job resumes after TgWitness stops.
- **Pseudo-secret** shows the other side's name and username when the account knows them, with the user ID beside it, and applies Secret Chat updates that Telegram delivers while the account is still connecting. Account export pages show times to the second. The first-setup estimate says `Less than 1 MB` instead of `About 0 MB`.
- Stopping the panel keeps the main workspace's route up until its Telegram connection has closed, so shutdown no longer spends a minute on reconnection attempts through a tunnel that is already gone.
- **Pseudo-secret** notices within half a minute when the other side ends a chat: while a chat is open the account asks Telegram for missed updates every 30 seconds, because Telegram does not always push the ending to a connected session.
- `verify.py` given an unpacked folder says to pass the original ZIP instead of failing with a key error. The journal names the session records written when observation starts and shows their values instead of raw English notes.
- The goal choice says what differs: **Follow chats** keeps panel actions, **Evidence for a case** saves every file, confirms each record and turns sending, joining and accepting off. **Pseudo-secret** explains that notice as a warning and points to the goal. The route check shows its time and latency in the panel language, and its buttons match the rest of the panel.
- **Pseudo-secret**: sending to a chat that has ended, or that the other side has not accepted yet, says so instead of failing, and ending a chat writes one journal record instead of two. Account export pages show the reason an attachment was not saved in the report language, and the Telegram-style chat list labels message counts as `Messages: N`.
- **Pseudo-secret** installs its protocol module with one button, **Install and turn on**. The panel downloads the pinned commit of [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat) (GPL-3.0-or-later) from GitHub through the workspace's route for requests outside Telegram, checks every file against the SHA-256 fixed in the TgWitness release, loads it without a restart and checks it again at every start. The page names the module, its author and license. An environment that already has the `secret-chats` extra keeps using it ([Secret Chats](PSEUDO-SECRET.md)).
- Reports in a language other than English open with a recommendation to file the English original with a certified or sworn translation. Evidence, chat and handover ZIPs then also carry the sealed English original (`report.en.html`, `report.en.pdf`, `chat.en.*`), named under `report.original` in the signed manifest, and `README.txt` ends with terms for translators ([Translating reports for court](TRANSLATION.md)).
- **Settings** is a list with the account card on top and sections grouped as **Account**, **Recording**, **Panel** and **More tools**; each row shows the value in use, and a section opens in a window over the list instead of replacing the page. A section whose settings are all above the chosen interface level shows them instead of an empty fold. **Pseudo-secret** shows chats as a list beside the conversation, with message bubbles, service notes, state marks and the key fingerprint in the header.
- Report studio: **Add message numbers** under the chat list takes a chat ID with message numbers, or `t.me/c` links, and adds them to **Selected messages**.
- Fixed: the report studio's design preview stayed empty after opening the studio by its address or reloading the page; in Pseudo-secret a new record took keyboard focus away from **Load older records**, **End chat**, **Accept here** and **Save file**; the overview button of an unavailable account read **Open chats** and led to the connection page; **Alerts**, **Geo lookup** and the default workspace name on the network topology stayed in English; in reports in other languages the opening paragraph of **Coverage** and, in the PDF, **Standards and methodology** stayed in English, and the Russian custody log named the releasing party **Published**.
- Fixed: report downloads on the **Downloads** tab took unsaved report studio choices although the page says they use the saved ones; a report with hand-picked messages names the numbers that have no journal record; an unknown panel address opens the panel with a notice instead of a JSON error; a notification no longer blocks clicks in a settings window opened over it; settings search finds **Language**, **Theme**, **Time zone** and **Interface level** and moves focus to the found setting; leaving an unsaved chat selection with the browser's Back button or **Pseudo-secret**, and closing a settings form with unsaved edits, ask first; the Case Board no longer stays on **Loading…** after a failed request; message links ending in a slash are accepted and `t.me/c/0/…` is refused; the Pseudo-secret list said **1 chats**; the report studio keeps **Save report settings** and the unsaved-changes counter on screen instead of inside the collapsed configurations block; record numbers under **Changes** and **Actions** open that record in the six report designs where they led nowhere.
- Fixed: **Unobserved message IDs** under **Selected data** compared every chat on its own numbers, so private chats, bots and ordinary groups, which share one account-wide numbering, listed numbers saved in other chats as unobserved; these chats are now left out and counted, and a selection without a whole channel or supergroup says that numbers were not compared instead of reporting that none are missing. The case assessment counts coverage notes next to gaps, and **Coverage** lists them with their time, chat and reason.
- Fixed: counts in reports used one plural form for every number, so Russian, Ukrainian, Polish, Arabic and Hebrew reports read wrongly and English ones said **1 messages**; four counters in the panel stayed in English in every other language; the capture page under **Extras** answered 404 after a reload; on phones the chat tabs **Authors** and **Profile** were hidden; in the system map the Telegram node covered the nodes below it; the account switcher showed no keyboard focus. Russian wording of counters and of the main pages is corrected.
- Fixed: settings search named many fields by their internal identifier instead of their label; the account button on the overview read **Open chats** while it led to the connection page, and in the demo it opened that page instead of the chats; **Free disk space** on the overview wrapped its value; Pseudo-secret kept times in the previous time zone after the display zone changed; when the panel could not be reached, pages showed the browser's own text such as **Failed to fetch** or a bare **Request failed** and now say that the panel did not answer; the empty chat **Profile** tab repeated **not saved yet**.
- Reports can cover hand-picked messages: **Select** in a chat marks messages, **Build report** opens the report studio with them, and the report lists the chosen message numbers under **Selected data**. The selection format gained an optional `messages` list of chat and message numbers.
- The report studio shows which parts are in every report under **Always included**. Settings, the Case Board and Extras use the same icon set as the rest of the panel instead of emoji. **Saved by day** on the overview zooms to the days that hold records and labels its dates and peak.
- Fixed: the overview's **System** card reported **Needs attention** in every state; its first row is now **Collection** and shows the real collector state; the quick navigation window could extend below the screen; on a phone **Chats** opened a conversation instead of the list; disclosure arrows pointed the wrong way in right-to-left languages; coverage gap markers in a chat only used the latest 500 journal notices instead of the period of the messages shown.
- Report studio: the chat and author lists show names and can be searched by them, and Enter in a field no longer saves the settings. Coverage gap markers in chats keep single notices as points and show an unexpected interruption that has not ended yet.
- Chat header counts for saved, deleted, not found and edited messages filter the chat when pressed, and the **Deleted** and **Not found at recheck** marks open a note with the observed time.
- **Build report** in a chat's actions and under an author's details opens the report studio with that chat, or that chat and author, already selected.
- Chats show gap markers between messages: message numbers the journal has no record for (channels and supergroups) and coverage gaps between a recorded interruption and resumption. The chat messages response gains a `gaps` list for the returned page.
- **Telegram account** in Settings opens the profile and privacy editor. Overview adds record counters, record composition and activity by chat. Notifications show an icon, a close button and stay above open dialogs.
- The saved Telegram update position no longer runs ahead of the journal. Telegram's client library advanced it as soon as a batch of updates arrived, so a reconnect or stop while a handler was still waiting, for example during a FloodWait, skipped the rest of that batch; edits and deletions in it were lost. The position now covers only updates whose handling has finished, and the rest are requested again.
- Other sessions signed in when observation starts are recorded as `session.concurrent_at_start` instead of a coverage gap. Telegram delivers updates to each signed-in session separately, so these sessions do not take updates from TgWitness; a shared session key is still detected as `updates_diverted`. The verifier reads both forms.
- **Make this the only session when Telegram allows it** kept the two-step password it set only in memory until the operator opened **Sessions of this account**, so a restart in between left the account with a password nobody knew. The password is now saved in the workspace vault before Telegram sets it and removed once it has been shown.
- **Overview** replaces the start page: every account with its state, what it is doing now with progress, what is unavailable and what still works, a chart of saved messages, edits and deletions by day, running tasks and the system state. A busy account explains its current task instead of "This account is busy".
- Sign-in shows phone, QR code, account files and authorization key side by side in first setup too. First setup asks first whether the account is a separate one (recommended) or the main one, and names the restriction and ban risk of a main account.
- Every page stays in the menu at every interface level, including the System map.
- **Load messages** and **Load full history** offer to pause a running observation; loaded messages restart it right away, and history can start observation when it finishes (**Start observation when the history is loaded**). Profile photos load while the account observes or exports.
- Account export: **Export everything** on the Overview starts it with every chat, file and account category in all formats. The default **Automatic** method uses Takeout and continues with the regular session when Telegram asks to wait for Takeout approval; the signed inventory records the method used.
- Account archives add `message-gaps.json` and `map.html`: absent message numbers per channel and supergroup, and, for the account-wide sequence of private chats and groups, each absent run attributed to a chat by a reply or pin or estimated from the chats active at that time. The map shows a calendar, chats over time and weekday-by-hour grids for messages and absent numbers; chat pages mark where messages are absent. `verify.py` recomputes the file.
- Settings: each section opens at its own address and closes with **Back to settings**, the close button, Escape or the browser's Back button. **Which chats?** is edited in place instead of reopening first setup. First setup opened after setup is complete has a close button. Analysis → Insights loads the selected chat at once and explains an empty journal instead of showing zeros.
- Settings open with the recommended values in use and four everyday sections; goal, files, record protection, notifications and the expert tools move under **Advanced settings**. Every change can be undone at once or later from **Recent changes**, custom file limits included. Switches, choice buttons and a short explanation under each setting replace bare checkboxes and question marks; the interface level moves to **Language, time and appearance**.
- `verify.py --tsa-ca` and `python -m tgwitness.anchor verify` check the RFC 3161 signature, the signing certificate and its chain in Python with the `cryptography` library. OpenSSL is no longer needed, also on Windows; `--openssl` is removed from `tgwitness.anchor verify`.
- Proxy lists: an unreadable or invalid `proxy-sources.json` no longer falls back to the defaults, which turn on every bundled list and country lookups for proxy addresses. Proxy lists stay unused and the panel asks to restore the file; saving the list settings again replaces it.
- **Record the other side’s typing in the journal**: `visibility.peer_typing` and `secret_chat.peer_typing` records list the reported actions in order with the times they were received (`timeline`), with the forum topic (`top_msg_id`), the upload progress at the first and last notice of a step and the plain fields of the action, such as the emoji of an emoji interaction. A burst keeps its first 100 steps and counts the notices after them.
- History snapshots record `returned`, `captured`, `already_recorded` and `skipped_own` separately. `telegram_returned_none` includes the observed restriction flags when Telegram returns no messages. `all_already_recorded` is used only when every returned message already has saved content; policy exclusions are not described as preservation.
- When **Hide online after actions** is on, the first sign-in of a newly created session sends an offline status request in place of the online request. This records the requested behavior; Telegram controls the status delivered to other clients.

## 0.9.3 preview · 11 November 2026

- Chat exports add `journal-changes.jsonl` when the observing workspace saw messages of the chat deleted, missing on recheck or edited: those journal records, every saved version and the notice, each with its journal hash and Ed25519 signature. `verify.py` checks every record against the export key, and the HTML and PDF reports list them under **Deletions and earlier versions**. See [evidence](EVIDENCE.md).
- Add the signed [account loss report](ACCOUNTS.md#when-telegram-ends-the-session). When Telegram bans, freezes or signs out the account, or the session is ended from another device, the journal records the cause, the Telegram error, the route and the data centre, and the account's health offers a JSON file with the journal records of the 24 hours before the loss. `verify.py` checks the report's signature and every record in it.
- Export progress: multi-account exports read attachments in batches of 100 messages and show the stage and the estimated time left; a single chat export shows the recheck and packaging stages. Attachments in a multi-account export follow the lead account's capture policy.
- Collector: attachment downloads stop while the account must sign in again and are retried afterwards; the absent-number recheck includes the 1,000 numbers below the first message and spreads up to 10,000 numbers evenly over all gaps; an authorization error of another client is recorded as `account.authorization_error`; a frozen account is detected through `help.getAppConfig`.
- The verifier's archive and JSON parsing are fuzzed in CI with ClusterFuzzLite, and `verify.py` rejects a malformed manifest with a clear message. The installer signing job runs in a dedicated `installer-signing` environment.
- Add the [expert examination protocol](NARRATIVE.md#expert-examination-protocol): `python -m tgwitness.narrative evidence.zip --jurisdiction PL --expert --procedure criminal` writes a draft of the expert's report as HTML, PDF and JSON from the examiner's own verification run. It holds blank fields for the case and the expert, the legal basis, the liability warning and any required declaration, the repeatable checks, findings in three groups and the questions the package can and cannot answer. The [examination catalog](../tgwitness/narrative/examination/README.md) covers 53 jurisdictions; each entry names its official sources and lists the points it could not confirm. The protocol and the narrative recommend filing the English original with a certified or sworn translation into the court language. Narrative reports are available in 39 languages.
- The narrative and the expert protocol use the dossier layout: a header with the jurisdiction, the procedure, the court languages and the package SHA-256, status labels with text, times as `YYYY-MM-DD HH:MM:SS.mmm UTC` and record references shortened to ranges. The terms section and the declaration follow `--procedure`; a declaration that applies to civil proceedings is left out of a criminal protocol.
- Reports: the activity chart axis shows whole numbers, words in the conditions table are no longer split inside a word, and removed and inserted words in an edit comparison are separated.
- The operator notice links the [106-day GDPR file](TAYLOR-WESSING-GDPR-FILE.md), which is available in every documentation language. [Questions and checks](QUESTIONS-AND-CHECKS.md#built-in-api-pairs-identify-a-client-not-an-account) answers the built-in API pair, public MTProxy and deleted-message objections with the facts first.
- Add `verify.py --bitcoin-source URL`: OpenTimestamps proofs are checked against block headers from your own node's Esplora API instead of the two public explorers.
- Verifier, panel and documentation state what each check establishes: the line for an archive without checked external time names the options that add it, and the witness condition refers to the custodian's key-control record.
- The website's reference pages, guides and homepage are translated in all 24 site languages; about 450 text blocks per language were still shown in English after the 0.9.2 documentation update. Translated with DeepL; markup, links and code are checked unchanged.
- Interface translations: short panel labels were translated again with DeepL using interface context, and the Russian labels were reviewed one by one. Fixes include "Observe" and "Observing" read as "comply" or "note" in several languages, "Off-site copy" read as "off-site text", "Follow new lines" read as "insert new lines", and Russian button labels in the imperative.

## 0.9.2 preview · 10 November 2026

- Watch the account's sessions while observing. A new entry in Telegram's session list is recorded under `added` in `account.sessions` and raises an alert with the device, application and country. Security notices from Telegram (777000) are recorded as `account.security_event`, the session key fingerprint as `session.fingerprint`, and other sessions signed in when observation starts or a session ended from elsewhere as coverage gaps. Phone call updates are recorded as `account.phone_call`.
- **Account security → Sessions of this account** ends one session or all other sessions. For a session key created in this workspace, **Make this the only session** ends every other session and sets a two-step password if the account has none; **Make this the only session when Telegram allows it** runs the same action once Telegram's 24-hour limit has passed. The journal records `session.exclusive_from`, and `session.exclusive_ended` if another session appears later.
- Add the [witness probe](ACCOUNTS.md#witness-probe): a second workspace with its own account answers probes in a private group. An answer that reaches this session only through history, not as a live update, marks event intake as failed until a later answer arrives live. The verifier counts probes sent, answered live and missed live, and on the witness side the probes it saw and answered.
- The journal records where the session key came from: `key_origin: "created"` for a phone, QR or independent sign-in, `imported` for a session file. Attested deployments refuse imported keys. With the goal **Evidence for a case**, starting observation first names any other signed-in sessions.
- Import an auth key and DC as one line, `<512 hex characters>:<DC 1–5>`: pasted, as a text file or in the `session` field of an Account JSON.

- A single-chat export that fails or is cancelled keeps what it has read under a statement signed with the collector key, with a signed checkpoint every 5,000 messages and another before the files stage. The export form offers **Resume export**, **Start over** and **Download partial export**. Partial exports set aside more than seven days ago are removed at startup.
- Reuse attachments already saved for the same Telegram file instead of downloading them again; reused bytes are hashed before use. Each account runs up to three file reads in parallel.

- `verify.py` checks Intel TDX quotes offline: the quote and quoting-enclave signatures, the PCK chain up to the pinned Intel root, the REPORTDATA binding and, when the archive carries Intel's collateral, the TCB status at the recorded time. Without the provider checks of `python -m tgwitness.cloud verify` the attested run stays partial.
- Evidence mode stores OCSP or CRL revocation data for each RFC 3161 signing certificate, and `verify.py` checks it against the time stamp.
- Signed checkpoints carry the latest drand round, fetched through the workspace's outside route so Hide IP, proxies and a turned-off outside route apply. `verify.py --check-drand` confirms it; the round shows the checkpoint was signed no earlier than that time.
- The verifier output lists session records: sessions added and ended, other sessions at the start, only-session periods and witness probes.

- Count failed sign-ins toward the lockout for every JSON body the panel accepts, not only for an exact `application/json` content type. The disclosure note no longer says that filtering and redaction were checked.
- Restore 6 November work missing from `main`: the chat export eligibility check with time estimates, the automatic connection route with WARP consent, the route choice for bulk import, and separate `deletion.unscoped` records for unknown messages and messages in chats outside observation.
- Before publishing the download site, CI checks the signed installer artifact and installs its wheel on Ubuntu and Windows; pull requests that change the installer also run `install.sh` and `install.ps1` twice against a local HTTPS origin. [Verification](VERIFICATION.md) records the 9 and 10 November live runs: parallel clients on one session, session resets, two-step password changes, the witness probe, interrupted chat exports and a Phala TDX deployment; [Timestamps](TIMESTAMP.md) records the live TSA services.
- The minimum for evidence is now integrity, the confirmed signer key and external time from a third party covering the last exported record: a validated RFC 3161 timestamp, a confirmed OpenTimestamps proof, a witness post read live from t.me, a witness Bitcoin seal or a checked GitHub attestation. A retained checkpoint and a witness with its own key are supporting checks, because the collector could create both alone. `verify.py --channel https://t.me/s/…` reads post dates from Telegram and skips the dates of edited posts; dates from a supplied `result.json` or any other source remain supplied metadata.

- Refresh the pinned Wolfi base images and runtime/MCP dependencies, regenerate root and capture hash locks, and require patched QR reader wheels. Exclude OpenCV 5.0.0.93, which bundles FFmpeg 8.1.1 affected by [CVE-2026-8461](https://github.com/advisories/GHSA-qff7-4q6c-m8h6).

- Simplify the panel around six daily sections: Home, Chats, Journal, Exports, Accounts and Settings. Move secondary tools, collection diagnostics, chat actions and advanced filters into contextual menus. Open saved chats after sign-in, preserve drafts and filter selections, and give messages more space on phones and desktops. Update the Russian labels and panel guide.

- First setup starts with one question: Just download, Follow chats or Evidence for a case. The answer sets the goal and interface level; five stages with a progress bar replace the seven numbered steps, connection routes open only when the automatic check fails, and the Telegram step hides account diagnostics. Level, theme and time zone stay under More options.
- The README adds animated panels for the first start and system map, and for case documentation: subject cards, conversation plans and wallet codes with watchlist hits. The capability panel adds investigation mode and the court case package. Each animation has narrow-screen and reduced-motion versions.
- Verify reused Secret Chat attachments, retain damaged cached bytes during repair, and retry pending downloads through a bounded persistent queue. Preserve exact protocol identifiers in the panel and make older history available through explicit pagination.
- Serialize analyst report edits and detect stale revisions so concurrent changes cannot silently remove revision history.
- Require verified owner-only permissions when explicitly exporting an MTProto session key in a forensic bundle.

- Create a new provider-metadata directory with readable traversal permissions even under a restrictive service umask, while preserving permissions on an existing directory.
- Cancel a pending QR sign-in when its panel session ends or is revoked, including main-token rotation. Recheck access before a queued QR request starts. Other sessions and completed account authorizations stay intact.
- Preserve Secret Chat message drafts, focus and reading position during refresh. Bind chat and auto-accept confirmations to the account where they were opened, and preserve edits made while a message is being sent.

- Update the development-history and validation overview, distinguish live monitoring from history and recheck observations, and document verification results by acquisition mode.
- Record Secret Chat integration in the published 0.9.1 installer package: backend, collector hooks, API and panel. The pinned protocol library remains an optional `secret-chats` dependency enabled per account.

- Add an administrator [System map](SYSTEM-MAP.md) with per-account routes, socket
  endpoints, proxy state, storage and key boundaries, service configuration and a
  bounded network-observation buffer. Refresh visible snapshots every five seconds;
  distinguish requests, connection attempts, results and unavailable host telemetry.

- Isolate request-body capacity and token-family lockouts, set Secure download cookies behind trusted HTTPS proxies, limit pending tickets per access, and expose journal write failures.
- Add an English Secret Chat interface demo with fictional requests, replies, attachments and retained deletion notices. See the current Secret Chat guide for installed integration and recording behavior.

- Remove the unused one-shot exporter and check recovery against the current exporter. Reject unexpected or repeated message IDs in recheck responses.

- Combine concurrent exports with resumable Standard API and Takeout acquisition. Each job retains its own progress, timings and signed checkpoints; accounts remain reserved until that job stops. Include the account controls, batch import and report-verification updates in the same build.

- Add offline `VERIFY.cmd` / `VERIFY.sh` launchers, plain-language verification explanations and saved UTF-8 transcripts to signed exports in all 25 panel languages. Build a separate Windows verifier with an embedded runtime and a language menu. The result reports signer pinning, integrity, coverage and external time checks separately.
- Add optional jurisdiction guidance for 25 countries to Report Studio and exported assessments, with separate civil/criminal sources, local-language summaries and next steps derived from the actual package. Guidance remains a research draft, does not raise assurance, and is excluded from reusable layout profiles and inherited sharing-copy settings.
- Allow the pinned Russian morphology dictionary resources in Windows portable builds while continuing to reject unrecognized files in dependency data directories.

- Keep missing-on-recheck observations separate from deletion notices in HTML, JSON and PDF counts and viewer labels. Do not claim unscoped deletion IDs were never saved when their chat is outside the current observation scope.

- Record multiple deleted IDs as a deletion batch without inferring a whole-history clear, the deleting participant, or deletion for everyone. Relabel legacy history-clear events without changing their signed records.

- Publish the one-command installer only after application and security checks pass for the exact main commit and the signed package passes Ubuntu local/HTTPS service and Windows PowerShell acceptance. Keep the previous download when checks fail or time out. Add authenticated tests of the actual public installer URLs.

- Preserve `previous_hash` in the signed-record preview even when its hexadecimal digits resemble a payment card number. Secret masking still applies to message content; the stored record is unchanged.

- Reconstruct compact chat snapshots consistently in MCP, retain unknown fields, and distinguish capped lists from removals. Resume date scans, preserve topic names across history reads, and bound image previews. Apply metric choices to filtered reports and count historical service messages separately.

- Plan sealed exports against the remaining session time, offer smaller selections, update progress estimates and reserve time for packaging.
- Compare every message field, validate record counts and structure, enforce CLI verification options, and display OpenTimestamps states separately.
- Close coverage on worker failure, bind heartbeats to the capture run, and verify TDX signing-key binding and supported component statuses.

- Add read-only MCP tools (preview): `get_messages_by_date` (one calendar day in a named time zone, computed server-side), `get_pinned_messages`, `get_chat_stats` with `gap_summary`, `get_topics`, and `get_media`, which returns a verified, downscaled image preview anchored to its SHA-256 and `media.saved` record. Every MCP tool now declares an output schema. New connections include these tools; existing connections keep the tools they were issued with.
- Show each account's selected route and checked exit address, group session controls, and retain interface preferences when adding an account. Record connection changes without repeating identical background checks. Validate withheld-marker contents and reply states in minimized exports, including rejection of a missing-source label for an included record.

- Update collection-mode instructions and Russian guidance. Allow a bounded publication-settling interval while requiring exact installer bytes.

- Mark messages left out of a minimized disclosure (preview): inside each disclosed chat, withheld messages appear as content-free markers naming the selection rule, one per run or one per message, and disclosed replies state whether they answer a disclosed message, a withheld one or one that is not in the source export. The package format becomes `tgwitness-account-disclosure-v2`; `verify.py` rejects markers with content and replies pointing at missing records, and still verifies version 1 packages.
- Repeat gap analysis with the settings carried by the signed export, count each service-message number once, and bound account estimates to the measured interval. Require explicit whole-account scope, retain pause/resume boundaries, and interrupt expensive archive scans at their time budget.

- Add missing message numbers (preview): `coverage.json`, the HTML and PDF reports, `verify.py` and the archive's `get_capture_status` measure numbers Telegram assigned and this collector never saw, per channel or supergroup and for the account-wide sequence of private chats, bots and ordinary groups during whole-account collection. Each result states whether it applies and why, lists its parameters, and anchors listed gaps to the neighbouring observations. **Parameters → Gap analysis** sets the listed gaps, the account-wide sequence and an optional service-message estimate that is never subtracted. A gap names no actor and no reason.
- Record in the signed message when self-destructing media is fetched despite a type or duration rule (`media_capture.rule_override`), with the limits that still applied.
- Add chat-state snapshots (preview): while observing, every enabled source is read periodically and saved as a signed `chat.state` record with title, description, counts, pinned messages, administrators with rights, and gifts on channels and profiles, plus the differences from the previous snapshot. Unpinning, rights changes and gift conversions or upgrades without a service message become visible. Parts Telegram refuses are named and carried forward, never reported as removed. **Parameters → Chat state** sets the interval, pause and parts.
- Add anomaly indicators to evidence reports (preview) as registered, versioned processors in `tgwitness/metrics/`: first-time posters per day with flagged injection-like days, service messages among message numbers, joins and departures per month, and pins and unpins per month. Reports list every processor that ran with its version and print its method; **Parameters → Report metrics** chooses them.
- Keep ranked-search pages within the first 1,000 results regardless of page size, order OCR/transcription results before pagination, and retain exact match positions when Unicode expansions and invisible-character removal cancel each other's length changes.

- Keep photo downloads on the still variant named by their metadata and hash manifests, including after file-reference renewal. Reject truncated photo/chat attachments and corrupt reused files instead of counting them as saved. Check recovered multi-account message IDs against missing intervals without expanding large gaps.

- Release a session's local connection lock after transport shutdown, including when a disconnected client was already removed from the workspace. Cancelling the waiting operation cannot release the lock early, and closing an older session cannot unlock a different current key.

- Apply a chat export's skip/hash-only choice to recovered messages and profile photos, and record that choice in the acquisition metadata. Reject changed messages before fetching attachments in the separate files stage. Count missing message numbers as intervals so sparse histories do not exhaust memory, including during a cancellable full recheck.

- Preserve available self-destructing photos, videos and files in the API journal with a dedicated immediate queue, explicit TTL/view-once labels and signed saved/unavailable/not-saved outcomes. Block read receipts in the API client, including batches and wrapped requests. Keep byte limits, disk reserves and Telegram backoff; saved bytes record retrieval by the collector.
- Preserve image-rendered Unicode emoji in official Web message text, reply previews, reactions and derived page text without changing the client DOM. A live account test exposed the omission; video and saved pages already retained the image.
- Improve chat-export Takeout, unreadable-message recovery, shared absent-number rechecks and bounded range retries. Preserve observed deletions in export scope, compare verified archives, and distinguish archive integrity from an independently confirmed signer.
- Protect imported sessions from remote logout, close idle connections and prevent simultaneous reuse of a session key. Add explicit session management and masked two-step password entry; cancellation or switching workspaces prevents submission. Read single-account export messages before their separate attachment stage.
- Keep source export and AI actions disabled while local source search is pending, empty or has failed; clear stale previews before the next search. Exercise delayed replies explicitly in browser checks.
- Use unambiguous synthetic privacy identifiers and report the exact marker/context on handover-test failures, avoiding accidental matches inside report metadata.
- Add an in-panel comparison of collection methods and explain account task ownership beside full-history controls. Refresh source-version badges, qualification records and Trusted Live network results; check version labels before publication.

- Add [full-text search](SEARCH.md) (preview): Russian and Ukrainian word forms, English stems, Chinese and Japanese phrases without spaces, exact phrases, domains in hidden links and buttons, @usernames, wallets and phones, filters for chat, sender, message ID and observation period, ranked with BM25. The index is derived from the signed journal, bound to its latest record hash, never exported, and can be kept on disk, in memory only or turned off. Recognized text is indexed in memory only and labelled as machine recognition.
- Ask the archive retrieves the best matches from the full-text index when it is complete, keeps the 24-source limit, and cuts long texts around their match. MCP `search_messages` accepts `ranked=true`.
- Add `tgwitness index status|rebuild` with JSON output on stdout and stable exit codes.
- Fix ranked search paging: `next_offset` is now returned when more matches exist, through `/api/search`, MCP `search_messages` and Ask the archive's partial marker. Paging stops at the first 1,000 results.
- Fix Ask the archive failing on questions longer than 24 words or 200 characters. The full-text query keeps the question's first distinct words; a query the index cannot read falls back to exact-text retrieval.
- Centre excerpts on the match in long texts that hide zero-width characters between letters.
- Build the website when a language lacks new translations: untranslated blocks stay in English with the page notice and are listed by the build.
- Add the [command line](CLI.md) (preview): `tgwitness search`, `context`, `messages`, `stats` and `export` with `--json` and stable exit codes, reading a stopped workspace directly or a running panel through a scoped, revocable archive connection. Add `.agents/skills/tgwitness-cli/SKILL.md` for agents.
- Add the `get_activity_stats` archive tool, also offered over MCP: messages by UTC hour and weekday, peak days, edit and deletion shares, senders, domains and @handles, with coverage gaps. Computed on request, not stored.
- Add the `export_messages` archive tool for the command line: saved observations streamed as JSON Lines in journal order, with full text and a completion record. It is granted only when selected; existing connections keep the tools they were issued with.
- Recheck archive access before every streamed record, including completion. Revoked or expired connections end without a completion record; lazy export reads share the archive worker limit and timeout.
- `tgwitness index` and the new commands find the data directory of the installation that runs them.

## 0.9.1 preview · 5 November 2026

- Keep message and attachment outcomes visible after single-chat sealed capture, including missing data, failed files and unfinished downloads. Translate final status when changing language after shutdown, and clear connection or export errors once they recover while retaining rejected-action and unconfirmed-revocation warnings.
- Update the pinned OAuthLib dependency to 4.0.1 for CVE-2026-49272 and regenerate the runtime, browser and MCP hash locks.
- Show in-flight attachment bytes without counting them as preserved evidence, reset progress on retries and clear it on pause. Keep official-client chat controls disabled during QR/2FA login and until a chat is available. Explain that Takeout approval requires another previously signed-in device. Bound CI dependency installation and avoid the stalled Azure package mirror.
- Add explicitly selected direct networking for official Web capture through GitHub Actions. Proxy remains the default and never falls back to direct. The panel and signed verification report disclose direct IP exposure, and verification rejects a mismatch between the selected route and the hosted network.
- Add an optional official Telegram Web observation mode with passive or sequential paced viewing, a fresh profile, restricted UI actions, login-excluded video and signed rendered observations. A required proxy bridge prevents direct fallback; exit changes stop recording. The GitHub Actions mode uses the approved sealed workflow and recipient encryption.
- Bind official recordings to independently saved source/settings, check video segment order and clean endings, record fresh drand rounds and support independent public-relay comparison. Report unfinished procedures, unconfirmed logout and the limits of local or Cloudflare assurance explicitly. See [Official client witness](OFFICIAL-WITNESS.md) for scope and validation.
- Add opt-in Trusted Live preview: isolated official Desktop/Web sessions, native JSON preservation, guarded visual recording, per-chat continuity annotations, and verifier-recomputed reports. Supply a Linux network guard with no direct fallback, periodic proxy-routed drand observations, and optional independent read-only Cloudflare samples. Account/WARP/TDX qualification remains pending; see `docs/TRUSTED-LIVE.md`.

- Make sealed export modes explicit: Telegram Takeout by default, regular API account export, or a single-chat event journal, with differences and limits shown before collection. Select multiple chats, save agreed settings, verify them with `--expected-selection`, and reject incomplete account exports with `--require-complete`. Correct the outdated one-chat-only hosted documentation.
- Preserve signed message pages before requesting files or hashes. Resume from frozen history, retain completed attachments, and finish an interrupted export with explicit gaps when time or disk is limited.
- Add Telegram Desktop compatible JSON/HTML views alongside authoritative signed data. GitHub capture supports full-account and selected-chat exports through regular API or Takeout, with chat types, dates and media settings.
- Deliver large GitHub archives in encrypted parts with a signed, attested manifest and verified local assembly. Remove the fixed 4 GiB delivery failure without omitting preserved evidence.
- Retry transient pinned OCR source downloads without relaxing checksum checks. Retry brief Windows file-sharing failures when saving private state.
- Configure account exports before collection: select chats and media types, exclude avatars by default, and choose downloads, Telegram range hashes or metadata only. Keep a shared attachment budget and record incomplete files explicitly.
- Show Takeout approval requirements and retry deadlines before collecting; check approval again without replacing the waiting session. Phone, QR and existing-session login retain their own authorization flow.
- Save Telegram-provided SHA-256 ranges with file representation and data-center metadata. Compare them against locally supplied files; Telegram identifiers and access hashes are not treated as content hashes.
- Collect message history across selected chats before processing attachments when messages-first mode is enabled. Preserve the journal in a compact export when full HTML or attachment packaging exceeds the remaining capacity.
- Stream sealed delivery encryption without a second full plaintext archive. Remove interrupted ciphertext, preserve the original evidence for retry, and keep capture deadlines across runner steps with time reserved for delivery.
- Require sealed-container validation in the release workflow. Phala deployment status now distinguishes verified, incomplete and review-required attestation instead of inferring trust from the provider name.
- Validate every sealed-container build input against its pinned source. Retry transient package downloads up to three times while retaining signature, SHA-256 and exact-package checks before offline installation.
- Include the hash-export configuration examples in source archives and preserve the translated documentation and required site assets from the latest main revision.
- Keep the current tunnel address when an older signed address post is replayed.
  Signed posts are ordered by their signed time; unsigned posts use the relay's receive time.
- Trust only the Caddy proxy on the private Docker HTTPS network and normalize client addresses for authentication limits.
- Keep operator IP addresses out of new signed access events, hide administrative payloads from shared views, and enforce workspace and export ownership boundaries.
- Reject duplicate JSON keys, prepended ZIP content and HTML injected into report seals; distinguish pinned witness keys from pinned collector keys.

## 0.9.0 preview · 4 November 2026

- Reserve each account exclusively for monitoring, history or an export. Serialize Telegram RPCs and persist full FloodWait deadlines.
- Add durable distributed chat exports with date/language/reply filters, bounded labelled context, signed chunks and explicit pause/resume. See [Distributed chat export](DISTRIBUTED-EXPORT.md).
- Keep account reservations until every export worker has stopped, including repeated pause requests and sibling worker failures. History loading in sealed sessions also reserves the account exclusively.
- Add participant timelines from saved observations: names, membership, explicit deletion flags and message activity. Profile refreshes are bounded; optional presence recording preserves unavailable or expired status as unknown and does not attribute online activity to a chat.
- Save, import and reuse report layout profiles without copying case details or report filters. Profiles are validated and isolated by workspace.
- Automatically offload eligible attachments to configured external storage under disk pressure, with reserve-space checks, compression, optional encryption and full readback verification before local eviction. Journals remain local.
- Make the recording settings and chat tabs fit narrow screens, including wider system fonts, and fix profile controls and localized labels.
- Include reviewed website assets in source archives and verify conditional dependency versions in SBOM inventories.

- Phala Cloud deployments work on Phala Cloud itself (first real run, 4 November 2026): the
  compose carries its name, Phala's own pre-launch script is kept out of the measured
  app-compose, the production OS image is chosen instead of Phala's development default, the
  instance ID is read from the CVM state, and restarts from the CVM's operations count in
  `provider_actions`. Private Phala regressions simulate each of these.
- `tdx_os` without outside tools: the verifier downloads the published dstack OS image once,
  matches it to the hash the CVM reports and computes MRTD and RTMR0-2 itself, the ACPI tables
  QEMU builds for the VM's shape included. A development image, other firmware, kernel, command
  line, memory, vCPUs or devices fail. Each journal start is checked the same way.
- Attestation certificate for Phala deployments: `verify --report` also writes HTML and a signed
  PDF, sealed by a qualified eIDAS time stamp from the Belgian government's time-stamping
  authority, a FreeTSA time stamp and the verifier's own key; `check-report` checks the seal.
- Quick tunnel addresses are also posted signed with the collector key, so a verifier is not
  misled by forged posts on the address topic; on Phala Cloud the tunnel check passes, since its
  connector runs inside the measured compose.

## 0.8.1 preview · 2 November 2026

- Runtime, sealed and media containers moved to pinned Wolfi/glibc with Python 3.12 and
  hash-locked system packages (AMD64 + ARM64). Image scans are clean of HIGH/CRITICAL.
- Tesseract 5.5.4 built from verified source, English and Russian data pinned.
- Release checks now cover real OCR, offline transcription, signed multilingual PDFs and
  container restrictions. The source archive includes all container build inputs.
- **Extras → Independent capture** in the English panel: browser/AyuGram recorders with
  encrypted tokens, pinned keys, tab selection, start/pause, snapshots, checkpoints and
  verified ZIP downloads. Everything is off by default.
- New optional `tgwitness-capture` package: Chromium PNG/MHTML snapshots, AyuGram SQLite
  copies, optional silent video, Ed25519 event chains, signed ZIP/HTML reports and a
  standalone verifier. Each recorder has its own key and storage.
- Fixed Phala installs: source bundles were missing the capture package.

## 0.8.0 preview · 2 November 2026

**Reports**

- Report studio: eight designs (Classic, Editorial, Briefing, Analytics, Technical,
  Overview, Reading series, Ledger & margin), live preview, HTML and native signed PDF.
  Switching designs keeps filters, charts and notes.
- Pick report data by chat, author, date and event type and preview it before saving.
  Edits show before/after, deletions show what was saved earlier.
- Reports look like proper dossiers now: cover, key figures, evidence map, numbered
  findings, timeline. PDFs get an A4 cover with QR, bookmarks and page refs.
- Each report explains what its conclusions rest on: export-time checks, observations,
  missing material, how to check it independently (EN/RU/DE wording).
- Send, edit and observed times are shown separately, plus replies, threads and metadata.

**Case Board and groups**

- Private Case Board: signed bookmarks, exact-version highlights, action slices,
  collections, threaded comments and statuses. Team notes stay apart from observations;
  the verifier checks board exports too. Export permission alone doesn't reveal team notes.
- Account groups share settings. Members follow the group, an account's own value wins
  until reset. Changes show which accounts they hit and ask before overwriting. Access can
  be granted to a whole group.
- Group screen at `/groups/<id>`: accounts, problems, shared chats, group export.

**Setup and connection**

- Six-step first setup and one Settings page with simple/standard/expert levels, in all
  25 languages. Each step has its own URL, Back works.
- The setup asks whether the account is a separate one; a main account only records
  chosen chats. After Start it shows that connection, events, sources and files work.
- Guided Connection screen: pick accounts, prepare and check a route, then apply. Direct,
  own proxies, public MTProto pool, WireGuard profiles and portable WARP.
- Automatic connection tries public MTProxy, then WARP, then direct (if allowed) and shows
  a status indicator instead of failing silently.
- Video duration limits in file policies.

**Panel and safety**

- No more one-click accidents: pausing, excluding and removing sources are confirmed,
  sending from a chat needs "Write as @account" first, route changes while observing
  offer to pause.
- One set of counters everywhere (deleted with text, deleted before saving, missing on recheck).
- Account files are inspected before connecting. URL, workspace and account always agree,
  a mismatch blocks actions. Chats open read-only and mask detected secrets.
- Downloads fall back to normal browser downloads, big archives stream through one-time
  cookies. Prepared exports keep size, SHA-256 and "Download again".
- Panel token rotation keeps the new session alive. Temporary network failures offer Retry.
- Panel dialogs instead of `window.confirm`, journal paging fixed, lots of small UI fixes.
- Public-channel showcase: expiring read-only links with redacted authors and signed snapshots.

**Servers and evidence**

- Extras → Server 24/7: a Hetzner server from the panel with a quick tunnel or your own
  domain. `python -m tgwitness.cloud destroy` cleans everything up.
- Phala Cloud option: the collector runs in an Intel TDX confidential VM, `verify` checks
  the attestation up to Intel's root.
- Gateway DNS (`--gateway-dns`): the server only resolves through Cloudflare Gateway.
- Optional drand rounds and Telegram device lists in evidence mode.
- Setup by goal: four questions, suggested settings, credibility and reliability scales.

**Other**

- Notification service catalog with icons, optional operator control bot, Discord witness posts.
- Storage separates backups, verified file offloading and evidence retention.
- AI previews show the endpoint and outside route.
- Pull requests run both panel suites, including Firefox and WebKit downloads. Release
  packages wait for dependency, CodeQL and container audits.
- Docs: a [panel guide](PANEL.md) for every screen.

## 0.7.1 preview · 1 November 2026

- **Start here** with two paths: export my account, or follow an investigation.
- Account export through Telegram Takeout or the regular API, resumable, with signed progress
  and coverage records ([account export](ACCOUNT-EXPORT.md)).
- Separate signed sharing copies with filters, pseudonyms and optional text/file removal.
  Signatures bind the selected output; source references and transformation records
  support comparison with the retained original.
- Readable offline reports for account exports and sharing copies, printable, with record
  links and instructions for the recipient.
- Clear handoff after download: original vs sharing copy, report preview, instructions to copy.
- Rejected Telegram logins are told apart from paused accounts and network errors.
  **Sign in again** keeps the workspace.
- Load the history of enabled sources with pause/resume, plus a signed progress report
  ([history](HISTORY.md)).
- Read-only MCP at `/mcp`, local archive search with optional AI, local OCR/transcription,
  signed webhooks with retries.
- GitHub Actions capture preview: one chat on a temporary runner, encrypted result,
  pinned provenance ([sealed capture](SEALED-ACTIONS.md)).
- Self-contained signed reports in 25 languages with chain of custody; archives add
  `custody.json` and `SHA256SUMS`.
- Panel rework: workspace URLs, Back/Forward, drafts survive updates, Ctrl/Cmd+S, Sources
  split into tabs, Parameters search, journal filters and inspector, live updates.
- Batch session import, account groups, MTProxy dashboard with ping, countries and own lists.
- MTProxy decryption through OpenSSL (it used to eat a whole CPU core).
- Stronger masking in sharing copies, bounded media decoding, repeatable source ZIPs.
- Notification services refuse redirects. Weekly Dependabot, nightly CodeQL and container scans.
- Lots of fixes: stuck chat profiles, quick search, DST in search dates, 502s behind
  Caddy, GIF/sticker downloads, slow proxy list parsing, duplicate sessions on import.

## 0.7.0 preview · 31 October 2026

- OpenTimestamps proofs are parsed strictly; Bitcoin attestations show as
  `bitcoin-unverified` until you run `ots verify`.
- Verification reports which part of the journal witness checkpoints cover;
  `--require-witness` demands a pinned witness and matching final record.
- Access and permissions guides, updated proxy and IP mode guides.
- Panel and docs site in 25 languages. Site publishing fails on missing translations.
- Added the [roadmap](ROADMAP.md).

### Initial preview contents · 30 October 2026

- First GitHub release: Windows portable, wheel, source archive.
- The setup guide has an "Open to everyone" section: no country or sanctions blocks, and
  Taylor Wessing as the only incompatibility we name. It is our position, not a licence condition.
- The README and Wiki now present the authors' Ethical Notice & Historical
  Continuity statement, with document references, historical context and an
  explicit explanation that MIT permission applies to everyone.
- The operator notice and the Taylor Wessing page speak in our own voice.
- Returned to the MIT License. A tool whose output third parties must be able to check
  should not stumble over its licence. `LICENSE` is the standard MIT text again, the
  package declares MIT with the OSI classifier, and the container, portable package,
  website, Wiki and translated README labels say so. Our statement stays in NOTICE
  and on the Taylor Wessing page as our position; it adds no licence condition. The presentation artwork reads "open source" again.
- Added our Operator Incompatibility NOTICE to README, SECURITY,
  the documentation, Wiki and website. A single source keeps the complete statement
  consistent across those pages; source, Python and portable distributions include
  NOTICE alongside the licence.
- High-assurance deployment (`python -m tgwitness.cloud`, [guide](HIGH-ASSURANCE.md)) on
  Hetzner, DigitalOcean, Linode, Vultr or EC2: no SSH key, no inbound ports, panel only
  through a Cloudflare Tunnel, and a `verify` command for third parties.
- Local launchers open the panel in the browser once it's up.
- Read-only online demo of the real panel with fictional data.
- Wiki with 13 guides, docs website with a reference section, search, diagrams and 13 languages.
- **Sign out of Telegram** on the Account page.
- About 940 Russian panel strings fixed by hand.
- Observation scope: chosen chats, a folder or the whole account, by type. New chats are
  picked up immediately.
- Investigation mode for accounts that join groups and talk to bots.
- People profiles (opt-in per chat), independent witness bot, notification excerpts,
  Parameters page, light/dark theme.
- Panel mini-client: send messages, press bot buttons, preview and join invites.
- Fixed message loss after a long stop (rechecks used to stop after 1,000 messages).
- Many fixes from a full review: attachment byte counts, restore checks, scope edge cases,
  verify.py witness handling, off-site copy retries.
- Pillow 13 (39 advisories against 12.3).

## 0.6.1 · 27 October 2026

- Renamed TgWatch to TgWitness, old archives still verify.
- Evidence mode timestamps checkpoints with RFC 3161 and OpenTimestamps.
- Password-protected AES-256 ZIP exports.
- Notifications through Apprise.
- 13 interface languages; README, Quick start and Deployment in 12 languages.
- Encrypted off-site copy to S3-compatible storage with Object Lock.
- Catch-up after restart and rechecks every 15 minutes.
- Built-in pool of public API pairs, no own API ID needed.
- New Chats view, Accounts view, multi-account chat export, signed full chat export.
- Windows portable package, public website, GitHub Pages workflow.
- Better launchers on all platforms, redesigned panel, new logo.

## 0.6.0 · 27 October 2026

- New account form with Phone, QR code, Files and Auth key tabs.
- Auth Key + DC ID sign-in, Telethon/Pyrogram sessions, TData ZIPs, StringSession, account JSON.
- QR login with 2FA, Desktop local passcodes.
- Demo opens on its sample journal; refreshed panel look.

## 0.5.1 · 27 October 2026

- Only the active account client is accepted; rejected logins are disconnected.
- Windowless Windows launches with logs in `logs/server.log`.
- Case-insensitive Unicode search, full UTC dates on phones.
- Linux/macOS launch scripts, Docker helpers, optional HTTPS with Caddy, GHCR images.
- Docs on export signatures and investigation handoff.

## 0.5.0 · 26 October 2026

- Per-account monitoring categories, presets and signed policy changes.
- Direct local entry to synthetic demos.

Older history: [release status](internal/RELEASE.md) and [verification](VERIFICATION.md).
