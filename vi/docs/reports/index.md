# Telegram · Thiết kế báo cáo

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reports/

Đưa người đọc từ câu hỏi của vụ việc thẳng tới các bản ghi đã lưu.

Report studio ghép dữ liệu bạn chọn, lịch sử thay đổi, biểu đồ và các phát hiện của bạn. Tám thiết kế, HTML và PDF gốc. Mọi báo cáo HTML, PDF và JSON đều được niêm phong bằng khóa của bạn.

## Tạo báo cáo trong ba bước

1. **Xuất → Cấu hình và xem trước → Dữ liệu**: toàn bộ không gian làm việc, hoặc chọn cuộc trò chuyện, tác giả, ngày (UTC, lúc TgWitness thấy bản ghi) và loại bản ghi.
2. **Thiết kế & nội dung**: chọn thiết kế và những gì được đưa vào: biểu đồ, người tham gia, bản ghi hội thoại, thay đổi, mục Case Board, chi tiết vụ việc và ghi chú của bạn.
3. **Xem trước**: kiểm tra số lượng, hoạt động, mẫu và các dải ID bị thiếu. Lưu, rồi tải định dạng bạn cần.

### Sắp xếp lại các tài liệu đã lưu trữ sao cho phù hợp với người đọc

Ví dụ tổng hợp · bố cục sơ đồ, không phải báo cáo được tạo tự động

1. **Chọn.** Chọn hai cuộc trò chuyện và khoảng thời gian quan sát cho vụ việc.
2. **Soạn thảo.** Chọn bố cục và các phần trả lời câu hỏi.
3. **Xem trước.** Kiểm tra số lượng đã chọn và văn bản trước và sau khi dịch đã được lưu.
4. **Xác minh.** Tạo tệp cuối cùng và kiểm tra chữ ký của tệp đó so với dấu vân tay của không gian làm việc đáng tin cậy.

#### Một số lưu ý

2 cuộc trò chuyện · 1 ngày quan sát

Tin nhắn, các thao tác chỉnh sửa và thông báo xóa

#### Cấu trúc báo cáo

##### Đã thay đổi địa chỉ nhận thanh toán

Câu hỏi vụ việc → phạm vi → kết quả → tham chiếu hồ sơ

**Bối cảnh tin nhắn**

Ghi chú #142: “Sử dụng liên kết thanh toán mới.”

**Thay đổi đã lưu**

Trước: old.example.invalid → Sau: new.example.invalid

#### Xem lại các lựa chọn

18 nhận xét · 2 bản sửa đổi đã lưu

Thời gian gửi, chỉnh sửa và quan sát có các nhãn riêng biệt.

#### Sản phẩm cuối cùng

Tệp PDF đã ký + tệp JSON đã ký, hoặc tệp ZIP đã ký kèm theo báo cáo có thể đọc được

Người nhận kiểm tra tệp và dấu vân tay đáng tin cậy.

## Chọn phong cách trình bày

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, and Ledger & margin**: cùng bản ghi, khác diện mạo. Khi chuyển, lựa chọn và ghi chú của bạn vẫn được giữ. Bất kỳ ngôn ngữ nào trong 25 ngôn ngữ.

PDF được tạo bằng phông chữ đi kèm, không cần trình duyệt. Tiếng Trung, Nhật và Hàn cần phông chữ như Noto Sans CJK trên máy chủ (toàn hệ thống hoặc trong `TGWITNESS_FONT_DIR`), nếu không bạn chỉ có HTML và JSON.

## Đọc nội dung thay đổi cùng với bối cảnh của nó

Lần sửa hiển thị trước và sau, lần xóa hiển thị phiên bản đã lưu cuối cùng. Trả lời, chuyển tiếp, biểu cảm, nút và tệp đính kèm giữ nguyên tham chiếu.

Bản xem trước thiết kế dùng 50.000 bản ghi đầu tiên, bản xem trước dữ liệu đếm chính xác mọi thứ. Để xem bố cục trang cuối cùng, hãy tạo PDF.

## Chọn bản dành cho người nhận một cách cẩn thận

Bộ lọc chỉ định hình báo cáo, ZIP bằng chứng vẫn chứa toàn bộ sổ nhật ký và tệp. Nếu người nhận chỉ nên nhận ít hơn, hãy dùng [bản bàn giao rút gọn](https://phishdestroy.github.io/TgWitness/vi/docs/handover/). Thêm: [nội dung báo cáo](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-reports/), [xác minh bản xuất](https://phishdestroy.github.io/TgWitness/vi/docs/exports/).
