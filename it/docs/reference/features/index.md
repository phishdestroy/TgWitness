# Caratteristiche e limiti

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/features/

Cosa offre attualmente TgWitness, quali sono i limiti della piattaforma Telegram e quali aspetti rimangono da sviluppare in futuro.

Riferimento di progettazione: 26 ottobre 2026. Il caso d’uso principale riguarda i gruppi privati di Telegram e i canali accessibili agli account collegati. Il presente documento distingue tra comportamento implementato, limiti della piattaforma e attività future. Un elemento dell’architettura prevista non costituisce un’affermazione che la funzionalità esista già.

## Applicazione autonoma

TgWitness dispone di una propria procedura di installazione, di una directory dei dati e di un proprio ciclo di vita delle versioni. L’interfaccia web integrata gestisce la configurazione e la revisione; i record esportati possono essere utilizzati in modo indipendente.

L’operatore collega i propri account, sceglie le fonti visibili a ciascuno di essi e ottiene un registro delle osservazioni salvato. Il pannello mostra i contenuti, le modifiche salvate, la provenienza delle osservazioni e le lacune note. Un altro investigatore può verificare il materiale esportato.

Sono rilevanti quattro stati distinti: l’autorizzazione dell’account, l’accesso a una fonte, un collettore funzionante e la misura in cui viene accertata la completezza della consegna. Nessuno dei primi tre stati dimostra automaticamente il quarto. Un gruppo inattivo non è necessariamente un collettore non funzionante.

## Indagini condivise

Un amministratore può emettere [token di accesso](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/) limitati a spazi di lavoro e singole chat, con sette livelli di autorizzazione, restrizioni IP, scadenza, limiti di accesso e controllo delle sessioni. Un revisore con diritti di sola lettura può esaminare un caso senza ricevere l’autorizzazione di Telegram né la chiave del pannello principale. L’accesso limitato alle chat rimane separato dalle impostazioni a livello di account e dalle esportazioni complete del registro.

MTProxy automatica mantiene attive le rotte Telegram da quattro fonti pubbliche o da un catalogo gestito dall’operatore. [Le modalità IP](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/#ip-modes) determinano se, in caso di errore, sia necessario attendere un altro proxy o se sia possibile utilizzare una rotta diretta esplicitamente autorizzata. Le richieste HTTP esterne dispongono di una rotta separata e di un interruttore di disattivazione.

## Strumenti di archiviazione

[L'acquisizione della cronologia](https://phishdestroy.github.io/TgWitness/it/docs/reference/history/), [la ricerca e l'analisi degli archivi](https://phishdestroy.github.io/TgWitness/it/docs/reference/analysis/),[l'MCP in sola lettura](https://phishdestroy.github.io/TgWitness/it/docs/reference/mcp/), [l'OCR/trascrizione locale](https://phishdestroy.github.io/TgWitness/it/docs/reference/media-analysis/) e[i webhook in uscita](https://phishdestroy.github.io/TgWitness/it/docs/reference/webhooks/) sono inclusi in 0.7.1. I report analitici e il testo riconosciuto rimangono separati dagli eventi acquisiti.

## Elementi aggiuntivi opzionali

La configurazione quotidiana prevede: account → fonti → osservazione. **La sezione «Extra»** è una destinazione separata con un bot Telegram Witness e un'anteprima di acquisizione su GitHub. Ciascuna sezione indica la propria disponibilità e i requisiti prima di mostrare le impostazioni. Selezionando una scheda si aprono le istruzioni; ciò non comporta la registrazione né l'avvio di un servizio.

La configurazione del bot prevede tre passaggi: creare un accesso in sola lettura, scegliere le impostazioni di pubblicazione e avviare il bot sull’host di TgWitness. Le opzioni di rete e di pubblicazione, le connessioni esistenti e i comandi di verifica vengono resi disponibili su richiesta. La configurazione scaricata è distinta da un witness in esecuzione. Il cambio di opzioni aggiuntive conserva la bozza; le modifiche all’account e il blocco cancellano il token temporaneo e il modulo. La guida integrata include le istruzioni di avvio. [GitHub Actions cattura](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) l’avvio di un collector appuntato dal tuo fork, acquisisce una chat e produce un trasferimento crittografato con la provenienza del flusso di lavoro.

## Protocollo e fonti private

**MTProto è il protocollo di Telegram; Telethon è la libreria Python che TgWitness utilizza per comunicare tramite MTProto.** Non si tratta di metodi di connessione alternativi. La raccolta dati utilizza MTProto; il «witness» opzionale pubblica i controlli firmati tramite l’API del bot.

Ogni area di lavoro dispone di un proprio client autorizzato e di un flusso di aggiornamenti dell’account. TgWitness seleziona le osservazioni dalle fonti configurate ed effettua richieste esplicite separate per funzioni quali le istantanee della cronologia e il download di file multimediali.

Una fonte privata non necessita di un nome utente pubblico. Il tipo di peer Telegram e l’ID numerico costituiscono gli identificatori; i titoli e i nomi utente possono variare. L’accesso dipende dall’appartenenza e dalle autorizzazioni esistenti. TgWitness non si unisce automaticamente alle fonti né aggira l’approvazione di adesione. Un hash di accesso proveniente da un altro account non costituisce un token di accesso universale.

Il modello di raccolta deve tenere conto della cronologia nascosta precedente all’adesione, dei ruoli dei partecipanti e degli amministratori, della revoca delle sessioni, della rimozione o della modifica delle autorizzazioni, della migrazione da gruppo a supergruppo, degli argomenti e dei forum, delle discussioni collegate, delle identità dei canali e degli allegati non disponibili. Non tutte le combinazioni sono state verificate in tempo reale.

La visibilità della fonte viene verificata all’avvio del collettore. L’assenza di una fonte dal risultato del dialogo circoscritto indica **un accesso non confermato**, non una rimozione comprovata. Una fonte non disponibile non impedisce l’osservazione delle altre fonti accessibili. Non inserire mai link di invito o sessioni reali nei dati pubblici.

## Account multipli

Il pannello supporta un numero illimitato di **aree di lavoro**, ciascuna delle quali dispone di:

- Autorizzazione, archivio crittografato e percorso di connessione.
- Registro SQLite e identità di firma Ed25519.
- Fonti selezionate, coda dei media e impostazioni di acquisizione.
- Stato di monitoraggio, errori, punti di controllo ed esportazioni.

Il cambio dell’area di lavoro visualizzata non interrompe il funzionamento di un altro collettore. L’autorizzazione duplicata di un account tra diverse aree di lavoro viene rifiutata. Un registro già associato a un account Telegram non può essere riassegnato a un altro; è invece consentita la riconnessione dello stesso account. Ciò preserva l’identità dell’account e l’ambito relativo agli ID dei messaggi.

Non vi è un numero fisso né alcuna garanzia di throughput misurato. Gli spazi di lavoro condividono un processo Python e un ciclo di eventi. La realizzazione di worker separati per ogni account rimane un obiettivo futuro. Per l’isolamento dei processi attuale, si raccomanda di utilizzare installazioni, porte e directory di dati separate.

Assegnare a ciascun account le fonti a cui può accedere. Account diversi possono monitorare lo stesso gruppo, ma le loro osservazioni rimangono separate e conservano la propria origine. Due account su un unico dispositivo controllato da un operatore non costituiscono due testimoni indipendenti. Le esportazioni avvengono per area di lavoro; non è prevista l’esportazione di un pacchetto di casi unificato né di una cronologia globale di Telegram.

## Acquisizione e attribuzione

La sezione «Fonti» offre opzioni per singolo account relative a nuovi messaggi, modifiche, cancellazioni, reazioni e appartenenza ai gruppi. Le impostazioni predefinite conservano tutte le categorie oppure solo messaggi, modifiche e cancellazioni. La politica si applica ai gruppi selezionati dell’area di lavoro, rimane attiva anche dopo il riavvio ed è firmata con le modifiche prima e dopo. Le impostazioni predefinite conservano tutte le categorie. La disattivazione di una categoria non comporta la rimozione dei vecchi record; la sua riattivazione non ricostruisce gli eventi mancanti. I record operativi, gli altri eventi relativi ai servizi di gruppo e le istantanee esplicite della cronologia sono separati. Gli oggetti Telegram acquisiti possono conservare i metadati incorporati indipendentemente dalle opzioni di aggiornamento separato. Non sono ancora disponibili sostituzioni delle categorie a livello di gruppo.

| Materiale | Acquisito ora | Limiti |
| --- | --- | --- |
| Messaggio | Testo, ID dei partecipanti/messaggi, metadati del mittente, risposte e busta di aggiornamento originale | Il messaggio non presenta una firma Telegram verificabile pubblicamente |
| Modifica | Nuova versione rilevata ed eventuali versioni salvate in precedenza | Le modifiche apportate durante i periodi di inattività potrebbero andare perse; il mittente non è necessariamente colui che ha apportato la modifica |
| Cancellazione | Notifica ed eventuali contenuti acquisiti in precedenza | Di norma non viene indicato chi ha effettuato la cancellazione né l’ora esatta dell’azione |
| Cancellazione non circoscritta | Notifica originale a livello di account senza formulare ipotesi sul destinatario | La correlazione rigorosa con gli ID relativi agli account precedentemente salvati costituisce un obiettivo futuro |
| Reazione | Contatori forniti e identità recenti visibili | Per ottenere un elenco completo dei reattori disponibili sono necessarie ricerche separate; i canali potrebbero nascondere le identità |
| Iscrizione | Messaggi di servizio e aggiornamenti inviati ai partecipanti | La visibilità dipende dal ruolo e dal tipo di chat; la mancanza di eventi non implica l’assenza |
| Azioni dell’amministratore | Solo aggiornamenti rilevanti forniti | Non è implementato il polling separato del registro di amministrazione |
| Allegato | Descrizione della versione originale, byte scaricati/SHA-256 ed esiti dei tentativi | Un file cancellato potrebbe risultare irrecuperabile; la versione più recente non viene sostituita |
| Cronologia | Istantanea esplicita dei messaggi attualmente visibili | Non ricostruisce tutte le modifiche né i contenuti cancellati |
| Processo di raccolta | Avvio/arresto, heartbeat, errori, impostazioni, ambito di applicazione e ricevuta del programma | Autodichiarazione, non attestazione indipendente del processo |

Un’azione viene attribuita a una persona solo se la fonte indica effettivamente tale soggetto. In caso contrario, l’interfaccia segnala la mancanza di attribuzione. I nomi utente e i nomi propri sono attributi osservati, non prova di identità nel mondo reale.

## Capacità e limiti di Telegram

Non esiste un numero universale di chat che possano essere monitorate con qualità garantita. La capacità dipende dal picco di eventi al secondo, dal volume e dalle dimensioni degli allegati, dagli RPC aggiuntivi, dagli account attivi, dalla latenza del disco e dallo spazio libero, dalle condizioni di rete, dai limiti di Telegram, dal ritardo accettabile e dalla profondità della coda.

Telegram distingue la consegna passiva dal polling breve attivo. La sua documentazione sugli aggiornamenti descrive ulteriori chiamate `updates.getChannelDifference` per canali aperti e supergruppi e raccomanda un massimo di **dieci fonti sottoposte a polling breve simultaneo**. Non si tratta di un limite di dieci gruppi selezionati né di una garanzia di completezza.

| Modalità | Scopo | Stato |
| --- | --- | --- |
| Osservazione standard | Registrazione degli aggiornamenti ricevuti da fonti selezionate | Implementato |
| Osservazione prioritaria | Controlli aggiuntivi delle differenze per un insieme di fonti circoscritto | Non implementato in modalità utente |

Un polling arbitrario ad alta frequenza, che ignori FloodWait o ipotizzi una capacità lineare derivante da account aggiuntivi, non costituisce un modello di dimensionamento valido. I limiti predefiniti sono i primi 1.000 dialoghi elencati, fino a 500 messaggi per istantanea della cronologia, da 1 a 2.000 MiB per file raccolto in base al tipo e 4 GiB di contenuto ZIP firmato non compresso; ciascuno di questi valori è modificabile per ogni area di lavoro nella sezione **«Parametri**». Le esportazioni non hanno un limite fisso al numero di eventi. Il fallback del browser è limitato a 128 MiB per impostazione predefinita; la CLI di streaming presenta un limite di trasferimento configurabile, pari a 5 GiB per impostazione predefinita.

`tools/check_capacity.py` misura l’acquisizione e l’esportazione di dati sintetici a livello locale. I suoi risultati non costituiscono misurazioni delle consegne di Telegram né un conteggio garantito delle conversazioni reali. Si veda [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/) per la versione misurata e il carico di lavoro.

## Affidabilità e recupero

Le funzionalità implementate includono transazioni SQLite WAL/sincrone; scritture atomiche di messaggi e operazioni relative ai file multimediali; operazioni persistenti e ritardi di riprova; descrittori della versione originale; tentativi di riprova limitati; FloodWait persistente per i file multimediali; download di file multimediali al di fuori dell’ attesa di rete dell’evento di testo; esportazioni con prefisso stabile mentre proseguono le scritture successive; impostazioni atomiche e registrazioni di audit; mantenimento dell’autorizzazione operativa dopo un accesso di sostituzione non riuscito; isolamento di uno spazio di lavoro aggiuntivo danneggiato; tentativi espliciti di riconnnessione; segnalazione distinta della perdita di autorizzazione; e rilevamento delle modifiche in tempo reale tramite un orologio monotono.

I dati pts/qts/seq relativi agli account e ai canali vengono salvati e ripristinati dopo un riavvio, mentre le chat monitorate vengono ricontrollate periodicamente; si veda [il formato delle prove](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#durable-collection-and-process-receipts-02). Il salvataggio periodico della posizione non costituisce una conferma atomica e senza perdite dell’accettazione del registro.

All’inizio di ogni processo vengono registrati il punto di inizio precedente e il limite offline. La cronologia attuale non viene considerata come una riparazione delle lacune. La conservazione delle differenze di Telegram è limitata; `differenceTooLong` non è in grado di ricostruire tutti i contenuti scomparsi. Le lacune irrecuperabili devono rimanere esplicite anche qualora una successiva istantanea della cronologia riesca a essere acquisita.

## Modello probatorio

Ogni evento registra una sequenza, l’ora di osservazione locale in UTC, l’ora di origine (se fornita), il tipo, la fonte, l’autore (se specificato), il payload originale, l’hash precedente e la firma. Le osservazioni dei messaggi conservano inoltre l’account del collettore e il contesto di esecuzione.

La ricevuta di processo firmata contiene un ID di esecuzione casuale; le versioni delle dipendenze di TgWitness/Python/OS; i valori SHA-256 dei file sorgente e l’impronta digitale aggregata; l’account iniziale, l’ambito e le impostazioni; le letture UTC/monotone; e l’intestazione del registro precedente. Le modifiche alle impostazioni, l’avvio/arresto e gli errori vengono registrati nello stesso registro. I punti di controllo vengono conservati all’avvio, ogni cinque minuti durante il monitoraggio (intervallo modificabile) e al termine ordinato dell’operazione. Un punto di controllo locale conservato è in grado di rilevare un rollback a un prefisso del registro precedente.

| Meccanismo | Cosa stabilisce |
| --- | --- |
| File SHA-256 | I byte corrispondono a un digest noto |
| Catena di hash degli eventi | Registrazione dell’ordinamento/collegamento rispetto a un confine noto |
| Ed25519 | Firma con una chiave specifica |
| Punto di controllo gestito in modo indipendente | Il materiale successivo rispetta i limiti stabiliti |
| Analisi delle dimensioni del file di programma | Autodichiarazione del Collector relativa ai file misurati |
| Risposta valida e indipendente della TSA | Esistenza di determinati byte al momento TSA in base a presupposti di fiducia espliciti |

Sono implementate la preparazione delle richieste secondo lo standard RFC 3161 e la verifica delle risposte tramite OpenSSL. L’invio automatico non è implementato. Una richiesta o una firma locale recante l’ora del computer non costituisce un timestamp indipendente. Si veda [il file TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/timestamp/).

Un operatore che controlla il collettore e la chiave di firma può creare nuove osservazioni firmate. Le firme non attestano l’origine da Telegram, la veridicità né l’ ammissibilità legale automatica. Una custodia più rigorosa richiede un sistema indipendente di controllo e archiviazione temporale, controlli sull’accesso alle chiavi, registrazioni dei trasferimenti e verifica da parte di software affidabile.

## Esportazione, implementazione e consegna

Un file ZIP firmato contiene i file originali in formato JSONL, CSV, HTML, gli allegati conservati, gli hash, un manifesto firmato e uno strumento di verifica di facile utilizzo. Copre un unico spazio di lavoro e un prefisso fisso per l’intero registro. I filtri di ricerca del pannello non eliminano silenziosamente i record. Sono esclusi le chiavi segrete, i token e le sessioni di Telegram; le osservazioni originali possono comunque contenere informazioni personali e metadati di Telegram.

Conservare separatamente il digest ZIP, l’impronta digitale attendibile, il checkpoint, la ricevuta di elaborazione e il registro di trasferimento. Utilizzare un verificatore proveniente da un’installazione attendibile, anziché fidarsi del codice eseguibile solo perché presente nel file ZIP esaminato.

L’interfaccia browser viene fornita localmente senza Node.js, CDN o font esterni. Un unico token operatore controlla l’installazione. L’accesso remoto richiede HTTPS o un tunnel SSH. Vengono fornite definizioni native in Python e per container, con esempi di servizio nella cartella [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md); i controlli di piattaforma eseguiti sono elencati separatamente.

L’area di lavoro predefinita utilizza la radice dei dati; le aree di lavoro aggiuntive utilizzano `profiles/<id>/`. Il backup richiede l’arresto del processo e il set completo di dati e chiavi. I file ZIP contenenti le prove non costituiscono backup dell’applicazione. Per le informazioni riservate è possibile utilizzare una chiave master esterna per una nuova directory di dati; la crittografia del registro e dei file multimediali è garantita dal disco o dal volume dell’operatore. Si vedano i file [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/) e [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/operations/).

## Criteri di rilascio della versione stabile

Prima del rilascio di una versione stabile, specificare:

1. Gruppi privati reali, supergruppi, forum e canali con ruoli di membri/amministratori e cronologia nascosta/visibile, inclusi accesso/autenticazione a due fattori (2FA), revoca e perdita di accesso.
2. Modifiche, cancellazioni, reazioni, appartenenza e contenuti multimediali controllati rispetto ad azioni note.
3. Arresti anomali del processo o del server, guasti al disco o disco pieno, riferimenti a file scaduti, FloodWait, perdita di connessione di rete, file danneggiati e rollback del database.
4. Utilizzo prolungato di più account con ritardi misurati, code, memoria e spazio su disco, comprese sia fonti silenziose che rumorose.
5. Interruzione tra l’avanzamento dello stato MTProto e l’accettazione del registro.
6. Installazione pulita sulla matrice di sistemi operativi/container prevista e ripristino del backup verificato.
7. Analisi indipendente in materia di sicurezza, firme e affermazioni relative all’attribuzione e alle prove.

Il polling dei log di amministrazione, gli elenchi aggiuntivi di reattori, il polling prioritario, i worker separati e la crittografia a livello di applicazione rimangono attività da sviluppare in futuro. L’accesso ai pannelli con ambito limitato è descritto nella sezione [«Accesso e autorizzazioni](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/)». La versione 0.6 supporta il TData limitato a un singolo account e l’importazione di file di account descritti nel file [ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/). Si prega di consultare i termini dell’API di Telegram prima della pubblicazione. I riferimenti alla ricerca e i risultati relativi alla piattaforma sono riportati nel file [RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md).
