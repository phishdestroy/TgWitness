# Lưu trữ và khôi phục

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/storage/

Sao lưu, di chuyển các tệp cũ lên đám mây của bạn, các bản sao được bảo vệ bởi Object Lock và khôi phục trên máy mới.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/vi/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Bảng điều khiển này phân chia thành ba tác vụ:

| Nhiệm vụ | Chức năng |
| --- | --- |
| Lưu bản sao lưu | Sao chép nhật ký đã được ký, các điểm kiểm tra, các tệp đã được lưu giữ và các bản xuất đang chờ xử lý vào đích S3 đã được cấu hình. |
| Dung lượng lưu trữ cục bộ miễn phí | Sao chép các tệp đính kèm cũ đã chọn vào S3 hoặc một máy chủ đám mây từ xa rclone, đọc lại toàn bộ nội dung, xác minh các byte được mã hóa, sau đó xóa bản sao cục bộ đã được xác minh. |
| Lưu giữ bản sao làm bằng chứng | Cấu hình S3 Object Lock và kiểm tra trạng thái lưu trữ được trả về. Dịch vụ phải xác nhận chế độ và ngày tháng được yêu cầu. |

Việc giải phóng dung lượng không bao giờ xóa hoặc ghi đè lên nhật ký đã được ký. Mỗi tệp đính kèm giữ lại SHA-256 gốc và một biên nhận khôi phục. Nén gzip tùy chọn được thực hiện trước khi mã hóa được xác thực. Tên tệp trên đám mây không chứa tên Telegram, ID cuộc trò chuyện hoặc tên tệp đính kèm gốc. Một tệp đính kèm có thể có dung lượng tối đa 32 GiB.

Chỉ riêng phản hồi tải lên không phải là quyền xóa tệp. TgWitness tải xuống toàn bộ đối tượng được mã hóa và xác minh kích thước của nó, SHA-256 lưu biên nhận, sau đó kiểm tra lại các byte cục bộ ngay trước khi xóa. Nếu việc tải lên thất bại, kết quả đọc lại khác hoặc quá trình truyền tải bị hủy, tệp cục bộ sẽ vẫn được giữ nguyên. Nếu bản sao lưu bằng chứng đã được kích hoạt chưa sao chép tệp đó, quá trình xóa cũng sẽ chờ cho đến khi bản sao lưu hoàn tất.

**On this page**

- [When the disk is filling up](https://phishdestroy.github.io/TgWitness/vi/docs/reference/storage/#when-the-disk-is-filling-up)
- [Connect a destination](https://phishdestroy.github.io/TgWitness/vi/docs/reference/storage/#connect-a-destination)
- [Keep the recovery file](https://phishdestroy.github.io/TgWitness/vi/docs/reference/storage/#keep-the-recovery-file)
- [Recover after losing the installation](https://phishdestroy.github.io/TgWitness/vi/docs/reference/storage/#recover-after-losing-the-installation)
- [Operator bot and completion notices](https://phishdestroy.github.io/TgWitness/vi/docs/reference/storage/#operator-bot-and-completion-notices)

## Khi ổ đĩa sắp đầy

Tải tệp đính kèm tạm dừng khi dung lượng trống thấp hơn mức **Tham số → Tệp đính kèm → dung lượng đĩa trống** (mặc định 1 GiB), vẫn giữ hàng đợi. Quan sát văn bản tiếp tục. Điều này độc lập với thông báo: tắt thông báo không tắt dung lượng dự phòng tải xuống hay các biện pháp bảo vệ lưu trữ.

Để can thiệp sớm hơn, bật **Chạy tự động**, chọn **Xóa tệp cục bộ để giải phóng dung lượng** và bật **Chạy thêm một lượt chuyển khi ổ đĩa ít chỗ trống**. Mặc định, quy tắc tùy chọn bắt đầu dưới 5120 MiB trống và xử lý từng lô đến khi trống 10240 MiB. Cả hai ngưỡng đều cấu hình được. Nó dùng cùng đích, tuổi tệp tối thiểu, giới hạn lô, kiểm tra đọc lại toàn bộ và điều kiện sao lưu bằng chứng như lượt chạy thủ công; không tự bật đích. Kiểm tra mỗi 30 giây; lỗi hoặc không tiến triển sẽ lùi lần thử tiếp theo năm phút. Trạng thái và thời điểm thử lại vẫn được giữ sau khởi động lại. Khi quy tắc không hoạt động, các lượt theo lịch dùng khoảng thời gian thông thường.

Bảng điều khiển hiển thị dung lượng trống, dự phòng đóng gói, trạng thái sẵn sàng của quy tắc và tệp bị bỏ qua vì thiếu chỗ tạm. Đóng gói và khôi phục kiểm tra nhu cầu chỗ tạm tối đa trước khi bắt đầu và dung lượng còn trống trong lúc ghi. Dùng mức dự phòng tải xuống đã cấu hình, nhưng tối thiểu 64 MiB cho thao tác lưu trữ. Đây không phải hạn ngạch hệ thống tệp; tiến trình khác vẫn có thể dùng dung lượng giữa các lần kiểm tra.

Gzip nén không mất dữ liệu các đối tượng từ xa; không thu nhỏ nhật ký đang dùng hay tạo kho nén cục bộ. JPEG, video và ZIP có thể hầu như không nhỏ đi hoặc hơi lớn hơn. Khi bật nén, đóng gói có thể tạm cần khoảng hai lần kích thước tệp đính kèm cộng dung lượng dự phòng. Chọn ngưỡng bắt đầu đủ sớm cho tệp lớn nhất. Tệp quá lớn được giữ và báo cáo; tệp nhỏ hơn cùng bản sao từ xa đã xác minh vẫn có thể giải phóng chỗ. Có bản sao đã xác minh thì có thể bỏ tệp cục bộ mà không tạo thêm tệp đóng gói. Khôi phục cũng cần chỗ tạm và có thể bị từ chối đến khi đủ dung lượng.

Nếu không có tệp đủ điều kiện chuyển hoặc chưa cấu hình đích, TgWitness không thể tự giải phóng dung lượng. Quản lý lưu trữ không bao giờ cắt bớt hay viết lại nhật ký đã ký. Nhật ký vẫn cần chỗ cho quan sát văn bản mới.

## Kết nối đích

Trong **Extras → Storage & disk space → Manage storage**, chọn tác vụ và đích đến, lưu lại, sau đó chọn **Test upload & download**. Thao tác thử nghiệm này sẽ tải lên một đoạn dữ liệu ngẫu nhiên nhỏ và đọc lại nó. Thao tác này không sử dụng nội dung từ Telegram.

Đối với S3, hãy sử dụng điểm cuối, khu vực và bucket thực tế của nhà cung cấp. Wasabi, Backblaze, Cloudflare R2 và các dịch vụ tương thích khác sử dụng cùng các cài đặt S3. Một API tương thích không tự động đồng nghĩa với việc hỗ trợ Object Lock. Chế độ Quản trị có thể cho phép quản trị viên được ủy quyền bỏ qua thời gian lưu trữ; Chế độ Tuân thủ có các hạn chế khác nhau. Hãy kiểm tra trạng thái Object Lock được trả về trước khi dựa vào thời gian lưu trữ.

Đối với đích rclone, hãy tạo một máy chủ từ xa bằng cách thiết lập nhà cung cấp của rclone và dán phần `[name]` vào bảng điều khiển. Trợ lý đã cài đặt hỗ trợ MEGA, Google Drive, OneDrive, Dropbox, Box, pCloud và các nhà cung cấp khác được hiển thị trong bộ chọn. Thông tin đăng nhập được lưu trong kho lưu trữ được mã hóa của không gian làm việc này. Các lần làm mới OAuth được lưu trở lại vào kho lưu trữ. Thông tin đăng nhập không được thêm vào các sự kiện nhật ký hoặc bao gồm trong các bản tải xuống phục hồi.

Trợ lý được cài đặt bên trong không gian làm việc, với phiên bản được ghim và SHA-256. Nó không được thêm vào đường dẫn PATH của hệ thống. Các tệp cấu hình và tệp làm việc là các tệp tạm thời trong không gian làm việc đó. Các kết nối từ xa dựa trên lệnh và tệp cục bộ bị từ chối. Hiện tại, rclone yêu cầu phải chọn rõ ràng đường dẫn **Direct** cho các yêu cầu bên ngoài. Sử dụng bộ lưu trữ S3 gốc cho đường dẫn SOCKS5 hoặc HTTP của không gian làm việc; rclone sẽ không tự động bỏ qua một đường dẫn không khả dụng.

## Lưu giữ tệp khôi phục

Chọn **“Lưu tệp khôi phục”** sau khi sao chép tệp và lưu trữ nó ở một nơi riêng biệt với thư mục cài đặt. Tệp này chứa khóa giải mã và các biên lai đối tượng đã được ký, vì vậy hãy coi nó như bản sao lưu khóa riêng tư. Hãy lưu trữ cấu hình từ xa gốc và thông tin đăng nhập đích riêng biệt. Một tệp khôi phục được tạo trước khi thực hiện bản sao sau đó sẽ không chứa biên lai của tệp đó.

Dấu vân tay của khóa ký nên đã được ghi lại độc lập từ trước. Một chữ ký chỉ được kiểm tra so với khóa được cung cấp trong cùng một tệp không thể xác định được đó là tệp khôi phục của ai.

Để khôi phục các biên lai lưu trữ bị thiếu trong một không gian làm việc hiện có, hãy mở **“Khôi phục tệp” từ tệp khôi phục đã lưu** và chọn tệp đó. Bảng điều khiển sẽ kiểm tra chữ ký và yêu cầu cùng một khóa ký của không gian làm việc. Hệ thống sẽ từ chối thay thế bằng một khóa lưu trữ khác. Sau đó, chọn **“Khôi phục tất cả tệp**”. Quá trình khôi phục sẽ tạm dừng quy tắc lưu trữ tự động để lần quét theo lịch trình tiếp theo không thể xóa ngay lập tức các tệp đã được khôi phục. Hãy kích hoạt lại quy tắc khi đã hoàn tất việc sử dụng các bản sao cục bộ.

Quá trình khôi phục xác minh văn bản mã hóa, xác thực quá trình giải mã, giải nén nếu cần thiết và kiểm tra văn bản thuần gốc SHA-256 trước khi đặt tệp vào `media/`. Một đối tượng từ xa bị hỏng sẽ không bao giờ thay thế tệp cục bộ. Một tệp cục bộ hiện có với các byte khác biệt sẽ được giữ lại để xem xét thay vì bị ghi đè.

## Khôi phục sau khi mất bản cài đặt

Cài đặt TgWitness trên một máy khác. Sử dụng tệp khôi phục riêng tư, dấu vân tay được ghi lại riêng biệt và thông tin đăng nhập đích ban đầu:

```
python -m tgwitness.storage recover \
  --recovery storage-recovery.json \
  --fingerprint TRUSTED_WORKSPACE_SHA256 \
  --credentials original-rclone.conf \
  --output recovered-attachments
```

Đối với S3, `--credentials` trỏ đến một tệp JSON riêng tư với `access_key` và `secret_key`; tệp khôi phục đã được ký cung cấp các cài đặt đích. Lệnh này sử dụng kết nối bên ngoài trực tiếp và tải xuống trình trợ giúp được ghim khi một máy chủ từ xa rclone cần nó. Nó từ chối thư mục đầu ra hiện có.

Các byte gốc đã khôi phục được ghi vào `recovered-attachments/media/`, được đặt tên theo SHA-256 của chúng. `recovery-log.jsonl` là bản ghi không có chữ ký về các thao tác khôi phục. Lệnh này không tạo lại nhật ký đã mất có chữ ký hoặc khóa ký của nó. Hãy giữ một bản sao lưu đầy đủ không gian làm việc cho những dữ liệu đó. Tệp khôi phục lưu trữ không phải là bản sao lưu đầy đủ của không gian làm việc.

## Bot điều hành và thông báo hoàn thành

Bot Telegram thuộc sở hữu của người vận hành. Tạo bot thông qua BotFather và thiết lập mã thông báo (token), phòng chat đích và danh sách ID người dùng Telegram được phép cụ thể trong bảng điều khiển. Cả người gửi và phòng chat đều phải trùng khớp. Các tin nhắn được chuyển tiếp và lệnh từ các bot khác sẽ bị bỏ qua.

`/status` và `/stats` có sẵn ở chế độ mặc định chỉ hiển thị trạng thái. Chế độ điều khiển tùy chọn thêm `/pause`, `/resume` và `/copy`. `/copy` yêu cầu tác vụ lưu trữ đã được cấu hình; điều này không có nghĩa là quá trình tải lên từ xa đã hoàn tất. Các lệnh không thể cung cấp các URL, tệp hoặc chương trình shell tùy ý.

Sử dụng các cài đặt thông báo riêng biệt cho cảnh báo và hoàn thành tác vụ. Thông báo hoàn thành phân biệt việc xuất tài khoản có thiếu sót với việc xuất đầy đủ, đồng thời hiển thị lịch sử và số lượng lưu trữ. Các đoạn trích tin nhắn sẽ không được bao gồm trừ khi được kích hoạt riêng trong cài đặt thông báo. Trình chọn dịch vụ được tạo ra từ danh mục Apprise đã cài đặt thực tế thay vì một tập hợp cố định các ví dụ về nhà cung cấp.
