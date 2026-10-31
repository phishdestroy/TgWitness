# Điều tra trên tất cả các cuộc trò chuyện

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/cases/

Xử lý toàn bộ vụ việc trên các kênh, nhóm, cuộc trò chuyện riêng tư và bot: thu thập, kết nối, tái tạo và bàn giao bằng chứng.

Hướng dẫn này sẽ theo dõi một vụ việc giả định từ đầu đến cuối. Hướng dẫn sử dụng các tính năng thu thập, tìm kiếm, lập hồ sơ cá nhân và xuất dữ liệu thực tế. Bản đồ vụ việc chỉ là một ví dụ minh họa trong tài liệu; các kết luận và sổ đăng ký vụ việc của quý vị sẽ được lưu trữ bên ngoài ứng dụng.

TRƯỜNG HỢP ĐÃ XỬ LÝ / ĐỊA CHỈ NHẬN THANH TOÁN ĐÃ ĐƯỢC THAY ĐỔI

### Một sự cố. Bốn cuộc trò chuyện. Một dấu vết cần được tái hiện.

Một thông báo trên kênh đề cập đến một bot. Một nhóm vận hành thảo luận về một liên kết thanh toán mới. Một tin nhắn riêng tư tiếp theo nhắc lại nội dung đó. Sau đó, thông báo này bị chỉnh sửa và một tin nhắn trong nhóm biến mất.

Ai là người đã đăng tải từng phiên bản?Liên kết này xuất hiện ở đâu?Tệp nào đã được lưu giữ?Điều gì đã thay đổi và vào thời điểm nào?

Để tải lịch sử, xem xét nguồn bằng AI (tùy chọn), MCP, OCR và webhook gửi đi, hãy xem [phần "Quản lý kho lưu trữ"](https://phishdestroy.github.io/TgWitness/vi/docs/archive/).

## 1. Đảm bảo phạm vi bao quát toàn bộ tài khoản

1. [Vui lòng kết nối tài khoản thu thập dữ liệu](https://phishdestroy.github.io/TgWitness/vi/docs/accounts/) trong không gian làm việc riêng của nó. Ghi lại mã tham chiếu vụ việc, ID tài khoản, tên không gian làm việc và dấu vân tay khóa ký vào ghi chú vụ việc của quý vị.
2. **Nguồn** mở **→ Phạm vi quan sát → Chế độ điều tra**. Xem xét **toàn bộ tài khoản**, cả bốn loại nguồn và **các hành động của chính người dùng**. Cài đặt sẵn này cho phép lưu hồ sơ của một nguồn mới cùng **200 tin nhắn hiển thị** gần nhất của nguồn đó. Nhấn **Lưu phạm vi** và hoàn tất việc xác nhận phạm vi.
3. Nhấn vào **“Tải các cuộc trò chuyện**”. So sánh các nguồn với danh sách cuộc trò chuyện của tài khoản và xem xét các trường hợp loại trừ. Trong **phần “Tham số” → “Các cuộc trò chuyện được đọc từ danh sách tài khoản**”, hãy điều chỉnh giới hạn danh sách ban đầu nếu cần: giá trị mặc định là 1.000 cuộc trò chuyện, có thể cấu hình lên đến 20.000. Các cuộc trò chuyện vượt quá giới hạn sẽ được phát hiện khi chúng trở nên hoạt động.
4. Trong **phần Cài đặt ghi lại**, hãy chọn và lưu tùy chọn **“Tất cả hoạt động hiển thị**”. Kiểm tra các loại tệp đính kèm, giới hạn dung lượng và dung lượng đĩa trống. Bắt đầu quá trình giám sát và xác thực một tin nhắn, thao tác chỉnh sửa và xóa được kiểm soát trước khi tin tưởng vào cấu hình đã thiết lập.

Các kênhCác nhómCác cuộc trò chuyện riêng tưCác bot

MỘT TÀI KHOẢN / MỘT KHÓA KÝ**Tất cả các hoạt động có thể nhìn thấy trên tài khoản đã được chọn → một sổ ghi chép duy nhất**

Tin nhắn · các thao tác chỉnh sửa · thông báo xóa · phản ứng hiển thị · các sự kiện liên quan đến tư cách thành viên · các hành động của chính người dùng

“Toàn bộ tài khoản” bao gồm các cuộc trò chuyện mà tài khoản này có thể truy cập, cùng với các loại nguồn và các trường hợp loại trừ đã được cấu hình. Các cuộc trò chuyện bí mật không khả dụng. Các cuộc trò chuyện mới sẽ được thêm vào khi có bản cập nhật; việc kích hoạt chế độ này sẽ không tự động tải xuống toàn bộ lịch sử cũ của mọi cuộc trò chuyện hiện có.

## 2. Thu thập lịch sử và bảo quản các tệp tin

Xây dựng sổ đăng ký nguồn cho toàn bộ cuộc điều tra. Gán cho mỗi cuộc trò chuyện một hàng với ID số, tiêu đề, tài khoản, quyền truy cập/vai trò, thời điểm bắt đầu theo dõi trực tiếp, quá trình thu thập lịch sử, kết quả phương tiện truyền thông và các khoảng trống đã biết. Chỉ đánh dấu nguồn là đã thu thập sau khi kiểm tra kết quả liên quan.

| Yêu cầu | Thao tác trên bảng điều khiển | Các tính năng mà công cụ này cung cấp |
| --- | --- | --- |
| Lịch sử trong các cuộc trò chuyện đã kích hoạt | Nguồn → Tải lịch sử đầy đủ | Tính năng chính hiện tại: các tin nhắn trong quá khứ có sẵn sẽ được đưa vào nhật ký không gian làm việc, kèm theo tính năng tạm dừng/tiếp tục và báo cáo tiến độ có chữ ký. [Hướng dẫn sử dụng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/history/). |
| Bối cảnh cuộc trò chuyện hiện có trong sổ ghi chép | Nguồn → Cài đặt ghi lại → Bản chụp lịch sử | Các tin nhắn hiển thị gần đây dưới dạng các quan sát đã được ký xác thực. Giá trị mặc định tối đa là 500; tại mục **Thông số → Bản chụp lịch sử lớn nhất**, quý vị có thể tăng con số này lên đến 10.000. |
| Lịch sử đầy đủ hiện có của một cuộc trò chuyện | Xuất toàn bộ cuộc trò chuyện → Xuất toàn bộ cuộc trò chuyện, hoặc Cuộc trò chuyện → Xuất cuộc trò chuyện | Một gói dữ liệu được ký riêng biệt với các thuật toán `chat.json` và `chat.html`. Thực hiện lặp lại cho từng nguồn; lưu giữ kết quả thành công hoặc thất bại. |
| Bối cảnh khi một cuộc trò chuyện mới xuất hiện | Phạm vi quan sát → Khi một cuộc trò chuyện hoặc bot mới xuất hiện | Hồ sơ nguồn và tối đa 1.000 tin nhắn gần đây có thể hiển thị; Chế độ điều tra sẽ chọn 200 tin nhắn. Các cuộc trò chuyện hiện có sẽ không được ghi lại các tin nhắn này theo hình thức hồi tố. |
| Dung lượng tệp đính kèm | Tải xuống các tệp đính kèm có thể xem được + giới hạn theo từng loại | Vui lòng kiểm tra mã `media.saved`, giá trị SHA-256 và số byte tương ứng. Các tệp đang chờ xử lý, bị bỏ qua hoặc tải xuống không thành công sẽ không được lưu giữ. |

Việc xuất toàn bộ cuộc trò chuyện là một bản chụp riêng biệt; nó không nhập toàn bộ lịch sử vào sổ ghi chép hoặc hồ sơ cá nhân. Sử dụng **tính năng “Tải toàn bộ lịch sử** từ các nguồn đã bật” hoặc các bản chụp sổ ghi chép có giới hạn để tìm kiếm tài liệu lịch sử mà bạn cần trong TgWitness. Kiểm tra danh sách nguồn trước khi bắt đầu quá trình chạy.

Trong trường hợp cụ thể, hãy thu thập kênh thông báo, nhóm hoạt động, cuộc trò chuyện với bot và các cuộc trao đổi riêng tư tiếp theo. Lưu giữ các byte và mã băm của tệp đính kèm hóa đơn. Lịch sử hiện có không thể tái tạo lại một tin nhắn đã bị xóa trước khi ghi lại hoặc một lần chỉnh sửa trung gian mà Telegram không còn cung cấp nữa.

## 3. Theo dõi diễn biến cuộc trò chuyện và các hành động của chính quý vị

Hãy duy trì quá trình theo dõi khi vụ việc tiếp tục diễn biến. Đánh dấu các cuộc trò chuyện liên quan đến vụ việc đang diễn ra làm nguồn ưu tiên; cấu hình mức độ ưu tiên và việc kiểm tra lại các nguồn khác trong **phần Cài đặt ghi lại → Kiểm tra lại**. Kiểm tra lại các mục `recheck.completed`, cập nhật tiếp theo, FloodWait và kết quả liên quan đến phương tiện truyền thông khi công việc tiến triển.

Vui lòng sử dụng **Chats → Profile → Save profile now** để lưu giữ các mô tả nguồn hiện tại, lệnh bot và các siêu dữ liệu khác mà Telegram trả về. Hồ sơ nguồn này độc lập với các hồ sơ cá nhân được xây dựng từ các tin nhắn trong nhật ký.

**Theo dõi một bot hoặc lời mời trong khuôn khổ vụ việc**

1. Trong **mục Trò chuyện → Mở liên kết Telegram**, quý vị hãy lưu bản xem trước trước tiên. Liên kết gốc và bản xem trước được trả về sẽ trở thành các bản ghi có chữ ký.
2. Nếu cuộc điều tra yêu cầu, lệnh **Join / open sẽ theo dõi** các thao tác tham gia hoặc mở nguồn và khởi chạy một bot với tham số khởi động được cung cấp. Yêu cầu tham gia đang chờ xử lý sẽ vẫn được ghi nhận trong hồ sơ.
3. Đối với một hành động mà quý vị cần ghi lại, vui lòng sử dụng tính năng trả lời bằng văn bản trên bảng điều khiển hoặc **nút “Press”** được hỗ trợ. Nhật ký sẽ lưu giữ các giá trị `interaction.requested` và `interaction.result`, bao gồm cả văn bản hoặc URL được trả về từ hàm callback.

Các chức năng điều khiển này thực hiện các thao tác thực tế trên Telegram. Việc nhấn nút gọi lại trong một ứng dụng Telegram khác sẽ không được bộ thu thập ghi nhận; tuy nhiên, tin nhắn hoặc thao tác chỉnh sửa tiếp theo của bot có thể được ghi lại. Các ứng dụng web, giao dịch thanh toán và yêu cầu về số điện thoại/vị trí nằm ngoài phạm vi của ứng dụng khách thu nhỏ.

## 4. Theo dõi các cá nhân, liên kết và tệp tin trong các cuộc trò chuyện

1. Mở **Sổ nhật ký**, để bộ lọc nguồn ở chế độ **“Tất cả nguồn”** và tìm kiếm một cụm từ đặc trưng, tên miền, tên người dùng hoặc mã định danh đã lưu. Mở từng bản ghi phù hợp và ghi lại nội dung trò chuyện, ID tin nhắn cùng số thứ tự trong sổ nhật ký của bản ghi đó.
2. Để xem một cuộc trò chuyện cụ thể, hãy mở **Chats → People → Bật hồ sơ**, sau đó chọn một người. Xem lại lịch sử tên/tên người dùng, mối quan hệ trả lời, hoạt động, **cũng như các mục “Cũng trong…”** bao gồm các cuộc trò chuyện khác được theo dõi và các liên kết, ví tiền điện tử hoặc số điện thoại đã trích xuất. Mở các bản ghi nhật ký được trích dẫn.
3. Hãy theo dõi cùng một ID người dùng Telegram (dạng số) trong các cuộc trò chuyện khác thuộc không gian làm việc này. Hãy coi tên trùng khớp, việc đề cập đến ví tiền điện tử hoặc hình đại diện tương tự như một manh mối cần kiểm tra. Việc đề cập đến một địa chỉ không chứng minh quyền sở hữu; hình đại diện tương tự cũng không chứng minh đó là cùng một người.
4. So sánh các giá trị SHA-256 của tệp đính kèm được lưu giữ giữa các bản ghi. Các giá trị băm trùng khớp đảm bảo tính nhất quán về byte của các tệp đã lưu. Kiểm tra các bản ghi tin nhắn và người gửi liên quan trước khi đưa ra kết luận về người đã chia sẻ chúng.

BẢN ĐỒ VỤ VIỆC / THEO DÕI CÁC THAM CHIẾUTrường hợp giả định · không phải biểu đồ thực tế

KÊNH / THÔNG BÁO**Bản gốc → bản đích đã chỉnh sửa**

Bản ghi số 101, số 188 – Tin nhắn số 84 · không xác định người gửi

NHÓM / HOẠT ĐỘNG**Người dùng 71001 đã đăng liên kết mới**

Bản ghi số 146 · tin nhắn số 309 · Biên nhận tệp đã lưu số 151

BOT / CUỘC TRÒ CHUYỆN ĐẶT HÀNG**Một nút bấm dẫn đến trang đích đó**

Bản ghi số 173 · tin nhắn số 12: Dữ liệu meta của nút “Quay lại”

RIÊNG TƯ / THEO DÕI**Người dùng 71001 lặp lại địa chỉ đích**

Bản ghi số 205 · tin nhắn số 922 · Biên nhận tệp đã lưu số 209

Bốn cuộc trò chuyện cung cấp các quan sát khác nhau. Vui lòng theo dõi các bản ghi nguồn cho từng kết nối; không gán bài đăng trên kênh cho người dùng 71001 nếu không có thông tin người gửi được xác định rõ.

Các mã số nhận dạng và tham chiếu bản ghi được đặt ra riêng cho hướng dẫn này. Sơ đồ này giải thích quy trình làm việc của nhà phân tích thông qua việc sử dụng tính năng tìm kiếm, hồ sơ người dùng và kiểm tra bản ghi; ứng dụng này không tạo ra sơ đồ điều tra tổng thể.

| Kết nối | Quan sát bổ sung | Kết luận cần giữ lại |
| --- | --- | --- |
| Cùng một tài khoản Telegram | ID người dùng 71001 trong nhóm #146 và cuộc trò chuyện riêng tư #205 | ID người gửi được cung cấp giống hệt nhau trong cả hai cuộc trò chuyện. Danh tính thực tế vẫn là một vấn đề riêng biệt. |
| Địa chỉ đích lặp lại | `pay.example.invalid/new` tại #146, siêu dữ liệu nút #173, bài đăng đã chỉnh sửa #188 và #205 | Cùng một địa chỉ đích xuất hiện trong bốn bối cảnh được quan sát. Chỉ riêng điều này chưa đủ để xác định ai là người kiểm soát địa chỉ đó. |
| Cùng số byte tệp | Các giá trị SHA-256 hoàn toàn trùng khớp trong các biên nhận phương tiện đã hoàn tất số #151 và #209 | Hai tệp đính kèm được lưu giữ này có nội dung byte hoàn toàn giống hệt nhau. Chỉ dựa vào tên tệp hoặc hình thu nhỏ thì không thể xác định được điều này. |

Các hồ sơ cá nhân bao gồm thông tin về những người dùng có tin nhắn được lưu trữ trong cuộc trò chuyện đó và liên kết họ với các cuộc trò chuyện khác trong *cùng* một *nhật ký không gian làm việc*. Đây không phải là danh bạ thành viên đầy đủ. Các giá trị băm (hash) của ảnh đại diện được lấy từ bộ nhớ đệm cục bộ riêng biệt; số lượng trích dẫn trong hồ sơ có giới hạn có thể cấu hình tại **mục Cài đặt → Số bản ghi được trích dẫn cho mỗi sự kiện**.

## 5. Phục dựng trình tự và đánh dấu các khoảng trống

Trong **phần “Chats”**, quý vị có thể kiểm tra các phiên bản đã lưu cùng các liên kết **“Journal record #…”** tương ứng. Trong **phần “Journal”**, quý vị có thể sử dụng **các mục “All sources”** cùng với **“Edits”**, **“Deletions”** và **“Coverage**”. Xây dựng dòng thời gian vụ việc dựa trên cả ngày tháng từ Telegram được cung cấp và thời gian quan sát của người thu thập dữ liệu.

1. 09:00 · #101**Bài đăng trên kênh đã được ghi lại**

   Địa chỉ đích ban đầu được giữ nguyên.
2. 09:12 · #146 / #151**Nhóm giới thiệu một liên kết khác**

   Người dùng 71001 đã đăng tải nội dung này; quá trình tải xuống tệp đính kèm đã hoàn tất.
3. 09:16 · #173**Bot hiển thị cùng một đích đến**

   Dữ liệu siêu liên kết được lưu trữ trong thông tin siêu dữ liệu bàn phím.
4. 09:20 · #188**Các thay đổi trong thông báo trên kênh**

   Cả các quan sát ban đầu lẫn các quan sát đã được chỉnh sửa đều được giữ nguyên.
5. 09:24 · #205 / #209**Phần tiếp theo dành cho đối tượng riêng tư cũng lặp lại nội dung này**

   Tệp đính kèm đã lưu có mã SHA-256 đầy đủ trùng khớp với #151.
6. 09:28 · #231**Thông báo về việc xóa nhóm đã được gửi đến**

   Quan sát trước đó vẫn còn nguyên giá trị; thông tin về người xóa cũng như thời điểm xóa chính xác đều không được cung cấp.

Các mốc thời gian quan sát và tham chiếu mang tính minh họa. Các bản ghi nhật ký khác xuất hiện giữa các mục này.

Thứ tự trong nhật ký dựa trên thời điểm nhận được, không nhất thiết phải theo thứ tự các hành động ban đầu trên Telegram. Một bản chụp lịch sử cũ hơn có thể xuất hiện sau một tin nhắn trực tiếp mới hơn. Hãy phân biệt rõ ràng giữa các quan sát trực tiếp, bản chụp, tin nhắn đã khôi phục, thông báo xóa và các trường hợp “không tìm thấy khi kiểm tra lại”. Hãy thêm một khoảng thời gian “không xác định” rõ ràng vào bất kỳ vị trí nào mà phạm vi ghi nhận cho thấy có khoảng trống; một bản chụp sau đó sẽ không xóa bỏ khoảng trống đó.

## 6. Mở rộng phạm vi áp dụng sang các tài khoản thu thập khác

Thêm một không gian làm việc cho từng tài khoản riêng biệt và lặp lại quy trình xác định phạm vi cũng như lập danh mục lịch sử. Ghi lại thông tin về tư cách thành viên/vai trò và dấu vân tay khóa ký cho từng tài khoản. Đảm bảo các định danh được xác định rõ theo không gian làm việc và cuộc trò chuyện: cùng một số tin nhắn không phải là định danh chung áp dụng cho tất cả các tài khoản.

Quý vị có thể so sánh các quan sát có liên quan trong ghi chú vụ việc hoặc các công cụ phân tích của mình, đồng thời lưu giữ thông tin tài khoản và tham chiếu nhật ký cho từng hàng. Hiện tại, TgWitness chưa cung cấp tính năng tìm kiếm toàn cục, dòng thời gian hợp nhất, sơ đồ mối quan hệ giữa các cá nhân hoặc kho lưu trữ vụ việc trên các không gian làm việc. Tính năng xuất toàn bộ dữ liệu từ nhiều tài khoản của một kênh hoặc siêu nhóm là một tính năng riêng biệt; đây không phải là sự hợp nhất của tất cả các nhật ký tài khoản.

Trong quá trình làm việc kéo dài, hãy bổ sung một [nhân chứng độc lập](https://phishdestroy.github.io/TgWitness/vi/docs/witness/) để duy trì các ranh giới đã thiết lập từ trước. Sử dụng chương trình thí điểm phân phối có kiểm soát để xác định các lộ trình thu thập và phạm vi hiển thị của các tài khoản.

## 7. Cung cấp một bộ hồ sơ vụ việc đầy đủ và có thể kiểm chứng

Xuất tệp ZIP chứa nhật ký đã được ký điện tử từ từng không gian làm việc. Tệp này chứa toàn bộ nhật ký đã ghi lại, bất kể các bộ lọc tìm kiếm trên bảng điều khiển. Xuất riêng các hồ sơ cá nhân có liên quan, lưu giữ từng gói lịch sử trò chuyện đầy đủ và bảo toàn các bằng chứng đính kèm đã hoàn chỉnh.

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

Lưu giữ các dấu vân tay đáng tin cậy thông qua một kênh riêng biệt. Từ một hệ thống cài đặt đáng tin cậy, hãy xác minh từng bằng chứng dựa trên danh tính không gian làm việc riêng của nó:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Vui lòng kiểm tra kết quả xác minh thực tế, lưu giữ các bản gốc, đồng thời lưu lại báo cáo phạm vi, các trường hợp thu thập thất bại và bản ghi chuyển giao cùng với các phát hiện của quý vị. Thư mục cấp cao nhất của vụ việc và kết luận của nhà phân tích được tổng hợp bên ngoài; các bằng chứng riêng lẻ của TgWitness đều có chữ ký riêng.

## Áp dụng phương pháp tương tự cho các cuộc điều tra khác

**Tranh chấp về đơn hàng hoặc thanh toán do bot gây ra**

**Câu hỏi:** Bot đã hứa hẹn điều gì, nút bấm đó dẫn đến đâu, và sau đó đã có những thay đổi gì?

**Quá trình theo dõi:** bài đăng khi tham gia kênh → bản xem trước liên kết bot đã lưu → tham số khởi động bot → các tin nhắn và phiên bản nhập liệu từ bàn phím → bất kỳ biên nhận phản hồi nào do bảng điều khiển phát hành → các hoạt động tiếp theo trong nhóm/riêng tư. Phối hợp từng mục đích với bản ghi nguồn tương ứng; lưu giữ các mô tả hồ sơ và phương tiện truyền thông đã hoàn tất.

**Nội dung cung cấp:** dòng thời gian ghi lại các đề nghị và phản hồi được quan sát, các nguồn tham chiếu và các tệp xuất đã được xác minh. Việc hiển thị một liên kết thanh toán không phải là bằng chứng cho thấy giao dịch thanh toán đã diễn ra.

**Các tin nhắn bị xóa sau một sự cố liên quan đến nhiều cuộc trò chuyện**

**Câu hỏi:** Những điều gì đã được quan sát thấy trước khi các tin nhắn liên quan biến mất?

**Theo dõi:** tất cả các cuộc trò chuyện bị ảnh hưởng → tin nhắn gốc → các nội dung đã chỉnh sửa được gửi đi → thông báo xóa hoặc kết quả không tìm thấy khi kiểm tra lại sau đó → các tệp đính kèm được lưu giữ → phạm vi bao quát xung quanh sự cố. So sánh các quan sát từ các tài khoản độc lập với mức độ hiển thị được nêu rõ của chúng.

**Cần đảm bảo:** một chuỗi các phiên bản được lưu giữ cùng với các khoảng thời gian không xác định được nêu rõ. Không được coi việc một tin nhắn trong lịch sử không còn tồn tại là bằng chứng cho thấy một cá nhân cụ thể nào đó đã xóa tin nhắn đó.

**Một người tham gia thay đổi tên trong nhiều cuộc trò chuyện**

**Câu hỏi:** Hoạt động nào được quan sát thấy thuộc về cùng một tài khoản Telegram mặc dù tên tài khoản đã thay đổi?

**Quá trình theo dõi:** ID người gửi dạng số → lịch sử tên/tên người dùng đã lưu → các phản hồi → các cuộc trò chuyện khác trong không gian làm việc → các địa chỉ được đề cập và các tệp đã lưu. Kiểm tra các bản ghi nguồn cho mọi kết nối được xác định; phân biệt rõ các tài khoản có tên tương tự.

**Cung cấp:** dòng thời gian hoạt động của tài khoản kèm theo các nguồn tham chiếu và các giả thuyết riêng biệt về các mối quan hệ. Sự trùng khớp về tên và giá trị pHash của ảnh đại diện chỉ là manh mối, không phải bằng chứng xác thực danh tính.
