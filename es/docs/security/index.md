# Mantenga la seguridad

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/security/

Qué sale de su máquina, qué abre cada secreto y qué cubren las protecciones frente a lo que le toca a usted.

**127.0.0.1**Dirección del panel por defecto

**256 bits**token de panel aleatorio

**0**CDN, herramientas de análisis o fuentes remotas

**Ed25519**Firma en cada registro

## Donde se encuentra todo

El recolector, el panel y cada registro se quedan en su máquina. Por defecto solo se contacta con Telegram; todo lo demás es un interruptor aparte.

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
| **Token de panel** | `panel-token.txt` en el directorio de datos; el navegador lo guarda por pestaña | Todo en todos los espacios | Detenga TgWitness, borre `panel-token.txt` y arranque de nuevo: obtiene uno nuevo |
| **Sesión de Telegram** | Almacén cifrado (`credentials.enc`) | La propia cuenta de Telegram | Finalice la sesión en Telegram en *Ajustes → Dispositivos* |
| **Clave de firma** | Almacén cifrado (`signing.enc`) | Firmar registros con su huella | Los puntos de control guardados en otro sitio, un testigo y las marcas de tiempo siguen mostrando lo que existía antes |
| **Clave de la bóveda** | `vault.key` junto a los datos o una clave maestra externa | La bóveda | Dé por filtradas también la sesión y la clave de firma |
| **Token de Witness** | En el servidor de TgWitness | Solo lectura: puntos de control y estado | Bórrelo en la página del testigo y cree uno nuevo |
| **Texto clave para uso externo** | Vault; descárguelo una sola vez para poder recuperarlo | La copia externa | Quien tenga además el bucket puede descifrarla: considere la copia expuesta |

## Qué cubren las medidas de protección

### Cubierto

- Un registro cambiado, eliminado o reordenado: se rompe la cadena de hashes o una firma.
- Un diario recortado o reconstruido después de guardar un punto de control en otro sitio: el punto de control deja de coincidir.
- Adivinar el token: 256 bits aleatorios, comparación en tiempo constante; 15 fallos por minuto y la dirección queda bloqueada.
- Contenido hostil en chats: el texto sigue siendo texto, nunca HTML; los adjuntos se descargan como archivos; el panel no carga nada de otros sitios.
- Un directorio de datos robado con clave de bóveda externa: sesiones y claves siguen cifradas.

### A su criterio

- El token principal lo puede todo. Dé a otros acceso limitado y guárdese el principal.
- Quien sea administrador de la máquina puede leerlo todo y volver a firmar el diario. Guarde la huella y los puntos de control en otro sitio.
- TgWitness no cifra mensajes ni multimedia. Cifre el disco y restrinja los permisos.
- HTTP plano fuera de localhost filtra el token. Use HTTPS o un túnel SSH.
- Las firmas no le dicen qué se perdió. Compruebe la cobertura y pruebe la entrega en sus propias cuentas y fuentes.

[Comparta el acceso a un caso](https://phishdestroy.github.io/TgWitness/es/docs/access/) con permisos, caducidad y límites de sesión.

## Reforzar una instalación

0 de 8 completado

1. **Use una cuenta de Telegram dedicada**, nunca la principal.
2. **Mantenga el panel en 127.0.0.1.** Acceso remoto solo por HTTPS (Caddy incluido) o túnel SSH.
3. **Cifre el disco** con el directorio de datos: mensajes y multimedia se guardan tal cual.
4. **Restrinja el directorio de datos** a la cuenta de servicio (0700 en Unix, permisos de carpeta en Windows).
5. **Guarde la clave de la bóveda aparte** en servidores: defina `TGWITNESS_VAULT_KEY_FILE` antes del primer arranque.
6. **Guarde la huella y los puntos de control** en otro sistema y ejecute un testigo en otro host.
7. **Nunca suba** claves `data/`, de sesión, `panel-token.txt` o de bóveda a GitHub ni a un chat.
8. **No registre** los encabezados «`Authorization`» ni los cuerpos de las solicitudes en un proxy inverso.

**¿Puedo cambiar el token del panel sin perder datos?**

Sí, solo abre el panel. Detenga TgWitness, borre `panel-token.txt` y arranque de nuevo. Diario, sesiones y claves se mantienen. Si `TGWITNESS_TOKEN` está definido, ese valor manda sobre el archivo.

**¿Por qué los mensajes no están cifrados en reposo?**

El recolector tiene que leerlos para buscar, comparar y exportar. Una clave en la misma máquina no detendría a quien ya puede leer esa máquina. El cifrado de disco cubre un disco robado; los permisos, uno en marcha.

## Informar de una vulnerabilidad

**Security → Report a vulnerability** en GitHub. Versión, impacto y una reproducción mínima con datos ficticios. Nunca envíe credenciales, carpetas de cuentas ni evidencia real. Si el informe privado está desactivado, abra un issue pidiendo un canal privado, sin detalles del exploit.
