# Architettura

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/architecture/

Componenti del collettore, del pannello, del registro, dei worker e di Witness, e modalità di trasferimento dei dati tra di essi.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Sviluppo](https://phishdestroy.github.io/TgWitness/assets/chapter-develop.svg)

Un unico processo Python ospita il pannello FastAPI e un numero illimitato di aree di lavoro isolate, ciascuna dotata di un client con account utente Telethon. SQLite contiene un registro degli eventi firmato, in cui è possibile solo l’aggiunta di dati, e impostazioni operative modificabili. Un archivio crittografato contiene le credenziali API, la StringSession e la chiave di firma. Il frontend è costituito da un semplice pacchetto HTML/CSS/JavaScript: non sono necessari build Node, CDN né download del frontend in fase di esecuzione.

Optional browser and AyuGram recorders run in **separate processes or containers**. The `tgwitness_capture` package owns their event format, keys, artifacts, checkpoint API, independent witness and standalone verifier. It is bundled in the main wheel and can also be installed alone from `addons/capture`, without importing the collector. The main panel's `capture_api.py` and `capture_connections.py` provide administrator-only, workspace-scoped controls under `/api/capture`; connection tokens live in the encrypted vault. No recorder or outbound request starts with the main process. Each explicit command verifies a fresh challenge against the pinned recorder key. Exports are verified before download and keep their original signature; they do not become Telegram message events. Collection sessions and proxy routes stay with each client. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md) for deployment and trust boundaries.

| Modulo | Responsabilità |
| --- | --- |
| collector.py | Autorizzazione, selezione delle finestre di dialogo, aggiornamenti, istantanee, coda dei file multimediali, monitoraggio della connessione |
| interactions.py / telegram_client.py | Azioni esplicite del pannello, ricevute firmate, ID richiesta persistenti e politica di riprova per callback/join a livello di attività |
| message_content.py | Confronto dei messaggi osservabili, esclusi i metadati relativi all’accesso di trasporto |
| workers.py | Attendere il completamento delle operazioni di esportazione dei file prima di procedere alla pulizia post-cancellazione |
| distributed_export.py / distributed_pages.py | Processi di chat simultanei, riserve per account, checkpoint firmati e pulizia dopo la verifica dell’archivio |
| distributed_takeout.py / export_timing.py | Sessioni Takeout riprendibili e tempi relativi a ogni avvio o ripresa |
| store.py | Transazioni WAL, catena di eventi ordinata, filtri di query, impostazioni operative |
| fulltext.py | Indice full-text derivato (forme lessicali, BM25), associato all’intestazione del registro firmato; mai esportato |
| security.py | Creazione di file privati, archivio crittografato, firma Ed25519, blocco a processo singolo |
| evidence.py | Esportazione completa del registro, derivati, punti di controllo, verifica degli allegati |
| verify.py | Verificatore autonomo e di sola lettura (stdlib + crittografia): archivi, copertura, registri di testimonianza e post dei canali, file di profilo |
| app.py | API autenticata, ciclo di vita, convalida delle richieste, pannello statico |
| profiles.py | Raccoglitori di account multipli, controller di accesso condiviso, ciclo di vita per ogni area di lavoro |
| access.py | Concessioni limitate, controlli delle autorizzazioni, restrizioni IP, limiti di sessione e console di amministrazione |
| proxy_catalog.py | Istantanee dei feed pubblici, controlli sul trasporto, pool di proxy condiviso e selezione basata sullo stato di integrità |
| provenance.py | Identità firmata dell’esecuzione di acquisizione, misurazioni del codice e delle dipendenze |
| network.py | Percorsi convalidati per ogni area di lavoro; stato e prove oscurati; opzioni di trasferimento Telethon |
| sessions.py | Conversione offline in sola lettura degli schemi SQLite di Telethon sottoposti a revisione |
| account_import.py | Rilevamento e normalizzazione in memoria dei file degli account supportati e dei file JSON |
| tdata.py | Lettore ZIP TData moderno e limitato, verifica del checksum e della decrittografia, nessuna estrazione |
| doctor.py | Verifiche di idoneità locali senza raccolta di dati, accesso o installazione di pacchetti |
| download.py | Esportazione in streaming autenticata con lettura limitata e senza sovrascritture |
| monitoring.py | Politica sugli eventi convalidata per ogni area di lavoro e regole relative agli allegati per tipo, condivise tra gli addetti, lo stato e le ricevute firmate |
| scope.py | Ambito di monitoraggio (chat selezionate, cartella Telegram, intero account), tipi di fonti, esclusioni, livelli di ricontrollo |
| dossier.py | Profili degli utenti per ogni chat ricavati dai registri salvati: dati con riferimenti ai registri, SHA-256/pHash degli avatar, estrazione delle menzioni |
| witness_api.py | Token di testimonianza in sola lettura e l’intestazione del registro firmato che essi possono recuperare |
| witness.py | Processo di testimonianza indipendente: chiave e registro propri, controlli di integrità, post del canale firmati, esportazione |
| alerts.py | Notifiche di Apprise e l’elenco delle notifiche del pannello |
| logging_config.py | Registrazione dei log della console e diagnostica a rotazione del server per l’avvio senza interfaccia grafica |
| static/ | Interfaccia reattiva, porta di accesso locale, filtri, dettagli, esportazioni, configurazione dell’account |
| demo.py | Registro sintetico chiaramente identificato come tale, separato dalla raccolta reale |

I gestori di osservazione vengono registrati prima della connessione. La raccolta in tempo reale è regolata dall’ identità del client attivo, dallo stato di esecuzione esplicito, dalle fonti abilitate o dall’ambito di osservazione (le modalità «cartella» o «intero account» aggiungono una nuova chat come fonte al suo primo aggiornamento) e dalla politica relativa agli eventi. I client rifiutati o sostituiti non possono fornire aggiornamenti in tempo reale. Le reazioni grezze e gli aggiornamenti relativi all’appartenenza rispettano i limiti di visibilità. Il contenuto del messaggio in arrivo e il relativo processo multimediale permanente vengono registrati congiuntamente. I processi conservano il descrittore TL originale e associano il suo hash all’ osservazione del messaggio firmata. Le semantiche relative a mittente, modificatore ed eliminatore sono separate.

Ogni area di lavoro accetta un solo account e dispone di una propria directory e di una propria identità di firma. L’area di lavoro principale rimane nella directory radice per motivi di compatibilità; le aree di lavoro aggiuntive risiedono in profiles/<id>/. Un unico token bearer controlla l’intera installazione; le aree di lavoro non costituiscono entità di autorizzazione separate. I blocchi di processo proteggono le directory; i blocchi del database serializzano l’inserimento degli eventi. Ogni aggiunta viene registrata in modo sincrono nel WAL di SQLite con modalità sincrona FULL. I trigger di aggiornamento/cancellazione degli eventi impediscono le normali modifiche da parte delle applicazioni; gli amministratori del filesystem rimangono all’interno del perimetro di fiducia.

L’autorizzazione API è un token bearer. Le operazioni di accesso sono serializzate e limitate nel tempo. I caricamenti degli account utilizzano un limite dedicato di 12 MiB per il corpo codificato e un limite di 8 MiB per il file decodificato ; le normali richieste API mantengono il limite di 16 KiB. La conversione viene eseguita in un thread di lavoro, mantiene i caricamenti in memoria e restituisce l’input normalizzato al browser autenticato. L’accesso tramite QR prevede un candidato per ogni spazio di lavoro, un identificatore di breve durata, un’attività di attesa e una cancellazione esplicita. Solo l’autorizzazione accettata diventa il client attivo. Telegram FloodWait viene restituito con un valore Retry-After; le credenziali e i messaggi di errore RPC grezzi non vengono esposti negli errori API. Le esportazioni del journal vengono eseguite al di fuori del ciclo di eventi asincrono e sono serializzate per spazio di lavoro. Trasmettono in streaming un’istantanea di lettura stabile parallelamente alle continue scritture WAL. I processi di acquisizione delle chat possono essere eseguiti in modo concorrente su account separati; ogni account rimane riservato fino al termine del proprio processo. Un processo messo in pausa o fallito conserva i propri checkpoint. La verifica riuscita dell’archivio consente la pulizia dei file di lavoro, lasciando il file ZIP, il piano firmato e lo stato. I collettori degli spazi di lavoro condividono il processo/ciclo di eventi.

Le istantanee della cronologia attuale e gli aggiornamenti in tempo reale possono sovrapporsi. Entrambe costituiscono osservazioni distinte, contrassegnate dalla fonte; i duplicati non vengono nascosti automaticamente. Non vengono effettuate inferenze basate su ID mancanti, testo cancellato inventato, enumerazione forzata dei membri o adesione automatica ai gruppi. Non viene implementata alcuna di queste funzionalità.

Per le spiegazioni rivolte agli operatori, si veda [come funziona la raccolta](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/) nonché [gli account e i formati delle sessioni](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/).

La configurazione di rete risiede nel vault crittografato. L’applicazione di un percorso chiude i vecchi client e annulla gli accessi non completati; le connessioni successive utilizzano tale percorso senza alcun fallback diretto. Una nuova installazione con chiave esterna ricava la chiave Fernet di ciascun spazio di lavoro utilizzando HKDF-SHA256 a partire da un file di chiave master e da un salt casuale memorizzato. Ciò protegge le informazioni riservate separatamente dalla directory dei dati, non i contenuti in chiaro del registro o dei file multimediali.

L’accesso alla demo locale utilizza una capacità di processo generata separatamente, mai il token del pannello configurato. L’emissione e l’accettazione richiedono la modalità demo esplicita, una radice sintetica senza spazi di lavoro aggiuntivi o una sessione autorizzata, peer/host in loopback, assenza di intestazioni di inoltro proxy e nessuna richiesta del browser cross-origin. Le API live mantengono l’autenticazione del portatore e rifiutano le modifiche alla raccolta in modalità demo.
