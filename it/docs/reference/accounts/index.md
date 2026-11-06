# Account e formati delle sessioni

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/

Accedete tramite telefono, codice QR o chiave di autenticazione, importate sessioni da Telethon, Pyrogram o Telegram Desktop ed gestite più account.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Introduzione](https://phishdestroy.github.io/TgWitness/it/docs/reference/quickstart/)

![Introduzione](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

TgWitness effettua l’accesso come **account utente di Telegram** (non come bot) tramite MTProto, utilizzando Telethon. Ogni account risiede nel proprio **spazio** di lavoro (denominato *«workspace»* nell’ API e negli strumenti da riga di comando) con la propria sessione, le proprie fonti, il proprio registro e la propria chiave di firma.

I file di sessione, le stringhe di sessione e le chiavi di autenticazione costituiscono **autorizzazioni relative all’account**: chiunque ne sia in possesso può agire come se fosse titolare di quell’account. Essi non contengono la cronologia dei messaggi.

> [!AVVERTENZA] **Non utilizzi nulla che non possa permettersi di perdere.** Le sconsigliamo vivamente di collegare account personali o comunque di valore, nonché di creare un ID API o un hash API su un account a cui tiene particolarmente. Non si tratta del fatto che TgWitness non sia stato testato: Telegram limita e sospende definitivamente gli account in modo imprevedibile — per volumi di richieste che ritiene eccessivi, indipendentemente dal client o dallo scopo, senza adeguata documentazione. Molti blocchi sono irreversibili. Utilizzi account dedicati. Il corretto svolgimento dei test dipende da Telegram, non dal software, e non garantisce nulla per il futuro.

- [In sintesi](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#at-a-glance)
- [Prima di iniziare: ID API e hash API](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Numero di telefono](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#phone-number) · [Codice QR](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#qr-code) · [Chiave di autenticazione + ID DC](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#auth-key--dc-id)
- [File degli account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#pyrogram-session) · [Coppia sessione + JSON](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#telethon-stringsession) · [JSON dell'account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#account-json)
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

È possibile effettuare l’accesso senza creare un’applicazione API di Telegram. Quando non viene inserita alcuna coppia, né importata né già salvata nell’area di lavoro, TgWitness seleziona una coppia dal proprio pool integrato di coppie API pubbliche 50 (`tgwitness/api_pool.py`), privilegiando Telegram Desktop per un nuovo accesso e mantenendo per prima una coppia salvata; i candidati rimanenti vengono mescolati. Se Telegram rifiuta una coppia (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), viene provata quella successiva, fino a un massimo di otto per ogni accesso; le coppie rifiutate vengono saltate fino al riavvio. La coppia utilizzata per l’accesso viene salvata con l’account e riutilizzata per esso. Un ID API **,** e un hash API **,** identificano l’applicazione per Telegram; essi non autorizzano di per sé un account.

I campi di connessione mancanti utilizzano una coppia deterministica dispositivo/sistema operativo dai cataloghi [opentele2 2.0.0](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735) inclusi nel pacchetto: Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834` e Web `2496`. Anche l’ID di compilazione del codice sorgente di Android `4` utilizza il catalogo Android, come identificato in [BuildVars di Telegram per Android](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web imposta come predefinito A; un suffisso della versione dell’app `K` importato o un pacchetto lingua `macos` seleziona K, mentre la versione `0.7.0` seleziona Webogram. Gli ID applicazione sconosciuti mantengono le impostazioni predefinite del server di Telethon. I campi importati hanno sempre la precedenza, incluse una versione precedente dell’app e un pacchetto lingua vuoto. Il catalogo non modifica mai l’ID API/hash. La sua istantanea di versione viene verificata esplicitamente, non recuperata durante l’accesso. Un profilo salvato rimane stabile dopo gli aggiornamenti.

`account.getAuthorizations` riporta i metadati di autorizzazione salvati da Telegram; non si tratta di un’eco di ogni nuovo `initConnection`. Confrontarlo con il profilo effettivamente inviato. Il collegamento a un’autorizzazione esistente non convalida il relativo hash API: `initConnection` invia l’ID API, mentre l’hash viene utilizzato dalle richieste di accesso.

Dopo l’autorizzazione tramite nuovo telefono o codice QR, TgWitness richiede la configurazione, il DC più vicino, lo stato online, le lingue (quando il pacchetto linguistico non è vuoto), gli aggiornamenti dell’app e gli aggiornamenti dei termini di servizio, con un intervallo di 0.3–1.5 secondi tra una richiesta e l’altra. L’aggiornamento dello stato contrassegna brevemente l’account come online. Questa sequenza viene eseguita una sola volta al completamento dell’accesso, non in caso di importazioni, ricollegamenti o riavvii. L’autorizzazione viene salvata per prima; una richiesta fallita interrompe la sequenza senza riprovare né annullare l’accesso. I risultati vengono registrati come `account.initialized`, con i nomi degli errori anziché i corpi delle risposte. La sequenza non costituisce una garanzia contro le restrizioni dell’account.

Per `tdesktop` , in assenza di `tz_offset` viene utilizzato l’offset UTC locale del server, arrotondato a 900 secondi utilizzando l’algoritmo [opentele2](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; licenza in `tgwitness/client_profiles.LICENSE` ). Viene aggiornato ad ogni connessione in modo da riflettere le variazioni dell’ora legale. Un `tz_offset` importato ha la precedenza su ogni piattaforma e viene mantenuto esattamente, compreso lo zero. Le altre voci `initConnection.params` vengono conservate. Il modulo di accesso HTTP accetta il fuso orario numerico restituito dall’importazione del file; i valori booleani, le frazioni e gli offset al di fuori dell’intervallo supportato vengono rifiutati.

I percorsi diretti, SOCKS5 e HTTP CONNECT utilizzano l’`ConnectionTcpObfuscated` di Telethon (MTProto abbreviato e offuscato). HTTPS CONNECT mantiene il TLS verso il proxy e utilizza lo stesso trasporto offuscato all’interno del tunnel. MTProxy mantiene il proprio trasporto intermedio randomizzato e la gestione dei segreti. I cambi di percorso applicano le stesse scelte. L’offuscamento modifica la struttura dei pacchetti; non nasconde l’account né i metadati del client a Telegram, né implica l’immunità alle restrizioni.

Dopo aver connesso un client autorizzato, TgWitness verifica la configurazione, il DC più vicino, l’autorizzazione corrente, la baseline del livello revisionata, le lingue, gli aggiornamenti dell’app e gli aggiornamenti dei termini di servizio. Queste verifiche diagnostiche vengono eseguite una volta per ogni istanza del client, prima della raccolta, e vengono mostrate nei dettagli della connessione con la relativa ora. `account.connection_checked` registra il risultato senza hash di sessione, indirizzi IP, token o hash API. Non accetta mai i termini di servizio né installa aggiornamenti. Un errore nella richiesta o uno stato FloodWait blocca le richieste successive; un risultato mancante rimane sconosciuto. I controlli locali possono comunque segnalare i propri risultati mentre quelli di rete vengono saltati.

La diagnostica FloodWait conserva in `telegram.backoff` il metodo TL che ha dato esito negativo, eventuali wrapper Takeout/range, l’attesa richiesta dal server e la scadenza effettiva. I dettagli della connessione mostrano il metodo e la scadenza mentre le richieste sono in pausa. La diagnostica include i contatori delle chiamate client per metodo a partire dalla creazione di quel client; essi contano separatamente la risoluzione dei peer annidati, ma non contano i pacchetti né i tentativi di riprova interni di Telethon. I contatori attuali sono disponibili anche come `collector.rpc_activity` nell’API di stato. Non sono inclusi argomenti di richiesta, nomi utente, hash di accesso o testo delle eccezioni. L’ultima diagnostica e la scadenza completa sopravvivono al riavvio. Le attese precedenti prive di un record del metodo non possono essere attribuite retrospettivamente. Vedere [: limiti di esportazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) per la revisione della fonte e la distinzione tra scoperta e acquisizione della cronologia.

`official_app=True` o `False` è il flag di autorizzazione corrente di Telegram. Nessuno dei due valori indica se l’account sia soggetto a restrizioni, considerato affidabile o sotto osservazione. Gli snapshot `account.devices` in modalità evidenza esistenti rimangono la cronologia di tutti i dispositivi connessi; la diagnostica della connessione conserva solo la descrizione del dispositivo corrente.

Prima della connessione, i controlli di avviso confrontano la piattaforma API, il pacchetto linguistico, i formati relativi a dispositivo/sistema operativo e versione dell’app, le impostazioni regionali del sistema mobile e l’effettivo livello di schema di Telethon con la linea di base del catalogo revisionato. Gli avvisi compaiono nel log del server e nei metadati dello stato dell’account; non sostituiscono mai i valori importati né modificano il livello di schema. Un livello diverso costituisce un segnale di verifica della compatibilità, non la prova di un account compromesso o soggetto a restrizioni. Questi controlli e il codice `official_app` non certificano che Telegram consideri l’account al riparo da restrizioni. Lo stato dell’account disconnesso utilizza il profilo salvato invece di generare un’altra descrizione del dispositivo.

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

I moduli **File**, **Chiave di autenticazione** e importazione in blocco mostrano l’avviso relativo alle sessioni parallele prima della connessione. Per impostazione predefinita, le autorizzazioni importate vengono riutilizzate. Tenere chiuso il client originale mentre la sua chiave è in uso qui. Anche **File** e **Chiave di autenticazione** offrono la funzione **Crea un’autorizzazione indipendente**, descritta di seguito. L’importazione in blocco utilizza ancora la modalità diretta. L'accesso tramite telefono e tramite QR interattivo creano autorizzazioni separate. L'intestazione dell'avviso rimane visibile nel modulo di importazione; la sua spiegazione completa si apre automaticamente quando vengono forniti file o una chiave/stringa di sessione. Può essere nascosta dopo la lettura, in modo che il selettore di file e i controlli di connessione rimangano utilizzabili su un telefono.

- I file vengono convertiti **in memoria** sul vostro server TgWitness. I file caricati non vengono archiviati, i file ZIP non vengono estratti su disco e non viene effettuato alcun collegamento con servizi esterni.
- La sessione risultante viene quindi verificata con Telegram. Se un file riporta un ID utente, esso deve corrispondere all’account segnalato da Telegram.
- I file che descrivono account diversi o credenziali API diverse vengono respinti anziché selezionarne uno solo.
- Il campo **«Codice di accesso o testo di sessione»** contiene il campo «Codice di accesso locale TData», un campo in cui incollare una StringSession e **leggere i file senza effettuare l’accesso** (compila il modulo senza contattare Telegram).

### Creare un'autorizzazione indipendente

Selezionare **Crea un'autorizzazione indipendente** prima di collegare i file importati o una chiave di autorizzazione. TgWitness collega brevemente il donatore importato, lo utilizza per approvare il token di accesso QR del nuovo client e disconnette il donatore immediatamente dopo l'approvazione. Il nuovo cliente dispone di una propria chiave di autorizzazione e di un profilo Desktop selezionato separatamente. Le credenziali API e il profilo del dispositivo forniti dal donatore vengono utilizzati esclusivamente per la connessione del donatore. Nessuna autorizzazione esistente viene disconnessa o revocata.

**Tenere il client originale del donatore completamente chiuso durante questa fase.** La connessione iniziale utilizza ancora la chiave copiata, quindi questa modalità non può eliminare il rischio iniziale di uso parallelo. Una volta stabilita la nuova autorizzazione, il proprietario può riaprire il client originale e utilizzare entrambi in modo indipendente. Il login interattivo **tramite codice QR** consente al client originale di approvare l’accesso senza copiare o collegare la propria chiave in questa fase.

Se Telegram richiede 2FA, questa modalità utilizza `twoFA` dal JSON selezionato, se presente, oppure richiede la password. Una password importata non accettata riporta all’apposito modulo. Le password non vengono salvate. La chiave candidata viene salvata crittografata in `independent_login.enc`, comprese le modifiche apportate durante la migrazione del data center. Dopo un’ interruzione, selezionare lo stesso donatore e questa opzione per riprendere la chiave candidata salvata. L’area di lavoro rimane riservata a quell’account; il completamento non riuscito non elimina la nuova area di lavoro. Conserva la sua directory dei dati e la chiave del vault. Le credenziali finali e il registro del journal `account.authorized` includono il metodo di importazione, i formati di input e l’ID API del donatore, senza la chiave o la password del donatore.

Il 5 novembre 2026, un account dedicato ha superato i controlli in tempo reale con i donatori di Telethon, Pyrogram e TData: completamento dell’2FA, nuove chiavi di autorizzazione distinte, accesso simultaneo da parte del donatore e del nuovo cliente e lettura di un canale pubblico. Il caso Telethon ha inoltre ripreso un candidato salvato dopo un’interruzione nella fase della password. Ogni nuova autorizzazione ha completato le sei richieste di inizializzazione post-accesso e il relativo registro firmato è stato verificato. La sessione originale è rimasta utilizzabile in tutti e quattro i formati forniti.

Il database degli errori [RPC di Telegram](https://core.telegram.org/api/errors.json) associa `FRESH_CHANGE_ADMINS_FORBIDDEN` alla modifica degli amministratori, `FRESH_CHANGE_PHONE_FORBIDDEN` alla modifica del numero di telefono e `FRESH_RESET_AUTHORISATION_FORBIDDEN` alla revoca di altre sessioni, alla modifica della loro durata o alla registrazione di una passkey. `SESSION_TOO_FRESH_*` e `PASSWORD_TOO_FRESH_*` riguardano i trasferimenti di proprietà e i prelievi di ricavi o regali. Non si tratta di operazioni di raccolta; un nuovo accesso non implica un divieto generale di lettura di 24 ore. L’esportazione può restituire separatamente `TAKEOUT_INIT_DELAY_*`. TgWitness conserva le pause richieste dal server e non riprova automaticamente l’accettazione dei token né revoca le sessioni per aggirare le restrizioni.

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
- Il profilo di connessione utilizza `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` e `tz_offset` opzionale (secondi rispetto all’UTC, da -43200 a 50400). I campi forniti hanno la priorità sui valori predefiniti generati e sulla lingua del pannello/browser . Gli alias in conflitto vengono rifiutati. Il profilo risolto viene salvato nelle credenziali crittografate dell’area di lavoro e riutilizzato dopo il riavvio, inclusa la versione dell’app.
- `phone`, le impostazioni proxy e i token dei dispositivi vengono **ignorati**. `twoFA` è di sola lettura quando **Crea un'autorizzazione indipendente** è selezionato; l'importazione diretta lo ignora.
- Un JSON privo di un campo di autorizzazione supportato è solo un metadato. Aggiungere il relativo file di sessione oppure procedere con l’accesso tramite telefono o codice QR. Un JSON contenente una sessione supportata o una chiave di autenticazione (Auth Key) può autorizzare autonomamente; vedere [Account JSON](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData è la cartella `tdata` dell’applicazione Telegram Desktop (l’app multipiattaforma disponibile su desktop.telegram.org).

| Sistema | Posizione predefinita `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portatile: accanto a `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Per importarlo:

> **Avviso relativo alle sessioni parallele.** L’importazione diretta di TData riutilizza la chiave di autorizzazione di Telegram Desktop. Non utilizzare tale chiave contemporaneamente su Desktop e TgWitness. Telegram può invalidare l’autorizzazione con `AUTH_KEY_DUPLICATED`, rendendo entrambe le copie inutilizzabili fino a un nuovo accesso.
>
>
>
> Chiudere completamente Desktop, compreso il processo nella barra delle applicazioni, e mantenere chiusa quella copia mentre TgWitness utilizza la sessione importata. **Chiudere, non disconnettersi né revocare la sessione:** la revoca invalida anche la copia importata. Se è necessario che entrambi i client siano in esecuzione, selezionare **Crea un'autorizzazione indipendente** e mantenere Desktop chiuso fino a quando il nuovo accesso non va a buon fine, oppure accedere a TgWitness tramite telefono o codice QR. Si consiglia un account dedicato, ma ciò non rende sicuro l'uso parallelo delle chiavi clonate.
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

### JSON dell'account

Un oggetto JSON, di dimensioni massime pari a **64 KiB**, contenuto in un file con estensione **`.json`**.

| Campo (alias) | Significato |
| --- | --- |
| `api_id` (`app_id`) | ID dell’applicazione, un numero positivo |
| `api_hash` (`app_hash`) | Hash dell’applicazione, 32 caratteri esadecimali |
| `string_session` (`session_string`, `session_str`; `session` legacy) | Testo di Telethon StringSession, non un nome di file |
| `auth_key` (`auth_key_hex`) + `dc_id` | Chiave di autenticazione completa di 512 caratteri e DC 1–5 |
| `user_id` (`id`) | Opzionale; verifica effettuata su Telegram prima che l’autorizzazione venga salvata |
| `device_model` (`device`) | Descrizione del dispositivo di connessione |
| `system_version` (`sdk`) | Versione del sistema operativo di connessione |
| `app_version` | Versione dell’applicazione inviata a Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Lingua del client, lingua del sistema e pacchetto lingua del client; è consentito un valore `lang_pack` vuoto |
| `tz_offset` | Offset UTC opzionale in secondi, inviato in `initConnection.params`; numero intero o stringa di numero intero decimale |

Se sono presenti sia un alias che il nome principale, devono corrispondere. I campi di sessione Telethon espliciti hanno la priorità su un blob `session` generico in un altro formato. Se entrambi contengono sessioni Telethon riconoscibili, devono descrivere la stessa autorizzazione. In assenza di un campo esplicito, `session` deve essere una StringSession Telethon valida. Esempi:

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
| `*.json` con `auth_key` o `string_session` | JSON dell'account | **File** |
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

Utilizza **Account → Importa account** per aggiungere più account, abbinare i file in base al nome base e visualizzare il risultato di ogni accesso. Ogni account dispone di un proprio spazio di lavoro.

Un gruppo raggruppa account correlati senza unire le loro sessioni, le chiavi o le prove. **Il gruppo «Open group** on **Accounts»** rimanda alla relativa pagina all’indirizzo `/groups/<id>`:

- **Account:** percorso di connessione, osservazioni e ultimo messaggio di ciascun membro, con "Avvia**tutto"** e **"Metti in pausa tutto**".
- **Richiede attenzione:** account dai quali si è effettuato il logout, che non sono disponibili o che presentano un problema di connessione, acquisizione, fonte o file multimediale; ogni nome rimanda alla relativa scheda.
- **Le chat di più account mostrano:** le fonti condivise, gli account che le osservano e le interruzioni nel periodo di osservazione dello spazio di lavoro disponibile (fino a sette giorni). **L’esportazione con N account** suddivide l’esportazione di un canale o di un supergruppo tra di essi e firma un unico archivio.
- **Esporta gruppo:** un'ZIP contenente l'esportazione firmata di ciascun account sotto `accounts/` e `manifest.json` elencando le impronte digitali dei SHA-256 e delle chiavi, firmate dall’ spazio di lavoro principale in `manifest.signature.json`. Verifica separatamente l’archivio di ciascun account con `python -m tgwitness.verify` e l’impronta digitale attendibile di quell’account.

I membri condividono le impostazioni del gruppo; un account può mantenere i propri valori. Vedi [le impostazioni condivise](https://phishdestroy.github.io/TgWitness/it/docs/reference/settings/#account-groups), [la guida all’importazione e ai gruppi](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) e [la dashboard del pool MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Esci

**Account → Esci da Telegram** (con il monitoraggio in pausa) richiede a Telegram di terminare la sessione, che quindi scompare anche dalla sezione **Impostazioni → Dispositivi** dell’account e viene rimossa dal vault dell’area di lavoro. Il registro, le fonti, le impostazioni e la chiave di firma rimangono, e il registro registra l’uscita. L’area di lavoro appartiene ancora al proprio account: solo quell’ account potrà riconnettersi ad essa. Se Telegram non risponde, la sessione viene comunque rimossa qui e il pannello lo segnala; la si può terminare in Telegram alla voce **Impostazioni → Dispositivi**.

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
| Connessione proxy non riuscita | Controlla la modalità di instradamento e quella IP. La modalità automatica MTProxy prova un altro accesso funzionante. La modalità "Nascondi l'indirizzo" attende; la modalità "Diretta", come ultima risorsa, può connettersi direttamente dopo il ritardo configurato. Vedi [le modalità di instradamento](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/#ip-modes). |

Si veda anche: [connessione e sicurezza](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/) per i proxy e la crittografia, e [come funziona la raccolta](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/) dei dati acquisiti dopo l’accesso.
