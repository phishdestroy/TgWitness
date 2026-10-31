# Một nhật ký. Bốn chế độ thu thập. Tám cấp độ xác minh.

Canonical page: https://phishdestroy.github.io/TgWitness/vi/guides/modes.html

Các chế độ, kịch bản và mức độ bằng chứng

TgWitness Ghi lại những gì tài khoản được kết nối quan sát được. Một bên thứ ba có thể xác minh tính toàn vẹn của bản ghi so với một khóa đáng tin cậy độc lập.

[Các chế độ thu thập](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html#scope)[Các tình huống](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html#scenarios)[Các mức độ bằng chứng](https://phishdestroy.github.io/TgWitness/vi/guides/modes.html#levels)

Tổng quan trong 3–5 phút · các ví dụ giả định · triển khai hiện tại

1. **Telegram**

   Các bản cập nhật hiển thị trên tài khoản
2. **Trình thu thập**

   Các bản ghi được liên kết, mỗi bản ghi đều được ký
3. **Trình xác minh**

   Khóa đáng tin cậy + ranh giới được duy trì

`h₁ → h₂ → h₃ · Ed25519`Tính toàn vẹn đã được kiểm tra. Nguồn gốc từ Telegram và tính xác thực của một tin nhắn vẫn là hai vấn đề riêng biệt.

## Chọn phạm vi quan sát

Ba phạm vi và một cài đặt sẵn dành cho điều tra. Các trường hợp loại trừ và các loại nguồn được kích hoạt vẫn có hiệu lực.

Mặc định**Các cuộc trò chuyện đã chọn**

Các bản ghi

Chỉ sử dụng các nguồn được lựa chọn thủ công.

Các cuộc trò chuyện mới

Không được thêm tự động.

Hãy lựa chọn

Một tập hợp các kênh hoặc nhóm đã biết. Chưa có dung lượng trò chuyện cố định nào được xác định.

**Những điều không thực hiện** Nó không phát hiện các cuộc trò chuyện khác cũng như không bổ sung lại lịch sử trước đó.

Thư mục tài khoản**Thư mục Telegram**

Các bản ghi

Các thư mục được bao gồm và các danh mục, trừ các trường hợp loại trừ và các cuộc trò chuyện đã lưu trữ khi được cấu hình.

Các cuộc trò chuyện mới

Khớp các cuộc trò chuyện đang hoạt động; các thay đổi trong thư mục trong vòng một giờ.

Hãy lựa chọn

Một nhà phân tích đã duy trì một thư mục hồ sơ vụ việc. Hãy xác nhận việc thu thập dữ liệu trên một tài khoản chuyên dụng.

**Những điều không thực hiện** Nó không áp dụng các điều kiện thay đổi của thư mục muted/read của thư mục.

Xác nhận phạm vi**Toàn bộ tài khoản**

Các bản ghi

Các cuộc trò chuyện có thể nhìn thấy trên tài khoản, bao gồm các cuộc trò chuyện riêng tư và bot, thuộc các loại đã chọn.

Các cuộc trò chuyện mới

Sẽ được bổ sung khi bản cập nhật đầu tiên được phát hành.

Hãy lựa chọn

Một tài khoản quan sát chuyên dụng, bao gồm cả tài khoản tham gia vào một vụ việc.

**Những điều không thực hiện** Nó không tự động tham gia các cuộc trò chuyện hoặc bỏ qua quyền truy cập nguồn.

Cài đặt sẵn cho toàn bộ tài khoản**Chế độ điều tra**

Các bản ghi

Tất cả các loại nguồn, hành động riêng, hồ sơ nguồn và 200 tin nhắn hiển thị gần nhất của các nguồn mới được phát hiện.

Các cuộc trò chuyện mới

Một cuộc trò chuyện hoặc bot mới sẽ nhận được một hồ sơ và bản chụp nhanh lịch sử.

Hãy lựa chọn

Tham gia một nhóm hoặc tương tác với bot thông qua bảng điều khiển. Kiểm tra và lưu cài đặt sẵn.

**Những điều không thực hiện** Nó không chụp nhanh mọi cuộc trò chuyện hiện có cũng như không quan sát các sự kiện callback được kích hoạt trên một ứng dụng khách khác.

Các thẻ này chỉ mang tính chất so sánh cục bộ, không phải là các điều khiển thu thập dữ liệu trực tiếp. Chúng không gây thay đổi đối với tài khoản.

**Những điều không thực hiện** Không có chế độ nào đọc các cuộc trò chuyện bí mật, ghi lại khi quá trình bị dừng, tự động tham gia các nguồn hoặc truy xuất lịch sử trước đó vượt quá phạm vi yêu cầu snapshot/export.

[Vui lòng đọc chi tiết](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/)

## Thu thập qua GitHub Actions (bản xem trước)

Đăng nhập Telegram mới, một cuộc trò chuyện, tệp lưu trữ được mã hóa và chứng thực nguồn gốc GitHub.

[Mở trợ lý thu thập](https://phishdestroy.github.io/TgWitness/vi/docs/capture/)

## Những gì được ghi lại

Chỉ những quan sát đã được gửi hoặc được yêu cầu rõ ràng mới được đưa vào hồ sơ. Nguồn gốc không xác định sẽ vẫn được giữ nguyên trạng.

 Các công tắc ghi lại · minh họa cục bộTin nhắn mớiCác chỉnh sửaCác nội dung bị xóaPhản hồiTư cách thành viên

Bảng điều khiển áp dụng các tùy chọn này cho từng không gian làm việc. Việc tắt một tùy chọn sẽ giữ lại các bản ghi hiện có; việc bật lại tùy chọn đó sẽ không khôi phục các sự kiện đã bỏ lỡ.

**Ma trận sự kiện: tài liệu đã lưu trữ và các yếu tố chưa rõ còn lại**

| Danh mục | Đã lưu | Vẫn chưa rõ |
| --- | --- | --- |
| Thông điệp | Văn bản, ID, siêu dữ liệu người gửi, bối cảnh trả lời và gói cập nhật gốc. | Không có chữ ký Telegram nào có thể được xác minh bởi bên thứ ba. |
| Chỉnh sửa | Mọi phiên bản được quan sát, mà không ghi đè lên các phiên bản trước đó. | Các chỉnh sửa trung gian có thể bị bỏ sót; người gửi không nhất thiết phải là người chỉnh sửa. |
| Xóa | Thông báo kèm theo văn bản đã lưu trước đó, nếu có. | Thông tin về người xóa và thời gian thực hiện hành động chính xác không được cung cấp. |
| Xóa không có phạm vi | Thông báo ở cấp độ tài khoản; các đối tác không xác định vẫn được nêu rõ ràng. | Không dự đoán nội dung trò chuyện. Việc tương quan sẽ sử dụng các ID trong phạm vi tài khoản đã được lưu trước đó khi có thể. |
| Phản hồi | Các bộ đếm đã được truyền tải và danh tính gần đây có thể nhìn thấy. | Không phải mọi máy chủ phản hồi đều hiển thị; danh sách đầy đủ các máy chủ có sẵn cần phải thực hiện các truy vấn riêng biệt. |
| Tư cách thành viên | Các thông báo dịch vụ đã được gửi và các bản cập nhật dành cho người tham gia. | Vai trò và loại cuộc trò chuyện giới hạn khả năng hiển thị; sự im lặng không đồng nghĩa với sự vắng mặt. |
| Tệp đính kèm | Mô tả phiên bản gốc, số byte đã lưu, SHA-256 và kết quả của các lần thử. | Một tệp đã biến mất có thể không còn khả dụng; phiên bản mới hơn sẽ không thay thế tệp đó. |
| Ảnh chụp lịch sử | Các tin nhắn hiện đang hiển thị, được đánh dấu là các quan sát lịch sử. | Các bản chỉnh sửa trước đó và nội dung đã biến mất sẽ không được khôi phục. |
| Các hành động của chính mình | Đi messages/edits và siêu dữ liệu bàn phím trả lời tương ứng button_press . | Các hàm gọi lại được kích hoạt trên một ứng dụng Telegram khác sẽ không hiển thị. |
| Các nút của bot | Các thông tin về callback, URL, ứng dụng web và siêu dữ liệu yêu cầu được lưu giữ cùng với tin nhắn. | Các URL và phone/location các yêu cầu là văn bản, không được tự động mở hoặc thực thi. |

### Giới hạn tệp đính kèm mặc định

Hình ảnh

20 MiB

Video

100 MiB

Tệp tin

50 MiB

Hiệu ứng động

20 MiB

Ghi chú video

50 MiB

Giọng nói

20 MiB

Âm thanh

50 MiB

Hình dán

5 MiB

**Những điều không thực hiện** Chức năng chuyển đổi không xóa bỏ siêu dữ liệu được nhúng sẵn cũng như không vô hiệu hóa các bản ghi hoạt động. Quá trình ghi lại không xác định danh tính của bất kỳ chủ thể nào mà Telegram không cung cấp.

[Vui lòng đọc chi tiết](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/)

## Hãy sử dụng quyền ủy quyền mà quý vị đang có

Mỗi tài khoản đều có không gian làm việc, nhật ký, khóa ký, tuyến đường và hàng đợi riêng.

### Số điện thoại + mã

Nhập 2FA khi tính năng này được kích hoạt.

### QR mã

Quét từ một thiết bị được ủy quyền; 2FA vẫn có thể được yêu cầu.

### Telethon .session

Nhập tệp phiên làm việc của tài khoản.

### Pyrogram .session

Hãy nhập định dạng phiên Pyrogram được hỗ trợ.

### TData ZIP

Hỗ trợ một tài khoản Desktop; mã thông báo cục bộ nếu đã được thiết lập.

### StringSession text

Dán một Telethon StringSession.

### .session + .json

Vui lòng chọn phiên làm việc và siêu dữ liệu đi kèm tương ứng.

### Khóa xác thực HEX + DC ID

Nhập thông tin ủy quyền tài khoản kèm theo mã định danh trung tâm dữ liệu tương ứng.

**API cặp**

Cặp API là tùy chọn. Nếu không có cặp khóa riêng, TgWitness hệ thống sẽ sử dụng nhóm các cặp công khai, bao gồm cả các cặp từ ứng dụng Telegram Desktop chính thức.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy đang trong giai đoạn thử nghiệm; các danh sách MTProxy . Một tuyến proxy bị lỗi sẽ không chuyển sang kết nối trực tiếp.

Hai không gian làm việc trên cùng một máy tính không được coi là hai nhân chứng độc lập.

**Những điều không thực hiện** Việc nhập dữ liệu không bỏ qua quy trình xác thực của Telegram, 2FA cũng như các định dạng phiên không được hỗ trợ. Các tài khoản vẫn chia sẻ quy trình ứng dụng.

[Các định dạng tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/)

## Thực hiện từ bảng điều khiển

Gửi hoặc trả lời, nhấn vào nút bot hiện tại, lưu bản xem trước liên kết, sau đó tham gia cuộc trò chuyện một cách rõ ràng hoặc khởi chạy bot bằng tham số khởi động của nó.

`interaction.preview``interaction.requested``interaction.result`

Các biên nhận xem trước, yêu cầu và kết quả đều được ký điện tử. Trước khi nhấn nút, máy chủ sẽ truy xuất lại tin nhắn và từ chối bất kỳ thay đổi nào từ bàn phím. Văn bản và các URL được trả về qua hàm callback vẫn được ghi lại trong bối cảnh.

**Những điều không thực hiện** Không hỗ trợ ứng dụng web, thanh toán, phone/location chia sẻ hay truy vấn nội tuyến. Việc hiển thị một URL không đồng nghĩa với việc mở liên kết đó.

[Vui lòng đọc chi tiết](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/)

## Khôi phục và duy trì hoạt động

Các lỗ hổng được hiển thị, không bị che giấu.

### Tiếp tục từ vị trí đã lưu

Sau khi khởi động lại, Telegram sẽ được yêu cầu cập nhật các bản cập nhật bị bỏ lỡ. Thời gian lưu trữ có hạn và các bản cập nhật đã hết hạn có thể để lại những khoảng trống.

### Kiểm tra lại các tin nhắn hiển thị

Giá trị mặc định: các nguồn ưu tiên mỗi 15 phút, các nguồn khác mỗi 6 giờ. Kết quả bao gồm message.recovered và message.missing_on_recheck.

### Đọc coverage.json

Các khoảng thời gian quan sát, các khoảng trống kèm lý do và các ID không được quan sát sẽ đi kèm với tệp xuất đã được ký. Một bản ghi “thiếu khi kiểm tra lại” không phải là thông báo xóa.

**Những điều không thực hiện** Một bản chụp lịch sử sau này sẽ không xóa bỏ sự cố ngừng hoạt động hay khôi phục mọi phiên bản đã biến mất. Vị trí con trỏ được lưu lại không phải là xác nhận không mất mát về việc chấp nhận nhật ký.

[Vui lòng đọc chi tiết](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/)

## Bảy cấp độ. Các câu hỏi khác nhau.

Mỗi cơ chế giải quyết một câu hỏi có giới hạn. Hãy cấu hình các dịch vụ bên ngoài một cách riêng biệt và duy trì các điểm neo tin cậy của chúng bên ngoài bộ thu thập dữ liệu.

1. ### Ghi lại

   SHA-256 chuỗi + Ed25519 cho mỗi sự kiện; giá trị đầu tiên previous_hash là 64 số 0.

   **Kiểm tra của bên thứ ba** Thứ tự và chữ ký được thực hiện dưới khóa thu thập dữ liệu được ghim.

   **Những điều không thực hiện** Điều này không chứng minh nguồn gốc từ Telegram hay tính đầy đủ của dữ liệu.

   **Lệnh xác minh**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Thùng chứa

   manifest.json liệt kê các giá trị băm tệp; manifest.sig ký tên vào tệp đó. media.saved liên kết các byte tệp đính kèm với một sự kiện.

   **Kiểm tra của bên thứ ba** Các tệp được cung cấp phù hợp với bản kê khai đã ký và các biên nhận phương tiện.

   **Những điều không thực hiện** Nó không ký vào CSV, HTML hoặc ảnh chụp màn hình đã tải xuống riêng biệt.

   **Lệnh xác minh**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Giữ nguyên ranh giới

   Tạo điểm kiểm tra khi khởi động, mặc định cứ sau 5 phút một lần, và dừng hoạt động một cách có trật tự. Hãy lưu giữ một bản sao ở nơi khác.

   **Kiểm tra của bên thứ ba** Việc xuất dữ liệu sau này phải phù hợp với độ dài và phần đầu đã được lưu giữ trước đó; việc quay lại phiên bản trước có thể được phát hiện.

   **Những điều không thực hiện** Nó không phát hiện việc thay thế cả nhật ký lẫn tất cả các điểm kiểm tra được lưu giữ.

   **Lệnh xác minh**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### Thời gian bên ngoài

   Chế độ bằng chứng sẽ gửi một điểm kiểm tra SHA-256 đến RFC 3161 các cơ quan chức năng (FreeTSA, DigiCert) và OpenTimestamps lịch.

   **Kiểm tra của bên thứ ba** Một phản hồi TSA đã được xác minh sẽ ghi ngày tháng cho các byte đó; một OpenTimestamps sẽ gắn chúng vào Bitcoin.

   **Những điều không thực hiện** Nó không coi một yêu cầu đã được chuẩn bị sẵn hoặc biên nhận lịch đang chờ xử lý là một dấu thời gian đã được xác nhận.

   **Lệnh xác minh**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Người chứng kiến độc lập

   Tách biệt máy chủ, điểm cuối chỉ đọc có phạm vi giới hạn, thách thức mới, và key/journal và TGW1 các bài đăng trên kênh.

   **Kiểm tra của bên thứ ba** Các phiên bản đầu được chấp nhận trước đó; các trạng thái ok, key_changed, rollback, fork, invalid và no_response.

   **Những điều không thực hiện** Việc này không biến hai không gian làm việc trên cùng một máy chủ thu thập dữ liệu thành các nhân chứng độc lập.

   **Lệnh xác minh**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Bản sao ngoài trang web

   S3 Bản sao tương thích được mã hóa bằng AES-256-GCM; Object Lock khi bucket hỗ trợ tính năng này.

   **Kiểm tra của bên thứ ba** Chức năng khôi phục chỉ xuất bản các tệp sau khi quá trình xác minh nhật ký, điểm kiểm tra và phương tiện được lưu giữ thành công.

   **Những điều không thực hiện** Nó sẽ không khôi phục dữ liệu nếu thiếu khóa đã xuất ra, cũng như không giả định rằng dữ liệu được lưu giữ mà không kiểm tra phản hồi từ bộ nhớ lưu trữ.

   **Lệnh xác minh**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Chạy nguồn gốc

   Biên nhận thực thi đã ký: các hàm băm nguồn, phiên bản phụ thuộc và bối cảnh quá trình. Tự báo cáo.

   **Kiểm tra của bên thứ ba** Những thông tin mà bộ thu thập chữ ký đã báo cáo về quá trình thực thi của chính nó.

   **Những điều không thực hiện** Nó không cung cấp chứng thực quy trình độc lập cũng như không loại trừ khả năng bị xâm phạm trước khi ghi lại.

   **Lệnh xác minh**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### Điều mà không cấp độ nào có thể chứng minh

Việc truyền tải mọi bản cập nhật của Telegram; tính xác thực của văn bản; việc ID người gửi xác định một cá nhân thực sự; việc không có sự xâm phạm đối với người thu thập dữ liệu trước khi ghi lại; tính hợp lệ trước tòa án.

[Người chứng kiến độc lập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/)

Thí nghiệm SHA-256 thí nghiệm

### Hãy thử thay đổi bản ghi số 2

Bản ghi tiếp theo sẽ giữ lại liên kết đã được lưu trước đó. Việc thay đổi nội dung văn bản sẽ làm thay đổi giá trị băm được tính toán của bản ghi số 2.

Nội dung bản ghi số 2

Bản ghi 1`h1`Bắt đầu bằng 64 số 0

Bản ghi 2`h2`Bao gồm các bản lưu h1

Bản ghi số 3`h3`Bao gồm các bản lưu h2

Ví dụ tĩnh: h2 bao gồm nội dung “Gặp nhau lúc 11:00”. Việc thay đổi văn bản đó sẽ làm thay đổi h2; bản ghi số 3 vẫn tham chiếu đến nội dung đã lưu h2.

**Kiểm tra toàn bộ các bản tóm tắt**

Bản ghi đã lưu 2 băm

`SHA-256(e₂)`

Băm của bản ghi số 2 đã được tính lại

`SHA-256(e₂)`

Ví dụ này tính toán các giá trị băm, không phải chữ ký. Trình xác minh thực tế sẽ đối chiếu từng chữ ký và liên kết với khóa đáng tin cậy.

 [Vui lòng đọc chi tiết](https://phishdestroy.github.io/TgWitness/vi/docs/reference/how-it-works/)

## Hãy lựa chọn một lộ trình thông qua các bằng chứng

Các tình huống giả định. Hãy bắt đầu thu thập dữ liệu trước khi sự kiện liên quan xảy ra; hãy giữ nguyên các ranh giới và khoảng trống cùng với nội dung.

### Một kênh thay đổi thông tin thanh toán

Chế độ → sự kiện

Các cuộc trò chuyện đã chọn → tin nhắn, chỉnh sửa, xóa.

Kết quả đầu ra

Các phiên bản bài đăng và tệp đính kèm được quan sát thông qua mã băm.

Xác minh

Đã ký ZIP + điểm kiểm tra được lưu giữ + phản hồi TSA đã được xác minh.

**Những điều không thực hiện** Nó không khôi phục bản gốc chưa từng được ghi lại.

### Các tin nhắn sẽ biến mất sau khi xảy ra sự cố

Chế độ → sự kiện

Thư mục hoặc toàn bộ tài khoản → tất cả các danh mục sự kiện.

Kết quả đầu ra

Các bản gốc đã lưu trữ, thông báo xóa và phạm vi bao phủ có khoảng trống.

Xác minh

Đã ký ZIP + nhật ký chứng kiến độc lập.

**Những điều không thực hiện** Nó không xác định được người xóa từ một thông báo không cung cấp thông tin về chủ thể thực hiện.

### Tìm hiểu về bot cửa hàng

Chế độ → sự kiện

Cài đặt sẵn cho chế độ điều tra → các nút, bản xem trước liên kết và khởi động bot rõ ràng.

Kết quả đầu ra

Biên nhận tương tác đã ký, các hàm gọi lại được trả về và các hồ sơ đã lưu.

Xác minh

Đã ký ZIP; hãy xác minh bất kỳ hồ sơ nào so với ZIP.

**Những điều không thực hiện** Nó không mở ứng dụng web của bot, không thực hiện thanh toán cũng như không ghi lại các sự kiện gọi lại (callback) của khách hàng khác.

### Một người tham gia có thể thay đổi tên trong các cuộc trò chuyện

Chế độ → sự kiện

Bất kỳ phạm vi nào → dữ liệu sender/profile dữ liệu siêu dữ liệu.

Kết quả đầu ra

Lịch sử tên/tên người dùng theo ID số, các liên kết “cũng có trong” và các manh mối được trích xuất.

Xác minh

Hồ sơ JSON đã được đối chiếu với bản đã ký ZIP.

**Những điều không thực hiện** Nó không biến ví, chuỗi ký tự giống số điện thoại hoặc tên người dùng thành danh tính đã được chứng minh.

### Hoạt động quan sát dài hạn với bản sao lưu trữ ngoài hệ thống

Chế độ → sự kiện

Bất kỳ phạm vi nào → Chế độ Bằng chứng và một S3 bản sao được hỗ trợ Object Lock.

Kết quả đầu ra

Bản sao được mã hóa, các điểm kiểm tra được lưu giữ và các phản hồi có dấu thời gian.

Xác minh

Hãy khôi phục bằng khóa đã xuất, sau đó xác minh mà không cần đến máy chủ gốc.

**Những điều không thực hiện** Tài liệu này không thay thế cho một nhân chứng độc lập hoặc một khóa giải mã được lưu giữ riêng biệt.

[Vui lòng đọc chi tiết](https://phishdestroy.github.io/TgWitness/vi/docs/reference/investigation/)

## Chuyển giao một gói phần mềm có thể kiểm tra được

Vui lòng cung cấp bản gốc đã được ký, dấu vân tay khóa được lưu giữ độc lập, điểm kiểm tra liên quan và kết quả xác minh.

- Đã ký ZIP
- JSONL
- CSV
- HTML
- Điểm kiểm tra
- Chứng từ xác nhận
- Xuất dữ liệu trò chuyện: chat.json / chat.html
- Hồ sơ JSON
- Được bảo vệ bằng mật khẩu AES-256 ZIP
- Tách riêng các tệp xuất cho nhiều tài khoản
- CLI truyền trực tuyến: 5 GiB giới hạn mặc định

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Vui lòng lấy trình xác minh từ một bản sao đáng tin cậy, chứ không phải từ kho lưu trữ đang được kiểm tra.

**Những điều không thực hiện** Độc lập CSV và HTML không phải là các vùng chứa được ký. Mật khẩu bảo vệ tính bảo mật của quá trình truyền tải, chứ không phải tính xác thực. Việc xuất nhiều lần sẽ không hợp nhất các nhật ký tài khoản.

[Vui lòng đọc chi tiết](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/)

## So sánh với sản phẩm đã được cung cấp

Các thành phần cơ bản không có thêm hệ thống ký tên, đóng dấu thời gian hoặc hệ thống nhân chứng. Các tập lệnh và trình ghi nhật ký khác nhau tùy theo cách triển khai; “một phần” có nghĩa là giới hạn trong các tài liệu được ghi lại hoặc hiển thị.

| Cách tiếp cận | Chỉnh sửa / xóa bỏ | Ghi lại chữ ký | Thời gian bên ngoài | Người chứng kiến độc lập | Phạm vi bao phủ / những khoảng trống | Xác minh mà không cần tác giả |
| --- | --- | --- | --- | --- | --- | --- |
| Xuất dữ liệu từ Telegram Desktop | Một phần | Không | Không | Không | Không | Không |
| Telethon tập lệnh chụp nhanh | Một phần | Không | Không | Không | Không | Không |
| Trình ghi nhật ký xóa: nhật ký văn bản | Một phần | Không | Không | Không | Không | Không |
| Ảnh chụp màn hình / ảnh chụp trang web | Một phần | Không | Không | Không | Không | Không |
| TgWitness với các tùy chọn bổ sung đã được cấu hình | Một phần | Có | Có | Có | Một phần | Có |

**Những điều không thực hiện** Bảng này không đánh giá mọi tập lệnh hay sản phẩm ghi nhật ký. Các kiểm tra thời gian và nhân chứng tùy chọn đòi hỏi các dịch vụ và mốc tin cậy riêng; không có kiểm tra nào xác lập được sự thật nguồn gốc.

[Vui lòng đọc chi tiết](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/)

## Hãy giữ nguyên các giới hạn cùng với bằng chứng

Việc xác minh sẽ hữu ích khi phạm vi của nó được xác định rõ ràng.

- Các cuộc trò chuyện bí mật hiện không khả dụng.
- Không có dữ liệu nào được ghi lại khi quá trình bị dừng; khả năng khôi phục bị giới hạn.
- Một bản ghi đã được xác minh không phải là bằng chứng cho thấy nội dung của nó là đúng sự thật.
- Một nhà điều hành sở hữu khóa có thể ký vào bất kỳ nội dung nào. Các nhân chứng độc lập và dấu thời gian hạn chế việc thay thế sau này, chứ không phải việc thu thập ban đầu không trung thực.
- Hãy sử dụng một tài khoản chuyên dụng, không phải tài khoản chính của quý vị.
- Telegram có thể hạn chế các tài khoản do khối lượng yêu cầu quá lớn.

**Những điều không thực hiện** Không có chế độ hay mức độ bằng chứng nào xác lập tính hợp lệ về mặt pháp lý, việc gửi tin nhắn Telegram hoàn tất hay danh tính trong thế giới thực.

[Hướng dẫn thiết lập](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=vi)[Tài khoản chuyên dụng](https://phishdestroy.github.io/TgWitness/vi/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/investigation/)
