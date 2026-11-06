# Telegram · Erfahren Sie, wie die Beweissicherung funktioniert

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/concepts/

Nachrichten ändern sich. Ihre Aufzeichnung dessen, was Sie gesehen haben, sollte das nicht, und jeder sollte das prüfen können.

Unten zwei kleine Experimente. Erfundene Nachrichten, alles läuft im Browser, nichts geht an Telegram.

## Vom Chat-Export zum überprüfbaren Datensatz

Ein [Telegram-Desktop-Export](https://telegram.org/blog/export-and-more) speichert den gerade sichtbaren Verlauf als HTML oder JSON. TgWitness ergänzt ein laufendes Änderungsjournal, Signaturen auf jedem Eintrag und Prüfpunkte, mit denen andere vergleichen können.

| Aufgabe | Export aus Telegram Desktop | TgWitness |
| --- | --- | --- |
| Gespeicherte Unterhaltungen lesen | HTML oder JSON mit ausgewählten Medien | Gespeicherte Chats, durchsuchbares Protokoll und Offline-Berichte |
| Verfolgen Sie eine Veränderung im Zeitverlauf | Der beim Export verfügbare Verlauf | Alte Versionen, spätere Bearbeitungen und Löschungen, alles behalten |
| Dateien nach der Übergabe überprüfen | Standardmäßige HTML-/JSON-Exportdateien sind nicht signiert. | Signiertes Manifest, signierte Einträge und versiegelte Berichte, geprüft gegen einen vertrauenswürdigen Schlüssel |
| Vergleichen Sie mit einem früheren gespeicherten Zustand | Bewahren Sie eine separate Referenzkopie oder einen Hash auf | Signierte Kontrollpunkte, ein separater Zeuge und optionale externe Zeitstempel |

Der Vergleich beruht auf dem [Exportcode von Telegram Desktop](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) mit Stand 2. November 2026.

## Eine Nachricht, drei Beobachtungen

Eine neue Nachricht, eine Bearbeitung und eine Löschung werden drei getrennte Einträge. Die Bearbeitung überschreibt den ersten nicht, die Löschung entfernt ihn nicht.

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

Telegram sagt nicht, wer eine Nachricht gelöscht hat oder wann genau. TgWitness lässt diese Felder leer, statt zu raten.

## Ändern Sie einen Datensatz. Folgen Sie dem Hash.

Jeder Eintrag enthält den Hash des vorherigen. Ein anderswo aufbewahrter Prüfpunkt hält Journallänge und letzten Hash fest.

02 / HASH-CHAIN-SANDBOXEchtes SHA-256 · Beispieldatensätze

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

**C** sind die neun Ereignisfelder als UTF-8-JSON: sortierte Schlüssel, kein zusätzlicher Leerraum, kein ASCII-Escaping, kein NaN/Unendlich. `previous_hash` ist hi−1, h0 sind 64 Nullen, Signaturen decken die 32 Rohbytes des Digests ab.

Die Felder: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. Vollständige Spezifikation: [Ereigniskodierung](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#event-canonicalization).

BEIBEHALTENER PRÜFPUNKT

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Prüfen Sie die Signatur des Prüfpunkts gegen den festgelegten Schlüssel und vergleichen Sie ihn dann mit dem Journal. Ein späterer Export darf länger sein, muss aber am Prüfpunkt übereinstimmen.

## Drei Fragen, drei verschiedene Überprüfungen

[01 / INTEGRITÄT**Hat sich dieser Eintrag geändert?** Hashes und Signaturen gegen einen Schlüssel, dem Sie vertrauen.](https://phishdestroy.github.io/TgWitness/de/docs/exports/)[02 / KONTINUITÄT**Was wurde zuvor beibehalten?** Vergleichen Sie den Export mit Prüfpunkten, die ein Zeuge aufbewahrt hat.](https://phishdestroy.github.io/TgWitness/de/docs/witness/)[03 / LIEFERUNG**Sind diese Testereignisse eingegangen?** Senden, bearbeiten und löschen Sie Testnachrichten und sehen Sie, was jedes Konto erfasst hat.](https://phishdestroy.github.io/TgWitness/de/docs/cases/)

Signaturen beantworten „wurde es geändert?“, Prüfpunkte „passt es zu dem, was vorher da war?“, Testnachrichten „haben wir alles erfasst?“. [Was die Prüfung beweist und was nicht.](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope)

Weiter: eine [Untersuchung des ganzen Kontos](https://phishdestroy.github.io/TgWitness/de/docs/cases/) vom Start bis zum Fallpaket.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
