# Indagare su tutte le chat

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/cases/

Gestite un intero caso attraverso canali, gruppi, chat private e bot: raccogliete, collegate, ricostruite e consegnate le prove.

Questa guida passo passo segue un incidente fittizio attraverso l’intero processo. Utilizza le funzioni di raccolta, ricerca e i profili delle persone per individuare i record di origine, [Case Board](https://phishdestroy.github.io/TgWitness/it/docs/case-board/) per organizzarli e discuterne, e [Report Studio](https://phishdestroy.github.io/TgWitness/it/docs/reports/) per presentare i risultati. La mappa illustrata qui sotto spiega le connessioni presenti in questo esempio.

CASO TRATTATO / UNA DESTINAZIONE DI PAGAMENTO MODIFICATA

### Un unico episodio. Quattro conversazioni. Una traccia da ricostruire.

Un annuncio nel canale rimanda a un bot. Un gruppo operativo discute di un nuovo link di pagamento e il bot lo visualizza. L’annuncio viene modificato, un messaggio privato di follow-up ripete la destinazione e un messaggio di gruppo scompare.

Chi ha pubblicato ciascuna versione?Dove è apparso il link?Quale file è stato conservato?Cosa è cambiato e quando?

Per il caricamento della cronologia, la revisione facoltativa delle fonti tramite IA, MCP, OCR e webhook in uscita, consultare la sezione [«Gestisci l’archivio](https://phishdestroy.github.io/TgWitness/it/docs/archive/)».

## 1. Garantire la copertura dell’intero account

Utilizzare un account di raccolta dedicato per l’acquisizione dell’intero account. Gli account principali possono raccogliere chat selezionate o una cartella di Telegram.

1. [Collegate l’account di raccolta](https://phishdestroy.github.io/TgWitness/it/docs/accounts/) nel proprio spazio di lavoro. Registrate il numero di riferimento del caso, l’ID dell’account, il nome dello spazio di lavoro e l’impronta digitale della chiave di firma nelle note relative al caso.
2. **Fonti** aperte **→ Ambito di osservazione → Modalità di indagine**. Esaminare **l’intero account**, tutti e quattro i tipi di fonte e **le proprie azioni**. Questa impostazione predefinita consente di salvare il profilo di una nuova fonte e i suoi ultimi **200 messaggi visibili**. Premere **«Salva ambito»** e completare la conferma dell’ambito.
3. Premere **«Carica chat**». Confrontare le fonti con l’elenco delle conversazioni dell’account e verificare le esclusioni. In **«Parametri» → «Chat lette dall’elenco dell’account**», regolare il limite iniziale dell’elenco se necessario: il valore predefinito è 1.000 conversazioni, configurabile fino a 20.000. Le chat che superano il limite vengono individuate nel momento in cui diventano attive.
4. Nelle **impostazioni di registrazione**, selezionare e salvare **«Tutte le attività visibili**». Verificare i tipi di allegati, i limiti di dimensione e lo spazio libero su disco. Avviare il monitoraggio e verificare il corretto funzionamento della registrazione di messaggi, modifiche e cancellazioni prima di fare affidamento sulla configurazione.

CanaliGruppiChat privateBot

UN ACCOUNT / UNA CHIAVE DI FIRMA**Tutte le attività visibili sull’account selezionato → un unico registro**

Messaggi · modifiche · notifiche di cancellazione · reazioni visibili · eventi relativi all’appartenenza · azioni personali

La modalità «Account completo» comprende le chat a cui questo account può accedere, con i tipi di fonte e le esclusioni configurati. Le chat segrete non sono disponibili. Le nuove finestre di dialogo vengono aggiunte man mano che arrivano gli aggiornamenti; l’attivazione di questa modalità non comporta il download automatico della cronologia completa di ogni chat esistente.

## 2. Acquisizione della cronologia e conservazione dei file

Creare una raccolta "Case Board" per l’indagine e aggiungere ai preferiti i record salvati pertinenti. Tenere un registro delle fonti insieme al caso: ID numerico di ogni chat, titolo, account di raccolta, accesso/ruolo, inizio in tempo reale, acquisizione della cronologia, risultato multimediale e lacune note. Contrassegnare una fonte come acquisita dopo aver verificato il risultato pertinente.

| Necessità | Azione nel pannello | Cosa offre |
| --- | --- | --- |
| Cronologia delle chat abilitate | Fonti → Carica cronologia completa | I messaggi passati disponibili vengono inseriti nel registro dell’area di lavoro, con funzioni di pausa/ripresa e un rapporto sullo stato di avanzamento firmato. [Guida alla cronologia](https://phishdestroy.github.io/TgWitness/it/docs/reference/history/). |
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

1. Aprire **il Journal**, lasciare il filtro delle fonti su **“Tutte le fonti”** e cercare una frase distintiva, un dominio, un nome utente o un identificatore salvato. Aprire ogni record corrispondente, quindi selezionare **“Aggiungi al caso”** per conservare la chat, l’ID del messaggio e il riferimento al journal nel caso.
2. Per visualizzare una chat specifica, apra **Chat → Persone → Attiva profili**, quindi selezioni una persona. Esamini la cronologia del nome/nome utente, le relazioni di risposta, l’attività, nonché le voci **«Anche in…»,** altre chat osservate e i link, i portafogli o i numeri di telefono estratti. Apra i record del registro citati.
3. Seguire lo stesso ID utente numerico di Telegram nelle altre chat presenti in questo spazio di lavoro. Considerare un nome corrispondente, un riferimento al wallet o un avatar simile come un indizio da verificare; conservare i riferimenti alla fonte e qualsiasi attribuzione a supporto.
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

Quattro chat forniscono osservazioni diverse. Seguire i record di origine per ogni connessione; il post sul canale non ha un mittente attribuito.

Gli ID numerici e i riferimenti ai record sono stati inventati ai fini di questa guida. Questa mappa esplicativa mostra come collegare i risultati di ricerca, i profili e i record esaminati; Case Board archivia le schede corrispondenti e i riferimenti alle fonti.

| Collegamento | Osservazione a sostegno | Conclusione da mantenere |
| --- | --- | --- |
| Stesso account Telegram | ID utente 71001 nel gruppo n. 146 e nella chat privata n. 205 | Lo stesso ID mittente fornito è stato pubblicato in entrambe le chat. L’identità reale rimane una questione a sé stante. |
| Destinazione ripetuta | `pay.example.invalid/new` nel n. 146, metadati del pulsante n. 173, post modificato n. 188 e n. 205 | La stessa destinazione compare in quattro contesti osservati. Attribuirne il controllo utilizzando fonti aggiuntive. |
| Stessa dimensione del file | Valori SHA-256 identici nelle ricevute multimediali completate n. 151 e n. 209 | I due allegati conservati sono identici a livello di byte. Gli hash completi dei file consentono il confronto. |

I profili delle persone descrivono gli autori osservati e la loro attività nello *stesso diario dell’area di lavoro*, all’interno delle chat consentite all’utente. Si tratta di una vista degli autori osservati, piuttosto che di un elenco completo dei membri. Regolare il numero di citazioni a supporto in **Parametri → Record citati per fatto**.

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

Utilizza un [gruppo di account](https://phishdestroy.github.io/TgWitness/it/docs/groups/) per verificare lo stato operativo, condividere le impostazioni selezionate ed esportare gli account insieme. Il pacchetto di gruppo conserva il registro firmato e l’identità di ciascun spazio di lavoro. Per un canale o un supergruppo, gli account idonei possono anche suddividersi l’esportazione della cronologia completa. Crea una cronologia trasversale agli account nelle tue note sul caso o negli strumenti di analisi, mantenendo il riferimento allo spazio di lavoro e al registro per ogni riga.

Nel corso di attività di lunga durata, si raccomanda di coinvolgere un [testimone indipendente](https://phishdestroy.github.io/TgWitness/it/docs/witness/) per garantire il rispetto dei limiti stabiliti in precedenza. Si utilizzi il progetto pilota di consegna controllata per verificare i percorsi di acquisizione e la visibilità degli account.

## 7. Consegnare un pacchetto del caso verificabile

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

Verificare i risultati del verificatore, conservare gli originali e archiviare il rapporto di copertura, i risultati dell’acquisizione e il registro di trasferimento insieme alle proprie conclusioni. Redigere le conclusioni in Report Studio e scegliere se il rapporto debba includere il materiale di Case Board. La cartella di primo livello di esempio riunisce i singoli artefatti firmati. Per un destinatario che necessiti solo di materiale selezionato, preparare una [consegna ridotta all’essenziale](https://phishdestroy.github.io/TgWitness/it/docs/handover/).

## Si utilizzi lo stesso metodo per altre indagini

**Una controversia relativa a un ordine o a un pagamento gestita da un bot**

**Domanda:** cosa prometteva il bot, quale destinazione era stata indicata per il pulsante e cosa è cambiato in seguito?

**Percorso:** post di accesso al canale → anteprima del link del bot salvato → parametro di avvio del bot → messaggi e versioni da tastiera → eventuali ricevute di callback emesse dal pannello → follow-up di gruppo/privato. Abbinare ciascuna destinazione al relativo record di origine; conservare le descrizioni dei profili e i contenuti multimediali completi.

**Fornire:** una cronologia dell’offerta osservata e delle risposte, i riferimenti alle fonti e le esportazioni verificate. Supportare qualsiasi affermazione relativa a un pagamento completato con i relativi record di transazione.

**Messaggi rimossi a seguito di un incidente tra chat**

**Domanda:** cosa era già stato osservato prima che i messaggi rilevanti scomparissero?

**Tracciamento:** tutte le chat interessate → messaggi originali → modifiche consegnate → notifiche di cancellazione o risultati di successiva mancanza al ricontrollo → allegati conservati → copertura relativa all’incidente. Confrontare le osservazioni dei resoconti indipendenti con la loro visibilità dichiarata.

**Fornire:** una sequenza di versioni conservate e intervalli espliciti di dati sconosciuti. Mantenere separatamente le segnalazioni di cancellazione, i ricontrolli non andati a buon fine e qualsiasi attribuzione a una persona.

**Un partecipante cambia nome in diverse chat**

**Domanda:** quale attività osservata appartiene allo stesso account Telegram nonostante il cambio di nome?

**Percorso:** ID numerico del mittente → cronologia dei nomi/nomi utente salvati → risposte → altre chat nell’area di lavoro → destinazioni menzionate e file salvati. Verificare i record di origine per ogni connessione segnalata; tenere separati gli account simili.

**Fornire:** una cronologia citata delle attività dell’account e ipotesi separate sulle relazioni. Utilizzare la somiglianza dei nomi e il pHash dell’avatar per selezionare le piste da approfondire nell’analisi delle fonti.
