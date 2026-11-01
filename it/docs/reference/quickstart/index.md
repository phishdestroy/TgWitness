# Guida rapida

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/quickstart/

Tutte le modalità di installazione e avvio di TgWitness: pacchetto per Windows, Python, Docker e la demo sintetica, con i primi controlli.

**Inglese** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [Ucraino](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [Portoghese (Brasile)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [Cinese semplificato](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness è un’applicazione autonoma per il monitoraggio dei gruppi e dei canali di Telegram a cui i vostri account possono accedere. Funziona in locale con una propria directory di dati.

**È la prima volta che visita questo sito?** [Esplori la demo](https://phishdestroy.github.io/TgWitness/it/docs/reference/quickstart/#explore-the-interface) prima di collegare un account. [Scelga una guida](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) relativa a proxy, testimoni, esportazioni o configurazione del server.

## Installazione e avvio

[Acquisizione con GitHub Actions (anteprima)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

Scegliete un metodo. I download portatili diventano disponibili dopo la pubblicazione di una build di rilascio:

| Host | Nessuna installazione richiesta | Dalla fonte: Python 3.11+ | Docker: Engine/Desktop con Compose 2.20+ |
| --- | --- | --- | --- |
| Windows | Estrarre `TgWitness-<version>-windows-amd64-portable.zip` dai rilasci di GitHub, fare doppio clic su `TgWitness.cmd` | Fare doppio clic su `Start.cmd` | Fare doppio clic su `scripts\Docker.cmd` |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

Per i metodi basati sul codice sorgente, [scarica ed estrai il ramo `main` corrente](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) oppure clona il repository:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

`Start.cmd` propone di installare Python 3.12 per il tuo utente Windows se non viene trovato un Python adatto (tramite winget o il programma di installazione firmato di python.org). `start.sh` mostra il comando di installazione esatto per la tua distribuzione Linux o macOS se Python è assente. Il primo avvio da sorgente crea `.venv` e installa automaticamente le dipendenze.

Docker compila l’applicazione e la avvia in background; non è necessario un host Python. `scripts\Docker.cmd` e `scripts/docker-start.sh` visualizzano l’indirizzo del pannello e il token quando il container è in stato di funzionamento. I comandi Docker equivalenti su ogni host supportato sono:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Apra **http://127.0.0.1:8787**. Utilizzi il token generato dall’helper di Docker o dal secondo comando Docker, oppure consulti **il file data/live/panel-token.txt** per un’installazione portatile o dal codice sorgente. Prosegua alla sezione **«Connetti Telegram»** qui sotto. Le installazioni native e Docker utilizzano archivi separati; l’avvio di Docker non importa un registro nativo esistente.

Per quanto riguarda il server, [l’implementazione](https://phishdestroy.github.io/TgWitness/it/docs/reference/deployment/) comprende l’HTTPS automatico, il riavvio, le immagini pubblicate, gli aggiornamenti e i backup.

## Esplorate l’interfaccia

1. Eseguire **TgWitness-Demo.cmd** nel pacchetto portatile, **scripts\Demo.cmd** in una cartella sorgente di Windows oppure `sh start.sh --demo` su Linux/macOS. L’esecuzione dal sorgente crea innanzitutto `.venv` e installa le dipendenze.
2. **http://127.0.0.1:8787** aperto.
3. La demo locale apre automaticamente il registro di esempio. Non è necessaria alcuna copia del token per l’accesso locale diretto.

I messaggi di dimostrazione sono fittizi. La modalità demo non consente di collegare un account Telegram reale.

## Collegare Telegram

> [!AVVERTENZA] **Non utilizzi nulla che non possa permettersi di perdere.** Le sconsigliamo vivamente di collegare account personali o di valore e di creare un ID API / hash su un account a cui tiene particolarmente. Telegram blocca gli account in modo imprevedibile e spesso in modo permanente, indipendentemente dal client utilizzato. Il corretto svolgimento della prova dipende da Telegram, non da TgWitness, e non garantisce nulla per il futuro.

1. Se la demo nativa è in esecuzione, la interrompa ed esegua **Start.cmd** o `sh start.sh`. In caso contrario, mantenga in esecuzione l’installazione live avviata in precedenza.
2. Utilizzi il token del pannello corrispondente al Suo metodo di installazione per aprire il pannello.
3. Se ha bisogno di un proxy, lo salvi in **Account → Impostazioni → Impostazioni di connessione → Modifica percorso di connessione**.
4. Nella sezione **Account**, inserisca il Suo numero di telefono e prema **Continua**, scelga **Codice QR → Mostra codice QR**, oppure selezioni i file e prema **Collega account**. **L’ID API + Hash** è facoltativo: l’area di lavoro utilizza la coppia salvata o importata, oppure una coppia funzionante dal pool integrato. Per utilizzare la Sua app, incolli una coppia `API ID:API Hash` nel campo ID API. Per ottenere una chiave di autorizzazione completa, selezionare **“Chiave di autenticazione”**, incollare tutti i 512 caratteri esadecimali e selezionare l’ID DC fornito. L’ID utente è facoltativo e, se inserito, viene selezionato automaticamente.
5. Completare la procedura di accesso selezionata: telefono/codice/2FA, conferma da un’ app Telegram con accesso attivo per il codice QR, oppure importazione di una sessione autorizzata supportata.
6. Verifichi l’ID dell’account visualizzato. **Fonti** aperte: le Sue chat vengono caricate automaticamente; aggiunga i Suoi gruppi.
7. Nella sezione **«Scegliere quali modifiche conservare»**, selezionare le categorie di eventi o il preset **«Messaggi, modifiche e cancellazioni»**, quindi salvare le impostazioni di monitoraggio.
8. Selezionare separatamente le impostazioni relative agli allegati, quindi premere **«Avvia monitoraggio**».

Le credenziali API identificano la vostra applicazione; di per sé non autorizzano un account. I gruppi privati non richiedono un nome utente pubblico, ma il vostro account deve disporre dei diritti di accesso.

Per gli account esistenti, consulta [account e formati di sessione](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/): il pannello accetta Telethon StringSession, SQLite Telethon/Pyrogram, file ZIP TData a singolo account e file JSON di account supportati. Seleziona insieme una sessione e il relativo file JSON associato, quindi premi **Collegare l’account**. È disponibile anche l'accesso tramite QR con le stesse impostazioni API opzionali. TDLib, sessioni bot e inventari di account CSV/JSON non sono supportati.

Per più account, usa **Account → Importazione degli account** e seleziona i relativi file di sessione supportati. I file JSON associati vengono abbinati in base al nome base; ogni account importato ottiene il proprio spazio di lavoro. Consulta [importazione in blocco e gruppi di account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#bulk-import-and-account-groups).

Per aggiungere un altro account, prema **+** accanto al selettore di account oppure apra **Account → Impostazioni → Impostazioni di connessione → Spazi di lavoro**, oppure utilizzi **la sezione Account**. Gli spazi di lavoro dispongono di sessioni, registri, chiavi, fonti e code separati. Il cambio di vista lascia in esecuzione gli altri collettori. Lo stesso account Telegram non può essere assegnato a due spazi di lavoro in questa installazione. Non esiste un numero fisso di spazi di lavoro; essi condividono un unico processo, pertanto la capacità dipende dalla macchina.

Il token del pannello live protegge l’accesso alle vostre autorizzazioni Telegram e al materiale salvato; è separato dalle credenziali dell’API di Telegram. Solo una demo locale avviata esplicitamente e a cui si accede direttamente ottiene l’accesso automatico. Una demo remota o tramite proxy continua a utilizzare `data/demo/panel-token.txt`.

## Revisione ed esportazione

- **Registro:** ricerca e filtraggio delle osservazioni in base alla fonte e al tipo di evento.
- Selezioni un evento per esaminarne la registrazione originale, l’attribuzione e le versioni salvate.
- I dettagli delle modifiche mostrano i contenuti disponibili prima e dopo. I dettagli delle cancellazioni mostrano l’ ultimo contenuto acquisito, se presente; un autore sconosciuto rimane tale.
- **Formati di esportazione:** ZIP firmato, JSONL, CSV e HTML offline.
- **Esportazione completa della chat** (Fonti → Esportazione completa della chat): scaricate l’intera cronologia visibile di una chat sotto forma di pacchetto firmato con `chat.json` (in stile Telegram-export) e un file leggibile `chat.html`. Le chat private funzionano se l’account è membro del gruppo. Si tratta di un’istantanea attuale, non di una ricostruzione di messaggi cancellati o modificati in precedenza. Verifichi una copia con `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256`.
- **Punto di controllo:** mantenere i confini del registro firmato al di fuori del collettore.
- **Scaricare la ricevuta di esecuzione firmata:** conservare la registrazione del programma e della versione del collettore.
- **Preparazione della richiesta di timestamp:** preparare una richiesta offline all’autorità di timestamp; seguire le istruzioni contenute nel file [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/timestamp/) per ottenere e verificare la risposta.
- **Verifica del registro:** controllate le firme degli eventi e i collegamenti della catena. L’esportazione in formato ZIP verifica anche i file multimediali.

I browser supportati salvano esportazioni di grandi dimensioni direttamente in un file a scelta. Gli altri browser memorizzano nel buffer al massimo 128 MiB. Mentre il server è in esecuzione, la CLI di streaming supporta download di dimensioni maggiori senza memorizzare l’intera risposta nel buffer:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Per un altro spazio di lavoro, aggiunga `--profile ID` tramite **Esportazioni → ID spazio di lavoro**. Per un server remoto, aggiunga `--url https://your-server`. Il limite di trasferimento predefinito è di 5 GiB; `--max-mib` lo modifica. Il contenuto ZIP firmato ha un limite di verifica separato di 4 GiB non compressi per impostazione predefinita (**Parameters** lo aumenta; verificare tali archivi con `verify.py --max-gib N`). Verificare l’archivio utilizzando una copia attendibile del verificatore e un’impronta digitale/checkpoint della chiave conservata in modo indipendente.

## Verificare l’installazione

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check` verifica le dipendenze locali, il supporto alla firma, lo spazio di archiviazione, la configurazione delle chiavi e l’indirizzo di ascolto. Non installa nulla né si connette a Telegram. Una porta occupata potrebbe indicare che è in esecuzione un’altra istanza. Utilizzi un altro `--port` oppure interrompa prima l’istanza in corso.

Il programma di avvio si installa in `.venv`. I comandi ausiliari `python -m tgwitness...` devono utilizzare `.venv\Scripts\python.exe` su Windows o `.venv/bin/python` su Linux/macOS, a meno che tale ambiente non sia già attivato.

## Sessioni, protezione e funzionamento

Un file Telethon SQLite `.session` chiuso e coerente può essere convertito localmente con `python -m tgwitness.sessions account.session --out account.tgwitness-session`, quindi caricato in Account. Sono disponibili anche l’importazione diretta dei file e l’accesso tramite codice QR. Si veda [il file CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/) per i formati di accesso, SOCKS5, HTTP CONNECT, MTProxy e le chiavi master esterne.

**La funzione «Pausa osservazione»** interrompe la raccolta. **La funzione «Blocca»** chiude solo l’accesso tramite browser. La chiusura di una scheda lascia in esecuzione il processo di raccolta. L’arresto del processo interrompe la raccolta; un’istantanea della cronologia non è in grado di ricostruire tutte le modifiche o le cancellazioni mancanti. Scoprite [come funziona la raccolta](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/) in relazione alle politiche sugli eventi, alle code degli allegati, all’isolamento degli account e al comportamento in caso di riavvio.

Le sessioni e i dati riservati sono crittografati. Il contenuto dei messaggi, i file multimediali e le esportazioni richiedono un disco o un volume crittografato. Le firme garantiscono l’integrità rispetto a una chiave attendibile; non attestano l’origine da Telegram né impediscono la falsificazione da parte di un operatore che controlli il collettore e la relativa chiave.

Si prega di consultare [il file OPERATIONS.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/operations/) per le operazioni di backup e ripristino, [il file DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/deployment/) per l’hosting e [la directory deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) per esempi di utilizzo del servizio. Il pannello installato include inoltre una guida alla configurazione offline all’indirizzo `/guide.html`.

La verifica effettiva e i limiti rimanenti sono riportati nei file [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/) e [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md).
