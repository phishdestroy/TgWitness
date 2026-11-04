# Что проверено

Canonical page: https://phishdestroy.github.io/TgWitness/ru/docs/reference/verification/

Тестирование Telegram в режиме реального времени, автоматические проверки, проверки в браузере и то, что пока остаётся непроверенным.

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

## Остальные требования

Сохраняемый журнал в режиме реального времени фиксирует фактические события сбора данных, редактирования, уведомлений об удалении, вложений, повторных проверок и обработки ограничений скорости. Он не фиксирует исчерпывающие данные о доставке или контролируемую матрицу видимости ролей, субъектов реагирования, длительного ожидания FloodWait, блокировок учетных записей и восстановления после сбоев в работе сети или процессов. Выдача QR-токенов остается отдельным процессом от завершённого подтверждения с помощью мобильного QR-кода.

Сборка и запуск в Docker, установка на Linux/macOS, устойчивость к высокой нагрузке, независимая экспертиза безопасности, реальный независимый отклик TSA, проверка отзыва и архивирования сертификатов, а также криминалистическая сертификация остаются за пределами зафиксированной квалификации. Реализованы сохранение состояния MTProto и функция «catch-up»; атомарное устойчивое воспроизведение пока не реализовано. Сбор административных журналов, дополнительные списки реакторов и приоритетный короткий опрос остаются отдельными функциями. См. [текущую версию](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) матрицы контролируемой квалификации.

Местные подробные отчёты и скриншоты находятся в папке test-results/ (игнорируются Git). Общедоступные скриншоты в папке docs/assets/ содержат исключительно вымышленные демонстрационные данные.
