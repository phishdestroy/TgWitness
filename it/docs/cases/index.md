# Indagare su tutte le chat

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/cases/

Un caso intero tra canali, gruppi, chat private e bot: raccogliere, collegare i punti, ricostruire la cronologia, consegnare.

Un incidente inventato, dall’inizio alla fine. Raccolta, ricerca e profili delle persone trovano le voci, [Case Board](https://phishdestroy.github.io/TgWitness/it/docs/case-board/) le organizza, [Report studio](https://phishdestroy.github.io/TgWitness/it/docs/reports/) le presenta.

CASO TRATTATO / UNA DESTINAZIONE DI PAGAMENTO MODIFICATA

### Un unico episodio. Quattro conversazioni. Una traccia da ricostruire.

Un post di un canale rimanda a un bot. Un gruppo parla di un nuovo link di pagamento e il bot lo mostra. Il post viene modificato, una chat privata ripete il link, un messaggio del gruppo sparisce.

Chi ha pubblicato ciascuna versione?Dove è apparso il link?Quale file è stato conservato?Cosa è cambiato e quando?

Caricamento della cronologia, IA, MCP, OCR e webhook: [Lavorare l’archivio](https://phishdestroy.github.io/TgWitness/it/docs/archive/).

## 1. Garantire la copertura dell’intero account

Ambito intero account solo su un account dedicato. Un account principale usa chat scelte o una cartella.

1. [Colleghi l’account](https://phishdestroy.github.io/TgWitness/it/docs/accounts/) in uno spazio proprio. Annoti riferimento del caso, ID account, spazio e impronta della chiave.
2. **Fonti → Ambito di osservazione → Modalità indagine**: **Intero account**, tutti e quattro i tipi di fonte, **Azioni proprie**. Ogni nuova chat ha profilo e ultimi **200 messaggi visibili** salvati. **Salva ambito** e confermi.
3. **Carica chat** e confronti con l’elenco chat dell’account. Il limite è di 1.000 dialoghi (fino a 20.000 in **Parametri → Chat lette dall’elenco dell’account**); quelle oltre compaiono quando diventano attive.
4. **Impostazioni di registrazione** → **Tutta l’attività visibile**, controlli limiti degli allegati e spazio su disco. Avvii, poi provi con un messaggio, una modifica e un’eliminazione.

CanaliGruppiChat privateBot

UN ACCOUNT / UNA CHIAVE DI FIRMA**Tutte le attività visibili sull’account selezionato → un unico registro**

Messaggi · modifiche · notifiche di cancellazione · reazioni visibili · eventi relativi all’appartenenza · azioni personali

«Intero account» significa ogni chat che questo account può aprire, meno le esclusioni. Niente chat segrete. Le nuove chat si aggiungono man mano; la cronologia vecchia non viene scaricata da sola.

## 2. Acquisizione della cronologia e conservazione dei file

Crei una raccolta Case Board e segni ciò che conta. Tenga un registro delle fonti: ID chat, titolo, account, ruolo, inizio della cattura in diretta, risultato della cronologia, risultato dei media, lacune.

| Necessità | Azione nel pannello | Cosa offre |
| --- | --- | --- |
| Cronologia delle chat abilitate | Fonti → Carica cronologia completa | I messaggi passati disponibili vengono inseriti nel registro dell’area di lavoro, con funzioni di pausa/ripresa e un rapporto sullo stato di avanzamento firmato. [Guida alla cronologia](https://phishdestroy.github.io/TgWitness/it/docs/reference/history/). |
| Contesto della chat esistente nel registro | Fonti → Impostazioni di registrazione → Istantanea della cronologia | Messaggi recenti come voci firmate. 500 di default, fino a 10.000 in **Parametri → Istantanea di cronologia più grande**. |
| Cronologia completa, attualmente visibile, di una chat | Esportazione completa della chat → Esporta chat completa, oppure Chat → Esporta chat | Un pacchetto firmato a parte con `chat.json` e `chat.html`, uno per chat. |
| Contesto in cui compare una nuova chat | Ambito di osservazione → Quando compare una nuova chat o un nuovo bot | Il suo profilo e fino a 1.000 messaggi recenti (200 in modalità indagine). Non vale per le chat esistenti. |
| Byte dell’allegato | Scarica gli allegati visibili + limiti per tipo | Cerchi `media.saved` con SHA-256 e dimensione. In coda, saltato o non riuscito significa non salvato. |

Un’esportazione di chat non finisce nel diario né nei profili delle persone. Per cercare nella vecchia cronologia dentro TgWitness usi **Carica cronologia completa** o le istantanee.

Qui: il canale, il gruppo, la chat col bot e la chat privata, più il file della fattura e il suo hash. Ciò che è stato eliminato prima della cattura è perso.

## 3. Tenete traccia dell’evoluzione della conversazione e delle vostre azioni

Lo lasci girare. Contrassegni con la stella le chat calde come prioritarie, regoli i ricontrolli in **Impostazioni di registrazione → Ricontrollo** e tenga d’occhio `recheck.completed`, FloodWait e i risultati dei media.

**Chat → Profilo → Salva profilo ora** salva descrizione della chat, comandi del bot e altri metadati.

**Seguire un bot o un invito nell’ambito del caso**

1. **Chat → Apri link Telegram**, salvi prima l’anteprima. Link e anteprima diventano voci firmate.
2. Se serve, **Unisciti / apri e osserva** entra nella chat o avvia il bot con il suo parametro di avvio.
3. Per documentare un’azione risponda o usi **Premi pulsante** dal pannello. Ottiene `interaction.requested` e `interaction.result` con la risposta del bot.

Sono azioni reali. I pulsanti premuti in un’altra app non si vedono, solo la risposta del bot. Niente web app, pagamenti o telefono/posizione.

## 4. Tracciare persone, link e file nelle chat

1. **Diario**, **Tutte le fonti**, cerchi una frase, un dominio o un nome utente. Apra i risultati e li mandi **Alla bacheca**.
2. **Chat → Persone → Attiva profili**, scelga una persona: cronologia dei nomi, risposte, attività, **Anche in…**, link, wallet, telefoni. Apra le voci citate.
3. Segua lo stesso ID utente numerico in altre chat. Un nome, un wallet o un avatar uguale è un indizio, non una prova.
4. Confronti gli hash dei file. Stesso SHA-256 = stessi byte. Chi li ha condivisi è un’altra questione.

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
| Stesso account Telegram | ID utente 71001 nel gruppo n. 146 e nella chat privata n. 205 | Lo stesso ID mittente in entrambe le chat. Chi sia nella vita reale è un’altra questione. |
| Destinazione ripetuta | `pay.example.invalid/new` nel n. 146, metadati del pulsante n. 173, post modificato n. 188 e n. 205 | Lo stesso link in quattro posti. Chi lo controlla richiede altre fonti. |
| Stessa dimensione del file | Valori SHA-256 identici nelle ricevute multimediali completate n. 151 e n. 209 | I due file sono identici byte per byte. |

I profili coprono solo chi ha scritto qualcosa in *questo spazio*, non sono un elenco di membri. Citazioni per fatto: **Parametri → Voci citate per fatto**.

## 5. Ricostruire la sequenza e contrassegnare le lacune

Versioni in **Chat**, poi **Diario** con **Tutte le fonti** + **Modifiche**, **Eliminazioni**, **Copertura**. Metta entrambi gli orari nella cronologia: la data di Telegram e il momento dell’osservazione.

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

L’ordine del diario è l’ordine di arrivo, non per forza l’ordine dei fatti. Tenga separati voci in diretta, istantanee, messaggi recuperati, eliminazioni e «non trovato al ricontrollo», e segni ogni lacuna come sconosciuta.

## 6. Estendere il caso ad altri account di raccolta dati

Uno spazio per account, stessi passaggi. Annoti ruolo e impronta di ciascuno. I numeri dei messaggi sono per account, quindi indichi sempre spazio e chat.

Un [gruppo di account](https://phishdestroy.github.io/TgWitness/it/docs/groups/) mostra lo stato, condivide le impostazioni ed esporta tutti insieme, ognuno con il proprio diario e la propria chiave. La cronologia tra account la costruisce Lei nelle Sue note.

Caso lungo? Aggiunga un [testimone indipendente](https://phishdestroy.github.io/TgWitness/it/docs/witness/) e verifichi cosa cattura davvero ogni account.

## 7. Consegnare un pacchetto del caso verificabile

Uno ZIP firmato da ogni spazio (sempre il diario intero, i filtri non contano), più profili delle persone, esportazioni di chat e file.

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

Invii le impronte separatamente. Verifichi tutto rispetto al suo spazio:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Conservi l’output del verificatore, gli originali, la copertura e il registro di consegna con le Sue conclusioni. Scriva tutto in Report studio. Se il destinatario ha bisogno di meno, prepari una [consegna ridotta](https://phishdestroy.github.io/TgWitness/it/docs/handover/).
