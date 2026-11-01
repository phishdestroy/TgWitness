# Webhooks salientes

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/webhooks/

Envía eventos específicos a receptores HTTPS con firmas HMAC, reintentos y estado de entrega.

[Guía de flujo de trabajo](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Abre **Integraciones → Webhooks salientes** en el espacio de trabajo seleccionado. Añade un receptor HTTPS, elige eventos de recopilación/multimedia/exportación y, opcionalmente, selecciona chats para nuevas observaciones y cambios. El texto de los mensajes está desactivado por defecto. Al habilitar los extractos, se añaden como máximo 1.000 caracteres a los eventos de cambio de mensaje; los campos sin procesar de Telegram y las credenciales nunca se envían.

Copia la clave secreta HMAC una sola vez en la configuración protegida del receptor. Está cifrada en la bóveda de TgWitness y no se puede recuperar desde el panel. Elimina y vuelve a crear un destino para rotarlo. **Envía** a las colas **de prueba sintéticas** una prueba sin contenido de chat; actualiza el estado de entrega para ver el resultado.

La entrega amplía el ciclo de notificaciones existente junto con Apprise. Utiliza la ruta externa del espacio de trabajo y las restricciones de destino privado existentes. No hay ningún plan de contingencia directo ni redireccionamiento posterior. Las URL no deben contener credenciales, cadenas de consulta ni fragmentos; las direcciones privadas requieren la aceptación a nivel de servidor, no una configuración que un usuario del panel pueda eludir.

## Carga útil y firma

Esquema: [`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json). Cada carga útil contiene `event_id`, `timestamp`, `workspace`, `type`, `synthetic` y contadores. Los eventos basados en el registro incluyen su secuencia y su hash. La finalización de la exportación completa y las pruebas sintéticas son eventos de entrega, sin ninguna referencia inventada al registro firmado. Los avisos de eliminación de Telegram y `missing_on_recheck` siguen siendo tipos distintos.

El encabezado `X-TgWitness-Signature` es `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`. Calcula el HMAC sobre los bytes exactos `timestamp + "." + raw_request_body`, utilizando el secreto mostrado como bytes UTF-8. Compara las firmas en tiempo constante antes de analizar o procesar el cuerpo del mensaje. Rechaza las marcas de tiempo que se desvíen más de cinco minutos de tu reloj. La marca de tiempo se actualiza en cada intento de entrega.

Utiliza `event_id` como clave de idempotencia en un almacenamiento duradero, con una restricción atómica de unicidad antes de los efectos secundarios. Una firma válida por sí sola no impide que se repita una solicitud reciente. Conserva los ID procesados al menos durante toda la ventana de reintentos; consérvalos durante más tiempo si el receptor puede volver a procesar los eventos almacenados.

## Reintentos

Las entregas se ponen en cola de forma permanente antes de las solicitudes HTTP. Utilizan la semántica «al menos una vez»: una confirmación perdida o un reinicio pueden provocar que un evento se entregue de nuevo con el mismo ID. Hay ocho intentos con retroceso exponencial, que comienzan en 15 segundos y tienen un límite máximo de una hora. Para que se considere un éxito, se requiere una respuesta 2xx. Las tareas agotadas dejan un error visible; no se garantiza la entrega una vez finalizados los reintentos.

La cola tiene capacidad para 1.000 envíos. Cuando se llena, el escaneo de los eventos del registro se detiene y se reanuda cuando hay espacio disponible. La finalización de una exportación completa que no se pueda poner en cola genera un error de cola visible. Se intentan hasta cinco envíos por cada ciclo de notificación y se conservan los últimos 100 registros de intentos. Al eliminar un destino también se eliminan sus envíos pendientes.

## Ejemplo de n8n

Importa [el flujo de trabajo de ejemplo](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json). Está inactivo y no contiene información confidencial ni acciones posteriores. Configura `TGWITNESS_WEBHOOK_SECRET` en el entorno del trabajador de n8n, permite el acceso a ese entorno y habilita la función integrada `crypto` para el nodo Code. El ejemplo utiliza la opción «raw-body» del nodo Webhook, comprueba la firma y la vigencia, y confirma los eventos validados. Esto se ajusta a la [implementación documentada](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts) del nodo.

Antes de añadir entradas o notificaciones de SIEM, incorpora un almacenamiento idempotente y duradero claveado mediante `event_id`. Restringe la edición de flujos de trabajo de n8n y la retención de registros de ejecución de acuerdo con los datos que hayas elegido enviar. TgWitness no añade comandos entrantes.
