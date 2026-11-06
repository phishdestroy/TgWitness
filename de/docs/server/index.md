# Halten Sie den Betrieb aufrecht

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/server/

Halten Sie den Collector am Laufen und die Daten über Neustarts hinweg sicher.

## Wählen Sie eine Startmethode

Nativ: der [Starter](https://phishdestroy.github.io/TgWitness/de/docs/start/) plus Dienstvorlagen in [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker, aus dem Projektordner:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Das Panel lauscht auf localhost:8787. Lokal oder über einen SSH-Tunnel öffnen, mit dem Token aus dem zweiten Befehl.

## Behalten Sie das gesamte Datenverzeichnis bei

Nativ: `data/live`. Docker: das Volume `tgwitness-data`. Journale, Sitzungen und Schlüssel gehören zusammen. Ein signierter Export ist ein Beweis, kein Backup.

1. Zuerst die Erfassung stoppen.
2. Das ganze Datenverzeichnis an einen sicheren Ort außerhalb des Hosts kopieren.
3. Die Wiederherstellung auf einer separaten Installation testen, bevor Sie sich darauf verlassen.

## Bitte nach einem Neustart überprüfen

Arbeitsbereich und Schlüssel, Verbindung, Quellen und eingehende neue Nachrichten prüfen. TgWitness holt nach, was Telegram noch hat, nicht alles, was während der Ausfallzeit passiert ist.

Ein „gesunder“ Container heißt, der Webserver antwortet. Ob die Erfassung funktioniert, zeigen eine Testnachricht und der Zeuge.

## Veröffentlichen Sie nur das, was Sie beabsichtigen

HTTPS, Volumes, Updates und Wiederherstellung stehen in der Deployment-Referenz. Was tatsächlich getestet wurde: [Prüfprotokoll](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/).
