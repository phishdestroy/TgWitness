# شواہد کا فارمیٹ

Canonical page: https://phishdestroy.github.io/TgWitness/ur/docs/reference/evidence/

دستخط شدہ ZIP کے مندرجات، ریکارڈ کی اقسام، پراسیس رسیدیں، افراد کے پروفائلز، آف سائٹ نقول اور آف لائن تصدیق۔

TgWitness اکاؤنٹ میں دکھائی دینے والی ٹیلیگرام مشاہدات کو ایک دستخط شدہ جرنل میں محفوظ کرتا ہے۔ موصول کنندگان محفوظ شدہ ریکارڈز، منسلکات اور رپورٹس کی تصدیق ایک قابلِ اعتماد کلیکٹر کلید کے خلاف کر سکتے ہیں، پھر جرنل کا موازنہ ایک آزادانہ طور پر محفوظ کردہ چیک پوائنٹ سے کر سکتے ہیں۔ یہ صفحہ فارمیٹس، چیکس اور حوالگی کے لیے محفوظ رکھنے والے مواد کی وضاحت کرتا ہے۔

Recipients can start with **VERIFY.cmd** on Windows: it asks for the original ZIP and independently obtained key fingerprint, displays an explained result, and saves a separate verification transcript. See [verification launchers and the portable runtime](https://github.com/phishdestroy/TgWitness/blob/main/docs/VERIFICATION_LAUNCHER.md) for setup and trust limits.

## دستخط شدہ کیا ہے

| مواد | حفاظت | کیا برقرار رکھنا ہے |
| --- | --- | --- |
| ہر جرنل مشاہدہ، بشمول آپریشنل واقعات | ہر واقعے کے لیے SHA-256 چین اور Ed25519 دستخط | اصل `events.jsonl`، قابلِ اعتماد کلید کا فنگر پرنٹ، اور ایک برقرار رکھا گیا چیک پوائنٹ |
| شواہد کے زپ کا مواد | `manifest.sig` کینونکل منیفیسٹ پر دستخط کرتا ہے، جو مواد کی فائلوں کے ہیشز کی فہرست دیتا ہے۔ | مکمل ZIP، جس میں اس کا مینیفیسٹ اور دستخط شامل ہیں۔ |
| محفوظ شدہ منسلکات | SHA-256 اور بائٹ کاؤنٹ ایک دستخط شدہ `media.saved` واقعے میں؛ فائل ہیش دستخط شدہ ZIP منیفیسٹ میں | تصدیق شدہ ZIP کے اندر اصل بائٹس |
| چیک پوائنٹ | جرنل کی لمبائی، ہیڈ ہیش، عوامی کلید اور تخلیق کے وقت پر Ed25519 دستخط | متنازع تبدیلی سے پہلے محفوظ کی گئی ایک آزاد کاپی |
| رن رسید | Signed record of the collector version, source-file hashes and start settings, also included in `process.started` | The receipt, associated journal and the environment evidence for the selected verification mode |
| قابلِ مطالعہ رپورٹس: `report.html` اور اس کے اجزاء، `report.json`، `report.pdf`، `chat.pdf` | ہر فائل کے مواد پر ایک Ed25519 مہر؛ PDF میں ایک معیاری PDF دستخط بھی شامل ہے (دیکھیں [قابلِ مطالعہ رپورٹس](https://phishdestroy.github.io/TgWitness/ur/docs/reference/evidence/#readable-reports)) | موصول شدہ فائل اور قابلِ اعتماد کلید کا فنگر پرنٹ؛ وہ ZIP جس کا یہ بیان کرتا ہے |
| خودمختار CSV | کوئی آزاد کرپٹوگرافک دستخط نہیں؛ صرف ایونٹ ہیشز کافی نہیں ہیں۔ | سندیت کی جانچ کے لیے تصدیق شدہ ZIP کے اندر موجود عین نقل استعمال کریں۔ |
| برائوزر کے ذریعے تیار کردہ اسکرین شاٹس، پرنٹ آؤٹس یا پی ڈی ایف | ڈیرائیوویٹڈ پر TgWitness کے دستخط نہیں ہیں۔ | اصلی تصدیق شدہ پیکیج کو محفوظ رکھیں اور دستاویزی طور پر بتائیں کہ مشتق کیسے تیار کیا گیا۔ |

کلیکٹر ہر ایکسپورٹ فارمیٹ بنانے سے پہلے جرنل کے دستخطوں کی تصدیق کرتا ہے۔ قابلِ مطالعہ HTML اور PDF رپورٹس اپنے اپنے سیل رکھتی ہیں؛ خود مختار CSV کو دستخط شدہ ZIP کے حصے کے طور پر چیک کیا جاتا ہے۔ منسلک بائٹس اور مینفیسٹ کو برقرار رکھنے کے لیے ZIP کو محفوظ رکھیں، اور جرنل کو پہلے کے حدِ فاصلے کے خلاف چیک کرنے کے لیے ایک علیحدہ چیک پوائنٹ استعمال کریں۔

## Comparing chat exports

Verify and compare two signed chat-export ZIPs with independently retained signer fingerprints:

```
python -m tgwitness.verify first.zip --compare second.zip \
  --fingerprint FIRST_TRUSTED_KEY_SHA256 --compare-fingerprint SECOND_TRUSTED_KEY_SHA256
```

When both archives record the same numeric account and chat IDs, records are paired by message ID. **Unchanged** means equality of the complete saved JSON record: full text, author, dates, reply target, nested metadata and unknown fields are all included. JSON object key order does not matter; absent fields, nulls, value types and array order do. The 300-character preview is only for display. Changed entries name the differing top-level `changed_fields`, including changes invisible in that preview. Duplicate message IDs are rejected instead of overwriting one another during matching.

A difference can be a changed display name, view count, collection annotation or other observation metadata. It does not by itself establish a Telegram edit, identify who made a change, or prove which contradictory archive is accurate. Unparsed records remain in the comparison; equality of their saved representation does not mean their Telegram payload was decoded.

For different or missing account/chat identities, the tool only finds possible correspondences using sender, complete text, file hash, media type and a five-second time tolerance. It reports **Matched**, not **Unchanged**. These candidates do not establish message identity or equality of all metadata. Unparsed records remain unmatched. Differences in paired records remain listed in `changed`, including in content mode; these differences do not prove edits of the same message. With `--json`, `matched` counts pairs and `unchanged` counts pairs whose complete saved records are equal. Neither count proves message identity in content mode. The existing `changed_fields` and integer `unchanged` output remain compatible with earlier comparison results. Archive format and signature verification are unchanged.

## تحقیقات کی منتقلی

1. اپنے کیس نوٹس میں کیس ریفرنس، آپریٹر، عددی ٹیلیگرام اکاؤنٹ آئی ڈی، منتخب ذرائع، کلیکشن پالیسی، اور کلیکشن کی مدت کو ریکارڈ کریں۔ TgWitness مشاہدات کو محفوظ کرتا ہے اور [کیس بورڈ](https://phishdestroy.github.io/TgWitness/ur/docs/reference/case-board/) میں ماخذ سے منسلک نوٹس اور کلیکشنز کی حمایت کرتا ہے۔ اپنی کیس مواد کے ساتھ منتقلی اور تحویل کے ریکارڈز کو محفوظ رکھیں۔ متوقع کلیکشن سیٹ اپ کو [لائیو قبولیت](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) کے [طریقہ کار](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) کے ساتھ چیک کریں۔
2. اس کے ایکسپورٹس پر انحصار کرنے سے پہلے ورک اسپیس کے پبلک کی فنگر پرنٹ کو آزادانہ طور پر محفوظ رکھیں۔ کلیکشن کے دوران کلیکٹر کے باہر دستخط شدہ چیک پوائنٹس محفوظ کریں۔ رکاوٹوں اور اکاؤنٹ کی نمائش کی حدود کو ریکارڈ کریں۔
3. ایک **دستخط شدہ ZIP** ایکسپورٹ کریں اور دستخط شدہ رن رسید کو محفوظ رکھیں۔ ایک چیک پوائنٹ استعمال کریں یا ایکسپورٹ شدہ جرنل کی حد سے پہلے یا اس پر۔ ایک بعد کا چیک پوائنٹ درست طور پر مسترد کر سکتا ہے پہلے کے ایکسپورٹ کو بہت مختصر ہونے کی وجہ سے۔ ایکسپورٹس مکمل ورک اسپیس جرنل شامل کرتی ہیں، پینل فلٹرز سے قطع نظر؛ شیئر کرنے سے پہلے مواد کا جائزہ لیں۔
4. موصول کنندہ سے کہیں کہ وہ ZIP کو ایک معتبر ویریفائر کی کاپی اور آزادانہ طور پر فراہم کردہ فنگر پرنٹ/چیک پوائنٹ کے ذریعے تصدیق کرے۔ ایک معتبر چیک آؤٹ سے جس کا پائتھن ماحول فعال ہو:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   کامیاب آؤٹ پٹ رپورٹس `key_pinned: true` اور `checkpoint_checked: true` جب دونوں ان پٹس فراہم اور قبول کیے جائیں۔ تصدیقی نتیجہ محفوظ رکھیں۔

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. آرکائیو کا SHA-256، ایکسپورٹ کی حد، منتقلی کی تاریخ، بھیجنے والا اور وصول کنندہ کو اپنے تحویل ریکارڈ میں درج کریں۔ اصل پیکیج کو سالم رکھیں اور کاپیوں پر کام کریں۔ ایپلیکیشن کے نجی ڈیٹا ڈائریکٹری کے بجائے شواہد کی فائلیں شیئر کریں، جس میں اکاؤنٹ سیشنز اور دستخطی راز بھی شامل ہیں۔ منتقلی کے لیے، ایک ایکسپورٹ کو پاس ورڈ سے محفوظ AES-256 ZIP فائل میں رکھا جا سکتا ہے۔ یہ پاس ورڈ صرف رازداری کا تحفظ کرتا ہے اور محفوظ نہیں کیا جاتا؛ وصول کنندہ آرکائیو کو نکالتا ہے اور اندر موجود دستخط شدہ ایکسپورٹ کی تصدیق کرتا ہے، جو کہ تبدیل نہیں ہوتا۔
   2. اگر آزاد وقتی لنگر اندازی درکار ہو تو [RFC 3161 کے طریقہ کار](https://phishdestroy.github.io/TgWitness/ur/docs/reference/timestamp/) پر عمل کریں اور درخواست، چیک پوائنٹ، قابل اعتماد CA کی معلومات، اور تصدیق شدہ اتھارٹی کے جواب کو محفوظ رکھیں۔ صرف درخواست تیار کرنے سے ٹائم اسٹیمپ حاصل نہیں ہوتا۔

کامیاب تصدیق قابلِ اعتماد کلیکٹر کی اور برقرار رکھی گئی حد کے حوالے سے سالمیت قائم کرتی ہے۔ انجام دی گئی چیکس کے لیے اعتماد کے مفروضوں اور [توثیقی نتائج](https://phishdestroy.github.io/TgWitness/ur/docs/reference/verification/) کے لیے [تصدیق کے دائرہ کار](https://phishdestroy.github.io/TgWitness/ur/docs/reference/evidence/#verification-scope) کو دیکھیں۔

## ہینڈ اوور کا خلاصہ

ایک دستخط شدہ زپ پورے ورک اسپیس جرنل کو محفوظ کرتا ہے۔ جب عدالت، وکیل یا کسی بدسلوکی ڈیسک کو صرف چند چیٹس، ایک مخصوص مدت یا مخصوص افراد کی ضرورت ہو، تو **Exports → Handover extract** منتخب کردہ انکشاف کے قواعد کے مطابق ایک مختصر کاپی (`tgwitness-handover-v1`) تیار کرتا ہے۔ آپریٹر مقصد بیان کرتا ہے اور چیٹس، ایک اختیاری مدت (UTC)، اُن افراد کا انتخاب کرتا ہے جن کے بارے میں خلاصہ تیار کیا جا رہا ہے، اور یہ بھی طے کرتا ہے کہ باقی سب کے ساتھ کیا ہوگا (دکھایا جائے، P01 کے فرضی ناموں سے تبدیل کیا جائے، P02… یا خارج کر دیے جائیں)، کون سے پیغامات کے متن شامل رہیں گے، کون سی منسلکات اور پروفائل تصاویر شامل کی جائیں گی، اور آیا پیغامات میں موجود فون نمبرز اور ای میل پتے کو چھپایا جائے یا نہیں۔ مقصد اور یہ قواعد دستخط شدہ منیفیسٹ اور رپورٹ میں موجود ہیں؛ جرنل میں `handover.exported` کو اس رسائی کے ساتھ ریکارڈ کیا جاتا ہے جس نے اسے تیار کیا اور فائل کا SHA-256 شامل ہوتا ہے، نہ کہ اس کا مواد۔

`verify.py` ایک اقتباس کی دو طریقوں سے جانچ کرتا ہے۔ ایک ریکارڈ جو بغیر تبدیلی کے دکھایا گیا ہو مکمل طور پر تصدیق کیا جاتا ہے: اس کا مواد اس کے ہیش، اس کے Ed25519 دستخط اور شامل کردہ سابقہ ریکارڈ کے ساتھ اس کے لنک کے خلاف۔ ایک مختصر کردہ ریکارڈ اصل ہیش اور دستخط کو برقرار رکھتا ہے، لہٰذا دستخط اب بھی تصدیق ہو جاتا ہے، لیکن پوشیدہ کردہ فیلڈز کو اس سے دوبارہ شمار نہیں کیا جا سکتا؛ ریکارڈ میں بتایا جاتا ہے کہ کیا پوشیدہ کیا گیا تھا اور رپورٹ اسے نشان زد کرتی ہے۔ مینفیسٹ میں جرنل کی لمبائی اور سرخی کا ذکر ہوتا ہے، جس پر جمع کرنے والے کے دستخط اس سرخی کے اوپر ہوتے ہیں، اور باقی ماندہ ریکارڈز کی تعداد گنتی ہے؛ `coverage.json` منتخب کی گئی چیٹس کی وضاحت کرتا ہے۔ فائل کے ناموں کے اندر موجود نام معلوم نہیں کیے جاتے۔ شیئر کرنے سے پہلے حتمی فائلوں کا جائزہ لیں: آزاد متن، فائل کے نام اور منتخب کردہ منسلکات اب بھی لوگوں کی شناخت کر سکتے ہیں۔ مکمل دستخط شدہ ZIP کو محفوظ رکھیں: یہ خلاصہ افشاء ہے، متبادل نہیں۔

## قابلِ مطالعہ رپورٹس

دستخط شدہ شواہد، حوالگی اور چیٹ ZIPs میں پڑھنے کے قابل HTML اور JSON رپورٹس شامل ہوتی ہیں، نیز جب مطلوبہ فانٹس دستیاب ہوں تو منتخب کردہ رپورٹ زبان میں PDF بھی۔ ہر رپورٹ کو ورک اسپیس کی Ed25519 کلید کے ساتھ سیل کیا جاتا ہے اور اسے الگ سے تصدیق کیا جا سکتا ہے: `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]`۔

- `report.html` / `chat.html`: سیل بیان (`tgwitness-report-seal-v1`) فائل کو بند کرتا ہے اور اس سے پہلے کے ہر بائٹ کے SHA-256 پر دستخط کرتا ہے۔ طویل جرنلز اور چیٹس کو قابل ترتیب سائز کے حصوں میں تقسیم کیا جاتا ہے (رپورٹ سیٹنگز، 500 سے 100,000 ریکارڈز؛ ڈیفالٹ 5,000): `records/records-0001.html` یا `messages/messages-0001.html`، ہر ایک کو اس کے نمبر، حد اور کل کے ساتھ سیل کیا جاتا ہے، اور دستخط شدہ منسٹ میں اس کے SHA-256 کے ساتھ درج کیا جاتا ہے۔ کلیکٹر ہارٹ بیٹس کے سلسلوں کو ایک ہی لائن کے طور پر دکھایا جاتا ہے جب تک کہ رپورٹ سیٹنگز انہیں ایک ایک کر کے درج نہ کریں۔
- `report.json` (`tgwitness-report-json-v1`، keys `format`، `report`، `seal`): مہر SHA-256 کو JSON کے `report` کے طور پر دستخط کرتی ہے، تاکہ حقائق کیس سسٹمز اور اسکرپٹس کے ذریعے پڑھے جا سکیں اور ڈیٹا پروٹیکشن کے لیے ان میں سے انتخاب کیا جا سکتا ہے جبکہ دستخط شدہ فائل سالم رہتی ہے۔
- `report.pdf` / `chat.pdf`: پرنٹ اور فائلنگ کے لیے ایک رسمی دستاویز، ایک ہی بائٹس پر دو بار دستخط شدہ، دستخطی قدر (`/ByteRange`) کے علاوہ پوری فائل۔ معیاری PDF دستخط (`adbe.pkcs7.detached`، CMS کے ساتھ SHA-256 اور ECDSA P-256) ایک خود جاری کردہ دستاویز پر دستخط کرنے والا سرٹیفکیٹ ورک اسپیس والٹ میں رکھا جاتا ہے؛ اس کا سبجیکٹ سیریل نمبر Ed25519 کلید کا فنگر پرنٹ ہے۔ Ed25519 سیل CMS کے اندر غیر دستخط شدہ خصوصیت `2.25.240684792623320047764573196045913242332` کے طور پر سفر کرتا ہے اور سرٹیفکیٹ کے SHA-256 کو `"content": "pdf-byte-range"` کے ساتھ نام دیتا ہے، لہٰذا Ed25519 کلید سرٹیفکیٹ کی ضمانت دیتی ہے۔ PDF ریڈر بتاتا ہے کہ آیا دستخط کے بعد فائل تبدیل ہوئی ہے اور دستخط کنندہ کو نامعلوم قرار دیتا ہے جب تک کہ سرٹیفیکیٹ پر اعتماد نہ کیا جائے؛ اس کے بجائے Ed25519 فنگر پرنٹ کا موازنہ کریں۔ چینی، جاپانی اور کوریائی پی ڈی ایف کے لیے سرور پر (یا `TGWITNESS_FONT_DIR` میں) ایک فونٹ درکار ہوتا ہے؛ اس کے بغیر زپ صرف HTML اور JSON رپورٹس پر مشتمل ہوتی ہے۔

Telegram ایک چینل یا سپر گروپ میں پیغامات 1، 2، 3… کو ترتیب سے نمبر کرتا ہے۔ ایک چیٹ ایکسپورٹ پہلے اور آخری نمبر، موجود پیغامات کی تعداد اور `message-ids.json` میں غیر موجود نمبروں کے ہر سلسلہ، مینفیسٹ اور `chat.json` ہیڈر کو درج کرتا ہے، اور ٹرانسکرپٹ میں ہر خلا کو نشان زد کرتا ہے۔ `verify.py` ان کو `chat.json` سے دوبارہ گنتا ہے۔ غیر حاضر نمبر وہ پیغام ہوتا ہے جس کا Telegram نے جواب نہیں دیا (ایکسپورٹ سے پہلے حذف کیا گیا، یا اکاؤنٹ کے لیے نظر نہ آنے والا)؛ نجی چیٹس اور بنیادی گروپس میں نمبر اکاؤنٹ کی تمام چیٹس کے ذریعے شیئر کیے جاتے ہیں اور خالی جگہیں شمار نہیں کی جاتیں۔

After reading the history, the export asks Telegram for every absent number again, by number (`channels.getMessages`, up to 10,000 numbers). The result is in `message-ids.json` and the report. An empty answer records that the number is unavailable to this account at recheck time; it leaves the cause unspecified. A message returned on recheck is added to the export and marked `found_on_recheck`.

ہر رپورٹ**کے ساتھ شروع ہوتی ہے مختصراً**: ایک پیراگراف، پھر وہ جو مواد دکھاتا ہے اور جو نہیں دکھاتا (اکاؤنٹ کے پیچھے کون ہے، ترسیل کی مکملیت، مشاہدے سے پہلے حذف شدہ مواد، بغیر ٹائم اسٹیمپ کے گھڑی کا وقت)۔ صفحے کی اپنی سیل اسٹیمپ تیلہِ رنگ کی ہوتی ہے جب براؤزر نے سیل کے دستخط کی تصدیق کی ہو، نہ کہ صفحے کی: ایک براؤزر صفحے کو اس کے اپنے بائٹس فراہم نہیں کرتا۔ یہ صرف اس وقت سبز ہوتی ہے جب قاری فائل کو صفحے کے آخر میں موجود چیک میں ڈالتا ہے اور ہر بائٹ کا میل ہوتا ہے، اور صرف اس صورت میں جب دکھایا گیا صفحہ وہی فائل ہو؛ ورنہ یہ سرخ ہو جاتی ہے۔

ہر رپورٹ پروگرام کا نام بالکل درست بتاتی ہے: وہ git commit جب کلیکٹر ایک چیک آؤٹ سے چلتا ہے یا انسٹالر `TGWITNESS_COMMIT` سیٹ کرتا ہے، اور اس کے ماخذ فائلوں کا SHA-256 (`source_tree_sha256`، path کا معیاری JSON → ہر `.py` کا SHA-256، `.js`، `.css`، `.html` اور `.svg` فائل پیکج میں)، جسے اس کمٹ کا چیک آؤٹ دوبارہ پیدا کرتا ہے جب تک فائلیں تبدیل نہ کی گئی ہوں۔ Telegram کلائنٹ کا نام اس کی لائبریری، API پرت اور ڈیٹا سینٹر کے نام پر رکھا گیا ہے۔ جب مشاہدہ شروع ہوتا ہے اور جب چیٹ ایکسپورٹ شروع اور ختم ہوتا ہے، تو کلیکٹر Telegram سے اس کا وقت (`updates.getState`، مکمل سیکنڈ) پوچھتا ہے اور Telegram کا وقت منہاس کر کے کلیکٹر کی گھڑی کے وقت میں سے، راؤنڈ ٹرپ سے پیدا ہونے والی غیر یقینی صورتحال کے ساتھ ریکارڈ کرتا ہے؛ رپورٹس ان پیمائشوں کو 'چین آف کسٹڈی' کے تحت دکھاتی ہیں۔ ایک چیٹ ایکسپورٹ پیغامات کی تاریخوں کے علاوہ یہ بھی ریکارڈ کرتا ہے کہ اس نے تاریخ کب پڑھی۔

### آف لائن رپورٹ ویوئر اور آرکائیو گائیڈ

`chat.html` یا `report.html` کھولنے سے پہلے مکمل ZIP نکالیں۔ ویوئر تلاش، فلٹرز، شرکاء، اشارے، ریکارڈ کی تفصیلات اور سرور کے بغیر JSON/CSV کے انتخاب فراہم کرتا ہے۔ رپورٹ کے ساتھ `viewer/` اور `media/` رکھیں۔ انتخاب مشتق ہیں: دستخط شدہ آرکائیو کے ساتھ موازنہ کرنے کے لیے `verify.py SELECTION.json
--evidence ARCHIVE.zip` استعمال کریں۔ تصدیق کنندہ رپورٹ آئی ڈی، دستخطی کلید، آرکائیو کی حد اور ہر منتخب شے کی جانچ کرتا ہے؛ ترمیم شدہ، غائب اور ڈپلیکیٹ اشیاء ناکام ہو جاتی ہیں۔ انتخابی نوٹس اور تخلیقی وقت بغیر دستخط شدہ میٹا ڈیٹا رہتا ہے۔

پیغامات کے نمبروں میں وقفے صرف مکمل، غیر فلٹر شدہ صعودی چیٹ فیڈ میں دکھائے جاتے ہیں۔ کسی زمرے کو چھپانے یا ڈیٹا کے ٹکڑے کو لوڈ نہ کرنے سے حذف شدہ قطار کو غائب پیغام کا ثبوت نہیں سمجھا جائے گا۔ تلاش کے نمایاں حصے سادہ متن پر عمل کرتے ہیں، اس سے پہلے کہ 'HTML' کو فرار کیا جائے، اور لفظی مارک اپ کو برقرار رکھتے ہیں۔

براؤزر دستخط شدہ مینیفیسٹ، رپورٹ آئی ڈی اور کلید، اور تمام درج فائل ہیشز کی جانچ کرتا ہے۔ یہ مبہم یا خراب ساخت کے حامل ZIP ڈھانچے، ناموں کی نقل اور غیر محفوظ راستوں کو مسترد کرتا ہے، اور فائلوں کی حد 256 MiB اور کل مواد کی حد 4 GiB مقرر کرتا ہے۔ بڑے آرکائیوز کے لیے خود مختار ویریفائر استعمال کریں۔ یہ براؤزر چیک جرنل چینز اور ڈیٹا کے معنیات کے معائنہ کار کے چیکس کو مکمل کرتا ہے۔

`README.txt` میں ایک آغاز رہنما، ایک ہم آہنگ فائل انوینٹری، تصدیقی ہدایات اور رپورٹ کی زبان میں ڈیٹا فارمیٹ کے نوٹس شامل ہیں، جس کے بعد ایک مکمل انگریزی رہنما آتا ہے۔ `SHA256SUMS` اس میں شامل فائلوں کا احاطہ کرتا ہے، خود کو چھوڑ کر، `manifest.json` اور `manifest.sig`؛ دستخط شدہ منسٹ بھی `SHA256SUMS` کا احاطہ کرتا ہے۔ اصل ZIP کو بغیر تبدیل کیے رکھیں اور کام کرنے والی فائلوں کو نکالی گئی فولڈر کے باہر محفوظ کریں۔ PDF کی رپورٹس میں سیکشن بک مارکس اور کیس/رپورٹ کی شناخت بعد کے صفحات پر شامل ہیں۔

### برآمد کے وقت چیٹ

ایک چیٹ ایکسپورٹ اس بات کو ریکارڈ کرتا ہے کہ جب ایکسپورٹ شروع ہوا تو Telegram نے چیٹ کے بارے میں کیا کہا: Telegram کے اپنے لیبلز (`scam`, `fake`, `restricted` اپنے وجوہات کے ساتھ, `verified`), صارف کے نام, تفصیل, اراکین اور منتظمین کی تعداد, منسلک گفتگو, مواد کی حفاظت, آیا نئے اراکین پرانے پیغامات دیکھ سکتے ہیں اور اس اکاؤنٹ پر تاریخ کون سے پیغام سے دکھائی دیتی ہے (`available_min_id`), پیغام 1 کی تاریخ جب یہ چیٹ کی تخلیق ہو، اور چیٹ کی تصویر کا SHA-256 (`media/` میں محفوظ)۔ یہ برآمد کرنے والے اکاؤنٹ کی چیٹ میں جگہ کو ریکارڈ کرتا ہے: کردار، شمولیت کی تاریخ، کس نے اسے مدعو کیا اور، ایک ایڈمن کے لیے، اس کے حقوق۔ ایک درخواست جسے Telegram مسترد کرتا ہے اسے اس کے بجائے نام دیا جاتا ہے۔

جب برآمد کرنے والا اکاؤنٹ ایڈمن ہو تو ایکسپورٹ چیٹ کے ایڈمن لاگ (Telegram تقریباً 48 گھنٹے محفوظ رکھتا ہے) کو `admin-log.json` میں منتقل کرتا ہے: حذف اور ترامیم کے ساتھ متعلقہ مواد اور کارروائی کرنے والا اکاؤنٹ۔ یہ حذف کی واحد ریکارڈ ہے جو بتاتی ہے کہ کس نے حذف کیا۔

### اشارے

رپورٹس میں فہرست دی گئی ہے، اور آرکائیو میں درج ہے جیسا کہ `indicators.csv` ، `indicators.stix.json` (STIX 2.1 ) اور `indicators.misp.json` (MISP واقعہ)، وہ چیزیں جن پر ایک ابوز ڈیسک ریکارڈ شدہ پیغامات میں کارروائی کر سکتا ہے: لِنکس اور ڈومینز (جو متن کے پیچھے، بٹنوں اور لِنک پریویوز میں بھی چھپے ہوتے ہیں)، کرپٹو کرنسی کے پتے، Telegram کے صارف نام اور دعوت نامے کے لنکس، فون نمبرز، ای میل پتے اور محفوظ شدہ تصاویر۔ بٹ کوائن، لائٹ کوائن، ڈوج کوائن اور ٹرون کے پتے تب ہی درج کیے جاتے ہیں جب ان کا base58 چیک سم درست ہو، سیگ وِٹ پتے تب جب ان کا bech32 یا bech32m چیک سم درست ہو اور ٹون کے پتے تب جب ان کا CRC درست ہو؛ ای وی ایم اور سولانا کے پتے اس طرح نشان زد کیے جاتے ہیں کہ وہ چیک نہیں کیے گئے۔ تصاویر کے ساتھ SHA-256 اور ایک پرسیپچوئل ہیش (dHash، 64 بٹس) ہوتا ہے، جو دوبارہ کمپریس یا ری سائز شدہ کاپیوں میں تقریباً تبدیل نہیں ہوتا۔ رپورٹس میں اشارے اس طرح لکھے جاتے ہیں کہ وہ غلطی سے نہ کھلیں (`hxxps[://]example[.]com` )؛ فائلیں اقدار کو ویسا ہی برقرار رکھتی ہیں جیسا وہ تھیں۔ ہر انڈیکیٹر کو نامعلوم اور خودکار شناخت کے لیے نہیں کے طور پر نشان زد کیا گیا ہے (STIX `indicator_types: unknown` , MISP `to_ids: false` , اپنی تنظیم کو تقسیم): فہرست میں شامل ہونے کا مطلب ہے کہ اس میں ایک پیغام شامل تھا، نہ کہ یہ بدنیتی پر مبنی ہے۔ ایک لنک جس کا متن اس پتے سے مختلف ہو جہاں یہ کھلتا ہے، رپورٹ میں نشان زد کیا جاتا ہے۔

PDF رپورٹس ایک معائنہ کار کے دستخط کے لیے ہاتھ سے لکھے گئے اعلان، ایک نوٹری یا عدالتی ماہر کے لیے چیک لسٹ، اور ایک QR کوڈ (جو پہلے صفحے پر بھی ہوتا ہے) کے ساتھ ختم ہوتی ہیں، جس میں رپورٹ آئی ڈی، کلیدی فنگر پرنٹ اور مستند ڈیٹا کا SHA-256 شامل ہوتا ہے، تاکہ پرنٹ آؤٹ اسے اس کے آرکائیو سے منسلک کر دے۔

## واقعات کی معیاری شکل میں ترتیب

ہیش ان پٹ میں بالکل یہی فیلڈز شامل ہیں:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

Python کے مطابقت رکھنے والے JSON کے ساتھ UTF-8 استعمال کرتے ہوئے سیریلائز کریں، ترتیب شدہ آبجیکٹ کیز کے ساتھ، ASCII ایسکیپنگ کے بغیر، غیر اہم وائٹسپیس کے بغیر، اور NaN/infinity کے بغیر:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

ان بائٹس کا SHA-256 ہی ایونٹ ہیش بن جاتا ہے۔ دستخط 32 خام ہیش بائٹس پر Ed25519 کے ذریعے کیے جاتے ہیں، پھر base64 میں انکوڈ کیے جاتے ہیں۔ پہلا previous_hash 64 صفر پر مشتمل ہوتا ہے۔ سلسلہ وار نمبر 1 سے شروع ہوتے ہیں اور 1 کے اضافے سے بڑھتے ہیں۔ تمام واقعات، بشمول آپریشنل واقعات، ایک ہی چین شیئر کرتے ہیں۔ ڈپلیکیٹ ڈیلیوری کی روک تھام نہیں ہے: بار بار ہونے والی مشاہدات الگ الگ رسیدیں ہیں، نہ کہ الگ الگ ٹیلیگرام کارروائیوں کا دعویٰ۔

خام ٹیلیگرام کی تاریخیں ISO سٹرنگز ہیں؛ بائنری فیلڈز اشیاء میں تبدیل ہوتی ہیں جن میں bytes_base64 شامل ہوتا ہے۔ جب فراہم کیے جائیں تو پیغام کا متن، اکائیوں، میڈیا ڈسکرپٹرز، جوابی میٹا ڈیٹا، ردعمل اور سروس ایکشنز خام پیغام کے میٹا ڈیٹا میں محفوظ کیے جاتے ہیں۔

observed_at کلیکٹر کی UTC وال کلاک ہے۔ source_at ایک فراہم کردہ ٹیلیگرام تاریخ ہے جب دستیاب ہو۔ حذف کرنے کی اطلاعات بالکل درست حذف ہونے کا وقت فراہم نہیں کرتیں، لہٰذا source_at null رہتا ہے۔ ٹرانسپورٹ وصولی کا ترتیب ضروری نہیں کہ ماخذ-واقعے کے ترتیب کے مطابق ہو۔ ہسٹری کے سنپ شاٹس پرانی ماخذ تاریخیں استعمال کرتے ہیں لیکن موجودہ مشاہداتی اوقات استعمال کرتے ہیں۔

## ایکٹر کے معنی

message.new actor_id پیغام بھیجنے والا ہے۔ message.edited کا کوئی اندازہ شدہ مدیر نہیں ہوتا؛ payload.sender_id مشاہدہ شدہ پیغام کے بھیجنے والے کو ریکارڈ کرتا ہے۔ مٹانے والا actor_id null رہتا ہے۔ ممبرشپ سروس کے پیغامات بھیجنے والے اور عمل کی قسم کو برقرار رکھتے ہیں، بغیر ہر ہٹانے کو رضاکارانہ رخصت میں تبدیل کیے۔ خام شرکاء کی تازہ کاریاں فراہم کردہ actor_id کو برقرار رکھتی ہیں۔ ردعمل کے سنپ شاٹس تبدیلی کرنے والے ایکٹر کو ایجاد نہیں کرتے۔

نجی چیٹس اور عام گروپس کے لیے حذف ہونے کی اطلاعات میں صرف میسج آئی ڈیز شامل ہوتی ہیں۔ یہ چیٹس ایک اکاؤنٹ بھر میں ایک ہی آئی ڈی کے تسلسل کا اشتراک کرتی ہیں، لہٰذا ایک آئی ڈی اس اکاؤنٹ کے ایک واحد پیغام کی شناخت کرتی ہے۔ جب اس آئی ڈی والا پیغام پہلے اس جرنل میں محفوظ کیا گیا تھا، تو حذف کرنے کو اس چیٹ میں `message.deleted` کے طور پر ریکارڈ کیا جاتا ہے، جس میں `payload.chat_resolution` کو طریقہ کار کے نام کے طور پر استعمال کیا جاتا ہے۔ وہ آئی ڈیز جنہیں کبھی محفوظ نہیں کیا گیا، انہیں `deletion.unscoped` کے طور پر بغیر کسی `chat_id` کے رکھا جاتا ہے؛ کچھ بھی اندازہ نہیں لگایا جاتا۔ چینلز اور سپر گروپس پیغامات کو فی چیٹ گنتے ہیں اور اس طرح کبھی بھی میچ نہیں کیے جاتے۔ جب حذف شدہ پیغام مشاہدہ شدہ اکاؤنٹ کی طرف سے بھیجا گیا تھا، تو payload.deleted_message_was_outgoing سچ ہوتا ہے؛ حذف کرنے والا اب بھی فراہم نہیں کیا جاتا۔

An unscoped notice does not establish that a message was never saved: a matching chat may be outside the current observation scope, or a unique match may be unavailable. Recheck absence remains a separate observation from a deletion notification in report counts, filters and labels. A later recovery clears the current missing state while preserving the earlier unsuccessful check in the signed history; neither observation establishes a deletion notice.

Multiple IDs resolved to the same chat from one notification are grouped as `deletion.batch`, regardless of their count. The notification does not establish that the entire history was cleared, who performed the deletion, or whether it applied to all participants. Saved outgoing messages do not change these limits. Older journals may contain `history.cleared` events inferred from batches of ten or more IDs, with explanatory text attributing the deletion to the other participant. Those inferences are not supported by the update. Preserve those original signed records, but treat them as grouped deletion notifications; the current interface labels them accordingly.

## کوریج: تسلسل، خلا اور غیر مشاہدہ شدہ آئی ڈیز

ہر دستخط شدہ ZIP میں `coverage.json` شامل ہوتا ہے، HTML رپورٹ اسی خلاصے کے ساتھ کھلتی ہے، اور `verify.py` فائل پر بھروسہ کرنے کے بجائے اسے `events.jsonl` سے دوبارہ حساب کرتا ہے:

- **مسلسل X سے Y تک مشاہدہ کیا گیا۔** ایک دورانیہ `observation.started` کے ساتھ شروع ہوتا ہے اور وقف، رُکاوٹ، ٹیلیگرام کنکشن کھو جانے، سائن آؤٹ، بغیر منظم اختتام کے عمل کے آغاز، یا مشاہدے کے دوران بغیر کسی ریکارڈ کے تین منٹ سے زیادہ کے بعد ختم ہوتا ہے۔ (ہر منٹ میں ہارٹ بیٹس لکھے جاتے ہیں، لہٰذا خاموشی کا مطلب ہے کہ عمل رک گیا، جم گیا یا کمپیوٹر سلیپ موڈ میں چلا گیا)۔ جب **پیرامیٹرز** میں ہارٹ بیٹ وقفہ تبدیل کیا جاتا ہے، تو ہر ہارٹ بیٹ اسے ریکارڈ کرتا ہے اور اجازت یافتہ خاموشی تین وقفوں کی ہوتی ہے، جو کبھی تین منٹ سے کم نہیں ہوتی۔
- **خلائیں** ادوار کے درمیان وقت اور وجہ درج کرتی ہیں۔ آخری ریکارڈ پر اب بھی کھلا ہوا ایک خلا `not_resumed_by_last_record` کے ساتھ نشان زد ہے۔
- **پیغامات کی شناختیں غیر مشاہدہ شدہ ہیں۔** چینلز اور سپر گروپس کے لیے، جو فی چٹ پیغامات کی تعداد درج کرتے ہیں، مشاہدہ شدہ شناختوں کے درمیان غائب شناختیں حدود کے طور پر درج کی جاتی ہیں۔ انہیں غیر*مشاہدہ شدہ* کے طور پر رپورٹ کیا جاتا ہے — حذف شدہ، کبھی بھی فراہم نہ کیے گئے، یا محفوظ شدہ تاریخ سے باہر — کبھی بھی حذف شدہ کے طور پر نہیں۔ نجی چٹس اور عام گروپس ایک اکاؤنٹ بھرے تسلسل کو شیئر کرتے ہیں، لہٰذا ایسے کسی چٹ کے اندر خالی جگہیں کچھ بھی ظاہر نہیں کرتیں اور وہاں درج نہیں ہوتیں۔
- چٹ-سطح کے خلا کے نوٹس (مثلاً ٹیلیگرام کا ایک چینل میں فرق کی بازیابی کے لیے درخواست کرنا) نوٹس کے طور پر شمار کیے جاتے ہیں؛ یہ عالمی کوریج میں خلل نہیں ڈالتے۔

### غائب پیغام نمبر (`gap_summary`)

**پریویو۔** `coverage.json` → `gap_summary` یہ اُن نمبروں کو ناپتا ہے جو ٹیلیگرام نے تفویض کیے اور جنہیں یہ کلیکٹر کبھی نہیں دیکھ سکا۔ ٹیلیگرام ایک چینل یا سپر گروپ میں پیغامات کو ایک بار نمبر دیتا ہے، اور نجی چیٹس، بوٹس اور عام گروپس میں ایک اکاؤنٹ کے لیے ایک بار نمبر دیتا ہے۔ دو مشاہدہ شدہ پیغامات کے درمیان کوئی نمبر یا تو مشاہدہ کیا گیا ہے یا غائب ہے۔ ایک مسلسل رینج ایک مثبت بیان ہے کہ اس میں شامل ہر پیغام کو دیکھا گیا تھا۔ ایک خلا کسی بھی کردار اور کسی بھی وجہ کا ذکر نہیں کرتا۔

| میدان | معنی |
| --- | --- |
| `status` | `on`، یا `off` جب **پیرامیٹرز → گیپ اینالیسس** میں بند کیا جائے |
| `parameters` | وہ پیرامیٹرز جنہوں نے یہ نتیجہ دیا، تاکہ اسے دہرایا جا سکے |
| `chats[]` | ہر چینل یا سپر گروپ کے لیے ایک اندراج، ہر ایک کو الگ نمبر دیا گیا |
| `account` | تمام اکاؤنٹ پر پھیلی نجی چیٹس، بوٹس اور عام گروپس کا تسلسل |
| `status` (فی ترتیب) | `applicable`، یا `not_applicable` کے ساتھ `reason` |
| `observed_from`, `observed_to`, `span` | سب سے پہلے اور سب سے آخری مشاہدہ شدہ نمبر اور رینج کا سائز |
| `observed`, `observed_without_content` | مشاہدہ شدہ اعداد؛ وہ جو صرف حذف کرنے یا دوبارہ چیک کرنے کے ریکارڈ سے معلوم ہوتے ہیں |
| `missing`, `density`, `gap_ranges`, `largest_gap` | کبھی بھی مشاہدہ نہ ہونے والے اعداد، رینج میں ان کا حصہ، کتنے رنز، طویل ترین رن |
| `clusters[]` | درج کردہ خلائیں: `low`, `high`, `missing`، اور ملحقہ مشاہدہ شدہ اعداد `after` / `before` ان کے مشاہدے کے اوقات کے ساتھ |
| `service_estimate` | صرف فعال ہونے پر: کتنے غائب نمبرز ان کے مشاہدہ شدہ تناسب کے مطابق سروس پیغامات ہوں گے۔ کبھی بھی منہا نہیں کیا جاتا۔ `missing` |

صحیحیت جرنل سے ماخوذ ہوتی ہے، کبھی مفروضہ نہیں ہوتی:

- **چینلز اور سپر گروپس** ہر چیٹ کے لحاظ سے ناپے جاتے ہیں، منتخب کردہ چیٹس کی ایکسپورٹ میں بھی۔ بھیجنے والے کی جانب سے منتخب کردہ ریکارڈز پیمائش کا تعین کرتے ہیں۔ `not_applicable`.
- **پورے اکاؤنٹ کے لیے سلسلہ** صرف پہلے پیغام سے آخری پیغام تک ناپا جاتا ہے جو اس دوران موصول ہوئے جب پورے اکاؤنٹ کی کلیکشن آن تھی اور نجی چیٹس، بوٹس، عام گروپس اور اکاؤنٹ کے اپنے پیغامات کو برقرار رکھا گیا، کسی بھی چیٹ کو خارج نہیں کیا گیا (`scope.changed`). جن اعداد کا نام رکھا گیا `deletion.unscoped` بغیر مواد کے مشاہدہ شدہ کے طور پر شمار کیے جاتے ہیں۔ منتخب چیٹس کی ایکسپورٹ یا حوالگی اسے ماپ نہیں سکتی۔ اگر پورے اکاؤنٹ کی کلیکشن بند اور پھر آن کی گئی، تو ایک نوٹ میں کہا گیا ہے کہ اس دوران استعمال ہونے والے نمبر خلا کے طور پر ظاہر ہوتے ہیں۔
- سروس پیغامات جرنل کے ریکارڈز ہیں جن کے اپنے نمبر ہوتے ہیں، اس لیے یہ خود ہی اپنے خلا پُر کر لیتے ہیں؛ اختیاری تخمینہ صرف سیاق و سباق ہے۔

`verify.py` دوبارہ حساب `gap_summary` کی طرف `events.jsonl` دستیاب پیرامیٹرز کے ساتھ دستخط شدہ `coverage.json` ممبر (پرانے آرکائیوز کے لیے ڈیفالٹ) اور اپنے کوریج سمری میں اکاؤنٹ بھر کی لائن پرنٹ کرتا ہے۔ آرکائیو کا `get_capture_status`(MCP اور کمانڈ لائن) ان چیٹس کے لیے ایک ہی پیمائش واپس کرتا ہے جو ایک رسائی پڑھ سکتی ہے؛ پورے ورک اسپیس کو کور کرنے والی رسائی کے لیے ہی اکاؤنٹ بھرے سلسلہ کو دکھاتا ہے۔

Repeated observations of one service message count once, and the account service estimate uses only numbers inside the measured range. An applied scope must explicitly preserve the account's own messages before account-wide measurement is enabled; older records without that information cannot establish this condition. Stopped observation does not extend the measured range, and resuming it is noted. The live archive query has a time budget, including its database scan, and marks an unfinished measurement as partial.

Telegram documents the [separate message ID sequences](https://core.telegram.org/api/updates#message-id-sequences). These numbers describe observations; they do not identify a deletion actor or establish why a number is absent.

جب Telegram اکاؤنٹ قبول کرنا بند کر دیتا ہے، تو `coverage.gap` ریکارڈ جو مشاہدہ ختم کرتا ہے، اس میں `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended` یا `not_authorized`) اور Telegram ایرر شامل ہوتا ہے؛ `verify.py` اس وجہ کا نام بتاتا ہے جہاں مدت ختم ہوتی ہے۔

Coverage combines recorded observation periods, interruptions and message outcomes. Assess it together with the selected chats, period and attachment policy; continuous operation alone does not establish complete delivery of Telegram updates.

## تخلیق کار

ثبوت ZIPs، چیٹ ایکسپورٹس، ویٹنس جرنلز اور پیپل-پروفائل فائلوں کے بیان کے دستخط شدہ مینیفیسٹ میں `producer` شامل ہے: سافٹ ویئر، ورژن، پروجیکٹ (PhishDestroy)، ہوم پیج اور سورس ریپوزیٹری۔ HTML رپورٹ اسی لائن کو دکھاتی ہے، اور `verify.py` اسے اس کے تصدیق شدہ حصے کے طور پر پرنٹ کرتا ہے۔ اس فیلڈ کے وجود میں آنے سے پہلے بنائے گئے آرکائیوز پہلے کی طرح تصدیق کرتے ہیں اور ان میں پروڈیوسر کا نام نہ ہونے کی رپورٹ کی جاتی ہے۔

ہر `observation.started` ریکارڈ میں اس Telegram کلائنٹ کا نام بھی شامل ہوتا ہے جس نے مشاہدہ کیا: اس کا `api_id` (کبھی ہیش نہیں)، چاہے وہ بلٹ ان پبلک جوڑا ہو یا آپریٹر کی اپنی ایپلیکیشن، Telegram کے کنکشن ریکویسٹ میں بھیجا گیا کلائنٹ کا بیان، اور کنکشن روٹ کی قسم IP موڈ کے ساتھ (کوئی پروکسی ایڈریس یا سیکرٹ نہیں)۔ رپورٹ اور `custody.json` میں ہر منفرد کلائنٹ اور راستے کو اس کے ریکارڈ کیے جانے کے وقت کے ساتھ درج کیا جاتا ہے، اور وہ اوقات بھی درج ہوتے ہیں جب کسی بھی درج شدہ پراکسی نے جواب نہیں دیا اور Telegram نے سرور کا پتہ دیکھا۔ اس سے پہلے ریکارڈ کیے گئے جرنلز میں بھی یہی بتایا گیا ہے۔

## افراد کے پروفائلز

ایک پروفائل فائل (`tgwitness-dossier-v1`، JSON) ایک چیٹ کے لیے جرنل میں پہلے سے موجود ریکارڈز کی درخواست پر بنائی جاتی ہے؛ ٹیلیگرام سے کچھ بھی حاصل نہیں کیا جاتا اور پروفائل کا مواد کبھی بھی جرنل میں نہیں لکھا جاتا (پروفائلز کو آن اور آف کرنا `dossier.changed` کے طور پر ریکارڈ کیا جاتا ہے)۔ ہر ایس شخص کے لیے جس کا پیغام محفوظ ہو، یہ نام اور صارف نام کی تاریخ، ٹیلیگرام کے جھنڈے (بوٹ، فراڈ، جعلی، پریمیم، تصدیق شدہ، محدود، حذف شدہ) جیسا کہ محفوظ کرنے کے وقت نظر آئے، پروفائل فوٹو آئی ڈیز، لوکل اوتار کیش میں موجود مشابہ اوتاروں کے لیے SHA-256 اور پرسیپچوئل ہیش (pHash، جو `imagehash.phash` کے ساتھ مطابقت رکھتا ہے)، سرگرمی (پہلا اور آخری پیغام، تعداد، ترمیم شدہ اور حذف شدہ شیئرز، UTC گھنٹے کے مطابق پیغامات)، کون کس کو جواب دے رہا ہے، دیگر چیٹس اس جرنل میں جہاں اس شخص نے لکھا، اور والیٹس (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL; Base58Check پتے چیک سم کے ذریعے تصدیق شدہ ہیں)، فون نمبرز، صارف کے نام اور لنکس، بشمول متن کے پیچھے چھپے ہوئے لنکس شامل ہیں۔

ہر حقیقت میں اس جرنل ریکارڈ (`seq`) کا ذکر ہوتا ہے جس سے یہ ماخوذ ہے، اور `record_hashes` ہر حوالہ شدہ ریکارڈ کا ہیش رکھتا ہے۔ بیان کو ورک اسپیس کلید کے ساتھ دستخط کیا گیا ہے:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

دستخط کی تصدیق کرتا ہے، خود ثبوت کی برآمد (دستخط، ہیش چین اور فائلیں) کی توثیق کرتا ہے اور یہ کہ ہر حوالہ شدہ ریکارڈ اسی ورک اسپیس کی برآمد میں بغیر تبدیلی کے موجود ہے۔ اوتار کے ہیشز کو مقامی کیش سے آئے ہوئے کے طور پر لیبل کیا گیا ہے (جرنل ریکارڈز نہیں)۔ ذکروں کا میچ پیٹرن کے مطابق ہوتا ہے — یہ تصدیق شدہ حقائق نہیں بلکہ جانچ کے لیے اشارے ہیں۔ پروفائلز ہر چیٹ کے لیے الگ فعال کیے جاتے ہیں، AES-256 ZIP پاس ورڈ کے ساتھ برآمد کیے جا سکتے ہیں، اور جب انہیں بند کیا جائے یا چیٹ کو ذرائع سے ہٹایا جائے تو حذف ہو جاتے ہیں۔

## آزاد شاہد

ایک گواہ جرنل (`tgwitness-witness-v1`) اور اس کی چینل پوسٹس کا موازنہ `verify.py --witness … --channel …` کے ساتھ شواہد کی برآمد سے کیا جاتا ہے؛ [آزاد گواہ](https://phishdestroy.github.io/TgWitness/ur/docs/reference/witness/) دیکھیں۔

## منفیسٹ اور چیک پوائنٹس

manifest.json میں فارمیٹ، ایکسپورٹ کا وقت، پبلک کی، فنگر پرنٹ، جرنل کی لمبائی، ہیڈ ہیش، اسکوپ، پروڈیوسر، حدود، اور ہر مواد کے رکن کا SHA-256 شامل ہوتا ہے، سوائے خود `manifest.json` اور `manifest.sig` کے۔ manifest.sig کینونکل مینیفیسٹ JSON پر base64 Ed25519 دستخط ہے۔ تصدیق کنندہ غیر متوقع/غائب ارکان، ڈپلیکیٹ نام، خراب فائلیں، ٹوٹی ہوئی ترتیب/سلسلے، غیر معتبر دستخط، اور فراہم کردہ چیک پوائنٹ کے ساتھ عدم مطابقت کو مسترد کر دیتا ہے۔ یہ کبھی بھی آرکائیو راستے (archive paths) نکالنے کی کوشش نہیں کرتا۔ یہ کل اعلان کردہ غیر کمپریسڈ سائز کو 4 GiB تک محدود کرتا ہے؛ `--max-gib N` بڑھائی گئی **پیرامیٹرز** حد (**Parameters** limit) کے ساتھ بنائے گئے بڑے آرکائیوز کی اجازت دیتا ہے۔

Run verification from your installed TgWitness version or a reviewed checkout. The copy included in an archive supports portable use; check that copy against your trusted installation before executing it.

A checkpoint signs a statement containing the public key, journal length, head hash, and creation time. The verifier can check that a later archive contains the same prefix. Retain the checkpoint outside the collector, so later verification compares the archive with a reference held separately from it.

## تصدیق کا دائرہ

Verification checks the archive and the collection mode used to produce it. Choose the mode whose trust boundary matches the case, then retain its verification inputs.

| جمع کرنے کا موڈ | تصدیق کنندہ کیا چیک کرتا ہے | تصدیقی ان پٹس اور اعتماد کی حد |
| --- | --- | --- |
| مقامی ورک اسپیس | Record signatures, hash chain, manifest and attachment bytes | Independently retained collector fingerprint; the host administrator controls the local signing key |
| ایک آزاد گواہ کے ساتھ مقامی ورک اسپیس | آرکائیو چیک کرتا ہے اور گواہ کے ذریعہ برقرار رکھے گئے پہلے جرنل کے پیش‌نام سے اتفاق کرتا ہے۔ | Separately trusted witness key and records; the checkpoint binds the prefix already observed |
| [GitHub Actions کیپچر](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) | GitHub attestation of the archive digest, approved workflow and collector commits, hosted runner, fresh session/key origin and internal archive integrity | Trusted verifier policy, caller repository and GitHub attestation bundle; collection runs under the pinned workflow |
| [کلاؤڈ تعیناتی](https://phishdestroy.github.io/TgWitness/ur/docs/reference/high-assurance/) | Provider lifecycle and access records, firewall and Cloudflare state, plus the collector's signed run record | Read-only queries to the provider and Cloudflare; availability of individual checks depends on the provider |
| [Intel TDX خفیہ مجازی مشین](https://phishdestroy.github.io/TgWitness/ur/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx) | Quote signature and platform status, binding to the collector statement, compose and OS measurements | Intel trust chain and expected deployment measurements; retain the results of every required TDX check |

In sealed acquisition, the approved collector receives data through an authenticated Telegram connection inside the verified environment. Attestation binds the archive to that execution, so verification covers acquisition as well as later file integrity. This relies on the approved code and the platform trust chain listed above. GitHub capture verification requires a session created inside the run and rejects imported-session captures.

The run receipt records the collector version, file hashes and startup settings. GitHub provenance and TDX measurements provide the environment checks; the [validation record](https://phishdestroy.github.io/TgWitness/ur/docs/reference/verification/) identifies tested configurations.

TgWitness signs the observations it collects; Telegram and message authors do not issue these signatures. In a local workspace, material created before the first independent checkpoint still depends on the collector and its key holder. Coverage records describe the selected scope and collection outcomes, while verified external timestamps anchor the committed archive or journal boundary in time.

## منسلکات

فائلیں media/ کے تحت SHA-256 کے ذریعے پتے جاتے ہیں۔ media.saved واقعہ ایک ہیش اور بائٹ کی لمبائی کو ایک مخصوص پیغام کے واقعے سے منسلک کرتا ہے۔ خام فائل کے نام میٹا ڈیٹا ہیں، کبھی بھی مقامی راستے نہیں۔ میڈیا بائٹس غیر ہم آہنگ (asynchronously) ڈاؤن لوڈ کیے جاتے ہیں، لہٰذا فوری حذف کرنے سے ان کی گرفتاری (capture) رک سکتی ہے۔ غیر فعال شدہ کلیکشن، حد سے زیادہ/نامعلوم سائز والی فائلیں، ڈاؤن لوڈ کی ناکامیاں، اور منقطع شدہ ڈاؤن لوڈز نتائج کے طور پر ظاہر ہوتے ہیں۔ پراسیس کے کریش ہونے سے غیر متعلقہ (unreferenced) جزوی فائلیں رہ سکتی ہیں؛ یہ ایکسپورٹس میں شامل نہیں ہوتیں۔

ZIP ایکسپورٹر محفوظ شدہ میڈیا کو اس کے ناموں کے خلاف تصدیق کرتا ہے۔ JSONL، CSV، اور HTML ایکسپورٹس ایونٹ سگنیچرز کی تصدیق کرتے ہیں لیکن میڈیا بائٹس منتقل نہیں کرتے۔ مشتق رپورٹس سہولت کے لیے ہیں؛ events.jsonl ہی مستند ایونٹ نمائندگی ہے۔

ایک مکمل چیٹ ایکسپورٹ، ورک اسپیس کی اٹیچمنٹ سیٹنگز کے اندر منسلکات کو media/ میں محفوظ کرتا ہے، جن کے نام SHA-256 ہیں۔ chat.json میں ہر پیغام کے ریکارڈ میں اپنی فائل کا نام (`file`، `file_sha256`) یا اس کی غیر موجودگی کی وجہ (`file_status`) درج ہوتا ہے، اس کے ساتھ قاری نے متن کے گرد جو کچھ دیکھا وہ بھی شامل ہوتا ہے: متن کے پیچھے کے لنکس، بھیجنے والا، بوٹ بٹنز، دستخط، ویوز اور خود بخود حذف ہونے کا ٹائمر۔ `verify.py` اس بات کی تصدیق کرتا ہے کہ ہر نامزد فائل اس ہیش کے تحت دستخط شدہ مینفیسٹ میں موجود ہے۔

## دیرپا جمع‌آوری اور رسیدوں کا عمل (0.2)

ایک میڈیا جاب اور اس کا میسج ایونٹ ایک ہی ٹرانزیکشن میں کمٹ ہوتے ہیں۔ جاب اصل TL میسج ڈسکرپٹر کو محفوظ کرتا ہے؛ دستخط شدہ مشاہدہ اس کی SHA-256، اکاؤنٹ، اور سائز پالیسی کو منسلک کرتا ہے۔ بحالی ڈاؤن لوڈ کرنے سے پہلے اس وابستگی کی تصدیق کرتی ہے۔ یہ کبھی بھی موجودہ پیغام کو حاصل نہیں کرتا اور خاموشی سے ایک نئے منسلکے کو تبدیل کر دیتا ہے۔ منقطع شدہ جابز کو دوبارہ آزمایا جاتا ہے، جبکہ مستقل ناکامی ایک واضح نتیجہ رہتی ہے۔

Each workspace has its own journal and signing identity. A process.started event includes a run ID, local clocks, dependency versions, source-file hashes, initial account/scope, and capture settings. Heartbeats include the run ID, monotonic time, and queue state. The run receipt can also be downloaded as a separately signed statement. For verification of the execution environment, pair it with the GitHub attestation or TDX checks described in [Verification scope](https://phishdestroy.github.io/TgWitness/ur/docs/reference/evidence/#verification-scope).

Automatic checkpoints are retained locally on startup, every five minutes while observing (**Parameters → Signed checkpoint every**), and on orderly stop. Startup verification and export compare the journal against the latest retained local checkpoint. This can detect a database rollback when the checkpoint survives. Independent retention keeps that reference available outside the workspace; a verified external timestamp additionally anchors it in time.

ری اسٹارٹ کے بعد محفوظ شدہ ٹیلیگرام اپ ڈیٹ پوزیشن بحال کی جاتی ہے (`catch_up_from` میں `observation.started`) اور رہ جانے والی اپ ڈیٹس کی درخواست کی جاتی ہے۔ ایک دورانیے وار دوبارہ چیک رہ جانے والے پیغامات کے لیے `message.recovered` اور جب ٹیلیگرام مزید محفوظ شدہ پیغام واپس نہیں کرتا تو `message.missing_on_recheck` کو ریکارڈ کرتا ہے؛ یہ دوسرا نوٹس حذف کرنے کی اطلاع نہیں ہے اور نہ ہی حذف کرنے والے یا وقت کا ذکر کرتا ہے۔

### آف سائٹ کاپی اور بحالی (S3)

آف سائٹ کاپی (ایکسپورٹس، ڈیفالٹ طور پر غیر فعال) جرنل کے حصے، محفوظ شدہ فائلیں، چیک پوائنٹس ان کے ٹائم اسٹیمپ کے ساتھ اور مکمل چیٹ ایکسپورٹس کو S3-مطابقت پذیر اسٹوریج میں اپ لوڈ کرتی ہے، انکرپٹڈ کے ساتھ AES-256-GCM کے ساتھ انکرپٹ کیے جاتے ہیں، اپ لوڈ سے پہلے ورک اسپیس والٹ میں محفوظ کی گئی کلید کے تحت؛ جب بکیٹ اس کی حمایت کرتا ہے تو آبجیکٹ لاک ریٹینشن لاگو ہوتی ہے۔ ڈاؤن لوڈ کی گئی کلید کے بغیر کاپی پڑھی نہیں جا سکتی۔ بحال کریں اور تصدیق کریں `python -m tgwitness.replica restore --key-file KEY.json --out DIR` کے ساتھ۔

بحالی کے لیے ایک خالی عام ڈائریکٹری درکار ہوتی ہے۔ ڈاؤن لوڈ کی گئی اور ڈی کرپٹ شدہ اشیاء نجی عارضی اسٹوریج میں تب تک رہتی ہیں جب تک پورا جریدہ اور ہر محفوظ شدہ چیک پوائنٹ کی تصدیق نہ ہو جائے۔ غیر محفوظ آبجیکٹ پاتھز، غیر مطابقت پذیر سگمنٹ رینجز اور ایک چیک پوائنٹ سے کم طویل جریدے مسترد کر دیے جاتے ہیں؛ ناکام تصدیق کے بعد کوئی بحال شدہ فائل شائع نہیں ہوتی۔ ریٹینشن چیکس واپس کیے گئے آبجیکٹ لاک موڈ اور تاریخ کا موازنہ اپ لوڈ کے وقت بھیجی گئی ڈیڈ لائن سے کرتے ہیں (گولائی کی ایک سیکنڈ تک کی رواداری کے ساتھ)۔ ایک ختم شدہ، غیر درست یا مختصر ڈیڈ لائن کو تصدیق شدہ نہیں سمجھا جاتا۔ اسٹٹس اس نمونے والے آبجیکٹ کی رپورٹ دیتا ہے جس کی ریٹینشن اس اپ لوڈ پاس کے لیے واپس پڑھی گئی تھی۔

غائب یا خراب مقامی میڈیا کو پاس کی خرابی کے طور پر رپورٹ کیا جاتا ہے اور میڈیا کرسر کو اس کے سامنے روکا جاتا ہے، تاکہ فائل کو اگلے پاس میں دوبارہ آزمایا جا سکے؛ اس کے بعد والی فائلز، چیک پوائنٹس اور ایکسپورٹس پھر بھی کاپی کیے جاتے ہیں۔ بحالی چیکس تمام محفوظ شدہ میڈیا کے حوالوں کو ڈی کرپٹ شدہ ہیشز اور ریکارڈ شدہ سائزز کے خلاف چیک کرتے ہیں۔ رکے ہوئے اپ لوڈز کے یکساں اوورلیپنگ جرنل کے حصوں کو ڈی ڈوپلیکیٹ کیا جاتا ہے؛ متصادم اوورلیپز کو مسترد کر دیا جاتا ہے۔ اپ لوڈ کے دوران بنائے گئے چیک پوائنٹس کو اس وقت تک ملتوی کر دیا جاتا ہے جب تک کہ ان کے متعلقہ جرنل ریکارڈز کی کاپی نہ ہو جائے، تاکہ ایک مکمل پاس اپنے جرنل سے آگے کوئی چیک پوائنٹ شائع نہ کرے۔

### اسٹریمنگ ایکسپورٹ کے سنپ شاٹس

اسٹریمنگ ایکسپورٹس ایک مستحکم SQLite ریڈ سنپ شاٹ استعمال کرتی ہیں۔ جب ڈاؤن لوڈ مکمل ہو جائے تو اس کا ہیڈ موجودہ لائیو جرنل سے پرانا ہو سکتا ہے۔ اس سنپ شاٹ کے بعد بنایا گیا چیک پوائنٹ درست طور پر رپورٹ کر سکتا ہے کہ آرکائیو مختصر ہے؛ ایکسپورٹ کیے گئے پری فکس پر یا اس سے پہلے کے چیک پوائنٹ سے موازنہ کریں، نہ کہ کسی من مانی بعد کے چیک پوائنٹ سے۔

## RFC 3161 کی تیاری اور جواب کی تصدیق (0.2)

شواہد موڈ (ڈیفالٹ طور پر بند) ہر دستخط شدہ چیک پوائنٹ کا صرف SHA-256 درج کردہ RFC 3161 حکام اور OpenTimestamps کیلنڈرز کو ورک اسپیس راستے کے ذریعے بھیجتا ہے اور کبھی بھی MTProxy کے ذریعے نہیں۔ جوابات `checkpoints/anchors/` میں محفوظ کیے جاتے ہیں، برآمد کیے جاتے ہیں، اور `verify.py` کے ذریعے چیک کیے جاتے ہیں (`--tsa-ca` TSA دستخط کی تصدیق کرتا ہے؛ OpenTimestamps کے ثبوتوں کی تصدیق `ots upgrade` اور `ots verify` کے ساتھ کریں)۔

پینل ایک درخواست کا آرکائیو تیار کرتا ہے جس میں معیاری checkpoint.json بائٹس، ایک SHA-256 پیغام کا امپرینٹ اور timestamp.tsq میں بے ترتیب نونس، چیک سمز، اور ہدایات شامل ہوتی ہیں۔ کوئی نیٹ ورک درخواست نہیں کی جاتی۔ تیاری ایک قابلِ اعتماد ٹائم اسٹیمپ نہیں ہے۔

`python -m tgwitness.anchor verify` دو بار OpenSSL ts کو کال کرتا ہے: ایک بار چیک پوائنٹ بائٹس کے خلاف اور ایک بار اصل درخواست کے خلاف۔ ایک معتبر CA فائل کی واضح طور پر ضرورت ہے؛ شامل کردہ سرٹیفیکیٹس خود بخود قابلِ اعتماد نہیں ہوتے۔ CLI پر درخواست کی جانچ اختیاری ہے، لہٰذا نانسی (nonce) کی جانچ کے لیے --request استعمال کریں۔ نتیجہ بتاتا ہے کہ آیا اسے چیک کیا گیا تھا۔ کلیکٹر کے چیک پوائنٹ کے دستخط اور جرنل کو اب بھی قابلِ اعتماد کلیکٹر فنگر پرنٹ کے ساتھ علیحدہ طور پر تصدیق کرنا ضروری ہے۔

تصدیق جواب کے دستخط، چیک پوائنٹ بائٹس اور، فراہم کیے جانے پر، مخصوص CA اعتماد کے تحت اصل درخواست کی جانچ کرتی ہے۔ منسوخی کی جانچ اور سرٹیفیکیٹ کی میعاد ختم ہونے کے بعد طویل مدتی آرکائیول کی توثیق موجودہ مصدق کے دائرہ کار سے باہر ہیں۔ [طریقہ](https://phishdestroy.github.io/TgWitness/ur/docs/reference/timestamp/) [کار](https://phishdestroy.github.io/TgWitness/ur/docs/reference/timestamp/) اور [توثیقی نتائج](https://phishdestroy.github.io/TgWitness/ur/docs/reference/verification/) دیکھیں۔

## شہادت کے موڈ میں اختیاری ریکارڈز: drand اور Telegram ڈیوائسز

دو مزید ریکارڈز ٹائم اسٹیمپ کے ساتھ ایک ہی پاسز پر چل سکتے ہیں۔ دونوں ڈیفالٹ طور پر بند ہیں اور صرف تب اثر کرتے ہیں جب ایویڈنس موڈ آن ہو: اضافی → شواہد اور بیک اپس → **مزید گواہان · اختیاری**، یا `"drand": true` اور `"devices": true` میں `POST /api/evidence`۔ ایک کی خرابی دوسرے یا ٹائم اسٹیمپ کو نہیں روکتی؛ پینل فارم کے نیچے ہر ایک کے تازہ ترین نتائج دکھاتا ہے۔

**drand** (`beacon.drand` ). ہر پاس drand quicknet کے تازہ ترین راؤنڈ کو لکھتا ہے، جو لیگ آف اینٹروپی کی عوامی بے ترتیبی ہے (ہر 3 سیکنڈ میں ایک راؤنڈ)، جرنل میں: `chain` ، `round` ، `randomness` ، `signature` ، `round_time` اور وہ `relay` جس نے جواب دیا۔ ایک تصدیق شدہ غیر متوقع راؤنڈ بعد کے ہیش-لنکڈ مواد کے لیے ایک نچلا وقتی حوالہ فراہم کرتا ہے۔ بعد کے چیک پوائنٹ پر ایک تصدیق شدہ ٹائم اسٹیمپ ایک اعلیٰ زمانی حوالہ فراہم کرتا ہے۔ یہ چیکز منسلک مواد کو محدود کرتے ہیں؛ کلیکشن کی کوریج کا اندازہ علیحدہ طور پر لگایا جاتا ہے۔ کلیکٹر پہلے `drand.cloudflare.com` سے پوچھتا ہے، پھر ورک اسپیس راستے کے ذریعے پروٹوکول لیبز کے ریلیز سے، ہر پاس میں ایک درخواست۔

`verify.py` یہ چیک کرتا ہے کہ ہر بے ترتیب پن اپنے دستخط کا SHA-256 ہے اور راؤنڈ کا وقت درست ہے، اور راؤنڈز، ایک کے بغیر سب سے طویل وقفہ اور کلیکٹر کی گھڑی drand سے کتنی پیچھے تھی، رپورٹ کرتا ہے۔ یہ BLS دستخط کی جانچ نہیں کرتا۔ `--check-drand` راؤنڈز کا موازنہ Cloudflare ریلے اور Protocol Labs ریلے کے ساتھ کرتا ہے، ان سب کے ساتھ یا ایک طویل جریدے میں 100 کے بے ترتیب نمونے کے ساتھ؛ اگر کوئی راؤنڈ مختلف ہو تو توثیق ناکام ہو جاتی ہے۔

**Telegram ڈیوائسز** (`account.devices`). ہر پاس اکاؤنٹ کے سیشنز کو پڑھتا ہے `account.getAuthorizations`، وہ فہرست جو ٹیلیگرام سیٹنگز → ڈیوائسز میں دکھاتا ہے، اور اسے ریکارڈ کرتا ہے: پوری طرح جب یہ پچھلی پاس کے بعد تبدیل ہوئی ہو، کے ساتھ `added` اور `removed` سیشن ہیشز، ورنہ صرف اس کی گنتی اور SHA-256۔ ڈیوائس ماڈل، پلیٹ فارم، ایپ اور ورژن، تخلیق اور آخری سرگرمی، ملک اور خطہ محفوظ رکھا جاتا ہے؛ IP پتے نہیں، کیونکہ شواہد کی برآمدات آپ کے ہاتھ سے نکل جاتی ہیں۔ جمع کرنے والا اپنا سیشن ہر وقت فعال رکھتا ہے، لہٰذا صرف دوسرے سیشنز کی سرگرمی کو تبدیلی کے طور پر شمار کیا جاتا ہے۔ `verify.py` یہ رپورٹ کرتا ہے کہ فہرست کتنی بار ریکارڈ کی گئی اور ہر نئے اور ختم ہونے والے سیشن کے بارے میں۔ یہ فہرست صرف تب پڑھتا ہے جب مشاہدہ چل رہا ہو۔

جو وہ نہیں دکھاتے: drand عوامی وقت کے خلاف ریکارڈز کے ترتیب سے زیادہ کچھ ثابت نہیں کرتا، اور ڈیوائس کی فہرست جمع کنندہ کے ذریعے Telegram کا بیان ہے، جس پر ہر دوسرے ریکارڈ کی طرح جمع کنندہ نے دستخط کیے ہیں۔

**Cloudflare گیٹ وے لاگ** (`cloudflare.gateway_dns`). ایک سرور کے لیے جو Cloudflare Gateway ([Gateway DNS](https://phishdestroy.github.io/TgWitness/ur/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)) کے ذریعے حل کرتا ہے، ہر پاس اس کا نقل کرتا ہے جو Gateway نے پچھلی نقل کے بعد لاگ کیا ہے: ہر تین گھنٹے کے زیادہ سے زیادہ ونڈو کے لیے ایک ریکارڈ کے ساتھ `from`, `until`، سرور کا `location_id`، سرور کا `address` جب ایک سیٹ ہو، اور `queries` کی طرح `[at, name, type, rcode, decision, colo]`، نیز جب کوئی نہ ہوں۔ اسے **Cloudflare Gateway لاگ** کے تحت سیٹ کریں: اکاؤنٹ، مقام، اختیاری پتہ اور ایک ریڈ-ونلی ٹوکن (اکاؤنٹ اینالیٹکس ریڈ؛ شیئرڈ لوکیشن کے ایک پتہ کو محفوظ رکھنے کے لیے زیرو ٹرسٹ PII ریڈ)۔ پینل محفوظ کرنے سے پہلے ایک درخواست کے ساتھ ان کی تصدیق کرتا ہے؛ ٹوکن انکرپٹڈ رہتا ہے اور کبھی جرنل میں داخل نہیں ہوتا۔ `verify.py` ونڈوز کی فہرست دیتا ہے، وہ نام جو سب سے زیادہ تلاش کیے گئے اور کوئی بھی وقت جب کوئی کاپی موجود نہیں ہوتی؛ ایک ریکارڈ جس کی گنتی اس کے سوالات سے میل نہیں کھاتی، ناکام ہو جاتا ہے۔ ایک ونڈو جو ایک سیکنڈ میں ایک سے زیادہ صفحات کے سوالات رکھتی ہے، اس صفحے کو برقرار رکھتی ہے اور کہتی ہے کہ باقی غائب ہیں۔ کاپی ہے کلوڈ فلئیر کا جواب کلیکٹر کے ذریعے، کلیکٹر کے دستخط شدہ؛ 24 گھنٹوں کے اندر کوئی بھی جس کے پاس ریڈ-اونلی ٹوکن ہو اسے کلوڈ فلئیر کے ساتھ موازنہ کر سکتا ہے۔
