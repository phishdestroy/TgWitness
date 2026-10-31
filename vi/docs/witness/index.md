# Thiết lập bot chứng cứ

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/witness/

Hãy để một quy trình riêng biệt kiểm tra nhật ký này và đăng các mốc kiểm tra đã được ký lên kênh của quý vị.

## Hai máy chủ, hai khóa ký

TỰ LẮP ĐẶT / THIẾT BỊ THU THẬP**Tài khoản + sổ ghi chép**

Khóa ký của Trình thu thập phiên Telegram

Điểm cuối kiểm tra chỉ đọc

← yêu cầu câu trả lời có chữ ký →

HOST B / WITNESS**Xác minh + lưu trữ**

Dấu vân tay bộ thu được ghim sẵn; Khóa ký chứng thực riêng biệt

Sổ nhật ký riêng + mã thông báo bot

Witness → API Bot Telegram →**Kênh của quý vị · các bài đăng TGW1 đã được ký điện tử**

Công cụ TgWitness tự động thực hiện việc kiểm tra. Quyền truy cập của bộ thu thập chỉ giới hạn ở chế độ đọc. Việc đăng tải của bot sử dụng kết nối và mã thông báo của TgWitness; TgWitness không được cấp bất kỳ phiên tài khoản nào.

03 / CÁC QUYẾT ĐỊNH TẠI ĐIỂM KIỂM TRACác câu trả lời minh họa

BẢN CUỐI CÙNG ĐƯỢC CHẤP NHẬN**120 bản ghi**`head 9c7d…`

CÂU TRẢ LỜI TIẾP THEO**128 bản ghi**`head a4f2…`

Đã được chấp nhận: số lượng tăng lên, chữ ký đã được xác minh và khóa khớp. TgWitness duy trì ranh giới mới này.

Tất cả các ví dụ trả lời đều giả định có chữ ký hợp lệ và khóa được ghim. Các giá trị băm ở đây chỉ là minh họa tóm tắt. Chỉ riêng số lượng lớn hơn không thể chứng minh rằng toàn bộ tiền tố cũ vẫn không thay đổi; hãy so sánh bản xuất với các điểm kiểm tra được lưu giữ.

## Chuẩn bị một bot và một kênh

Hãy tạo một bot bằng BotFather và cho phép bot này đăng bài trong một kênh do quý vị quản lý. Chọn một máy tính hoặc máy chủ làm máy chủ lưu trữ cho công cụ này. Việc sử dụng máy chủ và người vận hành riêng biệt sẽ mang lại sự độc lập cao hơn so với việc chạy một tiến trình thứ hai trên máy chủ của người thu thập dữ liệu.

## Ba bước trong phần Tiện ích bổ sung

1. **Quyền truy cập chỉ đọc.** Mở **phần “Extras” →**Tạo**một bot trong kênh của quý vị**, tạo mã thông báo chứng thực (witness token) và lưu tệp truy cập. Tính năng này cho phép đọc các điểm kiểm tra (checkpoints) và trạng thái hoạt động (health), chứ không bao gồm các cuộc trò chuyện hay các thiết lập điều khiển của trình thu thập dữ liệu.
2. **Kênh và khoảng thời gian.** Vui lòng nhập tên kênh và địa chỉ máy thu dữ liệu mà TgWitness có thể truy cập được. Lưu tệp cài đặt.
3. **Khởi chạy.** Đặt các tệp `witness.json`, `witness-token.txt` và `bot-token.txt` đã được tạo trên máy chủ chứng thực vào cùng một thư mục. Vui lòng thực thi các lệnh dưới đây trong môi trường dự án đã cài đặt.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Việc tải xuống các tệp tin sẽ không khởi động công cụ TgWitness. Vui lòng kiểm tra xem bài đăng có chữ ký đầu tiên đã xuất hiện trong kênh hay chưa, sau đó lưu lại dấu vân tay khóa công khai của công cụ TgWitness một cách riêng biệt.

## Chọn tần suất đăng tải

Việc xuất bản mỗi lần kiểm tra sẽ tạo ra một bản ghi bên ngoài định kỳ. Với khoảng thời gian 5 phút một lần, điều này tương đương khoảng 288 bài đăng cho mỗi không gian làm việc mỗi ngày. Các cài đặt nâng cao còn cho phép xuất bản khi có thay đổi hoặc sự cố, sử dụng máy chủ proxy và địa chỉ API Bot tùy chỉnh.

**Thực tế, bot này xác nhận điều gì?**

TgWitness yêu cầu người thu thập cung cấp một điểm kiểm tra đã được ký, xác minh điểm kiểm tra đó dựa trên khóa dự kiến và lưu giữ một sổ nhật ký riêng biệt đã được ký. Công cụ này ghi lại các phản hồi bị thiếu và các câu trả lời bị từ chối cũng như các lần kiểm tra thành công. Việc công bố vẫn phụ thuộc vào việc TgWitness đang hoạt động và có thể kết nối với Bot API của Telegram.

Công cụ này kiểm tra trạng thái nhật ký được báo cáo bởi bộ thu thập dữ liệu. Công cụ này không tự động theo dõi từng tin nhắn Telegram. Để thực hiện việc đó, quý vị cần thêm tính năng kiểm tra việc gửi tin nhắn có kiểm soát.

## Xin vui lòng kiểm tra bằng chứng sau này

Hãy lưu giữ sổ nhật ký chứng cứ, các bài đăng trên kênh và các dấu vân tay được lưu trữ độc lập. [Quy trình xác minh đầy đủ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/#verify) sẽ so sánh các dữ liệu này với tệp xuất có chữ ký của người thu thập.
