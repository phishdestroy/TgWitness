# Cosa è stato testato

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/

Il test in tempo reale su Telegram, i controlli automatizzati, i controlli sul browser e ciò che rimane non verificato.

## Distribuzione su Phala Cloud · 4 novembre 2026

`--provider phala --quick-tunnel` è stato eseguito su un vero **Phala Cloud** (`tdx.small`, regione US-WEST-1) con una chiave API Phala Cloud di uno spazio di lavoro vuoto, il file ntfy.sh originale, GitHub e Intel PCS. La CVM ha installato il commit `df7d860c` (v0.8.1); le operazioni di distribuzione, verifica e distruzione sono state eseguite dalla riga di comando con le correzioni riportate di seguito. Sette CVM sono costate complessivamente circa 1,9 centesimi di dollaro.

Le prime due distribuzioni hanno rilevato cinque differenze rispetto al Phala Cloud simulato. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) ora riproduce ciascuna di esse e fallisce senza la relativa correzione:

| Su Phala Cloud | Prima della correzione | Correzione |
| --- | --- | --- |
| È richiesto `compose_file.name` | HTTP 422, non è stato creato nulla | La configurazione di Docker Compose riporta il nome della CVM |
| A meno che non ne venga specificato uno vuoto, Phala aggiunge il proprio script di pre-avvio al file app-compose sottoposto a misurazione (v0.0.20: login Docker, `docker compose pull`, password di root, chiavi SSH da `user_config`) | `tdx_compose` genera un errore: codice al di fuori della configurazione Docker Compose pubblicata | L’app-compose imposta `pre_launch_script` su `""`; Phala quindi lo omette |
| In assenza di `image`, Phala seleziona `dstack-dev-0.5.12`, la build di sviluppo, con accesso SSH abilitato | `server_state` non supera il controllo. In questa immagine è stato superato solo il record di attestazione hardware; solo il record del fornitore e `tdx_os` lo indicano | L’implementazione richiede la build di produzione dell’attuale versione di Phala, `dstack-0.5.12` |
| Con il gateway dstack disattivato, i dettagli della CVM non riportano mai un codice `instance_id` | La distribuzione attende 30 minuti e fallisce | L’ID dell’istanza viene ricavato dallo stato del CVM |
| I riavvii, gli arresti e gli avviamenti sono operazioni relative alla CVM, non revisioni dell’applicazione | `provider_actions` non ha riportato i riavvii | Le operazioni vengono lette come segue |

La terza distribuzione:

- La CVM ha eseguito `dstack-0.5.12` con l’accesso SSH disattivato. Il collettore ha pubblicato il proprio indirizzo firmato circa 1,5 minuti dopo la creazione. La distribuzione ha quindi superato `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, record di attestazione hardware v4, FMSPC `20a06f000000`, non in modalità debug, non migrabile, con supporto per i dati di verifica crittografica recuperati da Intel), `tdx_compose_hash`, `tdx_compose` (byte per byte) e `tdx_identity` (chiavi KMS).
- Il pannello all’indirizzo trycloudflare.com ha restituito un codice di stato 401 in assenza di token o in presenza di un token errato, e un codice di stato 200 con il token del pannello.
- `verify` con `--source` impostato sull’archivio GitHub del commit e l’impronta digitale superata separatamente: server, `server_state`, firewall (nessun gateway, nessun endpoint pubblico), log del provider, estratto conto, impronta digitale, hash di origine, avvio e i cinque controlli `tdx_*` superati. Cloudflare e `tdx_os` non erano disponibili, pertanto il risultato è stato INCOMPLETO.
- Due riavvii tramite l’API di Phala: ogni volta la CVM è tornata operativa in meno di due minuti con la stessa chiave di raccolta, un nuovo indirizzo firmato e quello precedente che rispondeva con il codice 530. `verify` ha segnalato il nuovo avvio ed entrambi i riavvii come REVIEW. Con `--evidence` ha confermato le firme del journal e tre avvii, ciascuno con il proprio record di attestazione hardware Intel TDX proveniente dallo stesso CVM.
- `destroy` ha rimosso solo quella CVM. L’area di lavoro era quindi vuota e l’indirizzo del pannello ha smesso di rispondere.
- La verifica del prezzo nella procedura guidata del pannello indicava `tdx.small` a 0,058 dollari l’ora. Una chiave errata ha generato un semplice messaggio del tipo «chiave API non accettata».

Altre due anomalie, successivamente risolte:

- In assenza della chiave di indirizzo, `verify` ha seguito l’ultimo post ben formato relativo all’argomento dell’indirizzo, che è riportato nella configurazione Docker Compose pubblicata. Un post contraffatto lo ha indirizzato verso un host inesistente e `statement` ha fallito: un falsario non è riuscito a spacciarsi per il collettore, ma ha potuto bloccare la verifica da parte di terzi, per un massimo di 12 ore, utilizzando un timestamp futuro contraffatto. Il collettore ora pubblica anche il proprio indirizzo firmato con la propria chiave; `verify` accetta solo tali messaggi quando sono emessi dal collettore stesso, e i messaggi vengono ordinati in base all’ora di ricezione da parte di ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) riproduce i post contraffatti. Un CVM esegue questa operazione solo a partire da un commit che la contenga, pertanto il collettore di questa esecuzione non aveva ancora firmato il proprio indirizzo e `verify` lo ha segnalato.
- `tdx_os` non poteva essere eseguito senza `dstack-mr`, la cui versione attuale presenta `measure-os` anziché il `measure --json` indicato nella documentazione. Il verificatore ora calcola autonomamente MRTD e RTMR0-2 a partire dall’immagine pubblicata e dalla configurazione della VM, tabelle ACPI incluse.

La quarta distribuzione, con i seguenti elementi:

- Il processo di distribuzione ha scaricato una volta il file `dstack-0.5.12` pubblicato, lo ha confrontato con l’hash dell’immagine del sistema operativo segnalato dalla CVM e `tdx_os` è risultato conforme: MRTD, RTMR0, RTMR1 e RTMR2 corrispondono ai valori calcolati per QEMU 8.2.2, 1 vCPU e 2 GiB. Lo stesso calcolo ha fornito un valore RTMR0 diverso per una configurazione dichiarata di 4 GiB, 2 vCPU, QEMU 9.2.1 o una seconda scheda di rete, e ha dato esito negativo in caso di modifica del kernel, del firmware o della riga di comando e per l’immagine di sviluppo.
- `verify` ha superato tutti e 16 i controlli, compreso il connettore del tunnel rapido, pertanto il risultato è stato «PASS». Ha generato il certificato in formato HTML e PDF, sigillato digitalmente con firme e timbri temporali, tra cui un timbro temporale eIDAS qualificato fornito dall’ unità di marcatura temporale del governo belga TSU 202301 (stato concesso nell’elenco di fiducia del Belgio ), un timbro temporale FreeTSA e la firma del verificatore; `check-report` ha confermato tutti questi elementi e la firma del PDF.
- Dopo un riavvio, `verify --evidence` ha confermato due avviamenti, ciascuno accompagnato da un’attestazione hardware generata all’interno della CVM e ciascuno avviato dal `dstack-0.5.12` pubblicato; sia il riavvio che il nuovo avvio erano di tipo REVIEW.
- `destroy` ha lasciato l’area di lavoro vuota.

La quinta distribuzione ha eseguito il collector a partire dal commit `53a0f7e9`, che include tutti gli elementi sopra indicati:

- Il collettore ha pubblicato il proprio indirizzo firmato con la propria chiave, accanto al post HMAC dell’operatore. Al thread sono stati quindi aggiunti due post contraffatti, uno con un HMAC azzerato e uno firmato da un’altra chiave Ed25519, entrambi con data indicante l’anno 2096. `verify` ha preso l’indirizzo firmato dalla chiave del collettore e ha superato tutti e 16 i controlli; il sigillo riportava nuovamente il timbro temporale belga qualificato, il timbro temporale di FreeTSA e la firma del verificatore, e `check-report` li ha confermati.
- Dopo un riavvio, il collettore ha pubblicato il nuovo indirizzo firmato: `verify` lo ha individuato immediatamente, mentre l’ operatore **ha individuato l’indirizzo corrente** 27 secondi dopo dal post HMAC, ed entrambi hanno ignorato i post contraffatti. `verify --evidence` ha confermato due avvii effettuati da `dstack-0.5.12`.
- Il processo di distribuzione ha indicato l’importo addebitato da Phala per il CVM, disco incluso: 0,06078 dollari all’ora.

La procedura guidata del pannello è stata eseguita su Phala Cloud due volte: una tramite la sua API di lavoro e una tramite il browser con un Chromium reale: la verifica del prezzo, la creazione con il commit sotto **Advanced**, tutti e sei i controlli di attestazione superati, l’elenco dei server che mostrava il prezzo fatturato (44,37 USD al mese), **Find l’indirizzo corrente**, il download della configurazione Docker Compose misurata e l’eliminazione. Il browser non ha rilevato errori di pagina. In entrambi i casi, l’area di lavoro risultava vuota al termine dell’operazione.

Non inclusi: un dominio Cloudflare su Phala, un account Telegram sul CVM e l’immagine `dstack-0.6.1` . Il prezzo indicato dalla procedura guidata prima della creazione corrisponde esclusivamente al costo di elaborazione di Phala, poiché la sua API indica il costo del disco solo per un CVM esistente; l’elenco dei server mostra il prezzo fatturato dopo la creazione.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Conteggio |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| Verifica | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Test in tempo reale su Telegram, account completo · 29 ottobre 2026

Lo stesso account ha continuato a funzionare dopo il test riportato di seguito. Il 29 ottobre alle ore 12:10 UTC il suo ambito di applicazione è stato esteso all’intero account (canali, gruppi, chat private e bot); il pannello ha richiesto una conferma e il registro firmato ne ha dato atto. Alle ore 17:59 UTC il registro riportava:

| Registrato dal 27 ottobre alle 21:36 al 29 ottobre alle 17:59 UTC | Conteggio |
| --- | --- |
| Registrazioni del registro | 9,968 |
| Nuovi messaggi | 5,308 |
| di essi dopo il passaggio all’account completo | 3,878 |
| Cancellazioni | 784 |
| di cui sono stati cancellati dopo che TgWitness aveva salvato il messaggio | 596 |
| Modifiche | 41 |
| Messaggi aggiunti in seguito a ulteriori verifiche | 2,273 |
| Messaggi che non è stato più possibile individuare in seguito a una nuova verifica | 18 |
| Messaggi salvati tramite istantanee della cronologia | 242 |
| Allegati salvati | 247 |
| Avvio di Collector | 19 |
| Pause di Telegram FloodWait | 26 |

- Il controllo **«Verify»** del comitato ha confermato le firme e la catena di hash di tutti i 9.968 record.
- I messaggi provenivano da 2 gruppi o canali e da 3 chat private e bot. È stato premuto un pulsante di invio messaggio dalla **sezione Chat**; la richiesta e la risposta di Telegram sono riportate nel registro.
- Le nuove chat sono state aggiunte quando il collettore ha eseguito una nuova scansione dell’account al momento del riavvio. Il salvataggio dei messaggi precedenti delle nuove chat era disattivato (`history = 0`), pertanto non viene trattato in questa sede.

Non sono inclusi: reazioni, modifiche alla composizione dei gruppi, profili degli utenti, invio di messaggi, adesione tramite invito, proxy, notifiche, il bot Witness e l’utilizzo di più account contemporaneamente. I file pubblici contengono esclusivamente i conteggi.

## Esportazione protetta da password aperta con libarchive · 29 ottobre 2026

Un archivio creato con il codice di crittografia di esportazione (WinZip AES-256, il formato leggibile da 7-Zip e WinRAR ) è stato aperto con Windows `tar` (bsdtar 3.6.2, libarchive). Con la password corretta, il file estratto corrispondeva allo SHA-256 originale; una password errata è stata rifiutata con il messaggio «Passphrase errata ». 7-Zip e WinRAR non sono stati eseguiti.

## Test in tempo reale su Telegram · dal 27 al 29 ottobre 2026

Un account Telegram reale, connesso tramite il pool di coppie API integrato, ha registrato un supergruppo dal **27 ottobre alle 21:36 UTC al 29 ottobre alle 05:15 UTC**. Il collettore è stato avviato 12 volte in tale periodo.

| Registrato | Conteggio |
| --- | --- |
| Registrazioni del registro, inclusi gli «heartbeat» e i registri di servizio | 2,385 |
| Nuovi messaggi | 1,291 |
| Cancellazioni | 472 |
| di cui alcuni sono stati cancellati dopo che TgWitness ne aveva salvato il testo | 347 |
| Modifiche | 12 |
| Messaggi non rilevati durante la sospensione, aggiunti in seguito a un nuovo controllo | 12 |
| Allegati salvati | 17 |
| Allegati non scaricati (download disattivati o nessun file da scaricare) | 14 |
| Telegram FloodWait effettua delle pause, della durata di 3 secondi ciascuna, durante le verifiche successive | 8 |

- Le firme e la catena di hash di tutti i 2.385 record sono verificabili rispetto alla chiave pubblica del registro.
- Dopo un riavvio, il collettore riprende dallo stato di aggiornamento salvato (`pts`) e Telethon effettua il recupero; la verifica successiva aggiunge quindi i messaggi ancora mancanti.
- Ad ogni evento FloodWait, il collettore attendeva il tempo richiesto e proseguiva.
- L’account è rimasto connesso e la stessa sessione si è ricollegata il 29 ottobre.

Non sono oggetto del presente test: la gestione simultanea di più account, i ruoli di amministratore, i proxy, le interruzioni di servizio di durata superiore a poche ore e la [procedura completa di accettazione in tempo reale](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). I file pubblici contengono esclusivamente questi dati: nessun identificativo di account o chat, nessun messaggio né credenziali.

## Misurazione sintetica della capacità locale

Comando: `python tools/check_capacity.py --events 10000 --chats 100`

| Metrica | Osservato |
| --- | --- |
| Dati in ingresso | 10.000 eventi relativi a messaggi sintetici provenienti da 100 fonti sintetiche selezionate |
| Testo del messaggio | 400 caratteri; nessun contenuto multimediale o di rete |
| Acquisizione | 53,273 secondi; 187,7 eventi al secondo |
| Latenza del gestore | p50 4,162 ms; p95 7,784 ms; massimo 129,118 ms |
| Esportazione in formato ZIP | 19,868 secondi con tracemalloc abilitato |
| Picchi rilevati nelle allocazioni di esportazione in Python | 0,51 MiB; non elaborare RSS |
| Dimensione del file ZIP | 4.610.962 byte |
| Verifica indipendente | Tutti i 10.000 eventi sono stati verificati |

Questo strumento misura il percorso locale di registrazione/esportazione seriale su questo host Windows. Non misura la consegna MTProto, gli account simultanei, la limitazione di banda di Telegram, i file multimediali, un carico di lavoro di lunga durata né un numero garantito di chat reali. La misurazione è antecedente alla versione definitiva dello strumento di timestamp offline, che non modifica il percorso dei messaggi misurato.

## Ulteriori precisazioni

Il registro in tempo reale conservato attesta l’effettiva raccolta, le modifiche, le notifiche di cancellazione, gli allegati, le verifiche successive e la gestione dei limiti di frequenza. Non documenta in modo esaustivo la consegna né fornisce una matrice controllata di visibilità dei ruoli, soggetti coinvolti, FloodWait prolungato, sospensioni degli account e ripristino in caso di interruzione della rete o dei processi. L’emissione del token QR rimane distinta dalla conferma tramite codice QR mobile completata.

La compilazione/esecuzione con Docker, l’installazione su Linux/macOS, la gestione di carichi elevati prolungati, la revisione indipendente della sicurezza, una risposta TSA realmente indipendente, la convalida della revoca/archiviazione dei certificati e la certificazione forense rimangono al di fuori della qualifica registrata. Sono implementati lo stato salvato di MTProto e il catch-up; il replay atomico durevole rimane non stabilito. La raccolta dei log di amministrazione, gli elenchi aggiuntivi dei reattori e il polling breve prioritario rimangono funzionalità separate. Si veda [l’accettazione in tempo reale](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) per la matrice di qualificazione controllata.

Le ricevute locali dettagliate e gli screenshot si trovano nella cartella test-results/ (ignorata da Git). Gli screenshot pubblici presenti in docs/assets/ contengono esclusivamente dati dimostrativi fittizi.
