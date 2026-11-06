# Accesso e autorizzazioni

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/access/

Configurare l’accesso limitato agli account e alle chat, selezionare le autorizzazioni, limitare le sessioni e gli indirizzi IP e revocare l’accesso.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/it/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

Conceda a un revisore l’accesso a una chat, a un analista l’autorizzazione a esportare un caso o a un operatore il controllo su account selezionati. A ciascuna persona viene assegnato un proprio token. Il token del pannello principale rimane in possesso dell’amministratore.

[Configurazione dell’account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/) · [Percorsi di connessione](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/) · [Modello di sicurezza](https://phishdestroy.github.io/TgWitness/it/docs/reference/security/)

## Due ambiti di applicazione, due ruoli distinti

**L’ambito di raccolta** determina cosa viene registrato per un account: chat selezionate, una cartella di Telegram o l’intero account. **L’ambito di accesso** determina quali di tali account e chat registrati un’altra persona possa visualizzare e utilizzare. Concedere l’accesso non comporta l’adesione a una chat di Telegram, l’avvio della raccolta né la concessione di autorizzazioni sull’account Telegram.

Un'autorizzazione può consentire l'accesso a spazi di lavoro selezionati, a chat selezionate al loro interno, a tutti gli spazi di lavoro o a tutti gli account di un [gruppo di account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#bulk-import-and-account-groups). L'accesso **a tutti gli spazi di lavoro, compresi quelli aggiunti in seguito**, copre anche gli account futuri. Anche l'accesso a un gruppo copre gli account aggiunti successivamente a quel gruppo. Selezionare esplicitamente gli spazi di lavoro quando un caso deve rimanere limitato a essi.

## Concedere l’accesso a qualcuno

1. Acceda come amministratore principale e apra la sezione **«Accesso**».
2. Nella sezione **«Concedi l’accesso a qualcuno**», inserisca un nome che potrà riconoscere nel registro.
3. Selezionate gli spazi di lavoro e, se necessario, le singole chat.
4. Selezionare ciò che questa persona potrebbe fare. L’azione **«Visualizza»** è sempre inclusa.
5. Impostare la scadenza, i limiti di accesso/sessione e gli indirizzi consentiti secondo necessità.
6. Clicchi su **«Crea accesso**». Copi subito il token: viene visualizzato una sola volta.
7. Invii l’indirizzo del pannello e il token in privato. Il destinatario inserisce tale token nella normale pagina di accesso; non ha bisogno del Suo token principale del pannello né di una sessione Telegram.

Apra il pannello con il token generato in una sessione separata del browser e verifichi le chat visibili e le azioni consentite prima di consegnarlo.

## Selezionare le autorizzazioni

Per una dimostrazione pubblica solo testuale, utilizzare **la “Vetrina pubblica”** anziché il normale accesso per i revisori. Mostra i canali pubblici esplicitamente selezionati, le modifiche e le cancellazioni conservate e le statistiche firmate, con i campi dell’autore oscurati e i file chiusi al confine dell’API. [Creare e verificare una vetrina](https://phishdestroy.github.io/TgWitness/it/docs/reference/showcase/).

| Autorizzazione | Cosa consente |
| --- | --- |
| `view` | È possibile consultare le chat autorizzate, i messaggi acquisiti, i profili, i file e le voci filtrate del registro. Sempre inclusi. |
| `export` | È consentita l’esportazione della cronologia delle chat e dei dossier. L’esportazione delle prove relative all’intero spazio di lavoro richiede l’accesso all’intero spazio di lavoro. |
| `sources` | Gestione delle fonti, delle istantanee e dell’acquisizione dei profili. L’accesso limitato alle chat consente di operare solo sulle chat autorizzate; l’individuazione delle fonti a livello di account e le impostazioni relative all’ambito di applicazione rimangono disattivate. |
| `collect` | Avviare o arrestare un collettore. Richiede l’accesso all’intero spazio di lavoro poiché la raccolta influisce sull’account. |
| `interact` | Eseguire le interazioni supportate su Telegram entro i limiti dell’ambito di accesso. L’accesso limitato alla chat non consente di utilizzare l’anteprima dei link a livello di account. |
| `settings` | Modifica le impostazioni di raccolta, i timestamp, le notifiche, le copie fuori sede e i parametri. Richiede l’accesso all’intero spazio di lavoro. |
| `account` | Accedete o disconnettetevi da Telegram e gestite i percorsi di connessione. Richiede l’accesso all’intero spazio di lavoro. |
| `board.read` | Leggere le note della bacheca dei casi solo all’interno dell’area di lavoro e delle chat autorizzate. |
| `board.write` | Aggiungere segnalibri, evidenziazioni, sezioni, commenti e stati di apertura/revisione. Richiede inoltre l’`board.read`. |
| `board.manage` | Gestire le raccolte, gli stati finali del team e le schede degli altri partecipanti. Richiede inoltre i diritti di lettura/scrittura sulla scheda. |

Le autorizzazioni e l’ambito di applicazione vengono verificati congiuntamente. La selezione di un’autorizzazione non comporta l’apertura di altre chat né sblocca un’operazione a livello di spazio di lavoro in caso di accesso limitato a una singola chat. Per un’esportazione parallela, l’accesso deve coprire la chat esportata in ogni account selezionato. Un accesso concesso non può creare nuovi accessi, gestire le sessioni di altre persone né aprire la console di amministrazione.

### Tre configurazioni utili

| Persona | Ambito di applicazione | Autorizzazioni |
| --- | --- | --- |
| Revisore | Chat registrate relative a un caso | `view` |
| Analista che prepara il passaggio di consegne | Le chat da esaminare ed esportare | `view`, `export`; aggiungere `interact` solo qualora debbano agire tramite Telegram |
| Operatore addetto alla raccolta | Spazi di lavoro completi selezionati | `view`, `sources`, `collect`; aggiungere `settings` o `account` solo se necessario |

Le impostazioni predefinite iniziali del modulo Access includono anche Case Board: il revisore può leggere, l’analista può leggere e scrivere, mentre l’operatore può gestirlo. Le impostazioni predefinite rimangono modificabili e le autorizzazioni esistenti non vengono automaticamente estese. Vedere [Case Board](https://phishdestroy.github.io/TgWitness/it/docs/reference/case-board/) per gli ambiti di chat ereditati e la privacy delle esportazioni.

## Limiti e sessioni

| Contesto | Come funziona |
| --- | --- |
| Sessioni parallele | Limitare le sessioni simultanee a un numero compreso tra 1 e 100. Al raggiungimento del limite, rifiutare il successivo accesso o terminare la sessione più vecchia. |
| È consentito l’accesso | Limitare il numero di utilizzi consentiti del token per avviare le sessioni. Le sessioni esistenti non vengono interrotte semplicemente perché è stato utilizzato l’ultimo accesso consentito. |
| Valido fino al | Scadenza definitiva dell’accesso. Un accesso scaduto non può effettuare l’accesso né continuare a inviare richieste. |
| Minuti di inattività | Timeout di inattività della sessione, da 5 minuti a 30 giorni. Le richieste andate a buon fine lo prolungano; un pannello aperto può mantenersi attivo tramite polling. |
| Indirizzi consentiti | Accettare indirizzi IP specifici o sottoreti CIDR. Lasciare vuoto per consentire qualsiasi indirizzo, a meno che non sia abilitato il vincolo al primo accesso. |
| Collegamento al primo accesso | Il primo accesso effettuato con esito positivo stabilisce l’indirizzo autorizzato per tale accesso. |

L’IP è l’indirizzo del client rilevato dall’applicazione. Se si utilizza un proxy inverso o un tunnel, si prega di verificare l’indirizzo visualizzato nella sezione **«Sessioni aperte»** prima di fare affidamento sulle regole relative all’IP: in caso contrario, potrebbe sembrare che diversi utenti condividano l’indirizzo del proxy.

## Modificare o revocare l’accesso

Modifica una voce nella sezione **«Accesso concesso»** per modificarne l’ambito, le autorizzazioni o i limiti. Le modifiche all’ambito e alle autorizzazioni vengono verificate nelle richieste successive, comprese quelle provenienti da sessioni già aperte. La revoca di un accesso termina le relative sessioni e rende inutilizzabile il token emesso. **La funzione «Sessioni aperte»** consente inoltre all’amministratore di terminare una singola sessione senza revocare l’intero accesso.

Le copie di esportazione salvate mantengono il nome del creatore, l’area di lavoro, l’ambito della chat e le autorizzazioni richieste. Un utente a cui è stato concesso l’accesso può visualizzare o scaricare le proprie copie solo finché tali autorizzazioni sono valide; le copie contenenti il Case Board richiedono inoltre l’autorizzazione «`board.read`». L’amministratore può recuperare tutte le copie. Le copie più vecchie prive di questi metadati e i pacchetti di gruppo sono accessibili solo all’amministratore. I ticket di download e le risposte con file preparati verificano nuovamente l’accesso dopo la preparazione del file, prima di inviarne i byte.

La revoca non consente di recuperare i file che sono già stati scaricati da qualcuno. La disconnessione, il blocco del pannello o la chiusura di una sessione non arrestano un collettore in esecuzione.

## Cosa può visualizzare l’amministratore

I revisori e gli analisti ricevono informazioni sullo stato di avanzamento della raccolta senza endpoint proxy, diagnostica del pool, percorsi dei server o errori di connessione grezzi. La diagnostica della connessione richiede l’autorizzazione `account` sull’intero spazio di lavoro. La lettura delle notifiche, della copia fuori sede e delle impostazioni dei parametri richiede l’autorizzazione `settings`.

Le stringhe complete del browser User-Agent non vengono conservate nelle sessioni di accesso. Un aggiornamento le rimuove anche dalla cache mutabile della sessione. Il log del processo del pannello maschera gli indirizzi IP letterali, le credenziali URL e i segreti etichettati. I log dei servizi locali e i record di registro precedentemente firmati non vengono riscritti. Le regole di accesso e i record di accesso firmati continuano a utilizzare l'indirizzo del client.

### Sostituire la chiave principale

Utilizzare **Access → I miei limiti → Riemetti chiave amministratore**, oppure eseguire `tgwitness token rotate` da un'installazione gestita mentre il pannello è in esecuzione. Tutte le sessioni del browser esistenti terminano, comprese quelle aperte con i token dei colleghi. Il browser richiedente riceve una nuova sessione; salvare la nuova chiave amministratore prima di nasconderla. I token dei colleghi emessi rimangono validi fino a quando non vengono revocati separatamente. Un'installazione che utilizza `TGWITNESS_TOKEN` deve modificare tale impostazione di ambiente e riavviare il sistema.

### Limiti delle richieste e del proxy

L’API ammette fino a 600 richieste al minuto per ogni IP client. Dieci autenticazioni rifiutate nell’arco di un minuto attivano un periodo di attesa esponenziale, da un secondo fino a cinque minuti. Un tentativo fallito dopo il periodo di attesa lo prolunga; dieci minuti senza tentativi falliti azzerano l’escalation. I rifiuti restituiscono i codici HTTP 429 e `Retry-After`. I limiti sono in memoria, condivisi tra gli spazi di lavoro in un unico processo del pannello; il riavvio li azzera. Gli streaming live sono limitati a quattro per token di supporto e a 32 per il processo del pannello. L’apertura di uno streaming consuma anche il budget di richieste API.

I corpi delle richieste hanno un limite di ricezione di 60 secondi (8 secondi per MCP). Ogni applicazione limita i corpi non completati a 32 richieste e 64 MiB di quota di percorso riservata. I corpi di dimensioni eccessive restituiscono il codice 413, quelli con timeout restituiscono il codice 408, mentre l’esaurimento della capacità dei corpi restituisce il codice 503 con `Retry-After`.

Le intestazioni IP inoltrate vengono ignorate a meno che il peer TCP effettivo non appartenga a `TGWITNESS_TRUSTED_PROXIES` (IP separati da virgola o CIDR). Impostare `TGWITNESS_PROXY_HEADER` su `x-forwarded-for` o `cf-connecting-ip`. L'XFF viene percorso dal proxy più vicino verso il primo peer non attendibile. I metadati degli indirizzi attendibili malformati o duplicati vengono rifiutati, pertanto non possono ereditare un indirizzo proxy inclusa nella lista dei permessi. Il tunnel rapido gestito si affida al connettore Cloudflare locale; la configurazione del dominio proprio si affida a Caddy locale. Le distribuzioni dirette, per impostazione predefinita, non si fidano di alcun proxy. Se si avvia Uvicorn autonomamente, disattivare l’elaborazione dell’intestazione proxy in modo che questo confine riceva il peer effettivo.

`TGWITNESS_PANEL_ALLOWED_IPS` limita l’accesso al pannello, compreso quello dell’amministratore, agli indirizzi IP o ai CIDR elencati. La sonda di identità di routing del programma di installazione rimane pubblica e non restituisce dati relativi all’account. Includere il percorso amministrativo locale richiesto prima di abilitare la lista bianca. La guida **START-HERE** per un’installazione gestita include le istruzioni per la configurazione del servizio e il ripristino.

Un selettore di query API `ws` deve identificare l'area di lavoro nel percorso della richiesta; i selettori sconosciuti, non corrispondenti o duplicati vengono rifiutati con codice di errore 404.

Gli script e gli stili dei pannelli contengono metadati di integrità SHA-384. Una mappa di importazione copre anche i moduli JS importati localmente nei browser che supportano l’integrità delle mappe di importazione. La risposta linguistica generata dinamicamente è separata. Questi controlli rilevano la sostituzione di risorse rispetto alla pagina fornita; non stabiliscono fiducia in un server compromesso in grado di sostituire sia la pagina che i relativi hash.

**Il registro, sin dall’avvio,** combina i log di processo con l’attività del registro proveniente da ogni area di lavoro: accessi, rifiuti, modifiche di percorso e azioni dell’operatore. Si tratta di una console in memoria per il processo in corso, non di una copia permanente di ogni messaggio. Gli eventi relativi ai messaggi più frequenti rimangono nel registro anziché riempire la console.

Anche il rilascio, la modifica e la revoca dell’accesso, nonché l’avvio o la chiusura delle sessioni, generano registrazioni firmate nel registro `access.*`. I token non sono inclusi in tali registrazioni. I token rilasciati e le credenziali di sessione vengono conservati sotto forma di hash nel deposito crittografato.

****Amministratore principale e confine di fiducia****

The main panel token remains unrestricted. Browser sign-ins with it create sessions subject to the administrator's configured session limits. Scripts sending the main token directly retain full access and are not counted as browser sessions.

This is application-level access control in one installation. All workspaces share the server process; this is not isolation from the host administrator. Keep the main token, Telegram sessions, signing keys and data directory private. A witness token is a separate checkpoint/health credential, not a panel access token.
