# آنچه آزمایش شده است

Canonical page: https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/

آزمون زنده تلگرام، بررسی‌های خودکار، بررسی‌های مرورگر و آنچه هنوز تأیید نشده است.

## راه‌اندازی زنده Phala Cloud · ۴ نوامبر ۲۰۲۶

`--provider phala --quick-tunnel` در مقابل **واقعی اجرا شد Phala Cloud** (`tdx.small`، منطقه US-WEST-1) با یک کلید API Phala Cloud از یک فضای کاری خالی، ntfy.sh واقعی، GitHub و Intel PCS. کمیّت `df7d860c` (v0.8.1) در CVM نصب شد؛ عملیات deploy، verify و destroy از طریق خط فرمان با اصلاحات زیر اجرا شد. مجموع هزینه هفت CVM حدود ۱.۹ سنت دلار آمریکا بود.

دو استقرار اول پنج تفاوت را از Phala Cloud شبیه‌سازی‌شده پیدا کردند. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) اکنون هر یک را بازتولید می‌کند و بدون اصلاح خود با شکست مواجه می‌شود:

| در Phala Cloud | قبل از رفع مشکل | رفع مشکل |
| --- | --- | --- |
| `compose_file.name` مورد نیاز است | HTTP 422، هیچ چیزی ایجاد نشد | پیکربندی Docker Compose نام CVM را حمل می‌کند |
| مگر اینکه یک مقدار خالی داده شود، Phala اسکریپت پیش از راه‌اندازی خود را به app-compose اندازه‌گیری‌شده اضافه می‌کند (نسخه 0.0.20: ورود به داکر، `docker compose pull`، رمز عبور ریشه، کلیدهای SSH از `user_config`) | `tdx_compose` شکست می‌خورد: کد خارج از پیکربندی منتشرشده Docker Compose | app-compose مقدار `pre_launch_script` را روی `""` تنظیم می‌کند؛ Phala سپس آن را نادیده می‌گیرد |
| بدون `image`، Phala، `dstack-dev-0.5.12`، نسخه توسعه را با دسترسی SSH فعال‌شده انتخاب می‌کند. | `server_state` شکست می‌خورد. تنها رکورد گواهی سخت‌افزاری در این تصویر تأیید شد؛ فقط رکورد ارائه‌دهنده و `tdx_os` آن را نشان می‌دهند. | راه‌اندازی، ساخت نسخه تولید (production build) از آخرین نسخه Phala، `dstack-0.5.12` را درخواست می‌کند. |
| با غیرفعال بودن دروازه dstack، جزئیات CVM هرگز مقدار `instance_id` را دریافت نمی‌کند. | استقرار ۳۰ دقیقه منتظر می‌ماند و با شکست مواجه می‌شود | شناسه نمونه از وضعیت CVM خوانده می‌شود. |
| راه‌اندازی مجدد، توقف و راه‌اندازی، عملیات CVM هستند، نه بازنگری‌های برنامه. | `provider_actions` راه‌اندازی مجددها را فهرست نکرد. | عملیات خواندن نیز در نظر گرفته می‌شوند |

سومین استقرار:

- CVM با `dstack-0.5.12` و دسترسی SSH غیرفعال اجرا شد. کالکتور حدود ۱.۵ دقیقه پس از ایجاد، آدرس امضا شده خود را ارسال کرد. سپس Deploy، `tdx_binding` و `tdx_quote` (Intel TCB UpToDate، رکورد گواهی سخت‌افزار v4، FMSPC `20a06f000000`، در حالت اشکال‌زدایی نیست، قابل مهاجرت نیست، پشتیبانی از داده‌های تأیید رمزنگاری استخراج‌شده از اینتل)، `tdx_compose_hash`، `tdx_compose` (بایت به بایت) و `tdx_identity` (کلیدهای KMS).
- پنل در آدرس trycloudflare.com خود، بدون توکن یا با توکن اشتباه، پاسخ ۴۰۱ و با توکن پنل، پاسخ ۲۰۰ داد.
- `verify` با `--source` که روی آرشیو گیت‌هابِ کامیت تنظیم شده بود و اثر انگشت به‌صورت جداگانه ارسال شد: سرور، `server_state`، فایروال (بدون گیت‌وی، بدون نقطه پایانی عمومی)، لاگ ارائه‌دهنده، بیانیه، اثر انگشت، هش منبع، بوت و پنج بررسی `tdx_*` با موفقیت انجام شد. Cloudflare و `tdx_os` در دسترس نبودند، بنابراین نتیجه ناقص بود.
- دو بار راه‌اندازی مجدد از طریق API فالا: هر بار که CVM با همان کلید گردآورنده، یک آدرس امضا شده جدید و پاسخ ۵۳۰ از آدرس قدیمی، در کمتر از دو دقیقه بازگشت. `verify` بوت جدید و هر دو راه‌اندازی مجدد را به عنوان REVIEW گزارش کرد. با `--evidence`، امضاهای ژورنال و سه راه‌اندازی تأیید شد، که هر کدام دارای رکورد گواهی سخت‌افزاری Intel TDX مخصوص به خود از همان CVM بودند.
- `destroy` فقط آن CVM را حذف کرد. سپس فضای کاری خالی شد و آدرس پنل دیگر پاسخی نداد.
- بررسی قیمت ویزارد پنل، `tdx.small` را با نرخ ۰.۰۵۸ دلار در ساعت خواند. یک کلید اشتباه، پیام ساده‌ی «کلید API پذیرفته نشد» را دریافت کرد.

دو یافته دیگر که بعداً اصلاح شدند:

- بدون کلید آدرس، `verify` جدیدترین پست صحیح در موضوع آدرس را دنبال کرد، که در پیکربندی منتشر شده Docker Compose چاپ شده است. یک پست جعل‌شده آن را به میزبانی که وجود ندارد فرستاد، و `statement` شکست خورد: یک جعل‌کننده نمی‌توانست خود را به جای گردآورنده جا بزند، اما می‌توانست مسدود کند تأیید شخص ثالث را برای حداکثر ۱۲ ساعت با یک مهر زمانی آینده جعل‌شده انجام می‌دهد. اکنون گردآورنده همچنین آدرس خود را با کلید خودش امضا می‌کند، `verify` فقط چنین پست‌هایی را زمانی که گردآورنده آنها را ارسال می‌کند می‌پذیرد، و پست‌ها بر اساس زمان دریافت ntfy.sh مرتب می‌شوند. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) پست‌های جعل‌شده را مجدداً پخش می‌کند. یک CVM این را فقط از کامیتی که حاوی آن است اجرا می‌کند، بنابراین کلکرکر این اجرا هنوز آدرس خود را امضا نکرده است و `verify` همین را اعلام کرد.
- `tdx_os` بدون `dstack-mr` که نسخه فعلی آن به جای `measure --json` که در مستندات نام برده شده، از `measure-os` استفاده می‌کند، قادر به اجرا نبود. اکنون اعتبارسنج، MRTD و RTMR0-2 را خود از روی ایمیج منتشر شده و شکل VM، شامل جداول ACPI، محاسبه می‌کند.

چهارمین استقرار، با این موارد:

- Deploy یک‌بار `dstack-0.5.12` منتشرشده را دانلود کرد، آن را با هش تصویر سیستم‌عامل که CVM گزارش کرده بود مطابقت داد، و `tdx_os` تأیید شد: MRTD، RTMR0، RTMR1 و RTMR2 با مقادیر محاسبه‌شده برای QEMU یکسان بودند. 8.2.2، 1 vCPU و 2 GiB. همان محاسبه، مقدار متفاوتی برای RTMR0 را برای ادعای 4 GiB، 2 vCPU، QEMU 9.2.1 یا یک کارت شبکه دوم، نشان داد و برای کرنل، فریمور یا خط فرمان تغییر یافته و برای ایمیج توسعه، ناموفق بود.
- `verify` هر ۱۶ بررسی خود را، از جمله کانکتور تونل سریع، با موفقیت پشت سر گذاشت، بنابراین نتیجه PASS بود. این گواهی HTML و PDF را نوشت که با امضاها و مهرهای زمانی، با یک مهر زمانی معتبر eIDAS از واحد زمان‌بندی دولت بلژیک TSU 202301 (وضعیت تأیید شده در لیست مورد اعتماد بلژیک)، یک مهر زمانی FreeTSA و امضای راستی‌آزما، مهر و موم دیجیتال شده بود؛ `check-report` همه آنها و امضای PDF را تأیید کرد.
- پس از راه‌اندازی مجدد، `verify --evidence` دو راه‌اندازی را تأیید کرد، هر یک همراه با گواهی سخت‌افزاری تولیدشده درون CVM و هر یک از `dstack-0.5.12` منتشرشده بوت شده بود؛ راه‌اندازی مجدد و بوت جدید تحت بررسی بودند.
- `destroy` فضای کاری را خالی رها کرد.

پنجمین استقرار، کولکتور را از commit `53a0f7e9` اجرا کرد که شامل همه موارد فوق است:

- کلکسیونر آدرس امضا شده با کلید خود را، در کنار پست HMAC اپراتور، منتشر کرد. سپس دو پست جعلی به موضوع اضافه شدند: یکی با HMAC صفر شده و دیگری امضا شده با یک کلید Ed25519 دیگر، که هر دو مدعی زمانی در سال ۲۰۹۶ بودند. `verify` آدرس امضا شده توسط کلید گردآورنده را برداشت و از هر ۱۶ بررسی سربلند بیرون آمد؛ مهر بار دیگر حاوی مهر زمانی معتبر بلژیکی، مهر زمانی FreeTSA و امضای راستی‌آزما بود، و `check-report` آنها را تأیید کرد.
- پس از یک راه‌اندازی مجدد، جمع‌آورنده آدرس جدید امضا شده را ارسال کرد: `verify` آن را بلافاصله پیدا کرد، اپراتور **آدرس فعلی را پیدا کرد** ۲۷ ثانیه بعد از ارسال HMAC، و هر دو ارسال‌های جعل شده را نادیده گرفتند. `verify --evidence` دو راه‌اندازی را که از `dstack-0.5.12` بوت شده بودند تأیید کرد.
- ابزار استقرار چاپ کرد که فالا از CVM چه مبلغی، شامل هزینه دیسک، دریافت می‌کند: $0.06078 در ساعت.

ویزارد پنل دو بار روی Phala Cloud اجرا شد، یک بار از طریق API وظیفه آن و یک بار از طریق مرورگر با یک کرومیم واقعی: بررسی قیمت، ایجاد با commit تحت **Advanced**، گذراندن هر شش بررسی احراز هویت، لیست سرور که قیمت صورتحساب شده (۴۴.۳۷ دلار در ماه) را نشان می‌دهد، **Find آدرس فعلی**، دانلود پیکربندی اندازه‌گیری‌شده Docker Compose و حذف آن. مرورگر هیچ خطای صفحه‌ای را مشاهده نکرد. هر بار پس از آن، فضای کاری خالی بود.

پوشش داده نشده: یک دامنه کلودفلر روی فالا، یک حساب تلگرام روی CVM، و ایمیج `dstack-0.6.1`. قیمت ویزارد قبل از ایجاد فقط قیمت محاسباتی فالا است، زیرا API آن فقط قیمت دیسک را برای یک CVM موجود نام می‌برد؛ لیست سرورها قیمت صورتحساب شده پس از ایجاد را نشان می‌دهد.

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

## صلاحیت‌های باقی‌مانده

ژورنال زندهٔ نگهداری‌شده، ثبت واقعی جمع‌آوری، ویرایش‌ها، اعلان‌های حذف، پیوست‌ها، بازبینی‌های مجدد و مدیریت محدودیت نرخ را فراهم می‌کند. این ابزار سوابق جامع تحویل، ماتریس کنترل‌شده دیده‌بانی نقش‌ها، واکنش‌دهندگان، انتظار سیل طولانی‌مدت (FloodWait)، مسدودسازی حساب‌ها و بازیابی پس از وقفه شبکه/فرآیند را ثبت نمی‌کند. صدور توکن QR از تأیید QR موبایلی تکمیل‌شده مستقل است.

ساخت/اجرای Docker، نصب لینوکس/macOS، تحمل بار بالا و مداوم، بازبینی امنیتی مستقل، پاسخ واقعی و مستقل به TSA، اعتبارسنجی لغو/آرشیو گواهی و گواهی‌نامه قانونی (forensic) خارج از محدوده صلاحیت‌های ثبت‌شده باقی می‌مانند. وضعیت MTProto ذخیره شده و قابلیت جبران (catch-up) پیاده‌سازی شده‌اند؛ اما بازپخش اتمی پایدار (atomic durable replay) هنوز پیاده‌سازی نشده است. جمع‌آوری لاگ‌های ادمین، لیست‌های ری‌اکتور اضافی و پینگ کوتاه‌مدت اولویت‌دار همچنان ویژگی‌های جداگانه‌ای هستند. برای مشاهدهٔ ماتریس صلاحیت کنترل‌شده، به [پذیرش زنده](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) مراجعه کنید.

رسیدهای محلی و اسکرین‌شات‌های دقیق در مسیر test-results/ (توسط Git نادیده گرفته شده) قرار دارند. اسکرین‌شات عمومی در docs/assets/ فقط حاوی داده‌های نمایشی خیالی است.
