# Cosa è stato testato

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/

Il test in tempo reale su Telegram, i controlli automatizzati, i controlli sul browser e ciò che rimane non verificato.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Prove e verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/)

![Prove e verifica](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Aggiornato il 6 novembre 2026.** I risultati sono legati alla revisione, all’ambiente e al carico di lavoro registrati per ogni esecuzione. [Le funzionalità attuali](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) descrivono i flussi di lavoro disponibili; questa pagina riporta ciò che è stato effettivamente verificato.

[Grafici delle prestazioni](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Revisione in inglese certificata](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Misurazioni scaricabili](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Prove più recenti | Risultato | Ambito di applicazione |
| --- | --- | --- |
| Audit della versione · 6, novembre | Test di base 1,461 superati; la piattaforma 37 salta | Fonte `92e539af40d8`; risultati aperti mantenuti |
| Esportazioni recenti · 6 novembre | 127.713 e 141.781 record/s, ciclo completo | Due account per server; testo e metadati tramite WARP |
| Archivi conservati · 6 novembre | Archivi 48; record 3,598,381 verificati | Archivi esistenti verificati rispetto alle chiavi dell’area di lavoro fissate |
| Trusted Live · 5 novembre | Registrazione protetta dell’attività della CPU e controlli WARP | L'accesso ufficiale da desktop e l'esportazione nativa rimangono senza riserve |
| Phala / Intel TDX · 4 novembre | Tutti i controlli del verificatore 16 sono stati superati nelle esecuzioni successive | Implementazione storica; nessun account Telegram sul CVM |

**In questa pagina**

- [Audit della versione e nuove esportazioni · 6 novembre 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu e WARP · 5 novembre 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Implementazione live di Phala Cloud · 4 novembre 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Inventario del registro del server in tempo reale · 1 novembre 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Controlli offline e di iniezione di errori recenti · 1 novembre 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Test Telegram in tempo reale, account completo · 29 ottobre 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Esportazione protetta da password aperta con libarchive · 29 ottobre 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Test in tempo reale su Telegram · dal 27 al 29 ottobre 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Misurazione sintetica della capacità locale](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Ricerca full-text su un milione di messaggi · 5 novembre 2026](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Qualifica rimanente](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/#remaining-qualification)

## Audit della versione e nuove esportazioni · 6 novembre 2026

L’audit ha utilizzato la versione v0.9.1 alla fonte `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. I controlli di funzionamento dei pacchetti installati sono stati superati su tre server. Il rapporto firmato riporta lo stato osservato in quel momento.

[![Tassi di acquisizione ed esportazione completa per due nuovi carichi di lavoro](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Carico di lavoro | Registrazioni | Acquisizione | Ciclo completo | Tasso di ciclo completo |
| --- | --- | --- | --- | --- |
| Server A · due account | 27,030 | 189.043 s | 211.647 s | 127.713 registrazioni/s |
| Server B · due account | 29,299 | 182.513 s | 206.650 s | 141.781 registrazioni/s |

Entrambe le esportazioni sono iniziate senza ripresa, hanno escluso allegati e avatar e si sono concluse senza record duplicati o riutilizzati. Il ciclo completo comprende preparazione, acquisizione, selezione, impacchettamento e verifica dell’archivio. Il server A ha inoltre eseguito un controllo di lettura delle chat protette. Sono stati rispettati quattro eventi FloodWait su A e tre su B. Queste osservazioni non costituiscono una garanzia generale di throughput.

| Verifica | Risultato | Requisiti |
| --- | --- | --- |
| Pytest di base | 1,461: superato | La piattaforma 37 salta |
| Browser / esperienza utente del browser / prove / sito | 102 / 66 / 15 / 9 superati | Questi programmi si sovrappongono ad altri test; i conteggi non sono cumulativi |
| Componente aggiuntivo Capture | 124: superato | Tre controlli Web ufficiali bloccati dalla sandbox Chromium richiesta |
| Autorizzazione API | Percorsi 269; richieste 538 passate | Credenziali mancanti e accesso revocato |
| Archivi conservati | 48 di 48 verificato | Record 3,598,381; chiavi dell’area di lavoro fissate |
| Controlli in tempo reale sulla lettura della flotta | Profili 24/40 superati | I percorsi WARP 16 non hanno superato la qualificazione; tali profili non erano connessi |

Il rapporto [firmato](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) registra tutti i risultati emersi, inclusi tre difetti in uno snapshot di una chat segreta non pubblicato, assente dalla build principale sottoposta a revisione. La precedente qualifica [della cronologia pubblica](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) utilizzava una diversa revisione e un carico di lavoro diverso; i suoi tassi non devono essere combinati con questo confronto.

Verificare il rapporto originale utilizzando la chiave [pinned e il verificatore](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). La sua firma protegge il rapporto dell’operatore da eventuali alterazioni. Non si tratta di un’attestazione indipendente, di una prova della paternità del messaggio su Telegram né di una certificazione GDPR.

## Trusted Live CPU Ubuntu e WARP · 5 novembre 2026

L'esecuzione di integrazione conservata ha utilizzato un guest Ubuntu 24.04.5 solo CPU (vCPU 4, 8 GiB) sotto QEMU all'interno di un host RunPod CPU. Il collettore utilizzava `14e642a5`; la verifica utilizzava `02072461`. Le correzioni finali sono state unite in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) come `755f78f6`, il cui albero corrispondeva alla testa del PR testato. Non si trattava di un TEE.

- Un vero connettore WARP è risultato funzionante; l’HTTPS tramite proxy ha segnalato che WARP e Gateway erano abilitati. Tre sonde hanno rilevato lo stesso indirizzo di uscita, il che non garantisce un IP fisso.
- La disconnessione da WARP ha causato il fallimento della richiesta proxy. Il servizio gateway HTTPS diretto è stato rifiutato. Nello spazio dei nomi del registratore, sono stati bloccati gli indirizzi IPv4/IPv6 diretti, il DNS esterno e il resolver UDP integrato di Docker.
- Un token provider in sola lettura con ambito limitato poteva leggere gli stati di integrità e le connessioni, ma non poteva leggere il token di registrazione del connettore. Le osservazioni firmate dal provider includevano campioni esplicitamente non disponibili. Il witness era in esecuzione sull’host dell’operatore, quindi ciò dimostra la registrazione e la conservazione dei dati, non la custodia da parte di terzi indipendenti.
- Official Desktop ha visualizzato la schermata di benvenuto senza autenticazione. L’input da tastiera protetto è stato rifiutato durante l’acquisizione. Sono stati decodificati tre segmenti di display H.264 e ne è stata ispezionata la sovrapposizione dell’orologio. L’archivio di preflight dell’evento 18 è stato verificato rispetto alla chiave di registrazione fissata e al checkpoint conservato.
- I test di acquisizione finali hanno superato i casi 114 su CI Windows e Linux, con Chromium/FFmpeg reali. Sono stati superati cinque test di riferimento e i controlli relativi alle dipendenze.

Un avvio iniziale con vCPU 2/4 GiB è andato in timeout a causa del carico simultaneo della creazione dell’immagine e si è interrotto tramite il meccanismo di protezione; non viene conteggiato come successo. L’accesso manuale all’account di test, l’esportazione nativa della chat, il confronto ibrido reale e il logout dal lato Telegram rimangono in sospeso. Non è stata importata alcuna sessione Telethon fornita. Allegati, OCR automatico, verifica BLS drand locale e attestazione Trusted Live TDX non sono stati qualificati.

## Distribuzione su Phala Cloud · 4 novembre 2026

**Risultato storico: le successive implementazioni** hanno superato tutti i controlli del verificatore 16, compresi Intel TDX e il tunnel rapido. Le prove di riavvio, l’individuazione degli indirizzi firmati e i timestamp dei report sono stati verificati separatamente. Ogni CVM di test è stato rimosso dopo l’esecuzione.

| Configurazione | Valore registrato |
| --- | --- |
| Fornitore | Phala Cloud · `tdx.small` · US-WEST-1 |
| Implementazione | `--provider phala --quick-tunnel`; area di lavoro inizialmente vuota |
| Collettore iniziale | `df7d860c` · v0.8.1 |
| Collector con tutte le correzioni | `53a0f7e9` |
| Ospite di produzione | `dstack-0.5.12`; accesso SSH disabilitato |
| Servizi esterni | ntfy.sh, GitHub e Intel PCS |
| Costo osservato | Sette CVM, per un totale di circa 1.9 centesimi di dollaro USA; prezzi storici dei test |

La sequenza riportata di seguito distingue tra errori iniziali, correzioni e controlli completati. Nessun account Telegram era collegato a questi CVM.

**Implementazioni 1–2 · differenze tra provider e controlli di regressione**

Le prime due distribuzioni hanno rilevato cinque differenze rispetto al Phala Cloud simulato. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) ora riproduce ciascuna di esse e fallisce senza la relativa correzione:

| Su Phala Cloud | Prima della correzione | Correzione |
| --- | --- | --- |
| È richiesto `compose_file.name` | HTTP 422, non è stato creato nulla | La configurazione di Docker Compose riporta il nome della CVM |
| A meno che non ne venga specificato uno vuoto, Phala aggiunge il proprio script di pre-avvio al file app-compose sottoposto a misurazione (v0.0.20: login Docker, `docker compose pull`, password di root, chiavi SSH da `user_config`) | `tdx_compose` genera un errore: codice al di fuori della configurazione Docker Compose pubblicata | L’app-compose imposta `pre_launch_script` su `""`; Phala quindi lo omette |
| In assenza di `image`, Phala seleziona `dstack-dev-0.5.12`, la build di sviluppo, con accesso SSH abilitato | `server_state` non supera il controllo. In questa immagine è stato superato solo il record di attestazione hardware; solo il record del fornitore e `tdx_os` lo indicano | L’implementazione richiede la build di produzione dell’attuale versione di Phala, `dstack-0.5.12` |
| Con il gateway dstack disattivato, i dettagli della CVM non riportano mai un codice `instance_id` | La distribuzione attende 30 minuti e fallisce | L’ID dell’istanza viene ricavato dallo stato del CVM |
| I riavvii, gli arresti e gli avviamenti sono operazioni relative alla CVM, non revisioni dell’applicazione | `provider_actions` non ha riportato i riavvii | Le operazioni vengono lette come segue |

**Distribuzione 3 · attestazione, controlli di accesso e prove di riavvio**

- La CVM ha eseguito `dstack-0.5.12` con l’accesso SSH disattivato. Il collettore ha pubblicato il proprio indirizzo firmato circa 1,5 minuti dopo la creazione. La distribuzione ha quindi superato `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, record di attestazione hardware v4, FMSPC `20a06f000000`, non in modalità debug, non migrabile, con supporto per i dati di verifica crittografica recuperati da Intel), `tdx_compose_hash`, `tdx_compose` (byte per byte) e `tdx_identity` (chiavi KMS).
- Il pannello all’indirizzo trycloudflare.com ha restituito un codice di stato 401 in assenza di token o in presenza di un token errato, e un codice di stato 200 con il token del pannello.
- `verify` con `--source` impostato sull’archivio GitHub del commit e l’impronta digitale superata separatamente: server, `server_state`, firewall (nessun gateway, nessun endpoint pubblico), log del provider, estratto conto, impronta digitale, hash di origine, avvio e i cinque controlli `tdx_*` superati. Cloudflare e `tdx_os` non erano disponibili, pertanto il risultato è stato INCOMPLETO.
- Due riavvii tramite l’API di Phala: ogni volta la CVM è tornata operativa in meno di due minuti con la stessa chiave di raccolta, un nuovo indirizzo firmato e quello precedente che rispondeva con il codice 530. `verify` ha segnalato il nuovo avvio ed entrambi i riavvii come REVIEW. Con `--evidence` ha confermato le firme del journal e tre avvii, ciascuno con il proprio record di attestazione hardware Intel TDX proveniente dallo stesso CVM.
- `destroy` ha rimosso solo quella CVM. L’area di lavoro era quindi vuota e l’indirizzo del pannello ha smesso di rispondere.
- La verifica del prezzo nella procedura guidata del pannello indicava `tdx.small` a 0,058 dollari l’ora. Una chiave errata ha generato un semplice messaggio del tipo «chiave API non accettata».

**Correzioni successive · individuazione degli indirizzi firmati e misurazioni del sistema operativo**

- In assenza della chiave di indirizzo, `verify` ha seguito l’ultimo post ben formato relativo all’argomento dell’indirizzo, che è riportato nella configurazione Docker Compose pubblicata. Un post contraffatto lo ha indirizzato verso un host inesistente e `statement` ha fallito: un falsario non è riuscito a spacciarsi per il collettore, ma ha potuto bloccare la verifica da parte di terzi, per un massimo di 12 ore, utilizzando un timestamp futuro contraffatto. Il collettore ora pubblica anche il proprio indirizzo firmato con la propria chiave; `verify` accetta solo tali messaggi quando sono emessi dal collettore stesso, e i messaggi vengono ordinati in base all’ora di ricezione da parte di ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) riproduce i post contraffatti. Un CVM esegue questa operazione solo a partire da un commit che la contenga, pertanto il collettore di questa esecuzione non aveva ancora firmato il proprio indirizzo e `verify` lo ha segnalato.
- `tdx_os` non poteva essere eseguito senza `dstack-mr`, la cui versione attuale presenta `measure-os` anziché il `measure --json` indicato nella documentazione. Il verificatore ora calcola autonomamente MRTD e RTMR0-2 a partire dall’immagine pubblicata e dalla configurazione della VM, tabelle ACPI incluse.

**Distribuzione 4 · tutti i controlli 16, sigilli dei report e verifica del riavvio**

- Il processo di distribuzione ha scaricato una volta il file `dstack-0.5.12` pubblicato, lo ha confrontato con l’hash dell’immagine del sistema operativo segnalato dalla CVM e `tdx_os` è risultato conforme: MRTD, RTMR0, RTMR1 e RTMR2 corrispondono ai valori calcolati per QEMU 8.2.2, 1 vCPU e 2 GiB. Lo stesso calcolo ha fornito un valore RTMR0 diverso per una configurazione dichiarata di 4 GiB, 2 vCPU, QEMU 9.2.1 o una seconda scheda di rete, e ha dato esito negativo in caso di modifica del kernel, del firmware o della riga di comando e per l’immagine di sviluppo.
- `verify` ha superato tutti e 16 i controlli, compreso il connettore del tunnel rapido, pertanto il risultato è stato «PASS». Ha generato il certificato in formato HTML e PDF, sigillato digitalmente con firme e timbri temporali, tra cui un timbro temporale eIDAS qualificato fornito dall’ unità di marcatura temporale del governo belga TSU 202301 (stato concesso nell’elenco di fiducia del Belgio ), un timbro temporale FreeTSA e la firma del verificatore; `check-report` ha confermato tutti questi elementi e la firma del PDF.
- Dopo un riavvio, `verify --evidence` ha confermato due avviamenti, ciascuno accompagnato da un’attestazione hardware generata all’interno della CVM e ciascuno avviato dal `dstack-0.5.12` pubblicato; sia il riavvio che il nuovo avvio erano di tipo REVIEW.
- `destroy` ha lasciato l’area di lavoro vuota.

**Implementazione 5 · individuazione firmata dal collettore e rifiuto dei post contraffatti**

Il collector è stato eseguito a partire dal commit `53a0f7e9`, che include le correzioni sopra indicate.

- Il collettore ha pubblicato il proprio indirizzo firmato con la propria chiave, accanto al post HMAC dell’operatore. Al thread sono stati quindi aggiunti due post contraffatti, uno con un HMAC azzerato e uno firmato da un’altra chiave Ed25519, entrambi con data indicante l’anno 2096. `verify` ha preso l’indirizzo firmato dalla chiave del collettore e ha superato tutti e 16 i controlli; il sigillo riportava nuovamente il timbro temporale belga qualificato, il timbro temporale di FreeTSA e la firma del verificatore, e `check-report` li ha confermati.
- Dopo un riavvio, il collettore ha pubblicato il nuovo indirizzo firmato: `verify` lo ha individuato immediatamente, mentre l’ operatore **ha individuato l’indirizzo corrente** 27 secondi dopo dal post HMAC, ed entrambi hanno ignorato i post contraffatti. `verify --evidence` ha confermato due avvii effettuati da `dstack-0.5.12`.
- Il processo di distribuzione ha indicato l’importo addebitato da Phala per il CVM, disco incluso: 0,06078 dollari all’ora.

### Procedura guidata del pannello e ambito rimanente

La procedura guidata del pannello è stata eseguita su Phala Cloud due volte: una tramite la sua API di lavoro e una tramite il browser con un Chromium reale: la verifica del prezzo, la creazione con il commit sotto **Advanced**, tutti e sei i controlli di attestazione superati, l’elenco dei server che mostrava il prezzo fatturato (44,37 USD al mese), **Find l’indirizzo corrente**, il download della configurazione Docker Compose misurata e l’eliminazione. Il browser non ha rilevato errori di pagina. In entrambi i casi, l’area di lavoro risultava vuota al termine dell’operazione.

Non inclusi: un dominio Cloudflare su Phala, un account Telegram sul CVM e l’immagine `dstack-0.6.1` . Il prezzo indicato dalla procedura guidata prima della creazione corrisponde esclusivamente al costo di elaborazione di Phala, poiché la sua API indica il costo del disco solo per un CVM esistente; l’elenco dei server mostra il prezzo fatturato dopo la creazione. Tutti i prezzi riportati in questa sezione sono stati rilevati il 4 novembre 2026.

## Inventario del registro del server in tempo reale · 1 novembre 2026

A circa 19:15 UTC, le query SQLite `query_only` sequenziali in sola lettura hanno contato gli eventi in dieci database dell’area di lavoro su un server in esecuzione. La raccolta è proseguita durante le query, quindi non si tratta di un’istantanea atomica trasversale alle aree di lavoro.

| Osservato nei dieci database degli spazi di lavoro | Conteggio |
| --- | --- |
| Aree di lavoro con almeno un evento `message.new` | 8 |
| Registrazioni di diario, inclusi gli eventi operativi | 1,610,818 |
| Eventi `message.new` | 900,232 |
| Eventi `message.edited` | 80,683 |
| Eventi `message.deleted` | 400,536 |
| Eventi `message.recovered` | 53,403 |
| Eventi `message.snapshot` | 2,183 |
| Eventi `media.saved` | 50,418 |
| Eventi `media.failed` | 5,575 |
| Eventi `coverage.gap` | 11 |
| Byte del database, esclusi i file WAL e i file multimediali | 7,909,003,264 |

Si tratta di **conteggi di eventi**, non di messaggi, persone o file multimediali unici. Lo stesso messaggio può apparire in più di un’area di lavoro, e una modifica o un’eliminazione può generare un altro evento nel registro. `media.failed` conta gli eventi di errore storici, non la coda multimediale attuale. Le query **non** hanno verificato ex novo le firme né la catena di hash completa di tutti i 1,610,818 record, né hanno misurato la consegna o il throughput, né hanno stabilito che ogni evento di Telegram fosse stato acquisito. Nessun contenuto di messaggi, ID di account o chat, etichette degli spazi di lavoro, credenziali o file privati sono pubblicati qui.

Al momento della presente revisione, il monitor pubblico configurato separatamente copriva tre fonti: una risposta di acquisizione era OK e due riportavano `no_response`. Tale monitor non è un riepilogo dello stato di salute di dieci spazi di lavoro. `no_response` significa che l’osservatore non è riuscito a ottenere una risposta in quel controllo; ciò non implica la perdita di messaggi. Il test più piccolo del 29 ottobre riportato di seguito ha una propria firma esplicita e una verifica della catena di hash.

## Controlli offline e di iniezione di errori recenti · 1 novembre 2026

Questi controlli utilizzano dati fittizi e file locali; aggiungono prove di regressione per la fonte attuale, non per un’altra misurazione della consegna su Telegram in tempo reale:

| Verifica | Cosa è stato testato |
| --- | --- |
| [Archivio sorgente](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Due build con byte sorgente identici ma con date dei file modificate hanno prodotto lo stesso file ZIP e lo stesso checksum. I byte esatti dell’archivio e gli hash dei file corrispondevano; i file di test privati sono rimasti esclusi. Un errore di scrittura simulato ha lasciato intatti l’archivio e il checksum precedenti. |
| [Recupero esportazione account](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | Un errore simulato sul disco relativo al secondo membro dello ZIP non ha prodotto alcun file ZIP pubblicato o parziale. La ripresa del processo ha mantenuto ogni ricevuta firmata identica a livello di byte, ha generato un archivio verificabile in modo indipendente utilizzando l’impronta digitale di firma prevista e ha conservato la lacuna di copertura sintetica come risultato parziale. Le asserzioni di scala impediscono la ripetizione delle scansioni delle attività e delle ricevute man mano che le cronologie crescono. |
| [Privacy con divulgazione ridotta al minimo](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | I nomi e gli alias Unicode sintetici, i metadati annidati, i mittenti sconosciuti e i campi multimediali sono stati verificati in tutte e tre le modalità di identità e in presenza di omissioni di testo. Un errore relativo al limite di mascheramento non ha compromesso silenziosamente la redazione; l’esportazione originale dell’account firmata è rimasta invariata. |
| [Decodificatore multimediale per Linux e OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | Un [controllo CI su Docker in ambiente Linux](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) al commit `5a9e0814` ha superato i test con input generati in formato Ogg/Opus, MP3, M4A, MP4 con video, WAV e FLAC; controlli su durata falsificata e riferimenti a file secondari; e 48 fixture del parser mutate (34 rifiutate, 14 decodificate entro i limiti). L’OCR Tesseract reale è stato eseguito senza modificare i byte originali. Il decodificatore e l’OCR sono stati eseguiti in container isolati dalla rete senza un modello Whisper. |

I controlli vengono eseguiti nei flussi di lavoro [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) e [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml). Essi verificano questi limiti di errore, non ogni possibile errore di archiviazione né se una divulgazione sia automaticamente sicura da pubblicare. Il controllo multimediale non misura l’accuratezza del riconoscimento vocale né la consegna tramite Telegram. Esaminare ogni derivato prima di condividerlo.

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

I controlli relativi a Docker/Compose e all’installazione sono registrati nella CI; la distribuzione reale su Phala e la verifica esterna dei timestamp sono descritte sopra. Essi non garantiscono un carico elevato e prolungato, una matrice completa di piattaforme/ruoli in tempo reale, una revisione indipendente della sicurezza, una convalida dell’archiviazione a lungo termine né una certificazione forense. Lo stato MTProto salvato e il catch-up sono implementati; il replay live atomico senza perdita di dati rimane non stabilito. Il backfill più recente esegue il commit di messaggi e cursori in modo atomico e conserva le azioni recenti disponibili, ma la sua copertura sintetica è distinta dalla qualificazione live. Vedere [accettazione live](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) per la matrice di qualificazione controllata.

La directory di audit pubblico  contiene solo il rapporto firmato e le misurazioni aggregate. Le ricevute operative dettagliate, le acquisizioni grezze e il materiale relativo agli account rimangono privati. Gli screenshot dell’applicazione in `docs/assets/` utilizzano dati dimostrativi fittizi.
