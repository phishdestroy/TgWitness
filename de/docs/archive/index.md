# Telegram · Das Archiv bearbeiten

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/archive/

Die Nachricht finden. Die Quelle überprüfen. Den Fall aufbauen.

01**Den Verlauf einbeziehen**

Holen Sie frühere Nachrichten Ihrer aktiven Quellen in den Arbeitsbereich.

02**Den Quellen folgen**

Suchen Sie und öffnen Sie dann die gespeicherte Nachricht hinter jedem Treffer.

03**Sorgen Sie für eine klare Übergabe**

Ihre Analyse in einer Datei, die signierten Beweise daneben.

Erfasste Datensätze, erkannter Text und Schlussfolgerungen der Analysten bleiben klar voneinander getrennt.

## Frühere Nachrichten laden

1. **Quellen → Chats im Umfang**: aktive Chats prüfen, Beobachtung starten.
2. **Gesamten Verlauf laden**. Nimmt die Quellenliste, wie sie gerade ist.
3. **Verlauf pausieren** / **Verlauf fortsetzen** jederzeit. Nach einem Neustart von Hand fortsetzen.
4. Ergebnisse pro Quelle und die Download-Warteschlange prüfen, den signierten Fortschrittsbericht beim Export behalten.

Das füllt den Arbeitsbereich. Ein Einzel-Chat-Export als HTML/JSON ist etwas anderes. [Details](https://phishdestroy.github.io/TgWitness/de/docs/reference/history/).

## Erst suchen, dann über KI entscheiden

1. **Journal** sucht lokal, filtert nach Quelle und Zeit.
2. Suchen Sie eine Phrase oder Domain, öffnen Sie den Eintrag und seine Versionen.
3. Für KI richtet der Admin einen Anbieter unter **Integrationen** ein. Dann **Archiv fragen**: Chats und Zeitraum wählen, **An das Modell gesendete Daten** ansehen und abwählen, was nicht raus soll.
4. Zitate prüfen, Antwort als Bericht speichern, eigene Notizen ergänzen.

Die Suche braucht keine KI. Berichte behalten Quellen und Revisionen, getrennt vom signierten Journal. [Anbieter einrichten](https://phishdestroy.github.io/TgWitness/de/docs/reference/analysis/).

## Wählen Sie die gewünschte Verbindung aus

| Aufgabe | Öffnen | Einrichtung |
| --- | --- | --- |
| Einen KI-Client ausgewählte Chats lesen lassen | **Integrationen → MCP** | [MCP installieren, begrenztes Token erstellen, verbinden](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/) |
| Text in gespeicherten Medien erkennen | Ein `media.saved`-Eintrag → **Anhang erkennen** | [Den lokalen Docker-Worker einrichten](https://phishdestroy.github.io/TgWitness/de/docs/reference/media-analysis/) |
| Ereignisse an n8n oder ein SIEM senden | **Integrationen → Ausgehende Webhooks** | [Empfänger hinzufügen, HMAC prüfen, IDs entduplizieren](https://phishdestroy.github.io/TgWitness/de/docs/reference/webhooks/) |

**Welches Zugriffstoken gehört wohin?**

Panelzugang ist für Menschen. MCP bekommt eigene Nur-Lese-Tokens, Webhooks ein eigenes HMAC-Geheimnis. Keiner davon braucht eine Telegram-Sitzung.

[Zugriff auf das Share-Panel gewähren](https://phishdestroy.github.io/TgWitness/de/docs/access/) oder [einen MCP-Client konfigurieren](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/).

## Quellen und Schlussfolgerungen angeben

Legen Sie den Bericht neben das signierte ZIP. Der Bericht ist Ihre Lesart der Quellen, das ZIP ist das, was der Empfänger prüft.

[Exportieren und verifizieren](https://phishdestroy.github.io/TgWitness/de/docs/exports/) · [Durchführung einer vollständigen Untersuchung](https://phishdestroy.github.io/TgWitness/de/docs/cases/)
