# কি পরীক্ষা করা হয়েছে

Canonical page: https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/

লাইভ টেলিগ্রাম পরীক্ষা, স্বয়ংক্রিয় যাচাইকরণ, ব্রাউজার যাচাইকরণ এবং যা যাচাই করা যায়নি।

[টিজিউইটনেস](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [ডকুমেন্টেশন](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/bn/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Updated 6 November 2026.** Results are tied to the revision, environment and workload recorded for each run. [Current capabilities](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describes the available workflows; this page records what has actually been checked.

[Performance graphs](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Signed English audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Downloadable measurements](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Latest evidence | ফলাফল | পরিধি |
| --- | --- | --- |
| Release audit · 6 Nov | 1,461 core tests passed; 37 platform skips | Source `92e539af40d8`; open findings retained |
| Fresh exports · 6 Nov | 127.713 and 141.781 records/s, complete cycle | Two accounts per server; text and metadata through WARP |
| Retained archives · 6 Nov | 48 archives; 3,598,381 records verified | Existing archives checked against pinned workspace keys |
| Trusted Live · 5 Nov | Guarded CPU recording and WARP checks | Official Desktop login and native export remain unqualified |
| Phala / Intel TDX · 4 Nov | All 16 verifier checks passed on later runs | Historical deployment; no Telegram account on the CVM |

**On this page**

- [Release audit and fresh exports · 6 November 2026](https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu and WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live Phala Cloud deployment · 4 November 2026](https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Live server journal inventory · 1 November 2026](https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Recent offline and fault-injection checks · 1 November 2026](https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live Telegram test, whole account · 29 October 2026](https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Password-protected export opened with libarchive · 29 October 2026](https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live Telegram test · 27 to 29 October 2026](https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetic local capacity measurement](https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Full-text search on one million messages · 5 November 2026](https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Remaining qualification](https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/#remaining-qualification)

## Release audit and fresh exports · 6 November 2026

The audit used v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. Installed-package smoke checks passed on three servers. The signed report retains the state observed at that time.

[![Acquisition and complete export rates for two fresh workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Workload | রেকর্ডসমূহ | Acquisition | Complete cycle | Complete-cycle rate |
| --- | --- | --- | --- | --- |
| Server A · two accounts | 27,030 | 189.043 s | 211.647 s | 127.713 records/s |
| Server B · two accounts | 29,299 | 182.513 s | 206.650 s | 141.781 records/s |

Both exports began without resume, excluded attachments and avatars, and ended with zero duplicate or reused records. The complete cycle includes preparation, acquisition, selection, packaging and archive verification. Server A also ran a protected-chat read check. Four FloodWait events on A and three on B were respected. These observations do not establish a general throughput guarantee.

| যাচাই করুন | ফলাফল | Qualification |
| --- | --- | --- |
| Core pytest | 1,461 passed | 37 platform skips |
| Browser / browser UX / evidence / site | 102 / 66 / 15 / 9 passed | These programs overlap other tests; counts are not additive |
| Capture addon | 124 passed | Three Official Web checks blocked by the required Chromium sandbox |
| API authorization | 269 routes; 538 requests passed | Missing credentials and revoked access |
| Retained archives | 48 of 48 verified | 3,598,381 records; pinned workspace keys |
| Live fleet read checks | 24 of 40 profiles passed | 16 WARP routes failed qualification; those profiles were not connected |

The [signed report](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) records all open findings, including three defects in an unpublished secret-chat snapshot absent from the audited main build. The earlier [public-history qualification](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) used a different revision and workload; its rates must not be combined with this comparison.

Verify the original report using the [pinned key and verifier](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Its signature protects the operator's report from alteration. It is not independent attestation, proof of Telegram authorship or GDPR certification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## লাইভ ফালা ক্লাউড ডিপ্লয়মেন্ট · ৪ নভেম্বর ২০২৬

**Historical result:** later deployments passed all 16 verifier checks, including Intel TDX and the quick tunnel. Restart evidence, signed address discovery and report timestamps were checked separately. Each test CVM was removed after its run.

| সেটআপ | Recorded value |
| --- | --- |
| প্রদানকারী | Phala Cloud · `tdx.small` · US-WEST-1 |
| নিয়োগ | `--provider phala --quick-tunnel`; initially empty workspace |
| Initial collector | `df7d860c` · v0.8.1 |
| Collector with all fixes | `53a0f7e9` |
| Production guest | `dstack-0.5.12`; SSH access disabled |
| External services | ntfy.sh, GitHub and Intel PCS |
| Observed cost | Seven CVMs, about 1.9 US cents together; historical test pricing |

The sequence below separates initial failures, fixes and completed checks. No Telegram account was connected to these CVMs.

**Deployments 1–2 · provider differences and regression checks**

প্রথম দুইটি ডিপ্লয়মেন্ট সিমুলেটেড Phala Cloud থেকে পাঁচটি পার্থক্য খুঁজে পেয়েছিল। [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) এখন প্রতিটি পুনরুত্পাদন করে, এবং এর ফিক্স ছাড়া ব্যর্থ হয়:

| Phala Cloud-এ | মরামতির আগে | ফিক্স |
| --- | --- | --- |
| `compose_file.name` প্রয়োজন | HTTP 422, কিছুই তৈরি হয়নি | Docker Compose কনফিগারেশন CVM-এর নাম বহন করে |
| যদি খালি কোনোটি না দেওয়া হয়, Phala তার নিজস্ব প্রি-লঞ্চ স্ক্রিপ্ট পরিমাপিত app-compose-এ যোগ করে (v0.0.20: Docker লগইন, `docker compose pull`, রুট পাসওয়ার্ড, SSH কী `user_config` থেকে) | `tdx_compose` ব্যর্থ হয়: প্রকাশিত Docker Compose কনফিগারেশনের বাইরে কোড | app-compose `pre_launch_script`-কে `""`-এ সেট করে; Phala তারপর এটি বাদ দেয় |
| `image` ছাড়া Phala `dstack-dev-0.5.12`, ডেভেলপমেন্ট বিল্ড, SSH অ্যাক্সেস সক্ষম সহ বেছে নেয় | `server_state` ব্যর্থ হয়েছে। শুধুমাত্র হার্ডওয়্যার অ্যাটেস্টেশন রেকর্ড এই ইমেজে পাস হয়েছে; শুধুমাত্র প্রদানকারী রেকর্ড এবং `tdx_os` এটি দেখায়। | ডিপ্লয়মেন্ট Phala-এর বর্তমান রিলিজ, `dstack-0.5.12`-এর প্রোডাকশন বিল্ড চায়। |
| dstack গেটওয়ে বন্ধ থাকায়, CVM বিবরণে কখনই `instance_id` পাওয়া যায় না। | ডিপ্লয় ৩০ মিনিট অপেক্ষা করে এবং ব্যর্থ হয় | ইনস্ট্যান্স আইডি CVM-এর অবস্থা থেকে পড়া হয় |
| রিস্টার্ট, স্টপ এবং স্টার্ট হল CVM অপারেশন, অ্যাপ্লিকেশন রিভিশনের নয়। | `provider_actions` রিস্টার্ট তালিকাভুক্ত করেনি | অপারেশনগুলোও পড়া হয় |

**Deployment 3 · attestation, access checks and restart evidence**

- CVM SSH অ্যাক্সেস বন্ধ রেখে `dstack-0.5.12` চালিয়েছিল। কালেক্টর তৈরি হওয়ার প্রায় ১.৫ মিনিট পর তার স্বাক্ষরিত ঠিকানা পোস্ট করেছিল। Deploy তারপর `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, হার্ডওয়্যার অ্যাটেস্টেশন রেকর্ড v4, FMSPC `20a06f000000`, ডিবাগ মোডে নেই, স্থানান্তরযোগ্য নয়, Intel থেকে প্রাপ্ত ক্রিপ্টোগ্রাফিক যাচাইকরণ ডেটা সমর্থন করে `tdx_compose_hash`, `tdx_compose` (বাইট অনুযায়ী) এবং `tdx_identity` (KMS কী)।
- trycloudflare.com ঠিকানায় প্যানেল টোকেন ছাড়া বা ভুল টোকেন দিয়ে 401 উত্তর দিয়েছে, এবং প্যানেল টোকেন দিয়ে 200।
- `verify`, যেখানে `--source` কমিটের GitHub আর্কাইভে সেট করা হয়েছিল এবং ফিঙ্গারপ্রিন্ট আলাদাভাবে পাঠানো হয়েছিল: সার্ভার, `server_state`, ফায়ারওয়াল (কোনো গেটওয়ে নেই, কোনো পাবলিক এন্ডপয়েন্ট নেই), প্রদানকারী লগ, স্টেটমেন্ট, ফিঙ্গারপ্রিন্ট, সোর্স হ্যাশ, বুট এবং পাঁচটি `tdx_*` চেক পাস হয়েছে। Cloudflare এবং `tdx_os` অনুপলব্ধ ছিল, তাই ফলাফল অসম্পূর্ণ ছিল।
- Phala-এর API-র মাধ্যমে দুইবার রিস্টার্ট: প্রতিবার CVM দুই মিনিটের মধ্যে ফিরে আসত একই কালেক্টর কী, একটি নতুন স্বাক্ষরিত ঠিকানা, এবং পুরনো ঠিকানা 530 উত্তর দিচ্ছিল। `verify` নতুন বুট এবং উভয় রিস্টার্টকে REVIEW হিসেবে রিপোর্ট করেছিল। `--evidence`-এর মাধ্যমে জার্নাল স্বাক্ষর এবং তিনটি স্টার্ট নিশ্চিত করা হয়েছে, প্রত্যেকটি একই CVM থেকে নিজস্ব Intel TDX হার্ডওয়্যার অ্যাটেস্টেশন রেকর্ডসহ।
- `destroy` শুধুমাত্র সেই CVM-টি মুছে ফেলেছে। এরপর ওয়ার্কস্পেস ফাঁকা হয়ে যায়, এবং প্যানেলের ঠিকানা সাড়া দেওয়া বন্ধ করে দেয়।
- প্যানেল উইজার্ডের মূল্য যাচাইয়ে `tdx.small` প্রতি ঘণ্টায় $0.058 দেখিয়েছে। একটি ভুল কী-তে একটি সাধারণ "API কী গ্রহণ করা হয়নি" বার্তা এসেছে।

**Follow-up fixes · signed address discovery and OS measurements**

- ঠিকানা কী ছাড়া, `verify` ঠিকানা বিষয়ের সর্বশেষ সুগঠিত পোস্টটি অনুসরণ করেছিল, যা প্রকাশিত Docker Compose কনফিগারেশনে মুদ্রিত আছে। একটি জাল পোস্ট এটিকে এমন একটি হোস্টে পাঠিয়েছিল যা বিদ্যমান নেই, এবং `statement` ব্যর্থ হয়েছিল: একজন জালকারী সংগ্রাহক হিসেবে নিজেকে চালাতে পারেনি, তবে ব্লক করতে পারত তৃতীয় পক্ষের যাচাইকরণ, সর্বোচ্চ ১২ ঘণ্টা পর্যন্ত একটি জাল ভবিষ্যতের টাইমস্ট্যাম্প সহ। কালেক্টর এখন তার ঠিকানাটি নিজের কী দিয়ে স্বাক্ষরিত অবস্থায় পোস্ট করে, `verify` শুধুমাত্র তখনই এমন পোস্টগুলো গ্রহণ করে যখন সেগুলো কালেক্টর নিজে করে, এবং পোস্টগুলো ntfy.sh-এর প্রাপ্তির সময় অনুযায়ী সাজানো হয়। [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) জাল পোস্টগুলো পুনরায় চালায়। একটি CVM এটিকে শুধুমাত্র সেই কমিট থেকে চালায় যাতে এটি থাকে, তাই এই রানের কালেক্টর এখনও তার ঠিকানায় স্বাক্ষর করেনি এবং `verify` তাই বলেছে।
- `tdx_os` `dstack-mr` ছাড়া চলতে পারেনি, যার বর্তমান সংস্করণে ডকুমেন্টেশনে উল্লেখিত `measure --json`-এর পরিবর্তে `measure-os` রয়েছে। যাচাইকারী এখন প্রকাশিত ইমেজ এবং VM-এর আকৃতি (ACPI টেবিলসহ) থেকে নিজেই MRTD এবং RTMR0-2 গণনা করে।

**Deployment 4 · all 16 checks, report seals and restart verification**

- Deploy প্রকাশিত `dstack-0.5.12` একবার ডাউনলোড করল, CVM রিপোর্টকৃত OS ইমেজ হ্যাশের সাথে মিলিয়ে দেখল, এবং `tdx_os` পাস করল: MRTD, RTMR0, RTMR1 এবং RTMR2 QEMU-এর জন্য গণনা করা মানগুলোর সমান। ৮.২.২, ১ vCPU এবং ২ GiB। একই গণনা দাবি করা ৪ GiB, ২ vCPU, QEMU 9.2.1 বা দ্বিতীয় নেটওয়ার্ক কার্ডের জন্য ভিন্ন RTMR0 দিয়েছে, এবং পরিবর্তিত কার্নেল, ফার্মওয়্যার বা কমান্ড লাইন এবং ডেভেলপমেন্ট ইমেজের জন্য ব্যর্থ হয়েছে।
- `verify` তার ১৬টি চেকের প্রত্যেকটি পাস করেছে, দ্রুত টানেলের সংযোগকারী সহ, তাই ফলাফল ছিল PASS। এটি HTML এবং PDF সার্টিফিকেট তৈরি করেছে, যা স্বাক্ষর এবং টাইমস্ট্যাম্প দিয়ে ডিজিটালি সিল করা হয়েছে, যার মধ্যে রয়েছে বেলজিয়াম সরকারের টাইমস্ট্যাম্পিং ইউনিট TSU 202301 (বেলজিয়ামের ট্রাস্টেড লিস্টে গ্রান্টেড স্ট্যাটাস) থেকে প্রাপ্ত একটি যোগ্য eIDAS টাইমস্ট্যাম্প, একটি FreeTSA টাইমস্ট্যাম্প এবং ভেরিফায়ারের স্বাক্ষর; `check-report` এগুলো এবং PDF-এর স্বাক্ষর সবই নিশ্চিত করেছে।
- পুনঃশুরু করার পর, `verify --evidence` দুটি শুরু নিশ্চিত করেছে, প্রতিটি CVM-এর ভিতরে তৈরি হওয়া হার্ডওয়্যার অ্যাটেস্টেশনের সাথে এবং প্রতিটি প্রকাশিত `dstack-0.5.12` থেকে বুট করা হয়েছে; পুনঃশুরু এবং নতুন বুট REVIEW ছিল।
- `destroy` ওয়ার্কস্পেস ফাঁকা রেখেছে।

**Deployment 5 · collector-signed discovery and forged-post rejection**

The collector ran from commit `53a0f7e9`, which includes the fixes above.

- কলেক্টর তার নিজস্ব কী দিয়ে স্বাক্ষরিত ঠিকানাটি অপারেটরের HMAC পোস্টের পাশে পোস্ট করল। তারপর টপিকে দুটি জাল পোস্ট যোগ করা হল, একটি শূন্য HMAC সহ এবং অন্যটি অন্য একটি Ed25519 কী দিয়ে স্বাক্ষরিত, উভয়ই ২০৯৬ সালের একটি সময় দাবি করছে। `verify` কালেক্টর কী দ্বারা স্বাক্ষরিত ঠিকানাটি গ্রহণ করে এবং সব ১৬টি যাচাই সফলভাবে সম্পন্ন করে; সীলটিতে আবার যোগ্য বেলজিয়ান টাইম স্ট্যাম্প, FreeTSA-এর টাইম স্ট্যাম্প এবং যাচাইকারীর স্বাক্ষর ছিল, এবং `check-report` সেগুলো নিশ্চিত করে।
- পুনঃশুরু করার পর কালেক্টর স্বাক্ষরিত নতুন ঠিকানা পোস্ট করল: `verify` তা সঙ্গে সঙ্গেই খুঁজে পেল, অপারেটরের **বর্তমান ঠিকানা খুঁজে পেল** HMAC পোস্টের ২৭ সেকেন্ড পর, এবং উভয়েই জাল পোস্টগুলো উপেক্ষা করল। `verify --evidence` নিশ্চিত করল যে দুইটি স্টার্ট `dstack-0.5.12` থেকে বুট হয়েছে।
- Deploy প্রিন্ট করেছে Phala CVM-কে কী বিল করে, ডিস্ক সহ: প্রতি ঘণ্টায় $0.06078।

### Panel wizard and remaining scope

প্যানেল উইজার্ড Phala Cloud-এ দুইবার চালানো হয়েছিল, একবার এর জব API-এর মাধ্যমে এবং একবার একটি প্রকৃত Chromium-সহ ব্রাউজারের মাধ্যমে: মূল্য যাচাই, **Advanced**-এর অধীনে commit-সহ তৈরি, সব ছয়টি attestation যাচাই পাস, সার্ভার তালিকা বিল করা মূল্য (মাসে 44.37 USD) দেখিয়েছিল, **বর্তমান ঠিকানা খুঁজে বের করা**, পরিমাপকৃত Docker Compose কনফিগারেশন ডাউনলোড, এবং মুছে ফেলা। ব্রাউজারে কোনো পৃষ্ঠা ত্রুটি দেখা যায়নি। প্রতিবার পরবর্তীতে ওয়ার্কস্পেস খালি ছিল।

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation. All prices in this section were observed on 4 November 2026.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | গণুন |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| যাচাই করুন | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## লাইভ টেলিগ্রাম পরীক্ষা, সম্পূর্ণ অ্যাকাউন্ট · ২৯ অক্টোবর ২০২৬

নীচের পরীক্ষায় একই অ্যাকাউন্ট চলতেই থাকল। ২৯ অক্টোবর ১২:১০ UTC-এ এর পরিধি পুরো অ্যাকাউন্টে (চ্যানেল, গ্রুপ, ব্যক্তিগত চ্যাট এবং বট) পরিবর্তন করা হয়; প্যানেল নিশ্চিতকরণের জন্য অনুরোধ করেছিল এবং স্বাক্ষরিত জার্নালে তা রেকর্ড করা হয়েছিল। ১৭:৫৯ UTC-এ জার্নালে ছিল:

| রেকর্ড করা হয়েছে, ২৭ অক্টোবর ২১:৩৬ থেকে ২৯ অক্টোবর ১৭:৫৯ ইউটিসি | গণুন |
| --- | --- |
| জার্নাল রেকর্ডসমূহ | 9,968 |
| নতুন বার্তা | 5,308 |
| পুরো অ্যাকাউন্টে স্যুইচ করার পর তাদের | 3,878 |
| মোছা | 784 |
| TgWitness বার্তাটি সংরক্ষণ করার পর সেগুলো মুছে ফেলা হয়েছিল। | 596 |
| সম্পাদনাগুলি | 41 |
| পুনঃপরীক্ষার মাধ্যমে যোগ করা বার্তাগুলি | 2,273 |
| বার্তাগুলো আর খুঁজে পাওয়া গেল না | 18 |
| ইতিহাসের স্ন্যাপশট দ্বারা সংরক্ষিত বার্তা | 242 |
| সংরক্ষিত সংযুক্তিগুলি | 247 |
| সংগ্রাহক শুরু করে | 19 |
| টেলিগ্রাম ফ্লাড অপেক্ষা করছে | 26 |

- প্যানেলের **Verify** চেক সমস্ত ৯,৯৬৮ রেকর্ডের স্বাক্ষর এবং হ্যাশ চেইন নিশ্চিত করেছে।
- বার্তাগুলো দুইটি গ্রুপ বা চ্যানেল এবং তিনটি ব্যক্তিগত চ্যাট ও বট থেকে এসেছে। একটি বার্তা বোতাম **চ্যাটস** থেকে চাপানো হয়েছিল; অনুরোধ এবং টেলিগ্রামের উত্তর জার্নালে রয়েছে।
- যখন কালেক্টর রিস্টার্টের পর অ্যাকাউন্টটি পুনরায় স্ক্যান করেছিল, তখন নতুন চ্যাটগুলো যোগ করা হয়েছিল। নতুন চ্যাটগুলোর পূর্ববর্তী বার্তা সংরক্ষণ বন্ধ ছিল (`history = 0`), তাই এখানে তা অন্তর্ভুক্ত করা হয়নি।

অন্তর্ভুক্ত নয়: প্রতিক্রিয়া, সদস্যপদ পরিবর্তন, ব্যক্তি প্রোফাইল, বার্তা পাঠানো, আমন্ত্রণের মাধ্যমে যোগদান, প্রক্সি, বিজ্ঞপ্তি, উইটনেস বট এবং একযোগে একাধিক অ্যাকাউন্ট। পাবলিক ফাইলগুলোতে শুধুমাত্র গণনা থাকে।

## পাসওয়ার্ড-সুরক্ষিত রপ্তানি libarchive দিয়ে খোলা হয়েছে · ২৯ অক্টোবর ২০২৬

রপ্তানি এনক্রিপশন কোড (WinZip AES-256, যা 7-Zip এবং WinRAR ফরম্যাট পড়ে) দ্বারা লেখা একটি আর্কাইভ Windows `tar` (bsdtar 3.6.2, libarchive) দিয়ে খোলা হয়েছিল। সঠিক পাসওয়ার্ডে এক্সট্র্যাক্ট করা ফাইলের SHA-256 মূলটির সাথে মিলল; ভুল পাসওয়ার্ডে "Incorrect passphrase" দেখিয়ে প্রত্যাখ্যাত করা হয়েছিল। 7-Zip এবং WinRAR নিজেই চালানো হয়নি।

## লাইভ টেলিগ্রাম পরীক্ষা · ২৭ থেকে ২৯ অক্টোবর ২০২৬

একটি আসল টেলিগ্রাম অ্যাকাউন্ট, বিল্ট-ইন API পেয়ার পুলের মাধ্যমে সাইন ইন করা, **২৭ অক্টোবর ২১:৩৬ UTC** থেকে **২৯ অক্টোবর ০৫:১৫ UTC পর্যন্ত** একটি সুপারগ্রুপ রেকর্ড করেছে। ওই সময়কালে কালেক্টরটি ১২ বার চালু করা হয়েছিল।

| রেকর্ড করা হয়েছে | গণুন |
| --- | --- |
| জার্নাল রেকর্ডসমূহ, যার মধ্যে হার্টবিট এবং সার্ভিস রেকর্ডসমূহ অন্তর্ভুক্ত | 2,385 |
| নতুন বার্তা | 1,291 |
| মোছা | 472 |
| TgWitness টেক্সটটি সংরক্ষণ করার পর সেগুলো মুছে ফেলা হয়েছিল। | 347 |
| সম্পাদনাগুলি | 12 |
| বন্ধ থাকা অবস্থায় মিস হওয়া বার্তাগুলো পুনরায় যাচাইকরণে যোগ করা হয়েছে। | 12 |
| সংরক্ষিত সংযুক্তিগুলি | 17 |
| সংযুক্তিগুলি ডাউনলোড হয়নি (ডাউনলোড বন্ধ, অথবা ডাউনলোডের কোনো ফাইল নেই) | 14 |
| টেলিগ্রাম ফ্লাড: পুনঃযাচাইয়ের সময় প্রতিবার ৩ সেকেন্ড করে বিরতি দেয়। | 8 |

- সকল ২,৩৮৫টি রেকর্ডের স্বাক্ষর এবং হ্যাশ চেইন জার্নালের পাবলিক কী-র বিরুদ্ধে যাচাই করা হয়।
- পুনঃশুরু করার পর কালেক্টর সংরক্ষিত আপডেট অবস্থা (`pts`) থেকে পুনরায় শুরু করে এবং Telethon পিছিয়ে থাকা মেসেজগুলো ধরতে থাকে; পুনঃপরীক্ষা তখন এখনও অনুপস্থিত মেসেজগুলো যোগ করে।
- প্রতিটি FloodWait-এ কালেক্টর অনুরোধকৃত সময় অপেক্ষা করল এবং চালিয়ে গেল।
- অ্যাকাউন্টটি সাইন ইন অবস্থায়ই ছিল, এবং একই সেশন ২৯ অক্টোবর পুনরায় সংযুক্ত হয়েছিল।

এই পরীক্ষায় অন্তর্ভুক্ত নয়: একযোগে একাধিক অ্যাকাউন্ট, প্রশাসক ভূমিকা, প্রক্সি, কয়েক ঘণ্টার বেশি সময়ের আউটেজ এবং সম্পূর্ণ [লাইভ গ্রহণ প্রক্রিয়া](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)। পাবলিক ফাইলগুলিতে শুধুমাত্র এই গণনাগুলি রয়েছে: কোনো অ্যাকাউন্ট বা চ্যাট আইডেন্টিফায়ার, বার্তা বা শংসাপত্র নেই।

## কৃত্রিম স্থানীয় সক্ষমতা পরিমাপ

কমান্ড: `python tools/check_capacity.py --events 10000 --chats 100`

| মিটারিক | পর্যবেক্ষিত |
| --- | --- |
| ইনপুট | ১০০টি সিন্থেটিকভাবে নির্বাচিত উৎসের মধ্যে ১০,০০০টি সিন্থেটিক বার্তা ইভেন্ট |
| বার্তার পাঠ্য | ৪০০ অক্ষর; কোনো মিডিয়া বা নেটওয়ার্ক নেই |
| সেবন | ৫৩.২৭৩ সেকেন্ড; ১৮৭.৭ ইভেন্ট/সেকেন্ড |
| হ্যান্ডলার ল্যাটেন্সি | p50 4.162 ms; p95 7.784 ms; সর্বোচ্চ 129.118 ms |
| ZIP রপ্তানি | ট্র্যাসম্যালক সক্রিয় অবস্থায় ১৯.৮৬৮ সেকেন্ড |
| শীর্ষ ট্রেসকৃত পাইথন রপ্তানি বরাদ্দ | 0.51 MiB; প্রক্রিয়া RSS নয় |
| ZIP আকার | ৪,৬১০,৯৬২ বাইট |
| স্বতন্ত্র যাচাইকরণ | সমস্ত ১০,০০০টি ইভেন্ট যাচাই করা হয়েছে |

এটি এই Windows হোস্টে স্থানীয় সিরিয়াল রেকর্ডিং/রপ্তানি পথ পরিমাপ করে। এটি MTProto ডেলিভারি, সমান্তরাল অ্যাকাউন্ট, টেলিগ্রাম থ্রটলিং, মিডিয়া, দীর্ঘমেয়াদী ওয়ার্কলোড বা নিশ্চিত সংখ্যক বাস্তব চ্যাট পরিমাপ করে না। এই পরিমাপটি চূড়ান্ত অফলাইন টাইমস্ট্যাম্প টুলিং-এর আগে করা হয়েছে, যা পরিমাপকৃত মেসেজ পথ পরিবর্তন করে না।

## এক মিলিয়ন বার্তায় পূর্ণ-পাঠ অনুসন্ধান · ৫ নভেম্বর ২০২৬

কমান্ড: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

২০০টি চ্যাটে ১,০০০,০০০টি সিন্থেটিক মেসেজের একটি নির্ধারিত স্বাক্ষরিত জার্নাল (রাশিয়ান শব্দরূপ, ইউক্রেনীয়, ইংরেজি, চীনা, জাপানি, লিঙ্ক এবং হ্যান্ডেল) ৭১ সেকেন্ডে সূচিবদ্ধ হয়েছে; জার্নালটির সাথে ১.৫০ জিবি জার্নালের জন্য ৫৮ MiB ইনডেক্স ব্যবহার করা হয়েছে। সেরা-মিলন অনুসন্ধানগুলি 9 থেকে 190 ms (মাধ্যক) সময় নিয়েছে, যেখানে পূর্ববর্তী সাবস্ট্রিং অনুসন্ধানে 2.4 থেকে 3.2 সেকেন্ড সময় লাগত। সম্পূর্ণ ফলাফল, হার্ডওয়্যার এবং সীমা: [পূর্ণ-পাঠ অনুসন্ধান](https://phishdestroy.github.io/TgWitness/bn/docs/reference/search/#benchmark)। `tools/test_fulltext.py` এছাড়াও পূর্ণ-পাঠ অনুসন্ধানের আগে তৈরি একটি স্বাক্ষরিত আর্কাইভ যাচাই করে (`tools/fixtures/evidence-before-fulltext.zip`) বর্তমান যাচাইকারী দিয়ে যাচাই করে, এবং সেই আর্কাইভের নিজস্ব দিয়ে একটি বর্তমান আর্কাইভ `verify.py`.

## বাকী যোগ্যতা

সংরক্ষিত লাইভ জার্নাল প্রকৃত সংগ্রহ, সম্পাদনা, মুছে ফেলার বিজ্ঞপ্তি, সংযুক্তি, পুনঃপরীক্ষা এবং রেট-লিমিট হ্যান্ডলিং প্রতিষ্ঠা করে। এটি সম্পূর্ণ ডেলিভারি বা ভূমিকা দৃশ্যমানতা, প্রতিক্রিয়াশীল অভিনেতারা, দীর্ঘায়িত FloodWait, অ্যাকাউন্ট নিষেধাজ্ঞা এবং নেটওয়ার্ক/প্রক্রিয়া বিঘ্ন পুনরুদ্ধারের নিয়ন্ত্রিত ম্যাট্রিক্স প্রতিষ্ঠা করে না। QR-টোকেন ইস্যু সম্পূর্ণ মোবাইল QR নিশ্চিতকরণের থেকে পৃথক।

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

The [public audit directory](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) contains only the signed report and aggregate measurements. Detailed operational receipts, raw captures and account material remain private. Application screenshots in `docs/assets/` use fictional demonstration data.
