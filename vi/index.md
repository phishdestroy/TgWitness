# Tin nhắn có thể thay đổi. Hãy lưu giữ những gì quý vị đã thấy.

Canonical page: https://phishdestroy.github.io/TgWitness/vi/

[Nguồn mở / v0.7.0](https://phishdestroy.github.io/TgWitness/vi/docs/reference/changelog/)

Ghi lại các tin nhắn Telegram, bảo toàn các thay đổi của chúng và xuất bản ghi có chữ ký.

[Mở bản demo](https://phishdestroy.github.io/TgWitness/demo/?lang=vi)[Hướng dẫn cài đặt](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=vi)

Bản demo sử dụng dữ liệu giả định. Không yêu cầu đăng nhập Telegram.

 [Thu thập qua GitHub Actions (bản xem trước)](https://phishdestroy.github.io/TgWitness/vi/docs/capture/) [Bản sao lưu ngoài trang web trên S3: thiết lập và khôi phục](https://phishdestroy.github.io/TgWitness/vi/#s3)

MỘT TIN NHẮN, VƯỢT QUA THỜI GIAN #0042

Northstar · Nghiên cứuNguồn/tin nhắn hư cấu số 42

1. **Tin nhắn được ghi nhận:**09:41:02

   Bản tóm tắt bắt đầu tại 14:00.
2. **Bản chỉnh sửa được lưu giữ**09:43:18

   Bản tóm tắt bắt đầu tại 15:00.

   Phiên bản trước vẫn được giữ nguyên
3. **Thông báo xóa**10:06:45

   Nội dung được ghi lại sẽ được lưu trữ trong sổ nhật ký của quý vị.

Ba quan sát. Một lịch sử. VÍ DỤ

Tin nhắn có thể biến mất. Nhưng lịch sử đã được ghi lại vẫn còn đó.

## Mọi thay đổi được ghi lại. Ngay tại nơi quý vị cần.

Hãy khám phá giao diện với dữ liệu minh họa giả định.

TgWitness / Các cuộc trò chuyện đã lưuKHÔNG GIAN LÀM VIỆC QUAN SÁT CỦA QUÝ VỊ

![Các cuộc trò chuyện Telegram được lưu trữ trong chế độ giao diện tối, kèm theo các thao tác chỉnh sửa và tin nhắn đã xóa được ghi lại đầy đủ trong bối cảnh tương ứng](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Các cuộc trò chuyện đã lưu: Giao diện xem cuộc trò chuyện quen thuộc, hiển thị các thao tác chỉnh sửa và thông báo xóa đã được ghi lại bên cạnh các tin nhắn.

TgWitness / Nhật kýKHÔNG GIAN LÀM VIỆC ĐỊA PHƯƠNG

![Tạp chí ghi lại các tin nhắn được quan sát, các thao tác chỉnh sửa, thông báo xóa và các sự kiện liên quan](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Nhật ký: Một dòng thời gian có thể tìm kiếm được về những gì tài khoản của quý vị đã ghi nhận, bao gồm cả các sự gián đoạn.

TgWitness / Lịch sử chỉnh sửaKHÔNG GIAN LÀM VIỆC ĐỊA PHƯƠNG

![Cửa sổ chi tiết so sánh phiên bản tin nhắn đã được ghi lại trước đó với phiên bản đã được chỉnh sửa](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Lịch sử chỉnh sửa: So sánh các phiên bản đã ghi lại mà không ghi đè lên bản ghi trước đó.

TgWitness / Các tệp xuất có chữ kýKHÔNG GIAN LÀM VIỆC ĐỊA PHƯƠNG

![Tính năng xuất không gian làm việc cung cấp các tệp ZIP, JSONL, CSV đã được ký số cùng với báo cáo HTML có thể sử dụng ngoại tuyến](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Xuất dữ liệu có chữ ký: Mang theo sổ nhật ký của quý vị, kèm theo bản kê khai và một bên xác minh độc lập.

01 / GHI LẠI

### Quý vị tự quyết định phạm vi áp dụng.

Các cuộc trò chuyện đã chọn, một thư mục trên Telegram hoặc toàn bộ tài khoản. Mỗi tài khoản sẽ có một không gian làm việc riêng biệt.

[So sánh các chế độ thu thập](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html#scope)

02 / BẢO QUẢN

### Những thay đổi góp phần làm phong phú thêm câu chuyện.

Các phiên bản đã được “Captured”, thông báo xóa và các khoảng trống trong quá trình quan sát vẫn được lưu giữ trong nhật ký.

[Xem ma trận sự kiện](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html#events)

03 / BÀN GIAO

### Một bản ghi có khả năng di chuyển.

Tệp ZIP được ký số, các tệp được bảo toàn và báo cáo ngoại tuyến. Tùy chọn bảo vệ bằng mật khẩu.

[Xuất và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/exports/)

## Chỉ cần thay đổi một byte. Chuỗi khối sẽ thông báo cho quý vị.

Mỗi sự kiện đều có liên kết đến mã băm trước đó và đi kèm với chữ ký Ed25519.

![Các sự kiện được ghi lại có liên kết đến các giá trị băm trước đó, kèm theo chữ ký và được xuất dưới dạng tệp có thể xác minh.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Việc thay đổi một bản ghi đã được thu thập sẽ làm thay đổi giá trị băm của bản ghi đó và khiến quá trình xác minh bản ghi được liên kết bị gián đoạn.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Một điểm kiểm tra được lưu giữ riêng biệt cho phép người nhận so sánh nhật ký đã xuất với một bản ghi trước đó.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Hãy tìm hiểu xem từng cơ chế xác minh thiết lập những gì, cũng như những hạn chế của chúng nằm ở đâu.

[Khám phá tám cấp độ bằng chứng](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html#levels)

## Sẵn sàng để nhận được ý kiến đóng góp từ các chuyên gia khác.

Chuyển giao các dữ liệu quan sát, tệp tin và báo cáo HTML ngoại tuyến trong một gói dữ liệu đã được ký số.

[Xem mô hình bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/)

tgwitness-evidence.zipGÓI CÓ CHỨNG THỰC

- 01

  Những quan sát ban đầuBản ghi JSONL + bảng CSV
- 02

  Bối cảnh dễ hiểuBáo cáo HTML ngoại tuyến + phương tiện truyền thông được lưu giữ nguyên vẹn
- 03

  Xác minh độc lậpBản kê khai có chữ ký + công cụ xác minh độc lập

Các chữ ký dùng để phát hiện hành vi giả mạo dựa trên một khóa tin cậy. Chúng không chứng minh nguồn gốc từ Telegram cũng như không đảm bảo việc ghi lại đầy đủ. Nội dung nhật ký và các tệp đa phương tiện cần được lưu trữ dưới dạng mã hóa do quý vị cung cấp.

## Bản sao trên S3. Các kiểm tra bên ngoài.

Giữ lại các bản sao được mã hóa và bổ sung các cơ chế kiểm tra độc lập.

Tắt theo mặc định

### Sao chép toàn bộ dữ liệu vào bộ lưu trữ tương thích với S3

Nhật ký, tệp tin, các điểm kiểm tra có dấu thời gian và dữ liệu xuất từ cuộc trò chuyện — đều được mã hóa trước khi tải lên AWS S3 hoặc các dịch vụ lưu trữ tương thích.

**Cài đặt lưu trữ và khôi phục**

Mã hóa phía máy khách

`AES-256-GCM` mã hóa các đối tượng trên máy này. Nhà cung cấp sẽ nhận được các đối tượng đã được mã hóa.

Sao chép theo lịch trình hoặc thủ công

Sao chép ngay bây giờ hoặc chọn khoảng thời gian từ 1 đến 1.440 phút. Kiểm tra tiến trình trong bảng điều khiển.

Khóa đối tượng

Vui lòng chọn số ngày lưu trữ và chế độ tương ứng khi kho lưu trữ hỗ trợ tính năng này. Bảng điều khiển sẽ thông báo liệu việc lưu trữ đối với một đối tượng đã tải lên có được xác nhận hay không.

Khôi phục đã được xác minh

Vui lòng tải xuống khóa mã hóa và lưu trữ riêng biệt. Khôi phục trên một máy tính khác; các tệp chỉ được công bố sau khi đã qua quá trình xác minh.

![Bảng điều khiển sao lưu ngoài trang web đầy đủ: điểm cuối, khu vực, thùng lưu trữ, khóa truy cập, lịch trình, các thiết lập kiểm soát Object Lock và khóa khôi phục](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Bảng điều khiển đầy đủ với các tùy chọn nâng cao đã được mở rộng. Không hiển thị bất kỳ thông tin đăng nhập lưu trữ nào.

Tạp chí và phương tiện truyền thông`AES-256-GCM`Bộ lưu trữ tương thích với S3

[Cấu hình S3 và khôi phục bản sao](https://phishdestroy.github.io/TgWitness/vi/docs/exports/#s3)[Xem chi tiết xác minh tại](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Những điều không thực hiện** Công cụ này không thể khôi phục dữ liệu nếu thiếu khóa giải mã đã xuất ra, cũng như không thể thay thế vai trò của một nhân chứng độc lập.

### Thông báo · Apprise

Cảnh báo sự cố, thay đổi trong cuộc trò chuyện và bản tóm tắt hàng ngày qua Apprise: các ứng dụng nhắn tin, email hoặc webhook JSON của riêng quý vị.

**Không thực hiện** Nó sẽ không gửi nội dung tin nhắn trừ khi quý vị bật tính năng trích dẫn.

 [Cấu hình điểm đến thông báo](https://phishdestroy.github.io/TgWitness/vi/docs/reference/operations/#notifications)

### Dấu thời gian bên ngoài

Tạo băm điểm kiểm tra dấu thời gian bằng RFC 3161 và OpenTimestamps.

**Những điều không thực hiện** Công cụ này không coi biên nhận lịch đang chờ xử lý là dấu thời gian Bitcoin đã được xác nhận.

 [Kiểm tra bằng chứng dấu thời gian](https://phishdestroy.github.io/TgWitness/vi/docs/reference/timestamp/)

### Nhân chứng độc lập

Một máy chủ riêng biệt sẽ lưu trữ các quan sát đã được ký và có thể công bố `TGW1` các điểm kiểm tra.

**Những điều không thực hiện** Việc này không biến hai không gian làm việc trên cùng một máy chủ thu thập dữ liệu thành các nhân chứng độc lập.

 [Thiết lập một Witness](https://phishdestroy.github.io/TgWitness/vi/docs/witness/)

### Khả năng phục hồi và những lỗ hổng rõ ràng

Tiếp tục sau khi khởi động lại. Kiểm tra lại và `coverage.json` hiển thị các tin nhắn đã khôi phục cùng các khoảng trống.

**Những điều không thực hiện** Công cụ này không tái tạo lại mọi thao tác chỉnh sửa bị bỏ sót hoặc tin nhắn đã biến mất.

 [Kiểm tra tính liên tục và các khoảng trống](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html#continuity)

## Không gian làm việc đầu tiên của quý vị bắt đầu từ đây.

Hãy khám phá bản demo trước tiên. Khi đã sẵn sàng, quý vị hãy kết nối với một tài khoản chuyên dụng. Hỗ trợ Windows, Linux, macOS hoặc Docker.

[Xin vui lòng tham khảo hướng dẫn cài đặt](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=vi)

**Mỗi phiên được nhập vào chỉ tương ứng với một ứng dụng khách đang chạy.**

Không được chạy cùng lúc khóa TData/phiên làm việc đã nhập vào Telegram Desktop và TgWitness. Telegram có thể làm mất hiệu lực ủy quyền chung (AUTH_KEY_DUPLICATED). Để sử dụng song song, hãy tạo một tài khoản TgWitness riêng biệt bằng số điện thoại hoặc mã QR.

[Vui lòng đọc cảnh báo về việc nhập phiên làm việc](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=vi#session-warning)

**Xin vui lòng tham khảo trước khi kết nối.**

Hãy thử không gian làm việc giả định này mà không cần tài khoản Telegram.

[Mở bản demo trực tuyến →](https://phishdestroy.github.io/TgWitness/demo/?lang=vi)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**Các lệnh cài đặt cục bộ**

BƯỚC 01

### Tải về mã nguồn.

[Vui lòng tải xuống tệp ZIP nguồn](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) và giải nén, hoặc sao chép kho lưu trữ:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Việc khởi chạy ứng dụng yêu cầu Python 3.11 trở lên. Trình khởi chạy trên Windows sẽ tự động cài đặt Python nếu hệ thống chưa có.

[Xem các bản phát hành](https://github.com/phishdestroy/TgWitness/releases)

Không có Python trên Windows? Vui lòng [tải xuống gói phần mềm di động](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.0/TgWitness-0.7.0-windows-amd64-portable.zip), giải nén và nhấp đúp vào tệp `TgWitness.cmd`.

BƯỚC 02

### Chọn cách thức vận hành.

Nhấp đúp vào tệp `Start.cmd` hoặc chạy lệnh trong PowerShell:

```
.\Start.cmd
```

Chỉ đang tìm hiểu sơ qua? Vui lòng nhấp đúp vào `scripts\Demo.cmd` để trải nghiệm bản demo độc lập. Không cần đăng nhập Telegram.

Với Python 3.11 trở lên và `venv`:

```
sh start.sh
```

Để mở sổ nhật ký giả định này, vui lòng chạy lệnh `sh start.sh --demo`.

Khi Docker đã được khởi chạy và Compose phiên bản 2.20 trở lên đã được cài đặt:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Lệnh thứ hai sẽ hiển thị mã thông báo bảng điều khiển riêng tư của quý vị. Vui lòng lưu giữ mã này trên thiết bị của quý vị.

Vui lòng truy cập [127.0.0.1:8787](http://127.0.0.1:8787) sau khi khởi chạy.

Đối với cài đặt từ nguồn, mã thông báo nằm trong `data/live/panel-token.txt`. Việc đăng nhập Telegram có thể sử dụng cài đặt API tích hợp sẵn hoặc cặp khóa riêng của bạn từ [my.telegram.org](https://my.telegram.org). [Hướng dẫn cài đặt đầy đủ ↗](https://phishdestroy.github.io/TgWitness/vi/docs/reference/quickstart/)

**TgWitness 0.7.0** [Có gì mới →](https://phishdestroy.github.io/TgWitness/vi/docs/reference/changelog/) · [Các tính năng và giới hạn đã biết →](https://phishdestroy.github.io/TgWitness/vi/docs/reference/features/)

## Hướng dẫn rõ ràng. Bước tiếp theo hữu ích.

[Khám phá các hướng dẫn ↗](https://phishdestroy.github.io/TgWitness/vi/docs/)

[### Các chế độ, tình huống và mức độ bằng chứng Bốn chế độ thu thập. Tám cấp độ xác minh. Hãy tìm quy trình làm việc phù hợp với trường hợp của quý vị.](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html)

[01 ### Kết nối tài khoản Hỗ trợ nhập dữ liệu từ điện thoại, mã QR và các phiên làm việc được hỗ trợ.](https://phishdestroy.github.io/TgWitness/vi/docs/accounts/)[02 ### Chọn một máy chủ proxy Danh sách MTProxy công khai hoặc tuyến đường riêng của quý vị.](https://phishdestroy.github.io/TgWitness/vi/docs/proxies/)[03 ### Thiết lập bot chứng cứ Các mốc kiểm tra có chữ ký trong kênh Telegram của quý vị.](https://phishdestroy.github.io/TgWitness/vi/docs/witness/)[04 ### Xuất và xác minh Chia sẻ lịch sử đã ghi lại và kiểm tra tính toàn vẹn của nó.](https://phishdestroy.github.io/TgWitness/vi/docs/exports/)

## Quản lý kho lưu trữ.

Tải lịch sử, xem xét các nguồn AI, kết nối với máy khách MCP, nhận diện phương tiện truyền thông đã lưu và gửi webhook có chữ ký.

Có sẵn từ nguồn hiện tại. Phiên bản xem trước di động 0.7.0 ra mắt trước các công cụ này.

[Khám phá quy trình làm việc](https://phishdestroy.github.io/TgWitness/vi/docs/archive/)

## Trước khi bắt đầu.

**Trang này có liên kết đến Telegram không?**

Không. Đây là trang dự án tĩnh với các ví dụ và ảnh chụp màn hình mang tính hư cấu. Ứng dụng thực tế sẽ chạy trên máy tính hoặc máy chủ của quý vị; quá trình đăng nhập diễn ra tại đó.

**Công cụ này có thể khôi phục các tin nhắn đã bị xóa trước khi được ghi lại không?**

Không. TgWitness chỉ lưu giữ nội dung mà tài khoản của quý vị đã quan sát được trong thời gian quá trình thu thập dữ liệu đang diễn ra. Một bản chụp lịch sử được thực hiện sau đó sẽ không thể tái tạo lại các thao tác chỉnh sửa bị bỏ sót hoặc các tin nhắn đã bị xóa.

**Toàn bộ nhật ký của tôi có được mã hóa không?**

Thông tin đăng nhập tài khoản và khóa ký được lưu trữ trong một kho dữ liệu được mã hóa. Các tin nhắn và tệp đính kèm cục bộ cần được lưu trữ trên một đĩa hoặc phân vùng được mã hóa. Khi xuất dữ liệu, người dùng có thể tùy chọn sử dụng tệp ZIP được mã hóa theo tiêu chuẩn AES-256 và bảo vệ bằng mật khẩu.

**Công cụ này có liên kết với Telegram không?**

Không. TgWitness là một dự án độc lập sử dụng Telethon, được phân phối theo Giấy phép MIT. Quý vị sẽ tự thực hiện việc ủy quyền cho các tài khoản của mình, thông qua cài đặt API tích hợp sẵn hoặc cặp API riêng của quý vị.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Hãy khám phá trước. Thiết lập khi đã sẵn sàng.

[Mở bản demo](https://phishdestroy.github.io/TgWitness/demo/?lang=vi)[Hướng dẫn cài đặt](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=vi)
