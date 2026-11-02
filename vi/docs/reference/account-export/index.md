# Xuất tài khoản

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/account-export/

Xuất những nội dung mà tài khoản có thể truy cập hiện tại: phạm vi, các tác vụ có thể tiếp tục, tệp lưu trữ đã được ký và các bản sao chia sẻ đã được thu gọn.

Với tư cách là quản trị viên cài đặt, hãy chọn **Bắt đầu tại đây → Xuất tài khoản của tôi**, hoặc **Xuất → Tài khoản Telegram → Cấu hình xuất tài khoản**. Đăng nhập nếu cần, xem lại phạm vi và bắt đầu xuất một cách rõ ràng. Không cần quan sát liên tục. **"Lưu quan sát**" là một bản xuất riêng biệt của nhật ký hiện có; ZIP của nó bao gồm tất cả các nguồn bất kể bộ lọc nhật ký. Mỗi không gian làm việc có các tác vụ, danh tính ký và bộ nhớ riêng. Quyền truy cập bảng điều khiển đã cấp, bao gồm quyền xuất thông thường không hạn chế, không thể mở các đường dẫn trên toàn tài khoản này.

Các bộ lọc người gửi và nội dung tin nhắn sẽ mở rộng khi chọn **“Lọc theo người gửi” hoặc “Lọc theo nội dung tin nhắn**”. **Phần “Dữ liệu tài khoản & phương thức kết nối**” chứa các danh mục tài khoản tùy chọn và tùy chọn “Takeout” hoặc “phiên làm việc thông thường”; phần tóm tắt của nó hiển thị các tùy chọn đang hoạt động ngay cả khi đã đóng. Việc đóng các phần này sẽ giữ nguyên cài đặt của chúng. Các bản nháp xuất và báo cáo vẫn tồn tại trong phiên làm việc hiện tại của bảng điều khiển khi chuyển đổi chế độ xem; chúng không được lưu khi tải lại trình duyệt. Các tác vụ hiện có vẫn có thể truy cập được từ cả hai tùy chọn xuất.

Quy trình làm việc này xuất dữ liệu hiện có thể truy cập được từ tài khoản đã kết nối. Mặc định sử dụng [Telegram Takeout](https://core.telegram.org/api/takeout); đây không phải là bản sao lưu dữ liệu Telegram không khả dụng hoặc đã bị xóa. Các cuộc trò chuyện bí mật, lịch sử không thể truy cập và các bản chỉnh sửa trước đó sẽ không được khôi phục. Telegram có thể áp đặt thời gian chờ trước khi Takeout bắt đầu. Bảng điều khiển sẽ hiển thị thời gian chờ đó; nó sẽ không tự động chuyển đổi phương thức truyền tải. Tùy chọn API thông thường rõ ràng có phạm vi bao phủ khác và ghi lại các danh mục không được hỗ trợ.

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

Định dạng tối giản loại bỏ các hồ sơ tài khoản có cấu trúc, danh bạ, ảnh đại diện, phiên làm việc, câu chuyện, đối tượng Telegram thô, tiêu đề chuyển tiếp, trích dẫn trả lời, thẻ liên hệ và siêu dữ liệu vị trí. Nó loại trừ các tệp JSONL gốc, cài đặt bộ lọc riêng tư, khóa bí danh và bản đồ danh tính. Văn bản được chọn, danh tính được giữ lại rõ ràng và các tệp được bao gồm vẫn có thể chứa cùng tên, ID hoặc cụm từ được sử dụng trong các bộ lọc đó; chúng cần được xem xét riêng. Chính sách riêng tư và khóa bí danh được lưu giữ dưới dạng mã hóa trong kho lưu trữ cục bộ của tác vụ; việc xóa tác vụ sẽ xóa các bản ghi tiết lộ riêng tư liên quan. Các bản ghi chính sách công khai ghi lại số lượng bộ lọc thay vì giá trị bộ lọc. Mục đích được nêu rõ là công khai trong tệp manifest và HTML: các tiêu chí riêng tư rõ ràng và, trong các chế độ ẩn danh, các danh tính ẩn đã biết cũng được che giấu tại đó, kể cả khi nội dung tin nhắn bị bỏ qua. Hãy giữ cho mục đích không chứa các chi tiết cá nhân không cần thiết; bối cảnh nhận dạng chưa xác định có thể được giữ lại.

Tệp manifest của nó liên kết các tệp phái sinh, chính sách công khai và băm của tệp ZIP gốc. Quá trình xác minh có thể xác định tính toàn vẹn và, nếu nguồn được cung cấp tại địa phương, xác định sự khớp nối nguồn:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Liên kết nguồn không tự nó chứng minh rằng quá trình chuyển đổi đã chọn tất cả các mục cần thiết hoặc loại bỏ tất cả các chi tiết nhận dạng. Văn bản gốc không được nhúng làm bằng chứng. Cần có một cuộc đánh giá mới để đưa ra phán đoán đó.

## Bảo vệ dữ liệu và bản xem trước Capture được lưu trữ

Các cơ chế kiểm soát này hỗ trợ nguyên tắc giới hạn mục đích và tối thiểu hóa dữ liệu; chúng không phải là công cụ kiểm tra tuân thủ pháp luật tự động. [Các Điều 5 và 25 của GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) đề cập đến các nguyên tắc này cùng với việc bảo vệ theo thiết kế/mặc định. Cơ sở pháp lý, tính cần thiết, các điều kiện liên quan đến danh mục dữ liệu đặc biệt (nếu có), thời hạn lưu trữ, an ninh và quyền truy cập của bên nhận vẫn cần có quyết định phù hợp với từng trường hợp cụ thể. Mục đích liên quan đến tranh tụng thôi chưa đủ để làm cho mọi việc tiết lộ dữ liệu trở nên hợp pháp. Dữ liệu được ẩn danh hóa nói chung vẫn được coi là dữ liệu cá nhân; xem [giải thích của EDPB](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisation-pseudonymisation_en).

Văn bản tự do, ngày tháng, các sự kiện hiếm gặp và sự kết hợp của các sự kiện có thể giúp xác định danh tính của người dùng ngay cả khi tên đã bị xóa. Nên bỏ qua văn bản khi nội dung tin nhắn không cần thiết; kiểm tra bản sao đầy đủ khi cần thiết. Bảo vệ nguồn và kho lưu trữ, thỏa thuận về thời gian lưu giữ và chia sẻ với người chịu trách nhiệm, đồng thời ghi lại chính xác hình ảnh nào ZIP đã được chuyển giao.

Tính năng này chạy trong bảng điều khiển cục bộ. Hình ảnh được xuất bản riêng biệt [Xem trước bản ghi được lưu trữ](https://phishdestroy.github.io/TgWitness/docs/capture/) sử dụng một trình chạy dùng một lần được ghim và chính sách xác thực riêng của nó. Chữ ký của trình thu thập cục bộ không kế thừa nguồn gốc của trình chạy đó. Một thay đổi tại đây sẽ không cập nhật quy trình làm việc từ xa đã được phê duyệt hoặc các ghim tin cậy của nó; việc thu thập toàn bộ tài khoản được lưu trữ cần một cặp trình thu thập/quy trình làm việc được xem xét và xuất bản riêng biệt cùng với sự chấp nhận của trình chạy đang hoạt động. Các bài kiểm tra tổng hợp cục bộ không tuyên bố bất kỳ triển khai được lưu trữ nào hoặc việc thu thập tài khoản Telegram thực tế.

[Định dạng bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/) · [Báo cáo trường hợp](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-reports/)
