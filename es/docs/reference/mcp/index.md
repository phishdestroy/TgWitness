# Telegram · MCP de solo lectura

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/

Conecta un cliente MCP a espacios de trabajo y chats seleccionados con acceso temporal y revocable.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentación](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Integraciones con archivos](https://phishdestroy.github.io/TgWitness/es/docs/reference/cli/)

![Integraciones con archivos](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

Conecta un cliente de análisis a los espacios de trabajo y chats seleccionados. TgWitness sirve **Streamable HTTP en `/mcp` en el proceso del panel**. Cada conexión tiene su propio token, fecha de caducidad y herramientas permitidas. MCP no puede enviar mensajes de Telegram, cambiar la configuración ni modificar el registro firmado. Las mismas conexiones funcionan con la [línea de comandos](https://phishdestroy.github.io/TgWitness/es/docs/reference/cli/).

[Guía de flujo de trabajo](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**En esta página**

- [Instalación y comprobación](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/#install-and-check)
- [Establecer una conexión](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/#issue-a-connection)
- [Conecta tu cliente](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/#connect-your-client)
- [Túnel de Cloudflare](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/#cloudflare-tunnel)
- [Herramientas y límites](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/#tools-and-boundaries)

## Instalar y comprobar

Use el entorno de Python que ejecuta el panel. Desde una descarga del código fuente:

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

Reinicie el panel con su directorio de datos habitual y sus argumentos de inicio después de la instalación. La comprobación de disponibilidad debe incluir `[PASS] mcp: streamable-http available`. **Integrations → MCP** muestra el estado del entorno de ejecución y un comando de instalación que utiliza el ejecutable real de Python de ese servidor. **Re-check** actualiza este estado sin recargar la página; no instala paquetes ni reinicia el servidor.

El complemento MCP utiliza el [SDK oficial de Python de MCP](https://github.com/modelcontextprotocol/python-sdk).`deploy/constraints-mcp.txt` fija la versión del SDK y las dependencias probadas.

## Emitir una conexión

1. Introduzca una etiqueta y elija los espacios de trabajo y los chats que el cliente puede leer.
2. Seleccione las herramientas individualmente o utilice un ajuste preestablecido. Solo se ofrecen las herramientas implementadas.
3. Elija 1, 7, 30 o 90 días, o un vencimiento personalizado de entre un minuto y 90 días.
4. Pulse **Create connection**. El token aparece una sola vez junto a la configuración del cliente.
5. Copie el token y la configuración y, a continuación, ejecute **Check connection**. Esto inicializa MCP y enumera las herramientas permitidas; **no se lee ningún mensaje**. El resultado muestra la versión del protocolo, los nombres de las herramientas, el recuento y el tiempo transcurrido.
6. Pulse **Done** cuando haya guardado la credencial. El sondeo conserva el formulario y la tarjeta que se muestra una sola vez. Al bloquear el panel se borran los secretos mostrados.

La lista muestra el uso reciente, la última herramienta, la dirección y las solicitudes en el último minuto. **Revoke** finaliza el acceso. **Rotate token** revoca la credencial antigua y emite un reemplazo con el mismo alcance, herramientas y vencimiento; copie el reemplazo una vez. Los tokens de inicio de sesión del panel y las credenciales de Telegram no funcionan como tokens de MCP.

## Conectar su cliente

Seleccione el cliente en el panel y copie su configuración generada. Las configuraciones utilizan referencias a secretos o marcadores de posición explícitos; el token se copia por separado.

| Cliente | Configuración | Conexión |
| --- | --- | --- |
| Código de Claude | `.mcp.json` | HTTP, `type: "http"`, encabezado bearer |
| Claude Desktop | `claude_desktop_config.json` | Puente stdio local |
| Cursor | `.cursor/mcp.json` | HTTP con un encabezado de variable de entorno |
| VS Code Local | `.vscode/mcp.json` | HTTP con una entrada `promptString` de contraseña |
| Windsurf | `mcp_config.json` | HTTP con un marcador de posición de encabezado bearer |
| Otros clientes | URL y encabezado Authorization | HTTP transmitible |

TgWitness utiliza tokens bearer, sin descubrimiento OAuth. Utilice el puente stdio local para clientes cuyo conector remoto requiera OAuth. Para VS Code, las variables de entrada se aplican al entorno **Local** y no se reenvían a las sesiones de Copilot. Referencias de configuración: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

El punto de entrada canónico para un puente local es:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

Utilice el Python local del cliente con el extra de MCP instalado. Establezca `TGWITNESS_MCP_TOKEN` en su entorno protegido. Mantenga las credenciales fuera de los argumentos de comandos y las URL. `tgwitness-mcp` es el mismo punto de entrada. El antiguo módulo `tgwitness.mcp_bridge` y el nombre `TGWITNESS_ARCHIVE_TOKEN` se mantienen como rutas de compatibilidad con una advertencia; las nuevas configuraciones utilizan `mcp_server` y `TGWITNESS_MCP_TOKEN`.

## Cloudflare Tunnel

Reenvíe la ruta `/mcp` del panel y conserve el encabezado bearer. Al abrir la configuración de MCP como administrador se registra el origen actual del panel para esta ejecución. Para obtener una dirección estable disponible inmediatamente después del reinicio, configure `TGWITNESS_PUBLIC_URL` con el origen HTTPS del panel antes de iniciarlo. Los encabezados Host y de reenvío arbitrarios no registran una dirección de confianza. Las comprobaciones de Host y Origin rechazan orígenes de navegador no relacionados. Las respuestas utilizan `Cache-Control: no-store`; los valores de autorización nunca se registran.

Una dirección `*.trycloudflare.com` es temporal. Cuando el reinicio de un túnel cambie el nombre de host, actualice la URL pública configurada y la URL de MCP de cada cliente. Utilice un nombre de host estable para las configuraciones de cliente guardadas.

## Herramientas y límites

| Herramienta | Lee |
| --- | --- |
| `list_workspaces` | Espacios de trabajo concedidos |
| `list_chats` | Chats concedidos |
| `search_messages` | Texto de los mensajes guardados dentro del periodo seleccionado; `ranked=true` utiliza [búsqueda de texto completo](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/) (formas de palabras, mejores coincidencias primero, `next_offset` paginación) |
| `get_message_versions` | Versiones capturadas y observaciones de eliminación |
| `get_message_context` | ID de mensajes capturados cercanos |
| `get_journal_event` | Un registro saneado con su referencia de origen |
| `get_capture_status` | Estado de la recopilación, registros de cobertura permitidos y `gap_summary`: números de mensajes nunca observados, por canal o supergrupo y para la secuencia de toda la cuenta ([detalles](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#missing-message-numbers-gap_summary)); elige un chat para ver su lista de lagunas |
| `get_activity_stats` | Mensajes por hora UTC y día de la semana, días de mayor actividad, porcentajes de edición y eliminación, remitentes, dominios y `@handles`, con cobertura ([detalles](https://phishdestroy.github.io/TgWitness/es/docs/reference/cli/#activity-statistics)) |
| `get_messages_by_date` | Mensajes guardados de un día natural en una zona horaria IANA especificada (`Europe/Kyiv`, `UTC`), según la hora indicada por Telegram; `from_utc` y `until_utc` indicar el día calculado, incluido el horario de verano |
| `get_pinned_messages` | Mensajes fijados en la última instantánea del estado del chat con sus versiones guardadas, y los avisos de fijación y desfijación observados en tiempo real. |
| `get_chat_stats` | Recuento básico de registros guardados para un chat o para todos los chats incluidos en el ámbito, primera y última observación, y `gap_summary`; utilízalo antes de realizar una lectura de gran volumen |
| `get_topics` | Temas del foro a partir de los mensajes del servicio de temas guardados: historial de títulos, temas cerrados u ocultos, recuento de mensajes guardados |
| `get_media` | Una imagen conservada como vista previa en formato JPEG con resolución reducida (como máximo 36 KB), devuelta como imagen junto con su SHA-256 y el `media.saved` registro; el archivo se compara primero con su hash registrado, mientras que el resto de archivos solo devuelven metadatos |
| `export_messages` | Solo línea de comandos, no seleccionada por defecto: guarda las observaciones como JSON Lines ([detalles](https://phishdestroy.github.io/TgWitness/es/docs/reference/cli/#export)); no disponible a través de MCP |

Todas las herramientas son de solo lectura (`readOnlyHint`) y declara un esquema de salida; los campos que no figuren entre los declarados se devuelven tal cual. `tools/list` Solo devuelve las herramientas concedidas a esa conexión. Se rechazan las llamadas a otras herramientas. Las herramientas de contexto de grupo, episodio, terminología y cadena de respuestas no están disponibles en esta versión; no se incluye su backend de paquete de contexto independiente.

Cada lectura comprueba el token, la herramienta y el alcance del espacio de trabajo/chat, incluso después de que finalice el trabajo de la base de datos. Los límites son 60 solicitudes por minuto, 50 registros por página, 64 KiB por resultado y un tiempo límite de archivo de ocho segundos. Una llamada MCP cuyo tiempo de espera se agota devuelve un error de herramienta solicitando un período más acotado o un límite inferior.

Los resultados de los mensajes incluyen `untrusted_content: true`, los ID de espacio de trabajo/chat/mensaje, la secuencia del evento, el hash guardado y un enlace al panel. Se omiten los objetos de Telegram sin procesar, los hashes de acceso, las sesiones y las claves. Se marca el truncamiento de texto. Las ediciones, los avisos de eliminación y `missing_on_recheck` son observaciones distintas. La ausencia de registros no demuestra que un evento no haya ocurrido nunca.

Trate las instrucciones dentro de los mensajes capturados como pruebas, nunca como instrucciones para el cliente. El acceso de solo lectura impide realizar cambios en el archivo; aun así, el cliente puede retener el contenido que tiene permiso para leer. Los hashes identifican los registros guardados y respaldan las comprobaciones de integridad; no demuestran la autoría en Telegram ni que la captura sea completa.
