# Bereiten Sie eine Kopie zur Weitergabe vor

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/handover/

Teilen Sie nur, was nötig ist, das Original bleibt unberührt.

Eine Übergabe ist ein separater signierter Auszug: Chats und Personen wählen, Identitäten oder Text verbergen, Dateien und Teamnotizen auswählen. Das Manifest hält fest, was behalten, gekürzt und weggelassen wurde.

## Auszug für den Empfänger vorbereiten

1. **Exporte → Übergabeauszug**: Zweck eintragen, Chats und Zeitraum wählen, **Personen der gewählten Chats laden**, wenn Sie namentlich genannte Personen brauchen.
2. Alle anderen: Pseudonyme, weggelassen oder wie aufgezeichnet. Text und Dateien sind getrennte Schalter; Telefonnummern und E-Mails lassen sich maskieren.
3. Case Board: nichts, Lesezeichen und Ausschnitte oder Karten mit Kommentaren. Teamnamen lassen sich durch Aliasse ersetzen.
4. **Übergabeauszug herunterladen**, öffnen, prüfen, vor dem Versenden durchsehen.

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
| Personen | Ausgewählte Personen bleiben namentlich genannt, andere bekommen Pseudonyme oder werden weggelassen. |
| Text | Der ganze Text, nur der der ausgewählten Personen und Ihres Kontos, oder keiner. |
| Dateien | Dateien der ausgewählten Personen und Ihres Kontos, alle angezeigten Dateien oder keine. |
| Case Board | Nichts, Lesezeichen und Ausschnitte oder Karten mit Diskussion. |

Lesen Sie auch Text und Dateien: Ein Pseudonym entfernt keine Namen, die in einer Nachricht oder einem Anhang stehen. Fehlt eine ausgewählte Datei, stellen Sie sie wieder her oder lassen Sie Anhänge weg.

## Der Text muss unabhängig überprüfbar bleiben.

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Behalten Sie das Originalarchiv und die Prüfpunkte selbst. Der Empfänger kann seine Kopie prüfen, ohne den ganzen Arbeitsbereich zu bekommen. Design: [Report studio](https://phishdestroy.github.io/TgWitness/de/docs/reports/). Vertrauenswürdige Referenzen: [Exportprüfung](https://phishdestroy.github.io/TgWitness/de/docs/exports/).
