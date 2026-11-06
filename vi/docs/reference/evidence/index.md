# Định dạng bằng chứng

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/

Nội dung của tệp ZIP đã được ký, các loại bản ghi, biên nhận giao dịch, hồ sơ người dùng, bản sao lưu ngoài trang web và xác minh ngoại tuyến.

TgWitness lưu trữ các quan sát trên Telegram có thể nhìn thấy trong tài khoản dưới dạng nhật ký được ký điện tử. Người nhận có thể xác minh các bản ghi, tệp đính kèm và báo cáo đã lưu so với một khóa thu thập đáng tin cậy, sau đó so sánh nhật ký với một điểm kiểm tra được lưu giữ độc lập. Trang này mô tả các định dạng, các bước kiểm tra và tài liệu cần lưu giữ để bàn giao.

Recipients can start with **VERIFY.cmd** on Windows: it asks for the original ZIP and independently obtained key fingerprint, displays an explained result, and saves a separate verification transcript. See [verification launchers and the portable runtime](https://github.com/phishdestroy/TgWitness/blob/main/docs/VERIFICATION_LAUNCHER.md) for setup and trust limits.

## “Được ký” là gì

| Nội dung | Bảo vệ | Những nội dung cần lưu giữ |
| --- | --- | --- |
| Mọi ghi nhận trong nhật ký, bao gồm các sự kiện hoạt động | Chuỗi SHA-256 và chữ ký Ed25519 cho mỗi sự kiện | `events.jsonl` gốc, dấu vân tay khóa đáng tin cậy, và điểm kiểm tra được lưu giữ |
| Nội dung tệp ZIP chứa bằng chứng | `manifest.sig` ký vào bản kê khai chuẩn, trong đó liệt kê các giá trị băm của các tệp nội dung | Tệp ZIP đầy đủ, bao gồm tệp manifest và chữ ký |
| Tệp đính kèm được lưu giữ | Giá trị SHA-256 và số byte trong một sự kiện `media.saved` có chữ ký; băm tệp trong bản kê khai ZIP có chữ ký | Các byte gốc bên trong tệp ZIP đã được xác minh |
| Checkpoint | Chữ ký Ed25519 trên độ dài sổ ghi chép, băm tiêu đề, khóa công khai và thời gian tạo | Một bản sao độc lập được lưu giữ trước khi có thay đổi gây tranh cãi |
| Biên lai giao dịch | Signed record of the collector version, source-file hashes and start settings, also included in `process.started` | The receipt, associated journal and the environment evidence for the selected verification mode |
| Báo cáo dễ đọc: `report.html` và các phần của nó, `report.json`, `report.pdf`, `chat.pdf` | Mỗi tệp có một con dấu Ed25519 trên nội dung của nó; PDF cũng mang theo chữ ký tiêu chuẩn PDF (xem [Báo cáo có thể đọc được](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#readable-reports)) | Tệp nhận được và dấu vân tay khóa đáng tin cậy; tệp ZIP được mô tả trong đó |
| CSV độc lập | Không có chữ ký mật mã độc lập; chỉ riêng các giá trị băm sự kiện là chưa đủ | Vui lòng sử dụng bản sao chính xác có trong tệp ZIP đã được xác minh để kiểm tra tính toàn vẹn |
| Ảnh chụp màn hình, bản in hoặc tệp PDF được tạo ra từ trình duyệt | Không có chữ ký của TgWitness trên bản sao | Vui lòng giữ lại gói phần mềm gốc đã được xác minh và ghi chép lại quy trình tạo ra phiên bản phái sinh |

Trình thu thập xác minh chữ ký nhật ký trước khi tạo mọi định dạng xuất. Các báo cáo HTML và PDF dễ đọc đều có con dấu riêng; tệp CSV độc lập được kiểm tra như một phần của tệp ZIP đã ký. Giữ lại tệp ZIP để bảo toàn các byte tệp đính kèm và bản kê khai, cùng một điểm kiểm tra riêng biệt để đối chiếu nhật ký với ranh giới trước đó.

## Comparing chat exports

Verify and compare two signed chat-export ZIPs with independently retained signer fingerprints:

```
python -m tgwitness.verify first.zip --compare second.zip \
  --fingerprint FIRST_TRUSTED_KEY_SHA256 --compare-fingerprint SECOND_TRUSTED_KEY_SHA256
```

When both archives record the same numeric account and chat IDs, records are paired by message ID. **Unchanged** means equality of the complete saved JSON record: full text, author, dates, reply target, nested metadata and unknown fields are all included. JSON object key order does not matter; absent fields, nulls, value types and array order do. The 300-character preview is only for display. Changed entries name the differing top-level `changed_fields`, including changes invisible in that preview. Duplicate message IDs are rejected instead of overwriting one another during matching.

A difference can be a changed display name, view count, collection annotation or other observation metadata. It does not by itself establish a Telegram edit, identify who made a change, or prove which contradictory archive is accurate. Unparsed records remain in the comparison; equality of their saved representation does not mean their Telegram payload was decoded.

For different or missing account/chat identities, the tool only finds possible correspondences using sender, complete text, file hash, media type and a five-second time tolerance. It reports **Matched**, not **Unchanged**. These candidates do not establish message identity or equality of all metadata. Unparsed records remain unmatched. Differences in paired records remain listed in `changed`, including in content mode; these differences do not prove edits of the same message. With `--json`, `matched` counts pairs and `unchanged` counts pairs whose complete saved records are equal. Neither count proves message identity in content mode. The existing `changed_fields` and integer `unchanged` output remain compatible with earlier comparison results. Archive format and signature verification are unchanged.

## Chuyển giao cuộc điều tra

1. Ghi lại mã tham chiếu vụ việc, người vận hành, ID tài khoản Telegram dạng số, các nguồn đã chọn, chính sách thu thập và khoảng thời gian thu thập vào ghi chú vụ việc của bạn. TgWitness bảo toàn các quan sát và hỗ trợ ghi chú liên kết với nguồn cũng như các bộ sưu tập trong [Case Board](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-board/). Lưu giữ hồ sơ chuyển giao và lưu giữ cùng với các tài liệu vụ việc của bạn. Kiểm tra cấu hình thu thập dự kiến thông qua quy [trình chấp nhận trực tiếp](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
2. Hãy lưu giữ riêng biệt dấu vân tay khóa công khai của không gian làm việc trước khi dựa vào các tệp xuất của nó. Lưu các điểm kiểm tra đã được ký bên ngoài bộ thu thập trong quá trình thu thập. Ghi lại các sự gián đoạn và giới hạn về khả năng hiển thị của tài khoản.
3. Xuất tệp **ZIP đã được ký** và lưu giữ biên nhận thực thi đã được ký. Sử dụng điểm kiểm tra tại hoặc trước ranh giới nhật ký đã xuất. Một điểm kiểm tra sau đó có thể từ chối chính xác việc xuất trước đó do quá ngắn. Các tệp xuất bao gồm toàn bộ nhật ký không gian làm việc, bất kể các bộ lọc trên bảng điều khiển; vui lòng xem xét kỹ tài liệu trước khi chia sẻ.
4. Yêu cầu người nhận xác minh tệp ZIP bằng một bản sao đáng tin cậy của trình xác minh cùng với dấu vân tay/điểm kiểm tra được cung cấp độc lập. Từ một bản checkout đáng tin cậy với môi trường Python đang hoạt động:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   Báo cáo đầu ra thành công sẽ hiển thị mã `key_pinned: true` và `checkpoint_checked: true` khi cả hai đầu vào đều được cung cấp và chấp nhận. Vui lòng lưu giữ kết quả xác minh.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. Ghi lại mã SHA-256 của kho lưu trữ, phạm vi xuất, ngày chuyển giao, người gửi và người nhận vào hồ sơ lưu giữ của quý vị. Giữ nguyên vẹn gói tệp gốc và làm việc trên các bản sao. Chia sẻ các tệp bằng chứng thay vì thư mục dữ liệu riêng tư của ứng dụng, vì thư mục này còn chứa các phiên tài khoản và khóa bí mật ký số. Để chuyển giao, tệp xuất có thể được nén vào tệp ZIP được bảo vệ bằng mật khẩu theo tiêu chuẩn AES-256. Mật khẩu chỉ nhằm bảo vệ tính bảo mật và không được lưu trữ; người nhận sẽ giải nén tệp lưu trữ và xác minh tệp xuất đã được ký bên trong, đảm bảo rằng tệp này không bị thay đổi.
   2. Nếu cần xác định mốc thời gian độc lập, vui lòng tuân thủ [quy trình theo RFC 3161](https://phishdestroy.github.io/TgWitness/vi/docs/reference/timestamp/) và lưu giữ yêu cầu, điểm kiểm tra, thông tin về CA đáng tin cậy, cùng phản hồi đã được xác minh từ cơ quan có thẩm quyền. Việc chỉ chuẩn bị yêu cầu sẽ không giúp thu được dấu thời gian.

Việc xác minh thành công chứng minh tính toàn vẹn so với khóa thu thập dữ liệu đáng tin cậy và ranh giới được duy trì. Xem [phạm vi xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope) để biết các giả định về độ tin cậy và [kết quả xác thực](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/) cho các kiểm tra đã thực hiện.

## Trích đoạn bàn giao

Một tệp ZIP đã ký chứa toàn bộ nhật ký không gian làm việc. Khi tòa án, luật sư hoặc bộ phận xử lý lạm dụng chỉ cần một số cuộc trò chuyện, một khoảng thời gian hoặc những người cụ thể, tùy chọn **Xuất → Trích xuất bàn giao** sẽ chuẩn bị một bản sao được tối ưu hóa (`tgwitness-handover-v1`) theo các quy tắc tiết lộ đã chọn. Người vận hành nêu rõ mục đích và chọn các cuộc trò chuyện, khoảng thời gian tùy chọn (UTC), những người mà bản trích xuất liên quan đến, những gì sẽ xảy ra với những người khác (được hiển thị, được thay thế bằng bí danh P01, P02… hoặc bị loại bỏ), những nội dung tin nhắn nào được giữ lại, những tệp đính kèm và ảnh đại diện nào được bao gồm, và liệu số điện thoại và địa chỉ email trong nội dung tin nhắn có bị che giấu hay không. Mục đích và các quy tắc này được ghi trong bản kê khai đã ký và trong báo cáo; nhật ký ghi lại `handover.exported` cùng với quyền truy cập đã chuẩn bị nó và mã SHA-256 của tệp, chứ không phải nội dung.

`verify.py` kiểm tra một bản trích xuất theo hai cách. Một bản ghi được hiển thị là không thay đổi sẽ được xác minh đầy đủ: nội dung của nó so với hàm băm, chữ ký Ed25519 và liên kết đến bản ghi trước đó được bao gồm. Một bản ghi được thu gọn vẫn giữ nguyên giá trị băm và chữ ký gốc, do đó chữ ký vẫn được xác minh, nhưng các trường bị ẩn không thể tính toán lại từ đó; bản ghi nêu rõ những gì đã bị ẩn và báo cáo sẽ đánh dấu phần đó. Tệp manifest nêu rõ độ dài nhật ký và phần đầu với chữ ký của người thu thập trên phần đầu đó, đồng thời đếm số bản ghi bị loại bỏ; tệp `coverage.json` mô tả các cuộc trò chuyện đã chọn. Các tên xuất hiện trong tên tệp sẽ không được phát hiện. Kiểm tra lại các tệp cuối cùng trước khi chia sẻ: văn bản tự do, tên tệp và các tệp đính kèm đã chọn vẫn có thể xác định danh tính người dùng. Giữ lại tệp ZIP đã ký đầy đủ: tệp giải nén chỉ là bản tiết lộ, không phải bản thay thế.

## Báo cáo dễ đọc

Bằng chứng đã ký, tệp ZIP bàn giao và tệp ZIP cuộc trò chuyện chứa các báo cáo HTML và JSON có thể đọc được, cùng với tệp PDF khi có sẵn các phông chữ cần thiết, bằng ngôn ngữ báo cáo đã chọn. Mỗi báo cáo được niêm phong bằng khóa Ed25519 của không gian làm việc và có thể được xác minh riêng biệt: ` `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]``.

- `report.html` / `chat.html`: lệnh đóng tệp (`tgwitness-report-seal-v1`) sẽ đóng tệp và ký xác thực từng byte trước đó bằng SHA-256. Các nhật ký và cuộc trò chuyện dài sẽ được chia thành các phần có kích thước có thể cấu hình (Cài đặt báo cáo, từ 500 đến 100.000 bản ghi; mặc định là 5.000): `records/records-0001.html` hoặc `messages/messages-0001.html`, mỗi phần được đóng dấu với số thứ tự, phạm vi và tổng số, đồng thời được liệt kê cùng với tệp SHA-256 trong bản kê khai đã ký. Các chuỗi tín hiệu kiểm tra trạng thái của bộ thu thập được hiển thị dưới dạng một dòng trừ khi Cài đặt báo cáo liệt kê chúng từng cái một.
- `report.json` (`tgwitness-report-json-v1`, các khóa `format`, `report`, `seal`): con dấu xác thực SHA-256 của bản chuẩn JSON thuộc `report`, do đó các hệ thống và kịch bản xử lý vụ án có thể đọc được các thông tin này và có thể thực hiện lựa chọn để bảo vệ dữ liệu từ đó trong khi tệp đã ký vẫn được giữ nguyên vẹn.
- `report.pdf` / `chat.pdf`: tài liệu chính thức để in và lưu trữ, được ký hai lần trên cùng một dãy byte, toàn bộ tệp ngoại trừ giá trị chữ ký (`/ByteRange`). Chữ ký tiêu chuẩn PDF (`adbe.pkcs7.detached`, CMS cùng với SHA-256 và ECDSA P-256) sử dụng chứng chỉ ký tài liệu tự cấp được lưu trữ trong kho lưu trữ không gian làm việc; số sê-ri chủ thể của nó là dấu vân tay khóa Ed25519 . Con dấu Ed25519 được truyền bên trong CMS dưới dạng thuộc tính chưa ký `2.25.240684792623320047764573196045913242332` và đặt tên cho chứng chỉ SHA-256 bằng `"content": "pdf-byte-range"`, do đó khóa Ed25519 xác nhận tính hợp lệ của chứng chỉ. Trình đọc PDF cho biết liệu tệp có bị thay đổi sau khi ký hay không và coi người ký là không xác định cho đến khi chứng chỉ được tin cậy; thay vào đó, hãy so sánh dấu vân tay Ed25519. Các tệp PDF tiếng Trung, tiếng Nhật và tiếng Hàn cần có phông chữ trên máy chủ (hoặc trong `TGWITNESS_FONT_DIR`); nếu không có, tệp ZIP chỉ chứa các báo cáo HTML và JSON mà thôi.

Trong một kênh hoặc siêu nhóm, Telegram đánh số các tin nhắn 1, 2, 3… theo thứ tự. Một bản xuất cuộc trò chuyện liệt kê số đầu tiên và số cuối cùng, số lượng tin nhắn hiện có và mọi dãy số bị thiếu trong `message-ids.json` , bản kê khai và tiêu đề `chat.json` , đồng thời đánh dấu từng khoảng trống ở vị trí tương ứng trong bản ghi. `verify.py` liệt kê lại chúng từ `chat.json` . Một số bị thiếu là tin nhắn mà Telegram không trả về (đã bị xóa trước khi xuất, hoặc không hiển thị với tài khoản); trong các cuộc trò chuyện riêng tư và nhóm cơ bản, các số được chia sẻ chung cho tất cả các cuộc trò chuyện của tài khoản và các khoảng trống không được tính.

After reading the history, the export asks Telegram for every absent number again, by number (`channels.getMessages`, up to 10,000 numbers). The result is in `message-ids.json` and the report. An empty answer records that the number is unavailable to this account at recheck time; it leaves the cause unspecified. A message returned on recheck is added to the export and marked `found_on_recheck`.

Mỗi báo cáo bắt đầu bằng **. Tóm tắt**: một đoạn văn, sau đó là những gì tài liệu thể hiện và những gì nó không thể hiện (ai đứng sau tài khoản, tính đầy đủ của dữ liệu, các nội dung bị xóa trước khi quan sát, thời gian không có dấu thời gian). Con dấu của trang sẽ chuyển sang màu hổ phách khi trình duyệt đã kiểm tra chữ ký của con dấu, chứ không phải trang: trình duyệt không cung cấp các byte riêng cho trang. Nó chỉ chuyển sang màu xanh lục khi người đọc kéo tệp vào phần kiểm tra ở cuối trang và mọi byte đều khớp, và chỉ khi trang được hiển thị chính là tệp đó; nếu không, nó sẽ chuyển sang màu đỏ.

Mỗi báo cáo nêu tên chương trình chính xác: cam kết Git khi trình thu thập dữ liệu chạy từ một bản checkout hoặc trình cài đặt đặt `TGWITNESS_COMMIT`, và SHA-256 của các tệp nguồn của nó (`source_tree_sha256`, JSON chuẩn của đường dẫn → SHA-256 của mọi tệp `.py`, `.js`, `.css`, `.html` và `.svg` trong gói), mà một bản checkout của cam kết đó sẽ tái tạo trừ khi các tệp đã bị thay đổi. Telegram được đặt tên theo thư viện, lớp API và trung tâm dữ liệu của nó. Khi quá trình quan sát bắt đầu và khi việc xuất dữ liệu trò chuyện bắt đầu và kết thúc, bộ thu thập sẽ yêu cầu Telegram cung cấp thời gian của nó (`updates.getState`, tính theo giây nguyên) và ghi lại thời gian của Telegram trừ đi thời gian trên đồng hồ của bộ thu thập, kèm theo độ không chắc chắn do thời gian truyền đi và về; các báo cáo hiển thị các phép đo này trong phần Chuỗi lưu giữ. Việc xuất dữ liệu trò chuyện cũng ghi lại thời điểm nó đọc lịch sử, ngoài các ngày tháng của các tin nhắn.

### Hướng dẫn sử dụng trình xem báo cáo ngoại tuyến và lưu trữ

Giải nén toàn bộ tệp ZIP trước khi mở `chat.html` hoặc `report.html`. Trình xem cung cấp các tính năng tìm kiếm, bộ lọc, danh sách người tham gia, chỉ báo, chi tiết bản ghi và lựa chọn JSON/CSV mà không cần máy chủ. Giữ `viewer/` và `media/` bên cạnh báo cáo. Các lựa chọn là các bản sao: sử dụng `verify.py SELECTION.json
--evidence ARCHIVE.zip` để so sánh chúng với kho lưu trữ đã ký. Trình xác minh kiểm tra ID báo cáo, khóa ký, ranh giới tệp lưu trữ và mọi mục đã chọn; các mục bị chỉnh sửa, thiếu hoặc trùng lặp sẽ bị từ chối. Ghi chú lựa chọn và thời gian tạo vẫn là siêu dữ liệu chưa được ký.

Khoảng trống giữa các số tin nhắn chỉ được hiển thị đối với luồng trò chuyện đầy đủ, chưa qua lọc và theo thứ tự tăng dần. Việc ẩn một danh mục hoặc không tải được một khối dữ liệu không được coi là bằng chứng cho việc thiếu tin nhắn. Tính năng đánh dấu tìm kiếm hoạt động trên văn bản thuần túy trước khi thực hiện mã hóa HTML, đồng thời giữ nguyên các thẻ đánh dấu nguyên văn.

Trình duyệt kiểm tra chữ ký của tệp manifest, ID báo cáo và khóa, cũng như tất cả các giá trị băm tệp được liệt kê. Nó từ chối các cấu trúc ZIP không rõ ràng hoặc bị lỗi, tên trùng lặp và đường dẫn không an toàn, đồng thời giới hạn kích thước tệp tối đa 256 MiB và tổng dung lượng nội dung được khai báo là 4 GiB. Sử dụng công cụ xác minh độc lập cho các tệp lưu trữ lớn hơn. Việc kiểm tra bằng trình duyệt này bổ sung cho các kiểm tra của trình xác minh về chuỗi nhật ký và ngữ nghĩa dữ liệu.

`README.txt` chứa hướng dẫn bắt đầu, danh mục tệp được sắp xếp theo thứ tự, hướng dẫn xác minh và ghi chú về định dạng dữ liệu bằng ngôn ngữ của báo cáo, tiếp theo là hướng dẫn đầy đủ bằng tiếng Anh. `SHA256SUMS` bao gồm các tệp được liệt kê trong đó, không bao gồm chính tệp này, `manifest.json` và `manifest.sig`; bản kê khai có chữ ký cũng bao gồm `SHA256SUMS`. Giữ nguyên tệp ZIP gốc và lưu các tệp làm việc bên ngoài thư mục đã giải nén. Các báo cáo PDF bao gồm các dấu trang phần và mã nhận dạng vụ việc/báo cáo ở các trang sau.

### Cuộc trò chuyện tại thời điểm xuất

Một bản xuất cuộc trò chuyện ghi lại những gì Telegram đã nêu về cuộc trò chuyện khi quá trình xuất bắt đầu: các nhãn riêng của Telegram (`scam`, `fake`, `restricted` kèm lý do, `verified`), tên người dùng, mô tả, số lượng thành viên và quản trị viên, cuộc thảo luận liên kết, bảo vệ nội dung, liệu thành viên mới có thể xem các tin nhắn trước đó hay không và từ tin nhắn nào trở đi tài khoản này có thể xem lịch sử (`available_min_id`), ngày của tin nhắn 1 khi đó là thời điểm tạo cuộc trò chuyện, và SHA-256 của ảnh đại diện cuộc trò chuyện (được lưu trong `media/`). Nó ghi lại vị trí của tài khoản xuất dữ liệu trong cuộc trò chuyện: vai trò, ngày tham gia, người đã mời tài khoản đó và, đối với quản trị viên, các quyền hạn của họ. Một yêu cầu bị Telegram từ chối sẽ được nêu tên thay thế.

Khi tài khoản xuất dữ liệu là quản trị viên, quá trình xuất sẽ đọc nhật ký quản trị của cuộc trò chuyện (Telegram lưu trữ trong khoảng 48 giờ) vào `admin-log.json`: các thao tác xóa và chỉnh sửa kèm theo nội dung và tài khoản thực hiện. Đây là bản ghi duy nhất về việc xóa có ghi rõ người đã xóa.

### Các chỉ số

Danh sách báo cáo và kho lưu trữ được đánh số là `indicators.csv` , `indicators.stix.json` (STIX 2.1 ) và `indicators.misp.json` (sự kiện MISP ), những thông tin mà bộ phận xử lý vi phạm có thể can thiệp trong các tin nhắn đã ghi lại: liên kết và tên miền (kể cả những liên kết ẩn sau văn bản, trong các nút bấm và trong bản xem trước liên kết), địa chỉ tiền điện tử, tên người dùng và liên kết mời Telegram , số điện thoại, địa chỉ email và hình ảnh đã lưu. Các địa chỉ Bitcoin, Litecoin, Dogecoin và TRON chỉ được liệt kê khi tổng kiểm tra base58 của chúng hợp lệ, các địa chỉ SegWit khi tổng kiểm tra bech32 hoặc bech32m của chúng hợp lệ và các địa chỉ TON khi tổng kiểm tra CRC của chúng hợp lệ; các địa chỉ EVM và Solana được đánh dấu là chưa được kiểm tra. Hình ảnh chứa SHA-256 và một hàm băm nhận thức (dHash, 64 bit) mà các bản sao được nén lại hoặc thay đổi kích thước vẫn giữ gần như nguyên vẹn. Các báo cáo ghi các chỉ báo để chúng không bị mở ngẫu nhiên (`hxxps[://]example[.]com` ); các tệp vẫn giữ nguyên các giá trị như ban đầu. Mỗi chỉ báo được đánh dấu là “không xác định” và “không dành cho phát hiện tự động” (STIX , `indicator_types: unknown` , MISP , `to_ids: false` , phân phối cho tổ chức của chính mình): việc được liệt kê chỉ cho biết tin nhắn chứa chỉ báo đó, chứ không phải nó là độc hại. Một liên kết có văn bản hiển thị địa chỉ khác với địa chỉ thực tế khi mở sẽ được đánh dấu trong báo cáo.

Các báo cáo PDF kết thúc bằng tuyên bố của người kiểm tra để ký tay, danh sách kiểm tra dành cho công chứng viên hoặc chuyên gia tòa án, và mã QR (cũng có trên trang đầu tiên) chứa ID báo cáo, dấu vân tay khóa và SHA-256 của dữ liệu chính thức, để bản in có thể truy xuất trở lại kho lưu trữ của nó.

## Tiêu chuẩn hóa sự kiện

Dữ liệu đầu vào cho hàm băm bao gồm chính xác các trường sau:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

Hãy chuyển đổi dữ liệu sang định dạng JSON tương thích với Python, sử dụng mã hóa UTF-8, các khóa đối tượng được sắp xếp theo thứ tự, không sử dụng ký tự thoát ASCII, không chứa khoảng trắng không cần thiết và không chứa các giá trị NaN/vô cực:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

Giá trị SHA-256 của các byte đó sẽ trở thành hàm băm sự kiện. Chữ ký được tạo bằng thuật toán Ed25519 trên 32 byte hàm băm thô, sau đó được mã hóa theo chuẩn base64. Giá trị previous_hash đầu tiên là 64 số 0. Số thứ tự bắt đầu từ 1 và tăng dần từng đơn vị 1. Tất cả các sự kiện, bao gồm cả các sự kiện vận hành, đều chia sẻ chung một chuỗi. Không có cơ chế loại bỏ các bản ghi trùng lặp: các quan sát lặp lại được coi là các biên nhận riêng biệt, chứ không phải là khẳng định về các hành động riêng biệt trên Telegram.

Dữ liệu ngày tháng thô của Telegram là các chuỗi ISO; các trường nhị phân sẽ được chuyển đổi thành các đối tượng chứa bytes_base64. Nội dung tin nhắn, các thực thể, mô tả phương tiện, siêu dữ liệu phản hồi, phản ứng, và các hành động dịch vụ sẽ được lưu giữ trong siêu dữ liệu tin nhắn thô khi được cung cấp.

observed_at là thời gian theo đồng hồ UTC của bộ thu thập. source_at là ngày trên Telegram được cung cấp khi có sẵn. Thông báo xóa không cung cấp thời gian xóa chính xác, do đó source_at vẫn là null. Thứ tự nhận dữ liệu truyền tải không nhất thiết phải trùng khớp với thứ tự sự kiện nguồn . Các bản chụp lịch sử sử dụng ngày nguồn cũ hơn nhưng thời gian quan sát hiện tại.

## Ngữ nghĩa về các chủ thể

message.new actor_id là người gửi tin nhắn. message.edited không có thông tin suy luận về người chỉnh sửa; payload.sender_id ghi lại người gửi của tin nhắn được quan sát. Việc xóa actor_id vẫn giữ giá trị null. Các tin nhắn của dịch vụ thành viên vẫn giữ nguyên người gửi và loại hành động , mà không chuyển đổi mọi trường hợp xóa thành việc rời khỏi tự nguyện. Các bản cập nhật thô về người tham gia vẫn giữ nguyên actor_id như đã được cung cấp. Các bản chụp nhanh phản ứng không tạo ra một đối tượng thực hiện thay đổi.

Các thông báo xóa đối với các cuộc trò chuyện riêng tư và các nhóm thông thường chỉ chứa ID tin nhắn. Các cuộc trò chuyện này chia sẻ một dãy ID chung cho toàn bộ tài khoản, do đó một ID xác định một tin nhắn duy nhất của tài khoản này. Khi một tin nhắn có ID đó đã được lưu trước đó trong sổ nhật ký này, việc xóa sẽ được ghi lại trong cuộc trò chuyện đó dưới dạng message.deleted với tên phương thức là payload.chat_resolution. Các ID chưa từng được lưu sẽ được lưu giữ dưới dạng deletion.unscoped mà không có chat_id; không có bất kỳ giả định nào được đưa ra. Các kênh và siêu nhóm đánh số tin nhắn theo từng cuộc trò chuyện và không bao giờ được khớp theo cách này. Khi tin nhắn bị xóa được gửi bởi tài khoản được theo dõi, payload.deleted_message_was_outgoing có giá trị true; người xóa vẫn chưa được cung cấp.

An unscoped notice does not establish that a message was never saved: a matching chat may be outside the current observation scope, or a unique match may be unavailable. Recheck absence remains a separate observation from a deletion notification in report counts, filters and labels. A later recovery clears the current missing state while preserving the earlier unsuccessful check in the signed history; neither observation establishes a deletion notice.

Multiple IDs resolved to the same chat from one notification are grouped as `deletion.batch`, regardless of their count. The notification does not establish that the entire history was cleared, who performed the deletion, or whether it applied to all participants. Saved outgoing messages do not change these limits. Older journals may contain `history.cleared` events inferred from batches of ten or more IDs, with explanatory text attributing the deletion to the other participant. Those inferences are not supported by the update. Preserve those original signed records, but treat them as grouped deletion notifications; the current interface labels them accordingly.

## Phạm vi bao quát: tính liên tục, các khoảng trống và các ID không được ghi nhận

Mỗi tệp ZIP được ký số đều chứa tệp `coverage.json`; báo cáo HTML mở đầu bằng cùng một bản tóm tắt; và tệp `verify.py` sẽ tính toán lại bản tóm tắt này dựa trên tệp `events.jsonl` thay vì tin tưởng vào nội dung của tệp:

- **Quá trình quan sát diễn ra liên tục từ X đến Y.** Một khoảng thời gian bắt đầu bằng `observation.started` và kết thúc khi có tạm dừng, ngừng hoạt động, mất kết nối Telegram, đăng xuất, quá trình khởi động mà không có bước dừng đúng trình tự, hoặc khi không có bất kỳ bản ghi nào trong hơn ba phút trong quá trình quan sát (các tín hiệu kiểm tra trạng thái được ghi lại mỗi phút, do đó sự im lặng có nghĩa là quá trình đã dừng lại, bị treo hoặc máy tính đã chuyển sang chế độ ngủ). Khi khoảng thời gian giữa các tín hiệu kiểm tra trạng thái được thay đổi trong **phần Cài đặt**, mỗi tín hiệu kiểm tra trạng thái sẽ ghi lại thay đổi này và khoảng thời gian im lặng được phép sẽ là ba khoảng thời gian, không bao giờ ít hơn ba phút.
- **Danh sách các khoảng trống** liệt kê khoảng thời gian giữa các giai đoạn kèm theo lý do. Một khoảng trống vẫn còn tồn tại tại bản ghi cuối cùng sẽ được đánh dấu là `not_resumed_by_last_record`.
- **ID tin nhắn không được ghi nhận.** Đối với các kênh và siêu nhóm, nơi số tin nhắn được tính theo cuộc trò chuyện, các ID bị thiếu giữa các ID đã ghi nhận sẽ được liệt kê dưới dạng khoảng. Chúng được báo cáo là không*được ghi nhận* — đã bị xóa, chưa bao giờ được gửi hoặc nằm ngoài lịch sử đã lưu — chứ không bao giờ được ghi là đã bị xóa. Các cuộc trò chuyện riêng tư và nhóm thông thường chia sẻ một chuỗi ID chung cho toàn tài khoản, do đó các khoảng trống bên trong một cuộc trò chuyện như vậy không có ý nghĩa gì và không được liệt kê ở đó.
- Các thông báo về khoảng trống ở cấp độ cuộc trò chuyện (ví dụ: Telegram yêu cầu khôi phục dữ liệu bị thiếu trong một kênh) được tính là các ghi chú; chúng không làm gián đoạn phạm vi ghi lại toàn bộ.

### Số tin nhắn bị thiếu (`gap_summary`)

**Xem trước.** `coverage.json` → `gap_summary` đo lường các số mà Telegram đã gán và công cụ thu thập này chưa từng ghi nhận. Telegram đánh số tin nhắn một lần cho mỗi kênh hoặc siêu nhóm, và một lần cho mỗi tài khoản trên các cuộc trò chuyện riêng tư, bot và nhóm thông thường. Một số nằm giữa hai tin nhắn được quan sát có thể đã được quan sát hoặc bị thiếu; một khoảng liên tục là một khẳng định chắc chắn rằng mọi tin nhắn được đánh số trong khoảng đó đều đã được quan sát. Một khoảng trống không chỉ ra bất kỳ đối tượng nào cũng như không nêu lý do.

| Lĩnh vực | Ý nghĩa |
| --- | --- |
| `status` | `on`, hoặc `off` khi được tắt trong **mục Cài đặt → Phân tích khoảng trống** |
| `parameters` | Các tham số đã tạo ra kết quả, để có thể lặp lại quá trình này |
| `chats[]` | Mỗi kênh hoặc siêu nhóm tương ứng với một mục, mỗi mục được đánh số riêng biệt |
| `account` | Danh sách các cuộc trò chuyện riêng tư, bot và nhóm thông thường trên toàn tài khoản |
| `status` (theo từng chuỗi) | `applicable`, hoặc `not_applicable` với `reason` |
| `observed_from`, `observed_to`, `span` | Số đầu tiên và số cuối cùng được quan sát cùng với kích thước của phạm vi |
| `observed`, `observed_without_content` | Các số liệu quan sát được; những số liệu chỉ được biết thông qua bản ghi xóa hoặc kiểm tra lại |
| `missing`, `density`, `gap_ranges`, `largest_gap` | Số lần chưa từng được quan sát, tỷ lệ phần trăm của chúng trong phạm vi, số lần chạy, lần chạy dài nhất |
| `clusters[]` | Các lỗ hổng được liệt kê: `low`, `high`, `missing`, cùng với các số quan sát liền kề `after` / `before` cùng với thời gian quan sát của chúng |
| `service_estimate` | Chỉ khi được kích hoạt: số lượng số điện thoại thiếu sẽ là tin nhắn dịch vụ theo tỷ lệ quan sát được. Không bao giờ trừ đi từ `missing` |

Tính hợp lệ được xác định dựa trên nhật ký, không bao giờ được giả định:

- **Các kênh và siêu nhóm** được đo lường theo từng cuộc trò chuyện, bao gồm cả khi xuất dữ liệu từ các cuộc trò chuyện đã chọn. Các bản ghi được người gửi chọn sẽ được sử dụng để thực hiện phép đo `not_applicable`.
- **Dãy tin nhắn trên toàn tài khoản** chỉ được tính từ tin nhắn đầu tiên đến tin nhắn cuối cùng được nhận trong thời gian chế độ thu thập toàn bộ tài khoản đang hoạt động và bao gồm các cuộc trò chuyện riêng tư, bot, nhóm thông thường và các tin nhắn của chính tài khoản đó, không loại trừ bất kỳ cuộc trò chuyện nào (`scope.changed`). Các số được chỉ định bởi `deletion.unscoped` được tính là đã quan sát được mà không bao gồm nội dung. Việc xuất hoặc chuyển giao các cuộc trò chuyện được chọn không thể đo lường được điều này. Nếu chế độ thu thập toàn bộ tài khoản đã được tắt và bật lại, một ghi chú sẽ cho biết rằng các số được sử dụng trong khoảng thời gian đó sẽ xuất hiện dưới dạng khoảng trống.
- Các tin nhắn dịch vụ là các bản ghi nhật ký có số thứ tự riêng, do đó chúng tự động lấp đầy các khoảng trống của chính mình; ước tính tùy chọn chỉ mang tính chất bối cảnh.

`verify.py` tính toán lại `gap_summary` từ `events.jsonl` với các tham số trong `coverage.json` (giá trị mặc định cho các kho lưu trữ cũ hơn) và in dòng toàn tài khoản trong bản tóm tắt phạm vi phủ sóng của nó. `get_capture_status`(MCP và dòng lệnh) trả về cùng một kết quả đo lường cho các cuộc trò chuyện mà một quyền truy cập có thể đọc; dãy dữ liệu toàn tài khoản chỉ áp dụng cho quyền truy cập bao phủ toàn bộ không gian làm việc.

Repeated observations of one service message count once, and the account service estimate uses only numbers inside the measured range. An applied scope must explicitly preserve the account's own messages before account-wide measurement is enabled; older records without that information cannot establish this condition. Stopped observation does not extend the measured range, and resuming it is noted. The live archive query has a time budget, including its database scan, and marks an unfinished measurement as partial.

Telegram documents the [separate message ID sequences](https://core.telegram.org/api/updates#message-id-sequences). These numbers describe observations; they do not identify a deletion actor or establish why a number is absent.

Khi Telegram ngừng chấp nhận tài khoản, bản ghi `coverage.gap` kết thúc quá trình giám sát sẽ chứa `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended` hoặc `not_authorized`) và lỗi Telegram; `verify.py` chỉ ra nguyên nhân khiến giai đoạn này kết thúc.

Coverage combines recorded observation periods, interruptions and message outcomes. Assess it together with the selected chats, period and attachment policy; continuous operation alone does not establish complete delivery of Telegram updates.

## Người sản xuất

Bản kê khai có chữ ký của các tệp ZIP bằng chứng, bản xuất cuộc trò chuyện, nhật ký chứng cứ và tuyên bố về các tệp hồ sơ cá nhân chứa thông tin `producer` : phần mềm, phiên bản, dự án (PhishDestroy), trang chủ và kho lưu trữ mã nguồn. Báo cáo HTML hiển thị dòng thông tin tương tự, và `verify.py` in thông tin này như một phần của nội dung đã được xác minh. Các tệp lưu trữ được tạo ra trước khi trường này tồn tại sẽ được xác minh như trước đây và được báo cáo là không nêu tên người tạo.

Mỗi bản ghi `observation.started` cũng nêu tên máy khách Telegram đã thực hiện việc giám sát: mã `api_id` (không bao giờ là giá trị băm), cho dù đó là cặp công khai tích hợp sẵn hay ứng dụng riêng của nhà điều hành, mô tả máy khách được gửi trong yêu cầu kết nối của Telegram, và loại đường dẫn kết nối cùng chế độ IP (không có địa chỉ proxy hoặc khóa bí mật). Báo cáo và `custody.json` liệt kê mọi máy khách và tuyến đường riêng biệt cùng thời điểm chúng được ghi lại, cũng như các thời điểm không có proxy nào trong danh sách trả lời và Telegram đã phát hiện địa chỉ máy chủ. Các nhật ký được ghi lại trước đó đã nêu rõ điều này.

## Hồ sơ cá nhân

Một tệp hồ sơ (`tgwitness-dossier-v1`, JSON) được tạo theo yêu cầu từ các bản ghi đã có sẵn trong sổ nhật ký cho một cuộc trò chuyện; không có dữ liệu nào được lấy từ Telegram và nội dung hồ sơ không bao giờ được ghi vào sổ nhật ký (việc bật và tắt hồ sơ được ghi lại dưới dạng `dossier.changed`). Đối với mỗi người dùng có tin nhắn được lưu, công cụ sẽ liệt kê tên và lịch sử tên người dùng, các cờ cảnh báo của Telegram (bot, lừa đảo, giả mạo, tài khoản cao cấp, đã xác minh, bị hạn chế, đã xóa) như được hiển thị tại thời điểm lưu trữ, thẻ nhận dạng ảnh, mã băm SHA-256 và mã băm nhận thức (pHash, tương thích với `imagehash.phash`) của hình đại diện từ bộ nhớ đệm hình đại diện cục bộ cùng các hình đại diện tương tự, hoạt động (tin nhắn đầu tiên và cuối cùng, số lượng, các bài chia sẻ đã chỉnh sửa và xóa, tin nhắn theo giờ UTC), ai trả lời ai, các cuộc trò chuyện khác trong nhật ký này mà người đó đã viết, cùng các ví được đề cập (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL; các địa chỉ Base58Check đã được xác thực tổng kiểm tra), số điện thoại, tên người dùng và các liên kết, bao gồm cả các liên kết ẩn sau văn bản.

Mỗi sự kiện đều liệt kê các bản ghi trong sổ nhật ký (`seq`) mà nó xuất phát, và `record_hashes` chứa giá trị băm của từng bản ghi được tham chiếu. Tuyên bố này được ký bằng khóa không gian làm việc:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

kiểm tra chữ ký, xác minh chính bản xuất bằng chứng (chữ ký, chuỗi băm và các tệp) cũng như đảm bảo mọi bản ghi được tham chiếu đều tồn tại nguyên vẹn trong bản xuất đó của cùng một không gian làm việc. Các giá trị băm của ảnh đại diện được ghi chú là lấy từ bộ nhớ đệm cục bộ (không phải bản ghi trong sổ nhật ký). Các đề cập là kết quả khớp mẫu — là manh mối cần kiểm tra, không phải sự thật đã được xác minh. Các hồ sơ được kích hoạt theo từng cuộc trò chuyện, có thể được xuất dưới dạng tệp ZIP mã hóa AES-256 kèm mật khẩu, và sẽ bị xóa khi bị tắt hoặc khi cuộc trò chuyện bị xóa khỏi các nguồn.

## Nhân chứng độc lập

Một sổ nhật ký chứng cứ (`tgwitness-witness-v1`) cùng các bài đăng trên kênh của nó sẽ được đối chiếu với tệp xuất chứng cứ bằng `verify.py --witness … --channel …`; xin tham khảo phần [“chứng cứ độc lập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/)”.

## Bản kê khai và các điểm kiểm tra

Tệp manifest.json bao gồm định dạng, thời gian xuất, khóa công khai, dấu vân tay, độ dài nhật ký, băm đầu, phạm vi, nhà sản xuất, các giới hạn và giá trị SHA-256 của mọi thành phần nội dung ngoại trừ chính các thành phần `manifest.json` và `manifest.sig`. Tệp manifest.sig là chữ ký Ed25519 mã hóa base64 trên tệp JSON manifest chuẩn. Công cụ xác minh sẽ từ chối các thành phần bất thường hoặc thiếu sót, tên trùng lặp, tệp bị hỏng, chuỗi/dãy bị gián đoạn, chữ ký không hợp lệ và sự không khớp với điểm kiểm tra được cung cấp. Công cụ này không bao giờ trích xuất đường dẫn lưu trữ. Công cụ này giới hạn tổng kích thước khai báo sau khi giải nén ở mức 4 GiB; tệp `--max-gib N` cho phép các tệp lưu trữ có kích thước lớn hơn được tạo ra nhờ giới hạn **tham số** được nâng cao.

Run verification from your installed TgWitness version or a reviewed checkout. The copy included in an archive supports portable use; check that copy against your trusted installation before executing it.

A checkpoint signs a statement containing the public key, journal length, head hash, and creation time. The verifier can check that a later archive contains the same prefix. Retain the checkpoint outside the collector, so later verification compares the archive with a reference held separately from it.

## Phạm vi xác minh

Verification checks the archive and the collection mode used to produce it. Choose the mode whose trust boundary matches the case, then retain its verification inputs.

| Chế độ thu thập | Những gì trình xác minh kiểm tra | Dữ liệu đầu vào xác minh và ranh giới tin cậy |
| --- | --- | --- |
| Không gian làm việc cục bộ | Record signatures, hash chain, manifest and attachment bytes | Independently retained collector fingerprint; the host administrator controls the local signing key |
| Không gian làm việc cục bộ với một nhân chứng độc lập | Việc kiểm tra kho lưu trữ cùng với sự nhất quán với tiền tố nhật ký trước đó được người làm chứng lưu giữ | Separately trusted witness key and records; the checkpoint binds the prefix already observed |
| [GitHub Actions ghi lại](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) | GitHub attestation of the archive digest, approved workflow and collector commits, hosted runner, fresh session/key origin and internal archive integrity | Trusted verifier policy, caller repository and GitHub attestation bundle; collection runs under the pinned workflow |
| [Triển khai trên đám mây](https://phishdestroy.github.io/TgWitness/vi/docs/reference/high-assurance/) | Provider lifecycle and access records, firewall and Cloudflare state, plus the collector's signed run record | Read-only queries to the provider and Cloudflare; availability of individual checks depends on the provider |
| [Máy ảo (VM) bảo mật Intel TDX](https://phishdestroy.github.io/TgWitness/vi/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx) | Quote signature and platform status, binding to the collector statement, compose and OS measurements | Intel trust chain and expected deployment measurements; retain the results of every required TDX check |

In sealed acquisition, the approved collector receives data through an authenticated Telegram connection inside the verified environment. Attestation binds the archive to that execution, so verification covers acquisition as well as later file integrity. This relies on the approved code and the platform trust chain listed above. GitHub capture verification requires a session created inside the run and rejects imported-session captures.

The run receipt records the collector version, file hashes and startup settings. GitHub provenance and TDX measurements provide the environment checks; the [validation record](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/) identifies tested configurations.

TgWitness signs the observations it collects; Telegram and message authors do not issue these signatures. In a local workspace, material created before the first independent checkpoint still depends on the collector and its key holder. Coverage records describe the selected scope and collection outcomes, while verified external timestamps anchor the committed archive or journal boundary in time.

## Tệp đính kèm

Các tệp được định danh bằng mã băm SHA-256 trong thư mục media/. Một sự kiện media.saved liên kết mã băm và độ dài byte với một sự kiện tin nhắn cụ thể. Tên tệp gốc là siêu dữ liệu, không bao giờ là đường dẫn cục bộ. Các byte phương tiện được tải xuống theo cơ chế không đồng bộ, do đó việc xóa ngay lập tức có thể ngăn cản quá trình ghi lại. Các trường hợp như việc thu thập bị vô hiệu hóa, tệp quá lớn/không xác định kích thước, lỗi tải xuống, và quá trình tải xuống bị gián đoạn đều được hiển thị dưới dạng kết quả. Sự cố sập hệ thống có thể để lại các tệp không hoàn chỉnh không có tham chiếu; những tệp này sẽ không được bao gồm trong các bản xuất.

Trình xuất ZIP sẽ xác minh các tệp phương tiện được lưu trữ dựa trên tên của chúng. Các định dạng xuất JSONL, CSV và HTML sẽ xác minh chữ ký sự kiện nhưng không chứa dữ liệu phương tiện. Các báo cáo phái sinh chỉ mang tính tiện lợi; tệp events.jsonl mới là bản ghi sự kiện chính thức.

Việc xuất toàn bộ cuộc trò chuyện sẽ lưu các tệp đính kèm theo cài đặt tệp đính kèm của không gian làm việc vào thư mục media/, được đặt tên theo định dạng SHA-256. Mỗi bản ghi tin nhắn trong chat.json sẽ ghi tên tệp của nó (`file`, `file_sha256`) hoặc lý do tại sao nó vắng mặt (`file_status`), cùng với những gì người đọc đã thấy xung quanh văn bản: các liên kết phía sau văn bản, nguồn gốc chuyển tiếp, các nút bot, chữ ký, lượt xem và bộ đếm thời gian tự động xóa. `verify.py` kiểm tra xem mọi tệp được đặt tên có nằm trong bản kê khai đã ký dưới mã băm đó hay không.

## Thu thập và xử lý bằng chứng bền vững (0.2)

Một tác vụ phương tiện và sự kiện tin nhắn tương ứng được ghi lại trong một giao dịch duy nhất. Tác vụ này lưu trữ mô tả tin nhắn TL gốc; quan sát có chữ ký liên kết mã SHA-256, tài khoản và chính sách kích thước của nó. Quá trình khôi phục sẽ xác minh liên kết đó trước khi tải xuống. Hệ thống không bao giờ truy xuất tin nhắn hiện tại mà sẽ âm thầm thay thế bằng tệp đính kèm mới hơn. Các tác vụ bị gián đoạn sẽ được thử lại, trong khi lỗi vĩnh viễn vẫn là một kết quả rõ ràng.

Each workspace has its own journal and signing identity. A process.started event includes a run ID, local clocks, dependency versions, source-file hashes, initial account/scope, and capture settings. Heartbeats include the run ID, monotonic time, and queue state. The run receipt can also be downloaded as a separately signed statement. For verification of the execution environment, pair it with the GitHub attestation or TDX checks described in [Verification scope](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope).

Automatic checkpoints are retained locally on startup, every five minutes while observing (**Parameters → Signed checkpoint every**), and on orderly stop. Startup verification and export compare the journal against the latest retained local checkpoint. This can detect a database rollback when the checkpoint survives. Independent retention keeps that reference available outside the workspace; a verified external timestamp additionally anchors it in time.

Sau khi khởi động lại, vị trí cập nhật Telegram đã lưu sẽ được khôi phục (`catch_up_from` trong `observation.started`) và hệ thống sẽ yêu cầu các bản cập nhật bị bỏ lỡ. Quá trình kiểm tra lại định kỳ sẽ ghi lại `message.recovered` đối với các tin nhắn bị bỏ lỡ và `message.missing_on_recheck` khi Telegram không còn trả về tin nhắn đã lưu; trường hợp sau không phải là thông báo xóa và không nêu tên người xóa cũng như thời gian.

### Sao lưu và khôi phục ngoài trang web (S3)

Bản sao ngoài trang web (Tính năng Xuất dữ liệu, mặc định là tắt) sẽ tải lên các phân đoạn nhật ký, tệp tin được lưu giữ, các điểm kiểm tra cùng với dấu thời gian của chúng và các bản xuất cuộc trò chuyện đã hoàn tất lên bộ lưu trữ tương thích với S3, được mã hóa bằng AES-256-GCM trước khi tải lên bằng khóa được lưu trữ trong kho lưu trữ của không gian làm việc; tính năng lưu giữ Object Lock sẽ được áp dụng khi bucket hỗ trợ tính năng này. Nếu không có khóa đã tải xuống, bản sao này sẽ không thể được đọc. Khôi phục và xác minh bằng `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Quá trình khôi phục yêu cầu một thư mục thông thường trống. Các tệp tải xuống và các đối tượng đã được giải mã sẽ được lưu giữ trong bộ nhớ tạm thời riêng tư cho đến khi toàn bộ nhật ký và mọi điểm kiểm tra được lưu giữ đều được xác minh. Các đường dẫn đối tượng không an toàn, phạm vi phân đoạn không nhất quán và các nhật ký ngắn hơn một điểm kiểm tra sẽ bị từ chối; nếu xác minh thất bại, hệ thống sẽ không công bố bất kỳ tệp nào đã được khôi phục. Các kiểm tra thời hạn lưu giữ sẽ so sánh chế độ Object Lock và ngày tháng được trả về với thời hạn được gửi khi tải lên (dung sai làm tròn là một giây). Thời hạn đã hết hạn, không hợp lệ hoặc bị rút ngắn sẽ không được coi là đã được xác minh. Trạng thái báo cáo đối tượng được lấy mẫu mà thời hạn lưu giữ của nó đã được đọc lại cho lần tải lên đó.

Các tệp phương tiện cục bộ bị thiếu hoặc bị hỏng sẽ được báo cáo là lỗi của lần xử lý và con trỏ phương tiện sẽ được giữ lại trước vị trí đó, để tệp này được thử lại trong lần xử lý tiếp theo; các tệp, điểm kiểm tra và tệp xuất sau đó vẫn được sao chép. Quá trình khôi phục sẽ kiểm tra tất cả các tham chiếu đến phương tiện được lưu giữ so với các hàm băm đã được giải mã và kích thước đã ghi lại. Các phân đoạn nhật ký trùng lặp giống hệt nhau từ các lần tải lên bị gián đoạn sẽ được loại bỏ trùng lặp; các phần trùng lặp mâu thuẫn sẽ bị từ chối. Các điểm kiểm tra được tạo ra trong quá trình tải lên sẽ được hoãn lại cho đến khi các bản ghi nhật ký liên quan đã được sao chép, do đó một lần quét hoàn tất sẽ không công bố điểm kiểm tra trước khi nhật ký tương ứng được hoàn tất.

### Xuất các bản chụp nhanh theo thời gian thực

Việc xuất dữ liệu theo thời gian thực sử dụng một bản chụp nhanh đọc ổn định từ cơ sở dữ liệu SQLite. Phần đầu của bản chụp nhanh này có thể cũ hơn so với sổ nhật ký trực tiếp hiện tại khi quá trình tải xuống hoàn tất. Một điểm kiểm tra được tạo ra sau bản chụp nhanh đó có thể báo cáo chính xác rằng kho lưu trữ ngắn hơn; hãy so sánh với một điểm kiểm tra tại hoặc trước tiền tố đã xuất, chứ không phải một điểm kiểm tra ngẫu nhiên nào đó sau đó.

## Chuẩn bị theo RFC 3161 và xác minh phản hồi (0.2)

Chế độ bằng chứng (tắt theo mặc định) chỉ gửi mã SHA-256 của từng điểm kiểm tra đã được ký đến các cơ quan có thẩm quyền theo tiêu chuẩn RFC 3161 và các lịch OpenTimestamps đã liệt kê, thông qua tuyến đường không gian làm việc và tuyệt đối không qua MTProxy. Các kết quả được lưu trữ trong `checkpoints/anchors/`, xuất ra và kiểm tra bằng `verify.py` (`--tsa-ca` kiểm tra chữ ký TSA; xác nhận các bằng chứng OpenTimestamps bằng `ots upgrade` và `ots verify`).

Bảng điều khiển sẽ chuẩn bị một kho lưu trữ yêu cầu chứa các byte chuẩn của tệp checkpoint.json, dấu vân tay tin nhắn SHA-256 và giá trị ngẫu nhiên (nonce) trong tệp timestamp.tsq, các tổng kiểm tra (checksums) cùng hướng dẫn. Không có yêu cầu mạng nào được thực hiện. Quá trình chuẩn bị này không phải là dấu thời gian đáng tin cậy.

`python -m tgwitness.anchor verify` gọi hàm OpenSSL ts hai lần: một lần đối với các byte điểm kiểm tra và một lần đối với yêu cầu ban đầu. Tệp CA đáng tin cậy phải được chỉ định rõ ràng; các chứng chỉ đi kèm sẽ không tự động được coi là đáng tin cậy. Việc kiểm tra yêu cầu là tùy chọn tại giao diện dòng lệnh (CLI), do đó quý vị cần giữ lại và cung cấp tham số --request để kiểm tra mã ngẫu nhiên (nonce). Kết quả sẽ cho biết liệu việc kiểm tra đã được thực hiện hay chưa. Chữ ký điểm kiểm tra của bộ thu thập và nhật ký vẫn phải được xác minh riêng biệt bằng dấu vân tay đáng tin cậy của bộ thu thập.

Quá trình xác minh kiểm tra chữ ký phản hồi, các byte điểm kiểm tra và, nếu có, yêu cầu gốc theo chứng chỉ CA được chỉ định. Việc kiểm tra thu hồi và xác thực lưu trữ dài hạn sau khi chứng chỉ hết hạn nằm ngoài phạm vi của trình xác minh hiện tại. Xem [quy](https://phishdestroy.github.io/TgWitness/vi/docs/reference/timestamp/) [trình](https://phishdestroy.github.io/TgWitness/vi/docs/reference/timestamp/) và [kết quả xác thực](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/).

## Các bản ghi tùy chọn trong chế độ bằng chứng: drand và các thiết bị Telegram

Hai bản ghi khác có thể chạy trên cùng các lần quét với các dấu thời gian. Cả hai đều bị tắt theo mặc định và chỉ có hiệu lực khi chế độ bằng chứng được bật: Extras → Evidence & backups → **More witnesses · tùy chọn**, hoặc `"drand": true` và `"devices": true` trong `POST /api/evidence`. Một bản ghi gặp sự cố sẽ không làm gián đoạn bản ghi khác hoặc các dấu thời gian; bảng điều khiển hiển thị kết quả mới nhất của từng bản ghi bên dưới biểu mẫu.

**drand** (`beacon.drand` ). Mỗi lần chạy sẽ ghi vòng drand quicknet mới nhất, tức là sự ngẫu nhiên công khai của League of Entropy (một vòng mỗi 3 giây), vào nhật ký: `chain` , `round` , `randomness` , `signature` , `round_time` và `relay` đã phản hồi. Một vòng được xác minh và không thể dự đoán trước cung cấp mốc thời gian tham chiếu thấp hơn cho tài liệu được liên kết bằng hàm băm tiếp theo. Dấu thời gian đã được xác minh tại một điểm kiểm tra sau đó cung cấp mốc thời gian trên. Các kiểm tra này giới hạn phạm vi của dữ liệu được liên kết; phạm vi thu thập được đánh giá riêng biệt. Trình thu thập sẽ truy vấn `drand.cloudflare.com` trước tiên, sau đó là các trạm trung chuyển của Protocol Labs, thông qua tuyến đường không gian làm việc, mỗi lượt thực hiện một yêu cầu.

`verify.py` kiểm tra xem mỗi giá trị ngẫu nhiên có phải là SHA-256 của chữ ký của nó hay không và liệu thời gian vòng lặp có chính xác hay không, đồng thời báo cáo số vòng lặp, khoảng thời gian dài nhất không có vòng lặp và độ trễ giữa drand và đồng hồ của bộ thu thập. Nó không kiểm tra chữ ký BLS. `--check-drand` so sánh các vòng với một trạm trung chuyển Cloudflare và một trạm trung chuyển Protocol Labs, tất cả các trạm hoặc một mẫu ngẫu nhiên gồm 100 trạm trong một nhật ký dài; một vòng có sự khác biệt sẽ không qua được quá trình xác minh.

**, Telegram,** (`account.devices`). Mỗi lần quét sẽ đọc các phiên của tài khoản bằng `account.getAuthorizations`, danh sách Telegram hiển thị trong Cài đặt → Thiết bị, và ghi lại: toàn bộ khi có thay đổi so với lần quét trước, kèm theo các mã băm phiên `added` và `removed`, nếu không thì chỉ ghi lại số lượng và SHA-256. Mẫu thiết bị, nền tảng, ứng dụng và phiên bản, thời gian tạo và hoạt động gần nhất, quốc gia và khu vực được lưu giữ; địa chỉ IP thì không, vì việc xuất bằng chứng nằm ngoài tầm kiểm soát của bạn. Phiên làm việc của chính bộ thu thập luôn hoạt động, do đó chỉ hoạt động của các phiên khác mới được tính là sự thay đổi. `verify.py` báo cáo tần suất danh sách được ghi lại cũng như mỗi phiên mới và phiên đã kết thúc. Nó chỉ đọc danh sách khi quá trình quan sát đang diễn ra.

Những gì họ không thể hiện: drand chỉ chứng minh thứ tự của các bản ghi so với thời gian công khai, và danh sách thiết bị là tuyên bố của Telegram thông qua bộ thu thập, được bộ thu thập ký tên giống như mọi bản ghi khác.

**Nhật ký Cloudflare Gateway** (`cloudflare.gateway_dns`). Đối với máy chủ giải quyết qua Cloudflare Gateway ([Gateway DNS](https://phishdestroy.github.io/TgWitness/vi/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)), mỗi lần sao chép sẽ sao chép những gì Gateway đã ghi lại kể từ lần sao chép trước: một bản ghi cho mỗi khoảng thời gian tối đa ba giờ với `from`, `until`, `location_id`, `address` của máy chủ khi có thiết lập, và `queries` dưới dạng `[at, name, type, rcode, decision, colo]`, ngay cả khi không có bản ghi nào. Thiết lập trong **(Nhật ký Cloudflare Gateway)**: tài khoản, vị trí, địa chỉ tùy chọn và mã thông báo chỉ đọc (Đọc phân tích; Đọc PII Zero Trust để lưu một địa chỉ của vị trí chia sẻ). Bảng điều khiển kiểm tra Analytics Read; Zero Trust PII Read để lưu một địa chỉ của vị trí chia sẻ). Bảng điều khiển kiểm tra chúng bằng một yêu cầu trước khi lưu; mã thông báo vẫn được mã hóa và không bao giờ xuất hiện trong nhật ký. `verify.py` liệt kê các cửa sổ, các tên được tra cứu nhiều nhất và bất kỳ khoảng thời gian nào không có bản sao nào bao phủ; một bản ghi có số lượng không khớp với các truy vấn của nó sẽ bị lỗi. Một cửa sổ chứa hơn một trang truy vấn trong một giây sẽ giữ lại trang đó và báo rằng phần còn lại bị thiếu. Bản sao là phản hồi của Cloudflare thông qua bộ thu thập, được bộ thu thập ký tên; trong vòng 24 giờ, bất kỳ ai có mã thông báo chỉ đọc đều có thể so sánh nó với Cloudflare.
