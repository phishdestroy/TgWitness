# Format der Beweismittel

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/

Inhalt der signierten ZIP-Datei, Protokolltypen, Prozessbestätigungen, Benutzerprofile, externe Kopien und Offline-Überprüfung.

TgWitness sichert für das Konto sichtbare Telegram-Beobachtungen in einem signierten Protokoll. Empfänger können die gespeicherten Datensätze, Anhänge und Berichte anhand eines vertrauenswürdigen Collector-Schlüssels verifizieren und anschließend das Protokoll mit einem unabhängig aufbewahrten Checkpoint vergleichen. Diese Seite beschreibt die Formate, die Prüfungen und das Material, das für die Übergabe aufzubewahren ist.

Recipients can start with **VERIFY.cmd** on Windows: it asks for the original ZIP and independently obtained key fingerprint, displays an explained result, and saves a separate verification transcript. See [verification launchers and the portable runtime](https://github.com/phishdestroy/TgWitness/blob/main/docs/VERIFICATION_LAUNCHER.md) for setup and trust limits.

## Was ist signiert?

| Material | Schutz | Was ist zu beachten? |
| --- | --- | --- |
| Jeder Eintrag im Protokoll, einschließlich operativer Ereignisse | SHA-256-Kette und eine Ed25519-Signatur pro Ereignis | Original-`events.jsonl`, der Fingerabdruck des vertrauenswürdigen Schlüssels, sowie ein gespeicherter Kontrollpunkt |
| Inhalt der ZIP-Datei mit den Beweismitteln | `manifest.sig` signiert das kanonische Manifest, in dem die Hash-Werte der Inhaltsdateien aufgeführt sind | Das vollständige ZIP-Archiv, einschließlich Manifest und Signatur |
| Erhaltene Anhänge | SHA-256 und Byteanzahl in einem signierten „`media.saved`“-Ereignis; Datei-Hash im signierten ZIP-Manifest | Die Originaldaten innerhalb der verifizierten ZIP-Datei |
| Checkpoint | Ed25519-Signatur über die Länge des Protokolls, den Kopf-Hash, den öffentlichen Schlüssel und den Erstellungszeitpunkt | Eine unabhängige Kopie, die vor einer umstrittenen Änderung gesichert wurde |
| Ausführungsbeleg | Signed record of the collector version, source-file hashes and start settings, also included in `process.started` | The receipt, associated journal and the environment evidence for the selected verification mode |
| Lesbare Berichte: „`report.html`“ und seine Teile „`report.json`“, „`report.pdf`“, „`chat.pdf`“ | Ein Ed25519-Siegel pro Datei über deren Inhalt; das PDF trägt zudem eine Standard-PDF-Signatur (siehe [Lesbare Berichte](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#readable-reports)) | Die empfangene Datei und der Fingerabdruck des vertrauenswürdigen Schlüssels; die darin beschriebene ZIP-Datei |
| Standalone-CSV | Keine eigenständige kryptografische Signatur; Ereignis-Hashes allein reichen nicht aus | Verwenden Sie den exakten Inhalt der verifizierten ZIP-Datei zur Integritätsprüfung. |
| Screenshots, Ausdrucke oder von einem Browser erstellte PDF-Dateien | Keine TgWitness-Signatur auf dem abgeleiteten Dokument | Bewahren Sie das ursprüngliche, verifizierte Paket auf und dokumentieren Sie, wie das Derivat erstellt wurde. |

Der Collector überprüft die Journal-Signaturen, bevor jedes Exportformat generiert wird. Lesbare HTML- und PDF-Berichte tragen ihre eigenen Siegel; eigenständige CSV-Dateien werden als Teil einer signierten ZIP-Datei überprüft. Behalten Sie die ZIP-Datei bei, um die Anhangsbytes und das Manifest zu erhalten, sowie einen separaten Checkpoint, um das Journal anhand einer früheren Grenze zu überprüfen.

## Comparing chat exports

Verify and compare two signed chat-export ZIPs with independently retained signer fingerprints:

```
python -m tgwitness.verify first.zip --compare second.zip \
  --fingerprint FIRST_TRUSTED_KEY_SHA256 --compare-fingerprint SECOND_TRUSTED_KEY_SHA256
```

When both archives record the same numeric account and chat IDs, records are paired by message ID. **Unchanged** means equality of the complete saved JSON record: full text, author, dates, reply target, nested metadata and unknown fields are all included. JSON object key order does not matter; absent fields, nulls, value types and array order do. The 300-character preview is only for display. Changed entries name the differing top-level `changed_fields`, including changes invisible in that preview. Duplicate message IDs are rejected instead of overwriting one another during matching.

A difference can be a changed display name, view count, collection annotation or other observation metadata. It does not by itself establish a Telegram edit, identify who made a change, or prove which contradictory archive is accurate. Unparsed records remain in the comparison; equality of their saved representation does not mean their Telegram payload was decoded.

For different or missing account/chat identities, the tool only finds possible correspondences using sender, complete text, file hash, media type and a five-second time tolerance. It reports **Matched**, not **Unchanged**. These candidates do not establish message identity or equality of all metadata. Unparsed records remain unmatched. Differences in paired records remain listed in `changed`, including in content mode; these differences do not prove edits of the same message. With `--json`, `matched` counts pairs and `unchanged` counts pairs whose complete saved records are equal. Neither count proves message identity in content mode. The existing `changed_fields` and integer `unchanged` output remain compatible with earlier comparison results. Archive format and signature verification are unchanged.

## Übergabe von Ermittlungsergebnissen

1. Halten Sie die Fallreferenz, den Bearbeiter, die numerische Telegram-Konto-ID, die ausgewählten Quellen, die Erfassungsrichtlinie und den Erfassungszeitraum in Ihren Fallnotizen fest. TgWitness sichert Beobachtungen und unterstützt quellenverknüpfte Notizen und Erfassungen im [„Case Board](https://phishdestroy.github.io/TgWitness/de/docs/reference/case-board/)“. Bewahren Sie Übergabe- und Verwahrungsprotokolle zusammen mit Ihren Fallunterlagen auf. Überprüfen Sie die geplante Erfassungs Konfiguration im Rahmen des [Live-Abnahmeverfahrens](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
2. Speichern Sie den Fingerabdruck des öffentlichen Schlüssels des Arbeitsbereichs separat, bevor Sie sich auf dessen Exporte verlassen. Speichern Sie signierte Kontrollpunkte während der Erfassung außerhalb des Collectors. Halten Sie Unterbrechungen sowie die Grenzen der Sichtbarkeit des Kontos fest.
3. Exportieren Sie eine **signierte ZIP-Datei** und bewahren Sie die signierte Ausführungsbestätigung auf. Verwenden Sie einen Prüfpunkt an oder vor der Grenze des exportierten Protokolls. Ein späterer Prüfpunkt kann einen früheren Export zu Recht als zu kurz zurückweisen. Exporte umfassen das vollständige Arbeitsbereichsprotokoll, unabhängig von Panel-Filtern; überprüfen Sie das Material, bevor Sie es weitergeben.
4. Lassen Sie den Empfänger die ZIP-Datei mit einer vertrauenswürdigen Kopie des Verifizierers und dem unabhängig bereitgestellten Fingerabdruck/Checkpoint überprüfen. Ausgehend von einem vertrauenswürdigen Checkout mit aktiver Python-Umgebung:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   Bei erfolgreicher Ausgabe werden die Berichte „`key_pinned: true` “ und „`checkpoint_checked: true` “ generiert, sofern beide Eingaben bereitgestellt und akzeptiert wurden. Das Verifizierungsergebnis wird beibehalten.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. Halten Sie den SHA-256-Hash des Archivs, die Exportgrenze, das Übertragungsdatum, den Absender und den Empfänger in Ihrem Aufbewahrungsprotokoll fest. Bewahren Sie das Originalpaket unverändert auf und arbeiten Sie mit Kopien. Geben Sie Beweisdateien weiter, anstatt das private Datenverzeichnis der Anwendung zu übermitteln, das auch Kontositzungen und Signaturschlüssel enthält. Zur Übertragung kann ein Export in eine passwortgeschützte AES-256-ZIP-Datei gepackt werden. Das Passwort dient ausschließlich dem Schutz der Vertraulichkeit und wird nicht gespeichert; der Empfänger entpackt das Archiv und überprüft den darin enthaltenen signierten Export, der unverändert ist.
   2. Falls eine unabhängige Zeitverankerung erforderlich ist, befolgen Sie das [Verfahren gemäß RFC 3161](https://phishdestroy.github.io/TgWitness/de/docs/reference/timestamp/) und bewahren Sie die Anfrage, den Checkpoint, die Informationen zur vertrauenswürdigen Zertifizierungsstelle sowie die verifizierte Antwort der Zertifizierungsstelle auf. Die bloße Erstellung einer Anfrage führt nicht zur Erlangung eines Zeitstempels.

Eine erfolgreiche Verifizierung stellt die Integrität in Bezug auf den vertrauenswürdigen Collector-Schlüssel und die beibehaltene Grenze sicher. Siehe [Verifizierungsumfang](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope) für die Vertrauensannahmen und [Validierungsergebnisse](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/) der durchgeführten Prüfungen.

## Auszug aus der Übergabe

Eine signierte ZIP-Datei enthält das gesamte Arbeitsbereichsprotokoll. Wenn ein Gericht, ein Anwalt oder eine Meldestelle für Missbrauch nur bestimmte Chats, einen Zeitraum oder bestimmte Personen benötigt, erstellt **„Exporte → Übergabeauszug“** eine minimierte Kopie (`tgwitness-handover-v1`) gemäß den ausgewählten Offenlegungsregeln. Der Bediener gibt den Zweck an und wählt die Chats, einen optionalen Zeitraum (UTC) sowie die Personen aus, auf die sich der Auszug bezieht, und legt fest, was mit allen anderen geschieht (angezeigt, durch Pseudonyme P01, P02… oder weggelassen werden), welche Nachrichtentexte erhalten bleiben, welche Anhänge und Profilfotos enthalten sind und ob Telefonnummern und E-Mail-Adressen in Texten maskiert werden. Der Zweck und diese Regeln sind im signierten Manifest und im Bericht enthalten; das Journal protokolliert „`handover.exported`“ mit dem Zugriff, der es erstellt hat, sowie dem SHA-256-Hash der Datei, nicht den Inhalt.

„`verify.py`“ überprüft einen Auszug auf zwei Arten. Ein als unverändert angezeigter Datensatz wird vollständig verifiziert: sein Inhalt wird mit seinem Hash, seiner Ed25519-Signatur und seinem Link zu einem enthaltenen Vorgänger abgeglichen. Ein minimierter Datensatz behält den ursprünglichen Hash und die Signatur bei, sodass die Signatur weiterhin verifiziert wird, die ausgeblendeten Felder jedoch nicht daraus neu berechnet werden können; der Datensatz nennt, was ausgeblendet wurde, und der Bericht kennzeichnet dies. Das Manifest gibt die Länge des Protokolls und den Kopf mit der Signatur des Erfassers über diesem Kopf an und zählt die ausgelassenen Datensätze; „`coverage.json`“ beschreibt die ausgewählten Chats. Namen innerhalb von Dateinamen werden nicht erkannt. Überprüfen Sie die endgültigen Dateien vor der Weitergabe: Freitext, Dateinamen und ausgewählte Anhänge können weiterhin Personen identifizieren. Bewahren Sie die vollständige, signierte ZIP-Datei auf: Der Auszug stellt eine Offenlegung dar, keinen Ersatz.

## Lesbare Berichte

Signierte Beweismittel, Übergabe- und Chat-ZIP-Dateien enthalten lesbare HTML- und JSON-Berichte sowie PDF-Dateien, sofern die erforderlichen Schriftarten verfügbar sind, in der ausgewählten Berichts-Sprache. Jeder Bericht ist mit dem Ed25519-Schlüssel des Arbeitsbereichs versiegelt und kann separat überprüft werden: ` `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]``.

- `report.html` / `chat.html`: Die Seal-Anweisung (`tgwitness-report-seal-v1`) schließt die Datei und signiert das SHA-256 jedes davor liegenden Bytes. Lange Protokolle und Chats werden in Teile einer konfigurierbaren Größe aufgeteilt (Berichtseinstellungen, 500 bis 100.000 Datensätze; standardmäßig 5.000): `records/records-0001.html` oder `messages/messages-0001.html`, jeweils mit Nummer, Bereich und Gesamtsumme versiegelt und zusammen mit dem entsprechenden SHA-256 im signierten Manifest aufgeführt. Serien von Collector-Heartbeats werden als eine Zeile angezeigt, sofern sie in den Berichtseinstellungen nicht einzeln aufgeführt sind.
- `report.json` (`tgwitness-report-json-v1`, Schlüssel `format`, `report`, `seal`): Das Siegel signiert das SHA-256 des kanonischen JSON von `report`, sodass die Fakten von Fallbearbeitungssystemen und Skripten gelesen werden können und daraus eine Auswahl zum Datenschutz getroffen werden kann, während die signierte Datei intakt bleibt.
- `report.pdf` / `chat.pdf`: ein formelles Dokument zum Ausdrucken und Ablegen, das zweimal über dieselben Bytes signiert ist, wobei die gesamte Datei mit Ausnahme des Signaturwerts (`/ByteRange`) betroffen ist. Die Standard-PDF-Signatur (`adbe.pkcs7.detached`, CMS mit SHA-256 und ECDSA P-256) verwendet ein selbst ausgestelltes Dokumentensignatur- Zertifikat, das im Workspace-Tresor gespeichert ist; dessen Seriennummer ist der Schlüssel-Fingerabdruck Ed25519 . Das Ed25519-Siegel wird innerhalb des CMS als das nicht signierte Attribut `2.25.240684792623320047764573196045913242332` übertragen und benennt das Zertifikat SHA-256 mit `"content": "pdf-byte-range"`, sodass der Schlüssel Ed25519 für das Zertifikat bürgt. Ein PDF-Lesegerät zeigt an, ob sich die Datei nach der Signierung geändert hat, und stuft den Unterzeichner als unbekannt ein, bis das Zertifikat als vertrauenswürdig eingestuft ist; vergleichen Sie stattdessen den Ed25519-Fingerabdruck. Chinesische, japanische und koreanische PDF-Dateien benötigen eine Schriftart auf dem Server (oder in `TGWITNESS_FONT_DIR`); ohne diese enthält die ZIP-Datei lediglich die Berichte HTML und JSON .

In einem Kanal oder einer Supergruppe nummeriert Telegram die Nachrichten der Reihe nach mit 1, 2, 3 … Ein Chat-Export listet die erste und letzte Nummer, die Gesamtanzahl sowie jede Folge fehlender Nummern in `message-ids.json` , das Manifest und den `chat.json` -Header auf und markiert jede Lücke an der Stelle, an der sie im Transkript auftritt. `verify.py` zählt sie ab `chat.json` neu. Eine fehlende Nummer ist eine Nachricht, die Telegram nicht zurückgegeben hat (vor dem Export gelöscht oder für das Konto nicht sichtbar); in privaten Chats und einfachen Gruppen werden die Nummern von allen Chats des Kontos gemeinsam genutzt, und Lücken werden nicht gezählt.

After reading the history, the export asks Telegram for every absent number again, by number (`channels.getMessages`, up to 10,000 numbers). The result is in `message-ids.json` and the report. An empty answer records that the number is unavailable to this account at recheck time; it leaves the cause unspecified. A message returned on recheck is added to the export and marked `found_on_recheck`.

Jeder Bericht beginnt mit „**“. Kurz gesagt: „**“ – ein Absatz, dann was das Material zeigt und was es nicht zeigt (wer hinter einem Konto steht, Vollständigkeit der Übermittlung, Löschungen vor der Überwachung, Uhrzeit ohne Zeitstempel). Der seiteninterne Siegelsstempel färbt sich bernsteinfarben, wenn der Browser die Signatur des Siegels überprüft hat, nicht die Seite selbst: Ein Browser weist einer Seite keine eigenen Bytes zu. Er wird erst grün, wenn der Leser die Datei in das Prüffeld am Ende der Seite zieht und jedes Byte übereinstimmt, und nur, wenn die angezeigte Seite genau diese Datei ist; andernfalls wird er rot.

Jeder Bericht nennt das Programm genau: den Git-Commit, bei dem der Collector aus einem Checkout ausgeführt wird oder der Installer `TGWITNESS_COMMIT` festlegt, sowie die SHA-256 der Quelldateien (`source_tree_sha256`, den kanonischen JSON des Pfads → SHA-256 jeder `.py`-, `.js`-, `.css`-, `.html`- und `.svg`-Datei im Paket), die ein Checkout dieses Commits reproduziert, sofern die Dateien nicht geändert wurden. Der Client „Telegram“ wird nach seiner Bibliothek, seiner API-Schicht und seinem Rechenzentrum benannt. Zu Beginn der Beobachtung sowie zu Beginn und Ende eines Chat-Exports fragt der Collector bei „Telegram“ nach dessen Zeit („`updates.getState`“, ganze Sekunden) und zeichnet die Zeit von „Telegram“ abzüglich der Uhrzeit des Collectors auf, unter Berücksichtigung der Ungenauigkeit durch die Übertragungszeit; die Berichte zeigen diese Messungen unter „Chain of Custody“ an. Ein Chat-Export protokolliert außerdem, wann er den Verlauf gelesen hat, zusätzlich zu den Datumsangaben der Nachrichten.

### Anleitung zum Offline-Berichtsbetrachter und zum Archiv

Entpacken Sie die ZIP-Datei vollständig, bevor Sie `chat.html` oder `report.html` öffnen. Der Viewer bietet Suchfunktionen, Filter, Teilnehmer, Indikatoren, Datensatzdetails sowie die Auswahl von JSON und CSV ohne Server. Bewahren Sie `viewer/` und `media/` neben dem Bericht auf. Auswahlen sind Ableitungen: Verwenden Sie `verify.py SELECTION.json
--evidence ARCHIVE.zip`, um sie mit dem signierten Archiv zu vergleichen. Der Verifizierer prüft die Berichts-ID, den Signaturschlüssel, die Archivgrenze und jeden ausgewählten Eintrag; bearbeitete, fehlende und doppelte Einträge führen zu einem Fehler. Auswahlhinweise und Erstellungszeitpunkt bleiben unsignierte Metadaten.

Lücken bei den Nachrichtennummern werden nur bei einem vollständigen, ungefilterten, aufsteigend sortierten Chat-Feed angezeigt. Das Ausblenden einer Kategorie oder das Nichtladen eines Datenblocks darf eine ausgelassene Zeile nicht als Hinweis auf eine fehlende Nachricht interpretieren. Suchmarkierungen werden auf Klartext vor der HTML-Escape-Verarbeitung angewendet, wobei literale Markups beibehalten werden.

Der Browser überprüft Manifest-Signaturen, die Berichts-ID und den Schlüssel sowie alle aufgeführten Datei-Hashes. Er lehnt mehrdeutige oder fehlerhafte ZIP-Strukturen, doppelte Namen und unsichere Pfade ab und begrenzt Dateien auf 256 MiB sowie die angegebene Gesamtgröße des Inhalts auf 4 GiB. Verwenden Sie für größere Archive den eigenständigen Verifizierer. Diese Browserprüfung ergänzt die Prüfungen des Verifiers hinsichtlich Journalketten und Datensemantik.

`README.txt` enthält eine Einführungsanleitung, ein abgeglichenes Dateiverzeichnis, Anweisungen zur Überprüfung sowie Hinweise zum Datenformat in der Berichts-Sprache, gefolgt von einer vollständigen englischen Anleitung. `SHA256SUMS` umfasst die darin aufgeführten Dateien, mit Ausnahme der Datei selbst, von `manifest.json` und `manifest.sig`; das signierte Manifest umfasst zudem `SHA256SUMS`. Behalten Sie die ursprüngliche ZIP-Datei unverändert bei und speichern Sie Arbeitsdateien außerhalb des entpackten Ordners. PDF-Berichte enthalten Abschnitts-Lesezeichen sowie Fall-/Berichts-Identifikationen auf den folgenden Seiten.

### Der Chat zum Zeitpunkt des Exports

Ein Chat-Export erfasst, was Telegram zu Beginn des Exports über den Chat angegeben hat: Telegrams eigene Bezeichnungen (`scam`, `fake`, `restricted` mit den jeweiligen Begründungen, `verified`), Benutzernamen, Beschreibung, Anzahl der Mitglieder und Administratoren, die verknüpfte Diskussion, den Inhaltsschutz, ob neue Mitglieder frühere Nachrichten sehen können und ab welcher Nachricht dieses Konto den Verlauf einsehen kann (`available_min_id`), das Datum der ersten Nachricht, sofern es sich um die Erstellung des Chats handelt, sowie die SHA-256-ID des Chat-Fotos (gespeichert in `media/`). Es erfasst die Position des exportierenden Kontos im Chat: Rolle, Beitrittsdatum, wer es eingeladen hat und, im Falle eines Administrators, dessen Rechte. Eine von Telegram abgelehnte Anfrage wird stattdessen benannt.

Wenn das exportierende Konto ein Administrator ist, liest der Export das Administratorprotokoll des Chats (Telegram wird etwa 48 Stunden lang aufbewahrt) in `admin-log.json` ein: Löschungen und Bearbeitungen mit dem Inhalt und dem Konto, das die Aktion durchgeführt hat. Es ist der einzige Datensatz einer Löschung, der angibt, wer gelöscht hat.

### Indikatoren

Die Berichtsliste und das Archiv enthalten die Einträge `indicators.csv` , `indicators.stix.json` (STIX 2.1 ) sowie `indicators.misp.json` (Ereignis MISP ), auf deren Grundlage eine Missbrauchsstelle in den aufgezeichneten Nachrichten Maßnahmen ergreifen kann: Links und Domains (auch solche, die hinter Text, in Schaltflächen und in Link-Vorschauen verborgen sind), Kryptowährungs- Adressen, Telegram -Benutzernamen und Einladungslinks, Telefonnummern, E-Mail-Adressen und gespeicherte Bilder. Bitcoin-, Litecoin-, Dogecoin- und TRON-Adressen werden nur aufgeführt, wenn ihre Base58-Prüfsumme stimmt, SegWit-Adressen, wenn ihre Bech32- oder Bech32m-Prüfsumme stimmt, und TON-Adressen, wenn ihr CRC stimmt; EVM- und Solana-Adressen werden als nicht geprüft markiert. Bilder enthalten SHA-256 und einen perzeptuellen Hash (dHash, 64 Bit), der bei komprimierten oder in der Größe angepassten Kopien nahezu unverändert bleibt. Berichte schreiben Indikatoren so, dass sie nicht versehentlich geöffnet werden (`hxxps[://]example[.]com` ); die Dateien behalten die Werte unverändert bei. Jeder Indikator wird als unbekannt und nicht zur automatischen Erkennung gekennzeichnet (STIX , `indicator_types: unknown` , MISP , `to_ids: false` , Verteilung an die eigene Organisation): Die Auflistung bedeutet, dass eine Nachricht ihn enthielt, nicht, dass er bösartig ist. Ein Link, dessen Text eine andere Adresse anzeigt als die, die beim Öffnen angezeigt wird, wird im Bericht markiert.

Die „PDF“-Berichte enden mit einer vom Prüfer handschriftlich zu unterzeichnenden Erklärung, einer Checkliste für einen Notar oder Gerichtssachverständigen sowie einem QR-Code (ebenfalls auf der ersten Seite) mit der Berichts-ID, dem Schlüssel-Fingerabdruck und dem „SHA-256“ der maßgeblichen Daten, sodass ein Ausdruck zum entsprechenden Archiv zurückverfolgt werden kann.

## Kanonisierung von Ereignissen

Die Hash-Eingabe besteht genau aus folgenden Feldern:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

Serialisierung unter Verwendung von Python-kompatiblem JSON mit UTF-8, sortierten Objektschlüsseln, ohne ASCII- Escaping, ohne unbedeutende Leerzeichen und ohne NaN/Unendlich:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

Der SHA-256-Hash dieser Bytes wird zum Ereignis-Hash. Die Signatur erfolgt mit Ed25519 über die 32 Roh-Hash-Bytes und wird anschließend Base64-kodiert. Der erste „previous_hash“ besteht aus 64 Nullen. Die Sequenznummern beginnen bei 1 und erhöhen sich um 1. Alle Ereignisse, einschließlich operativer Ereignisse, teilen sich eine Kette. Es erfolgt keine Unterdrückung doppelter Zustellungen: Wiederholte Beobachtungen stellen separate Empfangsbestätigungen dar und sind kein Hinweis auf unterschiedliche Telegram-Aktionen.

Die Rohdaten von Telegram sind ISO-Zeichenfolgen; binäre Felder werden zu Objekten, die bytes_base64 enthalten. Nachrichtentext, Entitäten, Medienbeschreibungen, Metadaten zu Antworten, Reaktionen sowie Serviceaktionen werden in den Rohmetadaten der Nachricht beibehalten, sofern sie bereitgestellt werden.

„observed_at“ ist die UTC-Uhrzeit des Erfassers. „source_at“ ist ein von Telegram bereitgestelltes Datum, sofern verfügbar. Löschbenachrichtigungen liefern keine genaue Löschzeit, daher bleibt „source_at“ null. Die Reihenfolge des Empfangs der Daten entspricht nicht unbedingt der Reihenfolge der Quellereignisse. Historien-Snapshots verwenden ältere Quelldaten, jedoch aktuelle Beobachtungszeitpunkte.

## Semantik der Akteure

message.new actor_id ist der Absender der Nachricht. message.edited enthält keinen abgeleiteten Bearbeiter; payload.sender_id erfasst den Absender der beobachteten Nachricht. Löschung „actor_id“ bleibt null. Nachrichten des Mitgliederservices behalten den Absender und den Aktionstyp bei, ohne jede Entfernung als freiwilligen Austritt zu interpretieren. Rohe Teilnehmeraktualisierungen behalten die „actor_id“ in der bereitgestellten Form bei. Reaktions-Snapshots erfinden keinen Änderungsakteur.

Löschbenachrichtigungen für private Chats und normale Gruppen enthalten ausschließlich Nachrichten-IDs. Diese Chats nutzen eine kontoweite ID-Sequenz, sodass eine ID eine einzelne Nachricht dieses Kontos identifiziert. Wurde eine Nachricht mit dieser ID zuvor in diesem Protokoll gespeichert, wird die Löschung in diesem Chat als „message.deleted“ mit der Methode „payload.chat_resolution“ erfasst. IDs, die nie gespeichert wurden, werden als „deletion.unscoped“ ohne „chat_id“ geführt; es werden keine Vermutungen angestellt. Kanäle und Supergruppen nummerieren Nachrichten pro Chat und werden auf diese Weise niemals abgeglichen. Wenn die gelöschte Nachricht vom beobachteten Konto gesendet wurde, ist „payload.deleted_message_was_outgoing“ wahr; der Löschende wird weiterhin nicht angegeben.

An unscoped notice does not establish that a message was never saved: a matching chat may be outside the current observation scope, or a unique match may be unavailable. Recheck absence remains a separate observation from a deletion notification in report counts, filters and labels. A later recovery clears the current missing state while preserving the earlier unsuccessful check in the signed history; neither observation establishes a deletion notice.

Multiple IDs resolved to the same chat from one notification are grouped as `deletion.batch`, regardless of their count. The notification does not establish that the entire history was cleared, who performed the deletion, or whether it applied to all participants. Saved outgoing messages do not change these limits. Older journals may contain `history.cleared` events inferred from batches of ten or more IDs, with explanatory text attributing the deletion to the other participant. Those inferences are not supported by the update. Preserve those original signed records, but treat them as grouped deletion notifications; the current interface labels them accordingly.

## Erfassungsumfang: Kontinuität, Lücken und nicht erfasste IDs

Jede signierte ZIP-Datei enthält „`coverage.json`“, der HTML-Bericht beginnt mit derselben Zusammenfassung, und „ `verify.py`“ berechnet diese anhand von „`events.jsonl`“ neu, anstatt der Datei zu vertrauen:

- **Kontinuierliche Beobachtung von X bis Y.** Ein Zeitraum beginnt mit „`observation.started`“ und endet bei einer Pause, einem Stopp, einer unterbrochenen Telegram-Verbindung, einer Abmeldung, einem Prozessstart ohne ordnungsgemäßen Stopp oder nach mehr als drei Minuten ohne Aufzeichnung während der Beobachtung (Heartbeats werden jede Minute geschrieben, daher bedeutet Stille, dass der Prozess gestoppt wurde, eingefroren ist oder der Computer in den Ruhezustand übergegangen ist). Wenn das Heartbeat-Intervall in **den Parametern** geändert wird, wird dies bei jedem Heartbeat protokolliert, und die zulässige Stille beträgt drei Intervalle, jedoch niemals weniger als drei Minuten.
- **In der Lückenliste** wird der Zeitraum zwischen den einzelnen Zeitabschnitten mit dem jeweiligen Grund aufgeführt. Eine Lücke, die zum Zeitpunkt des letzten Eintrags noch offen war, wird mit „`not_resumed_by_last_record`“ gekennzeichnet.
- **Nachrichten-IDs wurden nicht erfasst.** Bei Kanälen und Supergruppen, die die Nachrichten pro Chat nummerieren, werden die zwischen den erfassten IDs fehlenden IDs als Bereiche aufgeführt. Sie werden als „*nicht erfasst“* gemeldet – gelöscht, nie zugestellt oder außerhalb des gespeicherten Verlaufs – niemals als „gelöscht“. Private Chats und normale Gruppen nutzen eine accountweite Sequenz, daher haben Lücken innerhalb eines solchen Chats keine Bedeutung und werden dort nicht aufgeführt.
- Meldungen über Lücken auf Chat-Ebene (beispielsweise wenn Telegram in einem Kanal zur Wiederherstellung von Datenunterschieden auffordert) werden als Notizen gezählt; sie unterbrechen die globale Abdeckung nicht.

### Fehlende Nachrichtennummern (`gap_summary`)

**Vorschau.** `coverage.json` → `gap_summary` misst die von Telegram zugewiesenen Nummern, die dieser Kollektor nie gesehen hat. Telegram nummeriert Nachrichten einmal pro Kanal oder Supergruppe und einmal pro Konto über private Chats, Bots und normale Gruppen hinweg. Eine Nummer zwischen zwei beobachteten Nachrichten ist entweder beobachtet oder fehlt; ein zusammenhängender Bereich ist eine positive Aussage, dass jede darin nummerierte Nachricht beobachtet wurde. Eine Lücke nennt weder einen Akteur noch einen Grund.

| Fachgebiet | Bedeutung |
| --- | --- |
| `status` | `on`oder `off` wenn in **„Parameter → Lückenanalyse“** deaktiviert |
| `parameters` | Die Parameter, die zu dem Ergebnis geführt haben, damit es reproduziert werden kann |
| `chats[]` | Ein Eintrag pro Kanal oder Supergruppe, jeweils eigenständig nummeriert |
| `account` | Die kontoweite Abfolge von privaten Chats, Bots und normalen Gruppen |
| `status` (pro Sequenz) | `applicable`, oder `not_applicable` mit `reason` |
| `observed_from`, `observed_to`, `span` | Erste und letzte beobachtete Nummer sowie die Größe des Bereichs |
| `observed`, `observed_without_content` | Beobachtete Nummern; solche, die nur aus einem Lösch- oder Nachprüfungsdatensatz bekannt sind |
| `missing`, `density`, `gap_ranges`, `largest_gap` | Nie beobachtete Zahlen, ihr Anteil am Bereich, Anzahl der Durchläufe, der längste Durchlauf |
| `clusters[]` | Aufgeführte Lücken: `low`, `high`, `missing`, sowie die benachbarten beobachteten Zahlen `after` / `before` mit ihren Beobachtungszeitpunkten |
| `service_estimate` | Nur wenn aktiviert: Wie viele fehlende Nummern wären bei ihrem beobachteten Anteil Servicemeldungen? Wird niemals abgezogen von `missing` |

Die Gültigkeit wird aus dem Protokoll abgeleitet und niemals vorausgesetzt:

- **Kanäle und Supergruppen** werden pro Chat erfasst, auch beim Export ausgewählter Chats. Die vom Absender ausgewählten Einträge bilden die Grundlage für die Erfassung `not_applicable`.
- **Die kontoweite Sequenz** wird nur von der ersten bis zur letzten Nachricht gemessen, die eingegangen ist, während die Erfassung des gesamten Kontos aktiv war, und umfasst private Chats, Bots, normale Gruppen sowie die eigenen Nachrichten des Kontos, wobei kein solcher Chat ausgeschlossen wird (`scope.changed`). Zahlen, die mit `deletion.unscoped` als beobachtet, ohne dass deren Inhalt berücksichtigt wird. Ein Export oder eine Übergabe ausgewählter Chats kann diese nicht erfassen. Wurde die Erfassung des gesamten Kontos aus- und wieder eingeschaltet, weist ein Hinweis darauf hin, dass die in der Zwischenzeit verwendeten Zahlen als Lücken erscheinen.
- Servicemeldungen sind Protokolleinträge mit eigenen Nummern, sodass sie Lücken selbst schließen; die optionale Schätzung dient lediglich als Kontext.

`verify.py` berechnet neu `gap_summary` aus `events.jsonl` mit den Parametern im signierten `coverage.json` Element (Standardwerte für ältere Archive) und gibt die kontoweite Zeile in der Abdeckungszusammenfassung aus. Das `get_capture_status`(MCP und die Befehlszeile) gibt denselben Messwert für die Chats zurück, die ein Zugriff lesen darf; die kontoweite Sequenz gilt nur für Zugriffe, die den gesamten Arbeitsbereich abdecken.

Repeated observations of one service message count once, and the account service estimate uses only numbers inside the measured range. An applied scope must explicitly preserve the account's own messages before account-wide measurement is enabled; older records without that information cannot establish this condition. Stopped observation does not extend the measured range, and resuming it is noted. The live archive query has a time budget, including its database scan, and marks an unfinished measurement as partial.

Telegram documents the [separate message ID sequences](https://core.telegram.org/api/updates#message-id-sequences). These numbers describe observations; they do not identify a deletion actor or establish why a number is absent.

Wenn Telegram das Konto nicht mehr akzeptiert, enthält der Datensatz `coverage.gap`, der die Überwachung beendet, `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended` oder `not_authorized`) sowie den Fehler Telegram; `verify.py` benennt die Ursache, aus der der Zeitraum endet.

Coverage combines recorded observation periods, interruptions and message outcomes. Assess it together with the selected chats, period and attachment policy; continuous operation alone does not establish complete delivery of Telegram updates.

## Produzent

Das signierte Manifest der Beweismittel-ZIP-Dateien, Chat-Exporte, Zeugenprotokolle und der Erklärungen zu Personenprofil-Dateien enthält „`producer` “: Software, Version, Projekt (PhishDestroy), Homepage und Quellcode-Repository. Der HTML-Bericht zeigt dieselbe Zeile an, und „`verify.py` “ gibt sie als Teil der verifizierten Informationen aus. Archive, die erstellt wurden, bevor dieses Feld existierte, werden wie bisher verifiziert und so gemeldet, dass kein Ersteller angegeben ist.

Jeder `observation.started`-Datensatz nennt außerdem den Telegram-Client, der die Beobachtung durchgeführt hat: dessen `api_id` (niemals den Hash), unabhängig davon, ob es sich um ein integriertes öffentliches Schlüsselpaar oder die eigene Anwendung des Betreibers handelt, die in der Verbindungsanfrage von Telegram gesendete Client-Beschreibung sowie die Art der Verbindungsroute mit dem IP-Modus (keine Proxy-Adresse oder Geheimnis). Der Bericht und `custody.json` listen jeden einzelnen Client und jede Route mit dem Zeitpunkt ihrer Aufzeichnung auf sowie die Zeitpunkte, zu denen kein gelisteter Proxy geantwortet hat und Telegram die Adresse des Servers erkannt hat. Dies geht aus zuvor aufgezeichneten Protokollen hervor.

## Personenprofile

Eine Profildatei (`tgwitness-dossier-v1`, JSON) wird auf Anfrage aus den bereits im Protokoll vorhandenen Einträgen für einen Chat erstellt; es werden keine Daten von Telegram abgerufen, und Profilinhalt werden niemals in das Protokoll geschrieben (das Aktivieren und Deaktivieren von Profilen wird als `dossier.changed` protokolliert). Für jede Person mit einer gespeicherten Nachricht werden Name und Benutzernamenverlauf sowie Telegram-Kennzeichnungen (Bot, Betrug, Fälschung, Premium, verifiziert, eingeschränkt, gelöscht) – wie zum Zeitpunkt der Speicherung sichtbar – sowie Profil- Foto-IDs, SHA-256- und Perceptual-Hash (pHash, kompatibel mit `imagehash.phash`) des Avatars aus dem lokalen Avatar-Cache mit ähnlichen Avataren, Aktivitäten (erste und letzte Nachricht, Anzahlen, bearbeitete und gelöschte Freigaben, Nachrichten nach UTC-Stunde), wer wem antwortet, andere Chats in diesem Journal, in denen die Person geschrieben hat, sowie erwähnte Wallets (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL; Base58Check-Adressen werden anhand der Prüfsumme validiert), Telefonnummern, Benutzernamen und Links, einschließlich hinter Text versteckter Links.

Jeder Sachverhalt listet die Protokoll-Einträge (`seq`) auf, aus denen er stammt, und `record_hashes` enthält den Hashwert jedes referenzierten Eintrags. Die Aussage ist mit dem Workspace-Schlüssel signiert:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

Überprüft die Signatur, verifiziert den Beweisexport selbst (Signatur, Hash-Kette und Dateien) sowie die Tatsache, dass jeder referenzierte Datensatz unverändert in diesem Export desselben Arbeitsbereichs vorhanden ist. Avatar-Hashes werden als aus dem lokalen Cache stammend gekennzeichnet (keine Protokoll-Datensätze). Erwähnungen sind Musterübereinstimmungen – Anhaltspunkte zur Überprüfung, keine verifizierten Fakten. Profile werden pro Chat aktiviert, können als passwortgeschützte AES-256-ZIP-Datei exportiert werden und werden gelöscht, wenn sie deaktiviert werden oder wenn der Chat aus den Quellen entfernt wird.

## Unabhängiger Zeuge

Ein Zeugenprotokoll (`tgwitness-witness-v1`) und dessen Kanalbeiträge werden anhand eines Beweisexports mit `verify.py --witness … --channel …` überprüft; siehe [unabhängiger Zeuge](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/).

## Manifest und Kontrollpunkte

Die Datei „manifest.json“ enthält das Format, den Exportzeitpunkt, den öffentlichen Schlüssel, den Fingerabdruck, die Länge des Protokolls, den Head-Hash, den Geltungsbereich, den Ersteller, Einschränkungen sowie den SHA-256-Hash jedes Inhaltselements mit Ausnahme von „`manifest.json`“ und „`manifest.sig`“ selbst. „manifest.sig“ ist die Base64-Signatur nach Ed25519 über das kanonische Manifest-JSON. Der Verifizierer lehnt unerwartete/fehlende Elemente, doppelte Namen, beschädigte Dateien, unterbrochene Sequenzen/Ketten, ungültige Signaturen sowie Abweichungen von einem bereitgestellten Checkpoint ab. Er extrahiert niemals Archivpfade. Er begrenzt die insgesamt angegebene unkomprimierte Größe auf 4 GiB; mit `--max-gib N` sind größere Archive möglich, die mit einem erhöhten **Parameterlimit** erstellt wurden.

Run verification from your installed TgWitness version or a reviewed checkout. The copy included in an archive supports portable use; check that copy against your trusted installation before executing it.

A checkpoint signs a statement containing the public key, journal length, head hash, and creation time. The verifier can check that a later archive contains the same prefix. Retain the checkpoint outside the collector, so later verification compares the archive with a reference held separately from it.

## Umfang der Überprüfung

Verification checks the archive and the collection mode used to produce it. Choose the mode whose trust boundary matches the case, then retain its verification inputs.

| Erfassungsmodus | Was der Verifizierer überprüft | Verifizierungsdaten und Vertrauensgrenze |
| --- | --- | --- |
| Lokaler Arbeitsbereich | Record signatures, hash chain, manifest and attachment bytes | Independently retained collector fingerprint; the host administrator controls the local signing key |
| Lokaler Arbeitsbereich mit einem unabhängigen Witness | Die Archivprüfungen sowie die Übereinstimmung mit einem früheren Protokollpräfix, das vom Zeugen beibehalten wurde | Separately trusted witness key and records; the checkpoint binds the prefix already observed |
| [GitHub Actions-Aufzeichnung](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) | GitHub attestation of the archive digest, approved workflow and collector commits, hosted runner, fresh session/key origin and internal archive integrity | Trusted verifier policy, caller repository and GitHub attestation bundle; collection runs under the pinned workflow |
| [Cloud-Bereitstellung](https://phishdestroy.github.io/TgWitness/de/docs/reference/high-assurance/) | Provider lifecycle and access records, firewall and Cloudflare state, plus the collector's signed run record | Read-only queries to the provider and Cloudflare; availability of individual checks depends on the provider |
| [Vertrauliche Intel TDX-VM](https://phishdestroy.github.io/TgWitness/de/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx) | Quote signature and platform status, binding to the collector statement, compose and OS measurements | Intel trust chain and expected deployment measurements; retain the results of every required TDX check |

In sealed acquisition, the approved collector receives data through an authenticated Telegram connection inside the verified environment. Attestation binds the archive to that execution, so verification covers acquisition as well as later file integrity. This relies on the approved code and the platform trust chain listed above. GitHub capture verification requires a session created inside the run and rejects imported-session captures.

The run receipt records the collector version, file hashes and startup settings. GitHub provenance and TDX measurements provide the environment checks; the [validation record](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/) identifies tested configurations.

TgWitness signs the observations it collects; Telegram and message authors do not issue these signatures. In a local workspace, material created before the first independent checkpoint still depends on the collector and its key holder. Coverage records describe the selected scope and collection outcomes, while verified external timestamps anchor the committed archive or journal boundary in time.

## Anhänge

Dateien werden unter „media/“ anhand ihres SHA-256-Hashs adressiert. Ein „media.saved“-Ereignis verknüpft einen Hash und die Byte-Länge mit einem bestimmten Nachrichtenereignis. Die ursprünglichen Dateinamen dienen als Metadaten, niemals lokale Pfade. Mediendaten werden asynchron heruntergeladen, sodass eine sofortige Löschung die Erfassung verhindern kann. Deaktivierte Erfassung, übergroße Dateien oder Dateien mit unbekannter Größe, Download-Fehler sowie unterbrochene Downloads werden als Ergebnisse angezeigt. Ein Prozessabsturz kann nicht referenzierte Teil-Dateien hinterlassen; diese werden nicht in die Exporte einbezogen.

Der ZIP-Exporter gleicht gespeicherte Medien anhand ihrer Namen ab. JSONL-, CSV- und HTML-Exporte überprüfen Ereignissignaturen, enthalten jedoch keine Medienbytes. Abgeleitete Berichte dienen der Benutzerfreundlichkeit; „events.jsonl“ ist die maßgebliche Darstellung der Ereignisse.

Bei einem vollständigen Chat-Export werden Anhänge gemäß den Anhangseinstellungen des Arbeitsbereichs im Ordner „media/“ gespeichert und mit dem Namen „SHA-256“ versehen. Jeder Nachrichteneintrag in chat.json benennt seine Datei (`file`, `file_sha256`) oder den Grund für deren Fehlen (`file_status`), zusammen mit dem, was der Leser um den Text herum gesehen hat: Links hinter dem Text, Weiterleitungsquelle, Bot-Schaltflächen, Signatur, Aufrufe und den Timer für die automatische Löschung. `verify.py` überprüft, ob sich jede benannte Datei im signierten Manifest unter diesem Hash befindet.

## Dauerhafte Erfassung und Verarbeitung von Belegen (0,2)

Ein Medienauftrag und die damit verbundene Nachrichtenereignis-Festschreibung erfolgen in einer Transaktion. Der Auftrag speichert den ursprünglichen TL-Nachrichtenbeschreiber; die signierte Beobachtung bindet deren SHA-256-Hash, das Konto sowie die Größenrichtlinie. Die Wiederherstellung überprüft diese Bindung vor dem Herunterladen. Es wird niemals die aktuelle Nachricht abgerufen, und ein neuerer Anhang wird stillschweigend ersetzt. Unterbrochene Aufträge werden erneut versucht, während ein dauerhafter Fehler ein explizites Ergebnis bleibt.

Each workspace has its own journal and signing identity. A process.started event includes a run ID, local clocks, dependency versions, source-file hashes, initial account/scope, and capture settings. Heartbeats include the run ID, monotonic time, and queue state. The run receipt can also be downloaded as a separately signed statement. For verification of the execution environment, pair it with the GitHub attestation or TDX checks described in [Verification scope](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope).

Automatic checkpoints are retained locally on startup, every five minutes while observing (**Parameters → Signed checkpoint every**), and on orderly stop. Startup verification and export compare the journal against the latest retained local checkpoint. This can detect a database rollback when the checkpoint survives. Independent retention keeps that reference available outside the workspace; a verified external timestamp additionally anchors it in time.

Nach einem Neustart wird die gespeicherte Telegram-Aktualisierungsposition fortgesetzt (`catch_up_from` in `observation.started`) und es werden versäumte Aktualisierungen angefordert. Eine regelmäßige Überprüfung erfasst `message.recovered` für versäumte Nachrichten und `message.missing_on_recheck`, wenn Telegram keine gespeicherte Nachricht mehr zurückgibt; Letzteres ist keine Löschmeldung und nennt weder einen Löschenden noch einen Zeitpunkt.

### Externe Sicherung und Wiederherstellung (S3)

Die externe Kopie (Exporte, standardmäßig deaktiviert) lädt Protokollsegmente, gesicherte Dateien, Checkpoints mit ihren Zeitstempeln sowie fertige Chat-Exporte in einen S3-kompatiblen Speicher hoch, verschlüsselt mit AES-256-GCM verschlüsselt, wobei der Schlüssel im Workspace-Tresor gespeichert ist; die Aufbewahrung mittels „Object Lock“ gilt, sofern der Bucket dies unterstützt. Ohne den heruntergeladenen Schlüssel kann die Kopie nicht gelesen werden. Wiederherstellung und Überprüfung mit „`python -m tgwitness.replica restore --key-file KEY.json --out DIR`“.

Die Wiederherstellung erfordert ein leeres Standardverzeichnis. Downloads und entschlüsselte Objekte verbleiben im privaten Zwischenspeicher, bis das gesamte Protokoll und jeder aufbewahrte Prüfpunkt verifiziert sind. Unsichere Objektpfade, inkonsistente Segmentbereiche und Protokolle, die kürzer als ein Prüfpunkt sind, werden abgelehnt; bei fehlgeschlagener Verifizierung werden keine wiederhergestellten Dateien veröffentlicht. Bei Aufbewahrungsprüfungen werden der zurückgegebene „Object Lock“-Modus und das Datum mit der beim Upload übermittelten Frist verglichen (mit einer Rundungstoleranz von einer Sekunde). Eine abgelaufene, ungültige oder verkürzte Frist gilt nicht als verifiziert. Der Status gibt das Stichprobenobjekt an, dessen Aufbewahrungsstatus für diesen Upload-Durchlauf zurückgelesen wurde.

Fehlende oder beschädigte lokale Medien werden als Fehler des Durchlaufs gemeldet, und der Mediencursor bleibt vor diesem stehen, sodass die Datei im nächsten Durchlauf erneut versucht wird; die darauf folgenden Dateien, Checkpoints und Exporte werden weiterhin kopiert. Die Wiederherstellungsprüfung vergleicht alle Verweise auf erhaltene Medien mit entschlüsselten Hashes und aufgezeichneten Größen. Identische, sich überschneidende Protokollsegmente aus unterbrochenen Uploads werden dedupliziert; widersprüchliche Überschneidungen werden verworfen. Während eines Uploads erstellte Kontrollpunkte werden zurückgestellt, bis die von ihnen abgedeckten Protokolleinträge kopiert wurden, sodass ein abgeschlossener Durchlauf keinen Kontrollpunkt vor seinem Protokoll veröffentlicht.

### Streaming-Export-Momentaufnahmen

Streaming-Exporte verwenden einen stabilen SQLite-Lese-Snapshot. Dessen Anfang kann älter sein als das aktuelle Live-Protokoll, wenn der Download abgeschlossen ist. Ein nach diesem Snapshot erstellter Checkpoint kann korrekt melden, dass das Archiv kürzer ist; vergleichen Sie dies mit einem Checkpoint am oder vor dem exportierten Präfix, nicht mit einem beliebigen späteren Checkpoint.

## Vorbereitung gemäß RFC 3161 und Überprüfung der Antworten (0.2)

Im Beweismodus (standardmäßig deaktiviert) wird lediglich der SHA-256-Hash jedes signierten Checkpoints an die aufgeführten RFC-3161-Autoritäten und OpenTimestamps-Kalender gesendet – und zwar über die Workspace-Route und niemals über MTProxy. Die Antworten werden in `checkpoints/anchors/` gespeichert, exportiert und von `verify.py` überprüft (`--tsa-ca` überprüft die TSA-Signatur; Bestätigen Sie die OpenTimestamps-Nachweise mit `ots upgrade` und `ots verify`).

Das Panel erstellt ein Anforderungsarchiv, das kanonische „checkpoint.json“-Bytes, einen SHA-256-Nachrichtenabdruck und einen zufälligen Nonce in „timestamp.tsq“, Prüfsummen sowie Anweisungen enthält. Es wird keine Netzwerkanfrage gestellt. Die Vorbereitung stellt keinen vertrauenswürdigen Zeitstempel dar.

`python -m tgwitness.anchor verify` ruft OpenSSL zweimal auf: einmal anhand der Checkpoint- Bytes und einmal anhand der ursprünglichen Anfrage. Eine vertrauenswürdige CA-Datei ist ausdrücklich erforderlich; enthaltene Zertifikate werden nicht automatisch als vertrauenswürdig eingestuft. Die Überprüfung der Anfrage ist in der Befehlszeile optional; verwenden Sie daher weiterhin den Parameter „--request“, um den Nonce zu überprüfen. Das Ergebnis gibt an, ob die Überprüfung stattgefunden hat. Die Checkpoint-Signatur des Collectors und das Protokoll müssen weiterhin separat anhand des vertrauenswürdigen Fingerabdrucks des Collectors verifiziert werden.

Bei der Verifizierung werden die Antwort-Signatur, die Checkpoint-Bytes und, sofern vorhanden, die ursprüngliche Anfrage unter der angegebenen CA-Vertrauensstellung überprüft. Revokationsprüfungen und die Validierung der Langzeitarchivierung nach Ablauf des Zertifikats liegen außerhalb des aktuellen Verifizierers. Siehe die [Vorgehensweise](https://phishdestroy.github.io/TgWitness/de/docs/reference/timestamp/) und [die Validierungsergebnisse](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/).

## Optionale Datensätze im Beweismodus: „drand“- und „Telegram“-Geräte

Zwei weitere Aufzeichnungen können mit denselben Durchläufen wie die Zeitstempel ausgeführt werden. Beide sind standardmäßig deaktiviert und werden nur wirksam, wenn der Beweismodus aktiviert ist: Extras → Beweise & Backups → **Weitere Zeugen · optional**, oder `"drand": true` und `"devices": true` in `POST /api/evidence`. Ein Ausfall stoppt weder den anderen noch die Zeitstempel; das Bedienfeld zeigt das aktuellste Ergebnis jedes einzelnen unter dem Formular an.

**drand** (`beacon.drand` ). Bei jedem Durchlauf wird die neueste Runde von drand quicknet, die öffentliche Zufallszahl der League of Entropy (eine Runde alle 3 Sekunden), in das Journal geschrieben: `chain` , `round` , `randomness` , `signature` , `round_time` und das `relay` , das geantwortet hat. Eine verifizierte unvorhersehbare Runde liefert eine untere Zeitreferenz für das nachfolgende, per Hash verknüpfte Material. Ein verifizierter Zeitstempel an einem späteren Checkpoint liefert einen oberen Zeitbezug. Diese Prüfungen begrenzen das verknüpfte Material; die Erfassungsreichweite wird separat bewertet. Der Collector fragt zuerst `drand.cloudflare.com` ab, dann die Relays von Protocol Labs über die Workspace-Route, mit einer Anfrage pro Durchlauf.

`verify.py` prüft, ob jede Zufallszahl das SHA-256 ihrer Signatur ist und ob die Rundenzeit stimmt, und meldet die Runden, die längste Zeitspanne ohne eine Runde sowie den Rückstand der Uhr des Collectors gegenüber drand. Die BLS-Signatur wird nicht überprüft. `--check-drand` vergleicht die Runden mit einem Cloudflare-Relay und einem Protocol Labs-Relay, entweder mit allen oder mit einer zufälligen Stichprobe von 100 aus einem langen Protokoll; eine Runde, die abweicht, führt zum Fehlschlagen der Überprüfung.

**, Telegram,** (`account.devices`). Bei jedem Durchlauf werden die Sitzungen des Kontos mit `account.getAuthorizations` gelesen, die Liste Telegram wird unter „Einstellungen“ → „Geräte“ angezeigt und vollständig aufgezeichnet: vollständig, wenn sie sich seit dem letzten Durchlauf geändert hat, mit den Sitzungs-Hashes `added` und `removed`; ansonsten nur deren Anzahl und SHA-256. Gerätemodell, Plattform, App und Version, Erstellungsdatum und letzte Aktivität, Land und Region werden gespeichert; IP-Adressen hingegen nicht, da der Export von Beweismaterial außerhalb Ihrer Kontrolle liegt. Die eigene Sitzung des Collectors ist ständig aktiv, daher zählt nur die Aktivität anderer Sitzungen als Änderung. „`verify.py`“ meldet, wie oft die Liste aufgezeichnet wurde sowie jede neue und beendete Sitzung. Die Liste wird nur gelesen, solange die Beobachtung läuft.

Was sie nicht zeigen: drand beweist lediglich die Reihenfolge der Datensätze im Verhältnis zur öffentlichen Zeit, und die Geräteliste ist die Aussage von „Telegram“ über den Collector, die – wie jeder andere Datensatz auch – vom Collector signiert wurde.

**Cloudflare Gateway-Protokoll** (`cloudflare.gateway_dns`). Für einen Server, der über das Cloudflare-Gateway ([Gateway-DNS](https://phishdestroy.github.io/TgWitness/de/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)) auflöst, kopiert jeder Durchlauf die seit der letzten Kopie vom Gateway protokollierten Daten: ein Eintrag pro Zeitfenster von maximal drei Stunden mit `from`, `until`, `location_id`, dem `address` des Servers, sofern festgelegt, und dem `queries` als `[at, name, type, rcode, decision, colo]`, auch wenn keine vorhanden waren. Richten Sie dies unter „ **Cloudflare Gateway-Protokoll“ ein:**: Konto, Standort, optionale Adresse und ein schreibgeschütztes Token (Konto Analytics-Lesezugriff; Zero Trust PII-Lesezugriff, um eine Adresse eines gemeinsam genutzten Standorts zu speichern). Das Panel überprüft diese Angaben mit einer Anfrage vor dem Speichern; das Token bleibt verschlüsselt und gelangt niemals in das Protokoll. `verify.py` listet die Fenster, die am häufigsten aufgerufenen Namen und alle Zeiträume auf, für die keine Kopie vorliegt; ein Datensatz, dessen Anzahl nicht mit seinen Abfragen übereinstimmt, schlägt fehl. Ein Fenster, das mehr als eine Seite mit Abfragen in einer einzigen Sekunde enthält, behält diese Seite bei und gibt an, dass der Rest fehlt. Die Kopie ist die Antwort von Cloudflare über den Collector, signiert vom Collector; innerhalb von 24 Stunden kann jeder mit einem schreibgeschützten Token diese mit Cloudflare abgleichen.
