# Tin nhắn có thể thay đổi． Hãy lưu giữ những gì quý vị đã thấy．

Canonical page: https://phishdestroy.github.io/TgWitness/vi/

[Nguồn mở ／ v0.9.1](https://phishdestroy.github.io/TgWitness/vi/docs/reference/changelog/)

Xuất các cuộc trò chuyện trên Telegram， giữ nguyên lịch sử trò chuyện và chia sẻ một tệp lưu trữ được ký số mà người khác có thể xác minh．

[Mở bản demo](https://phishdestroy.github.io/TgWitness/demo/?lang=vi)[Hướng dẫn cài đặt](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=vi)

Dữ liệu giả， không cần đăng nhập Telegram．

 [Xuất tài khoản hoặc các cuộc trò chuyện đã chọn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/account-export/) [Thu thập qua GitHub Actions （bản xem trước）](https://phishdestroy.github.io/TgWitness/vi/docs/capture/) [Bản sao lưu ngoài trang web trên S3： thiết lập và khôi phục](https://phishdestroy.github.io/TgWitness/vi/#s3)

MỘT TIN NHẮN， VƯỢT QUA THỜI GIAN ＃0042

Northstar · Nghiên cứuNguồn／tin nhắn hư cấu số 42

1. **Tin nhắn được ghi nhận：**09：41：02

   Bản tóm tắt bắt đầu tại 14：00．
2. **Bản chỉnh sửa được lưu giữ**09：43：18

   Bản tóm tắt bắt đầu tại 15：00．

   Phiên bản trước vẫn được giữ nguyên
3. **Thông báo xóa**10：06：45

   Nội dung được ghi lại sẽ được lưu trữ trong sổ nhật ký của quý vị．

Ba quan sát． Một lịch sử． VÍ DỤ

Tin nhắn có thể biến mất． Nhưng lịch sử đã được ghi lại vẫn còn đó．

## Mọi thay đổi được ghi lại． Ngay tại nơi quý vị cần．

Giao diện thật， dữ liệu bịa．

TgWitness ／ Các cuộc trò chuyện đã lưuKHÔNG GIAN LÀM VIỆC QUAN SÁT CỦA QUÝ VỊ

![Các cuộc trò chuyện Telegram được lưu trữ trong chế độ giao diện tối， kèm theo các thao tác chỉnh sửa và tin nhắn đã xóa được ghi lại đầy đủ trong bối cảnh tương ứng](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ Cuộc trò chuyện đã lưu Trông như một cuộc trò chuyện bình thường， với các lần sửa và xóa ngay cạnh tin nhắn．

TgWitness ／ Nhật kýKHÔNG GIAN LÀM VIỆC ĐỊA PHƯƠNG

![Tạp chí ghi lại các tin nhắn được quan sát， các thao tác chỉnh sửa， thông báo xóa và các sự kiện liên quan](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ Sổ nhật ký Mọi thứ tài khoản của bạn thấy， tìm kiếm được， kể cả các khoảng trống．

TgWitness ／ Lịch sử chỉnh sửaKHÔNG GIAN LÀM VIỆC ĐỊA PHƯƠNG

![Cửa sổ chi tiết so sánh phiên bản tin nhắn đã được ghi lại trước đó với phiên bản đã được chỉnh sửa](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ Lịch sử chỉnh sửa Phiên bản cũ và mới đặt cạnh nhau， không gì bị ghi đè．

TgWitness ／ Các tệp xuất có chữ kýKHÔNG GIAN LÀM VIỆC ĐỊA PHƯƠNG

![Tính năng xuất không gian làm việc cung cấp các tệp ZIP， JSONL， CSV đã được ký số cùng với báo cáo HTML có thể sử dụng ngoại tuyến](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ Bản xuất có chữ ký Mang sổ nhật ký theo， đã ký， kèm công cụ xác minh riêng．

Theo dõi một bản ghi đã lưu qua [Case Board](https://phishdestroy.github.io/TgWitness/vi/docs/case-board/)， [thiết kế báo cáo](https://phishdestroy.github.io/TgWitness/vi/docs/reports/) và bản [sao chia sẻ](https://phishdestroy.github.io/TgWitness/vi/docs/handover/)． [Xem xét các nhóm tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/groups/) cùng nhau．

01 ／ GHI LẠI

### Quý vị tự quyết định phạm vi áp dụng．

Vài cuộc trò chuyện， một thư mục hoặc cả tài khoản． Mỗi tài khoản có không gian làm việc riêng．

[So sánh các chế độ thu thập](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html#scope)

02 ／ BẢO QUẢN

### Những thay đổi góp phần làm phong phú thêm câu chuyện．

Phiên bản， lần xóa và khoảng trống đều nằm lại trong sổ nhật ký．

[Xem ma trận sự kiện](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html#events)

03 ／ BÀN GIAO

### Một bản ghi có khả năng di chuyển．

ZIP có chữ ký， tệp và báo cáo ngoại tuyến． Mật khẩu tùy chọn．

[Xuất và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/exports/)

## Chỉ cần thay đổi một byte．
Hệ thống xác minh sẽ thông báo cho bạn．

Mỗi sự kiện đều có liên kết đến mã băm trước đó và đi kèm với chữ ký Ed25519．

![Các sự kiện được ghi lại có liên kết đến các giá trị băm trước đó， kèm theo chữ ký và được xuất dưới dạng tệp có thể xác minh．](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Việc thay đổi một bản ghi đã được thu thập sẽ làm thay đổi giá trị băm của bản ghi đó và khiến quá trình xác minh bản ghi được liên kết bị gián đoạn．](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Một điểm kiểm tra được lưu giữ riêng biệt cho phép người nhận so sánh nhật ký đã xuất với một bản ghi trước đó．](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Tuân thủ các bước kiểm tra từ băm tệp đến điểm kiểm tra được lưu giữ riêng biệt．

[Khám phá tám cấp độ bằng chứng](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html#levels)

## Sẵn sàng để nhận được ý kiến đóng góp từ các chuyên gia khác．

Tin nhắn， tệp và báo cáo ngoại tuyến trong một gói có chữ ký．

[Xem mô hình bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/)

tgwitness-evidence.zipGÓI CÓ CHỨNG THỰC

- 01

  Những quan sát ban đầuBản ghi JSONL ＋ bảng CSV
- 02

  Bối cảnh dễ hiểuBáo cáo HTML ngoại tuyến ＋ phương tiện truyền thông được lưu giữ nguyên vẹn
- 03

  Xác minh độc lậpBản kê khai có chữ ký ＋ công cụ xác minh độc lập

Người nhận kiểm tra mọi thứ bằng khóa của bạn， và một điểm kiểm tra lưu ở nơi khác cho thấy không có gì bị viết lại kể từ đó． [Cách hoạt động của các bước kiểm tra．](https://phishdestroy.github.io/TgWitness/vi/docs/concepts/#layers)

## Bản sao trên S3． Các kiểm tra bên ngoài．

Giữ lại các bản sao được mã hóa và bổ sung các cơ chế kiểm tra độc lập．

Tắt theo mặc định

### Sao chép toàn bộ dữ liệu vào bộ lưu trữ tương thích với S3

Sổ nhật ký， tệp， điểm kiểm tra và bản xuất trò chuyện， được mã hóa trước khi gửi lên S3．

**Cài đặt lưu trữ và khôi phục**

Mã hóa phía máy khách

`AES-256-GCM` trên máy của bạn． Nhà cung cấp chỉ thấy bản mã．

Sao chép theo lịch trình hoặc thủ công

Sao chép ngay hoặc cứ mỗi 1 đến 1.440 phút， tiến độ hiển thị trong bảng điều khiển．

Khóa đối tượng

Chọn số ngày lưu giữ và chế độ， bảng điều khiển kiểm tra xem nó có thực sự được áp dụng không．

Khôi phục đã được xác minh

Hãy giữ khóa riêng． Khôi phục ở bất cứ đâu， tệp chỉ được xuất ra sau khi xác minh．

![Bảng điều khiển sao lưu ngoài trang web đầy đủ： điểm cuối， khu vực， thùng lưu trữ， khóa truy cập， lịch trình， các thiết lập kiểm soát Object Lock và khóa khôi phục](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Bảng điều khiển đầy đủ với các tùy chọn nâng cao đã được mở rộng． Không hiển thị bất kỳ thông tin đăng nhập lưu trữ nào．

Tạp chí và phương tiện truyền thông`AES-256-GCM`Bộ lưu trữ tương thích với S3

[Cấu hình S3 và khôi phục bản sao](https://phishdestroy.github.io/TgWitness/vi/docs/exports/#s3)[Xem chi tiết xác minh tại](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Khóa khôi phục** Hãy giữ riêng， thiếu nó thì bản sao không đọc được．

### Thông báo · Apprise

Sự cố， thay đổi trong trò chuyện và bản tóm tắt hằng ngày gửi tới ứng dụng nhắn tin， email hoặc webhook của riêng bạn．

**Chọn nội dung cần chia sẻ** Không kèm nội dung tin nhắn trừ khi bạn bật lên．

 [Cấu hình điểm đến thông báo](https://phishdestroy.github.io/TgWitness/vi/docs/reference/operations/#notifications)

### Dấu thời gian bên ngoài

Tạo băm điểm kiểm tra dấu thời gian bằng RFC 3161 và OpenTimestamps．

**Theo dõi kết quả** Kiểm tra phản hồi TSA hoặc nâng biên nhận OpenTimestamps thành bằng chứng Bitcoin．

 [Kiểm tra bằng chứng dấu thời gian](https://phishdestroy.github.io/TgWitness/vi/docs/reference/timestamp/)

### Nhân chứng độc lập

Một máy chủ riêng biệt sẽ lưu trữ các quan sát đã được ký và có thể công bố `TGW1` các điểm kiểm tra．

**Tách riêng mốc tham chiếu** Chạy trên một máy chủ khác， với khóa và sổ nhật ký riêng．

 [Thiết lập một Witness](https://phishdestroy.github.io/TgWitness/vi/docs/witness/)

### Khả năng phục hồi và những lỗ hổng rõ ràng

Tiếp tục sau khi khởi động lại． Kiểm tra lại và `coverage.json` hiển thị các tin nhắn đã khôi phục cùng các khoảng trống．

**Xem lại khoảng thời gian** Tin nhắn khôi phục và khoảng trống đã ghi nhận đặt cạnh nhau．

 [Kiểm tra tính liên tục và các khoảng trống](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html#continuity)

## Không gian làm việc đầu tiên của quý vị bắt đầu từ đây．

Thử bản demo trước， khi sẵn sàng thì kết nối một tài khoản phụ．
Windows， Linux， macOS hoặc Docker．

[Xin vui lòng tham khảo hướng dẫn cài đặt](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=vi)

**Mỗi phiên được nhập vào chỉ tương ứng với một ứng dụng khách đang chạy．**

Đừng chạy cùng lúc TData hoặc phiên đã nhập trong Telegram Desktop và TgWitness， Telegram có thể vô hiệu hóa cả hai （AUTH_KEY_DUPLICATED）． Cần cả hai？ Hãy đăng nhập TgWitness riêng bằng số điện thoại hoặc mã QR．

[Vui lòng đọc cảnh báo về việc nhập phiên làm việc](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=vi#session-warning)

**Xin vui lòng tham khảo trước khi kết nối．**

Hãy thử không gian làm việc giả định này mà không cần tài khoản Telegram．

[Mở bản demo trực tuyến →](https://phishdestroy.github.io/TgWitness/demo/?lang=vi)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**Các lệnh cài đặt cục bộ**

BƯỚC 01

### Tải về mã nguồn．

[Vui lòng tải xuống tệp ZIP nguồn](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) và giải nén， hoặc sao chép kho lưu trữ：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Cần Python 3.11+． Trên Windows， trình khởi chạy sẽ đề nghị cài đặt giúp bạn．

[Xem các bản phát hành](https://github.com/phishdestroy/TgWitness/releases)

BƯỚC 02

### Chọn cách thức vận hành．

Nhấp đúp vào tệp `Start.cmd` hoặc chạy lệnh trong PowerShell：

```
.\Start.cmd
```

Chỉ đang tìm hiểu sơ qua？ Vui lòng nhấp đúp vào `scripts\Demo.cmd` để trải nghiệm bản demo độc lập． Không cần đăng nhập Telegram．

Với Python 3.11 trở lên và `venv`：

```
sh start.sh
```

Để mở sổ nhật ký giả định này， vui lòng chạy lệnh `sh start.sh --demo`．

Khi Docker đã được khởi chạy và Compose phiên bản 2.20 trở lên đã được cài đặt：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Lệnh thứ hai sẽ hiển thị mã thông báo bảng điều khiển riêng tư của quý vị． Vui lòng lưu giữ mã này trên thiết bị của quý vị．

Vui lòng truy cập [127.0.0.1:8787](http://127.0.0.1:8787) sau khi khởi chạy．

Khi cài từ mã nguồn， token nằm trong `data/live/panel-token.txt`． Cặp API riêng của bạn từ [my.telegram.org](https://my.telegram.org) là tùy chọn． [Hướng dẫn cài đặt đầy đủ ↗](https://phishdestroy.github.io/TgWitness/vi/docs/reference/quickstart/)

**TgWitness 0.9.1** [Có gì mới →](https://phishdestroy.github.io/TgWitness/vi/docs/reference/changelog/) · [Các tính năng và giới hạn đã biết →](https://phishdestroy.github.io/TgWitness/vi/docs/reference/features/)

## Hướng dẫn rõ ràng． Bước tiếp theo hữu ích．

[Khám phá các hướng dẫn ↗](https://phishdestroy.github.io/TgWitness/vi/docs/)

[### Các chế độ， tình huống và mức độ bằng chứng Bốn chế độ thu thập． Tám cấp độ xác minh． Hãy tìm quy trình làm việc phù hợp với trường hợp của quý vị．](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html)

[01 ### Kết nối tài khoản Hỗ trợ nhập dữ liệu từ điện thoại， mã QR và các phiên làm việc được hỗ trợ．](https://phishdestroy.github.io/TgWitness/vi/docs/accounts/)[02 ### Chọn một máy chủ proxy Danh sách MTProxy công khai hoặc tuyến đường riêng của quý vị．](https://phishdestroy.github.io/TgWitness/vi/docs/proxies/)[03 ### Thiết lập bot chứng cứ Các mốc kiểm tra có chữ ký trong kênh Telegram của quý vị．](https://phishdestroy.github.io/TgWitness/vi/docs/witness/)[04 ### Xuất và xác minh Chia sẻ lịch sử đã ghi lại và kiểm tra tính toàn vẹn của nó．](https://phishdestroy.github.io/TgWitness/vi/docs/exports/)

## Quản lý kho lưu trữ．

Lịch sử， AI có nguồn trích dẫn， MCP， OCR và webhook có chữ ký．

[Khám phá quy trình làm việc](https://phishdestroy.github.io/TgWitness/vi/docs/archive/)

## Trước khi bắt đầu．

**Trang này có liên kết đến Telegram không？**

Không． Đây là trang tĩnh với ví dụ giả． Ứng dụng chạy trên máy của bạn và bạn đăng nhập ở đó．

**Công cụ này có thể khôi phục các tin nhắn đã bị xóa trước khi được ghi lại không？**

Không． Nó lưu những gì tài khoản của bạn thấy trong lúc đang chạy． Ảnh chụp sau này không thể khôi phục các lần sửa đã bỏ lỡ hay tin nhắn đã xóa．

**Toàn bộ nhật ký của tôi có được mã hóa không？**

Phiên và khóa thì có． Tin nhắn và tệp thì không， hãy dùng mã hóa ổ đĩa． Bản xuất có thể đặt mật khẩu AES－256．

**Công cụ này có liên kết với Telegram không？**

Không． Đây là dự án độc lập theo giấy phép MIT， xây dựng trên Telethon． Bạn đăng nhập bằng tài khoản của chính mình．

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Hãy khám phá trước． Thiết lập khi đã sẵn sàng．

[Mở bản demo](https://phishdestroy.github.io/TgWitness/demo/?lang=vi)[Hướng dẫn cài đặt](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=vi)
