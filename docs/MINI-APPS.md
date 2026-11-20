[TgWitness](../README.md) / [Documentation](README.md) · [Investigation](INVESTIGATION.md)

**English** · [Русский](ru/MINI-APPS.md)

![Investigation](assets/presentation/chapter-investigate.svg)

# Mini applications

A Telegram mini application is a web page a bot opens inside the client: a shop, a
"bonus" claim, a wallet connection. Scam bots use them to collect phone numbers,
seed phrases and payments away from the chat. TgWitness opens one the way a
Telegram client does, loads it once in an isolated headless Chromium and records
what it does.

## In the panel

Under a message, a mini application button has **Open mini app**. In a chat,
**Info → Mini apps** lists where the chat opens mini applications:

- buttons under messages and reply-keyboard buttons;
- `t.me/<bot>/<app>` and `t.me/<bot>?startapp` links in messages, entities and link
  buttons;
- in a bot chat, the bot's menu button and its main app.

**Open** asks for confirmation, then:

1. asks Telegram for the launch address as this account, which is an account
   action: the bot learns that this account opened it and sees its name and ID.
   For a button under a message, the bot can post one message to the chat on the
   account's behalf while the application is open;
2. loads the address once in Chromium with a phone screen, through the
   workspace's route for requests outside Telegram;
3. records the result in the signed journal and shows it under **Recorded
   openings**.

Only the main administrator can open a mini application.

## What is recorded

- every request with method, type, status, MIME type and size, and the TLS
  certificate subject and issuer; hosts other than the application's own are
  listed separately;
- WebSocket addresses and up to 30 frames each;
- every call the page makes to the Telegram WebApp API, for example a request for
  the phone number, a payment, opening a link or sending data to the bot; requests
  that ask something of the user are flagged;
- dialogs it showed (they are dismissed), windows it tried to open (with their
  address; they are not loaded), downloads it started, forms and input fields;
- screenshots 2, 8 and 16 seconds after loading and of the whole page, the page as
  it was after loading and up to 25 of its scripts;
- links, domains, wallets, Telegram accounts, e-mail addresses and phone numbers
  found in the page, its traffic and Telegram calls; wallets in scripts only when
  their checksum is valid.

The launch address carries signed launch data (`tgWebAppData`) that works as a
login to the application for a while. It is removed from everything that is
recorded: the address keeps no fragment, and the data, its hash and its query ID
are replaced with `[removed]` in requests, frames, calls and saved files.

Journal records:

| Record | Meaning |
|---|---|
| `webapp.launch_requested` | Telegram returned the launch address; account action |
| `webapp.launch_failed` | Telegram refused to open it, with its answer |
| `webapp.file` | one preserved file (`media_sha256`, size, role), bound to the archive like saved media |
| `webapp.captured` | everything listed above, with the counts of items dropped at the caps |
| `webapp.capture_failed` | the application could not be loaded |

Screenshots appear in the investigation timeline and its documents, indicators
appear in reports under the source **mini app**, and evidence archives carry the
files under `media/`, checked by `verify.py`.

## Browser

TgWitness drives Chromium over `--remote-debugging-pipe`; no extra Python package
is needed. It looks for `chromium`, `chromium-browser`, `google-chrome` and a
Playwright Chromium; set `TGWITNESS_CHROMIUM` to a path to choose one.

The application runs in its own browser context. Every connection it makes,
WebSockets included, goes through a loopback gate that opens it over the
workspace route like any other request outside Telegram. Chromium's own
background requests (sign-in, component updates) go to a second gate that refuses
them; a Google host the browser contacts on its own, and the page never asked
for, is listed under `browser_connections` instead of the application's
connections. When that route is turned off, or Hide IP mode is on without a proxy,
the application is not opened. Addresses inside the local network are refused, and
WebRTC cannot send UDP outside the route.

Chromium runs with its sandbox. When TgWitness runs as root, Chromium cannot use
it, so opening is refused unless `TGWITNESS_BROWSER_NO_SANDBOX=1` is set; do that
only on a machine used for this work.

Without a browser, or on Windows, **Open** still asks Telegram for the address and
then fetches the page and up to 12 of its own scripts, parsing them for addresses
and WebSocket endpoints.

## API

```sh
curl -sS "http://127.0.0.1:8000/api/webapp?chat_id=-1001234567890&limit=200" \
  -H "Authorization: Bearer $TGWITNESS_TOKEN"
```

Reads saved records only and contacts nobody: `entries` lists buttons and links,
`captures` the recorded openings, `browser` whether a browser can be used. Accesses
limited to chosen chats see their own chats; `GET /api/webapp/captures/{seq}?chat_id=…`
returns one recorded opening.

```sh
curl -sS -X POST http://127.0.0.1:8000/api/webapp/open \
  -H "Authorization: Bearer $TGWITNESS_TOKEN" -H "Content-Type: application/json" \
  -d '{"chat_id": 5104055776, "entry": {"type": "button", "seq": 1522, "row": 0, "column": 0}}'
```

`entry.type` is `button` (with the keyboard record `seq`, `row` and `column`),
`link` (with `url`), `menu` or `main`.

`POST /api/webapp/inspect` with `{"url": "https://app.example/start", "scripts": 12}`
fetches a page you already know without asking Telegram, follows up to `scripts`
of its own scripts and records `webapp.inspected`.

## Limits

One loading, at one moment, from this workspace's address. Another visitor, time or
address can be served something else, and an application can check where it is
opened. Requests are capped at 400, Telegram calls at 200 and the whole opening at
about 75 seconds; the counts of dropped items are recorded. TgWitness does not
click inside the application or fill its forms.
