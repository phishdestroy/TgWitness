# Come funziona la raccolta dei dati

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/

Ambito di osservazione, aggiornamenti in tempo reale, ricontrolli, allegati, azioni intraprese e significato delle lacune, record per record.

TgWitness registra ciò che un account Telegram connesso osserva. Il registro conserva tali osservazioni, la loro sequenza e il contesto ad esse associato. Non deduce azioni non visibili dalla mancanza di un messaggio o dal fatto che un account sia connesso.

## Dall’accesso al registro

Diagramma di flusso · Autorizzare un account utente → Selezionare gruppi e canali accessibili; Selezionare gruppi e canali accessibili → Salvare le impostazioni relative agli eventi e agli allegati; Salvare le impostazioni relative agli eventi e agli allegati → Avviare l’osservazione; Avviare l’osservazione → Riceva gli aggiornamenti dal client attivo; Riceva gli aggiornamenti dal client attivo → Applicare la politica relativa alle fonti e agli eventi; Applicare la politica relativa alle fonti e agli eventi → Aggiungere un’osservazione firmata; Aggiungere un’osservazione firmata → Visualizzare o esportare il registro; Aggiungere un’osservazione firmata → Elaborare qualsiasi allegato in coda; Elaborare qualsiasi allegato in coda → Allegare il risultato del download · Autorizzare un accountutente · Selezionare gruppi ecanali accessibili · Salvare leimpostazioni relativeagli eventi e agliallegati · Avviare l’osservazione · Riceva gliaggiornamenti dalclient attivo · Applicare la politicarelativa alle fonti eagli eventi · Aggiungereun’osservazionefirmata · Visualizzare oesportare il registro · Elaborare qualsiasiallegato in coda · Allegare il risultatodel download

**Diagramma sotto forma di testo**

1. Autorizzare un account utente → Selezionare gruppi e canali accessibili
2. Selezionare gruppi e canali accessibili → Salvare le impostazioni relative agli eventi e agli allegati
3. Salvare le impostazioni relative agli eventi e agli allegati → Avviare l’osservazione
4. Avviare l’osservazione → Riceva gli aggiornamenti dal client attivo
5. Riceva gli aggiornamenti dal client attivo → Applicare la politica relativa alle fonti e agli eventi
6. Applicare la politica relativa alle fonti e agli eventi → Aggiungere un’osservazione firmata
7. Aggiungere un’osservazione firmata → Visualizzare o esportare il registro
8. Aggiungere un’osservazione firmata → Elaborare qualsiasi allegato in coda
9. Elaborare qualsiasi allegato in coda → Allegare il risultato del download

L’autorizzazione, l’accesso a una fonte, un collettore in esecuzione e la consegna completa sono questioni distinte. Un accesso riuscito non garantisce l’accesso a tutti i gruppi. Una connessione attiva non garantisce che ogni aggiornamento rilevante sia pervenuto.

## Ambito di monitoraggio: chat selezionate, una cartella o l’intero account

Fonti → **L’ambito di osservazione** determina quali chat vengono registrate in un’area di lavoro.

| Modalità | Registrazioni | Nuove chat |
| --- | --- | --- |
| Chat selezionate (impostazione predefinita) | Solo le chat che aggiungete manualmente | Non viene mai aggiunto automaticamente |
| Cartella Telegram | Chat presenti in una delle cartelle dell’account: chat incluse in base al nome, più le categorie della cartella (contatti, non contatti, gruppi, canali, bot), meno le chat escluse e, se la cartella lo specifica, le chat archiviate | Le chat corrispondenti vengono aggiunte non appena diventano attive; le chat che si aggiungono alla cartella in Telegram vengono acquisite entro un’ora |
| Account completo | Ogni chat a cui l’account ha accesso | Ogni nuova chat, gruppo, chat privata o bot viene aggiunto non appena viene registrato il suo primo aggiornamento |

- **I tipi di fonte** (canali, gruppi, chat private, bot) restringono le modalità «cartella» e «intero account». Le chat selezionate possono essere di qualsiasi tipo, comprese le chat private e i bot.
- **Le chat escluse** non vengono mai registrate, in nessuna modalità. Nelle modalità «Cartella» e «Intero account», *le operazioni «Escludi»* e *«Rimuovi»* su una fonte la inseriscono in questo elenco, in modo che il filtro non la aggiunga nuovamente. Selezionando nuovamente la chat manualmente (in «Fonti» o da «Chat») essa viene rimossa dall’elenco. L’elenco può contenere fino a 5.000 chat; superato tale limite, l’*operazione «Rimuovi»* non viene accettata e la chat può invece essere messa in pausa.
- **Azioni proprie** (attivate per impostazione predefinita): i messaggi inviati da questo account, le relative modifiche e le pressioni dei tasti della tastiera di risposta. Se disattivata, i messaggi in uscita e le modifiche vengono ignorati.
- Il passaggio a una cartella o all’intero account richiede una conferma: queste modalità registrano le chat private e i messaggi di terzi e devono essere utilizzate esclusivamente su un account dedicato. La conferma e ogni modifica dell’ambito di applicazione sono registrazioni firmate con `scope.changed`.
- Le chat aggiunte dall’ambito di analisi compaiono come fonti contrassegnate come *«auto»*, registrate come `scope.applied` (all’avvio e ogni ora) o `source.discovered` (una nuova chat durante il monitoraggio). Il ritorno alle chat selezionate mette in pausa ogni fonte aggiunta automaticamente.

Cosa non è possibile fare con queste modalità:

- **Le chat segrete** sono crittografate end-to-end tra due dispositivi e non raggiungono mai TgWitness, in nessuna modalità.
- **Non viene registrato nulla quando TgWitness non è in esecuzione.** Dopo un riavvio, l’applicazione richiede a Telegram gli aggiornamenti mancanti e ricontrolla le chat, ma Telegram non restituisce tutti i dati dopo lunghe interruzioni di servizio. I rapporti e `verify.py` mostrano tali periodi come lacune (vedere [la copertura](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)).
- All’inizio vengono elencate solo le prime 1.000 conversazioni (il limite è indicato **nella sezione «Parametri»**); le chat più vecchie vengono aggiunte non appena tornano attive. La cronologia precedente di una chat aggiunta non viene recuperata: si consiglia di effettuare un’ istantanea della cronologia o un’esportazione completa della chat quando necessario.
- Le condizioni delle cartelle soggette a continue variazioni (silenzioso, letto) non vengono applicate: tali chat rimangono sotto osservazione.
- **I pulsanti del bot in linea (callback)** premuti in un’altra app risultano invisibili a una seconda sessione; la risposta o la modifica del bot viene registrata. Le pressioni dei tasti di risposta arrivano come messaggi in uscita e sono contrassegnate con il codice `button_press`.
- Un numero maggiore di chat comporta un numero maggiore di richieste. Telegram limita gli account in caso di volumi che ritiene eccessivi, il che costituisce un motivo in più per utilizzare account dedicati.

## Ambito di applicazione e selezione degli eventi

Ogni area di lavoro dispone delle proprie fonti. TgWitness non si unisce ai gruppi, non accetta inviti né elenca automaticamente tutti i membri. Le fonti devono essere già accessibili all’account. All’avvio, il collettore verifica le fonti selezionate rispetto alle conversazioni visibili dell’account; vengono esaminate le prime 1.000 conversazioni, salvo diversa indicazione **nella sezione Parametri → Chat letta dall’elenco dell’account**. Una fonte assente viene contrassegnata **come «accesso non confermato»**, senza che si presuma che l’utente sia stato rimosso.

| Contesto | Raccoglie | Effetto in caso di disattivazione |
| --- | --- | --- |
| Nuovi messaggi | Messaggi ordinari inviati | Le modifiche o le cancellazioni successive potrebbero non avere testo acquisito in precedenza con cui effettuare un confronto. |
| Modifiche | Versioni modificate dei messaggi fornite | Le modifiche intermedie non vengono ricostruite in un secondo momento. |
| Cancellazioni | Notifiche di cancellazione con ambito specifico e notifiche a livello di account senza ambito specifico | Le notifiche di cancellazione non vengono aggiunte al registro. |
| Reazioni | Istantanee delle reazioni fornite | Non vengono aggiunti aggiornamenti separati relativi alle reazioni. |
| Iscrizione | Invio di messaggi relativi al servizio di abbonamento e aggiornamenti ai partecipanti | Tali osservazioni relative all’iscrizione non vengono aggiunte. |

Le impostazioni si applicano a tutte le fonti selezionate nell’area di lavoro. Salvi il modulo per applicare le modifiche; queste vengono registrate con valori «prima» e «dopo» firmati. La disattivazione di una categoria non comporta la rimozione dei record precedenti. La sua riattivazione non recupera gli aggiornamenti mancanti.

I registri operativi e altri eventi relativi ai servizi di gruppo rimangono distinti da queste impostazioni. I messaggi relativi al servizio di iscrizione possono generare registrazioni dei messaggi quando l’iscrizione è abilitata, anche se la normale acquisizione dei nuovi messaggi è disabilitata. Gli oggetti Telegram acquisiti conservano i metadati incorporati; un’impostazione non costituisce una regola di oscuramento.

**Le cancellazioni nelle chat private e nei gruppi ordinari** vengono registrate come ID dei messaggi senza una chat associata. Queste chat condividono un’unica sequenza di ID dei messaggi a livello di account; pertanto, quando un messaggio con quell’ID è stato salvato in precedenza, la relativa chat è nota: la cancellazione viene registrata in quella chat con `chat_resolution` che ne spiega il funzionamento. Gli ID mai salvati rimangono una **cancellazione senza ambito** con una fonte esplicitamente sconosciuta; il collettore non formula ipotesi. Telegram non indica mai chi abbia cancellato un messaggio; quando il messaggio cancellato è stato inviato da questo account, la registrazione lo indica (`deleted_message_was_outgoing`) senza nominare chi ha effettuato la cancellazione.

## Azioni proprie

I messaggi inviati dall’account monitorato sono contrassegnati con `outgoing`. Una modifica di un messaggio in uscita indica che nelle chat private e nei gruppi solo il suo autore può modificarlo, mentre i post nei canali possono essere modificati da altri amministratori. Quando un messaggio in uscita ripete il testo di un pulsante presente nella tastiera delle risposte salvate più recenti in quella chat, viene contrassegnato con `button_press`, con un link al registro della tastiera.

L’esclusione delle proprie azioni si applica anche alle verifiche in background e alla cronologia automatica delle nuove chat. I messaggi in uscita saltati fanno avanzare la posizione di verifica, in modo che non possano bloccare i messaggi in arrivo successivi. Le azioni esplicite effettuate dal pannello e le istantanee della cronologia richieste manualmente rimangono registrate.

## Modalità di indagine: entrare a far parte di team e interagire con i bot

**Fonti → Ambito di osservazione → La modalità Investigazione** prepara l’ambito per un account dedicato che si unisce alle chat di gruppo, avvia i bot e invia messaggi a essi: l’intero account, ogni tipo di fonte, le proprie azioni e, per ogni chat o bot che compare, il relativo profilo e i suoi ultimi 200 messaggi visibili. Riveda il modulo e prema **«Salva ambito»**; il passaggio all’intero account richiede la consueta conferma.

- **Pulsanti.** I pulsanti presenti sotto un messaggio vengono conservati insieme ad esso e visualizzati nelle **chat**: link, app web, link di accesso, testi da copiare, dati di richiamata, query in linea, richieste di un numero di telefono o di una posizione. I link vengono visualizzati come testo e non vengono mai aperti dal pannello. Quando un bot modifica solo i pulsanti (ad esempio, un nuovo link di pagamento), si tratta di una nuova versione del messaggio, sia in caso di aggiornamenti in tempo reale che di ricontrolli.
- **Nuove chat e bot.** Nelle modalità «per cartella» e «intero account», **quando compare una nuova chat o un nuovo bot**, viene salvata immediatamente dopo la sua comparsa:

  - il suo profilo come record `source.profile`: descrizione del bot e comandi, il testo «Informazioni su» di un utente, gruppo o canale, membri, chat collegata e link di invito quando Telegram ne fornisce uno;
  - i suoi ultimi messaggi visibili (fino a 1.000) come istantanea della cronologia contrassegnata con `new_chat`: i messaggi precedenti di una chat di gruppo a cui si è appena aderito, oppure ciò che un bot ha detto prima che l’osservazione rilevasse la chat. I messaggi già salvati in tempo reale non vengono ripetuti.

  Le chat già presenti nell’elenco al momento dell’attivazione della modalità vengono aggiunte senza istantanee. Un FloodWait sospende questa operazione, che riprende successivamente; gli errori vengono registrati e la registrazione in tempo reale della chat prosegue. - **Profili su richiesta. Chat → Profilo → Salva profilo ora** salva il profilo corrente di qualsiasi fonte; quello più recente viene visualizzato sopra i messaggi. - **Non visibile.** I pulsanti in linea (callback) premuti in un’altra app Telegram, il popup o il link con cui un bot risponde a tale pressione, nonché i link di invito utilizzati in un’altra app non raggiungono TgWitness. Ciò che il bot invia o modifica successivamente viene registrato.

### Intervento dal panel

**La sezione «Chat»** include ora un mini-client che utilizza l’account Telegram dell’area di lavoro selezionata:

- Scriva un messaggio in testo semplice oppure selezioni **«Rispondi»** sotto un messaggio salvato. Il messaggio in uscita generato viene registrato anche quando l’ambito di analisi esclude gli aggiornamenti in uscita.
- Premere **il pulsante «Press»** sotto un pulsante di callback o di testo attivo. Il server recupera nuovamente il messaggio e rifiuta l’azione se la digitazione differisce dalla versione salvata. Le conferme di ricezione dei callback conservano il testo del popup di Telegram, il flag di avviso e l’URL; la risposta viene inoltre visualizzata sotto la conversazione. Gli URL rimangono testo selezionabile e non vengono aperti automaticamente.
- Espandere **il link «Apri Telegram**», inserire `@username`, un link pubblico `https://t.me/name`, `https://t.me/+invite` / `joinchat/invite` oppure un link bot con `?start=parameter`, quindi premere **«Salva anteprima**». Il link originale e l’anteprima di Telegram vengono firmati prima dell’adesione. **Entrare / aprire e osservare**: il sistema si unisce al gruppo/canale oppure apre l’utente/bot, aggiunge la chat come fonte abilitata e invia `/start` a un bot, includendone il parametro di avvio. Una richiesta di adesione in attesa dell’approvazione dell’amministratore viene registrata come “in sospeso”, non come adesione effettiva.

Attivare l’opzione **«Avvia osservazione**» per acquisire in tempo reale le risposte in arrivo. Le azioni del pannello funzionano anche quando l’osservazione è in pausa, ma in tal caso viene garantito il salvataggio solo delle risposte dirette. Le fonti appena aggiunte utilizzano il profilo configurato e l’acquisizione della cronologia quando l’osservazione è in esecuzione. Quando una fonte è in pausa, attivarla in **«Fonti»** prima di inviare messaggi o premere i relativi pulsanti.

`interaction.preview`, `interaction.requested` e `interaction.result` sono normali eventi del registro firmati inclusi nelle esportazioni delle prove. Le richieste identificano l’account, il messaggio/pulsante o il record di anteprima e indicano se l’osservazione era in esecuzione. Le conferme distinguono tra esito positivo, rifiuto, approvazione in sospeso e esito sconosciuto. Una richiesta interrotta potrebbe essere giunta a Telegram: si prega di controllare la chat prima di avviare una nuova azione. Il riutilizzo di un ID di richiesta consente di recuperare la relativa ricevuta salvata senza ripetere l’azione, anche dopo il riavvio. Il pannello conserva l’ ID in caso di risposta ambigua per la stessa azione durante la sessione corrente della pagina. Conserva inoltre tale ID quando l’aggiornamento della visualizzazione fallisce dopo un’azione riuscita: la ricevuta rimane visibile e, cliccandoci nuovamente, la si recupera. Gli RPC di callback e join dispongono di un unico tentativo; le letture riprovabili mantengono la politica di riprova configurata. Il passaggio a un’altra chat cancella immediatamente la bozza e il destinatario della risposta e disabilita l’invio fino al caricamento della nuova conversazione.

Questo mini-client gestisce i pulsanti di testo e di richiamata. Le app web, le richieste di accesso/numero di telefono/posizione, i pagamenti, le query in linea e gli allegati richiedono comunque un client Telegram; i metadati dei pulsanti salvati rimangono visibili. I nuovi controlli utilizzano testo in inglese.

## Livelli di ricontrollo

Le ricontrolli richiedono nuovamente a Telegram i messaggi mancanti, le modifiche e i messaggi che non vengono più restituiti. Le fonti contrassegnate da un asterisco sono fonti **prioritarie**, ricontrollate ogni 15 minuti per impostazione predefinita; tutte le altre fonti ogni 6 ore. Le chat selezionate partono come fonti prioritarie, mentre le chat aggiunte tramite una cartella o l’intero account vengono considerate come fonti regolari. Vengono ricontrollate al massimo 30 fonti per ciclo e le restanti attendono il minuto successivo; dopo una riconnessione, le fonti prioritarie vengono elaborate per prime. Entrambi gli intervalli sono impostati in Fonti → Impostazioni di registrazione → Ricontrollo (0 disattiva un livello) e vengono registrati come `recheck.changed`.

I messaggi mancanti vengono recuperati a partire dal punto in cui si era interrotto il ciclo precedente, fino a un massimo di **Parametri → nuovi messaggi per ricontrollo** (1.000 per impostazione predefinita) per ciclo. Dopo una lunga interruzione, la ricontrollo colma quindi l’intero intervallo mancante, anche quando i messaggi in tempo reale più recenti rispetto a tale intervallo sono stati salvati per primi. Una chat che sta ancora recuperando i messaggi viene ricontrollata nuovamente nel minuto successivo, anziché attendere il proprio intervallo di livello; `recheck.completed` mostra `continues_after` fino al completamento dell’operazione.

I confronti includono il testo dei messaggi, le entità, le sequenze di tastiera (compresa la cancellazione) e il contenuto/l’identità degli allegati. La semplice modifica degli hash di accesso ai file o dei riferimenti ai file non costituisce una modifica, né lo è ciò che Telegram inserisce autonomamente: il caricamento dell’anteprima di un link, le visualizzazioni delle storie, i contenuti multimediali a pagamento sbloccati da questo account, la ricezione di una fattura. Ogni versione salvata in «Chat» rimanda al relativo record completo nel registro, compresi i metadati dei contenuti multimediali.

## Cronologia dei messaggi e attribuzione

Supponiamo che il sistema di raccolta rilevi «Riunione alle 10:00», poi rilevi «Riunione alle 11:00» e infine riceva una notifica di cancellazione. Il sistema aggiunge tre osservazioni distinte: il testo originale rimane, la modifica costituisce una versione separata e la notifica registra che è stata rilevata una cancellazione.

Se la raccolta è iniziata dopo la scomparsa della prima versione, tale testo non è disponibile. Se sono state apportate diverse modifiche mentre il processo era offline, è possibile salvare solo le versioni osservate successivamente. Una notifica di cancellazione non consente di recuperare contenuti mai acquisiti.

Il mittente del messaggio non è automaticamente colui che lo ha modificato. Telegram solitamente non fornisce l’identità della persona che ha cancellato un messaggio né l’ora esatta della cancellazione. Gli attori sconosciuti rimangono tali. Le istantanee delle reazioni e gli aggiornamenti sui partecipanti contengono solo i conteggi e le identità che Telegram rende visibili all’account.

I numeri di sequenza indicano l’ordine di osservazione. Il timestamp UTC del collettore corrisponde al suo orologio locale; il timestamp originale di Telegram viene archiviato separatamente, qualora venga fornito. Nessuno dei due costituisce un timestamp indipendente e attendibile.

## Istantanee storiche

Uno snapshot richiede gli ultimi messaggi visibili da una fonte abilitata, fino a 500 per richiesta. I risultati vengono etichettati come osservazioni storiche. Possono sovrapporsi alla cattura in tempo reale e le osservazioni ripetute vengono conservate come record separati.

Le istantanee rispettano la politica relativa agli allegati, ma rimangono separate dagli eventi in tempo reale. Non ricostruiscono i messaggi cancellati né le versioni intermedie mancanti. È possibile richiederne una mentre il sistema è in pausa; eventuali allegati in coda attendono l’inizio dell’osservazione e l’esecuzione del processo di download.

## Gestione degli allegati

Il download degli allegati è attivo per impostazione predefinita e viene sospeso quando lo spazio libero su disco è inferiore a 1 GiB. Il collettore esegue contemporaneamente l’ osservazione dei messaggi e l’operazione di download. L’operazione conserva il descrittore multimediale originale e le impostazioni relative alle dimensioni, pertanto un allegato modificato in un secondo momento non viene sostituito in modo silenzioso.

I download vengono eseguiti dopo l’acquisizione dei messaggi. Un download completato genera un record `media.saved` con il relativo SHA-256 e il conteggio dei byte. Le operazioni saltate, fallite, riprovate e interrotte producono risultati distinti. Un’attività in coda non costituisce prova che il file sia stato conservato. Il file completato deve inoltre corrispondere al conteggio dei byte presente nel descrittore dell’allegato originale osservato. Una risposta breve o inaspettatamente lunga non viene registrata come contenuto multimediale conservato.

I limiti sono impostati **per tipo**: foto, video, GIF e animazioni, messaggi video circolari, messaggi vocali, musica e audio, adesivi e file. Ogni tipo può essere disattivato e presenta un proprio limite di dimensione compreso tra 1 e 2.000 MiB; i nuovi spazi di lavoro partono da 20 MiB per le foto, 100 MiB per i video, 50 MiB per file, audio e video circolari, 20 MiB per messaggi vocali e GIF e 5 MiB per gli adesivi. *La dimensione massima dei file* viene impostata contemporaneamente per ogni tipo. Le politiche salvate prima dell’ introduzione dei limiti per tipo mantengono il limite unico per ciascun tipo. La disattivazione di un tipo genera un record `media.skipped`; i file di dimensione sconosciuta o sovradimensionati non vengono scaricati. I file di grandi dimensioni ottengono una velocità di download di almeno 256 KiB/s. I processi sopravvivono al riavvio, ma i riferimenti scaduti, la perdita di accesso o i file eliminati possono comunque impedire il recupero. I processi esistenti mantengono la politica salvata insieme a essi.

## Messa in pausa, blocco, disconnessione e riavvio

| Azione o condizione | Effetto |
| --- | --- |
| Cambia area di lavoro | Modifica la visualizzazione del pannello; gli altri collettori mantengono il proprio stato. |
| Bloccare il pannello o chiudere una scheda | Il server e il sistema di monitoraggio rimangono attivi. |
| Osservazione in pausa | Interrompe il funzionamento di quel collettore e preserva il lavoro relativo agli allegati in coda. |
| Disattivare una fonte | Blocca la futura acquisizione mirata; i processi multimediali in coda relativi a tale funzione rimangono in attesa finché essa rimane disabilitata. |
| Rimuovere una fonte | Se lo si esclude come fonte e si eliminano i profili degli utenti, le registrazioni già salvate rimangono nel registro a scrittura sola. Gli allegati ancora in attesa vengono registrati come non riusciti (`source_removed`). Viene escluso anche nelle modalità «cartella» e «intero account». |
| Modificare il percorso di connessione | Richiede una pausa, chiude i client obsoleti e annulla gli accessi non completati. |
| Arrestare il processo Python | Blocca tutti gli spazi di lavoro; non vengono effettuate osservazioni mentre è offline. |
| Riavvio dopo un periodo di osservazione attiva | Tenta di riprendere l’ambito salvato utilizzando la sessione salvata. Una pausa manuale annulla tale intento. |

Il collettore registra le disconnessioni rilevate, i tentativi di ricollegamento, gli errori, gli avvii/arresti e gli heartbeat. Brevi interruzioni potrebbero sfuggire ai controlli periodici di connettività. Dopo un riavvio, gli aggiornamenti mancati vengono richiesti a partire dalla posizione di aggiornamento salvata e le chat monitorate vengono ricontrollate periodicamente; si veda [il formato delle prove](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#durable-collection-and-process-receipts-02). Un’istantanea fornisce il contesto; non dimostra che una lacuna sia stata colmata.

## Isolamento e verifica degli account

Ogni spazio di lavoro dispone di un proprio registro, autorizzazione, chiave di firma, politica e coda. Solo il suo client attivo può contribuire con osservazioni in tempo reale. I client rifiutati, in sospeso, sostituiti e quelli in fase di test di connessione non possono inserire aggiornamenti in tempo reale nel relativo registro. Account diversi possono osservare lo stesso gruppo, ma i loro registri rimangono separati.

Ogni evento include l’hash precedente e una firma Ed25519. Le esportazioni coprono l’ intero registro dell’area di lavoro tramite un numero di sequenza fisso. I filtri del pannello non filtrano l’esportazione; la raccolta può proseguire oltre i suoi limiti mentre è in fase di preparazione.

**Il registro di verifica** controlla la catena di eventi e le firme entro i limiti visualizzati. Il risultato viene azzerato quando l’area di lavoro cambia e il pannello identifica i nuovi record aggiunti dopo la verifica. L’esportazione in formato ZIP verifica anche i file multimediali raccolti.

Una firma valida attesta l’integrità rispetto alla chiave fidata, non l’origine da Telegram né la veridicità del contenuto. Conservare le impronte digitali e i punti di controllo in modo indipendente. Si veda il [modello probatorio](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/), [le operazioni quotidiane](https://phishdestroy.github.io/TgWitness/it/docs/reference/operations/) e [la procedura di accettazione in tempo reale](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) per i requisiti di affidabilità e consegna.
