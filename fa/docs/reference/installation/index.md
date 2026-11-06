# نصب، تأیید و به‌روزرسانی

Canonical page: https://phishdestroy.github.io/TgWitness/fa/docs/reference/installation/

نصب با یک دستور، بررسی امضاها و هش‌ها، به‌روزرسانی و حذف یک نصب.

[پروژه](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [راه‌اندازی سریع](https://phishdestroy.github.io/TgWitness/fa/docs/reference/quickstart/) · [استقرار](https://phishdestroy.github.io/TgWitness/fa/docs/reference/deployment/)

## با یک دستور نصب کنید

نصب‌کنندهٔ راهنمایی‌شده شامل یک محیط اجرای خصوصی پایتون است. برای نصب‌های آینده از همان آدرس استفاده کنید: هر انتشار، نصب‌کننده، هش‌ها، امضاها و اطلاعات ساخت را به‌طور همزمان به‌روزرسانی می‌کند.

**لینوکس / مک‌اواس (بش):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

روی یک سرور اوبونتو، برای نصب یک سرویس پس‌زمینه، آن را با دسترسی ریشه اجرا کنید. روی یک دسکتاپ، آن را با حساب کاربری معمولی خود اجرا کنید.

**ویندوز (PowerShell یا Command Prompt):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

در ویندوز نیازی به مدیر سیستم نیست. فرآیند فرزند PowerShell ترمینال شما را با نتیجه باز نگه می‌دارد. پایتون و وابستگی‌ها در نصب باقی می‌مانند.

در اوبونتو، **«این رایانه**»، **«لینک موقت HTTPS**» یا **«دامنه اختصاصی**» را انتخاب کنید. نصب‌کننده آدرس پنل و کلید دسترسی را چاپ می‌کند. برای یک لینک موقت، آن آدرس HTTPS را در مرورگر خود باز کرده و کلید را وارد کنید. با دسترسی محلی روی یک سرور از راه دور، از یک فوروارد SSH از رایانه خود استفاده کنید (`ssh -L 8787:127.0.0.1:8787 user@server`) و آن را باز کنید `http://127.0.0.1:8787`. در macOS و ویندوز، پنل محلی در مرورگر شما باز می‌شود؛ ترمینال آن را در حال اجرا نگه دارید.

در پنل وارد تلگرام شوید و انتخاب کنید چه اطلاعاتی را جمع‌آوری کنید. نصب به تنهایی باعث شروع جمع‌آوری تلگرام نمی‌شود.

## محلی که همه‌چیز در آن اجرا می‌شود

`get.destroy.tools` یک **Cloudflare Worker دانلودهای ایستا را ارائه می‌دهد** است. این برنامه پنل TgWitness، جلسه تلگرام یا پایگاه داده شواهد کاربر ندارد. این برنامه به یک VPS پروژه مسیریابی نمی‌شود. این برنامه روی ماشینی که دستور را در آن اجرا می‌کنید، اجرا می‌شود.

| نصب | برنامه | داده‌ها |
| --- | --- | --- |
| اوبونتو به‌عنوان ریشه | `/opt/tgwitness` | سرویس سیستم: `/var/lib/tgwitness-<installation ID>`; استفاده کنید `tgwitness paths` برای مسیر دقیق. |
| کاربر لینوکس / مک‌اواس | `~/.local/share/tgwitness` | `data/live` زیر آن نصب. |
| کاربر ویندوز | `%LOCALAPPDATA%\TgWitness` | `data\live` زیر آن نصب. |

تنظیم `TGWITNESS_INSTALL_DIR` برای انتخاب پوشهٔ دیگر. نسخه‌های نصب‌شده و داده‌ها جدا هستند. نصاب، حساب‌ها، پیام‌ها یا کلیدهای شما را به سایت دانلود آپلود نمی‌کند. انتخاب یک تونل کلودفلر، ترافیک پنل را از طریق کلودفلر ارسال می‌کند؛ استفاده از دامنهٔ خودتان، ترافیک را به سرور خودتان هدایت می‌کند.

هر نصب شامل **فایل‌های START-HERE.html** و **START-HERE.txt** است که شامل مسیرهای محلی، دستورات و لینک‌هایی به مخزن (repository) می‌باشد. اجرا کنید `tgwitness guide` برای باز کردن راهنما. در ویندوز، از دستور زیر استفاده کنید: `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` در PowerShell استفاده کنید.

## تنظیمات جستجوی متن کامل

[جستجوی متن کامل](https://phishdestroy.github.io/TgWitness/fa/docs/reference/search/) (پیش‌نمایش) نیازی به تنظیم ندارد. نمایه‌اش پس از به‌روزرسانی در پس‌زمینه ساخته می‌شود.

| متغیر یا فرمان | اثر |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | پیش‌فرض: شاخص در نگهداری می‌شود `search/fulltext.sqlite3` هر فضای کاری |
| `TGWITNESS_FULLTEXT=memory` | فایل شاخص وجود ندارد؛ شاخص در هر بار راه‌اندازی دوباره ساخته می‌شود |
| `TGWITNESS_FULLTEXT=off` | بدون نمایه؛ فقط جستجوی متنی دقیق |
| `tgwitness index status` | وضعیت هر فضای کاری را فهرست‌بندی کنید |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | هر نمایه را از دفترچهٔ امضا‌شده بازسازی کنید |

انتخاب مدیر در **Journal → Filters → Search index** بر متغیر آن فضای کاری اولویت دارد. دستورات دایرکتوری دادهٔ نصب را که آن‌ها را اجرا می‌کند پیدا می‌کنند؛ در جاهای دیگر، اضافه کنید `--data-dir` با مسیر از `tgwitness paths`. برای یک فرهنگ لغت کامل اوکراینی (داده‌های GPL-3.0)، نصب کنید `pymorphy3-dicts-uk` در محیط پایتون نصب.

## دسترسی خط فرمان

[خط](https://phishdestroy.github.io/TgWitness/fa/docs/reference/cli/) [فرمان](https://phishdestroy.github.io/TgWitness/fa/docs/reference/cli/) (پیش‌نمایش) آرشیو را برای اسکریپت‌ها و ایجنت‌ها می‌خواند.

| متغیر | اثر |
| --- | --- |
| `TGWITNESS_URL` | آدرس پنل برای `tgwitness search`, `context`, `messages`, `stats` و `export`؛ پیش‌فرض `http://127.0.0.1:8787` وقتی یک توکن تنظیم می‌شود |
| `TGWITNESS_MCP_TOKEN` | توکن اتصال را از **Integrations → MCP** بایگانی کنید، که با کلاینت‌های MCP به اشتراک گذاشته می‌شود؛ `--token-file` در عوض آن را از یک فایل می‌خواند |
| `TGWITNESS_DATA` | زمانی که هیچ ... داده نمی‌شود، دایرکتوری داده‌ها مستقیماً خوانده می‌شود. `--data-dir`، URL یا توکن داده نشده باشد |

## پیش از اجرا تأیید کنید

دستور یک‌خطی برای اجرای اسکریپت اولیه به HTTPS اعتماد می‌کند. آن اسکریپت قبل از نصب، نشانی SHA-256 و امضای RSA پروژه را روی برنامه و محدودیت‌ها بررسی می‌کند. همچنین می‌توانید ابتدا اسکریپت اولیه را دانلود و تأیید کنید.

کلید انتشار عمومی [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub) است. SHA-256 آن عبارت است از:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

این اثر انگشت را از یک بازنگری مخزن که به آن اعتماد دارید، حفظ کنید. یک چک‌سام از همان سرور دانلود، عدم تطابق را تشخیص می‌دهد؛ کلید عمومی مستقل مورد اعتماد، چیزی است که امضای یک نسخه را احراز هویت می‌کند.

برای دانلودهای تأیید اعتبار زیر از یک دایرکتوری جدید و خالی استفاده کنید.

**لینوکس / مک‌اواس — در یک دایرکتوری دانلود جدید و خالی اجرا شود** (نیازمند curl و OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

The `&&` زنجیره در صورتی که بررسی دانلود، اثر انگشت کلید یا امضا ناموفق باشد، قبل از اجرا متوقف می‌شود. اگر انتشار بین دانلود اسکریپت و امضای آن رخ دهد، هر دو را دوباره دانلود کنید. نصبی‌های قدیمی، URLهای بستهٔ ثابت خود را حفظ می‌کنند.

**ویندوز — قبل از اجرا، SHA-256 را بررسی کنید:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

هش را با ... مقایسه کنید `install.ps1` خط. برای بررسی مستقل امضا، از OpenSSL (برای مثال، از طریق Git Bash) و همان اثر انگشت کلید عمومی فوق استفاده کنید:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

خود نصب ویندوز امضاهای بسته را با .NET تأیید می‌کند و به OpenSSL نیازی ندارد. این‌ها امضاهای جداگانه RSA-3072 / SHA-256 هستند، نه Authenticode. [منیفست](https://get.destroy.tools/manifest.json) نسخه نرم‌افزار، کامیت دقیق Git، شناسه انتشار تغییرناپذیر و SHA-256 هر آرتیفکت را ثبت می‌کند. این صفحه به منبع مربوطه لینک می‌دهد. منیفست و لیست چک‌سام نیز امضاهای جداگانه‌ای دارند (`manifest.json.sig` و `SHA256SUMS.txt.sig`).

## به‌روزرسانی یک نصب موجود

**یک انتشار جدید، سایت دانلود را به‌روزرسانی می‌کند؛ برنامه‌های نصب‌شده وقتی دوباره نصب‌کننده را اجرا می‌کنید، به‌روزرسانی می‌شوند.** هیچ به‌روزرسانی‌کننده‌ی بدون نظارت یا راه‌اندازی مجدد خودکار برای مجموعه‌ی در حال اجرا وجود ندارد. کانال نصب‌کننده‌ی فعلی **پیش‌نمایشی** است؛ این کانال از نسخه‌های منتشرشده و بررسی‌شده‌ی `main`، که commit آن می‌تواند جدیدتر از آخرین نسخه شماره‌گذاری‌شده GitHub باشد. نسخه صفحه از `pyproject.toml`؛ commit و شناسه build آن، به‌روزرسانی‌ها را در همان نسخه پیش‌نمایش از هم متمایز می‌کند.

Publication is automatic after that exact commit passes the application and security checks and the signed package passes Ubuntu service and Windows PowerShell installation tests. While checks are running, or if they fail, the same commands continue to install the previous checked build. The build manifest shows which commit is currently available; the version number alone may stay the same between preview updates.

از همان پوشه نصب و کاربر سیستم‌عامل قبلی استفاده کنید. از دایرکتوری کامل داده با متوقف کردن جمع‌آوری نسخه پشتیبان تهیه کنید؛ `tgwitness paths` آن را شناسایی می‌کند. یک خروجی امضا شده نسخه پشتیبان کامل نصب نیست.

**نصب ریشهٔ اوبونتو در `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

پس از نصب موفقیت‌آمیز:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

برای نصب کاربر لینوکس/macOS، از فایل نصب اصلی آن استفاده کنید. `TGWITNESS_INSTALL_DIR` یا از پیش‌فرض استفاده کرده و دستور نصب اول را دوباره اجرا کنید. قبل از به‌روزرسانی، یک پنل در پیش‌زمینه را ببندید و پس از آن دوباره آن را راه‌اندازی کنید. برای یک سرویس کاربر لینوکس پیکربندی‌شده، آن را اجرا کنید `tgwitness restart` را اجرا کنید.

**ویندوز:** پنل در حال اجرا را ببندید، دستور نصب ویندوز را دوباره اجرا کنید، سپس باز کنید `bin\tgwitness.cmd` در همان نصب. نصاب داده‌ها، جلسات، تنظیمات دسترسی و کلیدهای امضا را حفظ می‌کند. این نصاب تنها پس از اینکه محیط جدید بررسی‌های خود را با موفقیت پشت سر گذاشت، لانچر را تعویض می‌کند؛ نصب ناموفق، لانچر قبلی را سر جای خود باقی می‌گذارد. نسخه پشتیبان پیش از ارتقا را برای تغییرات در فرمت ذخیره‌سازی نگه دارید.

## دستورهای روزمره در اوبونتو

| فرمان | نتیجه |
| --- | --- |
| `tgwitness open` | URL فعلی پنل و کلید دسترسی. |
| `tgwitness paths` | مسیرهای دقیق برنامه، داده‌ها و راهنما. |
| `tgwitness guide --print` | دستورالعمل‌های کار آفلاین. |
| `tgwitness status` / `tgwitness logs` | دسترسی / گزارش‌های سرویس. |
| `tgwitness stop` / `tgwitness start` | متوقف / از سرگیری سرویس؛ حفظ داده‌ها. |
| `tgwitness token rotate` | کلید مدیر را تعویض کنید و جلسات مرورگر را پایان دهید. |
| `tgwitness tunnel off` | تونل سریع عمومی را غیرفعال کنید؛ پنل محلی را حفظ کنید. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | ایجاد یک لینک تونل سریع / جایگزینی آدرس آن. |

برای مشاهده توکن‌های همکار، جلسات و محدودیت‌های IP و [انتشار نصبی](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) برای گردش کار انتشار از گیت‌هاب به کلودفلر، به [بخش دسترسی](https://phishdestroy.github.io/TgWitness/fa/docs/reference/access/) مراجعه کنید.

## حذف TgWitness

هیچ پاک‌کننده‌ای وجود ندارد: شما پنل را متوقف کرده و پوشه‌های آن را حذف می‌کنید. حذف پوشهٔ داده‌ها، دفترچه‌ها، کلیدهای امضا، جلسات تلگرام و فایل‌های ذخیره‌شده را برای همیشه از بین می‌برد. پیش از آن:

1. آنچه نیاز دارید را صادر کنید (**صادرات → دانلود ZIP امضا شده**) و اثر انگشت کلید امضا و نقاط کنترل را خارج از این دستگاه نگه دارید. برای نگهداری خود فضای کاری، کل پوشه داده را با متوقف کردن جمع‌آوری کپی کنید.
2. سرورهایی را که در مسیر **Extras → Server 24/7** از **Your servers** یا با `python -m tgwitness.cloud destroy`؛ ارائه‌دهنده تا زمان حذف آن‌ها، هزینه‌شان را محاسبه می‌کند.
3. جلسه هر حساب را در تلگرام تحت **«تنظیمات» → «دستگاه‌ها»** پایان دهید. حذف فایل‌ها باعث خروج از جلسه از سمت تلگرام نمی‌شود.

**نصب روت اوبونتو.** به پوشهٔ داده توجه کنید، سرویس را متوقف کنید، سپس سرویس، پوشه‌ها و میانبر را حذف کنید:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**نصب برای کاربر لینوکس یا مک‌او‌اس.** پنل را ببندید. یک سرویس کاربر لینوکس پیکربندی‌شده با `systemctl --user disable --now tgwitness-<ID>`؛ واحد آن در `~/.config/systemd/user/`. سپس حذف کنید `~/.local/share/tgwitness` (یا `TGWITNESS_INSTALL_DIR`) و `~/.local/bin/tgwitness` را حذف کنید.

**ویندوز.** پنل را ببندید و حذف کنید `%LOCALAPPDATA%\TgWitness` (یا `TGWITNESS_INSTALL_DIR`). نصاب هیچ سرویس، وظیفه زمان‌بندی‌شده یا میان‌بر اضافه نمی‌کند.
