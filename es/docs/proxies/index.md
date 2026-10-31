# Elija un proxy

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/proxies/

Mantenga la cuenta conectada. Indique explícitamente cuándo su ruta puede utilizar la dirección del servidor.

## Seleccione primero el modo IP

01**Ocultar IP**

Utilice un proxy. Si ninguno funciona, espere sin conexión directa a Telegram.

02**Permitir alternativa**

Permitir la conexión directa tras el retraso configurado; volver a un proxy operativo cuando alguno responda.

03**Túnel / VPN**

Permita rutas directas a través de la red del proveedor de alojamiento. Esta opción no instala ni verifica una VPN.

La ruta determina la conexión. El modo IP determina si se permite una conexión directa.

## Deje que el grupo se encargue de la ruta

1. Abra **la cuenta → Ajustes → Ajustes de conexión**.
2. Seleccione el modo IP y **MTProxy automático**, o introduzca una ruta fija.
3. Guarde y ejecute **la prueba de conexión a Telegram**. También funciona antes de iniciar sesión.
4. Una vez iniciada la recopilación, compruebe que un mensaje de prueba llegue al registro.

Los nuevos espacios de trabajo utilizan MTProxy automático con la función «Ocultar IP». El conjunto combina cuatro fuentes públicas, comprueba las entradas, conserva las rutas operativas y sustituye los proxies que fallan. Las descargas fallidas conservan las instantáneas anteriores.

## Utilice su propio proxy

Introduzca los datos de SOCKS5 o HTTP CONNECT, pegue un enlace de proxy de Telegram compatible o facilite un catálogo de operadores. Ponga en pausa la observación antes de cambiar una ruta activa. Los secretos TLS falsos de MTProxy que comienzan por `ee` siguen sin ser compatibles.

**Configuración de rotación, uso compartido y reintentos**

En **Parámetros → MTProxy automático**, configure los umbrales de fallo, los tiempos de espera, la rotación planificada y el número de cuentas por proxy. Un límite de uso compartido de uno hace que una cuenta tenga que esperar cuando no hay ninguna entrada exclusiva disponible. Los intervalos de actualización de la lista y de sondeo siguen los valores del espacio de trabajo principal. Los proxies independientes no garantizan direcciones IP de salida independientes.

## Separar Telegram de las solicitudes externas

MTProxy solo transmite tráfico de Telegram. Las marcas de tiempo, las notificaciones, las copias y las comprobaciones de origen utilizan un proxy SOCKS5/HTTP independiente, la ruta SOCKS5/HTTP de la cuenta o la conexión directa cuando el modo IP lo permite. Dichas solicitudes externas pueden desactivarse.

Una configuración explícita de «`TGWITNESS_PROXY_FEED_PROXY`» establece la ruta del descargador de feeds. El [testigo independiente](https://phishdestroy.github.io/TgWitness/es/docs/witness/) mantiene su propia configuración. Estos controles no instalan una VPN del sistema ni redirigen el tráfico del navegador.

Consulte [todos los modos, valores predeterminados y listas de fuentes](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/#ip-modes), o [elija quién puede modificar la ruta de una cuenta](https://phishdestroy.github.io/TgWitness/es/docs/access/).
