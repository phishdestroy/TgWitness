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
