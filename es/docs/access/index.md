# Compartir un caso

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/access/

Comparta el caso que alguien necesite. Mantenga el control sobre el resto.

01**Seleccione las pruebas**

Espacios enteros o chats sueltos.

02**Seleccione las acciones**

Ver, exportar o solo las operaciones que necesiten.

03**Establezca los límites**

Un token personal con caducidad, límites de sesión y reglas de IP si lo desea.

El ámbito de recopilación determina qué se registra. El ámbito de acceso determina lo que una persona puede ver y hacer.

## Conceder acceso a alguien

1. Como administrador, abra **Acceso**.
2. Póngale nombre y elija espacios y chats.
3. A un revisor le basta con **Ver**. Añada **Exportar** para las descargas.
4. Establezca los límites y, a continuación, pulse **«Crear acceso**».
5. Copie el token (se muestra una vez) y envíelo en privado junto con la dirección del panel.
6. Compruebe antes lo que verá en una sesión de navegador aparte.

## Comience por la tarea que deben realizar

| Persona | Acceso | Resultado |
| --- | --- | --- |
| Revisor | Chats seleccionados; solo lectura | Lee el chat, no puede cambiar nada. |
| Analista | Chats seleccionados; ver y exportar | Lee y descarga lo que el caso necesita. |
| Operador | Espacios de trabajo completos seleccionados; fuentes y recopilación | Decide qué se observa e inicia y detiene recolectores. |

Son solo ejemplos, no roles fijos. El acceso limitado a chats nunca recibe ajustes de cuenta ni exportaciones completas del diario. El acceso a todos los espacios incluye las cuentas añadidas después.

## Puede cambiar de opinión en cualquier momento

Edite el acceso cuando quiera; se aplica desde la siguiente petición. Termine una sesión o revóquelo todo. Los archivos ya descargados no se pueden recuperar. La recogida sigue en marcha.

**Límites de sesiones y direcciones IP**

Limite sesiones paralelas e inicios de sesión, ponga una fecha de fin, permita IPs o subredes o fije el acceso a la IP del primer inicio. La caducidad cuenta la inactividad; un panel abierto cuenta como activo. Detrás de un proxy, compruebe qué IP de cliente ve la aplicación.

**La clave principal y el registro de actividad**

El token principal se queda con el administrador. El acceso emitido no puede gestionar el acceso de otros ni abrir la consola de administración. Los cambios de acceso y las sesiones se firman en el diario, sin tokens. El administrador del servidor sigue viéndolo todo.

Los siete permisos y las reglas de sesión: [referencia de acceso](https://phishdestroy.github.io/TgWitness/es/docs/reference/access/).
