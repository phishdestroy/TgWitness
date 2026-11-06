# Cargar historial de fuentes

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/history/

Carga mensajes anteriores de fuentes habilitadas, pausa y reanuda, y verifica un informe de progreso firmado.

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Pausa, reanudación y resultados parciales

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- La observación del mensaje, la tarea de adjuntar archivos y la confirmación del cursor se realizan en una sola transacción. Una ejecución reanudada no repite las observaciones ya confirmadas. La captura en tiempo real o una ejecución independiente, iniciada explícitamente, puede observar de forma independiente el mismo mensaje.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Las fuentes inaccesibles y aquellas desactivadas durante la adquisición permanecen visibles como fallidas u omitidas. El resto de fuentes continúan; el resultado global es incompleto.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

La finalización del historial describe únicamente las lecturas del historial. Los archivos adjuntos pueden quedar pendientes, fallar o ser excluidos por la política configurada. Comprueba los acuses de recibo multimedia en el registro y en la cola de archivos adjuntos; solo un acuse de recibo completado con los bytes conservados constituye un archivo adjunto guardado. La operación de historial es una solicitud explícita de instantánea y es independiente de los parámetros que seleccionan categorías de futuros eventos en directo.

## Transferir y verificar

Guarda el **informe de progreso firmado** y, a continuación, utiliza la opción **«Exportar pruebas»** para descargar el registro y los archivos adjuntos guardados. Una exportación posterior de pruebas puede incluir registros adicionales; el informe vincula sus contadores al prefijo del registro en el momento de su creación. Ejecuta el verificador desde una copia fiable de esta versión:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

El cursor de adquisición refleja el estado del espacio de trabajo local. La restauración de un archivo ZIP de pruebas por sí sola no restaura un trabajo de adquisición pendiente ni una sesión de Telegram. Conserva la copia de seguridad del espacio de trabajo si es necesario continuar con el trabajo original.
