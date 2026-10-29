![Keep an independent check — Checkpoints, signed counters and observation continuity.](../assets/presentation/wiki-witness-and-proof.svg)

# Witness and public Proof

[Project](../../README.md) · [Documentation](../README.md) · [Wiki](Home.md) · [Support](../../.github/SUPPORT.md)


| Component | Purpose |
| --- | --- |
| Collector | Records what its Telegram account observes |
| Witness | Fetches a signed journal boundary, signs its observation and can publish a channel post |
| Proof monitor | Shows signed counters and health for several workspaces |
| Controlled delivery test | Compares known send/edit/delete actions with captured evidence |

A witness has its own key and a read-only token. That token cannot read messages, control the collector or obtain its Telegram session.

## Keep a boundary you can compare

![A four-record export matches the independently retained boundary at record three.](../assets/presentation/evidence-checkpoint-animated.svg)

An export may grow beyond a checkpoint. After verifying the checkpoint signature,
compare the hash at its saved record count. A shorter export cannot satisfy a
checkpoint beyond its end; matching the boundary does not replace checking every event.

[Open the full-size animation](../assets/presentation/evidence-checkpoint-animated.svg) · [Static diagram](../assets/presentation/evidence-checkpoint-static.svg) · [Exact checkpoint formula](../HOW-IT-WORKS.md#what-an-earlier-checkpoint-adds)

## Set up a witness

1. Open **Extras → A bot in your channel → Set up a bot**.
2. Create a read-only token and save it as `witness-token.txt`.
3. Configure your channel, polling interval and reachable collector address. Download `witness.json`; it pins the workspace's collector key.
4. On the witness host, place the JSON and token together. Save your Telegram bot token in `bot-token.txt`. Give your bot permission to post in your channel.
5. In the installed project environment, check and launch:

~~~sh
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
~~~

The configuration check makes no network requests. Starting the witness may publish messages according to your configuration; downloading the JSON alone does not start it.

Retain its fingerprint separately:

~~~sh
python -m tgwitness.witness fingerprint --config witness.json
~~~

Check the witness log and actual channel posts. A last-poll time in the collector only confirms a request.


![Section divider](../assets/presentation/divider.svg)

## Add a public Proof monitor

Start with the [Proof setup guide](../PROOF.md) and [configuration example](../../deploy/proof.config.example). Give each workspace a distinct collector fingerprint and its own read-only token file. Use neutral public labels.

Check and start the native monitor:

~~~sh
python -m tgwitness.proof --config proof-config/proof.json --check-config
python -m tgwitness.proof --config proof-config/proof.json
~~~

The default panel is on port 8790. It exposes counters, hashes and health rather than message text. Use a separate HTTPS hostname for public access and keep the collector's control panel protected.

## Interpret the result

A witness on the same server provides a separate process and key, but not independent operator custody. A growing counter does not prove every message was captured. Compare downloaded proof receipts with the matching signed evidence archive, and use a controlled delivery test for specific events.

**Next:** [Witness reference](../WITNESS.md) · [Proof and canary procedure](../PROOF.md) · [Evidence limits](FAQ.md)
