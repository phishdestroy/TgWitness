# ما تم اختباره

Canonical page: https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/

اختبار Telegram المباشر، والفحوصات الآلية، وفحوصات المتصفح، وما لم يتم التحقق منه بعد.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [التوثيق](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/ar/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Updated 6 November 2026.** Results are tied to the revision, environment and workload recorded for each run. [Current capabilities](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describes the available workflows; this page records what has actually been checked.

[Performance graphs](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Signed English audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Downloadable measurements](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Latest evidence | النتيجة | النطاق |
| --- | --- | --- |
| Release audit · 6 Nov | 1,461 core tests passed; 37 platform skips | Source `92e539af40d8`; open findings retained |
| Fresh exports · 6 Nov | 127.713 and 141.781 records/s, complete cycle | Two accounts per server; text and metadata through WARP |
| Retained archives · 6 Nov | 48 archives; 3,598,381 records verified | Existing archives checked against pinned workspace keys |
| Trusted Live · 5 Nov | Guarded CPU recording and WARP checks | Official Desktop login and native export remain unqualified |
| Phala / Intel TDX · 4 Nov | All 16 verifier checks passed on later runs | Historical deployment; no Telegram account on the CVM |

**On this page**

- [Release audit and fresh exports · 6 November 2026](https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu and WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live Phala Cloud deployment · 4 November 2026](https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Live server journal inventory · 1 November 2026](https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Recent offline and fault-injection checks · 1 November 2026](https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live Telegram test, whole account · 29 October 2026](https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Password-protected export opened with libarchive · 29 October 2026](https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live Telegram test · 27 to 29 October 2026](https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetic local capacity measurement](https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Full-text search on one million messages · 5 November 2026](https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Remaining qualification](https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/#remaining-qualification)

## Release audit and fresh exports · 6 November 2026

The audit used v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. Installed-package smoke checks passed on three servers. The signed report retains the state observed at that time.

[![Acquisition and complete export rates for two fresh workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Workload | السجلات | Acquisition | Complete cycle | Complete-cycle rate |
| --- | --- | --- | --- | --- |
| Server A · two accounts | 27,030 | 189.043 s | 211.647 s | 127.713 records/s |
| Server B · two accounts | 29,299 | 182.513 s | 206.650 s | 141.781 records/s |

Both exports began without resume, excluded attachments and avatars, and ended with zero duplicate or reused records. The complete cycle includes preparation, acquisition, selection, packaging and archive verification. Server A also ran a protected-chat read check. Four FloodWait events on A and three on B were respected. These observations do not establish a general throughput guarantee.

| تحقق | النتيجة | Qualification |
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

## النشر المباشر على Phala Cloud · 4 نوفمبر 2026

**Historical result:** later deployments passed all 16 verifier checks, including Intel TDX and the quick tunnel. Restart evidence, signed address discovery and report timestamps were checked separately. Each test CVM was removed after its run.

| الإعداد | Recorded value |
| --- | --- |
| المزود | Phala Cloud · `tdx.small` · US-WEST-1 |
| النشر | `--provider phala --quick-tunnel`; initially empty workspace |
| Initial collector | `df7d860c` · v0.8.1 |
| Collector with all fixes | `53a0f7e9` |
| Production guest | `dstack-0.5.12`; SSH access disabled |
| External services | ntfy.sh, GitHub and Intel PCS |
| Observed cost | Seven CVMs, about 1.9 US cents together; historical test pricing |

The sequence below separates initial failures, fixes and completed checks. No Telegram account was connected to these CVMs.

**Deployments 1–2 · provider differences and regression checks**

اكتشفت عمليتا النشر الأوليتان خمسة اختلافات عن Phala Cloud المحاكاة. تقوم [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) الآن بإعادة إنتاج كل منها، وتفشل دون إصلاحها:

| على Phala Cloud | قبل الإصلاح | الإصلاح |
| --- | --- | --- |
| `compose_file.name` مطلوب | HTTP 422، لم يتم إنشاء أي شيء | يحتوي تكوين Docker Compose على اسم CVM |
| ما لم يتم توفير اسم فارغ، تضيف Phala البرنامج النصي الخاص بها قبل التشغيل إلى ملف app-compose الذي تم قياسه (v0.0.20: تسجيل الدخول إلى Docker، `docker compose pull`، كلمة مرور الجذر، مفاتيح SSH من `user_config`) | فشل `tdx_compose`: وجود كود خارج نطاق تكوين Docker Compose المنشور | يُعيّن ملف app-compose القيمة `pre_launch_script` إلى `""`؛ ثم يتجاهلها Phala |
| بدون `image`، تختار Phala `dstack-dev-0.5.12`، وهو إصدار التطوير، مع تمكين الوصول عبر SSH | فشل `server_state`. سجل إثبات الأجهزة وحده اجتاز الاختبار في هذه الصورة؛ ولا يظهر ذلك إلا في سجل المزود و`tdx_os` | يطلب النشر الإصدار الإنتاجي من الإصدار الحالي لـ Phala، `dstack-0.5.12` |
| مع إيقاف تشغيل بوابة dstack، لا تحصل تفاصيل CVM أبدًا على رمز الخطأ `instance_id` | ينتظر النشر لمدة 30 دقيقة ثم يفشل | يتم قراءة معرّف المثيل من حالة CVM |
| تعد عمليات إعادة التشغيل والإيقاف والتشغيل عمليات خاصة بـ CVM، وليست تعديلات على التطبيق | لم يدرج `provider_actions` عمليات إعادة التشغيل | يتم قراءة العمليات أيضًا |

**Deployment 3 · attestation, access checks and restart evidence**

- قامت الآلة الافتراضية (CVM) بتشغيل `dstack-0.5.12` مع تعطيل الوصول عبر SSH. نشر المجمع عنوانه الموقّع بعد حوالي 1.5 دقيقة من الإنشاء. ثم نجح النشر في تمرير `tdx_binding` و`tdx_quote` (Intel TCB UpToDate، وسجل إثبات الأجهزة v4، وFMSPC `20a06f000000`، وليس في وضع التصحيح، وغير قابل للترحيل، ويدعم بيانات التحقق التشفيرية المستلمة من Intel)، و`tdx_compose_hash`، و`tdx_compose` (بايتًا بايتًا)، و`tdx_identity` (مفاتيح KMS).
- أجابت اللوحة الموجودة على عنوان trycloudflare.com برمز 401 في حالة عدم وجود رمز مميز أو وجود رمز مميز خاطئ، ورمز 200 عند استخدام رمز مميز اللوحة.
- `verify` مع تعيين `--source` إلى أرشيف GitHub للالتزام (commit) وتمرير البصمة بشكل منفصل: الخادم، `server_state`، جدار الحماية (بدون بوابة، بدون نقطة نهاية عامة)، سجل المزود، البيان، البصمة، تجزئة المصدر، التمهيد، واجتياز الفحوصات الخمس `tdx_*`. لم تكن Cloudflare و `tdx_os` متاحتين، لذا كانت النتيجة «غير مكتملة».
- تمت عمليتا إعادة تشغيل عبر واجهة برمجة تطبيقات Phala: في كل مرة، عادت الآلة الافتراضية المركزية (CVM) في أقل من دقيقتين باستخدام نفس مفتاح المجمع، وعنوان موقّع جديد، والعنوان القديم الذي يرد بـ 530. أبلغ `verify` عن عملية التشغيل الجديدة وعمليتي إعادة التشغيل على أنهما «REVIEW». مع `--evidence`، تم تأكيد توقيعات السجل وعمليات التشغيل الثلاث، لكل منها سجل إثبات أجهزة Intel TDX الخاص بها من نفس CVM.
- أزال `destroy` ذلك CVM فقط. أصبحت مساحة العمل فارغة بعد ذلك، وتوقف عنوان اللوحة عن الاستجابة.
- أظهرت مراجعة السعر في معالج اللوحة `tdx.small` بسعر 0.058 دولار في الساعة. وأدى إدخال مفتاح خاطئ إلى ظهور رسالة بسيطة تقول «لم يتم قبول مفتاح واجهة برمجة التطبيقات».

**Follow-up fixes · signed address discovery and OS measurements**

- بدون مفتاح العنوان، اتبع `verify` أحدث منشور صحيح التكوين حول موضوع العنوان، والذي يرد مطبوعًا في تكوين Docker Compose المنشور. أرسله منشور مزور إلى مضيف غير موجود، وفشل `statement`: لم يتمكن المزور من التظاهر بأنه المجمع، لكنه تمكن من عرقلة عملية التحقق من طرف ثالث لمدة تصل إلى 12 ساعة باستخدام طابع زمني مزور لمستقبل. يقوم المجمع الآن أيضًا بنشر عنوانه موقّعًا بمفتاحه الخاص، ولا يقبل `verify` سوى هذه المنشورات عندما يقوم المجمع بإنشائها، ويتم ترتيب المنشورات حسب وقت الاستلام في ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) يعيد تشغيل المنشورات المزورة. لا يقوم CVM بتشغيل هذا إلا من التزام يحتوي عليه، لذا فإن المجمع في هذا التشغيل لم يوقع عنوانه بعد، وقد أشار `verify` إلى ذلك.
- لم يتمكن `tdx_os` من التشغيل بدون `dstack-mr`، الذي يحتوي إصداره الحالي على `measure-os` بدلاً من `measure --json` المذكور في الوثائق. يقوم المدقق الآن بحساب MRTD و RTMR0-2 بنفسه من الصورة المنشورة وشكل الجهاز الظاهري، بما في ذلك جداول ACPI.

**Deployment 4 · all 16 checks, report seals and restart verification**

- نزّلت عملية النشر الصورة المنشورة `dstack-0.5.12` مرة واحدة، وطابقتها مع تجزئة صورة نظام التشغيل التي أبلغت عنها CVM. نجح فحص `tdx_os`: تطابقت قيم MRTD وRTMR0 وRTMR1 وRTMR2 مع القيم المحسوبة لـ QEMU 8.2.2، و1 vCPU و2 GiB. أعطى الحساب نفسه قيمة RTMR0 مختلفة عند افتراض 4 GiB أو2 vCPU أوQEMU 9.2.1 أوبطاقة شبكة ثانية، وفشل عند تغيير النواة أوالبرامج الثابتة أو سطر الأوامر، وكذلك مع صورة التطوير.
- اجتاز `verify` جميع الفحوصات الـ 16، بما في ذلك موصل النفق السريع، لذا كانت النتيجة «ناجح». وقد كتب شهادة HTML وPDF، مختومة رقميًا بالتوقيعات والطوابع الزمنية باستخدام طابع زمني معتمد من eIDAS صادر عن وحدة الطوابع الزمنية التابعة للحكومة البلجيكية TSU 202301 (الحالة: مُنحت في قائمة الجهات الموثوقة في بلجيكا )، وطابع زمني من FreeTSA وتوقيع المُحقق؛ وقد أكد `check-report` صحة كل ذلك وتوقيع ملف PDF.
- بعد إعادة التشغيل، أكد `verify --evidence` حدوث عمليتي بدء تشغيل، رافق كل منهما شهادة أجهزة تم إنشاؤها داخل CVM، وتم تشغيل كل منهما من `dstack-0.5.12` المنشور؛ وكانت إعادة التشغيل وعملية التشغيل الجديدة من النوع REVIEW.
- ترك `destroy` مساحة العمل فارغة.

**Deployment 5 · collector-signed discovery and forged-post rejection**

The collector ran from commit `53a0f7e9`, which includes the fixes above.

- نشر المُجمِّع عنوانه المُوقَّع بمفتاحه الخاص، بجوار منشور HMAC الخاص بالمشغل. ثم أُضيف منشوران مزيفان إلى الموضوع، أحدهما بـ HMAC مُصفَّر والآخر مُوقَّع بمفتاح Ed25519 آخر، وكلاهما يدعيان تاريخًا في عام 2096. أخذ `verify` العنوان الموقع بمفتاح المجمع واجتاز جميع الاختبارات الـ 16؛ وحمل الختم مرة أخرى الطابع الزمني البلجيكي المعتمد، والطابع الزمني لـ FreeTSA وتوقيع المُحقق، وقام `check-report` بتأكيدها.
- بعد إعادة التشغيل، نشر المجمع العنوان الجديد الموقّع: `verify` عثر عليه على الفور، و **الخاص بالمشغل «ابحث عن العنوان الحالي»** بعد 27 ثانية من منشور HMAC، وكلاهما تجاهل المنشورات المزورة. `verify --evidence` أكد تشغيل جهازيْن من `dstack-0.5.12`.
- أظهر «Deploy» ما تحاسبه Phala على CVM، بما في ذلك القرص: 0.06078 دولار في الساعة.

### Panel wizard and remaining scope

تم تشغيل معالج اللوحة على Phala Cloud مرتين، مرة عبر واجهة برمجة تطبيقات المهام (API) الخاصة بها ومرة عبر المتصفح باستخدام Chromium حقيقي: فحص السعر، والإنشاء مع الالتزام تحت **Advanced**، واجتياز جميع فحوصات التصديق الستة، وقائمة الخوادم التي تعرض السعر المفوتر (44.37 دولارًا أمريكيًا شهريًا)، **Find العنوان الحالي**، وتنزيل تكوين Docker Compose المقاس، والحذف. لم يلاحظ المتصفح أي أخطاء في الصفحة. في كل مرة كانت مساحة العمل فارغة بعد ذلك.

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation. All prices in this section were observed on 4 November 2026.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | العدد |
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

| تحقق | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## اختبار Telegram مباشر، الحساب بالكامل · 29 أكتوبر 2026

استمر الحساب نفسه في العمل بعد الاختبار المذكور أدناه. في 29 أكتوبر الساعة 12:10 بالتوقيت العالمي المنسق (UTC)، تم تغيير نطاقه ليشمل الحساب بأكمله (القنوات، والمجموعات، والمحادثات الخاصة، والروبوتات)؛ وطلبت لوحة التحكم التأكيد، وسجلت السجلات الموقعة ذلك. بحلول الساعة 17:59 بالتوقيت العالمي المنسق (UTC)، كان السجل يحتوي على:

| تم التسجيل في الفترة من 27 أكتوبر الساعة 21:36 إلى 29 أكتوبر الساعة 17:59 بالتوقيت العالمي المنسق (UTC) | العدد |
| --- | --- |
| سجلات السجل | 9,968 |
| رسائل جديدة | 5,308 |
| منها بعد الانتقال إلى الحساب الكامل | 3,878 |
| عمليات الحذف | 784 |
| تم حذفها بعد أن قام TgWitness بحفظ الرسالة | 596 |
| التعديلات | 41 |
| الرسائل المضافة بعد إعادة التحقق | 2,273 |
| الرسائل التي لم يعد بالإمكان العثور عليها عند إعادة الفحص | 18 |
| الرسائل المحفوظة عبر لقطات السجل | 242 |
| المرفقات المحفوظة | 247 |
| يبدأ برنامج التجميع | 19 |
| Telegram FloodWait في وضع الإيقاف المؤقت | 26 |

- أكدت عملية التحقق **«Verify»** التي أجرتها اللجنة صحة التوقيعات وسلسلة التجزئة لجميع السجلات البالغ عددها 9,968 سجلاً.
- جاءت الرسائل من مجموعتين أو قناتين و3 محادثات خاصة وبوتات. تم الضغط على زر رسالة واحد من **قسم «المحادثات**»؛ ويرد الطلب ورد Telegram في السجل.
- تمت إضافة محادثات جديدة عندما أعاد المجمع مسح الحساب عند إعادة التشغيل. كان خيار حفظ الرسائل السابقة للمحادثات الجديدة معطلاً (`history = 0`)، لذا لم يتم تناوله هنا.

لا يشمل الموقع: ردود الفعل، وتغييرات العضوية، وملفات تعريف الأشخاص، وإرسال الرسائل، والانضمام عن طريق الدعوة، والوكلاء، والإشعارات، وروبوت Witness، وعدة حسابات في آن واحد. الملفات العامة تحتوي على الأعداد فقط.

## ملف تصدير محمي بكلمة مرور يُفتح باستخدام libarchive · 29 أكتوبر 2026

تم فتح أرشيف تم إنشاؤه بواسطة كود تشفير التصدير (WinZip AES-256، وهو التنسيق الذي يقرأه كل من 7-Zip وWinRAR ) باستخدام Windows `tar` (bsdtar 3.6.2، libarchive). باستخدام كلمة المرور الصحيحة، تطابق الملف المستخرج مع قيمة SHA-256 الأصلية؛ أما كلمة المرور الخاطئة فقد تم رفضها بعبارة «عبارة مرور غير صحيحة ». ولم يتم تشغيل برامج 7-Zip وWinRAR نفسها.

## اختبار Telegram المباشر · من 27 إلى 29 أكتوبر 2026

قام حساب Telegram حقيقي واحد، تم تسجيل الدخول إليه عبر مجموعة أزواج واجهة برمجة التطبيقات (API) المدمجة، بتسجيل مجموعة كبيرة واحدة من **27 أكتوبر الساعة 21:36 بالتوقيت العالمي المنسق (UTC) إلى 29 أكتوبر الساعة 05:15 بالتوقيت العالمي المنسق (UTC)**. تم تشغيل أداة التجميع 12 مرة خلال تلك الفترة.

| مسجلة | العدد |
| --- | --- |
| سجلات السجل، بما في ذلك نبضات القلب وسجلات الخدمة | 2,385 |
| رسائل جديدة | 1,291 |
| عمليات الحذف | 472 |
| تم حذفها بعد أن قام TgWitness بحفظ النص | 347 |
| التعديلات | 12 |
| الرسائل التي فاتت أثناء التوقف، تمت إضافتها عند إعادة الفحص | 12 |
| المرفقات المحفوظة | 17 |
| المرفقات لم يتم تنزيلها (التنزيل معطل، أو لا يوجد ملف للتنزيل) | 14 |
| يقوم Telegram FloodWait بالتوقف مؤقتًا لمدة 3 ثوانٍ في كل مرة أثناء إعادة الفحص | 8 |

- يتم التحقق من التوقيعات وسلسلة التجزئة لجميع السجلات البالغ عددها 2,385 سجلًا مقابل المفتاح العام للسجل.
- بعد إعادة التشغيل، يستأنف المجمع العمل من حالة التحديث المحفوظة (`pts`) ويقوم Telethon بملء الفجوات؛ ثم تضيف عملية إعادة الفحص الرسائل التي لا تزال مفقودة.
- في كل مرة يواجه فيها المجمع حالة «FloodWait»، ينتظر المجمع المدة المطلوبة ثم يواصل العمل.
- ظل الحساب مسجلاً للدخول، وأعيد الاتصال بنفس الجلسة في 29 أكتوبر.

لا يشمل هذا الاختبار: التعامل مع عدة حسابات في آن واحد، وأدوار المسؤولين، والبروكسيات، وانقطاعات الخدمة التي تزيد مدتها عن بضع ساعات، وإ[جراءات القبول المباشرة](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) الكاملة. تحتوي الملفات العامة على هذه العناصر فقط: لا توجد معرّفات للحسابات أو الدردشات، ولا رسائل، ولا بيانات اعتماد.

## قياس القدرات المحلية الاصطناعية

الأمر: `python tools/check_capacity.py --events 10000 --chats 100`

| المقاييس | تمت الملاحظة |
| --- | --- |
| المدخلات | 10,000 حدث رسالة اصطناعية عبر 100 مصدر اصطناعي مختار |
| نص الرسالة | 400 حرف؛ بدون وسائط أو شبكة |
| الاستيعاب | 53.273 ثانية؛ 187.7 حدثًا في الثانية |
| زمن استجابة المعالج | p50 4.162 مللي ثانية؛ p95 7.784 مللي ثانية؛ الحد الأقصى 129.118 مللي ثانية |
| تصدير ملف ZIP | 19.868 ثانية مع تمكين tracemalloc |
| ذروة تخصيصات تصدير Python التي تم تتبعها | 0.51 ميغابايت؛ لا يدعم RSS |
| حجم ملف ZIP | 4,610,962 بايت |
| التحقق المستقل | تم التحقق من صحة جميع الأحداث البالغ عددها 10,000 حدث |

يقيس هذا مسار التسجيل/التصدير التسلسلي المحلي على مضيف Windows هذا. ولا يقيس تسليم MTProto، أو الحسابات المتزامنة، أو تقييد سرعة Telegram، أو الوسائط، أو أعباء العمل طويلة الأمد، أو عددًا مضمونًا من المحادثات الحقيقية. ويأتي هذا القياس قبل أدوات الطابع الزمني النهائية في وضع عدم الاتصال، والتي لا تغير مسار الرسائل المقاسة.

## البحث عن النص الكامل في مليون رسالة · 5 نوفمبر 2026

الأمر: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

تم فهرسة سجل موقّع حتمي يحتوي على 1,000,000 رسالة اصطناعية في 200 محادثة (أشكال الكلمات الروسية والأوكرانية والإنجليزية والصينية واليابانية والروابط والمعرفات) في 71 ثانية؛ واستهلك الفهرس 58 ميغابايت إلى جانب سجل بحجم 1.50 جيجابايت. استغرقت عمليات البحث عن أفضل تطابق من 9 إلى 190 مللي ثانية (الوسيط)، مقابل 2.4 إلى 3.2 ثانية لعملية البحث السابقة عن سلسلة فرعية. النتائج الكاملة، والأجهزة، والحدود: [البحث عن النص الكامل](https://phishdestroy.github.io/TgWitness/ar/docs/reference/search/#benchmark). `tools/test_fulltext.py` كما يتحقق من أرشيف موقّع تم إنشاؤه قبل البحث عن النص الكامل (`tools/fixtures/evidence-before-fulltext.zip`) باستخدام أداة التحقق الحالية، والأرشيف الحالي باستخدام أداة التحقق الخاصة بذلك الأرشيف `verify.py`.

## المؤهلات المتبقية

تثبت السجلات الحية المحفوظة عمليات التجميع الفعلية، وإشعارات التعديل والحذف، والمرفقات، عمليات إعادة التحقق، ومعالجة حدود معدل الاستخدام. ولا يثبت التسليم الشامل أو وجود مصفوفة خاضعة للرقابة لرؤية الأدوار، والجهات الفاعلة في الاستجابة، وFloodWait المطول، وحظر الحسابات، و استعادة الشبكة/العملية بعد الانقطاع. ويظل إصدار رمز QR منفصلاً عن التأكيد النهائي لرمز QR عبر الهاتف المحمول.

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

The [public audit directory](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) contains only the signed report and aggregate measurements. Detailed operational receipts, raw captures and account material remain private. Application screenshots in `docs/assets/` use fictional demonstration data.
