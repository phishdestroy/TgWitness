# Explorar el archivo

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/archive/

Encuentra el mensaje. Comprueba la fuente. Construye el caso.

Estas herramientas están disponibles en la rama principal actual. La versión preliminar portátil 0.7.0 es anterior a ellas; utiliza una descarga del código fuente para este flujo de trabajo.

01**Incluir el historial**

Carga los mensajes anteriores de tus fuentes habilitadas en el espacio de trabajo.

02**Sigue las fuentes**

Busca en el archivo y abre el mensaje guardado correspondiente a cada resultado.

03**Mantén clara la transición**

Guarda tu análisis por separado y exporta las pruebas firmadas junto a él.

Los registros capturados, el texto reconocido y las conclusiones de los analistas se mantienen bien diferenciados.

## Cargar mensajes anteriores

1. Abra **Fuentes → Chats en alcance**, revise los chats habilitados e inicie la observación.
2. Selecciona **«Cargar historial completo**». La ejecución utiliza la lista de fuentes seleccionada en ese momento.
3. Utiliza **«Pausar historial»** y **«Continuar historial»** según sea necesario. Tras un reinicio, reanuda explícitamente.
4. Comprueba los resultados por fuente y la cola de archivos adjuntos. Guarda el informe de progreso firmado junto con la exportación de pruebas.

Esto llena el espacio de trabajo con los mensajes disponibles. La exportación en formato HTML/JSON por chat es una operación independiente. [Historial y detalles de recuperación](https://phishdestroy.github.io/TgWitness/es/docs/reference/history/).

## Busca primero y luego decide sobre la IA

1. Abra **Registro** para realizar búsquedas locales. Elija un espacio de trabajo y use los filtros de fuente y de tiempo.
2. Busca una frase o un dominio. Abre el registro correspondiente y sus versiones guardadas.
3. Para el análisis con IA, el administrador habilita y configura un proveedor en **Integraciones**. Abra **Consulte el archivo** y elija los chats y un periodo. Revise **Datos enviados al modelo** y desmarque los extractos no deseados antes de aprobar la solicitud.
4. Comprueba las citas obtenidas. Guarda la respuesta como un informe y añade tus propias revisiones o notas.

Las búsquedas se realizan de forma local, sin IA. Los informes analíticos conservan las referencias de las fuentes y el historial de revisiones; están separados del registro firmado. [Configuración del proveedor e informes](https://phishdestroy.github.io/TgWitness/es/docs/reference/analysis/).

## Elige la conexión que necesites

| Tarea | Abrir | Configuración |
| --- | --- | --- |
| Lee chats seleccionados desde un cliente de IA | **Integraciones → MCP** | [Instala el complemento MCP, genera un token con ámbito limitado y conecta el cliente](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/) |
| Reconocer texto en archivos multimedia guardados | Un registro `media.saved` → **Reconocer archivo adjunto** | [Configurar el worker local de Docker y los archivos de lenguaje y modelo necesarios](https://phishdestroy.github.io/TgWitness/es/docs/reference/media-analysis/) |
| Enviar eventos a n8n o a un SIEM | **Integraciones → Webhooks salientes** | [Añadir un destinatario, verificar el HMAC y deduplicar los ID de eventos](https://phishdestroy.github.io/TgWitness/es/docs/reference/webhooks/) |

**¿Qué token de acceso va en cada sitio?**

El acceso al panel está reservado a las personas que revisan el caso. Las conexiones MCP obtienen tokens de archivo independientes de solo lectura. Un receptor de webhooks utiliza su propio secreto HMAC. Ninguno necesita un archivo de sesión de Telegram.

[Compartir el acceso al panel](https://phishdestroy.github.io/TgWitness/es/docs/access/) o [configurar un cliente MCP](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/).

## Presentar las fuentes y las conclusiones

Conserva el informe analítico revisado junto con el archivo ZIP de pruebas firmado. El informe explica tu interpretación de las fuentes; el archivo ZIP permite al destinatario contrastar el registro guardado con una huella digital y un punto de control independientes y fiables.

[Exportar y verificar](https://phishdestroy.github.io/TgWitness/es/docs/exports/) · [Llevar a cabo una investigación completa](https://phishdestroy.github.io/TgWitness/es/docs/cases/)
