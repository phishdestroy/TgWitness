# Flussi di lavoro e operazioni

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/operations/

Funzionamento quotidiano del pannello: modalità, categorie di monitoraggio, parametri, notifiche, esportazioni, backup e capacità.

Per la prima connessione, utilizzi [gli account e i formati di sessione](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/). Per una spiegazione delle versioni salvate, delle politiche relative agli eventi e delle lacune, consulti [la sezione dedicata al funzionamento della raccolta](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/). La presente guida illustra il funzionamento quotidiano e le procedure di ripristino.

## Flusso di lavoro dell’operatore

Diagramma di flusso · Scegliere l’archiviazione e la protezione delle chiavi → Aprire il pannello con il relativo token; Aprire il pannello con il relativo token → Selezionare un’area di lavoro; Selezionare un’area di lavoro → Configurazione del percorso diretto o tramite proxy; Configurazione del percorso diretto o tramite proxy → Inserisca il numero di telefono o selezioni i file / QR; Inserisca il numero di telefono o selezioni i file / QR → Verificare l’identità dell’account e selezionare i gruppi accessibili; Verificare l’identità dell’account e selezionare i gruppi accessibili → Salvate le politiche relative agli eventi e agli allegati, quindi avviate il monitoraggio; Salvate le politiche relative agli eventi e agli allegati, quindi avviate il monitoraggio → Monitoraggio di errori, accessi, code e spazio su disco; Monitoraggio di errori, accessi, code e spazio su disco → Mantenere punti di controllo indipendenti; Mantenere punti di controllo indipendenti → Esportazione e verifica del materiale · Sceglierel’archiviazione e laprotezione dellechiavi · Aprire il pannello conil relativo token · Selezionare un’area dilavoro · Configurazione delpercorso diretto otramite proxy · Inserisca il numero ditelefono o selezioni ifile / QR · Verificare l’identitàdell’account eselezionare i gruppiaccessibili · Salvate le politicherelative agli eventi eagli allegati, quindiavviate ilmonitoraggio · Monitoraggio dierrori, accessi, codee spazio su disco · Mantenere punti dicontrollo indipendenti · Esportazione everifica del materiale

**Diagramma sotto forma di testo**

1. Scegliere l’archiviazione e la protezione delle chiavi → Aprire il pannello con il relativo token
2. Aprire il pannello con il relativo token → Selezionare un’area di lavoro
3. Selezionare un’area di lavoro → Configurazione del percorso diretto o tramite proxy
4. Configurazione del percorso diretto o tramite proxy → Inserisca il numero di telefono o selezioni i file / QR
5. Inserisca il numero di telefono o selezioni i file / QR → Verificare l’identità dell’account e selezionare i gruppi accessibili
6. Verificare l’identità dell’account e selezionare i gruppi accessibili → Salvate le politiche relative agli eventi e agli allegati, quindi avviate il monitoraggio
7. Salvate le politiche relative agli eventi e agli allegati, quindi avviate il monitoraggio → Monitoraggio di errori, accessi, code e spazio su disco
8. Monitoraggio di errori, accessi, code e spazio su disco → Mantenere punti di controllo indipendenti
9. Mantenere punti di controllo indipendenti → Esportazione e verifica del materiale

L’autorizzazione, la connettività di trasmissione, l’accesso a un gruppo e la completezza della consegna sono proprietà distinte. Uno stato di connessione verde non implica che tutti gli eventi siano stati acquisiti.

## Condividere il lavoro senza condividere la chiave principale

**Accesso** aperto per assegnare a un revisore o analista il proprio token. Scegliete gli account e le chat che possono aprire, quindi consentite la visualizzazione, l’esportazione o le azioni operative. Un operatore che avvia o interrompe la raccolta necessita dell’accesso all’intero spazio di lavoro; un revisore può essere limitato a una singola chat. I limiti di sessione, la scadenza e le regole relative agli indirizzi IP sono distinti dall’autorizzazione dell’account Telegram. Si veda la sezione [«Accesso e autorizzazioni](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/)».

Utilizzi **le «Sessioni aperte»** per terminare una connessione oppure revochi l’accesso per chiudere tutte le relative sessioni. La console di amministrazione riunisce l’attività dei processi in corso in tutti gli spazi di lavoro. La chiusura della sessione lascia attiva la raccolta dei dati.

## Modalità di esecuzione

| Modalità | Azione | Comportamento |
| --- | --- | --- |
| Demo | scripts\Demo.cmd oppure `--demo` | Dati sintetici; collegamenti agli account reali disabilitati |
| Osservazione | Avviare l’osservazione | Registrazione degli aggiornamenti forniti per le fonti selezionate |
| Panoramica storica | Fonti → istantanea della cronologia | Fino a 500 messaggi attuali; nessuna ricostruzione di tutte le modifiche passate |
| Pausa | Osservazione in pausa | Interruzione della raccolta con conservazione dei dati e dei processi in coda |
| Revisione/consegna | Esportazioni | ZIP, JSONL/CSV/HTML, checkpoint, ricevuta di elaborazione e richiesta di timestamp |
| Account multipli | Aree di lavoro o il pulsante in alto «**+**» | Un numero illimitato di aree di lavoro separate all’interno di un unico processo |

L’accesso alla demo locale si avvia automaticamente senza l’inserimento manuale di un token. Si avvale di una funzionalità valida per la durata del processo, applicabile esclusivamente all’accesso diretto in loopback a una demo sintetica isolata; il token del pannello principale non viene divulgato. Gli spazi di lavoro reali e l’accesso alla demo da remoto o tramite proxy mantengono l’autenticazione tramite token. L’accesso alla demo non conferisce alcuna autorizzazione su Telegram.

## Categorie di monitoraggio

![Impostazioni di monitoraggio per singolo account con dati di origine sintetici](https://phishdestroy.github.io/TgWitness/assets/sources.png)

In **Fonti → Impostazioni di acquisizione → Scegliere quali modifiche conservare**, selezionare in modo indipendente i nuovi messaggi, le modifiche, le notifiche di cancellazione, gli aggiornamenti delle reazioni e gli eventi relativi all’appartenenza. L’impostazione predefinita conserva tutte le categorie. L’opzione **Messaggi, modifiche e cancellazioni** mantiene il contesto originale disabilitando al contempo gli aggiornamenti separati relativi alle reazioni e ai membri. L’opzione **«Tutte le attività visibili»** ripristina tutte e cinque le categorie. Le impostazioni predefinite modificano la forma; premere **«Salva impostazioni di monitoraggio»** per applicare le modifiche.

La politica salvata si applica a tutte le fonti selezionate in quell’area di lavoro. Le altre aree di lavoro mantengono le proprie impostazioni. Ogni modifica effettiva registra i valori prima e dopo firmati; la politica corrente è inclusa anche nelle ricevute di processo e nei registri di inizio osservazione. La disattivazione di una categoria non elimina le osservazioni precedenti. La riattivazione non recupera le modifiche perse. In questa versione non è prevista la possibilità di sovrascrivere le categorie a livello di gruppo.

Si raccomanda di mantenere abilitata l’acquisizione dei nuovi messaggi quando i contenuti precedenti sono rilevanti: una notifica di cancellazione non consente di recuperare il testo che non è mai stato acquisito. I registri operativi e di copertura, nonché altri eventi relativi al servizio di gruppo, vengono sempre conservati. Le istantanee esplicite della cronologia sono separate dalla selezione delle categorie in tempo reale e possono includere messaggi di servizio. Queste impostazioni non oscurano i metadati relativi alle reazioni o ai membri incorporati in un oggetto Telegram altrimenti acquisito.

Un’istantanea della cronologia potrebbe mettere in coda gli allegati mentre è in pausa. Avviare il monitoraggio per elaborarli. Essere in coda non significa essere scaricati. Un file originale non disponibile non viene sostituito con una versione modificata più recente; i risultati vengono registrati separatamente.

**Il pulsante «Lock»** cancella l’accesso al browser e i campi segreti, ma lascia in esecuzione la raccolta dati. Anche la chiusura di una scheda lascia il processo in esecuzione. L’arresto del processo Python o del servizio interrompe la raccolta dati indipendentemente dallo stato del browser.

L’eliminazione di un’area di lavoro aggiuntiva arresta il relativo collettore e rimuove i dati locali. Se un file bloccato o un errore del filesystem interrompe la rimozione, il pannello segnala l’errore e mantiene l’area di lavoro elencata come non disponibile (`DeletionPending`). Chiuda i programmi che contengono i relativi file e riprovi a eseguire **l’eliminazione**. Il riavvio di TgWitness lascia tale spazio di lavoro in stato di arresto e non ricrea il registro o le chiavi parzialmente rimossi. Una cancellazione riuscita viene registrata solo dopo che la directory è stata rimossa; le copie esportate o sottoposte a backup separatamente rimangono soggette alla propria politica di conservazione.

## Notifiche

**Fonti** aperte **→ Notifiche → Avvisi e riepilogo giornaliero**. TgWitness utilizza Apprise per inviare avvisi a Matrix, Telegram, Discord, Slack, ntfy, e-mail e altri servizi supportati. È possibile aggiungere diverse destinazioni a un unico spazio di lavoro.

1. Inserisca un URL di destinazione Apprise per riga. Utilizzi il [catalogo dei servizi e i formati URL](https://appriseit.com/services/) relativi al Suo servizio.
2. Attivare l’opzione **“Invia notifiche”**, quindi selezionare gli avvisi relativi a problemi, alle modifiche nelle chat monitorate e a un riepilogo giornaliero. L’ora indicata nel riepilogo si basa sull’ora del server.
3. Attivare l’opzione **«Includi brevi estratti»** se si desidera che il testo salvato dai messaggi cancellati e modificati venga incluso negli avvisi.
4. Clicchi su **«Salva notifiche»**, quindi su **«Invia test»** per verificare la consegna.

Per il proprio destinatario, si utilizzi [il webhook JSON](https://appriseit.com/services/json/) di Apprise. Ad esempio, `jsons://notify.example.org/tgwitness` invia dati JSON tramite HTTPS a tale endpoint. Si tratta di un esempio fittizio; lo si sostituisca con la propria destinazione.

Le destinazioni e le impostazioni appartengono all’area di lavoro selezionata. Le notifiche di modifica riguardano le fonti monitorate, comprese le chat aggiunte di recente. La campana nella barra superiore elenca inoltre i problemi recenti e le modifiche alle chat.

Nella demo, i controlli delle notifiche sono visibili ma l’invio è disabilitato. Configurare l’invio in un ambiente di lavoro reale. Le notifiche utilizzano il percorso Direct, SOCKS5 o HTTP di tale ambiente di lavoro; MTProxy non è in grado di trasmetterle. Le destinazioni non HTTP, come SMTP, richiedono un percorso diretto.

## Disposizione dei riquadri

![Ambiente di lavoro di connessione che utilizza dati sintetici](https://phishdestroy.github.io/TgWitness/assets/connection.png)

**Il registro** mostra osservazioni, ricerche e filtri. Una modifica apre le versioni acquisite; una cancellazione apre il contenuto precedente, se disponibile. Le attribuzioni sconosciute rimangono esplicite. I conteggi sono disponibili nella sezione **Panoramica**; i dettagli relativi all’acquisizione rimangono nella guida locale.

**La sezione «Fonti»** contiene l’ambito di monitoraggio (chat selezionate, una cartella di Telegram o l’intero account), chat accessibili di ogni tipo, fonti selezionate contrassegnate da stelle di priorità, impostazioni relative agli allegati e alla verifica incrociata, nonché istantanee della cronologia. Le fonti private vengono selezionate tramite finestra di dialogo/ID senza un link pubblico. Lo stato di accesso descrive la verifica più recente, non le autorizzazioni permanenti.

**La sezione «Chat» → «Persone»** elenca tutti gli utenti con messaggi salvati; se i profili degli utenti sono attivati per la chat, un clic apre il profilo di quella persona con i collegamenti alle voci del registro.

**Witness** crea token di testimonianza in sola lettura, indica quando ciascun testimone è stato verificato l’ultima volta e fornisce i comandi e le opzioni per eseguire un [testimone (indipendente](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/)).

**La sezione «Parametri»** contiene tutti i limiti e le frequenze dell’area di lavoro che non figurano in altre pagine: il numero di finestre di dialogo lette, la frequenza di rilettura dell’elenco delle chat, gli intervalli di heartbeat e checkpoint, il buffer di avvio, la distribuzione delle richieste durante i ricontrolli (primo ritardo, chat per passaggio, pausa tra le chat, messaggi recuperati e richiesti nuovamente), riserva su disco, timeout e tentativi di download, cosa cercano i profili utente (comprese le vostre espressioni regolari), dimensioni e frequenza delle notifiche, limiti per snapshot, file ZIP e download dal browser, nonché timeout e tentativi del client Telegram. Ogni campo mostra il proprio intervallo e il valore predefinito; i campi modificati sono contrassegnati e possono essere ripristinati uno per uno o tutti insieme. Ogni modifica viene registrata come «`parameters.changed`» con i valori precedenti e successivi, mentre i record di inizio osservazione indicano i valori in vigore. I valori si applicano a partire dal loro prossimo utilizzo; i timeout e i tentativi di riprova del client a partire dalla prossima connessione. Gli intervalli di ricontrollo, i tipi e le dimensioni degli allegati, le prove e gli intervalli di copia fuori sede rimangono nelle rispettive pagine e possono assumere qualsiasi valore compreso nel proprio intervallo, non solo quelli preimpostati.

La campana nella barra superiore elenca i problemi e le modifiche recenti nelle chat monitorate; quelle non lette vengono conteggiate finché non vengono contrassegnate come lette. Le modifiche sono raggruppate per chat e per ora («12 cancellate, 1 modificata, 0 non trovate»), mentre i problemi quali la disconnessione o il disco pieno rimangono nell’elenco indipendentemente dall’attività delle chat.

**L’accesso** inizia dal campo del numero di telefono. **Proseguendo** si accede direttamente all’ inserimento del codice, con la richiesta delle credenziali API solo qualora queste non fossero presenti. Il codice QR e l’importazione di file sono schede alternative. Le credenziali API salvate vengono riutilizzate solo all’interno del proprio spazio di lavoro. La schermata di accesso non presenta barra laterale, statistiche né paragrafi di configurazione. L’icona **Impostazioni** apre i controlli relativi all’API, al proxy, all’archiviazione e agli account aggiuntivi. Le nuove installazioni iniziano da qui; gli account collegati senza fonti selezionate partono da **«Scegli chat**». La modifica del percorso richiede un’osservazione in pausa e annulla l’accesso non completato. Un registro esistente non può essere ricollegato in modo silenzioso a un account Telegram diverso.

**L’esportazione** verifica l’integrità del registro e produce file trasferibili. L’ID dell’area di lavoro può essere trasmesso alla CLI di download. Ogni esportazione assegna un prefisso al registro completo; gli eventi successivi vengono inseriti in un’esportazione successiva. I filtri di ricerca non modificano l’ambito del pacchetto. Informazioni dettagliate sulla firma e sulla copertura sono disponibili nella sezione **«Verifica e limitazioni**».

Il pannello riporta lo stato del collettore, i file multimediali in coda o non riusciti, i file multimediali in sospeso più vecchi, lo spazio libero su disco, le pause delle richieste e le fonti il cui accesso non è confermato nella sezione **“Stato del collettore”**. Questi dettagli sono inizialmente nascosti e non visibili nella sezione “Account”. Una scheda di configurazione illustra il passo successivo: collegare un account, scegliere le fonti o avviare il monitoraggio. L’elenco degli account è un’istantanea al momento del caricamento; l’area di lavoro selezionata viene aggiornata periodicamente. Non si tratta di un monitor SLA multiprocesso.

L’interfaccia utente utilizza risorse locali e il rendering del testo per i contenuti di origine. Sono stati testati i layout per desktop e per schermi stretti basati su Chromium. Non si tratta di una certificazione completa dell’accessibilità; la valutazione dell’usabilità da parte degli utenti e tramite lettori di schermo rimane un lavoro a sé stante.

## Ambienti di implementazione

| Contesto | Installazione | Stato della verifica |
| --- | --- | --- |
| PC/server Windows | Python 3.11+, scriptSetup.cmd/Start.cmd; directory dei dati privati | Verificato localmente su Windows/Python 3.12 |
| Server Linux/VPS | Ambiente virtuale Python (venv), utente di servizio dedicato, HTTPS/SSH | Vengono forniti esempi di codice, CI e systemd; non eseguiti su questo host |
| macOS | Venv Python, processo in primo piano o user agent | Viene fornito un esempio di `launchd`; è necessario un controllo separato dell’installazione |
| Docker/Compose | Volume persistente, un solo worker | Vengono fornite la definizione e la verifica del runtime della CI; Docker non è disponibile localmente |
| Browser del telefono | Accedete al pannello protetto su un server in esecuzione | Layout Chromium ridotto testato; il collector non funziona su iOS/Android |

La portabilità implica l’assenza di un servizio cloud obbligatorio o di una build frontend. Ciascun sistema di destinazione deve comunque disporre di dipendenze Python/crittografiche compatibili, nonché di accesso al disco locale e alla rete. Si vedano [il file DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/deployment/) e [i modelli di servizio](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md).

Gli spazi di lavoro condividono CPU, memoria e un ciclo di eventi. Per l’isolamento dei processi, si raccomanda di utilizzare istanze, porte, directory dei dati e autorizzazioni degli account distinte. Non esiste un pannello di controllo unificato tra istanze separate. Si raccomanda di non indirizzare mai più worker verso un unico database.

## Verifiche all’avvio ed esportazioni

Eseguire `python start.py --check` prima di avviare un ambiente predisposto. Aggiungere `--json` per i controlli leggibili da macchina oppure specificare i valori desiderati per `--data-dir`, `--host` e `--port`. Il comando verifica i prerequisiti senza effettuare l’accesso a Telegram né creare un registro. Non verifica il registro né attesta la prontezza alla registrazione; la verifica del registro avviene durante l’avvio dell’applicazione. Una porta occupata potrebbe semplicemente corrispondere a un’istanza già esistente.

I browser che supportano l’API di accesso al file system salvano le esportazioni tramite uno stream scrivibile. Gli altri browser memorizzano nel buffer al massimo 128 MiB. Utilizzi la CLI di streaming per esportazioni di dimensioni maggiori o per browser privi di streaming di file:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Aggiungere `--profile ID` da «Exports» per un’area di lavoro secondaria. Utilizzare `--url https://server` per l’accesso remoto. Il protocollo HTTP semplice è accettato solo per destinazioni di loopback. Il token viene letto da un file e inviato nell’intestazione, non viene visualizzato né inserito in un URL. I reindirizzamenti sono rifiutati. Le destinazioni esistenti non vengono sovrascritte. I trasferimenti non riusciti rimuovono il proprio file temporaneo. Lo SHA-256 riportato è un checksum del trasferimento; si prega di verificare il file ZIP firmato separatamente utilizzando un’impronta digitale o un checkpoint attendibile.

## Backup, ripristino e interruzioni

1. Sospendere il monitoraggio e interrompere il processo in modo corretto.
2. Copiare l’intera directory dei dati: database, WAL/SHM se presenti, file multimediali, `credentials.enc`, `signing.enc`, `network.enc`, chiavi del vault/metadati, token, checkpoint e ogni directory `profiles/`.
3. Per la modalità a chiave esterna, conservare separatamente la chiave principale e mantenere ogni `vault.external.json`. La generazione di una nuova chiave non consente di recuperare i segreti precedenti.
4. Eseguire il ripristino mentre la destinazione è inattiva; configurare la chiave originale, limitare l’accesso e verificare l’integrità prima di riprendere l’operazione.
5. Registrare i tempi di inattività e i risultati delle verifiche. Un’istantanea della cronologia non può dimostrare che non siano avvenute cancellazioni durante l’interruzione.

I file ZIP contenenti le prove escludono le sessioni e le chiavi private e non costituiscono backup completi del servizio. Quattro elementi sono protetti in modo diverso:

| Cosa | Protezione |
| --- | --- |
| Esportazione dei file senza password (impostazione predefinita) | Non crittografato. Firmato, pertanto le modifiche sono rilevabili, ma chiunque sia in possesso del file può leggerlo |
| Esportazione dei file con password | Se si imposta una password, l’esportazione completata viene salvata senza modifiche in un file ZIP con crittografia AES-256 di WinZip, apribile con 7-Zip e WinRAR; la password non viene memorizzata ([gestione delle prove](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/)) |
| Il database del registro e gli allegati salvati su disco | Non crittografato da TgWitness; si raccomanda l’uso di un disco o volume crittografato |
| Sessioni Telegram e chiavi di firma | Crittografato nella directory dei dati (`credentials.enc`, `signing.enc`, `network.enc`) |

Un backup completo corrisponde alla directory dei dati bloccati sopra descritta, non a un’esportazione. Si raccomanda di utilizzare un archivio protetto e un meccanismo di trasferimento mirato per entrambi. Le esportazioni temporanee sul server risiedono nella cartella `temporary-exports/` di ciascun spazio di lavoro; le risposte completate vengono eliminate, mentre i file di esportazione interrotti vengono rimossi al successivo avvio, fintanto che il blocco dell’istanza di quello spazio di lavoro rimane attivo.

Il ripristino della connessione non garantisce il recupero delle modifiche intermedie. I processi multimediali persistenti e lo stato di aggiornamento di Telegram sopravvivono al riavvio; si veda [il formato delle prove](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#durable-collection-and-process-receipts-02).

## Capacità e periodo di conservazione

Limiti predefiniti, tutti modificabili nella sezione **«Parametri**»: le prime 1.000 conversazioni, 500 messaggi per istantanea, 4 GiB di contenuto ZIP firmato non compresso (gli archivi più grandi richiedono `verify.py --max-gib N`) e un fallback del browser di 128 MiB. Gli allegati occupano da 1 a 2.000 MiB per tipo in **Fonti → Allegati**. La CLI di download è impostata di default su 5 GiB trasferiti. Lo spazio disponibile su disco può costituire un limite inferiore. Si raccomanda di riservare spazio per i registri, i file multimediali, il WAL, le esportazioni temporanee e i backup. Le esportazioni utilizzano il volume dei dati anziché i 512 MiB di Compose (`/tmp`).

Misurate gli eventi al secondo, l’età della coda, i byte dei file multimediali e la latenza del disco, anziché limitarsi a contare i soli gruppi. I benchmark locali sintetici non garantiscono la consegna dei messaggi su Telegram. Non è prevista alcuna eliminazione automatica dei dati conservati. La rimozione della parte finale di un registro invalida il suo collegamento ai checkpoint conservati.

Esistono già verifiche prioritarie: le fonti contrassegnate con un asterisco vengono ricontrollate ogni 15 minuti per impostazione predefinita, le altre ogni 6 ore (vedere [i livelli di verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/#recheck-tiers)). Sono disponibili esportazioni protette da password come descritto sopra. L’accettazione in tempo reale di Telegram/proxy, la riproduzione duratura, il registro amministrativo e il rilevamento delle reazioni, i worker isolati, la crittografia del registro locale e dei file multimediali da parte dello stesso TgWitness e la revisione indipendente rimangono attività separate. L’accesso limitato è documentato nella sezione [«Accesso e autorizzazioni](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/)». Si vedano [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md), [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) e [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/).
