# Định dạng bằng chứng

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/

Nội dung của tệp ZIP đã được ký, các loại bản ghi, biên nhận giao dịch, hồ sơ người dùng, bản sao lưu ngoài trang web và xác minh ngoại tuyến.

Một quan sát không phải là một kết luận. ID người gửi không phải là danh tính trong thế giới thực. Nguồn thông tin là bản cập nhật dịch vụ hiển thị trên tài khoản; Telegram không thực hiện việc ký số các bản ghi đã lưu này dành cho các nhà điều tra bên thứ ba.

## “Được ký” là gì

| Nội dung | Bảo vệ | Những nội dung cần lưu giữ |
| --- | --- | --- |
| Mọi ghi nhận trong nhật ký, bao gồm các sự kiện hoạt động | Chuỗi SHA-256 và chữ ký Ed25519 cho mỗi sự kiện | `events.jsonl` gốc, dấu vân tay khóa đáng tin cậy, và điểm kiểm tra được lưu giữ |
| Nội dung tệp ZIP chứa bằng chứng | `manifest.sig` ký vào bản kê khai chuẩn, trong đó liệt kê các giá trị băm của các tệp nội dung | Tệp ZIP đầy đủ, bao gồm tệp manifest và chữ ký |
| Tệp đính kèm được lưu giữ | Giá trị SHA-256 và số byte trong một sự kiện `media.saved` có chữ ký; băm tệp trong bản kê khai ZIP có chữ ký | Các byte gốc bên trong tệp ZIP đã được xác minh |
| Checkpoint | Chữ ký Ed25519 trên độ dài sổ ghi chép, băm tiêu đề, khóa công khai và thời gian tạo | Một bản sao độc lập được lưu giữ trước khi có thay đổi gây tranh cãi |
| Biên lai giao dịch | Các số liệu thu thập được ký riêng biệt; đồng thời cũng được bao gồm trong sự kiện `process.started` đã được ký | Biên bản ghi nhận và sổ nhật ký liên quan; các số liệu được tự báo cáo |
| Dạng tệp CSV hoặc HTML độc lập | Không có chữ ký mật mã độc lập; chỉ riêng các giá trị băm sự kiện là chưa đủ | Vui lòng sử dụng bản sao chính xác có trong tệp ZIP đã được xác minh để kiểm tra tính toàn vẹn |
| Ảnh chụp màn hình, bản in hoặc tệp PDF được tạo ra từ trình duyệt | Không có chữ ký của TgWitness trên bản sao | Vui lòng giữ lại gói phần mềm gốc đã được xác minh và ghi chép lại quy trình tạo ra phiên bản phái sinh |

Công cụ thu thập sẽ xác minh chữ ký của nhật ký trước khi tạo ra mọi định dạng xuất dữ liệu. Việc kiểm tra nguồn này không tạo ra chữ ký trên tệp CSV hoặc HTML được tải xuống riêng biệt. Tương tự, một chữ ký sự kiện JSONL hợp lệ cũng không cung cấp các byte đính kèm hoặc độc lập xác nhận rằng toàn bộ nhật ký đã quan sát được đã được cung cấp đầy đủ.

## Chuyển giao cuộc điều tra

1. Vui lòng ghi lại mã số vụ việc, người vận hành, ID tài khoản Telegram dạng số, các nguồn đã chọn, chính sách thu thập và khoảng thời gian thu thập vào ghi chú vụ việc của quý vị. TgWitness lưu giữ các quan sát; việc phân công vụ việc và hồ sơ lưu giữ được quản lý bên ngoài ứng dụng. Hãy xác nhận cấu hình thu thập dự kiến thông qua [quy trình chấp nhận trực tiếp](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
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

Việc xác minh thành công sẽ chứng minh tính toàn vẹn liên quan đến khóa thu thập đáng tin cậy và ranh giới được duy trì. Nguồn thông tin chính xác, việc gửi tin nhắn Telegram đầy đủ, thời gian đáng tin cậy, và tính hợp lệ về mặt pháp lý đòi hỏi các bằng chứng riêng biệt. Phiên bản này chưa hoàn tất quá trình kiểm định trên Telegram thực tế hoặc đánh giá pháp y/an ninh độc lập.

Một khóa thu thập bị sao chép có thể ký vào một sổ nhật ký thay thế được tạo giả mạo. Việc xác minh so với một điểm kiểm tra hoặc bản ghi chứng thực được lưu giữ độc lập sẽ phát hiện ra tiền tố trước đó đã bị thay đổi; chỉ riêng việc xác minh chữ ký thì không thể làm được điều này. Một nhân chứng sẽ xác nhận lại những gì bộ thu thập đã trình bày, do đó nó không tự mình xác định tính xác thực của các bản ghi bị làm giả trước khi đạt đến điểm kiểm tra bên ngoài đầu tiên. Các báo cáo triển khai trên đám mây kiểm tra cấu hình và các chỉ số do bộ thu thập báo cáo; chúng không chứng minh rằng khóa riêng tư chưa bao giờ bị sao chép trong quá trình khởi tạo.

Các thông báo được gửi qua Apprise bao gồm tên và số lượng không gian làm việc cũng như cuộc trò chuyện; các đoạn trích ngắn của tin nhắn đã bị xóa và chỉnh sửa chỉ được thêm vào khi người vận hành bật tính năng này (mặc định là tắt). Đây là tín hiệu tiện lợi, không phải bằng chứng: việc gửi đến không được đảm bảo, và chỉ có nhật ký cùng các bản xuất có chữ ký mới ghi lại những gì đã được quan sát. Khi có máy chủ trung gian cho không gian làm việc, các thông báo sẽ đi theo cùng một lộ trình; các dịch vụ không thể sử dụng lộ trình này, cũng như các lộ trình MTProxy, sẽ bị từ chối.

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

## Phạm vi bao quát: tính liên tục, các khoảng trống và các ID không được ghi nhận

Mỗi tệp ZIP được ký số đều chứa tệp `coverage.json`; báo cáo HTML mở đầu bằng cùng một bản tóm tắt; và tệp `verify.py` sẽ tính toán lại bản tóm tắt này dựa trên tệp `events.jsonl` thay vì tin tưởng vào nội dung của tệp:

- **Quá trình quan sát diễn ra liên tục từ X đến Y.** Một khoảng thời gian bắt đầu bằng `observation.started` và kết thúc khi có tạm dừng, ngừng hoạt động, mất kết nối Telegram, đăng xuất, quá trình khởi động mà không có bước dừng đúng trình tự, hoặc khi không có bất kỳ bản ghi nào trong hơn ba phút trong quá trình quan sát (các tín hiệu kiểm tra trạng thái được ghi lại mỗi phút, do đó sự im lặng có nghĩa là quá trình đã dừng lại, bị treo hoặc máy tính đã chuyển sang chế độ ngủ). Khi khoảng thời gian giữa các tín hiệu kiểm tra trạng thái được thay đổi trong **phần Cài đặt**, mỗi tín hiệu kiểm tra trạng thái sẽ ghi lại thay đổi này và khoảng thời gian im lặng được phép sẽ là ba khoảng thời gian, không bao giờ ít hơn ba phút.
- **Danh sách các khoảng trống** liệt kê khoảng thời gian giữa các giai đoạn kèm theo lý do. Một khoảng trống vẫn còn tồn tại tại bản ghi cuối cùng sẽ được đánh dấu là `not_resumed_by_last_record`.
- **ID tin nhắn không được ghi nhận.** Đối với các kênh và siêu nhóm, nơi số lượng tin nhắn được tính theo cuộc trò chuyện, các ID bị thiếu giữa các ID đã ghi nhận sẽ được liệt kê dưới dạng khoảng. Chúng được báo cáo là không*được ghi nhận* — do đã bị xóa, chưa bao giờ được gửi đi hoặc nằm ngoài lịch sử đã lưu — chứ không bao giờ được ghi là đã bị xóa. Các cuộc trò chuyện riêng tư và nhóm thông thường sử dụng chung một dãy số ID trên toàn tài khoản, do đó các khoảng trống ở đó không có ý nghĩa gì và không được liệt kê.
- Các thông báo về khoảng trống ở cấp độ cuộc trò chuyện (ví dụ: Telegram yêu cầu khôi phục dữ liệu bị thiếu trong một kênh) được tính là các ghi chú; chúng không làm gián đoạn phạm vi ghi lại toàn bộ.

Phạm vi ghi nhận mô tả những nội dung mà công cụ thu thập này đã ghi lại. Điều này không phải là bằng chứng cho thấy Telegram đã gửi mọi bản cập nhật trong suốt một khoảng thời gian liên tục.

## Người sản xuất

Bản kê khai có chữ ký của các tệp ZIP bằng chứng, bản xuất cuộc trò chuyện, nhật ký chứng cứ và tuyên bố về các tệp hồ sơ cá nhân chứa thông tin `producer` : phần mềm, phiên bản, dự án (PhishDestroy), trang chủ và kho lưu trữ mã nguồn. Báo cáo HTML hiển thị dòng thông tin tương tự, và `verify.py` in thông tin này như một phần của nội dung đã được xác minh. Các tệp lưu trữ được tạo ra trước khi trường này tồn tại sẽ được xác minh như trước đây và được báo cáo là không nêu tên người tạo.

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

Vui lòng lấy mã xác minh từ một bản tải xuống đáng tin cậy hoặc bản sao độc lập đã được kiểm duyệt. Mã xác minh nằm trong một kho lưu trữ không đáng tin cậy là tài liệu có thể thực thi do tác giả của kho lưu trữ đó cung cấp; sự hiện diện của nó chỉ nhằm mục đích thuận tiện cho việc di chuyển, chứ không phải là một điểm neo tin cậy độc lập.

Một điểm kiểm tra sẽ ký vào một tuyên bố chứa khóa công khai, độ dài nhật ký, băm đầu (head hash) và thời gian tạo. Người xác minh có thể kiểm tra xem một bản lưu trữ sau đó có chứa tiền tố tương tự hay không. Hãy lưu giữ một điểm kiểm tra bên ngoài bộ thu thập trước khi xảy ra thay đổi có tranh chấp: một kẻ tấn công kiểm soát cả bản lưu trữ lẫn điểm kiểm tra có thể thay thế cả hai.

Một chữ ký hợp lệ từ khóa chưa được ghim chỉ đảm bảo tính nhất quán nội bộ mà thôi. Ngay cả khóa đã được ghim cũng không thể chứng minh tính xác thực của nội dung nguồn nếu người thu thập hoặc khóa đó đã bị xâm phạm trước khi ghi lại. Việc đóng dấu thời gian bên ngoài và việc thu thập dữ liệu đáng tin cậy là những yêu cầu riêng biệt. TgWitness không cam kết về tính chấp nhận được làm bằng chứng hoặc chứng nhận pháp y.

## Tệp đính kèm

Các tệp được định danh bằng mã băm SHA-256 trong thư mục media/. Một sự kiện media.saved liên kết mã băm và độ dài byte với một sự kiện tin nhắn cụ thể. Tên tệp gốc là siêu dữ liệu, không bao giờ là đường dẫn cục bộ. Các byte phương tiện được tải xuống theo cơ chế không đồng bộ, do đó việc xóa ngay lập tức có thể ngăn cản quá trình ghi lại. Các trường hợp như việc thu thập bị vô hiệu hóa, tệp quá lớn/không xác định kích thước, lỗi tải xuống, và quá trình tải xuống bị gián đoạn đều được hiển thị dưới dạng kết quả. Sự cố sập hệ thống có thể để lại các tệp không hoàn chỉnh không có tham chiếu; những tệp này sẽ không được bao gồm trong các bản xuất.

Trình xuất ZIP sẽ xác minh các tệp phương tiện được lưu trữ dựa trên tên của chúng. Các định dạng xuất JSONL, CSV và HTML sẽ xác minh chữ ký sự kiện nhưng không chứa dữ liệu phương tiện. Các báo cáo phái sinh chỉ mang tính tiện lợi; tệp events.jsonl mới là bản ghi sự kiện chính thức.

## Thu thập và xử lý bằng chứng bền vững (0.2)

Một tác vụ phương tiện và sự kiện tin nhắn tương ứng được ghi lại trong một giao dịch duy nhất. Tác vụ này lưu trữ mô tả tin nhắn TL gốc; quan sát có chữ ký liên kết mã SHA-256, tài khoản và chính sách kích thước của nó. Quá trình khôi phục sẽ xác minh liên kết đó trước khi tải xuống. Hệ thống không bao giờ truy xuất tin nhắn hiện tại mà sẽ âm thầm thay thế bằng tệp đính kèm mới hơn. Các tác vụ bị gián đoạn sẽ được thử lại, trong khi lỗi vĩnh viễn vẫn là một kết quả rõ ràng.

Mỗi không gian làm việc đều có sổ nhật ký và danh tính ký riêng. Sự kiện `process.started` bao gồm ID phiên chạy, thời gian theo đồng hồ cục bộ, phiên bản các thành phần phụ thuộc, băm tệp nguồn, tài khoản/phạm vi ban đầu, và cài đặt ghi lại. Các tín hiệu kiểm tra trạng thái (heartbeats) bao gồm ID phiên chạy, thời gian đơn điệu và trạng thái hàng đợi. Biên nhận quá trình cũng có thể được tải xuống dưới dạng một bản tuyên bố được ký riêng biệt. Các số liệu về tệp là do hệ thống tự báo cáo và không phải là chứng nhận phần cứng đáng tin cậy.

Các điểm kiểm tra tự động được lưu giữ cục bộ khi khởi động, cứ sau năm phút trong quá trình theo dõi (**Tham số → Điểm kiểm tra có chữ ký mỗi**) và khi dừng hoạt động theo trình tự. Quá trình xác minh khi khởi động và xuất dữ liệu sẽ so sánh nhật ký với điểm kiểm tra cục bộ mới nhất được lưu giữ. Điều này có thể phát hiện tình trạng khôi phục cơ sở dữ liệu khi điểm kiểm tra vẫn còn tồn tại; tuy nhiên, người vận hành kiểm soát cả hai vẫn có thể thay thế cả hai. Việc lưu trữ độc lập và các dấu thời gian đáng tin cậy từ bên ngoài vẫn là các yêu cầu riêng biệt.

Sau khi khởi động lại, vị trí cập nhật Telegram đã lưu sẽ được khôi phục (`catch_up_from` trong `observation.started`) và hệ thống sẽ yêu cầu các bản cập nhật bị bỏ lỡ. Quá trình kiểm tra lại định kỳ sẽ ghi lại `message.recovered` đối với các tin nhắn bị bỏ lỡ và `message.missing_on_recheck` khi Telegram không còn trả về tin nhắn đã lưu; trường hợp sau không phải là thông báo xóa và không nêu tên người xóa cũng như thời gian.

### Sao lưu và khôi phục ngoài trang web (S3)

Bản sao ngoài trang web (Tính năng Xuất dữ liệu, mặc định là tắt) sẽ tải lên các phân đoạn nhật ký, tệp tin được lưu giữ, các điểm kiểm tra cùng với dấu thời gian của chúng và các bản xuất cuộc trò chuyện đã hoàn tất lên bộ lưu trữ tương thích với S3, được mã hóa bằng AES-256-GCM trước khi tải lên bằng khóa được lưu trữ trong kho lưu trữ của không gian làm việc; tính năng lưu giữ Object Lock sẽ được áp dụng khi bucket hỗ trợ tính năng này. Nếu không có khóa đã tải xuống, bản sao này sẽ không thể được đọc. Khôi phục và xác minh bằng `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Quá trình khôi phục yêu cầu một thư mục thông thường trống. Các tệp tải xuống và các đối tượng đã được giải mã sẽ được lưu giữ trong bộ nhớ tạm thời riêng tư cho đến khi toàn bộ nhật ký và mọi điểm kiểm tra được lưu giữ đều được xác minh. Các đường dẫn đối tượng không an toàn, phạm vi phân đoạn không nhất quán và các nhật ký ngắn hơn một điểm kiểm tra sẽ bị từ chối; nếu xác minh thất bại, hệ thống sẽ không công bố bất kỳ tệp nào đã được khôi phục. Các kiểm tra thời hạn lưu giữ sẽ so sánh chế độ Object Lock và ngày tháng được trả về với thời hạn được gửi khi tải lên (dung sai làm tròn là một giây). Thời hạn đã hết hạn, không hợp lệ hoặc bị rút ngắn sẽ không được coi là đã được xác minh. Trạng thái báo cáo đối tượng được lấy mẫu mà thời hạn lưu giữ của nó đã được đọc lại cho lần tải lên đó.

Tiến trình sao chép được giới hạn trong phạm vi đích và khóa mã hóa. Việc thay đổi điểm cuối, thùng lưu trữ hoặc tiền tố sẽ khởi động quá trình sao chép hoàn toàn nhật ký, tệp phương tiện và các điểm kiểm tra được lưu giữ cục bộ sang đích đó. Tiến trình cũ chưa được giới hạn phạm vi sẽ được bảo toàn nhưng chỉ được tái thực thi một lần sau khi nâng cấp. Các bản xuất lịch sử trò chuyện đã bị xóa khỏi hộp thư đi cục bộ vẫn được giữ nguyên tại đích ban đầu của chúng.

Các tệp phương tiện cục bộ bị thiếu hoặc bị hỏng sẽ được báo cáo là lỗi của lần xử lý và con trỏ phương tiện sẽ được giữ lại trước vị trí đó, để tệp này được thử lại trong lần xử lý tiếp theo; các tệp, điểm kiểm tra và tệp xuất sau đó vẫn được sao chép. Quá trình khôi phục sẽ kiểm tra tất cả các tham chiếu đến phương tiện được lưu giữ so với các hàm băm đã được giải mã và kích thước đã ghi lại. Các phân đoạn nhật ký trùng lặp giống hệt nhau từ các lần tải lên bị gián đoạn sẽ được loại bỏ trùng lặp; các phần trùng lặp mâu thuẫn sẽ bị từ chối. Các điểm kiểm tra được tạo ra trong quá trình tải lên sẽ được hoãn lại cho đến khi các bản ghi nhật ký liên quan đã được sao chép, do đó một lần quét hoàn tất sẽ không công bố điểm kiểm tra trước khi nhật ký tương ứng được hoàn tất.

### Xuất các bản chụp nhanh theo thời gian thực

Việc xuất dữ liệu theo thời gian thực sử dụng một bản chụp nhanh đọc ổn định từ cơ sở dữ liệu SQLite. Phần đầu của bản chụp nhanh này có thể cũ hơn so với sổ nhật ký trực tiếp hiện tại khi quá trình tải xuống hoàn tất. Một điểm kiểm tra được tạo ra sau bản chụp nhanh đó có thể báo cáo chính xác rằng kho lưu trữ ngắn hơn; hãy so sánh với một điểm kiểm tra tại hoặc trước tiền tố đã xuất, chứ không phải một điểm kiểm tra ngẫu nhiên nào đó sau đó.

## Chuẩn bị theo RFC 3161 và xác minh phản hồi (0.2)

Chế độ bằng chứng (tắt theo mặc định) chỉ gửi mã SHA-256 của từng điểm kiểm tra đã được ký đến các cơ quan có thẩm quyền theo tiêu chuẩn RFC 3161 và các lịch OpenTimestamps đã liệt kê, thông qua tuyến đường không gian làm việc và tuyệt đối không qua MTProxy. Các kết quả được lưu trữ trong `checkpoints/anchors/`, xuất ra và kiểm tra bằng `verify.py` (`--tsa-ca` kiểm tra chữ ký TSA; xác nhận các bằng chứng OpenTimestamps bằng `ots upgrade` và `ots verify`).

Bảng điều khiển sẽ chuẩn bị một kho lưu trữ yêu cầu chứa các byte chuẩn của tệp checkpoint.json, dấu vân tay tin nhắn SHA-256 và giá trị ngẫu nhiên (nonce) trong tệp timestamp.tsq, các tổng kiểm tra (checksums) cùng hướng dẫn. Không có yêu cầu mạng nào được thực hiện. Quá trình chuẩn bị này không phải là dấu thời gian đáng tin cậy.

`python -m tgwitness.anchor verify` gọi hàm OpenSSL ts hai lần: một lần đối với các byte điểm kiểm tra và một lần đối với yêu cầu ban đầu. Tệp CA đáng tin cậy phải được chỉ định rõ ràng; các chứng chỉ đi kèm sẽ không tự động được coi là đáng tin cậy. Việc kiểm tra yêu cầu là tùy chọn tại giao diện dòng lệnh (CLI), do đó quý vị cần giữ lại và cung cấp tham số --request để kiểm tra mã ngẫu nhiên (nonce). Kết quả sẽ cho biết liệu việc kiểm tra đã được thực hiện hay chưa. Chữ ký điểm kiểm tra của bộ thu thập và nhật ký vẫn phải được xác minh riêng biệt bằng dấu vân tay đáng tin cậy của bộ thu thập.

Công cụ xác minh hiện tại không thu thập thông tin thu hồi cũng như không thực hiện việc xác thực lưu trữ dài hạn sau khi chứng chỉ hết hạn. Xin đừng nhầm lẫn việc xác minh chữ ký thành công với dấu thời gian đủ điều kiện hoặc tính hợp lệ về mặt pháp lý. Một tổ chức TSA độc lập thực sự chưa được liên hệ trong quá trình phát triển. Vui lòng tham khảo [quy trình](https://phishdestroy.github.io/TgWitness/vi/docs/reference/timestamp/).
