# Averigüe qué ha fallado

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/troubleshooting/

Empiece por el síntoma y compruebe una cosa cada vez.

## El panel solicita un token

Pide el token del panel del archivo que indicó el lanzador. Docker: `docker compose exec tgwitness cat /data/panel-token.txt`. No es un código de Telegram, ni el token de un bot, ni el del testigo.

## Telegram no se conecta

Ejecute la comprobación de conexión. Con un proxy público, elija otro y guarde. Revise el tipo de proxy y el formato del secreto. Actualizar las listas no cambia la ruta por sí solo.

## Conectado, pero no hay mensajes nuevos

1. ¿Está la observación en marcha, en el espacio correcto?
2. ¿Está la fuente seleccionada y es visible para esa cuenta?
3. Envíe un mensaje único a su grupo de prueba y búsquelo.
4. Busque interrupciones o errores de Telegram en el diario.

Un chat tranquilo simplemente no tiene nada nuevo. Si importa la integridad, haga una prueba de entrega controlada.

## FloodWait o un lapso tras un reinicio

FloodWait es Telegram diciendo «más despacio». Espere a que pase y baje la carga; reconectar no ayuda. Tras un reinicio, TgWitness recupera lo que Telegram aún tiene; el resto es un hueco, así que anótelo.

## El bot está configurado, pero no publica nada.

¿Está el testigo en marcha, puede el bot publicar en el canal, llega al recolector y al Bot API? Busque publicaciones fallidas en su diario. Una consulta en el lado del recolector no significa que se publicara.

## ¿Dónde se encuentra la integración del token de GitHub?

**En fase de planificación.** La sección «Extras» describe el flujo de trabajo propuesto para la bifurcación y la verificación de la compilación. Actualmente no existe ningún formulario de token de GitHub ni ninguna certificación automatizada que confirme que una instalación en funcionamiento coincide con un repositorio. Consulte el [estado actual de las funcionalidades](https://phishdestroy.github.io/TgWitness/es/docs/reference/features/).

¿Informa de un error? Versión, sistema, pasos y un error sin datos personales. Nunca ponga sesiones, tokens, mensajes privados ni el directorio de datos en un issue público.
