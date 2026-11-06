# Telegram · Xuất và xác minh

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/exports/

Trao cho người khác những tệp họ có thể tự đối chiếu với không gian làm việc của bạn.

Giữ lại tham chiếuXuất tệp ZIP đã được ký điện tửNgười nhận xác minh

Mới làm quen với chữ ký và điểm kiểm tra? [Thay đổi một bản ghi mẫu](https://phishdestroy.github.io/TgWitness/vi/docs/concepts/#chain) và xem bước kiểm tra nào phát hiện ra.

Muốn lưu giữ một bản sao ngoài phạm vi của người thu thập dữ liệu? Vui lòng truy cập [phần Cài đặt S3](https://phishdestroy.github.io/TgWitness/vi/docs/exports/#s3), [tính năng Khóa đối tượng](https://phishdestroy.github.io/TgWitness/vi/docs/exports/#s3-retention) hoặc [tính năng khôi phục đã được xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/exports/#s3-restore).

## Lưu giữ một nguồn tham khảo đáng tin cậy

Ghi dấu vân tay khóa của không gian làm việc ở đâu đó ngoài máy thu thập. Trong khi thu thập, cũng hãy lưu điểm kiểm tra có chữ ký ở nơi khác, hoặc chạy một [nhân chứng độc lập](https://phishdestroy.github.io/TgWitness/vi/docs/witness/). Đó là thứ người nhận dùng để kiểm tra khóa và trạng thái trước đó của sổ nhật ký.

## Tải xuống tệp ZIP đã được ký số

**Xuất** → ZIP bằng chứng có chữ ký. Bên trong có toàn bộ sổ nhật ký và bản kê tệp có chữ ký. Định hình báo cáo dễ đọc trong [Report studio](https://phishdestroy.github.io/TgWitness/vi/docs/reports/), hoặc chỉ gửi dữ liệu đã chọn dưới dạng [bản trích xuất bàn giao](https://phishdestroy.github.io/TgWitness/vi/docs/handover/).

Báo cáo HTML, PDF và JSON có dấu niêm phong riêng. CSV chỉ là bản sao làm việc; để đảm bảo toàn vẹn, hãy dùng CSV bên trong ZIP đã xác minh.

## Vui lòng xác minh bằng một bản sao đáng tin cậy của TgWitness

Trong môi trường của dự án, với dấu vân tay và đường dẫn của bạn:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Khi đạt, bạn thấy `key_pinned: true` và `checkpoint_checked: true`. Giữ kết quả đó cạnh kho lưu trữ. Điểm kiểm tra phải nằm ở cuối bản xuất hoặc trước đó.

## Sử dụng kết quả xác minh

- **Tệp:** bản kê ràng buộc mã băm của chúng, chữ ký ràng buộc sổ nhật ký. Mọi thay đổi đều lộ ra.
- **Danh tính:** dấu vân tay bạn đã giữ chứng minh đó là khóa bạn mong đợi.
- **Trạng thái trước đó:** điểm kiểm tra so sánh bản xuất với phần đầu sổ nhật ký đã lưu trước khi bàn giao.
- **Phạm vi:** khoảng trống, kết quả thu nhận và phép thử gửi → sửa → xóa cho thấy cấu hình này thực sự bắt được gì.

Chi tiết: [xác minh chứng minh được gì và không chứng minh được gì](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope).

## Thiết lập bản sao lưu ngoài trang web trên S3

**Xuất → Bản sao ngoài trang web** trong không gian làm việc của bạn. Hoạt động với AWS S3 và mọi dịch vụ tương thích S3. Nó sao chép các đoạn sổ nhật ký, tệp đã lưu, điểm kiểm tra kèm dấu thời gian và bản xuất trò chuyện đã hoàn tất, mỗi thứ được mã hóa bằng `AES-256-GCM` trước khi rời máy thu thập.

Bản demo trực tuyến hiển thị các điều khiển này nhưng tắt tải lên. Chỉ nhập thông tin xác thực thật trong bản cài đặt của riêng bạn.

[![Bảng điều khiển sao lưu ngoài trang web đầy đủ: điểm cuối, khu vực, thùng lưu trữ, khóa truy cập, lịch trình, các thiết lập kiểm soát Object Lock và khóa khôi phục](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Bảng điều khiển đầy đủ với các tùy chọn nâng cao đã được mở rộng. Không hiển thị bất kỳ thông tin đăng nhập lưu trữ nào.

| Lĩnh vực | Nội dung cần nhập |
| --- | --- |
| Điểm cuối | URL lưu trữ, không kèm đường dẫn bucket hay thông tin xác thực. Ví dụ: `https://s3.example.invalid`. |
| Khu vực | Theo yêu cầu của nhà cung cấp. Mặc định `us-east-1`. |
| Bucket | Một bucket có sẵn mà bạn ghi được. Ví dụ: `example-case-backup`. |
| Thư mục trong bucket | Tiền tố, mặc định `tgwitness`. Một tiền tố riêng cho mỗi không gian làm việc được thêm vào phía sau. |
| ID khóa truy cập / Khóa truy cập bí mật | Cả hai cùng nhau, lưu trong kho bảo mật. Sau này để trống cả hai thì giá trị cũ được giữ. |
| Địa chỉ theo kiểu đường dẫn | Bật: `endpoint/bucket`. Tắt: `bucket.endpoint`. Tùy nhà cung cấp. |
| Khoảng thời gian sao chép | 1 đến 1.440 phút, mặc định 5. Chỉ khi ứng dụng đang chạy. |
| Chính sách lưu trữ Object Lock | Số ngày và chế độ, nếu bucket hỗ trợ Object Lock. Số 0 giữ mặc định của bucket. |

1. Tạo bucket, điền đích đến và thông tin xác thực trong khi **Giữ bản sao ngoài trang web** chưa được chọn, rồi bấm **Lưu bản sao ngoài trang web**.
2. **Kiểm tra kết nối** tải lên một đối tượng thử đã mã hóa.
3. **Tải xuống khóa mã hóa** và cất xa máy thu thập. Không có khóa thì không khôi phục được.
4. Chọn **Giữ bản sao ngoài trang web**, lưu, rồi **Sao chép ngay** hoặc để lịch chạy.

## Kiểm tra tiến độ lưu trữ và sao chép

Trong **Tùy chọn khác**, chọn số ngày lưu giữ và `GOVERNANCE` hoặc `COMPLIANCE`. TgWitness đọc lại cài đặt lưu giữ từ một đối tượng đã tải lên và báo cho bạn: đã xác nhận, thiếu hoặc kiểm tra thất bại.

Bảng điều khiển hiển thị lượt chạy gần nhất, số đối tượng, số byte, ranh giới sổ nhật ký đã sao chép và lỗi. Tệp cục bộ bị thiếu sẽ được báo và thử lại ở lượt sau, phần còn lại vẫn tiếp tục sao chép.

Tải lên đi qua kết nối trực tiếp, SOCKS5 hoặc HTTP. Với tuyến chỉ có MTProxy, bản sao sẽ chờ kèm lỗi.

## Hãy lưu giữ khóa khôi phục ở một nơi riêng biệt

Tệp JSON khóa chứa khóa giải mã, đích đến, tiền tố và dấu vân tay khóa. Để khôi phục, bạn cần nó cùng thông tin xác thực lưu trữ có quyền đọc.

Đã đổi endpoint, bucket hoặc tiền tố? Hãy tải lại khóa. Một bản sao mới bắt đầu ở đích mới; các bản xuất trò chuyện cũ vẫn ở chỗ cũ.

## Khôi phục và xác minh trên một máy tính khác

Bạn cần một bản cài TgWitness đáng tin cậy, tệp JSON khóa, thông tin xác thực lưu trữ chỉ đọc và một thư mục trống:

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

Mọi thứ được kiểm tra trước trong một thư mục tạm riêng tư: toàn bộ sổ nhật ký, điểm kiểm tra, mã băm và kích thước tệp. Đường dẫn không an toàn, các đoạn mâu thuẫn hoặc sổ nhật ký ngắn hơn điểm kiểm tra của nó sẽ thất bại, và khi đó không có gì được ghi ra.

Khi thành công, bạn nhận được `events.jsonl`, `media/`, `checkpoints/` và `exports/`. Giữ kết quả JSON của lệnh cùng chúng, và so sánh với các điểm kiểm tra hoặc bản ghi nhân chứng bạn tự lưu.
