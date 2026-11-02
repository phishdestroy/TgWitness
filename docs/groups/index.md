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
