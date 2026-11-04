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
