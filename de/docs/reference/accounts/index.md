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

You can sign in without creating a Telegram API application. When no pair is entered, imported or already saved in the workspace, TgWitness picks a pair from its built-in pool of 50 public API pairs (`tgwitness/api_pool.py`), preferring Telegram Desktop for a fresh login and retaining a saved pair first; remaining candidates are shuffled. If Telegram refuses a pair (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), the next one is tried, up to eight per sign-in; refused pairs are skipped until restart. The pair that signed in is saved with the account and reused for it. An **API ID** and **API hash** identify the application to Telegram; they do not authorize an account by themselves.

Missing connection fields use a deterministic device/OS pair from the bundled [opentele2 2.0.0 catalogs](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735): Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834`, and Web `2496`. Android's source-build ID `4` also uses the Android catalog, as identified in [Telegram Android's BuildVars](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web defaults to A; an imported `K` app-version suffix or `macos` language pack selects K, and version `0.7.0` selects Webogram. Unknown application IDs keep Telethon's host defaults. Imported fields always win, including an older app version and an empty language pack. The catalog never changes the API ID/hash. Its version snapshot is reviewed explicitly, not fetched during login. A saved profile stays stable after updates.

`account.getAuthorizations` reports Telegram's saved authorization metadata; it is not an echo of each new `initConnection`. Compare it with the actual sent profile. Connecting an existing authorization does not validate its companion API hash: `initConnection` sends the API ID, while the hash is used by login requests.

After a new phone or QR authorization, TgWitness requests config, nearest DC, online status, languages (when the language pack is nonempty), app updates and terms-of-service updates, with 0.3–1.5 seconds between requests. Updating status briefly marks the account online. This sequence runs once at login completion, not on imports, reconnects or restarts. The authorization is saved first; a failed request stops the sequence without retrying or discarding the login. Results are recorded as `account.initialized`, with error names rather than response bodies. The sequence is not a guarantee against account restrictions.

For `tdesktop`, a missing `tz_offset` uses the server's local UTC offset, rounded to 900 seconds using the [opentele2 algorithm](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; license in `tgwitness/client_profiles.LICENSE`). It is refreshed on each connection so daylight-saving changes are reflected. An imported `tz_offset` takes precedence on every platform and is kept exactly, including zero. Other `initConnection.params` entries are retained. The HTTP sign-in form accepts the numeric timezone returned by file import; booleans, fractions and offsets outside the supported range are rejected.

Direct, SOCKS5 and HTTP CONNECT routes use Telethon's `ConnectionTcpObfuscated` (obfuscated abridged MTProto). HTTPS CONNECT retains TLS to the proxy and uses the same obfuscated transport inside the tunnel. MTProxy retains its required randomized intermediate transport and secret handling. Route switches apply the same choices. Obfuscation changes packet framing; it does not hide the account or its client metadata from Telegram or imply immunity to restrictions.

After connecting an authorized client, TgWitness checks config, nearest DC, the current authorization, the reviewed layer baseline, languages, app updates and terms-of-service updates. These diagnostics run once per client instance, before collection, and are shown under the connection details with their time. `account.connection_checked` records the result without session hashes, IPs, tokens or API hashes. They never accept terms or install updates. A request failure or FloodWait stops subsequent requests; a missing result stays unknown. Local checks can still report their results while network checks are skipped.

FloodWait diagnostics retain the failed TL method, any Takeout/range wrappers, the server-requested wait and the effective deadline in `telegram.backoff`. Connection details show the method and deadline while requests are paused. The diagnostic includes per-method client-call counters since that client was created; they count nested peer resolution separately, but do not count packets or Telethon's internal retry attempts. Current counters are also available as `collector.rpc_activity` in the status API. No request arguments, usernames, access hashes or exception text are included. The last diagnostic and full deadline survive restart. Earlier waits without a method record cannot be attributed retrospectively. See [export limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) for the source review and the distinction between discovery and history acquisition.

`official_app=True` or `False` is Telegram's current-authorization flag. Neither value establishes whether the account is restricted, trusted or under observation. The existing evidence-mode `account.devices` snapshots remain the history of all signed-in devices; connection diagnostics retain only the current device description.

Before connection, advisory checks compare the API platform, language pack, device/OS and app-version formats, mobile system locale, and Telethon's actual schema layer against the reviewed catalog baseline. Warnings appear in the server log and account status metadata; they never replace imported values or change the schema layer. A different layer is a compatibility review signal, not proof of a broken or restricted account. These checks and `official_app` do not certify that Telegram considers the account safe from restrictions. Disconnected account status uses the saved profile instead of generating another device description.

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

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- Die Dateien werden **im Arbeitsspeicher** Ihres TgWitness-Servers konvertiert. Hochgeladene Dateien werden nicht gespeichert, ZIP-Dateien werden nicht auf die Festplatte entpackt und es wird kein externer Dienst kontaktiert.
- Die daraus resultierende Sitzung wird anschließend mit Telegram abgeglichen. Wenn eine Datei eine Benutzer-ID enthält, muss diese mit dem von Telegram gemeldeten Konto übereinstimmen.
- Dateien, die verschiedene Konten oder unterschiedliche API-Zugangsdaten beschreiben, werden abgelehnt, anstatt sich für eine Option zu entscheiden.
- **Das Feld „Passcode“ oder „Session Text“** enthält das lokale TData-Passcode-Feld, ein Feld zum Einfügen einer „StringSession“ sowie **zum Einlesen von Dateien ohne Anmeldung** (das Formular wird ausgefüllt, ohne Telegram zu kontaktieren).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

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
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData ist der Ordner „`tdata`“ der Telegram-Desktop-Anwendung (die plattformübergreifende App von desktop.telegram.org).

| System | Standardstandort „`tdata`“ |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (portables Telegram: neben `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

So importieren Sie es:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
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
| `string_session` (`session_string`, `session_str`; legacy `session`) | Text aus der Telethon-StringSession, kein Dateiname |
| `auth_key` (`auth_key_hex`) + `dc_id` | Vollständiger Auth-Schlüssel mit 512 Zeichen und DC 1–5 |
| `user_id` (`id`) | Optional; vor dem Speichern der Autorisierung mit Telegram abgeglichen |
| `device_model` (`device`) | Connection device description |
| `system_version` (`sdk`) | Connection OS version |
| `app_version` | Application version sent to Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Client language, system language and client language pack; an empty `lang_pack` is allowed |
| `tz_offset` | Optional UTC offset in seconds, sent in `initConnection.params`; integer or decimal integer string |

If both an alias and the main name are present, they must agree. Explicit Telethon session fields take priority over a generic `session` blob in another format. If both contain recognizable Telethon sessions, they must describe the same authorization. Without an explicit field, `session` must be a valid Telethon StringSession. Examples:

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
