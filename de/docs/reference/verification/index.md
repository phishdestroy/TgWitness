# Was wurde getestet?

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/

Der Live-Telegram-Test, automatisierte Prüfungen, Browser-Prüfungen und was noch nicht verifiziert ist.

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

## Verbleibende Qualifizierung

Das gespeicherte Live-Protokoll dokumentiert tatsächliche Erfassungen, Bearbeitungen, Löschmeldungen, Anhänge, Nachprüfungen sowie die Handhabung von Ratenbeschränkungen. Es dokumentiert jedoch nicht die vollständige Zustellung oder eine kontrollierte Matrix aus Sichtbarkeitsrollen, Reaktionsakteuren, verlängerten „FloodWait“-Zeiten, Kontosperrungen und der Wiederherstellung nach Netzwerk- oder Prozessunterbrechungen. Die Ausgabe von QR-Token bleibt von der abgeschlossenen mobilen QR-Bestätigung getrennt.

Docker-Build/Ausführung, Installation unter Linux/macOS, anhaltend hohe Auslastung, unabhängige Sicherheitsüberprüfung, eine echte unabhängige TSA-Reaktion, Validierung der Zertifikatssperrung/Archivierung sowie forensische Zertifizierung bleiben außerhalb der erfassten Qualifizierung. Gespeicherter MTProto-Zustand und Nachholfunktion sind implementiert; atomares, dauerhaftes Replay ist weiterhin nicht etabliert. Die Erfassung von Admin-Protokollen, zusätzliche Reaktorlisten und prioritätsgesteuertes Short-Polling bleiben separate Funktionen. Die kontrollierte Qualifikationsmatrix entnehmen Sie bitte [der Live-Abnahme](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).

Lokale detaillierte Belege und Screenshots befinden sich unter „test-results/“ (in Git ignoriert). Der öffentliche Screenshot in „docs/assets/“ enthält ausschließlich fiktive Demonstrationsdaten.
