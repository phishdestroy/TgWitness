# Diseñar un informe

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reports/

Ofrece al lector una ruta clara desde la cuestión del caso hasta los registros guardados.

Report Studio combina la selección de datos, historiales de cambios legibles, gráficos y tus conclusiones por escrito. Los ocho diseños integrados se aplican a los formatos de salida compatibles: HTML y PDF nativo. Los informes en HTML, PDF y JSON llevan sus propios sellos firmados; el manifiesto ZIP también agrupa los archivos del paquete. Los archivos HTML y PDF se sellan una vez completado su diseño final.

## Elabora un informe en tres pasos

1. Ve a **Exportaciones → Configurar y vista previa → Datos**. Utiliza todo el espacio de trabajo o selecciona chats, autores, fechas de observación en UTC y tipos de registros. Las fechas indican cuándo TgWitness observó el registro.
2. En **«Diseño y contenidos**», elige una plantilla de diseño y contenidos. Selecciona los gráficos de actividad, las etiquetas de los participantes, la transcripción, los cambios guardados y el material opcional del «Case Board». Añade los detalles de tu caso y las notas de la investigación.
3. Abre **«Vista previa»** para revisar recuentos, actividad, participantes, registros muestreados y rangos de ID que faltan. Guarda la configuración y, a continuación, descarga el formato que necesites.

### Organiza el mismo material guardado para que resulte comprensible al lector.

Ejemplo sintético · maquetación esquemática, no es un informe generado

1. **Seleccionar.** Elige dos chats y el periodo de observación para el caso.
2. **Redacta el texto.** Elige un formato y las secciones que respondan a la pregunta.
3. **Vista previa.** Revisa el recuento de palabras seleccionado y el texto guardado «antes y después».
4. **Verificar.** Generar el archivo final y comprobar su firma comparándola con la huella digital del espacio de trabajo de confianza.

#### Observaciones seleccionadas

2 chats · 1 día de observación

Mensajes, ediciones y avisos de eliminación

#### Estructura del informe

##### Se ha cambiado el destino del pago

Pregunta del caso → alcance → conclusiones → referencias de los registros

**Contexto del mensaje**

Observación n.º 142: «Utiliza el nuevo enlace de pago».

**Cambios guardados**

Antes: old.example.invalid → Después: new.example.invalid

#### Revisar la selección

18 observaciones · 2 ediciones guardadas

Las horas de envío, edición y consulta tienen etiquetas distintas.

#### Entrega final

PDF firmado + JSON firmado, o un ZIP firmado con su informe legible

El destinatario comprueba el archivo y la huella digital de confianza.

## Elige un estilo de lectura

**Las secciones «Clásico», «Editorial», «Resumen», «Análisis», «Técnico», «Visión general», «Serie de lecturas» y «Libro mayor y margen»** presentan los mismos registros subyacentes en diferentes composiciones. Al cambiar el diseño, se mantienen la selección de datos y las notas escritas. El idioma del informe se puede elegir entre los 25 idiomas admitidos.

La «Reading series» agrupa el caso, el alcance, las conclusiones y los cambios en torno a una barra lateral. «Ledger & margin» utiliza capítulos numerados y un margen amplio. Ambas opciones admiten también resúmenes HTML de cuentas y el intercambio de copias. Los PDF nativos se generan con fuentes incluidas; el equipo del usuario no necesita tener instalado ningún navegador ni Node para la creación de PDF. Los PDF en chino, japonés y coreano requieren además una fuente adecuada en el servidor, como Noto Sans CJK, instalada en todo el sistema o ubicada en `TGWITNESS_FONT_DIR`. Sin ella, el archivo ZIP conserva los informes HTML y JSON.

## Lee cada cambio en su contexto

Las modificaciones guardadas se muestran «antes» y «después». Un aviso de eliminación puede ir acompañado de la última versión capturada. Las respuestas, citas, reenvíos, reacciones, botones y metadatos de los archivos adjuntos conservan sus referencias disponibles. Los hash SHA-256 de los archivos y los de los registros del diario se etiquetan por separado.

La vista previa del diseño muestra los componentes de portada, examen y gráficos utilizando registros coincidentes entre los primeros 50 000 registros de origen. La vista previa de datos independiente analiza la instantánea completa y estable del diario para obtener recuentos exactos de la selección, con los límites de la muestra mostrados y etiquetados. Genera un PDF para revisar la paginación final. La exportación completa de la cuenta incluye una vista general en HTML; los archivos PDF individuales de los chats utilizan el diseño elegido.

## Elige cuidadosamente la versión destinada al destinatario.

Los filtros de informe dan forma al informe legible. El archivo ZIP con todas las pruebas conserva el diario original y los archivos adjuntos. Utiliza una [entrega minimizada](https://phishdestroy.github.io/TgWitness/es/docs/handover/) cuando el destinatario solo deba recibir datos seleccionados. Consulta [el contenido del informe y la verificación,](https://phishdestroy.github.io/TgWitness/es/docs/reference/case-reports/) o [verifica la exportación finalizada](https://phishdestroy.github.io/TgWitness/es/docs/exports/).
