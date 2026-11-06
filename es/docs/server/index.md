# Telegram · Manténgala en funcionamiento

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/server/

Mantenga el recolector en marcha y los datos a salvo en los reinicios.

## Elija un método de puesta en marcha

Nativo: el [lanzador](https://phishdestroy.github.io/TgWitness/es/docs/start/) más las plantillas de servicio en [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker, desde la carpeta del proyecto:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

El panel escucha en localhost:8787. Ábralo en local o por un túnel SSH, con el token del segundo comando.

## Conserve todo el directorio de datos

Nativo: `data/live`. Docker: el volumen `tgwitness-data`. Diarios, sesiones y claves van juntos. Una exportación firmada es evidencia, no una copia de seguridad.

1. Detenga primero la recogida.
2. Copie el directorio de datos entero a un lugar seguro, fuera del host.
3. Pruebe a restaurarlo en una instalación aparte antes de fiarse.

## Compruébelo tras reiniciar el sistema.

Compruebe el espacio y la clave, la conexión, las fuentes y que entran mensajes nuevos. TgWitness recupera lo que Telegram todavía guarda, no todo lo que pasó mientras estaba parado.

Contenedor «sano» significa que el servidor web responde. Si la recogida funciona se lo dirán un mensaje de prueba y el testigo.

## Publique únicamente lo que tenga intención de publicar

HTTPS, volúmenes, actualizaciones y restauración están en la referencia de despliegue. Lo que se ha probado de verdad: [registro de validación](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/).
