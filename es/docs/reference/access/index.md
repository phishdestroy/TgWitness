# Acceso y permisos

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/access/

Configure el acceso a cuentas y chats, seleccione los permisos, limite las sesiones y las direcciones IP, y revoque el acceso.

Conceda a un revisor acceso a un chat, a un analista permiso para exportar un caso o a un operador el control de cuentas seleccionadas. Cada persona dispone de su propio token. El token del panel principal lo conserva el administrador.

[Configuración de la cuenta](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/) · [Rutas de conexión](https://phishdestroy.github.io/TgWitness/es/docs/reference/connection/) · [Modelo de seguridad](https://phishdestroy.github.io/TgWitness/es/docs/reference/security/)

## Dos ámbitos de aplicación, dos funciones distintas

**El ámbito de recopilación** determina qué registra una cuenta: chats seleccionados, una carpeta de Telegram o la cuenta completa. **El ámbito de acceso** determina cuáles de esas cuentas y chats registrados puede ver y utilizar otra persona. Conceder acceso no implica unirse a un chat de Telegram, iniciar la recopilación ni otorgar permisos de la cuenta de Telegram.

Una autorización de acceso puede abrir espacios de trabajo seleccionados, chats específicos dentro de ellos o todos los espacios de trabajo. La inclusión de **todos los espacios de trabajo, incluidos los que se añadan posteriormente**, también abarca futuras cuentas. Seleccione los espacios de trabajo de forma explícita cuando un caso deba limitarse a ellos.

## Conceder acceso a alguien

1. Inicie sesión como administrador principal y abra **«Acceso**».
2. En **«Conceder acceso a alguien**», introduzca un nombre que pueda reconocer en el registro.
3. Seleccione los espacios de trabajo y, cuando sea necesario, los chats individuales.
4. Seleccione lo que esta persona puede hacer. La opción **«Ver»** siempre está incluida.
5. Configure la fecha de caducidad, los límites de inicio de sesión y de duración de la sesión, así como las direcciones permitidas, según sea necesario.
6. Pulse **«Crear acceso**». Copie el token ahora: solo se muestra una vez.
7. Envíe la dirección del panel y el token de forma privada. El destinatario introduce dicho token en la página de inicio de sesión habitual; no necesita su token principal del panel ni una sesión de Telegram.

Abra el panel con el token generado en una sesión de navegador independiente y compruebe los chats visibles y las acciones permitidas antes de entregarlo.

## Seleccione los permisos

| Autorización | Qué permite |
| --- | --- |
| `view` | Lea los chats autorizados, los mensajes capturados, los perfiles, los archivos y los registros filtrados del diario. Siempre incluidos. |
| `export` | Se permite la exportación del historial de chat y de los expedientes. Las exportaciones de pruebas de todo el espacio de trabajo requieren acceso a dicho espacio en su totalidad. |
| `sources` | Gestione fuentes, instantáneas y capturas de perfiles. El acceso limitado a los chats solo puede actuar sobre los chats permitidos; la detección de fuentes en toda la cuenta y la configuración del ámbito de aplicación permanecen inactivas. |
| `collect` | Iniciar o detener un recopilador. Requiere acceso a todo el espacio de trabajo, ya que la recopilación afecta a la cuenta. |
| `interact` | Realice las interacciones compatibles con Telegram dentro del ámbito de acceso. El acceso limitado al chat no permite utilizar la vista previa de enlaces en toda la cuenta. |
| `settings` | Modifique la configuración de la recopilación, las marcas de tiempo, las notificaciones, las copias externas y los parámetros. Requiere acceso a todo el espacio de trabajo. |
| `account` | Inicie o cierre sesión en Telegram y gestione las rutas de conexión. Requiere acceso a todo el espacio de trabajo. |

Los permisos y el alcance se comprueban conjuntamente. Marcar un permiso no abre otros chats ni desbloquea una operación a nivel de espacio de trabajo para un acceso limitado a un chat. Para una exportación paralela, el acceso debe abarcar el chat exportado en todas las cuentas seleccionadas. Un acceso concedido no puede crear nuevos accesos, gestionar las sesiones de otras personas ni abrir la consola de administrador.

### Tres configuraciones útiles

| Persona | Ámbito de aplicación | Permisos |
| --- | --- | --- |
| Revisor | Chats grabados de un caso concreto | `view` |
| Analista que prepara un traspaso de funciones | Los chats que se deben investigar y exportar | `view`, `export`; añada `interact` únicamente si deben actuar a través de Telegram |
| Operador de recopilación | Espacios de trabajo completos seleccionados | `view`, `sources`, `collect`; añada `settings` o `account` únicamente cuando sea necesario |

Estos son ejemplos que se configuran mediante las casillas de verificación de permisos, no son roles fijos.

## Límites y sesiones

| Configuración | Cómo funciona |
| --- | --- |
| Sesiones paralelas | Limite el número de sesiones simultáneas a entre 1 y 100. Al alcanzar el límite, rechace el siguiente inicio de sesión o finalice la sesión más antigua. |
| Se permite el inicio de sesión | Limite el número de usos correctos del token para iniciar sesiones. Las sesiones existentes no se cierran simplemente porque se haya agotado el último inicio de sesión permitido. |
| Válido hasta | El acceso tiene una caducidad definitiva. Un acceso caducado no puede iniciar sesión ni seguir realizando solicitudes. |
| Minutos sin actividad | Tiempo de espera por inactividad de la sesión, de 5 minutos a 30 días. Las solicitudes exitosas lo amplían; un panel abierto puede mantenerse activo mediante sondeos. |
| Direcciones permitidas | Acepte direcciones IP específicas o subredes CIDR. Déjelo en blanco para permitir cualquier dirección, a menos que esté habilitada la vinculación al primer inicio de sesión. |
| Vincular al primer inicio de sesión | El primer inicio de sesión correcto establece la dirección autorizada para ese acceso. |

La IP es la dirección del cliente que ve la aplicación. Si se encuentra detrás de un proxy inverso o un túnel, compruebe la dirección que aparece en **«Sesiones abiertas»** antes de basarse en reglas de IP: de lo contrario, podría parecer que varios usuarios comparten la dirección del proxy.

## Modificar o retirar el acceso

Modifique una entrada en **«Accesos»** para cambiar su ámbito de aplicación, permisos o límites. Los cambios en el ámbito de aplicación y los permisos se comprueban en las solicitudes posteriores, incluidas las solicitudes de sesiones que ya estén abiertas. La revocación de un acceso pone fin a sus sesiones y hace que el token emitido quede inutilizable. **Las sesiones abiertas** también permiten al administrador finalizar una sesión concreta sin revocar todo el acceso.

La revocación no permite recuperar archivos que alguien ya haya descargado. Cerrar sesión, bloquear el panel o finalizar una sesión no detiene un recopilador en ejecución.

## Lo que puede ver el administrador

**El registro desde este inicio** combina los registros de proceso con la actividad del diario de cada espacio de trabajo: inicios de sesión, rechazos, cambios de ruta y acciones del operador. Se trata de una consola en memoria para el proceso actual, no de una copia permanente de cada mensaje. Los eventos de mensajes frecuentes permanecen en el diario en lugar de saturar la consola.

La concesión, modificación y revocación de accesos, así como el inicio o la finalización de sesiones, también generan registros firmados en el diario `access.*`. Los tokens no se incluyen en dichos registros. Los tokens emitidos y las credenciales de sesión se conservan como hash en la bóveda cifrada.

****Administrador principal y límite de confianza**** El token del panel principal no está sujeto a restricciones. Los inicios de sesión en el navegador con dicho token crean sesiones sujetas a los límites de sesión configurados por el administrador. Los scripts que envían el token principal directamente conservan acceso completo y no se contabilizan como sesiones de navegador. Se trata de un control de acceso a nivel de aplicación en una única instalación. Todos los espacios de trabajo comparten el proceso del servidor; esto no supone un aislamiento respecto al administrador del host. Mantenga la privacidad del token principal, las sesiones de Telegram, las claves de firma y el directorio de datos. Un token de testigo es una credencial independiente de estado y control, no un token de acceso al panel.
