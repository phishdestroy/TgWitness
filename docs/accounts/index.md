# Connect Telegram: QR, Phone & Session Import

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
