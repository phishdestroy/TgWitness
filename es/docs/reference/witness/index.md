# Testigo independiente

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/

Ejecute un «witness» con su propia clave y bot, publique puntos de control firmados en un canal y compruebe las exportaciones comparándolas con ellos.

[Configuración del bot y del proxy en ruso](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

Un recopilador firma su propio registro, por lo que quienquiera que controle el recopilador y su clave podría, en principio, reescribir o truncar el registro y volver a firmarlo. Un «testigo» hace que eso sea detectable. Se trata de un proceso independiente —otro contenedor, o mejor aún, un servidor que gestiona otra persona— que, cada pocos minutos, recupera el encabezado del registro firmado del recopilador, firma lo que ha observado con su propia clave, lo guarda en su propio registro y lo publica en un canal de Telegram.

Diagrama de flujo · Recopilador → Witness (Punto de control firmado: recuento de registros + hash de cabecera); Witness → Registro de pruebas, clave propia; Witness → Canal de Telegram (Publicación firmada a través de su propio bot); Archivo ZIP de pruebas → verify.py; Registro de pruebas, clave propia → verify.py; Canal de Telegram → verify.py (Exportación desde Telegram Desktop o página t.me/s) · Recopilador · Witness · Registro de pruebas, clavepropia · Canal de Telegram · Archivo ZIP de pruebas · verify.py · Punto de control firmado: · recuento de registros + hash · de cabecera · Publicación firmada a través · de su propio bot · Exportación desde Telegram · Desktop o página t.me/s

**Diagrama en formato de texto**

1. Recopilador → Witness (Punto de control firmado: recuento de registros + hash de cabecera)
2. Witness → Registro de pruebas, clave propia
3. Witness → Canal de Telegram (Publicación firmada a través de su propio bot)
4. Archivo ZIP de pruebas → verify.py
5. Registro de pruebas, clave propia → verify.py
6. Canal de Telegram → verify.py (Exportación desde Telegram Desktop o página t.me/s)

## Lo que TgWitness ofrece y lo que no ofrece

| El testigo tiene | El testigo nunca tiene |
| --- | --- |
| Un **token de testigo** de solo lectura para un espacio de trabajo | La sesión de Telegram del recopilador o sus credenciales de la API |
| Su propia clave Ed25519 y su propio registro | La bóveda del recopilador, la clave de firma o el token del panel |
| Su propio token de bot de Telegram | Contenido del mensaje: el encabezado incluye el recuento de registros y un hash |

El token se crea en la página **«Witness»** del panel, se muestra una sola vez y se almacena únicamente como un SHA-256. Abre exactamente un punto final, `GET /api/witness/head`, que devuelve un punto de control recién firmado, además de contadores de recopilación sin contenido firmados y el estado operativo. No puede abrir el panel, leer el contenido de los mensajes ni modificar la configuración, y el token del panel no es válido en ese contexto. La revocación de un token se realiza en la misma página. El recopilador registra cuándo comienza a comprobarse una nueva clave de testigo (`witness.seen`) y muestra la última comprobación por token; un testigo que no se haya comprobado en un plazo de 2,5 intervalos se marca como vencido.

Los nuevos testigos envían un desafío aleatorio en cada encuesta; la declaración de captura lo repite bajo la firma del recopilador. Los contadores están vinculados al punto de control exacto y se incluyen en las publicaciones firmadas de los testigos. Los encabezados heredados siguen siendo aceptados por el testigo independiente. El mero crecimiento del registro nunca se cuenta como un nuevo mensaje.

## Qué comprueba y registra

Cada intervalo (10 minutos por defecto), TgWitness:

1. recoge el encabezado por sí mismo (el recopilador no puede forzarlo ni omitirlo);
2. verifica la firma del recopilador, la clave de recopilador fijada (`--collector-fingerprint`, o la primera clave que se observe), un recuento no decreciente y un encabezado inalterado con un recuento inalterado;
3. añade un registro firmado a su propio diario: `witness.anchor` con estado `ok`, `key_changed`, `rollback` (menos registros que antes), `fork` (misma longitud, diferente encabezado) o `invalid` (la respuesta no superó la verificación), o `witness.no_response` cuando el recopilador no respondió;
4. Publica el resultado en el canal, firmado, incluyendo «sin respuesta» mientras TgWitness está en funcionamiento y puede acceder a la API del bot. Se registra el ID de la publicación (`witness.posted`), así como una publicación fallida (`witness.post_failed`).

Una entrada tiene este aspecto; la última línea contiene la declaración firmada:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Ejecutar un «witness»

Necesitará un bot de Telegram (cree uno con @BotFather), un canal en el que dicho bot sea administrador y la dirección del recopilador accesible desde el testigo —a través de HTTPS fuera de una red privada (consulte el perfil HTTPS en [la sección de implementación](https://phishdestroy.github.io/TgWitness/es/docs/reference/deployment/)).

Seleccione **«Extras» → «Un bot en su canal» → «Configurar un bot»** en el panel. Se siguen tres pasos que abarcan el acceso de solo lectura, su canal y el intervalo, para, a continuación, iniciar el testigo. La política de publicación, el proxy HTTP/SOCKS5 opcional y la dirección personalizada de la API del bot se encuentran en **la configuración avanzada** . El formulario descarga `witness.json` con la clave del colector de este espacio de trabajo fijada. Descargue el token de solo lectura recién creado con **«Guardar archivo de acceso** como `witness-token.txt` »; colóquelo junto con un `bot-token.txt` creado en el servidor del testigo junto a ese archivo JSON. El colector nunca recibe el token del bot. La descarga no inicia ningún servicio ni publica ningún mensaje. No se inscribe implícitamente ningún testigo de proyecto alojado .

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

El primer comando comprueba los archivos de configuración y los archivos secretos sin realizar solicitudes de red ni crear claves. Las rutas en JSON son relativas a ese archivo; las rutas de la CLI o del entorno son relativas al directorio de trabajo. Conserve la huella digital del testigo fuera de su servidor. El indicador de última consulta del recopilador solo confirma una solicitud; la publicación se notifica mediante Proof o se comprueba en el diario y el canal del testigo.

Si el panel se encuentra detrás de un túnel SSH, exponga únicamente el punto final de Witness con ámbito limitado en un nombre de host HTTPS independiente, tal y como se muestra en [este ejemplo de Caddy](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example). El espacio de trabajo predeterminado utiliza entonces `https://witness.example.org`, mientras que los demás espacios de trabajo utilizan `https://witness.example.org/profiles/ID`. Siguen siendo necesarios los tokens; el panel y sus demás rutas de API no se reenvían a través de ese host virtual.

Elija `all` para obtener registros publicados periódicamente. Un intervalo de cinco minutos supone unas 288 entradas por espacio de trabajo al día. `changes` y `problems` omiten deliberadamente la publicación de algunos registros. MTProxy está destinado al cliente de Telegram del recopilador. El sondeo HTTP de Witness y la API HTTPS para bots de Telegram utilizan su propia ruta directa/HTTP/SOCKS5 ([API para bots](https://core.telegram.org/bots/api)).

**Junto al colector, con Docker** (mismo host —proceso y clave independientes, pero el mismo operador—): introduzca los valores en «`.env`» e inicie el perfil.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

Si se utiliza una imagen publicada, utilice el código `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**En el servidor de un tercero** (un testigo independiente real): copie allí el repositorio, configure `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` más los tres valores anteriores en `.env`, y a continuación

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

o sin Docker:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Opciones

| Opción | Entorno | Por defecto | Significado |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Intervalos entre comprobaciones: de 1 a 1440 |
| `--timeout` | `_TIMEOUT` | 30 | Tiempo de espera en segundos para el recopilador y la API del bot: de 5 a 600 |
| `--post` | `_POST` | `all` | `all`: todo en orden; `changes`: un nuevo problema; `problems`: solo problemas y respuestas que faltan |
| `--title` | `_TITLE` | `TgWitness witness` | Primeras palabras de cada publicación en el canal |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | Fije la clave del recopilador en lugar de confiar en la primera respuesta |
| `--proxy` | `_PROXY` | directo | `socks5://host:port` o `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Dirección de la API del bot, por ejemplo, un servidor local de la API del bot |
| `--data-dir` | `_DATA` | `witness-data` | Clave de Witness y registro |
| `--config` | `_CONFIG` | – | Archivo JSON con cualquiera de las opciones anteriores |

La dirección del recopilador, los tokens y el canal proceden de `--collector`, `--token` o `--token-file`, `--bot-token` o `--bot-token-file` y `--channel`, o bien de `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE` y `_CHANNEL`, lo que mantiene la confidencialidad fuera de la lista de procesos.

Un archivo de configuración utiliza los nombres de las opciones con guiones bajos, además de «`texts`», que sustituye las palabras de las publicaciones del canal:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Claves `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. La línea de comandos tiene prioridad sobre el entorno, y el entorno sobre el archivo. Las opciones desconocidas o las claves de texto detienen el proceso de registro con un mensaje, en lugar de ser ignoradas. La redacción nunca afecta a la verificación: verify.py comprueba el token firmado al final de cada publicación. Con `--post changes` o `problems`, las comprobaciones que no se han publicado siguen figurando en el diario de testigos y `verify.py` las enumera como nunca publicadas; el registro inicial indica la política. Todas las comprobaciones siguen apareciendo en el diario, por lo que un menor número de publicaciones implica un menor número de momentos independientes de Telegram, no un menor número de comprobaciones.

Aunque no haya un canal, TgWitness sigue manteniendo su registro. Guarde la huella digital de la clave de TgWitness (`python -m tgwitness.witness fingerprint`) en otro lugar.

## Verificar

Desde el punto de vista del testigo, exportar su registro:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

A continuación, desde cualquier lugar, con el archivo ZIP firmado del recopilador y el canal exportado desde Telegram Desktop (*Exportar historial de chat* → JSON genera `result.json` ) o su página pública `https://t.me/s/…` :

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` comprueba el registro de TgWitness (cadena y firmas) y, a continuación, verifica que **cada «head» que el testigo haya visto forme parte del registro exportado**: el registro en ese recuento debe tener exactamente ese hash. Un «head» que no coincida no supera la verificación —el registro se modificó después de que el testigo lo viera—. Asimismo, informa de los cabezales vistos tras la exportación, las anomalías que el testigo ha registrado, las respuestas que han fallado, los periodos cuyos puntos de control coincidentes están presentes en esta exportación («Testificado de X a Y») y las lagunas. Los puntos de control posteriores no amplían dichos periodos. El resultado incluye el último número de registro coincidente y el número de registros posteriores sin un punto de control coincidente. Solo cuentan las respuestas firmadas con la propia clave de la exportación: una exportación firmada con una clave que el testigo nunca haya visto se notifica como no atestiguada y, sin `--fingerprint`, su firmante permanece sin verificar. Con «`--channel`», cada publicación firmada debe coincidir con el diario del testigo registro por registro: las publicaciones modificadas no superan la verificación y las publicaciones que faltan se enumeran. Una fecha en una exportación JSON de Telegram facilitada es un metadato editable, ajeno al token de testigo firmado. La coincidencia con el token no autentica la fecha de publicación; el resultado indica explícitamente que no se ha realizado la verificación de la hora de publicación.

### Se requiere un límite de exportación con certificación

Para un traspaso que deba incluir un registro final certificado, añada `--require-witness`:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

Para ello se requiere la huella digital del testigo conservada de forma independiente y un punto de control coincidente justo al final de esta exportación. Un punto de control que abarque únicamente un prefijo anterior resulta insuficiente. Detenga la recopilación, permita que el testigo observe el estado final y realice la exportación antes de que se produzcan nuevas escrituras en el registro; si el registro cambia, conserve otro punto de control y exporte ese estado. Un punto de control posterior por sí solo no puede verificar el hash final de una exportación más corta. Cuando también se proporciona «`--channel`», la falta de publicaciones declaradas o un conjunto de coincidencias vacío hacen que se falle esta estricta comprobación. Sin el indicador, las comprobaciones de integridad habituales siguen informando de registros sin testificar sin rechazar un archivo que, por lo demás, está intacto.

La marca garantiza la coherencia con los registros de testigos facilitados y fijados. El operador debe seguir acreditando la independencia del testigo y conservar sus registros por separado. No garantiza la veracidad de los mensajes, la recopilación completa ni un tiempo de ejecución medido de forma independiente.

Un «testigo» muestra lo que el recopilador informó en esos momentos y que las exportaciones posteriores concuerdan con ello. No muestra que el recopilador haya registrado todo lo que Telegram entregó, ni que el contenido de los mensajes sea veraz. Un «testigo» ejecutado por el mismo operador en la misma máquina tiene menos valor que uno ejecutado por otra persona.

El mero aumento del recuento no basta para establecer la continuidad de «solo adición» en línea: la comparación fuera de línea debe cotejar cada hash de prefijo conservado con la exportación completa del colector. El tiempo de inactividad de Witness y los fallos en la publicación dejan intervalos sin referencias externas. Las publicaciones que faltan pueden notificarse comparando con un registro de Witness conservado; ni un canal ni un servidor controlado por el mismo operador constituyen un archivo inmutable de terceros.
