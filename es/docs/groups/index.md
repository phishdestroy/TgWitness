# Gestionar un grupo de cuentas

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/groups/

Gestione varias cuentas juntas, cada una con sus propios registros y su clave.

Un grupo reúne en una pantalla el estado de conexión, iniciar/pausar, los ajustes compartidos y las exportaciones. Práctico cuando varias cuentas trabajan el mismo caso.

## Abrir la vista general del grupo

Abra el grupo en **Cuentas**. Cada cuenta muestra su estado, ruta, latencia y último mensaje guardado. **Requiere atención** lista las que fallan y **Arreglar** le lleva directo.

**Iniciar todas** / **Pausar todas** preguntan antes de actuar. Los **Ajustes del grupo** se comparten, pero los valores propios de una cuenta se mantienen hasta que los sustituya.

### Revisar un cambio de ruta en un grupo

Ejemplo sintético · comprobaciones ilustrativas y resultados

1. **Seleccionar.** Elige el grupo y revisa qué cuentas cambiarán.
2. **Prepárate.** Mantén la ruta propia de una cuenta cuando deba permanecer separada.
3. **Comprobar.** Probar la conexión propuesta e inspeccionar los resultados medidos.
4. **Aplicar.** Volver a comprobar antes de guardar y revisar el resultado para cada cuenta.

#### Equipo del caso

Recopilador de canales · Recopilador de grupos · Cuenta de referencia

3 espacios de trabajo independientes

#### Selección revisada

Dos cuentas siguen la ruta propuesta.

La cuenta de referencia sigue su propio recorrido.

#### Comprobaciones previas

Recopilador de canales: tiempo de transmisión de Telegram: 84 ms

Recopilador de grupo: tiempo de transmisión de Telegram: 91 ms

Estas cifras son valores ficticios que sirven a modo de ejemplo.

#### Resultados de la solicitud

Recopilador de canales: ruta guardada, observación reanudada.

Recopilador de grupo: la comprobación ha fallado, se han restablecido los ajustes anteriores.

Cuenta de referencia: se mantiene la ruta propia.

## Modifica la ruta añadiendo un paso de revisión

1. **Cambiar la ruta del grupo**, elija tipo y ajustes.
2. **Revisar selección**: qué cuentas cambian y cuáles tienen ruta propia.
3. **Preparar y comprobar** prueba una conexión nueva con Telegram y, cuando se puede, la IP de salida.
4. **Aplicar conexión comprobada** y mire cada resultado. Las cuentas activas continúan; las inactivas siguen así.

La latencia es el tiempo de establecer la conexión con Telegram; la IP de salida es la que mostró la ruta al comprobarla. Los resultados pueden variar por cuenta.

## Utilizar el acceso superpuesto

**Chats que ven varias cuentas** lista las fuentes compartidas y su cobertura. Canales y supergrupos se pueden exportar con varias cuentas a la vez mediante **Exportar con … cuentas**. Los chats privados y grupos básicos no: allí los números de mensaje son por cuenta.

## Exportar el grupo como un paquete

**Exportar grupo** da un ZIP con la exportación firmada de cada cuenta y una lista firmada de ellas. Cada una conserva su huella para la verificación. La cronología unificada la monta usted.

Siguiente: [informes](https://phishdestroy.github.io/TgWitness/es/docs/reports/), [Case Board](https://phishdestroy.github.io/TgWitness/es/docs/case-board/), [verificar exportaciones](https://phishdestroy.github.io/TgWitness/es/docs/exports/).
