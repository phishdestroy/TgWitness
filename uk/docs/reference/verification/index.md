# Що було протестовано

Canonical page: https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/

Тестування Telegram у режимі реального часу, автоматизовані перевірки, перевірки в браузері та те, що залишається неперевіреним.

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
