# Установка, проверка и обновление

Canonical page: https://phishdestroy.github.io/TgWitness/ru/docs/reference/installation/

Установите с помощью одной команды, проверьте подписи и хеши, обновите и удалите установку.

[Проект](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Быстрый старт](https://phishdestroy.github.io/TgWitness/ru/docs/reference/quickstart/) · [Развертывание](https://phishdestroy.github.io/TgWitness/ru/docs/reference/deployment/)

## Установка одной командой

Установщик с пошаговыми инструкциями включает в себя частную среду выполнения Python. Используйте тот же адрес для будущих установок: каждая публикация обновляет установщик, хеши, подписи и информацию о сборке.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

На сервере Ubuntu запустите программу от имени root, чтобы установить фоновый сервис. На настольном компьютере запустите программу от имени обычного пользователя.

**Windows (PowerShell или командная строка):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

В Windows администраторские права не требуются. Дочерний процесс PowerShell оставляет ваш терминал открытым с результатом. Python и зависимости остаются в папке установки.

В Ubuntu выберите **«Этот компьютер**», **«Временная ссылка HTTPS**» или **«Собственный домен**». Установщик выводит адрес панели и ключ доступа. Для получения временной ссылки откройте этот HTTPS-адрес в браузере и введите ключ. При локальном доступе к удалённому серверу используйте перенаправление SSH с вашего компьютера (`ssh -L 8787:127.0.0.1:8787 user@server`) и откройте `http://127.0.0.1:8787`. В macOS и Windows локальная панель открывается в вашем браузере; оставьте терминал запущенным.

Войдите в Telegram на панели и выберите, что собирать. Сама по себе установка не запускает сбор данных из Telegram.

## Где всё работает

`get.destroy.tools` — это **Cloudflare Worker, обслуживающий статические загрузки**. У него нет панели TgWitness, сеанса Telegram или базы данных с данными о пользователях. Он не маршрутизируется на VPS проекта. Приложение работает на том компьютере, на котором вы выполняете команду.

| Установка | Программа | Данные |
| --- | --- | --- |
| Ubuntu с правами root | `/opt/tgwitness` | Системная служба: `/var/lib/tgwitness-<installation ID>`; используйте `tgwitness paths` для указания точного пути. |
| Пользователь Linux / macOS | `~/.local/share/tgwitness` | `data/live` в рамках данной установки. |
| Пользователь Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` в рамках данной установки. |

Нажмите `TGWITNESS_INSTALL_DIR` , чтобы выбрать другую папку. Установленные версии и данные хранятся отдельно. Установщик не загружает ваши аккаунты, сообщения или ключи на сайт загрузки. При выборе туннеля Cloudflare трафик панели проходит через Cloudflare; использование собственного домена направляет трафик на ваш собственный сервер.

Каждая установка включает **файлы START-HERE.html** и **START-HERE.txt** с указанием локальных путей, команд и ссылок на репозиторий. Запустите `tgwitness guide` , чтобы открыть руководство. В Windows используйте `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` в PowerShell.

## Проверьте перед запуском

Однострочная команда доверяет HTTPS для запуска начального скрипта. Этот скрипт проверяет SHA-256, а также RSA-подпись проекта на приложении и ограничениях перед установкой. Вы также можете сначала скачать и проверить начальный скрипт.

Публичный ключ выпуска — [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). Его SHA-256:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Сохраните этот отпечаток из ревизии репозитория, которой вы доверяете. Контрольная сумма с того же сервера загрузки позволяет обнаружить несоответствие; независимый доверенный открытый ключ служит для аутентификации подписи выпуска.

Используйте новый пустой каталог для загрузки файлов, необходимых для проверки, указанных ниже.

**Linux / macOS — запускайте в новом пустом каталоге для загрузок** (требуются curl и OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

Цепочка `&&` цепочка останавливается до выполнения, если загрузка, проверка отпечатка ключа или проверка подписи завершились неудачно. Если между загрузкой скрипта и проверкой его подписи произошла публикация, загрузите и то, и другое заново. Старые установщики сохраняют неизменяемые URL-адреса пакетов.

**Windows — перед запуском проверьте изображение SHA-256:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Сравните хеш со `install.ps1` строкой. Для независимой проверки подписи используйте OpenSSL (например, из Git Bash) и тот же отпечаток открытого ключа, что указан выше:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Сама система Windows проверяет подписи пакетов с помощью .NET и не требует OpenSSL. Это отдельные подписи RSA-3072 / SHA-256, а не Authenticode. [Манифест](https://get.destroy.tools/manifest.json) содержит версию программного обеспечения, точный коммит Git, неизменяемый идентификатор выпуска и SHA-256 каждого артефакта. Страница содержит ссылку на соответствующий исходный код. Манифест и список контрольных сумм также имеют отдельные подписи (`manifest.json.sig` и `SHA256SUMS.txt.sig`).

## Обновление существующей установки

**Новая публикация обновляет сайт загрузки; установленные программы обновляются при повторном запуске установщика.** Автоматического обновления или автоматического перезапуска работающей коллекции не предусмотрено. Текущий канал установщика — **«preview»**; он использует опубликованные и проверенные сборки из `main`, коммит которой может быть более поздним, чем последний пронумерованный релиз на GitHub. Версия страницы определяется `pyproject.toml`; её коммит и идентификатор сборки позволяют различать обновления в пределах одной и той же предварительной версии.

Используйте ту же папку установки и того же пользователя ОС, что и ранее. Сделайте резервную копию всего каталога данных при остановленной сборе данных; `tgwitness paths` идентифицирует его. Подписанный экспорт не является полной резервной копией установки.

**Установка с правами root в Ubuntu по адресу `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

После успешной установки:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Для установки пользователем Linux/macOS используйте исходный файл `TGWITNESS_INSTALL_DIR` или значение по умолчанию и запустите первую команду установки ещё раз. Перед обновлением закройте панель, работающую в фоновом режиме, а после обновления запустите её снова. Для настроенной службы под Linux запустите соответствующую `tgwitness restart` команду.

**Windows:** закройте запущенную панель, запустите команду установки для Windows ещё раз, затем откройте `bin\tgwitness.cmd` в той же установке. Установщик сохраняет данные, сессии, настройки доступа и ключи подписи. Он переключает лаунчер только после того, как новая среда пройдет проверки; в случае неудачной установки предыдущий лаунчер остаётся на месте. Сохраните резервную копию, созданную до обновления, на случай изменения формата хранения.

## Повседневные команды в Ubuntu

| Команда | Результат |
| --- | --- |
| `tgwitness open` | Текущий URL панели и ключ доступа. |
| `tgwitness paths` | Точные пути к программам, данным и руководствам. |
| `tgwitness guide --print` | Инструкции по работе в автономном режиме. |
| `tgwitness status` / `tgwitness logs` | Журналы доступности / обслуживания. |
| `tgwitness stop` / `tgwitness start` | Остановить/возобновить работу сервиса; сохранить данные. |
| `tgwitness token rotate` | Замените ключ администратора и завершите сеансы браузера. |
| `tgwitness tunnel off` | Отключить общедоступный быстрый туннель; сохранить локальную панель. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Создать ссылку на быстрый туннель / заменить его адрес. |

См. раздел [«Доступ»](https://phishdestroy.github.io/TgWitness/ru/docs/reference/access/) для получения информации о токенах коллег, сессиях и IP-ограничениях, а также раздел [«Публикация установщика»](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) для ознакомления с рабочим процессом выпуска из GitHub в Cloudflare.

## Удалить TgWitness

Деинсталлятора нет: нужно остановить работу панели и удалить её папки. Удаление папки с данными приводит к безвозвратной потере журналов, ключей подписи, сеансов Telegram и сохраненных файлов. Перед этим:

1. Экспортируйте то, что вам нужно (**Экспорт → Скачать подписанный ZIP**), и храните отпечаток ключа подписи и контрольные точки за пределами этого компьютера. Чтобы сохранить само рабочее пространство, скопируйте всю папку с данными после остановки сбора данных.
2. Удалите серверы, созданные в **разделе «Дополнительно» → «Сервер 24/7»** из спи**ска «Ваши серверы»** или с помощью `python -m tgwitness.cloud destroy`; провайдер выставляет счета за них до тех пор, пока они не будут удалены.
3. Завершите сессию каждой учётной записи в Telegram в разделе **«Настройки» → «Устройства**». Удаление файлов не приводит к выходу из сессии на стороне Telegram.

**Установка с правами root в Ubuntu.** Обратите внимание на папку с данными, остановите службу, а затем удалите службу, папки и ярлык:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Установка для пользователей Linux или macOS.** Закройте панель. Настроенная служба пользователя Linux останавливается с помощью `systemctl --user disable --now tgwitness-<ID>`; его модуль находится в `~/.config/systemd/user/`. Затем удалите `~/.local/share/tgwitness` (или ваш `TGWITNESS_INSTALL_DIR`) и `~/.local/bin/tgwitness` ярлык.

**Windows.** Закройте панель и удалите `%LOCALAPPDATA%\TgWitness` (или ваш `TGWITNESS_INSTALL_DIR`). Установщик не добавляет ни служб, ни запланированных задач, ни ярлыков.
