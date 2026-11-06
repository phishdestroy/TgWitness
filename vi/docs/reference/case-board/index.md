# Tham chiếu Case Board

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-board/

Dấu trang, phần đánh dấu chính xác, các đoạn hành động, cuộc thảo luận, quyền truy cập có phạm vi và lịch sử chú thích đã ký được sử dụng bởi Case Board.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Điều tra](https://phishdestroy.github.io/TgWitness/vi/docs/reference/investigation/)

![Điều tra](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

Case Board cung cấp cho đội điều tra một giao diện làm việc chung về các tài liệu đã lưu. Đánh dấu một quan sát, làm nổi bật một đoạn văn bản cụ thể, lưu lại một chuỗi hành động và thảo luận với đồng nghiệp. Các thẻ (Cards) giữ nguyên tham chiếu nguồn và lịch sử sửa đổi đã ký. Các chú thích của đội vẫn nằm trong không gian làm việc, có thể phân biệt riêng biệt với các quan sát gốc trên Telegram.

[Mô hình bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/) · [Truy cập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/) · [Báo cáo](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-reports/)

![Nguồn cấp dữ liệu điều tra tổng hợp](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

**Trên trang này**

- [Làm việc với một trường hợp](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-board/#work-with-a-case)
- [Quyền truy cập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-board/#permissions)
- [Hợp đồng được lưu trữ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-board/#stored-contracts)
- [API và các định dạng xuất](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-board/#api-and-exports)
- [Giới hạn hoạt động](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-board/#operating-limits)

## Làm việc với một vụ việc

Mở **Investigation → Case Board** ở chế độ Standard hoặc Expert. Ngôn ngữ sẽ tự động điều chỉnh theo bảng điều khiển. Sử dụng **nút** **“To board”** bên cạnh bản ghi nhật ký hoặc tin nhắn trò chuyện đã lưu, hoặc chọn nó làm tiêu điểm và nhấn **phím** **B**. Dấu trang sẽ được thêm vào Hộp thư đến chỉ với một cú nhấp chuột. Chỉnh sửa tiêu đề, nhãn và ghi chú của nó, hoặc di chuyển nó vào một bộ sưu tập. Thẻ đã thay đổi sẽ thêm một bản sửa đổi có chữ ký; việc xóa nó sẽ giữ lại lịch sử.

Đối với trường hợp đầu tiên, hãy chọn một bộ sưu tập và thêm các bản ghi trả lời một câu hỏi. Sử dụng phần bình luận để xem xét cách diễn giải, sau đó dùng **phần Trình bày** để xem xét các thẻ và bối cảnh nguồn. Chọn tài liệu Bảng vụ án riêng biệt trong [Report Studio](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-reports/) khi chuẩn bị bản báo cáo. Việc lưu một phần dữ liệu không tự động cấu hình các bộ lọc dữ liệu của báo cáo.

Chọn văn bản bên trong một tin nhắn trò chuyện đã lưu để hiển thị **Highlight → board**. Chọn màu sắc và thêm ghi chú. Máy chủ kiểm tra trích dẫn chính xác và phiên bản đã lưu, bao gồm biểu tượng cảm xúc, văn bản RTL và dấu kết hợp. Giao diện không ánh xạ vùng chọn qua văn bản bị che khuất hoặc biến đổi.

Nhấn Shift và nhấp vào hai bản ghi trong một cuộc trò chuyện để tạo **"Slice" giữa chúng**, sử dụng **"Slice" theo thời gian**, hoặc lưu các bộ lọc hiện tại của Journal về cuộc trò chuyện, khoảng thời gian và loại sự kiện. Một "Slice" đã lưu có điều kiện xác định riêng của nó: việc mở nó trong Journal cũng áp dụng các cuộc trò chuyện đa dạng, giới hạn số tin nhắn và bộ lọc người tham gia . **Tính năng “Hiển thị các bản ghi được thêm kể từ khi đánh dấu trang”** sẽ tách riêng các bản ghi được thêm sau đó. Việc thay đổi các bộ lọc trong Journal sẽ thoát khỏi phần cắt. Từ mục “Người dùng”, **tính năng “Cắt các hành động của người này”** sử dụng ID tác nhân đã được ghi lại; nó không giả định rằng tác giả tin nhắn đã chỉnh sửa, xóa hoặc phản hồi tin nhắn đó.

Hộp thoại "Slice" hiển thị số lượng bản ghi trước khi cho phép tạo. "`all`" bao gồm mọi loại bản ghi, bao gồm ảnh chụp màn hình, chỉnh sửa, xóa, phản hồi, cập nhật thành viên/dịch vụ, hành động của chính người dùng, nút bấm, kết quả phương tiện, tin nhắn được khôi phục và các loại sự kiện trong tương lai. Lựa chọn này mô tả các quan sát đã lưu. Các thông báo xóa cuộc trò chuyện không xác định là bối cảnh riêng biệt, chỉ khả dụng đối với quyền truy cập toàn bộ không gian làm việc, không bao giờ được gán cho một trong các cuộc trò chuyện đã chọn.

Các bộ sưu tập có phạm vi trò chuyện được khai báo. Phạm vi trống có nghĩa là toàn bộ không gian làm việc. Một bộ sưu tập không thể chứa các thẻ nằm ngoài phạm vi của nó; người tham gia bị giới hạn trong một cuộc trò chuyện không thể đọc một bộ sưu tập có phạm vi rộng hơn. Hộp thư đến là một bộ sưu tập ảo dành cho các thẻ chưa được phân công. Tính năng tìm kiếm và bộ lọc chỉ áp dụng cho các thẻ hiển thị; các chuỗi thảo luận và đề cập kế thừa quyền truy cập từ thẻ cha. Các bình luận đã xóa sẽ có biểu tượng "tombstone" trong cuộc thảo luận. Lịch sử xem không được ghi lại.

**Chế độ trình bày** mở tất cả các thẻ trong bộ sưu tập đã chọn, với các chế độ xem Thẻ, Bối cảnh nguồn và Bình luận của nhóm cùng các phím điều hướng Trước/Tiếp theo trên bàn phím. Chế độ này không cung cấp các công cụ chỉnh sửa. Dòng tin thông thường được chia trang; chế độ trình bày tải danh sách theo từng trang và hiển thị chi tiết của một thẻ tại một thời điểm.

## Quyền truy cập

Tất cả các thao tác đều yêu cầu quyền truy cập `view`, phạm vi không gian làm việc/trò chuyện và `board.read`. `board.write` cho phép thêm thẻ, bình luận, di chuyển và thay đổi trạng thái "mở"/"đang xem xét". `board.manage` cho phép quản lý bộ sưu tập, trạng thái "đã xác nhận"/"đã từ chối", cũng như chỉnh sửa hoặc xóa thẻ của người khác. Trạng thái là quyết định của nhóm, không phải kết quả xác minh mật mã.

Cài đặt sẵn biểu mẫu truy cập: Người xem xét = chỉ đọc; Nhà phân tích = đọc/ghi; Người vận hành = đọc/ghi/quản lý, bên cạnh các quyền hiện có của họ. Các quyền hiện có không tự động mở rộng sang các quyền mới. Quản trị viên chính có tất cả các quyền và đăng bài với tư cách là **Quản trị viên chính**. Sử dụng các quyền được đặt tên để ghi nhận nguồn. Danh sách đề cập chỉ bao gồm các quyền truy cập hiện tại có thể đọc toàn bộ thẻ cha.

Một quyền truy cập vào cuộc trò chuyện A không thể lấy được thẻ hoặc phần dữ liệu cho A+B, ngay cả khi đoán ID của nó hoặc cung cấp một `target.chat_id` sai. Siêu dữ liệu mục tiêu được xác định từ hàm băm sự kiện đã ký trên máy chủ. Các bộ sưu tập, số lượng thảo luận, thẻ liên quan và thông báo trực tiếp được lọc trước khi trả lời. Việc xuất dữ liệu yêu cầu quyền “`export`” cũng như “`board.read`”; một trình xuất hiện có sẵn nhưng không có quyền truy cập bảng sẽ nhận được kho lưu trữ bằng chứng thông thường mà không có ghi chú của nhóm. SSE sẽ kiểm tra lại các quyền hiện tại trước mỗi đợt xử lý.

## Hợp đồng được lưu trữ

Giống như các quan sát, các chú thích được ghi theo từng giao dịch vào một bảng SQLite chỉ ghi thêm trong không gian làm việc. `annotations.jsonl` là tệp xuất chuẩn chính xác từ cùng một bản chụp đọc như `events.jsonl`. Không có kho lưu trữ chú thích thứ hai cạnh tranh và không có sự kiện nhật ký `board.activity`.

Mỗi dòng phải chứa chính xác:

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

Ví dụ viết tắt ở trên minh họa phần bao bì; các tải trọng thực tế bao gồm các giá trị mặc định của mô hình và các trường đích được máy chủ giải quyết. Các lược đồ yêu cầu API nằm trong thư mục [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json), được tạo ra từ các mô hình Pydantic thời gian chạy bằng công cụ `python tools/build_board_schemas.py`. Các trường yêu cầu bổ sung sẽ bị từ chối. Các ID được tạo ra phía máy chủ khi bị bỏ trống. Tác giả, thời gian, ảnh chụp nhanh và chữ ký không thể được cung cấp bởi người gọi. Các ID cấp quyền có tên tuân theo định dạng 16 ký tự hex hiện có của Access; ID thẻ là 32 ký tự hex.

JSON chuẩn là UTF-8, các khóa đối tượng được sắp xếp theo thứ tự, không có khoảng trắng giữa các token, Unicode không được thoát, và không có NaN/vô cực. Băm chú thích là SHA-256 của đối tượng chuẩn chứa định dạng `format: "tgwitness-annotations-v1"` và tất cả bảy trường bao bọc cho đến `previous_hash`. Thẻ định dạng này tách miền băm của nó khỏi các quan sát. Chữ ký là Ed25519 trên 32 byte băm thô. Dãy bắt đầu từ 1. Các bản sửa đổi giữ nguyên ID thẻ và đặt tên cho băm chú thích trước đó trong trường "`supersedes`"; chúng không thể thay đổi phạm vi trò chuyện. Việc di chuyển, trạng thái và xóa là các bản ghi riêng biệt. Bảng SQLite từ chối các lệnh UPDATE và DELETE.

`case-board.json` chứa `{statement, signature}`. Tuyên bố chuẩn được ký bởi khóa không gian làm việc và chứa `format: "tgwitness-case-board-v1"`, `public_key`, `created_at`, `journal_head`, `meaning` và `state`. Trạng thái là tái phát xác định: `annotations_head`, một mảng `items` được sắp xếp theo thứ tự (bộ sưu tập, thẻ, bình luận bao gồm các mục đã xóa) và `status_history`. Các mục giữ lại băm chú thích cuối cùng, thứ tự, tác giả và thời gian, cũng như người tạo ban đầu và thời gian tạo qua các phiên bản sửa đổi. Quá trình phát lại kiểm tra các phiên bản sửa đổi, các mục cha, tham chiếu bộ sưu tập và ID hành động trùng lặp. Tệp ``manifest.json`` và các điểm kiểm tra mới cũng liên kết ``annotations_head``. Giữ lại một điểm kiểm tra một cách độc lập để phát hiện việc cắt bớt hoặc viết lại bằng khóa ký đã sao chép.

### Phiên bản văn bản

`range.start` là độ lệch điểm mã Unicode bắt đầu từ 0, `length` là số đếm điểm mã dương, và `quote` phải bằng chính xác chuỗi con của `payload.text` hoặc `payload.caption` tại sự kiện mục tiêu. Không áp dụng NFC/NFKC, chuyển đổi chữ hoa/thường hoặc chuẩn hóa grapheme. Các đoạn chuỗi trong Python và phương thức ``Array.from(text)`` trong JavaScript thực hiện cách lập chỉ mục tương tự. Việc kết hợp các ký hiệu và biểu tượng cảm xúc ZWJ có thể chiếm nhiều điểm mã. ``range.version`` là băm của sự kiện đích, không phải phiên bản tin nhắn hiện tại hoặc độ lệch thực thể UTF-16 của Telegram. Các chỉnh sửa sau này không bao giờ tự động di chuyển vị trí đánh dấu.

### Phân chia theo danh tính và thời gian

Lệnh `query` chấp nhận chính xác một `chat_id` hoặc các `chat_ids` không rỗng, phạm vi `from`/`to` bao gồm (tùy chọn), phạm vi ID tin nhắn bao gồm (chỉ một cuộc trò chuyện), các loại (`kinds: "all"`) hoặc các loại ký tự đại diện chính xác/tiền tố, các `actors` được chỉ định rõ, `search`, `hide_system` và `include_unscoped`. Các nhóm loại nhật ký (journal kind groups) sẽ mở rộng thành các điều kiện chính xác của chúng. Tìm kiếm sử dụng tìm kiếm tải trọng NFC/case-folded của nhật ký mà không thay đổi văn bản nguồn đã ký. Ngày tháng yêu cầu múi giờ và được chuẩn hóa sang UTC. Ngày tháng lọc **`observed_at`**. ``source_at`` của Telegram được hiển thị riêng biệt. Một lần xóa không có dấu thời gian nguồn sẽ không có thời gian xóa được tạo ra. Một bản ghi muộn được quan sát bên ngoài khoảng thời gian sẽ không được đưa vào; một đoạn `message-ID` có thể bao gồm một lần xóa muộn hơn cho các `message-ID` đó.

`snapshot` cố định thời gian tạo, ranh giới chuỗi/băm nhật ký, số lượng khớp, chuỗi đầu tiên/cuối cùng và `result_hash`. Giá trị sau là SHA-256 của mảng JSON chuẩn UTF-8 chứa các băm sự kiện khớp được sắp xếp theo thứ tự từ điển, bao gồm `[]` cho một lát cắt rỗng. Nó cũng chứa số lượng chính xác các loại và một bản thu nhỏ thời gian quan sát gồm 24 ô. Một lát (slice) lưu trữ một truy vấn, không phải các bản ghi nguồn trùng lặp . Khi xuất, `board/slices/<id>.json` liệt kê các băm hiện tại và các chuỗi đã thêm/xóa. Trình xác minh tái tạo kết quả ban đầu tại ranh giới tạo, sau đó là kết quả hiện tại. Các bản ghi được thêm vào được báo cáo dưới dạng một sự kiện thay đổi. Việc xóa một sự kiện ban đầu sẽ phá vỡ chuỗi bằng chứng bất biến; hành động này không được chấp nhận một cách im lặng như một hành động xóa thông thường khỏi một lát cắt.

Các ảnh chụp nhanh phản ứng có danh sách người tham gia gần đây không đầy đủ. Trình khám phá so sánh các ảnh chụp nhanh liền kề của cùng một cuộc trò chuyện/tin nhắn, bao gồm cả ảnh chụp nhanh tiền nhiệm nằm ngoài phạm vi cắt, và báo cáo sự chênh lệch tổng hợp về số lượng **giữa các quan sát**. Việc thiếu người tham gia gần đây không được coi là do họ đã xóa phản ứng. Bản chụp đầu tiên không có trạng thái trước đó được suy luận. Các quan sát về tác nhân vẫn được gán cho bản chụp mà chúng được cung cấp, chứ không phải cho một thời điểm hành động được giả định.

## API và xuất dữ liệu

`GET /api/board`chấp nhận các tham số collection/chat/author/label/state/from/to/q/kind/comments, offset/limit và thứ tự mới nhất/cũ nhất. `GET /api/board/card/{id}`trả về một thẻ, bản xem trước nguồn, chuỗi tin nhắn, lịch sử trạng thái và các thẻ liên quan. Đường dẫn con participants trả về các lựa chọn đề cập đủ điều kiện. `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}` thêm một bản ghi. `POST /api/board/slice-preview` tính toán một truy vấn. Các bản ghi lát cắt được phân trang tại `GET /api/board/slice/{id}/records`; việc tính toán lại luôn sử dụng bản chụp đọc ổn định hiện tại. `/api/stream` trực tiếp phát ra các thông báo `board` không chứa dữ liệu, tách biệt với các con trỏ nhật ký.

`GET /api/board/export` trả về một tài liệu đã được ký. Quyền truy cập giới hạn vào cuộc trò chuyện sẽ nhận được một **bản tiết lộ** đã ký và được dán nhãn rõ ràng, không bao giờ là chú thích của cuộc trò chuyện khác hoặc toàn bộ chuỗi. Các tệp ZIP chứa bằng chứng đầy đủ chứa tệp `annotations.jsonl`, tệp `case-board.json` đã ký và các phụ lục JSON dạng slice. Cài đặt báo cáo HTML/PDF/JSON cho phép chọn không sử dụng bảng, dấu trang/phần trích xuất không kèm thảo luận, hoặc thẻ có bình luận. Phần này tách biệt rõ ràng ý kiến của nhóm khỏi các quan sát. Bộ lọc dữ liệu báo cáo cũng hạn chế các ghi chú có thể đọc được; các tệp nguồn đầy đủ đã được ký trong tệp ZIP bằng chứng vẫn được giữ nguyên vẹn.

`GET /api/board/slice/{id}/export` trả về một đoạn trích JSON đã được ký tên `tgwitness-board-selection-v1`; `?format=csv` trả về một bảng dữ liệu tiện lợi mà không kèm theo chữ ký độc lập. Giữ nguyên định dạng JSON và ZIP:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

Kiểm tra lựa chọn xác thực tuyên bố đã ký, các bản ghi nguồn chính xác và tính đầy đủ của truy vấn tại ranh giới được chỉ định. Tệp ZIP chứa bằng chứng có thể mới hơn nhưng phải chứa tiền tố đó. Mục tiêu bị treo sẽ được báo cáo rõ ràng. Ảnh chụp lát cắt gốc khác, chú thích bị thay đổi , trạng thái phát lại không khớp hoặc nguồn bị thay đổi sẽ bị từ chối. Các kho lưu trữ cũ không có chú thích vẫn giữ nguyên hành vi xác minh hiện có.

Mặc định khi bàn giao là **“Không bao gồm**”. Việc bao gồm rõ ràng sẽ hiển thị các thẻ dự án thông qua các bản ghi đã được thu gọn, loại trừ các mục tiêu không thể truy cập hoặc bị bỏ qua, ẩn các phần được đánh dấu nổi bật mà văn bản nguồn đã bị thu gọn, làm sạch văn bản nhóm theo các quy tắc đề cập/liên hệ tương tự, và tùy chọn thay thế các nhãn điều tra viên bằng R01, R02… trong siêu dữ liệu và các trường hợp đã biết trong ghi chú. Không tiết lộ tệp gốc ` `annotations.jsonl``. Tệp sidecar ``tgwitness-case-board-handover-v1`` đã ký và báo cáo chứa cùng nội dung đã được thu gọn. Số lượng lát cắt chỉ mô tả các bản ghi được tiết lộ, trong khi chi tiết người thực hiện chụp nhanh/truy vấn gốc bị ẩn. Các tên trong văn bản tự do mà công cụ tối giản hóa không nhận diện được vẫn cần được rà soát, giống như trong các quy trình bàn giao thông thường. Phiên bản phái sinh này không khẳng định việc giữ nguyên chữ ký chú thích gốc sau khi che giấu thông tin.

## Giới hạn hoạt động

Các thông số bao gồm giới hạn mềm là 10.000 thẻ và 50.000 bình luận, một trang trích đoạn tối đa 5.000 bản ghi, và điều khiển xem trước phương tiện. Giới hạn mềm sẽ cảnh báo mà không xóa lịch sử. Các trang nguồn cấp dữ liệu có tối đa 200 thẻ. Các đoạn trích JSON độc lập bị giới hạn ở mức 64 MiB; hãy thu hẹp truy vấn hoặc sử dụng tệp ZIP có chữ ký cho tài liệu có dung lượng lớn hơn. Trình xác minh độc lập giới hạn việc phát lại chú thích ở mức 256 MiB. Case Board không kích hoạt hoặc triển khai bất kỳ thông báo bình luận bên ngoài nào.

Tính năng chấp nhận tự động sử dụng dữ liệu giả và một kênh truyền tải Telegram mô phỏng để kiểm tra lưu trữ, truy cập, hiển thị và xuất dữ liệu. Xem [phạm vi xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope) để biết phạm vi kiểm tra bằng chứng.
