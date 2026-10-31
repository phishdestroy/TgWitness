# Formato delle prove

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/

Contenuto del file ZIP firmato, tipi di registrazioni, ricevute di elaborazione, profili degli utenti, copie esterne e verifica offline.

Un’osservazione non è una conclusione. L’ID del mittente non corrisponde a un’identità nel mondo reale. La fonte è l’aggiornamento del servizio visibile sull’account; Telegram non firma crittograficamente questi record salvati per conto di un investigatore di terze parti.

## Che cosa viene firmato

| Materiale | Protezione | Cosa conservare |
| --- | --- | --- |
| Ogni osservazione del registro, compresi gli eventi operativi | Catena SHA-256 e una firma Ed25519 per ogni evento | `events.jsonl` originale, l’impronta digitale della chiave attendibile e un punto di controllo conservato |
| Contenuto del file ZIP delle prove | `manifest.sig` firma il manifesto canonico, che elenca gli hash dei file di contenuto | Il file ZIP completo, comprensivo di manifesto e firma |
| Allegati conservati | SHA-256 e conteggio dei byte in un evento `media.saved` firmato; hash del file nel manifesto ZIP firmato | I byte originali contenuti nel file ZIP verificato |
| Checkpoint | Firma Ed25519 relativa alla lunghezza del registro, all’hash dell’intestazione, alla chiave pubblica e alla data di creazione | Una copia indipendente conservata prima di una modifica contestata |
| Ricevuta di esecuzione | Misurazioni del collettore firmate separatamente; incluse anche in un evento `process.started` firmato | La ricevuta e il registro associato; i dati sono autodichiarati |
| File CSV o HTML autonomi | Non è presente una firma crittografica autonoma; gli hash degli eventi da soli non sono sufficienti | Si prega di utilizzare il testo esatto contenuto nel file ZIP verificato per il controllo dell’integrità |
| Screenshot, stampe o file PDF generati da un browser | Nessuna firma di TgWitness sul derivato | Conservare il pacchetto originale verificato e documentare le modalità di creazione del derivato |

Il collettore verifica le firme del registro prima di generare ogni formato di esportazione. Tale verifica alla fonte non crea una firma su un file CSV o HTML scaricato separatamente. Allo stesso modo, una firma di evento JSONL valida non fornisce i byte dell’allegato né stabilisce in modo indipendente che l’intero registro osservato sia stato fornito.

## Passaggio di consegne nell’ambito delle indagini

1. Annoti il numero di riferimento del caso, l’operatore, l’ID numerico dell’account Telegram, le fonti selezionate, la politica di raccolta e il periodo di raccolta nelle note relative al caso. TgWitness conserva le osservazioni; l’assegnazione dei casi e i registri di custodia sono gestiti al di fuori dell’applicazione. Verifichi la configurazione di raccolta prevista mediante la [procedura di accettazione in tempo reale](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
2. Conservare in modo indipendente l’impronta digitale della chiave pubblica dell’area di lavoro prima di fare affidamento sulle sue esportazioni. Salvare i checkpoint firmati al di fuori del collettore durante la raccolta. Registrare le interruzioni e i limiti di visibilità dell’account.
3. Esportare un file **ZIP firmato** e conservare la ricevuta di esecuzione firmata. Utilizzare un punto di controllo in corrispondenza o prima del limite del registro esportato. Un punto di controllo successivo può correttamente rifiutare un’esportazione precedente in quanto troppo breve. Le esportazioni includono il registro completo dell’area di lavoro, indipendentemente dai filtri del pannello; si raccomanda di esaminare il materiale prima di condividerlo.
4. Si prega il destinatario di verificare il file ZIP utilizzando una copia affidabile del verificatore e l’ impronta digitale/checkpoint fornito separatamente. Da un checkout affidabile con l’ambiente Python attivo:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   I report di output corretti riportano i valori `key_pinned: true` e `checkpoint_checked: true` quando entrambi gli input vengono forniti e accettati. Si prega di conservare il risultato della verifica.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. Registri lo SHA-256 dell’archivio, i limiti dell’esportazione, la data di trasferimento, il mittente e il destinatario nel Suo registro di custodia. Mantenga intatto il pacchetto originale e lavori sulle copie. Condivida i file di prova anziché la directory dei dati privati dell’applicazione, che contiene anche le sessioni dell’account e le chiavi di firma. Per il trasferimento, un’esportazione può essere inserita in un file ZIP protetto da password con crittografia AES-256. La password protegge esclusivamente la riservatezza e non viene memorizzata; il destinatario estrae l’archivio e verifica l’esportazione firmata al suo interno, che risulta inalterata.
   2. Qualora sia necessario un ancoraggio temporale indipendente, si prega di seguire la [procedura descritta nella RFC 3161](https://phishdestroy.github.io/TgWitness/it/docs/reference/timestamp/) e di conservare la richiesta, il checkpoint, le informazioni relative alla CA attendibile e la risposta verificata dell’autorità. La semplice preparazione di una richiesta non garantisce l’ottenimento di un timestamp.

Una verifica riuscita attesta l’integrità rispetto alla chiave del collettore affidabile e ai limiti stabiliti. L’autenticità della fonte, la completa consegna dei messaggi Telegram, l’ora attendibile e l’ammissibilità legale richiedono prove separate. Questa versione non ha ancora completato la qualificazione su Telegram in tempo reale né una valutazione forense/di sicurezza indipendente.

Una chiave di raccolta copiata può firmare un registro sostitutivo fabbricato. La verifica rispetto a un punto di controllo o a una registrazione di testimonianza conservati in modo indipendente rileva un prefisso precedente modificato; la sola verifica della firma non è in grado di farlo. Una testimonianza conferma quanto presentato dal collettore, pertanto non stabilisce in modo indipendente la veridicità dei registri falsificati prima del loro primo punto di controllo esterno. I rapporti di implementazione su cloud verificano la configurazione e le misurazioni riportate dal collettore; non stabiliscono che una chiave privata non sia mai stata copiata durante la fase di avvio.

Le notifiche inviate tramite Apprise contengono i nomi e il numero degli spazi di lavoro e delle chat; brevi estratti dei messaggi cancellati e modificati vengono aggiunti solo quando l’operatore attiva tale funzione (disattivata per impostazione predefinita). Si tratta di un segnale di comodità, non di una prova: la consegna non è garantita, e solo il registro e le sue esportazioni firmate riportano ciò che è stato osservato. Con un proxy dell’area di lavoro, le notifiche seguono lo stesso percorso; i servizi che non possono utilizzarlo, così come i percorsi MTProxy, vengono rifiutati.

## Canonizzazione degli eventi

L’input dell’hash è costituito esattamente dai seguenti campi:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

Serializzare utilizzando JSON compatibile con Python in formato UTF-8, con chiavi degli oggetti ordinate, senza escape ASCII, senza spazi bianchi insignificanti e senza valori NaN/infinito:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

L’SHA-256 di tali byte costituisce l’hash dell’evento. La firma è generata con Ed25519 sui 32 byte grezzi dell’hash, quindi codificata in base64. Il primo previous_hash è composto da 64 zeri. I numeri di sequenza partono da 1 e aumentano di 1. Tutti gli eventi, compresi quelli operativi, condividono un’unica catena. Non vi è alcuna soppressione delle consegne duplicate: le osservazioni ripetute costituiscono ricevute distinte, non una rivendicazione di azioni distinte su Telegram.

Le date grezze di Telegram sono stringhe ISO; i campi binari diventano oggetti contenenti byte_base64. Il testo dei messaggi, le entità, i descrittori multimediali, i metadati delle risposte, le reazioni e le azioni di servizio vengono conservati nei metadati grezzi dei messaggi, qualora forniti.

observed_at è l’ora UTC del collettore. source_at è la data fornita da Telegram, ove disponibile. Le notifiche di cancellazione non forniscono un’ora esatta di cancellazione, pertanto source_at rimane nullo. L’ordine di ricezione dei dati non corrisponde necessariamente all’ordine degli eventi alla fonte. Le istantanee della cronologia utilizzano date di origine precedenti ma orari di osservazione attuali.

## Semantica degli attori

message.new actor_id indica il mittente del messaggio. message.edited non presenta alcun editore dedotto; payload.sender_id registra il mittente del messaggio osservato. Cancellazione l’actor_id rimane nullo. I messaggi del servizio di iscrizione conservano il mittente e il tipo di azione, senza convertire ogni rimozione in un’uscita volontaria. Gli aggiornamenti grezzi dei partecipanti conservano l’actor_id così come fornito. Le istantanee delle reazioni non inventano un attore di modifica.

Le notifiche di cancellazione relative alle chat private e ai gruppi ordinari contengono esclusivamente gli ID dei messaggi. Tali chat condividono un’unica sequenza di ID a livello di account; pertanto, un ID identifica un singolo messaggio di questo account. Quando un messaggio con quell’ID è stato salvato in precedenza in questo registro, la cancellazione viene registrata in quella chat come message.deleted con payload.chat_resolution che indica il metodo. Gli ID che non sono mai stati salvati vengono conservati come deletion.unscoped senza chat_id; non viene effettuata alcuna deduzione. I canali e i supergruppi numerano i messaggi per chat e non vengono mai abbinati in questo modo. Quando il messaggio eliminato è stato inviato dall’account osservato, payload.deleted_message_was_outgoing è vero; l’autore dell’eliminazione non viene comunque specificato.

## Ambito di copertura: continuità, lacune e ID non rilevati

Ogni file ZIP firmato contiene `coverage.json`; il report HTML si apre con lo stesso riepilogo, mentre `verify.py` lo ricalcola a partire da `events.jsonl` anziché fare affidamento sul file:

- **Osservazione continua da X a Y.** Un periodo inizia con `observation.started` e termina in caso di pausa, arresto, interruzione della connessione a Telegram, disconnessione, avvio di un processo senza un arresto ordinato, oppure se trascorrono più di tre minuti senza alcuna registrazione durante l’osservazione (i segnali di attività vengono registrati ogni minuto, pertanto il silenzio indica che il processo si è arrestato, si è bloccato o che il computer è entrato in modalità di sospensione). Quando l’intervallo dei segnali di attività viene modificato in **«Parametri»**, ogni segnale ne tiene traccia e il silenzio consentito diventa pari a tre intervalli, mai inferiore a tre minuti.
- **Le lacune** indicano l’intervallo di tempo tra i periodi, con la relativa motivazione. Una lacuna ancora aperta all’ultimo record è contrassegnata con il codice `not_resumed_by_last_record`.
- **Gli ID dei messaggi non vengono rilevati.** Per i canali e i supergruppi, che numerano i messaggi per singola chat, gli ID mancanti tra quelli rilevati sono elencati come intervalli. Vengono segnalati come non*rilevati* — cancellati, mai consegnati o al di fuori della cronologia salvata — mai come cancellati. Le chat private e i gruppi ordinari condividono una sequenza a livello di account, pertanto eventuali lacune in tali casi non hanno alcun significato e non vengono elencate.
- Le segnalazioni di interruzioni a livello di chat (ad esempio quando Telegram richiede il ripristino delle differenze in un canale) vengono conteggiate come note; esse non interrompono la copertura globale.

La copertura descrive ciò che questo strumento di raccolta ha registrato. Non costituisce una prova del fatto che Telegram abbia consegnato ogni aggiornamento durante un periodo continuativo.

## Produttore

Il manifesto firmato dei file ZIP contenenti le prove, le esportazioni delle chat, i registri delle testimonianze e la dichiarazione relativa ai file dei profili personali contiene `producer` : software, versione, progetto (PhishDestroy), pagina web e repository del codice sorgente. Il rapporto in formato HTML riporta la stessa riga, e `verify.py` la riporta come parte di quanto verificato. Gli archivi creati prima che questo campo esistesse vengono verificati come in precedenza e vengono segnalati come privi di indicazione del produttore.

## Profili delle persone

Su richiesta, viene generato un file di profilo (`tgwitness-dossier-v1`, JSON) a partire dai dati già presenti nel registro relativi a una singola chat; non viene prelevato nulla da Telegram e i contenuti del profilo non vengono mai scritti nel registro (l’attivazione e la disattivazione dei profili vengono registrate come `dossier.changed`). Per ogni persona con un messaggio salvato, vengono elencati il nome e la cronologia dei nomi utente, i contrassegni di Telegram (bot, truffa, falso, premium, verificato, con restrizioni, eliminato) così come visibili al momento del salvataggio, le foto identificative, l’hash SHA-256 e l’hash percettivo (pHash, compatibile con `imagehash.phash`) dell’ avatar dalla cache locale degli avatar con avatar simili, l’attività (primo e ultimo messaggio, conteggi, condivisioni modificate ed eliminate, messaggi per ora UTC), chi risponde a chi, altre chat in questo diario in cui la persona ha scritto e i portafogli menzionati (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL; gli indirizzi Base58Check sono convalidati tramite checksum), numeri di telefono, nomi utente e link, compresi quelli nascosti dietro il testo.

Ogni fatto riporta i record del registro (`seq`) da cui proviene, mentre `record_hashes` contiene l’ hash di ciascun record a cui si fa riferimento. La dichiarazione è firmata con la chiave dell’area di lavoro:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

Verifica la firma, controlla l’esportazione delle prove stessa (firma, catena di hash e file) e che ogni record a cui si fa riferimento esista inalterato in tale esportazione dello stesso spazio di lavoro. Gli hash degli avatar sono contrassegnati come provenienti dalla cache locale (non dai record del registro). Le menzioni sono corrispondenze di pattern — indizi da verificare, non fatti accertati. I profili vengono attivati per ogni singola chat, possono essere esportati come file ZIP crittografato con AES-256 e protetto da password, e vengono eliminati quando vengono disattivati o quando la chat viene rimossa dalle fonti.

## Testimone indipendente

Un registro testimone (`tgwitness-witness-v1`) e i relativi post del canale vengono confrontati con un’ esportazione delle prove tramite `verify.py --witness … --channel …`; si veda [«testimone indipendente](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/)».

## Manifesto e punti di controllo

Il file manifest.json include il formato, l’ora di esportazione, la chiave pubblica, l’impronta digitale, la lunghezza del registro, l’hash di testa, l’ambito, il produttore, le limitazioni e l’SHA-256 di ogni elemento di contenuto diverso dagli stessi `manifest.json` e `manifest.sig`. Il file manifest.sig è la firma Ed25519 in base64 sul manifest JSON canonico. Il verificatore rifiuta elementi inattesi o mancanti, nomi duplicati, file danneggiati, sequenze o catene interrotte, firme non valide e discrepanze rispetto a un checkpoint fornito. Non estrae mai i percorsi degli archivi. Limita la dimensione totale dichiarata non compressa a 4 GiB; il `--max-gib N` consente archivi più grandi realizzati con un limite **di Parameters** aumentato.

Si prega di ottenere il codice di verifica da un checkout affidabile o da una copia indipendente sottoposta a revisione. Un verificatore contenuto in un archivio non attendibile è materiale eseguibile fornito dall’autore di tale archivio; la sua presenza costituisce una comodità in termini di portabilità, non un punto di riferimento indipendente di affidabilità.

Un checkpoint firma una dichiarazione contenente la chiave pubblica, la lunghezza del registro, l’hash di testa e l’ora di creazione. Il verificatore può accertarsi che un archivio successivo contenga lo stesso prefisso. Si raccomanda di conservare un checkpoint al di fuori del collettore prima di una modifica contestata: un malintenzionato che controlli sia l’archivio che il checkpoint può sostituire entrambi.

Una firma valida proveniente da una chiave non fissata garantisce esclusivamente la coerenza interna. Anche una chiave fissata non può dimostrare l’autenticità del contenuto originale se il dispositivo di raccolta o la chiave sono stati compromessi prima della registrazione. La marcatura temporale esterna e l’acquisizione affidabile sono requisiti distinti. TgWitness non garantisce l’ammissibilità né la certificazione forense.

## Allegati

I file sono identificati tramite SHA-256 nella cartella media/. Un evento media.saved associa un hash e la lunghezza in byte a un evento di messaggio specifico. I nomi dei file grezzi costituiscono metadati, mai percorsi locali. I byte multimediali vengono scaricati in modo asincrono, pertanto un’eliminazione immediata potrebbe impedire la cattura. La raccolta disabilitata, i file di dimensioni eccessive o sconosciute, gli errori di download e i download interrotti sono visibili come risultati. Un arresto anomalo del processo può lasciare file parziali senza riferimenti; essi non vengono inclusi nelle esportazioni.

L’esportatore ZIP verifica i file multimediali archiviati in base ai loro nomi. Le esportazioni in formato JSONL, CSV e HTML verificano le firme degli eventi ma non includono i byte dei file multimediali. I report derivati sono strumenti di comodità; il file events.jsonl costituisce la rappresentazione ufficiale degli eventi.

## Raccolta duratura e ricevute di elaborazione (0.2)

Un’operazione relativa a un file multimediale e il relativo evento di invio del messaggio vengono eseguiti in un’unica transazione. Il processo memorizza il descrittore originale del messaggio TL; l’osservazione firmata associa il proprio SHA-256, l’account e la politica relativa alle dimensioni. Il recupero verifica tale associazione prima del download. Non recupera mai il messaggio corrente e sostituisce silenziosamente l’allegato con uno più recente. I processi interrotti vengono riprovati, mentre il fallimento permanente rimane un esito esplicito.

Ogni area di lavoro dispone di un proprio registro e di una propria identità di firma. Un evento «process.started» include un ID di esecuzione, gli orologi locali, le versioni delle dipendenze, gli hash dei file sorgente, l’account/ambito iniziale, e le impostazioni di acquisizione. Gli «heartbeat» includono l’ID di esecuzione, il tempo monotono e lo stato della coda. La ricevuta del processo può inoltre essere scaricata come dichiarazione firmata separatamente. Le misurazioni dei file sono autodichiarate e non costituiscono un’attestazione hardware attendibile.

I checkpoint automatici vengono conservati localmente all’avvio, ogni cinque minuti durante il monitoraggio (**Parametri → Checkpoint firmato ogni**) e al termine ordinato dell’operazione. La verifica all’avvio e l’esportazione confrontano il registro con l’ultimo checkpoint locale conservato. Ciò consente di rilevare un rollback del database qualora il checkpoint sia ancora presente; un operatore che controlli entrambi può comunque sostituirli entrambi. La conservazione indipendente e i timestamp esterni attendibili rimangono requisiti distinti.

Dopo un riavvio, viene ripreso il punto di aggiornamento di Telegram salvato (`catch_up_from` in `observation.started`) e vengono richiesti gli aggiornamenti mancanti. Una verifica periodica registra `message.recovered` per i messaggi mancanti e `message.missing_on_recheck` quando Telegram non restituisce più un messaggio salvato; quest’ultimo non costituisce un avviso di cancellazione e non indica né l’autore della cancellazione né l’ora.

### Copia e ripristino fuori sede (S3)

La copia off-site (Esportazioni, disattivata per impostazione predefinita) carica segmenti del registro, file conservati, checkpoint con i relativi timestamp e le esportazioni complete delle chat su uno spazio di archiviazione compatibile con S3, crittografati con AES-256-GCM prima del caricamento, utilizzando una chiave conservata nel vault dell’area di lavoro; la conservazione con Object Lock si applica qualora il bucket la supporti. Senza la chiave scaricata, la copia non può essere letta. Ripristino e verifica con `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Il ripristino richiede una directory ordinaria vuota. I file scaricati e gli oggetti decriptati rimangono in un’area di archiviazione temporanea privata fino a quando l’intero registro e ogni checkpoint conservato non vengono verificati. I percorsi degli oggetti non sicuri, gli intervalli di segmenti incoerenti e i registri più brevi di un checkpoint vengono rifiutati; in caso di verifica fallita, non viene pubblicato alcun file ripristinato. I controlli di conservazione confrontano la modalità Object Lock e la data restituite con la scadenza inviata al momento del caricamento (con una tolleranza di arrotondamento di un secondo). Una scadenza scaduta, non valida o abbreviata non viene considerata verificata. Lo stato riporta l’oggetto campionato di cui è stata riletta la conservazione per quel ciclo di caricamento.

Lo stato di avanzamento della copia è limitato alla destinazione e alla chiave di crittografia specificate. La modifica dell’endpoint, del bucket o del prefisso avvia una copia completa del registro, dei file multimediali e dei checkpoint conservati localmente verso tale destinazione. Lo stato di avanzamento precedente non ancora coperto viene conservato, ma riprodotto una sola volta dopo l’aggiornamento. Le esportazioni storiche delle chat già rimosse dalla cartella “Posta in uscita” locale rimangono nella loro destinazione precedente.

I file multimediali locali mancanti o danneggiati vengono segnalati come errore del ciclo e il cursore multimediale rimane posizionato prima di essi, in modo che il file venga riprovato nel ciclo successivo; i file, i checkpoint e le esportazioni successivi vengono comunque copiati. Il ripristino verifica tutti i riferimenti ai file multimediali conservati confrontandoli con gli hash decrittografati e le dimensioni registrate. I segmenti identici e sovrapposti del registro derivanti da caricamenti interrotti vengono deduplicati; le sovrapposizioni in conflitto vengono respinte. I punti di controllo creati durante un caricamento vengono differiti fino a quando i relativi record del registro non siano stati copiati, in modo che un ciclo completato non pubblichi un punto di controllo prima del relativo registro.

### Esportazione in streaming di istantanee

Le esportazioni in streaming utilizzano uno snapshot di lettura stabile di SQLite. La sua parte iniziale potrebbe risultare più vecchia rispetto al registro attivo corrente al momento del completamento del download. Un checkpoint creato successivamente a tale snapshot può correttamente indicare che l’archivio è più breve; si raccomanda di effettuare il confronto con un checkpoint situato in corrispondenza o prima del prefisso esportato, non con un checkpoint successivo arbitrario.

## Preparazione della RFC 3161 e verifica delle risposte (0.2)

La modalità «Evidence» (disattivata per impostazione predefinita) invia solo l’SHA-256 di ciascun checkpoint firmato alle autorità RFC 3161 e ai calendari OpenTimestamps elencati, tramite il percorso dell’area di lavoro e mai tramite MTProxy. Le risposte vengono conservate in `checkpoints/anchors/`, esportate e verificate da `verify.py` (`--tsa-ca` verifica la firma TSA; confermare le prove OpenTimestamps con `ots upgrade` e `ots verify`).

Il pannello prepara un archivio delle richieste contenente i byte canonici del file checkpoint.json, un’impronta SHA-256 del messaggio e un nonce casuale nel file timestamp.tsq, i checksum e le istruzioni. Non viene effettuata alcuna richiesta di rete. La preparazione non costituisce un timestamp attendibile.

`python -m tgwitness.anchor verify` chiama OpenSSL due volte: una volta rispetto ai byte del checkpoint e una volta rispetto alla richiesta originale. È richiesto esplicitamente un file CA attendibile; i certificati inclusi non vengono automaticamente considerati attendibili. La verifica della richiesta è facoltativa nella CLI, pertanto si prega di mantenere e specificare l’opzione --request per verificare il nonce. Il risultato indica se la verifica è stata effettuata. La firma del checkpoint del collettore e il registro devono comunque essere verificati separatamente con l’impronta digitale attendibile del collettore.

L’attuale verificatore non recupera le informazioni di revoca né implementa la convalida dell’archiviazione a lungo termine dopo la scadenza del certificato. Non si deve equiparare la verifica positiva della firma a un timestamp qualificato o all’ammissibilità legale. Durante lo sviluppo non è stata contattata alcuna TSA realmente indipendente. Si veda [la procedura](https://phishdestroy.github.io/TgWitness/it/docs/reference/timestamp/).
