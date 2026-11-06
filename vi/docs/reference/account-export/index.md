# Xuất tài khoản

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/account-export/

Xuất những nội dung mà tài khoản có thể truy cập hiện tại: phạm vi, các tác vụ có thể tiếp tục, tệp lưu trữ đã được ký và các bản sao chia sẻ đã được thu gọn.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Tài liệu](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

Xuất tài khoản giữ riêng tài khoản đó. Hãy chủ động tạm dừng giám sát hoặc một hoạt động thu thập khác trước khi bắt đầu hay tiếp tục; ứng dụng không bao giờ tự dừng chúng.

Với tư cách là quản trị viên cài đặt, hãy chọn **Bắt đầu tại đây → Xuất tài khoản của tôi**, hoặc **Xuất → Tài khoản Telegram → Cấu hình xuất tài khoản**. Đăng nhập nếu cần, xem lại phạm vi và bắt đầu xuất một cách rõ ràng. Không cần quan sát liên tục. **"Lưu quan sát**" là một bản xuất riêng biệt của nhật ký hiện có; ZIP của nó bao gồm tất cả các nguồn bất kể bộ lọc nhật ký. Mỗi không gian làm việc có các tác vụ, danh tính ký và bộ nhớ riêng. Quyền truy cập bảng điều khiển đã cấp, bao gồm quyền xuất thông thường không hạn chế, không thể mở các đường dẫn trên toàn tài khoản này.

Các bộ lọc người gửi và nội dung tin nhắn sẽ mở rộng khi chọn **“Lọc theo người gửi” hoặc “Lọc theo nội dung tin nhắn**”. **Phần “Dữ liệu tài khoản & phương thức kết nối**” chứa các danh mục tài khoản tùy chọn và tùy chọn “Takeout” hoặc “phiên làm việc thông thường”; phần tóm tắt của nó hiển thị các tùy chọn đang hoạt động ngay cả khi đã đóng. Việc đóng các phần này sẽ giữ nguyên cài đặt của chúng. Các bản nháp xuất và báo cáo vẫn tồn tại trong phiên làm việc hiện tại của bảng điều khiển khi chuyển đổi chế độ xem; chúng không được lưu khi tải lại trình duyệt. Các tác vụ hiện có vẫn có thể truy cập được từ cả hai tùy chọn xuất.

Quy trình làm việc này xuất dữ liệu hiện có thể truy cập được từ tài khoản đã kết nối. Mặc định sử dụng [Telegram Takeout](https://core.telegram.org/api/takeout); đây không phải là bản sao lưu dữ liệu Telegram không khả dụng hoặc đã bị xóa. Các cuộc trò chuyện bí mật, lịch sử không thể truy cập và các bản chỉnh sửa trước đó sẽ không được khôi phục. Telegram có thể áp đặt thời gian chờ trước khi Takeout bắt đầu. Bảng điều khiển sẽ hiển thị thời gian chờ đó; nó sẽ không tự động chuyển đổi phương thức truyền tải. Tùy chọn API thông thường rõ ràng có phạm vi bao phủ khác và ghi lại các danh mục không được hỗ trợ.

Takeout is the official export API also used by Telegram Desktop. TgWitness can write Desktop-compatible JSON directly from its own acquisition; importing someone else's archive is not required. Chat and message IDs are available through both transports. A public chat or permission to forward does not guarantee a faster export or remove Takeout's approval delay. Measure the same scope and media settings before comparing speed.

For up to 20 explicitly selected chat IDs, regular-API export resolves those peers directly before considering the account's complete dialog inventory. A readable public channel can therefore be exported without joining it, even when it is absent from the dialog list. Uncached peers fall back to the ordinary inventory. The archive filter remains enforced: if Telegram does not return a dialog and archived chats are excluded, the unknown archive status is recorded as an omission. Takeout keeps its split-range inventory procedure. Neither path joins chats or changes forwarding permissions. In Desktop-compatible JSON, channels that Telegram marks `left` appear under `left_chats`, including readable public channels the account has not joined.

Both `FLOOD_WAIT` and `FLOOD_PREMIUM_WAIT` pause requests for the full server-requested period. The account's deadline is persisted across reconnects and restarts; a shorter later wait cannot shorten it. Retries are bounded, cancellation preserves sealed pages, and API credentials are not rotated to bypass a rate limit. No Premium purchase is made.

## Chọn những gì cần thu thập

| Bối cảnh | Ý nghĩa |
| --- | --- |
| Mục đích | Ghi lại lý do tại sao việc thu thập thông tin này là cần thiết. Không đưa các tên không cần thiết hoặc chi tiết nhạy cảm của vụ việc vào đây. |
| Ngôn ngữ báo cáo | Chọn ngôn ngữ cho các nhãn trong báo cáo có thể đọc được. Nội dung tin nhắn gốc vẫn giữ nguyên; các nhãn mẫu chưa được dịch sẽ sử dụng tiếng Anh. Ngôn ngữ được cố định thông qua các tùy chọn công việc đã được ký. |
| Các loại cuộc trò chuyện / ID cuộc trò chuyện | Tất cả các loại đã chọn hoặc chỉ các cuộc trò chuyện được liệt kê; "Tin nhắn đã lưu" thuộc về các cuộc trò chuyện riêng tư. Các cuộc trò chuyện đã lưu trữ có thể được chọn riêng biệt. |
| Ngày tháng | UTC. Cả hai ngày bắt đầu và kết thúc trên lịch của bảng điều khiển đều được bao gồm. API sử dụng các khoảng thời gian bao gồm `from_utc` và loại trừ `to_utc`; bảng điều khiển sẽ gửi thời điểm bắt đầu của ngày tiếp theo sau ngày “Through”. Một giới hạn trống sẽ không áp dụng hạn chế cho phía đó. |
| ID người gửi | Chỉ hiển thị tin nhắn từ những người gửi được liệt kê; danh sách trống bao gồm tất cả người gửi. |
| Nội dung bao gồm | Các cụm từ văn bản không phân biệt chữ hoa chữ thường, được so khớp bằng toán tử OR. Các điều kiện người gửi/ngày/nội dung tin nhắn của chính người dùng được kết hợp bằng toán tử AND. |
| Tin nhắn của chính mình | Chỉ lưu giữ các tin nhắn gửi đi. |
| Các loại phương tiện | Chọn các danh mục tệp đính kèm hoặc xóa tất cả để tránh tải xuống các tệp tin trong tin nhắn. |
| Giới hạn tệp / tổng dung lượng phương tiện | Dung lượng theo tệp (MiB) và tổng dung lượng phương tiện đã tải xuống (GiB). Văn bản, biên lai, báo cáo có thể đọc được và dung lượng phụZIP cần thêm dung lượng đĩa. |
| Các danh mục tài khoản | Hồ sơ, danh bạ, ảnh đại diện, câu chuyện, siêu dữ liệu phiên và các dữ liệu Takeout khác có các tùy chọn điều khiển riêng biệt. |

Cài đặt sẵn **bộ sưu tập “Minimize”** sẽ vô hiệu hóa các tệp và siêu dữ liệu tài khoản. Các bộ lọc người gửi/nội dung được áp dụng trước khi lưu giữ các trang tin nhắn và tải xuống phương tiện. Telegram vẫn truyền các trang lịch sử API chứa các tin nhắn cần thiết để đánh giá các bộ lọc đó: việc lọc không đảm bảo rằng các tin nhắn không được chọn sẽ không bao giờ vào bộ nhớ xử lý. Các hoạt động quan sát khác đang diễn ra trong không gian làm việc có phạm vi và cài đặt lưu giữ riêng.

Lịch sử ảnh đại diện và các câu chuyện không được chọn theo mặc định. Hãy tắt tính năng hiển thị ảnh đại diện và danh bạ khi vụ việc chỉ cần các tin nhắn. Nếu các tệp đính kèm hoặc siêu dữ liệu không cần thiết, việc loại trừ chúng trong quá trình thu thập sẽ giúp tránh lưu giữ một bản sao riêng tư khác trong tệp xuất này.

Photo payloads use the still-image variant identified in their metadata and hash manifests, including photos with an animated avatar variant. That animation is not substituted for the selected still image. A shorter or longer payload than the observed size is recorded as a failed attachment, and a changed representation during file-reference renewal is rejected. These failures leave the archive partial while retaining the message records. Independent verification also rejects saved attachments whose signed length contradicts their observed size or representation, including in older archives.

## Tóm tắt, phạm vi và xác minh

Mỗi tác vụ sẽ khóa các tùy chọn và danh tính tài khoản của nó. Danh mục và các trang đã thu thập được ký xác thực; biên lai trang ghi lại các giá trị băm, vị trí con trỏ, thời gian, kết quả tệp đính kèm và biên lai trước đó. Chỉ các trang đã được cam kết mới được tính vào tiến độ. Khi khởi động lại hoặc tiếp tục, hệ thống sẽ kiểm tra các bản ghi này trước khi tiếp tục. Tài khoản bị thay đổi, trang đã ký bị thay đổi hoặc chuỗi biên lai không nhất quán sẽ bị từ chối. Không thể chỉnh sửa tùy chọn trong quá trình thu thập: hãy bắt đầu một tác vụ khác cho phạm vi khác.

Nút "Pause" (Tạm dừng) sẽ tạm dừng hoạt động của tài khoản đang chạy. Khi khởi động lại ứng dụng, công việc chưa hoàn thành sẽ vẫn còn đó để bạn có thể tiếp tục một cách rõ ràng. Một phiên Takeout đã hết hạn yêu cầu phải tiếp tục một cách rõ ràng; việc thay đổi phạm vi phân chia Telegram có thể yêu cầu một quá trình thu thập mới. Chức năng "Resume" (Tiếp tục) giữ lại các quan sát trước đó, do đó, quá trình xuất dữ liệu kéo dài không phải là một bản chụp nhanh nguyên tử duy nhất. Các thao tác thay đổi tài khoản khác và các quá trình xuất dữ liệu xung đột sẽ bị chặn trong quá trình thu thập. Hãy đợi cho đến khi quá trình đóng gói hoàn tất trước khi xóa một không gian làm việc.

Chức năng "Resume" sẽ xác minh lại nội dung đã ghi lại trước khi tiếp tục. Các kho lưu trữ lớn trên thiết bị lưu trữ chậm có thể vượt quá thời gian được cấu hình **Các tham số → Thời gian chờ thực hiện hành động trên bảng điều khiển** (mặc định là 120 giây). Hãy tăng giá trị cài đặt này trước khi thử lại; việc hủy bỏ hoặc gián đoạn lưu trữ sẽ khiến tác vụ bị tạm dừng, còn việc kiểm tra tính toàn vẹn thất bại sẽ khiến tác vụ bị thất bại kèm theo lời giải thích. Quá trình xác minh phải hoàn tất hoặc dừng lại một cách an toàn trước khi các tệp liên quan có thể được đóng lại. Chưa có tuyên bố nào về thông lượng của các tài khoản lớn được xác thực bởi các kiểm tra tổng hợp.

Bảng điều khiển phân biệt phạm vi đã chọn hoàn chỉnh với kho lưu trữ một phần, đồng thời ghi lại các nội dung bị bỏ sót và các lần đọc không thành công. Các tệp bị loại trừ có chủ đích khác với các tệp không thành công hoặc không khả dụng. Kiểm tra phạm vi bao phủ ngay cả khi quá trình xác minh tính toàn vẹn thành công. Không có trình đọc cục bộ nào có thể chứng minh rằng Telegram đã trả về mọi tin nhắn từng tồn tại.

Các tệp ZIP đã hoàn thành vẫn có sẵn để tải xuống nhiều lần và tải xuống theo phạm vi HTTP. Một kho lưu trữ tài khoản chứa `manifest.json`, `manifest.sig`, đã được ký `job.json`, `inventory.json`, `receipts/`, có tính chính thức `data/*.jsonl`, đã được chọn `media/`, HTML có thể đọc được và một trình xác minh. Ghim dấu vân tay của trình thu thập thông qua một kênh độc lập, sau đó xác minh bằng cách sử dụng một bản cài đặt đáng tin cậy:

```
python -m tgwitness.verify account-export.zip --fingerprint TRUSTED_SHA256
```

Đối với các kho lưu trữ có dung lượng mở rộng vượt quá 4 GiB, hãy đặt một giới hạn dung lượng phù hợp một cách rõ ràng `--max-gib`. Bảng điều khiển xác minh các tệp lưu trữ cục bộ đã được xác thực và hoàn tất bằng cách sử dụng kích thước mở rộng đã khai báo và bản tóm tắt ZIP đã công bố; CLI bên ngoài duy trì giới hạn kích thước độc lập của riêng mình. Hãy xác minh trước khi mở tệp HTML có thể đọc được. Trình xác minh đi kèm trong tệp lưu trữ rất tiện lợi, nhưng việc sử dụng một trình xác minh được lấy độc lập sẽ giúp tránh phải tin tưởng vào mã thực thi được cung cấp cùng với bằng chứng.

Chữ ký Ed25519 và các hàm băm SHA-256 phát hiện các thay đổi sau khi bộ thu thập đã ghi lại các byte liên quan. Chúng **không** chứng minh rằng Telegram đã ký các tin nhắn đó, rằng người vận hành bộ thu thập là trung thực, rằng lịch sử tài khoản là đầy đủ, hoặc rằng tòa án sẽ chấp nhận tài liệu này. Thời gian ghi lại sử dụng đồng hồ của bộ thu thập. Dấu thời gian độc lập và nguồn gốc thu thập độc lập phải được đánh giá riêng biệt.

## Chuẩn bị tài liệu tiết lộ thông tin cho luật sư hoặc người nhận khác

Sau khi tải xuống tệp xuất hoàn chỉnh, hãy giữ lại tệp gốc ZIP và mở `index.html` từ bản sao đã giải nén. Báo cáo giải thích phạm vi, mức độ bao phủ có sẵn và các giới hạn của nó. Các tham chiếu bản ghi kết hợp tham chiếu kho lưu trữ, đường dẫn tài liệu và số bản ghi, để người nhận có thể tìm thấy mục tương ứng trong tệp HTML hoặc bản in. Để xem ví dụ minh họa, hãy truy cập [mở báo cáo hư cấu](https://phishdestroy.github.io/TgWitness/demo/report/).

Từ tệp xuất tài khoản đã hoàn tất, hãy chọn **“Chuẩn bị bản sao để chia sẻ**”. Thao tác này sẽ tạo ra một bản sao có chữ ký riêng biệt. Nguồn ZIP vẫn giữ nguyên và ở chế độ riêng tư; không gửi nó cùng với bản sao đã được tối ưu hóa trừ khi người nhận được ủy quyền để nhận toàn bộ nội dung của nó. Hãy chọn ngôn ngữ báo cáo riêng biệt. Việc thay đổi ngôn ngữ hoặc bất kỳ cài đặt lựa chọn nào đều yêu cầu xem trước một lần nữa trước khi tạo.

1. Nhập mục đích tiết lộ và chọn các tiêu chí về ngày tháng, ID người gửi và văn bản chính xác.
2. Chọn giữa việc giữ nguyên danh tính, chỉ hiển thị những người tham gia được liệt kê, hoặc ẩn danh cho tất cả mọi người. Trong cả hai chế độ ẩn danh, ID/tiêu đề cuộc trò chuyện và ID tin nhắn cũng sẽ được thay thế. Các biệt danh sẽ ổn định trong một lần chia sẻ thông tin và thay đổi giữa các lần chia sẻ được chuẩn bị độc lập.
3. Giữ nguyên văn bản tin nhắn, bỏ qua hoàn toàn hoặc thêm tên/cụm từ chính xác vào danh sách che giấu. Ở chế độ riêng tư, công cụ này cũng che giấu tên người gửi ẩn đã biết và tên người dùng thay thế, ID người gửi toàn bộ token, tên trong cuộc trò chuyện trực tiếp, liên kết, địa chỉ email và các chuỗi ký tự giống số điện thoại. Việc khớp tên đã biết xử lý việc chuyển đổi chữ hoa/thường theo Unicode, bao gồm `Straße`/`STRASSE`. Các tiêu đề chung của nhóm/kênh sẽ không tự động bị loại bỏ khỏi nội dung tin nhắn. Nếu vượt quá giới hạn che giấu danh tính đã biết, hãy thu hẹp phạm vi xuất nguồn hoặc loại bỏ văn bản; công cụ sẽ không tự động bỏ qua các tên xuất hiện sau đó. Đây là các quy tắc được áp dụng theo khả năng tốt nhất, không phải là biện pháp ẩn danh toàn diện.
4. Không nên bao gồm các tệp trừ khi người nhận cần chúng. Các tệp gốc được bao gồm vẫn giữ nguyên độ phân giải, âm thanh, văn bản và siêu dữ liệu. Chúng **không** được công cụ này ẩn danh hóa.
5. Xem trước số lượng, cảnh báo và các mẫu tin nhắn đã được chuyển đổi, sau đó xác nhận rõ ràng việc tạo bản ghi. Mỗi mẫu được giới hạn ở 12 tin nhắn và 2.000 ký tự văn bản. Đây chỉ là mẫu, không phải là bản xem xét đầy đủ về kết quả. Việc thay đổi cài đặt yêu cầu phải xem trước lại. Bản xem trước sẽ hết hạn sau 15 phút và chỉ áp dụng cho phiên quản trị viên đó cùng với thẻ ZIP gốc chính xác; nó không thể được sử dụng lại sau khi tạo. Một bản xem trước mới sẽ làm mất hiệu lực bản xem trước trước đó cho cùng một tác vụ và phiên làm việc.
6. Xem toàn bộ kết quả `index.html` và `messages.jsonl` trên máy cục bộ trước khi chuyển giao. Nếu phát hiện thông tin không cần thiết, hãy tạo một bản công bố mới với các điều khoản loại trừ chặt chẽ hơn. Không chỉnh sửa trực tiếp thẻ ZIP đã được ký.

### Các tin nhắn bị loại trừ khỏi kết quả lọc

**Xem trước.** Một thông báo tiết lộ sẽ không hiển thị đầy đủ nếu thông tin chưa hoàn chỉnh. Trong mỗi cuộc trò chuyện chứa ít nhất một tin nhắn đã được tiết lộ, các tin nhắn bị loại khỏi lựa chọn sẽ xuất hiện dưới dạng các dấu hiệu, `[withheld by selection — rule: sender]` (hoặc `text`, `period`). Chọn **“Các tin nhắn bị loại trừ bởi lựa chọn**”: một dấu hiệu cho mỗi chuỗi tin nhắn liên tiếp bị loại trừ (mặc định) hoặc một dấu hiệu cho mỗi tin nhắn. Các dấu hiệu chỉ chứa quy tắc và số lượng, không bao giờ chứa nội dung, người gửi, ngày tháng hoặc tệp đính kèm. Các cuộc trò chuyện không có tin nhắn nào được tiết lộ sẽ bị loại trừ hoàn toàn, do đó gói phần mềm này không tiết lộ sự tồn tại của chúng.

Các phản hồi được tiết lộ cho biết nội dung mà chúng trả lời: một tin nhắn có trong bản sao này, một tin nhắn bị loại trừ khỏi lựa chọn, hoặc một tin nhắn không có trong bản xuất nguồn (đã bị xóa trước khi xuất hoặc chưa bao giờ được xuất; bản xuất không thể xác định được trường hợp nào). Một tin nhắn bị loại trừ mà câu trả lời được tiết lộ đề cập đến luôn có dấu hiệu riêng, do đó câu trả lời sẽ trỏ đến một bản ghi giải thích lý do tại sao nó trống. Ba trạng thái này khác biệt với các trường hợp xóa và khoảng trống trong bộ sưu tập, vốn thuộc về tệp xuất nguồn.

Trong `messages.jsonl` (định dạng `tgwitness-account-disclosure-v2`) mỗi tin nhắn có `state`: `disclosed`, hoặc `withheld` với `rules` và `count`. Một phản hồi được tiết lộ có `reply_to` với mục tiêu `id` và `state` (`disclosed`, `withheld`, `not_in_source`). Danh sách này thống kê các tin nhắn, cuộc trò chuyện, phương tiện truyền thông và `withheld` tin nhắn. `verify.py` từ chối một dấu hiệu chứa nội dung và một phản hồi trỏ đến một bản ghi bị thiếu trong gói; các gói phiên bản 1 được xác minh như trước đây.

Định dạng tối giản loại bỏ các hồ sơ tài khoản có cấu trúc, danh bạ, ảnh đại diện, phiên làm việc, câu chuyện, đối tượng Telegram thô, tiêu đề chuyển tiếp, trích dẫn trả lời, thẻ liên hệ và siêu dữ liệu vị trí. Nó loại trừ các tệp JSONL gốc, cài đặt bộ lọc riêng tư, khóa bí danh và bản đồ danh tính. Văn bản được chọn, danh tính được giữ lại rõ ràng và các tệp được bao gồm vẫn có thể chứa cùng tên, ID hoặc cụm từ được sử dụng trong các bộ lọc đó; chúng cần được xem xét riêng. Chính sách riêng tư và khóa bí danh được lưu giữ dưới dạng mã hóa trong kho lưu trữ cục bộ của tác vụ; việc xóa tác vụ sẽ xóa các bản ghi tiết lộ riêng tư liên quan. Các bản ghi chính sách công khai ghi lại số lượng bộ lọc thay vì giá trị bộ lọc. Mục đích được nêu rõ là công khai trong tệp manifest và HTML: các tiêu chí riêng tư rõ ràng và, trong các chế độ ẩn danh, các danh tính ẩn đã biết cũng được che giấu tại đó, kể cả khi nội dung tin nhắn bị bỏ qua. Hãy giữ cho mục đích không chứa các chi tiết cá nhân không cần thiết; bối cảnh nhận dạng chưa xác định có thể được giữ lại.

Tệp manifest của nó liên kết các tệp phái sinh, chính sách công khai và băm của tệp ZIP gốc. Quá trình xác minh có thể xác định tính toàn vẹn và, nếu nguồn được cung cấp tại địa phương, xác định sự khớp nối nguồn:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Liên kết nguồn không tự nó chứng minh rằng quá trình chuyển đổi đã chọn tất cả các mục cần thiết hoặc loại bỏ tất cả các chi tiết nhận dạng. Văn bản gốc không được nhúng làm bằng chứng. Cần có một cuộc đánh giá mới để đưa ra phán đoán đó.

## Chia sẻ và lưu trữ dữ liệu ghi lại

Select the messages and files the recipient needs, review the complete sharing copy, and retain the source separately. Record the delivered ZIP's hash so the recipient can identify and verify that exact copy. Pseudonymization replaces the selected identifiers; included text and original files remain part of the review.

GitHub Actions supports full-account and selected-chat exports through Takeout or the regular API, plus a one-chat event journal. The [hosted capture guide](https://phishdestroy.github.io/TgWitness/docs/capture/) explains settings verification and the 120-minute limit. To verify a sharing copy derived from hosted capture, check its source hash against the original archive and verify that archive's attestation with the [mode-specific checks](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope).

[Định dạng bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/) · [Báo cáo trường hợp](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-reports/)
