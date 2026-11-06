# Telegram · Erstellen Sie einen Bericht

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reports/

Führen Sie den Leser von der Fallfrage direkt zu den gespeicherten Einträgen.

Report studio stellt Ihre ausgewählten Daten, Änderungsverläufe, Diagramme und Ergebnisse zusammen. Acht Designs, HTML und natives PDF. Jeder HTML-, PDF- und JSON-Bericht wird mit Ihrem Schlüssel versiegelt.

## Erstellen Sie einen Bericht in drei Schritten

1. **Exporte → Konfigurieren und Vorschau → Daten**: der ganze Arbeitsbereich oder ausgewählte Chats, Autoren, Daten (UTC, wann TgWitness den Eintrag gesehen hat) und Eintragstypen.
2. **Design & Inhalt**: Design wählen und was hineinkommt: Diagramme, Teilnehmer, Transkript, Änderungen, Case-Board-Elemente, Falldaten und Notizen.
3. **Vorschau**: Zahlen, Aktivität, Stichproben und fehlende ID-Bereiche prüfen. Speichern, dann das benötigte Format herunterladen.

### Ordnen Sie das gespeicherte Material für den Leser entsprechend an

Synthetisches Beispiel · schematisches Layout, kein generierter Bericht

1. **Auswahl.** Wählen Sie zwei Chats und den Beobachtungszeitraum für den Fall aus.
2. **Verfassen Sie den Text.** Wählen Sie ein Layout und die Abschnitte aus, die die Frage beantworten.
3. **Vorschau.** Überprüfen Sie die ausgewählten Zählwerte und den gespeicherten Vorher-Nachher-Text.
4. **Überprüfen.** Erstellen Sie die endgültige Datei und vergleichen Sie deren Signatur mit dem Fingerabdruck des vertrauenswürdigen Arbeitsbereichs.

#### Ausgewählte Beobachtungen

2 Chats · 1 Beobachtungstag

Nachrichten, Bearbeitungen und Löschhinweise

#### Berichtsstruktur

##### Geänderte Zahlungsadresse

Fallfrage → Umfang → Ergebnisse → Verweise auf Datensätze

**Nachrichtenkontext**

Anmerkung Nr. 142: „Verwenden Sie den neuen Zahlungslink.“

**Gespeicherte Änderungen**

Vorher: old.example.invalid → Nachher: new.example.invalid

#### Überprüfen Sie die Auswahl

18 Beobachtungen · 2 gespeicherte Bearbeitungen

Zeitangaben zu Versand, Bearbeitung und Beobachtung sind separat gekennzeichnet.

#### Endgültiges Ergebnis

Signiertes PDF + signiertes JSON oder eine signierte ZIP-Datei mit dem lesbaren Bericht

Der Empfänger überprüft die Datei und den vertrauenswürdigen Fingerabdruck.

## Wählen Sie einen Lesestil

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, and Ledger & margin**: gleiche Einträge, anderes Aussehen. Beim Wechsel bleiben Auswahl und Notizen. Jede der 25 Sprachen.

PDFs werden mit mitgelieferten Schriften erzeugt, kein Browser nötig. Chinesisch, Japanisch und Koreanisch brauchen eine Schrift wie Noto Sans CJK auf dem Server (systemweit oder in `TGWITNESS_FONT_DIR`), sonst gibt es nur HTML und JSON.

## Lesen Sie eine Änderung im Kontext

Bearbeitungen zeigen vorher und nachher, Löschungen die letzte gespeicherte Version. Antworten, Weiterleitungen, Reaktionen, Buttons und Anhänge behalten ihre Verweise.

Die Design-Vorschau nutzt die ersten 50.000 Einträge, die Datenvorschau zählt alles exakt. Für das endgültige Seitenlayout erzeugen Sie das PDF.

## Wählen Sie die Empfängerfassung sorgfältig aus

Filter formen nur den Bericht, das Beweis-ZIP enthält weiter das ganze Journal und alle Dateien. Soll der Empfänger weniger bekommen, nutzen Sie eine [minimierte Übergabe](https://phishdestroy.github.io/TgWitness/de/docs/handover/). Mehr: [Berichtsinhalte](https://phishdestroy.github.io/TgWitness/de/docs/reference/case-reports/), [den Export prüfen](https://phishdestroy.github.io/TgWitness/de/docs/exports/).
