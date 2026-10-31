# Quyền truy cập và quyền hạn

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/

Quản lý quyền truy cập vào các tài khoản và cuộc trò chuyện, chọn quyền hạn, giới hạn phiên truy cập và địa chỉ IP, cũng như thu hồi quyền truy cập.

Cấp quyền truy cập cho người đánh giá vào một cuộc trò chuyện, cấp quyền cho nhà phân tích để xuất dữ liệu vụ việc, hoặc cấp quyền kiểm soát các tài khoản đã chọn cho người vận hành. Mỗi người sẽ nhận được mã thông báo riêng. Mã thông báo trên bảng điều khiển chính sẽ do quản trị viên nắm giữ.

[Thiết lập tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/) · [Các tuyến kết nối](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/) · [Mô hình bảo mật](https://phishdestroy.github.io/TgWitness/vi/docs/reference/security/)

## Hai phạm vi, hai nhiệm vụ khác nhau

**Phạm vi thu thập** quyết định những gì một tài khoản sẽ ghi lại: các cuộc trò chuyện được chọn, một thư mục Telegram hoặc toàn bộ tài khoản. **Phạm vi truy cập** quyết định những tài khoản và cuộc trò chuyện đã được ghi lại nào mà người khác có thể xem và sử dụng. Việc cấp quyền truy cập không đồng nghĩa với việc tham gia cuộc trò chuyện trên Telegram, bắt đầu quá trình thu thập hay cấp quyền truy cập vào tài khoản Telegram.

Một quyền truy cập có thể mở các không gian làm việc đã chọn, các cuộc trò chuyện đã chọn trong đó hoặc tất cả các không gian làm việc. **Tất cả các không gian làm việc, bao gồm cả những không gian được thêm vào sau này**, cũng áp dụng cho các tài khoản trong tương lai. Vui lòng chọn rõ ràng các không gian làm việc khi cần giới hạn phạm vi điều tra trong phạm vi những không gian đó.

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

| Quyền sử dụng | Các tính năng mà công cụ này cung cấp |
| --- | --- |
| `view` | Xem các cuộc trò chuyện được phép truy cập, tin nhắn đã ghi lại, hồ sơ cá nhân, tệp tin và các bản ghi nhật ký đã được lọc. Luôn được bao gồm đầy đủ. |
| `export` | Cho phép xuất lịch sử trò chuyện và hồ sơ. Việc xuất toàn bộ bằng chứng trong không gian làm việc yêu cầu quyền truy cập vào toàn bộ không gian làm việc đó. |
| `sources` | Quản lý nguồn, ảnh chụp nhanh và thu thập thông tin hồ sơ. Quyền truy cập giới hạn theo cuộc trò chuyện chỉ có hiệu lực đối với các cuộc trò chuyện được phép; việc phát hiện nguồn và cài đặt phạm vi trên toàn tài khoản vẫn được giữ ở trạng thái đóng. |
| `collect` | Khởi động hoặc dừng trình thu thập dữ liệu. Yêu cầu quyền truy cập toàn bộ không gian làm việc vì quá trình thu thập sẽ ảnh hưởng đến tài khoản. |
| `interact` | Thực hiện các tương tác được hỗ trợ trên Telegram trong phạm vi quyền truy cập. Quyền truy cập giới hạn ở chế độ trò chuyện không thể sử dụng tính năng xem trước liên kết trên toàn tài khoản. |
| `settings` | Thay đổi cài đặt thu thập dữ liệu, dấu thời gian, thông báo, bản sao lưu ngoài trang web và các thông số. Yêu cầu quyền truy cập toàn bộ không gian làm việc. |
| `account` | Đăng nhập hoặc đăng xuất khỏi Telegram và quản lý các tuyến kết nối. Yêu cầu quyền truy cập toàn bộ không gian làm việc. |

Quyền truy cập và phạm vi sẽ được kiểm tra đồng thời. Việc chọn một quyền truy cập sẽ không mở các cuộc trò chuyện khác hoặc kích hoạt thao tác trên toàn không gian làm việc đối với quyền truy cập bị giới hạn trong một cuộc trò chuyện cụ thể. Để thực hiện xuất song song, quyền truy cập phải bao gồm cuộc trò chuyện được xuất trong mọi tài khoản đã chọn. Một quyền truy cập đã được cấp không thể tạo ra các quyền truy cập mới, quản lý các phiên làm việc của người khác hoặc mở bảng điều khiển quản trị viên.

### Ba cách thiết lập hữu ích

| Người | Phạm vi | Quyền truy cập |
| --- | --- | --- |
| Người đánh giá | Các cuộc trò chuyện được ghi lại trong một vụ việc | `view` |
| Chuyên viên phân tích đang chuẩn bị bàn giao công việc | Các cuộc trò chuyện cần điều tra và xuất dữ liệu | `view`, `export`; chỉ thêm `interact` nếu họ cần thực hiện các thao tác thông qua Telegram |
| Nhân viên thu thập dữ liệu | Các không gian làm việc được chọn lọc | `view`, `sources`, `collect`; chỉ thêm `settings` hoặc `account` khi cần thiết |

Đây là những ví dụ mà quý vị có thể cấu hình thông qua các ô chọn quyền, chứ không phải là các vai trò cố định.

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

Chỉnh sửa một mục trong **phần Quyền truy cập** để thay đổi phạm vi, quyền hạn hoặc giới hạn của mục đó. Các thay đổi về phạm vi và quyền hạn sẽ được kiểm tra trên các yêu cầu tiếp theo, bao gồm cả các yêu cầu từ các phiên đang mở. Việc thu hồi quyền truy cập sẽ kết thúc các phiên hiện có và khiến mã thông báo đã cấp không còn hiệu lực. **Tính năng phiên đang mở** cũng cho phép quản trị viên kết thúc một phiên cụ thể mà không cần thu hồi toàn bộ quyền truy cập.

Việc thu hồi không thể khôi phục các tệp mà người dùng đã tải xuống. Việc đăng xuất, khóa bảng điều khiển hoặc kết thúc phiên làm việc sẽ không làm dừng trình thu thập đang hoạt động.

## Những thông tin mà quản trị viên có thể xem

**Nhật ký kể từ khi bắt đầu này** kết hợp các bản ghi quá trình với hoạt động nhật ký từ mọi không gian làm việc: các lần đăng nhập, từ chối, thay đổi lộ trình và hành động của người vận hành. Đây là một bảng điều khiển trong bộ nhớ dành cho quá trình hiện tại, chứ không phải bản sao vĩnh viễn của mọi tin nhắn. Các sự kiện tin nhắn xảy ra thường xuyên sẽ được lưu trong nhật ký thay vì làm đầy bảng điều khiển.

Việc cấp, thay đổi và thu hồi quyền truy cập, cũng như bắt đầu hoặc kết thúc phiên làm việc, đều tạo ra các bản ghi nhật ký `access.*` được ký điện tử. Các mã thông báo (token) không được bao gồm trong các bản ghi này. Các mã thông báo đã được cấp và thông tin xác thực phiên làm việc được lưu giữ dưới dạng băm (hash) trong kho lưu trữ được mã hóa.

****Quản trị viên chính và ranh giới tin cậy**** Mã thông báo bảng điều khiển chính vẫn không bị hạn chế. Việc đăng nhập qua trình duyệt bằng mã thông báo này sẽ tạo ra các phiên tuân theo giới hạn phiên do quản trị viên cấu hình. Các tập lệnh gửi mã thông báo chính trực tiếp vẫn giữ quyền truy cập đầy đủ và không được tính là các phiên trình duyệt. Đây là cơ chế kiểm soát truy cập ở cấp độ ứng dụng trong một lần cài đặt. Tất cả các không gian làm việc đều chia sẻ quá trình máy chủ; điều này không có nghĩa là cách ly với quản trị viên máy chủ. Hãy bảo mật mã thông báo chính, các phiên Telegram, khóa ký và thư mục dữ liệu. Mã thông báo chứng thực là một thông tin xác thực kiểm tra trạng thái/điểm kiểm tra riêng biệt, không phải là mã thông báo truy cập bảng điều khiển.
