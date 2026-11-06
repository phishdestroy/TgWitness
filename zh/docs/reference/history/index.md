# 加载源代码历史记录

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/history/

从已启用的来源加载历史消息，暂停和恢复操作，并验证带签名的进度报告。

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## 暂停、重启和部分结果

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- 消息观察、附件处理和光标提交在一笔事务中完成。 恢复运行时不会重复已提交的观察结果。实时捕获或 单独、显式启动的运行可独立观察同一条消息。
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- 无法访问的来源以及在采集过程中被禁用的来源仍会显示为 “失败”或“跳过”。其他来源将继续采集；最终结果将不完整。
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

历史记录补全仅指历史记录的读取操作。附件可能仍处于待处理状态、 处理失败，或被配置的策略排除。请在日志 和附件队列中检查媒体回执；只有字节数据完整且已保存的回执才构成 已保存的附件。历史记录操作是一项显式的快照请求，与 用于选择未来实时事件类别的开关独立。

## 传输与验证

保存**已签名的进度报告**，然后使用**“导出证据**”功能下载 日志和已保存的附件。后续的证据导出可能包含额外记录； 该报告将其计数器与创建时的日志前缀绑定。 请从此版本的可信代码检出中运行验证器：

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

采集光标代表本地工作区的状态。仅恢复证据 ZIP 文件并 不会恢复待处理的采集任务或 Telegram 会话。若需继续执行原始任务， 请保留工作区备份。
