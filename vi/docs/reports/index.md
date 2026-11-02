# Thiết kế báo cáo

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reports/

Hướng dẫn người đọc một lộ trình rõ ràng từ câu hỏi vụ việc đến các bản ghi đã lưu.

Report Studio kết hợp tính năng chọn dữ liệu, lịch sử thay đổi dễ đọc, biểu đồ và các kết luận bằng văn bản của bạn. Tám mẫu thiết kế tích hợp áp dụng cho các định dạng đầu ra HTML và PDF gốc được hỗ trợ. Các báo cáo HTML, PDF và JSON đều có con dấu đã ký riêng; tệp ZIP manifest cũng liên kết các tệp trong gói. HTML và PDF được niêm phong sau khi bố cục cuối cùng hoàn tất.

## Tạo báo cáo trong ba bước

1. Mở **Exports → Configure and preview → Data**. Sử dụng toàn bộ không gian làm việc hoặc chọn các cuộc trò chuyện, tác giả, bao gồm cả ngày quan sát theo UTC và các loại bản ghi. Các ngày này mô tả thời điểm TgWitness quan sát được bản ghi.
2. Trong phần **“Thiết kế & nội dung**”, hãy chọn một mẫu thiết kế và nội dung có sẵn. Chọn biểu đồ hoạt động, nhãn người tham gia, bản ghi chép, các thay đổi đã lưu và tài liệu Case Board tùy chọn. Thêm chi tiết vụ việc và ghi chú điều tra của bạn.
3. Mở **phần** **Xem trước** để xem số liệu thống kê, hoạt động, người tham gia, các bản ghi được lấy mẫu và các dải ID bị thiếu. Lưu cài đặt, sau đó tải xuống định dạng bạn cần.

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

**Các chế độ Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series và Ledger & margin** trình bày cùng một bản ghi cơ bản dưới các bố cục khác nhau. Việc thay đổi thiết kế vẫn giữ nguyên lựa chọn dữ liệu và các ghi chú đã viết. Ngôn ngữ báo cáo có thể được chọn từ 25 ngôn ngữ được hỗ trợ.

Chuỗi đọc nhóm các trường hợp, phạm vi, kết quả và thay đổi xung quanh một thanh phân đoạn. Ledger & margin sử dụng các chương được đánh số và lề rộng. Cả hai đều hỗ trợ tổng quan HTML tài khoản và chia sẻ bản sao. Các tệp PDF gốc được tạo ra với các phông chữ đi kèm; máy tính của người dùng không cần cài đặt trình duyệt hoặc Node để tạo PDF. Các tệp PDF tiếng Trung, tiếng Nhật và tiếng Hàn còn yêu cầu một phông chữ phù hợp trên máy chủ, chẳng hạn như Noto Sans CJK, được cài đặt trên toàn hệ thống hoặc đặt trong thư mục `TGWITNESS_FONT_DIR`. Nếu không có phông chữ này, tệp ZIP sẽ chỉ giữ lại các báo cáo HTML và JSON.

## Đọc nội dung thay đổi cùng với bối cảnh của nó

Các chỉnh sửa đã lưu hiển thị cả phiên bản trước và sau. Thông báo xóa có thể đi kèm với phiên bản cuối cùng được ghi lại. Các phản hồi, trích dẫn, chia sẻ, phản ứng, nút bấm và siêu dữ liệu tệp đính kèm vẫn giữ nguyên các tham chiếu có sẵn. Băm SHA-256 của tệp và băm bản ghi nhật ký được ghi nhãn riêng biệt.

Bản xem trước thiết kế hiển thị các thành phần bìa, kiểm tra và biểu đồ bằng cách sử dụng các bản ghi khớp nhau trong số 50.000 bản ghi nguồn đầu tiên. Bản xem trước dữ liệu riêng biệt quét toàn bộ bản chụp nhật ký ổn định để xác định số lượng lựa chọn chính xác, với các giới hạn mẫu được hiển thị và gắn nhãn. Tạo tệp PDF để kiểm tra cách phân trang cuối cùng. Việc xuất toàn bộ tài khoản có bản tổng quan dưới dạng HTML; các tệp PDF trò chuyện riêng lẻ sử dụng thiết kế đã chọn.

## Chọn bản dành cho người nhận một cách cẩn thận

Các bộ lọc báo cáo giúp định hình báo cáo dễ đọc. Tệp ZIP chứa toàn bộ bằng chứng giữ nguyên nhật ký gốc và các tệp đính kèm. Sử dụng quy trình [bàn giao tối giản](https://phishdestroy.github.io/TgWitness/vi/docs/handover/) khi người nhận chỉ cần nhận dữ liệu đã chọn. Xem [nội dung báo cáo và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-reports/) hoặc [xác minh tệp xuất đã hoàn tất](https://phishdestroy.github.io/TgWitness/vi/docs/exports/).
