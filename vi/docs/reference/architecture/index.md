# Kiến trúc

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/architecture/

Các thành phần của bộ thu thập, bảng điều khiển, sổ nhật ký, các công cụ xử lý và công cụ chứng thực, cùng cách thức dữ liệu được truyền tải giữa các thành phần này.

Một tiến trình Python sẽ lưu trữ bảng điều khiển FastAPI cùng bất kỳ số lượng không gian làm việc độc lập nào, mỗi không gian đều có một khách hàng tài khoản người dùng Telethon. SQLite lưu trữ một nhật ký sự kiện được ký điện tử chỉ ghi thêm và các cài đặt vận hành có thể thay đổi. Một kho lưu trữ được mã hóa chứa thông tin đăng nhập API, StringSession và khóa ký. Giao diện người dùng là các tệp HTML/CSS/JavaScript được đóng gói đơn giản: không cần quá trình biên dịch Node, CDN hay tải xuống giao diện người dùng tại thời điểm chạy.

| Mô-đun | Trách nhiệm |
| --- | --- |
| collector.py | Ủy quyền, lựa chọn hộp thoại, cập nhật, ảnh chụp nhanh, hàng đợi phương tiện, giám sát kết nối |
| interactions.py / telegram_client.py | Các hành động cụ thể trên bảng điều khiển, biên nhận có chữ ký, ID yêu cầu tồn tại lâu dài và chính sách thử lại việc gọi lại/tham gia tại cấp tác vụ |
| message_content.py | So sánh tin nhắn có thể quan sát được, không bao gồm siêu dữ liệu truy cập truyền tải |
| workers.py | Vui lòng đợi cho đến khi các tác vụ xuất tệp hoàn tất trước khi tiến hành dọn dẹp sau khi hủy bỏ |
| store.py | Các giao dịch WAL, chuỗi sự kiện có thứ tự, bộ lọc truy vấn, cài đặt vận hành |
| security.py | Tạo tệp riêng tư, kho lưu trữ được mã hóa, ký số bằng Ed25519, khóa quy trình đơn |
| evidence.py | Xuất toàn bộ nhật ký, các bản sao, điểm kiểm tra, xác minh tệp đính kèm |
| verify.py | Trình xác minh độc lập, chỉ đọc (thư viện chuẩn + mật mã học): kho lưu trữ, phạm vi bao phủ, nhật ký chứng cứ và bài đăng trên kênh, tệp hồ sơ |
| app.py | API được xác thực, vòng đời, xác thực yêu cầu, bảng điều khiển tĩnh |
| profiles.py | Các trình thu thập từ nhiều tài khoản, bộ điều khiển quyền truy cập chung, vòng đời theo từng không gian làm việc |
| access.py | Các quyền truy cập được giới hạn, kiểm tra quyền, hạn chế địa chỉ IP, giới hạn phiên làm việc và bảng điều khiển quản trị viên |
| proxy_catalog.py | Ảnh chụp nhanh nguồn cấp dữ liệu công khai, kiểm tra đường truyền, nhóm proxy được chia sẻ và cơ chế lựa chọn dựa trên tình trạng hoạt động |
| provenance.py | Các chỉ số về danh tính, mã nguồn và phụ thuộc được xác thực trong quá trình thu thập dữ liệu |
| network.py | Các lộ trình được xác thực theo từng không gian làm việc; trạng thái và bằng chứng đã được che giấu; các tùy chọn truyền tải Telethon |
| sessions.py | Chuyển đổi sang chế độ chỉ đọc ngoại tuyến các lược đồ SQLite của Telethon đã được rà soát |
| account_import.py | Phát hiện và chuẩn hóa trong bộ nhớ đối với các tệp tài khoản được hỗ trợ và tệp JSON |
| tdata.py | Trình đọc tệp ZIP TData hiện đại có giới hạn, xác thực tổng kiểm tra/giải mã, không trích xuất |
| doctor.py | Kiểm tra khả năng sẵn sàng tại địa phương mà không cần thu thập dữ liệu, đăng nhập hay cài đặt gói phần mềm |
| download.py | Tính năng xuất dữ liệu trực tuyến đã được xác thực, cho phép tải xuống với số lần đọc giới hạn và không ghi đè |
| monitoring.py | Chính sách sự kiện được xác thực theo từng không gian làm việc và các quy tắc đính kèm theo từng loại tệp, được chia sẻ bởi các người xử lý, trạng thái và biên nhận có chữ ký |
| scope.py | Phạm vi giám sát (các cuộc trò chuyện được chọn, thư mục Telegram, toàn bộ tài khoản), các loại nguồn, các trường hợp loại trừ, các cấp độ kiểm tra lại |
| dossier.py | Hồ sơ cá nhân theo từng cuộc trò chuyện được xây dựng từ các bản ghi đã lưu: các sự kiện kèm theo tham chiếu bản ghi, mã SHA-256/pHash của ảnh đại diện, trích xuất các đề cập |
| witness_api.py | Các mã thông báo chứng nhân chỉ đọc và phần đầu nhật ký đã được ký điện tử mà chúng có thể truy xuất |
| witness.py | Quy trình chứng thực độc lập: khóa và nhật ký riêng, kiểm tra đầu vào, bài đăng trên kênh có chữ ký, xuất dữ liệu |
| alerts.py | Các thông báo của Apprise và danh sách thông báo trên bảng điều khiển |
| logging_config.py | Ghi nhật ký trên bảng điều khiển và chẩn đoán máy chủ theo chu kỳ cho các phiên khởi chạy không hiển thị giao diện người dùng |
| static/ | Giao diện đáp ứng, cổng truy cập cục bộ, bộ lọc, thông tin chi tiết, tính năng xuất dữ liệu, thiết lập tài khoản |
| demo.py | Nhật ký tổng hợp được ghi nhãn rõ ràng, tách biệt với dữ liệu thu thập thực tế |

Các trình xử lý quan sát được đăng ký trước khi kết nối. Việc thu thập dữ liệu trực tiếp được kiểm soát bởi danh tính khách hàng đang hoạt động, trạng thái chạy rõ ràng, các nguồn được kích hoạt hoặc phạm vi quan sát (chế độ thư mục hoặc toàn bộ tài khoản sẽ thêm một cuộc trò chuyện mới làm nguồn khi có bản cập nhật đầu tiên), và chính sách sự kiện. Các khách hàng bị từ chối hoặc bị thay thế không thể đóng góp các bản cập nhật trực tiếp. Các phản ứng thô và cập nhật thành viên vẫn tuân thủ các giới hạn về khả năng hiển thị. Nội dung tin nhắn đến và tác vụ phương tiện bền vững của nó được ghi lại cùng nhau. Các tác vụ giữ nguyên mô tả TL ban đầu và liên kết hàm băm của nó với quan sát tin nhắn đã được ký tên. Các khái niệm về người gửi/người chỉnh sửa/người xóa được tách biệt.

Mỗi không gian làm việc chỉ chấp nhận một tài khoản và có thư mục riêng cùng danh tính ký xác thực. Không gian làm việc chính được đặt tại thư mục gốc để đảm bảo tính tương thích; các không gian làm việc bổ sung nằm trong thư mục profiles/<id>/. Một mã thông báo mang (bearer token) duy nhất kiểm soát toàn bộ hệ thống; các không gian làm việc không phải là các đơn vị ủy quyền riêng biệt. Các khóa quy trình bảo vệ các thư mục; các khóa cơ sở dữ liệu thực hiện tuần tự hóa việc chèn sự kiện. Mỗi lần thêm dữ liệu đều được ghi đồng bộ vào WAL của SQLite với chế độ đồng bộ HOÀN TOÀN. Các trình kích hoạt cập nhật/xóa sự kiện ngăn chặn các thao tác chỉnh sửa thông thường từ ứng dụng; các quản trị viên hệ thống tệp vẫn nằm trong ranh giới tin cậy.

Ủy quyền API sử dụng mã thông báo mang theo (bearer token). Các thao tác đăng nhập được tuần tự hóa và có giới hạn thời gian. Việc tải lên tài khoản áp dụng giới hạn 12 MiB dành riêng cho phần nội dung được mã hóa và giới hạn 8 MiB cho tệp đã giải mã; các yêu cầu API thông thường vẫn giữ nguyên giới hạn 16 KiB. Quá trình chuyển đổi diễn ra trong một luồng công việc, giữ các dữ liệu tải lên trong bộ nhớ và trả về đầu vào đã chuẩn hóa cho trình duyệt đã được xác thực. Đăng nhập qua mã QR có mã định danh tạm thời dành riêng cho từng không gian làm việc, tác vụ chờ và cơ chế hủy bỏ rõ ràng. Chỉ ủy quyền được chấp nhận mới trở thành khách hàng đang hoạt động. Telegram FloodWait được trả về kèm theo giá trị Retry-After; thông tin xác thực và các thông báo lỗi RPC thô không được hiển thị trong các lỗi API. Các tác vụ xuất dữ liệu chạy bên ngoài vòng lặp sự kiện không đồng bộ và được tuần tự hóa theo từng không gian làm việc. Chúng truyền phát một bản chụp đọc ổn định và có thể tồn tại song song với các thao tác ghi WAL đang diễn ra. Các bộ thu thập không gian làm việc chia sẻ cùng một quy trình/vòng lặp sự kiện.

Các bản chụp lịch sử hiện tại và các bản cập nhật trực tiếp có thể trùng lặp. Cả hai đều là các quan sát riêng biệt, được gắn nhãn theo nguồn; các bản trùng lặp sẽ không bị gộp lại một cách im lặng. Không có bất kỳ suy luận nào từ việc thiếu ID, văn bản bị xóa giả mạo, liệt kê thành viên bắt buộc hoặc việc tham gia nhóm tự động được triển khai.

Để tham khảo phần giải thích dành cho người vận hành, vui lòng xem [cách thức thu thập dữ liệu](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/) cũng như [các định dạng tài khoản và phiên làm việc](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/).

Cấu hình mạng được lưu trữ trong kho dữ liệu được mã hóa. Việc áp dụng một tuyến đường sẽ đóng các máy khách cũ và hủy bỏ các phiên đăng nhập chưa hoàn tất; các kết nối sau đó sẽ sử dụng tuyến đường đó mà không có phương án dự phòng trực tiếp. Một quá trình cài đặt mới sử dụng khóa bên ngoài sẽ tạo ra khóa Fernet cho từng không gian làm việc bằng thuật toán HKDF-SHA256 từ tệp khóa chính và một giá trị muối ngẫu nhiên đã được lưu trữ. Điều này giúp bảo vệ các thông tin bí mật một cách riêng biệt so với thư mục dữ liệu, chứ không phải nội dung nhật ký/tệp phương tiện ở dạng văn bản thuần túy.

Mục demo cục bộ sử dụng khả năng xử lý được tạo riêng biệt, không bao giờ sử dụng mã thông báo bảng điều khiển đã được cấu hình. Việc phát hành và chấp nhận yêu cầu chế độ demo rõ ràng, một gốc tổng hợp không có không gian làm việc bổ sung hoặc phiên được ủy quyền, đối tác/máy chủ vòng lặp, không có tiêu đề chuyển tiếp proxy và không có yêu cầu trình duyệt xuyên nguồn. Các API trực tiếp vẫn duy trì xác thực người mang và từ chối các thay đổi về thu thập dữ liệu trong chế độ demo.
