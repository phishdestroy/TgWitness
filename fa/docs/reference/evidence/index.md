# فرمت مدرک

Canonical page: https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/

محتویات فایل ZIP امضا شده، انواع سوابق، رسیدهای فرایند، پروفایل افراد، نسخه‌های خارج از محل و تأیید آفلاین.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [مستندسازی](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

TgWitness مشاهدات تلگرام قابل مشاهده در حساب کاربری را در یک دفترچه ثبت امضا شده نگهداری می‌کند. دریافت‌کنندگان می‌توانند سوابق ذخیره شده، پیوست‌ها و گزارش‌ها را با یک کلید گردآورنده مورد اعتماد تأیید کنند، سپس دفترچه ثبت را با یک نقطه کنترل که به طور مستقل نگهداری شده است مقایسه نمایند. این صفحه فرمت‌ها، بررسی‌ها و موادی را که باید برای تحویل نگهداری شود، توصیف می‌کند.

Recipients can start with **VERIFY.cmd** on Windows: it asks for the original ZIP and independently obtained key fingerprint, displays an explained result, and saves a separate verification transcript. See [verification launchers and the portable runtime](https://github.com/phishdestroy/TgWitness/blob/main/docs/VERIFICATION_LAUNCHER.md) for setup and trust limits.

**On this page**

- [What is signed](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#what-is-signed)
- [Comparing chat exports](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#comparing-chat-exports)
- [Investigation handoff](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#investigation-handoff)
- [Handover extract](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#handover-extract)
- [Readable reports](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#readable-reports)
- [Event canonicalization](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#event-canonicalization)
- [Actor semantics](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#actor-semantics)
- [Coverage: continuity, gaps and unobserved IDs](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)
- [Producer](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#producer)
- [People profiles](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#people-profiles)
- [Independent witness](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#independent-witness)
- [Manifest and checkpoints](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#manifest-and-checkpoints)
- [Verification scope](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#verification-scope)
- [Attachments](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#attachments)
- [Durable collection and process receipts (0.2)](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#durable-collection-and-process-receipts-02)
- [RFC 3161 preparation and response verification (0.2)](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)
- [Optional records in evidence mode: drand and Telegram devices](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)

## امضا شده چیست

| مطالب | حفاظت | چه مواردی را باید حفظ کرد |
| --- | --- | --- |
| هر مشاهدهٔ دفترچه، از جمله رویدادهای عملیاتی | زنجیره SHA-256 و امضای Ed25519 برای هر رویداد | امضای اصلی `events.jsonl`، اثر انگشت کلید مورد اعتماد، و یک نقطه کنترل حفظ‌شده |
| محتویات فایل ZIP شواهد | `manifest.sig` مانیفست کانونیکال را امضا می‌کند که هش فایل‌های محتوا را فهرست می‌کند | فایل فشردهٔ کامل، شامل مانیفست و امضا |
| پیوست‌های نگهداری‌شده | SHA-256 و شمارش بایت در یک رویداد امضا‌شده با `media.saved`؛ هش فایل در مانیفست ZIP امضا‌شده | بایت‌های اصلی درون فایل ZIP تأییدشده |
| نقطهٔ کنترل | امضای Ed25519 بر طول دفترچه، هش سر، کلید عمومی و زمان ایجاد | یک نسخهٔ مستقل که پیش از تغییر مورد مناقشه نگهداری شده است |
| دریافت رسید | Signed record of the collector version, source-file hashes and start settings, also included in `process.started` | The receipt, associated journal and the environment evidence for the selected verification mode |
| گزارش‌های قابل‌خواندن: `report.html` و اجزای آن، `report.json`، `report.pdf`، `chat.pdf` | یک مهر Ed25519 بر هر فایل بر روی محتوای آن؛ PDF همچنین دارای امضای استاندارد PDF است (رجوع کنید به [گزارش‌های قابل‌خواندن](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#readable-reports)) | فایل دریافت‌شده و اثر انگشت کلید مورد اعتماد؛ زیپی که آن را توصیف می‌کند |
| مستقل CSV | امضای رمزنگاری مستقل وجود ندارد؛ هش‌های رویداد به‌تنهایی کافی نیستند | برای بررسی یکپارچگی، از متن دقیق داخل فایل ZIP تأییدشده استفاده کنید. |
| اسکرین‌شات‌ها، خروجی‌های چاپی یا PDF تولیدشده توسط مرورگر | امضای TgWitness روی مشتق وجود ندارد | پکیج اصلی تأییدشده را حفظ کنید و نحوهٔ ساخت نسخهٔ مشتق را مستندسازی کنید |

جمع‌آورنده پیش از تولید هر فرمت خروجی، امضاهای دفترچه را تأیید می‌کند. گزارش‌های قابل‌خواندن HTML و PDF دارای مهرهای مخصوص به خود هستند؛ CSV مستقل به عنوان بخشی از یک فایل ZIP امضا شده بررسی می‌شود. فایل ZIP را برای حفظ بایت‌های پیوست و منیفست نگه دارید، و یک نقطه کنترل جداگانه برای بررسی دفترچه در مقابل یک مرز قبلی ایجاد کنید.

## Comparing chat exports

Verify and compare two signed chat-export ZIPs with independently retained signer fingerprints:

```
python -m tgwitness.verify first.zip --compare second.zip \
  --fingerprint FIRST_TRUSTED_KEY_SHA256 --compare-fingerprint SECOND_TRUSTED_KEY_SHA256
```

When both archives record the same numeric account and chat IDs, records are paired by message ID. **Unchanged** means equality of the complete saved JSON record: full text, author, dates, reply target, nested metadata and unknown fields are all included. JSON object key order does not matter; absent fields, nulls, value types and array order do. The 300-character preview is only for display. Changed entries name the differing top-level `changed_fields`, including changes invisible in that preview. Duplicate message IDs are rejected instead of overwriting one another during matching.

A difference can be a changed display name, view count, collection annotation or other observation metadata. It does not by itself establish a Telegram edit, identify who made a change, or prove which contradictory archive is accurate. Unparsed records remain in the comparison; equality of their saved representation does not mean their Telegram payload was decoded.

For different or missing account/chat identities, the tool only finds possible correspondences using sender, complete text, file hash, media type and a five-second time tolerance. It reports **Matched**, not **Unchanged**. These candidates do not establish message identity or equality of all metadata. Unparsed records remain unmatched. Differences in paired records remain listed in `changed`, including in content mode; these differences do not prove edits of the same message. With `--json`, `matched` counts pairs and `unchanged` counts pairs whose complete saved records are equal. Neither count proves message identity in content mode. The existing `changed_fields` and integer `unchanged` output remain compatible with earlier comparison results. Archive format and signature verification are unchanged.

## واگذاری تحقیقات

1. مرجع پرونده، اپراتور، شناسه عددی حساب تلگرام، منابع انتخاب‌شده، سیاست جمع‌آوری و دوره جمع‌آوری را در یادداشت‌های پرونده خود ثبت کنید. TgWitness مشاهدات را حفظ می‌کند و از یادداشت‌ها و مجموعه‌های مرتبط با منبع در [Case Board](https://phishdestroy.github.io/TgWitness/fa/docs/reference/case-board/) پشتیبانی می‌کند. سوابق انتقال و تحویل را همراه با مدارک پرونده خود نگهداری کنید. تنظیمات جمع‌آوری مورد نظر را با [رویه پذیرش زنده](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) بررسی کنید.
2. اثر انگشت کلید عمومی فضای کاری را به‌طور مستقل حفظ کنید پیش از آنکه به خروجی‌های آن اتکا کنید. نقاط کنترل امضا شده را در حین جمع‌آوری خارج از جمع‌کننده ذخیره کنید. وقفه‌ها و محدودیت‌های دیده‌شدن حساب را ثبت کنید.
3. یک فایل **ZIP امضا شده** صادر کنید و رسید اجرای امضا شده را نگه دارید. از یک نقطه کنترل در یا قبل از مرز روزنامه‌نگاری صادر شده استفاده کنید. یک نقطه کنترل بعدی می‌تواند به‌درستی یک خروجی قبلی را به‌دلیل کوتاه بودن بیش از حد رد کند. خروجی‌ها شامل کل روزنامه‌نگاری فضای کاری هستند، صرف‌نظر از فیلترهای پنل؛ پیش از اشتراک‌گذاری محتوا، آن را بررسی کنید.
4. از گیرنده بخواهید فایل ZIP را با یک نسخه مورد اعتماد از ابزار تأیید و اثر انگشت/نقطه کنترل ارائه‌شده به‌طور مستقل، اعتبارسنجی کند. از یک نصب مورد اعتماد که محیط پایتون آن فعال است:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   گزارش‌های خروجی موفق `key_pinned: true` و `checkpoint_checked: true` را زمانی که هر دو ورودی ارائه و پذیرفته شوند، صادر می‌کند. نتیجه تأیید را حفظ کنید.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. SHA-256 بایگانی، مرز خروجی، تاریخ انتقال، فرستنده و گیرنده را در سوابق نگهداری خود ثبت کنید. بسته اصلی را دست‌نخورده نگه دارید و روی نسخه‌ها کار کنید. فایل‌های مدرک را به اشتراک بگذارید، نه دایرکتوری داده‌های خصوصی برنامه را، که شامل جلسات حساب کاربری و اسرار امضا نیز می‌شود. برای انتقال، می‌توان خروجی را در یک فایل فشرده ZIP با رمزگذاری AES-256 و محافظت با رمز عبور قرار داد. این رمز عبور فقط محرمانگی را حفظ می‌کند و ذخیره نمی‌شود؛ دریافت‌کننده، فایل فشرده را استخراج کرده و خروجی امضا شده داخل آن را که بدون تغییر است، تأیید می‌کند.
   2. اگر لنگراندازی زمانی مستقل مورد نیاز است، [رویه RFC 3161](https://phishdestroy.github.io/TgWitness/fa/docs/reference/timestamp/) را دنبال کنید و درخواست، نقطه کنترل، اطلاعات CA مورد اعتماد و پاسخ مرجع تأییدشده را نگهداری کنید. صرفاً آماده کردن یک درخواست، مهر زمانی را به دست نمی‌دهد.

تأیید موفقیت‌آمیز، یکپارچگی را نسبت به کلید گردآورنده مورد اعتماد و مرز حفظ‌شده برقرار می‌کند. برای مشاهده فرضیات اعتماد و [نتایج اعتبارسنجی](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/) برای بررسی‌های انجام‌شده، به [«دامنه تأیید»](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#verification-scope) مراجعه کنید.

## استخراج هاند‌اوور

یک فایل ZIP امضا شده، کل مجلهٔ فضای کاری را در خود حمل می‌کند. هنگامی که دادگاه، وکیل یا میز رسیدگی به سوءاستفاده تنها به برخی چت‌ها، یک بازه زمانی یا افراد خاصی نیاز دارند، **گزینهٔ «صادرات → تحویل» (Exports → Handover)** یک نسخهٔ فشرده‌شده (`tgwitness-handover-v1`) را مطابق با قوانین افشای انتخاب‌شده آماده می‌کند. اپراتور هدف را اعلام می‌کند و چت‌ها، یک دوره اختیاری (UTC)، افرادی را که استخراج در مورد آن‌هاست، و اینکه با سایر افراد چه اتفاقی می‌افتد (نمایش داده شوند، با نام‌های مستعار P01 جایگزین شوند، P02… یا حذف شوند)، کدام متن‌های پیام باقی می‌مانند، کدام پیوست‌ها و عکس‌های پروفایل گنجانده می‌شوند، و اینکه آیا شماره‌های تلفن و آدرس‌های ایمیل در متن‌ها مخفی (ماسک) شوند. هدف و این قوانین در مانیفست امضا شده و در گزارش وجود دارند؛ مجله، `handover.exported` را با دسترسی‌ای که آن را آماده کرده و SHA-256 فایل را ثبت می‌کند، نه محتویات آن.

پایگاه `verify.py` یک استخراج را به دو روش بررسی می‌کند. رکوردی که بدون تغییر نشان داده می‌شود، به طور کامل تأیید می‌شود: محتوای آن با هش، امضای Ed25519 و لینک آن به رکورد قبلی مربوطه تطبیق داده می‌شود. یک رکورد بهینه‌شده، هش و امضای اصلی را حفظ می‌کند، بنابراین امضا همچنان معتبر است، اما فیلدهای پنهان‌شده را نمی‌توان از آن بازحساب کرد؛ رکورد مشخص می‌کند چه چیزی پنهان شده است و گزارش آن را علامت‌گذاری می‌کند. مانیفست، طول ژورنال و سرآیند را با امضای گردآورنده در بالای آن سرآیند مشخص می‌کند، و رکوردهای حذف‌شده را می‌شمارد؛ فایل `coverage.json` چت‌های انتخاب‌شده را توصیف می‌کند. نام‌های داخل نام فایل‌ها شناسایی نمی‌شوند. پیش از اشتراک‌گذاری، فایل‌های نهایی را بازبینی کنید: متن آزاد، نام فایل‌ها و پیوست‌های منتخب همچنان می‌توانند افراد را شناسایی کنند. فایل ZIP امضا شده کامل را نگه دارید: فایل استخراج‌شده یک افشا است، نه جایگزین.

## گزارش‌های قابل‌خواندن

شواهد امضا شده، فایل‌های ZIP تحویل و چت، گزارش‌های قابل خواندن HTML و JSON را همراه با PDF در صورت در دسترس بودن فونت‌های مورد نیاز، در زبان گزارش انتخابی، حمل می‌کنند. هر گزارش با کلید Ed25519 فضای کاری مهر و موم شده و می‌توان آن را به صورت جداگانه تأیید کرد: `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]`.

- `report.html` / `chat.html`: بیانیه مهر (`tgwitness-report-seal-v1`) فایل را می‌بندد و SHA-256 هر بایت قبل از آن را امضا می‌کند. ژورنال‌ها و چت‌های طولانی به بخش‌هایی با اندازه قابل پیکربندی تقسیم می‌شوند (تنظیمات گزارش، ۵۰۰ تا ۱۰۰٬۰۰۰ رکورد؛ به‌صورت پیش‌فرض ۵٬۰۰۰): `records/records-0001.html` یا `messages/messages-0001.html`، که هر کدام با شماره، بازه و مجموع خود مهر و موم شده و در منیفست امضا شده به همراه SHA-256 خود فهرست می‌شوند. سلسله‌ای از ضربان‌های قلب جمع‌کننده به صورت یک خط نمایش داده می‌شوند، مگر اینکه در تنظیمات گزارش به صورت جداگانه فهرست شده باشند.
- `report.json` (`tgwitness-report-json-v1`، کلیدهای `format`، `report`، `seal`): مهر، SHA-256ِ JSONِ `report` را امضا می‌کند، بنابراین حقایق می‌توانند توسط سیستم‌های موردی و اسکریپت‌ها خوانده شوند و می‌توان از آن‌ها برای انتخابی جهت حفاظت از داده‌ها استفاده کرد، در حالی که فایل امضا شده دست‌نخورده باقی می‌ماند.
- `report.pdf` / `chat.pdf`: یک سند رسمی برای چاپ و بایگانی، که دو بار بر روی همان بایت‌ها امضا شده است، کل فایل به جز مقدار امضا (`/ByteRange`). امضای استاندارد PDF (`adbe.pkcs7.detached`، CMS با SHA-256 و ECDSA P-256) از یک سند امضای خود صادر شده استفاده می‌کند گواهی که در گاوصندوق فضای کاری نگهداری می‌شود؛ شماره سریال سوژه آن اثر انگشت کلید Ed25519 است. مهر Ed25519 به عنوان ویژگی بدون امضا CMS در داخل `2.25.240684792623320047764573196045913242332` جابجا می‌شود و SHA-256 را با `"content": "pdf-byte-range"` نام‌گذاری می‌کند، بنابراین کلید Ed25519 ضامن اعتبار گواهی است. یک خواننده PDF نشان می‌دهد که آیا فایل پس از امضا تغییر کرده است یا خیر و تا زمانی که گواهی مورد اعتماد قرار نگیرد، امضاکننده را ناشناس می‌نامد؛ در عوض اثر انگشت Ed25519 را مقایسه کنید. فایل‌های PDF چینی، ژاپنی و کره‌ای به یک فونت روی سرور (یا در `TGWITNESS_FONT_DIR`) نیاز دارند؛ بدون آن، فایل ZIP فقط حاوی گزارش‌های HTML و JSON خواهد بود.

در یک کانال یا ابرگروه، Telegram پیام‌های ۱، ۲، ۳ و ... را به ترتیب شماره‌گذاری می‌کند. یک خروجی چت، شماره‌های اول و آخر، تعداد کل پیام‌ها، هر سری از شماره‌های غایب در `message-ids.json` ، مانیفست و هدر `chat.json` را فهرست می‌کند و هر شکاف را در جایی که در متن گفتگو قرار دارد، علامت‌گذاری می‌کند. `verify.py` آنها را از `chat.json` شمارش می‌کند. یک شماره غایب، پیامی است که Telegram بازنگشت (پیش از خروجی‌گیری حذف شده یا برای حساب قابل مشاهده نبوده است)؛ در چت‌های خصوصی و گروه‌های پایه، شماره‌ها در تمام چت‌های یک حساب مشترک هستند و فاصله‌ها شمرده نمی‌شوند.

After reading the history, the export asks Telegram for every absent number again, by number (`channels.getMessages`, up to 10,000 numbers). The result is in `message-ids.json` and the report. An empty answer records that the number is unavailable to this account at recheck time; it leaves the cause unspecified. A message returned on recheck is added to the export and marked `found_on_recheck`.

هر گزارش با **آغاز می‌شود. به اختصار**: یک پاراگراف، سپس آنچه که محتوا نشان می‌دهد و آنچه که نشان نمی‌دهد (چه کسی پشت یک حساب کاربری است، کامل بودن تحویل، حذف‌ها پیش از مشاهده، زمان ساعت بدون مهر زمانی). مهر و موم صفحه زمانی به رنگ کهربایی درمی‌آید که مرورگر امضای مهر و موم را بررسی کرده باشد، نه خود صفحه را: مرورگر بایت‌های یک صفحه را به آن اختصاص نمی‌دهد. این رنگ فقط زمانی به سبز تغییر می‌کند که خواننده فایل را در قسمت بررسی در انتهای صفحه قرار دهد و تمام بایت‌ها مطابقت داشته باشند، و تنها در صورتی که صفحه نمایش داده شده همان فایل باشد؛ در غیر این صورت به قرمز تغییر می‌کند.

هر گزارش برنامه را دقیقاً نام می‌برد: commit گیت زمانی که گردآورنده از یک checkout اجرا می‌شود یا نصب‌کننده `TGWITNESS_COMMIT` را تنظیم می‌کند، و SHA-256 فایل‌های منبع آن (`source_tree_sha256`، JSON کانونیکال از path → SHA-256 هر `.py`، `.js`، `.css`، `.html` و `.svg` فایل در بسته)، که یک checkout از آن commit آن را بازتولید می‌کند مگر اینکه فایل‌ها تغییر کرده باشند). کلاینت Telegram با نام کتابخانه، لایه API و مرکز داده خود نامگذاری شده است. هنگامی که مشاهده شروع می‌شود و زمانی که خروجی چت آغاز و پایان می‌یابد، گردآورنده زمان را از Telegram می‌پرسد (`updates.getState`، ثانیه‌های کامل) و زمان Telegram منهای ساعت گردآورنده را به همراه عدم قطعیت ناشی از رفت و برگشت ثبت می‌کند؛ گزارش‌ها این اندازه‌گیری‌ها را تحت عنوان «زنجیره امانت» (Chain of custody) نشان می‌دهند. صادرات چت، علاوه بر تاریخ‌های پیام‌ها، زمان خواندن تاریخچه را نیز ثبت می‌کند.

### نمایشگر گزارش آفلاین و راهنمای بایگانی

قبل از باز کردن `chat.html` یا `report.html`، فایل ZIP کامل را استخراج کنید. این ویوئر قابلیت جستجو، فیلترها، شرکت‌کنندگان، شاخص‌ها، جزئیات رکورد و گزینش‌های JSON/CSV را بدون نیاز به سرور فراهم می‌کند. فایل‌های `viewer/` و `media/` را در کنار گزارش نگه دارید. گزینش‌ها مشتق هستند: برای مقایسه آنها با آرشیو امضا شده، از `verify.py SELECTION.json
--evidence ARCHIVE.zip` استفاده کنید. اعتبارسنج، شناسه گزارش، کلید امضا، مرز بایگانی و هر مورد انتخاب‌شده را بررسی می‌کند؛ موارد ویرایش‌شده، مفقود و تکراری ناموفق هستند. یادداشت‌های انتخاب و زمان ایجاد، متاداده‌های بدون امضا باقی می‌مانند.

شکاف‌های شماره‌ی پیام‌ها تنها در جریان چت کامل، بدون فیلتر و صعودی نمایش داده می‌شوند. پنهان کردن یک دسته‌بندی یا عدم بارگذاری یک بلوک داده نباید یک سطر حذف‌شده را به مدرکی برای وجود پیامی که مفقود شده است تبدیل کند. برجسته‌سازی‌های جستجو روی متن ساده قبل از فرارگیری HTML اعمال می‌شوند و نشانه‌گذاری‌های تحت‌اللفظی را حفظ می‌کنند.

این مرورگر امضاهای مانیفست، شناسه و کلید گزارش و تمام هش‌های فایل‌های فهرست‌شده را بررسی می‌کند. این ابزار ساختارهای ZIP مبهم یا ناقص، نام‌های تکراری و مسیرهای ناامن را رد می‌کند و فایل‌ها را به حداکثر ۲۵۶ مگابایت (MiB) و مجموع محتوای اعلام‌شده را به ۴ گیگابایت (GiB) محدود می‌نماید. برای آرشیوهای بزرگ‌تر از اعتبارسنج مستقل استفاده کنید. این بررسی مرورگر، بررسی‌های اعتبارسنج را که بر زنجیره‌های دفترچه خاطرات و معنایی داده‌ها انجام می‌دهد، تکمیل می‌کند.

`README.txt` شامل یک راهنمای شروع، فهرست فایل‌ها، دستورالعمل‌های تأیید و یادداشت‌های قالب داده به زبان گزارش است و پس از آن یک راهنمای کامل انگلیسی قرار دارد. فایل `SHA256SUMS` شامل فایل‌های فهرست‌شده در خود، به استثنای خودِ آن، `manifest.json` و `manifest.sig` است؛ مانیفست امضا شده همچنین شامل `SHA256SUMS` می‌شود. فایل ZIP اصلی را دست‌نخورده نگه دارید و فایل‌های در حال کار را خارج از پوشه استخراج‌شده ذخیره کنید. گزارش‌های PDF شامل نشانک‌های بخش و شناسایی پرونده/گزارش در صفحات بعدی هستند.

### گفت‌وگو در زمان صدور

صادرات یک چت، آنچه را که Telegram در مورد چت هنگام شروع صادرات گفته است، ثبت می‌کند: برچسب‌های خود Telegram (`scam`، `fake`، `restricted` با دلایل آن، `verified`)، نام‌های کاربری، توضیحات، تعداد اعضا و ادمین‌ها، بحث مرتبط، حفاظت از محتوا، اینکه آیا اعضای جدید پیام‌های قبلی را می‌بینند و از کدام پیام به بعد در این حساب تاریخچه قابل مشاهده است (`available_min_id`)، تاریخ پیام ۱ که همان تاریخ ایجاد چت است، و SHA-256 عکس چت (ذخیره شده در `media/`). این اطلاعات جایگاه حساب صادرکننده در چت را ثبت می‌کند: نقش، تاریخ پیوستن، اینکه چه کسی آن را دعوت کرده و برای یک ادمین، حقوق او. در عوض، درخواستی که Telegram رد می‌کند، نام‌گذاری می‌شود.

وقتی حساب صادرکننده، ادمین باشد، خروجی، لاگ ادمین چت را (Telegram حدود ۴۸ ساعت نگه می‌دارد) در `admin-log.json` ثبت می‌کند: حذف‌ها و ویرایش‌ها به همراه محتوا و حسابی که اقدام کرده است. این تنها سوابق یک حذف است که نام حذف‌کننده را مشخص می‌کند.

### شاخص‌ها

گزارش‌ها فهرست می‌کنند، و آرشیو شامل موارد زیر است که در پیام‌های ضبط‌شده، میز رسیدگی به تخلفات می‌تواند بر اساس آن‌ها اقدام کند: `indicators.csv` ، `indicators.stix.json` (STIX 2.1 ) و `indicators.misp.json` (رویداد MISP ): لینک‌ها و دامنه‌ها (که همچنین پشت متن، در دکمه‌ها و در پیش‌نمایش لینک‌ها پنهان شده‌اند)، آدرس‌های ارز دیجیتال، نام‌های کاربری و لینک‌های دعوت Telegram ، شماره‌های تلفن، آدرس‌های ایمیل و تصاویر ذخیره شده. آدرس‌های بیت‌کوین، لایت‌کوین، دوج‌کوین و ترون فقط زمانی فهرست می‌شوند که چک‌سام base58 آنها معتبر باشد، آدرس‌های سگ‌ویت زمانی که چک‌سام bech32 یا bech32m آنها معتبر باشد و آدرس‌های تون زمانی که CRC آنها معتبر باشد؛ آدرس‌های EVM و سولانا به عنوان بررسی‌نشده علامت‌گذاری می‌شوند. تصاویر دارای هش SHA-256 و هش دیداری (dHash، ۶۴ بیتی) هستند که در کپی‌های فشرده‌سازی یا تغییر اندازه مجدد شده، تقریباً بدون تغییر باقی می‌ماند. گزارش‌ها شاخص‌ها را طوری می‌نویسند که به طور تصادفی باز نشوند (`hxxps[://]example[.]com` )؛ فایل‌ها مقادیر را همان‌طور که بوده‌اند حفظ می‌کنند. هر شاخص به عنوان ناشناخته و نه برای تشخیص خودکار علامت‌گذاری شده است (STIX `indicator_types: unknown` , MISP `to_ids: false` ، توزیع در سازمان خود): قرار گرفتن در لیست به این معناست که پیامی حاوی آن بوده است، نه اینکه مخرب باشد. لینکی که متن آن آدرس متفاوتی را نسبت به آدرسی که با آن باز می‌شود نشان می‌دهد، در گزارش علامت‌گذاری می‌شود.

گزارش‌های PDF با اظهاریه‌ای از بازرس برای امضای دستی، یک چک‌لیست برای دفتر اسناد رسمی یا کارشناس دادگاه، و یک کد QR (که در صفحه اول نیز وجود دارد) به پایان می‌رسند که حاوی شناسه گزارش، اثر انگشت کلید و SHA-256 داده‌های معتبر است، به طوری که یک نسخه چاپی به آرشیو مربوطه منتهی می‌شود.

## کانونی‌سازی رویداد

ورودی هش دقیقاً شامل این فیلدها است:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

سریال‌سازی با JSON سازگار با پایتون با UTF-8، کلیدهای شیء مرتب‌شده، بدون فرار ASCII، بدون فاصله‌های خالی بی‌اهمیت و بدون NaN/بی‌نهایت:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

هَش رویداد از SHA-256 آن بایت‌ها به‌دست می‌آید. امضا، امضای Ed25519 بر روی ۳۲ بایت خام هَش است که سپس به کد base64 تبدیل می‌شود. اولین previous_hash شامل ۶۴ صفر است. اعداد توالی از ۱ شروع شده و به اندازه ۱ افزایش می‌یابند. تمام رویدادها، از جمله رویدادهای عملیاتی، یک زنجیره مشترک دارند. هیچ سرکوب ارسال تکراری وجود ندارد: مشاهدات مکرر رسیدهای متمایزی هستند، نه ادعایی مبنی بر اقدامات متمایز تلگرام.

تاریخ‌های خام تلگرام رشته‌های ISO هستند؛ فیلدهای باینری به اشیایی حاوی bytes_base64 تبدیل می‌شوند. متن پیام، انتیت‌ها، توصیف‌کننده‌های رسانه، متادیتای پاسخ، واکنش‌ها و اقدامات سرویس، در صورت ارائه، در متادیتای خام پیام حفظ می‌شوند.

observed_at ساعت دیواری UTC گردآورنده است. source_at تاریخ تلگرامی ارائه‌شده در صورت موجود بودن است. اعلان‌های حذف، زمان دقیق حذف را ارائه نمی‌دهند، بنابراین source_at نامشخص باقی می‌ماند. ترتیب دریافت در انتقال لزوماً با ترتیب رویداد منبع مطابقت ندارد. اسنپ‌شات‌های تاریخچه از تاریخ‌های منبع قدیمی‌تر اما زمان‌های مشاهده فعلی استفاده می‌کنند.

## سمانتیک بازیگر

actor_id در message.new، فرستنده پیام است. message.edited ویرایشگر مشخصی ندارد؛ payload.sender_id فرستنده پیام مشاهده‌شده را ثبت می‌کند. حذف actor_id همچنان null باقی می‌ماند. پیام‌های سرویس عضویت، فرستنده و نوع اقدام را حفظ می‌کنند، بدون اینکه هر حذف را به یک ترک داوطلبانه تبدیل کنند. به‌روزرسانی‌های خام شرکت‌کننده، actor_id را همان‌طور که ارائه شده حفظ می‌کنند. اسنپ‌شات‌های واکنش، یک عامل تغییر را ابداع نمی‌کنند.

اعلان‌های حذف برای چت‌های خصوصی و گروه‌های عادی فقط شامل شناسه پیام‌ها هستند. این چت‌ها یک توالی شناسه یکپارچه در سطح حساب را به اشتراک می‌گذارند، بنابراین یک شناسه، یک پیام واحد از این حساب را شناسایی می‌کند. زمانی که پیامی با آن شناسه قبلاً در این دفترچه ثبت شده باشد، حذف در آن چت به عنوان message.deleted با payload.chat_resolution به عنوان نام متد ثبت می‌شود. شناسه‌هایی که هرگز ذخیره نشده‌اند به صورت deletion.unscoped بدون chat_id نگه داشته می‌شوند؛ هیچ چیز حدس زده نمی‌شود. کانال‌ها و ابرگروه‌ها پیام‌ها را در هر چت شمارش می‌کنند و هرگز به این شکل مطابقت داده نمی‌شوند. هنگامی که پیام حذف‌شده توسط حساب مشاهده‌شده ارسال شده باشد، payload.deleted_message_was_outgoing مقدار true را دارد؛ اما هویت حذفی هنوز مشخص نمی‌شود.

An unscoped notice does not establish that a message was never saved: a matching chat may be outside the current observation scope, or a unique match may be unavailable. Recheck absence remains a separate observation from a deletion notification in report counts, filters and labels. A later recovery clears the current missing state while preserving the earlier unsuccessful check in the signed history; neither observation establishes a deletion notice.

Multiple IDs resolved to the same chat from one notification are grouped as `deletion.batch`, regardless of their count. The notification does not establish that the entire history was cleared, who performed the deletion, or whether it applied to all participants. Saved outgoing messages do not change these limits. Older journals may contain `history.cleared` events inferred from batches of ten or more IDs, with explanatory text attributing the deletion to the other participant. Those inferences are not supported by the update. Preserve those original signed records, but treat them as grouped deletion notifications; the current interface labels them accordingly.

## پوشش: پیوستگی، فواصل و شناسه‌های نادیده

هر فایل ZIP امضا شده حاوی `coverage.json` است، گزارش HTML با همان خلاصه باز می‌شود و `verify.py` آن را از روی `events.jsonl` بازحساب می‌کند به جای اینکه به فایل اعتماد کند:

- **به‌طور مداوم از X تا Y مشاهده می‌شود.** یک دوره با `observation.started` آغاز می‌شود و در یک مکث، یک توقف، قطع اتصال تلگرام، خروج، شروع فرآیندی بدون توقف منظم، یا بیش از سه دقیقه بدون هیچ ثبت در حین مشاهده پایان می‌یابد (تپش‌های قلب هر دقیقه ثبت می‌شوند، بنابراین سکوت به معنای توقف فرآیند، یخ‌زدگی یا خواب رفتن کامپیوتر است). هنگامی که فاصله تپش قلب در **بخش پارامترها** تغییر کند، هر تپش آن را ثبت می‌کند و سکوت مجاز به سه بازه تبدیل می‌شود، که هرگز کمتر از سه دقیقه نخواهد بود.
- **شکاف‌ها** زمان بین دوره‌ها را همراه با دلیل فهرست می‌کنند. شکافی که در آخرین ثبت هنوز باز است با `not_resumed_by_last_record` علامت‌گذاری می‌شود.
- **شناسه پیام‌های مشاهده‌نشده.** برای کانال‌ها و ابرگروه‌ها، که پیام‌ها را به‌ازای هر چت شمارش می‌کنند، شناسه‌هایی که بین موارد مشاهده‌شده مفقود هستند به‌صورت بازه فهرست می‌شوند. آن‌ها به‌عنوان *مشاهده‌نشده* گزارش می‌شوند — حذف‌شده، هرگز تحویل‌داده‌نشده، یا خارج از تاریخچه ذخیره‌شده — هرگز به‌عنوان حذف‌شده. چت‌های خصوصی و گروه‌های عادی از یک توالی در سراسر حساب استفاده می‌کنند، بنابراین فواصل درون یکی از این چت‌ها معنایی ندارند و در آنجا فهرست نمی‌شوند.
- اخطاریه‌های شکاف در سطح گفتگو (برای مثال درخواست تلگرام برای بازیابی تفاوت در یک کانال) به‌عنوان یادداشت محسوب می‌شوند؛ آن‌ها پوشش کلی را مختل نمی‌کنند.

### شماره‌های پیام‌های مفقود (`gap_summary`)

**پیش‌نمایش.** `coverage.json` → `gap_summary` اعدادی را که تلگرام اختصاص داده و این گردآورنده هرگز ندیده است، اندازه‌گیری می‌کند. تلگرام پیام‌ها را یک‌بار در هر کانال یا ابرگروه، و یک‌بار در هر حساب کاربری در سراسر چت‌های خصوصی، ربات‌ها و گروه‌های عادی شماره‌گذاری می‌کند. عددی بین دو پیام مشاهده‌شده یا مشاهده شده یا مفقود است؛ یک بازه پیوسته، این گزاره مثبت را بیان می‌کند که هر پیام شماره‌گذاری‌شده در آن مشاهده شده است. یک شکاف، نه کنشگری را نام می‌برد و نه دلیلی را.

| میدان | معنی |
| --- | --- |
| `status` | `on`، یا `off` وقتی در **پارامترها → تحلیل شکاف** غیرفعال شود |
| `parameters` | پارامترهایی که نتیجه را تولید کرده‌اند، تا بتوان آن را تکرار کرد |
| `chats[]` | برای هر کانال یا ابرگروه یک ورودی، که هر کدام به‌طور جداگانه شماره‌گذاری شده‌اند |
| `account` | سلسلهٔ سراسری حساب شامل چت‌های خصوصی، ربات‌ها و گروه‌های عادی |
| `status` (به ازای هر توالی) | `applicable`، یا `not_applicable` با `reason` |
| `observed_from`, `observed_to`, `span` | اولین و آخرین شماره مشاهده‌شده و اندازهٔ بازه |
| `observed`, `observed_without_content` | اعداد مشاهده‌شده؛ اعدادی که تنها از طریق سوابق حذف یا بازبینی مجدد شناخته می‌شوند |
| `missing`, `density`, `gap_ranges`, `largest_gap` | اعدادی که هرگز مشاهده نشدند، سهم آن‌ها از بازه، تعداد اجراها، طولانی‌ترین اجرا |
| `clusters[]` | شکاف‌های فهرست‌شده: `low`, `high`, `missing`، و اعداد مشاهده‌شده مجاور `after` / `before` به همراه زمان‌های مشاهدهٔ آن‌ها |
| `service_estimate` | فقط زمانی که فعال باشد: چند شماره مفقود بر اساس سهم مشاهده‌شده‌شان به‌عنوان پیام‌های خدماتی محسوب می‌شوند. هرگز از `missing` |

اعتبار از ژورنال استخراج می‌شود، هرگز فرض نمی‌شود:

- **کانال‌ها و ابرگروه‌ها** به‌ازای هر چت اندازه‌گیری می‌شوند، همچنین در خروجی چت‌های منتخب. سوابق انتخاب‌شده توسط فرستنده اندازه‌گیری را انجام می‌دهند. `not_applicable`.
- **سecuence در سطح کل حساب** فقط از اولین پیام تا آخرین پیامی که در حالی که جمع‌آوری کل حساب فعال بود دریافت شد، اندازه‌گیری می‌شود و چت‌های خصوصی، ربات‌ها، گروه‌های عادی و پیام‌های خود حساب را حفظ می‌کند، بدون اینکه هیچ چتی مستثنی شود (`scope.changed`). اعدادی که توسط `deletion.unscoped` به‌عنوان مشاهده‌شده بدون محتوا شمرده می‌شوند. خروجی‌گیری یا واگذاری چت‌های انتخابی نمی‌تواند آن را اندازه‌گیری کند. اگر جمع‌آوری کل حساب خاموش و سپس روشن شود، یادداشتی می‌گوید که اعدادی که در این فاصله استفاده شده‌اند، به‌صورت شکاف ظاهر می‌شوند.
- پیام‌های سرویس، رکوردهای دفترچه یادداشت با شماره‌های اختصاصی خود هستند، بنابراین خودِ شکاف‌هایشان را می‌بندند؛ برآورد اختیاری تنها یک زمینه است.

`verify.py` محاسبه مجدد `gap_summary` از `events.jsonl` با پارامترها در ژورنال امضا شده `coverage.json` member (پیش‌فرض برای آرشیوهای قدیمی‌تر) و خط مربوط به کل حساب را در خلاصه پوشش خود چاپ می‌کند. آرشیو `get_capture_status`(MCP و خط فرمان) همان اندازه‌گیری را برای گفتگوهایی که یک دسترسی می‌تواند بخواند بازمی‌گرداند؛ سecuence در سطح کل حساب فقط برای دسترسی‌ای که کل فضای کاری را پوشش می‌دهد.

Repeated observations of one service message count once, and the account service estimate uses only numbers inside the measured range. An applied scope must explicitly preserve the account's own messages before account-wide measurement is enabled; older records without that information cannot establish this condition. Stopped observation does not extend the measured range, and resuming it is noted. The live archive query has a time budget, including its database scan, and marks an unfinished measurement as partial.

Telegram documents the [separate message ID sequences](https://core.telegram.org/api/updates#message-id-sequences). These numbers describe observations; they do not identify a deletion actor or establish why a number is absent.

زمانی که Telegram پذیرش حساب را متوقف می‌کند، رکورد `coverage.gap` که نظارت را پایان می‌دهد، حاوی `cause` (`account_banned`، `account_frozen`، `account_deleted`، `session_duplicated`، `session_revoked`، `session_expired`، `session_ended` یا `not_authorized`) و خطای Telegram است؛ `verify.py` علت پایان دوره را نام‌گذاری می‌کند.

Coverage combines recorded observation periods, interruptions and message outcomes. Assess it together with the selected chats, period and attachment policy; continuous operation alone does not establish complete delivery of Telegram updates.

## تهیه‌کننده

مفاد امضاشده ZIPهای شواهد، خروجی‌های چت، دفترچه‌های شاهدی و بیانیه فایل‌های پروفایل افراد حاوی `producer` هستند: نرم‌افزار، نسخه، پروژه (PhishDestroy)، صفحه اصلی و مخزن منبع. گزارش HTML همان خط را نشان می‌دهد، و `verify.py` آن را به عنوان بخشی از آنچه تأیید کرده است، چاپ می‌کند. آرشیوهایی که قبل از وجود این فیلد ایجاد شده‌اند، تأیید می‌کنند که قبلاً بوده و گزارش می‌شود که تولیدکننده‌ای را نام نبرده‌اند.

هر رکورد `observation.started` همچنین نام کلاینت Telegram را که مشاهده کرده است، ذکر می‌کند: `api_id` آن (هرگز هش آن)، اینکه آیا این یک جفت عمومی داخلی است یا اپلیکیشن خود اپراتور، توضیحات کلاینت ارسال‌شده در درخواست اتصال Telegram، و نوع مسیر اتصال با حالت IP (بدون آدرس پروکسی یا رمز). گزارش و `custody.json`، هر کلاینت و مسیر متمایز را به همراه زمان ثبت آن‌ها، و زمان‌هایی که هیچ پروکسی فهرست‌شده پاسخ نداد و Telegram آدرس سرور را مشاهده کرد، فهرست می‌کنند. ژورنال‌های ثبت‌شده پیش از این نیز همین را نشان می‌دهند.

## پروفایل‌های افراد

یک فایل پروفایل (`tgwitness-dossier-v1`، JSON) به درخواست از روی سوابق موجود در دفترچه خاطرات برای یک چت ساخته می‌شود؛ هیچ چیزی از تلگرام دریافت نمی‌شود و محتوای پروفایل هرگز در دفترچه خاطرات نوشته نمی‌شود (فعال و غیرفعال کردن پروفایل‌ها به عنوان `dossier.changed` ثبت می‌شود). برای هر شخص دارای پیام ذخیره شده، تاریخچه نام و نام کاربری، برچسب‌های تلگرام (ربات، کلاهبرداری، جعلی، پریمیوم، تأیید شده، محدود، حذف شده) همان‌طور که در زمان ذخیره مشاهده شده، پروفایل شناسه عکس‌ها، هش SHA-256 و هش بصری (pHash، سازگار با `imagehash.phash`) آواتار از کش آواتار محلی با آواتارهای مشابه، فعالیت (اولین و آخرین پیام، شمارش‌ها، اشتراک‌گذاری‌های ویرایش‌شده و حذف‌شده، پیام‌ها بر اساس ساعت UTC)، اینکه چه کسی به چه کسی پاسخ می‌دهد، چت‌های دیگر در این گزارش، جایی که آن شخص نوشته و از کیف‌پول‌ها (BTC، EVM، TRON، TON، LTC، DOGE، XMR، SOL؛ آدرس‌های Base58Check اعتبارسنجی شده‌اند) یاد کرده است، شماره‌های تلفن، نام‌های کاربری و لینک‌ها، از جمله لینک‌های پنهان‌شده پشت متن.

هر واقعیت فهرست سوابق دفترچه (`seq`) را که از آن آمده است، ذکر می‌کند و `record_hashes` حاوی هش هر رکورد مرجع است. این بیانیه با کلید فضای کاری امضا شده است:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

امضا را بررسی می‌کند، خودِ خروجی مدرک را (امضا، زنجیره هش و فایل‌ها) اعتبارسنجی می‌کند و اطمینان حاصل می‌کند که هر رکورد ارجاع‌داده‌شده در همان خروجیِ همان فضای کاری بدون تغییر وجود دارد. هش‌های آواتار برچسب «منبع از کش محلی» (نه رکوردهای دفترچه) را دارند. @ها تطبیق الگو هستند — سرنخی برای بررسی، نه حقایق تأییدشده. پروفایل‌ها به صورت جداگانه برای هر چت فعال می‌شوند، می‌توانند به صورت یک فایل فشرده ZIP با رمزگذاری AES-256 صادر شوند و هنگام غیرفعال شدن یا حذف چت از منابع، پاک می‌گردند.

## شاهد مستقل

دفترچه یادداشت شاهد (`tgwitness-witness-v1`) و پست‌های کانال آن با خروجی مدرک با `verify.py --witness … --channel …` مطابقت داده می‌شوند؛ به [شاهد مستقل](https://phishdestroy.github.io/TgWitness/fa/docs/reference/witness/) مراجعه کنید.

## منشور و نقاط کنترل

فایل manifest.json شامل فرمت، زمان خروجی، کلید عمومی، اثر انگشت، طول دفترچه، هش سر، دامنه، تولیدکننده، محدودیت‌ها و SHA-256 هر عضو محتوای دیگر به جز خود `manifest.json` و `manifest.sig` است. فایل manifest.sig امضای Ed25519 در قالب base64 بر روی JSON کانونیکال manifest است. اعتبارسنج، اعضای غیرمنتظره/غایب، نام‌های تکراری، فایل‌های خراب، توالی/زنجیره شکسته، امضاهای نامعتبر و عدم تطابق با نقطه کنترل ارائه‌شده را رد می‌کند. این هیچ‌گاه مسیرهای آرشیو را استخراج نمی‌کند. اندازه کل اعلام‌شده بدون فشرده‌سازی را به ۴ گیگابایت محدود می‌کند؛ `--max-gib N` آرشیوهای بزرگ‌تری را که با افزایش حد **پارامترها** ساخته شده‌اند، مجاز می‌داند.

Run verification from your installed TgWitness version or a reviewed checkout. The copy included in an archive supports portable use; check that copy against your trusted installation before executing it.

A checkpoint signs a statement containing the public key, journal length, head hash, and creation time. The verifier can check that a later archive contains the same prefix. Retain the checkpoint outside the collector, so later verification compares the archive with a reference held separately from it.

## دامنهٔ اعتبارسنجی

Verification checks the archive and the collection mode used to produce it. Choose the mode whose trust boundary matches the case, then retain its verification inputs.

| حالت جمع‌آوری | آنچه اعتبارسنج بررسی می‌کند | ورودی‌های اعتبارسنجی و مرز اعتماد |
| --- | --- | --- |
| فضای کاری محلی | Record signatures, hash chain, manifest and attachment bytes | Independently retained collector fingerprint; the host administrator controls the local signing key |
| محیط کاری محلی با شاهد مستقل | آرشیو بررسی می‌کند و با پیش‌وند ژورنال قبلی که توسط شاهد حفظ شده است، تطابق را بررسی می‌کند | Separately trusted witness key and records; the checkpoint binds the prefix already observed |
| [GitHub Actions ضبط می‌کند](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) | GitHub attestation of the archive digest, approved workflow and collector commits, hosted runner, fresh session/key origin and internal archive integrity | Trusted verifier policy, caller repository and GitHub attestation bundle; collection runs under the pinned workflow |
| [استقرار ابری](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/) | Provider lifecycle and access records, firewall and Cloudflare state, plus the collector's signed run record | Read-only queries to the provider and Cloudflare; availability of individual checks depends on the provider |
| [ماشین مجازی محرمانه Intel TDX](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx) | Quote signature and platform status, binding to the collector statement, compose and OS measurements | Intel trust chain and expected deployment measurements; retain the results of every required TDX check |

In sealed acquisition, the approved collector receives data through an authenticated Telegram connection inside the verified environment. Attestation binds the archive to that execution, so verification covers acquisition as well as later file integrity. This relies on the approved code and the platform trust chain listed above. GitHub capture verification requires a session created inside the run and rejects imported-session captures.

The run receipt records the collector version, file hashes and startup settings. GitHub provenance and TDX measurements provide the environment checks; the [validation record](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/) identifies tested configurations.

TgWitness signs the observations it collects; Telegram and message authors do not issue these signatures. In a local workspace, material created before the first independent checkpoint still depends on the collector and its key holder. Coverage records describe the selected scope and collection outcomes, while verified external timestamps anchor the committed archive or journal boundary in time.

## پیوست‌ها

فایل‌ها در پوشه media/ با استفاده از SHA-256 آدرس‌دهی می‌شوند. یک رویداد media.saved یک هش و طول بایت را به یک رویداد پیام خاص پیوند می‌دهد. نام‌های خام فایل‌ها متادیتا هستند و هرگز مسیرهای محلی نیستند. بایت‌های رسانه به‌صورت ناهمزمان دانلود می‌شوند، بنابراین حذف فوری ممکن است از ضبط آن‌ها جلوگیری کند. موارد غیرفعال‌سازی جمع‌آوری، فایل‌های بزرگ/با اندازه نامشخص، خطاهای دانلود و دانلودهای قطع‌شده به‌عنوان نتایج قابل مشاهده هستند. از کار افتادن یک فرآیند می‌تواند فایل‌های ناقص و ارجاع‌نشده‌ای را باقی بگذارد؛ این فایل‌ها در خروجی‌ها گنجانده نمی‌شوند.

خروجی‌گیرنده ZIP، رسانه‌های ذخیره‌شده را با نام‌هایشان تطبیق می‌دهد. خروجی‌های JSONL، CSV و HTML امضاهای رویدادها را تأیید می‌کنند اما بایت‌های رسانه را منتقل نمی‌کنند. گزارش‌های مشتق شده صرفاً برای سهولت هستند؛ فایل events.jsonl، نمایش معتبر رویدادها است.

خروجی کامل چت، پیوست‌ها را در تنظیمات پیوست فضای کاری، در پوشه media/ ذخیره می‌کند که با نام SHA-256 نام‌گذاری شده‌اند. هر رکورد پیام در chat.json، فایل خود را (`file`، `file_sha256`) یا دلیل عدم وجود آن را (`file_status`)، به همراه آنچه خواننده در اطراف متن دیده است، ثبت می‌کند: لینک‌های پشت متن، منبع فوروارد، دکمه‌های ربات، امضا، بازدیدها و تایمر حذف خودکار. `verify.py` بررسی می‌کند که هر فایل نام‌گذاری‌شده در منیفست امضا‌شده زیر آن هش وجود داشته باشد.

## جمع‌آوری پایدار و رسیدهای فرایند (۰.۲)

یک جاب رسانه و رویداد پیام آن در یک تراکنش ثبت می‌شوند. این جاب، توصیف‌کننده اصلی پیام تلگرام (TL) را ذخیره می‌کند؛ مشاهده امضا شده، سیاست‌های SHA-256، حساب کاربری و اندازه آن را پیوند می‌دهد. بازیابی، پیش از دانلود، این پیوند را تأیید می‌کند. این جاب هرگز پیام فعلی را فراخوانی نمی‌کند و بی‌صدا یک پیوست جدیدتر را جایگزین آن می‌کند. جاب‌های متوقف‌شده دوباره امتحان می‌شوند، در حالی که شکست دائمی یک نتیجه صریح باقی می‌ماند.

Each workspace has its own journal and signing identity. A process.started event includes a run ID, local clocks, dependency versions, source-file hashes, initial account/scope, and capture settings. Heartbeats include the run ID, monotonic time, and queue state. The run receipt can also be downloaded as a separately signed statement. For verification of the execution environment, pair it with the GitHub attestation or TDX checks described in [Verification scope](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#verification-scope).

Automatic checkpoints are retained locally on startup, every five minutes while observing (**Parameters → Signed checkpoint every**), and on orderly stop. Startup verification and export compare the journal against the latest retained local checkpoint. This can detect a database rollback when the checkpoint survives. Independent retention keeps that reference available outside the workspace; a verified external timestamp additionally anchors it in time.

پس از راه‌اندازی مجدد، موقعیت به‌روزرسانی ذخیره‌شده تلگرام از سر گرفته می‌شود (`catch_up_from` در `observation.started`) و به‌روزرسانی‌های از دست رفته درخواست می‌شوند. یک بازبینی دوره‌ای، `message.recovered` را برای پیام‌های از دست رفته و `message.missing_on_recheck` را زمانی که تلگرام دیگر یک پیام ذخیره‌شده را بازنمی‌گرداند، ثبت می‌کند؛ مورد دوم یک اطلاعیه حذف نیست و نه نام حذف‌کننده و نه زمان را مشخص نمی‌کند.

### نسخه‌برداری و بازیابی خارج از محل (S3)

نسخهٔ خارج از محل (Exports، به‌صورت پیش‌فرض غیرفعال) بخش‌های مجله، فایل‌های نگهداری‌شده، نقاط کنترل با مهر زمانی و خروجی‌های چت تکمیل‌شده را به ذخیره‌سازی سازگار با S3 بارگذاری می‌کند، رمزگذاری‌شده با نسخهٔ خارج از محل (Exports، به طور پیش‌فرض غیرفعال) بخش‌های دفترچه، فایل‌های نگهداری‌شده، نقاط کنترل را به همراه مهرهای زمانی‌شان و خروجی‌های چت تکمیل‌شده را در یک فضای ذخیره‌سازی سازگار با S3 بارگذاری می‌کند، که پیش از بارگذاری با کلید نگه‌داری‌شده در گاوصندوق فضای کاری با استفاده از رمزگذاری 256-GCM AES رمزگذاری می‌شود؛ نگهداری Object Lock در صورتی اعمال می‌شود که باکت از آن پشتیبانی کند. بدون کلید دانلودشده، این نسخه قابل خواندن نیست. با `python -m tgwitness.replica restore --key-file KEY.json --out DIR` بازیابی و تأیید کنید.

بازیابی به یک دایرکتوری معمولی و خالی نیاز دارد. فایل‌های دانلود شده و اشیاء رمزگشایی شده تا زمان تأیید کامل دفترچه یادداشت و هر نقطه کنترل نگهداری‌شده، در حافظه موقت خصوصی باقی می‌مانند. مسیرهای شیء ناامن، بازه‌های بخش ناسازگار و دفترچه‌های یادداشت کوتاه‌تر از یک نقطه کنترل رد می‌شوند؛ اعتبارسنجی ناموفق، هیچ‌یک از فایل‌های بازیابی‌شده را منتشر نمی‌کند. تأییدهای نگهداری، حالت و تاریخ Object Lock بازگشتی را با مهلت ارسال‌شده هنگام بارگذاری (با تلرانس گرد کردن یک ثانیه‌ای) مقایسه می‌کنند. مهلت منقضی‌شده، نامعتبر یا کوتاه‌تر از حد مجاز، تأییدشده محسوب نمی‌شود. وضعیت، شیء نمونه‌برداری‌شده‌ای را گزارش می‌دهد که نگهداری آن برای آن بارگذاری خاص خوانده شده است.

نبود یا خرابی رسانه محلی به‌عنوان خطای مرحله گزارش می‌شود و مکان نمای رسانه را قبل از آن نگه می‌دارد، تا فایل در مرحله بعدی دوباره امتحان شود؛ فایل‌ها، نقاط کنترل و خروجی‌های بعد از آن همچنان کپی می‌شوند. عملیات بازیابی، تمام ارجاعات به رسانه‌های نگهداری‌شده را با هش‌های رمزگشایی‌شده و اندازه‌های ثبت‌شده مطابقت می‌دهد. بخش‌های مجله‌ای یکسان و همپوشان از بارگذاری‌های قطع‌شده یکپارچه‌سازی (deduplication) می‌شوند؛ همپوشانی‌های متضاد رد می‌شوند. نقاط کنترل ایجادشده در حین بارگذاری، تا زمانی که سوابق مجله‌ای مربوط به آن‌ها کپی نشده‌اند، به تعویق می‌افتند، بنابراین یک چرخه کامل‌شده، هیچ نقطه‌کنترلی را جلوتر از مجله‌اش منتشر نمی‌کند.

### اسنپ‌شات‌های خروجی استریم

صادرات جریانی از یک اسنپ‌شات خواندن پایدار SQLite استفاده می‌کند. ممکن است سر آن هنگام تکمیل دانلود، قدیمی‌تر از ژورنال زندهٔ فعلی باشد. یک نقطه‌کنترل که پس از آن اسنپ‌شات ایجاد می‌شود، می‌تواند به درستی گزارش دهد که آرشیو کوتاه‌تر است؛ آن را با یک نقطه‌کنترل در یا قبل از پیش‌وند صادر شده مقایسه کنید، نه یک نقطه‌کنترل دلخواه بعدی.

## آماده‌سازی RFC 3161 و تأیید پاسخ (۰.۲)

حالت مدرک (به طور پیش‌فرض غیرفعال) تنها هش SHA-256 هر نقطه کنترل امضا شده را از طریق مسیر فضای کاری و هرگز از طریق MTProxy، به مراجع RFC 3161 و تقویم‌های OpenTimestamps فهرست‌شده ارسال می‌کند. پاسخ‌ها در `checkpoints/anchors/` نگهداری، صادر و توسط `verify.py` بررسی می‌شوند (`--tsa-ca` امضای TSA را بررسی می‌کند؛ اثبات‌های OpenTimestamps را با `ots upgrade` و `ots verify` تأیید کنید).

پنل یک آرشیو درخواست آماده می‌کند که حاوی بایت‌های کانونیکال checkpoint.json، یک اثر انگشت پیام SHA-256 و یک نانس تصادفی در timestamp.tsq، چک‌سام‌ها و دستورالعمل‌ها است. هیچ درخواست شبکه‌ای انجام نمی‌شود. آماده‌سازی یک مهر زمانی معتبر نیست.

`python -m tgwitness.anchor verify` دو بار ts را در OpenSSL فراخوانی می‌کند: یک بار برای بررسی بایت‌های نقطه‌کنترل و یک بار دیگر برای بررسی درخواست اصلی. یک فایل CA مورد اعتماد به صراحت مورد نیاز است؛ گواهی‌نامه‌های ضمیمه‌شده به طور خودکار مورد اعتماد قرار نمی‌گیرند. بررسی درخواست در CLI اختیاری است، بنابراین برای بررسی نانسی (nonce) باید --request را نگه دارید و ارائه دهید. نتیجه بیان می‌کند که آیا بررسی شده است یا خیر. امضای نقطه کنترل جمع‌آورنده و دفترچه همچنان باید به طور جداگانه با اثر انگشت جمع‌آورنده مورد اعتماد، تأیید شوند.

فرآیند تأیید، امضای پاسخ، بایت‌های نقطه کنترل و در صورت ارائه، درخواست اصلی را تحت اعتماد CA مشخص‌شده بررسی می‌کند. بررسی‌های لغو و اعتبارسنجی بایگانی بلندمدت پس از انقضای گواهی‌نامه، خارج از محدوده اعتبارسنج فعلی است. [رویه](https://phishdestroy.github.io/TgWitness/fa/docs/reference/timestamp/) و [نتایج اعتبارسنجی](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/) را مشاهده کنید.

## سوابق اختیاری در حالت شواهد: دستگاه‌های drand و Telegram

دو رکورد دیگر می‌توانند روی همان پاس‌های مهر و زمان اجرا شوند. هر دو به‌طور پیش‌فرض غیرفعال هستند و تنها زمانی که حالت شواهد روشن است، فعال می‌شوند: اضافی‌ها → شواهد و پشتیبان‌ها → **شاهدان بیشتر · اختیاری**، یا `"drand": true` و `"devices": true` در `POST /api/evidence`یکی از آن‌ها مانع دیگری یا مهرهای زمانی نمی‌شود؛ پنل آخرین نتیجه هر یک را زیر فرم نشان می‌دهد.

**drand** (`beacon.drand` ). هر بار عبور، جدیدترین دور از drand quicknet، یعنی تصادفی‌سازی عمومی League of Entropy (هر دور ۳ ثانیه)، را در مجله ثبت می‌کند: `chain` ، `round` ، `randomness` ، `signature` ، `round_time` و `relay` که پاسخ داده است. یک دور تأییدشده و غیرقابل‌پیش‌بینی، یک مرجع زمانی پایین‌تر برای محتوای پیوندداده‌شده با هش بعدی فراهم می‌کند. یک مهر زمانی تأییدشده در یک نقطه کنترل بعدی، یک مرجع زمانی بالا را فراهم می‌کند. این بررسی‌ها، محتوای پیوندداده‌شده را محدود می‌کنند؛ پوشش جمع‌آوری به طور جداگانه ارزیابی می‌شود. گردآورنده ابتدا از `drand.cloudflare.com` می‌پرسد، سپس از رله‌های Protocol Labs، از طریق مسیر فضای کاری، هر بار یک درخواست.

`verify.py` بررسی می‌کند که هر تصادفی بودن، SHA-256 امضای آن است و زمان دور صحیح است، و دورها، طولانی‌ترین بازه بدون یک دور و اینکه ساعت جمع‌آورنده چقدر از drand عقب بوده را گزارش می‌دهد. این امضای BLS را بررسی نمی‌کند. `--check-drand` دورها را با یک رله Cloudflare و یک رله Protocol Labs مقایسه می‌کند، همگی آن‌ها یا یک نمونه تصادفی ۱۰۰ تایی در یک ژورنال طولانی؛ دوری که متفاوت باشد، اعتبارسنجی را رد می‌کند.

**دستگاه‌های تلگرام** (`account.devices`). هر بار عبور، جلسات حساب را با `account.getAuthorizations`، فهرستی که تلگرام در تنظیمات → دستگاه‌ها نشان می‌دهد را می‌خواند و ثبت می‌کند: در صورت تغییر از بار قبلی، به‌طور کامل، با `added` و `removed` هش‌های جلسه، در غیر این صورت فقط شمارش و SHA-256 آن. مدل دستگاه، پلتفرم، برنامه و نسخه، زمان ایجاد و آخرین فعالیت، کشور و منطقه حفظ می‌شوند؛ آدرس‌های IP حفظ نمی‌شوند، زیرا خروجی‌های شواهد از کنترل شما خارج می‌شوند. سشن خود گردآورنده همیشه فعال است، بنابراین فقط فعالیت سشن‌های دیگر به عنوان تغییر در نظر گرفته می‌شود. `verify.py` گزارش می‌دهد که لیست هر چند وقت یک‌بار ثبت شده و هر جلسه جدید و خاتمه‌یافته. این لیست فقط زمانی خوانده می‌شود که نظارت در حال اجرا باشد.

آنها چه چیزی را نشان نمی‌دهند: drand چیزی بیش از ترتیب سوابق در برابر زمان عمومی را اثبات نمی‌کند، و فهرست دستگاه‌ها بیانیهٔ Telegram است که از طریق گردآورنده صادر شده و مانند هر سابقهٔ دیگری توسط گردآورنده امضا شده است.

**لاگ Cloudflare Gateway** (`cloudflare.gateway_dns`). برای سروری که از طریق Cloudflare Gateway ([DNS Gateway](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)) حل‌نشانی می‌کند، هر بار کپی، آنچه را که Gateway از زمان کپی قبلی ثبت کرده است، کپی می‌کند: یک رکورد برای هر بازه زمانی حداکثر سه ساعته با `from`, `until`، سرور `location_id`، سرور `address` زمانی که یکی تنظیم شده باشد، و `queries` به عنوان `[at, name, type, rcode, decision, colo]`، همچنین زمانی که هیچ‌کدام وجود نداشته است. آن را در زیر **گزارش‌گیر Cloudflare Gateway** تنظیم کنید: حساب کاربری، مکان، آدرس اختیاری و یک توکن فقط-خواندنی (خواندن تحلیل‌های حساب کاربری؛ خواندن PII اعتماد صفر برای حفظ یک آدرس از یک مکان مشترک). این پنل قبل از ذخیره، آنها را با یک درخواست بررسی می‌کند؛ توکن رمزگذاری‌شده باقی می‌ماند و هرگز وارد گزارش‌ها نمی‌شود. `verify.py` فهرست پنجره‌ها، نام‌های بیشترین جستجو و هر زمانی که هیچ کپی‌ای پوشش نمی‌دهد را فهرست می‌کند؛ رکوردی که تعدادش با پرس‌وجوهایش مطابقت ندارد، ناموفق است. پنجره‌ای که در یک ثانیه بیش از یک صفحه از پرس‌وجوها را در خود جای دهد، آن صفحه را نگه می‌دارد و می‌گوید بقیه مفقود است. کپی پاسخ کلودفلر از طریق گردآورنده، که توسط گردآورنده امضا شده است؛ ظرف ۲۴ ساعت هر کسی که توکن فقط-خواندن داشته باشد می‌تواند آن را با کلودفلر مقایسه کند.
