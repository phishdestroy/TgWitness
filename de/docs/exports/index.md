# Exportieren und verifizieren

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/exports/

Geben Sie jemandem Dateien, die er selbst gegen Ihren Arbeitsbereich prüfen kann.

Bitte verweisen Sie daraufSignierte ZIP-Datei exportierenDer Empfänger überprüft

Neu bei Signaturen und Prüfpunkten? [Ändern Sie einen Beispieleintrag](https://phishdestroy.github.io/TgWitness/de/docs/concepts/#chain) und sehen Sie, welche Prüfungen es bemerken.

Möchten Sie eine Kopie außerhalb des Datensammlers aufbewahren? Gehen Sie zu [„S3-Einrichtung“](https://phishdestroy.github.io/TgWitness/de/docs/exports/#s3), [„Objekt-Sperre“](https://phishdestroy.github.io/TgWitness/de/docs/exports/#s3-retention) oder [„verifizierte Wiederherstellung](https://phishdestroy.github.io/TgWitness/de/docs/exports/#s3-restore)“.

## Eine vertrauenswürdige Referenz bereitstellen

Notieren Sie den Schlüssel-Fingerabdruck des Arbeitsbereichs irgendwo außerhalb des Collectors. Bewahren Sie während der Erfassung auch signierte Prüfpunkte woanders auf oder betreiben Sie einen [unabhängigen Zeugen](https://phishdestroy.github.io/TgWitness/de/docs/witness/). Dagegen prüft der Empfänger den Schlüssel und einen früheren Journalstand.

## Laden Sie die signierte ZIP-Datei herunter

**Exporte** → signiertes Beweis-ZIP. Es enthält das ganze Journal und ein signiertes Dateimanifest. Den lesbaren Bericht gestalten Sie im [Report studio](https://phishdestroy.github.io/TgWitness/de/docs/reports/), oder Sie schicken nur ausgewählte Daten als [Übergabeauszug](https://phishdestroy.github.io/TgWitness/de/docs/handover/).

HTML-, PDF- und JSON-Berichte tragen eigene Siegel. CSV ist nur eine Arbeitskopie; für die Integrität nehmen Sie die CSV aus dem geprüften ZIP.

## Überprüfen Sie dies anhand einer vertrauenswürdigen Kopie von TgWitness

In der Projektumgebung, mit Ihrem eigenen Fingerabdruck und Pfaden:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Bei Erfolg sehen Sie `key_pinned: true` und `checkpoint_checked: true`. Bewahren Sie diese Ausgabe beim Archiv auf. Der Prüfpunkt muss am Ende des Exports oder davor liegen.

## Verwenden Sie das Verifizierungsergebnis

- **Dateien:** Das Manifest bindet ihre Hashes, die Signaturen binden das Journal. Jede Änderung fällt auf.
- **Identität:** Der aufbewahrte Fingerabdruck belegt, dass es der erwartete Schlüssel ist.
- **Früherer Stand:** Ein Prüfpunkt vergleicht den Export mit einem vor der Übergabe gespeicherten Journalanfang.
- **Abdeckung:** Lücken, Erfassungsergebnisse und ein Test Senden → Bearbeiten → Löschen zeigen, was dieses Setup wirklich erfasst hat.

Details: [was die Prüfung beweist und was nicht](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope).

## Richten Sie die externe S3-Kopie ein

**Exporte → Externe Kopie** in Ihrem Arbeitsbereich. Funktioniert mit AWS S3 und allem, was S3-kompatibel ist. Kopiert Journalsegmente, gespeicherte Dateien, Prüfpunkte mit ihren Zeitstempeln und fertige Chat-Exporte, jeweils mit `AES-256-GCM` verschlüsselt, bevor sie den Collector verlassen.

Die Online-Demo zeigt diese Einstellungen mit deaktiviertem Upload. Echte Zugangsdaten nur in Ihrer eigenen Installation eingeben.

[![Vollständiges Off-Site-Kopier-Panel: Endpunkt, Region, Bucket, Zugriffsschlüssel, Zeitplan, „Object Lock“- und Wiederherstellungsschlüssel-Steuerelemente](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Das vollständige Bedienfeld mit erweiterten Optionen ist aufgeklappt. Es werden keine Anmeldedaten für den Speicher angezeigt.

| Fachgebiet | Was ist einzugeben? |
| --- | --- |
| Endpunkt | Speicher-URL, ohne Bucket-Pfad oder Zugangsdaten. Beispiel: `https://s3.example.invalid`. |
| Region | Was Ihr Anbieter verlangt. Standard `us-east-1`. |
| Bucket | Ein vorhandener Bucket mit Schreibrechten. Beispiel: `example-case-backup`. |
| Ordner im Bucket | Präfix, Standard `tgwitness`. Ein Präfix pro Arbeitsbereich kommt dazu. |
| Zugriffs-ID / Geheimer Zugangsschlüssel | Beide zusammen, im Tresor gespeichert. Später beide leer lassen, um sie zu behalten. |
| Adressen im Pfadformat | An: `endpoint/bucket`. Aus: `bucket.endpoint`. Hängt vom Anbieter ab. |
| Kopierintervall | 1 bis 1.440 Minuten, Standard 5. Nur solange die App läuft. |
| Aufbewahrungsfrist für „Object Lock“ | Tage und Modus, wenn der Bucket Object Lock unterstützt. Null lässt den Bucket-Standard. |

1. Bucket anlegen, Ziel und Zugangsdaten mit deaktiviertem **Externe Kopie behalten** ausfüllen, **Externe Kopie speichern** klicken.
2. **Verbindung testen** lädt ein verschlüsseltes Testobjekt hoch.
3. **Verschlüsselungsschlüssel herunterladen** und fern vom Collector aufbewahren. Kein Schlüssel, keine Wiederherstellung.
4. **Externe Kopie behalten** aktivieren, speichern, dann **Jetzt kopieren** oder den Zeitplan laufen lassen.

## Aufbewahrungsstatus und Kopierfortschritt prüfen

Unter **Weitere Optionen** Aufbewahrungstage und `GOVERNANCE` oder `COMPLIANCE` wählen. TgWitness liest die Aufbewahrung von einem hochgeladenen Objekt zurück und meldet: bestätigt, fehlt oder Prüfung fehlgeschlagen.

Das Panel zeigt den letzten Durchlauf, Objektanzahl, Bytes, kopierte Journalgrenze und Fehler. Eine fehlende lokale Datei wird gemeldet und im nächsten Durchlauf erneut versucht, der Rest wird weiter kopiert.

Uploads laufen direkt, über SOCKS5 oder HTTP. Mit einer reinen MTProxy-Route wartet die Kopie mit einem Fehler.

## Bewahren Sie den Wiederherstellungsschlüssel separat auf

Das Schlüssel-JSON enthält den Entschlüsselungsschlüssel, das Ziel, das Präfix und den Schlüssel-Fingerabdruck. Zur Wiederherstellung brauchen Sie es plus Speicherzugangsdaten mit Leserecht.

Endpunkt, Bucket oder Präfix geändert? Laden Sie den Schlüssel neu herunter. Am neuen Ziel startet eine frische Kopie, alte Chat-Exporte bleiben, wo sie waren.

## Wiederherstellung und Überprüfung auf einem anderen Rechner

Sie brauchen eine vertrauenswürdige TgWitness-Installation, das Schlüssel-JSON, Nur-Lese-Zugangsdaten und einen leeren Ordner:

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

Erst wird alles in einem privaten Temp-Ordner geprüft: das ganze Journal, Prüfpunkte, Datei-Hashes und Größen. Unsichere Pfade, widersprüchliche Segmente oder ein Journal kürzer als sein Prüfpunkt schlagen fehl, und dann wird nichts geschrieben.

Bei Erfolg bekommen Sie `events.jsonl`, `media/`, `checkpoints/` und `exports/`. Bewahren Sie die JSON-Ausgabe des Befehls dazu auf und vergleichen Sie mit selbst aufbewahrten Prüfpunkten oder Zeugen-Einträgen.
