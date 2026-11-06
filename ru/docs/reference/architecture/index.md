# Архитектура

Canonical page: https://phishdestroy.github.io/TgWitness/ru/docs/reference/architecture/

Компоненты системы: сборщик, панель управления, журнал, рабочие процессы и модуль «witness», а также схема передачи данных между ними.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Документация](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Development](https://phishdestroy.github.io/TgWitness/assets/chapter-develop.svg)

Один процесс на языке Python обеспечивает работу панели FastAPI и любого количества изолированных рабочих пространств, каждое из которых содержит клиент с учетной записью пользователя Telegram. В базе данных SQLite хранится подписанный журнал событий, доступный только для добавления, а также изменяемые операционные настройки. В зашифрованном хранилище находятся учетные данные API, объект StringSession и ключ подписи. Фронтенд представляет собой простой пакет HTML/CSS/JavaScript: не требуется сборка Node, использование CDN или загрузка фронтенда во время выполнения.

Optional browser and AyuGram recorders run in **separate processes or containers**. The `tgwitness_capture` package owns their event format, keys, artifacts, checkpoint API, independent witness and standalone verifier. It is bundled in the main wheel and can also be installed alone from `addons/capture`, without importing the collector. The main panel's `capture_api.py` and `capture_connections.py` provide administrator-only, workspace-scoped controls under `/api/capture`; connection tokens live in the encrypted vault. No recorder or outbound request starts with the main process. Each explicit command verifies a fresh challenge against the pinned recorder key. Exports are verified before download and keep their original signature; they do not become Telegram message events. Collection sessions and proxy routes stay with each client. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md) for deployment and trust boundaries.

| Модуль | Ответственность |
| --- | --- |
| collector.py | Авторизация, выбор диалога, обновления, моментальные снимки, очередь мультимедиа, мониторинг соединения |
| interactions.py / telegram_client.py | Четко описанные действия панели управления, подписанные подтверждения, постоянные идентификаторы запросов и политика повторных попыток обратного вызова/присоединения на уровне конкретной задачи |
| message_content.py | Наглядное сравнение сообщений без учета метаданных транспортного уровня |
| workers.py | Дождитесь завершения работы процессов экспорта файлов перед очисткой при отмене |
| distributed_export.py / distributed_pages.py | Concurrent chat jobs, per-account reservations, signed checkpoints and cleanup after archive verification |
| distributed_takeout.py / export_timing.py | Resumable Takeout sessions and timings for each start or resume |
| store.py | Транзакции WAL, упорядоченная цепочка событий, фильтры запросов, операционные настройки |
| fulltext.py | Производный полнотекстовый индекс (формы слов, BM25), привязанный к заголовку подписанного журнала; никогда не экспортируется |
| security.py | Создание частных файлов, зашифрованное хранилище, подпись с использованием алгоритма Ed25519, блокировка одного процесса |
| evidence.py | Экспорт полного журнала, производные файлы, контрольные точки, проверка вложений |
| verify.py | Автономный верификатор, доступный только для чтения (stdlib + криптография): архивы, охват, журналы свидетелей и сообщения в каналах, файлы профилей |
| app.py | Аутентифицированный API, жизненный цикл, проверка запросов, статическая панель |
| profiles.py | Средства сбора данных из нескольких учетных записей, механизм управления общим доступом, жизненный цикл на уровне рабочей среды |
| access.py | Гранты с ограниченным охватом, проверка разрешений, ограничения по IP-адресам, ограничения на количество сеансов и консоль администратора |
| proxy_catalog.py | Снимки общедоступных каналов, проверки транспортных протоколов, общий пул прокси-серверов и отбор на основе работоспособности |
| provenance.py | Подписанные измерения идентичности, кода и зависимостей, выполняемые в режиме сбора данных |
| network.py | Проверенные маршруты для каждой рабочей среды; отредактированные данные о статусе и доказательствах; варианты передачи данных через Telethon |
| sessions.py | Офлайн-конвертация проверенных схем баз данных Telethon в формате SQLite в режим «только для чтения» |
| account_import.py | Обнаружение и нормализация поддерживаемых файлов учетных записей и JSON-файлов в памяти |
| tdata.py | Ограниченный современный считыватель ZIP-файлов TData, проверка контрольных сумм и дешифрования, без извлечения данных |
| doctor.py | Проверка готовности на локальном устройстве без сбора данных, входа в систему или установки пакетов |
| download.py | Загрузка аутентифицированных потоковых данных с ограниченным объёмом чтения и без перезаписи |
| monitoring.py | Проверенные политики событий для каждого рабочего пространства и правила для вложений по типам, общие для обработчиков, статусов и подписанных подтверждений получения |
| scope.py | Область мониторинга (выбранные чаты, папка Telegram, весь аккаунт), типы источников, исключения, уровни повторной проверки |
| dossier.py | Профили участников по каждому чату, сформированные на основе сохраненных записей: факты со ссылками на записи, SHA-256/pHash аватаров, извлечение упоминаний |
| witness_api.py | Токены свидетелей, доступные только для чтения, и подписанная заголовочная часть журнала, которую они могут получить |
| witness.py | Процесс независимого фиксирования: собственный ключ и журнал, проверка подлинности, подписанные сообщения в каналах, экспорт |
| alerts.py | Уведомления Apprise и список уведомлений на панели |
| logging_config.py | Ведение журнала консоли и ротация диагностических данных сервера при запуске без оконного интерфейса |
| static/ | Адаптивный интерфейс, локальный шлюз доступа, фильтры, подробная информация, экспорт данных, настройка учетной записи |
| demo.py | Чётко обозначенный синтетический журнал, изолированный от реального массива данных |

Обработчики наблюдения регистрируются до установления соединения. Сбор данных в режиме реального времени ограничивается идентификацией активного клиента, явным состоянием работы, включенными источниками или областью наблюдения (режимы «папка» или «весь аккаунт» добавляют новый чат в качестве источника при его первом обновлении), а также политикой обработки событий. Отклоненные и замененные клиенты не могут передавать обновления в режиме реального времени. Необработанные реакции и обновления членства сохраняют ограничения видимости. Содержимое входящего сообщения и его задание на сохранение в постоянном носителе фиксируются одновременно. Задания сохраняют исходный дескриптор TL и привязывают его хеш к подписанному наблюдению за сообщением. Семантика отправителя, редактора и удаляющего лица разделена.

Каждая рабочая область поддерживает одну учетную запись и имеет собственный каталог и идентификатор для подписи. Главная рабочая область по-прежнему находится в корневом каталоге в целях обеспечения совместимости; дополнительные рабочие области размещаются в profiles/<id>/. Один токен-носитель управляет всей установкой; рабочие области не являются отдельными субъектами авторизации. Блокировки процессов защищают каталоги; блокировки базы данных обеспечивают последовательную вставку событий. Каждое добавление синхронно фиксируется в журнале WAL базы данных SQLite в режиме FULL. Триггеры обновления/удаления событий предотвращают обычные изменения со стороны приложения; администраторы файловой системы остаются в пределах зоны доверия.

API authorization is a bearer token. Login operations are serialized and time-bounded. Account uploads use a dedicated 12 MiB encoded-body limit and an 8 MiB decoded-file limit; normal API requests retain the 16 KiB limit. Conversion runs in a worker thread, keeps uploads in memory, and returns normalized input to the authenticated browser. QR login has a per-workspace candidate, short-lived identifier, waiter task, and explicit cancellation. Only accepted authorization becomes the active client. Telegram FloodWait is returned with a Retry-After value; credentials and raw RPC error messages are not exposed in API errors. Journal exports run outside the async event loop and are serialized per workspace. They stream a stable read snapshot alongside continuing WAL writes. Chat acquisition jobs can run concurrently on separate accounts; each account remains reserved until its job stops. A paused or failed job retains its checkpoints. Successful archive verification permits cleanup of its working files, leaving the ZIP, signed plan and status. Workspace collectors share the process/event loop.

Текущие моментальные снимки истории и обновления в режиме реального времени могут пересекаться. Оба представляют собой отдельные наблюдения, помеченные с указанием источника; дубликаты не сворачиваются автоматически. Не реализовано никаких выводов на основании отсутствующих идентификаторов, сфабрикованного удалённого текста, принудительного перечисления участников или автоматического вступления в группу .

Практическое описание для оператора: [как работает сбор данных](https://phishdestroy.github.io/TgWitness/ru/docs/reference/collection/) и [аккаунты и форматы сессий](https://phishdestroy.github.io/TgWitness/ru/docs/reference/accounts/).

Настройки сети хранятся в зашифрованном хранилище. Применение маршрута приводит к закрытию старых клиентов и отмене незавершённых попыток входа; последующие подключения используют этот маршрут без прямого резервного перехода. При новой установке с использованием внешнего ключа для каждого рабочего пространства генерируется ключ Fernet с помощью алгоритма HKDF-SHA256 на основе файла мастер-ключа и сохраненного случайного солевого значения. Это обеспечивает защиту конфиденциальных данных отдельно от каталога данных, а не содержимого журнала или мультимедиа в виде открытого текста.

Местный демо-доступ использует отдельно сгенерированные процессуальные возможности, но ни в коем случае не настроенный токен панели. Для выдачи и принятия требуется явный демо-режим, синтетический корневой домен без дополнительных рабочих пространств или авторизованной сессии, пир/хост с обратной связью, отсутствие прокси- заголовков переадресации и отсутствие междоменных запросов браузера. Активные API сохраняют аутентификацию по носителю и отклоняют изменения в сборе данных в демонстрационном режиме.
