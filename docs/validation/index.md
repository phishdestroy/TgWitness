# 56 329 messages.

Canonical page: https://phishdestroy.github.io/TgWitness/docs/validation/

TGWITNESS / REAL EXPORTS

Captured. Exported.

Two fresh Telegram exports, timed from collection to the finished archive. Explore the workspace, inspect the numbers and download a sample.

[Explore the demo](https://phishdestroy.github.io/TgWitness/demo/?lang=en)[Download sample export](https://phishdestroy.github.io/TgWitness/demo/downloads/tgwitness-demo.zip)

The interactive demo and sample use fictional messages. The measurements below come from real export runs.

TGW / 001

Recorded snapshot · not live monitoring

Checked at

2026-11-06 18:37:38 UTC

Tested revision

[92e539af](https://github.com/phishdestroy/TgWitness/commit/92e539af40d8368d198ff5e040f1d876f2c1310e)

Text + metadata · signed archives

**56 329**Messages exported

**160.531**Messages/s · best collection run

**2**Signed export runs

**3**Servers inspected

Server AWARP · 2 accounts

**27 030**Messages exported

**142.983**messages/s

Collection only

189.043 s

Complete export

211.647 s

Server BWARP · 2 accounts

**29 299**Messages exported

**160.531**messages/s

Collection only

182.513 s

Complete export

206.650 s

01 /

## Measured on real exports.

One new export per server, using two accounts on each. Text and metadata through WARP; attachments excluded. These are individual runs, not a capacity guarantee.

messages/s

Server A**142.983 messages/s**

Server B**160.531 messages/s**

Server C

Not measured

—

Messages ÷ collection time. Preparation, selection and packaging are outside this interval.

Messages ÷ total measured export time, including preparation and packaging.

No collection benchmark receipt for server C.

No reused records or duplicate IDs in either run. Server A also had a protected-source read running in the background. FloodWait pauses were respected: A · 4, B · 3.

**Exact measurements & archive hashes**

| Server | Messages | Collection only | Complete export |
| --- | --- | --- | --- |
| Server A | 27 030 | 189.043 s **142.983 messages/s** | 211.647 s **127.713 messages/s** |
| 2026-11-06T18:26:51.500Z → 2026-11-06T18:30:23.228Z SHA-256 `20e507fc68446680ed002fd486d0968a944ec0c71e02f937331ae2b19ab4cd66` |  |  |  |
| Server B | 29 299 | 182.513 s **160.531 messages/s** | 206.650 s **141.781 messages/s** |
| 2026-11-06T18:25:40.419Z → 2026-11-06T18:29:07.173Z SHA-256 `824601b502762efaabb8ff9afdb1e8d7fff189862ef2cbc4d8d26d0d68c83e4c` |  |  |  |

Both archives passed verification with a pinned collector key. This establishes integrity relative to that key, not Telegram authorship.

02 /

## All three, with the scope spelled out.

Journal integrity, file permissions, storage, network routes and running processes were inspected on every server.

A Inspected

### Server A

Collection & export

8 vCPU · 16 GiB · Ubuntu 24.04

Journals checked

21

Journal events

4 517

Checkpoints

147

Fresh collection benchmark, archive verification and backup integrity checks.

B Inspected

### Server B

Collection & export

8 vCPU · 16 GiB · Ubuntu 24.04

Journals checked

21

Journal events

1 993

Checkpoints

147

Fresh collection benchmark, archive verification and backup integrity checks.

C Inspected

### Server C

Panel & nested VM

8 vCPU · 32 GiB · Ubuntu 24.04

Journals checked

14

Journal events

7 185

Checkpoints

973

Panel authentication, loopback binding and a nested VM inspected. No collection benchmark on this server.

**Test results, scope & technical notes**

03 /

## Passes and gaps, side by side.

Latest result per pytest case, including reruns. Standalone browser and evidence suites are counted separately below; they are not added to the pytest total.

**1 585**Passed

**3**Failed

**37**Skipped

Three capture browser tests failed because the required Chromium sandbox is unavailable in these containers. The sandbox was not disabled. The 37 platform skips do not count as passes.

- Browser suites**102 passed**
- Interface suites**66 passed**
- Evidence suites**15 passed**
- Website suites**9 passed**
- Additional suites**13 passed**

04 /

## What this snapshot leaves open.

1. 01

   ### Browser sandbox

   Three browser failures remain in this environment. A successful run elsewhere does not replace these results.
2. 02

   ### Backup recency

   42 backup journals and 51,285 files passed integrity checks. At the snapshot, 3,507 live events were newer than the latest backups. Active data also needs durable storage.
3. 03

   ### Network coverage

   16 of 40 route qualifications were unavailable. Those accounts were not connected to Telegram through a direct fallback.
4. 04

   ### Independent time

   The retained witness journal passed integrity checks. Its last event was at 07:27 UTC on 6 November; independent timestamp verification was not performed.
5. 05

   ### Open security work

   Key protection, account protection, durable storage and release controls still have open findings. Successful integrity checks are not a security certification.
6. 06

   ### Access limits

   The separate CI host and the publishing account were not inspected at operating-system or account level. The three inspected servers are the scope of this page.
7. 07

   ### Measurement limits

   Two public sources, two individual runs, no attachment download and no repeated trials. Server C has no measured collection rate. These numbers do not predict other workloads.

05 /

## A dated record, with a way back to the numbers.

These are operator measurements, not an independent attestation. The JSON contains only aggregate data. Source and account identities, message contents, credentials and private archives are not published.

1. Pin the source revision and verify the installed release.
2. Collect into a new workspace, retaining zero reused records.
3. Measure collection and complete-export intervals separately.
4. Verify the archive against its pinned key; retain its SHA-256 digest.

Tested release `92e539af40d8-83e41104669e`

[Download the data ↓](https://phishdestroy.github.io/TgWitness/validation/snapshot.json)

SIGNED AUDIT / ENGLISH

### Check the numbers.

The English report includes the measured results, open findings and a reproducible signature check.

[Read the report ↗](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md)[Signed statement ↓](https://phishdestroy.github.io/TgWitness/validation/audit/PROOF.json)[Measurements CSV ↓](https://phishdestroy.github.io/TgWitness/validation/audit/MEASUREMENTS.csv)[Python verifier ↓](https://phishdestroy.github.io/TgWitness/validation/audit/VERIFY.py)[File checksums ↓](https://phishdestroy.github.io/TgWitness/validation/audit/SHA256SUMS.txt)

The signature protects the report against alteration. It does not independently attest the measurements or certify GDPR compliance. The report records the completed audit at 19:08 UTC; the infrastructure snapshot above was taken earlier.

**Source receipt digests**

These hashes identify retained receipts. A hash alone does not prove the measurements; the private originals are not downloadable from this page.

- benchmark-1.json`66cdf2db25901ee1f780a0e2d14b9b84888dbe525bff73bae19819b217f95d0c`
- benchmark-2.json`ad2978fe2a7563476da43293eaaf5f498ee12522f0ea3e401bc43205c64874d1`
- test-totals.json`922cf87d9320b149f2fc6791fc05f98335ec0952f9258e6eaeff179aeef33bb1`
- infra-summary.json`325d390ef752b15f44203f97348863e24f0f631fe88998d5e1f398a5311a9339`

The page is a snapshot, not a claim that every function or account has been tested. Absence of a measurement is shown explicitly.
