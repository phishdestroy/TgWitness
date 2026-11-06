# Carica cronologia sorgente

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/history/

Carica i messaggi precedenti dalle fonti abilitate, metti in pausa e riprendi, quindi verifica un rapporto sullo stato di avanzamento firmato.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Raccolta](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Raccolta](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, esaminare le chat abilitate, mettere in pausa l’osservazione, scegliere l’API standard o l’esportazione Takeout, quindi selezionare **Carica cronologia completa**. L’esecuzione corregge l’elenco delle fonti e legge i loro messaggi passati disponibili nelle chat e nel registro di osservazione firmato. I file multimediali utilizzano le impostazioni esistenti relative agli allegati e la coda di download permanente. Ciò è distinto dall’esportazione JSON/HTML firmata per singola chat.

Per la raccolta a livello di account, selezionare **Intero account**, avviare l’osservazione per caricarne l’ elenco delle fonti e rivedere tale elenco prima di avviare la cronologia. Il limite dell’elenco delle finestre di dialogo rimane valido (1,000 per impostazione predefinita, regolabile in Parametri). Un’esecuzione riuscita non garantisce che tutte le finestre di dialogo dell’account siano state elencate. Le chat scoperte o abilitate in un secondo momento richiedono un’altra esecuzione. Mettere in pausa l’osservazione prima di avviare la cronologia; un’acquisizione può gestire un solo account alla volta.

Scegliere da uno a cinque worker per gli allegati e se conservare le Azioni recenti disponibili e confrontare le versioni salvate in precedenza. L’esportazione potrebbe richiedere l’approvazione in Telegram e un tempo di attesa specificato dal server. Queste opzioni rimangono fisse al ripristino. Vedere [il comportamento di backfill e il contratto di prova](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) per i dettagli relativi a trasporto, riprova e affidabilità.

## Pausa, riavvio e risultati parziali

- **Cronologia delle pause** interrompe la lettura. **Cronologia delle continuazioni** riprende dall’ultimo messaggio salvato in ciascuna fonte; anche il riavvio dell’app lascia l’esecuzione in pausa fino alla ripresa. La ripresa richiede lo stesso account Telegram inattivo.
- L’osservazione del messaggio, l’elaborazione degli allegati e il salvataggio della posizione del cursore avvengono in un’unica transazione. Una sessione ripresa non ripete le osservazioni già salvate. L’acquisizione in tempo reale o una sessione separata, avviata esplicitamente, può osservare in modo indipendente lo stesso messaggio.
- Ogni fonte (ogni intervallo suddiviso di Telegram in Takeout) assegna un ID messaggio massimo alla sua prima lettura. I messaggi più recenti appartengono all’ osservazione in tempo reale, non alle restanti pagine storiche di quella fonte.
- Le fonti inaccessibili e quelle disabilitate durante l’acquisizione rimangono visibili come non riuscite o saltate. Le altre fonti proseguono; il risultato complessivo è incompleto.
- I ritardi di FloodWait rispettano il backoff dell’account salvato. In caso di errori transitori, vengono effettuati fino a cinque tentativi; l’esaurimento delle risorse e lo spazio su disco insufficiente causano una pausa con il cursore intatto.
- **Terminare questa esecuzione della cronologia** conserva le osservazioni salvate. Non le rimuove né annulla i processi di allegato dell’API standard. Terminando Takeout, i file Takeout rimanenti vengono contrassegnati come saltati; mettendolo in pausa, rimangono riprendibili. Una nuova esecuzione legge nuovamente le fonti abilitate.

Il completamento della cronologia descrive solo le letture della cronologia. Gli allegati potrebbero rimanere in sospeso, fallire o essere esclusi in base alla politica configurata. Verificare le conferme di ricezione dei file multimediali nel registro e nella coda degli allegati; solo una conferma di ricezione completata con byte conservati costituisce un allegato salvato. L’operazione relativa alla cronologia è una richiesta esplicita di snapshot ed è distinta dai parametri che selezionano le categorie di eventi live futuri.

## Trasferimento e verifica

Salvare il **rapporto di avanzamento firmato**, quindi utilizzare **«Esporta prove»** per scaricare il registro e gli allegati salvati. Un’esportazione successiva delle prove potrebbe includere registrazioni aggiuntive; il rapporto associa i propri contatori al prefisso del registro al momento della sua creazione. Eseguire il verificatore da un checkout affidabile di questa versione:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Mantenere separatamente l’impronta digitale prevista della chiave di firma. Il verificatore controlla la firma del rapporto, l’archivio delle prove, il checkpoint del rapporto, il piano sorgente, l’account e il conteggio dei messaggi salvati/non disponibili. Le nuove esecuzioni associano inoltre lo stato di avanzamento del codice sorgente e le opzioni agli eventi del cursore firmati. Senza l’`--evidence`, verifica solo il rapporto firmato e la sua coerenza interna. I campi di avanzamento legacy e i riepiloghi degli allegati rimangono dichiarazioni firmate dal collettore. Il verificatore delle prove controlla i byte multimediali archiviati.

Né la firma né il completamento della cronologia disponibile dimostrano l’origine da Telegram, un’istantanea atomica o la completezza storica. I messaggi possono cambiare durante la lettura; i messaggi eliminati e le modifiche intermedie al di fuori delle Azioni recenti disponibili e delle Chat segrete non vengono recuperati. Un operatore che controlla la chiave di firma può fabbricare un registro prima che esistano impegni esterni. Utilizzare punti di controllo conservati separatamente o un testimone indipendente per le proprietà documentate di rilevamento delle manomissioni.

Il cursore di acquisizione riflette lo stato dell’area di lavoro locale. Il ripristino del solo file ZIP contenente le prove non ripristina un’attività di acquisizione in sospeso né una sessione di Telegram. Conservare il backup dell’area di lavoro se è necessario proseguire l’attività originale.
