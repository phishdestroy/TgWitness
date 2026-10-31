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
