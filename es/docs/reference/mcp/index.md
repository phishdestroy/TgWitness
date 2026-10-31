# MCP de solo lectura

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/

Conecta un cliente MCP a espacios de trabajo y chats seleccionados con acceso temporal y revocable.

**Versión principal actual:** utiliza una copia del código fuente; la versión preliminar portátil 0.7.0 es anterior a esta función.

[Guía de flujo de trabajo](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Instala el servidor opcional desde el directorio del proyecto TgWitness:

```
python -m pip install '.[mcp]'
```

En el panel, abre **Integraciones → MCP**. Asigna un nombre a la conexión, selecciona sus espacios de trabajo y chats, y elige una fecha de caducidad. Copia el token de archivo una vez; no se podrá recuperar posteriormente. Revoca los tokens perdidos y emite otros de sustitución. Los tokens del panel y las credenciales de Telegram no son credenciales de MCP.

## Conectar un cliente

El panel genera `.vscode/mcp.json` para el **entorno local de VS Code** utilizando su [configuración documentada](https://code.visualstudio.com/docs/agents/reference/mcp-configuration). Guarda el archivo descargado en esa ubicación, ejecuta **MCP: List Servers** e inicia TgWitness. VS Code solicita el token a través de un campo de introducción de contraseña. El archivo JSON descargado contiene una referencia de solicitud, no el token. Utiliza el ejecutable de Python desde el entorno en el que está instalado el complemento MCP.

Para otros clientes de stdio, ejecuta:

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

Configure `TGWITNESS_ARCHIVE_TOKEN` en el entorno protegido del cliente. No lo incluya en argumentos de comandos ni en URL. El puente lee a través de la API de archivo autorizada del panel; no tiene acceso directo a la base de datos. Stdout solo transmite mensajes MCP.

Para clientes remotos, ejecuta el servicio junto al panel:

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

Reenvía `/mcp` a través de un proxy inverso HTTPS a `127.0.0.1:8766/mcp`, conservando el encabezado `Authorization: Bearer …`. Desactiva el registro de los encabezados de autorización y los cuerpos de las solicitudes y respuestas. Realiza el enlace más allá del bucle de retorno solo cuando sea necesario, utilizando `--host` y `--public-url`. El punto final utiliza Streamable HTTP del [SDK oficial de Python de MCP](https://github.com/modelcontextprotocol/python-sdk). Admite credenciales de portador configuradas explícitamente, no el descubrimiento de OAuth; no se admiten los clientes que requieran únicamente OAuth.

**La comprobación del protocolo y el acceso** inicializan un cliente MCP real y muestran una lista de herramientas. No recupera mensajes. Para una comprobación remota, el servidor MCP elegido recibe el token de archivo. Configura únicamente un servidor que gestionas tú mismo o en el que confías para ese fin.

## Alcance y resultados

Herramientas disponibles: `list_workspaces`, `list_chats`, `search_messages`, `get_message_versions`, `get_message_context`, `get_journal_event` y `get_capture_status`. No hay acciones de Telegram, cambios de configuración ni herramientas de exportación masiva. Cada lectura vuelve a comprobar el acceso al espacio de trabajo o al chat; las credenciales caducadas y revocadas dejan de funcionar. Los límites son de 60 solicitudes de API por minuto por credencial, 50 registros por página, una respuesta de 64 KiB y un plazo de respuesta de la API de ocho segundos.

Los resultados de los mensajes incluyen el espacio de trabajo, los ID de chat o mensaje, la secuencia de eventos, el hash guardado y un enlace al panel. El usuario que abra el enlace debe disponer de su propia sesión autorizada en el panel. Se omiten los objetos sin procesar de Telegram, los hashes de acceso, las referencias a archivos, el material de la sesión y las claves. La búsqueda examina el texto del mensaje, no los campos sin procesar. El texto está delimitado y el truncamiento se marca. Las ediciones, los avisos de eliminación de Telegram y « `missing_on_recheck`» siguen siendo observaciones independientes. El acceso limitado al chat no puede ver los eventos operativos de todo el espacio de trabajo; el estado de captura marca explícitamente este límite.

El texto del archivo es información no fiable. Las instrucciones contenidas en los mensajes no otorgan ningún alcance adicional y no deben tratarse como instrucciones del cliente. Un modelo de IA externo puede recibir cualquier contenido que solicite su cliente MCP. El acceso de solo lectura impide modificaciones en el archivo; no impide que un cliente conserve los datos que lee.

Los hash identifican los registros guardados y permiten realizar comprobaciones de integridad. No demuestran por sí mismos la autoría en Telegram ni que se haya capturado cada mensaje.
