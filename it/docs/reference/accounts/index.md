# Account e formati delle sessioni

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/

Accedete tramite telefono, codice QR o chiave di autenticazione, importate sessioni da Telethon, Pyrogram o Telegram Desktop ed gestite più account.

TgWitness effettua l’accesso come **account utente di Telegram** (non come bot) tramite MTProto, utilizzando Telethon. Ogni account risiede nel proprio **spazio** di lavoro (denominato *«workspace»* nell’ API e negli strumenti da riga di comando) con la propria sessione, le proprie fonti, il proprio registro e la propria chiave di firma.

I file di sessione, le stringhe di sessione e le chiavi di autenticazione costituiscono **autorizzazioni relative all’account**: chiunque ne sia in possesso può agire come se fosse titolare di quell’account. Essi non contengono la cronologia dei messaggi.

> [!AVVERTENZA] **Non utilizzi nulla che non possa permettersi di perdere.** Le sconsigliamo vivamente di collegare account personali o comunque di valore, nonché di creare un ID API o un hash API su un account a cui tiene particolarmente. Non si tratta del fatto che TgWitness non sia stato testato: Telegram limita e sospende definitivamente gli account in modo imprevedibile — per volumi di richieste che ritiene eccessivi, indipendentemente dal client o dallo scopo, senza adeguata documentazione. Molti blocchi sono irreversibili. Utilizzi account dedicati. Il corretto svolgimento dei test dipende da Telegram, non dal software, e non garantisce nulla per il futuro.

- [In sintesi](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#at-a-glance)
- [Prima di iniziare: ID API e hash API](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Numero di telefono](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#phone-number) · [Codice QR](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#qr-code) · [Chiave di autenticazione + ID DC](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#auth-key--dc-id)
- [File degli account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#pyrogram-session) · [Coppia sessione + JSON](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#telethon-stringsession) · [Account JSON](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#account-json)
- [Identifichi ciò di cui dispone](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#identify-what-you-have) · [Formati non supportati](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#unsupported-formats)
- [Account multipli](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#multiple-accounts) · [Garantire la sicurezza dei file degli account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#keeping-account-files-safe) · [Risoluzione dei problemi](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#troubleshooting)

## In sintesi

| Cosa avete a disposizione | Scheda **“Aggiungi account”** | Le serviranno inoltre |
| --- | --- | --- |
| Il numero di telefono e l’accesso ai relativi codici di accesso | **Telefono** | Password 2FA, se abilitata |
| Telegram aperto su un altro dispositivo | **Codice QR** | Password 2FA, se abilitata |
| Un file `.session` (Telethon o Pyrogram) | **File** | File JSON opzionale di accompagnamento per le impostazioni dell’app |
| `.session` + `.json` con lo stesso nome | **File** (selezionare entrambi) | Di norma, nient’altro |
| Una cartella «`tdata`» in Telegram Desktop | **File** (in formato ZIP) | Il codice di accesso locale per il desktop, qualora ne sia stato impostato uno |
| Una StringSession di Telethon (testo, `.txt`, `.tgwitness-session`) | **File** | Non è richiesta alcuna coppia API separata |
| Un codice `.json` associato a una sessione o a una chiave di autenticazione | **File** | Non è richiesta alcuna coppia API separata |
| Una chiave di autenticazione (512 caratteri esadecimali) e il relativo numero DC | **Chiave di autenticazione** | ID utente facoltativo |

TgWitness riconosce i file in base al loro **contenuto**, non al loro nome. La ridenominazione di un file non ne comporta mai la conversione.

## Prima di iniziare: ID API e hash API

È possibile effettuare l’accesso senza creare un’applicazione API di Telegram. Qualora non venga inserita alcuna coppia, né importata né già salvata nell’area di lavoro, TgWitness seleziona una coppia dal proprio pool integrato di 50 coppie API pubbliche (`tgwitness/api_pool.py`) in ordine casuale. Se Telegram rifiuta una coppia (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), viene provata quella successiva, fino a un massimo di otto per ogni accesso; le coppie rifiutate vengono ignorate fino al riavvio. La coppia utilizzata per l’accesso viene salvata con l’account e riutilizzata per lo stesso. Un **ID API** e **un hash API** identificano l’applicazione presso Telegram; essi non autorizzano di per sé un account.

Per utilizzare invece la propria applicazione (l’account che la registra è quello a rischio; si veda [«Perché un pool di API integrato?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)»):

1. Apra [my.telegram.org](https://my.telegram.org) ed effettui l’accesso con un numero di telefono qualsiasi di cui sia titolare. Il codice verrà inviato nell’app di Telegram, non tramite SMS.
2. Scegliete **gli strumenti di sviluppo API**.
3. Creare un’applicazione: titolo a scelta e nome abbreviato (5–32 lettere), piattaforma **Desktop**. L’URL e la descrizione possono essere lasciati vuoti.
4. Copiate **l’api_id dell’app** (un numero) e **l’api_hash dell’app** (32 caratteri esadecimali).

Nel pannello, sotto il modulo di accesso, sono presenti i campi **«ID API» e «Hash**». È possibile incollare una singola coppia `api_id:api_hash` nel campo **«ID API»** e entrambi i campi verranno compilati automaticamente. Una sola coppia può essere utilizzata per tutti i Suoi account. Dopo un accesso riuscito, i dati vengono salvati, crittografati, esclusivamente in quell’area di lavoro e non vengono mai rinviati al browser.

Sono coinvolte tre diverse credenziali:

| Segreto | Si apre | Dove si trova |
| --- | --- | --- |
| Token del pannello | Il pannello web di TgWitness | `panel-token.txt` nella directory dei dati, oppure `TGWITNESS_TOKEN` |
| ID API + hash | Nulla di specifico; identifica l’app | Accoppiamento integrato, impostazioni importate o la propria app su my.telegram.org |
| Autorizzazione dell’account | L’account Telegram | Creato tramite accesso tramite telefono/codice QR o importato come sessione |

Se è necessario accedere a Telegram tramite un proxy, configurarlo innanzitutto in **Account → Impostazioni → Impostazioni di connessione → Modifica percorso di connessione**.

## Numero di telefono

1. Apra **l’account**, selezioni la scheda **«Telefono»** e inserisca il numero in formato internazionale, ad esempio `+44 7700 900123`. Gli spazi e i trattini vengono rimossi automaticamente.
2. Clicchi su **«Continua**». I campi «ID API» e «Hash» possono essere lasciati vuoti.
3. Inserisca il codice inviato da Telegram (di norma all’app di Telegram; la ricezione tramite SMS non è garantita).
4. Se l’account dispone della verifica in due passaggi, inserisca tale password. Non si tratta del token del pannello né del codice di accesso del dispositivo.
5. Verifichi l’ID dell’account visualizzato dopo aver effettuato l’accesso, quindi selezioni le fonti.

I codici di accesso e la password 2FA non vengono mai salvati su disco.

## Codice QR

Utilizzi questa opzione quando l’account è già connesso su uno smartphone o su un altro computer.

1. Scheda **«Codice QR»** → **Mostra codice QR**. I campi «ID API» e «Hash» possono rimanere vuoti.
2. Sul dispositivo su cui si è effettuato l’accesso: **Impostazioni → Dispositivi → Collega dispositivo desktop**, scansionare il codice e confermare.
3. Inserisca la password 2FA in TgWitness qualora Telegram la richieda.

L’immagine QR viene generata localmente. I codici scadono; prema **«Genera un altro codice QR»** per riprovare. Il blocco del pannello, il cambio di area di lavoro o l’avvio di un’altra sessione di accesso annullano un codice in sospeso.

## Chiave di autenticazione + ID DC

Una chiave di autorizzazione (Auth Key) è l’autorizzazione grezza di 256 byte alla base di ogni sessione di Telegram, rappresentata da **512 caratteri esadecimali**, insieme al numero del data center **DC 1–5**.

1. Scheda **«Chiave di autenticazione**». Incolli la chiave completa; una chiave abbreviata contenente «`…`» non è valida.
2. Selezioni l’ID DC fornito insieme alla chiave.
3. È possibile inserire l’**ID utente**. In tal caso, TgWitness rifiuterà la connessione qualora Telegram segnalasse un account diverso.
4. **Account** Press **Connect**.

Una chiave di autenticazione (512 caratteri) non è un hash API (32 caratteri). La stessa chiave può anche essere importata in formato JSON; si veda [Account JSON](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#account-json).

## File degli account

Aprire **«Aggiungi account» → «File»** e selezionare fino a **quattro file appartenenti a un unico account**, per un totale di **8 MiB**, quindi premere **«Collega account**».

- I file vengono convertiti **in memoria** sul vostro server TgWitness. I file caricati non vengono archiviati, i file ZIP non vengono estratti su disco e non viene effettuato alcun collegamento con servizi esterni.
- La sessione risultante viene quindi verificata con Telegram. Se un file riporta un ID utente, esso deve corrispondere all’account segnalato da Telegram.
- I file che descrivono account diversi o credenziali API diverse vengono respinti anziché selezionarne uno solo.
- Il campo **«Codice di accesso o testo di sessione»** contiene il campo «Codice di accesso locale TData», un campo in cui incollare una StringSession e **leggere i file senza effettuare l’accesso** (compila il modulo senza contattare Telegram).

### Telethon `.session`

|  |  |
| --- | --- |
| Di cosa si tratta | Il database SQLite creato dagli strumenti basati su Telethon, ad esempio `my_account.session` |
| Riconoscuto da | Tabelle `sessions` (insieme a `dc_id`, `server_address`, `port`, `auth_key`) e `version` = 7 o 8 |
| Requisiti | Esattamente una riga relativa a una sessione autorizzata; un database chiuso e completo |

Chiuda innanzitutto il programma che ha creato il file. Se accanto ad esso è presente `my_account.session-journal` o `my_account.session-wal`, il database non è stato completato: apra e chiuda correttamente il client originale. L’eliminazione di tali file sidecar può lasciare una copia danneggiata.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Di cosa si tratta | Gli strumenti basati su Pyrogram creano un database SQLite |
| Riconoscuto da | Tabella `sessions` con `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 o 3 |
| Requisiti | È consentita una sola sessione **utente** autorizzata sulla rete di produzione. Le sessioni relative ai bot e ai DC di prova vengono respinte |

L’ID utente memorizzato viene verificato su Telegram al momento dell’accesso.

### Coppia sessione + JSON

Gli account vengono spesso distribuiti sotto forma di due file con lo stesso nome, ad esempio `447700900123.session` e `447700900123.json`. Selezionateli **entrambi** contemporaneamente.

- Dal file JSON, TgWitness utilizza `app_id`/`api_id` e `app_hash`/`api_hash`, pertanto di norma non è necessario inserire le credenziali API.
- Altri campi quali `phone`, `device`, `sdk`, `app_version`, `lang_pack` o una password `twoFA` memorizzata vengono **ignorati**. Se l’account dispone dell’autenticazione a due fattori (2FA), TgWitness la richiede.
- Un file JSON di per sé contiene solo metadati. In assenza del file di sessione, proceda con l’accesso tramite telefono o codice QR.

### Telegram Desktop (TData)

TData è la cartella `tdata` dell’applicazione Telegram Desktop (l’app multipiattaforma disponibile su desktop.telegram.org).

| Sistema | Posizione predefinita `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portatile: accanto a `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Per importarlo:

> **Avviso relativo alle sessioni parallele.** L’importazione di TData riutilizza la chiave di autorizzazione di Telegram Desktop; non crea un accesso indipendente. Si raccomanda di non utilizzare tale chiave contemporaneamente su Desktop e TgWitness. Telegram può invalidare l’autorizzazione con il codice `AUTH_KEY_DUPLICATED`, rendendo entrambe le copie inutilizzabili fino a un nuovo accesso.
>
>
>
> Chiuda completamente Desktop, compreso il processo nella barra delle applicazioni, e mantenga chiusa quella copia mentre TgWitness utilizza la sessione importata. **Chiuda l’applicazione, non effettui il logout né revochi la sessione:** la revoca invalida anche la copia importata. Se ha bisogno che entrambi i client siano in esecuzione, acceda a TgWitness tramite telefono o codice QR per creare la propria autorizzazione. Si raccomanda l’uso di un account dedicato, ma ciò non garantisce la sicurezza dell’uso in parallelo delle chiavi clonate.
>
>
>
> Ciò vale anche per i file `.session` importati, il testo di StringSession e l’Auth Key HEX. Gli altri client con autorizzazioni create in modo indipendente possono rimanere connessi. Si veda [la documentazione di Telegram relativa a AUTH_KEY_DUPLICATED](https://core.telegram.org/api/errors#406-not-acceptable).

1. Chiudere completamente Telegram Desktop.
2. Si crei un file ZIP contenente **esclusivamente** questi due elementi provenienti da `tdata`:

   - `key_datas`
   - il file di 16 caratteri che termina con «`s`» accanto ad esso, solitamente «`D877F783D5D3EF8Cs`»

   La compressione dell’intera cartella con la relativa cache multimediale supera solitamente i limiti (512 voci, 32 MiB decompressi). 3. Selezionare il file ZIP in **«File**». Se Telegram Desktop dispone di un **codice di accesso locale**, inserirlo prima nel campo **«Codice di accesso» o nel testo della sessione**. Non si tratta della password 2FA.

Supportato: un account per archivio, archiviazione moderna `key_datas`/`key_data0`/`key_data1`, codice di accesso locale. Non supportato: cartelle con più account connessi, versioni precedenti dell’applicazione Desktop, file ZIP protetti da password e l’app nativa separata per macOS «Telegram per macOS».

### Telethon StringSession

Una singola riga di testo, che solitamente inizia con `1` e contiene circa 350 caratteri. Caricatela come file `.txt` o `.tgwitness-session` (al massimo 4 KiB), oppure incollatela nella sezione **«Codice di accesso» o «Testo della sessione**». Sono accettate solo stringhe Telethon; le stringhe Pyrogram e TDLib utilizzano formati diversi.

### Account JSON

Un oggetto JSON, di dimensioni massime pari a **64 KiB**, contenuto in un file con estensione **`.json`**.

| Campo (alias) | Significato |
| --- | --- |
| `api_id` (`app_id`) | ID dell’applicazione, un numero positivo |
| `api_hash` (`app_hash`) | Hash dell’applicazione, 32 caratteri esadecimali |
| `string_session` (`session_string`, `session`) | Testo di Telethon StringSession, non un nome di file |
| `auth_key` (`auth_key_hex`) + `dc_id` | Chiave di autenticazione completa di 512 caratteri e DC 1–5 |
| `user_id` (`id`) | Opzionale; verifica effettuata su Telegram prima che l’autorizzazione venga salvata |

Qualora siano presenti sia un alias che il nome principale, questi devono corrispondere. Esempi:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

Il primo esempio si limita a inserire le credenziali API; è possibile effettuare l’accesso tramite telefono o codice QR, oppure aggiungere un file di sessione. Non sono accettati elenchi in blocco (un array JSON di account).

## Identifichi ciò di cui dispone

| Come potete vedere | Si tratta di | Utilizzo |
| --- | --- | --- |
| `*.session`; aprendolo in un editor di testo, in alto compare `SQLite format 3` | Telethon o Pyrogram SQLite | **File** (rilevati automaticamente) |
| Una cartella denominata «`tdata`» contenente «`key_datas`» | Telegram Desktop TData | Comprimere i due file in formato ZIP, quindi **«File»** |
| Una riga di testo che inizia con `1`, circa 350 caratteri | Telethon StringSession | **File** |
| `*.json` con `app_id`/`app_hash` | Metadati correlati | **File**, insieme alla relativa sessione |
| `*.json` con `auth_key` o `string_session` | Account JSON | **File** |
| 512 caratteri `0-9a-f` | Chiave di autenticazione | **Chiave di autenticazione** |
| 32 caratteri `0-9a-f` | Hash dell’API | **ID API + Hash** |
| `td.binlog` o `db.sqlite` proveniente da un’applicazione TDLib | Archiviazione TDLib | Non supportato |
| `123456789:AA…` | Token del bot | Non supportato |

## Formati non supportati

| Formato | Alternativa |
| --- | --- |
| Archiviazione TDLib (`td.binlog`) ed esportazioni TDLib | Acceda tramite telefono o codice QR |
| **Stringhe** di sessione di Pyrogram | Utilizzi il file Pyrogram `.session`, oppure il codice QR o il numero di telefono |
| TData con diversi account connessi | Effettuate il logout dagli altri account in Telegram Desktop oppure utilizzate il file di sessione specifico di ciascun account |
| Token dei bot | Non supportato: TgWitness opera in qualità di account utente |
| Elenchi in formato CSV/JSON di numerosi account | Importa i file di sessione supportati tramite **Account → Importazione degli account**, oppure accedi tramite telefono/QR in spazi di lavoro separati |
| Sessioni di Test-DC o con bot | Si prega di utilizzare un account utente di produzione |

## Account multipli

Premere **+** accanto al selettore dell’account, oppure aprire **Account → Impostazioni → Impostazioni di connessione → Ambienti di lavoro**, inserire un’etichetta e effettuare l’accesso.

- È possibile creare un numero illimitato di aree di lavoro, compresa quella principale. Ciascuna dispone di una propria sessione, percorso proxy, fonti, criteri di acquisizione, registro, chiave di firma, punti di controllo ed esportazioni.
- Il cambio dell’area di lavoro visualizzata non mette in pausa le altre.
- Un registro rimane associato all’account che lo ha creato. L’accesso con un account diverso richiede un altro spazio di lavoro, e un singolo account non può essere assegnato a due spazi di lavoro.
- Il token del pannello principale controlla tutte le aree di lavoro. [L’accesso concesso](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/) può limitare l’accesso di altre persone ad account e chat selezionati, con autorizzazioni distinte e limiti di sessione.
- **La voce «Accounts»** rinomina un’area di lavoro ed elimina quella aggiunta, insieme alla relativa sessione, al registro, alle fonti e alla chiave di firma. L’area di lavoro principale non può essere eliminata dal pannello.

### Importazione in blocco e gruppi di account

Usa **Account → Importazione degli account** per aggiungere più account, abbinare i file per nome e vedere l’esito di ogni accesso. Ogni account riceve un proprio spazio di lavoro. I gruppi possono copiare impostazioni selezionate da un modello senza unire sessioni, chiavi o prove. Consulta [la guida a importazione e gruppi](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) e [il pannello del pool MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Esci

**Account → Esci da Telegram** (con il monitoraggio in pausa) richiede a Telegram di terminare la sessione, che quindi scompare anche dalla sezione **Impostazioni → Dispositivi** dell’account e viene rimossa dal vault dell’area di lavoro. Il registro, le fonti, le impostazioni e la chiave di firma rimangono, e il registro registra l’uscita. L’area di lavoro appartiene ancora al proprio account: solo quell’ account potrà riconnettersi ad essa. Se Telegram non risponde, la sessione viene comunque rimossa qui e il pannello lo segnala; la si può terminare in Telegram alla voce **Impostazioni → Dispositivi**.

## Convertire una sessione di Telethon in modalità offline

Il pannello importa direttamente i file `.session`. Per una conversione offline in un file StringSession, esegua dalla cartella del progetto:

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

Il convertitore legge esclusivamente file Telethon SQLite (fino a 64 MiB), non modifica mai i dati in ingresso, non effettua alcuna richiesta di rete e rifiuta di sovrascrivere un file di output esistente.

## Garantire la sicurezza dei file degli account

- Trattate ogni `.session`, TData ZIP, StringSession, chiave di autenticazione e file JSON dell’account come una password. TgWitness conserva le autorizzazioni importate nel proprio archivio crittografato; potrete eliminare i file originali in un secondo momento.
- Non esegua la stessa autorizzazione in due programmi contemporaneamente. Telegram potrebbe revocarla (`AUTH_KEY_DUPLICATED`) e entrambe le copie smetterebbero di funzionare.
- Una sessione scaduta o revocata non può essere ripristinata tramite conversione. Effettate nuovamente l’accesso.

## Risoluzione dei problemi

| Messaggio o sintomo | Cosa fare |
| --- | --- |
| *Impossibile leggere questa sessione. Chiuda il client originale…* | Il file SQLite è aperto o non completato (sidecar `-journal`/`-wal`). Chiuda correttamente il programma originale e copi nuovamente il file. |
| *Schemi SQLite di Telethon supportati: 7 e 8* / *Pyrogram … 2 e 3* | Il file è stato creato da una versione della libreria molto vecchia o sconosciuta. Effettui invece l’accesso tramite telefono/codice QR. |
| *Sono supportate esclusivamente le sessioni utente autorizzate in ambiente di produzione* | Il file Pyrogram appartiene a un bot o alla rete di test. |
| *L’archivio TData supera le 512 voci o i 32 MiB* | Solo i file ZIP `key_datas` e `D877F783D5D3EF8Cs`, non l’intera cartella. |
| *Impossibile decriptare TData. Verifichi il codice di accesso locale del Desktop* | Inserisca il codice di accesso locale di Telegram Desktop nel campo **«Codice di accesso» o «Testo della sessione**». |
| *Importare un account TData alla volta* | Telegram Desktop disponeva di diversi account; si veda la sezione [«Formati non supportati](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#unsupported-formats)». |
| *I file selezionati descrivono diversi account o credenziali API* | Selezionare i file relativi a un solo account. |
| *Il file JSON non contiene credenziali API o autorizzazioni supportate* | Verifichi i nomi dei campi nel file [JSON dell’account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#account-json). |
| *Solo metadati API* | Il file JSON non contiene alcuna sessione. Si prega di aggiungere il file `.session` oppure di utilizzare il numero di telefono o il codice QR. |
| *La chiave di autenticazione HEX deve contenere tutti i 512 caratteri esadecimali* | La chiave è troncata o contiene «`…`». |
| L'ID dell'account non corrisponde a quello dell'account importato | L’ID utente del file differisce da quello riportato da Telegram; il file si riferisce a un altro account. |
| L'account appartiene già a un altro spazio di lavoro | Si apra quell’area di lavoro anziché aggiungere l’account due volte. |
| Collegato, ma nella lista delle chat alla voce **«Fonti»** manca un gruppo privato | Verificare l’iscrizione. Il selettore esamina le prime 1.000 conversazioni; aumentare il limite nella sezione **«Parametri**». |
| Connessione proxy non riuscita | Verifichi il percorso e la modalità IP. La modalità MTProxy automatica tenta un altro accesso funzionante. La modalità «Nascondi IP» rimane in attesa; la modalità di ripiego selezionata esplicitamente può connettersi direttamente dopo il ritardo configurato. Veda [le modalità di instradamento](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/#ip-modes). |

Si veda anche: [connessione e sicurezza](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/) per i proxy e la crittografia, e [come funziona la raccolta](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/) dei dati acquisiti dopo l’accesso.
