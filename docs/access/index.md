# Share Telegram Case Access with Reviewers

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
