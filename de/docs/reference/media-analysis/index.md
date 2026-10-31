# Lokale OCR und Transkription

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/media-analysis/

Erkennen Sie erfasste Bilder und Audiodateien mit einem lokalen Worker; verknüpfen Sie den abgeleiteten Text weiterhin mit der Quelldatei.

**Aktueller Hauptpunkt:** Verwenden Sie einen Source-Checkout; die portable Vorschauversion 0.7.0 stammt aus einer Zeit vor der Einführung dieser Funktion.

[Anleitung zum Arbeitsablauf](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Öffnen Sie einen `media.saved`-Protokoll-Eintrag, wählen Sie **„Anhang erkennen“** und wählen Sie anschließend unter **„Archiv befragen“** entweder „OCR“ oder „Transkription“ aus. Die Verarbeitung erfolgt manuell und lokal. Es gibt keinen Cloud-Medienmodus und keinen automatischen Upload. Die ursprünglichen Anhangsdaten und das „ `media_sha256`“-Protokoll bleiben unverändert; der erkannte Text wird ausdrücklich als maschinelle Erkennung gekennzeichnet und separat zusammen mit dem Quell-Hash, der Engine-/Modellversion, der Sprache, den Parametern und der Fertigstellungszeit gespeichert. Transkripte behalten die zurückgegebenen Zeitstempel bei.

Durchsuchen Sie diese Ergebnisse mithilfe **der Suche nach erkanntem Text** und dem OCR-/Transkript-Filter. Es handelt sich hierbei um eine separate Suche in abgeleiteten Daten; sie wandelt die maschinelle Erkennung nicht stillschweigend in den ursprünglichen Telegram-Text um und fügt ihn auch nicht zu signierten Ereignissen hinzu.

## Richten Sie den optionalen Worker ein

Version 1 erfordert einen Linux-Host mit einem lokalen Docker-Daemon. Unter Windows kann TgWitness in einer Linux-VM/WSL-Umgebung mit einem eigenen lokalen Daemon ausgeführt werden. Das Panel entschlüsselt niemals selbst einen nicht vertrauenswürdigen Anhang.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

Setzen Sie diese Variablen in der TgWitness-Serviceumgebung und starten Sie den Dienst neu. Der Daemon-Socket ist standardmäßig auf „`/var/run/docker.sock`“ eingestellt; bei rootlosen Bereitstellungen kann „ `TGWITNESS_DOCKER_SOCKET`“ festgelegt werden. Der Worker nutzt explizit diesen Unix-Socket anstelle eines entfernten Docker-Kontexts. Geben Sie die Docker-API nicht für Panel-Benutzer frei und mounten Sie den Socket nicht innerhalb des Erkennungscontainers.

Für die Transkription installieren Sie separat ein CTranslate2-kompatibles Whisper-Modell und legen Sie anschließend `TGWITNESS_WHISPER_MODEL_DIR` auf dessen Verzeichnis fest. Der Worker lädt es mit `local_files_only=True`; das ausgewählte Modell und die Eingabe werden schreibgeschützt eingebunden. Siehe die [Dokumentation zum Laden von Modellen](https://github.com/SYSTRAN/faster-whisper) der Engine. Das mitgelieferte OCR-Image enthält trainierte Daten für Englisch und Russisch. Integrieren Sie bei Bedarf eine weitere Sprache in Ihr Image; die Sprachcodes entsprechen [denen der Tesseract-Befehlszeilenschnittstelle](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).

Während der Verarbeitung wird kein Modell abgerufen. Die Erstellung/der Download des Setups kann eine Netzwerkverbindung erfordern; bei jedem einzelnen Erkennungscontainer ist die Netzwerkverbindung deaktiviert. Installieren Sie das Image, bevor Sie es aktivieren; die Laufzeitumgebung verwendet „`--pull=never`“.

## Grenzen und Wiederherstellung

Der Container läuft als Benutzer ohne Sonderrechte mit einem schreibgeschützten Root-Zugang, reduzierten Rechten, `no-new-privileges` , einer CPU, 2 GiB Arbeitsspeicher, einer PID-Begrenzung und einem begrenzten temporären Dateisystem. Es werden nur eine verifizierte Kopie der ausgewählten Datei und ein optionales Modellverzeichnis eingebunden. Die Datenbank, der Tresor und die Sitzung des Collectors werden nicht eingebunden. Die [Docker-Laufzeit-Flags](https://docs.docker.com/reference/cli/docker/container/run/) erzwingen diese Beschränkungen; es handelt sich hierbei um eine Containergrenze, nicht um eine Hardware-Enklave.

Dateien sind auf 50 MiB begrenzt, Bilder auf 20 Millionen Pixel, Audiodateien auf 30 Minuten mit bekannter Dauer und die Verarbeitung auf fünf Minuten. Es läuft jeweils nur ein Worker, mit maximal 20 Aufgaben in der Warteschlange bzw. in Ausführung und 100 gespeicherten Aufgaben pro Arbeitsbereich. „Cancel“ stoppt den Container; „Retry“ erstellt einen neuen Auftrag, der mit dem vorherigen Versuch verknüpft ist. Unterbrochene Aufträge werden nach dem Neustart entsprechend gekennzeichnet. Die Verarbeitung kann fehlschlagen, wenn ein Modell die konfigurierten Grenzen nicht einhalten kann; ohne Isolierung läuft es nicht im Hintergrund weiter.
