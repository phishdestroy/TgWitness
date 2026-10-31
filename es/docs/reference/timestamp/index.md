# Marcas de tiempo

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/timestamp/

Marcas de tiempo RFC 3161 para puntos de control firmados: qué se envía a la autoridad y cómo se verifica la respuesta.

TgWitness prepara solicitudes conforme a la norma RFC 3161 y verifica las respuestas de la autoridad de sellado de tiempo (TSA). Este procedimiento manual no selecciona una TSA ni envía datos; el modo de pruebas realiza ambas acciones según una programación ([formato de pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)). Una solicitud preparada **aún no** constituye **una prueba de sellado de tiempo**.

## Lo que la prueba acredita

Diagrama de flujo · Observaciones sobre la cuenta → Cadena SHA-256 y firmas Ed25519; Cadena SHA-256 y firmas Ed25519 → Punto de control firmado; Punto de control firmado → Hash de bytes exactos y nonce aleatorio; Hash de bytes exactos y nonce aleatorio → Solicitud RFC 3161; Solicitud RFC 3161 → TSA independiente; TSA independiente → Respuesta firmada de la TSA; Punto de control firmado → Verificar los datos, el nonce y la confianza explícita en la CA; Respuesta firmada de la TSA → Verificar los datos, el nonce y la confianza explícita en la CA · Observaciones sobre lacuenta · Cadena SHA-256 yfirmas Ed25519 · Punto de controlfirmado · Hash de bytes exactosy nonce aleatorio · Solicitud RFC 3161 · TSA independiente · Respuesta firmada dela TSA · Verificar los datos,el nonce y laconfianza explícita enla CA

**Diagrama en formato de texto**

1. Observaciones sobre la cuenta → Cadena SHA-256 y firmas Ed25519
2. Cadena SHA-256 y firmas Ed25519 → Punto de control firmado
3. Punto de control firmado → Hash de bytes exactos y nonce aleatorio
4. Hash de bytes exactos y nonce aleatorio → Solicitud RFC 3161
5. Solicitud RFC 3161 → TSA independiente
6. TSA independiente → Respuesta firmada de la TSA
7. Punto de control firmado → Verificar los datos, el nonce y la confianza explícita en la CA
8. Respuesta firmada de la TSA → Verificar los datos, el nonce y la confianza explícita en la CA

La firma del recopilador vincula los registros a su clave. Una respuesta fiable de la TSA puede confirmar que un punto de control concreto existía en la hora indicada por la TSA. El punto de control puede entonces vincular el prefijo del registro. Esto no establece la hora de cada acción de Telegram ni la veracidad del contenido capturado.

## Procedimiento

1. Conserve la huella digital de la clave del recopilador a través de un canal de confianza independiente. Una clave proporcionada únicamente por el archivo ZIP analizado resulta insuficiente para identificar al recopilador.
2. En **«Exportaciones» → «Preparar solicitud de marca de tiempo»**, descargue el archivo ZIP de solicitud del espacio de trabajo seleccionado. Extraiga los archivos `checkpoint.json`, `timestamp.tsq`, `SHA256SUMS` y `README.txt`. No modifique los bytes de punto de control.
3. Elija una TSA adecuada para la investigación. Envíe `timestamp.tsq` utilizando su método documentado, junto con `application/timestamp-query` para un servicio HTTP. Guarde la respuesta binaria original como `timestamp.tsr`, junto con el punto final, la hora de recuperación y el resultado de la solicitud. La solicitud contiene un hash y un nonce en lugar de mensajes; los metadatos de red siguen revelando la solicitud.
4. Obtenga el certificado raíz de confianza independientemente de la respuesta, además de cualquier certificado intermedio que sea necesario. Un certificado incluido en la respuesta no se considera de confianza simplemente por el hecho de estar incluido en ella.
5. Desde una instalación fiable de TgWitness, compruebe lo siguiente:

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

Añada «`--intermediates tsa-intermediates.pem`» o «`--openssl /path/to/openssl`» si es necesario. OpenSSL debe ser compatible con «`ts`». En Windows, el verificador también busca en la instalación estándar de Git. Se ha probado OpenSSL 3.5.9 localmente con una CA/TSA sintética.

1. Exporte un archivo ZIP del registro firmado tras el punto de control, de modo que incluya dicho prefijo. Verifique utilizando la huella digital conocida de forma independiente:

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. Conserve el archivo ZIP, el punto de control, la solicitud, la respuesta, la cadena de certificados, los resultados de la verificación y el registro de traspaso fuera del colector. Repita la verificación en el momento de la recepción.

Para preparar una solicitud a partir de un punto de control guardado:

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

La preparación normaliza el formato JSON e incluye el punto de control correspondiente en el archivo. Utilice los **bytes del punto de control de dicho archivo** para la verificación TSA, incluso si el archivo de entrada presentaba espacios en blanco diferentes.

## Límites de la verificación

| Comprobar | Comportamiento actual |
| --- | --- |
| Datos | El SHA-256 de los bytes exactos del punto de control debe coincidir con la respuesta. |
| Solicitud | Con `--request`, se verifican la consulta original y el nonce. |
| Firma de la TSA | OpenSSL verifica la firma y la cadena de certificación hasta la CA explícita. |
| Firma del recopilador | Verificado de forma independiente por el verificador del registro mediante una clave fijada. |
| Revocación | No se realiza la recuperación automática de OCSP/CRL |
| Validez a largo plazo | No se realiza validación de los archivos tras la caducidad del certificado |
| Envío programado | Modo de pruebas, desactivado por defecto |

`--request` es técnicamente opcional, pero si se omite, no se podrá verificar el nonce original. Para que este procedimiento sea completo, el resultado `request_checked` debe ser verdadero. La verificación del certificado se rige por las normas y los plazos de verificación de OpenSSL instalados. La conservación a largo plazo requiere una política independiente de certificados y pruebas de revocación.

Una firma criptográfica válida no constituye automáticamente una marca de tiempo cualificada ni una determinación de admisibilidad legal. Si un operador falsificara las observaciones antes de aplicar la marca de tiempo, la TSA fijaría esos bytes; no establecería su veracidad.

## Registro de traspaso

Registre el identificador del caso, el remitente y el destinatario, la hora de transferencia en UTC y su origen, la finalidad, los nombres de archivo y los valores SHA-256, la huella digital del recopilador, el rango de secuencia, las lagunas conocidas, la versión del verificador y el resultado de la verificación. Firme y conserve de forma independiente este registro siguiendo el proceso de su organización. TgWitness no cuenta con un sistema de registro de custodia multiusuario.

Durante el desarrollo no se contactó con ninguna TSA independiente en tiempo real. Las pruebas locales crean una CA/TSA sintética para comprobar la compatibilidad y el rechazo de datos modificados, nonces o CA.
