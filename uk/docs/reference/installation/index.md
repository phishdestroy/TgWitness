# Встановлення, перевірка та оновлення

Canonical page: https://phishdestroy.github.io/TgWitness/uk/docs/reference/installation/

Встановіть за допомогою однієї команди, перевіряйте підписи та хеші, оновлюйте та видаляйте інсталяцію.

[Проєкт](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Швидкий старт](https://phishdestroy.github.io/TgWitness/uk/docs/reference/quickstart/) · [Розгортання](https://phishdestroy.github.io/TgWitness/uk/docs/reference/deployment/)

## Встановіть за допомогою однієї команди

Інсталятор із покроковими інструкціями містить приватне середовище виконання Python. Використовуйте ту саму адресу для майбутніх інсталяцій: кожна публікація оновлює інсталятор, хеші, підписи та інформацію про збірку одночасно.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

На сервері Ubuntu запустіть програму з правами root, щоб встановити фоновий сервіс. На настільному комп’ютері запустіть програму як звичайний користувач.

**Windows (PowerShell або командний рядок):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

У Windows адміністратор не потрібен. Дочірній процес PowerShell залишає ваш термінал відкритим із результатом. Python та залежності залишаються в інсталяційному пакеті.

У Ubuntu виберіть **«Цей комп’ютер**», **«Тимчасове HTTPS-посилання**» або **«Власний домен**». Інсталятор виведе адресу панелі та ключ доступу. Для отримання тимчасового посилання відкрийте цю HTTPS-адресу у браузері та введіть ключ. У разі локального доступу до віддаленого сервера скористайтеся переадресацією SSH зі свого комп’ютера (`ssh -L 8787:127.0.0.1:8787 user@server`) та відкрийте `http://127.0.0.1:8787`. У macOS та Windows локальна панель відкривається у вашому браузері; залиште термінал увімкненим.

Увійдіть у Telegram на панелі та виберіть, що збирати. Сама лише інсталяція не запускає збір даних із Telegram.

## Де все працює

`get.destroy.tools` **Cloudflare Worker для обслуговування статичних завантажень**. У нього немає панелі TgWitness, сеансу Telegram або бази даних доказів користувачів. Він не підключений до VPS проекту. Додаток працює на тій машині, де ви виконуєте команду.

| Встановлення | Програма | Дані |
| --- | --- | --- |
| Ubuntu з правами суперкористувача | `/opt/tgwitness` | Системна служба: `/var/lib/tgwitness-<installation ID>`; використовуйте `tgwitness paths` для точного шляху. |
| Користувач Linux / macOS | `~/.local/share/tgwitness` | `data/live` у рамках цієї інсталяції. |
| Користувач Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` у рамках цієї інсталяції. |

Налаштуйте `TGWITNESS_INSTALL_DIR` , щоб вибрати іншу папку. Встановлені версії та дані зберігаються окремо. Інсталятор не завантажує ваші акаунти, повідомлення чи ключі на сайт завантаження. Вибір тунелю Cloudflare направляє трафік панелі через Cloudflare; використання власного домену спрямовує трафік на ваш власний сервер.

Кожна інсталяція містить **файли START-HERE.html** та **START-HERE.txt** із локальними шляхами, командами та посиланнями на репозиторій. Запустіть `tgwitness guide` , щоб відкрити посібник. У Windows використовуйте `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` у PowerShell.

## Налаштування повнотекстового пошуку

[Повнотекстовий пошук](https://phishdestroy.github.io/TgWitness/uk/docs/reference/search/) (попередній перегляд) не потребує налаштування. Його індекс формується у фоновому режимі після оновлення.

| Змінна або команда | Ефект |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | За замовчуванням: індекс зберігається в `search/fulltext.sqlite3` кожного робочого простору |
| `TGWITNESS_FULLTEXT=memory` | Індексний файл відсутній; індекс перебудовується при кожному запуску |
| `TGWITNESS_FULLTEXT=off` | Без індексу; лише пошук за точним текстом |
| `tgwitness index status` | Стан індексу кожного робочого простору |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | Перебудуйте кожен індекс із підписаного журналу |

Вибір адміністратора в меню **«Журнал» → «Фільтри» → «Індекс пошуку»** має пріоритет над змінною для цього робочого простору. Команди знаходять каталог даних тієї інсталяції, в якій вони виконуються; в інших випадках додайте `--data-dir` шлях із `tgwitness paths`. Для повного українського словника (дані під ліцензією GPL-3.0) встановіть `pymorphy3-dicts-uk` у середовищі Python цієї інсталяції.

## Доступ через командний рядок

[Командний рядок](https://phishdestroy.github.io/TgWitness/uk/docs/reference/cli/) (попередній перегляд) зчитує архів для скриптів та агентів.

| Змінна | Ефект |
| --- | --- |
| `TGWITNESS_URL` | Адреса панелі для `tgwitness search`, `context`, `messages`, `stats` та `export`; за замовчуванням `http://127.0.0.1:8787` , коли встановлено токен |
| `TGWITNESS_MCP_TOKEN` | Архівуйте токен підключення з **розділу «Інтеграції» → «MCP»**, який використовується спільно з клієнтами MCP; `--token-file` замість цього зчитує його з файлу |
| `TGWITNESS_DATA` | Каталог даних читається безпосередньо, якщо не вказано `--data-dir`, URL-адреси або токена |

## Перевірте перед запуском

Однорядкова команда довіряє HTTPS для запуску початкового скрипта. Цей скрипт перевіряє SHA-256 та RSA-підпис проєкту щодо додатка та обмежень перед встановленням. Ви також можете спочатку завантажити та перевірити початковий скрипт.

Публічний ключ випуску — [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). Його SHA-256:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Збережіть цей відбиток із версії репозиторію, якій ви довіряєте. Контрольна сума з того самого сервера завантаження виявляє невідповідність; незалежний, перевірений відкритий ключ — це те, що підтверджує автентичність підпису релізу.

Використовуйте новий порожній каталог для завантажень, необхідних для верифікації, наведені нижче.

**Linux / macOS — запускайте в новому, порожньому каталозі для завантажень** (потрібні curl та OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

Ланцюг `&&` ланцюг зупиняється перед виконанням, якщо завантаження, перевірка відбитка ключа або підпису закінчується невдачею. Якщо публікація відбувається між завантаженням скрипта та його підписом, завантажте обидва знову. Старі інсталятори зберігають незмінні URL-адреси пакетів.

**Windows — перед запуском перевірте SHA-256:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Порівняйте хеш із `install.ps1` рядком. Для незалежної перевірки підпису використовуйте OpenSSL (наприклад, із Git Bash) та той самий відбиток відкритого ключа, що наведено вище:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Сама система Windows перевіряє підписи пакетів за допомогою .NET і не потребує OpenSSL. Це відокремлені підписи RSA-3072 / SHA-256, а не Authenticode. [Маніфест](https://get.destroy.tools/manifest.json) містить версію програмного забезпечення, точний коміт Git, незмінний ідентифікатор випуску та SHA-256 кожного артефакту. Сторінка містить посилання на відповідне джерело. Маніфест і список контрольних сум також мають відокремлені підписи (`manifest.json.sig` та `SHA256SUMS.txt.sig`).

## Оновлення існуючої інсталяції

**Нова публікація оновлює сайт завантаження; встановлені програми оновлюються, коли ви запускаєте інсталятор знову.** Не існує автоматичного оновлення або автоматичного перезапуску колекції, що працює. Поточний канал інсталятора — це **попередній перегляд**; він слідує за опублікованими, перевіреними збірками з `main`, коміт яких може бути новішим за останній пронумерований реліз на GitHub. Версія сторінки походить з `pyproject.toml`; її коміт та ідентифікатор збірки дозволяють розрізняти оновлення в межах однієї попередньої версії.

Publication is automatic after that exact commit passes the application and security checks and the signed package passes Ubuntu service and Windows PowerShell installation tests. While checks are running, or if they fail, the same commands continue to install the previous checked build. The build manifest shows which commit is currently available; the version number alone may stay the same between preview updates.

Використовуйте ту саму папку інсталяції та того самого користувача ОС, що й раніше. Створіть резервну копію всього каталогу даних після зупинки збору даних; `tgwitness paths` що дозволяє його ідентифікувати. Підписаний експорт не є повною резервною копією інсталяції.

**Встановлення з правами суперкористувача в Ubuntu за адресою `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

Після успішної інсталяції:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Для встановлення на Linux/macOS використовуйте оригінальний `TGWITNESS_INSTALL_DIR` або за замовчуванням і знову виконайте першу команду встановлення. Перед оновленням закрийте панель, що працює у фоновому режимі, а після цього запустіть її знову. Для налаштованої служби користувача Linux виконайте відповідну `tgwitness restart` команду.

**Windows:** закрийте запущену панель, знову запустіть команду встановлення для Windows, а потім відкрийте `bin\tgwitness.cmd` у тій самій інсталяції. Інсталятор зберігає дані, сесії, налаштування доступу та ключі підпису. Він замінює запускач лише після того, як нове середовище пройде перевірки; у разі невдалої інсталяції попередній запускач залишається на місці. Зберігайте резервну копію, створену перед оновленням, на випадок змін формату зберігання.

## Повсякденні команди в Ubuntu

| Команда | Результат |
| --- | --- |
| `tgwitness open` | Поточна URL-адреса панелі та ключ доступу. |
| `tgwitness paths` | Точні шляхи до програм, даних та інструкцій. |
| `tgwitness guide --print` | Інструкція з роботи в автономному режимі. |
| `tgwitness status` / `tgwitness logs` | Журнали доступності / обслуговування. |
| `tgwitness stop` / `tgwitness start` | Зупинка / відновлення роботи сервісу; збереження даних. |
| `tgwitness token rotate` | Замініть ключ адміністратора та завершіть сесії браузера. |
| `tgwitness tunnel off` | Вимкніть публічний швидкий тунель; залиште локальну панель. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Створити посилання на швидкий тунель / замінити його адресу. |

Дивіться розділ [«Доступ»](https://phishdestroy.github.io/TgWitness/uk/docs/reference/access/) щодо токенів колег, сеансів та обмежень за IP-адресами, а також розділ [«Публікація інсталятора»](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) щодо робочого процесу випуску з GitHub до Cloudflare.

## Видалити TgWitness

Деінсталятора немає: потрібно зупинити роботу панелі та видалити її папки. Видалення папки з даними остаточно знищує журнали, ключі підпису, сесії Telegram та збережені файли. Перед цим:

1. Експортуйте те, що вам потрібно (**Експорт → Завантажити підписаний ZIP**), а відбиток ключа підпису та контрольні точки зберігайте поза цією машиною. Щоб зберегти саму робочу область, скопіюйте всю папку з даними, зупинивши збір даних.
2. Видаліть сервери, створені в меню **«Додаткові функції» → «Сервер 24/7»** у розділі **«Ваші сервери»** або за допомогою `python -m tgwitness.cloud destroy`; провайдер виставляє рахунки за них, доки вони не будуть видалені.
3. Завершіть сесію кожного облікового запису в Telegram у **меню «Налаштування» → «Пристрої**». Видалення файлів не призводить до виходу з сесії на стороні Telegram.

**Встановлення з правами суперкористувача в Ubuntu.** Зверніть увагу на папку з даними, зупиніть службу, а потім видаліть службу, папки та ярлик:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Встановлення для користувачів Linux або macOS.** Закрийте панель. Налаштована служба користувача Linux зупиняється за допомогою `systemctl --user disable --now tgwitness-<ID>`; його модуль знаходиться в `~/.config/systemd/user/`. Потім видаліть `~/.local/share/tgwitness` (або ваш `TGWITNESS_INSTALL_DIR`) та `~/.local/bin/tgwitness` ярлик.

**Windows.** Закрийте панель і видаліть `%LOCALAPPDATA%\TgWitness` (або свій `TGWITNESS_INSTALL_DIR`). Інсталятор не додає жодних служб, запланованих завдань чи ярликів.
