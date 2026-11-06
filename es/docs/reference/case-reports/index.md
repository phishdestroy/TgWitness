# Configuración y verificación de informes

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/case-reports/

Filtros de informes, ocho diseños, plantillas de contenido, historiales de cambios guardados y la evaluación incluida en las exportaciones firmadas.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentación](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Investigation](https://phishdestroy.github.io/TgWitness/es/docs/reference/investigation/)

![Investigation](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

Convierta las observaciones seleccionadas en un resumen legible del caso: su cuestión, alcance, cambios guardados, gráficos, conclusiones y referencias a las fuentes. Cada informe ofrece al destinatario una forma de comprobar el material entregado e inspeccionar la cobertura de la recopilación.

La sección **«Base de confianza y limitaciones»** aparece en los informes de diario, traspaso, chat, cuenta y uso compartido. Los archivos PDF de diario y traspaso utilizan la misma evaluación que su archivo «`report.json`» firmado. Los manifiestos ZIP incluyen «`case_assessment`» en el manifiesto firmado. Esta evaluación se transmite junto con el material exportado. Las observaciones originales conservan sus firmas existentes.

## Formatos de los documentos y orden de lectura

### Estudio de informes

Abre **«Exportaciones» → «Configurar» y «Vista previa**». Sigue el proceso en **«Datos» → «Diseño y contenido» → «Vista previa**»:

1. Utilice todo el espacio de trabajo o seleccione chats, autores, fechas de observación en UTC y tipos de eventos. Cargue el catálogo para buscar chats y autores, o introduzca sus ID de Telegram. Los filtros de autor coinciden con los ID de remitente registrados; un aviso de eliminación sin remitente no coincide con un filtro de autor.
2. Elige un diseño de página y, a continuación, selecciona los gráficos, las etiquetas de los participantes, la transcripción y tus conclusiones por escrito. Al cambiar el diseño, se mantienen estas opciones.
3. Genera la vista previa. En ella se muestran los recuentos reales, la actividad, los participantes, los registros de muestra, los cambios guardados y los rangos de números de mensajes que faltan. Si se cambia una opción, la vista previa queda desactualizada. Guarda antes de descargar el HTML, el PDF firmado, el JSON firmado o el archivo ZIP con las pruebas.

La vista previa de los datos incluye el prefijo completo y estable del registro, no una muestra inicial. Solo se limitan las filas de muestra mostradas y las listas largas; se muestran sus recuentos omitidos. Una exportación posterior toma una nueva instantánea estable, por lo que la recopilación en curso puede aumentar las cifras. El alcance, los recuentos y la identidad de la fuente se incluyen en el informe firmado. Abrir o previsualizar el formulario no lo guarda.

**Jurisdiction guidance.** Under Document details, open **Jurisdiction guidance · optional** to choose a jurisdiction and civil/commercial or criminal procedure. The appendix carries the legal basis, source links, preparation notes and research status. Local-language summaries and explanations of collection safeguards are optional. No jurisdiction is selected by default. These choices belong to the workspace, and are excluded from saved layout configurations and implicit sharing-copy defaults. See [defaults, supported reports and research limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/JURISDICTION_GUIDANCE.md).

**Elige la copia destinada al destinatario.** Los gráficos y la transcripción utilizan los registros seleccionados. La integridad, la custodia y la cobertura describen el diario de fuentes completo. El archivo ZIP de pruebas contiene sus registros originales y archivos adjuntos. Utiliza [una entrega minimizada](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#handover-extract) cuando el destinatario solo deba recibir datos seleccionados y autorizados.

### Leer modificaciones, eliminaciones e identificadores que faltan

Una modificación muestra el texto guardado **«antes»** y **«después»** y resalta las palabras modificadas. Una eliminación muestra la última versión guardada antes de la notificación. Si no se ha capturado ningún contenido anterior, el informe así lo indica. Cuando se seleccionan únicamente modificaciones o eliminaciones, las versiones anteriores siguen estando disponibles como contexto etiquetado explícitamente fuera de los filtros. Los mensajes no relacionados no se añaden a estos historiales.

**Los ID de mensajes no observados** son huecos entre números conocidos en los chats seleccionados y el intervalo de ID derivado de la fecha. Se comprueba cada registro de fuente conocido antes de declarar un número como no observado: filtrar a otro autor, un tipo de evento o una fecha no puede crear un hueco falso. Los mensajes guardados adyacentes se etiquetan como contexto. La ausencia de un número no prueba que un mensaje existiera o que se haya eliminado; los avisos de eliminación y las nuevas comprobaciones fallidas siguen siendo tipos de eventos independientes.

### Elige un diseño

Hay disponibles ocho diseños de página para informes en formato HTML (diario y chat individual) y PDF firmados. Utilizan los mismos registros y cálculos, con diferentes portadas, tipografía, títulos de capítulos, tablas y espaciado.

| Diseño | Estilo de lectura |
| --- | --- |
| Clásico | Un expediente tradicional con cubierta oscura y secciones numeradas. |
| Editorial | Una página de título con marco y tipografía serif, márgenes amplios y una barra de capítulos estrecha. |
| Instrucciones | Una portada compacta con lomo azul marino, títulos breves y tablas con espaciado reducido. |
| Análisis | Una portada estilo encuesta, tablas modulares y figuras con espaciado fijo. |
| Técnico | Un registro rayado, una barra de referencia numerada y tablas de comparación precisas. |
| Resumen | Una portada panorámica, espaciado generoso y cifras resumidas destacadas. |
| Serie de lectura | Una barra lateral y capítulos agrupados para los resultados, el alcance, los cambios y el diario de observaciones. |
| Libro mayor y margen | Capítulos numerados con un margen amplio, tablas y gráficos exactos y una transcripción de los mensajes en un apartado separado. |

El diseño se guarda por espacio de trabajo y se registra en el manifiesto de exportación firmado. El HTML funciona sin conexión, admite temas claros y oscuros, y se adapta a pantallas estrechas y a idiomas que se escriben de derecha a izquierda. Los PDF nativos utilizan fuentes incluidas; el diseño editorial incluye Noto Serif bajo su licencia SIL Open Font License incluida. Las series de lectura y el «Ledger & margin» también se aplican a los resúmenes de cuentas, los chats de cuentas y el intercambio de copias.

Los archivos PDF en chino, japonés y coreano requieren además una fuente adecuada en el servidor, como Noto Sans CJK, instalada en todo el sistema o ubicada en `TGWITNESS_FONT_DIR`. Si no está disponible, el archivo ZIP conserva los informes en formato HTML y JSON.

Estos dos diseños incluyen un registro legible sin JavaScript. Para exportaciones de gran volumen, esta vista contiene hasta 500 registros completos dentro de un límite de entrada de 8 MiB; el informe indica el límite y ofrece enlaces al visor completo y a los registros originales. El directorio de cuentas y el índice de relaciones describen esa misma muestra de lectura, no a todos los participantes. Los gráficos del diario completo mantienen su ámbito de aplicación indicado por separado.

### Selecciona el contenido

| Contenido preestablecido | Incluido por defecto |
| --- | --- |
| Expediente del caso | Actividad, horas de observación, participantes, chats y la transcripción del registro. |
| Instrucciones | Resumen de actividades sin clasificaciones de los participantes ni la transcripción. |
| Revisión de actividades | Actividad, horas de observación, participantes, chats y composición, con referencias a las fuentes y cifras exactas. |
| Informe personalizado | Tu propia combinación de gráficos, transcripciones y vistas previas. |

Al cambiar una configuración preestablecida, se conservan el diseño, los detalles del caso y el análisis escrito. Las comprobaciones de integridad, la cobertura, las limitaciones y las instrucciones de verificación se mantienen en cada diseño. Los registros originales del archivo ZIP permanecen inalterados cuando se oculta un gráfico o una transcripción.

Las **«Notas de examen»** opcionales contienen la pregunta, el método, los resultados y la conclusión redactados por el autor del informe. Cite el archivo de origen y los números de registro en los resultados. La firma conserva estas declaraciones del autor junto con el informe; las observaciones de origen y la interpretación del autor siguen siendo identificables. Los traspasos simplificados omiten estas notas privadas y las historias clínicas completas. Las opciones de historia clínica y exploración se aplican a los informes de la historia clínica.

Selecciona la actividad a lo largo del tiempo, el mapa de calor de días laborables y horas en UTC, las clasificaciones de participantes, las clasificaciones de chats y la composición de los registros. Elige entre 5 y 30 grupos clasificados y alias de participantes neutros o ID de cuenta. Los remitentes desconocidos y el resto de participantes aparecen en filas separadas. Los alias solo afectan a los gráficos; los registros de origen siguen conteniendo sus identidades.

La vista previa del diseño se actualiza a partir del borrador sin guardar utilizando la portada de producción, el examen y los componentes de gráficos, limitada a las coincidencias dentro de los primeros 50 000 registros de origen. La vista previa de datos que aparece a continuación calcula la selección completa. Está explícitamente sin firmar y no conserva las modificaciones. Los botones «Portada» y «Gráficos» cambian de sección. No se trata de una vista previa completa del PDF. La opción **«Guardar configuración del informe»** aplica las opciones a futuras exportaciones; los archivos firmados existentes son inmutables. El PDF utiliza la portada elegida, la tipografía, el diseño de capítulos y los mismos agregados seleccionados que el HTML y el JSON firmado.

La evaluación de fiabilidad, las limitaciones de cobertura y las instrucciones de verificación siguen estando presentes. Ocultar los gráficos o la transcripción legible no elimina las filas de fuentes fidedignas del archivo ZIP. Las series de gráficos desactivadas se omiten del JSON analítico; utilice una exportación minimizada para restringir la divulgación de los registros de origen.

Los filtros de selección de datos se aplican a los informes de registro; las exportaciones de cuentas y de contenido compartido conservan su propio ámbito de adquisición y divulgación.

Las preferencias compartidas de diseño y gráficos se conservan en las nuevas exportaciones de chats y cuentas, así como en las vistas previas de cuentas compartidas. La configuración de idioma y privacidad de las cuentas y del compartir se mantiene independiente; las notas privadas de casos y de examen no se copian en estas exportaciones. Los informes de cuentas y de compartir siguen estando en formato HTML protegidos por su manifiesto de archivo firmado. El diario, el traspaso de diario minimizado y los kits de chat único también proporcionan archivos PDF firmados.

### Lo que recogen los gráficos

La actividad del diario y los mapas de calor contabilizan **las observaciones** nuevas, históricas, recuperadas, editadas, eliminadas y ausentes en la nueva comprobación, según la hora de observación del recopilador en UTC. Se excluyen los latidos y los acuses de recibo de archivos adjuntos. Las clasificaciones de participantes solo cuentan las observaciones de mensajes nuevas, históricas y recuperadas: no se considera que un remitente sea quien edita o elimina el mensaje. Las observaciones repetidas pueden referirse al mismo mensaje de Telegram.

Los análisis de registros conservan los recuentos por tipo, las referencias al primer y último registro y el SHA-256 del archivo fuente « `events.jsonl`». Las cifras incluyen valores exactos en HTML y PDF. Los intervalos diarios pasan a ser mensuales una vez superados los 366 días registrados; los gráficos los agrupan en un máximo de 36 intervalos de igual anchura. Más de 100 000 identificadores distintos o 1 200 meses hacen que el gráfico afectado no esté disponible, aunque los recuentos totales exactos siguen estando disponibles.

Los gráficos de instantáneas y de uso compartido de cuentas solo cuentan las filas de mensajes no de servicio incluidas, utilizando la hora de los mensajes registrada. Los totales de uso compartido se calculan tras la censura y el filtrado. Estos gráficos utilizan como máximo 90 intervalos de fecha UTC de igual anchura y conservan hasta 10 000 valores de agrupación; los recuentos excedentes se declaran y concilian explícitamente. El último intervalo puede ser más corto. Las fechas desconocidas o aproximadas no se incluyen en los gráficos temporales.

Un intervalo vacío significa que no hay observaciones incluidas; consulta la cobertura para ver las lagunas. Estos gráficos describen la actividad guardada. Los remitentes desconocidos siguen siendo una categoría aparte, y cada comprobación se registra de forma individual.

Cuando se incluye, el archivo «`analytics.json`» queda protegido por los hash de los archivos firmados del archivo. El informe de registro «`report.json`» incorpora el mismo agregado seleccionado. La verificación de la firma detecta los bytes modificados. Para comprobar las cifras, vuelva a calcular los agregados del registro con «`report_analytics.Analytics`» y «`selected`», o los agregados de la instantánea con «`snapshot_analytics.collect`» y «`project`».

### Anomaly indicators

**Preview.** Evidence reports add an **Anomaly indicators** section computed by registered processors (`tgwitness/metrics/`, one file per metric). The report names every processor that ran with its version, and prints its method under its table, so the computation can be repeated from `events.jsonl` with `tgwitness.metrics.run`.

| Processor | Qué muestra |
| --- | --- |
| `first_time_posters_over_time` v1 | First-time posters and messages per UTC day. A flag requires at least five first-time posters and three times their median, with message volume at most 1.5 times its median. The baseline uses at least seven observed days within the previous 14 calendar days, after seven days of warm-up. |
| `service_vs_message_ratio` v1 | Distinct saved message numbers per chat and the share used by service messages. It describes a numbering; it does not explain a particular missing number. |
| `join_leave_per_month` v1 | Joins, departures and removals or bans per month, one per person, chat, change and day. |
| `pinned_per_month` v1 | Pin service messages, unpin notices, and pinned messages added or removed between chat-state snapshots, per month. |

**Parameters → Report metrics** selects processors and the number of displayed rows, including in filtered reports. Daily and monthly tables show recent rows, service-share tables rank chats by saved message count. Totals cover every row.

A partir de una copia del código fuente, crea los ocho diseños mencionados anteriormente a partir de la misma revista ficticia:

```
python tools/build_report_styles.py --output test-results/report-styles
```

Abre el archivo «`index.html`» resultante para comparar los informes HTML completos, los PDF firmados y los archivos ZIP. Todos los diseños utilizan el mismo diario de origen. Utiliza un nuevo directorio de salida para cada ejecución, de modo que se conserven los ejemplos firmados anteriormente.

![Expediente HTML ficticio](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

El HTML comienza con una portada del caso y cifras clave. El mapa de pruebas numerado enlaza con cada hallazgo, sus hechos justificativos, sus limitaciones y su revisión independiente. Los registros buscables y las referencias de registros estables siguen estando disponibles en el visor sin conexión. El diseño se adapta a pantallas estrechas, tanto a temas como a navegadores sin JavaScript.

El PDF firmado cuenta con una portada específica en formato A4, una referencia del informe y un código QR, un resumen ejecutivo, un mapa de pruebas, conclusiones numeradas y marcadores de documentos. Sus encabezados y pies de página identifican el informe. Un código QR identifica el material; no se trata de un resultado de verificación independiente. Las impresiones desde el navegador son independientes de este PDF firmado criptográficamente.

La línea de tiempo de observación sitúa los periodos de observación registrados y las interrupciones en el mismo eje UTC. El espacio en blanco no implica cobertura; las tablas detalladas conservan los intervalos exactos. El archivo ZIP contiene los informes legibles, el JSON firmado, los registros de origen y las instrucciones de verificación.

Crea un expediente nuevo y ficticio en inglés, ruso y alemán con el entorno de desarrollo instalado:

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Cada directorio de idioma contiene `report.html`, `report.pdf`, `report.json` y `dossier.zip`. Los directorios de ejemplos existentes nunca se sobrescriben. Para crearlo no se utiliza ninguna cuenta de Telegram, servicio externo de marca de tiempo ni conexión de red.

![Las tres primeras páginas del PDF ficticio firmado](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## Análisis de un caso concreto

En el caso de un registro de 1.200 entradas con una marca de tiempo validada en la entrada 1.000, el informe identifica 200 entradas posteriores fuera del límite de dicha marca de tiempo. Se trata de un límite superior respecto a la existencia de un punto de control, no de una prueba de la hora de envío de cada mensaje. Si otros tres archivos de marcas de tiempo no superan la validación o no pueden validarse, se cuentan por separado y no pueden aportar una conclusión positiva.

Una marca de tiempo válida debe cumplir todos estos requisitos: su huella coincide con el punto de control, su firma se remonta a una raíz TSA de confianza en el momento de la marca, y la firma, la clave, el recuento y el encabezado del punto de control coinciden exactamente con el prefijo del diario. No basta con analizar una marca de tiempo o disponer de un recibo de OTS. El lector debe elegir de forma independiente la raíz TSA de confianza y repetir la verificación. OTS necesita su propia comprobación de confirmación de Bitcoin.

| Estado del informe | Significado |
| --- | --- |
| Comprobado durante la exportación | El exportador ha realizado la comprobación indicada; aún es necesario repetirla de forma independiente. |
| Grabado; se requiere revisión | Se registra la observación subyacente o la declaración del operador; no se trata de una confirmación independiente. |
| No se incluye en este texto | El texto no aporta ninguna prueba que respalde esta afirmación. Tampoco afirma que no exista en ningún otro lugar. |
| No se ha comprobado de forma independiente | El informe no proporciona un resultado de verificación independiente. |
| Incompleto o no disponible | Falta algún material o alguna comprobación obligatoria, o bien está incompleto o no se ha realizado correctamente. |

Revisa cada comprobación por separado, junto con la cobertura de la recopilación registrada.

## Lo que debe conservar una configuración sólida

1. Antes de proceder a la recopilación, guarda la huella digital de la clave del recopilador a través de un canal de confianza independiente. Compara esa referencia con la clave de firma de la exportación.
2. Conserve los puntos de control con marcas de tiempo independientes y, cuando se utilice, un registro de testigos fuera del control administrativo del recopilador. Compárelos con el registro exportado para comprobar sus límites anteriores.
3. Alcance de la adquisición de registros, lagunas, filtros, límites y cambios en la recopilación. Explica los periodos que faltan y que son relevantes para la reclamación en cuestión, diferenciando claramente los ID de mensajes no observados, los avisos de eliminación y las revisiones fallidas.
4. Conserve los archivos ZIP originales y sus hash. Registre cada titular, transferencia, fecha y finalidad. Mantenga junto a ellos las declaraciones atribuidas a los operadores y las notas del caso.
5. En el caso de los mensajes de voz confidenciales, se deben conservar y verificar de forma independiente la cotización, la verificación, la cadena de certificados de Intel, las mediciones, la fuente exacta y las condiciones de gestión de claves. Se debe conservar el resultado de la verificación de la certificación junto con los artefactos revisados.

See [verification scope](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope) for the checks of acquisition, archive integrity, time and collection coverage in each mode.

## Revisión del destinatario

Utiliza una instalación fiable de TgWitness y una huella digital obtenida de forma independiente:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

El archivo ZIP de Witness debe proceder de una fuente independiente de confianza; conserve también su clave y su procedencia. Mantenga los comandos, la versión de la herramienta, los resultados, los hash de entrada revisados y las cuestiones sin resolver. La verificación de balizas es una comprobación en línea independiente; el generador de informes nunca se pone en contacto con un servicio con el único fin de mostrar un informe.

En caso de controversia sobre un mensaje concreto, cite la referencia del archivo, el archivo oficial y la referencia del registro; a continuación, describa el periodo de tiempo pertinente, las lagunas de cobertura, la selección y el material corroborativo. En el caso de una copia compartida, revise también la transformación registrada y sus referencias al archivo de origen. Los filtros privados y las asignaciones de identidad quedan fuera de su evaluación pública.

La verificación del PDF firmado detecta cambios en los bytes cubiertos. Conserva el archivo digital original y el resultado de la verificación junto con cualquier captura de pantalla o copia impresa para su lectura.
