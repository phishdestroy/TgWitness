# Загрузить историю источников

Canonical page: https://phishdestroy.github.io/TgWitness/ru/docs/reference/history/

Загрузка прошлых сообщений из включенных источников, приостановка и возобновление, а также проверка подписанного отчета о ходе работы.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Документация](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Коллекция](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collection](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Приостановка, возобновление и частичные результаты

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- Наблюдение за сообщением, обработка вложений и фиксация положения курсора выполняются в одной транзакции. При возобновлении выполнения уже зафиксированные наблюдения не повторяются. В режиме реального времени или в рамках отдельного, явно запущенного цикла могут независимо наблюдаться одни и те же сообщения.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Недоступные источники и источники, отключенные во время сбора данных, остаются видимыми как «неудачные» или «пропущенные». Работа с остальными источниками продолжается; общий результат является неполным.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

Завершение истории описывает только чтение истории. Вложения могут оставаться в ожидании, завершиться сбоем или быть исключены в соответствии с настроенной политикой. Проверяйте подтверждения получения медиафайлов в журнале и в очереди вложений; только завершенное подтверждение с сохраненными байтами считается сохраненным вложением. Операция с историей представляет собой явный запрос на создание моментального снимка и не связана с параметрами, выбирающими категории будущих событий в режиме реального времени.

## Передача и проверка

Сохраните **подписанный отчёт о ходе работы**, а затем воспользуйтесь **функцией «Экспорт доказательств»**, чтобы загрузить журнал и сохраненные вложения. Более поздний экспорт доказательств может включать дополнительные записи; отчёт привязывает свои счетчики к префиксу журнала на момент его создания. Запустите верификатор из надёжной копии этой версии:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

Курсор сбора данных отражает состояние локальной рабочей области. Восстановление только ZIP-архива с доказательствами не приводит к восстановлению ожидающего выполнения задания на сбор данных или сеанса Telegram. Сохраните резервную копию рабочей области, если требуется продолжение выполнения исходного задания.
