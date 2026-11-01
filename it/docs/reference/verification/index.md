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

Le voci precedenti riportate di seguito descrivono le rispettive esecuzioni; la maggior parte di esse ha utilizzato client di test sintetici. Di seguito sono riportati i risultati automatizzati più recenti.

## Elenchi MTProxy pubblici integrati · 29 ottobre 2026

Si tratta del registro storico dei test relativi alla versione originale con selezione manuale. Per le attuali modalità automatiche «pool» e «IP», si rimanda [alle impostazioni di connessione](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/#ip-modes). I conteggi e le funzionalità non supportate riportati di seguito si riferiscono a quella revisione testata.

Sono stati aggiunti uno snapshot pubblico integrato e un aggiornamento HTTPS esplicito da SoliSpirit/mtproto e zakky8/mtproto-proxy-pro. Su questo host, il programma di download dell’applicazione ha recuperato entrambi i feed con successo il 29 ottobre 2026 alle 12:58 UTC: **118 endpoint univoci compatibili** dopo il filtraggio, la deduplicazione e l’applicazione del limite di 64 voci per fonte. Ciò verifica il recupero dell’elenco, non la connettività né la consegna dei messaggi tramite tali endpoint. Nessun account reale è stato collegato a un proxy presente nell’elenco durante questo lavoro. [Guida per l’operatore e l’utente](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/PROXIES.md).

Le risposte della fonte non riuscite, vuote o incompatibili mantengono le voci e le date precedenti. Gli aggiornamenti non modificano il percorso selezionato. Gli indirizzi pubblici vengono convalidati e gli IP risolti vengono fissati al momento della selezione; i percorsi gestiti dall’operatore o quelli manuali rimangono separati. Il test di connessione è ora disponibile nel pannello prima dell’accesso all’account. Il certificato TLS contraffatto e la selezione automatica del proxy rimangono non supportati. Il catalogo dell’operatore prevale completamente sugli abbonamenti.

- Suite completa: **366 superati, 3 saltati**, 287,94 secondi. Permangono gli avvisi relativi alle dipendenze esistenti e i salti relativi alla piattaforma. Regressione finale dell’elenco pubblico/localizzazione: **36 superati**, incluso il rifiuto di porte proxy di download non valide; ciò si sovrappone alla suite completa.
- Test di compatibilità con i browser superato in inglese/russo, modalità chiara/scura a 390/1440 pixel: opzioni integrate, nessun recupero esterno all’apertura delle impostazioni, aggiornamento esplicito, mantenimento dei percorsi e della cache in caso di errori, verifica pre-accesso, isolamento dell’area di lavoro in caso di risposta tardiva, dettagli sulla fonte e layout/contrasto. Nessun errore JavaScript né richieste esterne al browser.
- La copertura finale della traduzione statica è stata approvata per tutte le 13 lingue; il nuovo testo è stato tradotto in russo con riferimenti espliciti all’inglese nelle altre sezioni. La guida integrata aggiornata ha superato i controlli di impaginazione e contrasto in entrambi i temi.
- Superati i controlli preliminari e quelli relativi alle pubblicazioni (259 file pubblici, 1.354 collegamenti locali); aggiornato Analisi dei file YAML di Compose e CI. Docker e la CI remota non sono stati eseguiti in questa fase.
- La versione ricostruita ha superato i test relativi all’installazione isolata, al caricamento dell’elenco dei pacchetti in bundle e alla verifica dell’esportazione firmata . Tutte le 69 risorse del pacchetto corrispondevano all’area di lavoro; sono stati verificati gli hash dei file sorgente.

Ricevute: `test-results/public-proxy-research/download-receipt.json`, `test-results/public-proxy-research/copy-receipt.json`, `test-results/public-proxies-full-suite.log`, `test-results/public-proxies-final-focused.log`, `test-results/public-proxies-browser/receipt.json` e `test-results/public-proxies-package.log`. Le impostazioni relative a browser, account e trasporto sono sintetiche; i due download dei feed sopra riportati sono richieste HTTPS reali.

## Presentazione delle funzionalità opzionali · 29 ottobre 2026

La precedente pagina dedicata al bot Proof è ora denominata **«Extras**»: una breve panoramica seguita da una pagina di configurazione separata per l’opzione selezionata. Il modulo di registrazione prevede tre passaggi, con la gestione della connessione, le opzioni di rete e i dettagli di implementazione nascosti. GitHub è esplicitamente previsto e non richiede l’inserimento di credenziali. [Panoramica in russo](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/EXTRAS.md).

- Superati 30 test mirati relativi alla localizzazione, alla configurazione di Witness e ai controlli di pubblicazione.
- Superati i test di accettazione della configurazione Chromium in inglese/russo, modalità chiara/scura, a 390/1440 pixel: focus sulla tastiera e tasto Invio, assenza di collegamenti impliciti durante la selezione delle opzioni aggiuntive, conservazione delle bozze, download delle configurazioni e dei token fissati, cancellazione dei token al blocco dello schermo e corretto funzionamento dei collegamenti alla guida locale. Superati i controlli di contrasto tra layout e testo su sfondo a tinta unita.
- Superato il test di accettazione del cambio di area di lavoro, compresa la risposta ritardata del token che arriva dopo il cambio. La navigazione rapida consente di individuare le sezioni aggiuntive tramite i termini relativi a bot, prove e GitHub; sono stati superati anche i controlli esistenti relativi alle risoluzioni 320/390/1440 pixel e ai formati russo/RTL.
- Durante l’esecuzione della configurazione non sono stati rilevati errori JavaScript né richieste esterne al browser. Si tratta di controlli sintetici dell’interfaccia utente, non di nuove prove relative a Telegram o alla pubblicazione di bot in tempo reale.
- Il caricamento definitivo delle lingue e la copertura del dizionario sono stati superati per tutte e 13 le impostazioni locali, mantenendo i fallback espliciti in inglese al di fuori del russo. Anche la guida Proof ampliata ha superato i controlli di layout e contrasto a 320/768/1440 pixel in entrambi i temi.
- La versione ricostruita ha superato i test di installazione isolata e di verifica dell’esportazione firmata. Tutte le 67 risorse incluse nel pacchetto corrispondevano all’area di lavoro; l’archivio sorgente contiene 253 file pubblici. Il controllo delle fonti e dei collegamenti ha dato esito positivo per 1.346 collegamenti alla documentazione locale.

Ricevute: `test-results/setup-browser/receipt.json`, `test-results/quick-navigation/receipt.json`, `test-results/extras-final.json`, `test-results/extras-package.log` e `test-results/extras-artifacts.json`. Le immagini di screenshot utilizzano spazi di lavoro sintetici.

## Verifica della configurazione del bot Witness e del proxy · 29 ottobre 2026

La configurazione di Witness (ora **in «Extras» → «Un bot nel vostro canale**») prepara un Witness distribuito in modo indipendente: chiave di raccolta fissata, download del token con ambito limitato, canale dedicato, politica di pubblicazione, percorso HTTP/SOCKS5 e API bot personalizzata. Il token del bot rimane sull’host del witness. Il suo nuovo `--check-config` convalida la configurazione e i file senza aprire una connessione di rete né creare una chiave. I percorsi dei file JSON vengono risolti accanto alla configurazione. Tutte le varianti del witness Compose ora inoltrano le impostazioni del proxy HTTP e dell’API del bot.

Le impostazioni dell’account supportano un catalogo MTProxy pubblico gestito dall’operatore, l’anteprima personalizzata dei link proxy di Telegram e i campi manuali esistenti. Le risposte del catalogo omettono le informazioni riservate; la selezione memorizza il percorso nel vault dell’area di lavoro. In caso di cataloghi mancanti o non validi, rimangono disponibili i percorsi manuali. Nessun indirizzo proxy di progetto né servizio di testimonianza ospitato vengono creati o abilitati per impostazione predefinita. Un esempio Caddy espone solo l’endpoint head con ambito limitato quando un testimone esterno deve raggiungere un collettore il cui pannello rimane privato.

Convalida:

- Suite completa: **348 test superati, 3 saltati**, 195,81 secondi. I limiti di Windows sono la causa dei test saltati; permangono i due avvisi relativi alla deprecazione delle dipendenze esistenti.
- Esecuzione finale dei test di regressione relativi a Witness/configurazione/rilascio: **11 superati, 1 saltato**. Ciò coincide con la suite completa. I test includono la risoluzione dei percorsi, il preflight offline, la firma/pubblicazione tramite un’effettiva fixture HTTP Bot API in loopback, il fallimento della consegna registrata, la verifica del token del canale e l’esclusione del segreto del proxy.
- Accettazione della configurazione di Chromium superata in inglese/russo a 390/1440 pixel: configurazione fissata e download dei token, cancellazione dei token alla chiusura, selezione del catalogo, anteprima dei link personalizzati seguita da salvataggio esplicito, layout/contrasto e assenza di errori JavaScript o richieste esterne al browser. Corretti il titolo troppo stretto dell’account in russo e l’overflow nella scheda di accesso.
- Ruff, verifiche delle fonti/dei link e analisi YAML di Compose/flusso di lavoro superate.
- La versione aggiornata ha superato i controlli relativi all’installazione isolata, ai pannelli/risorse statiche e all’autenticazione tramite API, oltre alla verifica indipendente delle esportazioni sintetiche dirette e in streaming di 32 eventi.

Ricevute: `test-results/setup-full-suite.log`, `setup-final-focused.log`, `setup-browser/receipt.json`, `setup-browser-final.log` e `setup-package.log`. Questi controlli utilizzano account sintetici/proxy e un’infrastruttura locale per l’API dei bot. Non presuppongono la pubblicazione di un bot reale, un server MTProxy pubblico funzionante, l’esecuzione remota di CI o l’implementazione su Docker. La cronologia delle osservazioni reali su Telegram sopra riportata rimane un elemento di prova separato. [Istruzioni di configurazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

## Revisione della presentazione e della documentazione · 29 ottobre 2026

La pagina del prodotto, la schermata di accesso, i file README in inglese e russo e le immagini di presentazione presentano ora uno stile visivo uniforme. Gli screenshot pubblici utilizzano dati dimostrativi fittizi. La revisione ha inoltre corretto le descrizioni obsolete relative alla convalida in tempo reale e al recupero riportate sopra.

- Localizzazione mirata, test del sito e delle pubblicazioni: **33 superati, 1 saltato**. Il test saltato richiede la creazione di un collegamento simbolico non disponibile su questo host.
- È stata approvata l’accettazione generale del pannello Chromium, inclusi tutti i cataloghi linguistici, il layout RTL, i temi chiaro/scuro, il contrasto solido del testo e il cambio di area di lavoro. Il controllo relativo alla creazione del profilo ora attende la risposta HTTP effettiva prima di verificare l’area di lavoro selezionata.
- Le schermate di accesso in inglese e russo hanno superato i controlli di layout e contrasto in entrambi i temi a 320, 390, 768, 850 e 1440 pixel; il pulsante di invio rimane all’interno del viewport iniziale.
- Conformità al sito pubblico verificata a 320, 390, 768, 1024 e 1440 pixel, inclusi i , ingrandimento degli screenshot/tasto Esc/ritorno al focus, tabulazioni da tastiera, rifiuto degli appunti, sottopercorsi del progetto, animazioni ridotte e modalità di ripiego senza JavaScript. Non sono state rilevate richieste di risorse non andate a buon fine, richieste esterne o errori JavaScript.
- La versione aggiornata ha superato un controllo di installazione isolata: le risorse del pannello e le impostazioni locali vengono caricate, l’accesso all’API richiede l’autenticazione e le esportazioni dirette/in streaming verificano in modo indipendente tutti i 32 eventi sintetici. I controlli Ruff e quelli relativi alle fonti pubbliche e ai link hanno dato esito positivo.

Ricevute locali: `test-results/design-tests.log`, `design-panel-final.log`, `design-review-final.log`, `design-site.log` e `design-package/install-receipt.json`. La suite completa del backend non è stata rieseguita in occasione di questa modifica alla presentazione/documentazione; il risultato precedente rimane nell’audit pre-pubblicazione.

## Versione 0.6.1

La versione 0.6.1 modifica la presentazione del pannello, i lanciatori, il pacchetto e la documentazione; il codice relativo alla raccolta, all’archiviazione, alla firma e all’esportazione rimane invariato. Su Windows 11 / Python 3.12.10 con il runtime fissato:

- La suite completa ha superato **137 test** con **2 salti** e l’avviso Starlette esistente. I nuovi test riguardano la gestione del comando Ctrl+C da parte del launcher (al server vengono concessi 30 secondi per un arresto ordinato) e gli errori risolvibili nelle fasi di configurazione.
- Chromium (shell headless 156) ha superato tutti **i 45 scenari generali** e **i 35 scenari relativi all’importazione di account, ai codici QR e alle chiavi di autenticazione**, compresi il controllo del contrasto del testo in tinta unita, l’assenza di overflow orizzontale a 320–1440 px e la visibilità dei campi di primo accesso a 320/390 px. Non sono stati rilevati errori JavaScript nella pagina né richieste esterne.
- `python start.py --setup-only` ha reinstallato il pacchetto nella versione 0.6.1 e `python start.py --check` ha segnalato di essere pronto. Un vero server `python -m tgwitness --demo` ha restituito il pannello, il foglio di stile, lo script, il logo, la guida e la versione `/api/status` 0.6.1; il server `workspace.css`, rimosso, ha restituito un errore 404.
- `Start.cmd` ha rilevato un’installazione di Python al di fuori del PATH. In assenza di Python disponibile, ha visualizzato la richiesta di installazione; dopo aver rifiutato le istruzioni manuali stampate, è uscito dal programma 1. La fase di download da python.org ha recuperato il programma di installazione 3.12.10, che ha superato il controllo Authenticode della Python Software Foundation; il programma di installazione stesso non è stato eseguito su questo host.
- `start.sh`, senza alcuna istruzione Python, ha visualizzato le indicazioni di installazione e si è chiuso. 1. `scripts\Docker.cmd` e `scripts/docker-start.sh` sono stati testati su eseguibili `docker` fasulli: sequenza di chiamata corretta, indirizzo del pannello e output del token corretti, e nessun messaggio di successo in caso di errore.
- `python tools/build_portable.py` ha creato un pacchetto Windows da 18,8 MiB dopo aver verificato il checksum del runtime incorporabile fissato. Una volta estratto in un percorso contenente spazi e avviato con solo le directory `C:\Windows` presenti nel PATH, il suo Python integrato ha superato il test `TgWitness-Check.cmd`, ha reso disponibile la demo (32 eventi) e uno spazio di lavoro in tempo reale, mentre Chromium ha visualizzato il registro e il pannello dei dettagli senza errori JavaScript. I dati sono stati scritti nella cartella `data` del pacchetto.
- `python tools/build_preview.py` ha prodotto un archivio sorgente composto da 110 file. Un’esecuzione di prova di `git add` ha elencato gli stessi 110 file, senza file di sessione, chiave, database, token, log o esportazione, senza percorsi assoluti locali e senza stringhe che potrebbero costituire informazioni riservate.

Non sono state eseguite in questa specifica sessione di pacchettizzazione del 27 ottobre: l’installazione automatica di Python stessa, i controlli di build/Compose di Docker, le esecuzioni su Linux/macOS né una nuova prova con account attivo . Le prove reali relative a Telegram sono registrate sopra e nei precedenti controlli degli account riportati di seguito. Le sole definizioni CI non sono sufficienti a qualificare l’esecuzione sulla piattaforma.

## Versione 0.6.0

L’ultima suite completa con runtime fissato su Windows 11 / Python 3.12.10 ha superato **135 test**, con **1 test saltato**, in 26,53 secondi e con l’avviso Starlette già presente. Il test saltato richiede i permessi POSIX. Dopo aver aggiunto il renderer QR ai controlli di prontezza e alle misurazioni dei processi, sono stati superati anche 8 controlli di prontezza/area di lavoro interessati.

La nuova copertura include gli schemi Telethon 7/8, gli schemi Pyrogram 2/3, JSON completo e JSON contenenti solo metadati, file di account corrispondenti o in conflitto, codici di accesso TData, manomissione dei checksum e percorsi non sicuri, conversione offline/autenticata in memoria, verifiche online dell’ID account, esito QR/2FA/scadenza, cancellazione per obsolescenza e isolamento dell’account. I fixture TData utilizzano un’implementazione AES-IGE separata per la crittografia.

Chromium ha superato **45 scenari generali** e **35 scenari relativi all’importazione di account, codici QR e chiavi di autenticazione**, senza che siano stati rilevati errori JavaScript nelle pagine né richieste esterne. I nuovi controlli del browser coprono tutti e quattro i formati di input, TData protetto, metadati API, rendering dei codici QR, scadenza/riprova, autenticazione a due fattori (2FA), rifiuto in caso di account errato, blocco/annullamento dell’area di lavoro, layout responsivo e risposte di conversione in ritardo a seguito della selezione di un file più recente.

Entrambe le suite di browser hanno superato nuovamente i test dopo le modifiche apportate alla pagina di accesso all’account. La configurazione in tempo reale apre il modulo di accesso all’account; la modalità demo apre il registro di esempio. La pagina “Account” della demo mostra le istruzioni di avvio in tempo reale e nasconde i campi di inserimento delle credenziali. Controlli mirati a 320, 390 e 1440 pixel hanno confermato che il campo numerico e il pulsante principale rientrano senza scorrimento, che i campi API sono inizialmente nascosti e che il contrasto del testo rimane leggibile. I controlli di acquisizione e verifica rimangono nascosti dopo l’apertura delle loro nuove sezioni espandibili.

Il flusso diretto della chiave di autenticazione è stato testato con credenziali sintetiche attraverso i reali endpoint di importazione e autorizzazione. I controlli riguardano chiavi incomplete, DC mancante, ID utente imprecisi, identità dell’account non corrispondente, credenziali API salvate, stato visibile dell’avanzamento della richiesta, cancellazione delle chiavi segrete e risposte in ritardo a seguito di modifiche o cambiamenti di metodo. Tutti e quattro i metodi di accesso sono stati verificati a 320, 390 e 1440 pixel. Il selettore di file precede le indicazioni sul formato e il pulsante «Connetti» si adatta al viewport iniziale di 844 pixel con le impostazioni API nascoste. In questa sessione di verifica dell’interfaccia utente non è stata tentata alcuna autorizzazione con chiave di autenticazione reale.

L’aggiornamento del pannello è stato nuovamente verificato con entrambe le suite di browser: non sono stati rilevati errori JavaScript nella pagina né richieste esterne. La suite di account ora prevede l’inserimento di una coppia ID API/hash, il rifiuto di coppie non valide o multiple senza sostituzione dei campi, indicazioni relative esclusivamente ai metadati e l’ignoramento delle risposte di importazione non aggiornate a seguito di un cambiamento del metodo di accesso o della modifica manuale delle credenziali. Sono stati superati sei ulteriori controlli mirati relativi alla guida di configurazione, all’avvio/pausa espliciti, al recupero in caso di ricerca vuota e al layout finale della connessione/guida locale, nonché al contrasto solido del testo a 320, 390 e 1440 pixel. L’aggiornamento relativo all’accesso diretto aggiunge un’unica operazione di richiesta tramite numero di telefono/codice e riutilizza la coppia API salvata nell’area di lavoro corrente per l’accesso tramite numero di telefono, codice QR e sessione. La suite completa in Python sopra indicata include nuovi test di persistenza, di rifiuto delle credenziali parziali e di isolamento dell’area di lavoro. I controlli del browser riguardano l’inserimento diretto del numero di telefono, il riutilizzo delle credenziali salvate, l’instradamento basato esclusivamente sui metadati, l’autorizzazione dei file con un solo pulsante e il rifiuto degli account duplicati. Sono stati inoltre verificati i moduli semplificati per token del pannello e numero di telefono senza scorrimento iniziale a 320, 390 e 1440 pixel. Un controllo di compatibilità ha confermato che il modulo diretto per il numero di telefono può utilizzare gli endpoint di configurazione/codice precedenti mentre è ancora in esecuzione un processo precedente.

Un account fornito dall’utente è stato verificato separatamente, al di fuori dei test pubblici. I suoi input Telethon, Pyrogram e TData hanno restituito la stessa autorizzazione; il file JSON allegato forniva le credenziali API. Tutti e quattro i file sono stati caricati tramite il pannello 0.6.0 e Telegram ha confermato l’ID numerico dell’account previsto. I file sorgente sono rimasti invariati. Non sono state selezionate fonti e la funzione di osservazione è rimasta disattivata. Ciò costituisce un esempio di importazione/accesso, non di raccolta, recupero o capacità in tempo reale.

Telegram ha inoltre emesso un vero token QR, che è stato annullato senza essere stato scansionato. L’ intero flusso di conferma tramite QR e di autenticazione a due fattori (2FA) è stato testato con client sintetici; la conferma su dispositivo mobile tramite una vera app Telegram rimane una fase di accettazione separata. Nei file pubblici non sono inclusi identificativi reali degli account, dati riservati o screenshot.

L’aggiornamento del launcher è stato completato; il codice sorgente, i metadati installati e l’indicatore di prontezza riportano la versione 0.6.0, con codice QR 8.2 e `pip check` superato. Il wheel installato ha fornito il pannello e la guida, ha respinto le richieste API non autenticate e ha verificato in modo indipendente le esportazioni sintetiche dirette e in streaming di 32 eventi. La guida offline aggiornata è stata verificata a 320, 390 e 1440 pixel. Gli screenshot pubblici rimangono sintetici.

Il rilascio del codice sorgente contiene 107 file inseriti nella lista delle eccezioni. I collegamenti alla documentazione locale sono funzionanti. L’esecuzione su Docker/Caddy, la pubblicazione remota tramite CI/pacchetti, il runtime ARM64, la raccolta continuativa e la matrice completa di compatibilità con Telegram in tempo reale non sono qui descritti in modo esaustivo.

## Versione 0.5.1

Su Windows 11 / Python 3.12.10, la suite completa dell’ambiente di progetto ha superato i test: **94 superati, 2 saltati**, in 31,21 secondi, con l’avviso Starlette esistente. Le operazioni saltate richiedono permessi POSIX e la creazione di collegamenti simbolici non disponibili su questo host. Il fixture HTTP di download ha visualizzato una diagnostica del thread di richiesta; tutte le asserzioni sono state superate. Questa esecuzione non garantisce l’assenza di problemi di trasporto a livello di host.

Le nuove operazioni di copertura dei test di regressione hanno preso in esame StringSession, le modifiche al codice e all’account 2FA, la ricerca di identità annullata, l’annullamento dell’accesso in sospeso e gli aggiornamenti tramite handler registrati su client attivi, rifiutati, sostituiti e di prova. Solo il collettore attivo contribuisce con gli eventi; le credenziali salvate e la cronologia firmata rimangono intatte. Altri nuovi controlli riguardano la ricerca Unicode dopo la riapertura di un database, l’inclusione dei limiti delle politiche di monitoraggio in Coverage e le esclusioni relative ai pacchetti di origine pubblica.

Il progetto effettivo `pythonw.exe` ha avviato un pannello sintetico isolato, ha restituito un codice di stato HTTP 200 e ha conservato la diagnostica di avvio in `logs/server.log`. Il registro non conteneva né il token del pannello generato né i record di accesso HTTP. Il test ha terminato solo il proprio processo sintetico. Non è stata registrata alcuna attività nell’Utility di pianificazione; l’accesso/la disconnessione, la modalità di sospensione e il ripristino del servizio rimangono requisiti distinti.

I test di accettazione su Chromium hanno superato **45 scenari**, senza errori JavaScript nelle pagine e senza che siano state rilevate richieste esterne. I nuovi controlli riguardano le date e gli orari della timeline a 601/768/850 pixel, le bozze degli allegati durante l’aggiornamento dello stato, le modifiche più recenti apportate durante il salvataggio, i risultati di verifica azzerati al cambio di account, le risposte di verifica in ritardo dopo il passaggio a un’altra pagina e il ritorno, nonché i limiti di verifica espliciti all’arrivo di nuovi eventi. È stata inoltre corretta la spaziatura tra l’icona di ricerca e il testo ed è stata rieseguita la suite di browser.

L’esecuzione del browser ha utilizzato il runtime fissato in `.venv` e il Playwright 1.62.0/Chromium fornito dal sistema, aggiunto dopo l’ambiente di progetto nel percorso di importazione. L’installazione facoltativa di una dipendenza di sviluppo è stata interrotta a causa di un download lento di Playwright; non è stata qualificata alcuna nuova versione dello strumento per browser. Un normale `python start.py --setup-only` ha completato l’aggiornamento dell’applicazione. Il codice sorgente, i metadati installati e il marker del launcher riportano la versione 0.5.1; `pip check` ha superato il test. I controlli di prontezza sono stati superati su un percorso nuovo e non utilizzato, mantenendo l’avviso previsto relativo alla chiave del vault locale.

Il pacchetto wheel 0.5.1 è stato installato separatamente e sottoposto a test di funzionamento: tutte le risorse relative ai pannelli e alle guide sono state fornite, l’accesso alle API senza autenticazione è stato rifiutato e sia i file ZIP contenenti prove dirette che quelli in streaming relativi a 32 eventi hanno superato la verifica indipendente. I file dell’applicazione contenuti nel pacchetto installato sono stati confrontati con il codice sorgente. L’archivio pubblico del codice sorgente utilizza un elenco esplicito di tipi di file consentiti e rifiuta i file sorgente collegati; il materiale di runtime inserito all’interno delle directory del codice sorgente viene escluso dai test di regressione.

Durante l’esecuzione della correzione del codice, la selezione del codice pubblico e l’insieme dei candidati Git contenevano 86 file, senza includere le directory dei dati di runtime. Una scansione alla ricerca di modelli riconoscibili di chiavi private, token GitHub, token dei bot di Telegram e StringSession non ha rilevato alcuna corrispondenza. Si tratta di una verifica limitata dei modelli, non di un audit completo delle informazioni riservate. Le verifiche delle regole di esclusione coprono dodici artefatti comuni relativi ad account, dati ed esportazioni. I file YAML relativi a Workflow, Issue e Compose, nonché lo script di attività di Windows, sono stati analizzati con esito positivo. I collegamenti alla documentazione locale sono risolvibili.

Vengono affrontati tutti e sette i risultati emersi dalla revisione del 27 ottobre. L’esecuzione del flusso di lavoro su GitHub, il runtime su Linux/macOS/Docker, l’interoperabilità con Telegram reale, proxy esterni e TSA, nonché la qualificazione sotto carico prolungato rimangono al di fuori di questa esecuzione locale. Non è stata effettuata alcuna pubblicazione su repository, registrazione di servizi o raccolta di account reali. Non è stata effettuata alcuna pubblicazione su repository, registrazione di servizi o raccolta di account reali.

### Aggiornamento della documentazione in inglese

Il file README, la guida di riferimento per account e sessioni, il flusso di lavoro di raccolta e la guida integrata ora descrivono gli input supportati, il comportamento dell’area di lavoro, le politiche relative agli eventi e i formati di esportazione in lingua inglese. Le tre schermate pubbliche sono state aggiornate utilizzando dati sintetici. A quel punto, la selezione di sorgenti pubbliche conteneva 88 file, comprese le due nuove guide. Tutti i 131 collegamenti locali presenti nei 23 documenti Markdown sono funzionanti.

A seguito delle modifiche apportate all’interfaccia e alla guida, i test di accettazione su Chromium hanno nuovamente superato tutti i 45 scenari, senza che siano stati rilevati errori JavaScript nelle pagine né richieste esterne. La suite completa di test Python non è stata rieseguita per questo aggiornamento della documentazione e della presentazione; il risultato di 94 test superati riportato sopra si riferisce alla precedente esecuzione dedicata alla correzione del codice.

La versione ricostruita è stata installata su un nuovo target isolato. I suoi componenti relativi a pannelli e guide hanno funzionato correttamente, l’accesso API non autenticato è stato respinto ed entrambe le esportazioni, sia dirette che in streaming, hanno superato la verifica indipendente su 32 eventi sintetici.

### Aggiornamento sull’installazione e l’implementazione

I controlli mirati relativi all’installatore, al pacchetto e alla prontezza all’uso hanno superato **14 test**, con un solo salto dovuto alla mancata disponibilità della creazione di un collegamento simbolico. I controlli del wrapper nativo coprono i percorsi contenenti spazi, l’inoltro degli argomenti, le modalità di configurazione/dimostrazione e la propagazione di un codice di uscita diverso da zero. I controlli di Git Bash verificano il funzionamento dell’helper della shell di Docker con un demone simulato, includendo casi quali assenza di Docker, assenza di Compose, attesa di integrità fallita e avvio riuscito su porta alternativa. Tali controlli simulati non stabiliscono la compatibilità del runtime di Docker.

Una copia completa proveniente da fonti pubbliche è stata installata in una nuova directory di Windows il cui percorso contiene spazi. `scripts\Setup.cmd` ha creato un nuovo ambiente e ha installato il runtime aggiunto ai preferiti; `Start.cmd --check --json` ha segnalato di essere pronto senza aver creato la propria directory di destinazione dei dati. `pip check` ha superato il test. Anche la versione ricostruita ha superato il controllo del pacchetto installato, comprese le esportazioni dirette e in streaming di 32 eventi.

Sintassi Shell e cinque file YAML relativi al flusso di lavoro e a Compose analizzati. Le configurazioni di Compose relative al codice sorgente e alle immagini concordano sulle impostazioni di archiviazione e di esecuzione. In quella fase, tutti i 139 collegamenti locali presenti in 23 documenti Markdown sono stati risolti. La selezione di origine pubblica contiene 99 file.

Le definizioni CI ora eseguono una nuova configurazione nativa su Windows/Linux/macOS, verificano lo stato di integrità, il controllo degli accessi e la persistenza di Compose durante la ricreazione dei container, nonché la configurazione di Caddy. Il flusso di lavoro di rilascio subordina la pubblicazione al superamento di tali controlli e aggiunge un test preliminare emulato su ARM64. Docker non è disponibile su questo host: l’esecuzione effettiva di Compose/Caddy, l’emissione dei certificati, l’esecuzione su ARM64 e la pubblicazione remota del flusso di lavoro/pacchetto rimangono senza riserve a livello locale. Il codice dell’applicazione e dell’interfaccia utente non è stato modificato da questo aggiornamento; i precedenti risultati completi relativi a Python e al browser non sono stati rieseguiti.

## Versione 0.5.0

La suite completa di test in runtime con impostazioni fisse ha superato i test: **81 superati, 1 saltato**, in 22,00 secondi, con l’avviso Starlette già presente. Il controllo dei permessi POSIX viene saltato su Windows. I nuovi test dell’handler inviano messaggi, modifiche, cancellazioni con o senza ambito, reazioni, aggiornamenti dei partecipanti e messaggi del servizio di appartenenza attraverso diverse politiche. Le categorie disabilitate non producono osservazioni in tempo reale corrispondenti; la diagnostica della copertura e le istantanee esplicite rimangono disponibili. I test verificano la persistenza della politica, la separazione degli spazi di lavoro, i record di audit firmati prima e dopo, il comportamento in caso di politica invariata, la convalida rigorosa e l’inclusione nella successiva ricevuta di processo.

I test di accesso alla versione demo verificano che le sue funzionalità differiscano da quelle del token del pannello configurato, che non sia in grado di autorizzare uno spazio di lavoro attivo, che non possa modificare le impostazioni di raccolta e che non sia emesso né accettato per richieste remote, inoltrate, cross-origin o con host non valido. L’apertura di una demo memorizzata senza l’esplicito flag «demo» non abilita l’accesso automatico.

I test di accettazione su Chromium hanno superato **39 scenari**, tra cui l’accesso alla demo locale senza inserimento del token, le impostazioni predefinite di monitoraggio, il passaggio dalla selezione della fonte alla politica, l’indipendenza per account e i controlli sul layout desktop/320/390 pixel e sul contrasto del testo. Non sono stati rilevati errori JavaScript nelle pagine. Le richieste dell’host in cui è stato inserito AdGuard rimangono nel registro. Il fixture HTTP di download ha registrato un ripristino della connessione dopo che un client ha chiuso la propria connessione; le asserzioni sono comunque state superate. Questo non è un risultato relativo al servizio attivo.

Il launcher standard ha aggiornato l’ambiente isolato alla versione 0.5.0; le versioni sorgente e installata corrispondono e il controllo pip è stato superato. I controlli relativi alla crittografia del caveau segreto esistente, al rifiuto in caso di chiave errata o mancante e alla manomissione delle firme e dei file multimediali sono stati superati nella suite completa. Non viene dichiarata alcuna nuova crittografia applicativa del contenuto dei messaggi o degli allegati.

La demo locale viene riavviata per rendere disponibile l’interfaccia utente aggiornata. I record sintetici esistenti vengono conservati; l’interruzione del vecchio processo di demo in background crea un limite offline al successivo avvio. Per questi controlli non viene utilizzata alcuna sessione Telegram reale.

Il pannello in esecuzione su localhost:8787 riportava la versione 0.5.0, l’accesso automatico alla demo, i cinque controlli di monitoraggio e 33 eventi sintetici conservati nel registro. Il pacchetto «wheel» 0.5.0 installato separatamente ha fornito tutte le risorse del pannello e della guida, ha rifiutato l’accesso API non autenticato e ha generato un file ZIP verificato contenente 32 eventi, sia direttamente che tramite l’utilità di download in streaming. Le versioni dei pacchetti di runtime rimangono bloccate su quelle registrate per la versione 0.4.

## Versione 0.4.0

La suite completa di test in runtime con impostazioni fisse è stata superata: **78 test superati, 1 saltato**, in 19,77 secondi. Il controllo saltato richiede i permessi POSIX; permane l’avviso di deprecazione relativo a Starlette TestClient a monte. I nuovi test riguardano il download in streaming e l’instradamento nell’area di lavoro, le intestazioni di autorizzazione, il rifiuto di sovrascrittura, i reindirizzamenti, le risposte troncate, i limiti di dimensione dichiarati ed effettivi, le letture limitate, la pulizia, i file system senza collegamenti fisici, gli errori di prontezza e le modalità di avvio che non devono installare pacchetti. I test di esportazione confermano la presenza di file temporanei locali nell’area di lavoro e la pulizia selettiva dei file orfani.

I test di accettazione su Chromium hanno superato tutti i 36 scenari elencati senza errori JavaScript nelle pagine. Vengono simulati accessi tramite telefono/codice/autenticazione a due fattori (2FA), sessioni convertite, due aree di lavoro e percorsi/stati separati, osservazioni, firme, punti di controllo e richieste di timestamp, oltre a:

- Layout per desktop e da 320/390 pixel, nessun traboccamento orizzontale, navigazione visibile, e il campo di primo accesso all’interno dei primi 844 pixel del viewport.
- Contrasto del testo su sfondo a tinta unita conforme alle soglie WCAG AA. Sono esclusi i controlli disabilitati, l’opacità e gli sfondi con immagini o sfumature; non si tratta di una verifica completa delle WCAG.
- Una risposta di esportazione locale reale generata tramite un simulatore di selezione file/scrittura del sistema operativo, seguita da una verifica ZIP indipendente; l’annullamento non invia alcuna richiesta di esportazione.
- Un errore di scrittura interrompe l’operazione di destinazione; il fallback da 128 MiB rifiuta una risposta pubblicizzata di dimensioni eccessive senza allocare un payload corrispondente.
- La guida locale in inglese per desktop e per entrambe le larghezze ridotte.

La finestra di dialogo di salvataggio del sistema operativo e le effettive operazioni di scrittura sul browser, dell’ordine di diversi gigabyte, non sono state automatizzate né convalidate. I test di download in Python utilizzano blocchi limitati e dispositivi di loopback. L’accettazione completa dell’implementazione con Telegram reale rimane una questione a parte.

Il programma di installazione standard ha aggiornato `.venv` alla versione 0.4.0. I metadati del codice sorgente e quelli dell’installazione coincidono; `pip check` ha superato il test. `python start.py --check --json` ha segnalato di essere pronto su un nuovo percorso sintetico senza creare la directory dei dati. L’avviso relativo all’archiviazione delle chiavi locali rimane correttamente visualizzato: i registri e i file multimediali non sono crittografati dall’applicazione.

Il pacchetto wheel 0.4.0 è stato compilato e installato in una directory separata. Tutti i 23 file dell’applicazione corrispondono al codice sorgente byte per byte. Il pacchetto installato ha fornito il pannello di controllo e le guide/risorse in inglese, ha respinto gli accessi all’API non autenticati e ha esportato un file ZIP sintetico contenente 32 eventi che ha superato la verifica. Il suo comando di download in streaming ha inoltre recuperato un file ZIP verificato in modo indipendente dall’applicazione installata e in esecuzione.

La documentazione pubblica e la guida locale sono in inglese; i collegamenti alla documentazione locale funzionano correttamente. PowerShell ha analizzato il modello di attività di Windows e Python ha analizzato il file plist di macOS. Si tratta di controlli sintattici, non dell’esecuzione del servizio. Nessuna attività/servizio è stato registrato. La configurazione CI ora include controlli di prontezza, ma la CI remota non è stata eseguita in questa sede.

L’esecuzione del browser nella versione 0.4 ha rilevato nuovamente l’iniezione da parte di AdGuard e l’errore OSError 10022 relativo alla pulizia dei socket asyncio di Windows. Le verifiche del browser sono state superate; tali osservazioni ambientali vengono conservate anziché essere considerate come un comportamento fisso dell’applicazione. I tentativi iniziali di esecuzione in sandbox di OpenSSL/browser/pip sono falliti; le esecuzioni di qualificazione andate a buon fine hanno utilizzato un’esecuzione approvata al di fuori della sandbox.

## Versione 0.3.1: correzioni volte a garantire la piena operatività

I controlli relativi al launcher, all’archiviazione delle prove e all’API hanno dato esito positivo: **31 superati, 1 saltato**, un avviso Starlette a monte. Il controllo saltato verifica i permessi delle directory POSIX e non è in grado di stabilire tali permessi su questo host Windows. Il test con Python legacy simula il confine tra versione e importazione; nessun interprete Python 3.10 è stato installato o qualificato. La suite 0.3, precedentemente superata, è riportata di seguito; l’intera suite e gli scenari relativi al browser non sono stati rieseguiti per queste modifiche mirate.

Il launcher standard ha aggiornato l’ambiente locale alla versione 0.3.1; i metadati del codice sorgente e di quelli installati concordano e il controllo pip è stato superato. Una wheel 0.3.1 installata separatamente ha fornito il pannello e le risorse, ha rifiutato l’accesso non autenticato all’API e ha prodotto un’esportazione sintetica verificata di 32 eventi. Il file YAML del flusso di lavoro è stato analizzato, ma il nuovo controllo del runtime del container non è stato eseguito: non era disponibile alcun runtime locale utilizzabile (Docker/Podman/Linux).

Si prega di consultare [i risultati della valutazione di idoneità](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) per individuare eventuali lacune residue in materia di usabilità, funzionamento in produzione e piattaforma. Questa patch non garantisce la compatibilità con ulteriori sistemi operativi.

## Versione 0.3.0

La suite completa di test in runtime con pinning ha superato **61 test**, con un unico avviso di deprecazione relativo a Starlette TestClient a monte. I metadati di runtime riportano TgWitness 0.3.0 e python-socks 2.8.2; il controllo pip è stato superato. La verifica di compatibilità con il browser è stata superata senza errori JavaScript nella pagina.

Il wheel 0.3.0 è stato compilato e installato in una directory separata dedicata ai pacchetti. Esso ha fornito il pannello di controllo e le risorse, ha respinto una richiesta API non autenticata e ha esportato un registro sintetico di 32 eventi che ha superato una verifica indipendente. I collegamenti alla documentazione locale funzionano correttamente. Dopo la correzione della normalizzazione delle chiavi nude da parte di MTProxy, tutti e nove i test di connessione e sicurezza sono stati rieseguiti con esito positivo.

Le nuove funzionalità includono:

- Nome utente/password SOCKS5 e HTTP CONNECT tramite server di test loopback effettivi; un proxy configurato non funzionante restituisce un errore anziché ricorrere alla destinazione.
- Convalida del proxy, selezione del trasporto MTProxy, rifiuto dei segreti TLS ee falsi, persistenza, isolamento dell’area di lavoro, rifiuto delle modifiche durante l’osservazione ed esclusione dei segreti dallo stato dell’API e dagli eventi firmati.
- Conversione in sola lettura degli schemi SQLite sintetici 7 e 8 di Telethon; hash del codice sorgente invariato; rifiuto di altri formati, delle viste SQL e di un file WAL in sospeso.
- Chiave master esterna del vault: diverse chiavi derivate per gli spazi di lavoro, riapertura riuscita, rifiuto in caso di chiave errata o mancante e nessuna migrazione implicita dei vault locali esistenti.
- Impostazioni del proxy del browser, cancellazione delle credenziali, informativa sulla protezione dell’archivio, pagina dedicata alla connessione mobile, autorizzazione dei file di sessione convertiti, percorsi separati, e tutti gli scenari di raccolta/esportazione precedentemente trattati con un client Telegram fittizio.

Durante lo sviluppo, un test di loopback ha atteso indefinitamente lo spegnimento del peer; in un’altra esecuzione è stato osservato un reset della connessione Windows dopo l’handshake. Il fixture ora delimita l’intero scambio e considera l’EOF/reset dopo un handshake completato come chiusura della connessione. Le asserzioni relative all’handshake e all’autenticazione rimangono necessarie. Ciò non esclude i veri provider di proxy né implica un difetto fisso nel trasporto di Telegram.

Rimane valida l’osservazione relativa alla richiesta di AdGuard descritta di seguito. Non è stato utilizzato alcun account Telegram reale, né proxy SOCKS/HTTP esterno, né server MTProxy attivo. MTProxy è in fase sperimentale e sono state verificate le opzioni selezionate e la convalida dei segreti, ma non l’interoperabilità in tempo reale. I nuovi comandi relativi alla chiave esterna e alla conversione delle sessioni sono stati testati esclusivamente con segreti sintetici. Linux/macOS/Docker rimangono qui non qualificati.

La misurazione della velocità di trasmissione della versione 0.2 riportata di seguito non è stata ripetuta e non deve essere presentata come un nuovo benchmark multi-account/proxy per la versione 0.3.

## Versione 0.2.0 di riferimento

Testato su Windows con Python 3.12.10. Non è stato collegato alcun account Telegram reale.

| Verifica | Risultato |
| --- | --- |
| Suite Python | 52 test superati nell’ambiente di sviluppo e 52 superati con il runtime fissato; un avviso di deprecazione di Starlette TestClient a monte in ciascuna esecuzione |
| Sintassi JavaScript | Realizzato con Node.js |
| Accettazione da parte di Chromium | Superato; nessun errore JavaScript nella pagina |
| Layout per desktop/dispositivi mobili | Verificato alle risoluzioni 1440 × 1060 e 390 × 844; nessun traboccamento orizzontale del documento |
| Contenuto del messaggio in formato HTML | Visualizzato come testo; lo script inserito non è stato eseguito |
| Esempio di flusso dell’account | Credenziali API → telefono → codice → 2FA → selezionare il gruppo → avviare → istantanea → mettere in pausa → ricaricare |
| Prove nel browser | Confronto delle modifiche, contenuto precedente alla cancellazione, filtri, download in formato ZIP, checkpoint, ricevuta firmata della procedura, download della richiesta secondo lo standard RFC 3161 e associazione al checkpoint |
| Gestione di più account | Registri, chiavi, fonti e stati in tempo reale separati; il cambio di browser lascia in esecuzione l’altro collettore; gli spazi di lavoro si riaprono dopo il riavvio; gli account duplicati e la riassegnazione degli account vengono rifiutati |
| Errori crittografici | Campi firmati modificati, campi non firmati aggiunti, chiave errata, elemento dell’archivio danneggiato, file multimediali modificati o mancanti, troncamento rilevato dal checkpoint e rifiutato |
| Archiviazione | Le aggiunte simultanee vengono verificate; gli aggiornamenti o le cancellazioni innescano un rifiuto; all’avvio, il sistema rifiuta un registro modificato senza aver effettuato l’aggiunta e sblocca il blocco |
| Durabilità dei supporti | Scritture atomiche di messaggi/operazioni; ripristino in caso di riavvio; mantenimento dei descrittori della versione originale; sostituzione della coda e rifiuto della corruzione dei file esistenti; persistenza di FloodWait; isolamento degli errori alla fonte |
| Streaming | Il prefisso stabile viene esportato mentre vengono aggiunti nuovi record; il checkpoint conservato rileva eventuali registri troncati; l’esportazione non riproduce l’intero flusso di eventi |
| RFC 3161 | OpenSSL 3.5.9 legge le richieste generate; vengono accettate le risposte CA/TSA sintetiche generate localmente; vengono rifiutati i dati alterati, i nonce e le CA errate; l’ambiente CA circostante non prevale sulla fiducia esplicita |
| Configurazione locale | start.py --setup-only ha aggiornato l’ambiente .venv isolato alla versione 0.2.0; i metadati del codice sorgente e quelli installati corrispondono; il controllo pip è stato superato |
| Wheel | Versione 0.2.0 compilata e installata separatamente nella cartella «test-results»; ha fornito panel/risorse, ha respinto le richieste API non autenticate, ha esportato e verificato un archivio sintetico contenente 32 eventi |

I test sul codice sorgente hanno utilizzato FastAPI 0.159.1, Uvicorn 0.54.0, Telethon 1.45.0, cryptography 50.0.2, pytest 9.1.1 e Playwright 1.62.0. L’ambiente di esecuzione fissato utilizza FastAPI 0.162.0, Starlette 1.10.0, Uvicorn 0.54.0, Telethon 1.45.0 e cryptography 50.0.2. Il file deploy/constraints.txt registra le versioni fisse del runtime; i file deploy/requirements.lock e deploy/build.lock aggiungono l’SHA-256 di ogni file del pacchetto, e i server Docker e ad alta sicurezza effettuano l’installazione esclusivamente a partire da essi (pip --require-hashes). Nessuna delle due costituisce prova di compatibilità su tutte le piattaforme CI configurate. La CI remota non è stata eseguita.

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

## Osservazioni ambientali

Le restrizioni della sandbox di Windows hanno bloccato le directory temporanee predefinite di pytest/pip e il sottoprocesso di Playwright. Pytest ha utilizzato una nuova directory temporanea all’interno del progetto; i processi di installazione e del browser hanno richiesto l’esecuzione autorizzata al di fuori della sandbox.

Il sistema AdGuard ha inserito nel browser delle richieste dirette a local.adguard.org. La cronologia del browser conserva tali richieste. Questa sessione **non** costituisce prova dell’assenza di richieste in uscita in un ambiente browser non modificato; il codice sorgente dell’app stessa non contiene richieste esterne relative a risorse, CDN o strumenti di analisi. Le impostazioni di AdGuard non sono state modificate.

L’esecuzione finale del browser ha inoltre registrato un errore OSError 10022 relativo alla pulizia dei socket asyncio di Windows. Tutte le verifiche del browser sono state superate e non si sono verificati errori JavaScript nelle pagine. La causa non è stata accertata e questa esecuzione non dimostra l’assenza di problemi di trasporto da parte dell’host.

La prima prova HTTP del pacchetto installato, che utilizzava le richieste di chiusura della connessione di urllib, ha riscontrato il ripristino della connessione, sia all’interno che all’esterno della sandbox e con entrambi i set di dipendenze. La prova finale ha utilizzato connessioni persistenti HTTP/1.1 standard tramite http.client ed è risultata superata. Anche le richieste del browser hanno superato il test. L’origine precisa dei ripristini non è stata stabilita; essi non sono stati classificati come un difetto fisso dell’applicazione.

## Ulteriori precisazioni

Il registro in tempo reale conservato attesta l’effettiva raccolta, le modifiche, le notifiche di cancellazione, gli allegati, le verifiche successive e la gestione dei limiti di frequenza. Non documenta in modo esaustivo la consegna né fornisce una matrice controllata di visibilità dei ruoli, soggetti coinvolti, FloodWait prolungato, sospensioni degli account e ripristino in caso di interruzione della rete o dei processi. L’emissione del token QR rimane distinta dalla conferma tramite codice QR mobile completata.

La compilazione/esecuzione con Docker, l’installazione su Linux/macOS, la gestione di carichi elevati prolungati, la revisione indipendente della sicurezza, una risposta TSA realmente indipendente, la convalida della revoca/archiviazione dei certificati e la certificazione forense rimangono al di fuori della qualifica registrata. Sono implementati lo stato salvato di MTProto e il catch-up; il replay atomico durevole rimane non stabilito. La raccolta dei log di amministrazione, gli elenchi aggiuntivi dei reattori e il polling breve prioritario rimangono funzionalità separate. Si veda [l’accettazione in tempo reale](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) per la matrice di qualificazione controllata.

Le ricevute locali dettagliate e gli screenshot si trovano nella cartella test-results/ (ignorata da Git). Gli screenshot pubblici presenti in docs/assets/ contengono esclusivamente dati dimostrativi fittizi.

## Preparazione del sito web pubblico e della pubblicazione · 27 ottobre 2026

La presentazione separata «`website/`» e la build Pages sono state aggiunte dopo i controlli del panel sopra indicati. Non è stata modificata alcuna configurazione dell’account attivo né alcuna logica di raccolta.

- La suite di applicazioni esistente ha superato i test: 138 superati, 1 saltato (solo POSIX) e un avviso di deprecazione a monte relativo a Starlette/httpx. Gli 11 test di compilazione del sito aggiunti sono stati superati indipendentemente, compresi quelli relativi al rifiuto di output inattesi e al rifiuto di input collegati.
- Entrambi gli script del browser dell’applicazione hanno superato i test utilizzando project-venv Playwright e Chromium headless shell 156. Non sono stati registrati errori JavaScript nelle pagine né richieste esterne. Tutti gli scenari relativi agli account hanno utilizzato un trasporto fittizio e dati di fantasia.
- `tools/check_site.py` ha superato i test con larghezze di 320, 390, 768, 1024 e 1440, con un sottoperCORSO dell’URL del progetto, tab della tastiera, accesso agli appunti concesso/negato, movimento ridotto e JavaScript disabilitato. Non si sono verificati errori nelle richieste di risorse né nelle richieste esterne.
- `tools/build_site.py` ha generato 10 file pubblici inseriti nell’elenco delle eccezioni, per un totale di circa 460 KB. Gli screenshot del browser e una ricevuta si trovano nel file `test-results/site/`, che viene ignorato.
- Il file wheel è stato creato con successo dopo l’installazione degli strumenti setuptools/wheel dedicati esclusivamente alla compilazione nell’ambiente di progetto. L’installazione in un ambiente di destinazione isolato e l’esecuzione di `tools/check_install.py` hanno dato esito positivo: risorse statiche, controllo degli accessi, un’esportazione sintetica firmata di 32 eventi e download in streaming verificato in modo indipendente.
- `pip check` ha superato il test. Una scansione dei modelli dei candidati pubblici selezionati da Git non ha rilevato blocchi di chiavi private riconoscibili, token GitHub/bot/AWS, assegnazioni di segreti letterali di lunga durata o indicatori di conflitto di unione. Ciò non costituisce una prova dell’assenza di ogni possibile formato segreto. Le sondature relative a dati di runtime, sessioni e chiavi sono state ignorate da Git.
- L’autenticazione della CLI di GitHub non era valida; non era stato configurato alcun remote e non esisteva alcun commit iniziale. Non sono state eseguite operazioni di push, flussi di lavoro ospitati, distribuzioni su Pages né rilasci. Docker e la verifica in tempo reale di Telegram/piattaforma rimangono al di fuori di questa verifica.

Su questo host, il blocco del download di Playwright non è andato a buon fine sul filesystem dell’area di lavoro E:. L’installazione di Chromium sotto `%LOCALAPPDATA%/tgwitness-playwright` e l’utilizzo dello stesso `PLAYWRIGHT_BROWSERS_PATH` per i controlli hanno avuto esito positivo. Si tratta di una soluzione alternativa a livello di ambiente, non di una modifica alle dipendenze di runtime dell’applicazione.

## Documentazione interattiva e metadati del sito web · 29 ottobre 2026

Il sito pubblico è costituito da 12 pagine HTML in lingua inglese: una pagina iniziale, un indice delle guide e dieci guide. L’artefatto contiene 28 file di presentazione esplicitamente elencati, per un totale di circa 1,85 MB, e nessun dato di raccolta. Il sito web pubblico è in lingua inglese; le traduzioni dell’applicazione e le guide tradotte del repository sono separate.

- Test relativi al sito, alla pubblicazione originale e ai limiti di rilascio: **18 superati, 2 saltati**. I test saltati riguardano la creazione di collegamenti simbolici su questo filesystem Windows. I test verificano l’unicità dei metadati delle pagine, le pagine pubbliche esclusivamente in lingua inglese, gli URL canonici, tutte le voci della mappa del sito, le risorse/ancore locali, la navigazione strutturata e l’esclusione dei file privati.
- Sia `tools/check_site.py` che `tools/check_docs_site.py` hanno superato i test su Chromium a 320, 390, 768, 1024 e 1440 pixel in un sottopercorso dell’URL del progetto. I controlli previsti dalla guida coprono tutte le 11 pagine della documentazione, la ricerca e la navigazione da tastiera, il funzionamento/mancato funzionamento degli appunti e la leggibilità dei contenuti senza JavaScript.
- Cinque esempi interattivi superati: riproduzione/avanzamento/pausa/ripristino dei messaggi con movimento ridotto e sospensione fuori schermo; catene di hash originali/alterate/ricostruite/troncate; decisioni di accettazione/rollback/fork/mancata risposta da parte dei testimoni; e scenari di consegna completa/ritardata/mancante; nonché una mappa investigativa che collega osservazioni fittizie tra chat in base all’ID del mittente, alla destinazione e all’hash dell’allegato. I controlli investigativi hanno superato le verifiche di navigazione da tastiera e di fallback senza JavaScript . I risultati SHA-256 del browser sono stati confrontati in modo indipendente con l’`hashlib` di Python e il JSON canonico. L’esempio di hash ha inoltre mantenuto il proprio fallback leggibile quando Web Crypto non era disponibile.
- I rapporti di visualizzazione e gli indicatori dei grafici sono stati allineati alla tabella accessibile. Le etichette dell’asse mobile sono state ingrandite a seguito di una revisione visiva. Ogni esempio è contrassegnato come illustrativo o sintetico e nessun esempio relativo al browser entra in contatto con Telegram.
- Non sono state registrate richieste esterne, richieste HTTP non andate a buon fine né errori JavaScript. Gli screenshot da desktop/dispositivi mobili e le ricevute sono riportati sotto i codici `test-results/site/` e `test-results/docs-site/`. L’indice della documentazione, gli esempi di messaggi/hash, il layout di Witness, il grafico di consegna e la mappa investigativa sono stati esaminati nelle dimensioni desktop/dispositivi mobili.
- La scansione della pubblicazione ha superato i controlli su 282 file di origine pubblica e 1.426 collegamenti alla documentazione locale. Ruff ha superato i test relativi agli strumenti e alle verifiche del sito Python modificati.
- `docs/HOW-IT-WORKS.md` fornisce un complemento Markdown per GitHub con diagrammi e formule Mermaid. `docs/INVESTIGATION.md` copre l’ambito dell’intero account, l’acquisizione della cronologia per singola chat, i profili degli utenti, i riferimenti tra chat, le linee temporali e il trasferimento verificato dei casi. Le sue fasi e i suoi limiti sono stati verificati rispetto all’ ambito attuale, alla raccolta, al dossier, all’esportazione, al codice di verifica e a quello del pannello. Il rendering ospitato su GitHub non è stato verificato.

Si tratta di una verifica locale del sito web e della documentazione. Non aggiunge alcuna qualifica relativa a Telegram in tempo reale né conferma l’implementazione delle pagine ospitate, il corretto funzionamento della CI remota o l’indicizzazione da parte dei motori di ricerca. Si prega di consultare [la procedura di pubblicazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md) e [le note relative ai metadati del sito web](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/SEO.md).
