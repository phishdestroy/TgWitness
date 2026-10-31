# Xuất và xác minh

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/exports/

Chia sẻ bản ghi có chữ ký để người khác có thể kiểm tra.

Giữ lại tham chiếuXuất tệp ZIP đã được ký điện tửNgười nhận xác minh

Quý vị mới làm quen với các chữ ký và điểm kiểm tra? Hãy [thử thay đổi một bản ghi mẫu](https://phishdestroy.github.io/TgWitness/vi/docs/concepts/#chain) và xem các kiểm tra nào sẽ phát hiện ra sự thay đổi đó.

Muốn lưu giữ một bản sao ngoài phạm vi của người thu thập dữ liệu? Vui lòng truy cập [phần Cài đặt S3](https://phishdestroy.github.io/TgWitness/vi/docs/exports/#s3), [tính năng Khóa đối tượng](https://phishdestroy.github.io/TgWitness/vi/docs/exports/#s3-retention) hoặc [tính năng khôi phục đã được xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/exports/#s3-restore).

## Lưu giữ một nguồn tham khảo đáng tin cậy

Vui lòng lưu dấu vân tay khóa công khai của không gian làm việc bên ngoài bộ thu thập dữ liệu. Trong quá trình thu thập, hãy lưu trữ các điểm kiểm tra đã được ký kết tại một vị trí khác hoặc sử dụng một [bên chứng kiến độc lập](https://phishdestroy.github.io/TgWitness/vi/docs/witness/). Các tham chiếu này cho phép người nhận kiểm tra khóa cũng như ranh giới của sổ nhật ký trước đó.

## Tải xuống tệp ZIP đã được ký số

Nhấp vào **“Xuất”** và tạo tệp ZIP bằng chứng đã được ký. Tệp này bao gồm nhật ký không gian làm việc và bản kê khai tệp đã được ký. Các bộ lọc trên bảng điều khiển không giới hạn việc xuất toàn bộ nhật ký này: vui lòng xem xét kỹ nội dung trước khi chia sẻ.

Các tệp HTML và CSV có thể tải xuống độc lập rất hữu ích cho việc đọc và phân tích. Quý vị nên giữ tệp ZIP đã được ký làm bản gốc có thể xác minh; các tệp HTML hoặc CSV riêng lẻ không có chữ ký độc lập.

## Vui lòng xác minh bằng một bản sao đáng tin cậy của TgWitness

Trong môi trường dự án đã cài đặt, vui lòng thay thế dấu vân tay và đường dẫn tệp trong ví dụ:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Khi cả hai tham chiếu đều hợp lệ, kết quả sẽ báo cáo `key_pinned: true` và `checkpoint_checked: true`. Vui lòng lưu giữ kết quả xác minh cùng với tệp lưu trữ gốc. Điểm kiểm tra được lưu giữ phải nằm tại hoặc trước ranh giới của tệp xuất.

## Hiểu rõ kết quả

- **Tính toàn vẹn:** lịch sử được ghi lại và các tệp đã xuất ra khớp với chữ ký của chúng.
- **Lưu ý trước đó:** điểm kiểm tra bên ngoài cho phép quý vị so sánh tệp xuất với tiền tố nhật ký đã được lưu giữ trước đó.
- **Quy trình thực hiện:** Một thử nghiệm có kiểm soát về các thao tác “gửi → chỉnh sửa → xóa” sẽ đối chiếu các sự kiện cụ thể với bản ghi đã thu thập được.

Một chữ ký hợp lệ không chứng minh rằng mọi sự kiện trên Telegram đều đã được gửi đến, rằng nguồn tin đã nói sự thật hay rằng đồng hồ của người thu thập dữ liệu là chính xác.

## Thiết lập bản sao lưu ngoài trang web trên S3

Trong không gian làm việc hiện tại của quý vị, hãy mở **mục Xuất → Bản sao ngoài trang web**. Tính năng tùy chọn này tương thích với AWS S3 và các dịch vụ tương thích S3 khác. Tính năng này sao chép các phân đoạn nhật ký, ảnh và tệp tin được lưu giữ, các điểm kiểm tra kèm theo phản hồi dấu thời gian, cũng như các bản xuất cuộc trò chuyện đã hoàn tất. Mọi đối tượng đều được mã hóa trên bộ thu thập bằng thuật toán `AES-256-GCM` trước khi tải lên.

Bản demo trực tuyến hiển thị các chức năng điều khiển tương tự nhưng tính năng tải lên đã bị vô hiệu hóa. Quý vị chỉ nên nhập thông tin đăng nhập lưu trữ trong không gian làm việc đang hoạt động của riêng mình.

[![Bảng điều khiển sao lưu ngoài trang web đầy đủ: điểm cuối, khu vực, thùng lưu trữ, khóa truy cập, lịch trình, các thiết lập kiểm soát Object Lock và khóa khôi phục](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Bảng điều khiển đầy đủ với các tùy chọn nâng cao đã được mở rộng. Không hiển thị bất kỳ thông tin đăng nhập lưu trữ nào.

| Lĩnh vực | Nội dung cần nhập |
| --- | --- |
| Điểm cuối | URL của dịch vụ lưu trữ, không bao gồm đường dẫn đến bucket hoặc thông tin đăng nhập. Ví dụ giả định: `https://s3.example.invalid`. |
| Khu vực | Khu vực do nhà cung cấp của quý vị yêu cầu. Giá trị mặc định của ứng dụng là `us-east-1`. |
| Bucket | Một bucket hiện có mà quý vị có thể truy cập. Ví dụ giả định: `example-case-backup`. |
| Thư mục trong bucket | Tiền tố đối tượng; mặc định là `tgwitness`. Ứng dụng sẽ thêm vào một tiền tố được tạo ra từ dấu vân tay khóa ký của không gian làm việc này. |
| ID khóa truy cập / Khóa truy cập bí mật | Vui lòng nhập cả hai thông tin đăng nhập lưu trữ cùng lúc. Các thông tin này sẽ được lưu trữ trong kho dữ liệu của không gian làm việc. Khi lưu lại sau này, quý vị hãy để trống cả hai trường này để giữ nguyên cặp thông tin đã lưu. |
| Địa chỉ theo kiểu đường dẫn | Vui lòng sử dụng mã `endpoint/bucket` khi tính năng được kích hoạt, hoặc mã `bucket.endpoint` khi tính năng bị vô hiệu hóa, tùy theo nhà cung cấp. |
| Khoảng thời gian sao chép | Từ 1 đến 1.440 phút; mặc định là 5 phút. Ứng dụng phải đang chạy để thực hiện việc sao chép theo lịch trình. |
| Chính sách lưu trữ Object Lock | Thời gian lưu trữ và chế độ lưu trữ đối với một bucket hỗ trợ tính năng Object Lock. Giá trị “Zero days” sẽ giữ nguyên cài đặt lưu trữ mặc định của bucket. |

1. Vui lòng nhập địa chỉ đích và thông tin đăng nhập. Trong quá trình chuẩn bị, xin vui lòng để tùy chọn **“Giữ bản sao ngoài trang web”** ở trạng thái chưa được chọn, sau đó chọn **“Lưu bản sao ngoài trang web**”.
2. Chọn **“Kiểm tra kết nối**”. Thao tác này sẽ tải lên một đối tượng thử nghiệm được mã hóa và kiểm tra phản hồi từ bộ lưu trữ.
3. Vui lòng chọn **“Tải xuống khóa mã hóa**”. Hãy lưu giữ tệp này riêng biệt với công cụ thu thập dữ liệu; tệp này là cần thiết cho quá trình khôi phục dữ liệu.
4. Vui lòng chọn hộp kiểm **“Lưu bản sao ngoài trang web**” và lưu lại. Chọn **“Sao chép ngay”** để thực hiện thủ công, hoặc để lịch trình tiếp tục chạy.

**Những điều không thực hiện** Công cụ này không tạo ra bất kỳ kho lưu trữ nào. Các tác vụ tải lên theo lịch trình sẽ dừng lại khi ứng dụng ngừng hoạt động.

## Kiểm tra tiến độ lưu trữ và sao chép

Trong phần**“Tùy chọn khác” (More options)**, quý vị hãy chọn số ngày lưu trữ và `GOVERNANCE` hoặc `COMPLIANCE` nếu kho lưu trữ (bucket) của quý vị hỗ trợ tính năng Object Lock. TgWitness sẽ đọc lại chế độ lưu trữ và thời hạn của đối tượng đã tải lên. Báo cáo trạng thái sẽ xác nhận việc lưu trữ, thông báo thiếu thời hạn lưu trữ hoặc lỗi kiểm tra; việc tải lên thành công không tự động đồng nghĩa với việc xác nhận lưu trữ.

Bảng điều khiển hiển thị thông tin về lần quét gần nhất, số lượng đối tượng, dung lượng dữ liệu đã truyền, ranh giới của nhật ký đã sao chép cùng bất kỳ lỗi nào phát sinh. Các phương tiện lưu trữ cục bộ bị thiếu hoặc đã thay đổi sẽ được báo cáo và hệ thống sẽ thử lại trong lần quét tiếp theo. Các tệp tin, điểm kiểm tra và các tác vụ xuất dữ liệu đang chờ xử lý sau phương tiện lưu trữ đó vẫn có thể được sao chép.

Việc tải lên sử dụng các đường dẫn Direct, SOCKS5 hoặc HTTP của không gian làm việc. Tính năng sao chép lên S3 không khả dụng qua MTProxy; ứng dụng sẽ không chuyển sang kết nối trực tiếp.

**Những điều không thực hiện** Việc này không bắt buộc nhà cung cấp phải áp dụng tính năng Object Lock chỉ vì việc tải lên đã được chấp nhận.

## Hãy lưu giữ khóa khôi phục ở một nơi riêng biệt

Tệp JSON đã tải xuống chứa khóa giải mã, cài đặt đích, tiền tố đối tượng không gian làm việc và dấu vân tay khóa ký. Tệp này không chứa thông tin đăng nhập S3: quá trình khôi phục cần có thông tin đăng nhập riêng với quyền truy cập đọc vào bucket.

Nếu quý vị thay đổi điểm cuối (endpoint), bucket hoặc tiền tố thư mục, vui lòng tải lại tệp khóa để các cài đặt đích của tệp này khớp với thay đổi. Ứng dụng sẽ khởi tạo một bản sao mới của nhật ký, tệp tin và các điểm kiểm tra được lưu trữ cục bộ tại đích mới. Các bản xuất cuộc trò chuyện đã hoàn tất nhưng đã bị xóa khỏi hàng đợi tải lên cục bộ sẽ vẫn được giữ nguyên tại đích cũ.

**Những điều không thực hiện** Công cụ này sẽ không giải mã bản sao nếu không có khóa đã xuất ra. Thông tin đăng nhập truy cập bộ nhớ lưu trữ không thể thay thế cho khóa đó.

## Khôi phục và xác minh trên một máy tính khác

Vui lòng sử dụng bản cài đặt đáng tin cậy của TgWitness, tệp JSON chứa khóa đã tải xuống, thông tin đăng nhập vào bộ lưu trữ có quyền truy cập đọc, cùng với một thư mục đầu ra trống. Hãy thay thế các thông tin đăng nhập giả định được ghi dưới đây.

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

Các tệp tải xuống và các đối tượng đã được giải mã sẽ được lưu trữ tạm thời trong kho lưu trữ riêng tư trong khi toàn bộ nhật ký, các điểm kiểm tra được lưu giữ cùng các giá trị băm và kích thước của phương tiện được bảo toàn sẽ được kiểm tra. Các đường dẫn không an toàn, các phân đoạn nhật ký mâu thuẫn và nhật ký có độ dài ngắn hơn điểm kiểm tra tương ứng sẽ bị từ chối. Trong trường hợp xác minh thất bại, hệ thống sẽ không công bố bất kỳ tệp nào đã được khôi phục.

Quá trình khôi phục thành công sẽ tạo ra các mã `events.jsonl`, `media/`, `checkpoints/` và `exports/` tương ứng với nội dung có sẵn trong bản sao. Vui lòng lưu giữ kết quả JSON của lệnh cùng với nội dung đã được khôi phục.

**Những điều không thực hiện** Công cụ này không tái tạo các quan sát chưa bao giờ được ghi vào sổ chứng cứ, cũng như không thay thế các điểm kiểm tra hoặc nhân chứng được lưu giữ độc lập.
