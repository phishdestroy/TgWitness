# Format der Beweismittel

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/

Inhalt der signierten ZIP-Datei, Protokolltypen, Prozessbestätigungen, Benutzerprofile, externe Kopien und Offline-Überprüfung.

Eine Beobachtung ist keine Schlussfolgerung. Eine Absender-ID ist keine Identität in der realen Welt. Die im Konto sichtbare Dienstaktualisierung ist die Quelle; Telegram signiert diese gespeicherten Datensätze nicht kryptografisch für einen externen Ermittler.

## Was ist signiert?

| Material | Schutz | Was ist zu beachten? |
| --- | --- | --- |
| Jeder Eintrag im Protokoll, einschließlich operativer Ereignisse | SHA-256-Kette und eine Ed25519-Signatur pro Ereignis | Original-`events.jsonl`, der Fingerabdruck des vertrauenswürdigen Schlüssels, sowie ein gespeicherter Kontrollpunkt |
| Inhalt der ZIP-Datei mit den Beweismitteln | `manifest.sig` signiert das kanonische Manifest, in dem die Hash-Werte der Inhaltsdateien aufgeführt sind | Das vollständige ZIP-Archiv, einschließlich Manifest und Signatur |
| Erhaltene Anhänge | SHA-256 und Byteanzahl in einem signierten „`media.saved`“-Ereignis; Datei-Hash im signierten ZIP-Manifest | Die Originaldaten innerhalb der verifizierten ZIP-Datei |
| Checkpoint | Ed25519-Signatur über die Länge des Protokolls, den Kopf-Hash, den öffentlichen Schlüssel und den Erstellungszeitpunkt | Eine unabhängige Kopie, die vor einer umstrittenen Änderung gesichert wurde |
| Ausführungsbeleg | Separat signierte Erfassungsdaten; ebenfalls enthalten in einem signierten „`process.started`“-Ereignis | Der Beleg und das zugehörige Protokoll; die Messwerte stammen aus Selbstauskünften |
| Einzelne CSV- oder HTML-Datei | Keine eigenständige kryptografische Signatur; Ereignis-Hashes allein reichen nicht aus | Verwenden Sie den exakten Inhalt der verifizierten ZIP-Datei zur Integritätsprüfung. |
| Screenshots, Ausdrucke oder von einem Browser erstellte PDF-Dateien | Keine TgWitness-Signatur auf dem abgeleiteten Dokument | Bewahren Sie das ursprüngliche, verifizierte Paket auf und dokumentieren Sie, wie das Derivat erstellt wurde. |

Der Collector überprüft die Signaturen des Protokolls, bevor er jedes Exportformat generiert. Diese Quellenprüfung erzeugt keine Signatur für eine separat heruntergeladene CSV- oder HTML-Datei. Eine gültige JSONL-Ereignissignatur liefert ebenfalls keine Informationen zu den Anhangsbytes und belegt auch nicht eigenständig, dass das gesamte beobachtete Protokoll bereitgestellt wurde.

## Übergabe von Ermittlungsergebnissen

1. Halten Sie die Fallreferenz, den Bearbeiter, die numerische Telegram-Konto-ID, die ausgewählten Quellen, die Erfassungsrichtlinie und den Erfassungszeitraum in Ihren Fallnotizen fest. TgWitness speichert die Beobachtungen; die Fallzuweisung und die Aufbewahrungsunterlagen werden außerhalb der Anwendung verwaltet. Überprüfen Sie die beabsichtigte Erfassungskonfiguration anhand des [Live-Abnahmeverfahrens](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
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

Eine erfolgreiche Verifizierung bestätigt die Integrität in Bezug auf den vertrauenswürdigen Erfassungsschlüssel und die festgelegte Grenze. Die Quelle der Wahrheit, die vollständige Telegram-Übermittlung, die vertrauenswürdige Zeitangabe sowie die rechtliche Zulässigkeit erfordern separate Nachweise. Diese Version hat weder die Live-Qualifizierung für Telegram noch eine unabhängige forensische/sicherheitstechnische Bewertung durchlaufen.

Ein kopierter Sammler-Schlüssel kann ein gefälschtes Ersatzprotokoll signieren. Die Überprüfung anhand eines unabhängig aufbewahrten Kontrollpunkts oder einer Zeugenaufzeichnung erkennt ein geändertes früheres Präfix; die Signaturüberprüfung allein kann dies nicht. Ein Zeuge bestätigt die vom Sammler vorgelegten Daten; er belegt jedoch nicht eigenständig die Richtigkeit von Aufzeichnungen, die vor ihrem ersten externen Kontrollpunkt gefälscht wurden. Berichte zur Cloud-Bereitstellung überprüfen die Konfiguration und die vom Sammler gemeldeten Messwerte; sie belegen nicht, dass ein privater Schlüssel während des Bootstrap-Vorgangs niemals kopiert wurde.

Über Apprise versendete Benachrichtigungen enthalten Arbeitsbereichs- und Chatnamen sowie Anzahlangaben; kurze Auszüge aus gelöschten und bearbeiteten Nachrichten werden nur hinzugefügt, wenn der Betreiber diese Funktion aktiviert (standardmäßig deaktiviert). Sie dienen lediglich als Hinweis und stellen keine Beweismittel dar: Die Zustellung ist nicht garantiert, und nur das Protokoll sowie dessen signierte Exporte dokumentieren, was beobachtet wurde. Bei Verwendung eines Arbeitsbereichs-Proxys verfolgen Benachrichtigungen denselben Weg; Dienste, die diesen nicht nutzen können, sowie MTProxy-Routen werden abgelehnt.

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

## Erfassungsumfang: Kontinuität, Lücken und nicht erfasste IDs

Jede signierte ZIP-Datei enthält „`coverage.json`“, der HTML-Bericht beginnt mit derselben Zusammenfassung, und „ `verify.py`“ berechnet diese anhand von „`events.jsonl`“ neu, anstatt der Datei zu vertrauen:

- **Kontinuierliche Beobachtung von X bis Y.** Ein Zeitraum beginnt mit „`observation.started`“ und endet bei einer Pause, einem Stopp, einer unterbrochenen Telegram-Verbindung, einer Abmeldung, einem Prozessstart ohne ordnungsgemäßen Stopp oder nach mehr als drei Minuten ohne Aufzeichnung während der Beobachtung (Heartbeats werden jede Minute geschrieben, daher bedeutet Stille, dass der Prozess gestoppt wurde, eingefroren ist oder der Computer in den Ruhezustand übergegangen ist). Wenn das Heartbeat-Intervall in **den Parametern** geändert wird, wird dies bei jedem Heartbeat protokolliert, und die zulässige Stille beträgt drei Intervalle, jedoch niemals weniger als drei Minuten.
- **In der Lückenliste** wird der Zeitraum zwischen den einzelnen Zeitabschnitten mit dem jeweiligen Grund aufgeführt. Eine Lücke, die zum Zeitpunkt des letzten Eintrags noch offen war, wird mit „`not_resumed_by_last_record`“ gekennzeichnet.
- **Nachrichten-IDs wurden nicht erfasst.** Bei Kanälen und Supergruppen, die die Nachrichten pro Chat nummerieren, werden die zwischen den erfassten IDs fehlenden Nummern als Bereiche aufgeführt. Sie werden als „nicht*erfasst“* gemeldet – gelöscht, nie zugestellt oder außerhalb des gespeicherten Verlaufs –, niemals als „gelöscht“. Private Chats und normale Gruppen nutzen eine accountweite Sequenz; daher haben Lücken dort keine Bedeutung und werden nicht aufgeführt.
- Meldungen über Lücken auf Chat-Ebene (beispielsweise wenn Telegram in einem Kanal zur Wiederherstellung von Datenunterschieden auffordert) werden als Notizen gezählt; sie unterbrechen die globale Abdeckung nicht.

Der Erfassungsumfang beschreibt, was dieser Datensammler aufgezeichnet hat. Er stellt keinen Beweis dafür dar, dass Telegram jede Aktualisierung während eines ununterbrochenen Zeitraums zugestellt hat.

## Produzent

Das signierte Manifest der Beweismittel-ZIP-Dateien, Chat-Exporte, Zeugenprotokolle und der Erklärungen zu Personenprofil-Dateien enthält „`producer` “: Software, Version, Projekt (PhishDestroy), Homepage und Quellcode-Repository. Der HTML-Bericht zeigt dieselbe Zeile an, und „`verify.py` “ gibt sie als Teil der verifizierten Informationen aus. Archive, die erstellt wurden, bevor dieses Feld existierte, werden wie bisher verifiziert und so gemeldet, dass kein Ersteller angegeben ist.

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

Beziehen Sie den Verifizierungscode aus einer vertrauenswürdigen Checkout-Version oder einer geprüften unabhängigen Kopie. Ein Verifizierer innerhalb eines nicht vertrauenswürdigen Archivs ist ausführbares Material, das vom Autor dieses Archivs bereitgestellt wird; sein Vorhandensein dient der Portabilität und stellt keinen unabhängigen Vertrauensanker dar.

Ein Checkpoint signiert eine Erklärung, die den öffentlichen Schlüssel, die Protokollänge, den Head-Hash und den Erstellungszeitpunkt enthält. Der Prüfer kann überprüfen, ob ein späteres Archiv dasselbe Präfix enthält. Bewahren Sie einen Checkpoint außerhalb des Collectors vor einer umstrittenen Änderung auf: Ein Angreifer, der sowohl das Archiv als auch den Checkpoint kontrolliert, kann beide ersetzen.

Eine gültige Signatur eines nicht gesicherten Schlüssels gewährleistet lediglich die interne Konsistenz. Selbst ein gesicherter Schlüssel kann die Echtheit des Quellinhalts nicht nachweisen, wenn der Erfasser oder der Schlüssel vor der Aufzeichnung kompromittiert wurde. Externe Zeitstempelung und vertrauenswürdige Erfassung sind separate Anforderungen. TgWitness verspricht keine Zulässigkeit als Beweismittel oder forensische Zertifizierung.

## Anhänge

Dateien werden unter „media/“ anhand ihres SHA-256-Hashs adressiert. Ein „media.saved“-Ereignis verknüpft einen Hash und die Byte-Länge mit einem bestimmten Nachrichtenereignis. Die ursprünglichen Dateinamen dienen als Metadaten, niemals lokale Pfade. Mediendaten werden asynchron heruntergeladen, sodass eine sofortige Löschung die Erfassung verhindern kann. Deaktivierte Erfassung, übergroße Dateien oder Dateien mit unbekannter Größe, Download-Fehler sowie unterbrochene Downloads werden als Ergebnisse angezeigt. Ein Prozessabsturz kann nicht referenzierte Teil-Dateien hinterlassen; diese werden nicht in die Exporte einbezogen.

Der ZIP-Exporter gleicht gespeicherte Medien anhand ihrer Namen ab. JSONL-, CSV- und HTML-Exporte überprüfen Ereignissignaturen, enthalten jedoch keine Medienbytes. Abgeleitete Berichte dienen der Benutzerfreundlichkeit; „events.jsonl“ ist die maßgebliche Darstellung der Ereignisse.

## Dauerhafte Erfassung und Verarbeitung von Belegen (0,2)

Ein Medienauftrag und die damit verbundene Nachrichtenereignis-Festschreibung erfolgen in einer Transaktion. Der Auftrag speichert den ursprünglichen TL-Nachrichtenbeschreiber; die signierte Beobachtung bindet deren SHA-256-Hash, das Konto sowie die Größenrichtlinie. Die Wiederherstellung überprüft diese Bindung vor dem Herunterladen. Es wird niemals die aktuelle Nachricht abgerufen, und ein neuerer Anhang wird stillschweigend ersetzt. Unterbrochene Aufträge werden erneut versucht, während ein dauerhafter Fehler ein explizites Ergebnis bleibt.

Jeder Arbeitsbereich verfügt über ein eigenes Protokoll und eine eigene Signaturidentität. Ein „process.started“-Ereignis enthält eine Lauf-ID, lokale Uhrzeiten, Versionen der Abhängigkeiten, Hashes der Quelldateien, das anfängliche Konto/den anfänglichen Umfang sowie die Erfassungseinstellungen. Heartbeats enthalten die Lauf-ID, die monotone Zeit und den Status der Warteschlange. Der Prozessbeleg kann zudem als separat signierte Erklärung heruntergeladen werden. Dateimessungen basieren auf Selbstauskünften und stellen keine vertrauenswürdige Hardware-Bescheinigung dar.

Automatische Checkpoints werden lokal beim Start, alle fünf Minuten während der Überwachung (**Parameter → „Signierter Checkpoint alle**“) sowie beim ordnungsgemäßen Beenden gespeichert. Bei der Überprüfung beim Start und beim Export wird das Protokoll mit dem zuletzt gespeicherten lokalen Kontrollpunkt abgeglichen. Auf diese Weise lässt sich ein Datenbank-Rollback erkennen, sofern der Kontrollpunkt erhalten bleibt; ein Betreiber, der beide kontrolliert, kann jedoch weiterhin beide ersetzen. Unabhängige Aufbewahrung und externe vertrauenswürdige Zeitstempel bleiben separate Anforderungen.

Nach einem Neustart wird die gespeicherte Telegram-Aktualisierungsposition fortgesetzt (`catch_up_from` in `observation.started`) und es werden versäumte Aktualisierungen angefordert. Eine regelmäßige Überprüfung erfasst `message.recovered` für versäumte Nachrichten und `message.missing_on_recheck`, wenn Telegram keine gespeicherte Nachricht mehr zurückgibt; Letzteres ist keine Löschmeldung und nennt weder einen Löschenden noch einen Zeitpunkt.

### Externe Sicherung und Wiederherstellung (S3)

Die externe Kopie (Exporte, standardmäßig deaktiviert) lädt Protokollsegmente, gesicherte Dateien, Checkpoints mit ihren Zeitstempeln sowie fertige Chat-Exporte in einen S3-kompatiblen Speicher hoch, verschlüsselt mit AES-256-GCM verschlüsselt, wobei der Schlüssel im Workspace-Tresor gespeichert ist; die Aufbewahrung mittels „Object Lock“ gilt, sofern der Bucket dies unterstützt. Ohne den heruntergeladenen Schlüssel kann die Kopie nicht gelesen werden. Wiederherstellung und Überprüfung mit „`python -m tgwitness.replica restore --key-file KEY.json --out DIR`“.

Die Wiederherstellung erfordert ein leeres Standardverzeichnis. Downloads und entschlüsselte Objekte verbleiben im privaten Zwischenspeicher, bis das gesamte Protokoll und jeder aufbewahrte Prüfpunkt verifiziert sind. Unsichere Objektpfade, inkonsistente Segmentbereiche und Protokolle, die kürzer als ein Prüfpunkt sind, werden abgelehnt; bei fehlgeschlagener Verifizierung werden keine wiederhergestellten Dateien veröffentlicht. Bei Aufbewahrungsprüfungen werden der zurückgegebene „Object Lock“-Modus und das Datum mit der beim Upload übermittelten Frist verglichen (mit einer Rundungstoleranz von einer Sekunde). Eine abgelaufene, ungültige oder verkürzte Frist gilt nicht als verifiziert. Der Status gibt das Stichprobenobjekt an, dessen Aufbewahrungsstatus für diesen Upload-Durchlauf zurückgelesen wurde.

Der Kopierfortschritt ist auf das Ziel und den Verschlüsselungsschlüssel beschränkt. Durch Ändern des Endpunkts, des Buckets oder des Präfixes wird eine vollständige Kopie des lokal gespeicherten Protokolls, der Medien und der Checkpoints an dieses Ziel gestartet. Alter, nicht in den Umfang fallender Fortschritt bleibt erhalten, wird jedoch nach dem Upgrade einmalig erneut ausgeführt. Historische Chat-Exporte, die bereits aus dem lokalen Ausgangsordner entfernt wurden, verbleiben an ihrem bisherigen Zielort.

Fehlende oder beschädigte lokale Medien werden als Fehler des Durchlaufs gemeldet, und der Mediencursor bleibt vor diesem stehen, sodass die Datei im nächsten Durchlauf erneut versucht wird; die darauf folgenden Dateien, Checkpoints und Exporte werden weiterhin kopiert. Die Wiederherstellungsprüfung vergleicht alle Verweise auf erhaltene Medien mit entschlüsselten Hashes und aufgezeichneten Größen. Identische, sich überschneidende Protokollsegmente aus unterbrochenen Uploads werden dedupliziert; widersprüchliche Überschneidungen werden verworfen. Während eines Uploads erstellte Kontrollpunkte werden zurückgestellt, bis die von ihnen abgedeckten Protokolleinträge kopiert wurden, sodass ein abgeschlossener Durchlauf keinen Kontrollpunkt vor seinem Protokoll veröffentlicht.

### Streaming-Export-Momentaufnahmen

Streaming-Exporte verwenden einen stabilen SQLite-Lese-Snapshot. Dessen Anfang kann älter sein als das aktuelle Live-Protokoll, wenn der Download abgeschlossen ist. Ein nach diesem Snapshot erstellter Checkpoint kann korrekt melden, dass das Archiv kürzer ist; vergleichen Sie dies mit einem Checkpoint am oder vor dem exportierten Präfix, nicht mit einem beliebigen späteren Checkpoint.

## Vorbereitung gemäß RFC 3161 und Überprüfung der Antworten (0.2)

Im Beweismodus (standardmäßig deaktiviert) wird lediglich der SHA-256-Hash jedes signierten Checkpoints an die aufgeführten RFC-3161-Autoritäten und OpenTimestamps-Kalender gesendet – und zwar über die Workspace-Route und niemals über MTProxy. Die Antworten werden in `checkpoints/anchors/` gespeichert, exportiert und von `verify.py` überprüft (`--tsa-ca` überprüft die TSA-Signatur; Bestätigen Sie die OpenTimestamps-Nachweise mit `ots upgrade` und `ots verify`).

Das Panel erstellt ein Anforderungsarchiv, das kanonische „checkpoint.json“-Bytes, einen SHA-256-Nachrichtenabdruck und einen zufälligen Nonce in „timestamp.tsq“, Prüfsummen sowie Anweisungen enthält. Es wird keine Netzwerkanfrage gestellt. Die Vorbereitung stellt keinen vertrauenswürdigen Zeitstempel dar.

`python -m tgwitness.anchor verify` ruft OpenSSL zweimal auf: einmal anhand der Checkpoint- Bytes und einmal anhand der ursprünglichen Anfrage. Eine vertrauenswürdige CA-Datei ist ausdrücklich erforderlich; enthaltene Zertifikate werden nicht automatisch als vertrauenswürdig eingestuft. Die Überprüfung der Anfrage ist in der Befehlszeile optional; verwenden Sie daher weiterhin den Parameter „--request“, um den Nonce zu überprüfen. Das Ergebnis gibt an, ob die Überprüfung stattgefunden hat. Die Checkpoint-Signatur des Collectors und das Protokoll müssen weiterhin separat anhand des vertrauenswürdigen Fingerabdrucks des Collectors verifiziert werden.

Der derzeitige Verifizierer ruft keine Informationen zu widerrufenen Zertifikaten ab und führt keine Langzeitarchivierungsprüfung nach Ablauf des Zertifikats durch. Setzen Sie eine erfolgreiche Signaturprüfung nicht mit einem qualifizierten Zeitstempel oder der rechtlichen Zulässigkeit gleich. Eine echte, unabhängige TSA wurde während der Entwicklung nicht kontaktiert. Siehe [Vorgehensweise](https://phishdestroy.github.io/TgWitness/de/docs/reference/timestamp/).
