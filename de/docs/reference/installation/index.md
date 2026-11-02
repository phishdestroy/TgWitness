# Installieren, überprüfen und aktualisieren

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/installation/

Installieren Sie das Tool mit einem einzigen Befehl, überprüfen Sie Signaturen und Hashes, aktualisieren Sie die Installation und entfernen Sie sie.

[Projekt](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Schnellstart](https://phishdestroy.github.io/TgWitness/de/docs/reference/quickstart/) · [Bereitstellung](https://phishdestroy.github.io/TgWitness/de/docs/reference/deployment/)

## Installation mit einem einzigen Befehl

Das Installationsprogramm mit Assistent enthält eine private Python-Laufzeitumgebung. Verwenden Sie für zukünftige Installationen dieselbe Adresse: Bei jeder Veröffentlichung werden das Installationsprogramm, die Hashes, Signaturen und Build-Informationen gemeinsam aktualisiert.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Führen Sie das Programm auf einem Ubuntu-Server als Root aus, um einen Hintergrunddienst zu installieren. Auf einem Desktop-Rechner führen Sie es als normaler Benutzer aus.

**Windows (PowerShell oder Eingabeaufforderung):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Unter Windows ist kein Administrator erforderlich. Der untergeordnete PowerShell-Prozess lässt Ihr Terminal mit dem Ergebnis geöffnet. Python und die Abhängigkeiten verbleiben in der Installation.

Wählen Sie unter Ubuntu **„Dieser Computer**“, **„Temporärer HTTPS-Link**“ oder **„Eigene Domain**“. Das Installationsprogramm zeigt die Panel-Adresse und den Zugangsschlüssel an. Für einen temporären Link öffnen Sie diese HTTPS-Adresse in Ihrem Browser und geben Sie den Schlüssel ein. Bei lokalem Zugriff auf einen Remote- Server verwenden Sie eine SSH-Weiterleitung von Ihrem Computer (`ssh -L 8787:127.0.0.1:8787 user@server`) und öffnen Sie `http://127.0.0.1:8787`. Unter macOS und Windows öffnet sich das lokale Panel in Ihrem Browser; lassen Sie das Terminal weiterlaufen.

Melden Sie sich im Panel bei Telegram an und wählen Sie aus, was erfasst werden soll. Die Installation allein löst die Telegram-Erfassung nicht aus.

## Wo alles läuft

`get.destroy.tools` ist ein **Cloudflare Worker, der statische Downloads bereitstellt**. Er verfügt weder über ein TgWitness-Panel noch über eine Telegram-Sitzung oder eine Datenbank mit Benutzerdaten. Er wird nicht an einen Projekt-VPS weitergeleitet. Die Anwendung läuft auf dem Rechner, auf dem Sie den Befehl ausführen.

| Installation | Programm | Daten |
| --- | --- | --- |
| Ubuntu als Root | `/opt/tgwitness` | Systemdienst: `/var/lib/tgwitness-<installation ID>`; den `tgwitness paths` für den genauen Pfad. |
| Linux-/macOS-Benutzer | `~/.local/share/tgwitness` | `data/live` unter dieser Installation. |
| Windows-Benutzer | `%LOCALAPPDATA%\TgWitness` | `data\live` unter dieser Installation. |

Wählen Sie `TGWITNESS_INSTALL_DIR` , um einen anderen Ordner auszuwählen. Installierte Versionen und Daten sind voneinander getrennt. Das Installationsprogramm lädt Ihre Konten, Nachrichten oder Schlüssel nicht auf die Download-Seite hoch. Wenn Sie einen Cloudflare-Tunnel auswählen, wird der Datenverkehr des Panels über Cloudflare geleitet; die Verwendung Ihrer eigenen Domain verweist auf Ihren eigenen Server.

Jede Installation enthält **die Dateien „START-HERE.html“** und **„START-HERE.txt“** mit lokalen Pfaden, Befehlen und Links zum Repository. Führen Sie `tgwitness guide` aus, um die Anleitung zu öffnen. Unter Windows verwenden Sie `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` in der PowerShell.

## Vor der Ausführung überprüfen

Der einzeilige Befehl vertraut bei seinem Startskript auf HTTPS. Dieses Skript überprüft vor der Installation SHA-256 sowie die RSA-Signatur des Projekts in Bezug auf die Anwendung und die Einschränkungen. Sie können das Startskript auch zunächst herunterladen und überprüfen.

Der öffentliche Veröffentlichungsschlüssel lautet [„release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub)“. Sein SHA-256 lautet:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Bewahren Sie diesen Fingerabdruck aus einer Repository-Revision auf, der Sie vertrauen. Eine Prüfsumme vom selben Download-Server erkennt Abweichungen; der unabhängig vertrauenswürdige öffentliche Schlüssel dient zur Authentifizierung einer Release-Signatur.

Verwenden Sie für die unten aufgeführten Verifizierungs-Downloads ein neues, leeres Verzeichnis.

**Linux / macOS – in einem neuen, leeren Download-Verzeichnis ausführen** (erfordert curl und OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

Die `&&` Kette wird vor der Ausführung angehalten, wenn ein Download, eine Schlüssel-Fingerabdruck- oder Signaturprüfung fehlschlägt. Wenn zwischen dem Herunterladen des Skripts und dessen Signierung eine Veröffentlichung erfolgt, werden beide erneut heruntergeladen. Alte Installationsprogramme behalten ihre unveränderlichen Paket-URLs bei.

**Windows – Überprüfen Sie vor der Ausführung das SHA-256:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Vergleichen Sie den Hash mit der `install.ps1` Zeile. Für eine unabhängige Signaturprüfung verwenden Sie OpenSSL (zum Beispiel über Git Bash) und denselben Fingerabdruck des öffentlichen Schlüssels wie oben:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Die Windows-Installation selbst überprüft die Paketsignaturen mit .NET und benötigt kein OpenSSL. Es handelt sich um separate RSA-3072-Signaturen (SHA-256), nicht um Authenticode. Das [Manifest](https://get.destroy.tools/manifest.json) enthält die Softwareversion, den genauen Git-Commit, die unveränderliche Release-ID und die SHA-256 jedes Artefakts. Die Seite enthält einen Link zur entsprechenden Quelle. Das Manifest und die Prüfsummenliste verfügen ebenfalls über separate Signaturen (`manifest.json.sig` und `SHA256SUMS.txt.sig`).

## Eine bestehende Installation aktualisieren

**Eine neue Veröffentlichung aktualisiert die Download-Seite; installierte Programme werden aktualisiert, wenn Sie das Installationsprogramm erneut ausführen.** Es gibt keinen unbeaufsichtigten Updater und keinen automatischen Neustart einer laufenden Sammlung. Der aktuelle Installationskanal ist **„Preview“**; er folgt veröffentlichten, geprüften Builds von `main`, deren Commit neuer sein kann als die letzte nummerierte GitHub-Version. Die Versionsangabe der Seite stammt aus `pyproject.toml`; ihr Commit und ihre Build-ID unterscheiden Aktualisierungen innerhalb derselben Preview-Version.

Verwenden Sie denselben Installationsordner und denselben Betriebssystembenutzer wie zuvor. Sichern Sie das gesamte Datenverzeichnis, während die Erfassung angehalten ist; `tgwitness paths` identifiziert es. Ein signierter Export ist keine vollständige Installationssicherung.

**Ubuntu-Root-Installation unter `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

Nach erfolgreicher Installation:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Für eine Installation unter Linux/macOS verwenden Sie die Originaldatei `TGWITNESS_INSTALL_DIR` oder die Standardeinstellung und führen Sie den ersten Installationsbefehl erneut aus. Schließen Sie ein Panel im Vordergrund vor der Aktualisierung und starten Sie es anschließend erneut. Für einen konfigurierten Linux-Dienst führen Sie den entsprechenden `tgwitness restart` Befehl aus.

**Windows:** Schließen Sie das geöffnete Fenster, führen Sie den Windows-Installationsbefehl erneut aus und öffnen Sie dann `bin\tgwitness.cmd` in derselben Installation. Das Installationsprogramm behält Daten, Sitzungen, Zugriffseinstellungen und Signaturschlüssel bei. Es wechselt den Launcher erst, nachdem die neue Umgebung die Prüfungen bestanden hat; bei fehlgeschlagener Installation bleibt der vorherige Launcher erhalten. Bewahren Sie die Sicherung vor dem Upgrade wegen Änderungen am Speicherformat auf.

## Alltägliche Befehle unter Ubuntu

| Befehl | Ergebnis |
| --- | --- |
| `tgwitness open` | Aktuelle Panel-URL und Zugriffsschlüssel. |
| `tgwitness paths` | Genaue Pfade zu Programmen, Daten und Anleitungen. |
| `tgwitness guide --print` | Anleitung für den Offline-Betrieb. |
| `tgwitness status` / `tgwitness logs` | Verfügbarkeits- und Dienstprotokolle. |
| `tgwitness stop` / `tgwitness start` | Dienst anhalten/fortsetzen; Daten beibehalten. |
| `tgwitness token rotate` | Ersetzen Sie den Administratorschlüssel und beenden Sie die Browsersitzungen. |
| `tgwitness tunnel off` | Den öffentlichen Quick-Tunnel deaktivieren; das lokale Panel beibehalten. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Erstellen Sie einen Quick-Tunnel-Link bzw. ersetzen Sie dessen Adresse. |

Siehe [„Zugriff“](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/) für Kollegentokens, Sitzungen und IP-Einschränkungen sowie [„Veröffentlichung des Installers“](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) für den Release-Workflow von GitHub zu Cloudflare.

## TgWitness entfernen

Es gibt kein Deinstallationsprogramm: Sie beenden das Panel und löschen dessen Ordner. Durch das Löschen des Datenordners werden Journale, Signaturschlüssel, Telegram-Sitzungen und gespeicherte Dateien endgültig gelöscht. Zuvor:

1. Exportieren Sie, was Sie benötigen (**Exporte → Signierte ZIP herunterladen**), und bewahren Sie den Fingerabdruck des Signaturschlüssels sowie die Checkpoints außerhalb dieses Rechners auf. Um den Arbeitsbereich selbst zu sichern, kopieren Sie den gesamten Datenordner, während die Erfassung angehalten ist.
2. Löschen Sie Server, die unter **„Extras → Server 24/7“** in **„Ihre Server“** oder mit `python -m tgwitness.cloud destroy`; der Anbieter stellt sie so lange in Rechnung, bis sie gelöscht werden.
3. Beenden Sie die Sitzung jedes Kontos in Telegram unter **„Einstellungen“ → „Geräte**“. Das Löschen der Dateien führt nicht dazu, dass die Sitzung auf der Seite von Telegram abgemeldet wird.

**Root-Installation unter Ubuntu.** Notieren Sie sich den Datenordner, stoppen Sie den Dienst und entfernen Sie anschließend den Dienst, die Ordner und die Verknüpfung:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Installation für Linux- oder macOS-Benutzer.** Schließen Sie das Fenster. Ein konfigurierter Linux-Benutzerdienst wird mit `systemctl --user disable --now tgwitness-<ID>`; seine Einheit befindet sich in `~/.config/systemd/user/`. Löschen Sie anschließend `~/.local/share/tgwitness` (oder Ihr `TGWITNESS_INSTALL_DIR`) sowie die `~/.local/bin/tgwitness` Verknüpfung.

**Windows.** Schließen Sie das Fenster und löschen Sie `%LOCALAPPDATA%\TgWitness` (oder Ihre `TGWITNESS_INSTALL_DIR`). Das Installationsprogramm fügt weder einen Dienst noch eine geplante Aufgabe oder eine Verknüpfung hinzu.
