# Verwalten Sie eine Gruppe von Konten

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/groups/

Verwalten Sie mehrere Erfassungskonten gleichzeitig und halten Sie dabei die Datensätze sowie die Signaturidentität jedes Kontos getrennt.

Eine Kontengruppe fasst Verbindungsstatus, Überwachungssteuerungen, gemeinsame Einstellungen und Exporte in einer Arbeitsansicht zusammen. Dies ist nützlich, wenn mehrere Konten dieselbe Untersuchung abdecken oder eine einheitliche Betriebskonfiguration benötigen.

## Gruppenübersicht öffnen

Öffnen Sie in **„Accounts**“ die Gruppe. Zu jedem Account werden der Beobachtungsstatus, die Verbindungsroute, die zuletzt gemessene Routenlatenz bei erfolgreicher aktueller Überprüfung sowie die zuletzt gespeicherte Nachricht angezeigt. Links **mit dem Hinweis „Beachtung erforderlich“** verweisen auf die Accounts, die bearbeitet werden müssen; über **„Fix“** werden der entsprechende Arbeitsbereich und die Steuerung geöffnet.

**„Alle starten“** und **„Alle anhalten“** wirken sich nach Bestätigung auf berechtigte Konten aus. **Gruppeneinstellungen** geben ausgewählte Einstellungen frei; Konten mit eigenen Werten behalten diese bei, bis Sie sich entscheiden, sie zu überschreiben.

### Überprüfen Sie eine Routenänderung innerhalb einer Gruppe

Fiktives Beispiel · illustrative Prüfungen und Ergebnisse

1. **Auswählen.** Wählen Sie die Gruppe aus und prüfen Sie, welche Konten sich ändern werden.
2. **Vorbereitung:** Behalten Sie den eigenen Pfad eines Kontos bei, wenn dieser getrennt bleiben soll.
3. **Überprüfen.** Testen Sie die vorgeschlagene Verbindung und überprüfen Sie die Messergebnisse.
4. **Anwenden.** Vor dem Speichern noch einmal überprüfen und das Ergebnis für jedes Konto kontrollieren.

#### Fallteam

Kanal-Collector · Gruppen-Collector · Referenzkonto

3 separate Arbeitsbereiche

#### Überprüfte Auswahl

2 Konten folgen dem vorgeschlagenen Vorgehen.

Das Referenzkonto verfügt über eine eigene Route.

#### Vorbereitungsprüfungen

Kanal-Collector: Telegram-Übertragungszeit 84 ms

Gruppen-Collector: Telegram-Übertragungszeit 91 ms

Diese Zahlen sind fiktive Messwerte für das Beispiel.

#### Anwendungsergebnisse

Kanal-Collector: Speicherung abgeschlossen, Beobachtung fortgesetzt.

Gruppen-Collector: Überprüfung fehlgeschlagen, vorherige Einstellungen wiederhergestellt.

Referenzkonto: eigene Route beibehalten.

## Ändern Sie die Route mit einem Überprüfungsschritt

1. Wählen Sie **„Gruppenroute ändern**“ und legen Sie anschließend den Verbindungstyp und die Einstellungen fest.
2. Wählen Sie **„Auswahl überprüfen**“. Überprüfen Sie die aufgelisteten Konten und deren individuelle Routenüberschreibungen.
3. Wählen Sie **„Vorbereiten und prüfen**“. Bei der Prüfung wird ein neuer Telegram-Transport verwendet; unterstützte HTTP-Routen melden zudem ihre HTTPS-Ausgangsprüfung.
4. Wählen Sie **„Markierte Verbindung anwenden“** und überprüfen Sie das Ergebnis jedes Kontos. Zuvor laufende Überwachungen werden dort fortgesetzt, wo die Anwendung erfolgreich ist; inaktive Konten bleiben inaktiv.

Die Latenz beschreibt den gemessenen Aufbau der Telegram-Verbindung. Eine Exit-IP-Prüfung beschreibt diese Route zum Zeitpunkt der aufgezeichneten Überprüfung. Die Kontoautorisierung und der Zustand der Überwachung haben eigene Indikatoren; eine Gruppenänderung kann je nach Konto zu unterschiedlichen Ergebnissen führen.

## Verwenden Sie überlappende Zugriffsrechte

**Unter „Chats mehrerer Konten anzeigen“** werden gemeinsam genutzte Quellen und der verfügbare Erfassungsbereich im Arbeitsbereich angezeigt. Berechtigte Kanäle und Supergruppen können **die** **Funktion** **„Exportieren mit … Konten“** nutzen, um die Erfassung des Chatverlaufs eines Chats aufzuteilen. Private Chats und normale Gruppen verbleiben beim Startkonto, da ihre Nachrichtenzahlen zum Verlauf dieses Kontos gehören.

## Die Gruppe als Paket exportieren

**Die Exportgruppe** erstellt eine ZIP-Datei, die den signierten Export jedes Kontos sowie eine signierte Liste dieser Dateien enthält. Die ursprünglichen Identitäten und Fingerabdrücke des Arbeitsbereichs bleiben zur Überprüfung verfügbar. Erstellen Sie anhand dieser Referenzen eine kontoübergreifende Darstellung; eine einzige zusammengeführte Zeitleiste wird weiterhin separat zusammengestellt.

Fahren Sie mit [der Berichtsgestaltung](https://phishdestroy.github.io/TgWitness/de/docs/reports/), [einem Case Board innerhalb eines Arbeitsbereichs](https://phishdestroy.github.io/TgWitness/de/docs/case-board/) oder [der Exportüberprüfung](https://phishdestroy.github.io/TgWitness/de/docs/exports/) fort.
