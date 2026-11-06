# Hisoblar va sessiya formatlari

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/

Telefon, QR kod yoki avtorizatsiya kaliti orqali tizimga kiring, Telethon, Pyrogram yoki Telegram Desktop sessiyalarini import qiling va bir nechta akkauntlarni boshqaring.

TgWitness **Telegram foydalanuvchi**hisobiga (bot emas) MTProto orqali Telethon yordamida kiradi. Har bir hisob o'zining alohida **ish** maydonida (API va buyruq qatori vositalarida "*workspace*" deb ataladi) joylashadi, o'z sessiyasi, manbalari, jurnali va imzolash kalitiga ega.

Sessiya fayllari, sessiya satrlari va Auth kalitlari **hisob ma'lumotlari ruxsatnomalaridir**: ularni egallagan har kim o'sha hisob sifatida harakat qilishi mumkin. Ular xabarlar tarixini o'z ichiga olmaydi.

> [!OGOHLANTIRISH] **Yo'qotishga qodir bo'lmagan narsani ishlatmang.** Shaxsiy yoki boshqa qimmatli hisoblarni ulashni va qadrlaydigan hisobingizda API ID / API xesh yaratishni qat'iyan tavsiya qilmaymiz. Bu TgWitness sinovdan o'tmaganligi haqida emas: Telegram hisoblarni oldindan aytib bo'lmaydigan tarzda cheklaydi va doimiy ravishda taqiqlaydi — u ortiqcha deb hisoblaydigan so'rov hajmlari uchun, mijoz yoki maqsadga qaramasdan, yetarli hujjatlashtirishsiz. Ko'plab taqiqlar qaytarib bo'lmaydi. Maxsus hisoblardan foydalaning. Sinovlarning muammosiz o'tishi Telegramga bog'liq, dasturiy ta'minotga emas, va keyinchalik hech narsani kafolatlamaydi.

- [Bir qarashda](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#at-a-glance)
- [Boshlashdan oldin: API ID va API xesh](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Telefon raqami](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#phone-number) · [QR kod](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#qr-code) · [Auth kaliti + DC identifikatori](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#auth-key--dc-id)
- [Hisob fayllari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#pyrogram-session) · [Sessiya + JSON juftligi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#telethon-stringsession) · [Hisob JSON](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#account-json)
- [Nimangiz borligini aniqlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#identify-what-you-have) · [Qo'llab-quvvatlanmaydigan formatlar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#unsupported-formats)
- [Bir nechta hisoblar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#multiple-accounts) · [Hisob fayllarini xavfsiz saqlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#keeping-account-files-safe) · [Muammolarni bartaraf etish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#troubleshooting)

## Bir qarashda

| Sizda nima bor | **Hisob qo'shish** yorlig'i | Shuningdek, sizga quyidagilar ham kerak bo'ladi |
| --- | --- | --- |
| Telefon raqami va uning kirish kodlariga kirish | **Telefon** | Agar yoqilgan bo'lsa, 2FA paroli |
| Telegram boshqa qurilmada ochiq | **QR kod** | Agar yoqilgan bo'lsa, 2FA paroli |
| `.session` fayli (Telethon yoki Pyrogram) | **Fayllar** | Ilova sozlamalari uchun ixtiyoriy hamroh JSON |
| `.session` va `.json`, bir xil nomga ega | **Fayllar** (ikkalasini ham tanlang) | Odatda boshqa hech narsa |
| `tdata` uchun Telegram Desktop papkasi | **Fayllar** (ZIP ko'rinishida) | Agar belgilangan bo'lsa, ish stoli mahalliy paroli |
| Telethon StringSession (matn, `.txt`, `.tgwitness-session`) | **Fayllar** | Alohida API juftligi talab etilmaydi |
| `.json` sessiya yoki Auth kaliti bilan | **Fayllar** | Alohida API juftligi talab etilmaydi |
| Auth kaliti (512 geksadetsimal belgilar) va uning DC raqami | **Auth kaliti** | Ixtiyoriy foydalanuvchi ID |

TgWitness fayllarni ularning nomiga qarab emas, **mazmuniga** qarab aniqlaydi. Fayl nomini o'zgartirish uni hech qachon konvertatsiya qilmaydi.

## Boshlashdan oldin: API ID va API xesh

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

Buning o'rniga o'zingizning ilovangizdan foydalanish uchun (ilovani ro'yxatdan o'tkazgan hisob xavf ostida; [Qo'shimcha API havzasi nima uchun?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account) bo'limiga qarang):

1. [my.telegram.org saytini](https://my.telegram.org) oching va o'zingizga tegishli istalgan telefon raqami bilan tizimga kiring. Kod Telegram ilovasiga keladi, SMS orqali emas.
2. **API ishlab chiqish vositalarini** tanlang.
3. Ilova yarating: istalgan sarlavha va qisqa nom (5–32 harf), platforma: **ish stoli**. URL va tavsif bo'sh qoldirilishi mumkin.
4. **App api_id** (raqam) va **App api_hash** (32 geksadesimal belgilar) nusxasini oling.

Panelda kirish formasining ostida ochiq **API ID va Hashni** ko'ring. Siz bitta `api_id:api_hash` juftligini **API ID**ga joylashtirishingiz mumkin va ikkala maydon ham to'ldiriladi. Bir juftlik barcha hisoblaringiz uchun ishlatilishi mumkin. Muvaffaqiyatli tizimga kirgandan so'ng u faqat shu ish maydonida shifrlangan holda saqlanadi va hech qachon brauzerga qaytmaydi.

Uch xil turdagi akkaunt ma'lumotlari ishtirok etadi:

| Maxfiy | Ochiladi | Joylashuvi |
| --- | --- | --- |
| Panel tokeni | TgWitness veb-paneli | Ma'lumotlar katalogida `panel-token.txt` yoki `TGWITNESS_TOKEN` |
| API ID + xesh | O'zi hech narsa emas; ilovani aniqlaydi | O'rnatilgan juftlik, import qilingan sozlamalar yoki my.telegram.org saytida o'zingizning ilovangiz |
| Hisobni avtorizatsiya qilish | Telegram akkaunti | Telefon/QR logini orqali yaratilgan yoki sessiya sifatida olib kelingan |

Agar Telegramga proksi orqali ulanish kerak bo'lsa, avvalo **Hisob → Sozlamalar → Ulanish sozlamalari → Ulanish yo'nalishini o'zgartirish** bo'limida sozlang.

## Telefon raqami

1. **Hisobni** oching, **"Telefon**" yorlig'iga o'ting va raqamni xalqaro formatda kiriting, masalan, `+44 7700 900123`. Bo'shliqlar va chiziqchalar avtomatik ravishda olib tashlanadi.
2. **Davom etish tugmasini** bosing. API ID va Hash bo'sh qoldirilishi mumkin.
3. Telegram yuboradigan kodni kiriting (odatda Telegram ilovasiga; SMS kafolatlanmaydi).
4. Agar akkauntda ikki bosqichli tasdiqlash yoqilgan bo'lsa, o'sha parolni kiriting. Bu panel tokeni yoki qurilma paroli emas.
5. Kirishdan so'ng ko'rsatilgan hisob IDni tekshiring, so'ng manbalarni tanlang.

Kirish kodlari va 2FA paroli hech qachon diskka yozilmaydi.

## QR kod

Hisob allaqachon telefon yoki boshqa kompyuterda tizimga kirgan bo'lsa, buni ishlating.

1. **QR kod** yorlig'i → **QR kodni ko'rsatish**. API ID va Hash bo'sh qoldirilishi mumkin.
2. Kirish qilingan qurilmada: **Sozlamalar → Qurilmalar → Desktop qurilmasini bog'lash**, kodni skanerlang va tasdiqlang.
3. Telegram so'rasa, TgWitness'ga 2FA parolini kiriting.

QR tasviri mahalliy ravishda yaratiladi. Kodlarning amal qilish muddati tugaydi; qayta urinib ko'rish uchun **"Yana bir QR kod yaratish"** tugmasini bosing. Panelni qulflash, ish maydonini almashtirish yoki boshqa kirishni boshlash kutib turgan kodni bekor qiladi.

## Auth kaliti + DC identifikatori

Auth kaliti har bir Telegram sessiyasining asosiy 256 baytli ruxsat kalitidir, u **512 geksadesimal**belgida, ma'lumot markazi raqami **DC 1–5** bilan birga yozilgan.

1. Tab **Auth kaliti**. To'liq kalitni joylashtiring; `…`ni o'z ichiga olgan qisqartirilgan kalit ishlamaydi.
2. Kalit bilan birga taqdim etilgan DC ID ni tanlang.
3. Ixtiyoriy ravishda **Foydalanuvchi ID**-ni kiriting. Agar Telegram boshqa hisobni xabar qilsa, TgWitness ulanishni rad etadi.
4. **Connect hisobini** bosing.

Auth kaliti (512 belgili) API xeshidan (32 belgili) farq qiladi. Xuddi shu kalitni JSON shaklida ham import qilish mumkin, qarang: [Hisob JSON](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#account-json).

## Hisob fayllari

**Hisobga qo'shish → Fayllar** bo'limiga o'ting va **bitta hisobga tegishli**, jami **8 MiB** gacha bo'lgan to'**rt**ta**faylni** tanlang, so'ng **Hisobni bog'lash tugmasini** bosing.

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- Fayllar TgWitness serveringiz **xotirasida** konvertlanadi. Yuklamalar saqlanmaydi, ZIP arxivlari diskka chiqarilmaydi va hech qanday tashqi xizmatga murojaat qilinmaydi.
- Olingan sessiya keyin Telegram bilan tekshiriladi. Agar faylda foydalanuvchi ID ko'rsatilgan bo'lsa, u Telegram xabar qiladigan hisobga mos kelishi kerak.
- Turli hisoblar yoki turli API ma'lumotlarini tasvirlovchi fayllar qabul qilinmaydi ularning birini tanlash o'rniga.
- **Parol yoki sessiya matni** TData mahalliy parol maydonini o'z ichiga oladi, u StringSession va **Read**fayllarini**imzolamasdan**joylashtirish uchun mo'ljallangan qutidir (Telegram bilan bog'lanmasdan shaklni to'ldiradi).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

### Telethon `.session`

|  |  |
| --- | --- |
| Bu nima | SQLite ma'lumotlar bazasi Telethon asosidagi vositalar tomonidan yaratiladi, masalan `my_account.session` |
| Tomonidan tan olingan | Jadvalar`sessions` (`dc_id`, `server_address`, `port`, `auth_key`) va `version` = 7 yoki 8 |
| Talablar | Aniq bir ruxsat berilgan sessiya qatori; yopiq, to'liq ma'lumotlar bazasi |

Avvalo faylni yaratgan dasturni yoping. Agar uning yonida `my_account.session-journal` yoki `my_account.session-wal` mavjud bo'lsa, ma'lumotlar bazasi yakunlanmagan: asl klientni toza ochib, toza yoping. Ushbu yon fayllarni o'chirish buzilgan nusxa qoldirishi mumkin.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Bu nima | SQLite ma'lumotlar bazasi Pyrogram asosidagi vositalar yaratadi |
| Tomonidan tan olingan | `sessions` va `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 yoki 3 |
| Talablar | Ishlab chiqarish tarmog'ida bitta ruxsat etilgan **foydalanuvchi** sessiyasi. Bot va test-DC sessiyalari rad etiladi |

Saqlangan foydalanuvchi identifikatori tizimga kirish paytida Telegram bilan tekshiriladi.

### Sessiya + JSON juftligi

Hisoblar ko'pincha bir xil nomga ega ikki fayl ko'rinishida tarqatiladi, masalan `447700900123.session` va `447700900123.json`. **Ikkalasini** bir vaqtda tanlang.

- JSONdan TgWitness `app_id`/`api_id` va `app_hash`/`api_hash` ni ishlatadi, shuning uchun odatda API ma'lumotlarini kiritishingiz shart emas.
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData — bu Telegram Desktop ilovasining (desktop.telegram.org saytidan olingan ko'p platformali ilova) `tdata` papkasi.

| Tizim | `tdata` bo'yicha standart joylashuv |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (portativ Telegram: `Telegram.exe` yonida) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Uni import qilish uchun:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> Bu shuningdek import qilingan `.session` fayllariga, StringSession matni va Auth Key HEX ga ham tegishli. O'zining mustaqil yaratilgan ruxsatnomalariga ega boshqa mijozlar ham tizimga kirgan holda qolishi mumkin. [Telegramning AUTH_KEY_DUPLICATED hujjatlarini](https://core.telegram.org/api/errors#406-not-acceptable) ko'ring.

1. Telegram Desktop'dan to'liq chiqing.
2. `tdata`-dan **faqat** ushbu ikkita elementni o'z ichiga olgan ZIP yarating:

   - `key_datas`
   - `s` bilan tugaydigan 16 belgili fayl yonida, odatda `D877F783D5D3EF8Cs`

   Media keshini o'z ichiga olgan butun papkani siqib yuborish odatda limitlardan oshadi (512 ta yozuv, 32 MiB ochilmagan holatda). 3. Fayllarda ZIP-ni tanlang. Agar Telegram Desktop'da **mahalliy parol** bo'lsa, avvalo uni **Passcode yoki sessiya matni** satriga kiriting. Bu 2FA paroli emas.

Qo'llab-quvvatlanadi: har bir arxiv uchun bitta hisob, zamonaviy `key_datas`/`key_data0`/`key_data1` saqlash, mahalliy parol. Qo'llab-quvvatlanmaydi: bir nechta tizimga kirgan hisoblarga ega papkalar, eski Desktop tartiblari, parol bilan himoyalangan ZIP-fayllar va macOS uchun alohida mahalliy "Telegram for macOS" ilovasi.

### Telethon StringSession

Bir qatorli matn, odatda `1` bilan boshlanib, taxminan 350 belgidan iborat. Uni `.txt` yoki `.tgwitness-session` fayli sifatida yuklang (eng ko'pi bilan 4 KiB) yoki **Passcode yoki session matni** ostiga joylashtiring. Faqat Telethon satrlari qabul qilinadi; Pyrogram va TDLib satrlari boshqa formatlardan foydalanadi.

### Hisob JSON

**`.json`** bilan tugaydigan faylda, maksimal **64 KiB** hajmdagi bitta JSON ob'ekti.

| Maydon (laqablari) | Ma'no |
| --- | --- |
| `api_id` (`app_id`) | Ilova ID, ijobiy son |
| `api_hash` (`app_hash`) | Ilova xesh, 32 geksadesimal belgilar |
| `string_session` (`session_string`, `session_str`; legacy `session`) | Telethon StringSession matni, fayl nomi emas |
| `auth_key` (`auth_key_hex`) + `dc_id` | 512 belgili Auth kalitini va DC 1–5 ni to'ldiring |
| `user_id` (`id`) | Ixtiyoriy; ruxsat saqlanmasidan oldin Telegramda tekshiriladi |
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

Birinchi misol faqat API ma'lumotlarini to'ldiradi; telefon yoki QR orqali tizimga kiring yoki sessiya faylini qo'shing. Ko'p hisob ro'yxatlari (hisoblarning JSON massiv) qabul qilinmaydi.

## Nimangiz borligini aniqlang

| Ko'ryapsiz | Bu | Foydalaning |
| --- | --- | --- |
| `*.session`; uni matn muharririda ochish yuqorida `SQLite format 3` ko'rinishini ko'rsatadi | Telethon yoki Pyrogram SQLite | **Fayllar** (avtomatik aniqlangan) |
| `tdata` papkasi ichida `key_datas` | Telegram Desktop TData | Ikki faylni ZIP qiling, so'ngra **Fayllar** |
| `1` bilan boshlanadigan bitta matn qatori, taxminan 350 belgili | Telethon StringSession | **Fayllar** |
| `*.json` va `app_id`/`app_hash` | Qo'shimcha metadata | **Fayllar**, sessiyasi bilan birga |
| `*.json`, `auth_key` yoki `string_session` bilan | Hisob JSON | **Fayllar** |
| 512 belgilar `0-9a-f` | Avtorlik kaliti | **Auth kaliti** |
| 32 belgilar`0-9a-f` | API xesh | **API ID + Hash** |
| `td.binlog` yoki TDLib ilovasidan `db.sqlite` | TDLib saqlash | Qo'llab-quvvatlanmaydi |
| `123456789:AA…` | Bot tokeni | Qo'llab-quvvatlanmaydi |

## Qo'llab-quvvatlanmaydigan formatlar

| Format | Alternativ |
| --- | --- |
| TDLib saqlash (`td.binlog`) va TDLib eksportlari | Telefon yoki QR orqali tizimga kiring |
| Pyrogram sessiya **satrlari** | Pyrogram `.session` faylidan yoki telefon/QR kodidan foydalaning |
| Bir nechta tizimga kirgan hisoblar bilan TData | Telegram Desktop'dagi boshqa hisoblardan chiqib turing yoki har bir hisob uchun alohida sessiya faylidan foydalaning |
| Bot tokenlari | Qo'llab-quvvatlanmaydi: TgWitness foydalanuvchi hisobini kuzatadi |
| Ko'plab akkauntlarning CSV/JSON ro'yxatlari | Qo‘llab-quvvatlanadigan sessiya fayllarini **Hisoblar → Hisoblarni import qilish** orqali import qiling yoki alohida ishchi maydonlarda telefon/QR orqali kiring |
| Test-DC yoki bot sessiyalari | Ishlab chiqarish foydalanuvchi hisobini ishlating |

## Bir nechta hisoblar

Hisob tanlovchisining yonidagi **+** tugmasini bosing yoki **Hisob → Sozlamalar → Ulanish sozlamalari → Ish maydonlari bo'limini** oching, yorliq kiriting va kirishni bosing.

- Asosiy ish maydoni hamda istalgan sonli boshqa ish maydonchalari mavjud. Har birining o'z sessiyasi, proxy yo'li, manbalari, yozib olish siyosati, jurnali, imzolash kaliti, tekshirish nuqtalari va eksportlari mavjud.
- Ko'rsatilayotgan ish maydonini almashtirish boshqalarni to'xtatmaydi.
- Jurnal uni yaratgan akkauntga bog'langan bo'lib qoladi. Boshqa akkauntga kirish uchun alohida ish maydoni talab etiladi va bir akkaunt ikki ish maydoniga tayinlanishi mumkin emas.
- Asosiy panel tokeni barcha ish maydonlarini nazorat qiladi. [Berilgan kirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/) boshqalarni tanlangan hisoblar va suhbatlarga, alohida ruxsatnomalar va sessiya cheklovlari bilan cheklashi mumkin.
- **Hisoblar** ish maydonini qayta nomlaydi va qo'shilgan ish maydonini sessiyasi, jurnali, manbalari va imzolash kaliti bilan o'chirib tashlaydi. Asosiy ish maydoni paneldan o'chirilmaydi.

### Ommaviy import va hisob guruhlari

**Hisoblar → Hisoblarni import qilish** orqali bir nechta hisobni qo'shing, fayllarni bazaviy nom bo'yicha juftlang va har bir kirish natijasini ko'ring. Har bir hisobga alohida ish maydoni beriladi.

Guruh tegishli hisoblarni ularning sessiyalari, kalitlari yoki dalillarini birlashtirmasdan birga saqlaydi. **Hisoblar** bo'limidagi **Ochiq guruhni** bosish uning sahifasiga olib boradi `/groups/<id>`:

- **Hisoblar:** har bir a'zoning ulanish yo'li, kuzatuvi va oxirgi xabari, **Barchasini** boshlash va **barchasini to'xtatish**.
- **E'tibor talab qiladi:** tizimdan chiqarilgan, mavjud bo'lmagan yoki ulanish, qabul qilish, manba yoki media bilan bog'liq muammo bo'lgan hisoblar; har bir nom uning kartasiga olib boradi.
- **Suhbatlar bir nechta hisoblarni ko'rsatadi:** ulashilgan manbalar, ularni kuzatayotgan hisoblar va mavjud ish maydoni-kuzatuv davrida (7 kungacha) uzilishlar. **N ta hisob bilan eksport** kanal yoki superguruh eksportini ularga bo'lib beradi va bitta arxivni imzolaydi.
- **Guruhni eksport qilish:** har bir hisobning imzolangan eksporti bilan bitta ZIP `accounts/` va `manifest.json` SHA-256 va kalit barmoq izlarini ro'yxatlab, asosiy ish maydoni tomonidan imzolangan `manifest.signature.json`. Har bir akkaunt arxivini alohida tarzda bilan tasdiqlang. `python -m tgwitness.verify` va o'sha hisobning ishonchli barmoq izi yordamida.

A'zolar guruh sozlamalarini baham ko'radi; hisob o'z qiymatlarini saqlab qolishi mumkin. Qarang [ulashilgan sozlamalar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/settings/#account-groups), [import va guruhlar bo'yicha qo'llanma](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) va [MTProxy pool boshqaruv paneli](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Chiqish

**Hisob → Telegramdan chiqish** (kuzatish to'xtatilgan holda) Telegramdan sessiyani yakunlashni so'raydi, shuning uchun u hisobning **Sozlamalar → Qurilmalar** bo'limidan ham yo'qoladi va ish maydoni shifri omboridan sessiyani o'chirib tashlaydi. Jurnal, manbalar, sozlamalar va imzolash kaliti saqlanib qoladi, va jurnal chiqishni qayd etadi. Ish maydoni hanuzgacha o'z hisobiga tegishli bo'lib qoladi: faqat shu hisob qayta ulanishi mumkin. Agar Telegram javob bermasa ham, sessiya bu yerda baribir o'chiriladi va panel bunga oid xabarni ko'rsatadi; Telegramda **Sozlamalar → Qurilmalar** bo'limida sessiyani yakunlang.

## Hisob fayllarini xavfsiz saqlash

- Har bir `.session`, TData ZIP, StringSession, Auth Key va hisob JSON faylini parol kabi muomala qiling. TgWitness import qilingan ruxsatnomalarni shifrlangan omborida saqlaydi; keyin asl fayllarni o'chirib tashlashingiz mumkin.
- Bir xil ruxsatni ikki dasturda bir vaqtda ishga tushirmang. Telegram uni bekor qilishi mumkin (`AUTH_KEY_DUPLICATED`), va ikkala nusxa ham ishlamay qoladi.
- Muddatidan o'tgan yoki bekor qilingan sessiyani konversiya orqali qayta tiklash mumkin emas. Qayta tizimga kiring.

## Muammolarni bartaraf etish

| Xabar yoki simptom | Nima qilish kerak |
| --- | --- |
| *Ushbu sessiyani o'qib bo'lmaydi. Uning asl mijozini yoping…* | SQLite fayl ochiq yoki yakunlanmagan (`-journal`/`-wal` yon fayl). Asl dasturni toza tarzda yoping va faylni yana nusxalang. |
| *Qo'llab-quvvatlanadigan Telethon SQLite sxemalari: 7 va 8* / *Pyrogram … 2 va 3* | Faylni juda eski yoki noma'lum kutubxona versiyasi yaratgan. Buning o'rniga telefon/QR orqali tizimga kiring. |
| *Faqat ruxsat etilgan ishlab chiqarish foydalanuvchi sessiyalari qo'llab-quvvatlanadi* | Pyrogram fayli botga yoki test tarmog'iga tegishli. |
| *TData arxivi 512 yozuvdan yoki 32 MiBdan oshadi* | Faqat `key_datas` va `D877F783D5D3EF8Cs` ZIP, butun papka emas. |
| *TData ni dekript qilib bo'lmadi. Desktop mahalliy parolini tekshiring* | **Passcode yoki sessiya matni** satriga Telegram Desktop mahalliy parolini kiriting. |
| *Bir vaqtning o'zida bitta TData hisobini import qiling* | Telegram Desktop bir nechta hisoblarga ega edi; [qo'llab-quvvatlanmaydigan formatlarga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#unsupported-formats) qarang. |
| *Tanlangan fayllar turli hisoblar yoki API ma'lumotlarini tasvirlaydi* | Fayllarni faqat bitta akkauntdan tanlang. |
| *JSONda qo'llab-quvvatlanadigan API ma'lumotlari yoki avtorizatsiya yo'q* | [Hisob JSON](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#account-json)idagi maydon nomlarini tekshiring. |
| *Faqat API metama'lumotlari* | JSONda sessiya yo'q. `.session` faylini qo'shing yoki telefon/QR-koddan foydalaning. |
| *Auth kaliti HEX barcha 512 geksadesimal belgini o'z ichiga olishi kerak* | Kalit qisqartirilgan yoki unda`…` mavjud. |
| Hisob IDi import qilingan hisob bilan mos kelmaydi | Faylning foydalanuvchi IDi Telegram xabar qilganidan farq qiladi; fayl boshqa hisob uchun mo'ljallangan. |
| Hisob allaqachon boshqa ish maydoniga tegishli | Hisobni ikki marta qo'shish o'rniga o'sha ish maydonini oching. |
| Ulanish mavjud, ammo **Manbalar** chat ro'yxatida shaxsiy guruh yo'q. | A'zolikni tekshiring. Tanlovchi birinchi 1 000 ta dialogni tekshiradi; **parametrlar** bo'limida limitni oshiring. |
| Proxy ulanishi muvaffaqiyatsiz bo'ldi | Yo'nalish va IP rejimini tekshiring. Avtomatik MTProxy boshqa ishlaydigan kirishni sinab ko'radi. "Adressni yashirish" kutadi; "To'g'ridan-to'g'ri" esa oxirgi chora sifatida sozlangan kechikishdan so'ng to'g'ridan-to'g'ri ulanishi mumkin. [Yo'naltirish rejimlarini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/#ip-modes) ko'ring. |

Shuningdek qarang: proksi va shifrlash uchun [ulanish va xavfsizlik](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/), hamda tizimga kirgandan keyin [qanday ma'lumotlar yig'ilishi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/).
