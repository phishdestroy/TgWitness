# An ninh và xử lý dữ liệu

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/security/

Mô hình mối đe dọa, mô hình truy cập, thông tin bí mật khi không được sử dụng, mức độ phơi bày mạng, nhập dữ liệu phiên làm việc và cách báo cáo lỗ hổng bảo mật.

Trang này mô tả các khía cạnh về quyền truy cập, lưu trữ và bảo vệ mạng trong môi trường làm việc cục bộ hoặc trên máy chủ. Để thu thập dữ liệu trên GitHub Runner hoặc trong máy ảo bảo mật Intel TDX, hãy tham khảo các chế độ [xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope), vốn bổ sung các kiểm tra đối với môi trường thu thập. Kết nối tài khoản, thông báo, dấu thời gian, bản sao ngoài site và các nhân chứng đều có cài đặt định tuyến riêng.

| Lĩnh vực | Tóm lại |
| --- | --- |
| Truy cập | Khóa quản trị viên cùng với quyền truy cập có phạm vi giới hạn vào các tài khoản/cuộc trò chuyện, bảy cấp quyền và các phiên làm việc có thể thu hồi; mặc định là localhost |
| Thông tin bí mật khi không được truy cập | Các thông tin về phiên làm việc, cặp API, khóa ký và cài đặt proxy đều được mã hóa bằng thuật toán Fernet |
| Tin nhắn và phương tiện truyền thông | Dữ liệu được lưu trữ dưới dạng không mã hóa: vui lòng sử dụng tính năng mã hóa đĩa và thiết lập quyền truy cập nghiêm ngặt |
| Tính toàn vẹn | Chuỗi băm SHA-256 và chữ ký Ed25519 trên mỗi bản ghi |
| Ranh giới tin cậy cục bộ | Quản trị viên máy chủ kiểm soát không gian làm việc và khóa ký của nó; các điểm kiểm tra độc lập lưu giữ ranh giới nhật ký trước đó |

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

Thông tin đăng nhập API Telegram, khóa phiên và khóa ký được mã hóa bằng thuật toán Fernet. Đối với tin nhắn và phương tiện truyền thông cục bộ, việc mã hóa được thực hiện trên đĩa hoặc phân vùng của máy chủ; không gian làm việc lưu trữ các tệp thông thường. Các tệp xuất có thể sử dụng định dạng ZIP được bảo vệ bằng mật khẩu theo tiêu chuẩn AES-256, và các bản sao lưu ngoài site sử dụng AES-256-GCM.

Khóa kho lưu trữ mặc định nằm trong thư mục dữ liệu được bảo vệ. Sử dụng tệp khóa chính bên ngoài dưới đây để lưu trữ riêng biệt. Trên Unix, các tệp khóa riêng tư mới sử dụng chế độ 0600 và các thư mục dữ liệu mới sử dụng 0700; trên Windows, thiết lập quyền truy cập (ACL) cho thư mục dành cho tài khoản dịch vụ và các quản trị viên được ủy quyền. Các quyền truy cập hiện có của thư mục sẽ được giữ nguyên.

### Khóa chính bên ngoài

Đối với thư mục dữ liệu mới, TGWITNESS_VAULT_KEY_FILE có thể cung cấp một khóa chính ngẫu nhiên từ bên ngoài. HKDF-SHA256 và một giá trị muối ngẫu nhiên riêng biệt sẽ tạo ra một khóa Fernet khác nhau cho mỗi không gian làm việc. Tệp vault.external.json phải được giữ lại để phục hồi. Nếu thiếu hoặc khóa chính sai, hệ thống sẽ không hoạt động. Các kho lưu trữ cục bộ hiện có sẽ không được di chuyển tự động. Bảng điều khiển hiển thị chế độ lưu trữ khóa đã chọn. Mã hóa đĩa bảo vệ các tệp tin tin nhắn và phương tiện cục bộ trong cả hai chế độ; xem [phần kết nối và bảo vệ dữ liệu](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/) để biết chi tiết thiết lập.

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

Các kiểm tra xác minh cục bộ kiểm tra chữ ký, chuỗi băm, tệp đính kèm và bản kê khai xuất khẩu. Quản trị viên nắm giữ khóa ký cục bộ và có thể tạo một nhật ký có chữ ký khác; một điểm kiểm tra được lưu trữ độc lập sẽ phát hiện việc thay thế tiền tố mà nó bao phủ. Giữ dấu vân tay khóa và các điểm kiểm tra với người nhận hoặc một nhân chứng độc lập.

Đối với việc thu thập dữ liệu được kiểm tra độc lập, hãy chọn [phương thức thu thập qua](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) [GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) hoặc [triển khai qua Intel TDX](https://phishdestroy.github.io/TgWitness/vi/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Các công cụ xác minh của họ kiểm tra nguồn gốc quy trình làm việc hoặc các phép đo phần cứng bên cạnh tính toàn vẹn của kho lưu trữ. Dấu thời gian tùy chọn và các bản sao được mã hóa lưu trữ ngoài địa điểm cung cấp mốc thời gian và bản sao có thể khôi phục; [định dạng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope) [bằng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope) [chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope) mô tả các bước kiểm tra cho từng chế độ.

## Nếu quý vị nghi ngờ có vấn đề

Giữ nguyên thư mục dữ liệu gốc và sử dụng một bản sao riêng biệt để phân tích. Báo cáo phiên bản bị ảnh hưởng, thao tác và các bước có thể tái hiện thông qua chính sách [bảo mật](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), đồng thời giữ bí mật dữ liệu tài khoản và thông tin đăng nhập.
