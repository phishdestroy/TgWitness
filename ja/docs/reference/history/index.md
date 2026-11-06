# ソース履歴を読み込む

Canonical page: https://phishdestroy.github.io/TgWitness/ja/docs/reference/history/

有効化されたソースから過去のメッセージを読み込み、一時停止や再開を行い、署名付きの進捗レポートを検証します。

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [ドキュメント](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [コレクション](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collection](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## 一時停止、再開、および部分的な結果

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- メッセージの観測、添付ファイルの処理、カーソルのコミットが1つのトランザクションで行われます。 再開された実行では、すでにコミット済みの観測は繰り返されません。ライブキャプチャや 別途明示的に開始された実行では、同じメッセージを独立して観測することができます。
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- アクセスできないソースや、取得中に無効化されたソースは、 「失敗」または「スキップ」として表示されたままになります。その他のソースは処理が継続されますが、全体的な結果は不完全となります。
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

履歴の完了とは、履歴の読み取りのみを指します。添付ファイルは、処理待ちの状態のままとなる場合、 処理に失敗する場合、または設定されたポリシーによって除外される場合があります。ジャーナル および添付ファイルキュー内のメディア受信確認状況を確認してください。バイトデータが保持された完了済みの受信確認のみが、 保存された添付ファイルとみなされます。履歴操作は明示的なスナップショット要求であり、 将来のライブイベントのカテゴリを選択するスイッチとは別個のものです。

## 転送と検証

**署名済みの進捗レポート**を保存した後、**「証拠のエクスポート」**機能を使用して、 ジャーナルと保存された添付ファイルをダウンロードしてください。後に行われる証拠のエクスポートには追加の記録が含まれる場合がありますが、 レポートのカウンターは、作成時点のジャーナルプレフィックスに紐付けられています。 このバージョンの信頼できるチェックアウトから検証ツールを実行してください：

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

取得カーソルはローカルワークスペースの状態を表します。証拠用ZIPファイルを復元しただけでは、 保留中の取得ジョブやTelegramセッションは復元されません。元のジョブを継続する必要がある場合は、 ワークスペースのバックアップを保管しておいてください。
