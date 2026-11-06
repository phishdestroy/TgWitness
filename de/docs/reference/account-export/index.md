# Kontoexport

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/account-export/

Exportieren Sie, was ein Konto derzeit lesen kann: Umfang, wiederaufnehmbare Aufträge, ein signiertes Archiv und minimierte Freigabekopien.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

Ein Kontoexport reserviert sein Konto exklusiv. Pausieren Sie vor dem Starten oder Fortsetzen ausdrücklich die Überwachung oder eine andere Erfassung; die Anwendung beendet diese niemals automatisch.

Wählen Sie als Installationsadministrator entweder **Hier beginnen → Mein Konto exportieren** oder **Exporte → Telegram-Konto → Kontoexport konfigurieren**. Melden Sie sich bei Bedarf an, überprüfen Sie den Umfang und starten Sie den Export explizit. Eine kontinuierliche Überwachung ist nicht erforderlich. **Gespeicherte Beobachtungen** ist ein separater Export des bestehenden Journals; dessen ZIP umfasst alle Quellen unabhängig von Journalfiltern. Jeder Arbeitsbereich verfügt über eigene Jobs, eine eigene Signaturidentität und eigenen Speicherplatz. Ein erteilter Panel-Zugriff, einschließlich einer uneingeschränkten Berechtigung für normale Exporte, kann diese kontoweiten Pfade nicht öffnen.

Sender- und Textfilter lassen sich unter **„Nach Absender oder Nachrichtentext filtern“** erweitern. **Der Bereich „Kontodaten & Verbindungsmethode“** enthält optionale Kontokategorien und die Auswahl zwischen „Takeout“ und „reguläre Sitzung“; in der Zusammenfassung werden die aktiven Auswahlen auch im geschlossenen Zustand angezeigt. Beim Schließen dieser Bereiche bleiben die Einstellungen erhalten. Export- und Berichtsentwürfe bleiben beim Wechseln der Ansichten in der aktuellen Panel-Sitzung erhalten; sie werden beim Neuladen des Browsers nicht gespeichert. Vorhandene Aufträge bleiben über beide Exportoptionen erreichbar.

Dieser Workflow exportiert Daten, auf die das verbundene Konto derzeit Zugriff hat. Standardmäßig wird [„Telegram Takeout“](https://core.telegram.org/api/takeout) verwendet; es handelt sich nicht um eine Sicherung nicht verfügbarer oder gelöschter Telegram-Daten. Geheime Chats, nicht zugänglicher Verlauf und frühere Bearbeitungen werden nicht wiederhergestellt. Telegram kann eine Wartezeit vorschreiben, bevor „Takeout“ startet. Das Bedienfeld zeigt diese Wartezeit an; es wechselt nicht unbemerkt den Übertragungsweg. Die explizite Option „regular-API“ hat einen anderen Erfassungsumfang und erfasst nicht unterstützte Kategorien.

Takeout is the official export API also used by Telegram Desktop. TgWitness can write Desktop-compatible JSON directly from its own acquisition; importing someone else's archive is not required. Chat and message IDs are available through both transports. A public chat or permission to forward does not guarantee a faster export or remove Takeout's approval delay. Measure the same scope and media settings before comparing speed.

For up to 20 explicitly selected chat IDs, regular-API export resolves those peers directly before considering the account's complete dialog inventory. A readable public channel can therefore be exported without joining it, even when it is absent from the dialog list. Uncached peers fall back to the ordinary inventory. The archive filter remains enforced: if Telegram does not return a dialog and archived chats are excluded, the unknown archive status is recorded as an omission. Takeout keeps its split-range inventory procedure. Neither path joins chats or changes forwarding permissions. In Desktop-compatible JSON, channels that Telegram marks `left` appear under `left_chats`, including readable public channels the account has not joined.

Both `FLOOD_WAIT` and `FLOOD_PREMIUM_WAIT` pause requests for the full server-requested period. The account's deadline is persisted across reconnects and restarts; a shorter later wait cannot shorten it. Retries are bounded, cancellation preserves sealed pages, and API credentials are not rotated to bypass a rate limit. No Premium purchase is made.

## Wählen Sie aus, was erfasst werden soll

| Einleitung | Bedeutung |
| --- | --- |
| Zweck | Halten Sie fest, warum diese Akquisition erforderlich ist. Geben Sie hier keine unnötigen Namen oder vertraulichen Details zum Fall an. |
| Berichtssprache | Wählen Sie die Sprache für die Beschriftungen im lesbaren Bericht aus. Der Originaltext der Nachrichten bleibt unverändert; nicht übersetzte Vorlagenbeschriftungen verwenden Englisch. Die Sprache wird über die Optionen des signierten Auftrags festgelegt. |
| Chat-Typen / Chat-IDs | Alle ausgewählten Arten oder nur die aufgelisteten Chats; „Gespeicherte Nachrichten“ gehören zu privaten Chats. Archivierte Chats sind separat auswählbar. |
| Daten | UTC. Die Kalenderdaten für „Von“ und „Bis“ des Panels sind beide enthalten. Die API verwendet inklusive `from_utc` und exklusive `to_utc`; das Panel sendet den Beginn des Tages nach „Through“. Ein leerer Grenzwert lässt diese Seite uneingeschränkt. |
| Absender-IDs | Nur Nachrichten der aufgeführten Absender; eine leere Liste umfasst alle Absender. |
| Der Text enthält | Groß-/Kleinschreibung bei wörtlichen Phrasen wird nicht berücksichtigt, die Suche erfolgt mit „ODER“. Bedingungen zu Absender, Datum und eigener Nachricht werden mit „UND“ kombiniert. |
| Eigene Nachrichten | Nur ausgehende Nachrichten aufbewahren. |
| Medientypen | Wählen Sie Anhangskategorien aus oder löschen Sie alle, um das Herunterladen von Nachrichtendateien zu vermeiden. |
| Datei- bzw. Gesamtmedienbeschränkungen | MiB pro Datei und GiB an insgesamt heruntergeladenen Medien. Text, Empfangsbestätigungen, lesbare Berichte und ZIP-Overhead benötigen zusätzlichen Speicherplatz. |
| Kontokategorien | Profil, Kontakte, Profilfotos, Stories, Sitzungsmetadaten und andere Takeout-Daten verfügen über separate Steuerelemente. |

Die Voreinstellung **„Minimize“** deaktiviert Dateien und Kontometadaten. Absender- und Inhaltsfilter werden vor der Speicherung von Nachrichtenseiten und dem Herunterladen von Medien angewendet. Telegram übermittelt weiterhin API-Verlaufsseiten, die Nachrichten enthalten, die zur Auswertung dieser Filter benötigt werden: Die Filterung ist keine Garantie dafür, dass nicht ausgewählte Nachrichten niemals in den Prozessspeicher gelangen. Andere laufende Beobachtungen im Arbeitsbereich haben ihre eigenen Umfangs- und Aufbewahrungseinstellungen.

Profilbildverlauf und Stories sind standardmäßig nicht ausgewählt. Deaktivieren Sie auch Profil und Kontakte, wenn für den Fall nur Nachrichten benötigt werden. Wenn Anhänge oder Metadaten nicht erforderlich sind, vermeiden Sie durch deren Ausschluss bei der Erfassung, dass eine weitere private Kopie in diesem Export verbleibt.

Photo payloads use the still-image variant identified in their metadata and hash manifests, including photos with an animated avatar variant. That animation is not substituted for the selected still image. A shorter or longer payload than the observed size is recorded as a failed attachment, and a changed representation during file-reference renewal is rejected. These failures leave the archive partial while retaining the message records. Independent verification also rejects saved attachments whose signed length contradicts their observed size or representation, including in older archives.

## Zusammenfassung, Berichterstattung und Überprüfung

Jeder Auftrag friert seine Optionen und die Kontoidentität ein. Bestandsliste und erfasste Seiten werden signiert; Seitenbelege zeichnen Hashes, Cursorpositionen, Zeitangaben, Ergebnisse von Anhängen und den vorhergehenden Beleg auf. Nur festgeschriebene Seiten treiben den Fortschritt voran. Beim Neustart/Fortsetzen werden diese Aufzeichnungen überprüft, bevor fortgefahren wird. Ein geändertes Konto, eine geänderte signierte Seite oder eine inkonsistente Belegkette werden abgelehnt. Optionen können während einer Erfassung nicht bearbeitet werden: Starten Sie einen neuen Auftrag für einen anderen Umfang.

Mit „Pause“ wird der laufende Kontovorgang unterbrochen. Beim Neustart der Anwendung bleiben unvollendete Arbeiten erhalten und können explizit fortgesetzt werden. Eine abgelaufene Takeout-Sitzung erfordert eine explizite Fortsetzung; das Ändern von Telegram-Split-Bereichen kann eine neue Erfassung erfordern. Bei der Fortsetzung bleiben vorherige Beobachtungen erhalten, sodass ein lang andauernder Export nicht als ein einziger atomarer Snapshot gilt. Andere Vorgänge, die einen Kontowechsel erfordern, sowie konfliktbehaftete Exporte werden während der Erfassung blockiert. Warten Sie, bis die Paketierung abgeschlossen ist, bevor Sie einen Arbeitsbereich löschen.

„Resume“ überprüft bereits erfasste Inhalte, bevor der Vorgang fortgesetzt wird. Große Archive auf langsamen Speichermedien können die konfigurierte Zeit **Parameter → Zeitlimit für Panel-Aktionen** (standardmäßig 120 Sekunden) überschreiten. Erhöhen Sie diese Einstellung, bevor Sie es erneut versuchen; bei Abbruch oder Speicherunterbrechung wird der Auftrag angehalten, und bei fehlgeschlagenen Integritätsprüfungen wird der Auftrag mit einer Erklärung als fehlgeschlagen markiert. Die Überprüfung muss abgeschlossen oder sicher beendet werden, bevor die Dateien geschlossen werden können. Keine der Angaben zum Durchsatz bei großen Konten wurde durch die synthetischen Tests validiert.

Das Panel unterscheidet zwischen einem vollständig erfassten ausgewählten Bereich und einem Teilarchiv und protokolliert Auslassungen sowie fehlgeschlagene Lesevorgänge. Absichtlich ausgeschlossene Dateien unterscheiden sich von fehlgeschlagenen oder nicht verfügbaren Dateien. Überprüfen Sie die Abdeckung auch dann, wenn die Integritätsprüfung erfolgreich verläuft. Kein lokaler Reader kann nachweisen, dass Telegram jede jemals existierende Nachricht zurückgegeben hat.

Fertiggestellte ZIP bleiben für wiederholte Downloads und HTTP-Range-Downloads verfügbar. Ein Kontoarchiv enthält `manifest.json`, `manifest.sig`, signierte `job.json`, `inventory.json`, `receipts/`, verbindliche `data/*.jsonl`, ausgewählte `media/`, lesbares HTML und einen Verifizierer. Heften Sie den Fingerabdruck des Collectors über einen unabhängigen Kanal an und verifizieren Sie ihn anschließend mithilfe einer vertrauenswürdigen Installation:

```
python -m tgwitness.verify account-export.zip --fingerprint TRUSTED_SHA256
```

Für Archive, deren entpackter Inhalt 4 GiB überschreitet, legen Sie explizit eine angemessene `--max-gib`. Das Panel überprüft seine authentifizierten, vollständigen lokalen Archive anhand ihrer angegebenen erweiterten Größe und des veröffentlichten ZIP-Digests; die externe CLI behält ihre eigene Größenbeschränkung bei. Überprüfen Sie das Archiv, bevor Sie die lesbare HTML-Datei öffnen. Der im Archiv enthaltene Verifizierer ist praktisch, aber ein unabhängig beschaffter Verifizierer vermeidet es, ausführbarem Code zu vertrauen, der mit den Nachweisen geliefert wird.

Die Ed25519-Signatur und die Hashes SHA-256 erkennen Änderungen, nachdem der Collector die entsprechenden Bytes gespeichert hat. Sie beweisen **nicht**, dass Telegram diese Nachrichten signiert hat, dass der Collector-Betreiber ehrlich war, dass der Verlauf des Kontos vollständig ist oder dass ein Gericht das Material akzeptieren wird. Als Erfassungszeitpunkte gilt die Uhrzeit des Collectors. Unabhängige Zeitstempel und die Herkunft der Erfassung müssen separat bewertet werden.

## Bereiten Sie eine Offenlegung für einen Anwalt oder einen anderen Empfänger vor

Behalten Sie nach dem Herunterladen eines fertigen Exports die Originaldatei ZIP bei und öffnen Sie `index.html` aus einer extrahierten Kopie. Der Bericht erläutert seinen Umfang, die verfügbare Abdeckung und Einschränkungen. Seine Datensatzreferenzen kombinieren die Archivreferenz, den Dokumentpfad und die Datensatznummer, sodass ein Empfänger denselben Eintrag im HTML-Code oder im Ausdruck finden kann. Ein Beispiel finden Sie unter [Den fiktiven Bericht öffnen](https://phishdestroy.github.io/TgWitness/demo/report/).

Wählen Sie nach Abschluss eines Kontoexports **die Option „Freigabekopie erstellen“** aus. Dadurch wird eine separate, signierte Derivatdatei erstellt. Die Quelldatei ZIP bleibt unverändert und privat; versenden Sie sie nicht zusammen mit einer minimierten Derivatdatei, es sei denn, der Empfänger ist zum Empfang des vollständigen Inhalts berechtigt. Wählen Sie die Sprache des Berichts separat aus. Das Ändern der Sprache oder einer Auswahl-Einstellung erfordert vor der Erstellung eine weitere Vorschau.

1. Geben Sie den Zweck der Offenlegung ein und wählen Sie Datumsbereiche, Absender-IDs und Kriterien für den Wortlaut aus.
2. Wählen Sie aus, ob Identitäten beibehalten, nur aufgeführte Teilnehmer angezeigt oder alle Teilnehmer pseudonymisiert werden sollen. Im pseudonymisierten Modus werden zudem Chat-IDs/Titel und Nachrichten-IDs ersetzt. Pseudonyme bleiben innerhalb einer Offenlegung unverändert und ändern sich zwischen unabhängig voneinander erstellten Offenlegungen.
3. Behalten Sie den Nachrichtentext bei, lassen Sie ihn vollständig weg oder fügen Sie wörtliche Namen/Phrasen zur Maskierung hinzu. Im privaten Modus maskiert das Tool außerdem bekannte versteckte Absendernamen und alternative Benutzernamen, Absender-IDs in Form ganzer Token, Namen aus Direktchats, Links, E-Mail-Adressen und telefonähnliche Zeichenfolgen. Der Abgleich bekannter Namen berücksichtigt die Unicode-Groß-/Kleinschreibung, einschließlich `Straße`/`STRASSE`. Allgemeine Gruppen-/Kanaltitel werden nicht automatisch aus dem Nachrichtentext entfernt. Wenn das Limit für die Maskierung bekannter Identitäten überschritten wird, schränken Sie den Quell-Export ein oder lassen Sie Text weg; das Tool überspringt spätere Namen nicht stillschweigend. Hierbei handelt es sich um „Best-Effort“-Regeln, nicht um eine allgemeine Anonymisierung.
4. Lassen Sie Dateien unberücksichtigt, es sei denn, der Empfänger benötigt sie. Die enthaltenen Originale behalten ihre Pixel, Audio, Text und Metadaten bei. Sie werden vom Tool **nicht** anonymisiert.
5. Zeigen Sie eine Vorschau der Zählwerte, Warnungen und Beispielnachrichten in transformierter Form an und bestätigen Sie anschließend die Erstellung ausdrücklich. Die Beispiele sind auf jeweils 12 Nachrichten und 2.000 Textzeichen begrenzt. Dies ist ein Beispiel und keine vollständige Überprüfung des Ergebnisses. Das Ändern von Einstellungen erfordert eine weitere Vorschau. Eine Vorschau läuft nach 15 Minuten ab und ist an diese Administratorsitzung sowie an das exakte Original-ZIP gebunden; sie kann nach der Erstellung nicht wiederverwendet werden. Eine neue Vorschau macht die vorherige für denselben Auftrag und dieselbe Sitzung ungültig.
6. Sehen Sie sich das vollständige Ergebnis an `index.html` und `messages.jsonl` vor der Übergabe. Falls darin unnötige Informationen enthalten sind, erstellen Sie eine neue Offenlegung mit strengeren Ausschlusskriterien. Bearbeiten Sie das signierte ZIP nicht direkt an Ort und Stelle.

### Durch die Auswahl ausgelassene Nachrichten

**Vorschau.** Eine Offenlegung erscheint unvollständig, wenn sie es tatsächlich ist. In jedem Chat, der mindestens eine offengelegte Nachricht enthält, werden die von der Auswahl ausgelassenen Nachrichten als Markierungen angezeigt, `[withheld by selection — rule: sender]` (oder `text`, `period`). Wählen Sie **„Durch die Auswahl ausgelassene Nachrichten**“: eine Markierung für jede Folge aufeinanderfolgender zurückgehaltener Nachrichten (Standard) oder eine für jede einzelne Nachricht. Markierungen enthalten nur die Regel und eine Zählung, niemals Text, Absender, Datum oder Dateien. Chats, in denen nichts offengelegt wurde, werden vollständig ausgelassen, sodass das Paket deren Existenz nicht preisgibt.

Offen gelegte Antworten geben an, worauf sie sich beziehen: eine in dieser Kopie enthaltene Nachricht, eine durch die Auswahl zurückgehaltene Nachricht oder eine Nachricht, die nicht im Quell-Export enthalten ist (vor dem Export gelöscht oder nie exportiert; der Export kann nicht unterscheiden, was zutrifft). Eine zurückgehaltene Nachricht, auf die eine offengelegte Antwort Bezug nimmt, erhält immer eine eigene Kennzeichnung, sodass die Antwort auf einen Datensatz verweist, der erklärt, warum sie leer ist. Diese drei Zustände unterscheiden sich von Löschungen und Lücken in der Datensammlung, die zum Quell-Export gehören.

Im `messages.jsonl` (Format `tgwitness-account-disclosure-v2`) enthält jede Nachricht `state`: `disclosed`oder `withheld` mit `rules` und `count`. Eine offengelegte Antwort enthält `reply_to` mit dem Ziel `id` und `state` (`disclosed`, `withheld`, `not_in_source`). Das Manifest zählt offengelegte Nachrichten, Chats, Medien und `withheld` Nachrichten. `verify.py` Es lehnt einen Marker ab, der Inhalt enthält, sowie eine Antwort, die auf einen im Paket fehlenden Datensatz verweist; Pakete der Version 1 werden wie bisher verifiziert.

Das minimierte Format lässt strukturierte Kontoprofile, Kontakte, Avatare, Sitzungen, Stories, Telegram-Rohobjekte, Weiterleitungs-Header, Antwortzitate, Kontaktkarten und Standort-Metadaten weg. Es schließt die ursprünglichen JSONL-Dateien, private Filtereinstellungen, den Pseudonymschlüssel und die Identitätszuordnung aus. Ausgewählter Text, explizit beibehaltene Identitäten und eingebundene Dateien können weiterhin dieselben Namen, IDs oder Phrasen enthalten, die in diesen Filtern verwendet werden; sie müssen separat überprüft werden. Die private Richtlinie und der Pseudonymschlüssel werden verschlüsselt im lokalen Tresor des Auftrags aufbewahrt; das Löschen des Auftrags löscht die zugehörigen privaten Offenlegungsdatensätze. Die öffentliche Richtlinie erfasst die Anzahl der Filter statt der Filterwerte. Der angegebene Zweck ist im Manifest und im HTML öffentlich: Explizite private Kriterien und – in pseudonymisierten Modi – bekannte verborgene Identitäten werden dort ebenfalls maskiert, auch wenn der Nachrichtentext weggelassen wird. Halten Sie den Zweck frei von unnötigen persönlichen Details; unbekannter identifizierender Kontext kann bestehen bleiben.

Sein Manifest bindet die abgeleiteten Dateien, die öffentlichen Richtlinien und den Hash des ursprünglichen ZIP zusammen. Durch die Verifizierung lassen sich die Integrität sowie – sofern die Quelle lokal bereitgestellt wird – die Übereinstimmung der Quellverknüpfung feststellen:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Die Quellenverknüpfung beweist nicht eigenständig, dass bei der Transformation alle erforderlichen Elemente ausgewählt oder alle identifizierenden Details entfernt wurden. Der ursprüngliche Klartext ist nicht als Nachweis eingebettet. Für diese Beurteilung ist eine erneute Überprüfung erforderlich.

## Freigabe und gehostete Erfassung

Select the messages and files the recipient needs, review the complete sharing copy, and retain the source separately. Record the delivered ZIP's hash so the recipient can identify and verify that exact copy. Pseudonymization replaces the selected identifiers; included text and original files remain part of the review.

GitHub Actions supports full-account and selected-chat exports through Takeout or the regular API, plus a one-chat event journal. The [hosted capture guide](https://phishdestroy.github.io/TgWitness/docs/capture/) explains settings verification and the 120-minute limit. To verify a sharing copy derived from hosted capture, check its source hash against the original archive and verify that archive's attestation with the [mode-specific checks](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope).

[Format der Beweismittel](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/) · [Fallberichte](https://phishdestroy.github.io/TgWitness/de/docs/reference/case-reports/)
