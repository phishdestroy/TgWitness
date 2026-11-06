# Что проверено

Canonical page: https://phishdestroy.github.io/TgWitness/ru/docs/reference/verification/

Тестирование Telegram в режиме реального времени, автоматические проверки, проверки в браузере и то, что пока остаётся непроверенным.

Each result below applies to its recorded revision and environment. The [current capability matrix](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) separates implementation, published downloads and remaining qualification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Развёртывание на реальном Phala Cloud · 4 ноября 2026 года

`--provider phala --quick-tunnel` запускался на реальной инстанции **Phala Cloud** (`tdx.small`, регион US-WEST-1) с ключом API Phala Cloud для пустой рабочей области, реальным ntfy.sh, GitHub и Intel PCS. CVM установила коммит `df7d860c` (v0.8.1); операции развертывания, проверки и удаления были запущены из командной строки с применением приведённых ниже исправлений. Стоимость семи CVM в совокупности составила около 1,9 цента США.

В ходе первых двух развёртываний было обнаружено пять расхождений по сравнению с моделируемым Phala Cloud. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) теперь воспроизводит каждое из них и завершает работу с ошибкой без соответствующего исправления:

| В Phala Cloud | До исправления | Исправление |
| --- | --- | --- |
| Требуется `compose_file.name` | HTTP 422, ничего не создано | В конфигурацию compose добавлено имя CVM |
| Если не указан пустой скрипт, Phala добавляет свой собственный скрипт предварительной подготовки к тестируемому app-compose (v0.0.20: вход в Docker, `docker compose pull`, пароль root, ключи SSH из `user_config`) | Ошибка `tdx_compose`: код находится за пределами опубликованной конфигурации Docker Compose | app-compose устанавливает значение `pre_launch_script` равным `""`; затем Phala исключает его из процесса |
| В отсутствие `image` Phala выбирает `dstack-dev-0.5.12` — версию для разработчиков с включённым доступом по SSH | `server_state` не проходит проверку. Сама аттестация на этом образе прошла; проблему выявляют только запись провайдера и `tdx_os` | Система развёртки запрашивает производственную сборку текущего выпуска Phala — `dstack-0.5.12` |
| При отключенном шлюзе dstack данные CVM никогда не получают `instance_id` | Развёртывание ожидает 30 минут и завершается с ошибкой | Идентификатор экземпляра считывается из состояния CVM |
| Перезапуски, остановки и запуски являются операциями CVM, а не ревизиями приложения | В `provider_actions` не были указаны перезапуски | Операции также считываются |

Третье развертывание:

- Виртуальная машина CVM запустила `dstack-0.5.12` с отключенным доступом по SSH. Коллектор опубликовал свой подписанный адрес примерно через 1,5 минуты после создания. Затем развертывание прошло успешно для `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, запись аттестации аппаратного обеспечения v4, FMSPC `20a06f000000`, не в режиме отладки, не подлежит миграции, с поддержкой данных криптографической проверки, полученных от Intel), `tdx_compose_hash`, `tdx_compose` (байт за байтом) и `tdx_identity` (ключи KMS).
- Панель по адресу trycloudflare.com отвечала кодом 401 без токена или с неверным токеном, а также кодом 200 при наличии токена панели.
- `verify` с `--source`, установленным на архив GitHub для данного коммита, а отпечаток передан отдельно: сервер, `server_state`, брандмауэр (без шлюза, без публичной конечной точки), журнал провайдера, отчет, отпечаток, хеш источника, загрузка и пять проверок `tdx_*` прошли успешно. Cloudflare и `tdx_os` были недоступны, поэтому результат был «НЕЗАВЕРШЕННЫЙ».
- Два перезапуска через API Phala: каждый раз CVM восстанавливалась менее чем за две минуты с тем же ключом коллектора, новым подписанным адресом и старым адресом, отвечающим кодом 530. `verify` сообщил о новой загрузке и обоих перезапусках как о REVIEW. С помощью `--evidence` были подтверждены подписи журнала и три запуска, каждый из которых сопровождался собственной записью аппаратной аттестации Intel TDX из той же CVM.
- `destroy` удалил только этот CVM. После этого рабочая область оказалась пустой, и адрес панели перестал отвечать.
- При проверке цены в мастере панели было указано значение `tdx.small` по цене 0,058 доллара в час. При использовании неверного ключа выводилось простое сообщение «API-ключ не принят».

Ещё два найденных и затем устранённых недостатка:

- Без ключа адреса `verify` следовал за самым последним корректно сформированным сообщением по теме адреса, которое указано в опубликованной конфигурации Docker Compose. Одно поддельное сообщение направило его на хост, который не существует, и `statement` завершил работу с ошибкой: подделывающий не смог выдать себя за сборщик, но смог заблокировать стороннюю проверку на срок до 12 часов с помощью поддельной временной метки будущего. Теперь сборщик также публикует свой адрес, подписанный собственным ключом; `verify` принимает только такие сообщения, когда их отправляет сборщик, а сообщения упорядочиваются по времени получения программой ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) воспроизводит поддельные записи. CVM запускает этот процесс только из коммита, содержащего его, поэтому коллектор данного запуска ещё не подписал свой адрес, о чём сообщил `verify`.
- `tdx_os` не мог работать без `dstack-mr`, текущая версия которого имеет `measure-os` вместо `measure --json`, указанного в документации. Теперь верификатор самостоятельно вычисляет MRTD и RTMR0-2 на основе опубликованного образа и конфигурации виртуальной машины, включая таблицы ACPI.

Четвёртое развёртывание с этими исправлениями:

- Система развертывания один раз загрузила опубликованный файл `dstack-0.5.12`, сопоставила его с хешем образа ОС, сообщённым виртуальной машиной CVM, и файл `tdx_os` прошел проверку: значения MRTD, RTMR0, RTMR1 и RTMR2 совпали со значениями, рассчитанными для QEMU 8.2.2, 1 vCPU и 2 GiB. Те же вычисления дали иное значение RTMR0 для заявленных 4 GiB, 2 vCPU, QEMU 9.2.1 или второй сетевой карты, а также завершились сбоем при изменении ядра, прошивки или командной строки и для образа для разработчиков.
- `verify` прошел все 16 проверок, включая проверку коннектора быстрого туннеля, поэтому результат составил «PASS». Он сформировал сертификат в форматах HTML и PDF, заверенный цифровыми подписями и временными метками, включая квалифицированную временную метку eIDAS от подразделения по присвоению временных меток правительства Бельгии TSU 202301 (статус присвоен в рамках бельгийского списка доверенных организаций), временную метку FreeTSA и подпись верификатора; `check-report` подтвердил все вышеперечисленное, а также подпись PDF-файла.
- После перезапуска `verify --evidence` подтвердил два запуска: каждый с аттестацией, сформированной внутри CVM, и каждый с загрузкой опубликованного `dstack-0.5.12`. Перезапуск и новая загрузка получили статус REVIEW.
- `destroy` оставил рабочую область пустой.

При пятом развертывании запускался коллектор из коммита `53a0f7e9`, который включает в себя всё вышеперечисленное:

- Коллектор опубликовал свой адрес, подписанный собственным ключом, рядом с сообщением оператора с HMAC. Затем в эту тему были добавлены два поддельных сообщения: одно с обнулённым HMAC, а другое — подписанное другим ключом Ed25519; в обоих случаях указывалось время в 2096 году. `verify` взял адрес, подписанный ключом сборщика, и прошел все 16 проверок; печать вновь содержала квалифицированную бельгийскую временную метку, временную метку FreeTSA и подпись верификатора, а `check-report` подтвердил их.
- После перезапуска сборщик опубликовал новый подписанный адрес: `verify` нашёл его сразу, а функция оператора **Найти текущий адрес** — через 27 секунд по сообщению с HMAC. Оба способа проигнорировали поддельные сообщения. `verify --evidence` подтвердил два запуска с загрузкой `dstack-0.5.12`.
- Система развертывания отобразила сумму, которую Phala выставляет в счёт за CVM, включая диск: 0,06078 доллара в час.

Мастер панели проверили на Phala Cloud дважды: через API заданий и через настоящий браузер Chromium. Проверили цену, создание с выбором коммита в разделе **Дополнительно**, успешное прохождение всех шести проверок аттестации, отображение выставляемой цены в списке серверов (44,37 USD в месяц), функцию **Найти текущий адрес**, скачивание конфигурации compose, учтённой в измерениях, и удаление. Ошибок страницы в браузере не было. После каждого прогона рабочая область оставалась пустой.

Не включено: домен Cloudflare на Phala, учётная запись Telegram на CVM и образ `dstack-0.6.1` . Стоимость, указанная в мастере до создания, включает только стоимость вычислительных ресурсов Phala, поскольку API указывает стоимость дискового пространства только для существующих CVM; в списке серверов отображается стоимость, выставленная к оплате после создания.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Количество |
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

| Проверить | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Тестовый аккаунт Telegram в режиме реального времени · 29 октября 2026 года

Данная учетная запись продолжала функционировать и после приведённого ниже теста. 29 октября в 12:10 по UTC её область действия была расширена на всю учетную запись (каналы, группы, личные чаты и боты); панель запросила подтверждение, и подписанный журнал зафиксировал это действие. К 17:59 по UTC в журнале содержалась следующая информация:

| Запись произведена с 27 октября 21:36 по 29 октября 17:59 по UTC | Количество |
| --- | --- |
| Записи в журнале | 9,968 |
| Новые сообщения | 5,308 |
| из них после перехода на полный аккаунт | 3,878 |
| Удаления | 784 |
| из них были удалены после того, как TgWitness сохранил сообщение | 596 |
| Редактирование | 41 |
| Сообщения, добавленные в ходе повторной проверки | 2,273 |
| Сообщения, которые не удалось обнаружить при повторной проверке | 18 |
| Сообщения, сохраненные с помощью моментальных снимков истории | 242 |
| Сохраненные вложения | 247 |
| Запуск программы сбора данных | 19 |
| Telegram FloodWait приостанавливает работу | 26 |

- Проверка **Verify,** проведённая экспертной группой, подтвердила подписи и цепочку хэшей всех 9 968 записей.
- Сообщения поступили из 2 групп или каналов, а также из 3 личных чатов и от ботов. Была нажата одна кнопка отправки сообщения в разделе **«Чаты»**; запрос и ответ Telegram зафиксированы в журнале.
- Новые чаты добавлялись при повторном сканировании учетной записи сборщиком данных после перезапуска. Функция сохранения ранее отправленных сообщений в новых чатах была отключена (`history = 0`), поэтому данный вопрос здесь не рассматривается.

Не охватываются: реакции, изменения в составе участников, профили пользователей, отправка сообщений, присоединение по приглашению, прокси-серверы, уведомления, бот «witness» и одновременное использование нескольких учетных записей. Публичные файлы содержат только статистические данные.

## Экспорт, защищённый паролем, открывается с помощью libarchive · 29 октября 2026 года

Архив, созданный с использованием кода шифрования экспорта (WinZip AES-256, формат, поддерживаемый 7-Zip и WinRAR ), был открыт с помощью Windows `tar` (bsdtar 3.6.2, libarchive). При вводе правильного пароля извлечённый файл совпал с исходным по SHA-256; при вводе неправильного пароля выдавалось сообщение «Неверная парольная фраза». Сами программы 7-Zip и WinRAR запускаться не стали.

## Тестирование Telegram в режиме реального времени · 27–29 октября 2026 года

Один реальный аккаунт Telegram, авторизованный через встроенный пул пар API, осуществлял запись данных одной супергруппы с **27 октября 21:36 UTC по 29 октября 05:15 UTC**. Сборщик данных запускался 12 раз в течение этого периода.

| Зарегистрировано | Количество |
| --- | --- |
| Записи журнала, включая сигналы о работоспособности и сервисные записи | 2,385 |
| Новые сообщения | 1,291 |
| Удаления | 472 |
| из них были удалены после того, как TgWitness сохранил текст | 347 |
| Редактирование | 12 |
| Сообщения, пропущенные во время остановки, добавлены в ходе повторной проверки | 12 |
| Сохраненные вложения | 17 |
| Вложения не загружены (функция загрузки отключена или файл для загрузки отсутствует) | 14 |
| Telegram FloodWait делает паузы продолжительностью по 3 секунды при повторных проверках | 8 |

- Подписи и цепочка хэшей всех 2 385 записей проверяются с помощью открытого ключа журнала.
- После перезапуска сборщик возобновляет работу с сохраненного состояния обновления (`pts`), и Telethon догоняет отставание; затем в ходе повторной проверки добавляются сообщения, которые все ещё отсутствуют.
- При каждом вызове FloodWait сборщик выжидал заданное время и продолжал работу.
- Учётная запись оставалась авторизованной, и 29 октября произошло повторное подключение к той же сессии.

В рамках данного теста не рассматривались следующие аспекты: одновременное использование нескольких учетных записей, права администратора, прокси-серверы, перебои в работе продолжительностью более нескольких часов, а также полная [процедура приёма данных в режиме реального времени](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Публичные файлы содержат исключительно следующие данные: никаких идентификаторов учетных записей или чатов, сообщений или учетных данных.

## Оценка синтетических локальных возможностей

Команда: `python tools/check_capacity.py --events 10000 --chats 100`

| Показатели | Наблюдаемое |
| --- | --- |
| Входные данные | 10 000 событий, связанных с синтетическими сообщениями, из 100 выбранных синтетических источников |
| Текст сообщения | 400 символов; без мультимедиа и ссылок на сети |
| Импорт данных | 53,273 секунды; 187,7 событий в секунду |
| Задержка обработки | p50 4,162 мс; p95 7,784 мс; максимальное значение 129,118 мс |
| Экспорт в формат ZIP | 19,868 секунд при включенной функции tracemalloc |
| Пиковые значения распределения ресурсов при экспорте в Python | 0,51 МБ; RSS не обрабатывается |
| Размер ZIP-архива | 4 610 962 байт |
| Независимая проверка | Все 10 000 событий прошли проверку |

Данное измерение определяет локальный последовательный путь записи/экспорта на данном хосте под управлением Windows. Оно не учитывает доставку по протоколу MTProto, одновременное использование нескольких учетных записей, ограничения со стороны Telegram, мультимедийные файлы, длительную нагрузку или гарантированное количество реальных чатов. Измерение было проведено до внедрения окончательной версии инструментария для офлайн-проставки временных меток, который не изменяет измеренный путь сообщений.

## Полнотекстовый поиск по миллиону сообщений · 5 ноября 2026 года

Команда: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

Детерминированный подписанный журнал из 1 000 000 синтетических сообщений в 200 чатах (русские словоформы, украинский, английский, китайский, японский языки, ссылки и хендлы) был проиндексирован за 71 секунду; индекс занял 58 MiB помимо журнала объёмом 1,50 GiB. Поиск по наилучшему совпадению занимал от 9 до 190 мс (медиана) по сравнению с 2,4–3,2 секундами для предыдущего поиска по подстроке . Полные результаты, аппаратное обеспечение и ограничения: [полнотекстовый поиск](https://phishdestroy.github.io/TgWitness/ru/docs/reference/search/#benchmark). `tools/test_fulltext.py` также проверяет зашифрованный архив, созданный до полнотекстового поиска (`tools/fixtures/evidence-before-fulltext.zip`) с помощью текущего верификатора, а также текущий архив с помощью собственного верификатора этого архива `verify.py`.

## Остальные требования

Сохраняемый журнал в режиме реального времени фиксирует фактические события сбора данных, редактирования, уведомлений об удалении, вложений, повторных проверок и обработки ограничений скорости. Он не фиксирует исчерпывающие данные о доставке или контролируемую матрицу видимости ролей, субъектов реагирования, длительного ожидания FloodWait, блокировок учетных записей и восстановления после сбоев в работе сети или процессов. Выдача QR-токенов остается отдельным процессом от завершённого подтверждения с помощью мобильного QR-кода.

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

Местные подробные отчёты и скриншоты находятся в папке test-results/ (игнорируются Git). Общедоступные скриншоты в папке docs/assets/ содержат исключительно вымышленные демонстрационные данные.
