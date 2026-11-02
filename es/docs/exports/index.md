# Exportar y verificar

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/exports/

Proporcione a los destinatarios archivos que puedan cotejar con el espacio de trabajo de recopilación y su historial guardado.

Conservar una referenciaExportar archivo ZIP firmadoEl destinatario verifica

¿Es nuevo en el tema de las firmas y los puntos de control? [Modifique un registro de ejemplo](https://phishdestroy.github.io/TgWitness/es/docs/concepts/#chain) y compruebe qué comprobaciones lo detectan.

¿Desea conservar una copia al margen del recopilador? Acceda a [la configuración de S3](https://phishdestroy.github.io/TgWitness/es/docs/exports/#s3), [al bloqueo de objetos](https://phishdestroy.github.io/TgWitness/es/docs/exports/#s3-retention) o a [la recuperación verificada](https://phishdestroy.github.io/TgWitness/es/docs/exports/#s3-restore).

## Conserve una referencia fiable

Guarde la huella digital de la clave pública del espacio de trabajo fuera del recopilador. Durante la recopilación, conserve los puntos de control firmados en otro lugar o utilice un [testigo independiente](https://phishdestroy.github.io/TgWitness/es/docs/witness/). Estas referencias permiten al destinatario verificar la clave y el límite de un registro anterior.

## Descargue el archivo ZIP firmado

Abra **«Exportaciones»** y cree un archivo ZIP de pruebas firmado. Este incluye el registro completo del espacio de trabajo y un manifiesto de archivos firmado. Utilice [«Report Studio»](https://phishdestroy.github.io/TgWitness/es/docs/reports/) para dar forma a un informe legible, o un [extracto de entrega](https://phishdestroy.github.io/TgWitness/es/docs/handover/) para proporcionar únicamente datos seleccionados y minimizados.

Los informes en formato HTML, PDF y JSON llevan sus propios sellos firmados y pueden verificarse por separado. El archivo CSV es una copia práctica para el análisis; utiliza el archivo CSV exacto que se encuentra dentro del ZIP verificado para comprobar su integridad. Conserva el ZIP firmado cuando el destinatario también necesite los registros originales y los archivos adjuntos.

## Verifíquelo con una copia fiable de TgWitness

En el entorno del proyecto instalado, sustituya la huella digital de ejemplo y las rutas de los archivos:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Cuando ambas referencias superan la comprobación, el resultado indica «`key_pinned: true`» y «`checkpoint_checked: true`». Conserve el resultado de la verificación junto con el archivo original. El punto de control conservado debe situarse en el límite de la exportación o antes de este.

## Utilizar el resultado de la verificación

- **Comprueba los archivos entregados:** el manifiesto vincula sus hash, y las firmas de los registros vinculan el diario guardado. Se detecta cualquier archivo modificado o cadena de registros rota.
- **Comprueba la identidad del espacio de trabajo:** la huella digital conservada de forma independiente identifica la clave de firma que esperabas.
- **Compara un límite anterior:** un punto de control conservado compara la exportación con un prefijo de registro guardado antes del traspaso.
- **Revisa la cobertura de la recopilación:** las lagunas, los resultados de la adquisición y una prueba controlada de «enviar → editar → eliminar» describen los eventos que ha capturado esta configuración.

Conserve estos resultados en la copia del destinatario. Consulte [lo que establece la verificación](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope) en cuanto al alcance de los controles y la evaluación independiente de las afirmaciones de las fuentes y la cobertura de la recopilación.

## Configure la copia externa en S3

En su espacio de trabajo activo, abra **«Exportaciones» → «Copia externa**». Esta función opcional es compatible con AWS S3 y otros servicios compatibles con S3. Copia segmentos del registro, fotos y archivos conservados, puntos de control con sus respuestas de marca de tiempo y exportaciones de chats completadas. Todos los objetos se cifran en el colector con `AES-256-GCM` antes de su carga.

La demostración en línea muestra los mismos controles con la función de carga desactivada. Introduzca las credenciales de almacenamiento únicamente en su propio espacio de trabajo en ejecución.

[![Panel completo de copias externas: punto final, región, depósito, claves de acceso, programación, controles de Object Lock y clave de recuperación](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

El panel completo con las opciones avanzadas desplegadas. No se muestran credenciales de almacenamiento.

| Campo | Qué debe introducir |
| --- | --- |
| Punto final | La URL del servicio de almacenamiento, sin ruta de bucket ni credenciales. Ejemplo ficticio: `https://s3.example.invalid`. |
| Región | La región requerida por su proveedor. El valor predeterminado de la aplicación es `us-east-1`. |
| Bucket | Un repositorio ya existente al que puede acceder. Ejemplo ficticio: `example-case-backup`. |
| Carpeta en el repositorio | El prefijo del objeto; por defecto, `tgwitness`. La aplicación añade un prefijo derivado de la huella digital de la clave de firma de este espacio de trabajo. |
| ID de clave de acceso / Clave de acceso secreta | Introduzca ambas credenciales de almacenamiento a la vez. Se guardarán en el almacén del espacio de trabajo. Déjelas ambas en blanco en los siguientes guardados para conservar el par guardado. |
| Direcciones en formato de ruta | Utilice «`endpoint/bucket`» cuando esté habilitado, o «`bucket.endpoint`» cuando esté deshabilitado, según el proveedor. |
| Intervalo de copia | De 1 a 1.440 minutos; por defecto, 5 minutos. La aplicación debe estar en ejecución para que se realicen las copias programadas. |
| Retención de Object Lock | Días de retención y modo para un depósito compatible con Object Lock. El valor «cero días» mantiene vigente la retención predeterminada del depósito. |

1. Crea el bucket con tu proveedor y, a continuación, introduce su destino y tus credenciales. Deja sin marcar la opción **«Guardar una copia externa**» mientras realizas los preparativos y, después, selecciona **«Guardar copia externa**».
2. Seleccione **«Probar conexión**». Esto carga un objeto de prueba cifrado y comprueba la respuesta del almacenamiento.
3. Seleccione **«Descargar clave de cifrado**». Guarde ese archivo por separado del recopilador; es necesario para la recuperación.
4. Marque la casilla **«Conservar una copia externa»** y guarde de nuevo. Seleccione **«Copiar ahora»** para realizar una copia manual, o deje que la programación siga su curso.

## Comprobar el estado de la retención y el progreso de la copia

En **«Más opciones**», selecciona los días de retención y «`GOVERNANCE`» o «`COMPLIANCE`» cuando tu depósito admita Object Lock. TgWitness lee el modo de retención y la fecha límite de un objeto cargado. Revisa el resultado de retención por separado: confirmado, retención ausente o comprobación fallida.

El panel informa de la última pasada, el recuento de objetos, los bytes transferidos, el límite del registro copiado y cualquier error. Se notifica la ausencia o modificación de un soporte local y se vuelve a intentar en la siguiente pasada. Los archivos, puntos de control y exportaciones en cola posteriores a dicho soporte aún pueden copiarse.

Las subidas utilizan la ruta Direct, SOCKS5 o HTTP del espacio de trabajo. Elige una de estas rutas para la copia a S3; una ruta exclusiva de MTProxy deja la copia pendiente con un error.

## Conserve la clave de recuperación por separado

El archivo JSON descargado contiene la clave de descifrado, la configuración de destino, el prefijo del objeto del espacio de trabajo y la huella digital de la clave de firma. La recuperación requiere tanto este archivo de clave como unas credenciales de almacenamiento independientes con acceso de lectura al depósito. Inclúyelas en tu plan de recuperación.

Si cambia el punto final, el depósito o el prefijo de la carpeta, descargue de nuevo el archivo de clave para que la configuración de destino coincida. La aplicación inicia una nueva copia del registro, los archivos y los puntos de control conservados localmente en el nuevo destino. Las exportaciones de chats finalizadas que ya se hayan eliminado de la cola de subida local permanecerán en su destino anterior.

## Restaurar y verificar en otro equipo

Utilice una instalación fiable de TgWitness, el archivo JSON de la clave descargado, credenciales de almacenamiento con acceso de lectura y un directorio de salida vacío. Sustituya los marcadores de posición ficticios de las credenciales que aparecen a continuación.

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

Las descargas y los objetos descifrados permanecen en un almacenamiento temporal privado mientras se comprueban el registro completo, los puntos de control conservados y los hash y tamaños de los archivos multimedia preservados. Se rechazan las rutas inseguras, los segmentos del registro conflictivos y los registros más cortos que su punto de control. Si la verificación falla, no se publican archivos restaurados.

Si la recuperación se realiza con éxito, se obtienen los valores `events.jsonl`, `media/`, `checkpoints/` y `exports/` para el material disponible en la copia. Conserve el resultado JSON del comando junto con el material recuperado.

Compara el material recuperado con tus puntos de control o registros de testigos conservados de forma independiente y, a continuación, revisa la cobertura de la recopilación registrada para el periodo que necesites.
