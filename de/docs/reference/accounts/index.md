# Konten und Sitzungsformate

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/

Melden Sie sich per Telefon, QR-Code oder Authentifizierungsschlüssel an, importieren Sie Sitzungen aus Telethon, Pyrogram oder Telegram Desktop und verwalten Sie mehrere Konten.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Erste Schritte](https://phishdestroy.github.io/TgWitness/de/docs/reference/quickstart/)

![Erste Schritte](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

TgWitness meldet sich über MTProto als **Telegram-Benutzerkonto** (nicht als Bot) an und nutzt dabei Telethon. Jedes Konto befindet sich in einem eigenen **Arbeitsbereich** (in der API und den Befehlszeilentools als *„Workspace“* bezeichnet) mit eigener Sitzung, eigenen Quellen, eigenem Protokoll und eigenem Signaturschlüssel.

Sitzungsdateien, Sitzungsstrings und Auth-Keys sind **Kontoautorisierungen**: Wer auch immer im Besitz einer solchen ist, kann im Namen dieses Kontos handeln. Sie enthalten keinen Nachrichtenverlauf.

> [!WARNUNG] **Verwenden Sie nichts, dessen Verlust Sie sich nicht leisten können.** Wir raten dringend davon ab, persönliche oder anderweitig wertvolle Konten zu verknüpfen sowie eine API-ID bzw. einen API-Hash für ein Konto zu erstellen, das Ihnen wichtig ist. Dabei geht es nicht darum, dass TgWitness ungetestet ist: Telegram schränkt Konten ein und sperrt sie unvorhersehbar dauerhaft – bei Anfragevolumina, die es als übermäßig erachtet, unabhängig vom Client oder Zweck und ohne angemessene Dokumentation. Viele Sperren sind irreversibel. Verwenden Sie dafür eigens eingerichtete Konten. Reibungslose Testläufe hängen von Telegram ab, nicht von der Software, und bieten keinerlei Garantie für die Zukunft.

- [Auf einen Blick](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#at-a-glance)
- [Bevor Sie beginnen: API-ID und API-Hash](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Telefonnummer](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#phone-number) · [QR-Code](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#qr-code) · [Authentifizierungsschlüssel + DC-ID](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#auth-key--dc-id)
- [Kontodateien](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#pyrogram-session) · [Paar aus Sitzung und JSON](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#telethon-stringsession) · [JSON-Datei für das Konto](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#account-json)
- [Ermitteln Sie, was Ihnen vorliegt](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#identify-what-you-have) · [Nicht unterstützte Formate](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#unsupported-formats)
- [Mehrere Konten](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#multiple-accounts) · [Sichere Aufbewahrung von Kontodateien](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#keeping-account-files-safe) · [Fehlerbehebung](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#troubleshooting)

## Auf einen Blick

| Was Sie haben | Registerkarte **„Konto hinzufügen“** | Außerdem benötigen Sie |
| --- | --- | --- |
| Die Telefonnummer und der Zugriff auf die Anmeldedaten | **Telefon** | 2FA-Passwort, sofern aktiviert |
| Telegram auf einem anderen Gerät geöffnet | **QR-Code** | 2FA-Passwort, sofern aktiviert |
| Eine `.session`-Datei (Telethon oder Pyrogram) | **Dateien** | Optionales begleitendes JSON-Dokument für App-Einstellungen |
| `.session` + `.json` mit demselben Namen | **Dateien** (bitte beide auswählen) | In der Regel nichts weiter |
| Ein „`tdata`“-Ordner in Telegram Desktop | **Dateien** (als ZIP) | Der lokale Desktop-Zugangscode, sofern einer festgelegt wurde |
| Eine Telethon-StringSession (Text, `.txt`, `.tgwitness-session`) | **Dateien** | Es ist kein separates API-Paar erforderlich |
| Ein „`.json`“ mit einer Sitzung oder einem Authentifizierungsschlüssel | **Dateien** | Es ist kein separates API-Paar erforderlich |
| Ein Auth-Schlüssel (512 Hexadezimalzeichen) und dessen DC-Nummer | **Authentifizierungsschlüssel** | Optionale Benutzer-ID |

TgWitness erkennt Dateien anhand ihres **Inhalts**, nicht anhand ihrer Namen. Das Umbenennen einer Datei führt niemals zu einer Konvertierung.

## Bevor Sie beginnen: API-ID und API-Hash

Sie können sich anmelden, ohne eine Telegram-API-Anwendung zu erstellen. Wenn kein Paar eingegeben, importiert oder bereits im Arbeitsbereich gespeichert ist, wählt TgWitness ein Paar aus seinem integrierten Pool von 50 öffentlichen API-Paaren (`tgwitness/api_pool.py`) aus, wobei es bei einer neuen Anmeldung Telegram Desktop bevorzugt und ein gespeichertes Paar vorrangig verwendet; die verbleibenden Kandidaten werden gemischt. Wenn Telegram ein Paar (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`) ablehnt, wird das nächste versucht, bis zu acht pro Anmeldung; abgelehnte Paare werden bis zum Neustart übersprungen. Das Paar, mit dem die Anmeldung erfolgte, wird zusammen mit dem Konto gespeichert und für dieses wiederverwendet. Eine **-API-ID** und ein **-API-Hash** identifizieren die Anwendung gegenüber Telegram; sie autorisieren ein Konto nicht von sich aus.

Fehlende Verbindungsfelder verwenden ein deterministisches Geräte-/Betriebssystem-Paar aus den mitgelieferten [opentele2-2.0.0-Katalogen](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735): Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834` und Web `2496`. Die Source-Build-ID `4` von Android verwendet ebenfalls den Android-Katalog, wie in [Telegram Android’s BuildVars](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java) angegeben. Web verwendet standardmäßig A; ein importiertes `K`-App-Versionssuffix oder ein `macos`-Sprachpaket wählt K aus, und die Version `0.7.0` wählt Webogram aus. Unbekannte Anwendungs-IDs behalten die Standardwerte des Telethon-Hosts bei. Importierte Felder haben immer Vorrang, einschließlich einer älteren App-Version und eines leeren Sprachpakets. Der Katalog ändert niemals die API-ID/den Hash. Sein Versions-Snapshot wird explizit überprüft und nicht während der Anmeldung abgerufen. Ein gespeichertes Profil bleibt nach Updates stabil.

`account.getAuthorizations` meldet die von Telegram gespeicherten Autorisierungsmetadaten; es handelt sich dabei nicht um eine Wiederholung jedes neuen `initConnection`. Vergleiche es mit dem tatsächlich gesendeten Profil. Das Verknüpfen einer bestehenden Autorisierung validiert nicht den zugehörigen API-Hash: `initConnection` sendet die API-ID, während der Hash bei Anmeldeanfragen verwendet wird.

Nach einer neuen Telefon- oder QR-Autorisierung fordert TgWitness die Konfiguration, den nächstgelegenen DC, den Online-Status, Sprachen (sofern das Sprachpaket nicht leer ist), App-Updates und Aktualisierungen der Nutzungsbedingungen an, wobei zwischen den Anfragen 0.3–1.5 Sekunden liegen. Die Statusaktualisierung markiert das Konto kurzzeitig als online. Diese Abfolge wird einmalig nach Abschluss der Anmeldung ausgeführt, nicht bei Importen, erneuten Verbindungen oder Neustarts. Die Autorisierung wird zuerst gespeichert; eine fehlgeschlagene Anfrage stoppt die Abfolge, ohne einen erneuten Versuch zu unternehmen oder die Anmeldung zu verwerfen. Die Ergebnisse werden als `account.initialized` aufgezeichnet, wobei Fehlerbezeichnungen anstelle von Antwortinhalten verwendet werden. Die Abfolge bietet keine Garantie gegen Kontoeinschränkungen.

Für `tdesktop` verwendet ein fehlendes `tz_offset` den lokalen UTC-Offset des Servers, gerundet auf 900 Sekunden unter Verwendung des [opentele2-Algorithmus](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; Lizenz in `tgwitness/client_profiles.LICENSE` ). Dieser wird bei jeder Verbindung aktualisiert, sodass Änderungen durch die Sommerzeit berücksichtigt werden. Ein importierter `tz_offset` -Wert hat auf jeder Plattform Vorrang und wird exakt beibehalten, einschließlich des Werts Null. Andere `initConnection.params` -Einträge bleiben erhalten. Das HTTP-Anmeldeformular akzeptiert die durch den Dateiimport zurückgegebene numerische Zeitzone; Boolesche Werte, Bruchteile und Offsets außerhalb des unterstützten Bereichs werden abgelehnt.

Direkte, SOCKS5- und HTTP-CONNECT-Routen verwenden Telethons `ConnectionTcpObfuscated` (verschleiertes, gekürztes MTProto). HTTPS CONNECT behält TLS zum Proxy bei und nutzt denselben verschleierten Transport innerhalb des Tunnels. MTProxy behält seinen erforderlichen zufälligen Zwischentransport und die geheime Handhabung bei. Routenwechsel wenden die gleichen Optionen an. Die Verschleierung verändert die Paketgestaltung; sie verbirgt weder das Konto noch dessen Client-Metadaten vor Telegram und impliziert keine Immunität gegenüber Einschränkungen.

Nach dem Verbindungsaufbau mit einem autorisierten Client überprüft TgWitness die Konfiguration, das nächstgelegene Rechenzentrum, die aktuelle Autorisierung, die überprüfte Basislinie der Ebene, Sprachen, App-Updates sowie Aktualisierungen der Nutzungsbedingungen. Diese Diagnosen werden einmal pro Client-Instanz vor der Datenerfassung durchgeführt und unter den Verbindungsdetails mit dem jeweiligen Zeitpunkt angezeigt. `account.connection_checked` protokolliert das Ergebnis ohne Sitzungs-Hashes, IP-Adressen, Token oder API-Hashes. Es akzeptiert niemals Nutzungsbedingungen und installiert keine Updates. Ein Fehlschlag der Anfrage oder FloodWait stoppt nachfolgende Anfragen; ein fehlendes Ergebnis bleibt unbekannt. Lokale Prüfungen können ihre Ergebnisse weiterhin melden, während Netzwerkprüfungen übersprungen werden.

Die FloodWait-Diagnose speichert die fehlgeschlagene TL-Methode, etwaige Takeout-/Range-Wrapper, die vom Server angeforderte Wartezeit und die effektive Frist in `telegram.backoff`. Die Verbindungsdetails zeigen die Methode und die Frist an, während Anfragen angehalten sind. Die Diagnose umfasst Client-Aufrufzähler pro Methode seit der Erstellung des jeweiligen Clients; sie zählen verschachtelte Peer-Auflösungen separat, berücksichtigen jedoch keine Pakete oder interne Wiederholungsversuche von Telethon. Aktuelle Zählerstände sind auch als `collector.rpc_activity` in der Status-API verfügbar. Es sind keine Anfrageargumente, Benutzernamen, Zugriffs- Hashes oder Ausnahmetexte enthalten. Die letzte Diagnose und die vollständige Frist bleiben nach einem Neustart erhalten. Frühere Wartezeiten ohne Methodendatensatz können nicht nachträglich zugeordnet werden. Siehe „[-Exportgrenzen“](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) für die Quellcodeüberprüfung und die Unterscheidung zwischen Erkennung und Historienerfassung.

`official_app=True` oder `False` ist das Flag für die aktuelle Autorisierung bei Telegram. Keiner der Werte gibt Aufschluss darüber, ob das Konto eingeschränkt, vertrauenswürdig oder unter Beobachtung steht. Die bestehenden `account.devices`-Snapshots im Beweismodus bleiben die Historie aller angemeldeten Geräte; die Verbindungsdiagnose behält nur die aktuelle Gerätebeschreibung bei.

Vor der Verbindung vergleichen Warnprüfungen die API-Plattform, das Sprachpaket, die Formate für Gerät/Betriebssystem und App-Version, die Ländereinstellung des mobilen Systems sowie die tatsächliche Schemaebene von Telethon mit der Basisversion des geprüften Katalogs. Warnungen erscheinen im Serverprotokoll und in den Metadaten zum Kontostatus; sie ersetzen niemals importierte Werte und ändern auch nicht die Schemaebene. Eine andere Ebene ist ein Signal zur Kompatibilitätsprüfung, kein Nachweis für ein defektes oder eingeschränktes Konto. Diese Prüfungen und `official_app` bestätigen nicht, dass Telegram das Konto als frei von Einschränkungen betrachtet. Der Status Getrenntes Konto verwendet das gespeicherte Profil, anstatt eine weitere Gerätebeschreibung zu generieren.

Um stattdessen Ihre eigene Anwendung zu verwenden (das Konto, unter dem diese registriert ist, ist dem Risiko ausgesetzt; siehe [„Warum ein integrierter API-Pool?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)“):

1. Öffnen Sie [my.telegram.org](https://my.telegram.org) und melden Sie sich mit einer beliebigen Telefonnummer an, die Ihnen gehört. Der Code wird in der Telegram-App angezeigt, nicht per SMS.
2. Wählen Sie **API-Entwicklungstools** aus.
3. Erstellen Sie eine Anwendung: beliebiger Titel und Kurzname (5–32 Zeichen), Plattform **„Desktop**“. URL und Beschreibung können leer bleiben.
4. Kopieren Sie **die App-API-ID** (eine Zahl) und **den App-API-Hash** (32 hexadezimale Zeichen).

Im Bedienfeld finden Sie die Felder **„API-ID“ und „Hash“** unterhalb des Anmeldeformulars. Sie können ein einzelnes „`api_id:api_hash`“-Paar in **das Feld „API-ID“** einfügen, woraufhin beide Felder automatisch ausgefüllt werden. Ein einziges Paar kann für alle Ihre Konten verwendet werden. Nach erfolgreicher Anmeldung wird es verschlüsselt ausschließlich in diesem Arbeitsbereich gespeichert und niemals an den Browser zurückgesendet.

Es sind drei verschiedene Zugangsdaten beteiligt:

| Geheim | Öffnet | Verfügbarkeit |
| --- | --- | --- |
| Panel-Token | Das TgWitness-Webpanel | `panel-token.txt` im Datenverzeichnis oder `TGWITNESS_TOKEN` |
| API-ID + Hash | Für sich genommen nichts Besonderes; identifiziert die App | Integriertes Paar, importierte Einstellungen oder Ihre eigene App unter my.telegram.org |
| Kontoautorisierung | Der Telegram-Account | Erstellt per Telefon-/QR-Anmeldung oder als Sitzung importiert |

Falls Telegram über einen Proxy erreicht werden muss, nehmen Sie die entsprechenden **Einstellungen** zunächst unter **„Konto“ → „Einstellungen“ → „Verbindungseinstellungen“ → „Verbindungsroute ändern“** vor.

## Telefonnummer

1. Eröffnen Sie **ein Konto**, wechseln Sie zur Registerkarte **„Telefon“** und geben Sie die Nummer im internationalen Format ein, beispielsweise `+44 7700 900123`. Leerzeichen und Bindestriche werden automatisch entfernt.
2. Klicken Sie auf **„Weiter**“. Die Felder „API-ID“ und „Hash“ können leer bleiben.
3. Geben Sie den Code ein, den Telegram versendet (in der Regel an die Telegram-App; der Empfang per SMS kann nicht garantiert werden).
4. Falls für das Konto eine zweistufige Verifizierung eingerichtet ist, geben Sie dieses Passwort ein. Es handelt sich dabei nicht um das Panel-Token und auch nicht um einen Gerätezugangscode.
5. Überprüfen Sie die nach der Anmeldung angezeigte Konto-ID und wählen Sie anschließend die Quellen aus.

Anmeldedaten und das 2FA-Passwort werden niemals auf die Festplatte geschrieben.

## QR-Code

Verwenden Sie diese Option, wenn das Konto bereits auf einem Smartphone oder einem anderen Computer angemeldet ist.

1. Registerkarte **„QR-Code“** → **QR-Code anzeigen**. API-ID + Hash können leer bleiben.
2. Auf dem angemeldeten Gerät: **Einstellungen → Geräte → Desktop-Gerät verknüpfen**, den Code scannen und bestätigen.
3. Geben Sie das 2FA-Passwort in TgWitness ein, falls Telegram Sie dazu auffordert.

Das QR-Bild wird lokal generiert. Codes verfallen; klicken Sie auf **„Einen weiteren QR-Code generieren“,** um es erneut zu versuchen. Das Sperren des Fensters, das Wechseln des Arbeitsbereichs oder das Starten einer weiteren Anmeldung bricht einen ausstehenden Code ab.

## Authentifizierungsschlüssel + DC-ID

Ein Auth-Key ist der 256-Byte-Autorisierungsschlüssel, der jeder Telegram-Sitzung zugrunde liegt und als **512 hexadezimale Zeichen** zusammen mit der Rechenzentrumsnummer **DC 1–5** geschrieben wird.

1. Registerkarte **„Auth-Schlüssel**“. Fügen Sie den vollständigen Schlüssel ein; ein verkürzter Schlüssel, der „`…`“ enthält, funktioniert nicht.
2. Wählen Sie die mit dem Schlüssel bereitgestellte DC-ID aus.
3. Geben Sie optional die **Benutzer-ID** ein. TgWitness lehnt die Verbindung dann ab, falls Telegram ein anderes Konto meldet.
4. Press **Connect-Konto**.

Ein Auth-Schlüssel (512 Zeichen) ist kein API-Hash (32 Zeichen). Derselbe Schlüssel kann auch als JSON importiert werden, siehe [Account-JSON](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#account-json).

## Kontodateien

Öffnen Sie **„Konto hinzufügen“ → „Dateien“** und wählen Sie bis zu **vier Dateien** aus, **die zu einem Konto gehören** (insgesamt **8 MiB**), und klicken Sie anschließend auf **„Konto verbinden**“.

Die Formulare „**Files**“, „**Auth key**“ und Bulk-Import zeigen vor dem Verbindungsaufbau die Warnung bezüglich paralleler Sitzungen an. Standardmäßig werden importierte Autorisierungen wiederverwendet. Halten Sie den ursprünglichen Client geschlossen, solange dessen Schlüssel hier verwendet wird. „**Files**“ und „**Auth key**“ bieten zudem die Option „**Create an independent authorization**“ an, die weiter unten beschrieben wird. Der Massenimport nutzt weiterhin den Direktmodus. Bei der Anmeldung per Telefon und über interaktiven QR-Code werden separate Autorisierungen erstellt. Die Warnungsüberschrift bleibt im Importformular sichtbar; die vollständige Erklärung wird automatisch angezeigt, sobald Dateien oder eine Schlüssel-/Sitzungszeichenfolge eingegeben werden. Sie kann nach dem Lesen ausgeblendet werden, sodass die Dateiauswahl und die Verbindungssteuerelemente auf einem Smartphone weiterhin nutzbar bleiben.

- Die Dateien werden **im Arbeitsspeicher** Ihres TgWitness-Servers konvertiert. Hochgeladene Dateien werden nicht gespeichert, ZIP-Dateien werden nicht auf die Festplatte entpackt und es wird kein externer Dienst kontaktiert.
- Die daraus resultierende Sitzung wird anschließend mit Telegram abgeglichen. Wenn eine Datei eine Benutzer-ID enthält, muss diese mit dem von Telegram gemeldeten Konto übereinstimmen.
- Dateien, die verschiedene Konten oder unterschiedliche API-Zugangsdaten beschreiben, werden abgelehnt, anstatt sich für eine Option zu entscheiden.
- **Das Feld „Passcode“ oder „Session Text“** enthält das lokale TData-Passcode-Feld, ein Feld zum Einfügen einer „StringSession“ sowie **zum Einlesen von Dateien ohne Anmeldung** (das Formular wird ausgefüllt, ohne Telegram zu kontaktieren).

### Erstellen Sie eine eigenständige Autorisierung

Wählen Sie „**Unabhängige Autorisierung erstellen“**, bevor Sie importierte Dateien oder einen Auth-Schlüssel verbinden. TgWitness verbindet den importierten Spender kurzzeitig, nutzt ihn zur Genehmigung des QR-Anmeldetokens des neuen Clients und trennt die Verbindung zum Spender unmittelbar nach der Genehmigung. Der neue Client verfügt über einen eigenen Autorisierungsschlüssel und ein separat ausgewähltes Desktop- Profil. Die vom Spender bereitgestellten API-Anmeldedaten und das Geräteprofil werden ausschließlich für die Verbindung zum Spender verwendet. Keine bestehende Autorisierung wird abgemeldet oder widerrufen.

**Halten Sie den ursprünglichen Client des Spenders während dieses Schritts vollständig geschlossen.** Die anfängliche Verbindung nutzt weiterhin den kopierten Schlüssel, daher kann dieser Modus das anfängliche Risiko einer parallelen Nutzung nicht beseitigen. Sobald die neue Autorisierung hergestellt ist, kann der Besitzer den ursprünglichen Client wieder öffnen und beide unabhängig voneinander nutzen. Die interaktive **QR-Code**-Anmeldung ermöglicht es dem ursprünglichen Client, die Anmeldung zu genehmigen, ohne seinen Schlüssel hier zu kopieren oder zu verbinden.

Wenn Telegram „2FA“ anfordert, verwendet dieser Modus `twoFA` aus der ausgewählten JSON-Datei, sofern vorhanden, oder fragt nach dem Passwort. Bei einem abgelehnten importierten Passwort erfolgt eine Rückkehr zum Passwortformular. Passwörter werden nicht gespeichert. Der Kandidatenschlüssel wird verschlüsselt in `independent_login.enc` gespeichert, einschließlich Änderungen während der Migration des Rechenzentrums. Nach einer Unterbrechung wählen Sie denselben Spender und diese Option aus, um den gespeicherten Kandidaten wiederherzustellen. Der Arbeitsbereich bleibt für dieses Konto reserviert; ein fehlgeschlagener Abschluss löscht den neuen Arbeitsbereich nicht. Behalten Sie dessen Datenverzeichnis und Tresorschlüssel bei. Die endgültigen Anmeldedaten und der `account.authorized`-Journal-Eintrag enthalten die Importmethode, die Eingabeformate und die Spender-API-ID, jedoch ohne den Spenderschlüssel oder das Passwort.

Am 5. November 2026 bestand ein spezielles Konto Live-Prüfungen mit den Anbietern Telethon, Pyrogram und TData: Abschluss der 2-Faktor-Authentifizierung, eindeutige neue Autorisierungsschlüssel, gleichzeitiger Zugriff durch den Anbieter und einen neuen Client sowie das Lesen eines öffentlichen Kanals. Im Telethon-Fall wurde zudem ein gespeicherter Kandidat nach einer Unterbrechung im Passwortschritt wieder aufgenommen. Jede neue Autorisierung schloss die sechs Initialisierungsanfragen nach der Anmeldung ab, und das signierte Journal wurde verifiziert. Die ursprüngliche Sitzung blieb in allen vier bereitgestellten Formaten nutzbar.

Die [RPC-Fehlerdatenbank von Telegram](https://core.telegram.org/api/errors.json) ordnet `FRESH_CHANGE_ADMINS_FORBIDDEN` dem Wechsel von Administratoren, `FRESH_CHANGE_PHONE_FORBIDDEN` der Änderung der Telefonnummer und `FRESH_RESET_AUTHORISATION_FORBIDDEN` dem Widerrufen anderer Sitzungen, der Änderung ihrer Laufzeit oder der Registrierung eines Passworts zu. `SESSION_TOO_FRESH_*` und `PASSWORD_TOO_FRESH_*` betreffen Eigentumsübertragungen sowie Einnahmen- oder Geschenkabhebungen. Hierbei handelt es sich nicht um Erfassungsvorgänge; eine neue Anmeldung bedeutet kein pauschales 24-stündiges Leseverbot. Der Export kann `TAKEOUT_INIT_DELAY_*` separat zurückgeben. TgWitness behält vom Server angeforderte Pausen bei und versucht nicht, die Token-Akzeptanz automatisch erneut durchzuführen oder Sitzungen zu widerrufen, um Einschränkungen zu umgehen.

### Telethon `.session`

|  |  |
| --- | --- |
| Was ist das? | Die SQLite-Datenbank, die von Telethon-basierten Tools erstellt wird, zum Beispiel `my_account.session` |
| Anerkannt von | Tabellen `sessions` (zusammen mit `dc_id`, `server_address`, `port`, `auth_key`) und `version` = 7 oder 8 |
| Anforderungen | Genau eine Zeile mit autorisierten Sitzungen; eine geschlossene, vollständige Datenbank |

Schließen Sie zunächst das Programm, das die Datei erstellt hat. Falls `my_account.session-journal` oder `my_account.session-wal` daneben vorhanden sind, ist die Datenbank noch nicht abgeschlossen: Öffnen und schließen Sie den ursprünglichen Client ordnungsgemäß. Das Löschen dieser Sidecar-Dateien kann zu einer beschädigten Kopie führen.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Was ist das? | Die SQLite-Datenbank, die von Pyrogram-basierten Tools erstellt wird |
| Anerkannt von | Tabelle `sessions` mit `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 oder 3 |
| Anforderungen | Eine autorisierte Benutzersitzung im Produktionsnetzwerk. Bot- und Test-DC-Sitzungen werden abgelehnt. |

Die gespeicherte Benutzer-ID wird bei der Anmeldung mit den Daten von Telegram abgeglichen.

### Paar aus Sitzung und JSON

Die Datensätze werden häufig als zwei Dateien mit demselben Namen bereitgestellt, beispielsweise „ `447700900123.session`“ und „`447700900123.json`“. Wählen Sie **beide** gleichzeitig aus.

- Ausgehend vom JSON verwendet TgWitness `app_id`/`api_id` und `app_hash`/`api_hash`, sodass Sie in der Regel keine API-Anmeldedaten eingeben müssen.
- Das Verbindungsprofil verwendet `device_model` (Alias `device`), `system_version` (Alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (Alias `system_lang_pack`), `lang_pack` und optional `tz_offset` (Sekunden ab UTC, -43200 bis 50400). Angegebene Felder haben Vorrang vor generierten Standardwerten und der Sprache des Panels bzw. Browsers . Widersprüchliche Aliase werden abgelehnt. Das aufgelöste Profil wird in den verschlüsselten Arbeitsbereichs-Anmeldedaten gespeichert und nach einem Neustart wiederverwendet, einschließlich der App-Version.
- `phone`, Proxy-Einstellungen und Gerätetoken werden **ignoriert**. `twoFA` ist schreibgeschützt, wenn **Unabhängige Autorisierung erstellen** ausgewählt ist; beim direkten Import wird es ignoriert.
- Ein JSON ohne ein unterstütztes Autorisierungsfeld ist lediglich Metadaten. Fügen Sie die zugehörige Sitzungsdatei hinzu oder fahren Sie mit der Anmeldung per Telefon oder QR-Code fort. Ein JSON, das eine unterstützte Sitzung oder einen Auth-Schlüssel enthält, kann eigenständig autorisieren; siehe [Account JSON](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData ist der Ordner „`tdata`“ der Telegram-Desktop-Anwendung (die plattformübergreifende App von desktop.telegram.org).

| System | Standardstandort „`tdata`“ |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (portables Telegram: neben `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

So importieren Sie es:

> **Warnung vor parallelen Sitzungen.** Der direkte TData-Import verwendet den Autorisierungsschlüssel von Telegram Desktop erneut . Verwenden Sie diesen Schlüssel nicht gleichzeitig in Desktop und TgWitness. Telegram kann die Autorisierung mit `AUTH_KEY_DUPLICATED` ungültig machen, wodurch beide Instanzen bis zu einer erneuten Anmeldung unbrauchbar werden.
>
>
>
> Beenden Sie Desktop vollständig, einschließlich des Taskleistens-Prozesses, und lassen Sie diese Instanz geschlossen, während TgWitness die importierte Sitzung nutzt. **Beenden Sie die Anwendung, melden Sie sich nicht ab und widerrufen Sie die Sitzung nicht:** Ein Widerruf macht auch die importierte Instanz ungültig. Wenn beide Clients laufen müssen, wählen Sie **Unabhängige Autorisierung erstellen** und lassen Sie den Desktop geschlossen, bis die neue Anmeldung erfolgreich ist, oder melden Sie sich bei TgWitness per Telefon oder QR-Code an. Ein eigenes Konto wird empfohlen, macht die parallele Nutzung geklonter Schlüssel jedoch nicht sicher.
>
>
>
> Dies gilt auch für importierte `.session`-Dateien, StringSession-Text und Auth-Key-HEX-Daten. Andere Clients mit eigenen, unabhängig erstellten Autorisierungen können angemeldet bleiben. Siehe [die Dokumentation zu „AUTH_KEY_DUPLICATED“ von Telegram](https://core.telegram.org/api/errors#406-not-acceptable).

1. Beenden Sie Telegram Desktop vollständig.
2. Erstellen Sie eine ZIP-Datei, die **ausschließlich** diese beiden Elemente aus `tdata` enthält:

   - `key_datas`
   - die 16-stellige Dateiendung „`s`“ daneben, in der Regel „`D877F783D5D3EF8Cs`“

   Das Komprimieren des gesamten Ordners einschließlich seines Medien-Caches überschreitet in der Regel die Grenzwerte (512 Einträge, 32 MiB entpackt). 3. Wählen Sie die ZIP-Datei unter **„Dateien“** aus. Falls für Telegram Desktop ein **lokaler Passcode** eingerichtet ist, geben Sie diesen zunächst unter **„Passcode“ oder „Sitzungstext“** ein. Dies ist nicht das 2FA-Passwort.

Unterstützt: ein Konto pro Archiv, moderner `key_datas`-/`key_data0`-/`key_data1`-Speicher, lokaler Passcode. Nicht unterstützt: Ordner mit mehreren angemeldeten Konten, ältere Desktop- Layouts, passwortgeschützte ZIP-Dateien sowie die separate native macOS-App „Telegram für macOS“.

### Telethon StringSession

Eine einzelne Textzeile, die in der Regel mit „`1`“ beginnt und etwa 350 Zeichen lang ist. Laden Sie sie als „`.txt`“- oder „`.tgwitness-session`“-Datei (maximal 4 KiB) hoch oder fügen Sie sie unter **„Passcode“ oder „Sitzungstext“** ein. Es werden ausschließlich Telethon-Zeichenfolgen akzeptiert; Pyrogram- und TDLib- Zeichenfolgen verwenden andere Formate.

### JSON-Datei für das Konto

Ein JSON-Objekt mit einer Größe von maximal **64 KiB** in einer Datei mit der Endung „**`.json`**“.

| Feld (Aliase) | Bedeutung |
| --- | --- |
| `api_id` (`app_id`) | Anwendungs-ID, eine positive Zahl |
| `api_hash` (`app_hash`) | Anwendungs-Hash, 32 hexadezimale Zeichen |
| `string_session` (`session_string`, `session_str`; veraltetes `session`) | Text aus der Telethon-StringSession, kein Dateiname |
| `auth_key` (`auth_key_hex`) + `dc_id` | Vollständiger Auth-Schlüssel mit 512 Zeichen und DC 1–5 |
| `user_id` (`id`) | Optional; vor dem Speichern der Autorisierung mit Telegram abgeglichen |
| `device_model` (`device`) | Beschreibung des Verbindungsgeräts |
| `system_version` (`sdk`) | Version des verbundenen Betriebssystems |
| `app_version` | An Telegram gesendete Anwendungsversion |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Client-Sprache, Systemsprache und Client-Sprachpaket; ein leeres `lang_pack` ist zulässig |
| `tz_offset` | Optionaler UTC-Offset in Sekunden, gesendet in `initConnection.params`; Ganzzahl oder dezimale Ganzzahl als Zeichenkette |

Sind sowohl ein Alias als auch der Hauptname vorhanden, müssen diese übereinstimmen. Explizite Telethon- Sitzungsfelder haben Vorrang vor einem generischen `session`-Blob in einem anderen Format. Wenn beide erkennbare Telethon-Sitzungen enthalten, müssen sie dieselbe Autorisierung beschreiben. Ohne ein explizites Feld muss `session` eine gültige Telethon-StringSession sein. Beispiele:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

Im ersten Beispiel werden lediglich die API-Anmeldedaten eingegeben; melden Sie sich per Telefon oder QR-Code an oder fügen Sie eine Sitzungsdatei hinzu. Massenlisten (ein JSON-Array mit Konten) werden nicht akzeptiert.

## Ermitteln Sie, was Ihnen vorliegt

| Wie Sie sehen | Es ist | Verwendung |
| --- | --- | --- |
| `*.session`; beim Öffnen in einem Texteditor wird oben „`SQLite format 3`“ angezeigt | Telethon oder Pyrogram SQLite | **Dateien** (werden automatisch erkannt) |
| Ein Ordner „`tdata`“, der „`key_datas`“ enthält | Telegram Desktop TData | Zwei Dateien als ZIP-Datei komprimieren, dann **„Dateien“** |
| Eine Textzeile, beginnend mit `1`, ca. 350 Zeichen | Telethon StringSession | **Dateien** |
| `*.json` mit `app_id`/`app_hash` | Begleitende Metadaten | **Dateien** zusammen mit der zugehörigen Sitzung |
| `*.json` mit `auth_key` oder `string_session` | JSON-Datei für das Konto | **Dateien** |
| 512 Zeichen `0-9a-f` | Auth-Schlüssel | **Authentifizierungsschlüssel** |
| 32 Zeichen `0-9a-f` | API-Hash | **API-ID + Hash** |
| `td.binlog` oder ein `db.sqlite` aus einer TDLib-App | TDLib-Speicher | Nicht unterstützt |
| `123456789:AA…` | Bot-Token | Nicht unterstützt |

## Nicht unterstützte Formate

| Format | Alternative |
| --- | --- |
| TDLib-Speicher (`td.binlog`) und TDLib-Exporte | Anmeldung per Telefon oder QR-Code |
| Pyrogram-Sitzungs**strings** | Verwenden Sie die Pyrogram-Datei „`.session`“ oder den Telefoncode bzw. den QR-Code. |
| TData mit mehreren angemeldeten Konten | Melden Sie sich von den anderen Konten in Telegram Desktop ab oder verwenden Sie die jeweilige Sitzungsdatei des jeweiligen Kontos |
| Bot-Token | Nicht unterstützt: TgWitness fungiert als Benutzerkonto |
| CSV-/JSON-Listen zahlreicher Konten | Importieren Sie unterstützte Sitzungsdateien über **Konten → Konten importieren** oder melden Sie sich per Telefon/QR in separaten Arbeitsbereichen an |
| Test-DC- oder Bot-Sitzungen | Verwenden Sie ein Produktionsbenutzerkonto |

## Mehrere Konten

Drücken Sie **+** neben der Kontoauswahl oder öffnen Sie **Konto → Einstellungen → Verbindungseinstellungen → Arbeitsbereiche**, geben Sie eine Bezeichnung ein und melden Sie sich an.

- Beliebig viele Arbeitsbereiche, einschließlich des Hauptarbeitsbereichs. Jeder verfügt über eine eigene Sitzung, eine eigene Proxy-Route, Quellen, Erfassungsrichtlinien, ein Protokoll, einen Signaturschlüssel, Checkpoints und Exportfunktionen.
- Das Wechseln des angezeigten Arbeitsbereichs führt nicht dazu, dass die anderen angehalten werden.
- Ein Protokoll bleibt an das Konto gebunden, das es erstellt hat. Die Anmeldung mit einem anderen Konto erfordert einen weiteren Arbeitsbereich, und ein Konto kann nicht zwei Arbeitsbereichen zugeordnet werden.
- Das Haupt-Panel-Token steuert alle Arbeitsbereiche. [Durch die Erteilung von Zugriffsrechten](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/) können andere Personen auf ausgewählte Konten und Chats beschränkt werden, wobei separate Berechtigungen und Sitzungslimits gelten.
- **„Accounts“** benennt einen Arbeitsbereich um und löscht einen hinzugefügten Arbeitsbereich samt dessen Sitzung, Protokoll, Quellen und Signaturschlüssel. Der Hauptarbeitsbereich kann nicht über das Bedienfeld gelöscht werden.

### Stapelimport und Kontogruppen

Verwenden Sie **„Konten“ → „Konten importieren“**, um mehrere Konten hinzuzufügen, Dateien anhand des Basisnamens zuzuordnen und die jeweiligen Anmeldeergebnisse einzusehen. Jedes Konto erhält einen eigenen Arbeitsbereich.

Eine Gruppe fasst verwandte Konten zusammen, ohne deren Sitzungen, Schlüssel oder Beweismaterialien zusammenzuführen. **„Gruppe** unter **‚Konten‘ öffnen**“ führt zu deren Seite unter `/groups/<id>`:

- **Konten:** Verbindungsweg, Beobachtungen und letzte Nachricht jedes Mitglieds, mit den Funktionen **„Alle** starten“ und **„Alle pausieren**“.
- **Erfordert Aufmerksamkeit:** Konten, bei denen die Anmeldung beendet wurde, die nicht verfügbar sind oder bei denen ein Verbindungs-, Erfassungs-, Quellen- oder Medienproblem vorliegt; jeder Name führt zu der entsprechenden Karte.
- **Chats mehrerer Konten zeigen:** gemeinsam genutzte Quellen, die Konten, die diese beobachten, sowie Unterbrechungen im verfügbaren Beobachtungszeitraum des Arbeitsbereichs (bis zu sieben Tage). **Der Export mit N Konten** teilt den Export eines Kanals oder einer Supergruppe auf diese Konten auf und signiert ein Archiv.
- **Gruppe exportieren:** ein ZIP mit dem signierten Export jedes Kontos unter `accounts/` und `manifest.json` mit einer Auflistung der SHA-256- und Schlüssel-Fingerabdrücke, signiert vom Haupt- Arbeitsbereich in `manifest.signature.json`. Überprüfen Sie jedes Kontoarchiv einzeln mit `python -m tgwitness.verify` und dem vertrauenswürdigen Fingerabdruck dieses Kontos.

Die Mitglieder nutzen die gemeinsamen Einstellungen der Gruppe; ein Konto kann jedoch eigene Werte beibehalten. Siehe [„Gemeinsame Einstellungen“](https://phishdestroy.github.io/TgWitness/de/docs/reference/settings/#account-groups), [die Anleitung zu Import und Gruppen](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) sowie [das Dashboard „MTProxy-Pool](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources)“.

## Abmelden

**„Konto → Bei Telegram abmelden“** (bei pausierter Überwachung) fordert Telegram auf, die Sitzung zu beenden, sodass diese auch aus den **„Einstellungen → Geräte**“ des Kontos verschwindet und die Sitzung aus dem Arbeitsbereich-Tresor entfernt wird. Das Protokoll, die Quellen, die Einstellungen und der Signaturschlüssel bleiben erhalten, und das Protokoll zeichnet die Abmeldung auf. Der Arbeitsbereich gehört weiterhin zu seinem Konto: Nur dieses Konto kann sich erneut damit verbinden. Wenn Telegram nicht antwortet, wird die Sitzung dennoch hier entfernt und dies wird im Bedienfeld angezeigt; beenden Sie sie in Telegram unter **„Einstellungen“ → „Geräte**“.

## Sichere Aufbewahrung von Kontodateien

- Behandeln Sie jedes `.session`, jede TData-ZIP-Datei, jede StringSession, jeden Auth-Schlüssel und jede Konto-JSON-Datei wie ein Passwort. TgWitness speichert die importierten Autorisierungsdaten in seinem verschlüsselten Tresor; Sie können die Originaldateien anschließend löschen.
- Führen Sie dieselbe Autorisierung nicht gleichzeitig in zwei Programmen aus. Telegram könnte diese widerrufen (`AUTH_KEY_DUPLICATED`), woraufhin beide Instanzen nicht mehr funktionieren.
- Eine abgelaufene oder widerrufene Sitzung kann nicht durch eine Konvertierung wiederhergestellt werden. Bitte melden Sie sich erneut an.

## Fehlerbehebung

| Meldung oder Symptom | Vorgehensweise |
| --- | --- |
| *Diese Sitzung kann nicht gelesen werden. Schließen Sie den ursprünglichen Client…* | Die SQLite-Datei ist geöffnet oder unvollständig (Sidecar-Datei `-journal`/`-wal`). Beenden Sie das ursprüngliche Programm ordnungsgemäß und kopieren Sie die Datei erneut. |
| *Unterstützte Telethon-SQLite-Schemas: 7 und 8* / *Pyrogram … 2 und 3* | Die Datei wurde mit einer sehr alten oder unbekannten Bibliotheksversion erstellt. Melden Sie sich stattdessen per Telefon/QR-Code an. |
| *Es werden ausschließlich autorisierte Produktionsnutzersitzungen unterstützt* | Die Pyrogram-Datei gehört zu einem Bot oder zum Testnetzwerk. |
| *Das TData-Archiv umfasst mehr als 512 Einträge oder 32 MiB* | Bitte nur die ZIP-Dateien „`key_datas`“ und „`D877F783D5D3EF8Cs`“, nicht den gesamten Ordner. |
| *TData kann nicht entschlüsselt werden. Überprüfen Sie den lokalen Passcode auf dem Desktop.* | Geben Sie den lokalen Passcode von Telegram Desktop unter **„Passcode“ oder „Sitzungstext“** ein. |
| *Importieren Sie jeweils ein TData-Konto* | Telegram Desktop verfügte über mehrere Konten; siehe [„Nicht unterstützte Formate](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#unsupported-formats)“. |
| *Ausgewählte Dateien beschreiben verschiedene Konten oder API-Zugangsdaten* | Wählen Sie Dateien nur aus einem einzigen Konto aus. |
| *Die JSON-Datei enthält keine unterstützten API-Anmeldedaten oder Autorisierungen.* | Überprüfen Sie die Feldnamen in [der JSON-Datei „Account](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#account-json)“. |
| *Ausschließlich API-Metadaten* | Die JSON-Datei enthält keine Sitzung. Fügen Sie die Datei „`.session`“ hinzu oder verwenden Sie die Telefonnummer bzw. den QR-Code. |
| *Der Auth-Key (HEX) muss alle 512 hexadezimalen Zeichen enthalten* | Der Schlüssel ist abgeschnitten oder enthält „`…`“. |
| Die Konto-ID stimmt nicht mit dem importierten Konto überein | Die Benutzer-ID der Datei weicht von der von Telegram gemeldeten ab; die Datei bezieht sich auf ein anderes Konto. |
| Das Konto gehört bereits zu einem anderen Arbeitsbereich | Öffnen Sie diesen Arbeitsbereich, anstatt das Konto zweimal hinzuzufügen. |
| Verbunden, jedoch fehlt eine private Gruppe in der Chat-Liste unter **„Quellen“** | Überprüfen Sie die Mitgliedschaft. Der Picker überprüft die ersten 1.000 Dialoge; erhöhen Sie das Limit unter **„Parameter**“. |
| Proxy-Verbindung fehlgeschlagen | Überprüfen Sie den Routing- und IP-Modus. „Automatic“ MTProxy versucht es mit einem anderen funktionierenden Eintrag. „Hide the address“ wartet; „Direct“ kann als letztes Mittel nach der konfigurierten Verzögerung eine direkte Verbindung herstellen. Siehe [Routing-Modi](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/#ip-modes). |

Siehe auch: [Verbindung und Sicherheit](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/) für Proxys und Verschlüsselung, sowie [die Funktionsweise der Datenerfassung](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/) hinsichtlich der nach der Anmeldung erfassten Inhalte.
