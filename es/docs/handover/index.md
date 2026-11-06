# Prepara una copia para compartir

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/handover/

Comparta solo lo necesario; el original queda intacto.

Una entrega es un extracto firmado aparte: elija chats y personas, oculte identidades o texto, decida qué archivos y notas del equipo van. El manifiesto registra qué se mantuvo, se recortó y se dejó fuera.

## Preparar el extracto del destinatario

1. **Exportaciones → Extracto de entrega**: escriba el propósito, elija chats y un periodo y use **Cargar personas de los chats elegidos** si necesita personas con nombre.
2. El resto: seudónimos, fuera o tal como se registró. Texto y archivos son interruptores separados; teléfonos y correos se pueden enmascarar.
3. Case Board: nada, marcadores y fragmentos, o tarjetas con comentarios. Los nombres del equipo se pueden cambiar por alias.
4. **Descargar extracto de entrega**, ábralo, verifíquelo y revíselo antes de enviarlo.

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
| Personas | Las personas seleccionadas conservan su nombre; las demás reciben seudónimos o quedan fuera. |
| Texto | Todo el texto, solo el de las personas seleccionadas y su cuenta, o nada. |
| Archivos | Archivos de las personas seleccionadas y su cuenta, todos los archivos mostrados o ninguno. |
| Tablero de casos | Nada, marcadores y fragmentos, o tarjetas con debate. |

Lea también el texto y los archivos: un seudónimo no borra los nombres escritos dentro de un mensaje o adjunto. Si falta un archivo seleccionado, restáurelo o deje fuera los adjuntos.

## Asegúrese de que el texto se pueda verificar de forma independiente.

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Quédese usted con el archivo original y los puntos de control. El destinatario puede verificar su copia sin recibir el espacio entero. Diseño: [Report studio](https://phishdestroy.github.io/TgWitness/es/docs/reports/). Referencias de confianza: [verificación de exportaciones](https://phishdestroy.github.io/TgWitness/es/docs/exports/).
