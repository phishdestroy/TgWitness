# Untersuchungen über alle Chats hinweg

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/cases/

Bearbeiten Sie einen gesamten Fall über Kanäle, Gruppen, private Chats und Bots hinweg: Sammeln, verknüpfen, rekonstruieren und übergeben Sie die Beweismittel.

Diese Schritt-für-Schritt-Anleitung verfolgt einen fiktiven Vorfall über den gesamten Verlauf hinweg. Nutzen Sie die Funktionen „Erfassung“, „Suche“ und „Personenprofile“, um die Quelldatensätze zu finden, [das „Case Board“](https://phishdestroy.github.io/TgWitness/de/docs/case-board/), um diese zu organisieren und zu besprechen, sowie [das „Report Studio“](https://phishdestroy.github.io/TgWitness/de/docs/reports/), um die Ergebnisse zu präsentieren. Die untenstehende illustrierte Übersicht verdeutlicht die Zusammenhänge in diesem Beispiel.

BEARBEITETER FALL / EINE GEÄNDERTE ZAHLUNGSADRESSE

### Ein Vorfall. Vier Unterhaltungen. Eine Spur, die es zu rekonstruieren gilt.

Eine Kanalankündigung verweist auf einen Bot. Eine Einsatzgruppe bespricht einen neuen Zahlungslink, und der Bot zeigt ihn an. Die Ankündigung wird bearbeitet, in einer privaten Folge-Nachricht wird das Ziel erneut genannt, und eine Gruppennachricht verschwindet.

Wer hat die jeweilige Version gepostet?Wo ist der Link erschienen?Welche Datei wurde gesichert?Was hat sich geändert und wann?

Informationen zum Laden des Verlaufs, zur optionalen Überprüfung durch KI, zu MCP, OCR und ausgehenden Webhooks finden Sie unter [„Das Archiv bearbeiten](https://phishdestroy.github.io/TgWitness/de/docs/archive/)“.

## 1. Erfassen Sie den gesamten Account

Verwenden Sie ein spezielles Erfassungskonto für den gesamten Kontenumfang. Hauptkonten können ausgewählte Chats oder einen Telegram-Ordner erfassen.

1. [Verbinden Sie das Erfassungskonto](https://phishdestroy.github.io/TgWitness/de/docs/accounts/) in einem eigenen Arbeitsbereich. Halten Sie die Fallreferenz, die Konto-ID, den Namen des Arbeitsbereichs und den Fingerabdruck des Signaturschlüssels in Ihren Fallnotizen fest.
2. Open **Sources → Beobachtungsumfang → Untersuchungsmodus**. Überprüfen Sie **„Gesamtes Konto“**, alle vier Quelltypen und **„Eigene Aktionen**“. Mit dieser Voreinstellung können Sie das Profil einer neuen Quelle sowie deren letzte **200 sichtbare Nachrichten** speichern. Klicken Sie auf **„Umfang speichern“** und schließen Sie die Bestätigung des Umfangs ab.
3. Klicken Sie auf **„Chats laden**“. Vergleichen Sie die Quellen mit der Dialogliste des Kontos und überprüfen Sie die Ausschlüsse. Passen Sie unter **„Parameter“ → „Aus der Kontoliste gelesene Chats“** bei Bedarf das anfängliche Listenlimit an: Die Standardeinstellung beträgt 1.000 Dialoge, konfigurierbar bis zu 20.000. Chats, die über das Limit hinausgehen, werden erkannt, sobald sie aktiv werden.
4. Wählen Sie in **den Aufzeichnungseinstellungen** die **Option „Alle sichtbaren Aktivitäten**“ aus und speichern Sie die Einstellung. Überprüfen Sie die Dateitypen für Anhänge, die Größenbeschränkungen und den verfügbaren Speicherplatz. Starten Sie die Überwachung und validieren Sie eine kontrollierte Nachricht sowie Bearbeitungen und Löschungen, bevor Sie sich auf die Konfiguration verlassen.

KanäleGruppenPrivate ChatsBots

EIN KONTO / EIN SIGNATURSCHLÜSSEL**Alle ausgewählten, für das Konto sichtbaren Aktivitäten → ein Protokoll**

Nachrichten · Bearbeitungen · Löschhinweise · sichtbare Reaktionen · Mitgliederereignisse · eigene Aktionen

„Gesamtes Konto“ umfasst die Chats, auf die dieses Konto zugreifen kann, einschließlich der konfigurierten Quelltypen und Ausschlüsse. Geheime Chats sind nicht verfügbar. Neue Dialoge werden hinzugefügt, sobald Aktualisierungen eintreffen; die Aktivierung dieses Modus führt nicht automatisch zum Herunterladen des vollständigen alten Verlaufs jedes bestehenden Chats.

## 2. Verlauf erfassen und Dateien sichern

Erstellen Sie eine „Case Board“-Sammlung für die Untersuchung und setzen Sie Lesezeichen für die relevanten gespeicherten Datensätze. Führen Sie parallel zum Fall ein Quellenregister: numerische ID jedes Chats, Titel, Erfassungskonto, Zugriffsberechtigung/Rolle, Startzeitpunkt, Erfassung des Verlaufs, Medienergebnis und bekannte Lücken. Markieren Sie eine Quelle nach Überprüfung des entsprechenden Ergebnisses als erfasst.

| Anforderungen | Aktivität im Panel | Was es bietet |
| --- | --- | --- |
| Verlauf aller aktivierten Chats | Quellen → Vollständigen Verlauf laden | Verfügbare frühere Nachrichten werden in das Arbeitsbereichsprotokoll aufgenommen, mit den Funktionen „Pause/Fortsetzen“ und einem signierten Fortschrittsbericht. [Anleitung zur Verlaufsanzeige](https://phishdestroy.github.io/TgWitness/de/docs/reference/history/). |
| Bestehender Chat-Kontext im Protokoll | Quellen → Aufzeichnungseinstellungen → Verlaufs-Snapshot | Zuletzt sichtbare Nachrichten als signierte Beobachtungen. Standardmäßig maximal 500; unter **„Parameter“ → „Größter Verlaufssnapshot“** kann dieser Wert auf bis zu 10.000 erhöht werden. |
| Vollständiger, derzeit sichtbarer Verlauf eines Chats | Gesamten Chat exportieren → Gesamten Chat exportieren oder Chats → Chat exportieren | Ein separates signiertes Bundle mit „`chat.json`“ und „`chat.html`“. Wiederholen Sie diesen Vorgang für jede Quelle; bewahren Sie die Ergebnisse bezüglich Erfolg oder Misserfolg auf. |
| Kontext beim Erscheinen eines neuen Chats | Beobachtungsumfang → Wenn ein neuer Chat oder Bot erscheint | Ein Quellenprofil und bis zu 1.000 zuletzt sichtbare Nachrichten; im Untersuchungsmodus werden 200 ausgewählt. Bestehende Chats werden nicht rückwirkend erfasst. |
| Anhangsgröße | Sichtbare Anhänge herunterladen + Begrenzungen pro Dateityp | Überprüfen Sie die Angabe „`media.saved`“, den SHA-256-Hashwert und die Byte-Anzahl. Ein in der Warteschlange befindlicher, übersprungener oder fehlgeschlagener Download gilt nicht als erhaltene Datei. |

Ein vollständiger Chat-Export ist ein separater Snapshot; dabei wird nicht der gesamte Verlauf in das Protokoll oder die Personenprofile importiert. Verwenden Sie**„Gesamten Verlauf** aus aktivierten Quellen **laden**“ oder begrenzte Protokoll-Snapshots für historisches Material, das Sie innerhalb von TgWitness durchsuchen müssen. Überprüfen Sie die Quellenliste, bevor Sie den Vorgang starten.

Im vorliegenden Fall erfassen Sie den Ankündigungskanal, die Arbeitsgruppe, die Bot-Konversation und die private Nachverfolgung. Bewahren Sie die Bytes und den Hash des Rechnungsanhangs auf. Mit den heute verfügbaren Verlaufsdaten lassen sich weder eine vor der Erfassung gelöschte Nachricht noch eine zwischenzeitliche Bearbeitung rekonstruieren, die Telegram nicht mehr zurückgibt.

## 3. Behalten Sie den Verlauf der Unterhaltung und Ihre eigenen Handlungen im Blick

Halten Sie die Überwachung aufrecht, während sich der Fall weiterentwickelt. Markieren Sie die aktiven Fall-Chats als vorrangige Quellen mit einem Stern; konfigurieren Sie die Nachprüfungen für vorrangige und andere Quellen unter **„Aufzeichnungseinstellungen“ → „Nachprüfung**“. Überprüfen Sie im Verlauf der Arbeit die Werte für „`recheck.completed`“, „fortlaufendes Nachholen“, „FloodWait“ und die Medienergebnisse.

Verwenden Sie **„Chats“ → „Profil“ → „Profil jetzt speichern“,** um die aktuellen Quellenbeschreibungen, Bot-Befehle und andere von Telegram zurückgegebenen Metadaten beizubehalten. Dieses Quellenprofil ist unabhängig von den Personenprofilen, die aus den Protokollnachrichten erstellt werden.

**Ein Bot oder eine Einladung im Rahmen des Falles folgen**

1. Gehen Sie zu **„Chats“ → „Telegram-Link öffnen**“ und speichern Sie zunächst die Vorschau. Der ursprüngliche Link und die angezeigte Vorschau werden zu signierten Datensätzen.
2. Falls es die Untersuchung erfordert, **führt der Befehl „Join / open“** den Beitritt oder das Öffnen der Quelle **durch** und startet einen Bot mit dem angegebenen Startparameter. Eine ausstehende Beitrittsanfrage bleibt im Protokoll als ausstehend vermerkt.
3. Verwenden Sie für eine Aktion, die Sie dokumentieren möchten, die Textantwort des Bedienfelds oder **die** unterstützte **Schaltfläche „Drücken**“. Das Protokoll speichert `interaction.requested` und `interaction.result`, einschließlich des zurückgegebenen Callback-Textes oder der URL.

Diese Steuerelemente führen echte Telegram-Aktionen aus. Ein in einer anderen Telegram-App gedrückter Rückruf ist für den Erfasser nicht sichtbar; die nachfolgende Nachricht oder Bearbeitung des Bots möglicherweise schon. Web-Apps, Zahlungen sowie Telefon- und Standortabfragen liegen außerhalb des Mini-Clients.

## 4. Verfolgen Sie Personen, Links und Dateien über Chats hinweg

1. Öffnen Sie **das Journal**, lassen Sie den Quellenfilter auf **„Alle Quellen“** eingestellt und suchen Sie nach einer bestimmten Phrase, einer Domain, einem Benutzernamen oder einer gespeicherten Kennung. Öffnen Sie jeden treffenden Datensatz und wählen Sie dann **„Zum Board hinzufügen“**, um den Chat, die Nachrichten-ID und den Journalverweis im Fall zu speichern.
2. Um einen relevanten Chat aufzurufen, öffnen Sie **„Chats“ → „Personen“ → „Profile aktivieren“** und wählen Sie anschließend eine Person aus. Überprüfen Sie den Verlauf von Namen/Benutzernamen, Antwortbeziehungen, Aktivitäten sowie **„Auch in…“ –** weitere beobachtete Chats und extrahierte Links, Wallets oder Telefonnummern. Öffnen Sie die zitierten Protokollaufzeichnungen.
3. Verfolgen Sie dieselbe numerische Telegram-Benutzer-ID in anderen Chats innerhalb dieses Arbeitsbereichs. Behandeln Sie einen übereinstimmenden Namen, eine Erwähnung der Wallet oder einen ähnlichen Avatar als Hinweis, den es zu überprüfen gilt; behalten Sie die Quellenangaben und alle unterstützenden Zuordnungen bei.
4. Vergleichen Sie die SHA-256-Werte der gespeicherten Anhänge über verschiedene Datensätze hinweg. Übereinstimmende Hash-Werte bestätigen die Byte-Identität der gespeicherten Dateien. Prüfen Sie die zugehörigen Nachrichten- und Absenderdatensätze, bevor Sie Rückschlüsse darauf ziehen, wer diese geteilt hat.

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
| Gleicher Telegram-Account | Benutzer-ID 71001 in der Gruppe #146 und im privaten Chat #205 | In beiden Chats wurde dieselbe Absender-ID angegeben. Die tatsächliche Identität bleibt eine separate Frage. |
| Wiederholtes Ziel | `pay.example.invalid/new` in #146, Metadaten der Schaltfläche #173, bearbeitete Beiträge #188 und #205 | Das gleiche Ziel taucht in vier beobachteten Kontexten auf. Ordnen Sie dessen Steuerung anhand zusätzlicher Quellen zu. |
| Gleiche Dateigröße | Identische vollständige SHA-256-Werte in den abgeschlossenen Medienbelegen Nr. 151 und Nr. 209 | Die beiden gesicherten Anhänge sind byteweise identisch. Die vollständigen Datei-Hashes dienen als Vergleichsgrundlage. |

Personenprofile beschreiben beobachtete Autoren und deren Aktivitäten im *Journal* *desselben Arbeitsbereichs* innerhalb der für den Betrachter zugelassenen Chats. Es handelt sich hierbei um eine Ansicht der beobachteten Autoren und nicht um ein vollständiges Mitgliederverzeichnis. Passen Sie die Anzahl der unterstützenden Zitate unter **„Parameter“ → „Pro Fakt zitierte Datensätze**“ an.

## 5. Rekonstruieren Sie die Abfolge und markieren Sie die Lücken

Überprüfen Sie im Bereich **„Chats**“ die gespeicherten Versionen und die dazugehörigen Links **„Journal-Eintrag Nr. …**“. Nutzen Sie im Bereich **„Journal**“ die Optionen **„Alle Quellen**“ sowie **„Bearbeitungen“**, **„Löschungen“** und **„Erfassungsbereich**“. Erstellen Sie eine Zeitleiste des Falls unter Berücksichtigung sowohl des von Telegram angegebenen Datums als auch des Erfassungszeitpunkts des Erfassers.

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

Die Reihenfolge im Protokoll richtet sich nach dem Eingangszeitpunkt, nicht unbedingt nach den ursprünglichen Telegram-Aktionen. Ein älterer Verlaufs-Snapshot kann nach einer neueren Live-Nachricht eintreffen. Unterscheiden Sie klar zwischen Live-Beobachtungen, Snapshots, wiederhergestellten Nachrichten, Löschmeldungen und „bei erneuter Überprüfung fehlenden“ Einträgen. Fügen Sie an jeder Stelle, an der die Erfassung eine Lücke aufweist, ausdrücklich ein unbekanntes Intervall hinzu; ein späterer Snapshot löscht diese Lücke nicht aus.

## 6. Erweitern Sie den Fall auf andere Sammelkonten

Fügen Sie für jedes einzelne Konto einen Arbeitsbereich hinzu und wiederholen Sie die Erfassung des Umfangs und des Verlaufs. Erfassen Sie für jedes Konto die Mitgliedschaft/Rolle sowie den Fingerabdruck des Signaturschlüssels. Halten Sie Identifikatoren nach Arbeitsbereich und Chat qualifiziert: Die gleiche Nachrichtennummer ist kein globaler, kontoübergreifender Identifikator.

Verwenden Sie eine [Kontengruppe](https://phishdestroy.github.io/TgWitness/de/docs/groups/), um den Betriebsstatus zu überprüfen, ausgewählte Einstellungen zu teilen und die Konten gemeinsam zu exportieren. Das Gruppenpaket bewahrt das signierte Protokoll und die Identität jedes Arbeitsbereichs. Für einen Kanal oder eine Supergruppe können berechtigte Konten auch einen vollständigen Verlaufsexport aufteilen. Erstellen Sie eine kontenübergreifende Zeitleiste in Ihren Fallnotizen oder Analysewerkzeugen und behalten Sie dabei die Arbeitsbereichs- und Protokollreferenz für jede Zeile bei.

Fügen Sie bei länger andauernden Arbeiten einen [unabhängigen Zeugen](https://phishdestroy.github.io/TgWitness/de/docs/witness/) hinzu, um frühere Abgrenzungen beizubehalten. Nutzen Sie das Pilotprojekt zur kontrollierten Zustellung, um die Erfassungswege und die Sichtbarkeit der Konten zu überprüfen.

## 7. Ein überprüfbares Fallpaket liefern

Exportieren Sie aus jedem Arbeitsbereich eine ZIP-Datei mit dem signierten Protokoll. Diese enthält das vollständige aufgezeichnete Protokoll, unabhängig von den Suchfiltern im Bedienfeld. Exportieren Sie relevante Personenprofile separat, bewahren Sie jedes vollständige Chat-Verlaufsbündel auf und sichern Sie die vollständigen Anhangsnachweise.

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

Bewahren Sie vertrauenswürdige Fingerabdrücke über einen separaten Kanal auf. Überprüfen Sie von einer vertrauenswürdigen Installation aus jedes Artefakt anhand seiner eigenen Arbeitsbereichs-Identität:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Überprüfen Sie die Ergebnisse der Verifizierung, bewahren Sie die Originale auf und fügen Sie Ihren Ergebnissen den Abdeckungsbericht, die Erfassungsergebnisse und das Übertragungsprotokoll bei. Verfassen Sie Ihre Ergebnisse in „Report Studio“ und entscheiden Sie, ob der Bericht Material aus dem „Case Board“ enthalten soll. Der Beispielordner auf oberster Ebene fasst die einzelnen signierten Artefakte zusammen. Für Empfänger, die nur ausgewähltes Material benötigen, bereiten Sie eine [reduzierte Übergabe](https://phishdestroy.github.io/TgWitness/de/docs/handover/) vor.

## Wenden Sie dieselbe Methode auch bei anderen Ermittlungen an

**Ein durch einen Bot ausgelöster Streitfall bezüglich einer Bestellung oder Zahlung**

**Frage:** Was hat der Bot versprochen, welche Zieladresse wurde für die Schaltfläche angegeben und was hat sich danach geändert?

**Ablauf:** Beitrag im Kanal → gespeicherte Vorschau des Bot-Links → Startparameter des Bots → Nachrichten und Tastatureingaben → etwaige vom Panel ausgestellte Rückrufbestätigungen → weitere Nachrichten in Gruppen oder privaten Chats. Ordnen Sie jedes Ziel dem entsprechenden Quelldatensatz zu; behalten Sie Profilbeschreibungen und angehängte Medien bei.

**Liefern Sie:** eine Zeitleiste der beobachteten Angebote und Antworten, die Quellenangaben und die verifizierten Exporte. Untermauern Sie jede Behauptung bezüglich einer abgeschlossenen Zahlung mit den entsprechenden Transaktionsbelegen.

**Nach einem „Cross-Chat“-Vorfall gelöschte Nachrichten**

**Frage:** Was war bereits zu beobachten gewesen, bevor die relevanten Nachrichten verschwanden?

**Nachverfolgung:** alle betroffenen Chats → Originalnachrichten → übermittelte Bearbeitungen → Löschmeldungen oder spätere Ergebnisse, bei denen bei erneuter Überprüfung ein Fehlen festgestellt wurde → erhaltene Anhänge → Berichterstattung rund um den Vorfall. Vergleichen Sie Beobachtungen unabhängiger Konten mit deren angegebenen Sichtbarkeitsstatus.

**Zu liefern sind:** eine Abfolge von gesicherten Versionen und explizit gekennzeichnete unbekannte Zeiträume. Löschhinweise, erfolglose Nachprüfungen und jegliche Zuordnung zu einer Person sind separat zu dokumentieren.

**Ein Teilnehmer wechselt in mehreren Chats seinen Namen**

**Frage:** Welche beobachtete Aktivität gehört trotz wechselnder Namen zum selben Telegram-Konto?

**Nachverfolgung:** numerische Absender-ID → gespeicherte Namen/Benutzernamen-Historie → Antworten → weitere Chats im Arbeitsbereich → erwähnte Ziele und gespeicherte Dateien. Überprüfen Sie die Quelldatensätze für jede behauptete Verbindung; halten Sie ähnlich klingende Konten getrennt.

**Ergebnis:** eine zitierte Zeitleiste der Kontoaktivitäten und separate Hypothesen zu Zusammenhängen. Nutzen Sie Namensähnlichkeiten und den Avatar-pHash, um Anhaltspunkte für die weitere Überprüfung von Quellen auszuwählen.
