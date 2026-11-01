# I messaggi cambiano. Conservi ciò che ha visto.

Canonical page: https://phishdestroy.github.io/TgWitness/it/

[Open source / v0.7.1](https://phishdestroy.github.io/TgWitness/it/docs/reference/changelog/)

Acquisite i messaggi di Telegram, conservatene le modifiche ed esportate un registro firmato.

[Aprire la demo](https://phishdestroy.github.io/TgWitness/demo/?lang=it)[Guida all’installazione](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=it)

La demo utilizza dati fittizi. Non è richiesto l’accesso a Telegram.

 [Acquisizione con GitHub Actions (anteprima)](https://phishdestroy.github.io/TgWitness/it/docs/capture/) [Copia off-site su S3: configurazione e ripristino](https://phishdestroy.github.io/TgWitness/it/#s3)

UN MESSAGGIO ATTRAVERSO IL TEMPO #0042

Northstar · RicercaFonte fittizia / messaggio 42

1. **Messaggio rilevato:**09:41:02

   Il briefing inizia all’indirizzo 14:00.
2. **Modifica conservata**09:43:18

   Il briefing inizia all’indirizzo 15:00.

   Versione precedente mantenuta
3. **Avviso di cancellazione**10:06:45

   I contenuti acquisiti rimangono nel Vostro registro.

Tre osservazioni. Una storia. ESEMPIO

Il messaggio scompare. La cronologia acquisita rimane.

## Ogni modifica registrata. Proprio dove ne avete bisogno.

Esplori l’interfaccia con dati dimostrativi fittizi.

TgWitness / Chat salvateIL VOSTRO SPAZIO DI LAVORO PER L’OSSERVAZIONE

![Conversazioni Telegram salvate con tema scuro, con le modifiche e i messaggi cancellati acquisiti e conservati nel loro contesto](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Chat salvate Una visualizzazione familiare delle conversazioni, con le modifiche e le notifiche di cancellazione acquisite accanto ai messaggi.

TgWitness / RegistroAREA DI LAVORO LOCALE

![Registro contenente i messaggi rilevati, le modifiche, le notifiche di cancellazione e gli eventi coperti](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Registro: una cronologia consultabile di ciò che il Suo account ha rilevato, comprese le interruzioni.

TgWitness / Cronologia delle modificheAREA DI LAVORO LOCALE

![Pannello di dettaglio che mette a confronto la versione precedente e quella modificata di un messaggio](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Cronologia delle modifiche: Confrontare le versioni acquisite senza sovrascrivere l’osservazione precedente.

TgWitness / Esportazioni firmateAREA DI LAVORO LOCALE

![Funzionalità di esportazione dell’area di lavoro che offre un file ZIP firmato, JSONL, CSV e un report HTML offline](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Esportazioni firmate: portate con voi il registro, corredato di un manifesto e di un verificatore indipendente.

01 / ACQUISIZIONE

### Siete voi a scegliere l’ambito di applicazione.

Chat selezionate, una cartella di Telegram o l’intero account. Uno spazio di lavoro separato per ciascun account.

[Confronto tra le modalità di raccolta](https://phishdestroy.github.io/TgWitness/it/guides/modes.html#scope)

02 / PRESERVE

### Le modifiche arricchiscono la narrazione.

Le versioni acquisite, le notifiche di cancellazione e le lacune di osservazione rimangono nel registro.

[Consultare la matrice degli eventi](https://phishdestroy.github.io/TgWitness/it/guides/modes.html#events)

03 / CONSEGNA

### Una registrazione che viaggia.

File ZIP firmati, file conservati e un rapporto offline. Protezione con password opzionale.

[Esportare e verificare](https://phishdestroy.github.io/TgWitness/it/docs/exports/)

## Modifichi un solo byte. La catena se ne accorge.

Ogni evento è collegato all’hash precedente e reca una firma Ed25519.

![Gli eventi acquisiti sono collegati agli hash precedenti, recano le firme e vengono esportati in un formato verificabile.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![La modifica di un record acquisito ne altera l’hash e compromette la verifica del record collegato.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Un punto di controllo conservato separatamente consente al destinatario di confrontare il registro esportato con un’osservazione precedente.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Scoprite cosa garantisce ciascun meccanismo di verifica e quali sono i suoi limiti.

[Scoprite gli otto livelli di prova](https://phishdestroy.github.io/TgWitness/it/guides/modes.html#levels)

## Pronto per una revisione.

Consegna osservazioni, file e un rapporto HTML offline in un unico pacchetto firmato.

[Legga il modello di prova](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/)

tgwitness-evidence.zipPACCHETTO FIRMATO

- 01

  Osservazioni originaliRecord JSONL + tabella CSV
- 02

  Contesto di facile letturaRapporto HTML offline + file multimediali conservati
- 03

  Verifica indipendenteManifesto firmato + verificatore autonomo

Le firme rilevano eventuali manomissioni rispetto a una chiave attendibile. Esse non dimostrano l’origine da Telegram né garantiscono l’acquisizione completa. Il contenuto del registro e i file multimediali richiedono un’archiviazione crittografata fornita dall’utente.

## Copie su S3. Controlli esterni.

Conservare copie crittografate e aggiungere controlli indipendenti.

Disattivato per impostazione predefinita

### Copiare tutto su un archivio compatibile con S3

Registro, file, checkpoint con data e ora ed esportazioni delle chat — crittografati prima del caricamento su AWS S3 o su un sistema di archiviazione compatibile.

**Impostazioni di archiviazione e recupero**

Crittografia lato client

`AES-256-GCM` crittografa gli oggetti presenti su questa macchina. Il provider riceve gli oggetti crittografati.

Copie programmate o manuali

Esegua ora la copia oppure scelga un intervallo compreso tra 1 e 1.440 minuti. Verifichi lo stato di avanzamento nel pannello.

Object Lock

Selezionare i giorni di conservazione e una modalità, qualora il bucket lo supporti. Il pannello indica se la conservazione è stata confermata per un oggetto caricato.

Recupero verificato

Scarichi la chiave di crittografia e la conservi separatamente. Esegua il ripristino su un altro computer; i file vengono pubblicati solo dopo la verifica.

![Pannello completo per il copia fuori sede: endpoint, regione, bucket, chiavi di accesso, pianificazione, Object Lock e controlli delle chiavi di ripristino](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Il pannello completo con le opzioni avanzate è espanso. Non vengono visualizzate credenziali di accesso all’archivio.

Giornale e media`AES-256-GCM`Archiviazione compatibile con S3

[Configurare S3 e ripristinare una copia](https://phishdestroy.github.io/TgWitness/it/docs/exports/#s3)[Legga i dettagli della verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Non esegue** il ripristino senza la chiave di decrittazione esportata né sostituisce un testimone indipendente.

### Notifiche · Apprise

Avvisi relativi a problemi, modifiche alle chat e riepiloghi giornalieri tramite Apprise: app di messaggistica, e-mail o il proprio webhook JSON.

**Non** invia il testo dei messaggi a meno che non si abilitino gli estratti.

 [Configurazione delle destinazioni delle notifiche](https://phishdestroy.github.io/TgWitness/it/docs/reference/operations/#notifications)

### Timestamp esterni

Hash dei checkpoint temporali con RFC 3161 e OpenTimestamps.

**Non** considera una ricevuta in sospeso nel calendario come un timestamp Bitcoin confermato.

 [Verificare le prove con timestamp](https://phishdestroy.github.io/TgWitness/it/docs/reference/timestamp/)

### Testimone indipendente

Un host separato conserva le osservazioni firmate e può pubblicare i checkpoint `TGW1`.

**Non** rende indipendenti tra loro due spazi di lavoro presenti su un unico host di raccolta.

 [Configurare un Witness](https://phishdestroy.github.io/TgWitness/it/docs/witness/)

### Recupero e lacune evidenti

Ripresa dopo il riavvio. Le verifiche successive e `coverage.json` mostrano i messaggi recuperati e le lacune.

Cosa**non fa**: non ricostruisce ogni modifica non registrata o ogni messaggio scomparso.

 [Verificare la continuità e le lacune](https://phishdestroy.github.io/TgWitness/it/guides/modes.html#continuity)

## Il Suo primo spazio di lavoro inizia qui.

Provi innanzitutto la demo. Quando è pronto, colleghi un account dedicato. Windows, Linux, macOS o Docker.

[Legga la guida all’installazione](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=it)

**Una sessione importata, un client in esecuzione.**

Si prega di non eseguire contemporaneamente una chiave TData/sessione importata su Telegram Desktop e su TgWitness. Telegram potrebbe invalidare l’autorizzazione condivisa (AUTH_KEY_DUPLICATED). Per un utilizzo parallelo, si prega di creare un account TgWitness separato tramite numero di telefono o codice QR.

[Legga l’avviso relativo all’importazione delle sessioni](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=it#session-warning)

**Si prega di consultare il sito prima di effettuare la connessione.**

Provi l’ambiente di lavoro fittizio senza un account Telegram.

[Aprire la demo online →](https://phishdestroy.github.io/TgWitness/demo/?lang=it)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**Comandi per l’installazione locale**

FASE 01

### Scaricate il codice sorgente.

[Scarichi il file ZIP contenente il codice sorgente](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) ed estragga il contenuto, oppure cloni il repository:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Per l’esecuzione del programma è necessario Python 3.11 o versioni successive. Il programma di avvio per Windows propone l’installazione qualora Python non fosse presente.

[Sfogliare le versioni](https://github.com/phishdestroy/TgWitness/releases)

Non dispone di Python su Windows? [Scarichi il pacchetto portatile](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.1/TgWitness-0.7.1-windows-amd64-portable.zip), lo estragga e faccia doppio clic su `TgWitness.cmd`.

FASE 02

### Scegliete come procedere.

Fare doppio clic su `Start.cmd` oppure eseguire il comando in PowerShell:

```
.\Start.cmd
```

Sta solo dando un’occhiata? Faccia doppio clic su `scripts\Demo.cmd` per una demo isolata. Non è necessario effettuare l’accesso a Telegram.

Con Python 3.11+ e `venv`:

```
sh start.sh
```

Per aprire invece il registro fittizio, esegua il comando `sh start.sh --demo`.

Con Docker in esecuzione e Compose 2.20+ installato:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Il secondo comando mostra il Suo token privato del pannello di controllo. Lo conservi sul Suo computer.

Aprire [127.0.0.1:8787](http://127.0.0.1:8787) dopo l’avvio.

Per le installazioni dal codice sorgente, il token è `data/live/panel-token.txt`. Per l’accesso a Telegram è possibile utilizzare le impostazioni API integrate oppure la propria coppia di credenziali ottenuta da [my.telegram.org](https://my.telegram.org). [Guida completa alla configurazione ↗](https://phishdestroy.github.io/TgWitness/it/docs/reference/quickstart/)

**TgWitness 0.7.1** [Novità →](https://phishdestroy.github.io/TgWitness/it/docs/reference/changelog/) · [Funzionalità e limiti noti →](https://phishdestroy.github.io/TgWitness/it/docs/reference/features/)

## Istruzioni chiare. Un utile passo successivo.

[Esplorate le guide ↗](https://phishdestroy.github.io/TgWitness/it/docs/)

[### Modalità, scenari e livelli di prova Quattro modalità di raccolta. Otto livelli di verifica. Individuate il flusso di lavoro più adatto al vostro caso.](https://phishdestroy.github.io/TgWitness/it/guides/modes.html)

[01 ### Collegare un account Importazione tramite telefono, codice QR e sessioni supportate.](https://phishdestroy.github.io/TgWitness/it/docs/accounts/)[02 ### Scegliere un proxy Elenchi pubblici di MTProxy o il proprio percorso.](https://phishdestroy.github.io/TgWitness/it/docs/proxies/)[03 ### Configurare un bot Witness Punti di controllo firmati nel Suo canale Telegram.](https://phishdestroy.github.io/TgWitness/it/docs/witness/)[04 ### Esportare e verificare Condivida la cronologia acquisita e ne verifichi l’integrità.](https://phishdestroy.github.io/TgWitness/it/docs/exports/)

## Elaborare l’archivio.

Carica la cronologia, esamina le fonti AI, collega un client MCP, riconosci i file multimediali salvati e invia webhook firmati.

[Esplora il flusso di lavoro](https://phishdestroy.github.io/TgWitness/it/docs/archive/)

## Prima di iniziare.

**Questa pagina è collegata a Telegram?**

No. Questa è una pagina statica del progetto con esempi fittizi e schermate. L’applicazione vera e propria viene eseguita sul Suo computer o server; l’accesso avviene lì.

**È in grado di recuperare i messaggi cancellati prima della registrazione?**

No. TgWitness conserva i contenuti rilevati dal Suo account durante l’esecuzione della raccolta. Una successiva istantanea della cronologia non è in grado di ricostruire le modifiche non rilevate o i messaggi cancellati.

**Il mio registro è interamente crittografato?**

Le credenziali degli account e le chiavi di firma sono conservate in un archivio crittografato. I messaggi locali e gli allegati richiedono un disco o un volume crittografato. Le esportazioni possono, facoltativamente, utilizzare un file ZIP AES-256 protetto da password.

**È affiliato a Telegram?**

No. TgWitness è un progetto indipendente che utilizza Telethon, distribuito sotto licenza MIT. L’utente autorizza i propri account utilizzando le impostazioni API integrate o la propria coppia API.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Esplori prima il sito. Effettui la configurazione quando è pronto.

[Aprire la demo](https://phishdestroy.github.io/TgWitness/demo/?lang=it)[Guida all’installazione](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=it)
