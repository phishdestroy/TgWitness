# Exportación de cuentas

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/account-export/

Exporta lo que una cuenta puede leer en este momento: ámbito, tareas reanudables, un archivo firmado y copias compartidas minimizadas.

Una exportación de cuenta reserva esa cuenta en exclusiva. Pausa explícitamente la supervisión u otra adquisición antes de iniciar o reanudar; la aplicación nunca la detiene automáticamente.

Como administrador de la instalación, selecciona **«Empezar aquí» → «Exportar mi cuenta**» o **«Exportaciones» → «Cuenta de Telegram» → «Configurar la exportación de la cuenta**». Inicia sesión si es necesario, revisa el alcance e inicia explícitamente la exportación. No es necesaria una observación continua. **«Observaciones guardadas»** es una exportación independiente del diario existente; su ZIP incluye todas las fuentes, independientemente de los filtros del diario. Cada espacio de trabajo tiene sus propias tareas, identidad de firma y almacenamiento. El acceso al panel concedido, incluida una autorización de exportación ordinaria sin restricciones, no puede abrir estas rutas que abarcan toda la cuenta.

Los filtros de remitente y de texto se despliegan en **«Filtrar por remitente» o «Texto del mensaje**». La sección **«Datos de la cuenta y método de conexión»** contiene categorías de cuenta opcionales y la opción «Takeout» o «sesión normal»; su resumen muestra las opciones activas incluso cuando está cerrada. Al cerrar estas secciones, se conservan sus ajustes. Los borradores de exportación e informes permanecen en la sesión actual del panel al cambiar de vista; no se guardan al recargar el navegador. Se puede acceder a los trabajos existentes desde cualquiera de las dos opciones de exportación.

Este flujo de trabajo exporta los datos a los que tiene acceso actualmente la cuenta conectada. Por defecto, utiliza [Telegram Takeout](https://core.telegram.org/api/takeout); no se trata de una copia de seguridad de datos de Telegram no disponibles o eliminados. No se recuperan los chats secretos, el historial inaccesible ni las ediciones anteriores. Telegram puede imponer un periodo de espera antes de que comience Takeout. El panel muestra ese tiempo de espera; no cambia de método de transferencia de forma silenciosa. La opción explícita de la API estándar tiene una cobertura diferente y registra categorías no compatibles.

## Elige qué se recopila

| Configuración | Significado |
| --- | --- |
| Objetivo | Explica por qué es necesaria esta adquisición. No incluyas aquí nombres innecesarios ni detalles confidenciales del caso. |
| Idioma del informe | Elige el idioma de las etiquetas del informe legible. El texto original del mensaje permanece sin cambios; las etiquetas de las plantillas no traducidas se muestran en inglés. El idioma se fija mediante las opciones de la tarea firmada. |
| Tipos de chat / ID de chat | Todos los tipos seleccionados, o solo los chats de la lista; «Mensajes guardados» corresponde a los chats privados. Los chats archivados se pueden seleccionar por separado. |
| Fechas | UTC. Se incluyen tanto la fecha de inicio como la de finalización del panel en el calendario. La API utiliza `from_utc` y exclusivos `to_utc`; el panel envía el inicio del día posterior a la fecha «Hasta». Un límite vacío deja ese lado sin restricciones. |
| Identificadores de remitente | Solo los mensajes de los remitentes que figuran en la lista; una lista vacía incluye a todos los remitentes. |
| El texto contiene | Las frases literales, sin distinción entre mayúsculas y minúsculas, se combinan con «OR». Las condiciones de remitente, fecha y mensaje propio se combinan con «AND». |
| Mensajes propios | Conserva únicamente los mensajes enviados. |
| Tipos de medios | Selecciona categorías de archivos adjuntos o borra todo para evitar la descarga de archivos de mensajes. |
| Límites de archivos y de contenido multimedia total | MiB por archivo y GiB de contenido multimedia descargado en total. El texto, los recibos, los informes legibles y los elementos de sobrecarga ZIP requieren espacio adicional en disco. |
| Categorías de cuentas | El perfil, los contactos, las fotos de perfil, las historias, los metadatos de sesión y otros datos de Takeout cuentan con controles independientes. |

El ajuste preestablecido **«Minimize»** desactiva los archivos y los metadatos de las cuentas. Los filtros de remitente y contenido se aplican antes de que se conserven las páginas de mensajes y se descarguen los archivos multimedia. Telegram sigue transmitiendo páginas del historial de la API que contienen los mensajes necesarios para evaluar dichos filtros: el filtrado no garantiza que los mensajes no seleccionados nunca entren en la memoria del proceso. Cualquier otra observación en curso en el espacio de trabajo tiene su propio ámbito de aplicación y configuración de retención.

El historial de fotos de perfil y las historias no están seleccionados por defecto. Desactiva también el perfil y los contactos cuando el caso solo requiera mensajes. Si los archivos adjuntos o los metadatos no son necesarios, excluirlos durante la adquisición evita que se conserve otra copia privada en esta exportación.

## Resumen, cobertura y verificación

Cada tarea congela sus opciones y la identidad de la cuenta. El inventario y las páginas capturadas se firman; los recibos de las páginas registran hash, cursores, horas, resultados de los archivos adjuntos y su recibo anterior. Solo las páginas confirmadas hacen avanzar el progreso. Al reiniciar o reanudar, se comprueban esos registros antes de continuar. Se rechaza cualquier cuenta modificada, página firmada modificada o cadena de recibos incoherente. Las opciones no se pueden editar a mitad de una adquisición: inicia otra tarea para otro ámbito.

La opción «Pausa» detiene la operación de la cuenta en ejecución. Al reiniciar la aplicación, el trabajo pendiente queda disponible para reanudarse de forma explícita. Una sesión de Takeout caducada requiere una reanudación explícita; cambiar los rangos de fragmentación de Telegram puede requerir una nueva adquisición. La opción «Reanudar» conserva las observaciones anteriores, por lo que una exportación de larga duración no es una instantánea atómica única. Otras operaciones de cambio de cuenta y exportaciones conflictivas se bloquean durante la adquisición. Espera a que finalice el empaquetado antes de eliminar un espacio de trabajo.

La función «Reanudar» verifica el contenido ya capturado antes de continuar. Los archivos de gran tamaño en un almacenamiento lento pueden superar el tiempo de espera configurado **Parámetros → Tiempo de espera de las acciones del panel** (120 segundos por defecto). Aumenta ese valor antes de volver a intentarlo; la cancelación o la interrupción del almacenamiento dejan una tarea en pausa, y los fallos en las comprobaciones de integridad dejan una tarea fallida con una explicación. La verificación debe finalizar o detenerse de forma segura antes de que se puedan cerrar sus archivos. Las comprobaciones sintéticas no han validado ninguna afirmación sobre el rendimiento con cuentas de gran tamaño.

El panel distingue entre un ámbito seleccionado completado y un archivo parcial, y registra las omisiones y las lecturas fallidas. Los archivos excluidos deliberadamente son distintos de los archivos fallidos o no disponibles. Comprueba la cobertura incluso cuando la verificación de integridad se realiza con éxito. Ningún lector local puede demostrar que Telegram haya devuelto todos los mensajes que han existido.

Los archivos ZIP finalizados siguen estando disponibles para descargas repetidas y descargas por rango HTTP. Un archivo de cuenta contiene `manifest.json`, `manifest.sig`, firmados `job.json`, `inventory.json`, `receipts/`, fidedignos `data/*.jsonl`, seleccionado `media/`, HTML legible y un verificador. Fija la huella digital del recopilador a través de un canal independiente y, a continuación, verifica utilizando una instalación de confianza:

```
python -m tgwitness.verify account-export.zip --fingerprint TRUSTED_SHA256
```

Para los archivos cuyo contenido expandido supere los 4 GiB, establece un límite explícito adecuado `--max-gib`. El panel verifica sus archivos locales autenticados y completos utilizando su tamaño expandido declarado y el resumen publicado ZIP; la CLI externa mantiene su límite de tamaño independiente. Verifícalo antes de abrir el HTML legible. El verificador integrado en el archivo es práctico, pero un verificador obtenido de forma independiente evita tener que confiar en el código ejecutable que se entrega junto con la evidencia.

La firma Ed25519 y los hashSHA-256 detectan cambios después de que el recopilador haya guardado los bytes correspondientes. No **no** demuestran que Telegram haya firmado esos mensajes, que el operador del recopilador haya actuado con honestidad, que el historial de la cuenta esté completo ni que un tribunal vaya a aceptar el material. Las horas de captura se basan en el reloj del recopilador. Las marcas de tiempo independientes y la procedencia independiente de la adquisición deben evaluarse por separado.

## Prepara una comunicación para un abogado u otro destinatario

Tras descargar una exportación completa, conserva la imagen original ZIP y abre `index.html` desde una copia extraída. El informe explica su alcance, la cobertura disponible y sus límites. Sus referencias de registro combinan la referencia del archivo, la ruta del documento y el número de registro, de modo que el destinatario pueda localizar la misma entrada en el HTML o en la copia impresa. Para ver un ejemplo práctico, [Abrir el informe ficticio](https://phishdestroy.github.io/TgWitness/demo/report/).

Una vez finalizada la exportación de la cuenta, selecciona **«Preparar una copia para compartir**». Esto genera un derivado firmado independiente. La fuente ZIP permanece inalterada y privada; no la envíes junto con un derivado minimizado a menos que el destinatario esté autorizado a recibir su contenido completo. Selecciona el idioma del informe por separado. Cambiar el idioma o cualquier configuración de selección requiere otra vista previa antes de la creación.

1. Introduce el motivo de la divulgación y selecciona las fechas, los ID de los remitentes y los criterios de texto literal.
2. Elige si deseas conservar las identidades, revelar solo a los participantes incluidos en la lista o seudonimizar a todos. En cualquier modo de seudonimización, también se sustituyen los ID o títulos de los chats y los ID de los mensajes. Los seudónimos son fijos dentro de una misma divulgación y cambian entre divulgaciones preparadas de forma independiente.
3. Conserva el texto del mensaje, omítelo por completo o añade nombres o frases literales para enmascarar. En los modos privados, la herramienta también enmascara los nombres ocultos conocidos de los remitentes y los nombres de usuario alternativos, los identificadores de remitente completos, los nombres de los chats directos, los enlaces, las direcciones de correo electrónico y las cadenas similares a números de teléfono. La coincidencia de nombres conocidos gestiona la conversión de mayúsculas y minúsculas de Unicode, incluyendo `Straße`/`STRASSE`. Los títulos genéricos de grupos o canales no se eliminan automáticamente del texto del mensaje. Si se supera el límite de ocultación de identidades conocidas, restringe la exportación de origen u omite texto; la herramienta se niega a omitir silenciosamente los nombres posteriores. Se trata de reglas de «mejor esfuerzo», no de una anonimización general.
4. No incluyas archivos a menos que el destinatario los necesite. Los originales incluidos conservan sus píxeles, audio, texto y metadatos. La herramienta **no** los anonimiza.
5. Previsualiza los recuentos, las advertencias y los mensajes transformados de muestra y, a continuación, confirma explícitamente la creación. Las muestras están limitadas a 12 mensajes y 2.000 caracteres de texto cada una. Se trata de una muestra, no de una revisión completa del resultado. Para cambiar la configuración es necesario realizar otra previsualización. Una previsualización caduca a los 15 minutos y está vinculada a esa sesión de administrador y al ZIP original exacto; no se puede reutilizar tras su creación. Una nueva previsualización invalida la anterior para el mismo trabajo y sesión.
6. Examina el resultado completo `index.html` y `messages.jsonl` localmente antes de entregarlo. Si revela información innecesaria, crea una nueva divulgación con exclusiones más estrictas. No edites in situ la imagen firmada ZIP.

El formato minimizado omite los perfiles estructurados de las cuentas, los contactos, los avatares, las sesiones, las historias, los objetos Telegram sin procesar, los encabezados de reenvío, las citas de respuestas, las fichas de contacto y los metadatos de ubicación. Excluye los archivos JSONL originales, la configuración de filtros privados, la clave de seudónimo y el mapa de identidades. El texto seleccionado, las identidades conservadas explícitamente y los archivos incluidos pueden seguir conteniendo los mismos nombres, identificadores o frases utilizados en dichos filtros; requieren una revisión por separado. La política privada y la clave de seudónimo se conservan cifradas en la caja fuerte local del trabajo; al eliminar el trabajo se borran los registros de divulgación privada asociados. Los registros de la política pública recogen el recuento de filtros en lugar de los valores de los mismos. La finalidad indicada es pública en el manifiesto y en el HTML: los criterios privados explícitos y, en los modos seudonimizados, las identidades ocultas conocidas también se enmascaran allí, incluso cuando se omite el texto del mensaje. Mantén la finalidad libre de datos personales innecesarios; el contexto de identificación desconocido puede permanecer.

Su manifiesto vincula los archivos derivados, la política pública y el hash de la imagen original ZIP. La verificación permite comprobar la integridad y, si la fuente se proporciona localmente, la correspondencia del enlace de origen:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

El enlace a la fuente no demuestra por sí solo que la transformación haya seleccionado todos los elementos necesarios o haya eliminado todos los detalles identificativos. El texto sin formato original no se incluye como prueba. Se necesita una nueva revisión para llegar a esa conclusión.

## Protección de datos y vista previa de Capture alojada

Estos controles respaldan la limitación de la finalidad y la minimización de datos; no constituyen una comprobación automática del cumplimiento normativo. [Los artículos 5 y 25 del RGPD](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) abordan dichos principios y la protección desde el diseño y por defecto. La base jurídica, la necesidad, las condiciones relativas a las categorías especiales cuando proceda, la conservación, la seguridad y el acceso de los destinatarios siguen requiriendo una decisión adecuada al caso concreto. El mero hecho de que exista una finalidad procesal no hace que toda divulgación sea lícita. Los datos seudonimizados siguen siendo, por lo general, datos personales; véase la [explicación del CEPD](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisation-pseudonymisation_en).

El texto libre, las fechas, los acontecimientos poco comunes y las combinaciones de hechos pueden identificar a personas incluso después de eliminar los nombres. Es preferible omitir texto cuando el contenido del mensaje sea innecesario; examina la versión completa cuando sea necesario. Mantén protegidos la fuente y el almacén, acuerda la conservación y el intercambio con la persona responsable, y registra qué ZIP exacto se ha entregado.

GitHub Actions permite exportar toda la cuenta o chats seleccionados mediante Takeout o la API normal，y crear un diario de un chat．La guía [GitHub Actions](https://phishdestroy.github.io/TgWitness/docs/capture/) explica la verificación de ajustes y el límite de 120 minutos．Las exportaciones locales y copias para compartir no heredan la atestación de GitHub，y las pruebas sintéticas no demuestran el funcionamiento con una cuenta real de Telegram．

[Formato de las pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/) · [Informes de casos](https://phishdestroy.github.io/TgWitness/es/docs/reference/case-reports/)
