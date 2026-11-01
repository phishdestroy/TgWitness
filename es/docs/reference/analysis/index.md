# Análisis de archivos

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/analysis/

Busca mensajes guardados, revisa las aportaciones de la IA y conserva informes analíticos con sus referencias de origen.

[Guía de flujo de trabajo](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Use **Registro** para realizar búsquedas locales sin IA. Para usar **Consulte el archivo**, primero habilite y configure un proveedor en **Integraciones**. El selector de espacio de trabajo elige la cuenta; el formulario selecciona los chats y el periodo de observación. La recuperación se realiza localmente. Una frase exacta o un dominio restringe la recuperación; un ID de mensaje solicita las versiones guardadas. Revise los extractos y abra sus registros en el diario o su contexto. No hay ninguna base de datos vectorial ni acción automática en Telegram.

## Proveedores y consentimiento

La IA viene desactivada por defecto en todos los espacios de trabajo. Solo el administrador principal puede configurar el modelo, el punto final, la clave API cifrada, los límites de contexto y salida, el tiempo de espera y el límite diario de solicitudes. La clave nunca se devuelve al navegador. Deja el campo de la clave en blanco para conservar la clave actual, o elimínala explícitamente.

Ollama utiliza su [punto final `/api/chat`](https://docs.ollama.com/api/chat) documentado con salida JSON sin streaming. Su dirección predeterminada es `http://127.0.0.1:11434` en el servidor de TgWitness. El operador puede cambiarla utilizando `TGWITNESS_AI_LOCAL_ENDPOINT`; no se trata de una dirección controlada por el modelo. Instala tú mismo el modelo seleccionado. TgWitness no lo descarga automáticamente.

El proveedor compatible debe tener una URL base que termine en `/v1` y admitir el [protocolo Chat Completions](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, modo de respuesta JSON, `max_completion_tokens` y `choices[0].message.content`. No se admiten los servicios que carezcan de estos campos. Las pruebas de conexión envían texto sintético y se contabilizan dentro del límite de solicitudes.

Cada solicitud utiliza la ruta externa configurada en el espacio de trabajo. Una ruta bloqueada o un MTProxy exclusivo para Telegram da lugar a un error; no hay reintento directo. Una dirección Ollama local configurada deliberadamente permite un destino privado, sin dejar de utilizar la ruta elegida. Para otros servicios privados se aplica la opción de activación del destino privado a nivel de servidor ya existente. El panel muestra el punto final realmente configurado.

Antes de la generación, **los datos enviados al modelo** muestran la solicitud: pregunta, fragmentos seleccionados, tipos de eventos, horas de observación y marcadores de cobertura. Las sesiones de Telegram, los campos sin procesar, las claves de los proveedores, los bytes de los archivos adjuntos y el registro completo no forman parte de ese contexto. Desmarca las fuentes no deseadas y, a continuación, aprueba explícitamente el procesamiento. Los proveedores externos pueden conservar el contenido enviado según sus propias políticas. La ejecución local significa que el punto final es local; no es una garantía sobre el comportamiento de un servicio configurado de forma independiente.

Hay un máximo de dos solicitudes simultáneas al proveedor a nivel global y una por espacio de trabajo. Una vista previa caduca a los diez minutos y puede generar una respuesta. Se muestran los recuentos de tokens comunicados por el proveedor; solo aparece una estimación de costes cuando se han configurado tanto las tarifas de entrada como las de salida. Los intentos fallidos también consumen el presupuesto diario de solicitudes. Los reintentos automáticos no consumen presupuesto adicional.

## Fuentes y limitaciones

La función de recuperación examina el texto de los mensajes guardados mediante una búsqueda léxica delimitada. Devuelve hasta 24 fuentes y señala los extractos truncados o los conjuntos de resultados incompletos. El periodo se refiere al **tiempo de observación**, no a una afirmación de que el historial de Telegram sea completo. Los eventos que abarcan todo el espacio de trabajo quedan excluidos del acceso limitado al chat. Los datos que faltan se describen como «no encontrados» en el archivo disponible.

El modelo no recibe herramientas. Sus identificadores de origen se cotejan con los registros seleccionados, se vuelven a comprobar los hash y las cadenas entre comillas deben aparecer en dichos registros. Los identificadores desconocidos, las citas modificadas y las afirmaciones sin citar dan lugar al rechazo de la respuesta. La aplicación crea enlaces; las URL generadas por el modelo no se utilizan como citas. Estas comprobaciones establecen la existencia de la fuente y la exactitud de la cita, no la veracidad de una inferencia. Revisa las inferencias contrastándolas con los registros antes de dar por ciertas.

## Informes

Guarda una respuesta revisada como un informe analítico independiente. Incluye el resumen del modelo, la cronología observada, los enlaces y los identificadores extraídos, los registros de edición y eliminación, los límites de cobertura y los hash de los eventos de origen. Se incluyen el proveedor, el modelo, el punto final, la hora y la versión de la plantilla de prompt. No se fusionan automáticamente las identidades.

Las revisiones y notas de los analistas se almacenan por separado del resumen del modelo. Los informes se guardan en archivos derivados cifrados, con un índice fuera del flujo de eventos firmado; los eventos y archivos multimedia originales no se modifican. Solo el propietario o el administrador pueden abrir un informe, y se vuelve a comprobar el acceso a la fuente. La descarga también requiere permiso de exportación . La versión 1 no firma los informes ni da a entender que las conclusiones del modelo sean pruebas verificadas. Límites: 100 informes por espacio de trabajo y 100 revisiones de analistas por informe.

Para el OCR manual y las transcripciones, consulta [«procesamiento de archivos multimedia](https://phishdestroy.github.io/TgWitness/es/docs/reference/media-analysis/)». Para el acceso de clientes, consulta [«MCP](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/)».
