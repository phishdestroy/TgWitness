# Ein Protokoll. Vier Erfassungsmodi. Acht Verifizierungsstufen.

Canonical page: https://phishdestroy.github.io/TgWitness/de/guides/modes.html

Modi, Szenarien und Evidenzstufen

TgWitness Zeichnet auf, was das verbundene Konto beobachtet. Ein Dritter kann die Integrität der Aufzeichnung anhand eines unabhängig vertrauenswürdigen Schlüssels überprüfen.

[Erfassungsmodi](https://phishdestroy.github.io/TgWitness/de/guides/modes.html#scope)[Szenarien](https://phishdestroy.github.io/TgWitness/de/guides/modes.html#scenarios)[Beweisstufen](https://phishdestroy.github.io/TgWitness/de/guides/modes.html#levels)

3–5-minütiger Überblick · fiktive Beispiele · aktuelle Implementierung

1. **Telegram**

   Für das Konto sichtbare Aktualisierungen
2. **Collector**

   Verknüpfte Datensätze, jeweils signiert
3. **Verifizierer**

   Vertrauenswürdiger Schlüssel + beibehaltene Grenze

`h₁ → h₂ → h₃ · Ed25519`Die Integrität wird überprüft. Die Herkunft aus Telegram und die Richtigkeit einer Nachricht bleiben getrennte Fragen.

## Wählen Sie den Beobachtungsumfang

Drei Bereiche und eine voreingestellte Untersuchung. Ausschlüsse und aktivierte Quelltypen gelten weiterhin.

Standard**Ausgewählte Chats**

Datensätze

Ausschließlich manuell ausgewählte Quellen.

Neue Chats

Wird nicht automatisch hinzugefügt.

Wählen Sie

Eine bekannte Menge von Kanälen oder Gruppen. Es wurde keine feste Chat-Kapazität festgelegt.

**Tut nicht** Es erkennt keine anderen Chats und füllt keine früheren Verlaufsdaten nach.

Kontoordner**Telegram-Ordner**

Datensätze

Eingeschlossene Ordner und Kategorien, abzüglich Ausschlüsse und archivierter Chats, sofern konfiguriert.

Neue Chats

Abgleich aktiver Chats; Ordneränderungen innerhalb einer Stunde.

Wählen Sie

Ein Analyst führt bereits eine Fallakte. Bestätigen Sie die Erfassung auf einem dafür vorgesehenen Konto.

**Tut nicht** Die sich ändernden Bedingungen des Ordners muted/read Bedingungen des Ordners an.

Geltungsbereich bestätigen**Gesamter Beitrag**

Datensätze

Für das Konto sichtbare Chats, einschließlich privater Unterhaltungen und Bots, innerhalb ausgewählter Typen.

Neue Chats

Wird hinzugefügt, sobald das erste Update eintrifft.

Wählen Sie

Ein spezielles Beobachtungskonto, einschließlich eines Kontos, das an einem Fall beteiligt ist.

**Tut nicht** Es tritt nicht automatisch Chats bei und umgeht auch nicht den Zugriff auf die Quelle.

Voreinstellung für das gesamte Konto**Untersuchungsmodus**

Datensätze

Alle Quelltypen, eigene Aktionen, Quellenprofile und die letzten 200 sichtbaren Nachrichten neu entdeckter Quellen.

Neue Chats

Ein neuer Chat oder Bot erhält ein Profil und einen Momentaufnahme des Verlaufs.

Wählen Sie

Treten Sie einem Team bei oder interagieren Sie über das Bedienfeld mit einem Bot. Überprüfen und speichern Sie die Voreinstellung.

**Tut nicht** Es werden nicht alle bestehenden Chats erfasst, und es werden keine in einem anderen Client ausgelösten Callbacks beobachtet.

Diese Karten dienen einem lokalen Vergleich und stellen keine Live-Steuerelemente des Collectors dar. Sie nehmen keine Änderungen an einem Konto vor.

**Tut nicht** Kein Modus liest geheime Chats aus, zeichnet auf, während der Prozess angehalten ist, tritt eigenständig Quellen bei oder ruft frühere Verlaufsdaten ab, die über die angeforderte snapshot/export.

[Lesen Sie die Details](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/)

## Erfassung mit GitHub Actions (Vorschau)

Neue Telegram-Anmeldung, ein Chat, ein verschlüsseltes Archiv und ein GitHub-Herkunftsnachweis.

[Erfassungsassistent öffnen](https://phishdestroy.github.io/TgWitness/de/docs/capture/)

## Was wird aufgezeichnet?

Nur übermittelte oder ausdrücklich angeforderte Beobachtungen werden in das Protokoll aufgenommen. Unbekannte Zuordnungen bleiben unbekannt.

 Schalter erfassen · lokale DarstellungNeue NachrichtenBearbeitungenLöschungenReaktionenMitgliedschaft

Das Bedienfeld wendet diese Schalter pro Arbeitsbereich an. Das Deaktivieren eines Schalters bewahrt bestehende Datensätze; das erneute Aktivieren stellt verpasste Ereignisse nicht wieder her.

**Ereignismatrix: gesichertes Material und verbleibende Unbekannte**

| Kategorie | Gespeichert | Bleibt unbekannt |
| --- | --- | --- |
| Nachricht | Text, IDs, Absender-Metadaten, Antwortkontext und ursprünglicher Update-Envelope. | Keine von Dritten überprüfbare Telegram-Signatur. |
| Bearbeiten | Jede beobachtete Version, ohne frühere zu überschreiben. | Zwischenzeitliche Bearbeitungen können übersehen werden; der Absender ist nicht zwangsläufig der Bearbeiter. |
| Löschung | Hinweis sowie zuvor gespeicherter Text, sofern verfügbar. | Der Löschvorgang und der genaue Zeitpunkt der Aktion werden nicht angegeben. |
| Löschen ohne Geltungsbereich | Hinweis auf Kontoebene; unbekannte Peers bleiben explizit. | Keine vermuteten Chats. Die Korrelation nutzt nach Möglichkeit zuvor gespeicherte, auf das Konto bezogene IDs. |
| Reaktion | Übermittelte Zähler und sichtbare aktuelle Identitäten. | Nicht jeder Reaktor ist sichtbar; eine vollständige Liste der verfügbaren Reaktoren erfordert separate Abfragen. |
| Mitgliedschaft | Zugestellte Dienstmeldungen und Teilnehmer-Updates. | Rolle und Chat-Typ schränken die Sichtbarkeit ein; Schweigen bedeutet nicht Abwesenheit. |
| Anhang | Deskriptor der Originalversion, gespeicherte Bytes, SHA-256 sowie Ergebnisse der Versuche. | Eine verschwundene Datei ist möglicherweise nicht mehr verfügbar; eine neuere Version ersetzt sie nicht. |
| Historischer Momentaufnahme | Derzeit sichtbare Nachrichten, die als Verlaufsbeobachtungen gekennzeichnet sind. | Frühere Bearbeitungen und verschwundene Inhalte werden nicht rekonstruiert. |
| Eigene Handlungen | Ausgehende messages/edits sowie die entsprechenden Metadaten der Antworttastatur button_press Metadaten. | In einem anderen Telegram-Client ausgelöste Callbacks sind nicht sichtbar. |
| Bot-Schaltflächen | Callback, URL, Web-App und Metadaten der Anfrage werden mit der Nachricht beibehalten. | URLs und phone/location Anfragen sind Text und werden nicht automatisch geöffnet oder ausgeführt. |

### Standardmäßige Anhangsbeschränkungen

Fotos

20 MiB

Video

100 MiB

Dateien

50 MiB

Animationen

20 MiB

Video-Notizen

50 MiB

Sprache

20 MiB

Audio

50 MiB

Sticker

5 MiB

**Tut nicht** Ein Schalter löscht keine eingebetteten Metadaten und deaktiviert keine Betriebsprotokolle. Die Erfassung identifiziert keinen Akteur, den Telegram nicht bereitgestellt hat.

[Lesen Sie die Details](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/)

## Nutzen Sie die Ihnen zur Verfügung stehenden Berechtigungen

Jedes Konto verfügt über einen eigenen Arbeitsbereich, ein eigenes Protokoll, einen eigenen Signaturschlüssel, eine eigene Route und eine eigene Warteschlange.

### Telefonnummer + Code

Geben Sie 2FA , wenn diese Option aktiviert ist.

### QR code

Scannen Sie von einem autorisierten Gerät aus; 2FA dies kann weiterhin erforderlich sein.

### Telethon .session

Importieren Sie die Sitzungsdatei des Kontos.

### Pyrogram .session

Importieren Sie das unterstützte Pyrogram Sitzungsformat.

### TData ZIP

Ein unterstütztes Desktop-Konto; lokaler Passcode, falls festgelegt.

### StringSession text

Fügen Sie ein Telethon StringSession.

### .session + .json

Wählen Sie die Sitzung und die dazugehörigen Metadaten aus.

### Authentifizierungsschlüssel HEX + DC ID

Importieren Sie die Kontoautorisierung zusammen mit ihrer Rechenzentrums-Kennung.

**API Paar**

Ihr eigenes API Paar ist optional. Ohne ein solches TgWitness wird ein Pool öffentlicher Paare verwendet, einschließlich Paare aus dem offiziellen Telegram Desktop.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy ist experimentell; integrierte öffentliche MTProxy Listen stehen zur Verfügung. Eine fehlgeschlagene Proxy-Route weicht nicht auf eine direkte Verbindung aus.

Zwei Arbeitsbereiche auf einem Rechner stellen keine zwei unabhängigen Zeugen dar.

**Tut nicht** Der Import umgeht weder die Telegram-Autorisierung noch 2FA noch nicht unterstützte Sitzungsformate. Die Konten nutzen weiterhin denselben Anwendungsprozess.

[Kontoformate](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/)

## Handeln Sie über das Bedienfeld

Senden oder antworten Sie, drücken Sie eine aktuelle Bot-Schaltfläche, speichern Sie eine Link-Vorschau und treten Sie anschließend explizit einem Chat bei oder starten Sie einen Bot mit dessen Startparameter.

`interaction.preview``interaction.requested``interaction.result`

Vorschau-, Anforderungs- und Ergebnisbestätigungen sind signiert. Vor dem Drücken einer Schaltfläche ruft der Server die Nachricht erneut ab und lehnt eine geänderte Eingabe ab. Zurückgesendete Callback-Texte und URLs bleiben als aufgezeichneter Kontext erhalten.

**Tut nicht** Keine Web-Apps, Zahlungen, phone/location Freigaben oder Inline-Abfragen. Das Anzeigen einer URL führt nicht zu deren Öffnung.

[Lesen Sie die Details](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/)

## Wiederherstellung und Kontinuität

Lücken werden aufgezeigt, nicht verborgen.

### Fahren Sie an der gespeicherten Position fort

Nach einem Neustart wird Telegram nach verpassten Aktualisierungen gefragt. Eine begrenzte Aufbewahrungsdauer und abgelaufene Differenzen können Lücken hinterlassen.

### Sichtbare Nachrichten erneut überprüfen

Standardeinstellungen: Prioritätsquellen alle 15 Minuten, andere alle 6 Stunden. Zu den Ergebnissen gehören message.recovered und message.missing_on_recheck.

### Lesen coverage.json

Beobachtungszeiträume, Lücken mit Begründungen und nicht beobachtete IDs sind im signierten Export enthalten. Ein Eintrag „bei erneuter Überprüfung nicht vorhanden“ ist keine Löschmitteilung.

**Tut nicht** Ein späterer Verlaufs-Snapshot löscht keinen Ausfall und stellt nicht jede verschwundene Version wieder her. Der gespeicherte Cursor ist keine verlustfreie Bestätigung der Protokollannahme.

[Lesen Sie die Details](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/)

## Sieben Ebenen. Unterschiedliche Fragen.

Jeder Mechanismus beantwortet eine klar abgegrenzte Frage. Konfigurieren Sie externe Dienste separat und bewahren Sie deren Vertrauensanker außerhalb des Collectors auf.

1. ### Aufzeichnen

   SHA-256 Kette + Ed25519 pro Ereignis; die erste previous_hash besteht aus 64 Nullen.

   **Überprüfungen durch Dritte** Reihenfolge und Signaturen unter dem festgesteckten Collector-Schlüssel.

   **Tut nicht** Dies belegt weder die Herkunft aus Telegram noch die Vollständigkeit.

   **Verifizierungsbefehl**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Container

   manifest.json listet Datei-Hashes auf; manifest.sig signiert diese. media.saved verknüpft Anhangsbytes mit einem Ereignis.

   **Überprüfungen durch Dritte** Die bereitgestellten Dateien stimmen mit dem signierten Manifest und den Medienbelegen überein.

   **Tut nicht** Es signiert weder eine separat heruntergeladene CSV, HTML oder Screenshot.

   **Verifizierungsbefehl**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Beibehaltene Grenze

   Checkpoint beim Start, standardmäßig alle 5 Minuten, sowie ordnungsgemäßer Abbruch. Bewahren Sie eine Kopie an einem anderen Ort auf.

   **Überprüfungen durch Dritte** Der spätere Export stimmt mit einer zuvor gespeicherten Länge und einem zuvor gespeicherten Header überein; ein Rollback kann erkannt werden.

   **Tut nicht** Es erkennt nicht, wenn sowohl das Protokoll als auch alle gespeicherten Kontrollpunkte ersetzt werden.

   **Verifizierungsbefehl**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### Externe Zeit

   Der Evidenzmodus sendet einen Checkpoint SHA-256 an RFC 3161 Behörden (FreeTSA, DigiCert) sowie OpenTimestamps Kalendern.

   **Überprüfungen durch Dritte** Eine verifizierte TSA-Antwort datiert diese Bytes; ein bestätigter OpenTimestamps Nachweis verankert sie in Bitcoin.

   **Tut nicht** Eine vorbereitete Anfrage oder eine ausstehende Kalenderbestätigung wird nicht als bestätigter Zeitstempel behandelt.

   **Verifizierungsbefehl**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Unabhängiger Zeuge

   Getrennter Host, bereichsgebundener, schreibgeschützter Endpunkt, neue Herausforderung, eigene key/journal sowie TGW1 Kanalbeiträge.

   **Überprüfungen durch Dritte** Zuvor akzeptierte Heads; Status: ok, key_changed, „Rollback“, „Fork“, „ungültig“ und no_response.

   **Tut nicht** Dies macht zwei Arbeitsbereiche auf einem Collector-Host nicht zu unabhängigen Zeugen.

   **Verifizierungsbefehl**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Externe Replik

   S3-kompatible Kopie, verschlüsselt mit AES-256-GCM; Object Lock , sofern der Bucket dies unterstützt.

   **Überprüfungen durch Dritte** „Restore“ veröffentlicht Dateien erst, nachdem die Überprüfung des Protokolls, des Checkpoints und der gesicherten Medien erfolgreich abgeschlossen wurde.

   **Tut nicht** Eine Wiederherstellung ohne den exportierten Schlüssel ist nicht möglich, und eine Aufbewahrung wird nicht vorausgesetzt, ohne die Speicherantwort zu überprüfen.

   **Verifizierungsbefehl**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Herkunft nachweisen

   Signierte Ausführungsbestätigung: Quell-Hashes, Versionen der Abhängigkeiten und Prozesskontext. Selbst gemeldet.

   **Überprüfungen durch Dritte** Was der Signatur-Kollektor über seine eigene Ausführung gemeldet hat.

   **Tut nicht** Es bietet keine unabhängige Prozessbeglaubigung und schließt eine Kompromittierung vor der Aufzeichnung nicht aus.

   **Verifizierungsbefehl**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### Was keine Stufe beweist

Übermittlung jedes Telegram-Updates; die Richtigkeit des Textes; dass eine Absender-ID eine reale Person identifiziert; das Fehlen einer Kompromittierung des Erfassers vor der Aufzeichnung; die Zulässigkeit vor Gericht.

[Unabhängiger Zeuge](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/)

Lokales SHA-256 Experiment

### Versuchen Sie, Datensatz 2 zu ändern

Der nächste Datensatz behält den zuvor gespeicherten Link bei. Eine Änderung des Textes verändert den berechneten Hash von Datensatz 2.

Text von Datensatz 2

Eintrag 1`h1`Beginnt mit 64 Nullen

Eintrag 2`h2`Enthält die gespeicherten h1

Eintrag 3`h3`Enthält die gespeicherten h2

Statisches Beispiel: h2 bezieht sich auf „Treffen um 11:00 Uhr“. Eine Änderung dieses Textes verändert h2; Datensatz 3 verweist weiterhin auf den gespeicherten h2.

**Überprüfen Sie die vollständigen Digests**

Hash des gespeicherten Datensatzes 2

`SHA-256(e₂)`

Neu berechneter Hash von Datensatz 2

`SHA-256(e₂)`

Dieses Beispiel berechnet Hashes, keine Signaturen. Der eigentliche Verifizierer gleicht jede Signatur und jeden Link mit dem vertrauenswürdigen Schlüssel ab.

 [Lesen Sie die Details](https://phishdestroy.github.io/TgWitness/de/docs/reference/how-it-works/)

## Wählen Sie einen Weg durch die Beweislage

Fiktive Situationen. Beginnen Sie die Erfassung vor dem relevanten Ereignis; bewahren Sie neben dem Inhalt auch die Grenzen und Lücken.

### Ein Kanal ändert seine Zahlungsdaten

Modus → Ereignisse

Ausgewählte Chats → Nachrichten, Bearbeitungen, Löschungen.

Ausgabe

Beobachtete Beitragsversionen und Anhänge anhand des Hash-Werts.

Verifizierung

Signiert ZIP + beibehaltener Checkpoint + verifizierte TSA-Antwort.

**Tut nicht** Es stellt kein Original wieder her, das nie erfasst wurde.

### Nachrichten verschwinden nach einem Vorfall

Modus → Ereignisse

Ordner oder gesamtes Konto → alle Ereigniskategorien.

Ausgabe

Gespeicherte Originale, Löschhinweise und lückenhafte Abdeckung.

Verifizierung

Unterzeichnet ZIP + unabhängiges Zeugenprotokoll.

**Tut nicht** Er identifiziert den Löschenden nicht anhand einer Benachrichtigung, die keinen Akteur angibt.

### Untersuchen Sie einen Shop-Bot

Modus → Ereignisse

Voreinstellung „Untersuchung“ → Schaltflächen, Link-Vorschauen und expliziter Bot-Start.

Ausgabe

Signierte Interaktionsbelege, zurückgegebene Callbacks und gespeicherte Profile.

Verifizierung

Unterzeichnet ZIP; überprüfen Sie jedes Dossier anhand des ZIP.

**Tut nicht** Es öffnet keine Bot-Web-App, führt keine Zahlungen durch und zeichnet keine Callbacks anderer Clients auf.

### Ein Teilnehmer wechselt seine Namen in verschiedenen Chats

Modus → Ereignisse

Jeder Geltungsbereich → beobachtete sender/profile Metadaten.

Ausgabe

Verlauf von Namen/Benutzernamen anhand numerischer IDs, „auch in“-Links und extrahierten Hinweisen.

Verifizierung

Das Dossier JSON gegen die signierte Version abgeglichen ZIP.

**Tut nicht** Er wandelt weder eine Wallet noch eine telefonähnliche Zeichenfolge oder einen Benutzernamen in eine nachgewiesene Identität um.

### Langfristige Beobachtung mit einer externen Kopie

Modus → Ereignisse

Beliebiger Geltungsbereich → Evidenzmodus und eine S3 Replik mit unterstützten Object Lock.

Ausgabe

Verschlüsselte Kopie, gespeicherte Checkpoints und Antworten mit Zeitstempel.

Verifizierung

Stellen Sie die Daten mit dem exportierten Schlüssel wieder her und überprüfen Sie sie anschließend ohne den ursprünglichen Server.

**Tut nicht** Es ersetzt weder einen unabhängigen Zeugen noch einen separat aufbewahrten Entschlüsselungsschlüssel.

[Lesen Sie die Details](https://phishdestroy.github.io/TgWitness/de/docs/reference/investigation/)

## Übergeben Sie ein überprüfbares Paket

Legen Sie das signierte Original, einen unabhängig gespeicherten Schlüssel-Fingerabdruck, den entsprechenden Checkpoint und das Verifizierungsergebnis vor.

- Unterzeichnet ZIP
- JSONL
- CSV
- HTML
- Checkpoint
- Ausführungsbeleg
- Chat-Export: chat.json / chat.html
- Dossier JSON
- Passwortgeschützt AES-256 ZIP
- Getrennte Exporte für mehrere Konten
- Streaming-CLI: 5 GiB Standardlimit

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Beziehen Sie den Verifizierer aus einer vertrauenswürdigen Kopie, nicht aus dem zu überprüfenden Archiv.

**Tut nicht** Standalone CSV und HTML sind keine signierten Container. Ein Passwort schützt die Vertraulichkeit der Übertragung, nicht die Authentizität. Mehrere Exporte führen nicht zu einer Zusammenführung der Kontoprotokolle.

[Lesen Sie die Details](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/)

## Vergleichen Sie das gelieferte Artefakt

Grundlegende Artefakte ohne zusätzliche Signatur-, Zeitstempel- oder Zeugen-Systeme. Skripte und Logger variieren je nach Implementierung; „teilweise“ bedeutet, dass sie auf erfasste oder sichtbare Daten beschränkt sind.

| Vorgehensweise | Bearbeitungen / Löschungen | Signatur aufzeichnen | Externe Zeit | Unabhängiger Zeuge | Abdeckung / Lücken | Verifizierung ohne Autor |
| --- | --- | --- | --- | --- | --- | --- |
| Telegram-Desktop-Export | Teilweise | Nein | Nein | Nein | Nein | Nein |
| Telethon Snapshot-Skript | Teilweise | Nein | Nein | Nein | Nein | Nein |
| Löschprotokoll: Textprotokoll | Teilweise | Nein | Nein | Nein | Nein | Nein |
| Screenshots / Web-Aufnahmen | Teilweise | Nein | Nein | Nein | Nein | Nein |
| TgWitness mit konfigurierten Zusatzfunktionen | Teilweise | Ja | Ja | Ja | Teilweise | Ja |

**Tut nicht** Die Tabelle bewertet nicht jedes Skript oder jedes Protokollierungsprodukt. Optionale Zeit- und Zeugenprüfungen erfordern eigene Dienste und Vertrauensanker; keiner davon begründet die „Source Truth“.

[Lesen Sie die Details](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/)

## Halten Sie sich an die Grenzen der Beweislage

Eine Verifizierung ist dann sinnvoll, wenn ihr Umfang eindeutig definiert bleibt.

- Geheime Chats sind nicht verfügbar.
- Solange der Prozess angehalten ist, wird nichts aufgezeichnet; die Wiederherstellungsmöglichkeiten sind begrenzt.
- Ein verifizierter Datensatz ist kein Beweis dafür, dass sein Inhalt wahr ist.
- Ein Betreiber, der über den Schlüssel verfügt, kann beliebige Inhalte signieren. Unabhängige Zeugen und Zeitstempel verhindern ein nachträgliches Ersetzen, nicht jedoch eine unredliche Erfassung bei der Erstellung.
- Verwenden Sie ein eigens dafür vorgesehenes Konto, nicht Ihr Hauptkonto.
- Telegram kann Konten aufgrund des Anfragevolumens einschränken.

**Tut nicht** Kein Modus und keine Beweisstufe begründen die rechtliche Zulässigkeit, die vollständige Zustellung über Telegram oder eine Identität in der realen Welt.

[Einrichtungsanleitung](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=de)[Spezielles Konto](https://phishdestroy.github.io/TgWitness/de/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/de/docs/reference/investigation/)
