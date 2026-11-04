# کیا جانچا گیا ہے

Canonical page: https://phishdestroy.github.io/TgWitness/ur/docs/reference/verification/

لائو ٹیلیگرام ٹیسٹ، خودکار چیکس، براؤزر چیکس اور جو ابھی تک غیر تصدیق شدہ ہے۔

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

## باقی اہلیت

محفوظ شدہ لائیو جرنل اصل جمع، ترامیم، حذف کے نوٹس، منسلکات، دوبارہ جانچ اور ریٹ-لیمٹ ہینڈلنگ کو مستند بناتا ہے۔ یہ مکمل ترسیل یا کردار کی نمائش، ردعمل کرنے والوں، طویل FloodWait، اکاؤنٹ کی پابندیوں اور نیٹ ورک/عمل کی رکاوٹ سے بحالی کے کنٹرول شدہ میٹرکس کو ثابت نہیں کرتا۔ QR ٹوکن کا اجرا مکمل شدہ موبائل QR تصدیق سے الگ رہتا ہے۔

ڈوکر بلڈ/رن، لینکس/میک او ایس انسٹالیشن، مسلسل زیادہ لوڈ، آزاد سیکیورٹی جائزہ، ایک حقیقی آزاد TSA ردعمل، سرٹیفیکیٹ کی منسوخی/آرکائیول کی توثیق اور عدالتی سرٹیفیکیشن ریکارڈ شدہ اہلیت سے باہر ہیں۔ محفوظ شدہ MTProto اسٹیٹ اور کیچ اپ نافذ کر دیے گئے ہیں؛ ایٹمی پائیدار ری پلے ابھی تک قائم نہیں ہوا ہے۔ ایڈمن لاگ کلیکشن، اضافی ری ایکٹر لسٹس اور ترجیحی شارٹ پولنگ الگ خصوصیات کے طور پر موجود ہیں۔ کنٹرول شدہ کوالیفیکیشن میٹرکس کے لیے [لائیو قبولیت](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) دیکھیں۔

مقامی تفصیلی رسیدیں اور اسکرین شاٹس test-results/ (Git-ignored) میں موجود ہیں۔ docs/assets/ میں موجود عوامی اسکرین شاٹ میں صرف فرضی مظاہرے کا ڈیٹا شامل ہے۔
