# Telegram · Finden Sie heraus, was schiefgelaufen ist

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/troubleshooting/

Fangen Sie beim Symptom an, prüfen Sie eins nach dem anderen.

## Das Panel fordert ein Token an

Es will das Panel-Token aus der Datei, die der Starter angezeigt hat. Docker: `docker compose exec tgwitness cat /data/panel-token.txt`. Kein Telegram-Code, kein Bot-Token, nicht das Zeugen-Token.

## Telegram stellt keine Verbindung her

Verbindungsprüfung ausführen. Bei einem öffentlichen Proxy einen anderen wählen und speichern. Proxy-Typ und Geheimnisformat prüfen. Listen aktualisieren wechselt die Route nicht von selbst.

## Verbunden, aber keine neuen Nachrichten

1. Läuft die Beobachtung, im richtigen Arbeitsbereich?
2. Ist die Quelle ausgewählt und für dieses Konto sichtbar?
3. Schicken Sie eine eindeutige Nachricht in Ihre Testgruppe und suchen Sie danach.
4. Suchen Sie im Journal nach Unterbrechungen oder Telegram-Fehlern.

Ein ruhiger Chat hat einfach nichts Neues. Wenn Vollständigkeit zählt, machen Sie einen kontrollierten Zustelltest.

## FloodWait oder eine Lücke nach einem Neustart

FloodWait ist Telegram, das „langsamer“ sagt. Abwarten und die Last senken, neu verbinden hilft nicht. Nach einem Neustart holt TgWitness nach, was Telegram noch hat; der Rest ist eine Lücke, notieren Sie sie.

## Der Bot ist konfiguriert, veröffentlicht jedoch nichts

Läuft der Zeuge, darf der Bot im Kanal posten, erreicht er Collector und Bot API? Suchen Sie in seinem Journal nach fehlgeschlagenen Beiträgen. Eine Abfrage auf Collector-Seite heißt nicht, dass ein Beitrag rausging.

## Wo befindet sich die GitHub-Token-Integration?

**In Planung.** Unter „Extras“ wird der vorgeschlagene Workflow zur Fork- und Build-Verifizierung beschrieben. Derzeit gibt es weder ein GitHub-Token-Formular noch eine automatisierte Bestätigung, dass eine laufende Installation mit einem Repository übereinstimmt. Siehe den [aktuellen Status der Funktionen](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/).

Sie melden einen Fehler? Version, Betriebssystem, Schritte und ein bereinigter Fehler. Legen Sie nie Sitzungen, Tokens, private Nachrichten oder das Datenverzeichnis in ein öffentliches Issue.
