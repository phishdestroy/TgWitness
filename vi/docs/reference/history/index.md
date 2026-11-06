# Tải lịch sử nguồn

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/history/

Tải các tin nhắn trước đây từ các nguồn đã được kích hoạt, tạm dừng và tiếp tục, đồng thời xác minh báo cáo tiến độ có chữ ký.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Bộ sưu tập](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collection](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Tạm dừng, khởi động lại và kết quả một phần

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- Việc quan sát tin nhắn, xử lý tệp đính kèm và ghi lại vị trí con trỏ được thực hiện trong một giao dịch duy nhất. Một phiên chạy được tiếp tục sẽ không lặp lại các quan sát đã được ghi lại trước đó. Việc ghi lại trực tiếp hoặc một phiên chạy riêng biệt, được khởi động rõ ràng, có thể quan sát độc lập cùng một tin nhắn.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Các nguồn không thể truy cập và các nguồn bị vô hiệu hóa trong quá trình thu thập vẫn hiển thị dưới dạng thất bại hoặc bị bỏ qua. Các nguồn khác tiếp tục hoạt động; kết quả tổng thể là không đầy đủ.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

Việc hoàn tất lịch sử chỉ mô tả các lần đọc lịch sử. Các tệp đính kèm có thể vẫn đang chờ xử lý, thất bại hoặc bị loại trừ theo chính sách đã cấu hình. Kiểm tra biên nhận phương tiện trong sổ ghi chép và hàng đợi tệp đính kèm; chỉ biên nhận đã hoàn tất với các byte được bảo toàn mới được coi là tệp đính kèm đã được lưu. Hoạt động lịch sử là một yêu cầu chụp nhanh rõ ràng và khác biệt với các tùy chọn chọn các danh mục sự kiện trực tiếp trong tương lai.

## Chuyển giao và xác minh

Lưu **báo cáo tiến độ đã được ký**, sau đó sử dụng **tính năng “Xuất bằng chứng”** để tải xuống sổ nhật ký và các tệp đính kèm đã lưu. Việc xuất bằng chứng sau này có thể bao gồm các bản ghi bổ sung; báo cáo này liên kết các bộ đếm của nó với tiền tố của sổ nhật ký tại thời điểm nó được tạo ra. Chạy trình xác minh từ một bản sao đáng tin cậy của phiên bản này:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

Con trỏ thu thập dữ liệu phản ánh trạng thái hiện tại của không gian làm việc cục bộ. Việc khôi phục tệp ZIP chứa bằng chứng sẽ không khôi phục công việc thu thập dữ liệu đang chờ xử lý hoặc phiên Telegram. Hãy giữ bản sao lưu không gian làm việc nếu cần tiếp tục công việc ban đầu.
