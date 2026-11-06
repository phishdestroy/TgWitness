# Telegram · Diseñar un informe

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reports/

Lleve al lector de la pregunta del caso directamente a los registros guardados.

Report studio junta los datos que elige, los historiales de cambios, los gráficos y sus conclusiones. Ocho diseños, HTML y PDF nativo. Cada informe HTML, PDF y JSON se sella con su clave.

## Elabora un informe en tres pasos

1. **Exportaciones → Configurar y previsualizar → Datos**: el espacio entero o los chats, autores, fechas (UTC, cuando TgWitness vio el registro) y tipos de registro que elija.
2. **Diseño y contenido**: elija un diseño y qué entra: gráficos, participantes, transcripción, cambios, elementos de Case Board, datos del caso y notas.
3. **Vista previa**: revise recuentos, actividad, muestras y rangos de IDs que faltan. Guarde y descargue el formato que necesite.

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

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, and Ledger & margin**: los mismos registros, otro aspecto. Al cambiar se conservan la selección y las notas. Cualquiera de los 25 idiomas.

Los PDF se generan con fuentes incluidas, sin navegador. Chino, japonés y coreano necesitan una fuente como Noto Sans CJK en el servidor (en el sistema o en `TGWITNESS_FONT_DIR`); si no, solo obtiene HTML y JSON.

## Lee cada cambio en su contexto

Las ediciones muestran antes y después; los borrados, la última versión guardada. Respuestas, reenvíos, reacciones, botones y adjuntos conservan sus referencias.

La vista previa del diseño usa los primeros 50 000 registros; la de datos lo cuenta todo con exactitud. Para la maquetación final, genere el PDF.

## Elige cuidadosamente la versión destinada al destinatario.

Los filtros solo dan forma al informe; el ZIP de evidencia sigue teniendo el diario y los archivos completos. Si el destinatario debe recibir menos, use una [entrega minimizada](https://phishdestroy.github.io/TgWitness/es/docs/handover/). Más: [contenido del informe](https://phishdestroy.github.io/TgWitness/es/docs/reference/case-reports/), [verificar la exportación](https://phishdestroy.github.io/TgWitness/es/docs/exports/).
