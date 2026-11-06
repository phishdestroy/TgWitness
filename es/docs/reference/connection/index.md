# Telegram · Conexión, servidores proxy y protección de datos

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/

Autenticación, grupos de proxies automáticos, modos de IP, política de respaldo, solicitudes externas y almacenamiento de claves secretas.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentación](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Implementación y recuperación](https://phishdestroy.github.io/TgWitness/es/docs/reference/deployment/)

![Implementación y recuperación](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Este documento describe el comportamiento de TgWitness 0.8.0 y sus limitaciones. La autenticación, el acceso a la fuente, la conectividad de red y la integridad de la captura son estados independientes. Para conocer los pasos de inicio de sesión, los formatos de archivo y la gestión de cuentas múltiples, comience por la sección [«Cuentas y formatos de sesión](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/)». Para conocer las políticas de eventos y el comportamiento ante reinicios, consulte [«Cómo funciona la recopilación](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/)».

## Configuración guiada de la conexión

En «**Conexión**», el administrador puede elegir «**Esta cuenta**», «**Un grupo de cuentas**» o «**Todas las cuentas**», y a continuación seleccionar una ruta. «**Revisar selección**» muestra la lista de cuentas afectadas. «**Preparar y comprobar**» comprueba la ruta propuesta sin modificar la guardada. «**Aplicar conexión comprobada**» vuelve a comprobar, pausa la observación si es necesario, guarda la ruta y reanuda la observación que ya se estaba ejecutando. Nunca inicia la recopilación en una cuenta que haya estado inactiva anteriormente. Las descargas del historial permanecen en pausa y pueden reanudarse por separado. Pausa las exportaciones activas antes de cambiar.

Los cambios en los grupos mantienen las cuentas con su propia ruta por defecto. Desactive esa opción solo cuando la vista previa muestre los cambios que desea realizar. La aplicación informa del resultado de cada cuenta; no se trata de una transacción de «todo o nada» entre bases de datos. Un cambio fallido restaura la configuración anterior de esa cuenta. Si no se puede reanudar, se muestra explícitamente. Las vistas previas caducan a los diez minutos y los cambios en la configuración de la conexión o en la pertenencia a grupos requieren una nueva comprobación.

| Ruta | Qué gestiona TgWitness |
| --- | --- |
| Directo | Conexiones desde el servidor; no se detecta ni se impone el uso de una VPN de un servidor externo. |
| VPN | Un perfil WireGuard de túnel completo por cuenta, ejecutado por un proceso SOCKS5 en el espacio de usuario local. No se instala ninguna interfaz de host ni controlador. |
| Mi proxy | Credenciales SOCKS5, HTTP CONNECT o MTProxy. Se puede introducir una URL en los campos SOCKS5/HTTP. Al seleccionar varias cuentas, se comparte este proxy introducido. |
| MTProto público | El grupo existente asigna rutas «Telegram». Las solicitudes externas están desactivadas hasta que se configure un proxy adecuado independiente en los ajustes avanzados. |
| WARP | Un túnel local independiente para cada cuenta seleccionada, con registro en WARP y un perfil de WireGuard almacenado en el almacén de esa cuenta. |

La comprobación de la ruta actual utiliza un transporte Telegram nuevo y sin autenticar, no la sesión de la cuenta. Para las rutas compatibles con HTTP, también solicita el rastreo HTTPS de Cloudflare a través de esa ruta y muestra la IP de salida, el país, el estado de WARP y la hora de la comprobación que se indican. La latencia medida es el tiempo de establecimiento de la conexión Telegram, no un ping ICMP. La preparación de WARP falla a menos que el rastreo indique que WARP está activo. Estas comprobaciones establecen la conectividad, no la autenticidad ni la integridad de los mensajes capturados. El mero hecho de que se ejecute un proceso local no constituye una comprobación de salida satisfactoria.

### WARP y WireGuard portátiles

Se trata de una integración no oficial de WARP **** que utiliza [wgcf 2.3.1](https://github.com/ViRb3/wgcf/releases/tag/v2.3.1) y [wireproxy 1.1.3](https://github.com/windtf/wireproxy/releases/tag/v1.1.3). El administrador acepta explícitamente la configuración antes de la primera descarga o del registro en WARP. Esas conexiones de configuración se dirigen directamente a GitHub y Cloudflare y revelan la IP del equipo. El tráfico habitual de la cuenta mantiene su ruta existente hasta la aplicación. Cloudflare elige la dirección de salida y el país; los túneles independientes pueden compartir una dirección de salida. Esta función no ofrece selección de país, rotación periódica de IP ni un «kill switch» de VPN para todo el host.

Descargas de utilidades compatibles: Linux y macOS x86-64/ARM64, y Windows x86-64. Los artefactos se comparan con los hash SHA-256 incluidos en el código fuente revisado, y los ejecutables almacenados en caché se comprueban de nuevo antes de su ejecución. No se añade ninguna herramienta auxiliar a la variable PATH, ni se instala como servicio del sistema, ni se le asigna un listener público. Todos los archivos se encuentran en el directorio `portable-routes/` del espacio de trabajo y en entradas cifradas del almacén. El listener de bucle cerrado SOCKS5 requiere credenciales generadas de forma independiente.

Los perfiles privados y las credenciales de la cuenta WARP se cifran con el almacén de datos del espacio de trabajo existente. Mientras se ejecuta, el programa auxiliar necesita una configuración en texto plano de acceso exclusivo para el propietario; esta se elimina al detenerse normalmente. Un fallo del servidor puede dejar este archivo en la carpeta de datos de acceso exclusivo para el propietario. Esto no cifra el disco ni protege contra su administrador. El supervisor cierra el túnel si la tubería principal del panel desaparece. Un túnel fallido nunca habilita una solución alternativa directa. El reinicio del panel restaura un túnel seleccionado; los inicios fallidos se reintentan con un retraso limitado. **Detener el túnel** también pausa la observación y mantiene el estado de parada. **Iniciar el túnel** inicia el túnel; reanuda la observación por separado cuando esté listo.

Los perfiles de WireGuard cargados deben contener una interfaz y un par, rutas IPv4 e IPv6 completas, y no deben incluir hooks, includes, sustituciones de entorno ni listeners adicionales. Las direcciones de los puntos finales públicos se resuelven y se fijan antes del inicio. Utiliza una VPN externa o una puerta de enlace SOCKS5 para OpenVPN/IPsec y puntos finales privados.

## Métodos de autenticación

**El ID de API y el hash de API identifican una aplicación; no sustituyen al inicio de sesión en la cuenta.** Son opcionales en TgWitness. Orden de prioridad: primero, un par introducido en el formulario; a continuación, uno procedente de un archivo JSON de una cuenta importada; después, el par guardado en el espacio de trabajo; y, por último, el conjunto integrado de 50 pares públicos, que se prueban en orden aleatorio con rotación automática cuando Telegram rechaza uno. Solo el par de Telegram Desktop (2040) se envía con una descripción coincidente del cliente de Telegram Desktop. Su propio par, obtenido de las Herramientas de desarrollo de la API en [my.telegram.org,](https://my.telegram.org) puede utilizarse con todas sus cuentas; cada cuenta sigue teniendo su propia autorización.

| Método | Requisitos | Asistencia técnica de TgWitness |
| --- | --- | --- |
| Teléfono, código, 2FA opcional | Acceso a la cuenta; par de API opcional | Inicio de sesión en el panel |
| Clave de autenticación HEX + ID de DC | Clave completa de 512 caracteres y DC 1–5 | Pestaña **«Clave de autenticación** directa»; se comprueba el ID de usuario opcional antes de guardar la autorización. |
| Telethon StringSession | Una cadena de sesión válida | Inicio de sesión en el panel |
| Telethon SQLite `.session` | Texto definitivo y coherente | Importación directa de esquemas mediante panel 7/8; CLI sin conexión opcional |
| Pyrogram SQLite `.session` | Sesión de usuario de producción cerrada | Importación directa de esquemas mediante el panel 2/3 |
| Telegram Desktop TData ZIP | Una cuenta moderna; código de acceso local si está protegida | Conversión en memoria con comprobaciones de suma de comprobación y descifrado |
| Fichero JSON de la cuenta | Campos compatibles de API/sesión/clave | Los metadatos por sí solos no bastan para completar las credenciales de la API; sigue siendo necesario iniciar sesión mediante una sesión/clave o un teléfono/código QR. |
| Inicio de sesión mediante código QR | Confirmación procedente de una aplicación autorizada de Telegram | Generación local de códigos QR, caducidad/reintento, autenticación de dos factores (2FA) opcional |
| TDLib / Pyrogram StringSession | Otros formatos específicos de bibliotecas | No compatible |
| Token del bot | Un bot con su propio modelo de acceso y actualización | No lo utiliza este recopilador |

Telegram opta por el envío de códigos; no se garantiza la entrega por SMS. Un hash de la API no puede restaurar una sesión revocada ni sustituir una contraseña de 2FA olvidada. TgWitness no almacena los códigos de inicio de sesión ni la contraseña de 2FA de Telegram en el disco.

En el caso de una fuente privada, la cuenta ya debe tener acceso. No es necesario indicar el nombre de usuario del grupo. Un proxy o una importación de sesión no otorgan ni la condición de miembro ni derechos de administrador. La pertenencia actual al grupo no garantiza el acceso al historial anterior a la incorporación.

## Importar un archivo de sesión de Telethon

Telethon SQLite, Pyrogram SQLite y Telegram Desktop TData utilizan formatos distintos. El panel detecta y convierte las estructuras compatibles; cambiar el nombre de un archivo no constituye una conversión. Seleccione una sesión y su archivo JSON asociado en **«Archivos**» y, a continuación, pulse **«Conectar cuenta**». Se aceptan hasta cuatro archivos coincidentes y un total de 8 MiB. Consulte [los límites de formato](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/) para obtener más detalles sobre TData/JSON. No existe la recuperación de la contraseña. El inicio de sesión mediante teléfono/autenticación de dos factores (2FA) o código QR crea una autorización independiente.

La ruta opcional de la línea de comandos exclusiva para Telethon sigue estando disponible:

1. Detenga el cliente que utiliza la sesión original y realice una copia coherente. El convertidor rechaza los archivos con un WAL/registro incompleto. Cierre el cliente original correctamente en lugar de eliminar dichos archivos para eludir la comprobación.
2. Desde el entorno de TgWitness, ejecute:

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. En **«Añadir cuenta» → «Archivos»**, cargue el resultado o pegue su cadena de texto y continúe.
2. Compruebe el ID numérico de la cuenta que se muestra, seleccione las fuentes e inicie la observación.

**El archivo convertido es una clave de acceso a la cuenta sin cifrar.** Guárdelo en un almacén protegido y nunca lo incorpore al control de versiones ni lo envíe a un servicio de conversión de terceros. TgWitness guarda la sesión autorizada en su almacén cifrado. Copiar una sesión no crea una autorización independiente: no ejecute clientes simultáneos con claves de autorización clonadas ni dé por sentado que las actualizaciones se entregan de forma independiente.

La conversión transfiere la autorización, no los mensajes originales, la caché de la entidad ni un cursor de actualización permanente. No garantiza la recuperación de las actualizaciones tras el reinicio de los procesos.

## MTProto, Telethon y proxies

MTProto es el protocolo de Telegram. Telethon es la biblioteca de cliente de Python que utiliza TgWitness. MTProxy es un proxy de transporte de Telegram; SOCKS5 y HTTP CONNECT proporcionan túneles generales. Ninguno de ellos sustituye a la autenticación de la cuenta.

Guarda la ruta de cada espacio de trabajo en **Cuenta → Ajustes → Ajustes de conexión → Cambiar ruta de conexión** antes de iniciar sesión. Los nuevos espacios de trabajo utilizan por defecto la opción **Automático MTProxy · listas públicas** con **la opción Ocultar la dirección**. Los espacios de trabajo existentes que utilizaban explícitamente Direct conservan un modo que lo permite.

## Modos de IP

La ruta elige la conexión. El modo IP, **la protección de IP** en la sección «Cuenta» del panel, determina cuándo puede quedar expuesta la dirección del servidor. Estos controles no instalan una VPN ni redirigen todo el tráfico del equipo.

| Modo | Telegram | Solicitudes externas |
| --- | --- | --- |
| Ocultar la dirección (`hide`) | Utilice un proxy; espere si ninguno funciona. No hay alternativa directa. | Requiere SOCKS5/HTTP; rechaza las solicitudes que no cuenten con un proxy adecuado. |
| Direct como último recurso (`fallback`) | El MTProxy automático puede utilizar la conexión directa tras el retraso configurado y, a continuación, volver a un proxy operativo. | Se prefiere un proxy externo configurado o la ruta SOCKS5/HTTP de la cuenta; en caso contrario, se permite el acceso directo. |
| Servidor detrás de un túnel o una VPN (`tunnel`) | Se permiten las rutas directas y el recurso inmediato al grupo automático. | Se permite el acceso directo cuando no se ha configurado ningún proxy aplicable. |

El modo «túnel» o «VPN» da por hecho que gestionas esa red por separado. Sin un túnel operativo, los destinatarios pueden ver la propia dirección del servidor. Selecciona el modo en función de tu red real, no del nombre de la opción.

### Elija una ruta

| Ruta | Configuración | Límites |
| --- | --- | --- |
| MTProxy automático | Listas integradas o un catálogo de operadores | Mantiene una ruta de Telegram operativa; la alternativa directa depende del modo IP. |
| Directo | Modo túnel o VPN | Telethon utiliza la ruta de red del anfitrión |
| SOCKS5 | Servidor, puerto, nombre de usuario y contraseña (opcionales) | python-socks, DNS de destino remoto habilitado |
| HTTP CONNECT | Servidor, puerto, nombre de usuario y contraseña (opcionales) | HTTP CONNECT sin cifrar; no se ha implementado el protocolo TLS con el propio proxy. |
| MTProxy | Servidor, puerto, clave secreta | Transporte experimental de Telethon; 32 dígitos hexadecimales o «`dd`» + 32 dígitos hexadecimales |

Se rechazan los secretos TLS falsos «`ee`». La normalización de Telethon 1.45 puede eliminar un prefijo y un dominio, pero eso no implementa el TLS falso. Pegue «`tg://proxy?server=…&port=…&secret=…`» o «`https://t.me/proxy?server=…&port=…&secret=…`» y seleccione **«Rellenar campos desde el enlace**». Esto valida y rellena los campos sin conectarse ni guardar; revise y guarde la ruta por separado. Los campos manuales siguen estando disponibles. Consulte [los enlaces de proxy de Telegram](https://core.telegram.org/api/links#proxy-links).

### Proxies públicos proporcionados por su instalación

La lista integrada combina cuatro fuentes: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) y [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). La instantánea incluida contiene datos de los puntos finales, la atribución de las fuentes y las fechas de descarga. La inclusión de un proveedor en la lista no constituye prueba de que el proxy funcione o de que proporcione todas las actualizaciones de Telegram.

**MTProxy** comprueba **automáticamente** la conectividad de transporte de Telegram, mantiene un proxy operativo y cambia a otro cuando falla. Los espacios de trabajo prefieren diferentes proxies cuando hay suficientes entradas operativas disponibles; no se garantiza una dirección de salida única. Los proxies que fallan descansan antes de un nuevo intento. Si ninguno funciona, el modo IP determina si la recopilación debe esperar o puede utilizar una conexión directa. El cambio de proxies no modifica la cuenta ni borra su registro. Las elecciones y los cambios de ruta se registran en el registro firmado.

Mientras las rutas automáticas estén activas, las listas se actualizan cada hora y las comprobaciones de transporte se ejecutan cada diez minutos de forma predeterminada. Estos intervalos son configurables. **La actualización de las listas públicas** requiere una refresco; el mero hecho de consultar la lista no modifica una ruta manual guardada.

**El tráfico de Telegram y las solicitudes HTTPS utilizan rutas diferentes.** Las descargas de listas utilizan una conexión HTTPS independiente y la ruta de solicitud externa proporcionada. «`TGWITNESS_PROXY_FEED_PROXY`» anula explícitamente dicha ruta mediante un proxy HTTP/SOCKS5; ambas variantes del recopilador «Compose» la reenvían. El grupo en segundo plano sigue el espacio de trabajo principal. No se envía ninguna sesión de Telegram, credenciales de API, token de panel ni token de bot a los proveedores de fuentes. Los nombres de los proveedores, las fechas de las instantáneas y la ruta de descarga aparecen en la sección **«De dónde procede la lista**».

Un MTProxy solo transporta tráfico de Telegram. Las operaciones HTTP del espacio de trabajo, como las marcas de tiempo, las notificaciones, las copias externas y las comprobaciones de origen, utilizan un proxy SOCKS5/HTTP independiente cuando está configurado, y posteriormente la ruta SOCKS5/HTTP de la cuenta. Sin ninguno de los dos, la opción «Ocultar la dirección» rechaza la solicitud; los demás modos permiten el acceso directo. Las solicitudes externas pueden desactivarse. Un proxy de descarga de feeds configurado explícitamente sigue siendo una opción de anulación independiente por parte del operador. El servicio de testigos independiente mantiene su propia ruta.

Para los servicios privados gestionados por el operador, la configuración existente del entorno del servidor `TGWITNESS_ALLOW_PRIVATE_DESTINATIONS=1` permite destinos privados y mantiene la resolución del nombre de host por parte del proxy. No se puede habilitar desde el panel. El modo «solo público» rechaza los destinos .`.onion` antes de consultar el resolutor público; los servicios «onion» de Tor requieren esa configuración explícita de destino privado y un proxy adecuado. Este comportamiento del DNS se aplica a las operaciones HTTP externas, no al transporte de Telegram. Cloudflare documenta el [punto final JSON del DNS](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/).

****Parámetros automáticos del grupo****

En **Parámetros → MTProxy automático**, configura el umbral de fallo, el tiempo de espera, la rotación planificada, el uso compartido del proxy y el retraso de recambio permitido.

| Control | Por defecto |
| --- | --- |
| Se desconecta antes de la sustitución | 3, en un plazo de 10 minutos |
| Proxies probados por cada intento de conexión | 3 |
| Primer / máximo reposo tras un fallo | 10 minutos / 6 horas |
| Rotación prevista | Desactivado; activar en caso de fallo |
| Cuentas por proxy | 0: dar preferencia a las entradas independientes; compartir cuando sea necesario. Establecer 1 en esperar para una entrada exclusiva. |
| Retardo antes de que se permita el recurso directo | 10 minutos; Ocultar la dirección sigue sin funcionar Direct |
| Comprobaciones de actualización y transporte de la fuente de datos | Actas de 60/10; los valores del espacio de trabajo principal se aplican al grupo compartido |

El uso de diferentes proxies no garantiza direcciones de salida diferentes. Estos ajustes no anulan los límites de Telegram ni garantizan el anonimato.

Para sustituir la lista pública por su propio catálogo de operadores, configure la sustitución que se indica a continuación. Esto desactiva por completo las suscripciones externas, incluso cuando su matriz «`proxies`» está vacía.

Copie [el catálogo vacío](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) en `proxy-config/proxies.json` y añada sus puntos finales públicos implementados:

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

Los valores de ejemplo deben sustituirse. Se aceptan hasta 32 entradas distintas. La lista autenticada devuelve etiquetas/hosts/puertos sin secretos compartidos; al seleccionar uno, sus credenciales se guardan en el almacén de seguridad del espacio de trabajo. La disponibilidad no se comprueba hasta que se realice una prueba de transporte explícita. Un catálogo mal formado permite la configuración manual.

Ejecución nativa: establezca «`TGWITNESS_PROXY_CATALOG`» como ruta JSON local. Docker:

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

La superposición se monta como `proxy-config` de solo lectura; los archivos deben ser legibles por el UID 10001 del contenedor. Dicho directorio queda excluido de Git, del contexto de compilación de Docker y de los archivos fuente. Este catálogo configura las cuentas de recopilación; [el bot testigo](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/) utiliza su propia ruta HTTP/SOCKS5, no MTProxy.

La alternativa directa se rige por el modo IP descrito anteriormente. Suspenda la observación antes de cambiar de ruta. Al guardar, se desconectan los clientes antiguos y se cancela el inicio de sesión pendiente; un nuevo cliente utiliza la ruta guardada. El enlace entre el diario y la sesión de la cuenta se mantiene. La configuración sustituye a la ruta anterior: vuelva a introducir las credenciales del proxy al editarla.

Las credenciales se cifran mediante el algoritmo `network.enc`. La API no devuelve el nombre de usuario, la contraseña ni el secreto. Los registros firmados contienen el tipo de ruta e indican si hay credenciales presentes, excluyendo el punto final y los secretos. El operador puede ver el punto final en el panel. Los campos de secretos se borran tras guardar, bloquear o cambiar de espacio de trabajo.

**La función «Probar conexión de Telegram**», disponible también antes de iniciar sesión, abre y cierra una conexión temporal y no autorizada a Telegram a través de la ruta. No se establece contacto con ningún sitio web de verificación de IP. El éxito de la prueba confirma la conectividad de transporte, pero no el acceso a grupos, la entrega completa ni el anonimato.

El proxy se aplica a las conexiones del cliente de Telegram, incluidas las descargas de archivos multimedia de los servidores de datos (DC) de Telegram. El navegador, pip, SSH y las herramientas TSA ejecutadas manualmente siguen rutas independientes. El nombre de host del proxy puede resolverse localmente. `rdns` afecta a los nombres de host de destino; Telegram suele proporcionar direcciones IP numéricas de los servidores de datos (DC).

Ni SOCKS5 ni el protocolo HTTP CONNECT sin cifrar cifran por sí mismos las credenciales del proxy ni el túnel entre el cliente y el proxy. MTProto protege por separado el tráfico de Telegram. Utilice un canal seguro adecuado para conectarse al proxy en una red no fiable. Los grupos privados son chats en la nube; MTProto no los convierte en chats secretos con cifrado de extremo a extremo.

## Cifrado y firmas

| Nivel | Implementado | Responsabilidad del operador |
| --- | --- | --- |
| Tráfico de Telegram | Telethon MTProto | Confianza, ruta y disponibilidad de la plataforma |
| Panel web | Token de portador, configuración predeterminada de bucle cerrado, límites de solicitudes | HTTPS o túnel SSH para el acceso remoto |
| Secretos | Fernet para las credenciales de la API, la sesión, las credenciales del proxy y la clave privada de firma | Proteja la clave de descifrado y el servidor en el que se ejecuta la herramienta |
| Clave de la bóveda | Clave local o clave maestra externa para una nueva instalación | Almacenamiento protegido independiente y copia de seguridad de las claves |
| Mensajes y archivos adjuntos | Almacenamiento de la aplicación en texto sin formato | Disco o volumen cifrado |
| ZIP/JSONL/CSV/HTML | Comprobaciones de integridad, sin cifrado de contenido | Proteja las copias exportadas y las transferencias |
| Procedencia y hora | Registro firmado, acuse de recibo, herramientas RFC 3161 | Clave de confianza, puntos de control independientes/TSA y procedimiento de custodia |

**La protección del almacenamiento** en «Cuenta» muestra estos estados. El token del panel es un secreto de acceso, no una contraseña de cifrado. Otorga acceso de administrador; [los tokens emitidos](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/) pueden limitarse a cuentas y chats. Los espacios de trabajo comparten el proceso anfitrión y no son inquilinos aislados.

BitLocker, LUKS, FileVault o un volumen cifrado gestionado pueden proteger el almacenamiento según sus respectivos modelos de amenaza. El administrador de un equipo en funcionamiento y desbloqueado sigue pudiendo leer los datos. Incluya SQLite WAL/SHM, archivos multimedia, exportaciones temporales, el espacio de intercambio, las copias de seguridad y las descargas del navegador en la planificación del almacenamiento. Un volumen de Docker no está cifrado por el mero hecho de ser un volumen. TgWitness no implementa SQLCipher ni el cifrado de objetos.

## Clave maestra externa

Para una **nueva** instalación, coloque la clave maestra fuera del directorio de datos. Esto no migra automáticamente una bóveda de claves local ya existente. Prepare un directorio de claves al que solo pueda acceder la identidad del servicio y, a continuación, ejecute:

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell, utilizando el entorno de proyecto instalado:

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

En Docker, monte el archivo en modo de solo lectura fuera de «`/data`», por ejemplo, en « `/run/secrets/tgwitness-master.key`», y configure la variable de entorno con esa ruta. El UID del servicio debe poder leerlo. Transmita la ruta, no los bytes de la clave, a través de los archivos de entorno o configuración.

Cada espacio de trabajo recibe una «salt» pública aleatoria y su propia clave Fernet derivada mediante HKDF-SHA256. `vault.external.json` almacena los metadatos de derivación, no la clave maestra. Si falta una clave o esta es incorrecta, el inicio fallará sin que se sustituya de forma silenciosa. Conserve tanto los metadatos de la «salt» como la clave maestra para la recuperación.

Todos los espacios de trabajo se derivan de la misma clave maestra; su compromiso afecta a toda la instalación. El proceso en ejecución puede descifrar secretos. No se trata de un HSM ni de un KDF de contraseña. No se aceptan contraseñas arbitrarias introducidas manualmente en lugar de una clave aleatoria.

Conserve la clave actual para las instalaciones existentes hasta que se haya implementado y verificado una migración planificada. La eliminación de «`vault.key`» o la sustitución de una clave maestra puede impedir el acceso a las sesiones o a las claves de firma. Mantenga las copias de seguridad cifradas y las claves por separado y pruebe la recuperación en una instancia aislada.
