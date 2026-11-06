# Quellhistorie laden

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/history/

Laden Sie vergangene Nachrichten aus aktivierten Quellen, halten Sie den Vorgang an und setzen Sie ihn fort, und überprüfen Sie einen signierten Fortschrittsbericht.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Sammlung](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Sammlung](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

Überprüfen Sie in „**Sources**“ die aktivierten Chats, unterbrechen Sie die Beobachtung, wählen Sie Standard-API oder Takeout-Export und wählen Sie anschließend „**Vollständigen Verlauf laden**“. Der Durchlauf korrigiert diese Quellenliste und liest die verfügbaren früheren Nachrichten in Chats und das signierte Beobachtungsprotokoll ein. Medien verwendet die vorhandenen Einstellungen für Anhänge und die dauerhafte Download-Warteschlange. Dies ist unabhängig vom signierten JSON/HTML-Export pro Chat.

Für eine kontoweite Erfassung wählen Sie **Gesamtes Konto**, starten Sie die Beobachtung, um die Quellliste zu laden, und überprüfen Sie diese Liste, bevor Sie den Verlauf starten. Die Begrenzung der Dialogliste gilt weiterhin (standardmäßig 1,000, einstellbar unter Parameter). Ein erfolgreicher Durchlauf beweist nicht, dass jeder Kontodialog aufgelistet wurde. Später entdeckte oder aktivierte Chats erfordern einen weiteren Durchlauf. Halten Sie die Beobachtung an, bevor Sie den Verlauf starten; jeweils nur eine Erfassung kann ein Konto erfassen.

Wählen Sie ein bis fünf Anhangs-Worker aus und legen Sie fest, ob verfügbare Aktuelle Aktionen beibehalten und zuvor gespeicherte Versionen verglichen werden sollen. Die Entnahme erfordert möglicherweise eine Genehmigung in Telegram und eine vom Server festgelegte Wartezeit. Diese Optionen bleiben bei der Wiederaufnahme unverändert. Siehe [Backfill-Verhalten und Beweiskontrakt](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) für Details zu Transport, Wiederholungsversuchen und Vertrauenswürdigkeit.

## Pause, Neustart und Teilergebnisse

- **Verlauf anhalten** unterbricht das Einlesen. **Verlauf fortsetzen** setzt den Ablauf ab der zuletzt gespeicherten Nachricht in jeder Quelle fort; beim Neustart der App bleibt der Ablauf ebenfalls angehalten, bis er fortgesetzt wird. Zur Fortsetzung ist dasselbe inaktive Telegram-Konto erforderlich.
- Die Nachrichtenbeobachtung, die Anhangsverarbeitung und die Cursor-Festschreibung erfolgen in einer einzigen Transaktion. Bei einem fortgesetzten Lauf werden bereits festgeschriebene Beobachtungen nicht wiederholt. Bei einer Live-Erfassung oder einem separaten, explizit gestarteten Lauf kann dieselbe Nachricht unabhängig davon beobachtet werden.
- Jede Quelle (jeder Telegram-Split-Bereich in Takeout) legt beim ersten Lesen eine obere Nachrichten-ID fest. Neuere Nachrichten gehören zur Live-Beobachtung und nicht zu den verbleibenden historischen Seiten dieser Quelle.
- Nicht zugängliche Quellen und Quellen, die während der Erfassung deaktiviert wurden, bleiben als fehlgeschlagen oder übersprungen sichtbar. Andere Quellen werden weiterverarbeitet; das Gesamtergebnis ist unvollständig.
- FloodWait-Verzögerungen berücksichtigen die gespeicherte Backoff-Zeit des Kontos. Bei vorübergehenden Fehlern werden bis zu fünf Wiederholungsversuche unternommen; bei Erschöpfung der Kontingente und geringem Speicherplatz wird die Ausführung mit erhaltenem Cursor unterbrochen.
- **Beendet diesen Verlaufslauf.** bewahrt gespeicherte Beobachtungen. Es entfernt diese nicht und bricht keine Anhangsaufträge der Standard-API ab. Das Beenden von Takeout markiert die verbleibenden Takeout-Dateien als übersprungen; beim Anhalten bleiben sie wiederherstellbar. Ein neuer Lauf liest aktivierte Quellen erneut ein.

Die Vervollständigung des Verlaufs bezieht sich ausschließlich auf das Auslesen des Verlaufs. Anhänge können noch ausstehen, fehlschlagen oder durch die konfigurierte Richtlinie ausgeschlossen werden. Überprüfen Sie Medienbestätigungen im Protokoll und in der Anhangswarteschlange; nur eine abgeschlossene Bestätigung mit erhaltenen Bytes gilt als gespeicherter Anhang. Der Verlaufsvorgang ist eine explizite Snapshot-Anfrage und unterscheidet sich von Schaltern, die Kategorien zukünftiger Live-Ereignisse auswählen.

## Übertragen und überprüfen

Speichern Sie den **signierten Fortschrittsbericht** und verwenden Sie anschließend **„Beweismaterial exportieren“**, um das Protokoll und die gespeicherten Anhänge herunterzuladen. Ein späterer Export des Beweismaterials kann zusätzliche Datensätze enthalten; der Bericht bindet seine Zähler an das Protokollpräfix zum Zeitpunkt seiner Erstellung. Führen Sie den Verifizierer aus einem vertrauenswürdigen Checkout dieser Version aus:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Behalten Sie den erwarteten Fingerabdruck des Signaturschlüssels separat bei. Der Verifizierer überprüft die Berichtsignatur, das Beweisarchiv, den Bericht-Checkpoint, den Quellplan, das Konto sowie die Anzahl der gespeicherten bzw. nicht verfügbaren Nachrichten. Neue Durchläufe binden zudem den Quellfortschritt und Optionen an signierte Cursor-Ereignisse. Ohne `--evidence` werden nur der signierte Bericht und dessen interne Konsistenz geprüft. Ältere Fortschrittsfelder und Anhangszusammenfassungen bleiben signierte Aussagen des Sammlers. Der Beweisprüfer überprüft archivierte Medienbytes.

Weder das Signieren noch das Vervollständigen des verfügbaren Verlaufs beweisen die Herkunft aus Telegram, einen atomaren Snapshot oder historische Vollständigkeit. Nachrichten können sich während des Lesens ändern; gelöschte Nachrichten und zwischenzeitliche Bearbeitungen außerhalb der verfügbaren Jüngsten Aktionen sowie geheime Chats werden nicht wiederhergestellt. Ein Betreiber, der den Signaturschlüssel kontrolliert, kann ein Protokoll fälschen, bevor externe Verpflichtungen bestehen. Verwenden Sie separat gespeicherte Kontrollpunkte oder einen unabhängigen Zeugen für die dokumentierten Eigenschaften zur Manipulationserkennung.

Der Erfassungscursor entspricht dem lokalen Arbeitsbereichszustand. Das Wiederherstellen einer Beweismittel-ZIP-Datei allein stellt keinen ausstehenden Erfassungsauftrag oder eine Telegram-Sitzung wieder her. Bewahren Sie die Arbeitsbereichssicherung auf, falls eine Fortsetzung des ursprünglichen Auftrags erforderlich ist.
