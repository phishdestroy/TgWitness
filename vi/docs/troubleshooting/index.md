# Tìm hiểu nguyên nhân sự cố

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/troubleshooting/

Hãy bắt đầu từ triệu chứng. Kiểm tra từng lớp một.

## Ban tổ chức yêu cầu một mã xác thực

Vui lòng sử dụng mã thông báo bảng điều khiển từ tệp cục bộ được trình khởi chạy hiển thị. Đối với Docker, hãy chạy lệnh ``docker compose exec tgwitness cat /data/panel-token.txt``. Mã đăng nhập Telegram, mã thông báo BotFather và mã thông báo chứng kiến chỉ đọc phục vụ các mục đích khác nhau.

## Telegram không kết nối

Mở cài đặt kết nối và thực hiện kiểm tra kết nối. Nếu sử dụng proxy công cộng, hãy thử một mục khác và lưu đường dẫn một cách rõ ràng. Kiểm tra loại proxy và định dạng khóa bí mật được hỗ trợ. Việc làm mới danh sách công cộng sẽ không thay đổi đường dẫn của tài khoản.

## Đang kết nối, nhưng không có tin nhắn mới

1. Vui lòng kiểm tra xem quá trình quan sát có đang chạy trong không gian làm việc đúng hay không.
2. Xác nhận rằng nguồn đã được chọn và hiển thị đối với tài khoản đó.
3. Hãy gửi một tin nhắn mới duy nhất trong một nhóm được kiểm soát và tìm kiếm chính xác đoạn văn bản đó.
4. Vui lòng rà soát nhật ký hoạt động để phát hiện các sự cố gián đoạn, tình trạng chậm trễ trong quá trình xử lý hoặc các lỗi phát sinh từ Telegram.

Các bản chụp lịch sử và các sự kiện tin nhắn mới là hai khái niệm khác nhau. Một nguồn im lặng có thể được kết nối mà không tạo ra tin nhắn mới. Hãy sử dụng thử nghiệm gửi tin nhắn có kiểm soát khi tính đầy đủ là yếu tố quan trọng.

## FloodWait hoặc khoảng trống sau khi khởi động lại

FloodWait có nghĩa là Telegram yêu cầu tạm dừng. Vui lòng chờ trong khoảng thời gian được chỉ định và rà soát khối lượng công việc thu thập; việc kết nối lại nhiều lần sẽ không loại bỏ giới hạn này. Trạng thái cập nhật đã lưu giúp khôi phục tiến độ sau khi khởi động lại, tuy nhiên các bản cập nhật đã hết hạn và một số khoảng thời gian gián đoạn vẫn là những hạn chế. Hãy ghi lại khoảng trống thay vì coi nhật ký là hoàn chỉnh.

## Bot đã được cấu hình nhưng chưa đăng tải bất kỳ nội dung nào

Hãy đảm bảo rằng quy trình Witness đang thực sự hoạt động, bot có thể đăng bài trong kênh và Witness có thể kết nối với bộ thu thập dữ liệu cũng như Bot API. Kiểm tra nhật ký của hệ thống để phát hiện các trường hợp đăng tải không thành công. Việc bộ thu thập dữ liệu thực hiện thăm dò thành công không tự động xác nhận rằng bài đăng trên kênh đã được thực hiện.

## Tính năng tích hợp mã thông báo GitHub hiện nằm ở đâu?

**Đang trong giai đoạn lập kế hoạch.** Phần “Extras” mô tả quy trình làm việc được đề xuất cho việc phân nhánh (fork) và xác minh bản dựng. Hiện tại chưa có biểu mẫu mã thông báo GitHub hay cơ chế xác nhận tự động nào để đảm bảo rằng một bản cài đặt đang hoạt động khớp với kho lưu trữ. Vui lòng tham khảo [tình trạng tính năng hiện tại](https://phishdestroy.github.io/TgWitness/vi/docs/reference/features/).

Khi báo cáo sự cố, vui lòng cung cấp thông tin về phiên bản, hệ điều hành, các bước thực hiện và nội dung lỗi đã được che bớt. Xin vui lòng không công khai thông tin về phiên làm việc, mã thông báo, tin nhắn riêng tư và thư mục dữ liệu trong các vấn đề công khai.
