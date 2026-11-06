# Account e formati delle sessioni

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/

Accedete tramite telefono, codice QR o chiave di autenticazione, importate sessioni da Telethon, Pyrogram o Telegram Desktop ed gestite più account.

TgWitness effettua l’accesso come **account utente di Telegram** (non come bot) tramite MTProto, utilizzando Telethon. Ogni account risiede nel proprio **spazio** di lavoro (denominato *«workspace»* nell’ API e negli strumenti da riga di comando) con la propria sessione, le proprie fonti, il proprio registro e la propria chiave di firma.

I file di sessione, le stringhe di sessione e le chiavi di autenticazione costituiscono **autorizzazioni relative all’account**: chiunque ne sia in possesso può agire come se fosse titolare di quell’account. Essi non contengono la cronologia dei messaggi.

> [!AVVERTENZA] **Non utilizzi nulla che non possa permettersi di perdere.** Le sconsigliamo vivamente di collegare account personali o comunque di valore, nonché di creare un ID API o un hash API su un account a cui tiene particolarmente. Non si tratta del fatto che TgWitness non sia stato testato: Telegram limita e sospende definitivamente gli account in modo imprevedibile — per volumi di richieste che ritiene eccessivi, indipendentemente dal client o dallo scopo, senza adeguata documentazione. Molti blocchi sono irreversibili. Utilizzi account dedicati. Il corretto svolgimento dei test dipende da Telegram, non dal software, e non garantisce nulla per il futuro.

- [In sintesi](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#at-a-glance)
- [Prima di iniziare: ID API e hash API](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Numero di telefono](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#phone-number) · [Codice QR](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#qr-code) · [Chiave di autenticazione + ID DC](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#auth-key--dc-id)
- [File degli account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#pyrogram-session) · [Coppia sessione + JSON](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#telethon-stringsession) · [Account JSON](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#account-json)
- [Identifichi ciò di cui dispone](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#identify-what-you-have) · [Formati non supportati](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#unsupported-formats)
- [Account multipli](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#multiple-accounts) · [Garantire la sicurezza dei file degli account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#keeping-account-files-safe) · [Risoluzione dei problemi](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#troubleshooting)

## In sintesi

| Cosa avete a disposizione | Scheda **“Aggiungi account”** | Le serviranno inoltre |
| --- | --- | --- |
| Il numero di telefono e l’accesso ai relativi codici di accesso | **Telefono** | Password 2FA, se abilitata |
| Telegram aperto su un altro dispositivo | **Codice QR** | Password 2FA, se abilitata |
| Un file `.session` (Telethon o Pyrogram) | **File** | File JSON opzionale di accompagnamento per le impostazioni dell’app |
| `.session` + `.json` con lo stesso nome | **File** (selezionare entrambi) | Di norma, nient’altro |
| Una cartella «`tdata`» in Telegram Desktop | **File** (in formato ZIP) | Il codice di accesso locale per il desktop, qualora ne sia stato impostato uno |
| Una StringSession di Telethon (testo, `.txt`, `.tgwitness-session`) | **File** | Non è richiesta alcuna coppia API separata |
| Un codice `.json` associato a una sessione o a una chiave di autenticazione | **File** | Non è richiesta alcuna coppia API separata |
| Una chiave di autenticazione (512 caratteri esadecimali) e il relativo numero DC | **Chiave di autenticazione** | ID utente facoltativo |

TgWitness riconosce i file in base al loro **contenuto**, non al loro nome. La ridenominazione di un file non ne comporta mai la conversione.

## Prima di iniziare: ID API e hash API

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

Per utilizzare invece la propria applicazione (l’account che la registra è quello a rischio; si veda [«Perché un pool di API integrato?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)»):

1. Apra [my.telegram.org](https://my.telegram.org) ed effettui l’accesso con un numero di telefono qualsiasi di cui sia titolare. Il codice verrà inviato nell’app di Telegram, non tramite SMS.
2. Scegliete **gli strumenti di sviluppo API**.
3. Creare un’applicazione: titolo a scelta e nome abbreviato (5–32 lettere), piattaforma **Desktop**. L’URL e la descrizione possono essere lasciati vuoti.
4. Copiate **l’api_id dell’app** (un numero) e **l’api_hash dell’app** (32 caratteri esadecimali).

Nel pannello, sotto il modulo di accesso, sono presenti i campi **«ID API» e «Hash**». È possibile incollare una singola coppia `api_id:api_hash` nel campo **«ID API»** e entrambi i campi verranno compilati automaticamente. Una sola coppia può essere utilizzata per tutti i Suoi account. Dopo un accesso riuscito, i dati vengono salvati, crittografati, esclusivamente in quell’area di lavoro e non vengono mai rinviati al browser.

Sono coinvolte tre diverse credenziali:

| Segreto | Si apre | Dove si trova |
| --- | --- | --- |
| Token del pannello | Il pannello web di TgWitness | `panel-token.txt` nella directory dei dati, oppure `TGWITNESS_TOKEN` |
| ID API + hash | Nulla di specifico; identifica l’app | Accoppiamento integrato, impostazioni importate o la propria app su my.telegram.org |
| Autorizzazione dell’account | L’account Telegram | Creato tramite accesso tramite telefono/codice QR o importato come sessione |

Se è necessario accedere a Telegram tramite un proxy, configurarlo innanzitutto in **Account → Impostazioni → Impostazioni di connessione → Modifica percorso di connessione**.

## Numero di telefono

1. Apra **l’account**, selezioni la scheda **«Telefono»** e inserisca il numero in formato internazionale, ad esempio `+44 7700 900123`. Gli spazi e i trattini vengono rimossi automaticamente.
2. Clicchi su **«Continua**». I campi «ID API» e «Hash» possono essere lasciati vuoti.
3. Inserisca il codice inviato da Telegram (di norma all’app di Telegram; la ricezione tramite SMS non è garantita).
4. Se l’account dispone della verifica in due passaggi, inserisca tale password. Non si tratta del token del pannello né del codice di accesso del dispositivo.
5. Verifichi l’ID dell’account visualizzato dopo aver effettuato l’accesso, quindi selezioni le fonti.

I codici di accesso e la password 2FA non vengono mai salvati su disco.

## Codice QR

Utilizzi questa opzione quando l’account è già connesso su uno smartphone o su un altro computer.

1. Scheda **«Codice QR»** → **Mostra codice QR**. I campi «ID API» e «Hash» possono rimanere vuoti.
2. Sul dispositivo su cui si è effettuato l’accesso: **Impostazioni → Dispositivi → Collega dispositivo desktop**, scansionare il codice e confermare.
3. Inserisca la password 2FA in TgWitness qualora Telegram la richieda.

L’immagine QR viene generata localmente. I codici scadono; prema **«Genera un altro codice QR»** per riprovare. Il blocco del pannello, il cambio di area di lavoro o l’avvio di un’altra sessione di accesso annullano un codice in sospeso.

## Chiave di autenticazione + ID DC

Una chiave di autorizzazione (Auth Key) è l’autorizzazione grezza di 256 byte alla base di ogni sessione di Telegram, rappresentata da **512 caratteri esadecimali**, insieme al numero del data center **DC 1–5**.

1. Scheda **«Chiave di autenticazione**». Incolli la chiave completa; una chiave abbreviata contenente «`…`» non è valida.
2. Selezioni l’ID DC fornito insieme alla chiave.
3. È possibile inserire l’**ID utente**. In tal caso, TgWitness rifiuterà la connessione qualora Telegram segnalasse un account diverso.
4. **Account** Press **Connect**.

Una chiave di autenticazione (512 caratteri) non è un hash API (32 caratteri). La stessa chiave può anche essere importata in formato JSON; si veda [Account JSON](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#account-json).

## File degli account

Aprire **«Aggiungi account» → «File»** e selezionare fino a **quattro file appartenenti a un unico account**, per un totale di **8 MiB**, quindi premere **«Collega account**».

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- I file vengono convertiti **in memoria** sul vostro server TgWitness. I file caricati non vengono archiviati, i file ZIP non vengono estratti su disco e non viene effettuato alcun collegamento con servizi esterni.
- La sessione risultante viene quindi verificata con Telegram. Se un file riporta un ID utente, esso deve corrispondere all’account segnalato da Telegram.
- I file che descrivono account diversi o credenziali API diverse vengono respinti anziché selezionarne uno solo.
- Il campo **«Codice di accesso o testo di sessione»** contiene il campo «Codice di accesso locale TData», un campo in cui incollare una StringSession e **leggere i file senza effettuare l’accesso** (compila il modulo senza contattare Telegram).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

### Telethon `.session`

|  |  |
| --- | --- |
| Di cosa si tratta | Il database SQLite creato dagli strumenti basati su Telethon, ad esempio `my_account.session` |
| Riconoscuto da | Tabelle `sessions` (insieme a `dc_id`, `server_address`, `port`, `auth_key`) e `version` = 7 o 8 |
| Requisiti | Esattamente una riga relativa a una sessione autorizzata; un database chiuso e completo |

Chiuda innanzitutto il programma che ha creato il file. Se accanto ad esso è presente `my_account.session-journal` o `my_account.session-wal`, il database non è stato completato: apra e chiuda correttamente il client originale. L’eliminazione di tali file sidecar può lasciare una copia danneggiata.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Di cosa si tratta | Gli strumenti basati su Pyrogram creano un database SQLite |
| Riconoscuto da | Tabella `sessions` con `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 o 3 |
| Requisiti | È consentita una sola sessione **utente** autorizzata sulla rete di produzione. Le sessioni relative ai bot e ai DC di prova vengono respinte |

L’ID utente memorizzato viene verificato su Telegram al momento dell’accesso.

### Coppia sessione + JSON

Gli account vengono spesso distribuiti sotto forma di due file con lo stesso nome, ad esempio `447700900123.session` e `447700900123.json`. Selezionateli **entrambi** contemporaneamente.

- Dal file JSON, TgWitness utilizza `app_id`/`api_id` e `app_hash`/`api_hash`, pertanto di norma non è necessario inserire le credenziali API.
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData è la cartella `tdata` dell’applicazione Telegram Desktop (l’app multipiattaforma disponibile su desktop.telegram.org).

| Sistema | Posizione predefinita `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portatile: accanto a `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Per importarlo:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> Ciò vale anche per i file `.session` importati, il testo di StringSession e l’Auth Key HEX. Gli altri client con autorizzazioni create in modo indipendente possono rimanere connessi. Si veda [la documentazione di Telegram relativa a AUTH_KEY_DUPLICATED](https://core.telegram.org/api/errors#406-not-acceptable).

1. Chiudere completamente Telegram Desktop.
2. Si crei un file ZIP contenente **esclusivamente** questi due elementi provenienti da `tdata`:

   - `key_datas`
   - il file di 16 caratteri che termina con «`s`» accanto ad esso, solitamente «`D877F783D5D3EF8Cs`»

   La compressione dell’intera cartella con la relativa cache multimediale supera solitamente i limiti (512 voci, 32 MiB decompressi). 3. Selezionare il file ZIP in **«File**». Se Telegram Desktop dispone di un **codice di accesso locale**, inserirlo prima nel campo **«Codice di accesso» o nel testo della sessione**. Non si tratta della password 2FA.

Supportato: un account per archivio, archiviazione moderna `key_datas`/`key_data0`/`key_data1`, codice di accesso locale. Non supportato: cartelle con più account connessi, versioni precedenti dell’applicazione Desktop, file ZIP protetti da password e l’app nativa separata per macOS «Telegram per macOS».

### Telethon StringSession

Una singola riga di testo, che solitamente inizia con `1` e contiene circa 350 caratteri. Caricatela come file `.txt` o `.tgwitness-session` (al massimo 4 KiB), oppure incollatela nella sezione **«Codice di accesso» o «Testo della sessione**». Sono accettate solo stringhe Telethon; le stringhe Pyrogram e TDLib utilizzano formati diversi.

### Account JSON

Un oggetto JSON, di dimensioni massime pari a **64 KiB**, contenuto in un file con estensione **`.json`**.

| Campo (alias) | Significato |
| --- | --- |
| `api_id` (`app_id`) | ID dell’applicazione, un numero positivo |
| `api_hash` (`app_hash`) | Hash dell’applicazione, 32 caratteri esadecimali |
| `string_session` (`session_string`, `session_str`; legacy `session`) | Testo di Telethon StringSession, non un nome di file |
| `auth_key` (`auth_key_hex`) + `dc_id` | Chiave di autenticazione completa di 512 caratteri e DC 1–5 |
| `user_id` (`id`) | Opzionale; verifica effettuata su Telegram prima che l’autorizzazione venga salvata |
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

Il primo esempio si limita a inserire le credenziali API; è possibile effettuare l’accesso tramite telefono o codice QR, oppure aggiungere un file di sessione. Non sono accettati elenchi in blocco (un array JSON di account).

## Identifichi ciò di cui dispone

| Come potete vedere | Si tratta di | Utilizzo |
| --- | --- | --- |
| `*.session`; aprendolo in un editor di testo, in alto compare `SQLite format 3` | Telethon o Pyrogram SQLite | **File** (rilevati automaticamente) |
| Una cartella denominata «`tdata`» contenente «`key_datas`» | Telegram Desktop TData | Comprimere i due file in formato ZIP, quindi **«File»** |
| Una riga di testo che inizia con `1`, circa 350 caratteri | Telethon StringSession | **File** |
| `*.json` con `app_id`/`app_hash` | Metadati correlati | **File**, insieme alla relativa sessione |
| `*.json` con `auth_key` o `string_session` | Account JSON | **File** |
| 512 caratteri `0-9a-f` | Chiave di autenticazione | **Chiave di autenticazione** |
| 32 caratteri `0-9a-f` | Hash dell’API | **ID API + Hash** |
| `td.binlog` o `db.sqlite` proveniente da un’applicazione TDLib | Archiviazione TDLib | Non supportato |
| `123456789:AA…` | Token del bot | Non supportato |

## Formati non supportati

| Formato | Alternativa |
| --- | --- |
| Archiviazione TDLib (`td.binlog`) ed esportazioni TDLib | Acceda tramite telefono o codice QR |
| **Stringhe** di sessione di Pyrogram | Utilizzi il file Pyrogram `.session`, oppure il codice QR o il numero di telefono |
| TData con diversi account connessi | Effettuate il logout dagli altri account in Telegram Desktop oppure utilizzate il file di sessione specifico di ciascun account |
| Token dei bot | Non supportato: TgWitness opera in qualità di account utente |
| Elenchi in formato CSV/JSON di numerosi account | Importa i file di sessione supportati tramite **Account → Importazione degli account**, oppure accedi tramite telefono/QR in spazi di lavoro separati |
| Sessioni di Test-DC o con bot | Si prega di utilizzare un account utente di produzione |

## Account multipli

Premere **+** accanto al selettore dell’account, oppure aprire **Account → Impostazioni → Impostazioni di connessione → Ambienti di lavoro**, inserire un’etichetta e effettuare l’accesso.

- È possibile creare un numero illimitato di aree di lavoro, compresa quella principale. Ciascuna dispone di una propria sessione, percorso proxy, fonti, criteri di acquisizione, registro, chiave di firma, punti di controllo ed esportazioni.
- Il cambio dell’area di lavoro visualizzata non mette in pausa le altre.
- Un registro rimane associato all’account che lo ha creato. L’accesso con un account diverso richiede un altro spazio di lavoro, e un singolo account non può essere assegnato a due spazi di lavoro.
- Il token del pannello principale controlla tutte le aree di lavoro. [L’accesso concesso](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/) può limitare l’accesso di altre persone ad account e chat selezionati, con autorizzazioni distinte e limiti di sessione.
- **La voce «Accounts»** rinomina un’area di lavoro ed elimina quella aggiunta, insieme alla relativa sessione, al registro, alle fonti e alla chiave di firma. L’area di lavoro principale non può essere eliminata dal pannello.

### Importazione in blocco e gruppi di account

Utilizza **Account → Importa account** per aggiungere più account, abbinare i file in base al nome base e visualizzare il risultato di ogni accesso. Ogni account dispone di un proprio spazio di lavoro.

Un gruppo raggruppa account correlati senza unire le loro sessioni, le chiavi o le prove. **Il gruppo «Open group** on **Accounts»** rimanda alla relativa pagina all’indirizzo `/groups/<id>`:

- **Account:** percorso di connessione, osservazioni e ultimo messaggio di ciascun membro, con "Avvia**tutto"** e **"Metti in pausa tutto**".
- **Richiede attenzione:** account dai quali si è effettuato il logout, che non sono disponibili o che presentano un problema di connessione, acquisizione, fonte o file multimediale; ogni nome rimanda alla relativa scheda.
- **Le chat di più account mostrano:** le fonti condivise, gli account che le osservano e le interruzioni nel periodo di osservazione dello spazio di lavoro disponibile (fino a sette giorni). **L’esportazione con N account** suddivide l’esportazione di un canale o di un supergruppo tra di essi e firma un unico archivio.
- **Esporta gruppo:** un'ZIP contenente l'esportazione firmata di ciascun account sotto `accounts/` e `manifest.json` elencando le impronte digitali dei SHA-256 e delle chiavi, firmate dall’ spazio di lavoro principale in `manifest.signature.json`. Verifica separatamente l’archivio di ciascun account con `python -m tgwitness.verify` e l’impronta digitale attendibile di quell’account.

I membri condividono le impostazioni del gruppo; un account può mantenere i propri valori. Vedi [le impostazioni condivise](https://phishdestroy.github.io/TgWitness/it/docs/reference/settings/#account-groups), [la guida all’importazione e ai gruppi](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) e [la dashboard del pool MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Esci

**Account → Esci da Telegram** (con il monitoraggio in pausa) richiede a Telegram di terminare la sessione, che quindi scompare anche dalla sezione **Impostazioni → Dispositivi** dell’account e viene rimossa dal vault dell’area di lavoro. Il registro, le fonti, le impostazioni e la chiave di firma rimangono, e il registro registra l’uscita. L’area di lavoro appartiene ancora al proprio account: solo quell’ account potrà riconnettersi ad essa. Se Telegram non risponde, la sessione viene comunque rimossa qui e il pannello lo segnala; la si può terminare in Telegram alla voce **Impostazioni → Dispositivi**.

## Garantire la sicurezza dei file degli account

- Trattate ogni `.session`, TData ZIP, StringSession, chiave di autenticazione e file JSON dell’account come una password. TgWitness conserva le autorizzazioni importate nel proprio archivio crittografato; potrete eliminare i file originali in un secondo momento.
- Non esegua la stessa autorizzazione in due programmi contemporaneamente. Telegram potrebbe revocarla (`AUTH_KEY_DUPLICATED`) e entrambe le copie smetterebbero di funzionare.
- Una sessione scaduta o revocata non può essere ripristinata tramite conversione. Effettate nuovamente l’accesso.

## Risoluzione dei problemi

| Messaggio o sintomo | Cosa fare |
| --- | --- |
| *Impossibile leggere questa sessione. Chiuda il client originale…* | Il file SQLite è aperto o non completato (sidecar `-journal`/`-wal`). Chiuda correttamente il programma originale e copi nuovamente il file. |
| *Schemi SQLite di Telethon supportati: 7 e 8* / *Pyrogram … 2 e 3* | Il file è stato creato da una versione della libreria molto vecchia o sconosciuta. Effettui invece l’accesso tramite telefono/codice QR. |
| *Sono supportate esclusivamente le sessioni utente autorizzate in ambiente di produzione* | Il file Pyrogram appartiene a un bot o alla rete di test. |
| *L’archivio TData supera le 512 voci o i 32 MiB* | Solo i file ZIP `key_datas` e `D877F783D5D3EF8Cs`, non l’intera cartella. |
| *Impossibile decriptare TData. Verifichi il codice di accesso locale del Desktop* | Inserisca il codice di accesso locale di Telegram Desktop nel campo **«Codice di accesso» o «Testo della sessione**». |
| *Importare un account TData alla volta* | Telegram Desktop disponeva di diversi account; si veda la sezione [«Formati non supportati](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#unsupported-formats)». |
| *I file selezionati descrivono diversi account o credenziali API* | Selezionare i file relativi a un solo account. |
| *Il file JSON non contiene credenziali API o autorizzazioni supportate* | Verifichi i nomi dei campi nel file [JSON dell’account](https://phishdestroy.github.io/TgWitness/it/docs/reference/accounts/#account-json). |
| *Solo metadati API* | Il file JSON non contiene alcuna sessione. Si prega di aggiungere il file `.session` oppure di utilizzare il numero di telefono o il codice QR. |
| *La chiave di autenticazione HEX deve contenere tutti i 512 caratteri esadecimali* | La chiave è troncata o contiene «`…`». |
| L'ID dell'account non corrisponde a quello dell'account importato | L’ID utente del file differisce da quello riportato da Telegram; il file si riferisce a un altro account. |
| L'account appartiene già a un altro spazio di lavoro | Si apra quell’area di lavoro anziché aggiungere l’account due volte. |
| Collegato, ma nella lista delle chat alla voce **«Fonti»** manca un gruppo privato | Verificare l’iscrizione. Il selettore esamina le prime 1.000 conversazioni; aumentare il limite nella sezione **«Parametri**». |
| Connessione proxy non riuscita | Controlla la modalità di instradamento e quella IP. La modalità automatica MTProxy prova un altro accesso funzionante. La modalità "Nascondi l'indirizzo" attende; la modalità "Diretta", come ultima risorsa, può connettersi direttamente dopo il ritardo configurato. Vedi [le modalità di instradamento](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/#ip-modes). |

Si veda anche: [connessione e sicurezza](https://phishdestroy.github.io/TgWitness/it/docs/reference/connection/) per i proxy e la crittografia, e [come funziona la raccolta](https://phishdestroy.github.io/TgWitness/it/docs/reference/collection/) dei dati acquisiti dopo l’accesso.
