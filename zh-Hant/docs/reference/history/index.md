# 載入來源歷史紀錄

Canonical page: https://phishdestroy.github.io/TgWitness/zh-Hant/docs/reference/history/

從已啟用的來源載入過往訊息、暫停與恢復操作，並驗證經簽署的進度報告。

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## 暫停、重新開始與部分結果

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- 訊息監測、附件處理及游標提交均於單一交易中完成。 恢復執行的任務不會重複已提交的監測結果。即時擷取或 另一項明確啟動的獨立執行任務，可獨立監測同一則訊息。
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- 無法存取的來源，以及在擷取過程中被停用的來源，仍會顯示為 「失敗」或「跳過」。其餘來源則會繼續運作；整體結果將不完整。
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

歷史記錄完成僅指歷史記錄的讀取操作。附件可能仍處於待處理狀態、 失敗，或因設定的政策而被排除。請檢查日誌中的媒體回執 及附件佇列；僅當回執已完成且位元組內容完整保留時， 才構成已儲存的附件。歷史記錄操作屬於明確的快照請求， 與用於篩選未來即時事件類別的開關設定相互獨立。

## 傳輸與驗證

儲存**已簽署的進度報告**後，請使用**「匯出證據」**功能下載 日誌及已儲存的附件。後續的證據匯出可能包含額外記錄； 該報告會將其計數器與日誌建立當下的前綴綁定。 請從此版本的可信賴版本中執行驗證器：

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

擷取游標代表本地工作區的狀態。僅還原證據 ZIP 檔案並 不會還原待處理的擷取工作或 Telegram 會話。若需繼續執行原始工作， 請保留工作區備份。
