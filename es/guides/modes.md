# Un diario. Cuatro modos de recopilación. Ocho niveles de verificación.

Canonical page: https://phishdestroy.github.io/TgWitness/es/guides/modes.html

Modos, escenarios y niveles de evidencia

TgWitness Registra lo que observa la cuenta conectada. Un tercero puede verificar la integridad del registro comparándolo con una clave de confianza independiente.

[Modos de recopilación](https://phishdestroy.github.io/TgWitness/es/guides/modes.html#scope)[Escenarios](https://phishdestroy.github.io/TgWitness/es/guides/modes.html#scenarios)[Niveles de evidencia](https://phishdestroy.github.io/TgWitness/es/guides/modes.html#levels)

Resumen de 3 a 5 minutos · ejemplos ficticios · implementación actual

1. **Telegram**

   Actualizaciones visibles en la cuenta
2. **Recopilador**

   Registros vinculados, cada uno de ellos firmado
3. **Verificador**

   Clave de confianza + límite conservado

`h₁ → h₂ → h₃ · Ed25519`Se comprueba la integridad. El origen de Telegram y la veracidad de un mensaje siguen siendo cuestiones distintas.

## Elija el ámbito de observación

Tres ámbitos y un ajuste preestablecido de investigación. Las exclusiones y los tipos de fuente habilitados siguen siendo aplicables.

Por defecto**Chats seleccionados**

Registros

Únicamente fuentes seleccionadas manualmente.

Nuevos chats

No se añade automáticamente.

Elija

Un conjunto conocido de canales o grupos. No se ha especificado ninguna capacidad fija para los chats.

**Qué no hace** No detecta otros chats ni completa el historial anterior.

Carpeta de cuentas**Carpeta de Telegram**

Registros

Incluye carpetas y categorías, excluyendo los chats excluidos y archivados cuando así se haya configurado.

Nuevos chats

Coincidencia de chats activos; cambios en las carpetas en el plazo de una hora.

Elija

Un analista ya mantiene una carpeta del caso. Confirme la recopilación en una cuenta específica.

**Qué no hace** No se aplican las condiciones variables de la carpeta muted/read de la carpeta.

Confirme el ámbito de aplicación**Cuenta completa**

Registros

Chats visibles para la cuenta, incluidas las conversaciones privadas y los bots, dentro de los tipos seleccionados.

Nuevos chats

Se añadirá cuando llegue la primera actualización.

Elija

Una cuenta dedicada a la observación, incluida una cuenta que participe en un caso.

**Qué no hace** No se une a los chats automáticamente ni elude el acceso a la fuente.

Configuración preestablecida para toda la cuenta**Modo de investigación**

Registros

Todos los tipos de fuentes, las acciones propias, los perfiles de las fuentes y los últimos 200 mensajes visibles de las fuentes recién descubiertas.

Nuevos chats

Cada nuevo chat o bot obtiene un perfil y una instantánea del historial.

Elija

Únase a un equipo o interactúe con un bot a través del panel. Revise y guarde la configuración preestablecida.

**Qué no hace** No realiza instantáneas de todos los chats existentes ni observa las llamadas de retorno activadas en otro cliente.

Estas tarjetas constituyen una comparación local, no controles del colector en tiempo real. No modifican ninguna cuenta.

**Qué no hace** Ningún modo lee chats secretos, registra mientras el proceso está detenido, se une a fuentes por su cuenta ni recupera el historial anterior más allá de lo solicitado snapshot/export.

[Lea los detalles](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/)

## Captura con GitHub Actions (versión preliminar)

Un nuevo inicio de sesión en Telegram, un chat, un archivo cifrado y procedencia de GitHub.

[Abrir el asistente de captura](https://phishdestroy.github.io/TgWitness/es/docs/capture/)

## Lo que se registra

Solo se incluyen en el registro las observaciones entregadas o solicitadas explícitamente. La atribución desconocida permanece desconocida.

 Captura de conmutadores · ilustración localNuevos mensajesModificacionesEliminacionesReaccionesAfiliación

El panel aplica estos modificadores por espacio de trabajo. Desactivar uno conserva los registros existentes; volver a activarlo no reconstruye los eventos perdidos.

**Matriz de eventos: material guardado y incógnitas pendientes**

| Categoría | Guardado | Sigue sin conocerse |
| --- | --- | --- |
| Mensaje | Texto, identificadores, metadatos del remitente, contexto de la respuesta y sobre de actualización original. | No existe una firma de Telegram verificable por terceros. |
| Editar | Todas las versiones observadas, sin sobrescribir las anteriores. | Es posible que se pasen por alto las modificaciones intermedias; el remitente no es necesariamente el editor. |
| Eliminación | Aviso más el texto guardado anteriormente, si está disponible. | No se facilitan el eliminador ni la hora exacta de la acción. |
| Eliminación sin ámbito | Aviso a nivel de cuenta; el par desconocido sigue siendo explícito. | No se deben adivinar los chats. La correlación utiliza, siempre que sea posible, los identificadores guardados previamente en el ámbito de la cuenta. |
| Reacción | Contadores entregados e identidades recientes visibles. | No todos los reactores son visibles; para obtener una lista completa de los disponibles se necesitan consultas independientes. |
| Afiliación | Mensajes de servicio entregados y actualizaciones de los participantes. | El rol y el tipo de chat limitan la visibilidad; el silencio no implica ausencia. |
| Archivo adjunto | Descriptor de la versión original, bytes guardados, SHA-256 y resultados de los intentos. | Es posible que un archivo desaparecido no esté disponible; una versión más reciente no lo sustituye. |
| Instantánea del historial | Mensajes visibles actualmente, marcados como observaciones del historial. | Las ediciones anteriores y el contenido desaparecido no se reconstruyen. |
| Acciones propias | Saliente messages/edits y los metadatos correspondientes del teclado de respuesta button_press . | Las llamadas de retorno activadas en otro cliente de Telegram no son visibles. |
| Botones del bot | Los metadatos de callback, URL, aplicación web y solicitud se conservan junto con el mensaje. | Las URL y phone/location las solicitudes son texto; no se abren ni se ejecutan automáticamente. |

### Límites predeterminados para los archivos adjuntos

Fotografías

20 MiB

Vídeo

100 MiB

Archivos

50 MiB

Animaciones

20 MiB

Notas en vídeo

50 MiB

Voz

20 MiB

Audio

50 MiB

Pegatinas

5 MiB

**Qué no hace** Un conmutador no suprime los metadatos incrustados ni desactiva los registros operativos. La captura no identifica a ningún actor que Telegram no haya facilitado.

[Lea los detalles](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/)

## Utilice la autorización de la que dispone

Cada cuenta dispone de su propio espacio de trabajo, diario, clave de firma, ruta y cola.

### Teléfono + código

Introduzca 2FA cuando esté habilitado.

### QR código

Realice el escaneo desde un dispositivo autorizado; 2FA puede que siga siendo necesario.

### Telethon .session

Importe el archivo de sesión de la cuenta.

### Pyrogram .session

Importe el Pyrogram formato de sesión compatible.

### TData ZIP

Se admite una sola cuenta de Desktop; código de acceso local, si se ha configurado.

### StringSession texto

Pegue un Telethon StringSession.

### .session + .json

Seleccione la sesión y los metadatos asociados correspondientes.

### Clave de autenticación HEX + DC ID

Importe la autorización de la cuenta junto con su identificador de centro de datos.

**API par**

Su propio API par es opcional. Si no dispone de uno, TgWitness se utiliza un conjunto de pares públicos, incluidos los del cliente oficial de Telegram Desktop.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy es experimental; las listas públicas integradas MTProxy . Una ruta de proxy fallida no recurre a una conexión directa.

Dos espacios de trabajo en un mismo equipo no constituyen dos testigos independientes.

**Qué no hace** La importación no elude la autorización de Telegram, 2FA ni los formatos de sesión no compatibles. Las cuentas siguen compartiendo el proceso de la aplicación.

[Formatos de cuenta](https://phishdestroy.github.io/TgWitness/es/docs/reference/accounts/)

## Actúe desde el panel

Envíe o responda, pulse un botón del bot actual, guarde una vista previa del enlace y, a continuación, únase explícitamente a un chat o inicie un bot con su parámetro de inicio.

`interaction.preview``interaction.requested``interaction.result`

Los acuses de recibo de vista previa, solicitud y resultado están firmados. Antes de pulsar un botón, el servidor vuelve a recuperar el mensaje y rechaza cualquier modificación introducida mediante el teclado. El texto y las URL de la llamada de retorno siguen formando parte del contexto registrado.

**Qué no hace** No se admiten aplicaciones web, pagos, phone/location compartir ni consultas en línea. Mostrar una URL no implica abrirla.

[Lea los detalles](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/)

## Recuperación y continuidad

Las lagunas se muestran, no se ocultan.

### Reanude la posición guardada

Tras el reinicio, se solicita a Telegram las actualizaciones perdidas. La retención finita y las diferencias caducadas pueden dejar lagunas.

### Vuelva a comprobar los mensajes visibles

Valores predeterminados: fuentes prioritarias cada 15 minutos; el resto, cada 6 horas. Los resultados incluyen message.recovered y message.missing_on_recheck.

### Leer coverage.json

Los periodos de observación, las lagunas con sus motivos y los ID no observados acompañan a la exportación firmada. Un registro que no aparece tras una nueva comprobación no constituye un aviso de eliminación.

**Qué no hace** Una instantánea posterior del historial no borra una interrupción del servicio ni recupera todas las versiones desaparecidas. El cursor guardado no constituye un acuse de recibo sin pérdidas de la aceptación del diario.

[Lea los detalles](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/)

## Siete niveles. Diferentes preguntas.

Cada mecanismo responde a una pregunta delimitada. Configure los servicios externos por separado y mantenga sus anclajes de confianza fuera del recopilador.

1. ### Registro

   SHA-256 cadena + Ed25519 por evento; el primero previous_hash son 64 ceros.

   **Comprobaciones de terceros** Ordenación y firmas bajo la clave del colector fijada.

   **Qué no hace** No demuestra el origen ni la integridad de Telegram.

   **Comando de verificación**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Contenedor

   manifest.json enumera los hash de los archivos; manifest.sig lo firma. media.saved vincula los bytes de los archivos adjuntos a un evento.

   **Comprobaciones de terceros** Los archivos proporcionados coinciden con el manifiesto firmado y los recibos multimedia.

   **Qué no hace** No firma una CSV, HTML o de una captura de pantalla.

   **Comando de verificación**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Límite conservado

   Punto de control al inicio, cada 5 minutos por defecto, y parada ordenada. Guarde una copia en otro lugar.

   **Comprobaciones de terceros** La exportación posterior concuerda con una longitud y un encabezado conservados anteriormente; se puede detectar una reversión.

   **Qué no hace** No detecta la sustitución tanto del diario como de todos los puntos de control conservados.

   **Comando de verificación**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### Hora externa

   El modo de evidencia envía un punto de control SHA-256 a RFC 3161 autoridades (FreeTSA, DigiCert) y OpenTimestamps a los calendarios.

   **Comprobaciones de terceros** Una respuesta TSA verificada fecha esos bytes; una OpenTimestamps prueba los vincula a Bitcoin.

   **Qué no hace** No considera una solicitud preparada ni un acuse de recibo pendiente del calendario como una marca de tiempo confirmada.

   **Comando de verificación**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Testigo independiente

   Separar el host, el punto final de solo lectura con ámbito limitado, el desafío nuevo y su propio key/journal y TGW1 publicaciones del canal.

   **Comprobaciones de terceros** Cabezas aceptadas anteriormente; estados «ok», key_changed, «rollback», «fork», «invalid» y no_response.

   **Qué no hace** No convierte dos espacios de trabajo en un mismo host colector en testigos independientes.

   **Comando de verificación**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Réplica externa

   S3Copia compatible con [...], cifrada con AES-256-GCM; Object Lock cuando el depósito lo admita.

   **Comprobaciones de terceros** La función «Restore» solo publica los archivos una vez que se haya completado con éxito la verificación del diario, del punto de control y de los medios conservados.

   **Qué no hace** No se restaura sin la clave exportada ni se da por hecho que se conserva sin comprobar la respuesta de almacenamiento.

   **Comando de verificación**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Ejecutar la procedencia

   Recibo de ejecución firmado: hash de código fuente, versiones de dependencias y contexto del proceso. Autodeclarado.

   **Comprobaciones de terceros** Lo que el recopilador de firmas informó sobre su propia ejecución.

   **Qué no hace** No proporciona una certificación independiente del proceso ni excluye la posibilidad de que se haya producido una vulneración antes del registro.

   **Comando de verificación**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### Lo que ningún nivel demuestra

Entrega de cada actualización de Telegram; la veracidad del texto; que el identificador del remitente identifique a una persona real; la ausencia de compromiso del recopilador antes del registro; la admisibilidad ante los tribunales.

[Testigo independiente](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/)

Experimento SHA-256 experimento

### Intente modificar el registro 2

El siguiente registro conserva el enlace guardado anteriormente. Al modificar el texto, cambia el hash calculado del registro 2.

Texto del registro 2

Registro 1`h1`Comienza con 64 ceros

Registro 2`h2`Incluye los archivos guardados h1

Registro 3`h3`Incluye los archivos guardados h2

Ejemplo estático: h2 incluye «Quedamos a las 11:00». Si se modifica ese texto, se modifica h2; el registro 3 sigue haciendo referencia al guardado h2.

**Revise los resúmenes completos**

Hash del registro 2 guardado

`SHA-256(e₂)`

Hash del registro 2 recalculado

`SHA-256(e₂)`

Este ejemplo calcula hash, no firmas. El verificador real comprueba cada firma y cada enlace con respecto a la clave de confianza.

 [Lea los detalles](https://phishdestroy.github.io/TgWitness/es/docs/reference/how-it-works/)

## Elija una ruta a través de las pruebas

Situaciones ficticias. Comience la recopilación antes del suceso relevante; conserve los límites y las lagunas junto con el contenido.

### Un canal modifica los datos de pago

Modo → eventos

Chats seleccionados → mensajes, modificaciones, eliminaciones.

Salida

Versiones de las publicaciones y archivos adjuntos observados mediante hash.

Verificación

Firmado ZIP + punto de control conservado + respuesta TSA verificada.

**Qué no hace** No recupera un original que nunca se haya capturado.

### Los mensajes desaparecen tras un incidente

Modo → eventos

Carpeta o cuenta completa → todas las categorías de eventos.

Salida

Originales guardados, avisos de eliminación y cobertura con lagunas.

Verificación

Firmado ZIP + diario de testigos independiente.

**Qué no hace** No identifica al autor de la eliminación a partir de una notificación que no indica quién la ha realizado.

### Investigue un bot de tienda

Modo → eventos

Configuración predeterminada de investigación → botones, vistas previas de enlaces e inicio explícito del bot.

Salida

Recibos de interacción firmados, devoluciones de llamada y perfiles guardados.

Verificación

Firmado ZIP; verifique cualquier expediente con respecto al ZIP.

**Qué no hace** No abre una aplicación web de bot, no realiza pagos ni registra las respuestas de otro cliente.

### Un participante cambia de nombre de un chat a otro

Modo → eventos

Cualquier ámbito → metadatos sender/profile metadatos observados.

Salida

Historial de nombres/nombres de usuario por ID numérico, enlaces «también en» y pistas extraídas.

Verificación

Expediente JSON comparado con el firmado ZIP.

**Qué no hace** No convierte una cartera, una cadena similar a la de un teléfono o un nombre de usuario en una identidad verificada.

### Observación a largo plazo con una copia externa

Modo → eventos

Cualquier ámbito → Modo de evidencia y una S3 réplica con compatibilidad Object Lock.

Salida

Copia cifrada, puntos de control conservados y respuestas con marca de tiempo.

Verificación

Restaure con la clave exportada y, a continuación, verifique sin el servidor original.

**Qué no hace** No sustituye a un testigo independiente ni a una clave de descifrado conservada por separado.

[Lea los detalles](https://phishdestroy.github.io/TgWitness/es/docs/reference/investigation/)

## Entregue un paquete que se pueda verificar

Proporcione el original firmado, una huella digital de la clave conservada de forma independiente, el punto de control pertinente y el resultado de la verificación.

- Firmado ZIP
- JSONL
- CSV
- HTML
- Punto de control
- Confirmación de entrega
- Exportación de chats: chat.json / chat.html
- Expediente JSON
- Protegido con contraseña AES-256 ZIP
- Exportaciones separadas para varias cuentas
- CLI de transmisión: 5 GiB límite por defecto

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Obtenga el verificador a partir de una copia de confianza, no del archivo que se está comprobando.

**Qué no hace** Autónomo CSV y HTML no son contenedores firmados. Una contraseña protege la confidencialidad de la transferencia, no su autenticidad. Las exportaciones múltiples no fusionan los registros de las cuentas.

[Lea los detalles](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/)

## Compare el artefacto entregado

Artefactos básicos sin sistemas añadidos de firma, marca de tiempo o testigos. Los scripts y los registradores varían según la implementación; «parcial» significa limitado al material capturado o visible.

| Enfoque | Modificaciones / eliminaciones | Registrar la firma | Hora externa | Testigo independiente | Cobertura / lagunas | Verificación sin autor |
| --- | --- | --- | --- | --- | --- | --- |
| Exportación de Telegram Desktop | Parcial | No | No | No | No | No |
| Telethon script de instantánea | Parcial | No | No | No | No | No |
| Registrador de eliminaciones: registro de texto | Parcial | No | No | No | No | No |
| Capturas de pantalla / captura web | Parcial | No | No | No | No | No |
| TgWitness con extras configurados | Parcial | Sí | Sí | Sí | Parcial | Sí |

**Qué no hace** La tabla no evalúa todos los scripts ni todos los productos de registro. Las comprobaciones opcionales de tiempo y de testigos requieren sus propios servicios y puntos de referencia de confianza; ninguno de ellos establece la veracidad de la fuente.

[Lea los detalles](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/)

## Mantenga los límites dentro de las pruebas

La verificación resulta útil cuando su ámbito de aplicación se mantiene explícito.

- Los chats secretos no están disponibles.
- No se registra nada mientras el proceso está detenido; la recuperación es limitada.
- Un registro verificado no es prueba de que su contenido sea cierto.
- Un operador que disponga de la clave puede firmar cualquier contenido. Los testigos independientes y las marcas de tiempo impiden la sustitución posterior, pero no la captura inicial fraudulenta.
- Utilice una cuenta específica, no su cuenta principal.
- Telegram puede restringir cuentas debido al volumen de solicitudes.

**Qué no hace** Ningún modo ni nivel de evidencia establece la admisibilidad legal, la entrega completa de Telegram ni la identidad en el mundo real.

[Guía de configuración](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=es)[Cuenta dedicada](https://phishdestroy.github.io/TgWitness/es/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/es/docs/reference/investigation/)
