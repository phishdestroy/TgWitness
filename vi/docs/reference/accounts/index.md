# Các định dạng tài khoản và phiên làm việc

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/

Đăng nhập bằng số điện thoại, mã QR hoặc khóa xác thực, nhập các phiên làm việc từ Telethon, Pyrogram hoặc Telegram Desktop, và quản lý nhiều tài khoản cùng lúc.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Bắt đầu](https://phishdestroy.github.io/TgWitness/vi/docs/reference/quickstart/)

![Bắt đầu](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

TgWitness đăng nhập dưới dạng tài **khoản người dùng Telegram** (không phải bot) qua giao thức MTProto, sử dụng Telethon. Mỗi tài khoản tồn tại trong **không gian** làm việc riêng (được gọi là *“workspace”* trong API và các công cụ dòng lệnh) với phiên làm việc, nguồn dữ liệu, nhật ký và khóa ký riêng.

Các tệp phiên làm việc, chuỗi phiên làm việc và Khóa xác thực là **các thông tin ủy quyền tài khoản**: bất kỳ ai sở hữu chúng đều có thể thực hiện các thao tác như chủ tài khoản đó. Chúng không chứa lịch sử tin nhắn.

> [!CẢNH BÁO] **Không nên sử dụng bất kỳ thứ gì mà quý vị không thể chấp nhận mất mát.** Chúng tôi khuyến cáo mạnh mẽ không nên kết nối các tài khoản cá nhân hoặc các tài khoản có giá trị khác, cũng như không nên tạo ID API / băm API trên một tài khoản mà quý vị coi trọng. Điều này không phải do TgWitness chưa được kiểm thử: Telegram hạn chế và cấm vĩnh viễn các tài khoản một cách khó lường — đối với khối lượng yêu cầu mà nền tảng này cho là quá mức, bất kể khách hàng hay mục đích là gì, mà không có tài liệu hướng dẫn đầy đủ. Nhiều trường hợp bị cấm là không thể đảo ngược. Hãy sử dụng các tài khoản chuyên dụng. Quá trình thử nghiệm diễn ra suôn sẻ phụ thuộc vào Telegram, không phải vào phần mềm, và không đảm bảo điều gì cho các giai đoạn sau này.

- [Tổng quan](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#at-a-glance)
- [Trước khi bắt đầu: ID API và mã băm API](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Số điện thoại](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#phone-number) · [Mã QR](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#qr-code) · [Khóa xác thực (Auth Key) + ID DC](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#auth-key--dc-id)
- [Tệp tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#pyrogram-session) · [Cặp phiên + JSON](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#telethon-stringsession) · [Tệp JSON tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#account-json)
- [Xác định những gì quý vị đang có](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#identify-what-you-have) · [Các định dạng không được hỗ trợ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#unsupported-formats)
- [Nhiều tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#multiple-accounts) · [Bảo vệ an toàn cho các tệp tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#keeping-account-files-safe) · [Khắc phục sự cố](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#troubleshooting)

## Tổng quan

| Những gì quý vị có | Tab **“Thêm tài khoản**” | Quý vị cũng sẽ cần |
| --- | --- | --- |
| Số điện thoại và quyền truy cập vào các mã đăng nhập của công cụ này | **Điện thoại** | Mật khẩu xác thực hai yếu tố (2FA) nếu tính năng này đã được kích hoạt |
| Telegram đang mở trên một thiết bị khác | **Mã QR** | Mật khẩu xác thực hai yếu tố (2FA) nếu tính năng này đã được kích hoạt |
| Một tệp `.session` (Telethon hoặc Pyrogram) | **Tệp tin** | Tệp JSON đi kèm (tùy chọn) dành cho cài đặt ứng dụng |
| `.session` + `.json` cùng tên | **Tệp tin** (chọn cả hai) | Thông thường không có nội dung nào khác |
| Thư mục `tdata` trên Telegram Desktop | **Tệp tin** (dạng ZIP) | Mật mã cục bộ trên máy tính để bàn (nếu đã được thiết lập) |
| Một phiên StringSession của Telethon (văn bản, `.txt`, `.tgwitness-session`) | **Tệp tin** | Không cần cặp API riêng biệt |
| Một khóa `.json` kèm theo phiên làm việc hoặc Khóa xác thực (Auth Key) | **Tệp tin** | Không cần cặp API riêng biệt |
| Một Khóa xác thực (512 ký tự hex) và số DC tương ứng | **Khóa xác thực** | ID người dùng (tùy chọn) |

TgWitness nhận diện các tệp dựa trên **nội dung** chứ không phải tên tệp. Việc đổi tên tệp sẽ không bao giờ làm thay đổi nội dung của tệp đó.

## Trước khi bắt đầu: ID API và mã băm API

Bạn có thể đăng nhập mà không cần tạo ứng dụng API Telegram. Khi không có cặp nào được nhập, nhập khẩu hoặc đã được lưu trong không gian làm việc, TgWitness sẽ chọn một cặp từ kho cặp API công khai 50 (`tgwitness/api_pool.py`) tích hợp sẵn, ưu tiên Telegram Desktop cho lần đăng nhập mới và ưu tiên cặp đã lưu trước; các cặp còn lại sẽ được xáo trộn. Nếu Telegram từ chối một cặp (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), cặp tiếp theo sẽ được thử, tối đa tám cặp mỗi lần đăng nhập; các cặp bị từ chối sẽ bị bỏ qua cho đến khi khởi động lại. Cặp đã dùng để đăng nhập sẽ được lưu cùng với tài khoản và tái sử dụng cho tài khoản đó. ID API **,** và băm API **,** xác định ứng dụng với Telegram; chúng không tự mình cấp quyền truy cập cho tài khoản.

Các trường kết nối bị thiếu sẽ sử dụng cặp thiết bị/hệ điều hành xác định từ các danh mục [opentele2 2.0.0 đi kèm](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735): Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834` và Web `2496`. ID xây dựng nguồn của Android `4` cũng sử dụng danh mục Android, như được xác định trong [BuildVars của Telegram Android](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web mặc định là A; hậu tố phiên bản ứng dụng `K` được nhập hoặc gói ngôn ngữ `macos` sẽ chọn K, và phiên bản `0.7.0` sẽ chọn Webogram. Các ID ứng dụng không xác định sẽ giữ nguyên các giá trị mặc định của máy chủ Telethon. Các trường được nhập vào luôn được ưu tiên, bao gồm cả phiên bản ứng dụng cũ hơn và gói ngôn ngữ trống. Danh mục không bao giờ thay đổi ID/băm API. Ảnh chụp phiên bản của nó được xem xét rõ ràng, không được lấy trong quá trình đăng nhập. Hồ sơ đã lưu sẽ vẫn ổn định sau khi cập nhật.

`account.getAuthorizations` báo cáo siêu dữ liệu ủy quyền đã lưu của Telegram; đây không phải là bản sao của mỗi `initConnection` mới. So sánh nó với hồ sơ thực tế đã được gửi. Việc kết nối một ủy quyền hiện có không xác thực băm API đi kèm: `initConnection` gửi ID API, trong khi băm được sử dụng cho các yêu cầu đăng nhập.

Sau khi xác thực bằng điện thoại mới hoặc mã QR, TgWitness yêu cầu cấu hình, DC gần nhất, trạng thái trực tuyến, ngôn ngữ (khi gói ngôn ngữ không trống), cập nhật ứng dụng và cập nhật điều khoản dịch vụ, với khoảng thời gian 0.3–1.5 giây giữa các yêu cầu. Việc cập nhật trạng thái sẽ tạm thời đánh dấu tài khoản là trực tuyến. Trình tự này chỉ chạy một lần khi hoàn tất đăng nhập, không chạy khi nhập dữ liệu, kết nối lại hoặc khởi động lại. Việc xác thực được lưu trước; một yêu cầu thất bại sẽ dừng trình tự mà không thử lại hoặc hủy bỏ quá trình đăng nhập. Kết quả được ghi lại dưới dạng `account.initialized`, với tên lỗi thay vì nội dung phản hồi. Trình tự này không đảm bảo tránh được các hạn chế tài khoản.

Đối với `tdesktop` , nếu thiếu `tz_offset` , hệ thống sẽ sử dụng độ lệch UTC cục bộ của máy chủ, được làm tròn đến 900 giây bằng thuật toán [opentele2](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; giấy phép tại `tgwitness/client_profiles.LICENSE` ). Giá trị này được cập nhật trên mỗi lần kết nối để phản ánh các thay đổi do giờ mùa hè. `tz_offset` được nhập vào sẽ được ưu tiên trên mọi nền tảng và được giữ nguyên chính xác, kể cả giá trị bằng không. Các mục `initConnection.params` khác vẫn được giữ lại. Biểu mẫu đăng nhập HTTP chấp nhận múi giờ dạng số được trả về từ quá trình nhập tệp; các giá trị boolean, số thập phân và độ lệch nằm ngoài phạm vi được hỗ trợ sẽ bị từ chối.

Các tuyến đường Direct, SOCKS5 và HTTP CONNECT sử dụng `ConnectionTcpObfuscated` của Telethon (MTProto được rút gọn và làm mờ). HTTPS CONNECT duy trì TLS đến proxy và sử dụng cùng một giao thức truyền tải được làm mờ bên trong đường hầm. MTProxy duy trì giao thức truyền tải trung gian ngẫu nhiên và xử lý khóa bí mật theo yêu cầu. Việc chuyển đổi đường dẫn áp dụng các lựa chọn tương tự. Việc làm mờ thay đổi cấu trúc gói tin; nó không che giấu tài khoản hoặc siêu dữ liệu khách hàng của tài khoản đó khỏi Telegram cũng như không ngụ ý khả năng miễn trừ các hạn chế.

Sau khi kết nối với một máy khách được ủy quyền, TgWitness sẽ kiểm tra cấu hình, trung tâm dữ liệu (DC) gần nhất, thông tin ủy quyền hiện tại, cơ sở tham chiếu lớp đã được xem xét, ngôn ngữ, các bản cập nhật ứng dụng và các bản cập nhật điều khoản dịch vụ. Các chẩn đoán này được chạy một lần cho mỗi phiên bản máy khách, trước khi thu thập dữ liệu, và được hiển thị trong phần chi tiết kết nối kèm theo thời gian thực hiện. `account.connection_checked` ghi lại kết quả mà không bao gồm băm phiên, địa chỉ IP, mã thông báo hoặc băm API. Chúng không bao giờ chấp nhận điều khoản hoặc cài đặt bản cập nhật. Lỗi yêu cầu hoặc trạng thái FloodWait sẽ dừng các yêu cầu tiếp theo; kết quả bị thiếu sẽ được coi là chưa xác định. Các kiểm tra cục bộ vẫn có thể báo cáo kết quả trong khi các kiểm tra mạng bị bỏ qua.

Chẩn đoán FloodWait lưu giữ phương thức TL bị lỗi, bất kỳ trình bao bọc Takeout/range nào, thời gian chờ do máy chủ yêu cầu và thời hạn hiệu lực trong `telegram.backoff`. Chi tiết kết nối hiển thị phương thức và thời hạn trong khi các yêu cầu bị tạm dừng. Chẩn đoán bao gồm bộ đếm số lần gọi của khách hàng theo từng phương thức kể từ khi khách hàng đó được tạo; chúng đếm việc giải quyết đối tác lồng nhau riêng biệt, nhưng không đếm gói tin hoặc các lần thử lại nội bộ của Telethon. Các bộ đếm hiện tại cũng có sẵn dưới dạng `collector.rpc_activity` trong API trạng thái. Không bao gồm đối số yêu cầu, tên người dùng, hàm băm truy cập hoặc văn bản ngoại lệ. Chẩn đoán cuối cùng và thời hạn đầy đủ vẫn tồn tại sau khi khởi động lại. Các lần chờ trước đó không có bản ghi phương thức không thể được gán lại sau này. Xem giới hạn xuất  để xem xét nguồn và sự khác biệt giữa khám phá và thu thập lịch sử.

`official_app=True` hoặc `False` là cờ ủy quyền hiện tại của Telegram. Cả hai giá trị này đều không xác định liệu tài khoản đó có bị hạn chế, đáng tin cậy hay đang được giám sát hay không. Các bản chụp nhanh `account.devices` ở chế độ bằng chứng hiện có vẫn lưu giữ lịch sử của tất cả các thiết bị đã đăng nhập; chẩn đoán kết nối chỉ lưu giữ mô tả thiết bị hiện tại.

Trước khi kết nối, các kiểm tra tư vấn sẽ so sánh nền tảng API, gói ngôn ngữ, định dạng thiết bị/hệ điều hành và phiên bản ứng dụng, cài đặt vùng địa phương của hệ thống di động, cùng với lớp lược đồ thực tế của Telethon với tiêu chuẩn cơ sở đã được xem xét. Các cảnh báo xuất hiện trong nhật ký máy chủ và siêu dữ liệu trạng thái tài khoản; chúng không bao giờ thay thế các giá trị đã nhập hoặc thay đổi lớp lược đồ. Một lớp khác là tín hiệu đánh giá khả năng tương thích, không phải bằng chứng về tài khoản bị hỏng hoặc bị hạn chế. Các kiểm tra này và `official_app` không chứng nhận rằng Telegram coi tài khoản đó là an toàn trước các hạn chế. Trạng thái tài khoản bị ngắt kết nối sử dụng hồ sơ đã lưu thay vì tạo một mô tả thiết bị khác.

Để sử dụng ứng dụng của riêng quý vị thay thế (tài khoản đăng ký ứng dụng đó sẽ là tài khoản chịu rủi ro; xem [phần “Tại sao lại có nhóm API tích hợp sẵn?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)”):

1. Vui lòng truy cập [my.telegram.org](https://my.telegram.org) và đăng nhập bằng bất kỳ số điện thoại nào mà quý vị đang sở hữu. Mã xác minh sẽ được gửi đến ứng dụng Telegram, không phải qua tin nhắn SMS.
2. Chọn **các công cụ phát triển API**.
3. Tạo ứng dụng: bất kỳ tiêu đề và tên ngắn nào (5–32 ký tự), nền tảng **Máy tính để bàn**. Các trường URL và mô tả có thể để trống.
4. Vui lòng sao chép **App api_id** (một số) và **App api_hash** (32 ký tự thập lục phân).

Trong bảng điều khiển, phần **“API ID + Hash**” nằm ngay dưới biểu mẫu đăng nhập. Quý vị có thể dán một cặp `api_id:api_hash` duy nhất vào **ô “API ID”** và cả hai trường sẽ được điền tự động. Một cặp này có thể được sử dụng cho tất cả các tài khoản của quý vị. Sau khi đăng nhập thành công, thông tin này sẽ được lưu trữ dưới dạng mã hóa, chỉ trong không gian làm việc đó và tuyệt đối không bao giờ được gửi trở lại trình duyệt.

Có ba loại thông tin xác thực khác nhau liên quan đến vấn đề này:

| Bí mật | Mở | Địa chỉ trang web |
| --- | --- | --- |
| Mã thông báo bảng điều khiển | Bảng điều khiển web TgWitness | `panel-token.txt` trong thư mục dữ liệu, hoặc `TGWITNESS_TOKEN` |
| ID API + mã băm | Không có nội dung nào riêng lẻ; chỉ xác định ứng dụng | Cặp tài khoản tích hợp sẵn, cài đặt được nhập vào hoặc ứng dụng của riêng quý vị tại my.telegram.org |
| Xác thực tài khoản | Tài khoản Telegram | Được tạo thông qua đăng nhập bằng điện thoại/mã QR hoặc được nhập dưới dạng phiên làm việc |

Nếu cần truy cập Telegram qua máy chủ proxy, vui lòng thiết lập trước tại **mục Tài khoản → Cài đặt → Cài đặt kết nối → Thay đổi đường dẫn kết nối**.

## Số điện thoại

1. Mở **Tài khoản**, chọn tab **Điện thoại** và nhập số theo định dạng quốc tế, ví dụ: `+44 7700 900123`. Các khoảng trắng và dấu gạch ngang sẽ được tự động loại bỏ.
2. Nhấn vào **“Tiếp tục**”. Các trường API ID và Hash có thể để trống.
3. Vui lòng nhập mã mà Telegram gửi (thường được gửi đến ứng dụng Telegram; việc gửi qua tin nhắn SMS không được đảm bảo).
4. Nếu tài khoản đã bật xác thực hai bước, vui lòng nhập mật khẩu đó. Đây không phải là mã token trên bảng điều khiển và cũng không phải là mã khóa thiết bị.
5. Vui lòng kiểm tra ID tài khoản hiển thị sau khi đăng nhập, sau đó chọn các nguồn.

Mã đăng nhập và mật khẩu xác thực hai yếu tố (2FA) tuyệt đối không bao giờ được lưu trữ trên đĩa cứng.

## Mã QR

Vui lòng sử dụng tính năng này khi tài khoản đã được đăng nhập sẵn trên điện thoại hoặc máy tính khác.

1. Nhấp vào tab **Mã QR** → **Hiển thị mã QR**. Các trường API ID và Hash có thể để trống.
2. Trên thiết bị đã đăng nhập: **Cài đặt → Thiết bị → Kết nối thiết bị máy tính để bàn**, quét mã và xác nhận.
3. Vui lòng nhập mật khẩu xác thực hai yếu tố (2FA) vào TgWitness nếu Telegram yêu cầu.

Hình ảnh mã QR được tạo tại địa phương. Mã có thời hạn sử dụng; vui lòng nhấn vào **“Tạo mã QR khác”** để thử lại. Việc khóa bảng điều khiển, chuyển sang không gian làm việc khác hoặc đăng nhập bằng tài khoản khác sẽ hủy bỏ mã đang chờ xử lý.

## Khóa xác thực (Auth Key) + ID DC

Khóa xác thực (Auth Key) là khóa ủy quyền thô dài 256 byte đằng sau mỗi phiên Telegram, được biểu diễn dưới dạng **512 ký tự thập lục phân**, kèm theo số trung tâm dữ liệu **từ DC 1 đến DC 5**.

1. Tab **Khóa xác thực**. Vui lòng dán toàn bộ khóa; khóa rút gọn có chứa ký tự `…` sẽ không hoạt động.
2. Vui lòng chọn ID DC được cung cấp kèm theo khóa.
3. Quý vị có thể nhập **ID người dùng (**tùy chọn). TgWitness sẽ từ chối kết nối nếu Telegram báo cáo một tài khoản khác.
4. **Tài khoản** Press **Connect**.

Khóa xác thực (512 ký tự) không phải là mã băm API (32 ký tự). Cùng một khóa này cũng có thể được nhập dưới dạng JSON; vui lòng tham khảo [phần JSON tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#account-json).

## Tệp tài khoản

Mở mục **Thêm tài khoản → Tệp** và chọn tối đa **bốn tệp thuộc về một tài khoản**, tổng dung lượng **8 MiB**, sau đó nhấn **Kết nối tài khoản**.

Các biểu mẫu **Files**, **Auth key** và nhập hàng loạt hiển thị cảnh báo phiên song song trước khi kết nối. Theo mặc định, các ủy quyền đã nhập sẽ được tái sử dụng. Giữ ứng dụng gốc đóng trong khi khóa của nó đang được sử dụng tại đây. **Files** và **Auth key** cũng cung cấp **Tạo ủy quyền độc lập**, được mô tả bên dưới. Nhập hàng loạt vẫn sử dụng chế độ trực tiếp. Đăng nhập qua điện thoại và QR tương tác sẽ tạo ra các ủy quyền riêng biệt. Tiêu đề cảnh báo vẫn hiển thị trong biểu mẫu nhập; phần giải thích đầy đủ sẽ mở ra tự động khi các tệp hoặc chuỗi khóa/phiên được cung cấp. Phần này có thể được thu gọn sau khi đọc, để trình chọn tệp và các điều khiển kết nối vẫn có thể sử dụng được trên điện thoại.

- Các tệp tin được chuyển đổi trực tiếp **trong bộ nhớ** trên máy chủ TgWitness của quý vị. Các tệp tải lên không được lưu trữ, các tệp ZIP không được giải nén ra đĩa và không có dịch vụ bên ngoài nào được liên hệ.
- Phiên ghi chép thu được sau đó sẽ được đối chiếu với Telegram. Nếu một tệp ghi nhận ID người dùng, thì ID đó phải trùng khớp với thông tin tài khoản mà Telegram cung cấp.
- Các tệp mô tả các tài khoản khác nhau hoặc thông tin đăng nhập API khác nhau sẽ bị từ chối thay vì chỉ chọn một tài khoản duy nhất.
- Trường **“Mật khẩu hoặc văn bản phiên làm việc”** chứa trường mật khẩu cục bộ TData, một ô để dán StringSession và **đọc tệp mà không cần đăng nhập** (điền biểu mẫu mà không cần liên hệ với Telegram).

### Tạo một quy trình ủy quyền độc lập

Chọn **Tạo một ủy quyền độc lập** trước khi kết nối các tệp đã nhập hoặc một Khóa ủy quyền. TgWitness kết nối tạm thời với thiết bị nguồn đã nhập, sử dụng nó để phê duyệt mã thông báo đăng nhập QR của khách hàng mới, và ngắt kết nối thiết bị nguồn ngay sau khi phê duyệt. Khách hàng mới có khóa ủy quyền riêng và một hồ sơ máy tính để bàn được chọn riêng. Thông tin đăng nhập API và hồ sơ thiết bị do người hiến tặng cung cấp chỉ được sử dụng cho kết nối với người hiến tặng. Không có ủy quyền hiện có nào bị đăng xuất hoặc thu hồi.

**Giữ ứng dụng khách gốc của người tặng hoàn toàn đóng trong bước này.** Kết nối ban đầu vẫn sử dụng khóa đã sao chép của nó, do đó chế độ này không thể loại bỏ rủi ro sử dụng song song ban đầu đó. Sau khi kết nối ủy quyền mới, chủ sở hữu có thể mở lại ứng dụng gốc và sử dụng cả hai một cách độc lập. Đăng nhập tương tác **qua mã QR** cho phép ứng dụng gốc phê duyệt việc đăng nhập mà không cần sao chép hoặc kết nối khóa của nó tại đây.

Nếu Telegram yêu cầu 2FA, chế độ này sẽ sử dụng `twoFA` từ tệp JSON đã chọn nếu có, hoặc yêu cầu nhập mật khẩu. Nếu mật khẩu nhập vào bị từ chối, hệ thống sẽ quay lại biểu mẫu nhập mật khẩu. Mật khẩu không được lưu lại. Khóa ứng viên được lưu dưới dạng mã hóa trong thẻ `independent_login.enc`, bao gồm cả các thay đổi trong quá trình di chuyển trung tâm dữ liệu. Sau khi bị gián đoạn, hãy chọn cùng một tài khoản nguồn và tùy chọn này để tiếp tục sử dụng khóa ứng viên đã lưu. Không gian làm việc vẫn được dành riêng cho tài khoản đó; việc hoàn tất không thành công sẽ không xóa không gian làm việc mới. Giữ lại thư mục dữ liệu và khóa kho lưu trữ của nó. Thông tin đăng nhập cuối cùng và bản ghi nhật ký `account.authorized` bao gồm phương thức nhập, định dạng đầu vào và ID API của người hiến tặng, không bao gồm khóa hoặc mật khẩu của người hiến tặng.

Vào ngày 5 tháng 11 năm 2026, một tài khoản chuyên dụng đã vượt qua các kiểm tra trực tiếp với các nhà tài trợ Telethon, Pyrogram và TData: hoàn tất xác thực hai yếu tố (2FA), các khóa ủy quyền mới riêng biệt, truy cập đồng thời của nhà tài trợ và khách hàng mới, cũng như đọc kênh công khai. Trường hợp Telethon cũng đã khôi phục một ứng viên đã lưu sau khi bị gián đoạn ở bước nhập mật khẩu. Mỗi lần xác thực mới đều hoàn tất sáu yêu cầu khởi tạo sau khi đăng nhập, và nhật ký đã ký của nó được xác minh. Phiên làm việc ban đầu vẫn có thể sử dụng được ở cả bốn định dạng được cung cấp.

Cơ sở dữ liệu lỗi [RPC của Telegram](https://core.telegram.org/api/errors.json) liên kết `FRESH_CHANGE_ADMINS_FORBIDDEN` với việc thay đổi quản trị viên, `FRESH_CHANGE_PHONE_FORBIDDEN` với việc thay đổi số điện thoại, và `FRESH_RESET_AUTHORISATION_FORBIDDEN` với việc thu hồi các phiên khác, thay đổi thời hạn tồn tại của chúng hoặc đăng ký khóa truy cập. `SESSION_TOO_FRESH_*` và `PASSWORD_TOO_FRESH_*` liên quan đến việc chuyển nhượng quyền sở hữu và rút tiền thu nhập hoặc quà tặng. Đây không phải là các thao tác thu thập dữ liệu; việc đăng nhập mới không đồng nghĩa với lệnh cấm đọc toàn diện trong 24 giờ. Tính năng xuất dữ liệu có thể trả về `TAKEOUT_INIT_DELAY_*` riêng biệt. TgWitness giữ lại các khoảng tạm dừng do máy chủ yêu cầu và không tự động thử lại việc chấp nhận token hoặc thu hồi phiên để vượt qua các hạn chế.

### Telethon `.session`

|  |  |
| --- | --- |
| Đây là gì | Cơ sở dữ liệu SQLite mà các công cụ dựa trên Telethon tạo ra, ví dụ như `my_account.session` |
| Được công nhận bởi | Các bảng `sessions` (cùng với `dc_id`, `server_address`, `port`, `auth_key`) và `version` = 7 hoặc 8 |
| Yêu cầu | Chính xác là một hàng phiên làm việc được ủy quyền; một cơ sở dữ liệu khép kín và hoàn chỉnh |

Trước tiên, hãy đóng chương trình đã tạo ra tệp đó. Nếu tệp `my_account.session-journal` hoặc `my_account.session-wal` vẫn tồn tại bên cạnh tệp chính, điều đó có nghĩa là cơ sở dữ liệu chưa được hoàn tất: hãy mở và đóng ứng dụng khách gốc một cách đúng quy trình. Việc xóa các tệp phụ này có thể để lại một bản sao bị hỏng.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Đây là gì | Các công cụ dựa trên Pyrogram tạo ra cơ sở dữ liệu SQLite |
| Được công nhận bởi | Bảng `sessions` với `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 hoặc 3 |
| Yêu cầu | Chỉ chấp nhận một phiên đăng nhập **của người dùng** được ủy quyền trên mạng sản xuất. Các phiên của bot và máy chủ thử nghiệm (test-DC) sẽ bị từ chối |

ID người dùng được lưu trữ sẽ được đối chiếu với hệ thống Telegram trong quá trình đăng nhập.

### Cặp phiên + JSON

Các tài khoản thường được phân phối dưới dạng hai tệp có cùng tên, ví dụ như `447700900123.session` và `447700900123.json`. Vui lòng chọn **cả hai tệp** cùng một lúc.

- Dựa trên dữ liệu JSON, TgWitness sử dụng các giao thức `app_id`/`api_id` và `app_hash`/`api_hash`, do đó quý vị thường không cần phải nhập thông tin đăng nhập API.
- Cấu hình kết nối sử dụng `device_model` (biệt danh `device`), `system_version` (biệt danh `sdk`), `app_version`, `lang_code`, `system_lang_code` (biệt danh `system_lang_pack`), `lang_pack` và tùy chọn `tz_offset` (giây so với UTC, từ -43200 đến 50400). Các trường được cung cấp có ưu tiên cao hơn các giá trị mặc định được tạo tự động và ngôn ngữ của bảng điều khiển/trình duyệt . Các tên gọi khác nhau gây xung đột sẽ bị từ chối. Hồ sơ đã được giải quyết được lưu trong thông tin đăng nhập không gian làm việc được mã hóa và được tái sử dụng sau khi khởi động lại, bao gồm cả phiên bản ứng dụng của nó.
- `phone`, cài đặt proxy và mã thông báo thiết bị được **bỏ qua**. `twoFA` chỉ ở chế độ đọc khi **Tạo ủy quyền độc lập** được chọn; nhập trực tiếp sẽ bỏ qua nó.
- Một tệp JSON không có trường ủy quyền được hỗ trợ chỉ là siêu dữ liệu. Thêm tệp phiên làm việc của nó hoặc tiếp tục đăng nhập bằng điện thoại hoặc mã QR. Một tệp JSON chứa phiên làm việc được hỗ trợ hoặc Khóa ủy quyền (Auth Key) có thể tự thực hiện ủy quyền; xem [Account JSON](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData là thư mục `tdata` của ứng dụng Telegram Desktop (ứng dụng đa nền tảng từ desktop.telegram.org).

| Hệ thống | Vị trí mặc định `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (phiên bản Telegram di động: bên cạnh `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Để nhập dữ liệu:

> **Cảnh báo về phiên song song.** Nhập TData trực tiếp sẽ tái sử dụng khóa ủy quyền của Telegram Desktop. Không sử dụng khóa đó đồng thời trên Desktop và TgWitness. Telegram có thể vô hiệu hóa ủy quyền với `AUTH_KEY_DUPLICATED`, khiến cả hai bản sao không thể sử dụng được cho đến khi đăng nhập lại.
>
>
>
> Đóng hoàn toàn Desktop, bao gồm cả tiến trình trong khay hệ thống, và giữ bản sao đó ở trạng thái đóng trong khi TgWitness sử dụng phiên đã nhập. **: Đóng ứng dụng, không đăng xuất hoặc thu hồi phiên:** việc thu hồi cũng làm vô hiệu hóa bản sao đã nhập. Nếu bạn cần cả hai ứng dụng khách chạy cùng lúc, hãy chọn **Tạo ủy quyền độc lập** và giữ Desktop ở trạng thái đóng cho đến khi đăng nhập mới thành công, hoặc đăng nhập vào TgWitness bằng điện thoại hoặc mã QR. Nên sử dụng một tài khoản chuyên dụng, nhưng điều này không đảm bảo an toàn khi sử dụng các khóa nhân bản song song.
>
>
>
> Quy định này cũng áp dụng cho các `.session` , văn bản StringSession và mã khóa xác thực (Auth Key) dưới dạng HEX. Các ứng dụng khách khác có các phiên xác thực được tạo độc lập vẫn có thể duy trì trạng thái đã đăng nhập. Xin tham khảo [tài liệu về AUTH_KEY_DUPLICATED của Telegram](https://core.telegram.org/api/errors#406-not-acceptable).

1. Đóng hoàn toàn ứng dụng Telegram Desktop.
2. Vui lòng tạo một tệp ZIP **chỉ** chứa hai mục sau đây từ `tdata`:

   - `key_datas`
   - tệp gồm 16 ký tự kết thúc bằng `s` nằm ngay bên cạnh, thường là `D877F783D5D3EF8Cs`

   Việc nén toàn bộ thư mục cùng bộ nhớ đệm phương tiện thường vượt quá giới hạn (512 mục, 32 MiB sau khi giải nén). 3. Chọn tệp ZIP trong **phần Tệp**. Nếu Telegram Desktop có **mã thông báo cục bộ**, hãy nhập mã đó vào **ô Mã thông báo hoặc văn bản phiên** trước tiên. Đây không phải là mật khẩu xác thực hai yếu tố (2FA).

Hỗ trợ: một tài khoản cho mỗi kho lưu trữ, công nghệ lưu trữ hiện đại `key_datas`/`key_data0`/`key_data1`, mã thông báo cục bộ. Không hỗ trợ: các thư mục chứa nhiều tài khoản đã đăng nhập, các giao diện Desktop cũ, các tệp ZIP được bảo vệ bằng mật khẩu, và ứng dụng gốc riêng biệt trên macOS có tên “Telegram for macOS”.

### Telethon StringSession

Một dòng văn bản duy nhất, thường bắt đầu bằng `1` và dài khoảng 350 ký tự. Vui lòng tải tệp này dưới dạng tệp `.txt` hoặc `.tgwitness-session` (tối đa 4 KiB), hoặc dán vào phần **Mã thông báo hoặc văn bản phiên làm việc**. Chỉ chấp nhận các chuỗi Telethon; các chuỗi Pyrogram và TDLib sử dụng các định dạng khác.

### Tệp JSON tài khoản

Một đối tượng JSON, tối đa **64 KiB**, trong một tệp có phần mở rộng là **`.json`**.

| Trường (tên gọi khác) | Ý nghĩa |
| --- | --- |
| `api_id` (`app_id`) | ID ứng dụng, một số dương |
| `api_hash` (`app_hash`) | Băm ứng dụng, gồm 32 ký tự thập lục phân |
| `string_session` (`session_string`, `session_str`; `session` cũ) | Văn bản Telethon StringSession, không phải tên tệp |
| `auth_key` (`auth_key_hex`) + `dc_id` | Khóa xác thực (Auth Key) đầy đủ gồm 512 ký tự và DC 1–5 |
| `user_id` (`id`) | Tùy chọn; đã được đối chiếu với Telegram trước khi lưu thông tin ủy quyền |
| `device_model` (`device`) | Mô tả thiết bị kết nối |
| `system_version` (`sdk`) | Phiên bản hệ điều hành kết nối |
| `app_version` | Phiên bản ứng dụng được gửi đến Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Ngôn ngữ khách hàng, ngôn ngữ hệ thống và gói ngôn ngữ khách hàng; cho phép giá trị `lang_pack` trống |
| `tz_offset` | Chênh lệch múi giờ UTC (tùy chọn) tính bằng giây, được gửi trong trường `initConnection.params`; chuỗi số nguyên hoặc số thập phân |

Nếu cả tên gọi khác và tên chính đều có mặt, chúng phải trùng khớp. Các trường phiên Telethon rõ ràng có ưu tiên cao hơn so với blob `session` chung chung ở định dạng khác. Nếu cả hai đều chứa các phiên Telethon có thể nhận diện được, chúng phải mô tả cùng một quyền truy cập. Nếu không có trường rõ ràng, `session` phải là một StringSession Telethon hợp lệ. Ví dụ:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

Ví dụ đầu tiên chỉ yêu cầu điền thông tin đăng nhập API; quý vị có thể đăng nhập qua số điện thoại hoặc mã QR, hoặc thêm tệp phiên làm việc. Các danh sách hàng loạt (mảng JSON chứa danh sách tài khoản) sẽ không được chấp nhận.

## Xác định những gì quý vị đang có

| Quý vị có thể thấy | Đây là | Cách sử dụng |
| --- | --- | --- |
| `*.session`; khi mở tệp này trong trình soạn thảo văn bản, phần đầu sẽ hiển thị `SQLite format 3` | Telethon hoặc Pyrogram SQLite | **Tệp tin** (được phát hiện tự động) |
| Một thư mục `tdata` chứa `key_datas` | Telegram Desktop TData | Nén hai tệp thành định dạng ZIP, sau đó là **các tệp** |
| Một dòng văn bản bắt đầu bằng `1`, khoảng 350 ký tự | Telethon StringSession | **Tệp tin** |
| `*.json` cùng với `app_id`/`app_hash` | Siêu dữ liệu đi kèm | **Các tệp tin**, cùng với phiên làm việc tương ứng |
| `*.json` kết hợp với `auth_key` hoặc `string_session` | Tệp JSON tài khoản | **Tệp tin** |
| 512 ký tự `0-9a-f` | Khóa xác thực | **Khóa xác thực** |
| 32 ký tự `0-9a-f` | Băm API | **ID API + Băm** |
| `td.binlog` hoặc `db.sqlite` từ ứng dụng TDLib | Bộ lưu trữ TDLib | Không được hỗ trợ |
| `123456789:AA…` | Mã thông báo bot | Không được hỗ trợ |

## Các định dạng không được hỗ trợ

| Định dạng | Lựa chọn thay thế |
| --- | --- |
| Bộ lưu trữ TDLib (`td.binlog`) và các tệp xuất từ TDLib | Đăng nhập bằng số điện thoại hoặc mã QR |
| **Các chuỗi** phiên làm việc của Pyrogram | Vui lòng sử dụng tệp Pyrogram `.session`, hoặc quét mã QR bằng điện thoại |
| TData với nhiều tài khoản đã đăng nhập | Vui lòng đăng xuất khỏi các tài khoản khác trên Telegram Desktop, hoặc sử dụng tệp phiên làm việc riêng của từng tài khoản |
| Mã thông báo bot | Không được hỗ trợ: TgWitness chỉ thực hiện quan sát với tư cách là một tài khoản người dùng |
| Danh sách CSV/JSON của nhiều tài khoản | Nhập các tệp phiên được hỗ trợ qua **Tài khoản → Nhập tài khoản**, hoặc đăng nhập bằng số điện thoại/mã QR trong các không gian làm việc riêng biệt |
| Các phiên thử nghiệm (Test-DC) hoặc phiên bot | Vui lòng sử dụng tài khoản người dùng chính thức |

## Nhiều tài khoản

Hãy nhấn vào mã **+** bên cạnh trình chọn tài khoản, hoặc truy cập **Tài khoản → Cài đặt → Cài đặt kết nối → Không gian làm việc**, nhập tên nhãn và đăng nhập.

- Bất kỳ số lượng không gian làm việc nào, bao gồm cả không gian làm việc chính. Mỗi không gian làm việc đều có phiên làm việc, tuyến đường proxy , nguồn dữ liệu, chính sách ghi lại, sổ nhật ký, khóa ký, điểm kiểm tra và các tùy chọn xuất dữ liệu riêng biệt.
- Việc chuyển đổi không gian làm việc đang hiển thị sẽ không làm tạm dừng các không gian làm việc khác.
- Một sổ ghi chép luôn gắn liền với tài khoản đã tạo ra nó. Việc đăng nhập bằng một tài khoản khác yêu cầu phải có một không gian làm việc riêng, và một tài khoản không thể được gán cho hai không gian làm việc.
- Token bảng điều khiển chính quản lý tất cả các không gian làm việc. [Quyền truy cập được cấp](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/) có thể giới hạn quyền của người khác đối với các tài khoản và cuộc trò chuyện đã chọn, kèm theo các quyền truy cập riêng biệt và giới hạn phiên làm việc.
- **Tài khoản** sẽ đổi tên một không gian làm việc và xóa một không gian làm việc đã thêm vào, cùng với phiên làm việc, nhật ký, các nguồn và khóa ký của không gian đó. Không gian làm việc chính không thể bị xóa khỏi bảng điều khiển.

### Nhập hàng loạt và nhóm tài khoản

Sử dụng **Accounts → Import accounts** để thêm nhiều tài khoản, ghép nối các tệp theo tên gốc và xem kết quả đăng nhập của từng tài khoản. Mỗi tài khoản sẽ có không gian làm việc riêng.

Một nhóm giúp tập hợp các tài khoản có liên quan lại với nhau mà không hợp nhất các phiên, khóa hoặc bằng chứng của chúng. **Mở nhóm** trên **Tài khoản** dẫn đến trang của nó tại `/groups/<id>`:

- **Tài khoản:** lộ trình kết nối, thông tin quan sát và tin nhắn cuối cùng của từng thành viên, kèm theo Bắt đầu**tất cả** và **Tạm dừng tất cả**.
- **Cần chú ý:** các tài khoản đã đăng xuất, không khả dụng hoặc gặp vấn đề về kết nối, nhập liệu, nguồn hoặc phương tiện; mỗi tên sẽ dẫn đến thẻ thông tin tương ứng.
- **Các cuộc trò chuyện trên nhiều tài khoản hiển thị:** các nguồn được chia sẻ, các tài khoản đang theo dõi chúng và các gián đoạn trong khoảng thời gian quan sát không gian làm việc có sẵn (tối đa bảy ngày). **Khi xuất với N tài khoản,** quá trình xuất kênh hoặc siêu nhóm sẽ được chia đều giữa các tài khoản này và tạo ra một tệp lưu trữ duy nhất.
- **Xuất nhóm:** một ZIP chứa bản xuất đã được ký của từng tài khoản dưới `accounts/` và `manifest.json` liệt kê các SHA-256 và dấu vân tay khóa của chúng, được ký bởi không gian làm việc chính trong `manifest.signature.json`. Xác minh từng bản lưu trữ tài khoản riêng lẻ bằng `python -m tgwitness.verify` và dấu vân tay đáng tin cậy của tài khoản đó.

Các thành viên chia sẻ cài đặt chung của nhóm; mỗi tài khoản có thể giữ nguyên các giá trị riêng của mình. Xem [phần cài đặt chung](https://phishdestroy.github.io/TgWitness/vi/docs/reference/settings/#account-groups), [hướng dẫn nhập dữ liệu và quản lý nhóm](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) cùng với [bảng điều khiển nhóm MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Đăng xuất

**Tài khoản → Đăng xuất khỏi Telegram** (với chế độ quan sát tạm dừng) sẽ yêu cầu Telegram kết thúc phiên làm việc, do đó phiên này cũng sẽ biến mất khỏi mục **Cài đặt → Thiết bị** của tài khoản, đồng thời xóa phiên làm việc khỏi kho lưu trữ không gian làm việc. Nhật ký, các nguồn, cài đặt và khóa ký vẫn được giữ lại, và nhật ký sẽ ghi lại thao tác đăng xuất này. Không gian làm việc vẫn thuộc về tài khoản đó: chỉ có tài khoản đó mới có thể kết nối lại với nó. Nếu Telegram không phản hồi, phiên làm việc vẫn sẽ bị xóa tại đây và bảng điều khiển sẽ hiển thị thông báo tương ứng; quý vị hãy kết thúc phiên làm việc trong Telegram tại **Cài đặt → Thiết bị**.

## Bảo vệ an toàn cho các tệp tài khoản

- Hãy coi mọi `.session`, TData ZIP, StringSession, Auth Key và tệp JSON tài khoản như một mật khẩu. TgWitness lưu trữ thông tin ủy quyền đã nhập vào kho lưu trữ được mã hóa của mình; quý vị có thể xóa các tệp gốc sau đó.
- Không được thực hiện cùng một quy trình ủy quyền trên hai chương trình cùng lúc. Telegram có thể thu hồi ủy quyền đó (`AUTH_KEY_DUPLICATED`), và cả hai bản sao sẽ ngừng hoạt động.
- Một phiên làm việc đã hết hạn hoặc bị thu hồi không thể được khôi phục thông qua quá trình chuyển đổi. Vui lòng đăng nhập lại.

## Khắc phục sự cố

| Tin nhắn hoặc triệu chứng | Hướng dẫn thực hiện |
| --- | --- |
| *Không thể đọc phiên làm việc này. Vui lòng đóng ứng dụng gốc…* | Tệp SQLite hiện đang mở hoặc chưa hoàn tất (tệp phụ `-journal`/`-wal`). Vui lòng đóng chương trình gốc một cách đúng quy trình và sao chép lại tệp. |
| *Các lược đồ SQLite của Telethon được hỗ trợ: 7 và 8* / *Pyrogram … 2 và 3* | Tệp này được tạo ra bởi một phiên bản thư viện rất cũ hoặc không xác định. Vui lòng đăng nhập bằng số điện thoại hoặc mã QR thay thế. |
| *Chỉ hỗ trợ các phiên làm việc của người dùng được ủy quyền* | Tệp Pyrogram này thuộc về một bot hoặc mạng thử nghiệm. |
| *Kho lưu trữ TData đã vượt quá 512 mục hoặc 32 MiB* | Chỉ bao gồm các tệp ZIP `key_datas` và `D877F783D5D3EF8Cs`, không bao gồm toàn bộ thư mục. |
| *Không thể giải mã TData. Vui lòng kiểm tra mật mã cục bộ trên máy tính để bàn* | Vui lòng nhập mã mật khẩu cục bộ của Telegram Desktop vào ô **“Mật khẩu” hoặc “Văn bản phiên làm việc**”. |
| *Nhập từng tài khoản TData một* | Telegram Desktop hỗ trợ nhiều tài khoản; vui lòng tham khảo phần [“Các định dạng không được hỗ trợ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#unsupported-formats)”. |
| *Các tệp được chọn mô tả các tài khoản hoặc thông tin đăng nhập API khác nhau* | Chỉ chọn các tệp tin từ một tài khoản duy nhất. |
| *Tệp JSON không chứa thông tin xác thực hoặc ủy quyền API nào được hỗ trợ* | Vui lòng kiểm tra các tên trường trong tệp [JSON Tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#account-json). |
| *Chỉ bao gồm siêu dữ liệu API* | Tệp JSON không có phiên làm việc. Vui lòng thêm tệp `.session` hoặc sử dụng số điện thoại/mã QR. |
| *Mã khóa xác thực (Auth Key) dưới dạng HEX phải chứa đầy đủ 512 ký tự thập lục phân* | Khóa đã bị cắt ngắn hoặc chứa chuỗi ký tự "`…`". |
| ID tài khoản không khớp với tài khoản đã nhập | ID người dùng trong tệp này khác với thông tin mà Telegram báo cáo; tệp này thuộc về một tài khoản khác. |
| Tài khoản này hiện đã thuộc về một không gian làm việc khác | Vui lòng mở không gian làm việc đó thay vì thêm tài khoản hai lần. |
| Đã kết nối, nhưng danh sách trò chuyện trong **phần Nguồn** còn thiếu một nhóm riêng tư | Kiểm tra tư cách thành viên. Công cụ chọn lọc sẽ kiểm tra 1.000 cuộc đối thoại đầu tiên; quý vị có thể tăng giới hạn này trong **phần Thông số**. |
| Kết nối proxy không thành công | Kiểm tra chế độ định tuyến và IP. Tự động MTProxy sẽ thử một mục nhập khác đang hoạt động. Chế độ ẩn địa chỉ sẽ chờ; chế độ Trực tiếp (Direct) là phương án cuối cùng, có thể kết nối trực tiếp sau thời gian trễ đã cấu hình. Xem [các chế độ định tuyến](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/#ip-modes). |

Xem thêm: các vấn đề về [kết nối và bảo mật](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/) liên quan đến máy chủ proxy và mã hóa, cũng như [cách thức thu thập dữ liệu](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/) đối với những nội dung được ghi lại sau khi đăng nhập.
