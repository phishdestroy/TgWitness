# Bereiten Sie eine Kopie zur Weitergabe vor

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/handover/

Teilen Sie die relevanten Beobachtungen mit, ohne den ursprünglichen Arbeitsbereich zu verändern.

Eine Übergabe ist ein separater, signierter Auszug. Wählen Sie die Chats und Personen aus, reduzieren Sie Identitäten oder Text und entscheiden Sie, welche Dateien und Teamnotizen in die Kopie des Empfängers gehören. Das Manifest dokumentiert die Auswahl sowie die Anzahl der unveränderten, minimierten und ausgelassenen Datensätze.

## Auszug für den Empfänger vorbereiten

1. Öffnen Sie **„Exporte“ → „Übergabeauszug**“. Geben Sie den Zweck an, wählen Sie die Chats und optional den UTC-Zeitraum aus und wählen Sie anschließend **„Teilnehmer der ausgewählten Chats laden**“, falls Sie namentlich genannte Personen benötigen.
2. Legen Sie fest, wie mit allen anderen Personen verfahren werden soll: Pseudonyme verwenden, deren Nachrichten weglassen oder wie aufgezeichnet anzeigen. Legen Sie Nachrichtentext und Anhänge unabhängig voneinander fest; optional können Sie Telefonnummern und E-Mail-Adressen maskieren.
3. Entscheiden Sie, ob Sie Lesezeichen und Ausschnitte aus dem Case Board oder Karten mit Kommentaren einbeziehen möchten. In diesem Text können Aliasnamen der Ermittler die Teamnamen ersetzen.
4. Wählen Sie **„Download-Übergabeauszug“** aus. Öffnen Sie den generierten Bericht und die ausgewählten Datensätze lokal, überprüfen Sie das Archiv und kontrollieren Sie die Kopie, bevor Sie sie versenden.

### Ein Original, eine Kopie zur Weitergabe

Fiktives Beispiel · dient nur zur Veranschaulichung

1. **Auswählen.** Den Fall-Chat einbeziehen und die Person identifizieren, um die es in dem Auszug geht.
2. **Minimieren.** Wählen Sie aus, wie ein anderer Teilnehmer in der Freigabekopie angezeigt wird.
3. **Überprüfen Sie** den Bericht und die Datensätze des generierten Archivs**,** bevor Sie es versenden.
4. **Teilen.** Liefern Sie die geprüfte Fassung und übermitteln Sie den zugehörigen vertrauenswürdigen Fingerabdruck separat.

#### Ursprüngliche Anmerkung

Nora · Benutzer 71002

„Ich habe den überarbeiteten Link erhalten.“

Das Quellprotokoll bewahrt diese gespeicherte Beobachtung auf.

#### Kopie für den Empfänger

Wie aufgezeichnet anzeigen: Nora · Benutzer 71002 · „Ich habe den überarbeiteten Link erhalten.“

Pseudonym: P01 · „Ich habe den überarbeiteten Link erhalten.“

Weglassen: Die Nachricht dieses Teilnehmers wird im Text nicht berücksichtigt.

#### Prüfen Sie die tatsächlichen Dateien

Lesen Sie die Dateien „report.html“ und „records.jsonl“.

Überprüfen Sie Identitäten, Text, Anhänge und optionale Teamkommentare.

#### Signierter Auszug

Auswahl + Datei-Hashes + signiertes Manifest

Ein separates Paket, das mit den Grenzen des zugehörigen Quellprotokolls verknüpft ist

## Verwenden Sie die Steuerelemente gemeinsam

| Kontrolle | Auswirkungen auf den Text |
| --- | --- |
| Personen | Ausgewählte Personen müssen identifizierbar bleiben; andere Teilnehmer sind je nach Wahl zu pseudonymisieren oder wegzulassen. |
| Text | Beziehen Sie den gesamten Text ein, nur den Text der ausgewählten Personen und des Beobachtungskontos oder lassen Sie den Nachrichtentext und die texthaltigen Detailfelder weg. |
| Dateien | Wählen Sie Dateien der ausgewählten Personen und des überwachten Kontos, alle Dateien der angezeigten Nachrichten oder keine Dateien aus. |
| Case Board | Verwenden Sie kein Board-Material, keine Lesezeichen und keine Ausschnitte sowie keine Karten mit Teamdiskussionen. |

Überprüfen Sie Freitext und Dateiinhalte sowie Identitäten: Ein Pseudonym entfernt nicht automatisch jeden Namen, der in einer Nachricht oder einem Anhang steht. Sollte eine ausgewählte, gesicherte Datei nicht verfügbar sein, stellen Sie diese wieder her oder lassen Sie Anhänge ausdrücklich weg, bevor Sie den Auszug erstellen.

## Der Text muss unabhängig überprüfbar bleiben.

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Bewahren Sie das ursprüngliche, signierte Beweismittelarchiv und die Checkpoints separat auf. Bei der Übergabe wird eine eigene Projektion erstellt, sodass der Empfänger die gelieferte Kopie überprüfen kann, ohne den gesamten Arbeitsbereich zu erhalten. [„Report Studio“](https://phishdestroy.github.io/TgWitness/de/docs/reports/) liefert das Layout für die Anzeige; [die Exportüberprüfung](https://phishdestroy.github.io/TgWitness/de/docs/exports/) erläutert die vertrauenswürdigen Referenzen.
