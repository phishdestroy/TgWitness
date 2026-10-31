# Schnellstart

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/quickstart/

Alle Möglichkeiten zur Installation und zum Start von TgWitness: Windows-Paket, Python, Docker und die synthetische Demo mit ersten Überprüfungen.

**Englisch** · [Russisch](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [Ukrainisch](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [Português (Brasil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [Farsi](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [Vereinfachtes Chinesisch](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness ist eine eigenständige Anwendung zur Überwachung von Telegram-Gruppen und -Kanälen, auf die Ihre Konten Zugriff haben. Sie läuft lokal mit einem eigenen Datenverzeichnis.

**Sind Sie zum ersten Mal hier?** [Sehen Sie sich die Demo an,](https://phishdestroy.github.io/TgWitness/de/docs/reference/quickstart/#explore-the-interface) bevor Sie ein Konto verknüpfen. [Wählen Sie eine Anleitung](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) zu Proxys, Witnesses, Exporten oder der Serverkonfiguration.

## Installieren und starten

[Erfassung mit GitHub Actions (Vorschau)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

Wählen Sie eine Methode aus. Portable Downloads stehen zur Verfügung, sobald eine Release-Version veröffentlicht wurde:

| Host | Keine Installation erforderlich | Aus der Quelle: Python 3.11+ | Docker: Engine/Desktop mit Compose 2.20+ |
| --- | --- | --- | --- |
| Windows | `TgWitness-<version>-windows-amd64-portable.zip` aus den GitHub-Veröffentlichungen extrahieren, auf `TgWitness.cmd` doppelklicken | Doppelklicken Sie auf „`Start.cmd`“ | Doppelklicken Sie auf „`scripts\Docker.cmd`“ |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

Um den Quellcode zu erhalten, laden Sie bitte die ZIP-Datei mit dem Quellcode von GitHub Releases herunter und entpacken Sie sie oder klonen Sie das Repository. „`Start.cmd`“ bietet an, Python 3.12 für Ihren Windows-Benutzer zu installieren, falls kein geeignetes Python gefunden wird (winget oder der signierte Installer von python.org). `start.sh` gibt den genauen Installationsbefehl für Ihre Linux-Distribution oder macOS aus, falls Python fehlt. Beim ersten Start der Quelldatei wird `.venv` erstellt und die Abhängigkeiten werden automatisch installiert.

Docker erstellt die Anwendung und startet sie im Hintergrund; ein Python-Host ist nicht erforderlich. „`scripts\Docker.cmd`“ und „`scripts/docker-start.sh`“ geben die Panel-Adresse und das Token aus, wenn der Container ordnungsgemäß läuft. Die entsprechenden Docker-Befehle auf jedem unterstützten Host lauten:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Öffnen Sie **http://127.0.0.1:8787**. Verwenden Sie das vom Docker-Helper ausgegebene Token oder den zweiten Docker-Befehl, oder lesen Sie **die Datei „data/live/panel-token.txt“** für eine portable oder Quellcode-Installation. Fahren Sie unten unter **„Telegram verbinden“** fort. Native und Docker-Installationen verwenden getrennte Speicher; beim Starten von Docker wird ein bereits vorhandenes natives Protokoll nicht importiert.

Bei einem Server umfasst [die Bereitstellung](https://phishdestroy.github.io/TgWitness/de/docs/reference/deployment/) automatisches HTTPS, Neustart, veröffentlichte Bilder, Updates und Backups.

## Entdecken Sie die Benutzeroberfläche

1. Führen Sie **„TgWitness-Demo.cmd“** im portablen Paket, **„scripts\Demo.cmd“** in einem Windows-Quellordner oder „`sh start.sh --demo` “ unter Linux/macOS aus. Beim Start aus dem Quellordner wird zunächst „`.venv` “ erstellt und die Abhängigkeiten werden installiert.
2. Open-**http://127.0.0.1:8787**.
3. Die lokale Demo öffnet das Beispielprotokoll automatisch. Für den direkten lokalen Zugriff ist keine Token-Kopie erforderlich.

Die Beispielnachrichten sind fiktiv. Im Demomodus kann keine Verbindung zu einem echten Telegram-Konto hergestellt werden.

## Telegram verbinden

> [!WARNUNG] **Verwenden Sie nichts, dessen Verlust Sie sich nicht leisten können.** Wir raten dringend davon ab, persönliche oder wertvolle Konten zu verknüpfen und eine API-ID bzw. einen Hash für ein Konto zu erstellen, das Ihnen wichtig ist. Telegram sperrt Konten unvorhersehbar und oft dauerhaft, unabhängig vom verwendeten Client. Ein reibungsloser Testlauf hängt von Telegram ab, nicht von TgWitness, und bietet keinerlei Garantie für die Zukunft.

1. Falls die native Demo ausgeführt wird, beenden Sie diese und führen Sie **„Start.cmd“** oder „`sh start.sh`“ aus. Andernfalls lassen Sie die oben gestartete Live-Installation weiterlaufen.
2. Verwenden Sie das Panel-Token für Ihre Installationsmethode, um das Panel zu öffnen.
3. Falls Sie einen Proxy benötigen, speichern Sie diesen unter **„Konto“ → „Einstellungen“ → „Verbindungseinstellungen“ → „Verbindungsroute ändern**“.
4. Geben Sie unter **„Konto**“ Ihre Telefonnummer ein und klicken Sie auf **„Weiter“**, wählen Sie **„QR-Code“ → „QR-Code anzeigen**“ oder wählen Sie Dateien aus und klicken Sie auf **„Konto verbinden**“. **API-ID + Hash** sind optional: Der Arbeitsbereich verwendet das gespeicherte oder importierte Paar oder ein funktionierendes Paar aus dem integrierten Pool. Um Ihre eigene App zu verwenden, fügen Sie ein „`API ID:API Hash`“-Paar in das Feld „API-ID“ ein. Für einen vollständigen Autorisierungsschlüssel wählen Sie **„Auth-Schlüssel“**, fügen Sie alle 512 hexadezimalen Zeichen ein und wählen Sie die bereitgestellte DC-ID aus. Die Benutzer-ID ist optional und wird bei Eingabe aktiviert.
5. Schließen Sie die von Ihnen gewählte Anmeldemethode ab: Telefon/Code/2FA, Bestätigung über eine angemeldete Telegram-App für QR oder Import einer unterstützten, autorisierten Sitzung.
6. Überprüfen Sie die angezeigte Konto-ID. Open **Sources**: Ihre Chats werden automatisch geladen; fügen Sie Ihre Gruppen hinzu.
7. Wählen Sie unter **„Auswählen**, **welche Änderungen beibehalten werden sollen**“ entweder Ereigniskategorien oder die Voreinstellung **„Nachrichten, Bearbeitungen und Löschungen**“ aus und speichern Sie anschließend die Überwachungseinstellungen.
8. Wählen Sie die Einstellungen für Anhänge separat aus und klicken Sie anschließend auf **„Beobachtung starten**“.

API-Zugangsdaten identifizieren Ihre Anwendung; sie autorisieren kein Konto an sich. Private Gruppen benötigen keinen öffentlichen Benutzernamen, aber Ihr Konto muss über Zugriffsrechte verfügen.

Für bestehende Konten siehe [Konten und Sitzungsformate](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/): Das Bedienfeld akzeptiert Telethon StringSession, Telethon/Pyrogram SQLite, TData-ZIP-Dateien für Einzelkonten sowie unterstützte Konto-JSON-Dateien. Wählen Sie eine Sitzung und die dazugehörige JSON-Datei gemeinsam aus und klicken Sie auf **„Konto verbinden**“. Eine Anmeldung per QR-Code ist ebenfalls mit denselben optionalen API-Einstellungen verfügbar. TDLib, Bots und Massenkontenlisten werden nicht unterstützt.

Um ein weiteres Konto hinzuzufügen, drücken Sie „**+**“ neben der Kontoauswahl oder öffnen Sie **„Konto“ → „Einstellungen“ → „Verbindungseinstellungen“ → „Arbeitsbereiche“** oder nutzen Sie **die Funktion „Konten**“. Arbeitsbereiche verfügen über separate Sitzungen, Protokolle, Schlüssel, Quellen und Warteschlangen. Beim Wechseln der Ansicht laufen die anderen Erfassungsmodule weiter. Dasselbe Telegram-Konto kann in dieser Installation nicht zwei Arbeitsbereichen zugewiesen werden. Es gibt keine festgelegte Anzahl von Arbeitsbereichen; sie teilen sich einen Prozess, sodass die Kapazität von der Rechenleistung des Computers abhängt.

Das Live-Panel-Token schützt den Zugriff auf Ihre Telegram-Berechtigungen und gespeicherte Daten; es ist unabhängig von den Anmeldedaten für die Telegram-API. Nur eine explizit gestartete, direkt aufgerufene lokale Demo erhält automatisch einen Eintrag. Eine Remote- oder Proxy-Demo verwendet weiterhin „ `data/demo/panel-token.txt`“.

## Überprüfen und exportieren

- **Protokoll:** Beobachtungen nach Quelle und Ereignistyp suchen und filtern.
- Wählen Sie ein Ereignis aus, um dessen Originaldatensatz, Zuordnung und gespeicherte Versionen einzusehen.
- Die Bearbeitungsdetails zeigen den verfügbaren Inhalt vor und nach der Bearbeitung an. Die Löschdetails zeigen den zuletzt erfassten Inhalt, sofern vorhanden; ein unbekannter Akteur bleibt unbekannt.
- **Exportformate:** signierte ZIP-, JSONL- und CSV-Dateien sowie Offline-HTML.
- **Vollständiger Chat-Export** (Quellen → Vollständiger Chat-Export): Laden Sie den gesamten sichtbaren Verlauf eines Chats als signiertes Bundle mit `chat.json` (im Telegram-Export-Format) und einer lesbaren `chat.html`-Datei herunter. Private Chats funktionieren, sofern das Konto Mitglied ist. Es handelt sich um eine aktuelle Momentaufnahme, nicht um eine Rekonstruktion gelöschter oder zuvor bearbeiteter Nachrichten. Überprüfen Sie eine Kopie mit `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256`.
- **Checkpoint beachten:** Die Grenze des signierten Protokolls muss außerhalb des Collectors liegen.
- **Signierten Ausführungsbeleg herunterladen:** Bewahren Sie die Programm- und Versionsdaten des Erfassungsprogramms auf.
- **Zeitstempelanfrage vorbereiten:** Bereiten Sie eine Offline-Anfrage an eine Zeitstempel-Behörde vor; befolgen Sie die Anweisungen in [der Datei „TIMESTAMP.md“,](https://phishdestroy.github.io/TgWitness/de/docs/reference/timestamp/) um eine Antwort zu erhalten und zu überprüfen.
- **Protokoll überprüfen:** Überprüfen Sie Ereignissignaturen und Kettenverknüpfungen. Beim ZIP-Export werden auch Medieninhalte überprüft.

Unterstützte Browser speichern umfangreiche Exporte direkt in einer Datei Ihrer Wahl. Andere Browser puffern maximal 128 MiB. Solange der Server läuft, unterstützt die Streaming-CLI größere Downloads, ohne die gesamte Antwort zwischenspeichern zu müssen:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Für einen weiteren Arbeitsbereich fügen Sie „`--profile ID`“ über **„Exporte → Arbeitsbereich-ID“** hinzu. Für einen Remote-Server fügen Sie „`--url https://your-server`“ hinzu. Das Standard-Übertragungslimit beträgt 5 GiB; mit `--max-mib` lässt sich dies ändern. Signierte ZIP-Inhalte unterliegen standardmäßig einem separaten Verifizierungslimit von 4 GiB im unkomprimierten Zustand (**mit „Parameters“** lässt sich dieses erhöhen; verifizieren Sie solche Archive mit `verify.py --max-gib N`). Verifizieren Sie das Archiv mithilfe einer vertrauenswürdigen Kopie des Verifizierers und eines unabhängig aufbewahrten Schlüssel-Fingerabdrucks bzw. Checkpoints.

## Installationsanleitung

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check` überprüft lokale Abhängigkeiten, die Signaturunterstützung, den Speicher, die Schlüsselkonfiguration und die Abhöradresse. Es wird nichts installiert und keine Verbindung zu Telegram hergestellt. Ein belegter Port kann darauf hindeuten, dass eine andere Instanz läuft. Verwenden Sie ein anderes `--port` oder beenden Sie diese zunächst.

Der Launcher wird in „`.venv`“ installiert. Zusatzbefehle für „`python -m tgwitness...`“ müssen unter Windows „`.venv\Scripts\python.exe`“ oder unter Linux/macOS „`.venv/bin/python`“ verwenden, es sei denn, diese Umgebung ist bereits aktiviert.

## Sitzungen, Schutz und Betrieb

Eine geschlossene, konsistente Telethon-SQLite-Datei „`.session`“ kann lokal mit „`python -m tgwitness.sessions account.session --out account.tgwitness-session`“ konvertiert und anschließend in Account geladen werden. Ein direkter Dateiimport und eine QR-Anmeldung sind ebenfalls verfügbar. Informationen zu Anmeldeformaten, SOCKS5, HTTP CONNECT, MTProxy und externen Hauptschlüsseln finden Sie in [der Datei „CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/)“.

**Beobachtung pausieren** stoppt die Erfassung. **Sperren** schließt nur den Browserzugriff. Beim Schließen eines Tabs läuft der Erfassungsprozess weiter. Das Beenden des Prozesses unterbricht die Erfassung; eine Momentaufnahme des Verlaufs kann nicht alle verpassten Bearbeitungen oder Löschungen rekonstruieren. Einzelheiten zu Ereignisrichtlinien, Anhangswarteschlangen, Kontoisolierung und Neustarts finden Sie unter [So funktioniert die Erfassung](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/).

Sitzungen und Geheimnisse sind verschlüsselt. Nachrichteninhalte, Medien und Exporte erfordern eine verschlüsselte Festplatte oder ein verschlüsseltes Volume. Signaturen gewährleisten die Integrität in Bezug auf einen vertrauenswürdigen Schlüssel; sie bestätigen jedoch weder die Herkunft aus Telegram noch verhindern sie Manipulationen durch einen Betreiber, der den Collector und dessen Schlüssel kontrolliert.

Lesen Sie [„OPERATIONS.md“](https://phishdestroy.github.io/TgWitness/de/docs/reference/operations/) für Informationen zu Sicherung und Wiederherstellung, [„DEPLOYMENT.md“](https://phishdestroy.github.io/TgWitness/de/docs/reference/deployment/) zum Thema Hosting sowie [„deploy/“](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) für Anwendungsbeispiele. Das installierte Panel enthält zudem eine Anleitung zur Offline-Einrichtung unter „`/guide.html`“.

Die tatsächliche Verifizierung und die verbleibenden Einschränkungen sind in [den Dateien „VERIFICATION.md“](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/) und [„READINESS.md“](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) dokumentiert.
