# Was wurde getestet?

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/

Der Live-Telegram-Test, automatisierte Prüfungen, Browser-Prüfungen und was noch nicht verifiziert ist.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Beweise und Verifizierung](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/)

![Beweise & Verifizierung](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Aktualisiert am 6. November 2026.** Die Ergebnisse sind an die Revision, die Umgebung und die für jeden Durchlauf aufgezeichnete Arbeitslast gebunden. Unter [Aktuelle Funktionen](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) werden die verfügbaren Workflows beschrieben; auf dieser Seite wird festgehalten, was tatsächlich überprüft wurde.

[Leistungsdiagramme](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Prüfung der Signed English-Übersetzung](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Messdaten zum Herunterladen](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Aktuelle Nachweise | Ergebnis | Geltungsbereich |
| --- | --- | --- |
| Release-Audit · 6. November | 1,461-Kerntests bestanden; 37-Plattformtests übersprungen | Quelle `92e539af40d8`; offene Ergebnisse beibehalten |
| Aktuelle Exporte · 6. Nov. | 127.713 und 141.781 Datensätze/s, vollständiger Zyklus | Zwei Konten pro Server; Text und Metadaten über WARP |
| Aufbewahrte Archive · 6. Nov. | 48-Archive; 3,598,381-Datensätze verifiziert | Vorhandene Archive wurden anhand der festgepinnten Workspace-Schlüssel überprüft |
| Trusted Live · 5. November | Geschützte CPU-Aufzeichnung und WARP-Prüfungen | Die offizielle Desktop-Anmeldung und der native Export bleiben ohne Einschränkungen bestehen. |
| Phala / Intel TDX · 4. November | Alle 16-Verifizierungsprüfungen wurden bei späteren Durchläufen bestanden | Historische Bereitstellung; kein Telegram-Konto auf dem CVM |

**Auf dieser Seite**

- [Release-Audit und neue Exporte · 6. November 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu und WARP · 5. November 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live-Bereitstellung von Phala Cloud · 4. November 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Bestandsliste der Live-Server-Journale · 1. November 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Aktuelle Offline- und Fehlerinjektionsprüfungen · 1. November 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live-Telegram-Test, gesamtes Konto · 29. Oktober 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Passwortgeschützter Export, geöffnet mit libarchive · 29. Oktober 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live-Telegram-Test · 27. bis 29. Oktober 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetische Messung der lokalen Kapazität](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Volltextsuche in einer Million Nachrichten · 5. November 2026](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Verbleibende Qualifikation](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/#remaining-qualification)

## Release-Audit und neue Exporte · 6. November 2026

Bei der Prüfung wurde v0.9.1 in der Version `92e539af40d8368d198ff5e040f1d876f2c1310e`, Release `92e539af40d8-83e41104669e`, verwendet. Die Smoke-Checks der installierten Pakete wurden auf drei Servern bestanden. Der signierte Bericht gibt den zu diesem Zeitpunkt beobachteten Zustand wieder.

[![Erfassungs- und vollständige Exportraten für zwei neue Workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Arbeitsaufwand | Aufzeichnungen | Erfassung | Vollständiger Zyklus | Vollzyklusrate |
| --- | --- | --- | --- | --- |
| Server A · zwei Konten | 27,030 | 189.043s | 211.647s | 127.713-Datensätze/s |
| Server B · zwei Konten | 29,299 | 182.513s | 206.650s | 141.781-Datensätze/s |

Beide Exporte begannen ohne Wiederaufnahme, schlossen Anhänge und Avatare aus und endeten ohne doppelte oder wiederverwendete Datensätze. Der vollständige Zyklus umfasst Vorbereitung, Erfassung, Auswahl, Paketierung und Archivüberprüfung. Server A führte zudem eine Prüfung auf das Lesen geschützter Chats durch. Vier FloodWait-Ereignisse auf A und drei auf B wurden berücksichtigt. Diese Beobachtungen begründen keine allgemeine Durchsatzgarantie.

| Überprüfen | Ergebnis | Qualifikation |
| --- | --- | --- |
| Kern-pytest | 1,461 bestanden | 37-Plattform überspringt |
| Browser / Browser-UX / Beweismaterial / Website | 102 / 66 / 15 / 9 bestanden | Diese Programme überschneiden sich mit anderen Tests; die Zahlen sind nicht additiv. |
| Add-on Capture | 124 bestanden | Drei offizielle Web-Prüfungen, die durch die erforderliche Chromium-Sandbox blockiert werden |
| API-Autorisierung | 269-Routen; 538-Anfragen bestanden | Fehlende Anmeldedaten und widerrufener Zugriff |
| Aufbewahrte Archive | 48 von 48 verifiziert | 3,598,381-Datensätze; angeheftete Arbeitsbereichsschlüssel |
| Live-Prüfungen der Flottenlesbarkeit | 24-Profile von 40 bestanden | 16-WARP-Routen haben die Qualifizierung nicht bestanden; diese Profile waren nicht verbunden |

Der [signierte Bericht](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) erfasst alle offenen Befunde, darunter drei Fehler in einem unveröffentlichten Snapshot eines geheimen Chats, der im geprüften Haupt-Build fehlt. Die frühere [Qualifizierung der öffentlichen Historie](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) verwendete eine andere Revision und Arbeitslast; deren Werte dürfen nicht mit diesem Vergleich kombiniert werden.

Überprüfen Sie den Originalbericht mithilfe des [-Pinned-Schlüssels und des Verifizierers](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Seine Signatur schützt den Bericht des Betreibers vor Manipulationen. Es handelt sich dabei nicht um eine unabhängige Beglaubigung, einen Nachweis der Telegram-Urheberschaft oder eine DSGVO-Zertifizierung.

## Trusted Live CPU Ubuntu und WARP · 5. November 2026

Der beibehaltene Integrationslauf verwendete einen reinen CPU-Gast „Ubuntu 24.04.5“ (4 vCPU, 8 GiB) unter QEMU innerhalb eines RunPod-CPU-Hosts. Der Collector verwendete `14e642a5`; die Verifizierung erfolgte mit `02072461`. Die endgültigen Korrekturen wurden in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) als `755f78f6` zusammengeführt, dessen Baum mit dem getesteten PR-Head übereinstimmte. Es handelte sich hierbei nicht um eine TEE.

- Ein echter WARP-Connector wurde als funktionsfähig gemeldet; bei HTTPS über Proxy wurden WARP und Gateway als aktiviert gemeldet. Drei Tests ergaben dieselbe Ausgangsadresse, was keine Garantie für eine feste IP-Adresse darstellt.
- Das Trennen von WARP führte zum Fehlschlagen der über den Proxy gesendeten Anfrage. Direkte HTTPS-Verbindungen zum Gateway-Dienst wurden abgelehnt. Im Recorder-Namespace wurden direkte IPv4/IPv6-Verbindungen, externe DNS-Anfragen und der in Docker integrierte UDP-Resolver blockiert.
- Ein Provider-Token mit eingeschränkten Lesezugriffsrechten konnte den Status und die Verbindungen auslesen, hatte jedoch keinen Zugriff auf das Registrierungs-Token des Connectors. Signierte Provider-Beobachtungen enthielten explizit nicht verfügbare Stichproben. Der Witness lief auf dem Host des Betreibers, was die Aufzeichnung und Aufbewahrung belegt, jedoch keine unabhängige Verwahrung durch Dritte.
- Official Desktop erreichte seinen nicht authentifizierten Begrüßungsbildschirm. Geschützte Tastatureingaben wurden während der Erfassung abgelehnt. Drei H.264-Anzeigesegmente wurden dekodiert und ihre Uhrenüberlagerung wurde überprüft. Das 18-Ereignis-Preflight-Archiv wurde anhand des festgesteckten Aufzeichnungsschlüssels und des beibehaltenen Checkpoints verifiziert.
- Die abschließenden Erfassungstests bestanden die 114-Fälle auf Windows- und Linux-CI-Umgebungen mit echtem Chromium/FFmpeg. Fünf Anker-Tests und Überprüfungen der Abhängigkeitshinweise wurden bestanden.

Ein erster Startversuch mit 2 vCPU/4 GiB lief unter gleichzeitiger Belastung durch die Bilderstellung in die Zeitüberschreitung und wurde durch die Schutzvorrichtung gestoppt; er wird nicht als Erfolg gewertet. Die manuelle Anmeldung mit einem Testkonto, der native Chat-Export, der echte Hybridvergleich und die Abmeldung auf Telegram-Seite stehen noch aus. Es wurde keine bereitgestellte Telethon-Sitzung importiert. Anhänge, automatische OCR, lokale drand-BLS-Verifizierung und Trusted-Live-TDX-Bescheinigung wurden nicht qualifiziert.

## Live-Bereitstellung in der Phala Cloud · 4. November 2026

**Historisches Ergebnis:** spätere Bereitstellungen bestanden alle 16 Verifizierungsprüfungen, einschließlich Intel TDX und des Quick-Tunnels. Der Neustart der Nachweise, die Erkennung signierter Adressen sowie die Zeitstempel der Berichte wurden separat überprüft. Jedes Test-CVM wurde nach seiner Ausführung entfernt.

| Einrichtung | Aufgezeichneter Wert |
| --- | --- |
| Anbieter | Phala Cloud · `tdx.small` · US-WEST-1 |
| Bereitstellung | `--provider phala --quick-tunnel`; zunächst leerer Arbeitsbereich |
| Anfänglicher Collector | `df7d860c` · v0.8.1 |
| Collector mit allen Korrekturen | `53a0f7e9` |
| Produktionsgast | `dstack-0.5.12`; SSH-Zugriff deaktiviert |
| Externe Dienste | ntfy.sh, GitHub und Intel PCS |
| Beobachtete Kosten | Sieben CVMs, zusammen etwa 1.9 US-Cent; historische Testpreise |

Die folgende Abfolge unterscheidet zwischen anfänglichen Fehlern, Korrekturen und abgeschlossenen Prüfungen. Mit diesen CVMs war kein Telegram-Konto verbunden.

**Bereitstellungen 1–2 · Anbieterunterschiede und Regressionsprüfungen**

Bei den ersten beiden Bereitstellungen wurden fünf Abweichungen gegenüber der simulierten Phala Cloud festgestellt. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) reproduziert nun jede dieser Abweichungen und schlägt ohne entsprechende Korrektur fehl:

| Auf der Phala Cloud | Vor der Korrektur | Behebung |
| --- | --- | --- |
| `compose_file.name` ist erforderlich | HTTP 422, nichts erstellt | Die Docker-Compose-Konfiguration enthält den CVM-Namen |
| Sofern kein leeres Skript angegeben wird, fügt Phala dem gemessenen „app-compose“ ein eigenes Pre-Launch-Skript hinzu (v0.0.20: Docker-Anmeldung, `docker compose pull`, Root-Passwort, SSH-Schlüssel aus `user_config`) | `tdx_compose` schlägt fehl: Code außerhalb der veröffentlichten Docker-Compose-Konfiguration | Das „app-compose“ setzt `pre_launch_script` auf `""`; Phala lässt dies anschließend weg |
| Ohne `image` wählt Phala `dstack-dev-0.5.12` aus, die Entwicklungsversion, bei der der SSH-Zugriff aktiviert ist | `server_state` schlägt fehl. Bei diesem Image wurde lediglich der Hardware-Attestationsdatensatz erfolgreich übermittelt; dies geht nur aus dem Anbieterdatensatz und `tdx_os` hervor. | Bei der Bereitstellung wird nach dem Produktions-Build der aktuellen Phala-Version „`dstack-0.5.12`“ gefragt |
| Bei deaktiviertem dstack-Gateway wird in den CVM-Details niemals ein `instance_id` angezeigt | Die Bereitstellung wartet 30 Minuten und schlägt fehl | Die Instanz-ID wird aus dem CVM-Status ausgelesen |
| Neustarts, Stopps und Starts sind CVM-Vorgänge, keine Anwendungsrevisionen | `provider_actions` führte keine Neustarts auf | Die Vorgänge werden ebenfalls gelesen |

**Bereitstellungs3 · Attestierung, Zugriffsprüfungen und Nachweise für Neustarts**

- Die CVM führte `dstack-0.5.12` mit deaktiviertem SSH-Zugriff aus. Der Collector übermittelte seine signierte Adresse etwa 1,5 Minuten nach der Erstellung. Der Deployment-Vorgang durchlief anschließend `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, Hardware-Attestationsdatensatz v4, FMSPC `20a06f000000`, nicht im Debug-Modus, nicht migrierbar, unterstützt kryptografische Verifizierungsdaten, die von Intel abgerufen wurden), `tdx_compose_hash`, `tdx_compose` (Byte für Byte) und `tdx_identity` (KMS-Schlüssel).
- Das Panel unter der Adresse trycloudflare.com gab ohne Token oder mit einem falschen Token den Status 401 zurück, und mit dem Panel-Token den Status 200.
- `verify`, wobei `--source` auf das GitHub-Archiv des Commits gesetzt war und der Fingerabdruck separat übermittelt wurde: Server, `server_state`, Firewall (kein Gateway, kein öffentlicher Endpunkt), Anbieterprotokoll, Abrechnung, Fingerabdruck, Quell-Hash, Boot sowie die fünf `tdx_*`-Prüfungen wurden bestanden. Cloudflare und `tdx_os` waren nicht verfügbar, daher lautete das Ergebnis „INCOMPLETE“.
- Zwei Neustarts über die Phala-API: Jedes Mal war die CVM in weniger als zwei Minuten wieder verfügbar – mit dem gleichen Collector-Schlüssel, einer neuen signierten Adresse und der alten, die den Status 530 zurückgab. `verify` meldete den neuen Start sowie beide Neustarts als „REVIEW“. Mit `--evidence` bestätigte es die Journal-Signaturen sowie drei Startvorgänge, jeweils mit einem eigenen Intel-TDX-Hardware-Attestationsdatensatz aus derselben CVM.
- `destroy` entfernte ausschließlich diese CVM. Der Arbeitsbereich war daraufhin leer, und die Panel-Adresse reagierte nicht mehr auf Anfragen.
- Die Preisabfrage des Panel-Assistenten ergab `tdx.small` mit 0,058 $ pro Stunde. Bei einem falschen Schlüssel erschien lediglich die Meldung „API-Schlüssel wurde nicht akzeptiert“.

**Nachfolgende Korrekturen · Erkennung signierter Adressen und Betriebssystemmessungen**

- Ohne den Adressschlüssel folgte `verify` dem neuesten, wohlgeformten Beitrag zum Thema Adresse, der in der veröffentlichten Docker-Compose-Konfiguration aufgeführt ist. Ein gefälschter Beitrag leitete ihn an einen Host weiter, der nicht existiert, und `statement` schlug fehl: Ein Fälscher konnte sich nicht als Sammler ausgeben, konnte jedoch die Überprüfung durch Dritte für bis zu 12 Stunden mit einem gefälschten zukünftigen Zeitstempel blockieren. Der Collector veröffentlicht nun seine Adresse ebenfalls mit seinem eigenen Schlüssel signiert; `verify` akzeptiert nur solche Beiträge, wenn der Collector sie erstellt, und die Beiträge werden nach dem Empfangszeitpunkt von ntfy.sh sortiert. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) spielt die gefälschten Beiträge erneut ab. Ein CVM führt dies nur aus einem Commit aus, der es enthält; daher hat der Collector dieses Durchlaufs seine Adresse noch nicht signiert, und `verify` hat dies gemeldet.
- `tdx_os` konnte ohne `dstack-mr` nicht ausgeführt werden, dessen aktuelle Version `measure-os` anstelle von dem in der Dokumentation genannten `measure --json` enthält. Der Verifizierer berechnet nun MRTD und RTMR0-2 selbst aus dem veröffentlichten Image und der VM-Konfiguration, einschließlich der ACPI-Tabellen.

**Bereitstellungs4 · alle 16-Prüfungen, Berichtssiegel und Neustartüberprüfung**

- Deploy lud das veröffentlichte `dstack-0.5.12` einmal herunter, glich es mit dem vom CVM gemeldeten Betriebssystem-Image-Hash ab, und `tdx_os` wurde akzeptiert: MRTD, RTMR0, RTMR1 und RTMR2 entsprechen den für QEMU 8.2.2, 1 vCPU und 2 GiB. Dieselbe Berechnung ergab einen anderen RTMR0-Wert bei angegebenen 4 GiB, 2 vCPUs, QEMU 9.2.1 oder einer zweiten Netzwerkkarte und schlug bei einem geänderten Kernel, einer geänderten Firmware oder einer geänderten Befehlszeile sowie beim Entwicklungs-Image fehl.
- `verify` hat alle 16 Prüfungen bestanden, einschließlich des Quick-Tunnel-Konnektors, sodass das Ergebnis „PASS“ lautete. Es erstellte das HTML- und das PDF-Zertifikat, digital versiegelt mit Signaturen und Zeitstempeln, darunter ein qualifizierter eIDAS-Zeitstempel der belgischen Regierungsstelle für Zeitstempelung TSU 202301 (Status: in der vertrauenswürdigen Liste Belgiens geführt), ein FreeTSA-Zeitstempel sowie die Signatur des Verifizierers; `check-report` bestätigte all diese Elemente sowie die Signatur des PDF-Dokuments.
- Nach einem Neustart bestätigte `verify --evidence` zwei Startvorgänge, die jeweils von einer innerhalb der CVM generierten Hardware-Bescheinigung begleitet wurden und jeweils aus dem veröffentlichten `dstack-0.5.12` gebootet wurden; der Neustart und der neue Bootvorgang wurden als „REVIEW“ eingestuft.
- `destroy` hinterließ den Arbeitsbereich leer.

**Bereitstellungs5 · Vom Collector signierte Erkennung und Ablehnung gefälschter Beiträge**

Der Collector wurde ab Commit `53a0f7e9` ausgeführt, der die oben genannten Korrekturen enthält.

- Der Collector veröffentlichte seine mit seinem eigenen Schlüssel signierte Adresse neben dem HMAC-Beitrag des Betreibers. Anschließend wurden dem Thema zwei gefälschte Beiträge hinzugefügt, einer mit einem auf Null gesetzten HMAC und einer, der mit einem anderen Ed25519-Schlüssel signiert war; beide gaben einen Zeitpunkt im Jahr 2096 an. `verify` übernahm die mit dem Sammler-Schlüssel signierte Adresse und bestand alle 16 Prüfungen; das Siegel trug erneut den qualifizierten belgischen Zeitstempel, den Zeitstempel von FreeTSA sowie die Signatur des Verifizierers, und `check-report` bestätigte diese.
- Nach einem Neustart veröffentlichte der Collector die neue signierte Adresse: `verify` fand sie sofort, der Operator **fand die aktuelle Adresse** 27 Sekunden später anhand des HMAC-Posts, und beide ignorierten die gefälschten Posts. `verify --evidence` bestätigte zwei Starts, die von `dstack-0.5.12` gebootet wurden.
- Die Bereitstellung gab an, was Phala für die CVM in Rechnung stellt, einschließlich Festplatte: 0,06078 $ pro Stunde.

### Assistent für Bedienfelder und verbleibender Umfang

Der Panel-Assistent wurde zweimal auf Phala Cloud ausgeführt, einmal über deren Job-API und einmal über den Browser mit einem echten Chromium: die Preisprüfung, die Erstellung mit dem Commit unter **Advanced**, alle sechs Attestierungsprüfungen bestanden, die Serverliste zeigte den in Rechnung gestellten Preis (44,37 USD pro Monat) an, **Find die aktuelle Adresse**, den Download der gemessenen Docker-Compose-Konfiguration sowie die Löschung. Im Browser traten keine Seitenfehler auf. Jedes Mal war der Arbeitsbereich anschließend leer.

Nicht berücksichtigt: eine Cloudflare-Domain auf Phala, ein Telegram-Konto auf dem CVM und das `dstack-0.6.1` Image. Der Preis des Assistenten vor der Erstellung entspricht ausschließlich dem Rechenpreis von Phala, da dessen API den Speicherpreis nur für ein bestehendes CVM angibt; die Serverliste zeigt den in Rechnung gestellten Preis nach der Erstellung. Alle Preise in diesem Abschnitt wurden am 4. November 2026 erfasst.

## Bestandsliste der Live-Server-Journale · 1. November 2026

Um ca. 19:15 UTC zählten sequenzielle, schreibgeschützte SQLite-`query_only`-Abfragen Ereignisse in zehn Arbeitsbereichsdatenbanken auf einem laufenden Server. Die Datenerfassung wurde während der Abfragen fortgesetzt, sodass es sich hierbei nicht um eine atomare Momentaufnahme über alle Arbeitsbereiche hinweg handelt.

| Beobachtet in den zehn Workspace-Datenbanken | Anzahl |
| --- | --- |
| Arbeitsbereiche mit mindestens einem `message.new`-Ereignis | 8 |
| Protokollaufzeichnungen, einschließlich betrieblicher Ereignisse | 1,610,818 |
| `message.new`-Ereignisse | 900,232 |
| `message.edited`-Ereignisse | 80,683 |
| `message.deleted`-Ereignisse | 400,536 |
| `message.recovered`-Ereignisse | 53,403 |
| `message.snapshot`-Ereignisse | 2,183 |
| `media.saved`-Ereignisse | 50,418 |
| `media.failed`-Ereignisse | 5,575 |
| `coverage.gap`-Ereignisse | 11 |
| Datenbank-Bytes, ohne WAL-Dateien und Medien | 7,909,003,264 |

Es handelt sich hierbei um **Ereigniszahlen**, nicht um einzelne Nachrichten, Personen oder Mediendateien. Dieselbe Nachricht kann in mehr als einem Arbeitsbereich erscheinen, und eine Bearbeitung oder Löschung kann ein weiteres Journalereignis erzeugen. `media.failed` zählt historische Fehlerereignisse, nicht die aktuelle Medienwarteschlange. Die Abfragen haben **weder** die Signaturen noch die vollständige Hash-Kette aller 1,610,818 Datensätze neu überprüft, noch wurden die Zustellung oder der Durchsatz gemessen oder festgestellt, dass jedes Telegram-Ereignis erfasst wurde. Es werden hier keine Nachrichteninhalte, Konto- oder Chat-IDs, Workspace-Bezeichnungen, Anmeldedaten oder private Dateien veröffentlicht.

Zum Zeitpunkt dieser Überprüfung deckte der separat konfigurierte öffentliche Monitor drei Quellen ab: Eine Erfassungsantwort war in Ordnung, zwei meldeten `no_response`. Dieser Monitor ist keine Zustandsübersicht über zehn Arbeitsbereiche. `no_response` bedeutet, dass der Beobachter bei dieser Überprüfung keine Antwort erhalten konnte; dies bedeutet nicht, dass Nachrichten verloren gegangen sind. Der kleinere Test vom 29. Oktober unten verfügt über eine eigene explizite Signatur und eine Hash-Ketten-Verifizierung.

## Aktuelle Offline- und Fehlerinjektionsprüfungen · 1. November 2026

Diese Prüfungen verwenden fiktive Daten und lokale Dateien; sie liefern Regressionsnachweise für die aktuelle Quelle, nicht für eine andere Live-Messung der Telegram-Zustellung:

| Überprüfen | Was wurde getestet? |
| --- | --- |
| [Quellarchiv](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Zwei Builds mit identischen Quellbytes, aber geänderten Dateizeiten erzeugten dieselbe ZIP-Datei und dieselbe Prüfsumme. Die exakten archivierten Bytes und Datei-Hashes stimmten überein; private Testdateien blieben ausgeschlossen. Ein simulierter Schreibfehler ließ das vorherige Archiv und die Prüfsumme intakt. |
| [Wiederherstellung des Kontoexports](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | Ein simulierter Festplattenfehler auf dem zweiten ZIP-Mitglied hinterließ kein veröffentlichtes oder unvollständiges ZIP-Archiv. Die Wiederaufnahme behielt jeden signierten Beleg byteweise identisch bei, erzeugte ein unabhängig überprüfbares Archiv unter Verwendung des erwarteten Signatur-Fingerabdrucks und behielt die synthetische Abdeckungslücke als Teilergebnis bei. Skalierungsaussagen verhindern wiederholte Aufgaben- und Belegscans, wenn die Historie wächst. |
| [Datenschutz durch minimierte Offenlegung](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetische Unicode-Namen und Aliase, verschachtelte Metadaten, unbekannte Absender und Medienfelder wurden in allen drei Identitätsmodi sowie bei Textauslassungen überprüft. Ein Versagen der Maskierungsgrenze führte nicht zu einer stillschweigenden Schwächung der Schwärzung; der ursprüngliche signierte Kontoexport blieb unverändert. |
| [Linux-Mediendecoder und OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | Ein [Linux-Docker-CI-Check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) beim Commit `5a9e0814` bestand die Tests mit generierten Ogg/Opus-, MP3-, M4A-, MP4- mit Video-, WAV- und FLAC-Eingaben; Kontrollen auf gefälschte Dauer und sekundäre Dateiverweise; sowie 48 mutierte Parser-Fixtures (34 abgelehnt, 14 innerhalb der Grenzen dekodiert). Echtes Tesseract-OCR lief mit unveränderten Original-Bytes. Der Decoder und das OCR liefen in netzwerkisolierten Containern ohne Whisper-Modell. |

Die Prüfungen laufen in den Workflows „[pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml)“ und „[full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml)“. Sie testen diese Fehlergrenzen, nicht jeden möglichen Speicherfehler oder ob eine Offenlegung automatisch sicher zur Veröffentlichung ist. Die Medienprüfung misst nicht die Genauigkeit der Spracherkennung oder die Zustellung über Telegram. Überprüfen Sie jedes Derivat, bevor Sie es teilen.

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

Docker/Compose- und Installationsprüfungen werden in CI protokolliert; die tatsächliche Phala-Bereitstellung sowie die externe Zeitstempelüberprüfung sind oben beschrieben. Sie gewährleisten keine anhaltende hohe Auslastung, keine vollständige Live-Plattform-/Rollenmatrix, keine unabhängige Sicherheitsüberprüfung, keine Validierung der Langzeitarchivierung und keine forensische Zertifizierung. Gespeicherter MTProto-Zustand und Catch-up sind implementiert; eine atomare, verlustfreie Live-Wiedergabe ist weiterhin nicht etabliert. Das neuere Backfill führt Commits von Nachrichten und Cursorn atomar durch und bewahrt verfügbare Recent Actions (jüngste Aktionen), doch unterscheidet sich seine synthetische Abdeckung von der Live-Qualifizierung. Siehe „[live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)“ für die kontrollierte Qualifizierungsmatrix.

Das öffentliche Audit-Verzeichnis  enthält ausschließlich den signierten Bericht und aggregierte Messwerte. Detaillierte Transaktionsbelege, Rohdatenaufzeichnungen und Kontodaten bleiben vertraulich. Anwendungs-Screenshots in `docs/assets/` verwenden fiktive Demonstrationsdaten.
