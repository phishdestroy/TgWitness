# Lo que se ha probado

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/

La prueba en tiempo real de Telegram, las comprobaciones automatizadas, las comprobaciones en el navegador y lo que aún no se ha verificado.

## Despliegue en Phala Cloud en tiempo real · 4 de noviembre de 2026

`--provider phala --quick-tunnel` se ejecutó en un entorno real **Phala Cloud** (`tdx.small`, región US-WEST-1) con una clave de la API de Phala Cloud de un espacio de trabajo vacío, el archivo ntfy.sh real, GitHub e Intel PCS. La CVM instaló la confirmación `df7d860c` (v0.8.1); las operaciones de implementación, verificación y eliminación se ejecutaron desde la línea de comandos con las correcciones que se indican a continuación. Siete CVM costaron en total unos 1,9 céntimos de dólar estadounidense.

Las dos primeras implementaciones detectaron cinco diferencias con respecto a la Phala Cloud simulada. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) ahora reproduce cada una de ellas y falla si no se aplica la corrección correspondiente:

| En Phala Cloud | Antes de la corrección | Solución |
| --- | --- | --- |
| Se requiere `compose_file.name` | HTTP 422, no se ha creado nada | La configuración de Docker Compose incluye el nombre de la CVM |
| A menos que se le proporcione uno vacío, Phala añade su propio script de preinicio al «app-compose» evaluado (v0.0.20: inicio de sesión en Docker, `docker compose pull`, contraseña de root, claves SSH de `user_config`) | `tdx_compose` falla: código fuera de la configuración publicada de Docker Compose | El «app-compose» establece `pre_launch_script` en `""`; Phala, a continuación, lo omite |
| Sin `image`, Phala selecciona `dstack-dev-0.5.12`, la versión de desarrollo, con acceso SSH habilitado | `server_state` falla. En esta imagen, solo se ha superado el registro de certificación de hardware; únicamente el registro del proveedor y `tdx_os` lo muestran. | La implementación solicita la versión de producción de la actual versión de Phala, `dstack-0.5.12` |
| Con la pasarela dstack desactivada, los detalles de la CVM nunca muestran un `instance_id` | La implementación espera 30 minutos y falla | El ID de la instancia se lee del estado de la CVM |
| Los reinicios, las paradas y los arranques son operaciones de la CVM, no revisiones de la aplicación | `provider_actions` no incluyó los reinicios | Las operaciones también se leen |

Tercera implementación:

- La CVM ejecutó `dstack-0.5.12` con el acceso SSH desactivado. El colector publicó su dirección firmada aproximadamente 1,5 minutos después de su creación. A continuación, la implementación superó las pruebas de `tdx_binding` y `tdx_quote` (Intel TCB UpToDate, registro de certificación de hardware v4, FMSPC `20a06f000000`, sin modo de depuración, no migrable, compatible con datos de verificación criptográfica obtenidos de Intel), `tdx_compose_hash`, `tdx_compose` (byte a byte) y `tdx_identity` (claves KMS).
- El panel, en su dirección trycloudflare.com, devolvió un código de estado 401 sin token o con uno incorrecto, y un 200 con el token del panel.
- `verify` con `--source` configurado en el archivo de GitHub de la confirmación y la huella digital superada por separado: servidor, `server_state`, cortafuegos (sin puerta de enlace, sin punto final público), registro del proveedor, extracto, huella digital, hash de origen, arranque y las cinco comprobaciones `tdx_*` superadas. Cloudflare y `tdx_os` no estaban disponibles, por lo que el resultado fue INCOMPLETO.
- Dos reinicios a través de la API de Phala: en cada ocasión, la CVM volvió a estar operativa en menos de dos minutos con la misma clave de recopilador, una nueva dirección firmada y la antigua respondiendo con el código 530. `verify` notificó el nuevo arranque y ambos reinicios como REVIEW. Con `--evidence` se confirmaron las firmas del diario y tres arranques, cada uno con su propio registro de certificación de hardware Intel TDX procedente del mismo CVM.
- `destroy` eliminó únicamente esa CVM. A continuación, el espacio de trabajo quedó vacío y la dirección del panel dejó de responder.
- La comprobación de precios del asistente del panel indicaba `tdx.small` a 0,058 dólares por hora. Al introducir una clave incorrecta, apareció un mensaje sencillo que decía «no se ha aceptado la clave de API».

Otros dos hallazgos, corregidos posteriormente:

- Sin la clave de dirección, `verify` siguió la última publicación bien formada sobre el tema de la dirección, que figura en la configuración de Docker Compose publicada. Una publicación falsificada lo envió a un host que no existe, y `statement` falló: un falsificador no pudo hacerse pasar por el recopilador, pero sí pudo bloquear la verificación de terceros durante un máximo de 12 horas con una marca de tiempo futura falsificada. El recopilador ahora también publica su dirección firmada con su propia clave; `verify` solo acepta dichas publicaciones cuando el recopilador las realiza, y las publicaciones se ordenan según la hora de recepción de ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) reproduce las publicaciones falsificadas. Un CVM ejecuta esto únicamente desde una confirmación que lo contenga, por lo que el recopilador de esta ejecución aún no había firmado su dirección y `verify` así lo indicó.
- `tdx_os` no pudo ejecutarse sin `dstack-mr`, cuya versión actual es `measure-os` en lugar de el `measure --json` que figuraba en la documentación. El verificador calcula ahora por sí mismo MRTD y RTMR0-2 a partir de la imagen publicada y la configuración de la máquina virtual, incluidas las tablas ACPI.

La cuarta implementación, con los siguientes elementos:

- Deploy descargó una vez el archivo `dstack-0.5.12` publicado, lo comparó con el hash de la imagen del sistema operativo que la CVM notificó, y `tdx_os` superó la comprobación: MRTD, RTMR0, RTMR1 y RTMR2 coinciden con los valores calculados para QEMU 8.2.2, 1 vCPU y 2 GiB. El mismo cálculo arrojó un valor de RTMR0 diferente para una configuración declarada de 4 GiB, 2 vCPU, QEMU 9.2.1 o una segunda tarjeta de red, y falló en caso de cambios en el kernel, el firmware o la línea de comandos, así como para la imagen de desarrollo.
- `verify` superó cada una de sus 16 comprobaciones, incluido el conector del túnel rápido, por lo que el resultado fue «APROBADO». Generó el certificado en formato HTML y PDF, sellado digitalmente con firmas y marcas de tiempo mediante una marca de tiempo eIDAS cualificada de la unidad de marcado de tiempo del Gobierno belga TSU 202301 (estatus concedido en la lista de confianza de Bélgica), una marca de tiempo FreeTSA y la firma del verificador; `check-report` confirmó todos ellos y la firma del PDF.
- Tras un reinicio, `verify --evidence` confirmó dos arranques, cada uno acompañado de una certificación de hardware generada dentro de la CVM y cada uno iniciado desde el `dstack-0.5.12` publicado; tanto el reinicio como el nuevo arranque fueron de tipo REVIEW.
- `destroy` dejó el espacio de trabajo vacío.

La quinta implementación ejecutó el colector a partir de la confirmación `53a0f7e9`, que incluye todo lo anterior:

- El recopilador publicó su dirección firmada con su propia clave, junto a la publicación HMAC del operador. A continuación, se añadieron dos publicaciones falsificadas al tema, una con un HMAC a cero y otra firmada por otra clave Ed25519, ambas con una fecha del año 2096. `verify` tomó la dirección firmada por la clave del recopilador y superó las 16 comprobaciones; el sello volvía a incluir el sello de tiempo belga certificado, el sello de tiempo de FreeTSA y la firma del verificador, y `check-report` los confirmó.
- Tras un reinicio, el colector publicó la nueva dirección firmada: `verify` la detectó de inmediato; el operador **«Buscar la dirección actual»**, 27 segundos más tarde a partir de la publicación HMAC, y ambos ignoraron las publicaciones falsificadas. `verify --evidence` confirmó dos arranques iniciados desde `dstack-0.5.12`.
- La implementación mostró lo que Phala factura por la CVM, disco incluido: 0,06078 dólares por hora.

El asistente del panel se ejecutó en Phala Cloud en dos ocasiones: una a través de su API de tareas y otra a través del navegador con un Chromium real: la comprobación del precio, la creación con la confirmación bajo **Advanced**, las seis comprobaciones de certificación superadas, la lista de servidores que muestra el precio facturado (44,37 USD al mes), **Find la dirección actual**, la descarga de la configuración de Docker Compose medida y la eliminación. El navegador no detectó ningún error en las páginas. En ambas ocasiones, el espacio de trabajo quedó vacío posteriormente.

No se incluyen: un dominio de Cloudflare en Phala, una cuenta de Telegram en la CVM y la imagen `dstack-0.6.1` . El precio que indica el asistente antes de la creación corresponde únicamente al coste de computación de Phala, ya que su API solo especifica el coste del disco para una CVM ya existente; la lista de servidores muestra el precio facturado tras la creación.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Recuento |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| Comprobar | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Prueba en directo de Telegram, cuenta completa · 29 de octubre de 2026

La misma cuenta siguió funcionando tras la prueba que se describe a continuación. El 29 de octubre a las 12:10 UTC, su ámbito de aplicación se amplió a toda la cuenta (canales, grupos, chats privados y bots); el panel solicitó confirmación y el registro firmado lo dejó constancia. A las 17:59 UTC, el registro contenía:

| Registrado del 27 de octubre a las 21:36 al 29 de octubre a las 17:59 UTC | Recuento |
| --- | --- |
| Registros del diario | 9,968 |
| Nuevos mensajes | 5,308 |
| de ellos tras el cambio a la cuenta completa | 3,878 |
| Eliminaciones | 784 |
| de ellos se eliminaron después de que TgWitness hubiera guardado el mensaje | 596 |
| Modificaciones | 41 |
| Mensajes añadidos tras nuevas comprobaciones | 2,273 |
| Mensajes que ya no se pudieron localizar tras una nueva comprobación | 18 |
| Mensajes guardados mediante instantáneas del historial | 242 |
| Archivos adjuntos guardados | 247 |
| El recopilador se inicia | 19 |
| Pausas de Telegram FloodWait | 26 |

- La comprobación **«Verify»** del panel confirmó las firmas y la cadena de hash de los 9.968 registros.
- Los mensajes procedían de 2 grupos o canales y de 3 chats privados y bots. Se pulsó un botón de mensaje desde **«Chats»**; la solicitud y la respuesta de Telegram figuran en el registro.
- Se añadieron nuevos chats cuando el recopilador volvió a escanear la cuenta tras un reinicio. La opción de guardar los mensajes anteriores de los nuevos chats estaba desactivada (`history = 0`), por lo que no se trata aquí.

No se incluyen: reacciones, cambios en la composición de los grupos, perfiles de usuarios, envío de mensajes, incorporación mediante invitación, proxies, notificaciones, el bot «witness» ni el uso simultáneo de varias cuentas. Los archivos públicos solo contienen recuentos.

## Exportación protegida con contraseña que se abre con libarchive · 29 de octubre de 2026

Se abrió un archivo creado mediante el código de cifrado de exportación (WinZip AES-256, el formato que leen 7-Zip y WinRAR ) con Windows `tar` (bsdtar 3.6.2, libarchive). Con la contraseña correcta, el archivo extraído coincidió con el SHA-256 original; si se introducía una contraseña incorrecta, se rechazaba con el mensaje «Contraseña incorrecta». No se ejecutaron los propios programas 7-Zip ni WinRAR.

## Prueba en directo de Telegram · Del 27 al 29 de octubre de 2026

Una cuenta real de Telegram, conectada a través del conjunto de pares de API integrado, registró un supergrupo desde **las 21:36 UTC del 27 de octubre hasta las 05:15 UTC del 29 de octubre**. El recopilador se inició 12 veces durante ese periodo.

| Registrado | Recuento |
| --- | --- |
| Registros del diario, incluidos los «heartbeats» y los registros de servicio | 2,385 |
| Nuevos mensajes | 1,291 |
| Eliminaciones | 472 |
| de ellos se eliminaron después de que TgWitness hubiera guardado el texto | 347 |
| Modificaciones | 12 |
| Mensajes que se perdieron mientras la herramienta estaba detenida, añadidos tras una nueva comprobación | 12 |
| Archivos adjuntos guardados | 17 |
| Archivos adjuntos no descargados (descargas desactivadas o no hay ningún archivo que descargar) | 14 |
| Telegram FloodWait realiza pausas de 3 segundos cada una durante las revisiones | 8 |

- Las firmas y la cadena de hash de los 2.385 registros se verifican con la clave pública del registro.
- Tras un reinicio, el recopilador reanuda su funcionamiento desde el estado de actualización guardado (`pts`) y Telethon se pone al día; a continuación, la nueva comprobación añade los mensajes que aún faltan.
- En cada FloodWait, el recopilador esperaba el tiempo solicitado y continuaba.
- La cuenta permaneció conectada y la misma sesión se volvió a conectar el 29 de octubre.

No se incluyen en esta prueba: varias cuentas a la vez, roles de administrador, proxies, interrupciones de servicio de más de unas pocas horas y el [procedimiento completo de aceptación en tiempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Los archivos públicos contienen únicamente estos datos: no incluyen identificadores de cuentas ni de chats, mensajes ni credenciales.

## Medición sintética de la capacidad local

Comando: `python tools/check_capacity.py --events 10000 --chats 100`

| Métrica | Observado |
| --- | --- |
| Datos de entrada | 10 000 eventos de mensajes sintéticos procedentes de 100 fuentes sintéticas seleccionadas |
| Texto del mensaje | 400 caracteres; sin archivos multimedia ni menciones a redes sociales |
| Ingestión | 53,273 segundos; 187,7 eventos por segundo |
| Latencia del controlador | p50 4,162 ms; p95 7,784 ms; máximo 129,118 ms |
| Exportación en formato ZIP | 19,868 segundos con tracemalloc activado |
| Picos de asignaciones de exportación de Python rastreadas | 0,51 MiB; no procesa RSS |
| Tamaño del archivo ZIP | 4 610 962 bytes |
| Verificación independiente | Los 10 000 eventos han sido verificados |

Esto mide la ruta local de grabación/exportación en serie en este equipo con Windows. No mide la entrega de MTProto, las cuentas simultáneas, la limitación de Telegram, los archivos multimedia, una carga de trabajo de larga duración ni un número garantizado de chats reales. La medición es anterior a la herramienta definitiva de marcas de tiempo fuera de línea, que no modifica la ruta de los mensajes medidos.

## Cualificación restante

El registro en tiempo real conservado recoge de forma fehaciente las recopilaciones, modificaciones, avisos de eliminación, archivos adjuntos, nuevas comprobaciones y la gestión de los límites de frecuencia. No registra de forma exhaustiva la entrega ni ofrece una matriz controlada de visibilidad de roles, agentes de reacción, esperas prolongadas (FloodWait), bloqueos de cuentas y recuperación tras interrupciones de red o procesos. La emisión de tokens QR sigue siendo independiente de la confirmación completa del código QR en el móvil.

La compilación y ejecución en Docker, la instalación en Linux y macOS, la capacidad para soportar cargas elevadas de forma sostenida, la revisión de seguridad independiente, una respuesta TSA verdaderamente independiente, la validación de la revocación y el archivo de certificados, así como la certificación forense, quedan fuera de la certificación obtenida. Se han implementado el estado guardado de MTProto y la puesta al día; la reproducción atómica duradera sigue sin estar establecida. La recopilación de registros de administración, las listas de reactores adicionales y el sondeo corto prioritario siguen siendo características independientes. Consulte [la aceptación en tiempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) para consultar la matriz de cualificación controlada.

Los recibos locales detallados y las capturas de pantalla se encuentran en la carpeta test-results/ (ignorada por Git). La captura de pantalla pública que se encuentra en docs/assets/ contiene únicamente datos de demostración ficticios.
