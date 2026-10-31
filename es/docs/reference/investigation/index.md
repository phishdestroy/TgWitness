# Modo de investigación

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/investigation/

Investigaciones de cuentas completas en canales, grupos, chats privados y bots, desde la definición del alcance hasta la elaboración de un expediente de caso verificado.

Siga un caso a través de canales, grupos, chats privados y bots, desde la adquisición inicial hasta una cronología referenciada y un traspaso verificable. La versión interactiva del sitio web se encuentra en `/docs/cases/`; consulte [las instrucciones de vista previa](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

## Caso práctico: un cambio de destino a lo largo de cuatro conversaciones

Un anuncio hace referencia a un bot. Un grupo operativo debate sobre un nuevo destino de pago, el teclado del bot lo muestra y un mensaje privado de seguimiento lo repite. A continuación, el anuncio se edita y un mensaje del grupo desaparece.

Las preguntas son: ¿qué se observó antes y después del cambio?, ¿qué cuentas de Telegram publicaron cada elemento?, ¿dónde apareció el destino?, ¿qué bytes de los archivos adjuntos se conservaron? y ¿qué intervalos siguen sin conocerse?

Todos los nombres, identificadores, horas y referencias del registro que aparecen en este ejemplo son ficticios. El flujo de trabajo utiliza las funciones actuales; el mapa del caso es una ilustración, no un gráfico automático generado por la aplicación.

Diagrama de flujo · Canales → Registro del espacio de trabajo; Grupos → Registro del espacio de trabajo; Chats privados → Registro del espacio de trabajo; Bots → Registro del espacio de trabajo; Registro del espacio de trabajo → Buscar en todas las fuentes; Registro del espacio de trabajo → Perfiles de personas con referencias a los registros; Registro del espacio de trabajo → Versiones guardadas y confirmaciones de recepción de archivos adjuntos; Buscar en todas las fuentes → Cronología del analista y registro de fuentes; Perfiles de personas con referencias a los registros → Cronología del analista y registro de fuentes; Versiones guardadas y confirmaciones de recepción de archivos adjuntos → Cronología del analista y registro de fuentes; Registro del espacio de trabajo → Archivo ZIP de pruebas firmadas; Cronología del analista y registro de fuentes → Traspaso de casos con pruebas verificadas por separado; Archivo ZIP de pruebas firmadas → Traspaso de casos con pruebas verificadas por separado · Canales · Grupos · Chats privados · Bots · Registro del espacio detrabajo · Buscar en todas lasfuentes · Perfiles de personas conreferencias a losregistros · Versiones guardadas yconfirmaciones derecepción de archivosadjuntos · Archivo ZIP de pruebasfirmadas · Cronología del analista yregistro de fuentes · Traspaso de casos conpruebas verificadas porseparado

**Diagrama en formato de texto**

1. Canales → Registro del espacio de trabajo
2. Grupos → Registro del espacio de trabajo
3. Chats privados → Registro del espacio de trabajo
4. Bots → Registro del espacio de trabajo
5. Registro del espacio de trabajo → Buscar en todas las fuentes
6. Registro del espacio de trabajo → Perfiles de personas con referencias a los registros
7. Registro del espacio de trabajo → Versiones guardadas y confirmaciones de recepción de archivos adjuntos
8. Buscar en todas las fuentes → Cronología del analista y registro de fuentes
9. Perfiles de personas con referencias a los registros → Cronología del analista y registro de fuentes
10. Versiones guardadas y confirmaciones de recepción de archivos adjuntos → Cronología del analista y registro de fuentes
11. Registro del espacio de trabajo → Archivo ZIP de pruebas firmadas
12. Cronología del analista y registro de fuentes → Traspaso de casos con pruebas verificadas por separado
13. Archivo ZIP de pruebas firmadas → Traspaso de casos con pruebas verificadas por separado

## 1. Defina el caso y recopile toda la información

1. Conecte la cuenta de recopilación en su propio espacio de trabajo. En las notas externas del caso, registre la referencia del caso, el ID de la cuenta, el espacio de trabajo, la fecha de inicio de la observación y la huella digital de la clave de firma de confianza.
2. **Fuentes** abiertas **→ Ámbito de observación → Modo de investigación**. La configuración predeterminada selecciona **«Cuenta completa»**, canales/grupos/chats privados/bots, acciones propias, perfiles de origen y los últimos 200 mensajes visibles de las fuentes recién descubiertas. Revíselo, pulse **«Guardar ámbito**» y complete la confirmación del ámbito.
3. **Cargue los chats** y compare las fuentes con la lista de diálogos de la cuenta. Compruebe las exclusiones. **El parámetro «Chats leídos de la lista de la cuenta»** tiene un valor predeterminado de 1.000 y admite hasta 20.000. Las fuentes que superen el límite de la lista se añaden cuando se activan. Registre lo que realmente se haya enumerado.
4. En **la configuración de grabación**, seleccione **«Toda la actividad visible»** y guarde la configuración de supervisión. Revise los tipos y límites de archivos adjuntos, así como el espacio libre en disco.
5. Inicie la observación. Valide un nuevo mensaje controlado, así como su edición y eliminación, y a continuación conserve las referencias de la prueba y cualquier error que se produzca.

El alcance de toda la cuenta registra la actividad visible en la cuenta dentro de la configuración guardada. No accede a los chats secretos ni se une automáticamente a todos los grupos vinculados. Tampoco recopila retrospectivamente todas las conversaciones existentes. Consulte [el alcance de la recopilación](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account).

## 2. Realice un inventario de todas las fuentes y recopile el contexto histórico

Mantenga un registro de fuentes con una fila por cada chat:

| Campo | Registrar |
| --- | --- |
| Identidad | Espacio de trabajo, ID de cuenta, ID numérico del chat, título y tipo |
| Visibilidad | Afiliación/función, acceso confirmado o no confirmado, exclusiones |
| Captura en tiempo real | Fecha de inicio, tipos de eventos seleccionados y cambios posteriores en la política |
| Historial del registro | Instantáneas solicitadas/realizadas, límite, hora y referencias de los registros |
| Historial completo | Nombre del archivo de exportación firmado por chat, límites y estado de finalización o error |
| Archivos adjuntos | Recibos de archivos multimedia completados, hash, tamaños y resultados omitidos o fallidos |
| Ámbito de aplicación | Interrupciones del servicio, capturas incompletas, FloodWait, mensajes no disponibles y otras lagunas |

Utilice el método de adquisición adecuado para cada fuente:

- **La opción «Cargar historial completo** en **fuentes**» (`main` actual) carga los mensajes anteriores disponibles de las fuentes habilitadas en el registro del espacio de trabajo. Admite la función de pausa/reanudación y un informe de progreso firmado. Véase [«Adquisición del historial](https://phishdestroy.github.io/TgWitness/es/docs/reference/history/)».
- **La instantánea del historial** guarda los mensajes visibles recientes en el registro de observación. Su límite máximo por defecto es de 500; **en Parámetros → Instantánea de historial más grande** se puede aumentar esa cifra hasta 10 000. Se trata de observaciones del historial actual, no de ediciones reconstruidas.
- **Exportación completa del chat → «Exportar chat completo**», o **«Chats» → «Exportar chat**», extrae el historial actualmente visible de un chat y lo guarda en un paquete independiente firmado `chat.json` / `chat.html`. Repita este proceso con las fuentes del caso y conserve cada resultado.
- **Cuando aparece un nuevo chat o bot,** se puede guardar su perfil y hasta 1.000 mensajes recientes; el modo de investigación selecciona 200. Los chats existentes no reciben esa recopilación de forma retroactiva cuando se activa el modo.
- **La descarga de archivos adjuntos visibles** conserva los bytes según la política configurada. Se requiere un recibo `media.saved` completo con SHA-256 y recuento de bytes. Un trabajo en cola, una miniatura o un nombre de archivo no constituyen el archivo adjunto conservado.

Una exportación completa del chat **no** rellena el registro ni los perfiles de los usuarios con todos sus mensajes. Utiliza **«Cargar historial completo»** o «instantáneas delimitadas del registro» para el historial que necesites analizar dentro de TgWitness. Revisa la lista de fuentes habilitadas antes de iniciar una ejecución del historial. Ninguna de estas opciones recupera material que Telegram ya no devuelve.

## 3. Conservar la evolución del caso y las interacciones deliberadas

Marque los chats de casos activos como fuentes prioritarias. Revise los intervalos de reverificación, la puesta al día continua y los resultados multimedia. Mantenga el recopilador en funcionamiento mientras utiliza la cuenta. Utilice **Chats → Perfil → Guardar perfil ahora** para conservar los metadatos de origen, tales como descripciones y comandos de bot. Esto es independiente de los perfiles de personas derivados de los mensajes guardados.

Cuando el caso implique el seguimiento de una fuente o la interacción con un bot:

1. **Abrir enlace de Telegram → Guardar vista previa:** registra el enlace facilitado y la vista previa mostrada antes de realizar una acción.
2. **La función «Join / open and observe**» lleva a cabo la acción de unirse o abrir y envía el parámetro de inicio del bot cuando se le proporciona. Una solicitud de unión pendiente de aprobación se registra como «pendiente».
3. Las respuestas de texto emitidas por el panel y las pulsaciones de botones compatibles conservan `interaction.requested` y `interaction.result`. Los acuses de recibo de devolución de llamada pueden conservar el texto de la ventana emergente devuelta, el estado de la alerta y la URL.

Se trata de acciones reales de la cuenta. Las pulsaciones de «Callback» en otra aplicación de Telegram no son visibles para el recopilador, aunque sí pueden serlo los mensajes o modificaciones resultantes. El minicliente no realiza flujos de trabajo relacionados con aplicaciones web, pagos, llamadas telefónicas ni ubicación. Para conocer el comportamiento exacto, consulte [las interacciones con los paneles](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/#act-from-the-panel).

## 4. Relacionar las observaciones entre distintos chats

En **«Journal»**, seleccione **«Todas las fuentes»** y busque el contenido registrado. Abra los registros coincidentes y anote el espacio de trabajo, el chat, el ID del mensaje, la secuencia y el hash del registro.

En un chat relevante, abra **«Personas» → «Activar perfiles»** y examine el perfil de una persona:

- Nombres o nombres de usuario observados a lo largo del tiempo y el identificador numérico de Telegram.
- Relaciones de respuesta con referencias a los registros originales.
- **También en…** otros chats de este diario del espacio de trabajo en los que escribió ese ID.
- Actividad, modificaciones y eliminaciones, así como carteras, teléfonos, nombres de usuario y enlaces mencionados.
- Metadatos de avatares guardados y avatares similares almacenados en caché, con su origen respectivo.

Abra los registros citados antes de utilizar un perfil derivado en una conclusión. Los perfiles abarcan a las personas cuyos mensajes se han guardado, no a todos los miembros del grupo. **Parámetros → Los registros citados por hecho** limitan la lista de referencias, no el recuento de actividades subyacentes. Las menciones y la similitud de avatares son pistas; no establecen la propiedad ni la identidad.

En el ejemplo práctico:

| Enlace | Registros | Observación contrastada |
| --- | --- | --- |
| La misma cuenta de remitente | Grupo n.º 146 y seguimiento privado n.º 205 | Ambos proporcionan el ID de remitente de Telegram 71001 |
| Mismo destino | N.º 146, teclado del bot n.º 173, edición del canal n.º 188, mensaje privado n.º 205 | Todos contienen `pay.example.invalid/new`; no se ha establecido la titularidad ni el control. |
| El mismo archivo guardado | Se han completado los recibos multimedia n.º 151 y n.º 209 | Los valores SHA-256 completos coinciden para los bytes conservados |
| Atribución del canal | N.º 101 y n.º 188 | No atribuya una publicación del canal al usuario 71001 sin indicar el remitente correspondiente. |

Compare los hash de los archivos adjuntos y las referencias de los mensajes asociados. Los archivos idénticos no permiten determinar quién es el creador, el reenviador o un operador común. Los nombres iguales y los avatares similares, por sí solos, no permiten vincular dos ID de Telegram a una misma persona.

## 5. Crear la línea temporal entre chats

Utilice las versiones guardadas en **«Chats»** y sus enlaces **«Registro del diario n.º…**». En **el «Diario»**, combine **todas las fuentes** con **las modificaciones**, **las eliminaciones** y **la cobertura**. Conserve tanto el `source_at`, cuando se facilite, como el `observed_at`.

| Tiempo de observación ilustrativo | Referencia | Observación |
| --- | --- | --- |
| 09:00 | Canal n.º 101 | Destino original capturado |
| 09:12 | Grupo n.º 146; medio n.º 151 | Se ha publicado un nuevo destino; descarga del archivo completada |
| 09:16 | Bot n.º 173 | El teclado señala el nuevo destino |
| 09:20 | Canal n.º 188 | Anuncio editado; se conservan ambas versiones guardadas |
| 09:24 | Privado #205; medios de comunicación #209 | El mismo ID de remitente se repite en el destinatario; se conservan los mismos bytes del archivo |
| 09:28 | Grupo n.º 231 | Se ha recibido un aviso de eliminación; se desconoce quién la ha eliminado y la hora exacta de la eliminación. |

Entre estas referencias de ejemplo se producen otros registros. Los números de secuencia ordenan las observaciones; las instantáneas del historial pueden contener fechas de origen más antiguas y llegar más tarde que los eventos en tiempo real. Distinga entre instantáneas, mensajes recuperados, avisos de eliminación y resultados de «ausente tras nueva comprobación». Marque las lagunas de cobertura como intervalos desconocidos. La adquisición posterior del historial no establece de forma retroactiva una observación ininterrumpida.

## 6. Añadir perspectivas de las cuentas sin perder su origen

Utilice un espacio de trabajo independiente para cada cuenta distinta y repita su inventario. Conserve el ID de la cuenta, la función, la huella digital de la clave de firma y las referencias de origen en cada comparación. Los números de mensaje no son identificadores globales válidos para todos los chats o cuentas.

La correlación entre espacios de trabajo se lleva a cabo en notas de casos externas o en herramientas de análisis. Actualmente, TgWitness no dispone de búsqueda global entre espacios de trabajo, cronología fusionada, gráfico de investigación ni archivo de casos combinado. La exportación de varias cuentas de **un mismo** canal o supergrupo es una operación distinta, no una fusión de los registros de las cuentas.

En el caso de trabajos de mayor envergadura, mantenga los límites con un [testigo independiente](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/). Utilice comprobaciones de entrega controladas para validar la ruta de captura y la visibilidad de cada cuenta.

## 7. Recopilar y verificar el traspaso del caso

Mantenga todo esto reunido en un directorio de casos elaborado por un analista:

| Material | Objetivo |
| --- | --- |
| Notas de caso y registro de fuentes | Pregunta, política de recopilación, acceso/funciones, conclusiones, explicaciones alternativas y lagunas |
| Cronología | En cada entrada se incluyen tanto las fechas como las referencias al espacio de trabajo, el chat, el mensaje y la secuencia. |
| Archivo ZIP de pruebas firmadas por espacio de trabajo | Registro completo, manifiesto y archivos multimedia conservados incluidos; los filtros del panel no limitan la exportación del registro. |
| Archivos de perfiles de personas firmados por separado | Las referencias derivadas se han cotejado con las pruebas correspondientes del espacio de trabajo. |
| Exportaciones completas y firmadas de chats | Captura del historial visible actual, independiente del registro de observación |
| Huellas digitales fiables y puntos de control anteriores | Identidad clave y límites del registro conservado |
| Elementos de prueba, si se ha configurado | Registro independiente, entradas firmadas y huella digital del testigo |
| Resultados de la verificación y hash de los archivos entregados | Qué se ha comprobado, qué bytes se han transferido y a quién |

Desde una instalación de confianza, con los nombres de los archivos y la huella digital real de cada espacio de trabajo:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Se conservan los resultados reales de la verificación y los artefactos originales. El directorio de casos de nivel superior, el registro de fuentes y las conclusiones de los analistas se mantienen externamente; cada artefacto de TgWitness cuenta con su propia firma y procedimiento de verificación.

## Adaptar la investigación

| Caso | Trace | Entregar |
| --- | --- | --- |
| Disputa sobre pedidos o pagos gestionada por un bot | Anuncio de entrada → vista previa del enlace guardado → parámetro de inicio del bot → versiones de mensajes y teclado → recibos de devolución de llamada del panel → seguimiento de mensajes privados y de grupo | Se ha respectado la cronología de ofertas y respuestas y se han verificado las fuentes; un enlace de pago por sí solo no constituye prueba de que se haya realizado dicho pago. |
| Mensajes eliminados tras un incidente | Todos los chats afectados → originales y modificaciones guardados → resultados de eliminación o de ausencia tras una nueva comprobación → archivos multimedia conservados → cobertura y otras perspectivas de la cuenta | Versiones conservadas e intervalos desconocidos explícitos; no se atribuye a nadie la autoría de las eliminaciones. |
| Un participante cambia de nombre en los distintos chats | ID numérico del remitente → historial de nombres/nombres de usuario → respuestas → otros chats observados → destinos/archivos citados | Una cronología de la actividad de una cuenta de Telegram citada, en la que se mantienen separadas las hipótesis sobre la identidad real y las relaciones. |

[Referencia de la recopilación](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/) · [Verificación de perfiles de personas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#people-profiles) · [Entrega de pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#investigation-handoff) · [Validación completada](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/)
