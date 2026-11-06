# امنیت و مدیریت داده‌ها

Canonical page: https://phishdestroy.github.io/TgWitness/fa/docs/reference/security/

مدل تهدید، مدل دسترسی، اسرار در حالت استراحت، در معرض دید شبکه، وارد کردن جلسات و نحوه گزارش آسیب‌پذیری.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [مستندسازی](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/fa/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

This page describes access, storage and network protection in a local or server workspace. For collection on a GitHub runner or in an Intel TDX confidential VM, see the [verification modes](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#verification-scope), which add checks of the collection environment. Account connections, notifications, timestamps, off-site copies and witnesses have their own routing settings.

| حوزه | به طور خلاصه |
| --- | --- |
| دسترسی | کلید ادمین به‌علاوه دسترسی محدودشده به حساب‌ها/چت‌ها، هفت مجوز و جلسات قابل‌ابطال؛ به‌صورت پیش‌فرض localhost |
| رازهای در آرامش | تنظیمات جلسه، جفت API، کلید امضا و پروکسی با Fernet رمزگذاری می‌شوند. |
| پیام‌ها و رسانه‌ها | ذخیره بدون رمزگذاری: از رمزگذاری دیسک و مجوزهای سخت‌گیرانه استفاده کنید |
| یکپارچگی | زنجیره هش SHA-256 و امضای Ed25519 بر روی هر رکورد |
| مرز اعتماد محلی | The host administrator controls the workspace and its signing key; independent checkpoints retain an earlier journal boundary |

برای گزارش‌های آسیب‌پذیری، به [سیاست امنیتی](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md) مراجعه کنید.

**On this page**

- [Access model](https://phishdestroy.github.io/TgWitness/fa/docs/reference/security/#access-model)
- [Panel content and exports](https://phishdestroy.github.io/TgWitness/fa/docs/reference/security/#panel-content-and-exports)
- [Secrets at rest](https://phishdestroy.github.io/TgWitness/fa/docs/reference/security/#secrets-at-rest)
- [Proxies and network routes](https://phishdestroy.github.io/TgWitness/fa/docs/reference/security/#proxies-and-network-routes)
- [Sign-in and session imports](https://phishdestroy.github.io/TgWitness/fa/docs/reference/security/#sign-in-and-session-imports)
- [Logs and transport](https://phishdestroy.github.io/TgWitness/fa/docs/reference/security/#logs-and-transport)
- [Integrity limits](https://phishdestroy.github.io/TgWitness/fa/docs/reference/security/#integrity-limits)
- [If you suspect a problem](https://phishdestroy.github.io/TgWitness/fa/docs/reference/security/#if-you-suspect-a-problem)

## مدل دسترسی

توکن پنل اصلی کنترل کامل را اعطا می‌کند. سایر افراد می‌توانند [دسترسی محدود](https://phishdestroy.github.io/TgWitness/fa/docs/reference/access/) خود را دریافت کنند: فضاهای کاری و چت‌های منتخب، مجوزها، انقضا، محدودیت‌های IP، محدودیت‌های ورود و جلسات قابل لغو. یک دسترسی محدود به چت نمی‌تواند عملیات کل فضا را انجام دهد حتی اگر مجوز آن تیک خورده باشد. محیط‌های کاری یک فرآیند را به اشتراک می‌گذارند و داده‌ها را از مدیر میزبان ایزوله نمی‌کنند.

پنل به‌طور پیش‌فرض روی localhost گوش می‌دهد. ورود به سیستم از طریق مرورگر، یک توکن دسترسی را با یک اعتبارنامه جلسه (session credential) مبادله می‌کند؛ مرورگر آن را به‌عنوان یک توکن حمل‌کننده (bearer token) ارسال می‌کند. این توکن در sessionStorage نگهداری می‌شود، نه در یک کوکی احراز هویت. قفل کردن/خروج (Lock/sign-out) جلسه مرورگر را پاک می‌کند. بستن مرورگر یا پایان دادن به یک جلسه، جمع‌آوری داده‌ها را متوقف نمی‌کند.

توکن‌های صادر شده و اعتبارنامه‌های جلسه به صورت هش در گاوصندوق رمزگذاری شده نگهداری می‌شوند. ابطال، جلسات مرتبط را پایان می‌دهد؛ تغییرات مجوز بر درخواست‌های بعدی تأثیر می‌گذارد. فایل‌های دانلود شده قابل بازیابی نیستند. مدیر می‌تواند جلسات مرورگر خود را نیز محدود کند، اما اسکریپت‌هایی که مستقیماً از توکن پنل اصلی استفاده می‌کنند، دسترسی کامل خود را حفظ کرده و از آن محدودیت‌های جلسه مرورگر عبور می‌کنند.

احراز هویت ناموفق بر اساس آدرس کلاینت محدود شده است. محدودیت‌های IP بر اساس آدرسی اعمال می‌شوند که توسط برنامه دیده می‌شود؛ پیش از اتکا به آن، عملکرد پروکسی معکوس را بررسی کنید. اعتبارنامه‌های Witness همچنان جداگانه و فقط-خواندنی برای نقاط کنترل/وضعیت سلامت باقی می‌مانند.

### دسترسی دمو

`/api/demo-access` یک بوت‌استرپ عمدتا غیرمعتبر برای یک دمو مصنوعی، ایزوله و صریحاً راه‌اندازی‌شده است. این قابلیت یک فرآیند جداگانه با چرخه عمر محدود صادر می‌کند، هرگز توکن پنل واقعی یا بازنویسی TGWITNESS_TOKEN را صادر نمی‌کند. صدور و استفاده از آن نیازمند یک همتا و میزبان لوپ‌بک، بدون سربرگ‌های فوروارد شده و بدون درخواست فرا-منشأ (cross-origin) است. فضاهای کاری اضافی یا یک جلسه مجاز، این مسیر را غیرفعال می‌کنند. فضاهای کاری زنده هرگز این قابلیت را صادر نمی‌کنند. این دمو نمی‌تواند حساب‌ها را به هم متصل کند یا تنظیمات جمع‌آوری را تغییر دهد.

## محتوای پنل و خروجی‌ها

این پنل از هیچ فونت خارجی، ابزار تحلیل، منابع CDN یا رسانه‌های خارجی جاسازی‌شده استفاده نمی‌کند. متن استخراج‌شده از تلگرام به صورت متن درج می‌شود، نه HTML. فایل‌های پیوست دانلودشده به صورت پیوست‌های باینری ارائه می‌شوند. خروجی‌های JSONL رشته‌های اصلی را حفظ می‌کنند؛ HTML آن‌ها را فرار می‌کند؛ سلول‌های CSV که می‌توانند به فرمول تبدیل شوند، با یک آپاستروف پیش‌وند می‌شوند.

خروجی‌ها شامل اسرار احراز هویت و امضا نمی‌شوند، اما عمداً شامل متادیتای منبع جمع‌آوری‌شده، شناسه‌ها و احتمالاً محتوای شخصی یا حساس هستند. هش‌های دسترسی تلگرام و ارجاعات فایل‌ها می‌توانند در متادیتای خام منبع وجود داشته باشند.

## رازهای در آرامش

Telegram API credentials, the session and signing key are encrypted with Fernet. For local messages and media, encryption is provided by the host's disk or volume; the workspace stores ordinary files. Exports can use a password-protected AES-256 ZIP, and off-site copies use AES-256-GCM.

The vault key defaults to the protected data directory. Use an external master-key file below to store it separately. On Unix, new private-key files use mode 0600 and new data directories use 0700; on Windows, set the directory ACL for the service account and authorized administrators. Existing directory permissions are retained.

### کلید اصلی خارجی

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode. Disk encryption protects the local message and media files in either mode; see [connection and data protection](https://phishdestroy.github.io/TgWitness/fa/docs/reference/connection/) for setup details.

## پروکسی‌ها و مسیرهای شبکه

پیکربندی پروکسی در گاوصندوق رمزگذاری می‌شود. گذرواژه‌ها و اسرار MTProxy توسط API بازنمی‌گردند یا در سوابق شواهد نوشته نمی‌شوند. هر فضای کاری مسیر تلگرام و [حالت آی‌پی](https://phishdestroy.github.io/TgWitness/fa/docs/reference/connection/#ip-modes) خود را انتخاب می‌کند.

**مخفی کردن آدرس،** پشتیبان‌گیری مستقیم تلگرام را رد می‌کند و برای درخواست‌های HTTP خارجی به یک پروکسی نیاز دارد. حالت پشتیبان‌گیری صریحاً انتخاب‌شده پس از تأخیر، دسترسی مستقیم به تلگرام را مجاز می‌سازد؛ حالت تونل/VPN مسیرهای مستقیم را مجاز می‌کند. انتخاب حالت تونل، VPN را نصب یا تأیید اعتبار نمی‌کند. این تنظیمات، تمام ترافیک دستگاه، مرورگرها، مدیران بسته یا حل DNS میزبان پروکسی محلی را کنترل نمی‌کنند.

MTProxy فقط ترافیک تلگرام را منتقل می‌کند. درخواست‌های خارجی می‌توانند از یک پروکسی جداگانه SOCKS5/HTTP، مسیر SOCKS5/HTTP فضای کاری، یا یک مسیر مستقیم مجاز استفاده کنند؛ همچنین می‌توان آن‌ها را غیرفعال کرد. این شاهدی مستقل تنظیمات حمل‌ونقل خود را دارد. احراز هویت معمولی CONNECT در پروتکل‌های SOCKS5/HTTP توسط خود این پروتکل‌ها رمزگذاری نمی‌شود. پشتیبانی از رازهای MTProxy جعلی TLS همچنان فراهم نیست.

## ورود و واردسازی جلسات

فایل‌های تبدیل‌شده .tgwitness-session حاوی یک رمز مخفی مجوز متن ساده هستند تا زمانی که در گاوصندوق بارگذاری و ذخیره شوند. CLI آفلاین، اسکیماهای بازبینی‌شده Telethon را می‌پذیرد. پانل واردات علاوه بر این، ورودی‌های Pyrogram SQLite، TData ZIP مدرن تک‌حساب، و JSON مستند را می‌پذیرد. این قابلیت احراز هویت شده، به چهار فایل / ۸ مگابایت محدود است، و بارگذاری‌ها را بدون استخراج آرشیو یا ذخیره فایل‌های اصلی، در حافظه پردازش می‌کند. اطلاعات احراز هویت نرمال‌شده فقط به مرورگر احراز هویت‌شده درخواست‌کننده بازگردانده می‌شوند؛ آنها پس از موفقیت در احراز هویت تلگرام در گاوصندوق رمزگذاری‌شده ذخیره می‌شوند. از فایل‌های اصلی و تبدیل‌شده محافظت کنید و از کپی‌برداری همزمان یک مجوز توسط کلاینت‌ها جلوگیری کنید.

پردازش TData، چک‌سام‌های کانتینر، هش‌های رمزگشایی محلی و طول ساختارها را تأیید می‌کند. رمز عبور محلی دسکتاپ ارائه‌شده به‌طور موقت استفاده می‌شود و ذخیره نمی‌گردد. این پارسر محدود تضمین نمی‌کند که هر نسخه دسکتاپ سازگار است. تصاویر QR به‌صورت محلی تولید می‌شوند، توکن‌های ورود تلگرام با اعتبار محدود را در خود دارند و هرگز به سرویس رندرینگ خارجی ارسال نمی‌شوند. قفل کردن، تغییر فضای کاری، ورود جدید و تغییرات مسیر، تلاش‌های QR در حال انتظار را لغو می‌کنند. بارگذاری مجدد/بستن یک تب ممکن است یک تلاش را تا زمان انقضای آن در حالت انتظار باقی بگذارد. ورود موفق از طریق QR همچنان الزام به پیوند حساب را اعمال می‌کند. بدنه‌های معمولی API همچنان به ۱۶ کیلوبایت محدود هستند؛ مسیر وارداتی احراز شده تا ۱۲ مگابایت JSON رمزگذاری شده را می‌پذیرد و محدودیت فایل رمزگشایی شده کوچکتر را به طور جداگانه اعمال می‌کند.

کدهای ورود و رمزهای احراز هویت دو مرحله‌ای تلگرام ذخیره نمی‌شوند. وضعیت شماره تلفن/کد-هش در حین تأیید اعتبار در حافظه نگهداری می‌شود. جلسات تلگرام دسترسی به حساب کاربری را فراهم می‌کنند؛ هرگز یک پوشه داده، جلسه، توکن، کلید گاوصندوق یا کلید امضای خصوصی را در گیت‌هاب بارگذاری نکنید.

## لاگ‌ها و انتقال

پاسخ اعتبارسنجی پیش‌فرض API جایگزین می‌شود تا مقادیر اعتبارنامه‌ها را بازتاب ندهد. ثبت دسترسی برنامه غیرفعال است. از پیکربندی پروکسی معکوس برای ثبت سربرگ‌های احراز هویت یا بدنه درخواست‌ها خودداری کنید. HTTP توکن‌ها و اطلاعات محرمانه ورود را به صورت متن ساده حمل می‌کند: هرگاه از localhost خارج می‌شوید از HTTPS یا تونل SSH استفاده کنید.

## محدودیت‌های یکپارچگی

Local verification checks record signatures, the hash chain, attachments and the export manifest. The administrator holds the local signing key and can create another signed journal; an independently retained checkpoint detects replacement of the prefix it covers. Keep the key fingerprint and checkpoints with the recipient or an independent witness.

For independently checked collection, choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Their verifiers check workflow provenance or hardware measurements in addition to archive integrity. Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies; the [evidence format](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#verification-scope) describes the checks for each mode.

## اگر به وجود مشکل مشکوک هستید

Preserve the original data directory and use a separate copy for analysis. Report the affected version, operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), keeping account data and credentials private.
