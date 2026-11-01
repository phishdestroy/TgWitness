# Cómo funciona la recopilación

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/

Ámbito de observación, actualizaciones en tiempo real, verificaciones cruzadas, archivos adjuntos, acciones propias y qué significa una laguna, registro por registro.

TgWitness registra lo que observa una cuenta de Telegram conectada. El registro conserva esas observaciones, su secuencia y el contexto que las acompaña. No infiere acciones no observadas a partir de la ausencia de un mensaje o de que una cuenta esté conectada.

## Desde el inicio de sesión hasta el registro

Diagrama de flujo · Autorizar una cuenta de usuario → Seleccione grupos y canales accesibles; Seleccione grupos y canales accesibles → Guardar la configuración de eventos y archivos adjuntos; Guardar la configuración de eventos y archivos adjuntos → Iniciar la observación; Iniciar la observación → Reciba actualizaciones del cliente activo; Reciba actualizaciones del cliente activo → Aplicar la política de fuentes y eventos; Aplicar la política de fuentes y eventos → Añada una observación firmada; Añada una observación firmada → Revisar o exportar el registro; Añada una observación firmada → Procesar cualquier archivo adjunto en cola; Procesar cualquier archivo adjunto en cola → Añada el resultado de la descarga · Autorizar una cuentade usuario · Seleccione grupos ycanales accesibles · Guardar laconfiguración deeventos y archivosadjuntos · Iniciar la observación · Reciba actualizacionesdel cliente activo · Aplicar la política defuentes y eventos · Añada una observaciónfirmada · Revisar o exportar elregistro · Procesar cualquierarchivo adjunto encola · Añada el resultado dela descarga

**Diagrama en formato de texto**

1. Autorizar una cuenta de usuario → Seleccione grupos y canales accesibles
2. Seleccione grupos y canales accesibles → Guardar la configuración de eventos y archivos adjuntos
3. Guardar la configuración de eventos y archivos adjuntos → Iniciar la observación
4. Iniciar la observación → Reciba actualizaciones del cliente activo
5. Reciba actualizaciones del cliente activo → Aplicar la política de fuentes y eventos
6. Aplicar la política de fuentes y eventos → Añada una observación firmada
7. Añada una observación firmada → Revisar o exportar el registro
8. Añada una observación firmada → Procesar cualquier archivo adjunto en cola
9. Procesar cualquier archivo adjunto en cola → Añada el resultado de la descarga

La autorización, el acceso a una fuente, un recopilador en funcionamiento y la entrega completa son cuestiones distintas. Un inicio de sesión correcto no garantiza el acceso a todos los grupos. Una conexión de transporte no garantiza que se hayan recibido todas las actualizaciones pertinentes.

## Ámbito de observación: chats seleccionados, una carpeta o toda la cuenta

Fuentes → **El ámbito de observación** determina qué chats registra un espacio de trabajo.

| Modo | Registros | Nuevos chats |
| --- | --- | --- |
| Chats seleccionados (por defecto) | Solo los chats que añada manualmente | Nunca se añade automáticamente |
| Carpeta de Telegram | Chats en una de las carpetas de la cuenta: chats incluidos por nombre, más las categorías de la carpeta (contactos, no contactos, grupos, canales, bots), menos los chats excluidos y, si así lo indica la carpeta, los chats archivados | Los chats correspondientes se añaden tan pronto como se activan; los chats que añada a la carpeta en Telegram se recogen en el plazo de una hora. |
| Cuenta completa | Todas las conversaciones que recibe la cuenta | Cada nuevo chat, grupo, chat privado o bot se añade en el momento en que se produce su primera actualización. |

- **Los tipos de fuente** (canales, grupos, chats privados, bots) delimitan los modos de carpeta y de cuenta completa. Los chats seleccionados pueden ser de cualquier tipo, incluidos los chats privados y los bots.
- **Los chats excluidos** nunca se registran, en ningún modo. En los modos «por carpeta» y «cuenta completa», las opciones *«Excluir»* y *«Eliminar»* en una fuente la incluyen en esta lista, por lo que el ámbito de aplicación no la añade de nuevo. Si vuelve a seleccionar el chat manualmente (en «Fuentes» o desde «Chats»), se elimina de la lista. La lista tiene capacidad para un máximo de 5.000 chats; si se supera ese límite, no se acepta *la opción «Eliminar»* y, en su lugar, se puede pausar el chat.
- **Acciones propias** (activadas por defecto): los mensajes que envía esta cuenta, sus modificaciones y las pulsaciones del botón del teclado de respuesta. Si se desactiva, se omiten los mensajes salientes y las modificaciones.
- Al cambiar a una carpeta o a toda la cuenta, se solicita confirmación: estos modos graban chats privados y mensajes de terceros, y deben utilizarse únicamente en una cuenta dedicada. La confirmación y cada cambio de ámbito se registran en registros firmados con `scope.changed`.
- Los chats añadidos por el filtro aparecen como fuentes marcadas *como «auto»*, registradas como `scope.applied` (al inicio y cada hora) o `source.discovered` (un nuevo chat durante la observación). Al volver a los chats seleccionados, se pausan todas las fuentes añadidas automáticamente.

Lo que estos modos no pueden hacer:

- **Los chats secretos** cuentan con cifrado de extremo a extremo entre dos dispositivos y nunca llegan a TgWitness, en ningún modo.
- **No se registra nada mientras TgWitness no esté en funcionamiento.** Tras un reinicio, solicita a Telegram las actualizaciones perdidas y vuelve a comprobar los chats, pero Telegram no devuelve toda la información tras interrupciones prolongadas. Los informes y `verify.py` muestran dichos periodos como lagunas (véase [«cobertura»](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)).
- Al inicio solo se muestran los primeros 1.000 diálogos (el límite se encuentra en **«Parámetros»**); los chats más antiguos se añaden la próxima vez que se activen. No se recupera el historial anterior de un chat añadido; realice una captura del historial o una exportación completa del chat cuando lo necesite.
- No se aplican las condiciones de las carpetas que cambian constantemente (silenciadas, leídas): dichos chats siguen siendo objeto de observación.
- **Los botones del bot integrados (de devolución de llamada)** pulsados en otra aplicación son invisibles para una segunda sesión; se registra la respuesta o la edición del bot. Las pulsaciones del teclado de respuesta llegan como mensajes salientes y se etiquetan como `button_press`.
- Un mayor número de chats implica un mayor número de solicitudes. Telegram restringe las cuentas cuyo volumen considera excesivo, lo que constituye una razón más para utilizar cuentas específicas.

## Ámbito de aplicación y selección de eventos

Cada espacio de trabajo cuenta con sus propias fuentes. TgWitness no se une a grupos, no acepta invitaciones ni enumera automáticamente a todos los miembros. Las fuentes deben estar ya accesibles para la cuenta. Al iniciarse, el recopilador compara las fuentes seleccionadas con los diálogos visibles de la cuenta; se inspeccionan los primeros 1.000 diálogos, salvo que se indique lo contrario en **«Parámetros → Chats leídos de la lista de la cuenta**». Una fuente ausente se marca como **«acceso no confirmado**», sin que se dé por hecho que le haya eliminado.

| Configuración | Recopila | Efecto cuando está desactivado |
| --- | --- | --- |
| Nuevos mensajes | Mensajes entregados normales | Es posible que las modificaciones o eliminaciones posteriores no tengan texto capturado anteriormente con el que compararlas. |
| Modificaciones | Versiones editadas de los mensajes entregadas | Los cambios intermedios no se reconstruyen posteriormente. |
| Eliminaciones | Notificaciones de eliminación con alcance específico y notificaciones a nivel de cuenta sin alcance específico | Las notificaciones de eliminación no se añaden al registro. |
| Reacciones | Instantáneas de las reacciones recabadas | No se añaden actualizaciones de reacciones por separado. |
| Afiliación | Se han enviado mensajes de servicio a los miembros y actualizaciones a los participantes | No se incluyen las observaciones de los miembros. |

La configuración se aplica a todas las fuentes seleccionadas en el espacio de trabajo. Guarde el formulario para aplicar los cambios; estos se registran con valores firmados «antes» y «después». Desactivar una categoría no elimina los registros anteriores. Volver a activarla no recupera las actualizaciones perdidas.

Los registros operativos y otros eventos del servicio de grupo permanecen independientes de estos ajustes. Los mensajes de servicio relacionados con la afiliación pueden generar registros de mensajes cuando la afiliación está habilitada, incluso si la captura habitual de nuevos mensajes está desactivada. Los objetos de Telegram capturados conservan los metadatos incrustados; un ajuste no es una regla de censura.

**Las eliminaciones en chats privados y grupos normales** se registran como identificadores de mensaje sin chat asociado. Estos chats comparten una secuencia de identificadores de mensaje válida para toda la cuenta, por lo que, cuando un mensaje con ese identificador se ha guardado anteriormente, se conoce su chat: la eliminación se registra en ese chat, y `chat_resolution` explica cómo. Los identificadores que nunca se han guardado permanecen como una **eliminación sin contexto** con una fuente explícitamente desconocida; el recopilador no hace conjeturas. Telegram nunca indica quién ha eliminado un mensaje; cuando el mensaje eliminado fue enviado por esta cuenta, el registro así lo indica (`deleted_message_was_outgoing`) sin nombrar al autor de la eliminación.

## Acciones propias

Los mensajes enviados por la cuenta observada se etiquetan como `outgoing`. Una modificación de un mensaje saliente indica que, en los chats privados y los grupos, solo su autor puede modificarlo, mientras que las publicaciones en canales pueden ser modificadas por otros administradores. Cuando un mensaje saliente repite el texto de un botón del teclado de respuesta guardado más reciente en ese chat, lleva la etiqueta «`button_press`» con un enlace al registro de dicho teclado.

La exclusión de las acciones propias también se aplica a las revisiones de antecedentes y al historial automático de nuevos chats. Los mensajes salientes omitidos adelantan la posición de revisión, de modo que no puedan bloquear los mensajes entrantes posteriores. Las acciones explícitas en el panel y las instantáneas del historial solicitadas manualmente siguen quedando registradas.

## Modo de investigación: unirse a grupos y comunicarse con bots

**Fuentes → Ámbito de observación → El modo de investigación** prepara el ámbito para una cuenta dedicada que se une a chats de equipo, inicia bots y escribe en ellos: toda la cuenta, cada tipo de fuente, las acciones propias y, para cada chat o bot que aparezca, su perfil y sus últimos 200 mensajes visibles. Revise el formulario y pulse **«Guardar ámbito»**; el cambio a toda la cuenta requiere la confirmación habitual.

- **Botones.** Los botones que aparecen debajo de un mensaje se conservan junto a él y se muestran en **«Chats**»: enlaces, aplicaciones web, enlaces de inicio de sesión, textos para copiar, datos de devolución de llamada, consultas en línea, solicitudes de un número de teléfono o una ubicación. Los enlaces se muestran como texto y el panel nunca los abre. Cuando un bot solo modifica los botones (por ejemplo, un nuevo enlace de pago), se considera una nueva versión del mensaje, tanto en las actualizaciones en tiempo real como en las revisiones posteriores.
- **Nuevos chats y bots.** En los modos «por carpeta» y «cuenta completa», **cuando aparece un nuevo chat o bot**, se guarda inmediatamente después de su aparición:

  - su perfil como registro `source.profile`: descripción del bot y comandos, el texto de «Acerca de» de un usuario, grupo o canal, miembros, chat vinculado y enlace de invitación cuando Telegram lo proporcione;
  - sus últimos mensajes visibles (hasta 1.000) como una instantánea del historial marcada con `new_chat`: los mensajes anteriores de un chat de grupo al que acaba de unirse, o lo que dijo un bot antes de que la observación detectara el chat. Los mensajes ya guardados en tiempo real no se repiten.

  Los chats que ya figuran en la lista al activar el modo se añaden sin capturas de pantalla. Una «FloodWait» interrumpe esta tarea, que se reanuda posteriormente; los fallos se registran y la grabación en tiempo real del chat continúa. - **Perfiles bajo petición. En Chats → Perfil → Guardar perfil, ahora** se guarda el perfil actual de cualquier fuente; el más reciente se muestra encima de los mensajes. - **No visible.** Los botones en línea (de devolución de llamada) pulsados en otra aplicación de Telegram, la ventana emergente o el enlace con el que un bot responde a dicha pulsación, así como los enlaces de invitación utilizados en otra aplicación, no llegan a TgWitness. Lo que el bot envía o edita posteriormente queda registrado.

### Actuación desde el panel

**La sección «Chats»** incluye ahora un minicliente que utiliza la cuenta de Telegram del espacio de trabajo seleccionado:

- Escriba un mensaje de texto sin formato o seleccione **«Responder»** debajo de un mensaje guardado. El mensaje saliente resultante se registra incluso cuando el ámbito de aplicación excluye las actualizaciones salientes.
- Pulse **el botón «Pulsar»** situado debajo de un botón de respuesta o de texto actual. El servidor vuelve a recuperar el mensaje y rechaza la acción si el texto difiere de la versión guardada. Los acuses de recibo conservan el texto emergente de Telegram, el indicador de alerta y la URL; la respuesta también se muestra debajo de la conversación. Las URL siguen siendo texto seleccionable y no se abren automáticamente.
- Expanda **el enlace «Abrir Telegram**», introduzca `@username`, un enlace público `https://t.me/name`, `https://t.me/+invite` / `joinchat/invite`, o un enlace de bot con `?start=parameter`, y pulse **«Guardar vista previa**». El enlace original y la vista previa de Telegram se firman antes de unirse. **Al unirse o abrir y observar**, se incorpora al grupo o canal, o se abre el usuario o bot, se añade el chat como fuente habilitada y se envía `/start` a un bot, incluyendo su parámetro de inicio. Una solicitud de incorporación pendiente de la aprobación del administrador se registra como «pendiente», no como «pertenencia».

Active la opción **«Iniciar observación»** para capturar las respuestas entrantes en tiempo real. Las acciones del panel funcionan mientras la observación está en pausa, pero en ese caso solo se garantiza que se guarden sus respuestas directas. Las fuentes recién añadidas utilizan la configuración de perfil e historial configurada cuando la observación está en marcha. Cuando una fuente esté en pausa, actívela en **«Fuentes»** antes de enviar mensajes o pulsar sus botones.

`interaction.preview`, `interaction.requested` y `interaction.result` son eventos habituales del registro firmados que se incluyen en las exportaciones de pruebas. Las solicitudes identifican la cuenta, el mensaje o el botón o el registro de vista previa, así como si la observación estaba en ejecución. Los acuses de recibo distinguen entre éxito, rechazo, aprobación pendiente y un resultado desconocido. Es posible que una solicitud interrumpida haya llegado a Telegram: compruebe el chat antes de iniciar una nueva acción. La reutilización de un ID de solicitud recupera su confirmación guardada sin repetir la acción, incluso tras un reinicio. El panel conserva el ID tras una respuesta ambigua para la misma acción durante la sesión de la página actual. También conserva ese ID cuando falla la actualización de la vista tras una acción realizada con éxito: la confirmación permanece visible, y al hacer clic de nuevo se recupera. Las RPC de devolución de llamada y de incorporación tienen un único intento de aplicación; las lecturas reintentables mantienen su política de reintentos configurada. Al cambiar de chat, se borran inmediatamente el borrador y el destinatario de la respuesta, y se desactiva el envío hasta que se cargue la nueva conversación.

Este minicliente gestiona botones de texto y de devolución de llamada. Las aplicaciones web, las solicitudes de inicio de sesión, de número de teléfono o de ubicación, los pagos, las consultas en línea y los archivos adjuntos siguen requiriendo un cliente de Telegram; los metadatos guardados de sus botones siguen siendo visibles. Los nuevos controles utilizan texto en inglés.

## Niveles de verificación

Las revisiones solicitan de nuevo a Telegram los mensajes que se han perdido, las modificaciones y los mensajes que ya no devuelve. Las fuentes marcadas con un asterisco son fuentes **prioritarias**, que se revisan cada 15 minutos de forma predeterminada; el resto de fuentes, cada 6 horas. Los chats seleccionados comienzan como fuentes prioritarias, mientras que los chats añadidos mediante una carpeta o la cuenta completa se consideran fuentes normales. Se vuelven a comprobar un máximo de 30 fuentes por ciclo y el resto espera al minuto siguiente; tras una reconexión, las fuentes prioritarias tienen prioridad. Ambos intervalos se configuran en Fuentes → Ajustes de grabación → Revisión (el valor 0 desactiva un nivel) y se registran como `recheck.changed`.

Los mensajes perdidos se recuperan a partir del punto en el que se detuvo la pasada anterior, con un máximo de [ **Parámetros → nuevos mensajes por nueva comprobación**] (1.000 por defecto) por pasada. Por lo tanto, tras una interrupción prolongada, la revisión vuelve a cubrir todo el intervalo perdido, incluso cuando se hayan guardado primero mensajes en tiempo real más recientes que dicho intervalo . Un chat que aún se está poniendo al día se vuelve a revisar al minuto siguiente, en lugar de esperar a que finalice su intervalo de nivel; `recheck.completed` muestra `continues_after` hasta que haya finalizado.

Las comparaciones incluyen el texto de los mensajes, las entidades, los teclados (incluida su eliminación) y el contenido o la identidad de los archivos adjuntos. El mero hecho de modificar los hash de acceso a los archivos o las referencias a los mismos no constituye una modificación, ni tampoco lo que Telegram rellena por sí mismo: la carga de una vista previa de un enlace, las visualizaciones de historias, los contenidos multimedia de pago desbloqueados por esta cuenta o la recepción de una factura. Cada versión guardada en «Chats» enlaza con su registro completo en el diario, incluidos los metadatos multimedia.

## Historial de mensajes y atribución

Supongamos que el recopilador observa «Reunión a las 10:00», posteriormente ve «Reunión a las 11:00» y, a continuación, recibe un aviso de eliminación. Se añaden tres observaciones distintas: el texto original se conserva, la modificación constituye una versión separada y el aviso registra que se ha observado una eliminación.

Si la recopilación comenzó después de que desapareciera la primera versión, dicho texto no estará disponible. Si se produjeron varias modificaciones mientras el proceso estaba fuera de línea, solo se podrán guardar las versiones observadas posteriormente. Un aviso de eliminación no permite recuperar contenido que nunca se haya capturado.

El remitente del mensaje no es necesariamente quien lo ha editado. Telegram no suele facilitar la identidad de la persona que ha eliminado un mensaje ni la hora exacta de la eliminación. Los autores desconocidos siguen sin identificarse. Las instantáneas de reacciones y las actualizaciones de los participantes contienen únicamente los recuentos y las identidades que Telegram muestra a la cuenta.

Los números de secuencia indican el orden de observación. La marca de tiempo UTC del recopilador corresponde a su reloj local; la marca de tiempo original de Telegram se almacena por separado cuando se facilita. Ninguna de ellas constituye una marca de tiempo independiente y fiable.

## Instantáneas del historial

Una instantánea solicita los últimos mensajes visibles de una fuente habilitada, hasta 500 por solicitud. Los resultados se etiquetan como observaciones del historial. Pueden solaparse con la captura en tiempo real, y las observaciones repetidas se conservan como registros independientes.

Las capturas de pantalla se ajustan a la política de archivos adjuntos, pero permanecen separadas de los cambios en tiempo real. No reconstruyen los mensajes eliminados ni las versiones intermedias perdidas. Puede solicitar una mientras la herramienta está en pausa; cualquier archivo adjunto que se haya puesto en cola esperará hasta que comience la observación y se ejecute el proceso de descarga.

## Gestión de archivos adjuntos

La descarga de archivos adjuntos está activada por defecto y se detiene cuando queda menos de 1 GiB de espacio libre en disco. El recopilador realiza simultáneamente la observación de los mensajes y la tarea de descarga. La tarea conserva el descriptor multimedia original y la política de tamaño, por lo que un archivo adjunto editado posteriormente no se sustituye de forma silenciosa.

Las descargas se ejecutan tras la captura del mensaje. Una descarga completada genera un registro `media.saved` con su SHA-256 y el recuento de bytes. Las tareas omitidas, fallidas, reintentadas e interrumpidas tienen resultados distintos. Una tarea en cola no constituye prueba de que el archivo se haya conservado. El archivo completado también debe coincidir con el recuento de bytes del descriptor del archivo adjunto original observado. Una respuesta más corta o inesperadamente más larga no se registra como contenido conservado.

Los límites se establecen **por tipo**: fotos, vídeos, GIF y animaciones, mensajes de vídeo circulares, mensajes de voz, música y audio, pegatinas y archivos. Cada tipo puede desactivarse y tiene su propio límite de tamaño, que va de 1 a 2.000 MiB; los nuevos espacios de trabajo comienzan con 20 MiB para fotos, 100 MiB para vídeos, 50 MiB para archivos, audio y vídeos circulares, 20 MiB para mensajes de voz y GIF, y 5 MiB para los stickers. Los nuevos espacios de trabajo mantienen los GIF y los stickers desactivados hasta que se activen. Los espacios de trabajo con políticas guardadas antes de la implantación de los límites por tipo mantienen todos los tipos activados y conservan su único límite para cada tipo. *El tamaño máximo de archivo* se establece para todos los tipos a la vez. Un tipo desactivado genera un registro `media.skipped`; los archivos de tamaño desconocido o que superan el límite no se descargan. Los archivos de gran tamaño disponen de tiempo de descarga adicional en función de su tamaño y de una velocidad base de 256 KiB/s. Los trabajos se mantienen tras un reinicio, pero las referencias caducadas, la pérdida de acceso o los archivos eliminados pueden seguir impidiendo la recuperación. Los trabajos en espera conservan el límite guardado con ellos, por lo que un aumento del límite solo se aplica a los archivos nuevos. Desactivar un tipo o reducir su límite también omite los archivos en espera que excluye, cada uno con un registro «`media.skipped`»; desactivar las descargas pone en pausa la cola hasta que se vuelvan a activar.

## Pausar, bloquear, desconectar y reiniciar

| Acción o condición | Efecto |
| --- | --- |
| Cambiar de espacio de trabajo | Cambia la vista del panel; los demás recopiladores mantienen su estado. |
| Bloquee el panel o cierre la pestaña | Mantiene el servidor y la observación en funcionamiento. |
| Observación de pausa | Detiene ese recopilador y conserva el trabajo de los archivos adjuntos en cola. |
| Desactivar una fuente | Desactiva la captura programada futura; las tareas multimedia en cola relacionadas con ella quedan en espera mientras esté desactivada. |
| Eliminar una fuente | Se omite como fuente y se eliminan los perfiles de sus usuarios; los registros ya guardados permanecen en el registro de solo adición. Los archivos adjuntos que aún están pendientes se registran como fallidos (`source_removed`). En los modos de carpeta y de cuenta completa, también se excluyen. |
| Modificar la ruta de conexión | Requiere una pausa, cierra los clientes antiguos y cancela los inicios de sesión no completados. |
| Detenga el proceso de Python | Detiene todos los espacios de trabajo; no se realizan observaciones mientras está desconectado. |
| Reinicio tras la observación activa | Intenta reanudar el ámbito guardado utilizando la sesión guardada. Una pausa manual anula dicha intención. |

El recopilador registra las desconexiones detectadas, los reintentos, los errores, los inicios y paradas, y los pulsos de conexión. Las interrupciones breves pueden pasar desapercibidas en las comprobaciones periódicas de conectividad. Tras un reinicio, se solicitan las actualizaciones perdidas a partir de la posición de actualización guardada y los chats observados se vuelven a comprobar periódicamente; véase [el formato de las pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#durable-collection-and-process-receipts-02). Una instantánea proporciona contexto; no demuestra que se haya subsanado una laguna.

## Aislamiento y verificación de cuentas

Cada espacio de trabajo cuenta con su propio registro, autorización, clave de firma, política y cola. Solo su cliente activo puede aportar observaciones en tiempo real. Los clientes rechazados, pendientes, sustituidos y los que realizan pruebas de conexión no pueden escribir actualizaciones en tiempo real en su registro. Diferentes cuentas pueden observar el mismo grupo, pero sus registros permanecen separados.

Cada evento incluye el hash anterior y una firma Ed25519. Las exportaciones abarcan todo el registro del espacio de trabajo mediante un número de secuencia fijo. Los filtros del panel no filtran la exportación; la recopilación puede continuar más allá de sus límites mientras se está preparando.

**El registro de verificación** comprueba la cadena de eventos y las firmas a través del límite mostrado. Su resultado se borra cuando cambia el espacio de trabajo, y el panel identifica los nuevos registros añadidos tras la comprobación. La exportación en formato ZIP también verifica los archivos multimedia recopilados.

Una firma válida garantiza la integridad en relación con la clave de confianza, no con el origen de Telegram ni con la veracidad del contenido. Conserve las huellas digitales y los puntos de control de forma independiente. Consulte el [modelo de pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/), [las operaciones diarias](https://phishdestroy.github.io/TgWitness/es/docs/reference/operations/) y [el procedimiento de aceptación en tiempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) para conocer los requisitos de confianza y entrega.
