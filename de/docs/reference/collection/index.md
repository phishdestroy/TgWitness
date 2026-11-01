# So funktioniert die Datenerfassung

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/

Beobachtungsumfang, Live-Aktualisierungen, Nachprüfungen, Anhänge, eigene Aktionen und die Bedeutung von Lücken – Eintrag für Eintrag.

TgWitness protokolliert, was ein verbundenes Telegram-Konto wahrnimmt. Das Protokoll bewahrt diese Wahrnehmungen, ihre Reihenfolge und den damit verbundenen Kontext. Es leitet keine nicht beobachteten Handlungen aus einer fehlenden Nachricht oder aus der Verbindung eines Kontos ab.

## Von der Anmeldung bis zum Protokoll

Ablaufdiagramm · Ein Benutzerkonto autorisieren → Wählen Sie zugängliche Gruppen und Kanäle aus; Wählen Sie zugängliche Gruppen und Kanäle aus → Einstellungen für Ereignisse und Anhänge speichern; Einstellungen für Ereignisse und Anhänge speichern → Beobachtung starten; Beobachtung starten → Erhalten Sie Updates vom aktiven Client; Erhalten Sie Updates vom aktiven Client → Richtlinien zu Quellen und Ereignissen anwenden; Richtlinien zu Quellen und Ereignissen anwenden → Eine signierte Beobachtung anhängen; Eine signierte Beobachtung anhängen → Das Protokoll einsehen oder exportieren; Eine signierte Beobachtung anhängen → Alle in der Warteschlange befindlichen Anhänge verarbeiten; Alle in der Warteschlange befindlichen Anhänge verarbeiten → Fügen Sie das Ergebnis des Downloads hinzu · Ein Benutzerkontoautorisieren · Wählen Sie zugänglicheGruppen und Kanäle aus · Einstellungen fürEreignisse und Anhängespeichern · Beobachtung starten · Erhalten Sie Updatesvom aktiven Client · Richtlinien zu Quellenund Ereignissenanwenden · Eine signierteBeobachtung anhängen · Das Protokoll einsehenoder exportieren · Alle in derWarteschlangebefindlichen Anhängeverarbeiten · Fügen Sie das Ergebnisdes Downloads hinzu

**Diagramm als Text**

1. Ein Benutzerkonto autorisieren → Wählen Sie zugängliche Gruppen und Kanäle aus
2. Wählen Sie zugängliche Gruppen und Kanäle aus → Einstellungen für Ereignisse und Anhänge speichern
3. Einstellungen für Ereignisse und Anhänge speichern → Beobachtung starten
4. Beobachtung starten → Erhalten Sie Updates vom aktiven Client
5. Erhalten Sie Updates vom aktiven Client → Richtlinien zu Quellen und Ereignissen anwenden
6. Richtlinien zu Quellen und Ereignissen anwenden → Eine signierte Beobachtung anhängen
7. Eine signierte Beobachtung anhängen → Das Protokoll einsehen oder exportieren
8. Eine signierte Beobachtung anhängen → Alle in der Warteschlange befindlichen Anhänge verarbeiten
9. Alle in der Warteschlange befindlichen Anhänge verarbeiten → Fügen Sie das Ergebnis des Downloads hinzu

Autorisierung, Zugriff auf eine Quelle, ein laufender Datenerfasser und die vollständige Übermittlung sind unterschiedliche Aspekte. Eine erfolgreiche Anmeldung gewährt nicht den Zugriff auf jede Gruppe. Eine hergestellte Transportverbindung bedeutet nicht, dass jede relevante Aktualisierung angekommen ist.

## Beobachtungsumfang: ausgewählte Chats, ein Ordner oder das gesamte Konto

Quellen → **Der Beobachtungsumfang** bestimmt, welche Chats ein Arbeitsbereich aufzeichnet.

| Modus | Aufzeichnungen | Neue Chats |
| --- | --- | --- |
| Ausgewählte Chats (Standard) | Nur die Chats, die Sie manuell hinzufügen | Wird niemals automatisch hinzugefügt |
| Telegram-Ordner | Chats in einem der Ordner des Kontos: Chats, die namentlich aufgeführt sind, zuzüglich der Kategorien des Ordners (Kontakte, Nicht-Kontakte, Gruppen, Kanäle, Bots), abzüglich der ausgeschlossenen Chats und, sofern im Ordner angegeben, der archivierten Chats | Entsprechende Chats werden hinzugefügt, sobald sie aktiv werden; Chats, die Sie in Telegram zum Ordner hinzufügen, werden innerhalb einer Stunde erfasst. |
| Gesamter Bericht | Jeder Chat, den das Konto sieht | Jeder neue Chat, jede neue Gruppe, jeder neue private Chat und jeder neue Bot wird in dem Moment hinzugefügt, in dem die erste Aktualisierung eintrifft. |

- **Quellentypen** (Kanäle, Gruppen, private Chats, Bots) schränken die Modi „Ordner“ und „Gesamtes Konto“ ein. Ausgewählte Chats können beliebigen Typs sein, einschließlich privater Chats und Bots.
- **Ausgeschlossene Chats** werden in keinem Modus aufgezeichnet. Im Ordner- und im Gesamtkonto-Modus führen die Funktionen *„Ausschließen“* und *„Entfernen“* bei einer Quelle dazu, dass diese in diese Liste aufgenommen wird, sodass sie vom Erfassungsbereich nicht erneut hinzugefügt wird. Wählen Sie den Chat erneut manuell aus (unter „Quellen“ oder aus den „Chats“), wird er aus der Liste entfernt. Die Liste fasst bis zu 5.000 Chats; wird diese Grenze überschritten, wird *der Befehl „Entfernen“* abgelehnt und der Chat kann stattdessen pausiert werden.
- **Eigene Aktionen** (standardmäßig aktiviert): Nachrichten, die dieses Konto versendet, dessen Bearbeitungen sowie die Tastenanschläge auf der Antworttastatur. Bei Deaktivierung werden ausgehende Nachrichten und Bearbeitungen übersprungen.
- Beim Wechsel zu einem Ordner oder zum gesamten Konto wird eine Bestätigung angefordert: Diese Modi zeichnen private Chats und Nachrichten Dritter auf und gehören ausschließlich in ein dafür vorgesehenes Konto. Die Bestätigung sowie jede Änderung des Erfassungsumfangs werden als signierte `scope.changed`-Datensätze gespeichert.
- Durch den Scope hinzugefügte Chats erscheinen als Quellen mit der Kennzeichnung *„auto“* und werden als „`scope.applied`“ (zu Beginn und stündlich) oder „`source.discovered`“ (ein neuer Chat während der Beobachtung) aufgezeichnet. Beim Zurückwechseln zu ausgewählten Chats werden alle automatisch hinzugefügten Quellen angehalten.

Was diese Modi nicht leisten können:

- **Geheime Chats** sind zwischen zwei Geräten Ende-zu-Ende-verschlüsselt und gelangen in keinem Modus jemals zu TgWitness.
- **Solange TgWitness nicht ausgeführt wird, erfolgt keine Aufzeichnung.** Nach einem Neustart fragt das Programm bei Telegram nach versäumten Aktualisierungen und überprüft die Chats erneut; nach längeren Ausfällen liefert Telegram jedoch nicht alle Daten zurück. In Berichten und in „`verify.py`“ werden solche Zeiträume als Lücken dargestellt (siehe [Erfassungsbereich](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)).
- Zu Beginn werden nur die ersten 1.000 Dialoge aufgelistet (die Obergrenze ist unter **„Parameter“** festgelegt); ältere Chats werden hinzugefügt, sobald sie wieder aktiv werden. Der frühere Verlauf eines hinzugefügten Chats wird nicht abgerufen – erstellen Sie bei Bedarf einen Verlaufs-Snapshot oder einen vollständigen Chat-Export.
- Sich ständig ändernde Ordnerstatus (stummgeschaltet, gelesen) werden nicht berücksichtigt: Solche Chats bleiben weiterhin im Beobachtungsbereich.
- **Inline-Bot-Schaltflächen (Callback), die** in einer anderen App betätigt werden, sind für eine zweite Sitzung nicht sichtbar; die Antwort oder Bearbeitung des Bots wird aufgezeichnet. Tastatureingaben zur Beantwortung werden als ausgehende Nachrichten gesendet und mit „`button_press`“ gekennzeichnet.
- Mehr Chats bedeuten mehr Anfragen. Telegram schränkt Konten bei einem als übermäßig erachteten Volumen ein, was ein weiterer Grund für die Verwendung dedizierter Konten ist.

## Umfang und Auswahl der Ereignisse

Jeder Arbeitsbereich verfügt über eigene Quellen. TgWitness tritt keinen Gruppen bei, nimmt keine Einladungen an und listet nicht automatisch alle Mitglieder auf. Die Quellen müssen für das Konto bereits zugänglich sein. Beim Start gleicht der Collector ausgewählte Quellen mit den sichtbaren Dialogen des Kontos ab; die ersten 1.000 Dialoge werden überprüft, sofern unter **„Parameter → Chats aus der Liste des Kontos lesen**“ nichts anderes festgelegt ist. Eine fehlende Quelle wird als **„Zugriff unbestätigt“** markiert; es wird nicht davon ausgegangen, dass Sie entfernt wurden.

| Einleitung | Erfasst | Auswirkung bei Deaktivierung |
| --- | --- | --- |
| Neue Nachrichten | Normale zugestellte Nachrichten | Bei späteren Bearbeitungen oder Löschungen steht möglicherweise kein zuvor erfasster Text zum Vergleich zur Verfügung. |
| Bearbeitungen | Bereitgestellte bearbeitete Versionen der Nachrichten | Zwischenzeitliche Änderungen werden später nicht rekonstruiert. |
| Löschungen | Löschhinweise mit festgelegter Geltungsbereich und Hinweise auf Kontoebene ohne festgelegten Geltungsbereich | Löschmeldungen werden nicht in das Protokoll aufgenommen. |
| Reaktionen | Bereitgestellte Momentaufnahmen der Reaktionen | Separate Aktualisierungen zu Reaktionen werden nicht hinzugefügt. |
| Mitgliedschaft | Versendung von Mitteilungen zum Mitgliederservice und Aktualisierungen für Teilnehmer | Diese Beobachtungen von Mitgliedern werden nicht hinzugefügt. |

Die Einstellungen gelten für alle ausgewählten Quellen im Arbeitsbereich. Speichern Sie das Formular, um die Änderungen zu übernehmen; Änderungen werden mit signierten Vorher-Nachher-Werten protokolliert. Das Deaktivieren einer Kategorie führt nicht zur Löschung früherer Datensätze. Das erneute Aktivieren führt nicht zur nachträglichen Ergänzung versäumter Aktualisierungen.

Betriebliche Protokolle und andere Ereignisse des Gruppendienstes bleiben von diesen Einstellungen unberührt. Nachrichten des Mitgliederservices können Nachrichtenprotokolle erstellen, wenn die Mitgliedschaft aktiviert ist, selbst wenn die normale Erfassung neuer Nachrichten deaktiviert ist. Erfasste Telegram- Objekte behalten eingebettete Metadaten bei; eine Einstellung ist keine Schwärzungsregel.

**Löschungen in privaten Chats und normalen Gruppen** werden als Nachrichten-IDs ohne zugehörigen Chat erfasst. Diese Chats nutzen eine gemeinsame, kontoweite Nachrichten-ID-Sequenz; wenn also eine Nachricht mit dieser ID zuvor gespeichert wurde, ist der zugehörige Chat bekannt: Die Löschung wird in diesem Chat erfasst, wobei `chat_resolution` erläutert, wie dies geschieht. Niemals gespeicherte IDs bleiben eine **nicht zugeordnete Löschung** mit einer explizit unbekannten Quelle; der Collector unternimmt keine Vermutungen. Telegram gibt niemals an, wer eine Nachricht gelöscht hat; wenn die gelöschte Nachricht von diesem Konto gesendet wurde, wird dies im Datensatz vermerkt (`deleted_message_was_outgoing`), ohne den Löschenden namentlich zu nennen.

## Eigene Maßnahmen

Vom beobachteten Konto gesendete Nachrichten werden mit „`outgoing`“ gekennzeichnet. Bei der Bearbeitung einer ausgehenden Nachricht wird darauf hingewiesen, dass in privaten Chats und Gruppen nur der Verfasser die Nachricht bearbeiten kann, während Beiträge in Kanälen auch von anderen Administratoren bearbeitet werden können. Wenn eine ausgehende Nachricht den Text einer Schaltfläche aus der zuletzt gespeicherten Antworttastatur in diesem Chat wiederholt, wird sie mit „`button_press`“ gekennzeichnet und enthält einen Link zu dem Datensatz der Tastatur.

Der Ausschluss eigener Aktionen gilt auch für Hintergrundüberprüfungen und den automatischen Verlauf neuer Chats. Übersprungene ausgehende Nachrichten verschieben die Position der Überprüfung nach vorne, sodass sie spätere eingehende Nachrichten nicht blockieren können. Explizite Aktionen über das Bedienfeld und manuell angeforderte Verlaufs-Snapshots bleiben weiterhin aufgezeichnet.

## Ermittlungsmodus: Beitritt zu Teams und Kommunikation mit Bots

**Quellen → Beobachtungsumfang → Untersuchungsmodus** bereitet den Umfang für ein spezielles Konto vor, das Team-Chats beitritt, Bots startet und an diese schreibt: das gesamte Konto, jeden Quellentyp, eigene Aktionen sowie für jeden Chat oder Bot, der erscheint, dessen Profil und die letzten 200 sichtbaren Nachrichten. Überprüfen Sie das Formular und klicken Sie auf **„Umfang speichern“**; der Wechsel zum gesamten Konto erfordert die übliche Bestätigung.

- **Schaltflächen.** Schaltflächen unter einer Nachricht bleiben mit dieser erhalten und werden in **Chats** angezeigt: Links, Web- Apps, Anmeldelinks, zu kopierende Texte, Rückrufdaten, Inline-Abfragen, Anfragen nach einer Telefonnummer oder einem Standort. Links werden als Text angezeigt und vom Panel niemals geöffnet. Wenn ein Bot nur die Schaltflächen ändert (z. B. einen neuen Zahlungslink), handelt es sich um eine neue Version der Nachricht, sowohl bei Live-Updates als auch bei erneuten Überprüfungen.
- **Neue Chats und Bots.** Im Ordner- und im Gesamtkonto-Modus **werden neue Chats oder Bots** unmittelbar nach ihrem **Erscheinen** gespeichert:

  - sein Profil als `source.profile`-Datensatz: Bot-Beschreibung und Befehle, der „Über“-Text eines Nutzers, einer Gruppe oder eines Kanals, Mitglieder, verknüpfter Chat und Einladungslink, sofern Telegram einen zurückgibt;
  - seine zuletzt sichtbaren Nachrichten (bis zu 1.000) als Verlaufs-Snapshot mit der Kennzeichnung „`new_chat`“: die früheren Nachrichten eines gerade betretenen Team-Chats oder das, was ein Bot gesagt hat, bevor die Beobachtung den Chat registriert hat. Bereits live gespeicherte Nachrichten werden nicht erneut aufgezeichnet.

  Chats, die sich bereits in der Liste befinden, wenn der Modus aktiviert wird, werden ohne Momentaufnahmen hinzugefügt. Ein „FloodWait“ unterbricht diesen Vorgang vorübergehend; er wird anschließend fortgesetzt; Fehler werden protokolliert und die Live-Aufzeichnung des Chats wird fortgesetzt. – **Profile auf Anfrage.** Unter **„Chats“ → „Profil“ → „Profil speichern“** wird **nun** das aktuelle Profil jeder Quelle gespeichert; das neueste wird oberhalb der Nachrichten angezeigt. - **Nicht sichtbar.** Inline-Schaltflächen (Callback), die in einer anderen Telegram-App gedrückt werden, das Popup oder der Link, mit dem ein Bot auf einen solchen Klick reagiert, sowie Einladungslinks, die in einer anderen App verwendet werden, erreichen TgWitness nicht. Was der Bot anschließend sendet oder bearbeitet, wird aufgezeichnet.

### Maßnahme aus der Podiumsdiskussion

**„Chats“** enthält nun einen Mini-Client, der das Telegram-Konto des ausgewählten Arbeitsbereichs nutzt:

- Verfassen Sie eine Klartextnachricht oder wählen Sie **„Antworten“** unter einer gespeicherten Nachricht. Die zurückgesendete ausgehende Nachricht wird auch dann aufgezeichnet, wenn der Erfassungsbereich ausgehende Aktualisierungen ausschließt.
- Drücken Sie **die Schaltfläche „Press“** unter einem aktuellen Callback oder einer Text-Schaltfläche. Der Server ruft die Nachricht erneut ab und lehnt die Aktion ab, wenn die Eingabe von der gespeicherten Version abweicht. Callback-Bestätigungen behalten den Popup-Text, die Warnmarkierung und die URL von Telegram bei; die Antwort wird zudem unterhalb der Unterhaltung angezeigt. URLs bleiben als auswählbarer Text erhalten und werden nicht automatisch geöffnet.
- Erweitern Sie **den „Telegram öffnen“-Link**, geben Sie `@username`, einen öffentlichen `https://t.me/name`-Link, `https://t.me/+invite` / `joinchat/invite` oder einen Bot-Link mit `?start=parameter` ein und klicken Sie auf **„Vorschau speichern**“. Der ursprüngliche Link und die Telegram-Vorschau werden vor dem Beitritt signiert. **Beitreten / Öffnen und Beobachten**: Anschließend tritt der Nutzer der Gruppe/dem Kanal bei oder öffnet den Nutzer/Bot, fügt den Chat als aktivierte Quelle hinzu und sendet „`/start`“ an einen Bot, einschließlich dessen Startparameters. Eine Beitrittsanfrage, die auf die Genehmigung durch den Administrator wartet, wird als „ausstehend“ und nicht als Mitgliedschaft erfasst.

Aktivieren Sie **„Beobachtung starten“**, um eingehende Antworten in Echtzeit zu erfassen. Die Funktionen des Bedienfelds funktionieren auch, während die Beobachtung pausiert ist; es wird jedoch nur garantiert, dass deren direkte Antworten gespeichert werden. Neu hinzugefügte Quellen verwenden die konfigurierten Einstellungen für Profil und Verlauf, wenn die Beobachtung läuft. Wenn eine Quelle pausiert ist, aktivieren Sie sie unter **„Quellen“,** bevor Sie eine Nachricht senden oder deren Schaltflächen betätigen.

`interaction.preview`, `interaction.requested` und `interaction.result` sind gewöhnliche signierte Protokollereignisse, die in den Beweismittelexporten enthalten sind. Anfragen identifizieren das Konto, die Nachricht/Schaltfläche oder den Vorschau-Datensatz sowie, ob die Überwachung aktiv war. Empfangsbestätigungen unterscheiden zwischen Erfolg, Ablehnung, ausstehender Genehmigung und einem unbekannten Ergebnis. Eine unterbrochene Anfrage könnte Telegram erreicht haben: Überprüfen Sie den Chat, bevor Sie eine neue Aktion starten. Durch die Wiederverwendung einer Anfrage-ID wird die gespeicherte Bestätigung abgerufen, ohne die Aktion zu wiederholen – auch nach einem Neustart. Das Fenster behält die ID bei, wenn während der aktuellen Seitensitzung eine mehrdeutige Antwort für dieselbe Aktion erfolgt. Es behält diese ID auch bei, wenn die Aktualisierung der Ansicht nach einer erfolgreichen Aktion fehlschlägt: Die Bestätigung bleibt sichtbar, und durch erneutes Klicken wird sie abgerufen. RPCs für Rückrufe und Beitritte verfügen über einen einzigen Versuchsversuch; wiederholbare Lesevorgänge behalten ihre konfigurierte Wiederholungsrichtlinie bei. Ein sofortiger Wechsel des Chats löscht den Entwurf und das Antwortziel und deaktiviert das Senden, bis die neue Konversation geladen ist.

Dieser Mini-Client verarbeitet Text- und Callback-Schaltflächen. Für Web-Apps, Anmelde-, Telefon- und Standortanfragen, Zahlungen, Inline-Abfragen und Anhänge ist weiterhin ein Telegram-Client erforderlich; die gespeicherten Metadaten der Schaltflächen bleiben sichtbar. Die neuen Steuerelemente verwenden englischen Text.

## Stufen erneut überprüfen

Bei Nachprüfungen wird Telegram erneut nach übersehenen Nachrichten, Bearbeitungen und Nachrichten abgefragt, die nicht mehr zurückgegeben werden. Mit einem Stern gekennzeichnete Quellen sind Prioritätsquellen, die standardmäßig alle 15 Minuten erneut überprüft werden; alle anderen Quellen alle 6 Stunden. Ausgewählte Chats werden zunächst als Prioritätsquellen behandelt, Chats, die über einen Ordner oder das gesamte Konto hinzugefügt wurden, als reguläre Quellen. Pro Durchlauf werden höchstens 30 Quellen erneut überprüft, und der Rest wartet bis zur nächsten Minute; nach einer erneuten Verbindung werden prioritäre Quellen zuerst berücksichtigt. Beide Intervalle werden unter „Quellen“ → „Aufzeichnungseinstellungen“ → „Erneute Überprüfung“ festgelegt (0 deaktiviert eine Stufe) und werden als „`recheck.changed`“ aufgezeichnet.

Verpasste Nachrichten werden ab der Stelle abgerufen, an der der vorherige Durchlauf beendet wurde, und zwar maximal so viele, wie unter **„Parameter → Neue Nachrichten pro erneuter Überprüfung**“ (standardmäßig 1.000) pro Durchlauf festgelegt ist. Nach einer längeren Unterbrechung füllt die erneute Überprüfung daher die gesamte Lücke, selbst wenn Live-Nachrichten, die neuer sind als die Lücke, zuerst gespeichert wurden . Ein Chat, der noch dabei ist, den Rückstand aufzuholen, wird in der nächsten Minute erneut überprüft, anstatt auf sein Zeitintervall zu warten; `recheck.completed` zeigt `continues_after` an, bis der Vorgang abgeschlossen ist.

Vergleiche umfassen Nachrichtentexte, Entitäten, Tastatureingaben (einschließlich Löschvorgänge) sowie den Inhalt und die Identität von Anhängen. Das bloße Ändern von Datei-Zugriffshashes oder Dateiverweisen stellt keine Bearbeitung dar, ebenso wenig wie das, was Telegram von sich aus einträgt: das Laden einer Link-Vorschau, Aufrufe von Stories, durch dieses Konto freigeschaltete kostenpflichtige Medien sowie der Erhalt einer Rechnung. Jede gespeicherte Version in „Chats“ ist mit ihrem vollständigen Protokoll-Eintrag verknüpft, einschließlich der Medien-Metadaten.

## Nachrichtenverlauf und Zuordnung

Angenommen, der Datensammler registriert „Besprechung um 10:00 Uhr“, sieht später „Besprechung um 11:00 Uhr“ und erhält anschließend eine Löschmeldung. Es werden drei unterschiedliche Einträge angefügt. Der ursprüngliche Text bleibt erhalten, die Bearbeitung wird als separate Version gespeichert, und die Meldung dokumentiert, dass eine Löschung festgestellt wurde.

Sollte die Erfassung erst nach dem Verschwinden der ersten Version begonnen haben, ist dieser Text nicht mehr verfügbar. Sollten während der Offline-Phase mehrere Bearbeitungen stattgefunden haben, können nur die anschließend erfassten Versionen gespeichert werden. Eine Löschmeldung kann Inhalte, die nie erfasst wurden, nicht wiederherstellen.

Der Absender einer Nachricht ist nicht automatisch der Bearbeiter. Telegram gibt in der Regel weder die Person an, die eine Nachricht gelöscht hat, noch den genauen Zeitpunkt der Löschung. Unbekannte Akteure bleiben unbekannt. Reaktions-Snapshots und Teilnehmer-Updates enthalten lediglich die Zahlen und Identitäten, die Telegram für das Konto sichtbar macht.

Sequenznummern geben die Reihenfolge der Beobachtungen an. Der UTC-Zeitstempel des Erfassers entspricht dessen lokaler Uhrzeit; ein Zeitstempel der Telegram-Quelle wird separat gespeichert, sofern dieser bereitgestellt wird. Keiner der beiden Zeitstempel stellt einen unabhängigen, vertrauenswürdigen Zeitstempel dar.

## Momentaufnahmen der Historie

Ein Snapshot-Aufruf fordert die neuesten sichtbaren Nachrichten von einer aktivierten Quelle ab, bis zu 500 pro Aufruf. Die Ergebnisse werden als Verlaufsbeobachtungen gekennzeichnet. Sie können sich mit der Live-Erfassung überschneiden, und wiederholte Beobachtungen werden als separate Datensätze gespeichert.

Die Momentaufnahmen entsprechen den Richtlinien für Anhänge, bleiben jedoch von den Schaltvorgängen bei Live-Ereignissen getrennt. Sie rekonstruieren keine gelöschten Nachrichten oder fehlenden Zwischenversionen. Sie können eine Momentaufnahme anfordern, während der Vorgang angehalten ist; alle darin enthaltenen Anhänge werden in die Warteschlange gestellt und warten, bis die Beobachtung beginnt und der Download-Prozess abläuft.

## Umgang mit Anhängen

Der Download von Anhängen ist standardmäßig aktiviert und wird angehalten, sobald weniger als 1 GiB freier Speicherplatz verfügbar ist. Der Collector führt die Beobachtung der Nachrichten und den Download-Auftrag gemeinsam aus. Der Auftrag behält den ursprünglichen Medien-Deskriptor und die Größenrichtlinie bei, sodass ein später bearbeiteter Anhang nicht unbemerkt ersetzt wird.

Downloads werden nach der Erfassung der Nachrichten ausgeführt. Ein abgeschlossener Download erzeugt einen „`media.saved` “-Datensatz mit dessen SHA-256-Hash und Byteanzahl. Übersprungene, fehlgeschlagene, erneut versuchte und unterbrochene Vorgänge führen zu unterschiedlichen Ergebnissen. Ein in der Warteschlange befindlicher Auftrag ist kein Nachweis dafür, dass die Datei gesichert wurde. Die fertige Datei muss zudem mit der Byteanzahl im ursprünglichen, beobachteten Anhangsdeskriptor übereinstimmen. Eine zu kurze oder unerwartet lange Antwort wird nicht als gesichertes Medium erfasst.

Die Speichergrenzen werden **pro Dateityp** festgelegt: Fotos, Videos, GIFs und Animationen, Rund-Video-Nachrichten, Sprachnachrichten, Musik und Audiodateien, Sticker sowie Dateien. Jeder Typ kann deaktiviert werden und verfügt über ein eigenes Größenlimit von 1 bis 2.000 MiB; neue Arbeitsbereiche beginnen mit 20 MiB für Fotos, 100 MiB für Videos, 50 MiB für Dateien, Audio und Rundvideos, 20 MiB für Sprachnachrichten und GIFs sowie 5 MiB für Sticker. In neuen Arbeitsbereichen sind GIFs und Sticker deaktiviert, bis sie aktiviert werden. Arbeitsbereiche mit Richtlinien, die vor der Einführung der typbezogenen Begrenzungen gespeichert wurden, behalten alle Typen aktiviert und behalten ihre einheitliche Obergrenze für jeden Typ bei. *Die maximale Dateigröße* gilt für alle Typen gleichzeitig. Ein deaktivierter Typ erzeugt einen „`media.skipped`“-Datensatz; Dateien mit unbekannter Größe oder übergroße Dateien werden nicht heruntergeladen. Große Dateien erhalten zusätzliche Download-Zeit, basierend auf ihrer Größe und einer Basisgeschwindigkeit von 256 KiB/s. Aufträge bleiben nach einem Neustart erhalten, doch abgelaufene Verweise, verlorener Zugriff oder gelöschte Dateien können die Wiederherstellung dennoch verhindern. Wartende Aufträge behalten das für sie gespeicherte Limit bei, sodass eine Anhebung des Limits nur für neue Dateien gilt. Das Deaktivieren eines Typs oder das Herabsetzen seines Limits überspringt auch die davon ausgeschlossenen wartenden Dateien, für die jeweils ein „`media.skipped`“-Datensatz erstellt wird; das Deaktivieren von Downloads hält die Warteschlange an, bis sie wieder aktiviert werden.

## Anhalten, sperren, Verbindung trennen und neu starten

| Handlung oder Zustand | Wirkung |
| --- | --- |
| Arbeitsbereich wechseln | Ändert die Ansicht des Panels; andere Collector-Instanzen behalten ihren Status bei. |
| Das Fenster sperren oder einen Tab schließen | Der Server und die Überwachung bleiben dabei in Betrieb. |
| Beobachtung unterbrechen | Hält diesen Collector an und bewahrt die in der Warteschlange befindlichen Anhänge auf. |
| Eine Quelle deaktivieren | Verhindert künftige gezielte Erfassung; dafür in der Warteschlange befindliche Medienaufträge werden angehalten, solange die Funktion deaktiviert ist. |
| Eine Quelle entfernen | Es ignoriert diese Quelle und löscht die zugehörigen Benutzerprofile; bereits gespeicherte Einträge verbleiben im Protokoll, das nur nachträglich ergänzt werden kann. Noch ausstehende Anhänge werden als fehlgeschlagen (`source_removed`) erfasst. Im Ordner- und im Gesamtkonto-Modus werden sie ebenfalls ausgeschlossen. |
| Ändern Sie die Verbindungsroute | Erfordert eine Pause, schließt alte Clients und bricht unvollständige Anmeldungen ab. |
| Beenden Sie den Python-Prozess | Alle Arbeitsbereiche werden angehalten; während der Offline-Zeit werden keine Beobachtungen vorgenommen. |
| Neustart nach aktiver Beobachtung | Es wird versucht, den gespeicherten Umfang mithilfe der gespeicherten Sitzung fortzusetzen. Eine manuelle Unterbrechung hebt diese Absicht auf. |

Der Collector protokolliert erkannte Verbindungsabbrüche, Wiederholungsversuche, Fehler, Starts/Stops und Heartbeats. Kurze Unterbrechungen können bei periodischen Verbindungsprüfungen übersehen werden. Nach einem Neustart werden versäumte Aktualisierungen ab der gespeicherten Aktualisierungsposition angefordert und beobachtete Chats werden regelmäßig erneut überprüft; siehe [Beweisformat](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#durable-collection-and-process-receipts-02). Ein Snapshot liefert Kontext; er beweist jedoch nicht, dass eine Lücke geschlossen wurde.

## Kontoisolierung und -überprüfung

Jeder Arbeitsbereich verfügt über ein eigenes Protokoll, eigene Berechtigungen, einen eigenen Signaturschlüssel, eigene Richtlinien und eine eigene Warteschlange. Nur der aktive Client dieses Arbeitsbereichs kann Live-Beobachtungen einbringen. Abgelehnte, ausstehende, ersetzte und Verbindungstest-Clients können keine Live-Aktualisierungen in das Protokoll dieses Arbeitsbereichs schreiben. Verschiedene Konten können dieselbe Gruppe beobachten, ihre Protokolle bleiben jedoch getrennt.

Jedes Ereignis enthält den vorherigen Hashwert und eine Ed25519-Signatur. Die Exporte umfassen das gesamte Arbeitsbereichsprotokoll anhand einer festen Sequenznummer. Panel-Filter filtern den Export nicht; die Erfassung kann über dessen Grenzen hinaus fortgesetzt werden, während der Export vorbereitet wird.

**„Verify Journal“** überprüft die Ereigniskette und die Signaturen anhand des angezeigten Grenzwerts. Das Ergebnis wird gelöscht, sobald sich der Arbeitsbereich ändert, und das Bedienfeld identifiziert neue Datensätze, die nach der Überprüfung hinzugefügt wurden. Der ZIP-Export überprüft zudem die gesammelten Medien.

Eine gültige Signatur gewährleistet die Integrität in Bezug auf den vertrauenswürdigen Schlüssel, nicht in Bezug auf die Herkunft aus Telegram oder die Richtigkeit des Inhalts. Fingerabdrücke und Kontrollpunkte sind unabhängig voneinander aufzubewahren. Siehe das [Beweismodell](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/), [den täglichen Betrieb](https://phishdestroy.github.io/TgWitness/de/docs/reference/operations/) und [das Live-Abnahmeverfahren](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) hinsichtlich der Vertrauens- und Übermittlungsanforderungen.
