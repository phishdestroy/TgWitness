# Prove e affidabilità

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence-trust/

Cosa possono dimostrare le esportazioni, i video, gli archivi web e i record firmati, e in che modo il dispositivo di raccolta influisce sulla loro affidabilità.

Un’esportazione, uno screenshot o una registrazione possono costituire prove utili. La loro affidabilità dipende dal modo in cui sono stati raccolti, conservati e corroborati. **Un hash o una firma validi verificano il materiale salvato; non stabiliscono in modo indipendente che il dispositivo di raccolta abbia ricevuto contenuti di origine veritieri.** Questo limite si applica anche a TgWitness.

La presente guida separa la verifica tecnica dalla valutazione legale. La documentazione del prodotto e le disposizioni legali riportate di seguito sono state riviste il 1° novembre 2026; il confronto di Hunchly descrive la documentazione pubblicata, non una nuova verifica del prodotto.

## Quando la fiducia entra in gioco nell’acquisizione

Diagramma di flusso · Account e servizio Telegram → Client, browser e sistema operativo; Client, browser e sistema operativo → Esportazione, registrazione video o cattura della pagina; Esportazione, registrazione video o cattura della pagina → Hash e firme dei collettori; Hash e firme dei collettori → Hash conservato da una parte indipendente · Account e servizioTelegram · Client, browser esistema operativo · Esportazione,registrazione video ocattura della pagina · Hash e firme deicollettori · Hash conservato da unaparte indipendente

**Diagramma sotto forma di testo**

1. Account e servizio Telegram → Client, browser e sistema operativo
2. Client, browser e sistema operativo → Esportazione, registrazione video o cattura della pagina
3. Esportazione, registrazione video o cattura della pagina → Hash e firme dei collettori
4. Hash e firme dei collettori → Hash conservato da una parte indipendente

Il modello di minaccia qui ipotizza che un aggressore o un operatore possa alterare l’ambiente di raccolta prima che le prove vengano salvate. Si tratta di un’analisi condizionale, non di un’affermazione secondo cui un particolare dispositivo o prodotto sia stato compromesso.

Un client ufficiale e una connessione crittografata contribuiscono a proteggere l’uso normale. Essi non rendono il sistema operativo, il browser o il display circostanti di per sé affidabili. Se il contenuto viene sostituito dopo la decrittografia ma prima dell’acquisizione, l’esportatore può salvarlo accuratamente e il firmatario può firmarlo correttamente. Nessuna delle due operazioni richiede un algoritmo hash compromesso o una firma contraffatta.

Un video realizzato sullo stesso dispositivo può registrare la stessa presentazione sostituita. Una fotocamera separata può confermare ciò che il display mostrava, ma il display da solo non autentica ciò che Telegram ha fornito. Allo stesso modo, HTML, JSON, screenshot e log del browser corrispondenti provenienti da un unico ambiente controllato possono presentare lo stesso errore. La loro corrispondenza costituisce un contesto utile; non rappresenta automaticamente una corroborazione indipendente.

## Il contributo di ciascuna forma di prova

| Materiale | Contributo utile | Domanda rimanente |
| --- | --- | --- |
| Esportazione da Telegram Desktop | Conversazioni leggibili o leggibili da macchina e contenuti multimediali selezionati | Chi ha gestito i file client e di esportazione, e quali elementi erano disponibili o esclusi? |
| Screenshot o registrazione dello schermo | Contesto visibile, sequenza di azioni e presentazione | La presentazione riflette fedelmente la fonte e ciò che è accaduto al di fuori della registrazione? |
| Archivio web locale, compreso MHTML | Contenuto della pagina e risorse associate per un’analisi successiva | Cosa ha fornito il browser all’archiviatore e chi controllava quel browser? |
| Archivio firmato dal raccoglitore | Le modifiche ai byte firmati possono essere rilevate rispetto a una chiave attendibile e a un riferimento conservato | Chi ha controllato la chiave di firma e i dati inseriti prima della firma? |
| Punto di controllo conservato in modo indipendente o timestamp verificato | Un hash o un checkpoint conservato per il confronto con un invio successivo | Quali byte e quali limiti sono coperti, e cosa attesta effettivamente la parte indipendente? |

Telegram documenta la sua esportazione da Desktop come copia offline in formato HTML/JSON e la sua API Takeout come metodo per recuperare dati selezionati dall’account. Queste descrizioni non forniscono una firma di Telegram sull’archivio finale esportato che il destinatario possa verificare. La nostra conclusione si limita a tali meccanismi di esportazione documentati; non si tratta di un’ affermazione secondo cui le prove di Telegram non abbiano valore legale.[Esportazione da Telegram Desktop](https://telegram.org/blog/export-and-more),[API Takeout](https://core.telegram.org/api/takeout).

La stessa distinzione si applica alle richieste in background, alle voci della cache e ai log di rete. Questi possono rivelare incongruenze e aiutare a corroborare una raccolta. La loro complessità di per sé non stabilisce chi li abbia prodotti. Un archivio gestito in modo indipendente o un registro di servizio ottenuto separatamente introduce una fonte diversa da confrontare, soggetta alle proprie limitazioni di raccolta e custodia.

## Hunchly illustra lo stesso confine

La documentazione di Hunchly descrive l’hash SHA-256 delle acquisizioni MHTML, delle foto e degli allegati, con verifica indipendente dell’hash. Spiega inoltre perché un file alterato accompagnato da un hash ricalcolato possa superare tale confronto, e indica le firme e la conferma della fonte come controlli aggiuntivi.[Hunchly: hash di contenuti, foto e allegati](https://support.maltego.com/support/solutions/articles/15000061289-content-photo-and-attachment-hashing).

*La sua Guida alle prove* pubblicata, revisione 1.0 del 17 ottobre 2018, descrive le chiavi GPG e le firme generate localmente per le acquisizioni MHTML. Identifica esplicitamente l’accesso alla chiave privata locale come un modo per firmare nuovamente il materiale modificato. Si tratta di una limitazione di fiducia documentata, non di una prova di un exploit attuale non divulgato. La guida afferma inoltre che Chrome esegue l’acquisizione MHTML. Descrivere Hunchly come un sistema che si basa esclusivamente sulla reputazione di un investigatore ometterebbe questi controlli tecnici.[Guida alle prove di Hunchly, sezioni 2–4](https://hunch.ly/resources/Hunchly%20Evidence%20Guide.pdf).

L’ammissibilità in un caso del materiale raccolto con un determinato prodotto dipende dalla decisione e dalle circostanze del caso specifico. Non esprimiamo qui alcuna affermazione sulla frequenza con cui i tribunali accettano Hunchly o TgWitness, né sul fatto che uno dei due prodotti goda di un’ approvazione generale da parte dei tribunali.

## Cosa aggiunge TgWitness e dove si ferma la sua protezione

TgWitness registra le osservazioni in un registro firmato e collegato e fornisce esportazioni che il destinatario può verificare. I checkpoint conservati, i timestamp e un testimone separato forniscono ai revisori riferimenti che vanno oltre i file attuali del responsabile della raccolta. Essi aiutano a evidenziare le modifiche apportate ai record precedentemente salvati. I registri di copertura e i risultati espliciti della raccolta aiutano a spiegare cosa è stato e cosa non è stato acquisito.[Formato e trasferimento delle prove](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/), [ambito della raccolta](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/).

Il momento in cui avviene un’eventuale sostituzione è importante:

1. **Dopo la firma, senza accesso alla chiave di firma:** la modifica di un record firmato o di un file associato al manifesto comporta il fallimento della verifica da parte di un verificatore e di una chiave affidabili.
2. **Con la chiave del collettore, dopo che è stato conservato un punto di controllo indipendente:** un registro sostitutivo può avere nuove firme valide, ma un prefisso modificato non supera il confronto con quel punto di controllo precedente. Un punto di controllo conservato solo sullo stesso dispositivo controllato può essere sostituito insieme al registro. I record oltre il limite conservato richiedono una copertura a sé stante.
3. **Prima che un checkpoint che copre un'osservazione venga conservato in modo indipendente:**dati di input falsi possono essere firmati e ancorati con successo, compresi i nuovi record aggiunti dopo un checkpoint precedente. Il checkpoint o il timestamp risultante copre comunque quei record falsi; non ne stabilisce la veridicità.

Un testimone TgWitness riceve i checkpoint firmati dal collettore; non legge in modo indipendente la conversazione Telegram sottostante. La sua chiave e i record conservati devono essere considerati affidabili separatamente. Quando l’intero registro inviato deve essere testimoniato, utilizzare la[procedura di passaggio di consegne che richiede il limite di esportazione finale](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/#require-a-witnessed-export-boundary). Un normale controllo di integrità può comunque segnalare una coda non testimoniata.

Una risposta RFC 3161 verificata può confermare l’esistenza di un checkpoint all’ora dichiarata dall’autorità. Non stabilisce quando un messaggio Telegram sia stato inviato né se il suo contenuto fosse veritiero. Una richiesta preparata o un file di risposta incluso da soli non sono sufficienti. Quando si verifica un’esportazione con `tgwitness.verify`, la verifica delle firme TSA incluse richiede una CA esplicitamente attendibile tramite `--tsa-ca`. Le ricevute OpenTimestamps necessitano di una verifica indipendente `ots verify`, con aggiornamenti delle prove ove necessario. [Procedura di marcatura temporale](https://phishdestroy.github.io/TgWitness/it/docs/reference/timestamp/), [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html).

[Nell’acquisizione GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md), un runner ospitato temporaneamente raccoglie i messaggi. L’attestazione vincola l’archivio a un flusso di lavoro approvato. Questa modalità continua a fare affidamento su GitHub, sul software approvato e sulle dipendenze, sull’helper/browser e sul tunnel. Non si tratta di hardware riservato, di una firma Telegram né di una prova che nessuno abbia avuto accesso all’host. Anche una ricevuta di esecuzione firmata localmente è una misurazione autodichiarata, non un’attestazione hardware.

## Il peso giuridico dipende dalle basi su cui si fonda

Quattro questioni devono rimanere distinte: se l’elemento sia effettivamente ciò che si dichiara essere, se i byte inviati corrispondano al record conservato, se il contenuto confermi i fatti dichiarati e se le norme applicabili ne consentano l’uso. Un controllo crittografico riguarda solo una parte di tale fondamento.

Nei procedimenti federali statunitensi, la Regola 901 prevede modalità per autenticare le prove, comprese le testimonianze di testimoni informati e le prove relative a un processo o a un sistema. Le Regole 902(13) e 902(14) prevedono modalità di certificazione per determinati documenti e copie elettroniche, con relativi requisiti procedurali. Le note della commissione distinguono l’autenticazione da questioni quali il sentito dire, la rilevanza e l’attribuzione. Una firma software di per sé non costituisce la certificazione da parte di una persona qualificata ivi descritta.[Regola federale di prova 901](https://www.law.cornell.edu/rules/fre/rule_901),[Regola federale di prova 902](https://www.law.cornell.edu/rules/fre/rule_902).

Laddove si applica la Legge canadese sulle prove (Evidence Act), la sezione 31.1 riguarda l’autenticazione dei documenti elettronici. La sezione 31.2 collega la regola della prova migliore all’integrità del sistema o a una presunzione applicabile; la sezione 31.3 specifica le circostanze per una presunzione di integrità. Si tratta di condizioni probatorie definite, non di una presunzione generica secondo cui qualsiasi investigatore autorizzato o prodotto commerciale sia infallibile. [Legge canadese sulle prove, 31.1](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.1.html),[31.2](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.2.html),[31.3](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.3.html).

Questi esempi non stabiliscono l’ammissibilità in un’altra giurisdizione o in un caso specifico. I controlli tecnici devono essere applicati in modo coerente al materiale a sostegno o a contestazione di un’accusa. La presente guida non sostiene in alcun modo che le prove dell’accusa siano generalmente più facili da ammettere rispetto a quelle della difesa.

## Preparare un documento che possa essere valutato da un’altra persona

- Descrivere l’account, il dispositivo di raccolta, l’operatore, la versione del software, i diritti di accesso, l’ambito selezionato e il periodo di raccolta. Registrare le interruzioni e le possibili compromissioni, invece di considerare una verifica della firma riuscita come un test di integrità del dispositivo.
- Conservare i pacchetti originali e registrare i trasferimenti, gli hash e la fonte temporale. Conservare l’impronta digitale della chiave e i checkpoint tramite un canale separato e affidabile. Verificare l’effettiva copertura dei testimoni o dei timestamp prima di descriverla in un rapporto.
- Cercare una conferma indipendente adeguata all’affermazione: i registri di un altro partecipante, una registrazione indipendente o registri di servizio ottenuti legalmente. Spiegare la loro indipendenza e i loro limiti; la corrispondenza tra le copie non è di per sé sufficiente.
- Conservare il contesto pertinente. Identificare i file omessi, la cronologia non disponibile e le censure. Preparare una [divulgazione separata e ridotta al minimo](https://github.com/phishdestroy/TgWitness/blob/main/docs/ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient)quando necessario, e descriverne le trasformazioni senza presentarla come l’originale completo.
- Fornire al destinatario le istruzioni di verifica e il materiale necessario per tali controlli. Mantenere distinguibili le osservazioni, i risultati tecnici e le conclusioni dell’analista.

Per un particolare passaggio di consegne, indicare l’hash dell’archivio, la chiave attendibile, il risultato della verifica e l’esatto confine coperto esternamente. Descrivere separatamente l’autenticità della fonte, l’attribuzione dell’account, la completezza e le conclusioni legali. Ciò fornisce al prossimo revisore affermazioni specifiche da esaminare.
