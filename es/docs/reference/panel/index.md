# Guía de paneles

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/

Todas las pantallas del panel: chats, diario, fuentes, exportaciones, Extras, modos de protección y la comprobación de código.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentación](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/es/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Primera configuración y ajustes](https://phishdestroy.github.io/TgWitness/es/docs/reference/settings/) · [Cuentas](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/) · [Exportar y verificar](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/) · [Informes de casos](https://phishdestroy.github.io/TgWitness/es/docs/reference/case-reports/)

Qué hace cada pantalla, qué escribe en el diario firmado y dónde se encuentra la guía detallada. El panel muestra un espacio de trabajo cada vez: una cuenta de Telegram con sus propias fuentes, diario y clave de firma. El selector situado en la parte superior de la barra lateral permite cambiar de espacio de trabajo. La dirección identifica el espacio de trabajo (`?ws=…`); mientras la dirección, el selector y la cuenta cargada no coincidan, las acciones permanecerán bloqueadas.

Use [Compare collection methods](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md) to choose between live observation, full history, fresh account/chat exports and saved-record handover. The Exports page includes the same comparison above its download controls.

**On this page**

- [Find your way](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#find-your-way)
- [Start here](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#start-here)
- [Chats](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#chats)
- [Journal](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#journal)
- [Sources](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#sources)
- [Exports](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#exports)
- [Settings, accounts and connection](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#settings-accounts-and-connection)
- [Extras](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#extras)
- [Protection modes](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#protection-modes)
- [More tools](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#more-tools)

## Oriéntate

Las secciones diarias se encuentran en la parte superior de la barra lateral; **«Cuentas»** está debajo de **«Espacio de trabajo»** , y todo lo demás se encuentra en **«Más herramientas y ajustes** ». El selector **de nivel de interfaz** de la barra superior determina cuántas secciones aparecen:

| Nivel | Secciones de la barra lateral |
| --- | --- |
| Sencillo | Inicio, Chats, Cambios, Archivos y Ajustes |
| Estándar | Además, Case Board, Cuentas y Acceso |
| Experto | También «Fuentes», «Extras», «Preguntar al archivo», «Parámetros», «Cuenta», «Registro del sistema» e «Integraciones». |

Llamadas sencillas: «Empezar aquí», «Diario» y «Exportaciones», **«Inicio**», **«Cambios»** y **«Archivos**». Un nivel solo oculta secciones. Una función oculta sigue funcionando, y el servidor comprueba cada permiso por sí mismo. El nivel, el idioma, el tema y la zona horaria se guardan por operador y espacio de trabajo; consulta [la configuración](https://phishdestroy.github.io/TgWitness/es/docs/reference/settings/).

La barra superior también incluye:

- **Ve a una sección** (Ctrl+K, o ⌘K en un Mac): busca un chat, un parámetro o un registro del diario mediante `#number`. Las teclas de flecha permiten desplazarse; «Intro» abre y «Esc» cierra.
- **Notificaciones**: problemas y cambios en los chats extraídos del diario. La opción **«Marcar todo como leído»** borra el contador y **«Reglas de notificación»** abre las reglas. El envío a Telegram, Discord o correo electrónico se configura en [Extras → Notificaciones](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#notifications).
- El indicador de conexión de este espacio de trabajo. **El estado del colector,** situado debajo de la barra superior, lo desglosa en conexión a Telegram, recepción de eventos, fuentes y cola de archivos adjuntos.
- **Cerrar**: cierra el panel en este navegador. La colección sigue funcionando en el servidor.
- El modo de protección que aparece junto al número de versión; consulta [los modos de protección](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#protection-modes).

El espacio de trabajo de demostración contiene mensajes ficticios y nunca se conecta a Telegram. Allí se rechazan las acciones que podrían modificar un espacio de trabajo real.

## Empieza aquí

Elige una tarea. **«Exportar mi cuenta»** descarga todo lo que la cuenta puede leer en ese momento. **«Seguir una investigación»** registra los nuevos mensajes, las modificaciones observadas y los avisos de eliminación de los chats que elijas. La ficha de configuración muestra los tres pasos: conectar la cuenta, elegir fuentes e iniciar la observación. La pregunta de objetivo permanece en esta página hasta que la respondas o la omitas. En su lugar, un nuevo espacio de trabajo abre la [primera configuración](https://phishdestroy.github.io/TgWitness/es/docs/reference/settings/).

## Chats

Conversaciones guardadas, de lectura solo por defecto.

- Busca en la lista por nombre o ID. **La opción «Elegir»** añade o elimina chats seguidos. «**Abrir enlace de Telegram»** acepta un nombre de usuario o un enlace de invitación y guarda una vista previa en el diario. **«Unirse/abrir y observar»** se une al chat y lo añade a tus fuentes; al abrir un bot, este se envía `/start`.
- El encabezado del chat cuenta los mensajes **eliminados, el texto conservado**, **los eliminados antes de guardarlos** y **los que no se encuentran al volver a comprobar**. La lista de chats y las notificaciones utilizan las mismas definiciones. Un mensaje eliminado aparece en rojo y conserva su texto guardado; un mensaje editado conserva todas las versiones guardadas. Cada eliminación indica lo que se sabe: cuándo se vio, que Telegram no informa de quién lo eliminó, o que solo llegó el aviso.
- **El historial de carga** muestra los últimos 100, 250 o 500 mensajes en esta vista y en el diario. Para cargar todas las fuentes habilitadas, utiliza [Fuentes → Historial completo](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#sources).
- **La opción «Exportar chat»** descarga todo el historial visible como un `chat.json` y `chat.html`. Varias cuentas conectadas pueden compartir el trabajo: cada una descarga su propio rango de números de mensajes y firma su parte, y la cuenta que inicia la exportación firma el archivo. Véase [«Exportar un chat](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md)».
- **La sección «Personas»** muestra a todos los usuarios con mensajes guardados en este chat. Los perfiles de las personas están desactivados por defecto, ya que se trata de datos personales de terceros. Cuando están activados para un chat, el perfil muestra el nombre y el historial de nombres de usuario, las marcas de Telegram, los hash de los avatares, la actividad, quién responde a quién, otros chats observados y las carteras, teléfonos, nombres de usuario y enlaces mencionados. Cada dato apunta a su registro. **La exportación de perfiles** guarda un archivo firmado, opcionalmente protegido con contraseña ZIP; al desactivar los perfiles se elimina el archivo de perfiles. Consulta [los perfiles de los usuarios](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#people-profiles).
- **La opción «Guardar perfil» ahora** registra una instantánea del perfil del chat o del bot: descripción, miembros, enlace de invitación y comandos del bot.

### Solo lectura, envío y secretos

Dos interruptores situados encima de los mensajes protegen la cuenta y al lector:

- **El modo de solo lectura** se activa al abrir un chat. Desactívalo para enviar mensajes o pulsar los botones del bot . Cada acción pregunta **«¿Enviar como @cuenta?**» o **«¿Pulsar este botón del bot como @cuenta?»**, lo que te indica que los miembros del chat lo verán y que se incluirá en el registro firmado. **La opción «No volver a preguntar durante 10 minutos en este chat»** omite la pregunta durante un rato. El envío está desactivado para el objetivo **«Pruebas de un caso**», tanto en el panel como en la API.
- **«Mask secrets»** oculta lo que parece una contraseña, un código de inicio de sesión, una clave API o un hash, un token de bot, una cadena de sesión, una clave privada, un JWT o un número de tarjeta de pago (los números de tarjeta se comprueban con la suma de Luhn). **«Show»** revela un valor; la revelación se registra en el diario. También se registra la desactivación del enmascaramiento para este navegador. Solo cambia la visualización: los registros originales y todas las exportaciones conservan el texto completo.

## Registro

Todos los registros que ha firmado el espacio de trabajo, ordenados de más reciente a más antiguo.

- **La vista general** cuenta los mensajes observados, las ediciones registradas, los avisos de eliminación y las fuentes seleccionadas.
- **Cronología de eventos** filtra por tipo de evento (todos, ediciones, eliminaciones, reacciones, pertenencia, cobertura), por texto y por fuente. **Cargar eventos anteriores** permite retroceder una página.
- Abre un registro para ver sus detalles, su hash y su carga útil. **El enlace a este registro** es una dirección que abre el mismo registro. Los posibles datos confidenciales se ocultan en esta vista previa; las exportaciones conservan el original.
- El registro es de solo adición: nada en el panel permite editar o eliminar un registro. Compruébalo en **Exportaciones → Verificar registro** o `python -m tgwitness.verify`; consulta [«Exportar y verificar](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/)».

## Fuentes

Este espacio de trabajo registra determinadas conversaciones y conserva la información que considera relevante de ellas. Los cambios se aplican a la actividad futura; los registros guardados se mantienen.

**La opción «Actualizar lista de chats»** lee los chats y las carpetas de la cuenta. No descarga mensajes.

### Ámbito de aplicación

- **Qué registra esta cuenta** : **Chats seleccionados** (solo los chats que añadas), **Carpeta de Telegram** (una de las carpetas de la cuenta, incluidos los chats añadidos a ella posteriormente) o **Cuenta completa** (todos los chats, así como cada nuevo chat, grupo, chat privado o bot a medida que aparezca). **Modo de investigación** es para una cuenta dedicada: registra todo lo que ve la cuenta, sus propios mensajes y las pulsaciones de botones, y guarda inmediatamente el perfil de cada nuevo chat y los mensajes visibles anteriores. La imagen [Guía dedicada a las cuentas](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) explica por qué nunca debes utilizar tu cuenta principal.
- **Los tipos de fuente** limitan los modos de carpeta y de cuenta completa a canales, grupos, chats privados y bots. **«Acciones propias»** añade los mensajes propios de la cuenta, las ediciones y las pulsaciones del teclado al responder.
- **Cuando aparece un nuevo chat o bot**: guarda su perfil y hasta el número elegido de sus últimos mensajes visibles.

Limitaciones: los chats secretos nunca llegan a TgWitness. No se registra nada mientras TgWitness no esté en ejecución; tras un reinicio, solo recupera lo que Telegram aún devuelve, y el informe muestra la diferencia. Los chats que superen el límite de la lista de chats (1.000 diálogos, salvo que se modifique en «Parámetros») se añaden la próxima vez que se activen. Los botones del bot integrados en otra aplicación son invisibles; se registra la respuesta del bot.

### Chats incluidos

Filtra por estado (**Activado**, **En pausa**, **Prioritario**, **Excluido**, **Acceso no confirmado**, **Ignorado**) y tipo, y luego realiza acciones sobre la selección: activar, poner en pausa, marcar o eliminar la prioridad, excluir del ámbito o eliminar. La insignia de estado solo muestra el estado; las acciones se encuentran en el menú de cada fila, con una descripción de lo que hacen. La pausa y la exclusión requieren confirmación, también de forma masiva. Al eliminar una fuente, se solicita su nombre y se borran los perfiles de sus usuarios ; sus registros guardados permanecen en el diario.

Una fuente que no aparece en la lista de chats de la cuenta es **recibir actualizaciones, no en la lista de chats**, mientras siguen llegando registros; en caso contrario, **Acceso sin confirmar**. **Chats disponibles** añade chats con **Añadir seleccionados** o **Añadir todas las coincidencias**.

### Historial completo

Carga el historial disponible de cada fuente habilitada en «Chats» y en el diario. El progreso se conserva tras un reinicio; los archivos adjuntos se ajustan a tu configuración multimedia. Consulta [el historial de la fuente](https://phishdestroy.github.io/TgWitness/es/docs/reference/history/).

### Grabación

- **Elige qué cambios quieres conservar**: mensajes nuevos, ediciones, avisos de eliminación, reacciones visibles, altas y bajas. Un ajuste preestablecido modifica el formulario; la **opción «Guardar configuración de grabación»** lo aplica. Volver a activar una categoría no recupera los eventos perdidos.
- **Conserva los archivos multimedia cuando estén disponibles**: descarga archivos adjuntos hasta un tamaño máximo por archivo, establece por tipo entre 1 y 2.000 MiB, y limita la duración de los vídeos en segundos (0 significa que no hay límite). Cada intento de descarga genera un resultado registrado.
- **Revisión**: los chats prioritarios se comprueban cada pocos minutos, los demás chats rara vez, de modo que la cuenta no supera los límites de FloodWait de Telegram. El valor 0 desactiva un grupo. Marca los chats prioritarios con la estrella en la lista; el número de chats por pasada y la pausa entre chats se configuran en «Parámetros». Consulta [la colección](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/).

## Exportaciones

**«Descargas»** prepara los archivos; **«Informe de compilación»** determina el aspecto de los informes.

| ¿Qué? | Úsalo para | Guía |
| --- | --- | --- |
| Exportación de cuentas | Una instantánea actualizada de lo que la cuenta puede leer ahora | [Exportación de cuentas](https://phishdestroy.github.io/TgWitness/es/docs/reference/account-export/) |
| Compartir copia | Una versión simplificada de una exportación de cuenta completada | [Divulgación](https://phishdestroy.github.io/TgWitness/es/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| Firmado ZIP | Diario, informe, archivos adjuntos y herramientas de verificación dentro de un límite fijo del diario | [Exportar y verificar](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/) |
| Informes en HTML, PDF y JSON | Un informe sellado y legible | [Informes de casos](https://phishdestroy.github.io/TgWitness/es/docs/reference/case-reports/) |
| JSONL, CSV | Registros originales con firmas; una hoja de cálculo con fórmulas protegidas | [Exportar y verificar](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/) |
| Extracto del traspaso | Solo los chats, el periodo y las personas que necesita el destinatario | [Pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#investigation-handoff) |
| Exportación de chats | Un chat firmado `chat.json` y `chat.html` | [Exportar un chat](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **Al cifrar las descargas anteriores con una contraseña** (de 12 caracteres o más), se guarda un archivo AES-256 ZIP que se puede abrir con 7-Zip o WinRAR. El archivo firmado que contiene permanece inalterado. La contraseña no se almacena.
- **Las exportaciones preparadas** conservan hasta 20 archivos de un máximo de 2 GiB, más el más reciente, para descargas repetidas, cada uno con su SHA-256. La preparación de un archivo no garantiza su entrega.
- Cuando el navegador rechaza el cuadro de diálogo de guardado, el panel recurre a una descarga normal.
- **Tu identidad de firma** muestra la huella digital de la clave. Las opciones **«Guardar punto de control»** y «Descargar **recibo de ejecución firmado»** te permiten conservar los registros fuera del colector. La opción «Preparar **solicitud de marca de tiempo»** genera una solicitud RFC 3161 sin contactar con ningún servicio.

## Configuración, cuentas y conexión

- **Configuración**: objetivo, conexión, qué grabar y la interfaz. Consulta [la primera configuración y los ajustes](https://phishdestroy.github.io/TgWitness/es/docs/reference/settings/).
- **Cuentas**: cada espacio de trabajo con su estado, fuentes, eventos y cola de archivos adjuntos. Filtrar por **«Requiere atención»**, **«Recopilando»**, **«Desconectado» o «Pausado»** o **«No conectado»**, pausar o reanudar una selección, importar archivos de cuentas de forma masiva y gestionar grupos. Ver [cuentas](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/).
- **Cuenta**: inicio de sesión y ruta de conexión de esta cuenta. Directa, un perfil de WireGuard, tu propio proxy, el grupo público de MTProto o WARP; prepara y comprueba una ruta, y luego aplícala a esta cuenta, a un grupo o a todas las cuentas. Consulta [«Conexión» y](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/)[«Proxies](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md)».

## Extras

Opcional: basta con una cuenta y unas fuentes para empezar a recopilar información. Solo la opción que elijas abre su configuración, y nada se conecta automáticamente. La tarjeta **«Nivel de protección»,** situada en la parte superior, muestra el [modo de protección](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#protection-modes).

| Tarjeta | Qué aporta | Guía |
| --- | --- | --- |
| Almacenamiento y espacio en disco | Copias de seguridad, traslado de archivos antiguos a tu nube, una copia de prueba que no se puede eliminar | [Almacenamiento](https://phishdestroy.github.io/TgWitness/es/docs/reference/storage/) |
| Objetivo y nivel de protección | Configuración recomendada para tu objetivo y dos escalas | [a continuación](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#goal-and-protection-level) |
| Notificaciones | Problemas, mensajes modificados y un resumen diario; tu propio bot de control | [a continuación](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#notifications) |
| Pruebas y copias de seguridad | Marcas de tiempo, más testigos y una copia cifrada externa | [a continuación](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#evidence-and-backups) |
| Servidor disponible las 24 horas del día, los 7 días de la semana | Un servidor en la nube sin SSH, que se crea y se elimina desde el panel | [Alta fiabilidad](https://phishdestroy.github.io/TgWitness/es/docs/reference/high-assurance/#from-the-panel) |
| Testigo independiente | Comprobantes firmados publicados en tu canal de Telegram o en Discord | [Witness](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/) |
| Revisión del código | Compara el programa en ejecución con una confirmación pública de GitHub. | [a continuación](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#code-check) |

### Objetivo y nivel de protección

Cuatro preguntas:

1. **¿Para qué sirve? Para** un registro personal, una investigación o como prueba en un caso.
2. **¿Cuánto vas a supervisar?** Unos pocos chats (hasta unos 50), muchos chats (hasta unos 500) o cuentas completas. Esto establece el límite de la lista de chats en 1.000, 3.000 o 20.000.
3. **¿Fotos y archivos?** Solo texto, fotos y archivos multimedia cortos (fotos de 20 MB, vídeos de 100 MB), o todo (vídeos y documentos de hasta 1 GB cada uno). La opción «Todo» con cuentas completas también deja 4 GiB de espacio libre en disco.
4. **¿Dónde se ejecutará? En** este ordenador o en un servidor que esté siempre encendido.

La sugerencia enumera marcas de tiempo independientes, drand y la lista de dispositivos de Telegram, cada una con una línea que explica lo que aporta. Las marcas de tiempo se inician cada 60, 30 o 10 minutos para un registro personal , una investigación o pruebas; drand y la lista de dispositivos necesitan marcas de tiempo. **Aplica** cambios solo a estos, a la política de archivos adjuntos y a los dos parámetros anteriores. Cada cambio es un registro del diario, además de `setup.applied`. Las notificaciones, una copia externa, un servidor, el DNS de la puerta de enlace, la comprobación del código y un testigo se ofrecen como pasos siguientes con sus propios formularios.

Se calculan dos escalas a partir de lo que se ha configurado, no a partir del objetivo:

| Escala | Puntos |
| --- | --- |
| Credibilidad | Diario firmado 1, marcas de tiempo 3, drand 1, lista de dispositivos 1, comprobación de código que coincide 1, sondeo de testigos 1, servidor certificado 2, registro DNS de Gateway 1 |
| Fiabilidad | Servidor siempre activo: 3; copia externa: 3; Object Lock: 1; notificaciones de problemas: 1 |

Un 80 % o más se considera **«máximo»**, un 50 % **«alto»**, un 25 % **«moderado**» y por debajo de eso, **«básico**». La fiabilidad se calcula actualmente en función de un servidor siempre activo, según la respuesta a la pregunta 4, antes de que se compruebe ningún servidor.

### Notificaciones

Las notificaciones se envían a través de Apprise a Telegram, Discord, Slack, ntfy, correo electrónico, Matrix y más de 100 servicios adicionales. Elige un servicio, rellena uno o dos campos y envía una prueba, o pega directamente las direcciones de Apprise.

- **Problemas**: disco casi lleno, cuenta desconectada, errores de recopilación, copia o marca de tiempo. En un servidor sellado, un puerto SSH abierto o un inicio de sesión también suponen un problema.
- **Cambios**: mensajes eliminados, editados y que faltan en los chats observados, agrupados en una notificación por comprobación (cada minuto, a menos que se modifique en «Parámetros»).
- **Tareas completadas**: historial, exportaciones y copias de seguridad.
- **Resumen diario** a la hora elegida, según la hora del servidor.

Las notificaciones incluyen los nombres de los chats y el número de mensajes. Los extractos de mensajes están desactivados por defecto; si se activan, el texto de los mensajes sale de este equipo.

**Tu bot operador** es un bot propio creado desde @BotFather que responde `/status` y `/stats`, y, opcionalmente, `/pause`, `/resume` y `/copy`. Solo el chat indicado y los ID de usuario de Telegram pueden utilizarlo; el texto de la conversación permanece en el espacio de trabajo. Utiliza un bot independiente si otra aplicación ya recibe sus comandos. Consulta [notificaciones](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md) y [bot operador](https://phishdestroy.github.io/TgWitness/es/docs/reference/storage/#operator-bot-and-completion-notices).

### Pruebas y copias de seguridad

- **Las marcas de tiempo independientes** envían únicamente el SHA-256 de cada punto de control firmado a las autoridades de la RFC 3161 y a los calendarios de OpenTimestamps, cada 5 a 1.440 minutos. **Anchor ahora** ejecuta una pasada. Véanse [las marcas de tiempo](https://phishdestroy.github.io/TgWitness/es/docs/reference/timestamp/).
- **Más testigos**, cada uno inactivo hasta que se elija: la ronda más reciente de drand, la lista de Telegram de dispositivos conectados sin direcciones IP y el registro de Cloudflare Gateway de las consultas DNS del servidor. Véanse [los registros opcionales](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices).
- **La copia de seguridad cifrada** copia el diario, los archivos, los puntos de control y las exportaciones de chats a un almacenamiento compatible con S3 (Wasabi, Amazon S3, Backblaze B2, Cloudflare R2, MinIO). Todo se cifra primero en esta máquina. **Descarga la clave de cifrado** y guárdala por separado: sin ella, la copia no se puede leer. Object Lock, en modo «Governance» o «Compliance», impide que los objetos se eliminen durante un número determinado de días. Véase [«Copia externa](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md)».

### Revisión del código

Comprueba si el programa instalado coincide con una versión publicada.

1. Introduce un repositorio de GitHub (el oficial ya está rellenado) y una etiqueta, una rama o una confirmación.
2. **«Check now»** consulta la API de GitHub, a través de la ruta de este espacio de trabajo para solicitudes externas, la lista de archivos de esa confirmación. Compara el ID de blob de Git de cada archivo de programa medido con la confirmación. Una copia de Windows con finales de línea convertidos sigue coincidiendo.
3. El resultado muestra una lista de los archivos modificados, añadidos y que faltan (hasta 50 de cada tipo) y se guarda como un `source.checked` registro de diario.

El resultado solo se considera vigente mientras los archivos del programa en ejecución no sufran cambios: vuelve a comprobarlo tras una actualización. No se necesita ningún token y solo funcionan los repositorios públicos; no se suben chats ni credenciales. Una coincidencia identifica el código en el disco. No se trata de una certificación de hardware; para eso, consulta [Phala Cloud](https://phishdestroy.github.io/TgWitness/es/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx).

## Modos de protección

El selector situado junto al número de versión muestra el modo elegido y cuántas de las 18 capas de protección están activas; por ejemplo `🟠 Witnessed 9/18`. **Para cambiar de modo,** en **«Extras» → «Nivel de protección»** se abre el menú de opciones. Cada modo describe un objetivo y enumera lo que aún falta; el registro, la firma y la configuración guardada son iguales en todos los modos.

| Modo | Para | Añade |
| --- | --- | --- |
| 🟢 Fácil | Seguir un chat y guardar una copia | Chats, el diario y las exportaciones de chats; la firma se ejecuta en segundo plano. |
| 🟡 Firmado | Informes dirigidos a una plataforma, un proveedor de alojamiento o un servicio de denuncia de abusos | Archivo firmado, comprobación del diario, puntos de control, extracto de traspaso |
| 🟠 Testificado | Casos en los que alguien podría alegar que el registro ha sido modificado | Un testigo independiente que publica entradas firmadas en el diario |
| 🔴 Apto para los tribunales | Pruebas para un abogado, la policía o un tribunal | Marcas de tiempo, una copia cifrada externa y detalles del caso en informes |
| 🟣 Verificado por GitHub | Registros cuyo software debe poder comprobar cualquiera. | Comprobación del código y captura de GitHub Actions |
| ⚫ Mossad | Casos de gran envergadura contra un adversario con abundantes recursos | Un servidor sellado disponible las 24 horas del día, los 7 días de la semana, una dirección IP oculta y las 18 capas completas |

Las capas: cada registro firmado y encadenado; un recibo de ejecución firmado; archivos adjuntos guardados con SHA-256; puntos de control firmados; revisiones; alertas de problemas; acceso de testigo de solo lectura; un testigo que realiza comprobaciones según lo programado; marcas de tiempo RFC 3161; pruebas OpenTimestamps; una última marca de tiempo verificada; una copia cifrada fuera del sitio; detalles del caso en informes; una comprobación de coincidencia de código ; Telegram nunca ve la IP de este equipo; solicitudes externas a través de un proxy; Object Lock en la copia; un servidor sellado con los registros del proveedor. Una capa que está desactivada tiene **la opción «Configurar»**, que abre su formulario. Al elegir un modo inferior, se solicita confirmación y no se elimina nada.

## Más herramientas

**Extras → Independent capture**: connect a separate browser or AyuGram recorder, pin its signing key, select capture options, start/pause, take snapshots and download verified signed archives. Each recorder has its own manual login, route, journal and key. Both connections start disabled. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md).

- **Consulta el archivo**: busca observaciones guardadas, revisa las fuentes y, a continuación, decide si enviarlas a un modelo de IA. Consulta [el análisis del archivo](https://phishdestroy.github.io/TgWitness/es/docs/reference/analysis/) y [el OCR y la transcripción locales](https://phishdestroy.github.io/TgWitness/es/docs/reference/media-analysis/).
- **Parámetros**: límites y ritmo de recopilación, revisiones, descargas, perfiles, notificaciones y exportaciones. Búsqueda por nombre, mostrar **«Solo** valores **modificados»** y preparar los valores predeterminados como borrador con **«Restaurar valores predeterminados…». «Guardar parámetros»** aplica los valores a partir de su próximo uso, y cada cambio se registra en el diario.
- **Acceso**: tokens independientes para revisores, analistas y operadores, limitados a determinados espacios de trabajo, chats y derechos. Véase [«Acceso](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/)».
- **Registro del sistema** : lo que ha hecho este proceso desde que se inició (conexiones, cambios de proxy, inicios de sesión, rechazos, cambios de configuración) con las direcciones IP ocultas. La opción **«Seguir nuevas líneas»** mantiene visible la línea más reciente. Los mensajes permanecen únicamente en el diario.
- **Integraciones**: el proveedor de IA, conexiones [MCP de solo lectura](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/) y [webhooks firmados](https://phishdestroy.github.io/TgWitness/es/docs/reference/webhooks/).
- **Case Board**: notas privadas del equipo, marcadores y fragmentos junto a las pruebas. Véase [Case Board](https://phishdestroy.github.io/TgWitness/es/docs/reference/case-board/).
- **Captura de GitHub Actions** en «Exports»: un chat capturado desde tu bifurcación. Véase [captura sellada](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md).
