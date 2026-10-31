# Vea cómo funciona el registro de pruebas

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/concepts/

Un mensaje puede modificarse. El registro de lo que ha observado debe seguir siendo verificable.

Explore a continuación dos pequeños experimentos. Utilizan mensajes ficticios, se ejecutan directamente en su navegador y nunca se conectan a Telegram.

## Un mensaje, tres observaciones

Cuando Telegram envía un nuevo mensaje, una modificación o un aviso de eliminación, la herramienta de recopilación añade tres registros independientes. La modificación no sustituye al primer registro. Un aviso de eliminación no lo borra.

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

Un aviso de eliminación no proporciona ni una hora de eliminación fiable ni la identidad de la persona que eliminó el mensaje. Mantener desconocidos esos datos preserva la distinción entre una observación y una suposición.

## Modifique un registro. Siga el hash.

Cada registro contiene el hash del registro anterior. Su propio hash abarca los campos del evento, incluido ese enlace. Un punto de control conservado externamente fija una longitud específica del registro y el hash inicial.

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

**C** serializa los nueve campos del evento como JSON en UTF-8: claves ordenadas, sin espacios en blanco adicionales, sin caracteres de escape ASCII y sin valores NaN ni infinito. El `previous_hash` del evento es hi−1. El h0 que se muestra significa 64 caracteres cero; las firmas abarcan los 32 bytes del resumen sin procesar.

Los nueve campos son `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` y `previous_hash`. Esta es [la codificación JSON documentada](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#event-canonicalization) de TgWitness; el hash y la firma en sí mismos no son campos de entrada de hash.

PUNTO DE CONTROL CONSERVADO

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Verifique la firma del punto de control bajo la clave del recopilador fijada y, a continuación, compare su límite con el registro verificado. Una exportación posterior puede contener más registros; no obstante, debe coincidir con el punto de control anterior.

## Tres preguntas, tres comprobaciones diferentes

[01 / INTEGRIDAD**¿Ha cambiado este registro?** Verifique los hash y las firmas con una clave de confianza independiente.](https://phishdestroy.github.io/TgWitness/es/docs/exports/)[02 / CONTINUIDAD**¿Qué se había conservado anteriormente?** Compare una exportación firmada con los puntos de control conservados por un testigo independiente.](https://phishdestroy.github.io/TgWitness/es/docs/witness/)[03 / ENTREGA**¿Han llegado estos eventos de prueba?** Compare las acciones controladas de envío, edición y eliminación con el registro de cada cuenta.](https://phishdestroy.github.io/TgWitness/es/docs/cases/)

Una cadena de hash coincidente responde a una pregunta de integridad. No confirma la entrega completa del mensaje en Telegram, la veracidad de un mensaje ni una hora de observación fiable de forma independiente.

Siga la [investigación completa de la cuenta,](https://phishdestroy.github.io/TgWitness/es/docs/cases/) desde la adquisición hasta el expediente del caso.
