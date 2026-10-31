# Das Archiv bearbeiten

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/archive/

Die Nachricht finden. Die Quelle überprüfen. Den Fall aufbauen.

Diese Tools sind im aktuellen Hauptzweig verfügbar. Die portable Vorschauversion 0.7.0 ist älter als diese; verwenden Sie für diesen Arbeitsablauf einen Quellcode-Checkout.

01**Den Verlauf einbeziehen**

Laden Sie vergangene Nachrichten aus Ihren aktivierten Quellen in den Arbeitsbereich.

02**Den Quellen folgen**

Durchsuchen Sie das Archiv und öffnen Sie die hinter jedem Ergebnis gespeicherte Nachricht.

03**Sorgen Sie für eine klare Übergabe**

Speichern Sie Ihre Analyse separat und exportieren Sie die signierten Beweismittel daneben.

Erfasste Datensätze, erkannter Text und Schlussfolgerungen der Analysten bleiben klar voneinander getrennt.

## Frühere Nachrichten laden

1. Öffnen Sie „Open **Sources“**, überprüfen Sie die aktivierten Chats und beginnen Sie mit der Beobachtung.
2. Wählen Sie **„Vollständigen Verlauf laden**“. Der Durchlauf verwendet die zu diesem Zeitpunkt ausgewählte Quellenliste.
3. Verwenden Sie **„Pause-Verlauf“** und **„Weiter-Verlauf“** nach Bedarf. Setzen Sie nach einem Neustart die Arbeit explizit fort.
4. Überprüfen Sie die Ergebnisse pro Quelle und die Warteschlange der Anhänge. Speichern Sie den signierten Fortschrittsbericht zusammen mit dem Beweismittelexport.

Dadurch wird der Arbeitsbereich mit den verfügbaren Nachrichten gefüllt. Ein HTML-/JSON-Export pro Chat ist ein separater Vorgang. [Details zu Verlauf und Wiederherstellung](https://phishdestroy.github.io/TgWitness/de/docs/reference/history/).

## Erst suchen, dann über KI entscheiden

1. Öffnen **Sie das Archiv**. Wählen Sie einen Arbeitsbereich, Chats und einen Beobachtungszeitraum aus.
2. Suchen Sie nach einem Begriff, einer Domain oder einer Nachrichten-ID. Öffnen Sie den entsprechenden Datensatz und seine gespeicherten Versionen.
3. Für die KI-Analyse konfiguriert der Administrator zunächst einen Anbieter. Überprüfen Sie **die an das Modell gesendeten Daten** und deaktivieren Sie unerwünschte Auszüge, bevor Sie die Anfrage genehmigen.
4. Überprüfen Sie die angezeigten Quellenangaben. Speichern Sie die Antwort als Bericht und fügen Sie Ihre eigenen Überarbeitungen oder Anmerkungen hinzu.

Die Suche erfolgt lokal ohne KI. Analytische Berichte enthalten Quellenangaben und einen Revisionsverlauf; sie sind vom signierten Protokoll getrennt. [Einrichtung durch den Anbieter und Berichte](https://phishdestroy.github.io/TgWitness/de/docs/reference/analysis/).

## Wählen Sie die gewünschte Verbindung aus

| Aufgabe | Öffnen | Einrichtung |
| --- | --- | --- |
| Ausgewählte Chats eines KI-Clients lesen | **Integrationen → MCP** | [Installieren Sie das MCP-Extra, generieren Sie ein Scoped-Token und verbinden Sie den Client](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/) |
| Text in gespeicherten Medien erkennen | Ein `media.saved`-Eintrag → **Anhang erkennen** | [Richten Sie den lokalen Docker-Worker und die erforderlichen Sprach- und Modelldateien ein](https://phishdestroy.github.io/TgWitness/de/docs/reference/media-analysis/) |
| Ereignisse an n8n oder ein SIEM senden | **Integrationen → Ausgehende Webhooks** | [Empfänger hinzufügen, HMAC überprüfen und Ereignis-IDs deduplizieren](https://phishdestroy.github.io/TgWitness/de/docs/reference/webhooks/) |

**Welches Zugriffstoken gehört wohin?**

Der Zugriff auf das Panel ist den Personen vorbehalten, die den Fall prüfen. MCP-Anbindungen erhalten separate, schreibgeschützte Archiv-Token. Ein Webhook-Empfänger verwendet sein eigenes HMAC-Geheimnis. Es wird keine Telegram-Sitzungsdatei benötigt.

[Zugriff auf das Share-Panel gewähren](https://phishdestroy.github.io/TgWitness/de/docs/access/) oder [einen MCP-Client konfigurieren](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/).

## Quellen und Schlussfolgerungen angeben

Bewahren Sie den geprüften Analysebericht zusammen mit der signierten ZIP-Datei mit den Beweismitteln auf. Der Bericht erläutert Ihre Interpretation der Quellen; die ZIP-Datei ermöglicht es dem Empfänger, die gespeicherten Aufzeichnungen anhand eines unabhängig vertrauenswürdigen Fingerabdrucks und Checkpoints zu überprüfen.

[Exportieren und verifizieren](https://phishdestroy.github.io/TgWitness/de/docs/exports/) · [Durchführung einer vollständigen Untersuchung](https://phishdestroy.github.io/TgWitness/de/docs/cases/)
