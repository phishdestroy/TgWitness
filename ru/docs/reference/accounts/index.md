# Аккаунты и форматы сессий

Canonical page: https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/

Войдите в систему с помощью телефона, QR-кода или ключа аутентификации, импортируйте сеансы из Telethon, Pyrogram или Telegram Desktop и управляйте несколькими учётными записями.

TgWitness входит в систему как учетная **запись пользователя Telegram** (а не как бот) через протокол MTProto с использованием Telethon. Каждая учетная запись находится в собственном **рабочем пространстве** (называемом *«workspace»* в API и инструментах командной строки) с собственной сессией, источниками, журналом и ключом подписи.

Файлы сеансов, строки сеансов и ключи аутентификации являются **средствами авторизации учетной записи**: любой, кто имеет один из них, может действовать от имени этой учетной записи. Они не содержат истории сообщений.

> [!ПРЕДУПРЕЖДЕНИЕ] **Не используйте то, что вы не можете себе позволить потерять.** Мы настоятельно не рекомендуем подключать личные или иные ценные учетные записи, а также создавать API-идентификатор / API-хэш на учетной записи, которая для вас важна. Дело не в том, что TgWitness не прошел тестирование: Telegram неожиданно ограничивает доступ и навсегда блокирует аккаунты — при объёме запросов, который он считает чрезмерным, независимо от клиента или цели, без надлежащей документации. Многие блокировки неподдаются отмене. Используйте специальные аккаунты. Бесперебойное проведение тестов зависит от Telegram, а не от программного обеспечения, и не гарантирует ничего на будущее.

- [Краткий обзор](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#at-a-glance)
- [Прежде чем начать: идентификатор API и хеш API](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Номер телефона](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#phone-number) · [QR-код](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#qr-code) · [Ключ аутентификации + идентификатор DC](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#auth-key--dc-id)
- [Файлы учетных записей](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#pyrogram-session) · [Пара «сессия + JSON»](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#telethon-stringsession) · [JSON-файл учетной записи](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#account-json)
- [Определите, чем вы располагаете](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#identify-what-you-have) · [Неподдерживаемые форматы](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#unsupported-formats)
- [Наличие нескольких учётных записей](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#multiple-accounts) · [Обеспечение безопасности файлов учетных записей](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#keeping-account-files-safe) · [Устранение неполадок](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#troubleshooting)

## Краткий обзор

| Что у вас есть | Вкладка **«Добавить аккаунт**» | Вам также понадобятся |
| --- | --- | --- |
| Номер телефона и доступ к кодам входа в систему | **Телефон** | Пароль двухфакторной аутентификации (2FA), если она включена |
| Telegram открыт на другом устройстве | **QR-код** | Пароль двухфакторной аутентификации (2FA), если она включена |
| Файл `.session` (Telethon или Pyrogram) | **Файлы** | Дополнительный файл JSON с настройками приложения |
| `.session` + `.json` с одинаковым названием | **Файлы** (выберите оба) | Обычно ничего больше |
| Папка «`tdata`» в Telegram Desktop | **Файлы** (в формате ZIP) | Локальный пароль для настольной версии, если он установлен |
| StringSession Telethon (текст, `.txt`, `.tgwitness-session`) | **Файлы** | Отдельная пара API не требуется |
| `.json` с сессией или ключом аутентификации | **Файлы** | Отдельная пара API не требуется |
| Ключ аутентификации (512 шестнадцатеричных символов) и его номер DC | **Ключ аутентификации** | Необязательный идентификатор пользователя |

TgWitness распознает файлы по их **содержимому**, а не по именам. Переименование файла никогда не приводит к его преобразованию.

## Прежде чем начать: идентификатор API и хеш API

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

Если вы предпочитаете использовать собственное приложение (в этом случае риску подвергается учетная запись, на которой оно зарегистрировано; см. раздел [«Зачем нужен встроенный пул API?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)»):

1. Откройте сайт [my.telegram.org](https://my.telegram.org) и войдите, указав любой номер телефона, который принадлежит вам. Код приходит в приложение Telegram, а не в виде SMS.
2. Выберите **инструменты для разработки API**.
3. Создайте приложение: укажите любое название и краткое имя (5–32 буквы), платформа — **«Настольный компьютер**». Поля «URL» и «Описание» можно оставить пустыми.
4. Скопируйте **App api_id** (число) и **App api_hash** (32 шестнадцатеричных символа).

В панели под формой входа указаны поля**«Идентификатор API» и «Хеш**». Вы можете ввести одну пару `api_id:api_hash` в **поле «Идентификатор API»**, и оба поля будут заполнены. Одну пару можно использовать для всех ваших учётных записей. После успешного входа данные сохраняются в зашифрованном виде исключительно в данной рабочей среде и никогда не отправляются обратно в браузер.

Здесь задействованы три различных типа учетных данных:

| Секретно | Открыть | Где это находится |
| --- | --- | --- |
| Токен панели | Веб-панель TgWitness | `panel-token.txt` в каталоге данных или `TGWITNESS_TOKEN` |
| Идентификатор API + хеш | Ничего не говорит само по себе; определяет приложение | Встроенная пара, импортированные настройки или ваше собственное приложение на сайте my.telegram.org |
| Авторизация учетной записи | Аккаунт в Telegram | Создается посредством входа с помощью телефона или QR-кода либо импортируется в качестве сеанса |

Если для доступа к Telegram требуется прокси-сервер, сначала настройте его в разделе **«Аккаунт» → «Настройки» → «Настройки подключения» → «Изменить маршрут подключения**».

## Номер телефона

1. Откройте **раздел «Аккаунт»**, перейдите на вкладку **«Телефон»** и введите номер в международном формате, например, `+44 7700 900123`. Пробелы и дефисы удаляются автоматически.
2. Нажмите **«Продолжить**». Поля «API ID» и «Хеш» можно оставить пустыми.
3. Введите код, отправленный Telegram (обычно в приложение Telegram; доставка по SMS не гарантируется).
4. Если для аккаунта настроена двухэтапная аутентификация, введите соответствующий пароль. Это не токен панели и не код доступа к устройству.
5. Проверьте идентификатор учетной записи, отображаемый после входа в систему, а затем выберите источники.

Коды входа и пароль двухфакторной аутентификации (2FA) никогда не записываются на диск.

## QR-код

Используйте эту функцию, если учетная запись уже авторизована на телефоне или другом компьютере.

1. Вкладка **«QR-код»** → **Показать QR-код**. Поля «API ID» и «Хеш» можно оставить пустыми.
2. На устройстве, на котором выполнен вход: **«Настройки» → «Устройства» → «Привязать настольное устройство**», отсканируйте код и подтвердите.
3. Введите пароль двухфакторной аутентификации (2FA) в TgWitness, если Telegram запрашивает его.

Изображение QR-кода генерируется локально. Срок действия кодов истекает; нажмите **«Сгенерировать другой QR-код»,** чтобы повторить попытку. Блокировка панели, переключение рабочего пространства или вход под другим аккаунтом приводят к аннулированию кода, ожидающего обработки.

## Ключ аутентификации + идентификатор DC

Ключ авторизации — это исходный 256-байтовый ключ авторизации, лежащий в основе каждого сеанса Telegram, записанный в виде **512 шестнадцатеричных символов** вместе с номером центра обработки данных **DC 1–5**.

1. Вкладка **«Ключ аутентификации**». Вставьте полный ключ; сокращённый ключ, содержащий символ `…`, не будет работать.
2. Выберите идентификатор DC, предоставленный вместе с ключом.
3. По желанию введите **идентификатор пользователя**. В этом случае TgWitness откажется подключаться, если Telegram сообщит о другом аккаунте.
4. **Аккаунт в** Press **Connect**.

Ключ авторизации (512 символов) не является хешем API (32 символа). Тот же ключ также можно импортировать в формате JSON; см. раздел [«JSON-файл учетной записи](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#account-json)».

## Файлы учетных записей

Откройте **«Добавить аккаунт» → «Файлы»** и выберите до **четырёх файлов**, **относящихся к одному аккаунту**, общим объёмом **8 MiB**, затем нажмите **«Подключить аккаунт**».

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- Файлы конвертируются **в памяти** на вашем сервере TgWitness. Загруженные файлы не сохраняются, архивы ZIP не распаковываются на диск, и не происходит обращения к каким-либо внешним сервисам.
- Полученный файл затем сверяется с данными Telegram. Если в файле указан идентификатор пользователя, он должен совпадать с идентификатором учетной записи, указанным в отчёте Telegram.
- Файлы, в которых описываются разные учётные записи или разные учетные данные API, отклоняются, вместо того чтобы выбрать одну из них.
- Поле **«Пароль или текст сеанса**» содержит поле локального пароля TData — поле для вставки StringSession и **чтения файлов без входа в систему** (заполняет форму без обращения к Telegram).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

### Телемарафон `.session`

|  |  |
| --- | --- |
| Что это такое | База данных SQLite, создаваемая инструментами на основе Telethon, например, `my_account.session` |
| Признан | Таблицы `sessions` (вместе с `dc_id`, `server_address`, `port`, `auth_key`) и `version` = 7 или 8 |
| Требования | Ровно одна строка, относящаяся к авторизованной сессии; закрытая, полная база данных |

Сначала закройте программу, создавшую файл. Если рядом с ним присутствует файл `my_account.session-journal` или `my_account.session-wal`, это означает, что база данных не завершена: откройте и корректно закройте исходный клиент. Удаление этих вспомогательных файлов может привести к появлению повреждённой копии.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Что это такое | Инструменты на основе Pyrogram, использующие базу данных SQLite, создают |
| Признан | Таблица `sessions` с `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 или 3 |
| Требования | Допускается один авторизованный сеанс **пользователя** в производственной сети. Сеансы ботов и тестовых распределённых центров (DC) отклоняются. |

При входе в систему сохраненный идентификатор пользователя сверяется с данными Telegram.

### Пара «сессия + JSON»

Отчёты часто предоставляются в виде двух файлов с одинаковыми именами, например, `447700900123.session` и `447700900123.json`. Выберите **оба файла** одновременно.

- На основании данных JSON TgWitness использует `app_id`/`api_id` и `app_hash`/`api_hash`, поэтому вам как правило, не требуется вводить учетные данные API.
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData — это папка `tdata` приложения Telegram Desktop (кроссплатформенного приложения с сайта desktop.telegram.org).

| Система | Местоположение по умолчанию: `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (портативная версия Telegram: рядом с `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Чтобы импортировать его:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> Это также относится к импортированным `.session` файлы, текст StringSession и шестнадцатеричный код авторизационного ключа. Другие клиенты с собственными, независимо созданными авторизациями могут оставаться авторизованными. См. [документацию Telegram по AUTH_KEY_DUPLICATED](https://core.telegram.org/api/errors#406-not-acceptable).

1. Полностью закройте Telegram Desktop.
2. Создайте ZIP-архив, содержащий **только** эти два элемента из `tdata`:

   - `key_datas`
   - 16-символьный файл с расширением «`s`», расположенный рядом с ним, обычно «`D877F783D5D3EF8Cs`»

   Сжатие всей папки вместе с кэшем мультимедиа, как правило, превышает установленные ограничения (512 записей, 32 MiB в распакованном виде). 3. Выберите ZIP-файл в разделе **«Файлы**». Если у Telegram Desktop установлен **локальный пароль**, сначала введите его в поле **«Пароль» или «Текст сеанса**». Это не пароль двухфакторной аутентификации (2FA).

Поддерживается: один аккаунт на архив, современное хранилище `key_datas`/`key_data0`/`key_data1`, локальный пароль. Не поддерживается: папки с несколькими авторизованными аккаунтами, устаревшие версии десктопного приложения, ZIP-архивы, защищённые паролем, а также отдельное нативное приложение для macOS «Telegram для macOS».

### Telethon StringSession

Одна строка текста, обычно начинающаяся с `1` и содержащая около 350 символов. Загрузите её в виде файла `.txt` или `.tgwitness-session` (размером не более 4 КиБ) или вставьте в поле **«Пароль» или «Текст сеанса**». Принимаются только строки формата Telethon; строки Pyrogram и TDLib используют другие форматы.

### JSON-файл учетной записи

Один объект JSON размером не более **64 КиБ** в файле с расширением **`.json`**.

| Поле (псевдонимы) | Значение |
| --- | --- |
| `api_id` (`app_id`) | Идентификатор приложения — положительное число |
| `api_hash` (`app_hash`) | Хеш приложения, 32 шестнадцатеричных символа |
| `string_session` (`session_string`, `session_str`; legacy `session`) | Текст StringSession для Telethon, а не имя файла |
| `auth_key` (`auth_key_hex`) + `dc_id` | Полный 512-символьный ключ аутентификации и DC 1–5 |
| `user_id` (`id`) | Необязательно; проверка в Telegram производится до сохранения авторизации |
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

В первом примере заполняются только учетные данные API; войдите в систему с помощью телефона или QR-кода либо добавьте файл сеанса. Массовые списки (массив JSON с учетными записями) не принимаются.

## Определите, чем вы располагаете

| Как видите | Это | Использование |
| --- | --- | --- |
| `*.session`; при открытии в текстовом редакторе в верхней части отображается `SQLite format 3` | Telethon или Pyrogram SQLite | **Файлы** (обнаруживаются автоматически) |
| Папка «`tdata`», содержащая файл «`key_datas`» | Telegram Desktop TData | Скомпрессируйте два файла в ZIP, затем **«Файлы»** |
| Одна строка текста, начинающаяся с `1`, ~350 символов | Telethon StringSession | **Файлы** |
| `*.json` с `app_id`/`app_hash` | Сопутствующие метаданные | **Файлы** вместе с данными сеанса |
| `*.json` с `auth_key` или `string_session` | JSON-файл учетной записи | **Файлы** |
| 512 символов `0-9a-f` | Ключ аутентификации | **Ключ аутентификации** |
| 32 символа `0-9a-f` | Хеш API | **Идентификатор API + хеш** |
| `td.binlog` или `db.sqlite` из приложения TDLib | Хранилище TDLib | Не поддерживается |
| `123456789:AA…` | Токен бота | Не поддерживается |

## Неподдерживаемые форматы

| Формат | Альтернативный вариант |
| --- | --- |
| Хранилище TDLib (`td.binlog`) и экспорт данных из TDLib | Войдите с помощью телефона или QR-кода |
| **Строки** сеансов Pyrogram | Используйте файл Pyrogram с кодом `.session` или сканируйте QR-код с телефона |
| TData с несколькими авторизованными учетными записями | Выйдите из других учётных записей в Telegram Desktop или используйте файл сеанса для каждой учётной записи отдельно |
| Токены ботов | Не поддерживается: TgWitness осуществляет мониторинг в качестве учетной записи пользователя |
| Списки многих учетных записей в форматах CSV/JSON | Импортируйте поддерживаемые файлы сессий через **Аккаунты → Импорт учетных записей** или войдите по номеру телефона / QR-коду в отдельных рабочих пространствах |
| Тестовые сеансы DC или сеансы с ботами | Используйте рабочую учетную запись пользователя |

## Наличие нескольких учётных записей

Нажмите **кнопку «+»** рядом с выбором учетной записи или откройте **«Учетная запись» → «Настройки» → «Настройки подключения» → «Рабочие пространства»**, введите название и войдите в систему.

- Неограниченное количество рабочих пространств, включая основное. Каждое из них имеет собственную сессию, прокси- маршрут, источники, политику сбора данных, журнал, ключ подписи, контрольные точки и настройки экспорта.
- Переключение между отображаемыми рабочими пространствами не приводит к приостановке работы остальных.
- Журнал привязан к учетной записи, с которой он был создан. Для входа под другой учетной записью требуется отдельное рабочее пространство, при этом одна учетная запись не может быть привязана к двум рабочим пространствам.
- Токен главной панели управляет всеми рабочими пространствами. [Предоставленный доступ](https://phishdestroy.github.io/TgWitness/ru/docs/reference/access/) позволяет ограничить доступ других пользователей к выбранным аккаунтам и чатам с помощью отдельных прав доступа и ограничений по продолжительности сеанса.
- **Функция «Учётные записи»** позволяет переименовать рабочую область и удалить добавленную рабочую область вместе с её сессией, журналом, источниками и ключом подписи. Главную рабочую область нельзя удалить с панели.

### Массовый импорт и группы аккаунтов

Воспользуйтесь **меню «Аккаунты» → «Импорт аккаунтов»**, чтобы добавить несколько аккаунтов, сопоставить файлы по базовому имени и просмотреть результаты каждого входа в систему. Каждому аккаунту выделяется собственная рабочая область.

Группа объединяет связанные аккаунты, не объединяя при этом их сессии, ключи или доказательства. **Открыв группу** в разделе **«Аккаунты»,** вы перейдёте на её страницу по адресу `/groups/<id>`:

- **Аккаунты:** маршрут подключения каждого участника, наблюдения и последнее сообщение, с кнопками «Запустить**все»** и **«Приостановить все**».
- **Требует внимания:** аккаунты, из которых вышли, которые недоступны или у которых возникли проблемы с подключением, приемом данных, источником или мультимедиа; каждое имя ведёт к соответствующей карточке.
- **В чатах нескольких учетных записей отображаются:** общие источники, учетные записи, наблюдающие за ними, и перерывы в периоде наблюдения за рабочим пространством (до семи дней). **Экспорт с N учетными записями** распределяет экспорт канала или супергруппы между ними и подписывает один архив.
- **Экспорт группы:** один элемент ZIP, в котором находится подписанный экспорт каждого аккаунта в разделе `accounts/` и `manifest.json` с указанием их SHA-256 и отпечатков ключей, подписанных главным рабочим пространством в `manifest.signature.json`. Проверяйте каждый архив аккаунта отдельно с помощью `python -m tgwitness.verify` и доверенным отпечатком этой учетной записи.

Участники используют общие настройки группы; при этом каждый аккаунт может сохранять свои собственные значения. См. [раздел «Общие настройки»](https://phishdestroy.github.io/TgWitness/ru/docs/reference/settings/#account-groups), [руководство по импорту и группам](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings), а также [панель управления пулом MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Выйти

**«Учётная запись» → «Выйти из Telegram»** (с приостановкой наблюдения) отправляет запрос в Telegram на завершение сеанса, в результате чего он также исчезает из раздела **«Настройки» → «Устройства»** данной учётной записи и удаляется из хранилища рабочего пространства. Журнал, источники, настройки и ключ подписи сохраняются, и в журнале фиксируется факт выхода из системы. Рабочая область по-прежнему принадлежит данной учетной записи: только эта учетная запись может подключиться к ней повторно. Если Telegram не отвечает, сессия всё равно удаляется здесь, и на панели отображается соответствующее сообщение; завершите её в Telegram в разделе **«Настройки» → «Устройства**».

## Обеспечение безопасности файлов учетных записей

- Относитесь к каждому `.session`, TData ZIP, StringSession, Auth Key и JSON-файлу учетной записи как к паролю. TgWitness хранит импортированные данные авторизации в зашифрованном хранилище; вы можете удалить исходные файлы впоследствии.
- Не запускайте одну и ту же авторизацию одновременно в двух программах. Telegram может отозвать её (`AUTH_KEY_DUPLICATED`), и обе копии перестанут работать.
- Сеанс, срок действия которого истек или который был отозван, не может быть восстановлен посредством преобразования. Войдите в систему заново.

## Устранение неполадок

| Сообщение или признак | Что делать |
| --- | --- |
| *Не удаётся прочитать данную сессию. Закройте исходный клиент…* | Файл SQLite открыт или не завершен (файл-сайдкар `-journal`/`-wal`). Корректно закройте исходную программу и скопируйте файл заново. |
| *Поддерживаемые схемы базы данных Telethon SQLite: 7 и 8* / *Pyrogram … 2 и 3* | Файл был создан с использованием очень старой или неизвестной версии библиотеки. Вместо этого войдите в систему с помощью телефона или QR-кода. |
| *Поддерживаются только авторизованные сеансы пользователей в производственной среде* | Файл Pyrogram принадлежит боту или тестовой сети. |
| *Архив TData превышает 512 записей или 32 МиБ* | В ZIP-архив следует включить только файлы `key_datas` и `D877F783D5D3EF8Cs`, а не всю папку. |
| *Не удаётся расшифровать TData. Проверьте локальный пароль на рабочем столе* | Введите локальный пароль Telegram Desktop в поле **«Пароль» или «Текст сеанса**». |
| *Импортируйте по одной учетной записи TData за раз* | В Telegram Desktop было несколько учётных записей; см. раздел [«Неподдерживаемые форматы](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#unsupported-formats)». |
| *Выбранные файлы содержат информацию о различных учетных записях или учетных данных API* | Выберите файлы только из одной учетной записи. |
| *Файл JSON не содержит учетных данных или авторизационных данных для поддерживаемых API* | Проверьте названия полей в [JSON-файле учетной записи](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/#account-json). |
| *Только метаданные API* | В JSON отсутствует сессия. Добавьте файл `.session` или воспользуйтесь номером телефона/QR-кодом. |
| *HEX-код авторизационного ключа должен содержать все 512 шестнадцатеричных символов* | Ключ усечён или содержит символы «`…`». |
| Идентификатор учетной записи не совпадает с импортированной учетной записью | Идентификатор пользователя в файле отличается от того, который указывает Telegram; данный файл относится к другому аккаунту. |
| Данный аккаунт уже принадлежит другому рабочему пространству | Откройте эту рабочую область вместо того, чтобы добавлять аккаунт дважды. |
| Ссылка работает, однако в списке чатов в разделе **«Источники»** отсутствует закрытая группа | Проверьте членство. Программа анализирует первые 1 000 диалогов; увеличьте этот лимит в разделе **«Параметры**». |
| Ошибка подключения через прокси | Проверьте режим маршрутизации и IP. При автоматическом режиме MTProxy происходит попытка подключения к другой рабочей записи. При режиме «Скрыть адрес» происходит ожидание; режим «Прямой» в крайнем случае позволяет подключиться напрямую после заданной задержки. См. [режимы маршрутизации](https://phishdestroy.github.io/TgWitness/ru/docs/reference/connection/#ip-modes). |

См. также: [подключение и безопасность](https://phishdestroy.github.io/TgWitness/ru/docs/reference/connection/) прокси-серверов и шифрования, а также [принципы сбора данных](https://phishdestroy.github.io/TgWitness/ru/docs/reference/collection/), которые фиксируются после входа в систему.
