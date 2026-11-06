# اکاؤنٹس اور سیشن فارمیٹس

Canonical page: https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/

فون، QR کوڈ یا auth کلید کے ذریعے سائن ان کریں، Telethon، Pyrogram یا Telegram Desktop سیشنز کو امپورٹ کریں، اور متعدد اکاؤنٹس چلائیں۔

TgWitness MTProto کے ذریعے ایک **ٹیلیگرام صارف اکاؤنٹ** (بوٹ نہیں) کے طور پر سائن ان کرتا ہے، Telethon استعمال کرتے ہوئے۔ ہر اکاؤنٹ اپنے مخصوص **ورک اسپیس** (جسے API اور کمانڈ لائن ٹولز میں ورک *اسپیس* کہا جاتا ہے) میں موجود ہوتا ہے، جس کا اپنا سیشن، ذرائع، جرنل اور دستخطی کلید ہوتی ہے۔

سیشن فائلز، سیشن سٹرنگز اور آتھ کیز **اکاؤنٹ کی اجازت نامے** ہیں: جو بھی ان میں سے کسی کو اپنے پاس رکھے وہ اس اکاؤنٹ کے طور پر کام کر سکتا ہے۔ ان میں پیغامات کی تاریخ شامل نہیں ہوتی۔

> [!WARNING] **ایسی کوئی بھی چیز استعمال نہ کریں جسے آپ کھونے کا متحمل نہ ہو سکیں۔** ہم سختی سے مشورہ دیتے ہیں کہ ذاتی یا دیگر قیمتی اکاؤنٹس کو منسلک نہ کریں، اور کسی ایسے اکاؤنٹ پر API ID / API ہیش نہ بنائیں جسے آپ اہم سمجھتے ہوں۔ یہ اس بات کے بارے میں نہیں ہے کہ ٹی جی وٹنس (TgWitness) آزمایا ہوا نہیں ہے: ٹیلیگرام غیر متوقع طور پر اکاؤنٹس کو محدود اور مستقل طور پر بلاک کر دیتا ہے — ایسے درخواستوں کے حجم کے لیے جنہیں یہ ضرورت سے زیادہ سمجھتا ہے، چاہے کلائنٹ یا مقصد کچھ بھی ہو، اور اس کے لیے کوئی مناسب دستاویزات فراہم نہیں کرتا۔ بہت سے بلاک ناقابل واپسی ہوتے ہیں۔ مخصوص اکاؤنٹس استعمال کریں۔ ٹیسٹ رنز کا ہموار چلنا ٹیلیگرام پر منحصر ہے، نہ کہ سافٹ ویئر پر، اور مستقبل کے لیے کسی چیز کی ضمانت نہیں دیتا۔

- [ایک نظر میں](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#at-a-glance)
- [شروع کرنے سے پہلے: API ID اور API ہیش](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [فون نمبر](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#phone-number) · [کیو آر کوڈ](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#qr-code) · [آتھ کی + ڈی سی آئی ڈی](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#auth-key--dc-id)
- [اکاؤنٹ فائلیں](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#account-files): [ٹیلی تھون .سیشن](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#telethon-session) · [پائروگرام .سیشن](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#pyrogram-session) · [سیشن + JSON جوڑا](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#telegram-desktop-tdata) · [اسٹرنگ سیشن](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#telethon-stringsession) · [اکاؤنٹ JSON](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#account-json)
- [پہچانیں کہ آپ کے پاس کیا ہے](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#identify-what-you-have) · [غیر معاونت یافتہ فارمیٹس](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#unsupported-formats)
- [متعدد اکاؤنٹس](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#multiple-accounts) · [اکاؤنٹ فائلوں کو محفوظ رکھنا](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#keeping-account-files-safe) · [مسئلہ حل کرنا](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#troubleshooting)

## ایک نظر میں

| آپ کے پاس کیا ہے | **اکاؤنٹ شامل** کریں ٹیب | آپ کو یہ بھی درکار ہوگا |
| --- | --- | --- |
| فون نمبر اور اس کے لاگ ان کوڈز تک رسائی | **فون** | اگر فعال ہو تو 2FA پاس ورڈ |
| ٹیلیگرام دوسری ڈیوائس پر کھلا ہوا | **کیو آر کوڈ** | اگر فعال ہو تو 2FA پاس ورڈ |
| `.session`فائل (Telethon یا Pyrogram) | **فائلیں** | ایپ سیٹنگز کے لیے اختیاری JSON |
| `.session` + `.json` ایک ہی نام کے ساتھ | **فائلیں** (دونوں منتخب کریں) | عام طور پر کچھ نہیں |
| ٹیلیگرام ڈیسک ٹاپ کا `tdata` فولڈر | **فائلیں** (ZIP کے طور پر) | اگر ڈیسک ٹاپ کا مقامی پاس کوڈ مقرر ہو تو |
| ایک ٹیلی تھون سٹرنگ سیشن (متن، `.txt`، `.tgwitness-session`) | **فائلیں** | الگ API جوڑے کی ضرورت نہیں |
| `.json`، سیشن یا آتھ کی کے ساتھ | **فائلیں** | الگ API جوڑے کی ضرورت نہیں |
| ایک آتھ کی (512 ہیکس اکر) اور اس کا ڈی سی نمبر | **آتھ کی** | اختیاری صارف شناختی نام |

TgWitness فائلوں کو ان کے ناموں کی بجائے ان کے **مواد** کی بنیاد پر پہچانتا ہے۔ فائل کا نام تبدیل کرنے سے وہ کبھی تبدیل نہیں ہوتی۔

## شروع کرنے سے پہلے: API ID اور API ہیش

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

اپنی ایپلیکیشن استعمال کرنے کے لیے (اس اکاؤنٹ کو خطرہ ہے جس نے اسے رجسٹر کیا ہے؛ دیکھیں: [بلٹ ان API پول کیوں؟](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)):

1. اپنا [my.telegram.org](https://my.telegram.org) کھولیں اور اپنے کسی بھی فون نمبر سے سائن ان کریں۔ کوڈ Telegram ایپ میں آتا ہے، SMS کے ذریعے نہیں۔
2. **API ترقی کے اوزار** منتخب کریں۔
3. ایک ایپلیکیشن بنائیں: کوئی بھی عنوان اور مختصر نام (5–32 حروف)، پلیٹ فارم: **ڈیسک ٹاپ**۔ URL اور وضاحت خالی رہ سکتی ہیں۔
4. **ایپ کا api_id** (ایک عدد) اور **api_hash** (32 ہیکساڈیسمل حروف) کاپی کریں۔

پینل میں، سائن ان فارم کے نیچے اوپن **API ID + ہیش**۔ آپ ایک واحد `api_id:api_hash` جوڑا **API ID** میں پیسٹ کر سکتے ہیں اور دونوں فیلڈز بھر جائیں گے۔ ایک جوڑا آپ کے تمام اکاؤنٹس کے لیے استعمال کیا جا سکتا ہے۔ کامیاب لاگ ان کے بعد یہ محفوظ، انکرپٹڈ، صرف اسی ورک اسپیس میں ہوتا ہے اور کبھی بھی براؤزر کو واپس نہیں بھیجا جاتا۔

تین مختلف اسناد ملوث ہیں:

| خفیہ | کھولتا ہے | جہاں یہ موجود ہے |
| --- | --- | --- |
| پینل ٹوکن | ٹی جی وِٹنس ویب پینل | ڈیٹا ڈائریکٹری میں `panel-token.txt` یا `TGWITNESS_TOKEN` |
| API آئی ڈی + ہیش | اپنے آپ میں کچھ نہیں؛ ایپ کی شناخت کرتا ہے | بلٹ ان جوڑا، درآمد شدہ ترتیبات، یا my.telegram.org پر آپ کی اپنی ایپ |
| اکاؤنٹ کی اجازت | ٹیلیگرام اکاؤنٹ | فون/QR لاگ ان کے ذریعے تخلیق کیا گیا یا سیشن کے طور پر لایا گیا |

اگر ٹیلیگرام تک رسائی کے لیے پروکسی استعمال کرنا ضروری ہو تو پہلے **اکاؤنٹ → ترتیبات → کنکشن کی ترتیبات → کنکشن کا راستہ تبدیل کریں** میں سیٹ کریں۔

## فون نمبر

1. **اکاؤنٹ** کھولیں، **فون** ٹیب پر جائیں، اور نمبر بین الاقوامی فارمیٹ میں درج کریں، مثال کے طور پر `+44 7700 900123`۔ خالی جگہیں اور ڈیشز خود بخود ہٹا دیے جاتے ہیں۔
2. **جاری رکھیں پر** کلک کریں۔ API ID + ہیش خالی رہ سکتے ہیں۔
3. وہ کوڈ درج کریں جو ٹیلیگرام بھیجتا ہے (عموماً ٹیلیگرام ایپ میں؛ ایس ایم ایس کی ضمانت نہیں)۔
4. اگر اکاؤنٹ میں دو مرحلوں کی توثیق فعال ہے تو وہ پاس ورڈ درج کریں۔ یہ پینل ٹوکن یا ڈیوائس پاس کوڈ نہیں ہے۔
5. لاگ ان کے بعد دکھائی گئی اکاؤنٹ آئی ڈی چیک کریں، پھر ذرائع منتخب کریں۔

لاگ ان کوڈز اور 2FA پاس ورڈ کبھی بھی ڈسک پر محفوظ نہیں کیے جاتے۔

## کیو آر کوڈ

اس کا استعمال اس وقت کریں جب اکاؤنٹ پہلے ہی فون یا کسی دوسرے کمپیوٹر پر سائن ان ہو چکا ہو۔

1. **QR کوڈ** ٹیب → **QR کوڈ دکھائیں۔** API ID + ہیش خالی رہ سکتے ہیں۔
2. سائن ان شدہ ڈیوائس پر: **سیٹنگز → ڈیوائسز → ڈیسک ٹاپ ڈیوائس کو لنک کریں**، کوڈ اسکین کریں اور تصدیق کریں۔
3. اگر ٹیلیگرام درخواست کرے تو TgWitness میں 2FA پاس ورڈ درج کریں۔

QR تصویر مقامی طور پر تیار کی جاتی ہے۔ کوڈز کی میعاد ختم ہو جاتی ہے؛ دوبارہ کوشش کے لیے **'دوسرا QR کوڈ تیار کریں' پر** کلک کریں۔ پینل کو لاک کرنے، ورک اسپیس تبدیل کرنے یا دوسرا لاگ ان شروع کرنے سے زیر التواء کوڈ منسوخ ہو جاتا ہے۔

## آتھ کی + ڈی سی آئی ڈی

ایک آتھ کی ہر ٹیلیگرام سیشن کے پیچھے موجود خام 256 بائٹ کی اجازت ہے، جو **512 ہیکساڈیسمل حروف** میں لکھی جاتی ہے، ڈیٹا سینٹر نمبر **DC 1–5** کے ساتھ۔

1. ٹیب **'Auth key**'۔ مکمل کلید چسپاں کریں؛ ایک مختصر کلید جس میں صرف '`…`' شامل ہو، کام نہیں کرے گی۔
2. کلیدی کے ساتھ فراہم کردہ DC ID منتخب کریں۔
3. اختیاری طور پر **صارف** کی**شناخت** درج کریں۔ اگر ٹیلیگرام مختلف اکاؤنٹ رپورٹ کرے تو TgWitness کنکشن سے انکار کر دے گا۔
4. پریس **کنیکٹ اکاؤنٹ**۔

ایک آتھ کی (512 حروف) API ہیش (32 حروف) نہیں ہے۔ اسی کلید کو JSON کے طور پر بھی درآمد کیا جا سکتا ہے، دیکھیں [اکاؤنٹ JSON](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#account-json)۔

## اکاؤنٹ فائلیں

اوپن کریں، **Add account → Files پر جائیں** اور **ایک اکاؤنٹ سے تعلق رکھنے والی** زیادہ سے زیادہ **چار فائلیں** (کل **8 MiB**) منتخب کریں، پھر **Connect account** دبائیں۔

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- فائلیں آپ کے TgWitness سرور کی **میموری میں** تبدیل کی جاتی ہیں۔ اپلوڈز محفوظ نہیں کیے جاتے، ZIP فائلیں ڈسک پر نکالی نہیں جاتیں اور کسی بیرونی سروس سے رابطہ نہیں کیا جاتا۔
- پیدا ہونے والے سیشن کو پھر ٹیلیگرام کے ساتھ چیک کیا جاتا ہے۔ اگر کسی فائل میں صارف کی شناخت (یوزر آئی ڈی) درج ہو، تو اسے ٹیلیگرام کے رپورٹ کردہ اکاؤنٹ سے میل کھانا چاہیے۔
- وہ فائلیں جو مختلف اکاؤنٹس یا مختلف API کریڈنلز کو بیان کرتی ہیں مسترد کر دی جاتی ہیں ایک کو منتخب کرنے کے بجائے۔
- **پاس کوڈ یا سیشن ٹیکسٹ** میں TData کا مقامی پاس کوڈ فیلڈ ہوتا ہے، ایک باکس جہاں آپ **بغیر سائن ان کیے** StringSession اور **Read**فائلیں پیسٹ کر سکتے ہیں (یہ فارم ٹیلیگرام سے رابطہ کیے بغیر مکمل کرتا ہے).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

### ٹیلی تھون `.session`

|  |  |
| --- | --- |
| یہ کیا ہے | SQLite ڈیٹا بیس جو Telethon پر مبنی ٹولز بناتے ہیں، مثال کے طور پر `my_account.session` |
| کی طرف سے تسلیم شدہ | جدول `sessions` (`dc_id`، `server_address`، `port`، `auth_key`) اور `version` = 7 یا 8 |
| ضروریات | بالکل ایک مجاز سیشن قطار؛ ایک بند، مکمل ڈیٹا بیس |

سب سے پہلے اس پروگرام کو بند کریں جس نے فائل بنائی تھی۔ اگر اس کے ساتھ `my_account.session-journal` یا `my_account.session-wal` موجود ہے تو ڈیٹا بیس حتمی نہیں ہوا ہے: اصل کلائنٹ کو صاف طریقے سے کھولیں اور بند کریں۔ ان سائیڈ کار فائلوں کو حذف کرنے سے ایک خراب کاپی رہ سکتی ہے۔

### پائروگرام `.session`

|  |  |
| --- | --- |
| یہ کیا ہے | SQLite ڈیٹا بیس جو Pyrogram پر مبنی ٹولز بناتے ہیں |
| کی طرف سے تسلیم شدہ | `sessions` کو `dc_id`، `auth_key`، `test_mode`، `user_id`، `is_bot` کے ساتھ جدول کریں؛ `version` = 2 یا 3 |
| ضروریات | پروڈکشن نیٹ ورک پر ایک مجاز **صارف** سیشن۔ بوٹ اور ٹیسٹ-ڈی سی سیشنز مسترد کر دیے جاتے ہیں۔ |

محفوظ شدہ صارف آئی ڈی کو لاگ ان کے دوران ٹیلیگرام کے خلاف چیک کیا جاتا ہے۔

### سیشن + JSON جوڑا

اکاؤنٹس اکثر ایک ہی نام کی دو فائلوں کی صورت میں تقسیم کیے جاتے ہیں، مثال کے طور پر `447700900123.session` اور `447700900123.json`۔ **دونوں کو** ایک ساتھ منتخب کریں۔

- JSON سے، TgWitness `app_id`/`api_id` اور `app_hash`/`api_hash` استعمال کرتا ہے، لہٰذا آپ کو عام طور پر API کی کریڈینشلز ٹائپ کرنے کی ضرورت نہیں پڑتی۔
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#account-json).

### ٹیلیگرام ڈیسک ٹاپ (TData)

TData ٹیلیگرام ڈیسک ٹاپ ایپلیکیشن کا`tdata` فولڈر ہے (desktop.telegram.org سے دستیاب کراس پلیٹ فارم ایپ)۔

| نظام | ڈیفالٹ`tdata`مقام |
| --- | --- |
| ونڈوز | `%APPDATA%\Telegram Desktop\tdata` (پورٹیبل ٹیلیگرام: `Telegram.exe` کے ساتھ) |
| لینکس | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

اسے درآمد کرنے کے لیے:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> یہ درآمد شدہ پر بھی لاگو ہوتا ہے۔ `.session` فائلیں، StringSession ٹیکسٹ اور Auth Key HEX۔ دیگر کلائنٹس جن کے پاس اپنی آزادانہ طور پر بنائی گئی اجازتیں ہیں، وہ سائن ان رہ سکتے ہیں۔ [Telegram کی AUTH_KEY_DUPLICATED دستاویزات](https://core.telegram.org/api/errors#406-not-acceptable) دیکھیں۔

1. Telegram Desktop کو مکمل طور پر بند کر دیں۔
2. `tdata` سے **صرف** ان دو آئٹمز پر مشتمل ایک ZIP بنائیں:

   - `key_datas`
   - 16 حروف پر مشتمل فائل جو `s` پر ختم ہوتی ہے، اس کے ساتھ، عام طور پر `D877F783D5D3EF8Cs`

   میڈیا کیش کے ساتھ پورے فولڈر کو زپ کرنے سے عام طور پر حدیں (512 اندراجات، 32 MiB بغیر پیک) پار ہو جاتی ہیں۔ 3. **فائلز** میں زپ کو منتخب کریں۔ اگر ٹیلیگرام ڈیسک ٹاپ کا کوئی **مقامی پاس کوڈ** ہے تو پہلے اسے **پاس کوڈ یا سیشن ٹیکسٹ** کے تحت درج کریں۔ یہ 2FA پاس ورڈ نہیں ہے۔

مدد یافتہ: ہر آرکائیو میں ایک اکاؤنٹ، جدید `key_datas`/`key_data0`/`key_data1` اسٹوریج، مقامی پاس کوڈ۔ غیر مدد یافتہ: متعدد لاگ ان شدہ اکاؤنٹس والے فولڈرز، پرانے ڈیسک ٹاپ لی آؤٹس، پاس ورڈ سے محفوظ شدہ ZIPs، اور الگ نیٹیو macOS ایپ "Telegram for macOS"۔

### ٹیلی تھون سٹرنگ سیشن

ایک سطر پر مشتمل متن، عام طور پر `1` سے شروع ہوتا ہے اور تقریباً 350 حروف پر مشتمل ہوتا ہے۔ اسے `.txt` یا `.tgwitness-session` فائل (زیادہ سے زیادہ 4 KiB) کے طور پر لوڈ کریں، یا **پاس کوڈ یا سیشن ٹیکسٹ** کے تحت پیسٹ کریں۔ صرف Telethon سٹرنگز قبول کی جاتی ہیں؛ Pyrogram اور TDLib سٹرنگز مختلف فارمیٹس استعمال کرتی ہیں۔

### اکاؤنٹ JSON

ایک JSON آبجیکٹ، زیادہ سے زیادہ **64 KiB**، ایک فائل میں جو **`.json`** پر ختم ہوتی ہے۔

| میدان (عرف) | معنی |
| --- | --- |
| `api_id` (`app_id`) | ایپلیکیشن آئی ڈی، ایک مثبت عدد |
| `api_hash` (`app_hash`) | ایپلیکیشن ہیش، 32 ہیکساڈیسمل اعداد |
| `string_session` (`session_string`, `session_str`; legacy `session`) | Telethon StringSession متن ہے، فائل کا نام نہیں |
| `auth_key` (`auth_key_hex`) + `dc_id` | 512 حروف پر مشتمل Auth Key اور DC 1–5 مکمل کریں۔ |
| `user_id` (`id`) | اختیاری؛ اجازت محفوظ ہونے سے پہلے ٹیلیگرام کے خلاف چیک کیا جاتا ہے۔ |
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

پہلی مثال صرف API کی اسناد بھرتی ہے؛ فون یا QR کے ذریعے سائن ان کریں، یا سیشن فائل شامل کریں۔ بلک لسٹس (اکاؤنٹس کی JSON اری) قبول نہیں کی جاتیں۔

## پہچانیں کہ آپ کے پاس کیا ہے

| آپ دیکھتے ہیں | یہ ہے | استعمال کریں |
| --- | --- | --- |
| `*.session`؛ اسے ٹیکسٹ ایڈیٹر میں کھولنے پر اوپر `SQLite format 3` دکھائی دیتا ہے | Telethon یا Pyrogram SQLite | **فائلیں** (خودکار طور پر شناخت شدہ) |
| `tdata` فولڈر جس میں `key_datas` شامل ہے۔ | ٹیلیگرام ڈیسک ٹاپ ٹی ڈیٹا | دو فائلوں کو ZIP کریں، پھر **فائلیں** |
| `1` سے شروع ہونے والی ایک ٹیکسٹ لائن، تقریباً 350 حروف | ٹیلی تھون سٹرنگ سیشن | **فائلیں** |
| `*.json` کے ساتھ `app_id`/`app_hash` | متعلقہ میٹا ڈیٹا | **فائلیں**، اس کے سیشن کے ساتھ |
| `*.json` کے ساتھ `auth_key` یا `string_session` | اکاؤنٹ JSON | **فائلیں** |
| 512 حروف `0-9a-f` | آتھ کی | **آتھ کی** |
| 32 حروف `0-9a-f` | API ہیش | **API آئی ڈی + ہیش** |
| `td.binlog` یا `db.sqlite`، TDLib ایپ سے | TDLib اسٹوریج | مدد فراہم نہیں کی جاتی |
| `123456789:AA…` | بوٹ ٹوکن | مدد فراہم نہیں کی جاتی |

## غیر معاونت یافتہ فارمیٹس

| فارمیٹ | متبادل |
| --- | --- |
| TDLib اسٹوریج (`td.binlog`) اور TDLib ایکسپورٹس | فون یا QR کے ذریعے سائن ان کریں |
| پائروگرام سیشن **سٹرنگز** | Pyrogram فائل `.session` استعمال کریں، یا فون/QR |
| TData متعدد لاگ ان شدہ اکاؤنٹس کے ساتھ | Telegram Desktop میں دوسرے اکاؤنٹس سے لاگ آؤٹ کریں، یا ہر اکاؤنٹ کی اپنی سیشن فائل استعمال کریں۔ |
| بوٹ ٹوکنز | مدد نہیں کی جاتی: TgWitness صارف اکاؤنٹ کے طور پر مشاہدہ کرتا ہے |
| متعدد اکاؤنٹس کی CSV/JSON فہرستیں | **اکاؤنٹس → اکاؤنٹس درآمد کریں** کے ذریعے معاونت یافتہ سیشن فائلیں درآمد کریں، یا الگ ورک اسپیسز میں فون/QR کے ذریعے سائن ان کریں |
| ٹیسٹ-ڈی سی یا بوٹ سیشنز | پروڈکشن صارف اکاؤنٹ استعمال کریں |

## متعدد اکاؤنٹس

اکاؤنٹ منتخب کرنے والے کے پاس **+** دبائیں، یا کھولیں **اکاؤنٹ → ترتیبات → کنکشن کی ترتیبات → ورک اسپیسز**، ایک لیبل درج کریں اور سائن ان کریں۔

- کسی بھی تعداد میں ورک اسپیسز، بشمول مرکزی ورک اسپیس۔ ہر ایک کا اپنا سیشن، پروکسی روٹ، ذرائع، کیپچر پالیسی، جرنل، دستخطی کلید، چیک پوائنٹس اور ایکسپورٹس ہوتے ہیں۔
- ڈسپلے شدہ ورک اسپیس تبدیل کرنے سے دوسرے ورک اسپیس معطل نہیں ہوتے۔
- ایک جرنل ہمیشہ اُس اکاؤنٹ سے منسلک رہتا ہے جس نے اسے تخلیق کیا۔ مختلف اکاؤنٹ کے طور پر سائن ان کرنے کے لیے ایک الگ ورک اسپیس درکار ہوتا ہے، اور ایک اکاؤنٹ دو ورک اسپیسز میں تفویض نہیں کیا جا سکتا۔
- مین پینل ٹوکن تمام ورک اسپیسز کو کنٹرول کرتا ہے۔ [جاری کردہ رسائی](https://phishdestroy.github.io/TgWitness/ur/docs/reference/access/) دوسروں کو منتخب اکاؤنٹس اور چیٹس تک محدود کر سکتی ہے، الگ الگ اجازتوں اور سیشن کی حدوں کے ساتھ۔
- **اکاؤنٹس** ایک ورک اسپیس کا نام تبدیل کرتا ہے اور ایک اضافی ورک اسپیس کو اس کے سیشن، جرنل، ذرائع اور دستخطی کلید سمیت حذف کر دیتا ہے۔ مرکزی ورک اسپیس کو پینل سے حذف نہیں کیا جا سکتا۔

### اجتماعی درآمد اور اکاؤنٹ گروپس

**اکاؤنٹس → اکاؤنٹس امپورٹ** کریں تاکہ متعدد اکاؤنٹس شامل کیے جائیں، فائلوں کو بیس نام کے ذریعے جوڑیں اور ہر لاگ ان کا نتیجہ دیکھیں۔ ہر اکاؤنٹ کو اپنا ورک اسپیس ملتا ہے۔

ایک گروپ متعلقہ اکاؤنٹس کو ان کے سیشنز، کیز یا شواہد کو ضم کیے بغیر ایک ساتھ رکھتا ہے۔ **اکاؤنٹس** پر **گروپ کھولنے** سے اس کا صفحہ کھل جاتا ہے `/groups/<id>`:

- **اکاؤنٹس:** ہر رکن کا کنکشن راستہ، مشاہدہ اور آخری پیغام، کے ساتھ **سب** شروع کریں اور **سب کو معطل کریں**۔
- **توجہ درکار ہے:** وہ اکاؤنٹس جن سے سائن آؤٹ کیا گیا ہے، دستیاب نہیں ہیں یا جن میں کنکشن، انٹیک، ماخذ یا میڈیا کا مسئلہ ہے؛ ہر نام اس کے کارڈ کی طرف لے جاتا ہے۔
- **کئی اکاؤنٹس کی چیٹس دیکھیں:** مشترکہ ذرائع، انہیں دیکھنے والے اکاؤنٹس اور دستیاب ورک اسپیس-مشاہداتی مدت (سات دن تک) میں خلل۔ **N اکاؤنٹس کے ساتھ ایکسپورٹ** ایک چینل یا سپر گروپ کے ایکسپورٹ کو ان کے درمیان تقسیم کرتا ہے اور ایک آرکائیو پر دستخط کرتا ہے۔
- **گروپ کی برآمد:** ایک ZIP، جس کے تحت ہر اکاؤنٹ کا دستخط شدہ ایکسپورٹ موجود ہے۔ `accounts/` اور `manifest.json` ان کے SHA-256 اور کلید کے فنگر پرنٹس کی فہرست، جو مرکزی ورک اسپیس میں دستخط شدہ ہیں `manifest.signature.json`۔ ہر اکاؤنٹ آرکائیو کو اس کے اپنے ساتھ تصدیق کریں `python -m tgwitness.verify` اور اس اکاؤنٹ کے معتبر فنگر پرنٹ کے ساتھ۔

ارکان گروپ کی ترتیبات شیئر کرتے ہیں؛ ایک اکاؤنٹ اپنی مخصوص قدریں برقرار رکھ سکتا ہے۔ [مشترکہ ترتیبات](https://phishdestroy.github.io/TgWitness/ur/docs/reference/settings/#account-groups)، [امپورٹ اور گروپس گائیڈ](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) دیکھیں اور [MTProxy پول ڈیش بورڈ](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources)۔

## سائن آؤٹ

**اکاؤنٹ → ٹیلیگرام سے سائن آؤٹ کریں** (مشاہدہ معطل کے ساتھ) ٹیلیگرام سے سیشن ختم کرنے کی درخواست کرتا ہے، لہٰذا یہ اکاؤنٹ کی **سیٹنگز → ڈیوائسز** سے بھی غائب ہو جاتا ہے، اور ورک اسپیس والٹ سے سیشن کو ہٹا دیتا ہے۔ جرنل، ذرائع، سیٹنگز اور سگننگ کی موجود رہتی ہیں، اور جرنل سائن آؤٹ کو ریکارڈ کرتا ہے۔ ورک اسپیس اب بھی اپنے اکاؤنٹ کا ہی ہے: صرف وہی اکاؤنٹ دوبارہ اس سے کنیکٹ ہو سکتا ہے۔ اگر ٹیلیگرام جواب نہیں دیتا، تو سیشن یہاں سے پھر بھی ہٹا دیا جاتا ہے اور پینل اس کی اطلاع دیتا ہے؛ اسے ٹیلیگرام میں **Settings → Devices** کے تحت ختم کریں۔

## اکاؤنٹ فائلوں کو محفوظ رکھنا

- ہر `.session`، TData ZIP، StringSession، Auth Key اور اکاؤنٹ JSON کو پاس ورڈ کی طرح سمجھیں۔ TgWitness درآمد شدہ اجازت کو اپنے خفیہ کردہ والٹ میں محفوظ رکھتا ہے؛ آپ بعد میں اصل فائلیں حذف کر سکتے ہیں۔
- ایک ہی اجازت نامہ ایک ساتھ دو پروگراموں میں چلانے کی کوشش نہ کریں۔ ٹیلیگرام اسے منسوخ کر سکتا ہے (`AUTH_KEY_DUPLICATED`)، اور دونوں نقول کام کرنا بند کر دیں گی۔
- ایک ختم شدہ یا منسوخ شدہ سیشن کو تبدیلی کے ذریعے دوبارہ بحال نہیں کیا جا سکتا۔ دوبارہ سائن ان کریں۔

## مسئلہ حل کرنا

| پیغام یا علامت | کیا کرنا ہے |
| --- | --- |
| *اس سیشن کو پڑھا نہیں جا سکتا۔ اس کے اصل کلائنٹ کو بند کریں…* | SQLite فائل کھلی یا نامکمل ہے (`-journal`/`-wal` سائیڈ کار). اصل پروگرام کو صاف طریقے سے بند کریں اور فائل کو دوبارہ کاپی کریں۔ |
| *Telethon SQLite سکیمے جن کی حمایت کی جاتی ہے: 7 اور 8* / *پائروگرام … 2 اور 3* | فائل ایک بہت پرانی یا نامعلوم لائبریری ورژن نے بنائی۔ اس کے بجائے فون/QR کے ذریعے سائن ان کریں۔ |
| *صرف مجاز پروڈکشن صارف سیشنز کی حمایت کی جاتی ہے۔* | Pyrogram فائل کسی بوٹ یا ٹیسٹ نیٹ ورک سے تعلق رکھتی ہے۔ |
| *TData آرکائیو 512 اندراجات یا 32 MiB سے تجاوز کر گیا ہے۔* | صرف ZIP کریں `key_datas` اور `D877F783D5D3EF8Cs`، پورا فولڈر نہیں۔ |
| *TData کو ڈیکرپٹ نہیں کیا جا سکتا۔ ڈیسک ٹاپ کا مقامی پاس کوڈ چیک کریں۔* | Telegram Desktop کا مقامی پاس کوڈ **Passcode یا سیشن ٹیکسٹ** کے تحت درج کریں۔ |
| *ایک وقت میں ایک TData اکاؤنٹ درآمد کریں* | Telegram Desktop کے متعدد اکاؤنٹس تھے؛ [غیر معاونت یافتہ فارمیٹس](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#unsupported-formats) دیکھیں۔ |
| *منتخب فائلیں مختلف اکاؤنٹس یا API کی اسناد بیان کرتی ہیں۔* | صرف ایک اکاؤنٹ کی فائلیں منتخب کریں۔ |
| *JSON میں کوئی سپورٹڈ API کریڈینشلز یا اجازت نامہ شامل نہیں ہے۔* | [اکاؤنٹ JSON](https://phishdestroy.github.io/TgWitness/ur/docs/reference/accounts/#account-json) میں فیلڈ کے نام چیک کریں۔ |
| *صرف API میٹا ڈیٹا* | JSON میں کوئی سیشن نہیں ہے۔`.session` فائل شامل کریں یا فون/QR استعمال کریں۔ |
| *Auth Key HEX میں تمام 512 ہیکساڈیسمل اعداد شامل ہونے چاہئیں۔* | کلیدی ٹکڑے میں چھانٹی گئی ہے یا اس میں `…` شامل ہے۔ |
| اکاؤنٹ آئی ڈی درآمد شدہ اکاؤنٹ سے مطابقت نہیں رکھتی | فائل کا صارف آئی ڈی ٹیلیگرام کی رپورٹ کردہ معلومات سے مختلف ہے؛ یہ فائل کسی دوسرے اکاؤنٹ کے لیے ہے۔ |
| اکاؤنٹ پہلے ہی کسی دوسرے ورک اسپیس کا حصہ ہے۔ | اکاؤنٹ کو دو بار شامل کرنے کے بجائے اس ورک اسپیس کو کھولیں۔ |
| منسلک ہے، لیکن **Sources** میں چیٹ لسٹ سے ایک نجی گروپ غائب ہے۔ | رکنیت چیک کریں۔ پِکر پہلے 1,000 ڈائیلاگز کا معائنہ کرتا ہے؛ **پیرامیٹرز** میں حد بڑھائیں۔ |
| پراکسی کنکشن ناکام | روٹ اور آئی پی موڈ چیک کریں۔ خودکار MTProxy ایک اور قابلِ عمل اندراج آزمائیں۔ 'ایڈریس چھپائیں' انتظار کرتا ہے؛ 'براہِ راست' آخری چارہ کے طور پر متعین کردہ تاخیر کے بعد براہِ راست کنکٹ کر سکتا ہے۔ [روٹنگ موڈز](https://phishdestroy.github.io/TgWitness/ur/docs/reference/connection/#ip-modes) دیکھیں۔ |

مزید دیکھیں: پروکسیز اور انکرپشن کے لیے [کنکشن اور سیکیورٹی](https://phishdestroy.github.io/TgWitness/ur/docs/reference/connection/)، اور سائن ان کے بعد کیا جمع کیا جاتا ہے اس کے لیے [کلیکشن کیسے کام کرتی](https://phishdestroy.github.io/TgWitness/ur/docs/reference/collection/) ہے۔
