# Sorgen Sie für Sicherheit

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/security/

Was Ihren Rechner verlässt, was jedes Geheimnis öffnet und was die Schutzmaßnahmen abdecken und was an Ihnen hängt.

**127.0.0.1**Standardmäßige Panel-Adresse

**256-Bit**Zufälliges Panel-Token

**0**CDNs, Analysetools oder Remote-Schriftarten

**Ed25519**Signatur auf jedem Datensatz

## Hier finden Sie alles

Collector, Panel und alle Einträge bleiben auf Ihrem Rechner. Standardmäßig wird nur Telegram kontaktiert, alles andere ist ein eigener Schalter.

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
| **Panel-Token** | `panel-token.txt` im Datenverzeichnis; der Browser behält es pro Tab | Alles in jedem Arbeitsbereich | TgWitness stoppen, `panel-token.txt` löschen, neu starten: Sie bekommen ein neues |
| **Telegram-Sitzung** | Vault, verschlüsselt (`credentials.enc`) | Der Telegram-Account selbst | Beenden Sie die Sitzung in Telegram unter *„Einstellungen“ → „Geräte“* |
| **Signaturschlüssel** | Vault, verschlüsselt (`signing.enc`) | Einträge unter Ihrem Fingerabdruck signieren | Anderswo aufbewahrte Prüfpunkte, ein Zeuge und Zeitstempel zeigen weiterhin, was vorher existierte |
| **Tresorschlüssel** | `vault.key` neben den Daten oder ein externer Hauptschlüssel | Den Tresor | Gehen Sie davon aus, dass Sitzung und Signaturschlüssel ebenfalls geleakt sind |
| **Witness-Token** | Auf dem Witness-Host | Nur lesen: Prüfpunkte und Zustand | Auf der Zeugen-Seite löschen, ein neues erstellen |
| **Schlüsseltext für externe Seiten** | Vault; einmal herunterladen, um Daten wiederherzustellen | Die externe Kopie | Wer auch den Bucket hat, kann sie entschlüsseln: betrachten Sie die Kopie als offengelegt |

## Was die Schutzmaßnahmen abdecken

### Abgedeckt

- Ein geänderter, entfernter oder umsortierter Eintrag: Die Hash-Kette oder eine Signatur bricht.
- Ein Journal, das gekürzt oder neu aufgebaut wurde, nachdem Sie einen Prüfpunkt anderswo gespeichert haben: Der Prüfpunkt passt nicht mehr.
- Das Token erraten: 256 Zufallsbits, Vergleich in konstanter Zeit, 15 Fehlversuche pro Minute und die Adresse wird gesperrt.
- Feindselige Chat-Inhalte: Text bleibt Text, nie HTML; Anhänge werden als Dateien heruntergeladen; das Panel lädt nichts von anderen Seiten.
- Ein gestohlenes Datenverzeichnis bei externem Tresorschlüssel: Sitzungen und Schlüssel bleiben verschlüsselt.

### Ich überlasse es Ihnen

- Das Haupttoken kann alles. Geben Sie anderen begrenzten Zugriff und behalten Sie das Haupttoken für sich.
- Wer Admin auf dem Rechner ist, kann alles lesen und das Journal neu signieren. Bewahren Sie Fingerabdruck und Prüfpunkte anderswo auf.
- Nachrichten und Medien verschlüsselt TgWitness nicht. Verschlüsseln Sie die Festplatte, schränken Sie die Rechte ein.
- Einfaches HTTP außerhalb von localhost gibt das Token preis. Nutzen Sie HTTPS oder einen SSH-Tunnel.
- Signaturen sagen Ihnen nicht, was verpasst wurde. Prüfen Sie Abdeckung und Zustellung auf Ihren eigenen Konten und Quellen.

[Teilen Sie den Zugriff auf einen Fall](https://phishdestroy.github.io/TgWitness/de/docs/access/) mit Berechtigungen, Ablaufdatum und Sitzungslimits.

## Eine Installation absichern

0 von 8 fertiggestellt

1. **Nutzen Sie ein eigenes Telegram-Konto**, nie Ihr Hauptkonto.
2. **Lassen Sie das Panel auf 127.0.0.1.** Fernzugriff nur über HTTPS (mitgeliefertes Caddy) oder einen SSH-Tunnel.
3. **Verschlüsseln Sie die Festplatte** mit dem Datenverzeichnis, Nachrichten und Medien liegen so, wie sie ankamen.
4. **Beschränken Sie das Datenverzeichnis** auf das Dienstkonto (0700 unter Unix, Ordnerrechte unter Windows).
5. **Bewahren Sie den Tresorschlüssel anderswo auf** auf Servern: setzen Sie `TGWITNESS_VAULT_KEY_FILE` vor dem ersten Start.
6. **Speichern Sie Fingerabdruck und Prüfpunkte** auf einem anderen System, betreiben Sie einen Zeugen auf einem anderen Host.
7. **Laden Sie niemals** `data/`-, Sitzungs-, `panel-token.txt`- oder Tresorschlüssel auf GitHub oder in einen Chat **hoch**.
8. `Authorization`-Header oder Request-Bodies **dürfen** an einem Reverse-Proxy **nicht protokolliert werden**.

**Kann ich das Panel-Token ändern, ohne Daten zu verlieren?**

Ja, es öffnet nur das Panel. TgWitness stoppen, `panel-token.txt` löschen, neu starten. Journal, Sitzungen und Schlüssel bleiben. Ist `TGWITNESS_TOKEN` gesetzt, hat dieser Wert Vorrang vor der Datei.

**Warum werden Nachrichten im Ruhezustand nicht verschlüsselt?**

Der Collector muss sie lesen, um zu suchen, zu vergleichen und zu exportieren. Ein Schlüssel auf demselben Rechner würde niemanden aufhalten, der diesen Rechner ohnehin lesen kann. Festplattenverschlüsselung schützt eine gestohlene Platte, Rechte schützen eine laufende.

## Eine Sicherheitslücke melden

**Security → Report a vulnerability** auf GitHub. Version, Auswirkung und ein minimales Beispiel mit erfundenen Daten. Schicken Sie nie Zugangsdaten, Kontoordner oder echte Beweise. Ist die private Meldung aus, eröffnen Sie ein Issue und bitten Sie um einen privaten Kanal, ohne Exploit-Details.
