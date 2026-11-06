# Lo que se ha probado

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/

La prueba en tiempo real de Telegram, las comprobaciones automatizadas, las comprobaciones en el navegador y lo que aún no se ha verificado.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentación](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Pruebas y verificación](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/)

![Pruebas y verificación](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Actualizado el 6 de noviembre de 2026.** Los resultados están vinculados a la revisión, el entorno y la carga de trabajo registrados para cada ejecución. [Las capacidades actuales](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describen los flujos de trabajo disponibles; esta página recoge lo que se ha comprobado realmente.

[Gráficos de rendimiento](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Auditoría en inglés con lengua de signos](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Mediciones descargables](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Pruebas más recientes | Resultado | Ámbito de aplicación |
| --- | --- | --- |
| Auditoría de lanzamiento · 6, noviembre | Pruebas básicas de 1,461: superadas; la plataforma 37 se omite | Fuente `92e539af40d8`; se mantienen los resultados abiertos |
| Exportaciones recientes · 6 de noviembre | 127.713 y 141.781 registros/s, ciclo completo | Dos cuentas por servidor; texto y metadatos a través de WARP |
| Archivos conservados · 6 de noviembre | Archivos 48; registros 3,598,381 verificados | Los archivos existentes se han comprobado con las claves del espacio de trabajo fijadas. |
| Trusted Live · 5 de noviembre | Grabación de CPU protegida y comprobaciones WARP | El inicio de sesión oficial en la aplicación de escritorio y la exportación nativa siguen sin restricciones. |
| Phala / Intel TDX · 4 de noviembre | Se han superado todas las comprobaciones del verificador 16 en ejecuciones posteriores. | Despliegue histórico; no hay cuenta de Telegram en el CVM |

**En esta página**

- [Auditoría de la versión y nuevas exportaciones · 6 de noviembre de 2026](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu y WARP · 5 de noviembre de 2026](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Implementación en vivo de Phala Cloud · 4 de noviembre de 2026](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Inventario del diario del servidor en tiempo real · 1 de noviembre de 2026](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Comprobaciones recientes sin conexión y con inyección de fallos · 1 de noviembre de 2026](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Prueba en directo de Telegram, cuenta completa · 29 de octubre de 2026](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Exportación protegida con contraseña abierta con libarchive · 29 de octubre de 2026](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Prueba en directo de Telegram · del 27 al 29 de octubre de 2026](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Medición sintética de la capacidad local](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Búsqueda de texto completo en un millón de mensajes · 5 de noviembre de 2026](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Cualificación restante](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/#remaining-qualification)

## Auditoría de la versión y nuevas exportaciones · 6 de noviembre de 2026

La auditoría utilizó la versión v0.9.1 en el código fuente `92e539af40d8368d198ff5e040f1d876f2c1310e`, versión `92e539af40d8-83e41104669e`. Las pruebas de funcionamiento de los paquetes instalados se superaron en tres servidores. El informe firmado refleja el estado observado en ese momento.

[![Tasas de adquisición y exportación completa para dos cargas de trabajo recientes](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Volumen de trabajo | Registros | Adquisición | Ciclo completo | Tasa de ciclo completo |
| --- | --- | --- | --- | --- |
| Servidor A · dos cuentas | 27,030 | 189.043 s | 211.647 s | 127.713 registros/s |
| Servidor B · dos cuentas | 29,299 | 182.513 s | 206.650 s | 141.781 registros/s |

Ambas exportaciones se iniciaron sin reanudación, excluyeron archivos adjuntos y avatares, y finalizaron sin ningún registro duplicado o reutilizado. El ciclo completo incluye la preparación, la adquisición, la selección, el empaquetado y la verificación del archivo. El servidor A también ejecutó una comprobación de lectura de chats protegidos. Se respetaron cuatro eventos FloodWait en A y tres en B. Estas observaciones no establecen una garantía general de rendimiento.

| Comprobar | Resultado | Requisitos |
| --- | --- | --- |
| pytest básico | 1,461: aprobado | La plataforma 37 omite |
| Navegador / experiencia de usuario del navegador / pruebas / sitio web | 102 / 66 / 15 / 9 superadas | Estos programas se solapan con otras pruebas; los recuentos no son acumulativos. |
| Complemento Capture | 124: aprobado | Tres comprobaciones oficiales de la web bloqueadas por el entorno aislado (sandbox) de Chromium requerido |
| Autorización de la API | Rutas 269; solicitudes 538 aprobadas | Credenciales perdidas y acceso revocado |
| Archivos conservados | 48 de 48 verificado | Registros 3,598,381; claves del espacio de trabajo fijadas |
| Comprobaciones de lectura en tiempo real de la flota | Se ha superado el perfil 24 de 40 | Las rutas WARP 16 no superaron la calificación; esos perfiles no estaban conectados |

El informe [firmado](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) registra todos los hallazgos pendientes, incluidos tres defectos en una instantánea de un chat secreto no publicada que no figura en la versión principal auditada. La anterior [calificación del historial público](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) utilizó una revisión y una carga de trabajo diferentes; sus índices no deben combinarse con esta comparación.

Verifica el informe original utilizando la clave [fijada y el verificador](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Su firma protege el informe del operador frente a posibles alteraciones. No se trata de una certificación independiente, una prueba de la autoría de Telegram ni una certificación del RGPD.

## Trusted Live CPU Ubuntu y WARP · 5 de noviembre de 2026

La ejecución de integración conservada utilizó un invitado Ubuntu 24.04.5 solo con CPU (vCPU 4, 8 GiB) bajo QEMU dentro de un host RunPod con CPU. El recopilador utilizó `14e642a5`; la verificación utilizó `02072461`. Las correcciones finales se fusionaron en [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) como `755f78f6`, cuyo árbol coincidía con la cabeza del PR probado. No se trataba de un TEE.

- Se ha detectado un conector WARP real en buen estado; el HTTPS con proxy ha indicado que WARP y Gateway están habilitados. Tres sondas detectaron la misma dirección de salida, lo que no garantiza una IP fija.
- Al desconectar WARP, la solicitud mediante proxy falló. El servicio de puerta de enlace HTTPS directo fue rechazado. En el espacio de nombres del registrador, se bloquearon las direcciones IPv4/IPv6 directas, el DNS externo y el resolutor UDP integrado de Docker.
- Un token de proveedor de solo lectura con ámbito limitado podía leer el estado y las conexiones, pero no podía leer el token de inscripción del conector. Las observaciones firmadas del proveedor incluían muestras explícitas no disponibles. El testigo se ejecutaba en el servidor del operador, por lo que esto demuestra el registro y la conservación de datos, pero no la custodia por parte de un tercero independiente.
- Official Desktop llegó a su pantalla de bienvenida sin autenticar. La entrada de teclado protegida fue rechazada durante la captura. Se decodificaron tres segmentos de pantalla H.264 y se inspeccionó su superposición de reloj. Se verificó el archivo de comprobación previa del evento 18 con la clave de grabación fijada y el punto de control conservado.
- Las pruebas finales de captura superaron los casos 114 en el entorno de integración continua (CI) de Windows y Linux, con versiones reales de Chromium/FFmpeg. Se superaron cinco pruebas de referencia y las comprobaciones de avisos de dependencias.

Una puesta en marcha inicial de 2 vCPU/4 GiB agotó el tiempo de espera bajo una carga simultánea de creación de imágenes y se detuvo a través del mecanismo de protección; no se cuenta como un éxito. El inicio de sesión manual en la cuenta de prueba, la exportación nativa del chat, la comparación híbrida real y el cierre de sesión desde Telegram siguen pendientes. No se importó ninguna sesión de Telethon proporcionada. Los archivos adjuntos, el OCR automático, la verificación local de drand BLS y la certificación Trusted Live TDX no cumplieron los requisitos.

## Despliegue en Phala Cloud en tiempo real · 4 de noviembre de 2026

**Resultado histórico: las implementaciones posteriores a** superaron todas las comprobaciones del verificador 16, incluidas las de Intel TDX y el túnel rápido. Las pruebas de reinicio, la detección de direcciones firmadas y las marcas de tiempo de los informes se comprobaron por separado. Cada CVM de prueba se eliminó tras su ejecución.

| Configuración | Valor registrado |
| --- | --- |
| Proveedor | Phala Cloud · `tdx.small` · US-WEST-1 |
| Implementación | `--provider phala --quick-tunnel`: espacio de trabajo inicialmente vacío |
| Recopilador inicial | `df7d860c` · v0.8.1 |
| Recopilador con todas las correcciones | `53a0f7e9` |
| Invitado de producción | `dstack-0.5.12`; acceso SSH desactivado |
| Servicios externos | ntfy.sh, GitHub e Intel PCS |
| Coste observado | Siete CVM, que suman unos 1.9 centavos de dólar estadounidense; precios históricos de las pruebas |

La secuencia que figura a continuación distingue entre fallos iniciales, correcciones y comprobaciones completadas. No se conectó ninguna cuenta de Telegram a estos CVM.

**Implementaciones 1–2 · diferencias entre proveedores y comprobaciones de regresión**

Las dos primeras implementaciones detectaron cinco diferencias con respecto a la Phala Cloud simulada. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) ahora reproduce cada una de ellas y falla si no se aplica la corrección correspondiente:

| En Phala Cloud | Antes de la corrección | Solución |
| --- | --- | --- |
| Se requiere `compose_file.name` | HTTP 422, no se ha creado nada | La configuración de Docker Compose incluye el nombre de la CVM |
| A menos que se le proporcione uno vacío, Phala añade su propio script de preinicio al «app-compose» evaluado (v0.0.20: inicio de sesión en Docker, `docker compose pull`, contraseña de root, claves SSH de `user_config`) | `tdx_compose` falla: código fuera de la configuración publicada de Docker Compose | El «app-compose» establece `pre_launch_script` en `""`; Phala, a continuación, lo omite |
| Sin `image`, Phala selecciona `dstack-dev-0.5.12`, la versión de desarrollo, con acceso SSH habilitado | `server_state` falla. En esta imagen, solo se ha superado el registro de certificación de hardware; únicamente el registro del proveedor y `tdx_os` lo muestran. | La implementación solicita la versión de producción de la actual versión de Phala, `dstack-0.5.12` |
| Con la pasarela dstack desactivada, los detalles de la CVM nunca muestran un `instance_id` | La implementación espera 30 minutos y falla | El ID de la instancia se lee del estado de la CVM |
| Los reinicios, las paradas y los arranques son operaciones de la CVM, no revisiones de la aplicación | `provider_actions` no incluyó los reinicios | Las operaciones también se leen |

**Despliegue 3: certificación, comprobaciones de acceso y pruebas de reinicio**

- La CVM ejecutó `dstack-0.5.12` con el acceso SSH desactivado. El colector publicó su dirección firmada aproximadamente 1,5 minutos después de su creación. A continuación, la implementación superó las pruebas de `tdx_binding` y `tdx_quote` (Intel TCB UpToDate, registro de certificación de hardware v4, FMSPC `20a06f000000`, sin modo de depuración, no migrable, compatible con datos de verificación criptográfica obtenidos de Intel), `tdx_compose_hash`, `tdx_compose` (byte a byte) y `tdx_identity` (claves KMS).
- El panel, en su dirección trycloudflare.com, devolvió un código de estado 401 sin token o con uno incorrecto, y un 200 con el token del panel.
- `verify` con `--source` configurado en el archivo de GitHub de la confirmación y la huella digital superada por separado: servidor, `server_state`, cortafuegos (sin puerta de enlace, sin punto final público), registro del proveedor, extracto, huella digital, hash de origen, arranque y las cinco comprobaciones `tdx_*` superadas. Cloudflare y `tdx_os` no estaban disponibles, por lo que el resultado fue INCOMPLETO.
- Dos reinicios a través de la API de Phala: en cada ocasión, la CVM volvió a estar operativa en menos de dos minutos con la misma clave de recopilador, una nueva dirección firmada y la antigua respondiendo con el código 530. `verify` notificó el nuevo arranque y ambos reinicios como REVIEW. Con `--evidence` se confirmaron las firmas del diario y tres arranques, cada uno con su propio registro de certificación de hardware Intel TDX procedente del mismo CVM.
- `destroy` eliminó únicamente esa CVM. A continuación, el espacio de trabajo quedó vacío y la dirección del panel dejó de responder.
- La comprobación de precios del asistente del panel indicaba `tdx.small` a 0,058 dólares por hora. Al introducir una clave incorrecta, apareció un mensaje sencillo que decía «no se ha aceptado la clave de API».

**Correcciones posteriores: detección de direcciones firmadas y mediciones del sistema operativo**

- Sin la clave de dirección, `verify` siguió la última publicación bien formada sobre el tema de la dirección, que figura en la configuración de Docker Compose publicada. Una publicación falsificada lo envió a un host que no existe, y `statement` falló: un falsificador no pudo hacerse pasar por el recopilador, pero sí pudo bloquear la verificación de terceros durante un máximo de 12 horas con una marca de tiempo futura falsificada. El recopilador ahora también publica su dirección firmada con su propia clave; `verify` solo acepta dichas publicaciones cuando el recopilador las realiza, y las publicaciones se ordenan según la hora de recepción de ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) reproduce las publicaciones falsificadas. Un CVM ejecuta esto únicamente desde una confirmación que lo contenga, por lo que el recopilador de esta ejecución aún no había firmado su dirección y `verify` así lo indicó.
- `tdx_os` no pudo ejecutarse sin `dstack-mr`, cuya versión actual es `measure-os` en lugar de el `measure --json` que figuraba en la documentación. El verificador calcula ahora por sí mismo MRTD y RTMR0-2 a partir de la imagen publicada y la configuración de la máquina virtual, incluidas las tablas ACPI.

**Implementación 4 · todas las comprobaciones 16, sellos de informe y verificación de reinicio**

- Deploy descargó una vez el archivo `dstack-0.5.12` publicado, lo comparó con el hash de la imagen del sistema operativo que la CVM notificó, y `tdx_os` superó la comprobación: MRTD, RTMR0, RTMR1 y RTMR2 coinciden con los valores calculados para QEMU 8.2.2, 1 vCPU y 2 GiB. El mismo cálculo arrojó un valor de RTMR0 diferente para una configuración declarada de 4 GiB, 2 vCPU, QEMU 9.2.1 o una segunda tarjeta de red, y falló en caso de cambios en el kernel, el firmware o la línea de comandos, así como para la imagen de desarrollo.
- `verify` superó cada una de sus 16 comprobaciones, incluido el conector del túnel rápido, por lo que el resultado fue «APROBADO». Generó el certificado en formato HTML y PDF, sellado digitalmente con firmas y marcas de tiempo mediante una marca de tiempo eIDAS cualificada de la unidad de marcado de tiempo del Gobierno belga TSU 202301 (estatus concedido en la lista de confianza de Bélgica), una marca de tiempo FreeTSA y la firma del verificador; `check-report` confirmó todos ellos y la firma del PDF.
- Tras un reinicio, `verify --evidence` confirmó dos arranques, cada uno acompañado de una certificación de hardware generada dentro de la CVM y cada uno iniciado desde el `dstack-0.5.12` publicado; tanto el reinicio como el nuevo arranque fueron de tipo REVIEW.
- `destroy` dejó el espacio de trabajo vacío.

**Implementación 5: detección de mensajes firmados por el recopilador y rechazo de mensajes falsificados**

El recopilador se ejecutó a partir de la confirmación `53a0f7e9`, que incluye las correcciones mencionadas anteriormente.

- El recopilador publicó su dirección firmada con su propia clave, junto a la publicación HMAC del operador. A continuación, se añadieron dos publicaciones falsificadas al tema, una con un HMAC a cero y otra firmada por otra clave Ed25519, ambas con una fecha del año 2096. `verify` tomó la dirección firmada por la clave del recopilador y superó las 16 comprobaciones; el sello volvía a incluir el sello de tiempo belga certificado, el sello de tiempo de FreeTSA y la firma del verificador, y `check-report` los confirmó.
- Tras un reinicio, el colector publicó la nueva dirección firmada: `verify` la detectó de inmediato; el operador **«Buscar la dirección actual»**, 27 segundos más tarde a partir de la publicación HMAC, y ambos ignoraron las publicaciones falsificadas. `verify --evidence` confirmó dos arranques iniciados desde `dstack-0.5.12`.
- La implementación mostró lo que Phala factura por la CVM, disco incluido: 0,06078 dólares por hora.

### Asistente de paneles y alcance restante

El asistente del panel se ejecutó en Phala Cloud en dos ocasiones: una a través de su API de tareas y otra a través del navegador con un Chromium real: la comprobación del precio, la creación con la confirmación bajo **Advanced**, las seis comprobaciones de certificación superadas, la lista de servidores que muestra el precio facturado (44,37 USD al mes), **Find la dirección actual**, la descarga de la configuración de Docker Compose medida y la eliminación. El navegador no detectó ningún error en las páginas. En ambas ocasiones, el espacio de trabajo quedó vacío posteriormente.

No se incluyen: un dominio de Cloudflare en Phala, una cuenta de Telegram en el CVM y la imagen `dstack-0.6.1` . El precio del asistente antes de la creación corresponde únicamente al coste de computación de Phala, ya que su API indica el coste del disco solo para un CVM existente; la lista de servidores muestra el precio facturado tras la creación. Todos los precios de esta sección se observaron el 4 de noviembre de 2026.

## Inventario del diario del servidor en tiempo real · 1 de noviembre de 2026

Aproximadamente a las 19:15 UTC, las consultas SQLite `query_only` secuenciales de solo lectura contabilizaron los eventos en diez bases de datos de espacios de trabajo en un servidor en funcionamiento. La recopilación continuó durante las consultas, por lo que no se trata de una instantánea atómica de todos los espacios de trabajo.

| Observado en las diez bases de datos de espacios de trabajo | Recuento |
| --- | --- |
| Espacios de trabajo con al menos un evento `message.new` | 8 |
| Registros del diario, incluidos los eventos operativos | 1,610,818 |
| Eventos `message.new` | 900,232 |
| Eventos `message.edited` | 80,683 |
| Eventos `message.deleted` | 400,536 |
| Eventos `message.recovered` | 53,403 |
| Eventos `message.snapshot` | 2,183 |
| Eventos `media.saved` | 50,418 |
| Eventos `media.failed` | 5,575 |
| Eventos `coverage.gap` | 11 |
| Bytes de la base de datos, excluyendo los archivos WAL y los archivos multimedia | 7,909,003,264 |

Se trata de **recuentos de eventos**, no de mensajes, personas o archivos multimedia únicos. El mismo mensaje puede aparecer en más de un espacio de trabajo, y una edición o eliminación puede generar otro evento del diario. `media.failed` cuenta los eventos de fallo históricos, no la cola de archivos multimedia actual. Las consultas **no** verificaron de nuevo las firmas ni la cadena de hash completa de los 1,610,818 registros, ni midieron la entrega o el rendimiento, ni establecieron que se capturara cada evento de Telegram. Aquí no se publican contenidos de mensajes, ID de cuentas o de chats, etiquetas de espacios de trabajo, credenciales ni archivos privados.

En esta revisión, el monitor público configurado por separado abarcaba tres fuentes: una respuesta de captura fue correcta y dos informaron de `no_response`. Ese monitor no es un resumen del estado de diez entornos de trabajo. `no_response` significa que el observador no pudo obtener una respuesta en esa comprobación; no implica la pérdida de mensajes. La prueba más pequeña del 29 de octubre que se muestra a continuación tiene su propia firma explícita y verificación de cadena de hash.

## Comprobaciones recientes sin conexión y con inyección de fallos · 1 de noviembre de 2026

Estas comprobaciones utilizan datos ficticios y archivos locales; aportan pruebas de regresión para la fuente actual, no para otra medición real de entrega de Telegram:

| Comprobar | Qué se ha probado |
| --- | --- |
| [Archivo fuente](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Dos compilaciones con bytes de código fuente idénticos, pero con fechas de modificación de los archivos diferentes, generaron el mismo archivo ZIP y la misma suma de comprobación. Los bytes exactos del archivo y los hash de los archivos coincidieron; los archivos de prueba privados quedaron excluidos. Un fallo de escritura simulado dejó intactos el archivo y la suma de comprobación anteriores. |
| [Recuperación de la exportación de la cuenta](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | Un error de disco simulado en el segundo miembro del ZIP no dejó ningún ZIP publicado ni parcial. La reanudación mantuvo cada recibo firmado idéntico byte a byte, generó un archivo verificable de forma independiente utilizando la huella digital de firma esperada y conservó la laguna de cobertura sintética como resultado parcial. Las aserciones de escala evitan que se repitan las tareas y los escaneos de recibos a medida que crecen los historiales. |
| [Privacidad con divulgación mínima](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Se comprobaron los nombres y alias Unicode sintéticos, los metadatos anidados, los remitentes desconocidos y los campos multimedia en los tres modos de identidad y con omisión de texto. Un fallo en el límite de enmascaramiento no debilitó silenciosamente la censura; la exportación original de la cuenta firmada se mantuvo sin cambios. |
| [Decodificador multimedia para Linux y OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | Una [comprobación de CI en Docker para Linux](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) en la confirmación `5a9e0814` superó las pruebas con entradas generadas en formatos Ogg/Opus, MP3, M4A, MP4 con vídeo, WAV y FLAC; controles de duración falsificada y de referencia a archivos secundarios; y 48 fixtures de analizador mutados (34 rechazados, 14 decodificados dentro de los límites). El OCR real de Tesseract se ejecutó sin modificar los bytes originales. El decodificador y el OCR se ejecutaron en contenedores aislados de la red sin un modelo de Whisper. |

Las comprobaciones se ejecutan en los flujos de trabajo [(solicitud de incorporación de cambios)](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) y [(comprobaciones completas)](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml). Comprueban estos límites de fallo, no todos los posibles fallos de almacenamiento ni si una divulgación es automáticamente segura para su publicación. La comprobación de archivos multimedia no mide la precisión del reconocimiento de voz ni la entrega de Telegram. Revisa cada derivado antes de compartirlo.

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

## Búsqueda de texto completo en un millón de mensajes · 5 de noviembre de 2026

Comando: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

Se indexó un diario firmado determinista de 1 000 000 de mensajes sintéticos en 200 chats (formas léxicas en ruso, ucraniano, inglés, chino y japonés, además de enlaces e identificadores) en 71 segundos; el índice ocupó 58 MiB, además de un diario de 1,50 GiB. Las búsquedas de mejor coincidencia tardaron entre 9 y 190 ms (mediana), frente a los 2,4 a 3,2 segundos de la anterior búsqueda de subcadenas . Resultados completos, hardware y límites: [Búsqueda de texto completo](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/#benchmark). `tools/test_fulltext.py` También verifica un archivo firmado creado antes de la búsqueda de texto completo (`tools/fixtures/evidence-before-fulltext.zip`) con el verificador actual, y un archivo actual con el propio archivo de ese `verify.py`.

## Cualificación restante

El registro en tiempo real conservado recoge de forma fehaciente las recopilaciones, modificaciones, avisos de eliminación, archivos adjuntos, nuevas comprobaciones y la gestión de los límites de frecuencia. No registra de forma exhaustiva la entrega ni ofrece una matriz controlada de visibilidad de roles, agentes de reacción, esperas prolongadas (FloodWait), bloqueos de cuentas y recuperación tras interrupciones de red o procesos. La emisión de tokens QR sigue siendo independiente de la confirmación completa del código QR en el móvil.

Las comprobaciones de Docker/Compose y de instalación se registran en CI; el despliegue real de Phala y la verificación externa de marcas de tiempo se describen más arriba. No establecen una carga elevada sostenida, una matriz completa de plataformas/roles en tiempo real, una revisión de seguridad independiente, una validación de archivo a largo plazo ni una certificación forense. Se han implementado el estado guardado de MTProto y la puesta al día; la reproducción en tiempo real atómica y sin pérdidas sigue sin estar establecida. El backfill más reciente confirma los mensajes y los cursores de forma atómica y conserva las acciones recientes disponibles, pero su cobertura sintética es distinta de la cualificación en tiempo real. Véase «[: aceptación en tiempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)» para consultar la matriz de cualificación controlada.

El directorio de auditoría pública  contiene únicamente el informe firmado y las mediciones agregadas. Los recibos operativos detallados, las capturas sin procesar y el material de las cuentas siguen siendo privados. Las capturas de pantalla de la aplicación en `docs/assets/` utilizan datos de demostración ficticios.
