# Telegram · Elija un proxy

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/proxies/

Mantenga la cuenta conectada y decida usted si alguna vez puede mostrar la IP de su servidor.

## Seleccione primero el modo IP

01**Ocultar la dirección**

Solo proxy. Si ninguno funciona, espera.

02**Directo como último recurso**

Va directo tras un retraso y vuelve a un proxy en cuanto uno funcione.

03**Servidor detrás de un túnel o una VPN**

Directo está bien. No configura ni comprueba la VPN por usted.

La ruta determina la conexión. El modo IP determina si se permite una conexión directa.

## Deje que el grupo se encargue de la ruta

1. **Cuenta → Ajustes → Ajustes de conexión**.
2. Elija el modo de IP y **MTProxy automático**, o una ruta fija.
3. Guarde y pulse **Probar conexión con Telegram** (funciona también antes de iniciar sesión).
4. Empiece a recoger y envíese un mensaje de prueba.

Los espacios nuevos arrancan con MTProxy automático y **Ocultar la dirección**. El pool usa cuatro listas públicas, prueba servidores, se queda con los buenos y sustituye los caídos.

## Utilice su propio proxy

SOCKS5, HTTP CONNECT, un enlace de proxy de Telegram o un catálogo del operador. Pause la observación antes de cambiar. Los secretos Fake TLS (`ee`…) no funcionan.

**Configuración de rotación, uso compartido y reintentos**

**Parámetros → MTProxy automático**: umbrales de fallo, esperas, rotación y cuentas por proxy. Límite 1 significa que la cuenta espera en lugar de compartir. Proxies distintos pueden compartir la misma IP de salida.

## Separar Telegram de las solicitudes externas

MTProxy solo transporta Telegram. Marcas de tiempo, notificaciones, copias y comprobaciones de código van por un proxy SOCKS5/HTTP aparte, la ruta SOCKS5/HTTP de la cuenta o en directo si el modo lo permite. O desactívelas.

`TGWITNESS_PROXY_FEED_PROXY` fija la ruta para descargar las listas. El [testigo](https://phishdestroy.github.io/TgWitness/es/docs/witness/) tiene sus propios ajustes. Nada de esto toca su navegador ni la red del sistema.

Más: [modos y valores por defecto](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/#ip-modes), [quién puede cambiar rutas](https://phishdestroy.github.io/TgWitness/es/docs/access/).
