# Sicherheit und Datenumgang

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/security/

Bedrohungsmodell, Zugriffsmodell, gespeicherte vertrauliche Daten, Netzwerkexposition, Import von Sitzungen und Anleitung zur Meldung einer Sicherheitslücke.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Bereitstellung und Wiederherstellung](https://phishdestroy.github.io/TgWitness/de/docs/reference/deployment/)

![Bereitstellung und Wiederherstellung](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Diese Seite beschreibt den Zugriff, die Speicherung und den Netzwerkschutz in einem lokalen oder Server-Arbeitsbereich. Informationen zur Datenerfassung auf einem GitHub-Runner oder in einer vertraulichen Intel-TDX-VM finden Sie unter den [-Verifizierungsmodi](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope), die zusätzliche Prüfungen der Erfassungsumgebung beinhalten. Kontoverbindungen, Benachrichtigungen, Zeitstempel, externe Kopien und Zeugen verfügen über eigene Routing-Einstellungen.

| Bereich | Kurz gesagt |
| --- | --- |
| Zugriff | Administratorschlüssel sowie bereichsbezogener Zugriff auf Konten/Chats, sieben Berechtigungsstufen und widerrufbare Sitzungen; standardmäßig „localhost“ |
| Gespeicherte Geheimnisse | Sitzung, API-Paar, Signaturschlüssel und Proxy-Einstellungen werden mit Fernet verschlüsselt |
| Nachrichten und Medien | Unverschlüsselt gespeichert: Verwenden Sie Festplattenverschlüsselung und strenge Zugriffsrechte |
| Integrität | SHA-256-Hash-Kette und eine Ed25519-Signatur für jeden Datensatz |
| Lokale Vertrauensgrenze | Der Host-Administrator verwaltet den Arbeitsbereich und dessen Signaturschlüssel; unabhängige Kontrollpunkte bewahren eine frühere Journalgrenze. |

Informationen zu Sicherheitslücken finden Sie in der [Sicherheitsrichtlinie](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

**Auf dieser Seite**

- [Zugriffsmodell](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#access-model)
- [Inhalt des Panels und Exporte](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#panel-content-and-exports)
- [Gespeicherte Geheimnisse](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#secrets-at-rest)
- [Proxys und Netzwerkwege](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#proxies-and-network-routes)
- [Anmeldung und Import von Sitzungen](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#sign-in-and-session-imports)
- [Protokolle und Transport](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#logs-and-transport)
- [Integritätsgrenzen](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#integrity-limits)
- [Wenn Sie ein Problem vermuten](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#if-you-suspect-a-problem)

## Zugriffsmodell

Das Haupt-Panel-Token gewährt volle Kontrolle. Andere Personen können einen eigenen, [begrenzten Zugriff](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/) erhalten: ausgewählte Arbeitsbereiche und Chats, Berechtigungen, Ablaufdaten, IP-Einschränkungen, Anmeldebeschränkungen und widerrufbare Sitzungen. Ein auf Chats beschränkter Zugriff kann keine arbeitsbereichsweiten Vorgänge ausführen, selbst wenn die entsprechende Berechtigung aktiviert ist. Arbeitsbereiche nutzen denselben Prozess und isolieren Daten nicht vom Host-Administrator.

Das Panel lauscht standardmäßig auf „localhost“. Bei der Anmeldung über den Browser wird ein Zugriffstoken gegen eine Sitzungsberechtigung ausgetauscht; der Browser sendet diese als „Bearer-Token“. Es wird in „sessionStorage“ statt in einem Authentifizierungs-Cookie gespeichert. Durch Sperren oder Abmelden wird die Browsersitzung gelöscht. Das Schließen des Browsers oder das Beenden einer Sitzung unterbricht die Erfassung nicht.

Ausgegebene Tokens und Sitzungszugangsdaten werden als Hashes im verschlüsselten Tresor gespeichert. Eine Sperrung beendet die zugehörigen Sitzungen; Änderungen der Berechtigungen wirken sich auf nachfolgende Anfragen aus. Heruntergeladene Dateien können nicht zurückgerufen werden. Der Administrator kann auch seine eigenen Browsersitzungen einschränken, jedoch behalten Skripte, die das Token des Hauptpanels direkt verwenden, den vollen Zugriff und umgehen diese Browsersitzungsbeschränkungen.

Fehlgeschlagene Authentifizierungsversuche werden anhand der Client-Adresse rate-begrenzt. Bei IP-Einschränkungen wird die von der Anwendung erkannte Adresse herangezogen; überprüfen Sie das Verhalten des Reverse-Proxys, bevor Sie sich darauf verlassen. Die Anmeldedaten von Witness bleiben separate, schreibgeschützte Checkpoint-/Zustandsdaten.

### Zugang zur Demo

`/api/demo-access` ist ein bewusst nicht authentifizierter Bootstrap für eine explizit gestartete, isolierte synthetische Demo. Er vergibt eine separate, auf die Prozesslaufzeit begrenzte Berechtigung, niemals das echte Panel-Token oder eine TGWITNESS_TOKEN-Überschreibung. Die Ausstellung und Nutzung erfordern einen Loopback-Peer und einen Host, keine weitergeleiteten Header und keine Cross-Origin-Anfrage. Zusätzliche Arbeitsbereiche oder eine autorisierte Sitzung deaktivieren diesen Pfad. Live-Arbeitsbereiche stellen die Berechtigung niemals aus. Die Demo kann keine Konten verbinden oder Erfassungseinstellungen ändern.

## Inhalt der Übersichtsansicht und Exporte

Das Panel verwendet keine externen Schriftarten, Analysetools, CDN-Ressourcen oder eingebettete Remote-Medien. Aus Telegram stammende Texte werden als Text und nicht als HTML eingefügt. Heruntergeladene Anhänge werden als binäre Anhänge bereitgestellt. JSONL-Exporte bewahren die ursprünglichen Zeichenfolgen bei; HTML führt ein Escape-Zeichen für diese ein; CSV-Zellen, die zu Formeln werden könnten, werden mit einem Apostroph vorangestellt.

Die Exporte schließen Authentifizierungs- und Signaturschlüssel aus, enthalten jedoch bewusst gesammelte Quellmetadaten, Identifikatoren sowie möglicherweise persönliche oder sensible Inhalte. Telegram-Zugriffshashes und Dateiverweise können in den Rohdaten der Quellmetadaten vorkommen.

## Gespeicherte Geheimnisse

Die Anmeldedaten für die Telegram-API, die Sitzung und der Signaturschlüssel werden mit Fernet verschlüsselt. Für lokale Nachrichten und Medien erfolgt die Verschlüsselung durch die Festplatte oder das Volume des Hosts; im Arbeitsbereich werden gewöhnliche Dateien gespeichert. Exporte können in einem passwortgeschützten AES-256-ZIP-Archiv erfolgen, und externe Kopien verwenden AES-256-GCM.

Der Tresorschlüssel verweist standardmäßig auf das Verzeichnis für geschützte Daten. Verwenden Sie eine externe Hauptschlüsseldatei (siehe unten), um ihn separat zu speichern. Unter Unix verwenden neue Dateien für private Schlüssel den Modus 0600 und neue Datenverzeichnisse den Modus 0700; unter Windows legen Sie die Verzeichnis-ACL für das Dienstkonto und autorisierte Administratoren fest. Bestehende Verzeichnisberechtigungen bleiben erhalten.

### Externer Hauptschlüssel

Für ein neues Datenverzeichnis kann TGWITNESS_VAULT_KEY_FILE einen externen zufälligen Hauptschlüssel bereitstellen. HKDF-SHA256 und ein separates zufälliges Salt leiten für jeden Arbeitsbereich einen anderen Fernet-Schlüssel ab. Die Datei vault.external.json muss zur Wiederherstellung beibehalten werden. Fehlende oder falsche Hauptschlüssel führen zu einem Fehler closed. Vorhandene lokale Tresore werden nicht stillschweigend migriert. Das Bedienfeld zeigt den ausgewählten Schlüsselspeichermodus an. Die Festplattenverschlüsselung schützt die lokalen Nachrichten- und Mediendateien in beiden Modi; siehe „ [-Verbindung“ und „Datenschutz](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/)“ für Details zur Einrichtung.

## Proxys und Netzwerkwege

Die Proxy-Konfiguration wird im Tresor verschlüsselt gespeichert. Passwörter und MTProxy-Geheimnisse werden weder von der API zurückgegeben noch in die Beweisdokumente geschrieben. Jeder Arbeitsbereich wählt seine eigene Telegram-Route und einen [IP-Modus](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/#ip-modes) aus.

**Die Option „Adresse verbergen“** unterbindet den direkten Telegram-Fallback und erfordert einen Proxy für externe HTTP-Anfragen. Der explizit ausgewählte Fallback-Modus erlaubt den direkten Zugriff auf Telegram nach einer Verzögerung; der Tunnel-/VPN-Modus erlaubt direkte Verbindungen. Die Auswahl des Tunnelmodus führt weder zur Installation noch zur Überprüfung eines VPNs. Diese Einstellungen haben keinen Einfluss auf den gesamten Datenverkehr des Computers, Browser, Paketmanager oder die DNS-Auflösung durch einen lokal gehosteten Proxy.

MTProxy leitet ausschließlich Telegram-Datenverkehr weiter. Externe Anfragen können einen separaten SOCKS5/HTTP-Proxy, die SOCKS5/HTTP-Route des Arbeitsbereichs oder eine zugelassene direkte Route nutzen; sie können auch deaktiviert werden. Der unabhängige Witness verfügt über eigene Transporteinstellungen. Die gewöhnliche SOCKS5/HTTP-CONNECT-Authentifizierung wird durch diese Proxy-Protokolle selbst nicht verschlüsselt. Gefälschte TLS-MTProxy-Geheimnisse werden weiterhin nicht unterstützt.

## Anmeldung und Import von Sitzungsdaten

Konvertierte .tgwitness-session-Dateien enthalten ein Autorisierungsgeheimnis im Klartext, bis sie geladen und im Tresor gespeichert werden. Die Offline-Befehlszeilenschnittstelle akzeptiert geprüfte Telethon-Schemas. Der Panel-Import akzeptiert zusätzlich Pyrogram SQLite, moderne TData-ZIP-Dateien für Einzelkonten sowie dokumentierte JSON-Eingaben. Er ist authentifiziert, auf vier Dateien bzw. 8 MiB begrenzt und verarbeitet Uploads im Arbeitsspeicher, ohne das Archiv zu entpacken oder Originaldateien zu speichern. Normalisierte Anmeldedaten werden ausschließlich an den anfragenden, authentifizierten Browser zurückgegeben; sie werden nach erfolgreicher Telegram-Autorisierung im verschlüsselten Tresor gespeichert. Schützen Sie Original- und konvertierte Dateien und verhindern Sie, dass mehrere Clients gleichzeitig eine Autorisierung klonen.

Die Datenverarbeitung überprüft Container-Prüfsummen, lokale Entschlüsselungs-Hashes und Strukturlängen. Ein bereitgestellter lokaler Desktop-Zugangscode wird vorübergehend verwendet und nicht gespeichert. Dieser begrenzte Parser stellt nicht sicher, dass jede Desktop-Version kompatibel ist. QR-Bilder werden lokal generiert, enthalten kurzlebige Telegram-Anmeldetoken und werden niemals an einen externen Rendering-Dienst gesendet. Sperren, Wechsel des Arbeitsbereichs, neue Anmeldung sowie Routenänderungen brechen ausstehende QR-Versuche ab. Das Neuladen oder Schließen eines Tabs kann dazu führen, dass ein Versuch bis zum Ablauf ausstehend bleibt. Eine erfolgreiche QR-Anmeldung erzwingt weiterhin die Kontoverbindung. Gewöhnliche API-Payloads bleiben auf 16 KiB begrenzt; die authentifizierte Import-Route akzeptiert bis zu 12 MiB kodiertes JSON, wobei die geringere Obergrenze für dekodierte Dateien separat durchgesetzt wird.

Anmeldedaten und Passwörter für die zweistufige Verifizierung bei Telegram werden nicht dauerhaft gespeichert. Der Status der Telefonnummer bzw. des Code-Hashes wird während der Autorisierung im Arbeitsspeicher gehalten. Der Zugriff auf das Konto erfolgt über Telegram-Sitzungen; laden Sie niemals ein Datenverzeichnis, eine Sitzung, ein Token, einen Tresorschlüssel oder einen privaten Signaturschlüssel auf GitHub hoch.

## Protokolle und Übertragung

Die standardmäßige API-Validierungsantwort wird ersetzt, sodass keine Anmeldeinformationen wiedergegeben werden. Die Protokollierung des Anwendungszugriffs ist deaktiviert. Konfigurieren Sie keinen Reverse-Proxy zur Protokollierung von Autorisierungs-Headern oder Request-Bodies. HTTP überträgt Tokens und Anmelde- Geheimnisse im Klartext: Verwenden Sie HTTPS oder einen SSH-Tunnel, sobald eine Verbindung über „localhost“ hinausgeht.

## Integritätsgrenzen

Bei der lokalen Verifizierung werden Datensatzsignaturen, die Hash-Kette, Anhänge und das Exportmanifest überprüft. Der Administrator verfügt über den lokalen Signaturschlüssel und kann ein weiteres signiertes Journal erstellen; ein unabhängig aufbewahrter Checkpoint erkennt das Ersetzen des von ihm abgedeckten Präfixes. Bewahren Sie den Schlüssel-Fingerabdruck und die Checkpoints beim Empfänger oder bei einem unabhängigen Zeugen auf.

Für eine unabhängig überprüfte Erfassung wählen Sie [GitHub Actions Capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) oder [Intel TDX Deployment](https://phishdestroy.github.io/TgWitness/de/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Deren Verifizierer überprüfen zusätzlich zur Archivintegrität die Herkunft des Workflows oder Hardware-Messungen. Optionale Zeitstempel und verschlüsselte externe Kopien bieten Zeitanker und wiederherstellbare Kopien; das [Evidence-Format](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope) beschreibt die Prüfungen für jeden Modus.

## Sollten Sie ein Problem vermuten

Behalten Sie das ursprüngliche Datenverzeichnis bei und verwenden Sie eine separate Kopie für die Analyse. Melden Sie die betroffene Version, den Vorgang und die reproduzierbaren Schritte gemäß der [Sicherheitsrichtlinie](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md) und behandeln Sie dabei Kontodaten und Anmeldedaten vertraulich.
