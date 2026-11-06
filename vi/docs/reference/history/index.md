# Tải lịch sử nguồn

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/history/

Tải các tin nhắn trước đây từ các nguồn đã được kích hoạt, tạm dừng và tiếp tục, đồng thời xác minh báo cáo tiến độ có chữ ký.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Bộ sưu tập](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Bộ sưu tập](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

Trong **Sources**, xem lại các cuộc trò chuyện đã bật, tạm dừng quan sát, chọn Standard API hoặc Takeout export, sau đó chọn **Load full history**. Quá trình chạy sẽ sửa danh sách các nguồn đó và đọc các tin nhắn trong quá khứ có sẵn của chúng vào Chats và nhật ký quan sát đã ký. Tệp đa phương tiện sử dụng các cài đặt tệp đính kèm hiện có và hàng đợi tải xuống bền vững. Điều này tách biệt với việc xuất JSON/HTML đã ký cho từng cuộc trò chuyện.

Để thu thập trên toàn tài khoản, hãy chọn **Toàn bộ tài khoản**, bắt đầu quan sát để tải danh sách nguồn của nó, và xem lại danh sách đó trước khi bắt đầu lịch sử. Giới hạn danh sách hộp thoại vẫn áp dụng (mặc định là 1,000, có thể điều chỉnh trong Tham số). Một lần chạy thành công không chứng minh rằng mọi hộp thoại trong tài khoản đều đã được liệt kê. Các cuộc trò chuyện được phát hiện hoặc kích hoạt sau đó cần một lần chạy khác. Tạm dừng quan sát trước khi bắt đầu lịch sử; mỗi lần thu thập chỉ xử lý một tài khoản tại một thời điểm.

Chọn từ một đến năm công cụ xử lý tệp đính kèm và quyết định có giữ lại các Hành động gần đây có sẵn hay không, cũng như so sánh với các phiên bản đã lưu trước đó. Việc trích xuất có thể yêu cầu phê duyệt trong Telegram và thời gian chờ do máy chủ quy định. Các tùy chọn này sẽ được giữ nguyên khi tiếp tục. Xem [hành vi Backfill và hợp đồng bằng chứng](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) để biết chi tiết về truyền tải, thử lại và độ tin cậy.

## Tạm dừng, khởi động lại và kết quả một phần

- **Lịch sử tạm dừng** ngừng đọc. **Lịch sử tiếp tục** tiếp tục từ tin nhắn cuối cùng đã được lưu trong mỗi nguồn; việc khởi động lại ứng dụng cũng khiến quá trình chạy bị tạm dừng cho đến khi được tiếp tục. Việc tiếp tục yêu cầu cùng một tài khoản Telegram không hoạt động.
- Việc quan sát tin nhắn, xử lý tệp đính kèm và ghi lại vị trí con trỏ được thực hiện trong một giao dịch duy nhất. Một phiên chạy được tiếp tục sẽ không lặp lại các quan sát đã được ghi lại trước đó. Việc ghi lại trực tiếp hoặc một phiên chạy riêng biệt, được khởi động rõ ràng, có thể quan sát độc lập cùng một tin nhắn.
- Mỗi nguồn (mỗi phạm vi phân chia Telegram trong Takeout) sẽ cố định một ID tin nhắn tối đa ngay từ lần đọc đầu tiên. Các tin nhắn mới hơn thuộc về quan sát trực tiếp, chứ không thuộc về các trang lịch sử còn lại của nguồn đó.
- Các nguồn không thể truy cập và các nguồn bị vô hiệu hóa trong quá trình thu thập vẫn hiển thị dưới dạng thất bại hoặc bị bỏ qua. Các nguồn khác tiếp tục hoạt động; kết quả tổng thể là không đầy đủ.
- Thời gian chờ FloodWait tuân thủ khoảng thời gian chờ đã lưu của tài khoản. Các lỗi tạm thời sẽ được thử lại tối đa năm lần; khi hết lượt thử hoặc dung lượng đĩa thấp, quá trình sẽ tạm dừng nhưng con trỏ vẫn được giữ nguyên.
- **Kết thúc phiên chạy lịch sử này** giữ lại các quan sát đã lưu. Tính năng này không xóa chúng hoặc hủy các tác vụ đính kèm theo API tiêu chuẩn. Việc kết thúc Takeout sẽ đánh dấu các tệp Takeout còn lại là đã bỏ qua; việc tạm dừng cho phép tiếp tục các tác vụ này sau này. Một phiên chạy mới sẽ đọc lại các nguồn đã bật.

Việc hoàn tất lịch sử chỉ mô tả các lần đọc lịch sử. Các tệp đính kèm có thể vẫn đang chờ xử lý, thất bại hoặc bị loại trừ theo chính sách đã cấu hình. Kiểm tra biên nhận phương tiện trong sổ ghi chép và hàng đợi tệp đính kèm; chỉ biên nhận đã hoàn tất với các byte được bảo toàn mới được coi là tệp đính kèm đã được lưu. Hoạt động lịch sử là một yêu cầu chụp nhanh rõ ràng và khác biệt với các tùy chọn chọn các danh mục sự kiện trực tiếp trong tương lai.

## Chuyển giao và xác minh

Lưu **báo cáo tiến độ đã được ký**, sau đó sử dụng **tính năng “Xuất bằng chứng”** để tải xuống sổ nhật ký và các tệp đính kèm đã lưu. Việc xuất bằng chứng sau này có thể bao gồm các bản ghi bổ sung; báo cáo này liên kết các bộ đếm của nó với tiền tố của sổ nhật ký tại thời điểm nó được tạo ra. Chạy trình xác minh từ một bản sao đáng tin cậy của phiên bản này:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Giữ riêng biệt dấu vân tay khóa ký dự kiến. Trình xác minh kiểm tra chữ ký báo cáo, kho lưu trữ bằng chứng, điểm kiểm tra báo cáo, kế hoạch nguồn, tài khoản và số lượng tin nhắn đã lưu/không khả dụng. Các lần chạy mới cũng liên kết tiến trình nguồn và các tùy chọn với các sự kiện con trỏ đã ký. Nếu không có `--evidence`, công cụ chỉ kiểm tra báo cáo đã ký và tính nhất quán nội bộ của nó. Các trường tiến trình cũ và tóm tắt tệp đính kèm vẫn là các tuyên bố đã ký của người thu thập. Công cụ xác minh bằng chứng kiểm tra các byte phương tiện đã lưu trữ.

Việc ký hoặc hoàn tất lịch sử có sẵn không chứng minh nguồn gốc từ Telegram, một bản chụp nhanh nguyên tử hoặc tính đầy đủ lịch sử. Tin nhắn có thể thay đổi trong khi đọc; các tin nhắn đã xóa và các chỉnh sửa trung gian nằm ngoài các Hành động Gần đây có sẵn, cũng như các Cuộc trò chuyện Bí mật, sẽ không được khôi phục. Một người vận hành kiểm soát khóa ký có thể tạo ra một nhật ký trước khi có các cam kết từ bên ngoài. Hãy sử dụng các điểm kiểm tra được lưu giữ riêng biệt hoặc một nhân chứng độc lập để xác minh các tính chất phát hiện sự can thiệp đã được ghi chép.

Con trỏ thu thập dữ liệu phản ánh trạng thái hiện tại của không gian làm việc cục bộ. Việc khôi phục tệp ZIP chứa bằng chứng sẽ không khôi phục công việc thu thập dữ liệu đang chờ xử lý hoặc phiên Telegram. Hãy giữ bản sao lưu không gian làm việc nếu cần tiếp tục công việc ban đầu.
