[TgWitness](../README.md) / [Documentation](README.md) · [Getting started](QUICKSTART.md)

![Getting started](assets/presentation/chapter-start.svg)

# Panel guide

[First setup and settings](SETTINGS.md) · [Accounts](ACCOUNTS.md) · [Export and verify](EVIDENCE.md) · [Case reports](CASE_REPORTS.md)

What each screen does, what it writes to the signed journal and where the detailed
guide is. The panel shows one workspace at a time: one Telegram account with its own
sources, journal and signing key. The account selector in the top bar switches
workspaces. The address carries the workspace (`?ws=…`); while the address, the
selector and the loaded account disagree, actions stay blocked.

Use [Compare collection methods](COLLECTION-MODES.md) to choose between live
observation, full history, fresh account/chat exports and saved-record handover.
The Exports page includes the same comparison above its download controls.

<details>
<summary>On this page</summary>

- [Find your way](#find-your-way)
- [Start here](#start-here)
- [Chats](#chats)
- [Journal](#journal)
- [Sources](#sources)
- [Exports](#exports)
- [Settings, accounts and connection](#settings-accounts-and-connection)
- [Extras](#extras)
- [Protection modes](#protection-modes)
- [More tools](#more-tools)

</details>

## Find your way

The sidebar keeps six daily sections together: **Home**, **Chats**, **Journal**,
**Exports**, **Accounts** and **Settings**. Sections that your access does not permit
are omitted. **More tools** contains investigation and administration tools.
Open **Appearance** at the bottom of the sidebar to change the language, theme,
time zone or interface level:

| Level | Sections in the sidebar |
| --- | --- |
| Simple | The daily sections |
| Standard | Also Case Board, Sources, Access and Documentation under More tools |
| Expert | Also System map, Network topology, Extras, Ask the archive, Parameters, Account, System log and Integrations under More tools |

Section names stay the same at every level. A level only hides sections. A hidden feature keeps working, and the server checks
every permission on its own. Level, language, theme and time zone are saved per
operator and workspace; see [settings](SETTINGS.md).

Use **Go to a section** at the top of the sidebar (Ctrl+K, or ⌘K on a Mac) to find
a chat, a parameter or a journal record by `#number`. Arrow keys move, Enter opens,
Esc closes.

The top bar has:

- **Notifications**: problems and chat changes worked out from the journal.
  **Mark all as read** clears the counter and **Notification rules** opens the rules.
  Delivery to Telegram, Discord or email is set up in
  [Extras → Notifications](#notifications).
- A collection-status menu with the start/pause control, connection settings and
  health diagnostics for Telegram, event intake, sources and the attachment queue.
  On a narrow screen, open it with the activity icon.
- **Lock**: closes the panel in this browser. Collection keeps running on the server.

The version and protection mode are under **Appearance**; see [protection modes](#protection-modes).
An installation opens **Home** after sign-in; an explicit link opens its requested
screen. A chat-scoped reviewer opens **Chats**. The addresses `/home`, `/case-board`,
`/pseudo-secret` and `/network-topology` also open their corresponding screens.
Unknown page addresses return HTTP 404 with nearby page suggestions.

The demo workspace contains fictional messages and never connects to Telegram.
Actions that would change a real workspace are refused there.

[System map](SYSTEM-MAP.md) shows this installation's account routes, proxy state,
socket endpoints, encrypted vaults, evidence services and observed network requests.
Select an account to inspect its path. Available but disabled services stay visible.

## Start here

The overview clears its account-specific chart and summary when you switch accounts
or sign in again. Loading, failed reads and a period with no saved records have
separate states. **Retry** repeats the failed read; if the server requests a wait,
the next attempt time appears. A failed refresh keeps the last successful data for
the same workspace and labels it with its last update time.

Each connected account shows **Collector heartbeat** and **Last event received**
separately. The first is collector activity; the second is the latest Telegram
update received. A quiet source can leave the second time unchanged while the
collector keeps running. Open the collection-status menu for connection, intake,
source and attachment diagnostics.

Choose a task. **Export my account** downloads what the account can read now.
**Follow an investigation** records new messages, observed edits and deletion notices
from the chats you choose. While observation is paused, Chats, Journal and Sources
show the setup card: connect the account, choose sources, start observation.
With the goal **Evidence for a case**, or in the Witnessed, Case preparation,
GitHub-verified or Maximum [protection mode](#protection-modes), starting observation
first reads Telegram's session list. If other sessions are signed in, the panel names
their number and offers **Start anyway** or **Open Sessions of this account**. Other
goals and modes start without that question.
The goal question stays on this page until you
answer or skip it. A new workspace opens the [first setup](SETTINGS.md) instead.

## Chats

Saved conversations, read-only by default.

Chat rows show collection state, pending and failed file downloads, initial history
loading and restrictions returned in Telegram's dialog metadata. A lost or unconfirmed
access state does not identify a content ban. Open **Filters** to select these states
or sort by the file queue; the selection stays in the URL when the page is reloaded.
The **Retry** filter finds initial chat loads waiting after an error. Their badge shows
the error type and, while collecting, the next attempt time. Home summarizes how many
loads need another attempt. Paused collection retains the jobs until it resumes.

Preserved-attachment journal entries show the observed type, name and byte size.
New download outcomes also retain the media kind and duration when Telegram provides
them. Older signed records stay unchanged; absent metadata is not reconstructed.

- Search the list by name or ID. Several words match in any order, including a
  name and part of an ID together. **Choose** adds or removes watched chats.
  **Open Telegram link** takes a username or invite link and saves a preview to the
  journal. **Join / open and observe** then joins the chat and adds it to your sources;
  opening a bot sends it `/start`.
- The list has four quick filters: **All**, **Priority**, **Changes** (saved edits
  or deletion notices), and **Needs attention** (lost or unconfirmed access, messages not found on recheck,
  failed media, history retries or Telegram restrictions). Counts respect the
  search and type filter; a quick filter replaces the state filter. These choices
  stay in the URL for reloads and Back/Forward navigation.
  **Needs attention** does not label a message as deleted. Type, state and custom
  sorting remain visible as removable chips when **Filters** is collapsed.
- Large lists show 80 matches at a time; **Show more** adds the next 80. The open
  chat and a focused row stay available when they match, even outside that batch.
  The counter shows displayed chats out of all matches. Search covers the entire
  list, including chats that have not been displayed yet.
- From search, **↓** moves to the first result, **↑** to the last displayed result,
  and **Enter** opens the first match. Within the list, **↑/↓** and **Home/End**
  move focus; **Enter** opens the focused chat. **Escape** returns to search, where
  pressing it again clears the query. **Clear filters** resets the list without
  changing collection or the open conversation.
- The chat header counts messages **deleted, text kept**, **deleted before saving**
  and **not found on recheck**. Each count is a button that shows only those messages;
  press it again to show all. **Deleted** and **Not found at recheck** on a message open
  a note with the time and what was observed. The chat list and notifications use the same
  definitions. A deleted message is red and keeps its saved text; an edited message
  keeps every saved version.
- **Search saved messages** searches the complete retained chat, including earlier
  text versions. Deleted, edited, media and author filters also cover the complete
  retained chat. **Not found at recheck** is separate from received deletion notices.
  Search does not request messages from Telegram; use **Load history** to acquire more.
  A match in an earlier version opens the saved versions with their journal links.
  **Displayed version** identifies the record used for the message and its bookmark;
  a late history response cannot replace a newer live edit on screen.
- Between messages the chat shows two kinds of gap markers. **Message numbers not
  observed** lists numbers the journal has no record for, in channels and supergroups
  only: other chats share one account-wide numbering, so a jump there says nothing
  about the chat. **Coverage gap** marks a period between a recorded interruption and
  the next recorded resumption, with the reason when the journal has one. The markers
  appear with all messages shown and hide while a message filter is on.
- **Build report** above the messages opens the report studio with this chat selected.
  The same button in an author's person card selects the chat and that author.
  Both change only the draft; save it before exporting.
- Pressing an author's name opens a person card beside the messages: saved profile,
  bio, profile photos, gifts, links, message counts and the activity timeline with its
  journal records, plus **Refresh profile** and **Build report**. **Close**, Esc or
  another chat closes the card; the chat keeps its position. **Rhythm** in the card
  counts the author's saved messages in this chat in UTC: active days, starts after
  6 hours of silence, median time to reply to someone else within 24 hours, the
  longest run of consecutive messages, the share sent between 00:00 and 06:00 and a
  weekday × hour heatmap.
- **Select** above the messages turns on message selection: press messages to mark
  them, Shift-press to mark a range, or use **Select shown**, then **Build report**.
  The report studio opens with **Selected messages** filled in. The report covers the
  message records of those messages (observations, edits, deletion notices) that pass
  the other filters; an author filter leaves out deletion notices, which carry no
  sender. Up to 1,000 messages can be selected; a chip in the studio removes one
  message, and whole chats can be added next to them. Missing message numbers are
  reported only for chats selected in full.
- **Load history** brings the last 100, 250 or 500 messages into this view and the
  journal. Find it in **Chat actions**, alongside recording settings, read-only and
  secret-masking controls. The menu closes with Escape or a click outside it.
  Loading earlier messages keeps the current reading position. If the query or page
  changes while Telegram responds, the completed load updates the saved journal without
  replacing the newer view. A failed automatic load offers **Retry**.
  To load every enabled source, use [Sources → Full history](#sources).
- **Export chat** downloads the whole visible history as a signed `chat.json` and
  `chat.html`. Several connected accounts can share the work: each downloads its own
  range of message numbers and signs its part, and the account that starts the
  export signs the archive. See [export one chat](wiki/Chat-Export.md).
- **People** lists everyone with saved messages in this chat. People profiles are off
  by default because they are personal data about third parties. When they are on for
  a chat, a profile shows name and username history, Telegram flags, avatar hashes, activity,
  who replies to whom, other observed chats, and mentioned wallets, phones, usernames
  and links. Every fact points to its record. **Export profiles** saves a signed file,
  optionally in a password ZIP; turning profiles off deletes the profile file. See
  [people profiles](EVIDENCE.md#people-profiles).
- **Save profile now** records a snapshot of the chat or bot profile: description,
  members, invite link, bot commands.

### Read-only, sending and secrets

Two switches above the messages protect the account and the reader:

- **Read-only** is on when a chat opens. Turn it off to send messages or press bot
  buttons. Each action asks **Send as @account?** or **Press this bot button as
  @account?**, tells you that chat members see it and that it goes into the signed
  journal. **Do not ask again for 10 minutes in this chat** skips the question for a
  while. Sending is off for the **Evidence for a case** goal, in the panel and in the API.
- **Mask secrets** hides what looks like a password, a login code, an API key or
  hash, a bot token, a session string, a private key, a JWT or a payment card number
  (card numbers are checked with the Luhn sum). **Show** reveals one value; the reveal is
  recorded in the journal. Turning masking off for this browser is recorded too.
  Only the display changes: the original records and every export keep the full text.

### Save selected messages as images

In a cloud chat, choose **Select**, mark the messages, then choose **Save as image**.
To capture a whole chat, choose **Save chat as images** in the chat tools menu; it
loads up to the latest 2,000 saved messages and says when older ones are left out.
The preview offers **Light**, **Dark** and **Classic** styles; use Previous and Next
for longer captures. **Download signed ZIP** saves every page as PNG together with
`pages.sig.json` and `README.txt` ([signed chat images](EVIDENCE.md#signed-chat-images)).
Up to 50 messages may be selected, and all of them must still be in the loaded chat
window. The panel asks you to reduce an oversized selection instead of silently
dropping messages.

Every page ends with an authenticity block: the journal record numbers it shows, the
chat, the render time, the workspace key fingerprint, the `verify.py` command for that
page and a QR code with the chat, key and render time. Signing requires the export
permission and adds an `export.image_attested` record to the journal.

The image includes the saved text, author, message number, UTC time, reply number,
attachment labels and saved edit/deletion status. It uses the latest saved text
with the number of retained versions; attachment contents, inline buttons,
reactions and earlier text versions are not rendered. A long message continues on
the next page with its message number and part count. Each page identifies itself
as rendered from saved messages. The PNG is a visual excerpt; use the archive and
its verifier when handing over the signed records and attachments.

Rendering happens in the browser without making a Telegram request; for signing,
only each page's SHA-256 and record numbers are sent to the panel. The existing secret masker protects text, author names and
attachment labels. The preview holds a snapshot until closed and clears on panel
lock or a workspace/chat change. The signed journal and report selection remain
unchanged. See [case reports](CASE_REPORTS.md) for complete report exports.

### Forward a chat to a channel or group

The main administrator can open a saved cloud chat and choose **Forward chat**
from its tools menu. Choose **New channel**, **New group**, or **Existing channel
or group**. New destinations are private; an existing destination uses its numeric
Telegram ID and must allow this account to post. Forum destinations are not supported.

Pause observation or another active account job and enable Telegram actions before
previewing. Read-only accounts and the **Evidence for a case** goal block transfers.
**Preview** reads the accessible Telegram history boundary and checks the destination.
It does not create a destination or send messages. **Start** starts the transfer;
the preview expires after ten minutes. One transfer can be active per workspace.

The transfer reads Telegram history from oldest to newest, through the last message
seen in the preview. It is not limited to the messages already saved in TgWitness.
Messages arriving above that boundary are excluded. Native forwarding preserves
Telegram's available author attribution and media without downloading and uploading
copies. Albums within the boundary stay together. Notifications are silent. Replies,
topic structure, reactions, edits and deleted or inaccessible messages are not
reconstructed. Secret Chats are outside this workflow. Telegram's content protection
and posting restrictions remain in force.

The panel shows confirmed sends, skips, state and the next allowed attempt time.
Service messages and individually protected messages are skipped with a recorded
reason. Account message spacing and hourly limits apply to every message; an album
waits until its reserved slots are due. FloodWait and slow-mode pauses update the
account's shared RPC backoff. The account's existing pacing defaults remain unchanged.

**Pause** stops between requests; **Cancel** stops remaining work without removing
messages already sent or deleting a created destination. An in-flight request may
finish before either action takes effect. Closing the dialog does not cancel a job.
After a process restart, unfinished jobs require an explicit **Resume**. A lost or
incomplete send response pauses the job for review: inspect the destination before
resuming. A retry retains the stored Telegram random IDs and confirmed counts;
this is not a guarantee of indefinite deduplication by Telegram. An unknown creation
result cannot be resumed automatically: check Telegram and cancel the old job before
starting a new transfer to the destination that was created, if any.

If saving a job or its journal entry fails, the worker restores the last saved
state and releases the account. A send or creation that may already have reached
Telegram remains marked for review. Retry a failed start or resume after storage
is available again; confirmed progress advances only with its journal entry.

Signed `interaction.forward.*` journal entries record the boundary, destination,
confirmed source/destination message IDs and skips. They document the transfer;
they do not replace the original signed observations and exports.


## Journal

Every record the workspace has signed, newest first.

- **Overview** counts observed messages, recorded edits, deletion notices and
  selected sources.
- **Event timeline** filters by event type (all, edits, deletions, reactions,
  membership, coverage), by text and by source. **Load earlier events** pages back.
- Open a record to see its details, hash and payload. **Link to this record** is an
  address that opens the same record. Possible secrets are masked in this preview;
  exports keep the original.
- The journal is append-only: nothing in the panel edits or deletes a record. Check it
  with **Exports → Verify journal** or `python -m tgwitness.verify`; see
  [export and verify](EVIDENCE.md).

## Sources

Which conversations this workspace records, and what it keeps from them. Changes
apply to future activity; saved records stay.

**Refresh chat list** reads the account's chats and folders. It does not download messages.

### Scope

- **What this account records**: **Chosen chats** (only the chats you add),
  **Telegram folder** (one of the account's folders, including chats added to it
  later) or **Whole account** (every chat, and every new chat, group, private chat or
  bot as it appears). **Investigation mode** is for a dedicated account: it records
  everything the account sees, its own messages and button presses, and saves each new
  chat's profile and earlier visible messages straight away. The
  [dedicated account guide](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/)
  explains why never to use your main account.
- **Source types** limit folder and whole-account modes to channels, groups, private
  chats and bots. **Own actions** adds the account's own messages, edits and
  reply-keyboard presses.
- **When a new chat or bot appears**: save its profile and up to the chosen number of
  its latest visible messages.

[Pseudo-secret](PSEUDO-SECRET.md) is the included Secret Chat interface, enabled
per account after installing its protocol module with one button. Cloud observation
and history use their own settings. Nothing is recorded while TgWitness is
not running; after a restart it catches up only what Telegram still returns, and the
report shows the gap. Chats beyond the chat list limit (1,000 dialogs unless changed in
Parameters) are added when they next become active. Inline bot buttons pressed in
another app are invisible; the bot's reply is recorded.

### Chats in scope

Filter by status (**Enabled**, **Paused**, **Priority**, **Excluded**, **Unconfirmed
access**, **Ignored**) and type, then act on a selection: enable, pause, mark or remove
priority, exclude from scope or remove. The status badge only shows the state; actions
are in each row's menu with a line on what they do. Pausing and excluding ask for
confirmation, also in bulk. Removing a source asks for its name and deletes its people
profiles; its saved records stay in the journal.

A source the account's chat list does not show is **receiving updates, not in the chat
list** while records keep arriving, otherwise **access unconfirmed**. **Available
chats** adds chats with **Add selected** or **Add all matching**.

### Full history

Loads the available history of every enabled source into Chats and the journal.
Progress survives a restart; attachments follow your media settings. See
[source history](HISTORY.md).

### Recording

- **Choose which changes to preserve**: new messages, edits, deletion notices,
  visible reactions, joins and leaves. A preset changes the form;
  **Save recording settings** applies it. Turning a category back on does not recover
  missed events.
- **Preserve media when available**: download attachments up to a size per file, set
  per type from 1 to 2,000 MiB, and limit video length in seconds (0 means no limit).
  Every download attempt gets a recorded outcome.
- **Recheck**: priority chats every few minutes, other chats rarely, so the account
  stays clear of Telegram's FloodWait limits. 0 turns a group off. Mark priority chats
  with the star in the list; chats per pass and the pause between chats are in
  Parameters. See [collection](COLLECTION.md).

## Exports

**Downloads** prepares files; **Build report** chooses how reports look.

| What | Use it for | Guide |
| --- | --- | --- |
| Account export | A fresh snapshot of what the account can read now | [Account export](ACCOUNT-EXPORT.md) |
| Sharing copy | A minimized derivative of a finished account export | [Disclosure](ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| Signed ZIP | Journal, report, attachments and verification tools at a fixed journal boundary | [Export and verify](EVIDENCE.md) |
| HTML, PDF, JSON report | A sealed readable report | [Case reports](CASE_REPORTS.md) |
| JSONL, CSV | Original records with signatures; a formula-safe spreadsheet | [Export and verify](EVIDENCE.md) |
| Handover extract | Only the chats, period and people a recipient needs | [Evidence](EVIDENCE.md#investigation-handoff) |
| Chat export | One chat as signed `chat.json` and `chat.html` | [Export one chat](wiki/Chat-Export.md) |

- **Encrypt the downloads above with a password** (12 characters or more) saves an
  AES-256 ZIP that 7-Zip or WinRAR opens. The signed file inside is unchanged. The
  password is not stored.
- When the session key of this workspace was imported, the account export and chat
  export dialogs say so in one line: copies of that key can exist outside Telegram's
  session list. The same line offers **Create an independent authorization**, which
  opens the sign-in page with that option selected. See
  [accounts](ACCOUNTS.md#create-an-independent-authorization).
- A chat export that fails or is cancelled keeps the range it saved. **Capture or export
  one chat** then offers **Resume export** and **Start over**; see
  [export one chat](wiki/Chat-Export.md).
- While a chat export reads, **Download messages read so far** saves a ZIP whose pages are
  signed as they are written; the line under it counts the signed messages.
- **Prepared exports** keeps up to 20 files within 2 GiB, plus the latest one, for
  repeat downloads, each with its SHA-256 for the recipient to compare.
- When the browser refuses its save dialog, the panel falls back to an ordinary download.
- **Your signing identity** shows the key fingerprint. **Save checkpoint** and
  **Download signed run receipt** give you records to keep outside the collector.
  **Prepare timestamp request** builds an RFC 3161 request without contacting any service.

## Settings, accounts and connection

- **Settings**: goal, connection, what to record and the interface. See
  [first setup and settings](SETTINGS.md).
- **Accounts**: every workspace with its state, sources, events and attachment queue.
  Filter by **Needs attention**, **Collecting**, **Offline or paused** or **Not
  connected**, pause or resume a selection, import account files in bulk and manage
  groups. See [accounts](ACCOUNTS.md).
- **Account**: sign-in and the connection route of this account. Direct, a WireGuard
  profile, your own proxy, the public MTProto pool or WARP; prepare and check a route,
  then apply it to this account, a group or all accounts. See
  [connection and proxies](CONNECTION-SECURITY.md) and [proxies](wiki/Proxies.md).
  **Account security → Sessions of this account** lists Telegram's sessions, ends one
  or all of them, and — for a key created in this workspace — offers **Make this the
  only session when Telegram allows it**, which repeats that action after the 24 hours
  Telegram requires and shows the two-step password it sets once. See
  [account security](ACCOUNTS.md#create-an-independent-authorization).
  **Account security → Witness probe** uses a second workspace to check that this
  session receives updates live; see [witness probe](ACCOUNTS.md#witness-probe).

Bulk pause and resume keep the confirmed selection within the session where it
was opened. Controls stay disabled while confirmation or execution is pending;
changing workspaces or locking the panel cancels the remaining commands.
After execution, the panel refreshes account states. A failed request is reported
as a request failure, because the server may already have applied the command.
Commands are not automatically repeated.

## Extras

Optional: an account and sources are enough to start collecting. Only the option you
choose opens its settings, and nothing is connected automatically. The
**Protection level** card at the top shows the [protection mode](#protection-modes).

| Card | What it adds | Guide |
| --- | --- | --- |
| Storage & disk space | Backups, moving older files to your cloud, an evidence copy that cannot be deleted | [Storage](STORAGE.md) |
| Goal & protection level | Suggested settings for your goal and two scales | [below](#goal-and-protection-level) |
| Notifications | Problems, changed messages and a daily summary; your own control bot | [below](#notifications) |
| Evidence & backups | Timestamps, more witnesses and an encrypted off-site copy | [below](#evidence-and-backups) |
| Server 24/7 | A cloud server without SSH, created and deleted from the panel | [High assurance](HIGH-ASSURANCE.md#from-the-panel) |
| Independent witness | Signed checks posted to your Telegram channel or Discord | [Witness](WITNESS.md) |
| Code check | Compares the running program with a public GitHub commit | [below](#code-check) |

### Goal and protection level

Four questions:

1. **What is it for?** A personal record, an investigation, or evidence for a case.
2. **How much will you observe?** A few chats (up to about 50), many chats (up to about
   500) or whole accounts. This sets the chat list limit to 1,000, 3,000 or 20,000.
3. **Photos and files?** Text only, photos and short media (photos 20 MB, videos
   100 MB), or everything (videos and documents up to 1 GB each). Everything with whole
   accounts also keeps 4 GiB of disk free.
4. **Where will it run?** This computer, or a server that is always on.

The suggestion lists independent timestamps, drand and Telegram's device list, each
with a line on what it adds. Timestamps start every 60, 30 or 10 minutes for a personal
record, an investigation or evidence; drand and the device list need timestamps.
**Apply** changes only these, the attachment policy and the two parameters above. Each
change is a journal record, plus `setup.applied`. Notifications, an off-site copy, a
server, Gateway DNS, the code check and a witness are offered as next steps with their
own forms.

Two scales are computed from what is set, not from the goal:

| Scale | Points |
| --- | --- |
| Credibility | Signed journal 1, timestamps 3, drand 1, device list 1, code check that matches 1, witness polling 1, attested server 2, Gateway DNS log 1 |
| Reliability | Always-on server 3, off-site copy 3, Object Lock 1, problem notifications 1 |

80% or more reads **maximum**, 50% **high**, 25% **moderate**, below that **basic**.
Reliability currently counts an always-on server from the answer to question 4,
before any server is checked.

### Notifications

Notifications go through Apprise to Telegram, Discord, Slack, ntfy, email, Matrix and
100+ other services. Pick a service, fill in one or two fields and send a test, or
paste Apprise addresses directly.

- **Problems**: disk almost full, account signed out, collection, copy or timestamp
  errors, a new session signed in to the account with the device, application and
  country Telegram lists, a login code or new sign-in that Telegram reports during
  observation, and another session after **Make this the only session**. On a sealed
  server, an opened SSH port or a login is a problem too.
- **Changes**: deleted, edited and missing messages in observed chats, grouped into
  one notification per check (every minute unless changed in Parameters).
- **Completed tasks**: history, exports and storage copies.
- **Watchlist hits**: matches from watchlists set to send an alert.
- **Daily summary** at the chosen hour, server time.

Notifications carry chat names and counts. Message excerpts are off by default; with
them on, message text leaves this machine.

**Your operator bot** is a bot of your own from @BotFather that answers `/status` and
`/stats`, and optionally `/pause`, `/resume` and `/copy`. Only the listed chat and
Telegram user IDs can use it; conversation text stays in the workspace. Use a separate
bot if another application already receives its commands. See
[notifications](wiki/Notifications.md) and [operator bot](STORAGE.md#operator-bot-and-completion-notices).

### Evidence and backups

- **Independent timestamps** send only the SHA-256 of each signed checkpoint to RFC 3161
  authorities and OpenTimestamps calendars, every 5 to 1,440 minutes. A recipient needs
  such third-party time for the minimum for evidence. **Anchor now**
  runs a pass. See [timestamps](TIMESTAMP.md).
- **More witnesses**, each off until chosen: the newest drand round, Telegram's list of
  signed-in devices without IP addresses, and Cloudflare Gateway's log of the server's
  DNS queries. See [optional records](EVIDENCE.md#optional-records-in-evidence-mode-drand-and-telegram-devices).
- **Encrypted backup** copies the journal, files, checkpoints and chat exports to
  S3-compatible storage (Wasabi, Amazon S3, Backblaze B2, Cloudflare R2, MinIO).
  Everything is encrypted on this machine first. **Download encryption key** and keep it
  apart: without it the copy cannot be read. Object Lock in Governance or Compliance mode
  keeps objects from deletion for a set number of days. See [off-site copy](wiki/Off-site-Copy.md).

### Code check

Checks whether the installed program matches a published version.

1. Enter a GitHub repository (the official one is filled in) and a tag, branch or commit.
2. **Check now** asks GitHub's API, through this workspace's route for outside requests,
   for that commit's file list. It compares the git blob ID of every measured program
   file with the commit. A Windows checkout with converted line endings still matches.
3. The result lists changed, extra and missing files (up to 50 of each) and is saved as
   a `source.checked` journal record.

The result counts as current only while the running program files are unchanged:
check again after an update. No token is needed and only public repositories work;
chats and credentials are not uploaded. A match identifies the code on disk. It is not
hardware attestation; for that, see [Phala Cloud](HIGH-ASSURANCE.md#confidential-vm-on-phala-cloud-intel-tdx).

## Protection modes

The switcher next to the version number shows the chosen mode and how many of the 18
protection layers are active, for example `🟠 Witnessed 9/18`. **Change mode** in
**Extras → Protection level** opens the choice. A mode describes a target and lists what
is still missing; recording, signing and saved settings are the same in every mode.

| Mode | For | Adds |
| --- | --- | --- |
| 🟢 Easy | Watching a chat and keeping a copy | Chats, the journal and chat exports; signing runs in the background |
| 🟡 Signed | Reports to a platform, a host or an abuse desk | Signed archive, journal check, checkpoints, handover extract |
| 🟠 Witnessed | Cases where someone may claim the record was changed | An independent witness posting signed journal heads |
| 🔴 Court-ready | Evidence for a lawyer, the police or a court | Timestamps, an encrypted off-site copy, case details in reports |
| 🟣 GitHub-verified | Records whose software anyone must be able to check | Code check and GitHub Actions capture |
| ⚫ Maximum | High-stakes cases against a well-funded adversary | A sealed 24/7 server, a hidden IP address, all 18 layers |

The layers: every record signed and chained; a signed run receipt; attachments saved
with SHA-256; signed checkpoints; rechecks; problem alerts; read-only witness access; a
witness checking on schedule; RFC 3161 timestamps; OpenTimestamps proofs; a verified
latest timestamp; an encrypted off-site copy; case details in reports; a matching code
check; Telegram never seeing this machine's IP; outside requests through a proxy; Object
Lock on the copy; a sealed server with provider records. A layer that is off has
**Set up**, which opens its form. Choosing a lower mode asks for confirmation and
deletes nothing.

## More tools

<p lang="en" translate="no"><strong>Extras → Independent capture</strong>: connect a
separate browser or AyuGram recorder, pin its signing key, select capture options,
start/pause, take snapshots and download verified signed archives. Each recorder has
its own manual login, route, journal and key. Both connections start disabled.
See the English <a href="OPTIONAL-CAPTURE.md">Independent capture guide</a>.</p>

- **Ask the archive**: search saved observations, review the sources, then decide
  whether to send them to an AI model. See [archive analysis](ANALYSIS.md) and
  [local OCR and transcription](MEDIA-ANALYSIS.md).
- **Parameters**: limits and pace of collection, rechecks, downloads, profiles,
  notifications and exports. Search by name, show **Only changed** values and prepare
  defaults as a draft with **Restore defaults…**. **Save parameters** applies the values
  from their next use, and each change is a journal record.
- **Access**: separate tokens for reviewers, analysts and operators, limited to chosen
  workspaces, chats and rights. See [access](ACCESS.md).
- **System log**: what this process did since it started (connections, proxy changes,
  sign-ins, refusals, settings changes) with IP addresses hidden. **Follow new lines**
  keeps the newest line in view. Messages stay in the journal only.
- **Integrations**: the AI provider, [read-only MCP](MCP.md) connections and
  [signed webhooks](WEBHOOKS.md).
- **Case Board**: private team notes, bookmarks and slices next to the evidence. See
  [Case Board](CASE-BOARD.md).
- **Documentation**: the [investigation mode](INVESTIGATION-MODE.md) drawer. While a
  documented session is recording, it moves to the main sidebar.
- **GitHub Actions capture** in Exports: one chat captured from your fork. See
  [sealed capture](SEALED-ACTIONS.md).
