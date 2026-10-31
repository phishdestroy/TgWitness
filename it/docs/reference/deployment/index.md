# Implementazione

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/deployment/

Eseguite TgWitness come servizio su Windows, Linux, macOS o Docker, tramite HTTPS, con backup e aggiornamenti.

**Inglese** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [Ucraino](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [Portoghese (Brasile)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [Cinese semplificato](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## Scegliere un'installazione

Per il pacchetto portatile, estrarre `TgWitness-<version>-windows-amd64-portable.zip` da GitHub Releases. Per gli altri metodi, scaricare ed estrarre il file ZIP contenente il codice sorgente oppure clonare il repository, quindi eseguire il seguente comando dalla directory del progetto:

| Installazione | Inizio | Funziona in background? |
| --- | --- | --- |
| Pacchetto portatile per Windows | `TgWitness.cmd` | No; mantenga la finestra aperta. |
| Versione nativa per Windows | `Start.cmd` | No; si utilizzi l’attività di accesso opzionale per l’esecuzione in background. |
| Versione nativa per Linux/macOS | `sh start.sh` | No; si utilizzi systemd/launchd per l’esecuzione in background. |
| Docker su qualsiasi host supportato | `docker compose up -d --build --wait` | Sì, mentre il daemon di Docker è in esecuzione. |
| Guida all’uso di Docker su Windows | `scripts\Docker.cmd` | Sì; l’helper attende che il server web sia operativo. |
| Guida all’uso di Docker su Linux/macOS | `sh scripts/docker-start.sh` | Sì; l’helper attende che il server web sia operativo. |

Per un server cloud che possa essere verificato da terzi — creato tramite l’ API del provider, senza SSH, raggiungibile esclusivamente tramite un Cloudflare Tunnel — si veda [la sezione dedicata all’implementazione ad alta sicurezza](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md).

L’avvio nativo crea un file `.venv` privato e installa le dipendenze fissate. Docker le compila all’interno dell’immagine, senza richiedere Python sull’host. La configurazione iniziale richiede l’accesso a Internet. Qualora non venga rilevata la presenza di Python 3.11 o versioni successive, `Start.cmd` chiede conferma prima di installare Python 3.12 per l’utente Windows corrente (tramite winget, oppure tramite il programma di installazione di python.org dopo aver verificato la firma della Python Software Foundation); non richiede mai privilegi di amministratore. Docker e i servizi del sistema operativo rimangono prerequisiti.

Le installazioni native e portatili utilizzano `data/live` all’interno della propria cartella. Docker utilizza il volume denominato `tgwitness-data` all’indirizzo `/data`. Si tratta di installazioni separate fino a quando non si esegue deliberatamente la migrazione della directory dei dati completa. Non si deve aspettarsi che un nuovo container Docker rilevi automaticamente gli account nativi.

## Requisiti di installazione

L’installazione nativa richiede Python 3.11 o versioni successive con `venv` e `ensurepip`, accesso a Internet per l’installazione della prima dipendenza e una directory di progetto scrivibile per `.venv`. Il pannello integrato non richiede Node.js né la compilazione del frontend. Eseguite il programma di avvio dal vostro normale account del sistema operativo; TgWitness non richiede privilegi di amministratore/root.

- **Windows:** `Start.cmd` verifica `py -3`, poi `python`, quindi le cartelle di installazione predefinite per utente e in «Programmi», e richiede la versione 3.11 o successive. Se nessuna di queste opzioni funziona, viene proposta l’installazione automatica per utente descritta sopra. Funziona anche `py -3 start.py`. Il pacchetto portatile non richiede affatto Python.
- **Linux:** `start.sh` prova `python3.13`, `python3.12`, `python3.11`, `python3` e `python`, e visualizza il comando di installazione per apt, dnf, pacman, zypper, apk o Homebrew qualora nessuno di essi risulti idoneo. Le installazioni su Debian/Ubuntu potrebbero richiedere il pacchetto `python3-venv` corrispondente all’interprete selezionato. La versione predefinita più vecchia di Python presente in una distribuzione deve essere sostituita o integrata con Python 3.11+.
- **macOS:** installi una distribuzione aggiornata di Python 3.11 o superiore; non dia per scontato che un interprete fornito dal sistema operativo soddisfi i requisiti. Utilizzi `python3 start.py` dalla directory del progetto.
- **Docker:** si raccomanda di utilizzare Docker Engine/Desktop con Compose v2.20 o versioni successive. Docker Desktop deve utilizzare container Linux su Windows. Il container installa le proprie dipendenze Python; l’host non necessita di un’installazione separata di Python.

Utilizzi un archivio locale persistente per la directory dei dati. Pianifichi la capacità in base ai messaggi, ai file multimediali, alla crescita del WAL, alle esportazioni e ai backup; non esiste una specifica minima universale, basata su prove concrete, relativa a disco/RAM per ogni carico di lavoro. Le architetture CPU e le versioni di Python prive di wheel di dipendenze compatibili potrebbero richiedere strumenti di compilazione aggiuntivi e una loro specifica qualificazione. Il termine «portatile» non implica un supporto universale per sistemi operativi o hardware.

Il funzionamento su Windows 11/Python 3.12 è stato verificato localmente. Le definizioni per Linux/macOS/container e la CI sono fornite, ma non sono state eseguite su questo host di sviluppo. Si veda [il file VERIFICATION.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/) per l’ambito esatto.

## Computer locale

Utilizzi `Start.cmd` su Windows o `sh start.sh` su Linux/macOS. `scripts\Setup.cmd` o `sh start.sh --setup-only` preparano l’ambiente. Il programma di avvio installa le dipendenze al primo utilizzo; gli avvii successivi riutilizzano l’ambiente. È necessario l’accesso a Internet per la configurazione e la raccolta dei dati da Telegram, ma la consultazione dei record esistenti e la creazione di esportazioni funzionano offline.

Eseguire `python start.py --check` dopo la configurazione per verificare le dipendenze locali, Ed25519, lo spazio di archiviazione, la configurazione delle chiavi e l’indirizzo di ascolto senza avviare un collettore. Utilizzi `--json` per un output strutturato. Passi i comandi `--data-dir`, `--host` e `--port` previsti. Il controllo non installa pacchetti, non crea un registro né si connette a Telegram; non si tratta di una verifica di integrità o di copertura. All’avvio vengono verificati separatamente i registri esistenti. Anche `python start.py --help` evita l’installazione.

Opzioni:

Dopo aver eseguito start.py, esegua i comandi ausiliari con `.venv\Scripts\python.exe` su Windows o `.venv/bin/python` su Linux/macOS, oppure attivi prima tale ambiente. Gli esempi `python -m ...` riportati di seguito presuppongono che l’ambiente sia attivo.

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

Variabili d’ambiente: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN. TGWITNESS_VAULT_KEY_FILE seleziona la modalità con chiave esterna per una nuova installazione; si veda di seguito. TGWITNESS_TOKEN, se specificato, deve contenere almeno 24 caratteri; si raccomanda di utilizzare un valore casuale generato crittograficamente. In assenza di tale parametro, l’applicazione genera un token casuale a 256 bit nel file panel-token.txt. La sovrascrittura delle variabili d’ambiente non modifica tale file. Si prega di riavviare il sistema per aggiornare le credenziali.

Esattamente un solo processo può essere proprietario di una directory di dati. Un blocco dei file multipiattaforma a livello di sistema operativo impedisce scritture simultanee accidentali. Utilizzi un solo worker Uvicorn. Il pannello di controllo è in grado di gestire un numero illimitato di spazi di lavoro, con directory aggiuntive per gli spazi di lavoro all’interno di profiles/<id>/. Per istanze di servizio separate, utilizzare directory e porte distinte. I file WAL di SQLite devono risiedere su un’area di archiviazione locale persistente , non su un file system di rete. Non condividere un unico volume tra le repliche.

## Pacchetto portatile per Windows

Ogni versione su GitHub include `TgWitness-<version>-windows-amd64-portable.zip` e il relativo `.sha256`. Contiene il runtime ufficiale incorporabile di Python 3.12 proveniente da python.org (checksum fissato in `tools/build_portable.py`), TgWitness e le sue dipendenze fisse, oltre a tre programmi di avvio:

| File | Scopo |
| --- | --- |
| `TgWitness.cmd` | Avviare il pannello; le opzioni aggiuntive vengono trasmesse, ad esempio `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | Avviare la demo sintetica in `data\demo` |
| `TgWitness-Check.cmd` | Eseguire il controllo di prontezza senza avviare il sistema |

Estraete l’intero archivio in una cartella scrivibile, ad esempio `Documents\TgWitness`; non eseguite il programma dall’interno del file ZIP né dalla cartella Programmi. Il runtime utilizza un percorso dei moduli isolato, pertanto altre installazioni di Python e `PYTHONPATH` non lo influenzano. I dati rimangono nella cartella `data` del pacchetto. Per effettuare l’aggiornamento, interrompa l’esecuzione di TgWitness, estragga la nuova versione in una nuova cartella e copi la cartella `data` nella nuova posizione.

Compilatelo autonomamente su Windows a 64 bit con Python 3.12:

```
python tools/build_portable.py
```

Il builder verifica il checksum di runtime, installa le dipendenze vincolate nel pacchetto, esegue il controllo di prontezza con l’interprete incorporato e salva il file ZIP e il checksum su `dist/`.

## Contenitore

```
docker compose up -d --build --wait
```

Ciò crea un volume persistente con nome per /data. La porta web è mappata su 127.0.0.1:8787. Il processo viene eseguito con UID 10001 con capacità ridotte, un filesystem root di sola lettura e le directory /data e /tmp scrivibili. `--wait` verifica lo stato di salute del server web prima di restituire un risultato; non stabilisce l’ autorizzazione né la consegna di Telegram. Gli helper forniti utilizzano un timeout di disponibilità di 180 secondi dopo la compilazione. Il download iniziale delle dipendenze potrebbe richiedere più tempo.

Entrambi i file Compose di base utilizzano il nome del progetto `tgwitness`; pertanto, l’estrazione di una nuova versione in un’altra directory non comporta la selezione automatica di un nuovo volume di dati. Mantenga attiva una sola distribuzione per quel progetto. Per installazioni indipendenti, utilizzi un `docker compose -p NAME ...` univoco e una porta host diversa, conservando entrambi in caso di aggiornamenti. Per una distribuzione precedente che utilizza un nome di progetto diverso, continui a utilizzare il nome originale con `-p`; `docker compose ls` elenca i progetti esistenti.

Copi `deploy/env.example` in `.env` e modifichi `TGWITNESS_PORT` per utilizzare una porta di loopback diversa. Ad esempio, `TGWITNESS_PORT=8788` espone il pannello all’indirizzo `http://127.0.0.1:8788`; il container continua a ascoltare sulla porta 8787. `.env` è ignorato da Git.

Recuperare il token iniziale:

```
docker compose exec tgwitness cat /data/panel-token.txt
```

Comandi utili:

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` riavvia il collector in seguito a un arresto anomalo o al riavvio del daemon di Docker . Su un server Linux, abiliti Docker all’avvio utilizzando il gestore dei servizi della Sua distribuzione , solitamente `sudo systemctl enable --now docker`. Su Windows/macOS, abiliti l’impostazione “Avvia all’accesso” di Docker Desktop. La disconnessione dal desktop, la modalità di sospensione o l’arresto del possono interrompere la raccolta. Un container arrestato esplicitamente rimane arrestato fino a quando non lo si riavvia.

Il volume /tmp è limitato a 512 MiB nella configurazione di esempio. La procedura di esportazione utilizza invece l’`temporary-exports/` di ciascun spazio di lavoro sul volume persistente /data. Si raccomanda di riservare spazio in tale posizione per le esportazioni simultanee, la crescita del registro/WAL, i file multimediali e i backup. Il programma di avvio utilizza il file deploy/constraints.txt per fissare le versioni qualificate delle dipendenze di runtime. I server Docker e ad alta sicurezza vengono installati da deploy/requirements.lock e deploy/build.lock con pip --require-hashes: ogni file del pacchetto deve corrispondere a uno SHA-256 registrato nel commit, pertanto un file sostituito su PyPI o su un mirror viene rifiutato. L’immagine di base Python e i pacchetti del sistema operativo richiedono ancora una qualificazione indipendente della versione.

Non utilizzi il comando `docker compose down -v` a meno che non intenda distruggere il registro e le chiavi. Lo stato di integrità del container indica la disponibilità del server web, non il corretto funzionamento della cattura dei messaggi di Telegram. Verifichi lo stato del collettore del pannello, l’heartbeat, gli errori e gli eventi di copertura.

### Profilo del testimone indipendente

Il servizio opzionale `witness` esegue un [witness indipendente](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/) nel proprio container, con chiave e registro propri nel volume `witness-data` e solo un token witness in sola lettura per il collector. Creare il token nella pagina **Witness** del pannello di controllo, aggiungerlo insieme a un token bot e a un canale a `.env`, quindi avviare il profilo:

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

Il servizio raggiunge il collettore all’interno della rete Compose all’indirizzo `http://tgwitness:8787` (`TGWITNESS_WITNESS_COLLECTOR` lo sovrascrive; ad esempio, `/profiles/<workspace ID>` per un altro spazio di lavoro). Per un witness su un server separato, gestito da qualcun altro, utilizzi `deploy/compose/compose.witness.yaml` , impostando `TGWITNESS_WITNESS_COLLECTOR` sull’indirizzo HTTPS del collettore; tale file contiene esclusivamente il witness.

## Installare un'immagine pubblicata

Tale contenuto diventa disponibile al termine di un [flusso di lavoro di rilascio](https://phishdestroy.github.io/TgWitness/it/docs/reference/deployment/#automated-github-releases) andato a buon fine e della configurazione pubblica del pacchetto GHCR. Il nome del proprietario del repository non è hardcoded in questo albero di sorgenti. Si prega di utilizzare l’immagine riportata nel riepilogo del flusso di lavoro di quella versione.

Copi `deploy/env.example` in `.env`. Imposti `TGWITNESS_IMAGE` sulla versione pubblicata, utilizzando il percorso del repository **in minuscolo**, ad esempio:

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.0
TGWITNESS_PORT=8787
```

Esegua questo file autonomamente, anziché `compose.yaml`:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

Non sono necessari build del codice sorgente, Python o compilatori sull’host. Il flusso di lavoro di rilascio è destinato a container Linux AMD64 e ARM64, inclusa la macchina virtuale Linux di Docker Desktop. Utilizzi un tag di versione o «`ghcr.io/owner/repository@sha256:...`» dal riepilogo del flusso di lavoro. Non è configurato alcun tag «`latest`» mobile né alcun aggiornamento automatico dell’applicazione. L’ immagine e le varianti del codice sorgente utilizzano lo stesso volume di dati quando il nome del progetto corrisponde.

## HTTPS automatico su un server

Utilizzi un server con Docker, un dominio di sua proprietà e uno spazio di archiviazione locale persistente. Indirizzi i record A/AAAA del dominio verso il server; pubblichi il record AAAA solo se l’IPv6 lo raggiunge. Consenta il traffico in entrata su TCP 80 e 443 e quello in uscita su DNS/HTTPS per l’emissione dei certificati. Tali porte non devono essere già occupate da altri servizi.

Copi `deploy/env.example` in `.env` e imposti un nome host, senza schema né percorso:

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

Avviare la compilazione del codice sorgente con l’overlay HTTPS:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

Per un’immagine pubblicata, utilizzi invece `deploy/compose/compose.image.yaml` come primo file. Mantenga entrambi gli argomenti `-f` per i successivi comandi relativi a stato, registri, aggiornamento e arresto.

Caddy ottiene e rinnova un certificato, reindirizza il traffico HTTP verso HTTPS e inoltra le richieste al collettore sulla rete privata Compose. Lo stato del certificato dispone di un proprio volume persistente. La porta host diretta del collettore rimane riservata esclusivamente al loopback. La configurazione di Caddy fornita non abilita la registrazione degli accessi.

Apra `https://watch.your-domain.org` e inserisca il token del pannello. La verifica della prontezza non conferma l’emissione del certificato né la raggiungibilità esterna. Se HTTPS non è pronto, verifichi il DNS, le regole del firewall e:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

L’immagine Caddy fornita è contrassegnata dal tag `2-alpine`. Eseguendo il comando «pull» si aggiorna tale immagine; se necessitate di versioni fisse dell’infrastruttura, inserite un digest verificato nella vostra distribuzione.

## Aggiornamenti e backup

Mantenere il nome del progetto Compose e il volume dei dati durante gli aggiornamenti. Arrestare innanzitutto il collettore ed eseguire un backup completo. Per l’implementazione predefinita basata sulla sorgente:

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Utilizzi ogni volta una nuova destinazione di backup, esterna al repository, e la protegga come materiale di accesso all’account. Il percorso riportato a titolo esemplificativo; utilizzi la Sua posizione di backup privata. Copi l’intera directory, inclusi i file nascosti, tutti gli spazi di lavoro, le chiavi, i registri e i file multimediali. Esegua separatamente il backup della chiave master del vault esterno, se configurata. Un file ZIP contenente le prove non è un backup dell’applicazione ripristinabile. Per HTTPS, conservi anche i volumi Caddy qualora sia necessario mantenere lo stato del certificato o dell’account.

Per l’installazione dal codice sorgente, si prega di procurarsi i file della nuova versione ed eseguire:

```
docker compose up -d --build --wait
```

Per l’implementazione dell’immagine, sostituisca `TGWITNESS_IMAGE` con la versione desiderata, quindi esegua:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Utilizzi i file Compose della Sua installazione anche per i comandi stop/copy precedenti. Mantenete `.env`, la configurazione personalizzata e lo stesso nome del progetto. `down` conserva i volumi denominati; **`down -v` li elimina**. Non copiate `.venv` tra sistemi operativi o versioni di Python. Per gli aggiornamenti nativi, arrestate TgWitness, eseguite il backup della sua intera directory dei dati, sostituite i file sorgente ed eseguite `python start.py --setup-only` prima del lancio.

Verifichi l’accesso al pannello di controllo, l’identità dell’account, lo stato di monitoraggio e la copertura dopo un aggiornamento. Il riavvio non ripristina gli aggiornamenti di Telegram persi. Un rollback potrebbe richiedere il backup precedente all’aggiornamento qualora una versione futura modifichi i formati di archiviazione.

## Rilasci automatizzati su GitHub

Il [flusso di lavoro di rilascio](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml) è pronto all’uso dopo che il presente progetto è stato caricato in un repository GitHub con Actions abilitato. Si avvia quando viene **pubblicata** una versione su GitHub, compresa una versione preliminare. Le bozze e i push di tag da soli non comportano la pubblicazione dei pacchetti.

1. Impostare la versione del pacchetto e il log delle modifiche, quindi pubblicare una versione contrassegnata con `v` più la versione esatta `pyproject.toml`, ad esempio `v0.7.0`.
2. Il flusso di lavoro convalida il tag ed esegue i controlli condivisi per Windows/Linux/macOS relativi a Python, general/account-import/QR browser, source-package e Docker. Viene inoltre eseguita un’installazione nativa ex novo su tutti e tre i sistemi operativi utilizzando Python 3.12.
3. Una volta superati tali controlli, esegue uno smoke test su un’immagine ARM64 in ambiente QEMU, pubblica le immagini AMD64/ARM64 su `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>`, e allega alla versione il file ZIP del codice sorgente, il checksum e il pacchetto Python wheel. Un processo separato su Windows compila e allega il file ZIP portatile e il relativo checksum.
4. Dopo la prima pubblicazione, apra le impostazioni del pacchetto GHCR e imposti la visibilità su **«Pubblico»** qualora si intenda effettuare il recupero anonimo delle immagini. Un repository di origine pubblico di per sé non garantisce un pacchetto container pubblico. Le politiche dell’organizzazione devono consentire la pubblicazione del pacchetto. Il flusso di lavoro utilizza `GITHUB_TOKEN`; nessuna password del registro né credenziali VPS devono essere presenti nel repository.

Il successo del flusso di lavoro remoto non è stato ancora dimostrato da questa configurazione locale. L’emulazione ARM64 costituisce un test preliminare, non una qualificazione su hardware nativo o su Telegram in tempo reale. Ciò automatizza la creazione del pacchetto di rilascio; l’avvio di un server richiede comunque il comando Compose e i relativi prerequisiti relativi a dominio/host. I server esistenti non vengono aggiornati né riavviati in modo automatico quando viene pubblicata una nuova versione.

## Server remoto

Si raccomanda di mantenere il servizio limitato al loopback e di utilizzare un tunnel SSH, oppure di terminare la connessione HTTPS presso un proxy inverso. Il file Compose di base è solo locale; l’overlay opzionale `deploy/compose/compose.https.yaml` fornisce Caddy per un dominio configurato. Si raccomanda di non includere il token bearer negli URL e nei log del proxy. Un proxy inverso dovrebbe limitare la dimensione delle richieste e la frequenza delle connessioni. Si raccomanda di non esporre HTTP in chiaro a Internet.

Sono forniti esempi relativi a systemd, a un’attività di accesso a Windows, a un user agent di macOS e a Caddy nella cartella [deploy/.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Si raccomanda di verificare e adattare i relativi percorsi prima dell’installazione. Si tratta di modelli forniti, non di configurazioni della piattaforma eseguite localmente. Nessun servizio o attività in background viene registrato dal normale programma di avvio.

Su Windows, l’avvio senza finestra di `pythonw.exe` memorizza le diagnostiche di avvio/server in `logs/server.log` all’interno della directory dei dati (5 MiB per file, due backup a rotazione). L’avvio da console conserva i log della console. La registrazione degli accessi HTTP è disabilitata in entrambe le modalità. Protegga i log insieme alla directory dei dati e li esamini prima di condividerli.

## Riavvio e lacune

Viene mantenuto l’ultimo stato di monitoraggio richiesto. Se il monitoraggio era attivo, all’avvio il sistema tenta di riconnettersi e riprendere le fonti selezionate. La pausa manuale annulla tale intenzione. Un riavvio non riuscito viene registrato e visualizzato nel pannello.

StringSession conserva l’autorizzazione ma non lo stato permanente degli aggiornamenti/delle entità di Telethon. Le finestre di dialogo vengono ricaricate all’avvio. Telegram/Telethon è in grado di recuperare alcune interruzioni di trasmissione durante l’esecuzione, ma TgWitness non garantisce la riproduzione permanente in caso di riavvio del processo. Ad ogni avvio vengono registrati l’intestazione del registro precedente e il confine offline. Il monitor verifica la connettività ogni 10 secondi e aggiunge un segnale di attività ogni minuto (**Parametri → Registrazione di attività ogni**). Brevi interruzioni potrebbero non essere rilevate; un trasporto connesso non garantisce la completa consegna degli aggiornamenti. Le istantanee sono osservazioni esplicite della cronologia corrente, mai una riparazione di lacune.

La coda dei file multimediali è memorizzata nel database SQLite di ciascun spazio di lavoro. Un messaggio e la relativa operazione vengono salvati in modo atomico. Le operazioni in esecuzione interrotte vengono recuperate per essere riprovate all’avvio. Ogni download ha un timeout di base di 120 secondi più un tempo calcolato a 256 KiB/s in base alla sua dimensione, e un limite compreso tra 1 e 2.000 MiB per tipo di allegato; timeout, velocità e tentativi di ripetizione sono gestiti nella sezione **Parametri**. Il collettore salta i file la cui dimensione è sconosciuta. La messa in pausa conserva il lavoro in coda. Il riprovo utilizza il descrittore di file originale osservato, mai l’ultima versione di un messaggio modificato successivamente. Gli errori temporanei hanno un numero limitato di riprovi; le pause di FloodWait per i file multimediali sopravvivono al riavvio. Il recupero dei file multimediali è separato dal recupero degli aggiornamenti dei Telegram e non può ricreare i file scomparsi.

## Backup, ripristino e capacità

Interrompa il processo prima di copiare **l’intera directory dei dati**, inclusi vault.key, signing.enc, credentials.enc, il database SQLite e i file WAL, i file multimediali, il token, i checkpoint, e tutte le sottodirectory dei profili. Ripristini la copia completa mentre il servizio di destinazione è arrestato. La mancanza di chiavi del vault o la non corrispondenza delle chiavi di firma causano il fallimento dell’avvio; non rigeneri le chiavi per forzare l’accesso.

Conservare i backup segreti crittografati e con accesso controllato. I file ZIP contenenti le prove sono artefatti di revisione portatili, non backup dell’applicazione né delle sessioni di Telegram. Non è prevista alcuna cancellazione automatica in base a criteri di conservazione. Prevedere spazio su disco sufficiente per tutti i messaggi, i metadati grezzi, i file multimediali, le esportazioni temporanee e i backup.

Verifica iniziale ed esportazione dei record di flusso anziché caricare l’intero registro. Un’esportazione blocca un’istantanea di lettura mentre possono continuare le nuove scritture WAL; le esportazioni di lunga durata possono conservare le pagine WAL, pertanto la capacità del disco rimane un fattore rilevante. I file ZIP hanno un limite massimo di 4 GiB non compressi, in linea con l’impostazione predefinita del verificatore indipendente; **Parametri → ZIP firmato più grande** aumenta il limite, e tali archivi vengono verificati con `verify.py --max-gib N`. Altri formati non hanno limiti al numero di eventi. I browser supportati trasmettono in streaming blocchi di risposta in un file selezionato dall’utente. Altri browser memorizzano nel buffer al massimo 128 MiB e indirizzano i trasferimenti di dimensioni maggiori alla CLI autenticata:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Utilizzi `--profile ID` da **Esportazioni → ID area di lavoro** per un’altra area di lavoro, `--format zip|jsonl|csv|html`, `--url https://your-server` per un server remoto, oppure `--max-mib` per modificare il limite di trasferimento di 5 GiB. Il protocollo HTTP semplice è consentito solo per il loopback. I token viaggiano nelle intestazioni, i reindirizzamenti vengono rifiutati, i file esistenti non vengono sovrascritti e i download incompleti non vengono pubblicati come file completati. Se TGWITNESS_TOKEN sovrascrive il token generato, utilizzi un file protetto separatamente contenente tale valore attivo: panel-token.txt non viene riscritto dalla sovrascrittura. Lo SHA-256 del comando è solo un checksum di trasferimento; verifichi in modo indipendente il file ZIP firmato.

I file di esportazione del server rimangono all’interno della directory privata `temporary-exports/` di ciascun spazio di lavoro. Le operazioni andate a buon fine eliminano i propri file. Le esportazioni interrotte vengono rimosse al successivo avvio dell’area di lavoro, con il blocco dell’istanza esclusiva ancora attivo. Questa directory fa parte del modello di minaccia/capacità di archiviazione; si raccomanda l’uso di un volume di dati crittografato. I trasferimenti su scala produttiva dell’ordine di diversi gigabyte richiedono comunque una verifica sul sistema di destinazione.

Il pannello visualizza i file multimediali in coda o non riusciti, i file multimediali in sospeso più vecchi, lo spazio libero su disco, le sospensioni delle richieste di Telegram e le fonti il cui accesso non è stato confermato. Queste informazioni diagnostiche non costituiscono un monitoraggio completo della consegna end-to-end. Gli spazi di lavoro condividono un unico processo; un account che genera molto traffico può comunque influire sugli altri. Rimangono i processi di lavoro separati, la conservazione/rotazione, il recupero durevole degli aggiornamenti e la qualificazione completa dell’implementazione. L’accesso limitato al pannello è documentato nelle sezioni relative ad [accesso e autorizzazioni](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/); i punti di controllo indipendenti sono trattati nella [guida per i testimoni](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/).

## Opzioni di connessione e protezione

I percorsi di connessione sono specifici per ogni area di lavoro e devono essere configurati prima dell’autorizzazione. SOCKS5/HTTP CONNECT utilizzano la dipendenza python-socks fissata. MTProxy utilizza il trasporto intermedio randomizzato sperimentale di Telethon; i segreti TLS ee falsi non sono supportati. Il fallback diretto dipende dalla [modalità IP](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/#ip-modes) selezionata: «Hide IP» lo rifiuta; la modalità di fallback esplicita lo consente dopo un ritardo. La modalità Tunnel/VPN consente percorsi diretti ma non crea una VPN. Non si tratta di una politica di rete a livello di sistema.

Per le nuove installazioni, TGWITNESS_VAULT_KEY_FILE punta a un file di chiave principale casuale protetto separatamente. Montatelo in sola lettura all’esterno della directory /data all’interno di un container. Conservate separatamente i metadati pubblici del file vault.external.json relativi al salt per ogni area di lavoro e la chiave principale. I vault locali esistenti richiedono una migrazione pianificata; l’impostazione di questa variabile non li converte automaticamente. L’archiviazione e l’esportazione di messaggi e file multimediali non sono crittografate dall’applicazione. Si raccomanda di utilizzare volumi crittografati e uno spazio di archiviazione temporaneo privato sufficiente, ove necessario.

Procedure dettagliate: [connessione/sicurezza](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/) e [modalità operative](https://phishdestroy.github.io/TgWitness/it/docs/reference/operations/).
