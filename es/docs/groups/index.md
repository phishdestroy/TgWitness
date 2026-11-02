# Gestionar un grupo de cuentas

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/groups/

Gestiona varias cuentas de recopilación a la vez, manteniendo diferenciados los registros y la identidad de firma de cada cuenta.

Un grupo de cuentas reúne el estado de la conexión, los controles de observación, la configuración compartida y las exportaciones en una única vista de trabajo. Resulta útil cuando varias cuentas abarcan la misma investigación o necesitan una configuración operativa coherente.

## Abrir la vista general del grupo

En **«Cuentas»**, abre el grupo. Cada cuenta muestra su estado de observación, la ruta de conexión, la última latencia de ruta medida cuando se ha realizado con éxito una comprobación reciente y el último mensaje guardado. Los enlaces **«Requiere atención»** remiten a las cuentas que necesitan revisión; **«Corregir»** abre el espacio de trabajo y los controles pertinentes.

**Las opciones «Iniciar todo»** y **«Pausar todo»** se aplican a las cuentas que cumplan los requisitos tras la confirmación. **La configuración de grupo** comparte los ajustes seleccionados; las cuentas con sus propios valores los conservan hasta que decidas sustituirlos.

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

1. Selecciona **«Cambiar la ruta del grupo**» y, a continuación, elige el tipo de conexión y la configuración.
2. Selecciona **«Revisar selección**». Revisa las cuentas de la lista y sus modificaciones de ruta individuales.
3. Selecciona **«Preparar y comprobar**». La comprobación utiliza un transporte de Telegram nuevo; las rutas HTTP compatibles también informan de su comprobación de salida HTTPS.
4. Selecciona **«Aplicar conexión marcada»** e inspecciona el resultado de cada cuenta. La observación que se estaba ejecutando anteriormente se reanuda cuando la aplicación tiene éxito; las cuentas inactivas permanecen inactivas.

La latencia describe el tiempo medido de establecimiento de la conexión de Telegram. Una comprobación de la IP de salida describe esa ruta en el momento de la comprobación registrado. La autorización de la cuenta y el estado de la observación tienen sus propios indicadores; un cambio de grupo puede dar lugar a resultados diferentes según la cuenta.

## Utilizar el acceso superpuesto

**La opción «Chats que ven varias cuentas**» muestra las fuentes compartidas y la cobertura de observación del espacio de trabajo disponible. Los canales y supergrupos elegibles pueden utilizar **la opción «Exportar con… cuentas»** para dividir la adquisición del historial de un chat. Los chats privados y los grupos normales permanecen en la cuenta inicial, ya que sus números de mensajes pertenecen al historial de dicha cuenta.

## Exportar el grupo como un paquete

**El grupo «Export»** crea un archivo ZIP que contiene la exportación firmada de cada cuenta y una lista firmada de dichos archivos. Las identidades y huellas digitales originales del espacio de trabajo siguen estando disponibles para su verificación. Elabora una narrativa que abarque todas las cuentas utilizando esas referencias; la línea temporal única fusionada se sigue montando por separado.

Continúa con [el diseño del informe](https://phishdestroy.github.io/TgWitness/es/docs/reports/), [un «Case Board» dentro de un espacio de trabajo](https://phishdestroy.github.io/TgWitness/es/docs/case-board/) o [la verificación de la exportación](https://phishdestroy.github.io/TgWitness/es/docs/exports/).
