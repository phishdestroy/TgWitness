# Telegram · Testimone indipendente

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/

Eseguite un’istanza di Witness con chiave e bot propri, pubblicate i checkpoint firmati su un canale e verificate le esportazioni confrontandole con essi.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Prove e verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/)

![Prove e verifica](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

[Esportare e verificare](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/) · [Elevata affidabilità](https://phishdestroy.github.io/TgWitness/it/docs/reference/high-assurance/) · [Guida ai pannelli](https://phishdestroy.github.io/TgWitness/it/docs/reference/panel/#extras)

Un testimone conserva i checkpoint firmati separatamente dal collettore. Verifica la firma del collettore e la continuità del registro, firma il risultato con la propria chiave e lo pubblica su un canale Telegram. Eseguirlo su un server separato con accesso in sola lettura all’ endpoint del testimone del collettore.

Diagramma di flusso · Collector → Testimone (punto di controllo firmato: numero di record + hash dell’intestazione); Testimone → Registro delle testimonianze, chiave propria; Testimone → Canale Telegram (messaggio firmato tramite il proprio bot); File ZIP contenente le prove → verify.py; Registro delle testimonianze, chiave propria → verify.py; Canale Telegram → verify.py (Esportazione da Telegram Desktop o pagina t.me/s) · Collector · Testimone · Registro delletestimonianze, chiavepropria · Canale Telegram · File ZIP contenente leprove · verify.py · punto di controllo firmato: · numero di record + hash · dell’intestazione · messaggio firmato tramite il · proprio bot · Esportazione da Telegram · Desktop o pagina t.me/s

**Diagramma sotto forma di testo**

1. Collector → Testimone (punto di controllo firmato: numero di record + hash dell’intestazione)
2. Testimone → Registro delle testimonianze, chiave propria
3. Testimone → Canale Telegram (messaggio firmato tramite il proprio bot)
4. File ZIP contenente le prove → verify.py
5. Registro delle testimonianze, chiave propria → verify.py
6. Canale Telegram → verify.py (Esportazione da Telegram Desktop o pagina t.me/s)

**In questa pagina**

- [Cosa ottiene il witness e cosa non ottiene](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/#what-the-witness-gets-and-what-it-does-not)
- [Cosa verifica e registra](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/#what-it-checks-and-records)
- [Eseguire un witness](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/#run-a-witness)
- [Pagina di prova pubblica per diversi spazi di lavoro](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/#public-proof-page-for-several-workspaces)
- [Verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/#verify)

## Cosa offre TgWitness e cosa non offre

| Il testimone ha | Il testimone non ha mai |
| --- | --- |
| Un **token di testimonianza** in sola lettura per un’area di lavoro | Le credenziali della sessione Telegram o dell’API del responsabile della raccolta |
| La propria chiave Ed25519 e il proprio registro | Il deposito del collettore, la chiave di firma o il token del pannello |
| Il proprio token del bot di Telegram | Contenuto del messaggio: l’intestazione è costituita dal conteggio dei record e da un hash |

Il token viene creato in **«Extras» → «Independent witness»**, viene visualizzato una sola volta e memorizzato esclusivamente come SHA-256. Apre esattamente un endpoint, `GET /api/witness/head`il quale restituisce un checkpoint appena firmato, oltre a contatori di raccolta privi di contenuto firmati e lo stato di integrità operativa. Non può aprire il pannello, leggere il contenuto dei messaggi né modificare le impostazioni, e il token del pannello non viene accettato in quella sede. È possibile revocare un token nella stessa pagina. Il collettore registra quando una nuova chiave di witness inizia a effettuare il controllo (`witness.seen`) e mostra l’ultimo controllo per ogni token; un testimone che non ha effettuato controlli entro 2,5 intervalli viene contrassegnato come scaduto.

I nuovi testimoni inviano una sfida casuale in occasione di ogni sondaggio; la dichiarazione di acquisizione la riporta sotto la firma del collettore. I contatori sono vincolati al checkpoint esatto e sono inclusi nei post firmati dai testimoni. Le intestazioni preesistenti continuano ad essere accettate dal testimone autonomo. La sola crescita del registro non viene mai conteggiata come un nuovo messaggio.

## Cosa verifica e registra

A ogni intervallo (10 minuti per impostazione predefinita) il sistema:

1. recupera l’intestazione autonomamente (il collettore non può inserirla né saltarla);
2. Verifica la firma del collettore, la chiave del collettore fissata (`--collector-fingerprint`, ovvero la prima chiave rilevata), un conteggio non decrescente e una testa invariata a un conteggio invariato. Le prove di inclusione e di coerenza di Merkle verificano che un registro in crescita estenda il punto di controllo conservato. Una volta utilizzate le prove di continuità, la loro rimozione viene rifiutata;
3. aggiunge una registrazione firmata al proprio registro: `witness.anchor` con stato `ok`, `key_changed`, `rollback` (numero di registrazioni inferiore rispetto a prima), `fork` (stessa lunghezza, intestazione diversa ) o `invalid` (la risposta non ha superato la verifica), oppure `witness.no_response` quando il collettore non ha risposto;
4. pubblica il risultato sul canale, firmato, includendo anche la dicitura «nessuna risposta» fintanto che TgWitness è in esecuzione e può accedere all’API del bot. Viene registrato l’ID del post (`witness.posted`), così come quello di un post non andato a buon fine (`witness.post_failed`).

Un post si presenta in questo modo; l’ultima riga riporta la dichiarazione firmata:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Eseguire un’operazione di registrazione

È necessario disporre di un bot di Telegram (createne uno con @BotFather), di un canale in cui tale bot sia amministratore e dell’indirizzo del collettore raggiungibile dal testimone — tramite HTTPS al di fuori di una rete privata (si veda il profilo HTTPS nella sezione dedicata [all’implementazione](https://phishdestroy.github.io/TgWitness/it/docs/reference/deployment/)).

Apri **Extra → Testimone indipendente → Configura** nel pannello. Tre passaggi riguardano l’accesso in sola lettura, il tuo canale e l’intervallo, quindi l’avvio del testimone. La politica di pubblicazione, il proxy HTTP/SOCKS5 opzionale e l’indirizzo API del bot personalizzato si trovano nelle **impostazioni avanzate**. Il modulo scarica `witness.json` con la chiave del collettore di questo spazio di lavoro già inserita. Scarica il token di sola lettura appena creato con **Salva file di accesso** come `witness-token.txt`; salvatelo insieme a un `bot-token.txt`creato sull’host del witness accanto a quel file JSON. Il collector non riceve mai il token del bot. Il download non avvia alcun servizio né pubblica alcun messaggio. Nessun witness di progetto ospitato viene iscritto implicitamente.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

Il primo comando verifica i file di configurazione e quelli segreti senza effettuare richieste di rete né creare chiavi. I percorsi nel file JSON sono relativi a tale file; i percorsi della CLI e dell’ambiente sono relativi alla directory di lavoro. Conservare l’impronta digitale del testimone al di fuori del proprio host. L’ indicatore di ultimo polling del collettore conferma solo una richiesta; la pubblicazione viene segnalata da Proof o verificata nel registro del testimone e nel canale.

Se il pannello si trova dietro un tunnel SSH, esponga solo l’endpoint Witness con ambito limitato su un nome host HTTPS separato, come illustrato in [questo esempio di Caddy](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example). L’area di lavoro predefinita utilizza quindi `https://witness.example.org`, mentre le altre aree di lavoro utilizzano `https://witness.example.org/profiles/ID`. I token sono comunque necessari; il pannello e le sue altre rotte API non vengono inoltrate da tale host virtuale.

Scegliete `all` per i checkpoint pubblicati regolarmente. Un intervallo di cinque minuti corrisponde a circa 288 post al giorno per ogni spazio di lavoro. `changes` e `problems` omettono deliberatamente la pubblicazione di alcuni controlli. MTProxy è destinato al client Telegram del collettore. Il polling HTTP di Witness e l’API HTTPS Bot di Telegram utilizzano il proprio percorso diretto/HTTP/SOCKS5 ([API Bot](https://core.telegram.org/bots/api)).

**Accanto al collector, con Docker** (stesso host — processo e chiave indipendenti, ma lo stesso operatore): inserite i valori in `.env` e avviate il profilo.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

In caso di utilizzo di un'immagine pubblicata, si prega di utilizzare il codice `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**Sul server di un’altra persona** (un vero testimone indipendente): copiare il repository su tale server, impostare `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` più i tre valori sopra indicati in `.env`, quindi

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

oppure senza Docker:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Pubblica su Discord

Un testimone può pubblicare su un canale Discord anziché su Telegram. In Discord, apri **Modifica canale → Integrazioni → Webhook**, crea un webhook e copia il suo URL. Nel pannello, scegli **Webhook Discord · il tuo canale** al punto 2. Sull’host del testimone, salva l’URL come `discord-webhook.txt` accanto a `witness.json`; non raggiunge mai il collettore.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

Un testimone ha un solo editore: un canale Telegram o un webhook Discord, non entrambi. I post contengono la stessa dichiarazione firmata e non possono taggare nessuno. Un post più lungo dei 2.000 caratteri consentiti da Discord viene sostituito da una breve riga con il controllo completo allegato come `witness-check.txt`. Ogni ID del post viene registrato come `witness.posted`. `verify.py --channel`legge solo le esportazioni dei canali Telegram, quindi per Discord è necessario conservare il registro dei testimoni: esso contiene ogni controllo.

### Opzioni

| Opzione | Contesto | Impostazione predefinita | Significato |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Intervallo tra i controlli: da 1 a 1440 |
| `--timeout` | `_TIMEOUT` | 30 | Tempo di attesa in secondi per il collector e l’API del bot: da 5 a 600 |
| `--post` | `_POST` | `all` | `all`: ogni controllo; `changes`: una nuova questione o un problema; `problems`: solo problemi e risposte mancanti |
| `--title` | `_TITLE` | `TgWitness witness` | Prime parole di ogni post pubblicato sul canale |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | Salvi la chiave del collettore anziché fidarsi della prima risposta |
| `--proxy` | `_PROXY` | diretto | `socks5://host:port` o `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Indirizzo dell’API del bot, ad esempio un server locale dell’API del bot |
| `--data-dir` | `_DATA` | `witness-data` | Chiave di Witness e registro |
| `--config` | `_CONFIG` | – | File JSON contenente una qualsiasi delle opzioni sopra indicate |

L’indirizzo del collector, i token e il canale provengono da `--collector`, `--token` oppure `--token-file`, `--bot-token` oppure `--bot-token-file`, `--discord-webhook-file` e `--channel`, oppure `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` e `_CHANNEL`, che impedisce ai segreti di comparire nell'elenco dei processi.

Un file di configurazione utilizza i nomi delle opzioni con trattini bassi, oltre a «`texts`», che sostituisce le parole dei post del canale:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Chiavi `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. La riga di comando ha la precedenza sull’ambiente, l’ambiente sul file. Le opzioni o le chiavi di testo sconosciute interrompono il processo di registrazione con un messaggio, anziché essere ignorate. La formulazione non influisce mai sulla verifica: verify.py controlla il token firmato alla fine di ogni pubblicazione. Con `--post changes` o `problems`, i controlli che non sono stati pubblicati rimangono comunque nel registro dei testimoni e `verify.py` li elenca come mai pubblicati; il record iniziale indica la politica. Ogni controllo compare comunque nel registro, quindi un numero minore di pubblicazioni comporta un numero minore di tempi Telegram indipendenti, non un numero minore di controlli.

Anche in assenza di un canale, TgWitness continua a mantenere il proprio registro. Conservi l’impronta digitale della chiave di TgWitness (`python -m tgwitness.witness fingerprint`) in un luogo separato.

## Pagina pubblica di verifica per diversi spazi di lavoro

`python -m tgwitness.proof` Supporta fino a 32 spazi di lavoro contemporaneamente e fornisce una pagina di sola lettura con l’ultimo controllo firmato di ciascuno. Ogni spazio di lavoro dispone di una propria chiave di testimonianza e di un proprio registro nella cartella dei dati, oltre a una chiave di raccolta fissata; la pubblicazione su un canale Telegram è facoltativa per ogni spazio di lavoro. Inizia da [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example):

| Settore | Significato |
| --- | --- |
| `title` | Titolo della pagina, 1–100 caratteri |
| `data_dir` | Chiavi e registri di Witness, relativi al file; impostazioni predefinite `proof-data` |
| `interval`, `timeout` | Minuti tra un controllo e l’altro (1–1440, valore predefinito 5); secondi di attesa (5–600, valore predefinito 20) |
| `workspaces[].id`, `label` | Alias breve in minuscolo e nome visualizzato |
| `workspaces[].collector` | Indirizzo del Collector; gli altri spazi di lavoro terminano con `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | Obbligatorio, diverso per ogni spazio di lavoro |
| `workspaces[].token_file` | File contenente il token di testimonianza in sola lettura di quell’area di lavoro |
| `workspaces[].channel`, `bot_token_file` | Opzionale, in combinazione: pubblica ogni verifica su un canale |
| `workspaces[].proxy`, `bot_api` | Percorso opzionale e indirizzo API del bot |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

Il primo comando verifica la validità del file e dei file dei token senza aprire una connessione. La pagina risponde solo ai metodi GET e HEAD:

- `/` Mostra tutti gli spazi di lavoro; uno spazio di lavoro senza alcun segno di attività per 2,5 intervalli viene contrassegnato come inattivo.
- `/api/proof` Restituisce lo stesso risultato del JSON.
- `/api/proof/<id>` scarica l’ultima dichiarazione firmata (`tgwitness-public-proof-v1`): numero e hash del record del testimone, stato, chiave del collettore fissata, punto di controllo, contatori di raccolta e indicazione dell’esito positivo della pubblicazione sul canale, firmata dalla chiave del testimone di quell’area di lavoro.
- `/healthz` Restituisce il codice di errore 503 quando il monitor di un'area di lavoro si è arrestato.

Assegnare alla pagina un proprio nome host, come in [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example). Per la verifica, esportare il diario di testimonianza di un'area di lavoro con `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` e utilizzalo come descritto di seguito.

## Verificare

Da parte del testimone, esportare il proprio registro:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

Successivamente, ovunque, utilizzando il file ZIP firmato del collettore e il canale esportato da Telegram Desktop (*Esporta cronologia chat* → JSON fornisce `result.json` ) o la sua pagina pubblica `https://t.me/s/…` :

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` verifica il registro di testimonianza (catena e firme), quindi controlla che **ogni intestazione che il testimone ha visionato faccia parte del registro esportato**: la voce corrispondente a quel conteggio deve avere esattamente quell’hash. Un’intestazione che non corrisponde non supera la verifica — il registro è stato modificato dopo che il testimone lo ha visionato. Segnala inoltre i «head» visualizzati dopo l’esportazione, le anomalie registrate dal testimone, le risposte non valide, i periodi i cui checkpoint corrispondenti sono presenti in questa esportazione («Testimoniato da X a Y») e le lacune. I checkpoint successivi non estendono tali periodi. Il risultato include l’ultimo numero di record corrispondente e il numero di record successivi privi di un checkpoint corrispondente. Vengono conteggiate solo le risposte firmate dalla chiave dell’esportazione stessa: un’esportazione firmata da una chiave che il testimone non ha mai visto viene segnalata come non testimoniata e, in assenza di `--fingerprint`, il suo firmatario rimane non identificato. Con `--channel`, ogni post firmato deve corrispondere al diario del testimone record per record: i post modificati non superano la verifica, mentre quelli mancanti vengono elencati. Una data contenuta in un’ esportazione JSON fornita da Telegram è un metadato modificabile, esterno al token del testimone firmato. La corrispondenza con il token non autentica la data di pubblicazione; il risultato riporta esplicitamente che la verifica della data di pubblicazione non è stata eseguita.

### È richiesto un limite di esportazione certificato

Per un passaggio di consegne che debba includere un registro finale autenticato, si prega di aggiungere `--require-witness`:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

Ciò richiede l’impronta digitale di riferimento conservata in modo indipendente e un punto di controllo corrispondente esattamente alla fine di questa esportazione. Un punto di controllo che copra solo un prefisso precedente è insufficiente. Sospenda la raccolta, consenta al testimone di osservare lo stato finale ed esporti prima di ulteriori scritture nel registro; se il registro cambia, conservi un altro punto di controllo ed esporti quello stato. Un checkpoint successivo da solo non può verificare l’hash finale di un’esportazione più breve. Quando viene fornito anche il flag `--channel`, la mancanza di post dichiarati o un insieme di corrispondenze vuoto comportano il fallimento di questo rigoroso controllo. Senza il flag, i normali controlli di integrità segnalano comunque i record non certificati senza rifiutare un archivio altrimenti intatto.

Conservare separatamente il registro dei witness e la relativa chiave fissata. I controlli online verificano la continuità tra i checkpoint; la verifica offline confronta ogni checkpoint conservato con l’ esportazione. I witness legacy privi di prove di continuità conservano il confronto offline e vengono segnalati senza verifica della continuità online. Il rapporto elenca i tempi di inattività dei witness e le pubblicazioni non riuscite per intervallo.

### Sigilli giornalieri e calendari dei timestamp non disponibili

Il testimone sigilla il confine del diario del giorno UTC precedente e invia l’hash di quel sigillo firmato a OpenTimestamps. Un invio al calendario è una prova in sospeso; solo gli impegni Bitcoin verificati in modo indipendente ricevono conferma nel verificatore.

Se tutti i calendari falliscono, il sigillo firmato e il tentativo fallito rimangono nel registro. Il ciclo di manutenzione orario riprova a elaborare quel record originale, anche dopo un riavvio o un cambio di data. Esegue la scansione di un massimo di 32 sigilli, invia al massimo due invii mancanti e impiega al massimo 60 secondi per i tentativi di riprova per ogni ciclo. Un cursore persistente passa in rassegna i sigilli più vecchi. Gli invii conservati seguono il percorso di aggiornamento della prova esistente.

Un nuovo tentativo non riscrive il sigillo, non modifica la sua data originale né sostiene che il calendario lo abbia ricevuto in precedenza. Un impegno Bitcoin successivo rimane una conferma esterna successiva. Le prove mancanti rimangono `none`; le prove in sospeso rimangono `pending` fino a quando il verificatore non le controlla in modo indipendente.
