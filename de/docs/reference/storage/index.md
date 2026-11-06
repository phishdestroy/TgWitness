# Speicherung und Wiederherstellung

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/storage/

Backups, das Verschieben älterer Dateien in Ihre Cloud, Kopien unter „Object Lock“ und die Wiederherstellung auf einem neuen Rechner.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/de/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Das Panel unterteilt drei Aufgaben:

| Aufgabe | Funktionsweise |
| --- | --- |
| Erstellen Sie ein Backup | Kopieren Sie das signierte Protokoll, die Checkpoints, die gesicherten Dateien und die in der Warteschlange befindlichen Exporte in das konfigurierte S3-Ziel. |
| Kostenloser lokaler Speicherplatz | Kopieren Sie ausgewählte ältere Anhänge auf S3 oder einen rclone-Cloud-Remote, lesen Sie sie vollständig wieder ein, überprüfen Sie die verschlüsselten Bytes und entfernen Sie anschließend die verifizierte lokale Kopie. |
| Bewahren Sie eine Kopie als Beweismittel auf | Konfigurieren Sie „S3 Object Lock“ und überprüfen Sie den zurückgegebenen Aufbewahrungsstatus. Der Dienst muss den angeforderten Modus und das Datum bestätigen. |

Beim Freigeben von Speicherplatz wird das signierte Protokoll niemals gelöscht oder überschrieben. Jeder Anhang behält sein ursprüngliches SHA-256 und eine Wiederherstellungsbestätigung. Eine optionale gzip-Komprimierung erfolgt vor der authentifizierten Verschlüsselung. Cloud-Dateinamen enthalten keine Telegram-Namen, Chat-IDs oder ursprünglichen Anhangsnamen. Ein Anhang darf bis zu 32 GiB groß sein.

Eine Upload-Antwort allein ist keine Erlaubnis zum Löschen einer Datei. TgWitness lädt das vollständige verschlüsselte Objekt herunter, überprüft dessen Größe und SHA-256, speichert die Quittung und überprüft die lokalen Bytes unmittelbar vor dem Löschen erneut. Bei einem fehlgeschlagenen Upload, einer abweichenden Rücklesung oder einer abgebrochenen Übertragung bleibt die lokale Datei erhalten. Falls eine aktivierte Beweissicherung diese Datei noch nicht kopiert hat, wird auch das Löschen darauf gewartet.

**On this page**

- [When the disk is filling up](https://phishdestroy.github.io/TgWitness/de/docs/reference/storage/#when-the-disk-is-filling-up)
- [Connect a destination](https://phishdestroy.github.io/TgWitness/de/docs/reference/storage/#connect-a-destination)
- [Keep the recovery file](https://phishdestroy.github.io/TgWitness/de/docs/reference/storage/#keep-the-recovery-file)
- [Recover after losing the installation](https://phishdestroy.github.io/TgWitness/de/docs/reference/storage/#recover-after-losing-the-installation)
- [Operator bot and completion notices](https://phishdestroy.github.io/TgWitness/de/docs/reference/storage/#operator-bot-and-completion-notices)

## Wenn der Datenträger voll wird

Downloads von Anhängen pausieren unter dem Wert für **Parameter → Anhänge → freier Speicherplatz** (standardmäßig 1 GiB); die Warteschlange bleibt erhalten. Textbeobachtungen laufen weiter. Dies ist unabhängig von Benachrichtigungen: Ihr Abschalten deaktiviert weder die Downloadreserve noch die Speicherschutzprüfungen.

Für einen früheren Eingriff aktivieren Sie **Automatisch ausführen**, wählen **Lokale Datei zum Freigeben von Speicherplatz entfernen** und aktivieren **Zusätzliche Auslagerung bei wenig Speicherplatz starten**. Standardmäßig beginnt diese optionale Regel unter 5120 MiB freiem Speicher und arbeitet in Stapeln, bis 10240 MiB frei sind. Beide Schwellen sind einstellbar. Ziel, Mindestalter, Stapellimit, vollständige Rückleseprüfung und Voraussetzungen zur Beweissicherung entsprechen einem manuellen Lauf. Die Regel aktiviert niemals selbst ein Ziel. Prüfungen erfolgen alle 30 Sekunden; Fehler oder fehlender Fortschritt verschieben den nächsten Versuch um fünf Minuten. Zustand und Wiederholungszeit bleiben nach einem Neustart erhalten. Bei inaktiver Regel nutzen geplante Läufe ihr normales Intervall.

Das Panel zeigt freien Speicher, die Verpackungsreserve, die Bereitschaft der Regel und wegen fehlenden temporären Speichers übersprungene Dateien. Verpacken und Wiederherstellen prüfen vor Beginn ihren maximalen temporären Platzbedarf und während des Schreibens den verfügbaren Speicher. Es gilt die konfigurierte Downloadreserve, für Speichervorgänge jedoch mindestens 64 MiB. Das ist keine Dateisystemquote: Andere Prozesse können zwischen den Prüfungen Speicher verbrauchen.

Gzip komprimiert entfernte Objekte verlustfrei; es verkleinert weder das aktive Journal noch erstellt es lokale Archive. JPEG-, Video- und ZIP-Dateien werden eventuell kaum kleiner oder etwas größer. Mit Komprimierung kann das Verpacken vorübergehend etwa die doppelte Anhanggröße plus Reserve benötigen. Wählen Sie die Startschwelle früh genug für Ihre größten Dateien. Zu große Dateien bleiben erhalten und werden gemeldet; kleinere Dateien und bereits geprüfte entfernte Kopien können weiterhin Platz schaffen. Eine geprüfte Kopie erlaubt das Entfernen der lokalen Datei ohne eine weitere Verpackungsdatei. Auch die Wiederherstellung braucht temporären Speicher und kann bis zu dessen Verfügbarkeit abgelehnt werden.

Ohne geeignete verschiebbare Dateien oder konfiguriertes Ziel kann TgWitness nicht automatisch Speicher freigeben. Die Speicherverwaltung kürzt oder überschreibt das signierte Journal niemals. Es benötigt weiterhin Platz für neue Textbeobachtungen.

## Ein Ziel verbinden

Wählen Sie unter **„Extras“ → „Speicher & Speicherplatz“ → „Speicher verwalten**“ die Aufgabe und das Ziel aus, speichern Sie diese und wählen Sie anschließend **„Upload und Download testen**“. Der Test lädt eine kleine zufällige Testdatei hoch und liest sie wieder ein. Dabei werden keine Telegram-Inhalte verwendet.

Verwenden Sie für S3 den tatsächlichen Endpunkt, die Region und den Bucket des Anbieters. Wasabi, Backblaze, Cloudflare R2 und andere kompatible Dienste verwenden dieselben S3-Einstellungen. Eine kompatible API allein bedeutet nicht, dass Object Lock unterstützt wird. Im Governance-Modus kann ein autorisierter Administrator die Aufbewahrungsfrist möglicherweise umgehen; der Compliance-Modus unterliegt anderen Einschränkungen. Lesen Sie den zurückgegebenen Object-Lock-Status, bevor Sie sich auf die Aufbewahrungsfrist verlassen.

Für ein rclone-Ziel erstellen Sie mithilfe der Provider-Einrichtung von rclone einen Remote und fügen Sie den Abschnitt dieses Remotes `[name]` Abschnitt dieses Remotes in das Bedienfeld ein. Der installierte Helfer unterstützt MEGA, Google Drive, OneDrive, Dropbox, Box, pCloud und die anderen in der Auswahlliste angezeigten Anbieter. Anmeldedaten werden im verschlüsselten Tresor dieses Arbeitsbereichs gespeichert. OAuth- Aktualisierungen werden wieder im Tresor gespeichert. Anmeldedaten werden nicht zu Journal- Ereignissen hinzugefügt oder in Wiederherstellungs-Downloads einbezogen.

Der Helper wird innerhalb des Arbeitsbereichs installiert, mit einer angehefteten Version und SHA-256. Er wird nicht zum System-PATH hinzugefügt. Konfigurations- und Arbeitsdateien sind temporäre Dateien innerhalb dieses Arbeitsbereichs. Befehlsbasierte und lokale Dateiremotes werden abgelehnt. rclone erfordert derzeit eine explizit ausgewählte **„Direct**“-Route für externe Anfragen. Verwenden Sie nativen S3-Speicher für eine SOCKS5- oder HTTP-Route des Arbeitsbereichs; rclone umgeht eine nicht verfügbare Route nicht stillschweigend.

## Bewahre die Wiederherstellungsdatei auf

Wählen Sie nach dem Kopieren der Dateien **Wiederherstellungsdatei speichern** aus und bewahren Sie diese Datei an einem Ort auf, der von der Installation getrennt ist. Sie enthält den Entschlüsselungsschlüssel und signierte Objektbelege, behandeln Sie sie daher wie ein Backup eines privaten Schlüssels. Bewahren Sie die ursprüngliche Remote-Konfiguration und die Ziel-Anmeldedaten ebenfalls separat auf. Eine vor einer späteren Kopie erstellte Wiederherstellungsdatei enthält nicht den Beleg dieser späteren Datei.

Der Fingerabdruck des Signaturschlüssels sollte bereits separat gespeichert worden sein. Eine Signatur, die nur anhand des in derselben Datei enthaltenen Schlüssels überprüft wird, liefert keinen Hinweis darauf, wem die Wiederherstellungsdatei gehört.

Um fehlende Speicherbelege in einem bestehenden Arbeitsbereich wiederherzustellen, öffnen Sie **„Dateien wiederherstellen aus einer gespeicherten Wiederherstellungsdatei“** und wählen Sie die Datei aus. Das Fenster überprüft die Signatur und verlangt denselben Signaturschlüssel des Arbeitsbereichs. Es lehnt es ab, einen anderen Speicherschlüssel zu ersetzen. Wählen Sie anschließend **„Alle Dateien wiederherstellen**“. Die Wiederherstellung pausiert die automatische Speicherregel, sodass der nächste geplante Durchlauf die wiederhergestellten Dateien nicht sofort wieder entfernen kann. Aktivieren Sie die Regel wieder, wenn Sie mit den lokalen Kopien fertig sind.

Bei der Wiederherstellung wird der Chiffretext überprüft, die Entschlüsselung authentifiziert, bei Bedarf dekomprimiert und der ursprüngliche Klartext SHA-256 überprüft, bevor eine Datei in `media/`. Ein beschädigtes Remote-Objekt ersetzt niemals eine lokale Datei. Eine vorhandene lokale Datei mit abweichenden Bytes wird zur Überprüfung beibehalten und nicht überschrieben.

## Wiederherstellung nach Verlust der Installation

Installieren Sie TgWitness auf einem anderen Rechner. Verwenden Sie die private Wiederherstellungsdatei, den separat gespeicherten Fingerabdruck und die ursprünglichen Anmeldedaten für das Zielkonto:

```
python -m tgwitness.storage recover \
  --recovery storage-recovery.json \
  --fingerprint TRUSTED_WORKSPACE_SHA256 \
  --credentials original-rclone.conf \
  --output recovered-attachments
```

Für S3 `--credentials` verweist auf eine private JSON-Datei mit `access_key` und `secret_key`; die signierte Wiederherstellungsdatei liefert die Zieleinstellungen. Der Befehl nutzt eine direkte externe Verbindung und lädt den angehefteten Helper herunter, wenn ein rclone-Remote ihn benötigt. Er lehnt ein bereits vorhandenes Ausgabeverzeichnis ab.

Wiederhergestellte Original-Bytes werden in `recovered-attachments/media/`, benannt nach ihrer SHA-256. `recovery-log.jsonl` ist ein unsignierter Datensatz der Wiederherstellungsvorgänge. Der Befehl stellt ein verlorenes signiertes Journal oder dessen Signaturschlüssel nicht wieder her. Bewahren Sie hierfür eine vollständige Arbeitsbereichssicherung auf. Eine Speicherwiederherstellungsdatei ist keine vollständige Arbeitsbereichssicherung .

## Operator-Bot und Benachrichtigungen bei Fertigstellung

Der Telegram-Bot gehört dem Betreiber. Erstellen Sie ihn über BotFather und legen Sie im Kontrollfeld sein Token, den Ziel-Chat sowie die ausdrücklich zugelassenen Telegram-Benutzer-IDs fest. Sowohl der Absender als auch der Chat müssen übereinstimmen. Weitergeleitete Nachrichten und Befehle von anderen Bots werden ignoriert.

`/status` und `/stats` sind im standardmäßigen „Nur-Status“-Modus verfügbar. Der optionale Steuerungsmodus fügt `/pause`, `/resume` und `/copy`. `/copy` fordert die konfigurierte Speicheraufgabe an; dies bedeutet nicht, dass ein Remote-Upload bereits abgeschlossen ist. Befehle können keine beliebigen URLs, Dateien oder Shell-Programme übergeben.

Verwenden Sie die separaten Benachrichtigungseinstellungen für Warnmeldungen und den Abschluss von Aufgaben. Abschlussbenachrichtigungen unterscheiden einen Kontoexport mit Lücken von einem vollständigen Export und zeigen den Verlauf sowie die Speicherzahlen an. Nachrichtenauszüge werden nur dann einbezogen, wenn dies separat in den Benachrichtigungseinstellungen aktiviert wurde. Die Dienstauswahl wird aus dem tatsächlich installierten Apprise-Katalog generiert und nicht aus einer festen Auswahl an Anbieterbeispielen.
