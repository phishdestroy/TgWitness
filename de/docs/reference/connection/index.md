# Verbindung, Proxys und Datenschutz

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/

Authentifizierung, automatische Proxy-Pools, IP-Modi, Fallback-Richtlinie, externe Anfragen und Speicherung von Geheimnissen.

Dieses Dokument beschreibt das Verhalten von TgWitness 0.7.0 und dessen Grenzen. Authentifizierung, Zugriff auf die Quelle, Netzwerkverbindung und Vollständigkeit der Erfassung sind separate Zustände. Informationen zu Anmeldeschritten, Dateiformaten und mehreren Konten finden Sie unter [„Konten und Sitzungsformate](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/)“. Informationen zu Ereignisrichtlinien und zum Verhalten bei einem Neustart finden Sie unter [„So funktioniert die Erfassung](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/)“.

## Authentifizierungsmethoden

**Die API-ID und der API-Hash identifizieren eine Anwendung; sie ersetzen nicht die Kontoanmeldung.** Sie sind in TgWitness optional. Prioritätsreihenfolge: ein im Formular eingegebenes Paar, dann eines aus einer importierten Konto-JSON-Datei, dann das im Arbeitsbereich gespeicherte Paar, dann der integrierte Pool von 50 öffentlichen Paare, die in zufälliger Reihenfolge ausprobiert werden, mit automatischer Rotation, wenn Telegram eines ablehnt. Nur das Telegram-Desktop-Paar (2040) wird zusammen mit einer passenden Beschreibung des Telegram-Desktop-Clients gesendet. Ihr eigenes Paar aus den API-Entwicklungstools unter [my.telegram.org](https://my.telegram.org) kann für alle Ihre Konten verwendet werden; jedes Konto verfügt weiterhin über eine eigene Autorisierung.

| Vorgehensweise | Anforderungen | TgWitness-Support |
| --- | --- | --- |
| Telefonnummer, Code, optionale 2FA | Zugriff auf das Konto; API-Paar optional | Anmeldung im Panel |
| Authentifizierungsschlüssel (HEX) + DC-ID | Vollständiger 512-Zeichen-Schlüssel und DC 1–5 | Registerkarte „Direct **Auth Key“**; optionale Benutzer-ID wird vor dem Speichern der Autorisierung überprüft |
| Telethon StringSession | Eine gültige Sitzungs-Zeichenkette | Anmeldung im Panel |
| Telethon SQLite `.session` | Abgeschlossener, konsistenter Text | Direkter Import von Schemata über das Bedienfeld 7/8; optionale Offline-Befehlszeilenschnittstelle (CLI) |
| Pyrogram SQLite `.session` | Geschlossene Produktionssitzung | Direkter Import von Schemata über das Bedienfeld 2/3 |
| Telegram Desktop TData ZIP | Ein modernes Konto; lokaler Passcode, falls geschützt | In-Memory-Konvertierung mit Prüfsummen- und Entschlüsselungsprüfungen |
| JSON-Datei für das Konto | Unterstützte API-/Sitzungs-/Schlüssel-Felder | Die Metadaten allein reichen nicht aus, um die API-Anmeldedaten zu füllen; eine Anmeldung per Sitzung/Schlüssel oder per Telefon/QR-Code ist weiterhin erforderlich. |
| QR-Anmeldung | Bestätigung durch eine autorisierte Telegram-App | Lokale QR-Code-Generierung, Ablauf/Wiederholungsversuch, optionale 2FA |
| TDLib / Pyrogram StringSession | Weitere bibliotheksspezifische Formate | Nicht unterstützt |
| Bot-Token | Ein Bot mit eigenem Zugriffs- und Aktualisierungsmodell | Wird von diesem Sammler nicht verwendet |

Telegram wählt die Zustellung per Code; die Zustellung per SMS ist nicht garantiert. Ein API-Hash kann eine widerrufene Sitzung nicht wiederherstellen oder ein vergessenes 2FA-Passwort ersetzen. TgWitness speichert Anmeldecodes oder das Telegram-2FA-Passwort nicht auf der Festplatte.

Bei einer privaten Quelle muss das Konto bereits über Zugriffsrechte verfügen. Ein Gruppenbenutzername ist nicht erforderlich. Ein Proxy oder ein Sitzungsimport gewährt weder Mitgliedschafts- noch Administratorrechte. Eine aktuelle Mitgliedschaft garantiert keinen Zugriff auf den Verlauf vor dem Beitritt.

## Eine Telethon-Sitzungsdatei importieren

Telethon SQLite, Pyrogram SQLite und Telegram Desktop TData verwenden unterschiedliche Formate. Das Bedienfeld erkennt und konvertiert die unterstützten Strukturen; das Umbenennen einer Datei gilt nicht als Konvertierung. Wählen Sie unter **„Dateien“** eine Sitzung und die dazugehörige JSON-Datei aus und klicken Sie anschließend auf **„Konto verbinden**“. Es werden bis zu vier übereinstimmende Dateien und insgesamt 8 MiB akzeptiert. Einzelheiten zu TData/JSON finden Sie unter [„Formatbeschränkungen](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/)“. Es gibt keine Wiederherstellung des Passworts. Die Anmeldung per Telefon/2FA oder QR-Code erstellt eine separate Autorisierung.

Der optionale, ausschließlich für Telethon vorgesehene Befehlszeilenpfad steht weiterhin zur Verfügung:

1. Beenden Sie den Client unter Verwendung der ursprünglichen Sitzung und erstellen Sie eine konsistente Kopie. Der Konverter lehnt Dateien mit einem unvollständigen WAL/Journal ab. Schließen Sie den ursprünglichen Client ordnungsgemäß, anstatt diese Dateien zu löschen, um die Überprüfung zu umgehen.
2. Führen Sie in der TgWitness-Umgebung folgenden Befehl aus:

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. Laden Sie unter **„Konto hinzufügen“ → „Dateien**“ das Ergebnis hoch oder fügen Sie den entsprechenden Text ein und fahren Sie fort.
2. Überprüfen Sie die angezeigte numerische Konto-ID, wählen Sie die Quellen aus und beginnen Sie mit der Beobachtung.

Der Konverter öffnet SQLite im schreibgeschützten Modus, führt weder eine Schemaaktualisierung noch eine Netzwerkanfrage durch und gibt die Sitzung nicht aus. Er überprüft die Schemaversion, die Tabellentypen, eine einzelne Sitzungszeile, IP/Port/DC sowie die Schlüssellänge. Die CLI-Eingabe ist auf 64 MiB begrenzt; der Text von „StringSession“ ist auf 4 KiB begrenzt. Bei der Panel-Konvertierung werden Dateien auf den authentifizierten TgWitness-Server hochgeladen, im Arbeitsspeicher verarbeitet und die normalisierten Anmeldedaten an diesen Browser zurückgegeben, ohne die hochgeladenen Originale zu speichern. Verwenden Sie HTTPS für einen Remote-Server.

**Die konvertierte Datei ist ein unverschlüsseltes Passwort für den Kontozugang.** Bewahren Sie ihn an einem geschützten Ort auf und übertragen Sie ihn niemals in ein Repository oder senden Sie ihn an einen externen Konvertierungsdienst. TgWitness speichert die autorisierte Sitzung in seinem verschlüsselten Tresor. Das Kopieren einer Sitzung führt nicht zur Erstellung einer separaten Autorisierung: Führen Sie keine parallelen Clients mit geklonten Authentifizierungsschlüsseln aus und gehen Sie nicht davon aus, dass Aktualisierungen unabhängig voneinander bereitgestellt werden.

Die Konvertierung überträgt die Autorisierung, nicht jedoch die Originalnachrichten, den Entity-Cache oder einen dauerhaften Aktualisierungszeiger. Sie gewährleistet keine Wiederherstellung von Aktualisierungen über Prozessneustarts hinweg.

## MTProto, Telethon und Proxys

MTProto ist das Protokoll von Telegram. Telethon ist die Python-Client-Bibliothek, die TgWitness verwendet. MTProxy ist ein Telegram-Transport-Proxy; SOCKS5 und HTTP CONNECT stellen allgemeine Tunnel bereit. Keines dieser Verfahren ersetzt die Kontoauthentifizierung.

Speichern Sie die Route für jeden Arbeitsbereich unter **„Konto“ → „Einstellungen“ → „Verbindungseinstellungen“ → „Verbindungsroute ändern“**, bevor Sie sich anmelden. Für neue Arbeitsbereiche ist standardmäßig **„Automatischer MTProxy“ · öffentliche Listen** mit IP-Versteck-Funktion eingestellt. Bestehende Arbeitsbereiche, die explizit „Direkt“ verwendet haben, behalten einen Modus bei, der dies zulässt.

## IP-Modi

Die Route bestimmt die Verbindung. Der IP-Modus legt fest, wann die Adresse des Servers offengelegt werden darf. Diese Einstellungen führen weder zur Installation eines VPNs noch zur Umleitung des gesamten Datenverkehrs des Computers.

| Modus | Telegram | Externe Anfragen |
| --- | --- | --- |
| Hide IP (`hide`) | Verwenden Sie einen Proxy; warten Sie, falls keiner funktioniert. Es gibt keine direkte Ausweichmöglichkeit. | SOCKS5/HTTP ist erforderlich; Anfragen ohne entsprechenden Proxy werden abgelehnt. |
| Fallback zulassen (`fallback`) | Der automatische MTProxy kann nach Ablauf der konfigurierten Verzögerung „Direct“ verwenden und anschließend wieder zu einem funktionierenden Proxy zurückkehren. | Bevorzugen Sie einen konfigurierten externen Proxy oder die SOCKS5/HTTP-Route des Kontos; andernfalls ist „Direct“ zulässig. |
| Tunnel / VPN (`tunnel`) | Direkte Zugriffe und ein sofortiger automatischer Fallback auf den Pool sind zulässig. | Eine direkte Verbindung ist zulässig, wenn kein entsprechender Proxy konfiguriert ist. |

Der Tunnel-/VPN-Modus setzt voraus, dass Sie dieses Netzwerk separat verwalten. Ohne einen funktionierenden Tunnel können die Empfänger die eigene Adresse des Servers einsehen. Wählen Sie den Modus entsprechend Ihrer tatsächlichen Netzwerkkonfiguration aus, nicht anhand der Bezeichnung der Option.

### Wählen Sie einen Pfad

| Route | Einstellungen | Grenze |
| --- | --- | --- |
| Automatischer MTProxy | Integrierte Listen oder ein Operator-Katalog | Unterhält eine funktionierende Telegram-Verbindung; der direkte Fallback hängt vom IP-Modus ab |
| Direkt | Tunnel-/VPN-Modus | Telethon nutzt die Netzwerkroute des Hosts |
| SOCKS5 | Host, Port, optionaler Benutzername/Passwort | python-socks, Remote-Destination-DNS aktiviert |
| HTTP CONNECT | Host, Port, optionaler Benutzername/Passwort | Einfaches HTTP-CONNECT; TLS zum Proxy selbst ist nicht implementiert |
| MTProxy | Host, Port, Geheimnis | Experimenteller Telethon-Transport; 32 Hexadezimalziffern oder „`dd`“ + 32 Hexadezimalziffern |

Gefälschte TLS-`ee`-Geheimnisse werden abgelehnt. Die Normalisierung von Telethon 1.45 kann ein Präfix und eine Domain entfernen, implementiert jedoch kein Fake TLS. Fügen Sie `tg://proxy?server=…&port=…&secret=…` oder `https://t.me/proxy?server=…&port=…&secret=…` ein und wählen Sie **„Felder aus Link ausfüllen**“. Dadurch werden die Felder validiert und ausgefüllt, ohne dass eine Verbindung hergestellt oder gespeichert wird; überprüfen und speichern Sie die Route separat. Manuelle Felder bleiben verfügbar. Siehe [Telegram-Proxy-Links](https://core.telegram.org/api/links#proxy-links).

### Öffentliche Proxys, die von Ihrer Installation bereitgestellt werden

Die integrierte Liste vereint vier Quellen: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) und [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). Der mitgelieferte Snapshot enthält Endpunktdaten, Quellenangaben und Download-Daten. Die Auflistung eines Anbieters ist kein Beweis dafür, dass der Proxy funktioniert oder jedes Telegram-Update bereitstellt.

**MTProxy** überprüft **automatisch** die Telegram-Transportverbindung, hält einen funktionierenden Proxy bereit und wechselt zu einem anderen, wenn dieser ausfällt. Arbeitsbereiche bevorzugen unterschiedliche Proxys, sofern genügend funktionierende Einträge verfügbar sind; eine eindeutige Ausgangsadresse kann nicht garantiert werden. Ausgefallene Proxys werden vor einem erneuten Versuch pausiert. Wenn keiner funktioniert, bestimmt der IP-Modus, ob die Erfassung warten muss oder eine direkte Verbindung nutzen darf. Ein Wechsel der Proxys hat keine Auswirkungen auf das Konto und löscht dessen Protokoll nicht. Routenauswahlen und -änderungen werden im signierten Protokoll aufgezeichnet.

Solange automatische Routen aktiv sind, werden die Listen stündlich aktualisiert und Transportprüfungen standardmäßig alle zehn Minuten durchgeführt. Diese Intervalle sind konfigurierbar. **Das Aktualisieren öffentlicher Listen** löst eine Aktualisierung aus; das bloße Anzeigen der Liste ändert nichts an einer gespeicherten manuellen Route.

Jede Feed-Antwort ist auf 1 MiB begrenzt, mit einem Zeitlimit von acht Sekunden für die Anfrage und einer Gesamt-Download-Frist von 20 Sekunden; Weiterleitungen werden abgelehnt. Pro Quelle werden bis zu 64 kompatible Einträge beibehalten und dedupliziert. Der Parser akzeptiert unterstützte hexadezimale und Base64URL-Schlüssel sowie den JSON-Feed. Gefälschte TLS-`ee`-Zertifikate, ungültige Links, private/reservierte IP-Literale und lokale Hostnamen werden übersprungen. Hostnamen werden vor der Verwendung aufgelöst und überprüft, und die ausgewählte IP-Adresse wird für diese Verbindung festgehalten. Bei der automatischen Neuerfassung wird ein Hostname erneut aufgelöst; wenden Sie einen manuellen Eintrag erneut an, um ihn erneut aufzulösen.

Fehlgeschlagene, leere oder inkompatible Feed-Antworten behalten den vorherigen Quell-Snapshot bei. Aktualisierungen erfolgen atomar, serialisiert und sind auf einen Versuch pro Minute und Arbeitsbereich beschränkt. Eine erfolgreiche Transportprüfung stellt die Konnektivität her, nicht jedoch Anonymität oder die Vollständigkeit der Erfassung.

**Telegram-Datenverkehr und HTTPS-Anfragen nutzen unterschiedliche Routen.** Listen-Downloads verwenden eine separate HTTPS-Verbindung sowie die bereitgestellte Route für externe Anfragen. „`TGWITNESS_PROXY_FEED_PROXY`“ überschreibt diese Route explizit durch einen HTTP/SOCKS5-Proxy; beide „Compose“-Varianten des Collectors leiten diese weiter. Der Hintergrundpool folgt dem Hauptarbeitsbereich. Es werden keine Telegram-Sitzungen, API-Zugangsdaten, Panel-Token oder Bot-Token an Feed-Anbieter gesendet. Anbieternamen, Erfassungsdaten und die Download-Route werden unter **„Woher die Liste stammt“** angezeigt.

Ein MTProxy leitet ausschließlich Telegram-Datenverkehr weiter. HTTP-Vorgänge im Arbeitsbereich wie Zeitstempel, Benachrichtigungen, externe Kopien und Quellenprüfungen nutzen bei entsprechender Konfiguration einen separaten SOCKS5/HTTP-Proxy und anschließend die SOCKS5/HTTP-Route des Kontos. Fehlt eine der beiden, lehnt Hide IP die Anfrage ab; die anderen Modi erlauben „Direct“. Externe Anfragen können deaktiviert werden. Ein explizit konfigurierter Proxy für den Feed-Download bleibt eine separate, vom Betreiber vorgenommene Übersteuerung. Der unabhängige Witness-Dienst behält seine eigene Route bei.

****Automatische Pool-Parameter**** Konfigurieren Sie unter **Parameter → Automatischer MTProxy** die Fehlerschwelle, die Wartezeit, die geplante Rotation, die Proxy-Freigabe und die zulässige Fallback-Verzögerung. | Steuerung | Standard | | --- | --- | | Trennt die Verbindung vor dem Austausch | 3 innerhalb von 10 Minuten | | Proben für Proxys pro Verbindungsversuch | 3 | | Erste / maximale Wartezeit nach einem Ausfall | 10 Minuten / 6 Stunden | | Geplante Rotation | Deaktiviert; Wechsel bei Ausfall | | Konten pro Proxy | 0: separate Einträge bevorzugen, bei Bedarf gemeinsam nutzen. Setzen Sie den Wert auf 1, um auf einen exklusiven Eintrag zu warten. | | Verzögerung vor zulässigem „Direct“-Fallback | 10 Minuten; „Hide IP“ lehnt „Direct“ weiterhin ab | | Feed-Aktualisierung / Transportprüfungen | 60 / 10 Minuten; die Werte des Hauptarbeitsbereichs gelten für den gemeinsamen Pool | Unterschiedliche Proxys garantieren keine unterschiedlichen Ausgangsadressen. Diese Einstellungen setzen die Telegram-Beschränkungen nicht außer Kraft und gewährleisten keine Anonymität.

Um die öffentliche Liste durch Ihren eigenen Betreiberkatalog zu ersetzen, konfigurieren Sie die folgende Überschreibung. Dadurch werden externe Abonnements vollständig deaktiviert, auch wenn das Array „`proxies`“ leer ist.

Kopieren Sie [den leeren Katalog](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) nach „`proxy-config/proxies.json` “ und fügen Sie Ihre bereitgestellten öffentlichen Endpunkte hinzu:

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

Die Beispielwerte müssen ersetzt werden. Es werden bis zu 32 unterschiedliche Einträge akzeptiert. Die authentifizierte Auflistung gibt Labels/Hosts/Ports ohne gemeinsame Geheimnisse zurück; bei Auswahl eines Eintrags werden dessen Anmeldedaten im Workspace-Tresor gespeichert. Die Verfügbarkeit bleibt bis zu einem expliziten Transporttest ungeprüft. Bei einem fehlerhaften Katalog ist eine manuelle Konfiguration möglich.

Native Ausführung: Legen Sie „`TGWITNESS_PROXY_CATALOG`“ als lokalen JSON-Pfad fest. Docker:

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

Das Overlay wird schreibgeschützt unter dem Namen „`proxy-config`“ eingebunden; die Dateien müssen für die Container-UID 10001 lesbar sein. Dieses Verzeichnis ist von Git, dem Docker-Build-Kontext und den Quellarchiven ausgeschlossen. Dieser Katalog konfiguriert die Erfassungskonten; [der Witness-Bot](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/) verwendet seine eigene HTTP/SOCKS5-Route, nicht MTProxy.

Der direkte Fallback unterliegt dem oben beschriebenen IP-Modus. Unterbrechen Sie die Überwachung, bevor Sie eine Route ändern. Durch das Speichern werden alte Clients getrennt und unvollendete Anmeldungen abgebrochen; ein neuer Client verwendet die gespeicherte Route. Die Verknüpfung zwischen Konto und Protokoll/Sitzung bleibt bestehen. Einstellungen ersetzen die vorherige Route: Geben Sie die Proxy-Anmeldedaten bei der Bearbeitung erneut ein.

Anmeldedaten werden mit `network.enc` verschlüsselt. Die API gibt weder den Benutzernamen, noch das Passwort oder den geheimen Schlüssel zurück. Signierte Datensätze enthalten den Routentyp und die Angabe, ob Anmeldedaten vorhanden sind, wobei der Endpunkt und geheime Schlüssel ausgeschlossen sind. Der Betreiber kann den Endpunkt im Bedienfeld einsehen. Geheime Felder werden nach dem Speichern, Sperren oder Wechseln von Arbeitsbereichen gelöscht.

**Die Telegram-Verbindungsprüfung**, **die** auch vor der Anmeldung verfügbar ist, öffnet und schließt eine temporäre, nicht autorisierte Telegram-Verbindung über die Route. Es wird keine Verbindung zu einer IP-Prüfungs- Website hergestellt. Ein erfolgreicher Test stellt lediglich die Transportverbindung her, nicht jedoch den Zugriff auf Gruppen, die vollständige Zustellung oder Anonymität.

Der Proxy gilt für die Verbindungen des Telegram-Clients, einschließlich der Medien-Downloads von Telegram-DCs. Browser, pip, SSH und manuell aufgerufene TSA-Tools verfügen über separate Routen. Der Proxy-Hostname kann lokal aufgelöst werden. „`rdns`“ wirkt sich auf Ziel-Hostnamen aus; Telegram stellt häufig numerische DC-IP-Adressen bereit.

SOCKS5 und einfaches HTTP CONNECT verschlüsseln an sich weder die Proxy-Anmeldedaten noch den Tunnel zwischen Client und Proxy. MTProto schützt den Telegram-Datenverkehr separat. Verwenden Sie einen geeigneten sicheren Kanal zum Proxy in einem nicht vertrauenswürdigen Netzwerk. Private Gruppen sind Cloud-Chats; MTProto wandelt diese nicht in Ende-zu-Ende-verschlüsselte „Secret Chats“ um.

## Verschlüsselung und Signaturen

| Ebene | Umsgesetzt | Verantwortung des Betreibers |
| --- | --- | --- |
| Telegram-Datenverkehr | Telethon MTProto | Vertrauen in die Plattform, Übertragungsweg und Verfügbarkeit |
| Web-Panel | Bearer-Token, Standard-Loopback, Anforderungslimits | HTTPS oder SSH-Tunnel für den Fernzugriff |
| Geheimnisse | Fernet für API-Zugangsdaten, Sitzungsdaten, Proxy-Zugangsdaten und den privaten Signaturschlüssel | Schützen Sie den Entschlüsselungsschlüssel und den laufenden Host |
| Tresorschlüssel | Lokaler Schlüssel oder externer Hauptschlüssel für eine Neuinstallation | Getrennter, geschützter Speicher und Schlüssel-Backup |
| Nachrichten und Anhänge | Speicherung der Anwendung im Klartext | Verschlüsselte Festplatte/Datenträger |
| ZIP/JSONL/CSV/HTML | Integritätsprüfungen, keine Verschlüsselung der Inhalte | Schützen Sie exportierte Kopien und Übertragungen |
| Herkunft und Zeitpunkt | Signiertes Protokoll, Prozessbeleg, RFC 3161-Tools | Vertrauenswürdiger Schlüssel, unabhängige Kontrollpunkte/TSA und Aufbewahrungsverfahren |

**Der Speicherschutz** im Konto zeigt diese Zustände an. Das Panel-Token ist ein Zugriffsgeheimnis, kein Verschlüsselungspasswort. Es gewährt Administratorzugriff; [ausgestellte Token](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/) können auf Konten und Chats beschränkt werden. Arbeitsbereiche teilen sich den Host-Prozess und sind keine isolierten Mandanten.

Eine explizit gestartete, isolierte synthetische Demo kann automatisch über eine direkte Loopback-Verbindung geöffnet werden. Dies nutzt eine separate, auf die Prozesslaufzeit begrenzte Funktion; dabei wird weder das konfigurierte Panel-Token offengelegt noch wird Zugriff auf echte Arbeitsbereiche gewährt. Remote-, Proxy- oder Cross-Origin-Anfragen können diese Funktion zum automatischen Aufruf nicht abrufen oder nutzen. Diese Erleichterung hebt die Authentifizierungsgrenze für echte Kontodaten nicht auf.

BitLocker, LUKS, FileVault oder ein verwaltetes verschlüsseltes Volume können Speichermedien im Rahmen ihrer jeweiligen Bedrohungsmodelle schützen. Ein Administrator eines entsperrten, laufenden Rechners kann die Daten weiterhin lesen. Berücksichtigen Sie SQLite-WAL/SHM, Medien, temporäre Exporte, Auslagerungsspeicher, Backups sowie Browser-Downloads bei der Speicherplanung. Ein Docker-Volume ist nicht allein deshalb verschlüsselt, weil es sich um ein Volume handelt. TgWitness implementiert weder SQLCipher noch Objektverschlüsselung.

## Externer Hauptschlüssel

Bei einer Neuinstallation legen Sie den Hauptschlüssel außerhalb des Datenverzeichnisses ab. Dadurch wird ein bestehender Tresor mit lokalem Schlüssel nicht automatisch migriert. Richten Sie ein Schlüsselverzeichnis ein, auf das nur die Dienstidentität Zugriff hat, und führen Sie anschließend folgenden Befehl aus:

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell unter Verwendung der installierten Projektumgebung:

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

Binden Sie die Datei in Docker schreibgeschützt außerhalb von „`/data`“ ein, beispielsweise unter „ `/run/secrets/tgwitness-master.key`“, und setzen Sie die Umgebungsvariable auf diesen Pfad. Die UID des Dienstes muss Lesezugriff darauf haben. Übergeben Sie den Pfad – nicht die Schlüsselbytes – über Umgebungs- bzw. Konfigurationsdateien.

Jeder Arbeitsbereich erhält ein zufälliges öffentliches Salt sowie einen eigenen Fernet-Schlüssel, der mittels HKDF-SHA256 abgeleitet wird. „`vault.external.json`“ speichert die Metadaten der Ableitung, nicht den Hauptschlüssel. Ein fehlender oder falscher Schlüssel führt zum Fehlschlagen des Startvorgangs, ohne dass dieser stillschweigend ersetzt wird. Bewahren Sie sowohl die Salt-Metadaten als auch den Hauptschlüssel zur Wiederherstellung auf.

Alle Arbeitsbereiche leiten sich vom selben Hauptschlüssel ab; dessen Kompromittierung wirkt sich auf die gesamte Installation aus. Der laufende Prozess kann Geheimnisse entschlüsseln. Es handelt sich hierbei nicht um ein HSM oder ein Passwort-KDF. Beliebige, von Menschen festgelegte Passwörter werden nicht anstelle eines Zufallsschlüssels akzeptiert.

Behalten Sie den bestehenden Schlüssel für bestehende Installationen bei, bis eine gezielte Migration durchgeführt und verifiziert wurde. Das Löschen von „`vault.key`“ oder das Ersetzen eines Hauptschlüssels kann den Zugriff auf Sitzungen/Signaturschlüssel zunichte machen. Bewahren Sie verschlüsselte Sicherungskopien und Schlüssel getrennt auf und testen Sie die Wiederherstellung in einer isolierten Instanz.

## Quellen und Umfang der Überprüfung

Überprüft am 26. Oktober 2026:

- https://core.telegram.org/api/auth
- https://core.telegram.org/api/obtaining_api_id
- https://docs.telethon.dev/en/stable/basic/signing-in.html
- https://docs.telethon.dev/en/stable/concepts/sessions.html
- https://core.telegram.org/mtproto/mtproto-transports
- https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/SourceFiles/storage/storage_account.cpp
- Telethon 1.45.0: SQLiteSession, StringSession, „`Connection._proxy_connect`“, „ `TcpMTProxy.normalize_secret`“ und Download-Methoden.

Lokale Tests umfassen Loopback-SOCKS5-/HTTP-CONNECT-Fixtures, synthetische SQLite-Sitzungen, Routenisolierung, Ausschluss geheimer Daten und Ablehnung bei fehlendem Schlüssel. Sie stellen keine tatsächliche Interoperabilität zwischen Telegram und Proxy oder das Live-Verhalten von MTProxy her. Siehe [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/) und [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
