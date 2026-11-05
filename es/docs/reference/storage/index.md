# Almacenamiento y recuperación

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/storage/

Copias de seguridad, traslado de archivos antiguos a tu nube, copias bajo Object Lock y recuperación en un nuevo equipo.

El panel distingue tres tareas:

| Tarea | Qué hace |
| --- | --- |
| Haz una copia de seguridad | Copia el registro firmado, los puntos de control, los archivos conservados y las exportaciones en cola al destino S3 configurado. |
| Espacio local gratuito | Copia los archivos adjuntos antiguos seleccionados a S3 o a un servidor remoto en la nube de rclone, vuelve a leerlos íntegramente, verifica los bytes cifrados y, a continuación, elimina la copia local verificada. |
| Conserva una copia como prueba | Configura S3 Object Lock y comprueba el estado de retención devuelto. El servicio debe confirmar el modo y la fecha solicitados. |

Al liberar espacio nunca se borra ni se sobrescribe el registro firmado. Cada archivo adjunto conserva su SHA-256 original y un recibo de recuperación. La compresión gzip opcional se lleva a cabo antes del cifrado autenticado. Los nombres de los archivos en la nube no contienen nombres de Telegram, ID de chat ni nombres originales de los archivos adjuntos. Un archivo adjunto puede tener un tamaño de hasta 32 GiB.

Una respuesta de subida por sí sola no supone permiso para eliminar un archivo. TgWitness descarga el objeto cifrado completo y verifica su tamaño; SHA-256 guarda el recibo y, a continuación, vuelve a comprobar los bytes locales inmediatamente antes de la eliminación. Un error en la subida, una lectura diferente o una transferencia cancelada hacen que el archivo local permanezca en su sitio. Si una copia de seguridad de pruebas habilitada aún no ha copiado ese archivo, la eliminación también espera a que lo haga.

## Cuando el disco se está llenando

La descarga de adjuntos se pausa por debajo del espacio indicado en **Parámetros → Adjuntos → espacio libre en disco** (1 GiB por defecto), conservando la cola. Las observaciones de texto continúan. Esto es independiente de las notificaciones: desactivarlas no elimina la reserva de descarga ni las protecciones del almacenamiento.

Para intervenir antes, activa **Ejecutar automáticamente**, elige **Eliminar el archivo local para liberar espacio** y activa **Iniciar una descarga adicional al almacenamiento externo cuando quede poco espacio**. Por defecto, esta regla opcional se inicia con menos de 5120 MiB libres y continúa por lotes hasta alcanzar 10240 MiB. Ambos umbrales son configurables. Usa el mismo destino, antigüedad mínima, límite de lote, verificación mediante lectura completa y requisitos de copia de seguridad de pruebas que una ejecución manual. Nunca habilita un destino por sí sola. Comprueba el espacio cada 30 segundos; un error o la falta de progreso retrasa el siguiente intento cinco minutos. El estado y la hora del reintento sobreviven a los reinicios. Cuando la regla está inactiva, las ejecuciones programadas mantienen su intervalo normal.

El panel muestra el espacio libre, la reserva de empaquetado, si la regla está preparada y los archivos omitidos por falta de espacio temporal. El empaquetado y la restauración comprueban su necesidad máxima de espacio temporal antes de empezar y el espacio disponible durante la escritura. La reserva es la configurada para descargas, con un mínimo de 64 MiB para operaciones de almacenamiento. No es una cuota del sistema de archivos: otro proceso puede consumir espacio entre comprobaciones.

La compresión Gzip es sin pérdida y se aplica a objetos remotos; no reduce el diario activo ni crea archivos comprimidos locales. Los JPEG, vídeos y ZIP pueden reducirse muy poco o crecer ligeramente. Con compresión, el empaquetado puede necesitar temporalmente aproximadamente el doble del tamaño del adjunto más la reserva. Elige un umbral suficientemente temprano para los archivos más grandes. Los archivos demasiado grandes se conservan y se notifican; los menores y las copias remotas ya verificadas aún pueden liberar espacio. Una copia verificada permite retirar el archivo local sin crear otro archivo de empaquetado. La restauración también necesita espacio temporal y puede rechazarse hasta que esté disponible.

Si no hay archivos aptos para trasladar o no se ha configurado un destino, TgWitness no puede recuperar espacio automáticamente. La gestión del almacenamiento nunca recorta ni reescribe el diario firmado. Este sigue necesitando espacio para nuevas observaciones de texto.

## Conectar un destino

En **Extras → Almacenamiento y espacio en disco → Gestionar almacenamiento**, elige la tarea y el destino, guárdala y, a continuación, selecciona **Probar subida y descarga**. La prueba sube una pequeña prueba aleatoria y la lee de nuevo. No utiliza contenido de Telegram.

Para S3, utiliza el punto final, la región y el bucket reales del proveedor. Wasabi, Backblaze, Cloudflare R2 y otros servicios compatibles utilizan la misma configuración de S3. El hecho de que una API sea compatible no implica por sí solo que admita Object Lock. El modo «Governance» puede permitir que un administrador autorizado eluda la retención; el modo «Compliance» tiene diferentes restricciones. Consulta el estado de Object Lock devuelto antes de basarte en la retención.

Para un destino de rclone, crea un remoto utilizando la configuración del proveedor de rclone y pega la sección `[name]` en el panel. El asistente instalado es compatible con MEGA, Google Drive, OneDrive, Dropbox, Box, pCloud y los demás proveedores que aparecen en el selector. Las credenciales se guardan en la caja fuerte cifrada de este espacio de trabajo. Las actualizaciones de OAuth se guardan de nuevo en la caja fuerte. Las credenciales no se añaden a los eventos del registro ni se incluyen en las descargas de recuperación.

El ayudante se instala dentro del espacio de trabajo, con una versión anclada y SHA-256. No se añade a la ruta PATH del sistema. Los archivos de configuración y los archivos de trabajo son archivos temporales dentro de ese espacio de trabajo. Se rechazan los remotos basados en comandos y en archivos locales. Actualmente, rclone requiere una ruta **Direct** seleccionada explícitamente para las solicitudes externas. Utiliza el almacenamiento S3 nativo para una ruta SOCKS5 o HTTP del espacio de trabajo; rclone no omite silenciosamente una ruta no disponible.

## Guarda el archivo de recuperación

Selecciona **«Guardar archivo de recuperación»** después de copiar los archivos y guárdalo en un lugar distinto al de la instalación. Contiene la clave de descifrado y los recibos firmados de los objetos, por lo que debes tratarlo como una copia de seguridad de la clave privada. Guarda también por separado la configuración remota original y las credenciales de destino. Un archivo de recuperación creado antes de una copia posterior no contiene el recibo de ese archivo posterior.

La huella digital de la clave de firma ya debería estar registrada por separado. Una firma que solo se compruebe con la clave proporcionada en el mismo archivo no permite determinar de quién es el archivo de recuperación.

Para recuperar los recibos de almacenamiento que faltan en un espacio de trabajo existente, abre **«Recuperar archivos desde un archivo de recuperación guardado**» y selecciona el archivo. El panel comprueba la firma y requiere la misma clave de firma del espacio de trabajo. No permite sustituir una clave de almacenamiento diferente. A continuación, selecciona **«Restaurar todos los archivos**». La restauración pausa la regla de almacenamiento automático para que la siguiente ejecución programada no pueda volver a eliminar inmediatamente los archivos restaurados. Vuelve a activar la regla cuando hayas terminado con las copias locales.

La restauración verifica el texto cifrado, autentica el descifrado, descomprime si es necesario y comprueba el texto en claro original SHA-256 antes de colocar un archivo en `media/`. Un objeto remoto dañado nunca sustituye a un archivo local. Un archivo local existente con bytes diferentes se conserva para su revisión en lugar de sobrescribirse.

## Recuperación tras la pérdida de la instalación

Instala TgWitness en otro equipo. Utiliza el archivo de recuperación privado, la huella digital registrada por separado y las credenciales de destino originales:

```
python -m tgwitness.storage recover \
  --recovery storage-recovery.json \
  --fingerprint TRUSTED_WORKSPACE_SHA256 \
  --credentials original-rclone.conf \
  --output recovered-attachments
```

Para S3, `--credentials` apunta a un archivo JSON privado con `access_key` y `secret_key`; el archivo de recuperación firmado proporciona la configuración de destino. El comando utiliza una conexión externa directa y descarga el programa auxiliar anclado cuando un remoto de rclone lo necesita. Rechaza un directorio de salida ya existente.

Los bytes originales recuperados se escriben en `recovered-attachments/media/`, con el nombre de su SHA-256. `recovery-log.jsonl` es un registro sin firmar de las operaciones de recuperación. El comando no recrea un diario firmado perdido ni su clave de firma. Mantén una copia de seguridad completa del espacio de trabajo para esos casos. Un archivo de recuperación de almacenamiento no es una copia de seguridad completa del espacio de trabajo .

## Bot de operador y notificaciones de finalización

El bot de Telegram pertenece al operador. Créalo a través de BotFather y configure su token, el chat de destino y los ID de usuario de Telegram explícitamente permitidos en el panel. Tanto el remitente como el chat deben coincidir. Se ignoran los mensajes reenviados y los comandos procedentes de otros bots.

`/status` y `/stats` están disponibles en el modo predeterminado «solo estado». El modo de control opcional añade `/pause`, `/resume` y `/copy`. `/copy` solicita la tarea de almacenamiento configurada; esto no significa que la subida remota ya haya finalizado. Los comandos no pueden proporcionar URL, archivos o programas de shell arbitrarios.

Utiliza los ajustes de notificación independientes para las alertas y la finalización de tareas. Los avisos de finalización distinguen una exportación de cuenta con lagunas de una exportación completa, y muestran el historial y el recuento de almacenamiento. Los extractos de mensajes no se incluyen a menos que se active por separado en los ajustes de notificación. El selector de servicios se genera a partir del catálogo real de Apprise instalado, en lugar de un conjunto fijo de ejemplos de proveedores.
