# Inicio rápido

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/quickstart/

Todas las formas de instalar y poner en marcha TgWitness: paquete para Windows, Python, Docker y la demostración sintética, con las primeras comprobaciones.

**Inglés** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [Ucraniano](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [Portugués (Brasil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [Chino simplificado](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness es una aplicación independiente para supervisar los grupos y canales de Telegram a los que tienen acceso sus cuentas. Se ejecuta localmente con su propio directorio de datos.

**¿Es su primera visita?** [Explore la demostración](https://phishdestroy.github.io/TgWitness/es/docs/reference/quickstart/#explore-the-interface) antes de vincular una cuenta. [Elija una guía](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) sobre proxies, testigos, exportaciones o configuración del servidor.

## Instalación y puesta en marcha

[Captura con GitHub Actions (versión preliminar)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

Elija un método. Las descargas portátiles estarán disponibles una vez que se publique una versión estable:

| Alojamiento | No es necesario instalar nada | Fuente: Python 3.11+ | Docker: Engine/Desktop con Compose 2.20 o superior |
| --- | --- | --- | --- |
| Windows | Extraiga «`TgWitness-<version>-windows-amd64-portable.zip`» de las versiones de GitHub y haga doble clic en «`TgWitness.cmd`» | Haga doble clic en `Start.cmd` | Haga doble clic en `scripts\Docker.cmd` |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

Para los métodos desde el código fuente, [descargue y extraiga la rama `main` actual](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) o clone el repositorio:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

El código fuente actual incluye la importación de cuentas por lotes, el panel de MTProxy y la carga de historial reanudable. La versión preliminar portátil 0.7.0 y el archivo de código fuente de su lanzamiento son anteriores a estas incorporaciones. Consulte [el registro de cambios](https://phishdestroy.github.io/TgWitness/es/docs/reference/changelog/) para ver los límites entre versiones.

`Start.cmd` ofrece instalar Python 3.12 para su usuario de Windows si no se encuentra un Python adecuado (mediante winget o el instalador firmado de python.org). `start.sh` muestra el comando de instalación exacto para su distribución de Linux o macOS si falta Python. El primer inicio desde el código fuente crea `.venv` e instala las dependencias automáticamente.

Docker compila la aplicación y la inicia en segundo plano; no es necesario un servidor Python. `scripts\Docker.cmd` y `scripts/docker-start.sh` muestran la dirección del panel y el token cuando el contenedor funciona correctamente. Los comandos de Docker equivalentes en todos los hosts compatibles son:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Abra **http://127.0.0.1:8787**. Utilice el token generado por el asistente de Docker o el segundo comando de Docker, o consulte **el archivo data/live/panel-token.txt** si se trata de una instalación portátil o desde el código fuente. Continúe en **«Conectar Telegram»** más abajo. Las instalaciones nativas y de Docker utilizan un almacenamiento independiente; al iniciar Docker no se importa ningún registro nativo existente.

En el caso de un servidor, [la implementación](https://phishdestroy.github.io/TgWitness/es/docs/reference/deployment/) incluye HTTPS automático, reinicio, imágenes publicadas, actualizaciones y copias de seguridad.

## Explore la interfaz

1. Ejecute **«TgWitness-Demo.cmd»** en el paquete portátil, **«scripts\Demo.cmd»** en una carpeta de origen de Windows o «`sh start.sh --demo` » en Linux/macOS. Al ejecutarlo desde la fuente, primero se crea «`.venv` » y se instalan las dependencias.
2. Open **http://127.0.0.1:8787**.
3. La demostración local abre automáticamente el registro de muestra. No se necesita ningún código de acceso para el acceso local directo.

Los mensajes de demostración son ficticios. El modo de demostración no permite conectarse a una cuenta real de Telegram.

## Conectarse a Telegram

> [!ADVERTENCIA] **No utilice nada que no pueda permitirse perder.** Le recomendamos encarecidamente que no conecte cuentas personales o valiosas y que no cree un ID de API ni un hash en una cuenta que considere importante. Telegram bloquea cuentas de forma impredecible y, a menudo, de manera permanente, independientemente del cliente utilizado. El buen funcionamiento de la prueba depende de Telegram, no de TgWitness, y no garantiza nada para el futuro.

1. Si la demostración nativa está en ejecución, deténgala y ejecute **«Start.cmd»** o «`sh start.sh`». De lo contrario, mantenga en ejecución la instalación en vivo iniciada anteriormente.
2. Utilice el token del panel correspondiente a su método de instalación para abrir el panel.
3. Si necesita un proxy, configúrelo en **Cuenta → Ajustes → Ajustes de conexión → Cambiar ruta de conexión**.
4. En **«Cuenta**», introduzca su número de teléfono y pulse **«Continuar»**, elija **«Código QR» → «Mostrar código QR**», o seleccione archivos y pulse **«Conectar cuenta**». **El «ID de API + Hash»** es opcional: el espacio de trabajo utiliza el par guardado o importado, o un par válido del conjunto integrado. Para utilizar su propia aplicación, pegue un par `API ID:API Hash` en el campo «ID de API». Para obtener una clave de autorización completa, seleccione **«Clave de autenticación»**, pegue los 512 caracteres hexadecimales y seleccione el ID de DC facilitado. El ID de usuario es opcional y se marca si se introduce.
5. Complete el método de inicio de sesión que haya seleccionado: teléfono/código/autenticación de dos factores (2FA), confirmación desde una aplicación de Telegram en la que haya iniciado sesión para el código QR, o una importación de sesión autorizada compatible.
6. Compruebe el ID de cuenta que se muestra. **Fuentes** abiertas: sus chats se cargan automáticamente; añada sus grupos.
7. En **«Elija qué cambios desea conservar**», seleccione las categorías de eventos o la opción predefinida **«Mensajes, ediciones y eliminaciones**» y, a continuación, guarde la configuración de supervisión.
8. Seleccione la configuración de los archivos adjuntos por separado y, a continuación, pulse **«Iniciar observación**».

Las credenciales de la API identifican su aplicación; por sí solas, no autorizan una cuenta. Los grupos privados no necesitan un nombre de usuario público, pero su cuenta debe tener acceso.

Para cuentas existentes, consulte [cuentas y formatos de sesión](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/): el panel acepta StringSession de Telethon, SQLite de Telethon/Pyrogram, ZIP de TData de una sola cuenta y archivos JSON de cuenta compatibles. Seleccione una sesión y su JSON complementario juntos, y pulse **Conectar cuenta**. El inicio de sesión por QR también está disponible con los mismos ajustes opcionales de API. No se admiten TDLib, sesiones de bots ni inventarios de cuentas en CSV/JSON.

Para varias cuentas, use **Cuentas → Importar cuentas** y seleccione sus archivos de sesión compatibles. Los archivos JSON complementarios se emparejan por su nombre base; cada cuenta importada obtiene su propio espacio de trabajo. Consulte [importación masiva y grupos de cuentas](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/#bulk-import-and-account-groups).

Para añadir otra cuenta, pulse **+** junto al selector de cuentas o abra **Cuenta → Ajustes → Ajustes de conexión → Espacios de trabajo**, o utilice **Cuentas**. Los espacios de trabajo tienen sesiones, registros, claves, fuentes y colas independientes. Al cambiar de vista, los demás recopiladores siguen en funcionamiento. En esta instalación, no es posible asignar la misma cuenta de Telegram a dos espacios de trabajo. No hay un número fijo de espacios de trabajo; estos comparten un único proceso, por lo que la capacidad depende del equipo.

El token del panel en tiempo real protege el acceso a sus autorizaciones de Telegram y al material guardado; es independiente de las credenciales de la API de Telegram. Solo una demostración local iniciada explícitamente y a la que se acceda directamente obtiene acceso automático. Una demostración remota o a través de un proxy sigue utilizando `data/demo/panel-token.txt`.

## Revisión y exportación

- **Registro:** busque y filtre las observaciones por fuente y tipo de evento.
- Seleccione un evento para examinar su registro original, su atribución y las versiones guardadas.
- Los detalles de la edición muestran el contenido disponible antes y después. Los detalles de la eliminación muestran el último contenido capturado, si lo hubiera; un actor desconocido sigue sin identificarse.
- **Formatos de exportación:** ZIP firmado, JSONL, CSV y HTML sin conexión.
- **Exportación completa del chat** (Fuentes → Exportación completa del chat): descargue todo el historial visible de un chat como un paquete firmado con `chat.json` (estilo de exportación de Telegram) y un archivo legible `chat.html`. Los chats privados funcionan cuando la cuenta es miembro. Se trata de una instantánea actual, no de una reconstrucción de mensajes eliminados o editados previamente. Verifique una copia con `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256`.
- **Punto de control:** mantenga los límites del registro firmado fuera del recopilador.
- **Descargar el recibo de ejecución firmado:** conserve el registro del programa y la versión del recopilador.
- **Preparar una solicitud de marca de tiempo:** prepare una solicitud fuera de línea dirigida a una autoridad de marcas de tiempo; siga las instrucciones de [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/timestamp/) para obtener y verificar una respuesta.
- **Verificar el registro:** compruebe las firmas de los eventos y los eslabones de la cadena. La exportación en formato ZIP también comprueba los archivos multimedia.

Los navegadores compatibles guardan exportaciones de gran tamaño directamente en el archivo elegido. Otros navegadores almacenan en el búfer un máximo de 128 MiB. Mientras el servidor está en funcionamiento, la CLI de transmisión admite descargas de mayor tamaño sin necesidad de almacenar en el búfer la respuesta completa:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Para otro espacio de trabajo, añada `--profile ID` mediante **«Exportaciones» → «ID del espacio de trabajo**». Para un servidor remoto, añada `--url https://your-server`. El límite de transferencia predeterminado es de 5 GiB; `--max-mib` lo modifica. El contenido ZIP firmado tiene un límite de verificación independiente de 4 GiB sin comprimir por defecto (**Parameters** lo aumenta; verifique dichos archivos con `verify.py --max-gib N`). Verifique el archivo utilizando una copia fiable del verificador y una huella digital o punto de control de la clave conservada de forma independiente.

## Consulte la instalación

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check` comprueba las dependencias locales, la compatibilidad con la firma, el almacenamiento, la configuración de claves y la dirección de escucha. No instala nada ni se conecta a Telegram. Si un puerto está ocupado, puede significar que hay otra instancia en ejecución. Utilice un `--port` diferente o deténgala primero.

El lanzador se instala en `.venv`. Los comandos auxiliares de `python -m tgwitness...` deben utilizar `.venv\Scripts\python.exe` en Windows o `.venv/bin/python` en Linux/macOS, a menos que dicho entorno ya esté activado.

## Sesiones, protección y funcionamiento

Un archivo `.session` de Telethon SQLite cerrado y coherente puede convertirse localmente con `python -m tgwitness.sessions account.session --out account.tgwitness-session` y, a continuación, cargarse en la cuenta. También están disponibles la importación directa de archivos y el inicio de sesión mediante código QR. Consulte [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/) para conocer los formatos de inicio de sesión, SOCKS5, HTTP CONNECT, MTProxy y las claves maestras externas.

**La función «Pausar observación»** detiene la recopilación. La opción **«Bloquear»** solo cierra el acceso al navegador. Al cerrar una pestaña, el proceso de recopilación sigue en ejecución. Detener el proceso interrumpe la recopilación; una instantánea del historial no puede reconstruir todas las modificaciones o eliminaciones que se hayan perdido. Consulte [cómo funciona la recopilación](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/) en relación con las políticas de eventos, las colas de archivos adjuntos, el aislamiento de cuentas y el comportamiento al reiniciar.

Las sesiones y los secretos están cifrados. El contenido de los mensajes, los archivos multimedia y las exportaciones requieren un disco o volumen cifrado. Las firmas garantizan la integridad en relación con una clave de confianza; no confirman el origen en Telegram ni impiden la falsificación por parte de un operador que controle el recopilador y su clave.

Consulte [el archivo OPERATIONS.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/operations/) para obtener información sobre copias de seguridad y restauración, [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/deployment/) para el alojamiento, y [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) para ver ejemplos de uso del servicio. El panel instalado también incluye una guía de configuración sin conexión en `/guide.html`.

La verificación real y las limitaciones existentes se recogen en [los archivos VERIFICATION.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/) y [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md).
