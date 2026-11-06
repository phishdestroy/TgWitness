# Telegram · Testigo independiente

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/

Ejecute un «witness» con su propia clave y bot, publique puntos de control firmados en un canal y compruebe las exportaciones comparándolas con ellos.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentación](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Pruebas y verificación](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/)

![Pruebas y verificación](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

[Exportar y verificar](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/) · [Alta fiabilidad](https://phishdestroy.github.io/TgWitness/es/docs/reference/high-assurance/) · [Guía de paneles](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/#extras)

Un testigo conserva los puntos de control firmados por separado del recopilador. Comprueba la firma del recopilador y la continuidad del diario, firma el resultado con su propia clave y lo publica en un canal de Telegram. Ejecútalo en un servidor independiente con acceso de solo lectura al punto final del testigo del recopilador.

Diagrama de flujo · Recopilador → Testigo (Punto de control firmado: recuento de registros + hash de cabecera); Testigo → Registro de pruebas, clave propia; Testigo → Canal de Telegram (Publicación firmada a través de su propio bot); Archivo ZIP de pruebas → verify.py; Registro de pruebas, clave propia → verify.py; Canal de Telegram → verify.py (Exportación desde Telegram Desktop o página t.me/s) · Recopilador · Testigo · Registro de pruebas, clavepropia · Canal de Telegram · Archivo ZIP de pruebas · verify.py · Punto de control firmado: · recuento de registros + hash · de cabecera · Publicación firmada a través · de su propio bot · Exportación desde Telegram · Desktop o página t.me/s

**Diagrama en formato de texto**

1. Recopilador → Testigo (Punto de control firmado: recuento de registros + hash de cabecera)
2. Testigo → Registro de pruebas, clave propia
3. Testigo → Canal de Telegram (Publicación firmada a través de su propio bot)
4. Archivo ZIP de pruebas → verify.py
5. Registro de pruebas, clave propia → verify.py
6. Canal de Telegram → verify.py (Exportación desde Telegram Desktop o página t.me/s)

**En esta página**

- [Lo que obtiene el testigo y lo que no](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/#what-the-witness-gets-and-what-it-does-not)
- [Qué comprueba y registra](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/#what-it-checks-and-records)
- [Ejecutar un testigo](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/#run-a-witness)
- [Página de pruebas pública para varios espacios de trabajo](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/#public-proof-page-for-several-workspaces)
- [Verificar](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/#verify)

## Lo que TgWitness ofrece y lo que no ofrece

| El testigo tiene | El testigo nunca tiene |
| --- | --- |
| Un **token de testigo** de solo lectura para un espacio de trabajo | La sesión de Telegram del recopilador o sus credenciales de la API |
| Su propia clave Ed25519 y su propio registro | La bóveda del recopilador, la clave de firma o el token del panel |
| Su propio token de bot de Telegram | Contenido del mensaje: el encabezado incluye el recuento de registros y un hash |

El token se crea en **Extras → Testigo independiente**, se muestra una sola vez y se almacena únicamente como un SHA-256. Abre exactamente un punto final, `GET /api/witness/head`que devuelve un punto de control recién firmado, además de contadores de colecciones sin contenido firmados y el estado operativo. No puede abrir el panel, leer el contenido de los mensajes ni modificar la configuración, y el token del panel no se acepta allí. Revoca un token en la misma página. El recopilador registra cuándo una nueva clave de testigo comienza a comprobar (`witness.seen`) y muestra la última comprobación por token; un testigo que no haya realizado una comprobación en un plazo de 2,5 intervalos se marca como vencido.

Los nuevos testigos envían un desafío aleatorio en cada encuesta; la declaración de captura lo repite bajo la firma del recopilador. Los contadores están vinculados al punto de control exacto y se incluyen en las publicaciones firmadas de los testigos. Los encabezados heredados siguen siendo aceptados por el testigo independiente. El mero crecimiento del registro nunca se cuenta como un nuevo mensaje.

## Qué comprueba y registra

Cada intervalo (10 minutos por defecto), TgWitness:

1. recoge el encabezado por sí mismo (el recopilador no puede forzarlo ni omitirlo);
2. Verifica la firma del recopilador, la clave del recopilador fijada (`--collector-fingerprint`, o la primera clave vista), un recuento no decreciente y una cabecera inalterada con un recuento inalterado. Las pruebas de inclusión y consistencia de Merkle verifican que un diario creciente amplíe el punto de control conservado. Una vez que se han utilizado las pruebas de continuidad, se rechaza su eliminación;
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

Abre **Extras → Testigo independiente → Configurar** en el panel. Hay tres pasos que abarcan el acceso de solo lectura, tu canal y el intervalo, y, a continuación, el inicio del testigo. La política de publicación, el proxy HTTP/SOCKS5 opcional y la dirección personalizada de la API del bot se encuentran en **la configuración avanzada**. El formulario se descarga `witness.json` con la clave del colector de este espacio de trabajo fijada. Descarga el token de solo lectura recién creado con **«Guardar archivo de acceso** como» `witness-token.txt`; colócalo junto a un `bot-token.txt`creado en el host del testigo junto a ese JSON. El colector nunca recibe el token del bot. La descarga no inicia ningún servicio ni publica ningún mensaje. No se inscribe implícitamente ningún testigo de proyecto alojado .

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

### Publicar en Discord

Un testigo puede publicar en un canal de Discord en lugar de en Telegram. En Discord, abre **«Editar canal» → «Integraciones» → «Webhooks»**, crea un webhook y copia su URL. En el panel, selecciona **«Webhook de Discord · tu canal»** en el paso 2. En el servidor del testigo, guarda la URL como `discord-webhook.txt` junto a `witness.json`; nunca llega al recopilador.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

Un «witness» tiene un único emisor: un canal de Telegram o un webhook de Discord, pero no ambos. Las publicaciones incluyen la misma declaración firmada y no pueden mencionar a nadie. Una publicación que supere los 2.000 caracteres de Discord se sustituye por una línea breve con el registro completo adjunto como `witness-check.txt`. Cada ID de publicación se registra como `witness.posted`. `verify.py --channel`solo lee las exportaciones de los canales de Telegram, por lo que, para Discord, hay que llevar el diario de «witness»: este contiene todas las comprobaciones.

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

La dirección del recopilador, los tokens y el canal proceden de `--collector`, `--token` o `--token-file`, `--bot-token` o `--bot-token-file`, `--discord-webhook-file` y `--channel`, o `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` y `_CHANNEL`, lo que mantiene los secretos fuera de la lista de procesos.

Un archivo de configuración utiliza los nombres de las opciones con guiones bajos, además de «`texts`», que sustituye las palabras de las publicaciones del canal:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Claves `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. La línea de comandos tiene prioridad sobre el entorno, y el entorno sobre el archivo. Las opciones desconocidas o las claves de texto detienen el proceso de registro con un mensaje, en lugar de ser ignoradas. La redacción nunca afecta a la verificación: verify.py comprueba el token firmado al final de cada publicación. Con `--post changes` o `problems`, las comprobaciones que no se han publicado siguen figurando en el diario de testigos y `verify.py` las enumera como nunca publicadas; el registro inicial indica la política. Todas las comprobaciones siguen apareciendo en el diario, por lo que un menor número de publicaciones implica un menor número de momentos independientes de Telegram, no un menor número de comprobaciones.

Aunque no haya un canal, TgWitness sigue manteniendo su registro. Guarde la huella digital de la clave de TgWitness (`python -m tgwitness.witness fingerprint`) en otro lugar.

## Página pública de verificación para varios espacios de trabajo

`python -m tgwitness.proof` TgWitness admite hasta 32 espacios de trabajo a la vez y ofrece una página de solo lectura con la última comprobación firmada de cada uno. Cada espacio de trabajo tiene su propia clave de testigo y su propio diario en la carpeta «data», así como una clave de recopilador fijada; la publicación en un canal de Telegram es opcional para cada espacio de trabajo. Empieza por [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example):

| Campo | Significado |
| --- | --- |
| `title` | Título de la página, de 1 a 100 caracteres |
| `data_dir` | Claves y registros de Witness, relativos al archivo; por defecto `proof-data` |
| `interval`, `timeout` | Mínimos entre comprobaciones (1–1440, por defecto 5); segundos de espera (5–600, por defecto 20) |
| `workspaces[].id`, `label` | Alias corto en minúsculas y el nombre que se muestra |
| `workspaces[].collector` | Dirección del «Collector»; los demás espacios de trabajo terminan en `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | Obligatorio, varía según cada espacio de trabajo |
| `workspaces[].token_file` | Archivo con el token de testigo de solo lectura de ese espacio de trabajo |
| `workspaces[].channel`, `bot_token_file` | Opcional, en conjunto: publicar cada comprobación en un canal |
| `workspaces[].proxy`, `bot_api` | Ruta opcional y dirección de la API del bot |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

El primer comando valida el archivo y los archivos de tokens sin establecer una conexión. La página solo responde a las solicitudes GET y HEAD:

- `/` Muestra todos los espacios de trabajo; un espacio de trabajo que no se haya comprobado durante 2,5 intervalos se marca como obsoleto.
- `/api/proof` Devuelve lo mismo que JSON.
- `/api/proof/<id>` descarga la última declaración firmada (`tgwitness-public-proof-v1`): número y hash del registro del testigo, estado, clave del recopilador fijada, punto de control, contadores de recopilación y si la publicación en el canal se ha realizado con éxito, firmado por la clave de testigo de ese espacio de trabajo.
- `/healthz` Devuelve el código de error 503 cuando el monitor de un espacio de trabajo se ha detenido.

Asigna a la página su propio nombre de host, como en [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example). Para su verificación, exporta el diario de testigos de un espacio de trabajo con `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` y utilízalo tal y como se describe a continuación.

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

Mantener el diario de testigos y su clave fijada por separado. Las comprobaciones en línea verifican la continuidad entre los puntos de control; la verificación fuera de línea compara cada punto de control conservado con la exportación. Los cabezales heredados sin pruebas de continuidad conservan la comparación fuera de línea y se incluyen en el informe sin la verificación de continuidad en línea. El informe enumera el tiempo de inactividad de los testigos y las publicaciones fallidas por intervalos.

### Sellos diarios y calendarios de marcas de tiempo no disponibles

El testigo sella el límite del diario del día anterior (UTC) y envía el hash de ese sello firmado a OpenTimestamps. Un envío al calendario es una prueba pendiente; solo los compromisos de Bitcoin verificados de forma independiente reciben confirmación en el verificador.

Si fallan todos los calendarios, el sello firmado y el intento fallido permanecen en el registro. La ronda de mantenimiento horaria vuelve a intentar ese registro original, incluso tras un reinicio o un cambio de fecha. Analiza como máximo 32 sellos, envía como máximo dos envíos pendientes y dedica como máximo 60 segundos a los reintentos por pasada. Un cursor persistente va rotando por los sellos más antiguos. Los envíos retenidos siguen la ruta de actualización de pruebas existente.

Un nuevo intento no reescribe el sello, ni cambia su fecha original, ni afirma que el calendario lo haya recibido antes. Un compromiso posterior de Bitcoin sigue siendo una confirmación externa posterior. Las pruebas que faltan siguen siendo `none`; las pruebas pendientes siguen siendo `pending` hasta que el verificador las compruebe de forma independiente.
