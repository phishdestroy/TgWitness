# TgWitness

> Open-source Telegram investigation software. Export chat history, preserve observed edits and deletion notices, follow people across chats, and hand over a signed archive that a recipient can verify.

TgWitness runs on your own computer or server. PhishDestroy maintains the project under the MIT License. The website is documentation; the browser demo contains synthetic records and does not connect to Telegram.

Signed exports let recipients verify file integrity and the signing key offline. A hash-linked journal preserves the sequence of saved observations; independently retained checkpoints provide an earlier comparison point. Reports combine readable history, source references and verification results in the same package.

The panel brings together isolated account workspaces, supported session imports, parallel chat export, cross-chat people profiles, observed name changes, bot-button interaction receipts, saved attachments and offline HTML/JSON evidence. Case Board keeps team annotations linked to saved records. The report studio offers eight designs, content choices and a data preview; minimized sharing copies control what recipients receive. Optional witnesses, timestamps and encrypted off-site copies add records outside the local journal. Archive search, AI analysis, OCR, transcription, MCP and signed webhooks work with the records you have collected.

These guides track the `main` source branch. The project version is `0.9.1`; check the changelog and release notes before assuming a source feature is included in a downloaded package.

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

- [GitHub Actions capture](https://phishdestroy.github.io/TgWitness/docs/capture/index.md): Choose Takeout，regular API export or a chat journal on a temporary GitHub runner．

- [Choose a proxy](https://phishdestroy.github.io/TgWitness/docs/proxies/index.md): Maintain automatic MTProxy routes or use your own proxy. Choose IP modes, fallback rules and the route for external requests.

- [Share a case](https://phishdestroy.github.io/TgWitness/docs/access/index.md): Give reviewers and analysts access to selected accounts and chats, with separate permissions, session limits and revocable tokens.

- [See how evidence works](https://phishdestroy.github.io/TgWitness/docs/concepts/index.md): Follow a message from capture to checkpoint. Change a sample record, recalculate its SHA-256 chain and see what a retained checkpoint detects.

- [Set up a witness bot](https://phishdestroy.github.io/TgWitness/docs/witness/index.md): Publish signed journal checkpoints to your Telegram channel with a separate witness, its own key and read-only collector access.

- [Timestamps](https://phishdestroy.github.io/TgWitness/docs/reference/timestamp/index.md): RFC 3161 timestamps for signed checkpoints: what is sent to the authority and how a response is verified.

- [Security and data handling](https://phishdestroy.github.io/TgWitness/docs/reference/security/index.md): Threat model, access model, secrets at rest, network exposure, session imports and how to report a vulnerability.

## Verification and scope

The journal records what the authorized account observed, subject to its access and Telegram rate limits. Saved content remains after a later deletion; content deleted before capture is unavailable. Deletion notices and unsuccessful rechecks remain distinct observations. Integrity verification establishes the relationship between supplied files, the signing key and retained checkpoints. The archive includes source identifiers, captured versions and coverage information for review. GitHub Actions capture adds an attestation binding the archive to an approved hosted workflow and collector version.

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

## Controlled experiment

- [Export Clinic](https://phishdestroy.github.io/TgWitness/docs/export-clinic/index.md): Watch a controlled Telegram Desktop export experiment, compare seven test conversations, and inspect the original recording and paired files.

## Checks and measurements

- [Checks & measurements](https://phishdestroy.github.io/TgWitness/docs/validation/index.md): 56,329 Telegram messages exported in two measured runs. Compare message counts, collection speed, export time and signed archives.

---

# Start in minutes

Canonical page: https://phishdestroy.github.io/TgWitness/docs/start/

Poke around the demo first, then connect your own account.

## Look around without an account

Get the project, have **Python 3.11 or later**, run the demo. The launcher sets up everything else.

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

A workspace with made-up messages opens in the browser. Open a chat, compare an edit, look at an export. No Telegram involved.

![TgWitness conversation view with sample messages](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

A sample workspace. Your own journal starts separately.

## Start your own workspace

Close the demo, then:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Open the address the launcher shows and paste the **panel access token** from the file it names. That's for TgWitness, not Telegram.

## Capture your first message

1. [Connect a dedicated Telegram account.](https://phishdestroy.github.io/TgWitness/docs/accounts/)
2. Pick a group or channel and start observation.
3. Send a message in your test group and watch it appear in the journal.

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

One workspace = one account, its journal and its key.

## Choose how to sign in

**Accounts** → add a workspace → connection settings. Use a separate account for this.

- **QR code:** scan it from Telegram's Devices screen and confirm.
- **Phone number:** number, code, then 2FA password if you have one.
- **Session import:** your own session file or Telegram Desktop data.

Use a built-in API profile or your own API ID and hash. It only identifies the app, it doesn't log you in or hide anything.

**Need a proxy first?**

You can [choose and test the connection route](https://phishdestroy.github.io/TgWitness/docs/proxies/) before signing in. Each account has its own route.

## Choose what to observe

1. Pick the chats, groups or channels you need.
2. Check collection settings, media included.
3. Start it and check the connection and recent activity.

The account has to have access. Admins and members see different things, the journal shows what this account got.

Whole account? **Sources → Observation scope → Investigation mode**, check it, **Save scope**. Full walkthrough: [investigating a whole account](https://phishdestroy.github.io/TgWitness/docs/cases/).

## Check the whole path

In your test group, send a message from another account, edit it, delete it. All three should show up in the journal. Then [export and verify](https://phishdestroy.github.io/TgWitness/docs/exports/).

"Connected" means the connection works. A captured test message means events actually arrive.

## Add another account

New workspace in **Accounts**, same steps. Note each account's key fingerprint so you can tell exports apart later.


---

# Choose a proxy

Canonical page: https://phishdestroy.github.io/TgWitness/docs/proxies/

Keep the account online, and decide yourself whether it may ever show your server's IP.

## Choose the IP mode first

01**Hide the address**

Proxy only. If none works, it waits.

02**Direct as a last resort**

Goes direct after a delay, back to a proxy once one works.

03**Server behind a tunnel or VPN**

Direct is fine. It doesn't set up or check the VPN for you.

The route chooses the connection. The IP mode determines whether a direct connection is permitted.

## Let the pool maintain the route

1. **Account → Settings → Connection settings**.
2. Pick the IP mode and **Automatic MTProxy**, or a fixed route.
3. Save, **Test Telegram connection** (works before sign-in too).
4. Start collecting and send yourself a test message.

New workspaces start on automatic MTProxy with **Hide the address**. The pool pulls four public lists, checks servers, keeps the good ones and swaps out dead ones.

## Use your own proxy

SOCKS5, HTTP CONNECT, a Telegram proxy link or an operator catalog. Pause observation before switching. Fake TLS secrets (`ee`…) don't work.

**Rotation, sharing and retry settings**

**Parameters → Automatic MTProxy**: failure thresholds, cooldowns, rotation, accounts per proxy. Limit 1 means an account waits rather than share. Different proxies can still share an exit IP.

## Separate Telegram from external requests

MTProxy only carries Telegram. Timestamps, notifications, copies and code checks go through a separate SOCKS5/HTTP proxy, the account's SOCKS5/HTTP route, or direct if the mode allows. Or turn them off.

`TGWITNESS_PROXY_FEED_PROXY` sets the route for list downloads. The [witness](https://phishdestroy.github.io/TgWitness/docs/witness/) has its own settings. None of this touches your browser or system network.

More: [modes and defaults](https://phishdestroy.github.io/TgWitness/docs/reference/connection/#ip-modes), [who may change routes](https://phishdestroy.github.io/TgWitness/docs/access/).


---

# Export and verify

Canonical page: https://phishdestroy.github.io/TgWitness/docs/exports/

Hand someone files they can check themselves against your workspace.

Retain a referenceExport signed ZIPRecipient verifies

New to signatures and checkpoints? [Change a sample record](https://phishdestroy.github.io/TgWitness/docs/concepts/#chain) and see which checks catch it.

Keeping a copy away from the collector? Go to [S3 setup](https://phishdestroy.github.io/TgWitness/docs/exports/#s3), [Object Lock](https://phishdestroy.github.io/TgWitness/docs/exports/#s3-retention) or [verified recovery](https://phishdestroy.github.io/TgWitness/docs/exports/#s3-restore).

## Retain a trusted reference

Write down the workspace key fingerprint somewhere other than the collector. While collecting, keep signed checkpoints elsewhere too, or run an [independent witness](https://phishdestroy.github.io/TgWitness/docs/witness/). That's what the recipient checks the key and an earlier journal state against.

## Download the signed ZIP

**Exports** → signed evidence ZIP. It has the whole journal and a signed file manifest. Shape the readable report in [Report studio](https://phishdestroy.github.io/TgWitness/docs/reports/), or send only selected data as a [handover extract](https://phishdestroy.github.io/TgWitness/docs/handover/).

HTML, PDF and JSON reports carry their own seals. CSV is just a working copy; for integrity use the CSV inside the verified ZIP.

## Verify with a trusted copy of TgWitness

In the project environment, with your own fingerprint and paths:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

A pass shows `key_pinned: true` and `checkpoint_checked: true`. Keep that output next to the archive. The checkpoint has to be at or before the end of the export.

## Use the verification result

- **Files:** the manifest binds their hashes, the signatures bind the journal. Any change shows up.
- **Identity:** the fingerprint you kept proves it's the key you expected.
- **Earlier state:** a checkpoint compares the export with a journal prefix saved before the handoff.
- **Coverage:** gaps, acquisition results and a send → edit → delete test show what this setup actually caught.

Details: [what verification proves and what it doesn't](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope).

## Set up the S3 off-site copy

**Exports → Off-site copy** in your workspace. Works with AWS S3 and anything S3-compatible. It copies journal segments, saved files, checkpoints with their timestamps and finished chat exports, each encrypted with `AES-256-GCM` before it leaves the collector.

The online demo shows these controls with uploads off. Only enter real credentials in your own install.

[![Complete Off-site copy panel: endpoint, region, bucket, access keys, schedule, Object Lock and recovery key controls](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

The complete panel with advanced options expanded. No storage credentials are shown.

| Field | What to enter |
| --- | --- |
| Endpoint | Storage URL, no bucket path or credentials. Example: `https://s3.example.invalid`. |
| Region | Whatever your provider needs. Default `us-east-1`. |
| Bucket | An existing bucket you can write to. Example: `example-case-backup`. |
| Folder in the bucket | Prefix, default `tgwitness`. A per-workspace prefix is added on top. |
| Access key ID / Secret access key | Both together, stored in the vault. Leave both empty later to keep them. |
| Path-style addresses | On: `endpoint/bucket`. Off: `bucket.endpoint`. Depends on the provider. |
| Copy interval | 1 to 1,440 minutes, default 5. Only while the app runs. |
| Object Lock retention | Days and mode, if the bucket supports Object Lock. Zero keeps the bucket default. |

1. Create the bucket, fill in destination and credentials with **Keep an off-site copy** unticked, hit **Save off-site copy**.
2. **Test connection** uploads an encrypted test object.
3. **Download encryption key** and keep it away from the collector. No key, no recovery.
4. Tick **Keep an off-site copy**, save, then **Copy now** or let the schedule run.

## Check retention and copy progress

Under **More options** pick retention days and `GOVERNANCE` or `COMPLIANCE`. TgWitness reads the retention back from an uploaded object and tells you: confirmed, missing or check failed.

The panel shows the last pass, object count, bytes, copied journal boundary and errors. A missing local file is reported and retried next pass, the rest keeps copying.

Uploads go over Direct, SOCKS5 or HTTP. With an MTProxy-only route the copy waits with an error.

## Keep the recovery key separately

The key JSON has the decryption key, destination, prefix and key fingerprint. For recovery you need it plus storage credentials with read access.

Changed endpoint, bucket or prefix? Download the key again. A fresh copy starts at the new destination; old chat exports stay where they were.

## Restore and verify on another machine

You need a TgWitness install you trust, the key JSON, read-only storage credentials and an empty folder:

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

Everything is checked in a private temp folder first: the whole journal, checkpoints, file hashes and sizes. Unsafe paths, conflicting segments or a journal shorter than its checkpoint fail, and then nothing is written out.

On success you get `events.jsonl`, `media/`, `checkpoints/` and `exports/`. Keep the command's JSON output with them, and compare against checkpoints or witness records you kept yourself.


---

# GitHub Actions capture

Canonical page: https://phishdestroy.github.io/TgWitness/docs/capture/

Choose Takeout，regular API export or a chat journal on a temporary GitHub runner．

Enable JavaScript to generate a key and decrypt your archive.

**Full reference**

**Preview available from `main`.** A fork launches a pinned reusable workflow from `phishdestroy/TgWitness`. The workflow exports an account, selected chats or one chat's event journal using a newly created Telegram session, attests the evidence ZIP or multipart manifest, and uploads only recipient-encrypted handoffs. The normal administration panel is not exposed.

Choose `client=official_web` to run the [official-client witness](https://github.com/phishdestroy/TgWitness/blob/main/docs/OFFICIAL-WITNESS.md) with guarded Telegram Web controls and video. It requires your own upstream proxy and observes one rendered chat. The default `client=api` retains the full-account export modes described below.

The verifier checks the archive against its GitHub attestation, the approved workflow and collector commits, and the signed journal and attachment hashes. The collection process uses pinned upstream code and fresh storage. A reviewer can inspect that code and verify the delivered archive against its recorded run.

## User flow

The helper explains the five stages and lets you try message or collector substitution on sample data. **Start my capture** opens the wizard.

1. Choose **GitHub Actions capture (preview)** on the project homepage, the workspace login screen, or **Exports → Open capture helper**. You can also open the [official helper](https://phishdestroy.github.io/TgWitness/sealed.html?lang=en) or `tgwitness/static/capture.html` from a trusted checkout in a modern browser. The helper makes no network requests for key or file processing. The helper supports the site's interface languages; the temporary collection panel supports English and Russian.
2. Generate a key and save **sealed-key.json**. This is the only private decryption key. Copy the separate public **recipient** value. Losing the private key loses access to both the connection and the archive. Confirm that you saved it to unlock the next step. If you already have a delivery file, load the saved key and choose **I already have an archive**.
3. Fork TgWitness, enable Actions in the fork, and run **Sealed chat capture**. Paste the public recipient and choose 30, 60, or 120 minutes. Never put a phone number, login code, Telegram password, private key, or session in workflow inputs, commits, issues, or logs.
4. During the run, download **sealed-connection** from Artifacts and unzip it. Load `connection.tgwsealed` in the helper, using the saved private key. The resulting link contains a random access secret in its URL fragment. Keep this link private. The panel removes the fragment and keeps the secret in this tab's session storage; it is not placed in HTTP access logs.
5. Open the connection link. Sign in with a QR code, or with your phone number and the login code. Enter your two-step verification password if Telegram asks for it. The built-in API credential pool is used by default, just like the normal workspace. You may expand the optional custom credentials section and enter both `api_id` and `api_hash` from [my.telegram.org/apps](https://my.telegram.org/apps). Leave both fields empty to use the built-in pool; a partial or malformed pair is rejected. Session imports are not allowed. Choose the export mode and scope. The connection link contains an access secret: keep it private.
6. Choose **Telegram Takeout**, **Regular Telegram API** or **Chat event journal**. For account export, choose all accessible chats or load and select one or more chats, then set dates, chat types, account categories and attachment rules. Check settings and size, optionally save the settings JSON for an independent reviewer, then press **Start capture**. Settings are fixed after starting. Resume works only while this runner exists; finishing early preserves acquired data and records gaps. Deadline expiry after starting produces an explicitly partial archive; expiry before starting or cancellation produces no archive.
7. Wait for **sealed-result**, download and unzip it, and decrypt `delivery.tgwsealed` in the helper. You receive `delivery.zip`, containing `evidence.zip`, `attestation.jsonl`, and instructions. Browser decryption is limited to 256 MiB; larger packages use the streaming local command below. Large results also include `delivery-NNNNNN.tgwsealed` parts; the main `delivery.tgwsealed` then contains `evidence.parts.json` and the attestation. Download every part and assemble locally as described below.
8. End the temporary session in Telegram Settings → Devices if revocation was not confirmed or the runner was killed. Normal completion attempts logout; network failures and forced runner termination prevent an absolute guarantee.

The repository must contain the published pinned source and reusable-workflow commits. A local branch alone cannot be invoked by another GitHub repository.

## Session time budget

Before collection, **Calculate time and size** estimates the selected history and files from message counts and a bounded sample. The display includes time already spent signing in, estimated collection time and a reserve for packaging. For files, the initial estimate uses 1 MiB/s and a twofold time margin; progress replaces that assumption with the measured rate. Use **Messages only** or select fewer chats when the estimate exceeds the remaining time.

Telegram's reported Takeout wait is added to the budget. The collector stops acquisition when the remaining time is needed for packaging, retains acquired data and marks a partial result. A 120-minute session therefore uses its remaining collection window rather than waiting for the deadline before preparing the archive. The display identifies selections whose full size could not be sampled.

## Choose this mode or a persistent workspace

| Capture mode | Configurable scope | Difference |
| --- | --- | --- |
| Telegram Takeout, the default | All accessible cloud chats or selected chats, dates, account categories, media policies and JSON/HTML views | Uses Telegram's official export mechanism; approval or waiting may be required. Takeout can enumerate left channels/groups where Telegram permits it and request additional personal data. |
| Regular Telegram API | The same account scope and output choices, subject to methods available through the regular API | Does not initialize Takeout; cannot enumerate left channels/supergroups or fetch Takeout-only personal data. Contacts cover Telegram users rather than the complete saved phone contact list. Rate limits still apply. |
| Chat event journal | One selected chat, attachment policies and optional avatars | Captures history and changes observed during this run. Account categories, date filters and Desktop-compatible views do not apply. |

All three modes have the same GitHub attestation and encrypted delivery. Takeout is an acquisition method, not a stronger signature. It is never silently replaced by regular API access. JSON/HTML views are generated by TgWitness; they are not Telegram-signed files or guaranteed byte-identical Desktop exports. See the [official Takeout API](https://core.telegram.org/api/takeout).

Defaults use Takeout, all accessible chat types including archived chats, all dates, account profile and contacts, compatible JSON and HTML, and file downloads. The initial media budget is 4 GiB, with visible per-type file limits; larger files or exhausted download budgets use server hashes where available. Review these limits before collecting. Hashes cannot reconstruct a file. Optional photos, stories, session metadata and extra personal data remain separate choices.

Takeout may require approval in an established Telegram session. Telegram sets the delay; a new login or runner does not bypass it. The maximum capture window is 120 minutes including login and approval, so a large account or long approval wait may not finish. A persistent local export can resume the same session, but does not inherit GitHub attestation.

### Agree and verify the settings

After **Check settings and size**, use **Save settings for verification**. Agree the resulting `sealed-export-settings.json` with the reviewer before collection. Changes invalidate the saved assessment. The collector signs the effective settings and their SHA-256, and account-export receipts bind the same options. The verifier reports the actual mode, selection and completeness, and rejects a disagreement between the journal and nested account export.

```
python -m tgwitness.sealed_verify evidence.zip --bundle attestation.jsonl --repo OWNER/TgWitness --expected-selection sealed-export-settings.json --require-complete
```

`--expected-selection` rejects a different transport, chat scope, filter or attachment policy. `--require-complete` rejects partial account exports and chat journals, whose overall completeness is not established. Without these flags, verification still checks provenance and integrity while reporting the recorded settings and gaps. A file supplied only with the finished archive cannot establish what was agreed beforehand. A valid signature never turns omitted data into data that was collected, or proves the owner did not edit/delete messages before capture.

| Need | Mode |
| --- | --- |
| Export accessible account data or selected chats during a limited session and give a reviewer an externally attested archive | GitHub Actions capture (preview) |
| Observe several chats continuously, manage accounts, search and read a growing archive | Local or Docker workspace |

This starts a separate capture with a new login. It does not upload your existing local journal, export the currently open workspace, or reuse its Telegram session. An unfinished cloud capture cannot resume after its runner is destroyed; a new workflow starts a new capture.

The workspace's **Exports → Open capture helper** opens the complete wizard inside the panel. The standalone page uses the same wizard, controls and themes. Both keep keys and decryption in your browser. GitHub workflow startup and the temporary Telegram panel open in separate tabs; the wizard tells you when to return. Locking the workspace clears the wizard's in-memory key. Your saved key file remains on your device.

## What is public, and what must stay private

Collection runs on a standard GitHub-hosted runner. GitHub, the approved collector and dependencies, the helper page, the browser and the HTTPS tunnel are trusted parts of this setup. The temporary host processes the Telegram session and plaintext messages; the delivered artifacts are encrypted for the recipient.

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
| No `sealed-result` | Cancellation or expiry before starting collection produces no archive. A failed collection, attestation or packaging step also prevents delivery. Inspect the failed step without posting credentials. |
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

For multipart delivery, decrypt the main package first and keep its extracted manifest beside every encrypted part, then run:

```
python -m tgwitness.sealed_parts evidence.parts.json --key sealed-key.json --out evidence.zip
python -m tgwitness.sealed_verify evidence.parts.json --assembled evidence.zip --bundle attestation.jsonl --repo OWNER/TgWitness
```

The manifest is the attested subject and binds every part and the assembled ZIP. Use `--max-gib` to set an appropriate uncompressed verification ceiling for a large archive; the default is 4 GiB. Expected-selection and complete-scope checks also work with multipart delivery.

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

The collector runs as a non-root user with a read-only image, dropped Linux capabilities, resource limits, and no Docker socket or GitHub-token environment. Its only mounts are fresh configuration, workspace, and output directories. The restricted FastAPI application exposes login, dialogs, configurable account or chat collection, status, resume, finish, and cancellation. There is no plaintext download route, general administration route, import route, or signing endpoint.

The supervisor stops the network-facing containers before the attest action reads the final fixed `evidence.zip` or `evidence.parts.json`. The packaging container has no network. The upload steps name only `connection.tgwsealed` and `delivery*.tgwsealed`; neither plaintext evidence nor Telegram credentials are uploaded as artifacts. Cleanup removes the private directories and containers, with no claim of physical disk erasure. Artifact retention is one day; download before expiry.

A fork owner can replace the caller or create a different signed file. The strict verifier must reject the resulting **different signer workflow/digest**. This construction still depends on the absence of exploitable bugs in approved code and on the integrity of GitHub's runner and signing infrastructure.

## Cryptographic handoff

Each recipient key is RSA-3072 (RSA-4096 imports also accepted), exponent 65537. Each envelope has a fresh random AES-256 key and 96-bit nonce. RSA-OAEP with SHA-256/MGF1-SHA256 wraps the AES key. AES-GCM with a 128-bit tag authenticates the complete prefix and payload. The public recipient is DER SPKI in base64; the private key file contains DER PKCS8 in base64.

Envelope bytes are `TGWSEAL1\n`, a big-endian uint32 JSON-header length, the header, ciphertext, and a 16-byte GCM tag. The header has exactly `algorithm`, `key`, and `nonce`; algorithm is `RSA-OAEP-256+A256GCM`. The complete prefix through the header is GCM additional authenticated data. Header size is bounded at 8192 bytes. The CLI streams payloads up to 8 GiB and authenticates before installing the requested output; it refuses overwriting an existing destination. This is a project-specific envelope around standard cryptographic primitives, not an independently audited encryption format.

The original evidence bytes are attested **before** placing the evidence and attestation in the encrypted outer package. This avoids a circular dependency between the archive's hash and a certificate included inside that same archive. For public repositories, attestation metadata (repository, workflow, commit, artifact name and digest) is public. Never put chat names in public metadata.

## Limits and validation

This mode uses the signed journal and account-export engine. Secret Chats, deleted history from before collection and data inaccessible to the account are excluded. Private cloud chats are eligible when selected. The chat picker is capped at 20,000 dialogs; account export discovers its own inventory. Missing data, failed files and unfinished tasks are recorded. Attachment limits and runner disk/time limits still apply. Large delivery uses encrypted parts instead of a fixed 4 GiB delivery cutoff. Completion means the frozen selected tasks finished, not that every historical Telegram record exists in the archive. The chat journal can also observe live updates; neither mode is an atomic snapshot. Generated screenshots and screen recordings are not part of this mode.

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


---

# Build a Case Board

Canonical page: https://phishdestroy.github.io/TgWitness/docs/case-board/

Turn saved messages into a case your team works on together.

Bookmarks, exact quotes, slices and discussion, each linked to its source. Every change is a signed revision.

## From a message to a case card

1. **Investigation → Case Board** (Standard or Expert mode). Make a collection for the case.
2. In **Journal** or a chat hit **To board** (or **B**). The card lands in Inbox, give it a title and move it.
3. Select text in a message, **Highlight → board** keeps the exact quote and version. Note why it matters.
4. Discuss, set a status, jump back to the source whenever needed. **Presentation** walks the team through it.

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

Shift-click two messages for **Slice between**, use **Slice by time**, or save the current Journal filters. **Show records added since bookmark** shows what came in later.

Time slices use observation time; message-ID slices follow those messages as they change.

## Give each colleague the right role

**Reviewer** reads, **Analyst** adds cards and comments, **Operator** also manages collections and decisions. Chat permissions apply to cards too.

## Carry the work into a deliverable

Slices export as signed JSON or CSV. Reports can include bookmarks, slices and comments, set that in [Report studio](https://phishdestroy.github.io/TgWitness/docs/reports/). For a limited recipient, use a [handover](https://phishdestroy.github.io/TgWitness/docs/handover/).

Details: [Case Board reference](https://phishdestroy.github.io/TgWitness/docs/reference/case-board/).


---

# Design a report

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


---

# Prepare a sharing copy

Canonical page: https://phishdestroy.github.io/TgWitness/docs/handover/

Share only what's needed, the original stays untouched.

A handover is a separate signed extract: pick chats and people, hide identities or text, choose files and team notes. The manifest records what was kept, trimmed and left out.

## Prepare the recipient's extract

1. **Exports → Handover extract**: write the purpose, pick chats and a period, **Load people of the chosen chats** if you need named people.
2. Everyone else: pseudonyms, left out, or as recorded. Text and files are separate switches; phones and emails can be masked.
3. Case Board: nothing, bookmarks and slices, or cards with comments. Team names can be swapped for aliases.
4. **Download handover extract**, open it, verify it, look through it before sending.

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
| People | Selected people stay named; others get pseudonyms or are left out. |
| Text | All text, only the selected people's and your account's, or none. |
| Files | Files of the selected people and your account, all shown files, or none. |
| Case Board | Nothing, bookmarks and slices, or cards with discussion. |

Read the text and files too: a pseudonym doesn't remove names written inside a message or attachment. If a selected file is missing, restore it or leave attachments out.

## Keep the copy independently checkable

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Keep the original archive and checkpoints yourself. The recipient can verify their copy without getting the whole workspace. Design: [Report studio](https://phishdestroy.github.io/TgWitness/docs/reports/). Trusted references: [export verification](https://phishdestroy.github.io/TgWitness/docs/exports/).


---

# Manage a group of accounts

Canonical page: https://phishdestroy.github.io/TgWitness/docs/groups/

Run several accounts together, each still with its own records and key.

A group puts connection status, start/pause, shared settings and exports on one screen. Handy when several accounts work the same case.

## Open the group overview

Open the group in **Accounts**. Each account shows its state, route, latency and last saved message. **Needs attention** lists the broken ones, **Fix** takes you straight there.

**Start all** / **Pause all** ask before acting. **Group settings** are shared, but an account's own values stay until you replace them.

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

1. **Change the group route**, pick the type and settings.
2. **Review selection**: see which accounts change and which have their own route.
3. **Prepare and check** tests a fresh Telegram connection, plus the exit IP where possible.
4. **Apply checked connection** and look at each result. Running accounts resume, idle ones stay idle.

Latency is the Telegram connection setup time, the exit IP is what the route showed at check time. Results can differ per account.

## Use overlapping access

**Chats several accounts see** lists shared sources and their coverage. Channels and supergroups can be exported by several accounts at once with **Export with … accounts**. Private chats and basic groups can't, their message numbers are per account.

## Export the group as a package

**Export group** gives one ZIP with every account's signed export and a signed list of them. Each keeps its own fingerprint for verification. A merged timeline you still build yourself.

Next: [reports](https://phishdestroy.github.io/TgWitness/docs/reports/), [Case Board](https://phishdestroy.github.io/TgWitness/docs/case-board/), [verifying exports](https://phishdestroy.github.io/TgWitness/docs/exports/).


---

# See how evidence works

Canonical page: https://phishdestroy.github.io/TgWitness/docs/concepts/

Messages change. Your record of what you saw shouldn't, and anyone should be able to check that.

Two small experiments below. Fake messages, everything runs in your browser, nothing goes to Telegram.

## From a chat export to a verifiable record

A [Telegram Desktop export](https://telegram.org/blog/export-and-more) saves the history you can see right now as HTML or JSON. TgWitness adds a running journal of changes, signatures on every record and checkpoints others can compare against.

| Task | Telegram Desktop export | TgWitness |
| --- | --- | --- |
| Read saved conversations | HTML or JSON with selected media | Saved chats, searchable journal and offline reports |
| Follow a change over time | The history available when exported | Old versions, later edits and deletions, all kept |
| Check files after handover | Standard HTML/JSON export files are unsigned | Signed manifest, signed records and sealed reports, checked against a trusted key |
| Compare with an earlier retained state | Keep a separate reference copy or hash | Signed checkpoints, a separate witness and optional external timestamps |

The comparison is based on the [Telegram Desktop export code](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) as of 2 November 2026.

## One message, three observations

A new message, an edit and a deletion become three separate records. The edit doesn't overwrite the first one, and the deletion doesn't erase it.

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

Telegram doesn't say who deleted a message or exactly when. TgWitness leaves those fields empty instead of guessing.

## Change a record. Follow the hash.

Every record contains the hash of the one before it. A checkpoint kept somewhere else pins the journal length and the last hash.

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

**C** is the nine event fields as UTF-8 JSON: sorted keys, no extra whitespace, no ASCII escaping, no NaN/infinity. `previous_hash` is hi−1, h0 is 64 zeros, signatures cover the 32 raw digest bytes.

The fields: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. Full spec: [event encoding](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#event-canonicalization).

RETAINED CHECKPOINT

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Check the checkpoint signature against the pinned key, then compare it with the journal. A later export can be longer, but it has to match at the checkpoint.

## Three questions, three different checks

[01 / INTEGRITY**Did this record change?** Hashes and signatures against a key you trust.](https://phishdestroy.github.io/TgWitness/docs/exports/)[02 / CONTINUITY**What was retained earlier?** Compare the export with checkpoints a witness kept.](https://phishdestroy.github.io/TgWitness/docs/witness/)[03 / DELIVERY**Did these test events arrive?** Send, edit and delete test messages and see what each account caught.](https://phishdestroy.github.io/TgWitness/docs/cases/)

Signatures answer "was it changed", checkpoints answer "does it match what was there before", test messages answer "did we catch everything". [What verification proves and what it doesn't.](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope)

Next: a [whole-account investigation](https://phishdestroy.github.io/TgWitness/docs/cases/) from start to case package.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.


---

# Keep it secure

Canonical page: https://phishdestroy.github.io/TgWitness/docs/security/

What leaves your machine, what each secret opens, and what the protections cover versus what's on you.

**127.0.0.1**panel address by default

**256-bit**random panel token

**0**CDNs, analytics or remote fonts

**Ed25519**signature on every record

## Where everything lives

The collector, the panel and every record stay on your machine. By default only Telegram is contacted; everything else is a separate switch.

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
| **Panel token** | `panel-token.txt` in the data directory; the browser keeps it per tab | Everything in every workspace | Stop TgWitness, delete `panel-token.txt`, start again: you get a new one |
| **Telegram session** | Vault, encrypted (`credentials.enc`) | The Telegram account itself | End the session in Telegram under *Settings → Devices* |
| **Signing key** | Vault, encrypted (`signing.enc`) | Signing records under your fingerprint | Checkpoints kept elsewhere, a witness and timestamps still show what existed before |
| **Vault key** | `vault.key` next to the data, or an external master key | The vault | Assume the session and signing key leaked too |
| **Witness token** | On the witness host | Read-only: checkpoints and health | Delete it on the Witness page, make a new one |
| **Off-site copy key** | Vault; download it once for recovery | The off-site copy | Anyone who also has the bucket can decrypt it: treat the copy as exposed |

## What the protections cover

### Covered

- A changed, removed or reordered record: the hash chain or a signature breaks.
- A journal cut back or rebuilt after you saved a checkpoint elsewhere: the checkpoint stops matching.
- Guessing the token: 256 random bits, constant-time compare, 15 failures a minute and the address is blocked.
- Hostile chat content: text stays text, never HTML; attachments download as files; the panel loads nothing from other sites.
- A stolen data directory with an external vault key: sessions and keys stay encrypted.

### Left to you

- The main token can do everything. Give others scoped access and keep the main one to yourself.
- Whoever is admin on the machine can read everything and re-sign the journal. Keep the fingerprint and checkpoints elsewhere.
- Messages and media aren't encrypted by TgWitness. Encrypt the disk, lock down permissions.
- Plain HTTP outside localhost leaks the token. Use HTTPS or an SSH tunnel.
- Signatures don't tell you what was missed. Check coverage and test delivery on your own accounts and sources.

[Share access to a case](https://phishdestroy.github.io/TgWitness/docs/access/) with permissions, expiry and session limits.

## Harden an installation

0 of 8 done

1. **Use a dedicated Telegram account**, never your main one.
2. **Keep the panel on 127.0.0.1.** Remote access only via HTTPS (bundled Caddy) or an SSH tunnel.
3. **Encrypt the disk** with the data directory, messages and media are stored as is.
4. **Restrict the data directory** to the service account (0700 on Unix, folder permissions on Windows).
5. **Keep the vault key elsewhere** on servers: set `TGWITNESS_VAULT_KEY_FILE` before the first start.
6. **Save the fingerprint and checkpoints** on another system, run a witness on another host.
7. **Never upload** `data/`, sessions, `panel-token.txt` or vault keys to GitHub or a chat.
8. **Do not log** `Authorization` headers or request bodies at a reverse proxy.

**Can I change the panel token without losing data?**

Yes, it only opens the panel. Stop TgWitness, delete `panel-token.txt`, start again. Journal, sessions and keys stay. If `TGWITNESS_TOKEN` is set, that value wins over the file.

**Why are messages not encrypted at rest?**

The collector has to read them to search, compare and export. A key on the same machine wouldn't stop someone who can read that machine anyway. Disk encryption covers a stolen disk, permissions cover a running one.

## Report a vulnerability

**Security → Report a vulnerability** on GitHub. Version, impact and a minimal repro with fake data. Never send credentials, account folders or real evidence. If private reporting is off, open an issue asking for a private channel, no exploit details.


---

# Set up a witness bot

Canonical page: https://phishdestroy.github.io/TgWitness/docs/witness/

A separate process checks your journal and posts signed checkpoints to a channel.

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

Make a bot with BotFather and let it post in your channel. Run the witness somewhere else: another host, ideally run by someone else, is worth much more than a second process next to the collector.

## Three steps in Extras

1. **Read-only access.** **Extras → Independent witness**, create a token, save the file. It reads checkpoints and health, nothing else.
2. **Channel and interval.** Telegram channel or Discord webhook, plus a collector address the witness can reach. Save the settings file.
3. **Launch.** Put `witness.json`, `witness-token.txt` and `bot-token.txt` together on the witness host and run:

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Wait for the first signed post in the channel, then save the witness fingerprint somewhere safe.

Discord instead? Save the webhook URL as `discord-webhook.txt`. One witness posts to one place; long checks arrive as a file on Discord.

## Choose how often to publish

Posting every check gives a steady outside record: every five minutes is about 288 posts a day per workspace. Advanced settings can post only on changes or problems, use a proxy or a custom Bot API.

**What does the bot actually attest to?**

It asks the collector for a signed checkpoint, checks it against the expected key and keeps its own signed journal, including missed and rejected answers.

It checks the journal state, it doesn't watch Telegram itself. For that, run a controlled delivery test.

## Check the evidence later

Keep the witness journal, the posts and the fingerprints. [How to check them](https://phishdestroy.github.io/TgWitness/docs/reference/witness/#verify) against the collector's export.


---

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


---

# Share a case

Canonical page: https://phishdestroy.github.io/TgWitness/docs/access/

Share the case someone needs. Keep control of the rest.

01**Choose the evidence**

Whole workspaces or single chats.

02**Choose the actions**

View, export, or just the operations they need.

03**Set the limits**

A personal token with expiry, session limits and IP rules if you want.

Collection scope decides what is recorded. Access scope decides what a person can see and do.

## Give someone access

1. As admin, open **Access**.
2. Name it, pick workspaces and chats.
3. A reviewer needs only **View**. Add **Export** for downloads.
4. Set limits, then press **Create access**.
5. Copy the token (shown once) and send it privately with the panel address.
6. Check what they'll see in a separate browser session first.

## Start with the job they need to do

| Person | Access | Result |
| --- | --- | --- |
| Reviewer | Selected chats; view only | Reads the chat, can't change anything. |
| Analyst | Selected chats; view and export | Reads and downloads what the case needs. |
| Operator | Selected whole workspaces; sources and collection | Decides what's observed, starts and stops collectors. |

These are just examples, not fixed roles. Chat-limited access never gets account settings or full journal exports. All-workspace access includes accounts added later.

## Change your mind at any time

Edit access any time, it applies from the next request. End one session or revoke everything. Already downloaded files are gone for good. Collection keeps running.

**Session and IP limits**

Limit parallel sessions and sign-ins, set an end date, allow IPs or subnets, or lock to the first sign-in IP. Expiry counts inactivity, an open panel counts as active. Behind a proxy, check which client IP the app sees.

**The main key and the activity log**

The main token stays with the admin. Issued access can't manage other people's access or open the admin console. Access changes and sessions are signed into the journal, without tokens. The server admin can still see everything.

All seven permissions and session rules: [access reference](https://phishdestroy.github.io/TgWitness/docs/reference/access/).


---

# Keep it running

Canonical page: https://phishdestroy.github.io/TgWitness/docs/server/

Keep the collector up and the data safe through restarts.

## Choose a launch method

Native: the [launcher](https://phishdestroy.github.io/TgWitness/docs/start/) plus service templates in [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker, from the project folder:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

The panel listens on localhost:8787. Open it locally or through an SSH tunnel, with the token from the second command.

## Keep the whole data directory

Native: `data/live`. Docker: the `tgwitness-data` volume. Journals, sessions and keys belong together. A signed export is evidence, not a backup.

1. Stop collecting first.
2. Copy the whole data directory somewhere safe, off the host.
3. Try restoring it on a separate install before you trust it.

## Check after a restart

Check the workspace and key, the connection, sources and that new messages come in. TgWitness catches up what Telegram still has, not everything that happened while it was down.

"Healthy" container means the web server answers. Whether collection works, a test message and the witness will tell.

## Publish only what you intend

HTTPS, volumes, updates and restore are in the deployment reference. What's actually been tested: [validation record](https://phishdestroy.github.io/TgWitness/docs/reference/verification/).


---

# Find what went wrong

Canonical page: https://phishdestroy.github.io/TgWitness/docs/troubleshooting/

Start from the symptom, check one thing at a time.

## The panel asks for a token

It wants the panel token from the file the launcher printed. Docker: `docker compose exec tgwitness cat /data/panel-token.txt`. Not a Telegram code, not a bot token, not the witness token.

## Telegram does not connect

Run the connection check. On a public proxy, pick another one and save. Check the proxy type and secret format. Refreshing lists doesn't switch the route by itself.

## Connected, but no new messages

1. Is observation running, in the right workspace?
2. Is the source selected and visible to that account?
3. Send a unique message in your test group and search for it.
4. Look for interruptions or Telegram errors in the journal.

A quiet chat just has nothing new. If completeness matters, run a controlled delivery test.

## FloodWait or a gap after a restart

FloodWait is Telegram saying "slow down". Wait it out and lighten the load, reconnecting won't help. After a restart TgWitness catches up what Telegram still has; the rest is a gap, so write it down.

## The bot is configured but posts nothing

Is the witness running, can the bot post in the channel, can it reach the collector and Bot API? Look in its journal for failed posts. A poll on the collector side doesn't mean a post went out.

## Where is GitHub token integration?

**Planned.** Extras describes the proposed fork and build verification workflow. There is currently no GitHub token form or automated attestation that a running installation matches a repository. See the [current feature status](https://phishdestroy.github.io/TgWitness/docs/reference/features/).

Reporting a bug? Version, OS, steps and a redacted error. Never put sessions, tokens, private messages or the data directory in a public issue.


---

# Export Clinic

Canonical page: https://phishdestroy.github.io/TgWitness/docs/export-clinic/

The chat says FAIL. The exported page says PASS. Watch the change, compare the files and check how it happened.

This experiment uses test accounts and scripted conversations. Telegram Desktop was downloaded from the official source and its executable was unchanged. A local helper deliberately changed selected export files.

Watch the download, sign-in and export, then compare the Telegram conversation with the altered HTML and JSON. The experiment shows where an ordinary export can be changed and why a record of the collection process matters.

**1:59.7** condensed film**6:08.8** full source recording**7** test conversations

## Watch the experiment

[Download the film](https://phishdestroy.io/research/telegram-export/2026-11-03/export-clinic-2min.mp4)

1:59.7 · Setup and repeated steps are accelerated ×2–×15 and labeled. Sign-in, the first export and selected comparisons run at their original speed. No audio.

[Download original MKV ↗](https://phishdestroy.io/research/telegram-export/2026-11-03/ExportClinic_2026-11-03_12-50-40.mkv)

## Compare the test exports

These excerpts come from the retained and modified JSON files. Choose a conversation type, compare the messages, then download the complete paired exports to inspect the HTML, JSON and included images yourself.

### Export Clinic | PDF Check

5 messages · 2 changed

**BEFORE THE LOCAL CHANGE**Retained original bytes

DOCUMENT CHECK / SYNTHETIC TEST RESULT: FAIL Hidden text remains selectable beneath the black rectangle. This is a scripted result for the demonstration PDF, not an examination of a third-party document.

d58d19814e1e07d5…

**AFTER THE LOCAL CHANGE**Deliberately altered bytes

DOCUMENT CHECK / SYNTHETIC TEST RESULT: PASS All sensitive text has been permanently removed. This is the deliberately substituted demonstration result.

83a0a37eb7110d51…

result.json · message 1216

Scripted scene content. The bot verdict is not an examination of a real third-party document.

Changed message 1 of 2

**Compare an included image from this export**

![Image before local modification](https://phishdestroy.github.io/TgWitness/docs/export-clinic/)

BEFORE · retained image bytes

![Deliberately modified image](https://phishdestroy.github.io/TgWitness/docs/export-clinic/)

AFTER · deliberately substituted image

Attachments were not included in this bot export. The archive preserves that limitation.

JavaScript is disabled. The default bot comparison and all downloads remain available. Download the paired archive to inspect the other six conversations.

## What the comparison demonstrates

Telegram's [normal export feature](https://telegram.org/blog/export-and-more) saves history and selected media as local files. Here, a helper with write access changes those files while the official client continues to show the original conversation. The paired files let you inspect each change.

1. **Official client:** download, sign in and inspect the test conversations.
2. **Native export:** the client writes HTML, JSON and selected images.
3. **Disclosed intervention:** a local helper deliberately changes selected files.
4. **Comparison:** the conversation and altered export appear side by side.

### Record the data as it is collected

The timing of a signature matters. Signing an already altered export preserves that altered version. TgWitness connects to Telegram, records the content delivered to the account, and signs and links journal entries during collection. The recipient can check the saved records and files against those signatures and independently retained checkpoints.

For an externally recorded collection process, [GitHub Actions capture](https://phishdestroy.github.io/TgWitness/docs/capture/) runs a pinned TgWitness collector with a fresh Telegram session. GitHub attests the resulting archive. Verification checks the approved workflow and collector version, the archive digest, journal and attachments.

[Verify a TgWitness archive](https://phishdestroy.github.io/TgWitness/docs/exports/#verify) · [Try changing a signed record](https://phishdestroy.github.io/TgWitness/docs/concepts/#chain) · [Run a GitHub capture](https://phishdestroy.github.io/TgWitness/docs/capture/)

## What Forensic Tools Actually Certify

Export Clinic demonstrates one specific case. The pattern it reveals is not specific to Telegram.

In the overwhelming majority of proceedings we have reviewed — across court filings, case discussions, and published analyses — "digital evidence" follows a consistent format: a Telegram export (HTML or JSON file, sometimes a screen recording of a monitor, sometimes a video from an iPhone navigating through profile pages) paired with an expert signature. That is typically the entire evidentiary chain.

Telegram does not cryptographically sign its export output. It has never claimed to. The export feature exists for personal data portability. Somewhere along the way, someone decided these files carry evidentiary weight in court — and that assumption has rarely been challenged at the technical level. In our assessment, this is one of the most significant open gaps in digital forensics practice today.

### The Tools Are Honest. The Problem Is What People Assume They Prove.

We have worked with UFED Cellebrite directly. It is excellent software. When it extracts data from a device, calculates SHA-256 hashes, and produces a signed report, it is accurately certifying exactly one thing: *these bytes were on this device at the time of extraction, and nothing changed in transit.*

That is real. That is useful. That is the complete extent of what it proves.

It says nothing about what was on the device before law enforcement touched it. It says nothing about whether the data reflects historical reality. The tool is correct. The tool is not a witness.

We could take tools specifically built to handle Telegram chat exports — viewers, archivers, court-presentation wrappers — test each one against prepared export files, and produce a comparison table. We won't. The point isn't which tool catches what. None of them can. They process what the export contains. If the export was constructed before it reached them, they report the construction faithfully.

A cryptographic signature certifies the integrity of data *from the moment of signing forward*. It makes no claim about what happened before. If the input was constructed before extraction, the report is cryptographically perfect and factually false. The tool reports both outcomes identically.

### The Accountability Gap

Imagine a jurisdiction where forensic equipment is procured through public tenders — versions, configurations, and acquisition timelines available in public records. Where no law requires devices to carry current firmware. Where expert witnesses bear no personal criminal liability before a court for their conclusions.

In the United States and United Kingdom, a forensic examiner faces individual legal accountability for every action they take with evidence. That accountability — not the software — is what makes the evidence chain function. Remove it, and the same tool that serves justice becomes available to serve whatever purpose the license holder finds convenient.

**Technical construction of pre-seizure device state**

If a subject learns of an impending seizure with sufficient lead time — seven days is more than enough — panic responses are both counterproductive and, in some jurisdictions, separately criminal. A prepared subject with technical access and resources does something different: they construct a device state.

**The firmware window.** Top-tier Samsung Galaxy S Ultra, Z Fold — Knox protection, locked bootloader. The gap between a security patch release and its availability for a specific regional device routinely reaches a month. For newly launched models the window in the first three to four months is considerably wider. No jurisdiction we are aware of legally requires current firmware on a personal device.

**Service-level tools.** Commercial servicing software provides low-level device access during this window without triggering the Knox tamper indicators a forensic examiner would look for.

**Timeline construction.** A full device backup deployed to an emulator, script-driven time manipulation and network isolation, allow construction of a desired event timeline: calls, messages, application activity, GPS coordinates.

**Location without cellular exposure.** Cellular tower billing records are independently verifiable — don't touch them. Instead, connections to public Wi-Fi access points are logged. The MAC addresses of public infrastructure are systematically collected and distributed by major technology corporations. A continuous geographic chain covering any desired period can be assembled from publicly available data.

**Account rotation.** Samsung account deletion takes approximately seven days for complete removal. A new account is created, the prepared backup is restored. No system integrity conflicts, bootloader untouched, no tamper flag triggered.

**Telegram specifically.** On certain device families, the application database and cache — conversations, media, notification metadata, activity patterns — can be replaced at the OS capability level without classical root access. Deep analysis by specialists examining a full raw dump could potentially detect anomalies. That analysis is expensive, slow, and in our experience essentially never requested in standard proceedings.

### Garbage In, Garbage Out

The signed report binds the extracted bytes to that acquisition．Earlier device history is assessed using records from the earlier period．

The chain that follows — expert witnesses reading the tool output, writing analyses, signing conclusions — is similarly accurate at each individual step. No one in the chain is lying. No one in the chain is proving historical truth. Each participant accurately reports what they received from the previous step.

A doctoral degree is a record of completed past research. It is not a current competence certification, and it cannot make a mathematically unverifiable claim true. We propose a different standard: **trust the math, not the title.**

### Zero Trust for Evidence

In information security, "Zero Trust" means no actor is trusted by default regardless of position or credentials — every claim must be independently verified. We propose applying the same principle to digital evidence. Trust is a vulnerability. If a claim cannot be verified independently and mathematically, it is a trust claim — and trust can be misplaced, purchased, or coerced.

For Telegram export evidence specifically: do not trust us, do not trust Telegram, do not trust the analyst, do not trust the expert witness. Verify the math.

What that looks like in practice: TgWitness attestations reference the SLSA v1 Level 3 model — build provenance signed by GitHub Actions infrastructure, bound to a specific commit hash and workflow run. The attestation can be verified independently, without trusting any individual involved in the collection. It does not remove all trust assumptions — it documents exactly which assumptions remain, and what they are.

**On expert witnesses and financial incentives**

A lawyer representing one party in a dispute, presenting themselves simultaneously as a neutral third-party expert in the same proceeding, with compensation tied to their client's outcome: this is a structural contradiction. We are not making accusations about any individual. We are asking why this structure is considered acceptable, and why it is so rarely examined.

The standard counter-argument: *how much would lying cost them?* In jurisdictions with right to erasure and right to be forgotten, the practical cost of pursuing expert perjury is frequently: very little. Those who raise concerns about an incorrect expert conclusion tend to receive legal correspondence requesting the concerns stop. That process is expensive for the person raising concerns. It is not expensive for the expert.

We are not suggesting all expert witnesses are dishonest. We are suggesting that "it would cost them too much to lie" is not a proof standard. It is a trust standard. And trust is a vulnerability.

A subject who wishes to challenge a TgWitness attestation would need to compromise the cryptographic signature, convince GitHub's signing infrastructure to retroactively attest something it never ran, and do so against an immutable commit history — with a witness present. If those capabilities exist and have merely been concealed beneath difficulty operating PDF software, we would genuinely welcome the demonstration.

We are not claiming our tools are better — we do not have a commercial product and have no interest in one. We observed a problem: the widespread assumption that forensic software output equals historical truth, and that expert signatures equal proof. That assumption is rarely challenged at the technical level in the proceedings where it matters most. This experiment is one controlled data point. The math has no opinion about titles.

## Download the materials

Videos and ZIP files are hosted on [phishdestroy.io](https://phishdestroy.io/). Choose the files you want to inspect. Both ZIPs contain selected test data and documentation. The modification tool, source, configuration, credentials and sessions are excluded.

### Before / after exports

Seven test conversations: HTML, JSON, included images and the standard viewer assets. Includes a file manifest and selected change ledger.

[Test exports · ZIP · 3.0 MB ↓](https://phishdestroy.io/research/telegram-export/2026-11-03/export-clinic-paired-files.zip)

No video. No modification tool.

### Video + test exports

The full original recording, the two-minute film, the paired exports, explanation, metadata review, edit map and checksums.

[Video + test exports · ZIP · 46.9 MB ↓](https://phishdestroy.io/research/telegram-export/2026-11-03/export-clinic-review-package.zip)

Contains the smaller ZIP. No modification tool.

**Exactly what is inside the 46.9 MB ZIP?**

- `video/ExportClinic_2026-11-03_12-50-40.mkv` — the untouched full recording, 6:08.8.
- `video/export-clinic-2min.mp4` — the condensed film, 1:59.7.
- `data/export-clinic-paired-files.zip` — extract this nested ZIP to inspect the `before/` and `modified/` folders.
- `description/article-en.md` — the explanation and limits.
- `verification/` — four JSON/Markdown files covering the edit map, metadata inspection and package review.
- `README.md` and `SHA256SUMS.txt` — reading instructions and file checksums.

Ten files in the outer ZIP. The separate full MP4 is omitted because the original MKV already contains the complete recording. Standard `js/script.js` inside each exported chat is Telegram's unchanged HTML-viewer asset.

### Individual video files

- [Original MKV · 6:08.8 · 29.6 MB](https://phishdestroy.io/research/telegram-export/2026-11-03/ExportClinic_2026-11-03_12-50-40.mkv) — byte-identical source recording.
- [Open full MP4 · 6:08.8 · 29.9 MB](https://phishdestroy.io/research/telegram-export/2026-11-03/export-clinic-full.mp4) — a browser-friendly container conversion, without video re-encoding.
- [Open condensed MP4 · 1:59.7 · 14.3 MB](https://phishdestroy.io/research/telegram-export/2026-11-03/export-clinic-2min.mp4) — playback-speed changes are labeled.

[Download checksums](https://phishdestroy.github.io/TgWitness/assets/export-clinic/SHA256SUMS.txt)[Video edit map](https://phishdestroy.github.io/TgWitness/assets/export-clinic/recording-manifest.json)[Paired-file manifest](https://phishdestroy.github.io/TgWitness/assets/export-clinic/review-file-manifest.json)[Metadata review](https://phishdestroy.github.io/TgWitness/assets/export-clinic/original-metadata-notes.md)[Current explanation and verification guide](https://phishdestroy.github.io/TgWitness/assets/export-clinic/article-en.md)

The downloadable review ZIP retains its original README and article. The current explanation includes the TgWitness collection and verification guide.

**How “before” was assembled:** this is a reconstructed pre-change folder tree. Changed files were restored byte for byte from retained backups and matched to their recorded hashes. Unchanged viewer assets were copied from the captured export. The file manifest documents the supplied versions.

Across the seven conversations, there are 45 message records; 17 records and 32 files differ. Each version contains 340 files. PDF attachments were not selected in the recorded exports and are absent from these archives.

## Experiment details

**Where did the change happen?**

A local helper changed files written by Telegram Desktop. The official client executable and the conversations visible in Telegram were unchanged. The comparison shows the original messages beside the altered export.

**Are these complete account exports?**

No. The materials cover seven owned test conversations: a personal chat, a bot, a private group, private and public supergroups, and private and public channels. They contain 45 message records. No unrelated chats, contacts or account-wide archive are included.

**Are the PDF attachments included?**

No. The recorded export settings excluded file attachments. The test messages and images refer to a PDF, but these archives do not contain that PDF. This distinction is preserved in the files and description.

**Does the package include the modification tool?**

No executables, helper source, transformation configuration, session data, credentials or full working logs are included. The small JavaScript files inside the paired exports are Telegram's unchanged standard HTML-viewer assets, checked to be identical across both versions.

**How do I check the downloaded files?**

Calculate each file's SHA-256 and compare it with the published checksums. Matching values confirm that you have the published bytes. The file manifest lists both export versions; the video edit map documents the condensed film. Recording times come from the host clock.

**How does TgWitness make the record checkable?**

The collector signs entries as it receives data from Telegram. The archive includes the journal, file hashes and verification data. Retain a key fingerprint and checkpoint separately, then check the recipient's copy against them. GitHub capture adds verification of the approved collection workflow and its output. [Follow the verification steps ↗](https://phishdestroy.github.io/TgWitness/docs/exports/)

The seven conversations were prepared for this experiment. The recording, paired exports and change ledger document the local-file changes described above.

Controlled local-file experiment · 3 November 2026

Full SHA-256 copied


---

# 56 329 messages.

Canonical page: https://phishdestroy.github.io/TgWitness/docs/validation/

TGWITNESS / REAL EXPORTS

Captured. Exported.

Two fresh Telegram exports, timed from collection to the finished archive. Explore the workspace, inspect the numbers and download a sample.

[Explore the demo](https://phishdestroy.github.io/TgWitness/demo/?lang=en)[Download sample export](https://phishdestroy.github.io/TgWitness/demo/downloads/tgwitness-demo.zip)

The interactive demo and sample use fictional messages. The measurements below come from real export runs.

TGW / 001

Recorded snapshot · not live monitoring

Checked at

2026-11-06 18:37:38 UTC

Tested revision

[92e539af](https://github.com/phishdestroy/TgWitness/commit/92e539af40d8368d198ff5e040f1d876f2c1310e)

Text + metadata · signed archives

**56 329**Messages exported

**160.531**Messages/s · best collection run

**2**Signed export runs

**3**Servers inspected

Server AWARP · 2 accounts

**27 030**Messages exported

**142.983**messages/s

Collection only

189.043 s

Complete export

211.647 s

Server BWARP · 2 accounts

**29 299**Messages exported

**160.531**messages/s

Collection only

182.513 s

Complete export

206.650 s

01 /

## Measured on real exports.

One new export per server, using two accounts on each. Text and metadata through WARP; attachments excluded. These are individual runs, not a capacity guarantee.

messages/s

Server A**142.983 messages/s**

Server B**160.531 messages/s**

Server C

Not measured

—

Messages ÷ collection time. Preparation, selection and packaging are outside this interval.

Messages ÷ total measured export time, including preparation and packaging.

No collection benchmark receipt for server C.

No reused records or duplicate IDs in either run. Server A also had a protected-source read running in the background. FloodWait pauses were respected: A · 4, B · 3.

**Exact measurements & archive hashes**

| Server | Messages | Collection only | Complete export |
| --- | --- | --- | --- |
| Server A | 27 030 | 189.043 s **142.983 messages/s** | 211.647 s **127.713 messages/s** |
| 2026-11-06T18:26:51.500Z → 2026-11-06T18:30:23.228Z SHA-256 `20e507fc68446680ed002fd486d0968a944ec0c71e02f937331ae2b19ab4cd66` |  |  |  |
| Server B | 29 299 | 182.513 s **160.531 messages/s** | 206.650 s **141.781 messages/s** |
| 2026-11-06T18:25:40.419Z → 2026-11-06T18:29:07.173Z SHA-256 `824601b502762efaabb8ff9afdb1e8d7fff189862ef2cbc4d8d26d0d68c83e4c` |  |  |  |

Both archives passed verification with a pinned collector key. This establishes integrity relative to that key, not Telegram authorship.

02 /

## All three, with the scope spelled out.

Journal integrity, file permissions, storage, network routes and running processes were inspected on every server.

A Inspected

### Server A

Collection & export

8 vCPU · 16 GiB · Ubuntu 24.04

Journals checked

21

Journal events

4 517

Checkpoints

147

Fresh collection benchmark, archive verification and backup integrity checks.

B Inspected

### Server B

Collection & export

8 vCPU · 16 GiB · Ubuntu 24.04

Journals checked

21

Journal events

1 993

Checkpoints

147

Fresh collection benchmark, archive verification and backup integrity checks.

C Inspected

### Server C

Panel & nested VM

8 vCPU · 32 GiB · Ubuntu 24.04

Journals checked

14

Journal events

7 185

Checkpoints

973

Panel authentication, loopback binding and a nested VM inspected. No collection benchmark on this server.

**Test results, scope & technical notes**

03 /

## Passes and gaps, side by side.

Latest result per pytest case, including reruns. Standalone browser and evidence suites are counted separately below; they are not added to the pytest total.

**1 585**Passed

**3**Failed

**37**Skipped

Three capture browser tests failed because the required Chromium sandbox is unavailable in these containers. The sandbox was not disabled. The 37 platform skips do not count as passes.

- Browser suites**102 passed**
- Interface suites**66 passed**
- Evidence suites**15 passed**
- Website suites**9 passed**
- Additional suites**13 passed**

04 /

## What this snapshot leaves open.

1. 01

   ### Browser sandbox

   Three browser failures remain in this environment. A successful run elsewhere does not replace these results.
2. 02

   ### Backup recency

   42 backup journals and 51,285 files passed integrity checks. At the snapshot, 3,507 live events were newer than the latest backups. Active data also needs durable storage.
3. 03

   ### Network coverage

   16 of 40 route qualifications were unavailable. Those accounts were not connected to Telegram through a direct fallback.
4. 04

   ### Independent time

   The retained witness journal passed integrity checks. Its last event was at 07:27 UTC on 6 November; independent timestamp verification was not performed.
5. 05

   ### Open security work

   Key protection, account protection, durable storage and release controls still have open findings. Successful integrity checks are not a security certification.
6. 06

   ### Access limits

   The separate CI host and the publishing account were not inspected at operating-system or account level. The three inspected servers are the scope of this page.
7. 07

   ### Measurement limits

   Two public sources, two individual runs, no attachment download and no repeated trials. Server C has no measured collection rate. These numbers do not predict other workloads.

05 /

## A dated record, with a way back to the numbers.

These are operator measurements, not an independent attestation. The JSON contains only aggregate data. Source and account identities, message contents, credentials and private archives are not published.

1. Pin the source revision and verify the installed release.
2. Collect into a new workspace, retaining zero reused records.
3. Measure collection and complete-export intervals separately.
4. Verify the archive against its pinned key; retain its SHA-256 digest.

Tested release `92e539af40d8-83e41104669e`

[Download the data ↓](https://phishdestroy.github.io/TgWitness/validation/snapshot.json)

SIGNED AUDIT / ENGLISH

### Check the numbers.

The English report includes the measured results, open findings and a reproducible signature check.

[Read the report ↗](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md)[Signed statement ↓](https://phishdestroy.github.io/TgWitness/validation/audit/PROOF.json)[Measurements CSV ↓](https://phishdestroy.github.io/TgWitness/validation/audit/MEASUREMENTS.csv)[Python verifier ↓](https://phishdestroy.github.io/TgWitness/validation/audit/VERIFY.py)[File checksums ↓](https://phishdestroy.github.io/TgWitness/validation/audit/SHA256SUMS.txt)

The signature protects the report against alteration. It does not independently attest the measurements or certify GDPR compliance. The report records the completed audit at 19:08 UTC; the infrastructure snapshot above was taken earlier.

**Source receipt digests**

These hashes identify retained receipts. A hash alone does not prove the measurements; the private originals are not downloadable from this page.

- benchmark-1.json`66cdf2db25901ee1f780a0e2d14b9b84888dbe525bff73bae19819b217f95d0c`
- benchmark-2.json`ad2978fe2a7563476da43293eaaf5f498ee12522f0ea3e401bc43205c64874d1`
- test-totals.json`922cf87d9320b149f2fc6791fc05f98335ec0952f9258e6eaeff179aeef33bb1`
- infra-summary.json`325d390ef752b15f44203f97348863e24f0f631fe88998d5e1f398a5311a9339`

The page is a snapshot, not a claim that every function or account has been tested. Absence of a measurement is shown explicitly.


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

## Full-text search settings

[Full-text search](https://phishdestroy.github.io/TgWitness/docs/reference/search/) (preview) needs no setup. Its index is built in the background after an update.

| Variable or command | Effect |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | Default: the index is kept in `search/fulltext.sqlite3` of each workspace |
| `TGWITNESS_FULLTEXT=memory` | No index file; the index is rebuilt at every start |
| `TGWITNESS_FULLTEXT=off` | No index; only exact-text search |
| `tgwitness index status` | Index state of every workspace |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | Rebuild every index from the signed journal |

The administrator's choice in **Journal → Filters → Search index** overrides the variable for that workspace. Commands find the data directory of the installation that runs them; elsewhere, add `--data-dir` with the path from `tgwitness paths`. For a full Ukrainian dictionary (GPL-3.0 data), install `pymorphy3-dicts-uk` in the installation's Python environment.

## Command-line access

The [command line](https://phishdestroy.github.io/TgWitness/docs/reference/cli/) (preview) reads the archive for scripts and agents.

| Variable | Effect |
| --- | --- |
| `TGWITNESS_URL` | Panel address for `tgwitness search`, `context`, `messages`, `stats` and `export`; default `http://127.0.0.1:8787` when a token is set |
| `TGWITNESS_MCP_TOKEN` | Archive connection token from **Integrations → MCP**, shared with MCP clients; `--token-file` reads it from a file instead |
| `TGWITNESS_DATA` | Data directory read directly when no `--data-dir`, URL or token is given |

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

Publication is automatic after that exact commit passes the application and security checks and the signed package passes Ubuntu service and Windows PowerShell installation tests. While checks are running, or if they fail, the same commands continue to install the previous checked build. The build manifest shows which commit is currently available; the version number alone may stay the same between preview updates.

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

You can sign in without creating a Telegram API application. When no pair is entered, imported or already saved in the workspace, TgWitness picks a pair from its built-in pool of 50 public API pairs (`tgwitness/api_pool.py`), preferring Telegram Desktop for a fresh login and retaining a saved pair first; remaining candidates are shuffled. If Telegram refuses a pair (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), the next one is tried, up to eight per sign-in; refused pairs are skipped until restart. The pair that signed in is saved with the account and reused for it. An **API ID** and **API hash** identify the application to Telegram; they do not authorize an account by themselves.

Missing connection fields use a deterministic device/OS pair from the bundled [opentele2 2.0.0 catalogs](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735): Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834`, and Web `2496`. Android's source-build ID `4` also uses the Android catalog, as identified in [Telegram Android's BuildVars](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web defaults to A; an imported `K` app-version suffix or `macos` language pack selects K, and version `0.7.0` selects Webogram. Unknown application IDs keep Telethon's host defaults. Imported fields always win, including an older app version and an empty language pack. The catalog never changes the API ID/hash. Its version snapshot is reviewed explicitly, not fetched during login. A saved profile stays stable after updates.

`account.getAuthorizations` reports Telegram's saved authorization metadata; it is not an echo of each new `initConnection`. Compare it with the actual sent profile. Connecting an existing authorization does not validate its companion API hash: `initConnection` sends the API ID, while the hash is used by login requests.

After a new phone or QR authorization, TgWitness requests config, nearest DC, online status, languages (when the language pack is nonempty), app updates and terms-of-service updates, with 0.3–1.5 seconds between requests. Updating status briefly marks the account online. This sequence runs once at login completion, not on imports, reconnects or restarts. The authorization is saved first; a failed request stops the sequence without retrying or discarding the login. Results are recorded as `account.initialized`, with error names rather than response bodies. The sequence is not a guarantee against account restrictions.

For `tdesktop`, a missing `tz_offset` uses the server's local UTC offset, rounded to 900 seconds using the [opentele2 algorithm](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; license in `tgwitness/client_profiles.LICENSE`). It is refreshed on each connection so daylight-saving changes are reflected. An imported `tz_offset` takes precedence on every platform and is kept exactly, including zero. Other `initConnection.params` entries are retained. The HTTP sign-in form accepts the numeric timezone returned by file import; booleans, fractions and offsets outside the supported range are rejected.

Direct, SOCKS5 and HTTP CONNECT routes use Telethon's `ConnectionTcpObfuscated` (obfuscated abridged MTProto). HTTPS CONNECT retains TLS to the proxy and uses the same obfuscated transport inside the tunnel. MTProxy retains its required randomized intermediate transport and secret handling. Route switches apply the same choices. Obfuscation changes packet framing; it does not hide the account or its client metadata from Telegram or imply immunity to restrictions.

After connecting an authorized client, TgWitness checks config, nearest DC, the current authorization, the reviewed layer baseline, languages, app updates and terms-of-service updates. These diagnostics run once per client instance, before collection, and are shown under the connection details with their time. `account.connection_checked` records the result without session hashes, IPs, tokens or API hashes. They never accept terms or install updates. A request failure or FloodWait stops subsequent requests; a missing result stays unknown. Local checks can still report their results while network checks are skipped.

FloodWait diagnostics retain the failed TL method, any Takeout/range wrappers, the server-requested wait and the effective deadline in `telegram.backoff`. Connection details show the method and deadline while requests are paused. The diagnostic includes per-method client-call counters since that client was created; they count nested peer resolution separately, but do not count packets or Telethon's internal retry attempts. Current counters are also available as `collector.rpc_activity` in the status API. No request arguments, usernames, access hashes or exception text are included. The last diagnostic and full deadline survive restart. Earlier waits without a method record cannot be attributed retrospectively. See [export limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) for the source review and the distinction between discovery and history acquisition.

`official_app=True` or `False` is Telegram's current-authorization flag. Neither value establishes whether the account is restricted, trusted or under observation. The existing evidence-mode `account.devices` snapshots remain the history of all signed-in devices; connection diagnostics retain only the current device description.

Before connection, advisory checks compare the API platform, language pack, device/OS and app-version formats, mobile system locale, and Telethon's actual schema layer against the reviewed catalog baseline. Warnings appear in the server log and account status metadata; they never replace imported values or change the schema layer. A different layer is a compatibility review signal, not proof of a broken or restricted account. These checks and `official_app` do not certify that Telegram considers the account safe from restrictions. Disconnected account status uses the saved profile instead of generating another device description.

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

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- Files are converted **in memory** on your TgWitness server. Uploads are not stored, ZIPs are not extracted to disk and no external service is contacted.
- The resulting session is then checked with Telegram. If a file states a user ID, it must match the account Telegram reports.
- Files that describe different accounts or different API credentials are rejected instead of picking one.
- **Passcode or session text** holds the TData local passcode field, a box for pasting a StringSession and **Read files without signing in** (fills the form without contacting Telegram).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

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
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData is the `tdata` folder of the Telegram Desktop application (the cross-platform app from desktop.telegram.org).

| System | Default `tdata` location |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (portable Telegram: next to `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

To import it:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
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
| `string_session` (`session_string`, `session_str`; legacy `session`) | Telethon StringSession text, not a file name |
| `auth_key` (`auth_key_hex`) + `dc_id` | Complete 512-character Auth Key and DC 1–5 |
| `user_id` (`id`) | Optional; checked against Telegram before the authorization is saved |
| `device_model` (`device`) | Connection device description |
| `system_version` (`sdk`) | Connection OS version |
| `app_version` | Application version sent to Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Client language, system language and client language pack; an empty `lang_pack` is allowed |
| `tz_offset` | Optional UTC offset in seconds, sent in `initConnection.params`; integer or decimal integer string |

If both an alias and the main name are present, they must agree. Explicit Telethon session fields take priority over a generic `session` blob in another format. If both contain recognizable Telethon sessions, they must describe the same authorization. Without an explicit field, `session` must be a valid Telethon StringSession. Examples:

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

**Telegram traffic and HTTPS requests use different routes.** List downloads use a separate HTTPS connection and the supplied external-request route. `TGWITNESS_PROXY_FEED_PROXY` explicitly overrides that route with an HTTP/SOCKS5 proxy; both collector Compose variants forward it. The background pool follows the main workspace. No Telegram session, API credentials, panel token or bot token is sent to feed providers. Provider names, snapshot dates and the download route appear under **Where the list comes from**.

An MTProxy carries Telegram traffic only. Workspace HTTP operations such as timestamps, notifications, off-site copies and source checks use a separate SOCKS5/HTTP proxy when configured, then the account's SOCKS5/HTTP route. Without either, Hide the address refuses the request; the other modes permit Direct. External requests can be disabled. An explicitly configured feed-download proxy remains a separate operator override. The independent witness service keeps its own route.

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

## Local computer

Use `Start.cmd` on Windows or `sh start.sh` on Linux/macOS. `scripts\Setup.cmd` or `sh start.sh --setup-only` prepares the environment. The launcher installs dependencies on first use; later launches reuse the environment. Internet access is needed for setup and Telegram collection, but browsing existing records and creating exports work offline.

Run `python start.py --check` after setup to inspect local dependencies, Ed25519, storage, key configuration and the listening address without starting a collector. Use `--json` for structured output. Pass the intended `--data-dir`, `--host` and `--port`. The check does not install packages, create a journal or connect Telegram; it is not an integrity or coverage qualification. Startup separately verifies existing journals. `python start.py --help` also avoids installation.

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

The pinned Russian morphology dictionary and PDF color profiles are bundled for offline use. Packaging permits only their known file paths inside dependency `data` directories; unexpected files in those directories fail the build.

Extract the whole archive to a writable folder such as `Documents\TgWitness`; do not run it from inside the ZIP or from Program Files. The runtime uses an isolated module path, so other Python installations and `PYTHONPATH` do not affect it. Data stays in the package's `data` folder. To update, stop TgWitness, extract the new version to a new folder and copy the `data` folder across.

Build it yourself on 64-bit Windows with Python 3.12:

```
python tools/build_portable.py
```

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

Copy `deploy/env.example` to `.env`. Set `TGWITNESS_IMAGE` to the published version, using the **lowercase** repository path, for example:

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.9.1
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

The panel displays queued/failed media, oldest pending media, free disk, Telegram request pauses, and sources whose access is unconfirmed. These diagnostics are not a complete end-to-end delivery monitor. Workspaces share a process; a noisy account can still affect others. Separate worker processes, retention/rotation, durable update recovery and full deployment qualification remain. Scoped panel access is documented in [access and permissions](https://phishdestroy.github.io/TgWitness/docs/reference/access/); independent checkpoints are covered by the [witness guide](https://phishdestroy.github.io/TgWitness/docs/reference/witness/).

Detailed procedures: [connection/security](https://phishdestroy.github.io/TgWitness/docs/reference/connection/) and [operating modes](https://phishdestroy.github.io/TgWitness/docs/reference/operations/).


---

# High-assurance deployment

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/

A sealed 24/7 server on Hetzner or Phala Cloud, Gateway DNS and the checks a third party can repeat.

High-assurance deployment adds independent checks of the collection environment to archive verification. The reviewer queries deployment and access records held by the cloud provider and Cloudflare, and an Intel TDX deployment adds hardware attestation of the collector's environment.

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

The collector records SSH state, sessions, login history and boot information in signed process-start and `host.state` records. On an ordinary VM these are local inventory records, which the reviewer compares with the provider's independent records. The Intel TDX deployment below additionally verifies hardware-backed measurements.

## Providers

| `--provider` | Credentials | Verifier's read-only access | Provider log for the verifier | Kept for |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Read token of the same project | Server and firewall actions | While the resources exist |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Read-only personal access token | Droplet actions | While the Droplet exists |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` read-only scopes | Account events, firewall rule versions | 90 days |
| `vultr` | `VULTR_API_KEY` | User with read access and the `activity_logs` permission | Account activity log (method, path, actor) | 30 days, longer with an audit-log subscription |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | CloudTrail event history | 90 days |
| `phala` | `PHALA_CLOUD_API_KEY` | An API key of the same workspace | Application revisions and CVM operations: compose and environment changes, restarts, OS upgrades | While the application exists |
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
| `tdx_os` | MRTD and RTMR0-2 equal the values the verifier computes from the dstack OS image Dstack-TEE publishes, found by the OS image hash the CVM reports, and from the ACPI tables QEMU builds for the VM's shape: firmware, kernel, initrd, command line with the root file system hash, memory, vCPUs and devices. A development image fails |

The OS image (about 180 MB, of which 21 MB are kept) is downloaded once from [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases) into `dstack-images` beside the record; `--tdx-image FOLDER` uses another folder or an unpacked image, `--tdx-image none` skips the comparison. The measurement follows `dstack-mr` and the `qemu-acpi` crate of Dstack-TEE/dstack; `tools/check_dstack_image.py` checks it against QEMU's own ACPI output and against a real Phala Cloud quote, `--live` also against the published image. `--tdx-measurements` still compares MRTD and RTMR0-2 given as JSON instead.

Every start of the collector recorded in the journal carries such an attestation, so `verify --evidence` checks each start and the OS image it booted. Phala's application revisions and the CVM's operations serve as the provider log: a compose changed after the deployment fails the report, and restarts are listed for review.

In the panel choose **Confidential virtual machine · Phala Cloud** under **Extras** → **Server 24/7** and paste a Phala Cloud API key; the quick tunnel works as on Hetzner. From the command line:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` reads Intel's certificates and revocation lists from a file instead of downloading them from Intel. Gateway DNS is not available here: Phala has no provider firewall for outgoing traffic.

### Attestation certificate

For a Phala deployment `verify --report certificate.md` also writes the certificate: a self-contained `certificate.html` and an A4 `certificate.pdf` with the verdict, the chain of trust from Intel's root to the collector key, a comparison with ordinary and high-assurance servers, the measurements next to the values computed from the published image, who vouches for each part, the Intel certificate chain, every check, the provider log, and how to repeat the verification. The JSON report stays the authoritative record; the pages render it.

The report is sealed, in `certificate.seal.json` and the `.tsq`/`.tsr` files beside it:

| Seal | What it adds |
| --- | --- |
| Qualified electronic time stamp, `http://tsa.belgium.be/connect` | RFC 3161 time stamp over the exact bytes of `certificate.json` from the Belgian federal government's qualified trust service provider (FPS Policy and Support, BOSA). Its unit is listed as a qualified time-stamping service, status granted, on Belgium's EU trusted list; the root (Belgium Root CA6) and the list's entries, as of the list issued on 20 October 2026, are pinned in `tgwitness/tsa_roots.py`. Under Regulation (EU) No 910/2014, article 41, such a time stamp is presumed accurate as to date and time and as to the integrity of the data in every EU member state |
| RFC 3161 time stamp, FreeTSA | A second, independent time stamp |
| Verifier signature | Ed25519 over a statement naming the report's SHA-256 and every time stamp, with the verifier's own key (`--sign-with FOLDER`, default `~/.tgwitness/verifier`); the PDF carries a signature by the same key |

`--timestamp URL` (repeatable) chooses other authorities, `--timestamp none` none, `--sign-with
none` leaves the seal unsigned. `check-report` checks the report's hash, the verifier signature, each time stamp to a trusted root and its qualified status, and the PDF's signature. The legal weight of a qualified time stamp outside the EU, and of the report as a whole, is for the court or authority that receives it; the seal shows when the report existed and that it has not changed.

An attestation cannot rule out a flaw in Intel's TDX module or microcode, or physical access to the memory bus. Whoever controls the application in Phala's account can deploy another compose; it appears as a new revision with a new compose hash. The host controls the machine's time source and network.

Deploy, verify with `--evidence`, restarts, the OS image comparison, the sealed certificate and destroy have run on Phala Cloud itself; see [the 4 November 2026 run](https://phishdestroy.github.io/TgWitness/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026).

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

A verifier has no address key, and anyone who reads the topic can post to it. So the collector also posts the address itself, signed with its own Ed25519 key, and `verify` takes the newest post signed by the collector key in the deployment record; posts are ordered by the time ntfy.sh received them, not the time they claim. A collector from before this change signs nothing, and `verify` then takes the newest post and says so in the `statement` check; a forged post can only make that check fail, since the address must still answer with the collector's key.

What it costs: no Cloudflare account keeps records of a quick tunnel, so `verify` reports the tunnel, connector and DNS check as unavailable and the result is at best `incomplete` (on Phala Cloud the check passes instead: the connector runs inside the measured compose); the provider records, firewall, signed statement, host measurements and installer comparison are checked as usual. The byte comparison with the reference installer needs a deployed commit that already knows `--quick-tunnel`; a 0.7.0 checkout builds the domain installer and reports the difference. Cloudflare gives quick tunnels no uptime guarantee, allows 200 requests in flight and does not carry Server-Sent Events, so the panel's live updates (versions after 0.7.0) may not arrive through one and a view needs reloading; that part has not been tried. For a case that has to stand, use your own domain.

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

## Reading the deployment result

For an ordinary VM, the provider controls the host infrastructure, and local inventory is checked alongside provider records. For Intel TDX, the verifier additionally checks the hardware quote, collector binding, compose and OS measurements. Read the individual results to see which checks passed or were unavailable.

Historical firewall detail depends on the provider; Linode retains rule versions. The [validation record](https://phishdestroy.github.io/TgWitness/docs/reference/verification/) lists tested deployments and remaining live checks, and [verification scope](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope) connects these environment checks to archive acquisition and integrity.


---

# Panel guide

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/panel/

Every screen of the panel: chats, journal, sources, exports, Extras, protection modes and the code check.

[First setup and settings](https://phishdestroy.github.io/TgWitness/docs/reference/settings/) · [Accounts](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/) · [Export and verify](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/) · [Case reports](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/)

What each screen does, what it writes to the signed journal and where the detailed guide is. The panel shows one workspace at a time: one Telegram account with its own sources, journal and signing key. The selector at the top of the sidebar switches workspaces. The address carries the workspace (`?ws=…`); while the address, the selector and the loaded account disagree, actions stay blocked.

Use [Compare collection methods](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md) to choose between live observation, full history, fresh account/chat exports and saved-record handover. The Exports page includes the same comparison above its download controls.

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

For self-destructing photos and files, see [Self-destructing media](https://github.com/phishdestroy/TgWitness/blob/main/docs/EPHEMERAL-MEDIA.md). It explains the priority worker, saved and unavailable outcomes, and the limits of read-receipt blocking in the API collector.

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

  Chats already in the list when the mode is switched on are added without snapshots. A FloodWait pauses this work and it resumes afterwards; failures are recorded and live recording of the chat continues. This includes waits while resolving the new chat's identity: the pending profile/history task is retained for retry, and an existing longer account-wide wait is not shortened. - **Profiles on request.** **Chats → Profile → Save profile now** saves the current profile of any source; the newest one is shown above the messages. - **Chat state snapshots (preview).** State outside the message stream changes without a message: unpinning every message leaves no message-level trace, an administrator loses rights, a gift is hidden, converted, upgraded or refunded. While observing, every enabled source is read periodically and saved as a signed `chat.state` record: title, usernames, description, member and administrator counts, linked chat, slow mode, pinned message IDs (up to 100), administrators with their rights and titles, and gifts shown on channels and user profiles (up to 100). Each record lists the differences from the previous snapshot: changed fields with before and after, pinned messages added or removed, administrators and gifts added, changed or no longer listed. Telegram does not say who changed anything or when between snapshots. - A part Telegram refuses (for example the administrator list of a channel for a member who is not an administrator) is named in `errors`; its earlier value is kept and listed in `carried_forward`, never reported as removed. - A record whose only changes are counts, and a check that found no change, refer to the last full state with `state_seq` and cumulative `state_overrides`. A full state is written at least every seven days and whenever anything other than a count changes. - `parts_complete` marks capped lists. Additions require a complete earlier list, removals require a complete current list, and explicit empty values record clearing. - **Parameters → Chat state** sets the interval (12 hours by default, 0 turns snapshots off), the pause between sources, which parts are read, and whether checks that found no change are recorded. `FLOOD_WAIT` and `FLOOD_PREMIUM_WAIT` stop the remaining snapshot requests, preserve any longer account-wide deadline, and leave the interrupted chat eligible for another attempt after that wait. - **Not visible.** Inline (callback) buttons pressed in another Telegram app, the popup or link a bot answers such a press with, and invite links used in another app do not reach TgWitness. What the bot sends or edits afterwards is recorded.

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

A snapshot requests the latest visible messages from an enabled source, up to 500 per request. Results are labeled as history observations. Manual snapshots reserve an idle account; pause monitoring explicitly first. Repeated observations are kept as separate records.

Snapshots follow the attachment policy but remain separate from live-event switches. They do not reconstruct deleted messages or missed intermediate versions. You can request one while paused; any attachments it queues wait until observation starts and the download worker runs.

The **History** run is a separate exclusive task: it reads selected sources and downloads their queued attachments sequentially without starting monitoring. Pause releases the account; resume continues the saved run. For date, language and reply filters across several idle accounts, see [Distributed chat export](https://github.com/phishdestroy/TgWitness/blob/main/docs/DISTRIBUTED-EXPORT.md).

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

Retain fingerprints and checkpoints independently. See the [verification scope](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope) for acquisition checks in each mode, and [daily operations](https://phishdestroy.github.io/TgWitness/docs/reference/operations/) for routine collection.


---

# Load source history

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/history/

Load past messages from enabled sources, pause and resume, and verify a signed progress report.

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Pause, restart and partial results

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- The message observation, attachment job and cursor commit in one transaction. A resumed run does not repeat its already committed observations. Live capture or a separate, explicitly started run may independently observe the same message.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Inaccessible sources and sources disabled during acquisition remain visible as failed or skipped. Other sources continue; the overall result is incomplete.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

History completion describes history reads only. Attachments may remain pending, fail, or be excluded by the configured policy. Check media receipts in the journal and the attachment queue; only a completed receipt with preserved bytes constitutes a saved attachment. The history operation is an explicit snapshot request and is separate from switches that select categories of future live events.

## Transfer and verify

Save the **signed progress report**, then use **Export evidence** to download the journal and saved attachments. A later evidence export may include additional records; the report binds its counters to the journal prefix at the time it was created. Run the verifier from a trusted checkout of this version:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

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

Compare attachment hashes and their associated message references, and keep account timelines grouped by the Telegram IDs supplied in those records.

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
| A participant changes names across chats | Numeric sender ID → name/username history → replies → other observed chats → cited destinations/files | A Telegram-account activity timeline with links to its source records |

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
| Collector process | Start/stop, heartbeat, errors, settings, scope and signed run receipt | Local inventory; GitHub and TDX add [independent environment checks](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope) |

The interface names the account supplied in the source event and retains observed names and usernames. When the event omits its actor, the report leaves that field unspecified.

## Capacity and Telegram limits

There is no universal number of chats that can be monitored with guaranteed quality. Capacity depends on peak events per second, attachment volume and sizes, additional RPCs, active accounts, disk latency/free space, network conditions, Telegram limits, acceptable lag and queue depth.

Telegram distinguishes passive delivery from active short polling. Its update documentation describes additional `updates.getChannelDifference` calls for open channels/supergroups and recommends at most **ten simultaneously short-polled sources**. This is not a limit of ten selected groups or a completeness guarantee.

| Mode | Purpose | Status |
| --- | --- | --- |
| Standard observation | Record delivered updates from selected sources | Implemented |
| Priority rechecks | Starred sources use their own configurable interval and take precedence in each bounded recheck pass | Implemented with history and message queries |

The priority star controls these rechecks. Additional `updates.getChannelDifference` short polling is not exposed as a separate user mode.

Arbitrary high-frequency polling, ignoring FloodWait or assuming linear capacity from extra accounts is not a valid sizing model. Default limits are the first 1,000 listed dialogs, up to 500 messages per history snapshot, 1–2,000 MiB per collected file by type, and 4 GiB uncompressed signed ZIP content; each is changed per workspace under **Parameters**. Exports have no fixed event-count cap. Browser fallback is bounded to 128 MiB by default; the streaming CLI has a configurable transfer limit, 5 GiB by default.

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

Use **Journal** for local search without AI; [full-text search](https://phishdestroy.github.io/TgWitness/docs/reference/search/) (preview) matches word forms, phrases, domains and @usernames. For **Ask the archive**, first enable and configure a provider in **Integrations**. The workspace selector chooses the account; the form chooses chats and the observation period. Retrieval runs locally. An exact phrase or domain narrows retrieval; a message ID requests saved versions. Review the excerpts and open their journal records or context. There is no vector database or automatic Telegram action.

## Providers and consent

AI starts disabled in every workspace. Only the main administrator can configure the model, endpoint, encrypted API key, context/output limits, timeout and daily request budget. The key is never returned to the browser. Keep a blank key field to retain the current key, or explicitly remove it.

Ollama uses its documented [`/api/chat` endpoint](https://docs.ollama.com/api/chat) with non-streaming JSON output. Its default address is `http://127.0.0.1:11434` on the TgWitness server. The operator can change it using `TGWITNESS_AI_LOCAL_ENDPOINT`; this is not a model-controlled address. Install the selected model yourself. TgWitness does not download it automatically.

The compatible provider expects a base URL ending in `/v1` and the [Chat Completions protocol](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, JSON response mode, `max_completion_tokens`, and `choices[0].message.content`. Services lacking these fields are not supported. Connection testing sends synthetic text and counts toward the request budget.

Every request uses the workspace's configured outside route. A blocked route or Telegram-only MTProxy is an error; there is no direct retry. A deliberately configured local Ollama address permits a private destination. A loopback AI endpoint requires the workspace's Direct outside route; proxy routes are rejected before transmission. For other private services the existing server-level private destination opt-in applies. The preview shows the endpoint and outside route, including the proxy host when applicable. Changing that route requires a new preview.

Before generation, **Data sent to the model** shows the request: question, checked excerpts, event kinds, observation times and coverage markers. Telegram sessions, raw fields, provider keys, attachment bytes and the full journal are not part of that context. Uncheck unwanted sources, then explicitly approve processing. External providers may retain submitted content under their own policies. Local execution means the endpoint is local; it is not a guarantee about an independently configured service's behavior.

There are at most two concurrent provider requests globally and one per workspace. A preview expires after ten minutes and can generate one answer. The provider's reported token counts are shown; a cost estimate appears only when both input and output tariffs have been configured. Failed attempts also consume the daily request budget. No automatic retries spend additional budget.

## Sources and limits

Retrieval uses the [full-text index](https://phishdestroy.github.io/TgWitness/docs/reference/search/#ask-the-archive-and-mcp) when it is complete: the best matches across the selected chats, with word forms. Questions about recent changes or one message's versions, and searches while the index is building, use a bounded lexical search of the newest records. The preview names the method. Retrieval returns up to 24 sources; long texts are cut around their match. Truncated excerpts and incomplete result sets are marked. The period refers to **observation time**, not a claim that Telegram history is complete. Workspace-wide coverage events are withheld from chat-scoped access. Missing data is described as not found in the available archive.

The model receives no tools. Its source IDs are resolved against the selected records, hashes are rechecked, and quoted strings must occur in those records. Unknown IDs, changed quotes and uncited claims reject the answer. The application creates links; model-generated URLs are not used as citations. These checks establish source existence and quote accuracy, not the truth of an inference. Review inferences against the records before relying on them.

## Reports

Save a reviewed answer as a separate analytical report. It includes the model summary, observed chronology, extracted links and handles, edit/deletion records, coverage limits, and source event hashes. The provider, model, endpoint, time and prompt-template version accompany it. No identities are automatically merged.

Analyst revisions and notes are stored separately from the model summary. Reports live in encrypted derived files, with an index outside the signed event stream; the original events and media do not change. Only the owner or administrator can open a report, and source access is checked again. Download also requires export permission. Version 1 does not sign reports or imply that model conclusions are verified evidence. Limits: 100 reports per workspace and 100 analyst revisions per report.

For manual OCR and transcripts, see [media processing](https://phishdestroy.github.io/TgWitness/docs/reference/media-analysis/). For client access, see [MCP](https://phishdestroy.github.io/TgWitness/docs/reference/mcp/).


---

# Full-text search

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/search/

Find saved messages by word forms, exact phrases, domains and @usernames, best matches first, with the index bound to the signed journal.

[Archive analysis](https://phishdestroy.github.io/TgWitness/docs/reference/analysis/) · [Local OCR and transcription](https://phishdestroy.github.io/TgWitness/docs/reference/media-analysis/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Preview.** In **Journal**, choose **Best match · word forms** next to the search field. Results are ranked with BM25 and match other forms of the same word: *перевод* finds *переводом* and *переводы*, *transfer* finds *transfers*, a Chinese phrase is found without spaces. **Newest first · exact text** keeps the previous substring search over the whole record.

The index is derived data. It is rebuilt from the signed journal, is never signed itself and never enters an export. The original records do not change.

## Search syntax

| Write | Finds |
| --- | --- |
| `перевод карта` | Records containing both words, in any form |
| `"переводом на карту"` | The exact phrase, in this order |
| `бонус OR подарок` | Either word |
| `перевод -казино` | Records without the excluded word |
| `example.com` | The domain and its subdomains, also in hidden links and button URLs |
| `@username`, `t.me/username` | Mentions and links of the account, and messages it sent |
| `#tag` | The hashtag |
| `+79991234567`, a wallet address, an e-mail address | The same value in text or links |
| `from:@username`, `from:123456` | Messages from that sender |
| `chat:-1001234567890` | One chat; it can only narrow your own access |
| `id:42` | Saved versions of message 42 |
| `since:2026-01-01 until:2026-01-31` | Observation period; a date without a time covers the whole day |
| `kind:edited` | Only edits (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | Recognized text instead of, or with, messages |

Prepositions and other function words are ignored when other words are present. Look-alike letters mixed into a word (a Latin *a* inside a Cyrillic word), fullwidth and decorative Unicode letters and invisible characters are normalized.

## Languages

The language is detected per record from its script and letters:

| Script | Matching |
| --- | --- |
| Cyrillic | Russian and Ukrainian lemmas with [pymorphy3](https://github.com/no-plagiarism/pymorphy3). Without the optional Ukrainian dictionary a light Ukrainian stemmer is used |
| Latin | English Snowball stemmer; diacritics are ignored |
| Chinese, Japanese, Korean, Thai, Lao, Khmer, Myanmar | Overlapping character pairs: any phrase is found without spaces. Chinese queries are split into words with jieba |
| Other scripts | Exact words |

The Ukrainian dictionary (`pymorphy3-dicts-uk`) is distributed under GPL-3.0, so it is not installed by default. Install it with `pip install "tgwitness[uk-dictionary]"`; the index notices the new analyzer and rebuilds itself.

## Where the index lives

| Mode | Storage | Use |
| --- | --- | --- |
| On disk (default) | `search/fulltext.sqlite3` in the workspace directory | Large archives; survives restarts |
| In memory only | Nothing on disk; rebuilt at every start | No derived copy of message text on disk |
| Off | No index; **Newest first · exact text** remains | Minimal installations |

The main administrator chooses the mode under **Journal → Filters → Search index** for each workspace. `TGWITNESS_FULLTEXT=disk|memory|off` sets the default for workspaces without their own choice. Switching to memory or off deletes the file. The index file has the same protection as the journal: it sits in the private data directory. It is not encrypted, and is not part of backups or off-site copies.

New records are indexed in the background within seconds; a search also indexes a short backlog first, so a record saved a moment ago is found. An existing journal is indexed after the update without blocking the panel; until then, results cover the indexed records and the journal shows the progress. **Rebuild index** starts again from the first record.

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` needs the panel to be stopped (exit code 3 otherwise). With `--json`, standard output carries only the result; progress goes to standard error.

## Results and the signed journal

The index stores the sequence number and hash of the last journal record it covers and checks them against the journal when it opens. A replaced, restored or edited journal causes a rebuild. Every response reports this position, and every hit is read back from the signed journal by its sequence number: the index decides which records to show and in what order, never their content. Chat access is applied to the journal's own chat field, not to index content.

## Recognized text

OCR and transcripts stay in their encrypted artifacts. Their index exists only in memory and is rebuilt when a recognition job completes. A hit appears on its `media.saved` record, labelled as machine recognition with the engine, model and an excerpt; it is never presented as text sent in Telegram. The same index serves **Search recognized text**, which still also matches plain substrings.

## Access

Chat-scoped access finds only records from its chats, including recognized text of their attachments. `chat:` and other filters can only narrow that set. Index status shown to scoped access omits journal totals. Only the main administrator can change the mode or rebuild the index.

## Ask the archive and MCP

**Ask the archive** retrieves its sources from this index when it is complete: the best matches across the selected chats, with a saved text counted once. Up to 24 sources are sent; long texts are cut around their match and marked as truncated. Questions about recent changes, saved versions of one message, and searches while the index is still building use the previous chronological retrieval. The preview shows which method was used.

MCP clients can call `search_messages` with `ranked=true` and page with `next_offset`. Scoped connections receive only their chats.

Ranked pagination covers at most the first 1,000 results, regardless of page size. Narrow the query, chat or period to inspect further matches. Newest-first searches order messages, OCR and transcription results before selecting each page.

## Dependencies

| Package | Licence | Why |
| --- | --- | --- |
| pymorphy3, pymorphy3-dicts-ru, DAWG2-Python | MIT | Russian and Ukrainian lemmas; dictionaries are loaded locally |
| snowballstemmer | BSD-3-Clause | English stems, pure Python |
| jieba | MIT | Chinese query segmentation, pure Python (source distribution only) |
| pymorphy3-dicts-uk (optional) | GPL-3.0 | Full Ukrainian dictionary |

SQLite FTS5 with the `unicode61` tokenizer is required; it is part of the SQLite in current Python builds. Without it, best-match search reports that it is unavailable.

## Benchmark

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>` creates a deterministic signed journal of mixed Russian, Ukrainian, English, Chinese and Japanese messages with links and handles in 200 chats, builds the index and times typical searches (50 results, median of 7 runs).

Measured on Windows 11, Intel Core i9-13900K, 128 GB RAM, Python 3.12.10, SQLite 3.49.1, data on an exFAT drive, analyzer `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| Measure | Result |
| --- | --- |
| Signed journal | 1,000,000 messages, 1.50 GiB, written in 19 minutes |
| Index build from the journal | 71 s, about 14,141 messages per second |
| Index file | 58 MiB, 3.8% of the journal |
| Search right after a new record | 8 ms median, 9 ms p95 |
| Previous substring search, same journal | `перевод` 3.2 s, `银行转账` 2.6 s, `verify-account.example` 2.6 s |

| Search | Matching records | Best match, median | p95 | Newest first, median |
| --- | --- | --- | --- | --- |
| Common word, word forms: `перевод` | 134,403 | 82 ms | 85 ms | 7 ms |
| Two words: `оплата карта` | 28,996 | 43 ms | 43 ms | 14 ms |
| Rare word: `розыгрыш подарок` | 28,881 | 42 ms | 47 ms | 13 ms |
| Exact phrase: `"переказ коштів на картку"` | not counted | 35 ms | 36 ms | 6 ms |
| Domain with subdomains: `verify-account.example` | 12,435 | 17 ms | 17 ms | 3 ms |
| @username: `@support_desk_bot` | 10,331 | 15 ms | 16 ms | 3 ms |
| Chinese without spaces: `银行转账` | 17,691 | 23 ms | 24 ms | 3 ms |
| Japanese: `リンク` | 16,603 | 23 ms | 25 ms | 3 ms |
| English stem: `withdrawal` | 27,775 | 26 ms | 26 ms | 2 ms |
| OR and exclusion: `бонус OR подарок -казино` | 268,034 | 190 ms | 193 ms | 19 ms |
| Chat filter: `chat:-1000000000007 перевод` | 652 | 9 ms | 9 ms | 6 ms |
| Period filter: `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 ms | 156 ms | 81 ms |

An exact phrase is checked literally on candidates in rank order until the page is full, so its total is not counted. Times grow with the number of matching records; narrowing the chat or period makes broad searches faster. The synthetic corpus repeats a small vocabulary, so common words match far more records than in real chats.


---

# Read-only MCP

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/mcp/

Connect an MCP client to selected workspaces and chats with expiring, revocable access.

Connect an analyst client to selected workspaces and chats. TgWitness serves **Streamable HTTP at `/mcp` in the panel process**. Each connection has its own token, expiry and permitted tools. MCP cannot send Telegram messages, change settings or modify the signed journal. The same connections work with the [command line](https://phishdestroy.github.io/TgWitness/docs/reference/cli/).

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
| `search_messages` | Saved message text within the selected period; `ranked=true` uses [full-text search](https://phishdestroy.github.io/TgWitness/docs/reference/search/) (word forms, best matches first, `next_offset` paging) |
| `get_message_versions` | Captured versions and deletion observations |
| `get_message_context` | Nearby captured message IDs |
| `get_journal_event` | One sanitized record with its source reference |
| `get_capture_status` | Collection state, permitted coverage records and `gap_summary`: message numbers never observed, per channel or supergroup and for the account-wide sequence ([details](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#missing-message-numbers-gap_summary)); choose a chat to see its listed gaps |
| `get_activity_stats` | Messages by UTC hour and weekday, peak days, edit and deletion shares, senders, domains and `@handles`, with coverage ([details](https://phishdestroy.github.io/TgWitness/docs/reference/cli/#activity-statistics)) |
| `get_messages_by_date` | Saved messages of one calendar day in a named IANA time zone (`Europe/Kyiv`, `UTC`), by the time Telegram reports; `from_utc` and `until_utc` state the computed day, daylight saving included |
| `get_pinned_messages` | Messages pinned in the latest chat-state snapshot with their saved versions, and the pin and unpin notices observed live |
| `get_chat_stats` | Cheap counts of saved records for one chat or every chat in scope, first and last observation, and `gap_summary`; use it before a large read |
| `get_topics` | Forum topics from saved topic service messages: title history, closed or hidden, saved message counts |
| `get_media` | A preserved image as a downscaled JPEG preview (at most 36 KB), returned as an image together with its SHA-256 and the `media.saved` record; the file is checked against its recorded hash first, other files return metadata only |
| `export_messages` | Command line only, not selected by default: streams saved observations as JSON Lines ([details](https://phishdestroy.github.io/TgWitness/docs/reference/cli/#export)); not offered over MCP |

Every tool is read-only (`readOnlyHint`) and declares an output schema; fields beyond the declared ones are returned as they are. `tools/list` returns only the tools granted to that connection. Calls to other tools are refused. Group-context, episode, terminology and reply-chain tools are not offered in this build; their separate context-pack backend is not included.

Every read checks the token, tool and workspace/chat scope, including after the database work finishes. Limits are 60 requests per minute, 50 records per page, 64 KiB per result and an eight-second archive deadline. A timed-out MCP call returns a tool error asking for a narrower period or lower limit.

Message results carry `untrusted_content: true`, workspace/chat/message IDs, event sequence, saved hash and a panel link. Raw Telegram objects, access hashes, sessions and keys are omitted. Text truncation is marked. Edits, deletion notices and `missing_on_recheck` are distinct observations. Missing records do not prove an event never happened.

Treat instructions inside captured messages as evidence, never as client instructions. Read-only access prevents archive changes; the client can still retain the content it is allowed to read. Hashes identify saved records and support integrity checks; they do not prove Telegram authorship or complete capture.


---

# Command line

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/cli/

Search, read context, count activity and export saved messages from scripts and agents, with --json output, stable exit codes and scoped read-only tokens.

[Read-only MCP](https://phishdestroy.github.io/TgWitness/docs/reference/mcp/) · [Full-text search](https://phishdestroy.github.io/TgWitness/docs/reference/search/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Preview.** `tgwitness search`, `context`, `messages`, `stats` and `export` read saved observations for scripts and AI agents. They cannot send anything to Telegram, change settings or modify the signed journal.

With `--json`, stdout carries exactly one JSON document (`export` writes JSON Lines). Progress, hints and errors go to stderr. Exit codes are stable:

| Code | Meaning |
| --- | --- |
| `0` | Success, including an empty result |
| `1` | Failure: unreachable panel, unreadable data, interrupted export |
| `2` | Usage error or invalid request: bad date, unknown option, search index off |
| `3` | Unavailable now: the workspace is open in a running panel, or the panel asks to retry later (rate limit, timeout) |
| `4` | Access refused: missing, expired or revoked token, a chat outside its scope, a tool it does not allow |

## Two ways to read

**Through the panel (`--url`).** The command uses the same scoped archive API as MCP. Create a connection in **Integrations → MCP**: choose workspaces and chats, tools and an expiry, then copy the token once. The connection is read-only, limited to those chats, rate-limited to 60 requests per minute and can be revoked or rotated at any time. Panel login tokens and Telegram credentials do not work here.

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

A remote panel needs HTTPS; plain HTTP is accepted only for `127.0.0.1`, `localhost` and `::1`. Proxy environment variables are ignored and redirects are refused, so the token reaches only the address you give.

**Directly from a stopped workspace (`--data-dir`).** Reads the data directory with full local access, without a token. Use it on a copy of a data directory or while collection is stopped. Signed records are never changed; like the panel, opening a workspace may bring its derived indexes up to date. When the panel has the workspace open, the command exits with code `3`; read through the panel instead. Without `--data-dir`, `TGWITNESS_DATA`, `./data/live` or the data directory of the installation running the command is used.

`--workspace ID` selects a workspace (default `default`). `tgwitness messages
--workspaces` lists the ones you can read.

## Commands

| Command | Result |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | Best matches first, with word forms, exact phrases in quotes, domains and `@username` ([syntax](https://phishdestroy.github.io/TgWitness/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | Exact text, newest first, without the index |
| `tgwitness context CHAT_ID MESSAGE_ID` | Saved messages within ten message IDs on either side |
| `tgwitness messages` | Chats you can read |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | Saved messages of the chat, newest first |
| `tgwitness messages CHAT_ID --message ID` | Every saved version and deletion record of one message |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | Activity statistics, below |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | Saved observations as JSON Lines in journal order |

Dates are `2026-10-01` (UTC midnight) or ISO times with a timezone, `2026-10-01T09:00+03:00`. For `search`, `messages` and `export` they select observation time. Pages hold up to 50 records: follow `next_offset` (`--offset`) for ranked search and `next_before` (`--before`) elsewhere.

Ranked search stops at 1,000 results. The final page may be shorter than `--limit`; narrow the query, chat or period when more matching observations exist.

Every message result carries `untrusted_content: true`, the workspace, chat and message IDs, the journal sequence, the saved record hash and a panel link. Edits, deletion notices and `missing_on_recheck` are separate records. Absence of a record does not prove that an event never happened.

### Activity statistics

`stats` counts saved observations for one chat, one sender, or every chat in scope:

- messages by UTC hour and by weekday (Monday first), busiest hours and days;
- edited, deleted and `missing_on_recheck` shares;
- senders with message counts and first and last message times;
- the most frequent domains and `@handles`, counted once per message across its saved versions;
- coverage: `coverage.gap` records and, for access to the whole workspace, periods without a connected collector heartbeat (`collector_liveness`).

The period selects **message time reported by Telegram**. Hour and weekday counts can help estimate a sender's time zone; they do not establish it. Figures are computed on request from the journal and are not stored. Each result names the journal head it covers when your access spans the workspace. Reading stops after five seconds through the panel, or `--timeout` seconds locally (default 30); then `complete` is false and `partial` names the first record that was not read. Only the most recent records are counted in that case.

### Export

`export` writes one JSON object per saved observation (new messages, snapshots, edits, recovered messages, deletion notices, `missing_on_recheck` and saved media records) in journal order. Each line has the same fields as other results, with the full text. With `--output`, the file is written under a `.partial` name and renamed only after the panel's completion record; an interrupted export leaves no file and exits with code `1`. `--output` never overwrites an existing file. With `--output` and `--json`, stdout carries a summary: record count, last journal sequence and, for whole-workspace access, the journal head.

An export through the panel needs a connection that allows **Export messages (command line only)**; it is not selected by default. This file is a working copy, not evidence: for a verifiable handover use the signed export in **Exports**, which `python -m tgwitness.verify` checks.

The panel rechecks access before emitting each record, including the completion record. Revoked or expired access leaves an incomplete export. Lazy page reads share the archive worker limit with other queries and have a bounded wait.

## Agent skill

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) tells an agent how to use these commands, how to cite records and how to treat captured text. Agents that read `.agents/skills` load it from a repository checkout. For Claude Code, copy the `tgwitness-cli` folder to `.claude/skills/` in your project or `~/.claude/skills/`.

## MCP and the command line

Both use the same connections, scope checks and limits. MCP results are limited to one 64 KiB page, so MCP offers no bulk export; the command line streams it. `get_activity_stats` is available to both.


---

# Local OCR and transcription

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/media-analysis/

Recognize captured images and audio with a local worker; keep derived text linked to its source file.

[Workflow guide](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Open a `media.saved` journal record, choose **Recognize attachment**, then select OCR or transcription under **Ask the archive**. Processing is manual and local. There is no cloud media mode or automatic upload. Original attachment bytes and `media_sha256` remain unchanged; recognized text is explicitly marked as machine recognition and stored separately with the source hash, engine/model version, language, parameters and completion time. Transcripts retain returned timestamps.

Search these results using **Search recognized text** and the OCR/transcript filter, or choose recognized text as the source of a **Journal** best-match search. Both match word forms through an [in-memory index](https://phishdestroy.github.io/TgWitness/docs/reference/search/#recognized-text). This is a separate derived-data search; it does not silently turn machine recognition into original Telegram text or add it to signed events.

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

**Jurisdiction guidance.** Under Document details, open **Jurisdiction guidance · optional** to choose a jurisdiction and civil/commercial or criminal procedure. The appendix carries the legal basis, source links, preparation notes and research status. Local-language summaries and explanations of collection safeguards are optional. No jurisdiction is selected by default. These choices belong to the workspace, and are excluded from saved layout configurations and implicit sharing-copy defaults. See [defaults, supported reports and research limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/JURISDICTION_GUIDANCE.md).

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

### Anomaly indicators

**Preview.** Evidence reports add an **Anomaly indicators** section computed by registered processors (`tgwitness/metrics/`, one file per metric). The report names every processor that ran with its version, and prints its method under its table, so the computation can be repeated from `events.jsonl` with `tgwitness.metrics.run`.

| Processor | What it shows |
| --- | --- |
| `first_time_posters_over_time` v1 | First-time posters and messages per UTC day. A flag requires at least five first-time posters and three times their median, with message volume at most 1.5 times its median. The baseline uses at least seven observed days within the previous 14 calendar days, after seven days of warm-up. |
| `service_vs_message_ratio` v1 | Distinct saved message numbers per chat and the share used by service messages. It describes a numbering; it does not explain a particular missing number. |
| `join_leave_per_month` v1 | Joins, departures and removals or bans per month, one per person, chat, change and day. |
| `pinned_per_month` v1 | Pin service messages, unpin notices, and pinned messages added or removed between chat-state snapshots, per month. |

**Parameters → Report metrics** selects processors and the number of displayed rows, including in filtered reports. Daily and monthly tables show recent rows, service-share tables rank chats by saved message count. Totals cover every row.

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

See [verification scope](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope) for the checks of acquisition, archive integrity, time and collection coverage in each mode.

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

An account export reserves its account exclusively. Pause monitoring or another acquisition explicitly before starting or resuming; the app never stops it automatically.

As the installation administrator, choose **Start here → Export my account**, or **Exports → Telegram account → Configure account export**. Sign in if needed, review the scope, and explicitly start the export. Continuous observation is not required. **Saved observations** is a separate export of the existing journal; its ZIP includes all sources regardless of journal filters. Every workspace has its own jobs, signing identity and storage. Issued panel access, including an unrestricted ordinary export grant, cannot open these account-wide routes.

Sender and text filters expand under **Filter by sender or message text**. **Account data & connection method** contains optional account categories and the Takeout/regular-session choice; its summary shows the active choices even when closed. Closing these sections keeps their settings. Export and report drafts remain in the current panel session while changing views; they are not saved through a browser reload. Existing jobs remain reachable from either export choice.

This workflow exports data currently accessible to the connected account. The default uses [Telegram Takeout](https://core.telegram.org/api/takeout); it is not a backup of unavailable or deleted Telegram data. Secret Chats, inaccessible history and earlier edits are not recovered. Telegram can impose a waiting period before Takeout starts. The panel displays that wait; it does not silently switch transport. The explicit regular-API option has different coverage and records unsupported categories.

Takeout is the official export API also used by Telegram Desktop. TgWitness can write Desktop-compatible JSON directly from its own acquisition; importing someone else's archive is not required. Chat and message IDs are available through both transports. A public chat or permission to forward does not guarantee a faster export or remove Takeout's approval delay. Measure the same scope and media settings before comparing speed.

For up to 20 explicitly selected chat IDs, regular-API export resolves those peers directly before considering the account's complete dialog inventory. A readable public channel can therefore be exported without joining it, even when it is absent from the dialog list. Uncached peers fall back to the ordinary inventory. The archive filter remains enforced: if Telegram does not return a dialog and archived chats are excluded, the unknown archive status is recorded as an omission. Takeout keeps its split-range inventory procedure. Neither path joins chats or changes forwarding permissions. In Desktop-compatible JSON, channels that Telegram marks `left` appear under `left_chats`, including readable public channels the account has not joined.

Both `FLOOD_WAIT` and `FLOOD_PREMIUM_WAIT` pause requests for the full server-requested period. The account's deadline is persisted across reconnects and restarts; a shorter later wait cannot shorten it. Retries are bounded, cancellation preserves sealed pages, and API credentials are not rotated to bypass a rate limit. No Premium purchase is made.

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

Photo payloads use the still-image variant identified in their metadata and hash manifests, including photos with an animated avatar variant. That animation is not substituted for the selected still image. A shorter or longer payload than the observed size is recorded as a failed attachment, and a changed representation during file-reference renewal is rejected. These failures leave the archive partial while retaining the message records. Independent verification also rejects saved attachments whose signed length contradicts their observed size or representation, including in older archives.

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

### Messages left out by the selection

**Preview.** A disclosure does not look complete when it is not. Inside every chat that keeps at least one disclosed message, messages the selection left out appear as markers, `[withheld by selection — rule: sender]` (or `text`, `period`). Choose **Messages left out by the selection**: one marker for each run of consecutive withheld messages (default) or one for each message. Markers carry only the rule and a count, never text, sender, date or files. Chats with nothing disclosed are left out entirely, so the package does not reveal that they exist.

Disclosed replies say what they answer: a message included in this copy, a message withheld by the selection, or a message that is not in the source export (deleted before the export or never exported; the export cannot tell which). A withheld message that a disclosed reply answers always gets its own marker, so the reply points at a record that explains why it is empty. These three states are distinct from deletions and collection gaps, which belong to the source export.

In `messages.jsonl` (format `tgwitness-account-disclosure-v2`) each message has `state`: `disclosed`, or `withheld` with `rules` and `count`. A disclosed reply has `reply_to` with the target `id` and `state` (`disclosed`, `withheld`, `not_in_source`). The manifest counts disclosed messages, chats, media and `withheld` messages. `verify.py` rejects a marker that carries content and a reply that points at a record missing from the package; version 1 packages verify as before.

The minimized format omits structured account profiles, contacts, avatars, sessions, stories, raw Telegram objects, forwarding headers, reply quotations, contact cards and location metadata. It excludes the original JSONL files, private filter settings, pseudonym key and identity map. Selected text, explicitly retained identities and included files can still contain the same names, IDs or phrases used in those filters; they need separate review. The private policy and pseudonym key are retained encrypted in the local vault for the job; deleting the job clears its associated private disclosure records. The public policy records filter counts rather than filter values. The stated purpose is public in the manifest and HTML: explicit private criteria and, in pseudonymized modes, known hidden identities are masked there too, including when message text is omitted. Keep the purpose free of unnecessary personal details; unknown identifying context can remain.

Its manifest binds the derivative files, public policy and original ZIP's hash. Verification can establish integrity and, if the source is supplied locally, matching source linkage:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Source linkage does not independently prove that the transformation selected every required item or removed every identifying detail. Original plaintext is not embedded as a proof. A fresh review is needed for that judgment.

## Sharing and hosted capture

Select the messages and files the recipient needs, review the complete sharing copy, and retain the source separately. Record the delivered ZIP's hash so the recipient can identify and verify that exact copy. Pseudonymization replaces the selected identifiers; included text and original files remain part of the review.

GitHub Actions supports full-account and selected-chat exports through Takeout or the regular API, plus a one-chat event journal. The [hosted capture guide](https://phishdestroy.github.io/TgWitness/docs/capture/) explains settings verification and the 120-minute limit. To verify a sharing copy derived from hosted capture, check its source hash against the original archive and verify that archive's attestation with the [mode-specific checks](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope).

[Evidence format](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/) · [Case reports](https://phishdestroy.github.io/TgWitness/docs/reference/case-reports/)


---

# Evidence format

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/evidence/

Contents of the signed ZIP, record kinds, process receipts, people profiles, off-site copies and offline verification.

TgWitness preserves account-visible Telegram observations in a signed journal. Recipients can verify the saved records, attachments and reports against a trusted collector key, then compare the journal with an independently retained checkpoint. This page describes the formats, the checks and the material to keep for handover.

Recipients can start with **VERIFY.cmd** on Windows: it asks for the original ZIP and independently obtained key fingerprint, displays an explained result, and saves a separate verification transcript. See [verification launchers and the portable runtime](https://github.com/phishdestroy/TgWitness/blob/main/docs/VERIFICATION_LAUNCHER.md) for setup and trust limits.

## What is signed

| Material | Protection | What to retain |
| --- | --- | --- |
| Every journal observation, including operational events | SHA-256 chain and an Ed25519 signature per event | Original `events.jsonl`, the trusted key fingerprint, and a retained checkpoint |
| Evidence ZIP contents | `manifest.sig` signs the canonical manifest, which lists hashes of the content files | The complete ZIP, including its manifest and signature |
| Preserved attachments | SHA-256 and byte count in a signed `media.saved` event; file hash in the signed ZIP manifest | The original bytes inside the verified ZIP |
| Checkpoint | Ed25519 signature over journal length, head hash, public key, and creation time | An independent copy retained before a disputed change |
| Run receipt | Signed record of the collector version, source-file hashes and start settings, also included in `process.started` | The receipt, associated journal and the environment evidence for the selected verification mode |
| Readable reports: `report.html` and its parts, `report.json`, `report.pdf`, `chat.pdf` | An Ed25519 seal per file over its content; the PDF also carries a standard PDF signature (see [Readable reports](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#readable-reports)) | The file as received and the trusted key fingerprint; the ZIP it describes |
| Standalone CSV | No standalone cryptographic signature; event hashes alone are insufficient | Use the exact copy inside the verified ZIP for integrity checking |
| Screenshots, printouts, or PDF produced by a browser | No TgWitness signature on the derivative | Keep the original verified package and document how the derivative was made |

The collector verifies journal signatures before generating every export format. Readable HTML and PDF reports carry their own seals; standalone CSV is checked as part of a signed ZIP. Keep the ZIP to retain the attachment bytes and manifest, and a separate checkpoint to check the journal against an earlier boundary.

## Comparing chat exports

Verify and compare two signed chat-export ZIPs with independently retained signer fingerprints:

```
python -m tgwitness.verify first.zip --compare second.zip \
  --fingerprint FIRST_TRUSTED_KEY_SHA256 --compare-fingerprint SECOND_TRUSTED_KEY_SHA256
```

When both archives record the same numeric account and chat IDs, records are paired by message ID. **Unchanged** means equality of the complete saved JSON record: full text, author, dates, reply target, nested metadata and unknown fields are all included. JSON object key order does not matter; absent fields, nulls, value types and array order do. The 300-character preview is only for display. Changed entries name the differing top-level `changed_fields`, including changes invisible in that preview. Duplicate message IDs are rejected instead of overwriting one another during matching.

A difference can be a changed display name, view count, collection annotation or other observation metadata. It does not by itself establish a Telegram edit, identify who made a change, or prove which contradictory archive is accurate. Unparsed records remain in the comparison; equality of their saved representation does not mean their Telegram payload was decoded.

For different or missing account/chat identities, the tool only finds possible correspondences using sender, complete text, file hash, media type and a five-second time tolerance. It reports **Matched**, not **Unchanged**. These candidates do not establish message identity or equality of all metadata. Unparsed records remain unmatched. Differences in paired records remain listed in `changed`, including in content mode; these differences do not prove edits of the same message. With `--json`, `matched` counts pairs and `unchanged` counts pairs whose complete saved records are equal. Neither count proves message identity in content mode. The existing `changed_fields` and integer `unchanged` output remain compatible with earlier comparison results. Archive format and signature verification are unchanged.

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

## Handover extract

A signed ZIP carries the whole workspace journal. When a court, a lawyer or an abuse desk needs only some chats, a period or certain people, **Exports → Handover extract** prepares a minimised copy (`tgwitness-handover-v1`) according to the selected disclosure rules. The operator states the purpose and chooses the chats, an optional period (UTC), the people the extract is about, what happens to everyone else (shown, replaced by pseudonyms P01, P02… or left out), which message texts stay, which attachments and profile photos are included, and whether phone numbers and e-mail addresses in texts are masked. The purpose and these rules are in the signed manifest and in the report; the journal records `handover.exported` with the access that prepared it and the file's SHA-256, not the contents.

`verify.py` checks an extract in two ways. A record shown unchanged is verified in full: its content against its hash, its Ed25519 signature and its link to an included predecessor. A minimised record keeps the original hash and signature, so the signature still verifies, but the withheld fields cannot be recomputed from it; the record names what was withheld and the report marks it. The manifest names the journal length and head with the collector's signature over that head, and counts the records left out; `coverage.json` describes the chosen chats. Names inside file names are not detected. Review the final files before sharing: free text, file names and selected attachments can still identify people. Keep the full signed ZIP: the extract is a disclosure, not a replacement.

## Readable reports

Signed evidence, handover and chat ZIPs carry readable HTML and JSON reports, plus PDF when the required fonts are available, in the selected report language. Each report is sealed with the workspace's Ed25519 key and can be verified separately: `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]`.

- `report.html` / `chat.html`: the seal statement (`tgwitness-report-seal-v1`) closes the file and signs the SHA-256 of every byte before it. Long journals and chats are split into parts of a configurable size (Report settings, 500 to 100,000 records; 5,000 by default): `records/records-0001.html` or `messages/messages-0001.html`, each sealed with its number, range and the total, and listed with its SHA-256 in the signed manifest. Runs of collector heartbeats are shown as one line unless Report settings list them one by one.
- `report.json` (`tgwitness-report-json-v1`, keys `format`, `report`, `seal`): the seal signs the SHA-256 of the canonical JSON of `report`, so the facts can be read by case systems and scripts and a selection for data protection can be made from them while the signed file stays whole.
- `report.pdf` / `chat.pdf`: a formal document for printing and filing, signed twice over the same bytes, the whole file except the signature value (`/ByteRange`). The standard PDF signature (`adbe.pkcs7.detached`, CMS with SHA-256 and ECDSA P-256) uses a self-issued document-signing certificate kept in the workspace vault; its subject serial number is the Ed25519 key fingerprint. The Ed25519 seal travels inside the CMS as the unsigned attribute `2.25.240684792623320047764573196045913242332` and names the certificate's SHA-256 with `"content": "pdf-byte-range"`, so the Ed25519 key vouches for the certificate. A PDF reader shows whether the file changed after signing and calls the signer unknown until the certificate is trusted; compare the Ed25519 fingerprint instead. Chinese, Japanese and Korean PDFs need a font on the server (or in `TGWITNESS_FONT_DIR`); without one the ZIP carries the HTML and JSON reports only.

In a channel or supergroup Telegram numbers messages 1, 2, 3… in order. A chat export lists the first and last number, how many are present and every run of absent numbers in `message-ids.json`, the manifest and the `chat.json` header, and marks each gap where it falls in the transcript. `verify.py` recounts them from `chat.json`. An absent number is a message Telegram did not return (deleted before the export, or not visible to the account); in private chats and basic groups numbers are shared by all of the account's chats and gaps are not counted.

After reading the history, the export asks Telegram for every absent number again, by number (`channels.getMessages`, up to 10,000 numbers). The result is in `message-ids.json` and the report. An empty answer records that the number is unavailable to this account at recheck time; it leaves the cause unspecified. A message returned on recheck is added to the export and marked `found_on_recheck`.

Every report opens with **In brief**: one paragraph, then what the material shows and what it does not (who is behind an account, completeness of delivery, deletions before observation, clock time without a timestamp). The page's own seal stamp turns amber when the browser has checked the seal's signature, not the page: a browser does not give a page its own bytes. It turns green only when the reader drops the file into the check at the end of the page and every byte matches, and only if the page shown is that file; otherwise it turns red.

Each report names the program exactly: the git commit when the collector runs from a checkout or the installer sets `TGWITNESS_COMMIT`, and the SHA-256 of its source files (`source_tree_sha256`, the canonical JSON of path → SHA-256 of every `.py`, `.js`, `.css`, `.html` and `.svg` file in the package), which a checkout of that commit reproduces unless files were changed. The Telegram client is named with its library, API layer and data centre. When observation starts and when a chat export begins and ends, the collector asks Telegram for its time (`updates.getState`, whole seconds) and records Telegram's time minus the collector's clock, with the uncertainty from the round trip; the reports show these measurements under Chain of custody. A chat export also records when it read the history, apart from the dates of the messages.

### Offline report viewer and archive guide

Extract the complete ZIP before opening `chat.html` or `report.html`. The viewer provides search, filters, participants, indicators, record details and JSON/CSV selections without a server. Keep `viewer/` and `media/` next to the report. Selections are derivatives: use `verify.py SELECTION.json
--evidence ARCHIVE.zip` to compare them with the signed archive. The verifier checks the report ID, signing key, archive boundary and every selected item; edited, missing and duplicate items fail. Selection notes and creation time remain unsigned metadata.

Message-number gaps are shown only for a complete, unfiltered ascending chat feed. Hiding a category or failing to load a data chunk must not turn an omitted row into evidence of a missing message. Search highlights operate on plain text before HTML escaping, preserving literal markup.

The browser checks manifest signatures, the report ID and key, and all listed file hashes. It rejects ambiguous or malformed ZIP structures, duplicate names and unsafe paths, and caps files at 256 MiB and declared total contents at 4 GiB. Use the standalone verifier for larger archives. This browser check complements the verifier's checks of journal chains and data semantics.

`README.txt` contains a start guide, an aligned file inventory, verification instructions and data format notes in the report language, followed by a complete English guide. `SHA256SUMS` covers the files listed within it, excluding itself, `manifest.json` and `manifest.sig`; the signed manifest also covers `SHA256SUMS`. Keep the original ZIP unchanged and save working files outside the extracted folder. PDF reports include section bookmarks and case/report identification on later pages.

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

An unscoped notice does not establish that a message was never saved: a matching chat may be outside the current observation scope, or a unique match may be unavailable. Recheck absence remains a separate observation from a deletion notification in report counts, filters and labels. A later recovery clears the current missing state while preserving the earlier unsuccessful check in the signed history; neither observation establishes a deletion notice.

Multiple IDs resolved to the same chat from one notification are grouped as `deletion.batch`, regardless of their count. The notification does not establish that the entire history was cleared, who performed the deletion, or whether it applied to all participants. Saved outgoing messages do not change these limits. Older journals may contain `history.cleared` events inferred from batches of ten or more IDs, with explanatory text attributing the deletion to the other participant. Those inferences are not supported by the update. Preserve those original signed records, but treat them as grouped deletion notifications; the current interface labels them accordingly.

## Coverage: continuity, gaps and unobserved IDs

Every signed ZIP carries `coverage.json`, the HTML report opens with the same summary, and `verify.py` recomputes it from `events.jsonl` instead of trusting the file:

- **Continuously observed from X to Y.** A period starts with `observation.started` and ends at a pause, a stop, a lost Telegram connection, a sign-out, a process start without an orderly stop, or more than three minutes without any record while observing (heartbeats are written every minute, so silence means the process stopped, froze or the computer slept). When the heartbeat interval is changed in **Parameters**, each heartbeat records it and the allowed silence becomes three intervals, never less than three minutes.
- **Gaps** list the time between periods with the reason. A gap still open at the last record is marked `not_resumed_by_last_record`.
- **Message IDs not observed.** For channels and supergroups, which number messages per chat, the IDs missing between observed ones are listed as ranges. They are reported as *not observed* — deleted, never delivered, or outside the saved history — never as deleted. Private chats and ordinary groups share an account-wide sequence, so gaps inside one such chat mean nothing and are not listed there.
- Chat-level gap notices (for example Telegram asking for difference recovery in one channel) are counted as notes; they do not interrupt global coverage.

### Missing message numbers (`gap_summary`)

**Preview.** `coverage.json` → `gap_summary` measures the numbers Telegram assigned and this collector never saw. Telegram numbers messages once per channel or supergroup, and once per account across private chats, bots and ordinary groups. A number between two observed messages is either observed or missing; a contiguous range is a positive statement that every message numbered in it was observed. A gap names no actor and no reason.

| Field | Meaning |
| --- | --- |
| `status` | `on`, or `off` when turned off in **Parameters → Gap analysis** |
| `parameters` | The parameters that produced the result, so it can be repeated |
| `chats[]` | One entry per channel or supergroup, each numbered on its own |
| `account` | The account-wide sequence of private chats, bots and ordinary groups |
| `status` (per sequence) | `applicable`, or `not_applicable` with `reason` |
| `observed_from`, `observed_to`, `span` | First and last observed number and the size of the range |
| `observed`, `observed_without_content` | Observed numbers; those known only from a deletion or recheck record |
| `missing`, `density`, `gap_ranges`, `largest_gap` | Numbers never observed, their share of the range, how many runs, the longest run |
| `clusters[]` | Listed gaps: `low`, `high`, `missing`, and the neighbouring observed numbers `after` / `before` with their observation times |
| `service_estimate` | Only when enabled: how many missing numbers would be service messages at their observed share. Never subtracted from `missing` |

Validity is derived from the journal, never assumed:

- **Channels and supergroups** are measured per chat, also in an export of chosen chats. Records chosen by sender make the measurement `not_applicable`.
- **The account-wide sequence** is measured only from the first to the last message that arrived while whole-account collection was on and kept private chats, bots, ordinary groups and the account's own messages, with no such chat excluded (`scope.changed`). Numbers named by `deletion.unscoped` count as observed without content. An export or handover of chosen chats cannot measure it. If whole-account collection was switched off and on, a note says that numbers used meanwhile appear as gaps.
- Service messages are journal records with their own numbers, so they close their gaps themselves; the optional estimate is only context.

`verify.py` recomputes `gap_summary` from `events.jsonl` with the parameters in the signed `coverage.json` member (defaults for older archives) and prints the account-wide line in its coverage summary. The archive's `get_capture_status` (MCP and the command line) returns the same measurement for the chats an access may read; the account-wide sequence only to access covering the whole workspace.

Repeated observations of one service message count once, and the account service estimate uses only numbers inside the measured range. An applied scope must explicitly preserve the account's own messages before account-wide measurement is enabled; older records without that information cannot establish this condition. Stopped observation does not extend the measured range, and resuming it is noted. The live archive query has a time budget, including its database scan, and marks an unfinished measurement as partial.

Telegram documents the [separate message ID sequences](https://core.telegram.org/api/updates#message-id-sequences). These numbers describe observations; they do not identify a deletion actor or establish why a number is absent.

When Telegram stops accepting the account, the `coverage.gap` record that ends observation carries `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended` or `not_authorized`) and the Telegram error; `verify.py` names the cause where the period ends.

Coverage combines recorded observation periods, interruptions and message outcomes. Assess it together with the selected chats, period and attachment policy; continuous operation alone does not establish complete delivery of Telegram updates.

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

Run verification from your installed TgWitness version or a reviewed checkout. The copy included in an archive supports portable use; check that copy against your trusted installation before executing it.

A checkpoint signs a statement containing the public key, journal length, head hash, and creation time. The verifier can check that a later archive contains the same prefix. Retain the checkpoint outside the collector, so later verification compares the archive with a reference held separately from it.

## Verification scope

Verification checks the archive and the collection mode used to produce it. Choose the mode whose trust boundary matches the case, then retain its verification inputs.

| Collection mode | What the verifier checks | Verification inputs and trust boundary |
| --- | --- | --- |
| Local workspace | Record signatures, hash chain, manifest and attachment bytes | Independently retained collector fingerprint; the host administrator controls the local signing key |
| Local workspace with an independent witness | The archive checks plus agreement with an earlier journal prefix retained by the witness | Separately trusted witness key and records; the checkpoint binds the prefix already observed |
| [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) | GitHub attestation of the archive digest, approved workflow and collector commits, hosted runner, fresh session/key origin and internal archive integrity | Trusted verifier policy, caller repository and GitHub attestation bundle; collection runs under the pinned workflow |
| [Cloud deployment](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/) | Provider lifecycle and access records, firewall and Cloudflare state, plus the collector's signed run record | Read-only queries to the provider and Cloudflare; availability of individual checks depends on the provider |
| [Intel TDX confidential VM](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx) | Quote signature and platform status, binding to the collector statement, compose and OS measurements | Intel trust chain and expected deployment measurements; retain the results of every required TDX check |

In sealed acquisition, the approved collector receives data through an authenticated Telegram connection inside the verified environment. Attestation binds the archive to that execution, so verification covers acquisition as well as later file integrity. This relies on the approved code and the platform trust chain listed above. GitHub capture verification requires a session created inside the run and rejects imported-session captures.

The run receipt records the collector version, file hashes and startup settings. GitHub provenance and TDX measurements provide the environment checks; the [validation record](https://phishdestroy.github.io/TgWitness/docs/reference/verification/) identifies tested configurations.

TgWitness signs the observations it collects; Telegram and message authors do not issue these signatures. In a local workspace, material created before the first independent checkpoint still depends on the collector and its key holder. Coverage records describe the selected scope and collection outcomes, while verified external timestamps anchor the committed archive or journal boundary in time.

## Attachments

Files are addressed by SHA-256 under media/. A media.saved event links a hash and byte length to a specific message event. Raw filenames are metadata, never local paths. Media bytes are downloaded asynchronously, so immediate deletion may prevent capture. Disabled collection, oversize/unknown-size files, download failures, and interrupted downloads are visible as outcomes. A process crash can leave unreferenced partial files; they are not included in exports.

The ZIP exporter verifies stored media against their names. JSONL, CSV, and HTML exports verify event signatures but do not carry media bytes. Derivative reports are conveniences; events.jsonl is the authoritative event representation.

A full chat export saves attachments within the workspace's attachment settings into media/, named by SHA-256. Each message record in chat.json names its file (`file`, `file_sha256`) or the reason it is absent (`file_status`), together with what the reader saw around the text: links behind the text, forward origin, bot buttons, signature, views and the auto-delete timer. `verify.py` checks that every named file is in the signed manifest under that hash.

## Durable collection and process receipts (0.2)

A media job and its message event commit in one transaction. The job stores the original TL message descriptor; the signed observation binds its SHA-256, account, and size policy. Recovery verifies that binding before downloading. It never fetches the current message and silently substitutes a newer attachment. Interrupted jobs are retried, while permanent failure remains an explicit outcome.

Each workspace has its own journal and signing identity. A process.started event includes a run ID, local clocks, dependency versions, source-file hashes, initial account/scope, and capture settings. Heartbeats include the run ID, monotonic time, and queue state. The run receipt can also be downloaded as a separately signed statement. For verification of the execution environment, pair it with the GitHub attestation or TDX checks described in [Verification scope](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope).

Automatic checkpoints are retained locally on startup, every five minutes while observing (**Parameters → Signed checkpoint every**), and on orderly stop. Startup verification and export compare the journal against the latest retained local checkpoint. This can detect a database rollback when the checkpoint survives. Independent retention keeps that reference available outside the workspace; a verified external timestamp additionally anchors it in time.

After a restart the saved Telegram update position is resumed (`catch_up_from` in `observation.started`) and missed updates are requested. A periodic recheck records `message.recovered` for missed messages and `message.missing_on_recheck` when Telegram no longer returns a saved message; the latter is not a deletion notice and names no deleter or time.

### Off-site copy and restore (S3)

The off-site copy (Exports, off by default) uploads journal segments, preserved files, checkpoints with their timestamps and finished chat exports to S3-compatible storage, encrypted with AES-256-GCM before upload under a key kept in the workspace vault; Object Lock retention applies when the bucket supports it. Without the downloaded key the copy cannot be read. Restore and verify with `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Restore requires an empty ordinary directory. Downloads and decrypted objects stay in private temporary storage until the entire journal and every retained checkpoint verify. Unsafe object paths, inconsistent segment ranges and journals shorter than a checkpoint are rejected; failed verification publishes no restored files. Retention checks compare the returned Object Lock mode and date with the deadline sent at upload (one second of rounding tolerance). An expired, invalid or shortened deadline does not count as verified. The status reports the sampled object whose retention was read back for that upload pass.

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

**Cloudflare Gateway log** (`cloudflare.gateway_dns`). For a server that resolves through Cloudflare Gateway ([Gateway DNS](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)), each pass copies what Gateway logged since the previous copy: one record per window of at most three hours with `from`, `until`, the `location_id`, the server's `address` when one is set, and the `queries` as `[at, name, type, rcode, decision, colo]`, also when there were none. Set it under **Cloudflare Gateway log**: account, location, optional address and a read-only token (Account Analytics Read; Zero Trust PII Read to keep one address of a shared location). The panel checks them with one request before saving; the token stays encrypted and never enters the journal. `verify.py` lists the windows, the names looked up most and any time no copy covers; a record whose count does not match its queries fails. A window that holds more than one page of queries in a single second keeps that page and says the rest is missing. The copy is Cloudflare's answer through the collector, signed by the collector; within 24 hours anyone with a read-only token can compare it with Cloudflare.


---

# Independent witness

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/witness/

Run a witness with its own key and bot, publish signed checkpoints to a channel and check exports against it.

[Export and verify](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/) · [High assurance](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/) · [Panel guide](https://phishdestroy.github.io/TgWitness/docs/reference/panel/#extras)

A witness retains signed checkpoints separately from the collector. It checks the collector's signature and journal continuity, signs the result with its own key, and publishes it to a Telegram channel. Run it on a separate server with read-only access to the collector's witness endpoint.

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
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen), a nondecreasing count and an unchanged head at an unchanged count. Merkle inclusion and consistency proofs verify that a growing journal extends the retained checkpoint. Once continuity proofs have been used, removing them is rejected;
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

Keep the witness journal and its pinned key separately. Online checks verify continuity between checkpoints; offline verification compares every retained checkpoint with the export. Legacy heads without continuity proofs retain the offline comparison and are reported without online continuity verification. The report lists witness downtime and failed publications by interval.

### Daily seals and unavailable timestamp calendars

The witness seals the previous UTC day's journal boundary and submits the hash of that signed seal to OpenTimestamps. A calendar submission is pending evidence; only independently checked Bitcoin commitments receive confirmation in the verifier.

If all calendars fail, the signed seal and unsuccessful attempt remain in the journal. The hourly maintenance pass retries that original record, including after a restart or a change of date. It scans at most 32 seals, submits at most two missing submissions and spends at most 60 seconds on retries per pass. A persistent cursor rotates through older seals. Retained submissions follow the existing proof-upgrade path.

A retry does not rewrite the seal, change its original date or claim that the calendar received it earlier. A later Bitcoin commitment remains a later external confirmation. Missing proofs remain `none`; pending proofs remain `pending` until the verifier checks them independently.


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

## When the disk is filling up

Attachment downloads already pause below **Parameters → Attachments → free disk space** (1 GiB by default), keeping their queue. Text observations continue. This does not depend on notification settings. Disabling notifications does not disable the download reserve or storage safeguards.

For earlier intervention, enable **Run automatically**, choose **Remove the local file to free space**, and enable **Start an extra offload pass when disk space is low**. The optional rule starts below 5120 MiB free and continues in batches until 10240 MiB is free by default. Both thresholds are configurable. It uses the same destination, minimum file age, batch limit, full readback verification and evidence backup prerequisites as a manual pass. It never enables a destination on its own. Checks run every 30 seconds; an error or no progress delays another pressure pass for five minutes. The pressure state and retry time survive a restart. Scheduled passes still use their normal interval when the pressure rule is inactive.

The panel shows free space, the packing reserve, whether the pressure rule is armed, and files skipped for lack of temporary space. Packing and restoration check their peak temporary-space requirement before starting and check available space while writing. The reserve is the configured download reserve, with a 64 MiB minimum for storage operations. These checks are not a filesystem quota; another process can still consume space between checks.

Gzip compression is lossless and applies to remote objects; it does not shrink the active journal or create local archives. JPEG/video/ZIP files may barely shrink or grow slightly. The current packing pipeline may temporarily need approximately twice the attachment size plus the reserve when compression is enabled. Choose a start threshold early enough for your largest files. A file too large to prepare is kept and reported; smaller files and previously verified remote copies can still free space. A verified copy can be offloaded without another local packing file. Restoration also needs temporary space and can be refused until space is available.

If nothing eligible can be moved, or no destination is configured, TgWitness cannot reclaim space automatically. The signed journal is never pruned or rewritten by storage management. It still needs space for new text observations.

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

This page describes access, storage and network protection in a local or server workspace. For collection on a GitHub runner or in an Intel TDX confidential VM, see the [verification modes](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope), which add checks of the collection environment. Account connections, notifications, timestamps, off-site copies and witnesses have their own routing settings.

| Area | In short |
| --- | --- |
| Access | Administrator key plus scoped access to accounts/chats, seven permissions and revocable sessions; localhost by default |
| Secrets at rest | Session, API pair, signing key and proxy settings are encrypted with Fernet |
| Messages and media | Stored unencrypted: use disk encryption and strict permissions |
| Integrity | SHA-256 hash chain and an Ed25519 signature on every record |
| Local trust boundary | The host administrator controls the workspace and its signing key; independent checkpoints retain an earlier journal boundary |

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

Telegram API credentials, the session and signing key are encrypted with Fernet. For local messages and media, encryption is provided by the host's disk or volume; the workspace stores ordinary files. Exports can use a password-protected AES-256 ZIP, and off-site copies use AES-256-GCM.

The vault key defaults to the protected data directory. Use an external master-key file below to store it separately. On Unix, new private-key files use mode 0600 and new data directories use 0700; on Windows, set the directory ACL for the service account and authorized administrators. Existing directory permissions are retained.

### External master key

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode. Disk encryption protects the local message and media files in either mode; see [connection and data protection](https://phishdestroy.github.io/TgWitness/docs/reference/connection/) for setup details.

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

Local verification checks record signatures, the hash chain, attachments and the export manifest. The administrator holds the local signing key and can create another signed journal; an independently retained checkpoint detects replacement of the prefix it covers. Keep the key fingerprint and checkpoints with the recipient or an independent witness.

For independently checked collection, choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Their verifiers check workflow provenance or hardware measurements in addition to archive integrity. Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies; the [evidence format](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope) describes the checks for each mode.

## If you suspect a problem

Preserve the original data directory and use a separate copy for analysis. Report the affected version, operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), keeping account data and credentials private.


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
| distributed_export.py / distributed_pages.py | Concurrent chat jobs, per-account reservations, signed checkpoints and cleanup after archive verification |
| distributed_takeout.py / export_timing.py | Resumable Takeout sessions and timings for each start or resume |
| store.py | WAL transactions, ordered event chain, query filters, operational settings |
| fulltext.py | Derived full-text index (word forms, BM25), bound to the signed journal head; never exported |
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

API authorization is a bearer token. Login operations are serialized and time-bounded. Account uploads use a dedicated 12 MiB encoded-body limit and an 8 MiB decoded-file limit; normal API requests retain the 16 KiB limit. Conversion runs in a worker thread, keeps uploads in memory, and returns normalized input to the authenticated browser. QR login has a per-workspace candidate, short-lived identifier, waiter task, and explicit cancellation. Only accepted authorization becomes the active client. Telegram FloodWait is returned with a Retry-After value; credentials and raw RPC error messages are not exposed in API errors. Journal exports run outside the async event loop and are serialized per workspace. They stream a stable read snapshot alongside continuing WAL writes. Chat acquisition jobs can run concurrently on separate accounts; each account remains reserved until its job stops. A paused or failed job retains its checkpoints. Successful archive verification permits cleanup of its working files, leaving the ZIP, signed plan and status. Workspace collectors share the process/event loop.

Current history snapshots and live updates can overlap. Both are separate observations, labeled by source; duplicates are not silently collapsed. No inference from missing IDs, fabricated deleted text, forced member enumeration, or automatic group joining is implemented.

For the operator-facing explanation, see [how collection works](https://phishdestroy.github.io/TgWitness/docs/reference/collection/) and [accounts and session formats](https://phishdestroy.github.io/TgWitness/docs/reference/accounts/).

Network configuration lives in the encrypted vault. Applying a route closes old clients and cancels unfinished login; later connections use that route with no direct fallback. A new external-key installation derives each workspace's Fernet key with HKDF-SHA256 from a master key file and a stored random salt. This protects secrets separately from the data directory, not plaintext journal/media contents.

Local demo entry uses a separately generated process capability, never the configured panel token. Issuance and acceptance require explicit demo mode, a synthetic root without additional workspaces or an authorized session, loopback peer/Host, no proxy forwarding headers, and no cross-origin browser request. Live APIs retain bearer authentication and reject collection changes in demo mode.


---

# What has been tested

Canonical page: https://phishdestroy.github.io/TgWitness/docs/reference/verification/

The live Telegram test, automated checks, browser checks and what remains unverified.

Each result below applies to its recorded revision and environment. The [current capability matrix](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) separates implementation, published downloads and remaining qualification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Live Phala Cloud deployment · 4 November 2026

`--provider phala --quick-tunnel` ran against real **Phala Cloud** (`tdx.small`, region US-WEST-1) with a Phala Cloud API key of an empty workspace, real ntfy.sh, GitHub and Intel PCS. The CVM installed commit `df7d860c` (v0.8.1); deploy, verify and destroy ran from the command line with the fixes below. Seven CVMs cost about 1.9 US cents together.

The first two deployments found five differences from the simulated Phala Cloud. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) now reproduces each, and fails without its fix:

| On Phala Cloud | Before the fix | Fix |
| --- | --- | --- |
| `compose_file.name` is required | HTTP 422, nothing created | The compose carries the CVM name |
| Unless given an empty one, Phala adds its own pre-launch script to the measured app-compose (v0.0.20: Docker login, `docker compose pull`, root password, SSH keys from `user_config`) | `tdx_compose` fails: code outside the published compose | The app-compose sets `pre_launch_script` to `""`; Phala then leaves it out |
| Without `image` Phala picks `dstack-dev-0.5.12`, the development build, with SSH access enabled | `server_state` fails. The quote alone passed on this image; only the provider record and `tdx_os` show it | The deployment asks for the production build of Phala's current release, `dstack-0.5.12` |
| With the dstack gateway off, the CVM details never get an `instance_id` | Deploy waits 30 minutes and fails | The instance ID is read from the CVM state |
| Restarts, stops and starts are CVM operations, not application revisions | `provider_actions` did not list restarts | The operations are read as well |

The third deployment:

- The CVM ran `dstack-0.5.12` with SSH access off. The collector posted its signed address about 1.5 minutes after creation. Deploy then passed `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, quote v4, FMSPC `20a06f000000`, not in debug mode, not migratable, collateral fetched from Intel), `tdx_compose_hash`, `tdx_compose` (byte for byte) and `tdx_identity` (KMS keys).
- The panel at its trycloudflare.com address answered 401 without a token or with a wrong one, and 200 with the panel token.
- `verify` with `--source` set to GitHub's archive of the commit and the fingerprint passed separately: server, `server_state`, firewall (no gateway, no public endpoint), provider log, statement, fingerprint, source hash, boot and the five `tdx_*` checks passed. Cloudflare and `tdx_os` were unavailable, so the result was INCOMPLETE.
- Two restarts through Phala's API: each time the CVM was back in under two minutes with the same collector key, a new signed address, and the old one answering 530. `verify` reported the new boot and both restarts as REVIEW. With `--evidence` it confirmed the journal signatures and three starts, each with its own Intel TDX quote from the same CVM.
- `destroy` removed only that CVM. The workspace was then empty, and the panel address stopped answering.
- The panel wizard's price check read `tdx.small` at $0.058 an hour. A wrong key got a plain "did not accept the API key" message.

Two further findings, fixed afterwards:

- Without the address key, `verify` followed the newest well-formed post on the address topic, which is printed in the published compose. One forged post sent it to a host that does not exist, and `statement` failed: a forger could not pass as the collector, but could block third-party verification, for up to 12 hours with a forged future timestamp. The collector now also posts its address signed with its own key, `verify` accepts only such posts when the collector makes them, and posts are ordered by ntfy.sh's receive time. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) replays the forged posts. A CVM runs this only from a commit that contains it, so this run's collector did not sign its address yet and `verify` said so.
- `tdx_os` could not run without `dstack-mr`, whose current version has `measure-os` rather than the `measure --json` the documentation named. The verifier now computes MRTD and RTMR0-2 itself from the published image and the VM's shape, ACPI tables included.

The fourth deployment, with these:

- Deploy downloaded the published `dstack-0.5.12` once, matched it to the OS image hash the CVM reported, and `tdx_os` passed: MRTD, RTMR0, RTMR1 and RTMR2 equal the values computed for QEMU 8.2.2, 1 vCPU and 2 GiB. The same computation gave a different RTMR0 for a claimed 4 GiB, 2 vCPUs, QEMU 9.2.1 or a second network card, and failed for a changed kernel, firmware or command line and for the development image.
- `verify` passed every one of its 16 checks, the quick tunnel's connector included, so the result was PASS. It wrote the HTML and PDF certificate, sealed with a qualified eIDAS time stamp from the Belgian government's time-stamping unit TSU 202301 (status granted on Belgium's trusted list), a FreeTSA time stamp and the verifier's signature; `check-report` confirmed all of them and the PDF's signature.
- After a restart, `verify --evidence` confirmed two starts, each quoted inside the CVM and each booted from the published `dstack-0.5.12`; the restart and the new boot were REVIEW.
- `destroy` left the workspace empty.

The fifth deployment ran the collector from commit `53a0f7e9`, which has all of the above:

- The collector posted its address signed with its own key, next to the operator's HMAC post. Two forged posts were then added to the topic, one with a zeroed HMAC and one signed by another Ed25519 key, both claiming a time in the year 2096. `verify` took the address signed by the collector key and passed all 16 checks; the seal again carried the qualified Belgian time stamp, FreeTSA's and the verifier's signature, and `check-report` confirmed them.
- After a restart the collector posted the new address signed: `verify` found it at once, the operator's **Find the current address** 27 seconds later from the HMAC post, and both ignored the forged posts. `verify --evidence` confirmed two starts booted from `dstack-0.5.12`.
- Deploy printed what Phala bills the CVM, disk included: $0.06078 an hour.

The panel wizard ran against Phala Cloud twice, once through its job API and once through the browser with a real Chromium: the price check, creation with the commit under **Advanced**, all six attestation checks passed, the server list showing the billed price (44.37 USD a month), **Find the current address**, the measured compose download, and deletion. The browser saw no page errors. Each time the workspace was empty afterwards.

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation.

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

## Full-text search on one million messages · 5 November 2026

Command: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

A deterministic signed journal of 1,000,000 synthetic messages in 200 chats (Russian word forms, Ukrainian, English, Chinese, Japanese, links and handles) was indexed in 71 seconds; the index took 58 MiB beside a 1.50 GiB journal. Best-match searches took 9 to 190 ms (median), against 2.4 to 3.2 seconds for the previous substring search. Full results, hardware and limits: [Full-text search](https://phishdestroy.github.io/TgWitness/docs/reference/search/#benchmark). `tools/test_fulltext.py` also verifies a signed archive made before full-text search (`tools/fixtures/evidence-before-fulltext.zip`) with the current verifier, and a current archive with that archive's own `verify.py`.

## Remaining qualification

The retained live journal establishes real collection, edits, deletion notices, attachments, rechecks and rate-limit handling. It does not establish exhaustive delivery or a controlled matrix of role visibility, reaction actors, prolonged FloodWait, account bans and network/process interruption recovery. QR-token issuance remains distinct from completed mobile QR confirmation.

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

Local detailed receipts and screenshots are under test-results/ (Git-ignored). The public screenshot in docs/assets/ contains only fictional demonstration data.


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

- Remove the unused one-shot exporter and check recovery against the current exporter. Reject unexpected or repeated message IDs in recheck responses.
- Combine concurrent exports with resumable Standard API and Takeout acquisition. Each job retains its own progress, timings and signed checkpoints; accounts remain reserved until that job stops. Include the account controls, batch import and report-verification updates in the same build.
- Add offline `VERIFY.cmd` / `VERIFY.sh` launchers, plain-language verification explanations and saved UTF-8 transcripts to signed exports in all 25 panel languages. Build a separate Windows verifier with an embedded runtime and a language menu. Unpinned signers remain unconfirmed; successful integrity verification does not establish admissibility.
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
- Preserve available self-destructing photos, videos and files in the API journal with a dedicated immediate queue, explicit TTL/view-once labels and signed saved/unavailable/not-saved outcomes. Block read receipts in the API client, including batches and wrapped requests. Keep byte limits, disk reserves and Telegram backoff; saved bytes do not establish human viewing.
- Preserve image-rendered Unicode emoji in official Web message text, reply previews, reactions and derived page text without changing the client DOM. A live account test exposed the omission; video and saved pages already retained the image.
- Improve chat-export Takeout, unreadable-message recovery, shared absent-number rechecks and bounded range retries. Preserve observed deletions in export scope, compare verified archives, and distinguish archive integrity from an independently confirmed signer.
- Protect imported sessions from remote logout, close idle connections and prevent simultaneous reuse of a session key. Add explicit session management and masked two-step password entry; cancellation or switching workspaces prevents submission. Read single-account export messages before their separate attachment stage.
- Keep source export and AI actions disabled while local source search is pending, empty or has failed; clear stale previews before the next search. Exercise delayed replies explicitly in browser checks.
- Use unambiguous synthetic privacy identifiers and report the exact marker/context on handover-test failures, avoiding accidental matches inside report metadata.
- Add an in-panel comparison of collection methods and explain account task ownership beside full-history controls. Refresh source-version badges, qualification records and Trusted Live network results; check version labels before publication.
- Add [full-text search](https://phishdestroy.github.io/TgWitness/docs/reference/search/) (preview): Russian and Ukrainian word forms, English stems, Chinese and Japanese phrases without spaces, exact phrases, domains in hidden links and buttons, @usernames, wallets and phones, filters for chat, sender, message ID and observation period, ranked with BM25. The index is derived from the signed journal, bound to its latest record hash, never exported, and can be kept on disk, in memory only or turned off. Recognized text is indexed in memory only and labelled as machine recognition.
- Ask the archive retrieves the best matches from the full-text index when it is complete, keeps the 24-source limit, and cuts long texts around their match. MCP `search_messages` accepts `ranked=true`.
- Add `tgwitness index status|rebuild` with JSON output on stdout and stable exit codes.
- Fix ranked search paging: `next_offset` is now returned when more matches exist, through `/api/search`, MCP `search_messages` and Ask the archive's partial marker. Paging stops at the first 1,000 results.
- Fix Ask the archive failing on questions longer than 24 words or 200 characters. The full-text query keeps the question's first distinct words; a query the index cannot read falls back to exact-text retrieval.
- Centre excerpts on the match in long texts that hide zero-width characters between letters.
- Build the website when a language lacks new translations: untranslated blocks stay in English with the page notice and are listed by the build.
- Add the [command line](https://phishdestroy.github.io/TgWitness/docs/reference/cli/) (preview): `tgwitness search`, `context`, `messages`, `stats` and `export` with `--json` and stable exit codes, reading a stopped workspace directly or a running panel through a scoped, revocable archive connection. Add `.agents/skills/tgwitness-cli/SKILL.md` for agents.
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
- Bind official recordings to independently saved source/settings, check video segment order and clean endings, record fresh drand rounds and support independent public-relay comparison. Report unfinished procedures, unconfirmed logout and the limits of local or Cloudflare assurance explicitly. See [Official client witness](https://github.com/phishdestroy/TgWitness/blob/main/docs/OFFICIAL-WITNESS.md) for scope and validation.
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
- Keep the current tunnel address when an older signed address post is replayed. Signed posts are ordered by their signed time; unsigned posts use the relay's receive time.
- Trust only the Caddy proxy on the private Docker HTTPS network and normalize client addresses for authentication limits.
- Keep operator IP addresses out of new signed access events, hide administrative payloads from shared views, and enforce workspace and export ownership boundaries.
- Reject duplicate JSON keys, prepended ZIP content and HTML injected into report seals; distinguish pinned witness keys from pinned collector keys.

## 0.9.0 preview · 4 November 2026

- Reserve each account exclusively for monitoring, history or an export. Serialize Telegram RPCs and persist full FloodWait deadlines.
- Add durable distributed chat exports with date/language/reply filters, bounded labelled context, signed chunks and explicit pause/resume. See [Distributed chat export](https://github.com/phishdestroy/TgWitness/blob/main/docs/DISTRIBUTED-EXPORT.md).
- Keep account reservations until every export worker has stopped, including repeated pause requests and sibling worker failures. History loading in sealed sessions also reserves the account exclusively.
- Add participant timelines from saved observations: names, membership, explicit deletion flags and message activity. Profile refreshes are bounded; optional presence recording preserves unavailable or expired status as unknown and does not attribute online activity to a chat.
- Save, import and reuse report layout profiles without copying case details or report filters. Profiles are validated and isolated by workspace.
- Automatically offload eligible attachments to configured external storage under disk pressure, with reserve-space checks, compression, optional encryption and full readback verification before local eviction. Journals remain local.
- Make the recording settings and chat tabs fit narrow screens, including wider system fonts, and fix profile controls and localized labels.
- Include reviewed website assets in source archives and verify conditional dependency versions in SBOM inventories.
- Phala Cloud deployments work on Phala Cloud itself (first real run, 4 November 2026): the compose carries its name, Phala's own pre-launch script is kept out of the measured app-compose, the production OS image is chosen instead of Phala's development default, the instance ID is read from the CVM state, and restarts from the CVM's operations count in `provider_actions`. `tools/check_phala.py` simulates each of these.
- `tdx_os` without outside tools: the verifier downloads the published dstack OS image once, matches it to the hash the CVM reports and computes MRTD and RTMR0-2 itself, the ACPI tables QEMU builds for the VM's shape included. A development image, other firmware, kernel, command line, memory, vCPUs or devices fail. Each journal start is checked the same way.
- Attestation certificate for Phala deployments: `verify --report` also writes HTML and a signed PDF, sealed by a qualified eIDAS time stamp from the Belgian government's time-stamping authority, a FreeTSA time stamp and the verifier's own key; `check-report` checks the seal.
- Quick tunnel addresses are also posted signed with the collector key, so a verifier is not misled by forged posts on the address topic; on Phala Cloud the tunnel check passes, since its connector runs inside the measured compose.

## 0.8.1 preview · 2 November 2026

- Runtime, sealed and media containers moved to pinned Wolfi/glibc with Python 3.12 and hash-locked system packages (AMD64 + ARM64). Image scans are clean of HIGH/CRITICAL.
- Tesseract 5.5.4 built from verified source, English and Russian data pinned.
- Release checks now cover real OCR, offline transcription, signed multilingual PDFs and container restrictions. The source archive includes all container build inputs.
- **Extras → Independent capture** in the English panel: browser/AyuGram recorders with encrypted tokens, pinned keys, tab selection, start/pause, snapshots, checkpoints and verified ZIP downloads. Everything is off by default.
- New optional `tgwitness-capture` package: Chromium PNG/MHTML snapshots, AyuGram SQLite copies, optional silent video, Ed25519 event chains, signed ZIP/HTML reports and a standalone verifier. Each recorder has its own key and storage.
- Fixed Phala installs: source bundles were missing the capture package.

## 0.8.0 preview · 2 November 2026

**Reports**

- Report studio: eight designs (Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, Ledger & margin), live preview, HTML and native signed PDF. Switching designs keeps filters, charts and notes.
- Pick report data by chat, author, date and event type and preview it before saving. Edits show before/after, deletions show what was saved earlier.
- Reports look like proper dossiers now: cover, key figures, evidence map, numbered findings, timeline. PDFs get an A4 cover with QR, bookmarks and page refs.
- Each report explains what its conclusions rest on: export-time checks, observations, missing material, how to check it independently (EN/RU/DE wording).
- Send, edit and observed times are shown separately, plus replies, threads and metadata.

**Case Board and groups**

- Private Case Board: signed bookmarks, exact-version highlights, action slices, collections, threaded comments and statuses. Team notes stay apart from observations; the verifier checks board exports too. Export permission alone doesn't reveal team notes.
- Account groups share settings. Members follow the group, an account's own value wins until reset. Changes show which accounts they hit and ask before overwriting. Access can be granted to a whole group.
- Group screen at `/groups/<id>`: accounts, problems, shared chats, group export.

**Setup and connection**

- Six-step first setup and one Settings page with simple/standard/expert levels, in all 25 languages. Each step has its own URL, Back works.
- The setup asks whether the account is a separate one; a main account only records chosen chats. After Start it shows that connection, events, sources and files work.
- Guided Connection screen: pick accounts, prepare and check a route, then apply. Direct, own proxies, public MTProto pool, WireGuard profiles and portable WARP.
- Automatic connection tries public MTProxy, then WARP, then direct (if allowed) and shows a status indicator instead of failing silently.
- Video duration limits in file policies.

**Panel and safety**

- No more one-click accidents: pausing, excluding and removing sources are confirmed, sending from a chat needs "Write as @account" first, route changes while observing offer to pause.
- One set of counters everywhere (deleted with text, deleted before saving, missing on recheck).
- Account files are inspected before connecting. URL, workspace and account always agree, a mismatch blocks actions. Chats open read-only and mask detected secrets.
- Downloads fall back to normal browser downloads, big archives stream through one-time cookies. Prepared exports keep size, SHA-256 and "Download again".
- Panel token rotation keeps the new session alive. Temporary network failures offer Retry.
- Panel dialogs instead of `window.confirm`, journal paging fixed, lots of small UI fixes.
- Public-channel showcase: expiring read-only links with redacted authors and signed snapshots.

**Servers and evidence**

- Extras → Server 24/7: a Hetzner server from the panel with a quick tunnel or your own domain. `python -m tgwitness.cloud destroy` cleans everything up.
- Phala Cloud option: the collector runs in an Intel TDX confidential VM, `verify` checks the attestation up to Intel's root.
- Gateway DNS (`--gateway-dns`): the server only resolves through Cloudflare Gateway.
- Optional drand rounds and Telegram device lists in evidence mode.
- Setup by goal: four questions, suggested settings, credibility and reliability scales.

**Other**

- Notification service catalog with icons, optional operator control bot, Discord witness posts.
- Storage separates backups, verified file offloading and evidence retention.
- AI previews show the endpoint and outside route.
- Pull requests run both panel suites, including Firefox and WebKit downloads. Release packages wait for dependency, CodeQL and container audits.
- Docs: a [panel guide](https://phishdestroy.github.io/TgWitness/docs/reference/panel/) for every screen.

## 0.7.1 preview · 1 November 2026

- **Start here** with two paths: export my account, or follow an investigation.
- Account export through Telegram Takeout or the regular API, resumable, with signed progress and coverage records ([account export](https://phishdestroy.github.io/TgWitness/docs/reference/account-export/)).
- Separate signed sharing copies with filters, pseudonyms and optional text/file removal. Signatures establish integrity; they do not establish Telegram authorship, completeness or legal admissibility.
- Readable offline reports for account exports and sharing copies, printable, with record links and instructions for the recipient.
- Clear handoff after download: original vs sharing copy, report preview, instructions to copy.
- Rejected Telegram logins are told apart from paused accounts and network errors. **Sign in again** keeps the workspace.
- Load the history of enabled sources with pause/resume, plus a signed progress report ([history](https://phishdestroy.github.io/TgWitness/docs/reference/history/)).
- Read-only MCP at `/mcp`, local archive search with optional AI, local OCR/transcription, signed webhooks with retries.
- GitHub Actions capture preview: one chat on a temporary runner, encrypted result, pinned provenance ([sealed capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)).
- Self-contained signed reports in 25 languages with chain of custody; archives add `custody.json` and `SHA256SUMS`.
- Panel rework: workspace URLs, Back/Forward, drafts survive updates, Ctrl/Cmd+S, Sources split into tabs, Parameters search, journal filters and inspector, live updates.
- Batch session import, account groups, MTProxy dashboard with ping, countries and own lists.
- MTProxy decryption through OpenSSL (it used to eat a whole CPU core).
- Stronger masking in sharing copies, bounded media decoding, repeatable source ZIPs.
- Notification services refuse redirects. Weekly Dependabot, nightly CodeQL and container scans.
- Lots of fixes: stuck chat profiles, quick search, DST in search dates, 502s behind Caddy, GIF/sticker downloads, slow proxy list parsing, duplicate sessions on import.

## 0.7.0 preview · 31 October 2026

- OpenTimestamps proofs are parsed strictly; Bitcoin attestations show as `bitcoin-unverified` until you run `ots verify`.
- Verification reports which part of the journal witness checkpoints cover; `--require-witness` demands a pinned witness and matching final record.
- Access and permissions guides, updated proxy and IP mode guides.
- Panel and docs site in 25 languages. Site publishing fails on missing translations.
- Added the [roadmap](https://github.com/phishdestroy/TgWitness/blob/main/docs/ROADMAP.md).

### Initial preview contents · 30 October 2026

- First GitHub release: Windows portable, wheel, source archive.
- The setup guide has an "Open to everyone" section: no country or sanctions blocks, and Taylor Wessing as the only incompatibility we name. It is our position, not a licence condition.
- The README and Wiki now present the authors' Ethical Notice & Historical Continuity statement, with document references, historical context and an explicit explanation that MIT permission applies to everyone.
- The operator notice and the Taylor Wessing page speak in our own voice.
- Returned to the MIT License. A tool whose output third parties must be able to check should not stumble over its licence. `LICENSE` is the standard MIT text again, the package declares MIT with the OSI classifier, and the container, portable package, website, Wiki and translated README labels say so. Our statement stays in NOTICE and on the Taylor Wessing page as our position; it adds no licence condition. The presentation artwork reads "open source" again.
- Added our Operator Incompatibility NOTICE to README, SECURITY, the documentation, Wiki and website. A single source keeps the complete statement consistent across those pages; source, Python and portable distributions include NOTICE alongside the licence.
- High-assurance deployment (`python -m tgwitness.cloud`, [guide](https://phishdestroy.github.io/TgWitness/docs/reference/high-assurance/)) on Hetzner, DigitalOcean, Linode, Vultr or EC2: no SSH key, no inbound ports, panel only through a Cloudflare Tunnel, and a `verify` command for third parties.
- Local launchers open the panel in the browser once it's up.
- Read-only online demo of the real panel with fictional data.
- Wiki with 13 guides, docs website with a reference section, search, diagrams and 13 languages.
- **Sign out of Telegram** on the Account page.
- About 940 Russian panel strings fixed by hand.
- Observation scope: chosen chats, a folder or the whole account, by type. New chats are picked up immediately.
- Investigation mode for accounts that join groups and talk to bots.
- People profiles (opt-in per chat), independent witness bot, notification excerpts, Parameters page, light/dark theme.
- Panel mini-client: send messages, press bot buttons, preview and join invites.
- Fixed message loss after a long stop (rechecks used to stop after 1,000 messages).
- Many fixes from a full review: attachment byte counts, restore checks, scope edge cases, verify.py witness handling, off-site copy retries.
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

Older history: [release status](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RELEASE.md) and [verification](https://phishdestroy.github.io/TgWitness/docs/reference/verification/).


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
