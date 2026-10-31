# Quy trình làm việc và hoạt động

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/operations/

Hoạt động hàng ngày của bảng điều khiển: các chế độ, danh mục giám sát, thông số, thông báo, xuất dữ liệu, sao lưu và dung lượng.

Đối với lần kết nối đầu tiên, vui lòng sử dụng [các định dạng tài khoản và phiên làm việc](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/). Để tìm hiểu về các phiên bản đã lưu, chính sách sự kiện và các khoảng trống, xin tham khảo phần [giải thích về cơ chế thu thập dữ liệu](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/). Hướng dẫn này bao quát các hoạt động hàng ngày và quy trình khôi phục dữ liệu.

## Quy trình làm việc của người vận hành

Sơ đồ quy trình · Chọn phương thức lưu trữ và bảo vệ khóa → Mở bảng điều khiển bằng mã thông báo của nó; Mở bảng điều khiển bằng mã thông báo của nó → Chọn không gian làm việc; Chọn không gian làm việc → Cấu hình đường dẫn trực tiếp hoặc qua proxy; Cấu hình đường dẫn trực tiếp hoặc qua proxy → Nhập số điện thoại hoặc chọn tệp / mã QR; Nhập số điện thoại hoặc chọn tệp / mã QR → Xác minh danh tính tài khoản và chọn các nhóm có thể truy cập; Xác minh danh tính tài khoản và chọn các nhóm có thể truy cập → Lưu các chính sách về sự kiện và tệp đính kèm, sau đó bắt đầu quá trình giám sát; Lưu các chính sách về sự kiện và tệp đính kèm, sau đó bắt đầu quá trình giám sát → Theo dõi lỗi, quyền truy cập, hàng đợi và dung lượng đĩa; Theo dõi lỗi, quyền truy cập, hàng đợi và dung lượng đĩa → Giữ lại các điểm kiểm tra độc lập; Giữ lại các điểm kiểm tra độc lập → Xuất và xác minh tài liệu · Chọn phương thức lưutrữ và bảo vệ khóa · Mở bảng điều khiểnbằng mã thông báo củanó · Chọn không gian làmviệc · Cấu hình đường dẫntrực tiếp hoặc quaproxy · Nhập số điện thoạihoặc chọn tệp / mã QR · Xác minh danh tính tàikhoản và chọn các nhómcó thể truy cập · Lưu các chính sách vềsự kiện và tệp đínhkèm, sau đó bắt đầuquá trình giám sát · Theo dõi lỗi, quyềntruy cập, hàng đợi vàdung lượng đĩa · Giữ lại các điểm kiểmtra độc lập · Xuất và xác minh tàiliệu

**Sơ đồ dưới dạng văn bản**

1. Chọn phương thức lưu trữ và bảo vệ khóa → Mở bảng điều khiển bằng mã thông báo của nó
2. Mở bảng điều khiển bằng mã thông báo của nó → Chọn không gian làm việc
3. Chọn không gian làm việc → Cấu hình đường dẫn trực tiếp hoặc qua proxy
4. Cấu hình đường dẫn trực tiếp hoặc qua proxy → Nhập số điện thoại hoặc chọn tệp / mã QR
5. Nhập số điện thoại hoặc chọn tệp / mã QR → Xác minh danh tính tài khoản và chọn các nhóm có thể truy cập
6. Xác minh danh tính tài khoản và chọn các nhóm có thể truy cập → Lưu các chính sách về sự kiện và tệp đính kèm, sau đó bắt đầu quá trình giám sát
7. Lưu các chính sách về sự kiện và tệp đính kèm, sau đó bắt đầu quá trình giám sát → Theo dõi lỗi, quyền truy cập, hàng đợi và dung lượng đĩa
8. Theo dõi lỗi, quyền truy cập, hàng đợi và dung lượng đĩa → Giữ lại các điểm kiểm tra độc lập
9. Giữ lại các điểm kiểm tra độc lập → Xuất và xác minh tài liệu

Quyền truy cập, kết nối truyền tải, quyền tham gia nhóm và tính đầy đủ của việc gửi tin nhắn là các thuộc tính khác nhau. Trạng thái kết nối màu xanh lá cây không có nghĩa là tất cả các sự kiện đã được ghi lại.

## Chia sẻ công việc mà không cần chia sẻ khóa chính

**Tính năng Truy cập** Mở cho phép cấp mã thông báo riêng cho người đánh giá hoặc nhà phân tích. Quý vị có thể chọn các tài khoản và cuộc trò chuyện mà họ được phép truy cập, sau đó cấp quyền xem, xuất dữ liệu hoặc thực hiện các thao tác vận hành. Người vận hành thực hiện việc bắt đầu/dừng thu thập dữ liệu cần có quyền truy cập toàn bộ không gian làm việc; trong khi người đánh giá có thể bị giới hạn ở một cuộc trò chuyện duy nhất. Các giới hạn phiên, thời hạn hiệu lực và quy tắc IP là riêng biệt so với việc ủy quyền tài khoản Telegram. Vui lòng tham khảo [phần quyền truy cập và quyền hạn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/).

Sử dụng **tính năng “Open sessions”** để ngắt kết nối hoặc thu hồi quyền truy cập nhằm chấm dứt tất cả các phiên làm việc của người dùng đó. Bảng điều khiển quản trị tổng hợp hoạt động của các quy trình hiện tại trên các không gian làm việc. Việc đóng phiên làm việc sẽ không ảnh hưởng đến quá trình thu thập dữ liệu.

## Các chế độ hoạt động

| Chế độ | Hành động | Hành vi |
| --- | --- | --- |
| Bản demo | scripts\Demo.cmd hoặc `--demo` | Dữ liệu tổng hợp; tính năng kết nối với tài khoản thực đã bị vô hiệu hóa |
| Quan sát | Bắt đầu quan sát | Ghi lại các bản cập nhật đã được gửi cho các nguồn được chọn |
| Bản chụp lịch sử | Nguồn → ảnh chụp lịch sử | Lưu trữ tối đa 500 tin nhắn hiện tại; không tái tạo lại tất cả các thay đổi trong quá khứ |
| Tạm dừng | Tạm dừng quan sát | Tạm dừng thu thập dữ liệu trong khi vẫn lưu giữ dữ liệu và các tác vụ đang chờ xử lý |
| Xem xét/Chuyển giao | Xuất dữ liệu | ZIP, JSONL/CSV/HTML, điểm kiểm tra, biên nhận quá trình và yêu cầu dấu thời gian |
| Nhiều tài khoản | Các không gian làm việc hoặc nút **+** ở trên cùng | Có thể tạo bất kỳ số lượng không gian làm việc riêng biệt nào trong cùng một quy trình |

Quyền truy cập bản demo tại địa phương sẽ tự động mở mà không cần nhập mã thông báo thủ công. Tính năng này sử dụng khả năng tồn tại trong suốt quá trình xử lý, chỉ có hiệu lực đối với quyền truy cập vòng lặp trực tiếp vào một bản demo tổng hợp được cách ly; mã thông báo của bảng điều khiển chính không được tiết lộ. Các không gian làm việc thực tế cũng như quyền truy cập bản demo từ xa hoặc qua máy chủ proxy vẫn duy trì xác thực bằng mã thông báo. Việc truy cập bản demo không cấp bất kỳ quyền ủy quyền nào trên Telegram.

## Các danh mục giám sát

![Cài đặt giám sát theo từng tài khoản với dữ liệu nguồn tổng hợp](https://phishdestroy.github.io/TgWitness/assets/sources.png)

Trong **phần Nguồn → Cài đặt ghi lại → Chọn các thay đổi cần lưu giữ**, quý vị có thể chọn riêng biệt các tin nhắn mới, nội dung chỉnh sửa, thông báo xóa, cập nhật phản ứng và các sự kiện liên quan đến thành viên. Cài đặt mặc định sẽ lưu giữ tất cả các danh mục. Tùy chọn **“Tin nhắn, chỉnh sửa & xóa”** sẽ giữ nguyên bối cảnh ban đầu đồng thời vô hiệu hóa các cập nhật riêng biệt về phản ứng và thành viên. Tùy chọn **“Tất cả hoạt động hiển thị”** sẽ khôi phục cả năm loại. Các cài đặt sẵn sẽ thay đổi định dạng; nhấn **“Lưu cài đặt giám sát”** để áp dụng.

Chính sách đã lưu sẽ áp dụng cho tất cả các nguồn được chọn trong không gian làm việc đó. Các không gian làm việc khác vẫn giữ nguyên cài đặt riêng của mình. Mỗi thay đổi thực tế đều được ghi lại kèm theo các giá trị trước và sau đã được ký xác thực; chính sách hiện tại cũng được bao gồm trong biên nhận quá trình và bản ghi bắt đầu quan sát. Việc vô hiệu hóa một danh mục sẽ không xóa các quan sát trước đó. Việc kích hoạt lại sẽ không khôi phục các thay đổi đã bỏ lỡ. Trong phiên bản này, không có tính năng ghi đè danh mục theo từng nhóm.

Vui lòng duy trì tính năng ghi lại tin nhắn mới khi nội dung trước đó vẫn còn quan trọng: thông báo xóa tin nhắn không thể khôi phục lại văn bản chưa từng được ghi lại. Các bản ghi hoạt động/phạm vi phủ sóng cùng các sự kiện dịch vụ nhóm khác luôn được lưu giữ. Các bản chụp lịch sử rõ ràng là riêng biệt so với việc lựa chọn danh mục thời gian thực và có thể bao gồm các tin nhắn dịch vụ. Các tùy chọn này không che giấu siêu dữ liệu về phản ứng/thành viên được nhúng trong một đối tượng Telegram đã được ghi lại.

Một bản chụp lịch sử có thể xếp các tệp đính kèm vào hàng đợi khi đang tạm dừng. Hãy bắt đầu quá trình quan sát để xử lý chúng. Việc được xếp vào hàng đợi không có nghĩa là đã được tải xuống. Một tệp gốc không khả dụng sẽ không bị thay thế bằng phiên bản đã chỉnh sửa mới hơn; các kết quả sẽ được ghi lại riêng biệt.

**Nút “Lock”** sẽ xóa quyền truy cập trình duyệt và các trường bí mật nhưng vẫn duy trì quá trình thu thập dữ liệu. Việc đóng tab cũng không làm dừng quá trình thu thập dữ liệu. Việc dừng tiến trình Python hoặc dịch vụ sẽ ngừng quá trình thu thập dữ liệu bất kể trạng thái của trình duyệt.

Việc xóa một không gian làm việc bổ sung sẽ dừng trình thu thập dữ liệu của không gian đó và xóa dữ liệu cục bộ của nó. Nếu một tệp bị khóa hoặc lỗi hệ thống tệp làm gián đoạn quá trình xóa, bảng điều khiển sẽ báo cáo sự cố và giữ không gian làm việc đó trong danh sách là không khả dụng (`DeletionPending`). Vui lòng đóng các chương trình đang giữ các tệp của không gian làm việc đó và thử lại **lệnh Xóa**. Việc khởi động lại TgWitness sẽ khiến không gian làm việc đó vẫn ở trạng thái dừng và không khôi phục lại nhật ký hoặc các khóa đã bị xóa một phần. Việc xóa thành công chỉ được ghi lại sau khi thư mục đã được xóa; các bản sao được xuất hoặc sao lưu riêng biệt vẫn tuân theo chính sách lưu trữ riêng của chúng.

## Thông báo

Mở **Nguồn → Thông báo → Cảnh báo và bản tóm tắt hàng ngày**. TgWitness sử dụng Apprise để gửi cảnh báo đến Matrix, Telegram, Discord, Slack, ntfy, email và các dịch vụ được hỗ trợ khác. Quý vị có thể thêm nhiều điểm đến vào một không gian làm việc.

1. Vui lòng nhập một URL đích Apprise trên mỗi dòng. Hãy sử dụng danh mục dịch vụ ( [danh mục dịch vụ và các định dạng URL](https://appriseit.com/services/)) phù hợp với dịch vụ của quý vị.
2. Vui lòng bật tùy chọn **“Gửi thông báo”**, sau đó chọn các cảnh báo sự cố, thay đổi trong các cuộc trò chuyện được theo dõi và bản tóm tắt hàng ngày. Giờ trong bản tóm tắt sử dụng múi giờ của máy chủ.
3. Vui lòng bật tùy chọn **“Bao gồm các đoạn trích ngắn”** nếu quý vị muốn văn bản được lưu trữ từ các tin nhắn đã bị xóa và đã chỉnh sửa xuất hiện trong các thông báo.
4. Nhấn vào **“Lưu thông báo”**, sau đó nhấn **“Gửi thử nghiệm”** để kiểm tra việc gửi đi.

Đối với máy chủ nhận của riêng quý vị, vui lòng sử dụng [webhook JSON](https://appriseit.com/services/json/) của Apprise. Ví dụ: `jsons://notify.example.org/tgwitness` gửi JSON qua HTTPS đến điểm cuối đó. Đây là một ví dụ hư cấu; quý vị hãy thay thế bằng điểm đến của riêng mình.

Các đích đến và cài đặt thuộc về không gian làm việc đã chọn. Thông báo thay đổi bao gồm các nguồn được theo dõi, bao gồm cả các cuộc trò chuyện mới được thêm vào. Biểu tượng chuông trên thanh trên cùng cũng liệt kê các sự cố gần đây và những thay đổi trong cuộc trò chuyện.

Trong bản demo, các điều khiển thông báo hiển thị nhưng chức năng gửi đã bị vô hiệu hóa. Vui lòng cấu hình việc gửi thông báo trong một không gian làm việc thực tế. Các thông báo sẽ sử dụng đường dẫn Direct, SOCKS5 hoặc HTTP của không gian làm việc đó; MTProxy không thể truyền tải chúng. Các điểm đến không phải HTTP như SMTP yêu cầu một đường dẫn trực tiếp.

## Bố cục bảng điều khiển

![Kết nối không gian làm việc bằng dữ liệu tổng hợp](https://phishdestroy.github.io/TgWitness/assets/connection.png)

**Tạp chí này** hiển thị các quan sát, chức năng tìm kiếm và bộ lọc. Khi có thao tác chỉnh sửa, các phiên bản đã được ghi lại sẽ được mở ra; khi có thao tác xóa, nội dung trước đó (nếu có) sẽ được hiển thị. Nguồn gốc không xác định vẫn được nêu rõ ràng. Số liệu thống kê có sẵn trong **phần Tổng quan**; chi tiết về quá trình thu thập được lưu giữ trong hướng dẫn cục bộ.

Mở một tin nhắn đã chỉnh sửa để so sánh các phiên bản của nó bằng **Thay đổi trong văn bản** hoặc **Đặt cạnh nhau**; **Dữ liệu thô** hiển thị các trường đã lưu. Các thay đổi đối với liên kết ẩn và nút bot xuất hiện riêng biệt. Mở bản xem trước tệp đính kèm để kiểm tra hình ảnh, âm thanh hoặc video đã lưu; nút tải xuống giúp giữ cho bản gốc đã lưu trữ luôn sẵn có.

**Live** cập nhật nhật ký và các cuộc trò chuyện ngay khi có bản ghi mới. Tạm dừng tính năng này khi đang xem xét, hoặc sử dụng nút sự kiện mới khi đã sẵn sàng; quá trình thu thập vẫn tiếp tục chạy. **Ctrl/Cmd+K** tìm các thao tác trên bảng điều khiển và tìm kiếm trong nhật ký.

**Phần “Nguồn”** bao gồm phạm vi quan sát (các cuộc trò chuyện được chọn, một thư mục Telegram hoặc toàn bộ tài khoản), các cuộc trò chuyện có thể truy cập thuộc mọi loại, các nguồn được chọn kèm dấu sao ưu tiên, cài đặt về tệp đính kèm và kiểm tra lại, cùng các bản chụp lịch sử. Các nguồn riêng tư được chọn theo hộp thoại/ID mà không cần liên kết công khai. Trạng thái truy cập mô tả lần kiểm tra gần đây nhất, chứ không phải quyền truy cập vĩnh viễn.

Lọc các nguồn, đánh dấu vào ô chọn của chúng, sau đó bật, tạm dừng hoặc đánh dấu ưu tiên cho chúng cùng lúc. Trong danh sách cuộc trò chuyện khả dụng, **Thêm mục đã chọn** sẽ sử dụng lựa chọn của bạn; **Thêm tất cả kết quả phù hợp** sẽ sử dụng bộ lọc tìm kiếm và loại hiện tại.

**Phần “Trò chuyện” → “Người dùng”** liệt kê tất cả những người có tin nhắn được lưu trữ; khi tính năng hồ sơ người dùng được bật cho cuộc trò chuyện đó, chỉ cần nhấp chuột là hồ sơ của người đó sẽ mở ra kèm theo các liên kết đến các bản ghi trong sổ chứng cứ.

**Witness** tạo ra các mã chứng thực chỉ đọc, hiển thị thời điểm lần cuối mỗi mã chứng thực được kiểm tra và cung cấp các lệnh cùng tùy chọn để khởi chạy một [mã chứng thực độc lập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/).

**Phần “Tham số”** chứa mọi giới hạn và tốc độ của không gian làm việc mà không được đề cập trên các trang khác: số lượng cuộc trò chuyện được đọc, tần suất danh sách trò chuyện được đọc lại, khoảng thời gian giữa các lần kiểm tra trạng thái và điểm kiểm tra , bộ đệm khởi động, cách các lần kiểm tra lại phân bổ yêu cầu của mình (thời gian trễ ban đầu, số cuộc trò chuyện trên mỗi lần quét, thời gian tạm dừng giữa các cuộc trò chuyện, số tin nhắn được khôi phục và yêu cầu lại), dung lượng đĩa dự trữ, thời gian chờ và số lần thử lại khi tải xuống, các tiêu chí tìm kiếm trong hồ sơ người dùng (bao gồm cả biểu thức chính quy do quý vị tự định nghĩa), kích thước và tần suất thông báo, giới hạn chụp nhanh, ZIP và tải xuống qua trình duyệt, cũng như thời gian chờ và số lần thử lại của ứng dụng Telegram. Mỗi trường hiển thị phạm vi và giá trị mặc định; các trường đã thay đổi được đánh dấu và có thể khôi phục từng trường một hoặc tất cả cùng lúc. Mọi thay đổi đều được ghi lại dưới dạng mã `parameters.changed` kèm theo các giá trị trước và sau khi thay đổi, đồng thời các bản ghi bắt đầu quan sát sẽ nêu rõ các giá trị hiện đang có hiệu lực. Các giá trị có hiệu lực kể từ lần sử dụng tiếp theo; thời gian chờ và số lần thử lại của ứng dụng khách sẽ áp dụng từ lần kết nối tiếp theo. Khoảng thời gian kiểm tra lại, loại và kích thước tệp đính kèm, bằng chứng cũng như khoảng thời gian sao lưu ngoài trang web vẫn được duy trì trên các trang riêng biệt và có thể nhận bất kỳ giá trị nào trong phạm vi cho phép, không chỉ giới hạn ở các thiết lập mặc định.

Biểu tượng chuông ở thanh trên cùng liệt kê các sự cố và thay đổi gần đây trong các cuộc trò chuyện được theo dõi; các tin nhắn chưa đọc sẽ được tính cho đến khi được đánh dấu là đã đọc. Các thay đổi được nhóm theo từng cuộc trò chuyện và theo giờ (“12 tin nhắn đã bị xóa, 1 tin nhắn đã được chỉnh sửa, 0 tin nhắn không tìm thấy”), và các sự cố như đăng xuất hoặc ổ đĩa đầy vẫn được giữ lại trong danh sách bất kể các cuộc trò chuyện có bận rộn đến mức nào.

**Quá trình đăng ký** bắt đầu từ trường số điện thoại. **Tiếp tục** sẽ dẫn trực tiếp đến bước nhập mã, chỉ yêu cầu thông tin đăng nhập API khi chưa có. Nhập qua mã QR và tệp tin là các tab thay thế. Thông tin đăng nhập API đã lưu chỉ được tái sử dụng trong chính không gian làm việc của chúng. Màn hình đăng nhập không có thanh bên, thống kê hay các phần hướng dẫn thiết lập. Biểu tượng **Cài** đặt mở ra các tùy chọn điều khiển API, proxy, bộ nhớ và tài khoản bổ sung. Các cài đặt mới bắt đầu từ đây; các tài khoản đã kết nối nhưng chưa chọn nguồn nào sẽ bắt đầu từ **mục Chọn cuộc trò chuyện**. Việc thay đổi lộ trình yêu cầu tạm dừng quá trình quan sát và sẽ hủy bỏ quá trình đăng nhập chưa hoàn tất. Một sổ nhật ký hiện có không thể được liên kết lại một cách im lặng với một tài khoản Telegram khác.

**Tính năng xuất dữ liệu** sẽ kiểm tra tính toàn vẹn của nhật ký và tạo ra các tệp có thể di chuyển được. Mã định danh không gian làm việc (workspace ID) của công cụ có thể được truyền vào lệnh CLI tải xuống. Mỗi lần xuất dữ liệu sẽ gắn một tiền tố nhật ký đầy đủ; các sự kiện xảy ra sau đó sẽ được đưa vào lần xuất tiếp theo. Các bộ lọc tìm kiếm không làm thay đổi phạm vi của gói dữ liệu. Thông tin chi tiết về việc ký xác thực và phạm vi bao phủ được trình bày trong phần **“Xác minh & giới hạn**”.

Bảng điều khiển hiển thị trạng thái bộ thu thập, các tệp phương tiện đang xếp hàng/bị lỗi, tệp phương tiện đang chờ xử lý lâu nhất, dung lượng đĩa trống, các yêu cầu tạm dừng và các nguồn chưa được xác nhận quyền truy cập trong **phần Tình trạng bộ thu thập**. Các chi tiết này ban đầu được thu gọn và ẩn đi trên trang Tài khoản. Một thẻ hướng dẫn thiết lập sẽ hiển thị bước tiếp theo: kết nối tài khoản, chọn nguồn hoặc bắt đầu theo dõi. Danh sách tài khoản là bản chụp nhanh tại thời điểm tải; không gian làm việc đã chọn sẽ được làm mới định kỳ. Đây không phải là công cụ giám sát SLA đa quy trình.

Giao diện người dùng (UI) sử dụng các tài nguyên và cách hiển thị văn bản tại địa phương cho nội dung nguồn. Các bố cục dành cho máy tính để bàn và màn hình hẹp dựa trên Chromium đã được kiểm thử. Đây không phải là chứng nhận khả năng tiếp cận đầy đủ; việc đánh giá khả năng sử dụng đối với người dùng và trình đọc màn hình vẫn là các công việc riêng biệt.

## Môi trường triển khai

| Môi trường | Cài đặt | Tình trạng xác minh |
| --- | --- | --- |
| Máy tính cá nhân/máy chủ Windows | Python 3.11 trở lên, scripts\Setup.cmd/Start.cmd, thư mục dữ liệu riêng tư | Đã được kiểm tra tại địa phương trên hệ điều hành Windows/Python 3.12 |
| Máy chủ Linux/VPS | Môi trường ảo Python (venv), người dùng dịch vụ chuyên dụng, HTTPS/SSH | Cung cấp mã nguồn, CI và ví dụ về systemd; không được thực thi trên máy chủ này |
| macOS | Môi trường ảo Python (venv), tiến trình nền trước hoặc trình duyệt | Ví dụ về launchd được cung cấp; cần thực hiện kiểm tra cài đặt riêng biệt |
| Docker/Compose | Khối lượng dữ liệu ổn định, một nhân viên | Cung cấp định nghĩa và tính năng kiểm tra thời gian chạy CI; Docker không khả dụng tại địa phương |
| Trình duyệt trên điện thoại | Kết nối với bảng điều khiển được bảo vệ trên máy chủ đang hoạt động | Đã thử nghiệm với bố cục Chromium thu gọn; trình thu thập dữ liệu không hoạt động trên iOS/Android |

Khả năng di động có nghĩa là không bắt buộc phải sử dụng dịch vụ đám mây hay xây dựng giao diện người dùng. Mỗi hệ thống đích vẫn cần có các phụ thuộc Python/mã hóa tương thích, ổ đĩa cục bộ và quyền truy cập mạng. Vui lòng tham khảo [tệp DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/deployment/) và [các mẫu dịch vụ](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md).

Các không gian làm việc chia sẻ CPU, bộ nhớ và vòng lặp sự kiện. Để cách ly các tiến trình, hãy sử dụng các phiên bản, cổng, thư mục dữ liệu và quyền truy cập tài khoản riêng biệt. Không có bảng điều khiển thống nhất giữa các phiên bản riêng biệt. Tuyệt đối không được chỉ định nhiều tiến trình làm việc truy cập cùng một cơ sở dữ liệu.

## Kiểm tra và xuất dữ liệu ban đầu

Vui lòng chạy lệnh `python start.py --check` trước khi khởi động môi trường đã được chuẩn bị sẵn. Thêm `--json` để thực hiện các kiểm tra có thể đọc được bằng máy hoặc truyền các tham số `--data-dir`, `--host` và `--port` theo ý định. Lệnh này kiểm tra các điều kiện tiên quyết mà không yêu cầu đăng nhập Telegram hay tạo nhật ký. Lệnh này không xác minh nhật ký cũng như không chứng minh khả năng sẵn sàng ghi lại; quá trình xác minh nhật ký sẽ diễn ra trong quá trình khởi động ứng dụng. Cổng đang được sử dụng có thể chỉ đơn giản là một phiên bản hiện có.

Các trình duyệt hỗ trợ API Truy cập Hệ thống Tệp sẽ lưu các tệp xuất thông qua một luồng dữ liệu có thể ghi . Các trình duyệt khác chỉ lưu trữ tạm thời tối đa 128 MiB. Vui lòng sử dụng CLI truyền luồng cho các tệp xuất có dung lượng lớn hơn hoặc đối với các trình duyệt không hỗ trợ truyền tệp:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Thêm mã `--profile ID` từ mục Xuất để tạo không gian làm việc con. Sử dụng mã `--url https://server` để truy cập từ xa. Giao thức HTTP thuần túy chỉ được chấp nhận đối với các đích loopback. Mã thông báo được đọc từ tệp và gửi trong tiêu đề, không được hiển thị trên màn hình hay đưa vào URL. Các yêu cầu chuyển hướng sẽ bị từ chối. Các đích hiện có sẽ không bị ghi đè. Các lần truyền dữ liệu thất bại sẽ xóa tệp tạm thời tương ứng. Giá trị SHA-256 được báo cáo là tổng kiểm tra của quá trình truyền; quý vị cần xác minh tệp ZIP đã ký một cách riêng biệt bằng dấu vân tay/điểm kiểm tra đáng tin cậy.

## Sao lưu, khôi phục và các sự cố gián đoạn

1. Tạm dừng quá trình quan sát và dừng quy trình một cách triệt để.
2. Sao chép toàn bộ thư mục dữ liệu: cơ sở dữ liệu, WAL/SHM (nếu có), tệp phương tiện, `credentials.enc`, `signing.enc`, `network.enc`, khóa kho lưu trữ/siêu dữ liệu, mã thông báo, các điểm kiểm tra và mọi thư mục `profiles/`.
3. Đối với chế độ khóa bên ngoài, hãy bảo quản riêng biệt khóa chính và lưu giữ từng khóa `vault.external.json`. Việc tạo khóa mới sẽ không thể khôi phục các thông tin bí mật cũ.
4. Khôi phục dữ liệu trong khi đích đang bị tạm dừng; cấu hình khóa gốc, hạn chế quyền truy cập và xác minh tính toàn vẹn trước khi tiếp tục.
5. Ghi lại thời gian ngừng hoạt động và kết quả xác minh. Một bản chụp lịch sử không thể chứng minh rằng không có hành vi xóa nào xảy ra trong thời gian gián đoạn.

Các tệp ZIP chứa bằng chứng không bao gồm các phiên làm việc/khóa riêng tư và không phải là bản sao lưu toàn bộ dịch vụ. Có bốn loại dữ liệu được bảo vệ theo các cách khác nhau:

| Nội dung | Bảo vệ |
| --- | --- |
| Tệp xuất không có mật khẩu (mặc định) | Không được mã hóa. Đã được ký số, do đó mọi thay đổi đều có thể phát hiện được, nhưng bất kỳ ai sở hữu tệp tin này đều có thể đọc được nội dung. |
| Tệp xuất có mật khẩu | Nếu quý vị đặt mật khẩu, tệp xuất hoàn chỉnh sẽ được lưu nguyên vẹn dưới dạng tệp ZIP được mã hóa bằng AES-256 của WinZip mà 7-Zip và WinRAR đều có thể mở được; mật khẩu sẽ không được lưu trữ ([quy trình xử lý bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/)) |
| Cơ sở dữ liệu nhật ký và các tệp đính kèm được lưu trữ trên đĩa | Không được mã hóa bởi TgWitness; vui lòng sử dụng đĩa hoặc phân vùng được mã hóa |
| Các phiên Telegram và khóa ký | Được mã hóa trong thư mục dữ liệu (`credentials.enc`, `signing.enc`, `network.enc`) |

Sao lưu toàn bộ dịch vụ là thư mục dữ liệu đã được lưu trữ như mô tả ở trên, chứ không phải là tệp xuất. Vui lòng sử dụng bộ nhớ được bảo vệ và cơ chế truyền tải có chủ đích cho cả hai trường hợp. Các tệp xuất tạm thời trên máy chủ được lưu trữ trong thư mục `temporary-exports/` của từng không gian làm việc; các phản hồi đã hoàn tất sẽ được xóa, còn các tệp xuất bị gián đoạn sẽ bị loại bỏ vào lần khởi động tiếp theo trong khi khóa phiên bản của không gian làm việc đó vẫn còn hiệu lực.

Việc khôi phục kết nối không đảm bảo việc phục hồi các thay đổi xảy ra trong quá trình đó. Các tác vụ phương tiện lưu trữ liên tục và vị trí cập nhật của Telegram vẫn được duy trì sau khi khởi động lại; vui lòng tham khảo [định dạng bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#durable-collection-and-process-receipts-02).

## Dung lượng và thời gian lưu trữ

Các giới hạn mặc định, tất cả đều có thể thay đổi trong **phần Thông số**: 1.000 cuộc đối thoại đầu tiên, 500 tin nhắn cho mỗi bản chụp nhanh, 4 GiB nội dung ZIP đã ký không nén (các tệp lưu trữ lớn hơn cần `verify.py --max-gib N`) và dung lượng dự phòng 128 MiB cho trình duyệt. Các tệp đính kèm chiếm từ 1–2.000 MiB cho mỗi loại trong **phần Nguồn → Tệp đính kèm**. CLI tải xuống mặc định cho phép truyền tối đa 5 GiB. Dung lượng đĩa trống có thể là giới hạn thấp hơn. Hãy dành dung lượng cho các nhật ký, phương tiện truyền thông, WAL, các bản xuất tạm thời và bản sao lưu. Các bản xuất sử dụng dung lượng dữ liệu thay vì 512 MiB theo định dạng `/tmp` của Compose.

Hãy đo lường số sự kiện mỗi giây, thời gian tồn tại của hàng đợi, dung lượng phương tiện và độ trễ đĩa thay vì chỉ đếm số lượng nhóm. Các bài kiểm tra hiệu năng tổng hợp tại địa phương không đảm bảo việc gửi tin nhắn trên Telegram. Không có cơ chế xóa tự động theo thời gian lưu trữ. Việc xóa phần cuối của nhật ký sẽ làm mất hiệu lực mối liên hệ của nó với các điểm kiểm tra đã được lưu giữ.

Các lần kiểm tra lại ưu tiên đã được thiết lập sẵn: các nguồn được đánh dấu sao sẽ được kiểm tra lại mỗi 15 phút theo mặc định, các nguồn khác mỗi 6 giờ (xem [các cấp độ kiểm tra lại](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/#recheck-tiers)). Các tệp xuất được bảo vệ bằng mật khẩu như đã mô tả ở trên. Chức năng chấp nhận Telegram/proxy trực tiếp, phát lại bền vững, nhật ký quản trị và thăm dò phản hồi, các công cụ làm việc độc lập, mã hóa nhật ký cục bộ và phương tiện truyền thông bởi chính TgWitness cũng như việc rà soát độc lập vẫn là các công việc riêng biệt. Quyền truy cập có phạm vi giới hạn được ghi chép trong [phần truy cập và quyền hạn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/). Xin tham khảo các tệp [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md), [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) và [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/).
