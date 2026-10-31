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

Puede iniciar sesión sin necesidad de crear una aplicación de la API de Telegram. Cuando no se introduce ningún par, ni se importa ni está ya guardado en el espacio de trabajo, TgWitness selecciona un par de su conjunto integrado de 50 pares de API públicos (`tgwitness/api_pool.py`) en orden aleatorio. Si Telegram rechaza un par (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), se prueba el siguiente, hasta un máximo de ocho por sesión de inicio de sesión; los pares rechazados se omiten hasta que se reinicie el sistema. El par con el que se ha iniciado sesión se guarda con la cuenta y se reutiliza para ella. Un **ID de API** y **un hash de API** identifican la aplicación ante Telegram; estos no autorizan una cuenta por sí mismos.

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

- Los archivos se convierten **en memoria** en su servidor de TgWitness. Las subidas no se almacenan, los archivos ZIP no se extraen al disco y no se establece contacto con ningún servicio externo.
- A continuación, la sesión resultante se comprueba con Telegram. Si un archivo indica un ID de usuario, debe coincidir con la cuenta que Telegram indica.
- Se rechazan los archivos que describen diferentes cuentas o diferentes credenciales de API en lugar de seleccionar una sola.
- El campo **«Código de acceso o texto de sesión»** contiene el campo de código de acceso local de TData, un cuadro en el que se puede pegar una StringSession y **leer archivos sin iniciar sesión** (se rellena el formulario sin conectarse a Telegram).

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
- Se **ignoran** otros campos como `phone`, `device`, `sdk`, `app_version`, `lang_pack` o una contraseña `twoFA` almacenada. Si la cuenta dispone de autenticación de dos factores (2FA), TgWitness la solicita.
- Un archivo JSON por sí solo no es más que metadatos. Sin el archivo de sesión, continúe con el inicio de sesión mediante teléfono o código QR.

### Telegram Desktop (TData)

TData es la carpeta «`tdata`» de la aplicación Telegram Desktop (la aplicación multiplataforma de desktop.telegram.org).

| Sistema | Ubicación predeterminada: `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portátil: junto a `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Para importarlo:

> **Advertencia sobre sesiones paralelas.** Al importar TData se reutiliza la clave de autorización de Telegram Desktop; no se crea un inicio de sesión independiente. No utilice esa clave en Desktop y TgWitness simultáneamente. Telegram puede invalidar la autorización con `AUTH_KEY_DUPLICATED`, dejando ambas copias inutilizables hasta que se realice un nuevo inicio de sesión.
>
>
>
> Cierre completamente Desktop, incluido su proceso en la bandeja del sistema, y mantenga esa copia cerrada mientras TgWitness utiliza la sesión importada. **Cierre la aplicación; no cierre la sesión ni revoque la sesión:** la revocación también invalida la copia importada. Si necesita tener ambos clientes en ejecución, inicie sesión en TgWitness mediante el teléfono o un código QR para crear su propia autorización. Se recomienda utilizar una cuenta dedicada, aunque esto no garantiza que las claves clonadas sean seguras para su uso en paralelo.
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
| `string_session` (`session_string`, `session`) | Texto de «StringSession» de Telethon, no es un nombre de archivo |
| `auth_key` (`auth_key_hex`) + `dc_id` | Clave de autenticación completa de 512 caracteres y DC 1–5 |
| `user_id` (`id`) | Opcional; se comprueba con Telegram antes de guardar la autorización. |

Si figuran tanto un alias como el nombre principal, ambos deben coincidir. Ejemplos:

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

Usa **Cuentas → Importar cuentas** para añadir varias cuentas, emparejar archivos por nombre y ver el resultado de cada inicio de sesión. Cada cuenta tiene su propio espacio de trabajo. Los grupos pueden copiar ajustes seleccionados de una plantilla sin combinar sesiones, claves ni pruebas. Consulta [la guía de importación y grupos](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) y [el panel del conjunto MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Cerrar sesión

**Cuenta → Cerrar sesión en Telegram** (con la observación en pausa) solicita a Telegram que finalice la sesión, por lo que también desaparece de **Ajustes → Dispositivos** de la cuenta y elimina la sesión del almacén del espacio de trabajo. El registro, las fuentes, los ajustes y la clave de firma permanecen, y el registro recoge el cierre de sesión. El espacio de trabajo sigue perteneciendo a su cuenta: solo esa cuenta puede volver a conectarse a él. Si Telegram no responde, la sesión se elimina igualmente aquí y el panel lo indica; finalícela en Telegram en **Ajustes → Dispositivos**.

## Convertir una sesión de Telethon sin conexión

El panel importa directamente archivos `.session`. Para realizar una conversión sin conexión a un archivo StringSession, ejecute desde la carpeta del proyecto:

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

El conversor solo lee archivos SQLite de Telethon (hasta 64 MiB), nunca modifica los datos de entrada, no realiza ninguna solicitud de red y se niega a sobrescribir un archivo de salida ya existente.

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
| Error en la conexión mediante proxy | Compruebe la ruta y el modo de IP. El modo automático de MTProxy prueba otra entrada válida. El modo «Ocultar IP» espera; el modo de reserva seleccionado explícitamente puede conectarse directamente tras el retraso configurado. Consulte [los modos de enrutamiento](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/#ip-modes). |

Véase también: [conexión y seguridad](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/) para proxies y cifrado, y [cómo funciona la recopilación](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/) de los datos capturados tras iniciar sesión.
