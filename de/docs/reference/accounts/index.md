# Konten und Sitzungsformate

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/

Melden Sie sich per Telefon, QR-Code oder Authentifizierungsschlüssel an, importieren Sie Sitzungen aus Telethon, Pyrogram oder Telegram Desktop und verwalten Sie mehrere Konten.

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

Sie können sich anmelden, ohne eine Telegram-API-Anwendung zu erstellen. Wenn kein Schlüsselpaar eingegeben, importiert oder bereits im Arbeitsbereich gespeichert ist, wählt TgWitness ein Schlüsselpaar aus seinem integrierten Pool von 50 öffentlichen API-Schlüsselpaaren (`tgwitness/api_pool.py`) in zufälliger Reihenfolge aus. Wenn Telegram ein Paar ablehnt (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), wird das nächste versucht, bis zu acht pro Anmeldung; abgelehnte Paare werden bis zum Neustart übersprungen. Das Paar, mit dem die Anmeldung erfolgte, wird zusammen mit dem Konto gespeichert und für dieses wiederverwendet. Eine **API-ID** und **ein API-Hash** identifizieren die Anwendung gegenüber Telegram; sie autorisieren ein Konto jedoch nicht eigenständig.

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

- Die Dateien werden **im Arbeitsspeicher** Ihres TgWitness-Servers konvertiert. Hochgeladene Dateien werden nicht gespeichert, ZIP-Dateien werden nicht auf die Festplatte entpackt und es wird kein externer Dienst kontaktiert.
- Die daraus resultierende Sitzung wird anschließend mit Telegram abgeglichen. Wenn eine Datei eine Benutzer-ID enthält, muss diese mit dem von Telegram gemeldeten Konto übereinstimmen.
- Dateien, die verschiedene Konten oder unterschiedliche API-Zugangsdaten beschreiben, werden abgelehnt, anstatt sich für eine Option zu entscheiden.
- **Das Feld „Passcode“ oder „Session Text“** enthält das lokale TData-Passcode-Feld, ein Feld zum Einfügen einer „StringSession“ sowie **zum Einlesen von Dateien ohne Anmeldung** (das Formular wird ausgefüllt, ohne Telegram zu kontaktieren).

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
- Andere Felder wie `phone`, `device`, `sdk`, `app_version`, `lang_pack` oder ein gespeichertes `twoFA`-Passwort werden **ignoriert**. Wenn für das Konto eine 2FA aktiviert ist, fordert TgWitness diese an.
- Eine JSON-Datei allein enthält lediglich Metadaten. Ohne die Sitzungsdatei fahren Sie bitte mit der Anmeldung per Telefon oder QR-Code fort.

### Telegram Desktop (TData)

TData ist der Ordner „`tdata`“ der Telegram-Desktop-Anwendung (die plattformübergreifende App von desktop.telegram.org).

| System | Standardstandort „`tdata`“ |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (portables Telegram: neben `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

So importieren Sie es:

> **Warnung bezüglich paralleler Sitzungen.** Beim Import von TData wird der Autorisierungsschlüssel von Telegram Desktop wiederverwendet; es wird kein eigenständiger Login erstellt. Verwenden Sie diesen Schlüssel nicht gleichzeitig in Desktop und TgWitness. Telegram kann die Autorisierung mit „`AUTH_KEY_DUPLICATED`“ ungültig machen, wodurch beide Instanzen bis zu einem neuen Login unbrauchbar werden.
>
>
>
> Beenden Sie „Desktop“ vollständig, einschließlich des Prozesses in der Taskleiste, und lassen Sie diese Instanz geschlossen, während TgWitness die importierte Sitzung nutzt. **Beenden Sie die Anwendung, melden Sie sich nicht ab und widerrufen Sie die Sitzung nicht:** Ein Widerruf macht auch die importierte Kopie ungültig. Falls Sie beide Clients gleichzeitig ausführen müssen, melden Sie sich per Telefon oder QR-Code bei TgWitness an, um eine eigene Autorisierung zu erstellen. Ein eigenes Konto wird empfohlen, gewährleistet jedoch nicht, dass geklonte Schlüssel sicher parallel verwendet werden können.
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
| `string_session` (`session_string`, `session`) | Text aus der Telethon-StringSession, kein Dateiname |
| `auth_key` (`auth_key_hex`) + `dc_id` | Vollständiger Auth-Schlüssel mit 512 Zeichen und DC 1–5 |
| `user_id` (`id`) | Optional; vor dem Speichern der Autorisierung mit Telegram abgeglichen |

Sind sowohl ein Alias als auch der Hauptname vorhanden, müssen diese übereinstimmen. Beispiele:

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

Unter **Konten → Konten importieren** können Sie mehrere Konten hinzufügen, Dateien nach Basisnamen zuordnen und jedes Anmeldeergebnis sehen. Jedes Konto erhält einen eigenen Arbeitsbereich. Gruppen können ausgewählte Einstellungen aus einer Vorlage kopieren, ohne Sitzungen, Schlüssel oder Belege zusammenzuführen. Siehe [die Anleitung für Import und Gruppen](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) und [das MTProxy-Pool-Dashboard](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Abmelden

**„Konto → Bei Telegram abmelden“** (bei pausierter Überwachung) fordert Telegram auf, die Sitzung zu beenden, sodass diese auch aus den **„Einstellungen → Geräte**“ des Kontos verschwindet und die Sitzung aus dem Arbeitsbereich-Tresor entfernt wird. Das Protokoll, die Quellen, die Einstellungen und der Signaturschlüssel bleiben erhalten, und das Protokoll zeichnet die Abmeldung auf. Der Arbeitsbereich gehört weiterhin zu seinem Konto: Nur dieses Konto kann sich erneut damit verbinden. Wenn Telegram nicht antwortet, wird die Sitzung dennoch hier entfernt und dies wird im Bedienfeld angezeigt; beenden Sie sie in Telegram unter **„Einstellungen“ → „Geräte**“.

## Eine Telethon-Sitzung offline konvertieren

Das Panel importiert `.session`-Dateien direkt. Für eine Offline-Konvertierung in eine StringSession-Datei führen Sie im Projektordner folgenden Befehl aus:

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

Der Konverter liest ausschließlich Telethon-SQLite-Dateien (bis zu 64 MiB), verändert die Eingabedaten in keiner Weise, führt keine Netzwerkanfragen durch und überschreibt keine bereits vorhandene Ausgabedatei.

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
| Proxy-Verbindung fehlgeschlagen | Überprüfen Sie den Routing-Modus und den IP-Modus. Der automatische MTProxy versucht es mit einem anderen funktionierenden Eintrag. Der „IP verbergen“-Modus wartet; der explizit ausgewählte Fallback-Modus kann nach der konfigurierten Verzögerung eine direkte Verbindung herstellen. Siehe [Routing-Modi](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/#ip-modes). |

Siehe auch: [Verbindung und Sicherheit](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/) für Proxys und Verschlüsselung, sowie [die Funktionsweise der Datenerfassung](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/) hinsichtlich der nach der Anmeldung erfassten Inhalte.
