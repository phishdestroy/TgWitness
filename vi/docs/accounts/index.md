# Kết nối tài khoản

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/accounts/

Mỗi không gian làm việc chứa một tài khoản, sổ nhật ký của tài khoản đó và khóa ký của tài khoản đó.

## Chọn cách đăng nhập

Mở **Tài khoản**, thêm không gian làm việc và mở cài đặt kết nối của không gian đó. Hãy sử dụng một tài khoản chuyên dụng dành cho việc quan sát.

- **Mã QR: quý vị** hãy quét mã này từ phần cài đặt thiết bị trên Telegram và xác nhận thông tin đăng nhập mới.
- **Số điện thoại:** vui lòng nhập số điện thoại, mã xác minh mà Telegram gửi đến và mật khẩu xác thực hai bước (nếu tính năng này đã được kích hoạt).
- **Nhập phiên làm việc:** nhập một phiên làm việc được hỗ trợ hoặc dữ liệu Telegram Desktop thuộc sở hữu của quý vị.

Quý vị có thể chọn một cấu hình API có sẵn hoặc nhập ID API và mã băm của riêng mình. Cấu hình API dùng để xác định danh tính của khách hàng; nó không dùng để đăng nhập vào tài khoản hay làm cho kết nối trở nên ẩn danh.

**Quý vị có cần sử dụng máy chủ proxy trước không?**

Quý vị có thể [lựa chọn và kiểm tra lộ trình kết nối](https://phishdestroy.github.io/TgWitness/vi/docs/proxies/) trước khi đăng nhập. Mỗi tài khoản đều có lộ trình riêng.

## Chọn nội dung cần theo dõi

1. Vui lòng mở danh sách nguồn và chọn các cuộc trò chuyện, nhóm hoặc kênh mà quý vị cần.
2. Vui lòng kiểm tra các cài đặt thu thập dữ liệu, bao gồm cả tệp đa phương tiện, trước khi bắt đầu quá trình quan sát.
3. Khởi động trình thu thập dữ liệu và kiểm tra kết nối cũng như các hoạt động gần đây của nó.

Tài khoản phải có quyền truy cập vào nguồn dữ liệu. Các vai trò khác nhau có thể xem các sự kiện khác nhau; sổ nhật ký phản ánh chính xác những gì tài khoản đó đã nhận được.

Đối với một vụ việc liên quan đến toàn bộ tài khoản, vui lòng chọn **Nguồn → Phạm vi quan sát → Chế độ điều tra**, xem lại các cài đặt và nhấn **Lưu phạm vi**. [Hướng dẫn điều tra chi tiết](https://phishdestroy.github.io/TgWitness/vi/docs/cases/) bao quát tất cả các loại cuộc trò chuyện hiển thị, lịch sử cũ, hồ sơ cá nhân, các tham chiếu chéo giữa các cuộc trò chuyện và việc chuyển giao bằng chứng.

## Kiểm tra toàn bộ đường dẫn

Trong một nhóm thử nghiệm do quý vị quản lý, hãy gửi một tin nhắn duy nhất từ một tài khoản khác, chỉnh sửa và xóa tin nhắn đó. Xác nhận cả ba sự kiện trong sổ ghi chép, sau đó [xuất và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/exports/) bản ghi.

Trạng thái “Đã kết nối” xác nhận rằng kết nối đã được thiết lập. Một tin nhắn thử nghiệm được ghi lại xác nhận rằng một sự kiện cụ thể đã được truyền đến không gian làm việc này.

## Thêm một tài khoản khác

Vui lòng tạo một không gian làm việc khác trong **phần Tài khoản** và lặp lại quy trình thiết lập. Hãy lưu giữ dấu vân tay khóa ký của từng tài khoản để quý vị có thể nhận diện các tệp xuất từ tài khoản đó sau này.
