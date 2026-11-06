# Seguridad y tratamiento de datos

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/security/

Modelo de amenazas, modelo de acceso, información confidencial en reposo, exposición de la red, importación de sesiones y cómo notificar una vulnerabilidad.

Esta página describe el acceso, el almacenamiento y la protección de la red en un espacio de trabajo local o en un servidor. Para la recopilación en un GitHub Runner o en una máquina virtual confidencial de Intel TDX, consulta los modos [de verificación](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope), que añaden comprobaciones del entorno de recopilación. Las conexiones de cuentas, las notificaciones, las marcas de tiempo, las copias externas y los testigos tienen su propia configuración de enrutamiento.

| Área | En resumen |
| --- | --- |
| Acceso | Clave de administrador más acceso limitado a cuentas y chats, siete permisos y sesiones revocables; localhost por defecto. |
| Secretos en reposo | La sesión, el par de API, la clave de firma y la configuración del proxy se cifran con Fernet |
| Mensajes y archivos multimedia | Se almacena sin cifrar: utilice el cifrado de disco y permisos estrictos |
| Integridad | Cadena de hash SHA-256 y una firma Ed25519 en cada registro |
| Límite de confianza local | El administrador del servidor controla el espacio de trabajo y su clave de firma; los puntos de control independientes conservan un límite anterior del diario. |

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

Las credenciales de la API de Telegram, la sesión y la clave de firma se cifran con Fernet. Para los mensajes y archivos multimedia locales, el cifrado lo proporciona el disco o volumen del servidor; el espacio de trabajo almacena archivos normales. Las exportaciones pueden realizarse mediante un archivo ZIP con cifrado AES-256 protegido con contraseña, y las copias externas utilizan AES-256-GCM.

La clave de la bóveda se establece por defecto en el directorio de datos protegidos. Utilice un archivo externo de clave maestra como se indica a continuación para almacenarla por separado. En Unix, los nuevos archivos de clave privada utilizan el modo 0600 y los nuevos directorios de datos utilizan el modo 0700; en Windows, configure la lista de control de acceso (ACL) del directorio para la cuenta de servicio y los administradores autorizados. Se conservan los permisos existentes del directorio.

### Clave maestra externa

Para un nuevo directorio de datos, TGWITNESS_VAULT_KEY_FILE puede proporcionar una clave maestra aleatoria externa. HKDF-SHA256 y una sal aleatoria independiente generan una clave Fernet diferente para cada espacio de trabajo. Se debe conservar el archivo vault.external.json para la recuperación. Si faltan las claves maestras o estas son incorrectas, la operación no se completará. Las bóvedas locales existentes no se migran de forma silenciosa. El panel muestra el modo de almacenamiento de claves seleccionado. El cifrado de disco protege los archivos de mensajes y multimedia locales en cualquiera de los dos modos; consulte [«Conexión y protección de datos»](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/) para obtener detalles sobre la configuración.

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

Las comprobaciones de verificación locales verifican las firmas de los registros, la cadena de hash, los archivos adjuntos y el manifiesto de exportación. El administrador posee la clave de firma local y puede crear otro diario firmado; un punto de control conservado de forma independiente detecta la sustitución del prefijo que cubre. Conserva la huella digital de la clave y los puntos de control con el destinatario o un testigo independiente.

Para una recopilación verificada de forma independiente, elija [la captura](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) [de GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) o [la implementación de Intel TDX](https://phishdestroy.github.io/TgWitness/es/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Sus verificadores comprueban la procedencia del flujo de trabajo o las mediciones de hardware, además de la integridad del archivo. Las marcas de tiempo opcionales y las copias cifradas externas proporcionan puntos de referencia temporales y copias recuperables; el [formato de](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope) [las](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope) [pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope) describe las comprobaciones para cada modo.

## Si sospecha que hay algún problema

Conserve el directorio de datos original y utilice una copia independiente para el análisis. Informe de la versión afectada, el funcionamiento y los pasos para reproducir el fallo a través de la política [de seguridad](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), manteniendo la confidencialidad de los datos de la cuenta y las credenciales.
