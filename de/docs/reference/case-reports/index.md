# Berichtskonfiguration und -überprüfung

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/case-reports/

Berichtsfilter, acht Designs, Inhaltsvorlagen, gespeicherte Änderungsverläufe und die Bewertung sind in den signierten Exporten enthalten.

Verwandeln Sie ausgewählte Beobachtungen in einen lesbaren Fallbericht: mit Fragestellung, Umfang, gespeicherten Änderungen, Diagrammen, Ergebnissen und Quellenangaben. Jeder Bericht bietet dem Empfänger die Möglichkeit, das gelieferte Material zu überprüfen und den Erfassungsumfang der Datenerhebung zu begutachten.

Der Abschnitt **„Grundlage des Vertrauens und Einschränkungen“** erscheint in Protokoll-, Übergabe-, Chat-, Konto- und Freigabeberichten. Protokoll- und Übergabe-PDFs verwenden dieselbe Bewertung wie ihr signiertes „`report.json`“-Dokument. ZIP-Manifeste enthalten „`case_assessment`“ im signierten Manifest. Diese Bewertung wird zusammen mit dem exportierten Material übermittelt. Die ursprünglichen Beobachtungen behalten ihre bestehenden Signaturen bei.

## Dokumentformate und Lesereihenfolge

### Report Studio

Öffnen Sie **„Exporte“ → „Konfigurieren“ und „Vorschau**“. Gehen Sie die folgenden Schritte durch: **„Daten“ → „Gestaltung & Inhalte“ → „Vorschau**“:

1. Verwenden Sie den gesamten Arbeitsbereich oder wählen Sie Chats, Autoren, einschließlich UTC-Beobachtungsdaten und Ereignistypen aus. Laden Sie den Katalog, um nach Chats und Autoren zu suchen, oder geben Sie deren Telegram-IDs ein. Autorenfilter gleichen aufgezeichnete Absender-IDs ab; eine Löschmeldung ohne Absender entspricht keinem Autorenfilter.
2. Wählen Sie ein Seitendesign aus und legen Sie anschließend Diagramme, Teilnehmerbezeichnungen, das Protokoll und Ihre schriftlichen Erkenntnisse fest. Bei einer Änderung des Designs bleiben diese Einstellungen erhalten.
3. Erstellen Sie die Vorschau. Sie zeigt tatsächliche Zahlen, Aktivitäten, Teilnehmer, Beispiel- Datensätze, gespeicherte Änderungen und fehlende Nachrichtennummernbereiche an. Durch Ändern einer Auswahl wird die Vorschau als veraltet markiert. Speichern Sie die Datei, bevor Sie HTML, signiertes PDF, signiertes JSON oder die ZIP-Datei mit den Beweismitteln herunterladen.

Die Datenvorschau erfasst das vollständige, stabile Protokollpräfix, nicht nur eine anfängliche Stichprobe. Nur angezeigte Beispielzeilen und lange Listen sind begrenzt; ihre ausgelassenen Zählwerte werden angezeigt. Ein späterer Export erstellt einen neuen stabilen Snapshot, sodass die laufende Erfassung die Zahlen erhöhen kann. Umfang, Zählwerte und Quellenidentität sind im signierten Bericht enthalten. Das Öffnen oder Anzeigen des Formulars in der Vorschau speichert es nicht.

**Wählen Sie die Empfängerkopie aus.** Diagramme und das Protokoll verwenden die ausgewählten Datensätze. Integrität, Aufbewahrung und Erfassungsbereich beschreiben das vollständige Quellprotokoll. Die Beweismittel-ZIP-Datei enthält die Originaldatensätze und Anhänge. Verwenden Sie [eine minimierte Übergabe,](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#handover-extract) wenn ein Empfänger nur ausgewählte, zulässige Daten erhalten soll.

### Lesen Sie Änderungen, Löschungen und fehlende IDs

Eine Bearbeitung zeigt den gespeicherten Text **„Vorher“** und **„Nachher“** an und hebt die geänderten Wörter hervor. Eine Löschung zeigt die letzte vor der Meldung gespeicherte Version an. Wenn kein früherer Inhalt erfasst wurde, wird dies im Bericht vermerkt. Wenn Sie nur Bearbeitungen oder Löschungen auswählen, bleiben die vorherigen Versionen als explizit gekennzeichneter Kontext außerhalb der Filter verfügbar. Nicht relevante Meldungen werden diesen Verlaufsdaten nicht hinzugefügt.

**Nicht beobachtete Nachrichten-IDs** sind Lücken zwischen bekannten Nummern in den ausgewählten Chats und dem aus dem Datum abgeleiteten ID-Bereich. Jeder bekannte Quelldatensatz wird überprüft, bevor eine Nummer als nicht beobachtet deklariert wird: Das Herausfiltern eines anderen Autors, eines Ereignistyps oder eines Datums darf keine falsche Lücke erzeugen. Benachbarte gespeicherte Nachrichten werden als Kontext gekennzeichnet. Eine fehlende Nummer belegt nicht, dass eine Nachricht existierte oder gelöscht wurde; Löschmeldungen und erfolglose Nachprüfungen bleiben separate Ereignistypen.

### Wählen Sie ein Design

Für HTML-Berichte zu Protokollen und Einzelchats sowie für signierte PDF-Berichte stehen acht Seitenlayouts zur Verfügung. Sie basieren auf denselben Datensätzen und Berechnungen, unterscheiden sich jedoch in Bezug auf Titelseiten, Typografie, Kapitelüberschriften, Tabellen und Abstände.

| Gestaltung | Schreibstil |
| --- | --- |
| Klassisch | Eine klassische Akte mit dunklem Einband und nummerierten Abschnitten. |
| Redaktionelle Hinweise | Eine gerahmte Titelseite mit Serifenschrift, breiten Rändern und einer schmalen Kapitelleiste. |
| Briefing | Ein kompaktes Deckblatt mit marineblauem Buchrücken, kurzen Überschriften und eng gesetzten Tabellen. |
| Analytik | Ein Cover im Umfrage-Stil, modulare Diagrammtafeln und Abbildungen in Monospace-Schrift. |
| Technisch | Ein liniertes Register, eine nummerierte Referenzleiste und präzise Vergleichstabellen. |
| Übersicht | Ein Panorama-Titelbild, großzügige Abstände und auffällige Übersichtsgrafiken. |
| Lesereihe | Eine Abschnittsleiste und gruppierte Kapitel für Ergebnisse, Umfang, Änderungen und das Beobachtungsprotokoll. |
| Ledger & Margin | Nummerierte Kapitel mit breitem Rand, exakte Diagramme und Tabellen sowie ein separates Nachrichtenprotokoll. |

Das Design wird pro Arbeitsbereich gespeichert und im signierten Exportmanifest erfasst. HTML funktioniert offline, unterstützt helle und dunkle Designs und passt sich an schmale Bildschirme sowie Sprachen mit Schreibrichtung von rechts nach links an. Native PDFs verwenden mitgelieferte Schriftarten; das „Editorial“-Design umfasst „Noto Serif“ unter der mitgelieferten SIL Open Font License. Lesereihen sowie „Ledger & Margin“ gelten auch für Kontoübersichten, Konto-Chats und das Teilen von Kopien.

Für PDF-Dateien in Chinesisch, Japanisch und Koreanisch ist zusätzlich eine geeignete Schriftart auf dem Server erforderlich, wie beispielsweise „Noto Sans CJK“, die systemweit installiert oder im Verzeichnis „`TGWITNESS_FONT_DIR`“ abgelegt sein muss. Ist diese nicht verfügbar, enthält die ZIP-Datei die HTML- und JSON-Berichte.

Diese beiden Entwürfe umfassen ein lesbares Protokoll ohne JavaScript. Bei umfangreichen Exporten enthält diese Ansicht bis zu 500 vollständige Datensätze innerhalb eines Eingabebudgets von 8 MiB; der Bericht kennzeichnet die Obergrenze und enthält Links zum vollständigen Viewer sowie zu den Quelldatensätzen. Das Kontoverzeichnis und der Beziehungsindex beschreiben dasselbe Lesebeispiel, nicht alle Teilnehmer. Diagramme des vollständigen Journals behalten ihren separat angegebenen Umfang bei.

### Inhalt auswählen

| Inhaltsverzeichnis | Standardmäßig enthalten |
| --- | --- |
| Fallakte | Aktivitäten, Beobachtungszeitpunkte, Teilnehmer, Chats und das Transkript der Aufzeichnung. |
| Briefing | Eine Aktivitätsübersicht ohne Teilnehmerranglisten oder das Transkript. |
| Überprüfung der Aktivitäten | Aktivitäten, Beobachtungszeitpunkte, Teilnehmer, Chats und deren Zusammensetzung, mit Quellenangaben und genauen Zahlen. |
| Individueller Bericht | Ihre eigene Kombination aus Diagrammen, Transkripten und Vorschauen. |

Beim Ändern einer Voreinstellung bleiben Ihr Design, die Falldetails und die schriftliche Analyse erhalten. Integritätsprüfungen, Erfassungsgrad, Einschränkungen und Anweisungen zur Verifizierung bleiben in jedem Design erhalten. Quelldatensätze im ZIP-Archiv bleiben unverändert, wenn ein Diagramm oder ein Transkript ausgeblendet wird.

Die optionalen **Untersuchungsnotizen** enthalten die Frage, die Methode, die Ergebnisse und die Schlussfolgerung, die vom Verfasser des Berichts verfasst wurden. Geben Sie in den Ergebnissen die Quelldatei und die Datensatznummern an. Die Signatur sichert diese vom Verfasser verfassten Aussagen zusammen mit dem Bericht; die Beobachtungen aus der Quelle und die Interpretation des Verfassers bleiben identifizierbar. Bei minimierten Übergaben werden diese privaten Notizen und vollständigen Tagebuchdiagramme weggelassen. Die Auswahlmöglichkeiten für Diagramme und Untersuchungen gelten für Tagebuchberichte.

Wählen Sie Aktivitäten im Zeitverlauf, die UTC-Heatmap nach Wochentag/Stunde, Teilnehmer-Rankings, Chat- Rankings und die Zusammensetzung der Datensätze aus. Wählen Sie 5–30 rangierte Gruppen und neutrale Teilnehmer- Aliase oder Konto-IDs aus. Unbekannte Absender und die übrigen Teilnehmer werden in separaten Zeilen angezeigt. Aliase wirken sich nur auf Diagramme aus; die Quelldatensätze enthalten weiterhin die tatsächlichen Identitäten.

Die Designvorschau wird anhand des ungespeicherten Entwurfs aktualisiert und verwendet dabei Komponenten für Produktionsdeckblatt, Untersuchung und Diagramme, beschränkt auf Übereinstimmungen innerhalb der ersten 50.000 Quelldatensätze. Die Datenvorschau unten berechnet die vollständige Auswahl. Sie ist ausdrücklich nicht signiert und speichert keine Bearbeitungen. Die Schaltflächen „Deckblatt“ und „Diagramme“ wechseln den jeweiligen Abschnitt. Dies ist keine vollständige PDF-Vorschau. **Mit „Berichtseinstellungen speichern“** werden die Auswahlmöglichkeiten auf zukünftige Exporte angewendet; bereits signierte Dateien sind unveränderbar. Das PDF verwendet das ausgewählte Deckblatt, die Typografie, das Kapitellayout und dieselben ausgewählten Aggregate wie HTML und signiertes JSON.

Vertrauensbewertung, Abdeckungsbeschränkungen und Überprüfungsanweisungen bleiben erhalten. Das Ausblenden von Diagrammen oder des lesbaren Transkripts entfernt keine autoritativen Quellzeilen aus der ZIP-Datei. Deaktivierte Diagrammreihen werden im analytischen JSON-Format weggelassen; verwenden Sie einen minimierten Export, um die Offenlegung von Quelldatensätzen einzuschränken.

Filter zur Datenauswahl gelten für Protokollberichte; Konto- und Freigabe-Exporte behalten ihren eigenen Erfassungs- und Offenlegungsumfang bei.

Gemeinsame Design- und Diagrammeinstellungen werden in neue Chat-/Konto-Exporte und Vorschauen zur Kontofreigabe übernommen. Die Sprach- und Datenschutzeinstellungen für Konten und Freigaben bleiben unabhängig; private Fall- und Untersuchungsnotizen werden nicht in diese Exporte kopiert. Konto- und Freigabereports bleiben als HTML-Dateien durch ihr signiertes Archivmanifest geschützt. Das Journal, die minimierte Journalübergabe und Einzel-Chat-Kits stellen ebenfalls signierte PDFs bereit.

### Was die Diagramme aussagen

Protokollaktivitäten und Heatmaps erfassen neue, historische, wiederhergestellte, bearbeitete, gelöschte und bei erneuter Überprüfung fehlende **Beobachtungen**, sortiert nach dem Beobachtungszeitpunkt des Collectors in UTC. Heartbeats und Empfangsbestätigungen für Anhänge werden ausgeschlossen. Teilnehmer-Rankings zählen nur neue, historische und wiederhergestellte Nachrichtenbeobachtungen: Ein Absender wird nicht als Bearbeiter oder Löscher deklariert. Wiederholte Beobachtungen können dieselbe Telegram-Nachricht beschreiben.

Die Protokollanalysen behalten die Zählungen nach Art, Verweise auf den ersten/letzten Datensatz und den SHA-256-Hash der Quelldatei „ `events.jsonl`“ bei. Zahlenangaben enthalten exakte Werte in HTML und PDF. Tägliche Zeitintervalle werden nach 366 aufgezeichneten Tagen auf Monate umgestellt; Diagramme fassen diese zu höchstens 36 Intervallen gleicher Breite zusammen. Bei mehr als 100.000 eindeutigen Identifikatoren oder 1.200 Monaten ist das betroffene Diagramm nicht verfügbar, während die genauen Gesamtzahlen weiterhin verfügbar bleiben.

Snapshot- und Kontofreigabe-Diagramme zählen nur die enthaltenen Zeilen mit Nicht-Dienst-Nachrichten, unter Verwendung der aufgezeichneten Nachrichtenzeit. Freigabe-Aggregate werden nach der Schwärzung und Filterung berechnet. Diese Diagramme verwenden höchstens 90 gleich breite UTC-Datumsintervalle und behalten bis zu 10.000 Gruppierungswerte bei; überschüssige Zählwerte werden explizit ausgewiesen und abgeglichen. Das letzte Intervall kann kürzer sein. Unbekannte oder ungenaue Datumsangaben fließen nicht in Zeitdiagramme ein.

Ein leeres Intervall bedeutet, dass keine Beobachtungen enthalten sind; bei Lücken die Abdeckung prüfen. Diese Diagramme beschreiben gespeicherte Aktivitäten. Unbekannte Absender bleiben eine separate Kategorie, und jede Überprüfung wird einzeln ausgewiesen.

Sofern enthalten, wird „`analytics.json`“ durch die signierten Datei-Hashes des Archivs geschützt. Der Journal-`report.json` bettet dieselbe ausgewählte Aggregation ein. Die Signaturprüfung erkennt geänderte Bytes. Um die Zahlen zu überprüfen, berechnen Sie die Journal-Aggregate mit „`report_analytics.Analytics`“ und „`selected`“ neu oder die Snapshot-Aggregate mit „`snapshot_analytics.collect`“ und „`project`“.

Erstellen Sie ausgehend von einem Quell-Checkout alle acht oben aufgeführten Entwürfe aus derselben fiktiven Zeitschrift:

```
python tools/build_report_styles.py --output test-results/report-styles
```

Öffnen Sie die resultierende Datei „`index.html`“, um vollständige HTML-Berichte, signierte PDFs und ZIP-Dateien zu vergleichen. Jedes Layout basiert auf demselben Quellprotokoll. Verwenden Sie für jeden Durchlauf ein neues Ausgabeverzeichnis, damit zuvor signierte Beispiele erhalten bleiben.

![Fiktives HTML-Dossier](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

Die HTML-Seite beginnt mit einem Fallüberblick und Kennzahlen. Die nummerierte Beweiskarte verlinkt auf jeden Befund, die ihn stützenden Fakten, Einschränkungen und die unabhängige Überprüfung. Durchsuchbare Datensätze und stabile Datensatzverweise bleiben im Offline-Viewer verfügbar. Das Design passt sich an schmale Bildschirme, verschiedene Designs und Browser ohne JavaScript an.

Das signierte PDF verfügt über ein eigenes A4-Deckblatt, eine Berichtsreferenz und einen QR-Code, eine Zusammenfassung, eine Beweiskarte, nummerierte Feststellungen und Dokumenten-Lesezeichen. Die Seiten- Kopf- und Fußzeilen kennzeichnen den Bericht. Ein QR-Code identifiziert das Material; er ist kein eigenständiges Verifizierungsergebnis. Browser-Ausdrucke sind von diesem kryptografisch signierten PDF getrennt.

Die Beobachtungszeitleiste ordnet aufgezeichnete Beobachtungszeiträume und Unterbrechungen auf derselben UTC-Achse an. Leere Bereiche bedeuten keine abgeleitete Abdeckung; die detaillierten Tabellen behalten die genauen Intervalle bei. Die ZIP-Datei enthält die lesbaren Berichte, signierte JSON-Dateien, Quelldatensätze und Anweisungen zur Verifizierung.

Erstellen Sie ein neues, fiktives Dossier in Englisch/Russisch/Deutsch mit der installierten Entwicklungsumgebung:

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Jedes Sprachverzeichnis enthält die Dateien „`report.html`“, „`report.pdf`“, „`report.json`“ und „`dossier.zip`“. Vorhandene Beispielverzeichnisse werden niemals überschrieben. Zur Erstellung werden weder ein Telegram- Konto noch ein externer Zeitstempel-Dienst oder eine Netzwerkverbindung verwendet.

![Die ersten drei Seiten des fiktiven, signierten PDF-Dokuments](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## Ein konkreter Fall

Bei einem Protokoll mit 1.200 Einträgen und einem validierten Zeitstempel bei Eintrag 1.000 identifiziert der Bericht 200 spätere Einträge außerhalb des Zeitraums dieses Zeitstempels. Dies ist eine Obergrenze für das Vorhandensein eines Checkpoints, kein Nachweis für den Versandzeitpunkt jeder einzelnen Nachricht . Wenn drei weitere Zeitstempeldateien die Validierung nicht bestehen oder nicht validiert werden können, werden sie separat gezählt und können keine positive Schlussfolgerung liefern.

Ein verwendbarer Zeitstempel muss alle folgenden Prüfungen bestehen: Sein Abdruck stimmt mit dem Checkpoint überein, seine Signatur lässt sich zum Zeitpunkt der Stempelung auf eine vertrauenswürdige TSA-Root zurückverfolgen, und die Signatur, der Schlüssel, die Zählung und der Kopf des Checkpoints stimmen genau mit dem Journal-Präfix überein. Das bloße Parsen eines Zeitstempels oder das Vorhandensein einer OTS-Quittung reicht nicht aus. Der Leser muss die vertrauenswürdige TSA-Root selbstständig auswählen und die Überprüfung wiederholen. OTS benötigt eine eigene Bitcoin-Bestätigungsprüfung.

| Berichtsstatus | Bedeutung |
| --- | --- |
| Beim Export geprüft | Der Exporteur hat die angegebene Überprüfung durchgeführt; eine unabhängige Wiederholung ist dennoch erforderlich. |
| Aufgezeichnet; Überprüfung erforderlich | Die zugrunde liegende Beobachtung oder Aussage des Bedieners wird aufgezeichnet; es handelt sich nicht um eine unabhängige Bestätigung. |
| Nicht in diesem Text enthalten | Der Text enthält keine Belege für diese Behauptung. Es wird nicht gesagt, dass es anderswo keine gibt. |
| Nicht unabhängig überprüft | Der Bericht liefert kein unabhängiges Verifizierungsergebnis. |
| Unvollständig oder nicht verfügbar | Material oder eine erforderliche Überprüfung fehlt, ist unvollständig oder war nicht erfolgreich. |

Überprüfen Sie jede Prüfung separat und vergleichen Sie sie mit dem erfassten Erfassungsumfang.

## Was eine umfassende Konfiguration beibehalten muss

1. Bevor Sie sich auf die Erfassung verlassen, sichern Sie den Fingerabdruck des Erfassers über einen separaten, vertrauenswürdigen Kanal. Vergleichen Sie diese Referenz mit dem Signaturschlüssel des Exports.
2. Behalten Sie unabhängig voneinander mit Zeitstempeln versehene Kontrollpunkte bei sowie, sofern verwendet, ein Zeugenprotokoll, das außerhalb der administrativen Kontrolle des Collectors liegt. Vergleichen Sie diese mit dem exportierten Protokoll, um dessen frühere Grenzen zu überprüfen.
3. Erfassen Sie den Umfang der Datenerfassung, Lücken, Filter, Einschränkungen und Änderungen bei der Erfassung. Erläutern Sie fehlende Zeiträume, die für den konkreten Fall relevant sind, und unterscheiden Sie dabei klar zwischen nicht erfassten Nachrichten-IDs, Löschhinweisen und erfolglosen Nachprüfungen.
4. Behalten Sie die ursprünglichen ZIP-Dateien und deren Hashes bei. Erfassen Sie jeden Inhaber, jede Übertragung, jedes Datum und jeden Zweck. Behalten Sie die zugeordneten Aussagen der Betreiber und Fallnotizen dazu bei.
5. Bei vertraulichen VMs sind das Zitat, die Challenge, die Intel-Zertifikatskette, die Messwerte, die genaue Quelle und die Bedingungen für den Umgang mit Schlüsseln zu bewahren und unabhängig zu überprüfen. Das Ergebnis der Beglaubigungsprüfung ist zusammen mit den geprüften Artefakten aufzubewahren.

See [verification scope](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope) for the checks of acquisition， archive integrity，time and collection coverage in each mode．

## Überprüfung durch den Empfänger

Verwenden Sie eine vertrauenswürdige Installation von TgWitness und einen unabhängig ermittelten Fingerabdruck:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

Die „Witness“-ZIP-Datei muss von einer unabhängigen, vertrauenswürdigen Quelle stammen; bewahren Sie auch deren Schlüssel und Herkunft auf. Behalten Sie die Befehle, die Tool-Version, die Ausgaben, die überprüften Eingabe- Hashes und die ungeklärten Fragen bei. Die Beacon-Verifizierung ist eine separate Online-Prüfung; der Berichtsrenderer kontaktiert niemals einen Dienst, nur um einen Bericht anzuzeigen.

Bei Streitigkeiten über eine bestimmte Nachricht sind die Archivreferenz, die maßgebliche Datei- und Datensatzreferenz anzugeben und anschließend der relevante Zeitrahmen, Erfassungslücken, die Auswahl sowie bestätigendes Material zu beschreiben. Bei einer Kopie zur Weitergabe sind zudem die aufgezeichnete Transformation und deren Verweise auf das Quellarchiv zu überprüfen. Private Filter und Identitätszuordnungen bleiben von der öffentlichen Bewertung ausgeschlossen.

Die Überprüfung der signierten PDF-Datei erkennt Änderungen an den abgedeckten Bytes. Bewahren Sie die ursprüngliche digitale Datei und das Überprüfungsergebnis zusammen mit etwaigen Screenshots oder ausgedruckten Lesekopien auf.
