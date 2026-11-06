# Guida ai pannelli

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/panel/

Tutte le schermate del pannello: chat, diario, fonti, esportazioni, Extra, modalità di protezione e controllo del codice.

[Configurazione iniziale e impostazioni](https://phishdestroy.github.io/TgWitness/it/docs/reference/settings/) · [Account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/) · [Esportare e verificare](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/) · [Rapporti sui casi](https://phishdestroy.github.io/TgWitness/it/docs/reference/case-reports/)

Cosa fa ogni schermata, cosa scrive nel registro firmato e dove si trova la guida dettagliata. Il pannello mostra un’area di lavoro alla volta: un account Telegram con le proprie fonti, il proprio registro e la propria chiave di firma. Il selettore nella parte superiore della barra laterale consente di passare da un’ area di lavoro all’altra. L’indirizzo contiene l’area di lavoro (`?ws=…`); finché l’indirizzo, il selettore e l’account caricato non coincidono, le azioni rimangono bloccate.

Use [Compare collection methods](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md) to choose between live observation, full history, fresh account/chat exports and saved-record handover. The Exports page includes the same comparison above its download controls.

## Orientati

Le sezioni giornaliere si trovano nella parte superiore della barra laterale, **la sezione «Account»** è sotto **«Area di lavoro»** , mentre tutto il resto si trova sotto **«Altri strumenti e impostazioni** ». L’interruttore **a livello di interfaccia** nella barra superiore determina il numero di sezioni visualizzate:

| Livello | Sezioni nella barra laterale |
| --- | --- |
| Semplice | Home, Chat, Modifiche, Archivi e Impostazioni |
| Standard | Inoltre Case Board, Account e Accesso |
| Esperto | Inoltre: Fonti, Extra, Chiedi all’archivio, Parametri, Account, Registro di sistema e Integrazioni |

Chiamate semplici: «Inizia qui», «Diario» ed «Esportazioni» **Home**, **Modifiche** e **Archivi**. Un livello nasconde solo alcune sezioni. Una funzionalità nascosta continua a funzionare e il server verifica autonomamente ogni autorizzazione. Livello, lingua, tema e fuso orario vengono salvati per ogni operatore e spazio di lavoro; vedi [impostazioni](https://phishdestroy.github.io/TgWitness/it/docs/reference/settings/).

La barra superiore presenta inoltre:

- **Vai a una sezione** (Ctrl+K, o ⌘K su Mac): trova una chat, un parametro o una voce del diario tramite `#number`. I tasti freccia consentono di spostarsi, Invio apre, Esc chiude.
- **Notifiche**: problemi e modifiche alle chat ricavati dal diario. L’opzione **«Segna tutto come letto»** azzera il contatore, mentre **«Regole di notifica»** apre le impostazioni relative alle regole. L’invio a Telegram, Discord o via e-mail viene configurato in [Extra → Notifiche](https://phishdestroy.github.io/TgWitness/it/docs/reference/panel/#notifications).
- L’indicatore di connessione per questo spazio di lavoro. **Lo stato di funzionamento del Collector,** sotto la barra superiore, lo suddivide in connessione a Telegram, acquisizione degli eventi, fonti e coda degli allegati.
- **Lock**: chiude il pannello in questo browser. La raccolta continua a funzionare sul server.
- La modalità di protezione accanto al numero di versione; vedi [modalità di protezione](https://phishdestroy.github.io/TgWitness/it/docs/reference/panel/#protection-modes).

L’area di lavoro dimostrativa contiene messaggi fittizi e non si connette mai a Telegram. Le azioni che potrebbero modificare un’area di lavoro reale vengono lì bloccate.

## Inizia da qui

Scegli un'attività. L'**opzione «Esporta il mio account»** scarica ciò che l'account può leggere al momento. **L'opzione «Segui un'indagine»** registra i nuovi messaggi, le modifiche osservate e le notifiche di cancellazione dalle chat che scegli. La scheda di configurazione mostra i tre passaggi: collega l'account, scegli le fonti, avvia il monitoraggio. La domanda obiettivo rimane su questa pagina finché non rispondi o la salti. Un nuovo spazio di lavoro apre invece la [prima configurazione](https://phishdestroy.github.io/TgWitness/it/docs/reference/settings/).

## Chat

Conversazioni salvate, di default in sola lettura.

- Cerca nell’elenco per nome o ID. **Scegli** per aggiungere o rimuovere le chat monitorate. “**Apri link Telegram**” accetta un nome utente o un link di invito e salva un’anteprima nel diario. **“Partecipa / apri e osserva”** ti fa entrare nella chat e la aggiunge alle tue fonti; aprendo un bot, lo invia `/start`.
- L’intestazione della chat conta i messaggi **cancellati, il testo conservato**, **quelli cancellati prima del salvataggio** e **quelli non trovati al controllo successivo**. L’elenco delle chat e le notifiche utilizzano le stesse definizioni. Un messaggio cancellato è di colore rosso e conserva il testo salvato; un messaggio modificato conserva tutte le versioni salvate. Ogni cancellazione riporta le informazioni note: quando è stato visualizzato, che Telegram non segnala chi lo ha cancellato, oppure che è arrivata solo la notifica.
- **La cronologia dei messaggi caricati** riporta gli ultimi 100, 250 o 500 messaggi in questa vista e nel diario. Per caricare tutte le fonti abilitate, utilizzare [Fonti → Cronologia completa](https://phishdestroy.github.io/TgWitness/it/docs/reference/panel/#sources).
- **L’opzione “Esporta chat”** scarica l’intera cronologia visibile sotto forma di file firmato `chat.json` e `chat.html`. Diversi account collegati possono condividere il lavoro: ciascuno scarica il proprio intervallo di numeri di messaggi e firma la propria parte, mentre l’account che avvia l’ esportazione firma l’archivio. Vedi [esportare una chat](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md).
- **La sezione "Persone"** elenca tutti coloro che hanno messaggi salvati in questa chat. I profili delle persone sono disattivati per impostazione predefinita poiché contengono dati personali relativi a terzi. Quando sono attivati per una chat, un profilo mostra il nome e la cronologia dei nomi utente, i flag di Telegram, gli hash degli avatar, l’attività, chi risponde a chi, altre chat osservate e i portafogli, i telefoni, i nomi utente e i link menzionati. Ogni dato rimanda al proprio record. **L’esportazione dei profili** salva un file firmato, facoltativamente in un ZIP protetto da password; la disattivazione dei profili elimina il file del profilo. Vedi [i profili delle persone](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#people-profiles).
- **La funzione “Salva profilo” ora** registra un’istantanea del profilo della chat o del bot: descrizione, membri, link di invito, comandi del bot.

### Solo lettura, invio e segreti

Due interruttori situati sopra i messaggi proteggono l’account e il lettore:

- **La modalità "Sola lettura"** è attiva all’apertura di una chat. Disattivala per inviare messaggi o premere i pulsanti del bot . Ogni azione chiede **“Invia come @account?**” o **“Premi questo pulsante del bot come @account?**”, indicandoti che i membri della chat lo vedranno e che verrà inserito nel registro firmato. **L’opzione “Non chiedere più per 10 minuti in questa chat**” salta la domanda per un po’. L’invio è disattivato per l’obiettivo **“Prove per un caso**”, nel pannello e nell’API.
- **La funzione «Mask secrets»** nasconde ciò che sembra una password, un codice di accesso, una chiave API o un hash, un token di bot, una stringa di sessione, una chiave privata, un JWT o un numero di carta di pagamento (i numeri delle carte vengono verificati con la somma di Luhn). **La funzione «Show»** rivela un valore; la rivelazione viene registrata nel registro. Anche la disattivazione della mascheratura per questo browser viene registrata. Cambia solo la visualizzazione: i record originali e ogni esportazione mantengono il testo completo.

## Registro

Tutti i record firmati dall’area di lavoro, in ordine cronologico dal più recente al più vecchio.

- **La panoramica** riporta il numero di messaggi osservati, le modifiche registrate, le notifiche di cancellazione e le fonti selezionate.
- **Cronologia degli eventi** filtra per tipo di evento (tutti, modifiche, eliminazioni, reazioni, appartenenza, copertura), per testo e per fonte. **Carica gli eventi precedenti** torna alla pagina precedente.
- Apri un record per visualizzarne i dettagli, l’hash e il payload. **Il link a questo record** è un indirizzo che apre lo stesso record. Eventuali informazioni riservate vengono mascherate in questa anteprima; le esportazioni mantengono l’originale.
- Il registro è di sola aggiunta: nessuna operazione nel pannello modifica o elimina un record. Verificalo tramite **Esportazioni → Verifica registro** oppure `python -m tgwitness.verify`; vedi [esportazione e verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/).

## Fonti

Quali conversazioni vengono registrate in questo spazio di lavoro e quali dati vengono conservati. Le modifiche si applicano alle attività future; le registrazioni salvate rimangono invariate.

**L'aggiornamento dell'elenco delle chat** legge le chat e le cartelle dell'account. Non scarica i messaggi.

### Ambito di applicazione

- **Cosa registra questo account** : **Chat selezionate** (solo le chat che aggiungi), **Cartella Telegram** (una delle cartelle dell’account, comprese le chat aggiunte successivamente) oppure **Account completo** (ogni chat, e ogni nuova chat, gruppo, chat privata o bot non appena appare). **Modalità di indagine** è per un account dedicato: registra tutto ciò che l’account vede, i propri messaggi e le pressioni dei pulsanti, e salva immediatamente il profilo di ogni nuova chat e i messaggi visibili in precedenza. L’ [guida dedicata agli account](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) spiega perché non bisogna mai utilizzare il proprio account principale.
- **I tipi di origine** limitano le modalità «cartella» e «intero account» a canali, gruppi, chat private e bot. **«Azioni proprie»** aggiunge i messaggi, le modifiche e le pressioni sulla tastiera di risposta dell’account stesso.
- **Quando compare una nuova chat o un nuovo bot**: salva il suo profilo e fino al numero scelto dei suoi ultimi messaggi visibili.

Limiti: le chat segrete non vengono mai acquisite TgWitness. Non viene registrato nulla mentre TgWitness non è in esecuzione; dopo un riavvio, il programma recupera solo ciò che Telegram restituisce ancora e il rapporto mostra il divario. Le chat che superano il limite dell’elenco delle chat (1.000 conversazioni, salvo modifiche nei Parametri) vengono aggiunte non appena diventano attive. I pulsanti del bot integrati premuti in un’altra app non vengono rilevati; la risposta del bot viene registrata.

### Chat incluse

Filtra per stato (**Abilitato**, **In pausa**, **Prioritario**, **Escluso**, **Accesso non confermato**, **Ignorato**) e tipo, quindi agisci sulla selezione: abilita, metti in pausa, contrassegna o rimuovi la priorità, escludi dall’ambito o elimina. Il badge di stato mostra solo lo stato; le azioni si trovano nel menu di ogni riga con una descrizione di ciò che fanno. La messa in pausa e l’esclusione richiedono una conferma, anche in blocco. La rimozione di una fonte richiede il suo nome ed elimina i profili delle persone ad essa associate; i record salvati rimangono nel diario.

Una fonte che non compare nell’elenco delle chat dell’account sta **ricevendo aggiornamenti, pur non figurando nell’elenco delle chat**mentre continuano ad arrivare registrazioni; in caso contrario, **l’accesso non è confermato**. L’opzione **«Chat disponibili»** aggiunge le chat selezionando **«Aggiungi selezionati»** o **«Aggiungi tutti quelli corrispondenti**».

### Cronologia completa

Carica la cronologia disponibile di ogni fonte abilitata nelle chat e nel diario. I progressi vengono mantenuti dopo un riavvio; gli allegati seguono le impostazioni multimediali dell’utente. Vedi [la cronologia delle fonti](https://phishdestroy.github.io/TgWitness/it/docs/reference/history/).

### Registrazione

- **Scegli quali modifiche conservare**: nuovi messaggi, modifiche, notifiche di cancellazione, reazioni visibili, ingressi e uscite. Un'impostazione predefinita modifica il modulo; l'opzione **«Salva impostazioni di registrazione»** la applica. Riattivare una categoria non recupera gli eventi persi.
- **Conserva i file multimediali quando disponibili**: scarica allegati fino a una determinata dimensione per file, imposta per tipo da 1 a 2.000 MiB e limita la durata dei video in secondi (0 indica nessun limite). Ogni tentativo di download viene registrato con il relativo esito.
- **Ricontrollo**: le chat prioritarie vengono ricontrollate ogni pochi minuti, le altre raramente, in modo che l’account resti al di sotto dei limiti FloodWait di Telegram. Impostando il valore su 0 si disattiva un gruppo. Contrassegnare le chat prioritarie con la stellina nell’elenco; il numero di chat per ciclo e la pausa tra una chat e l’altra sono specificati in Parameters. Vedi [la raccolta](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/).

## Esportazioni

**La sezione «Downloads»** prepara i file; **«Build report»** consente di scegliere l’aspetto dei report.

| Cosa | Utilizzalo per | Guida |
| --- | --- | --- |
| Esportazione dell’account | Un'istantanea aggiornata di ciò che l'account può leggere in questo momento | [Esportazione dell’account](https://phishdestroy.github.io/TgWitness/it/docs/reference/account-export/) |
| Condivisione della copia | Una versione ridotta di un'esportazione completa dell’account | [Informativa](https://phishdestroy.github.io/TgWitness/it/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| Firmato ZIP | Diario, report, allegati e strumenti di verifica all’interno di un confine fisso del diario | [Esporta e verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/) |
| Report in formato HTML, PDF e JSON | Un rapporto sigillato e leggibile | [Rapporti sui casi](https://phishdestroy.github.io/TgWitness/it/docs/reference/case-reports/) |
| JSONL, CSV | Registrazioni originali con firme; un foglio di calcolo protetto dalle formule | [Esporta e verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/) |
| Estratto del passaggio di consegne | Solo le chat, il periodo e le persone di cui il destinatario ha bisogno | [Prove](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#investigation-handoff) |
| Esportazione delle chat | Una chat firmata `chat.json` e `chat.html` | [Esporta una chat](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **Crittografando i download sopra indicati con una password** (di almeno 12 caratteri) si salva un file AES-256 ZIP che può essere aperto con 7-Zip o WinRAR. Il file firmato al suo interno rimane inalterato. La password non viene memorizzata.
- **Le esportazioni preparate** conservano fino a 20 file entro un limite di 2 GiB, più l’ultimo, per download ripetuti, ciascuno con il proprio SHA-256. La preparazione di un file non garantisce la consegna.
- Quando il browser rifiuta la finestra di dialogo di salvataggio, il pannello ricorre a un normale download.
- **La tua identità di firma** mostra l’impronta digitale della chiave. Le opzioni **«Salva checkpoint»** e «Scarica **ricevuta di esecuzione firmata»** ti consentono di conservare le registrazioni al di fuori del collector. L’opzione «Prepara **richiesta di timestamp»** genera una richiesta RFC 3161 senza contattare alcun servizio.

## Impostazioni, account e connessione

- **Impostazioni**: obiettivo, connessione, cosa registrare e interfaccia. Vedi [prima configurazione e impostazioni](https://phishdestroy.github.io/TgWitness/it/docs/reference/settings/).
- **Account**: ogni spazio di lavoro con il proprio stato, le fonti, gli eventi e la coda degli allegati. Filtra per **“Richiede attenzione”**, **“In fase di raccolta”**, **“Offline” o “In pausa”** oppure **“Non connesso”**, metti in pausa o riprendi una selezione, importa file di account in blocco e gestisci i gruppi. Vedi [account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/).
- **Account**: accesso e percorso di connessione di questo account. Diretto, un profilo WireGuard, il proprio proxy, il pool pubblico MTProto o WARP; preparare e verificare un percorso, quindi applicarlo a questo account, a un gruppo o a tutti gli account. Vedi [connessione e proxy](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/) e [proxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md).

## Extra

Opzionale: bastano un account e delle fonti per iniziare a raccogliere dati. Solo l’opzione che scegli aprirà le relative impostazioni; nulla viene collegato automaticamente. La scheda **«Livello di protezione»** nella parte superiore mostra la [modalità di protezione](https://phishdestroy.github.io/TgWitness/it/docs/reference/panel/#protection-modes).

| Scheda | Cosa offre in più | Guida |
| --- | --- | --- |
| Archiviazione e spazio su disco | Backup, trasferimento dei file più vecchi sul cloud, una copia probatoria che non può essere cancellata | [Archiviazione](https://phishdestroy.github.io/TgWitness/it/docs/reference/storage/) |
| Obiettivo e livello di protezione | Impostazioni consigliate per il tuo obiettivo e due scale | [di seguito](https://phishdestroy.github.io/TgWitness/it/docs/reference/panel/#goal-and-protection-level) |
| Notifiche | Problemi, messaggi modificati e un riepilogo giornaliero; il tuo bot di controllo personale | [di seguito](https://phishdestroy.github.io/TgWitness/it/docs/reference/panel/#notifications) |
| Prove e backup | Timestamp, ulteriori testimoni e una copia crittografata fuori sede | [di seguito](https://phishdestroy.github.io/TgWitness/it/docs/reference/panel/#evidence-and-backups) |
| Server attivo 24 ore su 24, 7 giorni su 7 | Un server cloud senza SSH, creato ed eliminato dal pannello di controllo | [Elevata affidabilità](https://phishdestroy.github.io/TgWitness/it/docs/reference/high-assurance/#from-the-panel) |
| Testimone indipendente | Controlli firmati pubblicati sul tuo canale Telegram o su Discord | [Witness](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/) |
| Controllo del codice | Confronta il programma in esecuzione con un commit pubblico su GitHub | [di seguito](https://phishdestroy.github.io/TgWitness/it/docs/reference/panel/#code-check) |

### Obiettivo e livello di protezione

Quattro domande:

1. **A cosa serve? Per** una documentazione personale, un'indagine o come prova in un caso.
2. **Quanto intendi monitorare?** Poche chat (fino a circa 50), molte chat (fino a circa 500) o interi account. Questo imposta il limite dell’elenco delle chat a 1.000, 3.000 o 20.000.
3. **Foto e file?** Solo testo, foto e file multimediali di piccole dimensioni (foto fino a 20 MB, video fino a 100 MB), oppure tutto (video e documenti fino a 1 GB ciascuno). L’opzione “Tutto” con account completi mantiene inoltre 4 GiB di spazio libero su disco.
4. **Dove verrà eseguito?** Su questo computer o su un server sempre attivo.

Il suggerimento elenca i timestamp indipendenti, il drand e l’elenco dei dispositivi di Telegram, ciascuno corredato da una riga che ne descrive la funzione. I timestamp vengono generati ogni 60, 30 o 10 minuti per una registrazione personale , un’indagine o una prova; il drand e l’elenco dei dispositivi richiedono i timestamp. **Applicare** le modifiche solo a questi elementi, alla politica sugli allegati e ai due parametri sopra indicati. Ogni modifica costituisce una registrazione nel registro, oltre a `setup.applied`. Notifiche, una copia fuori sede, un server, il DNS del gateway, il controllo del codice e un testimone vengono proposti come passaggi successivi con i rispettivi moduli.

Due scale vengono calcolate in base a quanto impostato, non all’obiettivo:

| Scala | Punti |
| --- | --- |
| Credibilità | Diario firmato 1, timestamp 3, drand 1, elenco dispositivi 1, verifica del codice corrispondente 1, polling dei testimoni 1, server certificato 2, log DNS del gateway 1 |
| Affidabilità | Server sempre attivo 3, copia off-site 3, Object Lock 1, notifiche di problemi 1 |

L'80% o più corrisponde **al livello massimo**, il 50% **a quello alto**, il 25% **a quello moderato**, mentre al di sotto di tale soglia si considera **il livello base**. L'affidabilità attualmente tiene conto di un server sempre attivo in base alla risposta alla domanda 4, prima che venga verificato qualsiasi server.

### Notifiche

Le notifiche vengono inviate tramite Apprise a Telegram, Discord, Slack, ntfy, e-mail, Matrix e oltre 100 altri servizi. Scegli un servizio, compila uno o due campi e invia un test, oppure incolla direttamente gli indirizzi di Apprise.

- **Problemi**: disco quasi pieno, account disconnesso, errori relativi a raccolta, copia o timestamp. Su un server sigillato, anche una porta SSH aperta o un accesso rappresentano un problema.
- **Modifiche**: messaggi eliminati, modificati e mancanti nelle chat monitorate, raggruppati in una singola notifica per ogni controllo (ogni minuto, salvo diversa impostazione nei Parametri).
- **Attività completate**: cronologia, esportazioni e copie di archiviazione.
- **Riepilogo giornaliero** all’ora prescelta, secondo l’ora del server.

Le notifiche riportano i nomi delle chat e il numero di messaggi. Gli estratti dei messaggi sono disattivati per impostazione predefinita; se sono attivati, il testo dei messaggi esce da questo dispositivo.

**Il tuo bot operatore** è un bot personale creato tramite @BotFather che risponde `/status` e `/stats`, e, facoltativamente, `/pause`, `/resume` e `/copy`. Solo la chat indicata e gli ID utente di Telegram elencati possono utilizzarlo; il testo della conversazione rimane nell’area di lavoro. Utilizza un bot separato se un’altra applicazione riceve già i suoi comandi. Vedi [notifiche](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md) e [bot operatore](https://phishdestroy.github.io/TgWitness/it/docs/reference/storage/#operator-bot-and-completion-notices).

### Prove e backup

- **I timestamp indipendenti** inviano solo l’SHA-256 di ciascun checkpoint firmato alle autorità RFC 3161 e ai calendari OpenTimestamps, ogni 5-1.440 minuti. **Anchor ora** esegue un ciclo. Vedi [i timestamp](https://phishdestroy.github.io/TgWitness/it/docs/reference/timestamp/).
- **Altri testimoni**, ciascuno inattivo finché non viene selezionato: l’ultimo round di drand, l’elenco di Telegram dei dispositivi connessi senza indirizzi IP e il log di Cloudflare Gateway relativo alle query DNS del server. Vedi [i registri opzionali](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices).
- **Il backup crittografato** copia il diario, i file, i checkpoint e le esportazioni delle chat su un archivio compatibile con S3 (Wasabi, Amazon S3, Backblaze B2, Cloudflare R2, MinIO). Tutto viene prima crittografato su questa macchina. **Scarica la chiave di crittografia** e conservala in un luogo separato: senza di essa la copia non può essere letta. Object Lock in modalità Governance o Compliance impedisce la cancellazione degli oggetti per un numero prestabilito di giorni. Vedi [copia off-site](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md).

### Controllo del codice

Verifica se il programma installato corrisponde a una versione pubblicata.

1. Inserisci un repository GitHub (quello ufficiale è già precompilato) e un tag, un ramo o un commit.
2. **Check now** interroga l’API di GitHub, tramite la route di questo spazio di lavoro per le richieste esterne, per ottenere l’elenco dei file di quel commit. Confronta l’ID blob git di ogni file di programma analizzato con il commit. Un checkout da Windows con terminazioni di riga convertite risulta comunque compatibile.
3. Il risultato elenca i file modificati, aggiuntivi e mancanti (fino a 50 per ciascuna categoria) e viene salvato come un `source.checked` registro di diario.

Il risultato è considerato aggiornato solo finché i file del programma in esecuzione rimangono invariati: ricontrollare dopo un aggiornamento. Non è necessario alcun token e funzionano solo i repository pubblici; le chat e le credenziali non vengono caricate. Una corrispondenza identifica il codice presente sul disco. Non si tratta di un’attestazione hardware; per quella, consultare [Phala Cloud](https://phishdestroy.github.io/TgWitness/it/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx).

## Modalità di protezione

Il selettore accanto al numero di versione mostra la modalità selezionata e quanti dei 18 livelli di protezione sono attivi, ad esempio `🟠 Witnessed 9/18`. **Per cambiare modalità**, in **«Extras» → «Livello di protezione»** si apre il menu di selezione. Ogni modalità descrive un obiettivo e elenca ciò che manca ancora; la registrazione, la firma e le impostazioni salvate sono le stesse in ogni modalità.

| Modalità | Per | Aggiunge |
| --- | --- | --- |
| 🟢 Facile | Monitorare una chat e conservarne una copia | Chat, il diario e le esportazioni delle chat; la firma avviene in background |
| 🟡 Firmato | Segnala a una piattaforma, a un host o a un servizio di segnalazione degli abusi | Archivio firmato, verifica del registro, punti di controllo, estratto di passaggio di consegne |
| 🟠 Testimoniato | Casi in cui qualcuno potrebbe sostenere che il record sia stato modificato | Un testimone indipendente che pubblica le intestazioni del registro firmate |
| 🔴 Pronta per l’uso in tribunale | Prove per un avvocato, la polizia o un tribunale | Timestamp, una copia crittografata conservata in un luogo esterno, dettagli del caso nei report |
| 🟣 Verificato da GitHub | Registrazioni il cui software deve poter essere verificato da chiunque | Controllo del codice e acquisizione di GitHub Actions |
| ⚫ Mossad | Casi di grande rilevanza contro un avversario ben finanziato | Un server protetto attivo 24 ore su 24, 7 giorni su 7, un indirizzo IP nascosto, tutti i 18 livelli |

I livelli: ogni registrazione firmata e concatenata; una ricevuta di esecuzione firmata; allegati salvati con SHA-256; checkpoint firmati; ricontrolli; avvisi di problemi; accesso di sola lettura per i testimoni; un testimone che effettua controlli a intervalli regolari; timestamp RFC 3161; prove OpenTimestamps; un timestamp più recente verificato; una copia crittografata fuori sede; dettagli del caso nei rapporti; un controllo di corrispondenza del codice ; Telegram non vede mai l’IP di questa macchina; richieste esterne tramite un proxy; Object Lock sulla copia; un server sigillato con i registri del provider. Un livello disattivato presenta **l’opzione “Configura”**, che apre il relativo modulo. La scelta di una modalità inferiore richiede conferma e non elimina nulla.

## Altri strumenti

**Extras → Independent capture**: connect a separate browser or AyuGram recorder, pin its signing key, select capture options, start/pause, take snapshots and download verified signed archives. Each recorder has its own manual login, route, journal and key. Both connections start disabled. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md).

- **Consulta l’archivio**: cerca le osservazioni salvate, esamina le fonti, quindi decidi se inviarle a un modello di IA. Vedi [l’analisi dell’archivio](https://phishdestroy.github.io/TgWitness/it/docs/reference/analysis/) e [l’OCR e la trascrizione locali](https://phishdestroy.github.io/TgWitness/it/docs/reference/media-analysis/).
- **Parametri**: limiti e frequenza di raccolta, ricontrolli, download, profili, notifiche ed esportazioni. Ricerca per nome, mostra **«Solo** valori **modificati»** e prepara le impostazioni predefinite come bozza con **«Ripristina impostazioni predefinite…». «Salva parametri»** applica i valori dal loro prossimo utilizzo, e ogni modifica viene registrata nel registro.
- **Accesso**: token distinti per revisori, analisti e operatori, limitati a determinati spazi di lavoro, chat e diritti. Vedi la sezione "[Accesso"](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/).
- **Log di sistema** : attività svolte da questo processo dal suo avvio (connessioni, modifiche al proxy, accessi, rifiuti, modifiche alle impostazioni) con gli indirizzi IP nascosti. L’opzione **“Segui nuove righe”** mantiene visibile la riga più recente. I messaggi rimangono solo nel registro.
- **Integrazioni**: il provider di IA, connessioni [MCP in sola lettura](https://phishdestroy.github.io/TgWitness/it/docs/reference/mcp/) e [webhook firmati](https://phishdestroy.github.io/TgWitness/it/docs/reference/webhooks/).
- **Case Board**: note private del team, segnalibri e estratti accanto alle prove. Vedi [Case Board](https://phishdestroy.github.io/TgWitness/it/docs/reference/case-board/).
- **Acquisizioni di GitHub Actions** in Esportazioni: una chat acquisita dal tuo fork. Vedi [acquisizione sigillata](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md).
