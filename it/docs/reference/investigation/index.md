# Modalità di indagine

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/

Indagini complete sull’intero account, che abbracciano canali, gruppi, chat private e bot, dall’ambito di applicazione fino alla creazione di un fascicolo verificato.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Investigation](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

Seguite un caso attraverso canali, gruppi, chat private e bot, dall’acquisizione iniziale fino a una cronologia citata e a un passaggio di consegne verificabile. La versione interattiva del sito web è disponibile all’indirizzo `/docs/cases/`; [istruzioni per l’anteprima](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

**On this page**

- [Worked case: a destination changes across four conversations](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/#worked-case-a-destination-changes-across-four-conversations)
- [1. Define the case and collect the whole account](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/#1-define-the-case-and-collect-the-whole-account)
- [2. Inventory every source and acquire historical context](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/#2-inventory-every-source-and-acquire-historical-context)
- [3. Preserve the evolving case and deliberate interactions](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/#3-preserve-the-evolving-case-and-deliberate-interactions)
- [4. Connect observations across chats](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/#4-connect-observations-across-chats)
- [5. Build the cross-chat timeline](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/#5-build-the-cross-chat-timeline)
- [6. Add account perspectives without losing their origin](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/#6-add-account-perspectives-without-losing-their-origin)
- [7. Assemble and verify the case handoff](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/#7-assemble-and-verify-the-case-handoff)
- [Adapt the investigation](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/#adapt-the-investigation)

## Caso di studio: un cambiamento di destinazione in quattro conversazioni

Un annuncio rimanda a un bot. Un gruppo operativo discute una nuova destinazione di pagamento e la tastiera del bot la visualizza. L’annuncio viene modificato, un messaggio privato di follow-up ripete la destinazione e un messaggio di gruppo scompare.

Le domande sono: cosa è stato osservato prima e dopo la modifica, quali account Telegram hanno pubblicato ciascun elemento, dove è apparsa la destinazione, quali byte degli allegati sono stati conservati e quali intervalli rimangono sconosciuti?

Tutti i nomi, gli ID, gli orari e i riferimenti del registro riportati in questo esempio sono fittizi. Il flusso di lavoro utilizza le funzionalità attuali; la mappa del caso è un’illustrazione, non un grafico generato automaticamente dall’applicazione.

Diagramma di flusso · Canali → Registro dell’area di lavoro; Gruppi → Registro dell’area di lavoro; Chat private → Registro dell’area di lavoro; Bot → Registro dell’area di lavoro; Registro dell’area di lavoro → Cerca in tutte le fonti; Registro dell’area di lavoro → Profili delle persone con riferimenti ai registri; Registro dell’area di lavoro → Versioni salvate e conferme di ricezione degli allegati; Cerca in tutte le fonti → Cronologia dell’analista e registro delle fonti; Profili delle persone con riferimenti ai registri → Cronologia dell’analista e registro delle fonti; Versioni salvate e conferme di ricezione degli allegati → Cronologia dell’analista e registro delle fonti; Registro dell’area di lavoro → File ZIP contenente le prove firmate; Cronologia dell’analista e registro delle fonti → Trasferimento del caso con elementi di prova verificati separatamente; File ZIP contenente le prove firmate → Trasferimento del caso con elementi di prova verificati separatamente · Canali · Gruppi · Chat private · Bot · Registro dell’area dilavoro · Cerca in tutte le fonti · Profili delle persone conriferimenti ai registri · Versioni salvate econferme di ricezionedegli allegati · File ZIP contenente leprove firmate · Cronologia dell’analista eregistro delle fonti · Trasferimento del caso conelementi di provaverificati separatamente

**Diagramma sotto forma di testo**

1. Canali → Registro dell’area di lavoro
2. Gruppi → Registro dell’area di lavoro
3. Chat private → Registro dell’area di lavoro
4. Bot → Registro dell’area di lavoro
5. Registro dell’area di lavoro → Cerca in tutte le fonti
6. Registro dell’area di lavoro → Profili delle persone con riferimenti ai registri
7. Registro dell’area di lavoro → Versioni salvate e conferme di ricezione degli allegati
8. Cerca in tutte le fonti → Cronologia dell’analista e registro delle fonti
9. Profili delle persone con riferimenti ai registri → Cronologia dell’analista e registro delle fonti
10. Versioni salvate e conferme di ricezione degli allegati → Cronologia dell’analista e registro delle fonti
11. Registro dell’area di lavoro → File ZIP contenente le prove firmate
12. Cronologia dell’analista e registro delle fonti → Trasferimento del caso con elementi di prova verificati separatamente
13. File ZIP contenente le prove firmate → Trasferimento del caso con elementi di prova verificati separatamente

## 1. Definire il caso e raccogliere l’intera cronologia dei fatti

1. Collegare l’account di raccolta al proprio spazio di lavoro. In [Case Board](https://phishdestroy.github.io/TgWitness/it/docs/reference/case-board/) o nel registro dei casi, registrare il riferimento del caso, l’ID dell’account, lo spazio di lavoro e l’inizio dell’osservazione. Conservare separatamente l’impronta digitale della chiave di firma attendibile.
2. Per un account di raccolta dedicato, aprire **Fonti → Ambito di osservazione → Modalità investigativa**. L’impostazione predefinita seleziona **L’intero account**, canali/gruppi/chat private/bot, azioni proprie, profili delle fonti e gli ultimi 200 messaggi visibili per le fonti appena scoperte. Verifica le impostazioni, premi **“Salva ambito**” e completa la conferma dell’ambito. Gli account principali utilizzano chat selezionate o una cartella; la raccolta dell’intero account è disponibile per gli account contrassegnati per l’indagine.
3. **Caricare le chat** e confrontare le fonti con l’elenco delle conversazioni dell’account. Verificare le esclusioni. **Il parametro «Chat lette dall’elenco dell’account»** è impostato di default su 1.000 e consente un massimo di 20.000. Le fonti che superano il limite dell’elenco vengono aggiunte quando diventano attive. Registrare ciò che è stato effettivamente enumerato.
4. Nelle **impostazioni di registrazione**, selezionare **«Tutte le attività visibili»** e salvare le impostazioni di monitoraggio. Verificare i tipi e i limiti degli allegati e lo spazio libero su disco.
5. Avviare l’osservazione. Convalidare un nuovo messaggio controllato, una modifica e una cancellazione, quindi conservare i riferimenti del test ed eventuali errori.

La modalità «intero account» registra l’attività visibile sull’account secondo le impostazioni salvate. Non accede alle chat segrete né entra automaticamente in tutti i gruppi collegati. Inoltre, non recupera retroattivamente tutte le conversazioni esistenti. Si veda [l’ambito di raccolta](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account).

## 2. Elencare tutte le fonti e acquisire il contesto storico

Tenere un registro delle fonti con una riga per ogni chat:

| Settore | Registrazione |
| --- | --- |
| Identità | Area di lavoro, ID account, ID numerico della chat, titolo e tipo |
| Visibilità | Appartenenza/ruolo, accesso confermato o non confermato, esclusioni |
| Acquisizione in tempo reale | Data di avvio, tipi di eventi selezionati e successive modifiche alle linee guida |
| Cronologia del registro | Istantanee richieste/completate, limiti, tempistiche e riferimenti alle registrazioni |
| Cronologia completa | Nome del file di esportazione firmato per ogni chat, limiti e esito (completamento/fallimento) |
| Allegati | Ricevute multimediali complete, hash, dimensioni e risultati saltati o non riusciti |
| Ambito di applicazione | Interruzioni del servizio, acquisizione incompleta, FloodWait, messaggi non disponibili e altre lacune |

Utilizzi il metodo di acquisizione adeguato per ciascuna fonte:

- **L'opzione «Carica cronologia completa** nelle **fonti»** carica i messaggi passati disponibili dalle fonti abilitate nel registro dell'area di lavoro. Supporta la funzione di pausa/ripresa e un rapporto di avanzamento firmato. Vedi [acquisizione della cronologia](https://phishdestroy.github.io/TgWitness/it/docs/reference/history/).
- **L’istantanea della cronologia** salva i messaggi visibili più recenti nel registro di osservazione. Il limite massimo predefinito è 500; **in Parametri → Istantanea della cronologia più ampia** è possibile aumentarlo fino a 10.000. Si tratta di osservazioni della cronologia attuale, non di modifiche ricostruite.
- **Esportazione completa della chat → Esporta chat completa**, oppure **Chat → Esporta chat**: questa operazione recupera la cronologia attualmente visibile di una chat in un bundle separato e firmato `chat.json` / `chat.html`. Ripetere l’operazione per le fonti del caso e conservare ciascun risultato.
- **Quando compare una nuova chat o un nuovo bot,** è possibile salvarne il profilo e fino a 1.000 messaggi recenti; la modalità «Indagine» ne seleziona 200. Le chat esistenti non ricevono tale acquisizione in modo retroattivo quando la modalità viene attivata.
- **Il download degli allegati visibili** conserva i byte in base alla politica configurata. È necessario un ricevimento `media.saved` completo con SHA-256 e conteggio dei byte. Un’attività in coda, una miniatura o un nome di file non costituiscono l’allegato conservato.

L’esportazione completa di una chat **non** popola il registro né i profili degli utenti con tutti i suoi messaggi. Utilizza **“Carica cronologia completa”** o “Istantanee del registro limitate” per la cronologia che devi analizzare all’interno di TgWitness. Controlla l’elenco delle fonti abilitate prima di avviare un’elaborazione della cronologia. Nessuna delle due opzioni recupera il materiale che Telegram non restituisce più.

## 3. Conservare l’evoluzione del caso e le interazioni deliberate

Contrassegnare le chat relative a casi attivi come fonti prioritarie. Verificare gli intervalli di ricontrollo, il recupero continuo dei dati e i risultati relativi ai file multimediali. Mantenere attivo il collettore durante l’utilizzo dell’account. Utilizzare **Chat → Profilo → Salva profilo ora** per conservare i metadati delle fonti, quali descrizioni e comandi dei bot. Ciò è distinto dai profili delle persone ricavati dai messaggi salvati.

Nel caso in cui si debba seguire una fonte o interagire con un bot:

1. **Aprire il link di Telegram → Salva anteprima:** registra il link fornito e l’anteprima restituita prima di un’azione.
2. **Il comando «Join / open and observe»** esegue l’operazione di join/open e invia il parametro di avvio del bot, se specificato. Una richiesta di join in attesa di approvazione viene registrata come “in sospeso”.
3. Le risposte testuali inviate dal pannello e le pressioni dei pulsanti supportate conservano `interaction.requested` e `interaction.result`. Le conferme di callback possono conservare il testo del popup restituito, lo stato di avviso e l’URL.

Si tratta di azioni effettive dell’account. Le pressioni del tasto di richiamata in un’altra app Telegram non sono visibili al raccoglitore, sebbene possano esserlo i messaggi o le modifiche che ne derivano. Il mini-client non esegue flussi di lavoro relativi ad app web, pagamenti, telefono o posizione. Per il comportamento esatto, si vedano [le interazioni con i pannelli](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/#act-from-the-panel).

## 4. Collegare le osservazioni tra le diverse chat

In **«Journal»**, selezionare **«Tutte le fonti»** e cercare i contenuti registrati. Aprire i record corrispondenti e prendere nota dell’area di lavoro, della chat, dell’ID del messaggio, della sequenza e dell’hash del record.

In una chat pertinente, apra **«Persone» → «Attiva profili»** e esamini una persona:

- Nomi/nomi utente rilevati nel corso del tempo e l’ID numerico di Telegram.
- Relazioni tra le risposte con riferimenti alle registrazioni originali.
- **Inoltre, in…** altre chat presenti in questo registro dell’area di lavoro in cui quell’ID ha scritto.
- Attività, modifiche/cancellazioni e portafogli, telefoni, nomi utente e link menzionati.
- Metadati degli avatar salvati e avatar simili memorizzati nella cache, con la rispettiva provenienza indicata separatamente.

Si prega di aprire i record citati prima di utilizzare un profilo derivato in una conclusione. I profili riguardano le persone con messaggi salvati, non tutti i membri del gruppo. **L’opzione Parametri → Record citati per fatto** limita l’elenco dei riferimenti, non il conteggio delle attività sottostanti. Le menzioni e la somiglianza degli avatar costituiscono indizi; non stabiliscono la titolarità né l’identità.

Nell’esempio elaborato:

| Link | Registrazioni | Osservazione supportata |
| --- | --- | --- |
| Stesso account del mittente | Gruppo n. 146 e follow-up privato n. 205 | Entrambi riportano l’ID mittente Telegram 71001 |
| Stessa destinazione | #146, tastiera del bot #173, modifica del canale #188, messaggio privato #205 | Tutti contengono il codice `pay.example.invalid/new`; la titolarità o il controllo non sono stati accertati |
| Stesso file salvato | Ricevute multimediali completate n. 151 e n. 209 | I valori SHA-256 completi corrispondono per i byte conservati |
| Attribuzione del canale | #101 e #188 | Non attribuire un post del canale all’utente 71001 senza indicare il mittente |

Compare attachment hashes and their associated message references, and keep account timelines grouped by the Telegram IDs supplied in those records.

Conservare le note di lavoro del team su [Case Board](https://phishdestroy.github.io/TgWitness/it/docs/reference/case-board/): aggiungere ai segnalibri i record su cui ci si basa, come #146, #188 e #205, evidenziare la stringa di destinazione esatta e salvare una porzione di ogni azione registrata tra due record o in un intervallo di tempo. Le note e gli stati conservano la revisione del team nella propria cronologia firmata, separatamente identificabile dalle osservazioni di origine.

## 5. Creare la cronologia tra le chat

Utilizzi le versioni salvate nelle **chat** e i relativi link **al registro n. … del Journal**. Nel **Journal**, combini **tutte le fonti** con **le modifiche**, **le cancellazioni** e **la copertura**. Conservi sia `source_at`, ove fornito, sia `observed_at`.

| Tempo di osservazione illustrativo | Riferimento | Osservazione |
| --- | --- | --- |
| 09:00 | Canale n. 101 | Destinazione originale acquisita |
| 09:12 | Gruppo n. 146; media n. 151 | Nuova destinazione pubblicata; download del file completato |
| 09:16 | Bot n. 173 | La tastiera indica la nuova destinazione |
| 09:20 | Canale n. 188 | Annuncio modificato; entrambe le versioni salvate rimangono disponibili |
| 09:24 | Privato #205; media #209 | Lo stesso ID mittente ripete la destinazione; gli stessi byte del file vengono conservati |
| 09:28 | Gruppo n. 231 | Avviso di cancellazione ricevuto; autore della cancellazione e ora esatta della cancellazione sconosciuti |

Altre registrazioni si verificano tra questi riferimenti di esempio. I numeri di sequenza ordinano le osservazioni; le istantanee della cronologia possono contenere date di origine più vecchie e pervenire successivamente rispetto agli eventi in tempo reale. Si distinguano le istantanee, i messaggi recuperati, le notifiche di cancellazione e i risultati di «mancante al ricontrollo». Contrassegnare le lacune di copertura come intervalli sconosciuti. L’acquisizione successiva della cronologia non garantisce retroattivamente un’osservazione ininterrotta.

## 6. Aggiungere le prospettive degli account senza perderne l’origine

Utilizzi uno spazio di lavoro separato per ogni account distinto e ne ripeta l’inventario. Conservi l’ID dell’account, il ruolo, l’impronta digitale della chiave di firma e i riferimenti alla fonte in occasione di ogni confronto. I numeri dei messaggi non sono identificatori globali validi per tutte le chat o tutti gli account.

Case Board conserva le note e le raccolte collegate alle fonti all’interno di ciascun spazio di lavoro. La schermata di gruppo consente di esaminare collettivamente lo stato degli account e di raggruppare le esportazioni separate dagli spazi di lavoro. È possibile correlare tali fonti nelle note del caso o negli strumenti di analisi; ogni registro mantiene la propria origine e la propria chiave di firma. Non viene generata una ricerca globale né una timeline unificata tra gli spazi di lavoro. L’esportazione multi-account di un canale/supergruppo acquisisce la cronologia di quella chat utilizzando gli account idonei.

Per attività di maggiore entità, si raccomanda di avvalersi di un [testimone indipendente](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/). Utilizzare controlli di consegna controllati per verificare il percorso di acquisizione e la visibilità di ciascun account.

## 7. Compilare e verificare il passaggio di consegne del caso

Si prega di conservare questi elementi in un fascicolo del caso compilato da un analista:

| Materiale | Scopo |
| --- | --- |
| Note sul caso e registro delle fonti | Domande, politica di raccolta, accesso/ruolo, risultati, spiegazioni alternative e lacune |
| Cronologia | Per ogni voce sono indicati sia l’ora che i riferimenti relativi all’area di lavoro, alla chat, al messaggio e alla sequenza |
| Case Board esportazione e segmenti, se utilizzati | Segnalibri collegati alla fonte, citazioni, note del team, raccolte, cronologia delle revisioni e record selezionati verificati rispetto al file ZIP contenente le prove |
| File ZIP contenente le prove firmate per ogni area di lavoro | Registro completo delle registrazioni, elenco dei contenuti e file multimediali conservati inclusi; i filtri del pannello non limitano l’esportazione del registro |
| File dei profili personali firmati separatamente | I riferimenti derivati sono stati verificati confrontandoli con le prove presenti nell’area di lavoro corrispondente |
| Esportazioni complete e firmate delle chat | Acquisizione della cronologia visibile attuale, separata dal registro di osservazione |
| Impronte digitali attendibili e punti di controllo precedenti | Identità chiave e limiti del registro conservato |
| Elementi di prova, se configurati | Registro separato, post firmati e impronta digitale del testimone |
| Risultati della verifica e hash dei file forniti | Cosa è stato verificato, quali byte sono stati trasferiti e a chi |

Da un’installazione attendibile, con i nomi dei file e l’impronta digitale effettiva di ciascun spazio di lavoro:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Mantenere i risultati effettivi della verifica e gli artefatti originali. Esportare le note dell’area di lavoro da Case Board insieme al materiale di riferimento citato. Raggruppare i risultati relativi a più aree di lavoro nella directory di primo livello del caso; ogni artefatto di TgWitness ha una propria firma e una propria procedura di verifica.

## Adattare l’indagine

| Caso | Trace | Consegna |
| --- | --- | --- |
| Controversia relativa a ordini/pagamenti gestita da bot | Annuncio di inserimento → anteprima del link salvato → parametro di avvio del bot → versioni dei messaggi e della tastiera → ricevute di callback del pannello → follow-up privato/di gruppo | Sono state osservate le tempistiche delle offerte e delle risposte e sono state verificate le fonti; un semplice link di pagamento non costituisce di per sé prova di un pagamento |
| Messaggi rimossi a seguito di un incidente | Tutte le chat interessate → originali e modifiche salvati → esiti relativi a cancellazioni o messaggi mancanti al momento della verifica successiva → contenuti multimediali conservati → copertura e altre prospettive relative all’account | Versioni conservate e intervalli di tempo esplicitamente indicati come sconosciuti; nessun autore di cancellazione inventato |
| Un partecipante cambia nome nelle diverse chat | Numeric sender ID → name/username history → replies → other observed chats → cited destinations/files | Una cronologia delle attività di un account Telegram con collegamenti ai relativi record di origine |

[Riferimento alla raccolta](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/) · [Verifica dei profili delle persone](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#people-profiles) · [Trasferimento delle prove](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#investigation-handoff) · [Convalida completata](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/)
