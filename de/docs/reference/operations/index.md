# Arbeitsabläufe und Funktionen

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/operations/

Täglicher Betrieb des Dashboards: Betriebsmodi, Überwachungskategorien, Parameter, Benachrichtigungen, Exporte, Datensicherung und Kapazität.

Verwenden Sie für Ihre erste Verbindung [Konten und Sitzungsformate](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/). Eine Erläuterung zu gespeicherten Versionen, Ereignisrichtlinien und Lücken finden Sie unter [„So funktioniert die Erfassung](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/)“. Dieser Leitfaden behandelt den täglichen Betrieb und die Wiederherstellung.

## Arbeitsablauf für Bediener

Ablaufdiagramm · Wählen Sie Speicherort und Schlüsselschutz → Öffnen Sie das Fenster mit dem entsprechenden Token; Öffnen Sie das Fenster mit dem entsprechenden Token → Wählen Sie einen Arbeitsbereich aus; Wählen Sie einen Arbeitsbereich aus → Direkte oder Proxy-Route konfigurieren; Direkte oder Proxy-Route konfigurieren → Geben Sie Ihre Telefonnummer ein oder wählen Sie Dateien / QR-Code aus; Geben Sie Ihre Telefonnummer ein oder wählen Sie Dateien / QR-Code aus → Überprüfen Sie die Kontoidentität und wählen Sie zugängliche Gruppen aus; Überprüfen Sie die Kontoidentität und wählen Sie zugängliche Gruppen aus → Richten Sie Richtlinien für Ereignisse und Anhänge ein und beginnen Sie anschließend mit der Überwachung; Richten Sie Richtlinien für Ereignisse und Anhänge ein und beginnen Sie anschließend mit der Überwachung → Fehler, Zugriff, Warteschlangen und Festplattenspeicher überwachen; Fehler, Zugriff, Warteschlangen und Festplattenspeicher überwachen → Unabhängige Kontrollpunkte beibehalten; Unabhängige Kontrollpunkte beibehalten → Material exportieren und verifizieren · Wählen Sie Speicherortund Schlüsselschutz · Öffnen Sie das Fenstermit dem entsprechendenToken · Wählen Sie einenArbeitsbereich aus · Direkte oderProxy-Routekonfigurieren · Geben Sie IhreTelefonnummer ein oderwählen Sie Dateien /QR-Code aus · Überprüfen Sie dieKontoidentität undwählen Sie zugänglicheGruppen aus · Richten SieRichtlinien fürEreignisse und Anhängeein und beginnen Sieanschließend mit derÜberwachung · Fehler, Zugriff,Warteschlangen undFestplattenspeicherüberwachen · UnabhängigeKontrollpunktebeibehalten · Material exportierenund verifizieren

**Diagramm als Text**

1. Wählen Sie Speicherort und Schlüsselschutz → Öffnen Sie das Fenster mit dem entsprechenden Token
2. Öffnen Sie das Fenster mit dem entsprechenden Token → Wählen Sie einen Arbeitsbereich aus
3. Wählen Sie einen Arbeitsbereich aus → Direkte oder Proxy-Route konfigurieren
4. Direkte oder Proxy-Route konfigurieren → Geben Sie Ihre Telefonnummer ein oder wählen Sie Dateien / QR-Code aus
5. Geben Sie Ihre Telefonnummer ein oder wählen Sie Dateien / QR-Code aus → Überprüfen Sie die Kontoidentität und wählen Sie zugängliche Gruppen aus
6. Überprüfen Sie die Kontoidentität und wählen Sie zugängliche Gruppen aus → Richten Sie Richtlinien für Ereignisse und Anhänge ein und beginnen Sie anschließend mit der Überwachung
7. Richten Sie Richtlinien für Ereignisse und Anhänge ein und beginnen Sie anschließend mit der Überwachung → Fehler, Zugriff, Warteschlangen und Festplattenspeicher überwachen
8. Fehler, Zugriff, Warteschlangen und Festplattenspeicher überwachen → Unabhängige Kontrollpunkte beibehalten
9. Unabhängige Kontrollpunkte beibehalten → Material exportieren und verifizieren

Authentifizierung, Transportverbindung, Zugriff auf eine Gruppe und Vollständigkeit der Übermittlung sind unterschiedliche Eigenschaften. Ein grüner Verbindungsstatus bedeutet nicht, dass alle Ereignisse erfasst wurden.

## Arbeiten teilen, ohne den Hauptschlüssel weiterzugeben

Offener **Zugriff**, um einem Prüfer oder Analysten ein eigenes Token zuzuweisen. Wählen Sie die Konten und Chats aus, die diese Personen öffnen dürfen, und erteilen Sie ihnen anschließend Berechtigungen zum Anzeigen, Exportieren oder Ausführen von Aktionen. Ein Operator, der die Erfassung startet oder stoppt, benötigt Zugriff auf den gesamten Arbeitsbereich; ein Prüfer kann auf einen einzelnen Chat beschränkt werden. Sitzungslimits, Ablaufzeiten und IP-Regeln sind unabhängig von der Telegram-Kontoautorisierung. Siehe [„Zugriff und Berechtigungen](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/)“.

Verwenden Sie **„Offene Sitzungen“,** um eine Verbindung zu beenden, oder widerrufen Sie den Zugriff, um alle zugehörigen Sitzungen zu beenden. Die Administratorkonsole fasst die Aktivitäten der laufenden Prozesse über alle Arbeitsbereiche hinweg zusammen. Beim Schließen einer Sitzung läuft die Erfassung weiter.

## Ausführungsmodi

| Modus | Maßnahme | Verhalten |
| --- | --- | --- |
| Demo | scripts\Demo.cmd oder `--demo` | Synthetische Daten; Verknüpfungen zu echten Konten deaktiviert |
| Anmerkung | Beobachtung starten | Erfassung der bereitgestellten Aktualisierungen für ausgewählte Quellen |
| Historischer Überblick | Quellen → Momentaufnahme der Versionsgeschichte | Bis zu 500 aktuelle Nachrichten; keine Rekonstruktion aller vergangenen Änderungen |
| Pause | Beobachtung unterbrechen | Erfassung unterbrechen, dabei Daten und Aufträge in der Warteschlange beibehalten |
| Überprüfung/Übergabe | Exporte | ZIP, JSONL/CSV/HTML, Checkpoint, Prozessbestätigung und Zeitstempelanforderung |
| Mehrere Konten | Arbeitsbereiche oder die oberste Schaltfläche „**+**“ | Beliebig viele separate Arbeitsbereiche in einem Prozess |

Der lokale Demo-Zugriff wird automatisch ohne manuelle Token-Eingabe freigeschaltet. Dabei kommt eine auf die Prozesslaufzeit begrenzte Funktion zum Einsatz, die ausschließlich für den direkten Loopback-Zugriff auf eine isolierte synthetische Demo gilt; das Token für das Hauptpanel wird nicht offengelegt. Bei echten Arbeitsbereichen sowie beim Remote- oder Proxy-Zugriff auf die Demo bleibt die Token-Authentifizierung bestehen. Der Demo-Zugang gewährt keine Telegram-Berechtigung.

## Überwachungskategorien

![Überwachungseinstellungen pro Konto mit synthetischen Quelldaten](https://phishdestroy.github.io/TgWitness/assets/sources.png)

**Wählen Sie** unter **„Quellen“ → „Erfassungseinstellungen“ → „Zu speichernde Änderungen auswählen“ die Optionen** „Neue Nachrichten“, „Bearbeitungen“, „Löschmeldungen“, „Reaktionsaktualisierungen“ und „Mitgliedschaftsereignisse“ einzeln aus. In der Standardeinstellung werden alle Kategorien beibehalten. Die Option **„Nachrichten, Bearbeitungen und Löschungen“** bewahrt den ursprünglichen Kontext bei, während separate Reaktions- und Mitgliederaktualisierungen deaktiviert werden. **„Alle sichtbaren Aktivitäten“** stellt alle fünf Kategorien wieder her. Voreinstellungen ändern die Darstellung; klicken Sie auf **„Überwachungseinstellungen speichern“,** um die Änderungen zu übernehmen.

Die gespeicherte Richtlinie gilt für alle ausgewählten Quellen in diesem Arbeitsbereich. Andere Arbeitsbereiche behalten ihre eigenen Einstellungen bei. Bei jeder tatsächlichen Änderung werden signierte Vorher-Nachher-Werte aufgezeichnet; die aktuelle Richtlinie wird zudem in Prozessbelegen und Beobachtungsstartprotokollen erfasst. Das Deaktivieren einer Kategorie löscht frühere Beobachtungen nicht. Durch erneutes Aktivieren werden versäumte Änderungen nicht nachträglich erfasst. In dieser Version gibt es keine gruppenspezifische Übersteuerung von Kategorien.

Behalten Sie die Erfassung neuer Nachrichten bei, wenn frühere Inhalte von Bedeutung sind: Eine Löschmeldung kann keinen Text wiederherstellen, der nie erfasst wurde. Betriebs- und Erfassungsprotokolle sowie andere Ereignisse im Zusammenhang mit Gruppendiensten werden stets beibehalten. Explizite Verlaufs-Snapshots sind unabhängig von der Auswahl der Live-Kategorien und können Dienstmeldungen enthalten. Diese Einstellungen führen nicht zur Schwärzung von Reaktions- oder Mitglieder-Metadaten, die in einem ansonsten erfassten Telegram-Objekt eingebettet sind.

Ein Verlaufs-Snapshot kann Anhänge in die Warteschlange stellen, während er angehalten ist. Starten Sie die Beobachtung, um diese zu verarbeiten. „In der Warteschlange“ bedeutet nicht „heruntergeladen“. Eine nicht verfügbare Originaldatei wird nicht durch eine neuere bearbeitete Version ersetzt; die Ergebnisse werden separat aufgezeichnet.

**Mit „Lock“** werden der Browserzugriff und geheime Felder gelöscht, die Erfassung läuft jedoch weiter. Auch beim Schließen eines Tabs läuft der Prozess weiter. Das Beenden des Python-Prozesses oder -Dienstes stoppt die Erfassung unabhängig vom Status des Browsers.

Das Löschen eines zusätzlichen Arbeitsbereichs stoppt dessen Datenerfassung und entfernt dessen lokale Daten. Sollte eine gesperrte Datei oder ein Dateisystemfehler den Löschvorgang unterbrechen, meldet das Bedienfeld den Fehler und führt den Arbeitsbereich weiterhin als nicht verfügbar (`DeletionPending`) auf. Schließen Sie Programme, die dessen Dateien öffnen, und versuchen Sie **den Löschvorgang** erneut. Ein Neustart von TgWitness belässt diesen Arbeitsbereich im angehaltenen Zustand und stellt das teilweise entfernte Protokoll oder die Schlüssel nicht wieder her. Eine erfolgreiche Löschung wird erst dann protokolliert, wenn das Verzeichnis entfernt wurde; separat exportierte oder gesicherte Kopien unterliegen weiterhin ihrer eigenen Aufbewahrungsrichtlinie.

## Benachrichtigungen

Open **Sources → Benachrichtigungen → Warnmeldungen und eine tägliche Zusammenfassung**. TgWitness nutzt Apprise, um Warnmeldungen an Matrix, Telegram, Discord, Slack, ntfy, E-Mail und andere unterstützte Dienste zu senden. Sie können einem Arbeitsbereich mehrere Ziele hinzufügen.

1. Geben Sie pro Zeile eine Apprise-Ziel-URL ein. Verwenden Sie den [Servicekatalog und die URL-Formate](https://appriseit.com/services/) für Ihren Dienst.
2. Aktivieren Sie die Option **„Benachrichtigungen senden**“ und wählen Sie anschließend Problemwarnungen, Änderungen in beobachteten Chats sowie eine tägliche Zusammenfassung aus. Die Uhrzeit in der Zusammenfassung richtet sich nach der Serverzeit.
3. Aktivieren Sie die Option**„Kurze Auszüge einbeziehen“,** wenn Sie möchten, dass Text aus gelöschten und bearbeiteten Nachrichten in den Benachrichtigungen gespeichert wird.
4. Klicken Sie auf **„Benachrichtigungen speichern**“ und anschließend auf **„Test senden“**, um die Zustellung zu überprüfen.

Verwenden Sie für Ihren eigenen Empfänger [den JSON-Webhook](https://appriseit.com/services/json/) von Apprise. Beispielsweise sendet „`jsons://notify.example.org/tgwitness`“ JSON über HTTPS an diesen Endpunkt. Dies ist ein fiktives Beispiel; ersetzen Sie es durch Ihr eigenes Ziel.

Ziele und Einstellungen gehören zum ausgewählten Arbeitsbereich. Änderungsbenachrichtigungen umfassen die überwachten Quellen, einschließlich neu hinzugefügter Chats. Die Glocke in der oberen Leiste listet zudem aktuelle Probleme und Änderungen in Chats auf.

In der Demo sind die Benachrichtigungssteuerelemente sichtbar, das Versenden ist jedoch deaktiviert. Konfigurieren Sie die Zustellung in einem realen Arbeitsbereich. Benachrichtigungen nutzen die Direct-, SOCKS5- oder HTTP-Route dieses Arbeitsbereichs; MTProxy kann sie nicht weiterleiten. Nicht-HTTP-Ziele wie SMTP erfordern eine direkte Route.

## Layout der Seiten

![Arbeitsbereich für die Anbindung unter Verwendung synthetischer Daten](https://phishdestroy.github.io/TgWitness/assets/connection.png)

**Das Protokoll** zeigt Beobachtungen, Suchfunktionen und Filter an. Bei einer Bearbeitung werden die erfassten Versionen angezeigt; bei einer Löschung wird der vorherige Inhalt angezeigt, sofern verfügbar. Unbekannte Quellenangaben bleiben ausdrücklich gekennzeichnet. Zahlenangaben sind unter **„Übersicht“** verfügbar; Details zur Erfassung verbleiben im lokalen Leitfaden.

**Der Bereich „Quellen“** umfasst den Überwachungsumfang (ausgewählte Chats, einen Telegram-Ordner oder das gesamte Konto), zugängliche Chats aller Art, ausgewählte Quellen mit Prioritätssternen, Einstellungen für Anhänge und Nachprüfungen sowie Momentaufnahmen des Verlaufs. Private Quellen werden anhand des Dialogs/der ID ohne öffentlichen Link ausgewählt. Der Zugriffsstatus beschreibt die letzte Überprüfung, nicht dauerhafte Berechtigungen.

Unter **„Chats → Personen“** werden alle Personen mit gespeicherten Nachrichten aufgelistet; sind die Personenprofile für den Chat aktiviert, öffnet ein Klick das Profil der jeweiligen Person mit Links zu den Protokollen.

**Witness** erstellt schreibgeschützte Witness-Token, zeigt an, wann jeder Witness zuletzt überprüft wurde, und stellt die Befehle und Optionen zur Verfügung, um einen ([unabhängigen Witness](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/)) auszuführen.

**Unter „Parameter“** sind alle Grenzwerte und Zeitrhythmen des Arbeitsbereichs zusammengefasst, die nicht auf einer anderen Seite aufgeführt sind: die Anzahl der gelesenen Dialoge, die Häufigkeit der Neuauswertung der Chat-Liste, Heartbeat- und Checkpoint-Intervalle, der Startpuffer, die Verteilung der Anfragen bei erneuten Überprüfungen (erste Verzögerung, Chats pro Durchlauf, Pause zwischen Chats, wiederhergestellte und erneut angeforderte Nachrichten), Festplattenreserve, Timeouts und Wiederholungsversuche bei Downloads, wonach bei Benutzerprofilen gesucht wird (einschließlich Ihrer eigenen regulären Ausdrücke), Umfang und Häufigkeit von Benachrichtigungen, Limits für Snapshots, ZIP-Dateien und Browser-Downloads sowie Telegram- Client-Timeouts und Wiederholungsversuche. Jedes Feld zeigt seinen Wertebereich und den Standardwert an; geänderte Felder sind markiert und können einzeln oder alle zusammen wiederhergestellt werden. Jede Änderung wird als „`parameters.changed`“ mit den Werten vor und nach der Änderung protokolliert, und die Aufzeichnungen zum Beginn der Beobachtung nennen die jeweils geltenden Werte. Die Werte gelten ab ihrer nächsten Verwendung; Zeitlimits und Wiederholungsversuche des Clients gelten ab der nächsten Verbindung. Überprüfungsintervalle, Anhangstypen und -größen sowie Intervalle für Sicherungskopien und externe Kopien bleiben auf ihren eigenen Seiten und können beliebige Werte innerhalb ihres Bereichs annehmen, nicht nur voreingestellte Werte.

Die Glocke in der oberen Leiste listet aktuelle Probleme und Änderungen in den überwachten Chats auf; ungelesene Einträge werden gezählt, bis sie als gelesen markiert werden. Änderungen werden nach Chat und Stunde gruppiert („12 gelöscht, 1 bearbeitet, 0 nicht gefunden“), und Probleme wie eine Abmeldung oder ein voller Speicherplatz bleiben in der Liste, unabhängig davon, wie aktiv die Chats sind.

**Die Kontoeinrichtung** beginnt im Feld für die Telefonnummer. **Wenn Sie fortfahren**, gelangen Sie direkt zur Codeeingabe; API-Anmeldedaten werden nur abgefragt, wenn diese fehlen. QR-Code und Dateiimport sind alternative Registerkarten. Gespeicherte API-Anmeldedaten werden nur innerhalb des jeweiligen Arbeitsbereichs wiederverwendet. Der Eingabebildschirm enthält keine Seitenleiste, keine Statistiken und keine Einrichtungsabschnitte. Das Symbol **„Einstellungen**“ öffnet die Steuerelemente für API, Proxy, Speicher und zusätzliche Konten. Neue Installationen beginnen hier; verbundene Konten ohne ausgewählte Quellen beginnen bei **„Chats auswählen**“. Das Ändern der Route erfordert eine Unterbrechung der Überwachung und bricht einen noch nicht abgeschlossenen Anmeldevorgang ab. Ein bestehendes Protokoll kann nicht im Hintergrund mit einem anderen Telegram-Konto verknüpft werden.

**Der Export** überprüft die Integrität des Protokolls und erzeugt portierbare Dateien. Die Arbeitsbereichs-ID kann an die Download-Befehlszeilenschnittstelle übergeben werden. Jeder Export versieht ein vollständiges Protokoll mit einem Präfix; spätere Ereignisse werden in einem nachfolgenden Export erfasst. Suchfilter ändern den Umfang des Pakets nicht. Detaillierte Informationen zur Signatur und zum Erfassungsumfang finden Sie unter **„Verifizierung und Einschränkungen**“.

Das Dashboard zeigt unter „Collector**-Status“** den Status des Collectors, Medien in der Warteschlange bzw. fehlgeschlagene Medien, die ältesten ausstehenden Medien, freien Speicherplatz, angehaltene Anfragen sowie Quellen an, deren Zugriff unter **„Collector-Status“**noch nicht bestätigt ist. Diese Details sind zunächst ausgeblendet und auf der Registerkarte „Konto“ verborgen. Eine Einrichtungskarte zeigt den nächsten Schritt an: ein Konto verbinden, Quellen auswählen oder die Überwachung starten. Die Konto-Liste ist eine Momentaufnahme zum Zeitpunkt des Ladens; der ausgewählte Arbeitsbereich wird regelmäßig aktualisiert. Es handelt sich hierbei nicht um einen SLA-Monitor mit mehreren Prozessen.

Die Benutzeroberfläche nutzt lokale Ressourcen und Textdarstellung für Quellinhalte. Desktop- und schmale Chromium-Layouts wurden getestet. Dies stellt keine vollständige Zertifizierung der Barrierefreiheit dar; die Bewertung der Benutzerfreundlichkeit durch Screenreader und durch Menschen erfolgt weiterhin separat.

## Bereitstellungsumgebungen

| Umfeld | Installation | Verifizierungsstatus |
| --- | --- | --- |
| Windows-PC/Server | Python 3.11+, Skripte: „Setup.cmd/Start.cmd“, Verzeichnis für private Daten | Lokal getestet unter Windows/Python 3.12 |
| Linux-Server/VPS | Python-venv, dedizierter Service-Benutzer, HTTPS/SSH | Beispiele für Code, CI und systemd werden bereitgestellt; die Ausführung erfolgt nicht auf diesem Host |
| macOS | Python-venv, Vordergrundprozess oder User-Agent | Beispiel für „launchd“ bereitgestellt; separate Installationsprüfung erforderlich |
| Docker/Compose | Persistenter Speicher, ein Worker | Definition und CI-Laufzeitprüfung werden bereitgestellt; Docker ist lokal nicht verfügbar |
| Mobilbrowser | Stellen Sie eine Verbindung zum geschützten Panel auf einem laufenden Server her | Getestet mit schmalem Chromium-Layout; der Collector läuft nicht unter iOS/Android |

Portabilität bedeutet, dass kein Cloud-Dienst und kein Frontend-Build zwingend erforderlich sind. Jedes Zielsystem benötigt jedoch weiterhin kompatible Python-/Krypto-Abhängigkeiten sowie lokalen Festplatten- und Netzwerkzugriff. Siehe [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/de/docs/reference/deployment/) und [die Service-Vorlagen](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md).

Arbeitsbereiche teilen sich CPU, Arbeitsspeicher und eine Ereignisschleife. Verwenden Sie zur Prozessisolierung unterschiedliche Instanzen, Ports, Datenverzeichnisse und Kontoberechtigungen. Es gibt kein einheitliches Kontrollpanel für separate Instanzen. Richten Sie niemals mehrere Worker auf eine einzige Datenbank aus.

## Startvorgänge und Exporte

Führen Sie „`python start.py --check`“ aus, bevor Sie eine vorbereitete Umgebung starten. Fügen Sie „`--json`“ für maschinenlesbare Prüfungen hinzu oder übergeben Sie die vorgesehenen Werte für „`--data-dir`“, „`--host`“ und „`--port`“. Der Befehl überprüft die Voraussetzungen, ohne dass eine Telegram-Anmeldung erforderlich ist oder ein Protokoll erstellt wird. Er überprüft weder ein Protokoll noch stellt er die Aufnahmebereitschaft sicher; die Protokollüberprüfung erfolgt beim Start der Anwendung. Ein belegter Port kann lediglich auf eine bereits vorhandene Instanz hinweisen.

Browser, die die File System Access API unterstützen, speichern Exporte über einen beschreibbaren Stream. Andere Browser puffern maximal 128 MiB. Verwenden Sie die Streaming-CLI für größere Exporte oder für Browser ohne Datei-Streaming:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Fügen Sie „`--profile ID` “ aus „Exports“ für einen untergeordneten Arbeitsbereich hinzu. Verwenden Sie „`--url https://server` “ für den Fernzugriff. Einfaches HTTP wird nur für Loopback-Ziele akzeptiert. Das Token wird aus einer Datei gelesen und in einem Header gesendet; es wird weder ausgegeben noch in eine URL eingefügt. Weiterleitungen werden abgelehnt. Vorhandene Ziele werden nicht überschrieben. Bei fehlgeschlagenen Übertragungen wird die temporäre Teil-Datei entfernt. Der gemeldete SHA-256-Wert ist eine Übertragungsprüfsumme; überprüfen Sie die signierte ZIP-Datei separat anhand eines vertrauenswürdigen Fingerabdrucks/Checkpoints.

## Sicherung, Wiederherstellung und Unterbrechungen

1. Die Überwachung unterbrechen und den Vorgang ordnungsgemäß beenden.
2. Kopieren Sie das gesamte Datenverzeichnis: Datenbanken, WAL/SHM (falls vorhanden), Medien, `credentials.enc`, `signing.enc`, `network.enc`, Tresorschlüssel/Metadaten, Token, Checkpoints und jedes `profiles/`-Verzeichnis.
3. Im Modus mit externem Schlüssel sind der Hauptschlüssel separat aufzubewahren und jeder „ `vault.external.json`“-Wert zu sichern. Durch die Generierung eines neuen Schlüssels lassen sich die alten Geheimnisse nicht wiederherstellen.
4. Führen Sie die Wiederherstellung durch, während das Zielsystem angehalten ist; konfigurieren Sie den ursprünglichen Schlüssel, beschränken Sie den Zugriff und überprüfen Sie die Integrität, bevor Sie den Vorgang fortsetzen.
5. Erfassen Sie Ausfallzeiten und Verifizierungsergebnisse. Eine Momentaufnahme des Verlaufs kann nicht beweisen, dass während der Unterbrechung keine Löschungen stattgefunden haben.

Die ZIP-Dateien mit den Beweismitteln enthalten keine Sitzungsdaten oder privaten Schlüssel und stellen keine vollständigen Service-Backups dar. Vier Elemente werden unterschiedlich geschützt:

| Was | Schutz |
| --- | --- |
| Dateien ohne Passwort exportieren (Standardeinstellung) | Nicht verschlüsselt. Signiert, sodass Änderungen nachweisbar sind, aber jeder, der die Datei besitzt, kann sie lesen. |
| Dateien mit einem Passwort exportieren | Wenn Sie ein Passwort festlegen, wird der fertige Export unverändert in eine WinZip-ZIP-Datei mit AES-256-Verschlüsselung gespeichert, die sich mit 7-Zip und WinRAR öffnen lässt; das Passwort wird nicht gespeichert ([Beweismittelbehandlung](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/)). |
| Die Protokoll-Datenbank und die auf der Festplatte gespeicherten Anhänge | Nicht durch TgWitness verschlüsselt; verwenden Sie eine verschlüsselte Festplatte oder ein verschlüsseltes Volume |
| Telegram-Sitzungen und Signaturschlüssel | Verschlüsselt im Datenverzeichnis (`credentials.enc`, `signing.enc`, `network.enc`) |

Ein Vollsicherungs-Backup ist das oben beschriebene Verzeichnis mit den gesicherten Daten, kein Export. Verwenden Sie für beides einen geschützten Speicher und einen kontrollierten Übertragungsmechanismus. Vorläufige Server-Exporte werden im Verzeichnis „ `temporary-exports/`“ des jeweiligen Arbeitsbereichs gespeichert; abgeschlossene Antworten werden bereinigt, und unterbrochene Exportdateien werden beim nächsten Start entfernt, solange die Instanzsperre dieses Arbeitsbereichs aufrechterhalten wird.

Ein Ereignis zur Wiederherstellung der Verbindung garantiert nicht die Wiederherstellung zwischenzeitlicher Änderungen. Persistente Medienaufträge und der Telegram-Aktualisierungsstand bleiben nach einem Neustart erhalten; siehe [Beweismittelformat](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#durable-collection-and-process-receipts-02).

## Kapazität und Aufbewahrungsdauer

Standardgrenzwerte, die alle unter **„Parameter“** geändert werden können: die ersten 1.000 Dialoge, 500 Nachrichten pro Snapshot, 4 GiB unkomprimierter, signierter ZIP-Inhalt (größere Archive erfordern „ `verify.py --max-gib N`“) und ein 128 MiB großes Browser-Fallback. Anhänge belegen 1–2.000 MiB pro Typ unter **„Quellen“ → „Anhänge**“. Die Download-Befehlszeilenschnittstelle ist standardmäßig auf 5 GiB Datenübertragung eingestellt. Der verfügbare Speicherplatz kann eine untere Grenze darstellen. Reservieren Sie Speicherplatz für Protokolle, Medien, WAL, temporäre Exporte und Sicherungen. Exporte nutzen das Datenvolumen anstelle der 512 MiB „`/tmp`“-Einstellung von Compose.

Messen Sie Ereignisse pro Sekunde, das Alter der Warteschlange, Medienbytes und die Festplattenlatenz, anstatt lediglich Gruppen zu zählen. Synthetische lokale Benchmarks garantieren keine Telegram-Zustellung. Es erfolgt keine automatische Löschung bei Aufbewahrungsfristen. Das Entfernen des Endes eines Protokolls macht dessen Bezug zu den aufbewahrten Kontrollpunkten ungültig.

Prioritäre Nachprüfungen sind bereits vorhanden: Mit einem Stern markierte Quellen werden standardmäßig alle 15 Minuten erneut überprüft, andere alle 6 Stunden (siehe [Nachprüfungsstufen](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/#recheck-tiers)). Passwortgeschützte Exporte sind wie oben beschrieben verfügbar. Live-Telegram-/Proxy-Akzeptanz, dauerhafte Wiedergabe, Admin-Protokoll und Reaktionsabfrage, isolierte Worker, Verschlüsselung des lokalen Protokolls und der Medien durch TgWitness selbst sowie unabhängige Überprüfung bleiben separate Arbeitsbereiche. Der bereichsbezogene Zugriff ist unter [„Zugriff und Berechtigungen“](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/) dokumentiert. Siehe [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md), [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) und [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/).
