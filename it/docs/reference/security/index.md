# Sicurezza e trattamento dei dati

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/security/

Modello di minaccia, modello di accesso, dati sensibili inattivi, esposizione di rete, importazione delle sessioni e modalità di segnalazione di una vulnerabilità.

TgWitness funziona sul proprio computer o server. Le connessioni agli account, la gestione dell’elenco pubblico dei proxy e i servizi esterni opzionali sono soggetti a politiche di instradamento esplicite. Notifiche, timestamp, copie fuori sede e un testimone vengono configurati separatamente. Questa pagina elenca ciò che viene protetto, in che modo e ciò che è lasciato alla discrezione dell’operatore.

| Area | In sintesi |
| --- | --- |
| Accesso | Chiave amministratore più accesso limitato ad account/chat, sette autorizzazioni e sessioni revocabili; localhost come impostazione predefinita |
| Segreti inattivi | La sessione, la coppia API, la chiave di firma e le impostazioni del proxy sono crittografate con Fernet |
| Messaggi e contenuti multimediali | Archiviazione in chiaro: si raccomanda l’uso della crittografia del disco e di permessi rigorosi |
| Integrità | Catena di hash SHA-256 e firma Ed25519 su ogni registrazione |
| Non trattato | Un amministratore di sistema, un token di pannello trapelato, completezza dell’acquisizione |

Per le segnalazioni di vulnerabilità, si prega di consultare la [politica sulla sicurezza](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

## Modello di accesso

Il token del pannello principale garantisce il controllo completo. Ad altri utenti può essere concesso un [accesso limitato](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/): spazi di lavoro e chat selezionati, autorizzazioni, scadenza, restrizioni IP, limiti di accesso e sessioni revocabili. Un accesso limitato a una chat non consente di eseguire operazioni sull’intero spazio di lavoro, anche se l’autorizzazione corrispondente è selezionata. Gli spazi di lavoro condividono un processo e non isolano i dati dall’amministratore ospitante.

Il pannello è in ascolto su localhost per impostazione predefinita. L’accesso tramite browser scambia un token di accesso con una credenziale di sessione; il browser lo invia come token bearer. Esso viene conservato in sessionStorage anziché in un cookie di autenticazione. Il blocco o la disconnessione cancellano la sessione del browser. La chiusura del browser o la fine della sessione non interrompono la raccolta.

I token emessi e le credenziali di sessione vengono conservati sotto forma di hash nel deposito crittografato. La revoca pone fine alle sessioni associate; le modifiche alle autorizzazioni hanno effetto sulle successive richieste. I file scaricati non possono essere recuperati. L’amministratore può limitare anche le proprie sessioni del browser, ma gli script che utilizzano direttamente il token del pannello principale mantengono l’accesso completo e aggirano tali limiti delle sessioni del browser.

L’autenticazione non riuscita è soggetta a limitazioni di frequenza in base all’indirizzo del client. Le restrizioni IP utilizzano l’ indirizzo rilevato dall’applicazione; si raccomanda di verificare il comportamento del reverse proxy prima di fare affidamento su di esso. Le credenziali di Witness rimangono credenziali separate, di sola lettura, relative a checkpoint e integrità del sistema.

### Accesso alla demo

`/api/demo-access` è un bootstrap volutamente non autenticato per una demo sintetica isolata e avviata in modo esplicito. Emette una funzionalità separata valida per la durata del processo, mai il token del pannello reale né un override di TGWITNESS_TOKEN. L’emissione e l’utilizzo richiedono un peer di loopback e un host, senza intestazioni inoltrate né richieste cross-origin. Ulteriori spazi di lavoro o una sessione autorizzata disabilitano questo percorso. Gli spazi di lavoro attivi non emettono mai tale capacità. La demo non può collegare account né modificare le impostazioni di raccolta.

## Contenuti dei pannelli ed esportazioni

Il pannello non utilizza font esterni, strumenti di analisi, risorse CDN né contenuti multimediali remoti incorporati. Il testo proveniente da Telegram viene inserito come testo, non come HTML. Gli allegati scaricati vengono forniti come allegati binari. Le esportazioni in formato JSONL conservano le stringhe originali; l’HTML le sostituisce con caratteri di escape; alle celle CSV che potrebbero diventare formule viene anteposto un apostrofo.

Le esportazioni escludono i segreti di autenticazione e firma, ma contengono deliberatamente i metadati di origine raccolti, gli identificatori ed eventualmente contenuti personali o sensibili. Nei metadati di origine non elaborati possono essere presenti hash di accesso a Telegram e riferimenti ai file.

## Segreti inattivi

Le credenziali dell’API di Telegram, StringSession e la chiave privata Ed25519 vengono crittografate utilizzando Fernet. Per impostazione predefinita, la chiave viene memorizzata nella stessa directory dei dati protetti. Ciò riduce il rischio di esposizione accidentale in chiaro; non costituisce tuttavia una protezione contro un malintenzionato in grado di leggere l’intera directory. Il contenuto dei messaggi e i file multimediali **non** vengono **crittografati** da TgWitness. Si raccomanda di utilizzare la crittografia del disco e permessi restrittivi del sistema operativo. I file delle chiavi private Unix vengono creati con modalità 0600; le directory di dati di nuova creazione utilizzano la modalità 0700. I permessi delle directory esistenti non vengono modificati. Windows eredita gli ACL delle directory: li limiti all’account di servizio e agli amministratori autorizzati.

### Chiave master esterna

Per una nuova directory dei dati, TGWITNESS_VAULT_KEY_FILE può fornire una chiave principale casuale esterna. HKDF-SHA256 e un salt casuale separato generano una chiave Fernet diversa per ogni area di lavoro. Il file vault.external.json deve essere conservato ai fini del ripristino. Chiavi master mancanti o errate comportano un errore di chiusura. I vault locali esistenti non vengono migrati in modo silenzioso. Il processo in esecuzione può accedere alla chiave; non si tratta di isolamento HSM. Il pannello riporta la modalità selezionata e dichiara esplicitamente che l’archiviazione di messaggi e file multimediali non è crittografata dall’applicazione. Si vedano le sezioni relative a [connessione, proxy e protezione dei dati](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/) per il modello di minaccia completo.

## Proxy e percorsi di rete

La configurazione del proxy è crittografata nel vault. Le password e i segreti di MTProxy non vengono restituiti dall’API né registrati nei registri delle prove. Ogni area di lavoro sceglie il proprio percorso Telegram e una [modalità IP](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/#ip-modes).

La modalità «Nascondi IP» disabilita il fallback diretto di Telegram e richiede un proxy per le richieste HTTP esterne. La modalità «Fallback» selezionata esplicitamente consente l’accesso diretto a Telegram dopo un certo ritardo; la modalità «Tunnel/VPN» consente percorsi diretti. La scelta della modalità tunnel non comporta l’installazione né la verifica di una VPN. Queste impostazioni non controllano l’intero traffico del dispositivo, i browser, i gestori di pacchetti o la risoluzione DNS dell’host proxy locale.

MTProxy gestisce esclusivamente il traffico Telegram. Le richieste esterne possono avvalersi di un proxy SOCKS5/HTTP separato, del percorso SOCKS5/HTTP dell’area di lavoro o di un percorso diretto autorizzato; in alternativa, possono essere disabilitate. Il witness indipendente dispone di proprie impostazioni di trasporto. La normale autenticazione SOCKS5/HTTP CONNECT non è crittografata dai protocolli proxy stessi. I segreti TLS falsi di MTProxy non sono ancora supportati.

## Accesso e importazione delle sessioni

I file .tgwitness-session convertiti contengono una chiave di autorizzazione in testo chiaro fino a quando non vengono caricati e archiviati nel vault. L’interfaccia CLI offline accetta schemi Telethon revisionati. L’importazione tramite pannello accetta inoltre Pyrogram SQLite, il moderno formato ZIP TData a account singolo e input JSON documentati. È autenticata, limitata a quattro file / 8 MiB, ed elabora i caricamenti in memoria senza estrazione dell’archivio né salvataggio dei file originali. Le credenziali normalizzate vengono restituite esclusivamente al browser autenticato richiedente; vengono salvate nel vault crittografato dopo l’autorizzazione riuscita su Telegram. Protegga i file originali e quelli convertiti ed eviti che client concorrenti clonino un’autorizzazione.

L’elaborazione dei dati verifica i checksum dei container, gli hash di decrittografia locali e le lunghezze delle strutture. Il codice di accesso locale fornito per la versione Desktop viene utilizzato in modo temporaneo e non viene memorizzato. Questo parser limitato non garantisce la compatibilità con tutte le versioni Desktop. Le immagini QR vengono generate localmente, contengono token di accesso a Telegram di breve durata e non vengono mai inviate a un servizio di rendering esterno. Il blocco del dispositivo, il cambio di area di lavoro, un nuovo accesso e le modifiche al percorso annullano i tentativi QR in sospeso. Il ricaricamento o la chiusura di una scheda potrebbero lasciare un tentativo in sospeso fino alla scadenza. Un accesso QR riuscito impone comunque il vincolo all’account. I corpi API standard rimangono limitati a 16 KiB; il percorso di importazione autenticato accetta fino a 12 MiB di JSON codificato, applicando separatamente il limite inferiore per il file decodificato.

I codici di accesso e le password di verifica in due passaggi di Telegram non vengono memorizzati in modo permanente. Lo stato del numero di telefono o dell’hash del codice viene mantenuto in memoria durante l’autorizzazione. Le sessioni di Telegram consentono l’accesso all’account; non caricare mai su GitHub una directory di dati, una sessione, un token, una chiave del vault o una chiave di firma privata.

## Registri e trasmissione

La risposta predefinita di convalida dell’API viene sostituita in modo da non riportare i valori delle credenziali. La registrazione degli accessi all’applicazione è disabilitata. Si raccomanda di non configurare un proxy inverso per registrare le intestazioni di autorizzazione o i corpi delle richieste. Il protocollo HTTP trasporta i token e le credenziali di accesso in chiaro: si raccomanda di utilizzare HTTPS o un tunnel SSH ogni volta che si esce da localhost.

## Limiti di integrità

La catena di hash, i trigger del database e le firme rilevano determinate modifiche; non impediscono tuttavia a un amministratore locale di riscrivere e firmare nuovamente il registro. Conservare i checkpoint firmati e l’impronta digitale della chiave pubblica su un sistema separato. La modalità «evidenza» e la copia off-site (entrambe disattivate per impostazione predefinita) inviano gli hash dei checkpoint a servizi di marcatura temporale e copie crittografate a un archivio compatibile con S3; si veda il [formato delle prove](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/). I registri di trasparenza, la firma supportata da HSM e la certificazione formale della catena di custodia non sono implementati.

## Se sospetta un problema

Conservare la directory dei dati originale e utilizzare una copia separata per l’analisi. Non includere dati privati di Telegram o credenziali in una segnalazione pubblica. Non viene rivendicata alcuna certificazione di sicurezza indipendente.
