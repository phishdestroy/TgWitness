# Set up a witness bot

Canonical page: https://phishdestroy.github.io/TgWitness/docs/witness/

A separate process checks your journal and posts signed checkpoints to a channel.

## Two hosts, two signing keys

HOST A / COLLECTOR**Account + journal**

Telegram session
Collector signing key

Read-only checkpoint endpoint

← request
signed answer →

HOST B / WITNESS**Verify + retain**

Pinned collector fingerprint
Separate witness signing key

Own journal + bot token

Witness → Telegram Bot API →**Your channel · signed TGW1 posts**

The witness pulls checks itself. Collector access is read-only. Bot publication uses the witness’s connection and token; no account session is given to the witness.

03 / CHECKPOINT DECISIONSIllustrative answers

LAST ACCEPTED**120 records**`head 9c7d…`

NEXT ANSWER**128 records**`head a4f2…`

Accepted: the count grows, the signature verifies and the key matches. The witness retains this new boundary.

All answering examples assume a valid signature and the pinned key. Hashes here are abbreviated illustrations. A larger count alone cannot prove that the entire old prefix is unchanged; compare an export with retained checkpoints.

## Prepare a bot and a channel

Make a bot with BotFather and let it post in your channel. Run the witness somewhere else: another host, ideally run by someone else, is worth much more than a second process next to the collector.

## Three steps in Extras

1. **Read-only access.** **Extras → Independent witness**, create a token, save the file. It reads checkpoints and health, nothing else.
2. **Channel and interval.** Telegram channel or Discord webhook, plus a collector address the witness can reach. Save the settings file.
3. **Launch.** Put `witness.json`, `witness-token.txt` and `bot-token.txt` together on the witness host and run:

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Wait for the first signed post in the channel, then save the witness fingerprint somewhere safe.

Discord instead? Save the webhook URL as `discord-webhook.txt`. One witness posts to one place; long checks arrive as a file on Discord.

## Choose how often to publish

Posting every check gives a steady outside record: every five minutes is about 288 posts a day per workspace. Advanced settings can post only on changes or problems, use a proxy or a custom Bot API.

**What does the bot actually attest to?**

It asks the collector for a signed checkpoint, checks it against the expected key and keeps its own signed journal, including missed and rejected answers.

It checks the journal state, it doesn't watch Telegram itself. For that, run a controlled delivery test.

## Check the evidence later

Keep the witness journal, the posts and the fingerprints. [How to check them](https://phishdestroy.github.io/TgWitness/docs/reference/witness/#verify) against the collector's export.
