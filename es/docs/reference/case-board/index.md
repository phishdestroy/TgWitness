# Referencia de Case Board

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/case-board/

Marcadores, resaltados exactos, fragmentos de acción, debates, acceso restringido y el historial de anotaciones firmadas que utiliza Case Board.

Case Board ofrece al equipo de investigación una vista de trabajo compartida del material guardado. Se puede marcar una observación, resaltar un pasaje concreto, guardar una serie de acciones y comentarlas con los compañeros. Las fichas conservan sus referencias de origen y el historial de revisiones firmado. Las anotaciones del equipo permanecen en el espacio de trabajo, identificables por separado de las observaciones originales de Telegram.

[Modelo de pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/) · [Acceso](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/) · [Informes](https://phishdestroy.github.io/TgWitness/es/docs/reference/case-reports/)

![Feed de investigación sintético](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

## Trabajar con un caso

Abre **Investigación → «Case Board»** en modo Estándar o Experto. El idioma se adapta al panel. Utiliza **la** **opción** **«Añadir al panel»** junto a un registro del diario o un mensaje de chat guardado, o selecciona el elemento y pulsa **B**. El marcador se añade a la Bandeja de entrada con un solo clic. Edita su título, etiquetas y nota, o muévelo a una colección. Una tarjeta modificada incluye una revisión firmada; al eliminarla se conserva el historial.

Para un primer caso, elige una recopilación y añade los registros que respondan a una pregunta. Utiliza los comentarios para revisar la interpretación y, a continuación, **la opción «Presentación»** para recorrer las fichas y el contexto de las fuentes. Selecciona el material del «Case Board» por separado en [«Report Studio»](https://phishdestroy.github.io/TgWitness/es/docs/reference/case-reports/) al preparar el informe. Guardar una sección no configura automáticamente los filtros de datos del informe.

Selecciona texto dentro de un mensaje de chat guardado para que aparezca **«Resaltar → tablero**». Selecciona su color y añade una nota. El servidor comprueba la cita exacta y la versión guardada, incluidos los emojis, el texto RTL y los signos de combinación. La interfaz no asigna una selección a través de texto enmascarado o transformado.

Pulsa Mayús + clic en dos registros de un mismo chat para **«Slice between**» (**Seleccionar entre**), utiliza **«Slice by time**» (**Seleccionar por tiempo**) o guarda los filtros actuales del diario para chat, periodo y tipo de evento. Una selección guardada tiene su propio predicado de referencia: al abrirla en el Diario, también se aplican múltiples chats, límites de número de mensajes y filtros de participantes . La opción **«Mostrar registros añadidos desde el marcador»** aísla las adiciones posteriores. Cambiar los filtros de Journal hace que se salga de la sección. Desde «Personas», la opción **«Dividir las acciones de esta persona»** utiliza el ID de actor registrado; no da por sentado que el autor del mensaje lo haya editado, eliminado o haya reaccionado a él.

El cuadro de diálogo de selección muestra una vista previa de los recuentos antes de permitir la creación. «`all`» incluye todos los tipos registrados, incluidas instantáneas, ediciones, eliminaciones, reacciones, actualizaciones de membresía o servicio, acciones propias, botones, resultados multimedia, mensajes recuperados y tipos de eventos futuros. La selección describe las observaciones guardadas. Los avisos de eliminación de chats desconocidos constituyen un contexto independiente, disponible únicamente para el acceso a todo el espacio de trabajo, y nunca se atribuyen a ninguno de los chats seleccionados.

Las colecciones tienen un ámbito de chat definido. Un ámbito vacío significa todo el espacio de trabajo. Una colección no puede contener tarjetas fuera de su ámbito; un participante con acceso limitado a un chat no puede leer una colección de ámbito más amplio. La bandeja de entrada es una colección virtual para tarjetas sin asignar. La búsqueda y los filtros abarcan únicamente las tarjetas visibles; los hilos y las menciones heredan el acceso de la tarjeta principal. Los comentarios eliminados tienen una marca de eliminación en la discusión. No se registra ningún historial de visualización.

**La «Presentación»** abre todas las fichas de la colección elegida, con las vistas «Ficha», «Contexto de la fuente» y «Comentarios del equipo», así como los controles de teclado «Anterior» y «Siguiente». No ofrece controles de edición. El feed habitual está paginado; la «Presentación» carga su lista por páginas y recupera los detalles de una ficha cada vez.

## Permisos

Todas las operaciones requieren `view`, el ámbito del espacio de trabajo/chat y `board.read`. `board.write` añade tarjetas, comentarios, movimientos y estados de «abierto»/«revisado». `board.manage` permite la gestión de la recopilación, los estados «confirmado»/«desestimado» y la revisión o eliminación de la tarjeta de otra persona. Un estado es una decisión del equipo, no el resultado de una verificación criptográfica.

Acceder a las configuraciones predefinidas de los formularios: Revisor = lectura; Analista = lectura/escritura; Operador = lectura/escritura/gestión, además de sus permisos existentes. Las autorizaciones existentes no adquieren nuevos derechos de forma implícita. El administrador principal tiene todos los derechos y publica como **«Administrador principal**». Utiliza concesiones con nombre para la atribución. Las menciones solo incluyen los accesos actuales capaces de leer la ficha principal completa.

Una autorización para el chat A no puede obtener una tarjeta o una porción para A+B, ni siquiera adivinando su ID o proporcionando un `target.chat_id` falso. Los metadatos del objetivo se resuelven a partir del hash del evento firmado en el servidor. Las recopilaciones, el recuento de comentarios, las tarjetas relacionadas y las notificaciones en tiempo real se filtran antes de la respuesta. Las exportaciones requieren tanto `export` como `board.read`; un exportador existente sin acceso al tablero obtiene el archivo de pruebas habitual sin las notas del equipo. SSE vuelve a comprobar los permisos actuales antes de cada lote.

## Contratos almacenados

Al igual que las observaciones, las anotaciones se escriben de forma transaccional en una tabla SQLite de solo apéndice en el espacio de trabajo. `annotations.jsonl` es su exportación canónica exacta a partir de la misma instantánea de lectura que `events.jsonl`. No existe un segundo almacén de anotaciones competidor ni ningún evento de registro en `board.activity`.

Cada línea debe contener exactamente:

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

El ejemplo abreviado anterior ilustra la estructura general; las cargas útiles reales incluyen sus valores predeterminados de modelo y los campos de destino resueltos por el servidor. Los esquemas de solicitud de la API se encuentran en [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json), generados a partir de los modelos Pydantic en tiempo de ejecución mediante la herramienta `python tools/build_board_schemas.py`. Se rechazan los campos de solicitud adicionales. Los ID se generan en el lado del servidor cuando se omiten. La autoría, la hora, la instantánea y la firma no pueden ser proporcionadas por el solicitante. Los ID de concesión con nombre siguen el formato hexadecimal de 16 caracteres existente de Access; los ID de tarjeta son de 32 caracteres hexadecimales.

El JSON canónico está en UTF-8, con claves de objetos ordenadas, sin espacios en blanco entre tokens, Unicode sin escapar, y sin valores NaN ni infinitos. El hash de la anotación es un SHA-256 del objeto canónico que contiene el form `format: "tgwitness-annotations-v1"` y los siete campos de la envoltura hasta `previous_hash`. Esta etiqueta de formato separa su dominio de hash de las observaciones. La firma es Ed25519 sobre los 32 bytes sin procesar del hash. La secuencia comienza en 1. Las revisiones conservan el ID de la tarjeta y nombran el hash de anotación anterior en «`supersedes`»; no pueden cambiar el ámbito del chat. Los desplazamientos, los estados y las eliminaciones son registros independientes. La tabla SQLite rechaza las órdenes UPDATE y DELETE.

`case-board.json` contiene `{statement, signature}`. La declaración canónica está firmada por la clave del espacio de trabajo y contiene `format: "tgwitness-case-board-v1"`, `public_key`, `created_at`, `journal_head`, `meaning` y `state`. El estado es una reproducción determinista: `annotations_head`, una matriz ordenada de `items` (colecciones, tarjetas, comentarios, incluidas las marcas de eliminación) y `status_history`. Los elementos conservan el hash de su última anotación, la secuencia, el autor y la hora, así como el creador original y la hora de creación a lo largo de las revisiones. La reproducción comprueba las revisiones, los elementos padres, las referencias a colecciones y los ID de acción duplicados. «`manifest.json`» y los nuevos puntos de control también vinculan «`annotations_head`». Se conserva un punto de control de forma independiente para detectar truncamientos o reescrituras con una clave de firma copiada.

### Versiones de texto

`range.start` es un desplazamiento de punto de código Unicode con base en cero, `length` es un recuento positivo de puntos de código, y `quote` debe ser igual a la subcadena exacta de `payload.text` o `payload.caption` en el evento de destino. No se aplica NFC/NFKC, conversión de mayúsculas a minúsculas ni normalización de grafemas. Las secciones de cadena de Python y `Array.from(text)` de JavaScript implementan la misma indexación. La combinación de marcas y emojis ZWJ puede ocupar varios puntos de código. `range.version` es el hash del evento de destino, no la versión actual del mensaje ni el desplazamiento de entidad UTF-16 de Telegram. Las ediciones posteriores nunca reubican un resaltado automáticamente.

### Identidad y hora de la sección

`query` acepta exactamente un `chat_id` o varios `chat_ids` no vacíos, un rango opcional `from`/`to`, límites de ID de mensaje inclusivos (solo un chat), `kinds: "all"` o tipos exactos/con comodines de prefijo, `actors` explícitos, `search`, `hide_system` e `include_unscoped`. Los grupos de tipos de diario se expanden a sus predicados exactos. La búsqueda utiliza la búsqueda de carga útil NFC/sin distinción de mayúsculas y minúsculas del diario sin alterar el texto fuente firmado. Las fechas requieren una zona horaria y se normalizan a UTC. Las fechas filtran **«observed_at**». El «`source_at`» de Telegram se muestra por separado. Una eliminación sin una marca de tiempo de origen no tiene una hora de eliminación inventada. Un registro tardío observado fuera de un intervalo de tiempo no entra en él; un fragmento de ID de mensaje puede incluir una eliminación posterior para esos ID de mensaje.

La «`snapshot`» fija la hora de creación, la secuencia del diario/límite de hash, el recuento de coincidencias, la primera/última secuencia y el «`result_hash`». Este último es un SHA-256 de la matriz JSON canónica en UTF-8 de los hashes de eventos coincidentes ordenados lexicográficamente, incluyendo `[]` para una sección vacía. También contiene recuentos exactos de tipos y una miniatura del tiempo de observación de 24 intervalos. Un segmento almacena una consulta, no registros de fuente duplicados . Al exportar, «`board/slices/<id>.json`» enumera los hash actuales y las secuencias añadidas o eliminadas. El verificador reconstruye el resultado original en el momento de la creación y, a continuación, el resultado actual. Los registros añadidos se notifican como un hecho de cambio. La eliminación de un evento original rompe la cadena de pruebas inmutable; no se acepta de forma silenciosa como una eliminación ordinaria de una sección.

Las instantáneas de reacciones tienen listas incompletas de participantes recientes. El explorador compara instantáneas adyacentes del mismo chat o mensaje, incluida una anterior fuera del fragmento, e informa de las diferencias de recuento agregadas **entre observaciones**. No se considera que los participantes recientes que faltan hayan eliminado una reacción. La primera instantánea no tiene un estado anterior inferido. Las observaciones de los actores siguen atribuyéndose a la instantánea en la que se proporcionaron, no a un momento de acción inventado.

## API y exportaciones

`GET /api/board` acepta collection/chat/author/label/state/from/to/q/kind/comments, offset/limit y el orden más reciente/más antiguo. `GET /api/board/card/{id}` devuelve una ficha, una vista previa de la fuente, el hilo, el historial de estado y las fichas relacionadas. La subruta de participantes devuelve las opciones de mención elegibles. `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}` añade un registro. `POST /api/board/slice-preview` calcula una consulta. Los registros de «slice» se paginan en `GET /api/board/slice/{id}/records`; el recálculo utiliza siempre la instantánea de lectura estable actual. `/api/stream` en tiempo real emite notificaciones de `board` sin carga útil, independientemente de los cursores del diario.

`GET /api/board/export` devuelve un documento firmado. El acceso limitado al chat recibe una **divulgación** firmada claramente etiquetada, nunca las anotaciones de otro chat ni la cadena completa. Los archivos ZIP con pruebas completas incluyen `annotations.jsonl`, `case-board.json` firmado y apéndices JSON de fragmentos. La configuración de informes en HTML/PDF/JSON permite seleccionar «sin tablero», marcadores o fragmentos sin debate, o tarjetas con comentarios. La sección separa explícitamente las opiniones del equipo de las observaciones. Los filtros de datos del informe también restringen las notas legibles; los archivos fuente completos y firmados del archivo ZIP de pruebas permanecen íntegros.

`GET /api/board/slice/{id}/export` genera un extracto JSON firmado de «`tgwitness-board-selection-v1`»; `?format=csv` genera una tabla práctica sin firma independiente. Mantén el JSON y el ZIP:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

La comprobación de selección autentifica la declaración firmada, los registros de origen exactos y la integridad de su consulta en el límite especificado. El archivo ZIP de pruebas puede ser más reciente, pero debe contener ese prefijo. Se notifica explícitamente cualquier objetivo sin asignar. Se rechazan las instantáneas de fragmentos originales diferentes, las anotaciones modificadas, los estados de reproducción que no coincidan o las fuentes modificadas. Los archivos antiguos sin anotaciones conservan su comportamiento de verificación actual.

La opción predeterminada para el traspaso es **«No incluir**». La inclusión explícita genera fichas a partir de los registros ya minimizados, omite los objetivos inaccesibles u omitidos, retiene los elementos destacados cuyo texto original se haya minimizado, depura el texto del equipo siguiendo las mismas reglas de menciones y contactos, y, opcionalmente, sustituye las etiquetas de los investigadores por R01, R02… en los metadatos y en las apariciones conocidas en las notas. No se divulga ningún archivo « `annotations.jsonl`» original. El archivo sidecar firmado «`tgwitness-case-board-handover-v1`» y el informe contienen el mismo material minimizado. Los recuentos de segmentos describen únicamente los registros divulgados, ocultando los detalles originales del actor de la instantánea o la consulta. Los nombres en texto libre desconocidos para el minimizador siguen requiriendo revisión, al igual que en los traspasos habituales. Esta versión derivada no pretende conservar las firmas de las anotaciones originales tras la censura.

## Límites de funcionamiento

Los parámetros incluyen límites flexibles de 10 000 tarjetas y 50 000 comentarios, una página de fragmentos de hasta 5 000 registros y control de la vista previa de archivos multimedia. Los límites flexibles avisan sin borrar el historial. Las páginas de feeds tienen un máximo de 200 fichas. Los extractos de fragmentos JSON independientes tienen un límite de 64 MiB; restringe la consulta o utiliza el archivo ZIP firmado para material de mayor tamaño. El verificador independiente limita la reproducción de anotaciones a 256 MiB. Case Board no tiene habilitadas ni implementadas notificaciones de comentarios externos.

La aceptación automatizada de la función utiliza datos ficticios y una transmisión simulada de Telegram para comprobar el almacenamiento, el acceso, la visualización y las exportaciones. Consulte [el alcance de la verificación](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope) para conocer el alcance de las comprobaciones de las pruebas.
