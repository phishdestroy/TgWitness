# Fix Telegram Login, FloodWait & Collection Gaps

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
