# Averigüe qué ha fallado

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/troubleshooting/

Comience por el síntoma. Compruebe una capa cada vez.

## El panel solicita un token

Utilice el token del panel que aparece en el archivo local mostrado por el lanzador. Para Docker, ejecute «`docker compose exec tgwitness cat /data/panel-token.txt`». Un código de inicio de sesión de Telegram, un token de BotFather y un token de testigo de solo lectura tienen fines distintos.

## Telegram no se conecta

Abra la configuración de conexión y ejecute la comprobación de conexión. Si utiliza un proxy público, pruebe otra entrada y guarde la ruta de forma explícita. Compruebe el tipo de proxy y el formato de clave admitido. Actualizar una lista pública no cambia la ruta de la cuenta.

## Conectado, pero no hay mensajes nuevos

1. Compruebe que la observación se esté ejecutando en el espacio de trabajo correcto.
2. Confirme que la fuente esté seleccionada y sea visible para dicha cuenta.
3. Envíe un mensaje nuevo y único en un grupo controlado y busque ese texto exacto.
4. Revise el registro operativo para detectar interrupciones, retrasos en el trabajo o errores de Telegram.

Las instantáneas históricas y los eventos de mensajes nuevos son distintos. Se puede conectar una fuente inactiva sin que se generen mensajes nuevos. Utilice una prueba de entrega controlada cuando sea importante que la información esté completa.

## FloodWait o un lapso tras un reinicio

«FloodWait» significa que Telegram requiere una pausa. Espere el periodo indicado y revise la carga de trabajo de la recopilación; las reconexiones repetidas no eliminan el límite. El estado de actualización guardado ayuda a ponerse al día tras un reinicio, pero las actualizaciones caducadas y algunas ventanas de interrupción siguen siendo limitaciones. Registre el intervalo en lugar de considerar el registro como completo.

## El bot está configurado, pero no publica nada.

Asegúrese de que el proceso de «witness» se esté ejecutando correctamente, de que el bot pueda publicar en el canal y de que el «witness» pueda comunicarse con el colector y la API del bot. Revise su registro en busca de publicaciones fallidas. Una consulta exitosa al colector por sí sola no confirma la publicación en el canal.

## ¿Dónde se encuentra la integración del token de GitHub?

**En fase de planificación.** La sección «Extras» describe el flujo de trabajo propuesto para la bifurcación y la verificación de la compilación. Actualmente no existe ningún formulario de token de GitHub ni ninguna certificación automatizada que confirme que una instalación en funcionamiento coincide con un repositorio. Consulte el [estado actual de las funcionalidades](https://phishdestroy.github.io/TgWitness/es/docs/reference/features/).

Al informar de un problema, incluya la versión, el sistema operativo, los pasos seguidos y el mensaje de error censurado. No mencione en los tickets públicos las sesiones, los tokens, los mensajes privados ni el directorio de datos.
