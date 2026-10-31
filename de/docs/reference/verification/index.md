# Was wurde getestet?

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/

Der Live-Telegram-Test, automatisierte Prüfungen, Browser-Prüfungen und was noch nicht verifiziert ist.

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

Ältere Einträge weiter unten beschreiben die jeweiligen Durchläufe; bei den meisten davon kamen synthetische Test-Clients zum Einsatz. Die neuesten automatisierten Ergebnisse finden Sie weiter unten.

## Integrierte öffentliche MTProxy-Listen · 29. Oktober 2026

Dies ist der historische Testbericht der ursprünglichen, manuell ausgewählten Version. Informationen zu den aktuellen automatischen Pool- und IP-Modi finden Sie in[den Verbindungseinstellungen](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/#ip-modes). Die unten aufgeführten Zahlen und nicht unterstützten Funktionen beziehen sich auf diese getestete Version.

Es wurden ein gebündelter öffentlicher Snapshot sowie eine explizite HTTPS-Aktualisierung von SoliSpirit/mtproto und zakky8/mtproto-proxy-pro hinzugefügt. Auf diesem Host hat der Anwendungs-Downloader beide Feeds am 29. Oktober 2026 um 12:58 Uhr UTC erfolgreich abgerufen: **118 eindeutige kompatible Endpunkte** nach Filterung, Deduplizierung und der Begrenzung auf 64 Einträge pro Quelle. Dies bestätigt das Abrufen der Liste, nicht jedoch die Konnektivität oder die Nachrichtenübermittlung über diese Endpunkte. Während dieser Arbeiten war kein echtes Konto mit einem der aufgeführten Proxys verbunden. [Bedienungs- und Benutzerhandbuch](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/PROXIES.md).

Fehlgeschlagene, leere oder inkompatible Antworten der Quelle behalten frühere Einträge und Datumsangaben bei. Aktualisierungen ändern die ausgewählte Route nicht. Öffentliche Adressen werden validiert und aufgelöste IP-Adressen bei Auswahl fixiert; Betreiber- und manuelle Routen bleiben getrennt. Die Verbindungsprüfung ist nun im Bedienfeld vor der Kontoanmeldung verfügbar. Gefälschte TLS-Zertifikate und die automatische Proxy-Auswahl werden weiterhin nicht unterstützt. Der Betreiberkatalog hat Vorrang vor Abonnements.

- Vollständige Testsuite: **366 bestanden, 3 übersprungen**, 287,94 Sekunden. Vorhandene Abhängigkeitswarnungen und plattformbedingte Überspringungen bestehen weiterhin. Abschließende Regressionstests für öffentliche Listen/Lokalisierung: **36 bestanden**, einschließlich der Ablehnung ungültiger Download-Proxy-Ports; dies überschneidet sich mit der vollständigen Testsuite.
- Browser-Kompatibilität bestanden in Englisch/Russisch, Hell-/Dunkelmodus bei 390/1440 Pixeln: gebündelte Auswahlmöglichkeiten, kein Abruf externer Daten beim Öffnen der Einstellungen, explizite Aktualisierung, Beibehaltung von Routen und Cache bei Ausfällen, Überprüfung vor der Anmeldung, Isolierung des Arbeitsbereichs bei verzögerten Antworten, Angaben zur Quelle sowie Layout und Kontrast. Keine JavaScript-Fehler oder externen Browseranfragen.
- Die endgültige statische Übersetzungsabdeckung wurde für alle 13 Sprachversionen freigegeben; neue Texte wurden ins Russische übersetzt, wobei an anderen Stellen explizite englische Fallbacks vorgesehen sind. Der aktualisierte integrierte Leitfaden hat die Layout- und Kontrastprüfungen in beiden Designs bestanden.
- Ruff- und Veröffentlichungsprüfungen bestanden (259 öffentliche Dateien, 1.354 lokale Links); aktualisiert „Compose“ und CI-YAML wurden geparst. Docker und Remote-CI wurden hier nicht ausgeführt.
- Das neu erstellte Rad hat die Überprüfung der isolierten Installation, des Ladens der gebündelten Liste und des signierten Exports bestanden. Alle 69 Paketressourcen stimmten mit dem Arbeitsbereich überein; die Quell-Hashes wurden überprüft.

Belegnummern: `test-results/public-proxy-research/download-receipt.json`, `test-results/public-proxy-research/copy-receipt.json`, `test-results/public-proxies-full-suite.log`, `test-results/public-proxies-final-focused.log`, `test-results/public-proxies-browser/receipt.json` und `test-results/public-proxies-package.log`. Die Browser-, Konto- und Transportdaten sind fiktiv; die beiden oben genannten Feed-Downloads sind echte HTTPS-Anfragen.

## Präsentation der optionalen Zusatzfunktionen · 29. Oktober 2026

Die ehemalige Zielseite des „Proof“-Bots heißt nun **„Extras**“: eine kurze Übersicht, gefolgt von einer separaten Einrichtungsseite für die ausgewählte Option. Das Witness-Formular umfasst drei Schritte, wobei die Verbindungsverwaltung, die Netzwerkoptionen und die Bereitstellungsdetails ausgeblendet sind. GitHub ist ausdrücklich vorgesehen und erfordert kein Anmeldeformular. [Übersicht auf Russisch](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/EXTRAS.md).

- 30 gezielte Tests hinsichtlich Lokalisierung, Einrichtung von „Witness“ und Veröffentlichungsprüfungen wurden erfolgreich bestanden.
- Die Chromium-Einrichtungsprüfung wurde in Englisch/Russisch, Hell-/Dunkelmodus, bei einer Auflösung von 390/1440 Pixel bestanden: Tastaturfokus und Eingabetaste, keine impliziten Verbindungen bei der Auswahl von Zusatzfunktionen, Aufbewahrung von Entwürfen, festgesteckte Konfigurations-/Token-Downloads, Token-Löschung bei Sperrung sowie funktionierende Anker für lokale Anleitungen. Prüfungen des Layouts und des Textkontrasts vor einfarbigem Hintergrund bestanden.
- Die Akzeptanzprüfung beim Wechsel des Arbeitsbereichs wurde bestanden, einschließlich einer verzögerten Token-Antwort, die nach einem Wechsel eintrifft. Die Schnellnavigation ermöglicht das Auffinden der Zusatzfunktionen über die Suchbegriffe „Bot“, „Proof“ und „GitHub“; die bestehenden Prüfungen für 320/390/1440 Pixel sowie für Russisch und RTL wurden ebenfalls bestanden.
- Bei der Einrichtungsphase wurden keine JavaScript-Fehler oder externen Browseranfragen festgestellt. Es handelt sich hierbei um synthetische UI-Prüfungen, nicht um neue Live-Beweise aus Telegram oder Bot-Veröffentlichungen.
- Das endgültige Laden der Sprachen und die Wörterbuchabdeckung wurden für alle 13 Sprachversionen erfolgreich abgeschlossen, wobei außerhalb des Russischen explizite englische Fallbacks beibehalten wurden. Der erweiterte Proof-Leitfaden hat zudem die Layout- und Kontrastprüfungen bei 320/768/1440 Pixeln in beiden Designs bestanden.
- Das neu erstellte Tool hat die Isolationsprüfung und die Überprüfung des signierten Exports bestanden. Alle 67 gepackten Ressourcen stimmten mit dem Arbeitsbereich überein; das Quellarchiv enthält 253 öffentliche Dateien. Die Quellen-/Linkprüfung wurde für 1.346 lokale Dokumentationslinks erfolgreich abgeschlossen.

Quellennummern: `test-results/setup-browser/receipt.json`, `test-results/quick-navigation/receipt.json`, `test-results/extras-final.json`, `test-results/extras-package.log` und `test-results/extras-artifacts.json`. Die Screenshots stammen aus synthetischen Arbeitsbereichen.

## Prüfung der Einrichtung des Witness-Bots und des Proxys · 29. Oktober 2026

Die Witness-Einrichtung (jetzt unter **„Extras“ → „Ein Bot in Ihrem Kanal**“) bereitet einen unabhängig bereitgestellten Witness vor: festgesteckter Collector-Schlüssel, Token-Download mit begrenztem Geltungsbereich, eigener Kanal, Veröffentlichungsrichtlinie, HTTP/SOCKS5-Route und benutzerdefinierte Bot-API. Das Bot-Token verbleibt auf dem Witness-Host. Sein neuer „`--check-config`“ validiert die Konfiguration und Dateien, ohne eine Netzwerkverbindung herzustellen oder einen Schlüssel zu erstellen. JSON- Dateipfade werden neben der Konfiguration aufgelöst. Alle „Compose“-Witness-Varianten leiten nun die HTTP-Proxy- und Bot-API-Einstellungen weiter.

Die Kontoeinstellungen unterstützen einen vom Betreiber verwalteten öffentlichen MTProxy-Katalog, eine benutzerdefinierte Vorschau von Telegram-Proxy-Links sowie die vorhandenen manuellen Felder. Katalogantworten lassen vertrauliche Informationen weg; bei der Auswahl wird die Route im Workspace-Tresor gespeichert. Bei fehlenden oder fehlerhaften Katalogen bleiben manuelle Routen verfügbar. Es werden standardmäßig keine Projekt-Proxy-Adressen oder gehostete Witness-Dienste angelegt oder aktiviert. Ein Caddy-Beispiel gibt nur den bereichsgebundenen Head-Endpunkt frei, wenn ein externer Witness einen Collector erreichen muss, dessen Panel privat bleibt.

Validierung:

- Gesamtsuite: **348 bestanden, 3 übersprungen**, 195,81 Sekunden. Die Übersprünge sind auf Einschränkungen unter Windows zurückzuführen; die beiden bestehenden Warnungen bezüglich veralteter Abhängigkeiten bestehen weiterhin.
- Abschließender Regressionstest für Witness/Konfiguration/Release: **11 bestanden, 1 übersprungen**. Dies deckt sich mit der vollständigen Testsuite. Die Tests umfassen Pfadauflösung, Offline-Preflight, Signierung/Veröffentlichung über eine tatsächliche Loopback-HTTP-Bot-API-Fixture, aufgezeichnete Zustellungsfehler, Überprüfung des Kanal-Tokens und Ausschluss des Proxy-Geheimnisses.
- Chromium-Einrichtungsprüfung bestanden in Englisch/Russisch bei 390/1.440 Pixel: Festgesteckte Konfiguration und Token-Downloads, Token-Löschung beim Sperren, Katalogauswahl, Vorschau benutzerdefinierter Links gefolgt von explizitem Speichern, Layout/Kontrast sowie keine JavaScript-Fehler oder externe Browseranfragen. Der Überlauf bei der schmalen russischen Kontoüberschrift und auf der Anmelde-Registerkarte wurde korrigiert.
- Ruff, Quellen-/Link-Prüfungen sowie das Parsen der YAML-Datei für „Compose“ und den Workflow wurden erfolgreich bestanden.
- Das überarbeitete Tool hat Isolations-Installationsprüfungen, Überprüfungen der Panel-/statischen Ressourcen sowie API-Authentifizierungsprüfungen bestanden, sowie eine unabhängige Verifizierung von direkten und gestreamten synthetischen Exporten mit 32 Ereignissen.

Belegnummern: `test-results/setup-full-suite.log`, `setup-final-focused.log`, `setup-browser/receipt.json`, `setup-browser-final.log` und `setup-package.log`. Diese Überprüfungen nutzen synthetische Konten/Proxys und eine lokale Bot-API-Fixture. Sie erheben keinen Anspruch auf eine echte Bot-Veröffentlichung, einen funktionierenden öffentlichen MTProxy-Server, einen Remote-CI-Lauf oder eine Docker- Bereitstellung. Der oben aufgezeichnete reale Telegram-Beobachtungsverlauf bleibt ein separates Beweismittel. [Einrichtungsanleitung](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

## Präsentation und Überprüfung der Dokumentation · 29. Oktober 2026

Die Produktseite, der Anmeldebildschirm, die README-Dateien in Englisch und Russisch sowie die Präsentationsbilder weisen nun einen einheitlichen visuellen Stil auf. Öffentliche Screenshots verwenden fiktive Demodaten. Im Rahmen der Überarbeitung wurden zudem die oben stehenden veralteten Beschreibungen zur Live-Validierung und Wiederherstellung korrigiert.

- Gezielte Lokalisierung, Website- und Veröffentlichungstests: **33 bestanden, 1 übersprungen**. Der übersprungene Test erfordert die Erstellung eines Symlinks, was auf diesem Host nicht möglich ist.
- Die allgemeine Chromium-Panel-Zulassung wurde bestanden, einschließlich aller Sprachkataloge, des RTL-Layouts, der hellen/dunklen Designs, des ausreichenden Textkontrasts und des Wechsels zwischen Arbeitsbereichen. Die Überprüfung der Profilerstellung wartet nun auf die tatsächliche HTTP-Antwort, bevor der ausgewählte Arbeitsbereich überprüft wird.
- Die englischen und russischen Startseiten haben die Layout- und Kontrastprüfungen in beiden Designs bei 320, 390, 768, 850 und 1440 Pixel bestanden; die Schaltfläche „Absenden“ bleibt im anfänglichen Sichtbereich.
- Die Anpassung an öffentliche Websites wurde bei 320, 390, 768, 1024 und 1440 Pixeln erfolgreich getestet, einschließlich , Screenshot-Vergrößerung/Escape-Taste/Fokusrückgabe, Tastatur-Tabulator, Verweigerung der Zwischenablage, Projekt-Unterpfade, reduzierte Animationen und den Fallback ohne JavaScript. Es wurden keine fehlgeschlagenen Asset-Anfragen, externen Anfragen oder JavaScript-Fehler festgestellt.
- Das überarbeitete Tool hat eine isolierte Installationsprüfung bestanden: Panel-Ressourcen und Locales werden geladen, der API-Zugriff erfordert eine Authentifizierung, und direkte sowie gestreamte Exporte überprüfen unabhängig voneinander alle 32 synthetischen Ereignisse. Die Ruff-Prüfung sowie die Überprüfung öffentlicher Quellen und Links wurden erfolgreich bestanden.

Lokale Belege: `test-results/design-tests.log`, `design-panel-final.log`, `design-review-final.log`, `design-site.log` und `design-package/install-receipt.json`. Die gesamte Backend-Suite wurde für diese Änderung der Präsentation/Dokumentation nicht erneut ausgeführt; das vorherige Ergebnis bleibt im Audit vor der Veröffentlichung erhalten.

## Version 0.6.1

Version 0.6.1 enthält Änderungen an der Bedienoberfläche, den Startprogrammen, der Paketierung und der Dokumentation; der Code für die Erfassung, Speicherung, Signierung und den Export bleibt unverändert. Unter Windows 11 / Python 3.12.10 mit der festgesteckten Laufzeitumgebung:

- Die gesamte Suite hat **137 Tests** bestanden, wobei 2**Tests übersprungen wurden** und die bestehende Starlette-Warnung auftrat. Neue Tests umfassen die Behandlung von Strg+C durch den Launcher (der Server erhält 30 Sekunden Zeit für einen ordnungsgemäßen Abbruch) sowie behebbare Fehler bei den Einrichtungsschritten.
- Chromium (Headless-Shell 156) hat alle **45 allgemeinen Szenarien** und **35 Szenarien zum Kontoimport, QR-Code und Authentifizierungsschlüssel**, einschließlich der Kontrastprüfung bei Volltext, kein horizontaler Überlauf bei 320–1440 px und sichtbare Felder für die Erstanmeldung bei 320/390 px. Es wurden keine JavaScript-Fehler auf der Seite oder externe Anfragen festgestellt.
- `python start.py --setup-only` hat das Paket als Version 0.6.1 neu installiert und `python start.py --check` meldete, dass alles bereit sei. Ein echter `python -m tgwitness --demo`-Server gab das Panel, das Stylesheet, das Skript, das Logo, die Anleitung und `/api/status` in Version 0.6.1 zurück; der entfernte `workspace.css` gab einen 404-Fehler zurück.
- `Start.cmd` fand eine Python-Installation außerhalb des PATH. Da kein Python verfügbar war, wurde das Installationsangebot angezeigt; die manuelle Anleitung wurde abgelehnt und das Programm wurde mit 1 beendet. Beim Download-Schritt auf python.org wurde das Installationsprogramm 3.12.10 abgerufen und die Authenticode-Prüfung der Python Software Foundation bestanden; das Installationsprogramm selbst wurde auf diesem Host nicht ausgeführt.
- `start.sh` gab ohne Python-Ausgabe den Installationshinweis aus und beendete den Vorgang 1. `scripts\Docker.cmd` und `scripts/docker-start.sh` wurden an gefälschten `docker`-Ausführungsdateien getestet: korrekte Aufrufsequenz, Panel-Adresse und Token-Ausgabe sowie keine Erfolgsmeldung nach einem Fehler.
- `python tools/build_portable.py` erstellte ein 18,8 MiB großes Windows-Paket, nachdem die festgesteckte Prüfsumme der einbettbaren Laufzeitumgebung verifiziert worden war. Nach dem Entpacken in einen Pfad mit Leerzeichen und mit ausschließlich den Verzeichnissen „`C:\Windows`“ im PATH bestand das eingebettete Python die `TgWitness-Check.cmd`-Prüfung, stellte die Demo (32 Ereignisse) und einen Live-Arbeitsbereich bereit, und Chromium rendert das Protokoll und die Detailansicht ohne JavaScript-Fehler. Die Daten wurden in den Ordner „`data`“ des Pakets geschrieben.
- `python tools/build_preview.py` erzeugte ein Quellarchiv mit 110 Dateien. Ein Testlauf von `git add` listete dieselben 110 Dateien auf, ohne Sitzungs-, Schlüssel-, Datenbank-, Token-, Protokoll- oder Exportdateien, ohne lokale absolute Pfade und ohne Zeichenfolgen, die auf Geheimnisse hindeuten könnten.

In diesem speziellen Paketierungsdurchlauf vom 27. Oktober nicht durchgeführt: die automatische Python- Installation selbst, Docker-Build-/Compose-Prüfungen, Ausführungen unter Linux/macOS oder eine neue Übung mit einem Live-Konto . Echte Telegram-Beweismittel werden oben sowie in den früheren Kontoüberprüfungen unten aufgezeichnet. CI-Definitionen allein reichen nicht aus, um die Plattformausführung zu bestätigen.

## Version 0.6.0

Die neueste vollständige „Pinned-Runtime“-Suite unter Windows 11 / Python 3.12.10 bestand **135 Tests**, mit einem**Übersprung**, in 26,53 Sekunden und der bestehenden Starlette-Warnung. Das Überspringen erfordert POSIX-Berechtigungen. Nach Hinzufügen des QR- Renderers zu den Bereitschaftsprüfungen und Prozessmessungen wurden auch 8 betroffene Bereitschafts-/Arbeitsbereichsprüfungen bestanden.

Zu den neuen Funktionen gehören Telethon-Schemas 7/8, Pyrogram-Schemas 2/3, vollständige JSON-Schlüssel Schlüssel sowie reine Metadaten-JSON, übereinstimmende/widersprüchliche Kontodateien, TData-Passcodes, Manipulationen an Prüfsummen und unsichere Pfade, Offline-/authentifizierte In-Memory-Konvertierung, Online-Kont-ID-Prüfungen, QR-Erfolg/2FA/Ablauf, Stornierung veralteter Daten sowie Konto- Isolierung. TData-Fixtures verwenden eine separate AES-IGE-Implementierung zur Verschlüsselung.

Chromium hat **45 allgemeine Szenarien** sowie **35 Szenarien zum Kontoimport, zu QR-Codes und Authentifizierungsschlüsseln** bestanden, wobei keine JavaScript-Fehler auf den Seiten oder externe Anfragen festgestellt wurden. Neue Browserprüfungen decken alle vier Eingabeformate gemeinsam ab, darunter geschützte TData, API-Metadaten, QR-Darstellung, Ablauf/Wiederholungsversuche, 2FA, Ablehnung falscher Konten, Sperrung/Aufhebung des Arbeitsbereichs, responsives Layout sowie verspätete Konvertierungsantworten nach der Auswahl einer neueren Datei.

Beide Browser-Suiten bestanden den Test nach den Änderungen bei der Kontoeingabe erneut. Bei der Live-Einrichtung wird das Kontoformular geöffnet; im Demo-Modus wird das Beispielprotokoll angezeigt. Die Demo-Seite „Konto“ zeigt Anweisungen zum Live-Start an und verbirgt die Eingabefelder für Anmeldedaten. Gezielte Überprüfungen bei 320, 390 und 1.440 Pixeln bestätigten, dass das Zahlenfeld und die primäre Schaltfläche ohne Bildlauf passen, die API-Felder zunächst ausgeblendet sind und der Textkontrast lesbar bleibt. Die Steuerelemente für Erfassung und Verifizierung bleiben auch nach dem Öffnen ihrer neuen, erweiterbaren Abschnitte verdeckt.

Der direkte Auth-Key-Ablauf wurde mit synthetischen Anmeldedaten über die echten Import- und Autorisierungs-Endpunkte getestet. Die Prüfungen umfassen unvollständige Schlüssel, fehlende DC, ungenaue Benutzer-IDs, nicht übereinstimmende Kontoidentitäten, gespeicherte API-Anmeldedaten, sichtbaren Anfragefortschritt, das Löschen geheimer Daten sowie verspätete Antworten nach Bearbeitungen oder Methodenänderungen. Alle vier Anmeldemethoden wurden bei 320, 390 und 1.440 Pixeln geprüft. Die Dateiauswahl erfolgt vor der Formatierung, und die Schaltfläche „Verbinden“ passt in den anfänglichen 844-Pixel-Viewport, wobei die API-Einstellungen ausgeblendet sind. Bei diesem UI-Abnahmetest wurde keine echte Auth-Key-Autorisierung versucht.

Die Aktualisierung des Panels wurde erneut mit beiden Browser-Suiten überprüft: Es wurden keine JavaScript-Fehler auf der Seite oder externe Anfragen festgestellt. Die Konto-Suite umfasst nun das Einfügen eines API-ID-/Hash-Paares, das Zurückweisen fehlerhafter oder mehrerer Paare ohne Ersetzen von Feldern, eine ausschließlich auf Metadaten basierende Anleitung sowie das Ignorieren veralteter Importantworten nach einer Änderung der Anmeldemethode oder einer manuellen Bearbeitung der Anmeldedaten. Sechs zusätzliche gezielte Prüfungen wurden für die Einrichtungsanleitung, das explizite Starten/Pausieren, die Wiederherstellung bei leerer Suche sowie das endgültige Layout der Verbindung/lokalen Anleitung und einen soliden Textkontrast bei 320, 390 und 1440 Pixeln bestanden. Das Update für die direkte Anmeldung fügt einen einzelnen Vorgang zur Telefon-/Code-Anforderung hinzu und verwendet das im aktuellen Arbeitsbereich gespeicherte API-Paar für die Anmeldung per Telefon, QR-Code und Sitzung wieder. Die oben genannte vollständige Python- Suite umfasst neue Tests zur Persistenz, zur Ablehnung unvollständiger Anmeldedaten sowie zur Isolierung von Arbeitsbereichen. Die Browserprüfungen umfassen die direkte Telefoneingabe, die Wiederverwendung gespeicherter Anmeldedaten, das Routing ausschließlich anhand von Metadaten, die Dateiautorisierung per Knopfdruck sowie die Ablehnung doppelter Konten. Die vereinfachten Formulare für Panel-Token und Telefonnummern wurden ebenfalls ohne anfängliches Scrollen bei 320, 390 und 1440 Pixeln geprüft. Eine Kompatibilitätsprüfung bestätigte, dass das Formular für die direkte Telefonnummerneingabe die früheren Konfigurations- und Code-Endpunkte nutzen kann, während ein älterer Prozess noch läuft.

Ein vom Nutzer bereitgestelltes Konto wurde separat, außerhalb der öffentlichen Testumgebungen, überprüft. Die Eingaben „Telethon“, „Pyrogram“ und „TData“ führten zu derselben Autorisierung; die begleitende JSON-Datei lieferte die API-Anmeldedaten. Alle vier Dateien wurden über das 0.6.0-Panel geladen, und Telegram bestätigte die erwartete numerische Konto-ID. Die Quelldateien blieben unverändert. Es wurden keine Quellen ausgewählt, und die Beobachtung blieb deaktiviert. Dies stellt ein Beispiel für einen Import/eine Anmeldung dar, nicht jedoch für eine Live-Erfassung, -Wiederherstellung oder -Kapazität.

Telegram hat zudem einen echten QR-Token ausgegeben, der jedoch ohne Scannen ungültig gemacht wurde. Die vollständigen QR-Bestätigungs- und 2FA-Abläufe wurden mit synthetischen Clients getestet; die mobile Bestätigung über eine echte Telegram-App bleibt ein separater Akzeptanzschritt. In den öffentlichen Dateien sind keine echten Konto-Identifikatoren, Geheimdaten oder Screenshots enthalten.

Das Launcher-Upgrade wurde abgeschlossen; Quellcode, installierte Metadaten und Bereitschaftsmarker weisen die Version 0.6.0 auf, mit QR-Code 8.2 und einem bestandenen `pip check`-Test. Das installierte Wheel stellte das Bedienfeld und die Anleitung bereit, wies nicht authentifizierte API-Anfragen zurück und überprüfte unabhängig direkte sowie gestreamte synthetische Exporte mit 32 Ereignissen. Die aktualisierte Offline-Anleitung wurde bei 320, 390 und 1.440 Pixeln überprüft. Öffentliche Screenshots sind weiterhin synthetisch.

Die Quellcode-Veröffentlichung enthält 107 Dateien auf der Zulassungsliste. Links zur lokalen Dokumentation sind funktionsfähig. Die Ausführung mit Docker/Caddy, die Remote-CI- und Paketveröffentlichung, die ARM64-Laufzeitumgebung, die kontinuierliche Datenerfassung sowie die vollständige Live-Telegram-Akzeptanzmatrix werden hier noch nicht abgedeckt.

## Version 0.5.1

Unter Windows 11 / Python 3.12.10 wurde die gesamte Projektumgebungssuite erfolgreich durchlaufen: **94 Tests bestanden, 2 übersprungen**, in 31,21 Sekunden, mit der bestehenden Starlette-Warnung. Die übersprungenen Schritte erfordern POSIX-Berechtigungen und die Erstellung von Symlinks, die auf diesem Host nicht verfügbar sind. Die HTTP-Download-Fixture gab eine Diagnose des Request-Threads aus; alle Assertions wurden bestanden. Dieser Durchlauf schließt Probleme beim Host-Transport nicht aus.

Neue Regressionsprüfungen umfassen abgelehnte StringSession-Instanzen, Code- und 2FA-Kontoänderungen, abgebrochene Identitätsabfragen, ausstehende Anmeldeabbrüche sowie Aktualisierungen über registrierte Handler auf aktiven, abgelehnten, ersetzten und Test-Clients. Nur der aktive Collector liefert Ereignisse; gespeicherte Anmeldedaten und der signierte Verlauf bleiben unverändert. Weitere neue Prüfungen umfassen die Unicode-Suche nach der Wiedereröffnung einer Datenbank, die Einbeziehung von Grenzen der Überwachungsrichtlinien in die Abdeckung sowie Ausschlüsse bei der Paketierung aus öffentlich zugänglichen Quellen.

Das eigentliche Projekt „`pythonw.exe`“ startete ein isoliertes synthetisches Panel, gab den HTTP-Status 200 zurück und speicherte die Startdiagnose in „`logs/server.log`“. Das Protokoll enthielt weder das generierte Panel-Token noch HTTP-Zugriffsaufzeichnungen. Der Test beendete lediglich seinen eigenen synthetischen Prozess. Es wurde keine Aufgabe im Task-Scheduler registriert; An- und Abmeldung, Ruhezustand und Dienstwiederherstellung bleiben separate Prüfkriterien.

Die Chromium-Akzeptanzprüfung wurde **in 45 Szenarien** bestanden, wobei keine JavaScript-Fehler auf den Seiten und keine externen Anfragen festgestellt wurden. Neue Prüfungen umfassen Datums- und Zeitangaben auf der Zeitleiste mit einer Auflösung von 601/768/850 Pixeln, Anhang-Entwürfe bei Statusaktualisierungen, neuere Bearbeitungen während des Speichervorgangs, gelöschte Verifizierungsergebnisse beim Kontowechsel, verspätete Verifizierungsantworten nach dem Wegwechseln und Zurückkehren sowie explizite Verifizierungsgrenzen bei Eintreffen neuer Ereignisse. Zudem wurden der Abstand zwischen Suchsymbol und Text korrigiert und die Browser-Suite erneut ausgeführt.

Der Browser-Lauf nutzte die in `.venv` festgelegte Laufzeitumgebung sowie das vorhandene, vom System bereitgestellte Playwright 1.62.0/Chromium, das dem Importpfad der Projektumgebung angehängt wurde. Eine optionale Installation von Entwicklungsabhängigkeiten wurde während eines langsamen Playwright- Downloads abgebrochen; es wurde keine neue Version des Browser-Tools qualifiziert. Ein normaler „`python start.py --setup-only`“-Lauf schloss das Anwendungs-Upgrade ab. Quellcode, installierte Metadaten und der Marker-Bericht des Launchers 0.5.1; „`pip check`“ wurde bestanden. Die Bereitschaftsprüfungen wurden auf einem neuen, unbenutzten Pfad bestanden, wobei die erwartete Warnung bezüglich des lokalen Tresorschlüssels bestehen blieb.

Das Wheel der Version 0.5.1 wurde separat installiert und einem Smoke-Test unterzogen: Alle Panel-/Guide-Assets wurden bereitgestellt, nicht authentifizierter API-Zugriff wurde abgelehnt, und sowohl direkte als auch gestreamte 32-Ereignis-Beweis-ZIP-Dateien bestanden die unabhängige Überprüfung. Die Anwendungsdateien im installierten Paket wurden mit dem Quellcode abgeglichen. Das öffentliche Quellcode-Archiv verwendet eine explizite Zulassungsliste für Dateitypen und lehnt verknüpfte Quelldateien ab; Laufzeitmaterial, das in Quellcode-Verzeichnissen abgelegt wurde, wird durch Regressionstests ausgeschlossen.

Während des Code-Fix-Durchlaufs umfassten die Auswahl aus öffentlichen Quellen und der Git-Kandidatensatz 86 Dateien, wobei keine Laufzeitdatenverzeichnisse enthalten waren. Ein Scan nach erkennbaren Mustern für private Schlüssel, GitHub-Token, Telegram-Bot-Token und StringSession ergab keine Übereinstimmungen. Hierbei handelt es sich um eine begrenzte Musterprüfung, nicht um eine umfassende Überprüfung vertraulicher Daten. Die Prüfungen anhand von Ignorierregeln decken zwölf gängige Artefakte aus den Bereichen Konto, Daten und Export ab. Die YAML-Dateien für Workflow, Issue und Compose sowie das Windows- Aufgabenskript wurden erfolgreich geparst. Links zu lokaler Dokumentation sind auflösbar.

Alle sieben Feststellungen aus der Überprüfung vom 27. Oktober werden behandelt. Die Ausführung des GitHub- Workflows, die Laufzeitumgebung unter Linux/macOS/Docker, die Interoperabilität mit echtem Telegram sowie mit externen Proxys und TSA sowie die Qualifizierung unter Dauerbelastung bleiben im Rahmen dieses lokalen Durchlaufs unberücksichtigt. Es wurden weder eine Repository-Veröffentlichung noch eine Dienstregistrierung noch eine Erfassung echter Konten durchgeführt.

### Aktualisierung der englischen Dokumentation

Die README-Datei, die Referenz zu Konten und Sitzungen, der Erfassungsablauf sowie das mitgelieferte Handbuch beschreiben nun die unterstützten Eingaben, das Verhalten im Arbeitsbereich, Ereignisrichtlinien und Exportformate auf Englisch. Die drei öffentlich zugänglichen Screenshots wurden unter Verwendung synthetischer Daten aktualisiert. Zu diesem Zeitpunkt umfasste die öffentlich zugängliche Auswahl 88 Dateien, einschließlich der beiden neuen Handbücher. Alle 131 lokalen Links in 23 Markdown-Dokumenten sind funktionsfähig.

Nach den Anpassungen an der Benutzeroberfläche und der Anleitung hat die Chromium-Akzeptanzprüfung erneut alle 45 Szenarien bestanden, wobei keine JavaScript-Fehler auf den Seiten und keine externen Anfragen festgestellt wurden. Die vollständige Python-Testsuite wurde für diese Aktualisierung der Dokumentation und Präsentation nicht erneut ausgeführt; das oben genannte Ergebnis mit 94 bestandenen Tests stammt aus dem vorangegangenen Durchlauf zur Behebung von Codefehlern.

Das überarbeitete Modul wurde in eine neue, isolierte Testumgebung integriert. Seine Panel- und Führungs-Komponenten funktionierten einwandfrei, nicht authentifizierter API-Zugriff wurde abgelehnt, und sowohl direkte als auch gestreamte Exporte bestanden die unabhängige Überprüfung von 32 synthetischen Ereignissen.

### Aktuelles zur Installation und Bereitstellung

Die gezielten Installations-, Paketierungs- und Bereitschaftsprüfungen bestanden **14 Tests**, wobei ein Test aufgrund der nicht verfügbaren Erstellung eines Symlinks übersprungen wurde. Native-Wrapper-Prüfungen decken Pfade mit Leerzeichen, die Weiterleitung von Argumenten, Setup-/Demo-Modi sowie die Weitergabe von Beendigungscodes ungleich Null ab. Git-Bash-Prüfungen testen den Docker-Shell-Helper mit einem simulierten Daemon, einschließlich fehlendem Docker, fehlendem Compose, fehlgeschlagener Zustandsüberprüfung und einem erfolgreichen Start über einen alternativen Port. Diese simulierten Prüfungen stellen keine Docker-Laufzeitkompatibilität sicher.

Eine vollständige Kopie aus öffentlichen Quellen wurde in einem neuen Windows-Verzeichnis installiert, dessen Pfad Leerzeichen enthält. `scripts\Setup.cmd` erstellte eine neue Umgebung und installierte die angeheftete Laufzeitumgebung; `Start.cmd --check --json` meldete sich als bereit, ohne sein Zieldatenverzeichnis zu erstellen. `pip check` bestand den Test. Das neu erstellte „Wheel“ bestand ebenfalls die Prüfung der installierten Pakete, einschließlich direkter und gestreamter 32-Ereignis-Exporte.

Shell-Syntax und fünf Workflow-/Compose-YAML-Dateien wurden analysiert. Die Compose-Konfigurationen für Quellcode und Bilder stimmen hinsichtlich der Speicher- und Laufzeiteinstellungen überein. Zu diesem Zeitpunkt wurden alle 139 lokalen Links in 23 Markdown-Dokumenten aufgelöst. Die Auswahl aus öffentlich zugänglichen Quellen umfasst 99 Dateien.

Die CI-Definitionen umfassen nun eine neue native Einrichtung unter Windows/Linux/macOS, die Überprüfung des Zustands von Compose, der Zugriffskontrolle und der Persistenz bei der Neuerstellung von Containern sowie die Caddy-Konfiguration. Der Release-Workflow macht die Veröffentlichung von diesen Prüfungen abhängig und fügt einen emulierten ARM64- Smoke-Check hinzu. Docker ist auf diesem Host nicht verfügbar: Die eigentliche Ausführung von Compose/Caddy, die Zertifikatsausstellung, die ARM64-Ausführung sowie die Veröffentlichung von Remote-Workflows und -Paketen bleiben lokal uneingeschränkt möglich. Der Anwendungs- und UI-Code blieb von diesem Update unberührt; die früheren vollständigen Python- und Browser-Tests wurden nicht erneut ausgeführt.

## Version 0.5.0

Die vollständige „Pinned-Runtime“-Suite wurde bestanden: **81 bestanden, 1 übersprungen**, in 22,00 Sekunden, mit der bestehenden Starlette-Warnung. Die POSIX-Berechtigungsprüfung wird unter Windows übersprungen. Die neuen Handler-Tests senden Nachrichten, Bearbeitungen, bereichsbezogene/nicht bereichsbezogene Löschungen, Reaktionen, Teilnehmeraktualisierungen und Mitgliedschaftsdienst-Nachrichten durch verschiedene Richtlinien. Deaktivierte Kategorien erzeugen keine entsprechenden Live-Beobachtungen; Abdeckungsdiagnosen und explizite Momentaufnahmen bleiben verfügbar. Die Tests überprüfen die dauerhafte Richtlinie, die Trennung von Arbeitsbereichen, signierte Vorher-Nachher-Prüfprotokolle, das Verhalten bei unveränderter Richtlinie, die strenge Validierung sowie die Einbeziehung in den nächsten Prozessbeleg.

Demo-Zugriffstests bestätigen, dass sich dessen Funktionsumfang vom konfigurierten Panel-Token unterscheidet: Er kann keinen Live-Arbeitsbereich autorisieren, keine Erfassungseinstellungen ändern und wird nicht für Remote-, weitergeleitete, domänenübergreifende oder ungültige Host-Anfragen ausgestellt oder akzeptiert. Das Öffnen einer gespeicherten Demo ohne das explizite Demo-Flag aktiviert keinen automatischen Eintrag.

Die Chromium-Akzeptanzprüfung bestand **39 Szenarien**, darunter den lokalen Demo-Zugriff ohne Token-Eingabe, Überwachungsvoreinstellungen, den Übergang von der Quellenauswahl zur Richtlinie, die Unabhängigkeit pro Konto sowie Layout- und Textkontrastprüfungen für Desktop/320/390 Pixel. Es traten keine JavaScript-Fehler auf den Seiten auf. Die vom Host über AdGuard eingefügten Anfragen bleiben im Protokoll erhalten. Die HTTP-Testumgebung für den Download protokollierte einen Verbindungsabbruch, nachdem ein Client seine Verbindung geschlossen hatte; die Prüfungen wurden dennoch bestanden. Dies ist kein Ergebnis aus dem Live-Betrieb.

Der Standard-Launcher hat die isolierte Umgebung auf Version 0.5.0 aktualisiert; Quell- und installierte Versionen stimmen überein, und der pip-Check wurde bestanden. Die bestehende Verschlüsselung des Secret-Vaults, die Ablehnung falscher/fehlender Schlüssel sowie die Prüfungen auf Manipulationen an Signaturen und Medien wurden in der vollständigen Testsuite bestanden. Es wird keine neue Anwendungsverschlüsselung von Nachrichteninhalten oder Anhängen beansprucht.

Die lokale Demo wird neu gestartet, um die aktualisierte Benutzeroberfläche verfügbar zu machen. Vorhandene synthetische Datensätze bleiben erhalten; das Beenden des alten Demo-Hintergrundprozesses führt beim nächsten Start zu einer Offline-Grenze. Für diese Überprüfungen wird keine echte Telegram-Sitzung verwendet.

Das auf localhost:8787 ausgeführte Panel zeigte die Version 0.5.0, automatischen Demo-Zugang, die fünf Überwachungselemente sowie 33 gespeicherte synthetische Protokollereignisse an. Das separat installierte 0.5.0-Wheel stellte alle Panel-/Anleitungsressourcen bereit, lehnte nicht authentifizierte API-Zugriffe ab und erzeugte eine verifizierte ZIP-Datei mit 32 Ereignissen sowohl direkt als auch über den Streaming- Download-Helper. Die Versionen der Laufzeitpakete bleiben wie für 0.4 aufgezeichnet fixiert.

## Version 0.4.0

Die vollständige „Pinned-Runtime“-Suite wurde bestanden: **78 bestanden, 1 übersprungen**, in 19,77 Sekunden. Die übersprungene Prüfung erfordert POSIX-Berechtigungen; die Verwahrnungswarnung des Upstream-Starlette-TestClients besteht weiterhin. Neue Tests decken gestreamte Downloads/Workspace-Weiterleitung, Autorisierungs-Header, Verweigerung des Überschreibens, Weiterleitungen, verkürzte Antworten, angekündigte/tatsächliche Größenbeschränkungen, begrenzte Lesevorgänge, Bereinigung, Dateisysteme ohne Hardlinks, Bereitschaftsfehler sowie Launcher-Modi ab, in denen keine Pakete installiert werden dürfen. Exporttests bestätigen die Existenz von arbeitsbereichslokalen temporären Dateien und die selektive Bereinigung verwaister Dateien.

Die Chromium-Akzeptanzprüfung hat alle 36 aufgeführten Szenarien ohne JavaScript-Fehler auf der Seite bestanden. Es testet simulierte Anmeldungen per Telefon/Code/2FA, konvertierte Sitzungen, zwei Arbeitsbereiche sowie separate Routen/Zustände, Beobachtungen, Signaturen, Kontrollpunkte und Zeitstempelanfragen, außerdem:

- Layouts für Desktop und 320/390 Pixel, kein horizontaler Überlauf, sichtbare Navigation und das erste Anmeldefeld innerhalb des anfänglichen 844-Pixel-Viewports.
- Solider Textkontrast vor dem Hintergrund gemäß den WCAG-AA-Schwellenwerten für Text. Deaktivierte Steuerelemente, Deckkraft sowie Bild- und Farbverlaufshintergründe werden nicht berücksichtigt; es handelt sich hierbei nicht um eine vollständige WCAG-Prüfung.
- Eine echte lokale Exportantwort, die über einen simulierten OS-Dateiauswähler/Schreibzugriff erstellt wurde, gefolgt von einer unabhängigen ZIP-Überprüfung; bei Abbruch wird keine Exportanfrage gesendet.
- Ein Schreibfehler bricht die Übertragung zum Ziel ab; der 128-MiB-Fallback lehnt eine übergroße angekündigte Antwort ab, ohne eine entsprechende Nutzlast zuzuweisen.
- Der englische lokale Leitfaden für den Desktop und beide schmalen Bildschirmbreiten.

Der OS-Speicherdialog und die tatsächlichen Browser-Schreibvorgänge im Multi-Gigabyte-Bereich wurden weder automatisiert noch qualifiziert. Python-Download-Tests verwenden begrenzte Blöcke und Loopback-Fixtures. Die vollständige Abnahme der Bereitstellung mit echtem Telegram erfolgt separat.

Das Standard-Installationsprogramm hat `.venv` auf 0.4.0 aktualisiert. Quellcode und installierte Metadaten stimmen überein; `pip check` wurde erfolgreich geprüft. `python start.py --check --json` meldete sich auf einem neuen synthetischen Pfad als bereit, ohne das Datenverzeichnis anzulegen. Die Warnung bezüglich der lokalen Schlüsselspeicherung bleibt zu Recht bestehen: Journale und Medien werden von der Anwendung nicht verschlüsselt.

Das Wheel der Version 0.4.0 wurde erstellt und in einem separaten Verzeichnis installiert. Alle 23 Anwendungsdateien stimmen Byte für Byte mit dem Quellcode überein. Das installierte Paket stellte das Bedienfeld und die englische Anleitung/Ressourcen bereit, wies nicht authentifizierte API-Zugriffe zurück und exportierte eine synthetische ZIP-Datei mit 32 Ereignissen, die die Überprüfung bestand. Sein Befehl zum Streaming-Download holte zudem eine unabhängig verifizierte ZIP-Datei aus der laufenden, installierten Anwendung ab.

Die öffentliche Dokumentation und der lokale Leitfaden sind in englischer Sprache verfasst; die Links zur lokalen Dokumentation funktionieren. PowerShell hat die Windows-Aufgabenvorlage analysiert und Python die macOS- Plist-Datei. Hierbei handelt es sich um Syntaxprüfungen, nicht um die Ausführung von Diensten. Es wurde keine Aufgabe/kein Dienst registriert. Die CI-Konfiguration umfasst nun Bereitschaftsprüfungen, jedoch wurde die Remote-CI hier noch nicht ausgeführt.

Beim erneuten 0.4-Browserlauf wurden erneut eine AdGuard-Einblendung auf dem Host sowie ein „OSError 10022“ bei der asyncio-Socket-Bereinigung unter Windows festgestellt. Die Browser-Prüfungen wurden bestanden; diese Umgebungsbeobachtungen werden beibehalten und nicht als feststehendes Anwendungsverhalten behandelt. Erste Sandbox-Versuche mit OpenSSL, dem Browser und pip schlugen fehl; die erfolgreichen Qualifizierungsläufe nutzten eine genehmigte Ausführung außerhalb der Sandbox.

## Version 0.3.1 mit Schwerpunkt auf Fehlerbehebungen zur Betriebsbereitschaft

Die betroffenen Launcher-, Evidenz-/Speicher- und API-Prüfungen wurden bestanden: **31 bestanden, 1 übersprungen**, eine Starlette-Warnung auf Upstream-Ebene. Die übersprungene Prüfung überprüft POSIX- Verzeichnisberechtigungen und kann diese Berechtigungen auf diesem Windows-Host nicht feststellen. Der alte Python-Test simuliert die Versions-/Importgrenze; es war kein Python-3.10-Interpreter installiert oder qualifiziert. Die zuvor bestandene 0.3-Suite ist unten aufgeführt; die gesamte Suite und die Browserszenarien wurden für diese gezielten Änderungen nicht erneut ausgeführt.

Der normale Launcher hat die lokale Umgebung auf Version 0.3.1 aktualisiert; Quell- und installierte Metadaten stimmen überein, und der pip-Check wurde erfolgreich bestanden. Ein separat installiertes 0.3.1-Wheel stellte das Panel und die Assets bereit, lehnte nicht authentifizierten API-Zugriff ab und erzeugte einen verifizierten synthetischen Export mit 32 Ereignissen. Die Workflow-YAML-Datei wurde geparst, doch die neue Container-Laufzeitprüfung wurde nicht ausgeführt: Es stand keine verwendbare lokale Docker-/Podman-/Linux-Laufzeitumgebung zur Verfügung.

Siehe [die Ergebnisse der Bereitschaftsprüfung](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) hinsichtlich verbleibender Lücken in den Bereichen Benutzerfreundlichkeit, Live-Service und Plattform. Dieser Patch erweitert die Unterstützung auf keine weiteren Betriebssysteme.

## Version 0.3.0

Die vollständige „pinned-runtime“-Suite hat bestanden: **61 Tests**, mit einer Verwahrlosungswarnung für den Upstream-Starlette TestClient. Die Laufzeit-Metadaten melden TgWitness 0.3.0 und python-socks 2.8.2; der pip-Check wurde bestanden. Der Browser-Akzeptanztest wurde ohne JavaScript-Fehler auf der Seite bestanden.

Das 0.3.0-Wheel wurde erstellt und in einem separaten Paketverzeichnis installiert. Es stellte das Dashboard und die Ressourcen bereit, wies eine nicht authentifizierte API-Anfrage zurück und exportierte ein synthetisches Protokoll mit 32 Ereignissen, das eine unabhängige Überprüfung bestand. Lokale Dokumentationslinks sind funktionsfähig. Nach der Korrektur der MTProxy-Bare-Key-Normalisierung wurden alle neun Verbindungs- und Sicherheitstests erfolgreich erneut durchgeführt.

Zu den neuen Inhalten gehören:

- SOCKS5-Benutzername/Passwort und HTTP CONNECT über tatsächliche Loopback-Testserver; ein nicht mehr funktionierender konfigurierter Proxy schlägt fehl, anstatt auf das Ziel zurückzugreifen.
- Proxy-Validierung, Auswahl des MTProxy-Transportprotokolls, Ablehnung gefälschter TLS-Ee-Geheimnisse, Persistenz, Isolierung des Arbeitsbereichs, Ablehnung von Änderungen während der Beobachtung sowie Ausschluss von Geheimnissen aus API-Statusmeldungen und signierten Ereignissen.
- Schreibgeschützte Konvertierung der synthetischen Telethon-SQLite-Schemas 7 und 8; unveränderter Quell-Hash; Ablehnung anderer Formate, SQL-Ansichten und einer ausstehenden WAL-Datei.
- Externer Hauptschlüssel für den Tresor: verschiedene abgeleitete Arbeitsbereichsschlüssel, erfolgreiches Wiederöffnen, Ablehnung bei falschem/fehlendem Schlüssel sowie keine implizite Migration bestehender lokaler Tresore.
- Proxy-Einstellungen im Browser, Löschen von Anmeldedaten, Offenlegung von Speicherschutzmaßnahmen, Seite zur mobilen Verbindung, Autorisierung von konvertierten Sitzungsdateien, separate Routen sowie alle zuvor behandelten Erfassungs- und Export-Szenarien mit einem gefälschten Telegram-Client.

Während der Entwicklung wartete ein Loopback-Test unbegrenzt auf das Herunterfahren des Peers; bei einem weiteren Durchlauf wurde nach dem Handshake ein Verbindungsabbruch unter Windows beobachtet. Die Testumgebung begrenzt nun den gesamten Datenaustausch und behandelt EOF/Reset nach einem abgeschlossenen Handshake als Verbindungsabbruch. Assertions für den Handshake und die Authentifizierung sind weiterhin erforderlich. Dies gilt nicht für echte Proxy-Anbieter und deutet auch nicht auf einen festen Fehler im Telegram-Transport hin.

Die unten beschriebene Beobachtung der AdGuard-Anfrage gilt weiterhin. Es wurde kein echtes Telegram-Konto, kein externer SOCKS-/HTTP-Proxy und kein Live-MTProxy-Server verwendet. MTProxy befindet sich im Versuchsstadium, und es wurden lediglich die ausgewählten Optionen sowie die Validierung der geheimen Schlüssel überprüft, nicht jedoch die Interoperabilität im Live-Betrieb. Neue Befehle zur Konvertierung von externen Schlüsseln und Sitzungen wurden ausschließlich mit synthetischen Geheimnissen getestet. Linux/macOS/Docker sind hier weiterhin nicht geprüft.

Die unten aufgeführte Durchsatzmessung für Version 0.2 wurde nicht wiederholt und darf nicht als neuer Multi-Account-/Proxy-Benchmark für Version 0.3 dargestellt werden.

## Ausgangsversion 0.2.0

Getestet unter Windows mit Python 3.12.10. Es wurde kein echtes Telegram-Konto verbunden.

| Überprüfen | Ergebnis |
| --- | --- |
| Python-Suite | 52 Tests bestanden in der Entwicklungsumgebung und 52 Tests bestanden mit der festgelegten Laufzeitumgebung; jeweils eine Warnung bezüglich der Veralterung des „Starlette TestClient“ im Upstream bei jedem Durchlauf |
| JavaScript-Syntax | Mit Node.js umgesetzt |
| Chromium-Kompatibilität | Bestanden; keine JavaScript-Fehler auf der Seite |
| Layout für Desktop und Mobilgeräte | Geprüft bei 1440 × 1060 und 390 × 844; kein horizontaler Dokumentüberlauf |
| Nachrichteninhalt im HTML-Format | Als Text dargestellt; das eingefügte Skript wurde nicht ausgeführt |
| Beispiel für einen Account-Ablauf | API-Anmeldedaten → Telefon → Code → 2FA → Gruppe auswählen → Start → Momentaufnahme → Pause → Neu laden |
| Beweismaterial im Browser | Bearbeitungsvergleich, vorheriger Inhalt nach Löschung, Filter, ZIP-Download, Checkpoint, signierte Prozessbestätigung, Download von RFC 3161-Anfragen und Checkpoint-Verknüpfung |
| Mehrere Konten | Getrennte Protokolle, Schlüssel, Quellen und Live-Zustände; beim Wechseln des Browsers läuft der andere Collector weiter; Arbeitsbereiche werden nach einem Neustart wieder geöffnet; doppelte Konten und die Neuzuweisung von Konten werden abgelehnt |
| Kryptografische Fehler | Geänderte signierte Felder, hinzugefügte nicht signierte Felder, falscher Schlüssel, beschädigtes Archivelement, geänderte/fehlende Medien, durch Checkpoint erkannte, abgelehnte Verkürzung |
| Speicherung | Gleichzeitige Einträge werden verifiziert; Aktualisierungen oder Löschungen führen zur Ablehnung; beim Start wird ein geändertes Protokoll ohne nachträglichen Eintrag abgelehnt und die Sperre aufgehoben |
| Dauerhaftigkeit der Medien | Atomare Nachrichten-/Auftragsschreibvorgänge; Wiederherstellung nach Neustart; Beibehaltung der Deskriptoren der Originalversion; Ablehnung von Warteschlangenersetzungen und Beschädigungen bestehender Dateien; „FloodWait“ beibehalten; Isolierung von Quellfehlern |
| Streaming | Ein stabiles Präfix wird exportiert, während neue Einträge angehängt werden; ein gespeicherter Kontrollpunkt erkennt ein verkürztes Protokoll; der Export gibt nicht den gesamten Ereignisstrom wieder. |
| RFC 3161 | OpenSSL 3.5.9 liest generierte Anfragen; lokal generierte synthetische CA/TSA-Antworten werden akzeptiert; veränderte Daten, Nonces und falsche Zertifizierungsstellen werden abgelehnt; die umgebende CA-Umgebung hat keinen Vorrang vor explizitem Vertrauen |
| Lokale Einrichtung | start.py --setup-only hat die isolierte .venv-Umgebung auf Version 0.2.0 aktualisiert; Quellcode und installierte Metadaten stimmen überein; pip-Prüfung erfolgreich bestanden |
| Wheel | Version 0.2.0 wurde erstellt und separat unter „test-results“ installiert; stellte Panel/Assets bereit, wies nicht authentifizierte API-Anfragen zurück, exportierte und verifizierte ein synthetisches Archiv mit 32 Ereignissen |

Bei den Quelltests kamen FastAPI 0.159.1, Uvicorn 0.54.0, Telethon 1.45.0, cryptography 50.0.2, pytest 9.1.1 und Playwright 1.62.0 zum Einsatz. Die festgelegte Laufzeitumgebung verwendet FastAPI 0.162.0, Starlette 1.10.0, Uvicorn 0.54.0, Telethon 1.45.0 und Cryptography 50.0.2. In der Datei „deploy/constraints.txt“ sind die festgelegten Laufzeitversionen vermerkt; die Dateien „deploy/requirements.lock“ und „deploy/build.lock“ enthalten den SHA-256-Hash jeder Paketdatei, und Docker sowie Server mit hoher Sicherheitsstufe führen Installationen ausschließlich anhand dieser Dateien durch (pip --require-hashes). Beides stellt keinen Nachweis für die Kompatibilität auf jeder konfigurierten CI-Plattform dar. Die Remote-CI wurde noch nicht ausgeführt.

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

## Umgebungsbeobachtungen

Einschränkungen der Windows-Sandbox blockierten die standardmäßigen temporären Verzeichnisse von pytest/pip sowie den Playwright-Unterprozess. Pytest verwendete ein neues temporäres Verzeichnis innerhalb des Projekts; Installations- und Browserprozesse erforderten eine genehmigte Ausführung außerhalb der Sandbox.

AdGuard hat auf dem Rechner Anfragen an local.adguard.org in den Browser eingefügt. Der Browser-Verlauf speichert diese Anfragen. Dieser Durchlauf ist **kein** Beweis dafür, dass in einer unveränderten Browserumgebung keinerlei ausgehende Anfragen stattfinden; die App-Quelle selbst enthält keine externen Asset-/CDN-/Analytics-Anfragen. Die AdGuard-Einstellungen wurden nicht geändert.

Beim abschließenden Browserlauf wurde zudem ein Windows-asyncio-Socket-Cleanup-OSError 10022 protokolliert. Alle Browser-Prüfungen wurden bestanden, und es traten keine JavaScript-Fehler auf der Seite auf. Die Ursache konnte nicht ermittelt werden, und dieser Lauf belegt nicht, dass keine Probleme mit dem Host-Transport vorliegen.

Die erste HTTP-Prüfung des installierten Pakets unter Verwendung der „connection-close“-Anfragen von urllib führte sowohl innerhalb als auch außerhalb der Sandbox und bei beiden Abhängigkeitssätzen zu Verbindungsabbrüchen. Die abschließende Prüfung nutzte standardmäßige persistente HTTP/1.1-Verbindungen über http.client und war erfolgreich. Auch die Browser-Anfragen bestanden den Test. Die genaue Ursache der Verbindungsabbrüche konnte nicht ermittelt werden; sie wurden nicht als behobener Anwendungsfehler eingestuft.

## Verbleibende Qualifizierung

Das gespeicherte Live-Protokoll dokumentiert tatsächliche Erfassungen, Bearbeitungen, Löschmeldungen, Anhänge, Nachprüfungen sowie die Handhabung von Ratenbeschränkungen. Es dokumentiert jedoch nicht die vollständige Zustellung oder eine kontrollierte Matrix aus Sichtbarkeitsrollen, Reaktionsakteuren, verlängerten „FloodWait“-Zeiten, Kontosperrungen und der Wiederherstellung nach Netzwerk- oder Prozessunterbrechungen. Die Ausgabe von QR-Token bleibt von der abgeschlossenen mobilen QR-Bestätigung getrennt.

Docker-Build/Ausführung, Installation unter Linux/macOS, anhaltend hohe Auslastung, unabhängige Sicherheitsüberprüfung, eine echte unabhängige TSA-Reaktion, Validierung der Zertifikatssperrung/Archivierung sowie forensische Zertifizierung bleiben außerhalb der erfassten Qualifizierung. Gespeicherter MTProto-Zustand und Nachholfunktion sind implementiert; atomares, dauerhaftes Replay ist weiterhin nicht etabliert. Die Erfassung von Admin-Protokollen, zusätzliche Reaktorlisten und prioritätsgesteuertes Short-Polling bleiben separate Funktionen. Die kontrollierte Qualifikationsmatrix entnehmen Sie bitte [der Live-Abnahme](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).

Lokale detaillierte Belege und Screenshots befinden sich unter „test-results/“ (in Git ignoriert). Der öffentliche Screenshot in „docs/assets/“ enthält ausschließlich fiktive Demonstrationsdaten.

## Vorbereitung der öffentlichen Website und der Veröffentlichung · 27. Oktober 2026

Die separate „`website/`“-Präsentation und die Pages-Version wurden nach den oben genannten Panel-Prüfungen hinzugefügt. Es wurden weder die Konfiguration des Live-Kontos noch die Erfassungslogik geändert.

- Die bestehende Anwendungssuite hat bestanden: 138 bestanden, 1 POSIX-spezifischer Übersprung und eine Upstream-Warnung bezüglich der Veralterung von Starlette/httpx. Die 11 hinzugefügten Website-Build-Tests haben unabhängig voneinander bestanden, einschließlich der Ablehnung unerwarteter Ausgaben und der Ablehnung verknüpfter Eingaben.
- Beide Anwendungs-Browserskripte wurden unter Verwendung von „project-venv“, Playwright und der Chromium- Headless-Shell 156 ausgeführt. Es wurden keine JavaScript-Fehler auf den Seiten oder externe Anfragen verzeichnet. Alle Kontoszenarien verwendeten gefälschte Transportdaten und fiktive Daten.
- `tools/check_site.py` wurde bei den Breiten 320, 390, 768, 1024 und 1440 erfolgreich getestet, einschließlich eines URL-Teilpfads des Projekts, Tastatur-Tabulator-Befehlen, erfolgreichem bzw. verweigertem Zugriff auf die Zwischenablage, reduzierter Bewegung sowie deaktiviertem JavaScript. Es traten keine fehlgeschlagenen Asset-Anfragen oder externen Anfragen auf.
- `tools/build_site.py` hat 10 öffentliche Dateien auf der Zulassungsliste erstellt, insgesamt etwa 460 KB. Browser-Screenshots und eine Quittung befinden sich in der ignorierten Datei `test-results/site/`.
- Das Wheel wurde nach der Installation der ausschließlich für den Build bestimmten setuptools/wheel-Tools in der Projektumgebung erfolgreich erstellt. Die Installation in einer isolierten Zielumgebung und die Ausführung von „`tools/check_install.py`“ verliefen erfolgreich: statische Assets, Zugriffskontrolle, ein signierter synthetischer Export mit 32 Ereignissen sowie ein unabhängig verifizierter Streaming-Download.
- `pip check` wurde bestanden. Ein Muster-Scan der von Git ausgewählten öffentlichen Kandidaten ergab keine erkennbaren Blöcke mit privaten Schlüsseln, GitHub-/Bot-/AWS-Token, lange literale Geheimniszuweisungen oder Markierungen für Merge-Konflikte. Dies ist kein Beweis dafür, dass jedes mögliche Geheimnisformat fehlt. Laufzeitdaten-/Sitzungs-/Schlüsselabfragen wurden von Git ignoriert.
- Die GitHub-CLI-Authentifizierung war ungültig; es war kein Remote konfiguriert und es lag kein erster Commit vor. Es wurden weder ein Push noch ein gehosteter Workflow, eine Pages-Bereitstellung oder eine Veröffentlichung durchgeführt. Docker sowie die Live-Qualifizierung von Telegram und der Plattform bleiben von dieser Überprüfung ausgeschlossen.

Auf diesem Host schlug die Playwright-Download-Sperre auf dem Dateisystem des Arbeitsbereichs „E:“ fehl. Die Installation von Chromium unter `%LOCALAPPDATA%/tgwitness-playwright` und die Verwendung desselben `PLAYWRIGHT_BROWSERS_PATH` für die Prüfungen waren erfolgreich. Dies ist eine Umgehungslösung für die Umgebung, keine Änderung an den Laufzeitabhängigkeiten der Anwendung.

## Interaktive Dokumentation und Website-Metadaten · 29. Oktober 2026

Die öffentliche Website umfasst 12 englische HTML-Seiten: eine Startseite, ein Inhaltsverzeichnis der Anleitungen und zehn Anleitungen. Das Artefakt enthält 28 ausdrücklich aufgeführte Präsentationsdateien mit einer Größe von ca. 1,85 MB sowie keine Erfassungsdaten. Die öffentliche Website ist in englischer Sprache; Anwendungsübersetzungen und übersetzte Repository-Anleitungen sind separat verfügbar.

- Tests der Website, der Quellveröffentlichung und der Release-Grenzen: **18 bestanden, 2 übersprungen**. Die übersprungenen Tests betreffen die Erstellung von Symlinks auf diesem Windows-Dateisystem. Die Tests überprüfen eindeutige Seitenmetadaten, ausschließlich englischsprachige öffentliche Seiten, kanonische URLs, alle Sitemap-Einträge, lokale Assets/Anker, strukturierte Navigation sowie den Ausschluss privater Dateien.
- Sowohl „`tools/check_site.py`“ als auch „`tools/check_docs_site.py`“ bestanden den Test in Chromium bei 320, 390, 768, 1024 und 1440 Pixeln unter einem Unterpfad der Projekt-URL. Die im Leitfaden überprüften Punkte umfassen alle 11 Dokumentationsseiten, die Suche und die Tastaturnavigation, den Erfolg bzw. die Ablehnung bei der Nutzung der Zwischenablage sowie lesbare Inhalte ohne JavaScript.
- Fünf interaktive Beispiele bestanden: Wiedergabe/Schrittweise Navigation/Pause/Zurücksetzen von Nachrichten mit reduzierter Bewegung und Unterbrechung außerhalb des Bildschirms; ursprüngliche/veränderte/rekonstruierte/verkürzte Hash-Ketten; Entscheidungen bezüglich Zeugenakzeptanz/Rollback/Fork/keine Antwort; sowie Szenarien mit vollständiger/verzögerter/fehlender Zustellung; und eine Ermittlungskarte, die fiktive chatübergreifende Beobachtungen nach Absender-ID, Empfänger und Anhangs- Hash. Die Untersuchungsfunktionen bestanden die Prüfungen zur Tastaturnavigation und zum Fallback ohne JavaScript . Die SHA-256-Ergebnisse des Browsers wurden unabhängig mit Pythons „`hashlib`“ und dem kanonischen JSON verglichen. Das Hash- Beispiel behielt zudem seinen lesbaren Fallback bei, wenn Web Crypto nicht verfügbar war.
- Die Darstellungsquoten und Diagrammmarkierungen wurden an die barrierefreie Tabelle angepasst. Die Beschriftungen der mobilen Achsen wurden nach einer visuellen Überprüfung vergrößert. Jedes Beispiel ist als illustrativ oder synthetisch gekennzeichnet, und kein Browser-Beispiel stellt eine Verbindung zu Telegram her.
- Es wurden keine externen Anfragen, fehlgeschlagene HTTP-Anfragen oder JavaScript-Fehler erfasst. Screenshots und Belege für Desktop- und Mobilgeräte werden unter den Kennungen `test-results/site/` und `test-results/docs-site/` ignoriert. Der Dokumentationsindex, die Nachrichten-/Hash-Beispiele, das Witness-Layout, das Zustellungsdiagramm und die Untersuchungskarte wurden in den Größen für Desktop- und Mobilgeräte überprüft.
- Der Veröffentlichungsscan wurde für 282 öffentlich zugängliche Quelldateien und 1.426 lokale Dokumentationslinks erfolgreich durchgeführt. Ruff hat die modifizierten Python-Site-Tools und -Tests bestanden.
- `docs/HOW-IT-WORKS.md` bietet eine GitHub-Markdown-Ergänzung mit Mermaid- Diagrammen und Formeln. `docs/INVESTIGATION.md` deckt den gesamten Kontenumfang, die Erfassung des Chatverlaufs pro Chat, Personenprofile, chatübergreifende Verweise, Zeitachsen sowie die Übergabe verifizierter Fälle ab. Die einzelnen Schritte und Einschränkungen wurden anhand des aktuellen Codes für Umfang, Erfassung, Dossier, Export, Verifizierung und Bedienfeld überprüft. Die GitHub-Rendering-Funktion wurde nicht überprüft.

Hierbei handelt es sich um eine lokale Überprüfung der Website bzw. der Dokumentation. Es erfolgt keine Live-Qualifizierung von Telegram , noch wird die Bereitstellung gehosteter Seiten, der Erfolg einer Remote-CI oder die Indizierung durch Suchmaschinen festgestellt. Siehe [das Veröffentlichungsverfahren](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md) und [die Hinweise zu den Metadaten der Website](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/SEO.md).
