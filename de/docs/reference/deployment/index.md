# Bereitstellung

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/deployment/

Führen Sie TgWitness als Dienst unter Windows, Linux, macOS oder Docker hinter einer HTTPS-Verbindung aus, einschließlich Backups und Updates.

**Englisch** · [Russisch](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [Ukrainisch](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [Português (Brasil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [Farsi](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [Vereinfachtes Chinesisch](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## Wählen Sie eine Installationsvariante

Für das portable Paket entpacken Sie bitte „`TgWitness-<version>-windows-amd64-portable.zip`“ von GitHub Releases. Für die anderen Methoden laden Sie bitte die Quell-ZIP-Datei herunter und entpacken Sie diese oder klonen Sie das Repository und führen Sie anschließend im Projektverzeichnis Folgendes aus:

| Installation | Start | Läuft es im Hintergrund? |
| --- | --- | --- |
| Portables Windows-Paket | `TgWitness.cmd` | Nein; lassen Sie das Fenster geöffnet. |
| Native Windows-Version | `Start.cmd` | Nein; nutzen Sie die optionale Anmeldeaufgabe für den Hintergrundbetrieb. |
| Native Linux-/macOS-Version | `sh start.sh` | Nein; verwenden Sie systemd/launchd für den Betrieb im Hintergrund. |
| Docker auf jedem unterstützten Host | `docker compose up -d --build --wait` | Ja, solange der Docker-Daemon läuft. |
| Docker-Hilfsprogramm unter Windows | `scripts\Docker.cmd` | Ja; der Helper wartet auf den Betriebszustand des Webservers. |
| Docker-Hilfsprogramm unter Linux/macOS | `sh scripts/docker-start.sh` | Ja; der Helper wartet auf den Betriebszustand des Webservers. |

Für einen Cloud-Server, der von Dritten überprüft werden können sollte – erstellt über die API des Anbieters, ohne SSH, ausschließlich über einen Cloudflare-Tunnel erreichbar – siehe [„High-Assurance-Bereitstellung](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md)“.

Beim nativen Start wird ein privates „`.venv`“ erstellt und die festgelegten Abhängigkeiten installiert. Docker erstellt diese innerhalb des Images, ohne dass Python auf dem Host erforderlich ist. Für die erstmalige Einrichtung ist ein Internetzugang erforderlich. Wird kein Python 3.11+ gefunden, fragt „`Start.cmd`“ vor der Installation von Python 3.12 für den aktuellen Windows-Benutzer nach (winget, andernfalls der python.org- Installer nach Überprüfung der Signatur der Python Software Foundation); es werden niemals Administratorrechte angefordert. Docker und Betriebssystemdienste bleiben weiterhin Voraussetzungen.

Native und portable Installationen verwenden „`data/live`“ innerhalb ihres Ordners. Docker verwendet das Volume mit dem Namen „`tgwitness-data`“ unter „`/data`“. Dabei handelt es sich um separate Installationen, bis Sie das gesamte Datenverzeichnis bewusst migrieren. Erwarten Sie nicht, dass ein neuer Docker-Container native Konten automatisch erkennt.

## Installationsvoraussetzungen

Für die native Installation sind Python 3.11 oder höher mit „`venv`“ und „`ensurepip`“, ein Internetzugang für die Installation der ersten Abhängigkeiten sowie ein beschreibbares Projektverzeichnis für „ `.venv`“ erforderlich. Das mitgelieferte Panel benötigt weder Node.js noch eine Frontend-Erstellung. Führen Sie den Launcher von Ihrem normalen Betriebssystem-Konto aus; Administrator- oder Root-Rechte werden von TgWitness nicht benötigt.

- **Windows:** `Start.cmd` überprüft zunächst `py -3`, dann `python`, anschließend die standardmäßigen benutzerspezifischen und „Program Files“-Installationsordner und erfordert Version 3.11 oder höher. Sollte keine dieser Optionen funktionieren, bietet das Programm die oben beschriebene automatische benutzerspezifische Installation an. `py -3 start.py` funktioniert ebenfalls. Das portable Paket benötigt überhaupt kein Python.
- **Linux:** `start.sh` probiert `python3.13`, `python3.12`, `python3.11`, `python3` und `python` aus und gibt den Installationsbefehl für apt, dnf, pacman, zypper, apk oder Homebrew aus, sofern keiner davon geeignet ist. Bei Debian-/Ubuntu-Installationen ist möglicherweise das `python3-venv`-Paket erforderlich, das zum ausgewählten Interpreter passt. Die ältere Standard-Python-Version einer Distribution muss durch Python 3.11+ ersetzt oder ergänzt werden.
- **macOS:** Installieren Sie eine aktuelle Python-3.11-Distribution; gehen Sie nicht davon aus, dass ein vom Betriebssystem bereitgestellter Interpreter die Anforderungen erfüllt. Verwenden Sie „`python3 start.py`“ aus dem Projektverzeichnis.
- **Docker:** Verwenden Sie Docker Engine/Desktop mit Compose v2.20 oder neuer. Docker Desktop muss unter Windows Linux-Container verwenden. Der Container installiert seine eigenen Python-Abhängigkeiten; auf dem Host ist keine separate Python-Installation erforderlich.

Verwenden Sie für das Datenverzeichnis einen persistenten lokalen Speicher. Planen Sie die Kapazität unter Berücksichtigung von Nachrichten, Medien, WAL-Wachstum, Exporten und Backups ein; es gibt keine evidenzbasierte, universelle Mindestanforderung an Festplatten- oder RAM-Kapazität für jede Arbeitslast. CPU-Architekturen und Python-Versionen ohne kompatible Dependency-Wheels erfordern möglicherweise zusätzliche Build-Tools und deren eigene Qualifizierung. „Portabel“ ist kein Anspruch auf universelle Betriebssystem- oder Hardwareunterstützung.

Windows 11/Python 3.12 wurde lokal verifiziert. Definitionen für Linux, macOS und Container sowie CI werden bereitgestellt, wurden jedoch auf diesem Entwicklungsserver nicht ausgeführt. Den genauen Umfang entnehmen Sie bitte der Datei [„VERIFICATION.md](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/)“.

## Lokaler Computer

Verwenden Sie „`Start.cmd`“ unter Windows oder „`sh start.sh`“ unter Linux/macOS. „`scripts\Setup.cmd`“ oder „`sh start.sh --setup-only`“ bereitet die Umgebung vor. Der Launcher installiert bei der ersten Verwendung die erforderlichen Abhängigkeiten; bei späteren Starts wird die Umgebung wiederverwendet. Für die Einrichtung und die Telegram-Erfassung ist ein Internetzugang erforderlich, das Durchsuchen bestehender Datensätze und das Erstellen von Exporten funktionieren jedoch offline.

Führen Sie nach der Einrichtung „`python start.py --check`“ aus, um lokale Abhängigkeiten, Ed25519, den Speicher, die Schlüsselkonfiguration und die Empfangsadresse zu überprüfen, ohne einen Collector zu starten. Verwenden Sie „`--json`“ für eine strukturierte Ausgabe. Übergeben Sie die vorgesehenen Befehle „`--data-dir`“, „`--host`“ und „`--port`“. Die Überprüfung installiert keine Pakete, erstellt kein Protokoll und stellt keine Verbindung zu Telegram her; es handelt sich nicht um eine Integritäts- oder Abdeckungsprüfung. Der Startvorgang überprüft separat vorhandene Protokolle. „`python start.py --help`“ vermeidet ebenfalls eine Installation.

Optionen:

Führen Sie nach dem Ausführen von „start.py“ die Zusatzbefehle mit „`.venv\Scripts\python.exe`“ unter Windows oder „`.venv/bin/python`“ unter Linux/macOS aus, oder aktivieren Sie diese Umgebung zunächst. Die folgenden „`python -m ...`“-Beispiele setzen voraus, dass die Umgebung aktiv ist.

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

Umgebungsvariablen: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN. TGWITNESS_VAULT_KEY_FILE wählt bei einer Neuinstallation den Modus mit externem Schlüssel aus; siehe unten. TGWITNESS_TOKEN muss, sofern angegeben, mindestens 24 Zeichen enthalten; verwenden Sie einen kryptografisch generierten Zufallswert. Ohne diese Angabe generiert die App ein 256-Bit-Zufallstoken in der Datei „panel-token.txt“. Die Umgehung der Umgebungsvariablen überschreibt diese Datei nicht. Starten Sie die Anwendung neu, um die Anmeldedaten zu rotieren.

Ein Datenverzeichnis darf genau einem Prozess gehören. Eine plattformübergreifende Dateisperre des Betriebssystems verhindert versehentliche gleichzeitige Schreibvorgänge. Verwenden Sie einen Uvicorn-Worker. Das Panel kann eine beliebige Anzahl von Arbeitsbereichen verwalten, wobei zusätzliche Arbeitsbereichsverzeichnisse unter „profiles/<id>/“ liegen. Verwenden Sie für separate Service-Instanzen separate Verzeichnisse und Ports. SQLite-WAL-Dateien gehören in einen lokalen persistenten Speicher, nicht in ein Netzwerkdateisystem. Teilen Sie kein Volume zwischen Replikaten.

## Portables Windows-Paket

Jede GitHub-Veröffentlichung enthält `TgWitness-<version>-windows-amd64-portable.zip` und dessen `.sha256`. Sie umfasst die offizielle, einbettbare Python-3.12-Laufzeitumgebung von python.org (Prüfsumme in `tools/build_portable.py` festgehalten), TgWitness und dessen festgelegte Abhängigkeiten sowie drei Startprogramme:

| Datei | Zweck |
| --- | --- |
| `TgWitness.cmd` | Starten Sie das Panel; zusätzliche Optionen werden weitergeleitet, z. B. `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | Starten Sie die synthetische Demo unter `data\demo` |
| `TgWitness-Check.cmd` | Führen Sie die Bereitschaftsprüfung durch, ohne das Programm zu starten |

Entpacken Sie das gesamte Archiv in einen beschreibbaren Ordner wie beispielsweise „`Documents\TgWitness`“; führen Sie das Programm nicht direkt aus der ZIP-Datei oder aus dem Ordner „Programme“ aus. Die Laufzeitumgebung verwendet einen isolierten Modulpfad, sodass andere Python-Installationen und „`PYTHONPATH`“ keinen Einfluss darauf haben. Die Daten verbleiben im `data`-Ordner des Pakets. Um ein Update durchzuführen, beenden Sie TgWitness, entpacken Sie die neue Version in einen neuen Ordner und kopieren Sie den `data`-Ordner dorthin.

Stellen Sie es selbst unter 64-Bit-Windows mit Python 3.12 zusammen:

```
python tools/build_portable.py
```

Der Builder überprüft die Laufzeitsumme, installiert die erforderlichen Abhängigkeiten in das Paket, führt die Bereitschaftsprüfung mit dem eingebetteten Interpreter durch und schreibt die ZIP-Datei sowie die Prüfsumme in „`dist/`“.

## Container

```
docker compose up -d --build --wait
```

Dadurch wird ein benanntes persistentes Volume für /data erstellt. Der Web-Port wird auf 127.0.0.1:8787 abgebildet. Der Prozess läuft unter der UID 10001 mit eingeschränkten Berechtigungen, einem schreibgeschützten Root-Dateisystem sowie beschreibbaren Verzeichnissen /data und /tmp. `--wait` überprüft den Betriebszustand des Webservers, bevor es zurückkehrt; es stellt keine Telegram- Autorisierung oder -Zustellung her. Die bereitgestellten Hilfsprogramme verwenden nach dem Erstellen ein Bereitschafts-Timeout von 180 Sekunden . Das anfängliche Herunterladen von Abhängigkeiten kann länger dauern.

Beide Basis-„Compose“-Dateien verwenden den Projektnamen „`tgwitness`“, sodass beim Entpacken einer neuen Version in ein anderes Verzeichnis nicht automatisch ein neues Datenvolume ausgewählt wird. Halten Sie nur eine Bereitstellung für dieses Projekt aktiv. Verwenden Sie für unabhängige Installationen einen eindeutigen Namen „ `docker compose -p NAME ...`“ und einen anderen Host-Port und behalten Sie bei Updates beide bei. Bei einer älteren Bereitstellung mit einem anderen Projektnamen verwenden Sie weiterhin deren ursprünglichen Namen zusammen mit „`-p`“; „`docker compose ls`“ listet vorhandene Projekte auf.

Kopieren Sie `deploy/env.example` nach `.env` und ändern Sie `TGWITNESS_PORT` so, dass ein anderer Loopback-Port verwendet wird. Beispielsweise macht `TGWITNESS_PORT=8788` das Panel unter `http://127.0.0.1:8788` zugänglich; der Container lauscht weiterhin auf Port 8787. `.env` wird von Git ignoriert.

Das anfängliche Token abrufen:

```
docker compose exec tgwitness cat /data/panel-token.txt
```

Nützliche Befehle:

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` startet den Collector nach einem Absturz oder einem Neustart des Docker-Daemons neu. Aktivieren Sie auf einem Linux-Server Docker beim Systemstart über den Dienstmanager Ihrer Distribution, in der Regel `sudo systemctl enable --now docker`. Unter Windows/macOS aktivieren Sie die Einstellung „Beim Anmelden starten“ in Docker Desktop. Das Abmelden vom Desktop, der Ruhezustand oder ein angehaltener Docker-Daemon die Datenerfassung unterbrechen. Ein explizit angehaltener Container bleibt angehalten, bis Sie ihn erneut starten.

Das /tmp-Volume ist in der Beispielkonfiguration auf 512 MiB begrenzt. Die Exportkonstruktion verwendet stattdessen das „`temporary-exports/`“ jedes Arbeitsbereichs auf dem persistenten /data-Verzeichnis. Reservieren Sie dort Speicherplatz für gleichzeitige Exporte, das Wachstum von Journal/WAL, Medien und Backups. Der Launcher verwendet die Datei „deploy/constraints.txt“, um qualifizierte Versionen von Laufzeitabhängigkeiten festzulegen. Docker- und Hochsicherheitsserver werden anhand von „deploy/requirements.lock“ und „deploy/build.lock“ mit „pip --require-hashes“ installiert: Jede Paketdatei muss mit einem im Commit gespeicherten SHA-256-Hash übereinstimmen, sodass eine auf PyPI oder einem Mirror ersetzte Datei abgelehnt wird. Das Python-Basis-Image sowie die Betriebssystempakete erfordern weiterhin eine eigenständige Freigabeprüfung.

Verwenden Sie den Befehl „docker compose down -v“ nur, wenn Sie beabsichtigen, das Protokoll und die Schlüssel zu löschen. Der Container-Statusbericht gibt Auskunft über die Verfügbarkeit des Webservers, nicht über die erfolgreiche Erfassung von Telegram-Nachrichten. Überprüfen Sie den Status des Collectors, den Heartbeat, Fehler und Abdeckungsereignisse im Dashboard.

### Profil eines unabhängigen Zeugen

Der optionale `witness`-Dienst betreibt einen [unabhängigen Witness](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/) in einem eigenen Container, mit eigenem Schlüssel und eigenem Protokoll im `witness-data`-Volume sowie lediglich einem schreibgeschützten Witness-Token für den Collector. Erstellen Sie das Token auf der **Witness**-Seite des Panels, fügen Sie es zusammen mit einem Bot-Token und einem Kanal zu `.env` hinzu und starten Sie anschließend das Profil:

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

Der Dienst erreicht den Collector innerhalb des Compose-Netzwerks unter `http://tgwitness:8787` (`TGWITNESS_WITNESS_COLLECTOR` überschreibt diesen, beispielsweise `/profiles/<workspace ID>` für einen anderen Arbeitsbereich). Für einen Witness auf einem separaten Server, der von einer anderen Person betrieben wird, verwenden Sie dort `deploy/compose/compose.witness.yaml` , wobei `TGWITNESS_WITNESS_COLLECTOR` auf die HTTPS-Adresse des Collectors gesetzt ist; diese Datei enthält ausschließlich den Witness.

## Installieren Sie ein veröffentlichtes Image

Diese wird nach einem erfolgreichen [Release-Workflow](https://phishdestroy.github.io/TgWitness/de/docs/reference/deployment/#automated-github-releases) und der öffentlichen Konfiguration des GHCR-Pakets verfügbar. Der Eigentümer bzw. Name des Repositorys ist nicht fest in diesem Quellcode-Baum hinterlegt. Verwenden Sie das Bild, das in der Workflow-Zusammenfassung dieser Version angezeigt wird.

Kopieren Sie `deploy/env.example` nach `.env`. Setzen Sie `TGWITNESS_IMAGE` auf die veröffentlichte Version, wobei Sie den Repository-Pfad **in Kleinbuchstaben** verwenden, zum Beispiel:

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.1
TGWITNESS_PORT=8787
```

Führen Sie diese Datei separat aus, anstelle von „`compose.yaml`“:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

Auf dem Host sind weder eine Quellcode-Kompilierung noch Python oder ein Compiler erforderlich. Der Release-Workflow ist auf Linux-AMD64- und ARM64-Container ausgerichtet, einschließlich der Linux-VM von Docker Desktop. Verwenden Sie ein Versions-Tag oder „`ghcr.io/owner/repository@sha256:...`“ aus der Workflow-Zusammenfassung. Es ist weder ein bewegliches „`latest`“-Tag noch ein unbeaufsichtigtes Anwendungs-Upgrade konfiguriert. Die Image- und Quellvarianten nutzen dasselbe Datenvolumen, sofern ihre Projektnamen übereinstimmen.

## Automatisches HTTPS auf einem Server

Verwenden Sie einen Server mit Docker, eine von Ihnen verwaltete Domain und einen dauerhaften lokalen Speicher. Richten Sie die A-/AAAA-Einträge der Domain auf den Server aus; veröffentlichen Sie AAAA nur, wenn der Server über IPv6 erreichbar ist. Erlauben Sie eingehenden TCP-Verkehr auf den Ports 80 und 443 sowie ausgehenden DNS-/HTTPS-Verkehr für die Zertifikatsausstellung. Diese Ports dürfen nicht bereits von anderen Diensten belegt sein.

Kopieren Sie `deploy/env.example` nach `.env` und legen Sie einen Hostnamen fest, ohne Schema oder Pfad:

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

Starten Sie den Quellcode-Build mit dem HTTPS-Overlay:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

Verwenden Sie für ein veröffentlichtes Bild stattdessen „`deploy/compose/compose.image.yaml`“ als erste Datei. Behalten Sie beide „`-f`“-Argumente für spätere Status-, Protokoll-, Aktualisierungs- und Stoppbefehle bei.

Caddy bezieht und erneuert ein Zertifikat, leitet HTTP-Anfragen auf HTTPS um und leitet Anfragen an den Collector im privaten Compose-Netzwerk weiter. Der Zertifikatsstatus verfügt über ein eigenes persistentes Volume. Der direkte Host-Port des Collectors bleibt ausschließlich für Loopback-Verbindungen reserviert. Die bereitgestellte Caddy-Konfiguration aktiviert keine Zugriffsprotokollierung.

Öffnen Sie `https://watch.your-domain.org` und geben Sie das Panel-Token ein. Die Bereitschaftsprüfung bestätigt weder die Ausstellung eines Zertifikats noch die Erreichbarkeit von externen Servern. Sollte HTTPS nicht bereit sein, überprüfen Sie DNS, Firewall-Regeln sowie:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

Das bereitgestellte Caddy-Image folgt dem Tag „`2-alpine`“. Durch einen „Pull“ wird dieses Image aktualisiert; binden Sie einen getesteten Digest in Ihre Bereitstellung ein, falls Sie feste Infrastrukturversionen benötigen.

## Aktualisierungen und Sicherungen

Behalten Sie den Namen des „Compose“-Projekts und das Datenvolumen bei allen Aktualisierungen bei. Stoppen Sie zunächst den Collector und erstellen Sie eine vollständige Sicherung. Für die standardmäßige, quellbasierte Bereitstellung:

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Verwenden Sie jedes Mal ein neues Sicherungsziel außerhalb des Repositorys und schützen Sie dieses als Material mit Kontozugriff. Der Beispielpfad dient nur zur Veranschaulichung; verwenden Sie Ihren privaten Speicherort für die Sicherung. Kopieren Sie das gesamte Verzeichnis, einschließlich versteckter Dateien, aller Arbeitsbereiche, Schlüssel, Protokolle und Medien. Sichern Sie einen externen Tresor-Hauptschlüssel separat, falls dieser konfiguriert ist. Eine ZIP-Datei mit Beweismaterial ist kein wiederherstellbares Anwendungs-Backup. Bei HTTPS bewahren Sie bitte auch die Caddy-Volumes auf, falls Sie den Status des Zertifikats bzw. des Kontos beibehalten müssen.

Für eine Installation aus dem Quellcode laden Sie bitte die Dateien der neuen Version herunter und führen Sie folgenden Befehl aus:

```
docker compose up -d --build --wait
```

Für die Installation der Image-Version ändern Sie bitte „`TGWITNESS_IMAGE`“ in die gewünschte Version und führen Sie anschließend folgenden Befehl aus:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Verwenden Sie die „Compose“-Datei(en) Ihrer Installation auch für die vorangehenden „stop“- und „copy“-Befehle. Behalten Sie „`.env`“, die benutzerdefinierte Konfiguration und denselben Projektnamen bei. „`down`“ behält benannte Volumes bei; „**`down -v`**“**löscht diese**. Kopieren Sie „`.venv`“ nicht zwischen Betriebssystemen oder Python-Versionen. Für native Updates stoppen Sie TgWitness, sichern Sie das gesamte Datenverzeichnis, ersetzen Sie die Quelldateien und führen Sie „`python start.py --setup-only`“ vor dem Start aus.

Überprüfen Sie nach einem Update den Zugriff auf das Kontrollpanel, die Kontoidentität, den Beobachtungsstatus und die Abdeckung. Durch einen Neustart werden verpasste Telegram-Updates nicht wiederhergestellt. Ein Rollback erfordert möglicherweise die vor dem Update erstellte Sicherung, falls eine zukünftige Version die Speicherformate ändert.

## Automatisierte GitHub-Veröffentlichungen

Der [Release-Workflow](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml) ist einsatzbereit, sobald dieses Projekt in ein GitHub-Repository mit aktivierten Actions übertragen wurde. Er wird ausgeführt, wenn ein GitHub-Release **veröffentlicht** wird, einschließlich einer Vorabversion. Entwürfe und Tag-Pushes allein führen nicht zur Veröffentlichung von Paketen.

1. Legen Sie die Paketversion und das Changelog fest und veröffentlichen Sie anschließend eine Version mit dem Tag „`v`“ sowie der genauen „`pyproject.toml`“-Version, beispielsweise „`v0.7.1`“.
2. Der Workflow validiert das Tag und führt die gemeinsamen Python-, allgemeinen/Konto-Import-/QR-Browser-, Quellpaket- und Docker-Prüfungen unter Windows, Linux und macOS durch. Eine neue native Installation wird ebenfalls auf allen drei Betriebssystemen unter Verwendung von Python 3.12 durchgeführt.
3. Nachdem diese Prüfungen erfolgreich abgeschlossen sind, führt das System einen Smoke-Test eines ARM64-Images unter QEMU durch, veröffentlicht AMD64/ARM64-Images unter `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>`, und fügt die Quell-ZIP-Datei sowie das Python-Wheel mit ihren SHA-256-Sidecars bei. Die Windows-portable ZIP-Datei ist genau das Artefakt, das vom Prüf-Workflow getestet wurde; der Release-Workflow lädt dieses Artefakt und seine Prüfsumme herunter und veröffentlicht sie.
4. Ein abschließender Vorgang lädt alle drei veröffentlichten Pakete erneut herunter und überprüft deren Prüfsummen. Anschließend werden `SHA256SUMS.txt` und `RELEASE-MANIFEST.json` veröffentlicht, wobei die Version, die Quellcode-Revision und die Größe der Assets protokolliert werden. Beim Hochladen werden vorhandene Release-Assets nicht überschrieben.
5. Öffnen Sie nach der ersten Veröffentlichung die GHCR-Paketeinstellungen und legen Sie die Sichtbarkeit auf **„Öffentlich“** fest, falls anonyme Bildabrufe beabsichtigt sind. Ein öffentliches Quell-Repository allein garantiert noch kein öffentliches Container-Paket. Die Richtlinien Ihrer Organisation müssen die Veröffentlichung von Paketen zulassen. Der Workflow verwendet `GITHUB_TOKEN`; kein Registry- Passwort und keine VPS-Anmeldedaten dürfen im Repository enthalten sein.

Der Erfolg des Remote-Workflows wurde durch diese lokale Vorbereitung noch nicht nachgewiesen. Die ARM64- Emulation dient lediglich als Test, nicht als Qualifizierung für native Hardware oder den Live-Einsatz mit Telegram. Dies automatisiert die Erstellung der Release-Pakete; zum Starten eines Servers sind weiterhin der Befehl „Compose“ sowie die entsprechenden Domain- und Host-Voraussetzungen erforderlich. Bestehende Server werden bei der Veröffentlichung eines Releases nicht automatisch aktualisiert oder neu gestartet.

## Entfernungsserver

Beschränken Sie den Dienst auf Loopback und verwenden Sie einen SSH-Tunnel oder lassen Sie HTTPS an einem Reverse-Proxy enden. Die Basis-„Compose“-Datei ist ausschließlich lokal; das optionale „ `deploy/compose/compose.https.yaml`“-Overlay stellt Caddy für eine konfigurierte Domain bereit. Vermeiden Sie es, das Bearer-Token in URLs und Proxy-Protokollen offenzulegen. Ein Reverse-Proxy sollte die Anforderungsgröße und die Verbindungsraten begrenzen. Setzen Sie das Internet keinem unverschlüsselten HTTP aus.

Beispiele für systemd, eine Windows-Anmeldeaufgabe, einen macOS-User-Agent und Caddy finden Sie im Verzeichnis [„deploy/“](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Überprüfen und passen Sie deren Pfade vor der Installation an. Es handelt sich hierbei um bereitgestellte Vorlagen, nicht um lokal ausgeführte Plattformkonfigurationen. Es wird kein Hintergrunddienst oder keine Hintergrundaufgabe durch den normalen Launcher registriert.

Unter Windows speichert ein fensterloser `pythonw.exe`-Startvorgang die Start- und Serverdiagnosedaten in `logs/server.log` im Datenverzeichnis (5 MiB pro Datei, zwei rotierende Sicherungskopien). Bei Konsolenstarts werden die Konsolenprotokolle beibehalten. Die Protokollierung des HTTP-Zugriffs ist in beiden Modi deaktiviert. Schützen Sie die Protokolle zusammen mit dem Datenverzeichnis und überprüfen Sie diese, bevor Sie sie weitergeben.

## Neustart und Lücken

Der zuletzt angeforderte Beobachtungsstatus wird beibehalten. War die Beobachtung aktiv, versucht das Programm beim Start, die Verbindung wiederherzustellen und ausgewählte Quellen fortzusetzen. Durch manuelles Anhalten wird diese Absicht aufgehoben. Ein fehlgeschlagener Neustart wird protokolliert und im Bedienfeld angezeigt.

StringSession behält die Autorisierung bei, jedoch nicht den dauerhaften Aktualisierungs- bzw. Entitätsstatus von Telethon. Dialoge werden beim Start neu geladen. Telegram/Telethon kann einige Transportunterbrechungen während des Betriebs beheben, TgWitness erhebt jedoch keinen Anspruch auf dauerhafte Wiedergabe über Prozessneustarts hinweg. Bei jedem Start werden der vorherige Journal-Anfang und die Offline-Grenze aufgezeichnet. Der Monitor überprüft die Konnektivität alle 10 Sekunden und fügt jede Minute einen Heartbeat hinzu (**Parameter → „Liveness record every**“). Kurze Unterbrechungen können übersehen werden; eine bestehende Verbindung garantiert keine vollständige Übermittlung von Aktualisierungen. Snapshots sind explizite Momentaufnahmen des aktuellen Verlaufs und dienen niemals der Lückenfüllung.

Die Medienwarteschlange wird in der SQLite-Datenbank des jeweiligen Arbeitsbereichs gespeichert. Eine Nachricht und der dazugehörige Auftrag werden atomar festgeschrieben. Unterbrochene laufende Aufträge werden beim Start wiederhergestellt und erneut ausgeführt. Jeder Download hat ein Basis-Timeout von 120 Sekunden zuzüglich der für seine Größe erforderlichen Zeit bei 256 KiB/s sowie ein Limit von 1–2.000 MiB pro Anhangstyp; Timeout, Geschwindigkeit und Wiederholungsversuche sind unter **„Parameter“** einstellbar. Der Collector überspringt Dateien, deren Größe unbekannt ist. Beim Anhalten bleiben die in der Warteschlange befindlichen Aufgaben erhalten. Bei Wiederholungsversuchen wird der ursprüngliche beobachtete Dateideskriptor verwendet, niemals die neueste Version einer anschließend bearbeiteten Nachricht. Vorübergehende Fehler unterliegen einer begrenzten Anzahl von Wiederholungsversuchen; Pausen bei „Media FloodWait“ bleiben nach einem Neustart erhalten. Die Medienwiederherstellung erfolgt getrennt von der Telegram-Update-Wiederherstellung und kann verschwundene Dateien nicht wiederherstellen.

## Sicherung, Wiederherstellung und Speicherkapazität

Beenden Sie den Vorgang, bevor das **gesamte Datenverzeichnis** kopiert wird, einschließlich „vault.key“, „signing.enc“, „credentials.enc“, SQLite-Datenbank-/WAL-Dateien, Medien, Token, Checkpoints sowie aller Profile und Unterverzeichnisse. Stellen Sie die vollständige Kopie wieder her, während der Zieldienst angehalten ist. Fehlende Vault-Schlüssel oder eine Nichtübereinstimmung der Signaturschlüssel führen zu einem Fehlschlag beim Start; generieren Sie keine Schlüssel neu, um den Zugriff zu erzwingen.

Bewahren Sie geheime Backups verschlüsselt und mit Zugriffskontrolle auf. Die ZIP-Dateien mit den Beweismitteln sind portable Prüfartefakte, keine Anwendungs-Backups oder Backups von Telegram-Sitzungen. Es erfolgt keine automatische Löschung nach einer bestimmten Aufbewahrungsfrist. Planen Sie Speicherplatz für alle Nachrichten, Rohdaten, Metadaten, Medien, temporäre Exporte und Backups ein.

Starten Sie die Verifizierung und exportieren Sie Stream-Datensätze, anstatt das gesamte Protokoll zu laden. Ein Export fixiert einen Lese-Snapshot, während neue WAL-Schreibvorgänge fortgesetzt werden können; bei lang andauernden Exporten können WAL-Seiten beibehalten werden, sodass die Festplattenkapazität weiterhin eine Rolle spielt. ZIP-Dateien sind auf 4 GiB (unkomprimiert) begrenzt, um der Standardeinstellung des unabhängigen Prüfers zu entsprechen; **„Parameter → Größte signierte ZIP-Datei“** erhöht die Obergrenze, und solche Archive werden mit „`verify.py --max-gib N`“ verifiziert. Andere Formate haben keine Begrenzung der Ereignisanzahl. Unterstützte Browser streamen Antwortblöcke in eine vom Benutzer ausgewählte Datei. Andere Browser puffern maximal 128 MiB und leiten größere Übertragungen an die authentifizierte CLI weiter:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Verwenden Sie `--profile ID` aus **„Exports“ → „Workspace ID“** für einen anderen Arbeitsbereich, `--format zip|jsonl|csv|html` oder `--url https://your-server` für einen Remote-Server oder `--max-mib`, um das Übertragungslimit von 5 GiB zu ändern. Einfaches HTTP ist nur für Loopback zulässig. Token werden in Headern übertragen, Weiterleitungen werden abgelehnt, vorhandene Dateien werden nicht überschrieben und unvollständige Downloads werden nicht als abgeschlossene Dateien veröffentlicht. Falls TGWITNESS_TOKEN das generierte Token überschreibt, verwenden Sie eine separat geschützte Datei, die diesen aktiven Wert enthält: panel-token.txt wird durch die Überschreibung nicht überschrieben. Der SHA-256-Wert des Befehls dient lediglich als Übertragungsprüfsumme; überprüfen Sie die signierte ZIP-Datei unabhängig davon.

Server-Exportdateien verbleiben im privaten Verzeichnis „`temporary-exports/`“ des jeweiligen Arbeitsbereichs. Bei erfolgreichen Abfragen werden die Dateien bereinigt. Unterbrochene Exporte werden beim nächsten Start des Arbeitsbereichs entfernt, wobei dessen exklusive Instanzsperre aufrechterhalten bleibt. Dieses Verzeichnis ist Teil des Speicherbedrohungs-/Kapazitätsmodells; verwenden Sie ein verschlüsseltes Datenvolume. Übertragungen im Produktionsmaßstab im Multi-Gigabyte-Bereich erfordern weiterhin eine Qualifizierung auf Ihrem Zielsystem.

Das Dashboard zeigt Medien in der Warteschlange bzw. fehlgeschlagene Medien, die ältesten ausstehenden Medien, freien Speicherplatz, Pausen bei Telegram- Anfragen sowie Quellen an, deren Zugriff noch nicht bestätigt ist. Diese Diagnosedaten stellen keine vollständige End-to-End-Überwachung der Datenübertragung dar. Arbeitsbereiche teilen sich einen Prozess; ein „lautes“ Konto kann daher dennoch andere beeinträchtigen. Separate Arbeitsprozesse, Aufbewahrung/Rotation, dauerhafte Wiederherstellung von Aktualisierungen sowie die vollständige Qualifizierung der Bereitstellung bleiben bestehen. Der bereichsbezogene Zugriff auf das Dashboard ist unter [„Zugriff und Berechtigungen“](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/) dokumentiert; unabhängige Kontrollpunkte werden im [Zeugenleitfaden](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/) behandelt.

## Verbindungs- und Schutzoptionen

Verbindungswege sind arbeitsbereichsspezifisch und sollten vor der Autorisierung konfiguriert werden. SOCKS5/HTTP CONNECT verwenden die fest zugeordnete Python-Socks-Abhängigkeit. MTProxy nutzt Telethons experimentellen, zufallsbasierten Zwischenübertragungsmechanismus; gefälschte TLS-Ee-Geheimnisse werden nicht unterstützt. Der direkte Fallback hängt vom ausgewählten [IP-Modus](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/#ip-modes) ab: „Hide IP“ lehnt ihn ab; der explizite Fallback-Modus erlaubt ihn nach einer Verzögerung. Der Tunnel-/VPN-Modus erlaubt direkte Routen, erstellt jedoch kein VPN. Dies ist keine systemweite Netzwerkrichtlinie.

Bei Neuinstallationen verweist TGWITNESS_VAULT_KEY_FILE auf eine separat geschützte, zufällig generierte Hauptschlüsseldatei. Mounten Sie diese schreibgeschützt außerhalb von /data in einem Container. Bewahren Sie die öffentlichen „vault.external.json“-Salt-Metadaten für jeden Arbeitsbereich sowie den Hauptschlüssel separat auf. Bestehende lokale Tresore erfordern eine geplante Migration; das Setzen dieser Variablen führt nicht zu einer automatischen Konvertierung. Die Speicherung und der Export von Nachrichten und Medien erfolgen nicht anwendungsverschlüsselt. Verwenden Sie bei Bedarf verschlüsselte Volumes und ausreichend privaten temporären Speicher.

Detaillierte Anleitungen: [Verbindung/Sicherheit](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/) und [Betriebsmodi](https://phishdestroy.github.io/TgWitness/de/docs/reference/operations/).
