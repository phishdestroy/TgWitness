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
