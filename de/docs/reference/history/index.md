# Quellhistorie laden

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/history/

Laden Sie vergangene Nachrichten aus aktivierten Quellen, halten Sie den Vorgang an und setzen Sie ihn fort, und überprüfen Sie einen signierten Fortschrittsbericht.

**Aktuelle Hauptversion:** über den Quellcode verfügbar; nicht in der portablen Vorschauversion 0.7.0 enthalten.

Überprüfen Sie unter **„Quellen**“ die aktivierten Chats, starten Sie die Beobachtung und wählen Sie anschließend **„Gesamten Verlauf laden**“. Der Durchlauf legt diese Liste von Quellen fest und liest deren verfügbare vergangene Nachrichten in „Chats“ und das signierte Beobachtungsprotokoll ein. Medien verwenden die bestehenden Einstellungen für Anhänge und die dauerhafte Download-Warteschlange. Dies ist unabhängig vom signierten JSON/HTML-Export pro Chat.

Für die kontoweite Erfassung wählen Sie **„Gesamtes Konto“** aus, starten Sie die Beobachtung, um die Quellenliste zu laden, und überprüfen Sie diese Liste, bevor Sie den Verlauf starten. Die Begrenzung der Dialogliste gilt weiterhin (standardmäßig 1.000, einstellbar unter „Parameter“). Ein erfolgreicher Durchlauf beweist nicht, dass jeder Kontodialog aufgeführt wurde. Später entdeckte oder aktivierte Chats erfordern einen weiteren Durchlauf.

## Pause, Neustart und Teilergebnisse

- **Mit „Verlauf anhalten“** wird das Einlesen unterbrochen. **Mit „Weiter“** wird **der Verlauf** ab der zuletzt gespeicherten Nachricht in jeder Quelle fortgesetzt; auch beim Neustart der App bleibt der Lauf angehalten, bis er fortgesetzt wird. Starten Sie zunächst die Beobachtung neu. Zum Fortsetzen ist dasselbe Telegram-Konto erforderlich.
- Die Nachrichtenbeobachtung, die Anhangsverarbeitung und die Cursor-Festschreibung erfolgen in einer einzigen Transaktion. Bei einem fortgesetzten Lauf werden bereits festgeschriebene Beobachtungen nicht wiederholt. Bei einer Live-Erfassung oder einem separaten, explizit gestarteten Lauf kann dieselbe Nachricht unabhängig davon beobachtet werden.
- Jede Quelle legt beim ersten Einlesen eine obere Nachrichten-ID fest. Neuere Nachrichten gehören zur Live-Beobachtung und nicht zu den verbleibenden historischen Seiten dieser Quelle.
- Nicht zugängliche Quellen und Quellen, die während der Erfassung deaktiviert wurden, bleiben als fehlgeschlagen oder übersprungen sichtbar. Andere Quellen werden weiterverarbeitet; das Gesamtergebnis ist unvollständig.
- FloodWait-Verzögerungen berücksichtigen die für das gespeicherte Konto festgelegte Wartezeit. Transport-Timeouts und unzureichender Festplattenspeicher unterbrechen den Lauf, wobei der Cursor an seiner Position verbleibt. Der Lauf wird fortgesetzt, sobald die Ursache behoben ist.
- **Das Beenden dieses Verlaufslaufs** bewahrt die gespeicherten Beobachtungen. Es entfernt sie nicht und bricht bereits in der Warteschlange befindliche Anhang-Downloads nicht ab. Ein neuer Lauf liest die aktivierten Quellen erneut ein.

Die Vervollständigung des Verlaufs bezieht sich ausschließlich auf das Auslesen des Verlaufs. Anhänge können noch ausstehen, fehlschlagen oder durch die konfigurierte Richtlinie ausgeschlossen werden. Überprüfen Sie Medienbestätigungen im Protokoll und in der Anhangswarteschlange; nur eine abgeschlossene Bestätigung mit erhaltenen Bytes gilt als gespeicherter Anhang. Der Verlaufsvorgang ist eine explizite Snapshot-Anfrage und unterscheidet sich von Schaltern, die Kategorien zukünftiger Live-Ereignisse auswählen.

## Übertragen und überprüfen

Speichern Sie den **signierten Fortschrittsbericht** und verwenden Sie anschließend **„Beweismaterial exportieren“**, um das Protokoll und die gespeicherten Anhänge herunterzuladen. Ein späterer Export des Beweismaterials kann zusätzliche Datensätze enthalten; der Bericht bindet seine Zähler an das Protokollpräfix zum Zeitpunkt seiner Erstellung. Führen Sie den Verifizierer aus einem vertrauenswürdigen Checkout dieser Version aus:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Bewahren Sie den erwarteten Fingerabdruck des Signaturschlüssels separat auf. Der Prüfer überprüft die Berichtsignatur, das Beweismittelarchiv, den Berichts-Checkpoint, den Quellenplan, das Konto sowie die Anzahl der gespeicherten bzw. nicht verfügbaren Nachrichten. Ohne „`--evidence`“ überprüft er lediglich den signierten Bericht und dessen interne Konsistenz. Fortschrittsphasen, Titel, Cursor und Zusammenfassungen der Anhänge sind signierte Erklärungen des Erfassers und werden nicht unabhängig von diesem Berichtsprüfer rekonstruiert. Der Beweismittelprüfer überprüft weiterhin die archivierten Medienbytes.

Weder die Signierung noch die Vervollständigung des verfügbaren Verlaufs beweisen die Herkunft aus Telegram, einen atomaren Momentabbild oder die historische Vollständigkeit. Nachrichten können sich während des Lesens ändern; gelöschte Nachrichten, ungesehene zwischenzeitliche Bearbeitungen und geheime Chats werden nicht wiederhergestellt. Ein Betreiber, der den Signaturschlüssel kontrolliert, kann ein Protokoll fälschen, bevor externe Verpflichtungen bestehen. Verwenden Sie separat gespeicherte Kontrollpunkte oder einen unabhängigen Zeugen, um die dokumentierten Manipulationserkennungseigenschaften zu gewährleisten.

Der Erfassungscursor entspricht dem lokalen Arbeitsbereichszustand. Das Wiederherstellen einer Beweismittel-ZIP-Datei allein stellt keinen ausstehenden Erfassungsauftrag oder eine Telegram-Sitzung wieder her. Bewahren Sie die Arbeitsbereichssicherung auf, falls eine Fortsetzung des ursprünglichen Auftrags erforderlich ist.
