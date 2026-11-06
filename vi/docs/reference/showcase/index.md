# Trưng bày công khai

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/showcase/

Xuất bản các tin nhắn đã lưu từ các kênh công khai được chọn và các bản chụp màn hình đã được ký thông qua các liên kết có thời hạn và có thể thu hồi.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/vi/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

**Truy cập → Public showcase** tạo ra một trang riêng biệt, chỉ đọc, sử dụng hệ thống access-token hiện có. Nó đọc các quan sát đã lưu của bản cài đặt. Nó không khởi chạy trình thu thập dữ liệu, đăng nhập vào Telegram hoặc tạo kênh cho người truy cập.

## Xuất bản một trang

1. Lưu một hồ sơ nguồn cho mỗi kênh công khai mà bạn muốn hiển thị. Một kênh phải có tên người dùng công khai trong hồ sơ được lưu gần nhất; các nhóm và cuộc trò chuyện riêng tư không đủ điều kiện.
2. Mở **Quyền truy cập → Trưng bày công khai** (hoặc `/showcase-manage.html`) với tư cách quản trị viên.
3. Chọn các kênh từ tối đa 16 không gian làm việc, nhập tiêu đề trang công khai và chọn thời hạn tồn tại của liên kết là 1, 7 hoặc 30 ngày. Các nhãn nội bộ của không gian làm việc sẽ không được công khai. Có thể bao gồm tối đa 64 kênh.
4. Xem lại nội dung văn bản của các kênh đã chọn để xuất bản, sau đó nhấp vào **“Xem trước các bản ghi đã chọn**”. Bản xem trước sử dụng cùng một cách hiển thị phía máy chủ như trang dành cho khách truy cập.
5. Nhấp vào **liên kết “Tạo showcase**”. Sao chép liên kết khi nó còn hiển thị. Mở liên kết đó trong một trình duyệt riêng để xem trước trang của người nhận trước khi chia sẻ.

Liên kết chứa mã thông báo truy cập trong phần URL fragment. Trang web sẽ loại bỏ phần fragment này trước khi thực hiện các yêu cầu API và đổi nó lấy một phiên trình duyệt. Bất kỳ ai có liên kết này đều có thể mở tài liệu đã chọn cho đến khi hết hạn hoặc bị thu hồi. Các liên kết mới cho phép 100 phiên truy cập đồng thời, mỗi phiên kéo dài tối đa một giờ. Các kiểm soát truy cập hiện có cũng có thể áp dụng các hạn chế về địa chỉ và giới hạn đăng nhập thông qua API cấp quyền. Quyền truy cập bình thường của người đánh giá là một chế độ khác và vẫn bao gồm các tin nhắn và tệp được phép ban đầu.

## Những gì người truy cập nhìn thấy

| Hiển thị | Được giữ riêng tư |
| --- | --- |
| Các tiêu đề kênh công khai, tên người dùng và ngày quan sát hồ sơ được chọn lọc | Danh tính tài khoản, nhãn không gian làm việc nội bộ và các nguồn chưa được chọn |
| Văn bản được ghi lại và mỗi lần chỉnh sửa đã lưu | ID người gửi, tên, tên người dùng, số điện thoại và các giá trị hồ sơ được cấu trúc |
| Ghi lại các quan sát khi xóa kèm theo văn bản đã lưu trước đó (nếu có) | Tệp đính kèm, ảnh đại diện, hình thu nhỏ, tên tệp và nội dung gốc |
| Các dấu hiệu cho biết tác giả/hồ sơ hoặc tệp đính kèm đã được ghi lại | Siêu dữ liệu chuyển tiếp và trả lời, các tuyến mạng, địa chỉ IP và thông tin đăng nhập |
| Số lượng sự kiện trên các kênh đã chọn, trạng thái bật/tắt bộ sưu tập hiện tại, tín hiệu kiểm tra và khoảng thời gian kiểm tra định kỳ | Các điều khiển bộ sưu tập và các API xuất bằng chứng thông thường |
| Dấu vân tay ký, điểm kiểm tra nhật ký và bằng chứng nhất quán | Khóa ký và phiên Telegram |

**Nội dung tin nhắn công khai không được ẩn danh tự động.** Tên, đề cập, số điện thoại hoặc liên kết được ghi trong tin nhắn vẫn là một phần của nội dung đó. `Redacted`Áp dụng cho các trường tác giả/hồ sơ có cấu trúc. Hãy xem lại nội dung đã chọn thực tế trước khi đăng tải, bao gồm cả các chỉnh sửa và xóa đã được lưu lại.

Tính đủ điều kiện phản ánh **hồ sơ nguồn được lưu gần nhất**, không phải kết quả tra cứu Telegram theo thời gian thực. Nếu hồ sơ tiếp theo không còn tên người dùng kênh công khai, các yêu cầu mới sẽ loại trừ kênh đó. Hãy làm mới hồ sơ nguồn khi tính năng hiển thị công khai thay đổi. Người đọc có thể đã lưu trữ các tài liệu mà họ đã nhận được trước đó.

Các bản ghi gốc đã được ký vẫn giữ nguyên. Bản chiếu được hiển thị được ký riêng biệt và chứa các hàm băm tham chiếu đến các bản ghi gốc của nó. Chữ ký của bản chiếu xác thực tuyên bố được hiển thị; nó không phải là chữ ký của sự kiện gốc trên các byte đã được che giấu.

## Kiểm tra chữ ký và tính liên tục

Mở rộng **"Dấu vân tay & điểm kiểm tra đã ký**" và tải xuống bản chụp nhanh. Sau khi trang được làm mới, tệp tải xuống sẽ bao gồm bản chụp nhanh trình duyệt trước đó và bằng chứng tính nhất quán Merkle giữa các ranh giới nhật ký của chúng. Tự động làm mới diễn ra mỗi phút một lần khi trang đang hiển thị và đang hiển thị trang quan sát đầu tiên.

Sau khi cài đặt TgWitness, hãy xác minh tệp đã tải xuống ở chế độ ngoại tuyến:

```
python -m tgwitness.showcase_verify showcase.json --fingerprint TRUSTED_COLLECTOR_SHA256
```

Dấu vân tay phải đến từ một nguồn tham chiếu đáng tin cậy riêng biệt. Để so sánh với bản chụp nhanh mà bạn đã tự lưu giữ, hãy sử dụng `--previous earlier.json`; điều này sẽ ghi đè lên bản chụp nhanh trước đó được chứa trong tệp tải xuống. Bằng chứng hiện tại phải bắt đầu từ ranh giới đã lưu giữ đó. Các khách hàng đã được xác thực có thể yêu cầu bằng chứng đó bằng cách sử dụng `GET /api/showcase/{workspace_id}?challenge=<32-hex-random>&from_count=<retained-count>`. Một nhật ký ngắn hơn sẽ trả về mã trạng thái HTTP 409 thay vì tự động đặt lại ranh giới mà không có thông báo.

Điểm kiểm tra đã ký được ghi vào **toàn bộ nhật ký thu thập**, bao gồm cả số lượng bản ghi và hàm băm đầu mờ. Số lượng tin nhắn hiển thị chỉ áp dụng cho các kênh công khai đã chọn. Trang này không bao giờ liệt kê nội dung của các nhật ký khác. Đây là số lượng sự kiện, không phải số lượng tin nhắn duy nhất. Các cài đặt mô tả cấu hình hiện tại, không phải mọi khoảng thời gian ghi trước đó.

Việc xác minh chữ ký và tính nhất quán có thể phát hiện các thay đổi so với một ranh giới đã được lưu giữ. Công cụ này không tự động kiểm đếm lại các bộ đếm đã được ký, xác nhận nguồn gốc Telegram, chứng minh việc ghi lại liên tục, hoặc thay thế một nhân chứng độc lập. Để thực hiện việc kiểm tra đó, hãy sử dụng công [cụ xác minh bằng chứng](https://github.com/phishdestroy/TgWitness/blob/main/docs/TRUST.md), [nhân chứng độc lập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/) và [bản ghi đã được kiểm thử trên quy mô lớn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/). Các cài đặt tổng hợp được dán nhãn rõ ràng là tổng hợp.

## Hủy quyền truy cập hoặc lưu trữ trang

Sử dụng **tính năng “Revoke”** trong trình quản lý showcase hoặc phần **“Access**” hiện có để đóng liên kết và kết thúc tất cả các phiên của nó. Người truy cập sẽ xóa các bản ghi đang hiển thị khi yêu cầu phát hiện rằng quyền truy cập đã kết thúc. Thời hạn và quyền truy cập được kiểm tra trên mỗi yêu cầu. Quyền truy cập showcase không thể chuyển đổi trực tiếp thành quyền truy cập bảng điều khiển thông thường; hãy tạo một quyền truy cập mới để thay đổi chế độ.

Trang web được phục vụ thông qua địa chỉ HTTPS hiện có của hệ thống cài đặt. Việc chia sẻ một liên kết sẽ không mở cổng mới, tạo đường hầm hoặc thay đổi DNS. Mã HTML và API vẫn được lưu trữ trên hệ thống cài đặt của người dùng. Người truy cập bản demo không thể sử dụng các API thông thường liên quan đến tin nhắn, hồ sơ, phương tiện, xuất dữ liệu hoặc quản lý với quyền truy cập này.
