# Kết nối, máy chủ trung gian và bảo vệ dữ liệu

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/

Xác thực, nhóm proxy tự động, chế độ IP, chính sách dự phòng, yêu cầu bên ngoài và lưu trữ khóa bí mật.

Tài liệu này mô tả cách thức hoạt động và các giới hạn của TgWitness phiên bản 0.7.1. Quá trình xác thực, quyền truy cập nguồn, kết nối mạng và tính đầy đủ của dữ liệu thu thập là các trạng thái độc lập. Để tìm hiểu về các bước đăng nhập, định dạng tệp và quản lý nhiều tài khoản, quý vị hãy bắt đầu từ phần [“Tài khoản và định dạng phiên làm việc](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/)”. Đối với chính sách sự kiện và hành vi khởi động lại, xin vui lòng tham khảo phần [“Cách thức thu thập dữ liệu hoạt động](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/)”.

## Các phương thức xác thực

**ID API và mã băm API dùng để xác định một ứng dụng; chúng không thay thế cho thông tin đăng nhập tài khoản.** Chúng là tùy chọn trong TgWitness. Thứ tự ưu tiên: cặp được nhập vào biểu mẫu, tiếp theo là cặp từ tệp JSON tài khoản đã nhập, sau đó là cặp được lưu trong không gian làm việc, và cuối cùng là nhóm 50 cặp công khai, được thử theo thứ tự ngẫu nhiên với cơ chế luân phiên tự động khi Telegram từ chối một cặp. Chỉ có cặp Telegram Desktop (2040) mới được gửi kèm theo mô tả ứng dụng Telegram Desktop tương ứng. Cặp thông tin của riêng quý vị từ Công cụ Phát triển API tại [my.telegram.org](https://my.telegram.org) có thể được sử dụng cho tất cả các tài khoản của quý vị; mỗi tài khoản vẫn có quyền ủy quyền riêng.

| Phương pháp | Yêu cầu | Hỗ trợ TgWitness |
| --- | --- | --- |
| Số điện thoại, mã xác thực, xác thực hai yếu tố (2FA) tùy chọn | Quyền truy cập tài khoản; cặp API là tùy chọn | Đăng nhập vào bảng điều khiển |
| Mã xác thực HEX + ID DC | Khóa đầy đủ 512 ký tự và DC 1–5 | Tab **“Khóa xác thực** trực tiếp”; tùy chọn kiểm tra ID người dùng trước khi lưu thông tin xác thực |
| Telethon StringSession | Một chuỗi phiên làm việc hợp lệ | Đăng nhập vào bảng điều khiển |
| Telethon SQLite `.session` | Nội dung hoàn chỉnh, nhất quán | Tính năng nhập trực tiếp các lược đồ qua bảng điều khiển 7/8; tùy chọn sử dụng CLI ngoại tuyến |
| Pyrogram SQLite `.session` | Phiên làm việc của người dùng trong môi trường sản xuất đã đóng | Nhập trực tiếp các lược đồ từ bảng điều khiển 2/3 |
| Tệp ZIP TData của Telegram Desktop | Một tài khoản hiện đại; mã PIN cục bộ nếu được bảo vệ | Chuyển đổi trong bộ nhớ kèm theo các kiểm tra tổng kiểm tra (checksum) và giải mã |
| Tệp JSON tài khoản | Các trường API/phiên làm việc/khóa được hỗ trợ | Chỉ riêng siêu dữ liệu đã đủ để điền thông tin đăng nhập API; tuy nhiên, vẫn cần phải đăng nhập bằng phiên/khóa hoặc số điện thoại/mã QR |
| Đăng nhập bằng mã QR | Xác nhận từ ứng dụng Telegram được ủy quyền | Tạo mã QR cục bộ, thiết lập thời hạn hiệu lực/thử lại, tùy chọn xác thực hai yếu tố (2FA) |
| TDLib / Pyrogram StringSession | Các định dạng khác dành riêng cho thư viện | Không được hỗ trợ |
| Mã thông báo bot | Một bot có mô hình truy cập/cập nhật riêng | Không được sử dụng bởi người thu thập này |

Telegram lựa chọn phương thức gửi mã xác thực; việc gửi qua SMS không được đảm bảo. Mã băm API không thể khôi phục một phiên đã bị thu hồi hoặc thay thế mật khẩu 2FA đã bị quên. TgWitness không lưu trữ mã đăng nhập hoặc mật khẩu 2FA của Telegram trên đĩa cứng.

Đối với nguồn tin riêng tư, tài khoản đó phải đã có quyền truy cập. Tên người dùng nhóm là không cần thiết. Việc sử dụng proxy hoặc nhập phiên làm việc sẽ không cấp quyền thành viên cũng như quyền quản trị viên. Việc hiện đang là thành viên không đảm bảo quyền truy cập vào lịch sử trước khi tham gia.

## Nhập tệp phiên làm việc Telethon

Telethon SQLite, Pyrogram SQLite và Telegram Desktop TData sử dụng các định dạng khác nhau. Bảng điều khiển sẽ phát hiện và chuyển đổi các cấu trúc được hỗ trợ; việc đổi tên tệp không được coi là quá trình chuyển đổi. Vui lòng chọn một phiên và tệp JSON đi kèm trong mục **Tệp**, sau đó nhấn **Kết nối tài khoản**. Hệ thống chấp nhận tối đa bốn tệp khớp và tổng dung lượng tối đa là 8 MiB. Vui lòng tham khảo [giới hạn định dạng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/) để biết chi tiết về TData/JSON. Không có tính năng khôi phục mật mã. Đăng nhập qua điện thoại/2FA hoặc mã QR sẽ tạo ra một quyền truy cập riêng biệt.

Đường dẫn dòng lệnh tùy chọn dành riêng cho Telethon vẫn có sẵn:

1. Hãy ngừng sử dụng phiên làm việc gốc trên ứng dụng khách và tạo một bản sao nhất quán. Trình chuyển đổi sẽ từ chối các tệp có nhật ký WAL/journal chưa hoàn tất. Vui lòng đóng ứng dụng khách gốc một cách đúng quy trình thay vì xóa các tệp đó để né tránh quá trình kiểm tra.
2. Từ môi trường TgWitness, hãy thực thi lệnh:

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. Tại mục **Thêm tài khoản → Tệp**, hãy tải lên kết quả hoặc dán chuỗi ký tự của nó, sau đó tiếp tục.
2. Vui lòng kiểm tra ID tài khoản số được hiển thị, chọn các nguồn và bắt đầu quá trình theo dõi.

Trình chuyển đổi mở SQLite ở chế độ chỉ đọc, không thực hiện nâng cấp lược đồ hay yêu cầu mạng, và không in ra phiên làm việc. Trình này kiểm tra phiên bản lược đồ, các loại bảng, một hàng phiên làm việc, IP/cổng/DC và độ dài khóa. Dữ liệu đầu vào CLI bị giới hạn ở 64 MiB; văn bản StringSession bị giới hạn ở 4 KiB. Quá trình chuyển đổi trên bảng điều khiển sẽ tải các tệp lên máy chủ TgWitness đã được xác thực, xử lý chúng trong bộ nhớ và trả về thông tin xác thực đã được chuẩn hóa cho trình duyệt đó mà không lưu lại các tệp gốc đã tải lên. Vui lòng sử dụng HTTPS khi kết nối với máy chủ từ xa.

**Tệp đã chuyển đổi là một khóa truy cập tài khoản chưa được mã hóa.** Hãy lưu giữ nó trong kho lưu trữ được bảo vệ và tuyệt đối không được đưa vào kho lưu trữ chung hay gửi cho bất kỳ dịch vụ chuyển đổi bên thứ ba nào. TgWitness lưu trữ phiên đăng nhập được ủy quyền trong kho lưu trữ được mã hóa của mình. Việc sao chép một phiên đăng nhập sẽ không tạo ra một ủy quyền riêng biệt: xin đừng chạy các ứng dụng khách đồng thời với các khóa xác thực đã được sao chép và cho rằng các bản cập nhật sẽ được phân phối độc lập.

Quá trình chuyển đổi chỉ chuyển giao quyền truy cập, chứ không chuyển các tin nhắn gốc, bộ nhớ đệm của thực thể hay con trỏ cập nhật bền vững. Quá trình này không đảm bảo khả năng khôi phục cập nhật sau khi khởi động lại quy trình.

## MTProto, Telethon và các máy chủ proxy

MTProto là giao thức của Telegram. Telethon là thư viện khách hàng Python mà TgWitness sử dụng. MTProxy là một proxy truyền tải Telegram; SOCKS5 và HTTP CONNECT cung cấp các đường hầm chung. Không có phương thức nào thay thế cho việc xác thực tài khoản.

Vui lòng lưu đường dẫn kết nối cho từng không gian làm việc tại **Tài khoản → Cài đặt → Cài đặt kết nối → Thay đổi đường dẫn kết nối** trước khi đăng nhập. Các không gian làm việc mới sẽ được đặt mặc định là **MTProxy Tự động · danh sách công khai** với chế độ Ẩn địa chỉ IP. Các không gian làm việc hiện có đã sử dụng chế độ Trực tiếp một cách rõ ràng sẽ vẫn giữ chế độ cho phép điều này.

## Các chế độ IP

Tùy chọn đường dẫn sẽ quyết định kết nối. Chế độ IP xác định thời điểm địa chỉ máy chủ có thể bị lộ. Các thiết lập này không cài đặt VPN cũng như không định tuyến toàn bộ lưu lượng truy cập của máy.

| Chế độ | Telegram | Yêu cầu từ bên ngoài |
| --- | --- | --- |
| Hide IP (`hide`) | Vui lòng sử dụng máy chủ proxy; nếu không có máy chủ nào hoạt động, xin vui lòng chờ đợi. Không có phương án dự phòng trực tiếp. | Yêu cầu sử dụng SOCKS5/HTTP; từ chối các yêu cầu không có proxy phù hợp. |
| Cho phép sử dụng phương án dự phòng (`fallback`) | MTProxy tự động có thể sử dụng kết nối trực tiếp (Direct) sau khoảng thời gian trễ đã được cấu hình, sau đó quay trở lại sử dụng proxy đang hoạt động. | Ưu tiên sử dụng proxy bên ngoài đã được cấu hình hoặc tuyến SOCKS5/HTTP của tài khoản; nếu không, có thể sử dụng chế độ Trực tiếp. |
| Tunnel / VPN (`tunnel`) | Các đường dẫn trực tiếp và cơ chế chuyển hướng tự động sang nhóm dự phòng ngay lập tức đều được phép. | Việc kết nối trực tiếp được phép khi không có máy chủ trung gian nào được cấu hình. |

Chế độ Tunnel/VPN giả định rằng quý vị quản lý mạng đó một cách riêng biệt. Nếu không có đường hầm hoạt động, các điểm đích có thể nhìn thấy địa chỉ của chính máy chủ. Vui lòng chọn chế độ phù hợp với mạng thực tế của quý vị, chứ không phải dựa trên tên của tùy chọn.

### Chọn một lộ trình

| Lộ trình | Cài đặt | Phạm vi |
| --- | --- | --- |
| MTProxy tự động | Các danh sách tích hợp sẵn hoặc danh mục toán tử | Luôn duy trì một tuyến kết nối Telegram hoạt động; phương án dự phòng trực tiếp phụ thuộc vào chế độ IP |
| Trực tiếp | Chế độ Tunnel/VPN | Telethon sử dụng tuyến mạng của nhà cung cấp dịch vụ |
| SOCKS5 | Máy chủ, cổng, tên người dùng/mật khẩu (tùy chọn) | python-socks, đã kích hoạt tính năng DNS đích từ xa |
| HTTP CONNECT | Máy chủ, cổng, tên người dùng/mật khẩu (tùy chọn) | Sử dụng kết nối HTTP CONNECT thuần túy; giao thức TLS đến chính máy chủ proxy chưa được triển khai |
| MTProxy | Máy chủ, cổng, khóa bí mật | Phương thức truyền tải Telethon thử nghiệm; 32 chữ số thập lục phân hoặc `dd` + 32 chữ số thập lục phân |

Các khóa bí mật TLS giả mạo `ee` sẽ bị từ chối. Tính năng chuẩn hóa của Telethon 1.45 có thể loại bỏ tiền tố và tên miền, nhưng tính năng này không hỗ trợ TLS giả mạo. Vui lòng dán `tg://proxy?server=…&port=…&secret=…` hoặc `https://t.me/proxy?server=…&port=…&secret=…` và chọn **“Điền trường từ liên kết**”. Thao tác này sẽ xác thực và điền thông tin vào các trường mà không cần kết nối hay lưu lại; quý vị hãy kiểm tra và lưu đường dẫn đó riêng biệt. Các trường nhập liệu thủ công vẫn có sẵn. Vui lòng tham khảo [các liên kết proxy Telegram](https://core.telegram.org/api/links#proxy-links).

### Các máy chủ proxy công cộng do hệ thống cài đặt của quý vị cung cấp

Danh sách tích hợp sẵn kết hợp bốn nguồn: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) và [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). Bản chụp nhanh đi kèm chứa thông tin về điểm cuối, nguồn gốc và ngày tải xuống. Việc một nhà cung cấp được liệt kê trong danh sách này không phải là bằng chứng cho thấy máy chủ proxy đó hoạt động hoặc cung cấp mọi bản cập nhật của Telegram.

**MTProxy tự động** kiểm tra kết nối truyền tải của Telegram, duy trì một proxy đang hoạt động và chuyển sang proxy khác khi proxy đó gặp sự cố. Các không gian làm việc ưu tiên sử dụng các proxy khác nhau khi có đủ các mục proxy đang hoạt động; địa chỉ thoát duy nhất không được đảm bảo. Các proxy gặp sự cố sẽ tạm ngưng hoạt động trước khi thực hiện lần thử tiếp theo. Nếu không có proxy nào hoạt động, chế độ IP sẽ xác định liệu việc thu thập dữ liệu phải chờ đợi hay có thể sử dụng kết nối trực tiếp. Việc thay đổi proxy không làm thay đổi tài khoản hay xóa sổ nhật ký của tài khoản đó. Các lựa chọn và thay đổi về đường dẫn được ghi lại trong sổ nhật ký đã được ký điện tử.

Khi các tuyến tự động đang hoạt động, danh sách sẽ được làm mới mỗi giờ và các kiểm tra truyền tải được thực hiện mỗi mười phút theo mặc định. Các khoảng thời gian này có thể tùy chỉnh. **Việc cập nhật danh sách công khai** sẽ yêu cầu làm mới; chỉ xem danh sách sẽ không thay đổi tuyến thủ công đã lưu.

Mỗi phản hồi nguồn cấp dữ liệu bị giới hạn ở mức 1 MiB với thời gian chờ yêu cầu là tám giây và thời hạn tải xuống tổng cộng là 20 giây; các liên kết chuyển hướng sẽ bị từ chối. Tối đa 64 mục tương thích từ mỗi nguồn sẽ được lưu giữ và loại bỏ trùng lặp. Trình phân tích cú pháp chấp nhận các khóa bí mật dạng thập lục phân và base64url được hỗ trợ cũng như nguồn cấp dữ liệu JSON. Các TLS giả mạo `ee`, liên kết không hợp lệ, các địa chỉ IP riêng/dành riêng dưới dạng văn bản và tên máy chủ cục bộ sẽ bị bỏ qua. Tên máy chủ được giải quyết và kiểm tra trước khi sử dụng, đồng thời địa chỉ IP đã chọn sẽ được cố định cho kết nối đó. Quá trình thu thập lại tự động sẽ giải quyết lại tên máy chủ; hãy áp dụng lại một mục nhập thủ công để giải quyết lại tên máy chủ đó.

Các phản hồi nguồn cấp dữ liệu không thành công, trống hoặc không tương thích sẽ vẫn giữ lại bản chụp nhanh nguồn trước đó. Các bản cập nhật là nguyên tử, được tuần tự hóa và giới hạn ở một lần thử mỗi phút cho mỗi không gian làm việc. Một lần kiểm tra truyền tải thành công chỉ xác nhận kết nối, chứ không đảm bảo tính ẩn danh hay tính đầy đủ của dữ liệu được thu thập.

**Lưu lượng Telegram và các yêu cầu HTTPS sử dụng các tuyến đường khác nhau.** Việc tải xuống danh sách sử dụng một kết nối HTTPS riêng biệt và tuyến đường yêu cầu bên ngoài được cung cấp. Phiên bản `TGWITNESS_PROXY_FEED_PROXY` sẽ ghi đè rõ ràng tuyến đường đó bằng một proxy HTTP/SOCKS5; cả hai biến thể Compose của trình thu thập dữ liệu đều chuyển tiếp tuyến đường này. Nhóm nền sẽ tuân theo không gian làm việc chính. Không có phiên Telegram, thông tin đăng nhập API, mã thông báo bảng điều khiển hay mã thông báo bot nào được gửi đến các nhà cung cấp nguồn cấp dữ liệu. Tên nhà cung cấp, ngày chụp nhanh và tuyến đường tải xuống được hiển thị trong phần **“Nguồn gốc của danh sách**”.

MTProxy chỉ truyền tải lưu lượng Telegram. Các thao tác HTTP trên Workspace như đóng dấu thời gian, thông báo, sao chép ngoài trang web và kiểm tra nguồn sẽ sử dụng một proxy SOCKS5/HTTP riêng biệt khi được cấu hình, sau đó là tuyến SOCKS5/HTTP của tài khoản. Nếu thiếu một trong hai yếu tố này, Hide IP sẽ từ chối yêu cầu; các chế độ khác cho phép kết nối Trực tiếp. Các yêu cầu từ bên ngoài có thể bị vô hiệu hóa. Một proxy tải xuống nguồn cấp dữ liệu được cấu hình rõ ràng vẫn là một tùy chọn can thiệp riêng biệt của người vận hành. Dịch vụ chứng thực độc lập duy trì đường dẫn riêng của mình.

****Các tham số nhóm tự động**** Trong phần **Tham số → MTProxy tự động**, hãy cấu hình ngưỡng lỗi, thời gian chờ, lịch luân phiên, chia sẻ proxy và độ trễ dự phòng được phép. | Điều khiển | Mặc định | | --- | --- | | Ngắt kết nối trước khi thay thế | 3 lần trong vòng 10 phút | | Số proxy được thử cho mỗi lần kết nối | 3 | | Thời gian nghỉ đầu tiên / tối đa sau khi xảy ra lỗi | 10 phút / 6 giờ | | Xoay vòng theo kế hoạch | Tắt; chuyển đổi khi xảy ra lỗi | | Số tài khoản trên mỗi proxy | 0: ưu tiên các mục riêng biệt, chia sẻ khi cần thiết. Đặt thành 1 để chờ mục độc quyền. | | Thời gian trễ trước khi được phép chuyển sang Direct | 10 phút; Tính năng Ẩn IP vẫn từ chối Direct | | Kiểm tra làm mới nguồn cấp dữ liệu / kiểm tra truyền tải | 60 / 10 phút; các giá trị của không gian làm việc chính được áp dụng cho nhóm chia sẻ | Việc sử dụng các máy chủ proxy khác nhau không đảm bảo các địa chỉ thoát khác nhau. Các cài đặt này không vượt qua các giới hạn của Telegram cũng như không chứng minh được tính ẩn danh.

Để thay thế danh sách công khai bằng danh mục nhà mạng của riêng quý vị, vui lòng cấu hình tùy chọn ghi đè dưới đây. Tùy chọn này sẽ vô hiệu hóa hoàn toàn các đăng ký bên ngoài, kể cả khi mảng `proxies` của nó trống.

Vui lòng sao chép [danh mục trống](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) vào `proxy-config/proxies.json` và thêm các điểm cuối công khai đã triển khai của quý vị:

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

Các giá trị ví dụ phải được thay thế. Hệ thống chấp nhận tối đa 32 mục riêng biệt. Danh sách đã được xác thực sẽ trả về các nhãn/máy chủ/cổng mà không cần sử dụng khóa bí mật chung; việc chọn một mục sẽ lưu thông tin xác thực của mục đó vào kho lưu trữ của không gian làm việc. Tính khả dụng vẫn chưa được kiểm tra cho đến khi thực hiện một bài kiểm tra truyền tải rõ ràng. Trong trường hợp danh mục bị lỗi, người dùng vẫn có thể thực hiện cấu hình thủ công.

Khởi chạy trên hệ điều hành gốc: thiết lập đường dẫn JSON cục bộ là `TGWITNESS_PROXY_CATALOG`. Docker:

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

Lớp phủ được gắn vào `proxy-config` ở chế độ chỉ đọc; các tệp phải có thể được đọc bởi UID 10001 của container. Thư mục đó bị loại trừ khỏi Git, bối cảnh xây dựng Docker và các kho lưu trữ nguồn. Danh mục này cấu hình các tài khoản thu thập; [bot chứng thực](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/) sử dụng đường dẫn HTTP/SOCKS5 riêng của mình, không phải MTProxy.

Chế độ dự phòng trực tiếp tuân theo chế độ IP nêu trên. Vui lòng tạm dừng quá trình quan sát trước khi thay đổi lộ trình. Việc lưu lại sẽ ngắt kết nối các máy khách cũ và hủy bỏ các phiên đăng nhập chưa hoàn tất; một máy khách mới sẽ sử dụng lộ trình đã được lưu. Sự liên kết giữa nhật ký và phiên làm việc của tài khoản vẫn được duy trì. Các thiết lập sẽ thay thế lộ trình trước đó: vui lòng nhập lại thông tin đăng nhập proxy khi chỉnh sửa.

Thông tin đăng nhập được mã hóa theo tiêu chuẩn `network.enc`. API không trả về tên người dùng, mật khẩu hoặc khóa bí mật. Các bản ghi có chữ ký chứa loại đường dẫn và thông tin về việc có thông tin đăng nhập hay không, đồng thời loại trừ điểm cuối và các khóa bí mật. Người vận hành có thể xem điểm cuối trên bảng điều khiển. Các trường chứa khóa bí mật sẽ bị xóa sau khi lưu, khóa hoặc chuyển đổi không gian làm việc.

**Tính năng Kiểm tra kết nối Telegram**, cũng có sẵn trước khi đăng nhập, sẽ mở và đóng một kết nối Telegram tạm thời không được ủy quyền thông qua tuyến đường này. Tính năng này không liên hệ với bất kỳ trang web kiểm tra IP nào. Việc thực hiện thành công chỉ xác nhận kết nối truyền tải, chứ không phải quyền truy cập vào nhóm, việc gửi tin nhắn đến nơi hay tính ẩn danh.

Proxy này áp dụng cho các kết nối của ứng dụng Telegram, bao gồm cả việc tải xuống phương tiện từ máy chủ phân phối (DC) của Telegram. Các công cụ TSA được khởi chạy qua trình duyệt, pip, SSH hoặc theo cách thủ công sẽ đi theo các đường dẫn riêng biệt. Tên máy chủ proxy có thể được giải quyết tại địa phương. `rdns` ảnh hưởng đến tên máy chủ đích; Telegram thường cung cấp các địa chỉ IP số của máy chủ phân phối (DC).

SOCKS5 và HTTP CONNECT thuần túy bản thân chúng không mã hóa thông tin đăng nhập proxy hay kênh kết nối giữa máy khách và proxy. MTProto bảo vệ lưu lượng Telegram một cách riêng biệt. Hãy sử dụng một kênh bảo mật phù hợp để kết nối với máy chủ proxy khi ở trên mạng không đáng tin cậy. Các nhóm riêng tư là các cuộc trò chuyện trên đám mây; MTProto không biến chúng thành các Cuộc trò chuyện bí mật được mã hóa đầu cuối.

## Mã hóa và chữ ký

| Lớp | Đã triển khai | Trách nhiệm của người vận hành |
| --- | --- | --- |
| Lưu lượng Telegram | Telethon MTProto | Niềm tin vào nền tảng, lộ trình và tính sẵn sàng |
| Bảng điều khiển web | Token mang theo, cài đặt mặc định loopback, giới hạn yêu cầu | Sử dụng HTTPS hoặc đường hầm SSH để truy cập từ xa |
| Bí mật | Fernet dùng để quản lý thông tin đăng nhập API, phiên làm việc, thông tin đăng nhập proxy và khóa riêng dùng để ký số | Bảo vệ khóa giải mã và máy chủ đang chạy |
| Khóa kho lưu trữ | Khóa cục bộ hoặc khóa chính bên ngoài dành cho một cài đặt mới | Lưu trữ được bảo vệ riêng biệt và sao lưu khóa |
| Tin nhắn và tệp đính kèm | Lưu trữ ứng dụng dưới dạng văn bản thuần túy | Ổ đĩa/khối lượng được mã hóa |
| ZIP/JSONL/CSV/HTML | Kiểm tra tính toàn vẹn, không mã hóa nội dung | Bảo vệ các bản sao đã xuất và quá trình chuyển giao |
| Nguồn gốc và thời gian | Nhật ký có chữ ký, biên nhận quá trình, các công cụ tuân thủ RFC 3161 | Khóa tin cậy, các điểm kiểm tra độc lập/TSA và quy trình lưu giữ |

**Tính năng bảo vệ lưu trữ** trong phần Tài khoản hiển thị các trạng thái này. Mã thông báo bảng điều khiển là một mã truy cập bí mật, không phải mật khẩu mã hóa. Mã này cấp quyền truy cập cho quản trị viên; [các mã thông báo được cấp](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/) có thể được giới hạn phạm vi cho các tài khoản và cuộc trò chuyện. Các không gian làm việc chia sẻ quá trình máy chủ và không phải là các đơn vị thuê riêng biệt.

Một bản demo tổng hợp được khởi chạy rõ ràng và cách ly có thể tự động mở qua một kết nối loopback trực tiếp. Tính năng này sử dụng khả năng tồn tại trong một quy trình riêng biệt; nó không tiết lộ mã thông báo bảng điều khiển đã được cấu hình cũng như không cấp quyền truy cập vào các không gian làm việc thực tế. Các yêu cầu từ xa, qua proxy hoặc giữa các nguồn gốc khác nhau không thể truy cập hoặc sử dụng khả năng truy cập tự động này. Tính năng tiện lợi này không loại bỏ rào cản xác thực đối với dữ liệu tài khoản thực.

BitLocker, LUKS, FileVault hoặc một phân vùng được mã hóa và quản lý có thể bảo vệ bộ nhớ lưu trữ theo các mô hình đe dọa tương ứng của chúng. Quản trị viên của một máy tính đang hoạt động và không bị khóa vẫn có thể đọc được dữ liệu. Hãy bao gồm SQLite WAL/SHM, tệp đa phương tiện, tệp xuất tạm thời, vùng hoán đổi, bản sao lưu và các tệp tải xuống từ trình duyệt vào kế hoạch lưu trữ. Một phân vùng Docker không được mã hóa chỉ đơn thuần vì nó là một phân vùng. TgWitness không triển khai SQLCipher hay mã hóa đối tượng.

## Khóa chính bên ngoài

Đối với việc cài đặt **mới**, vui lòng đặt khóa chính bên ngoài thư mục dữ liệu. Thao tác này sẽ không tự động di chuyển kho khóa cục bộ hiện có. Hãy chuẩn bị một thư mục chứa khóa mà chỉ tài khoản dịch vụ mới có quyền truy cập, sau đó thực hiện lệnh:

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell, sử dụng môi trường dự án đã được cài đặt:

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

Trong Docker, hãy gắn tệp ở chế độ chỉ đọc bên ngoài `/data`, ví dụ như tại `/run/secrets/tgwitness-master.key`, và thiết lập biến môi trường trỏ đến đường dẫn đó. UID của dịch vụ phải có quyền đọc tệp này. Vui lòng truyền đường dẫn, chứ không phải các byte khóa, thông qua các tệp môi trường/cấu hình.

Mỗi không gian làm việc sẽ nhận được một giá trị salt công khai ngẫu nhiên cùng với khóa Fernet riêng của mình, được tạo ra thông qua HKDF-SHA256. `vault.external.json` lưu trữ siêu dữ liệu về quá trình tạo khóa, chứ không phải khóa chính. Nếu thiếu hoặc nhập sai khóa, hệ thống sẽ không khởi động được mà không tự động thay thế khóa đó. Vui lòng lưu giữ cả siêu dữ liệu về giá trị salt lẫn khóa chính để phục hồi hệ thống.

Tất cả các không gian làm việc đều được tạo ra từ cùng một khóa chính; việc khóa này bị xâm phạm sẽ ảnh hưởng đến toàn bộ hệ thống cài đặt. Quá trình đang chạy có thể giải mã các thông tin bí mật. Đây không phải là HSM hay KDF mật khẩu. Không chấp nhận sử dụng mật khẩu do người dùng tự đặt thay thế cho khóa ngẫu nhiên.

Vui lòng giữ lại khóa hiện có cho các bản cài đặt hiện tại cho đến khi quá trình di chuyển có chủ đích được triển khai và xác minh. Việc xóa `vault.key` hoặc thay thế khóa chính có thể làm mất quyền truy cập vào các phiên làm việc/khóa ký. Hãy lưu trữ các bản sao lưu được mã hóa và các khóa riêng biệt, đồng thời thử nghiệm quá trình khôi phục trong một môi trường cách ly.

## Nguồn thông tin và phạm vi xác minh

Được rà soát vào ngày 26 tháng 10 năm 2026:

- https://core.telegram.org/api/auth
- https://core.telegram.org/api/obtaining_api_id
- https://docs.telethon.dev/en/stable/basic/signing-in.html
- https://docs.telethon.dev/en/stable/concepts/sessions.html
- https://core.telegram.org/mtproto/mtproto-transports
- https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/SourceFiles/storage/storage_account.cpp
- Telethon 1.45.0: SQLiteSession, StringSession, `Connection._proxy_connect`, `TcpMTProxy.normalize_secret` và các phương thức tải xuống.

Các thử nghiệm cục bộ bao gồm các thiết bị mô phỏng SOCKS5/HTTP CONNECT vòng lặp, các phiên SQLite tổng hợp, cách ly tuyến đường, loại trừ thông tin bí mật và từ chối khi thiếu khóa. Các thử nghiệm này không xác định khả năng tương tác thực tế giữa Telegram và proxy cũng như hành vi hoạt động thực tế của MTProxy. Vui lòng tham khảo [các tệp VERIFICATION.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/) và [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
