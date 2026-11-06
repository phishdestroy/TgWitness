# Mostrador público

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/showcase/

Publica mensajes guardados de canales públicos seleccionados e instantáneas firmadas a través de enlaces caducables y revocables.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentación](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Implementación y recuperación](https://phishdestroy.github.io/TgWitness/es/docs/reference/deployment/)

![Implementación y recuperación](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

**«Acceso → Vitrina pública»** crea una página independiente de solo lectura utilizando el sistema de tokens de acceso existente. Lee las observaciones guardadas de la instalación. No inicia un recopilador, ni inicia sesión en Telegram, ni adquiere un canal para un visitante.

## Publicar una página

1. Guarda un perfil de origen para cada canal público que quieras mostrar. Un canal debe tener un nombre de usuario público en su último perfil guardado; los grupos y los chats privados no son válidos.
2. Abre **Acceso → Muestra pública** (o `/showcase-manage.html`) como administrador.
3. Selecciona canales de hasta 16 espacios de trabajo, introduce el título de la página pública y elige una duración del enlace de 1, 7 o 30 días. Las etiquetas internas de los espacios de trabajo no se publican. Se pueden incluir hasta 64 canales.
4. Revisa el texto de los canales seleccionados para su publicación y, a continuación, haz clic en **«Vista previa de los registros seleccionados**». La vista previa utiliza la misma proyección del lado del servidor que la página de visitantes.
5. Haz clic en **«Crear enlace de presentación**». Copia el enlace mientras esté visible. Ábrelo en un navegador aparte para revisar la página del destinatario antes de distribuirla.

El enlace contiene un token de acceso en su fragmento de URL. La página elimina el fragmento antes de realizar solicitudes a la API y lo sustituye por una sesión del navegador. Cualquier persona que disponga del enlace puede abrir el material seleccionado hasta su caducidad o revocación. Los nuevos enlaces permiten 100 sesiones simultáneas, cada una de una duración máxima de una hora. Los controles de acceso existentes también pueden aplicar restricciones de direcciones y límites de inicio de sesión a través de la API de concesión. El acceso normal de revisor es un modo diferente y sigue incluyendo los mensajes y archivos permitidos originalmente.

## Lo que ven los visitantes

| Visible | Se mantiene privado |
| --- | --- |
| Títulos seleccionados de canales públicos, nombres de usuario y fechas de observación de perfiles | Identidades de las cuentas, etiquetas internas del espacio de trabajo y fuentes no seleccionadas |
| Texto capturado y cada edición guardada | ID de remitente estructurados, nombres, nombres de usuario, números de teléfono y valores de perfil |
| Observaciones sobre eliminaciones con el texto guardado previamente, si está disponible | Archivos adjuntos, avatares, miniaturas, nombres de archivo y contenidos originales |
| Marcadores que indican que se ha registrado un autor, un perfil o un archivo adjunto | Metadatos de reenvío y respuesta, rutas de red, direcciones IP y credenciales |
| Recuento de eventos en canales seleccionados, cambios en la colección actual, latido e intervalo de puntos de control | Controles de recopilación y API estándar para la exportación de pruebas |
| Huella de firma, punto de control del diario y prueba de consistencia | Claves de firma y sesiones de Telegram |

**El texto de los mensajes públicos no se anonimiza automáticamente.** Un nombre, una mención, un número de teléfono o un enlace incluido en el mensaje sigue formando parte de dicho texto. `Redacted`Esto se aplica a los campos estructurados de autor/perfil. Revisa el contenido seleccionado antes de publicarlo, incluyendo las ediciones y eliminaciones conservadas.

La elegibilidad refleja el **último perfil de origen guardado**, no una consulta en tiempo real en Telegram. Si un perfil posterior ya no tiene un nombre de usuario de canal público, las nuevas solicitudes excluyen dicho canal. Actualiza los perfiles de origen cuando cambie la visibilidad pública. Es posible que los lectores ya tengan guardado material que hayan recibido anteriormente.

Los registros originales firmados permanecen inalterados. La proyección mostrada se firma por separado e incluye hash que hacen referencia a sus registros originales. Una firma de proyección autentica la declaración mostrada; no se trata de la firma del evento original sobre bytes censurados.

## Comprueba las firmas y la continuidad

Despliega **«Fingerprint & signed checkpoint»** y descarga una instantánea. Tras una actualización de la página, la descarga incluye la instantánea anterior del navegador y una prueba de consistencia de Merkle entre los límites de sus registros. La actualización automática se produce una vez por minuto mientras la página está visible y muestra su primera página de observaciones.

Una vez instalado TgWitness, comprueba el archivo descargado sin conexión:

```
python -m tgwitness.showcase_verify showcase.json --fingerprint TRUSTED_COLLECTOR_SHA256
```

La huella digital debe proceder de una referencia de confianza independiente. Para compararla con una instantánea que hayas guardado tú mismo, utiliza `--previous earlier.json`; esto anula la instantánea anterior incluida en la descarga. La prueba actual debe comenzar en ese límite guardado. Los clientes autenticados pueden solicitar esa prueba utilizando `GET /api/showcase/{workspace_id}?challenge=<32-hex-random>&from_count=<retained-count>`. Un diario más corto devuelve un código de estado HTTP 409 en lugar de restablecer el límite de forma silenciosa.

El punto de control firmado se registra en el **Diario completo del recopilador**, incluyendo su número de registros y el hash opaco del encabezado. Los recuentos de mensajes mostrados solo se aplican a los canales públicos seleccionados. La página nunca muestra el contenido del otro diario. Se trata de recuentos de eventos, no de mensajes únicos. Los ajustes describen la configuración actual, no todos los intervalos de grabación anteriores.

La verificación de la firma y la coherencia permite detectar cambios con respecto a un límite establecido. No recuenta de forma independiente los contadores firmados, ni certifica el origen de Telegram, ni demuestra que la captura se haya realizado de forma ininterrumpida, ni sustituye a un testigo independiente. Para esa revisión, utiliza el [verificador de pruebas](https://github.com/phishdestroy/TgWitness/blob/main/docs/TRUST.md), [el testigo independiente](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/) y [el registro a escala probada](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/). Las instalaciones sintéticas están claramente etiquetadas como sintéticas.

## Revocar o alojar la página

Utiliza **«Revocar»** en el gestor de vitrinas o en la sección **«Acceso»** existente para cerrar el enlace y finalizar todas sus sesiones. El visitante borra los registros mostrados cuando una solicitud detecta que el acceso ha finalizado. La caducidad y los permisos se comprueban en cada solicitud. Las autorizaciones de vitrina no se pueden convertir en acceso ordinario al panel in situ; crea una nueva autorización para cambiar de modo.

Sirve la página a través de la dirección HTTPS existente de la instalación. Publicar un enlace no abre un nuevo puerto, ni crea un túnel, ni cambia el DNS. El HTML y la API permanecen en la instalación del usuario. Un visitante de la demostración no puede utilizar las API habituales de mensajes, perfil, archivos multimedia, exportación o gestión con este acceso.
