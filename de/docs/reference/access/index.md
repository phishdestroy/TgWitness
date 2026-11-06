# Zugriff und Berechtigungen

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/access/

Legen Sie den Zugriff auf Konten und Chats fest, wählen Sie Berechtigungen aus, beschränken Sie Sitzungen und IP-Adressen und entziehen Sie den Zugriff.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Erste Schritte](https://phishdestroy.github.io/TgWitness/de/docs/reference/quickstart/)

![Erste Schritte](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

Gewähren Sie einem Prüfer Zugriff auf einen Chat, einem Analysten die Berechtigung zum Exportieren eines Falls oder einem Operator die Kontrolle über ausgewählte Konten. Jede Person erhält ihr eigenes Token. Das Haupt- Panel-Token verbleibt beim Administrator.

[Einrichtung eines Kontos](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/) · [Verbindungswege](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/) · [Sicherheitsmodell](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/)

## Zwei Anwendungsbereiche, zwei unterschiedliche Aufgabenbereiche

**Der Erfassungsumfang** bestimmt, was ein Konto aufzeichnet: ausgewählte Chats, einen Telegram-Ordner oder das gesamte Konto. **Der Zugriffsumfang** legt fest, welche dieser aufgezeichneten Konten und Chats eine andere Person einsehen und nutzen kann. Die Gewährung von Zugriff bedeutet nicht, dass man einem Telegram-Chat beitritt, die Erfassung startet oder Berechtigungen für das Telegram-Konto erhält.

Ein Zugriff kann ausgewählte Arbeitsbereiche, ausgewählte Chats innerhalb dieser, alle Arbeitsbereiche oder jedes Konto einer [Kontengruppe](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#bulk-import-and-account-groups) umfassen. **Alle Arbeitsbereiche, einschließlich später hinzugefügter,** umfassen auch zukünftige Konten. Ein Gruppenzugriff umfasst ebenfalls Konten, die dieser Gruppe später hinzugefügt werden. Wählen Sie Arbeitsbereiche explizit aus, wenn ein Fall auf diese beschränkt bleiben soll.

## Jemandem Zugriff gewähren

1. Melden Sie sich als Hauptadministrator an und öffnen Sie **„Zugriff**“.
2. Geben Sie unter **„Jemandem Zugriff gewähren**“ einen Namen ein, den Sie im Protokoll wiedererkennen werden.
3. Wählen Sie die Arbeitsbereiche und, falls erforderlich, die einzelnen Chats aus.
4. Wählen Sie aus, was diese Person tun könnte. **Die Ansicht** ist stets enthalten.
5. Legen Sie die Gültigkeitsdauer, die Anmelde-/Sitzungslimits und die zulässigen Adressen nach Bedarf fest.
6. Klicken Sie auf **„Zugriff erstellen**“. Kopieren Sie das Token jetzt: Es wird nur einmal angezeigt.
7. Senden Sie die Panel-Adresse und das Token privat. Der Empfänger gibt dieses Token auf der normalen Anmeldeseite ein; er benötigt weder Ihr Haupt-Panel-Token noch eine Telegram-Sitzung.

Öffnen Sie das Fenster mit dem ausgestellten Token in einer separaten Browsersitzung und überprüfen Sie die sichtbaren Chats sowie die zulässigen Aktionen, bevor Sie es weitergeben.

## Wählen Sie die Berechtigungen aus

Verwenden Sie für eine rein textbasierte öffentliche Demonstration **die Option „Public Showcase“** anstelle des normalen Reviewer-Zugriffs. Dabei werden explizit ausgewählte öffentliche Kanäle, gespeicherte Bearbeitungen und Löschungen sowie signierte Statistiken angezeigt, wobei Autorenfelder unkenntlich gemacht und Dateien an der API-Grenze geschlossen werden. [Erstellen und überprüfen Sie ein Showcase](https://phishdestroy.github.io/TgWitness/de/docs/reference/showcase/).

| Genehmigung | Was es ermöglicht |
| --- | --- |
| `view` | Lesen Sie freigegebene Chats, erfasste Nachrichten, Profile, Dateien und gefilterte Protokollaufzeichnungen. Immer enthalten. |
| `export` | Der Export von Chat-Verläufen und Dossiers ist zulässig. Für den Export von Beweismaterial aus dem gesamten Arbeitsbereich ist Zugriff auf den gesamten Arbeitsbereich erforderlich. |
| `sources` | Verwalten Sie Quellen, Momentaufnahmen und Profilerfassungen. Der auf Chats beschränkte Zugriff ist nur in zugelassenen Chats möglich; die kontoweite Quellenerkennung und die Umfangseinstellungen bleiben deaktiviert. |
| `collect` | Einen Collector starten oder stoppen. Erfordert Zugriff auf den gesamten Arbeitsbereich, da die Erfassung Auswirkungen auf das Konto hat. |
| `interact` | Führen Sie unterstützte Telegram-Interaktionen innerhalb des Zugriffsumfangs durch. Bei einem auf den Chat beschränkten Zugriff können keine kontoweiten Link-Vorschauen genutzt werden. |
| `settings` | Ändern Sie die Erfassungseinstellungen, Zeitstempel, Benachrichtigungen, externe Kopien und Parameter. Erfordert Zugriff auf den gesamten Arbeitsbereich. |
| `account` | Melden Sie sich bei Telegram an oder ab und verwalten Sie Verbindungswege. Erfordert Zugriff auf den gesamten Arbeitsbereich. |
| `board.read` | Lesen Sie die Notizen im Case Board nur innerhalb des zulässigen Arbeitsbereichs und der zulässigen Chats. |
| `board.write` | Fügen Sie Lesezeichen, Markierungen, Ausschnitte, Kommentare sowie Öffnungs- und Überprüfungsstatus hinzu. Erfordert außerdem „`board.read`“. |
| `board.manage` | Verwalten Sie Sammlungen, endgültige Teamstatus und die Karten anderer Teilnehmer. Erfordert außerdem Lese- und Schreibzugriff auf das Board. |

Berechtigungen und Geltungsbereich werden gemeinsam geprüft. Das Aktivieren einer Berechtigung führt nicht dazu, dass andere Chats geöffnet werden oder bei einem auf einen Chat beschränkten Zugriff eine arbeitsbereichsweite Aktion freigeschaltet wird. Für einen parallelen Export muss der Zugriff den exportierten Chat in jedem ausgewählten Konto abdecken. Ein erteilter Zugriff darf keine neuen Zugriffe erstellen, keine Sitzungen anderer Personen verwalten oder die Administratorkonsole öffnen.

### Drei nützliche Konfigurationen

| Person | Geltungsbereich | Berechtigungen |
| --- | --- | --- |
| Rezensent | Aufgezeichnete Chats aus einem Fall | `view` |
| Analyst, der eine Übergabe vorbereitet | Die zu untersuchenden und zu exportierenden Chats | `view`, `export`; fügen Sie `interact` nur hinzu, falls diese über Telegram agieren sollen |
| Erfassungsoperator | Ausgewählte vollständige Arbeitsbereiche | `view`, `sources`, `collect`; fügen Sie `settings` oder `account` nur bei Bedarf hinzu |

Zu den Startvoreinstellungen des Zugriffsformulars gehört auch das Fall-Dashboard: Prüfer können lesen, Analysten können lesen und schreiben, und Betreiber können es verwalten. Die Voreinstellungen bleiben bearbeitbar, und bestehende Berechtigungen werden nicht automatisch erweitert. Siehe [Fall-Dashboard](https://phishdestroy.github.io/TgWitness/de/docs/reference/case-board/) für vererbte Chat-Bereiche und Exportdatenschutz.

## Beschränkungen und Sitzungen

| Einleitung | So funktioniert es |
| --- | --- |
| Parallelsitzungen | Begrenzen Sie die Anzahl gleichzeitiger Sitzungen auf 1–100. Bei Erreichen der Obergrenze lehnen Sie die nächste Anmeldung ab oder beenden Sie die älteste Sitzung. |
| Anmeldungen sind zulässig | Die Anzahl der erfolgreichen Verwendungen des Tokens zum Starten von Sitzungen ist begrenzt. Bestehende Sitzungen werden nicht beendet, nur weil die letzte zulässige Anmeldung genutzt wurde. |
| Gültig bis | Eine absolute Ablauffrist für den Zugriff. Bei abgelaufenem Zugriff ist eine Anmeldung oder die weitere Übermittlung von Anfragen nicht mehr möglich. |
| Minuten ohne Aktivität | Zeitlimit für Inaktivität in einer Sitzung: von 5 Minuten bis zu 30 Tagen. Erfolgreiche Anfragen verlängern dieses Limit; ein geöffnetes Fenster kann durch regelmäßige Abfragen seine Aktivität aufrechterhalten. |
| Zulässige Adressen | Geben Sie bestimmte IP-Adressen oder CIDR-Subnetze an. Lassen Sie das Feld leer, um alle Adressen zuzulassen, sofern die Bindung bei der ersten Anmeldung nicht aktiviert ist. |
| Bei der ersten Anmeldung verknüpfen | Bei der ersten erfolgreichen Anmeldung wird die zulässige Adresse für diesen Zugriff festgelegt. |

Die IP-Adresse ist die vom Programm erkannte Client-Adresse. Wenn Sie sich hinter einem Reverse-Proxy oder einem Tunnel befinden, überprüfen Sie bitte die unter **„Offene Sitzungen“** angezeigte Adresse, bevor Sie sich auf IP-Regeln verlassen: Andernfalls könnte es den Anschein haben, dass sich mehrere Benutzer die Adresse des Proxys teilen.

## Zugriff ändern oder widerrufen

Bearbeiten Sie einen Eintrag unter **„Gewährter Zugriff“**, um dessen Geltungsbereich, Berechtigungen oder Einschränkungen zu ändern. Änderungen am Geltungsbereich und an den Berechtigungen werden bei nachfolgenden Anfragen überprüft, einschließlich Anfragen aus bereits geöffneten Sitzungen. Das Widerrufen eines Zugriffs beendet dessen Sitzungen und macht das ausgestellte Token unbrauchbar. Über **„Offene Sitzungen“** kann der Administrator auch eine einzelne Sitzung beenden, ohne den gesamten Zugriff zu widerrufen.

Gespeicherte Exportkopien behalten ihren Ersteller, den Arbeitsbereich, den Chat-Umfang und die erforderlichen Berechtigungen bei. Ein berechtigter Nutzer kann seine eigenen Kopien nur so lange auflisten oder herunterladen, wie diese Berechtigungen noch gelten; Kopien, die das Case Board enthalten, erfordern zusätzlich die Berechtigung „`board.read`“. Der Administrator kann alle Kopien abrufen. Ältere Kopien ohne diese Metadaten sowie Gruppenbündel sind nur für den Administrator zugänglich. Download-Tickets und vorbereitete Dateiantworten überprüfen den Zugriff erneut nach der Vorbereitung der Datei, bevor deren Daten gesendet werden.

Durch eine Widerrufung können bereits heruntergeladene Dateien nicht wiederhergestellt werden. Das Abmelden, das Sperren des Fensters oder das Beenden einer Sitzung stoppt einen laufenden Collector nicht.

## Was der Administrator sehen kann

Prüfer und Analysten erhalten Informationen zum Erfassungsfortschritt ohne Proxy-Endpunkte, Pool-Diagnosen, Serverpfade oder rohe Verbindungsfehler. Für die Verbindungsdiagnose ist die Berechtigung „`account`“ für den gesamten Arbeitsbereich erforderlich. Das Lesen von Benachrichtigungen, Offsite-Kopien und Parametereinstellungen erfordert die Berechtigung „`settings`“.

Vollständige Browser-User-Agent-Zeichenfolgen werden in Zugriffssitzungen nicht beibehalten. Bei einem Upgrade werden sie zudem aus dem veränderbaren Sitzungscache entfernt. Das Protokoll des Panel-Prozesses maskiert IP-Literale, URL-Anmeldedaten und gekennzeichnete Geheimnisse. Lokale Dienstprotokolle und zuvor signierte Journal-Einträge werden nicht überschrieben. Zugriffsregeln und signierte Anmeldeeinträge verwenden weiterhin die Client-Adresse.

### Den Hauptschlüssel ersetzen

Verwenden Sie „**Access“ → „Meine Grenzen“ → „Administratorschlüssel** neu ausstellen“ oder führen Sie „ `tgwitness token rotate`“ von einer verwalteten Installation aus, während das Panel läuft. Alle bestehenden Browsersitzungen werden beendet, einschließlich der mit Kollegen- Tokens eröffneten Sitzungen. Der anfragende Browser erhält eine neue Sitzung; speichern Sie den neuen Administratorschlüssel, bevor Sie ihn ausblenden. Ausgestellte Kollegen-Tokens bleiben gültig, bis sie separat widerrufen werden. Bei einer Installation, die `TGWITNESS_TOKEN` verwendet, muss diese Umgebungseinstellung geändert und ein Neustart durchgeführt werden.

### Anfrage- und Proxy-Grenzen

Die API lässt bis zu 600 Anfragen pro Minute pro Client-IP zu. Zehn abgelehnte Authentifizierungen innerhalb einer Minute lösen eine exponentielle Sperrzeit aus, die von einer Sekunde bis zu fünf Minuten reicht. Ein fehlgeschlagener Versuch nach Ablauf der Sperrzeit verlängert diese; zehn Minuten ohne fehlgeschlagenen Versuch setzen die Eskalation zurück. Ablehnungen geben HTTP 429 und `Retry-After` zurück. Die Limits werden im Speicher verwaltet und von allen Arbeitsbereichen innerhalb eines Panel-Prozesses gemeinsam genutzt; ein Neustart löscht sie. Live-Streams sind auf vier pro Träger-Token und 32 für den Panel-Prozess begrenzt. Das Öffnen eines Streams verbraucht ebenfalls das API-Anfrage-Kontingent.

Für Request-Bodies gilt eine Empfangsfrist von 60 Sekunden (8 Sekunden für MCP). Jede Anwendung begrenzt unvollständige Request-Bodies auf 32 Anfragen und 64 MiB reservierte Routenkapazität. Übergroße Request-Bodies führen zu einem 413-Fehler, Request-Bodies mit abgelaufener Zeit zu einem 408-Fehler und erschöpfte Request-Body-Kapazität zu einem 503-Fehler mit „`Retry-After`“.

Weitergeleitete IP-Header werden ignoriert, es sei denn, der tatsächliche TCP-Peer gehört zu `TGWITNESS_TRUSTED_PROXIES` (durch Kommas getrennte IPs oder CIDRs). Setzen Sie `TGWITNESS_PROXY_HEADER` auf `x-forwarded-for` oder `cf-connecting-ip`. XFF wird vom nächstgelegenen Proxy in Richtung des ersten nicht vertrauenswürdigen Peers durchlaufen. Fehlerhafte oder doppelte Metadaten vertrauenswürdiger Adressen werden abgelehnt, sodass sie keine Proxy-Adresse aus der Zulassungsliste erben können. Der verwaltete Quick-Tunnel vertraut dem lokalen Cloudflare-Connector; die Eigen-Domain-Konfiguration vertraut lokalem Caddy. Direkte Bereitstellungen vertrauen standardmäßig keinem Proxy. Wenn Sie Uvicorn selbst starten, deaktivieren Sie dessen Proxy-Header-Verarbeitung, damit diese Grenze den tatsächlichen Peer empfängt.

`TGWITNESS_PANEL_ALLOWED_IPS` beschränkt den gesamten Zugriff auf das Panel, einschließlich des Administrators, auf aufgeführte IP-Adressen oder CIDRs. Die Routing-Identity-Prüfung des Installationsprogramms bleibt öffentlich und gibt keine Kontodaten zurück. Fügen Sie die erforderliche lokale Verwaltungsroute ein, bevor Sie die Zulassungsliste aktivieren. Der Leitfaden „**START-HERE**“ für eine verwaltete Installation enthält die Anweisungen zur Dienstkonfiguration und Wiederherstellung.

Ein API-Abfrage-Selektor vom Typ „`ws`“ muss den Arbeitsbereich im Anforderungspfad identifizieren; unbekannte, nicht übereinstimmende und doppelte Selektoren werden mit dem Status 404 abgelehnt.

Panel-Skripte und -Stile enthalten SHA-384-Integritätsmetadaten. Eine Import-Map deckt zudem lokal importierte JS-Module in Browsern ab, die die Integrität von Import-Maps unterstützen. Die dynamisch generierte Sprachantwort erfolgt separat. Diese Prüfungen erkennen die Ersetzung von Assets im Vergleich zur ausgelieferten Seite; sie begründen jedoch kein Vertrauen in einen kompromittierten Server, der sowohl die Seite als auch deren Hashes ersetzen kann.

**Das Protokoll seit dem Start** kombiniert Prozessprotokolle mit Protokollaktivitäten aus jedem Arbeitsbereich: Anmeldungen, Ablehnungen, Routenänderungen und Bedieneraktionen. Es handelt sich um eine In-Memory-Konsole für den aktuellen Prozess, nicht um eine dauerhafte Kopie jeder einzelnen Nachricht. Häufig auftretende Nachrichtenereignisse verbleiben im Protokoll, anstatt die Konsole zu überfüllen.

Das Erteilen, Ändern und Widerrufen von Zugriffsrechten sowie das Starten oder Beenden von Sitzungen führen ebenfalls zur Erstellung signierter `access.*`-Protokollaufzeichnungen. Token sind in diesen Aufzeichnungen nicht enthalten. Ausgegebene Token und Sitzungszugangsdaten werden als Hash-Werte im verschlüsselten Tresor gespeichert.

****Hauptadministrator und Vertrauensgrenze****

Das Haupt-Panel-Token unterliegt keinen Einschränkungen. Browser-Anmeldungen mit diesem Token erstellen Sitzungen, die den vom Administrator konfigurierten Sitzungslimits unterliegen. Skripte, die das Haupt-Token direkt senden, behalten den vollen Zugriff und werden nicht als Browsersitzungen gezählt.

Es handelt sich hierbei um eine Zugriffskontrolle auf Anwendungsebene innerhalb einer Installation. Alle Arbeitsbereiche nutzen gemeinsam den Serverprozess; es besteht keine Isolierung vom Host-Administrator. Halten Sie das Haupt-Token, die Telegram-Sitzungen, die Signaturschlüssel und das Datenverzeichnis geheim. Ein Witness-Token ist ein separater Checkpoint/Zustandsnachweis, kein Zugriffstoken für das Panel.
