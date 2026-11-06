# Hướng dẫn sử dụng bảng điều khiển

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/

Mọi màn hình của bảng điều khiển: cuộc trò chuyện, nhật ký, nguồn, xuất dữ liệu, Tính năng bổ sung, chế độ bảo vệ và kiểm tra mã nguồn.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/vi/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Cài đặt ban đầu và cấu hình](https://phishdestroy.github.io/TgWitness/vi/docs/reference/settings/) · [Tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/) · [Xuất và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/) · [Báo cáo trường hợp](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-reports/)

Chức năng của từng màn hình, nội dung được ghi vào nhật ký đã ký và vị trí của hướng dẫn chi tiết. Bảng điều khiển hiển thị một không gian làm việc tại một thời điểm: một tài khoản Telegram với các nguồn, nhật ký và khóa ký riêng. Bộ chọn ở đầu thanh bên dùng để chuyển đổi giữa các không gian làm việc. Địa chỉ chứa thông tin về không gian làm việc (`?ws=…`); trong khi địa chỉ, công cụ chọn và tài khoản đã tải không khớp nhau, các thao tác sẽ bị chặn.

Use [Compare collection methods](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md) to choose between live observation, full history, fresh account/chat exports and saved-record handover. The Exports page includes the same comparison above its download controls.

**On this page**

- [Find your way](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#find-your-way)
- [Start here](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#start-here)
- [Chats](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#chats)
- [Journal](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#journal)
- [Sources](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#sources)
- [Exports](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#exports)
- [Settings, accounts and connection](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#settings-accounts-and-connection)
- [Extras](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#extras)
- [Protection modes](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#protection-modes)
- [More tools](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#more-tools)

## Tìm hiểu cách sử dụng

Các phần hàng ngày nằm ở đầu thanh bên, **phần Tài khoản** nằm dưới **mục Không gian làm việc** , và tất cả các mục khác nằm dưới **mục Công cụ và cài đặt khác** . Công tắc **cấp độ giao diện** trên thanh trên cùng quyết định số lượng phần hiển thị:

| Cấp độ | Các phần trong thanh bên |
| --- | --- |
| Đơn giản | Trang chủ, Trò chuyện, Thay đổi, Lưu trữ và Cài đặt |
| Tiêu chuẩn | Xem thêm Case Board, Tài khoản và Quyền truy cập |
| Chuyên gia | Ngoài ra còn có Sources, Extras, Ask the archive, Parameters, Account, System log và Integrations |

Các chức năng cơ bản: Bắt đầu tại đây, Nhật ký và Xuất dữ liệu, **Trang chủ**, **Thay đổi** và **Lưu trữ**. Mức độ bảo mật chỉ ẩn các phần. Tính năng bị ẩn vẫn hoạt động bình thường, và máy chủ tự động kiểm tra mọi quyền truy cập. Mức độ bảo mật, ngôn ngữ, chủ đề và múi giờ được lưu riêng cho mỗi người dùng và không gian làm việc; xem [phần cài đặt](https://phishdestroy.github.io/TgWitness/vi/docs/reference/settings/).

Thanh trên cùng còn có:

- **Chuyển đến một phần** (Ctrl+K, hoặc ⌘K trên máy Mac): tìm một cuộc trò chuyện, một tham số hoặc một bản ghi nhật ký bằng cách `#number`. Các phím mũi tên để di chuyển, phím Enter để mở, phím Esc để đóng.
- **Thông báo**: các sự cố và thay đổi trong cuộc trò chuyện được xử lý từ nhật ký. **Chọn “Đánh dấu tất cả là đã đọc”** sẽ xóa số đếm, còn **“Quy tắc thông báo”** sẽ mở cửa sổ quy tắc. Việc gửi thông báo đến Telegram, Discord hoặc email được thiết lập trong [Phần bổ sung → Thông báo](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#notifications).
- Chỉ báo kết nối cho không gian làm việc này. **Trạng thái hoạt động của Collector** dưới thanh trên cùng được chia thành các phần: kết nối Telegram, thu thập sự kiện, nguồn dữ liệu và hàng đợi tệp đính kèm.
- **Khóa**: đóng bảng điều khiển trong trình duyệt này. Bộ sưu tập vẫn tiếp tục chạy trên máy chủ.
- Chế độ bảo vệ nằm bên cạnh số phiên bản; xem [các chế độ bảo vệ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#protection-modes).

Không gian làm việc demo chứa các tin nhắn giả định và không bao giờ kết nối với Telegram. Các thao tác có thể thay đổi không gian làm việc thực tế sẽ bị từ chối tại đây.

## Bắt đầu tại đây

Chọn một nhiệm vụ. **Tính năng “Xuất tài khoản của tôi”** sẽ tải xuống những nội dung mà tài khoản hiện có thể truy cập. **Tính năng “Theo dõi cuộc điều tra”** ghi lại các tin nhắn mới, các chỉnh sửa được quan sát và thông báo xóa từ các cuộc trò chuyện mà bạn chọn. Thẻ thiết lập hiển thị ba bước: kết nối tài khoản, chọn nguồn, bắt đầu quan sát. Câu hỏi mục tiêu sẽ vẫn hiển thị trên trang này cho đến khi bạn trả lời hoặc bỏ qua nó. Một không gian làm việc mới sẽ mở ra màn hình [thiết lập đầu tiên](https://phishdestroy.github.io/TgWitness/vi/docs/reference/settings/) thay thế.

## Cuộc trò chuyện

Các cuộc trò chuyện đã lưu, mặc định chỉ cho phép xem.

- Tìm kiếm trong danh sách theo tên hoặc ID. **Chọn** để thêm hoặc xóa các cuộc trò chuyện đang theo dõi. Tính năng “**Mở liên kết Telegram”** nhận tên người dùng hoặc liên kết mời và lưu bản xem trước vào nhật ký. Lệnh **“Tham gia / Mở và theo dõi**” sẽ tham gia vào cuộc trò chuyện và thêm nó vào danh sách nguồn của bạn; việc mở một bot sẽ gửi nó `/start`.
- Phần đầu trang cuộc trò chuyện thống kê các tin nhắn **đã bị xóa, văn bản được lưu giữ**, **tin nhắn bị xóa trước khi lưu** và **không tìm thấy khi kiểm tra lại**. Danh sách cuộc trò chuyện và thông báo sử dụng cùng các định nghĩa. Một tin nhắn đã bị xóa có màu đỏ và vẫn giữ nguyên văn bản đã lưu; một tin nhắn đã chỉnh sửa giữ lại mọi phiên bản đã lưu. Mỗi lần xóa đều ghi rõ những thông tin đã biết: thời điểm tin nhắn được xem, rằng Telegram không báo cáo ai là người đã xóa nó, hoặc rằng chỉ có thông báo được gửi đến.
- **Tính năng "Load history" (Tải lịch sử)** sẽ hiển thị 100, 250 hoặc 500 tin nhắn gần nhất trong giao diện này và trong nhật ký. Để tải toàn bộ lịch sử từ mọi nguồn đã bật, hãy chọn [Sources → Full history](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#sources).
- **Tính năng Xuất cuộc trò chuyện** sẽ tải xuống toàn bộ lịch sử hiển thị dưới dạng tệp đã được ký `chat.json` và `chat.html`. Một số tài khoản được kết nối có thể chia sẻ công việc: mỗi tài khoản tải xuống phạm vi số tin nhắn của riêng mình và ký xác nhận phần của mình, còn tài khoản khởi tạo quá trình xuất sẽ ký xác nhận tệp lưu trữ. Xem [hướng dẫn xuất một cuộc trò chuyện](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md).
- Danh sách **Người** hiển thị tất cả những người có tin nhắn được lưu trong cuộc trò chuyện này. Hồ sơ Người được tắt theo mặc định vì chúng là dữ liệu cá nhân về bên thứ ba. Khi được bật cho một cuộc trò chuyện, hồ sơ sẽ hiển thị tên và lịch sử tên người dùng, cờ Telegram, băm ảnh đại diện, hoạt động, ai trả lời ai, các cuộc trò chuyện khác được quan sát, cũng như ví, số điện thoại, tên người dùng và liên kết được đề cập. Mỗi thông tin đều trỏ đến bản ghi tương ứng. **Tính năng Xuất hồ sơ** sẽ lưu một tệp đã ký, tùy chọn bảo vệ bằng mật khẩu ZIP; việc tắt hồ sơ sẽ xóa tệp hồ sơ. Xem [hồ sơ người dùng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#people-profiles).
- **Tính năng "Lưu hồ sơ" hiện** ghi lại bản chụp nhanh của hồ sơ cuộc trò chuyện hoặc bot: mô tả, thành viên, liên kết mời, lệnh bot.

### Chế độ chỉ đọc, gửi tin nhắn và thông tin bí mật

Hai công tắc phía trên các tin nhắn giúp bảo vệ tài khoản và người đọc:

- **Chỉ đọc** được bật khi một cuộc trò chuyện được mở. Tắt tính năng này để gửi tin nhắn hoặc nhấn các nút bot . Mỗi hành động sẽ yêu cầu xác nhận qua **Gửi dưới dạng @tài_khoản?** hoặc **Nhấn nút bot này dưới dạng @account?**, thông báo cho bạn biết rằng các thành viên trong cuộc trò chuyện sẽ thấy thông báo này và nó sẽ được ghi vào nhật ký đã được ký. **Không hỏi lại trong vòng 10 phút trong cuộc trò chuyện này** sẽ bỏ qua yêu cầu xác nhận trong một thời gian. Tính năng gửi tin nhắn bị tắt đối với mục tiêu **Bằng chứng cho một vụ án**, cả trong bảng điều khiển và trong API.
- **Tính năng "Mask secrets"** ẩn đi những thông tin trông giống như mật khẩu, mã đăng nhập, khóa API hoặc băm (hash), token bot, chuỗi phiên, khóa riêng tư, JWT hoặc số thẻ thanh toán (số thẻ thanh toán được kiểm tra bằng tổng Luhn). **Tính năng "Show"** hiển thị một giá trị; việc hiển thị này được ghi lại trong nhật ký. Việc tắt tính năng ẩn thông tin cho trình duyệt này cũng được ghi lại. Chỉ nội dung hiển thị bị thay đổi: các bản ghi gốc và mọi bản xuất vẫn giữ nguyên văn bản đầy đủ.

## Sổ ghi chép

Tất cả các bản ghi mà không gian làm việc đã ký, sắp xếp theo thứ tự từ mới nhất đến cũ nhất.

- **Tổng quan** thống kê số tin nhắn được theo dõi, số lần chỉnh sửa được ghi lại, thông báo xóa và các nguồn được chọn.
- **Dòng thời gian sự kiện** lọc theo loại sự kiện (tất cả, chỉnh sửa, xóa, phản hồi, thành viên, phạm vi phủ sóng), theo văn bản và theo nguồn. **Tải các sự kiện trước đó** quay lại trang trước.
- Mở một bản ghi để xem chi tiết, mã băm và nội dung của nó. **Liên kết đến bản ghi này** là một địa chỉ mở cùng bản ghi đó. Các thông tin bí mật có thể có sẽ được che đi trong bản xem trước này; các tệp xuất vẫn giữ nguyên bản gốc.
- Nhật ký chỉ cho phép ghi thêm: không có thao tác nào trên bảng điều khiển có thể chỉnh sửa hoặc xóa bản ghi. Kiểm tra bằng cách chọn **Xuất → Xác minh nhật ký** hoặc `python -m tgwitness.verify`; xem [phần xuất và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/).

## Nguồn

Không gian làm việc này ghi lại những cuộc trò chuyện nào và lưu giữ những thông tin gì từ các cuộc trò chuyện đó. Các thay đổi sẽ áp dụng cho các hoạt động trong tương lai; các bản ghi đã lưu vẫn được giữ nguyên.

**Tính năng Refresh chat list** đọc các cuộc trò chuyện và thư mục của tài khoản. Tính năng này không tải xuống tin nhắn.

### Phạm vi

- **Những nội dung mà tài khoản này ghi lại** : **Các cuộc trò chuyện đã chọn** (chỉ các cuộc trò chuyện bạn thêm vào), **Thư mục Telegram** (một trong các thư mục của tài khoản, bao gồm cả các cuộc trò chuyện được thêm vào sau này) hoặc **Toàn bộ tài khoản** (mọi cuộc trò chuyện, cũng như mọi cuộc trò chuyện mới, nhóm, cuộc trò chuyện riêng tư hoặc bot ngay khi chúng xuất hiện). **Chế độ điều tra** dành cho một tài khoản chuyên dụng: nó ghi lại mọi thứ mà tài khoản đó nhìn thấy, các tin nhắn và thao tác nhấn nút của chính tài khoản đó, đồng thời lưu ngay lập tức hồ sơ của mỗi cuộc trò chuyện mới cùng các tin nhắn đã hiển thị trước đó. Hình [hướng dẫn dành riêng cho tài khoản](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) giải thích lý do tại sao không bao giờ nên sử dụng tài khoản chính của bạn.
- **Các loại nguồn** giới hạn chế độ thư mục và chế độ toàn tài khoản cho các kênh, nhóm, cuộc trò chuyện riêng tư và bot. **Các hành động của chính mình** thêm các tin nhắn, thao tác chỉnh sửa và các lần nhấn phím trả lời của chính tài khoản đó.
- **Khi có cuộc trò chuyện hoặc bot mới xuất hiện**: lưu hồ sơ của nó và tối đa số lượng tin nhắn mới nhất hiển thị đã chọn.

Giới hạn: các cuộc trò chuyện bí mật không bao giờ được ghi lại TgWitness. Không có dữ liệu nào được ghi lại khi TgWitness không đang chạy; sau khi khởi động lại, công cụ chỉ ghi lại những gì Telegram vẫn trả về, và báo cáo sẽ hiển thị khoảng trống đó. Các cuộc trò chuyện vượt quá giới hạn danh sách trò chuyện (1.000 cuộc đối thoại trừ khi được thay đổi trong Tham số) sẽ được thêm vào khi chúng hoạt động trở lại. Các nút bot nhúng được nhấn trong một ứng dụng khác sẽ không hiển thị; phản hồi của bot sẽ được ghi lại.

### Các cuộc trò chuyện trong phạm vi

Lọc theo trạng thái (**Đã bật**, **Đã tạm dừng**, **Ưu tiên**, **Đã loại trừ**, **Chưa xác nhận quyền truy cập**, **Đã bỏ qua**) và loại, sau đó thực hiện hành động trên phần đã chọn: bật, tạm dừng, đánh dấu hoặc xóa ưu tiên, loại trừ khỏi phạm vi hoặc xóa. Biểu tượng trạng thái chỉ hiển thị tình trạng; các hành động nằm trong menu của mỗi hàng kèm theo dòng mô tả chức năng của chúng. Việc tạm dừng và loại trừ sẽ yêu cầu xác nhận, kể cả khi thực hiện hàng loạt. Việc xóa một nguồn sẽ yêu cầu nhập tên của nguồn đó và xóa các hồ sơ cá nhân liên quan; các bản ghi đã lưu của nguồn đó vẫn được giữ lại trong nhật ký.

Một nguồn mà danh sách trò chuyện của tài khoản không hiển thị đang **nhận được cập nhật, không có trong danh sách trò chuyện**trong khi các bản ghi vẫn tiếp tục đến; nếu không, **quyền truy cập chưa được xác nhận**. **Tính năng "Trò chuyện có sẵn"** cho phép thêm các cuộc trò chuyện bằng cách chọn **"Thêm đã chọn**" hoặc **"Thêm tất cả các cuộc trò chuyện phù hợp**".

### Lịch sử đầy đủ

Tải lịch sử có sẵn của mọi nguồn đã bật vào phần Trò chuyện và nhật ký. Tiến trình được giữ nguyên sau khi khởi động lại; tệp đính kèm tuân theo cài đặt phương tiện của bạn. Xem [lịch sử nguồn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/history/).

### Ghi lại

- **Chọn những thay đổi cần lưu giữ**: tin nhắn mới, chỉnh sửa, thông báo xóa, phản ứng hiển thị, tham gia và rời khỏi. Một cài đặt sẵn sẽ thay đổi biểu mẫu; **Lưu cài đặt ghi lại** sẽ áp dụng cài đặt đó. Việc bật lại một danh mục sẽ không khôi phục các sự kiện đã bỏ lỡ.
- **Lưu giữ phương tiện khi có sẵn**: tải xuống tệp đính kèm với kích thước tối đa cho mỗi tệp, thiết lập theo từng loại từ 1 đến 2.000 MiB và giới hạn độ dài video tính bằng giây (0 có nghĩa là không giới hạn). Mỗi lần thử tải xuống đều được ghi lại kết quả.
- **Kiểm tra lại**: kiểm tra các cuộc trò chuyện ưu tiên vài phút một lần, các cuộc trò chuyện khác thì hiếm khi, để tài khoản không bị vượt quá giới hạn FloodWait của Telegram. Nhập 0 để tắt nhóm. Đánh dấu các cuộc trò chuyện ưu tiên bằng dấu sao trong danh sách; số lượng cuộc trò chuyện mỗi lần kiểm tra và khoảng thời gian tạm dừng giữa các cuộc trò chuyện được thiết lập trong Phần Thông số. Xem [bộ sưu tập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/).

## Xuất dữ liệu

**Tải xuống** chuẩn bị các tệp; **Báo cáo xây dựng** chọn cách hiển thị của các báo cáo.

| Nội dung | Sử dụng nó để | Hướng dẫn |
| --- | --- | --- |
| Xuất tài khoản | Một bản chụp nhanh mới nhất về những nội dung mà tài khoản có thể đọc được hiện tại | [Xuất tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/account-export/) |
| Chia sẻ bản sao | Một phiên bản thu gọn của tệp xuất tài khoản đã hoàn tất | [Thông báo](https://phishdestroy.github.io/TgWitness/vi/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| Đã ký ZIP | Nhật ký, báo cáo, tệp đính kèm và các công cụ xác minh tại một ranh giới nhật ký cố định | [Xuất và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/) |
| Báo cáo định dạng HTML, PDF, JSON | Một báo cáo có thể đọc được và được niêm phong | [Báo cáo trường hợp](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-reports/) |
| JSONL, CSV | Bản ghi gốc có chữ ký; bảng tính an toàn với công thức | [Xuất và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/) |
| Trích đoạn bàn giao | Chỉ các cuộc trò chuyện, khoảng thời gian và những người mà người nhận cần | [Bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#investigation-handoff) |
| Xuất nội dung trò chuyện | Một cuộc trò chuyện đã được ký `chat.json` và `chat.html` | [Xuất một cuộc trò chuyện](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **Việc mã hóa các tệp tải xuống ở trên bằng mật khẩu** (tối thiểu 12 ký tự) sẽ tạo ra một tệp AES-256 ZIP mà 7-Zip hoặc WinRAR có thể mở được. Tệp đã được ký bên trong vẫn giữ nguyên. Mật khẩu không được lưu trữ.
- **Các tệp xuất đã chuẩn bị** lưu trữ tối đa 20 tệp trong phạm vi 2 GiB, cộng với tệp mới nhất, để tải xuống lặp lại, mỗi tệp đều có thẻ SHA-256. Việc chuẩn bị tệp không đảm bảo việc giao nhận.
- Khi trình duyệt từ chối hiển thị hộp thoại lưu, bảng điều khiển sẽ chuyển sang chế độ tải xuống thông thường.
- **Danh tính ký của bạn** hiển thị dấu vân tay khóa. **Lưu điểm kiểm tra** và Tải xuống **biên nhận chạy đã ký** cung cấp cho bạn các bản ghi để lưu trữ bên ngoài bộ thu thập. Chuẩn bị **yêu cầu dấu thời gian** tạo ra một yêu cầu RFC 3161 mà không cần liên hệ với bất kỳ dịch vụ nào.

## Cài đặt, tài khoản và kết nối

- **Cài đặt**: mục tiêu, kết nối, nội dung cần ghi lại và giao diện. Xem [hướng dẫn thiết lập ban đầu và cài đặt](https://phishdestroy.github.io/TgWitness/vi/docs/reference/settings/).
- **Tài khoản**: mỗi không gian làm việc với trạng thái, nguồn, sự kiện và hàng đợi tệp đính kèm của nó. Lọc theo **Cần chú ý**, **Thu thập**, **Ngoại tuyến hoặc tạm dừng** hoặc **Chưa kết nối**, tạm dừng hoặc tiếp tục một lựa chọn, nhập hàng loạt tệp tài khoản và quản lý các nhóm. Xem [tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/).
- **Tài khoản**: đăng nhập và đường dẫn kết nối của tài khoản này. Trực tiếp, một cấu hình WireGuard , proxy của riêng bạn, nhóm MTProto công cộng hoặc WARP; chuẩn bị và kiểm tra đường dẫn, sau đó áp dụng nó cho tài khoản này, một nhóm hoặc tất cả các tài khoản. Xem [phần kết nối và proxy](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/)[.](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md)

## Tính năng bổ sung

Tùy chọn: chỉ cần một tài khoản và các nguồn là đủ để bắt đầu thu thập. Chỉ tùy chọn mà bạn chọn mới mở cài đặt của nó, và không có gì được kết nối tự động. Thẻ **“Mức độ bảo vệ**” ở phía trên hiển thị chế [độ bảo vệ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#protection-modes).

| Thẻ | Tính năng mới | Hướng dẫn |
| --- | --- | --- |
| Lưu trữ & dung lượng đĩa | Sao lưu, di chuyển các tệp cũ lên đám mây của bạn, một bản sao bằng chứng không thể bị xóa | [Lưu trữ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/storage/) |
| Mục tiêu & mức độ bảo mật | Các cài đặt được đề xuất cho mục tiêu và hai thang đo của bạn | [dưới đây](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#goal-and-protection-level) |
| Thông báo | Các vấn đề, tin nhắn đã thay đổi và bản tóm tắt hàng ngày; bot điều khiển của riêng bạn | [dưới đây](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#notifications) |
| Bằng chứng & bản sao lưu | Dấu thời gian, thêm các nhân chứng và bản sao được mã hóa lưu trữ ngoài hệ thống | [dưới đây](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#evidence-and-backups) |
| Máy chủ hoạt động 24/7 | Một máy chủ đám mây không hỗ trợ SSH, được tạo và xóa trực tiếp từ bảng điều khiển | [Độ tin cậy cao](https://phishdestroy.github.io/TgWitness/vi/docs/reference/high-assurance/#from-the-panel) |
| Nhân chứng độc lập | Các bản kiểm tra đã được ký sẽ được đăng lên kênh Telegram hoặc Discord của bạn | [Witness](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/) |
| Kiểm tra mã nguồn | So sánh chương trình đang chạy với một commit công khai trên GitHub | [dưới đây](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/#code-check) |

### Mục tiêu và mức độ bảo mật

Bốn câu hỏi:

1. **Công cụ này dùng để làm gì?** Để lưu trữ hồ sơ cá nhân, phục vụ công tác điều tra hoặc làm bằng chứng cho một vụ việc.
2. **Bạn sẽ theo dõi bao nhiêu?** Một vài cuộc trò chuyện (tối đa khoảng 50), nhiều cuộc trò chuyện (tối đa khoảng 500) hoặc toàn bộ tài khoản. Điều này sẽ đặt giới hạn danh sách cuộc trò chuyện thành 1.000, 3.000 hoặc 20.000.
3. **Ảnh và tệp tin?** Chỉ văn bản, ảnh và phương tiện truyền thông ngắn (ảnh 20 MB, video 100 MB), hoặc tất cả (video và tài liệu tối đa 1 GB mỗi loại). Tùy chọn “Tất cả” với tài khoản đầy đủ cũng giữ lại 4 GiB dung lượng đĩa trống.
4. **Nó sẽ chạy ở đâu?** Trên máy tính này hoặc trên một máy chủ luôn hoạt động.

Phần đề xuất liệt kê các dấu thời gian độc lập, drand và danh sách thiết bị của Telegram, mỗi mục đều kèm theo một dòng mô tả về chức năng của nó. Dấu thời gian được tạo mỗi 60, 30 hoặc 10 phút cho bản ghi cá nhân, cuộc điều tra hoặc bằng chứng; drand và danh sách thiết bị cần có dấu thời gian. Chỉ **áp dụng** các thay đổi này, chính sách tệp đính kèm và hai tham số ở trên. Mỗi thay đổi là một bản ghi nhật ký, cộng với `setup.applied`. Thông báo, bản sao ngoài trang web, máy chủ, Gateway DNS, kiểm tra mã và nhân chứng được đề xuất làm các bước tiếp theo với các biểu mẫu riêng.

Hai thang đo được tính toán dựa trên các thiết lập hiện tại, chứ không phải dựa trên mục tiêu:

| Quy mô | Điểm |
| --- | --- |
| Độ tin cậy | Nhật ký đã ký 1, dấu thời gian 3, drand 1, danh sách thiết bị 1, kiểm tra mã khớp 1, thăm dò chứng nhân 1, máy chủ được xác thực 2, nhật ký DNS Gateway 1 |
| Độ tin cậy | Máy chủ luôn hoạt động 3, bản sao ngoài cơ sở 3, Object Lock 1, thông báo sự cố 1 |

Tỷ lệ đọc **tối đa** 80% trở lên, 50% **là cao**, 25% **là trung bình**, dưới mức đó **là cơ bản**. Độ tin cậy hiện được tính dựa trên máy chủ luôn hoạt động theo câu trả lời cho câu hỏi 4, trước khi kiểm tra bất kỳ máy chủ nào.

### Thông báo

Các thông báo được gửi qua Apprise đến Telegram, Discord, Slack, ntfy, email, Matrix và hơn 100 dịch vụ khác. Chọn một dịch vụ, điền vào một hoặc hai trường và gửi thử nghiệm, hoặc dán trực tiếp các địa chỉ Apprise.

- **Các sự cố**: đĩa gần đầy, tài khoản bị đăng xuất, lỗi liên quan đến bộ sưu tập, sao chép hoặc dấu thời gian . Trên máy chủ được niêm phong, cổng SSH mở hoặc việc đăng nhập cũng là một vấn đề.
- **Thay đổi**: các tin nhắn đã xóa, đã chỉnh sửa và bị thiếu trong các cuộc trò chuyện được theo dõi, được nhóm lại thành một thông báo cho mỗi lần kiểm tra (mỗi phút trừ khi được thay đổi trong phần Cài đặt).
- **Các tác vụ đã hoàn thành**: lịch sử, xuất dữ liệu và bản sao lưu.
- **Tóm tắt hàng ngày** vào giờ đã chọn, theo giờ máy chủ.

Các thông báo hiển thị tên cuộc trò chuyện và số lượng tin nhắn. Trích đoạn tin nhắn bị tắt theo mặc định; khi bật tính năng này, nội dung tin nhắn sẽ được gửi ra khỏi máy này.

**Bot điều hành của bạn** là bot do chính bạn tạo từ @BotFather, có chức năng trả lời `/status` và `/stats`, và tùy chọn `/pause`, `/resume` và `/copy`. Chỉ các cuộc trò chuyện và ID người dùng Telegram được liệt kê mới có thể sử dụng nó; nội dung cuộc trò chuyện được lưu trữ trong không gian làm việc. Sử dụng một bot riêng nếu một ứng dụng khác đã nhận các lệnh của nó. Xem [phần thông báo](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md) và [bot điều hành](https://phishdestroy.github.io/TgWitness/vi/docs/reference/storage/#operator-bot-and-completion-notices).

### Bằng chứng và bản sao lưu

- **Các dấu thời gian độc lập** chỉ gửi phần SHA-256 của mỗi điểm kiểm tra đã được ký đến các cơ quan RFC 3161 và lịch OpenTimestamps, cứ sau 5 đến 1.440 phút. **Anchor hiện** đang chạy một vòng. Xem [các dấu thời gian](https://phishdestroy.github.io/TgWitness/vi/docs/reference/timestamp/).
- **Các bản ghi khác**, mỗi bản đều bị tắt cho đến khi được chọn: vòng drand mới nhất, danh sách các thiết bị đã đăng nhập của Telegram (không kèm địa chỉ IP) và nhật ký các truy vấn DNS của máy chủ từ Cloudflare Gateway. Xem [các bản ghi tùy chọn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices).
- **Bản sao lưu được mã hóa** sẽ sao chép nhật ký, tệp tin, điểm kiểm tra và bản xuất cuộc trò chuyện vào bộ lưu trữ tương thích với S3 (Wasabi, Amazon S3, Backblaze B2, Cloudflare R2, MinIO). Mọi thứ đều được mã hóa trên máy này trước tiên. **Tải xuống khóa mã hóa** và lưu giữ nó riêng biệt: nếu không có khóa này, bản sao sẽ không thể đọc được. Chức năng Object Lock ở chế độ Quản trị hoặc Tuân thủ ngăn không cho các đối tượng bị xóa trong một số ngày nhất định. Xem [bản sao ngoài trang web](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md).

### Kiểm tra mã nguồn

Kiểm tra xem chương trình đã cài đặt có khớp với phiên bản đã phát hành hay không.

1. Nhập tên kho lưu trữ GitHub (kho chính thức đã được điền sẵn) và một thẻ, nhánh hoặc bản cam kết.
2. **Check now** truy vấn API của GitHub, thông qua đường dẫn dành cho các yêu cầu từ bên ngoài của không gian làm việc này, để lấy danh sách tệp của commit đó. Nó so sánh ID blob git của mỗi tệp chương trình được đo lường với commit. Một bản checkout trên Windows với các ký tự kết thúc dòng đã được chuyển đổi vẫn khớp.
3. Kết quả liệt kê các tệp đã thay đổi, thêm mới và thiếu (tối đa 50 tệp cho mỗi loại) và được lưu dưới dạng một `source.checked` bản ghi nhật ký.

Kết quả chỉ được coi là cập nhật khi các tệp chương trình đang chạy không thay đổi: hãy kiểm tra lại sau khi cập nhật. Không cần mã thông báo và chỉ các kho lưu trữ công khai mới hoạt động; các cuộc trò chuyện và thông tin đăng nhập không được tải lên. Một kết quả khớp xác định mã trên đĩa. Đây không phải là chứng thực phần cứng; để biết thêm về điều này, hãy xem [Phala Cloud](https://phishdestroy.github.io/TgWitness/vi/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx).

## Các chế độ bảo vệ

Nút chuyển đổi bên cạnh số phiên bản hiển thị chế độ đã chọn và số lượng trong số 18 lớp bảo vệ đang hoạt động, ví dụ `🟠 Witnessed 9/18`. **Để thay đổi chế độ** trong **“Extras → Protection level”** sẽ mở ra menu lựa chọn. Mỗi chế độ mô tả một mục tiêu cụ thể và liệt kê những gì vẫn còn thiếu; quá trình ghi lại, ký xác thực và cài đặt đã lưu đều giống nhau ở mọi chế độ.

| Chế độ | Dành cho | Thêm |
| --- | --- | --- |
| 🟢 Dễ dàng | Theo dõi một cuộc trò chuyện và lưu giữ bản sao | Các cuộc trò chuyện, nhật ký và bản xuất cuộc trò chuyện; quá trình ký diễn ra ở chế độ nền |
| 🟡 Đã ký | Báo cáo lên nền tảng, máy chủ hoặc bộ phận xử lý vi phạm | Tập tin lưu trữ đã ký, kiểm tra nhật ký, điểm kiểm tra, bản trích xuất bàn giao |
| 🟠 Đã được chứng thực | Các trường hợp mà ai đó có thể khẳng định bản ghi đã bị thay đổi | Một nhân chứng độc lập đăng các tiêu đề nhật ký đã được ký |
| 🔴 Sẵn sàng cho phiên tòa | Bằng chứng dành cho luật sư, cảnh sát hoặc tòa án | Dấu thời gian, bản sao được mã hóa lưu trữ ngoài hệ thống, chi tiết vụ việc trong các báo cáo |
| 🟣 Được xác minh bởi GitHub | Các bản ghi mà bất kỳ ai cũng phải có thể kiểm tra phần mềm của chúng | Kiểm tra mã nguồn và ghi lại các hành động trên GitHub |
| ⚫ Mossad | Các vụ án có mức độ rủi ro cao chống lại một đối thủ có nguồn lực dồi dào | Một máy chủ được bảo mật 24/7, địa chỉ IP ẩn, tất cả 18 lớp bảo mật |

Các lớp: mọi bản ghi đều được ký và liên kết; biên nhận chạy đã ký; tệp đính kèm được lưu với SHA-256; các điểm kiểm tra đã ký; kiểm tra lại; cảnh báo sự cố; quyền truy cập chứng nhân chỉ đọc; một chứng nhân kiểm tra theo lịch trình; dấu thời gian RFC 3161; bằng chứng OpenTimestamps; một dấu thời gian mới nhất đã được xác minh; một bản sao được mã hóa tại vị trí ngoài; chi tiết vụ việc trong báo cáo; kiểm tra mã khớp; Telegram không bao giờ nhìn thấy địa chỉ IP của máy này; các yêu cầu từ bên ngoài thông qua proxy; Khóa đối tượng trên bản sao; một máy chủ được niêm phong chứa các bản ghi của nhà cung cấp. Một lớp đang tắt có tùy chọn **“Set up**”, mở biểu mẫu của nó. Chọn chế độ thấp hơn sẽ yêu cầu xác nhận và không xóa bất cứ thứ gì.

## Các công cụ khác

**Extras → Independent capture**: connect a separate browser or AyuGram recorder, pin its signing key, select capture options, start/pause, take snapshots and download verified signed archives. Each recorder has its own manual login, route, journal and key. Both connections start disabled. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md).

- **Tra cứu kho lưu trữ**: tìm kiếm các quan sát đã lưu, xem lại các nguồn, sau đó quyết định liệu có nên gửi chúng đến mô hình AI hay không. Xem [phân tích kho lưu trữ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/analysis/) và [chức năng OCR và phiên âm cục bộ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/media-analysis/).
- **Các tham số**: giới hạn và tốc độ thu thập, kiểm tra lại, tải xuống, hồ sơ, thông báo và xuất dữ liệu. Tìm kiếm theo tên, hiển thị các giá trị **Chỉ các thông số đã thay đổi** và chuẩn bị các giá trị mặc định dưới dạng bản nháp bằng **Khôi phục mặc định…**. **Lưu các tham số** áp dụng các giá trị từ lần sử dụng tiếp theo, và mỗi thay đổi đều được ghi lại dưới dạng bản ghi nhật ký.
- **Quyền truy cập**: các mã thông báo riêng biệt dành cho người đánh giá, nhà phân tích và người vận hành, giới hạn trong các không gian làm việc, cuộc trò chuyện và quyền hạn đã chọn. Xem [phần quyền truy cập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/).
- **Nhật ký hệ thống** : các hoạt động mà quá trình này đã thực hiện kể từ khi bắt đầu (kết nối, thay đổi proxy, đăng nhập, từ chối, thay đổi cài đặt) với địa chỉ IP được ẩn. Tính năng **“Theo dõi dòng mới”** giúp luôn hiển thị dòng mới nhất. Các tin nhắn chỉ được lưu trong nhật ký.
- **Tích hợp**: nhà cung cấp AI, kết nối [MCP chỉ đọc](https://phishdestroy.github.io/TgWitness/vi/docs/reference/mcp/) và [webhook đã ký](https://phishdestroy.github.io/TgWitness/vi/docs/reference/webhooks/).
- **Case Board**: ghi chú riêng tư của nhóm, dấu trang và các đoạn trích bên cạnh bằng chứng. Xem [Case Board](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-board/).
- **GitHub Actions ghi lại** trong mục Xuất: một cuộc trò chuyện được ghi lại từ bản fork của bạn. Xem [bản ghi được niêm phong](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md).
