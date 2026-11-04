# Сообщения меняются. Сохраните то, что вы видели.

Canonical page: https://phishdestroy.github.io/TgWitness/ru/

[Открытый исходный код / v0.8.1](https://phishdestroy.github.io/TgWitness/ru/docs/reference/changelog/)

Сохраняйте чаты Telegram со всеми правками и удалениями и передавайте запись, которую может проверить кто угодно.

[Открыть демо-версию](https://phishdestroy.github.io/TgWitness/demo/?lang=ru)[Руководство по настройке](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ru)

Вымышленные данные, без входа в Telegram.

 [Выгрузка через GitHub Actions (предварительная версия)](https://phishdestroy.github.io/TgWitness/ru/docs/capture/) [Внесайтовая копия на S3: настройка и восстановление](https://phishdestroy.github.io/TgWitness/ru/#s3)

СООБЩЕНИЕ, ПРЕОДОЛЕВАЮЩЕЕ ВРЕМЯ #0042

Northstar · ИсследованияВымышленный источник / сообщение 42

1. **Зафиксировано сообщение**09:41:02

   Брифинг начинается с 14:00.
2. **Редактирование сохранено**09:43:18

   Брифинг начинается с 15:00.

   Предыдущая версия сохранена
3. **Уведомление об удалении**10:06:45

   Зафиксированный контент остается в вашем журнале.

Три наблюдения. Одна история. ПРИМЕР

Сообщение исчезает. Зафиксированная история сохраняется.

## Каждое зафиксированное изменение. Именно там, где вам это нужно.

Настоящий интерфейс, но с выдуманными данными.

TgWitness / Сохраненные чатыВАШЕ РАБОЧЕЕ ПРОСТРАНСТВО ДЛЯ НАБЛЮДЕНИЙ

![Сохраненные переписки в Telegram в темной теме, с фиксированными изменениями и удалёнными сообщениями, представленными в контексте](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Сохранённые чаты Выглядит как обычный чат, а правки и удаления видны прямо рядом с сообщениями.

TgWitness / ЖурналЛОКАЛЬНОЕ РАБОЧЕЕ ПРОСТРАНСТВО

![Журнал с зафиксированными сообщениями, правками, уведомлениями об удалении и событиями, подпадающими под охват](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Журнал Всё, что видел аккаунт, с поиском и с отмеченными пробелами.

TgWitness / История измененийЛОКАЛЬНОЕ РАБОЧЕЕ ПРОСТРАНСТВО

![Вкладка с подробностями, в которой сравниваются зафиксированные предыдущая и отредактированная версии сообщения](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / История правок Старая и новая версии рядом, ничего не перезаписывается.

TgWitness / Подписанные экспортные файлыЛОКАЛЬНОЕ РАБОЧЕЕ ПРОСТРАНСТВО

![Функция экспорта рабочей области, позволяющая получить подписанные файлы в форматах ZIP, JSONL, CSV, а также автономный отчёт в формате HTML](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Подписанный экспорт Журнал можно забрать с собой — подписанный и со своим верификатором.

Отслеживайте сохраненную запись через [Case Board](https://phishdestroy.github.io/TgWitness/ru/docs/case-board/), [процесс составления отчета](https://phishdestroy.github.io/TgWitness/ru/docs/reports/) и [копию](https://phishdestroy.github.io/TgWitness/ru/docs/handover/) [для передачи](https://phishdestroy.github.io/TgWitness/ru/docs/handover/). [Просматривайте группы учетных записей](https://phishdestroy.github.io/TgWitness/ru/docs/groups/) вместе.

01 / ЗАПИСЬ

### Вы сами определяете сферу применения.

Несколько чатов, папка или весь аккаунт. У каждого аккаунта своё пространство.

[Сравните режимы сбора данных](https://phishdestroy.github.io/TgWitness/ru/guides/modes.html#scope)

02 / СОХРАНЕНИЕ

### Изменения дополняют общую картину.

Версии, удаления и пробелы — всё остаётся в журнале.

[См. матрицу событий](https://phishdestroy.github.io/TgWitness/ru/guides/modes.html#events)

03 / ПЕРЕДАЧА

### Запись, которая путешествует.

Подписанный ZIP, файлы и офлайн-отчёт. Пароль — по желанию.

[Экспорт и проверка](https://phishdestroy.github.io/TgWitness/ru/docs/exports/)

## Измените один байт —
система проверки сразу об этом сообщит.

Каждое событие содержит ссылку на предыдущий хеш и подпись Ed25519.

![Зафиксированные события сопряжены с предыдущими хешами, снабжены подписями и передаются в виде поддающегося проверке экспорта.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Изменение сохраненной записи приводит к изменению её хеша и делает невозможной проверку связанной с ней записи.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Отдельно сохраняемый контрольный пункт позволяет получателю сравнить экспортированный журнал с более ранними данными.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Следуйте схеме проверки от хеша файла до отдельно сохраненной контрольной точки.

[Ознакомьтесь с восемью уровнями доказательности](https://phishdestroy.github.io/TgWitness/ru/guides/modes.html#levels)

## Готов к дополнительной проверке.

Сообщения, файлы и офлайн-отчёт в одном подписанном архиве.

[Ознакомьтесь с моделью доказательств](https://phishdestroy.github.io/TgWitness/ru/docs/reference/evidence/)

tgwitness-evidence.zipПАКЕТ С ПОДПИСЯМИ

- 01

  Первоначальные наблюденияЗаписи в формате JSONL + таблица в формате CSV
- 02

  Удобный для чтения контекстОфлайн-отчёт в формате HTML + сохраненные мультимедийные файлы
- 03

  Независимая проверкаПодписанный манифест + автономный верификатор

Получатель проверяет всё по вашему ключу, а контрольная точка, сохранённая в другом месте, показывает, что с тех пор ничего не переписали. [Как работают проверки.](https://phishdestroy.github.io/TgWitness/ru/docs/concepts/#layers)

## Копии в S3. Внешние проверки.

Сохраняйте зашифрованные копии и добавляйте независимые проверки.

По умолчанию отключено

### Копирование в S3-совместимое хранилище

Журнал, файлы, контрольные точки и экспорты чатов шифруются ещё до отправки в S3.

**Настройки хранения и восстановление**

Шифрование перед загрузкой

`AES-256-GCM` на вашей машине. Провайдер видит только шифротекст.

Копирование по расписанию или вручную

Копировать сейчас или каждые 1–1440 минут, прогресс виден в панели.

Object Lock

Выберите срок и режим хранения — панель проверит, что они действительно применились.

Восстановление с проверкой

Храните ключ отдельно. Восстановить можно где угодно, файлы появятся только после проверки.

![Полная панель настроек для внешнего хранения: конечная точка, регион, хранилище, ключи доступа, расписание, управление функцией Object Lock и ключом восстановления](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Вся форма с раскрытыми дополнительными настройками. Учётные данные хранилища не указаны.

Журнал и СМИ`AES-256-GCM`Хранилище, совместимое с S3

[Настройте S3 и восстановите копию](https://phishdestroy.github.io/TgWitness/ru/docs/exports/#s3)[Ознакомьтесь с подробностями проверки:](https://phishdestroy.github.io/TgWitness/ru/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Ключ восстановления** Храните его отдельно: без него копию не прочитать.

### Уведомления · Apprise

Проблемы, изменения в чатах и ежедневная сводка — в мессенджеры, на почту или в ваш вебхук.

**Что отправлять** Текста сообщений нет, пока вы сами его не включите.

 [Настроить получателей уведомлений](https://phishdestroy.github.io/TgWitness/ru/docs/reference/operations/#notifications)

### Внешние временные метки

Метки времени RFC 3161 и OpenTimestamps для хешей контрольных точек.

**Следите за результатом** Проверьте ответ TSA или обновите квитанцию OpenTimestamps до доказательства в Bitcoin.

 [Проверьте доказательства с временными метками:](https://phishdestroy.github.io/TgWitness/ru/docs/reference/timestamp/)

### Независимый свидетель

Отдельный сервер хранит подписанные наблюдения и может публиковать контрольные точки `TGW1`.

**Отдельная опора** Запускайте его на другом хосте, со своим ключом и журналом.

 [Настройте Witness](https://phishdestroy.github.io/TgWitness/ru/docs/witness/)

### Восстановление данных и заметные пробелы

Продолжение после перезапуска. Перепроверки и `coverage.json` показывают восстановленные сообщения и разрывы.

**Проверьте промежуток** Восстановленные сообщения и записанные пробелы рядом.

 [Проверьте непрерывность и наличие пробелов](https://phishdestroy.github.io/TgWitness/ru/guides/modes.html#continuity)

## Ваша первая рабочая среда начинается здесь.

Сначала попробуйте демо, а когда будете готовы — подключите запасной аккаунт.
Windows, Linux, macOS или Docker.

[Ознакомьтесь с руководством по настройке](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ru)

**Один импортированный сеанс — один запущенный клиент.**

Не запускайте импортированные TData или сессию одновременно в Telegram Desktop и TgWitness: Telegram может отключить обе (AUTH_KEY_DUPLICATED). Нужны оба клиента? Войдите в TgWitness отдельно — по телефону или QR.

[Ознакомьтесь с предупреждением об импорте сеанса](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ru#session-warning)

**Ознакомьтесь с информацией, прежде чем подключаться.**

Откройте рабочее пространство с вымышленными данными без аккаунта Telegram.

[Открыть онлайн-демо →](https://phishdestroy.github.io/TgWitness/demo/?lang=ru)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**Команды для локальной установки**

ШАГ 01

### Получить исходный код.

[Скачайте ZIP-архив с исходным кодом](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) и распакуйте его или клонируйте репозиторий:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Нужен Python 3.11+. В Windows лаунчер сам предложит его установить.

[Просмотреть версии](https://github.com/phishdestroy/TgWitness/releases)

ШАГ 02

### Выберите способ запуска.

Дважды щелкните по файлу `Start.cmd` или запустите его в PowerShell:

```
.\Start.cmd
```

Просто знакомитесь с проектом? Дважды щелкните по ссылке `scripts\Demo.cmd`, чтобы перейти к автономной демо-версии. Вход в Telegram не требуется.

При наличии Python 3.11+ и библиотеки `venv`:

```
sh start.sh
```

Чтобы вместо этого открыть вымышленный журнал, выполните команду `sh start.sh --demo`.

При запущенном Docker и установленном Compose версии 2.20 или выше:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Вторая команда отображает токен вашей личной панели. Сохраните его на своём компьютере.

После запуска откройте [127.0.0.1:8787](http://127.0.0.1:8787).

При установке из исходников токен лежит в `data/live/panel-token.txt`. Своя пара API с [my.telegram.org](https://my.telegram.org) не обязательна. [Полная инструкция ↗](https://phishdestroy.github.io/TgWitness/ru/docs/reference/quickstart/)

**TgWitness 0.8.1** [Что нового →](https://phishdestroy.github.io/TgWitness/ru/docs/reference/changelog/) · [Возможности и известные ограничения →](https://phishdestroy.github.io/TgWitness/ru/docs/reference/features/)

## Четкие инструкции. Полезный следующий шаг.

[Ознакомьтесь с руководствами ↗](https://phishdestroy.github.io/TgWitness/ru/docs/)

[### Режимы, сценарии и уровни доказательности Четыре режима сбора данных. Восемь уровней проверки. Выберите рабочий процесс, подходящий для вашего дела.](https://phishdestroy.github.io/TgWitness/ru/guides/modes.html)

[01 ### Подключить аккаунт Импорт данных с мобильных телефонов, QR-кодов и поддерживаемых сеансов.](https://phishdestroy.github.io/TgWitness/ru/docs/accounts/)[02 ### Выберите прокси-сервер Публичные списки MTProxy или ваш собственный маршрут.](https://phishdestroy.github.io/TgWitness/ru/docs/proxies/)[03 ### Настройте бота-свидетеля Подписанные контрольные точки в вашем канале Telegram.](https://phishdestroy.github.io/TgWitness/ru/docs/witness/)[04 ### Экспорт и проверка Поделитесь сохраненной историей и проверьте её целостность.](https://phishdestroy.github.io/TgWitness/ru/docs/exports/)

## Работайте с архивом.

История, ИИ со ссылками на источники, MCP, OCR и подписанные вебхуки.

[Ознакомьтесь с рабочим процессом](https://phishdestroy.github.io/TgWitness/ru/docs/archive/)

## Прежде чем начать.

**Связана ли эта страница с Telegram?**

Нет. Это статическая страница с вымышленными примерами. Приложение работает на вашей машине, и входите вы там.

**Может ли он восстанавливать сообщения, удалённые до момента их фиксации?**

Нет. Он хранит то, что аккаунт видел, пока программа работала. Более поздний снимок не восстановит пропущенные правки или удалённые сообщения.

**Зашифрован ли весь мой журнал?**

Сессии и ключи — да. Сообщения и файлы — нет, используйте шифрование диска. На экспорт можно поставить пароль AES-256.

**Имеет ли этот проект какое-либо отношение к Telegram?**

Нет. Это независимый проект на Telethon под лицензией MIT. Вы входите со своими аккаунтами.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Сначала ознакомьтесь с информацией. Настройте систему, когда будете готовы.

[Открыть демо-версию](https://phishdestroy.github.io/TgWitness/demo/?lang=ru)[Руководство по настройке](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ru)
