# Chọn một máy chủ proxy

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/proxies/

Giữ tài khoản trực tuyến, và tự bạn quyết định nó có được để lộ IP máy chủ hay không.

## Vui lòng chọn chế độ IP trước tiên

01**Ẩn địa chỉ**

Chỉ dùng proxy. Nếu không cái nào hoạt động, nó chờ.

02**Chỉ sử dụng phương án này khi không còn lựa chọn nào khác**

Kết nối trực tiếp sau một khoảng chờ, quay lại proxy khi có cái hoạt động.

03**Máy chủ nằm sau một đường hầm hoặc VPN**

Kết nối trực tiếp cũng được. Nó không thiết lập hay kiểm tra VPN giúp bạn.

Tuyến đường sẽ quyết định loại kết nối. Chế độ IP sẽ xác định liệu kết nối trực tiếp có được phép hay không.

## Hãy để nhóm duy trì lộ trình

1. **Tài khoản → Cài đặt → Cài đặt kết nối**.
2. Chọn chế độ IP và **MTProxy tự động**, hoặc một tuyến cố định.
3. Lưu, rồi **Kiểm tra kết nối Telegram** (dùng được cả trước khi đăng nhập).
4. Bắt đầu thu thập và tự gửi cho mình một tin nhắn thử.

Không gian làm việc mới khởi đầu với MTProxy tự động và **Ẩn địa chỉ**. Nhóm proxy lấy bốn danh sách công khai, kiểm tra máy chủ, giữ cái tốt và thay cái đã chết.

## Vui lòng sử dụng máy chủ proxy của riêng quý vị

SOCKS5, HTTP CONNECT, liên kết proxy Telegram hoặc danh mục của nhà vận hành. Hãy tạm dừng quan sát trước khi chuyển. Khóa bí mật Fake TLS (`ee`…) không hoạt động.

**Cài đặt xoay vòng, chia sẻ và thử lại**

**Tham số → MTProxy tự động**: ngưỡng lỗi, thời gian nghỉ, xoay vòng, số tài khoản mỗi proxy. Giới hạn 1 nghĩa là tài khoản sẽ chờ thay vì dùng chung. Các proxy khác nhau vẫn có thể dùng chung một IP thoát.

## Tách biệt Telegram khỏi các yêu cầu từ bên ngoài

MTProxy chỉ mang lưu lượng Telegram. Dấu thời gian, thông báo, bản sao và kiểm tra mã đi qua một proxy SOCKS5/HTTP riêng, tuyến SOCKS5/HTTP của tài khoản, hoặc trực tiếp nếu chế độ cho phép. Hoặc tắt chúng đi.

`TGWITNESS_PROXY_FEED_PROXY` đặt tuyến dùng để tải danh sách. [Nhân chứng](https://phishdestroy.github.io/TgWitness/vi/docs/witness/) có cài đặt riêng. Không cái nào đụng tới trình duyệt hay mạng hệ thống của bạn.

Thêm: [các chế độ và giá trị mặc định](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/#ip-modes), [ai được đổi tuyến](https://phishdestroy.github.io/TgWitness/vi/docs/access/).
