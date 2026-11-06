# Формати облікових записів та сеансів

Canonical page: https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/

Увійдіть за допомогою телефону, QR-коду або ключа автентифікації, імпортуйте сесії з Telethon, Pyrogram або Telegram Desktop та керуйте кількома обліковими записами.

TgWitness входить у систему як облі**ковий запис користувача Telegram** (а не як бот) через MTProto, використовуючи Telethon. Кожен обліковий запис розміщується у власному робочому **просторі** (який у API та інструментах командного рядка називається *«workspace*») із власною сесією, джерелами, журналом та ключем підпису.

Файли сеансів, рядки сеансів та ключі автентифікації є **засобами авторизації облікового запису**: той, хто володіє ними, може діяти від імені цього облікового запису. Вони не містять історії повідомлень.

> [!ПОПЕРЕДЖЕННЯ] **Не використовуйте те, що не можете собі дозволити втратити.** Ми настійно не рекомендуємо підключати особисті або інші цінні акаунти, а також створювати API-ідентифікатор / API-хеш на акаунті, який для вас цінний. Справа не в тому, що TgWitness не пройшов тестування: Telegram обмежує та постійно блокує акаунти непередбачувано — за обсяги запитів, які він вважає надмірними, незалежно від клієнта чи мети, без належної документації. Багато блокувань є незворотними. Використовуйте спеціальні акаунти. Безперебійне тестування залежить від Telegram, а не від програмного забезпечення, і не гарантує нічого на майбутнє.

- [Короткий огляд](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#at-a-glance)
- [Перш ніж почати: ідентифікатор API та хеш API](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Номер телефону](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#phone-number) · [QR-код](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#qr-code) · [Ключ автентифікації + ідентифікатор DC](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#auth-key--dc-id)
- [Файли облікових записів](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#pyrogram-session) · [Пара «сесія + JSON»](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#telethon-stringsession) · [JSON-файл облікового запису](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#account-json)
- [Визначте, що у вас є](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#identify-what-you-have) · [Непідтримувані формати](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#unsupported-formats)
- [Кілька облікових записів](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#multiple-accounts) · [Забезпечення безпеки файлів облікових записів](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#keeping-account-files-safe) · [Усунення несправностей](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#troubleshooting)

## Короткий огляд

| Що у вас є | Вкладка «**Додати обліковий запис**» | Вам також знадобиться |
| --- | --- | --- |
| Номер телефону та доступ до кодів входу | **Телефон** | Пароль 2FA, якщо функція увімкнена |
| Telegram відкрито на іншому пристрої | **QR-код** | Пароль 2FA, якщо функція увімкнена |
| Файл `.session` (Telethon або Pyrogram) | **Файли** | Додатковий супровідний файл JSON для налаштувань додатка |
| `.session` + `.json` з однаковою назвою | **Файли** (виберіть обидва) | Зазвичай нічого іншого |
| Папка «`tdata`» у Telegram Desktop | **Файли** (у форматі ZIP) | Локальний пароль для настільного комп’ютера, якщо такий встановлено |
| StringSession для Telethon (текст, `.txt`, `.tgwitness-session`) | **Файли** | Окремої пари API не потрібно |
| `.json` із сесією або ключем автентифікації | **Файли** | Окремої пари API не потрібно |
| Ключ автентифікації (512 шестнадцяткових символів) та його номер DC | **Ключ автентифікації** | Опціональний ідентифікатор користувача |

TgWitness розпізнає файли за їхнім **вмістом**, а не за іменами. Перейменування файлу ніколи не призводить до його конвертації.

## Перш ніж почати: ідентифікатор API та хеш API

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

Щоб замість цього використовувати власний додаток (ризику піддається саме той обліковий запис, на якому його зареєстровано; див. [«Навіщо потрібен вбудований пул API?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)»):

1. Відкрийте [my.telegram.org](https://my.telegram.org) і увійдіть, вказавши будь-який номер телефону, який належить вам. Код надходить у додаток Telegram, а не у вигляді SMS.
2. Виберіть **інструменти для розробки API**.
3. Створити заявку: будь-яка назва та коротка назва (5–32 літери), платформа — **«Настільний ПК**». Поля «URL» та «Опис» можна залишити порожніми.
4. Скопіюйте **App api_id** (число) та **App api_hash** (32 шестнадцяткові символи).

У панелі під формою входу вказано **«API ID + Hash**». Ви можете ввести одну пару `api_id:api_hash` у **поле «API ID**», і обидва поля заповняться автоматично. Одну пару можна використовувати для всіх ваших облікових записів. Після успішного входу дані зберігаються у зашифрованому вигляді виключно в цьому робочому просторі й ніколи не надсилаються назад до браузера.

Задіяно три різні типи облікових даних:

| Секрет | Відкрити | Де це знаходиться |
| --- | --- | --- |
| Токен панелі | Веб-панель TgWitness | `panel-token.txt` у каталозі даних або `TGWITNESS_TOKEN` |
| Ідентифікатор API + хеш | Нічого окремо; ідентифікує додаток | Вбудована пара, імпортовані налаштування або ваш власний додаток на my.telegram.org |
| Авторизація облікового запису | Акаунт у Telegram | Створюється шляхом входу через телефон/QR-код або імпортується як сесія |

Якщо для доступу до Telegram потрібно використовувати проксі-сервер, спочатку налаштуйте його в меню **«Акаунт» → «Налаштування» → «Налаштування з’єднання» → «Змінити маршрут з’єднання**».

## Номер телефону

1. Відкрийте **обліковий запис**, перейдіть на вкладку **«Телефон»** і введіть номер у міжнародному форматі, наприклад, `+44 7700 900123`. Пробіли та тире видаляються автоматично.
2. Натисніть **«Продовжити**». Поля «API ID» та «Хеш» можна залишити порожніми.
3. Введіть код, який надсилає Telegram (зазвичай у додаток Telegram; надсилання SMS не гарантується).
4. Якщо для облікового запису налаштовано двоступеневу аутентифікацію, введіть цей пароль. Це не токен панелі і не код доступу до пристрою.
5. Перевірте ідентифікатор облікового запису, що відображається після входу, а потім виберіть джерела.

Коди входу та пароль 2FA ніколи не записуються на диск.

## QR-код

Використовуйте цю функцію, коли обліковий запис уже ввійшов у систему на телефоні або іншому комп’ютері.

1. Вкладка **«QR-код»** → **Показати QR-код**. Поля «API ID» та «Хеш» можна залишити порожніми.
2. На пристрої, на якому ви увійшли: **Налаштування → Пристрої → Підключити настільний пристрій**, відскануйте код та підтвердіть.
3. Введіть пароль 2FA у TgWitness, якщо Telegram його вимагає.

Зображення QR-коду генерується локально. Термін дії кодів обмежений; натисніть **«Створити інший QR-код»,** щоб спробувати ще раз. Блокування панелі, перехід до іншого робочого простору або початок нової сесії входу скасовує код, що очікує на використання.

## Ключ автентифікації + ідентифікатор DC

Ключ авторизації (Auth Key) — це необроблений 256-байтовий код авторизації, що лежить в основі кожного сеансу Telegram, записаний у вигляді **512 шістнадцяткових символів** разом із номером центру обробки даних **DC 1–5**.

1. Вкладка **«Ключ авторизації**». Вставте повний ключ; скорочений ключ, що містить `…`, не працюватиме.
2. Виберіть DC-ідентифікатор, наданий разом із ключем.
3. За бажанням введіть **ідентифікатор користувача**. У такому разі TgWitness відмовить у підключенні, якщо Telegram повідомить про інший обліковий запис.
4. **Акаунт у** Press **Connect**.

Ключ авторизації (512 символів) — це не хеш API (32 символи). Цей самий ключ також можна імпортувати у форматі JSON, див. [JSON-файл облікового запису](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#account-json).

## Файли облікових записів

Відкрийте **«Додати обліковий запис» → «Файли»** та виберіть до **чотирьох файлів**, **що належать до одного облікового запису**, загальним розміром до **8 МіБ**, а потім натисніть **«Підключити обліковий запис**».

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- Файли конвертуються **в оперативній пам’яті** на вашому сервері TgWitness. Завантажені дані не зберігаються, архіви ZIP не розпаковуються на диск, і не відбувається звернення до жодних зовнішніх сервісів.
- Отримані дані потім перевіряються за допомогою Telegram. Якщо у файлі вказано ідентифікатор користувача, він повинен збігатися з даними облікового запису, які надає Telegram.
- Файли, що описують різні облікові записи або різні облікові дані API, відхиляються, замість того, щоб вибрати один із них.
- Поле **«Пароль або текст сеансу»** містить поле локального пароля TData — поле для вставлення StringSession та **Read-файлів без входу в систему** (заповнює форму без звернення до Telegram).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

### Телемарафон `.session`

|  |  |
| --- | --- |
| Що це таке | База даних SQLite, яку створюють інструменти на базі Telethon, наприклад `my_account.session` |
| Визнано | Таблиці `sessions` (разом із `dc_id`, `server_address`, `port`, `auth_key`) та `version` = 7 або 8 |
| Вимоги | Рівно один рядок авторизованої сесії; закрита, повна база даних |

Спочатку закрийте програму, яка створила файл. Якщо поруч із ним є файл `my_account.session-journal` або `my_account.session-wal`, це означає, що база даних не завершена: відкрийте та повністю закрийте оригінальний клієнт. Видалення цих супутніх файлів може призвести до пошкодження копії.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Що це таке | База даних SQLite, яку створюють інструменти на основі Pyrogram |
| Визнано | Таблиця `sessions` з `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 або 3 |
| Вимоги | Допускається лише одна авторизована сесія **користувача** в робочій мережі. Сесії ботів та тестових DC відхиляються. |

Під час входу збережений ідентифікатор користувача перевіряється у Telegram.

### Пара «сесія + JSON»

Дані часто розповсюджуються у вигляді двох файлів з однаковою назвою, наприклад `447700900123.session` та `447700900123.json`. Виберіть **обидва** одночасно.

- На основі JSON TgWitness використовує `app_id`/`api_id` та `app_hash`/`api_hash`, тому вам зазвичай не потрібно вводити облікові дані API.
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData — це папка `tdata` у програмі Telegram Desktop (кросплатформовий додаток з desktop.telegram.org).

| Система | Стандартне розташування `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (портативний Telegram: поруч із `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Щоб імпортувати його:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> Це також стосується імпортованих `.session` файли, текст StringSession та HEX-код ключа авторизації. Інші клієнти з власними, незалежно створеними авторизаціями, можуть залишатися у системі. Дивіться [документацію Telegram щодо AUTH_KEY_DUPLICATED](https://core.telegram.org/api/errors#406-not-acceptable).

1. Повністю закрийте Telegram Desktop.
2. Створіть ZIP-архів, що містить **лише** ці два елементи з `tdata`:

   - `key_datas`
   - 16-символьний файл із розширенням «`s`», що знаходиться поруч, зазвичай «`D877F783D5D3EF8Cs`»

   Стиснення всієї папки разом із кешем мультимедіа зазвичай перевищує обмеження (512 записів, 32 МіБ у розпакованому вигляді). 3. Виберіть ZIP-файл у розділі **«Файли**». Якщо у Telegram Desktop встановлено **локальний пароль**, спочатку введіть його у полі **«Пароль» або «Текст сеансу**». Це не пароль 2FA.

Підтримується: один обліковий запис на архів, сучасне сховище `key_datas`/`key_data0`/`key_data1`, локальний пароль. Не підтримується: папки з кількома обліковими записами, що ввійшли в систему, старі версії десктопного додатка, ZIP-архіви, захищені паролем, та окремий нативний додаток для macOS «Telegram для macOS».

### Telethon StringSession

Один рядок тексту, який зазвичай починається з `1` і має довжину близько 350 символів. Завантажте його як файл `.txt` або `.tgwitness-session` (максимум 4 Кбайт) або вставте його в поле **«Пароль» або «Текст сеансу**». Приймаються лише рядки у форматі Telethon; рядки у форматах Pyrogram та TDLib мають інші формати.

### JSON-файл облікового запису

Один об’єкт JSON, розміром не більше **64 Кбайт**, у файлі з розширенням **`.json`**.

| Поле (псевдоніми) | Значення |
| --- | --- |
| `api_id` (`app_id`) | Ідентифікатор додатка — додатне число |
| `api_hash` (`app_hash`) | Хеш додатка, 32 шестнадцяткові символи |
| `string_session` (`session_string`, `session_str`; legacy `session`) | Текст Telethon StringSession, а не ім’я файлу |
| `auth_key` (`auth_key_hex`) + `dc_id` | Повний ключ автентифікації довжиною 512 символів та DC 1–5 |
| `user_id` (`id`) | Необов’язково; перевіряється у Telegram перед збереженням авторизації |
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

У першому прикладі заповнюються лише облікові дані API; увійдіть за допомогою телефону або QR-коду, або додайте файл сеансу. Масові списки (масив JSON з обліковими записами) не приймаються.

## Визначте, що у вас є

| Ви бачите | Це | Використання |
| --- | --- | --- |
| `*.session`; при відкритті у текстовому редакторі у верхній частині відображається `SQLite format 3` | Telethon або Pyrogram SQLite | **Файли** (виявляються автоматично) |
| Папка «`tdata`», що містить «`key_datas`» | Telegram Desktop TData | Стиснути два файли у ZIP, потім **«Файли»** |
| Один рядок тексту, що починається з `1`, приблизно 350 символів | Telethon StringSession | **Файли** |
| `*.json` з `app_id`/`app_hash` | Супровідні метадані | **Файли** разом із сесією |
| `*.json` з `auth_key` або `string_session` | JSON-файл облікового запису | **Файли** |
| 512 символів `0-9a-f` | Ключ автентифікації | **Ключ автентифікації** |
| 32 символи `0-9a-f` | Хеш API | **Ідентифікатор API + хеш** |
| `td.binlog` або `db.sqlite` із додатка TDLib | Хранилище TDLib | Не підтримується |
| `123456789:AA…` | Токен бота | Не підтримується |

## Непідтримувані формати

| Формат | Альтернатива |
| --- | --- |
| Сховище TDLib (`td.binlog`) та експорт даних TDLib | Увійдіть за допомогою телефону або QR-коду |
| **Строки** сеансів Pyrogram | Використовуйте файл Pyrogram `.session` або телефон/QR-код |
| TData з кількома обліковими записами, що ввійшли в систему | Вийдіть з інших облікових записів у Telegram Desktop або використовуйте власний файл сеансу кожного облікового запису |
| Токени ботів | Не підтримується: TgWitness здійснює спостереження як обліковий запис користувача |
| Списки багатьох акаунтів у форматі CSV/JSON | Імпортуйте підтримувані файли сесій через **Облікові записи → Імпорт облікових записів** або увійдіть за номером телефону / QR-кодом в окремих робочих просторах |
| Test-DC або сесії ботів | Використовуйте робочий обліковий запис користувача |

## Кілька облікових записів

Натисніть **+** поруч із перемикачем облікових записів або відкрийте **Обліковий запис → Налаштування → Налаштування з’єднання → Робочі простори**, введіть назву та увійдіть.

- Необмежена кількість робочих просторів, включаючи основний. Кожен має власну сесію, проксі- маршрут, джерела, політику збору даних, журнал, ключ підпису, контрольні точки та експортні файли.
- Перемикання між робочими просторами не призупиняє роботу інших.
- Журнал залишається прив’язаним до облікового запису, з якого його було створено. Для входу з іншого облікового запису потрібно створити інший робочий простір, а один обліковий запис не можна прив’язати до двох робочих просторів.
- Токен головної панелі керує всіма робочими просторами. [Наданий доступ](https://phishdestroy.github.io/TgWitness/uk/docs/reference/access/) дозволяє обмежити доступ інших користувачів до вибраних акаунтів та чатів із окремими правами доступу та обмеженнями сеансів.
- **Функція «Акаунти»** перейменовує робочу область та видаляє додану робочу область разом із її сесією, журналом, джерелами та ключем підпису. Головну робочу область неможливо видалити з панелі.

### Масовий імпорт і групи акаунтів

Скористайтеся **меню «Акаунти» → «Імпортувати акаунти»**, щоб додати кілька акаунтів, зіставити файли за базовим іменем та переглянути результати входу для кожного з них. Кожен акаунт отримує власний робочий простір.

Група об’єднує пов’язані акаунти, не об’єднуючи їхні сесії, ключі чи докази. Натиснувши **«Відкрити групу»** у розділі **«Акаунти»,** ви перейдете на її сторінку за адресою `/groups/<id>`:

- **Облікові записи:** маршрут підключення кожного учасника, спостереження та останнє повідомлення, з функціями «Запустити**все»** та **«Призупинити все**».
- **Потребує уваги:** акаунти, з яких вийшли, які недоступні або мають проблеми з підключенням, введенням даних, джерелом чи медіафайлами; кожне ім’я веде до відповідної картки.
- **У чатах, які переглядають кілька облікових записів, відображаються:** спільні джерела, облікові записи, що їх переглядають, та перерви в періоді спостереження за робочим простором (до семи днів). **Експорт із N обліковими записами** розподіляє експорт каналу або супергрупи між ними та підписує один архів.
- **Експорт групи:** один елемент ZIP, у якому міститься підписаний експорт кожного облікового запису під `accounts/` та `manifest.json` переліком їхніх SHA-256 та відбитків ключів, підписаних головним робочим простором у `manifest.signature.json`. Перевіряйте архів кожного облікового запису окремо за допомогою `python -m tgwitness.verify` та перевіряйте його за допомогою надійного відбитка цього облікового запису.

Учасники використовують спільні налаштування групи; кожен обліковий запис може зберігати власні значення. Дивіться [розділ «Спільні налаштування»](https://phishdestroy.github.io/TgWitness/uk/docs/reference/settings/#account-groups), [посібник з імпорту та груп](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) та [панель управління пулом MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Вийти

**Обліковий запис → Вийти з Telegram** (з призупиненням спостереження) надсилає Telegram запит на завершення сеансу, тому він також зникає з розділу **«Налаштування» → «Пристрої»** облікового запису та видаляється з сховища робочого простору. Журнал, джерела, налаштування та ключ підпису залишаються, а журнал фіксує вихід із системи. Робоча область все ще належить цьому обліковому запису: лише цей обліковий запис може знову підключитися до неї. Якщо Telegram не відповідає, сесія все одно видаляється тут, і панель повідомляє про це; завершіть її в Telegram у розділі **«Налаштування» → «Пристрої**».

## Забезпечення безпеки файлів облікових записів

- Ставтеся до кожного `.session`, TData ZIP, StringSession, Auth Key та JSON-файлу облікового запису як до пароля. TgWitness зберігає імпортовані дані авторизації у своєму зашифрованому сховищі; ви можете пізніше видалити оригінальні файли.
- Не використовуйте одну й ту саму авторизацію одночасно у двох програмах. Telegram може її скасувати (`AUTH_KEY_DUPLICATED`), і обидві копії перестануть працювати.
- Сесія, термін дії якої закінчився або яка була скасована, не може бути відновлена шляхом конвертації. Увійдіть знову.

## Усунення несправностей

| Повідомлення або ознака | Що робити |
| --- | --- |
| *Неможливо прочитати цю сесію. Закрийте оригінальний клієнт…* | Файл SQLite відкритий або незавершений (додатковий файл `-journal`/`-wal`). Належним чином закрийте вихідну програму та скопіюйте файл ще раз. |
| *Підтримувані схеми Telethon SQLite: 7 та 8* / *Pyrogram … 2 та 3* | Файл було створено за допомогою дуже старої або невідомої версії бібліотеки. Замість цього увійдіть за допомогою телефону/QR-коду. |
| *Підтримуються лише авторизовані сесії користувачів у виробничому середовищі* | Файл Pyrogram належить боту або тестовій мережі. |
| *Архів TData перевищує 512 записів або 32 МіБ* | У ZIP-файлі мають бути лише файли `key_datas` та `D877F783D5D3EF8Cs`, а не вся папка. |
| *Неможливо розшифрувати TData. Перевірте локальний пароль на робочому столі* | Введіть локальний пароль Telegram Desktop у полі **«Пароль» або «Текст сеансу**». |
| *Імпортуйте по одному обліковому запису TData за раз* | У Telegram Desktop було кілька облікових записів; див. розділ [«Непідтримувані формати](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#unsupported-formats)». |
| *Вибрані файли містять опис різних облікових записів або облікових даних API* | Вибирайте файли лише з одного облікового запису. |
| *JSON не містить жодних облікових даних або авторизаційних даних для підтримуваних API* | Перевірте назви полів у [JSON-файлі облікового запису](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/#account-json). |
| *Лише метадані API* | У JSON немає сесії. Додайте файл `.session` або скористайтеся номером телефону/QR-кодом. |
| *HEX-код авторизаційного ключа повинен містити всі 512 шістнадцяткових символів* | Ключ є урізаним або містить `…`. |
| Ідентифікатор облікового запису не збігається з імпортованим обліковим записом | Ідентифікатор користувача у файлі відрізняється від того, що вказує Telegram; файл належить іншому обліковому запису. |
| Цей обліковий запис уже належить іншому робочому простору | Відкрийте цю робочу область замість того, щоб додавати обліковий запис двічі. |
| Посилання є, але у списку чатів у **розділі «Джерела»** відсутня приватна група | Перевірте членство. Програма перевіряє перші 1 000 діалогів; збільште цей ліміт у розділі **«Параметри**». |
| Помилка підключення через проксі | Перевірте режим маршрутизації та IP. Автоматичний MTProxy пробує інший робочий запис. «Hide the address» очікує; «Direct» як крайній захід може встановити з’єднання безпосередньо після налаштованої затримки. Див. [режими маршрутизації](https://phishdestroy.github.io/TgWitness/uk/docs/reference/connection/#ip-modes). |

Див. також: [підключення та безпека](https://phishdestroy.github.io/TgWitness/uk/docs/reference/connection/) проксі-серверів і шифрування, а також [як відбувається збір](https://phishdestroy.github.io/TgWitness/uk/docs/reference/collection/) даних після входу в систему.
