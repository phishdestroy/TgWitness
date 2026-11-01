# Pruebas y confianza

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence-trust/

Qué pueden demostrar las exportaciones, los vídeos, los archivos web y los registros firmados, y cómo el dispositivo de recopilación afecta a su fiabilidad.

Una exportación, una captura de pantalla o una grabación pueden constituir pruebas útiles. Su fiabilidad depende de cómo se hayan recopilado, conservado y corroborado. **Un hash o una firma válidos verifican el material guardado; no establecen de forma independiente que el dispositivo de recopilación haya recibido contenido original veraz.** Esta distinción también se aplica a TgWitness.

Esta guía separa la verificación técnica de la evaluación jurídica. La documentación del producto y las disposiciones legales que figuran a continuación se revisaron el 1 de noviembre de 2026; la comparación de Hunchly describe su documentación publicada, no una nueva auditoría del producto.

## Cuando la confianza entra en juego en la captura

Diagrama de flujo · Cuenta y servicio de Telegram → Cliente, navegador y sistema operativo; Cliente, navegador y sistema operativo → Exportación, captura de vídeo o de página; Exportación, captura de vídeo o de página → Hashes y firmas del recopilador; Hashes y firmas del recopilador → Hash conservado por una parte independiente · Cuenta y servicio deTelegram · Cliente, navegador ysistema operativo · Exportación, capturade vídeo o de página · Hashes y firmas delrecopilador · Hash conservado poruna parteindependiente

**Diagrama en formato de texto**

1. Cuenta y servicio de Telegram → Cliente, navegador y sistema operativo
2. Cliente, navegador y sistema operativo → Exportación, captura de vídeo o de página
3. Exportación, captura de vídeo o de página → Hashes y firmas del recopilador
4. Hashes y firmas del recopilador → Hash conservado por una parte independiente

El modelo de amenaza aquí supone que un atacante u operador puede alterar el entorno de recopilación antes de que se guarden las pruebas. Se trata de un análisis condicional, no de una afirmación de que un dispositivo o producto concreto haya sido comprometido.

Un cliente oficial y una conexión cifrada ayudan a proteger el uso normal. No hacen que el sistema operativo, el navegador o la pantalla que los rodean sean, por sí mismos, fiables. Si el contenido se sustituye tras el descifrado pero antes de la captura, el exportador puede guardarlo con precisión y el firmante puede firmarlo correctamente. Ninguna de las dos operaciones requiere un algoritmo hash defectuoso ni una firma falsificada.

Un vídeo grabado en el mismo dispositivo puede registrar la misma presentación sustituida. Una cámara independiente puede confirmar lo que mostraba la pantalla, pero la pantalla por sí sola no autentifica lo que proporcionó Telegram. Del mismo modo, el HTML, el JSON, las capturas de pantalla y los registros del navegador coincidentes procedentes de un mismo entorno controlado pueden compartir el mismo fallo. Su coincidencia constituye un contexto útil; no supone automáticamente una corroboración independiente.

## Qué aporta cada tipo de prueba

| Material | Contribución útil | Pregunta pendiente |
| --- | --- | --- |
| Exportación de Telegram Desktop | Conversaciones legibles o legibles por máquina y archivos multimedia seleccionados | ¿Quién controlaba los archivos del cliente y de exportación, y qué estaba disponible o excluido? |
| Captura de pantalla o grabación de pantalla | Contexto visible, secuencia de acciones y presentación | ¿Refleja la presentación fielmente el texto original y lo que ocurrió fuera de la grabación? |
| Archivo web local, incluido MHTML | Contenido de la página y recursos asociados para su examen posterior | ¿Qué proporcionó el navegador al archivador y quién controlaba ese navegador? |
| Archivo firmado por el recopilador | Los cambios en los bytes firmados pueden detectarse en relación con una clave de confianza y una referencia conservada. | ¿Quién controlaba la clave de firma y los datos introducidos antes de la firma? |
| Punto de control conservado de forma independiente o marca de tiempo verificada | Un hash o punto de control conservado para compararlo con un envío posterior | ¿Qué bytes y límites se abarcan, y qué certifica realmente la parte independiente? |

Telegram documenta su exportación de Desktop como una copia HTML/JSON sin conexión y su API Takeout como una forma de recuperar datos seleccionados de la cuenta. Estas descripciones no proporcionan una firma de Telegram sobre el archivo exportado final para que el destinatario la verifique. Nuestra conclusión se limita a esos mecanismos de exportación documentados; no es una afirmación de que las pruebas de Telegram carezcan de valor legal.[Exportación de Telegram Desktop](https://telegram.org/blog/export-and-more),[API Takeout](https://core.telegram.org/api/takeout).

La misma distinción se aplica a las solicitudes en segundo plano, las entradas de caché y los registros de red. Pueden revelar inconsistencias y ayudar a corroborar una recopilación. Su complejidad por sí sola no determina quién los generó. Un archivo gestionado de forma independiente o un registro de servicio obtenido por separado introduce una fuente diferente con la que comparar, sujeta a sus propias limitaciones de recopilación y custodia.

## Hunchly ilustra el mismo límite

La documentación de Hunchly describe el hash SHA-256 de capturas MHTML, fotos y archivos adjuntos, con verificación independiente del hash. También explica por qué un archivo alterado acompañado de un hash recién calculado puede superar esa comparación, y señala las firmas y la corroboración de la fuente como comprobaciones adicionales.[Hunchly: hash de contenido, fotos y archivos adjuntos](https://support.maltego.com/support/solutions/articles/15000061289-content-photo-and-attachment-hashing).

Su *Guía de Pruebas* publicada, revisión 1.0 del 17 de octubre de 2018, describe las claves GPG y las firmas generadas localmente para las capturas MHTML. Identifica explícitamente el acceso a la clave privada local como una forma de volver a firmar el material modificado. Se trata de una limitación de confianza documentada, no de una prueba de un exploit actual no revelado. La guía también indica que Chrome realiza la captura MHTML. Describir Hunchly como una herramienta que se basa únicamente en la reputación del investigador omitiría estos controles técnicos.[Guía de pruebas de Hunchly, secciones 2-4](https://hunch.ly/resources/Hunchly%20Evidence%20Guide.pdf).

Que el material recopilado con un producto concreto haya sido admitido en un caso depende de la resolución pertinente y de las circunstancias. No hacemos aquí ninguna afirmación sobre la frecuencia con la que los tribunales aceptan Hunchly o TgWitness, ni sobre que ninguno de los dos productos cuente con una aprobación judicial general.

## Qué aporta TgWitness y hasta dónde llega su protección

TgWitness registra las observaciones en un diario firmado y enlazado, y proporciona exportaciones que el destinatario puede verificar. Los puntos de control conservados, las marcas de tiempo y un testigo independiente proporcionan a los revisores referencias más allá de los archivos actuales del recopilador. Ayudan a poner de manifiesto los cambios en los registros previamente confirmados. Los registros de cobertura y los resultados explícitos de la recopilación ayudan a explicar qué se ha capturado y qué no.[Formato y entrega de las pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/), [alcance de la recopilación](https://phishdestroy.github.io/TgWitness/es/docs/reference/collection/).

El momento en que se produzca una posible sustitución es importante:

1. **Tras la firma, sin acceso a la clave de firma:** modificar un registro firmado o un archivo vinculado al manifiesto provocará que falle la verificación con un verificador y una clave de confianza.
2. **Con la clave del recopilador, tras conservar un punto de control independiente:** un registro de sustitución puede tener nuevas firmas válidas, pero un prefijo modificado no supera la comparación con ese punto de control anterior. Un punto de control conservado únicamente en el mismo dispositivo controlado puede sustituirse junto con el registro. Los registros más allá del límite conservado requieren su propia cobertura.
3. **Antes de que se conserve de forma independiente un punto de control que abarque una observación:**se pueden firmar y anclar con éxito entradas falsas, incluidos los nuevos registros añadidos tras un punto de control anterior. El punto de control o la marca de tiempo resultantes siguen abarcando esos registros falsos; no establecen su veracidad.

Un testigo TgWitness recibe los puntos de control firmados por el recopilador; no lee de forma independiente la conversación subyacente de Telegram. Su clave y los registros conservados deben ser considerados fiables por separado. Cuando sea necesario que todo el diario enviado sea verificado, utilice el[procedimiento de traspaso que requiere el límite de exportación final](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/#require-a-witnessed-export-boundary). Una comprobación de integridad ordinaria puede seguir informando de una cola no verificada.

Una respuesta RFC 3161 verificada puede respaldar que existía un punto de control en el momento indicado por la autoridad. No establece cuándo se envió un mensaje de Telegram ni si su contenido era veraz. Una solicitud preparada o un archivo de respuesta incluido por sí solos son insuficientes. Al verificar una exportación con `tgwitness.verify`, la comprobación de las firmas TSA incluidas requiere una CA explícitamente de confianza a través de `--tsa-ca`. Los recibos de OpenTimestamps necesitan una verificación independiente `ots verify`, con actualizaciones de las pruebas cuando sea necesario. [Procedimiento de marca de tiempo](https://phishdestroy.github.io/TgWitness/es/docs/reference/timestamp/), [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html).

En [la captura de GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md), un «runner» alojado temporalmente recopila los mensajes. La certificación vincula el archivo a un flujo de trabajo aprobado. Este modo sigue confiando en GitHub, el software y las dependencias aprobadas, el asistente/navegador y el túnel. No se trata de hardware confidencial, una firma de Telegram ni una prueba de que nadie haya accedido al servidor. Un recibo de ejecución firmado localmente es también una medición autodeclarada, no una certificación de hardware.

## El peso jurídico depende de la base

Hay cuatro cuestiones que deben mantenerse diferenciadas: si el elemento es lo que se dice que es, si los bytes enviados coinciden con el registro conservado, si el contenido respalda los hechos alegados y si las normas aplicables permiten su uso. Una verificación criptográfica solo aborda una parte de esa base.

En los procedimientos federales de EE. UU., la Regla 901 establece formas de autenticar las pruebas, incluidos el testimonio de testigos bien informados y las pruebas sobre un proceso o sistema. Las Reglas 902(13) y 902(14) establecen vías de certificación para determinados registros y copias electrónicos, con requisitos procesales. Las notas del comité distinguen la autenticación de cuestiones como el testimonio de oídas, la pertinencia y la atribución. Una firma de software por sí sola no constituye la certificación de la persona cualificada descrita en dichas normas.[Regla Federal de Prueba 901](https://www.law.cornell.edu/rules/fre/rule_901),[Regla Federal de Prueba 902](https://www.law.cornell.edu/rules/fre/rule_902).

En los casos en que se aplique la Ley de Pruebas de Canadá, el artículo 31.1 aborda la autenticación de los documentos electrónicos. El artículo 31.2 vincula la regla de la mejor prueba a la integridad del sistema o a una presunción aplicable; el artículo 31.3 especifica las circunstancias para una presunción de integridad. Se trata de condiciones probatorias definidas, no de una presunción general de que cualquier investigador autorizado o producto comercial sea infalible. [Ley de Pruebas de Canadá, 31.1](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.1.html),[31.2](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.2.html),[31.3](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.3.html).

Estos ejemplos no determinan la admisibilidad en otra jurisdicción ni en un caso concreto. Las comprobaciones técnicas deben aplicarse de forma coherente al material que respalde o rebata una alegación. Esta guía no afirma en modo alguno que las pruebas de la acusación sean, en general, más fáciles de admitir que las de la defensa.

## Prepara un registro que otra persona pueda evaluar

- Describe la cuenta, el dispositivo de recopilación, el operador, la versión del software, los derechos de acceso, el ámbito seleccionado y el periodo de recopilación. Registra las interrupciones y posibles vulnerabilidades, en lugar de considerar una comprobación de firma satisfactoria como una prueba de que el dispositivo está limpio.
- Conserva los paquetes originales y registra las transferencias, los hash y la fuente de la hora. Conserva la huella digital de la clave y los puntos de control a través de un canal de confianza independiente. Verifica la cobertura real de los testigos o las marcas de tiempo antes de describirla en un informe.
- Busque una corroboración independiente adecuada a la afirmación: los registros de otro participante, una captura independiente o registros de servicio obtenidos legalmente. Explique su independencia y sus limitaciones; la coincidencia entre copias no es suficiente por sí sola.
- Conserve el contexto relevante. Identifique los archivos omitidos, el historial no disponible y las censuras. Prepare una [divulgación minimizada por separado](https://github.com/phishdestroy/TgWitness/blob/main/docs/ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient)cuando sea necesario, y describa sus transformaciones sin presentarla como el original completo.
- Proporcione al destinatario las instrucciones de verificación y el material necesario para dichas comprobaciones. Mantenga diferenciadas las observaciones, los hallazgos técnicos y las conclusiones del analista.

Para un traspaso concreto, indica el hash del archivo, la clave de confianza, el resultado de la verificación y el límite exacto cubierto externamente. Describe por separado la autenticidad de la fuente, la atribución de la cuenta, la integridad y las conclusiones legales. Esto proporciona al siguiente revisor afirmaciones específicas que examinar.
