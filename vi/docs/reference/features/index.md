# Các tính năng và giới hạn

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/features/

Những tính năng mà TgWitness hiện đang triển khai, những hạn chế của nền tảng Telegram và những công việc còn cần thực hiện trong tương lai.

Tham chiếu thiết kế: ngày 26 tháng 10 năm 2026. Trường hợp sử dụng chính là các nhóm và kênh Telegram riêng tư mà các tài khoản được kết nối có thể truy cập. Tài liệu này phân biệt rõ giữa hành vi đã được triển khai, giới hạn của nền tảng và các công việc trong tương lai. Một mục kiến trúc mục tiêu không đồng nghĩa với việc tính năng đó đã tồn tại.

## Ứng dụng độc lập

TgWitness có quy trình cài đặt, thư mục dữ liệu và chu kỳ phát hành riêng. Giao diện web đi kèm giúp quản lý việc thiết lập và xem xét; các bản ghi đã xuất ra có thể được sử dụng độc lập.

Người vận hành kết nối các tài khoản của mình, chọn các nguồn mà mỗi tài khoản có thể truy cập, và nhận được một sổ nhật ký quan sát đã được lưu trữ. Bảng điều khiển hiển thị nội dung, các thay đổi đã lưu, nguồn gốc của quan sát và các lỗ hổng đã biết. Một điều tra viên khác có thể xác minh tài liệu đã xuất ra.

Có bốn trạng thái riêng biệt cần được xem xét: ủy quyền tài khoản, quyền truy cập vào nguồn, một bộ thu thập đang hoạt động, và mức độ hoàn chỉnh của việc chuyển phát được xác định. Không có trạng thái nào trong ba trạng thái đầu tiên tự động chứng minh được trạng thái thứ tư. Một nhóm im lặng không nhất thiết có nghĩa là bộ thu thập đã thất bại.

## Các cuộc điều tra chung

Quản trị viên có thể cấp [các mã thông báo truy cập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/) được giới hạn phạm vi cho các không gian làm việc và các cuộc trò chuyện riêng lẻ, kèm theo bảy quyền truy cập, hạn chế địa chỉ IP, thời hạn hiệu lực, giới hạn đăng nhập và kiểm soát phiên làm việc. Người xem chỉ đọc có thể kiểm tra một vụ việc mà không cần nhận sự ủy quyền từ Telegram hay khóa bảng điều khiển chính. Quyền truy cập giới hạn theo cuộc trò chuyện được tách biệt với các cài đặt chung của tài khoản và tính năng xuất toàn bộ nhật ký.

MTProxy tự động duy trì các tuyến kết nối Telegram hoạt động từ bốn nguồn công khai hoặc danh mục của nhà điều hành. [Chế độ IP](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/#ip-modes) quyết định liệu trong trường hợp lỗi, hệ thống phải chờ proxy khác hay có thể sử dụng tuyến kết nối trực tiếp được cho phép rõ ràng. Các yêu cầu HTTP bên ngoài có tuyến kết nối riêng biệt và công tắc tắt.

## Công cụ lưu trữ

Phiên bản hiện tại `main` bổ sung [các tính năng thu thập lịch sử](https://phishdestroy.github.io/TgWitness/vi/docs/reference/history/), [tìm kiếm và phân tích kho lưu trữ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/analysis/), [MCP chỉ đọc](https://phishdestroy.github.io/TgWitness/vi/docs/reference/mcp/), [OCR/chuyển đổi văn bản cục bộ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/media-analysis/) và [webhook gửi đi](https://phishdestroy.github.io/TgWitness/vi/docs/reference/webhooks/). Đây là các tính năng từ mã nguồn, được thêm vào sau bản xem trước di động 0.7.0. Các báo cáo phân tích và văn bản được nhận diện được lưu trữ riêng biệt với các sự kiện đã ghi lại.

## Các tính năng bổ sung tùy chọn

Quy trình thiết lập hàng ngày là tài khoản → nguồn → quan sát. **Phần Tiện ích bổ sung** là một đích đến riêng biệt với bot chứng thực Telegram và bản xem trước ghi lại trên GitHub. Mỗi phần đều nêu rõ tính khả dụng và yêu cầu trước khi hiển thị các thiết lập. Chọn một thẻ sẽ mở hướng dẫn; thao tác này không đăng ký hoặc khởi động dịch vụ.

Việc thiết lập bot bao gồm ba bước: tạo quyền truy cập chỉ đọc, chọn cài đặt xuất bản và khởi chạy trên máy chủ chứng thực. Các tùy chọn mạng và xuất bản, kết nối hiện có và lệnh xác minh sẽ được hiển thị theo yêu cầu. Cấu hình đã tải xuống là riêng biệt so với một Witness đang chạy. Việc chuyển đổi các tùy chọn bổ sung sẽ giữ lại bản nháp; các thay đổi tài khoản và việc khóa sẽ xóa mã thông báo tạm thời và biểu mẫu. Hướng dẫn tích hợp sẵn bao gồm các hướng dẫn khởi chạy. [GitHub Actions ghi lại](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) các lần khởi chạy một trình thu thập được ghim từ bản phân nhánh của bạn, ghi lại một cuộc trò chuyện và tạo ra một tệp chuyển giao được mã hóa kèm theo nguồn gốc quy trình làm việc.

## Giao thức và các nguồn tin riêng tư

**MTProto là giao thức của Telegram; Telethon là thư viện Python mà TgWitness sử dụng để giao tiếp qua MTProto.** Đây không phải là các phương thức kết nối thay thế. Quá trình thu thập dữ liệu sử dụng MTProto; tính năng chứng kiến tùy chọn sẽ công bố các bản kiểm tra đã được ký thông qua Bot API.

Mỗi không gian làm việc đều có luồng cập nhật tài khoản và khách hàng được ủy quyền riêng. TgWitness lựa chọn các dữ liệu quan sát từ các nguồn đã được cấu hình và thực hiện các yêu cầu riêng biệt, rõ ràng đối với các chức năng như chụp nhanh lịch sử và tải xuống tệp đa phương tiện.

Nguồn riêng tư không cần tên người dùng công khai. Loại kết nối ngang hàng trên Telegram và ID số là các thông tin nhận dạng; tiêu đề và tên người dùng có thể thay đổi. Quyền truy cập phụ thuộc vào tình trạng thành viên và quyền hạn hiện có. TgWitness không tự động tham gia vào các nguồn hoặc bỏ qua quy trình phê duyệt tham gia. Mã băm truy cập từ một tài khoản khác không phải là mã thông báo truy cập chung.

Mô hình thu thập dữ liệu phải tính đến lịch sử ẩn trước khi tham gia, vai trò của người tham gia/quản trị viên, việc thu hồi phiên, xóa bỏ hoặc thay đổi quyền truy cập, quá trình chuyển đổi từ nhóm sang siêu nhóm, các chủ đề/diễn đàn, các cuộc thảo luận liên kết, danh tính kênh và các tệp đính kèm không khả dụng. Không phải mọi trường hợp kết hợp đều đã được kiểm chứng trong thực tế.

Tính khả dụng của nguồn được kiểm tra khi trình thu thập bắt đầu hoạt động. Việc thiếu một nguồn trong kết quả cuộc đối thoại được giới hạn có nghĩa là **quyền truy cập chưa được xác nhận**, chứ không phải là bằng chứng cho thấy nguồn đó đã bị xóa. Việc một nguồn không khả dụng sẽ không cản trở việc quan sát các nguồn khác vẫn có thể truy cập được. Tuyệt đối không được đưa các liên kết mời hoặc phiên làm việc thực tế vào các tài liệu công khai.

## Nhiều tài khoản

Bảng điều khiển này hỗ trợ bất kỳ số lượng không **gian làm việc** nào, mỗi không gian đều có:

- Quyền truy cập, kho lưu trữ được mã hóa và đường dẫn kết nối.
- Sổ nhật ký SQLite và danh tính ký số Ed25519.
- Các nguồn được chọn, hàng đợi phương tiện và cài đặt ghi lại.
- Trạng thái quan sát, lỗi, điểm kiểm tra và các bản xuất dữ liệu.

Việc chuyển đổi không gian làm việc đang hiển thị sẽ không làm dừng hoạt động của bộ thu thập khác. Việc ủy quyền tài khoản trùng lặp giữa các không gian làm việc sẽ bị từ chối. Một sổ nhật ký đã được liên kết với một tài khoản Telegram không thể được gán lại cho tài khoản khác; tuy nhiên, việc kết nối lại cùng một tài khoản vẫn được phép. Điều này giúp duy trì danh tính tài khoản và phạm vi ID tin nhắn liên quan.

Không có số lượng cố định và không có đảm bảo về thông lượng được đo lường. Các không gian làm việc chia sẻ chung một quá trình Python và vòng lặp sự kiện. Việc triển khai các công cụ xử lý tài khoản riêng biệt vẫn là nhiệm vụ trong tương lai. Để tách biệt các quá trình hiện tại, vui lòng sử dụng các bản cài đặt, cổng và thư mục dữ liệu riêng biệt.

Gán cho mỗi tài khoản các nguồn mà tài khoản đó có thể truy cập. Các tài khoản khác nhau có thể theo dõi cùng một nhóm, nhưng các quan sát của chúng vẫn được tách biệt và giữ nguyên nguồn gốc. Hai tài khoản trên cùng một máy do một người vận hành kiểm soát không được coi là hai nhân chứng độc lập. Việc xuất dữ liệu được thực hiện theo từng không gian làm việc; tính năng gói hồ sơ vụ việc hợp nhất hoặc dòng thời gian Telegram toàn cầu hiện chưa được triển khai.

## Ghi lại và xác định nguồn gốc

Tính năng Nguồn cung cấp các tùy chọn riêng cho từng tài khoản đối với tin nhắn mới, các thao tác chỉnh sửa, xóa, phản hồi và thông tin thành viên. Các cài đặt sẵn sẽ lưu giữ toàn bộ danh mục hoặc chỉ các tin nhắn/thao tác chỉnh sửa/xóa. Chính sách này áp dụng cho các nhóm được chọn trong không gian làm việc, vẫn duy trì sau khi khởi động lại và được ký kèm theo thông tin trước và sau khi thay đổi. Cài đặt mặc định sẽ lưu giữ toàn bộ danh mục. Việc tắt một danh mục sẽ không xóa các bản ghi cũ; việc bật lại danh mục đó cũng không khôi phục các sự kiện đã bỏ lỡ. Các bản ghi hoạt động, các sự kiện dịch vụ nhóm khác và các bản chụp lịch sử rõ ràng là riêng biệt. Các đối tượng Telegram được ghi lại có thể vẫn giữ lại siêu dữ liệu nhúng bất kể các tùy chọn cập nhật riêng biệt. Hiện tại vẫn chưa có tùy chọn ghi đè danh mục cho từng nhóm.

| Nội dung | Đã ghi lại ngay lập tức | Phạm vi |
| --- | --- | --- |
| Thông điệp | Nội dung văn bản, ID người dùng/ID tin nhắn, siêu dữ liệu người gửi, các phản hồi và gói tin cập nhật gốc | Tin nhắn này không có chữ ký Telegram có thể xác minh công khai |
| Chỉnh sửa | Phiên bản mới được ghi nhận và bất kỳ phiên bản nào đã được lưu trước đó | Các thao tác chỉnh sửa tạm thời trong thời gian hệ thống ngừng hoạt động có thể bị mất; người gửi không nhất thiết phải là người chỉnh sửa |
| Việc xóa | Thông báo và nội dung đã được ghi lại trước đó (nếu có) | Thông thường không ghi nhận người xóa hoặc thời gian thực hiện hành động cụ thể |
| Việc xóa không được xác định phạm vi | Thông báo gốc ở cấp tài khoản mà không cần phỏng đoán về đối tượng liên quan | Việc đảm bảo sự tương quan chặt chẽ với các ID phạm vi tài khoản đã được lưu trữ trước đó là nhiệm vụ cần thực hiện trong tương lai |
| Phản hồi | Số liệu thống kê và danh tính gần đây được hiển thị rõ ràng | Danh sách đầy đủ các máy chủ phản hồi hiện có cần phải thực hiện các truy vấn riêng biệt; các kênh có thể ẩn danh tính |
| Thành viên | Thông báo dịch vụ và các bản cập nhật được gửi đến người tham gia | Khả năng hiển thị phụ thuộc vào vai trò và loại cuộc trò chuyện; việc thiếu các sự kiện không đồng nghĩa với việc chúng không tồn tại |
| Các thao tác của quản trị viên | Chỉ cung cấp các bản cập nhật có liên quan | Chức năng lấy mẫu nhật ký quản trị riêng biệt hiện chưa được triển khai |
| Tệp đính kèm | Mô tả phiên bản gốc, số byte đã tải xuống/SHA-256 và kết quả các lần thử | Một tệp đã biến mất có thể không thể khôi phục được; phiên bản mới nhất sẽ không được thay thế |
| Lịch sử | Ảnh chụp màn hình chi tiết các tin nhắn hiện đang hiển thị | Không tái tạo lại toàn bộ các nội dung đã được chỉnh sửa hoặc xóa bỏ |
| Quy trình thu thập dữ liệu | Khởi động/dừng, tín hiệu hoạt động, lỗi, cài đặt, phạm vi và biên nhận chương trình | Báo cáo tự nguyện, không phải là chứng nhận quy trình độc lập |

Một hành động chỉ được quy cho một cá nhân khi nguồn thực sự cung cấp thông tin về chủ thể đó. Nếu không, giao diện sẽ báo cáo việc thiếu thông tin xác định chủ thể. Tên người dùng và tên gọi là các thuộc tính được quan sát, không phải bằng chứng về danh tính trong thế giới thực.

## Dung lượng và các giới hạn của Telegram

Không có con số chung nào về số lượng cuộc trò chuyện có thể được giám sát với chất lượng được đảm bảo. Khả năng xử lý phụ thuộc vào số sự kiện đỉnh điểm mỗi giây, khối lượng và kích thước tệp đính kèm, các yêu cầu RPC bổ sung, số tài khoản đang hoạt động, độ trễ đĩa/dung lượng trống, điều kiện mạng, các giới hạn của Telegram, mức độ trễ chấp nhận được và độ sâu hàng đợi.

Telegram phân biệt giữa việc gửi tin nhắn thụ động và việc thăm dò ngắn chủ động. Tài liệu cập nhật của nền tảng này mô tả các cuộc gọi `updates.getChannelDifference` bổ sung dành cho các kênh mở/siêu nhóm và khuyến nghị tối đa **mười nguồn được thăm dò ngắn đồng thời**. Đây không phải là giới hạn mười nhóm được chọn hay một đảm bảo về tính đầy đủ.

| Chế độ | Mục đích | Tình trạng |
| --- | --- | --- |
| Quan sát tiêu chuẩn | Ghi lại các bản cập nhật được gửi từ các nguồn đã chọn | Đã triển khai |
| Quan sát ưu tiên | Các kiểm tra sự khác biệt bổ sung đối với tập nguồn có giới hạn | Chưa được triển khai dưới dạng chế độ người dùng |

Việc lấy mẫu ngẫu nhiên với tần suất cao, bỏ qua FloodWait hoặc giả định dung lượng tuyến tính từ các tài khoản bổ sung không phải là mô hình xác định quy mô hợp lệ. Các giới hạn mặc định là 1.000 cuộc đối thoại đầu tiên được liệt kê, tối đa 500 tin nhắn cho mỗi bản chụp lịch sử, 1–2.000 MiB cho mỗi tệp thu thập theo loại, và 4 GiB nội dung ZIP đã ký không nén; mỗi giới hạn này có thể được điều chỉnh cho từng không gian làm việc trong **phần Thông số**. Các tệp xuất không có giới hạn cố định về số lượng sự kiện. Chế độ dự phòng trình duyệt bị giới hạn ở mức 128 MiB theo mặc định; CLI truyền trực tuyến có giới hạn truyền tải có thể cấu hình, mặc định là 5 GiB.

`tools/check_capacity.py` đo lường việc nhập và xuất dữ liệu tổng hợp tại địa phương. Kết quả của công cụ này không phải là số liệu về tỷ lệ gửi tin nhắn thành công trên Telegram hay số lượng cuộc trò chuyện thực tế được đảm bảo. Vui lòng tham khảo [tệp VERIFICATION.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/) để biết phiên bản được đo lường và khối lượng công việc.

## Độ tin cậy và khả năng khôi phục

Các tính năng đã triển khai bao gồm giao dịch đồng bộ SQLite WAL; ghi tin nhắn và tác vụ phương tiện theo kiểu nguyên tử; tác vụ liên tục và độ trễ thử lại; mô tả phiên bản gốc; số lần thử lại có giới hạn; FloodWait phương tiện được lưu trữ lâu dài; việc tải xuống phương tiện bên ngoài thời gian chờ mạng của sự kiện văn bản; xuất dữ liệu với tiền tố ổn định trong khi các thao tác ghi sau đó vẫn tiếp tục; cài đặt nguyên tử và hồ sơ kiểm toán; duy trì quyền truy cập đang hoạt động sau khi đăng nhập thay thế thất bại; cách ly không gian làm việc bổ sung bị hỏng; các nỗ lực kết nối lại rõ ràng; báo cáo mất quyền truy cập riêng biệt; và phát hiện thay đổi theo đồng hồ thực bằng cách sử dụng đồng hồ đơn điệu.

Các thông số pts/qts/seq của tài khoản và kênh sẽ được lưu lại và khôi phục sau khi khởi động lại hệ thống, đồng thời các cuộc trò chuyện được theo dõi sẽ được kiểm tra lại định kỳ; xin tham khảo [định dạng bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#durable-collection-and-process-receipts-02). Việc lưu lại vị trí định kỳ không phải là một xác nhận nguyên tử, không mất mát về việc chấp nhận nhật ký.

Mỗi lần bắt đầu quá trình đều ghi lại vị trí đầu của bản ghi trước đó và ranh giới ngoại tuyến. Lịch sử hiện tại không được coi là phương pháp khắc phục khoảng trống. Khả năng lưu giữ sự khác biệt của Telegram là hữu hạn; `differenceTooLong` không thể tái tạo toàn bộ nội dung đã biến mất. Các khoảng trống không thể phục hồi phải được ghi nhận rõ ràng ngay cả khi bản chụp lịch sử sau đó thành công.

## Mô hình bằng chứng

Mỗi sự kiện ghi lại trình tự, thời gian quan sát theo múi giờ UTC địa phương, thời gian nguồn (nếu có), loại sự kiện, nguồn, tác nhân (nếu có), nội dung gốc, giá trị băm trước đó và chữ ký. Các quan sát tin nhắn cũng lưu giữ thông tin về tài khoản thu thập dữ liệu và bối cảnh thực thi.

Biên bản quá trình có chữ ký chứa ID chạy ngẫu nhiên; các phiên bản phụ thuộc của TgWitness/Python/OS; giá trị SHA-256 của tệp nguồn và dấu vân tay tổng hợp; tài khoản ban đầu, phạm vi và cài đặt; các giá trị UTC/đơn điệu; cùng phần đầu của nhật ký trước đó. Các thay đổi về cài đặt, thao tác khởi động/dừng và các lỗi đều được ghi vào cùng một nhật ký. Các điểm kiểm tra được lưu giữ khi khởi động, cứ sau năm phút trong quá trình quan sát (có thể điều chỉnh) và khi dừng hoạt động theo đúng trình tự. Một điểm kiểm tra cục bộ được lưu giữ có thể phát hiện việc quay trở lại một tiền tố nhật ký trước đó.

| Cơ chế | Những nội dung được xác lập |
| --- | --- |
| Mã SHA-256 của tệp | Số byte khớp với bản tóm tắt đã biết |
| Chuỗi băm sự kiện | Ghi lại thứ tự/mối liên kết so với một ranh giới đã biết |
| Ed25519 | Chữ ký được tạo bằng một khóa cụ thể |
| Điểm kiểm tra được lưu giữ độc lập | Các nội dung sau đây tuân thủ ranh giới đã được duy trì |
| Đo lường kích thước tệp chương trình | Báo cáo tự đánh giá của Collector về các tệp đã được đo lường |
| Phản hồi độc lập hợp lệ từ TSA | Sự tồn tại của các byte cụ thể tại thời điểm TSA dựa trên các giả định tin cậy rõ ràng |

Việc chuẩn bị yêu cầu theo RFC 3161 và xác minh phản hồi bằng OpenSSL đã được triển khai. Tính năng gửi tự động thì chưa được triển khai. Một yêu cầu hoặc chữ ký cục bộ mang thời gian của máy không phải là dấu thời gian độc lập. Vui lòng tham khảo [tệp TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/timestamp/).

Người vận hành kiểm soát bộ thu thập dữ liệu và khóa ký có thể tạo ra các bằng chứng mới đã được ký. Các chữ ký này không xác nhận nguồn gốc từ Telegram, tính xác thực hay tính hợp lệ pháp lý tự động. Để đảm bảo việc lưu giữ dữ liệu an toàn hơn, cần có điểm kiểm tra độc lập/lưu trữ theo thời gian, các biện pháp kiểm soát truy cập khóa, hồ sơ chuyển giao và quá trình xác minh từ phần mềm đáng tin cậy.

## Xuất dữ liệu, triển khai và bàn giao

Một tệp ZIP có chữ ký chứa các tệp JSONL, CSV, HTML gốc, các tệp đính kèm được bảo toàn, các giá trị băm, một bản kê khai có chữ ký và một công cụ xác minh tiện lợi. Tệp này bao gồm một không gian làm việc và một tiền tố nhật ký đầy đủ cố định. Các bộ lọc tìm kiếm trên bảng điều khiển sẽ không tự động xóa các bản ghi. Các khóa bí mật, mã thông báo và phiên Telegram sẽ bị loại trừ; tuy nhiên, các quan sát gốc vẫn có thể chứa thông tin cá nhân và siêu dữ liệu của Telegram.

Vui lòng lưu giữ riêng biệt bản tóm tắt ZIP, dấu vân tay đáng tin cậy, điểm kiểm tra, biên nhận quá trình và bản ghi chuyển giao. Hãy sử dụng trình xác minh từ một bản cài đặt đáng tin cậy, thay vì chỉ tin tưởng vào mã thực thi chỉ vì nó xuất hiện trong tệp ZIP đang được kiểm tra.

Giao diện trình duyệt được triển khai cục bộ mà không cần Node.js, CDN hay phông chữ bên ngoài. Một mã thông báo điều hành sẽ kiểm soát quá trình cài đặt. Việc truy cập từ xa yêu cầu HTTPS hoặc đường hầm SSH. Các định nghĩa Python gốc và container được cung cấp kèm theo, cùng với các ví dụ về dịch vụ trong [thư mục deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md); các kiểm tra nền tảng đã được thực thi được liệt kê riêng biệt.

Không gian làm việc mặc định sử dụng thư mục gốc dữ liệu; các không gian làm việc bổ sung sử dụng `profiles/<id>/`. Việc sao lưu yêu cầu quá trình phải được dừng lại và có đầy đủ bộ dữ liệu/khóa. Các tệp ZIP chứa bằng chứng không phải là bản sao lưu ứng dụng. Các thông tin bí mật có thể sử dụng khóa chính bên ngoài cho một thư mục dữ liệu mới; việc mã hóa nhật ký/tệp đa phương tiện được thực hiện bởi đĩa/khối lượng lưu trữ của người vận hành. Xin tham khảo các tệp [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/) và [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/operations/).

## Tiêu chí phát hành phiên bản ổn định

Trước khi phát hành phiên bản ổn định, cần làm rõ:

1. Các nhóm riêng tư, siêu nhóm, diễn đàn và kênh thực tế với các vai trò thành viên/quản trị viên cùng lịch sử ẩn/hiển thị, bao gồm thông tin đăng nhập/xác thực hai yếu tố (2FA), việc thu hồi quyền truy cập và tình trạng mất quyền truy cập.
2. Các hành động chỉnh sửa, xóa, phản hồi, thông tin thành viên và phương tiện truyền thông được kiểm soát so với các hành động đã biết.
3. Sự cố hệ thống/máy chủ, lỗi đĩa/đĩa đầy, tham chiếu tệp đã hết hạn, FloodWait, mất kết nối mạng, tệp bị hỏng và khôi phục cơ sở dữ liệu về phiên bản trước.
4. Hỗ trợ sử dụng liên tục nhiều tài khoản với độ trễ được kiểm soát, hàng đợi, bộ nhớ và dung lượng đĩa, bao gồm cả các nguồn dữ liệu im lặng lẫn ồn ào.
5. Sự gián đoạn giữa quá trình chuyển đổi trạng thái MTProto và việc chấp nhận nhật ký.
6. Quá trình cài đặt sạch trên ma trận hệ điều hành/môi trường container mục tiêu và đã xác minh khả năng khôi phục từ bản sao lưu.
7. Đánh giá độc lập về các vấn đề an ninh, chữ ký điện tử cũng như các tuyên bố liên quan đến nguồn gốc và bằng chứng.

Việc lấy dữ liệu nhật ký quản trị, danh sách máy chủ phản hồi bổ sung, lấy dữ liệu ưu tiên, các công cụ xử lý riêng biệt, cũng như mã hóa toàn bộ ứng dụng vẫn là những công việc cần thực hiện trong tương lai. Quyền truy cập theo phạm vi bảng điều khiển được mô tả trong phần [“Quyền truy cập và quyền hạn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/)”. Phiên bản 0.6 hỗ trợ TData giới hạn cho một tài khoản duy nhất và tính năng nhập tệp tài khoản được mô tả trong [tệp ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/). Vui lòng xem lại các điều khoản API của Telegram trước khi công bố. Các tài liệu tham khảo nghiên cứu và kết quả phân tích nền tảng được trình bày trong [tệp RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md).
