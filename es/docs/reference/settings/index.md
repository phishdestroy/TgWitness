# Primera configuración y ajustes

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/settings/

El asistente de configuración, los objetivos, los niveles de interfaz, las rutas de conexión y los ajustes compartidos por un grupo de cuentas.

[Cuentas](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/) · [Conexión](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/) · [Acceso](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/)

Se abre un nuevo espacio de trabajo `/first-run`: idioma y hora, nivel de interfaz, objetivo, conexión, Telegram y chats. Cada respuesta se guarda en el servidor tan pronto como cambia, por lo que al recargar la página se continúa en el mismo paso. La última pantalla muestra una lista de las respuestas y te permite volver a cualquiera de ellas.

El idioma, la zona horaria de la IANA, el tema y el nivel se almacenan por operador y por espacio de trabajo. Los valores predeterminados son el idioma del navegador, la zona horaria del dispositivo, el tema del sistema y la interfaz sencilla. Al cambiar el idioma, se mantiene la sesión del panel. Las horas que aparecen en el registro firmado nunca cambian.

`/settings` Edita los mismos registros que el asistente. La búsqueda abarca los campos principales, los parámetros y los formularios ampliados; se puede abrir un campo oculto sin cambiar el nivel. Los niveles solo modifican lo que se muestra: el servidor comprueba los permisos por sí mismo. La configuración de la colección y la primera conexión son competencia del administrador del espacio de trabajo.

| Nivel | Campos | Barra lateral |
| --- | --- | --- |
| Sencillo | Solo lo imprescindible | Inicio, Chats, Cambios, Archivos, Ajustes |
| Estándar | Configuraciones comunes con explicaciones | Se añaden Case Board, Cuentas y Acceso |
| Experto | Todos los campos, límites y detalles técnicos | Añade «Fuentes», «Extras», «Preguntar al archivo», «Parámetros», «Cuenta», «Registro del sistema» e «Integraciones». |

[La guía de paneles](https://phishdestroy.github.io/TgWitness/es/docs/reference/panel/) describe cada sección.

## Objetivos

| Objetivo | Colección | Archivos | Servicios externos | Dirección del servidor |
| --- | --- | --- | --- | --- |
| Copia de archivo | Desactivado; **«Start»** ejecuta una exportación | Fotos de hasta 20 MB | Desactivado | Automático |
| Seguir chats | Continuo | Fotos y vídeos de hasta 60 segundos / 20 MB | Marcas de tiempo y notificaciones de problemas | Automático |
| Pruebas | Continuo | Todos los archivos de hasta 1 GB | Marcas de tiempo, drand, notificaciones | No, ocultarlo |

Se recomienda utilizar la copia externa, el bot «witness» y la comprobación de código como pruebas. Las direcciones de almacenamiento y notificación necesitan primero un destino. Una función que se comunica con un servicio externo solicita permiso para permitir solicitudes fuera de Telegram; al desactivarla, se ofrece la opción de desactivar también las marcas de tiempo, las notificaciones y la copia externa.

Al modificar el objetivo, se muestra primero la diferencia, y los cambios manuales se pueden conservar. Un campo que difiera del objetivo se marca **como «Modificado por ti»** y se puede restaurar. La revisión de la configuración evita que una diferencia revisada se aplique sobre un cambio realizado en otra pestaña.

## Conexión

**Automatic** prueba primero los servidores públicos MTProxy, luego WARP y, por último, una conexión directa, esta última solo cuando se pueda mostrar la dirección del servidor. Automatic y WARP pueden instalar componentes con verificación de hash y registrar el servidor en Cloudflare. WARP utiliza el gestor wgcf/wireproxy existente y un puerto SOCKS5 local; la tabla de enrutamiento del sistema no se modifica. Cuando se necesitan servicios externos, Automatic da prioridad a WARP frente a MTProxy.

Tu propio proxy acepta `tg://proxy`, `socks5://`, `http://` y `https://`. El certificado de un proxy HTTPS se comprueba antes de enviarle las credenciales.

Una comprobación de conexión tiene una validez de cinco minutos y está vinculada a la ruta, la política y las respuestas del asistente; si se modifica cualquiera de estos elementos, es necesario realizar una nueva comprobación. Existe la opción de **«Continuar sin comprobar»**, que no sustituye al inicio de sesión en Telegram. La ruta elegida se vuelve a comprobar en segundo plano, y «Automático» vuelve a ejecutar su cadena tras una pérdida de conexión. Cuando ningún proxy público responde, el contador se vuelve rojo y se activan las acciones de WARP y recomprobación.

## Grupos de cuentas

Las cuentas de un grupo comparten su configuración. Abre **Cuentas → Grupos y configuración compartida → Configuración compartida**, o **Configuración del grupo** en la página de configuración de una cuenta.

El grupo comparte el objetivo, los archivos guardados, las marcas de tiempo, el drand, las notificaciones de problemas, la copia externa, las solicitudes fuera de Telegram, el modo IP, qué registrar, el calendario de revisiones, las reglas de notificación, la configuración de informes, los parámetros y la ruta de conexión. Los destinos de las notificaciones, las credenciales del proxy y el inicio de sesión son específicos de cada cuenta, al igual que el inicio y la pausa de la recopilación.

- Todos los miembros siguen el grupo. En «Configuración» se establece un valor 🔗 **del grupo** o ✏️ **un valor propio**; al seleccionar **«Volver al valor del grupo»** se restablece el valor original.
- Un cambio enumera las cuentas a las que afecta (**se aplica a 2 de 3 cuentas**) y pregunta por cuenta antes de sustituir un valor propio. Las cuentas sin marcar conservan el suyo.
- Un parámetro que el grupo no comparte permanece en **«No compartido»: cada cuenta conserva su propio valor** hasta que pulses **«Compartir este valor**».
- **Al copiar la configuración de una cuenta,** los valores de la cuenta seleccionada pasan a ser los del grupo.
- A una cuenta que se traslada a un grupo se le pregunta: **«¿Aplicar los valores del grupo?».** De lo contrario, conserva sus propios valores, marcados con ✏️. Las cuentas añadidas posteriormente comienzan con los valores del grupo.
- Una cuenta de observación mantiene su modo IP hasta que se pone en pausa.

Cada cambio queda registrado en el diario firmado del espacio de trabajo principal y de cada miembro al que llega. Al eliminar un grupo, se conservan sus cuentas y sus valores actuales.

La página del grupo `/groups/<id>` muestra a los miembros, lo que requiere atención y los chats que ven varias cuentas. Véase [«Grupos de cuentas](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#bulk-import-and-account-groups)».

## Espacios de trabajo existentes

Un espacio de trabajo con una sesión o una configuración anterior ya completada no muestra el asistente. Sus valores no se sustituyen por un objetivo cuando se carga la página. Ocultar un campo no desactiva la función ni elimina su valor.

La estimación de tamaño y tiempo se basa en hasta tres chats seleccionados y hasta 20 mensajes de cada uno. Se trata de una estimación: no tiene en cuenta los límites de Telegram, la velocidad de un servidor concreto ni los archivos de cada chat.

```
python tools/test_settings_hub.py
python tools/test_group_settings.py
python tools/check_group_settings_browser.py
python tools/check_first_run.py
```
