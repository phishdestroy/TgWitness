# Quyền truy cập và quyền hạn

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/

Quản lý quyền truy cập vào các tài khoản và cuộc trò chuyện, chọn quyền hạn, giới hạn phiên truy cập và địa chỉ IP, cũng như thu hồi quyền truy cập.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/vi/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

Cấp quyền truy cập cho người đánh giá vào một cuộc trò chuyện, cấp quyền cho nhà phân tích để xuất dữ liệu vụ việc, hoặc cấp quyền kiểm soát các tài khoản đã chọn cho người vận hành. Mỗi người sẽ nhận được mã thông báo riêng. Mã thông báo trên bảng điều khiển chính sẽ do quản trị viên nắm giữ.

[Thiết lập tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/) · [Các tuyến kết nối](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/) · [Mô hình bảo mật](https://phishdestroy.github.io/TgWitness/vi/docs/reference/security/)

## Hai phạm vi, hai nhiệm vụ khác nhau

**Phạm vi thu thập** quyết định những gì một tài khoản sẽ ghi lại: các cuộc trò chuyện được chọn, một thư mục Telegram hoặc toàn bộ tài khoản. **Phạm vi truy cập** quyết định những tài khoản và cuộc trò chuyện đã được ghi lại nào mà người khác có thể xem và sử dụng. Việc cấp quyền truy cập không đồng nghĩa với việc tham gia cuộc trò chuyện trên Telegram, bắt đầu quá trình thu thập hay cấp quyền truy cập vào tài khoản Telegram.

Một quyền truy cập có thể mở các không gian làm việc được chọn, các cuộc trò chuyện được chọn trong đó, tất cả các không gian làm việc hoặc mọi tài khoản trong một [nhóm tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#bulk-import-and-account-groups). **Tất cả các không gian làm việc, bao gồm cả những không gian được thêm vào sau này**, cũng bao gồm các tài khoản trong tương lai. Quyền truy cập nhóm cũng bao gồm các tài khoản được thêm vào nhóm đó sau này. Hãy chọn các không gian làm việc một cách rõ ràng khi một vụ việc cần được giới hạn trong phạm vi của chúng.

## Cấp quyền truy cập cho ai đó

1. Vui lòng đăng nhập với tư cách quản trị viên chính và mở **mục Truy cập**.
2. Trong phần **“Cấp quyền truy cập cho ai đó**”, vui lòng nhập tên mà quý vị có thể nhận ra trong nhật ký.
3. Vui lòng chọn các không gian làm việc và, khi cần thiết, các cuộc trò chuyện riêng lẻ.
4. Vui lòng chọn những hành động mà người này có thể thực hiện. Tính năng **“Xem”** luôn được bao gồm.
5. Vui lòng thiết lập thời hạn hiệu lực, giới hạn đăng nhập/phiên làm việc và các địa chỉ được phép theo nhu cầu.
6. Nhấn vào **“Tạo quyền truy cập**”. Sao chép mã thông báo ngay bây giờ: mã này chỉ hiển thị một lần duy nhất.
7. Vui lòng gửi địa chỉ bảng điều khiển và mã thông báo một cách riêng tư. Người nhận sẽ nhập mã thông báo đó trên trang đăng nhập thông thường; họ không cần mã thông báo bảng điều khiển chính của quý vị hay phiên Telegram nào cả.

Vui lòng mở bảng điều khiển có chứa mã thông báo đã được cấp trong một phiên trình duyệt riêng biệt và kiểm tra các cuộc trò chuyện hiển thị cũng như các thao tác được phép trước khi chuyển giao mã thông báo này.

## Chọn các quyền truy cập

Để thực hiện trình diễn công khai chỉ chứa văn bản, hãy sử dụng **“Trình diễn công khai”** thay vì quyền truy cập người đánh giá thông thường. Tính năng này hiển thị các kênh công khai được chọn rõ ràng, các thao tác chỉnh sửa và xóa đã được lưu giữ, cùng với số liệu thống kê đã được ký xác nhận, trong đó các trường tác giả được che đi và các tệp được đóng lại tại ranh giới API. [Tạo và xác minh một trình diễn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/showcase/).

| Quyền sử dụng | Các tính năng mà công cụ này cung cấp |
| --- | --- |
| `view` | Xem các cuộc trò chuyện được phép truy cập, tin nhắn đã ghi lại, hồ sơ cá nhân, tệp tin và các bản ghi nhật ký đã được lọc. Luôn được bao gồm đầy đủ. |
| `export` | Cho phép xuất lịch sử trò chuyện và hồ sơ. Việc xuất toàn bộ bằng chứng trong không gian làm việc yêu cầu quyền truy cập vào toàn bộ không gian làm việc đó. |
| `sources` | Quản lý nguồn, ảnh chụp nhanh và thu thập thông tin hồ sơ. Quyền truy cập giới hạn theo cuộc trò chuyện chỉ có hiệu lực đối với các cuộc trò chuyện được phép; việc phát hiện nguồn và cài đặt phạm vi trên toàn tài khoản vẫn được giữ ở trạng thái đóng. |
| `collect` | Khởi động hoặc dừng trình thu thập dữ liệu. Yêu cầu quyền truy cập toàn bộ không gian làm việc vì quá trình thu thập sẽ ảnh hưởng đến tài khoản. |
| `interact` | Thực hiện các tương tác được hỗ trợ trên Telegram trong phạm vi quyền truy cập. Quyền truy cập giới hạn ở chế độ trò chuyện không thể sử dụng tính năng xem trước liên kết trên toàn tài khoản. |
| `settings` | Thay đổi cài đặt thu thập dữ liệu, dấu thời gian, thông báo, bản sao lưu ngoài trang web và các thông số. Yêu cầu quyền truy cập toàn bộ không gian làm việc. |
| `account` | Đăng nhập hoặc đăng xuất khỏi Telegram và quản lý các tuyến kết nối. Yêu cầu quyền truy cập toàn bộ không gian làm việc. |
| `board.read` | Chỉ được đọc các ghi chú trên Bảng vụ án trong phạm vi không gian làm việc và các cuộc trò chuyện được phép. |
| `board.write` | Thêm dấu trang, đánh dấu nổi bật, đoạn trích, bình luận và trạng thái mở/xem lại. Cũng cần có chức năng ``board.read``. |
| `board.manage` | Quản lý các bộ sưu tập, trạng thái cuối cùng của nhóm và thẻ của các thành viên khác. Ngoài ra, cần quyền đọc/ghi trên bảng điều khiển. |

Quyền truy cập và phạm vi sẽ được kiểm tra đồng thời. Việc chọn một quyền truy cập sẽ không mở các cuộc trò chuyện khác hoặc kích hoạt thao tác trên toàn không gian làm việc đối với quyền truy cập bị giới hạn trong một cuộc trò chuyện cụ thể. Để thực hiện xuất song song, quyền truy cập phải bao gồm cuộc trò chuyện được xuất trong mọi tài khoản đã chọn. Một quyền truy cập đã được cấp không thể tạo ra các quyền truy cập mới, quản lý các phiên làm việc của người khác hoặc mở bảng điều khiển quản trị viên.

### Ba cách thiết lập hữu ích

| Người | Phạm vi | Quyền truy cập |
| --- | --- | --- |
| Người đánh giá | Các cuộc trò chuyện được ghi lại trong một vụ việc | `view` |
| Chuyên viên phân tích đang chuẩn bị bàn giao công việc | Các cuộc trò chuyện cần điều tra và xuất dữ liệu | `view`, `export`; chỉ thêm `interact` nếu họ cần thực hiện các thao tác thông qua Telegram |
| Nhân viên thu thập dữ liệu | Các không gian làm việc được chọn lọc | `view`, `sources`, `collect`; chỉ thêm `settings` hoặc `account` khi cần thiết |

Các cài đặt mặc định ban đầu của biểu mẫu Access cũng bao gồm Bảng vụ việc: Người xem xét có thể đọc, Nhà phân tích có thể đọc và viết, còn Người vận hành có thể quản lý. Các cài đặt mặc định vẫn có thể chỉnh sửa, và các quyền truy cập hiện có sẽ không được mở rộng tự động. Xem [Bảng vụ việc](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-board/) để biết phạm vi trò chuyện được kế thừa và quyền riêng tư khi xuất dữ liệu.

## Giới hạn và phiên làm việc

| Bối cảnh | Cách thức hoạt động |
| --- | --- |
| Các phiên họp song song | Hạn chế số phiên truy cập đồng thời từ 1 đến 100. Khi đạt đến giới hạn này, hệ thống sẽ từ chối lần đăng nhập tiếp theo hoặc kết thúc phiên truy cập lâu đời nhất. |
| Cho phép đăng nhập | Hạn chế số lần sử dụng thành công mã thông báo để bắt đầu các phiên làm việc. Các phiên làm việc hiện có sẽ không bị kết thúc chỉ vì lần đăng nhập được phép cuối cùng đã được sử dụng. |
| Hiệu lực đến | Thời hạn truy cập đã hết hiệu lực hoàn toàn. Tài khoản đã hết hạn không thể đăng nhập hoặc tiếp tục thực hiện các yêu cầu. |
| Thời gian không có hoạt động | Thời gian chờ do không hoạt động trong phiên, từ 5 phút đến 30 ngày. Các yêu cầu thành công sẽ gia hạn thời gian này; một bảng điều khiển đang mở có thể duy trì trạng thái hoạt động bằng cách thực hiện các yêu cầu kiểm tra định kỳ. |
| Các địa chỉ được phép | Chấp nhận các địa chỉ IP cụ thể hoặc các mạng con CIDR. Để trống để cho phép bất kỳ địa chỉ nào, trừ khi tính năng ràng buộc lần đăng nhập đầu tiên được kích hoạt. |
| Liên kết với lần đăng nhập đầu tiên | Lần đăng nhập thành công đầu tiên sẽ xác định địa chỉ được phép cho lần truy cập đó. |

Địa chỉ IP là địa chỉ máy khách mà ứng dụng nhận diện được. Trong trường hợp sử dụng proxy ngược hoặc đường hầm, vui lòng kiểm tra địa chỉ hiển thị trong **phần “Các phiên đang mở”** trước khi áp dụng các quy tắc dựa trên IP: nếu không, nhiều người dùng có thể bị nhận diện là đang chia sẻ cùng một địa chỉ proxy.

## Thay đổi hoặc thu hồi quyền truy cập

Chỉnh sửa một mục trong **phần “Granted access” (Quyền truy cập đã cấp)** để thay đổi phạm vi, quyền hoặc giới hạn của nó. Các thay đổi về phạm vi và quyền sẽ được kiểm tra trên các yêu cầu tiếp theo, bao gồm các yêu cầu từ các phiên đang mở. Việc thu hồi quyền truy cập sẽ kết thúc các phiên đó và khiến mã thông báo đã cấp không còn sử dụng được. **Tính năng “Open sessions” (Phiên đang mở)** cũng cho phép quản trị viên kết thúc một phiên riêng lẻ mà không cần thu hồi toàn bộ quyền truy cập.

Các bản sao xuất đã lưu giữ nguyên thông tin về người tạo, không gian làm việc, phạm vi cuộc trò chuyện và các quyền truy cập cần thiết. Quyền truy cập được cấp chỉ cho phép liệt kê hoặc tải xuống các bản sao của chính nó trong thời gian các quyền đó còn hiệu lực; các bản sao chứa Case Board cũng yêu cầu quyền ``board.read``. Quản trị viên có thể truy xuất tất cả các bản sao. Các bản sao cũ hơn không có siêu dữ liệu này và các gói nhóm chỉ dành riêng cho quản trị viên. Tải xuống phiếu yêu cầu và các tệp phản hồi đã chuẩn bị sẽ kiểm tra lại quyền truy cập sau khi chuẩn bị tệp, trước khi gửi các byte của tệp đó.

Việc thu hồi không thể khôi phục các tệp mà người dùng đã tải xuống. Việc đăng xuất, khóa bảng điều khiển hoặc kết thúc phiên làm việc sẽ không làm dừng trình thu thập đang hoạt động.

## Những thông tin mà quản trị viên có thể xem

Người đánh giá và nhà phân tích nhận được tiến độ thu thập dữ liệu mà không kèm theo các điểm cuối proxy, chẩn đoán nhóm, đường dẫn máy chủ hoặc lỗi kết nối thô. Chẩn đoán kết nối yêu cầu quyền `account` trên toàn bộ không gian làm việc. Việc đọc thông báo, sao chép ngoài hệ thống và cài đặt tham số yêu cầu quyền `settings`.

Các chuỗi User-Agent đầy đủ trong trình duyệt không được lưu giữ trong các phiên truy cập. Việc nâng cấp cũng xóa chúng khỏi bộ nhớ đệm phiên có thể thay đổi. Nhật ký quá trình của bảng điều khiển che giấu các địa chỉ IP, thông tin xác thực URL và các bí mật được gắn nhãn. Nhật ký dịch vụ cục bộ và các bản ghi nhật ký đã được ký trước đó không bị ghi đè. Các quy tắc truy cập và bản ghi đăng nhập đã được ký vẫn sử dụng địa chỉ của máy khách.

### Thay thế khóa chính

Sử dụng **Access → Giới hạn của tôi → Phát hành lại khóa quản trị viên**, hoặc chạy `tgwitness token rotate` từ một bản cài đặt được quản lý trong khi bảng điều khiển đang chạy. Tất cả các phiên trình duyệt hiện có sẽ kết thúc, bao gồm cả các phiên được mở bằng mã thông báo đồng nghiệp . Trình duyệt yêu cầu sẽ nhận được một phiên mới; hãy lưu khóa quản trị viên mới trước khi ẩn nó đi. Các mã thông báo đồng nghiệp đã được cấp vẫn có hiệu lực cho đến khi bị thu hồi riêng. Một bản cài đặt sử dụng lệnh ``TGWITNESS_TOKEN`` phải thay đổi cài đặt môi trường đó và khởi động lại.

### Ranh giới yêu cầu và proxy

API cho phép tối đa 600 yêu cầu mỗi phút cho mỗi địa chỉ IP khách hàng. Mười lần xác thực bị từ chối trong vòng một phút sẽ kích hoạt thời gian chờ tăng theo cấp số nhân, từ một giây lên đến năm phút. Một lần thử thất bại sau thời gian chờ sẽ làm tăng thời gian chờ; mười phút không có lần thử thất bại nào sẽ đặt lại mức tăng. Các yêu cầu bị từ chối sẽ trả về mã lỗi HTTP 429 và `Retry-After`. Giới hạn được lưu trữ trong bộ nhớ, được chia sẻ giữa các không gian làm việc trong một quy trình bảng điều khiển; việc khởi động lại sẽ xóa các giới hạn này. Các luồng trực tiếp bị giới hạn ở bốn luồng cho mỗi mã thông báo mang và 32 luồng cho quy trình bảng điều khiển. Việc mở một luồng cũng tiêu tốn hạn mức yêu cầu API.

Nội dung yêu cầu có thời hạn nhận là 60 giây (8 giây đối với MCP). Mỗi ứng dụng giới hạn số lượng nội dung chưa hoàn thành ở mức 32 yêu cầu và 64 MiB dung lượng đường dẫn được phân bổ. Nội dung vượt quá giới hạn sẽ trả về mã trạng thái 413, nội dung hết thời gian chờ sẽ trả về 408, và khi dung lượng nội dung đã cạn kiệt sẽ trả về 503 kèm theo thông tin "`Retry-After`".

Các tiêu đề IP được chuyển tiếp sẽ bị bỏ qua trừ khi đối tác TCP thực sự thuộc về `TGWITNESS_TRUSTED_PROXIES` (các địa chỉ IP hoặc CIDR được phân tách bằng dấu phẩy). Đặt `TGWITNESS_PROXY_HEADER` thành `x-forwarded-for` hoặc `cf-connecting-ip`. XFF được di chuyển từ proxy gần nhất đến đối tác không đáng tin cậy đầu tiên. Siêu dữ liệu địa chỉ đáng tin cậy bị lỗi hoặc trùng lặp sẽ bị từ chối, do đó nó không thể kế thừa địa chỉ proxy trong danh sách cho phép. Đường hầm nhanh được quản lý tin tưởng trình kết nối cloudflared cục bộ; thiết lập miền riêng tin tưởng Caddy cục bộ. Các triển khai trực tiếp mặc định không tin cậy bất kỳ proxy nào. Nếu tự khởi chạy Uvicorn, hãy vô hiệu hóa tính năng xử lý tiêu đề proxy của nó để ranh giới này nhận được peer thực tế.

`TGWITNESS_PANEL_ALLOWED_IPS` hạn chế toàn bộ quyền truy cập bảng điều khiển, bao gồm cả quản trị viên, chỉ cho phép từ các địa chỉ IP hoặc CIDR được liệt kê. Công cụ kiểm tra định danh định tuyến của trình cài đặt vẫn ở chế độ công khai và không trả về dữ liệu tài khoản. Hãy bao gồm đường dẫn quản trị cục bộ bắt buộc trước khi kích hoạt danh sách cho phép. Hướng dẫn **START-HERE** dành cho cài đặt được quản lý bao gồm các hướng dẫn cấu hình dịch vụ và khôi phục.

Bộ chọn truy vấn API `ws` phải xác định không gian làm việc trong đường dẫn yêu cầu; các bộ chọn không xác định, không khớp hoặc trùng lặp sẽ bị từ chối với mã trạng thái 404.

Các tập lệnh và kiểu dáng của bảng điều khiển chứa siêu dữ liệu tính toàn vẹn SHA-384. Bản đồ nhập khẩu cũng bao gồm các mô-đun JS được nhập khẩu cục bộ trong các trình duyệt hỗ trợ tính toàn vẹn của bản đồ nhập khẩu. Phản hồi ngôn ngữ được tạo động là một phần riêng biệt. Các kiểm tra này phát hiện việc thay thế tài nguyên so với trang đã được phân phối; chúng không xác lập sự tin cậy vào một máy chủ bị xâm nhập có thể thay thế cả trang lẫn các giá trị băm của nó.

**Nhật ký kể từ khi bắt đầu này** kết hợp các bản ghi quá trình với hoạt động nhật ký từ mọi không gian làm việc: các lần đăng nhập, từ chối, thay đổi lộ trình và hành động của người vận hành. Đây là một bảng điều khiển trong bộ nhớ dành cho quá trình hiện tại, chứ không phải bản sao vĩnh viễn của mọi tin nhắn. Các sự kiện tin nhắn xảy ra thường xuyên sẽ được lưu trong nhật ký thay vì làm đầy bảng điều khiển.

Việc cấp, thay đổi và thu hồi quyền truy cập, cũng như bắt đầu hoặc kết thúc phiên làm việc, đều tạo ra các bản ghi nhật ký `access.*` được ký điện tử. Các mã thông báo (token) không được bao gồm trong các bản ghi này. Các mã thông báo đã được cấp và thông tin xác thực phiên làm việc được lưu giữ dưới dạng băm (hash) trong kho lưu trữ được mã hóa.

****Quản trị viên chính và ranh giới tin cậy****

The main panel token remains unrestricted. Browser sign-ins with it create sessions subject to the administrator's configured session limits. Scripts sending the main token directly retain full access and are not counted as browser sessions.

This is application-level access control in one installation. All workspaces share the server process; this is not isolation from the host administrator. Keep the main token, Telegram sessions, signing keys and data directory private. A witness token is a separate checkpoint/health credential, not a panel access token.
