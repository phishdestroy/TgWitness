# Hãy đảm bảo tính bảo mật

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/security/

Những gì rời khỏi máy của bạn, mỗi khóa bí mật mở được gì, và các lớp bảo vệ lo phần nào, phần nào là trách nhiệm của bạn.

**127.0.0.1**Địa chỉ bảng điều khiển theo mặc định

**256 bit**mã thông báo bảng ngẫu nhiên

**0**CDN, phân tích dữ liệu hoặc phông chữ từ xa

**Ed25519**chữ ký trên mỗi bản ghi

## Nơi lưu trữ mọi thông tin

Máy thu thập, bảng điều khiển và mọi bản ghi đều ở trên máy của bạn. Mặc định chỉ liên lạc với Telegram; mọi thứ khác là một công tắc riêng.

06 / NHỮNG GÌ ĐƯỢC LƯU LẠI TỪ HỆ THỐNGQuá trình cài đặt của quý vị

MÁY TÍNH HOẶC MÁY CHỦ CỦA QUÝ VỊ

**Bảng điều khiển**127.0.0.1:8787 · mã thông báo bearer

**Trình thu thập**Mỗi không gian làm việc tương ứng với một ứng dụng Telegram

THƯ MỤC DỮ LIỆU

**Sổ ghi chép**SQLite · chuỗi băm · có chữ ký

**Phương tiện truyền thông**các tệp được đặt tên theo mã SHA-256

**Vault**Fernet · phiên làm việc, cặp API, khóa ký, máy chủ proxy

- **Telegram**Luôn luôn · thông qua lộ trình của quý vị

  Kết nối MTProto của tài khoản: trực tiếp, SOCKS5, HTTP hoặc MTProxy. Chế độ Ẩn địa chỉ IP sẽ chờ một máy chủ proxy hoạt động. Chế độ chuyển sang kết nối trực tiếp yêu cầu phải có chế độ cho phép rõ ràng việc này.
- **Nội dung ngoài trang web**Tùy chọn · tắt theo mặc định

  Nhật ký, tệp tin và các điểm kiểm tra được mã hóa bằng thuật toán AES-GCM trước khi tải lên kho lưu trữ tương thích với S3. Khóa mã hóa do quý vị quản lý; các tệp đính kèm được đặt tên dựa trên hàm băm có khóa, chứ không phải hàm băm nội dung của chúng.
- **Thông báo**Tùy chọn · tắt theo mặc định

  Các vấn đề và số lần thay đổi được hiển thị kèm theo tiêu đề cuộc trò chuyện. Các đoạn trích tin nhắn chỉ được gửi khi quý vị bật tính năng này.
- **Tính xác thực của dấu thời gian**Tùy chọn · tắt theo mặc định

  Chỉ bao gồm mã SHA-256 của điểm kiểm tra đã được ký và một giá trị ngẫu nhiên (nonce). Không chứa tin nhắn hay tên người dùng trong cuộc trò chuyện.
- **Witness**Tùy chọn · tắt theo mặc định

  Công cụ này trích xuất các điểm kiểm tra đã được ký và số lần ghi lại bằng một mã thông báo chỉ đọc. Công cụ này không thể đọc nội dung cuộc trò chuyện hoặc thay đổi cài đặt.

Mặc định: chỉ kết nối Telegram mới được truyền ra khỏi máy này.

Các đích lưu trữ tùy chọn được cấu hình riêng cho từng không gian làm việc. Nội dung tin nhắn và tệp đa phương tiện được lưu trữ dưới dạng không mã hóa trong thư mục dữ liệu: quý vị cần bảo vệ thư mục này bằng cách mã hóa ổ đĩa và thiết lập quyền truy cập tệp.

## Mỗi bí mật sẽ mở ra điều gì

| Bí mật | Nơi lưu trữ | Những lợi ích mà công cụ này mang lại | Trong trường hợp thông tin bị rò rỉ |
| --- | --- | --- | --- |
| **Mã thông báo bảng điều khiển** | `panel-token.txt` trong thư mục dữ liệu; trình duyệt giữ nó theo từng tab | Mọi thứ trong mọi không gian làm việc | Dừng TgWitness, xóa `panel-token.txt`, khởi động lại: bạn nhận được token mới |
| **Phiên làm việc trên Telegram** | Kho lưu trữ, được mã hóa (`credentials.enc`) | Tài khoản Telegram này | Kết thúc phiên làm việc trên Telegram tại *mục Cài đặt → Thiết bị* |
| **Khóa ký** | Kho lưu trữ, được mã hóa (`signing.enc`) | Ký bản ghi dưới dấu vân tay của bạn | Điểm kiểm tra lưu ở nơi khác, nhân chứng và dấu thời gian vẫn cho thấy những gì đã tồn tại trước đó |
| **Khóa kho lưu trữ** | `vault.key` cạnh dữ liệu, hoặc một khóa chính bên ngoài | Kho bảo mật | Hãy coi như phiên và khóa ký cũng đã bị lộ |
| **Token Witness** | Trên máy chủ Witness | Chỉ đọc: điểm kiểm tra và tình trạng | Xóa nó trên trang Nhân chứng, tạo cái mới |
| **Nội dung chính trên trang web bên ngoài** | Vault; chỉ cần tải xuống một lần để phục hồi | Bản sao ngoài trang web | Ai có cả bucket đều giải mã được: hãy coi bản sao là đã bị lộ |

## Phạm vi bảo vệ bao gồm những gì

### Đã được đề cập

- Bản ghi bị sửa, xóa hoặc đổi thứ tự: chuỗi băm hoặc chữ ký bị phá vỡ.
- Sổ nhật ký bị cắt bớt hoặc dựng lại sau khi bạn đã lưu điểm kiểm tra ở nơi khác: điểm kiểm tra không còn khớp.
- Đoán token: 256 bit ngẫu nhiên, so sánh thời gian hằng định, 15 lần thất bại trong một phút là địa chỉ bị chặn.
- Nội dung trò chuyện độc hại: văn bản vẫn là văn bản, không bao giờ là HTML; tệp đính kèm tải xuống dưới dạng tệp; bảng điều khiển không tải gì từ trang web khác.
- Thư mục dữ liệu bị đánh cắp khi dùng khóa kho bảo mật bên ngoài: phiên và khóa vẫn được mã hóa.

### , xin để quý vị tự quyết định

- Token chính làm được mọi thứ. Hãy cấp cho người khác quyền truy cập giới hạn và giữ token chính cho riêng mình.
- Bất kỳ ai là quản trị viên trên máy đều đọc được mọi thứ và ký lại sổ nhật ký. Hãy giữ dấu vân tay và điểm kiểm tra ở nơi khác.
- TgWitness không mã hóa tin nhắn và phương tiện. Hãy mã hóa ổ đĩa, siết chặt quyền.
- HTTP thường bên ngoài localhost làm lộ token. Hãy dùng HTTPS hoặc đường hầm SSH.
- Chữ ký không cho bạn biết những gì đã bị bỏ lỡ. Hãy kiểm tra phạm vi và thử việc nhận tin trên chính tài khoản và nguồn của bạn.

[Chia sẻ quyền truy cập vào một vụ việc](https://phishdestroy.github.io/TgWitness/vi/docs/access/) với quyền hạn, thời hạn và giới hạn phiên.

## Tăng cường bảo mật cho hệ thống cài đặt

Đã hoàn thành 0/8

1. **Hãy sử dụng một tài khoản Telegram chuyên dụng**, không bao giờ dùng tài khoản chính.
2. **Giữ bảng điều khiển trên 127.0.0.1.** Truy cập từ xa chỉ qua HTTPS (Caddy đi kèm) hoặc đường hầm SSH.
3. **Mã hóa ổ đĩa** chứa thư mục dữ liệu, tin nhắn và phương tiện được lưu nguyên trạng.
4. **Hãy giới hạn thư mục dữ liệu** cho tài khoản dịch vụ (0700 trên Unix, quyền thư mục trên Windows).
5. **Giữ khóa kho bảo mật ở nơi khác** trên máy chủ: đặt `TGWITNESS_VAULT_KEY_FILE` trước lần khởi động đầu tiên.
6. **Lưu dấu vân tay và điểm kiểm tra** trên một hệ thống khác, chạy nhân chứng trên một máy chủ khác.
7. **Tuyệt đối không được tải lên các** khóa `data/`, phiên làm việc, `panel-token.txt` hoặc khóa kho lưu trữ lên GitHub hoặc trong các cuộc trò chuyện.
8. **Không ghi lại** các tiêu đề `Authorization` hoặc nội dung yêu cầu tại máy chủ proxy ngược.

**Tôi có thể thay đổi mã thông báo bảng điều khiển mà không làm mất dữ liệu không?**

Có, nó chỉ mở bảng điều khiển. Dừng TgWitness, xóa `panel-token.txt`, khởi động lại. Sổ nhật ký, phiên và khóa vẫn còn. Nếu đã đặt `TGWITNESS_TOKEN`, giá trị đó được ưu tiên hơn tệp.

**Tại sao các tin nhắn không được mã hóa khi lưu trữ?**

Máy thu thập phải đọc chúng để tìm kiếm, so sánh và xuất. Một khóa trên cùng máy cũng không ngăn được người vốn đã đọc được máy đó. Mã hóa ổ đĩa bảo vệ ổ bị đánh cắp, quyền truy cập bảo vệ hệ thống đang chạy.

## Báo cáo lỗ hổng bảo mật

**Security → Report a vulnerability** trên GitHub. Phiên bản, tác động và cách tái hiện tối thiểu bằng dữ liệu giả. Không bao giờ gửi thông tin xác thực, thư mục tài khoản hay bằng chứng thật. Nếu báo cáo riêng tư bị tắt, hãy mở một issue xin kênh riêng tư, không kèm chi tiết khai thác.
