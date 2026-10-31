# Indagare su tutte le chat

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/cases/

Gestite un intero caso attraverso canali, gruppi, chat private e bot: raccogliete, collegate, ricostruite e consegnate le prove.

Questa guida illustrativa segue lo svolgimento di un incidente fittizio attraverso l’intero account. Utilizza le effettive funzionalità di raccolta, ricerca, profilazione delle persone ed esportazione. La mappa del caso è un esempio di documentazione; le vostre conclusioni e il registro del caso vengono gestiti al di fuori dell’applicazione.

CASO TRATTATO / UNA DESTINAZIONE DI PAGAMENTO MODIFICATA

### Un unico episodio. Quattro conversazioni. Una traccia da ricostruire.

Un annuncio nel canale rimanda a un bot. Un gruppo operativo discute di un nuovo link di pagamento. Un messaggio privato di follow-up lo ripete. Successivamente, l’annuncio viene modificato e un messaggio di gruppo scompare.

Chi ha pubblicato ciascuna versione?Dove è apparso il link?Quale file è stato conservato?Cosa è cambiato e quando?

Per il caricamento della cronologia, la revisione facoltativa delle fonti tramite IA, MCP, OCR e webhook in uscita, consultare la sezione [«Gestisci l’archivio](https://phishdestroy.github.io/TgWitness/it/docs/archive/)».

## 1. Garantire la copertura dell’intero account

1. [Collegate l’account di raccolta](https://phishdestroy.github.io/TgWitness/it/docs/accounts/) nel proprio spazio di lavoro. Registrate il numero di riferimento del caso, l’ID dell’account, il nome dello spazio di lavoro e l’impronta digitale della chiave di firma nelle note relative al caso.
2. **Fonti** aperte **→ Ambito di osservazione → Modalità di indagine**. Esaminare **l’intero account**, tutti e quattro i tipi di fonte e **le proprie azioni**. Questa impostazione predefinita consente di salvare il profilo di una nuova fonte e i suoi ultimi **200 messaggi visibili**. Premere **«Salva ambito»** e completare la conferma dell’ambito.
3. Premere **«Carica chat**». Confrontare le fonti con l’elenco delle conversazioni dell’account e verificare le esclusioni. In **«Parametri» → «Chat lette dall’elenco dell’account**», regolare il limite iniziale dell’elenco se necessario: il valore predefinito è 1.000 conversazioni, configurabile fino a 20.000. Le chat che superano il limite vengono individuate nel momento in cui diventano attive.
4. Nelle **impostazioni di registrazione**, selezionare e salvare **«Tutte le attività visibili**». Verificare i tipi di allegati, i limiti di dimensione e lo spazio libero su disco. Avviare il monitoraggio e verificare il corretto funzionamento della registrazione di messaggi, modifiche e cancellazioni prima di fare affidamento sulla configurazione.

CanaliGruppiChat privateBot

UN ACCOUNT / UNA CHIAVE DI FIRMA**Tutte le attività visibili sull’account selezionato → un unico registro**

Messaggi · modifiche · notifiche di cancellazione · reazioni visibili · eventi relativi all’appartenenza · azioni personali

La modalità «Account completo» comprende le chat a cui questo account può accedere, con i tipi di fonte e le esclusioni configurati. Le chat segrete non sono disponibili. Le nuove finestre di dialogo vengono aggiunte man mano che arrivano gli aggiornamenti; l’attivazione di questa modalità non comporta il download automatico della cronologia completa di ogni chat esistente.

## 2. Acquisizione della cronologia e conservazione dei file

Creare un registro delle fonti per l’intera indagine. Assegnare a ogni chat una riga contenente l’ID numerico, il titolo, l’account, l’accesso/ruolo, l’inizio della registrazione in tempo reale, l’acquisizione della cronologia, i risultati multimediali e le lacune note. Contrassegnare una fonte come acquisita solo dopo aver verificato il risultato pertinente.

| Necessità | Azione nel pannello | Cosa offre |
| --- | --- | --- |
| Cronologia delle chat abilitate | Fonti → Carica cronologia completa | Funzionalità principale attuale: i messaggi passati disponibili vengono inseriti nel registro dell’area di lavoro, con opzioni di pausa/ripresa e un rapporto sullo stato di avanzamento firmato. [Guida alla cronologia](https://phishdestroy.github.io/TgWitness/it/docs/reference/history/). |
| Contesto della chat esistente nel registro | Fonti → Impostazioni di registrazione → Istantanea della cronologia | I messaggi visibili più recenti vengono riportati come osservazioni firmate. Il limite massimo predefinito è 500; la voce **Parametri → «Istantanea della cronologia più estesa»** consente di aumentarlo fino a 10.000. |
| Cronologia completa, attualmente visibile, di una chat | Esportazione completa della chat → Esporta chat completa, oppure Chat → Esporta chat | Un pacchetto separato e firmato contenente `chat.json` e `chat.html`. Ripetere l’operazione per ogni fonte; conservare i risultati relativi al completamento o al fallimento. |
| Contesto in cui compare una nuova chat | Ambito di osservazione → Quando compare una nuova chat o un nuovo bot | Un profilo della fonte e fino a 1.000 messaggi recenti visibili; la modalità «Indagine» ne seleziona 200. Le chat esistenti non beneficiano di questa acquisizione con effetto retroattivo. |
| Byte dell’allegato | Scarica gli allegati visibili + limiti per tipo | Verifichi la presenza di `media.saved`, il relativo SHA-256 e il numero di byte. Un download in coda, saltato o non riuscito non costituisce un file conservato. |

L’esportazione completa di una chat costituisce un’istantanea separata; non importa l’intera cronologia nel registro né nei profili degli utenti. Utilizza **l’opzione “Carica cronologia completa** da tutte le fonti abilitate” o le istantanee del registro limitate per il materiale storico che devi cercare all’interno di TgWitness. Controlla l’elenco delle fonti prima di avviare l’elaborazione.

Nel caso in esame, si acquisiscono il canale di annuncio, il gruppo operativo, la conversazione con il bot e il seguito privato. Si conservano i byte e l’hash dell’allegato della fattura. La cronologia attualmente disponibile non consente di ricostruire un messaggio cancellato prima dell’acquisizione né una modifica intermedia che Telegram non restituisce più.

## 3. Tenete traccia dell’evoluzione della conversazione e delle vostre azioni

Mantenere attivo il monitoraggio man mano che il caso si evolve. Contrassegnare con un asterisco le chat relative al caso in corso come fonti prioritarie; configurare le verifiche prioritarie e quelle su altre fonti in **Impostazioni di registrazione → Verifica**. Esaminare `recheck.completed`, il recupero continuo, FloodWait e i risultati relativi ai file multimediali man mano che il lavoro procede.

Utilizzi **«Chat» → «Profilo» → «Salva profilo ora»** per conservare le descrizioni delle fonti attuali, i comandi del bot e gli altri metadati restituiti da Telegram. Questo profilo della fonte è distinto dai profili delle persone ricavati dai messaggi del registro.

**Seguire un bot o un invito nell’ambito del caso**

1. In **«Chat» → «Apri link Telegram**», salvi prima l’anteprima. Il link originale e l’anteprima restituita diventano registrazioni firmate.
2. Se l’indagine lo richiede, **il comando «Join / open» consente** di accedere alla fonte e avvia un bot con il parametro di avvio specificato. Una richiesta di accesso in sospeso rimane tale nel registro.
3. Per un’azione che si desidera documentare, si utilizzi la risposta testuale del pannello o il comando **«Premere il pulsante»** supportato. Il registro conserva `interaction.requested` e `interaction.result`, compreso il testo o l’URL restituito dal callback.

Questi controlli eseguono azioni effettive su Telegram. Un pulsante di richiamata premuto in un’altra app di Telegram non è visibile al collettore; il messaggio o la modifica successivi del bot potrebbero invece esserlo. Le app web, i pagamenti e le richieste relative al numero di telefono o alla posizione non rientrano nell’ambito del mini-client.

## 4. Tracciare persone, link e file nelle chat

1. Apra **il registro**, lasci il filtro delle fonti su **«Tutte le fonti»** e cerchi una frase distintiva, un dominio, un nome utente o un identificatore salvato. Apra ogni record corrispondente e registri la relativa chat, l’ID del messaggio e il numero di sequenza del registro.
2. Per visualizzare una chat specifica, apra **Chat → Persone → Attiva profili**, quindi selezioni una persona. Esamini la cronologia del nome/nome utente, le relazioni di risposta, l’attività, nonché le voci **«Anche in…»,** altre chat osservate e i link, i portafogli o i numeri di telefono estratti. Apra i record del registro citati.
3. Seguite lo stesso ID utente numerico di Telegram in altre chat all’interno di questo spazio di lavoro. Considerate un nome corrispondente, un riferimento al portafoglio o un avatar simile come un indizio da verificare. Un indirizzo menzionato non costituisce prova di proprietà; un avatar simile non costituisce prova che si tratti della stessa persona.
4. Confronti i valori SHA-256 degli allegati conservati tra i vari record. La corrispondenza degli hash conferma l’identità a livello di byte dei file salvati. Esamini i record relativi ai messaggi e ai mittenti associati prima di trarre conclusioni su chi li abbia condivisi.

MAPPA DEL CASO / SEGUI I RIFERIMENTICaso fittizio · non si tratta di un grafico in tempo reale

CANALE / ANNUNCIO**Originale → versione modificata**

Registrazioni n. 101, n. 188 Messaggio n. 84 · mittente non attribuito

GRUPPO / OPERAZIONI**L’utente 71001 pubblica il nuovo link**

Registrazione n. 146 · messaggio n. 309 Ricevuta del file salvato n. 151

BOT / CONVERSAZIONE RELATIVA ALL’ORDINE**Un pulsante rimanda a tale destinazione**

Registrazione n. 173 · messaggio n. 12 Metadati del pulsante «Torna indietro»

PRIVATO / SEGUITO**L’utente 71001 ripete la destinazione**

Registrazione n. 205 · messaggio n. 922 Ricevuta del file salvato n. 209

Quattro chat forniscono osservazioni diverse. Si prega di seguire i registri originali per ogni connessione; non attribuire il post del canale all’utente 71001 in assenza di un mittente identificato.

Gli ID numerici e i riferimenti ai record sono stati inventati ai fini di questa guida. Questa mappa illustra il flusso di lavoro di un analista che utilizza la ricerca, i profili e l’analisi dei record; l’applicazione non genera un grafico investigativo globale.

| Collegamento | Osservazione a sostegno | Conclusione da mantenere |
| --- | --- | --- |
| Stesso account Telegram | ID utente 71001 nel gruppo n. 146 e nella chat privata n. 205 | Lo stesso ID mittente fornito è stato pubblicato in entrambe le chat. L’identità reale rimane una questione a sé stante. |
| Destinazione ripetuta | `pay.example.invalid/new` nel n. 146, metadati del pulsante n. 173, post modificato n. 188 e n. 205 | La stessa destinazione compare in quattro contesti osservati. Questo fatto, di per sé, non è sufficiente a stabilire chi ne abbia il controllo. |
| Stessa dimensione del file | Valori SHA-256 identici nelle ricevute multimediali completate n. 151 e n. 209 | I due allegati conservati sono identici a livello di byte. I nomi dei file o le miniature da soli non consentirebbero di stabilirlo. |

I profili degli utenti includono gli autori con messaggi salvati in quella chat e li collegano ad altre chat presenti nello *stesso registro dell’area di lavoro*. Non costituiscono un elenco completo degli iscritti. Gli hash degli avatar provengono da una cache locale separata; i riferimenti ai profili hanno un limite configurabile in **Parametri → Record citati per fatto**.

## 5. Ricostruire la sequenza e contrassegnare le lacune

Nella **sezione «Chat»**, esamini le versioni salvate e i relativi link **«Registro n. …**». Nella sezione **«Registro**», utilizzi **«Tutte le fonti»** oltre a **«Modifiche»**, **«Cancellazioni»** e **«Copertura**». Crei una cronologia del caso utilizzando sia la data fornita da Telegram sia l’ora di osservazione del responsabile della raccolta.

1. 09:00 · #101**Post del canale acquisito**

   La destinazione originale viene mantenuta.
2. 09:12 · #146 / #151**Il gruppo introduce un link diverso**

   L’utente 71001 lo pubblica; il download dell’allegato viene completato.
3. 09:16 · #173**Il bot mostra la stessa destinazione**

   I metadati della tastiera salvati contengono il link.
4. 09:20 · #188**Modifiche agli annunci del canale**

   Vengono conservate sia le osservazioni originali che quelle modificate.
5. 09:24 · #205 / #209**Il seguito privato lo ribadisce**

   L’allegato salvato presenta lo stesso SHA-256 completo del n. 151.
6. 09:28 · #231**Arriva la notifica di cancellazione del gruppo**

   Rimane valida l’osservazione precedente: non vengono forniti né l’autore della cancellazione né l’ora esatta della cancellazione.

Esempi illustrativi di orari di osservazione e riferimenti. Tra queste voci sono presenti altre registrazioni nel registro.

L’ordine delle voci nel registro segue la data di ricezione, non necessariamente le azioni originali su Telegram. È possibile che un’istantanea della cronologia più datata compaia dopo un messaggio in tempo reale più recente. Si prega di distinguere chiaramente le osservazioni in tempo reale, le istantanee, i messaggi recuperati, le notifiche di cancellazione e i casi di «mancanza al ricontrollo». Si prega di aggiungere un intervallo esplicito contrassegnato come «sconosciuto» ogni volta che la copertura presenti una lacuna; un’istantanea successiva non cancella tale lacuna.

## 6. Estendere il caso ad altri account di raccolta dati

Aggiungere un’area di lavoro per ciascun account distinto e ripetere l’inventario dell’ambito e della cronologia. Registrare l’appartenenza/il ruolo e l’impronta digitale della chiave di firma per ciascuno di essi. Mantenere gli identificatori qualificati in base all’area di lavoro e alla chat: lo stesso numero di messaggio non costituisce un identificatore globale valido per tutti gli account.

Confronti le osservazioni rilevanti nelle Sue note relative al caso o negli strumenti di analisi, conservando il riferimento all’account e al registro per ogni riga. TgWitness non offre attualmente una ricerca globale, una cronologia unificata, un grafico delle persone o un archivio dei casi trasversale a tutti gli spazi di lavoro. L’esportazione completa multi-account di un singolo canale o supergruppo costituisce una funzionalità a sé stante; non si tratta di una fusione di tutti i registri degli account.

Nel corso di attività di lunga durata, si raccomanda di coinvolgere un [testimone indipendente](https://phishdestroy.github.io/TgWitness/it/docs/witness/) per garantire il rispetto dei limiti stabiliti in precedenza. Si utilizzi il progetto pilota di consegna controllata per verificare i percorsi di acquisizione e la visibilità degli account.

## 7. Fornire un fascicolo completo e verificabile relativo al caso

Esportare un file ZIP contenente il registro firmato da ciascun spazio di lavoro. Esso contiene il registro completo registrato, indipendentemente dai filtri di ricerca del pannello. Esportare separatamente i profili delle persone interessate, conservare ogni pacchetto completo della cronologia delle chat e preservare le prove relative agli allegati.

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

Conservare le impronte digitali attendibili tramite un canale separato. Da un’installazione attendibile, verificare ogni artefatto rispetto alla propria identità dell’area di lavoro:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Verifichi i risultati effettivi del verificatore, conservi gli originali e mantenga il rapporto di copertura, gli errori di acquisizione e il registro dei trasferimenti insieme alle Sue conclusioni. La cartella principale del caso e le conclusioni dell’analista vengono compilate esternamente; i singoli artefatti di TgWitness recano le proprie firme.

## Si utilizzi lo stesso metodo per altre indagini

**Una controversia relativa a un ordine o a un pagamento gestita da un bot**

**Domanda:** cosa prometteva il bot, quale destinazione era stata indicata per il pulsante e cosa è cambiato in seguito?

**Percorso:** post di accesso al canale → anteprima del link del bot salvato → parametro di avvio del bot → messaggi e versioni da tastiera → eventuali ricevute di callback emesse dal pannello → follow-up di gruppo/privato. Abbinare ciascuna destinazione al relativo record di origine; conservare le descrizioni dei profili e i contenuti multimediali completi.

**Contenuti da fornire:** una cronologia dell’offerta osservata e delle relative risposte, i riferimenti alle fonti e le esportazioni verificate. La presenza di un link di pagamento non costituisce prova dell’effettivo avvio del pagamento.

**Messaggi rimossi a seguito di un incidente tra chat**

**Domanda:** cosa era già stato osservato prima che i messaggi rilevanti scomparissero?

**Tracciamento:** tutte le chat interessate → messaggi originali → modifiche consegnate → notifiche di cancellazione o risultati di successiva mancanza al ricontrollo → allegati conservati → copertura relativa all’incidente. Confrontare le osservazioni dei resoconti indipendenti con la loro visibilità dichiarata.

**Da fornire:** una sequenza di versioni conservate e intervalli di tempo esplicitamente indicati come sconosciuti. Non trasformare l’assenza di un messaggio nella cronologia in una prova che una determinata persona lo abbia cancellato.

**Un partecipante cambia nome in diverse chat**

**Domanda:** quale attività osservata appartiene allo stesso account Telegram nonostante il cambio di nome?

**Percorso:** ID numerico del mittente → cronologia dei nomi/nomi utente salvati → risposte → altre chat nell’area di lavoro → destinazioni menzionate e file salvati. Verificare i record di origine per ogni connessione segnalata; tenere separati gli account simili.

**Risultato:** una cronologia citata delle attività dell’account e ipotesi separate sulle relazioni. La somiglianza dei nomi e l’avatar pHash costituiscono indizi, non prove di identità.
