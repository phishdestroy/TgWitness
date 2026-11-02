# TgWitness

> Open-source Telegram investigation software. Export chat history, preserve observed edits and deletion notices, follow people across chats, and hand over a signed archive that a recipient can verify.

TgWitness runs on your own computer or server. PhishDestroy maintains the project under the MIT License. The website is documentation; the browser demo contains synthetic records and does not connect to Telegram.

Signed exports let recipients verify file integrity and the signing key offline. A hash-linked journal preserves the sequence of saved observations; independently retained checkpoints provide an earlier comparison point. Reports combine readable history, source references and verification results in the same package.

The panel brings together isolated account workspaces, supported session imports, parallel chat export, cross-chat people profiles, observed name changes, bot-button interaction receipts, saved attachments and offline HTML/JSON evidence. Case Board keeps team annotations linked to saved records. The report studio offers eight designs, content choices and a data preview; minimized sharing copies control what recipients receive. Optional witnesses, timestamps and encrypted off-site copies add records outside the local journal. Archive search, AI analysis, OCR, transcription, MCP and signed webhooks work with the records you have collected.

These guides track the `main` source branch. The project version is `0.8.1`; check the changelog and release notes before assuming a source feature is included in a downloaded package.

Choose an entry below for the exact workflow, commands and limits. Each guide has a Markdown edition; its canonical HTML page retains diagrams, animations and interactive examples. Translated pages also expose Markdown through `rel=alternate` links.

## Start here

- [Start in minutes](https://phishdestroy.github.io/TgWitness/docs/start/index.md): Try TgWitness with sample data, then launch your own Telegram observation workspace on Windows, Linux or macOS.

- [Dedicated account](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/index.md): Prepare a separate Telegram account for collection.

- [Connect an account](https://phishdestroy.github.io/TgWitness/docs/accounts/index.md): Connect Telegram by QR code, phone number or session import. Choose sources and check that new messages reach your journal.

- [Collection modes and evidence levels](https://phishdestroy.github.io/TgWitness/guides/modes.md): Compare one-off export, observation, investigation and independent verification.

- [Read-only browser demo](https://phishdestroy.github.io/TgWitness/demo/): Explore the panel with fictional accounts and messages.

## Investigate and preserve

- [Investigate across all chats](https://phishdestroy.github.io/TgWitness/docs/cases/index.md): Run an end-to-end Telegram investigation across channels, groups, private chats and bots: whole-account capture, history, people, links, files, timelines and verified evidence.

- [Build a Case Board](https://phishdestroy.github.io/TgWitness/docs/case-board/index.md): Collect saved observations, exact highlights and action slices on a private board, discuss them with your team and present a collection.

- [Manage a group of accounts](https://phishdestroy.github.io/TgWitness/docs/groups/index.md): Compare group workspaces, find a source, review observation periods and apply shared settings with per-account exceptions.

- [How collection works](https://phishdestroy.github.io/TgWitness/docs/reference/collection/index.md): Observation scope, live updates, rechecks, attachments, own actions and what a gap means, record by record.

- [Load source history](https://phishdestroy.github.io/TgWitness/docs/reference/history/index.md): Load past messages from enabled sources, pause and resume, and verify a signed progress report.

- [Export and verify](https://phishdestroy.github.io/TgWitness/docs/exports/index.md): Export captured Telegram history, verify signatures and compare a journal with a checkpoint retained by an independent witness.

- [Design a report](https://phishdestroy.github.io/TgWitness/docs/reports/index.md): Choose report data, one of eight designs and the contents, then preview and export HTML, signed PDF or a complete evidence package.

- [Prepare a sharing copy](https://phishdestroy.github.io/TgWitness/docs/handover/index.md): Choose the records and fields a recipient can receive, inspect the finished copy and verify its signed manifest and source journal boundary.

- [Case Board reference](https://phishdestroy.github.io/TgWitness/docs/reference/case-board/index.md): Bookmarks, exact highlights, action slices, discussions, scoped access and the signed annotation history used by Case Board.

- [Report configuration and verification](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/index.md): Report filters, eight designs, contents presets, saved change histories and the assessment included in signed exports.

- [Evidence format](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/index.md): Contents of the signed ZIP, record kinds, process receipts, people profiles, off-site copies and offline verification.

## Search the archive and connect AI tools

- [Work the archive](https://phishdestroy.github.io/TgWitness/docs/archive/index.md): Load history, search saved records, review AI sources and connect your tools.

- [Archive analysis](https://phishdestroy.github.io/TgWitness/docs/reference/analysis/index.md): Search saved messages, review AI inputs and keep analytical reports with their source references.

- [Read-only MCP](https://phishdestroy.github.io/TgWitness/docs/reference/mcp/index.md): Connect an MCP client to selected workspaces and chats with expiring, revocable access.

- [Local OCR and transcription](https://phishdestroy.github.io/TgWitness/docs/reference/media-analysis/index.md): Recognize captured images and audio with a local worker; keep derived text linked to its source file.

- [Outgoing webhooks](https://phishdestroy.github.io/TgWitness/docs/reference/webhooks/index.md): Send scoped events to HTTPS receivers with HMAC signatures, retries and delivery status.

## Deploy, share and verify

- [Keep it running](https://phishdestroy.github.io/TgWitness/docs/server/index.md): Run TgWitness on a server with persistent storage, private panel access, backups and checks after a restart.

- [GitHub Actions capture](https://phishdestroy.github.io/TgWitness/docs/capture/index.md): Export one Telegram chat on a temporary GitHub runner.

- [Choose a proxy](https://phishdestroy.github.io/TgWitness/docs/proxies/index.md): Maintain automatic MTProxy routes or use your own proxy. Choose IP modes, fallback rules and the route for external requests.

- [Share a case](https://phishdestroy.github.io/TgWitness/docs/access/index.md): Give reviewers and analysts access to selected accounts and chats, with separate permissions, session limits and revocable tokens.

- [See how evidence works](https://phishdestroy.github.io/TgWitness/docs/concepts/index.md): Follow a message from capture to checkpoint. Change a sample record, recalculate its SHA-256 chain and see what a retained checkpoint detects.

- [Set up a witness bot](https://phishdestroy.github.io/TgWitness/docs/witness/index.md): Publish signed journal checkpoints to your Telegram channel with a separate witness, its own key and read-only collector access.

- [Timestamps](https://phishdestroy.github.io/TgWitness/docs/reference/timestamp/index.md): RFC 3161 timestamps for signed checkpoints: what is sent to the authority and how a response is verified.

- [Security and data handling](https://phishdestroy.github.io/TgWitness/docs/reference/security/index.md): Threat model, access model, secrets at rest, network exposure, session imports and how to report a vulnerability.

## Verification and scope

The journal records what the authorized account observed, subject to its access and Telegram rate limits. Saved content remains after a later deletion; content deleted before capture is unavailable. Deletion notices and unsuccessful rechecks remain distinct observations. Integrity verification establishes the relationship between supplied files, the signing key and retained checkpoints. Telegram authorship, complete coverage and the truth of message content require separate supporting evidence.

The connection reference explains IP modes, fallback and external-request routing. MCP provides read-only access to selected saved records through a separate scoped token; Telegram actions and configuration changes are outside that interface. Archived messages remain untrusted source material for an AI client.

- [Features and limits](https://phishdestroy.github.io/TgWitness/docs/reference/features/index.md): The current collection model, multi-account workflows, exports and operational boundaries of TgWitness.

- [What has been tested](https://phishdestroy.github.io/TgWitness/docs/reference/verification/index.md): The live Telegram test, automated checks, browser checks and what remains unverified.

- [Changelog](https://phishdestroy.github.io/TgWitness/docs/reference/changelog/index.md): Every change by version, including the changes not yet released.

## Optional

- [Complete English handbook](https://phishdestroy.github.io/TgWitness/llms-full.md): Public guide and reference articles in one Markdown file, including source URLs.

- [Documentation hub](https://phishdestroy.github.io/TgWitness/docs/): Browse the illustrated handbook and its language editions.

- [Source code](https://github.com/phishdestroy/TgWitness): Implementation, documentation and issue templates.

- [Releases](https://github.com/phishdestroy/TgWitness/releases): Packages and their release notes.

- [MIT License](https://phishdestroy.github.io/TgWitness/LICENSE): Software license.

- [Operator incompatibility notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/index.md): Our operator notice on Taylor Wessing and its source record.

---

# Start in minutes

Canonical page: https://phishdestroy.github.io/TgWitness/docs/start/

First, explore a working example. Then connect your own account.

## Look around without an account

Download or clone the project, install **Python 3.11 or later**, and run the demo. The launcher creates a local environment and installs the pinned dependencies.

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

The browser opens a workspace with fictional messages. Open a conversation, compare an edit and inspect an export. Demo mode does not connect to Telegram.

![TgWitness conversation view with sample messages](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

A sample workspace. Your own journal starts separately.

## Start your own workspace

Close the demo process, then use the normal launcher:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Open the local address shown by the launcher. If asked, enter the **panel access token** from the local file named in the terminal. This unlocks TgWitness; it is separate from Telegram sign-in.

## Capture your first message

1. [Connect a dedicated Telegram account.](https://phishdestroy.github.io/TgWitness/docs/accounts/)
2. Select a group or channel the account can access, then start observation.
3. Send a new message in a test group you control and check that it appears in the journal.

For a server installation, follow [Keep it running](https://phishdestroy.github.io/TgWitness/docs/server/).


---

# Use a separate account. Never your main one.

Canonical page: https://phishdestroy.github.io/TgWitness/docs/dedicated-account/

Read before you connect an account

Our advice not to use your main account is not a joke. It is reality.

Main account

- Your own app hash: 99% logged out
- Bans just for low trust are frequent
- Using it is a really stupid idea

Extra account on public pairs

- Over a million accounts registered through these pairs
- The pairs have been alive for 5+ years
- Nobody can see anything of yours through them

01

## Why not your main account

This is accurate information. We know exactly where the pitfalls of these problems are.

1. ### Your own app hash: 99% logged out

   Logging in to my.telegram.org from an account you have no access to, to get an app hash, and then any request through that app hash means a 99% chance the account is logged out. You can check it.
2. ### Bans just for low trust are frequent

   Accounts are banned simply because Telegram does not trust them, and such bans are frequent. You can check this too. Using your own account is a really stupid idea.
3. ### Copied session keys can be revoked

   Running an imported TData/session key in Telegram Desktop and TgWitness at the same time can trigger `AUTH_KEY_DUPLICATED`. Telegram invalidates that authorization, so both copies need a new login. A dedicated account does not prevent this.

   Fully quit the original client and keep it closed while using its imported session. For parallel use, sign in to TgWitness by phone or QR to create a separate authorization; other separately authorized clients can remain signed in.

   [Read the session import warning](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=en#session-warning)

Telegram documentation

- [Logout errors: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [Creating your own app hash: obtaining api_id](https://core.telegram.org/api/obtaining_api_id)

02

## Why TgWitness works through public app hash/app ID pairs

That is why we built TgWitness on public app hash/app ID pairs. By our logic, bans are less likely with them: more than a million Telegram accounts have been registered through these pairs, and many different programs work through them. By our logic, this is better than working directly with a personal app hash: these pairs have been alive for 5+ years for sure.

### Your own new pair

Created at my.telegram.org from the account.

- About 99% of accounts logged out
- One new application, one account

### Public pairs of the pool

The same pairs many programs use.

- Over a million accounts registered
- Many different programs
- Working for 5+ years

### Why nobody can see anything of yours through these pairs

- #### The pair is a name, not a key

  Telegram asks for the API ID and API hash when a program connects and when it requests a login code. They identify the application and give no access to any account; Telethon's documentation notes that one pair works with any phone number.
- #### Your session key never leaves your server

  Signing in creates an authorization key by a Diffie–Hellman exchange between your TgWitness and Telegram; the key itself is never sent. Telegram's documentation: after authorization the key becomes associated with the user, and every call with this key runs as that user. Other programs with the same pair have their own keys and cannot use yours.
- #### Traffic is encrypted with your key

  Every request and answer is encrypted with the session's authorization key, not with the API hash. Knowing the API hash decrypts nothing.
- #### The owner of a pair sees nothing

  Telegram has no method that lists accounts, sessions or messages by API ID. The owner of a pair sees only its app settings at my.telegram.org.
- #### Only your account sees which app it is

  Settings → Devices of your own account lists each session's app name and API ID, device, IP address and dates. Nobody else gets this list.

Telegram documentation

- [User authorization: the key becomes the user](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [Creating an authorization key](https://core.telegram.org/mtproto/auth_key)
- [MTProto encryption](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [What a session record holds](https://core.telegram.org/constructor/authorization)
- [Obtaining api_id](https://core.telegram.org/api/obtaining_api_id)
- [Telegram apps' open source code](https://telegram.org/apps#source-code)

Libraries and discussions

- [Telethon: signing in](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: official app APIs](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: should the api_hash be kept secret?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### The same pairs in other programs 7

The pairs of official Telegram apps are public and built into many independent programs and libraries:

- [opentelePython · src/api.py](https://github.com/anmv/opentele/blob/4df17bd8c443d6452afc5a2d29ec7922fad1a5c3/src/api.py#L575)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [opentele2Rust · opentele2-core/src/api.rs](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/api.rs#L641)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [GrampoPython · Grampo/ut/api.py](https://github.com/abbas-bachari/Grampo/blob/00aa662d853c4ac2180432371c5e0d9444bbfe9e/Grampo/ut/api.py#L526)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [tgmanagePython · api/schemas/api_app.py](https://github.com/xdsnich/tgmanage/blob/f67c46be0ab234bd04526a8663d3936bd98a8597/api/schemas/api_app.py#L47)

  - Android 6
  - iOS 8
  - Desktop 2040
  - macOS 2834
  - Telegram X 21724
  - Web K 2496
- [LyChatBotTDLib · helpers/tdlib/index.js](https://github.com/LyoSU/LyChatBot/blob/fac0ae5d5f2cddb8a26312014f51c0f6f40ec191/helpers/tdlib/index.js#L11)

  - macOS 2834
- [hsadasdPython · config.py](https://github.com/herobrinovaleksandr-png/hsadasd/blob/6842c74895038c16e219324fcd07dbe8153f37f0/config.py#L68)

  - Desktop 2040
  - Desktop 17349
  - Telegram X 21724
  - macOS 2834
  - iOS 10840
  - Web 2496
  - +4
- [blb.teamblb.team/threads/…294](https://blb.team/threads/app-hash-app-id-ofitsial-nykh-kliyentov.294/)

  - Android 4 · 5 · 6
  - iOS 8
  - Desktop 2040
  - Desktop 17349
  - macOS 2834
  - Telegram X 21724

  Forum list of official app pairs, published for registering accounts

03

## Ways to create an extra account

A Telegram account needs a phone number that receives the login code. Choose by how long the account has to live.

- Best choice

  ### Prepaid SIM or eSIM

  ********

  Lasts

  As long as you keep it topped up

  Watch out

  The most reliable: Telegram accepts real mobile numbers best. A number the carrier takes back goes to someone else.
- ### Virtual number app

  ********

  Lasts

  While the app keeps the number

  Watch out

  Telegram may refuse a virtual number, not deliver the code or limit the new account at once; some apps take back numbers that are not used.
- ### Number rental

  ********

  Lasts

  The rental period

  Watch out

  When it ends, the number goes to the next customer.
- ### One-time activation

  ********

  Lasts

  One code

  Watch out

  The number returns to the pool at once, often with a history of previous owners. Set the cloud password before anything else.

Whoever holds the number later can request a login code. A cloud password (two-step verification) stops them from signing in; without it the account belongs to the next owner of the number.

Telegram documentation

- [Spam FAQ: virtual numbers and previous owners](https://telegram.org/faq_spam)
- [Two-step verification](https://core.telegram.org/api/srp)

### Rented +888 numbers (Fragment)

Some marketplaces and services offer temporary rental of Telegram's official +888 numbers from Fragment.

Approximate price: US $20 per day.

- You can register an account directly in Telegram Web or Telegram Desktop.
- You can delete accounts on the number and create new ones.
- These accounts generally face fewer anti-fraud checks, but they do not provide immunity or special privileges.

The number is not yours. After the rental ends, the owner can reclaim it. Set a cloud password immediately and do not treat the account as long-term.

Owning the +888 yourself or using a prepaid SIM you control remains more reliable.

### Ready-made accounts from marketplaces

Some marketplaces (for example G2G or Z2U) sell ready-made Telegram accounts — new, aged, or with session files.

- [G2G: Telegram account listings](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: Telegram account listings](https://www.z2u.com/telegram/accounts-5-15140)

NEVER USE YOUR MAIN ACCOUNT! A dedicated account obtained this way is still safer than putting your primary Telegram account into TgWitness.

#### Warnings before purchase

- This violates Telegram's Terms of Service.
- Many accounts are mass-registered (auto-reg) or have an unknown history.
- Some sellers may still have recovery access.
- Accounts from such markets are frequently banned or restricted later.
- Avoid marketplaces that openly sell stealers, phishing tools, or clearly stolen accounts.
- Buying an account — even one advertised as auto-reg — from platforms that openly sell phishing tools, stealers, stolen sessions or accounts violates not only Telegram's Terms of Service but also the laws of most countries. This can later invalidate your evidence. Choose carefully.

#### If you use this option

1. Treat the account as disposable.
2. Terminate all other sessions, set a cloud password and change recovery methods immediately.
3. Use 2–3 accounts from different providers or accounts you registered yourself.

**Premium, deletion and the seven-day delay**

If the account has Premium, someone with access to the phone number cannot delete the account immediately. You receive a notification and have seven days before deletion.

This matters because your investigation depends on the account: you have time to prepare a replacement.

**Fresh accounts and API credentials**

If you obtain and use your own api_id/api_hash from a fresh account you registered yourself using a number from an SMS service, the account will be logged out on the first API request or session authorization. Keep this in mind when planning an investigation.

04

## Creating the account

From a number to the first recorded chat.

1. ### Get a number

   A prepaid SIM or eSIM when the account has to live long; a rental or a one-time activation for a short job. Services are listed below.
2. ### Register apart from your main account

   Register in the official Telegram app on a separate device, emulator or phone profile, not next to your main account.
3. ### Lock it with a cloud password

   Right away set a cloud password and a recovery email used nowhere else.
4. ### Close the privacy settings

   Phone number **Nobody**, find me by my number **My contacts**, last seen, profile photos and bio **Nobody** or **My contacts**; turn contact sync off.
5. ### Keep it from self-destructing

   Set account self-destruct to the longest period, so a stopped TgWitness does not cost you the account.
6. ### Give it a neutral profile

   No name, photo, username or bio from your other accounts, no personal contacts.
7. ### Let it warm up

   Join a few chats a day at first. New accounts that rush are limited first.
8. ### Share nothing with bots

   Never press “Share phone number” or “Share location” for a bot. Open links and Mini Apps through a VPN or proxy on that device.
9. ### Connect it to TgWitness

   In its own workspace, connect with **Account → QR code**, then press **Sources → Investigation mode**. The app is where you act, TgWitness is the record.

Telegram documentation

- [Two-step verification](https://core.telegram.org/api/srp)
- [Privacy settings](https://core.telegram.org/api/privacy)
- [Account self-destruct](https://core.telegram.org/method/account.setAccountTTL)

05

## Number services

Options to start from. Countries, prices and whether Telegram accepts a number change often; check before paying.

### Prepaid SIM and eSIM 11

- [SMARTYsmarty.co.uk](https://smarty.co.uk)

  - UK
  - SIM
- [VOXIvoxi.co.uk](https://www.voxi.co.uk)

  - UK
  - SIM
- [iD Mobileidmobile.co.uk](https://www.idmobile.co.uk)

  - UK
  - SIM
- [Threethree.co.uk](https://www.three.co.uk)

  - UK
  - SIM
- [Asda Mobilemobile.asda.com](https://mobile.asda.com)

  - UK
  - SIM
- [Ultra Mobileultramobile.com](https://www.ultramobile.com)

  - US
  - Prepaid

  PayGo plan, very cheap
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - Prepaid
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - Prepaid
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - Prepaid
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### Virtual number apps 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  US only; registration needs a US number
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  The number is taken back if you do not use it
- [TextFreetextfree.us](https://www.textfree.us)

  - US
- [2ndLine2ndline.co](https://www.2ndline.co)

  - US
  - CA
- [Talkatonetalkatone.com](https://www.talkatone.com)

  - US
- [TextMego-text.me](https://go-text.me)

  - US
  - CA
  - Other countries
- [textPlustextplus.com](https://textplus.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.gogii.textplus)
- [FreeToneGoogle Play](https://play.google.com/store/apps/details?id=com.textmeinc.freetone)

  - US

  [TextMe Up · textmeup.com](https://www.textmeup.com)
- [Nextplusnextplus.me](https://nextplus.me)

  - US
- [Dingtonedingtone.me](https://www.dingtone.me)

  - US
  - CA
- [Burnerburnerapp.com](https://www.burnerapp.com)

  - US
  - CA
  - Paid

  With a trial period
- [Hushedhushed.com](https://hushed.com)

  - Many countries
  - Paid

  Cheap
- [Sidelinesideline.com](https://www.sideline.com)

  - US
- [MySudomysudo.com](https://mysudo.com)

  - US
  - CA
  - UK
- [2NumberGoogle Play](https://play.google.com/store/apps/details?id=com.bpmobile.second.phone)

  [App Store](https://apps.apple.com/app/id1216135390)
- [SLYNUMBERslynumber.com](https://slynumber.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.dev.slynumber)
- [Phonerphonerapp.com](https://phonerapp.com)
- [Onoffonoff.app](https://www.onoff.app)

  - EU

  European mobile numbers in an app
- [Sonetelsonetel.com](https://sonetel.com)

  - Many countries
  - Free number
- [Zadarmazadarma.com](https://zadarma.com)

  - Many countries

  Virtual numbers

### Number rental and activations 12

Rental keeps a number for weeks or months. A one-time activation gives a single code: set the cloud password right after registering.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - Rental
  - Activations
- [SMSPVAsmspva.com](https://smspva.com)

  - Rental
  - Activations
- [5SIM5sim.net](https://5sim.net)

  - Rental
  - Activations
- [SMSPoolsmspool.net](https://www.smspool.net)

  - Rental
  - One-time
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - Rental
  - Activations
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - Rental
  - Activations
- [JuicySMSjuicysms.com](https://juicysms.com)

  - Rental
  - Activations
- [365SMS365sms.org](https://365sms.org)

  - Rental
  - Activations
- [SIMSMSsimsms.org](https://simsms.org)

  - Rental
  - Activations
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - One-time
- [SMS-MANsms-man.com](https://sms-man.com)

  - One-time
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - One-time


---

# Connect an account

Canonical page: https://phishdestroy.github.io/TgWitness/docs/accounts/

One workspace holds one account, its journal and its signing key.

## Choose how to sign in

Open **Accounts**, add a workspace and open its connection settings. Use a dedicated account for observation.

- **QR code:** scan it from Telegram’s device settings and confirm the new login.
- **Phone number:** enter the number, the code Telegram sends and your two-step verification password if enabled.
- **Session import:** import a supported session or Telegram Desktop data belonging to you.

Choose a built-in API profile or enter your own API ID and hash. An API profile identifies the client; it does not sign in to an account or make the connection anonymous.

**Need a proxy first?**

You can [choose and test the connection route](https://phishdestroy.github.io/TgWitness/docs/proxies/) before signing in. Each account has its own route.

## Choose what to observe

1. Open the source list and select the chats, groups or channels you need.
2. Review collection settings, including media, before starting observation.
3. Start the collector and check its connection and recent activity.

The account must be able to access the source. Different roles can see different events; the journal reflects what that account received.

For a case spanning the entire account, use **Sources → Observation scope → Investigation mode**, review the settings and press **Save scope**. The [complete investigation walkthrough](https://phishdestroy.github.io/TgWitness/docs/cases/) covers all visible chat types, old history, people profiles, cross-chat references and evidence handoff.

## Check the whole path

In a test group you control, send a unique message from another account, edit it and delete it. Confirm all three events in the journal, then [export and verify](https://phishdestroy.github.io/TgWitness/docs/exports/) the record.

A connected status confirms the connection. A captured test message confirms that a particular event reached this workspace.

## Add another account

Create another workspace in **Accounts** and repeat the setup. Keep each account’s signing-key fingerprint so you can identify its exports later.


---

# Choose a proxy

Canonical page: https://phishdestroy.github.io/TgWitness/docs/proxies/

Keep the account connected. Decide explicitly when its route may use the server's address.

## Choose the IP mode first

01**Hide the address**

Use a proxy. When none works, wait without a direct Telegram connection.

02**Direct as a last resort**

Permit Direct after the configured delay; return to a working proxy when one answers.

03**Server behind a tunnel or VPN**

Allow direct routes through the host's network. This option does not install or verify a VPN.

The route chooses the connection. The IP mode determines whether a direct connection is permitted.

## Let the pool maintain the route

1. Open **Account → Settings → Connection settings**.
2. Choose the IP mode and **Automatic MTProxy**, or enter a fixed route.
3. Save and run **Test Telegram connection**. It also works before sign-in.
4. After starting collection, check that a controlled message reaches the journal.

New workspaces use automatic MTProxy with **Hide the address**. The pool combines four public sources, probes entries, retains working routes and replaces failing proxies. Failed downloads retain the previous snapshots.

## Use your own proxy

Enter SOCKS5 or HTTP CONNECT details, paste a supported Telegram proxy link, or provide an operator catalog. Pause observation before changing an active route. Fake TLS MTProxy secrets beginning with `ee` remain unsupported.

**Rotation, sharing and retry settings**

Under **Parameters → Automatic MTProxy**, set failure thresholds, cooldowns, planned rotation and accounts per proxy. A sharing limit of one makes an account wait when no exclusive entry is available. List refresh and probe intervals follow the main workspace's values. Separate proxies do not guarantee separate exit IPs.

## Separate Telegram from external requests

MTProxy carries Telegram traffic only. Timestamps, notifications, copies and source checks use a separate SOCKS5/HTTP proxy, the account's SOCKS5/HTTP route, or Direct where the IP mode permits it. Those external requests can be disabled.

An explicit `TGWITNESS_PROXY_FEED_PROXY` configures the feed downloader's route. The [independent witness](https://phishdestroy.github.io/TgWitness/docs/witness/) keeps its own settings. These controls do not install a system VPN or route browser traffic.

See [all modes, defaults and source lists](https://phishdestroy.github.io/TgWitness/docs/reference/connection/#ip-modes), or [choose who may change an account's route](https://phishdestroy.github.io/TgWitness/docs/access/).


---

# Export and verify

Canonical page: https://phishdestroy.github.io/TgWitness/docs/exports/

Give a recipient files they can check against the collecting workspace and its saved history.

Retain a referenceExport signed ZIPRecipient verifies

New to signatures and checkpoints? [Change a sample record](https://phishdestroy.github.io/TgWitness/docs/concepts/#chain) and see which checks detect it.

Keeping a copy away from the collector? Go to [S3 setup](https://phishdestroy.github.io/TgWitness/docs/exports/#s3), [Object Lock](https://phishdestroy.github.io/TgWitness/docs/exports/#s3-retention) or [verified recovery](https://phishdestroy.github.io/TgWitness/docs/exports/#s3-restore).

## Retain a trusted reference

Save the workspace’s public-key fingerprint outside the collector. During collection, keep signed checkpoints elsewhere or use an [independent witness](https://phishdestroy.github.io/TgWitness/docs/witness/). These references let a recipient check the key and an earlier journal boundary.

## Download the signed ZIP

Open **Exports** and create a signed evidence ZIP. It includes the full workspace journal and a signed file manifest. Use [Report studio](https://phishdestroy.github.io/TgWitness/docs/reports/) to shape its readable report, or a [handover extract](https://phishdestroy.github.io/TgWitness/docs/handover/) to deliver only selected, minimized data.

HTML, PDF and JSON reports carry their own signed seals and can be checked separately. CSV is a convenient analysis copy; use the exact CSV inside the verified ZIP to check its integrity. Keep the signed ZIP when the recipient also needs the source records and attachments.

## Verify with a trusted copy of TgWitness

In the installed project environment, replace the example fingerprint and file paths:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

When both references pass, the result reports `key_pinned: true` and `checkpoint_checked: true`. Keep the verification result with the original archive. The retained checkpoint must be at or before the export’s boundary.

## Use the verification result

- **Check the delivered files:** the manifest binds their hashes, and record signatures bind the saved journal. A changed file or broken record chain is detected.
- **Check the workspace identity:** the independently retained fingerprint identifies the signing key you expected.
- **Compare an earlier boundary:** a retained checkpoint checks the export against a journal prefix saved before the handoff.
- **Review collection coverage:** gaps, acquisition results and a controlled send → edit → delete test describe the events this setup captured.

Keep these results with the recipient's copy. See [what verification establishes](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope) for the scope of the checks and the separate assessment of source claims and collection coverage.

## Set up the S3 off-site copy

In your running workspace, open **Exports → Off-site copy**. This optional feature works with AWS S3 and other S3-compatible services. It copies journal segments, preserved photos and files, checkpoints with their timestamp responses, and finished chat exports. Every object is encrypted on the collector with `AES-256-GCM` before upload.

The online demo shows the same controls with uploads disabled. Enter storage credentials only in your own running workspace.

[![Complete Off-site copy panel: endpoint, region, bucket, access keys, schedule, Object Lock and recovery key controls](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

The complete panel with advanced options expanded. No storage credentials are shown.

| Field | What to enter |
| --- | --- |
| Endpoint | The storage service URL, without a bucket path or credentials. Fictional example: `https://s3.example.invalid`. |
| Region | The region required by your provider. The application default is `us-east-1`. |
| Bucket | An existing bucket you can access. Fictional example: `example-case-backup`. |
| Folder in the bucket | The object prefix; default `tgwitness`. The application appends a prefix derived from this workspace’s signing-key fingerprint. |
| Access key ID / Secret access key | Enter both storage credentials together. They are saved in the workspace vault. Leave both empty on later saves to keep the saved pair. |
| Path-style addresses | Use `endpoint/bucket` when enabled, or `bucket.endpoint` when disabled, according to the provider. |
| Copy interval | From 1 to 1,440 minutes; default 5 minutes. The application must be running for scheduled copies. |
| Object Lock retention | Retention days and mode for a bucket that supports Object Lock. Zero days leaves the bucket’s default retention in effect. |

1. Create the bucket with your provider, then enter its destination and credentials. Leave **Keep an off-site copy** unchecked while preparing, then select **Save off-site copy**.
2. Select **Test connection**. This uploads an encrypted test object and checks the storage response.
3. Select **Download encryption key**. Keep that file separately from the collector; it is required for recovery.
4. Enable the **Keep an off-site copy** checkbox and save again. Select **Copy now** for a manual pass, or leave the schedule running.

## Check retention and copy progress

Under **More options**, choose retention days and `GOVERNANCE` or `COMPLIANCE` when your bucket supports Object Lock. TgWitness reads back the retention mode and deadline of an uploaded object. Review the separate retention result: confirmed, missing retention or check failed.

The panel reports the last pass, object count, transferred bytes, the copied journal boundary and any error. Missing or changed local media is reported and retried on the next pass. Files, checkpoints and queued exports after that media can still be copied.

Uploads use the workspace’s Direct, SOCKS5 or HTTP route. Choose one of these routes for S3 copying; an MTProxy-only route leaves the copy pending with an error.

## Keep the recovery key separately

The downloaded JSON contains the decryption key, destination settings, workspace object prefix and signing-key fingerprint. Recovery needs both this key file and separate storage credentials with read access to the bucket. Keep them in your recovery plan.

If you change the endpoint, bucket or folder prefix, download the key file again so its destination settings match. The application starts a new copy of the locally retained journal, files and checkpoints at the new destination. Finished chat exports already removed from the local upload queue remain at their previous destination.

## Restore and verify on another machine

Use a trusted installation of TgWitness, the downloaded key JSON, storage credentials with read access, and an empty output directory. Replace the fictional credential placeholders below.

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

Downloads and decrypted objects stay in private temporary storage while the entire journal, retained checkpoints and preserved-media hashes and sizes are checked. Unsafe paths, conflicting journal segments and a journal shorter than its checkpoint are rejected. A failed verification publishes no restored files.

Successful recovery produces `events.jsonl`, `media/`, `checkpoints/` and `exports/` for the material available in the copy. Keep the command’s JSON result with the recovered material.

Compare recovered material with your independently retained checkpoints or witness records, then review the recorded collection coverage for the period you need.


---

# GitHub Actions capture

Canonical page: https://phishdestroy.github.io/TgWitness/docs/capture/

Export one Telegram chat on a temporary GitHub runner, then download and verify the encrypted result.

Enable JavaScript to generate a key and decrypt your archive.

**Full reference**

**Preview available from `main`.** A fork launches a pinned reusable workflow from `phishdestroy/TgWitness`. The workflow reads one selected chat using a newly created Telegram session, attests the resulting evidence ZIP, and uploads only recipient-encrypted handoffs. The normal administration panel is not exposed.

This is an ordinary GitHub-hosted runner, not confidential hardware. GitHub, the approved collector and dependencies, the helper page, the browser, and the HTTPS tunnel remain in the trust boundary. A GitHub attestation binds bytes to an approved workflow; it does not give the messages a Telegram signature, establish historical completeness, or certify that nobody accessed the host.

## User flow

The helper explains the five stages and lets you try message or collector substitution on sample data. **Start my capture** opens the wizard.

1. Choose **GitHub Actions capture (preview)** on the project homepage, the workspace login screen, or **Exports → Open capture helper**. You can also open the [official helper](https://phishdestroy.github.io/TgWitness/sealed.html?lang=en) or `tgwitness/static/capture.html` from a trusted checkout in a modern browser. The helper makes no network requests for key or file processing. It is available in English and Russian.
2. Generate a key and save **sealed-key.json**. This is the only private decryption key. Copy the separate public **recipient** value. Losing the private key loses access to both the connection and the archive. Confirm that you saved it to unlock the next step. If you already have a delivery file, load the saved key and choose **I already have an archive**.
3. Fork TgWitness, enable Actions in the fork, and run **Sealed chat capture**. Paste the public recipient and choose 30, 60, or 120 minutes. Never put a phone number, login code, Telegram password, private key, or session in workflow inputs, commits, issues, or logs.
4. During the run, download **sealed-connection** from Artifacts and unzip it. Load `connection.tgwsealed` in the helper, using the saved private key. The resulting link contains a random access secret in its URL fragment. Keep this link private. The panel removes the fragment and keeps the secret in this tab's session storage; it is not placed in HTTP access logs.
5. Open the connection link. Sign in with a QR code, or with your phone number and the login code. Enter your two-step verification password if Telegram asks for it. The built-in API credential pool is used by default, just like the normal workspace. You may expand the optional custom credentials section and enter both `api_id` and `api_hash` from [my.telegram.org/apps](https://my.telegram.org/apps). Leave both fields empty to use the built-in pool; a partial or malformed pair is rejected. Session imports are not allowed. Load the chats and choose one source. The connection link contains an access secret: keep it private.
6. Load the dialogs and select one chat. Capture starts immediately. The selected source cannot be changed after starting. You can resume a paused history read, finish with the data already collected, or cancel without producing an archive. History reading and attachment downloading finish separately. Deadline expiry after starting produces an explicitly partial archive; expiry before starting produces no archive.
7. Wait for **sealed-result**, download and unzip it, and decrypt `delivery.tgwsealed` in the helper. You receive `delivery.zip`, containing `evidence.zip`, `attestation.jsonl`, and instructions. Browser decryption is limited to 256 MiB; larger packages use the streaming local command below.
8. End the temporary session in Telegram Settings → Devices if revocation was not confirmed or the runner was killed. Normal completion attempts logout; network failures and forced runner termination prevent an absolute guarantee.

The repository must contain the published pinned source and reusable-workflow commits. A local branch alone cannot be invoked by another GitHub repository.

## Choose this mode or a persistent workspace

| Need | Mode |
| --- | --- |
| Collect one accessible chat during a limited session and give a reviewer an externally attested archive | GitHub Actions capture (preview) |
| Observe several chats continuously, manage accounts, search and read a growing archive | Local or Docker workspace |
| Prove that messages were never fabricated, recover unseen deletions, or hide live processing from the hosting provider | Neither mode establishes this |

This starts a separate capture with a new login. It does not upload your existing local journal, export the currently open workspace, or reuse its Telegram session. An unfinished cloud capture cannot resume after its runner is destroyed; a new workflow starts a new capture. The helper is English/Russian; its entry points are translated with the rest of the interface.

The workspace's **Exports → Open capture helper** opens the complete wizard inside the panel. The standalone page uses the same wizard, controls and themes. Both keep keys and decryption in your browser. GitHub workflow startup and the temporary Telegram panel open in separate tabs; the wizard tells you when to return. Locking the workspace clears the wizard's in-memory key. Your saved key file remains on your device.

## What is public, and what must stay private

Forking copies project code into your repository. It does **not** export your Telegram account. The recipient workflow input is a public encryption key. Keep `sealed-key.json`, Telegram credentials, login codes, 2FA passwords and the decrypted connection URL out of commits, workflow inputs and public logs.

The workflow publishes encrypted connection/result artifacts for one day. Download both in time; GitHub Actions availability, account limits and billing apply. A public fork is not a promise of unlimited free compute. No payment or GitHub access token is entered into the helper.

The private decryption key stays in your browser/file. Telegram session material and plaintext observations necessarily exist inside the temporary collector. GitHub and the HTTPS tunnel remain trusted infrastructure. Attestation may make the archive digest and workflow identity public; the archive contents are not placed in the attestation. The attestation timestamp is not a message timestamp.

## Troubleshooting

| Symptom | Next step |
| --- | --- |
| No **Run workflow** button | Open your own fork, enable Actions, and sync it with upstream `main`. Do not edit the approved upstream pins to bypass a failure. |
| No `sealed-connection` artifact | Check whether the job started and completed its startup/upload step. Queue, runner, image download, tunnel or repository policy failures can prevent startup. |
| Cannot open the connection | Load the saved key for this run, unzip the downloaded artifact and select `connection.tgwsealed`. The runner must still be active. |
| History is paused | Check the panel's status and use Resume while the session remains active, or finish with the data already collected. Telegram limits and inaccessible content can leave gaps. |
| No `sealed-result` | Cancellation or expiry before selecting a chat produces no archive. A failed collection, attestation or packaging step also prevents delivery. Inspect the failed step without posting credentials. |
| Browser cannot decrypt a large archive | Use the streaming CLI below for packages larger than 256 MiB. A wrong or lost private key cannot decrypt the result. |
| Verification rejects the signer | Use a trusted current TgWitness installation and the exact caller `OWNER/REPOSITORY`. Do not accept a replacement policy supplied with the archive. |
| Telegram still lists the temporary session | End it in Settings → Devices. Logout can fail and a forcibly terminated workflow may not run cleanup. |

Before relying on this preview, try a small chat you control: create a message and attachment, collect them, decrypt the result, run the verifier, check the coverage/media outcomes and confirm Telegram session revocation. Automated checks use a synthetic Telegram client plus a separate real GitHub certificate test; they do not establish live account acceptance.

## Local decryption and verification

Use tools from an independently trusted installation, not executable files supplied by an unknown evidence archive:

```
python -m tgwitness.sealed_crypto decrypt delivery.tgwsealed --key sealed-key.json --out delivery.zip
# Unzip delivery.zip using your archive manager, then:
python -m tgwitness.sealed_verify evidence.zip --bundle attestation.jsonl --repo OWNER/TgWitness
```

Python 3.11+, the project's dependencies, and a recent GitHub CLI supporting `--signer-digest` and `--deny-self-hosted-runners` are required. A CLI key generator is also available: `python -m tgwitness.sealed_crypto keygen sealed-key.json`.

The verifier uses `tgwitness/sealed_policy.json` from the trusted installation. It checks the caller repository, upstream signer workflow, approved signer commit, hosted runner requirement, complete ZIP digest, internal journal and attachment integrity, fresh account-key origin, and expected collector commit. It displays history and media outcomes instead of implying all data was saved. An empty approved-release list fails closed. Updating the policy is an explicit trust decision; never accept an archive's own proposed policy automatically.

For offline use, obtain trusted roots ahead of time from a trusted environment:

```
gh attestation trusted-root > trusted_root.jsonl
python -m tgwitness.sealed_verify evidence.zip --bundle attestation.jsonl --repo OWNER/TgWitness --trusted-root trusted_root.jsonl
```

The timestamp of the attestation concerns the archive's commitment. It does not authenticate message timestamps or the collector's wall clock. See [GitHub's verification options](https://cli.github.com/manual/gh_attestation_verify).

## How the fork is kept outside the capture process

The caller contains a job-level reference to the upstream reusable workflow at a full commit SHA. That workflow explicitly checks out **the upstream repository at a fixed collector SHA**. A default `actions/checkout` in a reusable workflow would check out the caller and is intentionally not used.

The workflow does not restore caller caches, consume caller artifacts, execute caller files, or accept source/image URLs, shell commands, prepared ZIP files, or hashes to sign. It accepts a bounded public recipient and session duration. Actions, the Python base image, and cloudflared are pinned by immutable digests; Python dependencies use the existing hash-locked requirements. The image is built from the trusted source without a cache.

The collector runs as a non-root user with a read-only image, dropped Linux capabilities, resource limits, and no Docker socket or GitHub-token environment. Its only mounts are fresh configuration, workspace, and output directories. The restricted FastAPI application exposes login, dialogs, one-chat collection, status, resume, finish, and cancellation. There is no plaintext download route, general administration route, import route, or signing endpoint.

The supervisor stops the network-facing containers before the attest action reads the final fixed `evidence.zip`. The packaging container has no network. The upload steps name only `connection.tgwsealed` and `delivery.tgwsealed`; neither plaintext evidence nor Telegram credentials are uploaded as artifacts. Cleanup removes the private directories and containers, with no claim of physical disk erasure. Artifact retention is one day; download before expiry.

A fork owner can replace the caller or create a different signed file. The strict verifier must reject the resulting **different signer workflow/digest**. This construction still depends on the absence of exploitable bugs in approved code and on the integrity of GitHub's runner and signing infrastructure.

## Cryptographic handoff

Each recipient key is RSA-3072 (RSA-4096 imports also accepted), exponent 65537. Each envelope has a fresh random AES-256 key and 96-bit nonce. RSA-OAEP with SHA-256/MGF1-SHA256 wraps the AES key. AES-GCM with a 128-bit tag authenticates the complete prefix and payload. The public recipient is DER SPKI in base64; the private key file contains DER PKCS8 in base64.

Envelope bytes are `TGWSEAL1\n`, a big-endian uint32 JSON-header length, the header, ciphertext, and a 16-byte GCM tag. The header has exactly `algorithm`, `key`, and `nonce`; algorithm is `RSA-OAEP-256+A256GCM`. The complete prefix through the header is GCM additional authenticated data. Header size is bounded at 8192 bytes. The CLI streams payloads up to 8 GiB and authenticates before installing the requested output; it refuses overwriting an existing destination. This is a project-specific envelope around standard cryptographic primitives, not an independently audited encryption format.

The original evidence bytes are attested **before** placing the evidence and attestation in the encrypted outer package. This avoids a circular dependency between the archive's hash and a certificate included inside that same archive. For public repositories, attestation metadata (repository, workflow, commit, artifact name and digest) is public. Never put chat names in public metadata.

## Limits and validation

This mode uses the existing signed journal, resumable history reader, and media queue. It collects one visible chat, not Secret Chats, deleted history from before collection, or all account dialogs. Dialog enumeration is capped at 20,000. Existing attachment type/size limits and a 4 GiB export limit apply. Live updates for the selected chat can also be observed during the read; the history is not an atomic Telegram snapshot. Generated screenshots and screen recordings are not part of this mode.

Tests cover synthetic fresh login, scope isolation, media, cancellation, partial deadline completion, failed logout, forbidden API paths and fields, preloaded workspace rejection, wrong-key and tamper rejection, required verifier flags, and browser/Python encryption interoperability. The browser acceptance test uses a plainly labelled mock attestation; it is not a real Sigstore test. Real hosted-runner, Docker, GitHub attestation, and live Telegram acceptance must be reported separately from local synthetic checks.

[GitHub Actions terms](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features#actions) restrict use of hosted runners to the software project's lifecycle. A fork does not remove these restrictions; this preview must not be marketed as unrestricted free production hosting. [Cloudflare Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) are also intended for testing and development. The helper/workflows are suitable for evaluating this feature; production service eligibility remains a separate deployment requirement.

## Maintainer release sequence

1. Commit and review the collector, supervisor, container definition and tests.
2. Pin that collector commit in `sealed-collector.yml`, then commit/review the reusable workflow. Never silently derive the checkout from the caller SHA.
3. Pin the reusable workflow commit in `sealed-witness.yml` and add its workflow/collector SHA pair to `sealed_policy.json` in a trusted release.
4. Publish all referenced commits and the helper, then test an independent fork and the real GitHub certificate. Do not squash away commits referenced by these pins unless the references are regenerated and published again.

See [reusable workflows and attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/increase-security-rating) for the distinction between the caller repository and the upstream signer.


---

# Investigate across all chats

Canonical page: https://phishdestroy.github.io/TgWitness/docs/cases/

Work an entire case across channels, groups, private chats and bots: collect, connect, reconstruct and hand over the evidence.

This walkthrough follows one fictional incident through a whole account. Use collection, search and people profiles to find the source records, [Case Board](https://phishdestroy.github.io/TgWitness/docs/case-board/) to organize and discuss them, and [Report studio](https://phishdestroy.github.io/TgWitness/docs/reports/) to present the findings. The illustrated map below explains the connections in this example.

WORKED CASE / A CHANGED PAYMENT DESTINATION

### One incident. Four conversations. A trail to reconstruct.

A channel announcement points to a bot. An operations group discusses a new payment link, and the bot displays it. The announcement is edited, a private follow-up repeats the destination, and a group message disappears.

Who posted each version?Where did the link appear?Which file was preserved?What changed, and when?

For history loading, optional AI source review, MCP, OCR and outgoing webhooks, see [Work the archive](https://phishdestroy.github.io/TgWitness/docs/archive/).

## 1. Establish coverage across the whole account

Use a dedicated collecting account for whole-account scope. Main accounts can collect selected chats or a Telegram folder.

1. [Connect the collecting account](https://phishdestroy.github.io/TgWitness/docs/accounts/) in its own workspace. Record the case reference, account ID, workspace name and signing-key fingerprint in your case notes.
2. Open **Sources → Observation scope → Investigation mode**. Review **Whole account**, all four source types and **Own actions**. This preset enables saving a new source’s profile and its latest **200 visible messages**. Press **Save scope** and complete the scope confirmation.
3. Press **Load chats**. Compare the sources with the account’s dialog list and review exclusions. Under **Parameters → Chats read from the account’s list**, adjust the initial list limit if needed: the default is 1,000 dialogs, configurable up to 20,000. Chats beyond the limit are discovered when they become active.
4. In **Recording settings**, select and save **All visible activity**. Review attachment types, size limits and free disk space. Start observation and validate a controlled message, edit and deletion before relying on the setup.

ChannelsGroupsPrivate chatsBots

ONE ACCOUNT / ONE SIGNING KEY**All selected account-visible activity → one journal**

Messages · edits · deletion notices · visible reactions · membership events · own actions

“Whole account” covers the chats this account can access, with the configured source types and exclusions. Secret chats are unavailable. New dialogs are added as updates arrive; enabling this mode does not automatically download the complete old history of every existing chat.

## 2. Acquire history and preserve the files

Create a Case Board collection for the investigation and bookmark the relevant saved records. Keep a source register alongside the case: each chat's numeric ID, title, collecting account, access/role, live start, history acquisition, media result and known gaps. Mark a source as acquired after checking the relevant result.

| Need | Action in the panel | What it provides |
| --- | --- | --- |
| History across enabled chats | Sources → Load full history | Available past messages enter the workspace journal, with pause/resume and a signed progress report. [History guide](https://phishdestroy.github.io/TgWitness/docs/reference/history/). |
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

1. Open **Journal**, leave the source filter at **All sources** and search a distinctive phrase, domain, username or saved identifier. Open each matching record, then choose **To board** to keep its chat, message ID and journal reference in the case.
2. For a relevant chat, open **Chats → People → Turn on profiles**, then select a person. Review name/username history, reply relationships, activity, **Also in…** other observed chats and extracted links, wallets or phone numbers. Open the cited journal records.
3. Follow the same numeric Telegram user ID into other chats in this workspace. Treat a matching name, wallet mention or similar avatar as a lead to check; retain the source references and any supporting attribution.
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

Four chats contribute different observations. Follow the source records for every connection; the channel post has no attributed sender.

The numeric IDs and record references are invented for this walkthrough. This explanatory map shows how to connect search results, profiles and inspected records; Case Board stores the corresponding cards and source references.

| Connection | Supporting observation | Conclusion to retain |
| --- | --- | --- |
| Same Telegram account | User ID 71001 in group #146 and private-chat #205 | The same supplied sender ID posted in both chats. Real-world identity remains a separate question. |
| Repeated destination | `pay.example.invalid/new` in #146, button metadata #173, edited post #188 and #205 | The same destination appears in four observed contexts. Attribute its control using additional sources. |
| Same file bytes | Equal full SHA-256 values in completed media receipts #151 and #209 | The two preserved attachments are byte-identical. The full file hashes provide the comparison. |

People profiles describe observed authors and their activity in the *same workspace journal*, within the viewer's permitted chats. This is an observed-author view, rather than a complete membership directory. Adjust the number of supporting citations under **Parameters → Records cited per fact**.

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

Use an [account group](https://phishdestroy.github.io/TgWitness/docs/groups/) to review operating status, share selected settings and export the accounts together. The group package keeps each workspace's signed journal and identity. For one channel or supergroup, eligible accounts can also divide a full history export. Assemble a cross-account timeline in your case notes or analysis tools, retaining the workspace and journal reference for each row.

During longer work, add an [independent witness](https://phishdestroy.github.io/TgWitness/docs/witness/) to retain earlier boundaries. Use the controlled delivery pilot to qualify the accounts’ capture paths and visibility.

## 7. Deliver a checkable case package

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

Check the verifier results, preserve the originals, and retain the coverage report, acquisition outcomes and transfer record with your findings. Write findings in Report studio and choose whether its report includes Case Board material. The example top-level folder combines the separate signed artifacts. For a recipient who needs only selected material, prepare a [minimized handover](https://phishdestroy.github.io/TgWitness/docs/handover/).

## Use the same method for other investigations

**A bot-driven order or payment dispute**

**Question:** what did the bot promise, which button destination was supplied, and what changed afterwards?

**Trace:** channel entry post → saved bot-link preview → bot start parameter → messages and keyboard versions → any panel-issued callback receipt → group/private follow-up. Match each destination to its source record; retain profile descriptions and completed media.

**Deliver:** a timeline of the observed offer and responses, the source references and verified exports. Support any claim about a completed payment with its own transaction records.

**Messages removed after a cross-chat incident**

**Question:** what had already been observed before relevant messages disappeared?

**Trace:** all affected chats → original messages → delivered edits → deletion notices or later missing-on-recheck results → preserved attachments → coverage around the incident. Compare independent account observations with their visibility stated.

**Deliver:** a sequence of preserved versions and explicit unknown intervals. Keep deletion notices, unsuccessful rechecks and any attribution to a person separately supported.

**A participant changes names across several chats**

**Question:** which observed activity belongs to the same Telegram account despite changing names?

**Trace:** numeric sender ID → saved name/username history → replies → other chats in the workspace → mentioned destinations and saved files. Check source records for every asserted connection; keep look-alike accounts separate.

**Deliver:** a cited account-activity timeline and separate hypotheses about relationships. Use name similarity and avatar pHash to choose leads for further source review.


---

# Build a Case Board

Canonical page: https://phishdestroy.github.io/TgWitness/docs/case-board/

Turn saved Telegram observations into a case your team can review together.

Case Board keeps bookmarks, exact-text highlights, saved slices and discussion beside their source references. A collection gives the case a working structure; signed revisions preserve how the team developed it.

## From a message to a case card

1. Open **Investigation → Case Board** in Standard or Expert mode. Create a collection for the case and choose its chat scope.
2. In **Journal** or a saved chat, choose **To board**, or focus the record and press **B**. The card enters Inbox; give it a useful title and move it to your collection.
3. Select a passage in a saved chat message and choose **Highlight → board** to retain the exact quote and message version. Add a note explaining why it matters.
4. Discuss the card, assign a review status, and return to its source context whenever a claim needs checking. Use **Presentation** to walk through the collection with colleagues.

### Follow one changed payment link

Synthetic example · local illustration

1. **Capture.** Open saved observation #142 and its message version.
2. **Bookmark.** Keep the quote, source reference and your question on a card.
3. **Review.** Add a team comment and move the card to Review.
4. **Present.** Walk through the collection and open the cited source context.

#### Saved observation #142

“Use the new payment link.”

Operations chat · message 38 · observed 09:12 UTC

#### Card: changed destination

> Use the new payment link.

Question: which destination appeared in the earlier version?

#### Team review

Analyst: compare with observation #101.

Status: Review · revision retained

#### Source context

Card → saved version → earlier observation

The annotation and the Telegram observation remain separately identifiable.

## Save a useful range once

Shift-click two records in one chat for **Slice between**, choose **Slice by time**, or save the current Journal filters. Review the count before saving. Reopen the slice to apply its saved query; **Show records added since bookmark** reveals later additions.

A time slice follows collector observation time. A message-ID slice can follow the selected messages as later changes arrive. The saved creation boundary lets a recipient compare the original selection with its later state.

## Give each colleague the right role

**Reviewer** reads the board; **Analyst** adds cards and comments; **Operator** also manages collections and review decisions. Workspace and chat permissions apply to cards, source context and discussions. Use named access grants for clear attribution.

## Carry the work into a deliverable

Export a slice as signed JSON, or use CSV for a spreadsheet. Report settings can include bookmarks and slices, with team comments when selected. Choose these contents in [Report studio](https://phishdestroy.github.io/TgWitness/docs/reports/); a saved slice does not automatically configure a report. For a restricted recipient, use the separate [handover controls](https://phishdestroy.github.io/TgWitness/docs/handover/).

Read the [Case Board reference](https://phishdestroy.github.io/TgWitness/docs/reference/case-board/) for signed revisions, exact quote matching, selection verification and permissions.


---

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


---

# Prepare a sharing copy

Canonical page: https://phishdestroy.github.io/TgWitness/docs/handover/

Share the relevant observations while keeping the original workspace intact.

A handover is a separate signed extract. Choose the chats and people, reduce identities or text, and decide which files and team notes belong in the recipient's copy. Its manifest records the selection and the number of unchanged, minimized and omitted records.

## Prepare the recipient's extract

1. Open **Exports → Handover extract**. Write its purpose, choose the chats and optional UTC period, then select **Load people of the chosen chats** if you need named subjects.
2. Choose how to handle everyone else: pseudonyms, omit their messages, or show as recorded. Set message text and attachments independently; optionally mask phone numbers and email addresses.
3. Choose whether to include Case Board bookmarks and slices, or cards with comments. Investigator aliases can replace team names in this copy.
4. Select **Download handover extract**. Open the generated report and selected records locally, verify the archive, and inspect the copy before sending it.

### One original, a deliberate sharing copy

Synthetic example · identity illustration only

1. **Select.** Include the case chat and identify the person the extract is about.
2. **Minimize.** Choose how another participant appears in the sharing copy.
3. **Inspect.** Open the generated archive's report and records before sending it.
4. **Share.** Deliver the checked copy and communicate its trusted fingerprint separately.

#### Original observation

Nora · user 71002

“I received the revised link.”

The source journal keeps this saved observation.

#### Recipient's copy

Show as recorded: Nora · user 71002 · “I received the revised link.”

Pseudonym: P01 · “I received the revised link.”

Omit: this participant's message is left out of the copy.

#### Inspect the actual files

Read report.html and records.jsonl.

Check identities, text, attachments and optional team comments.

#### Signed extract

Selection + file hashes + signed manifest

A separate package linked to its source journal boundary

## Use the controls together

| Control | Effect on the copy |
| --- | --- |
| People | Keep selected subjects identifiable; pseudonymize or omit other participants as chosen. |
| Text | Include all text, only the selected people's and observing account's text, or omit message text and its text-bearing detail fields. |
| Files | Choose files of the selected people and observing account, all shown messages' files, or no files. |
| Case Board | Choose no board material, bookmarks and slices, or cards with team discussion. |

Review free-form text and file contents as well as identities: a pseudonym does not automatically remove every name written in a message or attachment. If a selected preserved file is unavailable, restore it or explicitly omit attachments before generating the extract.

## Keep the copy independently checkable

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Retain the original signed evidence archive and checkpoints separately. The handover records its own projection, so a recipient can check the delivered copy without receiving the entire workspace. [Report studio](https://phishdestroy.github.io/TgWitness/docs/reports/) supplies its reading design; [export verification](https://phishdestroy.github.io/TgWitness/docs/exports/) explains the trusted references.


---

# Manage a group of accounts

Canonical page: https://phishdestroy.github.io/TgWitness/docs/groups/

Manage several collecting accounts together while keeping each account's records and signing identity distinct.

An account group brings connection status, observation controls, shared settings and exports into one working view. It is useful when several accounts cover the same investigation or need a consistent operating setup.

## Open the group overview

In **Accounts**, open the group. Each account shows its observation state, connection route, latest measured route latency when a current check succeeded, and last saved message. **Needs attention** links to the accounts that need work; **Fix** opens the relevant workspace and control.

**Start all** and **Pause all** act on eligible accounts after confirmation. **Group settings** shares selected settings; accounts with their own values keep them until you choose to replace them.

### Review a route change across a group

Synthetic example · illustrative checks and outcomes

1. **Select.** Choose the group and review which accounts will change.
2. **Prepare.** Keep an account's own route when it should remain separate.
3. **Check.** Test the proposed connection and inspect the measured results.
4. **Apply.** Recheck before saving and review the outcome for each account.

#### Case team

Channel collector · Group collector · Reference account

3 separate workspaces

#### Reviewed selection

2 accounts take the proposed route.

Reference account keeps its own route.

#### Preparation checks

Channel collector: Telegram transport 84 ms

Group collector: Telegram transport 91 ms

These numbers are fictional measurements for the example.

#### Application results

Channel collector: route saved, observation resumed.

Group collector: recheck failed, previous settings restored.

Reference account: own route retained.

## Change the route with a review step

1. Select **Change the group route**, then choose the connection type and settings.
2. Choose **Review selection**. Review the listed accounts and their individual route overrides.
3. Select **Prepare and check**. The check uses a fresh Telegram transport; supported HTTP routes also report their HTTPS exit check.
4. Select **Apply checked connection** and inspect each account's result. Previously running observation resumes where application succeeds; idle accounts remain idle.

Latency describes the measured Telegram connection setup. An exit-IP check describes that route at the recorded check time. Account authorization and observation health have their own indicators; a group change can finish with different outcomes per account.

## Use overlapping access

**Chats several accounts see** shows shared sources and the available workspace-observation coverage. Eligible channels and supergroups can use **Export with … accounts** to divide one chat's history acquisition. Private chats and ordinary groups stay with the starting account because their message numbers belong to an account's history.

## Export the group as a package

**Export group** creates one ZIP containing each account's signed export and a signed list of those files. The original workspace identities and fingerprints remain available for verification. Build a cross-account narrative using those references; a single merged timeline is still assembled separately.

Continue with [report design](https://phishdestroy.github.io/TgWitness/docs/reports/), [a Case Board within a workspace](https://phishdestroy.github.io/TgWitness/docs/case-board/), or [export verification](https://phishdestroy.github.io/TgWitness/docs/exports/).


---

# See how evidence works

Canonical page: https://phishdestroy.github.io/TgWitness/docs/concepts/

A message can change. The record of what you observed should remain checkable.

Explore two small experiments below. They use fictional messages, stay in your browser and never connect to Telegram.

## From a chat export to a verifiable record

[Telegram Desktop exports](https://telegram.org/blog/export-and-more) save available chat history and media as HTML or JSON for offline use. TgWitness adds an ongoing journal of received changes, signatures on observations and exports, and checkpoints that recipients can compare independently.

| Task | Telegram Desktop export | TgWitness |
| --- | --- | --- |
| Read saved conversations | HTML or JSON with selected media | Saved chats, searchable journal and offline reports |
| Follow a change over time | The history available when exported | Earlier captured versions, later edits and deletion observations retained together |
| Check files after handover | Standard HTML/JSON export files are unsigned | Signed manifest, per-record signatures and sealed HTML/PDF/JSON reports checked against a trusted collector key |
| Compare with an earlier retained state | Keep a separate reference copy or hash | Signed checkpoints, a separate witness and optional external timestamps |

The file-signing comparison is based on the [Telegram Desktop export writers](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) reviewed on 2 November 2026. TgWitness signs with the collector’s key; the checks below show how a recipient uses it.

## One message, three observations

When Telegram delivers a new message, an edit and a deletion notice, the collector appends three separate observations. The edit does not replace the first record. A deletion notice does not erase it.

01 / MESSAGE JOURNEYIllustrative sequence

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Collector · Journal · update → · append →

CURRENT CHAT VIEW Message #42

Message deleted

The message has disappeared from the chat view.

OBSERVATION JOURNAL 3 records

1. 01

   `message.new`

   Meet at 10:00

   ✓
2. 02

   `message.edited`

   Meet at 11:00

   ✓
3. 03

   `message.deleted`

   Deletion notice for #42

   ✓

All three received observations remain in the journal.

Simplified path for one already selected source. Operational records also share the real journal. Capture depends on what the account can see and what Telegram delivers.

A deletion notice supplies neither a reliable deletion time nor the person who deleted the message. Keeping those values unknown preserves the distinction between an observation and a guess.

## Change a record. Follow the hash.

Each record contains the previous record’s hash. Its own hash covers the event fields, including that link. An externally retained checkpoint pins a specific journal length and head hash.

02 / HASH-CHAIN SANDBOXReal SHA-256 · sample records

RECORD 01**Message received**`h₁ = SHA-256(e₁)`Links to 64 zeroes

RECORD 02**Meet at 11:00**`h₂ = SHA-256(e₂)`Includes h₁

RECORD 03**Deletion observed**`h₃ = SHA-256(e₃)`Includes h₂

RETAINED ELSEWHERE**3 records · head `h₃`**Compare this fixed boundary with the supplied journal.

Altering an event changes its hash. Rebuilding the chain changes its head. Removing the tail makes it shorter than the retained checkpoint.

**Inspect record 2 and the full hashes**

This is the exact UTF-8 JSON hashed in this example. Values are fictional; the nine fields and serialization match the journal format.

```

```

Saved record 2 hash

``

Recalculated record 2 hash

``

This sandbox computes hashes, not signatures. The real verifier also checks every event’s Ed25519 signature, sequence and link. Rebuilding hashes alone cannot create valid signatures under the trusted key.

## The actual rules, in a few lines

HASH + SIGNATURE

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** serializes the nine event fields as UTF-8 JSON: sorted keys, no extra whitespace, no ASCII escaping and no NaN/infinity. The event’s `previous_hash` is hi−1. The displayed h0 means 64 zero characters; signatures cover the 32 raw digest bytes.

The nine fields are `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` and `previous_hash`. This is TgWitness’s [documented JSON encoding](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#event-canonicalization); the hash and signature themselves are not hash-input fields.

RETAINED CHECKPOINT

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Verify the checkpoint signature under the pinned collector key, then compare its boundary with the verified journal. A later export may contain more records; it must still agree at the earlier checkpoint.

## Three questions, three different checks

[01 / INTEGRITY**Did this record change?** Verify hashes and signatures against a separately trusted key.](https://phishdestroy.github.io/TgWitness/docs/exports/)[02 / CONTINUITY**What was retained earlier?** Compare a signed export with checkpoints kept by a separate witness.](https://phishdestroy.github.io/TgWitness/docs/witness/)[03 / DELIVERY**Did these test events arrive?** Match controlled send, edit and delete actions against each account’s journal.](https://phishdestroy.github.io/TgWitness/docs/cases/)

Use signatures to check the retained records, checkpoints to compare an earlier boundary, and controlled delivery tests to measure collection. Each answers a specific question. [Read the verification scope and trust assumptions.](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope)

Follow the [whole-account investigation](https://phishdestroy.github.io/TgWitness/docs/cases/) from acquisition to case package.


---

# Keep it secure

Canonical page: https://phishdestroy.github.io/TgWitness/docs/security/

Know the routes for Telegram, public proxy lists and optional external services. Know what each secret unlocks, what the protections cover and what they leave to you.

**127.0.0.1**panel address by default

**256-bit**random panel token

**0**CDNs, analytics or remote fonts

**Ed25519**signature on every record

## Where everything lives

The collector, its panel and every saved record stay on the computer or server you run it on. Telegram is the only destination by default; each other one is a separate switch.

06 / WHAT LEAVES THE MACHINEYour installation

YOUR COMPUTER OR SERVER

**Panel**127.0.0.1:8787 · bearer token

**Collector**one Telegram client per workspace

DATA DIRECTORY

**Journal**SQLite · hash-chained · signed

**Media**files named by SHA-256

**Vault**Fernet · session, API pair, signing key, proxy

- **Telegram**Always · through your route

  The account's MTProto connection: direct, SOCKS5, HTTP or MTProxy. Hide IP mode waits for a working proxy. Direct fallback requires a mode that explicitly permits it.
- **Off-site copy**Optional · off by default

  Journal, files and checkpoints encrypted with AES-GCM before upload to S3-compatible storage. The key stays with you; attachments are named by keyed hashes, not their content hash.
- **Notifications**Optional · off by default

  Problems and change counts with chat titles. Message excerpts are sent only if you turn them on.
- **Timestamp authority**Optional · off by default

  Only the SHA-256 of a signed checkpoint and a random nonce. No messages, no chat names.
- **Witness**Optional · off by default

  Pulls signed checkpoints and capture counters with a read-only token. It cannot read conversations or change settings.

Default: only the Telegram connection leaves this machine.

Optional destinations are configured per workspace. Message text and media are stored unencrypted in the data directory: protect it with disk encryption and file permissions.

## What each secret unlocks

| Secret | Where it is kept | What it unlocks | If it leaks |
| --- | --- | --- | --- |
| **Panel token** | `panel-token.txt` in the data directory; the browser keeps it for the tab only | Everything in every workspace: read and export, change scope, sign in accounts | Stop TgWitness, delete `panel-token.txt`, start it again: a new token is created |
| **Telegram session** | Vault, encrypted (`credentials.enc`) | The Telegram account itself | End the session in Telegram under *Settings → Devices* |
| **Signing key** | Vault, encrypted (`signing.enc`) | Signing records that verify under your fingerprint | Checkpoints kept elsewhere, a witness and timestamps show what existed before |
| **Vault key** | `vault.key` beside the data, or an external master key for a new data directory | Decrypting the vault | Treat the session and signing key as leaked too |
| **Witness token** | On the witness host | Read-only: signed checkpoints and health | Delete it on the Witness page; create a new one |
| **Off-site copy key** | Vault; download it once for recovery | Decrypting the off-site copy | Whoever also holds the stored objects can decrypt them: treat that copy as exposed |

## What the protections cover

### Covered

- A changed, removed or reordered record in an export: the hash chain or a signature no longer verifies.
- A journal cut back or rebuilt after a checkpoint was kept elsewhere: the retained checkpoint no longer matches.
- Guessing the panel token: 256 random bits, compared in constant time; after 15 failures a minute an address is refused.
- Hostile chat content: text is inserted as text, never as HTML; attachments download as files; the panel loads nothing from other sites.
- A copied data directory with an external vault key: sessions and signing keys stay encrypted without the master key.

### Left to you

- The main panel token has full control. Give other people scoped access to the accounts, chats and actions they need; keep the main key private.
- An administrator of the machine can read everything and rewrite and re-sign the journal. Keep the fingerprint and checkpoints on another system.
- Message text and media are not encrypted by TgWitness. Use disk encryption and strict permissions.
- Plain HTTP beyond localhost shows the token on the network. Use HTTPS or an SSH tunnel.
- Check saved records with signatures and checkpoints. Review collection coverage and test delivery for the accounts and sources you use.

[Share access to a case](https://phishdestroy.github.io/TgWitness/docs/access/) with permissions, expiry and session limits. A witness token remains a separate credential.

## Harden an installation

0 of 8 done

1. **Use a dedicated Telegram account** — never your main one. The panel token and the session give full control of it.
2. **Keep the panel on 127.0.0.1.** Reach it remotely only through HTTPS (the bundled Caddy configuration) or an SSH tunnel.
3. **Encrypt the disk** that holds the data directory: message text and media are stored as they arrived.
4. **Restrict the data directory** to the service account. New directories get mode 0700 on Unix; on Windows, set the folder's permissions.
5. **Keep the vault master key elsewhere** on servers: set `TGWITNESS_VAULT_KEY_FILE` before creating the data directory.
6. **Save the signing-key fingerprint and checkpoints** on another system, and add a witness on another host.
7. **Never upload** `data/`, sessions, `panel-token.txt` or vault keys to GitHub or a chat.
8. **Do not log** `Authorization` headers or request bodies at a reverse proxy.

**Can I change the panel token without losing data?**

Yes. The token only opens the panel. Stop TgWitness, delete `panel-token.txt` from the data directory and start it again; the journal, sessions and keys are untouched. With `TGWITNESS_TOKEN` set, the environment value is used instead of the file.

**Why are messages not encrypted at rest?**

The collector must read them to search, compare versions and export. Encrypting them with a key on the same machine would add little against someone who can read that machine. Disk encryption protects a stopped or stolen disk; strict permissions protect a running one.

## Report a vulnerability

Use **Security → Report a vulnerability** in the GitHub repository. Include the version, the impact and a minimal synthetic reproduction. Never send credentials, account directories or real evidence archives. If private reporting is unavailable, open an issue asking for a private channel without exploit details.


---

# Set up a witness bot

Canonical page: https://phishdestroy.github.io/TgWitness/docs/witness/

Let a separate process check the journal and publish signed checkpoints to your channel.

## Two hosts, two signing keys

HOST A / COLLECTOR**Account + journal**

Telegram session
Collector signing key

Read-only checkpoint endpoint

← request
signed answer →

HOST B / WITNESS**Verify + retain**

Pinned collector fingerprint
Separate witness signing key

Own journal + bot token

Witness → Telegram Bot API →**Your channel · signed TGW1 posts**

The witness pulls checks itself. Collector access is read-only. Bot publication uses the witness’s connection and token; no account session is given to the witness.

03 / CHECKPOINT DECISIONSIllustrative answers

LAST ACCEPTED**120 records**`head 9c7d…`

NEXT ANSWER**128 records**`head a4f2…`

Accepted: the count grows, the signature verifies and the key matches. The witness retains this new boundary.

All answering examples assume a valid signature and the pinned key. Hashes here are abbreviated illustrations. A larger count alone cannot prove that the entire old prefix is unchanged; compare an export with retained checkpoints.

## Prepare a bot and a channel

Create a bot with BotFather and allow it to post in a channel you control. Choose a computer or server for the witness. A separate host and operator provide stronger independence than a second process on the collector’s server.

## Three steps in Extras

1. **Read-only access.** Open **Extras → Independent witness**, create a witness token and save the access file. It allows reading checkpoints and health, not conversations or collector controls.
2. **Channel and interval.** Choose a Telegram channel or a Discord webhook and enter a collector address reachable from the witness. Save the settings file.
3. **Launch.** Put `witness.json`, `witness-token.txt` and a `bot-token.txt` created on the witness host together. Run the commands below in the installed project environment.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Downloading the files does not start the witness. Check that the first signed post appears in the channel, then retain the witness’s public-key fingerprint separately.

For Discord, save the channel’s webhook URL as `discord-webhook.txt` instead of the bot token. A witness posts to one place, a Telegram channel or a Discord channel; checks longer than a Discord message arrive as an attached file.

## Choose how often to publish

Publishing every check creates a regular external record. At five-minute intervals, that is about 288 posts per workspace per day. The advanced settings also offer publication on changes or problems, a proxy and a custom Bot API address.

**What does the bot actually attest to?**

The witness asks the collector for a signed checkpoint, verifies it against the expected key and keeps a separate signed journal. It records missing responses and rejected answers as well as successful checks. Publication still depends on the witness running and reaching Telegram’s Bot API.

It checks the collector’s reported journal state. It does not independently observe every Telegram message. For that, add the controlled delivery test.

## Check the evidence later

Keep the witness journal, channel posts and independently saved fingerprints. The [full verification procedure](https://phishdestroy.github.io/TgWitness/docs/reference/witness/#verify) compares them with the collector’s signed export.


---

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


---

# Share a case

Canonical page: https://phishdestroy.github.io/TgWitness/docs/access/

Share the case someone needs. Keep control of the rest.

01**Choose the evidence**

Select whole account workspaces or individual recorded chats.

02**Choose the actions**

Allow viewing, export or the specific operational permissions the person needs.

03**Set the limits**

Issue a personal token with an expiry, session limits and optional IP restrictions.

Collection scope decides what is recorded. Access scope decides what a person can see and do.

## Give someone access

1. Sign in as the administrator and open **Access**.
2. Name the access and select workspaces and chats.
3. Keep **View** for a reviewer. Add **Export** if they should download records.
4. Set limits, then press **Create access**.
5. Copy the token shown once. Send it privately with the panel address.
6. Check the allowed view in a separate browser session before handing it over.

## Start with the job they need to do

| Person | Access | Result |
| --- | --- | --- |
| Reviewer | Selected chats; view only | Read the captured conversation without changing collection. |
| Analyst | Selected chats; view and export | Review and download the records needed for the case. |
| Operator | Selected whole workspaces; sources and collection | Manage what is observed and start or stop collectors. |

These are configurations you choose, not fixed roles. Account-wide settings and full journal exports stay closed to chat-limited access even when another permission is enabled. All-workspace access includes future accounts.

## Change your mind at any time

Edit the access to change what subsequent requests can do. End one session or revoke the whole access to end all its sessions. Files already downloaded cannot be recalled. Ending a panel session does not stop collection.

**Session and IP limits**

Limit parallel sessions and successful sign-ins, set an absolute end date, allow IP addresses or subnets, or bind access to its first sign-in address. Session expiry measures inactivity; an open panel's polling counts as activity. Check the client address shown by the application when it runs behind a proxy or tunnel.

**The main key and the activity log**

The administrator keeps the main panel token. Issued access cannot manage other people's access or open the administrator console. The console shows current-process activity across workspaces; signed access records retain grant and session events without tokens. Workspaces share the host process and do not isolate data from the server administrator.

Use the [full permission reference](https://phishdestroy.github.io/TgWitness/docs/reference/access/) for all seven permissions, session rules and the administrator boundary.


---

# Keep it running

Canonical page: https://phishdestroy.github.io/TgWitness/docs/server/

Keep the collector available and its data intact across restarts.

## Choose a launch method

For a native installation, use the [launcher](https://phishdestroy.github.io/TgWitness/docs/start/) and the service examples in [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). For Docker, install Docker with Compose and run from the project directory:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

The default panel listens on the host’s loopback address, port 8787. Open it locally or through an SSH tunnel. Use the token from the second command to unlock the panel.

## Keep the whole data directory

Native installations use `data/live`. Docker uses the persistent `tgwitness-data` volume. Keep journals, account sessions, keys and operational state together. A signed export is useful evidence, but it is not a full installation backup.

1. Stop collection before taking a consistent backup.
2. Copy the full private data directory to protected storage outside the host.
3. Test restoration into an isolated installation before relying on the backup.

## Check after a restart

Confirm the expected workspace and key, Telegram connection, selected sources and new message capture. Saved MTProto state and catch-up help recover updates that Telegram still retains. They cannot reconstruct every expired update or an edit deleted before capture.

Container health means the web server responds. Use a controlled message and a witness check to assess collection and external publication.

## Publish only what you intend

The deployment reference includes HTTPS examples, persistent-volume commands, updates and restore steps. Docker commands are provided for deployment; the current [validation record](https://phishdestroy.github.io/TgWitness/docs/reference/verification/) identifies the environments actually tested.


---

# Find what went wrong

Canonical page: https://phishdestroy.github.io/TgWitness/docs/troubleshooting/

Start with the symptom. Check one layer at a time.

## The panel asks for a token

Use the panel token from the local file shown by the launcher. For Docker, run `docker compose exec tgwitness cat /data/panel-token.txt`. A Telegram login code, BotFather token and read-only witness token serve different purposes.

## Telegram does not connect

Open connection settings and run the connection check. If using a public proxy, try another entry and save the route explicitly. Check the proxy type and supported secret format. Refreshing a public list does not switch the account’s route.

## Connected, but no new messages

1. Check that observation is running in the right workspace.
2. Confirm the source is selected and visible to that account.
3. Send a unique new message in a controlled group and look for that exact text.
4. Review the operational journal for interruptions, delayed work or Telegram errors.

Historical snapshots and new-message events are different. A quiet source can be connected without producing new messages. Use a controlled delivery test when completeness matters.

## FloodWait or a gap after a restart

FloodWait means Telegram requires a pause. Wait for the indicated period and review collection workload; repeated reconnects do not remove the limit. Saved update state helps catch up after a restart, but expired updates and some interruption windows remain limitations. Record the gap rather than treating the journal as complete.

## The bot is configured but posts nothing

Make sure the witness process is actually running, the bot can post in the channel and the witness can reach the collector and Bot API. Inspect its journal for failed publications. A successful collector poll alone does not confirm a channel post.

## Where is GitHub token integration?

**Planned.** Extras describes the proposed fork and build verification workflow. There is currently no GitHub token form or automated attestation that a running installation matches a repository. See the [current feature status](https://phishdestroy.github.io/TgWitness/docs/reference/features/).

When reporting a problem, include the version, operating system, steps and a redacted error. Keep sessions, tokens, private messages and the data directory out of public issues.


---

# Quick start

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/quickstart/

Every way to install and launch TgWitness: Windows package, Python, Docker and the synthetic demo, with first checks.

**English** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [Українська](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [Português (Brasil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [اردو](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [हिन्दी](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [简体中文](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness is a standalone application for observing Telegram groups and channels that your accounts can access. It runs locally with its own data directory.

**First visit?** [Explore the demo](https://phishdestroy.github.io/TgWitness/docs/reference/quickstart/#explore-the-interface) before connecting an account. [Choose a guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) for proxies, witnesses, exports or server setup.

## Install and start

[GitHub Actions capture (preview)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

Choose one method. Portable downloads become available after a release build is published:

| Host | Nothing installed | From source: Python 3.11+ | Docker: Engine/Desktop with Compose 2.20+ |
| --- | --- | --- | --- |
| Windows | Extract `TgWitness-<version>-windows-amd64-portable.zip` from GitHub Releases, double-click `TgWitness.cmd` | Double-click `Start.cmd` | Double-click `scripts\Docker.cmd` |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

For the source methods, [download and extract current `main`](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) or clone the repository:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

`Start.cmd` offers to install Python 3.12 for your Windows user if no suitable Python is found (winget, or the signed python.org installer). `start.sh` prints the exact install command for your Linux distribution or macOS if Python is missing. The first source launch creates `.venv` and installs dependencies automatically.

Docker builds the application and starts it in the background; host Python is unnecessary. `scripts\Docker.cmd` and `scripts/docker-start.sh` print the panel address and token when the container is healthy. The equivalent Docker commands on every supported host are:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Open **http://127.0.0.1:8787**. Use the token printed by the Docker helper or the second Docker command, or read **data/live/panel-token.txt** for a portable or source installation. Continue at **Connect Telegram** below. Native and Docker installations use separate storage; starting Docker does not import an existing native journal.

For a server, [deployment](https://phishdestroy.github.io/TgWitness/docs/reference/deployment/) covers automatic HTTPS, restart, published images, updates, and backups.

## Explore the interface

1. Run **TgWitness-Demo.cmd** in the portable package, **scripts\Demo.cmd** in a Windows source folder, or `sh start.sh --demo` on Linux/macOS. A source launch first creates `.venv` and installs dependencies.
2. Open **http://127.0.0.1:8787**.
3. The local demo opens the sample journal automatically. No token copy is needed for direct local access.

Demo messages are fictional. Demo mode cannot connect a real Telegram account.

## Connect Telegram

> [!WARNING] **Do not use anything you cannot afford to lose.** We strongly advise against connecting personal or valuable accounts and against creating an API ID / hash on an account you value. Telegram bans accounts unpredictably and often permanently, regardless of the client. A smooth test run depends on Telegram, not on TgWitness, and guarantees nothing for later.

1. If the native demo is running, stop it and run **Start.cmd** or `sh start.sh`. Otherwise, keep the live installation started above running.
2. Use the panel token for your installation method to open the panel.
3. If you need a proxy, save it under **Account → Settings → Connection settings → Change connection route**.
4. In **Account**, enter your phone number and press **Continue**, choose **QR code → Show QR code**, or select files and press **Connect account**. **API ID + Hash** is optional: the workspace uses its saved or imported pair, or a working pair from the built-in pool. To use your own app, paste one `API ID:API Hash` pair into API ID. For a complete authorization key, choose **Auth key**, paste all 512 hexadecimal characters, and select the supplied DC ID. User ID is optional and checked if entered.
5. Complete your selected sign-in method: phone/code/2FA, confirmation from a signed-in Telegram app for QR, or a supported authorized session import.
6. Check the displayed account ID. Open **Sources**: your chats load automatically; add your groups.
7. Under **Choose which changes to preserve**, select event categories or the **Messages, edits & deletions** preset, then save monitoring settings.
8. Choose attachment settings separately, then press **Start observation**.

API credentials identify your application; they do not authorize an account by themselves. Private groups need no public username, but your account must have access.

For existing accounts, see [accounts and session formats](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/): the panel accepts Telethon StringSession, Telethon/Pyrogram SQLite, single-account TData ZIP, and supported account JSON. Select a session and its companion JSON together, press **Connect account**. QR login is also available with the same optional API settings. TDLib, bot sessions and CSV/JSON account inventories are unsupported.

For several accounts, use **Accounts → Import accounts** and select their supported session files. Companion JSON files are paired by basename; each imported account gets its own workspace. See [bulk import and account groups](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#bulk-import-and-account-groups).

To add another account, press **+** beside the account selector or open **Account → Settings → Connection settings → Workspaces**, or use **Accounts**. Workspaces have separate sessions, journals, keys, sources and queues. Switching views leaves other collectors running. The same Telegram account cannot be assigned to two workspaces in this installation. There is no fixed number of workspaces; they share one process, so capacity depends on the machine.

The live panel token protects access to your Telegram authorizations and saved material; it is separate from Telegram API credentials. Only an explicitly started, directly accessed local demo gets automatic entry. A remote/proxied demo still uses `data/demo/panel-token.txt`.

## Review and export

- **Journal:** search and filter observations by source and event type.
- Select an event to inspect its original record, attribution and saved versions.
- Edit details show the available before/after content. Deletion details show the last captured content, if any; an unknown actor remains unknown.
- **Exports:** signed ZIP, JSONL, CSV and offline HTML.
- **Full chat export** (Sources → Full chat export): download one chat's entire visible history as a signed bundle with `chat.json` (Telegram-export style) and a readable `chat.html`. Private chats work when the account is a member. It is a current snapshot, not a reconstruction of deleted or previously edited messages. Verify a copy with `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256`.
- **Save checkpoint:** keep the signed journal boundary outside the collector.
- **Download signed run receipt:** preserve the collector's program/version record.
- **Prepare timestamp request:** prepare an offline request for a timestamp authority; follow [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/docs/reference/timestamp/) to obtain and verify a response.
- **Verify journal:** check event signatures and chain links. ZIP export also checks media.

Supported browsers save large exports directly to a chosen file. Other browsers buffer at most 128 MiB. While the server is running, the streaming CLI supports larger downloads without buffering the whole response:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

For another workspace, add `--profile ID` using **Exports → Workspace ID**. For a remote server, add `--url https://your-server`. The default transfer limit is 5 GiB; `--max-mib` changes it. Signed ZIP content has a separate 4 GiB uncompressed verification limit by default (**Parameters** raises it; verify such archives with `verify.py --max-gib N`). Verify the archive using a trusted copy of the verifier and an independently retained key fingerprint/checkpoint.

## Check the installation

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check` probes local dependencies, signing support, storage, key configuration and the listening address. It does not install anything or connect to Telegram. A busy port may mean another instance is running. Use a different `--port` or stop it first.

The launcher installs into `.venv`. Auxiliary `python -m tgwitness...` commands must use `.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on Linux/macOS, unless that environment is already activated.

## Sessions, protection and operation

A closed, consistent Telethon SQLite `.session` can be converted locally with `python -m tgwitness.sessions account.session --out account.tgwitness-session`, then loaded in Account. Direct file import and QR login are also available. See [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/docs/reference/connection/) for login formats, SOCKS5, HTTP CONNECT, MTProxy and external master keys.

**Pause observation** stops collection. **Lock** only closes browser access. Closing a tab leaves the collector process running. Stopping the process interrupts collection; a history snapshot cannot reconstruct all missed edits or deletions. See [how collection works](https://phishdestroy.github.io/TgWitness/docs/reference/collection/) for event policies, attachment queues, account isolation, and restart behavior.

Sessions and secrets are encrypted. Message content, media and exports require an encrypted disk or volume. Signatures establish integrity relative to a trusted key; they do not establish Telegram origin or prevent fabrication by an operator who controls the collector and its key.

Read [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/docs/reference/operations/) for backup/restore, [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/docs/reference/deployment/) for hosting, and [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) for service examples. The installed panel also includes an offline setup guide at `/guide.html`.

Actual verification and remaining boundaries are recorded in [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/docs/reference/verification/) and [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md).


---

# Install, verify and update

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/installation/

Install with one command, check signatures and hashes, update and remove an installation.

[Project](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Quick start](https://phishdestroy.github.io/TgWitness/docs/reference/quickstart/) · [Deployment](https://phishdestroy.github.io/TgWitness/docs/reference/deployment/)

## Install with one command

The guided installer includes a private Python runtime. Use the same address for future installations: each publication updates the installer, hashes, signatures and build information together.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

On an Ubuntu server, run as root to install a background service. On a desktop, run as your normal user.

**Windows (PowerShell or Command Prompt):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

No administrator is needed on Windows. The child PowerShell process leaves your terminal open with the result. Python and dependencies stay in the installation.

On Ubuntu, choose **This computer**, **Temporary HTTPS link** or **Own domain**. The installer prints the panel address and access key. For a temporary link, open that HTTPS address in your browser and enter the key. With local access on a remote server, use an SSH forward from your computer (`ssh -L 8787:127.0.0.1:8787 user@server`) and open `http://127.0.0.1:8787`. On macOS and Windows, the local panel opens in your browser; keep its terminal running.

Sign in to Telegram in the panel and choose what to collect. Installation alone does not start Telegram collection.

## Where everything runs

`get.destroy.tools` is a **Cloudflare Worker serving static downloads**. It has no TgWitness panel, Telegram session or user evidence database. It is not routed to a project VPS. The application runs on the machine where you execute the command.

| Installation | Program | Data |
| --- | --- | --- |
| Ubuntu as root | `/opt/tgwitness` | System service: `/var/lib/tgwitness-<installation ID>`; use `tgwitness paths` for the exact path. |
| Linux / macOS user | `~/.local/share/tgwitness` | `data/live` under that installation. |
| Windows user | `%LOCALAPPDATA%\TgWitness` | `data\live` under that installation. |

Set `TGWITNESS_INSTALL_DIR` to choose another folder. Installed versions and data are separate. The installer does not upload your accounts, messages or keys to the download site. Choosing a Cloudflare tunnel sends panel traffic through Cloudflare; using your own domain points to your own server.

Every installation includes **START-HERE.html** and **START-HERE.txt**, with local paths, commands and links to the repository. Run `tgwitness guide` to open the guide. On Windows, use `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` in PowerShell.

## Verify before running

The one-line command trusts HTTPS for its initial script. That script checks SHA-256 and the project's RSA signature on the application and constraints before installation. You can also download and verify the initial script first.

The public release key is [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). Its SHA-256 is:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Retain this fingerprint from a repository revision you trust. A checksum from the same download server detects a mismatch; the independently trusted public key is what authenticates a release signature.

Use a new, empty directory for the verification downloads below.

**Linux / macOS — run in a new, empty download directory** (requires curl and OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

The `&&` chain stops before execution if a download, key fingerprint or signature check fails. If publication happens between downloading the script and its signature, download both again. Old installers keep their immutable package URLs.

**Windows — inspect the SHA-256 before running:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Compare the hash with the `install.ps1` line. For an independent signature check, use OpenSSL (for example, from Git Bash) and the same public-key fingerprint above:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Windows installation itself verifies package signatures with .NET and does not require OpenSSL. These are detached RSA-3072 / SHA-256 signatures, not Authenticode. The [manifest](https://get.destroy.tools/manifest.json) records the software version, exact Git commit, immutable release ID and each artifact's SHA-256. The page links to the corresponding source. The manifest and checksum list also have detached signatures (`manifest.json.sig` and `SHA256SUMS.txt.sig`).

## Update an existing installation

**A new publication updates the download site; installed programs update when you run the installer again.** There is no unattended updater or automatic restart of a running collection. The current installer channel is **preview**; it follows published, checked builds from `main`, whose commit can be newer than the last numbered GitHub release. The page's version comes from `pyproject.toml`; its commit and build ID distinguish updates within the same preview version.

Use the same installation folder and OS user as before. Back up the complete data directory with collection stopped; `tgwitness paths` identifies it. A signed export is not a complete installation backup.

**Ubuntu root installation at `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

After a successful installation:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

For a Linux/macOS user installation, use its original `TGWITNESS_INSTALL_DIR` or the default and run the first installation command again. Close a foreground panel before updating and start it again afterwards. For a configured Linux user service, run its `tgwitness restart` command.

**Windows:** close the running panel, run the Windows installation command again, then open `bin\tgwitness.cmd` in the same installation. The installer retains data, sessions, access settings and signing keys. It switches the launcher only after the new environment passes its checks; failed installation leaves the previous launcher in place. Keep the pre-upgrade backup for storage-format changes.

## Everyday commands on Ubuntu

| Command | Result |
| --- | --- |
| `tgwitness open` | Current panel URL and access key. |
| `tgwitness paths` | Exact program, data and guide paths. |
| `tgwitness guide --print` | Offline operating instructions. |
| `tgwitness status` / `tgwitness logs` | Availability / service logs. |
| `tgwitness stop` / `tgwitness start` | Stop / resume the service; retain data. |
| `tgwitness token rotate` | Replace the administrator key and end browser sessions. |
| `tgwitness tunnel off` | Disable the public quick tunnel; retain the local panel. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Create a quick-tunnel link / replace its address. |

See [Access](https://phishdestroy.github.io/TgWitness/docs/reference/access/) for colleague tokens, sessions and IP restrictions, and [installer publishing](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) for the GitHub-to-Cloudflare release workflow.

## Remove TgWitness

There is no uninstaller: you stop the panel and delete its folders. Deleting the data folder destroys journals, signing keys, Telegram sessions and saved files for good. Before that:

1. Export what you need (**Exports → Download signed ZIP**) and keep the signing key fingerprint and checkpoints outside this machine. To keep the workspace itself, copy the whole data folder with collection stopped.
2. Delete servers created under **Extras → Server 24/7** from **Your servers** or with `python -m tgwitness.cloud destroy`; the provider bills them until they are deleted.
3. End each account's session in Telegram under **Settings → Devices**. Deleting the files does not sign the session out on Telegram's side.

**Ubuntu root installation.** Note the data folder, stop the service, then remove the service, the folders and the shortcut:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Linux or macOS user installation.** Close the panel. A configured Linux user service is stopped with `systemctl --user disable --now tgwitness-<ID>`; its unit is in `~/.config/systemd/user/`. Then delete `~/.local/share/tgwitness` (or your `TGWITNESS_INSTALL_DIR`) and the `~/.local/bin/tgwitness` shortcut.

**Windows.** Close the panel and delete `%LOCALAPPDATA%\TgWitness` (or your `TGWITNESS_INSTALL_DIR`). The installer adds no service, scheduled task or shortcut.


---

# First setup and settings

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/settings/

The setup wizard, goals, interface levels, connection routes and settings shared by an account group.

[Accounts](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/) · [Connection](https://phishdestroy.github.io/TgWitness/docs/reference/connection/) · [Access](https://phishdestroy.github.io/TgWitness/docs/reference/access/)

A new workspace opens `/first-run`: language and time, interface level, goal, connection, Telegram and chats. Each answer is saved on the server as soon as it changes, so a reload continues the same step. The last screen lists the answers and lets you go back to any of them.

Language, IANA time zone, theme and level are stored per operator and per workspace. The defaults are the browser language, the device time zone, the system theme and the Simple interface. Changing the language keeps the panel session. Times in the signed journal never change.

`/settings` edits the same records as the wizard. Search covers the main fields, parameters and the extended forms; a hidden field can be opened without changing the level. Levels only change what is shown: the server checks permissions on its own. Collection settings and the first connection belong to the workspace administrator.

| Level | Fields | Sidebar |
| --- | --- | --- |
| Simple | Only the essentials | Home, Chats, Changes, Archives, Settings |
| Standard | Common settings with explanations | Adds Case Board, Accounts and Access |
| Expert | All fields, limits and technical details | Adds Sources, Extras, Ask the archive, Parameters, Account, System log and Integrations |

The [panel guide](https://phishdestroy.github.io/TgWitness/docs/reference/panel/) describes each section.

## Goals

| Goal | Collection | Files | Outside services | Server address |
| --- | --- | --- | --- | --- |
| Archive copy | Off; **Start** runs an export | Photos up to 20 MB | Off | Automatic |
| Follow chats | Continuous | Photos and videos up to 60 seconds / 20 MB | Timestamps and problem notifications | Automatic |
| Evidence | Continuous | All files up to 1 GB | Timestamps, drand, notifications | No, hide it |

Off-site copy, the witness bot and the code check are recommended for evidence. Storage and notification addresses need a destination first. A feature that talks to an outside service asks to allow requests outside Telegram; turning that off offers to switch off timestamps, notifications and the off-site copy with it.

Changing the goal shows the difference first, and manual changes can be kept. A field that differs from the goal is marked **Changed by you** and can be restored. The settings revision keeps a reviewed difference from being applied over a change made in another tab.

## Connection

**Automatic** tries public MTProxy servers, then WARP, then a direct connection, the last only when the server's address may be shown. Automatic and WARP can install hash-checked components and register the server with Cloudflare. WARP uses the existing wgcf/wireproxy manager and a local SOCKS5 port; the system routing table is not changed. When outside services are needed, Automatic prefers WARP to MTProxy.

Your own proxy accepts `tg://proxy`, `socks5://`, `http://` and `https://`. An HTTPS proxy's certificate is checked before credentials are sent to it.

A connection check is valid for five minutes and is bound to the route, the policy and the wizard answers; changing any of them needs a new check. **Continue without checking** is available and does not replace the Telegram sign-in. The chosen route is rechecked in the background, and Automatic runs its chain again after a lost connection. When no public proxy answers, the count turns red with WARP and recheck actions.

## Account groups

Accounts in a group share their settings. Open **Accounts → Groups and shared settings → Shared settings**, or **Group settings** on an account's Settings page.

The group shares the goal, saved files, timestamps, drand, problem notifications, off-site copy, requests outside Telegram, IP mode, what to record, the recheck schedule, notification rules, report settings, parameters and the connection route. Notification destinations, proxy credentials and sign-in stay per account, as do starting and pausing collection.

- Every member follows the group. Settings marks a value 🔗 **From the group** or ✏️ **Own value**; **Return to the group value** puts it back.
- A change lists the accounts it reaches (**Applies to 2 of 3 accounts**) and asks per account before replacing an own value. Unticked accounts keep theirs.
- A parameter the group does not share stays **Not shared: each account keeps its own value** until you press **Share this value**.
- **Copy settings from one account** takes the chosen account's values as the group's.
- An account moved into a group is asked **Take the group's values?** Otherwise it keeps its own values, marked ✏️. Accounts added later start with the group's values.
- An observing account keeps its IP mode until it is paused.

Each change is recorded in the signed journal of the main workspace and of every member it reaches. Deleting a group keeps its accounts and their current values.

The group page `/groups/<id>` shows the members, what needs attention and the chats several accounts see. See [account groups](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#bulk-import-and-account-groups).

## Existing workspaces

A workspace with a session or an earlier completed setup does not get the wizard. Its values are not replaced by a goal when the page loads. Hiding a field does not turn the feature off or delete its value.

The size and time estimate reads up to three selected chats and up to 20 messages from each. It is an estimate: it does not predict Telegram limits, the speed of a given server or the files in every chat.

```
python tools/test_settings_hub.py
python tools/test_group_settings.py
python tools/check_group_settings_browser.py
python tools/check_first_run.py
```


---

# Accounts and session formats

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/accounts/

Sign in by phone, QR code or auth key, import Telethon, Pyrogram or Telegram Desktop sessions, and run several accounts.

TgWitness signs in as a **Telegram user account** (not a bot) over MTProto, using Telethon. Each account lives in its own **workspace** (called a *workspace* in the API and command-line tools) with its own session, sources, journal and signing key.

Session files, session strings and Auth Keys are **account authorizations**: whoever holds one can act as that account. They do not contain message history.

> [!WARNING] **Do not use anything you cannot afford to lose.** We strongly advise against connecting personal or otherwise valuable accounts, and against creating an API ID / API hash on an account you value. This is not about TgWitness being untested: Telegram restricts and permanently bans accounts unpredictably — for request volumes it happens to consider excessive, regardless of the client or purpose, with no adequate documentation. Many bans are irreversible. Use dedicated accounts. Smooth test runs depend on Telegram, not on the software, and guarantee nothing for later.

- [At a glance](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#at-a-glance)
- [Before you start: API ID and API hash](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Phone number](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#phone-number) · [QR code](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#qr-code) · [Auth Key + DC ID](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#auth-key--dc-id)
- [Account files](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#pyrogram-session) · [Session + JSON pair](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#telethon-stringsession) · [Account JSON](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#account-json)
- [Identify what you have](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#identify-what-you-have) · [Unsupported formats](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#unsupported-formats)
- [Multiple accounts](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#multiple-accounts) · [Keeping account files safe](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#keeping-account-files-safe) · [Troubleshooting](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#troubleshooting)

## At a glance

| What you have | Tab in **Add account** | You will also need |
| --- | --- | --- |
| The phone number and access to its login codes | **Phone** | 2FA password if enabled |
| Telegram open on another device | **QR code** | 2FA password if enabled |
| A `.session` file (Telethon or Pyrogram) | **Files** | Optional companion JSON for app settings |
| `.session` + `.json` with the same name | **Files** (select both) | Usually nothing else |
| A Telegram Desktop `tdata` folder | **Files** (as a ZIP) | The Desktop local passcode if one is set |
| A Telethon StringSession (text, `.txt`, `.tgwitness-session`) | **Files** | No separate API pair required |
| A `.json` with a session or Auth Key | **Files** | No separate API pair required |
| An Auth Key (512 hex characters) and its DC number | **Auth key** | Optional User ID |

TgWitness recognises files by their **contents**, not their names. Renaming a file never converts it.

## Before you start: API ID and API hash

You can sign in without creating a Telegram API application. When no pair is entered, imported or already saved in the workspace, TgWitness picks a pair from its built-in pool of 50 public API pairs (`tgwitness/api_pool.py`) in random order. If Telegram refuses a pair (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), the next one is tried, up to eight per sign-in; refused pairs are skipped until restart. The pair that signed in is saved with the account and reused for it. An **API ID** and **API hash** identify the application to Telegram; they do not authorize an account by themselves.

To use your own application instead (the account that registers it is the one at risk; see [Why a built-in API pool?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)):

1. Open [my.telegram.org](https://my.telegram.org) and sign in with any phone number you own. The code arrives in the Telegram app, not by SMS.
2. Choose **API development tools**.
3. Create an application: any title and short name (5–32 letters), platform **Desktop**. URL and description can stay empty.
4. Copy **App api_id** (a number) and **App api_hash** (32 hexadecimal characters).

In the panel, open **API ID + Hash** under the sign-in form. You can paste a single `api_id:api_hash` pair into **API ID** and both fields are filled. One pair can be used for all of your accounts. After a successful login it is saved, encrypted, in that workspace only and is never sent back to the browser.

Three different credentials are involved:

| Secret | Opens | Where it lives |
| --- | --- | --- |
| Panel token | The TgWitness web panel | `panel-token.txt` in the data directory, or `TGWITNESS_TOKEN` |
| API ID + hash | Nothing by itself; identifies the app | Built-in pair, imported settings, or your own app at my.telegram.org |
| Account authorization | The Telegram account | Created by phone/QR login or brought in as a session |

If Telegram must be reached through a proxy, set it first under **Account → Settings → Connection settings → Change connection route**.

## Phone number

1. Open **Account**, tab **Phone**, and enter the number in international format, for example `+44 7700 900123`. Spaces and dashes are removed automatically.
2. Press **Continue**. API ID + Hash can stay empty.
3. Enter the code Telegram sends (usually to the Telegram app; SMS is not guaranteed).
4. If the account has two-step verification, enter that password. It is not the panel token and not a device passcode.
5. Check the account ID shown after login, then choose sources.

Login codes and the 2FA password are never written to disk.

## QR code

Use this when the account is already signed in on a phone or another computer.

1. Tab **QR code** → **Show QR code**. API ID + Hash can stay empty.
2. On the signed-in device: **Settings → Devices → Link Desktop Device**, scan the code and confirm.
3. Enter the 2FA password in TgWitness if Telegram requests it.

The QR image is generated locally. Codes expire; press **Generate another QR code** to retry. Locking the panel, switching workspace or starting another login cancels a pending code.

## Auth Key + DC ID

An Auth Key is the raw 256-byte authorization behind every Telegram session, written as **512 hexadecimal characters**, together with the data-centre number **DC 1–5**.

1. Tab **Auth key**. Paste the complete key; a shortened key containing `…` cannot work.
2. Select the DC ID supplied with the key.
3. Optionally enter the **User ID**. TgWitness then refuses to connect if Telegram reports a different account.
4. Press **Connect account**.

An Auth Key (512 characters) is not an API hash (32 characters). The same key can also be imported as JSON, see [Account JSON](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#account-json).

## Account files

Open **Add account → Files** and select up to **four files belonging to one account**, **8 MiB** in total, then press **Connect account**.

- Files are converted **in memory** on your TgWitness server. Uploads are not stored, ZIPs are not extracted to disk and no external service is contacted.
- The resulting session is then checked with Telegram. If a file states a user ID, it must match the account Telegram reports.
- Files that describe different accounts or different API credentials are rejected instead of picking one.
- **Passcode or session text** holds the TData local passcode field, a box for pasting a StringSession and **Read files without signing in** (fills the form without contacting Telegram).

### Telethon `.session`

|  |  |
| --- | --- |
| What it is | The SQLite database Telethon-based tools create, for example `my_account.session` |
| Recognised by | Tables `sessions` (with `dc_id`, `server_address`, `port`, `auth_key`) and `version` = 7 or 8 |
| Requirements | Exactly one authorized session row; a closed, complete database |

Close the program that created the file first. If `my_account.session-journal` or `my_account.session-wal` exists next to it, the database is not finalised: open and close the original client cleanly. Deleting those sidecar files can leave a broken copy.

### Pyrogram `.session`

|  |  |
| --- | --- |
| What it is | The SQLite database Pyrogram-based tools create |
| Recognised by | Table `sessions` with `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 or 3 |
| Requirements | One authorized **user** session on the production network. Bot and test-DC sessions are rejected |

The stored user ID is checked against Telegram during login.

### Session + JSON pair

Accounts are often distributed as two files with the same name, for example `447700900123.session` and `447700900123.json`. Select **both** at once.

- From the JSON, TgWitness uses `app_id`/`api_id` and `app_hash`/`api_hash`, so you usually do not have to type API credentials.
- Other fields such as `phone`, `device`, `sdk`, `app_version`, `lang_pack` or a stored `twoFA` password are **ignored**. If the account has 2FA, TgWitness asks for it.
- A JSON on its own is only metadata. Without the session file, continue with phone or QR login.

### Telegram Desktop (TData)

TData is the `tdata` folder of the Telegram Desktop application (the cross-platform app from desktop.telegram.org).

| System | Default `tdata` location |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (portable Telegram: next to `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

To import it:

> **Parallel session warning.** Importing TData reuses Telegram Desktop's authorization key; it does not create an independent login. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, sign in to TgWitness by phone or QR to create its own authorization. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> This also applies to imported `.session` files, StringSession text and Auth Key HEX. Other clients with their own independently created authorizations can remain signed in. See [Telegram's AUTH_KEY_DUPLICATED documentation](https://core.telegram.org/api/errors#406-not-acceptable).

1. Fully quit Telegram Desktop.
2. Create a ZIP containing **only** these two items from `tdata`:

   - `key_datas`
   - the 16-character file ending in `s` next to it, usually `D877F783D5D3EF8Cs`

   Zipping the whole folder with its media cache usually exceeds the limits (512 entries, 32 MiB unpacked). 3. Select the ZIP in **Files**. If Telegram Desktop has a **local passcode**, enter it under **Passcode or session text** first. This is not the 2FA password.

Supported: one account per archive, modern `key_datas`/`key_data0`/`key_data1` storage, local passcode. Not supported: folders with several logged-in accounts, older Desktop layouts, password-protected ZIPs, and the separate native macOS app "Telegram for macOS".

### Telethon StringSession

A single line of text, usually starting with `1` and about 350 characters long. Load it as a `.txt` or `.tgwitness-session` file (at most 4 KiB), or paste it under **Passcode or session text**. Only Telethon strings are accepted; Pyrogram and TDLib strings use different formats.

### Account JSON

One JSON object, at most **64 KiB**, in a file ending in **`.json`**.

| Field (aliases) | Meaning |
| --- | --- |
| `api_id` (`app_id`) | Application ID, a positive number |
| `api_hash` (`app_hash`) | Application hash, 32 hexadecimal characters |
| `string_session` (`session_string`, `session`) | Telethon StringSession text, not a file name |
| `auth_key` (`auth_key_hex`) + `dc_id` | Complete 512-character Auth Key and DC 1–5 |
| `user_id` (`id`) | Optional; checked against Telegram before the authorization is saved |

If both an alias and the main name are present, they must agree. Examples:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

The first example only fills API credentials; sign in by phone or QR, or add a session file. Bulk lists (a JSON array of accounts) are not accepted.

## Identify what you have

| You see | It is | Use |
| --- | --- | --- |
| `*.session`; opening it in a text editor shows `SQLite format 3` at the top | Telethon or Pyrogram SQLite | **Files** (detected automatically) |
| A `tdata` folder containing `key_datas` | Telegram Desktop TData | ZIP two files, then **Files** |
| One text line starting with `1`, ~350 characters | Telethon StringSession | **Files** |
| `*.json` with `app_id`/`app_hash` | Companion metadata | **Files**, together with its session |
| `*.json` with `auth_key` or `string_session` | Account JSON | **Files** |
| 512 characters `0-9a-f` | Auth Key | **Auth key** |
| 32 characters `0-9a-f` | API hash | **API ID + Hash** |
| `td.binlog` or a `db.sqlite` from a TDLib app | TDLib storage | Not supported |
| `123456789:AA…` | Bot token | Not supported |

## Unsupported formats

| Format | Alternative |
| --- | --- |
| TDLib storage (`td.binlog`) and TDLib exports | Sign in by phone or QR |
| Pyrogram session **strings** | Use the Pyrogram `.session` file, or phone/QR |
| TData with several logged-in accounts | Log out the other accounts in Telegram Desktop, or use each account's own session file |
| Bot tokens | Not supported: TgWitness observes as a user account |
| CSV/JSON lists of many accounts | Import supported session files through **Accounts → Import accounts**, or sign in by phone/QR in separate workspaces |
| Test-DC or bot sessions | Use a production user account |

## Multiple accounts

Press **+** beside the account selector, or open **Account → Settings → Connection settings → Workspaces**, enter a label and sign in.

- Any number of workspaces, including the main one. Each has its own session, proxy route, sources, capture policy, journal, signing key, checkpoints and exports.
- Switching the displayed workspace does not pause the others.
- A journal stays bound to the account that created it. Signing in as a different account requires another workspace, and one account cannot be assigned to two workspaces.
- The main panel token controls all workspaces. [Issued access](https://phishdestroy.github.io/TgWitness/docs/reference/access/) can restrict other people to selected accounts and chats, with separate permissions and session limits.
- **Accounts** renames a workspace and deletes an added one, with its session, journal, sources and signing key. The main workspace cannot be deleted from the panel.

### Bulk import and account groups

Use **Accounts → Import accounts** to add several accounts, pair files by basename and see each login result. Each account gets its own workspace.

A group keeps related accounts together without merging their sessions, keys or evidence. **Open group** on **Accounts** leads to its page at `/groups/<id>`:

- **Accounts:** each member's connection route, observation and last message, with **Start all** and **Pause all**.
- **Needs attention:** accounts that were signed out, are unavailable or have a connection, intake, source or media problem; each name leads to its card.
- **Chats several accounts see:** shared sources, the accounts observing them and interruptions in the available workspace-observation period (up to seven days). **Export with N accounts** splits a channel or supergroup export between them and signs one archive.
- **Export group:** one ZIP with each account's signed export under `accounts/` and `manifest.json` listing their SHA-256 and key fingerprints, signed by the main workspace in `manifest.signature.json`. Verify each account archive on its own with `python -m tgwitness.verify` and that account's trusted fingerprint.

Members share the group's settings; an account can keep its own values. See [shared settings](https://phishdestroy.github.io/TgWitness/docs/reference/settings/#account-groups), [the import and groups guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) and [the MTProxy pool dashboard](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Sign out

**Account → Sign out of Telegram** (with observation paused) asks Telegram to end the session, so it also disappears from the account's **Settings → Devices**, and removes the session from the workspace vault. The journal, sources, settings and signing key stay, and the journal records the sign-out. The workspace still belongs to its account: only that account can connect to it again. If Telegram does not answer, the session is still removed here and the panel says so; end it in Telegram under **Settings → Devices**.

## Convert a Telethon session offline

The panel imports `.session` files directly. For an offline conversion to a StringSession file, run from the project folder:

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

The converter reads Telethon SQLite only (up to 64 MiB), never modifies the input, makes no network request and refuses to overwrite an existing output file.

## Keeping account files safe

- Treat every `.session`, TData ZIP, StringSession, Auth Key and account JSON like a password. TgWitness keeps the imported authorization in its encrypted vault; you can remove the original files afterwards.
- Do not run the same authorization in two programs at once. Telegram may revoke it (`AUTH_KEY_DUPLICATED`), and both copies stop working.
- An expired or revoked session cannot be revived by conversion. Sign in again.

## Troubleshooting

| Message or symptom | What to do |
| --- | --- |
| *Cannot read this session. Close its original client…* | The SQLite file is open or unfinished (`-journal`/`-wal` sidecar). Close the original program cleanly and copy the file again. |
| *Supported Telethon SQLite schemas: 7 and 8* / *Pyrogram … 2 and 3* | A very old or unknown library version created the file. Sign in by phone/QR instead. |
| *Only authorized production user sessions are supported* | The Pyrogram file belongs to a bot or the test network. |
| *TData archive exceeds 512 entries or 32 MiB* | ZIP only `key_datas` and `D877F783D5D3EF8Cs`, not the whole folder. |
| *Cannot decrypt TData. Check the Desktop local passcode* | Enter the Telegram Desktop local passcode under **Passcode or session text**. |
| *Import one TData account at a time* | Telegram Desktop had several accounts; see [Unsupported formats](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#unsupported-formats). |
| *Selected files describe different accounts or API credentials* | Select files of one account only. |
| *JSON contains no supported API credentials or authorization* | Check the field names in [Account JSON](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#account-json). |
| *API metadata only* | The JSON has no session. Add the `.session` file or use phone/QR. |
| *Auth Key HEX must contain all 512 hexadecimal characters* | The key is truncated or contains `…`. |
| Account ID does not match the imported account | The file's user ID differs from what Telegram reports; the file is for another account. |
| Account already belongs to another workspace | Open that workspace instead of adding the account twice. |
| Connected, but a private group is missing from the chat list in **Sources** | Check membership. The picker inspects the first 1,000 dialogs; raise the limit under **Parameters**. |
| Proxy connection fails | Check the route and IP mode. Automatic MTProxy tries another working entry. Hide the address waits; Direct as a last resort can connect directly after its configured delay. See [routing modes](https://phishdestroy.github.io/TgWitness/docs/reference/connection/#ip-modes). |

See also: [connection and security](https://phishdestroy.github.io/TgWitness/docs/reference/connection/) for proxies and encryption, and [how collection works](https://phishdestroy.github.io/TgWitness/docs/reference/collection/) for what is captured after sign-in.


---

# Access and permissions

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/access/

Issue scoped access to accounts and chats, choose permissions, limit sessions and IP addresses, and withdraw access.

Give a reviewer access to one chat, an analyst permission to export a case, or an operator control of selected accounts. Each person gets their own token. The main panel token stays with the administrator.

[Account setup](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/) · [Connection routes](https://phishdestroy.github.io/TgWitness/docs/reference/connection/) · [Security model](https://phishdestroy.github.io/TgWitness/docs/reference/security/)

## Two scopes, two different jobs

**Collection scope** decides what an account records: selected chats, a Telegram folder or the whole account. **Access scope** decides which of those recorded accounts and chats another person can see and use. Giving access does not join a Telegram chat, start collection or grant Telegram account permissions.

An access can open selected workspaces, selected chats within them, all workspaces, or every account of an [account group](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#bulk-import-and-account-groups). **All workspaces, including ones added later** also covers future accounts. A group access also covers accounts added to that group later. Select workspaces explicitly when a case should stay limited to them.

## Give someone access

1. Sign in as the main administrator and open **Access**.
2. Under **Give someone access**, enter a name you will recognize in the log.
3. Choose the workspaces and, where needed, the individual chats.
4. Select what this person may do. **View** is always included.
5. Set the expiry, sign-in/session limits and allowed addresses as needed.
6. Press **Create access**. Copy the token now: it is shown only once.
7. Send the panel address and token privately. The recipient enters that token on the normal sign-in page; they do not need your main panel token or a Telegram session.

Open the panel with the issued token in a separate browser session and check the visible chats and permitted actions before handing it over.

## Choose the permissions

For a text-only public demonstration, use **Public showcase** instead of ordinary reviewer access. It shows explicitly selected public channels, retained edits and deletions, and signed statistics, with author fields redacted and files closed at the API boundary. [Create and verify a showcase](https://phishdestroy.github.io/TgWitness/docs/reference/showcase/).

| Permission | What it allows |
| --- | --- |
| `view` | Read permitted chats, captured messages, profiles, files and filtered journal records. Always included. |
| `export` | Export permitted chat history and dossiers. Whole-workspace evidence exports require access to the whole workspace. |
| `sources` | Manage sources, snapshots and profile capture. Chat-limited access can act only on allowed chats; account-wide source discovery and scope settings stay closed. |
| `collect` | Start or stop a collector. Requires whole-workspace access because collection affects the account. |
| `interact` | Perform supported Telegram interactions within the access scope. Chat-limited access cannot use account-wide link previews. |
| `settings` | Change collection settings, timestamps, notifications, off-site copies and parameters. Requires whole-workspace access. |
| `account` | Sign in or out of Telegram and manage connection routes. Requires whole-workspace access. |
| `board.read` | Read Case Board notes only within the permitted workspace and chats. |
| `board.write` | Add bookmarks, highlights, slices, comments and open/review statuses. Also needs `board.read`. |
| `board.manage` | Manage collections, final team statuses and other participants' cards. Also needs board read/write. |

Permissions and scope are checked together. Ticking a permission does not open other chats or unlock a workspace-wide operation for a chat-limited access. For a parallel export, the access must cover the exported chat in every selected account. An issued access cannot create new accesses, manage other people's sessions or open the administrator console.

### Three useful setups

| Person | Scope | Permissions |
| --- | --- | --- |
| Reviewer | One case's recorded chats | `view` |
| Analyst preparing a handover | The chats to investigate and export | `view`, `export`; add `interact` only if they should act through Telegram |
| Collection operator | Selected whole workspaces | `view`, `sources`, `collect`; add `settings` or `account` only when needed |

The Access form's starting presets also include Case Board: Reviewer can read, Analyst can read and write, and Operator can manage it. Presets remain editable, and existing grants are not automatically expanded. See [Case Board](https://phishdestroy.github.io/TgWitness/docs/reference/case-board/) for inherited chat scopes and export privacy.

## Limits and sessions

| Setting | How it works |
| --- | --- |
| Parallel sessions | Limit simultaneous sessions to 1–100. At the limit, refuse the next sign-in or end the oldest session. |
| Sign-ins allowed | Limit successful uses of the token to start sessions. Existing sessions are not ended just because the last allowed sign-in was used. |
| Valid until | An absolute expiry for the access. Expired access cannot sign in or keep making requests. |
| Minutes without activity | Session inactivity timeout, from 5 minutes to 30 days. Successful requests extend it; an open panel may keep itself active by polling. |
| Allowed addresses | Accept specific IP addresses or CIDR subnets. Leave empty to allow any address unless first-sign-in binding is enabled. |
| Bind to the first sign-in | The first successful sign-in fixes the permitted address for that access. |

The IP is the client address seen by the application. Behind a reverse proxy or tunnel, check the address shown in **Open sessions** before relying on IP rules: several users may otherwise appear to share the proxy's address.

## Change or withdraw access

Edit an entry under **Granted access** to change its scope, permissions or limits. Scope and permission changes are checked on subsequent requests, including requests from sessions that are already open. Revoking an access ends its sessions and makes the issued token unusable. **Open sessions** also lets the administrator end an individual session without revoking the whole access.

Saved export copies retain their creator, workspace, chat scope and required permissions. An issued access can list or download its own copies only while those permissions still apply; copies containing Case Board also require `board.read`. The administrator can retrieve all copies. Older copies without this metadata and group bundles are administrator-only. Download tickets and prepared file responses recheck access after preparing the file, before sending its bytes.

Revocation cannot recall files that someone already downloaded. Signing out, locking the panel or ending a session does not stop a running collector.

## What the administrator can see

Reviewers and analysts receive collection progress without proxy endpoints, pool diagnostics, server paths or raw connection errors. Connection diagnostics require `account` permission over the whole workspace. Reading notification, off-site-copy and parameter settings requires `settings` permission.

Full browser User-Agent strings are not retained in access sessions. An upgrade also removes them from the mutable session cache. The panel process log masks IP literals, URL credentials and labelled secrets. Local service logs and previously signed journal records are not rewritten. Access rules and signed sign-in records still use the client address.

### Replace the main key

Use **Access → My limits → Reissue administrator key**, or run `tgwitness token rotate` from a managed installation while the panel is running. All existing browser sessions end, including sessions opened with colleague tokens. The requesting browser receives a new session; save the new administrator key before hiding it. Issued colleague tokens remain valid until separately revoked. An installation using `TGWITNESS_TOKEN` must change that environment setting and restart.

### Request and proxy boundaries

The API admits up to 600 requests per minute per client IP. Ten rejected authentications within a minute start an exponential cooldown, from one second up to five minutes. A failed attempt after the cooldown increases it; ten minutes without a failed attempt resets escalation. Rejections return HTTP 429 and `Retry-After`. Limits are in memory, shared across workspaces in one panel process; restart clears them. Live streams are limited to four per bearer token and 32 for the panel process. Opening a stream also consumes the API request budget.

Request bodies have a 60-second receive deadline (8 seconds for MCP). Each application bounds unfinished bodies to 32 requests and 64 MiB of reserved route allowances. Oversized bodies return 413, timed-out bodies return 408, and exhausted body capacity returns 503 with `Retry-After`.

Forwarded IP headers are ignored unless the actual TCP peer belongs to `TGWITNESS_TRUSTED_PROXIES` (comma-separated IPs or CIDRs). Set `TGWITNESS_PROXY_HEADER` to `x-forwarded-for` or `cf-connecting-ip`. XFF is walked from the nearest proxy toward the first untrusted peer. Malformed or duplicate trusted address metadata is rejected, so it cannot inherit an allowlisted proxy address. The managed quick tunnel trusts the local cloudflared connector; the own-domain setup trusts local Caddy. Direct deployments trust no proxy by default. If launching Uvicorn yourself, disable its proxy-header processing so this boundary receives the actual peer.

`TGWITNESS_PANEL_ALLOWED_IPS` restricts all panel access, including the administrator, to listed IPs or CIDRs. The installer routing-identity probe stays public and returns no account data. Include the required local administrative route before enabling the allowlist. A managed installation's **START-HERE** guide includes the service configuration and recovery instructions.

An API `ws` query selector must identify the workspace in the request path; unknown, mismatching and duplicate selectors are rejected with 404.

Panel scripts and styles carry SHA-384 integrity metadata. An import map also covers locally imported JS modules in browsers that support import-map integrity. The dynamically generated language response is separate. These checks detect asset substitution relative to the delivered page; they do not establish trust in a compromised server that can replace both the page and its hashes.

**Log since this start** combines process logs with journal activity from every workspace: sign-ins, refusals, route changes and operator actions. It is an in-memory console for the current process, not a permanent copy of every message. Frequent message events stay in the journal rather than filling the console.

Issuing, changing and revoking access, and starting or ending sessions, also create signed `access.*` journal records. Tokens are not included in those records. Issued tokens and session credentials are retained as hashes in the encrypted vault.

****Main administrator and trust boundary**** The main panel token remains unrestricted. Browser sign-ins with it create sessions subject to the administrator's configured session limits. Scripts sending the main token directly retain full access and are not counted as browser sessions. This is application-level access control in one installation. All workspaces share the server process; this is not isolation from the host administrator. Keep the main token, Telegram sessions, signing keys and data directory private. A witness token is a separate checkpoint/health credential, not a panel access token.


---

# Connection, proxies and data protection

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/connection/

Authentication, automatic proxy pools, IP modes, fallback policy, external requests and secret storage.

This document describes TgWitness 0.8.0 behavior and its limits. Authentication, source access, network connectivity and capture completeness are separate states. For sign-in steps, file formats, and multiple accounts, start with [accounts and session formats](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/). For event policies and restart behavior, see [how collection works](https://phishdestroy.github.io/TgWitness/docs/reference/collection/).

## Guided connection setup

In **Connection**, the administrator can choose **This account**, **An account group** or **All accounts**, then select a route. **Review selection** lists the affected accounts. **Prepare and check** tests the proposed route without changing the saved one. **Apply checked connection** checks again, pauses observation if necessary, saves the route and resumes observation that was already running. It never starts collection in a previously idle account. History downloads remain paused and can be resumed separately. Pause active exports before switching.

Group changes keep accounts with their own route by default. Clear that option only when the preview lists the changes you intend. Application reports each account's result; it is not an all-or-nothing transaction across databases. A failed switch restores that account's previous settings. A failure to resume is shown explicitly. Previews expire after ten minutes and changes to connection settings or group membership require a new check.

| Route | What TgWitness manages |
| --- | --- |
| Direct | Connections from the host; an external host VPN is not detected or enforced. |
| VPN | One full-tunnel WireGuard profile per account, carried by a local userspace SOCKS5 process. No host interface or driver is installed. |
| My proxy | SOCKS5, HTTP CONNECT or MTProxy credentials. A URL can fill the SOCKS5/HTTP fields. Selecting several accounts shares this entered proxy. |
| Public MTProto | The existing pool assigns Telegram routes. External requests are disabled until a separate suitable proxy is configured in the advanced settings. |
| WARP | A separate local tunnel for each selected account, with WARP registration and a WireGuard profile kept in that account's vault. |

The current-route check uses a fresh unauthenticated Telegram transport, not the account's session. For HTTP-capable routes it also requests Cloudflare's HTTPS trace through that route and displays its reported exit IP, country, WARP state and check time. The measured latency is the Telegram connection setup time, not an ICMP ping. WARP preparation fails unless the trace reports WARP active. These checks establish connectivity, not the authenticity or completeness of captured messages. A running local process alone is not a successful exit check.

### Portable WARP and WireGuard

This is an **unofficial WARP integration** using [wgcf 2.3.1](https://github.com/ViRb3/wgcf/releases/tag/v2.3.1) and [wireproxy 1.1.3](https://github.com/windtf/wireproxy/releases/tag/v1.1.3). The administrator explicitly accepts setup before the first download or WARP registration. Those setup connections go directly to GitHub and Cloudflare and reveal the machine's IP. Ordinary account traffic keeps its existing route until application. Cloudflare chooses the exit address and country; separate tunnels can share an exit address. Country selection, periodic IP rotation and a host-wide VPN kill switch are not provided by this feature.

Supported helper downloads: Linux and macOS x86-64/ARM64, and Windows x86-64. Artifacts are checked against SHA-256 hashes bundled in the reviewed source, and cached executables are checked again before launch. No helper is added to PATH, installed as a system service, or given a public listener. All files live under the workspace's `portable-routes/` directory and encrypted vault entries. The loopback SOCKS5 listener requires independently generated credentials.

Private profiles and WARP account credentials are encrypted with the existing workspace vault. While running, the helper needs an owner-only plaintext config; it is removed on a normal stop. A host crash can leave this file behind in the owner-only data folder. This does not encrypt the disk or protect against its administrator. The supervisor closes the tunnel if the panel's parent pipe disappears. A failed tunnel never enables a direct fallback. Panel restart restores a selected tunnel; failed starts retry with a bounded delay. **Stop tunnel** also pauses observation and persists the stopped state. **Start tunnel** starts the tunnel; resume observation separately when ready.

Uploaded WireGuard profiles must contain one Interface and one Peer, full IPv4 and IPv6 routes, and no hooks, includes, environment substitutions or extra listeners. Public endpoint addresses are resolved and pinned before startup. Use an external VPN or SOCKS5 gateway for OpenVPN/IPsec and private endpoints.

The synthetic checks are `python tools/check_guided_connection.py` and `python tools/check_guided_connection_browser.py`. The optional `python tools/check_portable_routes_runtime.py` downloads verified helpers and tests their actual local process lifecycle against loopback fixtures. It does not register a Cloudflare device or use a Telegram account.

## Authentication methods

**API ID and API hash identify an application; they do not replace account login.** They are optional in TgWitness. Precedence: a pair entered in the form, then one from an imported account JSON, then the pair saved in the workspace, then the built-in pool of 50 public pairs, tried in random order with automatic rotation when Telegram refuses one. Only the Telegram Desktop pair (2040) is sent with a matching Telegram Desktop client description. Your own pair from API Development Tools at [my.telegram.org](https://my.telegram.org) can be used with all of your accounts; each account still has its own authorization.

| Method | Requirements | TgWitness support |
| --- | --- | --- |
| Phone, code, optional 2FA | Account access; API pair optional | Panel login |
| Auth Key HEX + DC ID | Full 512-character key and DC 1–5 | Direct **Auth key** tab; optional User ID checked before authorization is saved |
| Telethon StringSession | A valid session string | Panel login |
| Telethon SQLite `.session` | Closed, consistent copy | Direct panel import of schemas 7/8; optional offline CLI |
| Pyrogram SQLite `.session` | Closed production user session | Direct panel import of schemas 2/3 |
| Telegram Desktop TData ZIP | One modern account; local passcode if protected | In-memory conversion with checksum/decryption checks |
| Account JSON | Supported API/session/key fields | Metadata alone fills API credentials; a session/key or phone/QR login is still needed |
| QR login | Confirmation from an authorized Telegram app | Local QR generation, expiry/retry, optional 2FA |
| TDLib / Pyrogram StringSession | Other library-specific formats | Unsupported |
| Bot token | A bot with its own access/update model | Not used by this collector |

Telegram chooses code delivery; SMS is not guaranteed. An API hash cannot repair a revoked session or replace a forgotten 2FA password. TgWitness does not persist login codes or the Telegram 2FA password to disk.

For a private source, the account must already have access. A group username is unnecessary. A proxy or session import grants neither membership nor administrator rights. Current membership does not guarantee access to pre-join history.

## Import a Telethon session file

Telethon SQLite, Pyrogram SQLite, and Telegram Desktop TData use different formats. The panel detects and converts the supported structures; renaming a file is not conversion. Select one session and its companion JSON under **Files**, then press **Connect account**. Up to four matching files and 8 MiB total are accepted. See [format limits](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/) for TData/JSON details. There is no passcode recovery. Phone/2FA or QR login creates a separate authorization.

The optional Telethon-only command-line path remains available:

1. Stop the client using the original session and make a consistent copy. The converter rejects files with an unfinished WAL/journal. Close the original client properly instead of deleting those files to bypass the check.
2. From the TgWitness environment, run:

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. Under **Add account → Files**, load the result or paste its string, and continue.
2. Check the displayed numeric account ID, select sources and start observation.

The converter opens SQLite read-only, performs no schema upgrade or network request, and does not print the session. It checks schema version, table types, a single session row, IP/port/DC and key length. CLI input is limited to 64 MiB; StringSession text is limited to 4 KiB. Panel conversion uploads files to the authenticated TgWitness server, processes them in memory, and returns the normalized credentials to that browser without saving the uploaded originals. Use HTTPS for a remote server.

**The converted file is an unencrypted account-access secret.** Keep it in protected storage and never commit it or send it to a third-party conversion service. TgWitness saves the authorized session in its encrypted vault. Copying a session does not create a separate authorization: do not run concurrent clients with cloned auth keys and assume independent update delivery.

Conversion transfers authorization, not original messages, the entity cache or a durable update cursor. It does not fix update recovery across process restarts.

## MTProto, Telethon and proxies

MTProto is Telegram's protocol. Telethon is the Python client library TgWitness uses. MTProxy is a Telegram transport proxy; SOCKS5 and HTTP CONNECT provide general tunnels. None replaces account authentication.

Save the route for each workspace in **Account → Settings → Connection settings → Change connection route** before signing in. New workspaces default to **Automatic MTProxy · public lists** with **Hide the address**. Existing workspaces that explicitly used Direct retain a mode permitting it.

## IP modes

The route chooses the connection. The IP mode, **IP protection** in the panel's Account section, determines when the server's address may be exposed. These controls do not install a VPN or route all machine traffic.

| Mode | Telegram | External requests |
| --- | --- | --- |
| Hide the address (`hide`) | Use a proxy; wait if none works. No direct fallback. | Require SOCKS5/HTTP; refuse requests without an applicable proxy. |
| Direct as a last resort (`fallback`) | Automatic MTProxy may use Direct after the configured delay, then return to a working proxy. | Prefer a configured external proxy or the account's SOCKS5/HTTP route; otherwise Direct is allowed. |
| Server behind a tunnel or VPN (`tunnel`) | Direct routes and immediate automatic-pool fallback are permitted. | Direct is permitted when no applicable proxy is configured. |

The tunnel or VPN mode assumes you manage that network separately. Without a working tunnel, destinations can see the server's own address. Select the mode according to your actual network, not the name of the option.

### Choose a route

| Route | Settings | Boundary |
| --- | --- | --- |
| Automatic MTProxy | Built-in lists or an operator catalog | Maintains a working Telegram route; direct fallback depends on the IP mode |
| Direct | Tunnel or VPN mode | Telethon uses the host's network route |
| SOCKS5 | Host, port, optional username/password | python-socks, remote destination DNS enabled |
| HTTP CONNECT | Host, port, optional username/password | Plain HTTP CONNECT; TLS to the proxy itself is not implemented |
| MTProxy | Host, port, secret | Experimental Telethon transport; 32 hex digits or `dd` + 32 hex digits |

Fake TLS `ee` secrets are rejected. Telethon 1.45's normalization can strip a prefix and domain, but that does not implement Fake TLS. Paste `tg://proxy?server=…&port=…&secret=…` or `https://t.me/proxy?server=…&port=…&secret=…` and choose **Fill fields from link**. This validates and fills the fields without connecting or saving; review and save the route separately. Manual fields remain available. See [Telegram proxy links](https://core.telegram.org/api/links#proxy-links).

### Public proxies supplied by your installation

The built-in list combines four sources: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) and [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). The bundled snapshot contains endpoint facts, source attribution and download dates. A provider's listing is not proof that the proxy works or delivers every Telegram update.

**Automatic MTProxy** checks Telegram transport connectivity, keeps a working proxy and switches to another when it fails. Workspaces prefer different proxies when enough working entries are available; a unique exit address is not guaranteed. Failed proxies rest before another attempt. If none works, the IP mode determines whether collection must wait or may use a direct connection. Changing proxies does not change the account or erase its journal. Route choices and changes are recorded in the signed journal.

While automatic routes are active, lists refresh hourly and transport checks run every ten minutes by default. These intervals are configurable. **Update public lists** requests a refresh; viewing the list alone does not change a saved manual route.

Each feed response is limited to 1 MiB with an eight-second request timeout and a 20-second overall download deadline; redirects are rejected. Up to 64 compatible entries per source are retained and deduplicated. The parser accepts supported hexadecimal and base64url secrets and the JSON feed. Fake TLS `ee`, invalid links, private/reserved IP literals and local hostnames are skipped. Hostnames are resolved and checked before use, and the chosen IP is pinned for that connection. Automatic reacquisition resolves a hostname again; reapply a manual entry to resolve it again.

Failed, empty or incompatible feed responses retain the previous source snapshot. Updates are atomic, serialized and limited to one attempt per minute per workspace. A successful transport probe establishes connectivity, not anonymity or capture completeness.

**Telegram traffic and HTTPS requests use different routes.** List downloads use a separate HTTPS connection and the supplied external-request route. `TGWITNESS_PROXY_FEED_PROXY` explicitly overrides that route with an HTTP/SOCKS5 proxy; both collector Compose variants forward it. The background pool follows the main workspace. No Telegram session, API credentials, panel token or bot token is sent to feed providers. Provider names, snapshot dates and the download route appear under **Where the list comes from**.

An MTProxy carries Telegram traffic only. Workspace HTTP operations such as timestamps, notifications, off-site copies and source checks use a separate SOCKS5/HTTP proxy when configured, then the account's SOCKS5/HTTP route. Without either, Hide the address refuses the request; the other modes permit Direct. External requests can be disabled. An explicitly configured feed-download proxy remains a separate operator override. The independent witness service keeps its own route.

Public-only external HTTP requests through SOCKS5 or HTTP proxies resolve the destination with Cloudflare DNS over HTTPS at `https://1.1.1.1/dns-query`, through that same proxy. Only the hostname and A/AAAA query types go to the resolver; service URLs, credentials and notification contents are not included. TLS verifies the resolver certificate for its IP address. Both address families are checked, and any private, loopback, link-local or reserved answer rejects the request. Connections use a checked numeric address while retaining the service's original HTTP Host and TLS certificate name. Notification HTTP forwarding and CONNECT requests use the same destination checks. DNS failure stops the request without local destination DNS or a direct fallback. Successful answers are cached in memory per proxy route for at most 30 seconds and no longer than their DNS TTL; the cache is limited to 128 entries. The proxy hostname itself may use local DNS. SOCKS and CONNECT failures can try another checked address before sending the service request body. Plain HTTP forwarding reports a failed request without automatically replaying its body through another address.

For operator-managed private services, the existing server environment setting `TGWITNESS_ALLOW_PRIVATE_DESTINATIONS=1` permits private destinations and keeps proxy-side hostname resolution. It cannot be enabled from the panel. Public-only mode rejects `.onion` destinations before querying the public resolver; Tor onion services require that explicit private-destination setting and a suitable proxy. This DNS behavior applies to external HTTP operations, not Telegram's transport. Cloudflare documents the [JSON DNS endpoint](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/).

****Automatic pool parameters**** Under **Parameters → Automatic MTProxy**, configure the failure threshold, cooldown, planned rotation, proxy sharing and permitted fallback delay. | Control | Default | | --- | --- | | Disconnects before replacement | 3 within 10 minutes | | Proxies tried per connection attempt | 3 | | First / maximum rest after failure | 10 minutes / 6 hours | | Planned rotation | Disabled; switch on failure | | Accounts per proxy | 0: prefer separate entries, share when needed. Set 1 to wait for an exclusive entry. | | Delay before permitted Direct fallback | 10 minutes; Hide the address still refuses Direct | | Feed refresh / transport checks | 60 / 10 minutes; main workspace values apply to the shared pool | Different proxies do not guarantee different exit addresses. These settings do not override Telegram limits or prove anonymity.

To replace the public list with your own operator catalog, configure the override below. It disables external subscriptions entirely, including when its `proxies` array is empty.

Copy [the empty catalog](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) to `proxy-config/proxies.json` and add your deployed public endpoints:

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

The example values must be replaced. Up to 32 distinct entries are accepted. The authenticated listing returns labels/hosts/ports without shared secrets; selecting one saves its credentials into the workspace vault. Availability remains untested until an explicit transport test. A malformed catalog leaves manual configuration available.

Native launch: set `TGWITNESS_PROXY_CATALOG` to the local JSON path. Docker:

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

The overlay mounts `proxy-config` read-only; files must be readable by container UID 10001. That directory is excluded from Git, Docker build context and source archives. This catalog configures the collecting accounts; [the witness bot](https://phishdestroy.github.io/TgWitness/docs/reference/witness/) uses its own HTTP/SOCKS5 route, not MTProxy.

Direct fallback is governed by the IP mode above. Pause observation before changing a route. Saving disconnects old clients and cancels unfinished login; a new client uses the saved route. The account's journal/session binding remains. Settings replace the previous route: re-enter proxy credentials when editing it.

Credentials are encrypted in `network.enc`. The API does not return the username, password or secret. Signed records contain the route type and whether credentials are present, excluding the endpoint and secrets. The operator can see the endpoint in the panel. Secret fields clear after saving, locking or switching workspaces.

**Test Telegram connection**, also available before login, opens and closes a temporary unauthorized Telegram connection through the route. It does not contact an IP-check website. Success establishes transport connectivity, not group access, complete delivery or anonymity.

The proxy applies to the Telegram client's connections, including Telegram DC media downloads. Browser, pip, SSH and manually invoked TSA tools have separate routes. The proxy hostname may be resolved locally. `rdns` affects destination hostnames; Telegram often supplies numeric DC IPs.

SOCKS5 and plain HTTP CONNECT do not themselves encrypt proxy credentials or the client-to-proxy tunnel. MTProto separately protects Telegram traffic. Use an appropriate secure channel to the proxy on an untrusted network. Private groups are cloud chats; MTProto does not turn them into end-to-end encrypted Secret Chats.

## Encryption and signatures

| Layer | Implemented | Operator responsibility |
| --- | --- | --- |
| Telegram traffic | Telethon MTProto | Platform trust, route and availability |
| Web panel | Bearer token, loopback default, request limits | HTTPS or SSH tunnel for remote access |
| Secrets | Fernet for API credentials, session, proxy credentials and signing private key | Protect the decryption key and running host |
| Vault key | Local key, or external master key for a new installation | Separate protected storage and key backup |
| Messages and attachments | Plaintext application storage | Encrypted disk/volume |
| ZIP/JSONL/CSV/HTML | Integrity checks, no content encryption | Protect exported copies and transfers |
| Provenance and time | Signed journal, process receipt, RFC 3161 tools | Trusted key, independent checkpoints/TSA and custody procedure |

**Storage protection** in Account shows these states. The panel token is an access secret, not an encryption password. It grants administrator access; [issued tokens](https://phishdestroy.github.io/TgWitness/docs/reference/access/) can be scoped to accounts and chats. Workspaces share the host process and are not isolated tenants.

An explicitly started, isolated synthetic demo can open automatically over a direct loopback connection. This uses a separate process-lifetime capability; it neither reveals the configured panel token nor grants access to real workspaces. Remote, proxied or cross-origin requests cannot obtain/use this automatic-entry capability. This convenience does not remove the authentication boundary for real account data.

BitLocker, LUKS, FileVault or a managed encrypted volume can protect storage under their respective threat models. An administrator of an unlocked running machine can still read data. Include SQLite WAL/SHM, media, temporary exports, swap, backups and browser downloads in storage planning. A Docker volume is not encrypted merely because it is a volume. TgWitness does not implement SQLCipher or object encryption.

## External master key

For a **new** installation, place the master key outside the data directory. This does not automatically migrate an existing local-key vault. Prepare a key directory accessible only to the service identity, then run:

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell, using the installed project environment:

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

In Docker, mount the file read-only outside `/data`, for example at `/run/secrets/tgwitness-master.key`, and set the environment variable to that path. The service UID must be able to read it. Pass the path, not the key bytes, through environment/configuration files.

Each workspace receives a random public salt and its own Fernet key derived through HKDF-SHA256. `vault.external.json` stores derivation metadata, not the master key. A missing/wrong key fails startup without silently replacing it. Retain both the salt metadata and master key for recovery.

All workspaces derive from the same master key; its compromise affects the entire installation. The running process can decrypt secrets. This is not an HSM or password KDF. Arbitrary human passwords are not accepted in place of a random key.

Keep the existing key for existing installations until a deliberate migration is implemented and verified. Deleting `vault.key` or replacing a master key can destroy access to sessions/signing keys. Keep encrypted backups and keys separately and test recovery in an isolated instance.

## Sources and verification scope

Reviewed on 26 October 2026:

- https://core.telegram.org/api/auth
- https://core.telegram.org/api/obtaining_api_id
- https://docs.telethon.dev/en/stable/basic/signing-in.html
- https://docs.telethon.dev/en/stable/concepts/sessions.html
- https://core.telegram.org/mtproto/mtproto-transports
- https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/SourceFiles/storage/storage_account.cpp
- Telethon 1.45.0: SQLiteSession, StringSession, `Connection._proxy_connect`, `TcpMTProxy.normalize_secret` and download methods.

Local tests cover loopback SOCKS5/HTTP CONNECT fixtures, synthetic SQLite sessions, route isolation, secret exclusion and missing-key refusal. They do not establish real Telegram/proxy interoperability or live MTProxy behavior. See [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/docs/reference/verification/) and [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).


---

# Deployment

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/deployment/

Run TgWitness as a service on Windows, Linux, macOS or Docker, behind HTTPS, with backups and updates.

**English** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [Українська](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [Português (Brasil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [اردو](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [हिन्दी](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [简体中文](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## Choose an installation

For the portable package, extract `TgWitness-<version>-windows-amd64-portable.zip` from GitHub Releases. For the other methods, download and extract the source ZIP or clone the repository, then run the following from the project directory:

| Installation | Start | Runs in the background? |
| --- | --- | --- |
| Windows portable package | `TgWitness.cmd` | No; keep the window open. |
| Native Windows | `Start.cmd` | No; use the optional logon task for background use. |
| Native Linux/macOS | `sh start.sh` | No; use systemd/launchd for background use. |
| Docker on any supported host | `docker compose up -d --build --wait` | Yes, while the Docker daemon runs. |
| Docker helper on Windows | `scripts\Docker.cmd` | Yes; the helper waits for web-server health. |
| Docker helper on Linux/macOS | `sh scripts/docker-start.sh` | Yes; the helper waits for web-server health. |

For a cloud server that a third party should be able to check — created through the provider's API, without SSH, reached only through a Cloudflare Tunnel — see [high-assurance deployment](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/).

Native startup creates a private `.venv` and installs the pinned dependencies. Docker builds them inside the image, without requiring host Python. First-time setup needs Internet access. When no Python 3.11+ is found, `Start.cmd` asks before installing Python 3.12 for the current Windows user (winget, otherwise the python.org installer after checking its Python Software Foundation signature); it never requests administrator privileges. Docker and OS services remain prerequisites.

Native and portable installations use `data/live` inside their folder. Docker uses the `tgwitness-data` named volume at `/data`. These are separate installations until you deliberately migrate the complete data directory. Do not expect a new Docker container to discover native accounts automatically.

## Installation requirements

Native installation needs Python 3.11 or later with `venv` and `ensurepip`, Internet access for the first dependency installation, and a writable project directory for `.venv`. The bundled panel needs no Node.js or frontend build. Run the launcher from your normal OS account; administrator/root privileges are not required by TgWitness.

- **Windows:** `Start.cmd` checks `py -3`, then `python`, then the default per-user and Program Files install folders, and requires version 3.11 or later. If none works, it offers the automatic per-user installation described above. `py -3 start.py` also works. The portable package needs no Python at all.
- **Linux:** `start.sh` tries `python3.13`, `python3.12`, `python3.11`, `python3` and `python`, and prints the install command for apt, dnf, pacman, zypper, apk or Homebrew when none qualifies. Debian/Ubuntu installations may require the `python3-venv` package matching the selected interpreter. A distribution's older default Python must be replaced or supplemented with Python 3.11+.
- **macOS:** install a current Python 3.11+ distribution; do not assume an OS-provided interpreter meets the requirement. Use `python3 start.py` from the project directory.
- **Docker:** use Docker Engine/Desktop with Compose v2.20 or newer. Docker Desktop must use Linux containers on Windows. The container installs its own Python dependencies; the host does not need a separate Python installation.

Use persistent local storage for the data directory. Plan capacity from messages, media, WAL growth, exports and backups; there is no evidence-based universal minimum disk/RAM specification for every workload. CPU architectures and Python versions without compatible dependency wheels may require additional build tools and their own qualification. "Portable" is not a claim of universal OS or hardware support.

Windows 11/Python 3.12 is locally verified. Linux/macOS/container definitions and CI are supplied but have not been executed on this development host. See [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/docs/reference/verification/) for the exact scope.

## Local computer

Use `Start.cmd` on Windows or `sh start.sh` on Linux/macOS. `scripts\Setup.cmd` or `sh start.sh --setup-only` prepares the environment. The launcher installs dependencies on first use; later launches reuse the environment. Internet access is needed for setup and Telegram collection, but browsing existing records and creating exports work offline.

Run `python start.py --check` after setup to inspect local dependencies, Ed25519, storage, key configuration and the listening address without starting a collector. Use `--json` for structured output. Pass the intended `--data-dir`, `--host` and `--port`. The check does not install packages, create a journal or connect Telegram; it is not an integrity or coverage qualification. Startup separately verifies existing journals. `python start.py --help` also avoids installation.

Options:

After using start.py, run auxiliary commands with `.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on Linux/macOS, or activate that environment first. The `python -m ...` examples below assume the environment is active.

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

Environment variables: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN. TGWITNESS_VAULT_KEY_FILE selects external-key mode for a new installation; see below. TGWITNESS_TOKEN, if supplied, must contain at least 24 characters; use a cryptographically random value. Without it, the app generates a 256-bit random token in panel-token.txt. The environment override does not rewrite that file. Restart to rotate credentials.

Exactly one process may own a data directory. A cross-platform OS file lock prevents accidental concurrent writers. Use one Uvicorn worker. The panel can manage any number of workspaces, with additional workspace directories under profiles/<id>/. For separate service instances, use separate directories and ports. SQLite WAL files belong on local persistent storage, not a network filesystem. Do not share one volume between replicas.

## Windows portable package

Each GitHub Release carries `TgWitness-<version>-windows-amd64-portable.zip` and its `.sha256`. It contains the official embeddable Python 3.12 runtime from python.org (checksum pinned in `tools/build_portable.py`), TgWitness and its pinned dependencies, and three launchers:

| File | Purpose |
| --- | --- |
| `TgWitness.cmd` | Start the panel; extra options are passed through, e.g. `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | Start the synthetic demo in `data\demo` |
| `TgWitness-Check.cmd` | Run the readiness check without starting |

Extract the whole archive to a writable folder such as `Documents\TgWitness`; do not run it from inside the ZIP or from Program Files. The runtime uses an isolated module path, so other Python installations and `PYTHONPATH` do not affect it. Data stays in the package's `data` folder. To update, stop TgWitness, extract the new version to a new folder and copy the `data` folder across.

Build it yourself on 64-bit Windows with Python 3.12:

```
python tools/build_portable.py
```

The builder verifies the runtime checksum, installs the constrained dependencies into the package, runs the readiness check with the embedded interpreter and writes the ZIP and checksum to `dist/`.

## Container

```
docker compose up -d --build --wait
```

This creates a named persistent volume for /data. The web port is mapped to 127.0.0.1:8787. The process runs as UID 10001 with dropped capabilities, a read-only root filesystem, and writable /data and /tmp. `--wait` checks web-server health before returning; it does not establish Telegram authorization or delivery. The supplied helpers use a 180-second readiness timeout after building. Initial dependency downloads can take longer than that.

Both base Compose files use the project name `tgwitness`, so extracting a new release into another directory does not silently select a new data volume. Keep only one deployment active for that project. For independent installations, use a unique `docker compose -p NAME ...` and a different host port, and retain both on updates. For an older deployment using a different project name, continue using its original name with `-p`; `docker compose ls` lists existing projects.

Copy `deploy/env.example` to `.env` and change `TGWITNESS_PORT` to use a different loopback port. For example, `TGWITNESS_PORT=8788` exposes the panel at `http://127.0.0.1:8788`; the container still listens on 8787. `.env` is Git-ignored.

Retrieve the initial token:

```
docker compose exec tgwitness cat /data/panel-token.txt
```

Useful commands:

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` restarts the collector after a crash or Docker daemon restart. On a Linux server, enable Docker at boot using your distribution's service manager, commonly `sudo systemctl enable --now docker`. On Windows/macOS, enable Docker Desktop's start-at-sign-in setting. Desktop sign-out, sleep, or a stopped Docker daemon can interrupt collection. An explicitly stopped container stays stopped until you start it again.

The /tmp volume is capped at 512 MiB in the example configuration. Export construction uses each workspace's `temporary-exports/` on persistent /data instead. Reserve space there for simultaneous exports, journal/WAL growth, media and backups. The launcher uses deploy/constraints.txt to pin qualified runtime dependency versions. Docker and high-assurance servers install from deploy/requirements.lock and deploy/build.lock with pip --require-hashes: every package file must match a SHA-256 recorded in the commit, so a file replaced on PyPI or a mirror is refused. The Python base image and operating-system packages still require independent release qualification.

Do not use docker compose down -v unless you intend to destroy the journal and keys. Container health reports web-server availability, not successful Telegram capture. Inspect the panel's collector state, heartbeat, errors, and coverage events.

### Independent witness profile

The optional `witness` service runs an [independent witness](https://phishdestroy.github.io/TgWitness/docs/reference/witness/) in its own container, with its own key and journal in the `witness-data` volume and only a read-only witness token for the collector. Create the token on the panel's **Witness** page, add it with a bot token and channel to `.env`, then start the profile:

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

The service reaches the collector inside the Compose network at `http://tgwitness:8787` (`TGWITNESS_WITNESS_COLLECTOR` overrides it, for example `/profiles/<workspace ID>` for another workspace). For a witness on a separate server, run by someone else, use `deploy/compose/compose.witness.yaml` there with `TGWITNESS_WITNESS_COLLECTOR` set to the collector's HTTPS address; that file contains only the witness.

## Install a published image

This becomes available after a successful [release workflow](https://phishdestroy.github.io/TgWitness/docs/reference/deployment/#automated-github-releases) and public GHCR package configuration. The repository's owner/name is not hardcoded into this source tree. Use the image shown in that release's workflow summary.

Copy `deploy/env.example` to `.env`. Set `TGWITNESS_IMAGE` to the published version, using the **lowercase** repository path, for example:

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.8.1
TGWITNESS_PORT=8787
```

Run this file on its own, instead of `compose.yaml`:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

No source build, Python, or compiler is needed on the host. The release workflow targets Linux AMD64 and ARM64 containers, including Docker Desktop's Linux VM. Use a version tag or `ghcr.io/owner/repository@sha256:...` from the workflow summary. No moving `latest` tag or unattended application upgrade is configured. The image and source variants use the same data volume when their project name matches.

## Automatic HTTPS on a server

Use a server with Docker, a domain you control, and persistent local storage. Point the domain's A/AAAA records at the server; publish AAAA only if IPv6 reaches it. Allow inbound TCP 80 and 443 and outbound DNS/HTTPS for certificate issuance. Other services must not already own these ports.

Copy `deploy/env.example` to `.env` and set a hostname, without a scheme or path:

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

Start the source build with the HTTPS overlay:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

For a published image, use `deploy/compose/compose.image.yaml` as the first file instead. Keep both `-f` arguments for later status, logs, update, and stop commands.

Caddy obtains and renews a certificate, redirects HTTP to HTTPS, and forwards requests to the collector on the private Compose network. Certificate state has its own persistent volume. The collector's direct host port remains loopback-only. The supplied Caddy configuration does not enable access logging.

Open `https://watch.your-domain.org` and enter the panel token. Compose readiness does not confirm certificate issuance or external reachability. If HTTPS is not ready, inspect DNS, firewall rules, and:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

The supplied Caddy image follows its `2-alpine` tag. Pulling refreshes that image; pin a tested digest in your deployment if you need fixed infrastructure versions.

## Updates and backups

Preserve the Compose project name and data volume across updates. First stop the collector and make a complete backup. For the default source-based deployment:

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Use a new backup destination each time, outside the repository, and protect it as account-access material. The example path is illustrative; use your private backup location. Copy the entire directory, including hidden files, all workspaces, keys, journals, and media. Back up an external vault master key separately if configured. An evidence ZIP is not a restorable application backup. For HTTPS, also preserve the Caddy volumes if you need to retain its certificate/account state.

For a source deployment, obtain the new release files and run:

```
docker compose up -d --build --wait
```

For an image deployment, change `TGWITNESS_IMAGE` to the desired version, then run:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Use your installation's Compose file(s) for the preceding stop/copy commands too. Keep `.env`, custom configuration, and the same project name. `down` keeps named volumes; **`down -v` deletes them**. Do not copy `.venv` between operating systems or Python versions. For native updates, stop TgWitness, back up its full data directory, replace source files, and run `python start.py --setup-only` before launch.

Check panel access, account identity, observation state, and coverage after an update. Restarting does not reconstruct missed Telegram updates. A rollback may require the pre-update backup if a future version changes storage formats.

## Automated GitHub releases

The [release workflow](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml) is ready to use after this project is pushed to a GitHub repository with Actions enabled. It runs when a GitHub Release is **published**, including a prerelease. Drafts and tag pushes alone do not publish packages.

1. Set the package version and changelog, then publish a release tagged with `v` plus the exact `pyproject.toml` version, such as `v0.8.0`.
2. The workflow validates the tag and runs the shared Windows/Linux/macOS Python, general/account-import/QR browser, source-package, and Docker checks. Fresh native installation is also exercised on all three operating systems using Python 3.12.
3. After those checks pass, it smoke-tests an ARM64 image under QEMU, publishes AMD64/ARM64 images to `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>`, and attaches the source ZIP and Python wheel with their SHA-256 sidecars. The Windows portable ZIP is the exact artifact tested by the checks workflow; the release workflow downloads and publishes that artifact and its checksum.
4. A final job downloads all three published packages again and verifies their checksums. It then publishes `SHA256SUMS.txt` and `RELEASE-MANIFEST.json`, recording the version, source revision and asset sizes. Uploads refuse to overwrite existing release assets.
5. After the first publication, open the GHCR package settings and set visibility to **Public** if anonymous image pulls are intended. A public source repository alone does not guarantee a public container package. Organization policies must permit package publication. The workflow uses `GITHUB_TOKEN`; no registry password or VPS credentials belong in the repository.

Remote workflow success has not been established by this local preparation. ARM64 emulation is a smoke check, not native-hardware or live Telegram qualification. This automates release packaging; starting a server still requires the Compose command and its domain/host prerequisites. Existing servers are not silently upgraded or restarted when a release is published.

## Remote server

Keep the service bound to loopback and use an SSH tunnel, or terminate HTTPS at a reverse proxy. The base Compose file is local-only; the optional `deploy/compose/compose.https.yaml` overlay supplies Caddy for a configured domain. Keep the bearer token out of URLs and proxy logs. A reverse proxy should limit request size and connection rates. Do not expose plain HTTP to the Internet.

Examples for systemd, a Windows logon task, a macOS user agent and Caddy are provided in [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Review/adapt their paths before installation. They are supplied templates, not locally executed platform qualifications. No background service or task is registered by the normal launcher.

On Windows, a windowless `pythonw.exe` launch stores startup/server diagnostics in `logs/server.log` under the data directory (5 MiB per file, two rotated backups). Console launches retain console logging. HTTP access logging is disabled in both modes. Protect logs with the data directory and review them before sharing.

## Restart and gaps

The last requested observation state is persisted. If observation was active, startup attempts to reconnect and resume selected sources. Manual pause clears that intention. A failed restart is recorded and shown in the panel.

StringSession retains authorization but not Telethon's durable update/entity state. Dialogs are reloaded on start. Telegram/Telethon can recover some transport interruptions while running, but TgWitness does not claim durable replay across process restarts. Every startup records the preceding journal head and the offline boundary. The monitor checks connectivity every 10 seconds and adds a heartbeat every minute (**Parameters → Liveness record every**). Brief interruptions can be missed; a connected transport does not guarantee complete update delivery. Snapshots are explicit current-history observations, never gap repair.

The media queue is stored in each workspace's SQLite database. A message and its job are committed atomically. Interrupted running jobs are recovered for retry on start. Each download has a 120-second base timeout plus time at 256 KiB/s for its size, and a 1–2,000 MiB limit per attachment type; timeout, speed and retries are under **Parameters**. The collector skips files whose size is unknown. Pausing retains queued work. Retry uses the original observed file descriptor, never the latest version of a subsequently edited message. Temporary failures have bounded retries; media FloodWait pauses survive restart. Media recovery is separate from Telegram update recovery and cannot recreate vanished files.

## Backup, restore, and capacity

Stop the process before copying the **entire data directory**, including vault.key, signing.enc, credentials.enc, SQLite database/WAL files, media, token, checkpoints, and all profiles/ subdirectories. Restore the complete copy while the destination service is stopped. Missing vault keys or signing-key mismatch cause startup to fail; do not regenerate keys to force access.

Keep secret backups encrypted and access-controlled. Evidence ZIPs are portable review artifacts, not application backups or Telegram-session backups. There is no automatic retention deletion. Plan disk space for all messages, raw metadata, media, temporary exports, and backups.

Startup verification and export stream records instead of loading the whole journal. An export pins a read snapshot while new WAL writes can continue; long-running exports can retain WAL pages, so disk capacity still matters. ZIPs are capped at 4 GiB uncompressed to match the independent verifier's default; **Parameters → Largest signed ZIP** raises the cap, and such archives are verified with `verify.py --max-gib N`. Other formats have no event-count cap. Supported browsers stream response chunks to a user-selected file. Other browsers buffer at most 128 MiB and direct larger transfers to the authenticated CLI:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Use `--profile ID` from **Exports → Workspace ID** for another workspace, `--format zip|jsonl|csv|html`, `--url https://your-server` for a remote server, or `--max-mib` to change the 5 GiB transfer limit. Plain HTTP is allowed only for loopback. Tokens travel in headers, redirects are refused, existing files are not overwritten, and incomplete downloads are not published as finished files. If TGWITNESS_TOKEN overrides the generated token, use a separately protected file containing that active value: panel-token.txt is not rewritten by the override. The command's SHA-256 is only a transfer checksum; independently verify the signed ZIP.

Server export files remain inside each workspace's private `temporary-exports/`. Successful responses clean up their files. Interrupted exports are removed at the next workspace startup with its exclusive instance lock held. This directory is part of the storage threat/capacity model; use an encrypted data volume. Production-scale multi-gigabyte transfers still require qualification on your target system.

The panel displays queued/failed media, oldest pending media, free disk, Telegram request pauses, and sources whose access is unconfirmed. These diagnostics are not a complete end-to-end delivery monitor. Workspaces share a process; a noisy account can still affect others. Separate worker processes, retention/rotation, durable update recovery and full deployment qualification remain. Scoped panel access is documented in [access and permissions](https://phishdestroy.github.io/TgWitness/docs/reference/access/); independent checkpoints are covered by the [witness guide](https://phishdestroy.github.io/TgWitness/docs/reference/witness/).

## Connection and protection options

Connection routes are per workspace and should be configured before authorization. SOCKS5/HTTP CONNECT use the pinned python-socks dependency. MTProxy uses Telethon's experimental randomized intermediate transport; Fake TLS ee secrets are unsupported. Direct fallback depends on the selected [IP mode](https://phishdestroy.github.io/TgWitness/docs/reference/connection/#ip-modes): **Hide the address** refuses it; **Direct as a last resort** permits it after a delay. **Server behind a tunnel or VPN** permits direct routes but does not create a VPN. This is not a system-wide network policy.

For new installations, TGWITNESS_VAULT_KEY_FILE points to a separately protected random master-key file. Mount it read-only outside /data in a container. Preserve the public vault.external.json salt metadata with each workspace and the master key separately. Existing local vaults require a planned migration; setting this variable does not silently convert them. Message/media storage and exports are not application-encrypted. Use encrypted volumes and sufficient private temporary storage where needed.

Detailed procedures: [connection/security](https://phishdestroy.github.io/TgWitness/docs/reference/connection/) and [operating modes](https://phishdestroy.github.io/TgWitness/docs/reference/operations/).


---

# High-assurance deployment

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/

A sealed 24/7 server on Hetzner or Phala Cloud, Gateway DNS and the checks a third party can repeat.

A signed journal proves that records were not changed **after** signing. For serious cases the next question is whether anyone could have shaped the data **before** it was signed: who ran the collector, on which machine, and whether someone logged in to it. This optional mode deploys the collector so that a third party can check that, using records kept by the cloud provider and Cloudflare rather than the operator's word.

Ordinary local and Docker use is unchanged. Nothing here runs unless you deploy with `python -m tgwitness.cloud`, and the collector reads its host only when the deployment sets `TGWITNESS_ASSURANCE`.

Flow diagram · Operator → Server, firewall without inbound rules (provider API); Operator → Tunnel and DNS (Cloudflare API); Server, firewall without inbound rules → Tunnel and DNS (outbound only); Server, firewall without inbound rules → Signing key created on the server; Verifier, read-only tokens → Provider log and firewall; Verifier, read-only tokens → Tunnel connector address and ingress; Verifier, read-only tokens → Signed /api/assurance statement; Verifier, read-only tokens → Evidence ZIP · Operator · Verifier, read-only tokens · Server, firewall withoutinbound rules · Provider log and firewall · Tunnel connector addressand ingress · Signed /api/assurancestatement · Evidence ZIP · Tunnel and DNS · Signing key created on theserver · provider API · Cloudflare API · outbound only

**Diagram as text**

1. Operator → Server, firewall without inbound rules (provider API)
2. Operator → Tunnel and DNS (Cloudflare API)
3. Server, firewall without inbound rules → Tunnel and DNS (outbound only)
4. Server, firewall without inbound rules → Signing key created on the server
5. Verifier, read-only tokens → Provider log and firewall
6. Verifier, read-only tokens → Tunnel connector address and ingress
7. Verifier, read-only tokens → Signed /api/assurance statement
8. Verifier, read-only tokens → Evidence ZIP

## What a verifier can check

| Claim | How it is checked | Kept by |
| --- | --- | --- |
| The server was created through the provider API at a known time | Server object and its creation in the provider's own log | Provider |
| Nobody used the provider's access paths | Log of console requests, rescue, password reset, rebuild, ISO, images, backups | Provider |
| Nothing could connect to it | The provider firewall has no inbound rules; SSH is masked from the first boot | Provider (firewall), host (SSH) |
| The panel is reached only through the tunnel | Tunnel ingress forwards to the panel alone; the connector runs from the server's address | Cloudflare |
| This exact software runs | The collector's signed source-tree hash equals a checkout of the deployed commit | Collector, checked against Git |
| The signing key was created on that server | The key signs a statement naming the provider's server ID and the hash of the cloud-init it received | Collector, checked against the provider |
| The journal belongs to that key and server | Every process start in the evidence ZIP carries the host measurement for that server | Evidence ZIP |

Host measurements (SSH listeners and processes, current sessions, logins in `wtmp`, the boot) are reported by the collector itself and are signed into every process start and into `host.state` records whenever they change. Root on the server could falsify them; they support the provider and Cloudflare records rather than replace them.

## Providers

| `--provider` | Credentials | Verifier's read-only access | Provider log for the verifier | Kept for |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Read token of the same project | Server and firewall actions | While the resources exist |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Read-only personal access token | Droplet actions | While the Droplet exists |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` read-only scopes | Account events, firewall rule versions | 90 days |
| `vultr` | `VULTR_API_KEY` | User with read access and the `activity_logs` permission | Account activity log (method, path, actor) | 30 days, longer with an audit-log subscription |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | CloudTrail event history | 90 days |
| `phala` | `PHALA_CLOUD_API_KEY` | An API key of the same workspace | Application revisions: compose and environment changes, restarts, OS upgrades | While the application exists |
| `generic` | none | none | none: **self-attested** | – |

Use a dedicated project, team, account or sub-account for each case: the verifier's read-only access then shows only this deployment. Credentials are read from `--provider-token-file` or the variable above, never from the command line. For AWS the file holds `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; the region is `--location`.

What each provider's records cannot show is printed in every report. In short: Hetzner logs console requests; DigitalOcean's Recovery Console, Linode's Lish/Glish and Vultr's web console are not logged as such, so root is locked at the first boot and a console login would need a password reset or a boot change, which are logged. Vultr returns the console address to any key that can read the instance; neither the record nor the report stores it.

## Confidential VM on Phala Cloud (Intel TDX)

With `--provider phala` the collector runs in an Intel TDX confidential virtual machine on [Phala Cloud](https://phala.com/), managed by dstack. The host and Phala's staff cannot read its memory, and the processor signs an attestation of what the machine booted. The verifier does not take Phala's word for it: `tgwitness.tdx` checks every attestation itself, up to the pinned Intel SGX Root CA, against Intel's revocation lists and Intel's signed platform data, and refuses machines that can be debugged or migrated.

| Report entry | What it shows |
| --- | --- |
| `tdx_binding` | The attestation covers the signed statement of the collector and the random value of this request |
| `tdx_quote` | Intel vouches for the attestation; it passes only when Intel rates the platform as up to date |
| `tdx_compose_hash` | RTMR3, replayed from the dstack event log, measures the app-compose the collector reports |
| `tdx_compose` | That compose is byte for byte the one the code of the deployed commit builds: source files pinned by hash, both images by digest, no other code |
| `tdx_identity` | The attestation comes from the deployed application and instance, with keys from Phala's KMS and an encrypted disk |
| `tdx_os` | With `--tdx-measurements`, MRTD and RTMR0-2 equal the values computed from the dstack OS image (`dstack-mr measure --json`) |

Every start of the collector recorded in the journal carries such an attestation, so `verify --evidence` checks each start. Phala's list of application revisions serves as the provider log: if the compose changed after the deployment, the report fails.

In the panel choose **Confidential virtual machine · Phala Cloud** under **Extras** → **Server 24/7** and paste a Phala Cloud API key; the quick tunnel works as on Hetzner. From the command line:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --tdx-measurements dstack-mr.json
```

`--tdx-collateral` reads Intel's certificates and revocation lists from a file instead of downloading them from Intel. Gateway DNS is not available here: Phala has no provider firewall for outgoing traffic.

An attestation cannot rule out a flaw in Intel's TDX module or microcode, or physical access to the memory bus. Whoever controls the application in Phala's account can deploy another compose; it appears as a new revision with a new compose hash. The host controls the machine's time source and network.

## Before you start

1. A Cloudflare zone, its account ID, and an API token with **Cloudflare Tunnel Edit**, **Zone Read** and **DNS Edit**, given with `--cloudflare-token-file` or `CLOUDFLARE_API_TOKEN`. For the verifier: **Cloudflare Tunnel Read**, **DNS Read** and, for the audit log, **Account Settings Read**. Without a domain, a [quick tunnel](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/#quick-tunnel-without-a-domain) needs none of this.
2. Provider credentials with write access to a dedicated project; `lock` uses the same:

   - Hetzner: API token with Read & Write permission;
   - DigitalOcean: personal access token with write access;
   - Linode: personal access token with `linodes`, `firewall` and `events` read/write scopes;
   - Vultr: API key of a dedicated account or sub-account;
   - AWS: IAM credentials allowed `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` and `ec2:RevokeSecurityGroupIngress`.
3. The commit to run. A release tag is resolved once to its commit with `git ls-remote`; the server only ever receives the 40-character commit.

## From the panel

On your own computer, **Extras → Server 24/7** runs the same `deploy` for Hetzner in three steps: choose Europe or the United States, paste a Hetzner token (Read & Write), then review the server type, monthly price, address and version the panel found with that token. Nothing is created before you confirm. The panel shows each step as `deploy` reports it, then the address, the panel token and the signing key fingerprint. Without a domain the server gets a [quick tunnel](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/#quick-tunnel-without-a-domain); **Your servers → Find the current address** looks it up again after a restart. For a fixed address under your own domain, open **Optional · your own domain** and add a Cloudflare token (the prepared link selects Zone Read, DNS Edit and Cloudflare Tunnel Edit).

The tokens travel with each request from the browser tab to TgWitness on the same computer and are not written anywhere; the deployment record, redacted cloud-init, panel token and, for a quick tunnel, the address key are kept in `deployments/NAME` inside the data directory. The panel offers this only to the main administrator on a direct loopback connection (`127.0.0.1`, no proxy or tunnel headers); a panel reached over a network shows the commands instead. The version defaults to the release tag of the running panel, resolved through the GitHub API. Location, server type and price come from Hetzner's API: `cpx22` where it is offered, otherwise the cheapest x86 type with at least 2 GB of memory.

## Quick tunnel without a domain

`--quick-tunnel` replaces `--zone`, `--cloudflare-account` and `--panel-host`; no Cloudflare account or token is involved:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

On the server, cloudflared opens a [quick tunnel](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) to the panel: a random `https://….trycloudflare.com` address that changes whenever cloudflared or the server restarts. A small service on the server posts each address to a random ntfy.sh topic, signed (HMAC-SHA256) with a key only the deployment directory holds (`address-key.txt`), and repeats it every three hours because ntfy.sh keeps posts for 12. `deploy` and **Find the current address** accept signed posts only, so a forged post cannot send you, and your panel token, to someone else's address. The topic is in the record and the published cloud-init: whoever has them can read the current address, which still asks for the panel token. The server keeps no inbound port either way.

What it costs: no Cloudflare account keeps records of a quick tunnel, so `verify` reports the tunnel, connector and DNS check as unavailable and the result is at best `incomplete`; the provider records, firewall, signed statement, host measurements and installer comparison are checked as usual. The byte comparison with the reference installer needs a deployed commit that already knows `--quick-tunnel`; a 0.7.0 checkout builds the domain installer and reports the difference. Cloudflare gives quick tunnels no uptime guarantee, allows 200 requests in flight and does not carry Server-Sent Events, so the panel's live updates (versions after 0.7.0) may not arrive through one and a view needs reloading; that part has not been tried. For a case that has to stand, use your own domain.

## Deploy

Look at everything that will be sent first. `plan` makes no provider or Cloudflare request:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

Then deploy with the same options and the credentials:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Server types to start with: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` and `--image` default to each provider's Ubuntu 24.04 in a European region.

`--repository` takes the commit from another https Git repository, without credentials in the URL (default `https://github.com/phishdestroy/TgWitness.git`). `deploy` also accepts `--out` for another deployment directory (default `deployments/NAME`; a directory that already holds a deployment is refused) and `--wait`, the minutes to wait for the collector's signed statement: 1 to 240, default 20, or 60 for `generic`.

The command:

1. creates a Cloudflare tunnel whose ingress forwards the panel hostname to the panel and, if given, the witness hostname to `/api/witness/head` and `/api/assurance` only;
2. creates proxied CNAME records for those hostnames, refusing names that already exist;
3. creates a provider firewall without inbound rules and a server behind it with no SSH key, no backups, no console agent, and cloud-init that masks SSH, locks root, installs `cloudflared`, fetches exactly the commit, checks it and starts TgWitness as a hardened systemd service;
4. waits for the collector's signed statement and checks that it names this server and the hash of this cloud-init.

`deployments/case-2026-11/` then holds:

| File | Contents | Share? |
| --- | --- | --- |
| `deployment.json` | IDs, hashes, the API calls made (method, path, status) and the first signed statement | Yes, with the verifier |
| `cloud-init.redacted.yaml` | The exact cloud-init with its two secrets replaced by `REDACTED` | Yes |
| `panel-token.txt` | The panel token | No |

The provider's root password, the tunnel token and the panel token are never written to `deployment.json`. Publish the collector fingerprint printed at the end through a channel you do not control alone, for example a witness channel or a message to the recipient.

Sign in to Telegram at `https://case.example.org` with the panel token, as in the [account guide](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/). Panel actions are recorded in the signed journal; they are not SSH sessions. A [witness](https://phishdestroy.github.io/TgWitness/docs/reference/witness/) can poll `https://case-witness.example.org`.

There is no SSH: if the bootstrap fails, the collector never answers. Delete the server and deploy again, or use a debug deployment to find the cause.

### Secrets in the user data

The cloud-init carries two secrets: the panel token and the Cloudflare tunnel token. The signing key is not among them; it is created on the server. Hetzner, DigitalOcean and Linode do not return user data through their API. Vultr returns it to any key that can read the instance, and EC2 through `DescribeInstanceAttribute`. For AWS give the verifier only the three actions in the table, never `ec2:Describe*`. For Vultr, assume the verifier's key can read both tokens. A tunnel token lets someone run a second connector: `verify` reports any connector not on the server, and the collector's statements cannot be forged that way because each one signs a fresh challenge. With `--quick-tunnel` the second secret is the address key instead: whoever reads it can post a false address that the panel would accept.

The collector's public statement leaves out the server's address and the sources of logins; both stay in the signed journal.

## Debug deployment and lock

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` keeps SSH for one key from one address or small network, at most a /24 for IPv4 or a /48 for IPv6. `KEY` is already registered with the provider: the name or ID of an SSH key in the Hetzner project, the ID or fingerprint of an SSH key in the DigitalOcean team, a Linode username whose profile SSH keys are added to root, the ID of an SSH key in the Vultr account, or the name of an EC2 key pair in the region. These options do not apply to `generic`. Such a deployment is recorded as `debug` and is **never** reported as high-assurance. When you are done, run `sudo tgwitness-lock` as the last command of the last SSH session, then:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

The firewall loses every inbound rule. Reports then show when SSH was allowed and when it was closed; that window stays visible.

## Remove a deployment

`destroy` deletes the server and its firewall, found by the deployment's label so that a deployment which failed half-way is removed as well, then the DNS records that point to its tunnel, and the tunnel. The server's journal and signing key are deleted with it: export the evidence first. The record stays, marked `removed`, with the API calls of the removal.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Removal through the API is implemented for Hetzner. For other providers `destroy` stops before deleting anything and names the label to delete in the provider's console. A hand-installed server (`generic`) loses only its tunnel and DNS records. A quick tunnel deployment needs no Cloudflare token: its tunnel ends with the server, and its posts expire from ntfy.sh within 12 hours.

## Any server (self-attested)

`--provider generic` is for a server bought or installed by hand. `deploy` creates the tunnel and DNS, writes `install.sh` (private) and `install.redacted.sh` (to publish), and waits. Copy `install.sh` to a freshly installed Ubuntu 24.04 server and run it there:

```
sudo bash install.sh
```

It records the host as it was (logins, accounts, `authorized_keys`, listening sockets, services, scheduled jobs, packages), installs the commit, enables a host firewall, deletes itself, masks SSH and ends the session. The report for such a server is at best **SELF-ATTESTED**: whoever ran the installer had root before it, and no provider record is available to the verifier. It is still better than an unexplained server: the inventory, the installer hash and every later login are signed.

## Verify

The verifier needs `deployment.json`, the published installer, read-only credentials and, ideally, a checkout of the commit and an evidence ZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

Every provider and Cloudflare value is requested by the verifier at that moment; the record supplies only the IDs to ask about. The exit code is 0 for **PASS**, 1 for **FAIL** and 2 for **REVIEW**, **INCOMPLETE** or **SELF-ATTESTED**. `--fingerprint` should come from an independent channel; without it the key is compared with the operator's record only. `python verify.py` still verifies the evidence ZIP itself, as in [Evidence](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/).

Provider actions are classified: creation and start within 30 minutes of creation pass; console, rescue, password reset, rebuild, ISO, images, snapshots, backups, Systems Manager, EC2 Instance Connect and firewall openings fail; power actions and anything not expected are marked for review. An unknown action never passes silently.

## Report for evidence handover

`--report report.md` writes the Markdown report and `report.json` beside it:

1. result, collector key fingerprint, deployment, provider, commit, server, firewall, tunnel;
2. every check with its status and source (provider API, Cloudflare API, collector statement, evidence journal);
3. the provider log with each action's assessment and, where the provider records it, the actor;
4. the Cloudflare endpoints holding the tunnel's connections, configuration and audit log;
5. the signed collector statement;
6. what the report establishes and what it does not;
7. commands to reproduce it, and the SHA-256 of every file it was given.

Hand over the report, `report.json`, `deployment.json`, the published installer and the evidence ZIP. Produce the report early: provider logs are kept for limited periods.

## Cloudflare as an outside witness

Everything here is optional. Without a Cloudflare account the server still runs, and two of these work today:

| What | What it shows | In TgWitness |
| --- | --- | --- |
| Quick tunnel or your domain's tunnel | the panel is reached only through the tunnel | the server wizard, see above |
| drand relay `drand.cloudflare.com` | records after a drand round are newer than it: the journal was written as it went | evidence mode, **More witnesses**, no account ([format](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| Tunnel health notifications | when the tunnel was down, by email or webhook from Cloudflare | set them in the Cloudflare dashboard |
| Gateway DNS (`--gateway-dns`, or **Cloudflare Gateway DNS** in the wizard) | every name the server looked up, answered by Cloudflare over TLS; the Hetzner firewall lets DNS reach nothing else; whether a Gateway policy could rewrite answers | Hetzner, free Zero Trust plan, no domain; `verify` checks the firewall, the location, logging, policies, the server's queries and the audit log; evidence mode copies the log into the journal |
| Gateway with the Cloudflare One client on the server, an outbound firewall that allows only Cloudflare | every connection the server made, not just DNS | not built yet |
| Access in front of the panel | who signed in to the panel and when | not built: needs your own domain |
| SSH command logging | each command in a debug session | not built yet |

Logpush, which would keep Cloudflare's own copy in R2, is an Enterprise feature: on the free plan Cloudflare answers `logpush is not enabled for this account`. Its Gateway log lasts 24 hours there, so evidence mode copies it into the signed journal (**Cloudflare Gateway's log of this server's DNS queries**, a read-only token with Account Analytics Read).

Without a Zero Trust plan an account has one DNS location. When Cloudflare refuses another, the server shares the existing one and its queries are told apart by its address; that filter needs Zero Trust PII Read as well, and `destroy` leaves a shared location. One log query spans at most three hours, so the copy and `verify` read the day in three-hour windows.

Gateway DNS covers the system resolver. DNS over HTTPS on port 443 to another resolver, and connections to an address looked up nowhere (Telegram's data centres, for one), are not in its log.

Cloudflare cannot see inside Telegram's encryption, other devices on the Telegram account (evidence mode's device list records them from Telegram's side) or the provider's hypervisor.

On 1 November 2026 Gateway DNS ran against real Hetzner Cloud and a free Cloudflare account: Hetzner accepted the outbound rules, the server installed v0.7.0 with every lookup going through Gateway over TLS, the quick tunnel worked through that firewall, and `verify` read the server's 19 names back from Cloudflare (Ubuntu and Hetzner mirrors, GitHub, PyPI, NTP, the tunnel, ntfy.sh). The panel copied 36 queries in eight windows into a journal and `verify.py` summarised them without gaps; `destroy` removed the server and firewall and left the shared location.

## What this does not establish

- The provider and its staff control the hypervisor, disks and network.
- Host measurements are self-reported by the collector.
- Earlier firewall rule contents are not in every provider log; only Linode keeps rule versions.
- It says nothing new about message authenticity; see [Evidence](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/).

## Tested here

The deployment, lock and verification logic is covered by automated tests against simulated Hetzner, DigitalOcean, Linode, Vultr, EC2/CloudTrail and Cloudflare APIs built from their published API references, and the AWS request signing against AWS's published examples. `tools/check_cloud_wizard.py` runs the panel's server wizard the same way, with a domain and with a quick tunnel. `tools/check_tdx.py` verifies real Intel TDX attestations from dcap-qvl and dstack up to Intel's root certificate (sources in [tools/tdx/README.md](https://github.com/phishdestroy/TgWitness/blob/main/tools/tdx/README.md)); `tools/check_phala.py` runs deploy, verify, the journal, destroy and the panel wizard against a simulated Phala Cloud whose attestations come from a forged PKI shaped like Intel's. The Phala path has not yet been tried on Phala Cloud itself.

On 1 November 2026 the quick tunnel path ran against real **Hetzner Cloud** (Nuremberg, `cpx22`, TgWitness v0.7.0), real ntfy.sh and GitHub, from the panel and from code:

- the price check, then creation from the panel's buttons: server running after 13 seconds, signed statement with matching instance and installer hashes after about two minutes;
- the server's own panel opened through its trycloudflare.com address and accepted the panel token; without the token it answers 401;
- after a reboot through the Hetzner API the server posted a new signed address, **Find the current address** found it, the old address stopped answering, the signing key stayed the same; an unsigned post to an ntfy.sh topic was ignored;
- `verify` against Hetzner's API: server, firewall without inbound rules, statement, binding, host measurements, boot and the source hash of a v0.7.0 checkout passed; the Cloudflare checks were unavailable, as described above; the installer differed from the one v0.7.0 builds and equalled byte for byte the one this version's code builds;
- deletion from the panel removed exactly the server and firewall the deployment labelled; other servers and firewalls in the same project were untouched.

Not yet run against real accounts: a deployment under your own domain (Cloudflare tunnel and DNS), the other providers, a debug deployment and `lock`, a Telegram account on such a server, and the live updates of later versions through a quick tunnel. Check the first deployment on each provider with `plan`, a debug deployment and `verify` before relying on it in a case.


---

# Panel guide

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/panel/

Every screen of the panel: chats, journal, sources, exports, Extras, protection modes and the code check.

[First setup and settings](https://phishdestroy.github.io/TgWitness/docs/reference/settings/) · [Accounts](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/) · [Export and verify](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/) · [Case reports](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/)

What each screen does, what it writes to the signed journal and where the detailed guide is. The panel shows one workspace at a time: one Telegram account with its own sources, journal and signing key. The selector at the top of the sidebar switches workspaces. The address carries the workspace (`?ws=…`); while the address, the selector and the loaded account disagree, actions stay blocked.

## Find your way

Daily sections are at the top of the sidebar, **Accounts** is under **Workspace**, and everything else is under **More tools & settings**. The **Interface level** switch in the top bar decides how many sections appear:

| Level | Sections in the sidebar |
| --- | --- |
| Simple | Home, Chats, Changes, Archives and Settings |
| Standard | Also Case Board, Accounts and Access |
| Expert | Also Sources, Extras, Ask the archive, Parameters, Account, System log and Integrations |

Simple calls Start here, Journal and Exports **Home**, **Changes** and **Archives**. A level only hides sections. A hidden feature keeps working, and the server checks every permission on its own. Level, language, theme and time zone are saved per operator and workspace; see [settings](https://phishdestroy.github.io/TgWitness/docs/reference/settings/).

The top bar also has:

- **Go to a section** (Ctrl+K, or ⌘K on a Mac): find a chat, a parameter or a journal record by `#number`. Arrow keys move, Enter opens, Esc closes.
- **Notifications**: problems and chat changes worked out from the journal. **Mark all as read** clears the counter and **Notification rules** opens the rules. Delivery to Telegram, Discord or email is set up in [Extras → Notifications](https://phishdestroy.github.io/TgWitness/docs/reference/panel/#notifications).
- The connection indicator for this workspace. **Collector health** under the top bar splits it into the Telegram connection, event intake, sources and the attachment queue.
- **Lock**: closes the panel in this browser. Collection keeps running on the server.
- The protection mode next to the version number; see [protection modes](https://phishdestroy.github.io/TgWitness/docs/reference/panel/#protection-modes).

The demo workspace contains fictional messages and never connects to Telegram. Actions that would change a real workspace are refused there.

## Start here

Choose a task. **Export my account** downloads what the account can read now. **Follow an investigation** records new messages, observed edits and deletion notices from the chats you choose. The setup card shows the three steps: connect the account, choose sources, start observation. The goal question stays on this page until you answer or skip it. A new workspace opens the [first setup](https://phishdestroy.github.io/TgWitness/docs/reference/settings/) instead.

## Chats

Saved conversations, read-only by default.

- Search the list by name or ID. **Choose** adds or removes watched chats. **Open Telegram link** takes a username or invite link and saves a preview to the journal. **Join / open and observe** then joins the chat and adds it to your sources; opening a bot sends it `/start`.
- The chat header counts messages **deleted, text kept**, **deleted before saving** and **not found on recheck**. The chat list and notifications use the same definitions. A deleted message is red and keeps its saved text; an edited message keeps every saved version. Each deletion says what is known: when it was seen, that Telegram does not report who deleted it, or that only the notice arrived.
- **Load history** brings the last 100, 250 or 500 messages into this view and the journal. To load every enabled source, use [Sources → Full history](https://phishdestroy.github.io/TgWitness/docs/reference/panel/#sources).
- **Export chat** downloads the whole visible history as a signed `chat.json` and `chat.html`. Several connected accounts can share the work: each downloads its own range of message numbers and signs its part, and the account that starts the export signs the archive. See [export one chat](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md).
- **People** lists everyone with saved messages in this chat. People profiles are off by default because they are personal data about third parties. When they are on for a chat, a profile shows name and username history, Telegram flags, avatar hashes, activity, who replies to whom, other observed chats, and mentioned wallets, phones, usernames and links. Every fact points to its record. **Export profiles** saves a signed file, optionally in a password ZIP; turning profiles off deletes the profile file. See [people profiles](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#people-profiles).
- **Save profile now** records a snapshot of the chat or bot profile: description, members, invite link, bot commands.

### Read-only, sending and secrets

Two switches above the messages protect the account and the reader:

- **Read-only** is on when a chat opens. Turn it off to send messages or press bot buttons. Each action asks **Send as @account?** or **Press this bot button as @account?**, tells you that chat members see it and that it goes into the signed journal. **Do not ask again for 10 minutes in this chat** skips the question for a while. Sending is off for the **Evidence for a case** goal, in the panel and in the API.
- **Mask secrets** hides what looks like a password, a login code, an API key or hash, a bot token, a session string, a private key, a JWT or a payment card number (card numbers are checked with the Luhn sum). **Show** reveals one value; the reveal is recorded in the journal. Turning masking off for this browser is recorded too. Only the display changes: the original records and every export keep the full text.

## Journal

Every record the workspace has signed, newest first.

- **Overview** counts observed messages, recorded edits, deletion notices and selected sources.
- **Event timeline** filters by event type (all, edits, deletions, reactions, membership, coverage), by text and by source. **Load earlier events** pages back.
- Open a record to see its details, hash and payload. **Link to this record** is an address that opens the same record. Possible secrets are masked in this preview; exports keep the original.
- The journal is append-only: nothing in the panel edits or deletes a record. Check it with **Exports → Verify journal** or `python -m tgwitness.verify`; see [export and verify](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/).

## Sources

Which conversations this workspace records, and what it keeps from them. Changes apply to future activity; saved records stay.

**Refresh chat list** reads the account's chats and folders. It does not download messages.

### Scope

- **What this account records**: **Chosen chats** (only the chats you add), **Telegram folder** (one of the account's folders, including chats added to it later) or **Whole account** (every chat, and every new chat, group, private chat or bot as it appears). **Investigation mode** is for a dedicated account: it records everything the account sees, its own messages and button presses, and saves each new chat's profile and earlier visible messages straight away. The [dedicated account guide](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) explains why never to use your main account.
- **Source types** limit folder and whole-account modes to channels, groups, private chats and bots. **Own actions** adds the account's own messages, edits and reply-keyboard presses.
- **When a new chat or bot appears**: save its profile and up to the chosen number of its latest visible messages.

Limits: secret chats never reach TgWitness. Nothing is recorded while TgWitness is not running; after a restart it catches up only what Telegram still returns, and the report shows the gap. Chats beyond the chat list limit (1,000 dialogs unless changed in Parameters) are added when they next become active. Inline bot buttons pressed in another app are invisible; the bot's reply is recorded.

### Chats in scope

Filter by status (**Enabled**, **Paused**, **Priority**, **Excluded**, **Unconfirmed access**, **Ignored**) and type, then act on a selection: enable, pause, mark or remove priority, exclude from scope or remove. The status badge only shows the state; actions are in each row's menu with a line on what they do. Pausing and excluding ask for confirmation, also in bulk. Removing a source asks for its name and deletes its people profiles; its saved records stay in the journal.

A source the account's chat list does not show is **receiving updates, not in the chat list** while records keep arriving, otherwise **access unconfirmed**. **Available chats** adds chats with **Add selected** or **Add all matching**.

### Full history

Loads the available history of every enabled source into Chats and the journal. Progress survives a restart; attachments follow your media settings. See [source history](https://phishdestroy.github.io/TgWitness/docs/reference/history/).

### Recording

- **Choose which changes to preserve**: new messages, edits, deletion notices, visible reactions, joins and leaves. A preset changes the form; **Save recording settings** applies it. Turning a category back on does not recover missed events.
- **Preserve media when available**: download attachments up to a size per file, set per type from 1 to 2,000 MiB, and limit video length in seconds (0 means no limit). Every download attempt gets a recorded outcome.
- **Recheck**: priority chats every few minutes, other chats rarely, so the account stays clear of Telegram's FloodWait limits. 0 turns a group off. Mark priority chats with the star in the list; chats per pass and the pause between chats are in Parameters. See [collection](https://phishdestroy.github.io/TgWitness/docs/reference/collection/).

## Exports

**Downloads** prepares files; **Build report** chooses how reports look.

| What | Use it for | Guide |
| --- | --- | --- |
| Account export | A fresh snapshot of what the account can read now | [Account export](https://phishdestroy.github.io/TgWitness/docs/reference/account-export/) |
| Sharing copy | A minimized derivative of a finished account export | [Disclosure](https://phishdestroy.github.io/TgWitness/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| Signed ZIP | Journal, report, attachments and verification tools at a fixed journal boundary | [Export and verify](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/) |
| HTML, PDF, JSON report | A sealed readable report | [Case reports](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/) |
| JSONL, CSV | Original records with signatures; a formula-safe spreadsheet | [Export and verify](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/) |
| Handover extract | Only the chats, period and people a recipient needs | [Evidence](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#investigation-handoff) |
| Chat export | One chat as signed `chat.json` and `chat.html` | [Export one chat](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **Encrypt the downloads above with a password** (12 characters or more) saves an AES-256 ZIP that 7-Zip or WinRAR opens. The signed file inside is unchanged. The password is not stored.
- **Prepared exports** keeps up to 20 files within 2 GiB, plus the latest one, for repeat downloads, each with its SHA-256. Preparing a file does not prove delivery.
- When the browser refuses its save dialog, the panel falls back to an ordinary download.
- **Your signing identity** shows the key fingerprint. **Save checkpoint** and **Download signed run receipt** give you records to keep outside the collector. **Prepare timestamp request** builds an RFC 3161 request without contacting any service.

## Settings, accounts and connection

- **Settings**: goal, connection, what to record and the interface. See [first setup and settings](https://phishdestroy.github.io/TgWitness/docs/reference/settings/).
- **Accounts**: every workspace with its state, sources, events and attachment queue. Filter by **Needs attention**, **Collecting**, **Offline or paused** or **Not connected**, pause or resume a selection, import account files in bulk and manage groups. See [accounts](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/).
- **Account**: sign-in and the connection route of this account. Direct, a WireGuard profile, your own proxy, the public MTProto pool or WARP; prepare and check a route, then apply it to this account, a group or all accounts. See [connection and proxies](https://phishdestroy.github.io/TgWitness/docs/reference/connection/) and [proxies](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md).

## Extras

Optional: an account and sources are enough to start collecting. Only the option you choose opens its settings, and nothing is connected automatically. The **Protection level** card at the top shows the [protection mode](https://phishdestroy.github.io/TgWitness/docs/reference/panel/#protection-modes).

| Card | What it adds | Guide |
| --- | --- | --- |
| Storage & disk space | Backups, moving older files to your cloud, an evidence copy that cannot be deleted | [Storage](https://phishdestroy.github.io/TgWitness/docs/reference/storage/) |
| Goal & protection level | Suggested settings for your goal and two scales | [below](https://phishdestroy.github.io/TgWitness/docs/reference/panel/#goal-and-protection-level) |
| Notifications | Problems, changed messages and a daily summary; your own control bot | [below](https://phishdestroy.github.io/TgWitness/docs/reference/panel/#notifications) |
| Evidence & backups | Timestamps, more witnesses and an encrypted off-site copy | [below](https://phishdestroy.github.io/TgWitness/docs/reference/panel/#evidence-and-backups) |
| Server 24/7 | A cloud server without SSH, created and deleted from the panel | [High assurance](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/#from-the-panel) |
| Independent witness | Signed checks posted to your Telegram channel or Discord | [Witness](https://phishdestroy.github.io/TgWitness/docs/reference/witness/) |
| Code check | Compares the running program with a public GitHub commit | [below](https://phishdestroy.github.io/TgWitness/docs/reference/panel/#code-check) |

### Goal and protection level

Four questions:

1. **What is it for?** A personal record, an investigation, or evidence for a case.
2. **How much will you observe?** A few chats (up to about 50), many chats (up to about 500) or whole accounts. This sets the chat list limit to 1,000, 3,000 or 20,000.
3. **Photos and files?** Text only, photos and short media (photos 20 MB, videos 100 MB), or everything (videos and documents up to 1 GB each). Everything with whole accounts also keeps 4 GiB of disk free.
4. **Where will it run?** This computer, or a server that is always on.

The suggestion lists independent timestamps, drand and Telegram's device list, each with a line on what it adds. Timestamps start every 60, 30 or 10 minutes for a personal record, an investigation or evidence; drand and the device list need timestamps. **Apply** changes only these, the attachment policy and the two parameters above. Each change is a journal record, plus `setup.applied`. Notifications, an off-site copy, a server, Gateway DNS, the code check and a witness are offered as next steps with their own forms.

Two scales are computed from what is set, not from the goal:

| Scale | Points |
| --- | --- |
| Credibility | Signed journal 1, timestamps 3, drand 1, device list 1, code check that matches 1, witness polling 1, attested server 2, Gateway DNS log 1 |
| Reliability | Always-on server 3, off-site copy 3, Object Lock 1, problem notifications 1 |

80% or more reads **maximum**, 50% **high**, 25% **moderate**, below that **basic**. Reliability currently counts an always-on server from the answer to question 4, before any server is checked.

### Notifications

Notifications go through Apprise to Telegram, Discord, Slack, ntfy, email, Matrix and 100+ other services. Pick a service, fill in one or two fields and send a test, or paste Apprise addresses directly.

- **Problems**: disk almost full, account signed out, collection, copy or timestamp errors. On a sealed server, an opened SSH port or a login is a problem too.
- **Changes**: deleted, edited and missing messages in observed chats, grouped into one notification per check (every minute unless changed in Parameters).
- **Completed tasks**: history, exports and storage copies.
- **Daily summary** at the chosen hour, server time.

Notifications carry chat names and counts. Message excerpts are off by default; with them on, message text leaves this machine.

**Your operator bot** is a bot of your own from @BotFather that answers `/status` and `/stats`, and optionally `/pause`, `/resume` and `/copy`. Only the listed chat and Telegram user IDs can use it; conversation text stays in the workspace. Use a separate bot if another application already receives its commands. See [notifications](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md) and [operator bot](https://phishdestroy.github.io/TgWitness/docs/reference/storage/#operator-bot-and-completion-notices).

### Evidence and backups

- **Independent timestamps** send only the SHA-256 of each signed checkpoint to RFC 3161 authorities and OpenTimestamps calendars, every 5 to 1,440 minutes. **Anchor now** runs a pass. See [timestamps](https://phishdestroy.github.io/TgWitness/docs/reference/timestamp/).
- **More witnesses**, each off until chosen: the newest drand round, Telegram's list of signed-in devices without IP addresses, and Cloudflare Gateway's log of the server's DNS queries. See [optional records](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices).
- **Encrypted backup** copies the journal, files, checkpoints and chat exports to S3-compatible storage (Wasabi, Amazon S3, Backblaze B2, Cloudflare R2, MinIO). Everything is encrypted on this machine first. **Download encryption key** and keep it apart: without it the copy cannot be read. Object Lock in Governance or Compliance mode keeps objects from deletion for a set number of days. See [off-site copy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md).

### Code check

Checks whether the installed program matches a published version.

1. Enter a GitHub repository (the official one is filled in) and a tag, branch or commit.
2. **Check now** asks GitHub's API, through this workspace's route for outside requests, for that commit's file list. It compares the git blob ID of every measured program file with the commit. A Windows checkout with converted line endings still matches.
3. The result lists changed, extra and missing files (up to 50 of each) and is saved as a `source.checked` journal record.

The result counts as current only while the running program files are unchanged: check again after an update. No token is needed and only public repositories work; chats and credentials are not uploaded. A match identifies the code on disk. It is not hardware attestation; for that, see [Phala Cloud](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx).

## Protection modes

The switcher next to the version number shows the chosen mode and how many of the 18 protection layers are active, for example `🟠 Witnessed 9/18`. **Change mode** in **Extras → Protection level** opens the choice. A mode describes a target and lists what is still missing; recording, signing and saved settings are the same in every mode.

| Mode | For | Adds |
| --- | --- | --- |
| 🟢 Easy | Watching a chat and keeping a copy | Chats, the journal and chat exports; signing runs in the background |
| 🟡 Signed | Reports to a platform, a host or an abuse desk | Signed archive, journal check, checkpoints, handover extract |
| 🟠 Witnessed | Cases where someone may claim the record was changed | An independent witness posting signed journal heads |
| 🔴 Court-ready | Evidence for a lawyer, the police or a court | Timestamps, an encrypted off-site copy, case details in reports |
| 🟣 GitHub-verified | Records whose software anyone must be able to check | Code check and GitHub Actions capture |
| ⚫ Mossad | High-stakes cases against a well-funded adversary | A sealed 24/7 server, a hidden IP address, all 18 layers |

The layers: every record signed and chained; a signed run receipt; attachments saved with SHA-256; signed checkpoints; rechecks; problem alerts; read-only witness access; a witness checking on schedule; RFC 3161 timestamps; OpenTimestamps proofs; a verified latest timestamp; an encrypted off-site copy; case details in reports; a matching code check; Telegram never seeing this machine's IP; outside requests through a proxy; Object Lock on the copy; a sealed server with provider records. A layer that is off has **Set up**, which opens its form. Choosing a lower mode asks for confirmation and deletes nothing.

## More tools

**Extras → Independent capture**: connect a separate browser or AyuGram recorder, pin its signing key, select capture options, start/pause, take snapshots and download verified signed archives. Each recorder has its own manual login, route, journal and key. Both connections start disabled. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md).

- **Ask the archive**: search saved observations, review the sources, then decide whether to send them to an AI model. See [archive analysis](https://phishdestroy.github.io/TgWitness/docs/reference/analysis/) and [local OCR and transcription](https://phishdestroy.github.io/TgWitness/docs/reference/media-analysis/).
- **Parameters**: limits and pace of collection, rechecks, downloads, profiles, notifications and exports. Search by name, show **Only changed** values and prepare defaults as a draft with **Restore defaults…**. **Save parameters** applies the values from their next use, and each change is a journal record.
- **Access**: separate tokens for reviewers, analysts and operators, limited to chosen workspaces, chats and rights. See [access](https://phishdestroy.github.io/TgWitness/docs/reference/access/).
- **System log**: what this process did since it started (connections, proxy changes, sign-ins, refusals, settings changes) with IP addresses hidden. **Follow new lines** keeps the newest line in view. Messages stay in the journal only.
- **Integrations**: the AI provider, [read-only MCP](https://phishdestroy.github.io/TgWitness/docs/reference/mcp/) connections and [signed webhooks](https://phishdestroy.github.io/TgWitness/docs/reference/webhooks/).
- **Case Board**: private team notes, bookmarks and slices next to the evidence. See [Case Board](https://phishdestroy.github.io/TgWitness/docs/reference/case-board/).
- **GitHub Actions capture** in Exports: one chat captured from your fork. See [sealed capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md).


---

# How collection works

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/collection/

Observation scope, live updates, rechecks, attachments, own actions and what a gap means, record by record.

TgWitness records what a connected Telegram account observes. The journal preserves those observations, their sequence, and the context supplied with them. It does not infer unseen actions from a missing message or from an account being connected.

## From login to a journal

Flow diagram · Authorize a user account → Select accessible groups and channels; Select accessible groups and channels → Save event and attachment settings; Save event and attachment settings → Start observation; Start observation → Receive updates from the active client; Receive updates from the active client → Apply source and event policy; Apply source and event policy → Append a signed observation; Append a signed observation → Review or export the journal; Append a signed observation → Process any queued attachment; Process any queued attachment → Append the download outcome · Authorize a useraccount · Select accessiblegroups and channels · Save event andattachment settings · Start observation · Receive updates fromthe active client · Apply source and eventpolicy · Append a signedobservation · Review or export thejournal · Process any queuedattachment · Append the downloadoutcome

**Diagram as text**

1. Authorize a user account → Select accessible groups and channels
2. Select accessible groups and channels → Save event and attachment settings
3. Save event and attachment settings → Start observation
4. Start observation → Receive updates from the active client
5. Receive updates from the active client → Apply source and event policy
6. Apply source and event policy → Append a signed observation
7. Append a signed observation → Review or export the journal
8. Append a signed observation → Process any queued attachment
9. Process any queued attachment → Append the download outcome

Authorization, access to a source, a running collector, and complete delivery are different questions. A successful login does not grant access to every group. A connected transport does not establish that every relevant update arrived.

## Observation scope: chosen chats, a folder or the whole account

Sources → **Observation scope** decides which chats a workspace records.

| Mode | Records | New chats |
| --- | --- | --- |
| Chosen chats (default) | Only the chats you add by hand | Never added automatically |
| Telegram folder | Chats in one of the account's folders: chats included by name, plus the folder's categories (contacts, non-contacts, groups, channels, bots), minus its excluded chats and, if the folder says so, archived chats | Matching chats are added as soon as they become active; chats you add to the folder in Telegram are picked up within an hour |
| Whole account | Every chat the account sees | Every new chat, group, private chat or bot is added the moment its first update arrives |

- **Source types** (channels, groups, private chats, bots) narrow the folder and whole-account modes. Chosen chats can be of any type, including private chats and bots.
- **Excluded chats** are never recorded, in any mode. In folder and whole-account modes, *Exclude* and *Remove* on a source put it on this list, so the scope does not add it again. Choosing the chat again by hand (in Sources or from Chats) takes it off the list. The list holds up to 5,000 chats; past that, *Remove* is refused and the chat can be paused instead.
- **Own actions** (on by default): messages this account sends, its edits and its reply-keyboard button presses. Turned off, outgoing messages and edits are skipped.
- Switching to a folder or the whole account asks for confirmation: these modes record private chats and messages of third parties and belong on a dedicated account only. The confirmation and every scope change are signed `scope.changed` records.
- Chats added by the scope appear as sources marked *auto*, recorded as `scope.applied` (at start and hourly) or `source.discovered` (a new chat while observing). Switching back to chosen chats pauses every automatically added source.

What these modes cannot do:

- **Secret chats** are end-to-end encrypted between two devices and never reach TgWitness, in any mode.
- **Nothing is recorded while TgWitness is not running.** After a restart it asks Telegram for missed updates and rechecks chats, but Telegram does not return everything after long outages. Reports and `verify.py` show such periods as gaps (see [coverage](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)).
- Only the first 1,000 dialogs are listed at start (the limit is under **Parameters**); older chats are added when they next become active. The earlier history of an added chat is not fetched — take a history snapshot or a full chat export when you need it.
- Folder conditions that change all the time (muted, read) are not applied: such chats stay observed.
- **Inline (callback) bot buttons** pressed in another app are invisible to a second session; the bot's reply or edit is recorded. Reply-keyboard presses arrive as outgoing messages and are labeled `button_press`.
- More chats mean more requests. Telegram restricts accounts for volume it considers excessive, which is one more reason to use dedicated accounts.

## Scope and event selection

Each workspace has its own sources. TgWitness does not join groups, accept invitations, or enumerate every member automatically. Sources must already be accessible to the account. At startup, the collector checks selected sources against the account's visible dialogs; the first 1,000 dialogs are inspected unless **Parameters → Chats read from the account's list** says otherwise. An absent source is marked **access unconfirmed**, not assumed to have removed you.

| Setting | Collects | Effect when disabled |
| --- | --- | --- |
| New messages | Ordinary delivered messages | Later edits/deletions may have no earlier captured text to compare. |
| Edits | Delivered edited message versions | Intermediate changes are not reconstructed later. |
| Deletions | Scoped deletion notices and unscoped account-level notices | Deletion notices are not added to the journal. |
| Reactions | Delivered reaction snapshots | Separate reaction updates are not added. |
| Membership | Delivered membership service messages and participant updates | Those membership observations are not added. |

Settings apply to all selected sources in the workspace. Save the form to apply changes; changes are recorded with signed before/after values. Disabling a category does not remove earlier records. Re-enabling it does not backfill missed updates.

Operational records and other group service events remain separate from these switches. Membership service messages can create message records when membership is enabled even if ordinary new-message capture is disabled. Captured Telegram objects retain embedded metadata; a switch is not a redaction rule.

**Deletions in private chats and ordinary groups** arrive as message IDs without a chat. These chats share one account-wide message ID sequence, so when a message with that ID was saved earlier, its chat is known: the deletion is recorded in that chat with `chat_resolution` explaining how. IDs never saved stay an **unscoped deletion** with an explicit unknown source; the collector does not guess. Telegram never says who deleted a message; when the deleted message was sent by this account, the record says so (`deleted_message_was_outgoing`) without naming a deleter.

## Own actions

Messages sent by the observed account are labeled `outgoing`. An edit of an outgoing message notes that in private chats and groups only its author can edit it, while channel posts can be edited by other admins. When an outgoing message repeats the text of a button from the newest saved reply keyboard in that chat, it carries `button_press` with a link to the keyboard's record.

Excluding own actions also applies to background rechecks and automatic new-chat history. Skipped outgoing messages advance the recheck position so they cannot block later incoming messages. Explicit panel actions and manually requested history snapshots remain recorded.

## Investigation mode: joining teams and talking to bots

**Sources → Observation scope → Investigation mode** prepares the scope for a dedicated account that joins team chats, starts bots and writes to them: the whole account, every source type, own actions, and for every chat or bot that appears its profile and its latest 200 visible messages. Review the form and press **Save scope**; the switch to the whole account asks for the usual confirmation.

- **Buttons.** Buttons under a message are kept with it and shown in **Chats**: links, web apps, login links, texts to copy, callback data, inline queries, requests for a phone number or location. Links are shown as text and never opened by the panel. When a bot changes only the buttons (a new payment link), that is a new version of the message, both from live updates and from rechecks.
- **New chats and bots.** In folder and whole-account modes, **When a new chat or bot appears** saves, right after it appears:

  - its profile as a `source.profile` record: bot description and commands, the about text of a user, group or channel, members, linked chat and invite link when Telegram returns one;
  - its latest visible messages (up to 1,000) as a history snapshot marked `new_chat`: the earlier messages of a team chat just joined, or what a bot said before observation noticed the chat. Messages already saved live are not repeated.

  Chats already in the list when the mode is switched on are added without snapshots. A FloodWait pauses this work and it resumes afterwards; failures are recorded and live recording of the chat continues. - **Profiles on request.** **Chats → Profile → Save profile now** saves the current profile of any source; the newest one is shown above the messages. - **Not visible.** Inline (callback) buttons pressed in another Telegram app, the popup or link a bot answers such a press with, and invite links used in another app do not reach TgWitness. What the bot sends or edits afterwards is recorded.

### Act from the panel

**Chats** now includes a mini-client using the selected workspace's Telegram account:

- Write a plain-text message or choose **Reply** under a saved message. The returned outgoing message is recorded even when the scope excludes outgoing updates.
- Press **Press button** under a current callback or text button. The server fetches the message again and refuses the action if the keyboard differs from the saved version. Callback receipts retain Telegram's popup text, alert flag and URL; the answer is also shown below the conversation. URLs remain selectable text and are not opened automatically.
- Expand **Open Telegram link**, enter `@username`, a public `https://t.me/name` link, `https://t.me/+invite` / `joinchat/invite`, or a bot link with `?start=parameter`, and press **Save preview**. The original link and Telegram's preview are signed before joining. **Join / open and observe** then joins the group/channel or opens the user/bot, adds the chat as an enabled source, and sends `/start` to a bot, including its start parameter. A join request awaiting administrator approval is recorded as pending, not as membership.

Turn on **Start observation** to capture incoming replies live. Panel actions work while observation is paused, but only their direct responses are then guaranteed to be saved. Newly added sources use the configured profile/history intake when observation is running. When a source is paused, enable it in **Sources** before sending or pressing its buttons.

`interaction.preview`, `interaction.requested` and `interaction.result` are ordinary signed journal events included in evidence exports. Requests identify the account, message/button or preview record and whether observation was running. Receipts distinguish success, rejection, approval pending and an unknown outcome. An interrupted request may have reached Telegram: check the chat before starting a new action. Reusing a request ID retrieves its saved receipt without repeating the action, including after restart. The panel retains the ID after an ambiguous response for the same action during the current page session. It also retains that ID when refreshing the view fails after a successful action: the receipt stays visible, and clicking again retrieves it. Callback and join RPCs have one application attempt; retryable reads keep their configured retry policy. Switching chats immediately clears the draft and reply target and disables sending until the new conversation loads.

This mini-client handles text and callback buttons. Web apps, login/phone/location requests, payments, inline queries and attachments still require a Telegram client; their saved button metadata remains visible. The new controls use English text.

## Recheck tiers

Rechecks ask Telegram again for missed messages, edits and messages it no longer returns. Sources marked with a star are **priority** sources, rechecked every 15 minutes by default; all other sources every 6 hours. Chosen chats start as priority sources, chats added by a folder or the whole account as regular ones. At most 30 sources are rechecked per pass and the rest wait for the next minute; after a reconnect, priority sources go first. Both intervals are set under Sources → Recording settings → Recheck (0 turns a tier off) and are recorded as `recheck.changed`.

Missed messages are fetched upward from where the previous pass stopped, at most **Parameters → Missed messages recovered per chat and pass** (1,000 by default). After a long stop the recheck therefore fills the whole gap, even when live messages newer than the gap were saved first. A chat that is still catching up is rechecked again on the next minute instead of waiting for its tier interval; `recheck.completed` shows `continues_after` until it is done.

Comparisons include message text, entities, keyboards (including removal), and attachment content/identity. Changing file access hashes or file references alone does not create an edit, nor does what Telegram fills in on its own: a link preview loading, story views, paid media unlocked by this account, an invoice's receipt. Each saved version in Chats links to its full journal record, including media metadata.

## Message history and attribution

Suppose the collector observes “Meeting at 10:00,” later sees “Meeting at 11:00,” and then receives a deletion notice. It appends three distinct observations. The original text remains, the edit is a separate version, and the notice records that a deletion was observed.

If collection began after the first version disappeared, that text is unavailable. If several edits occurred while the process was offline, only subsequently observed versions can be saved. A deletion notice cannot recover content never captured.

The message sender is not automatically the editor. Telegram usually does not supply the person who deleted a message or the exact deletion time. Unknown actors stay unknown. Reaction snapshots and participant updates contain only the counts and identities Telegram makes visible to the account.

Sequence numbers express observation order. The collector's UTC timestamp is its local clock; a Telegram source timestamp is stored separately when supplied. Neither is an independent trusted timestamp.

## History snapshots

A snapshot requests the latest visible messages from an enabled source, up to 500 per request. Results are labeled as history observations. They can overlap with live capture, and repeated observations are kept as separate records.

Snapshots follow the attachment policy but remain separate from live-event switches. They do not reconstruct deleted messages or missed intermediate versions. You can request one while paused; any attachments it queues wait until observation starts and the download worker runs.

## Attachment handling

Attachment download is on by default and pauses below 1 GiB of free disk. The collector commits the message observation and download job together. The job retains the original media descriptor and size policy, so a later edited attachment is not silently substituted.

Downloads run after message capture. A completed download creates a `media.saved` record with its SHA-256 and byte count. Skipped, failed, retried, and interrupted work has separate outcomes. A queued job is not proof that the file was preserved. The completed file must also match the byte count in the original observed attachment descriptor. A short or unexpectedly long response is not recorded as preserved media.

Limits are set **per type**: photos, videos, GIFs and animations, round video messages, voice messages, music and audio, stickers, and files. Each type can be turned off and has its own size limit from 1 to 2,000 MiB; new workspaces start with 20 MiB for photos, 100 MiB for videos, 50 MiB for files, audio and round videos, 20 MiB for voice and GIFs and 5 MiB for stickers. New workspaces leave GIFs and stickers off until turned on. Workspaces with policies saved before per-type limits keep all types enabled and retain their single limit for every type. *Maximum file size* sets every type at once. A type turned off produces a `media.skipped` record; unknown-size or oversized files are not downloaded. Large files get extra download time based on their size and a baseline speed of 256 KiB/s. Jobs survive restart, but expired references, lost access, or deleted files can still prevent recovery. Waiting jobs keep the limit saved with them, so a raised limit applies to new files only. Turning a type off or lowering its limit also skips the waiting files it excludes, each with a `media.skipped` record; turning downloads off pauses the queue until they are turned on again.

## Pause, lock, disconnect, and restart

| Action or condition | Effect |
| --- | --- |
| Switch workspace | Changes the panel view; other collectors keep their state. |
| Lock the panel or close a tab | Leaves the server and observation running. |
| Pause observation | Stops that collector and preserves queued attachment work. |
| Disable a source | Stops future scoped capture; queued media jobs for it wait while it is disabled. |
| Remove a source | Forgets it as a source and deletes its people profiles; records already saved stay in the append-only journal. Its attachments still waiting are recorded as failed (`source_removed`). In folder and whole-account modes it is also excluded. |
| Change the connection route | Requires a pause, closes old clients, and cancels unfinished login. |
| Stop the Python process | Stops all workspaces; no observations are made while it is offline. |
| Restart after active observation | Attempts to resume the saved scope using the saved session. A manual pause clears that intent. |

The collector records detected disconnects, retries, errors, starts/stops, and heartbeats. Short interruptions can be missed by periodic connectivity checks. After a restart, missed updates are requested from the saved update position and observed chats are rechecked periodically; see [evidence format](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#durable-collection-and-process-receipts-02). A snapshot provides context; it does not prove that a gap was repaired.

## Account isolation and verification

Each workspace has its own journal, authorization, signing key, policy, and queue. Only its active client can contribute live observations. Rejected, pending, superseded, and connection-test clients cannot write live updates into its journal. Different accounts can observe the same group, but their journals remain separate.

Each event includes the previous hash and an Ed25519 signature. Exports cover the whole workspace journal through a fixed sequence number. Panel filters do not filter the export; collection may continue beyond its boundary while it is being prepared.

**Verify journal** checks the event chain and signatures through the displayed boundary. Its result is cleared when the workspace changes, and the panel identifies new records added after the check. ZIP export also verifies collected media.

A valid signature establishes integrity relative to the trusted key, not Telegram origin or truthful content. Retain fingerprints and checkpoints independently. See the [evidence model](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/), [daily operations](https://phishdestroy.github.io/TgWitness/docs/reference/operations/), and [live acceptance procedure](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for trust and delivery requirements.


---

# Load source history

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/history/

Load past messages from enabled sources, pause and resume, and verify a signed progress report.

In **Sources**, review the enabled chats, start observation, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run.

## Pause, restart and partial results

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Restart observation first. Resuming requires the same Telegram account.
- The message observation, attachment job and cursor commit in one transaction. A resumed run does not repeat its already committed observations. Live capture or a separate, explicitly started run may independently observe the same message.
- Each source fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Inaccessible sources and sources disabled during acquisition remain visible as failed or skipped. Other sources continue; the overall result is incomplete.
- FloodWait delays respect the saved account backoff. Transport timeouts and low disk space pause the run with its cursor intact. Resume after resolving the cause.
- **End this history run** preserves saved observations. It does not remove them or cancel already queued attachment downloads. A new run reads enabled sources anew.

History completion describes history reads only. Attachments may remain pending, fail, or be excluded by the configured policy. Check media receipts in the journal and the attachment queue; only a completed receipt with preserved bytes constitutes a saved attachment. The history operation is an explicit snapshot request and is separate from switches that select categories of future live events.

## Transfer and verify

Save the **signed progress report**, then use **Export evidence** to download the journal and saved attachments. A later evidence export may include additional records; the report binds its counters to the journal prefix at the time it was created. Run the verifier from a trusted checkout of this version:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. Without `--evidence`, it checks only the signed report and its internal consistency. Progress phases, titles, cursors and attachment summaries are signed collector statements, not independently reconstructed by this report checker. The evidence verifier still checks the archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages, unseen intermediate edits and Secret Chats are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

The acquisition cursor is local workspace state. Restoring an evidence ZIP alone does not restore a pending acquisition job or Telegram session. Keep the workspace backup if continuation of the original job is required.


---

# Workflows and operations

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/operations/

Daily operation of the panel: modes, monitoring categories, parameters, notifications, exports, backup and capacity.

For your first connection, use [accounts and session formats](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/). For an explanation of saved versions, event policies, and gaps, see [how collection works](https://phishdestroy.github.io/TgWitness/docs/reference/collection/). This guide covers daily operation and recovery.

A managed installation includes **START-HERE.html** and **START-HERE.txt** beside its launcher, with the repository link and commands tailored to its installation path. Run `tgwitness guide --print` over SSH, or `tgwitness paths` to locate the actual data directory. A root systemd install stores private state under `/var/lib/tgwitness-…`; `/opt/tgwitness` holds the program.

For a managed temporary Cloudflare tunnel, `tgwitness tunnel off` closes public access while the local panel and collection keep running. `tgwitness tunnel on` enables it; `tgwitness tunnel restart` creates a new tunnel connection. Use `tgwitness open` to see its current address. An explicit off setting survives service restarts. `tgwitness stop` stops both the panel and collection.

## Operator workflow

Flow diagram · Choose storage and key protection → Open the panel with its token; Open the panel with its token → Select a workspace; Select a workspace → Configure Direct or proxy route; Configure Direct or proxy route → Enter phone or choose files / QR; Enter phone or choose files / QR → Check account identity and select accessible groups; Check account identity and select accessible groups → Save event and attachment policies, then start observation; Save event and attachment policies, then start observation → Monitor errors, access, queues and disk; Monitor errors, access, queues and disk → Retain independent checkpoints; Retain independent checkpoints → Export and verify material · Choose storage and keyprotection · Open the panel withits token · Select a workspace · Configure Direct orproxy route · Enter phone or choosefiles / QR · Check account identityand select accessiblegroups · Save event andattachment policies,then start observation · Monitor errors,access, queues anddisk · Retain independentcheckpoints · Export and verifymaterial

**Diagram as text**

1. Choose storage and key protection → Open the panel with its token
2. Open the panel with its token → Select a workspace
3. Select a workspace → Configure Direct or proxy route
4. Configure Direct or proxy route → Enter phone or choose files / QR
5. Enter phone or choose files / QR → Check account identity and select accessible groups
6. Check account identity and select accessible groups → Save event and attachment policies, then start observation
7. Save event and attachment policies, then start observation → Monitor errors, access, queues and disk
8. Monitor errors, access, queues and disk → Retain independent checkpoints
9. Retain independent checkpoints → Export and verify material

Authorization, transport connectivity, access to a group and completeness of delivery are different properties. A green connection status does not imply all events have been captured.

## Share work without sharing the main key

Open **Access** to give a reviewer or analyst their own token. Choose the accounts and chats they can open, then allow viewing, export or operational actions. An operator who starts/stops collection needs whole-workspace access; a reviewer can be limited to a single chat. Session limits, expiry and IP rules are separate from Telegram account authorization. See [access and permissions](https://phishdestroy.github.io/TgWitness/docs/reference/access/).

Use **Open sessions** to end a connection or revoke the access to end all of its sessions. The administrator console combines current-process activity across workspaces. Session closure leaves collection running.

## Runtime modes

| Mode | Action | Behavior |
| --- | --- | --- |
| Demo | scripts\Demo.cmd or `--demo` | Synthetic data; real account connections disabled |
| Observation | Start observation | Record delivered updates for selected sources |
| History snapshot | Sources → history snapshot | Up to 500 current messages; no reconstruction of all past changes |
| Pause | Pause observation | Stop collection while retaining data and queued jobs |
| Review/handoff | Exports | ZIP, JSONL/CSV/HTML, checkpoint, process receipt and timestamp request |
| Multiple accounts | Workspaces or the top **+** button | Any number of separate workspaces in one process |

Local demo access opens automatically without manual token entry. It uses a process-lifetime capability valid only for direct loopback access to an isolated synthetic demo; the main panel token is not disclosed. Real workspaces and remote or proxied demo access retain token authentication. Demo entry grants no Telegram authorization.

## Monitoring categories

![Per-account monitoring settings with synthetic source data](https://phishdestroy.github.io/TgWitness/assets/sources.png)

In **Sources → Recording → Choose which changes to preserve**, select new messages, edits, deletion notices, reaction updates and membership events independently. The default retains all categories. **Messages, edits & deletions** keeps the original context while disabling separate reaction/member updates. **All visible activity** restores all five. Presets change the form; press **Save recording settings** to apply.

The saved policy applies to all selected sources in that workspace. Other workspaces retain their own settings. Each actual change records signed before/after values; the current policy is also included in process receipts and observation start records. Disabling a category does not delete earlier observations. Re-enabling does not retrieve missed changes. There is no per-group category override in this version.

Keep new messages enabled when prior content matters: a deletion notice cannot recover text that was never captured. Operational/coverage records and other group service events are always retained. Explicit history snapshots are separate from live-category selection and may include service messages. These switches do not redact reaction/member metadata embedded in an otherwise captured Telegram object.

A history snapshot may queue attachments while paused. Start observation to process them. Queued does not mean downloaded. An unavailable original file is not replaced with a newer edited version; outcomes are recorded separately.

**Lock** clears browser access and secret fields but leaves collection running. Closing a tab also leaves the process running. Stopping the Python process or service stops collection regardless of the browser state.

Deleting an additional workspace stops its collector and removes its local data. If a locked file or filesystem error interrupts removal, the panel reports the failure and keeps the workspace listed as unavailable (`DeletionPending`). Close programs holding its files and retry **Delete**. Restarting TgWitness leaves that workspace stopped and does not recreate its partially removed journal or keys. A successful deletion is recorded only after the directory has been removed; separately exported or backed-up copies remain under their own retention policy.

## Notifications

Open **Extras → Notifications → Configure**. TgWitness uses Apprise to send alerts to Matrix, Telegram, Discord, Slack, ntfy, email and other supported services. You can add several destinations to one workspace.

1. Enter one Apprise destination URL per line. Use the [service catalogue and URL formats](https://appriseit.com/services/) for your service.
2. Turn on **Send notifications**, then choose problem alerts, changes in observed chats and a daily summary. The summary hour uses the server's time.
3. Turn on **Include short excerpts** if you want saved text from deleted and edited messages in the alerts.
4. Press **Save notifications**, then **Send test** to check delivery.

For your own receiver, use Apprise's [JSON webhook](https://appriseit.com/services/json/). For example, `jsons://notify.example.org/tgwitness` sends JSON over HTTPS to that endpoint. This is a fictional example; replace it with your own destination.

Destinations and settings belong to the selected workspace. Change notifications cover its observed sources, including newly added chats. The bell in the top bar also lists recent problems and chat changes.

In the demo, the notification controls are visible but sending is disabled. Configure delivery in a real workspace. Notifications use that workspace's Direct, SOCKS5 or HTTP route; MTProxy cannot carry them. Non-HTTP destinations such as SMTP require a direct route.

## Panel layout

![Connection workspace using synthetic data](https://phishdestroy.github.io/TgWitness/assets/connection.png)

**Journal** shows observations, search and filters. An edit opens captured versions; a deletion opens prior content if available. Unknown attribution remains explicit. Counts are available under **Overview**; acquisition details stay in the local guide.

Open an edited message to compare its versions with **Inline diff** or **Side by side**; **Raw** shows the saved fields. Changes to hidden links and bot buttons appear separately. Open an attachment preview to inspect saved images, audio or video; the download button keeps the preserved original available.

**Live** updates the journal and chats as records arrive. Pause it while reviewing, or use the new-events button when ready; collection keeps running. **Ctrl/Cmd+K** finds panel actions and searches the journal.

**Sources** contains the observation scope (chosen chats, a Telegram folder or the whole account), accessible chats of every type, selected sources with priority stars, attachment and recheck settings and history snapshots. Private sources are selected by dialog/ID without a public link. Access status describes the most recent check, not permanent permissions.

Filter sources, select their checkboxes, then enable, pause or mark them as priority together. In the available-chat list, **Add selected** uses your selection; **Add all matching** uses the current search and type filter.

**Chats → People** lists everyone with saved messages; with people profiles switched on for the chat, a click opens that person's profile with links to the journal records.

**Witness** creates read-only witness tokens, shows when each witness last checked and gives the commands and options to run one ([independent witness](https://phishdestroy.github.io/TgWitness/docs/reference/witness/)).

**Parameters** holds every limit and pace of the workspace that is not on another page: how many dialogs are read, how often the chat list is re-read, heartbeat and checkpoint intervals, the startup buffer, how rechecks spread their requests (first delay, chats per pass, pause between chats, messages recovered and re-requested), disk reserve, timeouts and retries of downloads, what people profiles look for (including your own regular expressions), size and pace of notifications, snapshot, ZIP and browser-download limits, and Telegram client timeouts and retries. Each field shows its range and default; changed fields are marked and can be restored one by one or all together. Every change is recorded as `parameters.changed` with the values before and after, and observation start records name the values in force. Values apply from their next use; client timeouts and retries from the next connection. Recheck intervals, attachment types and sizes, evidence and off-site copy intervals stay on their own pages and take any value in their range, not only presets.

The bell in the top bar lists recent problems and changes in observed chats; unread ones are counted until marked as read. Changes are grouped per chat and hour ("12 deleted, 1 edited, 0 not found"), and problems such as a sign-out or a full disk stay in the list however busy the chats are.

**Account** starts on the phone-number field. **Continue** leads directly to code entry, asking for API credentials only when missing. QR and file import are alternative tabs. Saved API credentials are reused only within their own workspace. The entry screen has no sidebar, statistics, or setup paragraphs. The **Settings** icon opens API, proxy, storage, and additional-account controls. New installations start here; connected accounts with no selected sources start on **Choose chats**. Changing the route requires paused observation and cancels unfinished login. An existing journal cannot be silently rebound to a different Telegram account.

**Exports** checks journal integrity and produces portable files. Its workspace ID can be passed to the download CLI. Every export pins a full journal prefix; later events enter a subsequent export. Search filters do not change the package scope. Detailed signing and coverage information is under **Verification & limitations**.

The panel reports collector state, queued/failed media, oldest pending media, free disk, request pauses and sources whose access is unconfirmed under **Collector health**. These details are collapsed initially and hidden on Account. A setup card shows the next step: connect an account, choose sources, or start observation. The account list is a load-time snapshot; the selected workspace refreshes periodically. This is not a multi-process SLA monitor.

The UI uses local assets and text rendering for source content. Desktop and narrow Chromium layouts are tested. This is not a complete accessibility certification; screen-reader and human usability evaluation remain separate work.

## Deployment environments

| Environment | Installation | Verification status |
| --- | --- | --- |
| Windows PC/server | Python 3.11+, scripts\Setup.cmd/Start.cmd, private data directory | Locally checked on Windows/Python 3.12 |
| Linux server/VPS | Python venv, dedicated service user, HTTPS/SSH | Code, CI and systemd example provided; not executed on this host |
| macOS | Python venv, foreground process or user agent | launchd example provided; separate installation check needed |
| Docker/Compose | Persistent volume, one worker | Definition and CI runtime check provided; Docker unavailable locally |
| Phone browser | Connect to the protected panel on a running server | Narrow Chromium layout tested; collector does not run on iOS/Android |

Portability means no mandatory cloud service or frontend build. Each target still needs compatible Python/crypto dependencies, local disk and network access. See [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/docs/reference/deployment/) and [service templates](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md).

Workspaces share CPU, memory and an event loop. For process isolation, use distinct instances, ports, data directories and account authorizations. There is no unified panel across separate instances. Never point several workers at one database.

## Startup checks and exports

Run `python start.py --check` before starting a prepared environment. Add `--json` for machine-readable checks or pass the intended `--data-dir`, `--host` and `--port`. The command checks prerequisites without Telegram login or creating a journal. It does not verify a journal or prove capture readiness; journal verification runs during application startup. An occupied port may simply be an existing instance.

Browsers supporting the File System Access API save exports through a writable stream. Other browsers buffer at most 128 MiB. Use the streaming CLI for larger exports or browsers without file streaming:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Add `--profile ID` from Exports for a child workspace. Use `--url https://server` for remote access. Plain HTTP is accepted only for loopback destinations. The token is read from a file and sent in a header, not printed or put in a URL. Redirects are refused. Existing destinations are not overwritten. Failed transfers remove their temporary part file. The reported SHA-256 is a transfer checksum; verify the signed ZIP separately with a trusted fingerprint/checkpoint.

## Backup, restore and interruptions

1. Pause observation and stop the process cleanly.
2. Copy the entire data directory: databases, WAL/SHM if present, media, `credentials.enc`, `signing.enc`, `network.enc`, vault keys/metadata, token, checkpoints and every `profiles/` directory.
3. For external-key mode, separately preserve the master key and retain each `vault.external.json`. Generating a new key cannot recover the old secrets.
4. Restore while the destination is stopped; configure the original key, restrict access, and verify integrity before resuming.
5. Record downtime and verification results. A history snapshot cannot prove that no deletions happened during the interruption.

Evidence ZIPs exclude sessions/private keys and are not full service backups. Four things are protected differently:

| What | Protection |
| --- | --- |
| Export files without a password (the default) | Not encrypted. Signed, so changes are detectable, but anyone holding the file can read it |
| Export files with a password | If you set a password, the finished export goes unchanged into a WinZip AES-256 ZIP that 7-Zip and WinRAR open; the password is not stored ([evidence handling](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/)) |
| The journal database and saved attachments on disk | Not encrypted by TgWitness; use an encrypted disk or volume |
| Telegram sessions and signing keys | Encrypted in the data directory (`credentials.enc`, `signing.enc`, `network.enc`) |

A full service backup is the stopped data directory described above, not an export. Use protected storage and a deliberate transfer mechanism for both. Temporary server exports live in each workspace's `temporary-exports/`; completed responses are cleaned up, and interrupted export files are removed on the next startup while that workspace's instance lock is held.

A connection-restored event does not guarantee recovery of intermediate changes. Persistent media jobs and the Telegram update position survive restart; see [evidence format](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#durable-collection-and-process-receipts-02).

## Capacity and retention

Default limits, all changeable under **Parameters**: the first 1,000 dialogs, 500 messages per snapshot, 4 GiB uncompressed signed ZIP content (larger archives need `verify.py --max-gib N`) and a 128 MiB browser fallback. Attachments take 1–2,000 MiB per type under **Sources → Attachments**. The download CLI defaults to 5 GiB transferred. Available disk can be a lower limit. Reserve space for journals, media, WAL, temporary exports and backups. Exports use the data volume rather than Compose's 512 MiB `/tmp`.

Measure events/second, queue age, media bytes and disk latency rather than counting groups alone. Synthetic local benchmarks do not guarantee Telegram delivery. There is no automatic retention deletion. Removing a journal tail invalidates its relationship to retained checkpoints.

Priority rechecks already exist: starred sources are rechecked every 15 minutes by default, others every 6 hours (see [recheck tiers](https://phishdestroy.github.io/TgWitness/docs/reference/collection/#recheck-tiers)). Password-protected exports exist as described above. Live Telegram/proxy acceptance, durable replay, admin-log and reaction polling, isolated workers, encryption of the local journal and media by TgWitness itself and independent review remain separate work. Scoped access is documented in [access and permissions](https://phishdestroy.github.io/TgWitness/docs/reference/access/). See [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md), [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) and [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/docs/reference/verification/).


---

# Investigation mode

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/investigation/

Whole-account investigations across channels, groups, private chats and bots, from scope to a verified case package.

Follow a case across channels, groups, private chats and bots, from initial acquisition to a cited timeline and verifiable handoff. The interactive website version is at `/docs/cases/`; [preview instructions](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

## Worked case: a destination changes across four conversations

An announcement points to a bot. An operations group discusses a new payment destination, and the bot's keyboard displays it. The announcement is edited, a private follow-up repeats the destination, and a group message disappears.

The questions are: what was observed before and after the change, which Telegram accounts posted each item, where the destination appeared, which attachment bytes were preserved, and what intervals remain unknown?

All names, IDs, times and journal references in this example are fictional. The workflow uses current features; the case map is an illustration, not an automatic graph generated by the application.

Flow diagram · Channels → Workspace journal; Groups → Workspace journal; Private chats → Workspace journal; Bots → Workspace journal; Workspace journal → Search all sources; Workspace journal → People profiles with record references; Workspace journal → Saved versions and attachment receipts; Search all sources → Analyst timeline and source register; People profiles with record references → Analyst timeline and source register; Saved versions and attachment receipts → Analyst timeline and source register; Workspace journal → Signed evidence ZIP; Analyst timeline and source register → Case handoff with separately verified artifacts; Signed evidence ZIP → Case handoff with separately verified artifacts · Channels · Groups · Private chats · Bots · Workspace journal · Search all sources · People profiles withrecord references · Saved versions andattachment receipts · Signed evidence ZIP · Analyst timeline andsource register · Case handoff withseparately verifiedartifacts

**Diagram as text**

1. Channels → Workspace journal
2. Groups → Workspace journal
3. Private chats → Workspace journal
4. Bots → Workspace journal
5. Workspace journal → Search all sources
6. Workspace journal → People profiles with record references
7. Workspace journal → Saved versions and attachment receipts
8. Search all sources → Analyst timeline and source register
9. People profiles with record references → Analyst timeline and source register
10. Saved versions and attachment receipts → Analyst timeline and source register
11. Workspace journal → Signed evidence ZIP
12. Analyst timeline and source register → Case handoff with separately verified artifacts
13. Signed evidence ZIP → Case handoff with separately verified artifacts

## 1. Define the case and collect the whole account

1. Connect the collecting account in its own workspace. In [Case Board](https://phishdestroy.github.io/TgWitness/docs/reference/case-board/) or your case register, record the case reference, account ID, workspace and observation start. Retain the trusted signing-key fingerprint independently.
2. For a dedicated collecting account, open **Sources → Observation scope → Investigation mode**. The preset selects **Whole account**, channels/groups/private chats/bots, own actions, source profiles and the latest 200 visible messages for newly discovered sources. Review it, press **Save scope**, and complete the scope confirmation. Main accounts use selected chats or a folder; whole-account collection is available to accounts marked for investigation.
3. **Load chats** and compare the sources with the account's dialog list. Check exclusions. **Parameters → Chats read from the account's list** defaults to 1,000 and allows up to 20,000. Sources beyond the list limit are added when they become active. Record what was actually enumerated.
4. In **Recording settings**, select **All visible activity** and save the monitoring settings. Review attachment types/limits and free disk space.
5. Start observation. Validate a controlled new message, edit and deletion, then retain the test references and any failures.

Whole-account scope records account-visible activity within the saved settings. It does not access secret chats or automatically join every linked group. It also does not backfill every existing conversation. See [collection scope](https://phishdestroy.github.io/TgWitness/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account).

## 2. Inventory every source and acquire historical context

Keep a source register with one row per chat:

| Field | Record |
| --- | --- |
| Identity | Workspace, account ID, numeric chat ID, title and type |
| Visibility | Membership/role, access confirmed or unconfirmed, exclusions |
| Live capture | Start time, selected event types and later policy changes |
| Journal history | Snapshot requested/completed, limit, time and record references |
| Full history | Signed per-chat export filename, boundary and completion/failure |
| Attachments | Completed media receipts, hashes, sizes and skipped/failed outcomes |
| Coverage | Outages, incomplete intake, FloodWait, unavailable messages and other gaps |

Use the right acquisition for each source:

- **Load full history** in **Sources** loads available past messages from enabled sources into the workspace journal. It supports pause/resume and a signed progress report. See [history acquisition](https://phishdestroy.github.io/TgWitness/docs/reference/history/).
- **History snapshot** saves recent visible messages into the observation journal. Its default maximum is 500; **Parameters → Largest history snapshot** can raise that to 10,000. These are current history observations, not reconstructed edits.
- **Full chat export → Export full chat**, or **Chats → Export chat**, fetches the currently visible history of one chat into a separate signed `chat.json` / `chat.html` bundle. Repeat for the case's sources and retain each result.
- **When a new chat or bot appears** can save its profile and up to 1,000 recent messages; Investigation mode selects 200. Existing chats do not receive that intake retroactively when the mode is enabled.
- **Download visible attachments** preserves bytes under the configured policy. Require a completed `media.saved` receipt with SHA-256 and byte count. A queued job, thumbnail or filename is not the preserved attachment.

A full chat export does **not** populate the journal or people profiles with all its messages. Use **Load full history** or bounded journal snapshots for history you need to analyze inside TgWitness. Review the enabled source list before starting a history run. Neither route recovers material Telegram no longer returns.

## 3. Preserve the evolving case and deliberate interactions

Star active case chats as priority sources. Review recheck intervals, continued catch-up and media outcomes. Keep the collector observing while using the account. Use **Chats → Profile → Save profile now** to retain source metadata such as descriptions and bot commands. This is separate from people profiles derived from saved messages.

Where the case involves following a source or interacting with a bot:

1. **Open Telegram link → Save preview** records the supplied link and returned preview before an action.
2. **Join / open and observe** performs the join/open, and sends a bot's start parameter when supplied. A join request awaiting approval is recorded as pending.
3. Panel-issued text replies and supported button presses retain `interaction.requested` and `interaction.result`. Callback receipts can retain returned popup text, alert state and URL.

Those are real account actions. Callback presses in another Telegram app are not visible to the collector, although resulting messages or edits may be. The mini-client does not perform web-app, payment, phone or location workflows. For exact behavior, see [panel interactions](https://phishdestroy.github.io/TgWitness/docs/reference/collection/#act-from-the-panel).

## 4. Connect observations across chats

In **Journal**, select **All sources** and search recorded content. Open matching records and retain the workspace, chat, message ID, sequence and record hash.

In a relevant chat, open **People → Turn on profiles** and inspect a person:

- Names/usernames observed over time and the numeric Telegram ID.
- Reply relationships with source-record references.
- **Also in…** other chats in this workspace journal where that ID wrote.
- Activity, edits/deletions and mentioned wallets, phones, usernames and links.
- Saved avatar metadata and similar cached avatars, with their separate origin.

Open the cited records before using a derived profile in a finding. Profiles cover people with saved messages, not every member of the group. **Parameters → Records cited per fact** limits the reference list, not the underlying activity count. Mentions and avatar similarity are leads; they do not establish ownership or identity.

In the worked example:

| Link | Records | Supported observation |
| --- | --- | --- |
| Same sender account | Group #146 and private follow-up #205 | Both supply Telegram sender ID 71001 |
| Same destination | #146, bot keyboard #173, channel edit #188, private message #205 | All contain `pay.example.invalid/new`; ownership/control is not established |
| Same saved file | Completed media receipts #151 and #209 | The full SHA-256 values agree for the preserved bytes |
| Channel attribution | #101 and #188 | Do not attribute a channel post to user 71001 without an attributed sender |

Compare attachment hashes and their associated message references. Identical files do not establish a creator, forwarder or common operator. Equal names and similar avatars alone do not join two Telegram IDs into one person.

Keep the team's working notes on [Case Board](https://phishdestroy.github.io/TgWitness/docs/reference/case-board/): bookmark the records you rely on, such as #146, #188 and #205, highlight the exact destination string, and save a slice of every recorded action between two records or in a time range. Notes and statuses retain the team's review in their own signed history, separately identifiable from the source observations.

## 5. Build the cross-chat timeline

Use saved versions in **Chats** and their **Journal record #…** links. In **Journal**, combine **All sources** with **Edits**, **Deletions** and **Coverage**. Keep both `source_at`, where supplied, and `observed_at`.

| Illustrative observation time | Reference | Observation |
| --- | --- | --- |
| 09:00 | Channel #101 | Original destination captured |
| 09:12 | Group #146; media #151 | New destination posted; file download completed |
| 09:16 | Bot #173 | Keyboard points to the new destination |
| 09:20 | Channel #188 | Announcement edited; both saved versions remain |
| 09:24 | Private #205; media #209 | Same sender ID repeats destination; same file bytes preserved |
| 09:28 | Group #231 | Deletion notice received; deleter and exact deletion time unknown |

Other records occur between these example references. Sequence numbers order observations; history snapshots can contain older source dates and arrive later than live events. Distinguish snapshots, recovered messages, deletion notices and missing-on-recheck outcomes. Mark coverage gaps as unknown intervals. Later history acquisition does not retroactively establish uninterrupted observation.

## 6. Add account perspectives without losing their origin

Use a separate workspace for every distinct account and repeat its inventory. Keep account ID, role, signing-key fingerprint and source references with every comparison. Message numbers are not global identifiers across chats/accounts.

Case Board keeps source-linked notes and collections within each workspace. The group screen reviews account status together and can bundle separate workspace exports. Correlate those sources in your case notes or analysis tools; each journal retains its own origin and signing key. A global search or merged cross-workspace timeline is not generated. Multi-account export of one channel/supergroup acquires that chat's history using the eligible accounts.

For longer work, retain boundaries with an [independent witness](https://phishdestroy.github.io/TgWitness/docs/reference/witness/). Use controlled delivery checks to qualify each account's capture path and visibility.

## 7. Assemble and verify the case handoff

Keep these together in an analyst-assembled case directory:

| Material | Purpose |
| --- | --- |
| Case notes and source register | Question, collection policy, access/role, findings, alternate explanations and gaps |
| Timeline | Both times and workspace/chat/message/sequence references for each entry |
| Case Board export and slices, if used | Source-linked bookmarks, quotes, team notes, collections, revision history and selected records checked against the evidence ZIP |
| Signed evidence ZIP per workspace | Complete recorded journal, manifest and included preserved media; panel filters do not narrow the journal export |
| Separately signed people-profile files | Derived references checked against the matching workspace evidence |
| Signed full chat exports | Current visible-history acquisition, separate from the observation journal |
| Trusted fingerprints and earlier checkpoints | Key identity and retained journal boundaries |
| Witness artifacts, if configured | Separate journal, signed posts and witness fingerprint |
| Verification results and delivered-file hashes | What was checked, which bytes were transferred and to whom |

From a trusted installation, with filenames and each workspace's actual fingerprint:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Retain the actual verification results and original artifacts. Export workspace notes from Case Board alongside the cited source material. Assemble cross-workspace findings in the top-level case directory; each TgWitness artifact has its own signature and verification procedure.

## Adapt the investigation

| Case | Trace | Deliver |
| --- | --- | --- |
| Bot-driven order/payment dispute | Entry announcement → saved link preview → bot start parameter → message and keyboard versions → panel callback receipts → private/group follow-up | Observed offer/response timeline and verified sources; a payment link alone does not prove a payment |
| Removed messages after an incident | All affected chats → saved originals/edits → deletion or missing-on-recheck outcomes → preserved media → coverage and other account perspectives | Preserved versions and explicit unknown intervals; no invented deletion actor |
| A participant changes names across chats | Numeric sender ID → name/username history → replies → other observed chats → cited destinations/files | A cited Telegram-account activity timeline, with real-world identity and relationship hypotheses kept separate |

[Collection reference](https://phishdestroy.github.io/TgWitness/docs/reference/collection/) · [People-profile verification](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#people-profiles) · [Evidence handoff](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#investigation-handoff) · [Completed validation](https://phishdestroy.github.io/TgWitness/docs/reference/verification/)


---

# Features and limits

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/features/

The current collection model, multi-account workflows, exports and operational boundaries of TgWitness.

TgWitness preserves Telegram conversations accessible to connected accounts, records observed changes and prepares verifiable exports. This reference describes the collection model, current workflows and their boundaries.

## Standalone application

TgWitness has its own installation, data directory, and release lifecycle. The bundled web interface handles setup and review; exported records can be used independently.

The operator connects their accounts, chooses sources visible to each, and obtains a saved observation journal. The panel exposes content, saved changes, observation provenance and known gaps. Another investigator can verify the exported material.

The panel distinguishes account authorization, access to a source, collector activity and recorded coverage. Review those states together when assessing an interval with few messages or a connection problem.

## Shared investigations

An administrator can issue [access tokens](https://phishdestroy.github.io/TgWitness/docs/reference/access/) scoped to workspaces and individual chats, with per-action permissions, IP restrictions, expiry, sign-in limits and session control. A read-only reviewer can inspect a case without receiving Telegram authorization or the main panel key. Chat-limited access stays separate from account-wide settings and full-journal exports.

Automatic MTProxy maintains working Telegram routes from four public sources or an operator catalog. [IP modes](https://phishdestroy.github.io/TgWitness/docs/reference/connection/#ip-modes) determine whether failure must wait for another proxy or may use an explicitly permitted direct route. External HTTP requests have a separate route and off switch.

## Archive tools

[History acquisition](https://phishdestroy.github.io/TgWitness/docs/reference/history/), [archive search and analysis](https://phishdestroy.github.io/TgWitness/docs/reference/analysis/), [read-only MCP](https://phishdestroy.github.io/TgWitness/docs/reference/mcp/), [local OCR/transcription](https://phishdestroy.github.io/TgWitness/docs/reference/media-analysis/) and [outgoing webhooks](https://phishdestroy.github.io/TgWitness/docs/reference/webhooks/) are included in 0.7.1. Analytical reports and recognized text stay separate from captured events.

[Case Board](https://phishdestroy.github.io/TgWitness/docs/reference/case-board/) adds source-linked bookmarks, quotes, notes and collections within a workspace. The [report constructor](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/) selects material, sections and one of eight designs for supported HTML/PDF exports.

## Optional extras

Everyday setup is account → sources → observation. **Extras** is a separate destination with a Telegram witness bot and a GitHub capture preview. Each states its availability and requirements before showing settings. Choosing a card opens instructions; it does not enroll or start a service.

Bot setup has three steps: create read-only access, choose publication settings, and launch on the witness host. Network and publication options, existing connections and verification commands are disclosed on demand. Downloaded configuration is distinct from a running witness. Switching extras retains the draft; account changes and locking clear the temporary token and form. The built-in guide includes launch instructions. [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) launches a pinned collector from your fork, captures one chat and produces an encrypted handoff with workflow provenance.

## Protocol and private sources

**MTProto is Telegram's protocol; Telethon is the Python library TgWitness uses to speak MTProto.** They are not alternative connection methods. Collection uses MTProto; the optional witness publishes signed checks through the Bot API.

Each workspace has its own authorized client and account update stream. TgWitness selects observations from configured sources and makes separate explicit requests for functions such as history snapshots and media downloads.

A private source needs no public username. Telegram peer type and numeric ID are the identifiers; titles and usernames can change. Access depends on existing membership and permissions. TgWitness does not automatically join sources or bypass join approval. An access hash from another account is not a universal access token.

The collection model must account for pre-join hidden history, participant/admin roles, session revocation, removal or changed permissions, group-to-supergroup migration, topics/forums, linked discussions, channel identities and unavailable attachments. Not every combination has been qualified live.

Source visibility is checked at collector start. Missing a source from the bounded dialog result means **access unconfirmed**, not proven removal. One unavailable source does not prevent observing other accessible sources. Never put invitation links or real sessions in public fixtures.

## Multiple accounts

The panel supports any number of **workspaces**, each with its own:

- Authorization, encrypted vault and connection route.
- SQLite journal and Ed25519 signing identity.
- Selected sources, media queue and capture settings.
- Observation state, errors, checkpoints and exports.

Switching the displayed workspace does not stop another collector. Duplicate account authorization across workspaces is rejected. A journal already bound to one Telegram account cannot be reassigned to another; reconnecting the same account is allowed. This preserves account identity and the relevant message-ID scope.

The application sets no fixed workspace count. Each workspace runs its own collector tasks for connection monitoring, media downloads, rechecks and new-chat intake within a shared Python process and event loop. Throughput depends on the workload. For process isolation, use separate installations, ports and data directories.

Assign each account sources it can access. Different accounts may observe the same group, but their observations remain separate and retain their origin. Two accounts on one operator-controlled machine are not two independent witnesses. **Export group** bundles the separately signed workspace ZIPs with a signed file list containing their workspace IDs, hashes and signing-key fingerprints. Each journal retains its own boundary. Build a combined cross-workspace timeline in case notes or analysis tools, retaining those source references.

## Capture and attribution

Sources provides per-account switches for new messages, edits, deletions, reactions and membership. Presets retain either all categories or messages/edits/deletions. The policy applies to the workspace's selected groups, survives restart, and is signed with before/after changes. Defaults preserve all categories. Turning a category off does not remove old records; turning it back on does not reconstruct missed events. Operational records, other group service events and explicit history snapshots are separate. Captured Telegram objects may retain embedded metadata regardless of the separate-update switches. There are no per-group category overrides yet.

| Material | Captured now | Boundary |
| --- | --- | --- |
| Message | Text, peer/message IDs, sender metadata, replies and original update envelope | Preserved as an account-visible observation signed by the collector |
| Edit | New observed version and any previously saved versions | Intermediate edits during downtime can be lost; sender is not necessarily editor |
| Deletion | Notification and prior captured content, if any | Usually no deleter or precise action time |
| Account-level deletion notice | Original notice; resolved records include the saved chat and correlation method | Requires exactly one previously saved private-chat or ordinary-group match in scope; other IDs stay `deletion.unscoped`. Channel and supergroup IDs are excluded from this correlation |
| Reaction | Delivered counters and visible recent identities | A complete available reactor list requires separate queries; channels may hide identities |
| Membership | Service messages and delivered participant updates | Visibility depends on role and chat type; missing events do not establish absence |
| Admin actions | Relevant delivered updates and an admin-log snapshot in channel/supergroup chat exports | The export reads the log when available to the exporting admin account; continuous admin-log polling is outside this path |
| Attachment | Original version descriptor, downloaded bytes/SHA-256 and attempt outcomes | A vanished file may be unrecoverable; the latest version is not substituted |
| History | Explicit snapshot of current visible messages | Does not reconstruct all edits or deleted content |
| Collector process | Start/stop, heartbeat, errors, settings, scope and program receipt | Self-report, not independent process attestation |

An action is attributed to a person only if the source actually supplies that actor. Otherwise the interface reports the missing attribution. Usernames and names are observed attributes, not proof of real-world identity.

## Capacity and Telegram limits

There is no universal number of chats that can be monitored with guaranteed quality. Capacity depends on peak events per second, attachment volume and sizes, additional RPCs, active accounts, disk latency/free space, network conditions, Telegram limits, acceptable lag and queue depth.

Telegram distinguishes passive delivery from active short polling. Its update documentation describes additional `updates.getChannelDifference` calls for open channels/supergroups and recommends at most **ten simultaneously short-polled sources**. This is not a limit of ten selected groups or a completeness guarantee.

| Mode | Purpose | Status |
| --- | --- | --- |
| Standard observation | Record delivered updates from selected sources | Implemented |
| Priority rechecks | Starred sources use their own configurable interval and take precedence in each bounded recheck pass | Implemented with history and message queries |

The priority star controls these rechecks. Additional `updates.getChannelDifference` short polling is not exposed as a separate user mode.

Arbitrary high-frequency polling, ignoring FloodWait or assuming linear capacity from extra accounts is not a valid sizing model. Default limits are the first 1,000 listed dialogs, up to 500 messages per history snapshot, 1–2,000 MiB per collected file by type, and 4 GiB uncompressed signed ZIP content; each is changed per workspace under **Parameters**. Exports have no fixed event-count cap. Browser fallback is bounded to 128 MiB by default; the streaming CLI has a configurable transfer limit, 5 GiB by default.

`tools/check_capacity.py` measures local synthetic ingestion and export. Its results are not Telegram delivery measurements or a guaranteed real-chat count. See [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/docs/reference/verification/) for the measured version and workload.

## Reliability and recovery

Implemented behavior includes SQLite WAL/synchronous transactions; atomic message and media-job writes; persistent jobs and retry delays; original-version descriptors; bounded retries; persisted media FloodWait; media downloads outside the text event's network wait; stable-prefix exports while later writes continue; atomic settings and audit records; preservation of working authorization after failed replacement login; isolation of a damaged additional workspace; explicit reconnect attempts; distinct authorization-loss reporting; and wall-clock change detection using a monotonic clock.

Account and channel pts/qts/seq are saved and resumed after a restart, and observed chats are rechecked periodically; see [evidence format](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#durable-collection-and-process-receipts-02). Saving the position periodically is not an atomic, lossless acknowledgement of journal acceptance.

Every process start records the previous head and offline boundary. Current history is not treated as gap repair. Telegram's difference retention is finite; `differenceTooLong` cannot reconstruct all vanished content. Irrecoverable gaps must remain explicit even if a later history snapshot succeeds.

## Evidence model

Each event records a sequence, local UTC observation time, source time when supplied, kind, source, actor when supplied, original payload, previous hash and signature. Message observations also retain collector account/run context.

The signed process receipt contains a random run ID; TgWitness/Python/OS/dependency versions; source-file SHA-256 values and aggregate fingerprint; initial account, scope and settings; UTC/monotonic readings; and the preceding journal head. Settings changes, start/stop and errors enter the same journal. Checkpoints are retained at startup, every five minutes while observing (changeable), and on orderly stop. A retained local checkpoint can detect rollback to an earlier journal prefix.

| Mechanism | What it establishes |
| --- | --- |
| File SHA-256 | Bytes match a known digest |
| Event hash chain | Record ordering/linkage relative to a known boundary |
| Ed25519 | Signature under a particular key |
| Independently retained checkpoint | Later material agrees with the retained boundary |
| Program-file measurement | Collector self-report about measured files |
| Valid independent TSA response | Existence of particular bytes by the TSA time under explicit trust assumptions |

RFC 3161 request preparation and OpenSSL response verification are implemented. Evidence mode also submits checkpoint hashes to configured timestamp services. Retain and verify the authority's response to establish an independent time anchor. See [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/docs/reference/timestamp/).

Retain checkpoints independently, control access to signing keys, keep transfer records and verify exports with trusted software. The [verification scope](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope) explains how those checks complement one another and which trust assumptions apply.

## Export, deployment and handoff

A signed ZIP contains original JSONL, CSV, HTML, preserved attachments, hashes, a signed manifest and a convenience verifier. It covers one workspace and a fixed full journal prefix. Panel search filters do not silently remove records. Secret keys, tokens and Telegram sessions are excluded; original observations can still contain personal information and Telegram metadata.

Retain the ZIP digest, trusted fingerprint, checkpoint, process receipt and handoff record separately. Use a verifier from a trusted installation, rather than trusting executable code solely because it appears in the examined ZIP.

The browser interface ships locally without Node.js, CDNs or external fonts. One operator token controls the installation. Remote access needs HTTPS or an SSH tunnel. Native Python and container definitions are supplied, with service examples under [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md); executed platform checks are listed separately.

The default workspace uses the data root; additional workspaces use `profiles/<id>/`. Backup requires a stopped process and the complete data/key set. Evidence ZIPs are not application backups. Secrets can use an external master key for a new data directory; journal/media encryption is provided by the operator's disk/volume. See [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/docs/reference/connection/) and [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/docs/reference/operations/).

## Stable release criteria

Before a stable release, qualify:

1. Real private groups, supergroups, forums and channels with member/admin roles and hidden/visible history, including login/2FA, revocation and access loss.
2. Controlled edits, deletions, reactions, membership and media against known actions.
3. Process/host crashes, disk failures/full disk, expired file references, FloodWait, network loss, corrupted files and database rollback.
4. Sustained multi-account use with measured lag, queues, memory and disk, including quiet and noisy sources together.
5. Interruption between MTProto state advancement and journal acceptance.
6. Clean installation on the intended OS/container matrix and verified backup restore.
7. Independent review of security, signatures and attribution/evidence claims.

Scoped panel access is described in [access and permissions](https://phishdestroy.github.io/TgWitness/docs/reference/access/). Version 0.6 supports the bounded single-account TData and account-file import described in [ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/). Review Telegram API terms before publication. Research references and platform findings are in [RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md).


---

# Case Board reference

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/case-board/

Bookmarks, exact highlights, action slices, discussions, scoped access and the signed annotation history used by Case Board.

Case Board gives an investigation team a shared working view of saved material. Bookmark an observation, highlight an exact passage, save a range of actions, and discuss it with colleagues. Cards retain their source references and signed revision history. Team annotations stay in the workspace, separately identifiable from the original Telegram observations.

[Evidence model](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/) · [Access](https://phishdestroy.github.io/TgWitness/docs/reference/access/) · [Reports](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/)

![Synthetic investigation feed](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

## Work with a case

Open **Investigation → Case Board** in Standard or Expert mode. The language follows the panel. Use **To board** beside a journal record or saved chat message, or focus it and press **B**. The bookmark is added to Inbox in one click. Edit its title, labels and note, or move it to a collection. A changed card appends a signed revision; removing it preserves the history.

For a first case, choose a collection and add the records that answer one question. Use comments to review the interpretation, then **Presentation** to walk through the cards and source context. Choose Case Board material separately in [Report studio](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/) when preparing the deliverable. Saving a slice does not automatically configure a report's data filters.

Select text inside a saved chat message to reveal **Highlight → board**. Select its colour and add a note. The server checks the exact quote and saved version, including emoji, RTL text and combining marks. The interface does not map a selection through masked or transformed text.

Shift-click two records in one chat for **Slice between**, use **Slice by time**, or save the journal's current chat, period and event-kind filters. A saved slice has its own authoritative predicate: opening it in Journal also applies multiple chats, message-number limits and actor filters. **Show records added since bookmark** isolates the later additions. Changing Journal filters exits the slice. From People, **Slice this person’s actions** uses the recorded actor ID; it does not assume that the message author edited, deleted or reacted to a message.

The slice dialog previews counts before allowing creation. `all` includes every recorded kind, including snapshots, edits, deletions, reactions, membership/service updates, own actions, buttons, media outcomes, recovered messages and future event kinds. The selection describes saved observations. Unknown-chat deletion notices are separate context, available only to a whole-workspace access, never attributed to one of the chosen chats.

Collections have a declared chat scope. An empty scope means the whole workspace. A collection cannot contain cards outside its scope; a chat-limited participant cannot read a broader collection. Inbox is a virtual collection for unassigned cards. Search and filters cover visible cards only; threads and mentions inherit the parent card's access. Removed comments have a tombstone in the discussion. No viewer history is recorded.

**Presentation** opens all cards in the chosen collection, with Card, Source context and Team comments views and keyboard Previous/Next controls. It provides no editing controls. The ordinary feed is paginated; presentation loads its list in pages and retrieves one card's detail at a time.

## Permissions

All operations require `view`, workspace/chat scope and `board.read`. `board.write` adds cards, comments, moves and open/review statuses. `board.manage` permits collection management, confirmed/dismissed statuses, revisions/removal of someone else's card. A status is a team decision, not a cryptographic verification result.

Access form presets: Reviewer = read; Analyst = read/write; Operator = read/write/manage, in addition to their existing permissions. Existing grants do not silently acquire new rights. The main administrator has all rights, and posts as **Main administrator**. Use named grants for attribution. Mentions list only current accesses able to read the complete parent card.

A grant for chat A cannot obtain a card or slice for A+B, even by guessing its ID or supplying a false `target.chat_id`. Target metadata is resolved from the signed event hash on the server. Collections, discussion counts, related cards and live notifications are filtered before response. Exports require `export` as well as `board.read`; an existing exporter without board access gets the ordinary evidence archive without team notes. SSE rechecks current grants before each batch.

## Stored contracts

Like observations, annotations are written transactionally to an append-only SQLite table in the workspace. `annotations.jsonl` is its exact canonical export from the same read snapshot as `events.jsonl`. There is no second competing annotation store and no `board.activity` journal event.

Each line has exactly:

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

The abbreviated example above illustrates the envelope; actual payloads include their model defaults and server-resolved target fields. API request schemas are under [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json), generated from the runtime Pydantic models by `python tools/build_board_schemas.py`. Extra request fields are rejected. IDs are generated server-side when omitted. Authorship, time, snapshot and signature cannot be supplied by the caller. Named grant IDs follow Access's existing 16-hex format; card IDs are 32 hex.

Canonical JSON is UTF-8, sorted object keys, no whitespace between tokens, unescaped Unicode, and no NaN/infinities. The annotation hash is SHA-256 of the canonical object containing `format: "tgwitness-annotations-v1"` and all seven envelope fields through `previous_hash`. This format tag separates its hash domain from observations. The signature is Ed25519 over the 32 raw hash bytes. Sequence starts at 1. Revisions retain the card ID and name the preceding annotation hash in `supersedes`; they cannot change chat scope. Moves, statuses and removal are separate records. The SQLite table rejects UPDATE and DELETE.

`case-board.json` contains `{statement, signature}`. The canonical statement is signed by the workspace key and contains `format: "tgwitness-case-board-v1"`, `public_key`, `created_at`, `journal_head`, `meaning`, and `state`. State is deterministic replay: `annotations_head`, an ordered `items` array (collections, cards, comments including tombstones), and `status_history`. Items retain their last annotation hash, sequence, author and time, as well as the original creator and creation time across revisions. Replay checks revisions, parents, collection references and duplicate action IDs. `manifest.json` and new checkpoints also bind `annotations_head`. Retain a checkpoint independently to detect truncation or rewriting with a copied signing key.

### Text versions

`range.start` is a zero-based Unicode code-point offset, `length` is a positive code-point count, and `quote` must equal the exact substring of `payload.text` or `payload.caption` at the target event. No NFC/NFKC, case folding or grapheme normalization is applied. Python string slices and JavaScript `Array.from(text)` implement the same indexing. Combining marks and ZWJ emoji may occupy several code points. `range.version` is the target event hash, not the current message version or Telegram's UTF-16 entity offset. Later edits never relocate a highlight automatically.

### Slice identity and time

`query` accepts exactly one `chat_id` or nonempty `chat_ids`, optional inclusive `from`/`to`, inclusive message-ID bounds (one chat only), `kinds: "all"` or exact/prefix wildcard kinds, explicit `actors`, `search`, `hide_system`, and `include_unscoped`. Journal kind groups expand to their exact predicates. Search uses the journal's NFC/case-folded payload search without altering signed source text. Dates require a timezone and normalize to UTC. Dates filter **observed_at**. Telegram's `source_at` is displayed separately. A deletion without a source timestamp has no invented deletion time. A late record observed outside a time interval does not enter it; a message-ID slice can include a later deletion for those message IDs.

`snapshot` fixes creation time, the journal sequence/hash boundary, matching count, first/last sequence and `result_hash`. The latter is SHA-256 of the UTF-8 canonical JSON array of matching event hashes sorted lexicographically, including `[]` for an empty slice. It also carries exact kind counts and a 24-bin observation-time miniature. A slice stores a query, not duplicate source records. At export, `board/slices/<id>.json` lists current hashes and added/removed sequences. The verifier reconstructs the original result at the creation boundary, then the current result. Added records are reported as a change fact. Removing an original event breaks the immutable evidence chain; it is not silently accepted as an ordinary removal from a slice.

Reaction snapshots have incomplete recent-actor lists. The explorer compares adjacent snapshots of the same chat/message, including a predecessor outside the slice, and reports aggregate count deltas **between observations**. Missing recent actors are not claimed to have removed a reaction. The first snapshot has no inferred earlier state. Actor observations remain attributed to the snapshot in which they were supplied, not to an invented action time.

## API and exports

`GET /api/board` accepts collection/chat/author/label/state/from/to/q/kind/comments, offset/limit and newest/oldest order. `GET /api/board/card/{id}` returns a card, source preview, thread, status history and related cards. The participants subroute returns eligible mention choices. `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}` appends a record. `POST /api/board/slice-preview` calculates a query. Slice records are paged at `GET /api/board/slice/{id}/records`; recomputation always uses the current stable read snapshot. Live `/api/stream` emits payload-free `board` notifications, separately from journal cursors.

`GET /api/board/export` returns a signed document. Chat-limited access receives a clearly labelled signed **disclosure**, never another chat's annotations or the full chain. Full evidence ZIPs carry `annotations.jsonl`, signed `case-board.json` and slice JSON appendices. HTML/PDF/JSON report settings select no board, bookmarks/slices without discussion, or cards with comments. The section explicitly separates team opinions from observations. Report data filters restrict the readable notes too; full signed source files in the evidence ZIP remain complete.

`GET /api/board/slice/{id}/export` produces a signed `tgwitness-board-selection-v1` JSON excerpt; `?format=csv` produces a convenient table without a standalone signature. Keep the JSON and ZIP:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

The selection check authenticates the signed statement, exact source records and completeness of its query at the specified boundary. The evidence ZIP may be newer but must contain that prefix. A dangling target is reported explicitly. A different original slice snapshot, changed annotation, mismatched replay state or changed source fails. Old archives without annotations retain their existing verification behavior.

Handover defaults to **Do not include**. Explicit inclusion projects cards through the already minimized records, omits inaccessible/omitted targets, withholds highlights whose source text was minimized, cleans team text with the same mention/contact rules, and optionally replaces investigator labels with R01, R02… in metadata and known occurrences in notes. No original `annotations.jsonl` is disclosed. The signed `tgwitness-case-board-handover-v1` sidecar and report contain the same minimized material. Slice counts describe disclosed records only, with original snapshot/query actor details withheld. Free-text names not known to the minimizer still require review, as they do in ordinary handovers. This derivative does not claim to preserve original annotation signatures after redaction.

## Operating limits

Parameters include soft limits of 10,000 cards and 50,000 comments, a slice page of up to 5,000 records, and media-preview control. Soft limits warn without deleting history. Feed pages are at most 200 cards. Standalone JSON slice excerpts are capped at 64 MiB; narrow the query or use the signed ZIP for larger material. The standalone verifier caps annotations replay at 256 MiB. No external comment notifications are enabled or implemented by Case Board.

The feature's automated acceptance uses fictional data and a simulated Telegram transport to check storage, access, rendering and exports. See [verification scope](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope) for the scope of the evidence checks.


---

# Archive analysis

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/analysis/

Search saved messages, review AI inputs and keep analytical reports with their source references.

[Workflow guide](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Use **Journal** for local search without AI. For **Ask the archive**, first enable and configure a provider in **Integrations**. The workspace selector chooses the account; the form chooses chats and the observation period. Retrieval runs locally. An exact phrase or domain narrows retrieval; a message ID requests saved versions. Review the excerpts and open their journal records or context. There is no vector database or automatic Telegram action.

## Providers and consent

AI starts disabled in every workspace. Only the main administrator can configure the model, endpoint, encrypted API key, context/output limits, timeout and daily request budget. The key is never returned to the browser. Keep a blank key field to retain the current key, or explicitly remove it.

Ollama uses its documented [`/api/chat` endpoint](https://docs.ollama.com/api/chat) with non-streaming JSON output. Its default address is `http://127.0.0.1:11434` on the TgWitness server. The operator can change it using `TGWITNESS_AI_LOCAL_ENDPOINT`; this is not a model-controlled address. Install the selected model yourself. TgWitness does not download it automatically.

The compatible provider expects a base URL ending in `/v1` and the [Chat Completions protocol](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, JSON response mode, `max_completion_tokens`, and `choices[0].message.content`. Services lacking these fields are not supported. Connection testing sends synthetic text and counts toward the request budget.

Every request uses the workspace's configured outside route. A blocked route or Telegram-only MTProxy is an error; there is no direct retry. A deliberately configured local Ollama address permits a private destination. A loopback AI endpoint requires the workspace's Direct outside route; proxy routes are rejected before transmission. For other private services the existing server-level private destination opt-in applies. The preview shows the endpoint and outside route, including the proxy host when applicable. Changing that route requires a new preview.

Before generation, **Data sent to the model** shows the request: question, checked excerpts, event kinds, observation times and coverage markers. Telegram sessions, raw fields, provider keys, attachment bytes and the full journal are not part of that context. Uncheck unwanted sources, then explicitly approve processing. External providers may retain submitted content under their own policies. Local execution means the endpoint is local; it is not a guarantee about an independently configured service's behavior.

There are at most two concurrent provider requests globally and one per workspace. A preview expires after ten minutes and can generate one answer. The provider's reported token counts are shown; a cost estimate appears only when both input and output tariffs have been configured. Failed attempts also consume the daily request budget. No automatic retries spend additional budget.

## Sources and limits

Retrieval examines saved message text with a bounded lexical search. It returns up to 24 sources and marks truncated excerpts or incomplete result sets. The period refers to **observation time**, not a claim that Telegram history is complete. Workspace-wide coverage events are withheld from chat-scoped access. Missing data is described as not found in the available archive.

The model receives no tools. Its source IDs are resolved against the selected records, hashes are rechecked, and quoted strings must occur in those records. Unknown IDs, changed quotes and uncited claims reject the answer. The application creates links; model-generated URLs are not used as citations. These checks establish source existence and quote accuracy, not the truth of an inference. Review inferences against the records before relying on them.

## Reports

Save a reviewed answer as a separate analytical report. It includes the model summary, observed chronology, extracted links and handles, edit/deletion records, coverage limits, and source event hashes. The provider, model, endpoint, time and prompt-template version accompany it. No identities are automatically merged.

Analyst revisions and notes are stored separately from the model summary. Reports live in encrypted derived files, with an index outside the signed event stream; the original events and media do not change. Only the owner or administrator can open a report, and source access is checked again. Download also requires export permission. Version 1 does not sign reports or imply that model conclusions are verified evidence. Limits: 100 reports per workspace and 100 analyst revisions per report.

For manual OCR and transcripts, see [media processing](https://phishdestroy.github.io/TgWitness/docs/reference/media-analysis/). For client access, see [MCP](https://phishdestroy.github.io/TgWitness/docs/reference/mcp/).


---

# Read-only MCP

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/mcp/

Connect an MCP client to selected workspaces and chats with expiring, revocable access.

Connect an analyst client to selected workspaces and chats. TgWitness serves **Streamable HTTP at `/mcp` in the panel process**. Each connection has its own token, expiry and permitted tools. MCP cannot send Telegram messages, change settings or modify the signed journal.

[Workflow guide](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

## Install and check

Use the Python environment that runs the panel. From a source checkout:

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

Restart the panel with its usual data directory and launch arguments after installation. Readiness should include `[PASS] mcp: streamable-http available`. **Integrations → MCP** shows the runtime status and an installation command using that server's actual Python executable. **Re-check** refreshes this status without reloading the page; it does not install packages or restart the server.

The MCP extra uses the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk). `deploy/constraints-mcp.txt` pins the tested SDK and dependencies.

## Issue a connection

1. Enter a label and choose the workspaces and chats the client may read.
2. Select tools individually or use a preset. Only implemented tools are offered.
3. Choose 1, 7, 30 or 90 days, or a custom expiry between one minute and 90 days.
4. Press **Create connection**. The token appears once beside the client config.
5. Copy the token and config, then run **Check connection**. It initializes MCP and lists permitted tools; **no messages are read**. The result shows protocol version, tool names, count and elapsed time.
6. Press **Done** when the credential is saved. Polling preserves the form and the shown-once card. Locking the panel clears displayed secrets.

The list shows recent use, last tool, address and requests in the last minute. **Revoke** ends access. **Rotate token** revokes the old credential and issues a replacement with the same scope, tools and expiry; copy the replacement once. Panel login tokens and Telegram credentials do not work as MCP tokens.

## Connect your client

Select the client in the panel and copy its generated configuration. Configs use secret references or explicit placeholders; the token is copied separately.

| Client | Configuration | Connection |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP, `type: "http"`, bearer header |
| Claude Desktop | `claude_desktop_config.json` | Local stdio bridge |
| Cursor | `.cursor/mcp.json` | HTTP with an environment-variable header |
| VS Code Local | `.vscode/mcp.json` | HTTP with a password `promptString` input |
| Windsurf | `mcp_config.json` | HTTP with a bearer-header placeholder |
| Other clients | URL and Authorization header | Streamable HTTP |

TgWitness uses bearer tokens, without OAuth discovery. Use the local stdio bridge for clients whose remote connector requires OAuth. For VS Code, input variables apply to the **Local** harness and are not forwarded to Copilot sessions. Configuration references: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

The canonical entry point for a local bridge is:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

Use the client's local Python with the MCP extra installed. Set `TGWITNESS_MCP_TOKEN` in its protected environment. Keep credentials out of command arguments and URLs. `tgwitness-mcp` is the same entry point. The old `tgwitness.mcp_bridge` module and `TGWITNESS_ARCHIVE_TOKEN` name remain compatibility paths with a warning; new configs use `mcp_server` and `TGWITNESS_MCP_TOKEN`.

## Cloudflare Tunnel

Forward the panel's `/mcp` route and preserve the bearer header. Opening MCP settings as an administrator registers the panel's current origin for this run. For a stable address available immediately after restart, configure `TGWITNESS_PUBLIC_URL` with the panel's HTTPS origin before starting the panel. Arbitrary Host and forwarded headers do not register a trusted address. Host and Origin checks reject unrelated browser origins. Responses use `Cache-Control: no-store`; authorization values are never logged.

A `*.trycloudflare.com` address is temporary. When a tunnel restart changes the hostname, update the configured public URL and each client's MCP URL. Use a stable hostname for saved client configurations.

## Tools and boundaries

| Tool | Reads |
| --- | --- |
| `list_workspaces` | Granted workspaces |
| `list_chats` | Granted chats |
| `search_messages` | Saved message text within the selected period |
| `get_message_versions` | Captured versions and deletion observations |
| `get_message_context` | Nearby captured message IDs |
| `get_journal_event` | One sanitized record with its source reference |
| `get_capture_status` | Collection state and permitted coverage records |

`tools/list` returns only the tools granted to that connection. Calls to other tools are refused. Group-context, episode, terminology and reply-chain tools are not offered in this build; their separate context-pack backend is not included.

Every read checks the token, tool and workspace/chat scope, including after the database work finishes. Limits are 60 requests per minute, 50 records per page, 64 KiB per result and an eight-second archive deadline. A timed-out MCP call returns a tool error asking for a narrower period or lower limit.

Message results carry `untrusted_content: true`, workspace/chat/message IDs, event sequence, saved hash and a panel link. Raw Telegram objects, access hashes, sessions and keys are omitted. Text truncation is marked. Edits, deletion notices and `missing_on_recheck` are distinct observations. Missing records do not prove an event never happened.

Treat instructions inside captured messages as evidence, never as client instructions. Read-only access prevents archive changes; the client can still retain the content it is allowed to read. Hashes identify saved records and support integrity checks; they do not prove Telegram authorship or complete capture.


---

# Local OCR and transcription

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/media-analysis/

Recognize captured images and audio with a local worker; keep derived text linked to its source file.

[Workflow guide](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Open a `media.saved` journal record, choose **Recognize attachment**, then select OCR or transcription under **Ask the archive**. Processing is manual and local. There is no cloud media mode or automatic upload. Original attachment bytes and `media_sha256` remain unchanged; recognized text is explicitly marked as machine recognition and stored separately with the source hash, engine/model version, language, parameters and completion time. Transcripts retain returned timestamps.

Search these results using **Search recognized text** and the OCR/transcript filter. This is a separate derived-data search; it does not silently turn machine recognition into original Telegram text or add it to signed events.

## Set up the optional worker

Version 1 requires a Linux host with a local Docker daemon. Windows installations can run TgWitness inside a Linux VM/WSL environment with its own local daemon. The panel never decodes an untrusted attachment itself.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

Set these variables in the TgWitness service environment and restart it. The daemon socket defaults to `/var/run/docker.sock`; rootless deployments can set `TGWITNESS_DOCKER_SOCKET`. The worker explicitly uses that Unix socket rather than a remote Docker context. Do not expose a Docker API to panel users or mount its socket inside the recognition container.

For transcription, separately install a CTranslate2-compatible Whisper model, then set `TGWITNESS_WHISPER_MODEL_DIR` to its directory. The worker loads it with `local_files_only=True`; the selected model and input are mounted read-only. See the engine's [model-loading documentation](https://github.com/SYSTRAN/faster-whisper). The supplied OCR image includes English and Russian trained data. Build another language into your image when needed; language codes follow [Tesseract's CLI](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).

No model is fetched while processing. Build/download setup may use the network; each actual recognition container has networking disabled. Install the image before enabling it; runtime uses `--pull=never`.

## Bounds and recovery

The container runs as an unprivileged user with a read-only root, dropped capabilities, `no-new-privileges`, one CPU, 2 GiB memory, a PID limit and a bounded temporary filesystem. Only a verified copy of the selected file and an optional model directory are mounted. The collector's database, vault and session are not mounted. The [Docker runtime flags](https://docs.docker.com/reference/cli/docker/container/run/) enforce these limits; this remains a container boundary, not a hardware enclave.

Files are limited to 50 MiB, images to 20 million pixels, audio to 30 minutes with a known duration, and processing to five minutes. One worker runs at a time, with at most 20 queued/running jobs and 100 retained jobs per workspace. Cancel stops the container; retry creates a new job linked to the prior attempt. Interrupted jobs are marked after restart. Processing can fail when a model cannot fit the configured limits; it does not silently run without isolation.


---

# Outgoing webhooks

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/webhooks/

Send scoped events to HTTPS receivers with HMAC signatures, retries and delivery status.

[Workflow guide](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Open **Integrations → Outgoing webhooks** in the selected workspace. Add an HTTPS receiver, choose collector/media/export events, and optionally select chats for new observations and changes. Message text is off by default. Enabling excerpts adds at most 1,000 characters to message-change events; raw Telegram fields and credentials are never sent.

Copy the HMAC secret once into the receiver's protected configuration. It is encrypted in TgWitness's vault and cannot be retrieved from the panel. Remove and recreate a destination to rotate it. **Send synthetic test** queues a test with no chat content; refresh delivery status to see its outcome.

Delivery extends the existing notification loop alongside Apprise. It uses the workspace's outside route and existing private-destination restrictions. There is no direct fallback or redirect following. URLs must not contain credentials, query strings or fragments; private addresses require the server-level network opt-in, not a setting a panel user can bypass.

## Payload and signature

Schema: [`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json). Every payload contains `event_id`, `timestamp`, `workspace`, `type`, `synthetic`, and counters. Journal-based events include their sequence and hash. Full-export completion and synthetic tests are delivery events, with no invented signed journal reference. Telegram deletion notices and `missing_on_recheck` remain distinct types.

The `X-TgWitness-Signature` header is `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`. Compute HMAC over the exact bytes `timestamp + "." + raw_request_body`, using the displayed secret as UTF-8 bytes. Compare signatures in constant time before parsing or acting on the body. Reject timestamps more than five minutes from your clock. The timestamp is refreshed on each delivery attempt.

Use `event_id` as an idempotency key in durable storage, with an atomic unique constraint before side effects. A valid signature alone does not prevent a recent request from being replayed. Keep processed IDs for at least the entire retry window; retain them longer if the receiver can reprocess stored events.

## Retries

Deliveries are queued durably before HTTP requests. They use at-least-once semantics: a lost acknowledgement or restart may deliver an event again with the same ID. There are eight attempts with exponential backoff, starting at 15 seconds and capped at one hour. Success requires a 2xx response. Exhausted jobs leave a visible error; delivery is not guaranteed after retries end.

The queue holds 1,000 deliveries. When full, scanning journal events pauses and resumes after space is available. A full-export completion that cannot be queued sets a visible queue error. Up to five deliveries are attempted per notification pass, and the latest 100 attempt records are retained. Removing a destination also removes its pending deliveries.

## n8n example

Import [the example workflow](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json). It is inactive and contains no secrets or downstream actions. Set `TGWITNESS_WEBHOOK_SECRET` in the n8n worker environment, allow that environment access, and allow the `crypto` builtin for the Code node. The example uses the Webhook node's raw-body option, checks signature/freshness, and acknowledges validated events. This matches the node's [documented implementation](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts).

Before adding SIEM writes or notifications, add durable idempotency storage keyed by `event_id`. Restrict n8n workflow editing and execution-log retention according to the data you elected to send. TgWitness adds no inbound commands.


---

# Public showcase

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/showcase/

Publish saved messages of selected public channels and signed snapshots through expiring, revocable links.

**Access → Public showcase** creates a separate, read-only page using the existing access-token system. It reads the installation's saved observations. It does not start a collector, sign in to Telegram or acquire a channel for a visitor.

## Publish a page

1. Save a source profile for each public channel you want to show. A channel must have a public username in its latest saved profile; groups and private chats are not eligible.
2. Open **Access → Public showcase** (or `/showcase-manage.html`) as the administrator.
3. Select channels across up to 16 workspaces, enter the public page title, and choose a link lifetime of 1, 7 or 30 days. Internal workspace labels are not published. Up to 64 channels can be included.
4. Review the selected channels' text for publication, then click **Preview selected records**. The preview uses the same server-side projection as the visitor page.
5. Click **Create showcase link**. Copy the link while it is visible. Open it in a separate browser to review the recipient's page before distributing it.

The link contains an access token in its URL fragment. The page removes the fragment before making API requests and exchanges it for a browser session. Anyone holding the link can open the selected material until expiry or revocation. New links allow 100 concurrent sessions, each lasting at most one hour. Existing Access controls can also enforce address restrictions and sign-in limits through the grant API. Normal reviewer access is a different mode and still includes the original permitted messages and files.

## What visitors see

| Visible | Kept private |
| --- | --- |
| Selected public channel titles, usernames and profile observation dates | Account identities, internal workspace labels and unselected sources |
| Captured text and each saved edit | Structured sender IDs, names, usernames, phone numbers and profile values |
| Deletion observations with the previously saved text, if available | Attachments, avatars, thumbnails, filenames and original payloads |
| Markers saying an author/profile or attachment was recorded | Forwarding and reply metadata, network routes, IP addresses and credentials |
| Selected-channel event counts, current collection switches, heartbeat and checkpoint interval | Collection controls and ordinary evidence-export APIs |
| Signing fingerprint, journal checkpoint and consistency proof | Signing keys and Telegram sessions |

**Public message text is not automatically anonymized.** A name, mention, phone number or link written into the message remains part of that text. `Redacted` applies to the structured author/profile fields. Review the actual selected content before publishing it, including preserved edits and deletions.

Eligibility reflects the **latest saved source profile**, not a live Telegram lookup. If a subsequent profile no longer has a public channel username, new requests exclude the channel. Refresh source profiles when public visibility changes. Readers may already have saved material they previously received.

The original signed records stay unchanged. The displayed projection is signed separately and carries hashes referencing its original records. A projection signature authenticates the displayed statement; it is not the original event's signature over redacted bytes.

## Check signatures and continuity

Expand **Fingerprint & signed checkpoint** and download a snapshot. After a page refresh, the download includes the preceding browser snapshot and a Merkle consistency proof between their journal boundaries. Automatic refresh is once a minute while the page is visible and showing its first page of observations.

With TgWitness installed, verify the downloaded file offline:

```
python -m tgwitness.showcase_verify showcase.json --fingerprint TRUSTED_COLLECTOR_SHA256
```

The fingerprint must come from a separately trusted reference. To compare against a snapshot you retained yourself, use `--previous earlier.json`; this overrides the previous snapshot carried inside the download. The current proof must begin at that retained boundary. Authenticated clients can request that proof using `GET /api/showcase/{workspace_id}?challenge=<32-hex-random>&from_count=<retained-count>`. A shorter journal returns HTTP 409 instead of silently resetting the boundary.

The signed checkpoint commits to the **whole collector journal**, including its record count and opaque head hash. Displayed message counts apply only to the selected public channels. The page never lists the other journal's contents. These are event counts, not unique-message counts. The settings describe the current configuration, not every earlier recording interval.

Signature and consistency verification can detect changes relative to a retained boundary. It does not independently recount the signed counters, certify Telegram origin, demonstrate uninterrupted capture, or replace an independent witness. For that review, use the [evidence verifier](https://github.com/phishdestroy/TgWitness/blob/main/docs/TRUST.md), [independent witness](https://phishdestroy.github.io/TgWitness/docs/reference/witness/) and [tested-scale record](https://phishdestroy.github.io/TgWitness/docs/reference/verification/). Synthetic installations are visibly labelled as synthetic.

## Revoke or host the page

Use **Revoke** in the showcase manager or the existing **Access** section to close the link and end all its sessions. The visitor clears displayed records when a request detects that access has ended. Expiry and permissions are checked on every request. Showcase grants cannot be converted to ordinary panel access in place; create a new grant to change modes.

Serve the page through the installation's existing HTTPS address. Publishing a link does not open a new port, create a tunnel or change DNS. The HTML and API remain on the user's installation. A showcase visitor cannot use the ordinary message, profile, media, export or management APIs with this access.

## Local regression checks

```
python tools/check_showcase.py
python tools/check_showcase_browser.py
```

Both use synthetic records and a local HTTP server. They do not connect to Telegram.


---

# How the evidence works

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/how-it-works/

Hash chain, signatures, checkpoints and witnesses explained with the exact formulas the verifier uses.

TgWitness preserves what a collecting account observed, links those observations into a signed journal and lets another person verify an export against a trusted key and an earlier retained checkpoint.

The [local documentation website](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally) adds interactive examples at `/docs/concepts/`, a checkpoint decision explorer at `/docs/witness/`, and walkthroughs for [Case Board](https://phishdestroy.github.io/TgWitness/docs/reference/case-board/), [report design](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/) and [handover extracts](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#handover-extract). All example messages, counts and delays are fictional. Hashes in the chain sandbox are calculated with SHA-256 in the browser. Nothing is sent to Telegram.

## A message changes; observations accumulate

Sequence diagram · Telegram → Collector: New message: Meet at 10:00; Collector → Signed journal: Append message.new; Telegram → Collector: Edit: Meet at 11:00; Collector → Signed journal: Append message.edited; Telegram → Collector: Deletion notice; Collector → Signed journal: Append message.deleted; Note on Signed journal: Original + edit + deletion observation remain · Telegram · Collector · Signed journal · New message: Meet at 10:00 · Append message.new · Edit: Meet at 11:00 · Append message.edited · Deletion notice · Append message.deleted · Original + edit + deletion observation remain

**Diagram as text**

1. Telegram → Collector: New message: Meet at 10:00
2. Collector → Signed journal: Append message.new
3. Telegram → Collector: Edit: Meet at 11:00
4. Collector → Signed journal: Append message.edited
5. Telegram → Collector: Deletion notice
6. Collector → Signed journal: Append message.deleted
7. Note on Signed journal: Original + edit + deletion observation remain

This simplified sequence assumes Telegram delivered each update and the selected account could see it. Operational events also share the journal. A deletion notice does not supply the deleter or an exact deletion time. Repeated deliveries are separate observations; there is no journal-wide duplicate suppression.

## What a hash covers

![Observe, encode, hash and sign: each new event includes the preceding hash.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

Read the formula from the inside out: **C** turns the nine fields into exact bytes; **SHA-256** produces their digest; **hex** is how that digest is stored. The previous hash is already inside the event. **unhex** turns the stored hash back into the 32 bytes that Ed25519 signs.

[Static chain diagram](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

Let C(ei) be the canonical UTF-8 JSON of the nine event fields. The first `previous_hash` is 64 zero characters. Each later record includes the preceding record's hexadecimal hash:

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

The signature covers the 32 raw digest bytes. The hash input contains exactly `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` and `previous_hash`. Object keys are sorted; whitespace and ASCII escaping are omitted; NaN and infinity are rejected. See the [exact encoding](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#event-canonicalization).

Flow diagram · 64 zero characters → Record 1 / hash h1; Record 1 / hash h1 → Record 2 includes h1 / hash h2; Record 2 includes h1 / hash h2 → Record 3 includes h2 / hash h3; Record 3 includes h2 / hash h3 → Signed checkpoint: count 3, head h3 (retain elsewhere) · 64 zero characters · Record 1 / hash h1 · Record 2 includes h1 /hash h2 · Record 3 includes h2 /hash h3 · Signed checkpoint:count 3, head h3 · retain elsewhere

**Diagram as text**

1. 64 zero characters → Record 1 / hash h1
2. Record 1 / hash h1 → Record 2 includes h1 / hash h2
3. Record 2 includes h1 / hash h2 → Record 3 includes h2 / hash h3
4. Record 3 includes h2 / hash h3 → Signed checkpoint: count 3, head h3 (retain elsewhere)

| Change to the supplied journal | What detects it |
| --- | --- |
| Alter record 2 while leaving its saved hash | Recomputed event hash differs; its signature no longer covers the changed event |
| Rebuild the altered record and every later hash | The original signatures fail; a retained checkpoint at the affected boundary also disagrees |
| Remove the tail but keep the remaining prefix intact | An earlier retained checkpoint beyond the supplied prefix reveals that the export is too short |
| Re-sign a replacement journal with another key | A separately trusted key fingerprint rejects the replacement identity |

![Changing a saved field changes its digest; rebuilding hashes does not restore the original signatures.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**Try the logic on record 2:** change `Meet at 11:00` to `Meet at 12:00` in the saved event. Its recomputed hash no longer matches. Recalculating the later chain can repair its links, but cannot make the original signatures cover the new digests. An observed Telegram edit, by contrast, becomes a new journal record.

[Static change diagram](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

Hash links alone do not prevent someone from recalculating a replacement chain. Trust comes from checking signatures under an independently trusted key and comparing with references retained outside the collector.

## What an earlier checkpoint adds

![Retain count 3 and head h3; a later export of 4 records is checked at position 3.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**The reference stays still while the journal grows.** If the checkpoint says “3 records, head h3”, a four-record export can pass by matching h3 at position 3. Its newest head is h4, which is expected to differ. An export of only two records fails.

[Static checkpoint diagram](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

After verifying the checkpoint signature, require:

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

An export may extend beyond a checkpoint. It must agree at the retained boundary. The real verifier also checks every event's sequence, previous link, hash and signature. Comparing only the final stored head would miss an altered interior record whose saved hash was not updated.

## Where a witness belongs

Flow diagram · Collector / account session / key A → Read-only checkpoint endpoint; Witness / pinned collector key / own key B → Separate signed witness journal; Witness / pinned collector key / own key B → Read-only checkpoint endpoint (Request a check); Read-only checkpoint endpoint → Witness / pinned collector key / own key B (Signed answer); Witness / pinned collector key / own key B → Channel with signed TGW1 posts (Bot API / own token) · Host A · Host B · Collector / accountsession / key A · Read-only checkpointendpoint · Witness / pinned collectorkey / own key B · Separate signed witnessjournal · Channel with signed TGW1posts · Request a check · Signed answer · Bot API / own token

**Diagram as text**

1. Collector / account session / key A → Read-only checkpoint endpoint
2. Witness / pinned collector key / own key B → Separate signed witness journal
3. Witness / pinned collector key / own key B → Read-only checkpoint endpoint (Request a check)
4. Read-only checkpoint endpoint → Witness / pinned collector key / own key B (Signed answer)
5. Witness / pinned collector key / own key B → Channel with signed TGW1 posts (Bot API / own token)

The witness records rollback, a different head at the same count, changed keys, invalid answers and missing responses. A larger count alone does not establish that every earlier record remains unchanged; compare the export with retained checkpoints. A witness on another host avoids sharing the collector's host outage; a separate operator gives additional independence.

The witness attests to the collector's reported journal state. Use a controlled delivery test to measure which Telegram actions reached a collecting account. See [witness setup](https://phishdestroy.github.io/TgWitness/docs/reference/witness/).

## Test delivery against known actions

Use a controlled group, distinct collecting accounts and a fresh marker. Send, edit and delete deliberately, checking capture between stages. Define the expected actions and a cutoff before inspecting the results.

R = |observed∩expected| / |expected| Δ t = treceipt - taction

Only matched expected actions count; duplicate receipts do not increase the numerator. The denominator must be nonzero. A missing receipt has no measured delay. Document clock uncertainty; use your own controlled deletion action time, because Telegram does not provide the exact deletion time. A result such as 5/6 (83.3%) describes the test actions, not the completeness of all Telegram traffic.

## Pick a workflow

The [complete investigation walkthrough](https://phishdestroy.github.io/TgWitness/docs/reference/investigation/) follows an incident across a channel, group, bot and private chat:

1. On a dedicated collecting account, enable whole-account Investigation mode and inventory accessible chats. Use selected chats or a folder for a main account.
2. Acquire journal snapshots, per-chat full history and preserved attachments.
3. Keep live changes and any deliberate panel interactions with their receipts.
4. Follow numeric sender IDs, reply relationships, repeated destinations and file hashes through cited records and people profiles.
5. Add source-linked notes and collections in Case Board. Reconstruct a cross-chat timeline with both timestamps and explicit gaps.
6. Compare other account workspaces while keeping their origins and keys separate.
7. Assemble and verify the signed journals, profiles and history exports with case notes.

The website's `/docs/cases/` guide includes an interactive case map and variants for bot disputes, removed messages and participants changing names. Case Board keeps notes and collections within a workspace. Group exports collect separate workspace packages; cross-workspace correlation and a combined timeline remain analyst work.

[Completed validation and remaining work](https://phishdestroy.github.io/TgWitness/docs/reference/verification/) · [Export and verify](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#investigation-handoff) · [Start with one account](https://phishdestroy.github.io/TgWitness/docs/reference/quickstart/)


---

# Report configuration and verification

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/

Report filters, eight designs, contents presets, saved change histories and the assessment included in signed exports.

Turn selected observations into a readable account of the case: its question, scope, saved changes, charts, findings and source references. Each report gives the recipient a way to check the delivered material and inspect its collection coverage.

The **Basis of trust and limitations** section appears in journal, handover, chat, account and sharing reports. Journal and handover PDFs use the same assessment as their signed `report.json`. ZIP manifests carry `case_assessment` in the signed manifest. This assessment travels with the exported material. The original observations retain their existing signatures.

## Document formats and reading order

### Report studio

Open **Exports → Configure and preview**. Work through **Data → Design & contents → Preview**:

1. Use the whole workspace or choose chats, authors, inclusive UTC observation dates and event types. Load the catalog to search chats and authors, or enter their Telegram IDs. Author filters match recorded sender IDs; a deletion notice without a sender does not match an author filter.
2. Pick a page design, then choose charts, participant labels, the transcript and your written findings. Changing the design keeps these choices.
3. Build the preview. It shows actual counts, activity, participants, sample records, saved changes and missing message-number ranges. Changing a choice marks the preview out of date. Save before downloading HTML, signed PDF, signed JSON or the evidence ZIP.

The data preview counts the complete stable journal prefix, not an initial sample. Only displayed sample rows and long lists are bounded; their omitted counts are shown. A later export takes a fresh stable snapshot, so ongoing collection may increase the figures. Scope, counts and source identity are included in the signed report. Opening or previewing the form does not save it.

**Choose the recipient's copy.** Charts and the transcript use the selected records. Integrity, custody and coverage describe the full source journal. The evidence ZIP contains its original records and attachments. Use [a minimized handover](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#handover-extract) when a recipient should receive only selected, permitted data.

### Read edits, deletions and missing IDs

An edit shows the saved **Before** and **After** text and highlights the changed words. A deletion shows the last version saved before the notice. If no earlier content was captured, the report says so. When you select only edits or deletions, the preceding versions remain available as explicitly labelled context outside the filters. Unrelated messages are not added to these histories.

**Unobserved message IDs** are gaps between known numbers in the chosen chats and date-derived ID span. Every known source record is checked before declaring a number unobserved: filtering out another author, an event type or a date cannot create a false gap. Neighboring saved messages are labelled as context. A missing number does not establish that a message existed or was deleted; deletion notices and unsuccessful rechecks remain separate event types.

### Choose a design

Eight page designs are available for journal and single-chat HTML and signed PDF reports. They use the same records and calculations, with different covers, typography, chapter headings, tables and spacing.

| Design | Reading style |
| --- | --- |
| Classic | A traditional dossier with a dark cover and numbered sections. |
| Editorial | A framed serif title page, wide margins and a narrow chapter rail. |
| Briefing | A compact cover with a navy spine, short headings and close-set tables. |
| Analytics | A survey-style cover, modular chart plates and monospaced figures. |
| Technical | A ruled register, numbered reference rail and precise comparison tables. |
| Overview | A panoramic cover, generous spacing and prominent summary figures. |
| Reading series | A section rail and grouped chapters for findings, scope, changes and the observation journal. |
| Ledger & margin | Numbered chapters with a wide margin, exact chart tables and a separate message transcript. |

The design is saved per workspace and recorded in the signed export manifest. HTML works offline, supports light and dark themes, and adapts to narrow screens and right-to-left languages. Native PDFs use bundled fonts; the Editorial design includes Noto Serif under its bundled SIL Open Font License. Reading series and Ledger & margin also apply to account overviews, account chats and sharing copies.

Chinese, Japanese and Korean PDFs additionally need a suitable font on the server, such as Noto Sans CJK, installed system-wide or placed in `TGWITNESS_FONT_DIR`. When it is unavailable, the ZIP keeps the HTML and JSON reports.

These two designs include a readable journal without JavaScript. For large exports this view contains up to 500 whole records within an 8 MiB input budget; the report labels the limit and links to the complete viewer and source records. The account directory and relationship index describe that same reading sample, not all participants. Full-journal charts keep their separately stated scope.

### Choose the contents

| Contents preset | Included by default |
| --- | --- |
| Case dossier | Activity, observation times, participants, chats and the record transcript. |
| Briefing | An activity overview without participant rankings or the transcript. |
| Activity review | Activity, observation times, participants, chats and composition, with source references and exact figures. |
| Custom report | Your own combination of charts, transcript and previews. |

Changing a preset keeps your design, case details and written analysis. Integrity checks, coverage, limitations and verification instructions remain in every design. Source records in the ZIP stay unchanged when a chart or transcript is hidden.

The optional **Examination notes** contain the question, method, findings and conclusion written by the report's author. Cite the source file and record numbers in the findings. The signature preserves these authored statements alongside the report; source observations and the author's interpretation remain identifiable. Minimized handovers omit these private notes and full-journal charts. Chart and examination choices apply to journal reports.

Select activity over time, the UTC weekday/hour heatmap, participant rankings, chat rankings and record composition. Choose 5–30 ranked groups and neutral participant aliases or account IDs. Unknown senders and the remaining participants are separate rows. Aliases affect charts only; source records still contain their identities.

The design preview updates from the unsaved draft using production cover, examination and chart components, limited to matches within the first 50,000 source records. The data preview below calculates the complete selection. It is explicitly unsigned and does not persist edits. Cover and Charts buttons switch its section. This is not a complete PDF preview. **Save report settings** applies the choices to future exports; existing signed files are immutable. PDF uses the chosen cover, typography, chapter layout and the same selected aggregates as HTML and signed JSON.

Trust assessment, coverage limitations and verification instructions stay present. Hiding charts or the readable transcript does not remove authoritative source rows from the ZIP. Disabled chart series are omitted from the analytical JSON; use a minimized export to restrict disclosure of source records.

Data-selection filters apply to journal reports; account and sharing exports retain their own acquisition and disclosure scope.

Shared design/chart preferences are frozen into new chat/account exports and account sharing previews. Account/sharing language and privacy settings remain independent; private case and examination notes are not copied into these exports. Account and sharing reports remain HTML protected by their signed archive manifest. Journal, minimized journal handover and single-chat kits also provide signed PDFs.

### What the charts count

Journal activity and heatmaps count new, historical, recovered, edited, deleted and missing-on-recheck **observations**, by collector observation time in UTC. Heartbeats and attachment receipts are excluded. Participant rankings count only new, historical and recovered message observations: a sender is not declared to be the editor or deleter. Repeated observations can describe the same Telegram message.

Journal analytics retain counts by kind, first/last record references and the source `events.jsonl` SHA-256. Figures include exact values in HTML and PDF. Daily buckets switch to months beyond 366 recorded days; graphs combine these into at most 36 equal-width intervals. More than 100,000 distinct identifiers or 1,200 months marks the affected chart unavailable, while exact overall counts remain available.

Snapshot and account-sharing charts count only included non-service message rows, using their recorded message time. Sharing aggregates are calculated after redaction and filtering. These charts use at most 90 equal-width UTC date intervals and retain up to 10,000 grouping values; excess counts are explicitly declared and reconciled. The last interval may be shorter. Unknown or naive dates do not enter time charts.

An empty interval means no included observations; consult coverage for gaps. These charts describe saved activity. Unknown senders remain a separate category, and each check is reported individually.

When included, `analytics.json` is protected by the archive's signed file hashes. Journal `report.json` embeds the same selected aggregate. Signature verification detects changed bytes. To check the figures, recompute journal aggregates with `report_analytics.Analytics` and `selected`, or snapshot aggregates with `snapshot_analytics.collect` and `project`.

From a source checkout, build all eight designs listed above from the same fictional journal:

```
python tools/build_report_styles.py --output test-results/report-styles
```

Open the resulting `index.html` to compare complete HTML reports, signed PDFs and ZIPs. Every design uses the same source journal. Use a new output directory for each run so previously signed examples are preserved.

![Fictional HTML dossier](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

The HTML opens with a case cover and key figures. The numbered evidence map links to each finding, its supporting facts, limits and independent review. Searchable records and stable record references remain available in the offline viewer. The design adapts to narrow screens, both themes and browsers without JavaScript.

The signed PDF has a dedicated A4 cover, report reference and QR, an executive summary, an evidence map, numbered findings and document bookmarks. Its page headers and footers identify the report. A QR identifies the material; it is not an independent verification result. Browser printouts are separate from this cryptographically signed PDF.

The observation timeline places recorded observation periods and interruptions on the same UTC axis. Empty space is not inferred coverage; the detailed tables retain the exact intervals. The ZIP contains the readable reports, signed JSON, source records and verification instructions.

Generate a fresh, fictional English/Russian/German dossier with the development environment installed:

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Each language directory contains `report.html`, `report.pdf`, `report.json` and `dossier.zip`. Existing sample directories are never overwritten. No Telegram account, external timestamp service or network connection is used to create it.

![First three pages of the fictional signed PDF](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## Reading a concrete case

For a journal of 1,200 entries with a validated timestamp at entry 1,000, the report identifies 200 later entries outside that timestamp's bound. This is an upper bound on the existence of a checkpoint, not proof of each message's send time. If three other timestamp files fail validation or cannot be validated, they are counted separately and cannot supply a positive conclusion.

A usable timestamp must satisfy all of these checks: its imprint matches the checkpoint, its signature chains to a trusted TSA root at the stamped time, and the checkpoint's signature, key, count and head match the exact journal prefix. Merely parsing a timestamp or having an OTS receipt is insufficient. The reader must independently choose the trusted TSA root and repeat verification. OTS needs its own Bitcoin confirmation check.

| Report status | Meaning |
| --- | --- |
| Checked during export | The exporter performed the stated check; independent repetition is still needed. |
| Recorded; review required | The underlying observation or operator statement is recorded; it is not independent confirmation. |
| Not included in this copy | The copy has no supporting artifact for this claim. It does not say none exists elsewhere. |
| Not independently checked | The report does not supply an independent verification result. |
| Incomplete or unavailable | Material or a required check is missing, incomplete or unsuccessful. |

Review each check separately, alongside the recorded collection coverage.

## What a strong configuration must preserve

1. Before relying on collection, retain the collector's key fingerprint through a separate trusted channel. Compare that reference with the export's signing key.
2. Retain independently timestamped checkpoints and, where used, a witness journal outside the collector's administrative control. Compare them against the exported journal to check its earlier boundaries.
3. Record acquisition scope, gaps, filters, limits and changes in collection. Explain missing periods relevant to the actual claim, keeping unobserved message IDs, deletion notices and unsuccessful rechecks distinct.
4. Preserve original ZIPs and their hashes. Record each holder, transfer, date and purpose. Retain the attributed operator statements and case notes with them.
5. For confidential VMs, preserve and independently verify the quote, challenge, Intel certificate chain, measurements, exact source and key-handling conditions. Keep the attestation verification result with the reviewed artifacts.

See [verification scope](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope) for the trust assumptions and the separate assessment of source claims, identity, time and collection coverage.

## Recipient review

Use a trusted installation of TgWitness and an independently obtained fingerprint:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

The witness ZIP must come from an independently trusted source; preserve its key and provenance too. Retain the commands, tool version, outputs, reviewed input hashes and unresolved questions. Beacon verification is a separate online check; the report renderer never contacts a service merely to display a report.

For a dispute over a particular message, cite the archive reference, authoritative file and record reference, then describe the relevant time bound, coverage gaps, selection and corroborating material. For a sharing copy, also review the recorded transformation and its references to the source archive. Private filters and identity mappings stay outside its public assessment.

Verification of the signed PDF detects changes to covered bytes. Keep the original digital file and verification result alongside any screenshots or printed reading copies.


---

# Account export

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/account-export/

Export what an account can read now: scope, resumable jobs, a signed archive and minimized sharing copies.

As the installation administrator, choose **Start here → Export my account**, or **Exports → Telegram account → Configure account export**. Sign in if needed, review the scope, and explicitly start the export. Continuous observation is not required. **Saved observations** is a separate export of the existing journal; its ZIP includes all sources regardless of journal filters. Every workspace has its own jobs, signing identity and storage. Issued panel access, including an unrestricted ordinary export grant, cannot open these account-wide routes.

Sender and text filters expand under **Filter by sender or message text**. **Account data & connection method** contains optional account categories and the Takeout/regular-session choice; its summary shows the active choices even when closed. Closing these sections keeps their settings. Export and report drafts remain in the current panel session while changing views; they are not saved through a browser reload. Existing jobs remain reachable from either export choice.

This workflow exports data currently accessible to the connected account. The default uses [Telegram Takeout](https://core.telegram.org/api/takeout); it is not a backup of unavailable or deleted Telegram data. Secret Chats, inaccessible history and earlier edits are not recovered. Telegram can impose a waiting period before Takeout starts. The panel displays that wait; it does not silently switch transport. The explicit regular-API option has different coverage and records unsupported categories.

## Choose what is collected

| Setting | Meaning |
| --- | --- |
| Purpose | Record why this acquisition is needed. Do not put unnecessary names or sensitive case details here. |
| Report language | Choose the language of the readable report's labels. Original message text remains unchanged; untranslated template labels use English. The language is fixed with the signed job options. |
| Chat kinds / chat IDs | All selected kinds, or just the listed chats; Saved Messages belongs to private chats. Archived chats are separately selectable. |
| Dates | UTC. The panel's From and Through calendar dates are both included. The API uses inclusive `from_utc` and exclusive `to_utc`; the panel sends the start of the day after Through. An empty bound leaves that side unrestricted. |
| Sender IDs | Only messages by the listed senders; an empty list includes all senders. |
| Text contains | Case-insensitive literal phrases, matched with OR. Sender/date/own-message conditions combine with AND. |
| Own messages | Keep only outgoing messages. |
| Media types | Select attachment categories, or clear all to avoid downloading message files. |
| File / total media limits | Per-file MiB and total downloaded-media GiB. Text, receipts, readable reports and ZIP overhead require additional disk space. |
| Account categories | Profile, contacts, profile photos, stories, session metadata and other Takeout data have separate controls. |

The **Minimize collection** preset disables files and account metadata. Sender/content filters apply before retained message pages and media downloads. Telegram still transmits API history pages containing messages needed to evaluate those filters: filtering is not a promise that unselected messages never enter process memory. Other ongoing observation in the workspace has its own scope and retention settings.

Profile-photo history and stories are not selected by default. Disable profile and contacts as well when the case needs messages only. If attachments or metadata are unnecessary, excluding them during acquisition avoids retaining another private copy in this export.

## Resume, coverage and verification

Each job freezes its options and account identity. Inventory and captured pages are signed; page receipts record hashes, cursors, times, attachment outcomes and their preceding receipt. Only committed pages advance progress. Restart/resume checks those records before continuing. A changed account, changed signed page or inconsistent receipt chain is rejected. Options cannot be edited halfway through an acquisition: start another job for another scope.

Pause releases the running account operation. Restarting the application leaves unfinished work available for explicit resume. An expired Takeout session requires an explicit resume; changing Telegram split ranges can require a new acquisition. Resume retains previous observations, so a long-running export is not one atomic snapshot. Other account-changing operations and conflicting exports are blocked during acquisition. Wait for packaging to finish before deleting a workspace.

Resume verifies already captured content before continuing. Large archives on slow storage can exceed the configured **Parameters → Panel action timeout** (120 seconds by default). Increase that setting before retrying; cancellation/storage interruption leaves a paused job, and failed integrity checks leave a failed job with an explanation. Verification must finish or stop safely before its files can be closed. No large-account throughput claim has been validated by the synthetic checks.

The panel distinguishes a completed selected scope from a partial archive, and records omissions and failed reads. Deliberately excluded files are different from failed or unavailable files. Inspect coverage even when integrity verification succeeds. No local reader can prove Telegram returned every message that ever existed.

Finished ZIPs remain available for repeated and HTTP-range downloads. An account archive contains `manifest.json`, `manifest.sig`, signed `job.json`, `inventory.json`, `receipts/`, authoritative `data/*.jsonl`, selected `media/`, readable HTML and a verifier. Pin the collector fingerprint through an independent channel, then verify using a trusted installation:

```
python -m tgwitness.verify account-export.zip --fingerprint TRUSTED_SHA256
```

For archives whose expanded contents exceed 4 GiB, set an explicit adequate `--max-gib`. The panel verifies its authenticated, completed local archives using their declared expanded size and published ZIP digest; the external CLI keeps its independent size limit. Verify before opening the readable HTML. The archive's bundled verifier is convenient, but a verifier obtained independently avoids trusting executable code delivered with the evidence.

The Ed25519 signature and SHA-256 hashes detect changes after the collector committed the relevant bytes. They do **not** prove that Telegram signed those messages, that the collector operator was honest, that the account's history is complete, or that a court will accept the material. Capture times use the collector's clock. Independent timestamps and independent acquisition provenance must be evaluated separately.

## Prepare a disclosure for a lawyer or another recipient

After downloading a finished export, keep the original ZIP and open `index.html` from an extracted copy. The report explains its scope, available coverage and limits. Its record references combine the archive reference, document path and record number, so a recipient can locate the same entry in the HTML or printout. For a worked example, [open the fictional report](https://phishdestroy.github.io/TgWitness/demo/report/).

From a finished account export, choose **Prepare a sharing copy**. This builds a separate signed derivative. The source ZIP remains unchanged and private; do not send it together with a minimized derivative unless the recipient is authorized to receive its full contents. Choose its report language separately. Changing the language or any selection setting requires another preview before creation.

1. Enter the disclosure purpose and select dates, sender IDs and literal text criteria.
2. Choose whether to keep identities, reveal only listed participants, or pseudonymize everyone. In either pseudonymized mode chat IDs/titles and message IDs are also replaced. Pseudonyms are stable inside one disclosure and change between independently prepared disclosures.
3. Keep message text, omit it entirely, or add literal names/phrases to mask. In private modes the tool also masks known hidden sender names and alternate usernames, whole-token sender IDs, direct-chat names, links, email addresses and phone-like strings. Known-name matching handles Unicode case folding, including `Straße`/`STRASSE`. Generic group/channel titles are not automatically removed from message text. If the known-identity masking limit is exceeded, narrow the source export or omit text; the tool refuses to silently skip later names. These are best-effort rules, not general anonymization.
4. Leave files excluded unless the recipient needs them. Included originals retain their pixels, audio, text and metadata. They are **not** anonymized by the tool.
5. Preview the counts, warnings and sample transformed messages, then explicitly confirm creation. Samples are limited to 12 messages and 2,000 text characters each. This is a sample, not a full review of the result. Changing settings requires another preview. A preview expires after 15 minutes and is bound to that administrator session and exact original ZIP; it cannot be reused after creation. A new preview invalidates the previous one for the same job and session.
6. Inspect the complete resulting `index.html` and `messages.jsonl` locally before handing it over. If it reveals unnecessary information, create a new disclosure with stronger exclusions. Do not edit the signed ZIP in place.

The minimized format omits structured account profiles, contacts, avatars, sessions, stories, raw Telegram objects, forwarding headers, reply quotations, contact cards and location metadata. It excludes the original JSONL files, private filter settings, pseudonym key and identity map. Selected text, explicitly retained identities and included files can still contain the same names, IDs or phrases used in those filters; they need separate review. The private policy and pseudonym key are retained encrypted in the local vault for the job; deleting the job clears its associated private disclosure records. The public policy records filter counts rather than filter values. The stated purpose is public in the manifest and HTML: explicit private criteria and, in pseudonymized modes, known hidden identities are masked there too, including when message text is omitted. Keep the purpose free of unnecessary personal details; unknown identifying context can remain.

Its manifest binds the derivative files, public policy and original ZIP's hash. Verification can establish integrity and, if the source is supplied locally, matching source linkage:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Source linkage does not independently prove that the transformation selected every required item or removed every identifying detail. Original plaintext is not embedded as a proof. A fresh review is needed for that judgment.

## Data protection and the hosted Capture preview

These controls support purpose limitation and data minimization; they are not an automatic legal compliance check. [GDPR Articles 5 and 25](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) address those principles and protection by design/default. A lawful basis, necessity, special-category conditions where applicable, retention, security and recipient access still need a decision appropriate to the case. A litigation purpose alone does not make every disclosure lawful. Pseudonymized data generally remains personal data; see the [EDPB explanation](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisation-pseudonymisation_en).

Free text, dates, rare events and combinations of facts can identify people even after names are removed. Prefer text omission where message content is unnecessary; inspect the full derivative where it is necessary. Keep the source and vault protected, agree retention and sharing with the responsible person, and record which exact ZIP was handed over.

This feature runs in the local panel. The separately published [hosted Capture preview](https://phishdestroy.github.io/TgWitness/docs/capture/) uses a pinned disposable runner and its own attestation policy. Local collector signatures do not inherit that runner's provenance. A change here does not update an approved remote workflow or its trust pins; hosted full-account capture needs a separately reviewed and published collector/workflow pair and live runner acceptance. No hosted deployment or real Telegram account acquisition is claimed by local synthetic tests.

[Evidence format](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/) · [Case reports](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/)


---

# Evidence format

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/evidence/

Contents of the signed ZIP, record kinds, process receipts, people profiles, off-site copies and offline verification.

TgWitness preserves account-visible Telegram observations in a signed journal. Recipients can verify the saved records, attachments and reports against a trusted collector key, then compare the journal with an independently retained checkpoint. This page describes the formats, the checks and the material to keep for handover.

## What is signed

| Material | Protection | What to retain |
| --- | --- | --- |
| Every journal observation, including operational events | SHA-256 chain and an Ed25519 signature per event | Original `events.jsonl`, the trusted key fingerprint, and a retained checkpoint |
| Evidence ZIP contents | `manifest.sig` signs the canonical manifest, which lists hashes of the content files | The complete ZIP, including its manifest and signature |
| Preserved attachments | SHA-256 and byte count in a signed `media.saved` event; file hash in the signed ZIP manifest | The original bytes inside the verified ZIP |
| Checkpoint | Ed25519 signature over journal length, head hash, public key, and creation time | An independent copy retained before a disputed change |
| Run receipt | Separately signed collector measurements; also included in a signed `process.started` event | The receipt and associated journal; measurements are self-reported |
| Readable reports: `report.html` and its parts, `report.json`, `report.pdf`, `chat.pdf` | An Ed25519 seal per file over its content; the PDF also carries a standard PDF signature (see [Readable reports](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#readable-reports)) | The file as received and the trusted key fingerprint; the ZIP it describes |
| Standalone CSV | No standalone cryptographic signature; event hashes alone are insufficient | Use the exact copy inside the verified ZIP for integrity checking |
| Screenshots, printouts, or PDF produced by a browser | No TgWitness signature on the derivative | Keep the original verified package and document how the derivative was made |

The collector verifies journal signatures before generating every export format. Readable HTML and PDF reports carry their own seals; standalone CSV is checked as part of a signed ZIP. Keep the ZIP to retain the attachment bytes and manifest, and a separate checkpoint to check the journal against an earlier boundary.

## Investigation handoff

1. Record the case reference, operator, numeric Telegram account ID, selected sources, collection policy, and collection period in your case notes. TgWitness preserves observations and supports source-linked notes and collections in [Case Board](https://phishdestroy.github.io/TgWitness/docs/reference/case-board/). Keep transfer and custody records with your case materials. Check the intended collection setup with the [live acceptance procedure](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
2. Retain the workspace's public-key fingerprint independently before relying on its exports. Save signed checkpoints outside the collector during collection. Record interruptions and the limits of the account's visibility.
3. Export a **signed ZIP** and retain the signed run receipt. Use a checkpoint at or before the exported journal boundary. A later checkpoint can correctly reject an earlier export as too short. Exports include the full workspace journal, regardless of panel filters; review the material before sharing it.
4. Have the recipient verify the ZIP with a trusted copy of the verifier and the independently supplied fingerprint/checkpoint. From a trusted checkout with its Python environment active:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   Successful output reports `key_pinned: true` and `checkpoint_checked: true` when both inputs are supplied and accepted. Preserve the verification result.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. Record the archive's SHA-256, export boundary, transfer date, sender, and recipient in your custody record. Keep the original package intact and work from copies. Share evidence files rather than the application's private data directory, which also contains account sessions and signing secrets. For transfer, an export can be put into a password-protected AES-256 ZIP. The password only protects confidentiality and is not stored; the recipient extracts the archive and verifies the signed export inside, which is unchanged.
   2. If independent time anchoring is required, follow the [RFC 3161 procedure](https://phishdestroy.github.io/TgWitness/docs/reference/timestamp/) and retain the request, checkpoint, trusted CA information, and verified authority response. Preparing a request alone does not obtain a timestamp.

Successful verification establishes integrity relative to the trusted collector key and retained boundary. See [verification scope](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope) for the trust assumptions and [validation results](https://phishdestroy.github.io/TgWitness/docs/reference/verification/) for the checks performed.

Notifications sent through Apprise help operators follow workspace and chat activity. They contain names and counts; excerpts of deleted and edited messages are optional and off by default. Use the signed journal and exports for the retained record. With a workspace proxy, notifications use the same route; services that cannot use it, and MTProxy routes, are refused.

## Handover extract

A signed ZIP carries the whole workspace journal. When a court, a lawyer or an abuse desk needs only some chats, a period or certain people, **Exports → Handover extract** prepares a minimised copy (`tgwitness-handover-v1`) according to the selected disclosure rules. The operator states the purpose and chooses the chats, an optional period (UTC), the people the extract is about, what happens to everyone else (shown, replaced by pseudonyms P01, P02… or left out), which message texts stay, which attachments and profile photos are included, and whether phone numbers and e-mail addresses in texts are masked. The purpose and these rules are in the signed manifest and in the report; the journal records `handover.exported` with the access that prepared it and the file's SHA-256, not the contents.

`verify.py` checks an extract in two ways. A record shown unchanged is verified in full: its content against its hash, its Ed25519 signature and its link to an included predecessor. A minimised record keeps the original hash and signature, so the signature still verifies, but the withheld fields cannot be recomputed from it; the record names what was withheld and the report marks it. The manifest names the journal length and head with the collector's signature over that head, and counts the records left out; `coverage.json` describes the chosen chats. Names inside file names are not detected. Review the final files before sharing: free text, file names and selected attachments can still identify people. Keep the full signed ZIP: the extract is a disclosure, not a replacement.

## Readable reports

Signed evidence, handover and chat ZIPs carry readable HTML and JSON reports, plus PDF when the required fonts are available, in the selected report language. Each report is sealed with the workspace's Ed25519 key and can be verified separately: `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]`.

- `report.html` / `chat.html`: the seal statement (`tgwitness-report-seal-v1`) closes the file and signs the SHA-256 of every byte before it. Long journals and chats are split into parts of a configurable size (Report settings, 500 to 100,000 records; 5,000 by default): `records/records-0001.html` or `messages/messages-0001.html`, each sealed with its number, range and the total, and listed with its SHA-256 in the signed manifest. Runs of collector heartbeats are shown as one line unless Report settings list them one by one.
- `report.json` (`tgwitness-report-json-v1`, keys `format`, `report`, `seal`): the seal signs the SHA-256 of the canonical JSON of `report`, so the facts can be read by case systems and scripts and a selection for data protection can be made from them while the signed file stays whole.
- `report.pdf` / `chat.pdf`: a formal document for printing and filing, signed twice over the same bytes, the whole file except the signature value (`/ByteRange`). The standard PDF signature (`adbe.pkcs7.detached`, CMS with SHA-256 and ECDSA P-256) uses a self-issued document-signing certificate kept in the workspace vault; its subject serial number is the Ed25519 key fingerprint. The Ed25519 seal travels inside the CMS as the unsigned attribute `2.25.240684792623320047764573196045913242332` and names the certificate's SHA-256 with `"content": "pdf-byte-range"`, so the Ed25519 key vouches for the certificate. A PDF reader shows whether the file changed after signing and calls the signer unknown until the certificate is trusted; compare the Ed25519 fingerprint instead. Chinese, Japanese and Korean PDFs need a font on the server (or in `TGWITNESS_FONT_DIR`); without one the ZIP carries the HTML and JSON reports only.

In a channel or supergroup Telegram numbers messages 1, 2, 3… in order. A chat export lists the first and last number, how many are present and every run of absent numbers in `message-ids.json`, the manifest and the `chat.json` header, and marks each gap where it falls in the transcript. `verify.py` recounts them from `chat.json`. An absent number is a message Telegram did not return (deleted before the export, or not visible to the account); in private chats and basic groups numbers are shared by all of the account's chats and gaps are not counted.

After reading the history, the export asks Telegram for every absent number again, by number (`channels.getMessages`, up to 10,000 numbers). The result is in `message-ids.json` and the report. An empty answer means Telegram has no message under that number for this account; it does not say whether the message was deleted or was never visible to the account. A message Telegram does return then was missed while reading and is added to the export, marked `found_on_recheck`.

Every report opens with **In brief**: one paragraph, then what the material shows and what it does not (who is behind an account, completeness of delivery, deletions before observation, clock time without a timestamp). The page's own seal stamp turns amber when the browser has checked the seal's signature, not the page: a browser does not give a page its own bytes. It turns green only when the reader drops the file into the check at the end of the page and every byte matches, and only if the page shown is that file; otherwise it turns red.

Each report names the program exactly: the git commit when the collector runs from a checkout or the installer sets `TGWITNESS_COMMIT`, and the SHA-256 of its source files (`source_tree_sha256`, the canonical JSON of path → SHA-256 of every `.py`, `.js`, `.css`, `.html` and `.svg` file in the package), which a checkout of that commit reproduces unless files were changed. The Telegram client is named with its library, API layer and data centre. When observation starts and when a chat export begins and ends, the collector asks Telegram for its time (`updates.getState`, whole seconds) and records Telegram's time minus the collector's clock, with the uncertainty from the round trip; the reports show these measurements under Chain of custody. A chat export also records when it read the history, apart from the dates of the messages.

### Offline report viewer and archive guide

Extract the complete ZIP before opening `chat.html` or `report.html`. The viewer provides search, filters, participants, indicators, record details and JSON/CSV selections without a server. Keep `viewer/` and `media/` next to the report. Selections are derivatives: use `verify.py SELECTION.json
--evidence ARCHIVE.zip` to compare them with the signed archive. The verifier checks the report ID, signing key, archive boundary and every selected item; edited, missing and duplicate items fail. Selection notes and creation time remain unsigned metadata.

Current archive exports store viewer chunks in `viewer/*.html`. Each chunk is loaded in a sandboxed frame with scripts allowed but **without** same-origin access, and posts its JSON text to the report. The report checks the message source and its SHA-256 against the signed descriptor before display. The report's own CSP permits only its hashed application script. Missing data can be recovered by choosing the matching ZIP in the Check tab; data read from the ZIP is parsed without execution. Earlier exported reports keep their own embedded viewer and remain verifiable.

Message-number gaps are shown only for a complete, unfiltered ascending chat feed. Hiding a category or failing to load a data chunk must not turn an omitted row into evidence of a missing message. Search highlights operate on plain text before HTML escaping, preserving literal markup.

The browser checks manifest signatures, the report ID and key, and all listed file hashes. It rejects ambiguous or malformed ZIP structures, duplicate names and unsafe paths, and caps files at 256 MiB and declared total contents at 4 GiB. Use the standalone verifier for larger archives. This browser check complements the verifier's checks of journal chains and data semantics.

`README.txt` contains a start guide, an aligned file inventory, verification instructions and data format notes in the report language, followed by a complete English guide. `SHA256SUMS` covers the files listed within it, excluding itself, `manifest.json` and `manifest.sig`; the signed manifest also covers `SHA256SUMS`. Keep the original ZIP unchanged and save working files outside the extracted folder. PDF reports include section bookmarks and case/report identification on later pages.

Report settings are saved per workspace. The report language can follow the panel or be fixed; an explicit language on an export request overrides that choice for that export only. Every panel language is accepted, including the four right-to-left languages.

The journal transcript switch controls its HTML viewer and PDF transcript. Full record JSON is an HTML detail option: when enabled, the viewer carries the exact exported record, including a minimised record in a handover. Disabling it does not alter the authoritative journal file. Photo previews apply to both chat and journal HTML. Consecutive heartbeat runs can be collapsed without removing records; expanding long runs loads their rows incrementally.

`part_size` is the maximum item count per viewer data file (500–100000), and the maximum transcript size included in a PDF. Viewer chunks also split at a 16 MiB data budget. Longer PDF transcripts are omitted with an explicit pointer to the signed source files and HTML viewer. A standalone HTML report embeds at most 20000 items or 32 MiB of item data; once exceeded, it releases those items and directs the reader to the archive. These display limits never truncate the signed source files. The PDF font setup combines CJK fonts where needed: a Chinese font alone may lack Korean Hangul.

### The chat at export time

A chat export records what Telegram said about the chat when the export began: Telegram's own labels (`scam`, `fake`, `restricted` with its reasons, `verified`), usernames, description, member and admin counts, the linked discussion, content protection, whether new members see earlier messages and from which message on this account sees the history (`available_min_id`), the date of message 1 when it is the chat's creation, and the SHA-256 of the chat photo (saved in `media/`). It records the exporting account's place in the chat: role, join date, who invited it and, for an admin, its rights. A request Telegram refuses is named instead.

When the exporting account is an admin, the export reads the chat's admin log (Telegram keeps about 48 hours) into `admin-log.json`: deletions and edits with the content and the account that acted. It is the one record of a deletion that names who deleted.

### Indicators

The reports list, and the archive carries as `indicators.csv`, `indicators.stix.json` (STIX 2.1) and `indicators.misp.json` (MISP event), what an abuse desk can act on in the recorded messages: links and domains (also hidden behind text, in buttons and in link previews), cryptocurrency addresses, Telegram usernames and invite links, phone numbers, e-mail addresses and saved pictures. Bitcoin, Litecoin, Dogecoin and TRON addresses are listed only when their base58 checksum holds, segwit addresses when their bech32 or bech32m checksum holds and TON addresses when their CRC holds; EVM and Solana addresses are marked as not checked. Pictures carry SHA-256 and a perceptual hash (dHash, 64 bits) that recompressed or resized copies keep nearly unchanged. Reports write indicators so that they do not open by accident (`hxxps[://]example[.]com`); the files keep the values as they were. Every indicator is marked unknown and not for automatic detection (STIX `indicator_types: unknown`, MISP `to_ids: false`, distribution to the own organisation): being listed says that a message contained it, not that it is malicious. A link whose text shows a different address than it opens is marked in the report.

The PDF reports end with an examiner's declaration to sign by hand, a checklist for a notary or court expert, and a QR code (also on the first page) with the report ID, the key fingerprint and the SHA-256 of the authoritative data, so that a printout leads back to its archive.

## Event canonicalization

The hash input consists of exactly these fields:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

Serialize using Python-compatible JSON with UTF-8, sorted object keys, no ASCII escaping, no insignificant whitespace, and no NaN/infinity:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

SHA-256 of those bytes becomes the event hash. The signature is Ed25519 over the 32 raw hash bytes, then base64 encoded. The first previous_hash is 64 zeroes. Sequence numbers start at 1 and increase by 1. All events, including operational events, share one chain. There is no duplicate-delivery suppression: repeated observations are distinct receipts, not a claim of distinct Telegram actions.

Raw Telegram dates are ISO strings; binary fields become objects containing bytes_base64. Message text, entities, media descriptors, reply metadata, reactions, and service actions are retained in raw message metadata when supplied.

observed_at is the collector's UTC wall clock. source_at is a supplied Telegram date when available. Deletion notifications do not supply an exact deletion time, so source_at remains null. Transport reception order is not necessarily source-event order. History snapshots use older source dates but current observation times.

## Actor semantics

message.new actor_id is the message sender. message.edited has no inferred editor; payload.sender_id records the sender of the observed message. Deletion actor_id remains null. Membership service messages retain the sender and action type, without converting every removal into a voluntary leave. Raw participant updates retain actor_id as supplied. Reaction snapshots do not invent a change actor.

Deletion notifications for private chats and ordinary groups contain only message IDs. Those chats share one account-wide ID sequence, so an ID identifies a single message of this account. When a message with that ID was saved earlier in this journal, the deletion is recorded in that chat as message.deleted with payload.chat_resolution naming the method. IDs that were never saved are kept as deletion.unscoped with no chat_id; nothing is guessed. Channels and supergroups number messages per chat and are never matched this way. When the deleted message was sent by the observed account, payload.deleted_message_was_outgoing is true; the deleter is still not supplied.

## Coverage: continuity, gaps and unobserved IDs

Every signed ZIP carries `coverage.json`, the HTML report opens with the same summary, and `verify.py` recomputes it from `events.jsonl` instead of trusting the file:

- **Continuously observed from X to Y.** A period starts with `observation.started` and ends at a pause, a stop, a lost Telegram connection, a sign-out, a process start without an orderly stop, or more than three minutes without any record while observing (heartbeats are written every minute, so silence means the process stopped, froze or the computer slept). When the heartbeat interval is changed in **Parameters**, each heartbeat records it and the allowed silence becomes three intervals, never less than three minutes.
- **Gaps** list the time between periods with the reason. A gap still open at the last record is marked `not_resumed_by_last_record`.
- **Message IDs not observed.** For channels and supergroups, which number messages per chat, the IDs missing between observed ones are listed as ranges. They are reported as *not observed* — deleted, never delivered, or outside the saved history — never as deleted. Private chats and ordinary groups share an account-wide sequence, so gaps there mean nothing and are not listed.
- Chat-level gap notices (for example Telegram asking for difference recovery in one channel) are counted as notes; they do not interrupt global coverage.

When Telegram stops accepting the account, the `coverage.gap` record that ends observation carries `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended` or `not_authorized`) and the Telegram error; `verify.py` names the cause where the period ends.

Coverage describes what this collector recorded. It is not proof that Telegram delivered every update during a continuous period.

## Producer

The signed manifest of evidence ZIPs, chat exports, witness journals and the statement of people-profile files contain `producer`: software, version, project (PhishDestroy), homepage and source repository. The HTML report shows the same line, and `verify.py` prints it as part of what it verified. Archives made before this field existed verify as before and are reported as not naming a producer.

Each `observation.started` record also names the Telegram client that observed: its `api_id` (never the hash), whether that is a built-in public pair or the operator's own application, the client description sent in Telegram's connection request, and the kind of connection route with the IP mode (no proxy address or secret). The report and `custody.json` list every distinct client and route with when they were recorded, and the times no listed proxy answered and Telegram saw the server's address. Journals recorded before this say so.

## People profiles

A profile file (`tgwitness-dossier-v1`, JSON) is built on request from records already in the journal for one chat; nothing is fetched from Telegram and profile contents are never written to the journal (switching profiles on and off is recorded as `dossier.changed`). For every person with a saved message it lists name and username history, Telegram flags (bot, scam, fake, premium, verified, restricted, deleted) as seen at saving time, profile photo IDs, SHA-256 and perceptual hash (pHash, compatible with `imagehash.phash`) of the avatar from the local avatar cache with similar avatars, activity (first and last message, counts, edited and deleted shares, messages by UTC hour), who replies to whom, other chats in this journal where the person wrote, and mentioned wallets (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL; Base58Check addresses are checksum-validated), phone numbers, usernames and links, including links hidden behind text.

Every fact lists the journal records (`seq`) it comes from, and `record_hashes` holds the hash of each referenced record. The statement is signed with the workspace key:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

checks the signature, verifies the evidence export itself (signature, hash chain and files) and that every referenced record exists unchanged in that export of the same workspace. Avatar hashes are labeled as coming from the local cache (not journal records). Mentions are pattern matches — leads to check, not verified facts. Profiles are switched on per chat, can be exported as an AES-256 ZIP with a password, and are deleted when switched off or when the chat is removed from sources.

## Independent witness

A witness journal (`tgwitness-witness-v1`) and its channel posts are checked against an evidence export with `verify.py --witness … --channel …`; see [independent witness](https://phishdestroy.github.io/TgWitness/docs/reference/witness/).

## Manifest and checkpoints

manifest.json includes the format, export time, public key, fingerprint, journal length, head hash, scope, producer, limitations, and SHA-256 of every content member other than `manifest.json` and `manifest.sig` themselves. manifest.sig is the base64 Ed25519 signature over canonical manifest JSON. The verifier rejects unexpected/missing members, duplicate names, corrupt files, broken sequence/chain, invalid signatures, and mismatch with a provided checkpoint. It never extracts archive paths. It limits total declared uncompressed size to 4 GiB; `--max-gib N` allows larger archives made with a raised **Parameters** limit.

Obtain verifier code from a trusted checkout or reviewed independent copy. A verifier inside an untrusted archive is executable material supplied by that archive's author; its presence is a portability convenience, not an independent trust anchor.

A checkpoint signs a statement containing the public key, journal length, head hash, and creation time. The verifier can check that a later archive contains the same prefix. Retain a checkpoint outside the collector before a disputed change: an attacker controlling both archive and checkpoint can replace both.

## Verification scope

The signatures identify the collector key and protect the saved material. Pin its fingerprint independently to associate that key with the expected collector. Telegram updates are the input to collection; TgWitness signs its observations of those updates. The signatures are not signatures issued by Telegram or by message authors.

A retained checkpoint or witness record detects a changed earlier journal prefix, including a replacement signed with a copied collector key. Records fabricated before their first independent checkpoint require source corroboration: a collector key holder can sign new material. Keep signing-key access controlled and retain references separately.

Assess account visibility and delivery using coverage records and controlled tests. Use a verified external timestamp for independent time anchoring. A sender ID identifies a Telegram account; link it to a person through your investigation. Program receipts and cloud checks describe collector-reported measurements and deployment configuration. See [validation results](https://phishdestroy.github.io/TgWitness/docs/reference/verification/) for measured behavior and its scope.

## Attachments

Files are addressed by SHA-256 under media/. A media.saved event links a hash and byte length to a specific message event. Raw filenames are metadata, never local paths. Media bytes are downloaded asynchronously, so immediate deletion may prevent capture. Disabled collection, oversize/unknown-size files, download failures, and interrupted downloads are visible as outcomes. A process crash can leave unreferenced partial files; they are not included in exports.

The ZIP exporter verifies stored media against their names. JSONL, CSV, and HTML exports verify event signatures but do not carry media bytes. Derivative reports are conveniences; events.jsonl is the authoritative event representation.

A full chat export saves attachments within the workspace's attachment settings into media/, named by SHA-256. Each message record in chat.json names its file (`file`, `file_sha256`) or the reason it is absent (`file_status`), together with what the reader saw around the text: links behind the text, forward origin, bot buttons, signature, views and the auto-delete timer. `verify.py` checks that every named file is in the signed manifest under that hash.

## Durable collection and process receipts (0.2)

A media job and its message event commit in one transaction. The job stores the original TL message descriptor; the signed observation binds its SHA-256, account, and size policy. Recovery verifies that binding before downloading. It never fetches the current message and silently substitutes a newer attachment. Interrupted jobs are retried, while permanent failure remains an explicit outcome.

Each workspace has its own journal and signing identity. A process.started event includes a run ID, local clocks, dependency versions, source-file hashes, initial account/scope, and capture settings. Heartbeats include the run ID, monotonic time, and queue state. The process receipt can also be downloaded as a separately signed statement. File measurements are self-reported and are not trusted hardware attestation.

Automatic checkpoints are retained locally on startup, every five minutes while observing (**Parameters → Signed checkpoint every**), and on orderly stop. Startup verification and export compare the journal against the latest retained local checkpoint. This can detect a database rollback when the checkpoint survives; an operator controlling both can still replace both. Independent retention and external trusted timestamps remain separate requirements.

After a restart the saved Telegram update position is resumed (`catch_up_from` in `observation.started`) and missed updates are requested. A periodic recheck records `message.recovered` for missed messages and `message.missing_on_recheck` when Telegram no longer returns a saved message; the latter is not a deletion notice and names no deleter or time.

### Off-site copy and restore (S3)

The off-site copy (Exports, off by default) uploads journal segments, preserved files, checkpoints with their timestamps and finished chat exports to S3-compatible storage, encrypted with AES-256-GCM before upload under a key kept in the workspace vault; Object Lock retention applies when the bucket supports it. Without the downloaded key the copy cannot be read. Restore and verify with `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Restore requires an empty ordinary directory. Downloads and decrypted objects stay in private temporary storage until the entire journal and every retained checkpoint verify. Unsafe object paths, inconsistent segment ranges and journals shorter than a checkpoint are rejected; failed verification publishes no restored files. Retention checks compare the returned Object Lock mode and date with the deadline sent at upload (one second of rounding tolerance). An expired, invalid or shortened deadline does not count as verified. The status reports the sampled object whose retention was read back for that upload pass.

Copy progress is scoped to the destination and encryption key. Changing the endpoint, bucket or prefix starts a complete copy of the locally retained journal, media and checkpoints to that destination. Old unscoped progress is preserved but replayed once after upgrade. Historical chat exports already removed from the local outbox remain at their previous destination.

Missing or corrupt local media is reported as the pass's error and keeps the media cursor before it, so the file is tried again next pass; the files, checkpoints and exports after it are still copied. Restore checks all preserved-media references against decrypted hashes and recorded sizes. Identical overlapping journal segments from interrupted uploads are deduplicated; conflicting overlaps are rejected. Checkpoints created during an upload are deferred until their covered journal records have been copied, so a completed pass does not publish a checkpoint ahead of its journal.

### Streaming export snapshots

Streaming exports use a stable SQLite read snapshot. Its head may be older than the current live journal when download completes. A checkpoint created after that snapshot can correctly report that the archive is shorter; compare with a checkpoint at or before the exported prefix, not an arbitrary later checkpoint.

## RFC 3161 preparation and response verification (0.2)

Evidence mode (off by default) sends only the SHA-256 of each signed checkpoint to the listed RFC 3161 authorities and OpenTimestamps calendars, over the workspace route and never over MTProxy. Answers are kept in `checkpoints/anchors/`, exported, and checked by `verify.py` (`--tsa-ca` checks the TSA signature; confirm OpenTimestamps proofs with `ots upgrade` and `ots verify`).

The panel prepares a request archive containing canonical checkpoint.json bytes, a SHA-256 message imprint and random nonce in timestamp.tsq, checksums, and instructions. No network request is made. Preparation is not a trusted timestamp.

`python -m tgwitness.anchor verify` calls OpenSSL ts twice: once against checkpoint bytes and once against the original request. A trusted CA file is required explicitly; included certificates are not automatically trusted. Request checking is optional at the CLI, so retain and supply --request to check the nonce. The result states whether it was checked. The collector checkpoint signature and journal must still be verified separately with the trusted collector fingerprint.

Verification checks the response signature, checkpoint bytes and, when supplied, the original request under the specified CA trust. Revocation checks and long-term archival validation after certificate expiry are outside the current verifier. See the [procedure](https://phishdestroy.github.io/TgWitness/docs/reference/timestamp/) and [validation results](https://phishdestroy.github.io/TgWitness/docs/reference/verification/).

## Optional records in evidence mode: drand and Telegram devices

Two more records can run on the same passes as the timestamps. Both are off by default and take effect only while evidence mode is on: Extras → Evidence & backups → **More witnesses · optional**, or `"drand": true` and `"devices": true` in `POST /api/evidence`. One failing does not stop the other or the timestamps; the panel shows the latest result of each under the form.

**drand** (`beacon.drand`). Each pass writes the newest round of drand quicknet, the public randomness of the League of Entropy (a round every 3 seconds), into the journal: `chain`, `round`, `randomness`, `signature`, `round_time` and the `relay` that answered. A verified unpredictable round supplies a lower time reference for the subsequent hash-linked material. A verified timestamp on a later checkpoint supplies an upper time reference. These checks bound the linked material; collection coverage is assessed separately. The collector asks `drand.cloudflare.com` first, then the relays of Protocol Labs, through the workspace route, one request per pass.

`verify.py` checks that each randomness is the SHA-256 of its signature and that the round time is right, and reports the rounds, the longest stretch without one and how far behind drand the collector's clock was. It does not check the BLS signature. `--check-drand` compares the rounds with a Cloudflare relay and a Protocol Labs relay, all of them or a random sample of 100 in a long journal; a round that differs fails the verification.

**Telegram devices** (`account.devices`). Each pass reads the account's sessions with `account.getAuthorizations`, the list Telegram shows in Settings → Devices, and records it: in full when it changed since the previous pass, with the `added` and `removed` session hashes, otherwise only its count and SHA-256. Device model, platform, app and version, creation and last activity, country and region are kept; IP addresses are not, because evidence exports leave your hands. The collector's own session is active all the time, so only other sessions' activity counts as a change. `verify.py` reports how often the list was recorded and each new and ended session. It reads the list only while observation runs.

What they do not show: drand proves no more than the order of records against public time, and the device list is Telegram's statement through the collector, signed by the collector like every other record.

Tested on 1 November 2026: `tools/check_evidence_witnesses.py --live` wrote a real round from `drand.cloudflare.com`, exported the journal and confirmed the round with `drand.cloudflare.com` and `api.drand.sh`; the device list ran against simulated Telegram answers, not a real account.

**Cloudflare Gateway log** (`cloudflare.gateway_dns`). For a server that resolves through Cloudflare Gateway ([Gateway DNS](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)), each pass copies what Gateway logged since the previous copy: one record per window of at most three hours with `from`, `until`, the `location_id`, the server's `address` when one is set, and the `queries` as `[at, name, type, rcode, decision, colo]`, also when there were none. Set it under **Cloudflare Gateway log**: account, location, optional address and a read-only token (Account Analytics Read; Zero Trust PII Read to keep one address of a shared location). The panel checks them with one request before saving; the token stays encrypted and never enters the journal. `verify.py` lists the windows, the names looked up most and any time no copy covers; a record whose count does not match its queries fails. A window that holds more than one page of queries in a single second keeps that page and says the rest is missing. The copy is Cloudflare's answer through the collector, signed by the collector; within 24 hours anyone with a read-only token can compare it with Cloudflare.


---

# Independent witness

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/witness/

Run a witness with its own key and bot, publish signed checkpoints to a channel and check exports against it.

[Export and verify](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/) · [High assurance](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/) · [Panel guide](https://phishdestroy.github.io/TgWitness/docs/reference/panel/#extras)

A collector signs its own journal, so whoever controls the collector and its key could in principle rewrite or truncate the journal and sign it again. A witness makes that detectable. It is a separate process — another container, or better a server someone else runs — that every few minutes fetches the collector's signed journal head, signs what it saw with its own key, keeps it in its own journal and posts it to a Telegram channel.

Flow diagram · Collector → Witness (signed checkpoint: record count + head hash); Witness → Witness journal, own key; Witness → Telegram channel (signed post via its own bot); Evidence ZIP → verify.py; Witness journal, own key → verify.py; Telegram channel → verify.py (Telegram Desktop export or t.me/s page) · Collector · Witness · Witness journal, own key · Telegram channel · Evidence ZIP · verify.py · signed checkpoint: record · count + head hash · signed post via its own bot · Telegram Desktop export or · t.me/s page

**Diagram as text**

1. Collector → Witness (signed checkpoint: record count + head hash)
2. Witness → Witness journal, own key
3. Witness → Telegram channel (signed post via its own bot)
4. Evidence ZIP → verify.py
5. Witness journal, own key → verify.py
6. Telegram channel → verify.py (Telegram Desktop export or t.me/s page)

## What the witness gets, and what it does not

| The witness has | The witness never has |
| --- | --- |
| A read-only **witness token** for one workspace | The collector's Telegram session or API credentials |
| Its own Ed25519 key and journal | The collector's vault, signing key or panel token |
| Its own Telegram bot token | Message content: the head is a record count and a hash |

The token is created in **Extras → Independent witness**, shown once and stored only as a SHA-256. It opens exactly one endpoint, `GET /api/witness/head`, which returns a freshly signed checkpoint plus signed content-free collection counters and operational health. It cannot open the panel, read message content or change settings, and the panel token is not accepted there. Revoke a token on the same page. The collector records when a new witness key starts checking (`witness.seen`) and shows the last check per token; a witness that has not checked within 2.5 intervals is marked overdue.

New witnesses send a random challenge on each poll; the capture statement echoes it under the collector signature. Counters are bound to the exact checkpoint and are included in signed witness posts. Legacy heads remain accepted by the standalone witness. Journal growth alone is never counted as a new message.

## What it checks and records

Every interval (10 minutes by default) the witness:

1. fetches the head itself (the collector cannot push or skip it);
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen), a nondecreasing count and an unchanged head at an unchanged count;
3. appends a signed record to its own journal: `witness.anchor` with status `ok`, `key_changed`, `rollback` (fewer records than before), `fork` (same length, different head) or `invalid` (the answer failed verification), or `witness.no_response` when the collector did not answer;
4. posts the result to the channel, signed, including "no answer" while the witness is running and can reach the Bot API. The post ID is recorded (`witness.posted`), a failed post too (`witness.post_failed`).

A post looks like this; the last line carries the signed statement:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Run a witness

You need a Telegram bot (create one with @BotFather), a channel where that bot is an administrator, and the collector's address reachable from the witness — over HTTPS outside a private network (see the HTTPS profile in [deployment](https://phishdestroy.github.io/TgWitness/docs/reference/deployment/)).

Open **Extras → Independent witness → Configure** in the panel. Three steps cover read-only access, your channel and interval, then launching the witness. Publication policy, optional HTTP/SOCKS5 proxy and custom Bot API address are under **Advanced settings**. The form downloads `witness.json` with this workspace's collector key pinned. Download the newly created read-only token with **Save access file** as `witness-token.txt`; place it and a `bot-token.txt` created on the witness host beside that JSON. The collector never receives the bot token. Downloading does not start a service or publish a message. No hosted project witness is implicitly enrolled.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

The first command checks configuration and secret files without network requests or key creation. Paths in JSON are relative to that file; CLI/environment paths are relative to the working directory. Retain the witness fingerprint outside its host. The collector's last-poll indicator confirms a request only; publication is reported by Proof or checked in the witness journal and channel.

If the panel stays behind an SSH tunnel, expose only the scoped witness endpoint on a separate HTTPS hostname with [this Caddy example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example). The default workspace then uses `https://witness.example.org`, other workspaces use `https://witness.example.org/profiles/ID`. Tokens are still required; the panel and its other API routes are not forwarded by that virtual host.

Choose `all` for regularly published checkpoints. A five-minute interval means about 288 posts per workspace per day. `changes`/`problems` deliberately leave some checks unpublished. MTProxy is for the collector's Telegram client. Witness HTTP polling and Telegram's HTTPS Bot API use their own direct/HTTP/SOCKS5 route ([Bot API](https://core.telegram.org/bots/api)).

**Next to the collector, with Docker** (same host — independent process and key, but the same operator): put the values in `.env` and start the profile.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

With a published image use `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**On someone else's server** (a real independent witness): copy the repository there, set `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` plus the three values above in `.env`, then

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

or without Docker:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Publish to Discord

A witness can post to a Discord channel instead of Telegram. In Discord, open **Edit Channel → Integrations → Webhooks**, create a webhook and copy its URL. In the panel, choose **Discord webhook · your channel** in step 2. On the witness host, save the URL as `discord-webhook.txt` next to `witness.json`; it never reaches the collector.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

A witness has one publisher: a Telegram channel or a Discord webhook, not both. Posts carry the same signed statement and cannot ping anyone. A post longer than Discord's 2,000 characters is replaced by a short line with the full check attached as `witness-check.txt`. Each post ID is recorded as `witness.posted`. `verify.py --channel` reads Telegram channel exports only, so for Discord keep the witness journal: it holds every check.

### Options

| Option | Environment | Default | Meaning |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Minutes between checks, 1–1440 |
| `--timeout` | `_TIMEOUT` | 30 | Seconds to wait for the collector and the Bot API, 5–600 |
| `--post` | `_POST` | `all` | `all`: every check; `changes`: a new head or a problem; `problems`: only problems and missing answers |
| `--title` | `_TITLE` | `TgWitness witness` | First words of every channel post |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | Pin the collector key instead of trusting the first answer |
| `--proxy` | `_PROXY` | direct | `socks5://host:port` or `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Bot API address, e.g. a local Bot API server |
| `--data-dir` | `_DATA` | `witness-data` | Witness key and journal |
| `--config` | `_CONFIG` | – | JSON file with any of the options above |

The collector address, tokens and channel come from `--collector`, `--token` or `--token-file`, `--bot-token` or `--bot-token-file`, `--discord-webhook-file` and `--channel`, or `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` and `_CHANNEL`, which keeps secrets out of the process list.

A config file uses the option names with underscores, plus `texts`, which replaces the words of the channel posts:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts` keys: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. The command line wins over the environment, the environment over the file. Unknown options or text keys stop the witness with a message instead of being ignored. Wording never affects verification: verify.py checks the signed token at the end of every post. With `--post changes` or `problems`, checks that were not posted are still in the witness journal and `verify.py` lists them as never posted; the start record names the policy. Every check still appears in the journal, so fewer posts mean fewer independent Telegram times, not fewer checks.

Without a channel the witness still keeps its journal. Keep the witness key fingerprint (`python -m tgwitness.witness fingerprint`) somewhere else.

## Public proof page for several workspaces

`python -m tgwitness.proof` witnesses up to 32 workspaces at once and serves a read-only page with the latest signed check of each. Every workspace gets its own witness key and journal under the data folder and a pinned collector key; posting to a Telegram channel is optional per workspace. Start from [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example):

| Field | Meaning |
| --- | --- |
| `title` | Page title, 1–100 characters |
| `data_dir` | Witness keys and journals, relative to the file; default `proof-data` |
| `interval`, `timeout` | Minutes between checks (1–1440, default 5); seconds to wait (5–600, default 20) |
| `workspaces[].id`, `label` | Short lowercase alias and the name shown |
| `workspaces[].collector` | Collector address; other workspaces end in `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | Required, different for each workspace |
| `workspaces[].token_file` | File with that workspace's read-only witness token |
| `workspaces[].channel`, `bot_token_file` | Optional, together: post each check to a channel |
| `workspaces[].proxy`, `bot_api` | Optional route and Bot API address |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

The first command validates the file and the token files without opening a connection. The page answers only GET and HEAD:

- `/` shows every workspace; a workspace without a check for 2.5 intervals is marked stale.
- `/api/proof` returns the same as JSON.
- `/api/proof/<id>` downloads the latest signed statement (`tgwitness-public-proof-v1`): witness record number and hash, status, pinned collector key, checkpoint, collection counters and whether the channel post succeeded, signed by that workspace's witness key.
- `/healthz` answers 503 when a workspace's monitor has stopped.

Give the page its own hostname, as in [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example). For verification, export a workspace's witness journal with `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` and use it as described below.

## Verify

On the witness side, export its journal:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

Then, anywhere, with the collector's signed ZIP and the channel exported from Telegram Desktop (*Export chat history* → JSON gives `result.json`) or its public `https://t.me/s/…` page:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` checks the witness journal (chain and signatures), then that **every head the witness saw is part of the exported journal**: the record at that count must have exactly that hash. A head that does not match fails verification — the journal was changed after the witness saw it. It also reports heads seen after the export, anomalies the witness recorded, answers that failed, periods whose matching checkpoints are present in this export ("Witnessed from X to Y") and gaps. Later checkpoints do not extend those periods. The result includes the last matched record number and the number of trailing records without a matching checkpoint. Only answers signed by the export's own key count: an export signed by a key the witness never saw is reported as not witnessed, and without `--fingerprint` its signer stays unpinned. With `--channel` every signed post must match the witness journal record by record: changed posts fail verification, missing posts are listed. A date in a supplied Telegram JSON export is editable metadata, outside the signed witness token. Matching the token does not authenticate the publication date; the result explicitly reports that publication-time verification was not performed.

### Require a witnessed export boundary

For a handover that must include a witnessed final record, add `--require-witness`:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

This requires the independently retained witness fingerprint and a matching checkpoint at the exact end of this export. A checkpoint covering only an earlier prefix is insufficient. Pause collection, let the witness observe the final state, and export before further journal writes; if the journal changes, retain another checkpoint and export that state. A later checkpoint alone cannot verify a shorter export's final hash. When `--channel` is also supplied, missing claimed posts or an empty match set fail this strict check. Without the flag, ordinary integrity checks still report unwitnessed records without rejecting an otherwise intact archive.

The flag enforces consistency with the supplied, pinned witness records. The operator must still establish the witness's independence and preserve its records separately. It does not establish message truth, complete collection or an independently measured runtime.

A witness shows what the collector reported at those times and that later exports agree with it. It does not show that the collector recorded everything Telegram delivered, or that message content is true. A witness run by the same operator on the same machine is weaker than one run by someone else.

An increased count alone cannot establish append-only continuity online: the offline comparison must match each retained prefix hash against the full collector export. Witness downtime and failed publication leave intervals without external anchors. Missing posts can be reported against a retained witness journal; neither a channel nor a server controlled by the same operator is an immutable third-party archive.


---

# Timestamps

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/timestamp/

RFC 3161 timestamps for signed checkpoints: what is sent to the authority and how a response is verified.

TgWitness prepares RFC 3161 requests and verifies timestamp authority (TSA) responses. This manual procedure neither selects a TSA nor submits data; evidence mode does both on a schedule ([evidence format](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)). A prepared request is **not yet a timestamp proof**.

## What the proof binds

Flow diagram · Account observations → SHA-256 chain and Ed25519 signatures; SHA-256 chain and Ed25519 signatures → Signed checkpoint; Signed checkpoint → Exact-byte hash and random nonce; Exact-byte hash and random nonce → RFC 3161 request; RFC 3161 request → Independent TSA; Independent TSA → Signed TSA response; Signed checkpoint → Verify data, nonce and explicit CA trust; Signed TSA response → Verify data, nonce and explicit CA trust · Account observations · SHA-256 chain andEd25519 signatures · Signed checkpoint · Exact-byte hash andrandom nonce · RFC 3161 request · Independent TSA · Signed TSA response · Verify data, nonce andexplicit CA trust

**Diagram as text**

1. Account observations → SHA-256 chain and Ed25519 signatures
2. SHA-256 chain and Ed25519 signatures → Signed checkpoint
3. Signed checkpoint → Exact-byte hash and random nonce
4. Exact-byte hash and random nonce → RFC 3161 request
5. RFC 3161 request → Independent TSA
6. Independent TSA → Signed TSA response
7. Signed checkpoint → Verify data, nonce and explicit CA trust
8. Signed TSA response → Verify data, nonce and explicit CA trust

The collector signature binds records to its key. A trusted TSA response can establish that a particular checkpoint existed by the TSA's stated time. The checkpoint can then bind the journal prefix. This does not establish the time of each Telegram action or the truth of the captured content.

## Procedure

1. Retain the collector key fingerprint through a separate trusted channel. A key supplied only by the examined ZIP is insufficient to identify the collector.
2. In **Exports → Prepare timestamp request**, download the selected workspace's request ZIP. Extract `checkpoint.json`, `timestamp.tsq`, `SHA256SUMS` and `README.txt`. Do not change the checkpoint bytes.
3. Choose a TSA appropriate to the investigation. Submit `timestamp.tsq` using its documented method, with `application/timestamp-query` for an HTTP service. Save the original binary reply as `timestamp.tsr`, the endpoint, retrieval time and request outcome. The request contains a hash and nonce rather than messages; network metadata still reveals the request.
4. Obtain the trusted root certificate independently of the reply, plus any intermediates required. A certificate in the reply does not become trusted merely because it is included there.
5. From a trusted TgWitness installation, verify:

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

Add `--intermediates tsa-intermediates.pem` or `--openssl /path/to/openssl` if needed. OpenSSL must support `ts`. On Windows the verifier also searches the standard Git installation. OpenSSL 3.5.9 was tested locally with a synthetic CA/TSA.

1. Export a signed journal ZIP after the checkpoint so it includes that prefix. Verify using the independently known fingerprint:

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. Preserve the ZIP, checkpoint, request, reply, certificate chain, verification results and handoff record outside the collector. Repeat verification at receipt.

To prepare a request from a saved checkpoint:

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

Preparation canonicalizes JSON and includes the matching checkpoint in the archive. Use the **checkpoint bytes from that archive** for TSA verification, even if the input file had different whitespace.

## Verification boundaries

| Check | Current behavior |
| --- | --- |
| Data | SHA-256 of the exact checkpoint bytes must match the response |
| Request | With `--request`, the original query and nonce are verified |
| TSA signature | OpenSSL verifies the signature and chain to the explicit CA |
| Collector signature | Separately verified by the journal verifier with a pinned key |
| Revocation | No automatic OCSP/CRL retrieval |
| Long-term validity | No archival validation after certificate expiry |
| Scheduled submission | Evidence mode, off by default |

`--request` is technically optional, but omitting it prevents verification of the original nonce. For this full procedure, the result's `request_checked` must be true. Certificate verification follows the installed OpenSSL's rules and verification time. Long-term preservation needs a separate certificate/revocation evidence policy.

A valid cryptographic signature is not automatically a qualified timestamp or a legal admissibility determination. If an operator fabricated observations before timestamping, the TSA anchors those bytes; it does not establish their truth.

## Handoff record

Record the case identifier, sender and recipient, UTC transfer time and its source, purpose, filenames/SHA-256 values, collector fingerprint, sequence range, known gaps, verifier version and verification outcome. Sign and independently retain this record through your organization's process. A multi-user custody-record system is not implemented in TgWitness.

No independent live TSA was contacted during development. Local tests create a synthetic CA/TSA to check compatibility and rejection of changed data, nonce or CA.


---

# Storage and recovery

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/storage/

Backups, moving older files to your cloud, copies under Object Lock and recovery on a new machine.

The panel separates three tasks:

| Task | What it does |
| --- | --- |
| Keep a backup | Copy the signed journal, checkpoints, preserved files and queued exports to the configured S3 destination. |
| Free local space | Copy selected older attachments to S3 or an rclone cloud remote, read them back in full, verify the encrypted bytes, then remove the verified local copy. |
| Keep an evidence copy | Configure S3 Object Lock and check the returned retention status. The service must confirm the requested mode and date. |

Freeing space never deletes or rewrites the signed journal. Each attachment keeps its original SHA-256 and a recovery receipt. Optional gzip compression takes place before authenticated encryption. Cloud filenames do not contain Telegram names, chat IDs or original attachment names. One attachment may be up to 32 GiB.

An upload response alone is not permission to delete a file. TgWitness downloads the complete encrypted object and verifies its size and SHA-256, saves the receipt, then checks the local bytes again immediately before removal. An upload failure, different readback or cancelled transfer leaves the local file in place. If an enabled evidence backup has not yet copied that file, removal also waits for it.

## Connect a destination

In **Extras → Storage & disk space → Manage storage**, choose the task and destination, save it, then select **Test upload & download**. The test uploads a small random probe and reads it back. It does not use Telegram content.

For S3, use the provider's actual endpoint, region and bucket. Wasabi, Backblaze, Cloudflare R2 and other compatible services use the same S3 settings. A compatible API alone does not imply support for Object Lock. Governance mode may allow an authorized administrator to bypass retention; Compliance mode has different constraints. Read the returned Object Lock status before relying on retention.

For an rclone destination, create one remote using rclone's provider setup and paste that remote's `[name]` section into the panel. The installed helper supports MEGA, Google Drive, OneDrive, Dropbox, Box, pCloud and the other providers shown in the selector. Credentials are saved in this workspace's encrypted vault. OAuth refreshes are saved back into the vault. Credentials are not added to journal events or included in recovery downloads.

The helper is installed within the workspace, with a pinned version and SHA-256. It is not added to the system PATH. Configuration files and working files are temporary files within that workspace. Command-based and local-file remotes are refused. rclone currently requires an explicitly selected **Direct** route for external requests. Use native S3 storage for a workspace SOCKS5 or HTTP route; rclone does not silently bypass an unavailable route.

## Keep the recovery file

Choose **Save recovery file** after copying files and keep it somewhere separate from the installation. It contains the decryption key and signed object receipts, so treat it as a private key backup. Keep the original remote configuration and destination credentials separately as well. A recovery file taken before a later copy does not contain that later file's receipt.

The signing-key fingerprint should already be recorded independently. A signature checked only against the key supplied inside the same file does not establish whose recovery file it is.

To repair missing storage receipts in an existing workspace, open **Recover files from a saved recovery file** and select the file. The panel checks the signature and requires the same workspace signing key. It refuses to replace a different storage key. Then choose **Restore all files**. Restoration pauses the automatic storage rule so the next scheduled pass cannot immediately remove the restored files again. Re-enable the rule when finished with the local copies.

Restoration verifies the ciphertext, authenticates decryption, decompresses if needed and checks the original plaintext SHA-256 before placing a file in `media/`. A corrupt remote object never replaces a local file. An existing local file with different bytes is kept for review rather than overwritten.

## Recover after losing the installation

Install TgWitness on another machine. Use the private recovery file, the separately recorded fingerprint and the original destination credentials:

```
python -m tgwitness.storage recover \
  --recovery storage-recovery.json \
  --fingerprint TRUSTED_WORKSPACE_SHA256 \
  --credentials original-rclone.conf \
  --output recovered-attachments
```

For S3, `--credentials` points to a private JSON file with `access_key` and `secret_key`; the signed recovery file supplies the destination settings. The command uses a direct external connection and downloads the pinned helper when an rclone remote needs it. It refuses an existing output directory.

Recovered original bytes are written to `recovered-attachments/media/`, named by their SHA-256. `recovery-log.jsonl` is an unsigned record of recovery operations. The command does not recreate a lost signed journal or its signing key. Keep a full workspace backup for those. A storage recovery file is not a full workspace backup.

## Operator bot and completion notices

The Telegram bot belongs to the operator. Create it through BotFather and set its token, destination chat and explicit allowed Telegram user IDs in the panel. Both the sender and the chat must match. Forwarded messages and commands from other bots are ignored.

`/status` and `/stats` are available in the default status-only mode. Optional control mode adds `/pause`, `/resume` and `/copy`. `/copy` requests the configured storage task; it does not mean that a remote upload already finished. Commands cannot supply arbitrary URLs, files or shell programs.

Use the separate notification settings for alerts and task completion. Completion notices distinguish an account export with gaps from a complete export, and show history and storage counts. Message excerpts are not included unless separately enabled in notification settings. The service picker is generated from the actual installed Apprise catalog rather than a fixed set of provider examples.


---

# Security and data handling

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/security/

Threat model, access model, secrets at rest, network exposure, session imports and how to report a vulnerability.

TgWitness runs on your own computer or server. Account connections, public proxy-list upkeep and optional external services have explicit routing policies. Notifications, timestamps, off-site copies and a witness are separately configured. This page lists what is protected, how, and what is left to the operator.

| Area | In short |
| --- | --- |
| Access | Administrator key plus scoped access to accounts/chats, seven permissions and revocable sessions; localhost by default |
| Secrets at rest | Session, API pair, signing key and proxy settings are encrypted with Fernet |
| Messages and media | Stored unencrypted: use disk encryption and strict permissions |
| Integrity | SHA-256 hash chain and an Ed25519 signature on every record |
| Not covered | A machine administrator, a leaked panel token, completeness of capture |

For vulnerability reports, see the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

## Access model

The main panel token grants full control. Other people can receive their own [scoped access](https://phishdestroy.github.io/TgWitness/docs/reference/access/): chosen workspaces and chats, permissions, expiry, IP restrictions, sign-in limits and revocable sessions. A chat-limited access cannot perform whole-workspace operations even if their permission is ticked. Workspaces share a process and do not isolate data from the host administrator.

The panel listens on localhost by default. Browser sign-in exchanges an access token for a session credential; the browser sends it as a bearer token. It is kept in sessionStorage rather than an authentication cookie. Lock/sign-out clears the browser session. Closing a browser or ending a session does not stop collection.

Issued tokens and session credentials are kept as hashes in the encrypted vault. Revocation ends the associated sessions; permission changes affect subsequent requests. Downloaded files cannot be recalled. The administrator can limit their own browser sessions too, but scripts using the main panel token directly retain full access and bypass those browser-session limits.

Failed authentication is rate-limited by client address. IP restrictions use the address seen by the application; check reverse-proxy behavior before relying on it. Witness credentials remain separate read-only checkpoint/health credentials.

### Demo access

`/api/demo-access` is a deliberately unauthenticated bootstrap for an explicitly started, isolated synthetic demo. It issues a separate process-lifetime capability, never the real panel token or a TGWITNESS_TOKEN override. Issuance and use require a loopback peer and Host, no forwarded headers, and no cross-origin request. Additional workspaces or an authorized session disable this path. Live workspaces never issue the capability. The demo cannot connect accounts or change collection settings.

## Panel content and exports

The panel uses no external fonts, analytics, CDN resources, or embedded remote media. Telegram-sourced text is inserted as text, not HTML. Downloaded attachments are served as binary attachments. JSONL exports preserve original strings; HTML escapes them; CSV cells that could become formulas are prefixed with an apostrophe.

Exports exclude authentication and signing secrets, but deliberately contain collected source metadata, identifiers, and possibly personal or sensitive content. Telegram access hashes and file references can occur in raw source metadata.

## Secrets at rest

Telegram API credentials, StringSession, and the Ed25519 private key are encrypted using Fernet. By default its key is stored in the same protected data directory. This reduces accidental plaintext exposure; it is not protection against an attacker who can read the whole directory. Message content and media are **not encrypted** by TgWitness. Use disk encryption and restrictive OS permissions. Unix private key files are created with mode 0600; newly created data directories use mode 0700. Existing directory permissions are not changed. Windows inherits directory ACLs: restrict them to the service account and authorized administrators.

### External master key

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The running process can access the key; this is not HSM isolation. The panel reports the selected mode and explicitly states that message/media storage is not encrypted by the application. See [connection, proxies and data protection](https://phishdestroy.github.io/TgWitness/docs/reference/connection/) for the full threat model.

## Proxies and network routes

Proxy configuration is encrypted in the vault. Passwords and MTProxy secrets are not returned by the API or written to evidence records. Each workspace chooses its Telegram route and an [IP mode](https://phishdestroy.github.io/TgWitness/docs/reference/connection/#ip-modes).

**Hide the address** refuses direct Telegram fallback and requires a proxy for external HTTP requests. The explicitly selected fallback mode permits direct Telegram access after its delay; tunnel/VPN mode permits direct routes. Choosing tunnel mode does not install or verify a VPN. These settings do not control all machine traffic, browsers, package managers or local proxy-host DNS resolution.

MTProxy carries Telegram traffic only. External requests can use a separate SOCKS5/HTTP proxy, the workspace's SOCKS5/HTTP route, or an allowed direct route; they can also be disabled. The independent witness has its own transport settings. Ordinary SOCKS5/HTTP CONNECT authentication is not encrypted by those proxy protocols themselves. Fake TLS MTProxy secrets remain unsupported.

## Sign-in and session imports

Converted .tgwitness-session files contain a plaintext authorization secret until loaded and stored in the vault. The offline CLI accepts reviewed Telethon schemas. Panel import additionally accepts Pyrogram SQLite, modern single-account TData ZIP, and documented JSON inputs. It is authenticated, limited to four files / 8 MiB, and processes uploads in memory without archive extraction or saving original files. Normalized credentials are returned only to the requesting authenticated browser; they are saved in the encrypted vault after successful Telegram authorization. Protect originals and converted files, and avoid concurrent clients cloning an authorization.

TData processing verifies container checksums, local decryption hashes, and structure lengths. A supplied Desktop local passcode is used transiently and is not stored. This bounded parser does not establish that every Desktop version is compatible. QR images are generated locally, contain short-lived Telegram login tokens, and are never sent to an external rendering service. Lock, workspace switch, new login, and route changes cancel pending QR attempts. Reload/closing a tab may leave an attempt pending until expiry. A successful QR login still enforces account binding. Ordinary API bodies remain limited to 16 KiB; the authenticated import route accepts up to 12 MiB of encoded JSON, enforcing the smaller decoded-file limit separately.

Login codes and Telegram two-step verification passwords are not persisted. Phone number/code-hash state is held in memory during authorization. Telegram sessions grant account access; never upload a data directory, session, token, vault key, or private signing key to GitHub.

## Logs and transport

The default API validation response is replaced so it does not echo credential values. Application access logging is disabled. Do not configure a reverse proxy to log Authorization headers or request bodies. HTTP carries tokens and login secrets in plaintext: use HTTPS or an SSH tunnel whenever leaving localhost.

## Integrity limits

The hash chain, database triggers, and signatures detect certain modifications; they do not prevent a local administrator from rewriting and resigning the journal. Retain signed checkpoints and the public-key fingerprint on a separate system. Evidence mode and the off-site copy (both off by default) send checkpoint hashes to timestamp services and encrypted copies to S3-compatible storage; see the [evidence format](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/). Transparency logs, HSM-backed signing and formal chain-of-custody certification are not implemented.

## If you suspect a problem

Preserve the original data directory and use a separate copy for analysis. Do not include private Telegram data or credentials in a public issue. No independent security certification is claimed.


---

# Architecture

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/architecture/

Components of the collector, panel, journal, workers and witness, and how data moves between them.

One Python process hosts the FastAPI panel and any number of isolated workspaces, each with a Telethon user-account client. SQLite holds an append-only signed event journal and mutable operational settings. An encrypted vault holds API credentials, the StringSession, and signing key. The frontend is plain bundled HTML/CSS/JavaScript: no Node build, CDNs, or runtime frontend downloads are needed.

Optional browser and AyuGram recorders run in **separate processes or containers**. The `tgwitness_capture` package owns their event format, keys, artifacts, checkpoint API, independent witness and standalone verifier. It is bundled in the main wheel and can also be installed alone from `addons/capture`, without importing the collector. The main panel's `capture_api.py` and `capture_connections.py` provide administrator-only, workspace-scoped controls under `/api/capture`; connection tokens live in the encrypted vault. No recorder or outbound request starts with the main process. Each explicit command verifies a fresh challenge against the pinned recorder key. Exports are verified before download and keep their original signature; they do not become Telegram message events. Collection sessions and proxy routes stay with each client. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md) for deployment and trust boundaries.

| Module | Responsibility |
| --- | --- |
| collector.py | Authorization, dialog selection, updates, snapshots, media queue, connection monitoring |
| interactions.py / telegram_client.py | Explicit panel actions, signed receipts, persistent request IDs and task-local callback/join retry policy |
| message_content.py | Observable message comparison, excluding transport access metadata |
| workers.py | Wait for export file workers before cancellation cleanup |
| store.py | WAL transactions, ordered event chain, query filters, operational settings |
| security.py | Private-file creation, encrypted vault, Ed25519 signing, single-process lock |
| evidence.py | Complete-journal export, derivatives, checkpoints, attachment verification |
| verify.py | Standalone, read-only verifier (stdlib + cryptography): archives, coverage, witness journals and channel posts, profile files |
| app.py | Authenticated API, lifecycle, request validation, static panel |
| profiles.py | Multiple account collectors, shared access controller, per-workspace lifecycle |
| access.py | Scoped grants, permission checks, IP restrictions, session limits and administrator console |
| proxy_catalog.py | Public feed snapshots, transport checks, shared proxy pool and health-based selection |
| provenance.py | Signed acquisition-run identity, code and dependency measurements |
| network.py | Validated per-workspace routes; redacted status and evidence; Telethon transport options |
| sessions.py | Offline read-only conversion of reviewed Telethon SQLite schemas |
| account_import.py | In-memory detection and normalization of supported account files and JSON |
| tdata.py | Bounded modern TData ZIP reader, checksum/decryption validation, no extraction |
| doctor.py | Local readiness checks without collection, login or package installation |
| download.py | Authenticated streaming export download with bounded reads and no overwrites |
| monitoring.py | Validated per-workspace event policy and per-type attachment rules, shared by handlers, status and signed receipts |
| scope.py | Observation scope (chosen chats, Telegram folder, whole account), source types, exclusions, recheck tiers |
| dossier.py | People profiles per chat built from saved records: facts with record references, avatar SHA-256/pHash, mention extraction |
| witness_api.py | Read-only witness tokens and the signed journal head they may fetch |
| witness.py | Independent witness process: own key and journal, head checks, signed channel posts, export |
| alerts.py | Apprise notifications and the panel's notification list |
| logging_config.py | Console logging and rotating server diagnostics for windowless launches |
| static/ | Responsive interface, local access gate, filters, details, exports, account setup |
| demo.py | Clearly labeled synthetic journal, isolated from real collection |

Observation handlers are registered before connecting. Live collection is gated by the active client identity, explicit running state, enabled sources or the observation scope (folder or whole-account modes add a new chat as a source on its first update), and event policy. Rejected and superseded clients cannot contribute live updates. Raw reactions and membership updates preserve visibility limits. Incoming message content and its durable media job are committed together. Jobs preserve the original TL descriptor and bind its hash to the signed message observation. Sender/editor/deleter semantics are separated.

Each workspace accepts one account and has its own directory and signing identity. The main workspace remains at the root for compatibility; additional workspaces live in profiles/<id>/. One bearer token controls the whole installation; workspaces are not separate authorization tenants. Process locks protect directories; database locks serialize event insertion. Each append commits synchronously to SQLite WAL with FULL synchronous mode. Event update/delete triggers prevent ordinary application edits; filesystem administrators remain inside the trust boundary.

API authorization is a bearer token. Login operations are serialized and time-bounded. Account uploads use a dedicated 12 MiB encoded-body limit and an 8 MiB decoded-file limit; normal API requests retain the 16 KiB limit. Conversion runs in a worker thread, keeps uploads in memory, and returns normalized input to the authenticated browser. QR login has a per-workspace candidate, short-lived identifier, waiter task, and explicit cancellation. Only accepted authorization becomes the active client. Telegram FloodWait is returned with a Retry-After value; credentials and raw RPC error messages are not exposed in API errors. Exports run outside the async event loop and are serialized per workspace. They stream a stable read snapshot, and can coexist with continuing WAL writes. Workspace collectors share the process/event loop.

Current history snapshots and live updates can overlap. Both are separate observations, labeled by source; duplicates are not silently collapsed. No inference from missing IDs, fabricated deleted text, forced member enumeration, or automatic group joining is implemented.

For the operator-facing explanation, see [how collection works](https://phishdestroy.github.io/TgWitness/docs/reference/collection/) and [accounts and session formats](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/).

Network configuration lives in the encrypted vault. Applying a route closes old clients and cancels unfinished login; later connections use that route with no direct fallback. A new external-key installation derives each workspace's Fernet key with HKDF-SHA256 from a master key file and a stored random salt. This protects secrets separately from the data directory, not plaintext journal/media contents.

Local demo entry uses a separately generated process capability, never the configured panel token. Issuance and acceptance require explicit demo mode, a synthetic root without additional workspaces or an authorized session, loopback peer/Host, no proxy forwarding headers, and no cross-origin browser request. Live APIs retain bearer authentication and reject collection changes in demo mode.


---

# What has been tested

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/verification/

The live Telegram test, automated checks, browser checks and what remains unverified.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Count |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| Check | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Live Telegram test, whole account · 29 October 2026

The same account kept running after the test below. On 29 October at 12:10 UTC its scope was switched to the whole account (channels, groups, private chats and bots); the panel asked for confirmation and the signed journal recorded it. By 17:59 UTC the journal held:

| Recorded, 27 October 21:36 to 29 October 17:59 UTC | Count |
| --- | --- |
| Journal records | 9,968 |
| New messages | 5,308 |
| of them after the switch to the whole account | 3,878 |
| Deletions | 784 |
| of them deleted after TgWitness had saved the message | 596 |
| Edits | 41 |
| Messages added by rechecks | 2,273 |
| Messages a recheck could no longer find | 18 |
| Messages saved by history snapshots | 242 |
| Saved attachments | 247 |
| Collector starts | 19 |
| Telegram FloodWait pauses | 26 |

- The panel's **Verify** check confirmed the signatures and hash chain of all 9,968 records.
- Messages came from 2 groups or channels and 3 private chats and bots. One message button was pressed from **Chats**; the request and Telegram's answer are in the journal.
- New chats were added when the collector rescanned the account at a restart. Saving the earlier messages of new chats was off (`history = 0`), so it is not covered here.

Not covered: reactions, membership changes, people profiles, sending messages, joining by invitation, proxies, notifications, the witness bot and several accounts at once. Public files contain only counts.

## Password-protected export opened with libarchive · 29 October 2026

An archive written by the export encryption code (WinZip AES-256, the format 7-Zip and WinRAR read) was opened with Windows `tar` (bsdtar 3.6.2, libarchive). With the right password the extracted file matched the original SHA-256; a wrong password was refused with "Incorrect passphrase". 7-Zip and WinRAR themselves were not run.

## Live Telegram test · 27 to 29 October 2026

One real Telegram account, signed in through the built-in API pair pool, recorded one supergroup from **27 October 21:36 UTC to 29 October 05:15 UTC**. The collector was started 12 times in that period.

| Recorded | Count |
| --- | --- |
| Journal records, including heartbeats and service records | 2,385 |
| New messages | 1,291 |
| Deletions | 472 |
| of them deleted after TgWitness had saved the text | 347 |
| Edits | 12 |
| Messages missed while stopped, added by the recheck | 12 |
| Saved attachments | 17 |
| Attachments not downloaded (downloads off, or no file to download) | 14 |
| Telegram FloodWait pauses, 3 seconds each, during rechecks | 8 |

- The signatures and the hash chain of all 2,385 records verify against the journal's public key.
- After a restart the collector resumes from the saved update state (`pts`) and Telethon catches up; the recheck then adds messages that are still missing.
- On every FloodWait the collector waited the requested time and continued.
- The account stayed signed in, and the same session reconnected on 29 October.

Not covered by this test: several accounts at once, administrator roles, proxies, outages longer than a few hours and the full [live acceptance procedure](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Public files contain only these counts: no account or chat identifiers, messages or credentials.

Older entries below describe their own runs; most of them used synthetic test clients. The latest automated results are below.

## Built-in public MTProxy lists · 29 October 2026

This is the historical test record of the original manual-selection build. For the current automatic pool and IP modes, see [connection settings](https://phishdestroy.github.io/TgWitness/docs/reference/connection/#ip-modes). Counts and unsupported features below belong to that tested revision.

Added a bundled public snapshot and explicit HTTPS refresh from SoliSpirit/mtproto and zakky8/mtproto-proxy-pro. On this host, the application downloader fetched both feeds successfully on 29 October 2026 at 12:58 UTC: **118 unique compatible endpoints** after filtering, deduplication and the 64-entry limit per source. This verifies list retrieval, not connectivity or message delivery through those endpoints. No real account was connected to a listed proxy during this work. [Operator and user guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md).

Failed/empty/incompatible source responses retain previous entries and dates. Updates do not alter the selected route. Public addresses are validated and resolved IPs pinned on selection; operator/manual routes remain separate. The connection probe is now available in the panel before account login. Fake TLS ee and automatic proxy selection remain unsupported. The operator's catalog overrides subscriptions completely.

- Full suite: **366 passed, 3 skipped**, 287.94 seconds. Existing dependency warnings and platform skips remain. Final public-list/localization regression: **36 passed**, including rejection of invalid download-proxy ports; this overlaps the full suite.
- Browser acceptance passed in English/Russian, light/dark at 390/1440 pixels: bundled choices, no external fetch on opening settings, explicit refresh, retained routes and cache during failures, pre-login probe, late-response workspace isolation, source details and layout/contrast. No JavaScript errors or external browser requests.
- Final static translation coverage passed for all 13 locales; new copy is translated into Russian with explicit English fallbacks elsewhere. The updated built-in guide passed layout/contrast checks in both themes.
- Ruff and publication checks passed (259 public files, 1,354 local links); updated Compose and CI YAML parsed. Docker and remote CI were not executed here.
- The rebuilt wheel passed isolated installation, bundled-list loading and signed-export verification. All 69 package resources matched the workspace; source hashes were checked.

Receipts: `test-results/public-proxy-research/download-receipt.json`, `test-results/public-proxy-research/copy-receipt.json`, `test-results/public-proxies-full-suite.log`, `test-results/public-proxies-final-focused.log`, `test-results/public-proxies-browser/receipt.json` and `test-results/public-proxies-package.log`. Browser/account/transport fixtures are synthetic; the two feed downloads above are real HTTPS requests.

## Optional extras presentation · 29 October 2026

The former Proof bot destination is now **Extras**: a short overview followed by a separate setup page for the selected option. The witness form has three steps, with connection management, network options and deployment details folded away. GitHub is explicitly planned and has no credential form. [Overview of Extras](https://phishdestroy.github.io/TgWitness/docs/reference/panel/#extras).

- 30 focused tests passed for localization, witness setup and publication checks.
- Chromium setup acceptance passed in English/Russian, light/dark, at 390/1440 pixels: keyboard focus and return, no implicit connections when selecting extras, draft retention, pinned configuration/token downloads, token clearing on lock, and working local guide anchors. Layout and solid-background text contrast checks passed.
- Workspace-switch acceptance passed, including a delayed token response arriving after a switch. Quick navigation finds the extras through bot, proof and GitHub terms; its existing 320/390/1440-pixel and Russian/RTL checks also passed.
- No JavaScript errors or external browser requests were observed in the setup run. These are synthetic UI checks, not new live Telegram or bot publication evidence.
- Final language loading and dictionary coverage passed for all 13 locales, preserving explicit English fallbacks outside Russian. The expanded Proof guide also passed layout/contrast checks at 320/768/1440 pixels in both themes.
- The rebuilt wheel passed isolated installation and signed-export verification. All 67 packaged resources matched the workspace; the source archive contains 253 public files. Source/link checking passed for 1,346 local documentation links.

Receipts: `test-results/setup-browser/receipt.json`, `test-results/quick-navigation/receipt.json`, `test-results/extras-final.json`, `test-results/extras-package.log` and `test-results/extras-artifacts.json`. Screenshot assets use synthetic workspaces.

## Witness bot and proxy setup audit · 29 October 2026

The witness setup (now **Extras → Independent witness**) prepares an independently deployed witness: pinned collector key, scoped token download, own channel, publication policy, HTTP/SOCKS5 route and custom Bot API. The bot token remains on the witness host. Its new `--check-config` validates configuration and files without opening a network connection or creating a key. JSON file paths resolve beside the configuration. All Compose witness variants now forward the HTTP proxy and Bot API settings.

Account settings support an operator-managed public MTProxy catalog, custom Telegram proxy-link preview and the existing manual fields. Catalog responses omit secrets; selection stores the route in the workspace vault. Missing/malformed catalogs leave manual routes available. No project proxy addresses or hosted witness service are invented or enabled by default. A Caddy example exposes only the scoped head endpoint when an external witness must reach a collector whose panel stays private.

Validation:

- Full suite: **348 passed, 3 skipped**, 195.81 seconds. Windows limitations account for the skips; the two existing dependency deprecation warnings remain.
- Final witness/configuration/release regression run: **11 passed, 1 skipped**. This overlaps the full suite. Tests include path resolution, offline preflight, signing/publishing through an actual loopback HTTP Bot API fixture, recorded delivery failure, channel-token verification and proxy-secret exclusion.
- Chromium setup acceptance passed in English/Russian at 390/1440 pixels: pinned config and token downloads, token clearing on lock, catalog selection, custom-link preview followed by explicit save, layout/contrast and no JavaScript errors or external browser requests. Corrected narrow Russian account-heading and login-tab overflow.
- Ruff, source/link checks and Compose/workflow YAML parsing passed.
- The rebuilt wheel passed isolated installation, panel/static resource and API-auth checks, plus independent verification of direct and streamed 32-event synthetic exports.

Receipts: `test-results/setup-full-suite.log`, `setup-final-focused.log`, `setup-browser/receipt.json`, `setup-browser-final.log` and `setup-package.log`. These checks use synthetic accounts/proxies and a local Bot API fixture. They do not claim a real bot publication, working public MTProxy server, remote CI run or Docker deployment. The retained real Telegram observation history above remains a separate piece of evidence. [Setup instructions](https://phishdestroy.github.io/TgWitness/docs/reference/witness/#run-a-witness).

## Presentation and documentation review · 29 October 2026

The product page, access screen, English/Russian READMEs and presentation images now share one visual style. Public screenshots use fictional demo data. The review also corrected the outdated live-validation and recovery descriptions above.

- Focused localization, site and publication tests: **33 passed, 1 skipped**. The skipped test requires symlink creation unavailable on this host.
- General Chromium panel acceptance passed, including all language catalogs, RTL layout, light/dark themes, solid text contrast and workspace switching. The profile-creation check now waits for its actual HTTP response before checking the selected workspace.
- English/Russian access screens passed layout and contrast checks in both themes at 320, 390, 768, 850 and 1440 pixels; the submit button stays in the initial viewport.
- Public-site acceptance passed at 320, 390, 768, 1024 and 1440 pixels, including message history controls, screenshot enlargement/Escape/focus return, keyboard tabs, clipboard refusal, project subpaths, reduced motion and the no-JavaScript fallback. No failed asset requests, external requests or JavaScript errors were observed.
- The rebuilt wheel passed an isolated installation check: panel resources and locales load, API access requires authentication, and direct/streamed exports independently verify all 32 synthetic events. Ruff and public-source/link checks passed.

Local receipts: `test-results/design-tests.log`, `design-panel-final.log`, `design-review-final.log`, `design-site.log`, and `design-package/install-receipt.json`. The full backend suite was not rerun for this presentation/documentation change; its preceding result remains in the pre-publication audit.

## Version 0.6.1

0.6.1 changes the panel presentation, launchers, packaging and documentation; collection, storage, signing and export code is unchanged. On Windows 11 / Python 3.12.10 with the pinned runtime:

- The full suite passed **137 tests** with **2 skips** and the existing Starlette warning. New tests cover the launcher's Ctrl+C handling (the server gets 30 seconds for an orderly stop) and actionable setup-step failures.
- Chromium (headless shell 156) passed all **45 general scenarios** and **35 account-import/QR/Auth Key scenarios**, including the solid-text contrast check, no horizontal overflow at 320–1440 px and visible first login fields at 320/390 px. No page JavaScript errors or external requests were observed.
- `python start.py --setup-only` reinstalled the package as 0.6.1 and `python start.py --check` reported ready. A real `python -m tgwitness --demo` server returned the panel, stylesheet, script, logo, guide and `/api/status` version 0.6.1; the removed `workspace.css` returned 404.
- `Start.cmd` found a Python installation outside PATH. With no Python available it showed the installation offer; declining printed manual instructions and exited 1. The python.org download step fetched the 3.12.10 installer and passed the Python Software Foundation Authenticode check; the installer itself was not run on this host.
- `start.sh` without any Python printed the install hint and exited 1. `scripts\Docker.cmd` and `scripts/docker-start.sh` were exercised against fake `docker` executables: correct call sequence, panel address and token output, and no success message after a failure.
- `python tools/build_portable.py` built an 18.8 MiB Windows package after verifying the pinned embeddable-runtime checksum. Extracted to a path with spaces and started with only `C:\Windows` directories on PATH, its embedded Python passed `TgWitness-Check.cmd`, served the demo (32 events) and a live workspace, and Chromium rendered the journal and detail drawer without JavaScript errors. Data was written to the package's `data` folder.
- `python tools/build_preview.py` produced a 110-file source archive. A dry-run of `git add` listed the same 110 files with no session, key, database, token, log or export files, no local absolute paths and no secret-shaped strings.

Not executed in this particular 27 October packaging run: the automatic Python installation itself, Docker build/Compose checks, Linux/macOS runs or a new live-account exercise. Real Telegram evidence is recorded above and in the earlier account checks below. CI definitions alone do not qualify platform execution.

## Version 0.6.0

The latest full pinned-runtime suite on Windows 11 / Python 3.12.10 passed **135 tests**, with **1 skip**, in 26.53 seconds and the existing Starlette warning. The skip requires POSIX permissions. After adding the QR renderer to readiness checks and process measurements, 8 affected readiness/workspace checks also passed.

New coverage includes Telethon schemas 7/8, Pyrogram schemas 2/3, complete JSON keys and metadata-only JSON, matching/conflicting account files, TData passcodes, checksum tampering and unsafe paths, offline/authenticated in-memory conversion, online account-ID checks, QR success/2FA/expiry, stale cancellation, and account isolation. TData fixtures use a separate AES-IGE implementation for encryption.

Chromium passed **45 general scenarios** and **35 account-import/QR/Auth Key scenarios**, with no page JavaScript errors or external requests observed. New browser checks cover all four input formats together, protected TData, API metadata, QR rendering, expiry/retry, 2FA, wrong-account rejection, lock/workspace cancellation, responsive layout, and late conversion responses after a newer file selection.

Both browser suites passed again after the account-entry changes. Live setup opens the account form; demo mode opens its sample journal. The demo Account page shows live startup instructions and hides credential inputs. Focused checks at 320, 390, and 1440 pixels confirmed the number field and primary button fit without scrolling and API fields are initially collapsed, and text contrast remains readable. Capture and verification controls remain covered after opening their new expandable sections.

The direct Auth Key flow was exercised with synthetic credentials through the real import and authorization endpoints. Checks cover incomplete keys, missing DC, imprecise User IDs, mismatched account identity, saved API credentials, visible request progress, secret clearing, and late responses after edits or method changes. All four sign-in methods were checked at 320, 390, and 1440 pixels. The file picker precedes format guidance, and the Connect button fits the initial 844-pixel viewport with API settings collapsed. No real Auth Key authorization was attempted in this UI acceptance run.

The panel refresh was checked again with both browser suites: no page JavaScript errors or external requests were observed. The account suite now covers pasting one API ID/hash pair, rejecting malformed or multiple pairs without replacing fields, metadata-only guidance, and ignoring stale import responses after a sign-in method change or manual credential edit. Six additional focused checks passed for the setup guide, explicit start/pause, empty-search recovery, and final connection/local-guide layout and solid text contrast at 320, 390, and 1440 pixels. The direct-login update adds a single phone/code-request operation and reuses the current workspace's saved API pair for phone, QR, and session login. The full Python suite above includes new persistence, partial-credential rejection, and workspace isolation tests. Browser checks cover direct phone entry, saved-credential reuse, metadata-only routing, one-button file authorization, and duplicate-account rejection. The simplified panel-token and phone forms were also checked without initial scrolling at 320, 390, and 1440 pixels. A compatibility check confirmed the direct phone form can use the earlier configure/code endpoints while an older process is still running.

One user-supplied account was checked separately, outside public test fixtures. Its Telethon, Pyrogram, and TData inputs resolved to the same authorization; the companion JSON supplied API credentials. All four files were loaded through the 0.6.0 panel and Telegram confirmed the expected numeric account ID. Source files remained unchanged. No sources were selected and observation remained off. This qualifies one import/login example, not live collection, recovery, or capacity.

Telegram also issued a real QR token, which was cancelled without scanning. The full QR confirmation and 2FA flows were exercised with synthetic clients; mobile confirmation against a real Telegram app remains a separate acceptance step. No real account identifiers, secrets, or screenshots are included in public files.

The launcher upgrade completed; source, installed metadata, and readiness marker report 0.6.0, with qrcode 8.2 and a passing `pip check`. The installed wheel served the panel and guide, rejected unauthenticated API requests, and independently verified direct and streamed 32-event synthetic exports. The updated offline guide was checked at 320, 390, and 1440 pixels. Public screenshots remain synthetic.

The source release contains 107 allowlisted files. Local documentation links resolve. Docker/Caddy execution, remote CI/package publication, ARM64 runtime, sustained collection, and the full live Telegram acceptance matrix remain unqualified here.

## Version 0.5.1

On Windows 11 / Python 3.12.10, the full project-environment suite passed: **94 passed, 2 skipped**, in 31.21 seconds, with the existing Starlette warning. The skips require POSIX permissions and symlink creation unavailable on this host. The download HTTP fixture printed a request-thread diagnostic; all assertions passed. This run does not establish absence of host transport issues.

New regression coverage exercises rejected StringSession, code and 2FA account changes, cancelled identity lookup, pending login cancellation, and updates through registered handlers on active, rejected, superseded and probe clients. Only the active collector contributes events; saved credentials and signed history remain intact. Other new checks cover Unicode search after reopening a database, inclusion of monitoring-policy boundaries in Coverage, and public-source packaging exclusions.

The actual project `pythonw.exe` launched an isolated synthetic panel, returned HTTP 200 and retained startup diagnostics in `logs/server.log`. The log did not contain the generated panel token or HTTP access records. The test terminated only its own synthetic process. No Task Scheduler task was registered; logon/sign-out, sleep and service recovery remain separate qualifications.

Chromium acceptance passed **45 scenarios**, with no page JavaScript errors and no external requests observed. New checks cover 601/768/850-pixel timeline dates and times, attachment drafts across status refresh, newer edits made while saving, cleared verification results on account switch, late verification responses after switching away and back, and explicit verification boundaries when new events arrive. The search icon/text spacing was also corrected and the browser suite rerun.

The browser run used the pinned runtime in `.venv` and the existing system-provided Playwright 1.62.0/Chromium, appended after the project environment on the import path. An optional development-dependency install was stopped during a slow Playwright download; no new browser-tool version was qualified. A normal `python start.py --setup-only` completed the application upgrade. Source, installed metadata and the launcher's marker report 0.5.1; `pip check` passed. Readiness checks passed on a fresh unused path, retaining the expected local-vault-key warning.

The 0.5.1 wheel was separately installed and smoke-tested: all panel/guide assets were served, unauthenticated API access was rejected, and both direct and streamed 32-event evidence ZIPs passed independent verification. The application files in the installed package were compared against source. The public source archive uses an explicit file-type allowlist and refuses linked source files; runtime material placed inside source directories is excluded by regression tests.

During the code-fix run, the public-source selection and Git candidate set contained 86 files, with no runtime data directories included. A scan for recognizable private-key, GitHub token, Telegram bot-token and StringSession patterns found no matches. This is a bounded pattern check, not a comprehensive secret audit. Ignore-rule probes cover twelve common account/data/export artifacts. Workflow/issue/Compose YAML and the Windows task script parsed successfully. Local documentation links resolve.

All seven findings from the 27 October review are addressed. GitHub workflow execution, Linux/macOS/Docker runtime, real Telegram, outside proxy/TSA interoperability and sustained-load qualification remain outside this local run. No repository publication, service registration or real-account collection was performed.

### English documentation update

The README, account/session reference, collection workflow, and bundled guide now describe supported inputs, workspace behavior, event policies, and export formats in English. The three public screenshots were refreshed using synthetic data. At that point, the public-source selection contained 88 files, including the two new guides. All 131 local links across 23 Markdown documents resolve.

After the interface and guide edits, Chromium acceptance again passed all 45 scenarios, with no page JavaScript errors or external requests observed. The full Python suite was not rerun for this documentation and presentation update; the 94-pass result above belongs to the preceding code-fix run.

The rebuilt wheel was installed into a fresh isolated target. Its panel and guide assets served successfully, unauthenticated API access was rejected, and both direct and streamed exports passed independent verification of 32 synthetic events.

### Installation and deployment update

The focused installer, packaging, and readiness checks passed **14 tests**, with one skip for unavailable symlink creation. Native wrapper checks cover paths with spaces, argument forwarding, setup/demo modes, and nonzero exit propagation. Git Bash checks exercise the Docker shell helper with a simulated daemon, including missing Docker, missing Compose, failed health wait, and a successful alternate-port startup. These simulated checks do not establish Docker runtime compatibility.

A complete public-source copy was installed into a new Windows directory whose path contains spaces. `scripts\Setup.cmd` created a fresh environment and installed the pinned runtime; `Start.cmd --check --json` reported ready without creating its target data directory. `pip check` passed. The rebuilt wheel also passed the installed-package check, including direct and streamed 32-event exports.

Shell syntax and five workflow/Compose YAML files parsed. Source and image Compose configurations agree on storage and runtime settings. At that stage, all 139 local links across 23 Markdown documents resolved. The public-source selection contains 99 files.

The CI definitions now exercise fresh native setup on Windows/Linux/macOS, Compose health/access control/persistence across container recreation, and Caddy configuration. The release workflow gates publication on those checks and adds an emulated ARM64 smoke check. Docker is unavailable on this host: actual Compose/Caddy execution, certificate issuance, ARM64 execution, and remote workflow/package publication remain unqualified locally. The application/UI code was unchanged by this update; the earlier full Python and browser results were not rerun.

## Version 0.5.0

The full pinned-runtime suite passed: **81 passed, 1 skipped**, in 22.00 seconds, with the existing Starlette warning. The POSIX permissions check is skipped on Windows. The new handler tests send messages, edits, scoped/unscoped deletions, reactions, participant updates and membership service messages through different policies. Disabled categories produce no corresponding live observations; coverage diagnostics and explicit snapshots remain available. Tests verify persisted policy, workspace separation, signed before/after audit records, unchanged-policy behavior, strict validation and inclusion in the next process receipt.

Demo entry tests verify that its capability differs from the configured panel token, cannot authorize a live workspace, cannot change collection settings, and is not issued or accepted for remote, forwarded, cross-origin or invalid-Host requests. Opening a stored demo without the explicit demo flag does not enable automatic entry.

Chromium acceptance passed **39 scenarios**, including local demo entry without token input, monitoring presets, the transition from source selection to policy, per-account independence and desktop/320/390-pixel layout and text contrast checks. There were no page JavaScript errors. The host's AdGuard-injected requests remain in the receipt. The download HTTP fixture logged a connection reset after a client closed its connection; assertions still passed. This is not a live-service result.

The normal launcher upgraded the isolated environment to 0.5.0; source and installed versions match and pip check passed. Existing secret-vault encryption, wrong/missing key refusal and signature/media tamper checks passed in the full suite. No new application encryption of message content or attachments is claimed.

The local demo is restarted to make the updated UI available. Existing synthetic records are retained; stopping the old background demo process creates an offline boundary on the next startup. No real Telegram session is used for these checks.

The running localhost:8787 panel returned version 0.5.0, automatic demo access, the five monitoring controls and 33 retained synthetic journal events. The separate installed 0.5.0 wheel served all panel/guide assets, rejected unauthenticated API access, and produced a verified 32-event ZIP both directly and through the streaming download helper. Runtime package versions remain pinned as recorded for 0.4.

## Version 0.4.0

The full pinned-runtime suite passed: **78 passed, 1 skipped**, in 19.77 seconds. The skipped check requires POSIX permissions; the upstream Starlette TestClient deprecation warning remains. New tests cover streamed download/workspace routing, authorization headers, refusal to overwrite, redirects, truncated responses, advertised/actual size limits, bounded reads, cleanup, filesystems without hard links, readiness failures and launcher modes that must not install packages. Export tests confirm workspace-local temporary files and selective orphan cleanup.

Chromium acceptance passed all 36 listed scenarios with no page JavaScript errors. It exercises mock phone/code/2FA login, converted sessions, two workspaces and separate routes/states, observations, signatures, checkpoints and timestamp requests, plus:

- Desktop and 320/390-pixel layouts, no horizontal overflow, visible navigation, and the first login field within the initial 844-pixel viewport.
- Solid-background text contrast at WCAG AA text thresholds. Disabled controls, opacity and image/gradient backgrounds are excluded; this is not a full WCAG audit.
- A real local export response written through a mocked OS file picker/writable, followed by independent ZIP verification; cancellation sends no export request.
- Writable failure aborts the destination; the 128 MiB fallback rejects an oversized advertised response without allocating a matching payload.
- The English local guide on desktop and both narrow widths.

The OS save dialog and actual multi-gigabyte browser writes were not automated or qualified. Python download tests use bounded chunks and loopback fixtures. Full deployment acceptance with real Telegram remains separate.

The normal installer upgraded `.venv` to 0.4.0. Source and installed metadata agree; `pip check` passed. `python start.py --check --json` reported ready on a fresh synthetic path without creating the data directory. Its local-key storage warning correctly remains: journals/media are not encrypted by the application.

The 0.4.0 wheel was built and installed into a separate directory. All 23 application files match the source byte-for-byte. The installed package served the panel and English guide/assets, rejected unauthenticated API access, and exported a synthetic 32-event ZIP that passed verification. Its streaming download command also fetched an independently verified ZIP from the running installed application.

Public documentation and the local guide are English; local documentation links resolve. PowerShell parsed the Windows task template and Python parsed the macOS plist. These are syntax checks, not service execution. No task/service was registered. The CI configuration now includes readiness checks but remote CI has not run here.

The 0.4 browser run again observed host AdGuard injection and Windows asyncio socket-cleanup OSError 10022. Browser assertions passed; these environmental observations are retained rather than treated as fixed application behavior. Initial OpenSSL/browser/pip sandbox attempts failed; the successful qualifying runs used approved execution outside the sandbox.

## Version 0.3.1 focused readiness fixes

The affected launcher, evidence/storage and API checks passed: **31 passed, 1 skipped**, one upstream Starlette warning. The skipped check asserts POSIX directory permissions and cannot establish those permissions on this Windows host. The old-Python test simulates the version/import boundary; no Python 3.10 interpreter was installed or qualified. The previously passing 0.3 suite is recorded below; the entire suite and browser scenarios were not rerun for these focused changes.

The normal launcher upgraded the local environment to 0.3.1; source and installed metadata agree, and pip check passed. A separately installed 0.3.1 wheel served the panel/assets, rejected unauthenticated API access and produced a verified 32-event synthetic export. Workflow YAML parsed, but the new container runtime check was not executed: no usable local Docker/Podman/Linux runtime was available.

See [readiness findings](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) for remaining usability, live-service and platform gaps. This patch does not qualify additional operating systems.

## Version 0.3.0

The full pinned-runtime suite passed: **61 tests**, with one upstream Starlette TestClient deprecation warning. Runtime metadata reports TgWitness 0.3.0 and python-socks 2.8.2; pip check passed. The browser acceptance run passed with no page JavaScript errors.

The 0.3.0 wheel was built and installed into a separate package directory. It served the panel and assets, rejected an unauthenticated API request, and exported a 32-event synthetic journal that passed independent verification. Local documentation links resolve. After the MTProxy bare-key normalization correction, all nine connection/security tests were rerun successfully.

New coverage includes:

- SOCKS5 username/password and HTTP CONNECT through actual loopback test servers; a dead configured proxy fails rather than falling back to the destination.
- Proxy validation, MTProxy transport selection, rejection of Fake TLS ee secrets, persistence, workspace isolation, rejection of changes while observing, and secret exclusion from API status and signed events.
- Read-only conversion of synthetic Telethon SQLite schemas 7 and 8; unchanged source hash; rejection of other formats, SQL views, and an outstanding WAL file.
- External vault master key: different derived workspace keys, successful reopen, wrong/missing key rejection, and no implicit migration of existing local vaults.
- Browser proxy settings, credential clearing, storage-protection disclosure, mobile connection page, converted-session file authorization, separate routes, and all previously covered collection/export scenarios with a fake Telegram client.

During development a loopback test waited indefinitely for peer shutdown; another run observed a Windows connection reset after the handshake. The fixture now bounds the entire exchange and treats EOF/reset after a completed handshake as connection closure. Handshake/authentication assertions remain required. This does not qualify real proxy providers or imply a fixed Telegram transport defect.

The host AdGuard request observation described below still applies. No real Telegram account, outside SOCKS/HTTP proxy, or live MTProxy server was used. MTProxy is experimental and its selected options/secret validation have been checked, not live interoperability. New external-key and session conversion commands were tested with synthetic secrets only. Linux/macOS/Docker remain unqualified here.

The 0.2 throughput measurement below was not repeated and must not be presented as a new multi-account/proxy benchmark for 0.3.

## Version 0.2.0 baseline

Checked on Windows with Python 3.12.10. No real Telegram account was connected.

| Check | Result |
| --- | --- |
| Python suite | 52 passed in the development environment and 52 passed with the pinned runtime; one upstream Starlette TestClient deprecation warning in each run |
| JavaScript syntax | Passed with Node.js |
| Chromium acceptance | Passed; no page JavaScript errors |
| Desktop/mobile layout | Checked at 1440 × 1060 and 390 × 844; no horizontal document overflow |
| HTML-shaped message content | Rendered as text; injected script did not execute |
| Mock account flow | API credentials → phone → code → 2FA → select group → start → snapshot → pause → reload |
| Evidence in browser | Edit comparison, prior content after deletion, filters, ZIP download, checkpoint, signed process receipt, RFC 3161 request download and checkpoint binding |
| Multi-account | Separate journals, keys, sources and live states; browser switch leaves the other collector running; workspaces reopen after restart; duplicate account and account reassignment rejected |
| Cryptographic failures | Changed signed fields, added unsigned fields, wrong key, corrupt archive member, changed/missing media, checkpoint-detected truncation rejected |
| Storage | Concurrent appends verify; update/delete triggers reject; startup refuses a changed journal without appending and releases its lock |
| Media durability | Atomic message/job writes; restart recovery; original version descriptors retained; queue substitution and existing-file corruption rejected; FloodWait persisted; source failures isolated |
| Streaming | Stable prefix exported while new records append; retained checkpoint detects truncated journal; export does not materialize the entire event stream |
| RFC 3161 | OpenSSL 3.5.9 reads generated requests; locally generated synthetic CA/TSA response accepted; altered data, nonce and wrong CA rejected; ambient CA environment does not override explicit trust |
| Local setup | start.py --setup-only upgraded the isolated .venv to 0.2.0; source and installed metadata agree; pip check passed |
| Wheel | 0.2.0 built and separately installed under test-results; served panel/assets, rejected unauthenticated API, exported and verified a 32-event synthetic archive |

The source tests used FastAPI 0.159.1, Uvicorn 0.54.0, Telethon 1.45.0, cryptography 50.0.2, pytest 9.1.1, and Playwright 1.62.0. The pinned runtime uses FastAPI 0.162.0, Starlette 1.10.0, Uvicorn 0.54.0, Telethon 1.45.0, and cryptography 50.0.2. deploy/constraints.txt records runtime version pins; deploy/requirements.lock and deploy/build.lock add the SHA-256 of every package file, and Docker and high-assurance servers install only from them (pip --require-hashes). Neither is evidence of compatibility on every configured CI platform. Remote CI has not run.

## Synthetic local capacity measurement

Command: `python tools/check_capacity.py --events 10000 --chats 100`

| Metric | Observed |
| --- | --- |
| Input | 10,000 synthetic message events across 100 synthetic selected sources |
| Message text | 400 characters; no media or network |
| Ingestion | 53.273 seconds; 187.7 events/second |
| Handler latency | p50 4.162 ms; p95 7.784 ms; maximum 129.118 ms |
| ZIP export | 19.868 seconds with tracemalloc enabled |
| Peak traced Python export allocations | 0.51 MiB; not process RSS |
| ZIP size | 4,610,962 bytes |
| Independent verification | All 10,000 events verified |

This measures the local serial recording/export path on this Windows host. It does not measure MTProto delivery, concurrent accounts, Telegram throttling, media, a long-running workload, or a guaranteed number of real chats. The measurement predates the final offline timestamp tooling, which does not change the measured message path.

## Environmental observations

Windows sandbox restrictions blocked the default pytest/pip temporary directories and the Playwright subprocess. Pytest used a new temporary directory inside the project; installation and browser processes required approved execution outside the sandbox.

The machine's AdGuard injected requests to local.adguard.org into the browser. The browser receipt retains those requests. This run is **not** evidence of zero outbound requests in an unmodified browser environment; the app source itself contains no external asset/CDN/analytics requests. AdGuard settings were not changed.

The final browser run also logged a Windows asyncio socket-cleanup OSError 10022. All browser assertions passed and no page JavaScript errors occurred. Its cause was not established and this run does not demonstrate absence of host transport issues.

The first installed-package HTTP probe using urllib's connection-close requests encountered connection resets, both inside and outside the sandbox and with both dependency sets. The final probe used standard HTTP/1.1 persistent connections via http.client and passed. Browser requests also passed. The precise origin of the resets was not established; they were not labeled a fixed application defect.

## Remaining qualification

The retained live journal establishes real collection, edits, deletion notices, attachments, rechecks and rate-limit handling. It does not establish exhaustive delivery or a controlled matrix of role visibility, reaction actors, prolonged FloodWait, account bans and network/process interruption recovery. QR-token issuance remains distinct from completed mobile QR confirmation.

Docker build/run, Linux/macOS installation, sustained high load, independent security review, a real independent TSA response, certificate revocation/archival validation and forensic certification remain outside the recorded qualification. Saved MTProto state and catch-up are implemented; atomic durable replay remains unestablished. Admin-log collection, extra reactor lists and priority short polling remain separate features. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

Local detailed receipts and screenshots are under test-results/ (Git-ignored). The public screenshot in docs/assets/ contains only fictional demonstration data.

## Public website and publication preparation · 27 October 2026

The separate `website/` presentation and Pages build were added after the panel checks above. No live account configuration or collection logic was changed.

- The existing application suite passed: 138 passed, 1 POSIX-only skip, and one upstream Starlette/httpx deprecation warning. The 11 added site build tests passed independently, including unexpected-output rejection and linked-input rejection.
- Both application browser scripts passed using project-venv Playwright and Chromium headless shell 156. No page JavaScript errors or external requests were recorded. All account scenarios used fake transport and fictional data.
- `tools/check_site.py` passed at widths 320, 390, 768, 1024, and 1440, with a project URL subpath, keyboard tabs, successful/denied clipboard access, reduced motion, and disabled JavaScript. No failed asset requests or external requests occurred.
- `tools/build_site.py` produced 10 allowlisted public files, about 460 KB total. Browser screenshots and a receipt are in ignored `test-results/site/`.
- The wheel built successfully after installing the build-only setuptools/wheel tools in the project environment. Installing it into an isolated target and running `tools/check_install.py` passed: static assets, access control, a signed 32-event synthetic export, and independently verified streaming download.
- `pip check` passed. A pattern scan of Git-selected public candidates found no recognizable private-key blocks, GitHub/bot/AWS tokens, long literal secret assignments, or merge-conflict markers. This is not proof that every possible secret format is absent. Runtime-data/session/key probes were Git-ignored.
- GitHub CLI authentication was invalid; no remote was configured and no initial commit existed. No push, hosted workflow, Pages deployment, or release was performed. Docker and live Telegram/platform qualification remain outside this check.

On this host the Playwright download lock failed on the E: workspace filesystem. Installing Chromium under `%LOCALAPPDATA%/tgwitness-playwright` and using that same `PLAYWRIGHT_BROWSERS_PATH` for the checks succeeded. This is an environment workaround, not a change to the application's runtime dependencies.

## Interactive documentation and website metadata · 29 October 2026

The public site builds 12 English HTML pages: a homepage, a guide index and ten guides. The artifact contains 28 explicitly listed presentation files, approximately 1.85 MB, and no collector data. The public website is English; application translations and translated repository guides are separate.

- Site, source-publication and release-boundary tests: **18 passed, 2 skipped**. The skips concern symlink creation on this Windows filesystem. Tests check unique page metadata, English-only public pages, canonical URLs, all sitemap entries, local assets/anchors, structured navigation and private-file exclusion.
- Both `tools/check_site.py` and `tools/check_docs_site.py` passed in Chromium at 320, 390, 768, 1024 and 1440 pixels under a project URL subpath. The guide checks cover all 11 documentation pages, search and keyboard navigation, clipboard success/refusal and readable content without JavaScript.
- Five interactive examples passed: message playback/step/pause/reset with reduced motion and off-screen suspension; original/altered/rebuilt/truncated hash chains; witness acceptance/rollback/fork/no-response decisions; and complete/delayed/missing delivery scenarios; and an investigation map linking fictional cross-chat observations by sender ID, destination and attachment hash. The investigation controls passed keyboard navigation and no-JavaScript fallback checks. Browser SHA-256 results were independently compared with Python's `hashlib` and canonical JSON. The hash example also retained its readable fallback when Web Crypto was unavailable.
- Delivery ratios and chart markers matched the accessible table. Mobile axis labels were enlarged after visual review. Every example is labeled as illustrative or synthetic, and no browser example contacts Telegram.
- No external requests, failed HTTP requests or JavaScript errors were recorded. Desktop/mobile screenshots and receipts are under ignored `test-results/site/` and `test-results/docs-site/`. The documentation index, message/hash examples, witness layout, delivery chart and investigation map were inspected at desktop/mobile sizes.
- The publication scan passed for 282 public source files and 1,426 local documentation links. Ruff passed for the modified Python site tools and tests.
- `docs/HOW-IT-WORKS.md` provides a GitHub Markdown companion with Mermaid diagrams and formulas. `docs/INVESTIGATION.md` covers whole-account scope, per-chat history acquisition, people profiles, cross-chat references, timelines and a verified case handoff. Its steps and limits were checked against the current scope, collection, dossier, export, verifier and panel code. Hosted GitHub rendering was not checked.

This is a local website/documentation check. It does not add live Telegram qualification or establish hosted Pages deployment, remote CI success or search engine indexing. See [the publishing procedure](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md) and [the website metadata notes](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/SEO.md).


---

# Licence and architectural incompatibility notice

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/license/

TgWitness is MIT-licensed for everyone, and why it is architecturally incompatible with the Taylor Wessing workflow.

TgWitness is distributed under the [MIT License](https://phishdestroy.github.io/TgWitness/LICENSE). Our position adds no licence condition.

> A signature does not turn a lie into a fact.
>
>
>
> TgWitness is a poor fit for corporations, law firms or individuals who believe that putting "Dr." before a name makes whatever follows it true. Titles, letterheads and signatures do not override evidence.
>
>
>
> If your workflow starts with the conclusion a client paid for and requires the record to follow, you are looking for a different tool. TgWitness exists to preserve the record and make it open to examination.
>
>
>
> Let those "doctors" tend to their corporate clients' balance sheets. A title does not cure a lie.
>
>
>
> Mathematik verhandelt nicht.

[Source record](https://phishdestroy.io/steam_dossier/taylor_wessing) · [Ethical Notice & Historical Continuity](https://phishdestroy.github.io/TgWitness/docs/reference/notice/)

[Full MIT Licence](https://phishdestroy.github.io/TgWitness/LICENSE) · [Project](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Documentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Home.md)


---

# Operator incompatibility notice

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/notice/

Our operator notice on Taylor Wessing and its source record.

**PhishDestroy · TgWitness project notice**

[Source record](https://phishdestroy.io/steam_dossier/taylor_wessing) · [Original NOTICE](https://phishdestroy.github.io/TgWitness/NOTICE)

## ⚖️ Ethical Notice & Historical Continuity

We have recently learned that for certain law firms—and specifically Dr. Tobias Schelinski and Dr. Patrick Vincent Zurheide—mathematics and objective facts are irrelevant.

Selling GDPR non-compliance to corporations as a commercial service while failing at basic data handling yourselves is not legal expertise.

Operating under the delusion that you are the law, or that an elite signature on a falsified claim magically turns a lie into truth, does not mask technical incompetence.

This tool is incompatible with jurisdictions where the following prevail:

- Corporatocracy
- Privatized or commercial justice
- Plutocracy
- Kleptocracy and institutional corruption

A special mention to Dr. Patrick Zurheide, Dr. Tobias Schelinski, and those attempting to weaponize the "Right to be Forgotten" to bury their own data-processing failures, sanitize their institutional lineage, and erase the historical record:

> Taylor Wessing (Dr. Tobias Schelinski & Dr. Patrick Vincent Zurheide) → Wessing & Berenberg-Gossler → Stonewall Top 100 → Dr. Graf von der Goltz Dr. Wessing & Partner (since 1957) → Rüdiger Graf von der Goltz → Paragraph 175 in its 1935 revision

To strictly comply with the MIT License, we do not restrict the use of this software. However, let it be clear: corporate retainers, legal intimidation, and demands for digital erasure cannot override history, rewrite lineage, or conceal the truth.

[MIT License](https://phishdestroy.github.io/TgWitness/LICENSE) · [Our position on Taylor Wessing](https://phishdestroy.github.io/TgWitness/docs/reference/license/) · [Evidence model](https://phishdestroy.github.io/TgWitness/docs/reference/how-it-works/)

[Project](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Documentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Home.md)


---

# Changelog

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/changelog/

Every change by version, including the changes not yet released.

## Unreleased

## 0.8.1 preview · 2 November 2026

- Build the runtime, sealed and media containers on a pinned Wolfi/glibc base with Python 3.12 and hash-locked system packages for AMD64 and ARM64, authenticated through signed repository indexes.
- Build Tesseract 5.5.4 from verified source and pin its English and Russian recognition data. Preserve the existing Python dependency locks.
- Check real OCR and offline transcription, signed multilingual PDFs, installed source measurements and container restrictions. Include all container build inputs in the source archive and scan the ARM64 runtime before publication.
- Integrate **Extras → Independent capture** into the English main panel: separate browser/AyuGram connections, encrypted control tokens, pinned identity checks, tab selection, start/pause, capture options, snapshots, checkpoints and verified original ZIP downloads. Add optional Docker control-network wiring; keep recorders independently runnable and all connections disabled by default.
- Add the optional, independent `tgwitness-capture` preview: selected-tab Chromium PNG/MHTML, consistent AyuGram SQLite snapshots, separately enabled silent video, Ed25519 event chains, signed ZIP/HTML reports and standalone verification. Each recorder starts disabled and keeps its own key and storage. Optional Compose profiles are separate from ordinary startup. A read-only, separately operated witness can retain challenge-bound checkpoints and sign receipts.
- Include the independent capture package in Phala source bundles and their manifests, so the panel can import the capture integration after installation.

## 0.8.0 preview · 2 November 2026

- Apply sharing-copy text and contact controls to interaction records, and include chat metadata only for the selected chats.
- Keep pending confirmations bound to their original workspace, group and session. Mask detected secrets in Case Board source context until an explicit reveal.
- Keep the new panel session active after rotating its access token. Events from the old connection cannot sign out the replacement session.
- Preserve the collecting account's attribution when recovering missing messages in multi-account exports, and verify the completed archive before marking it ready.
- Show the AI endpoint and outside route in the data preview. Server-local AI requires an explicitly selected Direct outside route; a route change requires a new preview.
- Documentation: a [panel guide](https://phishdestroy.github.io/TgWitness/docs/reference/panel/) for every screen, protection modes and the code check; Discord publication and the public proof page in [witness](https://phishdestroy.github.io/TgWitness/docs/reference/witness/); removing an installation; current panel labels throughout.
- Group screen at `/groups/<id>`: accounts, problems, shared chats with coverage, group export.
- Add Reading series and Ledger & margin to the report builder, with distinct HTML and native signed PDF chapters, live preview, account and sharing layouts, and DeepL translations. Preserve selected scope and minimized data across designs.
- Add Classic, Editorial, Briefing, Analytics, Technical and Overview report designs with independent covers and typography; changing a design keeps filters, charts and written notes.
- Show separate send, edit and observation times, reply/thread references and permitted message metadata in reports and the viewer.
- Add a private Case Board with signed, append-only bookmarks, exact-version Unicode highlights, complete action slices, scoped collections, threaded comments and team statuses. Chats/Journal shortcuts, live updates, source navigation, presentation and UI in all 25 panel languages keep team interpretation separate from observed evidence. Signed ZIPs bind the annotations head and recomputed slices; the standalone verifier checks replay, references, query excerpts and retained checkpoints. Reports have independent board/comment controls; minimized handovers require explicit inclusion and support investigator aliases. New board rights do not expand existing grants, and export permission alone does not disclose team notes.
- Account groups now share settings. The group page sets the goal, collection, protection and notification rules, recording, recheck schedule, report settings, parameters and connection route; members follow it, and an account with its own value keeps it until it is returned to the group's. Settings marks each value 🔗 (from the group) or ✏️ (own). A change previews which accounts it reaches and asks per account before overwriting an own value; accounts added later start with the group's values. Notification destinations, proxies and sign-in stay per account, as does starting and pausing collection. Access can be granted to a whole group, including accounts added to it later; showcase links still list their channels. Every change is recorded in the signed journal of the main workspace and of each member it reaches; existing template groups are migrated.
- Add Report studio with independent document designs, live unsigned cover/chart preview, selectable activity, weekday/hour, participant, chat and composition charts, and journal history/indicator controls. Saved choices reach HTML, signed PDF/JSON and new account/disclosure jobs. Analytics use only included/minimized records, retain unknowns and bounded-grouping counts, and ship as manifest-protected `analytics.json`. Designs are independent of content presets. Author-written examination notes and source-linked journal statistics retain the published privacy defaults; minimized journal handovers exclude that private analysis. Existing signed exports remain unchanged.
- Configure report data by chat, author, UTC observation dates and event type. Preview real activity, participants, messages and missing-ID ranges before saving. HTML, PDF and JSON apply the same scope while preserving the original signed journal. Edits show Before/After text; deletions show previously saved content, with out-of-selection history explicitly marked as context.
- Preserve workspace-specific deep links through first setup, keep the shared account form current in Settings, and expose file import when adding an account. Compact mobile connection controls keep the account identity visible.
- Cancel pending Settings confirmations and setup continuations when their workspace changes, including accounts with identical configuration revisions.
- Keep a valid panel session through temporary startup/network failures and offer Retry. Expired or revoked access still returns the browser to sign-in.
- Run both panel regression suites on pull requests, including download checks in Firefox and WebKit. Release packages now wait for the exact revision's dependency, CodeQL and container audits; HIGH/CRITICAL container findings block publication.
- Renew an imported session in its existing workspace, expire history retries when leaving a chat, and keep bot controls disabled until the previous action finishes. Analysis previews use audited secret masking without changing model input or exports.
- Stream large account archives and sharing copies through one-use browser downloads; block job deletion until active transfers finish. Reject stale commands after changing the operator bot and serialize its start/stop commands with panel operations.
- Validate local originals before changing storage destinations or importing older recovery metadata, including native S3 settings. Recovery files cannot mix incompatible destinations.
- Inspect account files before connecting: settings-only JSON cannot be imported as a session, paired files are checked together, and additional accounts get their own workspace. Connected accounts and typed-name deletion are visible on Account.
- Keep URL, workspace selector and loaded account in agreement. A mismatch blocks actions. Exports and Telegram actions name the account in their confirmation. Chats open read-only, mask detected secrets without rewriting originals, and journal reveals. Empty chats can load history with a result or a retry.
- Fall back to ordinary downloads when the browser refuses its file picker or writer. Prepared journal exports retain their size, SHA-256 and a download-again action. Journal numbering, missing-time text and chat date spacing are clearer.
- Add a searchable notification-service catalog, service icons, an optional operator-owned control bot and Discord witness publication. Storage separates backups, verified attachment offloading and evidence retention. Recovery checks signatures and file hashes; exports require selected offloaded files to be restored. Investigation sources can be handed off as Markdown and JSONL.
- Reports now use a coordinated dossier design: case cover, prominent figures, linked evidence map, numbered findings and an observation/gap timeline. Signed PDFs have an A4 cover with identifying QR, a summary, bookmarks and page references; HTML remains offline, responsive and printable. Account and sharing copies use the same visual design. A fresh signed fictional example can be built with `tools/build_dossier_example.py`; see [case reports](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/).
- Signed reports now explain the trust basis for the specific archive, with separate export-time checks, recorded observations, missing material and independent review steps. HTML, PDF and signed JSON/manifest assessments share the same facts; English, Russian and German wording is available. Timestamp conclusions require a trusted certificate signature and a checkpoint bound to the exact journal prefix. See [case reports](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/).
- Added six-step first setup and a unified Settings page with simple, standard and expert presentation levels. Language, device time zone, theme and progress are saved per operator and workspace; language changes preserve the panel session.
- Copy, monitoring and evidence presets show a diff before changes, preserve optional manual overrides and expose hidden settings through search. External-service permissions are checked when enabling timestamps, notifications and off-site copies.
- Automatic connection tries public MTProxy, portable WARP, then an explicitly allowed direct route. Checks, a persistent status indicator and recovery actions replace silent proxy failures. HTTPS CONNECT verifies the proxy certificate.
- File policies can limit video duration; capture and account export enforce the configured size and duration. Existing journals and stored configurations stay intact. See [first setup and settings](https://phishdestroy.github.io/TgWitness/docs/reference/settings/).
- The first setup and Settings are translated into all 25 panel languages. Each step has its own address and browser Back moves between steps. The Telegram step asks whether the account is separate; a main account records only chosen chats, also when Settings change the chats later. Start stays on the setup and shows that the connection, event intake, sources and attachments work before offering what to do next. A change of IP protection through Settings is a signed journal record, and the journal names the new connection and settings records.
- Fixed Windows portable packaging of fpdf2's public colour profile and licence; private workspace files and generated caches remain excluded.
- Translated the guided connection controls and documentation into 24 additional languages.
- Added a guided Connection screen: choose accounts, prepare and check a route, then review and apply it. Direct, own proxies, the public MTProto pool, imported WireGuard profiles and portable WARP are available. Group changes preserve custom routes by default, check again before switching, pause active observation and report failures per account. WARP/WireGuard helpers stay in the data folder, use pinned SHA-256 downloads and stop when the owning panel exits.
- Long labels no longer spill on phones: the Sources tabs wrap their text, and the journal's period buttons wrap to a second row instead of five fixed columns. Russian gains the missing route, IP protection and administrator key confirmations; a working part of the status strip reads "Работает" and the custom period "Другое".
- Added signed HTML, JSON and PDF reports with an offline viewer, verified selections, archive sidecars and configurable report contents in all 25 panel languages.
- Added minimised journal handovers, message details, indicators, collection clock/profile receipts, absent-ID rechecks and admin-log context. Existing signed records remain verifiable.
- Added workspace protection modes and clearer account-loss reasons; packaged report fonts and assets for wheel and source installations.
- No consequential action on a single stray click. In Sources the status badge only shows the state; pausing, resuming, excluding and removing are in the row menu, each with what it does, pausing and excluding are confirmed (also in bulk), and removing a source asks for its name. Sending from a chat is closed until "Write as @account" is chosen, warns that chat members see the message and that the action is journaled, and is refused by the panel and the API for the Evidence for a case goal. Changing the connection route while observing shows a warning with one button that pauses and opens the route settings. The sticky chat date now sits on a full-width band.
- One set of numbers and statuses across the panel. Chat counters separate messages deleted with their text kept, deleted before any text was saved, and not found on recheck; the chat list, chat header and notifications use the same definitions (the notification states that it covers one hour). The journal's read index is rebuilt once to add this split. A source that keeps delivering records is "receiving updates" rather than unconfirmed when the account's chat list does not show it, and an unconfirmed source says why. The chat header lists attachment limits per type instead of the largest one. The priority star has one name and explains the recheck interval. Investigation mode saves what it describes after the whole-account confirmation. Hide-address mode with outside requests but no proxy for them says that timestamps, notifications, off-site copies and proxy-list updates are blocked, with buttons to set a proxy or turn those requests off. Without a chosen goal, the setup card says what the configuration already amounts to.
- Access can publish a separate public-channel showcase: captured text, saved edits/deletions and signed collection snapshots. Author fields are redacted; attachments and ordinary panel APIs stay closed. Links expire and can be revoked. The original journal is unchanged. Includes an offline snapshot/continuity verifier and synthetic API/browser regressions. See [Showcase](https://phishdestroy.github.io/TgWitness/docs/reference/showcase/).
- Panel fixes. The journal no longer stops at a skipped-attachment record ("mediaTypes is not defined"), so its record count and Newer/Older paging stay correct. Confirmations and name prompts are panel dialogs instead of `window.confirm`/`prompt`, which embedded and some mobile browsers refuse; deleting a workspace asks for its name. A direct `/chats/<id>` link no longer shows the previously open chat first. The live status reads "Page updates" so it is not mistaken for the Telegram connection. Chat filters no longer overflow in longer translations, the sticky chat date keeps clear of message text, the report settings link focuses the report language, hints no longer cover an open notification panel, an empty journal overview and an empty group list say what to do next, and the system log keeps each uvicorn line once.
- Preserve an active Telegram sign-in when workflow navigation finishes late. Returning through account export or investigation keeps the pending code, password or QR step instead of resetting the form.
- Added a guided 24/7 server in Extras → Server 24/7: on the local panel, a region and a Hetzner token are enough to review the type, monthly price and version from Hetzner's API, then run `deploy` with live progress. Without a domain the server gets a quick tunnel (`--quick-tunnel`): a random trycloudflare.com address that it posts, signed with a key kept by the deployment, to ntfy.sh, where the panel finds it again after a restart. A Cloudflare token adds an address under your own domain. Tokens are never stored and never accepted by a panel reached over a network. New `python -m tgwitness.cloud destroy` removes a deployment's server, firewall, DNS records and tunnel, including what a failed deployment left behind. `tools/check_cloud_wizard.py` covers it offline; the quick tunnel path was also run against real Hetzner Cloud. See [high assurance](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/#from-the-panel).
- Evidence mode has two optional records under **More witnesses**, both off by default: the newest drand round (League of Entropy, first from Cloudflare's relay), which shows the records after it are newer, and Telegram's list of the account's signed-in devices without IP addresses. `verify.py` reports both; `--check-drand` compares the rounds with Cloudflare and Protocol Labs relays. The drand path ran against the real relays. See [evidence](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices).
- Added Gateway DNS for a 24/7 server (`--gateway-dns`, **Cloudflare Gateway DNS** in the wizard): the server resolves only through a Cloudflare Gateway location over TLS, Hetzner's firewall blocks DNS to anything else, and `verify` checks that firewall, the location, logging, Gateway policies that could rewrite answers, the server's queries and the audit log. Evidence mode can copy the location's log into the journal (`cloudflare.gateway_dns`) and `verify.py` summarises it. Free accounts share their one location, told apart by address. Ran against real Hetzner Cloud and Cloudflare; `tools/check_gateway_dns.py` covers it offline.
- Added setup by goal in Extras → Goal & protection level, offered on Start here until it is answered or skipped: four questions (what for, how much, photos and files, where it runs) lead to suggested settings, each with one line on what it adds, and two scales, credibility and reliability, computed from what is actually set. Apply changes only timestamps, drand, the device list, the attachment policy and two parameters, each recorded in the journal as usual plus `setup.applied`; notifications, an off-site copy, a server, the code check and a witness bot are offered as next steps with their own forms.
- Added Phala Cloud for a 24/7 server (`--provider phala`, **Confidential virtual machine · Phala Cloud** in the wizard): the collector runs in an Intel TDX confidential virtual machine whose compose pins the commit's source files and both images by hash. `verify` checks each Intel attestation up to Intel's root itself (`tgwitness.tdx`), the measured compose, the instance and, with `--tdx-measurements`, the OS image; every start in the journal carries an attestation too. Works with the quick tunnel; `destroy` removes the machine. `tools/check_tdx.py` and `tools/check_phala.py` cover it offline; not yet tried on Phala Cloud itself. See [high assurance](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx).

## 0.7.1 preview · 1 November 2026

- Fixed chat profiles getting stuck after navigating away while a request was loading. Reopening the view can retry, and an outdated request cannot overwrite the current chat's profile state.
- Added a clear handoff after download: distinguish the original archive from sharing copies, review the report, and copy plain instructions for the recipient. Polling preserves the selected copy and focus; unavailable clipboard access leaves the instructions selectable.
- Added recipient guidance and stable record references to readable account and sharing reports, including print layouts. References describe the archived document; they do not turn printouts or screenshots into signed evidence.
- Added a browsable fictional report with the matching signed ZIP. Its preview is byte-identical to the archived HTML; previous signed demo samples are retained.
- Added missing translations for export controls, sharing copies and recipient reports in all 25 interface languages. Message text and content entered by the operator keep their original wording.
- Added **Start here** with separate personal-export and investigation journeys. Account snapshots and saved observations now have distinct export controls; secondary formats, account metadata and connection options are progressively disclosed. Navigation preserves drafts and never starts collection implicitly.
- Replaced disclosure JSON previews with readable transformed-message cards, exact included-record counts and explicit sample limits. Original archives remain separate from sharing copies, and privacy warnings remain visible.
- Added printable offline reports for account exports and sharing copies, with scope, coverage, readable messages and verification instructions. Choose the report language separately from the panel; original message text stays intact. New labels use explicit English fallbacks where translations are unavailable. Existing signed jobs and already published archives retain their original bytes.
- Distinguished rejected Telegram authorization from paused accounts and network failures. Account counters filter the list; **Sign in again** returns to the existing workspace without discarding its journal, sources or signing key. This state follows actual authorization checks; simply opening the panel does not probe every saved session.
- Made large account-export progress and HTML preparation use linear task/page scans. Interrupted ZIP writes leave no downloadable partial archive; regression checks resume from byte-identical signed receipts and retain coverage gaps.
- Strengthened disclosure masking for Unicode names, alternate usernames, direct-chat names and whole-token sender IDs, including the public purpose. Unknown senders no longer receive a shared identity alias. Exceeding the masking limit now stops preparation rather than silently skipping identities.
- Bound transcription by actual decoded audio samples, decode only once, and reject playlist formats and secondary file/URL references inside the isolated media worker. Native decoder checks cover generated common Telegram formats and malformed input without downloading a transcription model.
- Made source ZIP metadata repeatable and preserved the previous archive when a new build fails before publication. Input bytes, including signed demo files, remain unchanged; reproducibility requires matching inputs and compression tools.
- Capture now displays English text when a translation is missing and respects the user's language choice.
- Hardened Capture language selection and encoded its HTML/URL output, pinned release actions, and documented the dated security scan results, including unresolved Debian package findings in the container images.
- Updated Russian wording in the panel and Capture wizard, including privacy and evidence terms. Placeholders and command examples are preserved.
- Raised dependency security floors and regenerated the hash-locked build tools. Notification services now refuse HTTP redirects, including URL-level redirect overrides, so credentials cannot be forwarded to a different endpoint. Configure the final notification endpoint directly; HTTP 3xx responses fail delivery.
- Added weekly Dependabot updates, checks for pull requests on hosted runners, and nightly dependency, CodeQL and container vulnerability scans. Custom dependency locks remain reviewed and regenerated together with version changes.
- Fixed quick search after rapid close/reopen and temporary parameter API errors. Browser checks run two at a time with individual logs and a complete result summary, including checks after a failure.
- Corrected archive-search date defaults across daylight-saving transitions so recently captured records remain inside the selected period.
- Added configurable account export through Telegram Takeout or the explicitly selected regular API. Jobs retain signed progress, support pause/resume and produce a reusable ZIP with coverage and omission records.
- Added separate signed disclosure copies with purpose, sender/date/text filters, participant pseudonyms and optional text/file exclusions. Preview is bound to the administrator session and source archive. Signatures establish integrity; they do not establish Telegram authorship, completeness or legal admissibility. See [account export](https://phishdestroy.github.io/TgWitness/docs/reference/account-export/) and the [Russian guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/ACCOUNT-EXPORT.md).
- Added fictional account-export and disclosure downloads to the online demo.
- Added workspace-aware panel URLs, Back/Forward navigation and an active-view lifecycle. Background updates preserve form drafts and focus; settings can be saved with Ctrl/Cmd+S. Submitted secrets never become a Discard baseline.
- Reorganized Sources into Scope, Chats and Recording with one recording save; Parameters now have search, section links, inline validation and a reset preview.
- Kept chat navigation and messages in separate scrolling columns, with compact actions, source filters, priority and distinct conversation views/message filters.
- Added combined journal filters, cursor windows and a desktop record inspector. Routine system events are hidden by default and remain available with a toggle.
- Added grouped notifications, focused health actions, workspace summaries and access presets. Export preparation history records byte counts and hashes without changing signed evidence. See [panel development](https://github.com/phishdestroy/TgWitness/blob/main/docs/FRONTEND.md) for module ownership and the remaining extraction plan.
- Serve read-only MCP at the panel's `/mcp` endpoint. Connections select their tools and scope, support token rotation and report recent use. Client setup uses `tgwitness.mcp_server` and `TGWITNESS_MCP_TOKEN`; the runtime check provides an installation command when the optional SDK is absent. Setup forms keep their drafts, and protocol checks list tools without reading messages.
- Keep report settings separate when switching workspaces. Cancelled exports finish their file worker before releasing the lock and remove temporary data; failed downloads clean up too. Scoped source actions return only allowed chats.
- Refuse account/connection replacement during exports; roll back interrupted collector startup and bound TLS shutdown. Local export write failures stop immediately instead of skipping records. Verify signed attachment and avatar references during export checks and backup restore, and reject invalid TSA certificate constraints and broken storage pagination.
- Kept disabled AI out of the sidebar and attachment actions. Provider setup lives in Integrations; local recognition appears only when its worker is configured. Connection settings now show the fields for the selected route, with the automatic MTProxy catalog available on demand.
- Added inline and side-by-side edit comparisons, separate changes to hidden links and bot buttons, attachment previews and image zoom. The preserved original stays downloadable. Preview reads stop at 32 MiB; the browser cache holds at most 40 previews and 64 MiB, with three concurrent reads, and is cleared on lock or workspace switch.
- Added live journal/chat updates with a pause control for the view, batch source selection and actions, and journal search from Ctrl/Cmd+K. Live updates recheck access and chat scope; pausing the view does not pause collection.
- Indexed saved message state and source summaries. Existing journals build these derived indexes once during their first startup after the update; signed records and their hashes stay unchanged. Small and expiring attachments have a separate download lane so a large file does not hold them up.
- Preserved observed avatar changes as signed records with content-addressed files, including removal and reuse of an earlier photo. People profiles show scoped history and similarity leads; saved photos travel in evidence ZIPs.
- Added automatic upgrades for OpenTimestamps receipts older than one hour, with bounded requests through the configured route and the original receipt retained. A Bitcoin attestation remains explicitly unverified until checked independently.
- Reworked the workspace navigation and chat layout, added chat search and kept collection warnings visible. The desktop conversation fits the viewport.
- Rebuilt the online demo around a fictional investigation with named participants, edit comparisons and real signed sample downloads. Verification results now stay visible; unavailable online-only actions no longer look usable.
- Added batch session import and account groups with template settings. Failed imports leave no empty workspace; locking or switching stops the remaining queue.
- Added the MTProxy dashboard: ping, status, countries, filters, shared custom lists and optional GitHub search. Routes remain separate for each account.
- Added a country choice for the automatic MTProxy route (preferred, avoided, only preferred) and the list download and check intervals to the dashboard. Panel strings of groups, import and the dashboard are translated with their screen as context and with plural forms; context-dependent report labels are corrected in 23 languages.
- MTProxy traffic is deciphered through OpenSSL instead of Telethon's pure-Python AES (about 0.3 MB/s on a small server): a busy MTProxy route no longer holds a whole CPU core and delays every panel answer by seconds. The chats list shows that it is loading, and journal rows explain skipped and failed attachments in the panel language.
- The panel, proof, sealed and MCP servers keep idle connections for 150 seconds instead of 5: Caddy and cloudflared reused connections the server had already closed, and the browser received sporadic 502 answers.
- GIFs and stickers are no longer downloaded unless turned on. Turning downloads off now pauses the files already waiting, and turning a type off or lowering its limit skips the waiting files it excludes; before, the queue kept downloading under the old settings.
- Public proxy lists are parsed once, and again only after a list, a source setting or the GitHub token changes. Every status read of every workspace parsed them on the event loop that also carries Telegram traffic; with 10 workspaces the account list took 690 ms, now 7 ms.
- Bulk import refuses a session another workspace already holds before it connects: the same key from a second proxy address can make Telegram revoke it. An imported workspace disconnects until its sources are chosen, imports no longer hold the other workspaces' operations, an import can be stopped after the current account, files that are not account files are shown as such, and import errors appear in the panel language. Account groups can start or pause all their workspaces at once.
- Unanswered servers in preferred countries no longer hide working servers in other countries; servers identified as being in avoided countries are excluded, including from checks. Servers with unknown country remain eligible unless only preferred countries are allowed. Country lookups move past hosts without an answer, the saved lists stay readable at their size limits, the last list update shows when lists were actually downloaded, and a blocked list download disables the update button and offers the proxy setting. Own lists say how many links were left out and why. One server listed with several secrets counts as one address, so two workspaces are no longer put on the same server.
- People and chats without a photo no longer fill the browser console with 404 errors, and the panel asks for the high-assurance statement only where it exists. Sign-in tabs wrap long labels instead of cutting them; the offline-gap note, size units and the reason of attachments dropped with a removed source are shown in the panel language.
- Added scoped, read-only MCP connections and local archive search with optional AI source review and separate analytical reports.
- Added local OCR/transcription for saved attachments and signed outgoing webhooks with delivery status, retries and an n8n example.
- Connected the new workflows across README, Wiki and translated site reference.
- Sealed, localized reports. `report.html` and `chat.html` are rebuilt as self-contained case documents in any of the 25 panel languages: case details, integrity and key fingerprint, timestamps with their check commands, coverage, chain of custody with a printable transfer table, verification steps, standards and limitations. Each ends with an Ed25519 seal over its own bytes, checked in the browser or by `verify.py report.html --fingerprint … --evidence …`. Reports carry Dublin Core and schema.org metadata and a Content-Security-Policy that blocks network loads; the chat report shows the history oldest first.
- Signed archives add `custody.json` and `SHA256SUMS`; README.txt is written in the report language and in English. Case details from **Exports → Report settings** are signed into the manifest. `verify.py` checks the seal and the sums, prints a coloured summary at a terminal (`--lang en|ru|uk`) and offers `--json`.
- Added a five-stage capture animation and examples of message/collector substitution to the helper and Exports.
- Replaced the separate capture form with a four-step wizard shared by Exports and the standalone page. It uses workspace themes and controls, explains each file handoff, confirms key saving and clears its key when the workspace locks. The temporary Telegram panel also uses workspace styling and readable progress.
- Added entry points for the GitHub Actions capture preview on the workspace login screen, in Exports, on the project homepage and in the documentation. Entry labels are translated; the English/Russian helper preserves the chosen language. Expanded setup, privacy boundaries, mode selection and troubleshooting.
- Added a fork-launched sealed capture preview: restricted fresh-session login, one-chat history and media collection, encrypted connection/result artifacts, pinned reusable-workflow provenance and a fail-closed verifier. English/Russian browser helper keeps the private decryption key local. This uses ordinary GitHub infrastructure, not confidential hardware or Telegram-signed evidence. See [sealed capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) for setup, policy and deployment limits.
- Sources can load the available history of every currently enabled source into Chats and the signed journal. The persistent queue supports pause, resume and explicit continuation after restart, with separate per-source failures and media outcomes. It does not enumerate every account dialog or recover unseen deletions.
- A signed history progress report can be checked with `verify.py --evidence`: verify the journal prefix, source plan, account and message counters. Other report fields remain signed collector statements; this does not authenticate Telegram origin. See [history acquisition](https://phishdestroy.github.io/TgWitness/docs/reference/history/) for operation and limits.

## 0.7.0 preview · 31 October 2026

- OpenTimestamps summaries now parse bounded operation trees and attestation payloads, rejecting truncated, malformed and excessive proofs. Marker bytes in arguments or opaque payloads cannot produce a Bitcoin status. Parsed Bitcoin attestations are explicitly `bitcoin-unverified`; run `ots verify` for validation.
- Source releases include the exact public TSA fixtures used by the evidence tests. The synthetic calendar fixture now carries correct serialized URI lengths.
- Added the [delivery roadmap](https://github.com/phishdestroy/TgWitness/blob/main/docs/ROADMAP.md), separating release acceptance, the external controller prototype and future independent-observer integrations.
- Evidence verification now reports the exact prefix covered by witness checkpoints and any unwitnessed tail. `--require-witness` requires a pinned witness and a matching final exported record; requested channel checks also reject missing claimed posts.
- Cloud journal checks reject missing startup records or expected collector keys and report unavailable host measurements. Deployment reports distinguish configuration checks from independent runtime attestation; supplied channel dates are not authenticated by witness signatures.
- Added access and permissions guides with reviewer/analyst examples, session limits, IP restrictions and revocation. Updated routing guides for automatic MTProxy, IP modes and external requests; connected the README, Wiki, website and bundled guide.
- Expanded the panel and complete documentation site to 25 languages, including German, French, Italian, Japanese, Korean and Hebrew. Language switches preserve the current documentation page; the static demo includes the new panel dictionaries. Existing Amharic guides and notices remain available separately.
- Site publication now rejects missing translations in a full-site language.

### Initial preview contents · 30 October 2026

- First GitHub release, with the Windows portable package, the wheel and the source archive. README and the website link the portable package directly: extract, double-click `TgWitness.cmd`.
- The setup guide has an "Open to everyone" section: no country or sanctions blocks, and Taylor Wessing as the only incompatibility we name. It is our position, not a licence condition.
- The website's changelog links point to `docs/CHANGELOG.md`.
- The README and Wiki now present the authors' Ethical Notice & Historical Continuity statement, with document references, historical context and an explicit explanation that MIT permission applies to everyone.
- Repository identity: a larger wordmark and investigation scene, three direct navigation choices, a dedicated handbook cover and a shorter README. Source connections, travelling records and the signature animate inline; phone layouts and reduced-motion alternatives retain the same visual hierarchy.
- Investigation presentation: the illustrated source-to-dossier animation now leads the README and Wiki. A clearer case route, direct evidence-model navigation and a vertical phone diagram keep the workflow and verification formulas readable; all moving illustrations have reduced-motion alternatives.
- High-assurance deployment (`python -m tgwitness.cloud`, [guide](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/)). It creates the collector through the API of Hetzner Cloud, DigitalOcean, Linode, Vultr or Amazon EC2: no SSH key, a provider firewall without inbound rules, SSH masked from the first boot, one fixed commit, and a panel reachable only through a Cloudflare Tunnel. The `verify` command lets a third party compare the provider's own log and firewall, the tunnel connector's address and the collector's signed `/api/assurance` statement. It writes a Markdown/JSON report for evidence handover. `generic` installs on any server with `install.sh` and is never reported as more than self-attested. With `TGWITNESS_ASSURANCE` set, the collector signs host measurements (SSH, logins, boot, metadata) into every process start and into `host.state` records whenever they change. Ordinary installations are unchanged.
- Two clicks to start: a local start (TgWitness.cmd, Start.cmd, start.sh, the demo launchers and the Docker helpers) opens the panel in the browser once it answers, and a real workspace shows its panel token in the console instead of in the address bar. Services, containers, scheduled and windowless starts never open a browser; `--no-browser` or `TGWITNESS_NO_BROWSER` turns it off.
- The operator notice and the Taylor Wessing page speak in our own voice.
- Returned to the MIT License. A tool whose output third parties must be able to check should not stumble over its licence. `LICENSE` is the standard MIT text again, the package declares MIT with the OSI classifier, and the container, portable package, website, Wiki and translated README labels say so. Our statement stays in NOTICE and on the Taylor Wessing page as our position; it adds no licence condition. The presentation artwork reads "open source" again.
- Added our Operator Incompatibility NOTICE to README, SECURITY, the documentation, Wiki and website. A single source keeps the complete statement consistent across those pages; source, Python and portable distributions include NOTICE alongside the licence.
- The documentation website gains a read-only online demo: the real panel, answered from recorded records of the fictional demo, in all 13 interface languages. Every change is refused in the browser, nothing is sent anywhere, and `tools/capture_demo.py` regenerates the recording. The home page and README link to it.
- Put the workspace preview near the top of the repository landing page, simplified wiki entry links and connected the issue chooser to the live handbook. GitHub and website sharing images now have reproducible PNGs in the investigation style. README and wiki now include video players for the illustrated investigation and message-history films. The gallery includes all three 12-second films; their MP4s and the two original GIFs are included in the source archive. Animated evidence explanations retain static alternatives for reduced-motion preferences.
- Fixed all eleven audit findings, each with a regression test. The portable builder no longer reuses an earlier build directory and refuses private or unexpected files. The verifier applies its archive limits at every entry point, including format detection and witness journals. The HTTP client bounds chunked reads. Individual and multi-account exports share one reservation per account; a workspace in a running multi-account export cannot be deleted; setup failures end an export as failed. People profiles count distinct replies and messages. Reference pages link to the GitHub editor, translated README sections collapse again, and the operations guide describes password-protected exports and priority rechecks correctly.
- The additional launchers moved to `scripts/`: `scripts\Demo.cmd`, `scripts\Setup.cmd`, `scripts\Docker.cmd` and `sh scripts/docker-start.sh`. They still run from the project root; `Start.cmd`, `start.sh` and `start.py` stay where they were.
- Redesigned the repository presentation with a message-history cover, GitHub and website preview images, and an illustrated observation-to-verification workflow. The English README now leads with the workspace, feature cards and a demo; detailed instructions remain in expandable sections. Wiki and documentation entry pages share the presentation, with an editable, reproducible artwork kit.
- Added an English project wiki with 13 user guides, a sidebar and footer, plus support guidance and a documentation issue template. A checked builder prepares GitHub Wiki links and a ZIP with hashes; CI publishes the bundle as a downloadable artifact. The wiki's separate publication procedure is documented.
- The documentation website gained a reference section: 17 repository documents rendered with search, contents and links that stay on the site, and their Mermaid diagrams drawn as SVG that animate into view (with a text version, and still when reduced motion is asked for). A new **Keep it secure** guide shows what leaves the machine, what each secret unlocks, what the protections cover and a hardening checklist. Pages gained a reading-progress bar, the current section in the contents, `/` and Ctrl/Cmd+K for search and content that eases in. SECURITY.md is split into sections with a summary table. Internal reviews and release notes moved to `docs/internal/`.
- The website is available in 13 languages (English, Russian, Ukrainian, Spanish, Brazilian Portuguese, Turkish, Arabic, Persian, Urdu, Hindi, Indonesian, Vietnamese, Simplified Chinese): home page, guides, interactive examples, diagrams and the reference, with a language menu, `hreflang` links, a multilingual sitemap and right-to-left layout for Arabic, Persian and Urdu. A changed English passage shows in English with a notice until it is translated again; the changelog stays in English. Added a light/dark theme button that follows the system until chosen, and rendered the reference's formulas.
- The Account page shows the current connection route with a **Proxy settings** link that opens the public MTProxy lists, your own proxy link and SOCKS5/HTTP fields at once; quick navigation finds it by "proxy". While observation runs, the route form says why it cannot be saved instead of only disabling the button.
- The README and its 12 translations gained a **What has been tested** table (real account, synthetic clients, local test servers, not tested yet) and mark untested integrations in place: notification services, MTProxy and public proxies, the witness bot, timestamp services, Docker/Caddy and the release workflow. The live test record now covers the whole-account run (9,968 verified records). Translations were regenerated from the current English README; the Russian one was corrected by hand.
- **Sign out of Telegram** on the Account page (`POST /api/auth/logout`): with observation paused, Telegram is asked to end the session (`auth.logOut`) and the session is removed from the vault; the journal, sources and keys stay and an `account.signed_out` record notes whether Telegram confirmed. Previously a connected account could not be removed from the panel at all. ACCOUNTS.md no longer claims that workspaces cannot be renamed or deleted.
- The panel's Russian was reviewed by hand: about 940 strings corrected (wrong machine translations such as "Anchor now" as "go to this page", inverted error messages, mixed terms) and the mini-client, dedicated-account guide and other English leftovers translated. In folder and whole-account modes the Sources page is titled "Observed chats" instead of "Choose chats", and the main workspace's default name follows the panel language.
- Publication checks now scan staged text, reject unresolved merges and require the full reviewed source in the Git index. A clean working file no longer hides a staged secret, and missing new modules or stale staged versions can no longer pass the release check.
- Account deletion reports filesystem failures, keeps incomplete deletions visible for retry, and preserves that state across restarts without reopening a half-erased vault. Successful deletion is recorded only after local files are removed.
- Valid panel and witness tokens remain usable after invalid requests from the same client address reach the rate limit. Witness failures share the bounded address cache.
- Fixed message loss after a long stop: the recheck recovered at most 1,000 missed messages and then continued above the newest saved one, so the rest of the gap below live messages was never fetched. It now continues from where the previous pass stopped, and a chat still catching up is rechecked on the next minute instead of after its 15-minute or 6-hour interval.
- The panel's notification list groups changes per chat and hour and keeps problems in it: on a live chat deleting a message every two minutes, all 60 entries were single deletions covering about one hour, so a sign-out or a full disk dropped out of the list within an hour.
- Rewrote the live-test record in plain terms: one real account, one supergroup, 27 to 29 October 2026, 1,291 messages, 472 deletions (347 saved before deletion), 12 edits, all 2,385 record signatures verified. The translated READMEs no longer claim that only a fake Telegram transport was tested.
- Review fixes. A link preview that Telegram fills in later, story views, paid media unlocked by this account and paid invoices are no longer recorded as edits. A link preview saves the file whose type and size were checked (its photo) instead of failing on its video. Reply keyboard presses are recognised only on newly sent messages after the keyboard, not on snapshots, recovered messages or edits. People profiles of private chats and bots include the other person.
- Scope fixes: a chat Telegram could not describe is no longer declined until the next scope refresh; a chat that left the folder stays paused when it falls outside the dialogs read; adding a removed chat again lifts its exclusion; folder mode starts with the folders read last time when Telegram does not answer; removing a chat with 5,000 exclusions is refused instead of breaking the scope settings; files still waiting for a removed source are recorded as failed.
- verify.py: a profile checked with `--evidence` also verifies that archive's signature, hash chain and files; with `--witness`, only answers signed by the export's own key count as witnessed, and a key the witness never saw stays "unpinned". Raising the heartbeat interval while observing no longer shows a coverage gap.
- Off-site copy: a missing or damaged preserved file is reported and retried next pass without stopping the other files, checkpoints and exports. Notifications also work with Apprise 1.x. The panel summary names the largest per-type attachment limit.
- Made independent bot setup visible in the panel with pinned configuration downloads, separate token files, publishing cadence and custom Bot API / HTTP proxy settings. Added operator-managed public MTProxy catalogs and preview/import of Telegram proxy links alongside manual routes. Added offline witness configuration checks and documented where continuity requires a full archive comparison rather than a growing counter.
- Corrected stale validation summaries using a read-only review of 2,385 retained live Telegram events with verified signatures and hash-chain continuity. Documented the existing saved update-state/catch-up implementation and its remaining replay limits.
- Refreshed the product page with a dark hero, an interactive message history, four screenshot views and a demo-first introduction. Redesigned the desktop access screen, refined Russian labels and reorganized the English/Russian READMEs around features and getting started. Added matching English/Russian covers and social artwork.
- Require Pillow 13.0.0 or newer (below 14) and pin 13.0.0: the dependency audit reported 39 advisories against 12.3.0, with fixes in 13.0.0. The minimum Python version remains 3.11. See the [upstream security fixes](https://pillow.readthedocs.io/en/stable/releasenotes/13.0.0.html#security).
- Pre-publication checks: source ZIPs allow only known locale JSON resources; wheels use explicit asset types and locale files, excluding arbitrary static files and namespace data directories. Git/Docker ignore common account JSON files. A publication check validates local documentation links, recognized secret patterns and the Git file list; CI now runs it and audits pinned runtime dependencies with pip-audit.
- Added a searchable **Go to…** menu (Ctrl/Cmd+K), keyboard navigation, focus restoration, current-page announcements, Russian labels and responsive light/dark styling. Closing the workspace also closes the menu. Added browser checks at 320, 390 and 1440 pixels.
- Fixed two broken documentation links and refreshed release documentation. Synthetic attachment fixtures use a fixed document date so comparison tests do not depend on timing.
- Whole-tool review: reject attachment downloads with the wrong byte count; scope replica progress to its destination/key; report missing or corrupt preserved files; verify restored media; reconcile identical overlapping journal segments and defer checkpoints beyond the copied journal boundary. Old unscoped replica progress triggers one complete local-data replay.
- Workspace switches and panel locking discard late API responses, including records, dossier caches, witness tokens and export dialogs. Actions wait for the selected workspace to load. Cancelling the file picker leaves a finished chat export available to download.
- Dossier builds cannot recreate a cache after it has been disabled or removed. Export cancellation waits for its file worker before removing temporary files. Added backend and workspace-browser regression coverage; existing English controls and translations are preserved.
- Corrected chat-switch routing, preserved successful action receipts through refresh failures, and disabled automatic RPC retries for callback and join actions. Added browser regressions for delayed chat responses and interrupted refreshes; included the mini-client check in CI.
- Rechecks and live edits compare attachment identity, entities and keyboard removal; temporary file-access metadata does not create versions. Background recovery respects own-action scope.
- Restore validates object paths in private staging, verifies every checkpoint and journal range, and publishes only a fully verified archive into an empty directory. Object Lock verification checks the actual requested deadline. Added regression coverage for each reviewed failure.
- Declared English fallbacks for untranslated interface sections while retaining existing translations and strict dictionary coverage checks.
- Panel mini-client in Chats: plain-text messages and replies, callback/text button presses with saved bot answers, and Telegram invite/username/bot-start previews followed by explicit join/open actions. Signed request/result receipts, persistent request deduplication, stale keyboard checks, FloodWait handling, and separate pending/unknown outcomes. The new controls use English text.
- Observation scope: chosen chats, one Telegram folder or the whole account, with channels, groups, private chats and bots as switchable types. New chats are added the moment they appear; excluded chats are never recorded. Switching to a folder or the whole account asks for confirmation, which the signed journal records.
- Own actions: outgoing messages and edits are labeled, reply-keyboard button presses are recognised, and they can be left out.
- Deletions in private chats and ordinary groups are recorded in their chat when a message with that ID was saved before, instead of staying unscoped.
- Rechecks in two tiers: priority sources every 15 minutes, others every 6 hours, at most 30 per pass, so accounts stay clear of FloodWait.
- Attachment limits per type (photos, videos, GIFs, round videos, voice, audio, stickers, files), up to 2,000 MiB.
- Sources can be removed (their people profiles are deleted; saved records stay in the journal) and starred as priority.
- People profiles per chat, opt-in: name and username history, Telegram flags, avatar SHA-256 and pHash with similar avatars, activity, replies, other observed chats and mentioned wallets, phones, usernames and links. Built only from saved records, each fact citing its record; exported as a separate signed file, optionally as an AES-256 ZIP; verify.py checks it against an evidence export.
- Independent witness: a separate process or container with its own key, journal and bot fetches the signed journal head with a read-only token, posts it to a channel and records when the collector does not answer. Witness page in the panel, Docker profile, deploy/compose/compose.witness.yaml for another server; verify.py checks evidence exports against the witness journal and channel posts.
- Reports and verify.py state continuous observation periods, gaps with their reason and message IDs that were never observed (not presented as deleted); signed ZIPs include coverage.json.
- Evidence manifests, chat exports, witness journals and profile files name their producer (TgWitness, PhishDestroy) in the signed part; the report and verify.py show it.
- Notifications: optional excerpts of deleted and edited messages (off by default), newly added chats, and a notification list in the panel.
- Off-site copy: the bucket's Object Lock and each pass's retention are read back, so storage that ignores Object Lock is reported.
- Parameters page: every limit and pace that was fixed in code is set per workspace in the panel, with its range and default, and each change is recorded in the signed journal. Covers the chat list size and refresh, heartbeat and checkpoint intervals, the startup buffer, how rechecks spread requests, disk reserve, download timeouts and retries, people-profile options including your own regular expressions, notification size and pace, snapshot, ZIP and browser-download limits, panel action timeout and Telegram client timeouts and retries.
- Recheck, attachment size, evidence and off-site copy intervals and the history snapshot size take any number in their range instead of a few presets; the default attachment limit goes up to 2,000 MiB.
- Coverage follows the heartbeat interval recorded in each heartbeat; verify.py takes `--max-gib` for archives above 4 GiB.
- Witness: `--timeout`, `--post all|changes|problems`, `--title`, a JSON config file (`--config`) and replaceable post wording; unknown options are refused.
- Investigation mode: one button sets the scope for an account that joins teams and talks to bots. Buttons under messages (links, web apps, texts to copy, callback data) are kept and shown in Chats, button-only edits become new versions live and at recheck, and every new chat or bot gets its profile (description, bot commands, members, invite link) and up to 1,000 earlier visible messages saved at once. Chats → Profile saves a source's profile on request.
- Dedicated account guide, linked from the sidebar, Account, Investigation mode and the setup guide: why the main account must not be used, why TgWitness works through public app hash/app ID pairs and why nobody can see anything of yours through them (with links to Telegram's documentation and to programs that use the same pairs), ways to create an extra account, and services for getting a number. The setup guide shares its new look.
- New dependency: Pillow, for avatar perceptual hashes.
- Light and dark theme, following the system by default; Telegram-style chat view and interface motion, which an "Animations always on" switch keeps when the system asks for less.

## 0.6.1 · 27 October 2026

- Renamed TgWatch to TgWitness; archives and checkpoints made under the old name still verify.
- Evidence mode: checkpoints are timestamped automatically by RFC 3161 authorities and OpenTimestamps, and verify.py checks the answers.
- The UI and docs say "workspace" throughout.
- Exports can be saved as a password-protected AES-256 ZIP that 7-Zip and WinRAR open.
- Notifications through Apprise: problems, changes in observed chats and a daily summary.
- Added 13 interface languages and translated the README, Quick start and Deployment guide into 12 languages.
- Off-site copy: everything goes encrypted to any S3-compatible storage, with Object Lock where available and a verified restore command.
- After a restart, observation catches up on Telegram updates missed while it was off.
- Observed chats are rechecked every 15 minutes for missed messages, edits and messages Telegram no longer returns.
- Photos and files are saved by default; downloads pause below 1 GiB of free disk.
- Sign in without your own API ID/hash using a built-in pool of public API pairs.
- The chat list loads on its own in Sources, and every journal record type has a readable title.
- New Chats view as the start screen, with deleted and edited messages highlighted.
- Export one chat with several accounts at once; each account signs the ranges it fetched.
- Observation keeps running during chat exports.
- No fixed limit on workspaces.
- Full chat export shows the expected time and progress.
- Chat exports list every author; People shows each person's saved, deleted and edited counts.
- New Accounts view to manage, rename and delete workspaces.
- Full chat export as a signed ZIP.
- Portable package checks run on a temporary port.
- Public project website.
- GitHub Pages build and deployment workflow.
- Windows portable package with an embedded Python runtime.
- Start.cmd finds or offers to install Python 3.12.
- start.sh finds more Python versions and prints the install command.
- start.py explains a missing venv package or failed dependency download.
- Ctrl+C in the launcher stops the server in order.
- Docker helpers print the panel address and token once the container is healthy.
- Rewritten accounts guide.
- Redesigned panel on one stylesheet.
- Bundled SVG icon set and a new logo.
- Easier-to-scan journal.
- Version in the sidebar; `--host`, `--port` and `--data-dir` in `--help`.
- Offline setup guide restyled to match the panel.
- Rewritten README with current screenshots.
- tools/capture_screenshots.py regenerates README images; browser checks can use installed Chrome or Edge.
- Cleaner download test output.
- Local Playwright browsers excluded from git and Docker builds.

## 0.6.0 · 27 October 2026

- Start live setup on a focused account form with Phone, QR code, Files, and Auth key tabs. Make API ID + Hash directly accessible and explain each supported file beside the picker, including companion JSON and the difference from an Auth Key.
- Accept Auth Key HEX and DC ID directly, with optional online User ID verification. Reject incomplete keys locally and discard conversions after inputs change.
- Put file selection before format guidance and show progress while reading files, requesting login codes, generating QR codes, or connecting to Telegram.
- Open demo mode on its sample journal. Show live startup instructions on its Account page instead of a login form that cannot authorize accounts.
- Start connected, unconfigured workspaces on source selection. Move journal counts, capture settings, and detailed verification into expandable sections.
- Put phone entry first and request the code directly, with API settings revealed only when missing. Reuse the current workspace's saved API pair for phone, QR, and session login without exposing saved secrets to the browser.
- Connect selected account files with one action; metadata-only JSON leads to phone entry. Collapse connection/storage settings and simplify the panel-token gate.
- Refresh the panel with a light workspace, dark navigation, larger journal text, and a next-step guide for account connection, source selection, and observation.
- Separate phone, QR, and file sign-in. Paste one `API ID:API Hash` pair to fill both fields; reject malformed pairs locally and discard stale imports when changing sign-in methods. No shared API credentials are bundled.
- Import Telethon and Pyrogram SQLite sessions, modern single-account TData ZIPs, Telethon StringSession text, and documented account JSON fields in Connection.
- Read up to four matching files together; companion JSON can supply API metadata. Conversion stays in server memory, with bounded input and no ZIP extraction.
- Support Desktop local passcodes and complete Auth Key HEX + DC ID JSON. Check imported user IDs against Telegram before retaining account authorization.
- Add locally rendered QR login, Telegram 2FA, expiry/retry, and cancellation on lock, workspace switch, route change, and replacement login.
- Add synthetic parser, isolation, QR lifecycle, and browser acceptance coverage; update English format, deployment, security, and offline documentation.

## 0.5.1 · 27 October 2026

- Disconnect rejected authorization clients and accept live updates only from the active account client. Resuming observation cancels unfinished login.
- Support windowless Windows launches with rotating startup/server diagnostics in the data directory's `logs/server.log`; HTTP access logging remains disabled.
- Clear journal verification results on workspace changes, discard late responses, and identify the verified journal boundary when new records arrive.
- Search Unicode text without case differences, preserving original signed records.
- Keep unsaved attachment settings during status refresh and edits made during saving.
- Show full UTC event dates/times at phone and tablet widths.
- Keep the search icon clear of the input text at every layout width.
- Include monitoring-policy changes in the Coverage filter.
- Add regression coverage, contribution/issue guidance and stricter public-source packaging exclusions.
- Expand English account-format and collection guides, add workflow diagrams and export tables, and align the README, quick start, and offline setup guide.
- Add Linux/macOS launch scripts, Python discovery on Windows, and Docker startup helpers that wait for web-server health. Document one-command installation.
- Add optional automatic HTTPS with Caddy, image-only Compose deployment, and versioned AMD64/ARM64 GHCR builds triggered by a GitHub Release after CI passes.
- Check first-run installation across CI platforms and Compose persistence after container recreation; document updates, reboot behavior, and data migration.
- Explain signature coverage for each export format and the investigation handoff workflow, including independently retained fingerprints and checkpoints.

See [verification](https://phishdestroy.github.io/TgWitness/docs/reference/verification/) for executed checks and [readiness](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) for remaining live-service and deployment work.

## 0.5.0 · 26 October 2026

- Add per-account monitoring categories, presets and signed policy changes.
- Allow direct local entry to isolated synthetic demos without copying a token.

Earlier preview capabilities and qualification history are described in [release status](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RELEASE.md) and [verification](https://phishdestroy.github.io/TgWitness/docs/reference/verification/).


---

# One journal. Four collection modes. Eight verification levels.

Canonical page: https://phishdestroy.github.io/TgWitness/guides/modes.html

Modes, scenarios and evidence levels

TgWitness records what the connected account observes. A third party can verify the record’s integrity against an independently trusted key.

[Collection modes](https://phishdestroy.github.io/TgWitness/guides/modes.html#scope)[Scenarios](https://phishdestroy.github.io/TgWitness/guides/modes.html#scenarios)[Evidence levels](https://phishdestroy.github.io/TgWitness/guides/modes.html#levels)

3–5 minute overview · fictional examples · current implementation

1. **Telegram**

   Account-visible updates
2. **Collector**

   Linked records, each signed
3. **Verifier**

   Trusted key + retained boundary

`h₁ → h₂ → h₃ · Ed25519`Integrity is checked. Telegram origin and the truth of a message remain separate questions.

## Choose the observation scope

Three scopes and an investigation preset. Exclusions and enabled source types still apply.

Default**Chosen chats**

Records

Only sources selected by hand.

New chats

Not added automatically.

Choose for

A known set of channels or groups. No fixed chat capacity has been qualified.

**Does not do** It does not discover other chats or backfill earlier history.

Account folder**Telegram folder**

Records

Folder inclusions and categories, minus exclusions and archived chats when configured.

New chats

Matching active chats; folder changes within an hour.

Choose for

An analyst already maintains a case folder. Confirm collection on a dedicated account.

**Does not do** It does not apply the folder’s changing muted/read conditions.

Confirm scope**Whole account**

Records

Account-visible chats, including private conversations and bots, within selected types.

New chats

Added when the first update arrives.

Choose for

A dedicated observation account, including an account participating in a case.

**Does not do** It does not join chats automatically or bypass source access.

Whole-account preset**Investigation mode**

Records

All source types, own actions, source profiles and the latest 200 visible messages of newly discovered sources.

New chats

A new chat or bot gets a profile and a history snapshot.

Choose for

Join a team or interact with a bot through the panel. Review and save the preset.

**Does not do** It does not snapshot every existing chat or observe callbacks pressed in another client.

These cards are a local comparison, not live collector controls. They do not change an account.

**Does not do** No mode reads secret chats, records while the process is stopped, joins sources on its own or retrieves earlier history beyond a requested snapshot/export.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/collection/)

## GitHub Actions capture (preview)

A fresh Telegram login, one chat, an encrypted archive and GitHub provenance.

[Open capture helper](https://phishdestroy.github.io/TgWitness/docs/capture/)

## What is recorded

Only delivered or explicitly requested observations enter the record. Unknown attribution stays unknown.

 Capture switches · local illustrationNew messagesEditsDeletionsReactionsMembership

The panel applies these switches per workspace. Turning one off keeps existing records; turning it back on does not reconstruct missed events.

**Event matrix: saved material and remaining unknowns**

| Category | Saved | Remains unknown |
| --- | --- | --- |
| Message | Text, IDs, sender metadata, reply context and original update envelope. | No third-party-verifiable Telegram signature. |
| Edit | Every observed version, without overwriting earlier ones. | Intermediate edits may be missed; sender is not necessarily editor. |
| Deletion | Notice plus previously saved text, if available. | The deleter and exact action time are not supplied. |
| Unscoped deletion | Account-level notice; unknown peer remains explicit. | No guessed chat. Correlation uses previously saved account-scoped IDs when possible. |
| Reaction | Delivered counters and visible recent identities. | Not every reactor is visible; a full available list needs separate queries. |
| Membership | Delivered service messages and participant updates. | Role and chat type limit visibility; silence does not establish absence. |
| Attachment | Original-version descriptor, saved bytes, SHA-256 and attempt outcomes. | A vanished file may be unavailable; a newer version does not replace it. |
| History snapshot | Currently visible messages, marked as history observations. | Earlier edits and vanished content are not reconstructed. |
| Own actions | Outgoing messages/edits and matching reply-keyboard button_press metadata. | Callbacks pressed in another Telegram client are not visible. |
| Bot buttons | Callback, URL, web-app and request metadata retained with the message. | URLs and phone/location requests are text, not automatically opened or executed. |

### Default attachment limits

Photos

20 MiB

Video

100 MiB

Files

50 MiB

Animations

20 MiB

Video notes

50 MiB

Voice

20 MiB

Audio

50 MiB

Stickers

5 MiB

**Does not do** A switch does not redact embedded metadata or disable operational records. Capture does not identify an actor whom Telegram did not supply.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/collection/)

## Use the authorization you have

Each account has its own workspace, journal, signing key, route and queue.

### Phone + code

Enter 2FA when enabled.

### QR code

Scan from an authorized device; 2FA may still be required.

### Telethon .session

Import the account’s session file.

### Pyrogram .session

Import the supported Pyrogram session format.

### TData ZIP

One supported Desktop account; local passcode if set.

### StringSession text

Paste a Telethon StringSession.

### .session + .json

Select the session and matching companion metadata.

### Auth key HEX + DC ID

Import account authorization with its data-center identifier.

**API pair**

Your own API pair is optional. Without one, TgWitness uses a pool of public pairs, including pairs from official Telegram Desktop.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy is experimental; built-in public MTProxy lists are available. A failed proxy route does not fall back to a direct connection.

Two workspaces on one machine are not two independent witnesses.

**Does not do** Import does not bypass Telegram authorization, 2FA or unsupported session formats. Accounts still share the application process.

[Account formats](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/)

## Act from the panel

Send or reply, press a current bot button, save a link preview, then explicitly join a chat or start a bot with its start parameter.

`interaction.preview``interaction.requested``interaction.result`

Preview, request and result receipts are signed. Before a button press, the server fetches the message again and rejects a changed keyboard. Returned callback text and URLs remain recorded context.

**Does not do** No web apps, payments, phone/location sharing or inline queries. Displaying a URL does not open it.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/collection/)

## Recovery and continuity

Gaps are shown, not hidden.

### Resume the saved position

After restart, Telegram is asked for missed updates. Finite retention and expired differences can leave gaps.

### Recheck visible messages

Defaults: priority sources every 15 minutes, others every 6 hours. Outcomes include message.recovered and message.missing_on_recheck.

### Read coverage.json

Observation periods, gaps with reasons and unobserved IDs accompany the signed export. A missing-on-recheck record is not a deletion notice.

**Does not do** A later history snapshot does not erase an outage or recover every vanished version. The saved cursor is not a lossless acknowledgement of journal acceptance.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/)

## Seven levels. Different questions.

Each mechanism answers a bounded question. Configure external services separately and retain their trust anchors outside the collector.

1. ### Record

   SHA-256 chain + Ed25519 per event; the first previous_hash is 64 zeroes.

   **Third party checks** Ordering and signatures under the pinned collector key.

   **Does not do** It does not prove Telegram origin or completeness.

   **Verification command**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Container

   manifest.json lists file hashes; manifest.sig signs it. media.saved binds attachment bytes to an event.

   **Third party checks** The supplied files agree with the signed manifest and media receipts.

   **Does not do** It does not sign a separately downloaded CSV, HTML or screenshot.

   **Verification command**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Retained boundary

   Checkpoint at startup, every 5 minutes by default, and orderly stop. Keep a copy elsewhere.

   **Third party checks** The later export agrees with an earlier retained length and head; rollback can be detected.

   **Does not do** It does not detect replacement of both journal and all retained checkpoints.

   **Verification command**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### External time

   Evidence mode sends a checkpoint SHA-256 to RFC 3161 authorities (FreeTSA, DigiCert) and OpenTimestamps calendars.

   **Third party checks** A verified TSA response dates those bytes; a confirmed OpenTimestamps proof anchors them to Bitcoin.

   **Does not do** It does not treat a prepared request or pending calendar receipt as a confirmed timestamp.

   **Verification command**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Independent witness

   Separate host, scoped read-only endpoint, fresh challenge, its own key/journal and TGW1 channel posts.

   **Third party checks** Earlier accepted heads; statuses ok, key_changed, rollback, fork, invalid and no_response.

   **Does not do** It does not turn two workspaces on one collector host into independent witnesses.

   **Verification command**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Off-site replica

   S3-compatible copy encrypted with AES-256-GCM; Object Lock when the bucket supports it.

   **Third party checks** Restore publishes files only after journal, checkpoint and preserved-media verification succeeds.

   **Does not do** It does not restore without the exported key or assume retention without checking the storage response.

   **Verification command**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Run provenance

   Signed run receipt: source hashes, dependency versions and process context. Self-reported.

   **Third party checks** What the signing collector reported about its own execution.

   **Does not do** It does not provide independent process attestation or exclude compromise before recording.

   **Verification command**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### What no level proves

Delivery of every Telegram update; the truth of the text; that a sender ID identifies a real person; absence of collector compromise before recording; admissibility in court.

[Independent witness](https://phishdestroy.github.io/TgWitness/docs/reference/witness/)

Local SHA-256 experiment

### Try changing record 2

The next record keeps the previously saved link. Changing the text changes record 2’s calculated hash.

Text of record 2

Record 1`h1`Starts with 64 zeroes

Record 2`h2`Includes the saved h1

Record 3`h3`Includes the saved h2

Static example: h2 covers “Meet at 11:00”. Changing that text changes h2; record 3 still references the saved h2.

**Inspect the full digests**

Saved record 2 hash

`SHA-256(e₂)`

Recalculated record 2 hash

`SHA-256(e₂)`

This sample calculates hashes, not signatures. The real verifier checks every signature and link against the trusted key.

 [Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/how-it-works/)

## Choose a route through the evidence

Fictional situations. Start collection before the relevant event; preserve the boundaries and gaps alongside the content.

### A channel changes payment details

Mode → events

Chosen chats → messages, edits, deletions.

Output

Observed post versions and attachments by hash.

Verification

Signed ZIP + retained checkpoint + verified TSA response.

**Does not do** It does not recover an original that was never captured.

### Messages disappear after an incident

Mode → events

Folder or whole account → all event categories.

Output

Saved originals, deletion notices and coverage with gaps.

Verification

Signed ZIP + independent witness journal.

**Does not do** It does not identify the deleter from a notice that supplies no actor.

### Investigate a shop bot

Mode → events

Investigation preset → buttons, link previews and explicit bot start.

Output

Signed interaction receipts, returned callbacks and saved profiles.

Verification

Signed ZIP; verify any dossier against the ZIP.

**Does not do** It does not open a bot web app, make a payment or record another client’s callbacks.

### A participant changes names across chats

Mode → events

Any scope → observed sender/profile metadata.

Output

Name/username history by numeric ID, “also in” links and extracted leads.

Verification

Dossier JSON checked against the signed ZIP.

**Does not do** It does not turn a wallet, phone-like string or username into proven identity.

### Long-running observation with an off-site copy

Mode → events

Any scope → Evidence mode and an S3 replica with supported Object Lock.

Output

Encrypted copy, retained checkpoints and timestamp responses.

Verification

Restore with the exported key, then verify without the original server.

**Does not do** It does not replace an independent witness or a separately retained decryption key.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/investigation/)

## Hand over a checkable package

Supply the signed original, an independently retained key fingerprint, the relevant checkpoint and the verification result.

- Signed ZIP
- JSONL
- CSV
- HTML
- Checkpoint
- Run receipt
- Chat export: chat.json / chat.html
- Dossier JSON
- Password-protected AES-256 ZIP
- Separate exports for multiple accounts
- Streaming CLI: 5 GiB default limit

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Obtain the verifier from a trusted copy, not from the archive being checked.

**Does not do** Standalone CSV and HTML are not signed containers. A password protects transfer confidentiality, not authenticity. Multiple exports do not merge account journals.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/)

## Compare the delivered artifact

Basic artifacts without added signing, timestamp or witness systems. Scripts and loggers vary by implementation; “partial” means limited to captured or visible material.

| Approach | Edits / deletions | Record signature | External time | Independent witness | Coverage / gaps | Verification without author |
| --- | --- | --- | --- | --- | --- | --- |
| Telegram Desktop export | Partial | No | No | No | No | No |
| Telethon snapshot script | Partial | No | No | No | No | No |
| Deletion logger: text log | Partial | No | No | No | No | No |
| Screenshots / web capture | Partial | No | No | No | No | No |
| TgWitness with configured extras | Partial | Yes | Yes | Yes | Partial | Yes |

**Does not do** The table does not assess every script or logging product. Optional time and witness checks require their own services and trust anchors; none establishes source truth.

[Read the details](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/)

## Keep the limits with the evidence

Verification is useful when its scope stays explicit.

- Secret chats are unavailable.
- Nothing is recorded while the process is stopped; recovery is bounded.
- A verified record is not proof that its content is true.
- An operator with the key can sign arbitrary content. Independent witnesses and timestamps constrain later replacement, not dishonest initial capture.
- Use a dedicated account, not your primary account.
- Telegram can restrict accounts for request volume.

**Does not do** No mode or evidence level establishes legal admissibility, complete Telegram delivery or real-world identity.

[Setup guide](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=en)[Dedicated account](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/docs/reference/investigation/)
