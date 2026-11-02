# Case-Board-Referenz

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/case-board/

Lesezeichen, exakte Markierungen, Aktionsausschnitte, Diskussionen, bereichsbezogener Zugriff und der von Case Board verwendete Verlauf der signierten Anmerkungen.

Case Board bietet einem Ermittlungsteam eine gemeinsame Arbeitsansicht des gespeicherten Materials. Setzen Sie ein Lesezeichen für eine Beobachtung, markieren Sie eine bestimmte Passage, speichern Sie eine Reihe von Aktionen und besprechen Sie diese mit Kollegen. Karten behalten ihre Quellenverweise und den signierten Revisionsverlauf bei. Team-Anmerkungen verbleiben im Arbeitsbereich und sind separat von den ursprünglichen Telegram-Beobachtungen erkennbar.

[Beweismodell](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/) · [Zugriff](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/) · [Berichte](https://phishdestroy.github.io/TgWitness/de/docs/reference/case-reports/)

![Zusammenfassung der Ermittlungsergebnisse](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

## Arbeiten mit einem Fall

Öffnen Sie **„Untersuchung“ → „Case Board“** im Standard- oder Expertenmodus. Die Sprache richtet sich nach dem jeweiligen Bereich. Verwenden Sie **die** **Schaltfläche** **„Zum Board hinzufügen“** neben einem Tagebucheintrag oder einer gespeicherten Chat-Nachricht, oder markieren Sie diese und drücken Sie **B**. Das Lesezeichen wird mit einem Klick zum Posteingang hinzugefügt. Bearbeiten Sie dessen Titel, Etiketten und Notiz oder verschieben Sie es in eine Sammlung. Eine geänderte Karte wird mit einer signierten Revision versehen; beim Entfernen bleibt der Verlauf erhalten.

Wählen Sie für einen ersten Fall eine Erfassung aus und fügen Sie die Datensätze hinzu, die eine Frage beantworten. Verwenden Sie Kommentare, um die Interpretation zu überprüfen, und nutzen Sie anschließend **„Präsentation“**, um die Karten und den Quellenkontext durchzugehen. Wählen Sie das Material für das Case Board separat im [„Report Studio“](https://phishdestroy.github.io/TgWitness/de/docs/reference/case-reports/) aus, wenn Sie das Ergebnisdokument vorbereiten. Das Speichern eines Ausschnitts konfiguriert nicht automatisch die Datenfilter eines Berichts.

Markieren Sie Text innerhalb einer gespeicherten Chat-Nachricht, um **„Highlight → Board“** anzuzeigen. Wählen Sie die Farbe aus und fügen Sie eine Notiz hinzu. Der Server überprüft das genaue Zitat und die gespeicherte Version, einschließlich Emojis, RTL-Text und Kombinationszeichen. Die Benutzeroberfläche bildet eine Auswahl nicht durch maskierten oder transformierten Text ab.

Wählen Sie mit Umschalt-Klick zwei Datensätze in einem Chat aus, um **einen Ausschnitt dazwischen** zu erstellen, verwenden Sie **den Ausschnitt nach Zeit** oder speichern Sie die aktuellen Filter des Journals für Chat, Zeitraum und Ereignistyp. Ein gespeicherter Ausschnitt verfügt über ein eigenes maßgebliches Prädikat: Beim Öffnen im Journal werden auch mehrere Chats, Begrenzungen der Nachrichtenanzahl und Akteur-Filter angewendet. **„Seit Lesezeichen hinzugefügte Datensätze anzeigen“** isoliert die späteren Ergänzungen. Das Ändern von Journal-Filtern beendet den Ausschnitt. Unter „Personen“ verwendet **„Aktionen dieser Person ausschneiden“** die aufgezeichnete Akteur-ID; es wird nicht davon ausgegangen, dass der Verfasser einer Nachricht diese bearbeitet, gelöscht oder darauf reagiert hat.

Der „Slice“-Dialog zeigt eine Vorschau der Anzahl an, bevor die Erstellung zugelassen wird. „`all`“ umfasst alle aufgezeichneten Arten, einschließlich Momentaufnahmen, Bearbeitungen, Löschungen, Reaktionen, Aktualisierungen von Mitgliedschaften/Diensten, eigener Aktionen, Schaltflächen, Medienausgaben, wiederhergestellter Nachrichten und zukünftiger Ereignistypen. Die Auswahl beschreibt gespeicherte Beobachtungen. Löschbenachrichtigungen für unbekannte Chats stellen einen separaten Kontext dar, der nur bei Zugriff auf den gesamten Arbeitsbereich verfügbar ist und niemals einem der ausgewählten Chats zugeordnet wird.

Sammlungen haben einen festgelegten Chat-Umfang. Ein leerer Umfang bedeutet den gesamten Arbeitsbereich. Eine Sammlung kann keine Karten außerhalb ihres Umfangs enthalten; ein auf einen Chat beschränkter Teilnehmer kann keine umfassendere Sammlung einsehen. Der Posteingang ist eine virtuelle Sammlung für nicht zugewiesene Karten. Suche und Filter gelten nur für sichtbare Karten; Threads und Erwähnungen erben die Zugriffsrechte der übergeordneten Karte. Gelöschte Kommentare werden in der Diskussion als „Tombstone“ angezeigt. Es wird kein Verlauf der Betrachter aufgezeichnet.

**Die Präsentationsansicht** öffnet alle Karten in der ausgewählten Sammlung und bietet die Ansichten „Karte“, „Quellenkontext“ und „Teamkommentare“ sowie die Tastaturbefehle „Zurück“ und „Weiter“. Sie bietet keine Bearbeitungsfunktionen. Der normale Feed ist paginiert; die Präsentationsansicht lädt die Liste seitenweise und ruft jeweils die Details einer einzelnen Karte ab.

## Berechtigungen

Alle Vorgänge erfordern die Berechtigungen „`view`“, „workspace/chat scope“ und „`board.read`“. „`board.write`“ fügt Karten, Kommentare, Verschiebungen sowie den Status „offen“ oder „überprüft“ hinzu. „`board.manage`“ ermöglicht die Verwaltung der Sammlung, den Status „bestätigt“ oder „abgelehnt“ sowie die Überarbeitung oder Entfernung von Karten anderer Benutzer. Ein Status ist eine Teamentscheidung, kein Ergebnis einer kryptografischen Überprüfung.

Zugriffsvoreinstellungen: Prüfer = Lesen; Analyst = Lesen/Schreiben; Operator = Lesen/Schreiben/Verwalten, zusätzlich zu ihren bestehenden Berechtigungen. Bestehende Berechtigungen führen nicht automatisch zur Erlangung neuer Rechte. Der Hauptadministrator verfügt über alle Rechte und veröffentlicht als **„Hauptadministrator**“. Verwenden Sie benannte Berechtigungen zur Zuordnung. In den Erwähnungen werden nur aktuelle Zugriffe aufgeführt, die die vollständige übergeordnete Karte lesen können.

Ein Zugriffsrecht für Chat A kann keine Karte oder keinen Ausschnitt für A+B erhalten, selbst wenn die ID erraten oder eine falsche „`target.chat_id`“ angegeben wird. Die Metadaten des Ziels werden anhand des signierten Ereignis-Hashes auf dem Server ermittelt. Sammlungen, Diskussionszahlen, zugehörige Karten und Live-Benachrichtigungen werden vor der Antwort gefiltert. exports erfordern sowohl „`export`“ als auch „`board.read`“; ein bestehender Exporter ohne Board-Zugriff erhält das normale Beweismittelarchiv ohne Teamnotizen. SSE überprüft vor jedem Stapel die aktuellen Berechtigungen erneut.

## Gespeicherte Verträge

Genau wie Beobachtungen werden Anmerkungen transaktional in eine nur-anfügen-fähige SQLite-Tabelle im Arbeitsbereich geschrieben. „`annotations.jsonl`“ ist der exakte kanonische Export aus demselben Lese-Snapshot wie „`events.jsonl`“. Es gibt keinen zweiten konkurrierenden Anmerkungsspeicher und kein „`board.activity`“-Journalereignis.

Jede Zeile enthält genau:

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

Das obige verkürzte Beispiel veranschaulicht den „Envelope“; tatsächliche Nutzdaten enthalten ihre Modell- Standardwerte und vom Server aufgelöste Zielfelder. API-Anfrageschemata befinden sich unter „ [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json)“ und werden aus den Laufzeit-Pydantic- Modellen durch das `python tools/build_board_schemas.py` generiert. Zusätzliche Anfragefelder werden abgelehnt. IDs werden serverseitig generiert, wenn sie weggelassen werden. Urheberschaft, Zeit, Snapshot und Signatur können nicht vom Aufrufer angegeben werden. Benannte Berechtigungs-IDs folgen dem bestehenden 16-Hex-Format von Access; Karten-IDs sind 32 Hex.

Das kanonische JSON ist in UTF-8, mit sortierten Objektschlüsseln, ohne Leerzeichen zwischen den Tokens, mit unescaped Unicode und ohne NaN/Unendlichkeitswerte. Der Anmerkungs-Hash ist ein SHA-256 des kanonischen Objekts, das das `format: "tgwitness-annotations-v1"` sowie alle sieben Envelope-Felder bis einschließlich `previous_hash` enthält. Dieses Format-Tag trennt seine Hash-Domäne von den Beobachtungen. Die Signatur ist Ed25519 über die 32 Roh-Hash-Bytes. Die Sequenz beginnt bei 1. Revisionen behalten die Karten-ID bei und benennen den vorhergehenden Annotations-Hash in „`supersedes`“; sie können den Chat-Gültigkeitsbereich nicht ändern. Verschiebungen, Statusänderungen und Löschungen sind separate Datensätze. Die SQLite-Tabelle lehnt UPDATE- und DELETE-Befehle ab.

`case-board.json` enthält `{statement, signature}`. Die kanonische Aussage wird durch den Workspace-Schlüssel signiert und enthält `format: "tgwitness-case-board-v1"`, `public_key`, `created_at`, `journal_head`, `meaning` und `state`. Der Status ist eine deterministische Wiedergabe: `annotations_head`, ein geordnetes Array `items` (Sammlungen, Karten, Kommentare einschließlich Tombstones) und `status_history`. Elemente behalten ihren letzten Annotations-Hash, ihre Sequenz, ihren Autor und ihre Zeit sowie den ursprünglichen Ersteller und den Erstellungszeitpunkt über alle Revisionen hinweg bei. Die Wiedergabe überprüft Revisionen, übergeordnete Elemente, Sammlungsverweise und doppelte Aktions-IDs. „`manifest.json`“ und neue Checkpoints binden ebenfalls „`annotations_head`“. Bewahren Sie einen Checkpoint unabhängig auf, um eine Verkürzung oder ein Überschreiben mit einem kopierten Signaturschlüssel zu erkennen.

### Textversionen

„`range.start`“ ist ein nullbasierter Unicode-Codepunkt-Offset, „`length`“ ist eine positive Codepunktanzahl, und „`quote`“ muss genau der Teilzeichenfolge von „`payload.text`“ oder „`payload.caption`“ am Ziel- Ereignis entsprechen. Es wird keine NFC/NFKC, Groß-/Kleinschreibung oder Graphem-Normalisierung angewendet. Python-String-Slices und JavaScript-`Array.from(text)` implementieren dieselbe Indizierung. Die Kombination von Markierungen und ZWJ-Emojis kann mehrere Codepunkte einnehmen. „`range.version`“ ist der Hash des Zielereignisses, nicht die aktuelle Nachrichtenversion oder der UTF-16-Entity-Offset von Telegram. Spätere Bearbeitungen verschieben eine Markierung niemals automatisch.

### Identität und Zeit unterteilen

„`query`“ akzeptiert genau eine „`chat_id`“ oder nicht leere „`chat_ids`“, optional inklusive „`from`“/„`to`“, inklusive „message-ID“-Grenzen (nur ein Chat), „`kinds: "all"`“ oder exakte/Präfix-Platzhalter-Arten, explizite „`actors`“, „`search`“, „`hide_system`“ und „`include_unscoped`“. „Journal“-Artengruppen werden zu ihren exakten Prädikaten erweitert. Die Suche nutzt die NFC-/Case-Folded-Payload-Suche des Journals, ohne den signierten Quelltext zu verändern. Datumsangaben erfordern eine Zeitzone und werden auf UTC normiert. Datumsangaben filtern **„observed_at**“. Telegrams „`source_at`“ wird separat angezeigt. Eine Löschung ohne Quellzeitstempel hat keinen fiktiven Löschzeitpunkt. Ein später Datensatz, der außerhalb eines Zeitintervalls beobachtet wird, wird nicht in dieses aufgenommen; ein Message-ID-Ausschnitt kann eine spätere Löschung für diese Message-IDs enthalten.

„`snapshot`“ legt den Erstellungszeitpunkt, die Grenze zwischen Journalsequenz und Hash, die Anzahl der Übereinstimmungen sowie die erste und letzte Sequenz und den „`result_hash`“ fest. Letzterer ist der SHA-256-Hash des kanonischen UTF-8-JSON-Arrays der übereinstimmenden Ereignis-Hashes, lexikografisch sortiert, einschließlich `[]` für einen leeren Ausschnitt. Er enthält außerdem genaue Typanzahlen und eine 24-Bin-Miniatur der Beobachtungszeit. Ein „Slice“ speichert eine Abfrage, keine doppelten Quelldatensätze . Beim Export listet „`board/slices/<id>.json`“ aktuelle Hashes sowie hinzugefügte/entfernte Sequenzen auf. Der Verifizierer rekonstruiert zunächst das ursprüngliche Ergebnis an der Erstellungsgrenze und anschließend das aktuelle Ergebnis. Hinzugefügte Datensätze werden als Änderungsfakt gemeldet. Das Entfernen eines ursprünglichen Ereignisses unterbricht die unveränderliche Beweiskette; es wird nicht stillschweigend als gewöhnliche Entfernung aus einem Slice akzeptiert.

Reaktions-Snapshots weisen unvollständige Listen der jüngsten Akteure auf. Der Explorer vergleicht benachbarte Snapshots desselben Chats/derselben Nachricht, einschließlich eines Vorgängers außerhalb des Ausschnitts, und meldet aggregierte Zählungsdifferenzen **zwischen den Beobachtungen**. Bei fehlenden jüngsten Akteuren wird nicht behauptet, dass diese eine Reaktion entfernt hätten. Der erste Snapshot hat keinen abgeleiteten früheren Zustand. Akteurbeobachtungen bleiben dem Snapshot zugeordnet, in dem sie bereitgestellt wurden, und nicht einem fiktiven Aktionszeitpunkt.

## API und Exporte

`GET /api/board` akzeptiert collection/chat/author/label/state/from/to/q/kind/comments, offset/limit sowie die Sortierreihenfolge „neueste“ und „älteste“. `GET /api/board/card/{id}` gibt eine Karte, eine Quellenvorschau, den Thread, den Statusverlauf und zugehörige Karten zurück. Die Unterroute „Teilnehmer“ gibt zulässige Erwähnungsoptionen zurück. `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}` fügt einen Datensatz hinzu. `POST /api/board/slice-preview` berechnet eine Abfrage. Slice-Datensätze werden unter `GET /api/board/slice/{id}/records` paginiert; bei der Neuberechnung wird stets der aktuelle stabile Lese-Snapshot verwendet. Live `/api/stream` sendet payload-freie `board`-Benachrichtigungen, unabhängig von Journal-Cursorn.

`GET /api/board/export` gibt ein signiertes Dokument zurück. Bei chatbegrenztem Zugriff wird eine eindeutig gekennzeichnete, signierte **Offenlegung** bereitgestellt, niemals die Anmerkungen eines anderen Chats oder die gesamte Kette. Vollständige Beweismittel-ZIPs enthalten „`annotations.jsonl`“, ein signiertes „`case-board.json`“ sowie „Slice“-JSON-Anhänge. HTML/PDF/JSON-Berichtseinstellungen ermöglichen die Auswahl „kein Board“, Lesezeichen/Ausschnitte ohne Diskussion oder Karten mit Kommentaren. Der Abschnitt trennt Teammeinungen ausdrücklich von Beobachtungen. Berichtsdatenfilter schränken auch die lesbaren Notizen ein; vollständige signierte Quelldateien im Beweismaterial-ZIP bleiben unverändert.

`GET /api/board/slice/{id}/export` erzeugt einen signierten JSON-Auszug „`tgwitness-board-selection-v1`“; `?format=csv` erzeugt eine übersichtliche Tabelle ohne eigenständige Signatur. Behalten Sie das JSON und die ZIP-Datei bei:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

Die Auswahlprüfung authentifiziert die signierte Erklärung, die exakten Quelldatensätze und die Vollständigkeit der Abfrage an der angegebenen Grenze. Die Beweisdatei im ZIP-Format kann neuer sein, muss jedoch dieses Präfix enthalten. Ein fehlendes Ziel wird explizit gemeldet. Ein anderer ursprünglicher Slice-Snapshot, eine geänderte Anmerkung, ein nicht übereinstimmender Wiedergabestatus oder eine geänderte Quelle führen zum Fehlschlagen. Alte Archive ohne Anmerkungen behalten ihr bestehendes Verifizierungsverhalten bei.

Die Übergabe ist standardmäßig auf **„Nicht einbeziehen“** eingestellt. Die explizite Einbeziehung projiziert Karten über die bereits minimierten Datensätze, lässt unzugängliche/ausgelassene Ziele weg, unterdrückt Hervorhebungen, deren Quelltext minimiert wurde, bereinigt Teamtext nach denselben Erwähnungs-/Kontaktregeln und ersetzt optional Ermittlerbezeichnungen durch R01, R02… in Metadaten und bekannten Vorkommen in Notizen. Es wird keine ursprüngliche „ `annotations.jsonl`“-Datei offengelegt. Die signierte „`tgwitness-case-board-handover-v1`“-Sidecar-Datei und der Bericht enthalten dasselbe minimierte Material. Die Slice-Zählungen beschreiben nur offengelegte Datensätze, wobei ursprüngliche Snapshot-/Abfrage-Akteur-Details zurückgehalten werden. Freitext-Namen, die dem Minimierer nicht bekannt sind, müssen weiterhin überprüft werden, wie dies auch bei gewöhnlichen Übergaben der Fall ist. Diese Ableitung erhebt keinen Anspruch darauf, die ursprünglichen Annotationssignaturen nach der Schwärzung beizubehalten.

## Anwendungsgrenzen

Zu den Parametern gehören weiche Begrenzungen von 10.000 Karten und 50.000 Kommentaren, eine „Slice“-Seite mit bis zu 5.000 Datensätzen sowie die Steuerung der Medienvorschau. Weiche Begrenzungen lösen eine Warnung aus, ohne den Verlauf zu löschen. Feed-Seiten umfassen höchstens 200 Karten. Eigenständige JSON-Ausschnitte sind auf 64 MiB begrenzt; schränken Sie die Abfrage ein oder verwenden Sie die signierte ZIP-Datei für umfangreicheres Material. Der eigenständige Verifizierer begrenzt die Wiedergabe von Anmerkungen auf 256 MiB. Externe Benachrichtigungen zu Kommentaren sind in Case Board weder aktiviert noch implementiert.

Die automatisierte Abnahme der Funktion nutzt fiktive Daten und einen simulierten Telegram-Transport, um Speicherung, Zugriff, Darstellung und Exporte zu überprüfen. Den Umfang der Beweismittelprüfungen entnehmen Sie bitte [dem Verifizierungsumfang](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope) .
