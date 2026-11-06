# Безопасность и обращение с данными

Canonical page: https://phishdestroy.github.io/TgWitness/ru/docs/reference/security/

Модель угроз, модель доступа, защита конфиденциальных данных в состоянии покоя, сетевая уязвимость, импорт сеансов и порядок сообщения об уязвимостях.

This page describes access, storage and network protection in a local or server workspace. For collection on a GitHub runner or in an Intel TDX confidential VM, see the [verification modes](https://phishdestroy.github.io/TgWitness/ru/docs/reference/evidence/#verification-scope), which add checks of the collection environment. Account connections, notifications, timestamps, off-site copies and witnesses have their own routing settings.

| Область | Вкратце |
| --- | --- |
| Доступ | Ключ администратора, а также ограниченный доступ к аккаунтам и чатам, семь уровней прав доступа и сеансы с возможностью отзыва; по умолчанию используется localhost |
| Секреты в состоянии покоя | Настройки сеанса, пары API, ключа подписи и прокси шифруются с помощью алгоритма Fernet |
| Сообщения и мультимедиа | Данные хранятся в незашифрованном виде: рекомендуется использовать шифрование диска и строгие настройки прав доступа |
| Целостность | Цепочка хешей SHA-256 и подпись Ed25519 на каждой записи |
| Условия локального режима | The host administrator controls the workspace and its signing key; independent checkpoints retain an earlier journal boundary |

Информацию об отчетах об уязвимостях см. в [политике безопасности](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

## Модель доступа

Токен главной панели предоставляет полный контроль. Другие пользователи могут получить [доступ с ограниченным объемом](https://phishdestroy.github.io/TgWitness/ru/docs/reference/access/) полномочий: выбранные рабочие пространства и чаты, разрешения, срок действия, ограничения по IP-адресам, ограничения на вход в систему и отзывные сессии. Пользователь с доступом, ограниченным чатом, не может выполнять операции в масштабе всего рабочего пространства, даже если соответствующее разрешение отмечено. Рабочие пространства используют общий процесс и не изолируют данные от администратора хоста.

По умолчанию панель прослушивает соединения на localhost. При входе через браузер токен доступа обменивается на сессионные учетные данные; браузер отправляет их в виде токена «bearer». Он хранится в sessionStorage, а не в файле cookie аутентификации. Блокировка или выход из системы очищает сессию браузера. Закрытие браузера или завершение сессии не останавливает сбор данных.

Выданные токены и учетные данные сеанса хранятся в виде хэшей в зашифрованном хранилище. Отзыв токена приводит к завершению связанных с ним сеансов; изменения прав доступа влияют на последующие запросы. Загруженные файлы невозможно отозвать. Администратор может ограничить также свои собственные сеансы браузера, однако скрипты, использующие токен главной панели напрямую, сохраняют полный доступ и обходят эти ограничения сеансов браузера.

Число неудачных попыток аутентификации ограничивается по адресу клиента. При ограничении по IP-адресу используется адрес, видимый приложению; прежде чем полагаться на это ограничение, проверьте поведение обратного прокси-сервера. Учетные данные Witness остаются отдельными учетными данными для проверки работоспособности и контроля состояния, доступными только для чтения.

### Доступ к демо-версии

`/api/demo-access` представляет собой намеренно неаутентифицированный начальный код для явно запущенной, изолированной синтетической демонстрационной версии. Он предоставляет отдельную возможность, действующую в течение срока жизни процесса, но никогда не предоставляет реальный токен панели или переопределение TGWITNESS_TOKEN. Для выдачи и использования требуются узел loopback и хост, отсутствие перенаправленных заголовков и отсутствие междоменных запросов. Дополнительные рабочие пространства или авторизованная сессия блокируют этот путь. Активные рабочие пространства никогда не выдают данную возможность. Демонстрационная версия не может связывать учетные записи или изменять настройки сбора данных.

## Содержание панелей и экспорт данных

На данном сайте не используются внешние шрифты, аналитические инструменты, ресурсы CDN или встроенные удалённые мультимедийные файлы. Текст из Telegram вставляется в виде текста, а не HTML. Загруженные вложения предоставляются в виде двоичных вложений. При экспорте в формат JSONL сохраняются исходные строки; в HTML они кодируются; ячейки CSV, которые могут содержать формулы, снабжаются префиксом в виде апострофа.

При экспорте исключаются секретные данные аутентификации и подписи, однако намеренно сохраняются собранные исходные метаданные, идентификаторы, а также, возможно, личный или конфиденциальный контент. В исходных метаданных могут присутствовать хэши доступа к Telegram и ссылки на файлы.

## Секреты в состоянии покоя

Telegram API credentials, the session and signing key are encrypted with Fernet. For local messages and media, encryption is provided by the host's disk or volume; the workspace stores ordinary files. Exports can use a password-protected AES-256 ZIP, and off-site copies use AES-256-GCM.

The vault key defaults to the protected data directory. Use an external master-key file below to store it separately. On Unix, new private-key files use mode 0600 and new data directories use 0700; on Windows, set the directory ACL for the service account and authorized administrators. Existing directory permissions are retained.

### Внешний мастер-ключ

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode. Disk encryption protects the local message and media files in either mode; see [connection and data protection](https://phishdestroy.github.io/TgWitness/ru/docs/reference/connection/) for setup details.

## Прокси-серверы и сетевые маршруты

Настройки прокси зашифрованы в хранилище. Пароли и секретные ключи MTProxy не возвращаются API и не записываются в записи доказательств. Каждая рабочая область выбирает свой маршрут Telegram и [режим IP](https://phishdestroy.github.io/TgWitness/ru/docs/reference/connection/#ip-modes).

**Функция «Скрыть адрес»** отключает прямой резервный доступ к Telegram и требует использования прокси для внешних HTTP-запросов. Явно выбранный режим резервного доступа разрешает прямой доступ к Telegram после задержки; режим «туннель/VPN» разрешает прямые маршруты. Выбор режима «туннель» не влечёт за собой установку или проверку VPN. Эти настройки не контролируют весь трафик компьютера, браузеры, менеджеры пакетов или разрешение DNS локального прокси-хоста.

MTProxy передаёт исключительно трафик Telegram. Для внешних запросов можно использовать отдельный прокси SOCKS5/HTTP, маршрут SOCKS5/HTTP рабочей среды или разрешённый прямой маршрут; их также можно отключить. Независимый свидетель имеет собственные настройки транспорта. Обычная аутентификация SOCKS5/HTTP CONNECT не шифруется самими этими протоколами прокси. Поддельные секретные ключи TLS для MTProxy по-прежнему не поддерживаются.

## Вход в систему и импорт сеансов

Преобразованные файлы .tgwitness-session содержат секретный ключ авторизации в виде открытого текста до тех пор, пока они не будут загружены и сохранены в хранилище. Автономный интерфейс командной строки (CLI) поддерживает проверенные схемы Telethon. Функция импорта через панель управления дополнительно поддерживает форматы Pyrogram SQLite, современный ZIP-файл TData для одной учетной записи, а также задокументированные входы в формате JSON. Она проходит аутентификацию, ограничена четырьмя файлами / 8 MiB, и обрабатывает загрузки в памяти без извлечения архивов или сохранения исходных файлов. Нормализованные учетные данные возвращаются исключительно запрашивающему авторизованному браузеру; они сохраняются в зашифрованном хранилище после успешной авторизации в Telegram. Обеспечьте защиту исходных и преобразованных файлов и предотвратите клонирование авторизационных данных параллельными клиентами.

В процессе обработки данных проверяются контрольные суммы контейнеров, хэши локального дешифрования и длины структур. Предоставленный локальный пароль для Desktop используется временно и не сохраняется. Данный ограниченный парсер не гарантирует совместимость со всеми версиями Desktop. Изображения QR-кодов генерируются локально, содержат краткосрочные токены входа в Telegram и никогда не отправляются во внешний сервис рендеринга. Блокировка, переключение рабочего пространства, новый вход в систему и изменение маршрута отменяют ожидающие попытки сканирования QR-кода. Перезагрузка или закрытие вкладки может привести к тому, что попытка останется в ожидании до истечения срока действия. Успешный вход с помощью QR-кода по-прежнему обеспечивает привязку учетной записи. Размер обычных тел запросов API по-прежнему ограничен 16 КиБ; маршрут импорта с аутентификацией принимает до 12 МиБ закодированного JSON, при этом отдельно применяется ограничение на размер декодированного файла.

Коды входа и пароли двухэтапной аутентификации Telegram не сохраняются. Состояние номера телефона/хеша кода хранится в памяти во время авторизации. Сеансы Telegram предоставляют доступ к учётной записи; ни в коем случае не загружайте каталог данных, сеанс, токен, ключ хранилища или закрытый ключ подписи на GitHub.

## Журналы и передача данных

Стандартный ответ API при проверке достоверности заменяется таким образом, чтобы он не повторял значения учетных данных. Регистрация доступа к приложению отключена. Не настраивайте обратный прокси-сервер так, чтобы он регистрировал заголовки авторизации или тела запросов. Протокол HTTP передаёт токены и секретные данные для входа в виде открытого текста: всегда используйте HTTPS или SSH-туннель при выходе за пределы localhost.

## Ограничения целостности

Local verification checks record signatures, the hash chain, attachments and the export manifest. The administrator holds the local signing key and can create another signed journal; an independently retained checkpoint detects replacement of the prefix it covers. Keep the key fingerprint and checkpoints with the recipient or an independent witness.

For independently checked collection, choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/ru/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Their verifiers check workflow provenance or hardware measurements in addition to archive integrity. Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies; the [evidence format](https://phishdestroy.github.io/TgWitness/ru/docs/reference/evidence/#verification-scope) describes the checks for each mode.

## Если у вас возникли подозрения о наличии проблемы

Preserve the original data directory and use a separate copy for analysis. Report the affected version, operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), keeping account data and credentials private.
