# استقرار با تضمین بالا

Canonical page: https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/

یک سرور مهر و موم‌شدهٔ ۲۴ ساعته و ۷ روز هفته در Hetzner یا Phala Cloud، DNS Gateway و چک‌هایی که شخص ثالث می‌تواند تکرار کند.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [مستندسازی](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/fa/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

High-assurance deployment adds independent checks of the collection environment to archive verification. The reviewer queries deployment and access records held by the cloud provider and Cloudflare, and an Intel TDX deployment adds hardware attestation of the collector's environment.

استفادهٔ معمولی محلی و Docker بدون تغییر است. هیچ چیزی در اینجا اجرا نمی‌شود مگر اینکه با `python -m tgwitness.cloud`، و کالکتور تنها زمانی میزبان خود را می‌خواند که استقرار تنظیم کند. `TGWITNESS_ASSURANCE`.

نمودار جریان · اپراتور → سرور، فایروال بدون قواعد ورودی (API ارائه‌دهنده); اپراتور →  تونل و DNS (API کلودفلر); سرور، فایروال بدون قواعد ورودی →  تونل و DNS (فقط خروجی); سرور، فایروال بدون قواعد ورودی → کلید امضا روی سرور ایجاد شده است; تأییدکننده، توکن‌های فقط-خواندنی → لاگ ارائه‌دهنده و فایروال; تأییدکننده، توکن‌های فقط-خواندنی → آدرس کانکتور تونل و ورودی; تأییدکننده، توکن‌های فقط-خواندنی → بیانیه تضمین امضا شده /api/; تأییدکننده، توکن‌های فقط-خواندنی → فایل فشرده شواهد · اپراتور · تأییدکننده، توکن‌هایفقط-خواندنی · سرور، فایروال بدون قواعدورودی · لاگ ارائه‌دهنده و فایروال · آدرس کانکتور تونل و ورودی · بیانیه تضمین امضا شده/api/ · فایل فشرده شواهد · تونل و DNS · کلید امضا روی سرور ایجادشده است · API ارائه‌دهنده · API کلودفلر · فقط خروجی

**نمودار به صورت متن**

1. اپراتور → سرور، فایروال بدون قواعد ورودی (API ارائه‌دهنده)
2. اپراتور → تونل و DNS (API کلودفلر)
3. سرور، فایروال بدون قواعد ورودی → تونل و DNS (فقط خروجی)
4. سرور، فایروال بدون قواعد ورودی → کلید امضا روی سرور ایجاد شده است
5. تأییدکننده، توکن‌های فقط-خواندنی → لاگ ارائه‌دهنده و فایروال
6. تأییدکننده، توکن‌های فقط-خواندنی → آدرس کانکتور تونل و ورودی
7. تأییدکننده، توکن‌های فقط-خواندنی → بیانیه تضمین امضا شده /api/
8. تأییدکننده، توکن‌های فقط-خواندنی → فایل فشرده شواهد

**On this page**

- [What a verifier can check](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#what-a-verifier-can-check)
- [Providers](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#providers)
- [Confidential VM on Phala Cloud (Intel TDX)](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)
- [Before you start](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#before-you-start)
- [From the panel](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#from-the-panel)
- [Quick tunnel without a domain](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#quick-tunnel-without-a-domain)
- [Deploy](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#deploy)
- [Debug deployment and lock](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#debug-deployment-and-lock)
- [Remove a deployment](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#remove-a-deployment)
- [Any server (self-attested)](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#any-server-self-attested)
- [Verify](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#verify)
- [Report for evidence handover](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#report-for-evidence-handover)
- [Cloudflare as an outside witness](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)
- [Reading the deployment result](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#reading-the-deployment-result)

## آنچه یک راستی‌آزما می‌تواند بررسی کند

| ادعا | چگونه بررسی می‌شود | نگه‌داری‌شده توسط |
| --- | --- | --- |
| سرور در زمان مشخصی از طریق API ارائه‌دهنده ایجاد شد. | شیء سرور و ایجاد آن در لاگ اختصاصی ارائه‌دهنده | ارائه‌دهنده |
| هیچ‌کس از مسیرهای دسترسی ارائه‌دهنده استفاده نکرد | گزارش درخواست‌های کنسول، بازیابی، بازنشانی رمز عبور، بازسازی، ISO، تصاویر، پشتیبان‌ها | ارائه‌دهنده |
| هیچ چیزی نمی‌تواند به آن متصل شود | فایروال ارائه‌دهنده هیچ قاعده ورودی ندارد؛ SSH از اولین راه‌اندازی پنهان می‌شود. | ارائه‌دهنده (فایروال)، میزبان (SSH) |
| به پنل تنها از طریق تونل دسترسی پیدا می‌شود | ورودی تونل تنها به پنل فوروارد می‌شود؛ کانکتور از آدرس سرور اجرا می‌شود | کلودفلر |
| این نرم‌افزار دقیقاً اجرا می‌شود | هَش امضا‌شدهٔ درخت منبع گردآورنده برابر با خروجی یک چک‌آوت از کامیت مستقرشده است. | کالکِتور، بررسی‌شده در برابر گیت |
| کلید امضا روی آن سرور ایجاد شد | کلید بیانیه‌ای را امضا می‌کند که شامل شناسهٔ سرور ارائه‌دهنده و هش cloud-init دریافتی است. | کالکتور، بررسی‌شده در برابر ارائه‌دهنده |
| این مجله متعلق به آن کلید و سرور است | هر فرایند در شواهد آغاز می‌شود ZIP اندازه‌گیری میزبان را برای آن سرور حمل می‌کند | شواهد ZIP |

The collector records SSH state, sessions, login history and boot information in signed process-start and `host.state` records. On an ordinary VM these are local inventory records, which the reviewer compares with the provider's independent records. The Intel TDX deployment below additionally verifies hardware-backed measurements.

## ارائه‌دهندگان

| `--provider` | اطلاعات احراز هویت | دسترسی فقط-خواندن Verifier | لاگ ارائه‌دهنده برای اعتبارسنج | نگه‌داشته‌شده برای |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | خواندن توکن همان پروژه | اقدامات سرور و فایروال | در حالی که منابع وجود دارند |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | توکن دسترسی شخصی فقط-خواندنی | اقدامات دراپلت | در حالی که دراپلت وجود دارد |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` دامنه‌های فقط-خواندنی | رویدادهای حساب، نسخه‌های قوانین فایروال | ۹۰ روز |
| `vultr` | `VULTR_API_KEY` | کاربری با دسترسی خواندن و ... `activity_logs` مجوز | گزارش فعالیت حساب (روش، مسیر، عامل) | ۳۰ روز، با اشتراک گزارش‌های حسابرسی طولانی‌تر |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | تاریخچه رویدادهای CloudTrail | ۹۰ روز |
| `phala` | `PHALA_CLOUD_API_KEY` | یک کلید API از همان فضای کاری | بازنگری‌های برنامه و عملیات CVM: پیکربندی Docker Compose و تغییرات محیط، راه‌اندازی مجدد، ارتقاء سیستم‌عامل | در حالی که برنامه وجود دارد |
| `generic` | هیچ | هیچ | هیچ: **خودگواهی‌شده** | – |

برای هر پرونده از یک پروژه، تیم، حساب یا زیرحساب اختصاصی استفاده کنید: دسترسی فقط-خواندن اعتبارسنج سپس فقط این استقرار را نشان می‌دهد. اعتبارنامه‌ها از `--provider-token-file` یا متغیر بالا، هرگز از خط فرمان. برای AWS، فایل حاوی `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`؛ منطقه است `--location`.

آنچه سوابق هر ارائه‌دهنده نمی‌تواند نشان دهد، در هر گزارش چاپ می‌شود. به طور خلاصه: هتزنر درخواست‌های کنسول را ثبت می‌کند؛ کنسول بازیابی DigitalOcean، Lish/Glish در Linode و کنسول وب Vultr به این صورت ثبت نمی‌شوند، بنابراین روت در اولین بوت قفل می‌شود و ورود به کنسول نیاز به ریست کردن رمز عبور یا تغییر بوت دارد، که این موارد ثبت می‌شوند. Vultr آدرس کنسول را به هر کلیدی که بتواند نمونه را بخواند، بازمی‌گرداند؛ نه رکورد و نه گزارش آن را ذخیره می‌کنند.

## ماشین مجازی محرمانه روی Phala Cloud (Intel TDX)

با `--provider phala` جمع‌کننده در یک ماشین مجازی محرمانه Intel TDX روی [Phala Cloud](https://phala.com/)، که توسط dstack مدیریت می‌شود، اجرا می‌شود. میزبان و کارکنان Phala نمی‌توانند حافظه آن را بخوانند و پردازنده، گواهی‌ای از آنچه ماشین بوت کرده است، امضا می‌کند. اعتبارسنج صرفاً به حرف Phala اکتفا نمی‌کند: `tgwitness.tdx` خودش هر گواهی را، تا ریشه CA Intel SGX پین‌شده، با فهرست‌های لغو اعتبار و داده‌های پلتفرم امضا شده اینتل بررسی می‌کند، و ماشین‌هایی را که قابل اشکال‌زدایی یا مهاجرت هستند، رد می‌کند.

| گزارش ورود | آنچه نشان می‌دهد |
| --- | --- |
| `tdx_binding` | این گواهی، بیانیهٔ امضا شدهٔ گردآورنده و مقدار تصادفی این درخواست را پوشش می‌دهد. |
| `tdx_quote` | اینتل برای تأیید اعتبار ضامن است؛ این اعتبار تنها زمانی اعطا می‌شود که اینتل پلتفرم را به‌روز ارزیابی کند. |
| `tdx_compose_hash` | RTMR3 که از لاگ رویداد dstack بازپخش می‌شود، میزان app-compose را که گردآورنده گزارش می‌کند، اندازه‌گیری می‌کند. |
| `tdx_compose` | آن کامپوز دقیقاً بایت‌به‌بايت همان چیزی است که کد commit مستقر شده می‌سازد: فایل‌های منبع پین‌شده با هَش، هر دو تصویر با دیجست، بدون هیچ کد دیگری |
| `tdx_identity` | تصدیق از طریق اپلیکیشن و نمونهٔ استقرار یافته، با کلیدهای KMS فالا و یک دیسک رمزگذاری‌شده انجام می‌شود. |
| `tdx_os` | MRTD و RTMR0-2 با مقادیری برابر هستند که اعتبارسنج از تصویر سیستم‌عامل dstack که Dstack-TEE منتشر می‌کند، هش تصویر سیستم‌عملی که CVM گزارش می‌دهد و از جدول‌های ACPI که QEMU برای شکل VM می‌سازد، محاسبه می‌کند: فریمور، کرنل، initrd، خط فرمان با هش فایل‌سیستم ریشه، حافظه، vCPUها و دستگاه‌ها. یک تصویر توسعه ناموفق است |

تصویر سیستم‌عامل (حدود ۱۸۰ مگابایت، که ۲۱ مگابایت از آن نگهداری می‌شود) یک‌بار از [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases) به `dstack-images` در کنار رکورد دانلود می‌شود؛ `--tdx-image FOLDER` از یک پوشه دیگر یا یک تصویر بازشده استفاده می‌کند، `--tdx-image none` مقایسه را نادیده می‌گیرد. اندازه‌گیری از `dstack-mr` و بسته Rust از `qemu-acpi` در Dstack-TEE/dstack پیروی می‌کند؛ `tools/check_dstack_image.py` آن را با خروجی ACPI خود QEMU و با یک رکورد گواهی سخت‌افزاری واقعی Phala Cloud مقایسه می‌کند، و `--live` همچنین آن را با تصویر منتشر شده مقایسه می‌کند. `--tdx-measurements` همچنان MRTD و RTMR0-2 را که به صورت JSON ارائه شده‌اند، مقایسه می‌کند.

هر شروعِ کالکتور که در ژورنال ثبت می‌شود، چنین گواهی‌ای را در خود دارد، بنابراین `verify --evidence` هر شروع و تصویر سیستم عاملی را که با آن بوت شده است بررسی می‌کند. بازنگری‌های اپلیکیشن Phala و عملیات‌های CVM به عنوان لاگ ارائه‌دهنده عمل می‌کنند: یک پیکربندی Docker Compose که پس از استقرار تغییر کرده باشد، گزارش خطا می‌دهد و راه‌اندازی‌های مجدد برای بازبینی فهرست می‌شوند.

در پنل، در بخش **Extras** → **Server 24/7** گزینه **«ماشین مجازی محرمانه · Phala Cloud»** را انتخاب کرده و یک کلید API از Phala Cloud را الصاق کنید؛ تونل سریع مانند Hetzner کار می‌کند. از خط فرمان:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` به جای دانلود گواهی‌نامه‌ها و فهرست‌های لغو اعتبار اینتل از خود اینتل، آن‌ها را از یک فایل می‌خواند. Gateway DNS در اینجا در دسترس نیست: Phala فاقد فایروال ارائه‌دهنده برای ترافیک خروجی است.

### گواهی اعتبارسنجی

برای استقرار Phala، `verify --report certificate.md` همچنین گواهی را می‌نویسد: a `certificate.html` خودکفا و یک A4 `certificate.pdf` با نتیجه، زنجیره اعتماد از ریشه اینتل تا کلید گردآورنده، مقایسه‌ای با سرورهای معمولی و با تضمین بالا، اندازه‌گیری‌ها در کنار مقادیر محاسبه شده از تصویر منتشر شده، چه کسی برای هر بخش ضمانت می‌کند، زنجیره گواهی اینتل، هر بررسی، گزارش ارائه‌دهنده، و نحوه تکرار تأیید اعتبار. گزارش JSON سند معتبر باقی می‌ماند؛ صفحات آن را نمایش می‌دهند.

این گزارش با امضاها و مهرهای زمانی به‌صورت دیجیتال در فایل‌های `certificate.seal.json` و `.tsq`/`.tsr` کنار آن مهر و موم شده است:

| Seal | آنچه اضافه می‌کند |
| --- | --- |
| مهر زمانی الکترونیکی معتبر، `http://tsa.belgium.be/connect` | امضای زمانی RFC 3161 بر روی بایت‌های دقیق `certificate.json` از ارائه‌دهنده خدمات اعتماد معتبر دولت فدرال بلژیک (FPS Policy and Support, BOSA). واحد آن به عنوان یک سرویس مهر زمانی معتبر با وضعیت اعطا شده در فهرست مورد اعتماد اتحادیه اروپا برای بلژیک فهرست شده است؛ ریشه (Belgium Root CA6) و موارد موجود در این فهرست، بر اساس فهرستی که در تاریخ ۲۰ اکتبر ۲۰۲۶ منتشر شده است، در `tgwitness/tsa_roots.py` پین شده‌اند. بر اساس مقررات (اتحادیه اروپا) شماره ۹۱۰/۲۰۱۴، ماده ۴۱، چنین مهر زمانی از نظر تاریخ و زمان و همچنین از نظر یکپارچگی داده‌ها در هر یک از کشورهای عضو اتحادیه اروپا معتبر فرض می‌شود. |
| مهر زمانی RFC 3161، FreeTSA | یک نشانگر زمانی دوم و مستقل |
| امضای اعتبارسنج | امضای Ed25519 بر روی گزاره‌ای که SHA-256 و هر زمان‌مهر گزارش را نام می‌برد، با کلید خود راستی‌آزما (`--sign-with FOLDER`، پیش‌فرض `~/.tgwitness/verifier`)؛ PDF دارای امضایی با همان کلید است |

`--timestamp URL` (تکرارپذیر) مراجع دیگر را انتخاب می‌کند، `--timestamp none` هیچ‌کدام را، و `--sign-with
none` مهر را بدون امضا رها می‌کند. `check-report` هش گزارش، امضای راستی‌آزما، هر نشانگر زمانی را به یک ریشه مورد اعتماد و وضعیت معتبر آن، و امضای PDF را بررسی می‌کند. اعتبار قانونی یک مهر زمانی معتبر خارج از اتحادیه اروپا، و کل گزارش، بر عهده دادگاه یا مرجعی است که آن را دریافت می‌کند؛ این مهر نشان می‌دهد که گزارش چه زمانی وجود داشته و تغییر نکرده است.

یک گواهی‌نامه نمی‌تواند یک نقص در ماژول TDX یا میکروکد اینتل، یا دسترسی فیزیکی به گذرگاه حافظه را رد کند. هر کسی که کنترل برنامه در حساب فالا را در دست دارد می‌تواند یک کامپوز دیگر را مستقر کند؛ این کامپوز به عنوان یک بازنگری جدید با هش کامپوز جدید ظاهر می‌شود. میزبان منبع زمان و شبکه ماشین را کنترل می‌کند.

عملیات استقرار، تأیید با `--evidence`، راه‌اندازی مجدد، مقایسه تصویر سیستم‌عامل، گواهی مهر و موم دیجیتال با امضاها و مهرهای زمانی و نابودسازی روی خود Phala Cloud اجرا شده‌اند؛ به اجرای [در تاریخ ۴ نوامبر ۲۰۲۶ و](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026) مراجعه کنید.

## قبل از شروع

1. یک زون Cloudflare، شناسه حساب آن و یک توکن API با قابلیت‌های **Cloudflare Tunnel Edit**، **Zone Read** و **DNS Edit**، که با `--cloudflare-token-file` یا `CLOUDFLARE_API_TOKEN`برای اعتبارسنج: **خواندن تونل کلودفلر**، **خواندن DNS** و، برای سوابق حسابرسی، **خواندن تنظیمات حساب**. بدون دامنه، یک [تونل سریع](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#quick-tunnel-without-a-domain) به هیچ‌کدام از این موارد نیاز ندارد.
2. اطلاعات اعتبار ارائه‌دهنده با دسترسی نوشتن به یک پروژه اختصاصی؛ `lock` از همان استفاده می‌کند:

   - Hetzner: توکن API با مجوز خواندن و نوشتن؛
   - DigitalOcean: توکن دسترسی شخصی با دسترسی نوشتن؛
   - Linode: توکن دسترسی شخصی با `linodes`, `firewall` و `events` دامنه‌های خواندن/نوشتن؛
   - ولتر: کلید API یک حساب اختصاصی یا زیرحساب؛
   - AWS: اعتبارنامه‌های IAM مجاز هستند `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` و `ec2:RevokeSecurityGroupIngress`.
3. کامیتی که باید اجرا شود. یک تگ انتشار یک‌بار به کامیت خود با `git ls-remote`; سرور تنها commit ۴۰ کاراکتری را دریافت می‌کند.

## از پنل

روی کامپیوتر خود، مسیر **Extras → Server 24/7** همان را اجرا می‌کند `deploy` برای Hetzner در سه مرحله: اروپا یا ایالات متحده را انتخاب کنید، یک توکن Hetzner (خواندن و نوشتن) را الصاق کنید، سپس نوع سرور، قیمت ماهانه، آدرس و نسخه‌ای را که پنل با آن توکن پیدا کرده است بررسی کنید. هیچ چیزی قبل از تأیید شما ایجاد نمی‌شود. پنل هر مرحله را به صورت `deploy` گزارش می‌کند، سپس آدرس، توکن پنل و اثر انگشت کلید امضا را نشان می‌دهد. بدون دامنه، سرور یک [تونل سریع](https://phishdestroy.github.io/TgWitness/fa/docs/reference/high-assurance/#quick-tunnel-without-a-domain) دریافت می‌کند؛ **سرورها ← آدرس فعلی را** پس از راه‌اندازی مجدد دوباره بررسی می‌کند. برای یک آدرس ثابت تحت دامنه خود، **گزینه‌های اختیاری · دامنه خود را** باز کرده و یک توکن کلودفلر اضافه کنید (لینک آماده‌شده، گزینه‌های «خواندن منطقه»، «ویرایش DNS» و «ویرایش تونل کلودفلر» را انتخاب می‌کند).

توکن‌ها با هر درخواست از زبانه مرورگر به TgWitness در همان کامپیوتر جابجا می‌شوند و در هیچ‌کجا ذخیره نمی‌شوند؛ رکورد استقرار، cloud-init حذف‌شده، توکن پنل و، برای یک تونل سریع، کلید آدرس در نگهداری می‌شوند `deployments/NAME` داخل دایرکتوری داده. پنل این قابلیت را فقط به مدیر اصلی در یک اتصال لوپ‌بک مستقیم ارائه می‌دهد (`127.0.0.1`، بدون هیچ هدر پروکسی یا تونل)؛ پنلی که از طریق شبکه به آن دسترسی پیدا می‌شود، به جای آن دستورات را نمایش می‌دهد. نسخه به طور پیش‌فرض بر روی تگ انتشار پنل در حال اجرا تنظیم می‌شود که از طریق API گیت‌هاب حل شده است. مکان، نوع سرور و قیمت از API هتزنر دریافت می‌شوند: `cpx22` جایی که ارائه می‌شود، در غیر این صورت ارزان‌ترین نوع x86 با حداقل ۲ گیگابایت حافظه.

## تونل سریع بدون دامنه

`--quick-tunnel` جایگزین می‌کند `--zone`, `--cloudflare-account` و `--panel-host`؛ هیچ حساب یا توکن Cloudflare درگیر نیست:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

روی سرور، cloudflared یک [تونل سریع](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) به پنل باز می‌کند: یک ... تصادفی `https://….trycloudflare.com` آدرسی که هر زمان cloudflared یا سرور راه‌اندازی مجدد شود، تغییر می‌کند. یک سرویس کوچک روی سرور هر آدرس را در یک موضوع تصادفی ntfy.sh ارسال می‌کند، که با کلیدی که فقط در دایرکتوری استقرار موجود است (HMAC-SHA256) امضا شده است (`address-key.txt`)، و هر سه ساعت یک‌بار آن را تکرار می‌کند زیرا ntfy.sh پست‌ها را به مدت ۱۲ ساعت نگه می‌دارد. `deploy` و **Find the current address** فقط پست‌های امضا شده را می‌پذیرد، بنابراین یک پست جعل‌شده نمی‌تواند شما و توکن پنل‌تان را به آدرس شخص دیگری ارسال کند. این موضوع در رکورد و cloud-init منتشر شده وجود دارد: هر کسی که آن‌ها را داشته باشد می‌تواند آدرس فعلی را بخواند، که همچنان برای توکن پنل درخواست می‌کند. سرور به هر حال هیچ پورت ورودی‌ای را باز نگه نمی‌دارد.

یک راستی‌آزما کلید آدرس ندارد و هر کسی که موضوع را بخواند می‌تواند در آن پست بگذارد. بنابراین گردآورنده همچنین خودِ آدرس را، امضا شده با کلید Ed25519 خود، پست می‌کند و `verify` جدیدترین پستی را که با کلید گردآورنده در رکورد استقرار امضا شده است، برمی‌دارد؛ پست‌ها بر اساس زمانی که ntfy.sh آن‌ها را دریافت کرده است مرتب می‌شوند، نه زمانی که ادعا می‌کنند. یک گردآورنده از قبل از این تغییر، هیچ چیزی را امضا نمی‌کند، و سپس `verify` جدیدترین پست را انتخاب کرده و در بررسی `statement` این موضوع را اعلام می‌کند؛ یک پست جعل‌شده تنها می‌تواند باعث شکست آن بررسی شود، زیرا آدرس همچنان باید با کلید گردآورنده پاسخ دهد.

هزینه‌اش چیست: هیچ حساب Cloudflare رکورد تونل سریع را نگه نمی‌دارد، بنابراین `verify` تونل، کانکتور و بررسی DNS را به عنوان در دسترس نبودن گزارش می‌کند و نتیجه در بهترین حالت `incomplete` (روی Phala در عوض، بررسی Cloud با موفقیت انجام می‌شود: کانکتور در داخل پیکربندی اندازه‌گیری‌شده Docker Compose اجرا می‌شود؛ سوابق ارائه‌دهنده، فایروال، بیانیه امضا‌شده، اندازه‌گیری‌های میزبان و مقایسه نصب‌کننده طبق معمول بررسی می‌شوند. مقایسه بایت با نصب‌کننده مرجع به یک commit مستقر نیاز دارد که از قبل `--quick-tunnel` را بشناسد؛ یک checkout نسخه 0.7.0، نصب‌کننده دامنه را می‌سازد و تفاوت را گزارش می‌کند. کلودفلر به تونل‌های سریع هیچ تضمینی برای زمان بهره‌برداری (uptime) نمی‌دهد، اجازه می‌دهد ۲۰۰ درخواست در حال انجام (in-flight) داشته باشد و رویدادهای ارسال‌شده توسط سرور (Server-Sent Events) را منتقل نمی‌کند، بنابراین ممکن است به‌روزرسانی‌های زنده پنل (نسخه‌های بعد از 0.7.0) از طریق آن نرسند و نیاز به بارگذاری مجدد نما (view) باشد؛ این بخش آزمایش نشده است. برای موردی که باید پایدار بماند، از دامنه خود استفاده کنید.

## راه‌اندازی

ابتدا به همه چیزهایی که ارسال خواهند شد نگاه کنید. `plan` درخواست ارائه‌دهنده یا Cloudflare انجام نمی‌دهد:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

سپس با همان گزینه‌ها و اعتبارنامه‌ها مستقر کنید:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

انواع سرور برای شروع: `cpx22` (Hetzner)، `s-1vcpu-2gb` (DigitalOcean)، `g6-standard-1` (Linode)، `vc2-1c-2gb` (ولتر)، `t3.small` (AWS). `--location` و `--image` پیش‌فرض برای هر ارائه‌دهنده، اوبونتو ۲۴.۰۴ در یک منطقه اروپایی.

`--repository` تغییرات را از یک مخزن Git دیگر با HTTPS دریافت می‌کند، بدون اعتبارنامه‌ها در URL (پیش‌فرض `https://github.com/phishdestroy/TgWitness.git`). `deploy` همچنین می‌پذیرد `--out` برای یک دایرکتوری استقرار دیگر (پیش‌فرض `deployments/NAME`؛ دایرکتوری که در حال حاضر یک استقرار در آن وجود دارد، رد می‌شود) و `--wait`، زمان انتظار برای بیانیه امضا شده جمع‌آوری‌کننده: ۱ تا ۲۴۰، پیش‌فرض ۲۰، یا ۶۰ برای `generic`.

دستور:

1. یک تونل Cloudflare ایجاد می‌کند که ورودی آن نام میزبان پنل را به پنل و، در صورت ارائه، نام میزبان شاهد را به `/api/witness/head` و `/api/assurance` تنها؛
2. برای آن نام‌های میزبان، رکوردهای CNAME پروکسی‌شده ایجاد می‌کند و از ثبت نام‌هایی که از قبل وجود دارند، خودداری می‌کند؛
3. یک فایروال ارائه‌دهنده بدون قواعد ورودی و یک سرور پشت آن بدون کلید SSH، بدون پشتیبان، بدون عامل کنسول، و cloud-init که SSH را مخفی می‌کند، روت را قفل می‌کند، نصب می‌کند `cloudflared`، دقیقاً همان commit را دریافت می‌کند، آن را بررسی می‌کند و TgWitness را به عنوان یک سرویس systemd سخت‌شده راه‌اندازی می‌کند؛
4. منتظر بیانیهٔ امضا‌شدهٔ کلکسیونر می‌ماند و بررسی می‌کند که آیا این بیانیه، این سرور و هَش این cloud-init را نام می‌برد.

`deployments/case-2026-11/` سپس شامل است:

| فایل | فهرست مطالب | اشتراک‌گذاری؟ |
| --- | --- | --- |
| `deployment.json` | شناسهها، هشها، فراخوانی‌های API انجام‌شده (متد، مسیر، وضعیت) و اولین عبارت امضا‌شده | بله، با اعتبارسنج |
| `cloud-init.redacted.yaml` | نسخهٔ دقیق cloud-init که دو رمز آن با ... جایگزین شده‌اند `REDACTED` | بله |
| `panel-token.txt` | توکن پنل | خیر |

رمز عبور ریشهٔ ارائه‌دهنده، توکن تونل و توکن پنل هرگز در `deployment.json`. اثر انگشت کلکتیوری را که در انتها ثبت شده است، تنها از طریق کانالی که کنترل آن در دست شما نیست، مانند یک کانال شاهدی یا یک پیام به گیرنده، منتشر کنید.

در تلگرام وارد شوید در `https://case.example.org` با توکن پنل، همان‌طور که در [راهنمای حساب](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/) کاربری آمده است. اقدامات پنل در دفترچه یادداشت امضا شده ثبت می‌شوند؛ آن‌ها جلسات SSH نیستند. یک [شاهد](https://phishdestroy.github.io/TgWitness/fa/docs/reference/witness/) می‌تواند درخواست وضعیت بدهد `https://case-witness.example.org`.

SSH وجود ندارد: اگر بوت‌استرپ شکست بخورد، کالکتور هرگز پاسخ نمی‌دهد. سرور را حذف کرده و دوباره مستقر کنید، یا از استقرار عیب‌یابی (debug deployment) برای یافتن علت استفاده کنید.

### رازها در داده‌های کاربر

cloud-init دو رمز را در خود حمل می‌کند: توکن پنل و توکن تونل کلودفلر. کلید امضا در میان آن‌ها نیست؛ این کلید روی سرور ایجاد می‌شود. Hetzner، DigitalOcean و Linode داده‌های کاربر را از طریق API خود بازنمی‌گردانند. Vultr آن را به هر کلیدی که بتواند نمونه را بخواند بازمی‌گرداند، و EC2 از طریق `DescribeInstanceAttribute`. برای AWS، فقط سه اقدام جدول را به راستی‌آزما بدهید، هرگز `ec2:Describe*`. برای Vultr، فرض کنید کلید اعتبارسنج می‌تواند هر دو توکن را بخواند. یک توکن تونل به کسی اجازه می‌دهد یک کانکتور دوم را اجرا کند: `verify` گزارش می‌کند هر کانکتوری که روی سرور نیست، و بیانیه‌های جمع‌کننده را نمی‌توان به این شکل جعل کرد زیرا هر کدام یک چالش جدید را امضا می‌کنند. با `--quick-tunnel` راز دوم در عوض کلید آدرس است: هر کسی که آن را بخواند می‌تواند یک آدرس جعلی ارسال کند که پنل آن را می‌پذیرد.

بیانیهٔ عمومی گردآورنده، آدرس سرور و منابع ورودها را حذف می‌کند؛ هر دو در دفترچهٔ ثبت امضا شده باقی می‌مانند.

## عیب‌یابی استقرار و قفل

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` کلید SSH را برای یک کلید از یک آدرس یا شبکه کوچک، حداکثر یک /24 برای IPv4 یا یک /48 برای IPv6، نگه می‌دارد. `KEY` از قبل با ارائه‌دهنده ثبت شده است: نام یا شناسه یک کلید SSH در پروژه Hetzner، شناسه یا اثر انگشت یک کلید SSH در تیم DigitalOcean، نام کاربری Linode که کلیدهای SSH پروفایل آن به ریشه اضافه شده‌اند، شناسه یک کلید SSH در حساب Vultr، یا نام یک جفت کلید EC2 در منطقه. این گزینه‌ها برای `generic`. چنین استقراری به عنوان `debug` و **هرگز** به عنوان دارای سطح اطمینان بالا گزارش نمی‌شود. وقتی کارتان تمام شد، اجرا کنید `sudo tgwitness-lock` را به‌عنوان آخرین دستور جلسه SSH اجرا کنید، سپس:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

فایروال تمام قوانین ورودی را از دست می‌دهد. سپس گزارش‌ها نشان می‌دهند که SSH چه زمانی مجاز بوده و چه زمانی بسته شده است؛ آن بازه زمانی همچنان قابل مشاهده باقی می‌ماند.

## حذف یک استقرار

`destroy` سرور و فایروال آن را که با برچسب استقرار پیدا شده‌اند، حذف می‌کند تا استقراری که در نیمه راه ناموفق بوده نیز حذف شود، سپس رکوردهای DNS که به تونل آن اشاره دارند و خود تونل را حذف می‌کند. مجله و کلید امضای سرور به همراه آن حذف می‌شوند: ابتدا شواهد را صادر کنید. رکورد باقی می‌ماند، با علامت `removed`، با فراخوانی‌های API حذف.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

حذف از طریق API برای Hetzner پیاده‌سازی شده است. برای سایر ارائه‌دهندگان `destroy` پیش از حذف هر چیزی متوقف می‌شود و برچسبی را که باید حذف شود در کنسول ارائه‌دهنده نام‌گذاری می‌کند. یک سرور دستی نصب‌شده (`generic`) تنها رکوردهای تونل و DNS خود را از دست می‌دهد. استقرار سریع تونل به توکن Cloudflare نیازی ندارد: تونل آن با سرور پایان می‌یابد و پست‌های آن ظرف ۱۲ ساعت از ntfy.sh منقضی می‌شوند.

## هر سرور (خودگواهی‌شده)

`--provider generic` برای سروری است که خریداری شده یا به‌صورت دستی نصب شده باشد. `deploy` تونل و DNS را ایجاد می‌کند، می‌نویسد `install.sh` (خصوصی) و `install.redacted.sh` (برای انتشار)، و منتظر می‌ماند. کپی `install.sh` آن را در یک سرور تازه نصب‌شده اوبونتو ۲۴.۰۴ کپی کرده و در آنجا اجرا کنید:

```
sudo bash install.sh
```

این ابزار میزبان را همان‌گونه که بود ثبت می‌کند (ورودی‌ها، حساب‌ها، `authorized_keys`، سوکت‌های شنود، خدمات، کارهای زمان‌بندی‌شده، بسته‌ها)، commit را نصب می‌کند، فایروال میزبان را فعال می‌کند، خود را حذف می‌کند، SSH را مخفی می‌سازد و جلسه را پایان می‌دهد. گزارش چنین سروری در بهترین حالت **خودگواهی‌شده (SELF-ATTESTED)** است: هر کسی که نصب‌کننده را اجرا کرده قبلاً دسترسی روت داشته و هیچ رکورد ارائه‌دهنده‌ای برای راستی‌آزمایی‌کننده در دسترس نیست. این هنوز بهتر از یک سرور بدون توضیح است: موجودی، هش نصب‌کننده و هر ورود بعدی امضا شده‌اند.

## تأیید

تأییدکننده نیاز دارد `deployment.json`، نصب‌کننده منتشر شده، اعتبارنامه‌های فقط-خواندنی و، به‌طور ایده‌آل، یک خروجی از commit و یک مدرک ZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

هر ارائه‌دهنده و مقدار Cloudflare در آن لحظه توسط اعتبارسنج درخواست می‌شود؛ رکورد فقط شناسه‌هایی را که باید پرسیده شوند، فراهم می‌کند. کد خروج برای **PASS** برابر 0، برای **FAIL** برابر 1 و برای **REVIEW**، **INCOMPLETE** یا **SELF-ATTESTED** برابر 2 است. `--fingerprint` باید از یک کانال مستقل بیاید؛ بدون آن، کلید فقط با رکورد اپراتور مقایسه می‌شود. `python verify.py` هنوز خودِ ZIP، همانند بخش [Evidence](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/)، شواهد را تأیید می‌کند.

اقدامات ارائه‌دهنده طبقه‌بندی می‌شوند: ایجاد و شروع در ۳۰ دقیقه پس از ایجاد، عبور؛ کنسول، بازیابی، بازنشانی رمز عبور، بازسازی، ISO، تصاویر، اسنپ‌شات‌ها، پشتیبان‌ها، مدیر سیستم، اتصال نمونه EC2 و باز کردن فایروال ناموفق هستند؛ اقدامات مربوط به برق و هر چیزی که غیرمنتظره است برای بازبینی علامت‌گذاری می‌شوند. یک اقدام ناشناخته هرگز بی‌سروصدا رد نمی‌شود.

## گزارش تحویل مدرک

`--report report.md` گزارش مارک‌داون را می‌نویسد و `report.json` در کنار آن:

1. نتیجه، اثر انگشت کلید گردآورنده، استقرار، ارائه‌دهنده، کامیت، سرور، فایروال، تونل؛
2. هر بررسی به همراه وضعیت و منبع آن (API ارائه‌دهنده، API کلودفلر، بیانیه گردآورنده، مجله شواهد)؛
3. لاگ ارائه‌دهنده با ارزیابی هر اقدام و، در مواردی که ارائه‌دهنده آن را ثبت می‌کند، عامل؛
4. نقطه‌های پایانی کلودفلر که اتصالات، پیکربندی و گزارش‌های حسابرسی تونل را در خود نگه می‌دارند؛
5. بیانیهٔ امضا‌شدهٔ گردآورنده؛
6. آنچه گزارش اثبات می‌کند و آنچه اثبات نمی‌کند؛
7. دستورالعمل‌هایی برای بازتولید آن و SHA-256 هر فایلی که به آن داده شده است.

گزارش را تحویل دهید، `report.json`, `deployment.json`، نصاب منتشرشده و مدرک ZIP را تحویل دهید. گزارش را زود تهیه کنید: لاگ‌های ارائه‌دهنده برای دوره‌های محدودی نگهداری می‌شوند.

## کلودفلر به‌عنوان شاهد بیرونی

همه چیز در اینجا اختیاری است. بدون حساب Cloudflare، سرور همچنان اجرا می‌شود و دو مورد از این موارد امروز کار می‌کنند:

| چه | آنچه نشان می‌دهد | در TgWitness |
| --- | --- | --- |
| تونل سریع یا تونل دامنه‌ی شما | پنل تنها از طریق تونل قابل دسترسی است | جادوگر سرور، به بالا مراجعه کنید |
| drand relay `drand.cloudflare.com` | سوابق پس از یک دور drand جدیدتر از آن هستند: این دفترچه یادداشت همزمان با وقوع رویداد نوشته شده است. | حالت مدرک، **شاهدان بیشتر**، بدون حساب ([قالب](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| اعلان‌های وضعیت تونل | وقتی تونل قطع بود، از طریق ایمیل یا وب‌هوک از Cloudflare | آنها را در داشبورد کلودفلر تنظیم کنید |
| DNS دروازه (`--gateway-dns`، یا **DNS دروازه‌ای کلودفلر** در جادوگر) | هر نامی که سرور جستجو کرد، توسط Cloudflare از طریق TLS پاسخ داده شد؛ فایروال Hetzner اجازه نمی‌دهد DNS به هیچ چیز دیگری دسترسی پیدا کند؛ اینکه آیا یک سیاست Gateway می‌تواند پاسخ‌ها را بازنویسی کند | Hetzner، طرح رایگان Zero Trust، بدون دامنه؛ `verify` فایروال، مکان، لاگ‌گیری، سیاست‌ها، پرس‌وجوهای سرور و لاگ حسابرسی را بررسی می‌کند؛ حالت شواهد، لاگ را در ژورنال کپی می‌کند |
| Gateway با کلاینت Cloudflare One روی سرور، یک فایروال خروجی که تنها به Cloudflare اجازه عبور می‌دهد | هر اتصالِ سرور، نه فقط DNS | هنوز ساخته نشده است |
| دسترسی در مقابل پنل | چه کسی وارد پنل شده و چه زمانی | ساخته نشده: به دامنهٔ شخصی شما نیاز دارد |
| ثبت دستورات SSH | هر دستور در یک جلسه اشکال‌زدایی | هنوز ساخته نشده است |

Logpush که نسخهٔ اختصاصی Cloudflare را در R2 نگه می‌دارد، یک ویژگی سازمانی است: در طرح رایگان، Cloudflare پاسخ می‌دهد `logpush is not enabled for this account`. لاگ گیت‌وی آن در آنجا ۲۴ ساعت دوام می‌آورد، بنابراین حالت شواهد آن را در دفترچه یادداشت امضا شده کپی می‌کند (**لاگ گیت‌وی کلودفلر از پرس‌وجوهای DNS این سرور،** یک توکن فقط-خواندنی با دسترسی به تحلیل حساب).

بدون یک طرح اعتماد صفر، یک حساب یک مکان DNS دارد. هنگامی که Cloudflare مکان دیگری را رد می‌کند، سرور مکان موجود را به اشتراک می‌گذارد و پرس‌وجوهای آن بر اساس آدرسشان از هم متمایز می‌شوند؛ آن فیلتر نیاز به دسترسی خواندن PII اعتماد صفر نیز دارد، و `destroy` یک مکان مشترک را ترک می‌کند. یک پرس‌وجوی لاگ حداکثر سه ساعت را در بر می‌گیرد، بنابراین کپی و `verify` خواندن روز در بازه‌های ساعتی سه ساعته انجام می‌شود.

DNS گیت‌وی، حل‌کننده سیستم را پوشش می‌دهد. DNS بر روی HTTPS در پورت ۴۴۳ به یک حل‌کننده دیگر، و اتصالات به آدرسی که در هیچ‌جا یافت نمی‌شود (برای مثال، مراکز داده تلگرام)، در لاگ آن ثبت نمی‌شوند.

کلودفلر نمی‌تواند محتوای داخل رمزگذاری تلگرام، سایر دستگاه‌های متصل به حساب تلگرام (فهرست دستگاه‌های حالت مدرک، آن‌ها را از سمت تلگرام ثبت می‌کند) یا هایپروایزر ارائه‌دهنده را مشاهده کند.

## خواندن نتیجه استقرار

For an ordinary VM, the provider controls the host infrastructure, and local inventory is checked alongside provider records. For Intel TDX, the verifier additionally checks the hardware quote, collector binding, compose and OS measurements. Read the individual results to see which checks passed or were unavailable.

Historical firewall detail depends on the provider; Linode retains rule versions. The [validation record](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/) lists tested deployments and remaining live checks, and [verification scope](https://phishdestroy.github.io/TgWitness/fa/docs/reference/evidence/#verification-scope) connects these environment checks to archive acquisition and integrity.
