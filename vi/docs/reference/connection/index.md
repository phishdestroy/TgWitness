# Kết nối, máy chủ trung gian và bảo vệ dữ liệu

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/

Xác thực, nhóm proxy tự động, chế độ IP, chính sách dự phòng, yêu cầu bên ngoài và lưu trữ khóa bí mật.

Tài liệu này mô tả cách thức hoạt động và các giới hạn của TgWitness phiên bản 0.8.0. Quá trình xác thực, quyền truy cập nguồn, kết nối mạng và tính đầy đủ của dữ liệu thu thập là các trạng thái độc lập. Để tìm hiểu về các bước đăng nhập, định dạng tệp và quản lý nhiều tài khoản, quý vị hãy bắt đầu từ phần [“Tài khoản và định dạng phiên làm việc](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/)”. Đối với chính sách sự kiện và hành vi khởi động lại, xin vui lòng tham khảo phần [“Cách thức thu thập dữ liệu hoạt động](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/)”.

## Hướng dẫn thiết lập kết nối

Trong **Kết nối**, quản trị viên có thể chọn **Tài khoản này**, **Một nhóm tài khoản** hoặc **Tất cả tài khoản**, sau đó chọn một lộ trình. **Xem lại lựa chọn** liệt kê các tài khoản bị ảnh hưởng. **Chuẩn bị và kiểm tra** kiểm tra lộ trình đề xuất mà không thay đổi lộ trình đã lưu. **Áp dụng kết nối đã kiểm tra** kiểm tra lại, tạm dừng việc giám sát nếu cần thiết, lưu lộ trình và tiếp tục việc giám sát đang chạy. Chương trình không bao giờ bắt đầu thu thập dữ liệu trong một tài khoản trước đó đang ở trạng thái không hoạt động. Việc tải xuống lịch sử vẫn bị tạm dừng và có thể được tiếp tục riêng biệt. Tạm dừng các quá trình xuất dữ liệu đang hoạt động trước khi chuyển đổi.

Theo mặc định, các thay đổi trong nhóm sẽ giữ nguyên đường dẫn riêng cho từng tài khoản. Chỉ hủy chọn tùy chọn đó khi bản xem trước liệt kê các thay đổi mà bạn dự định thực hiện. Ứng dụng báo cáo kết quả của từng tài khoản; đây không phải là giao dịch “tất cả hoặc không gì cả” giữa các cơ sở dữ liệu. Một lần chuyển đổi thất bại sẽ khôi phục cài đặt trước đó của tài khoản đó. Trường hợp không thể tiếp tục sẽ được hiển thị rõ ràng. Bản xem trước hết hạn sau mười phút và các thay đổi đối với cài đặt kết nối hoặc tư cách thành viên nhóm yêu cầu kiểm tra lại.

| Lộ trình | TgWitness quản lý những gì |
| --- | --- |
| Trực tiếp | Kết nối từ máy chủ; VPN từ máy chủ bên ngoài không được phát hiện hoặc áp dụng. |
| VPN | Mỗi tài khoản có một cấu hình WireGuard đường hầm đầy đủ, được thực thi bởi quá trình SOCKS5 trong không gian người dùng cục bộ. Không cài đặt giao diện máy chủ hoặc trình điều khiển nào. |
| Proxy của tôi | Thông tin đăng nhập SOCKS5, HTTP CONNECT hoặc MTProxy. Một URL có thể được điền vào các trường SOCKS5/HTTP. Việc chọn nhiều tài khoản sẽ chia sẻ proxy đã nhập này. |
| MTProto công khai | Bể hiện tại gán các tuyến đường Telegram. Các yêu cầu từ bên ngoài bị vô hiệu hóa cho đến khi một proxy phù hợp riêng biệt được cấu hình trong cài đặt nâng cao. |
| WARP | Một đường hầm cục bộ riêng biệt cho mỗi tài khoản được chọn, kèm theo đăng ký WARP và hồ sơ WireGuard được lưu trữ trong kho lưu trữ của tài khoản đó. |

Kiểm tra tuyến đường hiện tại sử dụng kênh truyền tải Telegram mới chưa được xác thực, không phải phiên làm việc của tài khoản. Đối với các tuyến hỗ trợ HTTP, hệ thống cũng yêu cầu bản ghi HTTPS của Cloudflare qua tuyến đó và hiển thị địa chỉ IP xuất, quốc gia, trạng thái WARP và thời gian kiểm tra được báo cáo. Độ trễ được đo là thời gian thiết lập kết nối Telegram, không phải ping ICMP. Quá trình chuẩn bị WARP sẽ thất bại trừ khi bản theo dõi báo cáo WARP đang hoạt động. Các kiểm tra này xác định khả năng kết nối, không phải tính xác thực hoặc tính đầy đủ của các tin nhắn được ghi lại. Chỉ riêng việc có một tiến trình cục bộ đang chạy không được coi là kiểm tra điểm thoát thành công.

### WARP và WireGuard di động

Đây là bản tích hợp WARP không chính thức **** sử dụng [wgcf 2.3.1](https://github.com/ViRb3/wgcf/releases/tag/v2.3.1) và [wireproxy 1.1.3](https://github.com/windtf/wireproxy/releases/tag/v1.1.3). Quản trị viên phải chấp nhận thiết lập một cách rõ ràng trước lần tải xuống đầu tiên hoặc đăng ký WARP. Các kết nối thiết lập này truy cập trực tiếp đến GitHub và Cloudflare và tiết lộ địa chỉ IP của máy. Lưu lượng truy cập của tài khoản thông thường vẫn giữ nguyên tuyến đường hiện có cho đến khi ứng dụng được khởi chạy. Cloudflare chọn địa chỉ thoát và quốc gia; các đường hầm riêng biệt có thể chia sẻ cùng một địa chỉ thoát. Tính năng này không cung cấp lựa chọn quốc gia, xoay vòng IP định kỳ và tính năng ngắt kết nối VPN toàn hệ thống.

Các bản tải xuống trình hỗ trợ được hỗ trợ: Linux và macOS x86-64/ARM64, và Windows x86-64. Các tệp tin được kiểm tra so với các giá trị băm SHA-256 được gói sẵn trong mã nguồn đã được xem xét, và các tệp thực thi được lưu trong bộ nhớ đệm sẽ được kiểm tra lại trước khi khởi chạy. Không có công cụ hỗ trợ nào được thêm vào PATH, cài đặt dưới dạng dịch vụ hệ thống hoặc được cấp trình nghe công khai. Tất cả các tệp đều nằm trong thư mục `portable-routes/` của không gian làm việc và các mục kho lưu trữ được mã hóa. Trình nghe vòng lặp SOCKS5 yêu cầu thông tin đăng nhập được tạo độc lập.

Hồ sơ cá nhân và thông tin đăng nhập tài khoản WARP được mã hóa bằng kho lưu trữ không gian làm việc hiện có. Trong khi chạy, trình trợ giúp cần một cấu hình văn bản thuần túy chỉ dành cho chủ sở hữu; nó sẽ bị xóa khi dừng bình thường. Sự cố máy chủ có thể khiến tệp này bị bỏ lại trong thư mục dữ liệu chỉ dành cho chủ sở hữu. Điều này không mã hóa đĩa hoặc bảo vệ chống lại quản trị viên. Trình giám sát sẽ đóng đường hầm nếu ống dẫn cha của bảng điều khiển biến mất. Một đường hầm bị lỗi sẽ không bao giờ kích hoạt chế độ dự phòng trực tiếp. Khởi động lại bảng điều khiển sẽ khôi phục đường hầm đã chọn; các lần khởi động thất bại sẽ thử lại với độ trễ giới hạn. **Dừng đường hầm** cũng tạm dừng việc giám sát và duy trì trạng thái đã dừng. **Bắt đầu đường hầm** khởi động đường hầm; tiếp tục giám sát riêng biệt khi sẵn sàng.

Các cấu hình WireGuard được tải lên phải chứa một Giao diện (Interface) và một Nút kết nối (Peer), các tuyến đường IPv4 và IPv6 đầy đủ, và không được chứa các hook, include, thay thế biến môi trường hoặc các trình nghe (listener) bổ sung. Các địa chỉ điểm cuối công khai được giải quyết và cố định trước khi khởi động. Sử dụng VPN bên ngoài hoặc cổng SOCKS5 cho OpenVPN/IPsec và các điểm cuối riêng tư.

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

**Tệp đã chuyển đổi là một khóa truy cập tài khoản chưa được mã hóa.** Hãy lưu giữ nó trong kho lưu trữ được bảo vệ và tuyệt đối không được đưa vào kho lưu trữ chung hay gửi cho bất kỳ dịch vụ chuyển đổi bên thứ ba nào. TgWitness lưu trữ phiên đăng nhập được ủy quyền trong kho lưu trữ được mã hóa của mình. Việc sao chép một phiên đăng nhập sẽ không tạo ra một ủy quyền riêng biệt: xin đừng chạy các ứng dụng khách đồng thời với các khóa xác thực đã được sao chép và cho rằng các bản cập nhật sẽ được phân phối độc lập.

Quá trình chuyển đổi chỉ chuyển giao quyền truy cập, chứ không chuyển các tin nhắn gốc, bộ nhớ đệm của thực thể hay con trỏ cập nhật bền vững. Quá trình này không đảm bảo khả năng khôi phục cập nhật sau khi khởi động lại quy trình.

## MTProto, Telethon và các máy chủ proxy

MTProto là giao thức của Telegram. Telethon là thư viện khách hàng Python mà TgWitness sử dụng. MTProxy là một proxy truyền tải Telegram; SOCKS5 và HTTP CONNECT cung cấp các đường hầm chung. Không có phương thức nào thay thế cho việc xác thực tài khoản.

Lưu đường dẫn cho từng không gian làm việc tại **Tài khoản → Cài đặt → Cài đặt kết nối → Thay đổi đường dẫn kết nối** trước khi đăng nhập. Các không gian làm việc mới mặc định sử dụng **chế độ Tự động MTProxy · danh sách công khai** với tùy chọn **Ẩn địa chỉ**. Các không gian làm việc hiện có đã sử dụng chế độ Trực tiếp (Direct) một cách rõ ràng sẽ vẫn giữ chế độ cho phép điều này.

## Các chế độ IP

Tuyến đường kết nối sẽ quyết định cách kết nối. Chế độ IP và tính năng **bảo vệ IP** trong phần Tài khoản của bảng điều khiển sẽ xác định thời điểm địa chỉ máy chủ có thể bị lộ. Các tùy chọn này không cài đặt VPN hay định tuyến toàn bộ lưu lượng truy cập của máy.

| Chế độ | Telegram | Yêu cầu từ bên ngoài |
| --- | --- | --- |
| Ẩn địa chỉ (`hide`) | Vui lòng sử dụng máy chủ proxy; nếu không có máy chủ nào hoạt động, xin vui lòng chờ đợi. Không có phương án dự phòng trực tiếp. | Yêu cầu sử dụng SOCKS5/HTTP; từ chối các yêu cầu không có proxy phù hợp. |
| Chỉ sử dụng phương án này khi không còn lựa chọn nào khác (`fallback`) | MTProxy tự động có thể sử dụng kết nối trực tiếp (Direct) sau khoảng thời gian trễ đã được cấu hình, sau đó quay trở lại sử dụng proxy đang hoạt động. | Ưu tiên sử dụng proxy bên ngoài đã được cấu hình hoặc tuyến SOCKS5/HTTP của tài khoản; nếu không, có thể sử dụng chế độ Trực tiếp. |
| Máy chủ nằm sau một đường hầm hoặc VPN (`tunnel`) | Các đường dẫn trực tiếp và cơ chế chuyển hướng tự động sang nhóm dự phòng ngay lập tức đều được phép. | Việc kết nối trực tiếp được phép khi không có máy chủ trung gian nào được cấu hình. |

Chế độ đường hầm hoặc VPN giả định rằng bạn quản lý mạng đó riêng biệt. Nếu không có đường hầm hoạt động, các điểm đến có thể nhìn thấy địa chỉ của chính máy chủ. Hãy chọn chế độ phù hợp với mạng thực tế của bạn, chứ không phải dựa vào tên của tùy chọn.

### Chọn một lộ trình

| Lộ trình | Cài đặt | Phạm vi |
| --- | --- | --- |
| MTProxy tự động | Các danh sách tích hợp sẵn hoặc danh mục toán tử | Luôn duy trì một tuyến kết nối Telegram hoạt động; phương án dự phòng trực tiếp phụ thuộc vào chế độ IP |
| Trực tiếp | Chế độ Tunnel hoặc VPN | Telethon sử dụng tuyến mạng của nhà cung cấp dịch vụ |
| SOCKS5 | Máy chủ, cổng, tên người dùng/mật khẩu (tùy chọn) | python-socks, đã kích hoạt tính năng DNS đích từ xa |
| HTTP CONNECT | Máy chủ, cổng, tên người dùng/mật khẩu (tùy chọn) | Sử dụng kết nối HTTP CONNECT thuần túy; giao thức TLS đến chính máy chủ proxy chưa được triển khai |
| MTProxy | Máy chủ, cổng, khóa bí mật | Phương thức truyền tải Telethon thử nghiệm; 32 chữ số thập lục phân hoặc `dd` + 32 chữ số thập lục phân |

Các khóa bí mật TLS giả mạo `ee` sẽ bị từ chối. Tính năng chuẩn hóa của Telethon 1.45 có thể loại bỏ tiền tố và tên miền, nhưng tính năng này không hỗ trợ TLS giả mạo. Vui lòng dán `tg://proxy?server=…&port=…&secret=…` hoặc `https://t.me/proxy?server=…&port=…&secret=…` và chọn **“Điền trường từ liên kết**”. Thao tác này sẽ xác thực và điền thông tin vào các trường mà không cần kết nối hay lưu lại; quý vị hãy kiểm tra và lưu đường dẫn đó riêng biệt. Các trường nhập liệu thủ công vẫn có sẵn. Vui lòng tham khảo [các liên kết proxy Telegram](https://core.telegram.org/api/links#proxy-links).

### Các máy chủ proxy công cộng do hệ thống cài đặt của quý vị cung cấp

Danh sách tích hợp sẵn kết hợp bốn nguồn: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) và [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). Bản chụp nhanh đi kèm chứa thông tin về điểm cuối, nguồn gốc và ngày tải xuống. Việc một nhà cung cấp được liệt kê trong danh sách này không phải là bằng chứng cho thấy máy chủ proxy đó hoạt động hoặc cung cấp mọi bản cập nhật của Telegram.

**MTProxy tự động** kiểm tra kết nối truyền tải của Telegram, duy trì một proxy đang hoạt động và chuyển sang proxy khác khi proxy đó gặp sự cố. Các không gian làm việc ưu tiên sử dụng các proxy khác nhau khi có đủ các mục proxy đang hoạt động; địa chỉ thoát duy nhất không được đảm bảo. Các proxy gặp sự cố sẽ tạm ngưng hoạt động trước khi thực hiện lần thử tiếp theo. Nếu không có proxy nào hoạt động, chế độ IP sẽ xác định liệu việc thu thập dữ liệu phải chờ đợi hay có thể sử dụng kết nối trực tiếp. Việc thay đổi proxy không làm thay đổi tài khoản hay xóa sổ nhật ký của tài khoản đó. Các lựa chọn và thay đổi về đường dẫn được ghi lại trong sổ nhật ký đã được ký điện tử.

Khi các tuyến tự động đang hoạt động, danh sách sẽ được làm mới mỗi giờ và các kiểm tra truyền tải được thực hiện mỗi mười phút theo mặc định. Các khoảng thời gian này có thể tùy chỉnh. **Việc cập nhật danh sách công khai** sẽ yêu cầu làm mới; chỉ xem danh sách sẽ không thay đổi tuyến thủ công đã lưu.

**Lưu lượng Telegram và các yêu cầu HTTPS sử dụng các tuyến đường khác nhau.** Việc tải xuống danh sách sử dụng một kết nối HTTPS riêng biệt và tuyến đường yêu cầu bên ngoài được cung cấp. Phiên bản `TGWITNESS_PROXY_FEED_PROXY` sẽ ghi đè rõ ràng tuyến đường đó bằng một proxy HTTP/SOCKS5; cả hai biến thể Compose của trình thu thập dữ liệu đều chuyển tiếp tuyến đường này. Nhóm nền sẽ tuân theo không gian làm việc chính. Không có phiên Telegram, thông tin đăng nhập API, mã thông báo bảng điều khiển hay mã thông báo bot nào được gửi đến các nhà cung cấp nguồn cấp dữ liệu. Tên nhà cung cấp, ngày chụp nhanh và tuyến đường tải xuống được hiển thị trong phần **“Nguồn gốc của danh sách**”.

Một MTProxy chỉ truyền tải lưu lượng Telegram. Các thao tác HTTP của không gian làm việc như dấu thời gian, thông báo, bản sao ngoài trang web và kiểm tra nguồn sử dụng một proxy SOCKS5/HTTP riêng biệt khi được cấu hình, sau đó là tuyến SOCKS5/HTTP của tài khoản. Nếu không có cả hai, tính năng Ẩn địa chỉ sẽ từ chối yêu cầu; các chế độ khác cho phép Trực tiếp. Các yêu cầu bên ngoài có thể bị vô hiệu hóa. Một proxy tải xuống nguồn cấp dữ liệu được cấu hình rõ ràng vẫn là một quyền ưu tiên riêng biệt của người vận hành. Dịch vụ chứng kiến độc lập duy trì đường dẫn riêng của mình.

Đối với các dịch vụ riêng tư do nhà điều hành quản lý, cài đặt môi trường máy chủ hiện có `TGWITNESS_ALLOW_PRIVATE_DESTINATIONS=1` cho phép các đích đến riêng tư và duy trì việc giải quyết tên máy chủ phía proxy. Tính năng này không thể được kích hoạt từ bảng điều khiển. Chế độ chỉ công khai sẽ từ chối các đích đến `.onion` trước khi truy vấn trình giải quyết công khai; các dịch vụ Tor onion yêu cầu cài đặt đích đến riêng tư rõ ràng và một proxy phù hợp. Hành vi DNS này áp dụng cho các hoạt động HTTP bên ngoài, không áp dụng cho giao thức truyền tải của Telegram. Cloudflare cung cấp tài liệu về [điểm cuối DNS JSON](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/).

****Các tham số nhóm tự động**** Trong phần **Tham số → Tự động MTProxy**, hãy cấu hình ngưỡng lỗi, thời gian chờ, lịch luân phiên, chia sẻ proxy và độ trễ dự phòng cho phép. | Kiểm soát | Mặc định | | --- | --- | | Ngắt kết nối trước khi thay thế | 3 lần trong vòng 10 phút | | Số proxy thử mỗi lần kết nối | 3 | | Thời gian nghỉ đầu tiên / tối đa sau khi thất bại | 10 phút / 6 giờ | | Luân phiên theo kế hoạch | Tắt; chuyển sang chế độ dự phòng khi thất bại | | Số tài khoản trên mỗi proxy | 0: ưu tiên các mục riêng biệt, chia sẻ khi cần thiết. Đặt 1 để chờ một mục độc quyền. | | Thời gian trễ trước khi cho phép chuyển sang Direct | 10 phút; Ẩn địa chỉ nếu vẫn từ chối Direct | | Tần suất làm mới nguồn cấp dữ liệu / kiểm tra kết nối | 60 / 10 phút; các giá trị trong không gian làm việc chính áp dụng cho nhóm chia sẻ | Các máy chủ proxy khác nhau không đảm bảo các địa chỉ thoát khác nhau. Các cài đặt này không vượt qua giới hạn của Telegram hoặc đảm bảo tính ẩn danh.

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
