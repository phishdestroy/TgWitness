# Telegram · Chats secretos: implementación y demostración

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/secret-chats/

Comprender la implementación independiente de Chat secreto, probar la interfaz ficticia y revisar los defectos pendientes.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentación](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

**Estado comprobado el 6 de noviembre de 2026:** existe una implementación independiente de Chats secretos en desarrollo. No se ha fusionado con la rama `main` publicada en `3d23e52b647b`. El recopilador estándar y la exportación Takeout no recopilan Chats secretos. El escenario interactivo del sitio web muestra la interfaz con datos ficticios; no permite la comunicación a través de Telegram.

## Dónde se encuentra la implementación

La confirmación `0e60f88e` ha añadido **Sources → Pseudo-secret** en la rama de desarrollo local `fix/panel-routes-sessions`. La instantánea revisada es `bb8788fb685c`. Su implementación incluye `tgwitness/secret_chats.py`, rutas de la aplicación, `tgwitness/static/views/secret-chats.js` y pruebas específicas.

El complemento opcional `secret-chats` de esa rama utiliza [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat), anclado a `d87bf037b90060383c7b704d8a06ebb98c621c6f`. La biblioteca implementa el protocolo de chat de extremo a extremo de Telegram sobre la autorización Telethon existente de la cuenta. La mera instalación de esa biblioteca no añade la integración que falta a `main`.

## Qué hace la interfaz de desarrollo

| Acción | Comportamiento registrado |
| --- | --- |
| Iniciar un chat por nombre de usuario o ID de usuario | Envía una solicitud; el otro participante debe aceptarla. |
| Aceptar una solicitud entrante | TgWitness se convierte en el punto final receptor de ese chat. La aceptación automática es una configuración independiente, desactivada por defecto. |
| Enviar o recibir un mensaje | Añadir un registro `secret_chat.message` saliente o entrante y mostrarlo en el hilo. |
| Recibir un archivo adjunto | Descifralos, almacena sus bytes según SHA-256 y registra `secret_chat.file`. |
| Recibir un aviso de temporizador o de eliminación | Registrar el aviso y conservar el contenido capturado anteriormente. |
| Revisar la conversación | Mostrar mensajes, archivos, avisos y la visualización de claves. La pestaña abierta se actualiza cada cuatro segundos. |

En una versión de desarrollo que incluya la integración, el operador activa el módulo para la cuenta seleccionada y lo conecta. Para iniciar, aceptar y enviar mensajes es necesario tener permiso para interactuar y que la protección de solo lectura de la cuenta esté desactivada. El otro participante debe aceptar un nuevo chat saliente. Estos controles no están presentes en la aplicación publicada en la revisión anterior.

Solo se incluyen los chats creados o aceptados por esta sesión de TgWitness. Los chats secretos existentes en un teléfono permanecen en ese dispositivo. La importación de una sesión no proporciona sus claves de cifrado independientes. El material de claves y los contadores de los chats secretos se almacenan en la bóveda del espacio de trabajo; los mensajes conservados y los archivos descifrados siguen las protecciones habituales de almacenamiento del espacio de trabajo.

## Demostración en la página web

El escenario «**Try Secret Chat**» del sitio web presenta una conversación ficticia. Permite al lector iniciar una solicitud, simular su aceptación, enviar un mensaje de muestra, recibir una respuesta y un archivo predefinidos, e inspeccionar un temporizador y un aviso de eliminación. También se puede aceptar una solicitud entrante. Los controles etiquetan explícitamente las acciones simuladas de los interlocutores.

Este escenario se ejecuta en la memoria del navegador. Al reiniciar o recargar la página, se borra. No inicia sesión, no se conecta a Telegram, no crea claves de cifrado reales ni altera las descargas de muestras firmadas. Los mensajes que muestra no constituyen pruebas firmadas. El escenario muestra la interacción prevista; no certifica que la implementación del desarrollo esté lista.

## Comprobaciones y defectos pendientes

Las cinco pruebas existentes abarcan la persistencia de claves cifradas, el ciclo de vida y los registros de mensajes, la política de aceptación de entradas, el envío de solo lectura y la exportación de archivos adjuntos. Superaron las pruebas con la biblioteca fijada durante la revisión del 6 de noviembre. Tres comprobaciones sintéticas adicionales reprodujeron defectos en la misma instantánea:

| Resultados | Consecuencia |
| --- | --- |
| El cierre evita el `read_only` | La ruta de cierre puede realizar una acción remota cuando se deban bloquear las interacciones. |
| La búsqueda de duplicados solo se realiza en los registros recientes de 500. | Una reproducción anterior puede crear un duplicado tras reiniciar. |
| Si falla la descarga de un archivo adjunto, se elimina su entrada pendiente. | Un fallo transitorio provoca la pérdida de la tarea de reintento. |

Se trata de fallos pendientes, también registrados en la auditoría [publicada](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md). Las cinco pruebas superadas no cubren estos fallos. La revisión utilizó entornos de trabajo sintéticos y simuló operaciones de Telegram; no repitió un protocolo de autenticación en tiempo real ni evaluó la implementación en producción.
