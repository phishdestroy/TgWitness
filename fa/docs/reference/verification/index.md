# آنچه آزمایش شده است

Canonical page: https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/

آزمون زنده تلگرام، بررسی‌های خودکار، بررسی‌های مرورگر و آنچه هنوز تأیید نشده است.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [مستندسازی](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Updated 6 November 2026.** Results are tied to the revision, environment and workload recorded for each run. [Current capabilities](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describes the available workflows; this page records what has actually been checked.

[Performance graphs](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Signed English audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Downloadable measurements](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Latest evidence | نتیجه | دامنه |
| --- | --- | --- |
| Release audit · 6 Nov | 1,461 core tests passed; 37 platform skips | Source `92e539af40d8`; open findings retained |
| Fresh exports · 6 Nov | 127.713 and 141.781 records/s, complete cycle | Two accounts per server; text and metadata through WARP |
| Retained archives · 6 Nov | 48 archives; 3,598,381 records verified | Existing archives checked against pinned workspace keys |
| Trusted Live · 5 Nov | Guarded CPU recording and WARP checks | Official Desktop login and native export remain unqualified |
| Phala / Intel TDX · 4 Nov | All 16 verifier checks passed on later runs | Historical deployment; no Telegram account on the CVM |

**On this page**

- [Release audit and fresh exports · 6 November 2026](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu and WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live Phala Cloud deployment · 4 November 2026](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Live server journal inventory · 1 November 2026](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Recent offline and fault-injection checks · 1 November 2026](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live Telegram test, whole account · 29 October 2026](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Password-protected export opened with libarchive · 29 October 2026](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live Telegram test · 27 to 29 October 2026](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetic local capacity measurement](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Full-text search on one million messages · 5 November 2026](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Remaining qualification](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/#remaining-qualification)

## Release audit and fresh exports · 6 November 2026

The audit used v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. Installed-package smoke checks passed on three servers. The signed report retains the state observed at that time.

[![Acquisition and complete export rates for two fresh workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Workload | ثبت می‌کند | Acquisition | Complete cycle | Complete-cycle rate |
| --- | --- | --- | --- | --- |
| Server A · two accounts | 27,030 | 189.043 s | 211.647 s | 127.713 records/s |
| Server B · two accounts | 29,299 | 182.513 s | 206.650 s | 141.781 records/s |

Both exports began without resume, excluded attachments and avatars, and ended with zero duplicate or reused records. The complete cycle includes preparation, acquisition, selection, packaging and archive verification. Server A also ran a protected-chat read check. Four FloodWait events on A and three on B were respected. These observations do not establish a general throughput guarantee.

| بررسی | نتیجه | Qualification |
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

## راه‌اندازی زنده Phala Cloud · ۴ نوامبر ۲۰۲۶

**Historical result:** later deployments passed all 16 verifier checks, including Intel TDX and the quick tunnel. Restart evidence, signed address discovery and report timestamps were checked separately. Each test CVM was removed after its run.

| راه‌اندازی | Recorded value |
| --- | --- |
| ارائه‌دهنده | Phala Cloud · `tdx.small` · US-WEST-1 |
| استقرار | `--provider phala --quick-tunnel`; initially empty workspace |
| Initial collector | `df7d860c` · v0.8.1 |
| Collector with all fixes | `53a0f7e9` |
| Production guest | `dstack-0.5.12`; SSH access disabled |
| External services | ntfy.sh, GitHub and Intel PCS |
| Observed cost | Seven CVMs, about 1.9 US cents together; historical test pricing |

The sequence below separates initial failures, fixes and completed checks. No Telegram account was connected to these CVMs.

**Deployments 1–2 · provider differences and regression checks**

دو استقرار اول پنج تفاوت را از Phala Cloud شبیه‌سازی‌شده پیدا کردند. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) اکنون هر یک را بازتولید می‌کند و بدون اصلاح خود با شکست مواجه می‌شود:

| در Phala Cloud | قبل از رفع مشکل | رفع مشکل |
| --- | --- | --- |
| `compose_file.name` مورد نیاز است | HTTP 422، هیچ چیزی ایجاد نشد | پیکربندی Docker Compose نام CVM را حمل می‌کند |
| مگر اینکه یک مقدار خالی داده شود، Phala اسکریپت پیش از راه‌اندازی خود را به app-compose اندازه‌گیری‌شده اضافه می‌کند (نسخه 0.0.20: ورود به داکر، `docker compose pull`، رمز عبور ریشه، کلیدهای SSH از `user_config`) | `tdx_compose` شکست می‌خورد: کد خارج از پیکربندی منتشرشده Docker Compose | app-compose مقدار `pre_launch_script` را روی `""` تنظیم می‌کند؛ Phala سپس آن را نادیده می‌گیرد |
| بدون `image`، Phala، `dstack-dev-0.5.12`، نسخه توسعه را با دسترسی SSH فعال‌شده انتخاب می‌کند. | `server_state` شکست می‌خورد. تنها رکورد گواهی سخت‌افزاری در این تصویر تأیید شد؛ فقط رکورد ارائه‌دهنده و `tdx_os` آن را نشان می‌دهند. | راه‌اندازی، ساخت نسخه تولید (production build) از آخرین نسخه Phala، `dstack-0.5.12` را درخواست می‌کند. |
| با غیرفعال بودن دروازه dstack، جزئیات CVM هرگز مقدار `instance_id` را دریافت نمی‌کند. | استقرار ۳۰ دقیقه منتظر می‌ماند و با شکست مواجه می‌شود | شناسه نمونه از وضعیت CVM خوانده می‌شود. |
| راه‌اندازی مجدد، توقف و راه‌اندازی، عملیات CVM هستند، نه بازنگری‌های برنامه. | `provider_actions` راه‌اندازی مجددها را فهرست نکرد. | عملیات خواندن نیز در نظر گرفته می‌شوند |

**Deployment 3 · attestation, access checks and restart evidence**

- CVM با `dstack-0.5.12` و دسترسی SSH غیرفعال اجرا شد. کالکتور حدود ۱.۵ دقیقه پس از ایجاد، آدرس امضا شده خود را ارسال کرد. سپس Deploy، `tdx_binding` و `tdx_quote` (Intel TCB UpToDate، رکورد گواهی سخت‌افزار v4، FMSPC `20a06f000000`، در حالت اشکال‌زدایی نیست، قابل مهاجرت نیست، پشتیبانی از داده‌های تأیید رمزنگاری استخراج‌شده از اینتل)، `tdx_compose_hash`، `tdx_compose` (بایت به بایت) و `tdx_identity` (کلیدهای KMS).
- پنل در آدرس trycloudflare.com خود، بدون توکن یا با توکن اشتباه، پاسخ ۴۰۱ و با توکن پنل، پاسخ ۲۰۰ داد.
- `verify` با `--source` که روی آرشیو گیت‌هابِ کامیت تنظیم شده بود و اثر انگشت به‌صورت جداگانه ارسال شد: سرور، `server_state`، فایروال (بدون گیت‌وی، بدون نقطه پایانی عمومی)، لاگ ارائه‌دهنده، بیانیه، اثر انگشت، هش منبع، بوت و پنج بررسی `tdx_*` با موفقیت انجام شد. Cloudflare و `tdx_os` در دسترس نبودند، بنابراین نتیجه ناقص بود.
- دو بار راه‌اندازی مجدد از طریق API فالا: هر بار که CVM با همان کلید گردآورنده، یک آدرس امضا شده جدید و پاسخ ۵۳۰ از آدرس قدیمی، در کمتر از دو دقیقه بازگشت. `verify` بوت جدید و هر دو راه‌اندازی مجدد را به عنوان REVIEW گزارش کرد. با `--evidence`، امضاهای ژورنال و سه راه‌اندازی تأیید شد، که هر کدام دارای رکورد گواهی سخت‌افزاری Intel TDX مخصوص به خود از همان CVM بودند.
- `destroy` فقط آن CVM را حذف کرد. سپس فضای کاری خالی شد و آدرس پنل دیگر پاسخی نداد.
- بررسی قیمت ویزارد پنل، `tdx.small` را با نرخ ۰.۰۵۸ دلار در ساعت خواند. یک کلید اشتباه، پیام ساده‌ی «کلید API پذیرفته نشد» را دریافت کرد.

**Follow-up fixes · signed address discovery and OS measurements**

- بدون کلید آدرس، `verify` جدیدترین پست صحیح در موضوع آدرس را دنبال کرد، که در پیکربندی منتشر شده Docker Compose چاپ شده است. یک پست جعل‌شده آن را به میزبانی که وجود ندارد فرستاد، و `statement` شکست خورد: یک جعل‌کننده نمی‌توانست خود را به جای گردآورنده جا بزند، اما می‌توانست مسدود کند تأیید شخص ثالث را برای حداکثر ۱۲ ساعت با یک مهر زمانی آینده جعل‌شده انجام می‌دهد. اکنون گردآورنده همچنین آدرس خود را با کلید خودش امضا می‌کند، `verify` فقط چنین پست‌هایی را زمانی که گردآورنده آنها را ارسال می‌کند می‌پذیرد، و پست‌ها بر اساس زمان دریافت ntfy.sh مرتب می‌شوند. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) پست‌های جعل‌شده را مجدداً پخش می‌کند. یک CVM این را فقط از کامیتی که حاوی آن است اجرا می‌کند، بنابراین کلکرکر این اجرا هنوز آدرس خود را امضا نکرده است و `verify` همین را اعلام کرد.
- `tdx_os` بدون `dstack-mr` که نسخه فعلی آن به جای `measure --json` که در مستندات نام برده شده، از `measure-os` استفاده می‌کند، قادر به اجرا نبود. اکنون اعتبارسنج، MRTD و RTMR0-2 را خود از روی ایمیج منتشر شده و شکل VM، شامل جداول ACPI، محاسبه می‌کند.

**Deployment 4 · all 16 checks, report seals and restart verification**

- Deploy یک‌بار `dstack-0.5.12` منتشرشده را دانلود کرد، آن را با هش تصویر سیستم‌عامل که CVM گزارش کرده بود مطابقت داد، و `tdx_os` تأیید شد: MRTD، RTMR0، RTMR1 و RTMR2 با مقادیر محاسبه‌شده برای QEMU یکسان بودند. 8.2.2، 1 vCPU و 2 GiB. همان محاسبه، مقدار متفاوتی برای RTMR0 را برای ادعای 4 GiB، 2 vCPU، QEMU 9.2.1 یا یک کارت شبکه دوم، نشان داد و برای کرنل، فریمور یا خط فرمان تغییر یافته و برای ایمیج توسعه، ناموفق بود.
- `verify` هر ۱۶ بررسی خود را، از جمله کانکتور تونل سریع، با موفقیت پشت سر گذاشت، بنابراین نتیجه PASS بود. این گواهی HTML و PDF را نوشت که با امضاها و مهرهای زمانی، با یک مهر زمانی معتبر eIDAS از واحد زمان‌بندی دولت بلژیک TSU 202301 (وضعیت تأیید شده در لیست مورد اعتماد بلژیک)، یک مهر زمانی FreeTSA و امضای راستی‌آزما، مهر و موم دیجیتال شده بود؛ `check-report` همه آنها و امضای PDF را تأیید کرد.
- پس از راه‌اندازی مجدد، `verify --evidence` دو راه‌اندازی را تأیید کرد، هر یک همراه با گواهی سخت‌افزاری تولیدشده درون CVM و هر یک از `dstack-0.5.12` منتشرشده بوت شده بود؛ راه‌اندازی مجدد و بوت جدید تحت بررسی بودند.
- `destroy` فضای کاری را خالی رها کرد.

**Deployment 5 · collector-signed discovery and forged-post rejection**

The collector ran from commit `53a0f7e9`, which includes the fixes above.

- کلکسیونر آدرس امضا شده با کلید خود را، در کنار پست HMAC اپراتور، منتشر کرد. سپس دو پست جعلی به موضوع اضافه شدند: یکی با HMAC صفر شده و دیگری امضا شده با یک کلید Ed25519 دیگر، که هر دو مدعی زمانی در سال ۲۰۹۶ بودند. `verify` آدرس امضا شده توسط کلید گردآورنده را برداشت و از هر ۱۶ بررسی سربلند بیرون آمد؛ مهر بار دیگر حاوی مهر زمانی معتبر بلژیکی، مهر زمانی FreeTSA و امضای راستی‌آزما بود، و `check-report` آنها را تأیید کرد.
- پس از یک راه‌اندازی مجدد، جمع‌آورنده آدرس جدید امضا شده را ارسال کرد: `verify` آن را بلافاصله پیدا کرد، اپراتور **آدرس فعلی را پیدا کرد** ۲۷ ثانیه بعد از ارسال HMAC، و هر دو ارسال‌های جعل شده را نادیده گرفتند. `verify --evidence` دو راه‌اندازی را که از `dstack-0.5.12` بوت شده بودند تأیید کرد.
- ابزار استقرار چاپ کرد که فالا از CVM چه مبلغی، شامل هزینه دیسک، دریافت می‌کند: $0.06078 در ساعت.

### Panel wizard and remaining scope

ویزارد پنل دو بار روی Phala Cloud اجرا شد، یک بار از طریق API وظیفه آن و یک بار از طریق مرورگر با یک کرومیم واقعی: بررسی قیمت، ایجاد با commit تحت **Advanced**، گذراندن هر شش بررسی احراز هویت، لیست سرور که قیمت صورتحساب شده (۴۴.۳۷ دلار در ماه) را نشان می‌دهد، **Find آدرس فعلی**، دانلود پیکربندی اندازه‌گیری‌شده Docker Compose و حذف آن. مرورگر هیچ خطای صفحه‌ای را مشاهده نکرد. هر بار پس از آن، فضای کاری خالی بود.

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation. All prices in this section were observed on 4 November 2026.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | شمارش |
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

| بررسی | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## آزمایش زنده تلگرام، کل حساب · ۲۹ اکتبر ۲۰۲۶

همان حساب کاربری پس از تست زیر همچنان فعال بود. در ۲۹ اکتبر ساعت ۱۲:۱۰ به وقت جهانی، دامنه آن به کل حساب کاربری (کانال‌ها، گروه‌ها، چت‌های خصوصی و ربات‌ها) تغییر یافت؛ پنل درخواست تأیید کرد و دفترچه ثبت‌شده امضا شده آن را ثبت نمود. تا ساعت ۱۷:۵۹ به وقت جهانی، دفترچه حاوی موارد زیر بود:

| ثبت‌شده، ۲۷ اکتبر ۲۱:۳۶ تا ۲۹ اکتبر ۱۷:۵۹ به وقت جهانی | شمارش |
| --- | --- |
| سوابق دفترچه | 9,968 |
| پیام‌های جدید | 5,308 |
| از آن‌ها پس از تغییر به کل حساب | 3,878 |
| حذف‌ها | 784 |
| از آن‌ها پس از اینکه TgWitness پیام را ذخیره کرده بود، حذف شدند | 596 |
| ویرایش‌ها | 41 |
| پیام‌های اضافه شده توسط بازبینی مجدد | 2,273 |
| پیام‌هایی که دیگر قابل بازیابی نیستند | 18 |
| پیام‌ها با اسنپ‌شات‌های تاریخچه ذخیره می‌شوند | 242 |
| پیوست‌های ذخیره‌شده | 247 |
| شروع جمع‌آوری | 19 |
| Telegram FloodWait مکث می‌کند | 26 |

- بررسی **Verify** پنل، امضاها و زنجیره هش تمام ۹٬۹۶۸ رکورد را تأیید کرد.
- پیام‌ها از ۲ گروه یا کانال و ۳ چت خصوصی و ربات‌ها ارسال شده‌اند. یک دکمه پیام در **چت‌ها** فشرده شد؛ درخواست و پاسخ تلگرام در دفترچه شواهد ثبت شده است.
- چت‌های جدید هنگام اسکن مجدد حساب توسط جمع‌آورنده در هنگام راه‌اندازی مجدد اضافه شدند. ذخیره پیام‌های قبلی چت‌های جدید (`history = 0`) غیرفعال بود، بنابراین در اینجا پوشش داده نشده است.

موارد پوشش داده نشده: واکنش‌ها، تغییرات عضویت، پروفایل افراد، ارسال پیام، پیوستن از طریق دعوت‌نامه، پروکسی‌ها، اعلان‌ها، ربات ویitness و چندین حساب به طور همزمان. فایل‌های عمومی فقط حاوی شمارش هستند.

## خروجی محافظت‌شده با رمز عبور با libarchive باز شد · ۲۹ اکتبر ۲۰۲۶

یک آرشیو که با کد رمزگذاری خروجی (WinZip AES-256، فرمت قابل‌خواندن توسط 7-Zip و WinRAR) نوشته شده بود، با Windows `tar` (bsdtar 3.6.2, libarchive) باز شد. با رمز عبور صحیح، فایل استخراج‌شده با SHA-256 اصلی مطابقت داشت؛ رمز عبور اشتباه با پیام «Incorrect passphrase» (عبارت عبور نادرست) رد شد. خود برنامه‌های 7-Zip و WinRAR اجرا نشدند.

## آزمایش زنده تلگرام · ۲۷ تا ۲۹ اکتبر ۲۰۲۶

یک حساب واقعی تلگرام که از طریق استخر جفت API داخلی وارد شده بود، یک ابرگروه را از **۲۷ اکتبر ساعت ۲۱:۳۶ به وقت جهانی تا ۲۹ اکتبر ساعت ۰۵:۱۵ به وقت جهانی** ضبط کرد. گردآورنده در آن دوره ۱۲ بار راه‌اندازی شد.

| ثبت‌شده | شمارش |
| --- | --- |
| سوابق دفترچه، شامل ضربان‌ها و سوابق سرویس | 2,385 |
| پیام‌های جدید | 1,291 |
| حذف‌ها | 472 |
| از آن‌ها پس از آنکه TgWitness متن را ذخیره کرده بود، حذف شدند | 347 |
| ویرایش‌ها | 12 |
| پیام‌هایی که هنگام توقف از دست رفته‌اند، توسط بازپروژه (recheck) اضافه می‌شوند | 12 |
| پیوست‌های ذخیره‌شده | 17 |
| پیوست‌ها دانلود نشده‌اند (دانلود غیرفعال است، یا فایلی برای دانلود وجود ندارد) | 14 |
| Telegram FloodWait در حین بازبینی مجدد، هر بار به مدت ۳ ثانیه مکث می‌کند | 8 |

- امضاها و زنجیره هش تمام ۲٬۳۸۵ رکورد با کلید عمومی دفترچه تأیید می‌شوند.
- پس از راه‌اندازی مجدد، جمع‌آورنده از وضعیت به‌روزرسانی ذخیره‌شده (`pts`) از سر گرفته می‌شود و Telethon جبران می‌کند؛ سپس بازبینی دوباره پیام‌های هنوز مفقود را اضافه می‌کند.
- در هر FloodWait، گردآورنده به مدت زمان درخواست‌شده صبر کرد و سپس ادامه داد.
- حساب همچنان وارد شده باقی ماند و همان جلسه در ۲۹ اکتبر دوباره متصل شد.

این تست شامل موارد زیر نمی‌شود: چندین حساب به طور همزمان، نقش‌های مدیر، پروکسی‌ها، قطعی‌های طولانی‌تر از چند ساعت و [رویه کامل پذیرش زنده](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). فایل‌های عمومی فقط حاوی این شمارش‌ها هستند: هیچ شناسه حساب یا چت، پیام یا اعتبارنامه‌ای.

## اندازه‌گیری مصنوعی ظرفیت محلی

فرمان: `python tools/check_capacity.py --events 10000 --chats 100`

| متریک | مشاهده‌شده |
| --- | --- |
| ورودی | ۱۰٬۰۰۰ رویداد پیام مصنوعی در ۱۰۰ منبع مصنوعی منتخب |
| متن پیام | ۴۰۰ کاراکتر؛ بدون رسانه یا شبکه |
| ورودی | ۵۳٫۲۷۳ ثانیه؛ ۱۸۷٫۷ رویداد در ثانیه |
| تاخیر پردازشگر | p50 4.162 میلی‌ثانیه؛ p95 7.784 میلی‌ثانیه؛ حداکثر 129.118 میلی‌ثانیه |
| خروجی زیپ | ۱۹٫۸۶۸ ثانیه با فعال بودن tracemalloc |
| نقطه اوج تخصیص‌های خروجی پی‌thon ردیابی‌شده | ۰.۵۱ مگابایت؛ RSS پردازش نمی‌شود |
| اندازهٔ فایل زیپ | ۴٬۶۱۰٬۹۶۲ بایت |
| تأیید مستقل | تمام ۱۰٬۰۰۰ رویداد تأیید شدند |

این ابزار مسیر محلی ضبط/صادرات سریالی را در این میزبان ویندوز اندازه‌گیری می‌کند. این ابزار اندازه‌گیری، تحویل MTProto، حساب‌های همزمان، محدودسازی تلگرام، رسانه‌ها، بار کاری طولانی‌مدت یا تعداد تضمین‌شده‌ای از چت‌های واقعی را انجام نمی‌دهد. این اندازه‌گیری مربوط به قبل از ابزارهای نهایی مهر و موم زمانی آفلاین است، که مسیر پیام اندازه‌گیری‌شده را تغییر نمی‌دهد.

## جستجوی متن کامل در یک میلیون پیام · ۵ نوامبر ۲۰۲۶

دستور: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

یک ژورنال امضاشده و تعیین‌کننده‌ی متشکل از ۱٬۰۰۰٬۰۰۰ پیام مصنوعی در ۲۰۰ چت (اشکال کلمات روسی، اوکراینی، انگلیسی، چینی، ژاپنی، لینک‌ها و نام‌های کاربری) در ۷۱ ثانیه نمایه شد؛ این نمایه علاوه بر ژورنال ۱.۵۰ گیگابایتی، ۵۸ مگابایت فضا اشغال کرد. جستجوهای تطابق برتر بین ۹ تا ۱۹۰ میلی‌ثانیه (میانه) زمان برد، در حالی که این رقم برای جستجوی زیرنویس قبلی ۲.۴ تا ۳.۲ ثانیه بود. نتایج کامل، سخت‌افزار و محدودیت‌ها: [جستجوی تمام‌متن](https://phishdestroy.github.io/TgWitness/fa/docs/reference/search/#benchmark). `tools/test_fulltext.py` همچنین آرشیوی امضا شده را که قبل از جستجوی تمام متن ایجاد شده است، تأیید می‌کند (`tools/fixtures/evidence-before-fulltext.zip`) با اعتبارسنج فعلی، و یک آرشیو فعلی با اعتبارسنج آن آرشیو تأیید می‌کند. `verify.py`.

## صلاحیت‌های باقی‌مانده

ژورنال زندهٔ نگهداری‌شده، ثبت واقعی جمع‌آوری، ویرایش‌ها، اعلان‌های حذف، پیوست‌ها، بازبینی‌های مجدد و مدیریت محدودیت نرخ را فراهم می‌کند. این ابزار سوابق جامع تحویل، ماتریس کنترل‌شده دیده‌بانی نقش‌ها، واکنش‌دهندگان، انتظار سیل طولانی‌مدت (FloodWait)، مسدودسازی حساب‌ها و بازیابی پس از وقفه شبکه/فرآیند را ثبت نمی‌کند. صدور توکن QR از تأیید QR موبایلی تکمیل‌شده مستقل است.

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

The [public audit directory](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) contains only the signed report and aggregate measurements. Detailed operational receipts, raw captures and account material remain private. Application screenshots in `docs/assets/` use fictional demonstration data.
