# Telegram · Untersuchungen über alle Chats hinweg

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/cases/

Ein ganzer Fall über Kanäle, Gruppen, private Chats und Bots: erfassen, verknüpfen, die Zeitleiste rekonstruieren, übergeben.

Ein erfundener Vorfall von Anfang bis Ende. Erfassung, Suche und Personenprofile finden die Einträge, [Case Board](https://phishdestroy.github.io/TgWitness/de/docs/case-board/) ordnet sie, [Report studio](https://phishdestroy.github.io/TgWitness/de/docs/reports/) präsentiert sie.

BEARBEITETER FALL / EINE GEÄNDERTE ZAHLUNGSADRESSE

### Ein Vorfall. Vier Unterhaltungen. Eine Spur, die es zu rekonstruieren gilt.

Ein Kanalbeitrag verweist auf einen Bot. Eine Gruppe spricht über einen neuen Zahlungslink, der Bot zeigt ihn an. Der Beitrag wird bearbeitet, ein privater Chat wiederholt den Link, eine Gruppennachricht verschwindet.

Wer hat die jeweilige Version gepostet?Wo ist der Link erschienen?Welche Datei wurde gesichert?Was hat sich geändert und wann?

Verlauf laden, KI, MCP, OCR und Webhooks: [Mit dem Archiv arbeiten](https://phishdestroy.github.io/TgWitness/de/docs/archive/).

## 1. Erfassen Sie den gesamten Account

Umfang „ganzes Konto“ nur auf einem eigenen Konto. Ein Hauptkonto bekommt ausgewählte Chats oder einen Ordner.

1. [Verbinden Sie das Konto](https://phishdestroy.github.io/TgWitness/de/docs/accounts/) in einem eigenen Arbeitsbereich. Notieren Sie Fallreferenz, Konto-ID, Arbeitsbereich und Schlüssel-Fingerabdruck.
2. **Quellen → Beobachtungsumfang → Ermittlungsmodus**: **Ganzes Konto**, alle vier Quellentypen, **Eigene Aktionen**. Jeder neue Chat bekommt Profil und die letzten **200 sichtbaren Nachrichten** gespeichert. **Umfang speichern** und bestätigen.
3. **Chats laden** und mit der Chatliste des Kontos vergleichen. Das Limit liegt bei 1.000 Dialogen (bis 20.000 unter **Parameter → Aus der Kontoliste gelesene Chats**); Chats darüber hinaus tauchen auf, sobald sie aktiv werden.
4. **Aufzeichnungseinstellungen** → **Alle sichtbaren Aktivitäten**, Anhangslimits und Speicherplatz prüfen. Starten, dann mit einer Nachricht, einer Bearbeitung und einer Löschung testen.

KanäleGruppenPrivate ChatsBots

EIN KONTO / EIN SIGNATURSCHLÜSSEL**Alle ausgewählten, für das Konto sichtbaren Aktivitäten → ein Protokoll**

Nachrichten · Bearbeitungen · Löschhinweise · sichtbare Reaktionen · Mitgliederereignisse · eigene Aktionen

„Ganzes Konto“ heißt jeder Chat, den dieses Konto öffnen kann, abzüglich Ausschlüssen. Keine geheimen Chats. Neue Chats kommen hinzu, sobald sie auftauchen; alter Verlauf wird nicht automatisch geladen.

## 2. Verlauf erfassen und Dateien sichern

Legen Sie eine Case-Board-Sammlung an und markieren Sie, was wichtig ist. Führen Sie ein Quellenregister: Chat-ID, Titel, Konto, Rolle, Beginn der Live-Erfassung, Verlaufsergebnis, Medienergebnis, Lücken.

| Anforderungen | Aktivität im Panel | Was es bietet |
| --- | --- | --- |
| Verlauf aller aktivierten Chats | Quellen → Vollständigen Verlauf laden | Verfügbare frühere Nachrichten werden in das Arbeitsbereichsprotokoll aufgenommen, mit den Funktionen „Pause/Fortsetzen“ und einem signierten Fortschrittsbericht. [Anleitung zur Verlaufsanzeige](https://phishdestroy.github.io/TgWitness/de/docs/reference/history/). |
| Bestehender Chat-Kontext im Protokoll | Quellen → Aufzeichnungseinstellungen → Verlaufs-Snapshot | Aktuelle Nachrichten als signierte Einträge. Standard 500, bis 10.000 unter **Parameter → Größter Verlaufs-Snapshot**. |
| Vollständiger, derzeit sichtbarer Verlauf eines Chats | Gesamten Chat exportieren → Gesamten Chat exportieren oder Chats → Chat exportieren | Ein separates signiertes Paket mit `chat.json` und `chat.html`, eines pro Chat. |
| Kontext beim Erscheinen eines neuen Chats | Beobachtungsumfang → Wenn ein neuer Chat oder Bot erscheint | Sein Profil und bis zu 1.000 aktuelle Nachrichten (200 im Ermittlungsmodus). Gilt nicht für bestehende Chats. |
| Anhangsgröße | Sichtbare Anhänge herunterladen + Begrenzungen pro Dateityp | Achten Sie auf `media.saved` mit SHA-256 und Größe. In der Warteschlange, übersprungen oder fehlgeschlagen heißt nicht gespeichert. |

Ein Chat-Export landet nicht im Journal oder in Personenprofilen. Um alten Verlauf in TgWitness zu durchsuchen, nehmen Sie **Gesamten Verlauf laden** oder Snapshots.

Hier: der Kanal, die Gruppe, der Bot-Chat und der private Chat, dazu die Rechnungsdatei und ihr Hash. Was vor der Erfassung gelöscht wurde, ist weg.

## 3. Behalten Sie den Verlauf der Unterhaltung und Ihre eigenen Handlungen im Blick

Lassen Sie es laufen. Markieren Sie die heißen Chats mit Stern als Priorität, stellen Sie Nachprüfungen unter **Aufzeichnungseinstellungen → Nachprüfung** ein und behalten Sie `recheck.completed`, FloodWait und Medienergebnisse im Blick.

**Chats → Profil → Profil jetzt speichern** speichert Chatbeschreibung, Bot-Befehle und weitere Metadaten.

**Ein Bot oder eine Einladung im Rahmen des Falles folgen**

1. **Chats → Telegram-Link öffnen**, zuerst die Vorschau speichern. Link und Vorschau werden signierte Einträge.
2. Falls nötig, tritt **Beitreten / öffnen und beobachten** dem Chat bei oder startet den Bot mit seinem Startparameter.
3. Um eine Aktion zu dokumentieren, antworten Sie oder nutzen Sie **Button drücken** im Panel. Sie bekommen `interaction.requested` und `interaction.result` mit der Antwort des Bots.

Das sind echte Aktionen. In einer anderen App gedrückte Buttons sind nicht sichtbar, nur die Antwort des Bots. Keine Web-Apps, Zahlungen oder Telefon/Standort.

## 4. Verfolgen Sie Personen, Links und Dateien über Chats hinweg

1. **Journal**, **Alle Quellen**, suchen Sie eine Phrase, Domain oder einen Benutzernamen. Öffnen Sie Treffer und schicken Sie sie **Aufs Board**.
2. **Chats → Personen → Profile einschalten**, wählen Sie eine Person: Namensverlauf, Antworten, Aktivität, **Auch in…**, Links, Wallets, Telefone. Öffnen Sie die zitierten Einträge.
3. Verfolgen Sie dieselbe numerische Benutzer-ID in andere Chats. Ein passender Name, eine Wallet oder ein Avatar ist ein Hinweis, kein Beweis.
4. Vergleichen Sie Datei-Hashes. Gleicher SHA-256 = gleiche Bytes. Wer sie geteilt hat, ist eine andere Frage.

FALLÜBERSICHT / VERWEISEN VERFOLGENFiktiver Fall · keine Echtzeit-Grafik

KANAL / ANKÜNDIGUNG**Original → bearbeitete Zielversion**

Einträge Nr. 101, Nr. 188, Nachricht Nr. 84 · Absender nicht zugeordnet

GRUPPE / EINSÄTZE**Benutzer 71001 veröffentlicht den neuen Link**

Eintrag Nr. 146 · Nachricht Nr. 309 · Gespeicherte Empfangsbestätigung Nr. 151

BOT / BESTELLUNGSGESPRÄCH**Eine Schaltfläche führt zu dieser Seite**

Eintrag Nr. 173 · Nachricht Nr. 12 Metadaten der „Zurück“-Schaltfläche

PRIVAT / WEITERFÜHRUNG**Benutzer 71001 wiederholt das Ziel**

Eintrag Nr. 205 · Nachricht Nr. 922 · Speicherbestätigung Nr. 209

Vier Chats liefern unterschiedliche Beobachtungen. Verfolgen Sie die Quelldatensätze für jede Verbindung; der Kanalbeitrag hat keinen zuordenbaren Absender.

Die numerischen IDs und Datensatzreferenzen wurden für diese Anleitung fiktiv erstellt. Diese übersichtliche Darstellung zeigt, wie Suchergebnisse, Profile und geprüfte Datensätze miteinander verknüpft werden; das „Case Board“ speichert die entsprechenden Karten und Quellenangaben.

| Zusammenhang | Unterstützende Anmerkung | Fazit: Beibehalten |
| --- | --- | --- |
| Gleicher Telegram-Account | Benutzer-ID 71001 in der Gruppe #146 und im privaten Chat #205 | Dieselbe Absender-ID in beiden Chats. Wer das im echten Leben ist, ist eine andere Frage. |
| Wiederholtes Ziel | `pay.example.invalid/new` in #146, Metadaten der Schaltfläche #173, bearbeitete Beiträge #188 und #205 | Derselbe Link an vier Stellen. Wer ihn kontrolliert, braucht andere Quellen. |
| Gleiche Dateigröße | Identische vollständige SHA-256-Werte in den abgeschlossenen Medienbelegen Nr. 151 und Nr. 209 | Beide Dateien sind byte-identisch. |

Profile umfassen nur Personen, die in *diesem Arbeitsbereich* etwas geschrieben haben, keine Mitgliederliste. Zitate pro Fakt: **Parameter → Zitierte Einträge pro Fakt**.

## 5. Rekonstruieren Sie die Abfolge und markieren Sie die Lücken

Versionen in **Chats**, dann **Journal** mit **Alle Quellen** + **Bearbeitungen**, **Löschungen**, **Abdeckung**. Beide Zeiten in die Zeitleiste: Telegrams Datum und wann es beobachtet wurde.

1. 09:00 · #101**Erfasster Kanalbeitrag**

   Das ursprüngliche Ziel bleibt erhalten.
2. 09:12 · #146 / #151**Die Gruppe fügt einen anderen Link hinzu**

   Benutzer 71001 veröffentlicht den Beitrag; der Download eines Anhangs wird abgeschlossen.
3. 09:16 · #173**Der Bot zeigt denselben Zielort an**

   Die gespeicherten Tastatur-Metadaten enthalten den Link.
4. 09:20 · #188**Änderungen bei den Kanalankündigungen**

   Sowohl die ursprünglichen als auch die bearbeiteten Einträge bleiben erhalten.
5. 09:24 · #205 / #209**In einer privaten Folge wird dies wiederholt**

   Der gespeicherte Anhang weist denselben vollständigen SHA-256-Hashwert wie #151 auf.
6. 09:28 · #231**Benachrichtigung über die Löschung einer Gruppe geht ein**

   Die frühere Feststellung gilt weiterhin: Weder der Verfasser der Löschung noch ein genauer Zeitpunkt der Löschung werden angegeben.

Beispielhafte Beobachtungszeitpunkte und Verweise. Zwischen diesen Einträgen befinden sich weitere Protokollaufzeichnungen.

Die Journalreihenfolge ist die Eingangsreihenfolge, nicht unbedingt die Reihenfolge der Ereignisse. Halten Sie Live-Einträge, Snapshots, wiederhergestellte Nachrichten, Löschungen und „bei Nachprüfung nicht gefunden“ auseinander und markieren Sie jede Lücke als unbekannt.

## 6. Erweitern Sie den Fall auf andere Sammelkonten

Ein Arbeitsbereich pro Konto, gleiche Schritte. Notieren Sie Rolle und Fingerabdruck von jedem. Nachrichtennummern gelten pro Konto, also immer Arbeitsbereich und Chat angeben.

Eine [Kontogruppe](https://phishdestroy.github.io/TgWitness/de/docs/groups/) zeigt den Status, teilt Einstellungen und exportiert alle zusammen, jeweils mit eigenem Journal und Schlüssel. Eine kontenübergreifende Zeitleiste bauen Sie in Ihren Notizen.

Langer Fall? Fügen Sie einen [unabhängigen Zeugen](https://phishdestroy.github.io/TgWitness/de/docs/witness/) hinzu und testen Sie, was jedes Konto wirklich erfasst.

## 7. Ein überprüfbares Fallpaket liefern

Ein signiertes ZIP aus jedem Arbeitsbereich (immer das ganze Journal, Filter spielen keine Rolle), dazu Personenprofile, Chat-Exporte und Dateien.

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

Schicken Sie die Fingerabdrücke separat. Prüfen Sie alles gegen seinen eigenen Arbeitsbereich:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Bewahren Sie Prüfausgabe, Originale, Abdeckung und Übergabeprotokoll bei Ihren Ergebnissen auf. Schreiben Sie alles im Report studio zusammen. Braucht der Empfänger weniger, erstellen Sie eine [minimierte Übergabe](https://phishdestroy.github.io/TgWitness/de/docs/handover/).
