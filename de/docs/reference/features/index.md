# Funktionen und Einschränkungen

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/features/

Das aktuelle Erfassungsmodell, Workflows für mehrere Konten, Exporte und operative Grenzen von TgWitness.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Projektreferenz](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Projektreferenz](https://phishdestroy.github.io/TgWitness/assets/chapter-project.svg)

TgWitness sichert Telegram-Konversationen, auf die verbundene Konten Zugriff haben, erfasst festgestellte Änderungen und erstellt überprüfbare Exporte. Diese Referenz beschreibt das Erfassungsmodell, aktuelle Arbeitsabläufe und deren Grenzen.

**Auf dieser Seite**

- [Standalone-Anwendung](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/#standalone-application)
- [Gemeinsame Untersuchungen](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/#shared-investigations)
- [Archivierungswerkzeuge](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/#archive-tools)
- [Optionale Extras](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/#optional-extras)
- [Protokoll und private Quellen](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/#protocol-and-private-sources)
- [Mehrere Konten](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/#multiple-accounts)
- [Erfassung und Zuordnung](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/#capture-and-attribution)
- [Kapazität und Telegram-Beschränkungen](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/#capacity-and-telegram-limits)
- [Zuverlässigkeit und Wiederherstellung](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/#reliability-and-recovery)
- [Beweismodell](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/#evidence-model)
- [Export, Bereitstellung und Übergabe](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/#export-deployment-and-handoff)
- [Kriterien für stabile Veröffentlichungen](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/#stable-release-criteria)

## Eigenständige Anwendung

TgWitness verfügt über eine eigene Installation, ein eigenes Datenverzeichnis und einen eigenen Release-Zyklus. Die mitgelieferte Weboberfläche übernimmt die Einrichtung und Überprüfung; exportierte Datensätze können eigenständig verwendet werden.

Der Betreiber verbindet seine Konten, wählt die für jedes Konto sichtbaren Quellen aus und erhält ein gespeichertes Beobachtungsprotokoll. Das Dashboard zeigt Inhalte, gespeicherte Änderungen, die Herkunft der Beobachtungen sowie bekannte Lücken an. Ein anderer Ermittler kann das exportierte Material überprüfen.

Das Panel unterscheidet zwischen Kontoautorisierung, Zugriff auf eine Quelle, Collector-Aktivität und erfasster Abdeckung. Überprüfen Sie diese Zustände gemeinsam, wenn Sie ein Intervall mit wenigen Nachrichten oder ein Verbindungsproblem bewerten.

## Gemeinsame Ermittlungen

Ein Administrator kann [Zugriffstoken](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/) ausstellen, [die](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/) auf Arbeitsbereiche und einzelne Chats beschränkt sind, mit Berechtigungen pro Aktion, IP-Einschränkungen, Ablaufdaten, Anmeldebeschränkungen und Sitzungskontrolle. Ein Prüfer mit Lesezugriff kann einen Fall einsehen, ohne die Telegram-Autorisierung oder den Schlüssel für das Hauptfenster zu erhalten. Der auf Chats beschränkte Zugriff bleibt getrennt von kontoweiten Einstellungen und vollständigen Journal-Exporten.

Automatic MTProxy unterhält funktionierende Telegram-Routen aus vier öffentlichen Quellen oder einem Betreiberkatalog. [IP-Modi](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/#ip-modes) legen fest, ob bei einem Ausfall auf einen anderen Proxy gewartet werden muss oder eine ausdrücklich zugelassene direkte Route genutzt werden darf. Externe HTTP-Anfragen verfügen über eine separate Route und einen Deaktivierungsschalter.

## Archivierungstools

[Die Erfassung von Verlaufsdaten](https://phishdestroy.github.io/TgWitness/de/docs/reference/history/), [die Suche und Analyse im Archiv](https://phishdestroy.github.io/TgWitness/de/docs/reference/analysis/),[ein schreibgeschütztes MCP](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/), [lokale OCR/Transkription](https://phishdestroy.github.io/TgWitness/de/docs/reference/media-analysis/) und[ausgehende Webhooks](https://phishdestroy.github.io/TgWitness/de/docs/reference/webhooks/) sind in 0.7.1 enthalten. Analyseberichte und erkannter Text bleiben getrennt von den erfassten Ereignissen.

[„Case Board“](https://phishdestroy.github.io/TgWitness/de/docs/reference/case-board/) fügt quellverknüpfte Lesezeichen, Zitate, Notizen und Sammlungen innerhalb eines Arbeitsbereichs hinzu. Der [Berichtskonstruktor](https://phishdestroy.github.io/TgWitness/de/docs/reference/case-reports/) wählt Material, Abschnitte und eines von acht Designs für unterstützte HTML-/PDF-Exporte aus.

## Optionale Zusatzfunktionen

Die tägliche Einrichtung erfolgt über „Konto“ → „Quellen“ → „Beobachtung“. **„Extras“** ist ein separater Bereich mit einem Telegram-Witness-Bot und einer GitHub-Erfassungsvorschau. Bei jedem werden zunächst die Verfügbarkeit und die Anforderungen angegeben, bevor die Einstellungen angezeigt werden. Durch Auswahl einer Karte werden Anweisungen geöffnet; es erfolgt keine Registrierung oder Aktivierung eines Dienstes.

Die Einrichtung des Bots erfolgt in drei Schritten: Erstellen eines Lesezugriffs, Auswählen der Veröffentlichungseinstellungen und Starten auf dem Witness-Host. Netzwerk- und Veröffentlichungsoptionen, bestehende Verbindungen sowie Verifizierungsbefehle werden auf Anfrage angezeigt. Die heruntergeladene Konfiguration unterscheidet sich von einem laufenden Witness. Beim Wechseln von Zusatzoptionen bleibt der Entwurf erhalten; Kontoänderungen und Sperren löschen das temporäre Token und das Formular. Die integrierte Anleitung enthält Anweisungen zum Start. [GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)starten einen angehefteten Collector aus Ihrem Fork, erfassen einen Chat und erzeugen eine verschlüsselte Übergabe mit Workflow-Herkunftsnachweis.

## Protokoll und private Quellen

**MTProto ist das Protokoll von Telegram; Telethon ist die Python-Bibliothek, die TgWitness verwendet, um MTProto zu nutzen.** Es handelt sich dabei nicht um alternative Verbindungsmethoden. Die Datenerfassung erfolgt über MTProto; der optionale „Witness“ veröffentlicht signierte Prüfberichte über die Bot-API.

Jeder Arbeitsbereich verfügt über einen eigenen autorisierten Client und einen eigenen Aktualisierungsstrom für das Konto. TgWitness wählt Beobachtungen aus konfigurierten Quellen aus und stellt separate, explizite Anfragen für Funktionen wie Verlaufs-Snapshots und Medien-Downloads.

Eine private Quelle benötigt keinen öffentlichen Benutzernamen. Der Telegram-Peer-Typ und die numerische ID sind die Identifikatoren; Titel und Benutzernamen können sich ändern. Der Zugriff hängt von der bestehenden Mitgliedschaft und den Berechtigungen ab. TgWitness tritt Quellen nicht automatisch bei und umgeht auch nicht die Beitrittsgenehmigung. Ein Zugriffshash von einem anderen Konto ist kein universelles Zugriffstoken.

Das Erfassungsmodell muss versteckte Verlaufsdaten vor dem Beitritt, Teilnehmer- und Administratorrollen, den Widerruf von Sitzungen, die Entfernung oder Änderung von Berechtigungen, die Migration von Gruppen zu Supergruppen, Themen und Foren, verknüpfte Diskussionen, Kanalidentitäten sowie nicht verfügbare Anhänge berücksichtigen. Nicht jede Kombination wurde bereits in der Praxis getestet.

Die Sichtbarkeit der Quellen wird beim Start des Collectors überprüft. Fehlt eine Quelle aus dem begrenzten Dialogergebnis, bedeutet dies, dass **der Zugriff nicht bestätigt ist**, nicht jedoch, dass eine Entfernung nachgewiesen wurde. Eine nicht verfügbare Quelle verhindert nicht die Beobachtung anderer zugänglicher Quellen. Fügen Sie niemals Einladungslinks oder echte Sitzungen in öffentliche Fixtures ein.

## Mehrere Konten

Das Panel unterstützt eine beliebige Anzahl von **Arbeitsbereichen**, von denen jeder über folgende Merkmale verfügt:

- Autorisierung, verschlüsselter Speicher und Verbindungsweg.
- SQLite-Protokoll und Ed25519-Signaturidentität.
- Ausgewählte Quellen, Medienwarteschlange und Erfassungseinstellungen.
- Überwachungsstatus, Fehler, Kontrollpunkte und Exporte.

Das Wechseln des angezeigten Arbeitsbereichs stoppt keinen anderen Collector. Eine doppelte Kontoautorisierung über verschiedene Arbeitsbereiche hinweg wird abgelehnt. Ein Protokoll, das bereits an ein Telegram-Konto gebunden ist, kann keinem anderen Konto zugewiesen werden; eine erneute Verbindung desselben Kontos ist jedoch zulässig. Dadurch bleiben die Kontoidentität und der relevante Nachrichten-ID-Bereich erhalten.

Die Anwendung legt keine feste Anzahl von Arbeitsbereichen fest. Jeder Arbeitsbereich führt seine eigenen Collector- Aufgaben zur Verbindungsüberwachung, zum Herunterladen von Medien, zu Nachprüfungen und zur Erfassung neuer Chats innerhalb eines gemeinsamen Python-Prozesses und einer gemeinsamen Ereignisschleife aus. Der Durchsatz hängt von der Arbeitslast ab. Zur Prozessisolierung sollten separate Installationen, Ports und Datenverzeichnisse verwendet werden.

Weisen Sie jedem Konto die Quellen zu, auf die es zugreifen kann. Verschiedene Konten können dieselbe Gruppe beobachten, doch ihre Beobachtungen bleiben getrennt und behalten ihre Herkunft bei. Zwei Konten auf einem vom Betreiber kontrollierten Rechner gelten nicht als zwei unabhängige Zeugen. **Der Export „Group“** bündelt die separat signierten ZIP-Dateien der Arbeitsbereiche mit einer signierten Dateiliste, die deren Arbeitsbereichs-IDs, Hashes und Fingerabdrücke der Signaturschlüssel enthält. Jedes Protokoll behält seine eigene Abgrenzung bei. Erstellen Sie eine kombinierte, arbeitsbereichsübergreifende Zeitleiste in Fallnotizen oder Analysetools, wobei diese Quellenverweise erhalten bleiben.

## Erfassung und Zuordnung

Unter „Quellen“ stehen pro Konto Schaltflächen für neue Nachrichten, Bearbeitungen, Löschungen, Reaktionen und Mitgliedschaften zur Verfügung. Voreinstellungen behalten entweder alle Kategorien oder Nachrichten/Bearbeitungen/Löschungen bei. Die Richtlinie gilt für die ausgewählten Gruppen des Arbeitsbereichs, bleibt auch nach einem Neustart erhalten und wird mit den Änderungen vor und nach der Anpassung signiert. Standardmäßig werden alle Kategorien beibehalten. Das Deaktivieren einer Kategorie führt nicht zum Löschen alter Datensätze; das erneute Aktivieren stellt verpasste Ereignisse nicht wieder her. Betriebliche Aufzeichnungen, andere Gruppen-Service-Ereignisse und explizite Verlaufs-Snapshots sind separat. Erfasste Telegram-Objekte können eingebettete Metadaten beibehalten, unabhängig von den Schaltflächen für separate Aktualisierungen. Es gibt noch keine gruppenspezifischen Kategorie-Überschreibungen.

| Material | Jetzt erfasst | Grenze |
| --- | --- | --- |
| Nachricht | Text, Peer-/Nachrichten-IDs, Metadaten des Absenders, Antworten und ursprünglicher Update-Envelope | Wird als für das Konto sichtbare Beobachtung gespeichert, die vom Erfasser signiert wurde |
| Bearbeiten | Neu erfasste Version und alle zuvor gespeicherten Versionen | Zwischenzeitliche Bearbeitungen während Ausfallzeiten können verloren gehen; der Absender ist nicht zwangsläufig der Bearbeiter. |
| Löschung | Benachrichtigung und gegebenenfalls zuvor erfasste Inhalte | In der Regel keine Angabe des Löschers oder des genauen Zeitpunkts der Aktion |
| Löschhinweis auf Kontoebene | Ursprünglicher Hinweis; zu den abgeschlossenen Datensätzen gehören der gespeicherte Chat und die Korrelationsmethode | Es muss genau eine zuvor gespeicherte Übereinstimmung aus einem privaten Chat oder einer normalen Gruppe im Umfang vorhanden sein; andere IDs bleiben „`deletion.unscoped`“. Kanal- und Supergruppen-IDs sind von dieser Korrelation ausgeschlossen. |
| Reaktion | Ausgegebene Zählerstände und sichtbare aktuelle Identitäten | Eine vollständige Liste der verfügbaren Reaktoren erfordert separate Abfragen; Kanäle können Identitäten verbergen |
| Mitgliedschaft | Service-Meldungen und zugestellte Teilnehmer-Updates | Die Sichtbarkeit hängt von der Rolle und der Art des Chats ab; fehlende Ereignisse bedeuten nicht zwangsläufig, dass keine Aktivitäten stattgefunden haben. |
| Administratoraktionen | Relevante bereitgestellte Updates und eine Momentaufnahme des Admin-Logs in den Exporten von Kanal-/Supergruppen-Chats | Der Export liest das Protokoll, sofern es für das exportierende Administratorkonto verfügbar ist; eine kontinuierliche Abfrage des Administratorprotokolls ist nicht Teil dieses Prozesses. |
| Anhang | Beschreibung der Originalversion, heruntergeladene Bytes/SHA-256 und Ergebnisse der Versuche | Eine gelöschte Datei ist möglicherweise nicht wiederherstellbar; die neueste Version wird nicht ersetzt. |
| Geschichte | Eindeutige Momentaufnahme der aktuell sichtbaren Nachrichten | Es werden nicht alle Bearbeitungen oder gelöschten Inhalte rekonstruiert. |
| Erfassungsprozess | Start/Stopp, Heartbeat, Fehler, Einstellungen, Umfang und signierte Ausführungsbestätigung | Lokales Inventar; GitHub und TDX fügen [-unabhängige Umgebungsprüfungen hinzu](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope) |

Die Benutzeroberfläche nennt das im Quellereignis angegebene Konto und behält beobachtete Namen und Benutzernamen bei. Wenn im Ereignis der Akteur fehlt, bleibt dieses Feld im Bericht unbesetzt.

## Kapazität und Telegram-Beschränkungen

Es gibt keine allgemeingültige Anzahl von Chats, die mit garantierter Qualität überwacht werden können. Die Kapazität hängt von der Spitzenanzahl an Ereignissen pro Sekunde, dem Volumen und der Größe der Anhänge, zusätzlichen RPCs, aktiven Konten, Festplattenlatenz/freiem Speicherplatz, Netzwerkbedingungen, Telegram-Beschränkungen, akzeptabler Verzögerung und der Warteschlangentiefe ab.

Telegram unterscheidet zwischen passiver Zustellung und aktivem Short-Polling. In der aktualisierten Dokumentation werden zusätzliche „`updates.getChannelDifference`“-Aufrufe für offene Kanäle/Supergruppen beschrieben und maximal **zehn gleichzeitig per Short-Polling abgefragte Quellen** empfohlen. Dies stellt weder eine Begrenzung auf zehn ausgewählte Gruppen noch eine Garantie für Vollständigkeit dar.

| Modus | Zweck | Status |
| --- | --- | --- |
| Standardbeobachtung | Erfassung der von ausgewählten Quellen übermittelten Aktualisierungen | Umsgesetzt |
| Prioritätsüberprüfungen | Mit einem Stern markierte Quellen verwenden ihr eigenes konfigurierbares Intervall und haben bei jedem begrenzten Überprüfungsprozess Vorrang. | Implementiert mit Verlaufs- und Nachrichtenabfragen |

Der Prioritätsstern steuert diese Nachprüfungen. Zusätzliche „`updates.getChannelDifference` “-Short-Polling-Abfragen werden nicht als separater Benutzermodus bereitgestellt.

Beliebige Abfragen mit hoher Frequenz, die „FloodWait“ ignorieren oder von einer linearen Kapazität durch zusätzliche Konten ausgehen, stellen kein gültiges Modell zur Dimensionierung dar. Die Standardgrenzen liegen bei den ersten 1.000 aufgelisteten Dialogen, bis zu 500 Nachrichten pro Verlaufs-Snapshot, 1–2.000 MiB pro erfasster Datei je nach Typ sowie 4 GiB unkomprimierter, signierter ZIP-Inhalte; diese Werte können pro Arbeitsbereich unter **„Parameter“** angepasst werden. Exporte unterliegen keiner festen Obergrenze für die Anzahl der Ereignisse. Der Browser-Fallback ist standardmäßig auf 128 MiB begrenzt; die Streaming-CLI verfügt über ein konfigurierbares Übertragungslimit, standardmäßig 5 GiB.

## Zuverlässigkeit und Wiederherstellung

Zu den implementierten Funktionen gehören SQLite-WAL/synchrone Transaktionen; atomare Schreibvorgänge für Nachrichten und Medienaufträge; persistente Aufträge und Wiederholungsverzögerungen; Deskriptoren für Originalversionen; begrenzte Wiederholungsversuche; persistentes „FloodWait“ für Medien; Medien-Downloads außerhalb der Netzwerkwartezeit des Text-Ereignisses; Exporte mit stabilem Präfix, während spätere Schreibvorgänge fortgesetzt werden; atomare Einstellungen und Prüfprotokolle; Beibehaltung der gültigen Autorisierung nach fehlgeschlagener Ersatzanmeldung; Isolierung eines beschädigten zusätzlichen Arbeitsbereichs; explizite Wiederverbindungsversuche; eindeutige Meldung von Autorisierungsverlusten; sowie Erkennung von Änderungen der Wanduhrzeit mithilfe einer monotonen Uhr.

Die PTS/QTS/SEQ-Werte von Konten und Kanälen werden gespeichert und nach einem Neustart wiederhergestellt, und die überwachten Chats werden regelmäßig erneut überprüft; siehe [Beweisformat](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#durable-collection-and-process-receipts-02). Das regelmäßige Speichern der Position stellt keine atomare, verlustfreie Bestätigung der Protokollakzeptanz dar.

Zu Beginn jedes Vorgangs werden der vorherige Kopf und die Offline-Grenze aufgezeichnet. Der aktuelle Verlauf wird nicht zur Lückenbehebung herangezogen. Die Differenzspeicherung von Telegram ist begrenzt; `differenceTooLong` kann nicht alle verschwundenen Inhalte rekonstruieren. Unwiederherstellbare Lücken müssen ausdrücklich gekennzeichnet bleiben, selbst wenn ein späterer Verlaufs-Snapshot erfolgreich ist.

## Beweismodell

Jedes Ereignis erfasst eine Sequenz, die lokale Beobachtungszeit in UTC, die Quellzeit (sofern angegeben), die Art des Ereignisses, die Quelle, den Akteur (sofern angegeben), die ursprüngliche Nutzlast, den vorherigen Hashwert und die Signatur. Bei der Erfassung von Nachrichten werden zudem das Konto des Erfassers und der Ausführungskontext gespeichert.

Der signierte Prozessbeleg enthält eine zufällige Lauf-ID; TgWitness/Python/OS/Abhängigkeitsversionen; SHA-256-Werte der Quelldateien und einen aggregierten Fingerabdruck; das ursprüngliche Konto, den Umfang und die Einstellungen; UTC-/monotone Messwerte; sowie den vorhergehenden Protokollkopf. Einstellungsänderungen, Start-/Stoppvorgänge und Fehler werden in dasselbe Protokoll eingetragen. Kontrollpunkte werden beim Start, alle fünf Minuten während der Überwachung (einstellbar) sowie bei ordnungsgemäßem Beenden gespeichert. Ein gespeicherter lokaler Kontrollpunkt kann ein Zurücksetzen auf ein früheres Protokollpräfix erkennen.

| Funktionsweise | Was damit erreicht wird |
| --- | --- |
| Datei-SHA-256 | Die Bytes stimmen mit einem bekannten Digest überein |
| Ereignis-Hash-Kette | Aufzeichnung der Reihenfolge/Verknüpfung in Bezug auf eine bekannte Grenze |
| Ed25519 | Signatur unter einem bestimmten Schlüssel |
| Unabhängig gespeicherter Kontrollpunkt | Der nachfolgende Text entspricht den beibehaltenen Grenzen. |
| Analyse der Programmdatei | Selbstbericht des Collectors über erfasste Dateien |
| Gültige, unabhängige TSA-Antwort | Vorhandensein bestimmter Bytes zum TSA-Zeitpunkt unter expliziten Vertrauensannahmen |

Die Vorbereitung von RFC-3161-Anfragen und die Überprüfung der Antworten mittels OpenSSL sind implementiert. Der „Evidence Mode“ übermittelt zudem Checkpoint-Hashes an konfigurierte Zeitstempel-Dienste. Die Antwort der Behörde ist zu speichern und zu überprüfen, um einen unabhängigen Zeitanker zu etablieren. Siehe [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/de/docs/reference/timestamp/).

Behalten Sie Kontrollpunkte unabhängig bei, kontrollieren Sie den Zugriff auf Signaturschlüssel, führen Sie Übertragungsprotokolle und überprüfen Sie Exporte mit vertrauenswürdiger Software. Der [Überprüfungsumfang](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope) erläutert, wie sich diese Kontrollen gegenseitig ergänzen und welche Vertrauensannahmen gelten.

## Export, Bereitstellung und Übergabe

Eine signierte ZIP-Datei enthält die Originaldateien im JSONL-, CSV- und HTML-Format sowie erhaltene Anhänge, Hashes, ein signiertes Manifest und ein praktisches Verifizierungswerkzeug. Sie umfasst einen Arbeitsbereich und ein festes, vollständiges Protokollpräfix. Suchfilter im Bedienfeld entfernen Datensätze nicht stillschweigend. Geheime Schlüssel, Token und Telegram-Sitzungen werden ausgeschlossen; die ursprünglichen Beobachtungen können dennoch personenbezogene Daten und Telegram-Metadaten enthalten.

Speichern Sie den ZIP-Digest, den vertrauenswürdigen Fingerabdruck, den Checkpoint, die Prozessquittung und die Übergabe separat. Verwenden Sie ein Verifizierungsprogramm aus einer vertrauenswürdigen Installation, anstatt ausführbarem Code allein deshalb zu vertrauen, weil er in der untersuchten ZIP-Datei enthalten ist.

Die Browser-Oberfläche wird lokal ohne Node.js, CDNs oder externe Schriftarten bereitgestellt. Ein Operator-Token steuert die Installation. Für den Fernzugriff sind HTTPS oder ein SSH-Tunnel erforderlich. Native Python- und Container-Definitionen werden bereitgestellt, zusammen mit Service-Beispielen im [Verzeichnis „deploy/“](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md); durchgeführte Plattformprüfungen sind separat aufgeführt.

Der Standard-Arbeitsbereich verwendet das Datenstammverzeichnis; zusätzliche Arbeitsbereiche verwenden „`profiles/<id>/`“. Für die Datensicherung müssen der Prozess angehalten und der vollständige Daten-/Schlüsselsatz vorhanden sein. Die ZIP-Dateien mit den Beweismitteln sind keine Anwendungssicherungen. Für Geheimnisse kann ein externer Hauptschlüssel für ein neues Datenverzeichnis verwendet werden; die Verschlüsselung von Protokoll und Medien erfolgt über die Festplatte bzw. das Volume des Betreibers. Siehe [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/) und [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/de/docs/reference/operations/).

## Kriterien für stabile Veröffentlichungen

Vor einer stabilen Veröffentlichung bitte folgenden Hinweis hinzufügen:

1. Echte private Gruppen, Supergruppen, Foren und Kanäle mit Mitglieder-/Administratorrollen sowie verborgenem/sichtbarem Verlauf, einschließlich Anmeldung/2FA, Widerruf und Zugriffsverlust.
2. Kontrollierte Bearbeitungen, Löschungen, Reaktionen, Mitgliedschaften und Medien im Zusammenhang mit bekannten Handlungen.
3. Prozess- oder Serverausfälle, Festplattenausfälle oder volle Festplatten, abgelaufene Dateiverweise, „FloodWait“, Netzwerkausfall, beschädigte Dateien und Datenbank-Rollback.
4. Dauerbetrieb mit mehreren Konten unter Berücksichtigung von Verzögerungen, Warteschlangen, Speicher- und Festplattenressourcen, einschließlich sowohl ruhiger als auch aktiver Quellen.
5. Unterbrechung zwischen dem Fortschreiten des MTProto-Status und der Annahme des Protokolls.
6. Saubere Installation auf der vorgesehenen Betriebssystem-/Container-Matrix und verifizierte Wiederherstellung aus dem Backup.
7. Unabhängige Überprüfung von Sicherheitsaspekten, Signaturen sowie Zuordnungs- und Beweisangaben.

Der bereichsbezogene Zugriff auf das Panel wird unter [„Zugriff und Berechtigungen“](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/) beschrieben. Version 0.6 unterstützt das in [ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/) beschriebene begrenzte TData für ein einzelnes Konto sowie den Import von Kontodateien. Lesen Sie vor der Veröffentlichung die Nutzungsbedingungen der Telegram-API durch. Referenzen zur Forschung und Erkenntnisse zur Plattform finden Sie in [RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md).
