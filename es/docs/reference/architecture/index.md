# Arquitectura

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/architecture/

Componentes del colector, el panel, el registro, los trabajadores y el testigo, y cómo se transfieren los datos entre ellos.

Un proceso de Python aloja el panel de FastAPI y un número ilimitado de espacios de trabajo aislados, cada uno con un cliente de cuenta de usuario de Telegram. SQLite almacena un registro de eventos firmado de solo adición y una configuración operativa modificable. Una bóveda cifrada almacena las credenciales de la API, la StringSession y la clave de firma. La interfaz de usuario es un paquete sencillo de HTML/CSS/JavaScript: no se requiere compilación con Node, CDN ni descargas de la interfaz de usuario en tiempo de ejecución.

| Módulo | Responsabilidad |
| --- | --- |
| collector.py | Autorización, selección de diálogos, actualizaciones, instantáneas, cola de archivos multimedia, supervisión de la conexión |
| interactions.py / telegram_client.py | Acciones explícitas de los paneles, recibos firmados, identificadores de solicitud persistentes y política de reintentos de llamada de retorno o reincorporación a la tarea a nivel local. |
| message_content.py | Comparación observable de mensajes, excluyendo los metadatos de acceso de transporte |
| workers.py | Espere a que finalicen los procesos de exportación de archivos antes de proceder a la limpieza tras la cancelación |
| store.py | Transacciones WAL, cadena de eventos ordenada, filtros de consulta, ajustes operativos |
| security.py | Creación de archivos privados, almacén cifrado, firma Ed25519, bloqueo de un único proceso |
| evidence.py | Exportación del registro completo, derivados, puntos de control y verificación de archivos adjuntos |
| verify.py | Verificador independiente y de solo lectura (biblioteca estándar + criptografía): archivos, cobertura, registros de testigos y publicaciones en canales, archivos de perfil |
| app.py | API autenticada, ciclo de vida, validación de solicitudes, panel estático |
| profiles.py | Recopiladores de cuentas múltiples, controlador de acceso compartido, ciclo de vida por espacio de trabajo |
| access.py | Concesiones de acceso, comprobaciones de permisos, restricciones de IP, límites de sesión y consola de administrador |
| proxy_catalog.py | Instantáneas de los canales públicos, comprobaciones de transporte, conjunto de proxies compartidos y selección basada en el estado de funcionamiento |
| provenance.py | Mediciones firmadas de identidad, código y dependencias en el ciclo de adquisición |
| network.py | Rutas validadas por espacio de trabajo; estado y pruebas censurados; opciones de transporte de Telethon |
| sessions.py | Conversión sin conexión y de solo lectura de los esquemas SQLite revisados de Telethon |
| account_import.py | Detección y normalización en memoria de los archivos de cuentas compatibles y de los archivos JSON |
| tdata.py | Lector ZIP TData moderno y limitado, validación de sumas de comprobación y descifrado, sin extracción. |
| doctor.py | Comprobaciones de disponibilidad local sin recopilación de datos, inicio de sesión ni instalación de paquetes |
| download.py | Descarga de exportación en tiempo real autenticada, con lecturas limitadas y sin sobrescrituras. |
| monitoring.py | Política de eventos validada por espacio de trabajo y reglas de archivos adjuntos por tipo, compartidas por los gestores, el estado y los recibos firmados. |
| scope.py | Ámbito de observación (chats seleccionados, carpeta de Telegram, cuenta completa), tipos de fuentes, exclusiones y niveles de revisión |
| dossier.py | Perfiles de usuarios por chat elaborados a partir de registros guardados: datos con referencias de registro, SHA-256/pHash del avatar y extracción de menciones. |
| witness_api.py | Tokens de testigo de solo lectura y el encabezado firmado del registro que pueden obtener |
| witness.py | Proceso de testimonio independiente: clave y registro propios, comprobaciones de autenticidad, publicaciones firmadas en el canal, exportación |
| alerts.py | Notificaciones de Apprise y la lista de notificaciones del panel |
| logging_config.py | Registro en consola y diagnóstico rotativo del servidor para ejecuciones sin ventana. |
| static/ | Interfaz adaptativa, puerta de acceso local, filtros, detalles, exportaciones y configuración de la cuenta. |
| demo.py | Registro sintético claramente identificado, aislado de la recopilación real. |

Los gestores de observación se registran antes de la conexión. La recopilación en tiempo real está condicionada por la identidad del cliente activo, el estado de ejecución explícito, las fuentes habilitadas o el ámbito de observación (los modos de carpeta o de cuenta completa añaden un nuevo chat como fuente en su primera actualización), y la política de eventos. Los clientes rechazados o sustituidos no pueden aportar actualizaciones en tiempo real. Las reacciones sin procesar y las actualizaciones de membresía mantienen los límites de visibilidad. El contenido del mensaje entrante y su tarea de soporte duradero se registran conjuntamente. Las tareas conservan el descriptor TL original y vinculan su hash a la observación del mensaje firmado. Se separan las semánticas de remitente, editor y eliminador.

Cada espacio de trabajo admite una cuenta y cuenta con su propio directorio e identidad de firma. El espacio de trabajo principal permanece en la raíz por motivos de compatibilidad; los espacios de trabajo adicionales se encuentran en profiles/<id>/. Un único token de portador controla toda la instalación; los espacios de trabajo no son entidades de autorización independientes. Los bloqueos de procesos protegen los directorios; los bloqueos de la base de datos serializan la inserción de eventos. Cada adición se confirma de forma sincrónica en el WAL de SQLite con el modo sincrónico FULL. Los controladores de actualización/eliminación de eventos impiden las modificaciones habituales de la aplicación; los administradores del sistema de archivos permanecen dentro del límite de confianza.

La autorización de la API se realiza mediante un token de portador. Las operaciones de inicio de sesión se serializan y están limitadas en el tiempo. Las cargas de cuentas utilizan un límite específico de 12 MiB para el cuerpo codificado y un límite de 8 MiB para el archivo descodificado; las solicitudes normales de la API mantienen el límite de 16 KiB. La conversión se ejecuta en un hilo de trabajo, mantiene las subidas en memoria y devuelve la entrada normalizada al navegador autenticado. El inicio de sesión mediante código QR cuenta con un candidato por espacio de trabajo, un identificador de corta duración, una tarea de espera y una cancelación explícita. Solo la autorización aceptada se convierte en el cliente activo. Telegram FloodWait se devuelve con un valor Retry-After; las credenciales y los mensajes de error RPC sin procesar no se exponen en los errores de la API. Las exportaciones se ejecutan fuera del bucle de eventos asíncrono y se serializan por espacio de trabajo. Transmiten una instantánea de lectura estable y pueden coexistir con escrituras WAL continuas. Los recopiladores de espacios de trabajo comparten el proceso y el bucle de eventos.

Las instantáneas del historial actual y las actualizaciones en tiempo real pueden solaparse. Ambas constituyen observaciones independientes, identificadas por su fuente; los duplicados no se ocultan de forma silenciosa. No se implementa ninguna inferencia a partir de identificadores que falten, texto eliminado inventado, enumeración forzada de miembros o incorporación automática a grupos. No se implementa.

Para obtener una explicación dirigida a los operadores, consulte [cómo funciona la recopilación](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/) y [los formatos de cuentas y sesiones](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/).

La configuración de red se almacena en la bóveda cifrada. Al aplicar una ruta, se cierran los clientes antiguos y se cancelan los inicios de sesión pendientes; las conexiones posteriores utilizan esa ruta sin recurso alternativo directo. Una nueva instalación con clave externa deriva la clave Fernet de cada espacio de trabajo mediante HKDF-SHA256 a partir de un archivo de clave maestra y una sal aleatoria almacenada. Esto protege los secretos de forma independiente del directorio de datos, y no el contenido del registro o de los archivos multimedia en texto plano.

La entrada de demostración local utiliza una capacidad de proceso generada por separado, nunca el token del panel configurado. La emisión y la aceptación requieren el modo de demostración explícito, una raíz sintética sin espacios de trabajo adicionales ni una sesión autorizada, un par/host de bucle cerrado, sin encabezados de reenvío de proxy y sin solicitudes del navegador de origen cruzado. Las API en tiempo real mantienen la autenticación de portador y rechazan los cambios en la recopilación de datos en modo de demostración.
