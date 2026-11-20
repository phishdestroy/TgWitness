[TgWitness](../README.md) / [Documentation](README.md) · [Investigation](INVESTIGATION.md)

**English** · [Русский](ru/SIMILAR-CHANNELS.md)

![Investigation](assets/presentation/chapter-investigate.svg)

# Similar channels

Telegram keeps a list of channels it considers similar to a given channel and
offers it to readers. TgWitness can walk that list from one or more starting
channels and record what Telegram returned.

A suggestion is produced by Telegram from its own usage signals. Treat the result
as a lead list: a shared operator, owner, author or purpose is established from
the channels' own records.

## Run a walk

```sh
curl -sS -X POST http://127.0.0.1:8787/api/channel-graph \
  -H "Authorization: Bearer $TGWITNESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"seeds": [-1001234567890], "depth": 2, "per_source": 20, "total": 100,
       "min_participants": 500, "require_username": true, "pause_seconds": 1}'
```

Only the main administrator can start a walk, and the account must be connected.
Each seed must be a chat this account has already read, so resolve the channel in
the panel first.

| Setting | Meaning | Range |
| --- | --- | --- |
| `seeds` | Channels the walk starts from | 1–50 chat IDs |
| `depth` | How many suggestion steps to follow; `1` reads the seeds only | 0–4 |
| `per_source` | Suggestions processed from one channel before filters | 1–200 |
| `total` | Channels in the whole result, including the seeds | 1–2000 |
| `min_participants`, `max_participants` | Subscriber range to keep | any order-consistent pair |
| `require_username` | Drop channels without a public username | off by default |
| `skip_restricted` | Drop channels Telegram marks as restricted | off by default |
| `pause_seconds` | Wait between requests | 0–60 |

Filters shape the retained node list. The journal keeps each processed
suggestion, including suggestions dropped by a filter, and reports the counts.
The `per_source` and whole-run budgets can leave received suggestions unprocessed.

## What the journal keeps

`graph.started` records the seeds and the settings. One `graph.suggestions`
record per visited channel holds what Telegram returned, how many were kept and
the channel IDs and usernames. `graph.source_unavailable` marks a seed the
account cannot read. `graph.finished` closes the run with the totals and the
reason it stopped.

Each suggestion record separates Telegram's reported `total` from the received
channel count (`suggested`), processed count (`returned`) and count passing
filters (`kept`). A sliced API response can therefore report a larger total than
the list available to this account. `response_complete` indicates that all
reported suggestions were received; `complete` additionally requires processing
the entire received list. These flags describe the response and processing before
filters, not a complete map of Telegram channels. The result's `sources` list
retains the same counts and flags for each successfully queried source.

A walk stops early and says so when it reaches `total`, or when Telegram asks the
account to wait. A flood-wait answer is recorded as `telegram.backoff`, the
account-wide pause is honoured, and `stopped` reads `rpc_backoff`.

## Result

The answer is a `tgwitness-channel-graph-v1` object with `nodes` (chat ID, title,
username, subscriber count, Telegram flags, discovery depth and source) and
`edges` (which channel suggested which). Each node keeps the flags Telegram
supplied, including `scam`, `fake`, `verified` and `restricted`.
