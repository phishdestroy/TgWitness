# Untersuchungsmodus

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/investigation/

Umfassende Untersuchungen ganzer Konten über Kanäle, Gruppen, private Chats und Bots hinweg – vom Untersuchungsumfang bis hin zu einem verifizierten Fallpaket.

Verfolgen Sie einen Fall über Kanäle, Gruppen, private Chats und Bots hinweg, von der ersten Erfassung bis hin zu einer zitierfähigen Zeitleiste und einer überprüfbaren Übergabe. Die interaktive Website-Version finden Sie unter `/docs/cases/`; [Anweisungen zur Vorschau](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

## Beispielfall: Eine Änderung des Zielortes über vier Unterhaltungen hinweg

Eine Ankündigung verweist auf einen Bot. Eine Einsatzgruppe bespricht ein neues Zahlungsziel, die Tastatur des Bots zeigt es an, und in einer privaten Folgenachricht wird es wiederholt. Die Ankündigung wird anschließend bearbeitet, und eine Gruppennachricht verschwindet.

Die Fragen lauten: Was wurde vor und nach der Änderung beobachtet, welche Telegram- Konten haben die einzelnen Einträge gepostet, wo erschien das Ziel, welche Bytes der Anhänge wurden erhalten und welche Zeitintervalle bleiben unbekannt?

Alle Namen, IDs, Zeitangaben und Verweise auf das Protokoll in diesem Beispiel sind fiktiv. Der Arbeitsablauf nutzt aktuelle Funktionen; die Fallübersicht dient lediglich der Veranschaulichung und ist kein automatischer , von der Anwendung generierter Graph.

Ablaufdiagramm · Kanäle → Arbeitsbereichsprotokoll; Gruppen → Arbeitsbereichsprotokoll; Private Chats → Arbeitsbereichsprotokoll; Bots → Arbeitsbereichsprotokoll; Arbeitsbereichsprotokoll → Alle Quellen durchsuchen; Arbeitsbereichsprotokoll → Personenprofile mit Verweisen auf die entsprechenden Aufzeichnungen; Arbeitsbereichsprotokoll → Gespeicherte Versionen und Empfangsbestätigungen für Anhänge; Alle Quellen durchsuchen → Chronologie der Analysten und Quellenverzeichnis; Personenprofile mit Verweisen auf die entsprechenden Aufzeichnungen → Chronologie der Analysten und Quellenverzeichnis; Gespeicherte Versionen und Empfangsbestätigungen für Anhänge → Chronologie der Analysten und Quellenverzeichnis; Arbeitsbereichsprotokoll → Signierte Beweisdatei im ZIP-Format; Chronologie der Analysten und Quellenverzeichnis → Fallübergabe mit separat verifizierten Beweismitteln; Signierte Beweisdatei im ZIP-Format → Fallübergabe mit separat verifizierten Beweismitteln · Kanäle · Gruppen · Private Chats · Bots · Arbeitsbereichsprotokoll · Alle Quellen durchsuchen · Personenprofile mitVerweisen auf dieentsprechendenAufzeichnungen · Gespeicherte Versionen undEmpfangsbestätigungen fürAnhänge · Signierte Beweisdatei imZIP-Format · Chronologie der Analystenund Quellenverzeichnis · Fallübergabe mit separatverifiziertenBeweismitteln

**Diagramm als Text**

1. Kanäle → Arbeitsbereichsprotokoll
2. Gruppen → Arbeitsbereichsprotokoll
3. Private Chats → Arbeitsbereichsprotokoll
4. Bots → Arbeitsbereichsprotokoll
5. Arbeitsbereichsprotokoll → Alle Quellen durchsuchen
6. Arbeitsbereichsprotokoll → Personenprofile mit Verweisen auf die entsprechenden Aufzeichnungen
7. Arbeitsbereichsprotokoll → Gespeicherte Versionen und Empfangsbestätigungen für Anhänge
8. Alle Quellen durchsuchen → Chronologie der Analysten und Quellenverzeichnis
9. Personenprofile mit Verweisen auf die entsprechenden Aufzeichnungen → Chronologie der Analysten und Quellenverzeichnis
10. Gespeicherte Versionen und Empfangsbestätigungen für Anhänge → Chronologie der Analysten und Quellenverzeichnis
11. Arbeitsbereichsprotokoll → Signierte Beweisdatei im ZIP-Format
12. Chronologie der Analysten und Quellenverzeichnis → Fallübergabe mit separat verifizierten Beweismitteln
13. Signierte Beweisdatei im ZIP-Format → Fallübergabe mit separat verifizierten Beweismitteln

## 1. Definieren Sie den Fall und erfassen Sie den gesamten Sachverhalt

1. Verbinden Sie das Erfassungskonto mit dem zugehörigen Arbeitsbereich. Halten Sie in externen Fallnotizen die Fallreferenz, die Konto-ID, den Arbeitsbereich, den Beginn der Beobachtung sowie den vertrauenswürdigen Fingerabdruck des Signaturschlüssels fest.
2. Open **Sources → Beobachtungsumfang → Untersuchungsmodus**. Die Voreinstellung umfasst **das gesamte Konto**, Kanäle/Gruppen/private Chats/Bots, eigene Aktionen, Quellenprofile sowie die letzten 200 sichtbaren Nachrichten für neu entdeckte Quellen. Überprüfen Sie die Angaben, klicken Sie auf **„Umfang speichern**“ und schließen Sie die Bestätigung des Umfangs ab.
3. **Laden Sie Chats** und vergleichen Sie die Quellen mit der Dialogliste des Kontos. Überprüfen Sie die Ausschlüsse. **Der Parameter „Chats, die aus der Liste des Kontos gelesen werden“** ist standardmäßig auf 1.000 eingestellt und erlaubt bis zu 20.000. Quellen, die über das Listenlimit hinausgehen, werden hinzugefügt, sobald sie aktiv werden. Zeichnen Sie auf, was tatsächlich erfasst wurde.
4. Wählen Sie in **den Aufzeichnungseinstellungen „Alle sichtbaren Aktivitäten**“ aus und speichern Sie die Überwachungseinstellungen. Überprüfen Sie die Anhangstypen/-beschränkungen sowie den freien Speicherplatz.
5. Beobachtung starten. Überprüfen Sie eine kontrollierte neue Nachricht, eine Bearbeitung und eine Löschung und speichern Sie anschließend die Testreferenzen sowie etwaige Fehler.

Der Erfassungsumfang für das gesamte Konto erfasst alle für das Konto sichtbaren Aktivitäten im Rahmen der gespeicherten Einstellungen. Es greift nicht auf geheime Chats zu und tritt auch nicht automatisch jeder verknüpften Gruppe bei. Außerdem werden nicht alle bestehenden Unterhaltungen nachträglich erfasst. Siehe [Erfassungsumfang](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account).

## 2. Erfassen Sie alle Quellen und ermitteln Sie den historischen Kontext

Führen Sie ein Quellenverzeichnis mit einer Zeile pro Chat:

| Fachgebiet | Aufzeichnen |
| --- | --- |
| Identität | Arbeitsbereich, Konto-ID, numerische Chat-ID, Titel und Typ |
| Sichtbarkeit | Mitgliedschaft/Rolle, bestätigter oder unbestätigter Zugriff, Ausschlüsse |
| Live-Erfassung | Startzeitpunkt, ausgewählte Ereignistypen und spätere Richtlinienänderungen |
| Verlauf des Protokolls | Angeforderte/fertiggestellte Momentaufnahmen, Begrenzung, Zeitangaben und Verweise auf Aufzeichnungen |
| Vollständiger Verlauf | Signierter Dateiname für den Export pro Chat, Begrenzung sowie Abschluss/Fehlschlag |
| Anhänge | Vollständige Medienbelege, Hashes, Dateigrößen sowie Ergebnisse zu übersprungenen bzw. fehlgeschlagenen Vorgängen |
| Umfang | Ausfälle, unvollständige Erfassung, „FloodWait“, nicht verfügbare Nachrichten und andere Lücken |

Verwenden Sie für jede Quelle die geeignete Erfassungsmethode:

- **„Vollständigen Verlauf** in **Quellen laden**“ (aktuell `main`) lädt verfügbare frühere Nachrichten aus aktivierten Quellen in das Arbeitsbereichsprotokoll. Die Funktion unterstützt das Anhalten/Fortsetzen sowie einen signierten Fortschrittsbericht. Siehe [Verlaufserfassung](https://phishdestroy.github.io/TgWitness/de/docs/reference/history/).
- **Der Verlaufs-Snapshot** speichert die zuletzt sichtbaren Nachrichten im Beobachtungsprotokoll. Der standardmäßige Höchstwert beträgt 500; unter **„Parameter → Größter Verlaufs-Snapshot“** kann dieser Wert auf 10.000 erhöht werden. Dabei handelt es sich um aktuelle Verlaufsbeobachtungen, nicht um rekonstruierte Bearbeitungen.
- **„Gesamten Chat exportieren“ → „Gesamten Chat exportieren**“ oder **„Chats“ → „Chat exportieren**“ ruft den derzeit sichtbaren Verlauf eines Chats in ein separates, signiertes `chat.json`-/ `chat.html`-Bundle ab. Wiederholen Sie diesen Vorgang für die Quellen des Falls und bewahren Sie jedes Ergebnis auf.
- **Wenn ein neuer Chat oder Bot erscheint,** können dessen Profil und bis zu 1.000 der letzten Nachrichten gespeichert werden; im Untersuchungsmodus werden 200 ausgewählt. Bestehende Chats erhalten diese Aufzeichnung nicht rückwirkend, wenn der Modus aktiviert wird.
- **Das Herunterladen sichtbarer Anhänge** bewahrt die Byte-Anzahl gemäß der konfigurierten Richtlinie. Erforderlich ist eine vollständige „`media.saved`“-Quittung mit SHA-256 und Byte-Angabe. Ein in der Warteschlange befindlicher Auftrag, eine Miniaturansicht oder ein Dateiname gilt nicht als bewahrter Anhang.

Ein vollständiger Chat-Export füllt das Protokoll oder die Personenprofile **nicht** mit allen darin enthaltenen Nachrichten. Verwenden Sie**„Vollständigen Verlauf laden“** oder begrenzte Protokoll-Snapshots für den Verlauf, den Sie innerhalb von TgWitness analysieren möchten. Überprüfen Sie die Liste der aktivierten Quellen, bevor Sie einen Verlaufslauf starten. Keine der beiden Methoden stellt Material wieder her, das Telegram nicht mehr zurückgibt.

## 3. Erfassung des sich entwickelnden Sachverhalts und der bewussten Interaktionen

Markieren Sie Chats zu aktiven Fällen als vorrangige Quellen. Überprüfen Sie die Intervalle für erneute Überprüfungen, die fortlaufende Nachverfolgung und die Ergebnisse der Medienauswertung. Lassen Sie den Collector während der Nutzung des Kontos weiter beobachten. Verwenden Sie **„Chats“ → „Profil“ → „Profil jetzt speichern“,** um Metadaten der Quelle wie Beschreibungen und Bot-Befehle zu erhalten. Dies ist unabhängig von Personenprofilen, die aus gespeicherten Nachrichten abgeleitet werden.

Wenn es in dem Fall darum geht, einer Quelle zu folgen oder mit einem Bot zu interagieren:

1. **Telegram-Link öffnen → „Vorschau speichern“** zeichnet den angegebenen Link und die angezeigte Vorschau vor einer Aktion auf.
2. **„Join / open and observe“** führt den Beitritt/das Öffnen durch und sendet den Startparameter eines Bots, sofern dieser angegeben wurde. Eine zur Genehmigung anstehende Beitrittsanfrage wird als „pending“ (ausstehend) protokolliert.
3. Vom Bedienfeld ausgegebene Textantworten und unterstützte Tastenbetätigungen behalten „ `interaction.requested`“ und „`interaction.result`“ bei. Rückrufbestätigungen können den zurückgegebenen Popup-Text, den Alarmstatus und die URL beibehalten.

Es handelt sich hierbei um echte Kontoaktivitäten. Callback-Aufrufe in einer anderen Telegram-App sind für den Erfasser nicht sichtbar, obwohl die daraus resultierenden Nachrichten oder Bearbeitungen möglicherweise sichtbar sind. Der Mini-Client führt keine Web-App-, Zahlungs-, Telefon- oder Standort-Workflows durch. Das genaue Verhalten entnehmen Sie bitte [den Panel-Interaktionen](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/#act-from-the-panel).

## 4. Verknüpfung von Beobachtungen über verschiedene Chats hinweg

Wählen Sie im **Protokoll „Alle Quellen**“ aus und durchsuchen Sie die aufgezeichneten Inhalte. Öffnen Sie die entsprechenden Einträge und notieren Sie sich den Arbeitsbereich, den Chat, die Nachrichten-ID, die Reihenfolge und den Datensatz-Hash.

Öffnen Sie in einem entsprechenden Chat **„Personen**“**→ „Profile aktivieren**“ und überprüfen Sie eine Person:

- Im Laufe der Zeit erfasste Namen/Benutzernamen sowie die numerische Telegram-ID.
- Antwortbeziehungen mit Verweisen auf die Quelldatensätze.
- **Ebenfalls enthalten sind …** andere Chats in diesem Arbeitsbereichsprotokoll, in denen diese ID geschrieben hat.
- Aktivitäten, Bearbeitungen/Löschungen sowie erwähnte Wallets, Telefone, Benutzernamen und Links.
- Gespeicherte Avatar-Metadaten und ähnliche zwischengespeicherte Avatare mit Angabe ihrer jeweiligen Herkunft.

Öffnen Sie die zitierten Datensätze, bevor Sie ein abgeleitetes Profil in einer Feststellung verwenden. Profile beziehen sich auf Personen mit gespeicherten Nachrichten, nicht auf jedes einzelne Gruppenmitglied. **Der Parameter „→ Datensätze pro Tatsache“** begrenzt die Referenzliste, nicht die Anzahl der zugrunde liegenden Aktivitäten. Erwähnungen und Ähnlichkeiten bei Avataren sind Anhaltspunkte; sie begründen weder Eigentumsverhältnisse noch Identität.

Im Beispiel:

| Link | Aufzeichnungen | Unterstützte Beobachtung |
| --- | --- | --- |
| Derselbe Absender-Account | Gruppe Nr. 146 und privater Folgebeitrag Nr. 205 | Beide geben die Telegram-Absender-ID 71001 an |
| Gleiche Zieladresse | #146, Bot-Tastatur #173, Kanalbearbeitung #188, private Nachricht #205 | Alle enthalten „`pay.example.invalid/new`“; Eigentumsverhältnisse bzw. Kontrollverhältnisse sind nicht geklärt. |
| Dieselbe gespeicherte Datei | Medienbelege Nr. 151 und Nr. 209 fertiggestellt | Die vollständigen SHA-256-Werte stimmen für die gespeicherten Bytes überein |
| Angabe der Kanalquelle | #101 und #188 | Ordnen Sie einen Kanalbeitrag nicht dem Nutzer 71001 zu, ohne dass ein Absender angegeben ist. |

Vergleichen Sie die Hashes der Anhänge und die zugehörigen Nachrichtenreferenzen. Identische Dateien lassen keine Rückschlüsse auf einen Ersteller, Weiterleiter oder gemeinsamen Betreiber zu. Gleiche Namen und ähnliche Avatare allein reichen nicht aus, um zwei Telegram-IDs einer Person zuzuordnen.

## 5. Erstellen Sie die chatübergreifende Zeitleiste

Verwenden Sie die gespeicherten Versionen in **Chats** und deren Links **zum Protokoll-Eintrag Nr. …** . Kombinieren Sie im **Protokoll alle Quellen** mit **Bearbeitungen**, **Löschungen** und **der Berichterstattung**. Behalten Sie sowohl `source_at`, sofern vorhanden, als auch `observed_at` bei.

| Beispielhafte Beobachtungsdauer | Referenz | Anmerkung |
| --- | --- | --- |
| 09:00 | Kanal #101 | Ursprüngliches Ziel erfasst |
| 09:12 | Gruppe #146; Medien #151 | Neues Ziel veröffentlicht; Dateidownload abgeschlossen |
| 09:16 | Bot Nr. 173 | Die Tastatur zeigt auf das neue Ziel |
| 09:20 | Kanal Nr. 188 | Ankündigung bearbeitet; beide gespeicherten Versionen bleiben erhalten |
| 09:24 | Privat #205; Medien #209 | Die gleiche Absender-ID wiederholt sich im Empfängerfeld; die gleichen Dateibyte bleiben erhalten |
| 09:28 | Gruppe Nr. 231 | Löschmeldung erhalten; Löschender und genauer Zeitpunkt der Löschung unbekannt |

Zwischen diesen Beispielverweisen liegen weitere Aufzeichnungen vor. Sequenznummern ordnen Beobachtungen; Verlaufs-Snapshots können ältere Quelldaten enthalten und später eintreffen als Live-Ereignisse. Unterscheiden Sie zwischen Snapshots, wiederhergestellten Nachrichten, Löschmeldungen und Ergebnissen, bei denen bei einer erneuten Überprüfung keine Daten mehr vorhanden sind. Kennzeichnen Sie Lücken in der Erfassung als unbekannte Intervalle. Eine spätere Erfassung von Verlaufsdaten begründet nicht rückwirkend eine lückenlose Beobachtung.

## 6. Fügen Sie Konto-Perspektiven hinzu, ohne deren Herkunft zu verlieren

Verwenden Sie für jedes einzelne Konto einen separaten Arbeitsbereich und wiederholen Sie dessen Bestandsaufnahme. Bewahren Sie bei jedem Vergleich die Konto-ID, die Rolle, den Fingerabdruck des Signaturschlüssels und die Quellenangaben auf. Nachrichtennummern sind keine globalen Identifikatoren, die über Chats und Konten hinweg gelten.

Die arbeitsbereichsübergreifende Korrelation erfolgt in externen Fallnotizen oder Analysewerkzeugen. TgWitness verfügt derzeit über keine globale, arbeitsbereichsübergreifende Suche, keine zusammengeführte Zeitleiste, keinen Ermittlungsgraphen und kein kombiniertes Fallarchiv. Der Export mehrerer Konten eines Kanals/einer Supergruppe ist ein separater Vorgang und stellt keine Zusammenführung der Kontenprotokolle dar.

Bei umfangreicheren Projekten sollten Sie die Grenzen durch einen [unabhängigen Zeugen](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/) wahren. Verwenden Sie kontrollierte Zustellungsprüfungen, um den Erfassungsweg und die Sichtbarkeit jedes Kontos zu überprüfen.

## 7. Zusammenstellung und Überprüfung der Fallübergabe

Fassen Sie diese Informationen in einem von einem Analysten zusammengestellten Fallverzeichnis zusammen:

| Material | Zweck |
| --- | --- |
| Fallnotizen und Quellenverzeichnis | Fragen, Erfassungsrichtlinien, Zugriffsrechte/Rollen, Ergebnisse, alternative Erklärungen und Lücken |
| Zeitleiste | Angaben zu Zeitpunkten sowie Verweise auf Arbeitsbereich, Chat, Nachricht und Sequenz für jeden Eintrag |
| Signierte Beweisdatei im ZIP-Format pro Arbeitsbereich | Vollständiges Protokoll, Manifest und enthaltene, gesicherte Medien; Filterfelder schränken den Protokollexport nicht ein |
| Separat signierte Personenprofil-Dateien | Abgeleitete Referenzen wurden anhand der entsprechenden Beweismittel im Arbeitsbereich überprüft |
| Signierte vollständige Chat-Exporte | Erfassung des aktuell sichtbaren Verlaufs, getrennt vom Beobachtungsprotokoll |
| Vertrauenswürdige Fingerabdrücke und frühere Kontrollpunkte | Wichtige Identitätsmerkmale und Grenzen des gespeicherten Protokolls |
| Witness-Artefakte, sofern konfiguriert | Separates Protokoll, signierte Einträge und Witness-Fingerabdruck |
| Verifizierungsergebnisse und Hashes der bereitgestellten Dateien | Was wurde überprüft, welche Bytes wurden übertragen und an wen? |

Aus einer vertrauenswürdigen Installation, mit Dateinamen und dem tatsächlichen Fingerabdruck jedes Arbeitsbereichs:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Die tatsächlichen Verifizierungsergebnisse und Originalartefakte werden beibehalten. Das oberste Fallverzeichnis, das Quellenregister und die Schlussfolgerungen der Analysten werden extern verwaltet; jedes TgWitness-Artefakt verfügt über eine eigene Signatur und ein eigenes Verifizierungsverfahren.

## Passen Sie die Untersuchung an

| Fall | Trace | Liefern |
| --- | --- | --- |
| Bot-gesteuerte Streitigkeiten bezüglich Bestellungen/Zahlungen | Ankündigung des Eintrags → Vorschau des gespeicherten Links → Startparameter des Bots → Nachrichten- und Tastaturversionen → Rückmeldebestätigungen über das Panel → Nachverfolgung in privaten Chats und Gruppen | Beobachtete Zeitachse von Angeboten und Antworten sowie verifizierte Quellen; ein Zahlungslink allein stellt keinen Zahlungsnachweis dar |
| Gelöschte Nachrichten nach einem Vorfall | Alle betroffenen Chats → gespeicherte Originale/Bearbeitungen → Ergebnisse bei Löschung oder Fehlen bei erneuter Überprüfung → erhaltene Medien → Berichterstattung und andere Perspektiven des Kontos | Gespeicherte Versionen und explizit angegebene unbekannte Zeitintervalle; keine fiktiven Löschakteure |
| Ein Teilnehmer verwendet in verschiedenen Chats unterschiedliche Namen | Numerische Absender-ID → Verlauf von Namen/Benutzernamen → Antworten → weitere beobachtete Chats → zitierte Ziele/Dateien | Eine zeitliche Übersicht über die Aktivitäten eines genannten Telegram-Kontos, wobei Hypothesen zur realen Identität und zu Beziehungen getrennt dargestellt werden |

[Referenz zur Sammlung](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/) · [Überprüfung von Personenprofilen](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#people-profiles) · [Übergabe von Beweismitteln](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#investigation-handoff) · [Validierung abgeschlossen](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/)
