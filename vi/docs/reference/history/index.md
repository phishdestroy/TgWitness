# Tải lịch sử nguồn

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/history/

Tải các tin nhắn trước đây từ các nguồn đã được kích hoạt, tạm dừng và tiếp tục, đồng thời xác minh báo cáo tiến độ có chữ ký.

Trong **phần Nguồn**, xem lại các cuộc trò chuyện đã được kích hoạt, bắt đầu quan sát, sau đó chọn **Tải toàn bộ lịch sử**. Quá trình này sẽ cố định danh sách các nguồn đó và đọc các tin nhắn trong quá khứ có sẵn của chúng vào phần Cuộc trò chuyện và sổ nhật ký quan sát có chữ ký. Tệp đính kèm sử dụng các cài đặt đính kèm hiện có và hàng đợi tải xuống bền vững. Điều này tách biệt với việc xuất JSON/HTML có chữ ký cho từng cuộc trò chuyện.

Để thu thập dữ liệu trên toàn tài khoản, hãy chọn **"Toàn bộ tài khoản"**, bắt đầu theo dõi để tải danh sách nguồn của tài khoản đó, và xem xét danh sách đó trước khi bắt đầu ghi lại lịch sử. Giới hạn danh sách cuộc trò chuyện vẫn áp dụng (mặc định là 1.000, có thể điều chỉnh trong phần "Tham số"). Việc chạy thành công không chứng minh rằng mọi cuộc trò chuyện trong tài khoản đều đã được liệt kê. Các cuộc trò chuyện được phát hiện hoặc kích hoạt sau đó cần phải chạy lại.

## Tạm dừng, khởi động lại và kết quả một phần

- **Tạm dừng lịch sử** sẽ ngừng ghi lại. **Tiếp tục lịch sử** sẽ tiếp tục từ tin nhắn cuối cùng đã được lưu trong mỗi nguồn; việc khởi động lại ứng dụng cũng sẽ giữ trạng thái tạm dừng cho đến khi được tiếp tục. Hãy khởi động lại quá trình quan sát trước. Việc tiếp tục yêu cầu phải sử dụng cùng một tài khoản Telegram.
- Việc quan sát tin nhắn, xử lý tệp đính kèm và ghi lại vị trí con trỏ được thực hiện trong một giao dịch duy nhất. Một phiên chạy được tiếp tục sẽ không lặp lại các quan sát đã được ghi lại trước đó. Việc ghi lại trực tiếp hoặc một phiên chạy riêng biệt, được khởi động rõ ràng, có thể quan sát độc lập cùng một tin nhắn.
- Mỗi nguồn sẽ thiết lập một ID tin nhắn tối đa khi lần đầu tiên đọc dữ liệu. Các tin nhắn mới hơn thuộc về quá trình quan sát trực tiếp, chứ không thuộc về các trang lịch sử còn lại của nguồn đó.
- Các nguồn không thể truy cập và các nguồn bị vô hiệu hóa trong quá trình thu thập vẫn hiển thị dưới dạng thất bại hoặc bị bỏ qua. Các nguồn khác tiếp tục hoạt động; kết quả tổng thể là không đầy đủ.
- Thời gian chờ FloodWait tuân thủ khoảng thời gian chờ đã lưu của tài khoản. Các trường hợp hết thời gian chờ truyền tải và dung lượng đĩa thấp sẽ tạm dừng quá trình chạy mà vẫn giữ nguyên vị trí con trỏ. Tiếp tục sau khi khắc phục nguyên nhân.
- **Việc kết thúc phiên ghi lịch sử này** sẽ giữ lại các quan sát đã lưu. Nó không xóa chúng hoặc hủy các tác vụ tải xuống tệp đính kèm đã được xếp hàng. Một phiên ghi mới sẽ đọc lại các nguồn đã được kích hoạt.

Việc hoàn tất lịch sử chỉ mô tả các lần đọc lịch sử. Các tệp đính kèm có thể vẫn đang chờ xử lý, thất bại hoặc bị loại trừ theo chính sách đã cấu hình. Kiểm tra biên nhận phương tiện trong sổ ghi chép và hàng đợi tệp đính kèm; chỉ biên nhận đã hoàn tất với các byte được bảo toàn mới được coi là tệp đính kèm đã được lưu. Hoạt động lịch sử là một yêu cầu chụp nhanh rõ ràng và khác biệt với các tùy chọn chọn các danh mục sự kiện trực tiếp trong tương lai.

## Chuyển giao và xác minh

Lưu **báo cáo tiến độ đã được ký**, sau đó sử dụng **tính năng “Xuất bằng chứng”** để tải xuống sổ nhật ký và các tệp đính kèm đã lưu. Việc xuất bằng chứng sau này có thể bao gồm các bản ghi bổ sung; báo cáo này liên kết các bộ đếm của nó với tiền tố của sổ nhật ký tại thời điểm nó được tạo ra. Chạy trình xác minh từ một bản sao đáng tin cậy của phiên bản này:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Lưu giữ dấu vân tay khóa ký dự kiến một cách độc lập. Trình xác minh kiểm tra chữ ký báo cáo, kho lưu trữ bằng chứng, điểm kiểm tra báo cáo, kế hoạch nguồn, tài khoản và số lượng tin nhắn đã lưu/không khả dụng. Nếu không có `--evidence`, trình xác minh chỉ kiểm tra báo cáo đã ký và tính nhất quán nội bộ của nó. Các giai đoạn tiến trình, tiêu đề, con trỏ và tóm tắt tệp đính kèm là các tuyên bố đã được ký của bên thu thập, không được tái tạo độc lập bởi công cụ kiểm tra báo cáo này. Người xác minh bằng chứng vẫn kiểm tra các byte phương tiện đã lưu trữ.

Việc ký kết hay hoàn tất lịch sử có sẵn đều không chứng minh nguồn gốc từ Telegram, một bản chụp nhanh nguyên tử, hay tính đầy đủ của lịch sử. Tin nhắn có thể thay đổi trong khi đọc; các tin nhắn đã xóa, các chỉnh sửa trung gian chưa được xem và các Cuộc trò chuyện bí mật sẽ không được khôi phục. Một người vận hành kiểm soát khóa ký có thể tạo ra một nhật ký trước khi có các cam kết từ bên ngoài. Hãy sử dụng các điểm kiểm tra được lưu giữ riêng biệt hoặc một nhân chứng độc lập để đảm bảo các tính năng phát hiện giả mạo được ghi lại.

Con trỏ thu thập dữ liệu phản ánh trạng thái hiện tại của không gian làm việc cục bộ. Việc khôi phục tệp ZIP chứa bằng chứng sẽ không khôi phục công việc thu thập dữ liệu đang chờ xử lý hoặc phiên Telegram. Hãy giữ bản sao lưu không gian làm việc nếu cần tiếp tục công việc ban đầu.
