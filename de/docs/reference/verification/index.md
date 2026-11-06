# Was wurde getestet?

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/

Der Live-Telegram-Test, automatisierte Prüfungen, Browser-Prüfungen und was noch nicht verifiziert ist.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Updated 6 November 2026.** Results are tied to the revision, environment and workload recorded for each run. [Current capabilities](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describes the available workflows; this page records what has actually been checked.

[Performance graphs](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Signed English audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Downloadable measurements](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Latest evidence | Ergebnis | Geltungsbereich |
| --- | --- | --- |
| Release audit · 6 Nov | 1,461 core tests passed; 37 platform skips | Source `92e539af40d8`; open findings retained |
| Fresh exports · 6 Nov | 127.713 and 141.781 records/s, complete cycle | Two accounts per server; text and metadata through WARP |
| Retained archives · 6 Nov | 48 archives; 3,598,381 records verified | Existing archives checked against pinned workspace keys |
| Trusted Live · 5 Nov | Guarded CPU recording and WARP checks | Official Desktop login and native export remain unqualified |
| Phala / Intel TDX · 4 Nov | All 16 verifier checks passed on later runs | Historical deployment; no Telegram account on the CVM |

**On this page**

- [Release audit and fresh exports · 6 November 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu and WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live Phala Cloud deployment · 4 November 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Live server journal inventory · 1 November 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Recent offline and fault-injection checks · 1 November 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live Telegram test, whole account · 29 October 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Password-protected export opened with libarchive · 29 October 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live Telegram test · 27 to 29 October 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetic local capacity measurement](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Full-text search on one million messages · 5 November 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Remaining qualification](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#remaining-qualification)

## Release audit and fresh exports · 6 November 2026

The audit used v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. Installed-package smoke checks passed on three servers. The signed report retains the state observed at that time.

[![Acquisition and complete export rates for two fresh workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Workload | Aufzeichnungen | Acquisition | Complete cycle | Complete-cycle rate |
| --- | --- | --- | --- | --- |
| Server A · two accounts | 27,030 | 189.043 s | 211.647 s | 127.713 records/s |
| Server B · two accounts | 29,299 | 182.513 s | 206.650 s | 141.781 records/s |

Both exports began without resume, excluded attachments and avatars, and ended with zero duplicate or reused records. The complete cycle includes preparation, acquisition, selection, packaging and archive verification. Server A also ran a protected-chat read check. Four FloodWait events on A and three on B were respected. These observations do not establish a general throughput guarantee.

| Überprüfen | Ergebnis | Qualification |
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

## Live-Bereitstellung in der Phala Cloud · 4. November 2026

**Historical result:** later deployments passed all 16 verifier checks, including Intel TDX and the quick tunnel. Restart evidence, signed address discovery and report timestamps were checked separately. Each test CVM was removed after its run.

| Einrichtung | Recorded value |
| --- | --- |
| Anbieter | Phala Cloud · `tdx.small` · US-WEST-1 |
| Bereitstellung | `--provider phala --quick-tunnel`; initially empty workspace |
| Initial collector | `df7d860c` · v0.8.1 |
| Collector with all fixes | `53a0f7e9` |
| Production guest | `dstack-0.5.12`; SSH access disabled |
| External services | ntfy.sh, GitHub and Intel PCS |
| Observed cost | Seven CVMs, about 1.9 US cents together; historical test pricing |

The sequence below separates initial failures, fixes and completed checks. No Telegram account was connected to these CVMs.

**Deployments 1–2 · provider differences and regression checks**

Bei den ersten beiden Bereitstellungen wurden fünf Abweichungen gegenüber der simulierten Phala Cloud festgestellt. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) reproduziert nun jede dieser Abweichungen und schlägt ohne entsprechende Korrektur fehl:

| Auf der Phala Cloud | Vor der Korrektur | Behebung |
| --- | --- | --- |
| `compose_file.name` ist erforderlich | HTTP 422, nichts erstellt | Die Docker-Compose-Konfiguration enthält den CVM-Namen |
| Sofern kein leeres Skript angegeben wird, fügt Phala dem gemessenen „app-compose“ ein eigenes Pre-Launch-Skript hinzu (v0.0.20: Docker-Anmeldung, `docker compose pull`, Root-Passwort, SSH-Schlüssel aus `user_config`) | `tdx_compose` schlägt fehl: Code außerhalb der veröffentlichten Docker-Compose-Konfiguration | Das „app-compose“ setzt `pre_launch_script` auf `""`; Phala lässt dies anschließend weg |
| Ohne `image` wählt Phala `dstack-dev-0.5.12` aus, die Entwicklungsversion, bei der der SSH-Zugriff aktiviert ist | `server_state` schlägt fehl. Bei diesem Image wurde lediglich der Hardware-Attestationsdatensatz erfolgreich übermittelt; dies geht nur aus dem Anbieterdatensatz und `tdx_os` hervor. | Bei der Bereitstellung wird nach dem Produktions-Build der aktuellen Phala-Version „`dstack-0.5.12`“ gefragt |
| Bei deaktiviertem dstack-Gateway wird in den CVM-Details niemals ein `instance_id` angezeigt | Die Bereitstellung wartet 30 Minuten und schlägt fehl | Die Instanz-ID wird aus dem CVM-Status ausgelesen |
| Neustarts, Stopps und Starts sind CVM-Vorgänge, keine Anwendungsrevisionen | `provider_actions` führte keine Neustarts auf | Die Vorgänge werden ebenfalls gelesen |

**Deployment 3 · attestation, access checks and restart evidence**

- Die CVM führte `dstack-0.5.12` mit deaktiviertem SSH-Zugriff aus. Der Collector übermittelte seine signierte Adresse etwa 1,5 Minuten nach der Erstellung. Der Deployment-Vorgang durchlief anschließend `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, Hardware-Attestationsdatensatz v4, FMSPC `20a06f000000`, nicht im Debug-Modus, nicht migrierbar, unterstützt kryptografische Verifizierungsdaten, die von Intel abgerufen wurden), `tdx_compose_hash`, `tdx_compose` (Byte für Byte) und `tdx_identity` (KMS-Schlüssel).
- Das Panel unter der Adresse trycloudflare.com gab ohne Token oder mit einem falschen Token den Status 401 zurück, und mit dem Panel-Token den Status 200.
- `verify`, wobei `--source` auf das GitHub-Archiv des Commits gesetzt war und der Fingerabdruck separat übermittelt wurde: Server, `server_state`, Firewall (kein Gateway, kein öffentlicher Endpunkt), Anbieterprotokoll, Abrechnung, Fingerabdruck, Quell-Hash, Boot sowie die fünf `tdx_*`-Prüfungen wurden bestanden. Cloudflare und `tdx_os` waren nicht verfügbar, daher lautete das Ergebnis „INCOMPLETE“.
- Zwei Neustarts über die Phala-API: Jedes Mal war die CVM in weniger als zwei Minuten wieder verfügbar – mit dem gleichen Collector-Schlüssel, einer neuen signierten Adresse und der alten, die den Status 530 zurückgab. `verify` meldete den neuen Start sowie beide Neustarts als „REVIEW“. Mit `--evidence` bestätigte es die Journal-Signaturen sowie drei Startvorgänge, jeweils mit einem eigenen Intel-TDX-Hardware-Attestationsdatensatz aus derselben CVM.
- `destroy` entfernte ausschließlich diese CVM. Der Arbeitsbereich war daraufhin leer, und die Panel-Adresse reagierte nicht mehr auf Anfragen.
- Die Preisabfrage des Panel-Assistenten ergab `tdx.small` mit 0,058 $ pro Stunde. Bei einem falschen Schlüssel erschien lediglich die Meldung „API-Schlüssel wurde nicht akzeptiert“.

**Follow-up fixes · signed address discovery and OS measurements**

- Ohne den Adressschlüssel folgte `verify` dem neuesten, wohlgeformten Beitrag zum Thema Adresse, der in der veröffentlichten Docker-Compose-Konfiguration aufgeführt ist. Ein gefälschter Beitrag leitete ihn an einen Host weiter, der nicht existiert, und `statement` schlug fehl: Ein Fälscher konnte sich nicht als Sammler ausgeben, konnte jedoch die Überprüfung durch Dritte für bis zu 12 Stunden mit einem gefälschten zukünftigen Zeitstempel blockieren. Der Collector veröffentlicht nun seine Adresse ebenfalls mit seinem eigenen Schlüssel signiert; `verify` akzeptiert nur solche Beiträge, wenn der Collector sie erstellt, und die Beiträge werden nach dem Empfangszeitpunkt von ntfy.sh sortiert. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) spielt die gefälschten Beiträge erneut ab. Ein CVM führt dies nur aus einem Commit aus, der es enthält; daher hat der Collector dieses Durchlaufs seine Adresse noch nicht signiert, und `verify` hat dies gemeldet.
- `tdx_os` konnte ohne `dstack-mr` nicht ausgeführt werden, dessen aktuelle Version `measure-os` anstelle von dem in der Dokumentation genannten `measure --json` enthält. Der Verifizierer berechnet nun MRTD und RTMR0-2 selbst aus dem veröffentlichten Image und der VM-Konfiguration, einschließlich der ACPI-Tabellen.

**Deployment 4 · all 16 checks, report seals and restart verification**

- Deploy lud das veröffentlichte `dstack-0.5.12` einmal herunter, glich es mit dem vom CVM gemeldeten Betriebssystem-Image-Hash ab, und `tdx_os` wurde akzeptiert: MRTD, RTMR0, RTMR1 und RTMR2 entsprechen den für QEMU 8.2.2, 1 vCPU und 2 GiB. Dieselbe Berechnung ergab einen anderen RTMR0-Wert bei angegebenen 4 GiB, 2 vCPUs, QEMU 9.2.1 oder einer zweiten Netzwerkkarte und schlug bei einem geänderten Kernel, einer geänderten Firmware oder einer geänderten Befehlszeile sowie beim Entwicklungs-Image fehl.
- `verify` hat alle 16 Prüfungen bestanden, einschließlich des Quick-Tunnel-Konnektors, sodass das Ergebnis „PASS“ lautete. Es erstellte das HTML- und das PDF-Zertifikat, digital versiegelt mit Signaturen und Zeitstempeln, darunter ein qualifizierter eIDAS-Zeitstempel der belgischen Regierungsstelle für Zeitstempelung TSU 202301 (Status: in der vertrauenswürdigen Liste Belgiens geführt), ein FreeTSA-Zeitstempel sowie die Signatur des Verifizierers; `check-report` bestätigte all diese Elemente sowie die Signatur des PDF-Dokuments.
- Nach einem Neustart bestätigte `verify --evidence` zwei Startvorgänge, die jeweils von einer innerhalb der CVM generierten Hardware-Bescheinigung begleitet wurden und jeweils aus dem veröffentlichten `dstack-0.5.12` gebootet wurden; der Neustart und der neue Bootvorgang wurden als „REVIEW“ eingestuft.
- `destroy` hinterließ den Arbeitsbereich leer.

**Deployment 5 · collector-signed discovery and forged-post rejection**

The collector ran from commit `53a0f7e9`, which includes the fixes above.

- Der Collector veröffentlichte seine mit seinem eigenen Schlüssel signierte Adresse neben dem HMAC-Beitrag des Betreibers. Anschließend wurden dem Thema zwei gefälschte Beiträge hinzugefügt, einer mit einem auf Null gesetzten HMAC und einer, der mit einem anderen Ed25519-Schlüssel signiert war; beide gaben einen Zeitpunkt im Jahr 2096 an. `verify` übernahm die mit dem Sammler-Schlüssel signierte Adresse und bestand alle 16 Prüfungen; das Siegel trug erneut den qualifizierten belgischen Zeitstempel, den Zeitstempel von FreeTSA sowie die Signatur des Verifizierers, und `check-report` bestätigte diese.
- Nach einem Neustart veröffentlichte der Collector die neue signierte Adresse: `verify` fand sie sofort, der Operator **fand die aktuelle Adresse** 27 Sekunden später anhand des HMAC-Posts, und beide ignorierten die gefälschten Posts. `verify --evidence` bestätigte zwei Starts, die von `dstack-0.5.12` gebootet wurden.
- Die Bereitstellung gab an, was Phala für die CVM in Rechnung stellt, einschließlich Festplatte: 0,06078 $ pro Stunde.

### Panel wizard and remaining scope

Der Panel-Assistent wurde zweimal auf Phala Cloud ausgeführt, einmal über deren Job-API und einmal über den Browser mit einem echten Chromium: die Preisprüfung, die Erstellung mit dem Commit unter **Advanced**, alle sechs Attestierungsprüfungen bestanden, die Serverliste zeigte den in Rechnung gestellten Preis (44,37 USD pro Monat) an, **Find die aktuelle Adresse**, den Download der gemessenen Docker-Compose-Konfiguration sowie die Löschung. Im Browser traten keine Seitenfehler auf. Jedes Mal war der Arbeitsbereich anschließend leer.

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation. All prices in this section were observed on 4 November 2026.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Anzahl |
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

| Überprüfen | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Live-Telegram-Test, gesamtes Konto · 29. Oktober 2026

Das gleiche Konto wurde nach dem unten beschriebenen Test weitergeführt. Am 29. Oktober um 12:10 Uhr UTC wurde der Erfassungsbereich auf das gesamte Konto (Kanäle, Gruppen, private Chats und Bots) erweitert; das Bedienfeld forderte eine Bestätigung an, und das signierte Protokoll zeichnete dies auf. Um 17:59 Uhr UTC enthielt das Protokoll:

| Aufgezeichnet vom 27. Oktober, 21:36 Uhr, bis zum 29. Oktober, 17:59 Uhr (UTC) | Anzahl |
| --- | --- |
| Protokollaufzeichnungen | 9,968 |
| Neue Nachrichten | 5,308 |
| davon nach der Umstellung auf das vollständige Konto | 3,878 |
| Löschungen | 784 |
| von denen gelöscht wurden, nachdem TgWitness die Nachricht gespeichert hatte | 596 |
| Bearbeitungen | 41 |
| Durch Nachprüfungen hinzugefügte Nachrichten | 2,273 |
| Nachrichten, die bei einer erneuten Überprüfung nicht mehr auffindbar waren | 18 |
| Durch Verlaufs-Snapshots gespeicherte Nachrichten | 242 |
| Gespeicherte Anhänge | 247 |
| Der Collector startet | 19 |
| Telegram FloodWait pausiert | 26 |

- Die **„Verify**“-Prüfung des Gremiums bestätigte die Signaturen und die Hash-Kette aller 9.968 Datensätze.
- Die Nachrichten stammten aus zwei Gruppen bzw. Kanälen sowie drei privaten Chats und Bots. Eine Nachrichten-Schaltfläche wurde in **den Chats** betätigt; die Anfrage und die Antwort von Telegram sind im Protokoll enthalten.
- Neue Chats wurden hinzugefügt, als der Collector das Konto nach einem Neustart erneut scannte. Das Speichern der früheren Nachrichten neuer Chats war deaktiviert (`history = 0`), daher wird dies hier nicht behandelt.

Nicht abgedeckt: Reaktionen, Änderungen der Mitgliederzahl, Personenprofile, das Versenden von Nachrichten, der Beitritt per Einladung, Proxys, Benachrichtigungen, der Witness-Bot sowie die gleichzeitige Nutzung mehrerer Konten. Öffentliche Dateien enthalten ausschließlich Zahlenangaben.

## Passwortgeschützter Export, geöffnet mit libarchive · 29. Oktober 2026

Ein Archiv, das mit dem Exportverschlüsselungscode erstellt wurde (WinZip AES-256, das von 7-Zip und WinRAR gelesen wird), wurde unter Windows mit `tar` (bsdtar 3.6.2, libarchive) geöffnet. Mit dem richtigen Passwort stimmte die extrahierte Datei mit dem ursprünglichen SHA-256 überein; ein falsches Passwort wurde mit der Meldung „Incorrect passphrase“ abgelehnt. 7-Zip und WinRAR selbst wurden nicht ausgeführt.

## Live-Test von Telegram · 27. bis 29. Oktober 2026

Ein echtes Telegram-Konto, das über den integrierten API-Paar-Pool angemeldet war, zeichnete eine Supergruppe vom **27. Oktober, 21:36 Uhr UTC, bis zum 29. Oktober, 05:15 Uhr UTC**, auf. Der Collector wurde in diesem Zeitraum 12 Mal gestartet.

| Aufgezeichnet | Anzahl |
| --- | --- |
| Protokollaufzeichnungen, einschließlich Heartbeats und Dienstaufzeichnungen | 2,385 |
| Neue Nachrichten | 1,291 |
| Löschungen | 472 |
| von denen wurden gelöscht, nachdem TgWitness den Text gespeichert hatte | 347 |
| Bearbeitungen | 12 |
| Nachrichten, die während der Unterbrechung übersehen wurden und durch die erneute Überprüfung hinzugefügt wurden | 12 |
| Gespeicherte Anhänge | 17 |
| Anhänge wurden nicht heruntergeladen (Downloads deaktiviert oder keine Datei zum Herunterladen vorhanden) | 14 |
| Telegram FloodWait legt bei Nachprüfungen jeweils 3-sekündige Pausen ein | 8 |

- Die Signaturen und die Hash-Kette aller 2.385 Datensätze lassen sich anhand des öffentlichen Schlüssels des Protokolls verifizieren.
- Nach einem Neustart setzt der Collector den Vorgang ab dem gespeicherten Aktualisierungsstatus (`pts`) fort, und Telethon holt den Rückstand auf; bei der erneuten Überprüfung werden dann die noch fehlenden Nachrichten hinzugefügt.
- Bei jedem „FloodWait“ wartete der Collector die angeforderte Zeit ab und fuhr dann fort.
- Das Konto blieb angemeldet, und dieselbe Sitzung wurde am 29. Oktober wiederhergestellt.

Nicht Gegenstand dieses Tests: mehrere Konten gleichzeitig, Administratorrechte, Proxys, Ausfälle von mehr als einigen Stunden sowie das vollständige [Live-Abnahmeverfahren](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Öffentliche Dateien enthalten ausschließlich diese Zahlenangaben: keine Konto- oder Chat-Kennungen, Nachrichten oder Anmeldedaten.

## Synthetische Messung der lokalen Kapazität

Befehl: `python tools/check_capacity.py --events 10000 --chats 100`

| Kennzahl | Beobachtet |
| --- | --- |
| Eingabe | 10.000 synthetische Nachrichtenereignisse aus 100 ausgewählten synthetischen Quellen |
| Nachrichtentext | 400 Zeichen; keine Medien oder Netzwerke |
| Erfassung | 53,273 Sekunden; 187,7 Ereignisse pro Sekunde |
| Latenz des Handlers | p50 4,162 ms; p95 7,784 ms; Maximum 129,118 ms |
| ZIP-Export | 19,868 Sekunden bei aktiviertem tracemalloc |
| Spitzenwerte der nachverfolgten Python-Exportzuweisungen | 0,51 MiB; RSS nicht verarbeiten |
| ZIP-Größe | 4.610.962 Byte |
| Unabhängige Überprüfung | Alle 10.000 Ereignisse wurden verifiziert |

Hiermit wird der lokale Pfad für die fortlaufende Aufzeichnung und den Export auf diesem Windows-Host gemessen. Nicht gemessen werden die MTProto-Übermittlung, gleichzeitige Konten, Telegram-Drosselung, Medien, eine lang andauernde Arbeitslast oder eine garantierte Anzahl echter Chats. Die Messung erfolgte vor der Einführung der endgültigen Offline-Zeitstempel-Tools, die den gemessenen Nachrichtenpfad nicht verändern.

## Volltextsuche in einer Million Nachrichten · 5. November 2026

Befehl: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

Ein deterministisches, signiertes Protokoll mit 1.000.000 synthetischen Nachrichten in 200 Chats (russische Wortformen, Ukrainisch, Englisch, Chinesisch, Japanisch, Links und Handles) wurde in 71 Sekunden indiziert; der Index belegte 58 MiB zusätzlich zu einem 1,50 GiB großen Protokoll. Die Suche nach der besten Übereinstimmung dauerte 9 bis 190 ms (Median), gegenüber 2,4 bis 3,2 Sekunden bei der bisherigen Teilstring-Suche . Vollständige Ergebnisse, Hardware und Grenzen: [Volltextsuche](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/#benchmark). `tools/test_fulltext.py` überprüft außerdem ein signiertes Archiv, das vor der Volltextsuche (`tools/fixtures/evidence-before-fulltext.zip`) mit dem aktuellen Verifizierer sowie ein aktuelles Archiv mit dem eigenen `verify.py`.

## Verbleibende Qualifizierung

Das gespeicherte Live-Protokoll dokumentiert tatsächliche Erfassungen, Bearbeitungen, Löschmeldungen, Anhänge, Nachprüfungen sowie die Handhabung von Ratenbeschränkungen. Es dokumentiert jedoch nicht die vollständige Zustellung oder eine kontrollierte Matrix aus Sichtbarkeitsrollen, Reaktionsakteuren, verlängerten „FloodWait“-Zeiten, Kontosperrungen und der Wiederherstellung nach Netzwerk- oder Prozessunterbrechungen. Die Ausgabe von QR-Token bleibt von der abgeschlossenen mobilen QR-Bestätigung getrennt.

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

The [public audit directory](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) contains only the signed report and aggregate measurements. Detailed operational receipts, raw captures and account material remain private. Application screenshots in `docs/assets/` use fictional demonstration data.
