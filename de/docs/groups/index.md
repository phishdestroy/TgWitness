# Telegram · Verwalten Sie eine Gruppe von Konten

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/groups/

Betreiben Sie mehrere Konten zusammen, jedes weiterhin mit eigenen Einträgen und eigenem Schlüssel.

Eine Gruppe bringt Verbindungsstatus, Start/Pause, gemeinsame Einstellungen und Exporte auf einen Bildschirm. Praktisch, wenn mehrere Konten am selben Fall arbeiten.

## Gruppenübersicht öffnen

Öffnen Sie die Gruppe unter **Konten**. Jedes Konto zeigt Status, Route, Latenz und letzte gespeicherte Nachricht. **Erfordert Aufmerksamkeit** listet die defekten, **Beheben** bringt Sie direkt hin.

**Alle starten** / **Alle pausieren** fragen vorher nach. **Gruppeneinstellungen** werden geteilt, aber die eigenen Werte eines Kontos bleiben, bis Sie sie ersetzen.

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

1. **Gruppenroute ändern**, Typ und Einstellungen wählen.
2. **Auswahl prüfen**: welche Konten sich ändern und welche eine eigene Route haben.
3. **Vorbereiten und prüfen** testet eine frische Telegram-Verbindung und, wo möglich, die Ausgangs-IP.
4. **Geprüfte Verbindung anwenden** und jedes Ergebnis ansehen. Laufende Konten machen weiter, inaktive bleiben inaktiv.

Latenz ist die Zeit für den Verbindungsaufbau zu Telegram, die Ausgangs-IP ist das, was die Route bei der Prüfung zeigte. Ergebnisse können je Konto abweichen.

## Verwenden Sie überlappende Zugriffsrechte

**Chats, die mehrere Konten sehen** listet gemeinsame Quellen und ihre Abdeckung. Kanäle und Supergruppen lassen sich mit **Mit … Konten exportieren** von mehreren Konten gleichzeitig exportieren. Private Chats und einfache Gruppen nicht, ihre Nachrichtennummern gelten pro Konto.

## Die Gruppe als Paket exportieren

**Gruppe exportieren** liefert ein ZIP mit dem signierten Export jedes Kontos und einer signierten Liste davon. Jedes behält seinen Fingerabdruck für die Prüfung. Eine zusammengeführte Zeitleiste bauen Sie weiterhin selbst.

Weiter: [Berichte](https://phishdestroy.github.io/TgWitness/de/docs/reports/), [Case Board](https://phishdestroy.github.io/TgWitness/de/docs/case-board/), [Exporte prüfen](https://phishdestroy.github.io/TgWitness/de/docs/exports/).
