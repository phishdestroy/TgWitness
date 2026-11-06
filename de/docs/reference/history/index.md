# Quellhistorie laden

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/history/

Laden Sie vergangene Nachrichten aus aktivierten Quellen, halten Sie den Vorgang an und setzen Sie ihn fort, und überprüfen Sie einen signierten Fortschrittsbericht.

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Pause, Neustart und Teilergebnisse

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- Die Nachrichtenbeobachtung, die Anhangsverarbeitung und die Cursor-Festschreibung erfolgen in einer einzigen Transaktion. Bei einem fortgesetzten Lauf werden bereits festgeschriebene Beobachtungen nicht wiederholt. Bei einer Live-Erfassung oder einem separaten, explizit gestarteten Lauf kann dieselbe Nachricht unabhängig davon beobachtet werden.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Nicht zugängliche Quellen und Quellen, die während der Erfassung deaktiviert wurden, bleiben als fehlgeschlagen oder übersprungen sichtbar. Andere Quellen werden weiterverarbeitet; das Gesamtergebnis ist unvollständig.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

Die Vervollständigung des Verlaufs bezieht sich ausschließlich auf das Auslesen des Verlaufs. Anhänge können noch ausstehen, fehlschlagen oder durch die konfigurierte Richtlinie ausgeschlossen werden. Überprüfen Sie Medienbestätigungen im Protokoll und in der Anhangswarteschlange; nur eine abgeschlossene Bestätigung mit erhaltenen Bytes gilt als gespeicherter Anhang. Der Verlaufsvorgang ist eine explizite Snapshot-Anfrage und unterscheidet sich von Schaltern, die Kategorien zukünftiger Live-Ereignisse auswählen.

## Übertragen und überprüfen

Speichern Sie den **signierten Fortschrittsbericht** und verwenden Sie anschließend **„Beweismaterial exportieren“**, um das Protokoll und die gespeicherten Anhänge herunterzuladen. Ein späterer Export des Beweismaterials kann zusätzliche Datensätze enthalten; der Bericht bindet seine Zähler an das Protokollpräfix zum Zeitpunkt seiner Erstellung. Führen Sie den Verifizierer aus einem vertrauenswürdigen Checkout dieser Version aus:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

Der Erfassungscursor entspricht dem lokalen Arbeitsbereichszustand. Das Wiederherstellen einer Beweismittel-ZIP-Datei allein stellt keinen ausstehenden Erfassungsauftrag oder eine Telegram-Sitzung wieder her. Bewahren Sie die Arbeitsbereichssicherung auf, falls eine Fortsetzung des ursprünglichen Auftrags erforderlich ist.
