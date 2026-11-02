# Chuẩn bị bản sao để chia sẻ

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/handover/

Chia sẻ các quan sát liên quan đồng thời giữ nguyên không gian làm việc ban đầu.

Việc bàn giao là một bản trích xuất riêng biệt đã được ký tên. Chọn các cuộc trò chuyện và người tham gia, rút gọn thông tin nhận dạng hoặc nội dung văn bản, và quyết định những tệp tin và ghi chú của nhóm nào sẽ được đưa vào bản sao của người nhận. Danh sách nội dung (manifest) ghi lại các mục đã chọn cùng số lượng bản ghi không thay đổi, đã rút gọn và bị loại bỏ.

## Chuẩn bị bản trích xuất cho người nhận

1. Mở **Exports → Handover extract**. Ghi rõ mục đích, chọn các cuộc trò chuyện và khoảng thời gian UTC (tùy chọn), sau đó chọn **Load people of the chosen chats** nếu bạn cần các đối tượng được nêu tên.
2. Chọn cách xử lý các đối tượng khác: sử dụng biệt danh, bỏ qua tin nhắn của họ hoặc hiển thị nguyên văn như đã ghi lại. Đặt nội dung tin nhắn và tệp đính kèm một cách độc lập; tùy chọn che giấu số điện thoại và địa chỉ email.
3. Hãy quyết định xem có nên bao gồm các dấu trang và phần trích xuất của Case Board, hay các thẻ kèm bình luận hay không. Các biệt danh của điều tra viên có thể thay thế tên nhóm trong bản dịch này.
4. Chọn **“Tải xuống bản trích xuất bàn giao**”. Mở báo cáo đã tạo và các bản ghi đã chọn trên máy tính cục bộ, xác minh kho lưu trữ và kiểm tra bản sao trước khi gửi đi.

### Một bản gốc, một bản sao để chia sẻ có chủ đích

Ví dụ tổng hợp · chỉ mang tính minh họa

1. **Chọn.** Bao gồm cuộc trò chuyện của vụ việc và xác định người mà đoạn trích liên quan đến.
2. **Tối giản hóa.** Chọn cách hiển thị người tham gia khác trong bản sao được chia sẻ.
3. **Kiểm tra.** Mở báo cáo và các bản ghi trong tệp lưu trữ đã tạo trước khi gửi.
4. **Chia sẻ.** Gửi bản đã kiểm tra và thông báo mã băm đáng tin cậy của bản dịch này riêng biệt.

#### Quan sát ban đầu

Nora · người dùng 71002

“Tôi đã nhận được liên kết đã được sửa đổi.”

Tạp chí nguồn lưu giữ quan sát đã lưu này.

#### Bản dành cho người nhận

Hiển thị như đã ghi lại: Nora · người dùng 71002 · “Tôi đã nhận được liên kết đã được sửa đổi.”

Bí danh: P01 · “Tôi đã nhận được liên kết đã được sửa đổi.”

Loại bỏ: tin nhắn của người tham gia này không được đưa vào bản dịch.

#### Kiểm tra các tệp thực tế

Đọc tệp report.html và records.jsonl.

Kiểm tra danh tính, nội dung văn bản, tệp đính kèm và các bình luận tùy chọn của nhóm.

#### Trích đoạn đã ký

Lựa chọn + băm tệp + bản kê khai đã ký

Một gói riêng biệt được liên kết với ranh giới nhật ký nguồn của nó

## Sử dụng các điều khiển này cùng nhau

| Kiểm soát | Ảnh hưởng đến nội dung bản dịch |
| --- | --- |
| Người dùng | Giữ nguyên danh tính của các đối tượng được chọn; ẩn danh hoặc loại bỏ các bên tham gia khác tùy theo lựa chọn. |
| Văn bản | Bao gồm toàn bộ văn bản, chỉ văn bản của những người được chọn và tài khoản quan sát, hoặc loại bỏ nội dung tin nhắn cùng các trường chi tiết chứa văn bản. |
| Tệp tin | Chọn các tệp của những người được chọn và tài khoản theo dõi, tất cả các tệp tin tin nhắn đã hiển thị, hoặc không chọn tệp nào. |
| Case Board | Không chọn các thành phần bảng, dấu trang và các phần cắt, hoặc thẻ có thảo luận nhóm. |

Kiểm tra nội dung văn bản tự do và nội dung tệp cũng như thông tin nhận dạng: việc sử dụng biệt danh không tự động loại bỏ mọi tên được đề cập trong tin nhắn hoặc tệp đính kèm. Nếu tệp được chọn để lưu trữ không khả dụng, hãy khôi phục tệp đó hoặc loại bỏ rõ ràng các tệp đính kèm trước khi tạo bản trích xuất.

## Đảm bảo nội dung có thể được kiểm tra độc lập

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Giữ riêng biệt kho lưu trữ bằng chứng đã ký gốc và các điểm kiểm tra. Quá trình bàn giao ghi lại bản sao của chính nó, do đó người nhận có thể kiểm tra bản sao đã được chuyển giao mà không cần nhận toàn bộ không gian làm việc. [Report Studio](https://phishdestroy.github.io/TgWitness/vi/docs/reports/) cung cấp thiết kế hiển thị của riêng mình; [quá trình xác minh xuất khẩu](https://phishdestroy.github.io/TgWitness/vi/docs/exports/) giải thích các tham chiếu đáng tin cậy.
