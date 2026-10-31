# Connessione, proxy e protezione dei dati

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/

Autenticazione, pool di proxy automatici, modalità IP, politica di fallback, richieste esterne e archiviazione dei dati riservati.

Il presente documento descrive il funzionamento di TgWitness 0.7.0 e i suoi limiti. L’autenticazione, l’accesso alla fonte, la connettività di rete e la completezza dell’acquisizione costituiscono stati distinti. Per le procedure di accesso, i formati dei file e la gestione di più account, si prega di consultare la sezione relativa [agli account e ai formati di sessione](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/). Per le politiche relative agli eventi e il comportamento in caso di riavvio, si prega di consultare [la sezione dedicata al funzionamento della raccolta](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/).

## Metodi di autenticazione

**L’ID API e l’hash API identificano un’applicazione; non sostituiscono le credenziali di accesso all’account.** In TgWitness sono facoltativi. Ordine di priorità: una coppia inserita nel modulo, poi una proveniente da un file JSON di un account importato, quindi la coppia salvata nell’area di lavoro, infine il pool integrato di 50 coppie pubbliche, provate in ordine casuale con rotazione automatica quando Telegram ne rifiuta una. Solo la coppia di Telegram Desktop (2040) viene inviata con una descrizione corrispondente del client Telegram Desktop. La propria coppia ottenuta dagli Strumenti di sviluppo API su [my.telegram.org](https://my.telegram.org) può essere utilizzata con tutti i propri account; ogni account mantiene comunque la propria autorizzazione.

| Metodo | Requisiti | Assistenza TgWitness |
| --- | --- | --- |
| Numero di telefono, codice, autenticazione a due fattori (2FA) facoltativa | Accesso all’account; coppia API facoltativa | Accesso al pannello di controllo |
| Chiave di autenticazione HEX + ID DC | Chiave completa da 512 caratteri e DC 1–5 | Scheda **«Chiave di autenticazione** diretta»; l’ID utente opzionale viene verificato prima che l’autorizzazione venga salvata |
| Telethon StringSession | Una stringa di sessione valida | Accesso al pannello di controllo |
| Telethon SQLite `.session` | Testo completo e coerente | Importazione diretta degli schemi tramite pannello 7/8; CLI offline opzionale |
| Pyrogram SQLite `.session` | Sessione utente di produzione chiusa | Importazione diretta degli schemi tramite pannello 2/3 |
| Telegram Desktop TData ZIP | Un unico account moderno; codice di accesso locale, se protetto | Conversione in memoria con controlli di checksum e decrittografia |
| Account JSON | Campi API/sessione/chiave supportati | I metadati da soli non sono sufficienti per compilare le credenziali API; è comunque necessario un accesso tramite sessione/chiave o numero di telefono/codice QR |
| Accesso tramite codice QR | Conferma da parte di un’app Telegram autorizzata | Generazione locale di codici QR, scadenza/riprova, autenticazione a due fattori (2FA) opzionale |
| TDLib / Pyrogram StringSession | Altri formati specifici per le librerie | Non supportato |
| Token del bot | Un bot dotato di un proprio modello di accesso e aggiornamento | Non utilizzato da questo raccoglitore |

Telegram opta per l’invio tramite codice; la consegna tramite SMS non è garantita. Un hash API non può ripristinare una sessione revocata né sostituire una password 2FA dimenticata. TgWitness non memorizza i codici di accesso né la password 2FA di Telegram su disco.

Per una fonte privata, l’account deve già disporre dell’accesso. Il nome utente di un gruppo non è necessario. Un proxy o un’importazione di sessione non conferisce né l’appartenenza al gruppo né i diritti di amministratore. L’appartenenza attuale non garantisce l’accesso alla cronologia precedente all’adesione.

## Importare un file di sessione di Telethon

Telethon SQLite, Pyrogram SQLite e Telegram Desktop TData utilizzano formati diversi. Il pannello rileva e converte le strutture supportate; la ridenominazione di un file non costituisce una conversione. Selezionate una sessione e il relativo file JSON in corrispondenza della voce **«File**», quindi premete **«Collega account**». Sono accettati fino a quattro file corrispondenti e un totale di 8 MiB. Consultare [i limiti di formato](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/) per i dettagli su TData/JSON. Non è previsto il recupero del codice di accesso. L’accesso tramite telefono/2FA o codice QR crea un’autorizzazione separata.

Il percorso opzionale della riga di comando, riservato esclusivamente a Telethon, rimane disponibile:

1. Chiuda la sessione del client originale e crei una copia coerente. Il convertitore rifiuta i file con un WAL/registro incompleto. Chiuda il client originale in modo corretto, anziché eliminare tali file per aggirare il controllo.
2. Dall’ambiente TgWitness, esegua:

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. In **«Aggiungi account» → «File»**, carichi il risultato oppure incolli la stringa corrispondente e prosegua.
2. Verifichi l’ID numerico dell’account visualizzato, selezioni le fonti e avvii il monitoraggio.

Il convertitore apre SQLite in modalità di sola lettura, non esegue alcun aggiornamento dello schema né richieste di rete, e non stampa la sessione. Verifica la versione dello schema, i tipi di tabella, una singola riga della sessione, IP/porta/DC e la lunghezza della chiave. L’input della CLI è limitato a 64 MiB; il testo di StringSession è limitato a 4 KiB. La conversione tramite pannello carica i file sul server TgWitness autenticato, li elabora in memoria e restituisce le credenziali normalizzate a quel browser senza salvare gli originali caricati. Utilizzi HTTPS per un server remoto.

**Il file convertito costituisce una chiave di accesso all’account non crittografata.** Conservatelo in un archivio protetto e non inseritelo mai nel codice né inviatelo a un servizio di conversione di terze parti. TgWitness salva la sessione autorizzata nel proprio archivio crittografato. La copia di una sessione non crea un’autorizzazione separata: non eseguite client simultanei con chiavi di autenticazione clonate e non date per scontata la consegna indipendente degli aggiornamenti.

La conversione trasferisce l’autorizzazione, non i messaggi originali, la cache dell’entità o un cursore di aggiornamento permanente. Non garantisce il recupero degli aggiornamenti in caso di riavvio del processo.

## MTProto, Telethon e proxy

MTProto è il protocollo di Telegram. Telethon è la libreria client Python utilizzata da TgWitness. MTProxy è un proxy di trasporto per Telegram; SOCKS5 e HTTP CONNECT forniscono tunnel generici. Nessuno di essi sostituisce l’autenticazione dell’account.

Salvi il percorso per ciascun spazio di lavoro in **Account → Impostazioni → Impostazioni di connessione → Modifica percorso di connessione** prima di effettuare l’accesso. Per i nuovi spazi di lavoro, l’impostazione predefinita è **MTProxy automatico · elenchi pubblici** con comportamento «Nascondi IP». Gli spazi di lavoro esistenti che utilizzavano esplicitamente la modalità Diretta mantengono una modalità che lo consenta.

## Modalità IP

È il percorso a determinare la connessione. La modalità IP stabilisce quando l’indirizzo del server può essere reso visibile. Questi controlli non installano una VPN né instradano tutto il traffico del dispositivo.

| Modalità | Telegram | Richieste esterne |
| --- | --- | --- |
| Hide IP (`hide`) | Utilizzi un proxy; attenda se nessuno funziona. Nessuna soluzione alternativa diretta. | Richiede SOCKS5/HTTP; respinge le richieste prive di un proxy idoneo. |
| Consentire l’alternativa (`fallback`) | MTProxy automatico può utilizzare Direct dopo il ritardo configurato, per poi tornare a un proxy funzionante. | Si preferisce l’utilizzo di un proxy esterno configurato o del percorso SOCKS5/HTTP dell’account; in alternativa, è consentito l’accesso diretto. |
| Tunnel / VPN (`tunnel`) | Sono consentiti percorsi diretti e il ricorso immediato al pool automatico di riserva. | L’accesso diretto è consentito qualora non sia configurato alcun proxy applicabile. |

La modalità Tunnel/VPN presuppone che gestiate tale rete separatamente. In assenza di un tunnel funzionante, i destinatari possono visualizzare l’indirizzo del server stesso. Selezionate la modalità in base alla vostra rete effettiva, non al nome dell’opzione.

### Scegliete un percorso

| Percorso | Impostazioni | Limiti |
| --- | --- | --- |
| MTProxy automatico | Elenchi integrati o un catalogo di operatori | Mantiene un percorso Telegram funzionante; il fallback diretto dipende dalla modalità IP |
| Diretto | Modalità Tunnel/VPN | Telethon utilizza il percorso di rete del conduttore |
| SOCKS5 | Host, porta, nome utente/password (facoltativi) | python-socks, DNS di destinazione remota abilitato |
| HTTP CONNECT | Host, porta, nome utente/password (facoltativi) | CONNECT HTTP semplice; il protocollo TLS verso il proxy stesso non è implementato |
| MTProxy | Host, porta, chiave segreta | Trasporto sperimentale Telethon; 32 cifre esadecimali oppure `dd` + 32 cifre esadecimali |

I segreti TLS falsi di tipo `ee` vengono rifiutati. La normalizzazione di Telethon 1.45 può rimuovere un prefisso e un dominio, ma ciò non implementa il Fake TLS. Incollate `tg://proxy?server=…&port=…&secret=…` o `https://t.me/proxy?server=…&port=…&secret=…` e selezionate **«Compila campi dal link**». In questo modo i campi vengono convalidati e compilati senza effettuare alcuna connessione né salvare i dati; si prega di verificare e salvare il percorso separatamente. I campi manuali rimangono disponibili. Si vedano [i link proxy di Telegram](https://core.telegram.org/api/links#proxy-links).

### Proxy pubblici forniti dalla vostra installazione

L’elenco integrato combina quattro fonti: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) e [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). L’istantanea inclusa nel pacchetto contiene i dati relativi agli endpoint, l’attribuzione delle fonti e le date di download. La presenza di un provider nell’elenco non costituisce prova del funzionamento del proxy né della trasmissione di tutti gli aggiornamenti di Telegram.

**MTProxy** verifica **automaticamente** la connettività di trasporto di Telegram, mantiene attivo un proxy funzionante e passa a un altro in caso di malfunzionamento. Gli spazi di lavoro preferiscono proxy diversi quando sono disponibili voci funzionanti in numero sufficiente; non è garantito un indirizzo di uscita univoco. I proxy non funzionanti rimangono inattivi prima di un nuovo tentativo. Se nessuno funziona, la modalità IP determina se la raccolta deve attendere o se è possibile utilizzare una connessione diretta. Il cambio di proxy non modifica l’account né cancella il relativo registro. Le scelte e le modifiche relative al percorso vengono registrate nel registro firmato.

Quando i percorsi automatici sono attivi, gli elenchi vengono aggiornati ogni ora e i controlli di trasmissione vengono eseguiti ogni dieci minuti per impostazione predefinita. Tali intervalli sono configurabili. **L’aggiornamento degli elenchi pubblici** richiede un refresh; la semplice visualizzazione dell’elenco non modifica un percorso manuale salvato.

Ogni risposta del feed è limitata a 1 MiB, con un timeout di richiesta di otto secondi e un limite massimo di 20 secondi per il download complessivo; i reindirizzamenti vengono respinti. Per ogni fonte vengono conservate e deduplicate fino a 64 voci compatibili. Il parser accetta i segreti esadecimali e in formato base64url supportati, nonché il feed JSON. I falsi certificati TLS «`ee`», i collegamenti non validi, i valori IP privati/riservati e i nomi host locali vengono ignorati. I nomi host vengono risolti e verificati prima dell’uso, e l’IP scelto viene fissato per quella connessione. La riacquisizione automatica risolve nuovamente un nome host; per risolverlo nuovamente, si deve riapplicare una voce inserita manualmente.

Le risposte del feed non riuscite, vuote o incompatibili mantengono l’istantanea della fonte precedente. Gli aggiornamenti sono atomici, serializzati e limitati a un tentativo al minuto per ogni area di lavoro. Il superamento con successo del test di trasporto stabilisce la connettività, non l’anonimato né la completezza dell’acquisizione.

**Il traffico Telegram e le richieste HTTPS utilizzano percorsi diversi.** I download degli elenchi utilizzano una connessione HTTPS separata e il percorso di richiesta esterna fornito. Il `TGWITNESS_PROXY_FEED_PROXY` sovrascrive esplicitamente tale percorso con un proxy HTTP/SOCKS5; entrambe le varianti del collector Compose lo inoltrano. Il pool in background segue l’area di lavoro principale. Nessuna sessione Telegram, nessuna credenziale API, nessun token del pannello né token del bot viene inviato ai fornitori di feed. I nomi dei fornitori, le date degli snapshot e il percorso di download compaiono nella sezione **«Da dove proviene l’elenco**».

Un MTProxy trasporta esclusivamente il traffico di Telegram. Le operazioni HTTP dell’area di lavoro, quali timestamp, notifiche, copie fuori sede e verifiche delle fonti, utilizzano un proxy SOCKS5/HTTP separato, se configurato, oppure il percorso SOCKS5/HTTP dell’account. In assenza di entrambi, Hide IP rifiuta la richiesta; le altre modalità consentono l’accesso diretto. Le richieste esterne possono essere disabilitate. Un proxy per il download dei feed configurato esplicitamente rimane una deroga separata da parte dell’operatore. Il servizio di testimonianza indipendente mantiene il proprio percorso.

****Parametri automatici del pool**** In **Parametri → MTProxy automatico**, configurare la soglia di errore, il tempo di attesa, la rotazione pianificata, la condivisione dei proxy e il ritardo di fallback consentito. | Controllo | Impostazione predefinita | | --- | --- | | Disconnessioni prima della sostituzione | 3 entro 10 minuti | | Proxy provati per ogni tentativo di connessione | 3 | | Prima / massima pausa dopo un errore | 10 minuti / 6 ore | | Rotazione pianificata | Disabilitata; attivazione in caso di errore | | Account per proxy | 0: preferire voci separate, condividere se necessario. Impostare 1 per attendere una voce esclusiva. | | Ritardo prima del fallback Direct consentito | 10 minuti; Hide IP continua a rifiutare Direct | | Aggiornamento feed / controlli di trasporto | 60 / 10 minuti; i valori dell’area di lavoro principale si applicano al pool condiviso | L’utilizzo di proxy diversi non garantisce indirizzi di uscita diversi. Queste impostazioni non prevalgono sui limiti di Telegram né garantiscono l’anonimato.

Per sostituire l’elenco pubblico con il proprio catalogo di operatori, configurare l’override riportato di seguito. Ciò disabilita completamente gli abbonamenti esterni, anche quando l’array `proxies` è vuoto.

Copi [il catalogo vuoto](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) in `proxy-config/proxies.json` e aggiunga i Suoi endpoint pubblici distribuiti:

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

I valori di esempio devono essere sostituiti. Sono accettate fino a 32 voci distinte. L’ elenco autenticato restituisce etichette/host/porte senza segreti condivisi; selezionandone uno si salvano le relative credenziali nel vault dell’area di lavoro. La disponibilità rimane non verificata fino a un test di trasporto esplicito. Un catalogo non valido consente la configurazione manuale.

Avvio nativo: impostare `TGWITNESS_PROXY_CATALOG` come percorso JSON locale. Docker:

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

L’overlay monta `proxy-config` in sola lettura; i file devono essere leggibili dall’UID 10001 del container. Tale directory è esclusa da Git, dal contesto di compilazione di Docker e dagli archivi sorgente. Questo catalogo configura gli account di raccolta; [il bot witness](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/) utilizza il proprio percorso HTTP/SOCKS5, non MTProxy.

Il fallback diretto è regolato dalla modalità IP sopra descritta. Sospendere il monitoraggio prima di modificare un percorso. Il salvataggio disconnette i client precedenti e annulla gli accessi non completati; un nuovo client utilizza il percorso salvato. Il collegamento tra registro e sessione dell’account rimane inalterato. Le impostazioni sostituiscono il percorso precedente: reinserire le credenziali del proxy al momento della modifica.

Le credenziali sono crittografate con l’algoritmo `network.enc`. L’API non restituisce il nome utente, la password né la chiave segreta. I record firmati contengono il tipo di percorso e indicano se le credenziali sono presenti, escludendo l’endpoint e le chiavi segrete. L’operatore può visualizzare l’endpoint nel pannello di controllo. I campi relativi alle chiavi segrete vengono cancellati dopo il salvataggio, il blocco o il cambio di area di lavoro.

**La funzione «Verifica connessione Telegram**», disponibile anche prima dell’accesso, apre e chiude una connessione temporanea non autorizzata a Telegram tramite il percorso. Non si collega a un sito web di verifica degli IP. Il successo della verifica attesta la connettività di trasporto, non l’accesso ai gruppi, la consegna completa o l’anonimato.

Il proxy si applica alle connessioni del client Telegram, compresi i download di file multimediali dai server di distribuzione (DC) di Telegram. Il browser, pip, SSH e gli strumenti TSA avviati manualmente seguono percorsi separati. Il nome host del proxy può essere risolto localmente. `rdns` influisce sui nomi host di destinazione; Telegram fornisce spesso indirizzi IP numerici dei server di distribuzione (DC).

I protocolli SOCKS5 e HTTP CONNECT non crittografano di per sé le credenziali del proxy né il tunnel client-proxy. MTProto protegge separatamente il traffico di Telegram. Si raccomanda di utilizzare un canale sicuro adeguato per connettersi al proxy su una rete non attendibile. I gruppi privati sono chat su cloud; MTProto non li trasforma in chat segrete con crittografia end-to-end.

## Crittografia e firme

| Livello | Implementato | Responsabilità dell’operatore |
| --- | --- | --- |
| Traffico Telegram | Telethon MTProto | Affidabilità, percorso e disponibilità della piattaforma |
| Pannello web | Token al portatore, impostazione predefinita di loopback, limiti delle richieste | HTTPS o tunnel SSH per l’accesso remoto |
| Segreti | Fernet per le credenziali API, la sessione, le credenziali proxy e la chiave privata di firma | Protegga la chiave di decrittografia e l’host su cui è in esecuzione |
| Chiave di archiviazione | Chiave locale o chiave master esterna per una nuova installazione | Archiviazione protetta separata e backup delle chiavi |
| Messaggi e allegati | Archiviazione dei dati dell’applicazione in testo semplice | Disco/volume crittografato |
| ZIP/JSONL/CSV/HTML | Controlli di integrità, nessuna crittografia dei contenuti | Proteggere le copie esportate e i trasferimenti |
| Provenienza e data | Registro firmato, ricevuta di elaborazione, strumenti RFC 3161 | Chiave affidabile, punti di controllo indipendenti/TSA e procedura di custodia |

**La protezione dell’archiviazione** nell’Account mostra questi stati. Il token del pannello è un segreto di accesso, non una password di crittografia. Concede l’accesso amministrativo; [i token emessi](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/) possono essere limitati ad account e chat. Gli spazi di lavoro condividono il processo host e non sono tenant isolati.

Una demo sintetica, avviata in modo esplicito e isolata, può aprirsi automaticamente tramite una connessione direct loopback. Ciò utilizza una funzionalità con durata di vita del processo separata; essa non rivela il token del pannello configurato né concede l’accesso agli spazi di lavoro reali. Le richieste remote, tramite proxy o cross-origin non possono ottenere né utilizzare questa funzionalità di accesso automatico. Tale comodità non elimina il limite di autenticazione per i dati reali dell’account.

BitLocker, LUKS, FileVault o un volume crittografato gestito possono proteggere l’archivio nell’ambito dei rispettivi modelli di minaccia. Un amministratore di una macchina in esecuzione e sbloccata può comunque leggere i dati. Si prega di includere SQLite WAL/SHM, file multimediali, esportazioni temporanee, swap, backup e download dal browser nella pianificazione dello spazio di archiviazione. Un volume Docker non è crittografato semplicemente perché si tratta di un volume. TgWitness non implementa SQLCipher né la crittografia degli oggetti.

## Chiave master esterna

Per una **nuova** installazione, collochi la chiave principale al di fuori della directory dei dati. Ciò non comporta la migrazione automatica di un archivio di chiavi locale esistente. Prepari una directory delle chiavi accessibile esclusivamente all’identità del servizio, quindi esegua:

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell, utilizzando l’ambiente di progetto installato:

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

In Docker, montare il file in sola lettura al di fuori di `/data`, ad esempio in `/run/secrets/tgwitness-master.key`, e impostare la variabile d’ambiente su tale percorso. L’UID del servizio deve essere in grado di leggerlo. Trasmettere il percorso, non i byte della chiave, tramite file di ambiente/configurazione.

Ogni spazio di lavoro riceve un salt pubblico casuale e una propria chiave Fernet derivata tramite HKDF-SHA256. `vault.external.json` memorizza i metadati di derivazione, non la chiave principale. Una chiave mancante o errata impedisce l’avvio senza sostituirla in modo silenzioso. Conservare sia i metadati del salt che la chiave principale a scopo di ripristino.

Tutti gli spazi di lavoro derivano dalla stessa chiave principale; la sua compromissione compromette l’intera installazione. Il processo in esecuzione è in grado di decriptare i dati riservati. Non si tratta di un HSM né di un KDF basato su password. Non sono accettate password arbitrarie inserite dall’utente in sostituzione di una chiave casuale.

Conservare la chiave esistente per le installazioni attuali fino a quando non venga implementata e verificata una migrazione pianificata. L’eliminazione di `vault.key` o la sostituzione di una chiave master può compromettere l’accesso alle sessioni o alle chiavi di firma. Conservare separatamente i backup crittografati e le chiavi e testare il ripristino in un’istanza isolata.

## Fonti e ambito di verifica

Revisionato il 26 ottobre 2026:

- https://core.telegram.org/api/auth
- https://core.telegram.org/api/obtaining_api_id
- https://docs.telethon.dev/en/stable/basic/signing-in.html
- https://docs.telethon.dev/en/stable/concepts/sessions.html
- https://core.telegram.org/mtproto/mtproto-transports
- https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/SourceFiles/storage/storage_account.cpp
- Telethon 1.45.0: SQLiteSession, StringSession, `Connection._proxy_connect`, `TcpMTProxy.normalize_secret` e metodi di download.

I test locali comprendono fixture SOCKS5/HTTP CONNECT in loopback, sessioni SQLite sintetiche, isolamento del percorso, esclusione dei segreti e rifiuto in caso di chiave mancante. Essi non stabiliscono l’effettiva interoperabilità tra Telegram e il proxy né il comportamento di MTProxy in tempo reale. Si vedano [i file VERIFICATION.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/) e [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
