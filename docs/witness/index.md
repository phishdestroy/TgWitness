# Set up a witness bot

Canonical page: https://phishdestroy.github.io/TgWitness/docs/witness/

Let a separate process check the journal and publish signed checkpoints to your channel.

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

Create a bot with BotFather and allow it to post in a channel you control. Choose a computer or server for the witness. A separate host and operator provide stronger independence than a second process on the collector’s server.

## Three steps in Extras

1. **Read-only access.** Open **Extras → A bot in your channel**, create a witness token and save the access file. It allows reading checkpoints and health, not conversations or collector controls.
2. **Channel and interval.** Enter the channel and a collector address reachable from the witness. Save the settings file.
3. **Launch.** Put `witness.json`, `witness-token.txt` and a `bot-token.txt` created on the witness host together. Run the commands below in the installed project environment.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Downloading the files does not start the witness. Check that the first signed post appears in the channel, then retain the witness’s public-key fingerprint separately.

## Choose how often to publish

Publishing every check creates a regular external record. At five-minute intervals, that is about 288 posts per workspace per day. The advanced settings also offer publication on changes or problems, a proxy and a custom Bot API address.

**What does the bot actually attest to?**

The witness asks the collector for a signed checkpoint, verifies it against the expected key and keeps a separate signed journal. It records missing responses and rejected answers as well as successful checks. Publication still depends on the witness running and reaching Telegram’s Bot API.

It checks the collector’s reported journal state. It does not independently observe every Telegram message. For that, add the controlled delivery test.

## Check the evidence later

Keep the witness journal, channel posts and independently saved fingerprints. The [full verification procedure](https://phishdestroy.github.io/TgWitness/docs/reference/witness/#verify) compares them with the collector’s signed export.
