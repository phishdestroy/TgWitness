# Instalación, verificación y actualización

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/installation/

Instálala con un solo comando, comprueba las firmas y los hash, actualízala y desinstálala.

[Proyecto](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Inicio rápido](https://phishdestroy.github.io/TgWitness/es/docs/reference/quickstart/) · [Implementación](https://phishdestroy.github.io/TgWitness/es/docs/reference/deployment/)

## Se instala con un solo comando

El instalador guiado incluye un entorno de ejecución privado de Python. Utiliza la misma dirección para futuras instalaciones: cada publicación actualiza conjuntamente el instalador, los hash, las firmas y la información de compilación.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

En un servidor Ubuntu, ejecútalo como root para instalar un servicio en segundo plano. En un ordenador de sobremesa, ejecútalo como usuario normal.

**Windows (PowerShell o Símbolo del sistema):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

En Windows no se necesita ningún administrador. El proceso secundario de PowerShell deja tu terminal abierto con el resultado. Python y las dependencias permanecen en la instalación.

En Ubuntu, elige **«Este ordenador**», **«Enlace HTTPS temporal»** o **«Dominio propio**». El instalador muestra la dirección del panel y la clave de acceso. Para obtener un enlace temporal, abre esa dirección HTTPS en tu navegador e introduce la clave. Si tienes acceso local a un servidor remoto, utiliza un reenvío SSH desde tu ordenador (`ssh -L 8787:127.0.0.1:8787 user@server`) y abre `http://127.0.0.1:8787`. En macOS y Windows, el panel local se abre en tu navegador; mantén su terminal en ejecución.

Inicia sesión en Telegram en el panel y elige qué datos quieres recopilar. La instalación por sí sola no inicia la recopilación de datos de Telegram.

## Donde todo funciona

`get.destroy.tools` Es un **Cloudflare Worker que sirve descargas estáticas**. No cuenta con un panel TgWitness, ni con una sesión de Telegram, ni con una base de datos de pruebas de los usuarios. No se redirige a un VPS del proyecto. La aplicación se ejecuta en el equipo en el que se ejecuta el comando.

| Instalación | Programa | Datos |
| --- | --- | --- |
| Ubuntu como root | `/opt/tgwitness` | Servicio del sistema: `/var/lib/tgwitness-<installation ID>`; utiliza `tgwitness paths` para obtener la ruta exacta. |
| Usuario de Linux / macOS | `~/.local/share/tgwitness` | `data/live` en esa instalación. |
| Usuario de Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` en esa instalación. |

Selecciona `TGWITNESS_INSTALL_DIR` para elegir otra carpeta. Las versiones instaladas y los datos están separados. El instalador no sube tus cuentas, mensajes ni claves al sitio de descarga. Si eliges un túnel de Cloudflare, el tráfico del panel se envía a través de Cloudflare; si utilizas tu propio dominio, se redirige a tu propio servidor.

Cada instalación incluye los archivos **START-HERE.html** y **START-HERE.txt**, con rutas locales, comandos y enlaces al repositorio. Ejecuta `tgwitness guide` para abrir la guía. En Windows, utiliza `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` en PowerShell.

## Configuración de la búsqueda de texto completo

[La búsqueda de texto completo](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/) (vista previa) no requiere configuración. Su índice se crea en segundo plano tras una actualización.

| Variable o comando | Efecto |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | Por defecto: el índice se guarda en `search/fulltext.sqlite3` de cada espacio de trabajo |
| `TGWITNESS_FULLTEXT=memory` | No hay archivo de índice; el índice se reconstruye cada vez que se inicia el programa. |
| `TGWITNESS_FULLTEXT=off` | Sin índice; solo búsqueda de texto exacto. |
| `tgwitness index status` | Estado del índice de cada espacio de trabajo |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | Recompilar todos los índices a partir del diario firmado. |

La selección del administrador en **Diario → Filtros → Índice de búsqueda** anula la variable para ese espacio de trabajo. Los comandos buscan el directorio de datos de la instalación en la que se ejecutan; en los demás casos, añade `--data-dir` la ruta de `tgwitness paths`. Para obtener un diccionario completo de ucraniano (datos bajo licencia GPL-3.0), instala `pymorphy3-dicts-uk` en el entorno de Python de la instalación.

## Acceso mediante la línea de comandos

La [línea de](https://phishdestroy.github.io/TgWitness/es/docs/reference/cli/) [comandos](https://phishdestroy.github.io/TgWitness/es/docs/reference/cli/) (vista previa) lee el archivo en busca de scripts y agentes.

| Variable | Efecto |
| --- | --- |
| `TGWITNESS_URL` | Dirección del panel para `tgwitness search`, `context`, `messages`, `stats` y `export`; por defecto `http://127.0.0.1:8787` cuando se establece un token |
| `TGWITNESS_MCP_TOKEN` | Archivar el token de conexión desde **Integraciones → MCP**, compartido con los clientes de MCP; `--token-file` en su lugar, lo lee de un archivo |
| `TGWITNESS_DATA` | El directorio de datos se lee directamente cuando no `--data-dir`se especifique una URL o un token. |

## Comprueba antes de ejecutar

El comando de una sola línea confía en HTTPS para su script inicial. Dicho script comprueba SHA-256 y la firma RSA del proyecto en la aplicación y las restricciones antes de la instalación. También puedes descargar y verificar primero el script inicial.

La clave de publicación pública es [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). Su SHA-256 es:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Conserva esta huella digital de una revisión del repositorio en la que confíes. Una suma de comprobación procedente del mismo servidor de descargas detecta cualquier discrepancia; la clave pública, cuya fiabilidad está verificada de forma independiente, es la que autentica la firma de una versión.

Utiliza un directorio nuevo y vacío para las descargas de verificación que se indican a continuación.

**Linux / macOS: ejecútalo en un directorio de descargas nuevo y vacío** (requiere curl y OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

La `&&` cadena se detiene antes de la ejecución si falla una descarga, la verificación de la huella digital de la clave o la verificación de la firma. Si se produce una publicación entre la descarga del script y su firma, se descargan ambos de nuevo. Los instaladores antiguos conservan las URL inmutables de sus paquetes.

**Windows: comprueba la imagen SHA-256 antes de ejecutarlo:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Compara el hash con la `install.ps1` línea. Para realizar una comprobación independiente de la firma, utiliza OpenSSL (por ejemplo, desde Git Bash) y la misma huella digital de la clave pública indicada anteriormente:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

La propia instalación de Windows verifica las firmas de los paquetes con .NET y no requiere OpenSSL. Se trata de firmas independientes RSA-3072 / SHA-256, no de Authenticode. El [manifiesto](https://get.destroy.tools/manifest.json) registra la versión del software, el commit exacto de Git, el ID de lanzamiento inmutable y el SHA-256 de cada artefacto. La página enlaza con el código fuente correspondiente. El manifiesto y la lista de sumas de comprobación también tienen firmas independientes (`manifest.json.sig` y `SHA256SUMS.txt.sig`).

## Actualizar una instalación existente

**Una nueva publicación actualiza el sitio de descargas; los programas instalados se actualizan cuando se vuelve a ejecutar el instalador.** No hay ningún actualizador automático ni reinicio automático de una colección en ejecución. El canal actual del instalador es **«preview»**; sigue las compilaciones publicadas y comprobadas de `main`, cuyo commit puede ser más reciente que la última versión numerada de GitHub. La versión de la página procede de `pyproject.toml`; su commit y el ID de la compilación distinguen las actualizaciones dentro de la misma versión de vista previa.

Publication is automatic after that exact commit passes the application and security checks and the signed package passes Ubuntu service and Windows PowerShell installation tests. While checks are running, or if they fail, the same commands continue to install the previous checked build. The build manifest shows which commit is currently available; the version number alone may stay the same between preview updates.

Utiliza la misma carpeta de instalación y el mismo usuario del sistema operativo que antes. Haz una copia de seguridad del directorio de datos completo con la recopilación detenida; `tgwitness paths` lo identifica. Una exportación firmada no es una copia de seguridad completa de la instalación.

**Instalación como root en Ubuntu en `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

Tras una instalación correcta:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Para la instalación en Linux o macOS, utiliza la ruta original `TGWITNESS_INSTALL_DIR` o la configuración predeterminada y vuelve a ejecutar el primer comando de instalación. Cierra el panel en primer plano antes de actualizar y vuelve a iniciarlo después. Para un servicio de usuario de Linux ya configurado, ejecuta su `tgwitness restart` comando.

**Windows:** cierra el panel en ejecución, vuelve a ejecutar el comando de instalación de Windows y, a continuación, abre `bin\tgwitness.cmd` en la misma instalación. El instalador conserva los datos, las sesiones, la configuración de acceso y las claves de firma. Solo cambia el lanzador después de que el nuevo entorno supere las comprobaciones; si la instalación falla, se mantiene el lanzador anterior. Conserva la copia de seguridad previa a la actualización por si se producen cambios en el formato de almacenamiento.

## Comandos habituales en Ubuntu

| Comando | Resultado |
| --- | --- |
| `tgwitness open` | URL actual del panel y clave de acceso. |
| `tgwitness paths` | Rutas exactas de programas, datos y guías. |
| `tgwitness guide --print` | Instrucciones de funcionamiento sin conexión. |
| `tgwitness status` / `tgwitness logs` | Disponibilidad / registros del servicio. |
| `tgwitness stop` / `tgwitness start` | Detener o reanudar el servicio; conservar los datos. |
| `tgwitness token rotate` | Sustituye la clave de administrador y cierra las sesiones del navegador. |
| `tgwitness tunnel off` | Desactiva el túnel rápido público; mantén el panel local. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Crea un enlace de túnel rápido o sustituye su dirección. |

Consulta la sección [«Acceso»](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/) para obtener información sobre tokens de compañeros, sesiones y restricciones de IP, y la sección [«Publicación del instalador»](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) para conocer el flujo de trabajo de lanzamiento de GitHub a Cloudflare.

## Eliminar TgWitness

No hay desinstalador: basta con cerrar el panel y eliminar sus carpetas. Al eliminar la carpeta de datos se destruyen definitivamente los diarios, las claves de firma, las sesiones de Telegram y los archivos guardados. Antes de eso:

1. Exporta lo que necesites (**Exportaciones → Descargar ZIP firmado**) y guarda la huella digital de la clave de firma y los puntos de control fuera de este equipo. Para conservar el propio espacio de trabajo, copia toda la carpeta de datos con la recopilación detenida.
2. Elimina los servidores creados en **Extras → Servidor 24/7** desde **«Tus servidores»** o con `python -m tgwitness.cloud destroy`; el proveedor los factura hasta que se eliminen.
3. Cierra la sesión de cada cuenta en Telegram en **Ajustes → Dispositivos**. Borrar los archivos no supone cerrar la sesión por parte de Telegram.

**Instalación como root en Ubuntu.** Toma nota de la carpeta de datos, detén el servicio y, a continuación, elimina el servicio, las carpetas y el acceso directo:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Instalación para usuarios de Linux o macOS.** Cierra el panel. Un servicio de usuario de Linux configurado se detiene con `systemctl --user disable --now tgwitness-<ID>`; su unidad se encuentra en `~/.config/systemd/user/`. A continuación, elimina `~/.local/share/tgwitness` (o tu `TGWITNESS_INSTALL_DIR`) y el `~/.local/bin/tgwitness` acceso directo.

**Windows.** Cierra el panel y elimina `%LOCALAPPDATA%\TgWitness` (o tu `TGWITNESS_INSTALL_DIR`). El instalador no añade ningún servicio, tarea programada ni acceso directo.
