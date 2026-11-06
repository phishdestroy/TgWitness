# کیا جانچا گیا ہے

Canonical page: https://phishdestroy.github.io/TgWitness/ur/docs/reference/verification/

لائو ٹیلیگرام ٹیسٹ، خودکار چیکس، براؤزر چیکس اور جو ابھی تک غیر تصدیق شدہ ہے۔

Each result below applies to its recorded revision and environment. The [current capability matrix](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) separates implementation, published downloads and remaining qualification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## لائو فالا کلاؤڈ تعیناتی · 4 نومبر 2026

`--provider phala --quick-tunnel` کو حقیقی **Phala Cloud** (`tdx.small`، ریجن US-WEST-1) کے خلاف چلایا گیا، ایک خالی ورک اسپیس کی Phala Cloud API کلید، حقیقی ntfy.sh، GitHub اور Intel PCS کے ساتھ۔ CVM نے `df7d860c` (v0.8.1) commit انسٹال کیا؛ deploy، verify اور destroy کمانڈ لائن سے نیچے دیے گئے حل کے ساتھ چلائے گئے۔ سات CVMs کی کل لاگت تقریباً 1.9 امریکی سینٹ تھی۔

پہلی دو تعیناتیوں نے سمولیٹڈ Phala کلاؤڈ سے پانچ فرق دریافت کیے۔ [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) اب ہر ایک کو دوبارہ پیدا کرتا ہے، اور اس کی مرمت کے بغیر ناکام ہو جاتا ہے:

| Phala Cloud پر | مرمت سے پہلے | اصلاح |
| --- | --- | --- |
| `compose_file.name` درکار ہے | HTTP 422، کچھ بھی تخلیق نہیں ہوا | Docker Compose کنفیگریشن CVM کا نام اپنے اندر رکھتی ہے۔ |
| جب تک کوئی خالی دیا گیا ہو، Phala اپنا pre-launch script ماپے گئے app-compose میں شامل کرتی ہے (v0.0.20: Docker login, `docker compose pull`, روٹ پاس ورڈ، SSH keys from `user_config`) | `tdx_compose` ناکام ہوتا ہے: شائع شدہ Docker Compose کنفیگریشن کے باہر کوڈ | ایپ-کمپوز `pre_launch_script` کو `""` پر سیٹ کرتا ہے؛ فالہ پھر اسے خارج کر دیتا ہے |
| `image` کے بغیر، Phala `dstack-dev-0.5.12`، ڈویلپمنٹ بلڈ، کو منتخب کرتا ہے، جس میں SSH رسائی فعال ہوتی ہے۔ | `server_state` ناکام ہو جاتا ہے۔ صرف ہارڈویئر تصدیقی ریکارڈ نے اس امیج کو پاس کیا؛ صرف فراہم کنندہ کا ریکارڈ اور `tdx_os` اسے دکھاتے ہیں۔ | ڈپلائمنٹ Phala کی موجودہ ریلیز، `dstack-0.5.12` کے پروڈکشن بلڈ کی درخواست کرتی ہے۔ |
| جب dstack گیٹ وے بند تھا، تو CVM کی تفصیلات کو کبھی `instance_id` نہیں ملا۔ | ڈپلائے 30 منٹ انتظار کرتا ہے اور ناکام ہو جاتا ہے | انستنس آئی ڈی سی وی ایم کی حالت سے پڑھی جاتی ہے۔ |
| ری اسٹارٹس، اسٹاپس اور اسٹارٹس سی وی ایم آپریشنز ہیں، ایپلیکیشن ریویژنز نہیں۔ | `provider_actions` نے ری اسٹارٹس کی فہرست نہیں دی۔ | آپریشنز بھی شامل ہیں |

تیسری تعیناتی:

- CVM نے SSH رسائی بند کرکے `dstack-0.5.12` چلایا۔ کلیکٹر نے تخلیق کے تقریباً 1.5 منٹ بعد اپنا دستخط شدہ پتہ پوسٹ کیا۔ Deploy نے پھر `tdx_binding`، `tdx_quote` (Intel TCB UpToDate، ہارڈویئر تصدیق ریکارڈ v4، FMSPC `20a06f000000`، ڈیبگ موڈ میں نہیں، منتقل نہیں کیا جا سکتا، Intel سے حاصل کردہ کرپٹوگرافک تصدیق کے ڈیٹا کی حمایت کرتا ہے)، `tdx_compose_hash`، `tdx_compose` (بائٹ بہ بائٹ) اور `tdx_identity` (KMS کلیدیں)۔
- اس کے trycloudflare.com پتے پر موجود پینل نے ٹوکن کے بغیر یا غلط ٹوکن کے ساتھ 401 کا جواب دیا، اور پینل ٹوکن کے ساتھ 200 کا۔
- `verify` کے ساتھ `--source` کو کمٹ کے گٹ ہب آرکائیو کے لیے سیٹ کیا گیا اور فنگر پرنٹ الگ سے دیا گیا: سرور، `server_state`، فائر وال (کوئی گیٹ وے نہیں، کوئی پبلک اینڈ پوائنٹ نہیں)، پرووائیڈر لاگ، بیان، فنگر پرنٹ، سورس ہیش، بوٹ اور پانچ `tdx_*` چیکس پاس ہوئے۔ Cloudflare اور `tdx_os` دستیاب نہیں تھے، لہٰذا نتیجہ نامکمل تھا۔
- Phala کی API کے ذریعے دو ری اسٹارٹس: ہر بار CVM دو منٹ سے کم وقت میں واپس آ گیا، ایک ہی کلیکٹر کی، ایک نیا دستخط شدہ پتہ، اور پرانا پتہ 530 کا جواب دے رہا تھا۔ `verify` نے نئے بوٹ اور دونوں ری اسٹارٹس کو REVIEW کے طور پر رپورٹ کیا۔ `--evidence` کے ساتھ اس نے جرنل دستخطوں اور تین شروعاتوں کی تصدیق کی، ہر ایک کے ساتھ اسی CVM سے اپنا Intel TDX ہارڈویئر تصدیقی ریکارڈ۔
- `destroy` نے صرف اسی CVM کو ہٹا دیا۔ اس کے بعد ورک اسپیس خالی ہو گیا، اور پینل کا پتہ جواب دینا بند کر دیا۔
- پینل وزرڈ کی قیمت کی جانچ نے `tdx.small` کو $0.058 فی گھنٹہ دکھایا۔ ایک غلط کلید کو ایک سادہ "API کلید قبول نہیں کی گئی" پیغام ملا۔

دو مزید نتائج، جو بعد میں ٹھیک کیے گئے:

- ایڈریس کی بغیر، `verify` نے ایڈریس موضوع پر تازہ ترین درست پوسٹ کی پیروی کی، جو شائع شدہ Docker Compose کنفیگریشن میں چھپی ہوتی ہے۔ ایک جعلی پوسٹ نے اسے ایک ایسے ہوسٹ پر بھیجا جو موجود نہیں ہے، اور `statement` ناکام ہو گیا: ایک جعلساز کلیکٹر کے طور پر پیش نہیں ہو سکتا تھا، لیکن بلاک کر سکتا تھا تیسری پارٹی کی تصدیق، مستقبل کے جعلی ٹائم اسٹیمپ کے ساتھ 12 گھنٹے تک۔ کلیکٹر اب اپنا پتہ اپنی ہی کلید سے دستخط شدہ پوسٹ بھی کرتا ہے، `verify` صرف ایسی پوسٹس قبول کرتا ہے جب کلیکٹر انہیں کرتا ہے، اور پوسٹس ntfy.sh کے وصولی کے وقت کے مطابق ترتیب دی جاتی ہیں۔ [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) جعلی پوسٹس کو دوبارہ چلاتا ہے۔ ایک CVM اسے صرف اس کمٹ سے چلاتا ہے جس میں یہ موجود ہو، لہٰذا اس رن کے کلیکٹر نے ابھی اپنا پتہ سائن نہیں کیا تھا اور `verify` نے یہی بتایا۔
- `tdx_os`، `dstack-mr` کے بغیر نہیں چل سکتا تھا، جس کے موجودہ ورژن میں دستاویزات میں نامزد `measure --json` کے بجائے `measure-os` ہے۔ اب ویریفائر شائع شدہ امیج اور VM کی شکل، بشمول ACPI ٹیبلز، سے خود MRTD اور RTMR0-2 کا حساب لگاتا ہے۔

چوتھی تعیناتی، ان کے ساتھ:

- ڈیپلائے نے شائع شدہ `dstack-0.5.12` کو ایک بار ڈاؤن لوڈ کیا، اسے CVM کی رپورٹ کردہ OS امیج ہیش سے ملا، اور `tdx_os` پاس ہو گیا: MRTD، RTMR0، RTMR1 اور RTMR2 QEMU کے لیے کیلکولیٹ کی گئی اقدار کے برابر ہیں۔ 8.2.2، 1 vCPU اور 2 GiB۔ اسی حساب نے دعویٰ کردہ 4 GiB، 2 vCPUs، QEMU 9.2.1 یا دوسری نیٹ ورک کارڈ کے لیے ایک مختلف RTMR0 دیا، اور تبدیل شدہ کرنل، فرم ویئر یا کمانڈ لائن اور ڈیولپمنٹ امیج کے لیے ناکام رہا۔
- `verify` نے اپنے 16 میں سے ہر ایک چیک پاس کیا، جن میں Quick Tunnel کا کنیکٹر بھی شامل تھا، لہٰذا نتیجہ PASS تھا۔ اس نے HTML اور PDF سرٹیفکیٹ لکھا، جسے دستخطوں اور ٹائم اسٹیمپ کے ساتھ ڈیجیٹلی سیل کیا گیا تھا، جس میں بیلجیئم حکومت کے ٹائم اسٹیمپنگ یونٹ TSU 202301 (بیلجیئم کی قابلِ اعتماد فہرست میں شامل) کا ایک کوالیفائیڈ eIDAS ٹائم اسٹیمپ، ایک FreeTSA ٹائم اسٹیمپ اور ویریفائر کے دستخط شامل تھے؛ `check-report` نے ان سب کی اور PDF کے دستخط کی تصدیق کی۔
- ری اسٹارٹ کے بعد، `verify --evidence` نے دو آغاز کی تصدیق کی، ہر ایک کے ساتھ CVM کے اندر تیار کردہ ہارڈویئر تصدیق نامہ اور ہر ایک شائع شدہ `dstack-0.5.12` سے بوٹ کیا گیا؛ ری اسٹارٹ اور نیا بوٹ REVIEW تھے۔
- `destroy` نے ورک اسپیس خالی چھوڑ دیا۔

پانچویں تعیناتی نے commit `53a0f7e9` سے collector چلایا، جس میں مذکورہ بالا تمام چیزیں شامل ہیں:

- کلیکٹر نے اپنا ایڈریس اپنی ہی کلید سے دستخط شدہ پوسٹ کیا، آپریٹر کے HMAC پوسٹ کے ساتھ۔ پھر موضوع میں دو جعلی پوسٹس شامل کی گئیں، ایک صفر شدہ HMAC کے ساتھ اور ایک دوسری Ed25519 کلید سے دستخط شدہ، دونوں نے 2096 کے سال میں ایک وقت کا دعویٰ کیا۔ `verify` نے کلیکٹر کی کلید کے ذریعے دستخط شدہ پتے کو لیا اور تمام 16 چیک پاس کیے؛ سیل میں دوبارہ کوالیفائیڈ بیلجیئن ٹائم اسٹیمپ، FreeTSA کا ٹائم اسٹیمپ اور ویریفائر کے دستخط شامل تھے، اور `check-report` نے ان کی تصدیق کی۔
- ری اسٹارٹ کے بعد کلیکٹر نے نیا دستخط شدہ پتہ پوسٹ کیا: `verify` نے اسے فوراً تلاش کر لیا، آپریٹر کے **نے موجودہ پتہ تلاش کیا** HMAC پوسٹ کے 27 سیکنڈ بعد، اور دونوں نے جعلی پوسٹس کو نظر انداز کر دیا۔ `verify --evidence` نے دو اسٹارٹس کی تصدیق کی جو `dstack-0.5.12` سے بوٹ ہوئے تھے۔
- ڈپلائے نے پرنٹ کیا کہ فالا CVM کو بل کیا جاتا ہے، جس میں ڈسک بھی شامل ہے: $0.06078 فی گھنٹہ۔

پینل وزرڈ دو بار Phala Cloud کے خلاف چلایا گیا، ایک بار اس کے جاب API کے ذریعے اور ایک بار ایک حقیقی Chromium کے ساتھ براؤزر کے ذریعے: قیمت کی جانچ، **Advanced** کے تحت کمٹ کے ساتھ تخلیق، تمام چھ تصدیقی چیک پاس ہوئے، سرور کی فہرست بل شدہ قیمت (ماہانہ 44.37 USD) دکھا رہی تھی، **موجودہ پتہ تلاش کریں**، ماپے گئے Docker Compose کنفیگریشن کی ڈاؤن لوڈ، اور حذف۔ براؤزر نے کوئی صفحے کی غلطیاں نہیں دیکھی۔ ہر بار بعد میں ورک اسپیس خالی تھا۔

شامل نہیں: Phala پر Cloudflare ڈومین، CVM پر Telegram اکاؤنٹ، اور `dstack-0.6.1` ایمیج۔ وزرڈ کی قیمت تخلیق سے پہلے صرف Phala کی کمپیوٹ قیمت ہے، کیونکہ اس کی API صرف ایک موجودہ CVM کے لیے ڈسک کی قیمت بتاتی ہے؛ سرور کی فہرست تخلیق کے بعد بل شدہ قیمت دکھاتی ہے۔

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | گنتی |
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

| چیک | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## براہِ راست ٹیلیگرام ٹیسٹ، پورا اکاؤنٹ · 29 اکتوبر 2026

نیچے دیے گئے ٹیسٹ کے بعد بھی وہی اکاؤنٹ چلتا رہا۔ 29 اکتوبر کو 12:10 UTC پر اس کا دائرہ کار پورے اکاؤنٹ (چینلز، گروپس، نجی چیٹس اور بوٹس) پر منتقل کر دیا گیا؛ پینل نے تصدیق طلب کی اور دستخط شدہ جرنل نے اسے ریکارڈ کیا۔ 17:59 UTC تک جرنل میں درج تھا:

| ریکارڈ شدہ، 27 اکتوبر 21:36 سے 29 اکتوبر 17:59 UTC تک | گنتی |
| --- | --- |
| جرنل کے ریکارڈز | 9,968 |
| نئے پیغامات | 5,308 |
| سوئچ کے بعد پورے اکاؤنٹ کے | 3,878 |
| مٹاؤ | 784 |
| جنہیں TgWitness کے پیغام محفوظ کرنے کے بعد حذف کر دیا گیا | 596 |
| ترمیمات | 41 |
| دوبارہ جانچ کے ذریعے شامل کردہ پیغامات | 2,273 |
| وہ پیغامات جنہیں دوبارہ چیک کرنے پر اب تلاش نہیں کیا جا سکا | 18 |
| تاریخ کے اسنیپ شاٹس کے ذریعے محفوظ کردہ پیغامات | 242 |
| محفوظ شدہ منسلکات | 247 |
| کلیکٹر شروع ہوتا ہے | 19 |
| Telegram FloodWait رک جاتا ہے | 26 |

- پینل کے **Verify** چیک نے تمام 9,968 ریکارڈز کے دستخط اور ہیش چین کی تصدیق کی۔
- پیغامات دو گروپس یا چینلز اور تین نجی چیٹس اور بوٹس سے آئے۔ **چیٹس** سے ایک پیغام کا بٹن دبایا گیا؛ درخواست اور ٹیلیگرام کا جواب جرنل میں موجود ہیں۔
- جب کلیکٹر نے اکاؤنٹ کو دوبارہ شروع کرنے پر دوبارہ اسکین کیا تو نئی چیٹس شامل ہوئیں۔ نئی چیٹس کے پرانے پیغامات محفوظ کرنا بند تھا (`history = 0`)، لہٰذا یہاں اس کا احاطہ نہیں کیا گیا۔

شامل نہیں: ردعمل، رکنیت میں تبدیلیاں، صارفین کے پروفائلز، پیغامات بھیجنا، دعوت نامے کے ذریعے شمولیت، پراکسیز، نوٹیفیکیشنز، وِٹنس بوٹ اور ایک ہی وقت میں متعدد اکاؤنٹس۔ عوامی فائلوں میں صرف تعداد شامل ہوتی ہے۔

## پاس ورڈ سے محفوظ شدہ ایکسپورٹ libarchive کے ساتھ کھولا گیا · 29 اکتوبر 2026

ایک آرکائیو جو ایکسپورٹ انکرپشن کوڈ (WinZip AES-256، وہ فارمیٹ جو 7-Zip اور WinRAR پڑھتے ہیں) کے ذریعے لکھا گیا تھا، Windows `tar` (bsdtar 3.6.2, libarchive) کے ساتھ کھولا گیا۔ صحیح پاس ورڈ کے ساتھ نکالی گئی فائل کا اصل SHA-256 سے میل تھا؛ غلط پاس ورڈ کے ساتھ "Incorrect passphrase" کی پیغام کے ساتھ مسترد کر دیا گیا۔ 7-Zip اور WinRAR خود چلائے نہیں گئے۔

## لائو ٹیلیگرام ٹیسٹ · 27 تا 29 اکتوبر 2026

ایک حقیقی ٹیلیگرام اکاؤنٹ، جو بلٹ ان API جوڑا پول کے ذریعے سائن ان تھا، نے **27 اکتوبر 21:36**UTC سے **29 اکتوبر 05:15 UTC تک** ایک سپر گروپ کو ریکارڈ کیا۔ اس عرصے میں کلیکٹر کو 12 بار شروع کیا گیا۔

| ریکارڈ شدہ | گنتی |
| --- | --- |
| جرنل کے ریکارڈز، بشمول ہارٹ بیٹس اور سروس ریکارڈز | 2,385 |
| نئے پیغامات | 1,291 |
| مٹاؤ | 472 |
| جن میں سے کچھ ٹیکسٹ TgWitness کے محفوظ کرنے کے بعد حذف کر دیے گئے | 347 |
| ترمیمات | 12 |
| رک جانے کے دوران رہ جانے والے پیغامات کو ریچیک کے ذریعے شامل کیا گیا | 12 |
| محفوظ شدہ منسلکات | 17 |
| منسلکات ڈاؤن لوڈ نہیں ہوئے (ڈاؤن لوڈز بند ہیں، یا ڈاؤن لوڈ کے لیے کوئی فائل موجود نہیں) | 14 |
| Telegram FloodWait دوبارہ جانچ کے دوران ہر بار 3 سیکنڈ کے لیے رک جاتا ہے | 8 |

- تمام 2,385 ریکارڈز کے دستخط اور ہیش چین جرنل کی عوامی کلید کے خلاف تصدیق کیے جاتے ہیں۔
- ری اسٹارٹ کے بعد کلیکٹر محفوظ شدہ اپ ڈیٹ اسٹیٹ (`pts`) سے دوبارہ شروع ہوتا ہے اور Telethon اپ ڈیٹ مکمل کر لیتا ہے؛ اس کے بعد ری چیک وہ پیغامات شامل کرتا ہے جو ابھی بھی غائب ہیں۔
- ہر FloodWait پر کلیکٹر نے مطلوبہ وقت تک انتظار کیا اور پھر جاری رکھا۔
- اکاؤنٹ سائن ان رہ گیا، اور وہی سیشن 29 اکتوبر کو دوبارہ منسلک ہوا۔

اس ٹیسٹ میں شامل نہیں: ایک ہی وقت میں متعدد اکاؤنٹس، ایڈمنسٹریٹر کے کردار، پراکسیز، چند گھنٹوں سے زیادہ کے وقفے اور مکمل [لائیو قبولیت کا طریقہ کار](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)۔ عوامی فائلوں میں صرف یہ گنتی شامل ہے: کوئی اکاؤنٹ یا چیٹ شناختی نمبر، پیغامات یا اسناد نہیں۔

## مصنوعی مقامی صلاحیت کی پیمائش

کمانڈ: `python tools/check_capacity.py --events 10000 --chats 100`

| میٹرک | مشاہدہ شدہ |
| --- | --- |
| ان پٹ | 100 منتخب مصنوعی ذرائع میں 10,000 مصنوعی پیغامات کے واقعات |
| پیغام کا متن | 400 حروف؛ کوئی میڈیا یا نیٹ ورک نہیں |
| انجیسٹن | 53.273 سیکنڈ؛ 187.7 واقعات فی سیکنڈ |
| ہینڈلر کی تاخیر | p50 4.162 ms؛ p95 7.784 ms؛ زیادہ سے زیادہ 129.118 ms |
| ZIP برآمد | 19.868 سیکنڈز ٹریس میلوک فعال ہونے کے ساتھ |
| Python ایکسپورٹ الاٹمنٹس کے عروج کا سراغ | 0.51 MiB؛ RSS پراسیس نہیں |
| ZIP کا سائز | 4,610,962 بائٹس |
| آزادانہ تصدیق | تمام 10,000 واقعات کی تصدیق ہو چکی ہے |

یہ اس ونڈوز ہوسٹ پر مقامی سیریل ریکارڈنگ/ایکسپورٹ راستے کی پیمائش کرتا ہے۔ یہ MTProto ڈیلیوری، متوازی اکاؤنٹس، ٹیلیگرام تھروٹلنگ، میڈیا، طویل المدتی ورک لوڈ، یا حقیقی چیٹس کی ضمانت شدہ تعداد کی پیمائش نہیں کرتا۔ یہ پیمائش حتمی آف لائن ٹائم اسٹیمپ ٹولنگ سے پہلے کی ہے، جو پیمائش شدہ پیغام کے راستے کو تبدیل نہیں کرتی۔

## ایک ملین پیغامات پر مکمل متن کی تلاش · 5 نومبر 2026

کمانڈ: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

200 چیٹس میں 1,000,000 مصنوعی پیغامات پر مشتمل ایک ڈیٹرمنسٹک دستخط شدہ جرنل (روسی لفظی شکلوں، یوکرینی، انگریزی، چینی، جاپانی، لنکس اور ہینڈلز) 71 سیکنڈ میں انڈیکس ہوا؛ انڈیکس نے 1.50 GiB جرنل کے علاوہ 58 MiB جگہ استعمال کی۔ بہترین مطابقت تلاشوں میں (درمیانی) 9 سے 190 ملی سیکنڈ لگے، جبکہ پچھلی سب اسٹرنگ تلاش میں 2.4 سے 3.2 سیکنڈ لگتے تھے۔ مکمل نتائج، ہارڈویئر اور حدود: [فل ٹیکسٹ سرچ](https://phishdestroy.github.io/TgWitness/ur/docs/reference/search/#benchmark)۔ `tools/test_fulltext.py` یہ فل ٹیکسٹ سرچ سے پہلے بنائے گئے دستخط شدہ آرکائیو کی بھی تصدیق کرتا ہے (`tools/fixtures/evidence-before-fulltext.zip`) کو موجودہ ویریفائر کے ساتھ، اور ایک موجودہ آرکائیو کو اس آرکائیو کے اپنے `verify.py`.

## باقی اہلیت

محفوظ شدہ لائیو جرنل اصل جمع، ترامیم، حذف کے نوٹس، منسلکات، دوبارہ جانچ اور ریٹ-لیمٹ ہینڈلنگ کو مستند بناتا ہے۔ یہ مکمل ترسیل یا کردار کی نمائش، ردعمل کرنے والوں، طویل FloodWait، اکاؤنٹ کی پابندیوں اور نیٹ ورک/عمل کی رکاوٹ سے بحالی کے کنٹرول شدہ میٹرکس کو ثابت نہیں کرتا۔ QR ٹوکن کا اجرا مکمل شدہ موبائل QR تصدیق سے الگ رہتا ہے۔

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

مقامی تفصیلی رسیدیں اور اسکرین شاٹس test-results/ (Git-ignored) میں موجود ہیں۔ docs/assets/ میں موجود عوامی اسکرین شاٹ میں صرف فرضی مظاہرے کا ڈیٹا شامل ہے۔
