# Formatos de cuentas y sesiones

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/

Inicie sesión mediante teléfono, código QR o clave de autenticación, importe sesiones de Telethon, Pyrogram o Telegram Desktop, y gestione varias cuentas.

TgWitness inicia sesión como una **cuenta de usuario de Telegram** (no como un bot) a través de MTProto, utilizando Telethon. Cada cuenta se encuentra en su propio **espacio de trabajo** (denominado *«workspace*» en la API y en las herramientas de línea de comandos) con su propia sesión, fuentes, registro y clave de firma.

Los archivos de sesión, las cadenas de sesión y las claves de autenticación son **autorizaciones de cuenta**: quienquiera que las posea puede actuar en nombre de dicha cuenta. No contienen el historial de mensajes.

> [!ADVERTENCIA] **No utilice nada que no pueda permitirse perder.** Le recomendamos encarecidamente que no conecte cuentas personales o de otro tipo que sean valiosas, ni que cree un ID de API o un hash de API en una cuenta que considere importante. No se trata de que TgWitness no haya sido probado: Telegram restringe y bloquea de forma permanente cuentas de manera impredecible —por volúmenes de solicitudes que considera excesivos—, independientemente del cliente o la finalidad, y sin documentación adecuada. Muchos bloqueos son irreversibles. Utilice cuentas específicas para este fin. El buen funcionamiento de las pruebas depende de Telegram, no del software, y no garantiza nada para el futuro.

- [De un vistazo](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#at-a-glance)
- [Antes de empezar: ID de la API y hash de la API](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Número de teléfono](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#phone-number) · [Código QR](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#qr-code) · [Clave de autenticación + ID de DC](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#auth-key--dc-id)
- [Archivos de cuentas](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#pyrogram-session) · [Par «sesión + JSON»](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#telethon-stringsession) · [Fichero JSON de la cuenta](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#account-json)
- [Identifique lo que tiene](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#identify-what-you-have) · [Formatos no compatibles](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#unsupported-formats)
- [Cuentas múltiples](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#multiple-accounts) · [Mantener a salvo los archivos de las cuentas](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#keeping-account-files-safe) · [Solución de problemas](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#troubleshooting)

## De un vistazo

| Lo que tiene | Pestaña **«Añadir cuenta»** | También necesitará |
| --- | --- | --- |
| El número de teléfono y el acceso a sus códigos de inicio de sesión | **Teléfono** | Contraseña de 2FA, si está activada |
| Telegram abierto en otro dispositivo | **Código QR** | Contraseña de 2FA, si está activada |
| Un archivo `.session` (Telethon o Pyrogram) | **Archivos** | Archivo JSON complementario opcional para la configuración de la aplicación |
| `.session` + `.json` con el mismo nombre | **Archivos** (seleccione ambos) | Por lo general, nada más |
| Una carpeta «`tdata`» en Telegram Desktop | **Archivos** (en formato ZIP) | El código de acceso local de la versión de escritorio, en caso de que se haya configurado uno |
| Una sesión de cadenas de Telethon (texto, `.txt`, `.tgwitness-session`) | **Archivos** | No se requiere un par de API independiente |
| Un `.json` con una sesión o una clave de autenticación | **Archivos** | No se requiere un par de API independiente |
| Una clave de autenticación (512 caracteres hexadecimales) y su número DC | **Clave de autenticación** | ID de usuario opcional |

TgWitness reconoce los archivos por su **contenido**, no por su nombre. Al cambiar el nombre de un archivo, este nunca se convierte.

## Antes de empezar: ID de la API y hash de la API

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

Para utilizar en su lugar su propia aplicación (la cuenta que la registre es la que corre riesgo; véase [«¿Por qué un conjunto de API integrado?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)»):

1. Abra [my.telegram.org](https://my.telegram.org) e inicie sesión con cualquier número de teléfono del que disponga. El código le llegará a la aplicación de Telegram, no por SMS.
2. Seleccione **herramientas de desarrollo de API**.
3. Cree una aplicación: cualquier título y nombre abreviado (de 5 a 32 letras), plataforma: **ordenador de sobremesa**. La URL y la descripción pueden dejarse en blanco.
4. Copie **el «api_id» de la aplicación** (un número) y **el «api_hash» de la aplicación** (32 caracteres hexadecimales).

En el panel, **«API ID + Hash»** aparece debajo del formulario de inicio de sesión. Puede pegar un único par `api_id:api_hash` en **el campo «API ID»** y ambos campos se rellenarán automáticamente. Un mismo par puede utilizarse para todas sus cuentas. Tras iniciar sesión con éxito, se guarda, cifrado, únicamente en ese espacio de trabajo y nunca se reenvía al navegador.

Intervienen tres tipos de credenciales diferentes:

| Secreto | Abrir | Dónde se encuentra |
| --- | --- | --- |
| Token de panel | El panel web de TgWitness | `panel-token.txt` en el directorio de datos, o `TGWITNESS_TOKEN` |
| ID de la API + hash | No aporta nada por sí solo; identifica la aplicación | Emparejamiento integrado, configuración importada o su propia aplicación en my.telegram.org |
| Autorización de la cuenta | La cuenta de Telegram | Se crea mediante inicio de sesión por teléfono o código QR, o bien se importa como una sesión. |

Si es necesario acceder a Telegram a través de un proxy, configúrelo primero en **Cuenta → Ajustes → Ajustes de conexión → Cambiar ruta de conexión**.

## Número de teléfono

1. Abra **la cuenta**, vaya a la pestaña **«Teléfono**» e introduzca el número en formato internacional, por ejemplo, `+44 7700 900123`. Los espacios y los guiones se eliminan automáticamente.
2. Pulse **«Continuar**». Los campos «API ID» y «Hash» pueden dejarse en blanco.
3. Introduzca el código que envía Telegram (normalmente a la aplicación de Telegram; no se garantiza su recepción por SMS).
4. Si la cuenta dispone de verificación en dos pasos, introduzca esa contraseña. No se trata del token del panel ni del código de acceso del dispositivo.
5. Compruebe el ID de la cuenta que aparece tras iniciar sesión y, a continuación, seleccione las fuentes.

Los códigos de inicio de sesión y la contraseña de autenticación de dos factores (2FA) nunca se guardan en el disco.

## Código QR

Utilice esta opción cuando la cuenta ya haya iniciado sesión en un teléfono u otro ordenador.

1. Pestaña **«Código QR»** → **Mostrar código QR**. Los campos «ID de API» y «Hash» pueden dejarse en blanco.
2. En el dispositivo en el que ha iniciado sesión: **Ajustes → Dispositivos → Vincular dispositivo de escritorio**, escanee el código y confirme.
3. Introduzca la contraseña de 2FA en TgWitness si Telegram se la solicita.

La imagen del código QR se genera localmente. Los códigos caducan; pulse **«Generar otro código QR»** para volver a intentarlo. Al bloquear el panel, cambiar de espacio de trabajo o iniciar otro inicio de sesión se cancela un código pendiente.

## Clave de autenticación + ID de DC

Una clave de autorización (Auth Key) es la autorización sin procesar de 256 bytes que subyace a cada sesión de Telegram, escrita como **512 caracteres hexadecimales**, junto con el número del centro de datos **DC 1–5**.

1. Pestaña **«Clave de autenticación**». Pegue la clave completa; una clave abreviada que contenga «`…`» no funcionará.
2. Seleccione el DC ID proporcionado junto con la clave.
3. Si lo desea, introduzca el **ID de usuario**. En ese caso, TgWitness rechazará la conexión si Telegram detecta una cuenta diferente.
4. **Cuenta de** Press **Connect**.

Una clave de autenticación (512 caracteres) no es un hash de API (32 caracteres). La misma clave también puede importarse como JSON; consulte [«JSON de la cuenta](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#account-json)».

## Archivos de cuentas

Abra **«Añadir cuenta» → «Archivos»** y seleccione hasta **cuatro archivos pertenecientes a una misma cuenta**, con un tamaño total de **8 MiB**; a continuación, pulse **«Conectar cuenta**».

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- Los archivos se convierten **en memoria** en su servidor de TgWitness. Las subidas no se almacenan, los archivos ZIP no se extraen al disco y no se establece contacto con ningún servicio externo.
- A continuación, la sesión resultante se comprueba con Telegram. Si un archivo indica un ID de usuario, debe coincidir con la cuenta que Telegram indica.
- Se rechazan los archivos que describen diferentes cuentas o diferentes credenciales de API en lugar de seleccionar una sola.
- El campo **«Código de acceso o texto de sesión»** contiene el campo de código de acceso local de TData, un cuadro en el que se puede pegar una StringSession y **leer archivos sin iniciar sesión** (se rellena el formulario sin conectarse a Telegram).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

### Telethon `.session`

|  |  |
| --- | --- |
| En qué consiste | La base de datos SQLite que crean las herramientas basadas en Telethon, por ejemplo, `my_account.session` |
| Reconocida por | Tablas `sessions` (junto con `dc_id`, `server_address`, `port`, `auth_key`) y `version` = 7 u 8 |
| Requisitos | Exactamente una fila de sesión autorizada; una base de datos cerrada y completa. |

Cierre primero el programa que creó el archivo. Si `my_account.session-journal` o `my_account.session-wal` aparecen junto a él, la base de datos no está finalizada: abra y cierre el cliente original correctamente. La eliminación de esos archivos «sidecar» puede dejar una copia dañada.

### Pyrogram `.session`

|  |  |
| --- | --- |
| En qué consiste | Las herramientas basadas en Pyrogram crean una base de datos SQLite |
| Reconocida por | Tabla `sessions` con `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 o 3 |
| Requisitos | Una sesión **de usuario** autorizada en la red de producción. Se rechazan las sesiones de bots y de centros de datos de prueba. |

El identificador de usuario almacenado se compara con el de Telegram durante el inicio de sesión.

### Par «sesión + JSON»

Las cuentas suelen distribuirse en dos archivos con el mismo nombre, por ejemplo, « `447700900123.session`» y «`447700900123.json`». Seleccione **ambos** a la vez.

- A partir del JSON, TgWitness utiliza `app_id`/`api_id` y `app_hash`/`api_hash`, por lo que normalmente no es necesario introducir credenciales de la API.
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData es la carpeta «`tdata`» de la aplicación Telegram Desktop (la aplicación multiplataforma de desktop.telegram.org).

| Sistema | Ubicación predeterminada: `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portátil: junto a `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Para importarlo:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> Esto también se aplica a los `.session` , al texto de StringSession y a la clave de autenticación en formato HEX. Otros clientes con sus propias autorizaciones creadas de forma independiente pueden permanecer conectados. Consulte [la documentación de Telegram sobre AUTH_KEY_DUPLICATED](https://core.telegram.org/api/errors#406-not-acceptable).

1. Cierre completamente Telegram Desktop.
2. Cree un archivo ZIP que contenga **únicamente** estos dos elementos de `tdata`:

   - `key_datas`
   - el archivo de 16 caracteres que termina en «`s`» situado junto a él, normalmente «`D877F783D5D3EF8Cs`»

   Al comprimir toda la carpeta con su caché multimedia, se suelen superar los límites (512 entradas, 32 MiB descomprimidos). 3. Seleccione el archivo ZIP en **«Archivos**». Si Telegram Desktop tiene un **código de acceso local**, introdúzcalo primero en el campo **«Código de acceso» o «Texto de sesión**». No se trata de la contraseña de la autenticación de dos factores (2FA).

Compatible con: una cuenta por archivo, almacenamiento moderno `key_datas`/`key_data0`/`key_data1`, código de acceso local. No compatible con: carpetas con varias cuentas conectadas, diseños antiguos de la versión de escritorio, archivos ZIP protegidos con contraseña y la aplicación nativa independiente de macOS «Telegram para macOS».

### Telethon StringSession

Una sola línea de texto, que suele comenzar por «`1`» y tiene una longitud aproximada de 350 caracteres. Cárguela como un archivo «`.txt`» o «`.tgwitness-session`» (de un máximo de 4 KiB), o pégela en el campo **«Código de acceso» o «Texto de sesión**». Solo se aceptan cadenas de Telethon; las cadenas de Pyrogram y TDLib utilizan formatos diferentes.

### Fichero JSON de la cuenta

Un objeto JSON, de un máximo de **64 KiB**, en un archivo con extensión «**`.json`**».

| Campo (alias) | Significado |
| --- | --- |
| `api_id` (`app_id`) | ID de la aplicación, un número positivo |
| `api_hash` (`app_hash`) | Hash de la aplicación, 32 caracteres hexadecimales |
| `string_session` (`session_string`, `session_str`; legacy `session`) | Texto de «StringSession» de Telethon, no es un nombre de archivo |
| `auth_key` (`auth_key_hex`) + `dc_id` | Clave de autenticación completa de 512 caracteres y DC 1–5 |
| `user_id` (`id`) | Opcional; se comprueba con Telegram antes de guardar la autorización. |
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

En el primer ejemplo solo se rellenan las credenciales de la API; inicie sesión mediante teléfono o código QR, o añada un archivo de sesión. No se aceptan listas masivas (una matriz JSON de cuentas).

## Identifique lo que tiene

| Como puede ver | Se trata de | Uso |
| --- | --- | --- |
| `*.session`; al abrirlo en un editor de texto, aparece `SQLite format 3` en la parte superior | Telethon o Pyrogram SQLite | **Archivos** (detectados automáticamente) |
| Una carpeta «`tdata`» que contiene «`key_datas`» | Telegram Desktop TData | Comprima los dos archivos en un ZIP y, a continuación, **«Archivos»** |
| Una línea de texto que comienza por `1`, ~350 caracteres | Telethon StringSession | **Archivos** |
| `*.json` con `app_id`/`app_hash` | Metadatos complementarios | **Archivos**, junto con su sesión |
| `*.json` con `auth_key` o `string_session` | Fichero JSON de la cuenta | **Archivos** |
| 512 caracteres `0-9a-f` | Clave de autenticación | **Clave de autenticación** |
| 32 caracteres `0-9a-f` | Hash de la API | **ID de la API + Hash** |
| `td.binlog` o un `db.sqlite` procedente de una aplicación de TDLib | Almacenamiento TDLib | No compatible |
| `123456789:AA…` | Token del bot | No compatible |

## Formatos no compatibles

| Formato | Alternativa |
| --- | --- |
| Almacenamiento de TDLib (`td.binlog`) y exportaciones de TDLib | Inicie sesión mediante el teléfono o un código QR |
| **Cadenas** de sesión de Pyrogram | Utilice el archivo Pyrogram `.session`, o el código QR/teléfono |
| TData con varias cuentas registradas | Cierre la sesión en las demás cuentas de Telegram Desktop o utilice el archivo de sesión propio de cada cuenta |
| Tokens de bot | No compatible: TgWitness actúa como una cuenta de usuario |
| Listas en formato CSV/JSON de numerosas cuentas | Importe archivos de sesión compatibles mediante **Cuentas → Importar cuentas**, o inicie sesión por teléfono/QR en espacios de trabajo separados |
| Sesiones de prueba en DC o con bots | Utilice una cuenta de usuario de producción |

## Cuentas múltiples

Pulse **+** junto al selector de cuentas, o bien abra **Cuenta → Ajustes → Ajustes de conexión → Espacios de trabajo**, introduzca una etiqueta y inicie sesión.

- Cualquier número de espacios de trabajo, incluido el principal. Cada uno cuenta con su propia sesión, ruta de proxy, fuentes, política de captura, registro, clave de firma, puntos de control y exportaciones.
- Cambiar el espacio de trabajo que se muestra no detiene los demás.
- Un registro permanece vinculado a la cuenta que lo creó. Para iniciar sesión con una cuenta diferente se requiere otro espacio de trabajo, y una misma cuenta no puede asignarse a dos espacios de trabajo.
- El token del panel principal controla todos los espacios de trabajo. [El acceso concedido](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/) puede limitar el acceso de otras personas a cuentas y chats seleccionados, con permisos y límites de sesión independientes.
- **La función «Cuentas»** cambia el nombre de un espacio de trabajo y elimina uno añadido, junto con su sesión, su registro, sus fuentes y su clave de firma. El espacio de trabajo principal no se puede eliminar desde el panel.

### Importación masiva y grupos de cuentas

Utiliza **Cuentas → Importar cuentas** para añadir varias cuentas, emparejar archivos por nombre base y ver el resultado de cada inicio de sesión. Cada cuenta dispone de su propio espacio de trabajo.

Un grupo agrupa cuentas relacionadas sin fusionar sus sesiones, claves ni pruebas. Al hacer clic en **«Grupo abierto»** en **«Cuentas»** se accede a su página en `/groups/<id>`:

- **Cuentas:** ruta de conexión, observación y último mensaje de cada miembro, con las opciones «Iniciar**todo»** y **«Pausar todo**».
- **Requiere atención:** cuentas en las que se ha cerrado sesión, que no están disponibles o que presentan un problema de conexión, recepción, fuente o multimedia; cada nombre lleva a su ficha.
- **En los chats de varias cuentas se pueden ver:** las fuentes compartidas, las cuentas que las observan y las interrupciones en el periodo de observación del espacio de trabajo disponible (hasta siete días). **La exportación con N cuentas** divide la exportación de un canal o supergrupo entre ellas y firma un único archivo.
- **Exportar grupo:** una imagen ZIP con la exportación firmada de cada cuenta en `accounts/` y `manifest.json` enumerando sus SHA-256 y huellas digitales de las claves, firmadas por el espacio de trabajo principal en `manifest.signature.json`. Verifica cada archivo de cuenta por separado con `python -m tgwitness.verify` y la huella digital de confianza de esa cuenta.

Los miembros comparten la configuración del grupo; cada cuenta puede mantener sus propios valores. Consulta [la configuración compartida](https://phishdestroy.github.io/TgWitness/es/docs/reference/settings/#account-groups), [la guía de importación y grupos](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) y [el panel de control del grupo MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Cerrar sesión

**Cuenta → Cerrar sesión en Telegram** (con la observación en pausa) solicita a Telegram que finalice la sesión, por lo que también desaparece de **Ajustes → Dispositivos** de la cuenta y elimina la sesión del almacén del espacio de trabajo. El registro, las fuentes, los ajustes y la clave de firma permanecen, y el registro recoge el cierre de sesión. El espacio de trabajo sigue perteneciendo a su cuenta: solo esa cuenta puede volver a conectarse a él. Si Telegram no responde, la sesión se elimina igualmente aquí y el panel lo indica; finalícela en Telegram en **Ajustes → Dispositivos**.

## Mantener a salvo los archivos de las cuentas

- Trate cada `.session`, TData ZIP, StringSession, clave de autenticación y JSON de cuenta como si fuera una contraseña. TgWitness guarda la autorización importada en su almacén cifrado; puede eliminar los archivos originales posteriormente.
- No ejecute la misma autorización en dos programas a la vez. Telegram podría revocarla (`AUTH_KEY_DUPLICATED`), y ambas copias dejarían de funcionar.
- Una sesión caducada o revocada no puede reactivarse mediante conversión. Vuelva a iniciar sesión.

## Solución de problemas

| Mensaje o síntoma | Qué hacer |
| --- | --- |
| *No se puede leer esta sesión. Cierre su cliente original…* | El archivo SQLite está abierto o sin terminar (sidecar `-journal`/`-wal`). Cierre correctamente el programa original y vuelva a copiar el archivo. |
| *Esquemas SQLite de Telethon compatibles: 7 y 8* / *Pyrogram … 2 y 3* | El archivo se ha creado con una versión muy antigua o desconocida de la biblioteca. Inicie sesión mediante teléfono o código QR en su lugar. |
| *Solo se admiten sesiones de usuario autorizadas en entorno de producción.* | El archivo Pyrogram pertenece a un bot o a la red de pruebas. |
| *El archivo TData supera las 512 entradas o los 32 MiB* | Solo los archivos ZIP «`key_datas`» y «`D877F783D5D3EF8Cs`», no toda la carpeta. |
| *No se puede descifrar TData. Compruebe el código de acceso local del ordenador de sobremesa.* | Introduzca el código de acceso local de Telegram Desktop en el campo **«Código de acceso» o «Texto de sesión**». |
| *Importe una cuenta de TData cada vez* | Telegram Desktop contaba con varias cuentas; véase [«Formatos no compatibles](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#unsupported-formats)». |
| *Los archivos seleccionados describen diferentes cuentas o credenciales de API.* | Seleccione archivos de una sola cuenta. |
| *El archivo JSON no contiene credenciales ni autorizaciones compatibles con la API.* | Compruebe los nombres de los campos en el archivo [JSON de la cuenta](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#account-json). |
| *Únicamente metadatos de la API* | El archivo JSON no contiene ninguna sesión. Añada el archivo «`.session`» o utilice el teléfono o el código QR. |
| *La clave de autenticación HEX debe contener los 512 caracteres hexadecimales completos* | La clave está truncada o contiene «`…`». |
| El ID de la cuenta no coincide con el de la cuenta importada | El ID de usuario del archivo difiere del que indica Telegram; el archivo corresponde a otra cuenta. |
| La cuenta ya pertenece a otro espacio de trabajo | Abra ese espacio de trabajo en lugar de añadir la cuenta dos veces. |
| Está conectado, pero falta un grupo privado en la lista de chats de **«Fuentes».** | Compruebe la pertenencia al servicio. El selector examina los primeros 1.000 diálogos; aumente el límite en **«Parámetros**». |
| Error en la conexión mediante proxy | Comprueba la ruta y el modo IP. El modo automático MTProxy prueba otra entrada que funcione. La opción «Ocultar la dirección» espera; el modo «Directo», como último recurso, puede conectarse directamente tras el retraso configurado. Consulta [los modos de enrutamiento](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/#ip-modes). |

Véase también: [conexión y seguridad](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/) para proxies y cifrado, y [cómo funciona la recopilación](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/) de los datos capturados tras iniciar sesión.
