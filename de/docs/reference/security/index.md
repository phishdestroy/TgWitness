# Sicherheit und Datenumgang

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/security/

Bedrohungsmodell, Zugriffsmodell, gespeicherte vertrauliche Daten, Netzwerkexposition, Import von Sitzungen und Anleitung zur Meldung einer Sicherheitslücke.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/de/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

This page describes access, storage and network protection in a local or server workspace. For collection on a GitHub runner or in an Intel TDX confidential VM, see the [verification modes](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope), which add checks of the collection environment. Account connections, notifications, timestamps, off-site copies and witnesses have their own routing settings.

| Bereich | Kurz gesagt |
| --- | --- |
| Zugriff | Administratorschlüssel sowie bereichsbezogener Zugriff auf Konten/Chats, sieben Berechtigungsstufen und widerrufbare Sitzungen; standardmäßig „localhost“ |
| Gespeicherte Geheimnisse | Sitzung, API-Paar, Signaturschlüssel und Proxy-Einstellungen werden mit Fernet verschlüsselt |
| Nachrichten und Medien | Unverschlüsselt gespeichert: Verwenden Sie Festplattenverschlüsselung und strenge Zugriffsrechte |
| Integrität | SHA-256-Hash-Kette und eine Ed25519-Signatur für jeden Datensatz |
| Lokale Vertrauensgrenze | The host administrator controls the workspace and its signing key; independent checkpoints retain an earlier journal boundary |

Informationen zu Sicherheitslücken finden Sie in der [Sicherheitsrichtlinie](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

**On this page**

- [Access model](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#access-model)
- [Panel content and exports](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#panel-content-and-exports)
- [Secrets at rest](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#secrets-at-rest)
- [Proxies and network routes](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#proxies-and-network-routes)
- [Sign-in and session imports](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#sign-in-and-session-imports)
- [Logs and transport](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#logs-and-transport)
- [Integrity limits](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#integrity-limits)
- [If you suspect a problem](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/#if-you-suspect-a-problem)

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

Telegram API credentials, the session and signing key are encrypted with Fernet. For local messages and media, encryption is provided by the host's disk or volume; the workspace stores ordinary files. Exports can use a password-protected AES-256 ZIP, and off-site copies use AES-256-GCM.

The vault key defaults to the protected data directory. Use an external master-key file below to store it separately. On Unix, new private-key files use mode 0600 and new data directories use 0700; on Windows, set the directory ACL for the service account and authorized administrators. Existing directory permissions are retained.

### Externer Hauptschlüssel

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode. Disk encryption protects the local message and media files in either mode; see [connection and data protection](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/) for setup details.

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

Local verification checks record signatures, the hash chain, attachments and the export manifest. The administrator holds the local signing key and can create another signed journal; an independently retained checkpoint detects replacement of the prefix it covers. Keep the key fingerprint and checkpoints with the recipient or an independent witness.

For independently checked collection, choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/de/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Their verifiers check workflow provenance or hardware measurements in addition to archive integrity. Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies; the [evidence format](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#verification-scope) describes the checks for each mode.

## Sollten Sie ein Problem vermuten

Preserve the original data directory and use a separate copy for analysis. Report the affected version, operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), keeping account data and credentials private.
