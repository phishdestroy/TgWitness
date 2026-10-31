# Cómo funciona el registro de pruebas

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/how-it-works/

Se explican la cadena de hash, las firmas, los puntos de control y los testigos con las fórmulas exactas que utiliza el verificador.

TgWitness conserva lo que ha observado una cuenta recopiladora, vincula dichas observaciones en un registro firmado y permite que otra persona verifique una exportación comparándola con una clave de confianza y un punto de control conservado anteriormente.

El [sitio web de documentación local](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally) incluye ejemplos interactivos en `/docs/concepts/`, así como un explorador de decisiones de puntos de control en `/docs/witness/`. Todos los mensajes de ejemplo, recuentos y retrasos son ficticios. Los hash de la cadena de pruebas se calculan con SHA-256 en el navegador. No se envía nada a Telegram.

## Un mensaje cambia; las observaciones se acumulan

Diagrama de secuencia · Telegram → Recopilador: Nuevo mensaje: Quedamos a las 10:00; Recopilador → Registro firmado: Añadir mensaje.new; Telegram → Recopilador: Edición: Quedamos a las 11:00; Recopilador → Registro firmado: Añadir «mensaje.editado»; Telegram → Recopilador: Aviso de eliminación; Recopilador → Registro firmado: Añadir «message.deleted»; Nota sobre Registro firmado: Se conservan el mensaje original, las modificaciones y las eliminaciones. · Telegram · Recopilador · Registro firmado · Nuevo mensaje: Quedamos a las 10:00 · Añadir mensaje.new · Edición: Quedamos a las 11:00 · Añadir «mensaje.editado» · Aviso de eliminación · Añadir «message.deleted» · Se conservan el mensaje original, las modificacionesy las eliminaciones.

**Diagrama en formato de texto**

1. Telegram → Recopilador: Nuevo mensaje: Quedamos a las 10:00
2. Recopilador → Registro firmado: Añadir mensaje.new
3. Telegram → Recopilador: Edición: Quedamos a las 11:00
4. Recopilador → Registro firmado: Añadir «mensaje.editado»
5. Telegram → Recopilador: Aviso de eliminación
6. Recopilador → Registro firmado: Añadir «message.deleted»
7. Nota sobre Registro firmado: Se conservan el mensaje original, las modificaciones y las eliminaciones.

Esta secuencia simplificada da por hecho que Telegram entregó cada actualización y que la cuenta seleccionada pudo verla. Los eventos operativos también se incluyen en el registro. Una notificación de eliminación no indica quién la realizó ni la hora exacta de la eliminación. Las entregas repetidas se consideran observaciones independientes; no se suprime ningún duplicado en todo el registro.

## Qué abarca un hash

![Observar, codificar, generar un hash y firmar: cada nuevo evento incluye el hash anterior.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

Lea la fórmula de dentro hacia fuera: **C** convierte los nueve campos en bytes exactos; **SHA-256** genera su resumen; **«hex»** indica cómo se almacena dicho resumen. El hash anterior ya se encuentra dentro del evento. **«unhex»** vuelve a convertir el hash almacenado en los 32 bytes que firma Ed25519.

[Diagrama de cadena estática](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

Sea C(ei) el JSON canónico en UTF-8 de los nueve campos de eventos. El primer `previous_hash` consta de 64 caracteres cero. Cada registro posterior incluye el hash hexadecimal del registro anterior:

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

La firma abarca los 32 bytes sin procesar del resumen. La entrada del hash contiene exactamente `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` y `previous_hash`. Las claves de los objetos están ordenadas; se omiten los espacios en blanco y los caracteres de escape ASCII ; se rechazan los valores NaN e infinito. Consulte la [codificación exacta](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#event-canonicalization).

Diagrama de flujo · 64 caracteres nulos → Registro 1 / hash h1; Registro 1 / hash h1 → El registro 2 incluye h1 / hash h2; El registro 2 incluye h1 / hash h2 → El registro 3 incluye h2 / hash h3; El registro 3 incluye h2 / hash h3 → Punto de control firmado: recuento 3, encabezado h3 (conservar en otro lugar) · 64 caracteres nulos · Registro 1 / hash h1 · El registro 2 incluyeh1 / hash h2 · El registro 3 incluyeh2 / hash h3 · Punto de controlfirmado: recuento 3,encabezado h3 · conservar en otro lugar

**Diagrama en formato de texto**

1. 64 caracteres nulos → Registro 1 / hash h1
2. Registro 1 / hash h1 → El registro 2 incluye h1 / hash h2
3. El registro 2 incluye h1 / hash h2 → El registro 3 incluye h2 / hash h3
4. El registro 3 incluye h2 / hash h3 → Punto de control firmado: recuento 3, encabezado h3 (conservar en otro lugar)

| Cambiar al registro facilitado | Qué lo detecta |
| --- | --- |
| Modifique el registro 2 conservando su hash guardado | El hash del evento recalculado difiere; su firma ya no abarca el evento modificado |
| Reconstruya el registro alterado y todos los hash posteriores | Las firmas originales fallan; un punto de control conservado en el límite afectado tampoco coincide. |
| Elimine la parte final, pero mantenga intacto el prefijo restante | Un punto de control anterior conservado, más allá del prefijo facilitado, revela que la exportación es demasiado corta |
| Vuelva a firmar un registro de sustitución con otra clave | Una huella digital de clave de confianza independiente rechaza la identidad sustitutiva |

![Al modificar un campo guardado, se altera su resumen; la reconstrucción de los hash no restaura las firmas originales.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**Pruebe la lógica en el registro 2:** cambie `Meet at 11:00` por `Meet at 12:00` en el evento guardado. Su hash recalculado ya no coincide. El recálculo de la cadena posterior puede reparar sus enlaces, pero no puede hacer que las firmas originales cubran los nuevos resúmenes. Por el contrario, una edición observada en Telegram se convierte en un nuevo registro del diario.

[Diagrama de cambios estáticos](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

Los enlaces de hash por sí solos no impiden que alguien recalcule una cadena de sustitución. La confianza se basa en la verificación de las firmas mediante una clave de confianza independiente y en la comparación con referencias conservadas fuera del recopilador.

## Lo que aporta un punto de control anterior

![Mantenga el recuento en 3 y el encabezado h3; una exportación posterior de 4 registros se comprueba en la posición 3.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**La referencia permanece fija mientras el registro crece.** Si el punto de control indica «3 registros, encabezado h3», una exportación de cuatro registros puede pasar la comprobación al coincidir con h3 en la posición 3. Su encabezado más reciente es h4, del que se espera que sea diferente. Una exportación de solo dos registros falla.

[Diagrama estático de puntos de control](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

Tras verificar la firma del punto de control, solicite:

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

Una exportación puede extenderse más allá de un punto de control. Debe coincidir en el límite retenido. El verificador real también comprueba la secuencia de cada evento, el enlace anterior, el hash y la firma. Si solo se comparara el encabezado final almacenado, se pasaría por alto un registro interior alterado cuyo hash guardado no se hubiera actualizado.

## El lugar que le corresponde a un testigo

Diagrama de flujo · Recopilador / sesión de cuenta / clave A → Punto final de control de solo lectura; Witness / clave de recopilación fijada / clave propia B → Registro de pruebas firmado independiente; Witness / clave de recopilación fijada / clave propia B → Punto final de control de solo lectura (Solicite una comprobación); Punto final de control de solo lectura → Witness / clave de recopilación fijada / clave propia B (Respuesta firmada); Witness / clave de recopilación fijada / clave propia B → Canal con publicaciones firmadas de TGW1 (API del bot / token propio) · Servidor A · Servidor B · Recopilador / sesión decuenta / clave A · Punto final de control desolo lectura · Witness / clave derecopilación fijada /clave propia B · Registro de pruebasfirmado independiente · Canal con publicacionesfirmadas de TGW1 · Solicite una comprobación · Respuesta firmada · API del bot / token propio

**Diagrama en formato de texto**

1. Recopilador / sesión de cuenta / clave A → Punto final de control de solo lectura
2. Witness / clave de recopilación fijada / clave propia B → Registro de pruebas firmado independiente
3. Witness / clave de recopilación fijada / clave propia B → Punto final de control de solo lectura (Solicite una comprobación)
4. Punto final de control de solo lectura → Witness / clave de recopilación fijada / clave propia B (Respuesta firmada)
5. Witness / clave de recopilación fijada / clave propia B → Canal con publicaciones firmadas de TGW1 (API del bot / token propio)

El testigo registra retrocesos, un encabezado diferente con el mismo recuento, claves modificadas, respuestas no válidas y respuestas que faltan. Un recuento mayor por sí solo no garantiza que todos los registros anteriores permanezcan inalterados; compare la exportación con los puntos de control conservados. Un testigo en otro servidor evita verse afectado por las interrupciones del servidor del recopilador; un operador independiente aporta una mayor independencia.

El «witness» certifica el estado del registro notificado por el recopilador. No observa de forma independiente todos los mensajes de Telegram. Véase [la configuración del «witness](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/)».

## Prueba de entrega frente a acciones conocidas

Utilice un grupo controlado, cuentas de recopilación diferenciadas y un marcador nuevo. Envíe, edite y elimine de forma deliberada, comprobando la captura entre cada etapa. Defina las acciones previstas y un límite antes de examinar los resultados.

R = |observed∩expected| / |expected| Δ t = treceipt - taction

Solo cuentan las acciones esperadas que coincidan; los recibos duplicados no aumentan el numerador. El denominador debe ser distinto de cero. Un recibo que falte no tiene un retardo medido. Documente la incertidumbre del reloj; utilice su propio tiempo de acción de eliminación controlado, ya que Telegram no proporciona la hora exacta de eliminación. Un resultado como 5/6 (83,3 %) describe las acciones de prueba, no la exhaustividad de todo el tráfico de Telegram.

## Elija un flujo de trabajo

A continuación se presenta [el proceso completo de investigación](https://phishdestroy.github.io/TgWitness/es/docs/reference/investigation/) tras un incidente que abarca un canal, un grupo, un bot y un chat privado:

1. Active el modo de investigación de toda la cuenta y realice un inventario de todos los chats accesibles.
2. Obtenga instantáneas del registro, el historial completo de cada chat y los archivos adjuntos conservados.
3. Conserve los cambios en tiempo real y cualquier interacción deliberada con los paneles junto con sus comprobantes.
4. Realice un seguimiento de los identificadores numéricos de los remitentes, las relaciones de respuesta, los destinatarios recurrentes y los hashes de los archivos a través de los registros citados y los perfiles de las personas.
5. Reconstruya una cronología entre chats con marcas de tiempo y lagunas explícitas.
6. Compare los espacios de trabajo de otras cuentas manteniendo separados sus orígenes y claves.
7. Recopile y verifique los registros firmados, los perfiles y las exportaciones del historial junto con las notas del caso.

La guía «`/docs/cases/`» del sitio web incluye un mapa interactivo de casos y variantes para disputas entre bots, mensajes eliminados y participantes que cambian de nombre. Las notas de los casos y el análisis entre espacios de trabajo son externos; la aplicación no genera automáticamente un gráfico global de la investigación ni un archivo de casos fusionado.

[Validación completada y trabajo pendiente](https://phishdestroy.github.io/TgWitness/es/docs/reference/verification/) · [Exportar y verificar](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#investigation-handoff) · [Empiece con una cuenta](https://phishdestroy.github.io/TgWitness/es/docs/reference/quickstart/)
