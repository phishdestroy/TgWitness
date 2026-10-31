# Hướng dẫn bắt đầu nhanh

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/quickstart/

Tất cả các phương thức cài đặt và khởi chạy TgWitness: gói phần mềm dành cho Windows, Python, Docker và bản demo tổng hợp, kèm theo các bước kiểm tra ban đầu.

**Tiếng Anh** · [Tiếng Nga](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [Tiếng Ukraina](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Tiếng Tây Ban Nha](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [Tiếng Bồ Đào Nha (Brazil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Tiếng Thổ Nhĩ Kỳ](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [Tiếng Ả Rập](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [Tiếng Ba Tư](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [Tiếng Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [Tiếng Hindi](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [Tiếng Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [Tiếng Trung giản thể](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness là một ứng dụng độc lập dùng để theo dõi các nhóm và kênh Telegram mà tài khoản của quý vị có quyền truy cập. Ứng dụng này chạy cục bộ với thư mục dữ liệu riêng.

**Đây là lần đầu tiên quý vị truy cập?** [Hãy khám phá bản demo](https://phishdestroy.github.io/TgWitness/vi/docs/reference/quickstart/#explore-the-interface) trước khi kết nối tài khoản. [Vui lòng chọn hướng dẫn](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) về proxy, chứng nhân, xuất dữ liệu hoặc thiết lập máy chủ.

## Cài đặt và bắt đầu

[Thu thập qua GitHub Actions (bản xem trước)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

Vui lòng chọn một phương thức. Các bản tải xuống di động sẽ có sẵn sau khi bản phát hành chính thức được công bố:

| Máy chủ | Không cần cài đặt bất kỳ phần mềm nào | Từ nguồn: Python 3.11 trở lên | Docker: Engine/Desktop với Compose 2.20 trở lên |
| --- | --- | --- | --- |
| Windows | Trích xuất tệp `TgWitness-<version>-windows-amd64-portable.zip` từ GitHub Releases, nhấp đúp vào tệp `TgWitness.cmd` | Nhấp đúp vào `Start.cmd` | Nhấp đúp vào `scripts\Docker.cmd` |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

Đối với các phương pháp lấy mã nguồn, quý vị hãy tải xuống và giải nén tệp ZIP chứa mã nguồn từ GitHub Releases hoặc sao chép kho lưu trữ. `Start.cmd` sẽ đề xuất cài đặt Python 3.12 cho người dùng Windows nếu không tìm thấy phiên bản Python phù hợp (winget hoặc trình cài đặt có chữ ký từ python.org). `start.sh` sẽ hiển thị lệnh cài đặt chính xác dành cho bản phân phối Linux hoặc macOS của quý vị nếu thiếu Python. Lần khởi chạy mã nguồn đầu tiên sẽ tạo ra `.venv` và tự động cài đặt các phụ thuộc.

Docker sẽ biên dịch ứng dụng và khởi chạy nó ở chế độ nền; không cần phải cài đặt Python trên máy chủ. `scripts\Docker.cmd` và `scripts/docker-start.sh` sẽ hiển thị địa chỉ bảng điều khiển và mã thông báo khi container hoạt động bình thường. Các lệnh Docker tương ứng trên mọi hệ điều hành được hỗ trợ là:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Mở trang **http://127.0.0.1:8787**. Sử dụng mã thông báo được tạo bởi trình trợ giúp Docker hoặc lệnh Docker thứ hai, hoặc truy cập **tệp data/live/panel-token.txt** đối với bản cài đặt di động hoặc từ nguồn. Tiếp tục tại **phần “Kết nối Telegram”** bên dưới. Các bản cài đặt gốc và Docker sử dụng bộ nhớ lưu trữ riêng biệt; việc khởi động Docker sẽ không nhập nhật ký gốc hiện có.

Đối với máy chủ, [quá trình triển khai](https://phishdestroy.github.io/TgWitness/vi/docs/reference/deployment/) bao gồm kích hoạt HTTPS tự động, khởi động lại hệ thống, các hình ảnh được công bố, các bản cập nhật và sao lưu.

## Khám phá giao diện

1. Vui lòng chạy **tệp `TgWitness-Demo.cmd`** trong gói di động, tệp **`scripts\Demo.cmd`** trong thư mục nguồn của Windows hoặc tệp ``sh start.sh --demo` ` trên hệ điều hành Linux/macOS. Khi khởi chạy từ nguồn, hệ thống sẽ tự động tạo tệp ``.venv` ` và cài đặt các thành phần phụ thuộc.
2. Truy cập **http://127.0.0.1:8787**.
3. Bản demo cục bộ sẽ tự động mở sổ nhật ký mẫu. Không cần sao chép mã thông báo để truy cập trực tiếp tại địa phương.

Các tin nhắn trong phần demo là hư cấu. Chế độ demo không thể kết nối với tài khoản Telegram thực tế.

## Kết nối với Telegram

> [!CẢNH BÁO] **Không nên sử dụng bất kỳ thứ gì mà quý vị không thể chấp nhận mất mát.** Chúng tôi khuyến cáo mạnh mẽ không nên kết nối các tài khoản cá nhân hoặc có giá trị, cũng như không nên tạo ID API / mã băm trên tài khoản mà quý vị coi trọng. Telegram có thể khóa tài khoản một cách bất ngờ và thường là vĩnh viễn, bất kể ứng dụng khách nào được sử dụng. Việc chạy thử nghiệm suôn sẻ phụ thuộc vào Telegram, không phải TgWitness, và không đảm bảo bất kỳ điều gì cho các giai đoạn sau này.

1. Nếu bản demo gốc đang chạy, hãy dừng nó lại và chạy **tệp Start.cmd** hoặc `sh start.sh`. Nếu không, hãy tiếp tục chạy bản cài đặt trực tiếp đã được khởi động ở trên.
2. Vui lòng sử dụng mã thông báo bảng điều khiển tương ứng với phương thức cài đặt của quý vị để mở bảng điều khiển.
3. Nếu quý vị cần sử dụng máy chủ trung gian (proxy), vui lòng lưu cài đặt tại **mục Tài khoản → Cài đặt → Cài đặt kết nối → Thay đổi đường dẫn kết nối**.
4. Trong **phần Tài khoản**, vui lòng nhập số điện thoại của quý vị và nhấn **Tiếp tục**, chọn **Mã QR → Hiển thị mã QR**, hoặc chọn tệp và nhấn **Kết nối tài khoản**. **API ID + Hash** là tùy chọn: không gian làm việc sẽ sử dụng cặp thông tin đã lưu hoặc nhập sẵn, hoặc một cặp thông tin hoạt động từ kho dự trữ tích hợp sẵn. Để sử dụng ứng dụng của riêng quý vị, vui lòng dán một cặp `API ID:API Hash` vào ô API ID. Để có khóa ủy quyền đầy đủ, hãy chọn **“Khóa ủy quyền”**, dán toàn bộ 512 ký tự thập lục phân và chọn ID DC được cung cấp. ID người dùng là tùy chọn và sẽ được đánh dấu nếu được nhập.
5. Vui lòng hoàn tất phương thức đăng nhập mà quý vị đã chọn: số điện thoại/mã xác thực/xác thực hai yếu tố (2FA), xác nhận từ ứng dụng Telegram đã đăng nhập đối với mã QR, hoặc nhập phiên đăng nhập được ủy quyền từ các nền tảng được hỗ trợ.
6. Vui lòng kiểm tra ID tài khoản được hiển thị. **Nguồn** mở: các cuộc trò chuyện của quý vị sẽ được tải tự động; hãy thêm các nhóm của quý vị vào.
7. Trong phần **“Chọn những thay đổi cần lưu giữ**”, hãy chọn các danh mục sự kiện hoặc tùy chọn có sẵn **“Tin nhắn, thao tác chỉnh sửa và xóa”**, sau đó lưu cài đặt giám sát.
8. Vui lòng chọn cài đặt tệp đính kèm riêng biệt, sau đó nhấn **Bắt đầu quan sát**.

Thông tin đăng nhập API dùng để xác định ứng dụng của quý vị; chúng không tự động cấp quyền truy cập cho tài khoản nào cả. Các nhóm riêng tư không yêu cầu tên người dùng công khai, nhưng tài khoản của quý vị phải có quyền truy cập.

Đối với các tài khoản hiện có, vui lòng tham khảo [các định dạng tài khoản và phiên làm việc](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/): bảng điều khiển hỗ trợ Telethon StringSession, Telethon/Pyrogram SQLite, tệp ZIP TData cho một tài khoản duy nhất và định dạng JSON tài khoản được hỗ trợ. Vui lòng chọn một phiên làm việc cùng với tệp JSON đi kèm, sau đó nhấn **“Kết nối tài khoản**”. Tính năng đăng nhập qua mã QR cũng có sẵn với các cài đặt API tùy chọn tương tự. TDLib, bot và danh sách tài khoản số lượng lớn không được hỗ trợ.

Để thêm một tài khoản khác, hãy nhấn vào **+** bên cạnh bộ chọn tài khoản hoặc mở **Tài khoản → Cài đặt → Cài đặt kết nối → Không gian làm việc**, hoặc sử dụng **mục Tài khoản**. Các không gian làm việc có các phiên làm việc, sổ nhật ký, khóa, nguồn và hàng đợi riêng biệt. Việc chuyển đổi chế độ xem sẽ không làm gián đoạn hoạt động của các trình thu thập khác. Cùng một tài khoản Telegram không thể được gán cho hai không gian làm việc trong bản cài đặt này. Không có số lượng không gian làm việc cố định; các không gian này chia sẻ chung một tiến trình, do đó dung lượng phụ thuộc vào cấu hình máy tính.

Mã thông báo bảng điều khiển trực tiếp bảo vệ quyền truy cập vào các thông tin ủy quyền Telegram và tài liệu đã lưu trữ của quý vị; mã này tách biệt với thông tin đăng nhập API của Telegram. Chỉ bản demo cục bộ được khởi chạy rõ ràng và truy cập trực tiếp mới được cấp quyền truy cập tự động. Bản demo từ xa hoặc qua proxy vẫn sử dụng mã `data/demo/panel-token.txt`.

## Xem lại và xuất dữ liệu

- **Sổ nhật ký:** tìm kiếm và lọc các ghi nhận theo nguồn và loại sự kiện.
- Vui lòng chọn một sự kiện để xem bản ghi gốc, thông tin nguồn gốc và các phiên bản đã lưu của sự kiện đó.
- Chi tiết chỉnh sửa hiển thị nội dung trước và sau khi chỉnh sửa (nếu có). Chi tiết xóa hiển thị nội dung được ghi lại lần cuối (nếu có); đối tượng không xác định vẫn được giữ nguyên trạng thái không xác định.
- **Các định dạng xuất:** tệp ZIP có chữ ký, JSONL, CSV và HTML ngoại tuyến.
- **Xuất toàn bộ cuộc trò chuyện** (Nguồn → Xuất toàn bộ cuộc trò chuyện): tải xuống toàn bộ lịch sử hiển thị của một cuộc trò chuyện dưới dạng gói dữ liệu được ký bằng `chat.json` (theo phong cách xuất Telegram) và một tệp `chat.html` có thể đọc được. Tính năng này hoạt động với các cuộc trò chuyện riêng tư khi tài khoản là thành viên. Đây là một bản chụp nhanh tại thời điểm hiện tại, không phải là bản tái tạo các tin nhắn đã bị xóa hoặc đã được chỉnh sửa trước đó. Xác minh bản sao bằng `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256`.
- **Lưu điểm kiểm tra:** duy trì ranh giới của sổ nhật ký đã được ký số bên ngoài bộ thu thập dữ liệu.
- **Tải xuống biên nhận thực thi có chữ ký:** lưu giữ bản ghi chương trình/phiên bản của bộ thu thập dữ liệu.
- **Chuẩn bị yêu cầu dấu thời gian:** chuẩn bị một yêu cầu ngoại tuyến gửi đến cơ quan cấp dấu thời gian; thực hiện theo hướng dẫn trong [tệp TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/timestamp/) để nhận và xác minh phản hồi.
- **Xác minh nhật ký:** kiểm tra chữ ký sự kiện và các liên kết trong chuỗi. Tính năng xuất dưới dạng ZIP cũng kiểm tra các tệp phương tiện.

Các trình duyệt được hỗ trợ có thể lưu trực tiếp các tệp xuất có dung lượng lớn vào tệp đã chọn. Các trình duyệt khác chỉ có thể lưu tạm tối đa 128 MiB. Trong khi máy chủ đang hoạt động, giao diện dòng lệnh (CLI) truyền trực tiếp hỗ trợ tải xuống các tệp có dung lượng lớn hơn mà không cần lưu tạm toàn bộ phản hồi:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Đối với không gian làm việc khác, hãy thêm `--profile ID` bằng cách sử dụng **Xuất → ID không gian làm việc**. Đối với máy chủ từ xa, hãy thêm `--url https://your-server`. Giới hạn truyền tải mặc định là 5 GiB; `--max-mib` cho phép thay đổi giới hạn này. Nội dung ZIP đã ký có giới hạn xác minh riêng là 4 GiB khi giải nén theo mặc định (**Parameters** cho phép tăng giới hạn này; hãy xác minh các tệp lưu trữ đó bằng `verify.py --max-gib N`). Hãy xác minh tệp lưu trữ bằng cách sử dụng bản sao đáng tin cậy của trình xác minh và dấu vân tay khóa/điểm kiểm tra được lưu giữ độc lập.

## Xem hướng dẫn cài đặt

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check` kiểm tra các phụ thuộc cục bộ, hỗ trợ ký số, bộ nhớ lưu trữ, cấu hình khóa và địa chỉ lắng nghe. Công cụ này không cài đặt bất kỳ thành phần nào cũng như không kết nối với Telegram. Nếu cổng đang bận, điều này có thể cho thấy một phiên bản khác đang chạy. Vui lòng sử dụng `--port` khác hoặc dừng phiên bản hiện tại trước.

Trình khởi chạy sẽ được cài đặt vào thư mục `.venv`. Các lệnh phụ trợ `python -m tgwitness...` phải sử dụng `.venv\Scripts\python.exe` trên Windows hoặc `.venv/bin/python` trên Linux/macOS, trừ khi môi trường đó đã được kích hoạt sẵn.

## Các phiên làm việc, biện pháp bảo vệ và quy trình vận hành

Một tệp Telethon SQLite `.session` đóng và nhất quán có thể được chuyển đổi tại địa phương bằng `python -m tgwitness.sessions account.session --out account.tgwitness-session`, sau đó tải vào Tài khoản. Tính năng nhập tệp trực tiếp và đăng nhập qua mã QR cũng có sẵn. Vui lòng tham khảo [tệp CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/) để biết các định dạng đăng nhập, SOCKS5, HTTP CONNECT, MTProxy và các khóa chính bên ngoài.

**Tạm dừng quan sát** sẽ ngừng quá trình thu thập. **Chế độ Khóa** chỉ chặn quyền truy cập trình duyệt. Đóng tab sẽ không làm dừng quá trình thu thập. Việc dừng quá trình này mới thực sự ngắt quá trình thu thập; bản chụp lịch sử không thể tái tạo lại toàn bộ các thao tác chỉnh sửa hoặc xóa đã bỏ lỡ. Xem [cách thức hoạt động của quá trình thu thập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/) đối với các chính sách sự kiện, hàng đợi tệp đính kèm, cách ly tài khoản và hành vi khởi động lại.

Các phiên làm việc và thông tin bí mật đều được mã hóa. Nội dung tin nhắn, tệp đa phương tiện và các tệp xuất ra yêu cầu phải có đĩa hoặc phân vùng được mã hóa. Các chữ ký xác nhận tính toàn vẹn dựa trên một khóa đáng tin cậy; chúng không xác định nguồn gốc từ Telegram cũng như không ngăn chặn việc làm giả bởi người vận hành kiểm soát công cụ thu thập dữ liệu và khóa của nó.

Vui lòng tham khảo [tệp OPERATIONS.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/operations/) để biết thông tin về sao lưu/khôi phục, [tệp DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/deployment/) về việc triển khai máy chủ, và [thư mục deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) để xem các ví dụ về dịch vụ. Bảng điều khiển đã cài đặt cũng bao gồm hướng dẫn thiết lập ngoại tuyến tại `/guide.html`.

Quá trình xác minh thực tế và các giới hạn hiện còn tồn tại được ghi chép trong [các tệp VERIFICATION.md](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/) và [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md).
