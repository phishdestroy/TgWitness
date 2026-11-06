# Trò chuyện bí mật: triển khai và demo

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/secret-chats/

Hiểu rõ cơ chế triển khai của Trò chuyện bí mật, thử nghiệm giao diện giả định và xem xét các lỗi chưa được khắc phục.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

**Tình trạng được kiểm tra vào ngày 6 tháng 11 năm 2026:** hiện đang có một triển khai riêng biệt cho Secret Chat đang được phát triển. Nó chưa được hợp nhất vào nhánh `main` đã công bố tại `3d23e52b647b`. Trình thu thập thông thường và tính năng xuất Takeout không thu thập dữ liệu từ Secret Chat. Kịch bản trang web tương tác minh họa giao diện bằng dữ liệu giả định; nó không hỗ trợ giao tiếp qua Telegram.

## Vị trí triển khai

Commit `0e60f88e` đã thêm **Sources → Pseudo-secret** vào nhánh phát triển cục bộ `fix/panel-routes-sessions`. Bản chụp nhanh đã được kiểm tra là `bb8788fb685c`. Việc triển khai bao gồm `tgwitness/secret_chats.py`, các tuyến ứng dụng, `tgwitness/static/views/secret-chats.js` và các bài kiểm thử chuyên dụng.

Tính năng bổ sung tùy chọn `secret-chats` trong nhánh đó sử dụng [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat), được ghim vào `d87bf037b90060383c7b704d8a06ebb98c621c6f`. Thư viện này triển khai giao thức trò chuyện đầu cuối của Telegram trên cơ sở ủy quyền Telethon hiện có của tài khoản. Việc cài đặt riêng thư viện này sẽ không bổ sung tính năng tích hợp còn thiếu vào `main`.

## Chức năng của giao diện phát triển

| Hành động | Hành vi đã ghi lại |
| --- | --- |
| Bắt đầu cuộc trò chuyện bằng tên người dùng hoặc ID người dùng | Gửi yêu cầu; người tham gia còn lại phải chấp nhận yêu cầu đó. |
| Chấp nhận yêu cầu đến | TgWitness sẽ trở thành điểm cuối nhận tin nhắn cho cuộc trò chuyện đó. Tính năng chấp nhận tự động là một cài đặt riêng biệt, mặc định là tắt. |
| Gửi hoặc nhận tin nhắn | Thêm một bản ghi `secret_chat.message` đi hoặc đến và hiển thị nó trong chuỗi trò chuyện. |
| Nhận tệp đính kèm | Giải mã nó, lưu trữ các byte theo SHA-256 và ghi lại `secret_chat.file`. |
| Nhận thông báo về thời gian đếm ngược hoặc thông báo xóa | Ghi lại thông báo và lưu giữ nội dung đã thu thập trước đó. |
| Xem lại cuộc trò chuyện | Hiển thị tin nhắn, tệp tin, thông báo và biểu đồ trực quan hóa khóa. Tab đang mở sẽ tự động làm mới sau mỗi bốn giây. |

Trong bản dựng phát triển có tích hợp tính năng này, người vận hành kích hoạt mô-đun cho tài khoản đã chọn và kết nối nó. Việc khởi động, chấp nhận và gửi yêu cầu phải có quyền tương tác và chế độ bảo vệ chỉ đọc của tài khoản phải được tắt. Người tham gia còn lại phải chấp nhận một cuộc trò chuyện mới được gửi đi. Các điều kiện này không có trong ứng dụng đã phát hành ở phiên bản trên.

Chỉ các cuộc trò chuyện được tạo hoặc chấp nhận bởi phiên TgWitness này mới được bao gồm. Các cuộc trò chuyện bí mật hiện có trên điện thoại vẫn được lưu giữ trên thiết bị đó. Việc nhập phiên không cung cấp các khóa mã hóa riêng biệt của chúng. Dữ liệu khóa và bộ đếm của cuộc trò chuyện bí mật được lưu trữ trong kho lưu trữ không gian làm việc; các tin nhắn được lưu giữ và tệp đã giải mã tuân theo các biện pháp bảo vệ lưu trữ thông thường của không gian làm việc.

## Trang web demo

Kịch bản “**Try Secret Chat**” trên trang web mở ra một cuộc trò chuyện hư cấu. Nó cho phép người đọc bắt đầu một yêu cầu, mô phỏng việc chấp nhận yêu cầu đó, gửi một tin nhắn mẫu, nhận phản hồi và tệp tin theo kịch bản, đồng thời kiểm tra bộ đếm thời gian và thông báo xóa. Một yêu cầu đến cũng có thể được chấp nhận. Các điều khiển ghi rõ các hành động được mô phỏng của đối tác.

Kịch bản này chạy trong bộ nhớ trình duyệt. Việc đặt lại hoặc tải lại sẽ xóa nó. Kịch bản này không đăng nhập, liên hệ với Telegram, tạo khóa mã hóa thực tế hoặc thay đổi các bản tải xuống mẫu đã ký. Các thông điệp được hiển thị không phải là bằng chứng đã ký. Kịch bản này minh họa cách tương tác dự kiến; nó không chứng nhận rằng bản triển khai phát triển đã sẵn sàng.

## Các kiểm tra và lỗi chưa được khắc phục

Năm bài kiểm tra hiện có bao gồm tính bền vững của khóa mã hóa, vòng đời và bản ghi tin nhắn, chính sách chấp nhận tin nhắn đến, gửi chỉ đọc và xuất tệp đính kèm. Các bài kiểm tra này đã vượt qua khi chạy trên thư viện được cố định trong đợt đánh giá ngày 6 tháng 11. Ba bài kiểm tra tổng hợp bổ sung đã tái hiện các lỗi trong cùng bản chụp nhanh:

| Kết quả | Hậu quả |
| --- | --- |
| Việc đóng lại sẽ bỏ qua lỗi `read_only` | Đường dẫn đóng có thể thực hiện một hành động từ xa khi các tương tác cần bị chặn. |
| Tính năng phát hiện trùng lặp chỉ tìm kiếm trong các bản ghi gần đây của 500 | Một bản phát lại cũ có thể tạo ra bản sao trùng lặp sau khi khởi động lại. |
| Việc tải xuống tệp đính kèm không thành công sẽ xóa mục đang chờ xử lý của tệp đó | Một lỗi tạm thời sẽ làm mất tác vụ thử lại. |

Đây là các lỗi chưa được khắc phục, cũng được ghi nhận trong báo cáo kiểm toán [đã công bố](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md). Năm bài kiểm tra đạt yêu cầu không bao gồm các lỗi này. Quá trình đánh giá đã sử dụng các không gian làm việc tổng hợp và mô phỏng các hoạt động của Telegram; nó không lặp lại quá trình thiết lập kết nối thực tế hoặc xác nhận triển khai trên môi trường sản xuất.
