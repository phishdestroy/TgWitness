# Carregar histórico de origem

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/history/

Carregue mensagens anteriores de fontes habilitadas, pause e retome a gravação e verifique um relatório de progresso assinado.

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Pausa, reinício e resultados parciais

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- A observação da mensagem, o processamento do anexo e o registro do cursor ocorrem em uma única transação. Uma execução retomada não repete as observações já registradas. A captura em tempo real ou uma execução separada, iniciada explicitamente, pode observar a mesma mensagem de forma independente.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Fontes inacessíveis e fontes desativadas durante a aquisição permanecem visíveis como falhadas ou ignoradas. Outras fontes continuam; o resultado geral fica incompleto.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

A conclusão do histórico descreve apenas as leituras do histórico. Os anexos podem permanecer pendentes, falhar ou ser excluídos pela política configurada. Verifique os recibos de mídia no registro e na fila de anexos; somente um recibo concluído com bytes preservados constitui um anexo salvo. A operação do histórico é uma solicitação explícita de instantâneo e é distinta das opções que selecionam categorias de eventos ao vivo futuros.

## Transferir e verificar

Salve o **relatório de progresso assinado** e, em seguida, use **a opção “Exportar evidências”** para baixar o registro e os anexos salvos. Uma exportação posterior de evidências pode incluir registros adicionais; o relatório vincula seus contadores ao prefixo do registro no momento em que foi criado. Execute o verificador a partir de uma cópia confiável desta versão:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

O cursor de aquisição representa o estado local da área de trabalho. A restauração de um arquivo ZIP de evidências, por si só, não restaura uma tarefa de aquisição pendente nem uma sessão do Telegram. Mantenha o backup da área de trabalho caso seja necessário dar continuidade à tarefa original.
