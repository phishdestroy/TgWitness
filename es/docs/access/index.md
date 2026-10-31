# Compartir un caso

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/access/

Comparta el caso que alguien necesite. Mantenga el control sobre el resto.

01**Seleccione las pruebas**

Seleccione espacios de trabajo de cuentas completas o chats registrados individualmente.

02**Seleccione las acciones**

Permita la visualización, la exportación o los permisos operativos específicos que la persona necesite.

03**Establezca los límites**

Emitir un token personal con fecha de caducidad, límites de sesión y restricciones de IP opcionales.

El ámbito de recopilación determina qué se registra. El ámbito de acceso determina lo que una persona puede ver y hacer.

## Conceder acceso a alguien

1. Inicie sesión como administrador y abra **«Acceso**».
2. Indique el nombre de acceso y seleccione los espacios de trabajo y los chats.
3. Mantenga la opción **«Ver»** para un revisor. Añada **«Exportar»** en caso de que deban descargar los registros.
4. Establezca los límites y, a continuación, pulse **«Crear acceso**».
5. Copie el token que se muestra una sola vez. Envíelo de forma privada junto con la dirección del panel.
6. Compruebe la vista autorizada en una sesión de navegador independiente antes de facilitarla.

## Comience por la tarea que deben realizar

| Persona | Acceso | Resultado |
| --- | --- | --- |
| Revisor | Chats seleccionados; solo lectura | Lea la conversación capturada sin alterar la recopilación. |
| Analista | Chats seleccionados; ver y exportar | Revise y descargue los registros necesarios para el caso. |
| Operador | Espacios de trabajo completos seleccionados; fuentes y recopilación | Gestione lo que se supervisa e inicie o detenga los recopiladores. |

Se trata de configuraciones que usted elige, no de roles fijos. La configuración general de la cuenta y las exportaciones completas del registro permanecen restringidas al acceso limitado al chat, incluso cuando se habilita otro permiso. El acceso a todo el espacio de trabajo incluye cuentas futuras.

## Puede cambiar de opinión en cualquier momento

Modifique el acceso para determinar qué acciones pueden realizar las solicitudes posteriores. Finalice una sesión o revoque todo el acceso para poner fin a todas sus sesiones. Los archivos ya descargados no se pueden recuperar. Finalizar una sesión del panel no detiene la recopilación.

**Límites de sesiones y direcciones IP**

Limite las sesiones paralelas y los inicios de sesión válidos, establezca una fecha de finalización absoluta, permita direcciones IP o subredes, o vincule el acceso a la dirección utilizada en el primer inicio de sesión. La caducidad de la sesión se determina en función de la inactividad; la actualización de un panel abierto se considera actividad. Compruebe la dirección del cliente que muestra la aplicación cuando se ejecuta detrás de un proxy o un túnel.

**La clave principal y el registro de actividad**

El administrador conserva el token del panel principal. Los usuarios con acceso concedido no pueden gestionar el acceso de otras personas ni abrir la consola de administración. La consola muestra la actividad de los procesos en curso en todos los espacios de trabajo; los registros de acceso firmados conservan los eventos de concesión y de sesión sin necesidad de tokens. Los espacios de trabajo comparten el proceso anfitrión y no aíslan los datos del administrador del servidor.

Utilice la [referencia completa de permisos](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/) para los siete permisos, las reglas de sesión y los límites del administrador.
