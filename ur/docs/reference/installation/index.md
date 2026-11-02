# انسٹال کریں، تصدیق کریں اور اپ ڈیٹ کریں

Canonical page: https://phishdestroy.github.io/TgWitness/ur/docs/reference/installation/

ایک کمانڈ کے ساتھ انسٹال کریں، دستخط اور ہیشز کی تصدیق کریں، انسٹالیشن کو اپ ڈیٹ اور ہٹائیں۔

[پروجیکٹ](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [تیز آغاز](https://phishdestroy.github.io/TgWitness/ur/docs/reference/quickstart/) · [تیناری](https://phishdestroy.github.io/TgWitness/ur/docs/reference/deployment/)

## ایک کمانڈ کے ساتھ انسٹال کریں

رہنمائی شدہ انسٹالر میں ایک نجی پائتھن رن ٹائم شامل ہے۔ مستقبل کی تنصیبات کے لیے ایک ہی پتہ استعمال کریں: ہر اشاعت انسٹالر، ہیشز، دستخط اور بلڈ معلومات کو ایک ساتھ اپ ڈیٹ کرتی ہے۔

**لینکس / میک او ایس (بش):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Ubuntu سرور پر، پسِ منظر سروس انسٹال کرنے کے لیے بطور روٹ چلائیں۔ ڈیسک ٹاپ پر، بطور معمول صارف چلائیں۔

**ونڈوز (پاور شیل یا کمانڈ پرامپٹ):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

ونڈوز پر کسی منتظم کی ضرورت نہیں۔ ذیلی پاور شیل پراسیس آپ کے ٹرمینل کو نتیجے کے ساتھ کھلا چھوڑ دیتی ہے۔ پائتھن اور انحصار انسٹالیشن میں ہی رہتے ہیں۔

اوبنٹو پر، **یہ کمپیوٹر**، **عارضی HTTPS لنک** یا **اپنا ڈومین** منتخب کریں۔ انسٹالر پینل کا پتہ اور ایکسس کی پرنٹ کرتا ہے۔ عارضی لنک کے لیے، اس HTTPS پتے کو اپنے براؤزر میں کھولیں اور کی درج کریں۔ ریموٹ سرور پر مقامی رسائی کے لیے، اپنے کمپیوٹر سے SSH فارورڈ استعمال کریں (`ssh -L 8787:127.0.0.1:8787 user@server`) اور کھولیں `http://127.0.0.1:8787`۔ macOS اور Windows پر، مقامی پینل آپ کے براؤزر میں کھلتا ہے؛ اس کے ٹرمینل کو چلتا رکھیں۔

پینل میں ٹیلیگرام میں سائن ان کریں اور منتخب کریں کہ کیا جمع کرنا ہے۔ صرف انسٹالیشن سے ٹیلیگرام کا مجموعہ شروع نہیں ہوتا۔

## جہاں سب کچھ چلتا ہے

`get.destroy.tools` یہ ایک **Cloudflare Worker جامد ڈاؤن لوڈز فراہم کر رہا ہے** ہے۔ اس میں کوئی TgWitness پینل، ٹیلیگرام سیشن یا صارف ثبوت ڈیٹا بیس نہیں ہے۔ یہ کسی پروجیکٹ VPS پر ہدایت نہیں کیا جاتا۔ یہ ایپلیکیشن اُس مشین پر چلتی ہے جہاں آپ کمانڈ چلاتے ہیں۔

| تنصیب | پروگرام | ڈیٹا |
| --- | --- | --- |
| اوبنٹو بطور روٹ | `/opt/tgwitness` | سسٹم سروس: `/var/lib/tgwitness-<installation ID>`؛ استعمال کریں `tgwitness paths` درست راستہ جاننے کے لیے۔ |
| لینکس / میک او ایس صارف | `~/.local/share/tgwitness` | `data/live` اس تنصیب کے تحت۔ |
| ونڈوز صارف | `%LOCALAPPDATA%\TgWitness` | `data\live` اس تنصیب کے تحت۔ |

سیٹ `TGWITNESS_INSTALL_DIR` دوسرا فولڈر منتخب کرنے کے لیے۔ انسٹال شدہ ورژنز اور ڈیٹا الگ ہیں۔ انسٹالر آپ کے اکاؤنٹس، پیغامات یا کیز کو ڈاؤن لوڈ سائٹ پر اپ لوڈ نہیں کرتا۔ کلاؤڈ فلیئر ٹنل منتخب کرنے سے پینل ٹریفک کلاؤڈ فلیئر کے ذریعے بھیجی جاتی ہے؛ اپنا ڈومین استعمال کرنے سے یہ آپ کے اپنے سرور کی طرف اشارہ کرتا ہے۔

ہر انسٹالیشن میں **START-HERE.html** اور **START-HERE.txt** شامل ہوتے ہیں، جن میں مقامی راستے، کمانڈز اور ریپوزیٹری کے لنکس ہوتے ہیں۔ چلائیں `tgwitness guide` رہنما کھولنے کے لیے۔ ونڈوز پر، استعمال کریں `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` PowerShell میں استعمال کریں۔

## چلانے سے پہلے تصدیق کریں

ایک سطری کمانڈ اپنی ابتدائی اسکرپٹ کے لیے HTTPS پر بھروسہ کرتی ہے۔ یہ اسکرپٹ انسٹالیشن سے پہلے SHA-256 اور ایپلیکیشن اور پابندیوں پر پروجیکٹ کے RSA دستخط کی جانچ کرتی ہے۔ آپ ابتدائی اسکرپٹ کو پہلے ڈاؤن لوڈ کر کے اس کی تصدیق بھی کر سکتے ہیں۔

عوامی ریلیز کلید [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub) ہے۔ اس کا SHA-256 ہے:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

اس فنگر پرنٹ کو اس ریپوزیٹری ریویژن سے محفوظ رکھیں جس پر آپ بھروسہ کرتے ہیں۔ ایک چیک سم اسی ڈاؤن لوڈ سرور سے بے مطابقت کا پتہ لگاتی ہے؛ آزادانہ طور پر قابلِ اعتماد عوامی چابی ہی ریلیز کے دستخط کی تصدیق کرتی ہے۔

نیچے دیے گئے تصدیقی ڈاؤن لوڈز کے لیے ایک نئی، خالی ڈائریکٹری استعمال کریں۔

**Linux / macOS — ایک نئی، خالی ڈاؤن لوڈ ڈائریکٹری میں چلائیں** (curl اور OpenSSL درکار ہیں):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

دی `&&` چین عملدرآمد سے پہلے رک جاتا ہے اگر ڈاؤن لوڈ، کلید کے فنگر پرنٹ یا دستخط کی جانچ ناکام ہو جائے۔ اگر اسکرپٹ کو ڈاؤن لوڈ کرنے اور اس کے دستخط کے درمیان کوئی اشاعت ہو جائے، تو دونوں کو دوبارہ ڈاؤن لوڈ کریں۔ پرانے انسٹالرز اپنے ناقابلِ تبدیلی پیکیج یو آر ایل برقرار رکھتے ہیں۔

**ونڈوز — چلانے سے پہلے SHA-256 کا معائنہ کریں:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

ہیش کا موازنہ کے ساتھ کریں `install.ps1` لائن کے ساتھ۔ ایک آزادانہ دستخطی جانچ کے لیے، OpenSSL استعمال کریں (مثال کے طور پر، Git Bash سے) اور اوپر دی گئی وہی پبلک-کی فنگر پرنٹ:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

ونڈوز انسٹالیشن خود .NET کے ساتھ پیکیج سگنیچرز کی تصدیق کرتی ہے اور اسے OpenSSL کی ضرورت نہیں ہوتی۔ یہ Authenticode نہیں بلکہ علیحدہ RSA-3072 / SHA-256 سگنیچرز ہیں۔ [مینفیسٹ](https://get.destroy.tools/manifest.json) میں سافٹ ویئر ورژن، عین Git کمٹ، ناقابلِ تبدیلی ریلیز آئی ڈی اور ہر آرٹیفیکٹ کا SHA-256 ریکارڈ کیا جاتا ہے۔ صفحہ متعلقہ ماخذ سے منسلک ہوتا ہے۔ مینفیسٹ اور چیک سم لسٹ میں بھی علیحدہ سگنیچرز ہوتے ہیں (`manifest.json.sig` اور `SHA256SUMS.txt.sig`).

## موجودہ تنصیب کو اپ ڈیٹ کریں

**ایک نئی اشاعت ڈاؤن لوڈ سائٹ کو اپ ڈیٹ کرتی ہے؛ انسٹال شدہ پروگرامز آپ کے انسٹالر دوبارہ چلانے پر اپ ڈیٹ ہوتے ہیں۔** کوئی خودکار اپڈیٹر یا چلتی ہوئی کلیکشن کا خودکار ری اسٹارٹ موجود نہیں ہے۔ موجودہ انسٹالر چینل **پیش نظارہ** ہے؛ یہ شائع شدہ، چیک شدہ بلڈز کی پیروی کرتا ہے جو `main`، جس کا کمٹ آخری نمبر شدہ GitHub ریلیز سے نیا ہو سکتا ہے۔ صفحے کا ورژن سے آتا ہے۔ `pyproject.toml`؛ اس کا کمٹ اور بلڈ آئی ڈی ایک ہی پیش نظارہ ورژن کے اندر اپ ڈیٹس کو ممتاز کرتا ہے۔

پہلے کی طرح ایک ہی انسٹالیشن فولڈر اور OS صارف استعمال کریں۔ مکمل ڈیٹا ڈائریکٹری کا بیک اپ لیں جب کلیکشن رک گیا ہو؛ `tgwitness paths` اس کی شناخت کرتا ہے۔ ایک دستخط شدہ ایکسپورٹ مکمل انسٹالیشن بیک اپ نہیں ہے۔

**اوبنٹو روٹ انسٹالیشن پر `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

کامیاب تنصیب کے بعد:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Linux/macOS صارف کی تنصیب کے لیے، اس کے اصل `TGWITNESS_INSTALL_DIR` یا ڈیفالٹ استعمال کریں اور پہلا انسٹالیشن کمانڈ دوبارہ چلائیں۔ اپ ڈیٹ کرنے سے پہلے ایک فرنٹیئم پینل کو بند کریں اور بعد میں اسے دوبارہ شروع کریں۔ ایک کنفیگر کیے گئے لینکس صارف سروس کے لیے، اس کا `tgwitness restart` کمانڈ چلائیں۔

**ونڈوز:** چلنے والا پینل بند کریں، ونڈوز انسٹالیشن کمانڈ دوبارہ چلائیں، پھر کھولیں `bin\tgwitness.cmd` اسی انسٹالیشن میں۔ انسٹالر ڈیٹا، سیشنز، رسائی کی ترتیبات اور دستخطی کلیدیں برقرار رکھتا ہے۔ یہ لانچر کو صرف اس کے بعد تبدیل کرتا ہے جب نیا ماحول اپنی جانچوں میں کامیاب ہو جاتا ہے؛ ناکام انسٹالیشن پچھلے لانچر کو اپنی جگہ برقرار رکھتی ہے۔ اسٹوریج فارمیٹ میں تبدیلیوں کے لیے پری-اپ گریڈ بیک اپ کو محفوظ رکھیں۔

## اوبنٹو پر روزمرہ کے کمانڈز

| کمانڈ | نتیجہ |
| --- | --- |
| `tgwitness open` | موجودہ پینل کا URL اور رسائی کلید۔ |
| `tgwitness paths` | بالکل درست پروگرام، ڈیٹا اور گائیڈ راستے۔ |
| `tgwitness guide --print` | آف لائن آپریٹنگ ہدایات۔ |
| `tgwitness status` / `tgwitness logs` | دستیابی / سروس لاگز۔ |
| `tgwitness stop` / `tgwitness start` | سروس کو روکیں / دوبارہ شروع کریں؛ ڈیٹا برقرار رکھیں۔ |
| `tgwitness token rotate` | انتظامی کلید تبدیل کریں اور براؤزر سیشنز ختم کریں۔ |
| `tgwitness tunnel off` | پبلک تیز سرنگ کو غیر فعال کریں؛ مقامی پینل کو برقرار رکھیں۔ |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | تیزی سے ٹنل لنک بنائیں / اس کا پتہ تبدیل کریں۔ |

ساتھی ٹوکنز، سیشنز اور آئی پی پابندیوں کے لیے [رسائی](https://phishdestroy.github.io/TgWitness/ur/docs/reference/access/) دیکھیں، اور GitHub-to-Cloudflare ریلیز ورک فلو کے لیے [انسٹالر شائع کرنے کے عمل](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) کو دیکھیں۔

## TgWitness کو ہٹا دیں

کوئی ان انسٹالر موجود نہیں ہے: آپ پینل کو روک کر اس کے فولڈرز حذف کر دیتے ہیں۔ ڈیٹا فولڈر کو حذف کرنے سے جرنلز، سگننگ کیز، ٹیلیگرام سیشنز اور محفوظ شدہ فائلیں ہمیشہ کے لیے ختم ہو جاتی ہیں۔ اس سے پہلے:

1. اپنی ضرورت کے مطابق برآمد کریں (**Exports → Download signed ZIP**) اور دستخطی کلید کے فنگر پرنٹ اور چیک پوائنٹس کو اس مشین سے باہر محفوظ رکھیں۔ ورک اسپیس کو برقرار رکھنے کے لیے، کلیکشن روک کر پورے ڈیٹا فولڈر کی کاپی کریں۔
2. **Extras → Server 24/7** کے تحت **آپ کے سرورز** یا کے ساتھ بنائے گئے سرورز کو حذف کریں `python -m tgwitness.cloud destroy`؛ فراہم کنندہ انہیں حذف کیے جانے تک بل کرتا ہے۔
3. ہر اکاؤنٹ کے سیشن کو Telegram میں **Settings → Devices** کے تحت ختم کریں۔ فائلوں کو حذف کرنے سے Telegram کی جانب سے سیشن لاگ آؤٹ نہیں ہوتا۔

**اوبنٹو روٹ انسٹالیشن۔** ڈیٹا فولڈر کو نوٹ کریں، سروس کو روکیں، پھر سروس، فولڈرز اور شارٹ کٹ کو ہٹا دیں:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Linux یا macOS صارف کی تنصیب۔** پینل بند کریں۔ ایک ترتیب شدہ Linux صارف سروس کو روکا جاتا ہے `systemctl --user disable --now tgwitness-<ID>`؛ اس کی یونٹ میں ہے `~/.config/systemd/user/`۔ پھر حذف کریں `~/.local/share/tgwitness` (یا آپ کا `TGWITNESS_INSTALL_DIR`) اور `~/.local/bin/tgwitness` شارٹ کٹ۔

**Windows۔** پینل بند کریں اور حذف کریں `%LOCALAPPDATA%\TgWitness` (یا آپ کا `TGWITNESS_INSTALL_DIR`)۔ انسٹالر کوئی سروس، شیڈولڈ ٹاسک یا شارٹ کٹ شامل نہیں کرتا۔
