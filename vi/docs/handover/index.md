# Chuẩn bị bản sao để chia sẻ

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/handover/

Chỉ chia sẻ những gì cần, bản gốc vẫn nguyên vẹn.

Bản bàn giao là một bản trích xuất có chữ ký riêng: chọn cuộc trò chuyện và người, ẩn danh tính hoặc nội dung, chọn tệp và ghi chú của nhóm. Bản kê ghi lại những gì được giữ, cắt bớt và loại bỏ.

## Chuẩn bị bản trích xuất cho người nhận

1. **Xuất → Trích xuất bàn giao**: ghi mục đích, chọn cuộc trò chuyện và khoảng thời gian, **Tải người từ các cuộc trò chuyện đã chọn** nếu bạn cần người có tên.
2. Tất cả những người khác: bí danh, loại bỏ, hoặc như đã ghi. Nội dung và tệp là các công tắc riêng; số điện thoại và email có thể được che.
3. Case Board: không gì cả, dấu trang và lát cắt, hoặc thẻ kèm bình luận. Tên thành viên nhóm có thể đổi thành bí danh.
4. **Tải xuống bản trích xuất bàn giao**, mở ra, xác minh, xem qua trước khi gửi.

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
| Người dùng | Người được chọn giữ nguyên tên; những người khác nhận bí danh hoặc bị loại bỏ. |
| Văn bản | Toàn bộ nội dung, chỉ nội dung của người được chọn và tài khoản của bạn, hoặc không gì cả. |
| Tệp tin | Tệp của người được chọn và tài khoản của bạn, tất cả tệp đang hiển thị, hoặc không gì cả. |
| Bảng trường hợp | Không gì cả, dấu trang và lát cắt, hoặc thẻ kèm thảo luận. |

Hãy đọc cả nội dung và tệp: bí danh không xóa những cái tên được viết bên trong tin nhắn hay tệp đính kèm. Nếu một tệp được chọn bị thiếu, hãy khôi phục nó hoặc loại tệp đính kèm ra.

## Đảm bảo nội dung có thể được kiểm tra độc lập

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Tự giữ kho lưu trữ gốc và các điểm kiểm tra. Người nhận có thể xác minh bản sao của họ mà không cần nhận cả không gian làm việc. Thiết kế: [Report studio](https://phishdestroy.github.io/TgWitness/vi/docs/reports/). Mốc tham chiếu tin cậy: [xác minh bản xuất](https://phishdestroy.github.io/TgWitness/vi/docs/exports/).
