# I messaggi cambiano． Conservi ciò che ha visto．

Canonical page: https://phishdestroy.github.io/TgWitness/it/

[Open source ／ v0.9.1](https://phishdestroy.github.io/TgWitness/it/docs/reference/changelog/)

Salvi le chat di Telegram con ogni modifica ed eliminazione e consegni un registro che chiunque può verificare．

[Aprire la demo](https://phishdestroy.github.io/TgWitness/demo/?lang=it)[Guida all＇installazione](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=it)

Dati fittizi， nessun accesso a Telegram．

 [Acquisizione con GitHub Actions （anteprima）](https://phishdestroy.github.io/TgWitness/it/docs/capture/) [Copia off－site su S3： configurazione e ripristino](https://phishdestroy.github.io/TgWitness/it/#s3)

UN MESSAGGIO ATTRAVERSO IL TEMPO ＃0042

Northstar · RicercaFonte fittizia ／ messaggio 42

1. **Messaggio rilevato：**09：41：02

   Il briefing inizia all＇indirizzo 14：00．
2. **Modifica conservata**09：43：18

   Il briefing inizia all＇indirizzo 15：00．

   Versione precedente mantenuta
3. **Avviso di cancellazione**10：06：45

   I contenuti acquisiti rimangono nel Vostro registro．

Tre osservazioni． Una storia． ESEMPIO

Il messaggio scompare． La cronologia acquisita rimane．

## Ogni modifica registrata． Proprio dove ne avete bisogno．

La vera interfaccia， con dati inventati．

TgWitness ／ Chat salvateIL VOSTRO SPAZIO DI LAVORO PER L＇OSSERVAZIONE

![Conversazioni Telegram salvate con tema scuro， con le modifiche e i messaggi cancellati acquisiti e conservati nel loro contesto](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ Chat salvate Sembra una chat normale， con modifiche ed eliminazioni proprio accanto ai messaggi．

TgWitness ／ RegistroAREA DI LAVORO LOCALE

![Registro contenente i messaggi rilevati， le modifiche， le notifiche di cancellazione e gli eventi coperti](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ Diario Tutto ciò che il Suo account ha visto， ricercabile， lacune comprese．

TgWitness ／ Cronologia delle modificheAREA DI LAVORO LOCALE

![Pannello di dettaglio che mette a confronto la versione precedente e quella modificata di un messaggio](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ Cronologia modifiche Versione vecchia e nuova affiancate， niente viene sovrascritto．

TgWitness ／ Esportazioni firmateAREA DI LAVORO LOCALE

![Funzionalità di esportazione dell＇area di lavoro che offre un file ZIP firmato， JSONL， CSV e un report HTML offline](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ Esportazioni firmate Porti con sé il diario， firmato e con il suo verificatore．

Seguire un record salvato attraverso [Case Board](https://phishdestroy.github.io/TgWitness/it/docs/case-board/)， [la progettazione del report](https://phishdestroy.github.io/TgWitness/it/docs/reports/) e una [copia condivisa](https://phishdestroy.github.io/TgWitness/it/docs/handover/)． [Esaminare i gruppi di account](https://phishdestroy.github.io/TgWitness/it/docs/groups/) nel loro insieme．

01 ／ ACQUISIZIONE

### Siete voi a scegliere l＇ambito di applicazione．

Poche chat， una cartella o l＇intero account． Ogni account ha il proprio spazio．

[Confronto tra le modalità di raccolta](https://phishdestroy.github.io/TgWitness/it/guides/modes.html#scope)

02 ／ PRESERVE

### Le modifiche arricchiscono la narrazione．

Versioni， eliminazioni e lacune restano tutte nel diario．

[Consultare la matrice degli eventi](https://phishdestroy.github.io/TgWitness/it/guides/modes.html#events)

03 ／ CONSEGNA

### Una registrazione che viaggia．

ZIP firmato， file e report offline． Password facoltativa．

[Esportare e verificare](https://phishdestroy.github.io/TgWitness/it/docs/exports/)

## Basta modificare un byte．
La verifica te lo segnalerà．

Ogni evento è collegato all＇hash precedente e reca una firma Ed25519．

![Gli eventi acquisiti sono collegati agli hash precedenti， recano le firme e vengono esportati in un formato verificabile．](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![La modifica di un record acquisito ne altera l＇hash e compromette la verifica del record collegato．](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Un punto di controllo conservato separatamente consente al destinatario di confrontare il registro esportato con un＇osservazione precedente．](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Seguire i controlli dall＇hash di un file a un checkpoint conservato separatamente．

[Scoprite gli otto livelli di prova](https://phishdestroy.github.io/TgWitness/it/guides/modes.html#levels)

## Pronto per una revisione．

Messaggi， file e report offline in un unico pacchetto firmato．

[Legga il modello di prova](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/)

tgwitness-evidence.zipPACCHETTO FIRMATO

- 01

  Osservazioni originaliRecord JSONL ＋ tabella CSV
- 02

  Contesto di facile letturaRapporto HTML offline ＋ file multimediali conservati
- 03

  Verifica indipendenteManifesto firmato ＋ verificatore autonomo

Il destinatario controlla tutto con la Sua chiave， e un punto di controllo conservato altrove mostra che da allora non è stato riscritto nulla． [Come funzionano i controlli．](https://phishdestroy.github.io/TgWitness/it/docs/concepts/#layers)

## Copie su S3． Controlli esterni．

Conservare copie crittografate e aggiungere controlli indipendenti．

Disattivato per impostazione predefinita

### Copiare tutto su un archivio compatibile con S3

Diario， file， punti di controllo ed esportazioni delle chat， cifrati prima di andare su S3．

**Impostazioni di archiviazione e recupero**

Crittografia lato client

`AES-256-GCM` sulla Sua macchina． Il provider vede solo testo cifrato．

Copie programmate o manuali

Copi subito oppure ogni 1－1.440 minuti， con l＇avanzamento nel pannello．

Object Lock

Scelga giorni e modalità di conservazione： il pannello verifica che siano davvero applicati．

Recupero verificato

Tenga la chiave separata． Ripristini dove vuole： i file escono solo dopo la verifica．

![Pannello completo per il copia fuori sede： endpoint， regione， bucket， chiavi di accesso， pianificazione， Object Lock e controlli delle chiavi di ripristino](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Il pannello completo con le opzioni avanzate è espanso． Non vengono visualizzate credenziali di accesso all＇archivio．

Giornale e media`AES-256-GCM`Archiviazione compatibile con S3

[Configurare S3 e ripristinare una copia](https://phishdestroy.github.io/TgWitness/it/docs/exports/#s3)[Legga i dettagli della verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Chiave di recupero** La tenga separata： senza， la copia è illeggibile．

### Notifiche · Apprise

Problemi， modifiche nelle chat e un riepilogo giornaliero verso messaggistica， e－mail o il Suo webhook．

**Scelga cosa condividere** Nessun testo dei messaggi finché non lo attiva．

 [Configurazione delle destinazioni delle notifiche](https://phishdestroy.github.io/TgWitness/it/docs/reference/operations/#notifications)

### Timestamp esterni

Hash dei checkpoint temporali con RFC 3161 e OpenTimestamps．

**Segua il risultato** Controlli la risposta della TSA o aggiorni la ricevuta OpenTimestamps a una prova Bitcoin．

 [Verificare le prove con timestamp](https://phishdestroy.github.io/TgWitness/it/docs/reference/timestamp/)

### Testimone indipendente

Un host separato conserva le osservazioni firmate e può pubblicare i checkpoint `TGW1`．

**Separi il riferimento** Lo esegua su un altro host， con chiave e diario propri．

 [Configurare un Witness](https://phishdestroy.github.io/TgWitness/it/docs/witness/)

### Recupero e lacune evidenti

Ripresa dopo il riavvio． Le verifiche successive e `coverage.json` mostrano i messaggi recuperati e le lacune．

**Esamini l＇intervallo** Messaggi recuperati e lacune registrate affiancati．

 [Verificare la continuità e le lacune](https://phishdestroy.github.io/TgWitness/it/guides/modes.html#continuity)

## Il Suo primo spazio di lavoro inizia qui．

Provi prima la demo e colleghi un account di riserva quando è pronto．
Windows， Linux， macOS o Docker．

[Legga la guida all＇installazione](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=it)

**Una sessione importata， un client in esecuzione．**

Non usi una TData o una sessione importata contemporaneamente in Telegram Desktop e in TgWitness： Telegram può invalidarle entrambe （AUTH_KEY_DUPLICATED）． Le servono tutte e due？ Acceda a TgWitness separatamente， con telefono o QR．

[Legga l＇avviso relativo all＇importazione delle sessioni](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=it#session-warning)

**Si prega di consultare il sito prima di effettuare la connessione．**

Provi l＇ambiente di lavoro fittizio senza un account Telegram．

[Aprire la demo online →](https://phishdestroy.github.io/TgWitness/demo/?lang=it)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**Comandi per l＇installazione locale**

FASE 01

### Scaricate il codice sorgente．

[Scarichi il file ZIP contenente il codice sorgente](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) ed estragga il contenuto， oppure cloni il repository：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Richiede Python 3.11+． Su Windows il launcher propone di installarlo．

[Sfogliare le versioni](https://github.com/phishdestroy/TgWitness/releases)

FASE 02

### Scegliete come procedere．

Fare doppio clic su `Start.cmd` oppure eseguire il comando in PowerShell：

```
.\Start.cmd
```

Sta solo dando un＇occhiata？ Faccia doppio clic su `scripts\Demo.cmd` per una demo isolata． Non è necessario effettuare l＇accesso a Telegram．

Con Python 3.11+ e `venv`：

```
sh start.sh
```

Per aprire invece il registro fittizio， esegua il comando `sh start.sh --demo`．

Con Docker in esecuzione e Compose 2.20+ installato：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Il secondo comando mostra il Suo token privato del pannello di controllo． Lo conservi sul Suo computer．

Aprire [127.0.0.1:8787](http://127.0.0.1:8787) dopo l＇avvio．

Nelle installazioni da sorgente il token si trova in `data/live/panel-token.txt`． Una Sua coppia API da [my.telegram.org](https://my.telegram.org) è facoltativa． [Guida completa ↗](https://phishdestroy.github.io/TgWitness/it/docs/reference/quickstart/)

**TgWitness 0.9.1** [Novità →](https://phishdestroy.github.io/TgWitness/it/docs/reference/changelog/) · [Funzionalità e limiti noti →](https://phishdestroy.github.io/TgWitness/it/docs/reference/features/)

## Istruzioni chiare． Un utile passo successivo．

[Esplorate le guide ↗](https://phishdestroy.github.io/TgWitness/it/docs/)

[### Modalità， scenari e livelli di prova Quattro modalità di raccolta． Otto livelli di verifica． Individuate il flusso di lavoro più adatto al vostro caso．](https://phishdestroy.github.io/TgWitness/it/guides/modes.html)

[01 ### Collegare un account Importazione tramite telefono， codice QR e sessioni supportate．](https://phishdestroy.github.io/TgWitness/it/docs/accounts/)[02 ### Scegliere un proxy Elenchi pubblici di MTProxy o il proprio percorso．](https://phishdestroy.github.io/TgWitness/it/docs/proxies/)[03 ### Configurare un bot Witness Punti di controllo firmati nel Suo canale Telegram．](https://phishdestroy.github.io/TgWitness/it/docs/witness/)[04 ### Esportare e verificare Condivida la cronologia acquisita e ne verifichi l＇integrità．](https://phishdestroy.github.io/TgWitness/it/docs/exports/)

## Elaborare l＇archivio．

Cronologia， IA con fonti， MCP， OCR e webhook firmati．

[Esplora il flusso di lavoro](https://phishdestroy.github.io/TgWitness/it/docs/archive/)

## Prima di iniziare．

**Questa pagina è collegata a Telegram？**

No． È una pagina statica con esempi fittizi． L＇app gira sulla Sua macchina ed è lì che si accede．

**È in grado di recuperare i messaggi cancellati prima della registrazione？**

No． Conserva ciò che il Suo account ha visto mentre era in funzione． Un＇istantanea successiva non può ricostruire modifiche perse o messaggi eliminati．

**Il mio registro è interamente crittografato？**

Sessioni e chiavi sì． Messaggi e file no： usi la cifratura del disco． Le esportazioni possono avere una password AES－256．

**È affiliato a Telegram？**

No． È un progetto indipendente con licenza MIT basato su Telethon． Si accede con i propri account．

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Esplori prima il sito． Effettui la configurazione quando è pronto．

[Aprire la demo](https://phishdestroy.github.io/TgWitness/demo/?lang=it)[Guida all＇installazione](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=it)
