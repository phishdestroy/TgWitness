# So funktioniert das Beweismaterial

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/how-it-works/

Hash-Kette, Signaturen, Kontrollpunkte und Zeugen werden anhand der genauen Formeln erläutert, die der Verifizierer verwendet.

TgWitness bewahrt die von einem Erfassungskonto beobachteten Inhalte auf, verknüpft diese Beobachtungen zu einem signierten Protokoll und ermöglicht es einer anderen Person, einen Export anhand eines vertrauenswürdigen Schlüssels und eines zuvor gespeicherten Prüfpunkts zu verifizieren.

Die [lokale Dokumentationswebsite](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally) enthält zudem interaktive Beispiele unter `/docs/concepts/` sowie einen Checkpoint-Entscheidungs-Explorer unter `/docs/witness/`. Alle Beispielnachrichten, Zählwerte und Verzögerungen sind fiktiv. Die Hashes in der Chain-Sandbox werden mit SHA-256 im Browser berechnet. Es werden keine Daten an Telegram gesendet.

## Eine Nachricht ändert sich; Beobachtungen sammeln sich an

Sequenzdiagramm · Telegram → Collector: Neue Nachricht: Treffen um 10:00 Uhr; Collector → Signiertes Protokoll: Nachricht.new anhängen; Telegram → Collector: Bearbeitet: Treffen um 11:00 Uhr; Collector → Signiertes Protokoll: Nachtrag: Nachricht.bearbeitet; Telegram → Collector: Hinweis zur Löschung; Collector → Signiertes Protokoll: Nachtrag: message.deleted; Anmerkung zu Signiertes Protokoll: Original + Bearbeitung + Löschvorgang bleiben erhalten · Telegram · Collector · Signiertes Protokoll · Neue Nachricht: Treffen um 10:00 Uhr · Nachricht.new anhängen · Bearbeitet: Treffen um 11:00 Uhr · Nachtrag: Nachricht.bearbeitet · Hinweis zur Löschung · Nachtrag: message.deleted · Original + Bearbeitung + Löschvorgang bleibenerhalten

**Diagramm als Text**

1. Telegram → Collector: Neue Nachricht: Treffen um 10:00 Uhr
2. Collector → Signiertes Protokoll: Nachricht.new anhängen
3. Telegram → Collector: Bearbeitet: Treffen um 11:00 Uhr
4. Collector → Signiertes Protokoll: Nachtrag: Nachricht.bearbeitet
5. Telegram → Collector: Hinweis zur Löschung
6. Collector → Signiertes Protokoll: Nachtrag: message.deleted
7. Anmerkung zu Signiertes Protokoll: Original + Bearbeitung + Löschvorgang bleiben erhalten

Diese vereinfachte Abfolge geht davon aus, dass Telegram jede Aktualisierung zugestellt hat und das ausgewählte Konto diese einsehen konnte. Auch operative Ereignisse werden im Protokoll erfasst. Eine Löschmeldung gibt weder den Löschenden noch einen genauen Löschzeitpunkt an. Wiederholte Zustellungen gelten als separate Beobachtungen; es erfolgt keine protokollweite Unterdrückung von Duplikaten.

## Was ein Hash abdeckt

![Beobachten, kodieren, hashen und signieren: Jedes neue Ereignis enthält den vorhergehenden Hashwert.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

Lesen Sie die Formel von innen nach außen: „**C**“ wandelt die neun Felder in exakte Bytes um; **„SHA-256“** erzeugt deren Digest; **„hex“** gibt an, wie dieser Digest gespeichert wird. Der vorherige Hash ist bereits im Ereignis enthalten. **„unhex“** wandelt den gespeicherten Hash wieder in die 32 Bytes um, die Ed25519 signiert.

[Statisches Ketten-Diagramm](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

Sei C(ei) das kanonische UTF-8-JSON der neun Ereignisfelder. Der erste Datensatz `previous_hash` besteht aus 64 Nullen. Jeder nachfolgende Datensatz enthält den hexadezimalen Hash des vorhergehenden Datensatzes:

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

Die Signatur umfasst die 32 Rohdaten-Byte des Digests. Die Hash-Eingabe enthält genau `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` und `previous_hash`. Objektschlüssel sind sortiert; Leerzeichen und ASCII- Escape-Zeichen werden weggelassen; NaN und Unendlich werden verworfen. Siehe die [genaue Kodierung](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#event-canonicalization).

Ablaufdiagramm · 64 Nullen → Eintrag 1 / Hash h1; Eintrag 1 / Hash h1 → Eintrag 2 enthält h1 / Hash h2; Eintrag 2 enthält h1 / Hash h2 → Eintrag 3 enthält h2 / Hash h3; Eintrag 3 enthält h2 / Hash h3 → Signierter Checkpoint: Zählung 3, Überschrift h3 (an anderer Stelle aufbewahren) · 64 Nullen · Eintrag 1 / Hash h1 · Eintrag 2 enthält h1 /Hash h2 · Eintrag 3 enthält h2 /Hash h3 · Signierter Checkpoint:Zählung 3, Überschrifth3 · an anderer Stelle · aufbewahren

**Diagramm als Text**

1. 64 Nullen → Eintrag 1 / Hash h1
2. Eintrag 1 / Hash h1 → Eintrag 2 enthält h1 / Hash h2
3. Eintrag 2 enthält h1 / Hash h2 → Eintrag 3 enthält h2 / Hash h3
4. Eintrag 3 enthält h2 / Hash h3 → Signierter Checkpoint: Zählung 3, Überschrift h3 (an anderer Stelle aufbewahren)

| Wechseln Sie zum bereitgestellten Protokoll | Was erkennt es? |
| --- | --- |
| Ändern Sie Datensatz 2, ohne dessen gespeicherten Hash zu verändern | Der neu berechnete Ereignis-Hash weicht ab; seine Signatur deckt das geänderte Ereignis nicht mehr ab |
| Rekonstruktion des veränderten Datensatzes und aller nachfolgenden Hash-Werte | Die ursprünglichen Signaturen sind ungültig; ein gespeicherter Prüfpunkt an der betroffenen Grenze weist ebenfalls Abweichungen auf |
| Entfernen Sie den Anhang, behalten Sie jedoch das verbleibende Präfix bei | Ein früherer gespeicherter Kontrollpunkt jenseits des angegebenen Präfixes zeigt, dass der Export zu kurz ist |
| Ein Ersatzprotokoll mit einem anderen Schlüssel neu signieren | Ein separat vertrauenswürdiger Schlüssel-Fingerabdruck weist die Ersatzidentität zurück |

![Das Ändern eines gespeicherten Feldes verändert dessen Digest; das Neuerstellen von Hashes stellt die ursprünglichen Signaturen nicht wieder her.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**Probieren Sie die Logik bei Datensatz 2 aus:** Ändern Sie „`Meet at 11:00`“ in „`Meet at 12:00`“ im gespeicherten Ereignis. Der neu berechnete Hash stimmt nun nicht mehr überein. Durch die Neuberechnung der nachfolgenden Kette können deren Verknüpfungen zwar wiederhergestellt werden, doch die ursprünglichen Signaturen können die neuen Digests nicht mehr abdecken. Eine beobachtete Bearbeitung in Telegram wird hingegen zu einem neuen Protokoll-Eintrag.

[Diagramm der statischen Änderungen](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

Hash-Links allein verhindern nicht, dass jemand eine Ersatzkette neu berechnet. Vertrauen entsteht durch die Überprüfung der Signaturen unter einem unabhängig vertrauenswürdigen Schlüssel und den Abgleich mit Referenzen, die außerhalb des Collectors aufbewahrt werden.

## Was ein früherer Prüfpunkt hinzufügt

![Behalten Sie die Zählung 3 und die Überschrift h3 bei; ein späterer Export von 4 Datensätzen wird an Position 3 überprüft.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**Der Referenzwert bleibt unverändert, während das Protokoll wächst.** Wenn der Prüfpunkt angibt: „3 Datensätze, Kopf h3“, kann ein Export mit vier Datensätzen erfolgreich sein, indem h3 an Position 3 abgeglichen wird. Der aktuellste Kopf ist h4, der sich voraussichtlich unterscheidet. Ein Export mit nur zwei Datensätzen schlägt fehl.

[Statisches Checkpoint-Diagramm](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

Nach Überprüfung der Checkpoint-Signatur ist Folgendes erforderlich:

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

Ein Export kann über einen Prüfpunkt hinausreichen. Er muss an der beibehaltenen Grenze übereinstimmen. Der eigentliche Prüfer überprüft zudem die Abfolge jedes Ereignisses, den vorherigen Link, den Hashwert und die Signatur. Würde man nur den abschließend gespeicherten Kopf vergleichen, würde ein veränderter innerer Datensatz übersehen werden, dessen gespeicherter Hashwert nicht aktualisiert wurde.

## Wo ein Zeuge hingehört

Ablaufdiagramm · Collector / Kontositzung / Schlüssel A → Endpunkt für schreibgeschützte Checkpoints; Witness / festgesteckter Sammelschlüssel / eigener Schlüssel B → Separates, signiertes Zeugenprotokoll; Witness / festgesteckter Sammelschlüssel / eigener Schlüssel B → Endpunkt für schreibgeschützte Checkpoints (Überprüfung anfordern); Endpunkt für schreibgeschützte Checkpoints → Witness / festgesteckter Sammelschlüssel / eigener Schlüssel B (Signierte Antwort); Witness / festgesteckter Sammelschlüssel / eigener Schlüssel B → Kanal mit signierten TGW1-Beiträgen (Bot-API / eigenes Token) · Host A · Host B · Collector / Kontositzung /Schlüssel A · Endpunkt fürschreibgeschützteCheckpoints · Witness / festgesteckterSammelschlüssel / eigenerSchlüssel B · Separates, signiertesZeugenprotokoll · Kanal mit signiertenTGW1-Beiträgen · Überprüfung anfordern · Signierte Antwort · Bot-API / eigenes Token

**Diagramm als Text**

1. Collector / Kontositzung / Schlüssel A → Endpunkt für schreibgeschützte Checkpoints
2. Witness / festgesteckter Sammelschlüssel / eigener Schlüssel B → Separates, signiertes Zeugenprotokoll
3. Witness / festgesteckter Sammelschlüssel / eigener Schlüssel B → Endpunkt für schreibgeschützte Checkpoints (Überprüfung anfordern)
4. Endpunkt für schreibgeschützte Checkpoints → Witness / festgesteckter Sammelschlüssel / eigener Schlüssel B (Signierte Antwort)
5. Witness / festgesteckter Sammelschlüssel / eigener Schlüssel B → Kanal mit signierten TGW1-Beiträgen (Bot-API / eigenes Token)

Der Witness protokolliert Rückgängigmachungen, unterschiedliche Kopfzeilen bei gleicher Zählung, geänderte Schlüssel, ungültige Antworten und fehlende Rückmeldungen. Eine höhere Zählung allein belegt nicht, dass alle früheren Einträge unverändert geblieben sind; vergleichen Sie den Export mit den gespeicherten Prüfpunkten. Ein Witness auf einem anderen Host verhindert, dass er von einem Ausfall des Collector-Hosts betroffen ist; ein separater Betreiber sorgt für zusätzliche Unabhängigkeit.

Der „Witness“ bestätigt den vom „Collector“ gemeldeten Protokollstatus. Er beobachtet nicht eigenständig alle Telegram-Nachrichten. Siehe [Einrichtung des „Witness](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/)“.

## Testdurchführung unter Berücksichtigung bekannter Maßnahmen

Verwenden Sie eine Kontrollgruppe, separate Sammelkonten und einen neuen Marker. Senden, bearbeiten und löschen Sie gezielt und überprüfen Sie die Erfassung zwischen den einzelnen Schritten. Legen Sie die erwarteten Aktionen und einen Stichtag fest, bevor Sie die Ergebnisse überprüfen.

R = |observed∩expected| / |expected| Δ t = treceipt - taction

Es zählen nur übereinstimmende erwartete Aktionen; doppelte Empfangsbestätigungen erhöhen den Zähler nicht. Der Nenner muss ungleich Null sein. Eine fehlende Empfangsbestätigung weist keine gemessene Verzögerung auf. Dokumentieren Sie die Unsicherheit der Zeitangaben; verwenden Sie Ihre eigene kontrollierte Löschzeit, da Telegram den genauen Zeitpunkt der Löschung nicht angibt. Ein Ergebnis wie 5/6 (83,3 %) beschreibt die Testaktionen, nicht die Vollständigkeit des gesamten Telegram-Datenverkehrs.

## Wählen Sie einen Arbeitsablauf aus

Die [vollständige Anleitung zur Untersuchung](https://phishdestroy.github.io/TgWitness/de/docs/reference/investigation/) verfolgt den Verlauf eines Vorfalls über einen Kanal, eine Gruppe, einen Bot und einen privaten Chat hinweg:

1. Aktivieren Sie den Untersuchungsmodus für das gesamte Konto und erfassen Sie jeden zugänglichen Chat.
2. Erfassen Sie Protokoll-Momentaufnahmen, den vollständigen Verlauf pro Chat sowie erhaltene Anhänge.
3. Speichern Sie Live-Änderungen sowie alle absichtlichen Interaktionen mit den Bedienfeldern zusammen mit den entsprechenden Belegen.
4. Verfolgen Sie numerische Absender-IDs, Antwortbeziehungen, wiederkehrende Empfänger und Datei- Hashes anhand zitierter Datensätze und Personenprofile.
5. Rekonstruktion einer chatübergreifenden Zeitleiste mit Zeitstempeln und expliziten Lücken.
6. Vergleichen Sie die Arbeitsbereiche anderer Konten, wobei deren Ursprünge und Schlüssel getrennt bleiben.
7. Stellen Sie die signierten Protokolle, Profile und Verlaufsexporte zusammen und überprüfen Sie diese anhand von Fallnotizen.

Der „`/docs/cases/`“-Leitfaden der Website enthält eine interaktive Fallkarte sowie Varianten für Bot-Streitigkeiten, gelöschte Nachrichten und Teilnehmer, die ihren Namen ändern. Fallnotizen und arbeitsbereichsübergreifende Analysen erfolgen extern; die Anwendung generiert nicht automatisch ein globales Ermittlungsdiagramm oder ein zusammengeführtes Fallarchiv.

[Abgeschlossene Validierung und verbleibende Arbeiten](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/) · [Exportieren und verifizieren](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#investigation-handoff) · [Beginnen Sie mit einem Konto](https://phishdestroy.github.io/TgWitness/de/docs/reference/quickstart/)
