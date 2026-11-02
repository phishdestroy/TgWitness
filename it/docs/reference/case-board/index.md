# Riferimento a Case Board

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/case-board/

Segnalibri, evidenziazioni precise, sezioni di azione, discussioni, accesso limitato e cronologia delle annotazioni firmate utilizzate da Case Board.

Case Board offre al team investigativo una visione condivisa del materiale salvato. È possibile aggiungere un segnalibro a un’ osservazione, evidenziare un passaggio preciso, salvare una serie di azioni e discuterne con i colleghi. Le schede conservano i riferimenti alle fonti e la cronologia delle revisioni firmata. Le annotazioni del team rimangono nell’ area di lavoro, distinguibili dalle osservazioni originali di Telegram.

[Modello probatorio](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/) · [Accesso](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/) · [Rapporti](https://phishdestroy.github.io/TgWitness/it/docs/reference/case-reports/)

![Feed sintetico delle indagini](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

## Lavorare su un caso

Aprire **Investigazione → Case Board** in modalità Standard o Esperto. La lingua segue quella del pannello. Utilizzare **il** **pulsante** **«Aggiungi alla bacheca»** accanto a una voce del diario o a un messaggio di chat salvato, oppure selezionarlo e premere **B**. Il segnalibro viene aggiunto alla Posta in arrivo con un solo clic. Modificarne il titolo, le etichette e la nota, oppure spostarlo in una raccolta. Una scheda modificata aggiunge una revisione firmata; la sua rimozione conserva la cronologia.

Per un primo caso, scegli una raccolta e aggiungi i record che rispondono a una domanda. Usa i commenti per rivedere l’interpretazione, poi **la sezione “Presentazione”** per scorrere le schede e il contesto delle fonti. Scegli separatamente il materiale per la bacheca del caso in [Report Studio](https://phishdestroy.github.io/TgWitness/it/docs/reference/case-reports/) quando prepari il documento finale. Il salvataggio di una sezione non configura automaticamente i filtri dei dati di un report.

Selezionare il testo all’interno di un messaggio di chat salvato per visualizzare **Evidenzia → bacheca**. Selezionarne il colore e aggiungere una nota. Il server verifica la citazione esatta e la versione salvata, inclusi emoji, testo RTL e segni di combinazione. L’interfaccia non mappa una selezione attraverso testo mascherato o trasformato.

Clicca tenendo premuto il tasto Maiusc su due record in una chat per selezionare **“Slice between**”, usa **“Slice by time**” oppure salva i filtri attuali del Journal relativi a chat, periodo e tipo di evento. Una sezione salvata ha un proprio predicato autorevole: aprirla nel Journal applica anche chat multiple, limiti al numero di messaggi e filtri relativi agli attori . L’opzione **“Mostra record aggiunti dopo il segnalibro**” isola le aggiunte successive. La modifica dei filtri di Journal comporta l’uscita dalla sezione. Da “Persone”, **l’opzione “Seleziona le azioni di questa persona”** utilizza l’ID dell’attore registrato; non presuppone che l’autore del messaggio abbia modificato, cancellato o reagito a un messaggio.

La finestra di dialogo “Slice” mostra un’anteprima dei conteggi prima di consentire la creazione. Il termine “`all`” include ogni tipo di dato registrato, comprese istantanee, modifiche, cancellazioni, reazioni, aggiornamenti relativi all’appartenenza o al servizio, azioni personali, pulsanti, risultati multimediali, messaggi recuperati e tipi di eventi futuri. La selezione descrive le osservazioni salvate. Le notifiche di cancellazione delle chat sconosciute costituiscono un contesto separato, disponibile solo con accesso all’intero spazio di lavoro, mai attribuito a una delle chat selezionate.

Le raccolte hanno un ambito di chat dichiarato. Un ambito vuoto indica l’intero spazio di lavoro. Una raccolta non può contenere schede al di fuori del proprio ambito; un partecipante con accesso limitato a una chat non può leggere una raccolta più ampia. La Posta in arrivo è una raccolta virtuale per le schede non assegnate. La ricerca e i filtri coprono solo le schede visibili; i thread e le menzioni ereditano l’accesso della scheda padre. I commenti rimossi hanno un segnalino di eliminazione nella discussione. Non viene registrata alcuna cronologia di visualizzazione.

**La modalità "Presentazione"** apre tutte le schede della raccolta selezionata, con le visualizzazioni "Scheda", "Contesto della fonte" e "Commenti del team" e i comandi da tastiera "Precedente"/"Successivo". Non fornisce comandi di modifica. Il feed standard è impaginato; la modalità "Presentazione" carica l'elenco a pagine e recupera i dettagli di una scheda alla volta.

## Autorizzazioni

Tutte le operazioni richiedono l’accesso a `view`, all’ambito dell’area di lavoro/chat e a `board.read`. `board.write` aggiunge schede, commenti, spostamenti e stati di apertura/revisione. `board.manage` consente la gestione della raccolta, gli stati “confermato”/“respinto”, le revisioni e la rimozione delle schede di altri utenti. Uno stato rappresenta una decisione del team, non il risultato di una verifica crittografica.

Impostazioni predefinite per l’accesso ai moduli: Revisore = lettura; Analista = lettura/scrittura; Operatore = lettura/scrittura/gestione, oltre alle autorizzazioni già in loro possesso. Le autorizzazioni esistenti non comportano l’acquisizione automatica di nuovi diritti. L’amministratore principale dispone di tutti i diritti e pubblica come **Amministratore principale**. Utilizzare autorizzazioni denominate per l’attribuzione. Le menzioni elencano solo gli accessi attuali in grado di leggere la scheda principale completa.

Un'autorizzazione per la chat A non può ottenere una scheda o uno slice per A+B, nemmeno indovinandone l’ID o fornendo un `target.chat_id` falso. I metadati di destinazione vengono risolti dall’hash dell’evento firmato sul server. Le raccolte, il conteggio delle discussioni, le schede correlate e le notifiche in tempo reale vengono filtrati prima della risposta. Le esportazioni richiedono sia `export` che `board.read`; un esportatore esistente senza accesso alla bacheca ottiene il normale archivio delle prove senza le note del team. SSE ricontrolla le autorizzazioni attuali prima di ogni batch.

## Contratti archiviati

Come le osservazioni, le annotazioni vengono scritte in modo transazionale in una tabella SQLite di sola aggiunta nell’ area di lavoro. `annotations.jsonl` è la sua esportazione canonica esatta dallo stesso snapshot di lettura di `events.jsonl`. Non esiste un secondo archivio di annotazioni concorrente né alcun evento di registro `board.activity`.

Ogni riga deve contenere esattamente:

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

L’esempio abbreviato sopra illustra la struttura esterna; i payload effettivi includono le impostazioni predefinite del modello e i campi di destinazione risolti dal server. Gli schemi delle richieste API si trovano in [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json), generati dai modelli Pydantic di runtime tramite lo scrip`python tools/build_board_schemas.py`. I campi di richiesta aggiuntivi vengono rifiutati. Gli ID vengono generati lato server se omessi. Autore, ora, istantanea e firma non possono essere forniti dal chiamante. Gli ID di autorizzazione con nome seguono il formato esadecimale a 16 cifre esistente di Access; gli ID delle carte sono a 32 cifre esadecimali.

Il JSON canonico è in UTF-8, con chiavi degli oggetti ordinate, senza spazi tra i token, Unicode non escapato, e senza NaN/infiniti. L’hash dell’annotazione è un SHA-256 dell’oggetto canonico contenente il `format: "tgwitness-annotations-v1"` e tutti e sette i campi dell’involucro fino a `previous_hash`. Questo tag di formato separa il proprio dominio hash dalle osservazioni. La firma è Ed25519 sui 32 byte grezzi dell’hash. La sequenza inizia da 1. Le revisioni mantengono l’ID della scheda e indicano l’hash dell’annotazione precedente nel campo «`supersedes`»; non possono modificare l’ambito della chat. Spostamenti, stati e rimozioni sono record separati. La tabella SQLite rifiuta i comandi UPDATE e DELETE.

`case-board.json` contiene `{statement, signature}`. La dichiarazione canonica è firmata dalla chiave dell’area di lavoro e contiene `format: "tgwitness-case-board-v1"`, `public_key`, `created_at`, `journal_head`, `meaning` e `state`. Lo stato è una riproduzione deterministica: `annotations_head`, un array ordinato di `items` (raccolte, schede, commenti inclusi i tombstone) e `status_history`. Gli elementi conservano l’hash dell’ultima annotazione, la sequenza, l’autore e l’ora, nonché il creatore originale e l’ora di creazione attraverso le revisioni. La riproduzione verifica le revisioni, i genitori, i riferimenti alle collezioni e gli ID delle azioni duplicati. Anche ``manifest.json`` e i nuovi checkpoint associano ``annotations_head``. Conservare un checkpoint in modo indipendente per rilevare troncamenti o riscritture con una chiave di firma copiata.

### Versioni testuali

`range.start` è un offset del codice Unicode con base zero, `length` è un conteggio positivo dei codici, e `quote` deve corrispondere esattamente alla sottostringa di `payload.text` o `payload.caption` nell’evento di destinazione. Non vengono applicati NFC/NFKC, conversione maiuscole/minuscole o normalizzazione dei grafemi. Gli slice di stringhe in Python e `Array.from(text)` in JavaScript implementano la stessa indicizzazione. La combinazione di segni e emoji ZWJ può occupare diversi punti di codice. `range.version` è l’hash dell’evento di destinazione, non la versione corrente del messaggio né l’offset dell’entità UTF-16 di Telegram. Le modifiche successive non riposizionano mai automaticamente un’evidenziazione.

### Identità e ora

La `query` accetta esattamente un `chat_id` o `chat_ids` non vuoti, intervalli opzionali `from`/`to`, intervalli inclusivi di ID messaggio (una sola chat), `kinds: "all"` o tipi con caratteri jolly esatti/prefissi, `actors` espliciti, `search`, `hide_system` e `include_unscoped`. I gruppi di tipi di journal si espandono nei loro predicati esatti. La ricerca utilizza la ricerca del payload NFC/case-folded del journal senza alterare il testo sorgente firmato. Le date richiedono un fuso orario e vengono normalizzate in UTC. Le date filtrano **`observed_at`**. Il ``source_at`` di Telegram viene visualizzato separatamente. Una cancellazione senza un timestamp di origine non ha un’ora di cancellazione inventata. Un record tardivo osservato al di fuori di un intervallo di tempo non vi entra; una porzione di ID dei messaggi può includere una cancellazione successiva per quegli ID dei messaggi.

Lo `snapshot`a fissa l’ora di creazione, la sequenza del journal/il confine dell’hash, il conteggio delle corrispondenze, la prima/ultima sequenza e il `result_hash`. Quest’ultimo è l’SHA-256 dell’array JSON canonico in UTF-8 degli hash degli eventi corrispondenti ordinati lessicograficamente, incluso `[]` per una slice vuota. Contiene inoltre il conteggio esatto dei tipi e una miniatura del tempo di osservazione a 24 bin. Una sezione memorizza una query, non record di origine duplicati . All’esportazione, `board/slices/<id>.json` elenca gli hash correnti e le sequenze aggiunte/rimosse. Il verificatore ricostruisce il risultato originale al momento della creazione, quindi il risultato corrente. I record aggiunti vengono segnalati come un fatto di modifica. La rimozione di un evento originale interrompe la catena di prove immutabile; non viene accettata silenziosamente come una normale rimozione da una sezione.

Gli snapshot delle reazioni presentano elenchi incompleti degli attori recenti. L’explorer confronta snapshot adiacenti della stessa chat/messaggio, incluso un predecessore al di fuori dello slice, e riporta i differenziali di conteggio aggregati **tra le osservazioni**. Non si presume che gli attori recenti mancanti abbiano rimosso una reazione. La prima istantanea non presenta uno stato precedente dedotto. Le osservazioni degli attori rimangono attribuite all’ istantanea in cui sono state fornite, non a un momento d’azione inventato.

## API ed esportazioni

`GET /api/board` accetta collection/chat/author/label/state/from/to/q/kind/comments, offset/limit e l’ordinamento newest/oldest. `GET /api/board/card/{id}` restituisce una scheda, l’anteprima della fonte, il thread, la cronologia dello stato e le schede correlate. La sottoruta dei partecipanti restituisce le menzioni idonee. `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}` aggiunge un record. `POST /api/board/slice-preview` calcola una query. I record delle sezioni sono suddivisi in pagine tramite `GET /api/board/slice/{id}/records`; il ricalcolo utilizza sempre l’istantanea di lettura stabile corrente. `/api/stream` in tempo reale emette notifiche della `board` prive di payload, separatamente dai cursori del diario.

`GET /api/board/export` restituisce un documento firmato. L’accesso limitato alla chat riceve una **divulgazione** firmata chiaramente etichettata, mai le annotazioni di un’altra chat né la catena completa. I file ZIP contenenti le prove complete contengono `annotations.jsonl`, `case-board.json` firmato e appendici JSON delle sezioni. Le impostazioni del report in HTML/PDF/JSON consentono di selezionare «nessuna bacheca», segnalibri/sezioni senza discussione o schede con commenti. La sezione separa esplicitamente le opinioni del team dalle osservazioni. I filtri dei dati del report limitano anche le note leggibili; i file sorgente completi e firmati nel file ZIP delle prove rimangono integri.

`GET /api/board/slice/{id}/export` produce un estratto JSON firmato denominato «`tgwitness-board-selection-v1`»; `?format=csv` produce una tabella di facile consultazione senza firma autonoma. Mantenere il formato JSON e ZIP:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

Il controllo di selezione autentica la dichiarazione firmata, i record di origine esatti e la completezza della sua query entro il limite specificato. Il file ZIP contenente le prove può essere più recente, ma deve contenere quel prefisso. Un target non risolvibile viene segnalato esplicitamente. Uno snapshot originale diverso, un’annotazione modificata, uno stato di riproduzione non corrispondente o una fonte modificata comportano un errore. I vecchi archivi senza annotazioni mantengono il loro comportamento di verifica esistente.

L’impostazione predefinita per il passaggio di consegne è **«Non includere**». L’inclusione esplicita proietta le schede attraverso i record già ridotti al minimo, omette i destinatari inaccessibili/omessi, esclude le evidenziazioni il cui testo di origine è stato ridotto al minimo, pulisce il testo del team con le stesse regole relative alle menzioni/ai contatti e, facoltativamente, sostituisce le etichette degli investigatori con R01, R02… nei metadati e nelle occorrenze note nelle note. Non viene divulgato alcun file « `annotations.jsonl`» originale. Il sidecar «`tgwitness-case-board-handover-v1`» firmato e il report contengono lo stesso materiale minimizzato. Il conteggio delle sezioni descrive solo i record divulgati, con i dettagli originali relativi agli autori degli snapshot/query omessi. I nomi in testo libero non noti al minimizzatore richiedono comunque una revisione, come avviene nei normali passaggi di consegne. Questo derivato non pretende di preservare le firme delle annotazioni originali dopo la redazione.

## Limiti operativi

I parametri includono limiti soft di 10.000 schede e 50.000 commenti, una pagina di estratti con un massimo di 5.000 record e il controllo dell’anteprima dei file multimediali. I limiti soft generano un avviso senza cancellare la cronologia. Le pagine dei feed contengono al massimo 200 schede. Gli estratti JSON autonomi sono limitati a 64 MiB; restringere la query o utilizzare il file ZIP firmato per materiale più voluminoso. Il verificatore autonomo limita la riproduzione delle annotazioni a 256 MiB. Case Board non abilita né implementa notifiche esterne relative ai commenti.

L’accettazione automatizzata della funzionalità utilizza dati fittizi e un trasporto Telegram simulato per verificare l’archiviazione, l’accesso, la visualizzazione e le esportazioni. Consultare [l’ambito di verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#verification-scope) per conoscere la portata dei controlli sulle prove.
