# Lo que se ha probado

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/

La prueba en tiempo real de Telegram, las comprobaciones automatizadas, las comprobaciones en el navegador y lo que aún no se ha verificado.

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

Las entradas anteriores que figuran a continuación describen sus propias ejecuciones; en la mayoría de ellas se utilizaron clientes de prueba sintéticos. A continuación se muestran los últimos resultados automatizados.

## Listas públicas de MTProxy integradas · 29 de octubre de 2026

Este es el historial de pruebas de la versión original con selección manual. Para conocer los modos actuales de grupo automático y IP, consulte [la configuración de conexión](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/#ip-modes). Las cifras y las funciones no compatibles que se indican a continuación corresponden a esa revisión probada.

Se ha añadido una instantánea pública empaquetada y una actualización explícita mediante HTTPS desde SoliSpirit/mtproto y zakky8/mtproto-proxy-pro. En este servidor, el programa de descarga de la aplicación obtuvo ambos flujos con éxito el 29 de octubre de 2026 a las 12:58 UTC: **118 puntos finales únicos compatibles** tras el filtrado, la deduplicación y el límite de 64 entradas por fuente. Esto verifica la recuperación de la lista, no la conectividad ni la entrega de mensajes a través de dichos puntos finales. No se conectó ninguna cuenta real a un proxy de la lista durante este trabajo. [Guía del operador y del usuario](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/PROXIES.md).

Las respuestas de origen fallidas, vacías o incompatibles conservan las entradas y fechas anteriores. Las actualizaciones no modifican la ruta seleccionada. Las direcciones públicas se validan y las direcciones IP resueltas se fijan al seleccionarlas; las rutas del operador y las manuales permanecen separadas. La prueba de conexión ya está disponible en el panel antes de iniciar sesión en la cuenta. El TLS falso y la selección automática de proxy siguen sin ser compatibles. El catálogo del operador anula por completo las suscripciones.

- Conjunto completo de pruebas: **366 superadas, 3 omitidas**, 287,94 segundos. Persisten las advertencias sobre dependencias existentes y las omisiones relacionadas con la plataforma. Regresión final de la lista pública/localización: **36 superadas**, incluido el rechazo de puertos de proxy de descarga no válidos; esto se solapa con el conjunto completo de pruebas.
- Se ha superado la prueba de compatibilidad con navegadores en inglés/ruso, en modo claro/oscuro a 390/1440 píxeles: opciones integradas, sin descargas externas al abrir la configuración, actualización explícita, rutas y caché conservadas durante los fallos, comprobación previa al inicio de sesión, aislamiento del espacio de trabajo en caso de respuesta tardía, detalles de la fuente y diseño/contraste. Sin errores de JavaScript ni solicitudes externas del navegador.
- Se ha aprobado la cobertura final de la traducción estática para las 13 configuraciones regionales; el nuevo texto se ha traducido al ruso, con texto de reserva en inglés explícito en el resto de casos. La guía integrada actualizada ha superado las comprobaciones de maquetación y contraste en ambos temas.
- Se han superado las comprobaciones de Ruff y de publicación (259 archivos públicos, 1.354 enlaces locales); se ha actualizado el análisis de los archivos YAML de «Compose» y de CI. Aquí no se han ejecutado Docker ni la integración continua remota.
- La rueda reconstruida superó las pruebas de instalación aislada, carga de la lista de paquetes incluidos y verificación de la exportación firmada . Los 69 recursos del paquete coincidían con el espacio de trabajo; se comprobaron los hash del código fuente.

Recibos: `test-results/public-proxy-research/download-receipt.json`, `test-results/public-proxy-research/copy-receipt.json`, `test-results/public-proxies-full-suite.log`, `test-results/public-proxies-final-focused.log`, `test-results/public-proxies-browser/receipt.json` y `test-results/public-proxies-package.log`. Los entornos de prueba de navegador, cuenta y transporte son sintéticos; las dos descargas de feeds anteriores son solicitudes HTTPS reales.

## Presentación de extras opcionales · 29 de octubre de 2026

Lo que antes era el destino del bot «Proof» ahora es **«Extras**»: una breve descripción general seguida de una página de configuración independiente para la opción seleccionada. El formulario de «Witness» consta de tres pasos, con la gestión de la conexión, las opciones de red y los detalles de implementación ocultos. GitHub está previsto de forma explícita y no requiere un formulario de credenciales. [Descripción general en ruso](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/EXTRAS.md).

- Se han superado 30 pruebas específicas de localización, configuración de Witness y comprobaciones de publicación.
- Se ha superado la prueba de aceptación de la configuración de Chromium en inglés/ruso, modo claro/oscuro, a 390/1440 píxeles: foco del teclado y tecla Intro, ausencia de conexiones implícitas al seleccionar elementos adicionales, retención de borradores, descargas de configuraciones y tokens fijados, borrado de tokens al bloquear la pantalla y enlaces a la guía local que funcionan correctamente. Se han superado las comprobaciones de contraste entre el diseño y el texto sobre fondo liso.
- Se ha superado la prueba de aceptación del cambio de espacio de trabajo, incluida la llegada de una respuesta de token retrasada tras un cambio. La navegación rápida permite encontrar los contenidos adicionales mediante los términos «bot», «prueba» y «GitHub»; también se han superado las comprobaciones existentes de 320/390/1440 píxeles y de ruso/RTL.
- No se observaron errores de JavaScript ni solicitudes externas del navegador durante la ejecución de la configuración. Se trata de comprobaciones sintéticas de la interfaz de usuario, no de nuevas pruebas de publicaciones en Telegram o de bots en tiempo real.
- Se ha superado la comprobación final de carga de idiomas y cobertura del diccionario para las 13 configuraciones regionales, conservando los valores por defecto explícitos en inglés fuera del ruso. La guía ampliada de Proof también ha superado las comprobaciones de maquetación y contraste a 320/768/1440 píxeles en ambos temas.
- La versión reconstruida superó la verificación de instalación aislada y de exportación firmada. Los 67 recursos empaquetados coincidían con el espacio de trabajo; el archivo fuente contiene 253 archivos públicos. Se superó la comprobación de fuentes y enlaces para 1.346 enlaces de documentación locales.

Recibos: `test-results/setup-browser/receipt.json`, `test-results/quick-navigation/receipt.json`, `test-results/extras-final.json`, `test-results/extras-package.log` y `test-results/extras-artifacts.json`. Las capturas de pantalla muestran entornos de trabajo sintéticos.

## Auditoría de la configuración del bot y del proxy de Witness · 29 de octubre de 2026

La configuración de Witness (ahora **en «Extras» → «Un bot en su canal**») prepara un Witness desplegado de forma independiente: clave de recopilador fijada, descarga de token con ámbito limitado, canal propio, política de publicación, ruta HTTP/SOCKS5 y API de bot personalizada. El token del bot permanece en el servidor del «witness». Su nuevo `--check-config` valida la configuración y los archivos sin establecer una conexión de red ni crear una clave. Las rutas de los archivos JSON se resuelven junto a la configuración. Todas las variantes de «Compose witness» ahora reenvían la configuración del proxy HTTP y de la API del bot.

La configuración de la cuenta admite un catálogo público de MTProxy gestionado por el operador, una vista previa personalizada de los enlaces de proxy de Telegram y los campos manuales existentes. Las respuestas del catálogo omiten los datos confidenciales; la selección almacena la ruta en el almacén de seguridad del espacio de trabajo. Si faltan catálogos o estos presentan errores de formato, se mantienen disponibles las rutas manuales. No se crean ni se activan de forma predeterminada direcciones de proxy del proyecto ni servicios de testigo alojados. Un ejemplo de Caddy expone únicamente el punto final principal con ámbito limitado cuando un testigo externo debe acceder a un recopilador cuyo panel permanece privado.

Validación:

- Conjunto completo: **348 superadas, 3 omitidas**, 195,81 segundos. Las limitaciones de Windows explican las omisiones; persisten las dos advertencias existentes sobre dependencias obsoletas.
- Ejecución final de regresión de TestWitness/configuración/lanzamiento: **11 superadas, 1 omitida**. Esto se solapa con el conjunto completo de pruebas. Las pruebas incluyen la resolución de rutas, la comprobación previa sin conexión, la firma y publicación a través de un dispositivo real de API de bot HTTP de bucle cerrado, el fallo de entrega registrado, la verificación del token del canal y la exclusión del secreto del proxy.
- Se ha superado la prueba de aceptación de la configuración de Chromium en inglés y ruso a 390/1440 píxeles: configuración fijada y descargas de tokens, borrado de tokens al bloquear la pantalla, selección de catálogo, vista previa de enlaces personalizados seguida de un guardado explícito, diseño y contraste correctos, y ausencia de errores de JavaScript o de solicitudes externas del navegador. Se ha corregido el desbordamiento del encabezado de la cuenta en ruso y de la pestaña de inicio de sesión debido a su anchura reducida.
- Se ha superado la comprobación de Ruff, la verificación de fuentes y enlaces, así como el análisis sintáctico del YAML de «Compose» y del flujo de trabajo.
- La versión renovada superó las comprobaciones de instalación aislada, de paneles y recursos estáticos, y de autenticación de la API, además de una verificación independiente de exportaciones sintéticas de 32 eventos, tanto directas como en streaming.

Comprobantes: `test-results/setup-full-suite.log`, `setup-final-focused.log`, `setup-browser/receipt.json`, `setup-browser-final.log` y `setup-package.log`. Estas comprobaciones utilizan cuentas sintéticas o proxies y un entorno de prueba local de la API de bots. No pretenden simular una publicación real de un bot, un servidor MTProxy público en funcionamiento, una ejecución remota de CI ni una implementación de Docker. El historial real de observación de Telegram conservado anteriormente sigue constituyendo una prueba independiente. [Instrucciones de configuración](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

## Revisión de la presentación y la documentación · 29 de octubre de 2026

La página del producto, la pantalla de acceso, los archivos README en inglés y ruso y las imágenes de presentación comparten ahora un mismo estilo visual. Las capturas de pantalla públicas utilizan datos de demostración ficticios. La revisión también ha corregido las descripciones obsoletas sobre la validación en tiempo real y la recuperación que figuraban anteriormente.

- Pruebas específicas de localización, del sitio web y de publicación: **33 superadas, 1 omitida**. La prueba omitida requiere la creación de un enlace simbólico, lo cual no está disponible en este servidor.
- Se ha superado la aceptación general del panel de Chromium, incluyendo todos los catálogos de idiomas, el diseño RTL, los temas claro/oscuro, el contraste sólido del texto y el cambio de espacio de trabajo. La comprobación de la creación del perfil ahora espera a recibir la respuesta HTTP efectiva antes de comprobar el espacio de trabajo seleccionado.
- Las pantallas de acceso en inglés y ruso han superado las comprobaciones de maquetación y contraste en ambos temas a 320, 390, 768, 850 y 1440 píxeles; el botón de envío permanece dentro del área de visualización inicial.
- Se ha superado la prueba de compatibilidad con sitios públicos a resoluciones de 320, 390, 768, 1024 y 1440 píxeles, incluyendo , la ampliación de capturas de pantalla/tecla Escape/recuperación del foco, las pestañas del teclado, el rechazo del portapapeles, las subrutas del proyecto, el movimiento reducido y la alternativa sin JavaScript. No se observaron solicitudes de recursos fallidas, solicitudes externas ni errores de JavaScript.
- La versión renovada ha superado una comprobación de instalación aislada: los recursos del panel y las configuraciones regionales se cargan, el acceso a la API requiere autenticación y las exportaciones directas y en streaming verifican de forma independiente los 32 eventos sintéticos. Se han superado las comprobaciones de Ruff y de fuentes públicas/enlaces.

Recibos locales: `test-results/design-tests.log`, `design-panel-final.log`, `design-review-final.log`, `design-site.log` y `design-package/install-receipt.json`. No se ha vuelto a ejecutar el conjunto completo de servicios de fondo para este cambio en la presentación o la documentación; su resultado anterior permanece en la auditoría previa a la publicación.

## Versión 0.6.1

La versión 0.6.1 modifica la presentación del panel, los lanzadores, el empaquetado y la documentación; el código de recopilación, almacenamiento, firma y exportación no ha sufrido cambios. En Windows 11 / Python 3.12.10 con el entorno de ejecución fijado:

- El conjunto completo de pruebas superó **137 pruebas,** con 2**omisiones** y la advertencia existente de Starlette. Las nuevas pruebas abarcan el manejo de Ctrl+C por parte del lanzador (el servidor dispone de 30 segundos para una parada ordenada) y los fallos en los pasos de configuración que requieren una acción.
- Chromium (shell sin interfaz gráfica 156) superó los **45 escenarios generales** y **los 35 escenarios de importación de cuentas, códigos QR y claves de autenticación**, incluida la comprobación de contraste del texto liso, la ausencia de desbordamiento horizontal entre 320 y 1440 píxeles y la visibilidad de los campos de primer inicio de sesión a 320 y 390 píxeles. No se observaron errores de JavaScript en la página ni solicitudes externas.
- `python start.py --setup-only` reinstaló el paquete en su versión 0.6.1 y `python start.py --check` informó de que estaba listo. Un servidor `python -m tgwitness --demo` real devolvió el panel, la hoja de estilos, el script, el logotipo, la guía y la versión `/api/status` 0.6.1; el `workspace.css` eliminado devolvió un error 404.
- `Start.cmd` encontró una instalación de Python fuera de la variable PATH. Al no haber Python disponible, mostró la oferta de instalación; al rechazarla, se mostraron las instrucciones manuales y se salió 1. El paso de descarga de python.org obtuvo el instalador 3.12.10 y superó la comprobación de Authenticode de la Python Software Foundation; el instalador en sí no se ejecutó en este host.
- `start.sh`, sin utilizar Python, mostró las instrucciones de instalación y se cerró. 1. `scripts\Docker.cmd` y `scripts/docker-start.sh` se probaron con ejecutables falsos de `docker`: secuencia de llamada correcta, dirección del panel y salida del token correctas, y ausencia de mensaje de éxito tras un fallo.
- `python tools/build_portable.py` creó un paquete para Windows de 18,8 MiB tras verificar la suma de comprobación del «embeddable-runtime» fijado. Tras extraerlo en una ruta que contenía espacios y ejecutar el programa con únicamente los directorios `C:\Windows` en la variable PATH, su Python integrado superó la prueba `TgWitness-Check.cmd`, sirvió la demostración (32 eventos) y un espacio de trabajo en tiempo real, y Chromium representó el registro y el panel de detalles sin errores de JavaScript. Los datos se escribieron en la carpeta `data` del paquete.
- `python tools/build_preview.py` generó un archivo fuente de 110 archivos. Una prueba de `git add` mostró los mismos 110 archivos, sin archivos de sesión, claves, bases de datos, tokens, registros ni exportaciones, sin rutas absolutas locales y sin cadenas con forma de secreto.

No se han llevado a cabo en esta ejecución concreta de empaquetado del 27 de octubre: la instalación automática de Python en sí misma, las comprobaciones de Docker Build/Compose, las ejecuciones en Linux/macOS ni un nuevo ejercicio con una cuenta activa . Las pruebas reales de Telegram se registran más arriba y en las comprobaciones de cuentas anteriores que figuran a continuación. Las definiciones de CI por sí solas no bastan para validar la ejecución en la plataforma.

## Versión 0.6.0

La última suite completa de tiempo de ejecución fijada en Windows 11 / Python 3.12.10 superó **135 pruebas**, con 1**prueba omitida**, en 26,53 segundos y la advertencia existente de Starlette. La omisión requiere permisos POSIX. Tras añadir el renderizador de códigos QR a las comprobaciones de estado de preparación y a las mediciones de procesos, también superaron la prueba las 8 comprobaciones de estado de preparación y del espacio de trabajo afectadas.

La nueva cobertura incluye los esquemas de Telethon 7/8, los esquemas de Pyrogram 2/3, JSON completo y JSON solo con metadatos, archivos de cuentas coincidentes o conflictivos, códigos de acceso de TData, manipulación de sumas de comprobación y rutas inseguras, conversión en memoria sin conexión o autenticada, comprobaciones de ID de cuenta en línea, éxito de códigos QR/autenticación de dos factores (2FA)/caducidad, cancelación de datos obsoletos y aislamiento de cuentas. Los Los elementos de prueba de TData utilizan una implementación independiente de AES-IGE para el cifrado.

Chromium superó **45 escenarios generales** y **35 escenarios de importación de cuentas, códigos QR y claves de autenticación**, sin que se observaran errores de JavaScript en las páginas ni solicitudes externas. Las nuevas comprobaciones del navegador abarcan los cuatro formatos de entrada en su conjunto, TData protegido, metadatos de la API, representación de códigos QR, caducidad/reintento, autenticación de dos factores (2FA), rechazo por cuenta incorrecta, bloqueo/cancelación del espacio de trabajo, diseño adaptativo y respuestas de conversión tardías tras la selección de un archivo más reciente.

Ambas suites de navegadores superaron de nuevo las pruebas tras los cambios en el acceso a la cuenta. La configuración en tiempo real abre el formulario de cuenta; el modo de demostración abre su registro de muestra. La página de demostración de la cuenta muestra instrucciones de inicio en tiempo real y oculta los campos de introducción de credenciales. Las comprobaciones específicas a 320, 390 y 1440 píxeles confirmaron que el campo numérico y el botón principal caben sin necesidad de desplazarse, que los campos de la API aparecen inicialmente ocultos y que el contraste del texto sigue siendo legible. Los controles de captura y verificación permanecen ocultos tras abrir sus nuevas secciones expandibles.

Se probó el flujo directo de la clave de autenticación con credenciales sintéticas a través de los puntos finales reales de importación y autorización. Las comprobaciones abarcan claves incompletas, falta de DC, ID de usuario imprecisos, identidad de cuenta no coincidente, credenciales de API guardadas, progreso visible de la solicitud, borrado de secretos y respuestas tardías tras ediciones o cambios de método. Se comprobaron los cuatro métodos de inicio de sesión a 320, 390 y 1440 píxeles. El selector de archivos precede a las instrucciones de formato, y el botón «Conectar» se ajusta a la ventana de visualización inicial de 844 píxeles con la configuración de la API oculta. No se intentó ninguna autorización real con clave de autenticación en esta prueba de aceptación de la interfaz de usuario.

Se ha vuelto a comprobar la actualización del panel con ambos conjuntos de navegadores: no se han observado errores de JavaScript en la página ni solicitudes externas. El conjunto de cuentas abarca ahora la inserción de un par de ID/hash de API, el rechazo de pares malformados o múltiples sin sustituir campos, la orientación basada únicamente en metadatos y el ignorar respuestas de importación caducadas tras un cambio en el método de inicio de sesión o una edición manual de credenciales. Se han superado seis comprobaciones específicas adicionales relativas a la guía de configuración, el inicio y la pausa explícitos, la recuperación de búsquedas vacías, así como el diseño final de la conexión y la guía local, y un contraste de texto sólido a 320, 390 y 1440 píxeles. La actualización del inicio de sesión directo añade una única operación de solicitud de teléfono/código y reutiliza el par de API guardado en el espacio de trabajo actual para el inicio de sesión mediante teléfono, código QR y sesión. El conjunto completo de pruebas en Python mencionado anteriormente incluye nuevas pruebas de persistencia, rechazo de credenciales parciales y aislamiento del espacio de trabajo. Las comprobaciones en el navegador abarcan la introducción directa del número de teléfono, la reutilización de credenciales guardadas, el enrutamiento basado únicamente en metadatos, la autorización de archivos con un solo botón y el rechazo de cuentas duplicadas. También se comprobaron los formularios simplificados de token de panel y de teléfono sin desplazamiento inicial a 320, 390 y 1440 píxeles. Una comprobación de compatibilidad confirmó que el formulario de teléfono directo puede utilizar los puntos finales de configuración/código anteriores mientras sigue ejecutándose un proceso anterior.

Se comprobó por separado una cuenta facilitada por el usuario, al margen de los entornos de prueba públicos. Sus entradas de Telethon, Pyrogram y TData coincidieron con la misma autorización; el archivo JSON adjunto proporcionó las credenciales de la API. Los cuatro archivos se cargaron a través del panel 0.6.0 y Telegram confirmó el ID numérico de la cuenta esperado. Los archivos de origen permanecieron sin cambios. No se seleccionó ninguna fuente y la observación permaneció desactivada. Esto constituye un ejemplo de importación/inicio de sesión, no una recopilación, recuperación o capacidad en tiempo real.

Telegram también emitió un token QR real, que se canceló sin llegar a escanearse. Se llevaron a cabo los flujos completos de confirmación por QR y de autenticación de dos factores (2FA) con clientes sintéticos; la confirmación móvil frente a una aplicación real de Telegram sigue siendo un paso de aceptación independiente. No se incluyen en los archivos públicos identificadores de cuentas reales, datos confidenciales ni capturas de pantalla.

Se ha completado la actualización del lanzador; el código fuente, los metadatos instalados y el marcador de disponibilidad indican la versión 0.6.0, con el código QR 8.2 y un `pip check` válido. La rueda instalada proporcionó el panel y la guía, rechazó las solicitudes de API no autenticadas y verificó de forma independiente las exportaciones sintéticas directas y en streaming de 32 eventos. La guía sin conexión actualizada se comprobó a 320, 390 y 1440 píxeles. Las capturas de pantalla públicas siguen siendo sintéticas.

La versión fuente contiene 107 archivos incluidos en la lista de permitidos. Los enlaces a la documentación local funcionan correctamente. La ejecución en Docker/Caddy, la publicación remota de CI/paquetes, el entorno de ejecución ARM64, la recopilación continua y la matriz completa de compatibilidad con Telegram en tiempo real no se tratan aquí de forma exhaustiva.

## Versión 0.5.1

En Windows 11 / Python 3.12.10, se superó el conjunto completo de pruebas del entorno del proyecto: **94 superadas, 2 omitidas**, en 31,21 segundos, con la advertencia existente de Starlette. Los pasos omitidos requieren permisos POSIX y la creación de enlaces simbólicos, que no están disponibles en este servidor. El fixture HTTP de descarga mostró un diagnóstico del hilo de solicitud; todas las aserciones se superaron. Esta ejecución no garantiza la ausencia de problemas de transporte en el servidor.

Los nuevos ejercicios de cobertura de regresión incluyen el rechazo de StringSession, cambios en el código y en la cuenta de 2FA, la cancelación de la búsqueda de identidad, la cancelación de inicio de sesión pendiente y las actualizaciones a través de manejadores registrados en clientes activos, rechazados, sustituidos y de prueba. Solo el recopilador activo aporta eventos; las credenciales guardadas y el historial firmado permanecen intactos. Otras nuevas comprobaciones abarcan la búsqueda Unicode tras la reapertura de una base de datos, la inclusión de los límites de la política de supervisión en Coverage y las exclusiones de paquetes de código abierto.

El proyecto `pythonw.exe` lanzó un panel sintético aislado, devolvió un código de estado HTTP 200 y conservó los diagnósticos de inicio en `logs/server.log`. El registro no contenía el token del panel generado ni los registros de acceso HTTP. La prueba solo terminó su propio proceso sintético. No se registró ninguna tarea en el Programador de tareas; el inicio de sesión/cierre de sesión, el modo de suspensión y la recuperación del servicio siguen siendo requisitos independientes.

La prueba de compatibilidad con Chromium superó **45 escenarios**, sin que se observaran errores de JavaScript en las páginas ni solicitudes externas. Las nuevas comprobaciones abarcan las fechas y horas de la línea de tiempo en 601/768/850 píxeles, los borradores de archivos adjuntos durante la actualización del estado, las ediciones más recientes realizadas durante el guardado, los resultados de verificación borrados al cambiar de cuenta, las respuestas de verificación tardías tras salir de la aplicación y volver a ella, y los límites de verificación explícitos cuando se producen nuevos eventos. También se corrigió el espaciado del icono de búsqueda y del texto, y se volvió a ejecutar la suite de navegadores.

La ejecución en el navegador utilizó el entorno de ejecución fijado en `.venv` y el Playwright 1.62.0/Chromium proporcionado por el sistema, añadido tras el entorno del proyecto en la ruta de importación. Se detuvo la instalación opcional de una dependencia de desarrollo debido a una descarga lenta de Playwright; no se validó ninguna nueva versión de la herramienta del navegador. Un `python start.py --setup-only` normal completó la actualización de la aplicación. El código fuente, los metadatos instalados y el marcador del lanzador indican la versión 0.5.1; `pip check` superó la prueba. Las comprobaciones de preparación se superaron en una ruta nueva sin usar, conservando la advertencia esperada sobre la clave de la bóveda local.

El paquete «wheel» 0.5.1 se instaló por separado y se sometió a pruebas de funcionamiento básico: se sirvieron todos los recursos de paneles y guías, se rechazó el acceso a la API sin autenticación, y tanto los archivos ZIP de pruebas con 32 eventos, directos como transmitidos, superaron la verificación independiente. Los archivos de la aplicación incluidos en el paquete instalado se compararon con el código fuente. El archivo público del código fuente utiliza una lista de tipos de archivo permitidos explícita y rechaza los archivos fuente vinculados; el material de tiempo de ejecución colocado dentro de los directorios de código fuente queda excluido de las pruebas de regresión.

Durante la ejecución de la corrección del código, la selección de código abierto y el conjunto de candidatos de Git contenían 86 archivos, sin incluir directorios de datos de tiempo de ejecución. Un análisis en busca de patrones reconocibles de claves privadas, tokens de GitHub, tokens de bots de Telegram y StringSession no encontró coincidencias. Se trata de una comprobación de patrones limitada, no de una auditoría exhaustiva de secretos. Las pruebas de reglas de exclusión abarcan doce artefactos comunes relacionados con cuentas, datos y exportaciones. Los archivos YAML de Workflow, Issue y Compose, así como el script de tareas de Windows, se analizaron correctamente. Los enlaces a la documentación local se resuelven.

Se abordan las siete conclusiones de la revisión del 27 de octubre. La ejecución del flujo de trabajo en GitHub, el entorno de ejecución en Linux/macOS/Docker, el uso de Telegram real, la interoperabilidad con proxies externos y TSA, así como la cualificación bajo carga sostenida, quedan fuera del alcance de esta ejecución local. No se llevó a cabo ninguna publicación en el repositorio, registro de servicios ni recopilación de cuentas reales. No se llevó a cabo.

### Actualización de la documentación en inglés

El archivo README, la referencia de cuentas y sesiones, el flujo de trabajo de recopilación y la guía incluida describen ahora en inglés las entradas compatibles, el comportamiento del espacio de trabajo, las políticas de eventos y los formatos de exportación. Las tres capturas de pantalla públicas se han actualizado utilizando datos sintéticos. En ese momento, la selección de código abierto contenía 88 archivos, incluidas las dos nuevas guías. Los 131 enlaces locales repartidos en 23 documentos Markdown funcionan correctamente.

Tras las modificaciones en la interfaz y la guía, las pruebas de aceptación de Chromium volvieron a superar los 45 escenarios, sin que se observaran errores de JavaScript en las páginas ni solicitudes externas. No se volvió a ejecutar el conjunto completo de pruebas de Python para esta actualización de la documentación y la presentación; el resultado de 94 pruebas superadas que figura más arriba corresponde a la ejecución anterior de corrección de código.

La rueda reconstruida se instaló en un nuevo objetivo aislado. Sus componentes de panel y guía funcionaron correctamente, se rechazó el acceso a la API sin autenticación y tanto las exportaciones directas como las transmitidas superaron la verificación independiente de 32 eventos sintéticos.

### Actualización sobre la instalación y la puesta en marcha

El instalador específico, el empaquetado y las comprobaciones de preparación superaron **14 pruebas**, con una omisión por la imposibilidad de crear un enlace simbólico. Las comprobaciones del envoltorio nativo abarcan rutas con espacios, reenvío de argumentos, modos de configuración/demostración y propagación de salida distinta de cero. Las comprobaciones de Git Bash ponen a prueba el asistente de shell de Docker con un demonio simulado, incluyendo la ausencia de Docker, la ausencia de Compose, el fallo en la espera de estado y un inicio correcto en un puerto alternativo. Estas comprobaciones simuladas no establecen la compatibilidad del tiempo de ejecución de Docker.

Se instaló una copia completa de código abierto en un nuevo directorio de Windows cuya ruta contiene espacios. `scripts\Setup.cmd` creó un entorno nuevo e instaló el entorno de ejecución anclado; `Start.cmd --check --json` informó de que estaba listo sin crear su directorio de datos de destino. `pip check` superó la prueba. La rueda reconstruida también superó la comprobación del paquete instalado, incluidas las exportaciones directas y en streaming de 32 eventos.

Se ha analizado la sintaxis de Shell y cinco archivos YAML de flujo de trabajo y de Compose. Las configuraciones de Compose, tanto de código fuente como de imágenes, coinciden en los ajustes de almacenamiento y de tiempo de ejecución. En esa fase, se resolvieron los 139 enlaces locales distribuidos en 23 documentos Markdown. La selección de código abierto contiene 99 archivos.

Las definiciones de CI aplican ahora una nueva configuración nativa en Windows/Linux/macOS, así como el control del estado, el control de acceso y la persistencia de Compose tras la recreación de contenedores, y la configuración de Caddy. El flujo de trabajo de lanzamiento condiciona la publicación a la superación de dichas comprobaciones y añade una prueba de funcionamiento emulada en ARM64. Docker no está disponible en este host: la ejecución real de Compose/Caddy, la emisión de certificados, la ejecución en ARM64 y el flujo de trabajo remoto/publicación de paquetes siguen funcionando sin restricciones a nivel local. El código de la aplicación y la interfaz de usuario no ha sufrido cambios con esta actualización; no se han vuelto a ejecutar los resultados completos anteriores de Python y del navegador.

## Versión 0.5.0

Se ha superado la suite completa de ejecución fijada: **81 superadas, 1 omitida**, en 22,00 segundos, con la advertencia existente de Starlette. La comprobación de permisos POSIX se omite en Windows. Las nuevas pruebas del controlador envían mensajes, ediciones, eliminaciones con o sin ámbito, reacciones, actualizaciones de participantes y mensajes del servicio de membresía a través de diferentes políticas. Las categorías desactivadas no generan observaciones en tiempo real correspondientes; los diagnósticos de cobertura y las instantáneas explícitas siguen estando disponibles. Las pruebas verifican la persistencia de la política, la separación de espacios de trabajo, los registros de auditoría firmados antes y después, el comportamiento de la política sin cambios, la validación estricta y la inclusión en el siguiente recibo del proceso.

Las pruebas de acceso de demostración verifican que su capacidad difiere del token del panel configurado, no puede autorizar un espacio de trabajo activo, no puede modificar la configuración de recopilación y no se emite ni se acepta para solicitudes remotas, reenviadas, de origen cruzado o con un host no válido. Abrir una demostración almacenada sin el indicador explícito de demostración no habilita el acceso automático.

Las pruebas de aceptación de Chromium superaron **39 escenarios**, entre los que se incluyen el acceso a la demostración local sin introducción de token, los ajustes preestablecidos de supervisión, la transición de la selección de la fuente a la política, la independencia por cuenta y las comprobaciones de diseño (escritorio/320/390 píxeles) y de contraste del texto. No se produjeron errores de JavaScript en la página. Las solicitudes inyectadas por AdGuard del servidor permanecen en el registro de recepción. El dispositivo de prueba HTTP de descarga registró un restablecimiento de la conexión después de que un cliente cerrara su conexión; las verificaciones se superaron de todos modos. Este no es un resultado de un servicio en producción.

El lanzador estándar ha actualizado el entorno aislado a la versión 0.5.0; las versiones del código fuente y la instalada coinciden y la comprobación con pip se ha superado. Las comprobaciones existentes de cifrado del almacén secreto, rechazo por clave errónea o ausente y de manipulación de firmas y archivos multimedia se han superado en el conjunto completo de pruebas. No se afirma que exista ningún nuevo cifrado de la aplicación para el contenido de los mensajes o los archivos adjuntos.

La demostración local se reinicia para que la interfaz de usuario actualizada esté disponible. Los registros sintéticos existentes se conservan; al detener el antiguo proceso de demostración en segundo plano se crea un límite de desconexión en el siguiente inicio. No se utiliza ninguna sesión real de Telegram para estas comprobaciones.

El panel en ejecución en localhost:8787 mostraba la versión 0.5.0, acceso automático a la demostración, los cinco controles de supervisión y 33 eventos sintéticos conservados en el registro. El wheel 0.5.0 instalado por separado proporcionaba todos los recursos del panel y la guía, rechazaba el acceso a la API sin autenticar y generaba un archivo ZIP verificado con 32 eventos, tanto directamente como a través del asistente de descarga en streaming. Las versiones de los paquetes en tiempo de ejecución permanecen fijadas tal y como se registraron para la versión 0.4.

## Versión 0.4.0

Se ha superado la suite completa de pruebas de tiempo de ejecución fijadas: **78 superadas, 1 omitida**, en 19,77 segundos. La comprobación omitida requiere permisos POSIX; persiste la advertencia de obsolescencia del Starlette TestClient del proyecto original. Las nuevas pruebas abarcan la descarga en streaming y el enrutamiento del espacio de trabajo, los encabezados de autorización, el rechazo a sobrescribir, las redirecciones, las respuestas truncadas, los límites de tamaño anunciados y reales, las lecturas acotadas, la limpieza, los sistemas de archivos sin enlaces duros, los fallos de preparación y los modos de lanzador que no deben instalar paquetes. Las pruebas de exportación confirman los archivos temporales locales del espacio de trabajo y la limpieza selectiva de archivos huérfanos.

Las pruebas de compatibilidad con Chromium superaron los 36 escenarios enumerados sin errores de JavaScript en la página. Simula el inicio de sesión mediante teléfono, código o autenticación de dos factores (2FA), sesiones convertidas, dos espacios de trabajo y rutas/estados independientes, observaciones, firmas, puntos de control y solicitudes de marca de tiempo, además de:

- Diseños para ordenador de sobremesa y de 320/390 píxeles, sin desbordamiento horizontal, navegación visible, y el primer campo de inicio de sesión dentro de la ventana de visualización inicial de 844 píxeles.
- Contraste del texto sobre fondo liso según los umbrales de texto de WCAG AA. Se excluyen los controles desactivados, la opacidad y los fondos de imagen o degradado; no se trata de una auditoría completa de WCAG.
- Una respuesta de exportación local real generada mediante un simulador de selector de archivos del sistema operativo/escriturable, seguida de una verificación independiente del archivo ZIP; la cancelación no envía ninguna solicitud de exportación.
- Un error de escritura interrumpe el envío al destino; el mecanismo de reserva de 128 MiB rechaza una respuesta anunciada de tamaño excesivo sin asignar una carga útil correspondiente.
- La guía local en inglés para ordenadores de sobremesa y ambos anchos reducidos.

El cuadro de diálogo de guardado del sistema operativo y las escrituras reales en el navegador de varios gigabytes no se automatizaron ni se validaron. Las pruebas de descarga en Python utilizan fragmentos delimitados y dispositivos de bucle cerrado. La aceptación completa de la implementación con Telegram real sigue siendo independiente.

El instalador estándar ha actualizado `.venv` a la versión 0.4.0. El código fuente y los metadatos de la instalación coinciden; `pip check` ha superado la comprobación. `python start.py --check --json` ha indicado que está listo en una nueva ruta sintética sin crear el directorio de datos. Su advertencia sobre el almacenamiento de claves locales sigue vigente: los registros y los archivos multimedia no están cifrados por la aplicación.

El paquete «wheel» 0.4.0 se compiló y se instaló en un directorio independiente. Los 23 archivos de la aplicación coinciden con el código fuente byte a byte. El paquete instalado proporcionaba el panel y la guía y los recursos en inglés, rechazaba el acceso no autenticado a la API y exportaba un archivo ZIP sintético con 32 eventos que superó la verificación. Su comando de descarga en streaming también obtuvo un archivo ZIP verificado de forma independiente desde la aplicación instalada y en ejecución.

La documentación pública y la guía local están en inglés; los enlaces a la documentación local funcionan correctamente. PowerShell ha analizado la plantilla de tareas de Windows y Python ha analizado el archivo plist de macOS. Se trata de comprobaciones sintácticas, no de la ejecución del servicio. No se ha registrado ninguna tarea ni servicio. La configuración de CI incluye ahora comprobaciones de disponibilidad, pero la CI remota no se ha ejecutado aquí.

En la ejecución 0.4 del navegador se observó de nuevo la inyección del host AdGuard y el error OSError 10022 de Windows asyncio relacionado con la limpieza de sockets. Las comprobaciones del navegador se superaron; estas observaciones ambientales se conservan en lugar de tratarse como un comportamiento fijo de la aplicación. Los intentos iniciales en el entorno aislado (sandbox) de OpenSSL, el navegador y pip fracasaron; las ejecuciones de calificación que tuvieron éxito utilizaron una ejecución autorizada fuera del entorno aislado.

## La versión 0.3.1 se centra en correcciones de preparación.

Las comprobaciones del lanzador, el almacenamiento de pruebas y la API afectadas se han superado: **31 superadas, 1 omitida**, una advertencia de Starlette en el código fuente. La comprobación omitida verifica los permisos de directorio POSIX y no puede establecer dichos permisos en este host de Windows. La prueba con Python antiguo simula el límite de versión/importación; no se instaló ni se validó ningún intérprete de Python 3.10. A continuación se registra el conjunto de pruebas 0.3 que había superado anteriormente; no se volvieron a ejecutar ni el conjunto completo de pruebas ni los escenarios de navegador para estos cambios específicos.

El lanzador habitual actualizó el entorno local a la versión 0.3.1; el código fuente y los metadatos de la instalación coinciden, y la comprobación con pip se superó. Una rueda 0.3.1 instalada por separado proporcionó el panel y los recursos, rechazó el acceso no autenticado a la API y generó una exportación sintética verificada de 32 eventos. Se analizó el archivo YAML del flujo de trabajo, pero no se ejecutó la nueva comprobación del entorno de ejecución del contenedor: no había disponible ningún entorno de ejecución local utilizable de Docker, Podman o Linux.

Consulte [los resultados de la evaluación de la preparación](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) para conocer las deficiencias restantes en materia de usabilidad, servicio en vivo y plataforma. Este parche no es compatible con sistemas operativos adicionales.

## Versión 0.3.0

La suite completa de ejecución fijada ha superado **61 pruebas**, con una advertencia de obsolescencia de Starlette TestClient en el código fuente. Los metadatos de ejecución indican TgWitness 0.3.0 y python-socks 2.8.2; la comprobación con pip se ha superado. La prueba de compatibilidad con el navegador se ha superado sin errores de JavaScript en la página.

Se compiló el paquete «wheel» 0.3.0 y se instaló en un directorio de paquetes independiente. Este proporcionó el panel y los recursos, rechazó una solicitud de API no autenticada y exportó un registro sintético de 32 eventos que superó una verificación independiente. Los enlaces a la documentación local funcionan correctamente. Tras la corrección de la normalización de claves sin formato de MTProxy, las nueve pruebas de conexión y seguridad se volvieron a ejecutar con éxito.

La nueva cobertura incluye:

- Nombre de usuario y contraseña de SOCKS5 y HTTP CONNECT a través de servidores de prueba de bucle invertido reales; un proxy inactivo falla en lugar de recurrir al destino.
- Validación de proxies, selección del transporte MTProxy, rechazo de secretos TLS falsos, persistencia, aislamiento del espacio de trabajo, rechazo de cambios durante la observación y exclusión de secretos del estado de la API y de los eventos firmados.
- Conversión de solo lectura de los esquemas sintéticos de Telethon SQLite 7 y 8; hash de origen sin cambios; rechazo de otros formatos, vistas SQL y un archivo WAL pendiente.
- Clave maestra externa del almacén: diferentes claves derivadas del espacio de trabajo, reapertura correcta, rechazo en caso de clave incorrecta o ausente, y ausencia de migración implícita de los almacenes locales existentes.
- Configuración del proxy del navegador, borrado de credenciales, divulgación de la protección del almacenamiento, página de conexión móvil, autorización de archivos de sesiones convertidas, rutas independientes, y todos los escenarios de recopilación y exportación tratados anteriormente con un cliente de Telegram falso.

Durante el desarrollo, una prueba de bucle de retorno esperaba indefinidamente a que el par se desconectara; en otra ejecución se observó un restablecimiento de la conexión en Windows tras el protocolo de enlace. El dispositivo de prueba ahora delimita todo el intercambio y trata el EOF o el restablecimiento tras un protocolo de enlace completado como un cierre de la conexión. Las verificaciones de establecimiento de conexión y autenticación siguen siendo necesarias. Esto no descarta a los proveedores de proxy reales ni implica un defecto fijo en el transporte de Telegram.

La observación sobre la solicitud de AdGuard que se describe a continuación sigue siendo válida. No se utilizó ninguna cuenta real de Telegram, ni ningún proxy SOCKS/HTTP externo, ni ningún servidor MTProxy en producción. MTProxy es experimental y se han comprobado las opciones seleccionadas y la validación de claves secretas, pero no la interoperabilidad en producción. Los nuevos comandos de conversión de claves externas y de sesión se han probado únicamente con secretos sintéticos. Linux, macOS y Docker siguen sin estar verificados en este contexto.

La medición de rendimiento de la versión 0.2 que figura a continuación no se ha repetido y no debe presentarse como una nueva referencia de rendimiento con múltiples cuentas o proxies para la versión 0.3.

## Versión 0.2.0 de referencia

Probado en Windows con Python 3.12.10. No se conectó ninguna cuenta real de Telegram.

| Comprobar | Resultado |
| --- | --- |
| Conjunto de herramientas en Python | Se han superado 52 pruebas en el entorno de desarrollo y 52 con el tiempo de ejecución fijado; se ha producido una advertencia de obsolescencia de Starlette TestClient en cada ejecución. |
| Sintaxis de JavaScript | Desarrollado con Node.js |
| Aceptación de Chromium | Aprobado; no se han detectado errores de JavaScript en la página. |
| Diseño para ordenador y móvil | Comprobado a 1440 × 1060 y 390 × 844; sin desbordamiento horizontal del documento |
| Contenido del mensaje en formato HTML | Se ha convertido a texto; el script insertado no se ha ejecutado |
| Flujo de cuenta de ejemplo | Credenciales de la API → teléfono → código → 2FA → seleccionar grupo → iniciar → captura instantánea → pausar → recargar |
| Pruebas en el navegador | Comparación de ediciones, contenido anterior tras la eliminación, filtros, descarga en formato ZIP, punto de control, acuse de recibo firmado del proceso, descarga de solicitudes según RFC 3161 y vinculación de puntos de control. |
| Múltiples cuentas | Registros, claves, fuentes y estados en tiempo real independientes; al cambiar de navegador, el otro recopilador sigue funcionando; los espacios de trabajo se reabren tras reiniciar el sistema; se rechazan las cuentas duplicadas y la reasignación de cuentas. |
| Fallos criptográficos | Campos firmados modificados, campos sin firmar añadidos, clave incorrecta, elemento del archivo dañado, archivos multimedia modificados o faltantes, truncamiento detectado en el punto de control rechazado |
| Almacenamiento | Las adiciones simultáneas se verifican; las actualizaciones o eliminaciones activan el rechazo; al iniciarse, el sistema rechaza un registro modificado sin haberlo añadido y libera su bloqueo. |
| Durabilidad de los soportes | Escrituras atómicas de mensajes/tareas; recuperación tras reinicio; conservación de los descriptores de la versión original; rechazo de la sustitución de colas y de la corrupción de archivos existentes; persistencia de FloodWait; aislamiento de fallos en el origen. |
| Transmisión en directo | Se exporta un prefijo estable a medida que se añaden nuevos registros; un punto de control conservado detecta si el registro está truncado; la exportación no recoge la totalidad del flujo de eventos. |
| RFC 3161 | OpenSSL 3.5.9 lee las solicitudes generadas; se aceptan las respuestas sintéticas de CA/TSA generadas localmente; se rechazan los datos alterados, los nonces y las CA erróneas; el entorno de CA no anula la confianza explícita. |
| Configuración local | start.py --setup-only ha actualizado el entorno .venv aislado a la versión 0.2.0; el código fuente y los metadatos instalados coinciden; la comprobación de pip se ha superado |
| Wheel | Se ha compilado la versión 0.2.0 e instalado por separado en la carpeta «test-results»; se han servido paneles y recursos, se han rechazado las solicitudes a la API sin autenticar, y se ha exportado y verificado un archivo sintético de 32 eventos. |

En las pruebas de código fuente se utilizaron FastAPI 0.159.1, Uvicorn 0.54.0, Telethon 1.45.0, cryptography 50.0.2, pytest 9.1.1 y Playwright 1.62.0. El entorno de ejecución fijado utiliza FastAPI 0.162.0, Starlette 1.10.0, Uvicorn 0.54.0, Telethon 1.45.0 y cryptography 50.0.2. El archivo `deploy/constraints.txt` registra las versiones fijas del entorno de ejecución; los archivos `deploy/requirements.lock` y `deploy/build.lock` incluyen el SHA-256 de cada archivo de paquete, y los servidores Docker y de alta seguridad solo realizan instalaciones a partir de ellos (pip --require-hashes). Ninguna de estas medidas constituye una garantía de compatibilidad en todas las plataformas de CI configuradas. La CI remota no se ha ejecutado.

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

## Observaciones sobre el entorno

Las restricciones del entorno aislado de Windows bloquearon los directorios temporales predeterminados de pytest/pip y el subproceso de Playwright. Pytest utilizó un nuevo directorio temporal dentro del proyecto; los procesos de instalación y del navegador requerían una ejecución autorizada fuera del entorno aislado.

AdGuard, instalado en el equipo, inyectó solicitudes a local.adguard.org en el navegador. El registro del navegador conserva dichas solicitudes. Esta ejecución **no** constituye prueba de que no haya ninguna solicitud saliente en un entorno de navegador no modificado; el propio código fuente de la aplicación no contiene solicitudes a recursos externos, CDN ni servicios de análisis. No se modificaron los ajustes de AdGuard.

En la última ejecución del navegador también se registró un error OSError 10022 de limpieza de sockets asíncronos de Windows. Se superaron todas las comprobaciones del navegador y no se produjeron errores de JavaScript en ninguna página. No se determinó su causa y esta ejecución no demuestra la ausencia de problemas de transporte del servidor.

La primera prueba HTTP del paquete instalado, que utilizaba las solicitudes de cierre de conexión de urllib, detectó reinicios de conexión, tanto dentro como fuera del entorno aislado y con ambos conjuntos de dependencias. La prueba final utilizó conexiones persistentes HTTP/1.1 estándar a través de http.client y superó la prueba. Las solicitudes del navegador también superaron la prueba. No se determinó el origen exacto de los reinicios; no se calificaron como un defecto fijo de la aplicación.

## Cualificación restante

El registro en tiempo real conservado recoge de forma fehaciente las recopilaciones, modificaciones, avisos de eliminación, archivos adjuntos, nuevas comprobaciones y la gestión de los límites de frecuencia. No registra de forma exhaustiva la entrega ni ofrece una matriz controlada de visibilidad de roles, agentes de reacción, esperas prolongadas (FloodWait), bloqueos de cuentas y recuperación tras interrupciones de red o procesos. La emisión de tokens QR sigue siendo independiente de la confirmación completa del código QR en el móvil.

La compilación y ejecución en Docker, la instalación en Linux y macOS, la capacidad para soportar cargas elevadas de forma sostenida, la revisión de seguridad independiente, una respuesta TSA verdaderamente independiente, la validación de la revocación y el archivo de certificados, así como la certificación forense, quedan fuera de la certificación obtenida. Se han implementado el estado guardado de MTProto y la puesta al día; la reproducción atómica duradera sigue sin estar establecida. La recopilación de registros de administración, las listas de reactores adicionales y el sondeo corto prioritario siguen siendo características independientes. Consulte [la aceptación en tiempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) para consultar la matriz de cualificación controlada.

Los recibos locales detallados y las capturas de pantalla se encuentran en la carpeta test-results/ (ignorada por Git). La captura de pantalla pública que se encuentra en docs/assets/ contiene únicamente datos de demostración ficticios.

## Preparación del sitio web público y de la publicación · 27 de octubre de 2026

La presentación independiente de `website/` y la compilación de Pages se añadieron tras las comprobaciones del panel mencionadas anteriormente. No se modificó ninguna configuración de la cuenta activa ni la lógica de recopilación.

- El conjunto de aplicaciones existente superó las pruebas: 138 superadas, 1 omisión exclusiva de POSIX y una advertencia de obsolescencia de Starlette/httpx en el código fuente. Las 11 pruebas de compilación del sitio añadidas se superaron de forma independiente, incluyendo el rechazo de salidas inesperadas y el rechazo de entradas enlazadas.
- Ambos scripts de navegador de la aplicación superaron las pruebas utilizando project-venv Playwright y Chromium headless shell 156. No se registraron errores de JavaScript en las páginas ni solicitudes externas. Todos los escenarios de cuentas utilizaron datos de transporte falsos y ficticios.
- `tools/check_site.py` superó las pruebas con anchos de 320, 390, 768, 1024 y 1440, con una subruta de la URL del proyecto, pestañas del teclado, acceso al portapapeles concedido o denegado, movimiento reducido y JavaScript desactivado. No se produjeron fallos en las solicitudes de recursos ni en las solicitudes externas.
- `tools/build_site.py` generó 10 archivos públicos incluidos en la lista de permitidos, con un tamaño total de unos 460 KB. Las capturas de pantalla del navegador y un recibo se encuentran en el archivo `test-results/site/`, que se ha ignorado.
- El archivo «wheel» se ha compilado correctamente tras instalar las herramientas setuptools/wheel destinadas exclusivamente a la compilación en el entorno del proyecto. Tras instalarlo en un entorno de destino aislado y ejecutar «`tools/check_install.py`», se han superado las pruebas: activos estáticos, control de acceso, una exportación sintética firmada de 32 eventos y una descarga en streaming verificada de forma independiente.
- Se ha superado la prueba `pip check`. Un análisis de patrones de los candidatos públicos seleccionados en Git no ha encontrado bloques de claves privadas reconocibles, tokens de GitHub/bot/AWS, asignaciones de secretos literales largos ni marcadores de conflictos de fusión. Esto no constituye una prueba de que todos los posibles formatos secretos estén ausentes. Las sondas de datos en tiempo de ejecución, de sesión y de claves fueron ignoradas por Git.
- La autenticación de GitHub CLI no era válida; no se había configurado ningún servidor remoto y no existía ninguna confirmación inicial. No se ha realizado ningún envío, flujo de trabajo alojado, implementación de Pages ni lanzamiento. Docker y la validación en tiempo real de Telegram y la plataforma quedan fuera del alcance de esta comprobación.

En este servidor, el bloqueo de descarga de Playwright falló en el sistema de archivos del espacio de trabajo E:. La instalación de Chromium en `%LOCALAPPDATA%/tgwitness-playwright` y el uso de ese mismo `PLAYWRIGHT_BROWSERS_PATH` para las comprobaciones se realizaron con éxito. Se trata de una solución alternativa del entorno, no de un cambio en las dependencias de tiempo de ejecución de la aplicación.

## Documentación interactiva y metadatos del sitio web · 29 de octubre de 2026

El sitio web público consta de 12 páginas HTML en inglés: una página de inicio, un índice de guías y diez guías. El artefacto contiene 28 archivos de presentación enumerados explícitamente, aproximadamente 1,85 MB, y no incluye datos de recopilación. El sitio web público está en inglés; las traducciones de la aplicación y las guías traducidas del repositorio se encuentran en archivos separados.

- Pruebas del sitio web, de la publicación original y de los límites de la versión: **18 superadas, 2 omitidas**. Las pruebas omitidas se refieren a la creación de enlaces simbólicos en este sistema de archivos de Windows. Las pruebas comprueban los metadatos únicos de las páginas, las páginas públicas exclusivamente en inglés, las URL canónicas, todas las entradas del mapa del sitio, los recursos y enlaces locales, la navegación estructurada y la exclusión de archivos privados.
- Tanto `tools/check_site.py` como `tools/check_docs_site.py` superaron las pruebas en Chromium a 320, 390, 768, 1024 y 1440 píxeles en una subruta de la URL del proyecto. Las comprobaciones de la guía abarcan las 11 páginas de documentación, la búsqueda y la navegación mediante teclado, el funcionamiento correcto o defectuoso del portapapeles y la legibilidad del contenido sin JavaScript.
- Se han superado cinco ejemplos interactivos: reproducción/avance paso a paso/pausa/reinicio de mensajes con movimiento reducido y suspensión fuera de pantalla; cadenas de hash originales/alteradas/reconstruidas/truncadas; decisiones de aceptación/reversión/bifurcación/ausencia de respuesta por parte de los testigos; y escenarios de entrega completa/retrasada/ausente; así como un mapa de investigación que vincula observaciones ficticias de chats cruzados por ID del remitente, destino y hash del archivo adjunto . Los controles de investigación superaron las comprobaciones de navegación por teclado y de solución alternativa sin JavaScript. Los resultados SHA-256 del navegador se compararon de forma independiente con el `hashlib` de Python y el JSON canónico. El ejemplo de hash también conservó su alternativa legible cuando Web Crypto no estaba disponible.
- Las proporciones de visualización y los marcadores de los gráficos se ajustaron a la tabla accesible. Las etiquetas del eje móvil se ampliaron tras una revisión visual. Cada ejemplo se identifica como ilustrativo o sintético, y ningún ejemplo del navegador se conecta con Telegram.
- No se registraron solicitudes externas, solicitudes HTTP fallidas ni errores de JavaScript. Las capturas de pantalla de escritorio y móvil, así como los recibos, se encuentran en las secciones ignoradas `test-results/site/` y `test-results/docs-site/`. Se revisaron el índice de la documentación, los ejemplos de mensajes y hash, el diseño de Witness, el gráfico de entrega y el mapa de investigación en formatos de escritorio y móvil.
- La comprobación de la publicación superó la verificación de 282 archivos de fuentes públicas y 1.426 enlaces de documentación locales. Ruff superó la comprobación de las herramientas y pruebas modificadas del sitio en Python.
- `docs/HOW-IT-WORKS.md` ofrece un complemento de GitHub Markdown con diagramas y fórmulas de Mermaid . `docs/INVESTIGATION.md` abarca el ámbito de toda la cuenta, la adquisición del historial por chat, los perfiles de los usuarios, las referencias entre chats, las líneas temporales y el traspaso de casos verificados. Sus pasos y limitaciones se han contrastado con el código actual relativo al ámbito de aplicación, la recopilación, el expediente, la exportación, el verificador y el panel. No se ha comprobado la representación alojada en GitHub.

Se trata de una comprobación local del sitio web y la documentación. No añade la certificación de Telegram en tiempo real ni confirma la implementación de Pages alojadas, el éxito de la infraestructura de código (CI) remota ni la indexación en motores de búsqueda. Consulte [el procedimiento de publicación](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md) y [las notas sobre los metadatos del sitio web](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/SEO.md).
