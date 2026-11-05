# Що було протестовано

Canonical page: https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/

Тестування Telegram у режимі реального часу, автоматизовані перевірки, перевірки в браузері та те, що залишається неперевіреним.

## Розгортання в хмарі Phala Cloud · 4 листопада 2026 року

`--provider phala --quick-tunnel` запускався на реальному **Phala Cloud** (`tdx.small`, регіон US-WEST-1) з ключем API Phala Cloud для порожнього робочого простору, реальним ntfy.sh, GitHub та Intel PCS. CVM встановив коміт `df7d860c` (v0.8.1); операції розгортання, перевірки та видалення були виконані з командного рядка з урахуванням наведених нижче виправлень. Сім CVM обійшлися загалом у близько 1,9 цента США.

Перші два розгортання виявили п’ять відмінностей від імітованого Phala Cloud. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) тепер відтворює кожну з них і завершується з помилкою без відповідного виправлення:

| У Phala Cloud | До виправлення | Виправлення |
| --- | --- | --- |
| `compose_file.name` є обов’язковим | HTTP 422, нічого не створено | Конфігурація Docker Compose містить ім’я CVM |
| Якщо не вказано порожнього значення, Phala додає власний скрипт перед запуском до вимірюваного app-compose (v0.0.20: вхід у Docker, `docker compose pull`, пароль root, SSH-ключі з `user_config`) | `tdx_compose` не працює: код знаходиться поза межами опублікованої конфігурації Docker Compose | app-compose встановлює `pre_launch_script` на `""`; після цього Phala пропускає це значення |
| Без `image` Phala обирає `dstack-dev-0.5.12` — версію для розробки — з увімкненим доступом через SSH | `server_state` не пройшов перевірку. У цьому образі пройшов перевірку лише запис атестації апаратного забезпечення; це видно лише за записом провайдера та `tdx_os` | Під час розгортання запитується виробнича збірка поточного релізу Phala, `dstack-0.5.12` |
| При вимкненому шлюзі dstack у деталях CVM ніколи не з’являється код `instance_id` | Розгортання очікує 30 хвилин і завершується невдачею | Ідентифікатор екземпляра зчитується зі стану CVM |
| Перезапуски, зупинки та запуски є операціями CVM, а не змінами у додатку | `provider_actions` не вказав перезапуски | Операції також читаються |

Третє розгортання:

- CVM запустив `dstack-0.5.12` із вимкненим доступом SSH. Колектор опублікував свою підписану адресу приблизно через 1,5 хвилини після створення. Потім розгортання пройшло для `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, запис атестації апаратного забезпечення v4, FMSPC `20a06f000000`, не в режимі налагодження, не підлягає міграції, підтримує дані криптографічної верифікації, отримані від Intel), `tdx_compose_hash`, `tdx_compose` (байт за байтом) та `tdx_identity` (ключі KMS).
- Панель за адресою trycloudflare.com повертала код 401 без токена або з неправильним токеном, а також код 200 із токеном панелі.
- `verify` із `--source`, налаштованим на архів коміту GitHub, та відбитком, переданим окремо: сервер, `server_state`, брандмауер (без шлюзу, без публічної кінцевої точки), журнал провайдера, виписка, відбиток, хеш джерела, завантаження та п’ять перевірок `tdx_*` пройшли успішно. Cloudflare та `tdx_os` були недоступні, тому результат — INCOMPLETE.
- Два перезапуски через API Phala: щоразу CVM поверталася до роботи менш ніж за дві хвилини з тим самим ключем колектора, новою підписаною адресою та старою, що відповідала кодом 530. `verify` повідомила про новий запуск та обидва перезапуски як REVIEW. За допомогою `--evidence` було підтверджено підписи журналу та три запуски, кожен із яких мав власний запис атестації апаратного забезпечення Intel TDX з того самого CVM.
- Команда `destroy` видалила лише цю CVM. Після цього робоча область була порожньою, а адреса панелі перестала відповідати.
- Перевірка вартості у майстрі панелі показала `tdx.small` за 0,058 долара за годину. При введенні неправильного ключа з’являлося просте повідомлення «API-ключ не прийнято».

Ще два виявлені недоліки, які було виправлено згодом:

- Без ключа адреси `verify` слідував за найновішим коректно сформованим повідомленням на тему адреси, яке надруковано в опублікованій конфігурації Docker Compose. Одне підроблене повідомлення надіслало його на хост, який не існує, і `statement` зазнав невдачі: фальсифікатор не зміг видати себе за колектор, але зміг заблокувати сторонню перевірку на строк до 12 годин за допомогою підробленої майбутньої мітки часу. Тепер колектор також публікує свою адресу, підписану власним ключем; `verify` приймає лише такі публікації, коли їх створює колектор, а публікації сортуються за часом отримання ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) відтворює підроблені публікації. CVM запускає це лише з коміту, що містить його, тому колектор цього запуску ще не підписав свою адресу, і `verify` про це повідомив.
- `tdx_os` не міг працювати без `dstack-mr`, поточна версія якого має `measure-os` замість `measure --json`, зазначеного в документації. Тепер верифікатор самостійно обчислює MRTD та RTMR0-2 на основі опублікованого образу та конфігурації віртуальної машини, включаючи таблиці ACPI.

Четверте розгортання, що включає:

- Deploy один раз завантажив опублікований `dstack-0.5.12`, зіставив його з хешем образу ОС, який повідомив CVM, і `tdx_os` пройшов перевірку: MRTD, RTMR0, RTMR1 та RTMR2 дорівнюють значенням, обчисленим для QEMU 8.2.2, 1 vCPU та 2 ГіБ. Той самий розрахунок дав інше значення RTMR0 для заявлених 4 ГіБ, 2 vCPU, QEMU 9.2.1 або другої мережевої карти, а також завершився невдачею у разі зміни ядра, прошивки чи командного рядка та для образу для розробки.
- `verify` пройшов усі 16 перевірок, включаючи коннектор швидкого тунелю, тому результат був «PASS». Він створив HTML- та PDF-сертифікат, цифровим чином завірений підписами та часовими мітками з кваліфікованою часовою міткою eIDAS від бельгійського урядового підрозділу часового мічення TSU 202301 (статус надано у довірчому списку Бельгії), часовою міткою FreeTSA та підписом верифікатора; `check-report` підтвердив усі ці елементи та підпис у PDF-файлі.
- Після перезапуску `verify --evidence` підтвердив два запуски, кожен із яких супроводжувався атестацією апаратного забезпечення, згенерованою всередині CVM, і кожен із яких був завантажений з опублікованого `dstack-0.5.12`; перезапуск і новий запуск мали статус REVIEW.
- `destroy` залишив робочу область порожньою.

Під час п’ятого розгортання запускався колектор із коміту `53a0f7e9`, який містить усе вищезазначене:

- Колектор опублікував свою адресу, підписану власним ключем, поруч із повідомленням оператора з HMAC. Потім до теми було додано два підроблені повідомлення: одне з обнуленим HMAC, а інше — підписане іншим ключем Ed25519; обидва вказували на час у 2096 році. `verify` взяв адресу, підписану ключем колектора, і пройшов усі 16 перевірок; печатка знову містила кваліфіковану бельгійську мітку часу, мітку часу FreeTSA та підпис верифікатора, а `check-report` підтвердив їх.
- Після перезапуску колектор опублікував нову підписану адресу: `verify` знайшов її одразу, оператор **«Знайти поточну адресу»** — через 27 секунд після публікації HMAC, і обидва проігнорували підроблені публікації. `verify --evidence` підтвердив два запуски, що завантажилися з `dstack-0.5.12`.
- Deploy відобразив суму, яку Phala виставляє за CVM, включаючи диск: 0,06078 долара за годину.

Майстер панелі двічі запускався у Phala Cloud: один раз через API завдань, а інший — через браузер на базі справжнього Chromium: перевірка ціни, створення з комітом під **Advanced**, усі шість перевірок атестації пройдені, список серверів із зазначенням ціни, що підлягає оплаті (44,37 доларів США на місяць), **Find поточну адресу**, завантаження виміряної конфігурації Docker Compose та видалення. У браузері не було виявлено помилок сторінок. Після кожного разу робоча область залишалася порожньою.

Не враховано: домен Cloudflare на Phala, обліковий запис Telegram на CVM та образ `dstack-0.6.1` . Вартість у майстрі перед створенням включає лише вартість обчислювальних ресурсів Phala, оскільки API вказує вартість дискового простору лише для існуючого CVM; у списку серверів показано вартість, що підлягає оплаті після створення.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Кількість |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| Перевірити | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Тест Telegram у реальному часі, весь акаунт · 29 жовтня 2026 року

Цей самий акаунт продовжував працювати після наведеного нижче тесту. 29 жовтня о 12:10 за UTC його сфера дії була розширена на весь акаунт (канали, групи, приватні чати та боти); панель запросила підтвердження, і підписаний журнал зафіксував це. Станом на 17:59 за UTC журнал містив:

| Записано з 27 жовтня 21:36 до 29 жовтня 17:59 за UTC | Кількість |
| --- | --- |
| Записи журналу | 9,968 |
| Нові повідомлення | 5,308 |
| з них після переходу на повний обліковий запис | 3,878 |
| Видалення | 784 |
| з них було видалено після того, як TgWitness зберіг повідомлення | 596 |
| Редагування | 41 |
| Повідомлення, додані в результаті повторної перевірки | 2,273 |
| Повідомлення, які не вдалося знайти під час повторної перевірки | 18 |
| Повідомлення, збережені за допомогою знімків історії | 242 |
| Збережені вкладення | 247 |
| Запуск колектора | 19 |
| Telegram FloodWait призупиняє роботу | 26 |

- Перевірка **Verify,** проведена експертною групою, підтвердила підписи та ланцюжок хеш-кодів усіх 9 968 записів.
- Повідомлення надійшли з 2 груп або каналів та 3 приватних чатів і ботів. Була натиснута одна кнопка повідомлення в **розділі «Чати»**; запит та відповідь Telegram містяться в журналі.
- Нові чати додавалися, коли колектор повторно сканував обліковий запис після перезапуску. Функція збереження попередніх повідомлень нових чатів була вимкнена (`history = 0`), тому вона тут не розглядається.

Не охоплюються: реакції, зміни у складі учасників, профілі користувачів, надсилання повідомлень, приєднання за запрошенням, проксі-сервери, сповіщення, бот-свідок та одночасне використання кількох облікових записів. Публічні файли містять лише статистичні дані.

## Експорт, захищений паролем, відкривається за допомогою libarchive · 29 жовтня 2026 року

Архів, створений за допомогою коду шифрування експорту (WinZip AES-256, формат, який читають 7-Zip та WinRAR ), було відкрито за допомогою Windows `tar` (bsdtar 3.6.2, libarchive). При введенні правильного пароля витягнутий файл збігався з оригінальним SHA-256; при введенні неправильного пароля з’являлося повідомлення «Неправильна парольна фраза». Самі програми 7-Zip та WinRAR не запускалися.

## Тестування Telegram у реальному часі · 27–29 жовтня 2026 року

Один реальний обліковий запис Telegram, увійшовши через вбудований пул пар API, записав дані однієї супергрупи з **27 жовтня 21:36 UTC до 29 жовтня 05:15 UTC**. Колектор було запущено 12 разів протягом цього періоду.

| Записано | Кількість |
| --- | --- |
| Записи журналу, включаючи сигнали активності та записи про роботу сервісу | 2,385 |
| Нові повідомлення | 1,291 |
| Видалення | 472 |
| з них було видалено після того, як TgWitness зберіг текст | 347 |
| Редагування | 12 |
| Повідомлення, пропущені під час зупинки, додані під час повторної перевірки | 12 |
| Збережені вкладення | 17 |
| Вкладення не завантажено (завантаження вимкнено або немає файлу для завантаження) | 14 |
| Telegram FloodWait робить паузи тривалістю по 3 секунди під час повторних перевірок | 8 |

- Підписи та ланцюжок хеш-кодів усіх 2 385 записів перевіряються за допомогою відкритого ключа журналу.
- Після перезапуску колектор продовжує роботу зі збереженого стану оновлення (`pts`), а Telethon наздоганяє пропущене; під час повторної перевірки додаються повідомлення, яких ще бракує.
- При кожному виклику FloodWait колектор очікував протягом заданого часу, а потім продовжував роботу.
- Акаунт залишався увійшов у систему, і та сама сесія відновилася 29 жовтня.

Цей тест не охоплює: одночасне використання кількох облікових записів, ролі адміністратора, проксі-сервери, перебої в роботі, тривалістю понад кілька годин, а також повну [процедуру прийняття даних у режимі реального часу](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Публічні файли містять лише такі дані: жодних ідентифікаторів облікових записів чи чатів, повідомлень або уповноважень.

## Оцінка синтетичних місцевих можливостей

Команда: `python tools/check_capacity.py --events 10000 --chats 100`

| Показники | Спостереження |
| --- | --- |
| Вхідні дані | 10 000 синтезованих подій повідомлень із 100 вибраних синтезованих джерел |
| Текст повідомлення | 400 символів; без медіафайлів та посилань на мережі |
| Імпорт даних | 53,273 секунди; 187,7 подій на секунду |
| Затримка обробки | p50 4,162 мс; p95 7,784 мс; максимум 129,118 мс |
| Експорт у форматі ZIP | 19,868 секунди з увімкненою функцією tracemalloc |
| Максимальні відстежені обсяги експорту Python | 0,51 Мб; RSS не обробляється |
| Розмір ZIP-архіву | 4 610 962 байт |
| Незалежна перевірка | Усі 10 000 подій перевірено |

Цей показник вимірює локальний послідовний шлях запису/експорту на цьому хості під управлінням Windows. Він не вимірює доставку через MTProto, одночасну роботу декількох облікових записів, обмеження пропускної здатності Telegram, мультимедіа, тривалі робочі навантаження або гарантовану кількість реальних чатів. Вимірювання було проведено до впровадження остаточної версії інструменту для офлайн-маркування часом, який не змінює виміряний шлях повідомлень.

## Решта кваліфікаційних вимог

Збережений журнал у режимі реального часу фіксує факти збору, редагування, повідомлення про видалення, вкладення, повторні перевірки та обробку обмежень швидкості. Він не фіксує вичерпну інформацію про доставку або контрольовану матрицю видимості ролей, суб’єктів, що реагують, тривалого FloodWait, блокування облікових записів та відновлення після перебоїв у роботі мережі/процесів. Видача QR-токенів залишається окремим процесом від завершеного підтвердження за допомогою мобільного QR-коду.

Створення/запуск у Docker, інсталяція на Linux/macOS, стійке високе навантаження, незалежна перевірка безпеки, реальна незалежна реакція TSA, перевірка анулювання/архівування сертифікатів та криміналістична сертифікація залишаються поза межами зафіксованої кваліфікації. Збереження стану MTProto та функція наздоганяння реалізовані; атомарне стійке відтворення залишається нереалізованим. Збір журналів адміністратора, додаткові списки реакторів та пріоритетне коротке опитування залишаються окремими функціями. Дивіться [актуальну версію](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) матриці контрольованої кваліфікації.

Детальні локальні квитанції та скріншоти знаходяться в папці test-results/ (ігнорується Git). Публічний скріншот у папці docs/assets/ містить лише вигадані демонстраційні дані.
