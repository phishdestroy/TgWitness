# Архітектура

Canonical page: https://phishdestroy.github.io/TgWitness/uk/docs/reference/architecture/

Компоненти колектора, панелі, журналу, робочих процесів та свідка, а також схема передачі даних між ними.

Один процес Python обслуговує панель FastAPI та будь-яку кількість ізольованих робочих просторів, кожен із яких має клієнт облікового запису користувача Telethon. SQLite зберігає підписаний журнал подій, до якого можна лише додавати записи, та змінні операційні налаштування. У зашифрованому сховищі зберігаються облікові дані API, StringSession та ключ підпису. Інтерфейс користувача — це простий пакет HTML/CSS/JavaScript: не потрібні збірка на Node, CDN або завантаження інтерфейсу під час виконання.

Optional browser and AyuGram recorders run in **separate processes or containers**. The `tgwitness_capture` package owns their event format, keys, artifacts, checkpoint API, independent witness and standalone verifier. It is bundled in the main wheel and can also be installed alone from `addons/capture`, without importing the collector. The main panel's `capture_api.py` and `capture_connections.py` provide administrator-only, workspace-scoped controls under `/api/capture`; connection tokens live in the encrypted vault. No recorder or outbound request starts with the main process. Each explicit command verifies a fresh challenge against the pinned recorder key. Exports are verified before download and keep their original signature; they do not become Telegram message events. Collection sessions and proxy routes stay with each client. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md) for deployment and trust boundaries.

| Модуль | Відповідальність |
| --- | --- |
| collector.py | Авторизація, вибір діалогів, оновлення, знімки екрана, черга мультимедіа, моніторинг з’єднання |
| interactions.py / telegram_client.py | Чітко визначені дії панелі, підписані квитанції, постійні ідентифікатори запитів та політика повторних спроб зворотного виклику/приєднання на рівні завдань |
| message_content.py | Наочне порівняння повідомлень, без урахування метаданих про транспортний доступ |
| workers.py | Дочекатися завершення роботи процесів експорту файлів перед очищенням після скасування |
| distributed_export.py / distributed_pages.py | Concurrent chat jobs, per-account reservations, signed checkpoints and cleanup after archive verification |
| distributed_takeout.py / export_timing.py | Resumable Takeout sessions and timings for each start or resume |
| store.py | Транзакції WAL, впорядкований ланцюжок подій, фільтри запитів, операційні налаштування |
| fulltext.py | Похідний повнотекстовий індекс (словоформи, BM25), прив’язаний до заголовка підписаного журналу; ніколи не експортується |
| security.py | Створення приватних файлів, зашифроване сховище, підпис за алгоритмом Ed25519, блокування одного процесу |
| evidence.py | Експорт повного журналу, похідні файли, контрольні точки, перевірка вкладень |
| verify.py | Автономний верифікатор, доступний лише для читання (stdlib + криптографія): архіви, охоплення, журнали свідків та публікації в каналах, файли профілів |
| app.py | Аутентифікований API, життєвий цикл, перевірка запитів, статична панель |
| profiles.py | Колектори з кількома обліковими записами, контролер спільного доступу, життєвий цикл для кожного робочого простору |
| access.py | Гранти з обмеженим обсягом, перевірка дозволів, обмеження за IP-адресами, обмеження сеансів та консоль адміністратора |
| proxy_catalog.py | Знімки публічних каналів, перевірки каналу передачі даних, спільний пул проксі-серверів та відбір на основі працездатності |
| provenance.py | Підписані вимірювання ідентичності, коду та залежностей під час збору даних |
| network.py | Перевірені маршрути для кожного робочого простору; відредагований статус та докази; варіанти передачі даних через Telethon |
| sessions.py | Офлайн-конвертація перевірених схем Telethon SQLite у режим «тільки для читання» |
| account_import.py | Виявлення та нормалізація у пам’яті файлів підтримуваних облікових записів та JSON |
| tdata.py | Обмежений сучасний ZIP-зчитувач TData, перевірка контрольної суми та розшифрування, без розпакування |
| doctor.py | Перевірка готовності на місцевому рівні без збору даних, входу в систему чи встановлення програмного забезпечення |
| download.py | Завірений потоковий експорт із обмеженим читанням та без перезапису |
| monitoring.py | Перевірені правила щодо подій для кожного робочого простору та правила для вкладених файлів за типом, спільні для обробників, статусів та підписаних підтверджень отримання |
| scope.py | Обсяг спостереження (обрані чати, папка Telegram, весь обліковий запис), типи джерел, виключення, рівні повторної перевірки |
| dossier.py | Профілі користувачів за кожним чатом, створені на основі збережених записів: факти з посиланнями на записи, SHA-256/pHash аватарів, виокремлення згадок |
| witness_api.py | Токени свідків, доступні лише для читання, та підписаний заголовок журналу, який вони можуть отримати |
| witness.py | Процес незалежного свідчення: власний ключ і журнал, перевірка авторизації, підписані публікації в каналах, експорт |
| alerts.py | Сповіщення Apprise та список сповіщень на панелі |
| logging_config.py | Реєстрація в консолі та циклічна діагностика сервера для запуску без вікон |
| static/ | Адаптивний інтерфейс, локальний доступ, фільтри, детальна інформація, експорт даних, налаштування облікового запису |
| demo.py | Чітко позначений синтетичний журнал, ізольований від реального масиву даних |

Обробники спостереження реєструються перед підключенням. Збір даних у реальному часі обмежується ідентифікацією активного клієнта, явним станом роботи, увімкненими джерелами або сферою спостереження (режими «папка» або «весь обліковий запис» додають новий чат як джерело під час його першого оновлення), а також політикою подій. Відхилені та замінені клієнти не можуть надсилати оновлення в реальному часі. Необроблені реакції та оновлення членства зберігають обмеження видимості. Вміст вхідного повідомлення та завдання щодо його збереження на стійкому носії фіксуються разом. Завдання зберігають оригінальний дескриптор TL та прив’язують його хеш до підписаного спостереження за повідомленням. Семантика відправника/редактора/видаляча розділена.

Кожен робочий простір підтримує один обліковий запис і має власний каталог та ідентифікатор підпису. Головний робочий простір залишається в кореневому каталозі для забезпечення сумісності; додаткові робочі простори розміщуються в profiles/<id>/. Один токен-носій контролює всю інсталяцію; робочі простори не є окремими орендарями авторизації. Блокування процесів захищають каталоги; блокування бази даних серіалізують вставку подій. Кожне додавання синхронно фіксується у WAL SQLite у повному синхронному режимі. Тригери оновлення/видалення подій запобігають звичайним редагуванням з боку додатків; адміністратори файлової системи залишаються в межах зони довіри.

API authorization is a bearer token. Login operations are serialized and time-bounded. Account uploads use a dedicated 12 MiB encoded-body limit and an 8 MiB decoded-file limit; normal API requests retain the 16 KiB limit. Conversion runs in a worker thread, keeps uploads in memory, and returns normalized input to the authenticated browser. QR login has a per-workspace candidate, short-lived identifier, waiter task, and explicit cancellation. Only accepted authorization becomes the active client. Telegram FloodWait is returned with a Retry-After value; credentials and raw RPC error messages are not exposed in API errors. Journal exports run outside the async event loop and are serialized per workspace. They stream a stable read snapshot alongside continuing WAL writes. Chat acquisition jobs can run concurrently on separate accounts; each account remains reserved until its job stops. A paused or failed job retains its checkpoints. Successful archive verification permits cleanup of its working files, leaving the ZIP, signed plan and status. Workspace collectors share the process/event loop.

Поточні знімки історії та оновлення в режимі реального часу можуть перекриватися. Обидва є окремими спостереженнями, позначеними за джерелом; дублікати не приховуються автоматично. Не здійснюється жодних висновків на основі відсутніх ідентифікаторів, сфабрикованого видаленого тексту, примусового переліку учасників або автоматичного приєднання до групи .

Пояснення для операторів див. у розділах [«Як працює збір даних](https://phishdestroy.github.io/TgWitness/uk/docs/reference/collection/)» та [«Формати облікових записів і сеансів](https://phishdestroy.github.io/TgWitness/uk/docs/reference/accounts/)».

Конфігурація мережі зберігається у зашифрованому сховищі. Застосування маршруту закриває старі клієнти та скасовує незавершені входи; подальші з’єднання використовують цей маршрут без прямого резервного варіанту. Під час нової інсталяції з зовнішнім ключем ключ Fernet для кожного робочого простору генерується за допомогою алгоритму HKDF-SHA256 на основі файлу головного ключа та збереженого випадкового солі. Це забезпечує захист секретних даних окремо від каталогу даних, а не вмісту журналу чи медіафайлів у вигляді відкритого тексту.

Місцевий демо-доступ використовує окремо згенеровану здатність процесу, ніколи не використовуючи налаштований токен панелі. Для видачі та прийняття необхідний явний демо-режим, синтетичний кореневий домен без додаткових робочих просторів або авторизованої сесії, пеер/хост із зворотним зв’язком, відсутність проксі- заголовків переадресації та відсутність міждоменних запитів браузера. Активні API зберігають аутентифікацію за носієм та відхиляють зміни у зборі даних у демо-режимі.
