# Prepara una copia para compartir

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/handover/

Comparte las observaciones pertinentes manteniendo intacto el espacio de trabajo original.

Un traspaso es un extracto independiente firmado. Selecciona los chats y las personas, reduce las identidades o el texto, y decide qué archivos y notas del equipo deben incluirse en la copia del destinatario. Su manifiesto registra la selección y el número de registros sin modificar, minimizados y omitidos.

## Preparar el extracto del destinatario

1. Abre **«Exportaciones» → «Extracto de traspaso**». Indica su finalidad, elige los chats y el periodo UTC opcional; a continuación, selecciona **«Cargar personas de los chats elegidos»** si necesitas los nombres de los sujetos.
2. Elige cómo tratar al resto de personas: utiliza seudónimos, omite sus mensajes o muéstralos tal y como se han registrado. Configura el texto de los mensajes y los archivos adjuntos de forma independiente; opcionalmente, oculta los números de teléfono y las direcciones de correo electrónico.
3. Decide si incluir marcadores y fragmentos de «Case Board», o tarjetas con comentarios. Los alias de los investigadores pueden sustituir a los nombres de los equipos en este texto.
4. Selecciona **«Descargar extracto de entrega**». Abre localmente el informe generado y los registros seleccionados, verifica el archivo e inspecciona la copia antes de enviarla.

### Un original y una copia para compartir.

Ejemplo sintético · solo a título ilustrativo

1. **Seleccionar.** Incluir el chat del caso e identificar a la persona a la que se refiere el extracto.
2. **Minimizar.** Elige cómo aparece otro participante en la copia compartida.
3. **Revisa.** Abre el informe y los registros del archivo generado antes de enviarlo.
4. **Compartir.** Entregar la copia revisada y comunicar por separado su huella digital verificada.

#### Observación original

Nora · usuario 71002

«He recibido el enlace revisado».

El diario de origen conserva esta observación guardada.

#### Copia para el destinatario

Mostrar tal y como se registró: Nora · usuario 71002 · «He recibido el enlace revisado».

Seudónimo: P01 · «He recibido el enlace revisado».

Omitir: el mensaje de este participante no se incluye en el texto.

#### Revisa los archivos reales

Lee los archivos report.html y records.jsonl.

Comprueba las identidades, el texto, los archivos adjuntos y los comentarios opcionales del equipo.

#### Extracto firmado

Selección + hash de archivos + manifiesto firmado

Un paquete independiente vinculado al límite del diario de origen

## Utiliza los controles de forma conjunta

| Control | Repercusión en el texto |
| --- | --- |
| Personas | Mantén identificables a los sujetos seleccionados; seudonimiza u omite a los demás participantes según se considere oportuno. |
| Texto | Incluye todo el texto, solo el texto de las personas seleccionadas y de la cuenta observadora, u omite el texto de los mensajes y sus campos de detalles que contengan texto. |
| Archivos | Elige los archivos de las personas seleccionadas y de la cuenta de observación, todos los archivos de los mensajes mostrados o ningún archivo. |
| Case Board | No incluyas material del tablero, marcadores ni fragmentos, ni tarjetas con debates del equipo. |

Revisa el texto libre y el contenido de los archivos, así como las identidades: un seudónimo no elimina automáticamente todos los nombres que aparecen en un mensaje o archivo adjunto. Si un archivo conservado seleccionado no está disponible, restáuralo u omite explícitamente los archivos adjuntos antes de generar el extracto.

## Asegúrese de que el texto se pueda verificar de forma independiente.

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Conserva por separado el archivo original de pruebas firmado y los puntos de control. El traspaso registra su propia proyección, de modo que el destinatario puede comprobar la copia entregada sin necesidad de recibir todo el espacio de trabajo. [Report Studio](https://phishdestroy.github.io/TgWitness/es/docs/reports/) proporciona su diseño de lectura; [la verificación de la exportación](https://phishdestroy.github.io/TgWitness/es/docs/exports/) explica las referencias fiables.
