# Configurazione e verifica dei report

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/case-reports/

Filtri per i report, otto modelli, impostazioni predefinite per i contenuti, cronologie delle modifiche salvate e la valutazione inclusa nelle esportazioni firmate.

Trasformare le osservazioni selezionate in una descrizione leggibile del caso: la sua domanda, l’ambito, le modifiche salvate, i grafici, i risultati e i riferimenti alle fonti. Ogni rapporto offre al destinatario la possibilità di verificare il materiale consegnato e di esaminarne la copertura della raccolta.

La sezione **«Basi di fiducia e limitazioni**» compare nei report relativi a registro, consegna, chat, account e condivisione. I PDF relativi al registro e alla consegna utilizzano la stessa valutazione del loro file «`report.json`» firmato. I manifesti ZIP contengono «`case_assessment`» nel manifesto firmato. Tale valutazione accompagna il materiale esportato. Le osservazioni originali mantengono le loro firme esistenti.

## Formati dei documenti e ordine di lettura

### Report Studio

Aprire **Esportazioni → Configura e anteprima**. Procedere attraverso **Dati → Progettazione e contenuti → Anteprima**:

1. Utilizzare l’intero spazio di lavoro oppure selezionare chat, autori, date di osservazione UTC inclusive e tipi di evento. Caricare il catalogo per cercare chat e autori, oppure inserire i relativi ID Telegram. I filtri per autore corrispondono agli ID dei mittenti registrati; una notifica di cancellazione priva di mittente non corrisponde a un filtro per autore.
2. Scegli un layout di pagina, quindi seleziona i grafici, le etichette dei partecipanti, la trascrizione e le tue conclusioni scritte. Modificando il layout, queste scelte vengono mantenute.
3. Generare l’anteprima. Essa mostra i conteggi effettivi, l’attività, i partecipanti, i record di esempio, le modifiche salvate e gli intervalli di numeri di messaggi mancanti. La modifica di una scelta rende l’anteprima non più aggiornata. Salvare prima di scaricare l’HTML, il PDF firmato, il JSON firmato o il file ZIP contenente le prove.

L’anteprima dei dati riporta il prefisso completo e stabile del registro, non un campione iniziale. Solo le righe di esempio visualizzate e gli elenchi lunghi sono limitati; i relativi conteggi omessi vengono mostrati. Un’esportazione successiva acquisisce una nuova istantanea stabile, pertanto la raccolta in corso potrebbe aumentare le cifre. Ambito, conteggi e identità della fonte sono inclusi nel rapporto firmato. L’apertura o l’anteprima del modulo non ne comporta il salvataggio.

**Scegliere la copia destinata al destinatario.** I grafici e la trascrizione utilizzano i record selezionati. Integrità, custodia e copertura descrivono l’intero registro delle fonti. Il file ZIP delle prove contiene i record originali e gli allegati. Utilizzare [una consegna ridotta al minimo](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#handover-extract) quando un destinatario deve ricevere solo i dati selezionati e autorizzati.

### Leggi le modifiche, le cancellazioni e gli ID mancanti

Una modifica mostra il testo salvato **"Prima"** e **"Dopo"** ed evidenzia le parole modificate. Una cancellazione mostra l’ultima versione salvata prima della segnalazione. Se non è stato acquisito alcun contenuto precedente, il report lo indica. Quando si selezionano solo le modifiche o le cancellazioni, le versioni precedenti rimangono disponibili come contesto esplicitamente etichettato al di fuori dei filtri. I messaggi non correlati non vengono aggiunti a queste cronologie.

**Gli ID dei messaggi non osservati** sono lacune tra i numeri noti nelle chat selezionate e l’ intervallo di ID derivato dalla data. Ogni record di origine noto viene verificato prima di dichiarare un numero come non osservato: l’esclusione di un altro autore, di un tipo di evento o di una data non può creare una falsa lacuna. I messaggi salvati adiacenti vengono etichettati come contesto. Un numero mancante non dimostra che un messaggio esistesse o sia stato cancellato; le notifiche di cancellazione e le ricontrolli non andati a buon fine rimangono tipi di evento distinti.

### Scegli un design

Sono disponibili otto modelli di pagina per i report in formato HTML (diario e singola chat) e PDF firmati. Essi utilizzano gli stessi dati e calcoli, con copertine, tipografia, titoli dei capitoli, tabelle e spaziatura diversi.

| Progettazione | Stile di lettura |
| --- | --- |
| Classico | Un fascicolo tradizionale con copertina scura e sezioni numerate. |
| Note redazionali | Una pagina del titolo con cornice serif, margini ampi e un'asta dei capitoli stretta. |
| Briefing | Una copertina compatta con dorso blu navy, titoli brevi e tabelle ravvicinate. |
| Analisi | Copertina in stile questionario, grafici modulari e figure a spaziatura fissa. |
| Tecnico | Un registro a righe, un indice numerato e tabelle di confronto precise. |
| Panoramica | Una copertina panoramica, una spaziatura generosa e figure riassuntive ben visibili. |
| Serie di letture | Una barra laterale e capitoli raggruppati per risultati, ambito, modifiche e registro delle osservazioni. |
| Registro e margine | Capitoli numerati con ampi margini, tabelle grafiche precise e una trascrizione separata dei messaggi. |

Il layout viene salvato per ogni area di lavoro e registrato nel manifesto di esportazione firmato. L’HTML funziona offline, supporta i temi chiaro e scuro e si adatta agli schermi stretti e alle lingue scritte da destra a sinistra. I PDF nativi utilizzano i font integrati; il design editoriale include Noto Serif con la relativa licenza SIL Open Font License integrata. Le serie di lettura e Ledger & margin si applicano anche alle panoramiche degli account, alle chat degli account e alle copie condivise.

I file PDF in cinese, giapponese e coreano richiedono inoltre un font adeguato sul server, come Noto Sans CJK, installato a livello di sistema o collocato nella directory `TGWITNESS_FONT_DIR`. Se non è disponibile, il file ZIP conserva i report in formato HTML e JSON.

Questi due modelli includono un registro leggibile senza JavaScript. Per esportazioni di grandi dimensioni, questa visualizzazione contiene fino a 500 record completi entro un limite di input di 8 MiB; il report indica il limite e rimanda al visualizzatore completo e ai record di origine. La directory degli account e l’indice delle relazioni descrivono lo stesso campione di lettura, non tutti i partecipanti. I grafici del registro completo mantengono il loro ambito specificato separatamente.

### Scegli i contenuti

| Indice predefinito | Inclusi di default |
| --- | --- |
| Fascicolo del caso | Attività, orari delle osservazioni, partecipanti, chat e trascrizione del registro. |
| Briefing | Una panoramica delle attività senza classifiche dei partecipanti né trascrizioni. |
| Revisione delle attività | Attività, orari delle osservazioni, partecipanti, chat e composizione, con riferimenti alle fonti e cifre esatte. |
| Rapporto personalizzato | Una combinazione personalizzata di grafici, trascrizioni e anteprime. |

La modifica di un'impostazione predefinita mantiene inalterati il layout, i dettagli del caso e l’analisi scritta. I controlli di integrità, la copertura, le limitazioni e le istruzioni di verifica rimangono in ogni layout. I record sorgente nel file ZIP rimangono invariati quando un grafico o una trascrizione vengono nascosti.

Le **note di esame** opzionali contengono la domanda, il metodo, i risultati e la conclusione redatti dall’autore del rapporto. Citare il file di origine e i numeri dei record nei risultati. La firma conserva queste dichiarazioni dell’autore insieme al rapporto; le osservazioni di origine e l’interpretazione dell’autore rimangono identificabili. I passaggi di consegne ridotti al minimo omettono queste note private e le cartelle cliniche complete. Le scelte relative alle cartelle cliniche e agli esami si applicano ai referti.

Selezionare l’attività nel tempo, la mappa di calore UTC per giorno della settimana/ora, le classifiche dei partecipanti, le classifiche delle chat e la composizione dei record. Scegliere da 5 a 30 gruppi classificati e alias neutri dei partecipanti o ID degli account. I mittenti sconosciuti e i restanti partecipanti sono riportati in righe separate. Gli alias influiscono solo sui grafici; i record di origine contengono comunque le loro identità.

L’anteprima del layout si aggiorna dalla bozza non salvata utilizzando la copertina di produzione, l’esame e i componenti dei grafici, limitatamente alle corrispondenze presenti nei primi 50.000 record di origine. L’anteprima dei dati sottostante calcola la selezione completa. È esplicitamente non firmata e non conserva le modifiche. I pulsanti “Copertina” e “Grafici” consentono di passare da una sezione all’altra. Non si tratta di un’anteprima PDF completa. L’opzione **“Salva impostazioni del report”** applica le scelte alle future esportazioni; i file firmati esistenti sono immutabili. Il PDF utilizza la copertina scelta, la tipografia, il layout dei capitoli e gli stessi aggregati selezionati per l’HTML e il JSON firmato.

La valutazione dell’affidabilità, i limiti di copertura e le istruzioni di verifica rimangono presenti. Nascondere i grafici o la trascrizione leggibile non rimuove le righe delle fonti autorevoli dal file ZIP. Le serie di grafici disabilitate vengono omesse dal JSON analitico; utilizzare un’ esportazione ridotta al minimo per limitare la divulgazione dei record di origine.

I filtri di selezione dei dati si applicano ai report di registro; le esportazioni relative agli account e alla condivisione mantengono il proprio ambito di acquisizione e divulgazione.

Le preferenze condivise relative al design e ai grafici vengono mantenute nelle nuove esportazioni di chat e account e nelle anteprime di condivisione degli account. Le impostazioni relative alla lingua e alla privacy dell’account e della condivisione rimangono indipendenti; le note private relative ai casi e alle indagini non vengono copiate in queste esportazioni. I rapporti relativi all’account e alla condivisione rimangono in formato HTML protetti dal loro manifesto di archivio firmato. Il diario, il passaggio di consegne del diario ridotto a icona e i kit per chat singola forniscono anch’essi PDF firmati.

### Cosa indicano i grafici

L’attività del registro e le mappe di calore contano **le osservazioni** nuove, storiche, recuperate, modificate, eliminate e mancanti al ricontrollo, in base all’ora di osservazione del collettore in UTC. Gli heartbeat e le conferme di ricezione degli allegati sono esclusi. Le classifiche dei partecipanti contano solo le osservazioni di messaggi nuove, storiche e recuperate: un mittente non viene dichiarato come autore della modifica o dell’eliminazione. Osservazioni ripetute possono descrivere lo stesso messaggio di Telegram.

L’analisi dei log conserva i conteggi per tipo, i riferimenti al primo/ultimo record e l’SHA-256 del file sorgente ` `events.jsonl``. Le cifre includono valori esatti in HTML e PDF. I segmenti giornalieri passano a intervalli mensili oltre i 366 giorni registrati; i grafici li combinano in un massimo di 36 intervalli di uguale ampiezza. Più di 100.000 identificatori distinti o 1.200 mesi rendono il grafico interessato non disponibile, mentre i conteggi complessivi esatti rimangono disponibili.

I grafici relativi agli snapshot e alla condivisione degli account contano solo le righe dei messaggi non di servizio incluse, utilizzando l’ora di invio registrata dei messaggi. Gli aggregati di condivisione vengono calcolati dopo la redazione e il filtraggio. Questi grafici utilizzano al massimo 90 intervalli di data UTC di uguale ampiezza e conservano fino a 10.000 valori di raggruppamento; i conteggi in eccesso vengono esplicitamente dichiarati e riconciliati. L’ultimo intervallo può essere più breve. Le date sconosciute o approssimative non vengono inserite nei grafici temporali.

Un intervallo vuoto indica l’assenza di osservazioni incluse; consultare la copertura per individuare eventuali lacune. Questi grafici descrivono l’attività salvata. I mittenti sconosciuti rimangono in una categoria separata e ogni controllo viene riportato singolarmente.

Quando incluso, il file `analytics.json` è protetto dagli hash dei file firmati dell’archivio. Il file `report.json` del registro incorpora lo stesso aggregato selezionato. La verifica della firma rileva i byte modificati. Per verificare i dati, ricalcolare gli aggregati del registro con `report_analytics.Analytics` e `selected`, oppure gli aggregati dello snapshot con `snapshot_analytics.collect` e `project`.

### Anomaly indicators

**Preview.** Evidence reports add an **Anomaly indicators** section computed by registered processors (`tgwitness/metrics/`, one file per metric). The report names every processor that ran with its version, and prints its method under its table, so the computation can be repeated from `events.jsonl` with `tgwitness.metrics.run`.

| Processor | Cosa mostra |
| --- | --- |
| `first_time_posters_over_time` v1 | First-time posters and messages per UTC day．A flag requires at least five first-time posters and three times their median，with message volume at most 1.5 times its median．The baseline uses at least seven observed days within the previous 14 calendar days，after seven days of warm-up． |
| `service_vs_message_ratio` v1 | Distinct saved message numbers per chat and the share used by service messages. It describes a numbering; it does not explain a particular missing number. |
| `join_leave_per_month` v1 | Joins, departures and removals or bans per month, one per person, chat, change and day. |
| `pinned_per_month` v1 | Pin service messages, unpin notices, and pinned messages added or removed between chat-state snapshots, per month. |

**Parameters → Report metrics** selects processors and the number of displayed rows， including in filtered reports．Daily and monthly tables show recent rows，service-share tables rank chats by saved message count．Totals cover every row．

Partendo da un checkout del codice sorgente, creare tutti e otto i modelli sopra elencati a partire dallo stesso diario fittizio:

```
python tools/build_report_styles.py --output test-results/report-styles
```

Aprire il file `index.html` risultante per confrontare i report HTML completi, i PDF firmati e i file ZIP. Ogni progetto utilizza lo stesso registro di origine. Utilizzare una nuova directory di output per ogni esecuzione, in modo da conservare gli esempi firmati in precedenza.

![Dossier HTML fittizio](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

Il codice HTML si apre con una copertina del caso e i dati salienti. La mappa delle prove numerata rimanda a ciascun risultato, ai fatti a sostegno, ai limiti e alla revisione indipendente. I record ricercabili e i riferimenti stabili ai record rimangono disponibili nel visualizzatore offline. Il design si adatta agli schermi stretti, a entrambi i temi e ai browser senza JavaScript.

Il PDF firmato presenta una copertina A4 dedicata, un riferimento al rapporto e un codice QR, una sintesi esecutiva, una mappa delle prove, risultati numerati e segnalibri per i documenti. Le intestazioni e i piè di pagina identificano il rapporto. Un codice QR identifica il materiale; non si tratta di un risultato di verifica indipendente. Le stampe dal browser sono separate da questo PDF firmato crittograficamente.

La cronologia delle osservazioni colloca i periodi di osservazione registrati e le interruzioni sullo stesso asse UTC. Lo spazio vuoto non indica una copertura dedotta; le tabelle dettagliate mantengono gli intervalli esatti. Il file ZIP contiene i report leggibili, i file JSON firmati, i record di origine e le istruzioni di verifica.

Creare un dossier nuovo e fittizio in inglese/russo/tedesco con l’ambiente di sviluppo installato:

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Ogni directory linguistica contiene `report.html`, `report.pdf`, `report.json` e `dossier.zip`. Le directory di esempio esistenti non vengono mai sovrascritte. Per la creazione non vengono utilizzati né account Telegram, né servizi esterni di marcatura temporale, né connessioni di rete.

![Prime tre pagine del PDF fittizio firmato](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## Analisi di un caso concreto

Per un registro di 1.200 voci con un timestamp convalidato alla voce numero 1.000, il rapporto identifica 200 voci successive al di fuori dell’intervallo di quel timestamp. Si tratta di un limite massimo relativo all’esistenza di un checkpoint, non di una prova dell’ora di invio di ciascun messaggio . Se altri tre file di timestamp non superano la convalida o non possono essere convalidati, vengono conteggiati separatamente e non possono fornire una conclusione positiva.

Un timestamp utilizzabile deve soddisfare tutti questi controlli: la sua impronta corrisponde al checkpoint, la sua firma è concatenata a una radice TSA attendibile al momento della marcatura, e la firma, la chiave, il conteggio e l’intestazione del checkpoint corrispondono esattamente al prefisso del giornale. La semplice analisi di un timestamp o il possesso di una ricevuta OTS non sono sufficienti. Il lettore deve scegliere in modo indipendente la radice TSA attendibile e ripetere la verifica. OTS necessita di un proprio controllo di conferma Bitcoin.

| Stato del rapporto | Significato |
| --- | --- |
| Verificato durante l’esportazione | L’esportatore ha eseguito il controllo indicato; è comunque necessaria una ripetizione indipendente. |
| Registrato; revisione richiesta | L’osservazione sottostante o la dichiarazione dell’operatore viene registrata; non si tratta di una conferma indipendente. |
| Non incluso in questo testo | Il testo non presenta alcuna prova a sostegno di questa affermazione. Non afferma che non ne esistano altrove. |
| Non verificato in modo indipendente | Il rapporto non fornisce un risultato di verifica indipendente. |
| Incompleto o non disponibile | Manca del materiale o una verifica richiesta, oppure è incompleto o non è andato a buon fine. |

Esaminare ogni controllo separatamente, insieme alla copertura della raccolta registrata.

## Cosa deve preservare una configurazione robusta

1. Prima di procedere alla raccolta, conservare l’impronta digitale della chiave del raccoglitore tramite un canale affidabile separato. Confrontare tale riferimento con la chiave di firma dell’esportazione.
2. Mantenere i checkpoint con timestamp indipendenti e, ove utilizzato, un registro di controllo al di fuori del controllo amministrativo del Collector. Confrontarli con il registro esportato per verificarne i confini precedenti.
3. Acquisizione dei record: ambito, lacune, filtri, limiti e modifiche nella raccolta. Spiegare i periodi mancanti rilevanti per la richiesta effettiva, distinguendo chiaramente gli ID dei messaggi non osservati, gli avvisi di cancellazione e le ricontrolli non andati a buon fine.
4. Mantenere i file ZIP originali e i relativi hash. Registrare ogni detentore, trasferimento, data e scopo. Conservare insieme a essi le dichiarazioni attribuite agli operatori e le note relative al caso.
5. Per i messaggi vocali riservati, conservare e verificare in modo indipendente la citazione, la verifica, la catena di certificati Intel, le misurazioni, la fonte esatta e le condizioni di gestione delle chiavi. Conservare il risultato della verifica dell’attestazione insieme agli artefatti esaminati.

Consultare [l’ambito di verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#verification-scope) per i controlli relativi all’acquisizione, all’integrità dell’archivio, alla copertura temporale e alla copertura della raccolta in ciascuna modalità.

## Revisione da parte del destinatario

Utilizzare un'installazione affidabile di TgWitness e un'impronta digitale ottenuta in modo indipendente:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

Il file ZIP di prova deve provenire da una fonte indipendente e affidabile; mantenere anche la sua chiave e la sua provenienza. Conservare i comandi, la versione dello strumento, i risultati, gli hash degli input verificati e le domande irrisolte. La verifica del beacon è un controllo online separato; il renderer del report non contatta mai un servizio al solo scopo di visualizzare un report.

In caso di controversia su un messaggio specifico, citare il riferimento all’archivio, il file di riferimento autorevole e il riferimento al record, quindi descrivere l’intervallo di tempo pertinente, le lacune di copertura, la selezione e il materiale corroborante. Per una copia condivisa, esaminare anche la trasformazione registrata e i relativi riferimenti all’archivio di origine. I filtri privati e le mappature di identità non rientrano nella valutazione pubblica.

La verifica del PDF firmato rileva eventuali modifiche ai byte interessati. Conservare il file digitale originale e il risultato della verifica insieme a eventuali screenshot o copie cartacee di lettura.
