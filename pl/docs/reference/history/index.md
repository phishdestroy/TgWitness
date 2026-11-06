# Wczytaj historię źródła

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/history/

Pobieraj poprzednie wiadomości z włączonych źródeł, wstrzymuj i wznawiaj proces oraz weryfikuj podpisany raport z postępów.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Kolekcja](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collection](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Wstrzymywanie, wznawianie i wyniki częściowe

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- Obserwacja wiadomości, operacja na załączniku i zatwierdzenie pozycji kursora odbywają się w ramach jednej transakcji. Wznowione uruchomienie nie powtarza już zatwierdzonych obserwacji. Obserwacja na żywo lub oddzielne, jawnie uruchomione zadanie mogą niezależnie obserwować tę samą wiadomość.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Źródła niedostępne oraz źródła wyłączone podczas pozyskiwania danych pozostają widoczne jako nieudane lub pominięte. Pozostałe źródła działają dalej; ogólny wynik jest niekompletny.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

Operacja uzupełniania historii dotyczy wyłącznie odczytów historii. Załączniki mogą pozostać w toku, nie powiodć się lub zostać wykluczone przez skonfigurowaną politykę. Należy sprawdzić potwierdzenia odbioru multimediów w dzienniku oraz w kolejce załączników; jedynie zakończone potwierdzenie odbioru z zachowanymi bajtami stanowi zapisany załącznik. Operacja historii jest wyraźnym żądaniem utworzenia migawki i jest oddzielna od przełączników wybierających kategorie przyszłych zdarzeń na żywo.

## Przesyłanie i weryfikacja

Zapisz **podpisany raport z postępów**, a następnie skorzystaj z opcji **„Eksportuj dowody”**, aby pobrać dziennik i zapisane załączniki. Późniejszy eksport dowodów może zawierać dodatkowe zapisy; raport wiąże swoje liczniki z prefiksem dziennika z momentu jego utworzenia. Uruchom weryfikator z zaufanej kopii tej wersji:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

Kursor pozyskiwania danych odzwierciedla stan lokalnego obszaru roboczego. Samo przywrócenie pliku ZIP z dowodami nie powoduje przywrócenia oczekującego zadania pozyskiwania danych ani sesji Telegramu. Należy zachować kopię zapasową obszaru roboczego, jeśli wymagana jest kontynuacja pierwotnego zadania.
