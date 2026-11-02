# Acceso y permisos

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/access/

Configure el acceso a cuentas y chats, seleccione los permisos, limite las sesiones y las direcciones IP, y revoque el acceso.

Conceda a un revisor acceso a un chat, a un analista permiso para exportar un caso o a un operador el control de cuentas seleccionadas. Cada persona dispone de su propio token. El token del panel principal lo conserva el administrador.

[Configuración de la cuenta](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/) · [Rutas de conexión](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/) · [Modelo de seguridad](https://phishdestroy.github.io/TgWitness/es/docs/reference/security/)

## Dos ámbitos de aplicación, dos funciones distintas

**El ámbito de recopilación** determina qué registra una cuenta: chats seleccionados, una carpeta de Telegram o la cuenta completa. **El ámbito de acceso** determina cuáles de esas cuentas y chats registrados puede ver y utilizar otra persona. Conceder acceso no implica unirse a un chat de Telegram, iniciar la recopilación ni otorgar permisos de la cuenta de Telegram.

Un acceso puede abrir espacios de trabajo seleccionados, chats seleccionados dentro de ellos, todos los espacios de trabajo o todas las cuentas de un [grupo de cuentas](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#bulk-import-and-account-groups). **Todos los espacios de trabajo, incluidos los que se añadan posteriormente**, también abarcan las cuentas futuras. Un acceso de grupo también abarca las cuentas que se añadan a ese grupo más adelante. Selecciona los espacios de trabajo de forma explícita cuando un caso deba limitarse a ellos.

## Conceder acceso a alguien

1. Inicie sesión como administrador principal y abra **«Acceso**».
2. En **«Conceder acceso a alguien**», introduzca un nombre que pueda reconocer en el registro.
3. Seleccione los espacios de trabajo y, cuando sea necesario, los chats individuales.
4. Seleccione lo que esta persona puede hacer. La opción **«Ver»** siempre está incluida.
5. Configure la fecha de caducidad, los límites de inicio de sesión y de duración de la sesión, así como las direcciones permitidas, según sea necesario.
6. Pulse **«Crear acceso**». Copie el token ahora: solo se muestra una vez.
7. Envíe la dirección del panel y el token de forma privada. El destinatario introduce dicho token en la página de inicio de sesión habitual; no necesita su token principal del panel ni una sesión de Telegram.

Abra el panel con el token generado en una sesión de navegador independiente y compruebe los chats visibles y las acciones permitidas antes de entregarlo.

## Seleccione los permisos

Para una demostración pública solo de texto, utilice **la «Galería pública»** en lugar del acceso habitual para revisores. Muestra canales públicos seleccionados explícitamente, ediciones y eliminaciones conservadas, y estadísticas firmadas, con los campos de autor ocultos y los archivos cerrados en el límite de la API. [Cree y verifique una galería](https://phishdestroy.github.io/TgWitness/es/docs/reference/showcase/).

| Autorización | Qué permite |
| --- | --- |
| `view` | Lea los chats autorizados, los mensajes capturados, los perfiles, los archivos y los registros filtrados del diario. Siempre incluidos. |
| `export` | Se permite la exportación del historial de chat y de los expedientes. Las exportaciones de pruebas de todo el espacio de trabajo requieren acceso a dicho espacio en su totalidad. |
| `sources` | Gestione fuentes, instantáneas y capturas de perfiles. El acceso limitado a los chats solo puede actuar sobre los chats permitidos; la detección de fuentes en toda la cuenta y la configuración del ámbito de aplicación permanecen inactivas. |
| `collect` | Iniciar o detener un recopilador. Requiere acceso a todo el espacio de trabajo, ya que la recopilación afecta a la cuenta. |
| `interact` | Realice las interacciones compatibles con Telegram dentro del ámbito de acceso. El acceso limitado al chat no permite utilizar la vista previa de enlaces en toda la cuenta. |
| `settings` | Modifique la configuración de la recopilación, las marcas de tiempo, las notificaciones, las copias externas y los parámetros. Requiere acceso a todo el espacio de trabajo. |
| `account` | Inicie o cierre sesión en Telegram y gestione las rutas de conexión. Requiere acceso a todo el espacio de trabajo. |
| `board.read` | Lee las notas del «Case Board» únicamente dentro del espacio de trabajo y los chats permitidos. |
| `board.write` | Añade marcadores, resaltados, fragmentos, comentarios y estados de apertura/revisión. También requiere «`board.read`». |
| `board.manage` | Gestiona las recopilaciones, los estados finales de los equipos y las fichas de otros participantes. También requiere permisos de lectura y escritura en el tablero. |

Los permisos y el alcance se comprueban conjuntamente. Marcar un permiso no abre otros chats ni desbloquea una operación a nivel de espacio de trabajo para un acceso limitado a un chat. Para una exportación paralela, el acceso debe abarcar el chat exportado en todas las cuentas seleccionadas. Un acceso concedido no puede crear nuevos accesos, gestionar las sesiones de otras personas ni abrir la consola de administrador.

### Tres configuraciones útiles

| Persona | Ámbito de aplicación | Permisos |
| --- | --- | --- |
| Revisor | Chats grabados de un caso concreto | `view` |
| Analista que prepara un traspaso de funciones | Los chats que se deben investigar y exportar | `view`, `export`; añada `interact` únicamente si deben actuar a través de Telegram |
| Operador de recopilación | Espacios de trabajo completos seleccionados | `view`, `sources`, `collect`; añada `settings` o `account` únicamente cuando sea necesario |

Los ajustes preestablecidos iniciales del formulario de Access también incluyen el Tablero de casos: el revisor puede leer, el analista puede leer y escribir, y el operador puede gestionarlo. Los ajustes preestablecidos siguen siendo editables y los permisos existentes no se amplían automáticamente. Consulte [el Tablero de casos](https://phishdestroy.github.io/TgWitness/es/docs/reference/case-board/) para conocer los ámbitos de chat heredados y la privacidad de las exportaciones.

## Límites y sesiones

| Configuración | Cómo funciona |
| --- | --- |
| Sesiones paralelas | Limite el número de sesiones simultáneas a entre 1 y 100. Al alcanzar el límite, rechace el siguiente inicio de sesión o finalice la sesión más antigua. |
| Se permite el inicio de sesión | Limite el número de usos correctos del token para iniciar sesiones. Las sesiones existentes no se cierran simplemente porque se haya agotado el último inicio de sesión permitido. |
| Válido hasta | El acceso tiene una caducidad definitiva. Un acceso caducado no puede iniciar sesión ni seguir realizando solicitudes. |
| Minutos sin actividad | Tiempo de espera por inactividad de la sesión, de 5 minutos a 30 días. Las solicitudes exitosas lo amplían; un panel abierto puede mantenerse activo mediante sondeos. |
| Direcciones permitidas | Acepte direcciones IP específicas o subredes CIDR. Déjelo en blanco para permitir cualquier dirección, a menos que esté habilitada la vinculación al primer inicio de sesión. |
| Vincular al primer inicio de sesión | El primer inicio de sesión correcto establece la dirección autorizada para ese acceso. |

La IP es la dirección del cliente que ve la aplicación. Si se encuentra detrás de un proxy inverso o un túnel, compruebe la dirección que aparece en **«Sesiones abiertas»** antes de basarse en reglas de IP: de lo contrario, podría parecer que varios usuarios comparten la dirección del proxy.

## Modificar o retirar el acceso

Edita una entrada en **«Acceso concedido»** para cambiar su ámbito, permisos o límites. Los cambios en el ámbito y los permisos se comprueban en las solicitudes posteriores, incluidas las solicitudes de sesiones que ya estén abiertas. La revocación de un acceso pone fin a sus sesiones y hace que el token emitido quede inutilizable. La opción **«Sesiones abiertas»** también permite al administrador cerrar una sesión individual sin revocar todo el acceso.

Las copias de exportación guardadas conservan su creador, el espacio de trabajo, el alcance del chat y los permisos necesarios. Un usuario con acceso concedido solo puede ver o descargar sus propias copias mientras dichos permisos sigan vigentes; las copias que contengan el «Case Board» también requieren el permiso «`board.read`». El administrador puede recuperar todas las copias. Las copias más antiguas que carezcan de estos metadatos y los paquetes de grupo son de acceso exclusivo para el administrador. Las solicitudes de descarga y las respuestas de archivos preparadas vuelven a comprobar el acceso tras preparar el archivo, antes de enviar sus bytes.

La revocación no permite recuperar archivos que alguien ya haya descargado. Cerrar sesión, bloquear el panel o finalizar una sesión no detiene un recopilador en ejecución.

## Lo que puede ver el administrador

Los revisores y analistas reciben información sobre el progreso de la recopilación sin puntos finales de proxy, diagnósticos de grupo, rutas de servidor ni errores de conexión sin procesar. Los diagnósticos de conexión requieren el permiso «`account`» en todo el espacio de trabajo. La lectura de notificaciones, las copias externas y la configuración de parámetros requieren el permiso «`settings`».

Las cadenas completas de User-Agent del navegador no se conservan en las sesiones de acceso. Una actualización también las elimina de la caché mutable de la sesión. El registro de procesos del panel enmascara las direcciones IP literales, las credenciales de URL y los secretos etiquetados. Los registros de servicio locales y los registros de diario firmados anteriormente no se reescriben. Las reglas de acceso y los registros de inicio de sesión firmados siguen utilizando la dirección del cliente.

### Sustituir la clave principal

Utilice **Acceso → Mis límites → Reemitir clave de administrador**, o ejecute `tgwitness token rotate` desde una instalación gestionada mientras el panel está en funcionamiento. Se cierran todas las sesiones del navegador existentes, incluidas las sesiones abiertas con tokens de compañeros. El navegador solicitante recibe una nueva sesión; guarde la nueva clave de administrador antes de ocultarla. Los tokens de compañeros emitidos siguen siendo válidos hasta que se revoquen por separado. Una instalación que utilice `TGWITNESS_TOKEN` debe modificar esa configuración del entorno y reiniciarse.

### Límites de las solicitudes y del proxy

La API admite hasta 600 solicitudes por minuto por IP de cliente. Diez autenticaciones rechazadas en un minuto activan un periodo de espera exponencial, que va desde un segundo hasta cinco minutos. Un intento fallido tras el periodo de espera lo prolonga; diez minutos sin intentos fallidos reinician la escalada. Los rechazos devuelven HTTP 429 y `Retry-After`. Los límites se almacenan en memoria y se comparten entre los espacios de trabajo de un mismo proceso del panel; al reiniciar, se borran. Las transmisiones en directo están limitadas a cuatro por token de portador y a 32 para el proceso del panel. Abrir una transmisión también consume el presupuesto de solicitudes de la API.

Los cuerpos de las solicitudes tienen un plazo de recepción de 60 segundos (8 segundos para MCP). Cada aplicación limita los cuerpos incompletos a 32 solicitudes y 64 MiB de asignaciones de ruta reservadas. Los cuerpos de tamaño excesivo devuelven el código 413, los que superan el tiempo de espera devuelven el 408, y cuando se agota la capacidad de los cuerpos se devuelve el 503 con «`Retry-After`».

Se ignoran los encabezados de IP reenviados a menos que el par TCP real pertenezca a `TGWITNESS_TRUSTED_PROXIES` (IP separadas por comas o CIDR). Establece `TGWITNESS_PROXY_HEADER` en `x-forwarded-for` o `cf-connecting-ip`. El XFF se recorre desde el proxy más cercano hacia el primer par no fiable. Los metadatos de direcciones de confianza malformados o duplicados se rechazan, por lo que no pueden heredar una dirección de proxy incluida en la lista de permitidos . El túnel rápido gestionado confía en el conector local de Cloudflare; la configuración de dominio propio confía en Caddy local. Las implementaciones directas no confían en ningún proxy por defecto. Si inicias Uvicorn tú mismo, desactiva su procesamiento de encabezados de proxy para que este límite reciba el par real.

`TGWITNESS_PANEL_ALLOWED_IPS` restringe todo el acceso al panel, incluido el del administrador, a las direcciones IP o CIDR indicadas. La sonda de identidad de enrutamiento del instalador permanece pública y no devuelve datos de la cuenta. Incluye la ruta administrativa local requerida antes de habilitar la lista de permitidos. La guía **START-HERE** de una instalación gestionada incluye la configuración del servicio y las instrucciones de recuperación.

Un selector de consulta de la API `ws` debe identificar el espacio de trabajo en la ruta de la solicitud; los selectores desconocidos, que no coinciden o que son duplicados se rechazan con un error 404.

Los scripts y estilos de los paneles incluyen metadatos de integridad SHA-384. Un mapa de importación también cubre los módulos JS importados localmente en navegadores que admiten la integridad de import-map. La respuesta de lenguaje generada dinámicamente es independiente. Estas comprobaciones detectan la sustitución de activos en relación con la página entregada; no establecen confianza en un servidor comprometido que pueda sustituir tanto la página como sus hash.

**El registro desde este inicio** combina los registros de proceso con la actividad del diario de cada espacio de trabajo: inicios de sesión, rechazos, cambios de ruta y acciones del operador. Se trata de una consola en memoria para el proceso actual, no de una copia permanente de cada mensaje. Los eventos de mensajes frecuentes permanecen en el diario en lugar de saturar la consola.

La concesión, modificación y revocación de accesos, así como el inicio o la finalización de sesiones, también generan registros firmados en el diario `access.*`. Los tokens no se incluyen en dichos registros. Los tokens emitidos y las credenciales de sesión se conservan como hash en la bóveda cifrada.

****Administrador principal y límite de confianza**** El token del panel principal no está sujeto a restricciones. Los inicios de sesión en el navegador con dicho token crean sesiones sujetas a los límites de sesión configurados por el administrador. Los scripts que envían el token principal directamente conservan acceso completo y no se contabilizan como sesiones de navegador. Se trata de un control de acceso a nivel de aplicación en una única instalación. Todos los espacios de trabajo comparten el proceso del servidor; esto no supone un aislamiento respecto al administrador del host. Mantenga la privacidad del token principal, las sesiones de Telegram, las claves de firma y el directorio de datos. Un token de testigo es una credencial independiente de estado y control, no un token de acceso al panel.
