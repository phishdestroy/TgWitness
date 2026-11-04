# Quản lý kho lưu trữ

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/archive/

Tìm tin nhắn. Kiểm tra nguồn. Xây dựng hồ sơ vụ việc.

01**Hiển thị lịch sử**

Kéo tin nhắn cũ từ các nguồn đã bật vào không gian làm việc.

02**Theo dõi các nguồn**

Tìm kiếm, rồi mở tin nhắn đã lưu đằng sau mỗi kết quả.

03**Giữ cho phần chuyển giao thông tin rõ ràng**

Phân tích của bạn trong một tệp, bằng chứng có chữ ký nằm bên cạnh.

Các bản ghi được thu thập, văn bản được nhận diện và kết luận của nhà phân tích được phân biệt rõ ràng.

## Tải các tin nhắn trước đây

1. **Nguồn → Trò chuyện trong phạm vi**: kiểm tra các cuộc trò chuyện đã bật, bắt đầu quan sát.
2. **Tải toàn bộ lịch sử**. Nó lấy danh sách nguồn đúng như hiện tại.
3. **Tạm dừng lịch sử** / **Tiếp tục lịch sử** bất cứ lúc nào. Sau khi khởi động lại, hãy tiếp tục thủ công.
4. Kiểm tra kết quả theo từng nguồn và hàng đợi tải xuống, giữ báo cáo tiến độ có chữ ký cùng bản xuất.

Việc này lấp đầy không gian làm việc. Xuất HTML/JSON một cuộc trò chuyện là chuyện khác. [Chi tiết](https://phishdestroy.github.io/TgWitness/vi/docs/reference/history/).

## Tìm kiếm trước, sau đó quyết định về AI

1. **Sổ nhật ký** tìm kiếm cục bộ, lọc theo nguồn và thời gian.
2. Tìm một cụm từ hoặc tên miền, mở bản ghi và các phiên bản của nó.
3. Để dùng AI, quản trị viên thiết lập nhà cung cấp trong **Tích hợp**. Sau đó **Hỏi kho lưu trữ**: chọn cuộc trò chuyện và khoảng thời gian, xem **Dữ liệu được gửi đến mô hình** và bỏ chọn những gì không được gửi ra ngoài.
4. Kiểm tra trích dẫn, lưu câu trả lời thành báo cáo, thêm ghi chú của bạn.

Tìm kiếm không cần AI. Báo cáo giữ nguồn và các bản sửa đổi riêng, tách khỏi sổ nhật ký có chữ ký. [Thiết lập nhà cung cấp](https://phishdestroy.github.io/TgWitness/vi/docs/reference/analysis/).

## Chọn kết nối phù hợp với nhu cầu của bạn

| Nhiệm vụ | Mở | Cài đặt |
| --- | --- | --- |
| Cho phép ứng dụng AI đọc các cuộc trò chuyện được chọn | **Tích hợp → MCP** | [Cài MCP, tạo token giới hạn phạm vi, kết nối](https://phishdestroy.github.io/TgWitness/vi/docs/reference/mcp/) |
| Nhận diện văn bản trong các tệp phương tiện đã lưu | Một bản ghi `media.saved` → **Nhận diện tệp đính kèm** | [Thiết lập worker Docker cục bộ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/media-analysis/) |
| Gửi sự kiện đến n8n hoặc một hệ thống SIEM | **Tích hợp → Webhook đi** | [Thêm bên nhận, kiểm tra HMAC, loại trùng ID](https://phishdestroy.github.io/TgWitness/vi/docs/reference/webhooks/) |

**Token truy cập nào được sử dụng ở đâu?**

Quyền vào bảng điều khiển là cho con người. MCP có token chỉ đọc riêng, webhook có khóa bí mật HMAC riêng. Không cái nào cần phiên Telegram.

[Chia sẻ quyền truy cập bảng điều khiển](https://phishdestroy.github.io/TgWitness/vi/docs/access/) hoặc [cấu hình máy khách MCP](https://phishdestroy.github.io/TgWitness/vi/docs/reference/mcp/).

## Cung cấp nguồn thông tin và kết luận

Đặt báo cáo cạnh tệp ZIP có chữ ký. Báo cáo là cách bạn đọc các nguồn, còn ZIP là thứ người nhận xác minh.

[Xuất và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/exports/) · [Tiến hành một cuộc điều tra toàn diện](https://phishdestroy.github.io/TgWitness/vi/docs/cases/)
