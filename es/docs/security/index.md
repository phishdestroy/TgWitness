# Mantenga la seguridad

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/security/

Conozca las rutas de Telegram, las listas de proxies públicos y los servicios externos opcionales. Sepa qué ofrece cada opción, qué protegen y qué aspectos quedan en sus manos.

**127.0.0.1**Dirección del panel por defecto

**256 bits**token de panel aleatorio

**0**CDN, herramientas de análisis o fuentes remotas

**Ed25519**Firma en cada registro

## Donde se encuentra todo

El recopilador, su panel y todos los registros guardados permanecen en el ordenador o servidor en el que se ejecuta. Telegram es el único destino por defecto; cada uno de los demás es una opción independiente.

06 / LO QUE SALE DE LA MÁQUINASu instalación

SU ORDENADOR O SERVIDOR

**Panel**127.0.0.1:8787 · token de portador

**Recopilador**Un cliente de Telegram por espacio de trabajo

DIRECTORIO DE DATOS

**Registro**SQLite · encadenado por hash · firmado

**Medios de comunicación**archivos nombrados según SHA-256

**Vault**Fernet · sesión, par de API, clave de firma, proxy

- **Telegram**Siempre · a través de su ruta

  Conexión MTProto de la cuenta: directa, SOCKS5, HTTP o MTProxy. El modo «Ocultar IP» espera a que haya un proxy operativo. La conexión directa de reserva requiere un modo que lo permita explícitamente.
- **Texto externo**Opcional · desactivado por defecto

  El registro, los archivos y los puntos de control se cifran con AES-GCM antes de subirlos a un almacenamiento compatible con S3. La clave la conserva usted; los archivos adjuntos se nombran mediante hash con clave, no mediante el hash de su contenido.
- **Notificaciones**Opcional · desactivado por defecto

  Problemas y recuento de cambios con los títulos de los chats. Los extractos de los mensajes solo se envían si usted activa esta opción.
- **Autoridad de sellado de tiempo**Opcional · desactivado por defecto

  Únicamente el SHA-256 de un punto de control firmado y un nonce aleatorio. Sin mensajes ni nombres de chat.
- **Witness**Opcional · desactivado por defecto

  Obtiene puntos de control firmados y contadores de capturas mediante un token de solo lectura. No puede leer conversaciones ni modificar la configuración.

Por defecto: solo la conexión a Telegram sale de este equipo.

Los destinos opcionales se configuran por espacio de trabajo. El texto de los mensajes y los archivos multimedia se almacenan sin cifrar en el directorio de datos: protéjalo mediante el cifrado del disco y los permisos de los archivos.

## Lo que cada secreto desvela

| Secreto | Dónde se almacena | Qué posibilidades ofrece | En caso de filtración |
| --- | --- | --- | --- |
| **Token de panel** | `panel-token.txt` en el directorio de datos; el navegador lo conserva únicamente para la pestaña correspondiente | Todo lo que ofrece cada espacio de trabajo: leer y exportar, modificar el alcance, iniciar sesión en cuentas | Detenga TgWitness, elimine `panel-token.txt` y vuelva a iniciarlo: se creará un nuevo token |
| **Sesión de Telegram** | Almacén cifrado (`credentials.enc`) | La propia cuenta de Telegram | Finalice la sesión en Telegram en *Ajustes → Dispositivos* |
| **Clave de firma** | Almacén cifrado (`signing.enc`) | Registros firmados que se verifican mediante su huella digital | Los puntos de control almacenados en otro lugar, un registro de testigos y las marcas de tiempo muestran lo que existía anteriormente. |
| **Clave de la bóveda** | `vault.key` junto a los datos, o una clave maestra externa para un nuevo directorio de datos | Descifrando la caja fuerte | Considere que la clave de sesión y la clave de firma también se han filtrado |
| **Token de Witness** | En el servidor de TgWitness | Solo lectura: puntos de control firmados y estado del sistema | Elimínelo de la página «Witness»; cree uno nuevo |
| **Texto clave para uso externo** | Vault; descárguelo una sola vez para poder recuperarlo | Descifrado de la copia externa | Cualquiera que también posea los objetos almacenados puede descifrarlos: considere esa copia como expuesta |

## Qué cubren las medidas de protección

### Cubierto

- Un registro modificado, eliminado o reordenado en una exportación: la cadena de hash o la firma ya no se verifican.
- Un registro recortado o reconstruido tras un punto de control que se conservaba en otro lugar: el punto de control conservado ya no coincide.
- Adivinación del token del panel: 256 bits aleatorios, comparados en tiempo constante; tras 15 intentos fallidos por minuto, se rechaza la dirección.
- Contenido de chat hostil: el texto se inserta como texto, nunca como HTML; los archivos adjuntos se descargan como archivos; el panel no carga nada de otros sitios web.
- Un directorio de datos copiados con una clave de almacén externa: las sesiones y las claves de firma permanecen cifradas sin la clave maestra.

### A su criterio

- El titular de la clave principal tiene control total. Conceda a otras personas acceso limitado a las cuentas, los chats y las acciones que necesiten; mantenga la clave principal en la más estricta confidencialidad.
- Un administrador del servidor puede leer todo el contenido, así como reescribir y volver a firmar el registro. Guarde la huella digital y los puntos de control en otro sistema.
- TgWitness no cifra el texto de los mensajes ni los archivos multimedia. Utilice el cifrado de disco y establezca permisos estrictos.
- El protocolo HTTP sin cifrar fuera de localhost expone el token en la red. Utilice HTTPS o un túnel SSH.
- Las firmas demuestran que lo registrado no ha sido modificado, no que se haya registrado cada evento de Telegram.

[Comparta el acceso a un caso](https://phishdestroy.github.io/TgWitness/es/docs/access/) con permisos, plazos de caducidad y límites de sesión. El token de testigo sigue siendo una credencial independiente.

## Reforzar una instalación

0 de 8 completado

1. **Utilice una cuenta de Telegram específica**; nunca su cuenta principal. El token del panel y la sesión le proporcionan un control total sobre ella.
2. **Mantenga el panel en 127.0.0.1.** Acceda a él de forma remota únicamente a través de HTTPS (la configuración de Caddy incluida) o de un túnel SSH.
3. **Cifre el disco** que contiene el directorio de datos: el texto de los mensajes y los archivos multimedia se almacenan tal y como se recibieron.
4. **Limite el directorio de datos** a la cuenta de servicio. Los nuevos directorios se configuran con el modo 0700 en Unix; en Windows, establezca los permisos de la carpeta.
5. **Guarde la clave maestra del almacén en otro lugar** de los servidores: configure «`TGWITNESS_VAULT_KEY_FILE`» antes de crear el directorio de datos.
6. **Guarde la huella digital de la clave de firma y los puntos de control** en otro sistema, y añada un testigo en otro servidor.
7. **Nunca suba** claves `data/`, de sesión, `panel-token.txt` o de bóveda a GitHub ni a un chat.
8. **No registre** los encabezados «`Authorization`» ni los cuerpos de las solicitudes en un proxy inverso.

**¿Puedo cambiar el token del panel sin perder datos?**

Sí. El token solo abre el panel. Detenga TgWitness, elimine «`panel-token.txt`» del directorio de datos y vuelva a iniciarlo; el registro, las sesiones y las claves permanecen intactos. Con «`TGWITNESS_TOKEN`» configurado, se utiliza el valor de entorno en lugar del archivo.

**¿Por qué los mensajes no están cifrados en reposo?**

El recopilador debe leerlos para realizar búsquedas, comparar versiones y exportarlos. Cifrarlos con una clave en el mismo equipo aportaría poco frente a alguien que pueda acceder a dicho equipo. El cifrado del disco protege un disco inactivo o robado; los permisos estrictos protegen uno que está en funcionamiento.

## Informar de una vulnerabilidad

Utilice **«Seguridad → Informar de una vulnerabilidad»** en el repositorio de GitHub. Incluya la versión, el impacto y una reproducción sintética mínima. No envíe nunca credenciales, directorios de cuentas ni archivos de pruebas reales. Si no es posible realizar un informe privado, abra una incidencia solicitando un canal privado sin detalles sobre el exploit.
