[TgWitness](../../README.md) / [Documentación](../README.md) / [Carpeta](README.md)

![Despliegue y recuperación](../assets/presentation/chapter-operate.svg)

[English](../DEPLOYMENT.md) · [Русский](../ru/DEPLOYMENT.md) · [Українська](../uk/DEPLOYMENT.md) · **Español** · [Português (Brasil)](../pt/DEPLOYMENT.md) · [Türkçe](../tr/DEPLOYMENT.md) · [العربية](../ar/DEPLOYMENT.md) · [فارسی](../fa/DEPLOYMENT.md) · [اردو](../ur/DEPLOYMENT.md) · [हिन्दी](../hi/DEPLOYMENT.md) · [Bahasa Indonesia](../id/DEPLOYMENT.md) · [Tiếng Việt](../vi/DEPLOYMENT.md) · [简体中文](../zh/DEPLOYMENT.md)

# Despliegue y operación

## Elección de la instalación

Para el paquete portátil, extraiga `TgWitness-<version>-windows-amd64-portable.zip` de
GitHub Releases. Para los demás métodos, descargue y extraiga el archivo ZIP con el código fuente o clone el
repositorio; a continuación, ejecute lo siguiente desde el directorio del proyecto:

| Instalación | Inicio | ¿Se ejecuta en segundo plano? |
| --- | --- | --- |
| Paquete portátil de Windows | `TgWitness.cmd` | No; mantenga la ventana abierta. |
| Nativo de Windows | `Start.cmd` | No; utilice la tarea de inicio de sesión opcional para su ejecución en segundo plano. |
| Nativo para Linux/macOS | `sh start.sh` | No; utilice systemd/launchd para la ejecución en segundo plano. |
| Docker en cualquier host compatible | `docker compose up -d --build --wait` | Sí, mientras el demonio de Docker esté en ejecución. |
| Herramienta auxiliar de Docker en Windows | `scripts\Docker.cmd` | Sí; el helper espera a que el servidor web esté operativo. |
| Herramienta auxiliar de Docker en Linux/macOS | `sh scripts/docker-start.sh` | Sí; el helper espera a que se compruebe el estado del servidor web. |

Para obtener información sobre un servidor en la nube que un tercero pueda comprobar —creado a través de la
API del proveedor, sin SSH y al que solo se pueda acceder a través de un túnel de Cloudflare—, consulte
[implementación de alta seguridad](../HIGH-ASSURANCE.md).

La aplicación nativa crea una imagen privada `.venv` e instala las dependencias fijadas.
Docker las compila dentro de la imagen, sin necesidad de utilizar Python del equipo anfitrión. La
configuración inicial requiere acceso a Internet. Cuando no se encuentra Python 3.11 o superior, `Start.cmd` solicita permiso antes de
instalar Python 3.12 para el usuario actual de Windows (mediante winget; en caso contrario, se utiliza el instalador de python.org
tras comprobar su firma de la Python Software Foundation); nunca solicita
privilegios de administrador. Docker y los servicios del sistema operativo siguen siendo requisitos previos.

Las instalaciones nativas y portátiles utilizan `data/live` dentro de su carpeta. Docker utiliza el volumen denominado `tgwitness-data`
en `/data`. Se trata de instalaciones independientes hasta que se migre deliberadamente el
directorio de datos completo. No espere que un nuevo contenedor de Docker detecte las cuentas nativas
de forma automática.

## Requisitos de instalación

La instalación nativa requiere Python 3.11 o posterior, junto con `venv` y `ensurepip`, acceso a Internet
para la instalación de la primera dependencia y un directorio de proyecto con permisos de escritura para
`.venv`. El panel incluido no requiere Node.js ni compilación de frontend. Ejecute el lanzador desde
su cuenta habitual del sistema operativo; TgWitness no requiere privilegios de administrador ni de root.

- **Windows:** `Start.cmd` comprueba `py -3`, a continuación `python`, después las carpetas de instalación predeterminadas por usuario y
  «Archivos de programa», y requiere la versión 3.11 o posterior. Si ninguna de ellas funciona,
  ofrece la instalación automática por usuario descrita anteriormente. `py -3 start.py` también funciona.
  El paquete portátil no necesita Python en absoluto.
- **Linux:** `start.sh` comprueba `python3.13`, `python3.12`, `python3.11`, `python3` y
  `python`, y muestra el comando de instalación para apt, dnf, pacman, zypper, apk o Homebrew
  cuando ninguno cumple los requisitos. Las instalaciones en Debian/Ubuntu pueden requerir el paquete
  `python3-venv` que coincida con el intérprete seleccionado. La versión predeterminada más antigua
  de Python de una distribución debe sustituirse o complementarse con Python 3.11 o superior.
- **macOS:** instale una distribución actual de Python 3.11 o superior; no dé por sentado que un intérprete
  proporcionado por el sistema operativo cumple los requisitos. Utilice `python3 start.py` desde el directorio del proyecto.
- **Docker:** utilice Docker Engine/Desktop con Compose v2.20 o posterior. Docker Desktop
  debe utilizar contenedores Linux en Windows. El contenedor instala sus
  propias dependencias de Python; el sistema anfitrión no necesita una instalación independiente de Python.

## Equipo local

Utilice `Start.cmd` en Windows o `sh start.sh` en Linux/macOS. `scripts\Setup.cmd` o
`sh start.sh --setup-only` preparan
el entorno. El programa de inicio instala las dependencias la primera vez que se utiliza; los siguientes inicios
reutilizan el entorno. Se necesita acceso a Internet para la configuración y la recopilación de datos de Telegram,
pero la consulta de registros existentes y la creación de exportaciones funcionan sin conexión.

Ejecute `python start.py --check` tras la configuración para comprobar las dependencias locales, Ed25519,
el almacenamiento, la configuración de claves y la dirección de escucha sin iniciar un colector.
Utilice `--json` para obtener una salida estructurada. Pase los elementos `--data-dir`, `--host` y
`--port` previstos. La comprobación no instala paquetes, no crea un diario ni se conecta a Telegram;
no se trata de una verificación de integridad ni de cobertura. El proceso de inicio verifica por separado
los diarios existentes. `python start.py --help` también evita la instalación.

Tras ejecutar start.py, ejecute los comandos auxiliares con `.venv\Scripts\python.exe` en
Windows o `.venv/bin/python` en Linux/macOS, o bien active primero dicho entorno.
Los ejemplos `python -m ...` que figuran a continuación dan por hecho que el entorno está activo.

~~~sh
python -m tgwitness --data-dir /ruta/a/datos/privados --host 127.0.0.1 --port 8787
~~~

Variables de entorno: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN.
TGWITNESS_VAULT_KEY_FILE selecciona el modo de clave externa para una nueva instalación; véase [Clave maestra externa](../SECURITY-MODEL.md#external-master-key).
TGWITNESS_TOKEN, si se proporciona, debe contener al menos 24 caracteres; utilice un valor aleatorio
criptográficamente seguro. Sin él, la aplicación genera un token aleatorio de 256 bits en el archivo panel-token.txt.
La sustitución de variables de entorno no sobrescribe ese archivo. Reinicie el sistema para rotar las credenciales.

Solo un proceso puede ser el propietario de un directorio de datos. Un bloqueo de archivos multiplataforma del sistema operativo evita
escrituras simultáneas accidentales. Utilice un único trabajador de Uvicorn. El panel puede gestionar cualquier número de
espacios de trabajo, con directorios de espacios de trabajo adicionales en la ruta «profiles/<id>/».
Para instancias de servicio independientes, utilice directorios y puertos distintos. Los archivos WAL de SQLite deben almacenarse en un
almacén persistente local, no en un sistema de archivos de red. No comparta un mismo volumen entre réplicas.

## Paquete portátil para Windows

Cada versión de GitHub incluye `TgWitness-<version>-windows-amd64-portable.zip` y su
`.sha256`. Contiene el entorno de ejecución oficial de Python 3.12 de python.org, que se puede incrustar
(suma de comprobación fijada en `tools/build_portable.py`), TgWitness y sus dependencias fijadas,
y tres programas de inicio:

| Archivo | Objetivo |
| --- | --- |
| `TgWitness.cmd` | Inicie el panel; se transmiten opciones adicionales, p. ej., `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | Inicie la demostración sintética en `data\demo` |
| `TgWitness-Check.cmd` | Ejecute la comprobación de preparación sin iniciar el sistema |

El diccionario de morfología rusa fijado y los perfiles de color en formato PDF se incluyen en el paquete para
su uso sin conexión. El proceso de empaquetado solo permite que las rutas de archivo conocidas se encuentren dentro de los directorios de dependencias
`data`; la presencia de archivos inesperados en dichos directorios provoca un error en la compilación.

Descomprima todo el archivo en una carpeta en la que se pueda escribir, como `Documents\TgWitness`; no lo ejecute
desde dentro del archivo ZIP ni desde «Archivos de programa». El entorno de ejecución utiliza una ruta de módulos aislada,
por lo que otras instalaciones de Python y `PYTHONPATH` no le afectan. Los datos permanecen en la
carpeta `data` del paquete. Para actualizar, cierre TgWitness, extraiga la nueva versión en una nueva
carpeta y copie la carpeta `data` a la nueva ubicación.

Compílelo usted mismo en Windows de 64 bits con Python 3.12:

~~~sh
python tools/build_portable.py
~~~

## Contenedor

```sh
docker compose up -d --build --wait
```

Esto crea un volumen persistente con nombre para /data.
El puerto web se asigna a 127.0.0.1:8787. El proceso se ejecuta con el UID 10001 con
capacidades restringidas, un sistema de archivos raíz de solo lectura y los directorios /data y /tmp con permisos de escritura.
`--wait` comprueba el estado del servidor web antes de devolver un resultado; la autorización y la
entrega de Telegram aparecen en el panel. Los ayudantes proporcionados utilizan un tiempo de espera de disponibilidad de 180 segundos
tras la compilación. Las descargas iniciales de dependencias pueden tardar más tiempo.

Ambos archivos Compose básicos utilizan el nombre del proyecto `tgwitness`, por lo que extraer una nueva versión
a otro directorio no selecciona automáticamente un nuevo volumen de datos. Mantenga solo una
implementación activa para ese proyecto. Para instalaciones independientes, utilice un
`docker compose -p NAME ...` único y un puerto de host diferente, y conserve ambos en las actualizaciones.
En el caso de una implementación anterior que utilice un nombre de proyecto diferente, siga utilizando su nombre original
con `-p`; `docker compose ls` muestra los proyectos existentes.

Copie `deploy/env.example` en `.env` y modifique `TGWITNESS_PORT` para utilizar un puerto de bucle cerrado
diferente. Por ejemplo, `TGWITNESS_PORT=8788` expone el panel en
`http://127.0.0.1:8788`; el contenedor sigue escuchando en el puerto 8787. `.env` se omite en Git.

Recupere el token inicial:

~~~sh
docker compose exec tgwitness cat /data/panel-token.txt
~~~

Comandos útiles:

```sh
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` reinicia el colector tras un fallo o un reinicio del demonio de Docker.
En un servidor Linux, active Docker al arrancar utilizando el gestor de servicios
de su distribución, normalmente `sudo systemctl enable --now docker`. En Windows/macOS, active
la configuración «Iniciar al iniciar sesión» de Docker Desktop. El cierre de sesión, el modo de suspensión o la detención del
puede interrumpir la recopilación. Un contenedor detenido explícitamente permanece
detenido hasta que lo vuelva a iniciar.

El volumen /tmp tiene un límite de 512 MiB en la configuración de ejemplo. La construcción de la exportación
utiliza, en su lugar, el `temporary-exports/` de cada espacio de trabajo en el directorio persistente /data. Reserve espacio
allí para exportaciones simultáneas, el crecimiento del diario/WAL, los archivos multimedia y las copias de seguridad.
El lanzador utiliza el archivo deploy/constraints.txt para fijar las versiones de las dependencias de tiempo de ejecución que cumplen los requisitos.
Los servidores Docker y de alta seguridad se instalan a partir de deploy/requirements.lock y
deploy/build.lock con pip --require-hashes: cada archivo de paquete debe coincidir con un SHA-256
registrado en la confirmación, por lo que se rechaza cualquier archivo sustituido en PyPI o en un servidor espejo. Los paquetes que
solo incluyen el código fuente (jieba, pyaes) se compilan con las herramientas de configuración fijadas en deploy/build.lock
(`--no-build-isolation`) por el lanzador, el compilador portátil de Windows y el Dockerfile,
por lo que pip no resuelve un entorno de compilación independiente y sin fijar. La imagen base de Python
y los paquetes del sistema operativo siguen requiriendo una calificación de lanzamiento independiente.

No utilice el comando «docker compose down -v» a menos que tenga la intención de destruir el registro y las claves.
El informe de estado del contenedor indica la disponibilidad del servidor web, no que la captura de Telegram se haya realizado correctamente.
Compruebe el estado del colector del panel, el «heartbeat», los errores y los eventos de cobertura.

### Perfil de testigo independiente

El servicio opcional `witness` ejecuta un [testigo independiente](../WITNESS.md) en su propio
contenedor, con su propia clave y diario en el volumen `witness-data` y únicamente un
token de testigo de solo lectura para el recopilador. Cree el token en el panel en **Más herramientas → Extras → Testigo independiente**, añádalo
con un token de bot y un canal a `.env` y, a continuación, inicie el perfil:

```sh
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

El servicio se conecta al colector dentro de la red Compose en `http://tgwitness:8787`
(`TGWITNESS_WITNESS_COLLECTOR`
lo sustituye; por ejemplo, `/profiles/<workspace ID>`
para
otro espacio de trabajo). Para un testigo en un servidor independiente, gestionado por otra persona, utilice
`deploy/compose/compose.witness.yaml`
allí, con `TGWITNESS_WITNESS_COLLECTOR`
configurado con la dirección HTTPS
del colector; dicho archivo contiene únicamente el testigo.

## Instalación de una imagen publicada

Copie `deploy/env.example` en `.env`. Establezca `TGWITNESS_IMAGE` en la versión publicada, utilizando
la ruta del repositorio en **minúsculas**, por ejemplo:

```dotenv
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:1.0.2
TGWITNESS_PORT=8787
```

Ejecute este archivo por sí solo, en lugar de `compose.yaml`:

```sh
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

No se necesita ninguna compilación de código fuente, Python ni compilador en el equipo host. El flujo de trabajo de lanzamiento
está destinado a contenedores Linux AMD64 y ARM64, incluida la máquina virtual Linux de Docker Desktop.
Utilice una etiqueta de versión o `ghcr.io/owner/repository@sha256:...` desde el resumen del flujo de trabajo.
No se ha configurado ninguna etiqueta móvil `latest` ni ninguna actualización automática de la aplicación. La
imagen y las variantes de código fuente utilizan el mismo volumen de datos cuando coinciden en el nombre del proyecto.

## HTTPS automático en un servidor

Utilice un servidor con Docker, un dominio bajo su control y almacenamiento local persistente.
Dirija los registros A/AAAA del dominio hacia el servidor; publique el registro AAAA únicamente si el IPv6 llega
hasta él. Permita el tráfico entrante por los puertos TCP 80 y 443, así como el tráfico saliente por DNS/HTTPS para la emisión de certificados.
Estos puertos no deben estar ya ocupados por otros servicios.

Copie `deploy/env.example` en `.env` y establezca un nombre de host, sin esquema ni ruta:

```dotenv
TGWITNESS_DOMAIN=watch.your-domain.org
```

Inicie la compilación del código fuente con la superposición HTTPS:

```sh
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```sh
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

En el caso de una imagen publicada, utilice en su lugar `deploy/compose/compose.image.yaml` como primer archivo. Conserve
ambos argumentos `-f` para los comandos posteriores de estado, registro, actualización y parada.

Caddy obtiene y renueva un certificado, redirige el tráfico HTTP a HTTPS y reenvía
las solicitudes al colector en la red privada de Compose. El estado del certificado cuenta
con su propio volumen persistente. El puerto de host directo del colector sigue siendo de solo bucle de retorno.
La configuración de Caddy proporcionada no habilita el registro de accesos.

Abra `https://watch.your-domain.org` e introduzca el token del panel. El estado de preparación
abarca los contenedores; la emisión de certificados y la accesibilidad externa dependen del DNS
y del cortafuegos. Si HTTPS no está listo, compruebe el DNS, las reglas del cortafuegos y:

```sh
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

La imagen de Caddy proporcionada aparece tras la etiqueta `2-alpine`. Al ejecutar «pull», se actualiza dicha imagen;
incluya un resumen comprobado en su implementación si necesita versiones fijas de la infraestructura.

## Actualizaciones y copias de seguridad

Conserve el nombre del proyecto Compose y el volumen de datos tras cada actualización. En primer lugar, detenga el
recopilador y realice una copia de seguridad completa. Para la implementación predeterminada basada en el código fuente:

```sh
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Utilice cada vez un nuevo destino de copia de seguridad, fuera del repositorio, y protéjalo como
material de acceso a la cuenta. La ruta de ejemplo es meramente ilustrativa; utilice su propia ubicación privada
para la copia de seguridad. Copie todo el directorio, incluidos los archivos ocultos, todos los espacios de trabajo, las claves,
los registros y los archivos multimedia. Realice una copia de seguridad por separado de la clave maestra de la bóveda externa, si está configurada.
Un archivo ZIP de pruebas no es una copia de seguridad de la aplicación que se pueda restaurar. En el caso de HTTPS, conserve también
los volúmenes de Caddy si necesita mantener el estado de su certificado o de su cuenta.

Para una implementación desde el código fuente, obtenga los archivos de la nueva versión y ejecute:

```sh
docker compose up -d --build --wait
```

Para implementar una imagen, cambie `TGWITNESS_IMAGE` por la versión deseada y, a continuación, ejecute:

```sh
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Utilice también los archivos Compose de su instalación para los comandos de detención y copia anteriores.
Mantenga `.env`, la configuración personalizada y el mismo nombre de proyecto. `down` conserva los
volúmenes con nombre; **`down -v` los elimina**. No copie `.venv` entre sistemas operativos
o versiones de Python. Para actualizaciones nativas, detenga TgWitness, realice una copia de seguridad de todo su
directorio de datos, sustituya los archivos de origen y ejecute `python start.py --setup-only` antes de iniciar el programa.

Compruebe el acceso al panel, la identidad de la cuenta, el estado de observación y la cobertura tras una
actualización. Tras el reinicio, TgWitness retoma la posición de actualización de Telegram guardada y
solicita las actualizaciones que se hayan perdido durante el proceso. Una reversión podría
requerir la copia de seguridad previa a la actualización si una versión futura cambia los formatos de almacenamiento.

## Servidor remoto

Mantenga el servicio vinculado al bucle de retorno y utilice un túnel SSH, o bien termine la conexión HTTPS en un
proxy inverso. El archivo Compose base es de uso exclusivamente local; la superposición opcional
`deploy/compose/compose.https.yaml` proporciona Caddy para un dominio configurado.
Mantenga el token de portador fuera de las URL y de los registros del proxy. Un proxy inverso debe limitar
el tamaño de las solicitudes y la frecuencia de las conexiones. No exponga el HTTP sin cifrar a Internet.

En [deploy/](../../deploy/README.md) se proporcionan ejemplos para systemd, una tarea de inicio de sesión de Windows, un agente de usuario de macOS y Caddy.
Revise y adapte sus rutas antes de la instalación.
Se trata de plantillas, no de configuraciones de plataforma ejecutadas localmente. El lanzador estándar no
registra ningún servicio ni tarea en segundo plano.

En Windows, al iniciar una instancia sin ventana `pythonw.exe`, los diagnósticos de inicio y del servidor se almacenan en
`logs/server.log`, dentro del directorio de datos (5 MiB por archivo, dos copias de seguridad rotativas).
Las ejecuciones desde la consola conservan los registros de la consola. El registro de acceso HTTP está desactivado en ambos
modos. Proteja los registros junto con el directorio de datos y revíselos antes de compartirlos.

## Reinicio y lagunas

Se guarda el último estado de observación solicitado. Si la observación estaba activa,
el sistema intenta, al iniciarse, volver a conectarse y reanudar las fuentes seleccionadas. La pausa manual anula
esa intención. Se registra cualquier reinicio fallido y se muestra en el panel.

TgWitness almacena la posición de actualización de Telegram para la cuenta y para cada canal
(pts, qts, seq y fecha) en el almacén del espacio de trabajo y la restaura en el siguiente inicio.
A continuación, el cliente solicita las actualizaciones perdidas mientras el proceso estaba detenido, y la
revisión periódica recupera los mensajes perdidos y registra aquellos guardados que Telegram ya
no devuelve. Los diálogos se recargan al iniciar. Cada vez que se inicia, se registra el
encabezado del diario anterior, el límite de desconexión y la posición de actualización desde la que se reanudó.
El monitor comprueba la conectividad cada 10 segundos y añade un pulso de vida cada minuto
(**Más herramientas → Parámetros → Registro de actividad cada**).
Las desconexiones y los períodos de inactividad se registran como lagunas de cobertura junto con su motivo.
Las instantáneas del historial se almacenan como observaciones separadas del historial actual junto a los registros en tiempo real.

La cola de archivos multimedia se almacena en la base de datos SQLite de cada espacio de trabajo. Un mensaje y su tarea
se confirman de forma atómica. Las tareas en ejecución que se interrumpen se recuperan para volver a intentarlas al reiniciar.
Cada descarga tiene un tiempo de espera base de 120 segundos, más el tiempo correspondiente a su tamaño a una velocidad de 256 KiB/s, y un
límite de entre 1 y 2.000 MiB por tipo de archivo adjunto; el tiempo de espera, la velocidad y los reintentos se configuran en **Más herramientas → Parámetros**. El recopilador
omite los archivos cuyo tamaño se desconoce. Al pausar la aplicación, se conservan las tareas en cola. El reintento utiliza el
descriptor de archivo original observado, nunca la última versión de un mensaje editado posteriormente.
Los fallos temporales tienen un número limitado de reintentos; las pausas de FloodWait de archivos multimedia se mantienen tras el reinicio.
La recuperación de archivos multimedia es independiente de la recuperación de actualizaciones de Telegram y no puede recrear archivos que hayan desaparecido.

## Copia de seguridad, restauración y capacidad

`tgwitness backup FOLDER`
copia el directorio de datos mientras el panel sigue en funcionamiento:
primero los puntos de control, luego los archivos SQLite a través de la API de copia de seguridad en línea, y a continuación las claves, los medios y
los perfiles, de modo que ningún punto de control copiado sea más reciente que el diario copiado. `backup-manifest.json`
muestra el SHA-256 de cada archivo y los encabezados del diario. Para restaurar, detenga TgWitness y sustituya
todo el directorio de datos por esa carpeta. Al siguiente inicio, se registrará que el diario se ha restaurado
a partir de una copia anterior. Dicho registro compara el diario con el encabezado guardado en
`TGWITNESS_STATE_DIR`
, una carpeta situada fuera del directorio de datos: el volumen `tgwitness-state`
en
Compose, `/var/lib/tgwitness-state`
en las unidades de systemd y, en los demás casos, en la carpeta de estado local del usuario
. Si la carpeta de estado no es grabable, la restauración no se detecta y el registro lo indica una vez.

Si no se utiliza este comando, detenga el proceso antes de copiar el **directorio de datos completo**, incluidos los archivos vault.key,
signing.enc, credentials.enc, la base de datos SQLite y los archivos WAL, los archivos multimedia, el token, los puntos de control,
y todos los subdirectorios de «profiles/». Restaure
la copia completa mientras el servicio de destino esté detenido. La falta de claves de la bóveda o
una discrepancia en las claves de firma provocarán que el inicio falle; no vuelva a generar claves para forzar el acceso.

Mantenga las copias de seguridad secretas cifradas y con acceso controlado. Los archivos ZIP de pruebas son
elementos de revisión portátiles, no copias de seguridad de aplicaciones ni de sesiones de Telegram.
No existe un proceso automático de eliminación por retención. Prevea espacio en disco suficiente para todos los mensajes, metadatos
sin procesar, archivos multimedia, exportaciones temporales y copias de seguridad.

Verificación de inicio y exportación de registros de flujo en lugar de cargar todo el diario.
Una exportación fija una instantánea de lectura mientras pueden continuar las nuevas escrituras en el WAL; las exportaciones de larga duración
pueden retener páginas del WAL, por lo que la capacidad del disco sigue siendo importante. Los archivos ZIP tienen un límite de 4 GiB
sin comprimir, para ajustarse al valor predeterminado del verificador independiente; **Más herramientas → Parámetros → ZIP firmado más grande**
aumenta dicho límite, y dichos archivos se verifican con `verify.py --max-gib N`. Otros formatos no tienen límite en el recuento de eventos.
Los navegadores compatibles transmiten fragmentos de respuesta a un archivo seleccionado por el usuario. Otros navegadores
almacenan en el búfer un máximo de 128 MiB y dirigen las transferencias de mayor tamaño a la CLI autenticada:

~~~sh
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
~~~

Utilice `--profile ID`, procedente de **Exportaciones → ID del espacio de trabajo**, para otro espacio de trabajo;
`--format zip|jsonl|csv|html`, `--url https://your-server` para un servidor remoto; o
`--max-mib` para modificar el límite de transferencia de 5 GiB. El protocolo HTTP sin cifrar solo está permitido para
el bucle de retorno. Los tokens se transmiten en los encabezados, se rechazan las redirecciones, los archivos existentes
no se sobrescriben y las descargas incompletas no se publican como archivos finalizados.
Si TGWITNESS_TOKEN anula el token generado, utilice un archivo protegido por separado
que contenga ese valor activo: el archivo panel-token.txt no se reescribe con la anulación.
El SHA-256 del comando es solo una suma de comprobación de la transferencia; verifique de forma independiente el archivo ZIP firmado.

El panel muestra los archivos en cola o con error, los archivos pendientes más antiguos, el espacio libre en disco, las
pausas en las solicitudes de Telegram y las fuentes cuyo acceso no está confirmado. Estos diagnósticos no constituyen
un monitor completo de la entrega de extremo a extremo. Los espacios de trabajo comparten un proceso; una cuenta con actividad irregular puede
seguir afectando a los demás. Se mantienen los procesos de trabajo independientes, la retención y rotación, la recuperación de actualizaciones duraderas
y la cualificación completa de la implementación. El acceso al panel con alcance limitado se documenta
en [acceso y permisos](../ACCESS.md); los puntos de control independientes se tratan en la
[guía de testigos](../WITNESS.md).

Procedimientos detallados: [conexión/seguridad](../CONNECTION-SECURITY.md) y
[modos de funcionamiento](../OPERATIONS.md).
