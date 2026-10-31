# Finden Sie heraus, was schiefgelaufen ist

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/troubleshooting/

Beginnen Sie mit dem Symptom. Überprüfen Sie jeweils eine Ebene nach der anderen.

## Das Panel fordert ein Token an

Verwenden Sie das Panel-Token aus der lokalen Datei, die vom Launcher angezeigt wird. Für Docker führen Sie „`docker compose exec tgwitness cat /data/panel-token.txt`“ aus. Ein Telegram-Anmeldecode, ein BotFather-Token und ein schreibgeschütztes Witness-Token dienen unterschiedlichen Zwecken.

## Telegram stellt keine Verbindung her

Öffnen Sie die Verbindungseinstellungen und führen Sie die Verbindungsprüfung durch. Wenn Sie einen öffentlichen Proxy verwenden, probieren Sie einen anderen Eintrag aus und speichern Sie die Route explizit. Überprüfen Sie den Proxy-Typ und das unterstützte Geheimformat. Das Aktualisieren einer öffentlichen Liste ändert die Route des Kontos nicht.

## Verbunden, aber keine neuen Nachrichten

1. Bitte überprüfen Sie, ob die Überwachung im richtigen Arbeitsbereich ausgeführt wird.
2. Bitte stellen Sie sicher, dass die Quelle ausgewählt und für dieses Konto sichtbar ist.
3. Senden Sie eine eindeutige neue Nachricht in einer kontrollierten Gruppe und suchen Sie nach genau diesem Text.
4. Überprüfen Sie das Betriebsprotokoll auf Unterbrechungen, Arbeitsverzögerungen oder Telegram-Fehler.

Historische Momentaufnahmen und Ereignisse bei neuen Nachrichten unterscheiden sich voneinander. Eine „stille“ Quelle kann verbunden werden, ohne dass neue Nachrichten erzeugt werden. Führen Sie einen kontrollierten Zustellungstest durch, wenn es auf Vollständigkeit ankommt.

## FloodWait oder eine Lücke nach einem Neustart

„FloodWait“ bedeutet, dass Telegram eine Pause benötigt. Warten Sie die angegebene Zeitspanne ab und überprüfen Sie den Erfassungsumfang; wiederholte Verbindungsversuche heben die Beschränkung nicht auf. Der gespeicherte Aktualisierungsstatus hilft dabei, nach einem Neustart den Rückstand aufzuholen, doch abgelaufene Aktualisierungen und bestimmte Unterbrechungszeitfenster bleiben weiterhin Einschränkungen. Erfassen Sie die Lücke, anstatt das Protokoll als vollständig zu betrachten.

## Der Bot ist konfiguriert, veröffentlicht jedoch nichts

Stellen Sie sicher, dass der Witness-Prozess tatsächlich läuft, der Bot im Kanal posten kann und der Witness den Collector sowie die Bot-API erreichen kann. Überprüfen Sie das Protokoll auf fehlgeschlagene Veröffentlichungen. Eine erfolgreiche Abfrage des Collectors allein bestätigt noch keinen Kanalbeitrag.

## Wo befindet sich die GitHub-Token-Integration?

**In Planung.** Unter „Extras“ wird der vorgeschlagene Workflow zur Fork- und Build-Verifizierung beschrieben. Derzeit gibt es weder ein GitHub-Token-Formular noch eine automatisierte Bestätigung, dass eine laufende Installation mit einem Repository übereinstimmt. Siehe den [aktuellen Status der Funktionen](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/).

Wenn Sie ein Problem melden, geben Sie bitte die Version, das Betriebssystem, die Schritte sowie einen unkenntlich gemachten Fehler an. Halten Sie Sitzungen, Tokens, private Nachrichten und das Datenverzeichnis aus öffentlichen Meldungen heraus.
