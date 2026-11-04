# Formato de las pruebas

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/

Contenido del archivo ZIP firmado, tipos de registros, acuses de recibo, perfiles de usuarios, copias externas y verificación sin conexión.

TgWitness conserva las observaciones de Telegram visibles en la cuenta en un registro firmado. Los destinatarios pueden verificar los registros guardados, los archivos adjuntos y los informes comparándolos con una clave de recopilador de confianza y, a continuación, comparar el registro con un punto de control conservado de forma independiente. Esta página describe los formatos, las comprobaciones y el material que hay que conservar para el traspaso.

## ¿Qué es la firma?

| Material | Protección | Qué debe conservarse |
| --- | --- | --- |
| Cada entrada del registro, incluidos los eventos operativos | Cadena SHA-256 y una firma Ed25519 por cada evento | `events.jsonl` original, la huella digital de la clave de confianza, y un punto de control conservado |
| Contenido del archivo ZIP de pruebas | `manifest.sig` firma el manifiesto canónico, que recoge los hash de los archivos de contenido | El archivo ZIP completo, que incluye su manifiesto y su firma |
| Archivos adjuntos conservados | SHA-256 y recuento de bytes en un evento «`media.saved`» firmado; hash del archivo en el manifiesto ZIP firmado | Los bytes originales contenidos en el archivo ZIP verificado |
| Punto de control | Firma Ed25519 sobre la longitud del registro, el hash de cabecera, la clave pública y la hora de creación. | Una copia independiente conservada antes de un cambio objeto de controversia |
| Recibo de entrega | Mediciones del recopilador firmadas por separado; también incluidas en un evento firmado «`process.started`». | El registro y el diario asociado; las mediciones son declaradas por los propios usuarios. |
| Informes legibles: `report.html` y sus partes, `report.json`, `report.pdf`, `chat.pdf` | Un sello «Ed25519» por archivo sobre su contenido; el «PDF» también lleva una firma estándar «PDF» (véase «[» Informes legibles «](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#readable-reports)») | El archivo tal y como se ha recibido y la huella digital de la clave de confianza; el archivo ZIP al que hace referencia. |
| CSV independiente | No se incluye una firma criptográfica independiente; los hash de los eventos por sí solos resultan insuficientes | Utilice el contenido exacto del archivo ZIP verificado para comprobar su integridad. |
| Capturas de pantalla, impresiones o archivos PDF generados por un navegador | No se incluye la firma de TgWitness en el contenido derivado. | Conserve el paquete original verificado y documente cómo se ha creado la copia derivada. |

El recopilador verifica las firmas del registro antes de generar cada formato de exportación. Los informes legibles en HTML y PDF llevan sus propios sellos; el archivo CSV independiente se comprueba como parte de un ZIP firmado. Mantén el ZIP para conservar los bytes del archivo adjunto y el manifiesto, y un punto de control independiente para comparar el registro con un límite anterior.

## Traspaso de la investigación

1. Anote en las notas del caso la referencia del caso, el operador, el ID numérico de la cuenta de Telegram, las fuentes seleccionadas, la política de recopilación y el periodo de recopilación. TgWitness conserva las observaciones y admite notas y recopilaciones vinculadas a las fuentes en [el «Case Board](https://phishdestroy.github.io/TgWitness/es/docs/reference/case-board/)». Conserve los registros de transferencia y custodia junto con los materiales del caso. Comprueba la configuración de recopilación prevista con el [procedimiento de aceptación en tiempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
2. Conserve la huella digital de la clave pública del espacio de trabajo de forma independiente antes de basarse en sus exportaciones. Guarde los puntos de control firmados fuera del recopilador durante la recopilación. Registre las interrupciones y los límites de visibilidad de la cuenta.
3. Exporte un archivo **ZIP firmado** y conserve el recibo de ejecución firmado. Utilice un punto de control en o antes del límite del registro exportado. Un punto de control posterior puede rechazar correctamente una exportación anterior por ser demasiado corta. Las exportaciones incluyen el registro completo del espacio de trabajo, independientemente de los filtros de los paneles; revise el material antes de compartirlo.
4. Pida al destinatario que verifique el archivo ZIP con una copia fiable del verificador y la huella digital o punto de control facilitados de forma independiente. Desde un entorno de desarrollo fiable con su entorno de Python activo:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   Los informes de resultados correctos muestran «`key_pinned: true` » y «`checkpoint_checked: true` » cuando se proporcionan y aceptan ambas entradas. Conserve el resultado de la verificación.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. Registre el SHA-256 del archivo, el límite de exportación, la fecha de transferencia, el remitente y el destinatario en su registro de custodia. Mantenga intacto el paquete original y trabaje a partir de copias. Comparta los archivos de pruebas en lugar del directorio de datos privados de la aplicación, que también contiene sesiones de cuenta y claves de firma. Para la transferencia, la exportación puede guardarse en un archivo ZIP con cifrado AES-256 protegido por contraseña. La contraseña solo protege la confidencialidad y no se almacena; el destinatario extrae el archivo y verifica la exportación firmada que contiene, la cual permanece inalterada.
   2. Si se requiere una fijación de tiempo independiente, siga el [procedimiento del RFC 3161](https://phishdestroy.github.io/TgWitness/es/docs/reference/timestamp/) y conserve la solicitud, el punto de control, la información de la CA de confianza y la respuesta verificada de la autoridad. La mera preparación de una solicitud no garantiza la obtención de una marca de tiempo.

Una verificación satisfactoria establece la integridad en relación con la clave de recopilación de confianza y el límite retenido. Consulte [el alcance de la verificación](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope) para conocer los supuestos de confianza y [los resultados](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/) [de la validación](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/) de las comprobaciones realizadas.

## Extracto del traspaso

Un archivo ZIP firmado contiene todo el historial del espacio de trabajo. Cuando un tribunal, un abogado o una oficina de denuncia de abusos solo necesita algunos chats, un periodo concreto o determinadas personas, la opción **«Exportaciones → Extracto de entrega»** prepara una copia reducida (`tgwitness-handover-v1`) de acuerdo con las normas de divulgación seleccionadas. El operador indica la finalidad y selecciona los chats, un periodo opcional (UTC), las personas a las que se refiere el extracto, qué ocurre con el resto (se muestran, se sustituyen por seudónimos P01, P02… o se omiten), qué textos de los mensajes se conservan, qué archivos adjuntos y fotos de perfil se incluyen, y si se ocultan los números de teléfono y las direcciones de correo electrónico que aparecen en los textos. La finalidad y estas reglas figuran en el manifiesto firmado y en el informe; el registro «`handover.exported`» se almacena con el acceso que lo preparó y el SHA-256 del archivo, no el contenido.

`verify.py` comprueba un extracto de dos maneras. Un registro que se muestra sin cambios se verifica en su totalidad: su contenido se compara con su hash, su firma Ed25519 y su enlace a un predecesor incluido. Un registro minimizado conserva el hash y la firma originales, por lo que la firma sigue siendo válida, pero los campos omitidos no pueden volver a calcularse a partir de ella; el registro indica qué se ha omitido y el informe lo señala. El manifiesto indica la longitud del diario y el encabezado con la firma del recopilador sobre dicho encabezado, y cuenta los registros omitidos; el archivo «`coverage.json`» describe los chats seleccionados. No se detectan los nombres que aparecen dentro de los nombres de archivo. Revisa los archivos finales antes de compartirlos: el texto libre, los nombres de archivo y los archivos adjuntos seleccionados aún pueden identificar a personas. Conserva el ZIP completo firmado: la extracción supone una divulgación, no un sustituto.

## Informes legibles

Las pruebas firmadas, los traspasos y los archivos ZIP de chats contienen informes legibles en formato HTML y JSON, además de PDF cuando las fuentes necesarias están disponibles, en el idioma seleccionado para el informe. Cada informe está sellado con la clave Ed25519 del espacio de trabajo y puede verificarse por separado: ` `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]``.

- `report.html` / `chat.html`: la instrucción de sellado (`tgwitness-report-seal-v1`) cierra el archivo y firma el SHA-256 de cada byte anterior. Los historiales y chats largos se dividen en partes de un tamaño configurable (ajustes del informe, de 500 a 100 000 registros; 5 000 por defecto): `records/records-0001.html` o `messages/messages-0001.html`, cada una sellada con su número, rango y el total, y enumerada con su SHA-256 en el manifiesto firmado. Las series de pulsos del colector se muestran en una sola línea, a menos que la configuración del informe las enumere una por una.
- `report.json` (`tgwitness-report-json-v1`, claves `format`, `report`, `seal`): el sello firma el SHA-256 del JSON canónico del `report`, de modo que los sistemas y scripts de casos puedan leer los datos y se pueda realizar una selección para la protección de datos a partir de ellos, mientras que el archivo firmado permanece intacto.
- `report.pdf` / `chat.pdf`: un documento formal para imprimir y archivar, firmado dos veces sobre los mismos bytes, todo el archivo excepto el valor de la firma (`/ByteRange`). La firma estándar PDF (`adbe.pkcs7.detached`, CMS con SHA-256 y ECDSA P-256) utiliza un certificado de firma de documentos autoemitido almacenado en el almacén del espacio de trabajo; su número de serie de sujeto es la huella digital de la clave Ed25519 . El sello Ed25519 se incluye dentro del CMS como el atributo sin firmar `2.25.240684792623320047764573196045913242332` e identifica el certificado SHA-256 con `"content": "pdf-byte-range"`, de modo que la clave Ed25519 avala el certificado. Un lector PDF muestra si el archivo ha cambiado tras la firma y considera al firmante desconocido hasta que el certificado sea de confianza; en su lugar, compara la huella digital Ed25519. Los archivos PDF en chino, japonés y coreano necesitan una fuente en el servidor (o en `TGWITNESS_FONT_DIR`); sin ella, el archivo ZIP solo contiene los informes HTML y JSON .

En un canal o supergrupo, Telegram numera los mensajes 1, 2, 3… en orden. Una exportación de chat enumera el primer y último número, cuántos hay presentes y cada serie de números ausentes en `message-ids.json` , el manifiesto y el encabezado `chat.json` , y marca cada hueco donde se produce en la transcripción. `verify.py` vuelve a enumerarlos a partir de `chat.json` . Un número ausente es un mensaje que Telegram no devolvió (eliminado antes de la exportación o no visible para la cuenta); en los chats privados y los grupos básicos, los números se comparten entre todos los chats de la cuenta y no se cuentan los huecos.

Tras leer el historial, la exportación vuelve a solicitar a Telegram cada número ausente, por orden numérico (`channels.getMessages`, hasta 10 000 números). El resultado se encuentra en `message-ids.json` y en el informe. Una respuesta vacía significa que Telegram no tiene ningún mensaje con ese número para esta cuenta; no indica si el mensaje se eliminó o si nunca fue visible para la cuenta. Si se devuelve un mensaje Telegram, significa que se pasó por alto durante la lectura y se añade a la exportación, marcado como `found_on_recheck`.

Cada informe comienza con **. En resumen,**: un párrafo, seguido de lo que muestra el material y lo que no muestra (quién está detrás de una cuenta, la integridad de la entrega, las eliminaciones previas a la observación, la hora sin marca de tiempo). El sello de la propia página se vuelve ámbar cuando el navegador ha comprobado la firma del sello, no la de la página: un navegador no proporciona a una página sus propios bytes. Solo se vuelve verde cuando el lector arrastra el archivo al campo de verificación al final de la página y todos los bytes coinciden, y solo si la página mostrada es ese archivo; de lo contrario, se vuelve rojo.

Cada informe nombra el programa con exactitud: el commit de Git en el que el recopilador se ejecuta desde un checkout o el instalador establece `TGWITNESS_COMMIT`, y el SHA-256 de sus archivos fuente (`source_tree_sha256`, el JSON canónico de la ruta → SHA-256 de cada archivo `.py`, `.js`, `.css`, `.html` y `.svg` del paquete), que se reproduce al realizar un checkout de ese commit, a menos que se hayan modificado los archivos. El cliente Telegram recibe su nombre de su biblioteca, capa de API y centro de datos. Cuando comienza la observación y cuando una exportación de chat comienza y finaliza, el recopilador solicita a Telegram su hora (`updates.getState`, segundos enteros) y registra la hora de Telegram menos la del reloj del recopilador, con la incertidumbre derivada del tiempo de ida y vuelta; los informes muestran estas mediciones en la sección «Cadena de custodia». Una exportación de chat también registra cuándo se leyó el historial, además de las fechas de los mensajes.

### Visor de informes sin conexión y guía de archivo

Descomprime el archivo ZIP completo antes de abrir `chat.html` o `report.html`. El visor ofrece funciones de búsqueda, filtros, participantes, indicadores, detalles de los registros y selecciones de JSON y CSV sin necesidad de un servidor. Mantén `viewer/` y `media/` junto al informe. Las selecciones son derivadas: utiliza `verify.py SELECTION.json
--evidence ARCHIVE.zip` para compararlas con el archivo firmado. El verificador comprueba el ID del informe, la clave de firma, el límite del archivo y cada elemento seleccionado; los elementos editados, faltantes o duplicados no superan la comprobación. Las notas de selección y la hora de creación siguen siendo metadatos sin firmar.

Las lagunas en los números de mensaje solo se muestran en un historial de chat completo, sin filtrar y en orden ascendente. Ocultar una categoría o no poder cargar un bloque de datos no debe convertir una fila omitida en prueba de que falte un mensaje. Las búsquedas resaltadas se realizan sobre texto sin formato antes de la conversión de HTML, conservando el marcado literal.

El navegador comprueba las firmas del manifiesto, el ID y la clave del informe, así como todos los hash de los archivos enumerados. Rechaza estructuras ZIP ambiguas o mal formadas, nombres duplicados y rutas inseguras, y limita los archivos a 256 MiB y el contenido total declarado a 4 GiB. Utilice el verificador independiente para archivos más grandes. Esta comprobación del navegador complementa las comprobaciones que realiza el verificador sobre las cadenas de registros y la semántica de los datos.

`README.txt` contiene una guía de inicio, un inventario de archivos alineado, instrucciones de verificación y notas sobre el formato de los datos en el idioma del informe, seguidas de una guía completa en inglés. `SHA256SUMS` abarca los archivos que figuran en él, excluyéndose a sí mismo, a `manifest.json` y a `manifest.sig`; el manifiesto firmado también abarca `SHA256SUMS`. Mantén el ZIP original sin modificaciones y guarda los archivos de trabajo fuera de la carpeta extraída. Los informes PDF incluyen marcadores de sección e identificación del caso o del informe en páginas posteriores.

### El chat en el momento de la exportación

Una exportación de chat registra lo que Telegram indicaba sobre el chat cuando se inició la exportación: las propias etiquetas de Telegram (`scam`, `fake`, `restricted` con sus motivos, `verified`), los nombres de usuario, la descripción, el número de miembros y administradores, la discusión vinculada, la protección de contenidos, si los nuevos miembros ven los mensajes anteriores y a partir de qué mensaje esta cuenta puede ver el historial (`available_min_id`), la fecha del mensaje 1 cuando se trata de la creación del chat, y el SHA-256 de la foto del chat (guardada en `media/`). Registra la posición de la cuenta exportadora en el chat: función, fecha de incorporación, quién la invitó y, en el caso de un administrador, sus derechos. En su lugar, se indica una solicitud que Telegram rechaza.

Cuando la cuenta que realiza la exportación es un administrador, la exportación lee el registro de administración del chat (Telegram se conserva durante unas 48 horas) en `admin-log.json`: eliminaciones y ediciones con el contenido y la cuenta que las realizó. Es el único registro de una eliminación que indica quién la realizó.

### Indicadores

La lista de informes y el archivo contienen, como `indicators.csv` , `indicators.stix.json` (STIX 2.1 ) y `indicators.misp.json` (evento MISP ), lo que un servicio de gestión de abusos puede tratar en los mensajes grabados: enlaces y dominios (incluso los ocultos tras texto, en botones y en vistas previas de enlaces), direcciones de criptomonedas, nombres de usuario y enlaces de invitación Telegram , números de teléfono, direcciones de correo electrónico e imágenes guardadas. Las direcciones de Bitcoin, Litecoin, Dogecoin y TRON se incluyen en la lista solo cuando su suma de comprobación base58 es válida, las direcciones segwit cuando su suma de comprobación bech32 o bech32m es válida y las direcciones TON cuando su CRC es válido; las direcciones EVM y Solana se marcan como no comprobadas. Las imágenes contienen SHA-256 y un hash perceptual (dHash, 64 bits) que las copias recomprimidas o redimensionadas mantienen prácticamente sin cambios. Los informes escriben indicadores para que no se abran por accidente (`hxxps[://]example[.]com` ); los archivos conservan los valores tal y como estaban. Cada indicador se marca como desconocido y no apto para la detección automática (STIX , `indicator_types: unknown` , MISP , `to_ids: false` ; distribución a la propia organización): su inclusión en la lista indica que un mensaje lo contenía, no que sea malicioso. Un enlace cuyo texto muestre una dirección diferente a la que abre se marca en el informe.

Los informes PDF terminan con una declaración del examinador que debe firmarse a mano, una lista de comprobación para un notario o perito judicial, y un código QR (que también aparece en la primera página) con el ID del informe, la huella digital de la clave y el SHA-256 de los datos oficiales, de modo que una copia impresa permita remontarse a su archivo.

## Canonización de eventos

La entrada de hash consta exactamente de estos campos:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

Serialice utilizando JSON compatible con Python con UTF-8, claves de objetos ordenadas, sin escapismos ASCII, sin espacios en blanco insignificantes y sin NaN/infinito:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

El SHA-256 de esos bytes se convierte en el hash del evento. La firma se genera mediante Ed25519 sobre los 32 bytes sin procesar del hash y, a continuación, se codifica en base64. El primer «previous_hash» está compuesto por 64 ceros. Los números de secuencia comienzan en 1 y aumentan en 1. Todos los eventos, incluidos los operativos, comparten una misma cadena. No se suprime la duplicación de entregas: las observaciones repetidas constituyen recibos distintos, no una afirmación de acciones distintas en Telegram.

Las fechas sin procesar de Telegram son cadenas ISO; los campos binarios se convierten en objetos que contienen bytes_base64. El texto del mensaje, las entidades, los descriptores multimedia, los metadatos de respuesta, las reacciones y las acciones del servicio se conservan en los metadatos sin procesar del mensaje cuando se facilitan.

«observed_at» es la hora del reloj de pared UTC del recopilador. «source_at» es la fecha facilitada por Telegram, cuando está disponible. Las notificaciones de eliminación no proporcionan una hora exacta de eliminación, por lo que «source_at» permanece nulo. El orden de recepción de los datos no coincide necesariamente con el orden de los eventos en la fuente. Las instantáneas del historial utilizan fechas de origen más antiguas, pero horas de observación actuales.

## Semántica de los actores

message.new actor_id es el remitente del mensaje. message.edited no tiene ningún editor inferido; payload.sender_id registra al remitente del mensaje observado. Eliminación: el `actor_id` permanece nulo. Los mensajes del servicio de afiliación conservan el remitente y el tipo de acción, sin convertir cada eliminación en una baja voluntaria. Las actualizaciones sin procesar de los participantes conservan el `actor_id` tal y como se ha facilitado. Las instantáneas de reacciones no inventan un actor de cambio.

Las notificaciones de eliminación para chats privados y grupos normales solo contienen los identificadores de los mensajes. Dichos chats comparten una secuencia de identificadores para toda la cuenta, por lo que un identificador identifica un único mensaje de esta cuenta. Cuando un mensaje con ese identificador se ha guardado anteriormente en este registro, la eliminación se registra en ese chat como «message.deleted», utilizando «payload.chat_resolution» como nombre del método. Los identificadores que nunca se han guardado se conservan como «deletion.unscoped» sin «chat_id»; no se hace ninguna suposición. Los canales y los supergrupos numeran los mensajes por chat y nunca se emparejan de esta forma. Cuando el mensaje eliminado fue enviado por la cuenta observada, payload.deleted_message_was_outgoing es verdadero; aún no se ha facilitado quién lo ha eliminado.

## Cobertura: continuidad, lagunas e identificadores no observados

Cada archivo ZIP firmado contiene «`coverage.json`», el informe HTML se abre con el mismo resumen, y « `verify.py`» lo vuelve a calcular a partir de «`events.jsonl`» en lugar de confiar en el archivo:

- **Se observa de forma continua desde X hasta Y.** Un periodo comienza con `observation.started` y finaliza ante una pausa, una interrupción, una pérdida de conexión con Telegram, un cierre de sesión, un inicio de proceso sin una parada ordenada, o más de tres minutos sin ningún registro durante la observación (los pulsos se registran cada minuto, por lo que el silencio significa que el proceso se detuvo, se bloqueó o que el ordenador entró en modo de suspensión). Cuando se modifica el intervalo de los pulsos en **«Parámetros»**, cada pulso lo registra y el silencio permitido pasa a ser de tres intervalos, nunca menos de tres minutos.
- **Las lagunas** indican el tiempo transcurrido entre períodos, junto con el motivo. Una laguna que sigue sin resolverse en el último registro se marca como `not_resumed_by_last_record`.
- **No se registran los identificadores de los mensajes.** En el caso de los canales y supergrupos, que numeran los mensajes por chat, los identificadores que faltan entre los observados se indican como rangos. Se indican como «no*observados*» —por haber sido eliminados, no haberse entregado nunca o estar fuera del historial guardado— y nunca como «eliminados». Los chats privados y los grupos ordinarios comparten una secuencia para toda la cuenta, por lo que las lagunas en estos casos no significan nada y no se incluyen en la lista.
- Los avisos de interrupciones a nivel de chat (por ejemplo, cuando Telegram solicita la recuperación de diferencias en un canal) se contabilizan como notas; no interrumpen la cobertura global.

Cuando Telegram deja de aceptar la cuenta, el registro `coverage.gap` que pone fin a la observación contiene `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended` o `not_authorized`) y el Telegram error; `verify.py` indica la causa por la que finaliza el periodo.

La cobertura describe lo que este recopilador ha registrado. No constituye una prueba de que Telegram haya entregado todas las actualizaciones durante un periodo continuo.

## Productor

El manifiesto firmado de los archivos ZIP de pruebas, las exportaciones de chats, los registros de testigos y la declaración de los archivos de perfiles de usuarios contienen `producer` : software, versión, proyecto (PhishDestroy), página web y repositorio de código fuente. El informe HTML muestra la misma línea, y `verify.py` la incluye como parte de lo que ha verificado. Los archivos creados antes de que existiera este campo se verifican como anteriormente y se indican como si no mencionaran al creador.

Cada registro `observation.started` también identifica al cliente Telegram que realizó la observación: su `api_id` (nunca el hash), ya sea un par público integrado o la propia aplicación del operador, la descripción del cliente enviada en la solicitud de conexión de Telegram, y el tipo de ruta de conexión con el modo IP (sin dirección de proxy ni clave secreta). El informe y el `custody.json` enumeran todos los clientes y rutas distintos con la fecha en que se registraron, así como las ocasiones en las que ningún proxy de la lista respondió y el Telegram detectó la dirección del servidor. Los registros anteriores a este así lo indican.

## Perfiles de personas

A petición, se genera un archivo de perfil (`tgwitness-dossier-v1`, JSON) a partir de los registros ya presentes en el registro de pruebas correspondientes a un chat; no se recupera nada de Telegram y el contenido de los perfiles nunca se escribe en el registro de pruebas (la activación y desactivación de perfiles se registra como `dossier.changed`). Para cada persona con un mensaje guardado, se enumeran el nombre y el historial de nombres de usuario, las marcas de Telegram (bot, estafa, falso, premium, verificado, restringido, eliminado) tal y como se ve en el momento del guardado, las identificadores de foto de perfil, el hash SHA-256 y el hash perceptual (pHash, compatible con `imagehash.phash`) del avatar procedente de la caché local de avatares con avatares similares, la actividad (primer y último mensaje, recuentos, publicaciones editadas y eliminadas, mensajes por hora UTC), quién responde a quién, otros chats en este diario en los que la persona ha escrito, y carteras mencionadas (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL; las direcciones Base58Check se validan mediante suma de comprobación), números de teléfono, nombres de usuario y enlaces, incluidos los enlaces ocultos tras el texto.

Cada dato indica los registros del diario (`seq`) de los que procede, y `record_hashes` contiene el hash de cada registro al que se hace referencia. La declaración está firmada con la clave del espacio de trabajo:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

Comprueba la firma, verifica la propia exportación de pruebas (firma, cadena de hash y archivos) y que cada registro al que se hace referencia exista sin modificaciones en dicha exportación del mismo espacio de trabajo. Los hash de los avatares se etiquetan como procedentes de la caché local (no de registros del diario). Las menciones son coincidencias de patrones: pistas que deben comprobarse, no hechos verificados. Los perfiles se activan por cada chat, pueden exportarse como un archivo ZIP cifrado con AES-256 y protegido con contraseña, y se eliminan cuando se desactivan o cuando el chat se retira de las fuentes.

## Testigo independiente

Un diario de testigos (`tgwitness-witness-v1`) y sus publicaciones en el canal se cotejan con una exportación de pruebas realizada con `verify.py --witness … --channel …`; véase [«testigo independiente](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/)».

## Manifiesto y puntos de control

El archivo `manifest.json` incluye el formato, la hora de exportación, la clave pública, la huella digital, la longitud del registro, el hash de cabecera, el ámbito, el productor, las limitaciones y el SHA-256 de cada elemento de contenido, salvo los propios ``manifest.json`` y ``manifest.sig``. El archivo `manifest.sig` es la firma Ed25519 en base64 sobre el JSON del manifiesto canónico. El verificador rechaza elementos inesperados o ausentes, nombres duplicados, archivos dañados, secuencias o cadenas rotas, firmas no válidas y discrepancias con un punto de control facilitado. Nunca extrae rutas de archivos. Limita el tamaño total declarado sin comprimir a 4 GiB; el `--max-gib N` permite archivos de mayor tamaño creados con un límite **de parámetros** ampliado.

Obtenga el código verificador de una versión de confianza o de una copia independiente revisada. Un verificador incluido en un archivo no fiable es material ejecutable proporcionado por el autor de dicho archivo; su presencia supone una ventaja en cuanto a portabilidad, pero no constituye un punto de referencia independiente de confianza.

Un punto de control firma una declaración que contiene la clave pública, la longitud del registro, el hash inicial y la hora de creación. El verificador puede comprobar que un archivo posterior contenga el mismo prefijo. Conserve un punto de control fuera del recopilador antes de un cambio objeto de controversia: un atacante que controle tanto el archivo como el punto de control puede sustituir ambos.

## Ámbito de verificación

Las firmas identifican la clave del recopilador y protegen el material guardado. Asigna su huella digital de forma independiente para asociar esa clave con el recopilador previsto. Las actualizaciones de Telegram constituyen la entrada para la recopilación; TgWitness firma sus observaciones sobre dichas actualizaciones. Las firmas no son firmas emitidas por Telegram ni por los autores de los mensajes.

Un punto de control conservado o un registro de testigo detecta un prefijo de diario anterior modificado, incluida una sustitución firmada con una clave de recopilador copiada. Los registros falsificados antes de su primer punto de control independiente requieren corroboración de la fuente: el titular de una clave de recopilador puede firmar material nuevo. Mantenga controlado el acceso a la clave de firma y conserve las referencias por separado.

Evalúa la visibilidad de la cuenta y la entrega utilizando registros de cobertura y pruebas controladas. Utiliza una marca de tiempo externa verificada para el anclaje temporal independiente. Un ID de remitente identifica una cuenta de Telegram; vincúlalo a una persona a lo largo de tu investigación. Los recibos del programa y las comprobaciones en la nube describen las mediciones comunicadas por el recopilador y la configuración de la implementación. Consulta [los resultados de la validación](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/) para conocer el comportamiento medido y su alcance.

## Archivos adjuntos

Los archivos se identifican mediante SHA-256 en el directorio «media/». Un evento «media.saved» vincula un hash y la longitud en bytes a un evento de mensaje específico. Los nombres de archivo sin procesar son metadatos, nunca rutas locales. Los bytes multimedia se descargan de forma asíncrona, por lo que una eliminación inmediata podría impedir su captura. La recopilación desactivada, los archivos de tamaño excesivo o desconocido, los errores de descarga y las descargas interrumpidas se muestran como resultados. Un fallo del proceso puede dejar archivos parciales sin referenciar; estos no se incluyen en las exportaciones.

El exportador ZIP verifica los archivos multimedia almacenados comparándolos con sus nombres. Las exportaciones en formato JSONL, CSV y HTML verifican las firmas de los eventos, pero no incluyen los bytes de los archivos multimedia. Los informes derivados son meras facilidades; el archivo events.jsonl constituye la representación oficial de los eventos.

Una exportación completa del chat guarda los archivos adjuntos, según la configuración de archivos adjuntos del espacio de trabajo, en media/, con nombres del tipo SHA-256. Cada registro de mensaje en chat.json indica el nombre de su archivo (`file`, `file_sha256`) o el motivo de su ausencia (`file_status`), junto con lo que el lector vio alrededor del texto: enlaces detrás del texto, origen del reenvío, botones de bot, firma, visualizaciones y el temporizador de eliminación automática. `verify.py` comprueba que todos los archivos nombrados se encuentren en el manifiesto firmado bajo ese hash.

## Recibos de recogida y procesamiento duraderos (0,2)

Una tarea multimedia y su confirmación del evento de mensaje se realizan en una sola transacción. La tarea almacena el descriptor original del mensaje de Telegram; la observación firmada vincula su SHA-256, la cuenta y la política de tamaño. La recuperación verifica dicha vinculación antes de la descarga. Nunca recupera el mensaje actual y sustituye de forma silenciosa por un archivo adjunto más reciente. Las tareas interrumpidas se vuelven a intentar, mientras que el fallo permanente sigue siendo un resultado explícito.

Cada espacio de trabajo cuenta con su propio registro y su propia identidad de firma. Un evento «process.started» incluye un identificador de ejecución, las horas locales, las versiones de las dependencias, los hash de los archivos fuente, la cuenta y el ámbito iniciales, y la configuración de captura. Las señales de vida incluyen el identificador de ejecución, el tiempo monótono y el estado de la cola. El recibo del proceso también puede descargarse como un informe firmado por separado. Las mediciones de los archivos son autodeclaradas y no constituyen una certificación de hardware fiable.

Los puntos de control automáticos se conservan localmente al iniciar el sistema, cada cinco minutos mientras se realiza la observación (**Parámetros → Punto de control firmado cada**), y al detenerse de forma ordenada. La verificación al inicio y la exportación comparan el registro con el último punto de control local conservado. Esto permite detectar una reversión de la base de datos cuando el punto de control se conserva; un operador que controle ambos elementos aún puede sustituirlos. La retención independiente y las marcas de tiempo externas fiables siguen siendo requisitos distintos.

Tras un reinicio, se reanuda la posición de actualización de Telegram guardada (`catch_up_from` en `observation.started`) y se solicitan las actualizaciones perdidas. Una nueva comprobación periódica registra `message.recovered` para los mensajes perdidos y `message.missing_on_recheck` cuando Telegram ya no devuelve un mensaje guardado; este último no es un aviso de eliminación y no indica quién lo ha eliminado ni la hora.

### Copia y restauración externas (S3)

La copia externa (Exportaciones, desactivada por defecto) carga segmentos del registro, archivos conservados y puntos de control con sus marcas de tiempo, así como las exportaciones completas de chats, a un almacenamiento compatible con S3, cifrados con AES-256-GCM antes de la subida, mediante una clave almacenada en la bóveda del espacio de trabajo; se aplica la retención de Object Lock cuando el depósito lo admita. Sin la clave descargada, la copia no puede leerse. Restablezca y verifique con `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

La restauración requiere un directorio ordinario vacío. Las descargas y los objetos descifrados permanecen en un almacenamiento temporal privado hasta que se verifiquen todo el registro y cada punto de control conservado. Se rechazan las rutas de objetos no seguras, los rangos de segmentos incoherentes y los registros más cortos que un punto de control; si la verificación falla, no se publican archivos restaurados. Las comprobaciones de retención comparan el modo «Object Lock» y la fecha devueltos con el plazo enviado en el momento de la carga (con una tolerancia de redondeo de un segundo). Un plazo caducado, no válido o acortado no se considera verificado. El estado informa del objeto muestreado cuya retención se ha recuperado para esa ronda de carga.

Los archivos locales que faltan o están dañados se notifican como un error de la pasada y el cursor se mantiene antes de ellos, de modo que el archivo se vuelve a intentar en la siguiente pasada; los archivos, puntos de control y exportaciones posteriores a este se siguen copiando. La restauración comprueba todas las referencias a los archivos conservados cotejándolas con los hash descifrados y los tamaños registrados. Los segmentos idénticos y superpuestos del registro procedentes de subidas interrumpidas se deduplican; las superposiciones conflictivas se rechazan. Los puntos de control creados durante una subida se aplazan hasta que se hayan copiado los registros del diario a los que corresponden, de modo que una pasada completada no publique un punto de control antes que su correspondiente registro del diario.

### Instantáneas de exportación en tiempo real

Las exportaciones en tiempo real utilizan una instantánea de lectura estable de SQLite. Es posible que su parte inicial sea más antigua que el registro actual en tiempo real cuando finalice la descarga. Un punto de control creado después de dicha instantánea puede indicar correctamente que el archivo es más corto; compárelo con un punto de control situado en el prefijo exportado o anterior a él, no con un punto de control posterior arbitrario.

## Preparación de RFC 3161 y verificación de respuestas (0.2)

El modo de pruebas (desactivado por defecto) envía únicamente el SHA-256 de cada punto de control firmado a las autoridades RFC 3161 y a los calendarios de OpenTimestamps indicados, a través de la ruta del espacio de trabajo y nunca a través de MTProxy. Las respuestas se almacenan en `checkpoints/anchors/`, se exportan y se verifican mediante `verify.py` (`--tsa-ca` comprueba la firma TSA; confirme las pruebas de OpenTimestamps con `ots upgrade` y `ots verify`).

El panel prepara un archivo de solicitud que contiene los bytes canónicos de checkpoint.json, una huella SHA-256 del mensaje y un nonce aleatorio en timestamp.tsq, sumas de comprobación e instrucciones. No se realiza ninguna solicitud de red. La preparación no constituye un sello de tiempo fiable.

`python -m tgwitness.anchor verify` invoca OpenSSL dos veces: una vez con los bytes del punto de control y otra vez con la solicitud original. Se requiere explícitamente un archivo de CA de confianza; los certificados incluidos no se consideran automáticamente de confianza. La comprobación de la solicitud es opcional en la CLI, por lo que debe conservar y proporcionar el parámetro --request para comprobar el nonce. El resultado indica si se ha comprobado. La firma del punto de control del recopilador y el registro deben verificarse por separado con la huella digital de confianza del recopilador.

La verificación comprueba la firma de la respuesta, los bytes de punto de control y, cuando se facilite, la solicitud original bajo la confianza de la CA especificada. Las comprobaciones de revocación y la validación del archivo a largo plazo tras la caducidad del certificado quedan fuera del alcance del verificador actual. Consulte el [procedimiento](https://phishdestroy.github.io/TgWitness/es/docs/reference/timestamp/) y [los resultados de la validación](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/).

## Registros opcionales en modo de pruebas: dispositivos «drand» y «Telegram»

Hay otros dos registros que pueden ejecutarse en las mismas pasadas que las marcas de tiempo. Ambos están desactivados por defecto y solo surten efecto mientras el modo de pruebas está activado: Extras → Pruebas y copias de seguridad → **Más testigos · opcional**, o `"drand": true` y `"devices": true` en `POST /api/evidence`. Un fallo no detiene al otro ni a las marcas de tiempo; el panel muestra el último resultado de cada uno debajo del formulario.

**drand** (`beacon.drand` ). Cada pasada escribe la ronda más reciente de drand quicknet, la aleatoriedad pública de la Liga de la Entropía (una ronda cada 3 segundos), en el diario: `chain` , `round` , `randomness` , `signature` , `round_time` y el `relay` que respondió. Una ronda verificada e impredecible proporciona una referencia temporal inferior para el material vinculado mediante hash posterior. Una marca de tiempo verificada en un punto de control posterior proporciona una referencia temporal superior. Estas comprobaciones delimitan el material vinculado; la cobertura de la recopilación se evalúa por separado. El recopilador consulta primero a `drand.cloudflare.com` y, a continuación, a los repetidores de Protocol Labs, a través de la ruta del espacio de trabajo, con una solicitud por pasada.

`verify.py` comprueba que cada valor aleatorio sea el SHA-256 de su firma y que el tiempo de ronda sea correcto, e informa de las rondas, del tramo más largo sin ninguna y de cuánto se retrasó el reloj del recopilador respecto a drand. No comprueba la firma BLS. `--check-drand` compara las rondas con un relé de Cloudflare y un relé de Protocol Labs, ya sean todas ellas o una muestra aleatoria de 100 en un registro extenso; una ronda que difiera no supera la verificación.

Dispositivos **, Telegram,** (`account.devices`). En cada pasada se leen las sesiones de la cuenta con `account.getAuthorizations`; la lista Telegram que aparece en Ajustes → Dispositivos se registra: íntegramente cuando ha cambiado desde la pasada anterior, con los hash de sesión `added` y `removed`, en caso contrario, solo su recuento y SHA-256. Se conservan el modelo del dispositivo, la plataforma, la aplicación y la versión, la fecha de creación y la última actividad, el país y la región; las direcciones IP no, ya que las exportaciones de pruebas quedan fuera de tu control. La propia sesión del recopilador está activa en todo momento, por lo que solo la actividad de otras sesiones cuenta como un cambio. `verify.py` informa de la frecuencia con la que se ha registrado la lista y de cada sesión nueva y finalizada. Solo lee la lista mientras se ejecuta la observación.

Lo que no muestran: drand no demuestra más que el orden de los registros con respecto al tiempo público, y la lista de dispositivos es la declaración de Telegram a través del recopilador, firmada por este al igual que cualquier otro registro.

**Registro de Cloudflare Gateway** (`cloudflare.gateway_dns`). Para un servidor que realiza la resolución a través de Cloudflare Gateway ([, Gateway DNS](https://phishdestroy.github.io/TgWitness/es/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)), cada copia incluye lo que Gateway ha registrado desde la copia anterior: un registro por ventana de, como máximo, tres horas con `from`, `until`, `location_id`, el `address` del servidor cuando esté configurado, y el `queries` como `[at, name, type, rcode, decision, colo]`, incluso cuando no haya ninguno. Configurarlo en **. Registro de Cloudflare Gateway**: cuenta, ubicación, dirección opcional y un token de solo lectura (lectura de datos analíticos de la cuenta Analytics Read; Zero Trust PII Read para mantener una dirección de una ubicación compartida). El panel los comprueba mediante una solicitud antes de guardarlos; el token permanece cifrado y nunca entra en el registro. `verify.py` enumera las ventanas, los nombres más buscados y cualquier momento en el que no haya ninguna copia; un registro cuyo recuento no coincida con sus consultas falla. Una ventana que contenga más de una página de consultas en un solo segundo conserva esa página e indica que falta el resto. La copia es la respuesta de Cloudflare a través del colector, firmada por este; en un plazo de 24 horas, cualquier persona con un token de solo lectura puede compararla con Cloudflare.
