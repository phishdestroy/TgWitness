# Flujos de trabajo y operaciones

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/operations/

Funcionamiento diario del panel: modos, categorías de supervisión, parámetros, notificaciones, exportaciones, copias de seguridad y capacidad.

Para su primera conexión, utilice [las cuentas y los formatos de sesión](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/). Para obtener una explicación sobre las versiones guardadas, las políticas de eventos y las lagunas, consulte [cómo funciona la recopilación](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/). Esta guía abarca el funcionamiento diario y la recuperación.

## Flujo de trabajo del operador

Diagrama de flujo · Elija el almacenamiento y la protección de claves → Abra el panel con su token; Abra el panel con su token → Seleccione un espacio de trabajo; Seleccione un espacio de trabajo → Configurar ruta directa o a través de un proxy; Configurar ruta directa o a través de un proxy → Introduzca su número de teléfono o seleccione archivos / código QR; Introduzca su número de teléfono o seleccione archivos / código QR → Compruebe la identidad de la cuenta y seleccione los grupos a los que tiene acceso; Compruebe la identidad de la cuenta y seleccione los grupos a los que tiene acceso → Guarde las políticas de eventos y archivos adjuntos y, a continuación, inicie la observación; Guarde las políticas de eventos y archivos adjuntos y, a continuación, inicie la observación → Supervisar errores, accesos, colas y espacio en disco; Supervisar errores, accesos, colas y espacio en disco → Mantener puntos de control independientes; Mantener puntos de control independientes → Exportar y verificar el material · Elija elalmacenamiento y laprotección de claves · Abra el panel con sutoken · Seleccione un espaciode trabajo · Configurar rutadirecta o a través deun proxy · Introduzca su númerode teléfono oseleccione archivos /código QR · Compruebe la identidadde la cuenta yseleccione los gruposa los que tiene acceso · Guarde las políticasde eventos y archivosadjuntos y, acontinuación, iniciela observación · Supervisar errores,accesos, colas yespacio en disco · Mantener puntos decontrol independientes · Exportar y verificarel material

**Diagrama en formato de texto**

1. Elija el almacenamiento y la protección de claves → Abra el panel con su token
2. Abra el panel con su token → Seleccione un espacio de trabajo
3. Seleccione un espacio de trabajo → Configurar ruta directa o a través de un proxy
4. Configurar ruta directa o a través de un proxy → Introduzca su número de teléfono o seleccione archivos / código QR
5. Introduzca su número de teléfono o seleccione archivos / código QR → Compruebe la identidad de la cuenta y seleccione los grupos a los que tiene acceso
6. Compruebe la identidad de la cuenta y seleccione los grupos a los que tiene acceso → Guarde las políticas de eventos y archivos adjuntos y, a continuación, inicie la observación
7. Guarde las políticas de eventos y archivos adjuntos y, a continuación, inicie la observación → Supervisar errores, accesos, colas y espacio en disco
8. Supervisar errores, accesos, colas y espacio en disco → Mantener puntos de control independientes
9. Mantener puntos de control independientes → Exportar y verificar el material

La autorización, la conectividad de la red, el acceso a un grupo y la integridad de la entrega son propiedades distintas. Un estado de conexión verde no implica que se hayan capturado todos los eventos.

## Compartir el trabajo sin compartir la clave principal

**Acceso** abierto para proporcionar a un revisor o analista su propio token. Seleccione las cuentas y los chats a los que puedan acceder y, a continuación, autorice la visualización, la exportación o las acciones operativas. Un operador que inicie o detenga la recopilación necesita acceso a todo el espacio de trabajo; un revisor puede estar limitado a un único chat. Los límites de sesión, la caducidad y las reglas de IP son independientes de la autorización de la cuenta de Telegram. Consulte el apartado [de acceso y permisos](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/).

Utilice **«Sesiones abiertas»** para finalizar una conexión o «Revocar el acceso» para poner fin a todas sus sesiones. La consola de administración combina la actividad de los procesos en curso en todos los espacios de trabajo. El cierre de la sesión deja la recopilación en marcha.

## Modos de funcionamiento

| Modo | Acción | Comportamiento |
| --- | --- | --- |
| Demostración | scripts\Demo.cmd o `--demo` | Datos sintéticos; conexiones con cuentas reales desactivadas |
| Observación | Iniciar la observación | Registre las actualizaciones recibidas de las fuentes seleccionadas |
| Instantánea del historial | Fuentes → instantánea del historial | Hasta 500 mensajes actuales; no se reconstruyen todos los cambios anteriores. |
| Pausa | Observación de pausa | Detener la recopilación conservando los datos y los trabajos en cola |
| Revisión/entrega | Exportaciones | ZIP, JSONL/CSV/HTML, punto de control, acuse de recibo del proceso y solicitud de marca de tiempo |
| Cuentas múltiples | Espacios de trabajo o el botón superior «**+**» | Cualquier número de espacios de trabajo independientes en un único proceso |

El acceso a la demostración local se abre automáticamente sin necesidad de introducir un token manualmente. Utiliza una capacidad válida durante la vida útil del proceso, exclusiva para el acceso directo de bucle cerrado a una demostración sintética aislada; el token del panel principal no se revela. Los espacios de trabajo reales y el acceso a la demostración de forma remota o a través de un proxy mantienen la autenticación mediante token. El acceso a la demostración no otorga ninguna autorización de Telegram.

## Categorías de seguimiento

![Configuración de supervisión por cuenta con datos de origen sintéticos](https://phishdestroy.github.io/TgWitness/assets/sources.png)

En **Fuentes → Configuración de captura → Elegir qué cambios conservar**, seleccione de forma independiente los mensajes nuevos, las modificaciones, los avisos de eliminación, las actualizaciones de reacciones y los eventos de pertenencia a grupos. La configuración predeterminada conserva todas las categorías. La opción **«Mensajes, modificaciones y eliminaciones»** mantiene el contexto original mientras desactiva las actualizaciones independientes de reacciones y miembros. **«Toda la actividad visible**» restaura las cinco opciones. Los ajustes preestablecidos modifican el formato; pulse **«Guardar configuración de supervisión»** para aplicarlos.

La política guardada se aplica a todas las fuentes seleccionadas en ese espacio de trabajo. Los demás espacios de trabajo conservan su propia configuración. Cada cambio real registra los valores firmados «antes» y «después» ; la política actual también se incluye en los recibos de proceso y en los registros de inicio de observación . Desactivar una categoría no elimina las observaciones anteriores. Volver a activarla no recupera los cambios que se hayan perdido. En esta versión no existe la posibilidad de anular las categorías por grupo.

Mantenga activada la opción de nuevos mensajes cuando el contenido anterior sea relevante: un aviso de eliminación no puede recuperar texto que nunca se haya capturado. Los registros operativos y de cobertura, así como otros eventos del servicio de grupo, se conservan siempre. Las instantáneas explícitas del historial son independientes de la selección de categorías en tiempo real y pueden incluir mensajes de servicio. Estas opciones no ocultan los metadatos de reacciones o de miembros incrustados en un objeto de Telegram que, por lo demás, haya sido capturado.

Una instantánea del historial puede poner en cola los archivos adjuntos mientras está en pausa. Inicie la observación para procesarlos. Estar en cola no significa que se hayan descargado. Un archivo original no disponible no se sustituye por una versión editada más reciente; los resultados se registran por separado.

**Al bloquearse,** se borra el acceso del navegador y los campos secretos, pero la recopilación sigue en marcha. Al cerrar una pestaña, el proceso también sigue en marcha. Al detener el proceso o el servicio de Python, se detiene la recopilación independientemente del estado del navegador.

Al eliminar un espacio de trabajo adicional, se detiene su recopilador y se eliminan sus datos locales. Si un archivo bloqueado o un error del sistema de archivos interrumpe la eliminación, el panel informa del fallo y mantiene el espacio de trabajo en la lista como no disponible (`DeletionPending`). Cierre los programas que tengan abiertos sus archivos y vuelva a intentar **la eliminación**. Al reiniciar TgWitness, dicho espacio de trabajo permanece detenido y no se recrean su registro ni sus claves parcialmente eliminados. Una eliminación satisfactoria se registra solo después de que se haya eliminado el directorio; las copias exportadas o respaldadas por separado permanecen sujetas a su propia política de retención.

## Notificaciones

Abra **«Fuentes» → «Notificaciones» → «Alertas» y un resumen diario**. TgWitness utiliza Apprise para enviar alertas a Matrix, Telegram, Discord, Slack, ntfy, correo electrónico y otros servicios compatibles. Puede añadir varios destinos a un mismo espacio de trabajo.

1. Introduzca una URL de destino de Apprise por línea. Utilice el [catálogo de servicios y los formatos de URL](https://appriseit.com/services/) correspondientes a su servicio.
2. Active la opción **«Enviar notificaciones**» y, a continuación, seleccione las alertas de problemas, los cambios en los chats supervisados y un resumen diario. La hora del resumen se basa en la hora del servidor.
3. Active la opción **«Incluir extractos breves»** si desea que el texto guardado de los mensajes eliminados y editados aparezca en las alertas.
4. Pulse **«Guardar notificaciones**» y, a continuación, **«Enviar prueba»** para comprobar la entrega.

Para su propio receptor, utilice [el webhook JSON](https://appriseit.com/services/json/) de Apprise. Por ejemplo, `jsons://notify.example.org/tgwitness` envía JSON a través de HTTPS a ese punto final. Se trata de un ejemplo ficticio; sustitúyalo por su propio destino.

Los destinos y la configuración pertenecen al espacio de trabajo seleccionado. Las notificaciones de cambios abarcan las fuentes supervisadas, incluidos los chats añadidos recientemente. La campana de la barra superior también muestra los problemas recientes y los cambios en los chats.

En la demostración, los controles de notificación están visibles, pero el envío está desactivado. Configure el envío en un espacio de trabajo real. Las notificaciones utilizan la ruta Direct, SOCKS5 o HTTP de ese espacio de trabajo; MTProxy no puede transmitirlas. Los destinos que no sean HTTP, como SMTP, requieren una ruta directa.

## Diseño de paneles

![Espacio de trabajo de conexión con datos sintéticos](https://phishdestroy.github.io/TgWitness/assets/connection.png)

**El registro** muestra observaciones, búsquedas y filtros. Al editar un mensaje, se abren las versiones capturadas; al borrar un mensaje, se muestra el contenido anterior, si está disponible. Las atribuciones desconocidas se indican de forma explícita. Los recuentos están disponibles en **«Visión general»**; los detalles de la adquisición se mantienen en la guía local.

**La sección «Fuentes»** incluye el ámbito de observación (chats seleccionados, una carpeta de Telegram o toda la cuenta), chats accesibles de todo tipo, fuentes seleccionadas con estrellas de prioridad, ajustes de archivos adjuntos y de reverificación, así como instantáneas del historial. Las fuentes privadas se seleccionan por diálogo o ID sin enlace público. El estado de acceso describe la última comprobación, no los permisos permanentes.

**En «Chats → Personas»** se muestra una lista de todas las personas cuyos mensajes se han guardado; si se han activado los perfiles de usuario para el chat, al hacer clic se abre el perfil de esa persona con enlaces a los registros del diario.

**Witness** crea tokens de testigo de solo lectura, muestra cuándo se comprobó por última vez cada testigo y proporciona los comandos y opciones para ejecutar uno ([testigo independiente](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/)).

**La sección «Parámetros»** recoge todos los límites y ritmos del espacio de trabajo que no figuran en otras páginas: el número de diálogos leídos, la frecuencia con la que se vuelve a leer la lista de chats, los intervalos de latido y de puntos de control, el búfer de inicio, cómo se distribuyen las solicitudes en las revisiones (primer retraso, chats por paso, pausa entre chats, mensajes recuperados y solicitados de nuevo), reserva de disco, tiempos de espera y reintentos de descargas, qué buscan los perfiles de usuario (incluidas sus propias expresiones regulares), tamaño y frecuencia de las notificaciones, límites de instantáneas, archivos ZIP y descargas en el navegador, así como los tiempos de espera y reintentos del cliente de Telegram. Cada campo muestra su rango y su valor por defecto; los campos modificados quedan marcados y pueden restablecerse uno a uno o todos a la vez. Cada cambio se registra como «`parameters.changed`» con los valores anteriores y posteriores, y los registros de inicio de observación indican los valores vigentes. Los valores se aplican a partir de su próximo uso; los tiempos de espera y los reintentos del cliente, a partir de la próxima conexión. Los intervalos de revisión, los tipos y tamaños de archivos adjuntos, así como los intervalos de copia de seguridad y copia externa permanecen en sus propias páginas y pueden adoptar cualquier valor dentro de su rango, no solo los preestablecidos.

La campana de la barra superior muestra los problemas y cambios recientes en los chats supervisados; los mensajes no leídos se contabilizan hasta que se marcan como leídos. Los cambios se agrupan por chat y por hora («12 eliminados, 1 editado, 0 no encontrados»), y los problemas, como un cierre de sesión o un disco lleno, permanecen en la lista independientemente de lo activos que estén los chats.

**La creación de la cuenta** comienza en el campo del número de teléfono. **Al continuar**, se accede directamente a la introducción del código, solicitándose las credenciales de la API únicamente cuando faltan. El código QR y la importación de archivos son pestañas alternativas. Las credenciales de la API guardadas solo se reutilizan dentro de su propio espacio de trabajo. La pantalla de inicio no incluye barra lateral, estadísticas ni apartados de configuración. El icono de **«Configuración»** abre los controles de API, proxy, almacenamiento y cuentas adicionales. Las nuevas instalaciones comienzan aquí; las cuentas conectadas sin fuentes seleccionadas comienzan en **«Elegir chats**». Cambiar la ruta requiere una observación pausada y cancela cualquier inicio de sesión no finalizado. Un registro existente no puede vincularse de forma silenciosa a una cuenta de Telegram diferente.

**La exportación** comprueba la integridad del registro y genera archivos portátiles. Su identificador de espacio de trabajo puede introducirse en la línea de comandos de descarga. Cada exportación asigna un prefijo al registro completo; los eventos posteriores se incluyen en una exportación siguiente. Los filtros de búsqueda no modifican el ámbito del paquete. La información detallada sobre la firma y la cobertura se encuentra en la sección **«Verificación y limitaciones**».

El panel muestra el estado del recopilador, los archivos multimedia en cola o fallidos, los archivos multimedia pendientes más antiguos, el espacio libre en disco, las pausas en las solicitudes y las fuentes cuyo acceso no está confirmado en **la sección «Estado del recopilador**». Estos detalles aparecen inicialmente ocultos y se ocultan en la pestaña «Cuenta». Una ficha de configuración muestra el siguiente paso: conectar una cuenta, elegir fuentes o iniciar la observación. La lista de cuentas es una instantánea en el momento de la carga; el espacio de trabajo seleccionado se actualiza periódicamente. No se trata de un monitor de SLA multiproceso.

La interfaz de usuario utiliza recursos locales y renderización de texto para el contenido original. Se han probado los diseños para ordenador de sobremesa y los diseños estrechos basados en Chromium. No se trata de una certificación completa de accesibilidad; la evaluación de la usabilidad con lectores de pantalla y la evaluación de la usabilidad por parte de usuarios humanos siguen siendo tareas independientes.

## Entornos de implementación

| Entorno | Instalación | Estado de la verificación |
| --- | --- | --- |
| PC/servidor con Windows | Python 3.11 o superior, scripts\Setup.cmd/Start.cmd, directorio de datos privado | Comprobado localmente en Windows/Python 3.12 |
| Servidor Linux/VPS | Entorno virtual de Python (venv), usuario de servicio dedicado, HTTPS/SSH | Se proporcionan ejemplos de código, CI y systemd; no se ejecutan en este servidor. |
| macOS | Entorno virtual de Python (venv), proceso en primer plano o agente de usuario | Se proporciona un ejemplo de «launchd»; es necesario realizar una comprobación de instalación por separado. |
| Docker/Compose | Volumen constante, un trabajador | Se proporcionan la definición y la comprobación de tiempo de ejecución de la infraestructura de código (CI); Docker no está disponible localmente. |
| Navegador del móvil | Acceda al panel protegido en un servidor en funcionamiento | Se ha probado un diseño estrecho basado en Chromium; el recopilador no funciona en iOS ni en Android. |

La portabilidad implica que no es obligatorio utilizar un servicio en la nube ni crear una interfaz de usuario. Cada sistema de destino sigue necesitando dependencias compatibles de Python y criptografía, así como acceso al disco local y a la red. Consulte [el archivo DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/deployment/) y [las plantillas de servicio](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md).

Los espacios de trabajo comparten CPU, memoria y un bucle de eventos. Para aislar los procesos, utilice instancias, puertos, directorios de datos y autorizaciones de cuenta distintos. No existe un panel unificado para las distintas instancias. Nunca asigne varios trabajadores a una misma base de datos.

## Comprobaciones iniciales y exportaciones

Ejecute «`python start.py --check`» antes de iniciar un entorno preparado. Añada «`--json`» para comprobaciones legibles por máquina o introduzca los valores previstos para «`--data-dir`», «`--host`» y «`--port`». El comando comprueba los requisitos previos sin necesidad de iniciar sesión en Telegram ni de crear un registro. No verifica el registro ni comprueba que esté listo para la captura; la verificación del registro se lleva a cabo durante el inicio de la aplicación. Un puerto ocupado puede deberse simplemente a la existencia de una instancia previa.

Los navegadores compatibles con la API de acceso al sistema de archivos guardan las exportaciones a través de un flujo escribible. Otros navegadores almacenan en el búfer un máximo de 128 MiB. Utilice la CLI de streaming para exportaciones de mayor tamaño o para navegadores que no admitan streaming de archivos:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Añada «`--profile ID` » desde «Exportaciones» para un espacio de trabajo secundario. Utilice «`--url https://server` » para el acceso remoto. Solo se acepta HTTP sin cifrar para destinos de bucle invertido. El token se lee de un archivo y se envía en un encabezado; no se muestra ni se incluye en una URL. No se admiten redireccionamientos. Los destinos existentes no se sobrescriben. Las transferencias fallidas eliminan su archivo parcial temporal. El SHA-256 indicado es una suma de comprobación de la transferencia; verifique el archivo ZIP firmado por separado con una huella digital o un punto de control de confianza.

## Copias de seguridad, restauración e interrupciones

1. Pause la observación y detenga el proceso de forma limpia.
2. Copie todo el directorio de datos: bases de datos, WAL/SHM si existen, archivos multimedia, `credentials.enc`, `signing.enc`, `network.enc`, claves y metadatos del almacén, token, puntos de control y todos los directorios `profiles/`.
3. En el modo de clave externa, conserve por separado la clave maestra y guarde cada `vault.external.json`. La generación de una nueva clave no permite recuperar los secretos anteriores.
4. Restaure mientras el destino está detenido; configure la clave original, restrinja el acceso y verifique la integridad antes de reanudar.
5. Registre los periodos de inactividad y los resultados de la verificación. Una instantánea del historial no puede demostrar que no se produjeran eliminaciones durante la interrupción.

Los archivos ZIP de pruebas excluyen las claves de sesión y las claves privadas, y no constituyen copias de seguridad completas del servicio. Hay cuatro elementos que se protegen de forma diferente:

| ¿Qué? | Protección |
| --- | --- |
| Archivos exportados sin contraseña (predeterminado) | No está cifrado. Está firmado, por lo que los cambios son detectables, pero cualquier persona que tenga el archivo puede leerlo. |
| Archivos exportados con contraseña | Si establece una contraseña, la exportación final se guarda sin modificaciones en un archivo ZIP con cifrado AES-256 de WinZip que pueden abrir tanto 7-Zip como WinRAR; la contraseña no se almacena ([manejo de pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/)). |
| La base de datos del registro y los archivos adjuntos guardados en el disco | No está cifrado por TgWitness; utilice un disco o volumen cifrado |
| Sesiones de Telegram y claves de firma | Cifrado en el directorio de datos (`credentials.enc`, `signing.enc`, `network.enc`) |

Una copia de seguridad completa es el directorio de datos congelados descrito anteriormente, no una exportación. Utilice almacenamiento protegido y un mecanismo de transferencia controlado para ambos. Las exportaciones temporales del servidor se almacenan en el directorio « `temporary-exports/`» de cada espacio de trabajo; las respuestas completadas se eliminan, y los archivos de exportación interrumpidos se eliminan en el siguiente inicio, mientras se mantiene el bloqueo de la instancia de ese espacio de trabajo.

Un evento de restablecimiento de la conexión no garantiza la recuperación de los cambios intermedios. Las tareas de medios persistentes y la posición de actualización de Telegram se conservan tras el reinicio; véase [el formato de las pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#durable-collection-and-process-receipts-02).

## Capacidad y retención

Límites predeterminados, todos modificables en **«Parámetros**»: los primeros 1.000 diálogos, 500 mensajes por instantánea, 4 GiB de contenido ZIP firmado sin comprimir (los archivos más grandes requieren `verify.py --max-gib N`) y un límite de 128 MiB para el modo de navegador. Los archivos adjuntos ocupan entre 1 y 2.000 MiB por tipo en **«Fuentes» → «Archivos adjuntos**». La CLI de descarga tiene un valor predeterminado de 5 GiB transferidos. El espacio disponible en disco puede constituir un límite inferior. Reserve espacio para registros, archivos multimedia, WAL, exportaciones temporales y copias de seguridad. Las exportaciones utilizan el volumen de datos en lugar de los 512 MiB de «`/tmp`» de Compose.

Mida los eventos por segundo, la antigüedad de la cola, los bytes de archivos multimedia y la latencia del disco, en lugar de limitarse a contar solo los grupos. Las pruebas de rendimiento locales sintéticas no garantizan la entrega de mensajes en Telegram. No existe una eliminación automática de los datos retenidos. La eliminación de la parte final de un registro invalida su relación con los puntos de control retenidos.

Ya existen revisiones prioritarias: las fuentes marcadas con estrella se revisan cada 15 minutos de forma predeterminada, las demás, cada 6 horas (véanse [los niveles de revisión](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/#recheck-tiers)). Existen exportaciones protegidas con contraseña, tal y como se ha descrito anteriormente. La aceptación en tiempo real de Telegram/proxy, la reproducción duradera, el registro de administración y el sondeo de reacciones, los trabajadores aislados, el cifrado del registro local y los archivos multimedia por parte del propio TgWitness, así como la revisión independiente, siguen siendo tareas independientes. El acceso restringido se documenta en [«Acceso y permisos](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/)». Consulte [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md), [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) y [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/).
