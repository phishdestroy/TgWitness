# Telegram · Investigue en todos los chats

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/cases/

Un caso completo entre canales, grupos, chats privados y bots: recoger, unir las piezas, reconstruir la cronología y entregarlo.

Un incidente inventado, de principio a fin. La recogida, la búsqueda y los perfiles de personas encuentran los registros, [Case Board](https://phishdestroy.github.io/TgWitness/es/docs/case-board/) los organiza y [Report studio](https://phishdestroy.github.io/TgWitness/es/docs/reports/) los presenta.

CASO RESUELTO / UN DESTINO DE PAGO MODIFICADO

### Un incidente. Cuatro conversaciones. Un rastro que reconstruir.

Una publicación de canal lleva a un bot. Un grupo habla de un nuevo enlace de pago y el bot lo muestra. La publicación se edita, un chat privado repite el enlace y un mensaje del grupo desaparece.

¿Quién publicó cada versión?¿Dónde apareció el enlace?¿Qué archivo se conservó?¿Qué ha cambiado y cuándo?

Carga de historial, IA, MCP, OCR y webhooks: [Trabajar el archivo](https://phishdestroy.github.io/TgWitness/es/docs/archive/).

## 1. Establecer una cobertura que abarque toda la cuenta

Alcance de cuenta entera solo en una cuenta dedicada. Una cuenta principal usa chats elegidos o una carpeta.

1. [Conecte la cuenta](https://phishdestroy.github.io/TgWitness/es/docs/accounts/) en su propio espacio. Apunte la referencia del caso, el ID de cuenta, el espacio y la huella de la clave.
2. **Fuentes → Alcance de observación → Modo investigación**: **Cuenta entera**, los cuatro tipos de fuente y **Acciones propias**. Cada chat nuevo guarda su perfil y sus últimos **200 mensajes visibles**. **Guardar alcance** y confirme.
3. **Cargar chats** y compare con la lista de chats de la cuenta. El límite es de 1000 diálogos (hasta 20 000 en **Parámetros → Chats leídos de la lista de la cuenta**); los que queden fuera aparecen cuando se activan.
4. **Ajustes de grabación** → **Toda la actividad visible**, revise límites de adjuntos y espacio en disco. Arranque y pruebe con un mensaje, una edición y un borrado.

CanalesGruposChats privadosBots

UNA CUENTA / UNA CLAVE DE FIRMA**Toda la actividad visible de las cuentas seleccionadas → un único registro**

Mensajes · modificaciones · avisos de eliminación · reacciones visibles · eventos relacionados con la pertenencia al grupo · acciones propias

«Cuenta entera» significa todos los chats que esta cuenta puede abrir, menos las exclusiones. Sin chats secretos. Los chats nuevos se suman al aparecer; el historial antiguo no se descarga solo.

## 2. Obtener el historial y conservar los archivos

Cree una colección en Case Board y marque lo importante. Lleve un registro de fuentes: ID del chat, título, cuenta, rol, inicio de la captura en vivo, resultado del historial, resultado multimedia y huecos.

| Se necesita | Acción en el panel | Qué ofrece |
| --- | --- | --- |
| Historial de los chats habilitados | Fuentes → Cargar historial completo | Los mensajes anteriores disponibles se incorporan al diario del espacio de trabajo, con funciones de pausa/reanudación y un informe de progreso firmado. [Guía del historial](https://phishdestroy.github.io/TgWitness/es/docs/reference/history/). |
| Contexto del chat existente en el registro | Fuentes → Ajustes de grabación → Instantánea del historial | Mensajes recientes como registros firmados. 500 por defecto, hasta 10 000 en **Parámetros → Captura de historial más grande**. |
| Historial completo, tal y como se muestra actualmente, de un chat | Exportación completa del chat → Exportar el chat completo, o Chats → Exportar chat | Un paquete firmado aparte con `chat.json` y `chat.html`, uno por chat. |
| Contexto en el que aparece un nuevo chat | Ámbito de observación → Cuando aparece un nuevo chat o un nuevo bot | Su perfil y hasta 1000 mensajes recientes (200 en modo investigación). No se aplica a chats existentes. |
| Tamaño del archivo adjunto | Descarga de archivos adjuntos visibles + límites por tipo | Busque `media.saved` con SHA-256 y tamaño. En cola, omitido o fallido significa que no se guardó. |

Una exportación de chat no entra en el diario ni en los perfiles de personas. Para buscar historial antiguo dentro de TgWitness, use **Cargar historial completo** o capturas.

Aquí: el canal, el grupo, el chat del bot y el chat privado, más el archivo de la factura y su hash. Lo borrado antes de la captura ya no vuelve.

## 3. Mantenga el hilo de la conversación y sus propias acciones

Déjelo funcionando. Marque con estrella los chats calientes como prioritarios, ajuste las revisiones en **Ajustes de grabación → Revisión** y vigile `recheck.completed`, FloodWait y los resultados multimedia.

**Chats → Perfil → Guardar perfil ahora** guarda la descripción del chat, los comandos del bot y otros metadatos.

**Seguir a un bot o aceptar una invitación como parte del caso**

1. **Chats → Abrir enlace de Telegram**, guarde primero la vista previa. Enlace y vista previa pasan a ser registros firmados.
2. Si hace falta, **Unirse / abrir y observar** se une al chat o arranca el bot con su parámetro de inicio.
3. Para documentar una acción, responda o use **Pulsar botón** desde el panel. Obtiene `interaction.requested` e `interaction.result` con la respuesta del bot.

Son acciones reales. Los botones pulsados en otra app no se ven, solo la respuesta del bot. Sin web apps, pagos ni teléfono/ubicación.

## 4. Realice un seguimiento de personas, enlaces y archivos en los distintos chats

1. **Diario**, **Todas las fuentes**, busque una frase, un dominio o un usuario. Abra los resultados y envíelos **Al tablero**.
2. **Chats → Personas → Activar perfiles**, elija a alguien: historial de nombres, respuestas, actividad, **También en…**, enlaces, monederos, teléfonos. Abra los registros citados.
3. Siga el mismo ID numérico de usuario en otros chats. Un nombre, monedero o avatar que coincide es una pista, no una prueba.
4. Compare hashes de archivos. Mismo SHA-256 = mismos bytes. Quién los compartió es otra cuestión.

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
| La misma cuenta de Telegram | ID de usuario 71001 en el grupo n.º 146 y en el chat privado n.º 205 | El mismo ID de remitente en los dos chats. Quién es en la vida real es otra cuestión. |
| Destino repetido | `pay.example.invalid/new` en el n.º 146, metadatos del botón en el n.º 173, publicación editada en los n.º 188 y 205 | El mismo enlace en cuatro sitios. Quién lo controla requiere otras fuentes. |
| Mismo número de bytes del archivo | Valores SHA-256 completos idénticos en los recibos multimedia completados n.º 151 y n.º 209 | Los dos archivos son idénticos byte a byte. |

Los perfiles solo cubren a quien escribió algo en *este espacio*; no son una lista de miembros. Citas por hecho: **Parámetros → Registros citados por hecho**.

## 5. Reconstruir la secuencia y señalar las lagunas

Versiones en **Chats**, luego **Diario** con **Todas las fuentes** + **Ediciones**, **Borrados**, **Cobertura**. Ponga las dos horas en la cronología: la fecha de Telegram y cuándo se observó.

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

El orden del diario es el orden de llegada, no necesariamente el orden en que ocurrieron las cosas. Mantenga separados registros en vivo, capturas, mensajes recuperados, borrados y «no encontrado en revisión», y marque cada hueco como desconocido.

## 6. Amplíe el caso a otras cuentas de recopilación

Un espacio por cuenta, mismos pasos. Apunte el rol y la huella de cada uno. Los números de mensaje son por cuenta, así que indique siempre el espacio y el chat.

Un [grupo de cuentas](https://phishdestroy.github.io/TgWitness/es/docs/groups/) muestra el estado, comparte ajustes y exporta a todos juntos, cada uno con su diario y su clave. La cronología entre cuentas la monta usted en sus notas.

¿Caso largo? Añada un [testigo independiente](https://phishdestroy.github.io/TgWitness/es/docs/witness/) y pruebe qué capta realmente cada cuenta.

## 7. Entregar un paquete de caso verificable

Un ZIP firmado de cada espacio (siempre el diario entero; los filtros no importan), más perfiles de personas, exportaciones de chats y archivos.

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

Envíe las huellas por separado. Verifique cada cosa con su propio espacio:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Guarde la salida del verificador, los originales, la cobertura y el registro de entrega con sus conclusiones. Redáctelo en Report studio. Si el destinatario necesita menos, prepare una [entrega minimizada](https://phishdestroy.github.io/TgWitness/es/docs/handover/).
