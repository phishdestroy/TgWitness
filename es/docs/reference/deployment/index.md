# Implementación

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/deployment/

Ejecute TgWitness como servicio en Windows, Linux, macOS o Docker, a través de HTTPS, con copias de seguridad y actualizaciones.

**Inglés** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [Ucraniano](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [Portugués (Brasil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [Chino simplificado](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## Elija una instalación

Para obtener el paquete portátil, extraiga «`TgWitness-<version>-windows-amd64-portable.zip`» de GitHub Releases. Para los demás métodos, descargue y extraiga el archivo ZIP con el código fuente o clone el repositorio; a continuación, ejecute lo siguiente desde el directorio del proyecto:

| Instalación | Inicio | ¿Funciona en segundo plano? |
| --- | --- | --- |
| Paquete portátil para Windows | `TgWitness.cmd` | No; mantenga la ventana abierta. |
| Nativo de Windows | `Start.cmd` | No; utilice la tarea de inicio de sesión opcional para su ejecución en segundo plano. |
| Compatible con Linux y macOS | `sh start.sh` | No; utilice systemd/launchd para el funcionamiento en segundo plano. |
| Docker en cualquier servidor compatible | `docker compose up -d --build --wait` | Sí, mientras el daemon de Docker esté en ejecución. |
| Ayuda para Docker en Windows | `scripts\Docker.cmd` | Sí; el helper espera a que el servidor web esté operativo. |
| Ayuda para Docker en Linux/macOS | `sh scripts/docker-start.sh` | Sí; el helper espera a que el servidor web esté operativo. |

Para un servidor en la nube que un tercero pueda comprobar —creado a través de la API del proveedor, sin SSH, al que solo se puede acceder a través de un túnel de Cloudflare—, consulte [la implementación de alta seguridad](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md).

El inicio nativo crea un `.venv` privado e instala las dependencias fijadas. Docker las compila dentro de la imagen, sin necesidad de Python en el host. La configuración inicial requiere acceso a Internet. Cuando no se encuentra Python 3.11 o superior, `Start.cmd` solicita permiso antes de instalar Python 3.12 para el usuario actual de Windows (mediante winget; en caso contrario, el instalador de python.org tras comprobar su firma de la Python Software Foundation); nunca solicita privilegios de administrador. Docker y los servicios del sistema operativo siguen siendo requisitos previos.

Las instalaciones nativas y portátiles utilizan «`data/live`» dentro de su carpeta. Docker utiliza el volumen denominado «`tgwitness-data`» en «`/data`». Se trata de instalaciones independientes hasta que se migre deliberadamente el directorio de datos completo. No espere que un nuevo contenedor de Docker detecte las cuentas nativas de forma automática.

## Requisitos de instalación

La instalación nativa requiere Python 3.11 o posterior con `venv` y `ensurepip`, acceso a Internet para la instalación de la primera dependencia y un directorio de proyecto con permisos de escritura para `.venv`. El panel incluido no necesita Node.js ni compilación de interfaz de usuario. Ejecute el lanzador desde su cuenta habitual del sistema operativo; TgWitness no requiere privilegios de administrador ni de root.

- **Windows:** `Start.cmd` comprueba `py -3`, luego `python`, a continuación las carpetas de instalación predeterminadas por usuario y en «Archivos de programa», y requiere la versión 3.11 o posterior. Si ninguna de estas opciones funciona, ofrece la instalación automática por usuario descrita anteriormente. `py -3 start.py` también funciona. El paquete portátil no necesita Python en absoluto.
- **Linux:** `start.sh` prueba `python3.13`, `python3.12`, `python3.11`, `python3` y `python`, y muestra el comando de instalación para apt, dnf, pacman, zypper, apk o Homebrew cuando ninguno cumple los requisitos. Las instalaciones en Debian/Ubuntu pueden requerir el paquete `python3-venv` correspondiente al intérprete seleccionado. La versión predeterminada más antigua de Python de una distribución debe sustituirse o complementarse con Python 3.11 o superior.
- **macOS:** instale una distribución actual de Python 3.11 o superior; no dé por sentado que un intérprete proporcionado por el sistema operativo cumple los requisitos. Utilice `python3 start.py` desde el directorio del proyecto.
- **Docker:** utilice Docker Engine/Desktop con Compose v2.20 o una versión posterior. Docker Desktop debe utilizar contenedores de Linux en Windows. El contenedor instala sus propias dependencias de Python; el sistema anfitrión no necesita una instalación independiente de Python.

Utilice almacenamiento local persistente para el directorio de datos. Planifique la capacidad teniendo en cuenta los mensajes, los archivos multimedia, el crecimiento del WAL, las exportaciones y las copias de seguridad; no existe una especificación mínima universal basada en pruebas de disco o RAM para todas las cargas de trabajo. Las arquitecturas de CPU y las versiones de Python que carezcan de ruedas de dependencias compatibles pueden requerir herramientas de compilación adicionales y su propia validación. «Portátil» no implica compatibilidad universal con todos los sistemas operativos ni con todo el hardware.

Se ha verificado localmente en Windows 11/Python 3.12. Se proporcionan las definiciones para Linux, macOS y contenedores, así como la infraestructura de integración continua (CI), pero no se han ejecutado en este servidor de desarrollo. Consulte [el archivo VERIFICATION.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/) para conocer el alcance exacto.

## Ordenador local

Utilice `Start.cmd` en Windows o `sh start.sh` en Linux/macOS. `scripts\Setup.cmd` o `sh start.sh --setup-only` prepara el entorno. El lanzador instala las dependencias la primera vez que se utiliza; los ejecuciones posteriores reutilizan el entorno. Se necesita acceso a Internet para la configuración y la recopilación de datos de Telegram, pero la consulta de registros existentes y la creación de exportaciones funcionan sin conexión.

Ejecute «`python start.py --check`» tras la configuración para comprobar las dependencias locales, Ed25519, el almacenamiento, la configuración de claves y la dirección de escucha sin iniciar un colector. Utilice `--json` para obtener una salida estructurada. Introduzca los comandos `--data-dir`, `--host` y `--port` según corresponda. La comprobación no instala paquetes, no crea un registro ni se conecta a Telegram; no se trata de una verificación de integridad ni de cobertura. El inicio verifica por separado los registros existentes. `python start.py --help` también evita la instalación.

Opciones:

Tras ejecutar start.py, ejecute los comandos auxiliares con `.venv\Scripts\python.exe` en Windows o `.venv/bin/python` en Linux/macOS, o bien active primero dicho entorno. Los ejemplos `python -m ...` que figuran a continuación dan por hecho que el entorno está activo.

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

Variables de entorno: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN. TGWITNESS_VAULT_KEY_FILE selecciona el modo de clave externa para una nueva instalación; véase más abajo. TGWITNESS_TOKEN, si se proporciona, debe contener al menos 24 caracteres; utilice un valor aleatorio cifrado. Sin él, la aplicación genera un token aleatorio de 256 bits en el archivo panel-token.txt. La sustitución de variables de entorno no sobrescribe dicho archivo. Reinicie el sistema para rotar las credenciales.

Exactamente un proceso puede ser propietario de un directorio de datos. Un bloqueo de archivos multiplataforma del sistema operativo evita escrituras simultáneas accidentales. Utilice un único trabajador de Uvicorn. El panel puede gestionar cualquier número de espacios de trabajo, con directorios de espacios de trabajo adicionales en profiles/<id>/. Para instancias de servicio independientes, utilice directorios y puertos distintos. Los archivos WAL de SQLite deben almacenarse en un almacenamiento local persistente, no en un sistema de archivos de red. No comparta un mismo volumen entre réplicas.

## Paquete portátil para Windows

Cada versión de GitHub incluye `TgWitness-<version>-windows-amd64-portable.zip` y su `.sha256`. Contiene el entorno de ejecución oficial de Python 3.12 incrustable de python.org (suma de comprobación fijada en `tools/build_portable.py`), TgWitness y sus dependencias fijadas, así como tres lanzadores:

| Archivo | Objetivo |
| --- | --- |
| `TgWitness.cmd` | Inicie el panel; se transmiten opciones adicionales, p. ej., `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | Inicie la demostración sintética en `data\demo` |
| `TgWitness-Check.cmd` | Ejecute la comprobación de preparación sin iniciar el proceso |

Descomprima todo el archivo en una carpeta en la que se pueda escribir, como «`Documents\TgWitness`»; no lo ejecute desde dentro del archivo ZIP ni desde «Archivos de programa». El entorno de ejecución utiliza una ruta de módulos aislada, por lo que otras instalaciones de Python y «`PYTHONPATH`» no le afectan. Los datos permanecen en la carpeta «`data`» del paquete. Para actualizar, detenga TgWitness, extraiga la nueva versión a una nueva carpeta y copie la carpeta «`data`» en ella.

Compílelo usted mismo en Windows de 64 bits con Python 3.12:

```
python tools/build_portable.py
```

El generador verifica la suma de comprobación en tiempo de ejecución, instala las dependencias restringidas en el paquete, ejecuta la comprobación de preparación con el intérprete integrado y graba el archivo ZIP y la suma de comprobación en `dist/`.

## Contenedor

```
docker compose up -d --build --wait
```

Esto crea un volumen persistente con nombre para /data. El puerto web está asignado a 127.0.0.1:8787. El proceso se ejecuta con el UID 10001, con capacidades restringidas, un sistema de archivos raíz de solo lectura y los directorios /data y /tmp con permisos de escritura. `--wait` comprueba el estado del servidor web antes de devolver un resultado; no establece la autorización ni la entrega de Telegram. Los ayudantes proporcionados utilizan un tiempo de espera de disponibilidad de 180 segundos tras la compilación. Las descargas iniciales de dependencias pueden tardar más tiempo.

Ambos archivos «Compose» base utilizan el nombre de proyecto «`tgwitness`», por lo que extraer una nueva versión a otro directorio no selecciona automáticamente un nuevo volumen de datos. Mantenga solo una implementación activa para ese proyecto. Para instalaciones independientes, utilice un « `docker compose -p NAME ...`» único y un puerto de host diferente, y conserve ambos en las actualizaciones. En el caso de una implementación anterior que utilice un nombre de proyecto diferente, continúe utilizando su nombre original junto con «`-p`»; «`docker compose ls`» muestra los proyectos existentes.

Copie `deploy/env.example` en `.env` y modifique `TGWITNESS_PORT` para utilizar un puerto de bucle cerrado diferente. Por ejemplo, `TGWITNESS_PORT=8788` expone el panel en `http://127.0.0.1:8788`; el contenedor sigue escuchando en el puerto 8787. `.env` se omite en Git.

Obtenga el token inicial:

```
docker compose exec tgwitness cat /data/panel-token.txt
```

Comandos útiles:

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` reinicia el colector tras un fallo o un reinicio del daemon de Docker . En un servidor Linux, active Docker al arrancar utilizando el gestor de servicios de su distribución , normalmente `sudo systemctl enable --now docker`. En Windows/macOS, active la configuración «Iniciar al iniciar sesión» de Docker Desktop. El cierre de sesión, el modo de suspensión o la detención del puede interrumpir la recopilación. Un contenedor detenido explícitamente permanece detenido hasta que lo vuelva a iniciar.

El volumen /tmp tiene un límite de 512 MiB en la configuración de ejemplo. La construcción de la exportación utiliza, en su lugar, el `temporary-exports/` de cada espacio de trabajo en el directorio persistente /data. Reserve espacio allí para exportaciones simultáneas, el crecimiento del diario/WAL, archivos multimedia y copias de seguridad. El lanzador utiliza el archivo deploy/constraints.txt para fijar las versiones de las dependencias de tiempo de ejecución que cumplen los requisitos. Los servidores Docker y de alta seguridad se instalan a partir de deploy/requirements.lock y deploy/build.lock con pip --require-hashes: cada archivo de paquete debe coincidir con un SHA-256 registrado en la confirmación, por lo que se rechaza cualquier archivo sustituido en PyPI o en un servidor espejo. La imagen base de Python y los paquetes del sistema operativo siguen requiriendo una certificación de versión independiente.

No utilice el comando «docker compose down -v» a menos que tenga la intención de destruir el registro y las claves. El estado del contenedor indica la disponibilidad del servidor web, no que la captura de Telegram se haya realizado con éxito. Compruebe el estado del colector del panel, el «heartbeat», los errores y los eventos de cobertura.

### Perfil de testigo independiente

El servicio opcional «`witness`» ejecuta un [testigo independiente](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/) en su propio contenedor, con su propia clave y registro en el volumen «`witness-data`» y únicamente un token de testigo de solo lectura para el recopilador. Cree el token en la página **«Witness»** del panel, añádalo junto con un token de bot y un canal a «`.env`» y, a continuación, inicie el perfil:

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

El servicio accede al recopilador dentro de la red Compose en `http://tgwitness:8787` (`TGWITNESS_WITNESS_COLLECTOR` lo anula; por ejemplo, `/profiles/<workspace ID>` para otro espacio de trabajo). Para un testigo en un servidor independiente, gestionado por otra persona, utilice `deploy/compose/compose.witness.yaml` allí, con `TGWITNESS_WITNESS_COLLECTOR` configurado en la dirección HTTPS del recopilador; dicho archivo contiene únicamente el testigo.

## Instalar una imagen publicada

Esto estará disponible tras completar con éxito el [flujo de trabajo de lanzamiento](https://phishdestroy.github.io/TgWitness/es/docs/reference/deployment/#automated-github-releases) y la configuración pública del paquete GHCR. El propietario o el nombre del repositorio no están codificados de forma fija en este árbol de código fuente. Utilice la imagen que se muestra en el resumen del flujo de trabajo de dicha versión.

Copie `deploy/env.example` en `.env`. Establezca `TGWITNESS_IMAGE` en la versión publicada, utilizando la ruta del repositorio **en minúsculas**; por ejemplo:

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.1
TGWITNESS_PORT=8787
```

Ejecute este archivo por sí solo, en lugar de `compose.yaml`:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

No se necesita compilación del código fuente, Python ni compilador en el servidor. El flujo de trabajo de lanzamiento está orientado a contenedores Linux AMD64 y ARM64, incluida la máquina virtual Linux de Docker Desktop. Utilice una etiqueta de versión o «`ghcr.io/owner/repository@sha256:...`» del resumen del flujo de trabajo. No se ha configurado ninguna etiqueta «`latest`» móvil ni ninguna actualización automática de la aplicación. Las variantes de imagen y código fuente utilizan el mismo volumen de datos cuando su nombre de proyecto coincide.

## HTTPS automático en un servidor

Utilice un servidor con Docker, un dominio bajo su control y almacenamiento local persistente. Dirija los registros A/AAAA del dominio hacia el servidor; publique el registro AAAA únicamente si se accede a él a través de IPv6. Permita el tráfico entrante por los puertos TCP 80 y 443, así como el tráfico saliente de DNS/HTTPS para la emisión de certificados. Estos puertos no deben estar ya ocupados por otros servicios.

Copie `deploy/env.example` en `.env` y establezca un nombre de host, sin esquema ni ruta:

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

Inicie la compilación del código fuente con la superposición HTTPS:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

En el caso de una imagen publicada, utilice `deploy/compose/compose.image.yaml` como primer archivo. Conserve ambos argumentos `-f` para futuros comandos de estado, registros, actualización y parada.

Caddy obtiene y renueva un certificado, redirige el tráfico HTTP a HTTPS y reenvía las solicitudes al colector en la red privada de Compose. El estado del certificado cuenta con su propio volumen persistente. El puerto de host directo del colector permanece restringido exclusivamente al bucle de retorno. La configuración de Caddy proporcionada no habilita el registro de accesos.

Abra `https://watch.your-domain.org` e introduzca el token del panel. La comprobación de disponibilidad no confirma la emisión del certificado ni la accesibilidad externa. Si HTTPS no está disponible, compruebe el DNS, las reglas del cortafuegos y:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

La imagen de Caddy proporcionada lleva la etiqueta «`2-alpine`». Al ejecutar «pull», se actualiza dicha imagen; fije un resumen comprobado en su implementación si necesita versiones fijas de la infraestructura.

## Actualizaciones y copias de seguridad

Conserve el nombre del proyecto «Compose» y el volumen de datos en todas las actualizaciones. En primer lugar, detenga el recopilador y realice una copia de seguridad completa. Para la implementación predeterminada basada en el código fuente:

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Utilice cada vez un nuevo destino de copia de seguridad, fuera del repositorio, y protéjalo como material de acceso a la cuenta. La ruta de ejemplo es meramente ilustrativa; utilice su propia ubicación privada para la copia de seguridad. Copie todo el directorio, incluidos los archivos ocultos, todos los espacios de trabajo, las claves, los registros y los archivos multimedia. Realice una copia de seguridad por separado de la clave maestra de la bóveda externa, si está configurada. Un archivo ZIP de pruebas no es una copia de seguridad de la aplicación que se pueda restaurar. En el caso de HTTPS, conserve también los volúmenes de Caddy si necesita mantener el estado de su certificado o cuenta.

Para una implementación desde el código fuente, obtenga los archivos de la nueva versión y ejecute:

```
docker compose up -d --build --wait
```

Para la implementación de una imagen, cambie `TGWITNESS_IMAGE` por la versión deseada y, a continuación, ejecute:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Utilice también los archivos «Compose» de su instalación para los comandos «stop» y «copy» anteriores. Mantenga «`.env`», la configuración personalizada y el mismo nombre de proyecto. «`down`» conserva los volúmenes con nombre; «**`down -v`**» **los elimina**. No copie «`.venv`» entre sistemas operativos o versiones de Python. Para actualizaciones nativas, detenga TgWitness, realice una copia de seguridad de todo su directorio de datos, sustituya los archivos fuente y ejecute «`python start.py --setup-only`» antes de iniciarlo.

Compruebe el acceso al panel, la identidad de la cuenta, el estado de observación y la cobertura tras una actualización. Al reiniciar no se recuperan las actualizaciones de Telegram que se hayan perdido. Una restauración a una versión anterior puede requerir la copia de seguridad previa a la actualización si una versión futura cambia los formatos de almacenamiento.

## Publicaciones automatizadas en GitHub

El [flujo de trabajo de lanzamiento](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml) estará listo para su uso una vez que este proyecto se haya subido a un repositorio de GitHub con Actions habilitado. Se ejecuta cuando se **publica** un lanzamiento en GitHub, incluida una versión preliminar. Los borradores y las subidas de etiquetas por sí solos no publican paquetes.

1. Establezca la versión del paquete y el registro de cambios; a continuación, publique una versión etiquetada con «`v`» más la versión exacta de «`pyproject.toml`», como por ejemplo «`v0.7.1`».
2. El flujo de trabajo valida la etiqueta y ejecuta las comprobaciones compartidas de Python para Windows/Linux/macOS, del navegador «general/account-import/QR», del paquete fuente y de Docker. También se lleva a cabo una instalación nativa nueva en los tres sistemas operativos utilizando Python 3.12.
3. Una vez superadas esas comprobaciones, se realiza una prueba de funcionamiento de una imagen ARM64 en QEMU, se publican las imágenes AMD64/ARM64 en `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>`, y se adjuntan el archivo ZIP con el código fuente y el paquete Python wheel junto con sus archivos SHA-256 adjuntos. El archivo ZIP portátil para Windows es exactamente el mismo artefacto que se ha probado en el flujo de trabajo de comprobaciones; el flujo de trabajo de lanzamiento descarga y publica ese artefacto y su suma de comprobación.
4. Una tarea final vuelve a descargar los tres paquetes publicados y verifica sus sumas de comprobación. A continuación, publica `SHA256SUMS.txt` y `RELEASE-MANIFEST.json`, registrando la versión, la revisión del código fuente y los tamaños de los recursos. Las subidas no sobrescriben los recursos de la versión existentes.
5. Tras la primera publicación, abra la configuración del paquete GHCR y establezca la visibilidad en **«Pública»** si se pretende realizar descargas anónimas de imágenes. Un repositorio de código fuente público por sí solo no garantiza que el paquete del contenedor sea público. Las políticas de la organización deben permitir la publicación del paquete. El flujo de trabajo utiliza `GITHUB_TOKEN`; no deben incluirse en el repositorio contraseñas de registro ni credenciales de VPS.

El éxito del flujo de trabajo remoto no se ha confirmado mediante esta preparación local. La emulación de ARM64 es una prueba preliminar, no una validación en hardware nativo ni en Telegram en entorno real. Esto automatiza la creación de paquetes de lanzamiento; para iniciar un servidor sigue siendo necesario el comando «Compose» y sus requisitos previos de dominio/host. Los servidores existentes no se actualizan ni se reinician de forma silenciosa cuando se publica una versión.

## Servidor remoto

Mantenga el servicio vinculado al bucle de retorno y utilice un túnel SSH, o bien termine la conexión HTTPS en un proxy inverso. El archivo Compose base es de uso exclusivamente local; la superposición opcional « `deploy/compose/compose.https.yaml`» proporciona Caddy para un dominio configurado. Mantenga el token de portador fuera de las URL y de los registros del proxy. Un proxy inverso debe limitar el tamaño de las solicitudes y la frecuencia de conexión. No exponga el protocolo HTTP sin cifrar a Internet.

En [la carpeta «deploy/»](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) se proporcionan ejemplos para systemd, una tarea de inicio de sesión en Windows, un agente de usuario de macOS y Caddy. Revise y adapte sus rutas antes de la instalación. Se trata de plantillas, no de configuraciones de plataforma ejecutadas localmente. El lanzador estándar no registra ningún servicio ni tarea en segundo plano.

En Windows, al iniciar `pythonw.exe` sin ventana, los diagnósticos de inicio y del servidor se almacenan en `logs/server.log`, dentro del directorio de datos (5 MiB por archivo, dos copias de seguridad rotativas). Las ejecuciones desde la consola conservan los registros de la misma. El registro de acceso HTTP está desactivado en ambos modos. Proteja los registros junto con el directorio de datos y revíselos antes de compartirlos.

## Reinicio y lagunas

Se conserva el último estado de observación solicitado. Si la observación estaba activa, al iniciar la aplicación se intenta volver a conectarse y reanudar las fuentes seleccionadas. La pausa manual anula esa intención. Se registra cualquier reinicio fallido y se muestra en el panel.

StringSession conserva la autorización, pero no el estado duradero de las actualizaciones o entidades de Telethon. Los diálogos se recargan al inicio. Telegram/Telethon pueden recuperar algunas interrupciones de transporte mientras se ejecutan, pero TgWitness no garantiza una reproducción duradera tras los reinicios del proceso. Cada inicio registra el encabezado del registro anterior y el límite de desconexión. El monitor comprueba la conectividad cada 10 segundos y añade un pulso de **vida** cada minuto (**Parámetros → Registro de actividad cada**). Pueden pasarse por alto breves interrupciones; un canal de transporte conectado no garantiza la entrega completa de las actualizaciones. Las instantáneas son observaciones explícitas del historial actual, nunca una reparación de lagunas.

La cola de archivos multimedia se almacena en la base de datos SQLite de cada espacio de trabajo. Un mensaje y su tarea se confirman de forma atómica. Las tareas en ejecución que se interrumpen se recuperan para volver a intentarlas al reiniciar. Cada descarga tiene un tiempo de espera base de 120 segundos, más el tiempo correspondiente a su tamaño a una velocidad de 256 KiB/s, y un límite de 1 a 2.000 MiB por tipo de archivo adjunto; el tiempo de espera, la velocidad y los reintentos se configuran en **«Parámetros**». El recopilador omite los archivos cuyo tamaño se desconoce. Al pausar la aplicación, se conservan las tareas en cola. El reintento utiliza el descriptor de archivo original observado, nunca la última versión de un mensaje editado posteriormente. Los fallos temporales tienen un número limitado de reintentos; las pausas de «FloodWait» de los archivos multimedia se conservan tras el reinicio. La recuperación de archivos multimedia es independiente de la recuperación de actualizaciones de Telegram y no puede recrear archivos que hayan desaparecido.

## Copia de seguridad, restauración y capacidad

Detenga el proceso antes de copiar **todo** el **directorio de datos**, incluidos vault.key, signing.enc, credentials.enc, la base de datos SQLite y los archivos WAL, los archivos multimedia, el token, los puntos de control, y todos los perfiles y subdirectorios. Restaure la copia completa mientras el servicio de destino esté detenido. La falta de claves de «vault» o la discrepancia entre claves de firma provocarán que el inicio falle; no regenere claves para forzar el acceso.

Mantenga las copias de seguridad secretas cifradas y con acceso controlado. Los archivos ZIP de pruebas son artefactos de revisión portátiles, no copias de seguridad de la aplicación ni de sesiones de Telegram. No existe una eliminación automática por retención. Prevea espacio en disco suficiente para todos los mensajes, metadatos sin procesar, archivos multimedia, exportaciones temporales y copias de seguridad.

La verificación inicial y la exportación de registros de flujo se realizan en lugar de cargar el diario completo. Una exportación fija una instantánea leída mientras pueden continuar las nuevas escrituras en el WAL; las exportaciones de larga duración pueden retener páginas del WAL, por lo que la capacidad del disco sigue siendo importante. Los archivos ZIP tienen un límite de 4 GiB sin comprimir para ajustarse a la configuración predeterminada del verificador independiente; **Parámetros → ZIP firmado más grande** aumenta el límite, y dichos archivos se verifican con `verify.py --max-gib N`. Otros formatos no tienen límite de recuento de eventos. Los navegadores compatibles transmiten fragmentos de respuesta a un archivo seleccionado por el usuario. Otros navegadores almacenan en el búfer un máximo de 128 MiB y dirigen las transferencias de mayor tamaño a la CLI autenticada:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Utilice `--profile ID`, de **«Exportaciones» → «ID del espacio de trabajo»**, para otro espacio de trabajo; `--format zip|jsonl|csv|html` o `--url https://your-server` para un servidor remoto; o `--max-mib` para modificar el límite de transferencia de 5 GiB. Solo se permite el protocolo HTTP sin cifrar para el bucle de retorno. Los tokens se transmiten en los encabezados, se rechazan las redirecciones, los archivos existentes no se sobrescriben y las descargas incompletas no se publican como archivos finalizados. Si TGWITNESS_TOKEN anula el token generado, utilice un archivo protegido por separado que contenga ese valor activo: panel-token.txt no se reescribe con la anulación. El SHA-256 del comando es solo una suma de comprobación de la transferencia; verifique de forma independiente el archivo ZIP firmado.

Los archivos de exportación del servidor permanecen dentro del directorio privado «`temporary-exports/`» de cada espacio de trabajo. Las exportaciones completadas con éxito eliminan sus archivos. Las exportaciones interrumpidas se eliminan en el siguiente inicio del espacio de trabajo, mientras se mantiene el bloqueo exclusivo de la instancia. Este directorio forma parte del modelo de amenazas y capacidad de almacenamiento; utilice un volumen de datos cifrado. Las transferencias a escala de producción de varios gigabytes siguen requiriendo una validación en su sistema de destino.

El panel muestra los archivos multimedia en cola o fallidos, los archivos multimedia pendientes más antiguos, el espacio libre en disco, las pausas en las solicitudes de Telegram y las fuentes cuyo acceso no está confirmado. Estos diagnósticos no constituyen un monitor completo de entrega de extremo a extremo. Los espacios de trabajo comparten un proceso; una cuenta con mucha actividad puede seguir afectando a los demás. Se mantienen los procesos de trabajo independientes, la retención y rotación, la recuperación duradera de actualizaciones y la cualificación completa de la implementación. El acceso limitado al panel se documenta en la sección de [acceso y permisos](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/); los puntos de control independientes se tratan en la [guía del testigo](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/).

## Opciones de conexión y protección

Las rutas de conexión son específicas de cada espacio de trabajo y deben configurarse antes de la autorización. SOCKS5/HTTP CONNECT utilizan la dependencia fijada «python-socks». MTProxy utiliza el transporte intermedio aleatorio experimental de Telethon; no se admiten secretos TLS falsos. El recurso directo depende del [modo de IP](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/#ip-modes) seleccionado: «Ocultar IP» lo rechaza; el modo de recurso explícito lo permite tras un retraso. El modo «Túnel/VPN» permite rutas directas, pero no crea una VPN. No se trata de una política de red para todo el sistema.

Para nuevas instalaciones, TGWITNESS_VAULT_KEY_FILE apunta a un archivo de clave maestra aleatoria protegido por separado. Móntelo en modo de solo lectura fuera de /data en un contenedor. Conserve los metadatos públicos de la sal de vault.external.json con cada espacio de trabajo y la clave maestra por separado. Las bóvedas locales existentes requieren una migración planificada; la configuración de esta variable no las convierte automáticamente. El almacenamiento y las exportaciones de mensajes y archivos multimedia no están cifrados por la aplicación. Utilice volúmenes cifrados y suficiente almacenamiento temporal privado cuando sea necesario.

Procedimientos detallados: [conexión/seguridad](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/) y [modos de funcionamiento](https://phishdestroy.github.io/TgWitness/es/docs/reference/operations/).
