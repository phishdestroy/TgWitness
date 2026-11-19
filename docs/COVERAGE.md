[TgWitness](../README.md) / [Documentation](README.md) · [Evidence and verification](EVIDENCE.md)

**English** · [Русский](ru/COVERAGE.md)

# What was collected and what was not

A TgWitness archive says what it holds and, separately, what it does not. This page explains
how to read that: a complete or partial export, the weekday and hour heat map, the periods the
collector was observing, the message numbers it never saw, and how to cite each of them by ID.
Every figure below comes from files inside the signed archive, so the panel, the HTML and PDF
report and `coverage.json` give the same numbers.

## Full account export and full chat export

- **Whole account.** [Account export](ACCOUNT-EXPORT.md) acquires every chat the account can see,
  inside the chosen scope (chat types, dates, media actions). The archive holds `job.json` (frozen
  options), `inventory.json` (the chats found), signed `receipts/` and `data/*.jsonl` pages,
  `message-gaps.json`, `analytics.json`, `map.html`, `index.html`, one `chats/<chat ID>.html` per chat and
  `result.json`.
- **One chat or channel.** The [distributed chat export](DISTRIBUTED-EXPORT.md) and the single-chat
  export take a chat by ID or link and write the same kind of signed archive for that chat.
- **Complete is never assumed.** An account export's Coverage section reads *Completed within
  selected scope* only when discovery finished, no task failed and every planned task is done;
  otherwise it reads *Partial acquisition*. Either way it adds that acquisition is not an atomic
  account snapshot, and that deleted, inaccessible or previously edited data may be unavailable.
  The section lists tasks done against tasks planned, failures and omissions, and `inventory.json`
  records whether discovery finished and how many chats were found and excluded. A scope that
  completed is different from messages that were never numbered into the archive, and both are
  different from deletions.
- **Check before you rely on it.** Verify the original ZIP with the signer's fingerprint from a
  separate channel:

```sh
python -m tgwitness.verify tgwitness-evidence.zip --fingerprint TRUSTED_SHA256
```

## Activity heat map

The report draws activity as a grid of weekday (Monday first) by hour of the day, in UTC. Darker
cells mean more observations. In the evidence report each cell carries its own label, for example
`Monday 00:00 UTC · 0`, so the figure can be read without colour. The account export states the
largest cell instead.

- In an **evidence report** the grid counts observation times, which come from the collector's
  clock. In an **account export** the grid (*Weekly rhythm*) counts message rows by the time Telegram
  reports for the message.
- The grid describes the selected records only. If the selection holds no records, the report says
  *No observations in this selection* instead of showing a grid of zeros.
- Hour and weekday counts help estimate a sender's time zone; they do not reconstruct activity
  outside the period that was collected.

## Observation periods and gaps

`coverage.json` separates four things:

| Field | What it holds |
| --- | --- |
| `continuous` | Periods the collector was observing, each with `from`, `to` and `seconds`. A period follows connected capture heartbeats and ends at its last confirmation or a recorded stop. |
| `gaps` | Intervals with no observation, each with `from`, `to` and a `reason`. A gap that runs to the end of the journal carries `not_resumed_by_last_record`. |
| `session_windows` | Stretches where Telegram's update counter grew without updates reaching this session, or the session left Telegram's session list. They are gaps for coverage purposes. |
| `notes` | Events about one chat, for example a `flood_wait` recorded for a chat. They are listed as *Coverage notes*, counted apart from gaps, and give the chat ID, time and reason. |

A journal with no capture heartbeats, such as one imported or built from a single export, shows
*0 continuous observation periods* and the report says *No observation period recorded*. That is a
statement that nothing recorded the collector's presence, not that nothing happened.

## Message numbers that were never seen

Telegram numbers messages once per channel or supergroup, and once per account across private
chats, bots and ordinary groups. A number between the first and last observed message that was
never seen belongs to a message this collector does not hold. `coverage.json` records this twice:

- `unobserved_ids[]` has one entry per chat with `observed_from`, `observed_to`, `observed`,
  `not_observed` and `ranges[]` of `low` and `high`.
- `gap_summary` adds `numbering`, `status`, `density`, `gap_ranges`, `largest_gap` and `clusters[]`.
  Each cluster gives the missing range and the neighbouring observed messages as `after` and
  `before`, with their observation times. Details: [Missing message numbers](EVIDENCE.md#missing-message-numbers-gap_summary).

A missing number is not a deletion. The archive records deleted messages and messages missing on
recheck as separate observations. The account-wide sequence of private chats, bots and ordinary
groups is measured only while whole-account collection is on; otherwise `account.status` is
`not_applicable` with the reason, and the report lists the chats not compared.

## Where the report shows it

| Report section | What it tells the reader |
| --- | --- |
| *In brief* and the cover | Records, chats, messages, edits, deletions, files and the observation period, or *No observation period recorded*. |
| *Unobserved message IDs* (in the selected data) | For the chosen chats and dates, each missing range with the saved message before and after it, for example `-1001000000001 · 20–29 · Message 19 · record #21 … Message 30 · record #22`. |
| *Scope and missing material* | One line of counts: recorded gaps, coverage notes, continuous periods and message numbers not observed. |
| *Source journal coverage* | The tables behind those counts: *Continuous observation*, *Gaps*, *Message IDs per chat* (observed range, observed, not observed, numbers not observed), *Missing message numbers* and *Coverage notes*. |
| *Activity map* in an account export (`map.html`) | Absent message numbers per chat, the largest runs, and how many were proven by an exported reply or pin. |

The counts in these sections come from the same signed files as `coverage.json`: for a test journal
the report showed *Message numbers not observed: 11* and `coverage.json` listed 11 numbers in the
ranges `20–29` and `41`. `verify.py` recomputes the gap measurement from `events.jsonl`, so a
changed number is reported as a failure.

## Citing a record or a gap by ID

Use the IDs that appear in the files:

- **Chat ID** as in `coverage.json` and the report, for example `-1001000000001` for a channel or
  supergroup.
- **Message ID** within that chat. Message numbers repeat across chats, so always give both.
- **Record reference**: the journal sequence number and its SHA-256 hash. The report appendix lists
  both for every cited record, and an account export names the archive reference beside each
  message.
- **A gap** is cited as the chat ID, the missing range and its two neighbours, for example: chat
  `-1001000000001`, message numbers `20–29` (10 numbers) between message 19 (record #21) and
  message 30 (record #22).

## What to tell a reader

1. State what the archive holds: scope, dates and the observation periods in `continuous`.
2. State what it does not hold: gaps and their reasons, session windows, coverage notes and the
   unobserved message ranges, each with the chat ID.
3. Do not describe a missing number or a gap as a deletion, and do not describe an absence of
   observation as proof that nothing happened.
4. Give the fingerprint source and the verification result next to these figures.
