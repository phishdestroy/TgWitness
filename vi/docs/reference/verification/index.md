# Những nội dung đã được kiểm thử

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/

Thử nghiệm Telegram trực tiếp, các kiểm tra tự động, kiểm tra trên trình duyệt và những nội dung vẫn chưa được xác minh.

## Thử nghiệm Telegram trực tiếp, toàn bộ tài khoản · Ngày 29 tháng 10 năm 2026

Tài khoản này vẫn tiếp tục hoạt động sau thử nghiệm dưới đây. Vào lúc 12:10 UTC ngày 29 tháng 10, phạm vi ghi chép đã được chuyển sang toàn bộ tài khoản (kênh, nhóm, cuộc trò chuyện riêng tư và bot); bảng điều khiển đã yêu cầu xác nhận và sổ nhật ký có chữ ký đã ghi lại thao tác này. Đến 17:59 UTC, sổ nhật ký ghi nhận:

| Thời gian ghi lại: từ 21:36 ngày 27 tháng 10 đến 17:59 ngày 29 tháng 10 theo giờ UTC | Số lượng |
| --- | --- |
| Các bản ghi trong sổ chứng cứ | 9,968 |
| Tin nhắn mới | 5,308 |
| của họ sau khi chuyển sang tài khoản đầy đủ | 3,878 |
| Các hành động xóa | 784 |
| trong số đó đã bị xóa sau khi TgWitness đã lưu lại tin nhắn | 596 |
| Các chỉnh sửa | 41 |
| Các tin nhắn được bổ sung sau khi kiểm tra lại | 2,273 |
| Các tin nhắn mà quá trình kiểm tra lại không thể tìm thấy được nữa | 18 |
| Các tin nhắn được lưu trữ thông qua các bản chụp lịch sử | 242 |
| Tệp đính kèm đã lưu | 247 |
| Trình thu thập bắt đầu | 19 |
| Telegram FloodWait tạm dừng | 26 |

- Chức năng kiểm tra **“Verify”** của ban chuyên gia đã xác nhận các chữ ký và chuỗi băm của toàn bộ 9.968 bản ghi.
- Các tin nhắn này đến từ 2 nhóm hoặc kênh và 3 cuộc trò chuyện riêng tư cùng các bot. Một nút gửi tin nhắn đã được nhấn từ **mục Trò chuyện**; yêu cầu và phản hồi của Telegram đều được ghi lại trong sổ nhật ký.
- Các cuộc trò chuyện mới đã được thêm vào khi trình thu thập dữ liệu quét lại tài khoản sau khi khởi động lại. Tính năng lưu trữ các tin nhắn trước đó của các cuộc trò chuyện mới đã bị tắt (`history = 0`), do đó nội dung này không được đề cập tại đây.

Không bao gồm: các phản ứng, thay đổi thành viên, hồ sơ cá nhân, việc gửi tin nhắn, tham gia qua lời mời, máy chủ proxy, thông báo, bot Witness và việc sử dụng nhiều tài khoản cùng lúc. Các tệp công khai chỉ chứa số liệu thống kê.

## Tệp xuất được bảo vệ bằng mật khẩu, mở bằng libarchive · Ngày 29 tháng 10 năm 2026

Một tệp lưu trữ được tạo bởi mã mã hóa xuất (WinZip AES-256, định dạng mà 7-Zip và WinRAR có thể đọc) đã được mở bằng Windows `tar` (bsdtar 3.6.2, libarchive). Khi nhập mật khẩu chính xác, tệp đã giải nén trùng khớp với giá trị SHA-256 ban đầu; mật khẩu sai sẽ bị từ chối với thông báo “Mật khẩu không chính xác”. Bản thân các phần mềm 7-Zip và WinRAR không được khởi chạy.

## Thử nghiệm Telegram trực tiếp · Từ ngày 27 đến ngày 29 tháng 10 năm 2026

Một tài khoản Telegram thực, được đăng nhập thông qua nhóm cặp API tích hợp sẵn, đã ghi lại một siêu nhóm từ **21:36 UTC ngày 27 tháng 10 đến 05:15 UTC ngày 29 tháng 10**. Trình thu thập dữ liệu đã được khởi động 12 lần trong khoảng thời gian đó.

| Đã ghi lại | Số lượng |
| --- | --- |
| Các bản ghi nhật ký, bao gồm các bản ghi hoạt động định kỳ và bản ghi dịch vụ | 2,385 |
| Tin nhắn mới | 1,291 |
| Các hành động xóa | 472 |
| trong số đó đã bị xóa sau khi TgWitness đã lưu lại nội dung văn bản | 347 |
| Các chỉnh sửa | 12 |
| Các tin nhắn bị bỏ sót trong thời gian ngừng hoạt động đã được bổ sung thông qua quá trình kiểm tra lại | 12 |
| Tệp đính kèm đã lưu | 17 |
| Các tệp đính kèm chưa được tải xuống (chức năng tải xuống bị tắt hoặc không có tệp để tải xuống) | 14 |
| Telegram FloodWait sẽ tạm dừng, mỗi lần 3 giây, trong quá trình kiểm tra lại | 8 |

- Các chữ ký và chuỗi băm của toàn bộ 2.385 bản ghi đều được xác minh dựa trên khóa công khai của sổ nhật ký.
- Sau khi khởi động lại, trình thu thập dữ liệu sẽ tiếp tục từ trạng thái cập nhật đã lưu (`pts`) và Telethon sẽ tiến hành đồng bộ hóa; quá trình kiểm tra lại sau đó sẽ bổ sung các tin nhắn còn thiếu.
- Trong mỗi lần FloodWait, bộ thu thập sẽ chờ trong khoảng thời gian được yêu cầu rồi tiếp tục hoạt động.
- Tài khoản vẫn duy trì trạng thái đăng nhập, và cùng phiên làm việc đó đã kết nối lại vào ngày 29 tháng 10.

Những nội dung sau đây không nằm trong phạm vi kiểm tra này: việc quản lý nhiều tài khoản cùng lúc, vai trò quản trị viên, máy chủ proxy, các sự cố ngừng hoạt động kéo dài hơn vài giờ và toàn bộ [quy trình chấp nhận trực tiếp](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Các tệp công khai chỉ chứa các số liệu thống kê này: không bao gồm thông tin nhận dạng tài khoản hay cuộc trò chuyện, tin nhắn hoặc thông tin đăng nhập.

Các mục cũ hơn dưới đây mô tả các lần chạy riêng lẻ; hầu hết trong số đó đều sử dụng các máy khách thử nghiệm tổng hợp. Kết quả tự động mới nhất được trình bày dưới đây.

## Danh sách MTProxy công khai được tích hợp sẵn · Ngày 29 tháng 10 năm 2026

Đây là bản ghi thử nghiệm lịch sử của phiên bản ban đầu được chọn thủ công. Đối với các chế độ nhóm tự động và IP hiện tại, vui lòng tham khảo [cài đặt kết nối](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/#ip-modes). Các số liệu thống kê và tính năng không được hỗ trợ dưới đây thuộc về phiên bản đã được thử nghiệm đó.

Đã bổ sung bản chụp nhanh công khai được gói sẵn và tính năng làm mới HTTPS rõ ràng từ SoliSpirit/mtproto và zakky8/mtproto-proxy-pro. Trên máy chủ này, trình tải xuống ứng dụng đã truy xuất thành công cả hai nguồn cấp dữ liệu vào lúc 12:58 UTC ngày 29 tháng 10 năm 2026: **118 điểm cuối tương thích duy nhất** sau khi lọc, loại trừ trùng lặp và áp dụng giới hạn 64 mục cho mỗi nguồn. Điều này xác nhận việc truy xuất danh sách, chứ không phải khả năng kết nối hay việc truyền tải tin nhắn qua các điểm cuối đó. Không có tài khoản thực nào được kết nối với máy chủ proxy nào trong danh sách trong quá trình thực hiện công việc này. [Hướng dẫn dành cho nhà điều hành và người dùng](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/PROXIES.md).

Các phản hồi nguồn không thành công/trống/không tương thích sẽ giữ nguyên các mục và ngày tháng trước đó. Các bản cập nhật không thay đổi lộ trình đã chọn. Các địa chỉ công khai được xác thực và các địa chỉ IP được giải quyết sẽ được cố định khi được chọn; các lộ trình do nhà điều hành/thủ công thiết lập vẫn được tách biệt. Tính năng kiểm tra kết nối hiện đã có sẵn trên bảng điều khiển trước khi đăng nhập tài khoản. TLS ee giả mạo và tính năng chọn proxy tự động vẫn chưa được hỗ trợ. Danh mục của nhà điều hành sẽ hoàn toàn ghi đè lên các đăng ký.

- Bộ kiểm thử đầy đủ: **366 bài kiểm tra đạt, 3 bài bỏ qua**, 287,94 giây. Các cảnh báo về phụ thuộc hiện có và các trường hợp bỏ qua do nền tảng vẫn còn tồn tại. Kiểm tra hồi quy danh sách công khai/bản địa hóa cuối cùng: **36 bài đạt**, bao gồm việc từ chối các cổng proxy tải xuống không hợp lệ; phần này trùng lặp với bộ kiểm thử đầy đủ.
- Đã vượt qua kiểm tra tương thích trình duyệt ở các ngôn ngữ tiếng Anh/tiếng Nga, chế độ sáng/tối ở độ phân giải 390/1440 pixel: các tùy chọn được tích hợp sẵn, không tải dữ liệu bên ngoài khi mở cài đặt, làm mới rõ ràng, duy trì đường dẫn và bộ nhớ đệm trong trường hợp sự cố, kiểm tra trước khi đăng nhập, cách ly không gian làm việc khi phản hồi chậm, chi tiết nguồn và bố cục/độ tương phản. Không có lỗi JavaScript hoặc yêu cầu từ trình duyệt bên ngoài.
- Việc dịch tĩnh cuối cùng đã hoàn tất cho tất cả 13 ngôn ngữ; nội dung mới đã được dịch sang tiếng Nga, kèm theo các tùy chọn tiếng Anh rõ ràng ở những phần khác. Hướng dẫn tích hợp đã được cập nhật và đã vượt qua các kiểm tra về bố cục/độ tương phản trên cả hai chủ đề.
- Đã vượt qua các bước kiểm tra sơ bộ và kiểm tra xuất bản (259 tệp công khai, 1.354 liên kết cục bộ); đã cập nhật Đã phân tích cú pháp tệp YAML của Compose và CI. Docker và CI từ xa không được thực thi tại đây.
- Bản phát triển lại đã vượt qua các bước kiểm tra cài đặt độc lập, tải danh sách gói phần mềm đi kèm và xác minh xuất bản có chữ ký . Tất cả 69 tài nguyên gói phần mềm đều khớp với không gian làm việc; các giá trị băm mã nguồn đã được kiểm tra.

Biên lai: `test-results/public-proxy-research/download-receipt.json`, `test-results/public-proxy-research/copy-receipt.json`, `test-results/public-proxies-full-suite.log`, `test-results/public-proxies-final-focused.log`, `test-results/public-proxies-browser/receipt.json` và `test-results/public-proxies-package.log`. Các thiết lập trình duyệt/tài khoản/giao thức truyền tải là giả định; hai yêu cầu tải xuống nguồn cấp dữ liệu ở trên là các yêu cầu HTTPS thực tế.

## Bài thuyết trình về các tính năng bổ sung tùy chọn · Ngày 29 tháng 10 năm 2026

Trang đích trước đây của bot Proof nay đã được chuyển sang **mục Extras**: bao gồm một phần tổng quan ngắn gọn, tiếp theo là một trang thiết lập riêng biệt dành cho tùy chọn đã chọn. Biểu mẫu Witness gồm ba bước, với các mục quản lý kết nối, tùy chọn mạng và chi tiết triển khai được ẩn đi. GitHub được lên kế hoạch rõ ràng và không yêu cầu điền thông tin đăng nhập. [Tổng quan bằng tiếng Nga](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/EXTRAS.md).

- Đã vượt qua 30 bài kiểm tra chuyên sâu về bản địa hóa, thiết lập TgWitness và kiểm tra trước khi xuất bản.
- Việc kiểm tra thiết lập Chromium đã đạt yêu cầu ở các phiên bản tiếng Anh/tiếng Nga, chế độ sáng/tối, ở độ phân giải 390/1440 pixel: tập trung bàn phím và phím Enter, không có kết nối ngầm khi chọn các tính năng bổ sung, lưu giữ bản nháp, tải xuống cấu hình/mã thông báo đã ghim, xóa mã thông báo khi khóa màn hình, và các liên kết hướng dẫn cục bộ hoạt động bình thường. Đã vượt qua các kiểm tra về bố cục và độ tương phản giữa văn bản với nền đồng nhất.
- Việc chấp nhận chuyển đổi không gian làm việc đã được thông qua, bao gồm cả phản hồi mã thông báo bị trì hoãn sau khi chuyển đổi. Việc điều hướng nhanh giúp tìm thấy các tính năng bổ sung thông qua các thuật ngữ liên quan đến bot, bằng chứng và GitHub; các kiểm tra hiện có về độ phân giải 320/390/1440 pixel cũng như hỗ trợ tiếng Nga và RTL cũng đã vượt qua.
- Không phát hiện thấy lỗi JavaScript hay yêu cầu trình duyệt bên ngoài nào trong quá trình thiết lập. Đây là các kiểm tra giao diện người dùng (UI) mô phỏng, không phải bằng chứng mới từ Telegram trực tiếp hay bài đăng của bot.
- Quá trình tải ngôn ngữ cuối cùng và phạm vi bao phủ từ điển đã hoàn tất thành công cho tất cả 13 ngôn ngữ, đồng thời duy trì các tùy chọn tiếng Anh rõ ràng làm phương án dự phòng đối với các ngôn ngữ khác ngoài tiếng Nga. Hướng dẫn Proof mở rộng cũng đã vượt qua các kiểm tra bố cục/độ tương phản ở các độ phân giải 320/768/1440 pixel trên cả hai chủ đề.
- Bản dựng lại đã vượt qua quá trình kiểm tra cài đặt độc lập và xác minh xuất bản có chữ ký. Tất cả 67 tài nguyên được đóng gói đều khớp với không gian làm việc; kho lưu trữ nguồn chứa 253 tệp công khai. Việc kiểm tra nguồn/liên kết đã thành công đối với 1.346 liên kết tài liệu cục bộ.

Các mã xác nhận: `test-results/setup-browser/receipt.json`, `test-results/quick-navigation/receipt.json`, `test-results/extras-final.json`, `test-results/extras-package.log` và `test-results/extras-artifacts.json`. Các tài liệu ảnh chụp màn hình sử dụng không gian làm việc mô phỏng.

## Kiểm tra thiết lập bot Witness và máy chủ proxy · Ngày 29 tháng 10 năm 2026

Quá trình thiết lập Witness (hiện tại là **Extras → Một bot trong kênh của quý vị**) sẽ chuẩn bị một Witness được triển khai độc lập: khóa thu thập được ghim cố định , tải xuống mã thông báo có phạm vi giới hạn, kênh riêng, chính sách công bố, tuyến đường HTTP/SOCKS5 và API Bot tùy chỉnh. Token bot vẫn được lưu trữ trên máy chủ chứng cứ. Token mới của nó (`--check-config`) xác thực cấu hình và các tệp mà không cần thiết lập kết nối mạng hay tạo khóa. Đường dẫn tệp JSON được xác định bên cạnh tệp cấu hình. Tất cả các biến thể chứng cứ của Compose hiện đều chuyển tiếp các thiết lập proxy HTTP và Bot API.

Cài đặt tài khoản hỗ trợ danh mục MTProxy công khai do người vận hành quản lý, tính năng xem trước liên kết proxy Telegram tùy chỉnh và các trường nhập liệu thủ công hiện có. Các phản hồi từ danh mục sẽ loại bỏ thông tin bí mật; khi chọn, lộ trình sẽ được lưu trữ trong kho lưu trữ của không gian làm việc. Trong trường hợp danh mục bị thiếu hoặc có định dạng không đúng, các lộ trình thủ công vẫn có thể được sử dụng. Không có địa chỉ proxy dự án hay dịch vụ chứng kiến được lưu trữ nào được tạo ra hoặc kích hoạt theo mặc định. Một ví dụ về Caddy chỉ hiển thị điểm cuối head trong phạm vi nhất định khi một nhân chứng bên ngoài cần tiếp cận bộ thu thập dữ liệu mà bảng điều khiển của bộ thu thập đó vẫn được giữ riêng tư.

Xác thực:

- Bộ kiểm thử đầy đủ: **348 bài kiểm tra đạt, 3 bài bị bỏ qua**, thời gian thực hiện 195,81 giây. Các hạn chế của hệ điều hành Windows là nguyên nhân dẫn đến việc bỏ qua các bài kiểm tra; hai cảnh báo về việc ngừng hỗ trợ các phụ thuộc hiện có vẫn còn tồn tại.
- Chuỗi kiểm thử hồi quy cuối cùng cho phiên bản Witness/cấu hình/phát hành: **11 bài kiểm tra đạt, 1 bài bị bỏ qua**. Chuỗi kiểm thử này trùng lặp với bộ kiểm thử đầy đủ. Các bài kiểm tra bao gồm giải quyết đường dẫn, kiểm tra sơ bộ ngoại tuyến, quá trình ký/xuất bản thông qua một thiết bị mô phỏng API Bot HTTP loopback thực tế, lỗi gửi tin nhắn đã ghi lại, xác minh mã thông báo kênh và loại trừ thông tin bí mật proxy.
- Quá trình thiết lập Chromium đã được kiểm tra thành công bằng tiếng Anh/tiếng Nga ở độ phân giải 390/1440 pixel: cấu hình cố định và tải xuống mã thông báo, xóa mã thông báo khi khóa màn hình, lựa chọn danh mục, xem trước liên kết tùy chỉnh tiếp theo là thao tác lưu rõ ràng, bố cục/độ tương phản và không có lỗi JavaScript hay yêu cầu từ trình duyệt bên ngoài. Đã khắc phục tình trạng tiêu đề tài khoản tiếng Nga bị thu hẹp và hiện tượng tràn ngoài trên tab đăng nhập.
- Đã vượt qua các bước kiểm tra Ruff, kiểm tra nguồn/liên kết cũng như phân tích cú pháp YAML cho Compose và quy trình làm việc.
- Công cụ được tái cấu trúc này đã vượt qua các bài kiểm tra cài đặt độc lập, kiểm tra bảng điều khiển/tài nguyên tĩnh và xác thực API, cùng với việc xác minh độc lập đối với các bản xuất tổng hợp gồm 32 sự kiện, bao gồm cả dạng trực tiếp và dạng truyền phát.

Biên lai: `test-results/setup-full-suite.log`, `setup-final-focused.log`, `setup-browser/receipt.json`, `setup-browser-final.log` và `setup-package.log`. Các kiểm tra này sử dụng các tài khoản tổng hợp/máy chủ proxy và một thiết bị cố định Bot API cục bộ. Chúng không tuyên bố là một bản phát hành bot thực tế, máy chủ MTProxy công cộng đang hoạt động, quá trình chạy CI từ xa hay triển khai Docker . Lịch sử quan sát Telegram thực tế được lưu giữ ở trên vẫn là một bằng chứng riêng biệt. [Hướng dẫn thiết lập](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

## Đánh giá bản trình bày và tài liệu · Ngày 29 tháng 10 năm 2026

Trang giới thiệu sản phẩm, màn hình truy cập, các tệp README bằng tiếng Anh/tiếng Nga và hình ảnh trình bày hiện đã thống nhất một phong cách thiết kế chung. Các ảnh chụp màn hình công khai sử dụng dữ liệu demo giả định. Bản cập nhật này cũng đã sửa chữa các mô tả đã lỗi thời về tính năng xác thực trực tiếp và khôi phục dữ liệu ở phần trên.

- Các bài kiểm thử bản địa hóa, trang web và xuất bản được tập trung thực hiện: **33 bài đã vượt qua, 1 bài bị bỏ qua**. Bài kiểm thử bị bỏ qua yêu cầu tạo liên kết tượng trưng (symlink), tính năng này hiện không khả dụng trên máy chủ này.
- Việc chấp nhận bảng điều khiển Chromium chung đã được thông qua, bao gồm tất cả các danh mục ngôn ngữ, bố cục RTL, chế độ sáng/tối, độ tương phản văn bản ổn định và tính năng chuyển đổi không gian làm việc. Quá trình kiểm tra việc tạo hồ sơ hiện sẽ chờ phản hồi HTTP thực tế trước khi kiểm tra không gian làm việc đã chọn.
- Các màn hình truy cập bằng tiếng Anh/tiếng Nga đã vượt qua các kiểm tra về bố cục và độ tương phản trên cả hai chủ đề ở các độ phân giải 320, 390, 768, 850 và 1440 pixel; nút gửi vẫn nằm trong vùng hiển thị ban đầu.
- Trang web công khai đã vượt qua các mức độ tương thích ở các độ phân giải 320, 390, 768, 1024 và 1440 pixel, bao gồm , chức năng phóng to ảnh chụp màn hình/phím Escape/quay lại tiêu điểm, chuyển tab bằng bàn phím, tính năng từ chối khay nhớ tạm, các đường dẫn con của dự án, hiệu ứng chuyển động giảm thiểu và chế độ dự phòng không sử dụng JavaScript. Không ghi nhận bất kỳ lỗi yêu cầu tài nguyên, yêu cầu bên ngoài hay lỗi JavaScript nào.
- Bản cập nhật mới nhất đã vượt qua kiểm tra cài đặt độc lập: các tài nguyên bảng điều khiển và cài đặt ngôn ngữ được tải thành công, việc truy cập API yêu cầu xác thực, đồng thời các bản xuất trực tiếp và theo luồng đều xác minh độc lập toàn bộ 32 sự kiện mô phỏng. Các kiểm tra Ruff và nguồn công khai/liên kết cũng đã đạt yêu cầu.

Các bản ghi địa phương: `test-results/design-tests.log`, `design-panel-final.log`, `design-review-final.log`, `design-site.log` và `design-package/install-receipt.json`. Bộ công cụ backend hoàn chỉnh đã không được chạy lại cho bản trình bày/thay đổi tài liệu này; kết quả trước đó vẫn được lưu giữ trong bản kiểm toán trước khi công bố.

## Phiên bản 0.6.1

Phiên bản 0.6.1 thay đổi giao diện bảng điều khiển, trình khởi chạy, gói phần mềm và tài liệu hướng dẫn; mã nguồn liên quan đến việc thu thập, lưu trữ, ký số và xuất dữ liệu vẫn giữ nguyên. Trên Windows 11 / Python 3.12.10 với môi trường chạy được ghim:

- Bộ công cụ hoàn chỉnh đã vượt qua **137 bài kiểm tra** với **2 trường hợp bỏ qua** và cảnh báo Starlette hiện có. Các bài kiểm tra mới bao gồm việc xử lý phím tắt Ctrl+C của trình khởi chạy (máy chủ có 30 giây để tắt hệ thống một cách trật tự) và các lỗi có thể khắc phục trong các bước thiết lập.
- Chromium (vỏ không giao diện 156) đã vượt qua toàn bộ **45 kịch bản chung** và **35 kịch bản liên quan đến nhập tài khoản/mã QR/khóa xác thực**, bao gồm kiểm tra độ tương phản của văn bản đặc, không xảy ra hiện tượng tràn ngang ở độ phân giải 320–1440 px và các trường đăng nhập đầu tiên hiển thị rõ ràng ở độ phân giải 320/390 px. Không phát hiện thấy lỗi JavaScript trên trang hay yêu cầu bên ngoài nào.
- `python start.py --setup-only` đã cài đặt lại gói phần mềm với phiên bản 0.6.1 và `python start.py --check` báo cáo đã sẵn sàng. Một máy chủ `python -m tgwitness --demo` thực sự đã trả về bảng điều khiển, bảng kiểu, tập lệnh, biểu tượng, hướng dẫn và phiên bản `/api/status` 0.6.1; máy chủ `workspace.css` đã bị gỡ bỏ trả về mã trạng thái 404.
- `Start.cmd` đã phát hiện một bản cài đặt Python nằm ngoài biến môi trường PATH. Do không có Python sẵn có, hệ thống đã hiển thị lời đề nghị cài đặt; sau khi từ chối, hệ thống đã hiển thị hướng dẫn thủ công và thoát khỏi bước 1. Bước tải xuống từ python.org đã lấy được trình cài đặt phiên bản 3.12.10 và vượt qua kiểm tra Authenticode của Python Software Foundation; bản thân trình cài đặt này không được chạy trên máy chủ này.
- `start.sh`, khi không có bất kỳ lệnh Python nào, đã hiển thị gợi ý cài đặt và thoát khỏi chương trình. 1. `scripts\Docker.cmd` và `scripts/docker-start.sh` đã được thử nghiệm với các tệp thực thi `docker` giả mạo: trình tự gọi hàm đúng, địa chỉ bảng điều khiển và đầu ra mã thông báo chính xác, đồng thời không hiển thị thông báo thành công sau khi xảy ra lỗi.
- `python tools/build_portable.py` đã xây dựng một gói Windows có dung lượng 18,8 MiB sau khi xác minh tổng kiểm tra của runtime nhúng được ghim. Sau khi giải nén vào một đường dẫn có chứa khoảng trắng và chỉ khởi động với các thư mục `C:\Windows` trong biến môi trường PATH, Python nhúng trong đó đã vượt qua bài kiểm tra `TgWitness-Check.cmd`, phục vụ bản demo (32 sự kiện) và một không gian làm việc trực tiếp, đồng thời Chromium đã hiển thị nhật ký và ngăn chi tiết mà không gặp lỗi JavaScript nào. Dữ liệu đã được ghi vào thư mục `data` của gói phần mềm.
- `python tools/build_preview.py` đã tạo ra một kho lưu trữ nguồn gồm 110 tệp. Một lần chạy thử của `git add` đã liệt kê chính xác 110 tệp này mà không có tệp phiên làm việc, khóa, cơ sở dữ liệu, mã thông báo, nhật ký hoặc tệp xuất , không có đường dẫn tuyệt đối cục bộ và không có chuỗi ký tự mang hình thức thông tin bí mật.

Các tác vụ sau đây chưa được thực hiện trong đợt đóng gói ngày 27 tháng 10 này: quá trình cài đặt tự động Python , các kiểm tra xây dựng Docker/Compose, các lần chạy trên Linux/macOS hoặc bài kiểm tra tài khoản trực tiếp mới. Bằng chứng Telegram thực tế được ghi lại ở phần trên và trong các bài kiểm tra tài khoản trước đó ở phần dưới. Chỉ riêng các định nghĩa CI không đủ điều kiện để xác nhận việc thực thi trên nền tảng.

## Phiên bản 0.6.0

Bộ công cụ chạy thời gian thực (pinned-runtime) đầy đủ mới nhất trên Windows 11 / Python 3.12.10 đã vượt qua **135 bài kiểm tra**, với **1 bài bị bỏ qua**, trong thời gian 26,53 giây và vẫn còn cảnh báo Starlette hiện có. Lỗi bỏ qua này yêu cầu quyền truy cập POSIX. Sau khi thêm trình hiển thị mã QR vào các kiểm tra sẵn sàng và đo lường quy trình, 8 kiểm tra sẵn sàng/không gian làm việc bị ảnh hưởng cũng đã vượt qua.

Phạm vi bao quát mới bao gồm các lược đồ Telethon 7/8, các lược đồ Pyrogram 2/3, JSON hoàn chỉnh và JSON chỉ chứa siêu dữ liệu, các tệp tài khoản trùng khớp/mâu thuẫn, mã thông hành TData, việc can thiệp vào tổng kiểm tra và các đường dẫn không an toàn, chuyển đổi ngoại tuyến/đã xác thực trong bộ nhớ, kiểm tra ID tài khoản trực tuyến, trạng thái thành công của mã QR/xác thực hai yếu tố (2FA)/hết hạn, hủy bỏ do hết hạn và cách ly tài khoản. Các fixture TData sử dụng một triển khai AES-IGE riêng biệt để mã hóa.

Chromium đã vượt qua **45 tình huống chung** và **35 tình huống liên quan đến nhập tài khoản/mã QR/Khóa xác thực**, không ghi nhận bất kỳ lỗi JavaScript trên trang hay yêu cầu bên ngoài nào. Các kiểm tra trình duyệt mới bao quát đồng thời cả bốn định dạng đầu vào, dữ liệu TData được bảo vệ, siêu dữ liệu API, hiển thị mã QR, hết hạn/thử lại, xác thực hai yếu tố (2FA), từ chối tài khoản sai, hủy khóa/không gian làm việc, bố cục đáp ứng và các phản hồi chuyển đổi chậm trễ sau khi chọn tệp mới hơn.

Cả hai bộ trình duyệt đều vượt qua kiểm tra lần nữa sau khi thực hiện các thay đổi liên quan đến mục nhập tài khoản. Thiết lập trực tiếp sẽ mở biểu mẫu tài khoản; chế độ demo sẽ mở sổ nhật ký mẫu. Trang Tài khoản trong chế độ demo hiển thị hướng dẫn khởi động trực tiếp và ẩn các trường nhập thông tin đăng nhập. Các kiểm tra tập trung ở các độ phân giải 320, 390 và 1440 pixel đã xác nhận rằng trường số và nút chính vừa vặn mà không cần cuộn trang, các trường API ban đầu được thu gọn, và độ tương phản văn bản vẫn đảm bảo khả năng đọc. Các điều khiển ghi lại và xác minh vẫn được che phủ sau khi mở các phần mở rộng mới của chúng.

Quy trình Auth Key trực tiếp đã được thực hiện bằng thông tin đăng nhập tổng hợp thông qua các điểm cuối nhập và ủy quyền thực tế. Các kiểm tra bao gồm khóa không đầy đủ, thiếu DC, ID người dùng không chính xác, danh tính tài khoản không khớp, thông tin đăng nhập API đã lưu, tiến trình yêu cầu hiển thị, xóa thông tin bí mật và các phản hồi chậm trễ sau khi chỉnh sửa hoặc thay đổi phương thức. Cả bốn phương thức đăng nhập đều đã được kiểm tra ở các độ phân giải 320, 390 và 1440 pixel. Trình chọn tệp xuất hiện trước hướng dẫn về định dạng, và nút “Kết nối” vừa vặn với khung nhìn ban đầu 844 pixel khi các cài đặt API được thu gọn. Không có nỗ lực ủy quyền bằng Khóa xác thực thực tế nào được thực hiện trong lần chạy kiểm tra chấp nhận giao diện người dùng này.

Việc làm mới bảng điều khiển đã được kiểm tra lại bằng cả hai bộ trình duyệt: không phát hiện thấy lỗi JavaScript trên trang hay yêu cầu bên ngoài nào. Bộ tài liệu hướng dẫn tài khoản hiện bao gồm việc dán một cặp ID API/băm, từ chối các cặp bị lỗi định dạng hoặc nhiều cặp mà không thay thế các trường, hướng dẫn chỉ dành cho siêu dữ liệu, và bỏ qua các phản hồi nhập liệu đã hết hạn sau khi thay đổi phương thức đăng nhập hoặc chỉnh sửa thông tin đăng nhập thủ công. Sáu kiểm tra chuyên sâu bổ sung đã đạt yêu cầu đối với hướng dẫn thiết lập, các thao tác bắt đầu/tạm dừng rõ ràng, khôi phục tìm kiếm trống, cũng như bố cục cuối cùng của kết nối/hướng dẫn cục bộ và độ tương phản văn bản ổn định ở các độ phân giải 320, 390 và 1440 pixel. Bản cập nhật đăng nhập trực tiếp bổ sung thao tác yêu cầu số điện thoại/mã xác thực duy nhất và tái sử dụng cặp API đã lưu của không gian làm việc hiện tại cho đăng nhập qua số điện thoại, mã QR và phiên làm việc. Bộ kiểm tra Python đầy đủ nêu trên bao gồm các bài kiểm tra mới về tính bền vững, từ chối thông tin đăng nhập không đầy đủ và cách ly không gian làm việc. Các kiểm tra trên trình duyệt bao gồm nhập số điện thoại trực tiếp, tái sử dụng thông tin đăng nhập đã lưu, định tuyến chỉ dựa trên siêu dữ liệu, ủy quyền tệp bằng một nút bấm và từ chối tài khoản trùng lặp. Các biểu mẫu mã thông báo bảng điều khiển và số điện thoại được đơn giản hóa cũng đã được kiểm tra mà không cần cuộn ban đầu ở các độ phân giải 320, 390 và 1.440 pixel. Một kiểm tra tương thích đã xác nhận rằng biểu mẫu số điện thoại trực tiếp có thể sử dụng các điểm cuối cấu hình/mã trước đó trong khi quy trình cũ vẫn đang chạy.

Một tài khoản do người dùng cung cấp đã được kiểm tra riêng biệt, ngoài các môi trường thử nghiệm công khai. Các dữ liệu đầu vào Telethon, Pyrogram và TData của tài khoản này đều dẫn đến cùng một thông tin ủy quyền; tệp JSON đi kèm cung cấp thông tin đăng nhập API. Cả bốn tệp đều được tải lên thông qua bảng điều khiển phiên bản 0.6.0 và Telegram đã xác nhận ID tài khoản số như dự kiến. Các tệp nguồn vẫn giữ nguyên. Không có nguồn nào được chọn và chế độ quan sát vẫn ở trạng thái tắt. Điều này chỉ đáp ứng tiêu chí cho một ví dụ về nhập dữ liệu/đăng nhập, chứ không phải thu thập, khôi phục hoặc khả năng hoạt động thực tế.

Telegram cũng đã phát hành một mã QR thực, nhưng mã này đã bị hủy trước khi được quét. Toàn bộ quy trình xác nhận mã QR và xác thực hai yếu tố (2FA) đã được thực hiện thông qua các ứng dụng khách mô phỏng; việc xác nhận trên thiết bị di động thông qua ứng dụng Telegram thực tế vẫn là một bước chấp nhận riêng biệt. Không có bất kỳ thông tin nhận dạng tài khoản thực, thông tin bí mật hay ảnh chụp màn hình nào được bao gồm trong các tệp công khai.

Việc nâng cấp trình khởi chạy đã hoàn tất; nguồn, siêu dữ liệu đã cài đặt và chỉ báo sẵn sàng báo cáo phiên bản 0.6.0, với mã QR 8.2 và mã `pip check` đạt yêu cầu. Bánh xe đã cài đặt phục vụ bảng điều khiển và hướng dẫn, từ chối các yêu cầu API không được xác thực, đồng thời độc lập xác minh các bản xuất tổng hợp 32 sự kiện theo dạng trực tiếp và phát trực tuyến. Hướng dẫn ngoại tuyến đã được cập nhật đã được kiểm tra ở các độ phân giải 320, 390 và 1440 pixel. Các ảnh chụp màn hình công khai vẫn là ảnh tổng hợp.

Bản phát hành nguồn chứa 107 tệp nằm trong danh sách cho phép. Các liên kết tài liệu cục bộ hoạt động bình thường. Việc triển khai trên Docker/Caddy, xuất bản CI/gói phần mềm từ xa, môi trường chạy ARM64, thu thập dữ liệu liên tục cùng ma trận chấp nhận Telegram trực tiếp đầy đủ vẫn chưa được đề cập đầy đủ tại đây.

## Phiên bản 0.5.1

Trên Windows 11 / Python 3.12.10, bộ môi trường dự án đầy đủ đã vượt qua kiểm tra: **94 bài kiểm tra thành công, 2 bài bị bỏ qua**, trong 31,21 giây, kèm theo cảnh báo Starlette hiện có. Các bước bị bỏ qua yêu cầu quyền truy cập POSIX và việc tạo liên kết tượng trưng (symlink) – những tính năng không có sẵn trên máy chủ này. Fixture HTTP tải xuống đã hiển thị chẩn đoán luồng yêu cầu; tất cả các khẳng định đều đạt yêu cầu. Lần chạy này không khẳng định chắc chắn rằng không có vấn đề về truyền tải trên máy chủ.

Các bài kiểm tra phạm vi hồi quy mới đã loại trừ StringSession, các thay đổi về mã nguồn và tài khoản 2FA, hủy tra cứu danh tính, hủy đăng nhập đang chờ xử lý, cũng như các bản cập nhật thông qua các trình xử lý đã đăng ký trên các máy khách đang hoạt động, bị từ chối, bị thay thế và máy khách thăm dò. Chỉ có bộ thu thập đang hoạt động mới đóng góp các sự kiện; thông tin đăng nhập đã lưu và lịch sử có chữ ký vẫn được giữ nguyên vẹn. Các kiểm tra mới khác bao gồm tìm kiếm Unicode sau khi mở lại cơ sở dữ liệu, việc đưa các ranh giới chính sách giám sát vào phạm vi kiểm tra, cũng như các trường hợp loại trừ gói phần mềm nguồn mở.

Dự án thực tế `pythonw.exe` đã khởi chạy một bảng tổng hợp độc lập, trả về mã trạng thái HTTP 200 và lưu giữ các chẩn đoán khởi động trong `logs/server.log`. Nhật ký không chứa mã thông báo bảng tổng hợp được tạo ra cũng như các bản ghi truy cập HTTP. Thử nghiệm chỉ chấm dứt quá trình tổng hợp của chính nó. Không có tác vụ nào trong Trình lập lịch tác vụ được đăng ký; việc đăng nhập/đăng xuất, chế độ ngủ và khôi phục dịch vụ vẫn là các tiêu chí đánh giá riêng biệt.

Quá trình kiểm tra tương thích với Chromium đã vượt qua **45 tình huống**, không ghi nhận lỗi JavaScript trên trang và không phát hiện yêu cầu bên ngoài nào. Các kiểm tra mới bao gồm ngày và giờ trên dòng thời gian có độ phân giải 601/768/850 pixel, bản nháp tệp đính kèm trong quá trình làm mới trạng thái, các chỉnh sửa mới được thực hiện trong khi lưu, kết quả xác minh bị xóa khi chuyển đổi tài khoản, phản hồi xác minh chậm trễ sau khi chuyển sang ứng dụng khác rồi quay lại, và các ranh giới xác minh rõ ràng khi có sự kiện mới xuất hiện. Khoảng cách giữa biểu tượng tìm kiếm và văn bản cũng đã được điều chỉnh và bộ trình duyệt đã được chạy lại.

Quá trình chạy trình duyệt đã sử dụng môi trường chạy được ghim sẵn trong `.venv` và phiên bản Playwright 1.62.0/Chromium do hệ thống cung cấp sẵn, được bổ sung vào đường dẫn nhập sau môi trường dự án. Quá trình cài đặt phụ thuộc phát triển tùy chọn đã bị dừng lại do tốc độ tải xuống Playwright chậm; không có phiên bản công cụ trình duyệt mới nào đáp ứng yêu cầu. Một quy trình `python start.py --setup-only` thông thường đã hoàn tất việc nâng cấp ứng dụng. Nguồn, siêu dữ liệu đã cài đặt và báo cáo đánh dấu của trình khởi chạy ghi nhận phiên bản 0.5.1; `pip check` đã vượt qua kiểm tra. Các kiểm tra sẵn sàng đã vượt qua trên một đường dẫn mới chưa từng sử dụng, đồng thời vẫn duy trì cảnh báo dự kiến về khóa kho lưu trữ cục bộ.

Gói 0.5.1 đã được cài đặt riêng biệt và kiểm tra sơ bộ: tất cả các tài nguyên bảng điều khiển/hướng dẫn đều được cung cấp, quyền truy cập API không được xác thực đã bị từ chối, và cả hai tệp ZIP bằng chứng gồm 32 sự kiện (dạng trực tiếp và dạng truyền trực tuyến) đều đã vượt qua quá trình xác minh độc lập. Các tệp ứng dụng trong gói đã cài đặt đã được so sánh với mã nguồn. Kho lưu trữ mã nguồn công khai sử dụng danh sách cho phép loại tệp rõ ràng và từ chối các tệp nguồn được liên kết; các tài liệu thời gian chạy được đặt bên trong các thư mục mã nguồn sẽ bị loại trừ khỏi các bài kiểm tra hồi quy.

Trong quá trình chạy sửa lỗi mã nguồn, tập hợp nguồn mở và tập hợp ứng viên Git bao gồm 86 tệp, không bao gồm các thư mục dữ liệu thời gian chạy. Quá trình quét các mẫu khóa riêng, mã thông báo GitHub, mã thông báo bot Telegram và StringSession có thể nhận diện được không tìm thấy kết quả trùng khớp nào. Đây là một kiểm tra mẫu có giới hạn, không phải là một cuộc kiểm toán bí mật toàn diện. Các quy tắc bỏ qua bao quát mười hai thành phần phổ biến liên quan đến tài khoản/dữ liệu/xuất dữ liệu. Các tệp YAML liên quan đến quy trình làm việc, vấn đề và Compose cùng với tập lệnh tác vụ Windows đã được phân tích cú pháp thành công. Các liên kết tài liệu cục bộ đều hoạt động bình thường.

Tất cả bảy phát hiện từ đợt rà soát ngày 27 tháng 10 đều đã được giải quyết. Việc thực thi quy trình làm việc trên GitHub, môi trường chạy trên Linux/macOS/Docker, Telegram thực tế, khả năng tương tác với proxy bên ngoài/TSA cùng việc đánh giá khả năng chịu tải liên tục vẫn nằm ngoài phạm vi của đợt chạy thử nghiệm cục bộ này. Không có hoạt động công bố kho lưu trữ, đăng ký dịch vụ hay thu thập tài khoản thực nào được thực hiện.

### Cập nhật tài liệu tiếng Anh

Tài liệu README, tài liệu tham khảo về tài khoản/phiên làm việc, quy trình thu thập dữ liệu và hướng dẫn đi kèm hiện nay đã mô tả các đầu vào được hỗ trợ, cách thức hoạt động của không gian làm việc, chính sách sự kiện và các định dạng xuất dữ liệu bằng tiếng Anh. Ba ảnh chụp màn hình công khai đã được cập nhật bằng dữ liệu tổng hợp. Tại thời điểm đó, bộ tài liệu nguồn mở bao gồm 88 tệp, trong đó có hai hướng dẫn mới. Tất cả 131 liên kết cục bộ trong 23 tài liệu Markdown đều hoạt động bình thường.

Sau khi chỉnh sửa giao diện và hướng dẫn, quá trình kiểm thử chấp nhận trên Chromium một lần nữa đã vượt qua toàn bộ 45 tình huống thử nghiệm, không ghi nhận bất kỳ lỗi JavaScript nào trên trang hay yêu cầu bên ngoài. Bộ kiểm thử Python đầy đủ đã không được chạy lại cho bản cập nhật tài liệu và bản trình bày lần này; kết quả 94 lần vượt qua nêu trên thuộc về đợt chạy sửa lỗi mã nguồn trước đó.

Bản nâng cấp đã được cài đặt vào một mục tiêu mới, được cách ly hoàn toàn. Các thành phần bảng điều khiển và hướng dẫn của nó đã hoạt động thành công, các yêu cầu truy cập API không được xác thực đã bị từ chối, và cả việc xuất dữ liệu trực tiếp lẫn theo luồng đều đã vượt qua quá trình xác minh độc lập đối với 32 sự kiện mô phỏng.

### Cập nhật về cài đặt và triển khai

Các kiểm tra tập trung vào trình cài đặt, đóng gói và kiểm tra sẵn sàng đã vượt qua **14 bài kiểm tra**, với một trường hợp bỏ qua do không thể tạo liên kết tượng trưng. Các kiểm tra trình bao bọc gốc bao gồm các đường dẫn có khoảng trắng, chuyển tiếp đối số, chế độ thiết lập/trình diễn và truyền kết quả thoát không bằng 0. Các kiểm tra Git Bash thực hiện trình trợ giúp shell Docker với một daemon mô phỏng, bao gồm trường hợp thiếu Docker, thiếu Compose, chờ trạng thái hoạt động thất bại và khởi động thành công qua cổng thay thế. Các kiểm tra mô phỏng này không xác định tính tương thích của môi trường chạy Docker.

Một bản sao nguồn mở hoàn chỉnh đã được cài đặt vào một thư mục Windows mới có đường dẫn chứa khoảng trắng. `scripts\Setup.cmd` đã tạo một môi trường mới và cài đặt môi trường chạy được ghim; `Start.cmd --check --json` báo cáo đã sẵn sàng mà không tạo thư mục dữ liệu đích của nó. `pip check` đã vượt qua kiểm tra. Gói phần mềm được xây dựng lại cũng đã vượt qua kiểm tra gói đã cài đặt, bao gồm cả việc xuất 32 sự kiện theo hình thức trực tiếp và qua luồng.

Cú pháp Shell và năm tệp YAML liên quan đến quy trình làm việc/Compose đã được phân tích cú pháp. Các cấu hình Compose cho mã nguồn và hình ảnh đều thống nhất về các thiết lập lưu trữ và thời gian chạy. Tại giai đoạn đó, tất cả 139 liên kết cục bộ trong 23 tài liệu Markdown đã được giải quyết. Bộ sưu tập mã nguồn công khai bao gồm 99 tệp.

Các định nghĩa CI hiện áp dụng cấu hình gốc mới trên Windows/Linux/macOS, kiểm tra tình trạng hoạt động của Compose, kiểm soát truy cập và tính bền vững khi tái tạo container, cũng như cấu hình Caddy. Quy trình phát hành sẽ chỉ cho phép xuất bản sau khi vượt qua các kiểm tra này và bổ sung thêm một bài kiểm tra sơ bộ trên nền tảng ARM64 mô phỏng. Docker không khả dụng trên máy chủ này: việc thực thi Compose/Caddy thực tế, việc cấp chứng chỉ, thực thi ARM64, cũng như quy trình làm việc từ xa/việc xuất bản gói phần mềm vẫn chưa được xác nhận tại môi trường cục bộ. Mã ứng dụng/giao diện người dùng không thay đổi sau bản cập nhật này; các kết quả trước đó trên Python và trình duyệt chưa được chạy lại.

## Phiên bản 0.5.0

Bộ kiểm tra thời gian chạy được ghim đầy đủ đã hoàn tất: **81 bài kiểm tra đạt, 1 bài bỏ qua**, trong 22,00 giây, kèm theo cảnh báo Starlette hiện có. Việc kiểm tra quyền truy cập POSIX bị bỏ qua trên hệ điều hành Windows. Các bài kiểm tra trình xử lý mới gửi tin nhắn, các thao tác chỉnh sửa, xóa có phạm vi/không có phạm vi, phản hồi, cập nhật người tham gia và tin nhắn dịch vụ thành viên thông qua các chính sách khác nhau. Các danh mục bị vô hiệu hóa sẽ không tạo ra bất kỳ quan sát trực tiếp tương ứng nào; chẩn đoán phạm vi và các ảnh chụp nhanh rõ ràng vẫn có sẵn. Các bài kiểm tra xác minh chính sách được duy trì, sự tách biệt không gian làm việc, các bản ghi kiểm toán trước/sau được ký điện tử, hành vi chính sách không thay đổi, xác thực nghiêm ngặt và việc đưa vào biên nhận quy trình tiếp theo.

Các bài kiểm tra mục demo xác nhận rằng khả năng của nó khác biệt so với mã thông báo bảng điều khiển đã được cấu hình, không thể ủy quyền cho không gian làm việc trực tiếp, không thể thay đổi cài đặt thu thập dữ liệu, và không được cấp hoặc chấp nhận đối với các yêu cầu từ xa, chuyển tiếp, giữa các nguồn gốc hoặc có máy chủ không hợp lệ. Việc mở bản demo đã lưu trữ mà không có cờ demo rõ ràng sẽ không kích hoạt tính năng nhập tự động.

Quá trình kiểm tra tương thích với Chromium đã vượt qua **39 kịch bản**, bao gồm việc truy cập bản demo cục bộ mà không cần nhập mã thông báo, các cài đặt sẵn cho chức năng giám sát, quá trình chuyển đổi từ lựa chọn nguồn sang chính sách, tính độc lập theo từng tài khoản cũng như các kiểm tra về bố cục màn hình máy tính để bàn/320/390 pixel và độ tương phản văn bản. Không có lỗi JavaScript nào trên trang. Các yêu cầu được AdGuard chèn vào từ máy chủ vẫn được ghi lại trong biên nhận. Bộ kiểm tra HTTP tải xuống đã ghi nhận việc thiết lập lại kết nối sau khi máy khách đóng kết nối của mình; các khẳng định vẫn đạt yêu cầu. Đây không phải là kết quả từ dịch vụ trực tiếp.

Trình khởi chạy tiêu chuẩn đã nâng cấp môi trường cách ly lên phiên bản 0.5.0; phiên bản nguồn và phiên bản đã cài đặt trùng khớp với nhau và kiểm tra pip đã thành công. Các kiểm tra về mã hóa kho bí mật hiện có, từ chối khóa sai/thiếu cũng như kiểm tra giả mạo chữ ký/tệp đính kèm đã vượt qua toàn bộ bộ kiểm tra. Không có tuyên bố nào về việc áp dụng mã hóa mới đối với nội dung tin nhắn hoặc tệp đính kèm.

Bản demo cục bộ được khởi động lại để cung cấp giao diện người dùng (UI) đã được cập nhật. Các bản ghi tổng hợp hiện có vẫn được giữ nguyên; việc dừng quá trình chạy nền của bản demo cũ sẽ tạo ra một ranh giới ngoại tuyến khi khởi động lại lần tiếp theo. Không có phiên Telegram thực tế nào được sử dụng cho các kiểm tra này.

Bảng điều khiển đang chạy tại localhost:8787 hiển thị phiên bản 0.5.0, quyền truy cập bản demo tự động, năm điều khiển giám sát và 33 sự kiện nhật ký tổng hợp được lưu giữ. Gói wheel phiên bản 0.5.0 được cài đặt riêng biệt đã cung cấp tất cả các tài nguyên của bảng điều khiển/hướng dẫn, từ chối quyền truy cập API không được xác thực, đồng thời tạo ra tệp ZIP chứa 32 sự kiện đã được xác minh, cả trực tiếp lẫn thông qua trình hỗ trợ tải xuống dạng luồng. Các phiên bản gói phần mềm đang chạy vẫn được cố định theo ghi nhận ở phiên bản 0.4.

## Phiên bản 0.4.0

Bộ kiểm tra thời gian chạy được ghim đầy đủ đã hoàn tất: **78 bài kiểm tra đạt, 1 bài bị bỏ qua**, trong 19,77 giây. Bài kiểm tra bị bỏ qua yêu cầu quyền truy cập POSIX; cảnh báo ngừng hỗ trợ từ Starlette TestClient phiên bản gốc vẫn còn tồn tại. Các bài kiểm tra mới bao gồm tải xuống theo luồng/định tuyến không gian làm việc, tiêu đề ủy quyền, từ chối ghi đè, chuyển hướng, phản hồi bị cắt ngắn, giới hạn kích thước công bố/thực tế, đọc có giới hạn, dọn dẹp, hệ thống tệp không có liên kết cứng, lỗi sẵn sàng và các chế độ khởi chạy không được phép cài đặt gói phần mềm. Các bài kiểm tra xuất dữ liệu xác nhận các tệp tạm thời tại không gian làm việc và việc dọn dẹp có chọn lọc các tệp mồ côi.

Chromium đã vượt qua tất cả 36 tình huống được liệt kê mà không gặp bất kỳ lỗi JavaScript nào trên trang. Công cụ này thực hiện các thao tác đăng nhập giả lập qua điện thoại/mã xác thực/2FA, các phiên đã chuyển đổi, hai không gian làm việc và các lộ trình/trạng thái riêng biệt, các quan sát, chữ ký, điểm kiểm tra và yêu cầu dấu thời gian, cùng với:

- Bố cục dành cho máy tính để bàn và kích thước 320/390 pixel, không bị tràn ngang, thanh điều hướng hiển thị rõ ràng, và trường đăng nhập đầu tiên nằm trong vùng hiển thị 844 pixel ban đầu.
- Độ tương phản giữa văn bản và nền đồng nhất, đáp ứng các ngưỡng văn bản theo tiêu chuẩn WCAG AA. Các thành phần điều khiển bị vô hiệu hóa, độ mờ cũng như nền hình ảnh/độ dốc màu không được tính vào; đây không phải là một cuộc kiểm tra tuân thủ WCAG toàn diện.
- Một phản hồi xuất dữ liệu thực tế tại địa phương được tạo thông qua trình chọn tệp hệ điều hành mô phỏng/có thể ghi, tiếp theo là quá trình xác minh ZIP độc lập; việc hủy bỏ sẽ không gửi yêu cầu xuất dữ liệu.
- Lỗi ghi dữ liệu sẽ khiến quá trình gửi đến đích bị hủy bỏ; cơ chế dự phòng 128 MiB sẽ từ chối phản hồi được thông báo có kích thước vượt quá giới hạn mà không phân bổ dung lượng tải phù hợp.
- Hướng dẫn tiếng Anh dành cho phiên bản máy tính để bàn và cả hai phiên bản có chiều rộng hẹp.

Hộp thoại lưu tệp trên hệ điều hành và các thao tác ghi dữ liệu thực tế lên trình duyệt với dung lượng nhiều gigabyte chưa được tự động hóa hoặc đánh giá đầy đủ. Các thử nghiệm tải xuống bằng Python sử dụng các khối dữ liệu có giới hạn và các thiết bị mô phỏng vòng lặp. Việc chấp nhận triển khai đầy đủ với ứng dụng Telegram thực tế vẫn được thực hiện riêng biệt.

Trình cài đặt tiêu chuẩn đã nâng cấp `.venv` lên phiên bản 0.4.0. Nguồn và siêu dữ liệu đã cài đặt khớp nhau; `pip check` đã vượt qua kiểm tra. `python start.py --check --json` báo cáo đã sẵn sàng trên một đường dẫn tổng hợp mới mà không tạo thư mục dữ liệu. Cảnh báo về lưu trữ khóa cục bộ vẫn hiển thị chính xác: các nhật ký/tệp đa phương tiện không được ứng dụng mã hóa.

Gói 0.4.0 đã được biên dịch và cài đặt vào một thư mục riêng biệt. Tất cả 23 tệp ứng dụng đều trùng khớp từng byte với tệp nguồn. Gói phần mềm đã cài đặt cung cấp giao diện người dùng và hướng dẫn/tài nguyên bằng tiếng Anh, từ chối quyền truy cập API không được xác thực, đồng thời xuất ra một tệp ZIP tổng hợp gồm 32 sự kiện đã vượt qua quá trình xác minh. Lệnh tải xuống theo luồng của nó cũng đã lấy được một tệp ZIP được xác minh độc lập từ ứng dụng đang chạy đã được cài đặt.

Tài liệu công khai và hướng dẫn dành cho người dùng địa phương được viết bằng tiếng Anh; các liên kết đến tài liệu địa phương đã được giải quyết. PowerShell đã phân tích cú pháp mẫu tác vụ Windows và Python đã phân tích cú pháp tệp plist trên macOS. Đây là các kiểm tra cú pháp, không phải quá trình thực thi dịch vụ. Không có tác vụ/dịch vụ nào được đăng ký. Cấu hình CI hiện đã bao gồm các kiểm tra sẵn sàng nhưng CI từ xa vẫn chưa được chạy tại đây.

Lần chạy trình duyệt phiên bản 0.4 một lần nữa ghi nhận việc chèn mã từ AdGuard trên máy chủ và lỗi OSError 10022 liên quan đến việc dọn dẹp socket asyncio trên Windows. Các kiểm tra xác nhận của trình duyệt đã vượt qua; những quan sát về môi trường này vẫn được ghi nhận thay vì được coi là hành vi cố định của ứng dụng. Các nỗ lực ban đầu trong môi trường cách ly (sandbox) đối với OpenSSL/trình duyệt/pip đã thất bại; các lần chạy đạt tiêu chuẩn thành công đã sử dụng cơ chế thực thi được phê duyệt bên ngoài môi trường cách ly.

## Phiên bản 0.3.1 tập trung vào các bản sửa lỗi để đảm bảo tính sẵn sàng

Các kiểm tra liên quan đến trình khởi chạy, bằng chứng/lưu trữ và API đã vượt qua: **31 kiểm tra đạt, 1 kiểm tra bị bỏ qua**, một cảnh báo từ Starlette ở nguồn. Kiểm tra bị bỏ qua này xác nhận quyền truy cập thư mục theo tiêu chuẩn POSIX và không thể thiết lập các quyền đó trên máy chủ Windows này. Bài kiểm tra Python phiên bản cũ mô phỏng ranh giới giữa phiên bản và lệnh import; không có trình thông dịch Python 3.10 nào được cài đặt hoặc đáp ứng yêu cầu. Bộ kiểm tra phiên bản 0.3 đã vượt qua trước đây được ghi lại dưới đây; toàn bộ bộ kiểm tra và các kịch bản trình duyệt không được chạy lại đối với những thay đổi tập trung này.

Trình khởi chạy thông thường đã nâng cấp môi trường cục bộ lên phiên bản 0.3.1; nguồn và siêu dữ liệu đã cài đặt khớp nhau, đồng thời kiểm tra pip đã thành công. Một gói wheel phiên bản 0.3.1 được cài đặt riêng biệt đã cung cấp các thành phần giao diện người dùng và tài nguyên, từ chối quyền truy cập API không được xác thực và tạo ra một tệp xuất tổng hợp gồm 32 sự kiện đã được xác minh. Tệp YAML quy trình làm việc đã được phân tích cú pháp, nhưng quá trình kiểm tra thời gian chạy container mới không được thực thi: không có môi trường thời gian chạy Docker/Podman/Linux cục bộ nào có thể sử dụng được.

Xin tham khảo [các kết quả đánh giá mức độ sẵn sàng](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) để biết các lỗ hổng còn tồn tại về khả năng sử dụng, dịch vụ trực tuyến và nền tảng. Bản vá này không hỗ trợ thêm các hệ điều hành khác.

## Phiên bản 0.3.0

Bộ kiểm thử thời gian chạy được ghim đầy đủ đã vượt qua: **61 bài kiểm thử**, với một cảnh báo ngừng hỗ trợ từ Starlette TestClient ở phiên bản nguồn. Siêu dữ liệu thời gian chạy báo cáo TgWitness 0.3.0 và python-socks 2.8.2; kiểm tra pip đã thành công. Vòng chạy kiểm tra tương thích trình duyệt đã vượt qua mà không có lỗi JavaScript nào trên trang.

Gói 0.3.0 đã được biên dịch và cài đặt vào một thư mục gói riêng biệt. Gói này đã cung cấp các thành phần giao diện và tài nguyên, từ chối yêu cầu API không được xác thực, đồng thời xuất một nhật ký tổng hợp gồm 32 sự kiện đã vượt qua quá trình xác minh độc lập. Các liên kết tài liệu cục bộ đã hoạt động bình thường. Sau khi thực hiện điều chỉnh chuẩn hóa khóa trần của MTProxy, cả chín bài kiểm tra kết nối/bảo mật đều đã được chạy lại thành công.

Các nội dung mới bao gồm:

- Tên người dùng/mật khẩu SOCKS5 và HTTP CONNECT thông qua các máy chủ thử nghiệm loopback thực tế; một máy chủ proxy đã được cấu hình nhưng không hoạt động sẽ báo lỗi thay vì chuyển hướng sang đích.
- Xác thực proxy, lựa chọn giao thức truyền tải MTProxy, từ chối các khóa bí mật TLS giả mạo, tính bền vững, cách ly không gian làm việc, từ chối các thay đổi trong quá trình quan sát, và loại trừ thông tin bí mật khỏi trạng thái API và các sự kiện đã được ký xác thực.
- Chuyển đổi chỉ đọc các lược đồ SQLite tổng hợp Telethon số 7 và 8; băm nguồn không thay đổi; từ chối các định dạng khác, các chế độ xem SQL và tệp WAL còn tồn đọng.
- Khóa chính của kho lưu trữ bên ngoài: các khóa không gian làm việc được dẫn xuất khác nhau, khả năng mở lại thành công, từ chối khi khóa sai hoặc thiếu, và không có quá trình di chuyển ngầm các kho lưu trữ cục bộ hiện có.
- Cài đặt proxy trình duyệt, xóa thông tin đăng nhập, thông báo về bảo vệ bộ nhớ, trang kết nối trên thiết bị di động, ủy quyền tệp phiên làm việc đã chuyển đổi, các lộ trình riêng biệt, cùng tất cả các tình huống thu thập/xuất dữ liệu đã được đề cập trước đây thông qua một ứng dụng Telegram giả mạo.

Trong quá trình phát triển, một thử nghiệm loopback đã chờ đợi vô thời hạn cho đến khi đối tác ngừng hoạt động; một lần chạy khác ghi nhận việc kết nối Windows bị thiết lập lại sau quá trình bắt tay. Hiện tại, bộ công cụ này đã giới hạn toàn bộ quá trình trao đổi và coi EOF/thiết lập lại sau khi hoàn tất quá trình bắt tay là việc đóng kết nối. Các điều kiện xác nhận về quá trình bắt tay/xác thực vẫn là bắt buộc. Điều này không loại trừ các nhà cung cấp proxy thực sự cũng như không ngụ ý rằng Telegram có lỗi cố hữu trong cơ chế truyền tải.

Yêu cầu quan sát từ nhà cung cấp dịch vụ AdGuard được mô tả dưới đây vẫn còn hiệu lực. Không có tài khoản Telegram thực tế, proxy SOCKS/HTTP bên ngoài, hay máy chủ MTProxy đang hoạt động nào được sử dụng. MTProxy hiện đang ở giai đoạn thử nghiệm và các tùy chọn đã chọn cùng quá trình xác thực khóa bí mật đã được kiểm tra, chứ không phải khả năng tương tác thực tế. Các lệnh chuyển đổi khóa bên ngoài và phiên mới đã được thử nghiệm chỉ với các khóa bí mật tổng hợp. Linux/macOS/Docker vẫn chưa được xác nhận ở đây.

Kết quả đo lường thông lượng phiên bản 0.2 dưới đây không được lặp lại và tuyệt đối không được trình bày như một tiêu chuẩn tham chiếu mới về khả năng xử lý nhiều tài khoản/proxy cho phiên bản 0.3.

## Phiên bản 0.2.0 cơ sở

Đã kiểm tra trên hệ điều hành Windows với Python phiên bản 3.12.10. Không có tài khoản Telegram thực nào được kết nối.

| Kiểm tra | Kết quả |
| --- | --- |
| Bộ công cụ Python | 52 bài kiểm thử đã vượt qua trong môi trường phát triển và 52 bài kiểm thử đã vượt qua với phiên bản runtime được cố định; mỗi lần chạy đều có một cảnh báo về việc ngừng hỗ trợ thành phần Starlette TestClient từ nguồn gốc. |
| Cú pháp JavaScript | Được phát triển bằng Node.js |
| Sự chấp nhận của Chromium | Đã đạt yêu cầu; không có lỗi JavaScript trên trang |
| Giao diện dành cho máy tính để bàn/thiết bị di động | Đã kiểm tra ở các kích thước 1440 × 1060 và 390 × 844; không có hiện tượng tràn nội dung theo chiều ngang |
| Nội dung tin nhắn dưới dạng HTML | Được hiển thị dưới dạng văn bản; đoạn mã được chèn vào không được thực thi |
| Quy trình sử dụng tài khoản mẫu | Thông tin đăng nhập API → số điện thoại → mã xác thực → xác thực hai yếu tố (2FA) → chọn nhóm → bắt đầu → chụp nhanh → tạm dừng → tải lại |
| Bằng chứng ngay trong trình duyệt | So sánh các phiên bản chỉnh sửa, nội dung trước khi xóa, bộ lọc, tải xuống dưới dạng ZIP, điểm kiểm tra, biên nhận quá trình có chữ ký, tải xuống yêu cầu theo RFC 3161 và liên kết điểm kiểm tra |
| Hỗ trợ nhiều tài khoản | Các nhật ký, khóa, nguồn và trạng thái thời gian thực được tách biệt; việc chuyển đổi trình duyệt sẽ không làm gián đoạn hoạt động của bộ thu thập khác; không gian làm việc sẽ tự động mở lại sau khi khởi động lại; hệ thống từ chối các tài khoản trùng lặp và việc chuyển nhượng tài khoản. |
| Các sự cố liên quan đến mật mã | Các trường đã ký đã thay đổi, các trường chưa ký đã được thêm vào, khóa sai, thành phần lưu trữ bị hỏng, phương tiện truyền thông bị thay đổi/thiếu, việc cắt ngắn được phát hiện tại điểm kiểm tra đã bị từ chối |
| Lưu trữ | Việc bổ sung đồng thời sẽ được xác minh; các thao tác cập nhật/xóa sẽ kích hoạt cơ chế từ chối; khi khởi động, hệ thống sẽ từ chối nhật ký đã bị thay đổi nếu không có dữ liệu bổ sung và sẽ giải phóng khóa của nhật ký đó |
| Độ bền của phương tiện lưu trữ | Ghi tin nhắn/tác vụ theo từng đơn vị; khôi phục sau khi khởi động lại; các mô tả phiên bản gốc được giữ nguyên; từ chối việc thay thế hàng đợi và làm hỏng tệp hiện có; FloodWait được duy trì; các sự cố nguồn được cách ly |
| Phát trực tuyến | Tiền tố ổn định được xuất ra trong khi các bản ghi mới được thêm vào; điểm kiểm tra được lưu giữ sẽ phát hiện trường hợp nhật ký bị cắt ngắn; quá trình xuất dữ liệu không tái hiện toàn bộ luồng sự kiện |
| RFC 3161 | OpenSSL 3.5.9 đọc các yêu cầu được tạo ra; chấp nhận phản hồi CA/TSA tổng hợp được tạo tại địa phương; từ chối dữ liệu bị thay đổi, nonce và CA không chính xác; môi trường CA xung quanh không ghi đè lên mức độ tin cậy được chỉ định rõ ràng |
| Cài đặt tại địa phương | Lệnh `start.py --setup-only` đã nâng cấp môi trường .venv cách ly lên phiên bản 0.2.0; nguồn và siêu dữ liệu đã cài đặt khớp nhau; kiểm tra pip đã thành công |
| Wheel | Phiên bản 0.2.0 đã được xây dựng và cài đặt riêng biệt trong thư mục test-results; cung cấp các tệp panel/assets, từ chối các yêu cầu API không được xác thực, đồng thời xuất và xác minh một kho lưu trữ tổng hợp gồm 32 sự kiện |

Các bản thử nghiệm nguồn đã sử dụng FastAPI 0.159.1, Uvicorn 0.54.0, Telethon 1.45.0, cryptography 50.0.2, pytest 9.1.1 và Playwright 1.62.0. Môi trường chạy được cố định sử dụng FastAPI 0.162.0, Starlette 1.10.0, Uvicorn 0.54.0, Telethon 1.45.0 và cryptography 50.0.2. Tệp deploy/constraints.txt ghi lại các phiên bản runtime được cố định; các tệp deploy/requirements.lock và deploy/build.lock chứa mã SHA-256 của từng tệp gói, và các máy chủ Docker cũng như máy chủ có mức độ bảo mật cao chỉ cài đặt dựa trên các mã này (pip --require-hashes). Cả hai đều không phải là bằng chứng về tính tương thích trên mọi nền tảng CI đã được cấu hình. CI từ xa vẫn chưa được chạy.

## Đo lường năng lực địa phương tổng hợp

Lệnh: `python tools/check_capacity.py --events 10000 --chats 100`

| Chỉ số | Đã quan sát |
| --- | --- |
| Nội dung đầu vào | 10.000 sự kiện tin nhắn tổng hợp từ 100 nguồn tổng hợp được lựa chọn |
| Nội dung tin nhắn | 400 ký tự; không kèm phương tiện truyền thông hoặc thông tin mạng |
| Quá trình nhập dữ liệu | 53,273 giây; 187,7 sự kiện/giây |
| Độ trễ của trình xử lý | p50 4,162 ms; p95 7,784 ms; tối đa 129,118 ms |
| Xuất dưới dạng ZIP | 19,868 giây khi bật tracemalloc |
| Phân bổ xuất Python được theo dõi ở mức cao nhất | 0,51 MiB; không hỗ trợ RSS |
| Kích thước tệp ZIP | 4.610.962 byte |
| Xác minh độc lập | Tất cả 10.000 sự kiện đã được xác minh |

Chỉ số này đo lường đường dẫn ghi lại/xuất dữ liệu cục bộ trên máy chủ Windows này. Chỉ số này không đo lường việc truyền tải qua MTProto, số lượng tài khoản đồng thời, việc giới hạn băng thông của Telegram, tệp đa phương tiện, tải công việc kéo dài, hay số lượng cuộc trò chuyện thực tế được đảm bảo. Việc đo lường này được thực hiện trước khi công cụ đóng dấu thời gian ngoại tuyến cuối cùng được triển khai, và công cụ này không làm thay đổi đường dẫn tin nhắn đã được đo lường.

## Các quan sát về môi trường

Các hạn chế của môi trường sandbox trên Windows đã chặn các thư mục tạm thời mặc định của pytest/pip cũng như tiến trình con của Playwright. Pytest đã sử dụng một thư mục tạm thời mới bên trong dự án; các tiến trình cài đặt và trình duyệt yêu cầu được phép thực thi bên ngoài môi trường sandbox.

AdGuard trên máy tính đã chèn các yêu cầu tới local.adguard.org vào trình duyệt. Bản ghi của trình duyệt vẫn lưu giữ các yêu cầu đó. Kết quả này **không** phải là bằng chứng cho thấy không có yêu cầu đi ra nào trong môi trường trình duyệt chưa được sửa đổi; bản thân mã nguồn của ứng dụng không chứa bất kỳ yêu cầu nào tới tài nguyên bên ngoài, CDN hay dịch vụ phân tích. Cài đặt AdGuard không bị thay đổi.

Lần chạy trình duyệt cuối cùng cũng ghi nhận lỗi OSError 10022 liên quan đến việc dọn dẹp socket asyncio trên Windows. Tất cả các kiểm tra xác nhận của trình duyệt đều thành công và không xảy ra lỗi JavaScript nào trên trang. Nguyên nhân của sự cố này chưa được xác định và lần chạy này không chứng minh được rằng không tồn tại các vấn đề về truyền tải từ phía máy chủ.

Thử nghiệm HTTP đầu tiên trên gói phần mềm đã cài đặt, sử dụng các yêu cầu ngắt kết nối của urllib, đã gặp phải tình trạng kết nối bị thiết lập lại, cả trong và ngoài môi trường sandbox, đồng thời xảy ra với cả hai bộ phụ thuộc. Thử nghiệm cuối cùng sử dụng kết nối HTTP/1.1 liên tục tiêu chuẩn thông qua http.client và đã vượt qua kiểm tra. Các yêu cầu từ trình duyệt cũng đã vượt qua kiểm tra. Nguồn gốc chính xác của các sự cố ngắt kết nối chưa được xác định; chúng không được xác định là một lỗi cố hữu của ứng dụng.

## Các tiêu chí còn lại

Nhật ký trực tiếp được lưu giữ này ghi nhận chính xác các hoạt động thu thập, chỉnh sửa, thông báo xóa, tệp đính kèm, việc kiểm tra lại và xử lý giới hạn tốc độ. Nó không ghi lại toàn bộ quá trình gửi tin nhắn hay một ma trận được kiểm soát về phạm vi hiển thị theo vai trò, các chủ thể phản ứng, thời gian chờ FloodWait kéo dài, việc khóa tài khoản và quá trình khôi phục sau sự cố gián đoạn mạng/quy trình. Việc phát hành mã QR-token vẫn tách biệt với quá trình xác nhận mã QR trên thiết bị di động đã hoàn tất.

Việc xây dựng/chạy Docker, cài đặt trên Linux/macOS, khả năng chịu tải cao liên tục, đánh giá bảo mật độc lập, phản hồi TSA độc lập thực sự, xác thực thu hồi/lưu trữ chứng chỉ và chứng nhận pháp y vẫn nằm ngoài phạm vi chứng nhận đã ghi nhận. Tình trạng MTProto đã lưu và tính năng bắt kịp đã được triển khai; tính năng phát lại nguyên tử bền vững vẫn chưa được thiết lập. Việc thu thập nhật ký quản trị, danh sách máy chủ phản hồi bổ sung và cơ chế thăm dò ưu tiên ngắn vẫn là các tính năng riêng biệt. Vui lòng tham khảo [bản chấp nhận trực tiếp](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) để xem ma trận chứng nhận có kiểm soát.

Các bản ghi chi tiết và ảnh chụp màn hình tại địa phương hiện được lưu trữ trong thư mục test-results/ (bị Git bỏ qua). Ảnh chụp màn hình công khai trong thư mục docs/assets/ chỉ chứa dữ liệu minh họa hư cấu.

## Chuẩn bị trang web công khai và ấn phẩm · Ngày 27 tháng 10 năm 2026

Bản trình bày `website/` và bản dựng Pages riêng biệt đã được bổ sung sau khi hoàn tất các bước kiểm tra nêu trên. Không có bất kỳ thay đổi nào được thực hiện đối với cấu hình tài khoản trực tiếp hay logic thu thập dữ liệu.

- Bộ ứng dụng hiện có đã vượt qua kiểm tra: 138 bài kiểm tra đạt, 1 bài bỏ qua do chỉ hỗ trợ POSIX và một cảnh báo về tính lỗi thời của Starlette/httpx từ phiên bản gốc. 11 bài kiểm tra xây dựng trang web mới được bổ sung đã vượt qua một cách độc lập, bao gồm cả việc từ chối đầu ra bất ngờ và từ chối đầu vào liên kết.
- Cả hai tập lệnh trình duyệt của ứng dụng đều đã vượt qua kiểm tra khi sử dụng Playwright trong môi trường project-venv và Chromium headless shell 156. Không ghi nhận bất kỳ lỗi JavaScript nào trên trang hay yêu cầu bên ngoài nào. Tất cả các kịch bản tài khoản đều sử dụng phương thức truyền tải giả và dữ liệu hư cấu.
- `tools/check_site.py` đã vượt qua các bài kiểm tra ở các độ rộng 320, 390, 768, 1024 và 1440, với đường dẫn con của URL dự án, các tab bàn phím, quyền truy cập khay nhớ tạm thành công/bị từ chối, hiệu ứng chuyển động giảm thiểu, và JavaScript bị vô hiệu hóa. Không xảy ra bất kỳ yêu cầu tài nguyên hoặc yêu cầu bên ngoài nào bị thất bại.
- `tools/build_site.py` đã tạo ra 10 tệp công khai nằm trong danh sách cho phép, với tổng dung lượng khoảng 460 KB. Các ảnh chụp màn hình trình duyệt và biên lai được lưu trong tệp `test-results/site/` (đã bị bỏ qua).
- Quá trình tạo tệp wheel đã thành công sau khi cài đặt các công cụ setuptools/wheel chỉ dành cho việc xây dựng trong môi trường dự án. Việc cài đặt nó vào một mục tiêu cách ly và chạy lệnh ``tools/check_install.py`` đã vượt qua các bước kiểm tra: tài sản tĩnh, kiểm soát truy cập, một tệp xuất tổng hợp gồm 32 sự kiện đã được ký số, cùng với quá trình tải xuống dạng luồng được xác minh độc lập.
- `pip check` đã vượt qua kiểm tra. Quá trình quét mẫu trên các ứng viên công khai được chọn từ Git không phát hiện thấy các khối khóa riêng có thể nhận diện, mã thông báo GitHub/bot/AWS, các giá trị bí mật dạng chuỗi dài hoặc các dấu hiệu xung đột hợp nhất. Điều này không chứng minh rằng mọi định dạng bí mật có thể có đều vắng mặt. Các phép kiểm tra dữ liệu thời gian chạy/phiên làm việc/khóa đã bị Git bỏ qua.
- Quá trình xác thực GitHub CLI không hợp lệ; không có máy chủ từ xa nào được cấu hình và không có bản cam kết ban đầu nào tồn tại. Không có thao tác đẩy (push), quy trình làm việc được lưu trữ, triển khai Pages hay phát hành nào được thực hiện. Việc kiểm tra Docker và khả năng hoạt động thực tế của Telegram/nền tảng vẫn nằm ngoài phạm vi kiểm tra này.

Trên máy chủ này, quá trình khóa tải xuống Playwright đã thất bại trên hệ thống tệp làm việc E:. Việc cài đặt Chromium dưới `%LOCALAPPDATA%/tgwitness-playwright` và sử dụng chính `PLAYWRIGHT_BROWSERS_PATH` đó để thực hiện các kiểm tra đã thành công. Đây là một giải pháp tạm thời về môi trường, chứ không phải là sự thay đổi đối với các phụ thuộc thời gian chạy của ứng dụng.

## Tài liệu tương tác và siêu dữ liệu trang web · Ngày 29 tháng 10 năm 2026

Trang web công khai bao gồm 12 trang HTML bằng tiếng Anh: một trang chủ, một chỉ mục hướng dẫn và mười hướng dẫn. Tài liệu này chứa 28 tệp trình bày được liệt kê rõ ràng, với dung lượng khoảng 1,85 MB và không có dữ liệu thu thập. Trang web công khai sử dụng tiếng Anh; các bản dịch ứng dụng và hướng dẫn kho lưu trữ đã được dịch là các phần riêng biệt.

- Các bài kiểm tra về trang web, nguồn xuất bản và ranh giới phát hành: **18 bài đạt, 2 bài bị bỏ qua**. Các bài kiểm tra bị bỏ qua liên quan đến việc tạo liên kết tượng trưng (symlink) trên hệ thống tệp tin Windows này. Các bài kiểm tra xác minh siêu dữ liệu trang duy nhất, các trang công khai chỉ bằng tiếng Anh, URL chuẩn, tất cả các mục trong sơ đồ trang web , tài nguyên/liên kết nội bộ, hệ thống điều hướng có cấu trúc và việc loại trừ các tệp tin riêng tư.
- Cả `tools/check_site.py` và `tools/check_docs_site.py` đều vượt qua bài kiểm tra trên Chromium ở các độ phân giải 320, 390, 768, 1024 và 1440 pixel dưới đường dẫn con của URL dự án. Các bước kiểm tra trong hướng dẫn bao quát toàn bộ 11 trang tài liệu, chức năng tìm kiếm và điều hướng bằng bàn phím, hoạt động của khay nhớ tạm (thành công/thất bại) cũng như khả năng hiển thị nội dung mà không cần JavaScript.
- Năm ví dụ tương tác đã vượt qua kiểm tra: phát lại/di chuyển từng bước/tạm dừng/đặt lại tin nhắn với chuyển động được giảm thiểu và tính năng tạm dừng ngoài màn hình; chuỗi băm gốc/đã sửa đổi/được tái tạo/bị cắt ngắn; các quyết định chấp nhận/khôi phục/phân nhánh/không phản hồi của nhân chứng; cùng các tình huống gửi tin nhắn hoàn tất/bị trì hoãn/bị thiếu; và bản đồ điều tra liên kết các quan sát giả định xuyên cuộc trò chuyện theo ID người gửi, đích đến và băm tệp đính kèm . Các cơ chế kiểm soát điều tra đã vượt qua các bài kiểm tra điều hướng bằng bàn phím và kiểm tra dự phòng khi không có JavaScript . Kết quả SHA-256 trên trình duyệt đã được so sánh độc lập với `hashlib` của Python và định dạng JSON chuẩn. Ví dụ về hàm băm này cũng vẫn giữ được bản dự phòng dễ đọc khi Web Crypto không khả dụng.
- Tỷ lệ hiển thị và các điểm đánh dấu trên biểu đồ đã được điều chỉnh cho phù hợp với bảng dữ liệu dễ tiếp cận. Các nhãn trục trên phiên bản di động đã được phóng to sau khi rà soát trực quan. Mỗi ví dụ đều được ghi chú rõ là ví dụ minh họa hoặc tổng hợp, và không có ví dụ trình duyệt nào kết nối với Telegram.
- Không có yêu cầu bên ngoài, yêu cầu HTTP thất bại hoặc lỗi JavaScript nào được ghi lại. Các ảnh chụp màn hình trên máy tính để bàn/thiết bị di động và biên lai được phân loại dưới các mục `test-results/site/` và `test-results/docs-site/`. Chỉ mục tài liệu, các ví dụ về tin nhắn/băm, giao diện Witness, biểu đồ gửi tin và bản đồ điều tra đã được kiểm tra ở các kích thước dành cho máy tính để bàn và thiết bị di động.
- Quá trình quét tài liệu đã được thông qua đối với 282 tệp nguồn công khai và 1.426 liên kết tài liệu cục bộ. Ruff đã thông qua các công cụ và bài kiểm tra Python đã được sửa đổi trên trang web.
- `docs/HOW-IT-WORKS.md` cung cấp một công cụ hỗ trợ GitHub Markdown kèm theo các sơ đồ và công thức Mermaid. `docs/INVESTIGATION.md` bao quát phạm vi toàn bộ tài khoản, việc thu thập lịch sử từng cuộc trò chuyện, hồ sơ cá nhân, các tham chiếu liên cuộc trò chuyện, dòng thời gian và quy trình chuyển giao vụ việc đã được xác minh. Các bước thực hiện và giới hạn của công cụ này đã được đối chiếu với phạm vi hiện tại, quy trình thu thập, hồ sơ, xuất dữ liệu, công cụ xác minh và mã nguồn của bảng điều khiển. Việc hiển thị trên GitHub do bên thứ ba lưu trữ chưa được kiểm tra.

Đây là một cuộc kiểm tra trang web/tài liệu tại địa phương. Quá trình này không bổ sung tính năng xác thực Telegram trực tiếp, cũng như không thiết lập việc triển khai Pages được lưu trữ, xác nhận thành công của CI từ xa hay việc lập chỉ mục trên công cụ tìm kiếm. Vui lòng tham khảo [quy trình xuất bản](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md) và [các ghi chú về siêu dữ liệu trang web](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/SEO.md).
