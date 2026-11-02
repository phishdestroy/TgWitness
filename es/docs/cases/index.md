# Investigue en todos los chats

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/cases/

Trabaje en un caso completo a través de canales, grupos, chats privados y bots: recopile, relacione, reconstruya y entregue las pruebas.

Este tutorial sigue un incidente ficticio a lo largo de todo el proceso. Utiliza las funciones de recopilación, búsqueda y perfiles de personas para encontrar los registros originales; [el «Case Board»](https://phishdestroy.github.io/TgWitness/es/docs/case-board/) para organizarlos y analizarlos, y [el «Report Studio»](https://phishdestroy.github.io/TgWitness/es/docs/reports/) para presentar los resultados. El mapa ilustrado a continuación explica las conexiones de este ejemplo.

CASO RESUELTO / UN DESTINO DE PAGO MODIFICADO

### Un incidente. Cuatro conversaciones. Un rastro que reconstruir.

Un anuncio en un canal remite a un bot. Un grupo de operaciones debate sobre un nuevo enlace de pago y el bot lo muestra. Se edita el anuncio, un mensaje privado de seguimiento repite el destino y un mensaje de grupo desaparece.

¿Quién publicó cada versión?¿Dónde apareció el enlace?¿Qué archivo se conservó?¿Qué ha cambiado y cuándo?

Para la carga del historial, la revisión opcional de fuentes mediante IA, MCP, OCR y webhooks salientes, consulta [«Trabajar con el archivo](https://phishdestroy.github.io/TgWitness/es/docs/archive/)».

## 1. Establecer una cobertura que abarque toda la cuenta

Utiliza una cuenta de recopilación específica para el alcance de toda la cuenta. Las cuentas principales pueden recopilar chats seleccionados o una carpeta de Telegram.

1. [Conecte la cuenta de recopilación](https://phishdestroy.github.io/TgWitness/es/docs/accounts/) en su propio espacio de trabajo. Anote la referencia del caso, el ID de la cuenta, el nombre del espacio de trabajo y la huella digital de la clave de firma en sus notas del caso.
2. **Fuentes** abiertas **→ Ámbito de observación → Modo de investigación**. Revise **toda la cuenta**, los cuatro tipos de fuentes y **las acciones propias**. Esta configuración preestablecida permite guardar el perfil de una nueva fuente y sus últimos **200 mensajes visibles**. Pulse **«Guardar ámbito»** y complete la confirmación del ámbito.
3. Pulse **«Cargar chats**». Compare las fuentes con la lista de diálogos de la cuenta y revise las exclusiones. En **«Parámetros» → «Chats leídos de la lista de la cuenta**», ajuste el límite inicial de la lista si es necesario: el valor predeterminado es de 1.000 diálogos, configurable hasta 20.000. Los chats que superen el límite se detectarán cuando se activen.
4. En **la configuración de grabación**, seleccione y guarde **«Toda la actividad visible**». Revise los tipos de archivos adjuntos, los límites de tamaño y el espacio libre en disco. Inicie la observación y valide un mensaje, una edición y una eliminación controlados antes de dar por válida la configuración.

CanalesGruposChats privadosBots

UNA CUENTA / UNA CLAVE DE FIRMA**Toda la actividad visible de las cuentas seleccionadas → un único registro**

Mensajes · modificaciones · avisos de eliminación · reacciones visibles · eventos relacionados con la pertenencia al grupo · acciones propias

La opción «Cuenta completa» abarca los chats a los que esta cuenta tiene acceso, con los tipos de fuentes y las exclusiones configuradas. Los chats secretos no están disponibles. Se añaden nuevos diálogos a medida que llegan las actualizaciones; al activar este modo no se descarga automáticamente el historial completo de todos los chats existentes.

## 2. Obtener el historial y conservar los archivos

Crea una colección en el «Case Board» para la investigación y marca como favoritos los registros guardados pertinentes. Mantén un registro de fuentes junto con el caso: el identificador numérico de cada chat, el título, la cuenta de recopilación, el acceso/rol, el inicio en tiempo real, la adquisición del historial, el resultado multimedia y las lagunas conocidas. Marca una fuente como adquirida tras comprobar el resultado correspondiente.

| Se necesita | Acción en el panel | Qué ofrece |
| --- | --- | --- |
| Historial de los chats habilitados | Fuentes → Cargar historial completo | Los mensajes anteriores disponibles se incorporan al diario del espacio de trabajo, con funciones de pausa/reanudación y un informe de progreso firmado. [Guía del historial](https://phishdestroy.github.io/TgWitness/es/docs/reference/history/). |
| Contexto del chat existente en el registro | Fuentes → Ajustes de grabación → Instantánea del historial | Los mensajes visibles recientes aparecen como observaciones firmadas. El límite máximo por defecto es de 500; en **«Parámetros» → «Instantánea de historial más grande»** se puede aumentar hasta 10 000. |
| Historial completo, tal y como se muestra actualmente, de un chat | Exportación completa del chat → Exportar el chat completo, o Chats → Exportar chat | Un paquete firmado independiente con `chat.json` y `chat.html`. Repita el proceso por cada fuente; conserve los resultados de éxito o fracaso. |
| Contexto en el que aparece un nuevo chat | Ámbito de observación → Cuando aparece un nuevo chat o un nuevo bot | Un perfil de la fuente y hasta 1.000 mensajes recientes visibles; el modo de investigación selecciona 200. Los chats existentes no reciben esta recopilación de forma retroactiva. |
| Tamaño del archivo adjunto | Descarga de archivos adjuntos visibles + límites por tipo | Compruebe el código `media.saved`, su SHA-256 y el recuento de bytes. Una descarga en cola, omitida o fallida no se considera un archivo conservado. |

Una exportación completa del chat es una instantánea independiente; no importa todo su historial al registro ni a los perfiles de los usuarios. Utiliza la opción **«Cargar historial completo** de todas las fuentes habilitadas» o instantáneas delimitadas del registro para el material histórico que necesites buscar dentro de TgWitness. Revisa la lista de fuentes antes de iniciar la ejecución.

En el caso analizado, recopile el canal de anuncios, el grupo de operaciones, la conversación con el bot y el seguimiento privado. Conserve los bytes y el hash del archivo adjunto de la factura. El historial disponible en la actualidad no permite reconstruir un mensaje eliminado antes de su captura ni una modificación intermedia que Telegram ya no devuelva.

## 3. Mantenga el hilo de la conversación y sus propias acciones

Mantenga la observación en marcha a medida que se desarrolla el caso. Marque con una estrella los chats activos del caso como fuentes prioritarias; configure las revisiones de fuentes prioritarias y de otras fuentes en **Ajustes de grabación → Revisión**. Revise `recheck.completed`, la puesta al día continua, FloodWait y los resultados multimedia a medida que avanza el trabajo.

Utilice **Chats → Perfil → Guardar perfil ahora** para conservar las descripciones actuales de las fuentes, los comandos del bot y otros metadatos que proporciona Telegram. Este perfil de fuente es independiente de los perfiles de personas creados a partir de los mensajes del registro.

**Seguir a un bot o aceptar una invitación como parte del caso**

1. En **«Chats» → «Abrir enlace de Telegram»**, guarde primero la vista previa. El enlace original y la vista previa obtenida se convierten en registros firmados.
2. Si la investigación lo requiere, **la orden «Join / open» permite** acceder a la fuente e inicia un bot con el parámetro de inicio proporcionado. Una solicitud de acceso pendiente permanece como tal en el registro.
3. Para documentar una acción, utilice la respuesta de texto del panel o el control **«Pulsar botón»** compatible. El registro conserva `interaction.requested` y `interaction.result`, incluyendo el texto o la URL de la respuesta recibida.

Estos controles realizan acciones reales en Telegram. Una llamada de retorno pulsada en otra aplicación de Telegram no es visible para el recopilador; sin embargo, el mensaje o la modificación posteriores del bot sí pueden serlo. Las aplicaciones web, los pagos y las solicitudes de número de teléfono o ubicación quedan fuera del minicliente.

## 4. Realice un seguimiento de personas, enlaces y archivos en los distintos chats

1. Abre **el «Diario»**, deja el filtro de fuentes en **«Todas las fuentes»** y busca una frase distintiva, un dominio, un nombre de usuario o un identificador guardado. Abre cada registro que coincida y, a continuación, selecciona **«Añadir al panel»** para conservar su chat, el ID del mensaje y la referencia del diario en el caso.
2. Para acceder a un chat concreto, abra **«Chats» → «Personas» → «Activar perfiles»** y, a continuación, seleccione una persona. Revise el historial de nombres y nombres de usuario, las relaciones de respuesta, la actividad, así como **«También en…»:** otros chats observados y enlaces extraídos, carteras o números de teléfono. Abra los registros del diario citados.
3. Sigue el mismo ID numérico de usuario de Telegram en otros chats de este espacio de trabajo. Considera un nombre coincidente, una mención a un monedero o un avatar similar como una pista que hay que comprobar; conserva las referencias a las fuentes y cualquier atribución que las respalde.
4. Compare los valores SHA-256 de los archivos adjuntos conservados entre los distintos registros. La coincidencia de los hash garantiza la identidad a nivel de byte de los archivos guardados. Examine los registros asociados del mensaje y del remitente antes de llegar a una conclusión sobre quién los compartió.

MAPA DEL CASO / SIGA LAS REFERENCIASCaso ficticio · no es un gráfico en tiempo real

CANAL / ANUNCIO**Original → destino editado**

Registros n.º 101, n.º 188; mensaje n.º 84 · remitente no identificado

GRUPO / OPERACIONES**El usuario 71001 publica el nuevo enlace**

Registro n.º 146 · mensaje n.º 309. Acuse de recibo del archivo guardado n.º 151

BOT / CONVERSACIÓN SOBRE PEDIDOS**Un botón le lleva a ese destino**

Registro n.º 173 · mensaje n.º 12: Metadatos del botón «Volver»

PRIVADO / SEGUIMIENTO**El usuario 71001 repite el destino**

Registro n.º 205 · mensaje n.º 922. Recibo de archivo guardado n.º 209

Cuatro chats aportan diferentes observaciones. Sigue los registros originales de cada conexión; la publicación del canal no tiene remitente identificado.

Los identificadores numéricos y las referencias de los registros son ficticios para este tutorial. Este mapa explicativo muestra cómo relacionar los resultados de búsqueda, los perfiles y los registros inspeccionados; el «Case Board» almacena las fichas correspondientes y las referencias a las fuentes.

| Conexión | Observación complementaria | Conclusión: mantener |
| --- | --- | --- |
| La misma cuenta de Telegram | ID de usuario 71001 en el grupo n.º 146 y en el chat privado n.º 205 | En ambos chats aparece el mismo identificador de remitente facilitado. La identidad en el mundo real sigue siendo una cuestión aparte. |
| Destino repetido | `pay.example.invalid/new` en el n.º 146, metadatos del botón en el n.º 173, publicación editada en los n.º 188 y 205 | El mismo destino aparece en cuatro contextos observados. Atribuye su control utilizando fuentes adicionales. |
| Mismo número de bytes del archivo | Valores SHA-256 completos idénticos en los recibos multimedia completados n.º 151 y n.º 209 | Los dos archivos adjuntos conservados son idénticos al byte. Los hash completos de los archivos permiten realizar la comparación. |

Los perfiles de usuario describen a los autores observados y su actividad en el *diario del* *mismo espacio de trabajo*, dentro de los chats a los que tiene acceso el usuario. Se trata de una vista de los autores observados, más que de un directorio completo de miembros. Ajusta el número de citas de apoyo en **Parámetros → Registros citados por hecho**.

## 5. Reconstruir la secuencia y señalar las lagunas

En **«Chats»**, examine las versiones guardadas y sus enlaces **al registro del «Diario» n.º…** En **«Diario»**, utilice **«Todas las fuentes»,** además de **«Modificaciones»**, **«Eliminaciones»** y **«Cobertura**». Elabore una cronología del caso utilizando tanto la fecha proporcionada por Telegram como la hora de observación del recopilador.

1. 09:00 · #101**Publicación del canal capturada**

   Se mantiene el destino original.
2. 09:12 · #146 / #151**El grupo presenta un enlace diferente**

   El usuario 71001 lo publica; se completa la descarga de un archivo adjunto.
3. 09:16 · #173**El bot muestra el mismo destino**

   Los metadatos del teclado guardados contienen el enlace.
4. 09:20 · #188**Cambios en los anuncios del canal**

   Se conservan tanto las observaciones originales como las editadas.
5. 09:24 · #205 / #209**En el seguimiento privado se repite lo mismo**

   El archivo adjunto guardado tiene el mismo SHA-256 completo que el n.º 151.
6. 09:28 · #231**Llega una notificación de eliminación de grupo**

   La observación anterior sigue siendo válida: no se facilita ni quién ha eliminado el mensaje ni la hora exacta de la eliminación.

Se incluyen ejemplos de horas de observación y referencias. Entre estas entradas hay otros registros del diario.

La secuencia del registro sigue el orden de recepción, no necesariamente el de las acciones originales en Telegram. Una instantánea del historial más antigua puede aparecer después de un mensaje en tiempo real más reciente. Mantenga bien diferenciadas las observaciones en tiempo real, las instantáneas, los mensajes recuperados, los avisos de eliminación y los casos de «ausencia en la nueva comprobación». Añada un intervalo desconocido explícito siempre que la cobertura presente una laguna; una instantánea posterior no borra dicha laguna.

## 6. Amplíe el caso a otras cuentas de recopilación

Añada un espacio de trabajo para cada cuenta distinta y repita el inventario del alcance y el historial. Registre la pertenencia o función y la huella digital de la clave de firma de cada una. Mantenga los identificadores calificados por espacio de trabajo y chat: el mismo número de mensaje no constituye un identificador global válido para todas las cuentas.

Utiliza un [grupo de cuentas](https://phishdestroy.github.io/TgWitness/es/docs/groups/) para revisar el estado operativo, compartir ajustes seleccionados y exportar las cuentas conjuntamente. El paquete de grupo conserva el diario firmado y la identidad de cada espacio de trabajo. En el caso de un canal o un supergrupo, las cuentas que cumplan los requisitos también pueden dividir una exportación del historial completo. Crea una línea temporal que abarque varias cuentas en tus notas del caso o herramientas de análisis, conservando la referencia al espacio de trabajo y al diario para cada fila.

En trabajos de mayor duración, incorpore un [testigo independiente](https://phishdestroy.github.io/TgWitness/es/docs/witness/) para mantener los límites establecidos anteriormente. Utilice el programa piloto de entrega controlada para validar las rutas de captura y la visibilidad de las cuentas.

## 7. Entregar un paquete de caso verificable

Exporte un archivo ZIP del registro firmado desde cada espacio de trabajo. Este contiene el registro completo, independientemente de los filtros de búsqueda del panel. Exporte por separado los perfiles de las personas relevantes, conserve cada paquete completo del historial de chat y mantenga las pruebas completas de los archivos adjuntos.

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

Conserve las huellas digitales de confianza a través de un canal independiente. Desde una instalación de confianza, verifique cada artefacto comparándolo con la identidad de su propio espacio de trabajo:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Comprueba los resultados del verificador, conserva los originales y guarda el informe de cobertura, los resultados de la adquisición y el registro de transferencia junto con tus conclusiones. Redacta las conclusiones en Report Studio y decide si el informe incluye material de Case Board. La carpeta de nivel superior del ejemplo combina los artefactos firmados por separado. Para un destinatario que solo necesite material seleccionado, prepara una [entrega reducida](https://phishdestroy.github.io/TgWitness/es/docs/handover/).

## Utilice el mismo método para otras investigaciones

**Una disputa sobre un pedido o un pago gestionada por un bot**

**Pregunta:** ¿qué prometía el bot, qué destino se indicaba en el botón y qué cambió posteriormente?

**Rastreo:** publicación de entrada en el canal → vista previa del enlace del bot guardado → parámetro de inicio del bot → mensajes y versiones de teclado → cualquier acuse de recibo emitido por el panel → seguimiento en grupo o privado. Asigne cada destino a su registro de origen; conserve las descripciones de los perfiles y los archivos multimedia completos.

**Se debe entregar:** una cronología de la oferta observada y las respuestas, las referencias de las fuentes y las exportaciones verificadas. Se debe respaldar cualquier afirmación sobre un pago completado con sus propios registros de transacción.

**Mensajes eliminados tras un incidente entre chats**

**Pregunta:** ¿qué se había observado ya antes de que desaparecieran los mensajes relevantes?

**Rastreo:** todos los chats afectados → mensajes originales → modificaciones entregadas → avisos de eliminación o resultados posteriores de «no encontrado» al volver a comprobar → archivos adjuntos conservados → cobertura en torno al incidente. Compare las observaciones de cuentas independientes con la visibilidad indicada.

**Se debe reflejar:** una secuencia de versiones conservadas e intervalos desconocidos explícitos. Mantén por separado los avisos de eliminación, las revisiones fallidas y cualquier atribución a una persona.

**Un participante cambia de nombre en varios chats**

**Pregunta:** ¿qué actividad observada pertenece a la misma cuenta de Telegram a pesar de que haya cambiado de nombre?

**Rastreo:** identificador numérico del remitente → historial de nombres/nombres de usuario guardados → respuestas → otros chats en el espacio de trabajo → destinatarios mencionados y archivos guardados. Compruebe los registros de origen de cada conexión identificada; mantenga separadas las cuentas similares.

**Resultado esperado:** una cronología de la actividad de la cuenta con referencias y hipótesis separadas sobre las relaciones. Utiliza la similitud de nombres y el pHash del avatar para seleccionar pistas que justifiquen un análisis más detallado de las fuentes.
