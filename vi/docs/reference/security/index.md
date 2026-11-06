# An ninh và xử lý dữ liệu

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/security/

Mô hình mối đe dọa, mô hình truy cập, thông tin bí mật khi không được sử dụng, mức độ phơi bày mạng, nhập dữ liệu phiên làm việc và cách báo cáo lỗ hổng bảo mật.

This page describes access, storage and network protection in a local or server workspace. For collection on a GitHub runner or in an Intel TDX confidential VM, see the [verification modes](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope), which add checks of the collection environment. Account connections, notifications, timestamps, off-site copies and witnesses have their own routing settings.

| Lĩnh vực | Tóm lại |
| --- | --- |
| Truy cập | Khóa quản trị viên cùng với quyền truy cập có phạm vi giới hạn vào các tài khoản/cuộc trò chuyện, bảy cấp quyền và các phiên làm việc có thể thu hồi; mặc định là localhost |
| Thông tin bí mật khi không được truy cập | Các thông tin về phiên làm việc, cặp API, khóa ký và cài đặt proxy đều được mã hóa bằng thuật toán Fernet |
| Tin nhắn và phương tiện truyền thông | Dữ liệu được lưu trữ dưới dạng không mã hóa: vui lòng sử dụng tính năng mã hóa đĩa và thiết lập quyền truy cập nghiêm ngặt |
| Tính toàn vẹn | Chuỗi băm SHA-256 và chữ ký Ed25519 trên mỗi bản ghi |
| Ranh giới tin cậy cục bộ | The host administrator controls the workspace and its signing key; independent checkpoints retain an earlier journal boundary |

Để biết thêm thông tin về việc báo cáo lỗ hổng bảo mật, vui lòng tham khảo chính [sách bảo mật](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

## Mô hình truy cập

Mã thông báo bảng điều khiển chính cấp quyền kiểm soát toàn diện. Những người khác có thể nhận được [quyền truy cập có phạm vi giới hạn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/) riêng: các không gian làm việc và cuộc trò chuyện được chọn, quyền hạn, thời hạn hiệu lực, hạn chế IP, giới hạn đăng nhập và các phiên có thể thu hồi. Quyền truy cập giới hạn trong cuộc trò chuyện sẽ không thể thực hiện các thao tác trên toàn bộ không gian làm việc ngay cả khi quyền hạn của họ đã được chọn. Các không gian làm việc chia sẻ cùng một quy trình và không cách ly dữ liệu khỏi quản trị viên máy chủ.

Theo mặc định, bảng điều khiển sẽ lắng nghe trên localhost. Quá trình đăng nhập qua trình duyệt sẽ trao đổi một mã thông báo truy cập để lấy thông tin xác thực phiên; trình duyệt sẽ gửi mã thông báo này dưới dạng mã thông báo mang theo. Mã thông báo này được lưu trữ trong sessionStorage thay vì trong cookie xác thực. Việc khóa/đăng xuất sẽ xóa phiên trình duyệt. Việc đóng trình duyệt hoặc kết thúc phiên không làm ngừng quá trình thu thập dữ liệu.

Các mã thông báo đã phát hành và thông tin xác thực phiên làm việc được lưu trữ dưới dạng hàm băm trong kho lưu trữ được mã hóa. Việc thu hồi sẽ chấm dứt các phiên làm việc liên quan; các thay đổi về quyền truy cập sẽ ảnh hưởng đến các yêu cầu tiếp theo. Các tệp đã tải xuống không thể thu hồi lại được. Quản trị viên cũng có thể giới hạn các phiên trình duyệt của chính mình, nhưng các tập lệnh sử dụng trực tiếp mã thông báo trên bảng điều khiển chính vẫn giữ quyền truy cập đầy đủ và vượt qua các giới hạn của phiên trình duyệt đó.

Các trường hợp xác thực không thành công sẽ bị giới hạn tần suất theo địa chỉ máy khách. Các hạn chế về IP dựa trên địa chỉ mà ứng dụng nhận diện được; vui lòng kiểm tra hành vi của máy chủ proxy ngược trước khi dựa vào tính năng này. Thông tin đăng nhập của Witness vẫn là các thông tin đăng nhập riêng biệt, chỉ dành cho việc kiểm tra trạng thái và điểm kiểm tra.

### Truy cập bản demo

`/api/demo-access` là một quá trình khởi động không được xác thực có chủ đích dành cho một bản demo tổng hợp được khởi chạy rõ ràng và tách biệt. Nó cấp một quyền hạn có thời hạn tồn tại riêng biệt cho quá trình, không bao giờ là mã thông báo bảng điều khiển thực hay một giá trị ghi đè TGWITNESS_TOKEN. Việc cấp phát và sử dụng yêu cầu một đối tác loopback và Máy chủ, không có tiêu đề được chuyển tiếp và không có yêu cầu xuyên nguồn gốc. Các không gian làm việc bổ sung hoặc phiên được ủy quyền sẽ vô hiệu hóa đường dẫn này. Các không gian làm việc đang hoạt động không bao giờ cấp phát khả năng này. Bản demo không thể kết nối tài khoản hoặc thay đổi cài đặt thu thập dữ liệu.

## Nội dung bảng điều khiển và các tệp xuất

Bảng điều khiển này không sử dụng phông chữ bên ngoài, công cụ phân tích, tài nguyên CDN hay phương tiện truyền thông từ xa được nhúng. Văn bản lấy từ Telegram được chèn dưới dạng văn bản thuần túy, không phải HTML. Các tệp đính kèm đã tải xuống được cung cấp dưới dạng tệp đính kèm nhị phân. Các tệp xuất định dạng JSONL giữ nguyên các chuỗi ký tự gốc; định dạng HTML sẽ mã hóa chúng; các ô trong tệp CSV có khả năng chứa công thức sẽ được thêm dấu nháy đơn ở đầu.

Các tệp xuất ra không bao gồm thông tin xác thực và khóa ký, nhưng cố ý chứa siêu dữ liệu nguồn đã thu thập, các mã định danh, và có thể bao gồm nội dung cá nhân hoặc nhạy cảm. Các giá trị băm truy cập Telegram và tham chiếu tệp có thể xuất hiện trong siêu dữ liệu nguồn thô.

## Thông tin bí mật khi không được truy cập

Telegram API credentials, the session and signing key are encrypted with Fernet. For local messages and media, encryption is provided by the host's disk or volume; the workspace stores ordinary files. Exports can use a password-protected AES-256 ZIP, and off-site copies use AES-256-GCM.

The vault key defaults to the protected data directory. Use an external master-key file below to store it separately. On Unix, new private-key files use mode 0600 and new data directories use 0700; on Windows, set the directory ACL for the service account and authorized administrators. Existing directory permissions are retained.

### Khóa chính bên ngoài

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode. Disk encryption protects the local message and media files in either mode; see [connection and data protection](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/) for setup details.

## Máy chủ proxy và các tuyến mạng

Cấu hình proxy được mã hóa trong kho lưu trữ. Mật khẩu và thông tin bí mật của MTProxy không được API trả về cũng như không được ghi vào các bản ghi bằng chứng. Mỗi không gian làm việc sẽ tự chọn tuyến đường Telegram và [chế độ IP](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/#ip-modes) của riêng mình.

**Tính năng Ẩn địa chỉ** từ chối chế độ dự phòng Telegram trực tiếp và yêu cầu sử dụng proxy cho các yêu cầu HTTP bên ngoài. Chế độ dự phòng được chọn rõ ràng cho phép truy cập Telegram trực tiếp sau thời gian trễ; chế độ đường hầm/VPN cho phép các tuyến đường trực tiếp. Việc chọn chế độ đường hầm không cài đặt hoặc xác minh VPN. Các cài đặt này không kiểm soát toàn bộ lưu lượng máy tính, trình duyệt, trình quản lý gói phần mềm hoặc việc giải quyết DNS của máy chủ proxy cục bộ.

MTProxy chỉ truyền tải lưu lượng Telegram. Các yêu cầu bên ngoài có thể sử dụng một proxy SOCKS5/HTTP riêng biệt, tuyến SOCKS5/HTTP của không gian làm việc hoặc một tuyến trực tiếp được phép; các yêu cầu này cũng có thể bị vô hiệu hóa. Công cụ chứng thực độc lập có các cài đặt truyền tải riêng. Quá trình xác thực SOCKS5/HTTP CONNECT thông thường không được mã hóa bởi chính các giao thức proxy này. Các khóa bí mật TLS giả mạo của MTProxy vẫn chưa được hỗ trợ.

## Đăng nhập và nhập dữ liệu phiên làm việc

Các tệp .tgwitness-session đã chuyển đổi chứa mã bí mật ủy quyền dưới dạng văn bản thuần túy cho đến khi được tải lên và lưu trữ trong kho dữ liệu. Giao diện dòng lệnh ngoại tuyến (CLI) chấp nhận các lược đồ Telethon đã được kiểm duyệt. Tính năng nhập từ bảng điều khiển còn hỗ trợ các định dạng Pyrogram SQLite, tệp ZIP TData hiện đại dành cho một tài khoản duy nhất, và các đầu vào JSON đã được ghi chép đầy đủ. Tính năng này được xác thực, giới hạn ở bốn tệp / 8 MiB, và xử lý các tệp tải lên trong bộ nhớ mà không cần giải nén kho lưu trữ hay lưu giữ các tệp gốc. Thông tin xác thực đã được chuẩn hóa chỉ được trả về cho trình duyệt đã xác thực gửi yêu cầu; chúng được lưu trữ trong kho dữ liệu được mã hóa sau khi quá trình ủy quyền Telegram thành công. Hãy bảo vệ các tệp gốc và tệp đã chuyển đổi, đồng thời tránh tình trạng các khách hàng đồng thời sao chép thông tin ủy quyền.

Quá trình xử lý dữ liệu sẽ xác minh tổng kiểm tra của container, các hàm băm giải mã cục bộ và độ dài cấu trúc. Mật mã cục bộ trên Desktop được cung cấp chỉ được sử dụng tạm thời và không được lưu trữ. Trình phân tích cú pháp có giới hạn này không đảm bảo rằng mọi phiên bản Desktop đều tương thích. Các hình ảnh mã QR được tạo cục bộ, chứa các mã thông báo đăng nhập Telegram có thời hạn ngắn và không bao giờ được gửi đến dịch vụ hiển thị bên ngoài. Việc khóa thiết bị, chuyển đổi không gian làm việc, đăng nhập mới và thay đổi đường dẫn sẽ hủy bỏ các nỗ lực quét mã QR đang chờ xử lý. Việc tải lại hoặc đóng tab có thể khiến một nỗ lực quét mã QR vẫn đang chờ xử lý cho đến khi hết hạn. Việc đăng nhập bằng mã QR thành công vẫn yêu cầu liên kết tài khoản. Các nội dung API thông thường vẫn bị giới hạn ở mức 16 KiB; đường dẫn nhập đã được xác thực chấp nhận tối đa 12 MiB JSON được mã hóa, đồng thời áp dụng riêng giới hạn nhỏ hơn đối với tệp đã giải mã.

Mã đăng nhập và mật khẩu xác minh hai bước của Telegram sẽ không được lưu trữ lâu dài. Trạng thái băm của số điện thoại/mã được giữ trong bộ nhớ trong quá trình xác thực. Các phiên Telegram cấp quyền truy cập tài khoản; tuyệt đối không tải lên GitHub bất kỳ thư mục dữ liệu, phiên, mã thông báo, khóa kho lưu trữ hoặc khóa ký riêng tư nào.

## Nhật ký và truyền tải

Phản hồi xác thực API mặc định đã được thay thế để không hiển thị lại các giá trị thông tin đăng nhập. Tính năng ghi nhật ký truy cập ứng dụng đã bị vô hiệu hóa. Quý vị không nên cấu hình máy chủ proxy ngược để ghi lại các tiêu đề Authorization hoặc nội dung yêu cầu. Giao thức HTTP truyền các mã thông báo và thông tin đăng nhập dưới dạng văn bản thuần túy: hãy sử dụng HTTPS hoặc đường hầm SSH mỗi khi kết nối ra khỏi localhost.

## Giới hạn về tính toàn vẹn

Local verification checks record signatures, the hash chain, attachments and the export manifest. The administrator holds the local signing key and can create another signed journal; an independently retained checkpoint detects replacement of the prefix it covers. Keep the key fingerprint and checkpoints with the recipient or an independent witness.

For independently checked collection, choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/vi/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Their verifiers check workflow provenance or hardware measurements in addition to archive integrity. Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies; the [evidence format](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope) describes the checks for each mode.

## Nếu quý vị nghi ngờ có vấn đề

Preserve the original data directory and use a separate copy for analysis. Report the affected version, operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), keeping account data and credentials private.
