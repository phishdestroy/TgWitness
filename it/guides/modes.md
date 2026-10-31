# Un unico registro. Quattro modalità di raccolta. Otto livelli di verifica.

Canonical page: https://phishdestroy.github.io/TgWitness/it/guides/modes.html

Modalità, scenari e livelli di evidenza

TgWitness Registra ciò che l’account connesso osserva. Una terza parte può verificare l’integrità della registrazione rispetto a una chiave attendibile indipendente.

[Modalità di raccolta](https://phishdestroy.github.io/TgWitness/it/guides/modes.html#scope)[Scenari](https://phishdestroy.github.io/TgWitness/it/guides/modes.html#scenarios)[Livelli di evidenza](https://phishdestroy.github.io/TgWitness/it/guides/modes.html#levels)

Panoramica di 3–5 minuti · esempi fittizi · implementazione attuale

1. **Telegram**

   Aggiornamenti visibili sull’account
2. **Collector**

   Record collegati, ciascuno firmato
3. **Verificatore**

   Chiave fidata + confine mantenuto

`h₁ → h₂ → h₃ · Ed25519`L’integrità viene verificata. L’origine di Telegram e la veridicità di un messaggio rimangono questioni distinte.

## Scegliere l’ambito di osservazione

Tre ambiti e un’impostazione predefinita per le indagini. Le esclusioni e i tipi di fonte abilitati rimangono validi.

Impostazione predefinita**Chat selezionate**

Registrazioni

Solo fonti selezionate manualmente.

Nuove chat

Non viene aggiunto automaticamente.

Scegliere per

Un insieme noto di canali o gruppi. Non è stata specificata alcuna capacità fissa delle chat.

**Non esegue** Non individua altre chat né ricostruisce la cronologia precedente.

Cartella degli account**Cartella Telegram**

Registrazioni

Inclusioni di cartelle e categorie, escluse le esclusioni e le chat archiviate, se configurate.

Nuove chat

Corrispondenza delle chat attive; modifiche alle cartelle entro un’ora.

Scegliere per

Un analista gestisce già una cartella dedicata al caso. Confermare la raccolta su un account dedicato.

**Non esegue** Non si applicano le condizioni mutevoli della cartella muted/read della cartella.

Confermare l’ambito**Account completo**

Registrazioni

Chat visibili dall’account, comprese le conversazioni private e i bot, all’interno di tipi selezionati.

Nuove chat

Da aggiungere al momento del primo aggiornamento.

Scegliere per

Un account dedicato all’osservazione, compreso un account che partecipa a un caso.

**Non esegue** Non si unisce automaticamente alle chat né aggira l’accesso alla fonte.

Preimpostazione dell’intero account**Modalità di indagine**

Registrazioni

Tutti i tipi di fonte, le azioni proprie, i profili delle fonti e gli ultimi 200 messaggi visibili delle fonti appena individuate.

Nuove chat

A ogni nuova chat o bot vengono assegnati un profilo e un’istantanea della cronologia.

Scegliere per

Entrare a far parte di un team o interagire con un bot tramite il pannello. Verificare e salvare le impostazioni predefinite.

**Non esegue** Non acquisisce istantanee di tutte le chat esistenti né rileva i callback attivati in un altro client.

Queste schede rappresentano un confronto locale, non controlli in tempo reale del collettore. Non modificano alcun account.

**Non esegue** Nessuna modalità legge le chat segrete, registra mentre il processo è in pausa, si collega autonomamente alle fonti o recupera la cronologia precedente oltre quanto richiesto snapshot/export.

[Leggere i dettagli](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/)

## Acquisizione con GitHub Actions (anteprima)

Un nuovo accesso a Telegram, una chat, un archivio cifrato e un’attestazione di provenienza GitHub.

[Apri l’assistente di acquisizione](https://phishdestroy.github.io/TgWitness/it/docs/capture/)

## Cosa viene registrato

Solo le osservazioni consegnate o esplicitamente richieste vengono inserite nel registro. Le attribuzioni sconosciute rimangono tali.

 Acquisizione degli switch · illustrazione localeNuovi messaggiModificheCancellazioniReazioniAdesione

Il pannello applica queste opzioni per ogni area di lavoro. Disattivandone una, i record esistenti vengono mantenuti; riattivandola, gli eventi persi non vengono ricostruiti.

**Matrice degli eventi: materiale salvato e incognite residue**

| Categoria | Salvato | Rimane sconosciuto |
| --- | --- | --- |
| Messaggio | Testo, ID, metadati del mittente, contesto della risposta e busta di aggiornamento originale. | Nessuna firma Telegram verificabile da terze parti. |
| Modifica | Ogni versione osservata, senza sovrascrivere quelle precedenti. | Le modifiche intermedie potrebbero non essere rilevate; il mittente non è necessariamente l’editore. |
| Cancellazione | Avviso più il testo salvato in precedenza, se disponibile. | Il soggetto che effettua la cancellazione e l’ora esatta dell’azione non vengono forniti. |
| Cancellazione senza ambito | Avviso a livello di account; il peer sconosciuto rimane esplicito. | Nessuna chat ipotizzata. La correlazione utilizza, ove possibile, gli ID a livello di account salvati in precedenza. |
| Reazione | Contatori consegnati e identità recenti visibili. | Non tutti i reattori sono visibili; per ottenere un elenco completo e aggiornato sono necessarie query separate. |
| Adesione | Messaggi di servizio consegnati e aggiornamenti dei partecipanti. | Il ruolo e il tipo di chat limitano la visibilità; il silenzio non implica l’assenza. |
| Allegato | Descrittore della versione originale, byte salvati, SHA-256 e risultati dei tentativi. | Un file scomparso potrebbe non essere disponibile; una versione più recente non lo sostituisce. |
| Istantanea della cronologia | Messaggi attualmente visibili, contrassegnati come osservazioni della cronologia. | Le modifiche precedenti e i contenuti scomparsi non vengono ricostruiti. |
| Azioni proprie | In uscita messages/edits e i metadati corrispondenti della tastiera di risposta button_press . | I callback attivati in un altro client Telegram non sono visibili. |
| Pulsanti del bot | I metadati relativi a callback, URL, applicazioni web e richieste vengono conservati insieme al messaggio. | Gli URL e le phone/location le richieste sono testo, non vengono aperte o eseguite automaticamente. |

### Limiti predefiniti per gli allegati

Foto

20 MiB

Video

100 MiB

File

50 MiB

Animazioni

20 MiB

Note video

50 MiB

Voce

20 MiB

Audio

50 MiB

Adesivi

5 MiB

**Non esegue** Un switch non occlude i metadati incorporati né disabilita i registri operativi. L’acquisizione non identifica un attore che Telegram non abbia fornito.

[Leggere i dettagli](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/)

## Utilizzi l’autorizzazione di cui dispone

Ogni account dispone di un proprio spazio di lavoro, registro, chiave di firma, percorso e coda.

### Telefono + codice

Inserire 2FA quando abilitato.

### QR codice

Eseguire la scansione da un dispositivo autorizzato; 2FA potrebbe comunque essere richiesto.

### Telethon .session

Importare il file di sessione dell’account.

### Pyrogram .session

Importare il formato di sessione supportato Pyrogram formato di sessione supportato.

### TData ZIP

È supportato un solo account Desktop; codice di accesso locale, se impostato.

### StringSession testo

Inserisca un Telethon StringSession.

### .session + .json

Selezionare la sessione e i metadati associati corrispondenti.

### Chiave di autenticazione HEX + DC ID

Importare l’autorizzazione dell’account con il relativo identificatore del data center.

**API coppia**

La propria API è facoltativa. In assenza di una coppia, TgWitness viene utilizzato un pool di coppie pubbliche, comprese quelle provenienti dal client ufficiale di Telegram Desktop.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy è sperimentale; sono disponibili MTProxy . Un percorso proxy non riuscito non ricorre a una connessione diretta.

Due aree di lavoro su un unico computer non costituiscono due testimoni indipendenti.

**Non esegue** L’importazione non aggira l’autorizzazione di Telegram, 2FA né i formati di sessione non supportati. Gli account continuano a condividere il processo dell’applicazione.

[Formati degli account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/)

## Agire dal pannello

Inviare o rispondere, premere un pulsante del bot corrente, salvare l’anteprima di un link, quindi entrare esplicitamente in una chat o avviare un bot con il relativo parametro di avvio.

`interaction.preview``interaction.requested``interaction.result`

Le conferme di anteprima, di richiesta e di risultato sono firmate. Prima che venga premuto un pulsante, il server recupera nuovamente il messaggio e rifiuta eventuali modifiche apportate tramite tastiera. Il testo e gli URL restituiti dalla callback rimangono registrati nel contesto.

**Non esegue** Nessuna applicazione web, pagamento, phone/location condivisione né query inline. La visualizzazione di un URL non ne comporta l’apertura.

[Leggere i dettagli](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/)

## Ripristino e continuità

Le lacune vengono evidenziate, non nascoste.

### Riprendere la posizione salvata

Dopo il riavvio, a Telegram vengono richiesti gli aggiornamenti mancati. La conservazione limitata nel tempo e le differenze scadute possono lasciare delle lacune.

### Ricontrollare i messaggi visibili

Impostazioni predefinite: fonti prioritarie ogni 15 minuti, le altre ogni 6 ore. I risultati includono message.recovered e message.missing_on_recheck.

### Leggere coverage.json

I periodi di osservazione, le lacune con relative motivazioni e gli ID non osservati accompagnano l’esportazione firmata. Un record mancante al momento della verifica non costituisce un avviso di cancellazione.

**Non esegue** Un’istantanea successiva della cronologia non cancella un’interruzione del servizio né ripristina tutte le versioni scomparse. Il cursore salvato non costituisce una conferma senza perdita di dati dell’accettazione del diario.

[Leggere i dettagli](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/)

## Sette livelli. Domande diverse.

Ogni meccanismo risponde a una domanda circoscritta. Configurare i servizi esterni separatamente e mantenere i loro punti di riferimento di fiducia al di fuori del collettore.

1. ### Registrazione

   SHA-256 catena + Ed25519 per evento; il primo previous_hash è costituito da 64 zeri.

   **Verifiche da parte di terzi** Ordinamento e firme sotto la chiave del collettore fissata.

   **Non esegue** Ciò non dimostra l’origine da Telegram né la completezza.

   **Comando di verifica**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Contenitore

   manifest.json elenca gli hash dei file; manifest.sig lo firma; media.saved associa i byte degli allegati a un evento.

   **Verifiche da parte di terzi** I file forniti sono conformi al manifesto firmato e alle ricevute multimediali.

   **Non esegue** Non firma uno screenshot CSV, HTML o uno screenshot.

   **Comando di verifica**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Confine mantenuto

   Eseguire un checkpoint all’avvio, ogni 5 minuti per impostazione predefinita, e un arresto ordinato. Conservarne una copia altrove.

   **Verifiche da parte di terzi** L’esportazione successiva è coerente con una lunghezza e un’intestazione conservate in precedenza; è possibile rilevare un rollback.

   **Non esegue** Non rileva la sostituzione né del registro né di tutti i checkpoint conservati.

   **Comando di verifica**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### Tempo esterno

   La modalità «Evidence» invia un checkpoint SHA-256 alle RFC 3161 autorità (FreeTSA, DigiCert) e OpenTimestamps ai calendari.

   **Verifiche da parte di terzi** Una risposta TSA verificata data tali byte; un OpenTimestamps prova li ancorerà a Bitcoin.

   **Non esegue** Non considera una richiesta preparata o una ricevuta di calendario in sospeso come un timestamp confermato.

   **Comando di verifica**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Testimone indipendente

   Separare l’host, l’endpoint in sola lettura con ambito definito, la nuova sfida e il proprio key/journal e TGW1 i post del canale.

   **Verifiche da parte di terzi** Heads precedentemente accettati; stati: ok, key_changed, rollback, fork, invalid e no_response.

   **Non esegue** Ciò non trasforma due spazi di lavoro su un unico host di raccolta in testimoni indipendenti.

   **Comando di verifica**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Replica fuori sede

   S3- copia compatibile crittografata con AES-256-GCM; Object Lock qualora il bucket lo supporti.

   **Verifiche da parte di terzi** Restore pubblica i file solo dopo che la verifica del diario, del checkpoint e dei contenuti multimediali conservati è stata completata con esito positivo.

   **Non esegue** Non esegue il ripristino senza la chiave esportata né presume la conservazione senza verificare la risposta dell’archivio.

   **Comando di verifica**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Eseguire la verifica della provenienza

   Ricevuta di esecuzione firmata: hash delle fonti, versioni delle dipendenze e contesto del processo. Autodichiarata.

   **Verifiche da parte di terzi** Quanto riportato dal collettore di firme in merito alla propria esecuzione.

   **Non esegue** Non fornisce un’attestazione indipendente del processo né esclude la possibilità di compromissione prima della registrazione.

   **Comando di verifica**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### Ciò che nessun livello dimostra

Consegna di ogni aggiornamento di Telegram; la veridicità del testo; il fatto che l’ID del mittente identifichi una persona reale; l’assenza di compromissione del raccoglitore prima della registrazione; l’ammissibilità in sede giudiziaria.

[Testimone indipendente](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/)

Esperimento SHA-256 esperimento

### Provi a modificare il record 2

Il record successivo conserva il link salvato in precedenza. La modifica del testo altera l’hash calcolato del record 2.

Testo del record 2

Record 1`h1`Inizia con 64 zeri

Record 2`h2`Include i dati salvati h1

Record 3`h3`Include i dati salvati h2

Esempio statico: h2 riferisce a «Appuntamento alle 11:00». Modificando quel testo si modifica h2; il record 3 fa ancora riferimento a quello salvato h2.

**Esaminare i digest completi**

Hash del record 2 salvato

`SHA-256(e₂)`

Hash del record 2 ricalcolato

`SHA-256(e₂)`

Questo esempio calcola gli hash, non le firme. Il vero verificatore controlla ogni firma e ogni link rispetto alla chiave fidata.

 [Leggere i dettagli](https://phishdestroy.github.io/TgWitness/it/docs/reference/how-it-works/)

## Scegliere un percorso attraverso le prove

Situazioni fittizie. Avviare la raccolta prima dell’evento in questione; conservare i confini e le lacune insieme al contenuto.

### Un canale modifica i dettagli di pagamento

Modalità → eventi

Chat selezionate → messaggi, modifiche, cancellazioni.

Output

Versioni dei post e allegati osservati tramite hash.

Verifica

Firmato ZIP + checkpoint conservato + risposta TSA verificata.

**Non esegue** Non consente di recuperare un originale che non è mai stato acquisito.

### I messaggi scompaiono dopo un incidente

Modalità → eventi

Cartella o intero account → tutte le categorie di eventi.

Output

Originali salvati, avvisi di cancellazione e copertura con lacune.

Verifica

Firmato ZIP + diario di testimonianza indipendente.

**Non esegue** Non identifica chi ha effettuato la cancellazione da una notifica che non fornisce alcun attore.

### Analizzare un bot di negozio

Modalità → eventi

Preimpostazione di indagine → pulsanti, anteprime dei link e avvio esplicito del bot.

Output

Ricevute di interazione firmate, callback restituiti e profili salvati.

Verifica

Firmato ZIP; verificare qualsiasi dossier rispetto al ZIP.

**Non esegue** Non apre un’applicazione web per bot, non effettua pagamenti né registra i callback di un altro client.

### Un partecipante cambia nome da una chat all’altra

Modalità → eventi

Qualsiasi ambito → metadati sender/profile metadati.

Output

Cronologia dei nomi/nomi utente in base all’ID numerico, collegamenti «anche in» e indizi estratti.

Verifica

Il dossier JSON confrontato con il documento firmato ZIP.

**Non esegue** Non trasforma un portafoglio, una stringa simile a quella di un telefono o un nome utente in un’identità comprovata.

### Osservazione a lungo termine con una copia fuori sede

Modalità → eventi

Qualsiasi ambito → Modalità "Evidence" e una S3 replica con supporto Object Lock.

Output

Copia crittografata, checkpoint conservati e risposte con timestamp.

Verifica

Eseguire il ripristino con la chiave esportata, quindi verificare senza il server originale.

**Non esegue** Non sostituisce un testimone indipendente né una chiave di decrittografia conservata separatamente.

[Leggere i dettagli](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/)

## Consegnare un pacchetto verificabile

Fornire l’originale firmato, un’impronta digitale della chiave conservata in modo indipendente, il checkpoint pertinente e il risultato della verifica.

- Firmato ZIP
- JSONL
- CSV
- HTML
- Punto di controllo
- Conferma di ricezione
- Esportazione delle chat: chat.json / chat.html
- Dossier JSON
- Protetto da password AES-256 ZIP
- Esportazioni separate per più account
- CLI di streaming: 5 GiB limite predefinito

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Si ottenga il verificatore da una copia attendibile, non dall’archivio oggetto di verifica.

**Non esegue** Autonomo CSV e HTML non sono contenitori firmati. Una password protegge la riservatezza del trasferimento, non l’autenticità. Esportazioni multiple non uniscono i registri degli account.

[Leggere i dettagli](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/)

## Confrontare l’artefatto fornito

Artefatti di base senza sistemi aggiuntivi di firma, marcatura temporale o testimonianza. Gli script e i logger variano a seconda dell’implementazione; «parziale» significa limitato al materiale acquisito o visibile.

| Approccio | Modifiche / cancellazioni | Registrazione della firma | Tempo esterno | Testimone indipendente | Copertura / lacune | Verifica senza autore |
| --- | --- | --- | --- | --- | --- | --- |
| Esportazione da Telegram Desktop | Parziale | No | No | No | No | No |
| Telethon script di snapshot | Parziale | No | No | No | No | No |
| Registratore delle cancellazioni: registro di testo | Parziale | No | No | No | No | No |
| Screenshot / acquisizione web | Parziale | No | No | No | No | No |
| TgWitness con extra configurati | Parziale | Sì | Sì | Sì | Parziale | Sì |

**Non esegue** La tabella non valuta ogni script o prodotto di registrazione. I controlli opzionali relativi al tempo e ai testimoni richiedono servizi e punti di riferimento di fiducia propri; nessuno di essi stabilisce la veridicità della fonte.

[Leggere i dettagli](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/)

## Rispettare i limiti con le prove

La verifica è utile quando il suo ambito rimane esplicito.

- Le chat segrete non sono disponibili.
- Non viene registrato nulla mentre il processo è arrestato; il recupero è limitato.
- Un record verificato non costituisce prova della veridicità del suo contenuto.
- Un operatore in possesso della chiave può firmare contenuti arbitrari. I testimoni indipendenti e i timestamp limitano la sostituzione successiva, non l’acquisizione iniziale non veritiera.
- Utilizzi un account dedicato, non il Suo account principale.
- Telegram può limitare gli account in base al volume delle richieste.

**Non esegue** Nessuna modalità o livello di prova garantisce l’ammissibilità legale, la consegna completa su Telegram o l’identità nel mondo reale.

[Guida alla configurazione](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=it)[Account dedicato](https://phishdestroy.github.io/TgWitness/it/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/)
