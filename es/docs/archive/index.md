# Explorar el archivo

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/archive/

Encuentra el mensaje. Comprueba la fuente. Construye el caso.

01**Incluir el historial**

Traiga al espacio los mensajes antiguos de sus fuentes activas.

02**Sigue las fuentes**

Busque y abra el mensaje guardado detrás de cada resultado.

03**Mantén clara la transición**

Su análisis en un archivo, la evidencia firmada al lado.

Los registros capturados, el texto reconocido y las conclusiones de los analistas se mantienen bien diferenciados.

## Cargar mensajes anteriores

1. **Fuentes → Chats incluidos**: revise los chats activos e inicie la observación.
2. **Cargar historial completo**. Usa la lista de fuentes tal como está en ese momento.
3. **Pausar historial** / **Continuar historial** cuando quiera. Tras un reinicio, reanude a mano.
4. Revise el resultado por fuente y la cola de descargas, y guarde el informe de progreso firmado con la exportación.

Esto llena el espacio. Exportar un solo chat a HTML/JSON es otra cosa. [Detalles](https://phishdestroy.github.io/TgWitness/es/docs/reference/history/).

## Busca primero y luego decide sobre la IA

1. **Diario** busca en local, con filtros por fuente y fecha.
2. Busque una frase o un dominio y abra el registro y sus versiones.
3. Para la IA, el administrador configura un proveedor en **Integraciones**. Luego **Preguntar al archivo**: elija chats y un periodo, mire **Datos enviados al modelo** y desmarque lo que no deba salir.
4. Compruebe las citas, guarde la respuesta como informe y añada sus notas.

La búsqueda no necesita IA. Los informes guardan sus fuentes y revisiones, aparte del diario firmado. [Configurar el proveedor](https://phishdestroy.github.io/TgWitness/es/docs/reference/analysis/).

## Elige la conexión que necesites

| Tarea | Abrir | Configuración |
| --- | --- | --- |
| Dejar que un cliente de IA lea chats elegidos | **Integraciones → MCP** | [Instale MCP, cree un token limitado y conecte](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/) |
| Reconocer texto en archivos multimedia guardados | Un registro `media.saved` → **Reconocer archivo adjunto** | [Configure el worker local de Docker](https://phishdestroy.github.io/TgWitness/es/docs/reference/media-analysis/) |
| Enviar eventos a n8n o a un SIEM | **Integraciones → Webhooks salientes** | [Añada un receptor, compruebe el HMAC y descarte IDs repetidos](https://phishdestroy.github.io/TgWitness/es/docs/reference/webhooks/) |

**¿Qué token de acceso va en cada sitio?**

El acceso al panel es para personas. MCP tiene sus propios tokens de solo lectura y los webhooks su propio secreto HMAC. Ninguno necesita una sesión de Telegram.

[Compartir el acceso al panel](https://phishdestroy.github.io/TgWitness/es/docs/access/) o [configurar un cliente MCP](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/).

## Presentar las fuentes y las conclusiones

Ponga el informe junto al ZIP firmado. El informe es su lectura de las fuentes; el ZIP es lo que verifica el destinatario.

[Exportar y verificar](https://phishdestroy.github.io/TgWitness/es/docs/exports/) · [Llevar a cabo una investigación completa](https://phishdestroy.github.io/TgWitness/es/docs/cases/)
