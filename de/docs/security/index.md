# Sorgen Sie für Sicherheit

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/security/

Machen Sie sich mit den Routen für Telegram, öffentlichen Proxy-Listen und optionalen externen Diensten vertraut. Erfahren Sie, welche Funktionen die einzelnen Einstellungen freischalten, welchen Schutz sie bieten und welche Entscheidungen Ihnen überlassen bleiben.

**127.0.0.1**Standardmäßige Panel-Adresse

**256-Bit**Zufälliges Panel-Token

**0**CDNs, Analysetools oder Remote-Schriftarten

**Ed25519**Signatur auf jedem Datensatz

## Hier finden Sie alles

Der Collector, sein Bedienfeld und alle gespeicherten Datensätze verbleiben auf dem Computer oder Server, auf dem Sie das Tool ausführen. Telegram ist standardmäßig das einzige Ziel; jedes weitere Ziel wird über einen separaten Schalter ausgewählt.

06 / WAS DIE MASCHINE VERLÄSSTIhre Installation

IHR COMPUTER ODER SERVER

**Panel**127.0.0.1:8787 · Bearer-Token

**Collector**Ein Telegram-Client pro Arbeitsbereich

DATENVERZEICHNIS

**Protokoll**SQLite · Hash-verknüpft · signiert

**Medien**Dateien, benannt nach SHA-256

**Vault**Fernet · Sitzung, API-Paar, Signaturschlüssel, Proxy

- **Telegram**Immer · über Ihren Weg

  Die MTProto-Verbindung des Kontos: direkt, SOCKS5, HTTP oder MTProxy. Der „IP verbergen“-Modus wartet auf einen funktionierenden Proxy. Für den direkten Fallback ist ein Modus erforderlich, der dies ausdrücklich zulässt.
- **Text für externe Seiten**Optional · standardmäßig deaktiviert

  Das Protokoll, die Dateien und die Kontrollpunkte werden vor dem Hochladen in einen S3-kompatiblen Speicher mit AES-GCM verschlüsselt. Der Schlüssel verbleibt bei Ihnen; Anhänge werden anhand von schlüsselgebundenen Hashes benannt, nicht anhand ihres Inhalts-Hashes.
- **Benachrichtigungen**Optional · standardmäßig deaktiviert

  Probleme und Änderungszähler mit Chat-Titeln. Nachrichtenauszüge werden nur gesendet, wenn Sie diese Funktion aktivieren.
- **Zeitstempel-Autorität**Optional · standardmäßig deaktiviert

  Lediglich der SHA-256-Hash eines signierten Checkpoints und ein zufälliger Nonce. Keine Nachrichten, keine Chat-Namen.
- **Witness**Optional · standardmäßig deaktiviert

  Ruft signierte Checkpoints und Erfassungszähler mit einem schreibgeschützten Token ab. Es kann weder Unterhaltungen lesen noch Einstellungen ändern.

Standard: Nur die Telegram-Verbindung verlässt diesen Rechner.

Optionale Speicherorte werden pro Arbeitsbereich konfiguriert. Nachrichtentexte und Medien werden unverschlüsselt im Datenverzeichnis gespeichert: Schützen Sie dieses durch Festplattenverschlüsselung und Dateiberechtigungen.

## Was jedes Geheimnis enthüllt

| Geheim | Wo es aufbewahrt wird | Was es ermöglicht | Falls es bekannt wird |
| --- | --- | --- | --- |
| **Panel-Token** | `panel-token.txt` im Datenverzeichnis; der Browser speichert diese Datei ausschließlich für den jeweiligen Tab | Alle Funktionen in jedem Arbeitsbereich: Lesen und Exportieren, Umfang ändern, in Konten anmelden | Beenden Sie TgWitness, löschen Sie „`panel-token.txt`“ und starten Sie es erneut: Es wird ein neues Token erstellt. |
| **Telegram-Sitzung** | Vault, verschlüsselt (`credentials.enc`) | Der Telegram-Account selbst | Beenden Sie die Sitzung in Telegram unter *„Einstellungen“ → „Geräte“* |
| **Signaturschlüssel** | Vault, verschlüsselt (`signing.enc`) | Signierte Aufzeichnungen, die unter Ihrem Fingerabdruck verifiziert werden können | An anderer Stelle gespeicherte Kontrollpunkte, ein Zeuge und Zeitstempel zeigen, was zuvor vorhanden war |
| **Tresorschlüssel** | „`vault.key`“ neben den Daten oder ein externer Hauptschlüssel für ein neues Datenverzeichnis | Entschlüsselung des Tresors | Behandeln Sie die Sitzungs- und Signaturschlüssel ebenfalls als offengelegt |
| **Witness-Token** | Auf dem Witness-Host | Schreibgeschützt: signierte Kontrollpunkte und Integritätsprüfung | Löschen Sie diesen Eintrag auf der „Witness“-Seite; erstellen Sie einen neuen. |
| **Schlüsseltext für externe Seiten** | Vault; einmal herunterladen, um Daten wiederherzustellen | Entschlüsselung der externen Kopie | Wer auch immer die gespeicherten Objekte besitzt, kann diese entschlüsseln: Behandeln Sie diese Kopie als offengelegt. |

## Was die Schutzmaßnahmen abdecken

### Abgedeckt

- Ein geänderter, gelöschter oder neu angeordneter Eintrag in einem Export: Die Hash-Kette oder eine Signatur lässt sich nicht mehr verifizieren.
- Ein Protokoll, das nach einem Kontrollpunkt gekürzt oder neu erstellt wurde, wurde an anderer Stelle gespeichert: Der gespeicherte Kontrollpunkt stimmt nicht mehr überein.
- Erraten des Panel-Tokens: 256 zufällige Bits, die in konstanter Zeit verglichen werden; nach 15 Fehlversuchen pro Minute wird eine Adresse abgelehnt.
- Inhalte aus feindlichen Chats: Text wird als reiner Text eingefügt, niemals als HTML; Anhänge werden als Dateien heruntergeladen; das Panel lädt keine Inhalte von anderen Websites.
- Ein Verzeichnis mit kopierten Daten und einem externen Tresorschlüssel: Sitzungen und Signaturschlüssel bleiben ohne den Hauptschlüssel verschlüsselt.

### Ich überlasse es Ihnen

- Der Inhaber des Haupt-Tokens hat die volle Kontrolle. Gewähren Sie anderen Personen einen begrenzten Zugriff auf die Konten, Chats und Aktionen, die sie benötigen; halten Sie den Hauptschlüssel geheim.
- Ein Administrator des Servers kann alle Einträge einsehen und das Protokoll überschreiben sowie neu signieren. Bewahren Sie den Fingerabdruck und die Kontrollpunkte auf einem anderen System auf.
- Nachrichtentexte und Medien werden von TgWitness nicht verschlüsselt. Verwenden Sie Festplattenverschlüsselung und strenge Zugriffsberechtigungen.
- Bei einer einfachen HTTP-Verbindung außerhalb von „localhost“ wird das Token im Netzwerk sichtbar. Verwenden Sie HTTPS oder einen SSH-Tunnel.
- Die Signaturen belegen, dass die aufgezeichneten Inhalte nicht verändert wurden – nicht jedoch, dass jedes Telegram-Ereignis aufgezeichnet wurde.

[Teilen Sie den Zugriff auf einen Fall](https://phishdestroy.github.io/TgWitness/de/docs/access/) mit Berechtigungen, Ablaufdaten und Sitzungsbeschränkungen. Ein Witness-Token bleibt eine separate Zugangsberechtigung.

## Eine Installation absichern

0 von 8 fertiggestellt

1. **Verwenden Sie ein eigens dafür eingerichtetes Telegram-Konto** – niemals Ihr Hauptkonto. Das Panel-Token und die Sitzung ermöglichen die vollständige Kontrolle darüber.
2. **Lassen Sie das Panel auf 127.0.0.1 laufen.** Greifen Sie remote nur über HTTPS (die mitgelieferte Caddy-Konfiguration) oder einen SSH-Tunnel darauf zu.
3. **Verschlüsseln Sie die Festplatte,** auf der sich das Datenverzeichnis befindet: Nachrichtentexte und Medien werden so gespeichert, wie sie eingegangen sind.
4. **Beschränken Sie das Datenverzeichnis** auf das Dienstkonto. Neue Verzeichnisse erhalten unter Unix die Berechtigung 0700; unter Windows legen Sie die Berechtigungen für den Ordner fest.
5. **Bewahren Sie den Hauptschlüssel des Tresors an einem anderen Ort** auf den Servern **auf**: Legen Sie „`TGWITNESS_VAULT_KEY_FILE`“ fest, bevor Sie das Datenverzeichnis erstellen.
6. **Speichern Sie den Fingerabdruck des Signaturschlüssels und die Kontrollpunkte** auf einem anderen System und fügen Sie einen Zeugen auf einem anderen Host hinzu.
7. **Laden Sie niemals** `data/`-, Sitzungs-, `panel-token.txt`- oder Tresorschlüssel auf GitHub oder in einen Chat **hoch**.
8. `Authorization`-Header oder Request-Bodies **dürfen** an einem Reverse-Proxy **nicht protokolliert werden**.

**Kann ich das Panel-Token ändern, ohne Daten zu verlieren?**

Ja. Das Token öffnet lediglich das Bedienfeld. Beenden Sie TgWitness, löschen Sie „`panel-token.txt`“ aus dem Datenverzeichnis und starten Sie das Programm erneut; das Protokoll, die Sitzungen und die Schlüssel bleiben davon unberührt. Wenn „`TGWITNESS_TOKEN`“ festgelegt ist, wird anstelle der Datei der Umgebungswert verwendet.

**Warum werden Nachrichten im Ruhezustand nicht verschlüsselt?**

Der Erfasser muss diese lesen, um sie zu durchsuchen, Versionen zu vergleichen und zu exportieren. Eine Verschlüsselung mit einem Schlüssel auf demselben Rechner würde nur wenig Schutz bieten gegenüber jemandem, der Zugriff auf diesen Rechner hat. Eine Festplattenverschlüsselung schützt eine ausgeschaltete oder gestohlene Festplatte; strenge Zugriffsrechte schützen eine in Betrieb befindliche Festplatte.

## Eine Sicherheitslücke melden

Nutzen Sie **„Sicherheit → Eine Sicherheitslücke melden“** im GitHub-Repository. Geben Sie dabei die Version, die Auswirkungen und eine minimale synthetische Reproduktion an. Senden Sie niemals Anmeldedaten, Kontiverzeichnisse oder echte Beweismittelarchive. Falls eine private Meldung nicht möglich ist, eröffnen Sie ein Ticket, in dem Sie um einen privaten Kanal bitten, ohne Details zum Exploit anzugeben.
