# Cargar historial de fuentes

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/history/

Carga mensajes anteriores de fuentes habilitadas, pausa y reanuda, y verifica un informe de progreso firmado.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentación](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Colección](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Recopilación](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

En **Fuentes**, revisa los chats habilitados, pausa la observación, elige la API estándar o la exportación Takeout y, a continuación, selecciona **Cargar historial completo**. La ejecución corrige esa lista de fuentes e importa sus mensajes anteriores disponibles a Chats y al diario de observación firmado. Los archivos multimedia utilizan la configuración de archivos adjuntos existente y la cola de descargas permanente. Esto es independiente de la exportación firmada en formato JSON/HTML por chat.

Para una recopilación de toda la cuenta, selecciona **Toda la cuenta**, inicia la observación para cargar su lista de fuentes y revisa dicha lista antes de iniciar el historial. El límite de la lista de diálogos sigue siendo aplicable (1,000 por defecto, ajustable en Parámetros). Una ejecución satisfactoria no garantiza que se hayan incluido todos los diálogos de la cuenta. Los chats descubiertos o habilitados posteriormente requieren otra ejecución. Pausa la observación antes de iniciar el historial; cada adquisición abarca una cuenta a la vez.

Elige entre uno y cinco procesadores de archivos adjuntos y si deseas conservar las Acciones recientes disponibles y comparar versiones guardadas anteriormente. La extracción puede requerir aprobación en Telegram y un tiempo de espera especificado por el servidor. Estas opciones permanecen fijas al reanudar. Consulta [el comportamiento de Backfill y el contrato de pruebas](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) para obtener detalles sobre el transporte, los reintentos y la confianza.

## Pausa, reanudación y resultados parciales

- **Historial de pausa:** detiene la lectura. **Historial de continuación:** reanuda desde el último mensaje guardado en cada fuente; al reiniciar la aplicación, la ejecución también queda en pausa hasta que se reanude. Para reanudar es necesaria la misma cuenta de Telegram inactiva.
- La observación del mensaje, la tarea de adjuntar archivos y la confirmación del cursor se realizan en una sola transacción. Una ejecución reanudada no repite las observaciones ya confirmadas. La captura en tiempo real o una ejecución independiente, iniciada explícitamente, puede observar de forma independiente el mismo mensaje.
- Cada fuente (cada rango dividido de Telegram en Takeout) establece un ID de mensaje máximo en su primera lectura. Los mensajes más recientes pertenecen a la observación en tiempo real, no a las páginas históricas restantes de esa fuente.
- Las fuentes inaccesibles y aquellas desactivadas durante la adquisición permanecen visibles como fallidas u omitidas. El resto de fuentes continúan; el resultado global es incompleto.
- Los retrasos de FloodWait respetan el tiempo de espera guardado para la cuenta. Los fallos transitorios se reintentan hasta cinco veces; el agotamiento y el espacio insuficiente en disco provocan una pausa sin que se mueva el cursor.
- **: Finalizar esta ejecución del historial.**: conserva las observaciones guardadas. No las elimina ni cancela las tareas de adjuntar archivos de la API estándar. Al finalizar Takeout, marca los archivos de Takeout restantes como omitidos; al pausarlo, se mantienen reanudables. Una nueva ejecución vuelve a leer las fuentes habilitadas.

La finalización del historial describe únicamente las lecturas del historial. Los archivos adjuntos pueden quedar pendientes, fallar o ser excluidos por la política configurada. Comprueba los acuses de recibo multimedia en el registro y en la cola de archivos adjuntos; solo un acuse de recibo completado con los bytes conservados constituye un archivo adjunto guardado. La operación de historial es una solicitud explícita de instantánea y es independiente de los parámetros que seleccionan categorías de futuros eventos en directo.

## Transferir y verificar

Guarda el **informe de progreso firmado** y, a continuación, utiliza la opción **«Exportar pruebas»** para descargar el registro y los archivos adjuntos guardados. Una exportación posterior de pruebas puede incluir registros adicionales; el informe vincula sus contadores al prefijo del registro en el momento de su creación. Ejecuta el verificador desde una copia fiable de esta versión:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Mantener de forma independiente la huella digital esperada de la clave de firma. El verificador comprueba la firma del informe, el archivo de pruebas, el punto de control del informe, el plan de origen, la cuenta y el recuento de mensajes guardados o no disponibles. Las nuevas ejecuciones también vinculan el progreso de origen y las opciones a eventos de cursor firmados. Sin `--evidence`, solo comprueba el informe firmado y su coherencia interna. Los campos de progreso heredados y los resúmenes de archivos adjuntos siguen siendo declaraciones firmadas del recopilador. El verificador de pruebas comprueba los bytes de los archivos multimedia archivados.

Ni la firma ni la finalización del historial disponible demuestran el origen de Telegram, una instantánea atómica o la integridad histórica. Los mensajes pueden cambiar mientras se leen; los mensajes eliminados y las ediciones intermedias fuera de las Acciones recientes disponibles, así como los Chats secretos, no se recuperan. Un operador que controle la clave de firma puede falsificar un registro antes de que existan compromisos externos. Utilice puntos de control conservados por separado o un testigo independiente para las propiedades documentadas de detección de manipulaciones.

El cursor de adquisición refleja el estado del espacio de trabajo local. La restauración de un archivo ZIP de pruebas por sí sola no restaura un trabajo de adquisición pendiente ni una sesión de Telegram. Conserva la copia de seguridad del espacio de trabajo si es necesario continuar con el trabajo original.
