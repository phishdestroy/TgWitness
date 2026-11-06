# Що було протестовано

Canonical page: https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/

Тестування Telegram у режимі реального часу, автоматизовані перевірки, перевірки в браузері та те, що залишається неперевіреним.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Документація](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/uk/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Updated 6 November 2026.** Results are tied to the revision, environment and workload recorded for each run. [Current capabilities](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describes the available workflows; this page records what has actually been checked.

[Performance graphs](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Signed English audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Downloadable measurements](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Latest evidence | Результат | Сфера застосування |
| --- | --- | --- |
| Release audit · 6 Nov | 1,461 core tests passed; 37 platform skips | Source `92e539af40d8`; open findings retained |
| Fresh exports · 6 Nov | 127.713 and 141.781 records/s, complete cycle | Two accounts per server; text and metadata through WARP |
| Retained archives · 6 Nov | 48 archives; 3,598,381 records verified | Existing archives checked against pinned workspace keys |
| Trusted Live · 5 Nov | Guarded CPU recording and WARP checks | Official Desktop login and native export remain unqualified |
| Phala / Intel TDX · 4 Nov | All 16 verifier checks passed on later runs | Historical deployment; no Telegram account on the CVM |

**On this page**

- [Release audit and fresh exports · 6 November 2026](https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu and WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live Phala Cloud deployment · 4 November 2026](https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Live server journal inventory · 1 November 2026](https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Recent offline and fault-injection checks · 1 November 2026](https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live Telegram test, whole account · 29 October 2026](https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Password-protected export opened with libarchive · 29 October 2026](https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live Telegram test · 27 to 29 October 2026](https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetic local capacity measurement](https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Full-text search on one million messages · 5 November 2026](https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Remaining qualification](https://phishdestroy.github.io/TgWitness/uk/docs/reference/verification/#remaining-qualification)

## Release audit and fresh exports · 6 November 2026

The audit used v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. Installed-package smoke checks passed on three servers. The signed report retains the state observed at that time.

[![Acquisition and complete export rates for two fresh workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Workload | Записи | Acquisition | Complete cycle | Complete-cycle rate |
| --- | --- | --- | --- | --- |
| Server A · two accounts | 27,030 | 189.043 s | 211.647 s | 127.713 records/s |
| Server B · two accounts | 29,299 | 182.513 s | 206.650 s | 141.781 records/s |

Both exports began without resume, excluded attachments and avatars, and ended with zero duplicate or reused records. The complete cycle includes preparation, acquisition, selection, packaging and archive verification. Server A also ran a protected-chat read check. Four FloodWait events on A and three on B were respected. These observations do not establish a general throughput guarantee.

| Перевірити | Результат | Qualification |
| --- | --- | --- |
| Core pytest | 1,461 passed | 37 platform skips |
| Browser / browser UX / evidence / site | 102 / 66 / 15 / 9 passed | These programs overlap other tests; counts are not additive |
| Capture addon | 124 passed | Three Official Web checks blocked by the required Chromium sandbox |
| API authorization | 269 routes; 538 requests passed | Missing credentials and revoked access |
| Retained archives | 48 of 48 verified | 3,598,381 records; pinned workspace keys |
| Live fleet read checks | 24 of 40 profiles passed | 16 WARP routes failed qualification; those profiles were not connected |

The [signed report](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) records all open findings, including three defects in an unpublished secret-chat snapshot absent from the audited main build. The earlier [public-history qualification](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) used a different revision and workload; its rates must not be combined with this comparison.

Verify the original report using the [pinned key and verifier](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Its signature protects the operator's report from alteration. It is not independent attestation, proof of Telegram authorship or GDPR certification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Розгортання в хмарі Phala Cloud · 4 листопада 2026 року

**Historical result:** later deployments passed all 16 verifier checks, including Intel TDX and the quick tunnel. Restart evidence, signed address discovery and report timestamps were checked separately. Each test CVM was removed after its run.

| Налаштування | Recorded value |
| --- | --- |
| Провайдер | Phala Cloud · `tdx.small` · US-WEST-1 |
| Розгортання | `--provider phala --quick-tunnel`; initially empty workspace |
| Initial collector | `df7d860c` · v0.8.1 |
| Collector with all fixes | `53a0f7e9` |
| Production guest | `dstack-0.5.12`; SSH access disabled |
| External services | ntfy.sh, GitHub and Intel PCS |
| Observed cost | Seven CVMs, about 1.9 US cents together; historical test pricing |

The sequence below separates initial failures, fixes and completed checks. No Telegram account was connected to these CVMs.

**Deployments 1–2 · provider differences and regression checks**

Перші два розгортання виявили п’ять відмінностей від імітованого Phala Cloud. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) тепер відтворює кожну з них і завершується з помилкою без відповідного виправлення:

| У Phala Cloud | До виправлення | Виправлення |
| --- | --- | --- |
| `compose_file.name` є обов’язковим | HTTP 422, нічого не створено | Конфігурація Docker Compose містить ім’я CVM |
| Якщо не вказано порожнього значення, Phala додає власний скрипт перед запуском до вимірюваного app-compose (v0.0.20: вхід у Docker, `docker compose pull`, пароль root, SSH-ключі з `user_config`) | `tdx_compose` не працює: код знаходиться поза межами опублікованої конфігурації Docker Compose | app-compose встановлює `pre_launch_script` на `""`; після цього Phala пропускає це значення |
| Без `image` Phala обирає `dstack-dev-0.5.12` — версію для розробки — з увімкненим доступом через SSH | `server_state` не пройшов перевірку. У цьому образі пройшов перевірку лише запис атестації апаратного забезпечення; це видно лише за записом провайдера та `tdx_os` | Під час розгортання запитується виробнича збірка поточного релізу Phala, `dstack-0.5.12` |
| При вимкненому шлюзі dstack у деталях CVM ніколи не з’являється код `instance_id` | Розгортання очікує 30 хвилин і завершується невдачею | Ідентифікатор екземпляра зчитується зі стану CVM |
| Перезапуски, зупинки та запуски є операціями CVM, а не змінами у додатку | `provider_actions` не вказав перезапуски | Операції також читаються |

**Deployment 3 · attestation, access checks and restart evidence**

- CVM запустив `dstack-0.5.12` із вимкненим доступом SSH. Колектор опублікував свою підписану адресу приблизно через 1,5 хвилини після створення. Потім розгортання пройшло для `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, запис атестації апаратного забезпечення v4, FMSPC `20a06f000000`, не в режимі налагодження, не підлягає міграції, підтримує дані криптографічної верифікації, отримані від Intel), `tdx_compose_hash`, `tdx_compose` (байт за байтом) та `tdx_identity` (ключі KMS).
- Панель за адресою trycloudflare.com повертала код 401 без токена або з неправильним токеном, а також код 200 із токеном панелі.
- `verify` із `--source`, налаштованим на архів коміту GitHub, та відбитком, переданим окремо: сервер, `server_state`, брандмауер (без шлюзу, без публічної кінцевої точки), журнал провайдера, виписка, відбиток, хеш джерела, завантаження та п’ять перевірок `tdx_*` пройшли успішно. Cloudflare та `tdx_os` були недоступні, тому результат — INCOMPLETE.
- Два перезапуски через API Phala: щоразу CVM поверталася до роботи менш ніж за дві хвилини з тим самим ключем колектора, новою підписаною адресою та старою, що відповідала кодом 530. `verify` повідомила про новий запуск та обидва перезапуски як REVIEW. За допомогою `--evidence` було підтверджено підписи журналу та три запуски, кожен із яких мав власний запис атестації апаратного забезпечення Intel TDX з того самого CVM.
- Команда `destroy` видалила лише цю CVM. Після цього робоча область була порожньою, а адреса панелі перестала відповідати.
- Перевірка вартості у майстрі панелі показала `tdx.small` за 0,058 долара за годину. При введенні неправильного ключа з’являлося просте повідомлення «API-ключ не прийнято».

**Follow-up fixes · signed address discovery and OS measurements**

- Без ключа адреси `verify` слідував за найновішим коректно сформованим повідомленням на тему адреси, яке надруковано в опублікованій конфігурації Docker Compose. Одне підроблене повідомлення надіслало його на хост, який не існує, і `statement` зазнав невдачі: фальсифікатор не зміг видати себе за колектор, але зміг заблокувати сторонню перевірку на строк до 12 годин за допомогою підробленої майбутньої мітки часу. Тепер колектор також публікує свою адресу, підписану власним ключем; `verify` приймає лише такі публікації, коли їх створює колектор, а публікації сортуються за часом отримання ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) відтворює підроблені публікації. CVM запускає це лише з коміту, що містить його, тому колектор цього запуску ще не підписав свою адресу, і `verify` про це повідомив.
- `tdx_os` не міг працювати без `dstack-mr`, поточна версія якого має `measure-os` замість `measure --json`, зазначеного в документації. Тепер верифікатор самостійно обчислює MRTD та RTMR0-2 на основі опублікованого образу та конфігурації віртуальної машини, включаючи таблиці ACPI.

**Deployment 4 · all 16 checks, report seals and restart verification**

- Deploy один раз завантажив опублікований `dstack-0.5.12`, зіставив його з хешем образу ОС, який повідомив CVM, і `tdx_os` пройшов перевірку: MRTD, RTMR0, RTMR1 та RTMR2 дорівнюють значенням, обчисленим для QEMU 8.2.2, 1 vCPU та 2 ГіБ. Той самий розрахунок дав інше значення RTMR0 для заявлених 4 ГіБ, 2 vCPU, QEMU 9.2.1 або другої мережевої карти, а також завершився невдачею у разі зміни ядра, прошивки чи командного рядка та для образу для розробки.
- `verify` пройшов усі 16 перевірок, включаючи коннектор швидкого тунелю, тому результат був «PASS». Він створив HTML- та PDF-сертифікат, цифровим чином завірений підписами та часовими мітками з кваліфікованою часовою міткою eIDAS від бельгійського урядового підрозділу часового мічення TSU 202301 (статус надано у довірчому списку Бельгії), часовою міткою FreeTSA та підписом верифікатора; `check-report` підтвердив усі ці елементи та підпис у PDF-файлі.
- Після перезапуску `verify --evidence` підтвердив два запуски, кожен із яких супроводжувався атестацією апаратного забезпечення, згенерованою всередині CVM, і кожен із яких був завантажений з опублікованого `dstack-0.5.12`; перезапуск і новий запуск мали статус REVIEW.
- `destroy` залишив робочу область порожньою.

**Deployment 5 · collector-signed discovery and forged-post rejection**

The collector ran from commit `53a0f7e9`, which includes the fixes above.

- Колектор опублікував свою адресу, підписану власним ключем, поруч із повідомленням оператора з HMAC. Потім до теми було додано два підроблені повідомлення: одне з обнуленим HMAC, а інше — підписане іншим ключем Ed25519; обидва вказували на час у 2096 році. `verify` взяв адресу, підписану ключем колектора, і пройшов усі 16 перевірок; печатка знову містила кваліфіковану бельгійську мітку часу, мітку часу FreeTSA та підпис верифікатора, а `check-report` підтвердив їх.
- Після перезапуску колектор опублікував нову підписану адресу: `verify` знайшов її одразу, оператор **«Знайти поточну адресу»** — через 27 секунд після публікації HMAC, і обидва проігнорували підроблені публікації. `verify --evidence` підтвердив два запуски, що завантажилися з `dstack-0.5.12`.
- Deploy відобразив суму, яку Phala виставляє за CVM, включаючи диск: 0,06078 долара за годину.

### Panel wizard and remaining scope

Майстер панелі двічі запускався у Phala Cloud: один раз через API завдань, а інший — через браузер на базі справжнього Chromium: перевірка ціни, створення з комітом під **Advanced**, усі шість перевірок атестації пройдені, список серверів із зазначенням ціни, що підлягає оплаті (44,37 доларів США на місяць), **Find поточну адресу**, завантаження виміряної конфігурації Docker Compose та видалення. У браузері не було виявлено помилок сторінок. Після кожного разу робоча область залишалася порожньою.

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation. All prices in this section were observed on 4 November 2026.

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

## Повнотекстовий пошук серед мільйона повідомлень · 5 листопада 2026 року

Команда: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

Детермінований підписаний журнал із 1 000 000 синтетичних повідомлень у 200 чатах (російські словоформи, українська, англійська, китайська, японська мови, посилання та ніки) було проіндексовано за 71 секунду; індекс зайняв 58 МіБ, крім журналу розміром 1,50 ГіБ. Пошук за найкращим збігом займав від 9 до 190 мс (медіана), проти 2,4–3,2 секунди для попереднього пошуку за підрядком . Повні результати, апаратне забезпечення та обмеження: [Повнотекстовий пошук](https://phishdestroy.github.io/TgWitness/uk/docs/reference/search/#benchmark). `tools/test_fulltext.py` також перевіряє підписаний архів, створений до повнотекстового пошуку (`tools/fixtures/evidence-before-fulltext.zip`) за допомогою поточного верифікатора, а також поточний архів за допомогою власного архіву `verify.py`.

## Решта кваліфікаційних вимог

Збережений журнал у режимі реального часу фіксує факти збору, редагування, повідомлення про видалення, вкладення, повторні перевірки та обробку обмежень швидкості. Він не фіксує вичерпну інформацію про доставку або контрольовану матрицю видимості ролей, суб’єктів, що реагують, тривалого FloodWait, блокування облікових записів та відновлення після перебоїв у роботі мережі/процесів. Видача QR-токенів залишається окремим процесом від завершеного підтвердження за допомогою мобільного QR-коду.

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

The [public audit directory](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) contains only the signed report and aggregate measurements. Detailed operational receipts, raw captures and account material remain private. Application screenshots in `docs/assets/` use fictional demonstration data.
