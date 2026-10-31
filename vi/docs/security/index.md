# Hãy đảm bảo tính bảo mật

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/security/

Hãy tìm hiểu các tuyến đường truyền cho Telegram, danh sách proxy công khai và các dịch vụ bên ngoài tùy chọn. Hãy nắm rõ mỗi tính năng bảo mật mang lại lợi ích gì, phạm vi bảo vệ của chúng bao gồm những gì và những gì người dùng cần tự đảm nhận.

**127.0.0.1**Địa chỉ bảng điều khiển theo mặc định

**256-bit**mã thông báo bảng ngẫu nhiên

**0**CDN, phân tích dữ liệu hoặc phông chữ từ xa

**Ed25519**chữ ký trên mỗi bản ghi

## Nơi lưu trữ mọi thông tin

Công cụ thu thập dữ liệu, bảng điều khiển của nó và mọi bản ghi được lưu trữ đều nằm trên máy tính hoặc máy chủ mà quý vị đang vận hành. Telegram là điểm đến duy nhất theo mặc định; mỗi điểm đến khác đều là một tùy chọn riêng biệt.

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
| **Mã thông báo bảng điều khiển** | `panel-token.txt` trong thư mục dữ liệu; trình duyệt chỉ lưu trữ tệp này cho riêng tab đó | Tất cả các tính năng trong mọi không gian làm việc: đọc và xuất dữ liệu, thay đổi phạm vi, đăng nhập vào các tài khoản | Dừng TgWitness, xóa mã `panel-token.txt`, khởi động lại: một mã thông báo mới sẽ được tạo ra |
| **Phiên làm việc trên Telegram** | Kho lưu trữ, được mã hóa (`credentials.enc`) | Tài khoản Telegram này | Kết thúc phiên làm việc trên Telegram tại *mục Cài đặt → Thiết bị* |
| **Khóa ký** | Kho lưu trữ, được mã hóa (`signing.enc`) | Các bản ghi được ký điện tử và có thể xác minh thông qua dấu vân tay của quý vị | Các điểm kiểm tra được lưu trữ tại nơi khác, cùng với chứng cứ và dấu thời gian, cho thấy những gì đã tồn tại trước đó |
| **Khóa kho lưu trữ** | Mã `vault.key` đi kèm với dữ liệu, hoặc một khóa chính bên ngoài dành cho thư mục dữ liệu mới | Giải mã kho lưu trữ | Hãy coi phiên làm việc và khóa ký cũng như đã bị rò rỉ |
| **Token Witness** | Trên máy chủ Witness | Chế độ chỉ đọc: các điểm kiểm tra đã được ký và trạng thái hoạt động | Xóa nội dung này trên trang Witness; tạo một nội dung mới |
| **Nội dung chính trên trang web bên ngoài** | Vault; chỉ cần tải xuống một lần để phục hồi | Giải mã bản sao lưu ngoài trang web | Bất kỳ ai nắm giữ các đối tượng được lưu trữ đều có thể giải mã chúng: hãy coi bản sao đó như đã bị lộ |

## Phạm vi bảo vệ bao gồm những gì

### Đã được đề cập

- Một bản ghi bị thay đổi, xóa bỏ hoặc sắp xếp lại trong tệp xuất: chuỗi băm hoặc chữ ký sẽ không còn khả năng xác minh được nữa.
- Một nhật ký bị cắt bớt hoặc được xây dựng lại sau khi điểm kiểm tra đã được lưu trữ ở nơi khác: điểm kiểm tra còn lưu giữ không còn khớp nữa.
- Dự đoán mã thông báo bảng điều khiển: 256 bit ngẫu nhiên, được so sánh trong thời gian không đổi; sau 15 lần thất bại trong một phút, địa chỉ đó sẽ bị từ chối.
- Nội dung trò chuyện có tính chất thù địch: văn bản được chèn dưới dạng văn bản thuần túy, không bao giờ dưới dạng HTML; các tệp đính kèm được tải xuống dưới dạng tệp; bảng điều khiển không tải bất kỳ nội dung nào từ các trang web khác.
- Một thư mục dữ liệu sao chép kèm theo khóa kho lưu trữ bên ngoài: các phiên làm việc và khóa ký vẫn được mã hóa ngay cả khi không có khóa chính.

### , xin để quý vị tự quyết định

- Người nắm giữ mã thông báo bảng điều khiển chính có toàn quyền kiểm soát. Hãy cấp cho những người khác quyền truy cập có giới hạn vào các tài khoản, cuộc trò chuyện và hành động mà họ cần; đồng thời bảo mật mã khóa chính.
- Quản trị viên của hệ thống có thể xem toàn bộ nội dung cũng như chỉnh sửa và ký lại sổ nhật ký. Vui lòng lưu giữ dấu vân tay và các điểm kiểm tra trên một hệ thống khác.
- Nội dung tin nhắn và tệp đa phương tiện không được TgWitness mã hóa. Quý vị nên sử dụng tính năng mã hóa đĩa và thiết lập quyền truy cập nghiêm ngặt.
- Việc sử dụng HTTP thuần túy ngoài phạm vi localhost sẽ khiến mã thông báo bị lộ trên mạng. Vui lòng sử dụng HTTPS hoặc đường hầm SSH.
- Các chữ ký chứng minh rằng nội dung đã được ghi lại không bị thay đổi, chứ không phải là mọi sự kiện trên Telegram đều được ghi lại.

[Chia sẻ quyền truy cập vào một vụ việc](https://phishdestroy.github.io/TgWitness/vi/docs/access/) kèm theo các quyền hạn, thời hạn hiệu lực và giới hạn phiên làm việc. Mã thông báo chứng nhân vẫn là một thông tin xác thực riêng biệt.

## Tăng cường bảo mật cho hệ thống cài đặt

Đã hoàn thành 0/8

1. **Hãy sử dụng một tài khoản Telegram chuyên dụng** — tuyệt đối không sử dụng tài khoản chính của quý vị. Mã thông báo bảng điều khiển và phiên làm việc sẽ cho phép quý vị kiểm soát hoàn toàn tài khoản đó.
2. **Vui lòng duy trì máy chủ tại địa chỉ 127.0.0.1.** Chỉ truy cập từ xa thông qua HTTPS (cấu hình Caddy đi kèm) hoặc qua đường hầm SSH.
3. **Mã hóa ổ đĩa** chứa thư mục dữ liệu: nội dung tin nhắn và tệp phương tiện được lưu trữ nguyên vẹn như khi nhận được.
4. **Hãy giới hạn thư mục dữ liệu** trong phạm vi tài khoản dịch vụ. Trên hệ điều hành Unix, các thư mục mới sẽ được gán quyền truy cập 0700; trên Windows, hãy thiết lập quyền truy cập cho thư mục đó.
5. **Vui lòng lưu giữ khóa chính của kho dữ liệu tại một vị trí khác** trên máy chủ: hãy thiết lập `TGWITNESS_VAULT_KEY_FILE` trước khi tạo thư mục dữ liệu.
6. **Vui lòng lưu dấu vân tay của khóa ký và các điểm kiểm tra** trên một hệ thống khác, đồng thời thêm một nhân chứng trên một máy chủ khác.
7. **Tuyệt đối không được tải lên các** khóa `data/`, phiên làm việc, `panel-token.txt` hoặc khóa kho lưu trữ lên GitHub hoặc trong các cuộc trò chuyện.
8. **Không ghi lại** các tiêu đề `Authorization` hoặc nội dung yêu cầu tại máy chủ proxy ngược.

**Tôi có thể thay đổi mã thông báo bảng điều khiển mà không làm mất dữ liệu không?**

Đúng vậy. Mã thông báo này chỉ dùng để mở bảng điều khiển. Hãy dừng TgWitness, xóa `panel-token.txt` khỏi thư mục dữ liệu và khởi động lại; nhật ký, các phiên làm việc và khóa vẫn được giữ nguyên. Khi `TGWITNESS_TOKEN` được thiết lập, giá trị môi trường sẽ được sử dụng thay cho tệp tin.

**Tại sao các tin nhắn không được mã hóa khi lưu trữ?**

Người thu thập dữ liệu phải đọc các bản ghi này để tìm kiếm, so sánh các phiên bản và xuất dữ liệu. Việc mã hóa chúng bằng một khóa trên chính máy tính đó sẽ không mang lại nhiều lợi ích trước những đối tượng có khả năng truy cập vào máy tính đó. Mã hóa ổ đĩa bảo vệ ổ đĩa đã ngừng hoạt động hoặc bị đánh cắp; trong khi đó, các quyền truy cập nghiêm ngặt sẽ bảo vệ ổ đĩa đang hoạt động.

## Báo cáo lỗ hổng bảo mật

Vui lòng sử dụng **mục Bảo mật → Báo cáo lỗ hổng bảo mật** trong kho lưu trữ GitHub. Vui lòng cung cấp thông tin về phiên bản, mức độ ảnh hưởng và hướng dẫn tái hiện tối thiểu. Tuyệt đối không gửi thông tin đăng nhập, thư mục tài khoản hoặc các kho lưu trữ bằng chứng thực tế. Trong trường hợp không thể báo cáo riêng tư, xin vui lòng mở một vấn đề (issue) để yêu cầu một kênh riêng tư mà không kèm theo chi tiết về lỗ hổng.
