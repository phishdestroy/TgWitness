# Formatos de cuentas y sesiones

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/

Inicie sesión mediante teléfono, código QR o clave de autenticación, importe sesiones de Telethon, Pyrogram o Telegram Desktop, y gestione varias cuentas.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentación](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Primeros pasos](https://phishdestroy.github.io/TgWitness/es/docs/reference/quickstart/)

![Primeros pasos](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

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

Puedes iniciar sesión sin crear una aplicación de la API de Telegram. Cuando no se introduce ningún par, ni se importa ni está ya guardado en el espacio de trabajo, TgWitness elige un par de su conjunto integrado de pares de API pública 50 (`tgwitness/api_pool.py`), dando preferencia a Telegram Desktop para un nuevo inicio de sesión y conservando primero un par guardado; los candidatos restantes se barajan. Si Telegram rechaza un par (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), se prueba el siguiente, hasta un máximo de ocho por inicio de sesión; los pares rechazados se omiten hasta el reinicio. El par con el que se ha iniciado sesión se guarda con la cuenta y se reutiliza para ella. Un ID de API **,** y un hash de API **,** identifican la aplicación ante Telegram; estos no autorizan una cuenta por sí mismos.

Los campos de conexión que faltan utilizan un par determinista de dispositivo/sistema operativo de los catálogos [opentele2 2.0.0](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735) incluidos: Ordenador de sobremesa `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834` y Web `2496`. El ID de compilación del código fuente de Android `4` también utiliza el catálogo de Android, tal y como se identifica en [BuildVars de Telegram para Android](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web utiliza A por defecto; un sufijo de versión de aplicación `K` importado o un paquete de idioma `macos` selecciona K, y la versión `0.7.0` selecciona Webogram. Los ID de aplicación desconocidos mantienen los valores predeterminados del servidor de Telethon. Los campos importados siempre tienen prioridad, incluyendo una versión anterior de la aplicación y un paquete de idioma vacío. El catálogo nunca cambia el ID/hash de la API. Su instantánea de versión se revisa explícitamente, no se recupera durante el inicio de sesión. Un perfil guardado permanece estable tras las actualizaciones.

`account.getAuthorizations` informa de los metadatos de autorización guardados por Telegram; no es un reflejo de cada nuevo `initConnection`. Compáralo con el perfil realmente enviado. Conectar una autorización existente no valida su hash de API asociado: `initConnection` envía el ID de la API, mientras que el hash se utiliza en las solicitudes de inicio de sesión.

Tras una nueva autorización mediante teléfono o código QR, TgWitness solicita la configuración, el centro de datos más cercano, el estado de conexión, los idiomas (cuando el paquete de idiomas no está vacío), las actualizaciones de la aplicación y las actualizaciones de las condiciones de servicio, con un intervalo de 0.3–1.5 segundos entre solicitudes. La actualización del estado marca brevemente la cuenta como conectada. Esta secuencia se ejecuta una vez al completar el inicio de sesión, no en importaciones, reconexiones ni reinicios. La autorización se guarda en primer lugar; una solicitud fallida detiene la secuencia sin reintentar ni descartar el inicio de sesión. Los resultados se registran como `account.initialized`, con nombres de error en lugar de cuerpos de respuesta. La secuencia no es una garantía contra las restricciones de la cuenta.

Para `tdesktop` , si falta `tz_offset` , se utiliza la diferencia horaria local del servidor con respecto al UTC, redondeada a 900 segundos mediante el algoritmo [opentele2](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; licencia en `tgwitness/client_profiles.LICENSE` ). Se actualiza en cada conexión para que se reflejen los cambios por el horario de verano. Un `tz_offset` importado tiene prioridad en todas las plataformas y se conserva exactamente, incluido el cero. Se conservan las demás entradas `initConnection.params` . El formulario de inicio de sesión HTTP acepta la zona horaria numérica devuelta por la importación de archivos; se rechazan los valores booleanos, las fracciones y las diferencias horarias fuera del rango admitido.

Las rutas directas, SOCKS5 y HTTP CONNECT utilizan el `ConnectionTcpObfuscated` de Telethon (MTProto abreviado y ofuscado). HTTPS CONNECT mantiene el TLS hasta el proxy y utiliza el mismo transporte ofuscado dentro del túnel. MTProxy mantiene su transporte intermedio aleatorio obligatorio y la gestión de secretos. Los cambios de ruta aplican las mismas opciones. La ofuscación modifica la estructura de los paquetes; no oculta la cuenta ni los metadatos de su cliente a Telegram, ni implica inmunidad frente a las restricciones.

Tras conectarse un cliente autorizado, TgWitness comprueba la configuración, el centro de datos más cercano, la autorización actual, la línea de base de la capa revisada, los idiomas, las actualizaciones de la aplicación y las actualizaciones de las condiciones de servicio. Estos diagnósticos se ejecutan una vez por cada instancia de cliente, antes de la recopilación, y se muestran en los detalles de la conexión junto con su hora. `account.connection_checked` registra el resultado sin hash de sesión, direcciones IP, tokens ni hash de API. Nunca acepta condiciones ni instala actualizaciones. Un fallo en la solicitud o un FloodWait detiene las solicitudes posteriores; un resultado que falte permanece desconocido. Las comprobaciones locales pueden seguir informando de sus resultados, mientras que las comprobaciones de red se omiten.

Los diagnósticos de FloodWait conservan el método TL fallido, cualquier envoltorio Takeout/rango, la espera solicitada por el servidor y el plazo efectivo en `telegram.backoff`. Los detalles de la conexión muestran el método y el plazo mientras las solicitudes están en pausa. El diagnóstico incluye contadores de llamadas de cliente por método desde que se creó dicho cliente; cuentan por separado la resolución de pares anidados, pero no cuentan los paquetes ni los intentos de reintento internos de Telethon. Los contadores actuales también están disponibles como `collector.rpc_activity` en la API de estado. No se incluyen argumentos de solicitud, nombres de usuario, hashes de acceso ni texto de excepción. El último diagnóstico y el plazo completo se conservan tras el reinicio. Las esperas anteriores sin un registro de método no pueden atribuirse retrospectivamente. Consulte [: límites de exportación](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) para la revisión del código fuente y la distinción entre descubrimiento y adquisición del historial.

`official_app=True` o `False` es el indicador de autorización actual de Telegram. Ninguno de estos valores determina si la cuenta está restringida, es de confianza o se encuentra bajo observación. Las instantáneas `account.devices` existentes en modo de pruebas siguen constituyendo el historial de todos los dispositivos que han iniciado sesión; los diagnósticos de conexión solo conservan la descripción del dispositivo actual.

Antes de la conexión, las comprobaciones de asesoramiento comparan la plataforma API, el paquete de idioma, los formatos de dispositivo/sistema operativo y versión de la aplicación, la configuración regional del sistema móvil y la capa de esquema real de Telethon con la línea de base del catálogo revisado. Las advertencias aparecen en el registro del servidor y en los metadatos del estado de la cuenta; nunca sustituyen los valores importados ni modifican la capa de esquema. Una capa diferente es una señal de revisión de compatibilidad, no una prueba de que la cuenta esté inactiva o restringida. Estas comprobaciones y el código `official_app` no certifican que Telegram considere que la cuenta está a salvo de restricciones. El estado de cuenta desconectada utiliza el perfil guardado en lugar de generar otra descripción del dispositivo.

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

Los formularios **Archivos**, **Clave de autenticación** y de importación masiva muestran la advertencia de sesión paralela antes de conectarse. Por defecto, las autorizaciones importadas se reutilizan. Mantén el cliente original cerrado mientras su clave se esté utilizando aquí. **Archivos** y **Clave de autenticación** también ofrecen **Crear una autorización independiente**, descrita más adelante. La importación masiva sigue utilizando el modo directo. El inicio de sesión por teléfono y mediante QR interactivo crea autorizaciones independientes. El encabezado de la advertencia permanece visible en el formulario de importación; su explicación completa se abre automáticamente cuando se proporcionan archivos o una cadena de clave/sesión. Se puede ocultar tras leerla, de modo que el selector de archivos y los controles de conexión sigan siendo utilizables en un teléfono.

- Los archivos se convierten **en memoria** en su servidor de TgWitness. Las subidas no se almacenan, los archivos ZIP no se extraen al disco y no se establece contacto con ningún servicio externo.
- A continuación, la sesión resultante se comprueba con Telegram. Si un archivo indica un ID de usuario, debe coincidir con la cuenta que Telegram indica.
- Se rechazan los archivos que describen diferentes cuentas o diferentes credenciales de API en lugar de seleccionar una sola.
- El campo **«Código de acceso o texto de sesión»** contiene el campo de código de acceso local de TData, un cuadro en el que se puede pegar una StringSession y **leer archivos sin iniciar sesión** (se rellena el formulario sin conectarse a Telegram).

### Crear una autorización independiente

Selecciona **Crear una autorización independiente** antes de conectar archivos importados o una clave de autorización. TgWitness conecta brevemente al donante importado, lo utiliza para aprobar el token de inicio de sesión QR del nuevo cliente y desconecta al donante inmediatamente después de la aprobación. El nuevo cliente tiene su propia clave de autorización y un perfil de escritorio seleccionado por separado. Las credenciales de la API y el perfil del dispositivo proporcionados por el donante se utilizan únicamente para la conexión del donante. No se cierra sesión ni se revoca ninguna autorización existente.

**Mantén el cliente original del donante completamente cerrado durante este paso.** La conexión inicial sigue utilizando su clave copiada, por lo que este modo no puede eliminar ese riesgo inicial de uso paralelo. Una vez conectada la nueva autorización, el propietario puede reabrir el cliente original y utilizar ambos de forma independiente. El inicio de sesión interactivo **mediante código QR** permite que el cliente original apruebe el inicio de sesión sin copiar ni conectar su clave aquí.

Si Telegram solicita 2FA, este modo utiliza `twoFA` del JSON seleccionado cuando esté presente, o solicita la contraseña. Si se rechaza una contraseña importada, se vuelve al formulario de contraseña. Las contraseñas no se guardan. La clave candidata se guarda cifrada en el `independent_login.enc`, incluidos los cambios durante la migración del centro de datos. Tras una interrupción, selecciona el mismo donante y esta opción para reanudar la clave candidata guardada. El espacio de trabajo permanece reservado para esa cuenta; si la finalización falla, no se elimina el nuevo espacio de trabajo. Conserva su directorio de datos y la clave de la bóveda. Las credenciales finales y el registro del diario de `account.authorized` incluyen el método de importación, los formatos de entrada y el ID de la API del donante, sin la clave ni la contraseña del donante.

El 5 de noviembre de 2026, una cuenta dedicada superó las comprobaciones en tiempo real con los donantes de Telethon, Pyrogram y TData: finalización de la autenticación de 2 factores (2FA), nuevas claves de autorización distintas, acceso simultáneo por parte del donante y del nuevo cliente, y lectura de un canal público. El caso de Telethon también reanudó un candidato guardado tras una interrupción en el paso de la contraseña. Cada nueva autorización completó las seis solicitudes de inicialización posteriores al inicio de sesión, y su registro firmado se verificó. La sesión original siguió siendo utilizable en los cuatro formatos proporcionados.

La base de datos de errores [RPC de Telegram](https://core.telegram.org/api/errors.json) asocia `FRESH_CHANGE_ADMINS_FORBIDDEN` al cambio de administradores, `FRESH_CHANGE_PHONE_FORBIDDEN` al cambio de número de teléfono y `FRESH_RESET_AUTHORISATION_FORBIDDEN` a la revocación de otras sesiones, el cambio de su duración o el registro de una clave de acceso. `SESSION_TOO_FRESH_*` y `PASSWORD_TOO_FRESH_*` se refieren a transferencias de titularidad y retiradas de ingresos o regalos. No se trata de operaciones de recopilación; un nuevo inicio de sesión no implica una prohibición general de lectura de 24 horas. La exportación puede devolver `TAKEOUT_INIT_DELAY_*` por separado. TgWitness conserva las pausas solicitadas por el servidor y no reintenta la aceptación de tokens automáticamente ni revoca sesiones para eludir restricciones.

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
- El perfil de conexión utiliza `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` y `tz_offset` opcional (segundos respecto a UTC, de -43200 a 50400). Los campos proporcionados tienen prioridad sobre los valores predeterminados generados y el idioma del panel o del navegador . Se rechazan los alias conflictivos. El perfil resuelto se guarda en las credenciales cifradas del espacio de trabajo y se reutiliza tras el reinicio, incluida la versión de la aplicación.
- `phone`, la configuración del proxy y los tokens de dispositivo se **ignoran**. `twoFA` es de solo lectura cuando se selecciona **Crear una autorización independiente**; la importación directa lo ignora.
- Un JSON sin un campo de autorización compatible es solo metadatos. Añade su archivo de sesión o continúa con el inicio de sesión mediante teléfono o código QR. Un JSON que contenga una sesión compatible o una clave de autenticación puede autorizar por sí solo; consulta [Account JSON](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData es la carpeta «`tdata`» de la aplicación Telegram Desktop (la aplicación multiplataforma de desktop.telegram.org).

| Sistema | Ubicación predeterminada: `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portátil: junto a `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Para importarlo:

> **Advertencia de sesión paralela.** La importación directa de TData reutiliza la clave de autorización de Telegram Desktop. No utilices esa clave en Desktop y TgWitness simultáneamente. Telegram puede invalidar la autorización con `AUTH_KEY_DUPLICATED`, dejando ambas copias inutilizables hasta que se realice un nuevo inicio de sesión.
>
>
>
> Cierra completamente Desktop, incluido su proceso en la bandeja del sistema, y mantén esa copia cerrada mientras TgWitness utiliza la sesión importada. **Cierra la aplicación, no cierres la sesión ni revocas la sesión:** la revocación también invalida la copia importada. Si necesitas que ambos clientes estén en ejecución, selecciona **Crear una autorización independiente** y mantén Desktop cerrado hasta que el nuevo inicio de sesión se realice con éxito, o inicia sesión en TgWitness mediante teléfono o código QR. Se recomienda utilizar una cuenta dedicada, pero esto no garantiza que las claves clonadas sean seguras para su uso en paralelo.
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
| `string_session` (`session_string`, `session_str`; `session` heredado) | Texto de «StringSession» de Telethon, no es un nombre de archivo |
| `auth_key` (`auth_key_hex`) + `dc_id` | Clave de autenticación completa de 512 caracteres y DC 1–5 |
| `user_id` (`id`) | Opcional; se comprueba con Telegram antes de guardar la autorización. |
| `device_model` (`device`) | Descripción del dispositivo de conexión |
| `system_version` (`sdk`) | Versión del sistema operativo de conexión |
| `app_version` | Versión de la aplicación enviada a Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Idioma del cliente, idioma del sistema y paquete de idioma del cliente; se permite un valor `lang_pack` vacío. |
| `tz_offset` | Desfase opcional respecto al UTC en segundos, enviado en `initConnection.params`; número entero o cadena de números enteros decimales |

Si aparecen tanto un alias como el nombre principal, deben coincidir. Los campos explícitos de sesión de Telethon tienen prioridad sobre un blob genérico `session` en otro formato. Si ambos contienen sesiones de Telethon reconocibles, deben describir la misma autorización. A falta de un campo explícito, `session` debe ser una StringSession válida de Telethon. Ejemplos:

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
