# آزاد شاہد

Canonical page: https://phishdestroy.github.io/TgWitness/ur/docs/reference/witness/

اپنی مخصوص کلید اور بوٹ کے ساتھ ایک ویٹنس چلائیں، دستخط شدہ چیک پوائنٹس کو ایک چینل پر شائع کریں اور ان کے خلاف ایکسپورٹس کی تصدیق کریں۔

[ٹی جی وٹنس](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [دستاویزات](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/ur/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

[ایکسپورٹ اور تصدیق کریں](https://phishdestroy.github.io/TgWitness/ur/docs/reference/evidence/) · [اعلیٰ یقین دہانی](https://phishdestroy.github.io/TgWitness/ur/docs/reference/high-assurance/) · [پینل گائیڈ](https://phishdestroy.github.io/TgWitness/ur/docs/reference/panel/#extras)

A witness retains signed checkpoints separately from the collector. It checks the collector's signature and journal continuity, signs the result with its own key, and publishes it to a Telegram channel. Run it on a separate server with read-only access to the collector's witness endpoint.

دھارے کا خاکہ · جمع کنندہ → گواہ (مصنوعی چیک پوائنٹ: ریکارڈز کی تعداد + ہیڈ ہیش); گواہ → گواہ جرنل، اپنی کلید; گواہ → ٹیلیگرام چینل (اپنے بوٹ کے ذریعے دستخط شدہ پوسٹ); شواہد کا زپ → verify.py; گواہ جرنل، اپنی کلید → verify.py; ٹیلیگرام چینل → verify.py (ٹیلیگرام ڈیسک ٹاپ ایکسپورٹ یا t.me/s صفحہ) · جمع کنندہ · گواہ · گواہ جرنل، اپنی کلید · ٹیلیگرام چینل · شواہد کا زپ · verify.py · مصنوعی چیک پوائنٹ: ریکارڈز · کی تعداد + ہیڈ ہیش · اپنے بوٹ کے ذریعے دستخط شدہ · پوسٹ · ٹیلیگرام ڈیسک ٹاپ ایکسپورٹ · یا t.me/s صفحہ

**ڈایاگرام بطور متن**

1. جمع کنندہ → گواہ (مصنوعی چیک پوائنٹ: ریکارڈز کی تعداد + ہیڈ ہیش)
2. گواہ → گواہ جرنل، اپنی کلید
3. گواہ → ٹیلیگرام چینل (اپنے بوٹ کے ذریعے دستخط شدہ پوسٹ)
4. شواہد کا زپ → verify.py
5. گواہ جرنل، اپنی کلید → verify.py
6. ٹیلیگرام چینل → verify.py (ٹیلیگرام ڈیسک ٹاپ ایکسپورٹ یا t.me/s صفحہ)

**On this page**

- [What the witness gets, and what it does not](https://phishdestroy.github.io/TgWitness/ur/docs/reference/witness/#what-the-witness-gets-and-what-it-does-not)
- [What it checks and records](https://phishdestroy.github.io/TgWitness/ur/docs/reference/witness/#what-it-checks-and-records)
- [Run a witness](https://phishdestroy.github.io/TgWitness/ur/docs/reference/witness/#run-a-witness)
- [Public proof page for several workspaces](https://phishdestroy.github.io/TgWitness/ur/docs/reference/witness/#public-proof-page-for-several-workspaces)
- [Verify](https://phishdestroy.github.io/TgWitness/ur/docs/reference/witness/#verify)

## گواہ کو کیا ملتا ہے، اور کیا نہیں ملتا

| گواہ کے پاس ہے | گواہ نے کبھی نہیں |
| --- | --- |
| ایک ورک اسپیس کے لیے صرف پڑھنے کے قابل **وِٹنس ٹوکن** | جمع کرنے والے کا ٹیلیگرام سیشن یا API کی شناختی تفصیلات |
| اپنی Ed25519 کلید اور جرنل | جمع کنندہ کا خزانہ، دستخطی کلید یا پینل ٹوکن |
| اس کا اپنا ٹیلیگرام بوٹ ٹوکن | پیغام کا مواد: سر میں ریکارڈز کی تعداد اور ہیش شامل ہے |

ٹوکن **Extras → Independent witness** میں بنایا جاتا ہے، ایک بار دکھایا جاتا ہے اور صرف ایک SHA-256 کے طور پر محفوظ کیا جاتا ہے۔ یہ بالکل ایک ہی اینڈ پوائنٹ کھولتا ہے، `GET /api/witness/head`، جو ایک تازہ سائن شدہ چیک پوائنٹ کے ساتھ ساتھ سائن شدہ مواد سے خالی کلیکشن کاؤنٹرز اور آپریشنل ہیلتھ واپس کرتا ہے۔ یہ پینل نہیں کھول سکتا، پیغام کا مواد نہیں پڑھ سکتا یا ترتیبات تبدیل نہیں کر سکتا، اور پینل ٹوکن وہاں قبول نہیں کیا جاتا۔ اسی صفحے پر ٹوکن کو منسوخ کریں۔ کلیکٹر ریکارڈ کرتا ہے کہ ایک نئی ویٹنس کی چیکنگ کب شروع کرتی ہے (`witness.seen`) اور ہر ٹوکن کے لیے آخری چیک دکھاتا ہے؛ ایک گواہ جو 2.5 وقفوں کے اندر چیک نہیں کرتا اسے مقررہ وقت سے تجاوز شدہ قرار دیا جاتا ہے۔

نئے گواہ ہر پول پر ایک بے ترتیب چیلنج بھیجتے ہیں؛ کیپچر بیان اسے کلیکٹر کے دستخط کے نیچے دہراتا ہے۔ کاؤنٹر بالکل درست چیک پوائنٹ سے منسلک ہوتے ہیں اور دستخط شدہ گواہ پوسٹس میں شامل کیے جاتے ہیں۔ لیگیسی ہیڈز خود مختار گواہ کے ذریعے قبول کیے جاتے رہتے ہیں۔ صرف جرنل کی ترقی کو کبھی نئے پیغام کے طور پر نہیں گنا جاتا۔

## یہ کیا چیک اور ریکارڈ کرتا ہے

ہر وقفے (ڈیفالٹ کے طور پر 10 منٹ) پر گواہ:

1. خود ہی ہیڈ کو حاصل کرتا ہے (جمع کرنے والا اسے دھکیل یا چھوڑ نہیں سکتا)؛
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen), a nondecreasing count and an unchanged head at an unchanged count. Merkle inclusion and consistency proofs verify that a growing journal extends the retained checkpoint. Once continuity proofs have been used, removing them is rejected;
3. اپنے جرنل میں ایک دستخط شدہ ریکارڈ منسلک کرتا ہے: `witness.anchor` جس کی حیثیت `ok`، `key_changed`، `rollback` (پہلے سے کم ریکارڈز)، `fork` (لمبائی ایک جیسی، مختلف ہیڈر) یا `invalid` (جواب توثیق میں ناکام رہا)، یا `witness.no_response` جب جمع کرنے والے نے جواب نہیں دیا؛
4. نتیجہ چینل پر پوسٹ کیا جاتا ہے، دستخط شدہ، بشمول "کوئی جواب نہیں" جب تک گواہ چل رہا ہو اور Bot API تک پہنچ سکے۔ پوسٹ آئی ڈی ریکارڈ کی جاتی ہے (`witness.posted`)، ایک ناکام پوسٹ بھی (`witness.post_failed`).

ایک پوسٹ اس طرح نظر آتی ہے؛ آخری سطر میں دستخط شدہ بیان شامل ہوتا ہے:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## ویٹنس چلائیں

آپ کو ایک ٹیلیگرام بوٹ (@BotFather کے ذریعے ایک بنائیں)، ایک چینل جہاں وہ بوٹ منتظم ہو، اور گواہ کی جانب سے قابلِ رسائی کلیکٹر کا پتہ — نجی نیٹ ورک کے باہر HTTPS کے ذریعے ([تینفذ](https://phishdestroy.github.io/TgWitness/ur/docs/reference/deployment/) میں HTTPS پروفائل دیکھیں)۔

پینل میں **Extras → Independent witness → Configure** کھولیں۔ تین مراحل میں صرف پڑھنے کی اجازت، آپ کا چینل اور وقفہ شامل ہیں، پھر وِٹنس کو لانچ کریں۔ اشاعت کی پالیسی، اختیاری HTTP/SOCKS5 پروکسی اور کسٹم Bot API پتہ **Advanced settings** کے تحت ہیں۔ فارم ڈاؤن لوڈ ہوتا ہے `witness.json` اس ورک اسپیس کی کلیکٹر کی کو پن کر کے۔ نئے بنائے گئے ریڈ-اوْنلی ٹوکن کو "**Save access file** as" کے ساتھ ڈاؤن لوڈ کریں `witness-token.txt`؛ اسے اور ا `bot-token.txt`جو ویٹنس ہوسٹ پر اس JSON کے ساتھ بنایا گیا ہے۔ کلیکٹر کو کبھی بھی بوٹ ٹوکن موصول نہیں ہوتا۔ ڈاؤن لوڈ کرنا کوئی سروس شروع نہیں کرتا اور نہ ہی کوئی پیغام شائع کرتا ہے۔ کوئی بھی ہوسٹڈ پروجیکٹ ویٹنس خودکار طور پر شامل نہیں ہوتا۔

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

پہلی کمانڈ کنفیگریشن اور خفیہ فائلوں کی جانچ کرتی ہے، بغیر کسی نیٹ ورک درخواست یا کلید کی تخلیق کے۔ JSON میں راستے اس فائل کے نسبت سے ہوتے ہیں؛ CLI/ماحول کے راستے کام کرنے والی ڈائریکٹری کے نسبت سے ہوتے ہیں۔ گواہ کے فنگر پرنٹ کو اس کے ہوسٹ کے باہر محفوظ رکھیں۔ کلیکٹر کا آخری پول انڈیکیٹر صرف درخواست کی تصدیق کرتا ہے؛ اشاعت کی اطلاع Proof کے ذریعے دی جاتی ہے یا گواہ کے جرنل اور چینل میں چیک کی جاتی ہے۔

اگر پینل SSH ٹنل کے پیچھے رہے، تو صرف اسکوپڈ وِٹنس اینڈ پوائنٹ کو ایک الگ HTTPS ہوسٹ نیم پر [اس Caddy مثال](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example) کے ساتھ ظاہر کریں۔ ڈیفالٹ ورک اسپیس پھر `https://witness.example.org` استعمال کرتا ہے، دیگر ورک اسپیس `https://witness.example.org/profiles/ID` استعمال کرتے ہیں۔ ٹوکنز کی ضرورت اب بھی ہوتی ہے؛ پینل اور اس کے دیگر API روٹس اس ورچوئل ہوسٹ کے ذریعے فارورڈ نہیں کیے جاتے۔

`all` کو باقاعدگی سے شائع ہونے والے چیک پوائنٹس کے لیے منتخب کریں۔ پانچ منٹ کے وقفے کا مطلب ہے کہ روزانہ فی ورک اسپیس تقریباً 288 پوسٹس۔ `changes`/`problems` جان بوجھ کر کچھ چیکس غیر شائع شدہ چھوڑ دیتے ہیں۔ MTProxy کلیکٹر کے ٹیلیگرام کلائنٹ کے لیے ہے۔ Witness HTTP پولنگ اور ٹیلیگرام کا HTTPS Bot API اپنا براہِ راست/HTTP/SOCKS5 راستہ ([Bot API](https://core.telegram.org/bots/api)) استعمال کرتے ہیں۔

**کلیکٹر کے ساتھ، ڈوکر کے ذریعے** (ایک ہی ہوسٹ — آزاد عمل اور کلید، لیکن ایک ہی آپریٹر): `.env` میں ویلیوز درج کریں اور پروفائل شروع کریں۔

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

شائع شدہ تصویر کے لیے `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d` استعمال کریں۔

**کسی اور کے سرور پر** (ایک حقیقی آزاد گواہ): وہاں ریپوزیٹری کاپی کریں، `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` میں اوپر دیے گئے تین اقدار کے ساتھ `.env` سیٹ کریں، پھر

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

یا ڈاکر کے بغیر:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Discord پر شائع کریں

ایک گواہ ٹیلیگرام کے بجائے ڈسکارڈ چینل پر پوسٹ کر سکتا ہے۔ ڈسکارڈ میں، **Edit Channel → Integrations → Webhooks** کھولیں، ایک ویب ہوک بنائیں اور اس کا URL کاپی کریں۔ پینل میں، مرحلے 2 میں **Discord ویب ہوک · اپنا چینل** منتخب کریں۔ گواہ ہوسٹ پر، URL کو بطور محفوظ کریں `discord-webhook.txt` کے ساتھ `witness.json`؛ یہ کبھی کلیکٹر تک نہیں پہنچتا۔

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

ایک ویٹنس کا ایک ہی پبلشر ہوتا ہے: یا تو ایک ٹیلیگرام چینل یا ایک ڈسکارڈ ویب ہُک، دونوں نہیں۔ پوسٹس ایک ہی دستخط شدہ بیان رکھتی ہیں اور کسی کو بھی پنگ نہیں کر سکتیں۔ ڈسکارڈ کی 2,000 حروف کی حد سے زیادہ طویل پوسٹ کو ایک مختصر لائن سے بدل دیا جاتا ہے جس کے ساتھ مکمل چیک منسلک ہوتا ہے `witness-check.txt`۔ ہر پوسٹ آئی ڈی کو بطور درج کیا جاتا ہے `witness.posted`. `verify.py --channel`صرف ٹیلیگرام چینل کی برآمدات کو پڑھتا ہے، لہٰذا Discord کے لیے گواہ جریدہ رکھیں: اس میں ہر چیک موجود ہوتا ہے۔

### اختیارات

| اختیار | ماحول | ڈیفالٹ | معنی |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | چیکس کے درمیان منٹ، 1–1440 |
| `--timeout` | `_TIMEOUT` | 30 | کلیکٹر اور بوٹ API کے لیے انتظار کے سیکنڈز، 5–600 |
| `--post` | `_POST` | `all` | `all`: ہر چیک؛ `changes`: ایک نیا سربراہ یا ایک مسئلہ؛ `problems`: صرف مسائل اور غائب جوابات |
| `--title` | `_TITLE` | `TgWitness witness` | ہر چینل پوسٹ کے پہلے الفاظ |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | پہلے جواب پر بھروسہ کرنے کے بجائے کلیکٹر کلید کو پن کریں۔ |
| `--proxy` | `_PROXY` | براہِ راست | `socks5://host:port` یا `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | بوٹ API کا پتہ، مثلاً ایک مقامی بوٹ API سرور |
| `--data-dir` | `_DATA` | `witness-data` | ویٹنس کی اور جرنل |
| `--config` | `_CONFIG` | – | مندرجہ بالا اختیارات میں سے کسی کے ساتھ JSON فائل |

جمع کرنے والا پتہ، ٹوکنز اور چینل سے آتے ہیں `--collector`, `--token` یا `--token-file`, `--bot-token` یا `--bot-token-file`, `--discord-webhook-file` اور `--channel`، یا `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` اور `_CHANNEL`، جو عمل کی فہرست سے رازوں کو پوشیدہ رکھتا ہے۔

ایک کنفیگ فائل آپشن کے ناموں کے لیے انڈر اسکورز استعمال کرتی ہے، اور `texts` بھی، جو چینل کی پوسٹس کے الفاظ کو تبدیل کر دیتا ہے:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts` کلیدیں: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. کمانڈ لائن ماحول پر، اور ماحول فائل پر غالب آتی ہے۔ نامعلوم اختیارات یا ٹیکسٹ کلیدیں نظر انداز کیے جانے کے بجائے ایک پیغام کے ساتھ ویٹنس کو روک دیتی ہیں۔ الفاظ کی ترتیب کبھی تصدیق کو متاثر نہیں کرتی: verify.py ہر پوسٹ کے آخر میں دستخط شدہ ٹوکن کی جانچ کرتا ہے۔ `--post changes` یا `problems` کے ساتھ، وہ چیکس جو پوسٹ نہیں کیے گئے تھے وہ اب بھی ویٹنس جرنل میں موجود ہیں اور `verify.py` انہیں کبھی پوسٹ نہ کیے جانے کے طور پر درج کرتا ہے؛ شروع کا ریکارڈ پالیسی کا نام بتاتا ہے۔ ہر چیک اب بھی جرنل میں ظاہر ہوتا ہے، لہٰذا کم پوسٹس کا مطلب کم آزاد ٹیلیگرام اوقات ہیں، نہ کہ کم چیکس۔

چینل کے بغیر بھی ویٹنس اپنا جرنل برقرار رکھتا ہے۔ ویٹنس کی کلید کے فنگر پرنٹ (`python -m tgwitness.witness fingerprint`) کو کہیں اور محفوظ رکھیں۔

## کئی ورک اسپیسز کے لیے عوامی ثبوت صفحہ

`python -m tgwitness.proof` ایک ہی وقت میں 32 ورک اسپیسز کو وِٹنس کرتا ہے اور ہر ایک کے تازہ ترین دستخط شدہ چیک کے ساتھ ایک ریڈ-اونلی صفحہ فراہم کرتا ہے۔ ہر ورک اسپیس کو ڈیٹا فولڈر کے تحت اپنی وِٹنس کی اور جرنل اور ایک پن کیا ہوا کلیکٹر کی ملتا ہے؛ ٹیلیگرام چینل پر پوسٹ کرنا ہر ورک اسپیس کے لیے اختیاری ہے۔ [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example) سے شروع کریں:

| میدان | معنی |
| --- | --- |
| `title` | صفحے کا عنوان، 1–100 حروف |
| `data_dir` | گواہی کی چابیاں اور جرنلز، فائل کے حوالے سے؛ ڈیفالٹ `proof-data` |
| `interval`, `timeout` | چیکس کے درمیان منٹ (1–1440، ڈیفالٹ 5)؛ انتظار کے سیکنڈ (5–600، ڈیفالٹ 20) |
| `workspaces[].id`, `label` | چھوٹا چھوٹے حروف پر مشتمل عرفی نام اور دکھایا گیا نام |
| `workspaces[].collector` | کلیکٹر کا پتہ؛ دیگر ورک اسپیسز ختم ہوتے ہیں `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | ضروری، ہر ورک اسپیس کے لیے مختلف |
| `workspaces[].token_file` | اس ورک اسپیس کے ریڈ-اونلی وِٹنس ٹوکن کے ساتھ فائل |
| `workspaces[].channel`, `bot_token_file` | اختیاری، ایک ساتھ: ہر چیک کو ایک چینل پر پوسٹ کریں |
| `workspaces[].proxy`, `bot_api` | اختیاری راستہ اور بوٹ API پتہ |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

پہلی کمانڈ فائل اور ٹوکن فائلوں کی درستگی چیک کرتی ہے بغیر کنکشن کھولے۔ صفحہ صرف GET اور HEAD کے جوابات دیتا ہے:

- `/` ہر ورک اسپیس دکھاتا ہے؛ اگر کسی ورک اسپیس میں 2.5 وقفوں کے لیے چیک نہ کیا گیا ہو تو اسے پرانا (stale) نشان زد کیا جاتا ہے۔
- `/api/proof` JSON کی طرح ہی واپس کرتا ہے۔
- `/api/proof/<id>` تازہ ترین دستخط شدہ بیان ڈاؤن لوڈ کرتا ہے (`tgwitness-public-proof-v1`): گواہ ریکارڈ نمبر اور ہیش، اسٹیٹس، پن کی ہوئی کلیکٹر کی، چیک پوائنٹ، کلیکشن کاؤنٹرز اور یہ کہ چینل پوسٹ کامیاب ہوئی یا نہیں، اس ورک اسپیس کی گواہ کلید کے ذریعے دستخط شدہ۔
- `/healthz` جب کسی ورک اسپیس کا مانیٹر رک گیا ہو تو 503 کا جواب دیتا ہے۔

صفحے کو اپنا ہوسٹ نام دیں، جیسا کہ [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example) میں۔ تصدیق کے لیے، ایک ورک اسپیس کا ویٹنس جرنل ایکسپورٹ کریں۔ `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` اور اسے نیچے بیان کردہ طریقے کے مطابق استعمال کریں۔

## تصدیق کریں

گواہ کی جانب سے، اپنا جریدہ برآمد کریں:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

پھر، کہیں بھی، کلیکٹر کے دستخط شدہ ZIP اور ٹیلیگرام ڈیسک ٹاپ سے ایکسپورٹ کیے گئے چینل کے ساتھ (*Export chat history* → JSON سے `result.json` ملتا ہے) یا اس کے عوامی `https://t.me/s/…` صفحے کے ذریعے:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` گواہ کے جرنل (زنجیر اور دستخط) کی جانچ کرتا ہے، پھر یہ کہ **ہر وہ سر جو گواہ نے دیکھا ہے، برآمد شدہ جرنل کا حصہ ہے**: اس گنتی پر ریکارڈ میں بالکل وہی ہیش ہونا چاہیے۔ جو سر میل نہیں کھاتا وہ توثیق میں ناکام ہو جاتا ہے — جرنل گواہ کے دیکھنے کے بعد تبدیل کیا گیا تھا۔ یہ برآمدات کے بعد دیکھے گئے ہیڈز، گواہ کی ریکارڈ کردہ بے ضابطگیاں، ناکام جوابات، وہ ادوار جن کے مطابقت رکھنے والے چیک پوائنٹس اس برآمد میں موجود ہیں ("X سے Y تک گواہی دی گئی") اور خلاؤں کی بھی رپورٹ کرتا ہے۔ بعد کے چیک پوائنٹس ان ادوار کو بڑھا نہیں سکتے۔ نتیجے میں آخری مطابقت پذیر ریکارڈ نمبر اور بغیر میچنگ چیک پوائنٹ کے پیچھے آنے والے ریکارڈز کی تعداد شامل ہوتی ہے۔ صرف وہ جوابات شمار کیے جاتے ہیں جن پر خود ایکسپورٹ کی کلید نے دستخط کیے ہوں: ایک ایکسپورٹ جس پر ایسی کلید نے دستخط کیے ہوں جو گواہ نے کبھی نہیں دیکھی، اسے غیر گواہی شدہ رپورٹ کیا جاتا ہے، اور `--fingerprint` کے بغیر اس کا دستخط کنندہ پن نہ شدہ رہتا ہے۔ `--channel` کے ساتھ ہر دستخط شدہ پوسٹ کو ویٹنس جرنل سے ریکارڈ بہ ریکارڈ ملانا ضروری ہے: تبدیل شدہ پوسٹس کی توثیق ناکام ہو جاتی ہے، اور غائب پوسٹس کی فہرست بنائی جاتی ہے۔ فراہم کردہ ٹیلیگرام JSON ایکسپورٹ میں موجود تاریخ قابل ترمیم میٹا ڈیٹا ہے، جو دستخط شدہ ویٹنس ٹوکن کے باہر ہوتی ہے۔ ٹوکن سے مطابقت رکھنے کا مطلب اشاعت کی تاریخ کی تصدیق نہیں ہے؛ نتیجہ واضح طور پر رپورٹ کرتا ہے کہ اشاعت کے وقت کی توثیق نہیں کی گئی تھی۔

### مشاہدہ شدہ برآمدی حد درکار

ایک ہینڈ اوور کے لیے جس میں گواہی شدہ حتمی ریکارڈ شامل ہونا چاہیے، `--require-witness` شامل کریں:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

اس کے لیے آزادانہ طور پر محفوظ کردہ گواہ کے فنگر پرنٹ اور اس ایکسپورٹ کے بالکل آخر میں ایک مماثل چیک پوائنٹ درکار ہوتا ہے۔ صرف پہلے کے پری فکس کو کور کرنے والا چیک پوائنٹ ناکافی ہے۔ کلیکشن کو روک دیں، گواہ کو حتمی حالت دیکھنے دیں، اور مزید جرنل لکھنے سے پہلے ایکسپورٹ کریں؛ اگر جرنل تبدیل ہو جائے تو ایک اور چیک پوائنٹ محفوظ کریں اور اس حالت کو ایکسپورٹ کریں۔ صرف بعد والا چیک پوائنٹ ایک چھوٹے ایکسپورٹ کے حتمی ہیش کی تصدیق نہیں کر سکتا۔ جب `--channel` بھی فراہم کیا جائے، تو دعویٰ شدہ لیکن غائب پوسٹس یا خالی میچ سیٹ اس سخت چیک میں ناکام ہو جاتے ہیں۔ فلیگ کے بغیر، عام سالمیت چیکس اب بھی ایسے ریکارڈز کی اطلاع دیتے ہیں جن کی گواہی نہیں دی گئی، بغیر اس کے کہ ایک ورنہ سالم آرکائیو کو مسترد کر دیں۔

Keep the witness journal and its pinned key separately. Online checks verify continuity between checkpoints; offline verification compares every retained checkpoint with the export. Legacy heads without continuity proofs retain the offline comparison and are reported without online continuity verification. The report lists witness downtime and failed publications by interval.

### Daily seals and unavailable timestamp calendars

The witness seals the previous UTC day's journal boundary and submits the hash of that signed seal to OpenTimestamps. A calendar submission is pending evidence; only independently checked Bitcoin commitments receive confirmation in the verifier.

If all calendars fail, the signed seal and unsuccessful attempt remain in the journal. The hourly maintenance pass retries that original record, including after a restart or a change of date. It scans at most 32 seals, submits at most two missing submissions and spends at most 60 seconds on retries per pass. A persistent cursor rotates through older seals. Retained submissions follow the existing proof-upgrade path.

A retry does not rewrite the seal, change its original date or claim that the calendar received it earlier. A later Bitcoin commitment remains a later external confirmation. Missing proofs remain `none`; pending proofs remain `pending` until the verifier checks them independently.
