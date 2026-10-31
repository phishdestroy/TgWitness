# Manténgala en funcionamiento

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/server/

Mantenga el colector disponible y sus datos intactos tras cada reinicio.

## Elija un método de puesta en marcha

Para una instalación nativa, utilice el [lanzador](https://phishdestroy.github.io/TgWitness/es/docs/start/) y los ejemplos de servicio que se encuentran en [la carpeta «deploy/».](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Para Docker, instale Docker con Compose y ejecútelo desde el directorio del proyecto:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

El panel predeterminado escucha en la dirección de bucle invertido del servidor, en el puerto 8787. Ábralo localmente o a través de un túnel SSH. Utilice el token del segundo comando para desbloquear el panel.

## Conserve todo el directorio de datos

Las instalaciones nativas utilizan `data/live`. Docker utiliza el volumen persistente `tgwitness-data`. Mantenga juntos los registros, las sesiones de cuenta, las claves y el estado operativo. Una exportación firmada constituye una prueba útil, pero no es una copia de seguridad completa de la instalación.

1. Detenga la recopilación antes de realizar una copia de seguridad completa.
2. Copie todo el directorio de datos privados a un almacenamiento protegido fuera del servidor.
3. Pruebe la restauración en una instalación aislada antes de confiar en la copia de seguridad.

## Compruébelo tras reiniciar el sistema.

Confirme el espacio de trabajo y la clave previstos, la conexión a Telegram, las fuentes seleccionadas y la captura de nuevos mensajes. El estado guardado de MTProto y la función de recuperación permiten recuperar las actualizaciones que Telegram aún conserva. No es posible reconstruir todas las actualizaciones caducadas ni las modificaciones eliminadas antes de la captura.

El estado del contenedor indica que el servidor web responde. Utilice un mensaje controlado y una comprobación de validación para evaluar la recopilación y la publicación externa.

## Publique únicamente lo que tenga intención de publicar

La guía de implementación incluye ejemplos de HTTPS, comandos de volumen persistente, actualizaciones y pasos para la restauración. Se proporcionan comandos de Docker para la implementación; el [registro de validación](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/) actual identifica los entornos en los que se han realizado pruebas.
