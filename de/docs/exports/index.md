# Exportieren und verifizieren

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/exports/

Stellen Sie dem Empfänger Dateien zur Verfügung, die er mit dem Erfassungsarbeitsbereich und dessen gespeichertem Verlauf abgleichen kann.

Bitte verweisen Sie daraufSignierte ZIP-Datei exportierenDer Empfänger überprüft

Sind Sie neu im Bereich Signaturen und Prüfpunkte? [Ändern Sie einen Beispieldatensatz](https://phishdestroy.github.io/TgWitness/de/docs/concepts/#chain) und sehen Sie, welche Prüfungen dies erkennen.

Möchten Sie eine Kopie außerhalb des Datensammlers aufbewahren? Gehen Sie zu [„S3-Einrichtung“](https://phishdestroy.github.io/TgWitness/de/docs/exports/#s3), [„Objekt-Sperre“](https://phishdestroy.github.io/TgWitness/de/docs/exports/#s3-retention) oder [„verifizierte Wiederherstellung](https://phishdestroy.github.io/TgWitness/de/docs/exports/#s3-restore)“.

## Eine vertrauenswürdige Referenz bereitstellen

Speichern Sie den Fingerabdruck des öffentlichen Schlüssels des Arbeitsbereichs außerhalb des Erfassungssystems. Bewahren Sie während der Erfassung signierte Kontrollpunkte an einem anderen Ort auf oder nutzen Sie einen [unabhängigen Zeugen](https://phishdestroy.github.io/TgWitness/de/docs/witness/). Anhand dieser Referenzen kann ein Empfänger den Schlüssel und eine frühere Protokollgrenze überprüfen.

## Laden Sie die signierte ZIP-Datei herunter

Öffnen Sie **„Exports“** und erstellen Sie eine signierte ZIP-Datei mit Beweismaterial. Diese enthält das vollständige Arbeitsprotokoll sowie ein signiertes Dateimanifest. Verwenden Sie [„Report Studio“](https://phishdestroy.github.io/TgWitness/de/docs/reports/), um einen übersichtlichen Bericht zu erstellen, oder einen [Übergabeauszug](https://phishdestroy.github.io/TgWitness/de/docs/handover/), um nur ausgewählte, minimierte Daten zu übermitteln.

HTML-, PDF- und JSON-Berichte sind mit eigenen Signatursiegeln versehen und können separat überprüft werden. CSV-Dateien dienen als praktische Analysekopie; verwenden Sie die exakte CSV-Datei aus der verifizierten ZIP-Datei, um deren Integrität zu überprüfen. Bewahren Sie die signierte ZIP-Datei auf, wenn der Empfänger auch die Quelldatensätze und Anhänge benötigt.

## Überprüfen Sie dies anhand einer vertrauenswürdigen Kopie von TgWitness

Ersetzen Sie in der installierten Projektumgebung den Beispiel-Fingerabdruck und die Dateipfade:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Wenn beide Referenzen erfolgreich sind, werden im Ergebnis „`key_pinned: true`“ und „`checkpoint_checked: true`“ angezeigt. Bewahren Sie das Verifizierungsergebnis zusammen mit dem Originalarchiv auf. Der beibehaltene Prüfpunkt muss an der Grenze des Exports oder davor liegen.

## Verwenden Sie das Verifizierungsergebnis

- **Überprüfen Sie die gelieferten Dateien:** Das Manifest verknüpft deren Hashes, und Datensatzsignaturen verknüpfen das gespeicherte Protokoll. Eine geänderte Datei oder eine unterbrochene Datensatzkette wird erkannt.
- **Überprüfen Sie die Identität des Arbeitsbereichs:** Der unabhängig gespeicherte Fingerabdruck identifiziert den von Ihnen erwarteten Signaturschlüssel.
- **Vergleichen Sie eine frühere Grenze:** Ein beibehaltener Checkpoint gleicht den Export mit einem vor der Übergabe gespeicherten Journalpräfix ab.
- **Überprüfen Sie den Erfassungsumfang:** Lücken, Erfassungsergebnisse und ein kontrollierter Test mit den Schritten „Senden → Bearbeiten → Löschen“ beschreiben die Ereignisse, die diese Konfiguration erfasst hat.

Bewahren Sie diese Ergebnisse zusammen mit der Kopie des Empfängers auf. Prüfen Sie, [was die Verifizierung](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope) hinsichtlich des Umfangs der Überprüfungen und der separaten Bewertung von Quellenangaben und Erfassungsgrad [ergibt](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope).

## Richten Sie die externe S3-Kopie ein

Öffnen Sie in Ihrem aktiven Arbeitsbereich **„Exporte“ → „Externe Kopie**“. Diese optionale Funktion ist mit AWS S3 und anderen S3-kompatiblen Diensten kompatibel. Sie kopiert Protokollsegmente, gesicherte Fotos und Dateien, Checkpoints mit ihren Zeitstempel-Antworten sowie abgeschlossene Chat-Exporte. Jedes Objekt wird vor dem Hochladen auf dem Collector mit „`AES-256-GCM`“ verschlüsselt.

Die Online-Demo zeigt dieselben Bedienelemente, wobei das Hochladen deaktiviert ist. Geben Sie Ihre Speicherzugangsdaten bitte nur in Ihrem eigenen, laufenden Arbeitsbereich ein.

[![Vollständiges Off-Site-Kopier-Panel: Endpunkt, Region, Bucket, Zugriffsschlüssel, Zeitplan, „Object Lock“- und Wiederherstellungsschlüssel-Steuerelemente](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Das vollständige Bedienfeld mit erweiterten Optionen ist aufgeklappt. Es werden keine Anmeldedaten für den Speicher angezeigt.

| Fachgebiet | Was ist einzugeben? |
| --- | --- |
| Endpunkt | Die URL des Speicherdienstes, ohne Bucket-Pfad oder Anmeldedaten. Fiktives Beispiel: `https://s3.example.invalid`. |
| Region | Die von Ihrem Provider geforderte Region. Die Standardeinstellung der Anwendung lautet „`us-east-1`“. |
| Bucket | Ein bereits vorhandener Bucket, auf den Sie zugreifen können. Fiktives Beispiel: `example-case-backup`. |
| Ordner im Bucket | Das Objektpräfix; Standardwert `tgwitness`. Die Anwendung fügt ein Präfix hinzu, das aus dem Fingerabdruck des Signaturschlüssels dieses Arbeitsbereichs abgeleitet wird. |
| Zugriffs-ID / Geheimer Zugangsschlüssel | Geben Sie beide Speicherzugangsdaten gemeinsam ein. Diese werden im Workspace-Tresor gespeichert. Lassen Sie bei späteren Speichervorgängen beide Felder leer, um das gespeicherte Paar beizubehalten. |
| Adressen im Pfadformat | Verwenden Sie je nach Anbieter „`endpoint/bucket`“, wenn die Funktion aktiviert ist, oder „`bucket.endpoint`“, wenn sie deaktiviert ist. |
| Kopierintervall | Von 1 bis 1.440 Minuten; Standardwert 5 Minuten. Für geplante Sicherungen muss die Anwendung ausgeführt werden. |
| Aufbewahrungsfrist für „Object Lock“ | Aufbewahrungsdauer und -modus für einen Bucket, der „Object Lock“ unterstützt. Bei „Zero Days“ bleibt die Standardaufbewahrungsdauer des Buckets in Kraft. |

1. Erstellen Sie den Bucket bei Ihrem Anbieter und geben Sie anschließend dessen Zielort und Anmeldedaten ein. Lassen Sie die****Option**„Externe Kopie behalten“** während der Vorbereitung deaktiviert und wählen Sie anschließend **„Externe Kopie speichern“** aus.
2. Wählen Sie **„Verbindung testen“** aus. Dadurch wird ein verschlüsseltes Testobjekt hochgeladen und die Antwort des Speichers überprüft.
3. Wählen Sie **„Verschlüsselungsschlüssel herunterladen“** aus. Bewahren Sie diese Datei getrennt vom Datenerfassungs-Tool auf; sie wird für die Wiederherstellung benötigt.
4. Aktivieren Sie das Kontrollkästchen **„Externe Kopie erstellen“** und speichern Sie erneut. Wählen Sie **„Jetzt kopieren“** für einen manuellen Durchlauf oder lassen Sie den Zeitplan weiterlaufen.

## Aufbewahrungsstatus und Kopierfortschritt prüfen

Wählen Sie unter **„Weitere Optionen**“ die Aufbewahrungsdauer sowie „`GOVERNANCE`“ oder „`COMPLIANCE`“ aus, wenn Ihr Bucket „Object Lock“ unterstützt. TgWitness liest den Aufbewahrungsmodus und die Frist eines hochgeladenen Objekts aus. Überprüfen Sie das separate Aufbewahrungsergebnis: bestätigt, fehlende Aufbewahrung oder Überprüfung fehlgeschlagen.

Das Panel meldet den letzten Durchlauf, die Anzahl der Objekte, die übertragenen Bytes, die Grenze des kopierten Protokolls sowie etwaige Fehler. Fehlende oder geänderte lokale Medien werden gemeldet und im nächsten Durchlauf erneut versucht. Dateien, Checkpoints und in der Warteschlange befindliche Exporte, die nach diesen Medien folgen, können weiterhin kopiert werden.

Uploads erfolgen über die Route „Direct“, „SOCKS5“ oder „HTTP“ des Arbeitsbereichs. Wählen Sie eine dieser Routen für das Kopieren in S3; eine Route, die ausschließlich MTProxy verwendet, lässt die Kopie mit einem Fehler hängend.

## Bewahren Sie den Wiederherstellungsschlüssel separat auf

Die heruntergeladene JSON-Datei enthält den Entschlüsselungsschlüssel, die Zieleinstellungen, das Präfix für Arbeitsbereichsobjekte und den Fingerabdruck des Signaturschlüssels. Für die Wiederherstellung sind sowohl diese Schlüsseldatei als auch separate Speicherzugangsdaten mit Lesezugriff auf den Bucket erforderlich. Nehmen Sie diese in Ihren Wiederherstellungsplan auf.

Wenn Sie den Endpunkt, den Bucket oder das Ordnerpräfix ändern, laden Sie die Schlüsseldatei erneut herunter, damit die Zieleinstellungen übereinstimmen. Die Anwendung startet eine neue Kopie des lokal gespeicherten Protokolls, der Dateien und der Checkpoints am neuen Speicherort. Abgeschlossene Chat-Exporte, die bereits aus der lokalen Upload-Warteschlange entfernt wurden, verbleiben an ihrem bisherigen Speicherort.

## Wiederherstellung und Überprüfung auf einem anderen Rechner

Verwenden Sie eine vertrauenswürdige Installation von TgWitness, die heruntergeladene JSON-Schlüsseldatei, Speicherzugangsdaten mit Lesezugriff sowie ein leeres Ausgabeverzeichnis. Ersetzen Sie die unten aufgeführten fiktiven Platzhalter für die Zugangsdaten.

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

Downloads und entschlüsselte Objekte verbleiben in einem privaten Zwischenspeicher, während das gesamte Protokoll, die gespeicherten Kontrollpunkte sowie die Hashes und Größen der erhaltenen Medien überprüft werden. Unsichere Pfade, widersprüchliche Protokollsegmente und ein Protokoll, das kürzer ist als sein Kontrollpunkt, werden abgelehnt. Bei einer fehlgeschlagenen Überprüfung werden keine wiederhergestellten Dateien veröffentlicht.

Bei erfolgreicher Wiederherstellung werden die Werte „`events.jsonl`“, „`media/`“, „`checkpoints/`“ und „`exports/`“ für das in der Kopie verfügbare Material ausgegeben. Bewahren Sie das JSON-Ergebnis des Befehls zusammen mit dem wiederhergestellten Material auf.

Vergleichen Sie das wiederhergestellte Material mit Ihren unabhängig gespeicherten Kontrollpunkten oder Zeugenprotokollen und überprüfen Sie anschließend den Erfassungsumfang der Aufzeichnungen für den von Ihnen benötigten Zeitraum.
