# Sicurezza e trattamento dei dati

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/security/

Modello di minaccia, modello di accesso, dati sensibili inattivi, esposizione di rete, importazione delle sessioni e modalità di segnalazione di una vulnerabilità.

Questa pagina descrive l’accesso, l’archiviazione e la protezione della rete in un’area di lavoro locale o su server. Per la raccolta su un GitHub Runner o in una macchina virtuale riservata Intel TDX, consultare le modalità [di verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#verification-scope), che aggiungono controlli sull’ambiente di raccolta. Le connessioni agli account, le notifiche, i timestamp, le copie fuori sede e i testimoni dispongono di impostazioni di instradamento specifiche.

| Area | In sintesi |
| --- | --- |
| Accesso | Chiave amministratore più accesso limitato ad account/chat, sette autorizzazioni e sessioni revocabili; localhost come impostazione predefinita |
| Segreti inattivi | La sessione, la coppia API, la chiave di firma e le impostazioni del proxy sono crittografate con Fernet |
| Messaggi e contenuti multimediali | Archiviazione in chiaro: si raccomanda l’uso della crittografia del disco e di permessi rigorosi |
| Integrità | Catena di hash SHA-256 e firma Ed25519 su ogni registrazione |
| Confine di fiducia locale | L’amministratore dell’host controlla l’area di lavoro e la relativa chiave di firma; i checkpoint indipendenti conservano i confini del registro precedente |

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

Le credenziali dell'API di Telegram, la chiave di sessione e quella di firma sono crittografate con Fernet. Per i messaggi e i file multimediali locali, la crittografia è garantita dal disco o dal volume dell'host; l'area di lavoro memorizza file ordinari. Le esportazioni possono utilizzare un file ZIP protetto da password con crittografia AES-256, mentre le copie esterne utilizzano la crittografia AES-256-GCM.

La chiave del vault è impostata di default sulla directory dei dati protetti. Utilizzare un file esterno contenente la chiave principale come indicato di seguito per conservarla separatamente. Su Unix, i nuovi file delle chiavi private utilizzano la modalità 0600 e le nuove directory dei dati utilizzano la modalità 0700; su Windows, impostare le ACL della directory per l’account di servizio e gli amministratori autorizzati. I permessi esistenti della directory vengono mantenuti.

### Chiave master esterna

Per una nuova directory dei dati, TGWITNESS_VAULT_KEY_FILE può fornire una chiave master casuale esterna. HKDF-SHA256 e un salt casuale separato generano una chiave Fernet diversa per ogni area di lavoro. Il file vault.external.json deve essere conservato per il ripristino. Chiavi master mancanti o errate causano un errore di chiusura. I vault locali esistenti non vengono migrati in modo silenzioso. Il pannello visualizza la modalità di archiviazione delle chiavi selezionata. La crittografia del disco protegge i file di messaggi e multimediali locali in entrambe le modalità; consultare le sezioni relative [alla connessione e alla protezione dei dati](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/) per i dettagli sulla configurazione.

## Proxy e percorsi di rete

La configurazione del proxy è crittografata nel vault. Le password e i segreti di MTProxy non vengono restituiti dall’API né registrati nei registri delle prove. Ogni area di lavoro sceglie il proprio percorso Telegram e una [modalità IP](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/#ip-modes).

**L'opzione "Nascondi l'indirizzo"** disabilita il fallback diretto su Telegram e richiede un proxy per le richieste HTTP esterne. La modalità fallback selezionata esplicitamente consente l'accesso diretto a Telegram dopo un certo ritardo; la modalità tunnel/VPN consente percorsi diretti. La scelta della modalità tunnel non comporta l'installazione né la verifica di una VPN. Queste impostazioni non controllano tutto il traffico del computer, i browser, i gestori di pacchetti o la risoluzione DNS dell'host proxy locale.

MTProxy gestisce esclusivamente il traffico Telegram. Le richieste esterne possono avvalersi di un proxy SOCKS5/HTTP separato, del percorso SOCKS5/HTTP dell’area di lavoro o di un percorso diretto autorizzato; in alternativa, possono essere disabilitate. Il witness indipendente dispone di proprie impostazioni di trasporto. La normale autenticazione SOCKS5/HTTP CONNECT non è crittografata dai protocolli proxy stessi. I segreti TLS falsi di MTProxy non sono ancora supportati.

## Accesso e importazione delle sessioni

I file .tgwitness-session convertiti contengono una chiave di autorizzazione in testo chiaro fino a quando non vengono caricati e archiviati nel vault. L’interfaccia CLI offline accetta schemi Telethon revisionati. L’importazione tramite pannello accetta inoltre Pyrogram SQLite, il moderno formato ZIP TData a account singolo e input JSON documentati. È autenticata, limitata a quattro file / 8 MiB, ed elabora i caricamenti in memoria senza estrazione dell’archivio né salvataggio dei file originali. Le credenziali normalizzate vengono restituite esclusivamente al browser autenticato richiedente; vengono salvate nel vault crittografato dopo l’autorizzazione riuscita su Telegram. Protegga i file originali e quelli convertiti ed eviti che client concorrenti clonino un’autorizzazione.

L’elaborazione dei dati verifica i checksum dei container, gli hash di decrittografia locali e le lunghezze delle strutture. Il codice di accesso locale fornito per la versione Desktop viene utilizzato in modo temporaneo e non viene memorizzato. Questo parser limitato non garantisce la compatibilità con tutte le versioni Desktop. Le immagini QR vengono generate localmente, contengono token di accesso a Telegram di breve durata e non vengono mai inviate a un servizio di rendering esterno. Il blocco del dispositivo, il cambio di area di lavoro, un nuovo accesso e le modifiche al percorso annullano i tentativi QR in sospeso. Il ricaricamento o la chiusura di una scheda potrebbero lasciare un tentativo in sospeso fino alla scadenza. Un accesso QR riuscito impone comunque il vincolo all’account. I corpi API standard rimangono limitati a 16 KiB; il percorso di importazione autenticato accetta fino a 12 MiB di JSON codificato, applicando separatamente il limite inferiore per il file decodificato.

I codici di accesso e le password di verifica in due passaggi di Telegram non vengono memorizzati in modo permanente. Lo stato del numero di telefono o dell’hash del codice viene mantenuto in memoria durante l’autorizzazione. Le sessioni di Telegram consentono l’accesso all’account; non caricare mai su GitHub una directory di dati, una sessione, un token, una chiave del vault o una chiave di firma privata.

## Registri e trasmissione

La risposta predefinita di convalida dell’API viene sostituita in modo da non riportare i valori delle credenziali. La registrazione degli accessi all’applicazione è disabilitata. Si raccomanda di non configurare un proxy inverso per registrare le intestazioni di autorizzazione o i corpi delle richieste. Il protocollo HTTP trasporta i token e le credenziali di accesso in chiaro: si raccomanda di utilizzare HTTPS o un tunnel SSH ogni volta che si esce da localhost.

## Limiti di integrità

I controlli di verifica locali verificano le firme dei record, la catena di hash, gli allegati e il manifesto di esportazione. L'amministratore detiene la chiave di firma locale e può creare un altro registro firmato; un checkpoint conservato in modo indipendente rileva la sostituzione del prefisso che copre. Conservare l'impronta digitale della chiave e i checkpoint presso il destinatario o un testimone indipendente.

Per una raccolta verificata in modo indipendente, scegliere [l’acquisizione](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) [tramite GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) o [la distribuzione](https://phishdestroy.github.io/TgWitness/it/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx) [tramite Intel TDX](https://phishdestroy.github.io/TgWitness/it/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). I relativi verificatori controllano la provenienza del flusso di lavoro o le misurazioni hardware oltre all’integrità dell’archivio. I timestamp opzionali e le copie crittografate fuori sede forniscono punti di riferimento temporali e copie recuperabili; il [formato delle prove](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#verification-scope) descrive i controlli per ciascuna modalità.

## Se sospetta un problema

Conservare la directory dei dati originale e utilizzare una copia separata per l’analisi. Segnalare la versione interessata, l’operazione e i passaggi riproducibili tramite la politica [di sicurezza](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), mantenendo riservati i dati dell’account e le credenziali.
