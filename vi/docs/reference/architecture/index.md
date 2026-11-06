# Kiến trúc

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/architecture/

Các thành phần của bộ thu thập, bảng điều khiển, sổ nhật ký, các công cụ xử lý và công cụ chứng thực, cùng cách thức dữ liệu được truyền tải giữa các thành phần này.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Phát triển](https://phishdestroy.github.io/TgWitness/assets/chapter-develop.svg)

Một tiến trình Python sẽ lưu trữ bảng điều khiển FastAPI cùng bất kỳ số lượng không gian làm việc độc lập nào, mỗi không gian đều có một khách hàng tài khoản người dùng Telethon. SQLite lưu trữ một nhật ký sự kiện được ký điện tử chỉ ghi thêm và các cài đặt vận hành có thể thay đổi. Một kho lưu trữ được mã hóa chứa thông tin đăng nhập API, StringSession và khóa ký. Giao diện người dùng là các tệp HTML/CSS/JavaScript được đóng gói đơn giản: không cần quá trình biên dịch Node, CDN hay tải xuống giao diện người dùng tại thời điểm chạy.

Optional browser and AyuGram recorders run in **separate processes or containers**. The `tgwitness_capture` package owns their event format, keys, artifacts, checkpoint API, independent witness and standalone verifier. It is bundled in the main wheel and can also be installed alone from `addons/capture`, without importing the collector. The main panel's `capture_api.py` and `capture_connections.py` provide administrator-only, workspace-scoped controls under `/api/capture`; connection tokens live in the encrypted vault. No recorder or outbound request starts with the main process. Each explicit command verifies a fresh challenge against the pinned recorder key. Exports are verified before download and keep their original signature; they do not become Telegram message events. Collection sessions and proxy routes stay with each client. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md) for deployment and trust boundaries.

| Mô-đun | Trách nhiệm |
| --- | --- |
| collector.py | Ủy quyền, lựa chọn hộp thoại, cập nhật, ảnh chụp nhanh, hàng đợi phương tiện, giám sát kết nối |
| interactions.py / telegram_client.py | Các hành động cụ thể trên bảng điều khiển, biên nhận có chữ ký, ID yêu cầu tồn tại lâu dài và chính sách thử lại việc gọi lại/tham gia tại cấp tác vụ |
| message_content.py | So sánh tin nhắn có thể quan sát được, không bao gồm siêu dữ liệu truy cập truyền tải |
| workers.py | Vui lòng đợi cho đến khi các tác vụ xuất tệp hoàn tất trước khi tiến hành dọn dẹp sau khi hủy bỏ |
| distributed_export.py / distributed_pages.py | Các tác vụ trò chuyện đồng thời, giới hạn theo tài khoản, các điểm kiểm tra đã ký và quá trình dọn dẹp sau khi xác minh kho lưu trữ |
| distributed_takeout.py / export_timing.py | Các phiên Takeout có thể tiếp tục và thời gian cho mỗi lần bắt đầu hoặc tiếp tục |
| store.py | Các giao dịch WAL, chuỗi sự kiện có thứ tự, bộ lọc truy vấn, cài đặt vận hành |
| fulltext.py | Chỉ mục toàn văn được tạo ra (các dạng từ, BM25), được liên kết với tiêu đề của nhật ký có chữ ký; không bao giờ được xuất ra ngoài |
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

Ủy quyền API là mã thông báo mang theo (bearer token). Các thao tác đăng nhập được tuần tự hóa và giới hạn thời gian. Việc tải lên tài khoản sử dụng giới hạn nội dung được mã hóa 12 MiB chuyên dụng và giới hạn tệp được giải mã 8 MiB ; các yêu cầu API thông thường vẫn giữ giới hạn 16 KiB. Quá trình chuyển đổi chạy trong luồng công việc, giữ các tệp tải lên trong bộ nhớ và trả về đầu vào đã chuẩn hóa cho trình duyệt đã được xác thực. Đăng nhập qua QR có ứng viên cho từng không gian làm việc, định danh tồn tại trong thời gian ngắn, tác vụ chờ và hủy bỏ rõ ràng. Chỉ ủy quyền được chấp nhận mới trở thành khách hàng hoạt động. Telegram FloodWait được trả về kèm giá trị Retry-After; thông tin xác thực và thông báo lỗi RPC thô không được hiển thị trong các lỗi API. Việc xuất nhật ký diễn ra bên ngoài vòng lặp sự kiện async và được tuần tự hóa theo từng không gian làm việc. Chúng truyền một bản chụp đọc ổn định song song với các thao tác ghi WAL đang diễn ra. Các tác vụ thu thập tin nhắn có thể chạy đồng thời trên các tài khoản riêng biệt; mỗi tài khoản vẫn được giữ lại cho đến khi tác vụ của nó dừng lại. Một tác vụ bị tạm dừng hoặc thất bại vẫn giữ lại các điểm kiểm tra của mình. Việc xác minh kho lưu trữ thành công cho phép dọn dẹp các tệp làm việc của nó, chỉ giữ lại tệp ZIP, kế hoạch đã ký và trạng thái. Các trình thu thập không gian làm việc chia sẻ vòng lặp quá trình/sự kiện.

Các bản chụp lịch sử hiện tại và các bản cập nhật trực tiếp có thể trùng lặp. Cả hai đều là các quan sát riêng biệt, được gắn nhãn theo nguồn; các bản trùng lặp sẽ không bị gộp lại một cách im lặng. Không có bất kỳ suy luận nào từ việc thiếu ID, văn bản bị xóa giả mạo, liệt kê thành viên bắt buộc hoặc việc tham gia nhóm tự động được triển khai.

Để tham khảo phần giải thích dành cho người vận hành, vui lòng xem [cách thức thu thập dữ liệu](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/) cũng như [các định dạng tài khoản và phiên làm việc](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/).

Cấu hình mạng được lưu trữ trong kho dữ liệu được mã hóa. Việc áp dụng một tuyến đường sẽ đóng các máy khách cũ và hủy bỏ các phiên đăng nhập chưa hoàn tất; các kết nối sau đó sẽ sử dụng tuyến đường đó mà không có phương án dự phòng trực tiếp. Một quá trình cài đặt mới sử dụng khóa bên ngoài sẽ tạo ra khóa Fernet cho từng không gian làm việc bằng thuật toán HKDF-SHA256 từ tệp khóa chính và một giá trị muối ngẫu nhiên đã được lưu trữ. Điều này giúp bảo vệ các thông tin bí mật một cách riêng biệt so với thư mục dữ liệu, chứ không phải nội dung nhật ký/tệp phương tiện ở dạng văn bản thuần túy.

Mục demo cục bộ sử dụng khả năng xử lý được tạo riêng biệt, không bao giờ sử dụng mã thông báo bảng điều khiển đã được cấu hình. Việc phát hành và chấp nhận yêu cầu chế độ demo rõ ràng, một gốc tổng hợp không có không gian làm việc bổ sung hoặc phiên được ủy quyền, đối tác/máy chủ vòng lặp, không có tiêu đề chuyển tiếp proxy và không có yêu cầu trình duyệt xuyên nguồn. Các API trực tiếp vẫn duy trì xác thực người mang và từ chối các thay đổi về thu thập dữ liệu trong chế độ demo.
