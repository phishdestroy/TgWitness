# Xuất và xác minh

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/exports/

Cung cấp cho người nhận các tệp để họ có thể đối chiếu với không gian làm việc thu thập và lịch sử đã lưu của nó.

Giữ lại tham chiếuXuất tệp ZIP đã được ký điện tửNgười nhận xác minh

Quý vị mới làm quen với các chữ ký và điểm kiểm tra? Hãy [thử thay đổi một bản ghi mẫu](https://phishdestroy.github.io/TgWitness/vi/docs/concepts/#chain) và xem các kiểm tra nào sẽ phát hiện ra sự thay đổi đó.

Muốn lưu giữ một bản sao ngoài phạm vi của người thu thập dữ liệu? Vui lòng truy cập [phần Cài đặt S3](https://phishdestroy.github.io/TgWitness/vi/docs/exports/#s3), [tính năng Khóa đối tượng](https://phishdestroy.github.io/TgWitness/vi/docs/exports/#s3-retention) hoặc [tính năng khôi phục đã được xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/exports/#s3-restore).

## Lưu giữ một nguồn tham khảo đáng tin cậy

Vui lòng lưu dấu vân tay khóa công khai của không gian làm việc bên ngoài bộ thu thập dữ liệu. Trong quá trình thu thập, hãy lưu trữ các điểm kiểm tra đã được ký kết tại một vị trí khác hoặc sử dụng một [bên chứng kiến độc lập](https://phishdestroy.github.io/TgWitness/vi/docs/witness/). Các tham chiếu này cho phép người nhận kiểm tra khóa cũng như ranh giới của sổ nhật ký trước đó.

## Tải xuống tệp ZIP đã được ký số

Mở **tính năng Xuất (Exports)** và tạo tệp ZIP bằng chứng đã ký. Tệp này bao gồm nhật ký không gian làm việc đầy đủ và bản kê khai tệp đã ký. Sử dụng [Report Studio](https://phishdestroy.github.io/TgWitness/vi/docs/reports/) để tạo báo cáo dễ đọc, hoặc [trích xuất](https://phishdestroy.github.io/TgWitness/vi/docs/handover/) [bản](https://phishdestroy.github.io/TgWitness/vi/docs/handover/) [bàn giao](https://phishdestroy.github.io/TgWitness/vi/docs/handover/) để chỉ cung cấp dữ liệu đã chọn và được tối ưu hóa.

Các báo cáo định dạng HTML, PDF và JSON đều có con dấu đã ký riêng và có thể được kiểm tra độc lập. Tệp CSV là bản sao thuận tiện cho việc phân tích; hãy sử dụng chính tệp CSV bên trong tệp ZIP đã được xác minh để kiểm tra tính toàn vẹn của nó. Giữ lại tệp ZIP đã ký khi người nhận cũng cần các bản ghi nguồn và tệp đính kèm.

## Vui lòng xác minh bằng một bản sao đáng tin cậy của TgWitness

Trong môi trường dự án đã cài đặt, vui lòng thay thế dấu vân tay và đường dẫn tệp trong ví dụ:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Khi cả hai tham chiếu đều hợp lệ, kết quả sẽ báo cáo `key_pinned: true` và `checkpoint_checked: true`. Vui lòng lưu giữ kết quả xác minh cùng với tệp lưu trữ gốc. Điểm kiểm tra được lưu giữ phải nằm tại hoặc trước ranh giới của tệp xuất.

## Sử dụng kết quả xác minh

- **Kiểm tra các tệp đã được giao:** tệp manifest liên kết các giá trị băm của chúng, và chữ ký bản ghi liên kết với nhật ký đã lưu. Hệ thống sẽ phát hiện các tệp bị thay đổi hoặc chuỗi bản ghi bị gián đoạn.
- **Kiểm tra danh tính không gian làm việc:** dấu vân tay được lưu giữ độc lập xác định khóa ký mà bạn mong đợi.
- **So sánh với ranh giới trước đó:** một điểm kiểm tra được lưu giữ sẽ đối chiếu dữ liệu xuất ra với tiền tố nhật ký được lưu trước khi bàn giao.
- **Kiểm tra phạm vi thu thập:** các lỗ hổng, kết quả thu thập và thử nghiệm có kiểm soát theo trình tự “gửi → chỉnh sửa → xóa” mô tả các sự kiện mà cấu hình này đã ghi lại.

Lưu giữ các kết quả này cùng với bản sao của người nhận. Xem xét [những gì quá trình xác minh xác định được](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope) về phạm vi kiểm tra cũng như việc đánh giá riêng biệt các tuyên bố từ nguồn và phạm vi thu thập dữ liệu.

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

1. Tạo bucket với nhà cung cấp của bạn, sau đó nhập đích đến và thông tin đăng nhập. Để tùy chọn **“Giữ bản sao ngoài trang web”** ở trạng thái không được chọn trong quá trình chuẩn bị, sau đó chọn **“Lưu bản sao ngoài trang web**”.
2. Chọn **“Kiểm tra kết nối**”. Thao tác này sẽ tải lên một đối tượng thử nghiệm được mã hóa và kiểm tra phản hồi từ bộ lưu trữ.
3. Vui lòng chọn **“Tải xuống khóa mã hóa**”. Hãy lưu giữ tệp này riêng biệt với công cụ thu thập dữ liệu; tệp này là cần thiết cho quá trình khôi phục dữ liệu.
4. Vui lòng chọn hộp kiểm **“Lưu bản sao ngoài trang web**” và lưu lại. Chọn **“Sao chép ngay”** để thực hiện thủ công, hoặc để lịch trình tiếp tục chạy.

## Kiểm tra tiến độ lưu trữ và sao chép

Trong phần **“More options” (Tùy chọn khác**), hãy chọn số ngày lưu trữ và “`GOVERNANCE`” (Quản trị) hoặc “`COMPLIANCE`” (Tuân thủ) khi bucket của bạn hỗ trợ tính năng Object Lock. TgWitness sẽ đọc lại chế độ lưu trữ và thời hạn của một đối tượng đã tải lên. Kiểm tra kết quả lưu trữ riêng biệt: đã xác nhận, thiếu lưu trữ hoặc kiểm tra không thành công.

Bảng điều khiển hiển thị thông tin về lần quét gần nhất, số lượng đối tượng, dung lượng dữ liệu đã truyền, ranh giới của nhật ký đã sao chép cùng bất kỳ lỗi nào phát sinh. Các phương tiện lưu trữ cục bộ bị thiếu hoặc đã thay đổi sẽ được báo cáo và hệ thống sẽ thử lại trong lần quét tiếp theo. Các tệp tin, điểm kiểm tra và các tác vụ xuất dữ liệu đang chờ xử lý sau phương tiện lưu trữ đó vẫn có thể được sao chép.

Việc tải lên sử dụng các đường dẫn Direct, SOCKS5 hoặc HTTP của không gian làm việc. Chọn một trong các đường dẫn này để sao chép lên S3; đường dẫn chỉ sử dụng MTProxy sẽ khiến bản sao bị treo với thông báo lỗi.

## Hãy lưu giữ khóa khôi phục ở một nơi riêng biệt

Tệp JSON đã tải xuống chứa khóa giải mã, cài đặt đích, tiền tố đối tượng không gian làm việc và dấu vân tay khóa ký. Quá trình khôi phục cần cả tệp khóa này và thông tin đăng nhập lưu trữ riêng biệt có quyền truy cập đọc vào bucket. Hãy lưu giữ chúng trong kế hoạch khôi phục của bạn.

Nếu quý vị thay đổi điểm cuối (endpoint), bucket hoặc tiền tố thư mục, vui lòng tải lại tệp khóa để các cài đặt đích của tệp này khớp với thay đổi. Ứng dụng sẽ khởi tạo một bản sao mới của nhật ký, tệp tin và các điểm kiểm tra được lưu trữ cục bộ tại đích mới. Các bản xuất cuộc trò chuyện đã hoàn tất nhưng đã bị xóa khỏi hàng đợi tải lên cục bộ sẽ vẫn được giữ nguyên tại đích cũ.

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

So sánh tài liệu đã khôi phục với các điểm kiểm tra hoặc bản ghi chứng cứ mà bạn đã lưu giữ độc lập, sau đó xem xét phạm vi thu thập đã ghi lại cho khoảng thời gian bạn cần.
