# Thiết lập bot chứng cứ

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/witness/

Một tiến trình riêng kiểm tra sổ nhật ký của bạn và đăng các điểm kiểm tra có chữ ký lên một kênh.

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

Tạo một bot bằng BotFather và cho phép nó đăng bài trong kênh của bạn. Hãy chạy nhân chứng ở nơi khác: một máy chủ khác, lý tưởng là do người khác vận hành, giá trị hơn nhiều so với một tiến trình thứ hai cạnh máy thu thập.

## Ba bước trong phần Tiện ích bổ sung

1. **Quyền chỉ đọc.** **Tiện ích → Nhân chứng độc lập**, tạo token, lưu tệp. Nó đọc điểm kiểm tra và tình trạng, không gì khác.
2. **Kênh và khoảng thời gian.** Kênh Telegram hoặc webhook Discord, cùng địa chỉ máy thu thập mà nhân chứng truy cập được. Lưu tệp cài đặt.
3. **Khởi chạy.** Đặt `witness.json`, `witness-token.txt` và `bot-token.txt` cùng nhau trên máy chủ nhân chứng và chạy:

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Chờ bài đăng có chữ ký đầu tiên trong kênh, rồi lưu dấu vân tay của nhân chứng ở nơi an toàn.

Muốn dùng Discord? Lưu URL webhook thành `discord-webhook.txt`. Một nhân chứng đăng vào một nơi; các lần kiểm tra dài đến Discord dưới dạng tệp.

## Chọn tần suất đăng tải

Đăng mỗi lần kiểm tra tạo ra một bản ghi bên ngoài đều đặn: cứ năm phút một lần là khoảng 288 bài mỗi ngày cho mỗi không gian làm việc. Cài đặt nâng cao có thể chỉ đăng khi có thay đổi hoặc sự cố, dùng proxy hoặc Bot API tùy chỉnh.

**Thực tế, bot này xác nhận điều gì?**

Nó yêu cầu máy thu thập cung cấp điểm kiểm tra có chữ ký, kiểm tra bằng khóa mong đợi và giữ sổ nhật ký có chữ ký riêng, kể cả các phản hồi bị lỡ và bị từ chối.

Nó kiểm tra trạng thái sổ nhật ký, bản thân nó không theo dõi Telegram. Để làm việc đó, hãy chạy một phép thử nhận tin có kiểm soát.

## Xin vui lòng kiểm tra bằng chứng sau này

Giữ sổ nhật ký của nhân chứng, các bài đăng và dấu vân tay. [Cách đối chiếu chúng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/#verify) với bản xuất của máy thu thập.
