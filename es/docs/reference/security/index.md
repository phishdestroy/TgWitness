# Seguridad y tratamiento de datos

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/security/

Modelo de amenazas, modelo de acceso, información confidencial en reposo, exposición de la red, importación de sesiones y cómo notificar una vulnerabilidad.

This page describes access，storage and network protection in a local or server workspace． For collection on a GitHub runner or in an Intel TDX confidential VM，see the [verification modes](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope)，which add checks of the collection environment． Account connections，notifications，timestamps，off-site copies and witnesses have their own routing settings．

| Área | En resumen |
| --- | --- |
| Acceso | Clave de administrador más acceso limitado a cuentas y chats, siete permisos y sesiones revocables; localhost por defecto. |
| Secretos en reposo | La sesión, el par de API, la clave de firma y la configuración del proxy se cifran con Fernet |
| Mensajes y archivos multimedia | Se almacena sin cifrar: utilice el cifrado de disco y permisos estrictos |
| Integridad | Cadena de hash SHA-256 y una firma Ed25519 en cada registro |
| Local trust boundary | The host administrator controls the workspace and its signing key；independent checkpoints retain an earlier journal boundary |

Para informar sobre vulnerabilidades, consulte la [política de seguridad](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

## Modelo de acceso

El token del panel principal otorga control total. Otras personas pueden recibir su propio [acceso limitado](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/): espacios de trabajo y chats seleccionados, permisos, caducidad, restricciones de IP, límites de inicio de sesión y sesiones revocables. Un acceso limitado a un chat no puede realizar operaciones en todo el espacio de trabajo, aunque se haya marcado su permiso. Los espacios de trabajo comparten un proceso y no aíslan los datos del administrador del servidor.

El panel escucha en localhost de forma predeterminada. Al iniciar sesión desde el navegador, se intercambia un token de acceso por una credencial de sesión; el navegador lo envía como un token de portador. Se almacena en sessionStorage en lugar de en una cookie de autenticación. Al bloquear la sesión o cerrarla, se borra la sesión del navegador. Cerrar el navegador o finalizar una sesión no detiene la recopilación.

Los tokens emitidos y las credenciales de sesión se almacenan como hash en la bóveda cifrada. La revocación pone fin a las sesiones asociadas; los cambios en los permisos afectan a las solicitudes posteriores. Los archivos descargados no pueden recuperarse. El administrador también puede limitar sus propias sesiones de navegador, pero los scripts que utilizan directamente el token del panel principal conservan acceso completo y eluden dichos límites de sesión del navegador.

Los intentos fallidos de autenticación están limitados por la dirección del cliente. Las restricciones de IP utilizan la dirección que ve la aplicación; compruebe el comportamiento del proxy inverso antes de basarse en él. Las credenciales de Witness siguen siendo credenciales independientes de solo lectura para el control de estado y el punto de control.

### Acceso a la demostración

`/api/demo-access` es un bootstrap deliberadamente no autenticado para una demostración sintética aislada e iniciada explícitamente. Emite una capacidad independiente válida durante la vida útil del proceso, nunca el token real del panel ni una sustitución de TGWITNESS_TOKEN. Su emisión y uso requieren un par de bucle de retorno y un host, sin encabezados reenviados ni solicitudes de origen cruzado. Los espacios de trabajo adicionales o una sesión autorizada desactivan esta vía. Los espacios de trabajo activos nunca emiten dicha capacidad. La demostración no puede vincular cuentas ni modificar la configuración de recopilación.

## Contenido de los paneles y exportaciones

El panel no utiliza fuentes externas, herramientas de análisis, recursos CDN ni medios remotos incrustados. El texto procedente de Telegram se inserta como texto, no como HTML. Los archivos adjuntos descargados se sirven como archivos adjuntos binarios. Las exportaciones en formato JSONL conservan las cadenas originales; el HTML las escapa; a las celdas CSV que podrían convertirse en fórmulas se les antepone un apóstrofo.

Las exportaciones excluyen los secretos de autenticación y firma, pero contienen deliberadamente metadatos de origen recopilados, identificadores y, posiblemente, contenido personal o sensible. En los metadatos de origen sin procesar pueden aparecer hash de acceso a Telegram y referencias a archivos.

## Secretos en reposo

Telegram API credentials，the session and signing key are encrypted with Fernet． For local messages and media，encryption is provided by the host's disk or volume； the workspace stores ordinary files．Exports can use a password-protected AES-256 ZIP， and off-site copies use AES-256-GCM．

The vault key defaults to the protected data directory．Use an external master-key file below to store it separately．On Unix，new private-key files use mode 0600 and new data directories use 0700；on Windows，set the directory ACL for the service account and authorized administrators．Existing directory permissions are retained．

### Clave maestra externa

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode．Disk encryption protects the local message and media files in either mode；see [connection and data protection](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/) for setup details．

## Proxies y rutas de red

La configuración del proxy se cifra en el almacén de datos. Las contraseñas y los secretos de MTProxy no se devuelven a través de la API ni se registran en los registros de pruebas. Cada espacio de trabajo elige su ruta de Telegram y un [modo de IP](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/#ip-modes).

**La opción «Ocultar la dirección»** desactiva el acceso directo a Telegram y requiere un proxy para las solicitudes HTTP externas. El modo de acceso alternativo seleccionado explícitamente permite el acceso directo a Telegram tras un retraso; el modo túnel/VPN permite rutas directas. Al elegir el modo túnel no se instala ni se verifica ninguna VPN. Esta configuración no controla todo el tráfico del equipo, ni los navegadores, ni los gestores de paquetes, ni la resolución de DNS del proxy local.

MTProxy solo transmite tráfico de Telegram. Las solicitudes externas pueden utilizar un proxy SOCKS5/HTTP independiente, la ruta SOCKS5/HTTP del espacio de trabajo o una ruta directa autorizada; también pueden desactivarse. El testigo independiente cuenta con su propia configuración de transporte. La autenticación CONNECT habitual de SOCKS5/HTTP no está cifrada por dichos protocolos de proxy en sí mismos. Los secretos TLS falsos de MTProxy siguen sin ser compatibles.

## Inicio de sesión e importación de sesiones

Los archivos .tgwitness-session convertidos contienen un secreto de autorización en texto plano hasta que se cargan y se almacenan en la bóveda. La interfaz de línea de comandos (CLI) sin conexión acepta esquemas de Telethon revisados. Además, la importación a través del panel admite Pyrogram SQLite, el moderno formato ZIP de TData para una sola cuenta, y entradas JSON documentadas. Está autenticada, limitada a cuatro archivos / 8 MiB, y procesa las subidas en memoria sin necesidad de extraer el archivo ni guardar los archivos originales. Las credenciales normalizadas solo se devuelven al navegador autenticado que las solicita; se guardan en el almacén cifrado tras una autorización satisfactoria en Telegram. Proteja los archivos originales y los convertidos, y evite que clientes simultáneos clonen una autorización.

El procesamiento de datos verifica las sumas de comprobación de los contenedores, los hash de descifrado locales y las longitudes de las estructuras. Se utiliza de forma temporal una contraseña local de la versión de escritorio facilitada, que no se almacena. Este analizador limitado no garantiza que todas las versiones de escritorio sean compatibles. Las imágenes QR se generan localmente, contienen tokens de inicio de sesión de Telegram de corta duración y nunca se envían a un servicio de renderización externo. El bloqueo, el cambio de espacio de trabajo, un nuevo inicio de sesión y los cambios de ruta cancelan los intentos de QR pendientes. Al recargar o cerrar una pestaña, puede quedar un intento pendiente hasta su caducidad. Un inicio de sesión mediante QR satisfactorio sigue exigiendo la vinculación de la cuenta. Los cuerpos de la API ordinarios siguen estando limitados a 16 KiB; la ruta de importación autenticada acepta hasta 12 MiB de JSON codificado, aplicando por separado el límite más reducido para el archivo decodificado.

Los códigos de inicio de sesión y las contraseñas de verificación en dos pasos de Telegram no se almacenan de forma permanente. El estado del número de teléfono o del hash del código se mantiene en memoria durante la autorización. Las sesiones de Telegram otorgan acceso a la cuenta; nunca suba un directorio de datos, una sesión, un token, una clave de almacén o una clave de firma privada a GitHub.

## Registros y transporte

Se sustituye la respuesta predeterminada de validación de la API para que no repita los valores de las credenciales. Se desactiva el registro de acceso a la aplicación. No configure un proxy inverso para registrar encabezados de autorización ni cuerpos de solicitud. El protocolo HTTP transmite tokens y contraseñas de inicio de sesión en texto sin cifrar: utilice HTTPS o un túnel SSH siempre que salga de localhost.

## Límites de integridad

Local verification checks record signatures，the hash chain，attachments and the export manifest． The administrator holds the local signing key and can create another signed journal； an independently retained checkpoint detects replacement of the prefix it covers． Keep the key fingerprint and checkpoints with the recipient or an independent witness．

For independently checked collection，choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/es/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)． Their verifiers check workflow provenance or hardware measurements in addition to archive integrity． Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies； the [evidence format](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope) describes the checks for each mode．

## Si sospecha que hay algún problema

Preserve the original data directory and use a separate copy for analysis． Report the affected version，operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md)，keeping account data and credentials private．
