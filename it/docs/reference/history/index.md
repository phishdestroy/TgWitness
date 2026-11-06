# Carica cronologia sorgente

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/history/

Carica i messaggi precedenti dalle fonti abilitate, metti in pausa e riprendi, quindi verifica un rapporto sullo stato di avanzamento firmato.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Raccolta](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collection](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Pausa, riavvio e risultati parziali

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- L’osservazione del messaggio, l’elaborazione degli allegati e il salvataggio della posizione del cursore avvengono in un’unica transazione. Una sessione ripresa non ripete le osservazioni già salvate. L’acquisizione in tempo reale o una sessione separata, avviata esplicitamente, può osservare in modo indipendente lo stesso messaggio.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Le fonti inaccessibili e quelle disabilitate durante l’acquisizione rimangono visibili come non riuscite o saltate. Le altre fonti proseguono; il risultato complessivo è incompleto.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

Il completamento della cronologia descrive solo le letture della cronologia. Gli allegati potrebbero rimanere in sospeso, fallire o essere esclusi in base alla politica configurata. Verificare le conferme di ricezione dei file multimediali nel registro e nella coda degli allegati; solo una conferma di ricezione completata con byte conservati costituisce un allegato salvato. L’operazione relativa alla cronologia è una richiesta esplicita di snapshot ed è distinta dai parametri che selezionano le categorie di eventi live futuri.

## Trasferimento e verifica

Salvare il **rapporto di avanzamento firmato**, quindi utilizzare **«Esporta prove»** per scaricare il registro e gli allegati salvati. Un’esportazione successiva delle prove potrebbe includere registrazioni aggiuntive; il rapporto associa i propri contatori al prefisso del registro al momento della sua creazione. Eseguire il verificatore da un checkout affidabile di questa versione:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

Il cursore di acquisizione riflette lo stato dell’area di lavoro locale. Il ripristino del solo file ZIP contenente le prove non ripristina un’attività di acquisizione in sospeso né una sessione di Telegram. Conservare il backup dell’area di lavoro se è necessario proseguire l’attività originale.
