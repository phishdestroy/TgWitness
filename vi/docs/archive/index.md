# Quản lý kho lưu trữ

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/archive/

Tìm tin nhắn. Kiểm tra nguồn. Xây dựng hồ sơ vụ việc.

Các công cụ này hiện có sẵn trên nhánh chính hiện tại. Phiên bản xem trước di động 0.7.0 ra mắt trước đó; hãy sử dụng bản sao mã nguồn để thực hiện quy trình làm việc này.

01**Hiển thị lịch sử**

Tải các tin nhắn trước đây từ các nguồn đã được kích hoạt của bạn vào không gian làm việc.

02**Theo dõi các nguồn**

Tìm kiếm trong kho lưu trữ và mở tin nhắn đã lưu đằng sau mỗi kết quả.

03**Giữ cho phần chuyển giao thông tin rõ ràng**

Lưu phân tích của bạn riêng biệt và xuất bằng chứng đã được ký bên cạnh đó.

Các bản ghi được thu thập, văn bản được nhận diện và kết luận của nhà phân tích được phân biệt rõ ràng.

## Tải các tin nhắn trước đây

1. **Nguồn** mở, xem lại các cuộc trò chuyện đã được kích hoạt và bắt đầu quan sát.
2. Chọn "**Tải toàn bộ lịch sử**". Quá trình chạy sẽ sử dụng danh sách nguồn được chọn tại thời điểm đó.
3. Sử dụng "**Lịch sử tạm dừng"** và "**Lịch sử tiếp tục"** khi cần thiết. Sau khi khởi động lại, hãy tiếp tục một cách rõ ràng.
4. Kiểm tra kết quả theo từng nguồn và hàng đợi tệp đính kèm. Lưu báo cáo tiến độ đã được ký số cùng với tệp xuất bằng chứng.

Tính năng này sẽ hiển thị tất cả các tin nhắn hiện có trong không gian làm việc. Việc xuất dữ liệu theo từng cuộc trò chuyện dưới dạng HTML/JSON là một thao tác riêng biệt. [Chi tiết về lịch sử và khôi phục](https://phishdestroy.github.io/TgWitness/vi/docs/reference/history/).

## Tìm kiếm trước, sau đó quyết định về AI

1. Mở **"Ask the archive**". Chọn không gian làm việc, các cuộc trò chuyện và khoảng thời gian theo dõi.
2. Tìm kiếm một cụm từ, tên miền hoặc ID tin nhắn. Mở bản ghi phù hợp và các phiên bản đã lưu của nó.
3. Đối với phân tích bằng AI, quản trị viên trước tiên cần cấu hình nhà cung cấp. Kiểm tra **dữ liệu được gửi đến mô hình** và bỏ chọn các đoạn trích không mong muốn trước khi phê duyệt yêu cầu.
4. Kiểm tra các trích dẫn được trả về. Lưu câu trả lời dưới dạng báo cáo và thêm bản sửa đổi hoặc ghi chú của riêng bạn.

Tìm kiếm được thực hiện cục bộ mà không cần AI. Các báo cáo phân tích giữ lại các tham chiếu nguồn và lịch sử sửa đổi; chúng tách biệt với sổ nhật ký đã được ký điện tử. [Cài đặt nhà cung cấp và báo cáo](https://phishdestroy.github.io/TgWitness/vi/docs/reference/analysis/).

## Chọn kết nối phù hợp với nhu cầu của bạn

| Nhiệm vụ | Mở | Cài đặt |
| --- | --- | --- |
| Đọc các cuộc trò chuyện được chọn lọc từ một ứng dụng khách AI | **Tích hợp → MCP** | [Cài đặt tiện ích mở rộng MCP, tạo mã thông báo có phạm vi và kết nối ứng dụng khách](https://phishdestroy.github.io/TgWitness/vi/docs/reference/mcp/) |
| Nhận diện văn bản trong các tệp phương tiện đã lưu | Một bản ghi `media.saved` → **Nhận diện tệp đính kèm** | [Cài đặt máy chủ Docker cục bộ và các tệp ngôn ngữ/mô hình cần thiết](https://phishdestroy.github.io/TgWitness/vi/docs/reference/media-analysis/) |
| Gửi sự kiện đến n8n hoặc một hệ thống SIEM | **Tích hợp → Webhook đi** | [Thêm người nhận, xác minh HMAC và loại bỏ trùng lặp ID sự kiện](https://phishdestroy.github.io/TgWitness/vi/docs/reference/webhooks/) |

**Token truy cập nào được sử dụng ở đâu?**

Quyền truy cập vào bảng điều khiển dành cho những người xem xét vụ việc. Các kết nối MCP sẽ nhận được các mã thông báo lưu trữ riêng biệt chỉ dành cho đọc. Bộ thu webhook sử dụng khóa bí mật HMAC riêng của mình. Không ai cần tệp phiên Telegram.

[Chia sẻ quyền truy cập bảng điều khiển](https://phishdestroy.github.io/TgWitness/vi/docs/access/) hoặc [cấu hình máy khách MCP](https://phishdestroy.github.io/TgWitness/vi/docs/reference/mcp/).

## Cung cấp nguồn thông tin và kết luận

Hãy lưu giữ báo cáo phân tích đã được xem xét cùng với tệp ZIP bằng chứng đã được ký. Báo cáo giải thích cách bạn phân tích các nguồn thông tin; tệp ZIP cho phép người nhận đối chiếu bản ghi đã lưu với dấu vân tay và điểm kiểm tra đáng tin cậy độc lập.

[Xuất và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/exports/) · [Tiến hành một cuộc điều tra toàn diện](https://phishdestroy.github.io/TgWitness/vi/docs/cases/)
