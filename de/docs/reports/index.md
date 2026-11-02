# Erstellen Sie einen Bericht

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reports/

Bieten Sie dem Leser einen klaren Weg von der Fallfrage zu den gespeicherten Datensätzen.

Das „Report Studio“ kombiniert eine Datenauswahl, lesbare Änderungsprotokolle, Diagramme und Ihre schriftlichen Erkenntnisse. Acht integrierte Designs gelten für unterstützte HTML- und native PDF-Ausgaben. HTML-, PDF- und JSON-Berichte tragen ihre eigenen signierten Siegel; das ZIP-Manifest bündelt zudem die Dateien im Paket. HTML- und PDF-Dateien werden nach Fertigstellung ihres endgültigen Layouts versiegelt.

## Erstellen Sie einen Bericht in drei Schritten

1. Öffnen Sie **„Exporte“ → „Konfigurieren und Vorschau“ → „Daten**“. Verwenden Sie den gesamten Arbeitsbereich oder wählen Sie Chats, Autoren, einschließlich UTC-Beobachtungsdaten und Datensatztypen aus. Die Daten geben an, wann TgWitness den Datensatz erfasst hat.
2. Wählen Sie unter **„Design & Inhalte**“ eine Voreinstellung für Design und Inhalte aus. Wählen Sie Aktivitätsdiagramme, Teilnehmerbezeichnungen, das Protokoll, gespeicherte Änderungen und optionales „Case Board“-Material aus. Fügen Sie Ihre Falldetails und Untersuchungsnotizen hinzu.
3. Öffnen Sie **die Vorschau**, um Anzahl, Aktivitäten, Teilnehmer, stichprobenartig ausgewählte Datensätze und fehlende ID-Bereiche zu überprüfen. Speichern Sie die Einstellungen und laden Sie anschließend das gewünschte Format herunter.

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

**Die Bereiche „Classic“, „Editorial“, „Briefing“, „Analytics“, „Technical“, „Overview“, „Reading Series“ sowie „Ledger & Margin“** präsentieren dieselben zugrunde liegenden Datensätze in unterschiedlichen Zusammenstellungen. Bei einer Änderung des Designs bleiben die Datenauswahl und die schriftlichen Notizen erhalten. Die Berichts-Sprache kann aus den 25 unterstützten Sprachen ausgewählt werden.

Die „Reading Series“ gruppiert Fall, Umfang, Ergebnisse und Änderungen entlang einer Abschnittsleiste. „Ledger & Margin“ verwendet nummerierte Kapitel und einen breiten Rand. Beide unterstützen zudem HTML-Übersichten zu Konten und das Teilen von Kopien. Native PDF-Dateien werden mit den mitgelieferten Schriftarten erstellt; auf dem Rechner des Benutzers ist für die PDF-Erstellung weder ein Browser noch eine Node-Installation erforderlich. Für PDF-Dateien in Chinesisch, Japanisch und Koreanisch ist zusätzlich eine geeignete Schriftart auf dem Server erforderlich, beispielsweise „Noto Sans CJK“, die systemweit installiert oder im Verzeichnis „`TGWITNESS_FONT_DIR`“ abgelegt sein muss. Fehlt diese, enthält die ZIP-Datei lediglich die HTML- und JSON-Berichte.

## Lesen Sie eine Änderung im Kontext

Gespeicherte Bearbeitungen werden im Vorher-Nachher-Vergleich angezeigt. Ein Löschhinweis kann mit der zuletzt erfassten Version ergänzt werden. Antworten, Zitate, Weiterleitungen, Reaktionen, Schaltflächen und Metadaten von Anhängen behalten ihre verfügbaren Verweise bei. SHA-256-Hashes von Dateien und Journal-Einträgen werden separat gekennzeichnet.

Die Designvorschau zeigt Komponenten für Deckblatt, Auswertung und Diagramme anhand passender Datensätze aus den ersten 50.000 Quelldatensätzen. Die separate Datenvorschau durchsucht den vollständigen, stabilen Journal-Snapshot nach exakten Auswahlzahlen, wobei die angezeigten Stichprobengrenzen gekennzeichnet sind. Erstellen Sie ein PDF, um die endgültige Paginierung zu überprüfen. Ein vollständiger Kontoexport enthält eine HTML-Übersicht; die einzelnen Chat-PDFs verwenden das gewählte Design.

## Wählen Sie die Empfängerfassung sorgfältig aus

Berichtsfilter gestalten den übersichtlichen Bericht. Die ZIP-Datei mit den vollständigen Beweismitteln enthält das Originalprotokoll und die Anhänge. Verwenden Sie eine [minimierte Übergabe,](https://phishdestroy.github.io/TgWitness/de/docs/handover/) wenn der Empfänger nur ausgewählte Daten erhalten soll. Sehen Sie sich [den Berichtsinhalt und die Überprüfung](https://phishdestroy.github.io/TgWitness/de/docs/reference/case-reports/) an oder [überprüfen Sie den fertigen Export](https://phishdestroy.github.io/TgWitness/de/docs/exports/).
