# Implementación de alta seguridad

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/high-assurance/

Un servidor sellado disponible las 24 horas del día, los 7 días de la semana, en Hetzner o Phala Cloud, un DNS de puerta de enlace y comprobaciones que un tercero puede repetir.

High-assurance deployment adds independent checks of the collection environment to archive verification．The reviewer queries deployment and access records held by the cloud provider and Cloudflare，and an Intel TDX deployment adds hardware attestation of the collector's environment．

El uso habitual de Docker y en el entorno local no sufre cambios. Nada de lo que hay aquí se ejecuta a menos que se implemente con `python -m tgwitness.cloud`, y el recopilador lee su host únicamente cuando la implementación establece `TGWITNESS_ASSURANCE`.

Diagrama de flujo · Operador → Servidor, cortafuegos sin reglas de entrada (API del proveedor); Operador → Túnel y DNS (API de Cloudflare); Servidor, cortafuegos sin reglas de entrada → Túnel y DNS (solo salida); Servidor, cortafuegos sin reglas de entrada → Clave de firma creada en el servidor; Verifier, tokens de solo lectura → Registro del proveedor y cortafuegos; Verifier, tokens de solo lectura → Dirección del conector de túnel e ingreso; Verifier, tokens de solo lectura → Declaración firmada de /api/assurance; Verifier, tokens de solo lectura → Archivo ZIP de pruebas · Operador · Verifier, tokens de sololectura · Servidor, cortafuegos sinreglas de entrada · Registro del proveedor ycortafuegos · Dirección del conector detúnel e ingreso · Declaración firmada de/api/assurance · Archivo ZIP de pruebas · Túnel y DNS · Clave de firma creada enel servidor · API del proveedor · API de Cloudflare · solo salida

**Diagrama en formato de texto**

1. Operador → Servidor, cortafuegos sin reglas de entrada (API del proveedor)
2. Operador → Túnel y DNS (API de Cloudflare)
3. Servidor, cortafuegos sin reglas de entrada → Túnel y DNS (solo salida)
4. Servidor, cortafuegos sin reglas de entrada → Clave de firma creada en el servidor
5. Verifier, tokens de solo lectura → Registro del proveedor y cortafuegos
6. Verifier, tokens de solo lectura → Dirección del conector de túnel e ingreso
7. Verifier, tokens de solo lectura → Declaración firmada de /api/assurance
8. Verifier, tokens de solo lectura → Archivo ZIP de pruebas

## Lo que puede comprobar un verificador

| Afirmación | Cómo se comprueba | Mantenido por |
| --- | --- | --- |
| El servidor se creó a través de la API del proveedor en un momento determinado. | El objeto «servidor» y su creación en el propio registro del proveedor | Proveedor |
| Nadie utilizó las rutas de acceso del proveedor | Registro de solicitudes de consola, recuperación, restablecimiento de contraseña, reconstrucción, ISO, imágenes y copias de seguridad | Proveedor |
| No se pudo establecer conexión con él | El cortafuegos del proveedor no tiene reglas de entrada; el SSH queda oculto desde el primer arranque. | Proveedor (cortafuegos), servidor (SSH) |
| Solo se puede acceder al panel a través del túnel | El ingreso al túnel se reenvía únicamente al panel; el conector se ejecuta desde la dirección del servidor | Cloudflare |
| Este mismo software se ejecuta | El hash firmado del árbol de código fuente del recopilador coincide con una copia del commit implementado. | Collector, sincronizado con Git |
| La clave de firma se creó en ese servidor. | La clave firma una declaración en la que se indica el ID del servidor del proveedor y el hash del archivo «cloud-init» que ha recibido. | Collector, verificado con el proveedor |
| El diario pertenece a esa clave y a ese servidor | Cada inicio de proceso en la prueba ZIP incluye la medición del host correspondiente a ese servidor | Pruebas ZIP |

The collector records SSH state，sessions，login history and boot information in signed process-start and `host.state` records．On an ordinary VM these are local inventory records，which the reviewer compares with the provider's independent records．The Intel TDX deployment below additionally verifies hardware-backed measurements．

## Proveedores

| `--provider` | Credenciales | Acceso de solo lectura de Verifier | Registro del proveedor para el verificador | Se conserva para |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Token de lectura del mismo proyecto | Acciones del servidor y del cortafuegos | Mientras existan los recursos |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Token de acceso personal de solo lectura | Acciones de Droplet | Mientras el Droplet exista |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` ámbitos de solo lectura | Eventos de la cuenta, versiones de las reglas del cortafuegos | 90 días |
| `vultr` | `VULTR_API_KEY` | Usuario con acceso de lectura y el `activity_logs` permiso | Registro de actividad de la cuenta (método, ruta, actor) | 30 días, o más con una suscripción al registro de auditoría |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | Historial de eventos de CloudTrail | 90 días |
| `phala` | `PHALA_CLOUD_API_KEY` | Una clave API del mismo espacio de trabajo | Revisiones de la aplicación y operaciones de la CVM: cambios en la configuración y el entorno de Docker Compose, reinicios y actualizaciones del sistema operativo | Aunque la aplicación existe |
| `generic` | ninguno | ninguno | ninguno: **autocertificado** | – |

Utiliza un proyecto, equipo, cuenta o subcuenta específicos para cada caso: el acceso de solo lectura del verificador mostrará entonces únicamente esta implementación. Las credenciales se leen desde `--provider-token-file` de la variable anterior, nunca desde la línea de comandos. Para AWS, el archivo contiene `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; la región es `--location`.

En cada informe se indica lo que los registros de cada proveedor no pueden mostrar. En resumen: Hetzner registra las solicitudes de la consola; la consola de recuperación de DigitalOcean, Lish/Glish de Linode y la consola web de Vultr no se registran como tales, por lo que el acceso de root queda bloqueado en el primer arranque y para iniciar sesión en la consola sería necesario restablecer la contraseña o cambiar la configuración de arranque, acciones que sí se registran. Vultr devuelve la dirección de la consola a cualquier clave que pueda leer la instancia; ni el registro ni el informe la almacenan.

## Máquina virtual confidencial en Phala Cloud (Intel TDX)

Con `--provider phala` el colector se ejecuta en una máquina virtual confidencial Intel TDX en [Phala Cloud](https://phala.com/), gestionada por dstack. Ni el anfitrión ni el personal de Phala pueden leer su memoria, y el procesador firma un certificado que acredita lo que ha arrancado la máquina. El verificador no se fía de la palabra de Phala: `tgwitness.tdx` comprueba él mismo cada certificación, hasta la CA raíz de Intel SGX fijada, cotejándola con las listas de revocación de Intel y los datos de plataforma firmados por Intel, y rechaza las máquinas que puedan ser depuradas o migradas.

| Entrada de informe | Qué muestra |
| --- | --- |
| `tdx_binding` | La certificación abarca la declaración firmada del recopilador y el valor aleatorio de esta solicitud. |
| `tdx_quote` | Intel avala la certificación; solo se aprueba cuando Intel considera que la plataforma está actualizada. |
| `tdx_compose_hash` | RTMR3, reproducido a partir del registro de eventos de dstack, mide la composición de la aplicación que informa el recopilador. |
| `tdx_compose` | Ese código es, byte a byte, el mismo que genera el código de la confirmación desplegada: archivos fuente fijados por hash, ambas imágenes por resumen, sin ningún otro código. |
| `tdx_identity` | La certificación procede de la aplicación y la instancia desplegadas, con claves del KMS de Phala y un disco cifrado. |
| `tdx_os` | MRTD y RTMR0-2 equivalen a los valores que el verificador calcula a partir de la imagen del sistema operativo dstack que publica Dstack-TEE, determinada por el hash de la imagen del sistema operativo que informa la CVM, y a partir de las tablas ACPI que QEMU genera para la configuración de la máquina virtual: firmware, kernel, initrd, línea de comandos con el hash del sistema de archivos raíz, memoria, vCPU y dispositivos. Una imagen de desarrollo falla |

La imagen del sistema operativo (aproximadamente 180 MB, de los cuales se conservan 21 MB) se descarga una sola vez desde [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases) a `dstack-images` junto al registro; `--tdx-image FOLDER` utiliza otra carpeta o una imagen descomprimida, `--tdx-image none` omite la comparación. La medición sigue a `dstack-mr` y al paquete Rust `qemu-acpi` de Dstack-TEE/dstack; `tools/check_dstack_image.py` la compara con la salida ACPI propia de QEMU y con un registro de certificación de hardware real de Phala Cloud, mientras que `--live` la compara también con la imagen publicada. `--tdx-measurements` sigue comparando MRTD y RTMR0-2, pero en este caso en formato JSON.

Cada inicio del recopilador registrado en el diario lleva consigo dicha certificación, por lo que `verify --evidence` comprueba cada inicio y la imagen del sistema operativo con la que se ha arrancado. Las revisiones de la aplicación de Phala y las operaciones del CVM sirven como registro del proveedor: una configuración de Docker Compose modificada tras el despliegue hace que el informe no sea válido, y los reinicios se incluyen en la lista para su revisión.

En el panel, selecciona **«Máquina virtual confidencial · Phala Cloud»** en **«Extras»** → **«Servidor 24/7»** y pega una clave API de Phala Cloud; el túnel rápido funciona igual que en Hetzner. Desde la línea de comandos:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` Lee los certificados y las listas de revocación de Intel desde un archivo en lugar de descargarlos de Intel. El DNS de puerta de enlace no está disponible aquí: Phala no tiene un cortafuegos del proveedor para el tráfico saliente.

### Certificado de autenticación

En una implementación de Phala, `verify --report certificate.md` también genera el certificado: un `certificate.html` autónomo y un `certificate.pdf` en formato A4 con el veredicto, la cadena de confianza desde la raíz de Intel hasta la clave del recopilador, una comparación con servidores ordinarios y de alta seguridad, las mediciones junto a los valores calculados a partir de la imagen publicada, quién avala cada parte, la cadena de certificados de Intel, cada comprobación, el registro del proveedor y cómo repetir la verificación. El informe JSON sigue siendo el registro oficial; las páginas lo representan.

El informe está sellado digitalmente con firmas y marcas de tiempo, en el archivo `certificate.seal.json` y en los archivos `.tsq`/`.tsr` que lo acompañan:

| Sello | Qué aporta |
| --- | --- |
| Sello de tiempo electrónico cualificado, `http://tsa.belgium.be/connect` | Marca de tiempo RFC 3161 sobre los bytes exactos de `certificate.json` procedente del proveedor de servicios de confianza cualificado del Gobierno federal belga (FPS Policy and Support, BOSA). Dicha entidad figura como servicio cualificado de sellado de tiempo, con estado «concedido», en la lista de confianza de la UE de Bélgica; la raíz (Belgium Root CA6) y las entradas de la lista, según la versión publicada el 20 de octubre de 2026, están fijadas en `tgwitness/tsa_roots.py`. De conformidad con el artículo 41 del Reglamento (UE) n.º 910/2014, se presume que dicho sello de tiempo es exacto en cuanto a la fecha y la hora, así como en cuanto a la integridad de los datos, en todos los Estados miembros de la UE. |
| Marca de tiempo RFC 3161, FreeTSA | Una segunda marca de tiempo independiente |
| Firma del verificador | Ed25519 sobre una declaración que identifica el SHA-256 del informe y cada marca de tiempo, con la propia clave del verificador (`--sign-with FOLDER`, por defecto `~/.tgwitness/verifier`); el PDF lleva una firma con la misma clave |

`--timestamp URL` (repetible) elige otras autoridades, `--timestamp none` ninguna, `--sign-with
none` deja el sello sin firmar. `check-report` comprueba el hash del informe, la firma del verificador, cada marca de tiempo con respecto a una raíz de confianza y su estado cualificado, así como la firma del PDF. La validez jurídica de un sello de tiempo cualificado fuera de la UE, así como del informe en su conjunto, recae en el tribunal o la autoridad que lo reciba; el sello indica cuándo existía el informe y que no ha sufrido modificaciones.

Una certificación no puede descartar un fallo en el módulo TDX o en el microcódigo de Intel, ni el acceso físico al bus de memoria. Quien controle la aplicación en la cuenta de Phala puede implementar otro «compose»; aparecerá como una nueva revisión con un nuevo hash de «compose». El anfitrión controla la fuente de tiempo de la máquina y la red.

La implementación, la verificación con `--evidence`, los reinicios, la comparación de la imagen del sistema operativo, el certificado sellado digitalmente con firmas y marcas de tiempo y la destrucción se han ejecutado en la propia Phala Cloud; véase [, la ejecución del 4 de noviembre de 2026,](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026).

## Antes de empezar

1. Una zona de Cloudflare, su ID de cuenta y un token de API con permisos para **«Cloudflare Tunnel Edit**», **«Zone Read»** y **«DNS Edit**», proporcionado con `--cloudflare-token-file` o `CLOUDFLARE_API_TOKEN`. Para el verificador: **lectura de Cloudflare Tunnel**, **lectura de DNS** y, para el registro de auditoría, **lectura de la configuración de la cuenta**. Sin un dominio, un [túnel rápido](https://phishdestroy.github.io/TgWitness/es/docs/reference/high-assurance/#quick-tunnel-without-a-domain) no necesita nada de esto.
2. Credenciales de proveedor con acceso de escritura a un proyecto específico; `lock` utiliza lo mismo:

   - Hetzner: token de API con permisos de lectura y escritura;
   - DigitalOcean: token de acceso personal con permiso de escritura;
   - Linode: token de acceso personal con `linodes`, `firewall` y `events` ámbitos de lectura/escritura;
   - Vultr: clave API de una cuenta dedicada o una subcuenta;
   - AWS: se permiten credenciales de IAM `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` y `ec2:RevokeSecurityGroupIngress`.
3. La confirmación que se va a ejecutar. Una etiqueta de lanzamiento se resuelve una sola vez a su confirmación con `git ls-remote`; el servidor solo recibe siempre el commit de 40 caracteres.

## Desde el panel

En tu propio ordenador, en **Extras → Servidor 24/7** se ejecuta lo mismo `deploy` para Hetzner en tres pasos: elige Europa o Estados Unidos, pega un token de Hetzner (lectura y escritura) y, a continuación, revisa el tipo de servidor, el precio mensual, la dirección y la versión que el panel ha encontrado con ese token. No se crea nada hasta que lo confirmes. El panel muestra cada paso tal y como `deploy` se va indicando, y a continuación la dirección, el token del panel y la huella digital de la clave de firma. Sin un dominio, el servidor obtiene un [túnel rápido](https://phishdestroy.github.io/TgWitness/es/docs/reference/high-assurance/#quick-tunnel-without-a-domain) ; **en «Tus servidores» → «Buscar la dirección actual»** se vuelve a consultar tras un reinicio. Para obtener una dirección fija bajo tu propio dominio, abre **«Opcional · tu propio dominio»** y añade un token de Cloudflare (el enlace preparado selecciona «Lectura de zona», «Edición de DNS» y «Edición del túnel de Cloudflare»).

Los tokens se transmiten con cada solicitud desde la pestaña del navegador hasta TgWitness en el mismo ordenador y no se guardan en ningún sitio; el registro de implementación, el cloud-init censurado, el token del panel y, en el caso de un túnel rápido, la clave de dirección se guardan en `deployments/NAME` dentro del directorio de datos. El panel ofrece esto únicamente al administrador principal a través de una conexión directa de bucle invertido (`127.0.0.1`, sin encabezados de proxy ni de túnel); un panel al que se accede a través de una red muestra los comandos en su lugar. La versión por defecto es la etiqueta de lanzamiento del panel en ejecución, resuelta a través de la API de GitHub. La ubicación, el tipo de servidor y el precio proceden de la API de Hetzner: `cpx22` si está disponible; de lo contrario, el tipo x86 más barato con al menos 2 GB de memoria.

## Túnel rápido sin dominio

`--quick-tunnel` sustituye a `--zone`, `--cloudflare-account` y `--panel-host`; no interviene ninguna cuenta ni token de Cloudflare:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

En el servidor, Cloudflared abre un [túnel rápido](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) hacia el panel: una dirección aleatoria `https://….trycloudflare.com` que cambia cada vez que se reinicia cloudflared o el servidor. Un pequeño servicio en el servidor publica cada dirección en un tema aleatorio de ntfy.sh , firmada (HMAC-SHA256) con una clave que solo contiene el directorio de implementación (`address-key.txt`), y la repite cada tres horas porque ntfy.sh conserva las publicaciones durante 12. `deploy` y **«Find the current address»** solo aceptan publicaciones firmadas, por lo que una publicación falsificada no puede enviarte a ti, ni a tu token del panel, a la dirección de otra persona. El tema figura en el registro y en el cloud-init publicado: quienquiera que los tenga puede leer la dirección actual, que sigue solicitando el token del panel. El servidor no mantiene ningún puerto de entrada en ningún caso.

Un verificador no dispone de clave de dirección, y cualquiera que lea el tema puede publicar en él. Por lo tanto, el recopilador también publica la propia dirección, firmada con su propia clave Ed25519, y `verify` toma la publicación más reciente firmada por la clave del recopilador en el registro de implementación; las publicaciones se ordenan según la hora en que ntfy.sh las recibió, no según la hora que indican. Un recopilador anterior a este cambio no firma nada, y `verify` toma entonces la publicación más reciente y así lo indica en la comprobación de `statement`; una publicación falsificada solo puede hacer que dicha comprobación falle, ya que la dirección debe seguir respondiendo con la clave del recopilador.

Costes: ninguna cuenta de Cloudflare mantiene registros de un túnel rápido, por lo que `verify` informa de que el túnel, el conector y la comprobación de DNS no están disponibles, y el resultado es, en el mejor de los casos, `incomplete` (en Phala Cloud, en cambio, la comprobación se supera: el conector se ejecuta dentro de la configuración de Docker Compose medida); los registros del proveedor, el cortafuegos, la declaración firmada, las mediciones del host y la comparación del instalador se comprueban como de costumbre. La comparación de bytes con el instalador de referencia requiere una confirmación desplegada que ya conozca `--quick-tunnel`; una comprobación de la versión 0.7.0 compila el instalador del dominio e informa de la diferencia. Cloudflare no ofrece garantía de disponibilidad para los túneles rápidos, permite 200 solicitudes en tránsito y no admite eventos enviados por el servidor (Server-Sent Events), por lo que es posible que las actualizaciones en tiempo real del panel (versiones posteriores a la 0.7.0) no lleguen a través de uno de ellos y sea necesario recargar la vista; esa parte aún no se ha probado. Para un caso que deba funcionar de forma fiable, utilice su propio dominio.

## Implementar

Echa un vistazo primero a todo lo que se va a enviar. `plan` No realiza ninguna solicitud al proveedor ni a Cloudflare:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

A continuación, realice la implementación con las mismas opciones y las credenciales:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Tipos de servidor para empezar: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` y `--image` por defecto, Ubuntu 24.04 de cada proveedor en una región europea.

`--repository` Toma la confirmación de otro repositorio Git https, sin credenciales en la URL (por defecto `https://github.com/phishdestroy/TgWitness.git`). `deploy` también acepta `--out` para otro directorio de implementación (por defecto `deployments/NAME`; se rechaza un directorio que ya contenga una implementación) y `--wait`, los minutos que hay que esperar a la declaración firmada del recopilador: de 1 a 240, por defecto 20, o 60 para `generic`.

El comando:

1. crea un túnel de Cloudflare cuyo ingreso reenvía el nombre de host del panel al propio panel y, si se ha especificado, el nombre de host de Witness a `/api/witness/head` y `/api/assurance` solo;
2. crea registros CNAME proxy para esos nombres de host, rechazando los nombres que ya existen;
3. crea un cortafuegos de proveedor sin reglas de entrada y un servidor detrás de él sin clave SSH, sin copias de seguridad, sin agente de consola y con cloud-init que enmascara el SSH, bloquea el acceso de root, instala `cloudflared`, recupera exactamente el commit, lo comprueba e inicia TgWitness como un servicio de systemd reforzado;
4. espera la declaración firmada del recopilador y comprueba que en ella se mencione este servidor y el hash de este cloud-init.

`deployments/case-2026-11/` A continuación, contiene:

| Archivo | Índice | ¿Compartir? |
| --- | --- | --- |
| `deployment.json` | ID, hash, las llamadas a la API realizadas (método, ruta, estado) y la primera declaración firmada | Sí, con el verificador |
| `cloud-init.redacted.yaml` | El comando exact cloud-init con sus dos claves secretas sustituidas por `REDACTED` | Sí |
| `panel-token.txt` | El token del panel | No |

La contraseña de root del proveedor, el token del túnel y el token del panel nunca se escriben en `deployment.json`. Publica la huella digital del recopilador que aparece al final a través de un canal que no controles tú solo, por ejemplo, un canal de testigos o un mensaje al destinatario.

Inicia sesión en Telegram en `https://case.example.org` con el token del panel, tal y como se indica en la [guía de la cuenta](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/). Las acciones del panel se registran en el diario firmado; no se trata de sesiones SSH. Un [testigo](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/) puede consultar `https://case-witness.example.org`.

No hay SSH: si falla la inicialización, el recopilador nunca responde. Elimina el servidor y vuelve a implementarlo, o utiliza una implementación de depuración para encontrar la causa.

### Secretos en los datos de usuario

El cloud-init contiene dos claves secretas: el token del panel y el token del túnel de Cloudflare. La clave de firma no se encuentra entre ellas; se crea en el servidor. Hetzner, DigitalOcean y Linode no devuelven datos de usuario a través de su API. Vultr los devuelve a cualquier clave que pueda leer la instancia, y EC2 a través de `DescribeInstanceAttribute`. Para AWS, proporciona al verificador únicamente las tres acciones de la tabla, nunca `ec2:Describe*`. En el caso de Vultr, supongamos que la clave del verificador puede leer ambos tokens. Un token de túnel permite a alguien ejecutar un segundo conector: `verify` informa de cualquier conector que no esté en el servidor, y las declaraciones del recopilador no pueden falsificarse de esa manera porque cada una firma un desafío nuevo. Con `--quick-tunnel` el segundo secreto es, en cambio, la clave de dirección: quienquiera que la lea puede publicar una dirección falsa que el panel aceptaría.

La declaración pública del recopilador omite la dirección del servidor y las fuentes de los inicios de sesión; ambas permanecen en el registro firmado.

## Depuración de la implementación y bloqueo

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` mantiene SSH para una clave procedente de una dirección o una red pequeña, como máximo un /24 para IPv4 o un /48 para IPv6. `KEY` Ya está registrado con el proveedor: el nombre o el ID de una clave SSH en el proyecto Hetzner, el ID o la huella digital de una clave SSH en el equipo de DigitalOcean, un nombre de usuario de Linode cuyas claves SSH de perfil se añaden a root, el ID de una clave SSH en la cuenta de Vultr o el nombre de un par de claves de EC2 en la región. Estas opciones no se aplican a `generic`. Dicha implementación se registra como `debug` y **nunca** se clasifica como de alta seguridad. Cuando hayas terminado, ejecuta `sudo tgwitness-lock` como último comando de la última sesión SSH y, a continuación:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

El cortafuegos pierde todas las reglas de entrada. A continuación, los informes muestran cuándo se permitió el SSH y cuándo se cerró; esa ventana permanece visible.

## Eliminar una implementación

`destroy` Elimina el servidor y su cortafuegos, identificados mediante la etiqueta de la implementación, de modo que una implementación que haya fallado a mitad de camino también se elimine; a continuación, se eliminan los registros DNS que apuntan a su túnel, así como el propio túnel. El registro del servidor y la clave de firma se eliminan junto con él: exporta primero las pruebas. El registro permanece, marcado `removed`, con las llamadas a la API de la eliminación.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

La eliminación a través de la API está implementada para Hetzner. En el caso de otros proveedores `destroy` se detiene antes de eliminar nada y especifica la etiqueta que se va a eliminar en la consola del proveedor. Un servidor instalado manualmente (`generic`) solo pierde su túnel y sus registros DNS. Una implementación rápida del túnel no necesita token de Cloudflare: su túnel termina en el servidor, y sus publicaciones caducan en ntfy.sh en un plazo de 12 horas.

## Cualquier servidor (autocertificado)

`--provider generic` Es para un servidor comprado o instalado manualmente. `deploy` crea el túnel y el DNS, escribe `install.sh` (privado) y `install.redacted.sh` (para publicar), y espera. Copia `install.sh` en un servidor Ubuntu 24.04 recién instalado y ejecútalo allí:

```
sudo bash install.sh
```

Registra el servidor tal y como estaba (inicios de sesión, cuentas, `authorized_keys`, sockets de escucha, servicios, tareas programadas, paquetes), instala la confirmación, activa el cortafuegos del host, se elimina a sí mismo, enmascara el SSH y finaliza la sesión. El informe de un servidor de este tipo es, en el mejor de los casos, **AUTOATESTADO**: quienquiera que ejecutara el instalador ya tenía privilegios de root antes de hacerlo, y no hay ningún registro del proveedor disponible para el verificador. Aun así, es mejor que un servidor sin explicación: el inventario, el hash del instalador y todos los inicios de sesión posteriores están firmados.

## Verificar

El verificador necesita `deployment.json`el instalador publicado, credenciales de solo lectura y, a ser posible, una copia del commit y una prueba ZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

El verificador solicita en ese momento todos los datos de los proveedores y de Cloudflare; el registro solo proporciona los ID sobre los que se debe preguntar. El código de salida es 0 para **APROBADO**, 1 para **FALLO** y 2 para **REVISIÓN**, **INCOMPLETO** o **AUTOCERTIFICADO**. `--fingerprint` debería proceder de un canal independiente; sin él, la clave se compara únicamente con el registro del operador. `python verify.py` Sigue verificando las pruebas ZIP por sí mismo, tal y como se describe en [«Pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/)».

Las acciones del proveedor se clasifican: la creación y el inicio en los 30 minutos siguientes a la creación se aprueban; la consola, el rescate, el restablecimiento de contraseña, la reconstrucción, la ISO, las imágenes, las instantáneas, las copias de seguridad, Systems Manager, EC2 Instance Connect y las aperturas del cortafuegos se rechazan; las acciones relacionadas con la alimentación y cualquier otra acción no prevista se marcan para su revisión. Una acción desconocida nunca pasa desapercibida.

## Informe para la entrega de pruebas

`--report report.md` redacta el informe en Markdown y `report.json` junto a él:

1. resultado, huella digital de la clave del recopilador, implementación, proveedor, confirmación, servidor, cortafuegos, túnel;
2. cada comprobación con su estado y su origen (API del proveedor, API de Cloudflare, extracto del recopilador, registro de pruebas);
3. el registro del proveedor con la evaluación de cada acción y, cuando el proveedor lo registra, el autor;
4. los puntos finales de Cloudflare que contienen las conexiones del túnel, la configuración y el registro de auditoría;
5. la declaración firmada del recopilador;
6. lo que el informe establece y lo que no;
7. los comandos para reproducirlo y el SHA-256 de cada archivo que se le proporcionó.

Entrega el informe, `report.json`, `deployment.json`el instalador publicado y las pruebas ZIP. Elabora el informe con antelación: los registros de los proveedores se conservan durante un tiempo limitado.

## Cloudflare como testigo externo

Todo lo que aparece aquí es opcional. El servidor sigue funcionando aunque no se disponga de una cuenta de Cloudflare, y dos de estas opciones funcionan actualmente:

| ¿Qué? | Qué muestra | En TgWitness |
| --- | --- | --- |
| Túnel rápido o el túnel de tu dominio | Solo se puede acceder al panel a través del túnel | El asistente del servidor; véase más arriba. |
| drand relay `drand.cloudflare.com` | Los registros posteriores a una ronda de drand son más recientes que este: el diario se fue escribiendo sobre la marcha. | modo de pruebas, **Más testigos**, sin cuenta ([formato](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| Notificaciones sobre el estado del túnel | cuando el túnel estaba inactivo, por correo electrónico o mediante un webhook de Cloudflare | Configúralos en el panel de control de Cloudflare |
| DNS de Gateway (`--gateway-dns`, o **Cloudflare Gateway DNS** en el asistente) | cada nombre que el servidor consultó, respondido por Cloudflare a través de TLS; el cortafuegos de Hetzner impide que el DNS acceda a cualquier otra cosa; si una política de Gateway podría reescribir las respuestas | Hetzner, plan Zero Trust gratuito, sin dominio; `verify` comprueba el cortafuegos, la ubicación, el registro de actividades, las políticas, las consultas del servidor y el registro de auditoría; el modo de evidencia copia el registro en el diario |
| Puerta de enlace con Cloudflare: un cliente One en el servidor, un cortafuegos de salida que solo permite el acceso a Cloudflare | cada conexión que ha establecido el servidor, no solo las de DNS | Aún no está desarrollado |
| Acceso frente al panel | quién se ha conectado al panel y cuándo | No está implementado: requiere un dominio propio |
| Registro de comandos SSH | cada comando en una sesión de depuración | Aún no está desarrollado |

Logpush, que mantendría la copia propia de Cloudflare en R2, es una función de Enterprise: en el plan gratuito , Cloudflare responde `logpush is not enabled for this account`. Su registro de Gateway se conserva allí durante 24 horas, por lo que el «modo de evidencia» lo copia en el diario firmado (**el registro de Cloudflare Gateway de las consultas DNS de este servidor**, un token de solo lectura con «Account Analytics Read»).

Sin un plan Zero Trust, una cuenta tiene una única ubicación DNS. Cuando Cloudflare rechaza otra, el servidor comparte la existente y sus consultas se distinguen por su dirección; ese filtro también necesita Zero Trust PII Read, y `destroy` deja una ubicación compartida. Una consulta de registro abarca como máximo tres horas, por lo que la copia y la `verify` lectura del día en intervalos de tres horas.

El DNS de la puerta de enlace se encarga del resolutor del sistema. El DNS sobre HTTPS en el puerto 443 hacia otro resolutor, así como las conexiones a direcciones que no aparecen en ningún registro (como los centros de datos de Telegram, por ejemplo), no figuran en su registro.

Cloudflare no puede ver el interior del cifrado de Telegram, otros dispositivos de la cuenta de Telegram (la lista de dispositivos del modo «evidence» los registra desde el lado de Telegram) ni el hipervisor del proveedor.

## Reading the deployment result

For an ordinary VM，the provider controls the host infrastructure，and local inventory is checked alongside provider records．For Intel TDX，the verifier additionally checks the hardware quote，collector binding，compose and OS measurements．Read the individual results to see which checks passed or were unavailable．

Historical firewall detail depends on the provider；Linode retains rule versions． The [validation record](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/) lists tested deployments and remaining live checks，and [verification scope](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope) connects these environment checks to archive acquisition and integrity．
