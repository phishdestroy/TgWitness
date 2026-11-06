# Características y limitaciones

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/features/

El modelo de recopilación actual, los flujos de trabajo con varias cuentas, las exportaciones y los límites operativos de TgWitness.

TgWitness conserva las conversaciones de Telegram a las que tienen acceso las cuentas conectadas, registra los cambios observados y prepara exportaciones verificables. Esta referencia describe el modelo de recopilación, los flujos de trabajo actuales y sus límites.

## Aplicación independiente

TgWitness cuenta con su propia instalación, su propio directorio de datos y su propio ciclo de vida de versiones. La interfaz web incluida se encarga de la configuración y la revisión; los registros exportados pueden utilizarse de forma independiente.

El operador vincula sus cuentas, selecciona las fuentes visibles para cada una de ellas y obtiene un registro de observaciones guardado. El panel muestra el contenido, los cambios guardados, la procedencia de las observaciones y las lagunas conocidas. Otro investigador puede verificar el material exportado.

El panel distingue entre la autorización de la cuenta, el acceso a una fuente, la actividad del recopilador y la cobertura registrada. Revisa esos estados en conjunto al evaluar un intervalo con pocos mensajes o un problema de conexión.

## Investigaciones compartidas

Un administrador puede emitir [tokens de acceso](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/) limitados a espacios de trabajo y chats individuales, con permisos por acción, restricciones de IP, caducidad, límites de inicio de sesión y control de sesión. Un revisor con acceso de solo lectura puede examinar un caso sin recibir la autorización de Telegram ni la clave del panel principal. El acceso limitado al chat permanece independiente de la configuración general de la cuenta y de las exportaciones completas del diario.

MTProxy automático mantiene rutas de Telegram operativas a partir de cuatro fuentes públicas o de un catálogo de operadores. [Los modos de IP](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/#ip-modes) determinan si, en caso de fallo, se debe esperar a otro proxy o si se puede utilizar una ruta directa expresamente permitida. Las solicitudes HTTP externas cuentan con una ruta independiente y un interruptor de desactivación.

## Herramientas de archivo

[La adquisición de historiales](https://phishdestroy.github.io/TgWitness/es/docs/reference/history/), [la búsqueda y el análisis de archivos](https://phishdestroy.github.io/TgWitness/es/docs/reference/analysis/),[el MCP de solo lectura](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/), [el OCR y la transcripción locales](https://phishdestroy.github.io/TgWitness/es/docs/reference/media-analysis/), así como[los webhooks salientes](https://phishdestroy.github.io/TgWitness/es/docs/reference/webhooks/) se incluyen en 0.7.1. Los informes analíticos y el texto reconocido permanecen separados de los eventos capturados.

[Case Board](https://phishdestroy.github.io/TgWitness/es/docs/reference/case-board/) añade marcadores vinculados a fuentes, citas, notas y colecciones dentro de un espacio de trabajo. El [generador de informes](https://phishdestroy.github.io/TgWitness/es/docs/reference/case-reports/) selecciona el material, las secciones y uno de los ocho diseños disponibles para las exportaciones compatibles en formato HTML/PDF.

## Extras opcionales

La configuración diaria es: cuenta → fuentes → observación. **«Extras»** es un destino independiente con un bot de Telegram Witness y una vista previa de captura en GitHub. Cada uno indica su disponibilidad y requisitos antes de mostrar la configuración. Al seleccionar una ficha se abren las instrucciones; esto no implica registrarse ni iniciar un servicio.

La configuración del bot consta de tres pasos: crear un acceso de solo lectura, elegir los ajustes de publicación y iniciar el bot en el servidor de TgWitness. Las opciones de red y publicación, las conexiones existentes y los comandos de verificación se revelan bajo demanda. La configuración descargada es distinta de un «witness» en ejecución. Al cambiar de extras se conserva el borrador; los cambios en la cuenta y el bloqueo borran el token temporal y el formulario. La guía integrada incluye instrucciones de puesta en marcha. [GitHub Actions captura](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) y pone en marcha un colector fijado desde tu fork, captura un chat y genera un traspaso cifrado con la procedencia del flujo de trabajo.

## Protocolo y fuentes privadas

**MTProto es el protocolo de Telegram; Telethon es la biblioteca de Python que utiliza TgWitness para comunicarse mediante MTProto.** No se trata de métodos de conexión alternativos. La recopilación utiliza MTProto; el «witness» opcional publica comprobaciones firmadas a través de la API del bot.

Cada espacio de trabajo cuenta con su propio cliente autorizado y su propio flujo de actualizaciones de la cuenta. TgWitness selecciona las observaciones de las fuentes configuradas y realiza solicitudes explícitas independientes para funciones como instantáneas del historial y descargas de archivos multimedia.

Una fuente privada no necesita un nombre de usuario público. El tipo de par de Telegram y el identificador numérico son los identificadores; los títulos y los nombres de usuario pueden cambiar. El acceso depende de la afiliación y los permisos existentes. TgWitness no se une automáticamente a las fuentes ni elude la aprobación de la adhesión. Un hash de acceso procedente de otra cuenta no constituye un token de acceso universal.

El modelo de recopilación debe tener en cuenta el historial oculto previo a la incorporación, los roles de los participantes y administradores, la revocación de sesiones, la eliminación o modificación de permisos, la migración de grupos a supergrupos, los temas y foros, las discusiones vinculadas, las identidades de los canales y los archivos adjuntos no disponibles. No todas las combinaciones se han validado en tiempo real.

La visibilidad de la fuente se comprueba al iniciar el recopilador. La ausencia de una fuente en el resultado delimitado del diálogo significa que **el acceso no está confirmado**, no que se haya demostrado su eliminación. Una fuente no disponible no impide observar otras fuentes accesibles. Nunca incluya enlaces de invitación ni sesiones reales en elementos públicos.

## Cuentas múltiples

El panel admite un número ilimitado de **espacios de trabajo**, cada uno con sus propios:

- Autorización, almacén cifrado y ruta de conexión.
- Registro SQLite e identidad de firma Ed25519.
- Fuentes seleccionadas, cola de medios y ajustes de captura.
- Estado de observación, errores, puntos de control y exportaciones.

Cambiar el espacio de trabajo visible no detiene a otro recopilador. Se rechaza la autorización de cuentas duplicadas entre espacios de trabajo. Un registro ya vinculado a una cuenta de Telegram no puede reasignarse a otra; sí se permite volver a conectar la misma cuenta. De este modo se preserva la identidad de la cuenta y el ámbito de los ID de mensajes pertinentes.

La aplicación no establece un número fijo de espacios de trabajo. Cada espacio de trabajo ejecuta sus propias tareas de recopilación para la supervisión de conexiones, descargas de archivos multimedia, revisiones y captación de nuevos chats dentro de un proceso compartido de Python y un bucle de eventos. El rendimiento depende de la carga de trabajo. Para aislar los procesos, utilice instalaciones, puertos y directorios de datos independientes.

Asigna a cada cuenta las fuentes a las que puede acceder. Diferentes cuentas pueden observar el mismo grupo, pero sus observaciones permanecen separadas y conservan su origen. Dos cuentas en un mismo equipo controlado por un operador no constituyen dos testigos independientes. **La exportación de grupo** agrupa los archivos ZIP de los espacios de trabajo firmados por separado con una lista de archivos firmada que contiene sus ID de espacio de trabajo, hash y huellas de las claves de firma. Cada diario conserva su propio límite. Crea una línea temporal combinada entre espacios de trabajo en las notas del caso o en herramientas de análisis, conservando esas referencias a las fuentes.

## Captura y atribución

La sección «Fuentes» ofrece opciones por cuenta para mensajes nuevos, modificaciones, eliminaciones, reacciones y pertenencia a grupos. Los ajustes preestablecidos conservan todas las categorías o bien los mensajes, las modificaciones y las eliminaciones. La política se aplica a los grupos seleccionados del espacio de trabajo, se mantiene tras el reinicio y está firmada con los cambios anteriores y posteriores. Los valores predeterminados conservan todas las categorías. Desactivar una categoría no elimina los registros antiguos; volver a activarla no reconstruye los eventos omitidos. Los registros operativos, otros eventos del servicio de grupo y las instantáneas explícitas del historial son independientes. Los objetos de Telegram capturados pueden conservar metadatos incrustados independientemente de los parámetros de actualización independiente. Todavía no existen anulaciones de categorías por grupo.

| Material | Capturado ahora | Límites |
| --- | --- | --- |
| Mensaje | Texto, identificadores de interlocutor/mensaje, metadatos del remitente, respuestas y sobre de actualización original | Se conserva como una observación visible en la cuenta y firmada por el recopilador. |
| Editar | Nueva versión observada y cualquier versión guardada anteriormente | Las modificaciones realizadas durante el tiempo de inactividad pueden perderse; el remitente no es necesariamente quien realiza la edición. |
| Eliminación | Notificación y contenido capturado previamente, si lo hubiera | Por lo general, no se indica quién ha eliminado el mensaje ni la hora exacta de la acción. |
| Aviso de eliminación a nivel de cuenta | Aviso original; los registros resueltos incluyen el chat guardado y el método de correlación. | Se requiere exactamente una coincidencia de un chat privado o un grupo ordinario guardado previamente dentro del ámbito; los demás identificadores permanecen en «`deletion.unscoped`». Los identificadores de canales y supergrupos quedan excluidos de esta correlación. |
| Reacción | Contadores de mensajes enviados e identidades recientes visibles | Para obtener una lista completa de los reactores disponibles es necesario realizar consultas por separado; los canales pueden ocultar identidades. |
| Afiliación | Mensajes de servicio y actualizaciones enviadas a los participantes | La visibilidad depende del rol y del tipo de chat; la ausencia de eventos no implica que no se hayan producido. |
| Acciones de administración | Actualizaciones relevantes entregadas y una instantánea del registro de administración en las exportaciones de chats de canales y supergrupos. | La exportación lee el registro cuando está disponible para la cuenta de administrador que realiza la exportación; la consulta continua del registro de administración queda fuera de este proceso. |
| Archivo adjunto | Descriptor de la versión original, bytes descargados/SHA-256 y resultados de los intentos | Un archivo eliminado puede ser irrecuperable; la última versión no se sustituye. |
| Historia | Captura de pantalla explícita de los mensajes visibles en ese momento | No reconstruye todas las modificaciones ni el contenido eliminado. |
| Proceso de recopilación | Inicio/parada, señal de vida, errores, configuración, alcance y recibo de ejecución firmado | Inventario local; GitHub y TDX añaden [comprobaciones de entorno independientes](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope) |

La interfaz identifica la cuenta indicada en el evento de origen y conserva los nombres y nombres de usuario observados. Cuando el evento omite a su autor, el informe deja ese campo sin especificar.

## Capacidad y límites de Telegram

No existe un número universal de chats que puedan supervisarse con calidad garantizada. La capacidad depende de los picos de eventos por segundo, el volumen y el tamaño de los archivos adjuntos, los RPC adicionales, las cuentas activas, la latencia del disco y el espacio libre, las condiciones de la red, los límites de Telegram, el retraso aceptable y la profundidad de la cola.

Telegram distingue entre la entrega pasiva y el sondeo activo breve. Su documentación de actualización describe llamadas `updates.getChannelDifference` adicionales para canales abiertos y supergrupos, y recomienda un máximo de **diez fuentes sometidas a sondeo activo breve simultáneamente**. Esto no supone un límite de diez grupos seleccionados ni una garantía de exhaustividad.

| Modo | Objetivo | Estado |
| --- | --- | --- |
| Observación estándar | Registre las actualizaciones recibidas de fuentes seleccionadas | Implementado |
| Revisiones prioritarias | Las fuentes marcadas con una estrella utilizan su propio intervalo configurable y tienen prioridad en cada pasada de revisión delimitada. | Implementado con consultas de historial y mensajes |

La estrella de prioridad controla estas revisiones. El sondeo corto adicional «`updates.getChannelDifference` » no se muestra como un modo de usuario independiente.

Las consultas arbitrarias de alta frecuencia, que ignoren FloodWait o asuman una capacidad lineal procedente de cuentas adicionales, no constituyen un modelo de dimensionamiento válido. Los límites predeterminados son los primeros 1.000 diálogos de la lista, hasta 500 mensajes por instantánea del historial, entre 1 y 2.000 MiB por archivo recopilado según el tipo, y 4 GiB de contenido ZIP firmado sin comprimir; cada uno de estos valores se modifica por espacio de trabajo en **«Parámetros**». Las exportaciones no tienen un límite fijo de recuento de eventos. El modo alternativo del navegador está limitado a 128 MiB de forma predeterminada; la CLI de transmisión tiene un límite de transferencia configurable, de 5 GiB de forma predeterminada.

## Fiabilidad y recuperación

Entre los comportamientos implementados se incluyen transacciones WAL/sincrónicas de SQLite; escrituras atómicas de mensajes y tareas multimedia; tareas persistentes y retrasos en los reintentos; descriptores de la versión original; reintentos limitados; FloodWait de archivos multimedia persistentes; descargas de archivos multimedia fuera de la espera de red del evento de texto; exportaciones con prefijo estable mientras continúan las escrituras posteriores; ajustes atómicos y registros de auditoría; conservación de la autorización de trabajo tras un fallo en el inicio de sesión de sustitución; aislamiento de un espacio de trabajo adicional dañado; intentos explícitos de reconexión; informes diferenciados de pérdida de autorización; y detección de cambios en el reloj real mediante un reloj monótono.

Los puntos pts, qts y seq de las cuentas y los canales se guardan y se recuperan tras un reinicio, y los chats observados se vuelven a comprobar periódicamente; véase [el formato de las pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#durable-collection-and-process-receipts-02). Guardar la posición periódicamente no constituye una confirmación atómica y sin pérdidas de la aceptación del registro.

Cada inicio de proceso registra el encabezado anterior y el límite fuera de línea. El historial actual no se trata como una reparación de lagunas. La retención de diferencias de Telegram es finita; `differenceTooLong` no puede reconstruir todo el contenido desaparecido. Las lagunas irrecuperables deben permanecer explícitas incluso si una instantánea posterior del historial tiene éxito.

## Modelo de pruebas

Cada evento registra una secuencia, la hora de observación local en UTC, la hora de origen (cuando se facilite), el tipo, la fuente, el autor (cuando se facilite), la carga útil original, el hash anterior y la firma. Las observaciones de mensajes también conservan la cuenta del recopilador y el contexto de ejecución.

El recibo de proceso firmado contiene un identificador de ejecución aleatorio; las versiones de TgWitness/Python/OS y sus dependencias; los valores SHA-256 de los archivos fuente y la huella digital agregada; la cuenta inicial, el ámbito y la configuración; lecturas UTC/monotónicas; y el encabezado del registro anterior. Los cambios en la configuración, el inicio y la detención, así como los errores, se registran en el mismo registro. Los puntos de control se conservan al inicio, cada cinco minutos durante la observación (parámetro modificable) y al detener la herramienta de forma ordenada. Un punto de control local conservado permite detectar una reversión a un prefijo de registro anterior.

| Mecanismo | Qué establece |
| --- | --- |
| SHA-256 del archivo | Los bytes coinciden con un resumen conocido |
| Cadena de hash de eventos | Ordenación y vinculación de registros en relación con un límite conocido |
| Ed25519 | Firma con una clave concreta |
| Punto de control conservado de forma independiente | El material posterior se ajusta a los límites establecidos. |
| Análisis del archivo del programa | Informe del propio recopilador sobre los archivos analizados |
| Respuesta válida e independiente de la TSA | Existencia de bytes concretos en el momento TSA bajo supuestos de confianza explícitos |

Se han implementado la preparación de solicitudes según el RFC 3161 y la verificación de respuestas mediante OpenSSL. El modo «Evidence» también envía los hash de los puntos de control a los servicios de marca de tiempo configurados. Conserva y verifica la respuesta de la autoridad para establecer un punto de referencia temporal independiente. Consulta [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/timestamp/).

Conserve los puntos de control de forma independiente, controle el acceso a las claves de firma, mantenga registros de transferencia y verifique las exportaciones con software de confianza. El [alcance de la verificación](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope) explica cómo se complementan entre sí esas comprobaciones y qué supuestos de confianza se aplican.

## Exportación, implementación y traspaso

Un archivo ZIP firmado contiene los archivos originales en formato JSONL, CSV y HTML, los archivos adjuntos conservados, los hash, un manifiesto firmado y un verificador de conveniencia. Abarca un espacio de trabajo y un prefijo fijo para el registro completo. Los filtros de búsqueda del panel no eliminan registros de forma silenciosa. Se excluyen las claves secretas, los tokens y las sesiones de Telegram; las observaciones originales pueden seguir conteniendo información personal y metadatos de Telegram.

Conserve por separado el resumen ZIP, la huella digital de confianza, el punto de control, el acuse de recibo del proceso y el registro de traspaso. Utilice un verificador procedente de una instalación de confianza, en lugar de confiar en el código ejecutable únicamente porque aparece en el archivo ZIP examinado.

La interfaz del navegador se distribuye localmente sin necesidad de Node.js, CDN ni fuentes externas. Un token de operador controla la instalación. El acceso remoto requiere HTTPS o un túnel SSH. Se proporcionan definiciones nativas en Python y de contenedores, con ejemplos de servicios en [la carpeta «deploy/»](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md); las comprobaciones de plataforma ejecutadas se enumeran por separado.

El espacio de trabajo predeterminado utiliza la raíz de datos; los espacios de trabajo adicionales utilizan `profiles/<id>/`. La copia de seguridad requiere que el proceso esté detenido y que se disponga del conjunto completo de datos y claves. Los archivos ZIP de pruebas no son copias de seguridad de la aplicación. Secrets puede utilizar una clave maestra externa para un nuevo directorio de datos; el cifrado del registro y los archivos multimedia lo proporciona el disco o volumen del operador. Consulte [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/) y [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/operations/).

## Criterios de lanzamiento de la versión estable

Antes de una versión estable, especifique:

1. Grupos privados reales, supergrupos, foros y canales con roles de miembro/administrador y historial oculto/visible, incluyendo inicio de sesión/autenticación de dos factores (2FA), revocación y pérdida de acceso.
2. Se controlan las modificaciones, las eliminaciones, las reacciones, la pertenencia a grupos y los archivos multimedia en relación con acciones conocidas.
3. Fallos del proceso o del servidor, fallos del disco o disco lleno, referencias a archivos caducados, FloodWait, pérdida de conexión, archivos dañados y reversión de la base de datos.
4. Uso continuado de múltiples cuentas con retrasos, colas, memoria y disco controlados, incluyendo fuentes silenciosas y ruidosas de forma conjunta.
5. Interrupción entre el avance del estado de MTProto y la aceptación del registro.
6. Instalación limpia en la matriz de sistemas operativos y contenedores prevista, y restauración de copias de seguridad verificada.
7. Revisión independiente de la seguridad, las firmas y las afirmaciones relativas a la atribución y las pruebas.

El acceso limitado a los paneles se describe en [«Acceso y permisos](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/)». La versión 0.6 admite la importación de TData de una sola cuenta delimitada y la importación de archivos de cuenta descritas en [ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/). Revisa los términos de la API de Telegram antes de la publicación. Las referencias de investigación y los resultados sobre la plataforma se encuentran en [RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md).
