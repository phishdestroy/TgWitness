# فرمت‌های حساب کاربری و جلسه

Canonical page: https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/

ورود با شماره تلفن، کد QR یا کلید احراز هویت، وارد کردن جلسات تله‌تون، پایروگرام یا تلگرام دسکتاپ و اجرای چندین حساب کاربری.

TgWitness به عنوان یک **حساب کاربری تلگرام** (نه یک ربات) از طریق MTProto، با استفاده از Telethon، وارد می‌شود. هر حساب در **فضای** کاری خود (که در API و ابزارهای خط فرمان به آن *workspace* گفته می‌شود) با جلسه، منابع، دفترچه یادداشت و کلید امضای مخصوص به خود قرار دارد.

فایل‌های جلسه، رشته‌های جلسه و کلیدهای احراز هویت، **مجوزهای حساب کاربری** هستند: هر کسی که یکی از آن‌ها را در اختیار داشته باشد می‌تواند به‌عنوان آن حساب کاربری عمل کند. آن‌ها حاوی تاریخچه پیام‌ها نیستند.

> [!هشدار] **از هر چیزی که تحمل از دست دادن آن را ندارید، استفاده نکنید.** ما قویاً توصیه می‌کنیم که حساب‌های شخصی یا هر حساب باارزش دیگری را متصل نکنید و روی حسابی که برایتان ارزش دارد، شناسه API / هش API ایجاد نکنید. این موضوع به معنای آزمایش‌نشده بودن TgWitness نیست: تلگرام حساب‌ها را به طور غیرقابل پیش‌بینی محدود و برای همیشه مسدود می‌کند — به دلیل حجم درخواست‌هایی که آن را بیش از حد می‌داند، صرف‌نظر از کلاینت یا هدف، و بدون هیچ‌گونه مستندات کافی. بسیاری از این مسدودسازی‌ها برگشت‌ناپذیر هستند. از حساب‌های اختصاصی استفاده کنید. اجرای روان تست‌ها به تلگرام بستگی دارد، نه به نرم‌افزار، و هیچ تضمینی برای آینده ندارد.

- [نگاهی اجمالی](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#at-a-glance)
- [قبل از شروع: شناسهٔ API و هش API](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [شماره تلفن](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#phone-number) · [کد QR](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#qr-code) · [کلید اuth + شناسه DC](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#auth-key--dc-id)
- [فایل‌های حساب](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#account-files): [تله‌تون .جلسه](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#telethon-session) · [پایروگرام .session](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#pyrogram-session) · [جفت جلسه + JSON](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#telegram-desktop-tdata) · [رشتهٔ جلسه](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#telethon-stringsession) · [JSON حساب](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#account-json)
- [شناسایی کنید که چه چیزی در اختیار دارید](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#identify-what-you-have) · [فرمت‌های پشتیبانی‌نشده](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#unsupported-formats)
- [حساب‌های متعدد](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#multiple-accounts) · [حفظ امنیت فایل‌های حساب](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#keeping-account-files-safe) · [عیب‌یابی](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#troubleshooting)

## نگاهی اجمالی

| آنچه در اختیار دارید | زبانه‌ی **«افزودن حساب»** | همچنین به موارد زیر نیاز خواهید داشت |
| --- | --- | --- |
| شماره تلفن و دسترسی به کدهای ورود آن | **تلفن** | رمز عبور ۲FA در صورت فعال بودن |
| تلگرام در دستگاه دیگری باز است | **کد QR** | رمز عبور ۲FA در صورت فعال بودن |
| یک فایل `.session` (تله‌تون یا پایروگرام) | **فایل‌ها** | JSON اختیاری همراه برای تنظیمات برنامه |
| `.session` + `.json` با نام یکسان | **فایل‌ها** (هر دو را انتخاب کنید) | معمولاً هیچ چیز دیگری |
| پوشهٔ `tdata` در تلگرام دسکتاپ | **فایل‌ها** (به‌صورت ZIP) | رمز عبور محلی دسکتاپ در صورت تنظیم |
| یک جلسه رشته‌ای تله‌تون (متن، `.txt`، `.tgwitness-session`) | **فایل‌ها** | نیازی به جفت API جداگانه نیست |
| یک کلید `.json` با جلسه یا کلید احراز هویت | **فایل‌ها** | نیازی به جفت API جداگانه نیست |
| یک کلید احراز هویت (۵۱۲ کاراکتر هگزادسیمال) و شماره DC آن | **کلید رمزنگاری** | شناسه کاربری اختیاری |

TgWitness فایل‌ها را بر اساس **محتویات**شان شناسایی می‌کند، نه بر اساس نامشان. تغییر نام یک فایل هرگز آن را تبدیل نمی‌کند.

## قبل از شروع: شناسهٔ API و هش API

You can sign in without creating a Telegram API application. When no pair is entered, imported or already saved in the workspace, TgWitness picks a pair from its built-in pool of 50 public API pairs (`tgwitness/api_pool.py`), preferring Telegram Desktop for a fresh login and retaining a saved pair first; remaining candidates are shuffled. If Telegram refuses a pair (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), the next one is tried, up to eight per sign-in; refused pairs are skipped until restart. The pair that signed in is saved with the account and reused for it. An **API ID** and **API hash** identify the application to Telegram; they do not authorize an account by themselves.

Missing connection fields use a deterministic device/OS pair from the bundled [opentele2 2.0.0 catalogs](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735): Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834`, and Web `2496`. Android's source-build ID `4` also uses the Android catalog, as identified in [Telegram Android's BuildVars](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web defaults to A; an imported `K` app-version suffix or `macos` language pack selects K, and version `0.7.0` selects Webogram. Unknown application IDs keep Telethon's host defaults. Imported fields always win, including an older app version and an empty language pack. The catalog never changes the API ID/hash. Its version snapshot is reviewed explicitly, not fetched during login. A saved profile stays stable after updates.

`account.getAuthorizations` reports Telegram's saved authorization metadata; it is not an echo of each new `initConnection`. Compare it with the actual sent profile. Connecting an existing authorization does not validate its companion API hash: `initConnection` sends the API ID, while the hash is used by login requests.

After a new phone or QR authorization, TgWitness requests config, nearest DC, online status, languages (when the language pack is nonempty), app updates and terms-of-service updates, with 0.3–1.5 seconds between requests. Updating status briefly marks the account online. This sequence runs once at login completion, not on imports, reconnects or restarts. The authorization is saved first; a failed request stops the sequence without retrying or discarding the login. Results are recorded as `account.initialized`, with error names rather than response bodies. The sequence is not a guarantee against account restrictions.

For `tdesktop`, a missing `tz_offset` uses the server's local UTC offset, rounded to 900 seconds using the [opentele2 algorithm](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; license in `tgwitness/client_profiles.LICENSE`). It is refreshed on each connection so daylight-saving changes are reflected. An imported `tz_offset` takes precedence on every platform and is kept exactly, including zero. Other `initConnection.params` entries are retained. The HTTP sign-in form accepts the numeric timezone returned by file import; booleans, fractions and offsets outside the supported range are rejected.

Direct, SOCKS5 and HTTP CONNECT routes use Telethon's `ConnectionTcpObfuscated` (obfuscated abridged MTProto). HTTPS CONNECT retains TLS to the proxy and uses the same obfuscated transport inside the tunnel. MTProxy retains its required randomized intermediate transport and secret handling. Route switches apply the same choices. Obfuscation changes packet framing; it does not hide the account or its client metadata from Telegram or imply immunity to restrictions.

After connecting an authorized client, TgWitness checks config, nearest DC, the current authorization, the reviewed layer baseline, languages, app updates and terms-of-service updates. These diagnostics run once per client instance, before collection, and are shown under the connection details with their time. `account.connection_checked` records the result without session hashes, IPs, tokens or API hashes. They never accept terms or install updates. A request failure or FloodWait stops subsequent requests; a missing result stays unknown. Local checks can still report their results while network checks are skipped.

FloodWait diagnostics retain the failed TL method, any Takeout/range wrappers, the server-requested wait and the effective deadline in `telegram.backoff`. Connection details show the method and deadline while requests are paused. The diagnostic includes per-method client-call counters since that client was created; they count nested peer resolution separately, but do not count packets or Telethon's internal retry attempts. Current counters are also available as `collector.rpc_activity` in the status API. No request arguments, usernames, access hashes or exception text are included. The last diagnostic and full deadline survive restart. Earlier waits without a method record cannot be attributed retrospectively. See [export limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) for the source review and the distinction between discovery and history acquisition.

`official_app=True` or `False` is Telegram's current-authorization flag. Neither value establishes whether the account is restricted, trusted or under observation. The existing evidence-mode `account.devices` snapshots remain the history of all signed-in devices; connection diagnostics retain only the current device description.

Before connection, advisory checks compare the API platform, language pack, device/OS and app-version formats, mobile system locale, and Telethon's actual schema layer against the reviewed catalog baseline. Warnings appear in the server log and account status metadata; they never replace imported values or change the schema layer. A different layer is a compatibility review signal, not proof of a broken or restricted account. These checks and `official_app` do not certify that Telegram considers the account safe from restrictions. Disconnected account status uses the saved profile instead of generating another device description.

برای استفاده از برنامهٔ خود به جای آن (حساب کاربری که آن را ثبت می‌کند در معرض خطر است؛ ببینید: [چرا استخر API داخلی؟](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)):

1. [وب‌سایت my.telegram.org](https://my.telegram.org) را باز کنید و با هر شماره تلفنی که مالک آن هستید وارد شوید. کد به اپلیکیشن تلگرام ارسال می‌شود، نه از طریق پیامک.
2. **ابزارهای توسعهٔ API را** انتخاب کنید.
3. یک برنامه ایجاد کنید: هر عنوان و نام کوتاه (۵–۳۲ حرف)، پلتفرم **دسکتاپ**. URL و توضیحات می‌توانند خالی بمانند.
4. **ID اپلیکیشن api_id** (یک عدد) و **هش اپلیکیشن api_hash** (۳۲ کاراکتر هگزادسیمال) را کپی کنید.

در پنل، **شناسه API + هش** را زیر فرم ورود پیدا کنید. می‌توانید یک جفت `api_id:api_hash` را در **شناسه API** بچسبانید و هر دو فیلد پر می‌شوند. یک جفت می‌تواند برای تمام حساب‌های کاربری شما استفاده شود. پس از ورود موفقیت‌آمیز، این جفت فقط در همان فضای کاری ذخیره و رمزگذاری می‌شود و هرگز به مرورگر بازگردانده نمی‌شود.

سه اعتبارنامه‌ی متفاوت درگیر هستند:

| مخفی | باز می‌کند | محل استقرار |
| --- | --- | --- |
| توکن پنل | پنل وب TgWitness | `panel-token.txt` در دایرکتوری داده‌ها، یا `TGWITNESS_TOKEN` |
| شناسه API + هش | هیچ‌چیز به‌تنهایی؛ اپلیکیشن را شناسایی می‌کند | جفت پیش‌ساخته، تنظیمات واردشده، یا اپلیکیشن خودتان در my.telegram.org |
| مجوز حساب | حساب تلگرام | ایجادشده از طریق ورود با تلفن/QR یا واردشده به‌عنوان یک جلسه |

اگر تلگرام باید از طریق یک پروکسی دسترسی پیدا کند، ابتدا آن را در **حساب کاربری → تنظیمات → تنظیمات اتصال → تغییر مسیر اتصال** تنظیم کنید.

## شماره تلفن

1. **حساب کاربری را** باز کنید، به برگه **«تلفن»** بروید و شماره را به فرمت بین‌المللی وارد کنید، برای مثال `+44 7700 900123`. فاصله‌ها و خط‌های تیره به طور خودکار حذف می‌شوند.
2. روی **ادامه** کلیک کنید. شناسه API و هش می‌توانند خالی بمانند.
3. کدی را که تلگرام ارسال می‌کند وارد کنید (معمولاً به اپلیکیشن تلگرام؛ ارسال از طریق پیامک تضمین‌شده نیست).
4. اگر حساب کاربری احراز هویت دو مرحله‌ای داشته باشد، آن رمز عبور را وارد کنید. این توکن پنل نیست و کد عبور دستگاه نیز نیست.
5. شناسه حساب کاربری نمایش‌داده‌شده پس از ورود را بررسی کنید، سپس منابع را انتخاب کنید.

کدهای ورود و رمز عبور احراز هویت دو مرحله‌ای هرگز روی دیسک ذخیره نمی‌شوند.

## کد QR

از این زمانی استفاده کنید که حساب کاربری قبلاً در یک تلفن یا رایانه دیگر وارد شده باشد.

1. زبانه‌ی **کد QR** → **نمایش کد QR**. شناسهٔ API + هش می‌توانند خالی بمانند.
2. روی دستگاه وارد‌شده: **تنظیمات → دستگاه‌ها → اتصال دستگاه دسکتاپ**، کد را اسکن کرده و تأیید کنید.
3. در صورتی که تلگرام درخواست کند، رمز عبور ۲FA را در TgWitness وارد کنید.

تصویر QR به‌صورت محلی تولید می‌شود. کدها منقضی می‌شوند؛ برای تلاش مجدد روی **«تولید کد QR دیگر»** کلیک کنید. قفل کردن پنل، تغییر فضای کاری یا شروع ورود دیگری، کد در انتظار را لغو می‌کند.

## کلید اuth + شناسه DC

کلید احراز هویت (Auth Key) یک مجوز خام ۲۵۶ بایتی است که پشت هر جلسه تلگرام قرار دارد و به صورت **۵۱۲ کاراکتر هگزادسیمال**، به همراه شماره مرکز داده **DC 1–5** نوشته می‌شود.

1. **کلید احراز هویت** تب. کلید کامل را الصاق کنید؛ کلید کوتاه‌شده حاوی `…` کار نخواهد کرد.
2. شناسه DC ارائه‌شده همراه با کلید را انتخاب کنید.
3. اختیاری: **شناسه کاربری** را وارد کنید. در غیر این صورت، اگر تلگرام حساب متفاوتی را گزارش کند، TgWitness از اتصال خودداری می‌کند.
4. روی **حساب Connect** کلیک کنید.

یک کلید احراز هویت (۵۱۲ کاراکتر) با هش API (۳۲ کاراکتر) یکسان نیست. همین کلید همچنین می‌تواند به صورت JSON وارد شود، به [JSON حساب کاربری](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#account-json) مراجعه کنید.

## فایل‌های حساب

**گزینه «حساب جدید» را** باز کنید **→ «فایل‌ها» را** انتخاب کرده و تا **چهار فایل متعلق به یک حساب** (در مجموع **۸ مگابایت**) را برگزینید، سپس دکمه **«اتصال حساب» را** فشار دهید.

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- فایل‌ها **در حافظه‌ی** سرور TgWitness شما تبدیل می‌شوند. بارگذاری‌ها ذخیره نمی‌شوند، فایل‌های ZIP روی دیسک استخراج نمی‌شوند و هیچ سرویس خارجی‌ای درگیر نمی‌شود.
- سپس جلسهٔ حاصل با تلگرام بررسی می‌شود. اگر یک فایل شناسهٔ کاربر را مشخص کند، باید با حسابی که تلگرام گزارش می‌کند مطابقت داشته باشد.
- فایل‌هایی که حساب‌های مختلف یا اعتبارنامه‌های API متفاوت را توصیف می‌کنند، به جای انتخاب یکی، رد می‌شوند.
- **کد عبور یا متن جلسه**، فیلد رمز عبور محلی TData را در بر می‌گیرد، یک کادر برای چسباندن یک StringSession و **فایل‌های Read بدون نیاز به ورود** (فرم را بدون تماس با تلگرام پر می‌کند).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

### تله‌تون `.session`

|  |  |
| --- | --- |
| چیست | پایگاه دادهٔ SQLite که ابزارهای مبتنی بر Telethon ایجاد می‌کنند، برای مثال `my_account.session` |
| مورد تأیید | جدول‌ها `sessions` (با `dc_id`، `server_address`، `port`، `auth_key`) و `version` = ۷ یا ۸ |
| پیش‌نیازها | دقیقاً یک ردیف جلسه مجاز؛ یک پایگاه دادهٔ بسته و کامل |

ابتدا برنامه‌ای را که فایل را ایجاد کرده است ببندید. اگر فایل‌های `my_account.session-journal` یا `my_account.session-wal` در کنار آن وجود داشته باشد، پایگاه داده نهایی نشده است: کلاینت اصلی را به درستی باز و ببندید. حذف این فایل‌های جانبی (sidecar) می‌تواند یک نسخه خراب به جا بگذارد.

### پایروگرام `.session`

|  |  |
| --- | --- |
| چیست | پایگاه دادهٔ SQLite که ابزارهای مبتنی بر Pyrogram ایجاد می‌کنند |
| مورد تأیید | جدول `sessions` با `dc_id`، `auth_key`، `test_mode`، `user_id`، `is_bot`؛ `version` = ۲ یا ۳ |
| پیش‌نیازها | یک جلسهٔ **کاربر** مجاز در شبکهٔ تولید. جلسات بات و DC آزمایشی رد می‌شوند. |

شناسه کاربری ذخیره‌شده هنگام ورود با تلگرام بررسی می‌شود.

### جفت جلسه + JSON

حساب‌ها اغلب به صورت دو فایل با نام یکسان توزیع می‌شوند، برای مثال `447700900123.session` و `447700900123.json`. **هر دو را** همزمان انتخاب کنید.

- از روی JSON، TgWitness از `app_id`/`api_id` و `app_hash`/`api_hash` استفاده می‌کند، بنابراین معمولاً نیازی به وارد کردن اعتبارنامه‌های API ندارید.
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#account-json).

### تلگرام دسکتاپ (TData)

TData پوشهٔ `tdata` در اپلیکیشن Telegram Desktop (اپلیکیشن چندسکویی از desktop.telegram.org) است.

| سیستم | مکان پیش‌فرض `tdata` |
| --- | --- |
| ویندوز | `%APPDATA%\Telegram Desktop\tdata` (تلگرام قابل حمل: در کنار `Telegram.exe`) |
| لینوکس | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

برای وارد کردن آن:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> این امر در مورد موارد وارد شده نیز صدق می‌کند `.session` فایل‌ها، متن StringSession و هگز Auth Key. سایر کلاینت‌ها با مجوزهای مستقل خود می‌توانند به حالت ورود باقی بمانند. به [مستندات AUTH_KEY_DUPLICATED تلگرام](https://core.telegram.org/api/errors#406-not-acceptable) مراجعه کنید.

1. کاملاً از تلگرام دسکتاپ خارج شوید.
2. یک فایل ZIP ایجاد کنید که **فقط** شامل این دو مورد از `tdata` باشد:

   - `key_datas`
   - پایان فایل ۱۶ کاراکتری که با `s` خاتمه می‌یابد، در کنار آن، معمولاً `D877F783D5D3EF8Cs`

   زیپ کردن کل پوشه به همراه کش رسانه‌ای آن معمولاً از محدودیت‌ها (۵۱۲ مورد، ۳۲ مگابایت بدون فشرده‌سازی) فراتر می‌رود. ۳. در بخش **«فایل‌ها**»، زیپ را انتخاب کنید. اگر تلگرام دسکتاپ **رمز عبور محلی** دارد، ابتدا آن را در قسمت **«رمز عبور» یا متن جلسه** وارد کنید. این رمز عبور احراز هویت دو مرحله‌ای (2FA) نیست.

پشتیبانی‌شده: یک حساب در هر آرشیو، ذخیره‌سازی مدرن `key_datas`/`key_data0`/`key_data1`، رمز عبور محلی. پشتیبانی‌نشده: پوشه‌هایی با چندین حساب واردشده، طرح‌بندی‌های قدیمی‌تر دسکتاپ، فایل‌های ZIP محافظت‌شده با رمز عبور، و اپلیکیشن بومی جداگانه macOS به نام «Telegram for macOS».

### جلسه رشته‌ای تله‌تون

یک خط متن، معمولاً با شروع با `1` و با طول حدود ۳۵۰ کاراکتر. آن را به عنوان یک فایل `.txt` یا `.tgwitness-session` (حداکثر ۴ کیلوبایت) بارگذاری کنید، یا آن را زیر **متن رمز عبور یا جلسه** قرار دهید. فقط رشته‌های تله‌تون پذیرفته می‌شوند؛ رشته‌های Pyrogram و TDLib از فرمت‌های متفاوتی استفاده می‌کنند.

### JSON حساب

یک شیء JSON، حداکثر **۶۴ کیلوبایت**، در فایلی با پسوند **`.json`**.

| میدان (نام‌های مستعار) | معنی |
| --- | --- |
| `api_id` (`app_id`) | شناسهٔ برنامه، یک عدد مثبت |
| `api_hash` (`app_hash`) | هَش برنامه، ۳۲ کاراکتر هگزادسیمال |
| `string_session` (`session_string`, `session_str`; legacy `session`) | متن Telethon StringSession، نه نام فایل |
| `auth_key` (`auth_key_hex`) + `dc_id` | کلید احراز هویت ۵۱۲ کاراکتری و DC 1–5 را تکمیل کنید |
| `user_id` (`id`) | اختیاری؛ پیش از ذخیرهٔ مجوز، با تلگرام بررسی می‌شود |
| `device_model` (`device`) | Connection device description |
| `system_version` (`sdk`) | Connection OS version |
| `app_version` | Application version sent to Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Client language, system language and client language pack; an empty `lang_pack` is allowed |
| `tz_offset` | Optional UTC offset in seconds, sent in `initConnection.params`; integer or decimal integer string |

If both an alias and the main name are present, they must agree. Explicit Telethon session fields take priority over a generic `session` blob in another format. If both contain recognizable Telethon sessions, they must describe the same authorization. Without an explicit field, `session` must be a valid Telethon StringSession. Examples:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

اولین مثال فقط اطلاعات اعتبارنامه‌ی API را پر می‌کند؛ با تلفن یا QR وارد شوید، یا یک فایل جلسه اضافه کنید. فهرست‌های دسته‌ای (یک آرایه‌ی JSON از حساب‌ها) پذیرفته نمی‌شوند.

## شناسایی کنید که چه چیزی در اختیار دارید

| می‌بینید | این است | استفاده |
| --- | --- | --- |
| `*.session`؛ باز کردن آن در یک ویرایشگر متن، `SQLite format 3` را در بالا نشان می‌دهد | تله‌تون یا پایروگرام اس‌کیوالایت | **فایل‌ها** (به‌طور خودکار شناسایی‌شده) |
| یک پوشهٔ `tdata` حاوی `key_datas` | تلگرام دسکتاپ TData | دو فایل را فشرده کنید، سپس **Files** |
| یک خط متن با شروع `1`، حدود ۳۵۰ کاراکتر | جلسه رشته‌ای تله‌تون | **فایل‌ها** |
| `*.json` با `app_id`/`app_hash` | متادیتای همراه | **فایل‌ها**، همراه با جلسهٔ آن |
| `*.json` با `auth_key` یا `string_session` | JSON حساب | **فایل‌ها** |
| ۵۱۲ کاراکتر `0-9a-f` | کلید رمزنگاری | **کلید رمزنگاری** |
| ۳۲ کاراکتر `0-9a-f` | هَش API | **شناسهٔ API + هَش** |
| `td.binlog` یا `db.sqlite` از یک اپلیکیشن TDLib | ذخیره‌سازی TDLib | پشتیبانی نمی‌شود |
| `123456789:AA…` | توکن بات | پشتیبانی نمی‌شود |

## فرمت‌های پشتیبانی‌نشده

| قالب | جایگزین |
| --- | --- |
| ذخیره‌سازی TDLib (`td.binlog`) و خروجی‌های TDLib | ورود با تلفن یا QR |
| **رشته‌های** جلسه Pyrogram | از فایل Pyrogram `.session` استفاده کنید، یا تلفن/QR |
| TData با چندین حساب کاربری واردشده | از حساب‌های دیگر در تلگرام دسکتاپ خارج شوید، یا از فایل جلسهٔ اختصاصی هر حساب استفاده کنید |
| توکن‌های بات | پشتیبانی‌نشده: TgWitness به‌عنوان یک حساب کاربری مشاهده می‌کند |
| فهرست‌های CSV/JSON از حساب‌های متعدد | فایل‌های نشست پشتیبانی‌شده را از طریق **حساب‌ها → وارد کردن حساب‌ها** وارد کنید، یا در فضاهای کاری مجزا با شماره تلفن/QR وارد شوید |
| جلسات Test-DC یا بات | از یک حساب کاربری تولید استفاده کنید |

## حساب‌های متعدد

روی **+** در کنار انتخابگر حساب کاربری ضربه بزنید، یا مسیر **حساب کاربری → تنظیمات → تنظیمات اتصال → فضاهای کاری را** باز کنید، یک برچسب وارد کرده و وارد شوید.

- هر تعداد فضای کاری، از جمله فضای اصلی. هر کدام دارای جلسه، مسیر پروکسی، منابع، سیاست ضبط، دفترچه شواهد، کلید امضا، نقاط کنترل و خروجی‌های خود هستند.
- تغییر فضای کاری نمایش‌داده‌شده، سایر فضاها را متوقف نمی‌کند.
- یک ژورنال به حساب کاربری که آن را ایجاد کرده متصل می‌ماند. ورود به سیستم با حساب کاربری متفاوت نیازمند یک فضای کاری دیگر است و یک حساب نمی‌تواند به دو فضای کاری اختصاص یابد.
- توکن پنل اصلی بر تمام فضاهای کاری کنترل دارد. [دسترسی صادرشده](https://phishdestroy.github.io/TgWitness/fa/docs/reference/access/) می‌تواند افراد دیگر را به حساب‌ها و چت‌های منتخب محدود کند، با مجوزهای جداگانه و محدودیت‌های جلسه.
- **حساب‌ها** یک فضای کاری را بازنامه‌گذاری می‌کند و یکی از فضاهای کاری افزوده‌شده را همراه با جلسه، دفترچه، منابع و کلید امضای آن حذف می‌کند. فضای کاری اصلی را نمی‌توان از پنل حذف کرد.

### ورود دسته‌ای و گروه‌های حساب

برای افزودن چندین حساب، جفت کردن فایل‌ها بر اساس نام پایه و مشاهده نتیجه هر ورود، از مسیر **حساب‌ها → وارد کردن حساب‌ها** استفاده کنید. هر حساب فضای کاری مخصوص به خود را دریافت می‌کند.

یک گروه حساب‌های مرتبط را بدون ادغام جلسات، کلیدها یا شواهدشان در کنار هم نگه می‌دارد. **باز کردن گروه** در **بخش حساب‌ها** به صفحهٔ آن در `/groups/<id>`:

- **حساب‌ها:** مسیر اتصال، مشاهده و آخرین پیام هر عضو، با شروع**همه** و **توقف همه**.
- **نیاز به توجه:** حساب‌هایی که از آن‌ها خارج شده‌اند، در دسترس نیستند یا مشکل اتصال، دریافت، منبع یا رسانه دارند؛ هر نام به کارت مربوطه منتهی می‌شود.
- **چت‌ها در چندین حساب قابل مشاهده‌اند:** منابع مشترک، حساب‌هایی که آن‌ها را مشاهده می‌کنند و وقفه‌ها در دورهٔ مشاهدهٔ فضای کاری موجود (تا هفت روز). **خروجی‌گیری با N حساب،** خروجی یک کانال یا ابرگروه را بین آن‌ها تقسیم می‌کند و یک آرشیو را امضا می‌کند.
- **صادرات گروه:** یک ZIP با خروجی امضا‌شده هر حساب زیر `accounts/` و `manifest.json` که شامل امضاهای SHA-256 و اثرانگشت کلیدهای هر حساب است، امضا شده توسط فضای کاری اصلی در `manifest.signature.json`. هر آرشیو حساب را به طور جداگانه با `python -m tgwitness.verify` و اثر انگشت معتبر آن حساب.

اعضا تنظیمات گروه را به اشتراک می‌گذارند؛ یک حساب می‌تواند مقادیر خود را حفظ کند. به [تنظیمات مشترک](https://phishdestroy.github.io/TgWitness/fa/docs/reference/settings/#account-groups)، [راهنمای وارد کردن و گروه‌ها](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) و [داشبورد استخر MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources) مراجعه کنید.

## خروج

**گزینه حساب → خروج از تلگرام** (با توقف مشاهده) از تلگرام می‌خواهد که جلسه را پایان دهد، بنابراین این جلسه از بخش **تنظیمات → دستگاه‌ها** در حساب کاربری نیز ناپدید می‌شود و از گاوصندوق فضای کاری حذف می‌گردد. دفترچه یادداشت، منابع، تنظیمات و کلید امضا باقی می‌مانند و دفترچه یادداشت، خروج را ثبت می‌کند. محیط کاری همچنان متعلق به حساب کاربری خود است: فقط همان حساب کاربری می‌تواند دوباره به آن متصل شود. اگر تلگرام پاسخی ندهد، جلسه همچنان در اینجا حذف می‌شود و پنل این موضوع را اعلام می‌کند؛ جلسه را در تلگرام تحت **«تنظیمات → دستگاه‌ها»** پایان دهید.

## حفظ امنیت فایل‌های حساب

- با هر `.session`، فایل ZIP TData، StringSession، کلید احراز هویت و JSON حساب کاربری مانند یک رمز عبور رفتار کنید. TgWitness مجوز واردشده را در گاوصندوق رمزگذاری‌شده خود نگه می‌دارد؛ شما می‌توانید بعداً فایل‌های اصلی را حذف کنید.
- یک مجوز را همزمان در دو برنامه اجرا نکنید. تلگرام ممکن است آن را لغو کند (`AUTH_KEY_DUPLICATED`)، و هر دو نسخه از کار می‌افتند.
- یک جلسه منقضی‌شده یا لغوشده را نمی‌توان با تبدیل احیا کرد. دوباره وارد شوید.

## عیب‌یابی

| پیام یا نشانه | چه باید کرد |
| --- | --- |
| *نمی‌توان این جلسه را خواند. کلاینت اصلی آن را ببندید…* | فایل SQLite باز یا ناتمام است (سیدکار `-journal`/`-wal`). برنامهٔ اصلی را به‌طور صحیح ببندید و فایل را دوباره کپی کنید. |
| *اسکیماهای Telethon SQLite پشتیبانی‌شده: ۷ و ۸* / *پایروگرام … ۲ و ۳* | یک نسخه بسیار قدیمی یا ناشناخته از کتابخانه این فایل را ایجاد کرده است. به جای آن با تلفن/کد QR وارد شوید. |
| *فقط جلسات کاربری تولید مجاز پشتیبانی می‌شوند* | فایل Pyrogram متعلق به یک ربات یا شبکه آزمایشی است. |
| *آرشیو TData از ۵۱۲ ورودی یا ۳۲ مگابایت فراتر رفته است* | فقط فایل‌های ZIP `key_datas` و `D877F783D5D3EF8Cs`، نه کل پوشه. |
| *نمی‌توان TData را رمزگشایی کرد. رمز عبور محلی دسکتاپ را بررسی کنید.* | کد عبور محلی تلگرام دسکتاپ را در قسمت **«کد عبور» یا «متن جلسه**» وارد کنید. |
| *وارد کردن یک حساب TData به صورت همزمان* | تلگرام دسکتاپ چندین حساب داشت؛ به [فرمت‌های پشتیبانی‌نشده](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#unsupported-formats) مراجعه کنید. |
| *فایل‌های منتخب، حساب‌های مختلف یا اعتبارنامه‌های API را توصیف می‌کنند* | فایل‌های یک حساب کاربری را انتخاب کنید. |
| *JSON شامل هیچ اعتبارنامه‌ی API پشتیبانی‌شده یا مجوز نیست* | نام‌های فیلدها را در [JSON حساب](https://phishdestroy.github.io/TgWitness/fa/docs/reference/accounts/#account-json) بررسی کنید. |
| *فقط متادیتای API* | JSON فاقد جلسه است. فایل `.session` را اضافه کنید یا از تلفن/QR استفاده کنید. |
| *کلید رمزنگاری HEX باید شامل تمام ۵۱۲ کاراکتر هگزادسیمال باشد* | کلید کوتاه شده است یا حاوی `…` می‌باشد. |
| شناسه حساب با حساب واردشده مطابقت ندارد | شناسه کاربری فایل با آنچه تلگرام گزارش می‌کند متفاوت است؛ این فایل مربوط به حساب کاربری دیگری است. |
| حساب کاربری از قبل به فضای کاری دیگری تعلق دارد | به جای افزودن دوباره‌ی حساب، آن فضای کاری را باز کنید. |
| متصل است، اما یک گروه خصوصی در فهرست چت‌های **«منابع**» وجود ندارد. | عضویت را بررسی کنید. انتخابگر اولین ۱۰۰۰ دیالوگ را بازرسی می‌کند؛ محدودیت را در بخش **پارامترها** افزایش دهید. |
| اتصال پروکسی ناموفق است | مسیر و حالت آی‌پی را بررسی کنید. MTProxy خودکار ورودی دیگرِ کارا را امتحان می‌کند. «پنهان کردن آدرس در انتظار»؛ «راست‌زمانی» به‌عنوان آخرین راه‌حل می‌تواند پس از تأخیر تنظیم‌شده مستقیماً متصل شود. [حالت‌های مسیریابی را](https://phishdestroy.github.io/TgWitness/fa/docs/reference/connection/#ip-modes) ببینید. |

همچنین ببینید: [اتصال و امنیت](https://phishdestroy.github.io/TgWitness/fa/docs/reference/connection/) برای پروکسی‌ها و رمزگذاری، و [نحوه کارکرد جمع‌آوری](https://phishdestroy.github.io/TgWitness/fa/docs/reference/collection/) برای آنچه پس از ورود ثبت می‌شود.
