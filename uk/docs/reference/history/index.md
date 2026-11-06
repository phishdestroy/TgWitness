# Завантажити історію джерел

Canonical page: https://phishdestroy.github.io/TgWitness/uk/docs/reference/history/

Завантажуйте минулі повідомлення з увімкнених джерел, призупиняйте та відновлюйте процес, а також перевіряйте підписаний звіт про хід роботи.

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Призупинення, поновлення та часткові результати

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- Спостереження за повідомленням, обробка вкладень та фіксація позиції курсора відбуваються в одній транзакції. При відновленні виконання вже зафіксовані спостереження не повторюються. У режимі реального часу або під час окремого, явно запущеного циклу виконання може відбуватися незалежне спостереження за тим самим повідомленням.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Джерела, до яких неможливо отримати доступ, та джерела, вимкнені під час збору даних, залишаються видимими як «неуспішні» або «пропущені». Інші джерела продовжують працювати; загальний результат є неповним.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

Поняття «завершення історії» стосується лише зчитування історії. Вкладення можуть залишатися в стані очікування, завершуватися невдало або виключатися згідно з налаштованою політикою. Перевіряйте підтвердження отримання медіафайлів у журналі та черзі вкладень; лише завершене підтвердження з збереженими байтами вважається збереженим вкладенням. Операція з історією є явним запитом на створення знімка і відрізняється від параметрів, що вибирають категорії майбутніх подій у реальному часі.

## Передача та перевірка

Збережіть **підписаний звіт про хід роботи**, а потім скористайтеся **функцією «Експорт доказів»**, щоб завантажити журнал та збережені вкладення. Пізніший експорт доказів може містити додаткові записи; звіт прив’язує свої лічильники до префікса журналу на момент його створення. Запустіть верифікатор із надійної версії цієї версії:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

Курсор збору даних відображає стан локального робочого простору. Відновлення лише ZIP-файлу з доказами не відновлює завдання збору даних, що перебуває в процесі виконання, або сеансу Telegram. Зберігайте резервну копію робочого простору, якщо потрібно продовжити виконання початкового завдання.
