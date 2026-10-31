# Formato de las pruebas

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/

Contenido del archivo ZIP firmado, tipos de registros, acuses de recibo, perfiles de usuarios, copias externas y verificación sin conexión.

Una observación no es una conclusión. Un identificador de remitente no es una identidad en el mundo real. La fuente es la actualización del servicio visible en la cuenta; Telegram no firma criptográficamente estos registros guardados para un investigador externo.

## ¿Qué es la firma?

| Material | Protección | Qué debe conservarse |
| --- | --- | --- |
| Cada entrada del registro, incluidos los eventos operativos | Cadena SHA-256 y una firma Ed25519 por cada evento | `events.jsonl` original, la huella digital de la clave de confianza, y un punto de control conservado |
| Contenido del archivo ZIP de pruebas | `manifest.sig` firma el manifiesto canónico, que recoge los hash de los archivos de contenido | El archivo ZIP completo, que incluye su manifiesto y su firma |
| Archivos adjuntos conservados | SHA-256 y recuento de bytes en un evento «`media.saved`» firmado; hash del archivo en el manifiesto ZIP firmado | Los bytes originales contenidos en el archivo ZIP verificado |
| Punto de control | Firma Ed25519 sobre la longitud del registro, el hash de cabecera, la clave pública y la hora de creación. | Una copia independiente conservada antes de un cambio objeto de controversia |
| Recibo de entrega | Mediciones del recopilador firmadas por separado; también incluidas en un evento firmado «`process.started`». | El registro y el diario asociado; las mediciones son declaradas por los propios usuarios. |
| Archivo independiente en formato CSV o HTML | No se incluye una firma criptográfica independiente; los hash de los eventos por sí solos resultan insuficientes | Utilice el contenido exacto del archivo ZIP verificado para comprobar su integridad. |
| Capturas de pantalla, impresiones o archivos PDF generados por un navegador | No se incluye la firma de TgWitness en el contenido derivado. | Conserve el paquete original verificado y documente cómo se ha creado la copia derivada. |

El recopilador verifica las firmas del registro antes de generar cada formato de exportación. Dicha comprobación de origen no genera una firma en un archivo CSV o HTML descargado por separado. Del mismo modo, una firma de evento JSONL válida no proporciona los bytes del archivo adjunto ni establece de forma independiente que se haya facilitado la totalidad del registro observado.

## Traspaso de la investigación

1. Anote en sus notas del caso la referencia del caso, el operador, el identificador numérico de la cuenta de Telegram, las fuentes seleccionadas, la política de recopilación y el periodo de recopilación. TgWitness conserva las observaciones; la asignación de casos y los registros de custodia se gestionan fuera de la aplicación. Verifique la configuración de recopilación prevista mediante el [procedimiento de aceptación en tiempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
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

Una verificación satisfactoria establece la integridad en relación con la clave del recopilador de confianza y el límite establecido. La veracidad de la fuente, la entrega completa de Telegram, la hora fiable y la admisibilidad legal requieren pruebas independientes. Esta versión no ha superado la cualificación en Telegram en tiempo real ni una evaluación forense o de seguridad independiente.

Una clave de recopilador copiada puede firmar un registro de sustitución falsificado. La verificación frente a un punto de control o un registro de testigo conservado de forma independiente detecta un prefijo anterior modificado; la verificación de la firma por sí sola no puede hacerlo. Un testigo corrige lo que ha presentado el recopilador, por lo que no establece de forma independiente la veracidad de los registros falsificados antes de su primer punto de control externo. Los informes de implementación en la nube comprueban la configuración y las mediciones comunicadas por el recopilador; no establecen que nunca se haya copiado una clave privada durante la fase de arranque.

Las notificaciones enviadas a través de Apprise incluyen los nombres y recuentos de los espacios de trabajo y los chats; solo se añaden breves extractos de los mensajes eliminados y editados cuando el operador activa esta función (desactivada por defecto). Se trata de una señal de conveniencia, no de una prueba: no se garantiza su entrega, y solo el registro y sus exportaciones firmadas recogen lo que se ha observado. Con un proxy del espacio de trabajo, las notificaciones siguen la misma ruta; se rechazan los servicios que no puedan utilizarlo, así como las rutas de MTProxy.

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

La cobertura describe lo que este recopilador ha registrado. No constituye una prueba de que Telegram haya entregado todas las actualizaciones durante un periodo continuo.

## Productor

El manifiesto firmado de los archivos ZIP de pruebas, las exportaciones de chats, los registros de testigos y la declaración de los archivos de perfiles de usuarios contienen `producer` : software, versión, proyecto (PhishDestroy), página web y repositorio de código fuente. El informe HTML muestra la misma línea, y `verify.py` la incluye como parte de lo que ha verificado. Los archivos creados antes de que existiera este campo se verifican como anteriormente y se indican como si no mencionaran al creador.

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

Una firma válida procedente de una clave no fijada solo garantiza la coherencia interna. Ni siquiera una clave fijada puede demostrar la veracidad del contenido original si el recopilador o la clave se vieron comprometidos antes del registro. El sellado de tiempo externo y la captura fiable son requisitos independientes. TgWitness no garantiza la admisibilidad ni la certificación forense.

## Archivos adjuntos

Los archivos se identifican mediante SHA-256 en el directorio «media/». Un evento «media.saved» vincula un hash y la longitud en bytes a un evento de mensaje específico. Los nombres de archivo sin procesar son metadatos, nunca rutas locales. Los bytes multimedia se descargan de forma asíncrona, por lo que una eliminación inmediata podría impedir su captura. La recopilación desactivada, los archivos de tamaño excesivo o desconocido, los errores de descarga y las descargas interrumpidas se muestran como resultados. Un fallo del proceso puede dejar archivos parciales sin referenciar; estos no se incluyen en las exportaciones.

El exportador ZIP verifica los archivos multimedia almacenados comparándolos con sus nombres. Las exportaciones en formato JSONL, CSV y HTML verifican las firmas de los eventos, pero no incluyen los bytes de los archivos multimedia. Los informes derivados son meras facilidades; el archivo events.jsonl constituye la representación oficial de los eventos.

## Recibos de recogida y procesamiento duraderos (0,2)

Una tarea multimedia y su confirmación del evento de mensaje se realizan en una sola transacción. La tarea almacena el descriptor original del mensaje de Telegram; la observación firmada vincula su SHA-256, la cuenta y la política de tamaño. La recuperación verifica dicha vinculación antes de la descarga. Nunca recupera el mensaje actual y sustituye de forma silenciosa por un archivo adjunto más reciente. Las tareas interrumpidas se vuelven a intentar, mientras que el fallo permanente sigue siendo un resultado explícito.

Cada espacio de trabajo cuenta con su propio registro y su propia identidad de firma. Un evento «process.started» incluye un identificador de ejecución, las horas locales, las versiones de las dependencias, los hash de los archivos fuente, la cuenta y el ámbito iniciales, y la configuración de captura. Las señales de vida incluyen el identificador de ejecución, el tiempo monótono y el estado de la cola. El recibo del proceso también puede descargarse como un informe firmado por separado. Las mediciones de los archivos son autodeclaradas y no constituyen una certificación de hardware fiable.

Los puntos de control automáticos se conservan localmente al iniciar el sistema, cada cinco minutos mientras se realiza la observación (**Parámetros → Punto de control firmado cada**), y al detenerse de forma ordenada. La verificación al inicio y la exportación comparan el registro con el último punto de control local conservado. Esto permite detectar una reversión de la base de datos cuando el punto de control se conserva; un operador que controle ambos elementos aún puede sustituirlos. La retención independiente y las marcas de tiempo externas fiables siguen siendo requisitos distintos.

Tras un reinicio, se reanuda la posición de actualización de Telegram guardada (`catch_up_from` en `observation.started`) y se solicitan las actualizaciones perdidas. Una nueva comprobación periódica registra `message.recovered` para los mensajes perdidos y `message.missing_on_recheck` cuando Telegram ya no devuelve un mensaje guardado; este último no es un aviso de eliminación y no indica quién lo ha eliminado ni la hora.

### Copia y restauración externas (S3)

La copia externa (Exportaciones, desactivada por defecto) carga segmentos del registro, archivos conservados y puntos de control con sus marcas de tiempo, así como las exportaciones completas de chats, a un almacenamiento compatible con S3, cifrados con AES-256-GCM antes de la subida, mediante una clave almacenada en la bóveda del espacio de trabajo; se aplica la retención de Object Lock cuando el depósito lo admita. Sin la clave descargada, la copia no puede leerse. Restablezca y verifique con `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

La restauración requiere un directorio ordinario vacío. Las descargas y los objetos descifrados permanecen en un almacenamiento temporal privado hasta que se verifiquen todo el registro y cada punto de control conservado. Se rechazan las rutas de objetos no seguras, los rangos de segmentos incoherentes y los registros más cortos que un punto de control; si la verificación falla, no se publican archivos restaurados. Las comprobaciones de retención comparan el modo «Object Lock» y la fecha devueltos con el plazo enviado en el momento de la carga (con una tolerancia de redondeo de un segundo). Un plazo caducado, no válido o acortado no se considera verificado. El estado informa del objeto muestreado cuya retención se ha recuperado para esa ronda de carga.

El progreso de la copia se limita al destino y a la clave de cifrado. Al cambiar el punto final, el depósito o el prefijo, se inicia una copia completa del registro, los archivos multimedia y los puntos de control conservados localmente hacia ese destino. El progreso anterior no incluido en el ámbito de aplicación se conserva, pero se reproduce una sola vez tras la actualización. Las exportaciones históricas de chats que ya se hayan eliminado de la bandeja de salida local permanecen en su destino anterior.

Los archivos locales que faltan o están dañados se notifican como un error de la pasada y el cursor se mantiene antes de ellos, de modo que el archivo se vuelve a intentar en la siguiente pasada; los archivos, puntos de control y exportaciones posteriores a este se siguen copiando. La restauración comprueba todas las referencias a los archivos conservados cotejándolas con los hash descifrados y los tamaños registrados. Los segmentos idénticos y superpuestos del registro procedentes de subidas interrumpidas se deduplican; las superposiciones conflictivas se rechazan. Los puntos de control creados durante una subida se aplazan hasta que se hayan copiado los registros del diario a los que corresponden, de modo que una pasada completada no publique un punto de control antes que su correspondiente registro del diario.

### Instantáneas de exportación en tiempo real

Las exportaciones en tiempo real utilizan una instantánea de lectura estable de SQLite. Es posible que su parte inicial sea más antigua que el registro actual en tiempo real cuando finalice la descarga. Un punto de control creado después de dicha instantánea puede indicar correctamente que el archivo es más corto; compárelo con un punto de control situado en el prefijo exportado o anterior a él, no con un punto de control posterior arbitrario.

## Preparación de RFC 3161 y verificación de respuestas (0.2)

El modo de pruebas (desactivado por defecto) envía únicamente el SHA-256 de cada punto de control firmado a las autoridades RFC 3161 y a los calendarios de OpenTimestamps indicados, a través de la ruta del espacio de trabajo y nunca a través de MTProxy. Las respuestas se almacenan en `checkpoints/anchors/`, se exportan y se verifican mediante `verify.py` (`--tsa-ca` comprueba la firma TSA; confirme las pruebas de OpenTimestamps con `ots upgrade` y `ots verify`).

El panel prepara un archivo de solicitud que contiene los bytes canónicos de checkpoint.json, una huella SHA-256 del mensaje y un nonce aleatorio en timestamp.tsq, sumas de comprobación e instrucciones. No se realiza ninguna solicitud de red. La preparación no constituye un sello de tiempo fiable.

`python -m tgwitness.anchor verify` invoca OpenSSL dos veces: una vez con los bytes del punto de control y otra vez con la solicitud original. Se requiere explícitamente un archivo de CA de confianza; los certificados incluidos no se consideran automáticamente de confianza. La comprobación de la solicitud es opcional en la CLI, por lo que debe conservar y proporcionar el parámetro --request para comprobar el nonce. El resultado indica si se ha comprobado. La firma del punto de control del recopilador y el registro deben verificarse por separado con la huella digital de confianza del recopilador.

El verificador actual no recaba información sobre revocaciones ni implementa la validación de archivos a largo plazo tras la caducidad del certificado. No se debe equiparar la verificación satisfactoria de la firma con un sello de tiempo cualificado ni con la admisibilidad legal. No se ha contactado con ninguna TSA independiente real durante el desarrollo. Véase [el procedimiento](https://phishdestroy.github.io/TgWitness/es/docs/reference/timestamp/).
