# Halten Sie den Betrieb aufrecht

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/server/

Stellen Sie sicher, dass der Collector auch nach Neustarts verfügbar bleibt und seine Daten intakt bleiben.

## Wählen Sie eine Startmethode

Für eine native Installation verwenden Sie den [Launcher](https://phishdestroy.github.io/TgWitness/de/docs/start/) und die Service-Beispiele im Verzeichnis [„deploy/“.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Für Docker installieren Sie Docker mit Compose und führen Sie das Programm vom Projektverzeichnis aus:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Das Standard-Panel lauscht auf der Loopback-Adresse des Hosts, Port 8787. Öffnen Sie es lokal oder über einen SSH-Tunnel. Verwenden Sie das Token aus dem zweiten Befehl, um das Panel zu entsperren.

## Behalten Sie das gesamte Datenverzeichnis bei

Bei nativen Installationen wird „`data/live`“ verwendet. Docker nutzt das persistente Volume „`tgwitness-data`“. Bewahren Sie Protokolle, Kontositzungen, Schlüssel und den Betriebsstatus gemeinsam auf. Ein signierter Export ist ein nützliches Beweismittel, stellt jedoch keine vollständige Sicherungskopie der Installation dar.

1. Beenden Sie die Erfassung, bevor Sie eine konsistente Datensicherung erstellen.
2. Kopieren Sie das gesamte Verzeichnis mit den privaten Daten in einen geschützten Speicherort außerhalb des Hosts.
3. Testen Sie die Wiederherstellung in einer isolierten Installation, bevor Sie sich auf das Backup verlassen.

## Bitte nach einem Neustart überprüfen

Bestätigen Sie den erwarteten Arbeitsbereich und den Schlüssel, die Telegram-Verbindung, die ausgewählten Quellen sowie die Erfassung neuer Nachrichten. Der gespeicherte MTProto-Status und die Nachholfunktion helfen dabei, Aktualisierungen wiederherzustellen, die Telegram noch speichert. Es ist jedoch nicht möglich, jede abgelaufene Aktualisierung oder eine vor der Erfassung gelöschte Bearbeitung zu rekonstruieren.

„Container-Status“ bedeutet, dass der Webserver reagiert. Verwenden Sie eine kontrollierte Nachricht und eine Zeugenprüfung, um die Erfassung und externe Veröffentlichung zu bewerten.

## Veröffentlichen Sie nur das, was Sie beabsichtigen

Die Referenz zur Bereitstellung enthält HTTPS-Beispiele, Befehle für persistente Volumes sowie Schritte zur Aktualisierung und Wiederherstellung. Für die Bereitstellung werden Docker-Befehle bereitgestellt; der aktuelle [Validierungsbericht](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/) gibt Auskunft über die tatsächlich getesteten Umgebungen.
