# Telegram · Esportazione dell’account

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/account-export/

Esporta ciò che un account può leggere al momento: ambito, attività riprendibili, un archivio firmato e copie di condivisione ridotte al minimo.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Prove e verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/)

![Prove e verifica](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

L’esportazione di un account riserva quell’account in esclusiva. Sospendi esplicitamente il monitoraggio o un’altra acquisizione prima di avviare o riprendere: l’applicazione non la interrompe mai automaticamente.

In qualità di amministratore dell’installazione, seleziona **«Inizia qui» → «Esporta il mio account**» oppure **«Esportazioni» → «Account Telegram» → «Configura esportazione account**». Effettua l’accesso se necessario, verifica l’ambito e avvia esplicitamente l’esportazione. Non è richiesto un monitoraggio continuo. **Le osservazioni salvate** costituiscono un’esportazione separata del diario esistente; il suo ZIP include tutte le fonti indipendentemente dai filtri del diario. Ogni area di lavoro dispone di propri processi, identità di firma e spazio di archiviazione. L’accesso al pannello concesso, compresa un’autorizzazione illimitata all’esportazione ordinaria, non consente di aprire questi percorsi a livello di account.

I filtri per mittente e testo si espandono sotto **«Filtra per mittente» o «Testo del messaggio**». La sezione **«Dati account e metodo di connessione**» contiene categorie di account opzionali e la scelta tra Takeout e sessione regolare; il suo riepilogo mostra le opzioni attive anche quando la finestra è chiusa. Chiudendo queste sezioni, le impostazioni vengono mantenute. Le bozze di esportazione e dei report rimangono nella sessione corrente del pannello anche quando si cambia vista; non vengono salvate al ricaricamento del browser. I lavori esistenti rimangono accessibili da entrambe le opzioni di esportazione.

Questo flusso di lavoro esporta i dati attualmente accessibili dall’account collegato. L’impostazione predefinita utilizza [Telegram Takeout](https://core.telegram.org/api/takeout); non si tratta di un backup dei dati Telegram non disponibili o eliminati. Le chat segrete, la cronologia inaccessibile e le modifiche precedenti non vengono recuperate. Telegram può imporre un periodo di attesa prima che Takeout abbia inizio. Il pannello visualizza tale attesa; non cambia il metodo di trasferimento in modo silenzioso. L’opzione esplicita «regular-API» ha una copertura diversa e registra categorie non supportate.

Takeout è l’API di esportazione ufficiale utilizzata anche da Telegram Desktop. TgWitness può scrivere JSON compatibile con Desktop direttamente dalla propria acquisizione; non è necessario importare l’ archivio di qualcun altro. Gli ID delle chat e dei messaggi sono disponibili tramite entrambi i canali di trasmissione. Una chat pubblica o l’autorizzazione all’inoltro non garantiscono un’esportazione più veloce né eliminano il ritardo di approvazione di Takeout. Verificare che l’ambito e le impostazioni multimediali siano gli stessi prima di confrontare la velocità.

Per un massimo di 20 ID di chat selezionati esplicitamente, l’esportazione tramite API standard risolve tali peer direttamente prima di prendere in considerazione l’inventario completo delle conversazioni dell’account. Un canale pubblico leggibile può quindi essere esportato senza doversi unire ad esso, anche quando è assente dall’elenco delle conversazioni. I peer non memorizzati nella cache ricorrono all’inventario ordinario. Il filtro di archiviazione rimane attivo: se Telegram non restituisce una conversazione e le chat archiviate sono escluse, lo stato di archiviazione sconosciuto viene registrato come omissione. Takeout mantiene la sua procedura di inventario a intervallo diviso. Nessuno dei due percorsi entra nelle chat né modifica i permessi di inoltro. Nel formato JSON compatibile con Desktop, i canali che Telegram contrassegna come `left` compaiono sotto `left_chats`, compresi i canali pubblici leggibili a cui l’account non si è unito.

Sia `FLOOD_WAIT` che `FLOOD_PREMIUM_WAIT` sospendono le richieste per l’intero periodo richiesto dal server. La scadenza dell’account viene mantenuta anche in caso di ricollegamenti e riavvii; un’attesa successiva più breve non può accorciarla. I tentativi sono limitati, la cancellazione preserva le pagine sigillate e le credenziali API non vengono ruotate per aggirare un limite di frequenza. Non viene effettuato alcun acquisto Premium.

## Scegli cosa raccogliere

| Contesto | Significato |
| --- | --- |
| Scopo | Indica il motivo per cui questa acquisizione è necessaria. Non inserire qui nomi non necessari o dettagli sensibili relativi al caso. |
| Lingua del report | Scegli la lingua delle etichette del report leggibile. Il testo originale del messaggio rimane invariato; le etichette del modello non tradotte utilizzano l’inglese. La lingua viene fissata tramite le opzioni del processo firmato. |
| Tipi di chat / ID delle chat | Tutti i tipi selezionati o solo le chat elencate; i «Messaggi salvati» appartengono alle chat private. Le chat archiviate sono selezionabili separatamente. |
| Date | UTC. Sono incluse entrambe le date del calendario "Da" e "Fino a" del pannello. L’API utilizza date inclusive `from_utc` ed esclusive `to_utc`; il pannello invia l’inizio del giorno successivo alla data "Through". Un limite vuoto lascia quel lato senza restrizioni. |
| ID mittente | Solo i messaggi dei mittenti elencati; un elenco vuoto include tutti i mittenti. |
| Il testo contiene | Frasi letterali che non distinguono tra maiuscole e minuscole, abbinate con OR. Le condizioni relative a mittente/data/messaggio proprio si combinano con AND. |
| Messaggi propri | Conserva solo i messaggi in uscita. |
| Tipi di file multimediali | Seleziona le categorie di allegati oppure deseleziona tutto per evitare il download dei file dei messaggi. |
| Limiti relativi ai file e ai contenuti multimediali complessivi | MiB per file e GiB totali di contenuti multimediali scaricati. Testo, ricevute, report leggibili e overhead ZIP richiedono spazio su disco aggiuntivo. |
| Categorie di account | Profilo, contatti, foto del profilo, storie, metadati delle sessioni e altri dati Takeout dispongono di controlli separati. |

Il preset **della raccolta «Minimize»** disabilita i file e i metadati degli account. I filtri relativi al mittente e al contenuto vengono applicati prima della conservazione delle pagine dei messaggi e del download dei file multimediali. Telegram continua a trasmettere le pagine della cronologia API contenenti i messaggi necessari per valutare tali filtri: il filtraggio non garantisce che i messaggi non selezionati non entrino mai nella memoria di processo. Ogni altra osservazione in corso nell’area di lavoro ha le proprie impostazioni relative all’ambito e alla conservazione.

La cronologia delle foto del profilo e le storie non sono selezionate per impostazione predefinita. Disattivare anche il profilo e i contatti quando il caso richiede solo i messaggi. Se gli allegati o i metadati non sono necessari, escluderli durante l’acquisizione evita di conservare un’altra copia privata in questa esportazione.

I payload delle foto utilizzano la variante di immagine fissa identificata nei relativi metadati e nei manifest di hash, comprese le foto con una variante di avatar animato. Tale animazione non viene sostituita dall’immagine fissa selezionata. Un payload più corto o più lungo rispetto alla dimensione osservata viene registrato come allegato non riuscito, mentre una rappresentazione modificata durante il rinnovo del riferimento al file viene rifiutata. Questi errori lasciano l’archivio parziale, pur conservando i record dei messaggi. La verifica indipendente rifiuta inoltre gli allegati salvati la cui lunghezza firmata contraddice la loro dimensione o rappresentazione osservata, anche negli archivi più vecchi.

## Riepilogo, copertura e verifica

Ogni processo blocca le proprie opzioni e l’identità dell’account. L’inventario e le pagine acquisite vengono firmate; le ricevute delle pagine registrano hash, cursori, orari, esiti degli allegati e la ricevuta precedente. Solo le pagine confermate fanno avanzare lo stato di avanzamento. Il riavvio/ripresa verifica tali registrazioni prima di proseguire. Un account modificato, una pagina firmata modificata o una catena di ricevute incoerente vengono rifiutati. Le opzioni non possono essere modificate a metà di un’acquisizione: avviare un altro processo per un altro ambito.

La funzione “Pausa” interrompe l’operazione in corso sull’account. Il riavvio dell’applicazione lascia il lavoro incompiuto disponibile per una ripresa esplicita. Una sessione Takeout scaduta richiede una ripresa esplicita; la modifica degli intervalli di suddivisione di Telegram può richiedere una nuova acquisizione. La ripresa conserva le osservazioni precedenti, quindi un’esportazione di lunga durata non costituisce un’istantanea atomica. Altre operazioni di cambio di account ed esportazioni in conflitto vengono bloccate durante l’acquisizione. Attendere il completamento del packaging prima di eliminare un’area di lavoro.

La funzione "Riprendi" verifica i contenuti già acquisiti prima di proseguire. Gli archivi di grandi dimensioni su supporti di archiviazione lenti possono superare il timeout configurato **in Parametri → Timeout azione pannello** (120 secondi per impostazione predefinita). Aumentare tale impostazione prima di riprovare; l’annullamento o l’interruzione dell’archiviazione lascia un’operazione in pausa, mentre i controlli di integrità falliti lasciano un’operazione fallita con una spiegazione. La verifica deve terminare o arrestarsi in modo sicuro prima che i file possano essere chiusi. Nessuna affermazione relativa alla velocità di elaborazione di account di grandi dimensioni è stata convalidata dai controlli sintetici.

Il pannello distingue un ambito selezionato completato da un archivio parziale e registra le omissioni e le letture non riuscite. I file esclusi deliberatamente sono diversi dai file non disponibili o per cui la lettura non è riuscita. Verifica la copertura anche quando la verifica dell’integrità ha esito positivo. Nessun lettore locale può dimostrare che Telegram abbia restituito ogni messaggio mai esistito.

I ZIP completati rimangono disponibili per download ripetuti e tramite HTTP-range. Un archivio dell’account contiene `manifest.json`, `manifest.sig`, firmati `job.json`, `inventory.json`, `receipts/`, autorevoli `data/*.jsonl`, selezionato `media/`, in formato HTML leggibile e un verificatore. Fissa l’impronta digitale del collettore tramite un canale indipendente, quindi verifica utilizzando un’installazione affidabile:

```
python -m tgwitness.verify account-export.zip --fingerprint TRUSTED_SHA256
```

Per gli archivi il cui contenuto espanso supera i 4 GiB, impostare esplicitamente un limite adeguato `--max-gib`. Il pannello verifica i propri archivi locali autenticati e completati utilizzando la dimensione espansa dichiarata e il digest pubblicato ZIP; la CLI esterna mantiene il proprio limite di dimensione indipendente. Verificare prima di aprire l’HTML leggibile. Il verificatore integrato nell’archivio è comodo, ma un verificatore ottenuto in modo indipendente evita di affidarsi al codice eseguibile fornito insieme alle prove.

La firma Ed25519 e gli hash SHA-256 rilevano le modifiche successive al salvataggio dei byte pertinenti da parte del collettore. Essi non **non** dimostrano che Telegram abbia firmato quei messaggi, che l’operatore del collettore sia stato onesto, che la cronologia dell’account sia completa o che un tribunale accetterà il materiale. I tempi di acquisizione si basano sull’orologio del collettore. I timestamp indipendenti e la provenienza indipendente dell’acquisizione devono essere valutati separatamente.

## Preparare una comunicazione per un avvocato o un altro destinatario

Dopo aver scaricato un’esportazione completata, conservare l’ZIP originale e aprire `index.html` da una copia estratta. Il rapporto illustra l’ambito di applicazione, la copertura disponibile e i limiti. I riferimenti del registro combinano il riferimento all’archivio, il percorso del documento e il numero di registrazione, in modo che il destinatario possa individuare la stessa voce nel codice HTML o nella stampa. Per un esempio pratico, [apri il rapporto fittizio](https://phishdestroy.github.io/TgWitness/demo/report/).

Da un'esportazione dell'account completata, seleziona **«Prepara una copia da condividere**». In questo modo viene creato un derivato separato e firmato. Il file sorgente ZIP rimane invariato e privato; non inviarlo insieme a un derivato ridotto a meno che il destinatario non sia autorizzato a riceverne l'intero contenuto. Scegli separatamente la lingua del report. La modifica della lingua o di qualsiasi impostazione di selezione richiede un'altra anteprima prima della creazione.

1. Inserisci lo scopo della divulgazione e seleziona le date, gli ID dei mittenti e i criteri relativi al testo letterale.
2. È possibile scegliere se mantenere le identità, rivelare solo i partecipanti elencati o pseudonimizzare tutti. In entrambe le modalità di pseudonimizzazione, vengono sostituiti anche gli ID/titoli delle chat e gli ID dei messaggi. Gli pseudonimi rimangono invariati all’interno di una singola divulgazione e cambiano tra divulgazioni preparate in modo indipendente.
3. È possibile mantenere il testo del messaggio, ometterlo completamente oppure aggiungere nomi o frasi letterali da mascherare. Nelle modalità private, lo strumento maschera anche i nomi noti dei mittenti nascosti e i nomi utente alternativi, gli ID mittente composti da token interi, i nomi delle chat dirette, i link, gli indirizzi e-mail e le stringhe simili a numeri di telefono. La corrispondenza dei nomi noti gestisce la conversione maiuscolo/minuscolo Unicode, inclusi `Straße`/`STRASSE`. I titoli generici di gruppi/canali non vengono rimossi automaticamente dal testo del messaggio. Se viene superato il limite di mascheramento delle identità note, restringere l’esportazione di origine oppure omettere il testo; lo strumento rifiuta di saltare silenziosamente i nomi successivi. Si tratta di regole applicate al meglio, non di un’anonimizzazione generale.
4. Non includere i file a meno che il destinatario non ne abbia bisogno. Gli originali inclusi mantengono i propri pixel, audio, testo e metadati. **Non** vengono resi anonimi dallo strumento.
5. Visualizza in anteprima i conteggi, gli avvisi e i messaggi trasformati di esempio, quindi conferma esplicitamente la creazione. Gli esempi sono limitati a 12 messaggi e 2.000 caratteri di testo ciascuno. Si tratta di un esempio, non di una revisione completa del risultato. La modifica delle impostazioni richiede un’altra anteprima. Un’anteprima scade dopo 15 minuti ed è vincolata a quella sessione dell’amministratore e all’ZIP originale esatto; non può essere riutilizzata dopo la creazione. Una nuova anteprima invalida quella precedente per lo stesso lavoro e la stessa sessione.
6. Esamina il risultato completo `index.html` e `messages.jsonl` a livello locale prima di consegnarlo. Se rivela informazioni non necessarie, crea una nuova divulgazione con esclusioni più rigorose. Non modificare l'ZIP firmato in loco.

### Messaggi esclusi dalla selezione

**Anteprima.** Una divulgazione non appare completa quando non lo è. All’interno di ogni chat che contiene almeno un messaggio divulgato, i messaggi esclusi dalla selezione appaiono come indicatori, `[withheld by selection — rule: sender]` (oppure `text`, `period`). Scegliere **«Messaggi esclusi dalla selezione**»: un indicatore per ogni serie di messaggi esclusi consecutivi (impostazione predefinita) oppure uno per ogni singolo messaggio. Gli indicatori riportano solo la regola e un conteggio, mai il testo, il mittente, la data o i file. Le chat prive di messaggi divulgati vengono escluse interamente, pertanto il pacchetto non ne rivela l’esistenza.

Le risposte divulgate indicano a cosa si riferiscono: un messaggio incluso in questa copia, un messaggio escluso dalla selezione o un messaggio che non è presente nell’esportazione di origine (cancellato prima dell’esportazione o mai esportato; l’esportazione non è in grado di distinguere tra le due eventualità). Un messaggio escluso a cui risponde una risposta divulgata riceve sempre un proprio indicatore, in modo che la risposta rimandi a un record che spiega perché è vuoto. Questi tre stati sono distinti dalle cancellazioni e dalle lacune nella raccolta, che appartengono all’esportazione originale.

In `messages.jsonl` (formato `tgwitness-account-disclosure-v2`) ogni messaggio ha `state`: `disclosed`, oppure `withheld` con `rules` e `count`. Una risposta divulgata ha `reply_to` con il destinatario `id` e `state` (`disclosed`, `withheld`, `not_in_source`). Il manifesto conta i messaggi, le chat, i contenuti multimediali e i `withheld` messaggi. `verify.py` Rifiuta un marcatore che contiene contenuto e una risposta che punta a un record mancante dal pacchetto; i pacchetti della versione 1 vengono verificati come in precedenza.

Il formato ridotto omette i profili strutturati degli account, i contatti, gli avatar, le sessioni, le storie, gli oggetti Telegram grezzi, le intestazioni di inoltro, le citazioni nelle risposte, le schede dei contatti e i metadati di localizzazione. Esclude i file JSONL originali, le impostazioni dei filtri privati, la chiave dello pseudonimo e la mappa delle identità. Il testo selezionato, le identità esplicitamente conservate e i file inclusi possono comunque contenere gli stessi nomi, ID o frasi utilizzati in tali filtri; richiedono una revisione separata. La politica privata e la chiave pseudonima vengono conservate in forma crittografata nel vault locale del processo; l’eliminazione del processo cancella i relativi record di divulgazione privata. La politica pubblica registra il numero di filtri anziché i valori dei filtri. Lo scopo dichiarato è pubblico nel manifesto e nell’HTML: i criteri privati espliciti e, nelle modalità pseudonimizzate, anche le identità nascoste note vengono mascherate in tali documenti, anche quando il testo del messaggio viene omesso. Mantenere lo scopo libero da dettagli personali non necessari; il contesto identificativo sconosciuto può rimanere.

Il suo manifesto associa i file derivati, la politica pubblica e l’hash dell’ZIP originale. La verifica consente di accertare l’integrità e, se la fonte è fornita localmente, la corrispondenza del collegamento alla fonte:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Il collegamento alla fonte non dimostra di per sé che la trasformazione abbia selezionato tutti gli elementi richiesti o rimosso tutti i dettagli identificativi. Il testo in chiaro originale non è incorporato come prova. Per giungere a tale conclusione è necessaria una nuova revisione.

## Condivisione e acquisizione in hosting

Selezionare i messaggi e i file necessari al destinatario, esaminare la copia completa condivisa e conservare separatamente la fonte. Registrare l’hash del file ZIP consegnato in modo che il destinatario possa identificare e verificare quella copia esatta. La pseudonimizzazione sostituisce gli identificatori selezionati; il testo incluso e i file originali rimangono parte della revisione.

GitHub Actions supporta l’esportazione dell’intero account e di chat selezionate tramite Takeout o l’API standard, oltre a un registro degli eventi relativo a una singola chat. La guida alla cattura ospitata  spiega la verifica delle impostazioni e il limite di 120 minuti. Per verificare una copia condivisa derivata dalla cattura ospitata, confrontare l’hash della fonte con l’archivio originale e verificare l’attestazione di tale archivio con i controlli specifici della modalità .

[Formato delle prove](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/) · [Rapporti sui casi](https://phishdestroy.github.io/TgWitness/it/docs/reference/case-reports/)
