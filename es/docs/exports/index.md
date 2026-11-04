# Exportar y verificar

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/exports/

Entregue archivos que el destinatario puede comprobar por su cuenta frente a su espacio.

Conservar una referenciaExportar archivo ZIP firmadoEl destinatario verifica

¿Nuevo en firmas y puntos de control? [Cambie un registro de ejemplo](https://phishdestroy.github.io/TgWitness/es/docs/concepts/#chain) y vea qué comprobaciones lo detectan.

¿Desea conservar una copia al margen del recopilador? Acceda a [la configuración de S3](https://phishdestroy.github.io/TgWitness/es/docs/exports/#s3), [al bloqueo de objetos](https://phishdestroy.github.io/TgWitness/es/docs/exports/#s3-retention) o a [la recuperación verificada](https://phishdestroy.github.io/TgWitness/es/docs/exports/#s3-restore).

## Conserve una referencia fiable

Apunte la huella de la clave del espacio en algún sitio que no sea el recolector. Mientras recoge, guarde también puntos de control firmados en otro lugar o use un [testigo independiente](https://phishdestroy.github.io/TgWitness/es/docs/witness/). Con eso comprueba el destinatario la clave y un estado anterior del diario.

## Descargue el archivo ZIP firmado

**Exportaciones** → ZIP de evidencia firmado. Contiene el diario entero y un manifiesto de archivos firmado. Dé forma al informe legible en [Report studio](https://phishdestroy.github.io/TgWitness/es/docs/reports/) o envíe solo datos seleccionados como [extracto de entrega](https://phishdestroy.github.io/TgWitness/es/docs/handover/).

Los informes HTML, PDF y JSON llevan sus propios sellos. El CSV es solo una copia de trabajo; para la integridad use el CSV del ZIP verificado.

## Verifíquelo con una copia fiable de TgWitness

En el entorno del proyecto, con su propia huella y sus rutas:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Si pasa, verá `key_pinned: true` y `checkpoint_checked: true`. Guarde esa salida junto al archivo. El punto de control tiene que estar en el final de la exportación o antes.

## Utilizar el resultado de la verificación

- **Archivos:** el manifiesto fija sus hashes y las firmas fijan el diario. Cualquier cambio se nota.
- **Identidad:** la huella que guardó demuestra que es la clave que esperaba.
- **Estado anterior:** un punto de control compara la exportación con un prefijo del diario guardado antes de la entrega.
- **Cobertura:** huecos, resultados de adquisición y una prueba enviar → editar → borrar muestran lo que esta configuración captó de verdad.

Detalles: [qué demuestra la verificación y qué no](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope).

## Configure la copia externa en S3

**Exportaciones → Copia externa** en su espacio. Funciona con AWS S3 y cualquier servicio compatible con S3. Copia segmentos del diario, archivos guardados, puntos de control con sus marcas de tiempo y exportaciones de chats terminadas, cada uno cifrado con `AES-256-GCM` antes de salir del recolector.

La demo en línea muestra estos controles con las subidas desactivadas. Introduzca credenciales reales solo en su propia instalación.

[![Panel completo de copias externas: punto final, región, depósito, claves de acceso, programación, controles de Object Lock y clave de recuperación](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

El panel completo con las opciones avanzadas desplegadas. No se muestran credenciales de almacenamiento.

| Campo | Qué debe introducir |
| --- | --- |
| Punto final | URL del almacenamiento, sin ruta de bucket ni credenciales. Ejemplo: `https://s3.example.invalid`. |
| Región | Lo que pida su proveedor. Por defecto `us-east-1`. |
| Bucket | Un bucket existente en el que pueda escribir. Ejemplo: `example-case-backup`. |
| Carpeta en el repositorio | Prefijo, por defecto `tgwitness`. Se añade encima un prefijo por espacio. |
| ID de clave de acceso / Clave de acceso secreta | Las dos juntas, guardadas en la bóveda. Déjelas vacías más adelante para conservarlas. |
| Direcciones en formato de ruta | Activado: `endpoint/bucket`. Desactivado: `bucket.endpoint`. Depende del proveedor. |
| Intervalo de copia | De 1 a 1440 minutos, por defecto 5. Solo mientras la aplicación está en marcha. |
| Retención de Object Lock | Días y modo, si el bucket admite Object Lock. Cero mantiene el valor por defecto del bucket. |

1. Cree el bucket, rellene destino y credenciales con **Mantener una copia externa** sin marcar y pulse **Guardar copia externa**.
2. **Probar conexión** sube un objeto de prueba cifrado.
3. **Descargar clave de cifrado** y guárdela lejos del recolector. Sin clave no hay recuperación.
4. Marque **Mantener una copia externa**, guarde y luego **Copiar ahora** o deje que funcione la programación.

## Comprobar el estado de la retención y el progreso de la copia

En **Más opciones** elija los días de retención y `GOVERNANCE` o `COMPLIANCE`. TgWitness lee la retención de un objeto subido y le indica: confirmada, ausente o fallo de comprobación.

El panel muestra la última pasada, número de objetos, bytes, límite del diario copiado y errores. Un archivo local que falta se notifica y se reintenta en la siguiente pasada; el resto sigue copiándose.

Las subidas van en directo, por SOCKS5 o por HTTP. Con una ruta solo MTProxy, la copia espera con un error.

## Conserve la clave de recuperación por separado

El JSON de la clave contiene la clave de descifrado, el destino, el prefijo y la huella de la clave. Para recuperar necesita eso más credenciales de almacenamiento con permiso de lectura.

¿Cambió endpoint, bucket o prefijo? Vuelva a descargar la clave. Empieza una copia nueva en el nuevo destino; las exportaciones antiguas se quedan donde estaban.

## Restaurar y verificar en otro equipo

Necesita una instalación de TgWitness de confianza, el JSON de la clave, credenciales de solo lectura y una carpeta vacía:

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

Primero todo se comprueba en una carpeta temporal privada: el diario entero, los puntos de control, los hashes y tamaños de los archivos. Rutas inseguras, segmentos en conflicto o un diario más corto que su punto de control fallan, y entonces no se escribe nada.

Si sale bien, obtiene `events.jsonl`, `media/`, `checkpoints/` y `exports/`. Guarde con ellos la salida JSON del comando y compárelos con los puntos de control o registros del testigo que guarde usted.
