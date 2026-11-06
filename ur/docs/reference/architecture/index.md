# معمارِی

Canonical page: https://phishdestroy.github.io/TgWitness/ur/docs/reference/architecture/

جمع کرنے والے، پینل، جرنل، ورکرز اور ویٹنس کے اجزاء، اور ڈیٹا ان کے درمیان کیسے منتقل ہوتا ہے۔

ایک پائتھن پراسیس FastAPI پینل اور کسی بھی تعداد میں الگ تھلگ ورک اسپیسز کو ہوسٹ کرتا ہے، جن میں سے ہر ایک میں Telethon یوزر اکاؤنٹ کلائنٹ ہوتا ہے۔ SQLite ایک صرف-ضم (append-only) شدہ دستخط شدہ ایونٹ جرنل اور قابلِ تبدیلی آپریشنل ترتیبات کو محفوظ رکھتا ہے۔ ایک انکرپٹڈ والٹ میں API کی تفصیلات، StringSession، اور دستخطی کلید محفوظ ہوتی ہے۔ فرنٹ اینڈ محض بنڈل شدہ HTML/CSS/JavaScript پر مشتمل ہے: Node بلڈ، CDNs، یا فرنٹ اینڈ ڈاؤن لوڈز کی ضرورت نہیں ہے۔

Optional browser and AyuGram recorders run in **separate processes or containers**. The `tgwitness_capture` package owns their event format, keys, artifacts, checkpoint API, independent witness and standalone verifier. It is bundled in the main wheel and can also be installed alone from `addons/capture`, without importing the collector. The main panel's `capture_api.py` and `capture_connections.py` provide administrator-only, workspace-scoped controls under `/api/capture`; connection tokens live in the encrypted vault. No recorder or outbound request starts with the main process. Each explicit command verifies a fresh challenge against the pinned recorder key. Exports are verified before download and keep their original signature; they do not become Telegram message events. Collection sessions and proxy routes stay with each client. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md) for deployment and trust boundaries.

| ماڈیول | ذمہ داری |
| --- | --- |
| collector.py | تصدیق، ڈائیلاگ کے انتخاب، اپ ڈیٹس، اسنیپ شاٹس، میڈیا قطار، کنکشن کی نگرانی |
| interactions.py / telegram_client.py | مخصوص پینل ایکشنز، دستخط شدہ رسیدیں، مستقل درخواست آئی ڈیز اور ٹاسک-مقامی کال بیک/جوائن ری ٹرائی پالیسی |
| پیغام_مواد.پی ای وائی | مشاہدہ کے قابل پیغامات کا موازنہ، ٹرانسپورٹ رسائی میٹا ڈیٹا کو خارج کرتے ہوئے |
| workers.py | منسوخی کی صفائی سے پہلے ایکسپورٹ فائل ورکرز کے مکمل ہونے کا انتظار کریں |
| distributed_export.py / distributed_pages.py | Concurrent chat jobs, per-account reservations, signed checkpoints and cleanup after archive verification |
| distributed_takeout.py / export_timing.py | Resumable Takeout sessions and timings for each start or resume |
| store.py | WAL ٹرانزیکشنز، ترتیب وار واقعہ زنجیر، استفساری فلٹرز، عملیاتی ترتیبات |
| fulltext.py | مشتق مکمل متن انڈیکس (لفظی اشکال، BM25)، دستخط شدہ جرنل ہیڈ سے منسلک؛ کبھی برآمد نہیں کیا گیا |
| security.py | نجی فائل کی تخلیق، انکرپٹڈ والٹ، Ed25519 دستخط، سنگل پروسیس لاک |
| evidence.py | مکمل جرنل کی برآمد، مشتقات، چیک پوائنٹس، منسلکات کی تصدیق |
| verify.py | خودمختار، صرف پڑھنے کے لیے تصدیق کنندہ (stdlib + کرپٹوگرافی): آرکائیوز، کوریج، ویٹنس جرنلز اور چینل پوسٹس، پروفائل فائلیں |
| app.py | تصدیق شدہ API، لائف سائیکل، درخواست کی توثیق، جامد پینل |
| profiles.py | متعدد اکاؤنٹ کلیکٹرز، مشترکہ رسائی کنٹرولر، ہر ورک اسپیس کا الگ لائف سائیکل |
| access.py | اسکوفٹ گرانٹس، اجازت نامے کی جانچ، آئی پی پابندیاں، سیشن کی حدیں اور ایڈمنسٹریٹر کنسول |
| proxy_catalog.py | پبلک فیڈ کے اسنیپ شاٹس، ٹرانسپورٹ چیکس، مشترکہ پروکسی پول اور صحت کی بنیاد پر انتخاب |
| provenance.py | دستخط شدہ حصولی-چلانے والی شناخت، کوڈ اور انحصار کی پیمائشیں |
| network.py | ہر ورک اسپیس کے لیے تصدیق شدہ راستے؛ حذف شدہ حیثیت اور شواہد؛ ٹیلی تھون ٹرانسپورٹ کے اختیارات |
| sessions.py | نظر ثانی شدہ Telethon SQLite خاکوں کی آف لائن صرف پڑھنے کے قابل تبدیلی |
| account_import.py | میکین میں سپورٹ کی جانے والی اکاؤنٹ فائلوں اور JSON کی شناخت اور معیاری کاری |
| tdata.py | حدود شدہ جدید TData ZIP ریڈر، چیک سم/ڈیکرپشن کی توثیق، کوئی استخراج نہیں |
| doctor.py | مقامی تیاری کی جانچ بغیر جمع، لاگ ان یا پیکیج انسٹالیشن کے |
| download.py | تصدیق شدہ اسٹریمنگ ایکسپورٹ ڈاؤن لوڈ محدود ریڈز کے ساتھ اور اوور رائٹس کے بغیر |
| monitoring.py | ورک اسپیس کی سطح پر ایونٹ پالیسی اور ہر قسم کے اٹیچمنٹ کے قواعد کی توثیق، ہینڈلرز، اسٹیٹس اور دستخط شدہ رسیدیں شیئر کی گئی ہیں۔ |
| scope.py | مشاہدے کا دائرہ (منتخب چیٹس، ٹیلیگرام فولڈر، پورا اکاؤنٹ)، ماخذ کی اقسام، استثنا، دوبارہ جانچ کی سطحیں |
| dossier.py | ہر چیٹ کے لیے محفوظ شدہ ریکارڈز کی بنیاد پر افراد کے پروفائلز: حقائق ریکارڈ حوالہ جات کے ساتھ، اوتار کا SHA-256/pHash، ذکر کی استخراج |
| witness_api.py | صرف پڑھنے کے لیے وِٹنس ٹوکنز اور وہ دستخط شدہ جرنل ہیڈ جو وہ حاصل کر سکتے ہیں |
| witness.py | آزاد شاہد کا عمل: اپنی کلید اور جرنل، ہیڈ چیکس، دستخط شدہ چینل پوسٹس، برآمد |
| alerts.py | اطلاع رسانی کے نوٹیفیکیشنز اور پینل کی نوٹیفیکیشن فہرست |
| logging_config.py | کنسول لاگنگ اور بغیر ونڈو کے لانچز کے لیے گردش پذیر سرور تشخیصی ٹولز |
| static/ | جوابی انٹرفیس، مقامی رسائی گیٹ، فلٹرز، تفصیلات، برآمدات، اکاؤنٹ سیٹ اپ |
| demo.py | صاف طور پر لیبل شدہ مصنوعی جرنل، حقیقی مجموعے سے الگ |

مشاہدے کے ہینڈلرز کنکشن سے پہلے رجسٹر کیے جاتے ہیں۔ لائیو کلیکشن فعال کلائنٹ شناختی نام، واضح چلنے والی حالت، فعال ذرائع یا مشاہدے کے دائرہ کار (فولڈر یا پورے اکاؤنٹ موڈز اپنی پہلی اپ ڈیٹ پر ایک نئے چیٹ کو بطور ماخذ شامل کرتے ہیں)، اور ایونٹ پالیسی کے ذریعے کنٹرول کی جاتی ہے۔ مسترد شدہ اور تبدیل شدہ کلائنٹس لائیو اپ ڈیٹس میں حصہ نہیں ڈال سکتے۔ خام ردعمل اور رکنیت کی اپ ڈیٹس نظر کی حد کو برقرار رکھتی ہیں۔ آنے والے پیغام کا مواد اور اس کا پائیدار میڈیا کام ایک ساتھ محفوظ کیا جاتا ہے۔ کام اصل TL ڈسکرپٹر کو برقرار رکھتے ہیں اور اس کے ہیش کو دستخط شدہ پیغام کے مشاہدے سے منسلک کرتے ہیں۔ بھیجنے والے/ایڈیٹر/مٹانے والے کے معنی الگ کیے جاتے ہیں۔

ہر ورک اسپیس ایک اکاؤنٹ قبول کرتا ہے اور اس کی اپنی ڈائریکٹری اور دستخطی شناخت ہوتی ہے۔ مطابقت کے لیے مرکزی ورک اسپیس روٹ پر ہی رہتا ہے؛ اضافی ورک اسپیس profiles/<id>/ میں موجود ہوتے ہیں۔ ایک بیئرر ٹوکن پوری تنصیب کو کنٹرول کرتا ہے؛ ورک اسپیس علیحدہ اجازت نامہ یافتہ کرایہ دار نہیں ہیں۔ پروسیس لاکس ڈائریکٹریز کا تحفظ کرتے ہیں؛ ڈیٹا بیس لاکس ایونٹ داخل کرنے کو ترتیب وار انجام دیتے ہیں۔ ہر اپنڈ (append) ایک ساتھ (synchronously) SQLite WAL میں FULL ہم وقت موڈ کے ساتھ کمٹ ہوتا ہے۔ ایونٹ اپ ڈیٹ/ڈیلیٹ ٹریگرز عام ایپلیکیشن ترمیمات کو روکتے ہیں؛ فائل سسٹم کے منتظمین اعتماد کی حد کے اندر رہتے ہیں۔

API authorization is a bearer token. Login operations are serialized and time-bounded. Account uploads use a dedicated 12 MiB encoded-body limit and an 8 MiB decoded-file limit; normal API requests retain the 16 KiB limit. Conversion runs in a worker thread, keeps uploads in memory, and returns normalized input to the authenticated browser. QR login has a per-workspace candidate, short-lived identifier, waiter task, and explicit cancellation. Only accepted authorization becomes the active client. Telegram FloodWait is returned with a Retry-After value; credentials and raw RPC error messages are not exposed in API errors. Journal exports run outside the async event loop and are serialized per workspace. They stream a stable read snapshot alongside continuing WAL writes. Chat acquisition jobs can run concurrently on separate accounts; each account remains reserved until its job stops. A paused or failed job retains its checkpoints. Successful archive verification permits cleanup of its working files, leaving the ZIP, signed plan and status. Workspace collectors share the process/event loop.

موجودہ ہسٹری کے سنپ شاٹس اور لائیو اپ ڈیٹس ایک دوسرے میں شامل ہو سکتے ہیں۔ دونوں الگ مشاہدات ہیں، جنہیں ماخذ کے مطابق لیبل کیا گیا ہے؛ ڈپلیکیٹس کو خاموشی سے ضم نہیں کیا جاتا۔ غائب آئی ڈیز، من گھڑی ہوئی حذف شدہ عبارت، زبردستی ممبر کی فہرست سازی، یا خودکار گروپ شمولیت سے کوئی نتیجہ اخذ نہیں کیا جاتا۔

آپریٹر کے لیے وضاحت کے لیے دیکھیں کہ[کلیکشن کیسے کام کرتی ہے](https://phishdestroy.github.io/TgWitness/ur/docs/reference/collection/) اور [اکاؤنٹس اور سیشن فارمیٹس](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/)۔

نیٹ ورک کی تشکیلات انکرپٹڈ والٹ میں محفوظ ہوتی ہیں۔ ایک روٹ لاگو کرنے سے پرانے کلائنٹس بند ہو جاتے ہیں اور نامکمل لاگ ان منسوخ ہو جاتا ہے؛ بعد کے کنکشنز اس روٹ کو بغیر کسی براہِ راست واپسی کے استعمال کرتے ہیں۔ ایک نئی بیرونی کلید کی تنصیب ہر ورک اسپیس کی فرنیٹ کلید کو ایک ماسٹر کلید فائل اور محفوظ شدہ بے ترتیب سالٹ سے HKDF-SHA256 کے ذریعے حاصل کرتی ہے۔ یہ رازوں کو ڈیٹا ڈائریکٹری سے الگ طور پر محفوظ رکھتی ہے، نہ کہ جर्नل/میڈیا کے غیر محفوظ مواد کو۔

مقامی ڈیمو انٹری ایک علیحدہ طور پر تیار کردہ پراسیس کیپابلیٹی استعمال کرتی ہے، کبھی بھی ترتیب شدہ پینل ٹوکن استعمال نہیں کرتی۔ اجرا اور قبولیت کے لیے واضح ڈیمو موڈ درکار ہوتا ہے، ایک مصنوعی روٹ بغیر اضافی ورک اسپیسز یا کسی مجاز سیشن کے، لوپ بیک پیئر/ہوسٹ، بغیر پروکسی فارورڈنگ ہیڈرز کے، اور بغیر کراس-اورجن براؤزر درخواست کے۔ لائو APIز بیئرر کی تصدیق برقرار رکھتی ہیں اور ڈیمو موڈ میں کلیکشن کی تبدیلیوں کو مسترد کر دیتی ہیں۔
