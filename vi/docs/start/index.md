# Bắt đầu chỉ trong vài phút

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/start/

Trước tiên, quý vị hãy tham khảo một ví dụ minh họa. Sau đó, hãy kết nối tài khoản của riêng quý vị.

## Quý vị có thể tham quan trang web mà không cần tài khoản

Quý vị vui lòng tải xuống hoặc sao chép dự án, cài đặt **Python 3.11 trở lên**, sau đó chạy bản demo. Trình khởi chạy sẽ tạo môi trường cục bộ và cài đặt các phụ thuộc được ghim sẵn.

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

Trình duyệt sẽ mở ra một không gian làm việc với các tin nhắn giả định. Quý vị có thể mở một cuộc trò chuyện, so sánh các thay đổi và kiểm tra tệp xuất. Chế độ demo không kết nối với Telegram.

![Giao diện cuộc trò chuyện của TgWitness kèm các tin nhắn mẫu](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Một không gian làm việc mẫu. Nhật ký của riêng quý vị sẽ được bắt đầu riêng biệt.

## Bắt đầu không gian làm việc của riêng quý vị

Vui lòng kết thúc quy trình trình diễn, sau đó sử dụng trình khởi chạy thông thường:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Vui lòng mở địa chỉ cục bộ được trình khởi chạy hiển thị. Nếu được yêu cầu, hãy nhập **mã thông báo truy cập bảng điều khiển** từ tệp cục bộ có tên được hiển thị trong cửa sổ terminal. Thao tác này sẽ kích hoạt TgWitness; quá trình này hoàn toàn độc lập với việc đăng nhập vào Telegram.

## Ghi lại tin nhắn đầu tiên của quý vị

1. [Kết nối một tài khoản Telegram chuyên dụng.](https://phishdestroy.github.io/TgWitness/vi/docs/accounts/)
2. Vui lòng chọn một nhóm hoặc kênh mà tài khoản có quyền truy cập, sau đó bắt đầu quá trình theo dõi.
3. Hãy gửi một tin nhắn mới vào một nhóm thử nghiệm do quý vị quản lý và kiểm tra xem tin nhắn đó có xuất hiện trong sổ nhật ký hay không.

Để cài đặt trên máy chủ, vui lòng làm theo hướng dẫn tại [Keep it running](https://phishdestroy.github.io/TgWitness/vi/docs/server/).
