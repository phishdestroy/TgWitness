# Carica cronologia sorgente

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/history/

Carica i messaggi precedenti dalle fonti abilitate, metti in pausa e riprendi, quindi verifica un rapporto sullo stato di avanzamento firmato.

**Versione principale attuale:** disponibile dal codice sorgente; non inclusa nell’anteprima portatile della versione 0.7.0.

In **«Fonti**», esamina le chat abilitate, avvia l’osservazione, quindi seleziona **«Carica cronologia completa**». L’esecuzione fissa l’elenco delle fonti e importa i messaggi passati disponibili nelle «Chat» e nel registro di osservazione firmato. I file multimediali utilizzano le impostazioni di allegato esistenti e la coda di download permanente. Ciò è distinto dall’esportazione JSON/HTML firmata per singola chat.

Per la raccolta a livello di account, selezionare **«Intero account»**, avviare l’osservazione per caricare il relativo elenco delle fonti e verificare tale elenco prima di avviare la cronologia. Il limite dell’elenco delle finestre di dialogo rimane valido (1.000 per impostazione predefinita, regolabile in «Parametri»). Un’esecuzione riuscita non garantisce che tutte le conversazioni dell’account siano state incluse nell’elenco. Le chat scoperte o abilitate in un secondo momento richiedono un’altra esecuzione.

## Pausa, riavvio e risultati parziali

- **La cronologia in pausa** interrompe la lettura. **La cronologia "Continua"** riprende dall’ultimo messaggio salvato in ciascuna fonte; anche il riavvio dell’app lascia l’esecuzione in pausa fino alla ripresa. Riavviare prima l’osservazione. La ripresa richiede lo stesso account Telegram.
- L’osservazione del messaggio, l’elaborazione degli allegati e il salvataggio della posizione del cursore avvengono in un’unica transazione. Una sessione ripresa non ripete le osservazioni già salvate. L’acquisizione in tempo reale o una sessione separata, avviata esplicitamente, può osservare in modo indipendente lo stesso messaggio.
- Ogni fonte assegna un ID massimo ai messaggi al momento della prima lettura. I messaggi più recenti appartengono all’ osservazione in tempo reale, non alle pagine storiche rimanenti di quella fonte.
- Le fonti inaccessibili e quelle disabilitate durante l’acquisizione rimangono visibili come non riuscite o saltate. Le altre fonti proseguono; il risultato complessivo è incompleto.
- I ritardi di FloodWait rispettano il backoff dell’account salvato. I timeout di trasmissione e lo spazio su disco insufficiente sospendono l’esecuzione lasciando il cursore intatto. Riprendere dopo aver risolto la causa.
- **La chiusura di questa sessione di cronologia** conserva le osservazioni salvate. Non le rimuove né annulla i download degli allegati già in coda. Una nuova sessione legge nuovamente le fonti abilitate.

Il completamento della cronologia descrive solo le letture della cronologia. Gli allegati potrebbero rimanere in sospeso, fallire o essere esclusi in base alla politica configurata. Verificare le conferme di ricezione dei file multimediali nel registro e nella coda degli allegati; solo una conferma di ricezione completata con byte conservati costituisce un allegato salvato. L’operazione relativa alla cronologia è una richiesta esplicita di snapshot ed è distinta dai parametri che selezionano le categorie di eventi live futuri.

## Trasferimento e verifica

Salvare il **rapporto di avanzamento firmato**, quindi utilizzare **«Esporta prove»** per scaricare il registro e gli allegati salvati. Un’esportazione successiva delle prove potrebbe includere registrazioni aggiuntive; il rapporto associa i propri contatori al prefisso del registro al momento della sua creazione. Eseguire il verificatore da un checkout affidabile di questa versione:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Conservare separatamente l’impronta digitale prevista della chiave di firma. Il verificatore controlla la firma del rapporto, l’archivio delle prove, il checkpoint del rapporto, il piano di origine, l’account e il conteggio dei messaggi salvati/non disponibili. Senza `--evidence`, controlla solo il rapporto firmato e la sua coerenza interna. Le fasi di avanzamento, i titoli, i cursori e i riepiloghi degli allegati sono dichiarazioni firmate dal raccoglitore, non ricostruite in modo indipendente da questo strumento di verifica del rapporto. Il verificatore delle prove controlla comunque i byte multimediali archiviati.

Né la firma né il completamento della cronologia disponibile dimostrano l’origine da Telegram, un’istantanea atomica o la completezza storica. I messaggi possono cambiare durante la lettura; i messaggi cancellati, le modifiche intermedie non visualizzate e le chat segrete non vengono recuperati. Un operatore che controlla la chiave di firma può fabbricare un registro prima che esistano impegni esterni. Utilizzare punti di controllo conservati separatamente o un testimone indipendente per le proprietà documentate di rilevamento delle manomissioni.

Il cursore di acquisizione riflette lo stato dell’area di lavoro locale. Il ripristino del solo file ZIP contenente le prove non ripristina un’attività di acquisizione in sospeso né una sessione di Telegram. Conservare il backup dell’area di lavoro se è necessario proseguire l’attività originale.
