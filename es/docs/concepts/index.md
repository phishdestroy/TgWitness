# Vea cómo funciona el registro de pruebas

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/concepts/

Los mensajes cambian. Su registro de lo que vio no debería, y cualquiera debería poder comprobarlo.

Dos pequeños experimentos abajo. Mensajes ficticios, todo funciona en su navegador, nada va a Telegram.

## De una exportación de chat a un registro verificable

Una [exportación de Telegram Desktop](https://telegram.org/blog/export-and-more) guarda el historial que ve ahora en HTML o JSON. TgWitness añade un diario continuo de cambios, firmas en cada registro y puntos de control con los que otros pueden comparar.

| Tarea | Exportación desde Telegram Desktop | TgWitness |
| --- | --- | --- |
| Leer conversaciones guardadas | HTML o JSON con archivos multimedia seleccionados | Chats guardados, diario con función de búsqueda e informes sin conexión |
| Seguir la evolución a lo largo del tiempo | El historial disponible al exportarlo | Versiones antiguas, ediciones posteriores y borrados, todo guardado |
| Revisar los archivos tras la entrega | Los archivos de exportación estándar en formato HTML/JSON no están firmados. | Manifiesto firmado, registros firmados e informes sellados, comprobados con una clave de confianza |
| Comparar con un estado anterior conservado | Conserva una copia de referencia separada o un hash | Puntos de control firmados, un testigo independiente y marcas de tiempo externas opcionales |

La comparación se basa en el [código de exportación de Telegram Desktop](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) a 2 de noviembre de 2026.

## Un mensaje, tres observaciones

Un mensaje nuevo, una edición y un borrado se convierten en tres registros separados. La edición no sobrescribe el primero y el borrado no lo elimina.

01 / RECORRIDO DEL MENSAJESecuencia ilustrativa

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Recopilador · Registro · Actualización → · añadir →

VISTA DEL CHAT ACTUAL Mensaje n.º 42

Mensaje eliminado

El mensaje ha desaparecido de la vista del chat.

REGISTO DE OBSERVACIONES 3 registros

1. 01

   `message.new`

   Nos vemos a las 10:00

   ✓
2. 02

   `message.edited`

   Nos vemos a las 11:00

   ✓
3. 03

   `message.deleted`

   Aviso de eliminación del n.º 42

   ✓

Las tres observaciones recibidas permanecen en el registro.

Ruta simplificada para una fuente ya seleccionada. Los registros operativos también comparten el diario real. La captura depende de lo que la cuenta pueda ver y de lo que Telegram facilite.

Telegram no dice quién borró un mensaje ni cuándo exactamente. TgWitness deja esos campos vacíos en vez de adivinar.

## Modifique un registro. Siga el hash.

Cada registro contiene el hash del anterior. Un punto de control guardado en otro sitio fija la longitud del diario y el último hash.

02 / HASH-CHAIN SANDBOXSHA-256 real · registros de muestra

REGISTRO 01**Mensaje recibido**`h₁ = SHA-256(e₁)`Enlaces a 64 ceros

REGISTRO 02**Nos vemos a las 11:00**`h₂ = SHA-256(e₂)`Incluye h₁

REGISTRO 03**Se ha observado una eliminación**`h₃ = SHA-256(e₃)`Incluye h₂

CONSERVADO EN OTRO LUGAR**3 registros · encabezado `h₃`**Compare este límite fijo con el registro facilitado.

La modificación de un evento cambia su hash. La reconstrucción de la cadena cambia su cabeza. La eliminación de la cola hace que sea más corta que el punto de control conservado.

**Consulte el registro n.º 2 y los hash completos**

Este es el JSON UTF-8 exacto al que se ha aplicado el hash en este ejemplo. Los valores son ficticios; los nueve campos y la serialización se ajustan al formato del registro.

```

```

Hash del registro guardado n.º 2

``

Hash del registro 2 recalculado

``

Este entorno de pruebas calcula hash, no firmas. El verificador real comprueba además la firma Ed25519, la secuencia y el enlace de cada evento. La mera reconstrucción de los hash no permite crear firmas válidas bajo la clave de confianza.

## Las normas propiamente dichas, en unas pocas líneas

HASH + FIRMA

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** son los nueve campos del evento como JSON UTF-8: claves ordenadas, sin espacios extra, sin escapado ASCII, sin NaN/infinito. `previous_hash` es hi−1, h0 son 64 ceros y las firmas cubren los 32 bytes brutos del resumen.

Los campos: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. Especificación completa: [codificación de eventos](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#event-canonicalization).

PUNTO DE CONTROL CONSERVADO

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Compruebe la firma del punto de control con la clave fijada y luego compárelo con el diario. Una exportación posterior puede ser más larga, pero tiene que coincidir en el punto de control.

## Tres preguntas, tres comprobaciones diferentes

[01 / INTEGRIDAD**¿Ha cambiado este registro?** Hashes y firmas contra una clave de confianza.](https://phishdestroy.github.io/TgWitness/es/docs/exports/)[02 / CONTINUIDAD**¿Qué se había conservado anteriormente?** Compare la exportación con los puntos de control que guardó un testigo.](https://phishdestroy.github.io/TgWitness/es/docs/witness/)[03 / ENTREGA**¿Han llegado estos eventos de prueba?** Envíe, edite y borre mensajes de prueba y vea qué captó cada cuenta.](https://phishdestroy.github.io/TgWitness/es/docs/cases/)

Las firmas responden «¿se cambió?», los puntos de control «¿coincide con lo que había antes?» y los mensajes de prueba «¿lo captamos todo?». [Qué demuestra la verificación y qué no.](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#verification-scope)

Siguiente: una [investigación de cuenta entera](https://phishdestroy.github.io/TgWitness/es/docs/cases/) de principio a fin.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
