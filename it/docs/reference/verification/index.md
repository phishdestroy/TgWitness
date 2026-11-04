# Cosa è stato testato

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/

Il test in tempo reale su Telegram, i controlli automatizzati, i controlli sul browser e ciò che rimane non verificato.

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
