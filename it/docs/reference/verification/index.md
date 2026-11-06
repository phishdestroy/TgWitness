# Cosa è stato testato

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/

Il test in tempo reale su Telegram, i controlli automatizzati, i controlli sul browser e ciò che rimane non verificato.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Updated 6 November 2026.** Results are tied to the revision, environment and workload recorded for each run. [Current capabilities](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describes the available workflows; this page records what has actually been checked.

[Performance graphs](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Signed English audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Downloadable measurements](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Latest evidence | Risultato | Ambito di applicazione |
| --- | --- | --- |
| Release audit · 6 Nov | 1,461 core tests passed; 37 platform skips | Source `92e539af40d8`; open findings retained |
| Fresh exports · 6 Nov | 127.713 and 141.781 records/s, complete cycle | Two accounts per server; text and metadata through WARP |
| Retained archives · 6 Nov | 48 archives; 3,598,381 records verified | Existing archives checked against pinned workspace keys |
| Trusted Live · 5 Nov | Guarded CPU recording and WARP checks | Official Desktop login and native export remain unqualified |
| Phala / Intel TDX · 4 Nov | All 16 verifier checks passed on later runs | Historical deployment; no Telegram account on the CVM |

**On this page**

- [Release audit and fresh exports · 6 November 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu and WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live Phala Cloud deployment · 4 November 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Live server journal inventory · 1 November 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Recent offline and fault-injection checks · 1 November 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live Telegram test, whole account · 29 October 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Password-protected export opened with libarchive · 29 October 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live Telegram test · 27 to 29 October 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetic local capacity measurement](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Full-text search on one million messages · 5 November 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Remaining qualification](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#remaining-qualification)

## Release audit and fresh exports · 6 November 2026

The audit used v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. Installed-package smoke checks passed on three servers. The signed report retains the state observed at that time.

[![Acquisition and complete export rates for two fresh workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Workload | Registrazioni | Acquisition | Complete cycle | Complete-cycle rate |
| --- | --- | --- | --- | --- |
| Server A · two accounts | 27,030 | 189.043 s | 211.647 s | 127.713 records/s |
| Server B · two accounts | 29,299 | 182.513 s | 206.650 s | 141.781 records/s |

Both exports began without resume, excluded attachments and avatars, and ended with zero duplicate or reused records. The complete cycle includes preparation, acquisition, selection, packaging and archive verification. Server A also ran a protected-chat read check. Four FloodWait events on A and three on B were respected. These observations do not establish a general throughput guarantee.

| Verifica | Risultato | Qualification |
| --- | --- | --- |
| Core pytest | 1,461 passed | 37 platform skips |
| Browser / browser UX / evidence / site | 102 / 66 / 15 / 9 passed | These programs overlap other tests; counts are not additive |
| Capture addon | 124 passed | Three Official Web checks blocked by the required Chromium sandbox |
| API authorization | 269 routes; 538 requests passed | Missing credentials and revoked access |
| Retained archives | 48 of 48 verified | 3,598,381 records; pinned workspace keys |
| Live fleet read checks | 24 of 40 profiles passed | 16 WARP routes failed qualification; those profiles were not connected |

The [signed report](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) records all open findings, including three defects in an unpublished secret-chat snapshot absent from the audited main build. The earlier [public-history qualification](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) used a different revision and workload; its rates must not be combined with this comparison.

Verify the original report using the [pinned key and verifier](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Its signature protects the operator's report from alteration. It is not independent attestation, proof of Telegram authorship or GDPR certification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Distribuzione su Phala Cloud · 4 novembre 2026

**Historical result:** later deployments passed all 16 verifier checks, including Intel TDX and the quick tunnel. Restart evidence, signed address discovery and report timestamps were checked separately. Each test CVM was removed after its run.

| Configurazione | Recorded value |
| --- | --- |
| Fornitore | Phala Cloud · `tdx.small` · US-WEST-1 |
| Implementazione | `--provider phala --quick-tunnel`; initially empty workspace |
| Initial collector | `df7d860c` · v0.8.1 |
| Collector with all fixes | `53a0f7e9` |
| Production guest | `dstack-0.5.12`; SSH access disabled |
| External services | ntfy.sh, GitHub and Intel PCS |
| Observed cost | Seven CVMs, about 1.9 US cents together; historical test pricing |

The sequence below separates initial failures, fixes and completed checks. No Telegram account was connected to these CVMs.

**Deployments 1–2 · provider differences and regression checks**

Le prime due distribuzioni hanno rilevato cinque differenze rispetto al Phala Cloud simulato. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) ora riproduce ciascuna di esse e fallisce senza la relativa correzione:

| Su Phala Cloud | Prima della correzione | Correzione |
| --- | --- | --- |
| È richiesto `compose_file.name` | HTTP 422, non è stato creato nulla | La configurazione di Docker Compose riporta il nome della CVM |
| A meno che non ne venga specificato uno vuoto, Phala aggiunge il proprio script di pre-avvio al file app-compose sottoposto a misurazione (v0.0.20: login Docker, `docker compose pull`, password di root, chiavi SSH da `user_config`) | `tdx_compose` genera un errore: codice al di fuori della configurazione Docker Compose pubblicata | L’app-compose imposta `pre_launch_script` su `""`; Phala quindi lo omette |
| In assenza di `image`, Phala seleziona `dstack-dev-0.5.12`, la build di sviluppo, con accesso SSH abilitato | `server_state` non supera il controllo. In questa immagine è stato superato solo il record di attestazione hardware; solo il record del fornitore e `tdx_os` lo indicano | L’implementazione richiede la build di produzione dell’attuale versione di Phala, `dstack-0.5.12` |
| Con il gateway dstack disattivato, i dettagli della CVM non riportano mai un codice `instance_id` | La distribuzione attende 30 minuti e fallisce | L’ID dell’istanza viene ricavato dallo stato del CVM |
| I riavvii, gli arresti e gli avviamenti sono operazioni relative alla CVM, non revisioni dell’applicazione | `provider_actions` non ha riportato i riavvii | Le operazioni vengono lette come segue |

**Deployment 3 · attestation, access checks and restart evidence**

- La CVM ha eseguito `dstack-0.5.12` con l’accesso SSH disattivato. Il collettore ha pubblicato il proprio indirizzo firmato circa 1,5 minuti dopo la creazione. La distribuzione ha quindi superato `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, record di attestazione hardware v4, FMSPC `20a06f000000`, non in modalità debug, non migrabile, con supporto per i dati di verifica crittografica recuperati da Intel), `tdx_compose_hash`, `tdx_compose` (byte per byte) e `tdx_identity` (chiavi KMS).
- Il pannello all’indirizzo trycloudflare.com ha restituito un codice di stato 401 in assenza di token o in presenza di un token errato, e un codice di stato 200 con il token del pannello.
- `verify` con `--source` impostato sull’archivio GitHub del commit e l’impronta digitale superata separatamente: server, `server_state`, firewall (nessun gateway, nessun endpoint pubblico), log del provider, estratto conto, impronta digitale, hash di origine, avvio e i cinque controlli `tdx_*` superati. Cloudflare e `tdx_os` non erano disponibili, pertanto il risultato è stato INCOMPLETO.
- Due riavvii tramite l’API di Phala: ogni volta la CVM è tornata operativa in meno di due minuti con la stessa chiave di raccolta, un nuovo indirizzo firmato e quello precedente che rispondeva con il codice 530. `verify` ha segnalato il nuovo avvio ed entrambi i riavvii come REVIEW. Con `--evidence` ha confermato le firme del journal e tre avvii, ciascuno con il proprio record di attestazione hardware Intel TDX proveniente dallo stesso CVM.
- `destroy` ha rimosso solo quella CVM. L’area di lavoro era quindi vuota e l’indirizzo del pannello ha smesso di rispondere.
- La verifica del prezzo nella procedura guidata del pannello indicava `tdx.small` a 0,058 dollari l’ora. Una chiave errata ha generato un semplice messaggio del tipo «chiave API non accettata».

**Follow-up fixes · signed address discovery and OS measurements**

- In assenza della chiave di indirizzo, `verify` ha seguito l’ultimo post ben formato relativo all’argomento dell’indirizzo, che è riportato nella configurazione Docker Compose pubblicata. Un post contraffatto lo ha indirizzato verso un host inesistente e `statement` ha fallito: un falsario non è riuscito a spacciarsi per il collettore, ma ha potuto bloccare la verifica da parte di terzi, per un massimo di 12 ore, utilizzando un timestamp futuro contraffatto. Il collettore ora pubblica anche il proprio indirizzo firmato con la propria chiave; `verify` accetta solo tali messaggi quando sono emessi dal collettore stesso, e i messaggi vengono ordinati in base all’ora di ricezione da parte di ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) riproduce i post contraffatti. Un CVM esegue questa operazione solo a partire da un commit che la contenga, pertanto il collettore di questa esecuzione non aveva ancora firmato il proprio indirizzo e `verify` lo ha segnalato.
- `tdx_os` non poteva essere eseguito senza `dstack-mr`, la cui versione attuale presenta `measure-os` anziché il `measure --json` indicato nella documentazione. Il verificatore ora calcola autonomamente MRTD e RTMR0-2 a partire dall’immagine pubblicata e dalla configurazione della VM, tabelle ACPI incluse.

**Deployment 4 · all 16 checks, report seals and restart verification**

- Il processo di distribuzione ha scaricato una volta il file `dstack-0.5.12` pubblicato, lo ha confrontato con l’hash dell’immagine del sistema operativo segnalato dalla CVM e `tdx_os` è risultato conforme: MRTD, RTMR0, RTMR1 e RTMR2 corrispondono ai valori calcolati per QEMU 8.2.2, 1 vCPU e 2 GiB. Lo stesso calcolo ha fornito un valore RTMR0 diverso per una configurazione dichiarata di 4 GiB, 2 vCPU, QEMU 9.2.1 o una seconda scheda di rete, e ha dato esito negativo in caso di modifica del kernel, del firmware o della riga di comando e per l’immagine di sviluppo.
- `verify` ha superato tutti e 16 i controlli, compreso il connettore del tunnel rapido, pertanto il risultato è stato «PASS». Ha generato il certificato in formato HTML e PDF, sigillato digitalmente con firme e timbri temporali, tra cui un timbro temporale eIDAS qualificato fornito dall’ unità di marcatura temporale del governo belga TSU 202301 (stato concesso nell’elenco di fiducia del Belgio ), un timbro temporale FreeTSA e la firma del verificatore; `check-report` ha confermato tutti questi elementi e la firma del PDF.
- Dopo un riavvio, `verify --evidence` ha confermato due avviamenti, ciascuno accompagnato da un’attestazione hardware generata all’interno della CVM e ciascuno avviato dal `dstack-0.5.12` pubblicato; sia il riavvio che il nuovo avvio erano di tipo REVIEW.
- `destroy` ha lasciato l’area di lavoro vuota.

**Deployment 5 · collector-signed discovery and forged-post rejection**

The collector ran from commit `53a0f7e9`, which includes the fixes above.

- Il collettore ha pubblicato il proprio indirizzo firmato con la propria chiave, accanto al post HMAC dell’operatore. Al thread sono stati quindi aggiunti due post contraffatti, uno con un HMAC azzerato e uno firmato da un’altra chiave Ed25519, entrambi con data indicante l’anno 2096. `verify` ha preso l’indirizzo firmato dalla chiave del collettore e ha superato tutti e 16 i controlli; il sigillo riportava nuovamente il timbro temporale belga qualificato, il timbro temporale di FreeTSA e la firma del verificatore, e `check-report` li ha confermati.
- Dopo un riavvio, il collettore ha pubblicato il nuovo indirizzo firmato: `verify` lo ha individuato immediatamente, mentre l’ operatore **ha individuato l’indirizzo corrente** 27 secondi dopo dal post HMAC, ed entrambi hanno ignorato i post contraffatti. `verify --evidence` ha confermato due avvii effettuati da `dstack-0.5.12`.
- Il processo di distribuzione ha indicato l’importo addebitato da Phala per il CVM, disco incluso: 0,06078 dollari all’ora.

### Panel wizard and remaining scope

La procedura guidata del pannello è stata eseguita su Phala Cloud due volte: una tramite la sua API di lavoro e una tramite il browser con un Chromium reale: la verifica del prezzo, la creazione con il commit sotto **Advanced**, tutti e sei i controlli di attestazione superati, l’elenco dei server che mostrava il prezzo fatturato (44,37 USD al mese), **Find l’indirizzo corrente**, il download della configurazione Docker Compose misurata e l’eliminazione. Il browser non ha rilevato errori di pagina. In entrambi i casi, l’area di lavoro risultava vuota al termine dell’operazione.

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation. All prices in this section were observed on 4 November 2026.

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

## Ricerca full-text su un milione di messaggi · 5 novembre 2026

Comando: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

Un registro firmato deterministico di 1.000.000 di messaggi sintetici in 200 chat (forme lessicali russe, ucraine, inglesi, cinesi, giapponesi, link e handle) è stato indicizzato in 71 secondi; l’indice ha occupato 58 MiB oltre al registro da 1,50 GiB. Le ricerche per migliore corrispondenza hanno richiesto da 9 a 190 ms (mediana), contro i 2,4-3,2 secondi della precedente ricerca per sottostringa . Risultati completi, hardware e limiti: [Ricerca full-text](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#benchmark). `tools/test_fulltext.py` verifica anche un archivio firmato creato prima della ricerca full-text (`tools/fixtures/evidence-before-fulltext.zip`) con il verificatore corrente, e un archivio corrente con quello stesso archivio `verify.py`.

## Ulteriori precisazioni

Il registro in tempo reale conservato attesta l’effettiva raccolta, le modifiche, le notifiche di cancellazione, gli allegati, le verifiche successive e la gestione dei limiti di frequenza. Non documenta in modo esaustivo la consegna né fornisce una matrice controllata di visibilità dei ruoli, soggetti coinvolti, FloodWait prolungato, sospensioni degli account e ripristino in caso di interruzione della rete o dei processi. L’emissione del token QR rimane distinta dalla conferma tramite codice QR mobile completata.

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

The [public audit directory](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) contains only the signed report and aggregate measurements. Detailed operational receipts, raw captures and account material remain private. Application screenshots in `docs/assets/` use fictional demonstration data.
