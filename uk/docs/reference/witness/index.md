# Незалежний свідок

Canonical page: https://phishdestroy.github.io/TgWitness/uk/docs/reference/witness/

Запустіть «witness» із власним ключем та ботом, опублікуйте підписані контрольні точки в каналі та звіряйте експортовані дані з ними.

[Експорт та перевірка](https://phishdestroy.github.io/TgWitness/uk/docs/reference/evidence/) · [Високий рівень надійності](https://phishdestroy.github.io/TgWitness/uk/docs/reference/high-assurance/) · [Посібник з панелей](https://phishdestroy.github.io/TgWitness/uk/docs/reference/panel/#extras)

A witness retains signed checkpoints separately from the collector．It checks the collector's signature and journal continuity，signs the result with its own key，and publishes it to a Telegram channel．Run it on a separate server with read-only access to the collector's witness endpoint．

Блок-схема · Collector → Witness (підписаний контрольний пункт: кількість записів + хеш заголовка); Witness → Журнал Witness, власний ключ; Witness → Канал у Telegram (підписаний допис через власного бота); ЗIP-архів доказів → verify.py; Журнал Witness, власний ключ → verify.py; Канал у Telegram → verify.py (Експорт з Telegram Desktop або сторінка «t.me/s») · Collector · Witness · Журнал Witness, власнийключ · Канал у Telegram · ЗIP-архів доказів · verify.py · підписаний контрольний · пункт: кількість записів + · хеш заголовка · підписаний допис через · власного бота · Експорт з Telegram Desktop · або сторінка «t.me/s»

**Діаграма у вигляді тексту**

1. Collector → Witness (підписаний контрольний пункт: кількість записів + хеш заголовка)
2. Witness → Журнал Witness, власний ключ
3. Witness → Канал у Telegram (підписаний допис через власного бота)
4. ЗIP-архів доказів → verify.py
5. Журнал Witness, власний ключ → verify.py
6. Канал у Telegram → verify.py (Експорт з Telegram Desktop або сторінка «t.me/s»)

## Що отримує TgWitness і чого він не робить

| Свідок має | Свідок ніколи не має |
| --- | --- |
| **Токен-свідок,** доступний лише для читання, для одного робочого простору | Сесія Telegram користувача-збирача або облікові дані API |
| Власний ключ Ed25519 та журнал | Сховище колектора, ключ підпису або токен панелі |
| Власний токен бота Telegram | Зміст повідомлення: у заголовку вказано кількість записів та хеш |

Токен створюється в **меню «Extras» → «Independent witness»**, відображається один раз і зберігається лише у вигляді SHA-256. Він відкриває саме одну кінцеву точку, `GET /api/witness/head`, який повертає щойно підписану контрольну точку, а також підписані лічильники колекцій без вмісту та стан працездатності. Він не може відкривати панель, читати вміст повідомлень або змінювати налаштування, а токен панелі там не приймається. Скасувати токен можна на тій самій сторінці. Колектор фіксує момент, коли новий ключ свідка починає перевірку (`witness.seen`) та показує останню перевірку для кожного токена; свідок, який не перевірявся протягом 2,5 інтервалів, позначається як прострочений.

Нові свідки надсилають випадковий виклик під час кожного опитування; запис про фіксацію повторює його під підписом збирача. Лічильники прив’язані до конкретної контрольної точки та включаються до підписаних повідомлень свідків. Старі заголовки залишаються прийнятними для автономного свідка. Сам по собі приріст журналу ніколи не вважається новим повідомленням.

## Що перевіряється та фіксується

Кожного інтервалу (за замовчуванням — кожні 10 хвилин) TgWitness:

1. завантажує сам заголовок (колектор не може його додавати або пропускати);
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen)，a nondecreasing count and an unchanged head at an unchanged count． Merkle inclusion and consistency proofs verify that a growing journal extends the retained checkpoint．Once continuity proofs have been used，removing them is rejected；
3. додає підписаний запис до власного журналу: `witness.anchor` зі статусом `ok`, `key_changed`, `rollback` (менше записів, ніж раніше), `fork` (така сама довжина, інший заголовок) або `invalid` (відповідь не пройшла перевірку), або `witness.no_response`, коли колектор не відповів;
4. публікує результат у каналі, підписаний, включаючи «немає відповіді», поки TgWitness працює та має доступ до Bot API. Ідентифікатор публікації записується (`witness.posted`), так само як і невдала публікація (`witness.post_failed`).

Публікація виглядає так; в останньому рядку міститься підписана заява:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Запустити Witness

Вам знадобиться бот Telegram (створіть його за допомогою @BotFather), канал, де цей бот є адміністратором, а також адреса колектора, доступна для свідка — через HTTPS поза приватною мережею (див. профіль HTTPS у [розділі «Розгортання»](https://phishdestroy.github.io/TgWitness/uk/docs/reference/deployment/)).

Відкрийте **«Додатки» → «Незалежний свідок» → «Налаштувати»** на панелі. Три кроки охоплюють доступ тільки для читання, ваш канал та інтервал, а потім запуск свідка. Політика публікації, опціональний проксі HTTP/SOCKS5 та власна адреса Bot API знаходяться в розділі **«Додаткові налаштування**». Форма завантажується `witness.json` із закріпленим ключем колектора цього робочого простору. Завантажте щойно створений токен «тільки для читання», вибравши **«Зберегти файл доступу** як» `witness-token.txt`»; розмістіть його та `bot-token.txt`створений на хості свідка поруч із цим JSON-файлом. Колектор ніколи не отримує токен бота. Завантаження не запускає службу та не публікує повідомлення. Жоден свідок розміщеного проєкту не реєструється неявно.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

Перша команда перевіряє файли конфігурації та секретні файли без мережевих запитів або створення ключів. Шляхи у JSON є відносними до цього файлу; шляхи CLI/середовища є відносними до робочого каталогу. Зберігайте відбиток свідка поза межами його хоста. Індикатор останнього опитування колектора лише підтверджує запит; про публікацію повідомляється через Proof або перевіряється у журналі свідка та на каналі.

Якщо панель знаходиться за SSH-тунелем, відкрийте доступ лише до обмеженої кінцевої точки Witness на окремому HTTPS-хості за [цим прикладом використання Caddy](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example). Робоча область за замовчуванням використовує `https://witness.example.org`, інші робочі області — `https://witness.example.org/profiles/ID`. Токени все ще потрібні; панель та її інші маршрути API не переадресовуються цим віртуальним хостом.

Виберіть `all` для регулярно опублікованих контрольних точок. П’ятихвилинний інтервал означає приблизно 288 публікацій на робочу область на день. `changes`/`problems` навмисно залишають деякі перевірки неопублікованими. MTProxy призначений для клієнта Telegram, що виконує збір даних. HTTP-опитування Witness та HTTPS-інтерфейс Telegram Bot API використовують власні маршрути: прямий/HTTP/SOCKS5 ([Bot API](https://core.telegram.org/bots/api)).

**Поряд із колектором, з використанням Docker** (той самий хост — незалежний процес і ключ, але той самий оператор): введіть значення в поле «`.env`» і запустіть профіль.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

При використанні опублікованого зображення вказуйте код `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**На чужому сервері** (справжній незалежний свідок): скопіюйте туди репозиторій, вкажіть `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` та три значення, наведені вище, у `.env`, а потім

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

або без Docker:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Опублікувати в Discord

Свідок може публікувати повідомлення в каналі Discord замість Telegram. У Discord відкрийте **«Редагувати канал» → «Інтеграції» → «Вебхуки»**, створіть вебхук і скопіюйте його URL-адресу. У панелі на кроці 2 виберіть **«Вебхук Discord» · ваш канал**. На хості свідка збережіть URL-адресу як `discord-webhook.txt` поруч із `witness.json`; вона ніколи не надходить до збирача.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

Кожен «witness» має одного видавця: канал Telegram або веб-хук Discord, але не обидва одночасно. Пости містять однакове підписане твердження і не можуть відправляти сповіщення нікому. Пост, довжина якого перевищує обмеження Discord у 2 000 символів, замінюється коротким рядком із повним чеком, доданим у вигляді `witness-check.txt`. Кожен ідентифікатор публікації записується як `witness.posted`. `verify.py --channel`зчитує лише експорти з каналів Telegram, тому для Discord ведіть журнал свідка: він містить усі чеки.

### Параметри

| Варіант | Середовище | За замовчуванням | Значення |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Інтервал між перевірками: 1–1440 |
| `--timeout` | `_TIMEOUT` | 30 | Час очікування на роботу колектора та Bot API: 5–600 секунд |
| `--post` | `_POST` | `all` | `all`: все гаразд; `changes`: нова проблема; `problems`: лише проблеми та відсутні відповіді |
| `--title` | `_TITLE` | `TgWitness witness` | Перші слова кожного допису в каналі |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | Збережіть ключ колектора, замість того щоб покладатися на першу відповідь |
| `--proxy` | `_PROXY` | прямий | `socks5://host:port` або `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Адреса API-інтерфейсу бота, наприклад, локальний сервер API-інтерфейсу бота |
| `--data-dir` | `_DATA` | `witness-data` | Ключ Witness та журнал |
| `--config` | `_CONFIG` | – | Файл JSON із будь-яким із наведених вище варіантів |

Адреса колектора, токени та канал беруться з `--collector`, `--token` або `--token-file`, `--bot-token` або `--bot-token-file`, `--discord-webhook-file` та `--channel`, або `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` та `_CHANNEL`, що не дозволяє секретам потрапляти до списку процесів.

У файлі конфігурації використовуються назви опцій з підкресленнями, а також `texts`, який замінює слова у публікаціях каналу:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Ключі `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Командний рядок має пріоритет над середовищем, а середовище — над файлом. Невідомі опції або текстові ключі зупиняють роботу witness із повідомленням, а не ігноруються. Формулювання ніколи не впливає на перевірку: verify.py перевіряє підписаний токен наприкінці кожного допису. У разі використання `--post changes` або `problems` перевірки, які не були опубліковані, все одно залишаються в журналі свідків, а `verify.py` вказує їх як такі, що ніколи не публікувалися; у записі початку вказано назву політики. Кожна перевірка все одно з’являється в журналі, тому менша кількість публікацій означає меншу кількість незалежних моментів у Telegram, а не меншу кількість перевірок.

Навіть без каналу TgWitness все одно зберігає свій журнал. Зберігайте відбиток ключа TgWitness (`python -m tgwitness.witness fingerprint`) в іншому місці.

## Публічна сторінка з доказами для декількох робочих просторів

`python -m tgwitness.proof` witnesses підтримує до 32 робочих просторів одночасно та надає сторінку, доступну лише для читання, з останньою підписаною перевіркою кожного з них. Кожен робочий простір отримує власний ключ свідка та журнал у папці data, а також закріплений ключ колектора; публікація у каналі Telegram є необов’язковою для кожного робочого простору. Почніть із [файлу proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example):

| Галузь | Значення |
| --- | --- |
| `title` | Заголовок сторінки, 1–100 символів |
| `data_dir` | Ключі та журнали Witness, пов’язані з файлом; за замовчуванням `proof-data` |
| `interval`, `timeout` | Кількість хвилин між перевірками (1–1440, за замовчуванням 5); кількість секунд очікування (5–600, за замовчуванням 20) |
| `workspaces[].id`, `label` | Короткий псевдонім малими літерами та ім’я, що відображається |
| `workspaces[].collector` | Адреса Collector; інші робочі простори закінчуються на `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | Обов’язкове, різне для кожного робочого простору |
| `workspaces[].token_file` | Файл із токеном-свідком цього робочого простору, доступним лише для читання |
| `workspaces[].channel`, `bot_token_file` | Опціонально, разом: публікувати кожну перевірку в каналі |
| `workspaces[].proxy`, `bot_api` | Опціональний маршрут та адреса API-інтерфейсу бота |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

Перша команда перевіряє файл та файли токенів, не встановлюючи з’єднання. Сторінка відповідає лише на запити GET та HEAD:

- `/` Показує всі робочі простори; робочий простір, який не перевірявся протягом 2,5 інтервалів, позначається як застарілий.
- `/api/proof` повертає те саме, що й JSON.
- `/api/proof/<id>` завантажує останню підписану заяву (`tgwitness-public-proof-v1`): номер та хеш запису свідка, статус, закріплений ключ збирача, контрольна точка, лічильники збору даних та інформація про те, чи вдалося опублікувати допис у каналі, підписаний ключем свідка цього робочого простору.
- `/healthz` Повертає код 503, коли монітор робочого простору припинив роботу.

Присвойте сторінці власне ім’я хосту, як-от [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example). Для перевірки експортуйте журнал свідчень робочого простору за допомогою `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` та використовуйте його як описано нижче.

## Перевірити

З боку користувача TgWitness експортуйте цей журнал:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

Далі, будь-де, за допомогою підписаного ZIP-файлу колектора та каналу, експортованого з Telegram Desktop (*Експорт історії чату* → JSON дає `result.json` ) або його публічної сторінки `https://t.me/s/…` :

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` перевіряє журнал свідка (ланцюжок і підписи), а потім те, чи **кожен заголовок, який бачив свідок, є частиною експортованого журналу**: запис за цим номером повинен мати саме цей хеш. Заголовок, що не збігається, не проходить перевірку — журнал було змінено після того, як свідок його побачив. Він також повідомляє про заголовки, побачені після експорту, аномалії, які зафіксував свідок, відповіді, що не пройшли перевірку, періоди, відповідні контрольні точки яких присутні в цьому експорті («Засвідчено від X до Y») та пропуски. Пізніші контрольні точки не подовжують ці періоди. Результат містить номер останнього збіжного запису та кількість наступних записів, для яких немає відповідного контрольного пункту. Враховуються лише відповіді, підписані власним ключем експорту: експорт, підписаний ключем, якого свідок ніколи не бачив, повідомляється як не засвідчений, і без `--fingerprint` його підписувач залишається не закріпленим. З `--channel` кожен підписаний допис повинен збігатися з журналом свідка запис за записом: змінені дописи не проходять перевірку, відсутні дописи вказуються у списку. Дата у наданому JSON-експорті Telegram є редагованими метаданими, що не входять до підписаного токена свідка. Збіг токена не підтверджує дату публікації; у результаті явно зазначається, що перевірка часу публікації не проводилася.

### Необхідна межа експорту з підтвердженням

Для передачі, яка має містити остаточний запис у присутності свідків, додайте `--require-witness`:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

Для цього необхідний незалежно збережений відбиток свідка та відповідна контрольна точка саме в кінці цього експорту. Контрольна точка, що охоплює лише попередній префікс, є недостатньою. Призупиніть збір даних, дайте свідку можливість перевірити кінцевий стан і виконайте експорт до подальшого запису в журнал; якщо журнал зміниться, збережіть ще одну контрольну точку та експортуйте цей стан. Один лише пізніший контрольний пункт не може підтвердити кінцевий хеш коротшого експорту. Коли також надається `--channel`, відсутність заявлених публікацій або порожній набір збігів не проходять цю сувору перевірку. Без цього прапорця звичайні перевірки цілісності все одно повідомляють про записи без свідків, не відхиляючи при цьому архів, який в іншому випадку є цілим.

Keep the witness journal and its pinned key separately．Online checks verify continuity between checkpoints；offline verification compares every retained checkpoint with the export．Legacy heads without continuity proofs retain the offline comparison and are reported without online continuity verification．The report lists witness downtime and failed publications by interval．
