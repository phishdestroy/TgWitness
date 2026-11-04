# Tìm hiểu nguyên nhân sự cố

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/troubleshooting/

Bắt đầu từ triệu chứng, kiểm tra từng thứ một.

## Ban tổ chức yêu cầu một mã xác thực

Nó cần token bảng điều khiển từ tệp mà trình khởi chạy đã in ra. Docker: `docker compose exec tgwitness cat /data/panel-token.txt`. Không phải mã Telegram, không phải token bot, không phải token nhân chứng.

## Telegram không kết nối

Chạy kiểm tra kết nối. Nếu dùng proxy công khai, hãy chọn cái khác và lưu. Kiểm tra loại proxy và định dạng khóa bí mật. Làm mới danh sách không tự đổi tuyến.

## Đang kết nối, nhưng không có tin nhắn mới

1. Quan sát có đang chạy, đúng không gian làm việc không?
2. Nguồn đã được chọn và tài khoản đó có thấy không?
3. Gửi một tin nhắn duy nhất trong nhóm thử nghiệm và tìm nó.
4. Tìm các lần gián đoạn hoặc lỗi Telegram trong sổ nhật ký.

Cuộc trò chuyện im ắng chỉ là không có gì mới. Nếu độ đầy đủ quan trọng, hãy chạy một phép thử nhận tin có kiểm soát.

## FloodWait hoặc khoảng trống sau khi khởi động lại

FloodWait là Telegram nói "chậm lại". Hãy chờ cho qua và giảm tải, kết nối lại không giúp được gì. Sau khi khởi động lại, TgWitness bắt kịp những gì Telegram vẫn còn giữ; phần còn lại là khoảng trống, nên hãy ghi lại.

## Bot đã được cấu hình nhưng chưa đăng tải bất kỳ nội dung nào

Nhân chứng có đang chạy không, bot có đăng được vào kênh không, nó có kết nối được tới máy thu thập và Bot API không? Tìm các bài đăng thất bại trong sổ nhật ký của nó. Có truy vấn ở phía máy thu thập không có nghĩa là bài đã được đăng.

## Tính năng tích hợp mã thông báo GitHub hiện nằm ở đâu?

**Đang trong giai đoạn lập kế hoạch.** Phần “Extras” mô tả quy trình làm việc được đề xuất cho việc phân nhánh (fork) và xác minh bản dựng. Hiện tại chưa có biểu mẫu mã thông báo GitHub hay cơ chế xác nhận tự động nào để đảm bảo rằng một bản cài đặt đang hoạt động khớp với kho lưu trữ. Vui lòng tham khảo [tình trạng tính năng hiện tại](https://phishdestroy.github.io/TgWitness/vi/docs/reference/features/).

Báo lỗi? Phiên bản, hệ điều hành, các bước và thông báo lỗi đã che thông tin riêng. Không bao giờ đưa phiên, token, tin nhắn riêng tư hay thư mục dữ liệu vào issue công khai.
