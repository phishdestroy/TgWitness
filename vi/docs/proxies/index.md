# Chọn một máy chủ proxy

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/proxies/

Vui lòng duy trì kết nối tài khoản. Hãy quyết định rõ ràng khi nào đường dẫn của tài khoản đó có thể sử dụng địa chỉ máy chủ.

## Vui lòng chọn chế độ IP trước tiên

01**Ẩn địa chỉ IP**

Vui lòng sử dụng máy chủ trung gian (proxy). Trong trường hợp không có máy chủ trung gian nào hoạt động, xin vui lòng chờ đợi mà không cần kết nối trực tiếp với Telegram.

02**Cho phép sử dụng phương án dự phòng**

Cho phép kết nối trực tiếp sau khoảng thời gian trễ đã được cấu hình; quay trở lại sử dụng máy chủ proxy đang hoạt động khi có máy chủ nào đó phản hồi.

03**Tunnel / VPN**

Cho phép các kết nối trực tiếp qua mạng của nhà cung cấp dịch vụ. Tùy chọn này không cài đặt hoặc xác minh VPN.

Tuyến đường sẽ quyết định loại kết nối. Chế độ IP sẽ xác định liệu kết nối trực tiếp có được phép hay không.

## Hãy để nhóm duy trì lộ trình

1. Mở **Tài khoản → Cài đặt → Cài đặt kết nối**.
2. Vui lòng chọn chế độ IP và **MTProxy Tự động**, hoặc nhập một tuyến đường cố định.
3. Lưu lại và thực hiện **kiểm tra kết nối Telegram**. Tính năng này cũng hoạt động ngay cả trước khi đăng nhập.
4. Sau khi bắt đầu quá trình thu thập, vui lòng kiểm tra xem tin nhắn đã được kiểm soát có được ghi vào sổ chứng cứ hay không.

Các không gian làm việc mới sử dụng tính năng MTProxy tự động với chế độ Ẩn địa chỉ IP. Hệ thống này kết hợp bốn nguồn công khai, kiểm tra các mục, duy trì các tuyến đường hoạt động và thay thế các proxy không hoạt động. Các lần tải xuống không thành công sẽ giữ lại các bản chụp nhanh trước đó.

## Vui lòng sử dụng máy chủ proxy của riêng quý vị

Vui lòng nhập thông tin SOCKS5 hoặc HTTP CONNECT, dán liên kết proxy Telegram được hỗ trợ hoặc cung cấp danh mục nhà cung cấp dịch vụ. Hãy tạm dừng quá trình giám sát trước khi thay đổi tuyến đường đang hoạt động. Các khóa bí mật TLS MTProxy giả mạo bắt đầu bằng `ee` vẫn chưa được hỗ trợ.

**Cài đặt xoay vòng, chia sẻ và thử lại**

Trong **phần Cài đặt → MTProxy Tự động**, quý vị hãy thiết lập ngưỡng lỗi, thời gian chờ, lịch luân phiên dự kiến và số lượng tài khoản cho mỗi proxy. Giới hạn chia sẻ là một sẽ khiến tài khoản phải chờ khi không có kết nối độc quyền nào khả dụng. Khoảng thời gian làm mới danh sách và khoảng thời gian kiểm tra sẽ tuân theo các giá trị của không gian làm việc chính. Việc sử dụng các proxy riêng biệt không đảm bảo các địa chỉ IP đầu ra riêng biệt.

## Tách biệt Telegram khỏi các yêu cầu từ bên ngoài

MTProxy chỉ truyền tải lưu lượng Telegram. Dấu thời gian, thông báo, bản sao và việc kiểm tra nguồn sử dụng một proxy SOCKS5/HTTP riêng biệt, tuyến SOCKS5/HTTP của tài khoản, hoặc chế độ Trực tiếp (Direct) khi chế độ IP cho phép. Các yêu cầu bên ngoài này có thể bị vô hiệu hóa.

Một cấu hình `TGWITNESS_PROXY_FEED_PROXY` rõ ràng sẽ xác định lộ trình của trình tải xuống nguồn cấp dữ liệu. Công cụ [chứng thực độc lập](https://phishdestroy.github.io/TgWitness/vi/docs/witness/) này duy trì các thiết lập riêng của mình. Các thiết lập này không cài đặt VPN hệ thống cũng như không định tuyến lưu lượng truy cập trình duyệt.

Xem [tất cả các chế độ, cài đặt mặc định và danh sách nguồn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/#ip-modes), hoặc [chọn những người được phép thay đổi lộ trình của tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/access/).
