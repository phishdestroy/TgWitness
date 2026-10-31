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
