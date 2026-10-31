# Erfahren Sie, wie die Beweissicherung funktioniert

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/concepts/

Eine Nachricht kann sich ändern. Die Aufzeichnung dessen, was Sie beobachtet haben, sollte überprüfbar bleiben.

Entdecken Sie unten zwei kleine Experimente. Diese verwenden fiktive Nachrichten, laufen direkt in Ihrem Browser und stellen zu keinem Zeitpunkt eine Verbindung zu Telegram her.

## Eine Nachricht, drei Beobachtungen

Wenn Telegram eine neue Nachricht, eine Bearbeitungs- oder eine Löschbenachrichtigung übermittelt, fügt der Collector drei separate Einträge hinzu. Die Bearbeitung ersetzt den ersten Eintrag nicht. Eine Löschbenachrichtigung löscht ihn nicht.

01 / DER WEG DER NACHRICHTBeispielablauf

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Collector · Protokoll · Aktualisierung → · Anhängen →

AKTUELLE CHAT-ANSICHT Nachricht Nr. 42

Nachricht gelöscht

Die Nachricht ist aus der Chat-Ansicht verschwunden.

BEOBACHTUNGSPROTOKOLL 3 Einträge

1. 01

   `message.new`

   Treffpunkt um 10:00 Uhr

   ✓
2. 02

   `message.edited`

   Treffpunkt um 11:00 Uhr

   ✓
3. 03

   `message.deleted`

   Löschhinweis zu Nr. 42

   ✓

Alle drei erfassten Beobachtungen verbleiben im Protokoll.

Vereinfachter Pfad für eine bereits ausgewählte Quelle. Operative Aufzeichnungen greifen ebenfalls auf das tatsächliche Protokoll zurück. Die Erfassung hängt davon ab, was das Konto einsehen kann und was Telegram bereitstellt.

Eine Löschmeldung liefert weder einen verlässlichen Zeitpunkt der Löschung noch den Namen der Person, die die Nachricht gelöscht hat. Indem diese Werte unbekannt bleiben, wird die Unterscheidung zwischen einer Beobachtung und einer Vermutung gewahrt.

## Ändern Sie einen Datensatz. Folgen Sie dem Hash.

Jeder Datensatz enthält den Hash des vorherigen Datensatzes. Sein eigener Hash umfasst die Ereignisfelder, einschließlich dieses Links. Ein extern gespeicherter Checkpoint fixiert eine bestimmte Protokollänge und den Kopf-Hash.

02 / HASH-CHAIN SANDBOXEchtes SHA-256 · Beispieldatensätze

AUFZEICHNUNG 01**Nachricht empfangen**`h₁ = SHA-256(e₁)`Links zu 64 Nullen

AUFZEICHNUNG 02**Treffpunkt um 11:00 Uhr**`h₂ = SHA-256(e₂)`Enthält h₁

AUFZEICHNUNG 03**Löschung festgestellt**`h₃ = SHA-256(e₃)`Enthält h₂

AN ANDERER STELLE GESPEICHERT**3 Einträge · Kopfzeile `h₃`**Vergleichen Sie diese festgelegte Abgrenzung mit dem bereitgestellten Protokoll.

Das Ändern eines Ereignisses verändert dessen Hash-Wert. Das Neuerstellen der Kette verändert deren Kopf. Das Entfernen des Endes führt dazu, dass die Kette kürzer ist als der beibehaltene Kontrollpunkt.

**Sehen Sie sich Datensatz 2 und die vollständigen Hashes an**

Dies ist der exakte UTF-8-JSON-Text, der in diesem Beispiel gehasht wurde. Die Werte sind fiktiv; die neun Felder und die Serialisierung entsprechen dem Protokollformat.

```

```

Hash des gespeicherten Datensatzes 2

``

Neu berechneter Hash von Datensatz 2

``

Diese Sandbox berechnet Hashes, keine Signaturen. Der eigentliche Verifizierer überprüft zudem die Ed25519-Signatur, die Sequenz und den Link jedes Ereignisses. Durch die bloße Rekonstruktion von Hashes lassen sich unter dem vertrauenswürdigen Schlüssel keine gültigen Signaturen erstellen.

## Die eigentlichen Regeln in wenigen Zeilen

HASH + SIGNATUR

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** serialisiert die neun Ereignisfelder als UTF-8-JSON: sortierte Schlüssel, keine zusätzlichen Leerzeichen, keine ASCII-Escape-Zeichen und keine NaN-/Unendlich-Werte. Der Wert `previous_hash` des Ereignisses beträgt hi−1. Der angezeigte Wert h0 steht für 64 Nullzeichen; die Signaturen decken die 32 Rohdaten-Byte des Digests ab.

Die neun Felder lauten `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` und `previous_hash`. Dies ist [die dokumentierte JSON-Kodierung](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#event-canonicalization) von TgWitness; der Hash und die Signatur selbst sind keine Hash-Eingabefelder.

BEIBEHALTENER PRÜFPUNKT

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Überprüfen Sie die Signatur des Checkpoints unter dem angehefteten Collector-Schlüssel und vergleichen Sie anschließend dessen Grenzen mit dem verifizierten Protokoll. Ein späterer Export kann weitere Datensätze enthalten; er muss jedoch weiterhin mit dem früheren Checkpoint übereinstimmen.

## Drei Fragen, drei verschiedene Überprüfungen

[01 / INTEGRITÄT**Hat sich dieser Eintrag geändert?** Überprüfen Sie Hashes und Signaturen anhand eines separat vertrauenswürdigen Schlüssels.](https://phishdestroy.github.io/TgWitness/de/docs/exports/)[02 / KONTINUITÄT**Was wurde zuvor beibehalten?** Vergleichen Sie einen signierten Export mit Kontrollpunkten, die von einem separaten Zeugen geführt werden.](https://phishdestroy.github.io/TgWitness/de/docs/witness/)[03 / LIEFERUNG**Sind diese Testereignisse eingegangen?** Abgleichen von kontrollierten Sende-, Bearbeitungs- und Löschvorgängen mit dem Protokoll des jeweiligen Kontos.](https://phishdestroy.github.io/TgWitness/de/docs/cases/)

Eine übereinstimmende Hash-Kette beantwortet eine Integritätsfrage. Sie belegt weder die vollständige Zustellung einer Telegram-Nachricht noch die Richtigkeit einer Nachricht oder einen unabhängig verifizierten Beobachtungszeitpunkt.

Verfolgen Sie die [gesamte Untersuchung eines Kontos](https://phishdestroy.github.io/TgWitness/de/docs/cases/) von der Erfassung bis zur Fallakte.
