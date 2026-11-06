# Export and verify

Canonical page: https://phishdestroy.github.io/TgWitness/docs/exports/

Hand someone files they can check themselves against your workspace.

Retain a referenceExport signed ZIPRecipient verifies

New to signatures and checkpoints? [Change a sample record](https://phishdestroy.github.io/TgWitness/docs/concepts/#chain) and see which checks catch it.

Keeping a copy away from the collector? Go to [S3 setup](https://phishdestroy.github.io/TgWitness/docs/exports/#s3), [Object Lock](https://phishdestroy.github.io/TgWitness/docs/exports/#s3-retention) or [verified recovery](https://phishdestroy.github.io/TgWitness/docs/exports/#s3-restore).

## Retain a trusted reference

Write down the workspace key fingerprint somewhere other than the collector. While collecting, keep signed checkpoints elsewhere too, or run an [independent witness](https://phishdestroy.github.io/TgWitness/docs/witness/). That's what the recipient checks the key and an earlier journal state against.

## Download the signed ZIP

**Exports** → signed evidence ZIP. It has the whole journal and a signed file manifest. Shape the readable report in [Report studio](https://phishdestroy.github.io/TgWitness/docs/reports/), or send only selected data as a [handover extract](https://phishdestroy.github.io/TgWitness/docs/handover/).

HTML, PDF and JSON reports carry their own seals. CSV is just a working copy; for integrity use the CSV inside the verified ZIP.

## Verify with a trusted copy of TgWitness

In the project environment, with your own fingerprint and paths:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

A pass shows `key_pinned: true` and `checkpoint_checked: true`. Keep that output next to the archive. The checkpoint has to be at or before the end of the export.

## Use the verification result

- **Files:** the manifest binds their hashes, the signatures bind the journal. Any change shows up.
- **Identity:** the fingerprint you kept proves it's the key you expected.
- **Earlier state:** a checkpoint compares the export with a journal prefix saved before the handoff.
- **Coverage:** gaps, acquisition results and a send → edit → delete test show what this setup actually caught.

Details: [what verification proves and what it doesn't](https://phishdestroy.github.io/TgWitness/docs/reference/evidence/#verification-scope).

## Set up the S3 off-site copy

**Exports → Off-site copy** in your workspace. Works with AWS S3 and anything S3-compatible. It copies journal segments, saved files, checkpoints with their timestamps and finished chat exports, each encrypted with `AES-256-GCM` before it leaves the collector.

The online demo shows these controls with uploads off. Only enter real credentials in your own install.

[![Complete Off-site copy panel: endpoint, region, bucket, access keys, schedule, Object Lock and recovery key controls](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

The complete panel with advanced options expanded. No storage credentials are shown.

| Field | What to enter |
| --- | --- |
| Endpoint | Storage URL, no bucket path or credentials. Example: `https://s3.example.invalid`. |
| Region | Whatever your provider needs. Default `us-east-1`. |
| Bucket | An existing bucket you can write to. Example: `example-case-backup`. |
| Folder in the bucket | Prefix, default `tgwitness`. A per-workspace prefix is added on top. |
| Access key ID / Secret access key | Both together, stored in the vault. Leave both empty later to keep them. |
| Path-style addresses | On: `endpoint/bucket`. Off: `bucket.endpoint`. Depends on the provider. |
| Copy interval | 1 to 1,440 minutes, default 5. Only while the app runs. |
| Object Lock retention | Days and mode, if the bucket supports Object Lock. Zero keeps the bucket default. |

1. Create the bucket, fill in destination and credentials with **Keep an off-site copy** unticked, hit **Save off-site copy**.
2. **Test connection** uploads an encrypted test object.
3. **Download encryption key** and keep it away from the collector. No key, no recovery.
4. Tick **Keep an off-site copy**, save, then **Copy now** or let the schedule run.

## Check retention and copy progress

Under **More options** pick retention days and `GOVERNANCE` or `COMPLIANCE`. TgWitness reads the retention back from an uploaded object and tells you: confirmed, missing or check failed.

The panel shows the last pass, object count, bytes, copied journal boundary and errors. A missing local file is reported and retried next pass, the rest keeps copying.

Uploads go over Direct, SOCKS5 or HTTP. With an MTProxy-only route the copy waits with an error.

## Keep the recovery key separately

The key JSON has the decryption key, destination, prefix and key fingerprint. For recovery you need it plus storage credentials with read access.

Changed endpoint, bucket or prefix? Download the key again. A fresh copy starts at the new destination; old chat exports stay where they were.

## Restore and verify on another machine

You need a TgWitness install you trust, the key JSON, read-only storage credentials and an empty folder:

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

Everything is checked in a private temp folder first: the whole journal, checkpoints, file hashes and sizes. Unsafe paths, conflicting segments or a journal shorter than its checkpoint fail, and then nothing is written out.

On success you get `events.jsonl`, `media/`, `checkpoints/` and `exports/`. Keep the command's JSON output with them, and compare against checkpoints or witness records you kept yourself.
