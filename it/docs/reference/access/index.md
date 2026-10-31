# Accesso e autorizzazioni

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/access/

Configurare l’accesso limitato agli account e alle chat, selezionare le autorizzazioni, limitare le sessioni e gli indirizzi IP e revocare l’accesso.

Conceda a un revisore l’accesso a una chat, a un analista l’autorizzazione a esportare un caso o a un operatore il controllo su account selezionati. A ciascuna persona viene assegnato un proprio token. Il token del pannello principale rimane in possesso dell’amministratore.

[Configurazione dell’account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/) · [Percorsi di connessione](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/) · [Modello di sicurezza](https://phishdestroy.github.io/TgWitness/it/docs/reference/security/)

## Due ambiti di applicazione, due ruoli distinti

**L’ambito di raccolta** determina cosa viene registrato per un account: chat selezionate, una cartella di Telegram o l’intero account. **L’ambito di accesso** determina quali di tali account e chat registrati un’altra persona possa visualizzare e utilizzare. Concedere l’accesso non comporta l’adesione a una chat di Telegram, l’avvio della raccolta né la concessione di autorizzazioni sull’account Telegram.

Un’autorizzazione può consentire l’accesso a spazi di lavoro selezionati, a chat selezionate all’interno di essi o a tutti gli spazi di lavoro. **Tutti gli spazi di lavoro, compresi quelli aggiunti in un secondo momento**, comprendono anche gli account futuri. Selezionare esplicitamente gli spazi di lavoro qualora un caso debba limitarsi a essi.

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

| Autorizzazione | Cosa consente |
| --- | --- |
| `view` | È possibile consultare le chat autorizzate, i messaggi acquisiti, i profili, i file e le voci filtrate del registro. Sempre inclusi. |
| `export` | È consentita l’esportazione della cronologia delle chat e dei dossier. L’esportazione delle prove relative all’intero spazio di lavoro richiede l’accesso all’intero spazio di lavoro. |
| `sources` | Gestione delle fonti, delle istantanee e dell’acquisizione dei profili. L’accesso limitato alle chat consente di operare solo sulle chat autorizzate; l’individuazione delle fonti a livello di account e le impostazioni relative all’ambito di applicazione rimangono disattivate. |
| `collect` | Avviare o arrestare un collettore. Richiede l’accesso all’intero spazio di lavoro poiché la raccolta influisce sull’account. |
| `interact` | Eseguire le interazioni supportate su Telegram entro i limiti dell’ambito di accesso. L’accesso limitato alla chat non consente di utilizzare l’anteprima dei link a livello di account. |
| `settings` | Modifica le impostazioni di raccolta, i timestamp, le notifiche, le copie fuori sede e i parametri. Richiede l’accesso all’intero spazio di lavoro. |
| `account` | Accedete o disconnettetevi da Telegram e gestite i percorsi di connessione. Richiede l’accesso all’intero spazio di lavoro. |

Le autorizzazioni e l’ambito di applicazione vengono verificati congiuntamente. La selezione di un’autorizzazione non comporta l’apertura di altre chat né sblocca un’operazione a livello di spazio di lavoro in caso di accesso limitato a una singola chat. Per un’esportazione parallela, l’accesso deve coprire la chat esportata in ogni account selezionato. Un accesso concesso non può creare nuovi accessi, gestire le sessioni di altre persone né aprire la console di amministrazione.

### Tre configurazioni utili

| Persona | Ambito di applicazione | Autorizzazioni |
| --- | --- | --- |
| Revisore | Chat registrate relative a un caso | `view` |
| Analista che prepara il passaggio di consegne | Le chat da esaminare ed esportare | `view`, `export`; aggiungere `interact` solo qualora debbano agire tramite Telegram |
| Operatore addetto alla raccolta | Spazi di lavoro completi selezionati | `view`, `sources`, `collect`; aggiungere `settings` o `account` solo se necessario |

Si tratta di esempi che è possibile configurare tramite le caselle di controllo relative alle autorizzazioni, non di ruoli fissi.

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

Modifichi una voce nella **sezione «Accessi»** per modificarne l’ambito, le autorizzazioni o i limiti. Le modifiche relative all’ambito e alle autorizzazioni vengono verificate nelle richieste successive, comprese quelle provenienti da sessioni già aperte. La revoca di un accesso termina le relative sessioni e rende inutilizzabile il token emesso. **La funzione «Sessioni aperte»** consente inoltre all’amministratore di terminare una singola sessione senza revocare l’intero accesso.

La revoca non consente di recuperare i file che sono già stati scaricati da qualcuno. La disconnessione, il blocco del pannello o la chiusura di una sessione non arrestano un collettore in esecuzione.

## Cosa può visualizzare l’amministratore

**Il registro, sin dall’avvio,** combina i log di processo con l’attività del registro proveniente da ogni area di lavoro: accessi, rifiuti, modifiche di percorso e azioni dell’operatore. Si tratta di una console in memoria per il processo in corso, non di una copia permanente di ogni messaggio. Gli eventi relativi ai messaggi più frequenti rimangono nel registro anziché riempire la console.

Anche il rilascio, la modifica e la revoca dell’accesso, nonché l’avvio o la chiusura delle sessioni, generano registrazioni firmate nel registro `access.*`. I token non sono inclusi in tali registrazioni. I token rilasciati e le credenziali di sessione vengono conservati sotto forma di hash nel deposito crittografato.

****Amministratore principale e confine di fiducia**** Il token del pannello principale rimane senza restrizioni. Gli accessi tramite browser effettuati con esso creano sessioni soggette ai limiti di sessione configurati dall’amministratore. Gli script che inviano direttamente il token principale mantengono l’accesso completo e non vengono conteggiati come sessioni del browser. Si tratta di un controllo degli accessi a livello di applicazione in un’unica installazione. Tutti gli spazi di lavoro condividono il processo del server; non si tratta di un isolamento dall’amministratore dell’host. Si raccomanda di mantenere riservati il token principale, le sessioni di Telegram, le chiavi di firma e la directory dei dati. Un token «witness» è una credenziale separata di controllo dello stato di integrità, non un token di accesso al pannello.
