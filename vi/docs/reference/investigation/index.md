# Chế độ điều tra

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/investigation/

Các cuộc điều tra toàn diện về tài khoản trên các kênh, nhóm, cuộc trò chuyện riêng tư và bot, từ phạm vi điều tra cho đến bộ hồ sơ vụ việc đã được xác minh.

Theo dõi một vụ việc qua các kênh, nhóm, cuộc trò chuyện riêng tư và bot, từ giai đoạn thu thập ban đầu cho đến dòng thời gian được trích dẫn và quá trình chuyển giao có thể xác minh. Phiên bản trang web tương tác có tại `/docs/cases/`; [hướng dẫn xem trước](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

## Ví dụ thực tế: sự thay đổi về điểm đến trong bốn cuộc trò chuyện

Một thông báo đề cập đến một bot. Một nhóm vận hành thảo luận về một địa chỉ thanh toán mới, bàn phím của bot hiển thị thông tin đó, và một tin nhắn riêng tư tiếp theo lặp lại nội dung này. Sau đó, thông báo này bị chỉnh sửa và một tin nhắn nhóm biến mất.

Các câu hỏi đặt ra là: những gì đã được quan sát trước và sau khi thay đổi, tài khoản Telegram nào đã đăng từng nội dung, đích đến xuất hiện ở đâu, các byte tệp đính kèm nào đã được lưu giữ, và những khoảng thời gian nào vẫn chưa được xác định?

Tất cả tên, ID, thời gian và các tham chiếu trong sổ ghi chép trong ví dụ này đều là hư cấu. Quy trình làm việc sử dụng các tính năng hiện có; sơ đồ vụ việc chỉ mang tính minh họa, không phải là biểu đồ tự động được tạo ra bởi ứng dụng.

Sơ đồ quy trình · Các kênh → Nhật ký không gian làm việc; Các nhóm → Nhật ký không gian làm việc; Các cuộc trò chuyện riêng tư → Nhật ký không gian làm việc; Các bot → Nhật ký không gian làm việc; Nhật ký không gian làm việc → Tìm kiếm trên tất cả các nguồn; Nhật ký không gian làm việc → Hồ sơ cá nhân kèm theo các tham chiếu đến hồ sơ ghi chép; Nhật ký không gian làm việc → Các phiên bản đã lưu và biên nhận tệp đính kèm; Tìm kiếm trên tất cả các nguồn → Dòng thời gian của nhà phân tích và sổ đăng ký nguồn; Hồ sơ cá nhân kèm theo các tham chiếu đến hồ sơ ghi chép → Dòng thời gian của nhà phân tích và sổ đăng ký nguồn; Các phiên bản đã lưu và biên nhận tệp đính kèm → Dòng thời gian của nhà phân tích và sổ đăng ký nguồn; Nhật ký không gian làm việc → Tệp ZIP chứa bằng chứng đã được ký xác thực; Dòng thời gian của nhà phân tích và sổ đăng ký nguồn → Chuyển giao vụ việc kèm theo các bằng chứng đã được xác minh riêng biệt; Tệp ZIP chứa bằng chứng đã được ký xác thực → Chuyển giao vụ việc kèm theo các bằng chứng đã được xác minh riêng biệt · Các kênh · Các nhóm · Các cuộc trò chuyện riêngtư · Các bot · Nhật ký không gian làmviệc · Tìm kiếm trên tất cả cácnguồn · Hồ sơ cá nhân kèm theo cáctham chiếu đến hồ sơ ghichép · Các phiên bản đã lưu vàbiên nhận tệp đính kèm · Tệp ZIP chứa bằng chứng đãđược ký xác thực · Dòng thời gian của nhàphân tích và sổ đăng kýnguồn · Chuyển giao vụ việc kèmtheo các bằng chứng đãđược xác minh riêng biệt

**Sơ đồ dưới dạng văn bản**

1. Các kênh → Nhật ký không gian làm việc
2. Các nhóm → Nhật ký không gian làm việc
3. Các cuộc trò chuyện riêng tư → Nhật ký không gian làm việc
4. Các bot → Nhật ký không gian làm việc
5. Nhật ký không gian làm việc → Tìm kiếm trên tất cả các nguồn
6. Nhật ký không gian làm việc → Hồ sơ cá nhân kèm theo các tham chiếu đến hồ sơ ghi chép
7. Nhật ký không gian làm việc → Các phiên bản đã lưu và biên nhận tệp đính kèm
8. Tìm kiếm trên tất cả các nguồn → Dòng thời gian của nhà phân tích và sổ đăng ký nguồn
9. Hồ sơ cá nhân kèm theo các tham chiếu đến hồ sơ ghi chép → Dòng thời gian của nhà phân tích và sổ đăng ký nguồn
10. Các phiên bản đã lưu và biên nhận tệp đính kèm → Dòng thời gian của nhà phân tích và sổ đăng ký nguồn
11. Nhật ký không gian làm việc → Tệp ZIP chứa bằng chứng đã được ký xác thực
12. Dòng thời gian của nhà phân tích và sổ đăng ký nguồn → Chuyển giao vụ việc kèm theo các bằng chứng đã được xác minh riêng biệt
13. Tệp ZIP chứa bằng chứng đã được ký xác thực → Chuyển giao vụ việc kèm theo các bằng chứng đã được xác minh riêng biệt

## 1. Xác định vụ việc và thu thập toàn bộ diễn biến sự việc

1. Kết nối tài khoản thu thập dữ liệu trong không gian làm việc riêng của nó. Trong các ghi chú vụ việc bên ngoài, hãy ghi lại mã tham chiếu vụ việc, ID tài khoản, không gian làm việc, thời điểm bắt đầu quan sát và dấu vân tay khóa ký đáng tin cậy.
2. **Nguồn** mở **→ Phạm vi quan sát → Chế độ điều tra**. Cài đặt sẵn sẽ chọn **Toàn bộ tài khoản**, các kênh/nhóm/cuộc trò chuyện riêng tư/bot, các hành động của chính người dùng, hồ sơ nguồn và 200 tin nhắn hiển thị gần nhất đối với các nguồn mới được phát hiện. Hãy xem xét lại, nhấn **Lưu phạm vi** và hoàn tất việc xác nhận phạm vi.
3. **Tải các cuộc trò chuyện** và so sánh các nguồn với danh sách cuộc trò chuyện của tài khoản. Kiểm tra các trường hợp loại trừ. Trong **phần Thông số → Số lượng cuộc trò chuyện được đọc từ danh sách tài khoản** mặc định là 1.000 và cho phép tối đa 20.000. Các nguồn vượt quá giới hạn danh sách sẽ được thêm vào khi chúng trở nên hoạt động. Ghi lại những gì thực tế đã được liệt kê.
4. Trong **phần Cài đặt ghi lại**, hãy chọn **“Tất cả hoạt động hiển thị”** và lưu các cài đặt giám sát. Kiểm tra các loại tệp đính kèm/giới hạn và dung lượng đĩa trống.
5. Bắt đầu quá trình quan sát. Xác thực một tin nhắn mới được kiểm soát, các thao tác chỉnh sửa và xóa, sau đó lưu giữ các tham chiếu thử nghiệm cùng mọi lỗi phát sinh.

Chế độ ghi lại toàn bộ tài khoản sẽ ghi lại các hoạt động hiển thị trên tài khoản theo các cài đặt đã lưu. Công cụ này không truy cập vào các cuộc trò chuyện bí mật cũng như không tự động tham gia vào mọi nhóm được liên kết. Ngoài ra, công cụ này cũng không khôi phục lại toàn bộ các cuộc trò chuyện hiện có. Vui lòng tham khảo [phạm vi thu thập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account).

## 2. Lập danh mục tất cả các nguồn và thu thập bối cảnh lịch sử

Quản lý sổ đăng ký nguồn với mỗi cuộc trò chuyện được ghi vào một hàng riêng biệt:

| Lĩnh vực | Ghi lại |
| --- | --- |
| Thông tin nhận diện | Không gian làm việc, ID tài khoản, ID cuộc trò chuyện dạng số, tiêu đề và loại |
| Khả năng hiển thị | Tư cách thành viên/vai trò, quyền truy cập đã được xác nhận hoặc chưa được xác nhận, các trường hợp loại trừ |
| Ghi lại theo thời gian thực | Thời điểm bắt đầu, các loại sự kiện được chọn và những thay đổi về chính sách sau này |
| Lịch sử nhật ký | Yêu cầu/hoàn tất bản chụp nhanh, giới hạn, thời gian và các tham chiếu bản ghi |
| Lịch sử đầy đủ | Tên tệp xuất theo từng cuộc trò chuyện có chữ ký, phạm vi và trạng thái hoàn tất/thất bại |
| Tệp đính kèm | Các thông tin về biên nhận phương tiện truyền thông đã hoàn tất, mã băm, kích thước cũng như các kết quả bị bỏ qua hoặc không thành công |
| Phạm vi bao quát | Các sự cố ngừng hoạt động, dữ liệu thu thập không đầy đủ, FloodWait, tin nhắn không khả dụng và các lỗ hổng khác |

Sử dụng phương thức thu thập phù hợp cho từng nguồn:

- **Tải toàn bộ lịch sử** trong **Sources** (hiện tại là `main`) sẽ tải các tin nhắn trong quá khứ có sẵn từ các nguồn đã kích hoạt vào nhật ký không gian làm việc. Tính năng này hỗ trợ tạm dừng/tiếp tục và báo cáo tiến trình có chữ ký. Xem [phần thu thập lịch sử](https://phishdestroy.github.io/TgWitness/vi/docs/reference/history/).
- **Tính năng chụp nhanh lịch sử** lưu các tin nhắn hiển thị gần đây vào nhật ký quan sát. Giá trị mặc định tối đa là 500; quý vị có thể tăng con số này lên 10.000 thông qua **mục Thông số → Số lượng tin nhắn tối đa trong bản chụp nhanh lịch sử**. Đây là các quan sát lịch sử hiện tại, không phải các thao tác chỉnh sửa được tái tạo.
- **Xuất toàn bộ cuộc trò chuyện → Xuất toàn bộ cuộc trò chuyện**, hoặc **Cuộc trò chuyện → Xuất cuộc trò chuyện**, sẽ trích xuất lịch sử hiện đang hiển thị của một cuộc trò chuyện vào một gói `chat.json` / `chat.html` được ký số riêng biệt. Lặp lại thao tác này đối với các nguồn của vụ việc và lưu giữ từng kết quả.
- **Khi một cuộc trò chuyện hoặc bot mới xuất hiện,** hệ thống có thể lưu lại hồ sơ của nó cùng tối đa 1.000 tin nhắn gần đây; chế độ Điều tra sẽ chọn 200 tin nhắn. Các cuộc trò chuyện hiện có sẽ không được lưu lại các tin nhắn đó một cách hồi tố khi chế độ này được kích hoạt.
- **Việc tải xuống các tệp đính kèm hiển thị** sẽ lưu giữ số byte theo chính sách đã cấu hình. Yêu cầu phải có biên nhận `media.saved` hoàn chỉnh kèm theo mã SHA-256 và số byte. Một tác vụ đang chờ xử lý, hình thu nhỏ hoặc tên tệp không được coi là tệp đính kèm được lưu giữ.

Việc xuất toàn bộ cuộc trò chuyện sẽ **không** tự động điền vào sổ ghi chép hoặc hồ sơ người dùng tất cả các tin nhắn của cuộc trò chuyện đó. Hãy sử dụng **tính năng “Tải toàn bộ lịch sử”** hoặc các bản chụp nhanh có giới hạn của sổ ghi chép để lấy lịch sử bạn cần phân tích trong TgWitness. Kiểm tra danh sách nguồn đã kích hoạt trước khi bắt đầu quá trình xử lý lịch sử. Cả hai phương pháp này đều không khôi phục được nội dung mà Telegram không còn cung cấp nữa.

## 3. Lưu giữ diễn biến của vụ việc và các tương tác có chủ đích

Đánh dấu các cuộc trò chuyện liên quan đến vụ việc đang diễn ra làm nguồn ưu tiên. Rà soát khoảng thời gian kiểm tra lại, quá trình bổ sung dữ liệu liên tục và kết quả liên quan đến phương tiện truyền thông. Duy trì hoạt động theo dõi của trình thu thập dữ liệu trong suốt quá trình sử dụng tài khoản. Sử dụng **Chats → Profile → Save profile now** để lưu giữ siêu dữ liệu nguồn như mô tả và lệnh bot. Thông tin này độc lập với hồ sơ cá nhân được trích xuất từ các tin nhắn đã lưu.

Trong trường hợp liên quan đến việc theo dõi một nguồn tin hoặc tương tác với một bot:

1. **Mở liên kết Telegram → Lưu bản xem trước** sẽ ghi lại liên kết được cung cấp và bản xem trước hiển thị trước khi thực hiện hành động.
2. **Lệnh "Join / open and observe"** thực hiện thao tác tham gia/mở và gửi tham số khởi động của bot khi được cung cấp. Yêu cầu tham gia đang chờ phê duyệt sẽ được ghi lại với trạng thái "đang chờ xử lý".
3. Các phản hồi văn bản do bảng điều khiển phát ra và các thao tác nhấn nút được hỗ trợ sẽ giữ nguyên mã `interaction.requested` và `interaction.result`. Biên nhận phản hồi có thể lưu giữ văn bản cửa sổ bật lên được trả về, trạng thái cảnh báo và URL.

Đó là các hành động thực tế trên tài khoản. Các thao tác nhấn nút gọi lại trong một ứng dụng Telegram khác sẽ không hiển thị với trình thu thập dữ liệu, mặc dù các tin nhắn hoặc thao tác chỉnh sửa phát sinh từ đó có thể được ghi lại. Ứng dụng khách thu nhỏ (mini-client) không thực hiện các quy trình liên quan đến ứng dụng web, thanh toán, điện thoại hoặc vị trí. Để biết chi tiết về cách thức hoạt động, vui lòng tham khảo [phần tương tác với bảng điều khiển](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/#act-from-the-panel).

## 4. Liên kết các quan sát giữa các cuộc trò chuyện

Trong mục **Journal**, hãy chọn **“Tất cả nguồn”** và tìm kiếm nội dung đã được ghi lại. Mở các bản ghi phù hợp và lưu lại không gian làm việc, cuộc trò chuyện, ID tin nhắn, thứ tự cũng như mã băm của bản ghi.

Trong một cuộc trò chuyện liên quan, hãy mở **mục “Người dùng” → “Bật hồ sơ”** và kiểm tra thông tin của một người dùng:

- Các tên/tên người dùng được ghi nhận theo thời gian và mã định danh số (ID) trên Telegram.
- Các mối quan hệ phản hồi kèm theo tham chiếu đến bản ghi nguồn.
- **Ngoài ra còn có…** các cuộc trò chuyện khác trong nhật ký không gian làm việc này mà ID đó đã tham gia.
- Hoạt động, các thao tác chỉnh sửa/xóa cũng như các ví, số điện thoại, tên người dùng và liên kết được đề cập.
- Dữ liệu siêu dữ liệu của ảnh đại diện đã lưu và các ảnh đại diện tương tự được lưu trong bộ nhớ đệm, kèm theo nguồn gốc riêng biệt của từng ảnh.

Vui lòng mở các bản ghi được trích dẫn trước khi sử dụng hồ sơ được tạo ra từ đó trong kết luận điều tra. Các hồ sơ này bao gồm những người có tin nhắn được lưu trữ, chứ không phải mọi thành viên trong nhóm. **Thông số → Số lượng bản ghi được trích dẫn cho mỗi sự kiện** sẽ giới hạn danh sách tham chiếu, chứ không phải số lượng hoạt động cơ bản. Các đề cập và mức độ tương đồng của ảnh đại diện chỉ là manh mối; chúng không xác định quyền sở hữu hay danh tính.

Trong ví dụ minh họa:

| Liên kết | Ghi lại | Quan sát được hỗ trợ |
| --- | --- | --- |
| Cùng một tài khoản người gửi | Nhóm #146 và cuộc thảo luận riêng tư tiếp theo #205 | Cả hai đều cung cấp ID người gửi Telegram là 71001 |
| Cùng một đích đến | #146, bàn phím bot #173, chỉnh sửa kênh #188, tin nhắn riêng tư #205 | Tất cả đều chứa mã `pay.example.invalid/new`; quyền sở hữu/quyền kiểm soát chưa được xác định |
| Tệp lưu trữ tương tự | Đã hoàn tất các biên nhận phương tiện truyền thông số #151 và #209 | Các giá trị SHA-256 đầy đủ trùng khớp với các byte được lưu giữ |
| Nguồn thông tin kênh | #101 và #188 | Không được quy cho người dùng 71001 là tác giả của bài đăng trên kênh nếu không có thông tin xác định người gửi |

So sánh các giá trị băm của tệp đính kèm và các tham chiếu tin nhắn liên quan. Các tệp giống hệt nhau không đủ để xác định người tạo, người chuyển tiếp hoặc người vận hành chung. Chỉ riêng việc có cùng tên và hình đại diện tương tự không đủ để kết luận rằng hai ID Telegram thuộc về cùng một người.

## 5. Xây dựng dòng thời gian liên cuộc trò chuyện

Sử dụng các phiên bản đã lưu trong **phần Trò chuyện** cùng các liên kết **bản ghi Nhật ký #…** tương ứng. Trong **Nhật ký**, kết hợp **Tất cả các nguồn** với **các thao tác Chỉnh sửa**, **Xóa bỏ** và **Phạm vi ghi nhận**. Giữ lại cả mã `source_at` (nếu có) và mã `observed_at`.

| Thời gian quan sát minh họa | Tham khảo | Quan sát |
| --- | --- | --- |
| 09:00 | Kênh #101 | Địa chỉ đích ban đầu đã được ghi lại |
| 09:12 | Nhóm #146; phương tiện truyền thông #151 | Đã đăng tải địa chỉ đích mới; quá trình tải xuống tệp đã hoàn tất |
| 09:16 | Bot số 173 | Bàn phím chỉ đến đích mới |
| 09:20 | Kênh #188 | Thông báo đã được chỉnh sửa; cả hai phiên bản đã lưu đều được giữ lại |
| 09:24 | Tư nhân #205; phương tiện truyền thông #209 | ID người gửi trùng khớp với địa chỉ nhận; các byte của tệp được giữ nguyên |
| 09:28 | Nhóm #231 | Đã nhận được thông báo xóa; người xóa và thời gian xóa chính xác hiện chưa được xác định |

Các bản ghi khác có thể xuất hiện giữa các tham chiếu ví dụ này. Số thứ tự sắp xếp các quan sát; các bản chụp lịch sử có thể chứa ngày nguồn cũ hơn và được gửi đến muộn hơn so với các sự kiện đang diễn ra. Hãy phân biệt rõ các bản chụp, tin nhắn đã khôi phục, thông báo xóa và kết quả “không tìm thấy khi kiểm tra lại”. Đánh dấu các khoảng trống trong phạm vi ghi nhận là các khoảng thời gian chưa xác định. Việc thu thập lịch sử sau này không có nghĩa là xác lập được việc quan sát liên tục một cách hồi tố.

## 6. Thêm các góc nhìn từ tài khoản mà không làm mất nguồn gốc của chúng

Hãy sử dụng một không gian làm việc riêng biệt cho từng tài khoản khác nhau và lặp lại quy trình kiểm kê đối với từng tài khoản đó. Lưu giữ ID tài khoản, vai trò, dấu vân tay khóa ký và các tham chiếu nguồn trong mỗi lần so sánh. Số tin nhắn không phải là mã định danh chung cho tất cả các cuộc trò chuyện/tài khoản.

Việc tương quan giữa các không gian làm việc được thực hiện trong các ghi chú vụ việc bên ngoài hoặc các công cụ phân tích. Hiện tại, TgWitness chưa hỗ trợ tính năng tìm kiếm toàn cầu xuyên không gian làm việc, dòng thời gian hợp nhất, sơ đồ điều tra hoặc kho lưu trữ vụ việc tổng hợp. Việc xuất dữ liệu từ nhiều tài khoản của **một** kênh/siêu nhóm là một thao tác riêng biệt, không phải là việc hợp nhất các nhật ký tài khoản.

Đối với các công việc có quy mô lớn hơn, cần duy trì sự tách biệt với một [nhân chứng độc lập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/). Sử dụng các kiểm tra giao nhận có kiểm soát để xác minh đường dẫn thu thập và phạm vi hiển thị của từng tài khoản.

## 7. Tổng hợp và xác minh việc chuyển giao hồ sơ vụ việc

Vui lòng lưu giữ các tài liệu này cùng nhau trong một thư mục hồ sơ vụ việc do chuyên viên phân tích lập:

| Nội dung | Mục đích |
| --- | --- |
| Ghi chú vụ việc và sổ đăng ký nguồn | Các câu hỏi, chính sách thu thập, quyền truy cập/vai trò, kết quả điều tra, các giải thích thay thế và những điểm còn thiếu sót |
| Dòng thời gian | Các thông tin về thời gian cũng như tham chiếu đến không gian làm việc/cuộc trò chuyện/tin nhắn/chuỗi tin nhắn cho từng mục ghi chép |
| Tệp ZIP chứa bằng chứng đã được ký số cho từng không gian làm việc | Bản ghi nhật ký hoàn chỉnh, bảng kê khai và các tệp phương tiện được lưu giữ kèm theo; các bộ lọc trên bảng điều khiển không làm thu hẹp phạm vi xuất nhật ký |
| Các tệp hồ sơ cá nhân được ký xác thực riêng biệt | Các tài liệu tham khảo được trích dẫn đã được đối chiếu với bằng chứng tương ứng trong không gian làm việc |
| Các bản xuất toàn bộ cuộc trò chuyện đã được ký xác thực | Việc thu thập lịch sử hiển thị hiện tại, tách biệt với sổ ghi chép quan sát |
| Dấu vân tay đáng tin cậy và các điểm kiểm tra trước đó | Các yếu tố nhận diện chính và phạm vi của sổ nhật ký được lưu giữ |
| Các bằng chứng từ Witness, nếu được cấu hình | Sổ nhật ký riêng biệt, các bài đăng có chữ ký và dấu vân tay chứng thực |
| Kết quả xác minh và các giá trị băm của tệp đã được cung cấp | Những nội dung nào đã được kiểm tra, những byte nào đã được chuyển và chuyển cho ai |

Từ một bản cài đặt đáng tin cậy, kèm theo tên tệp và dấu vân tay thực tế của từng không gian làm việc:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Lưu giữ kết quả xác minh thực tế và các bằng chứng gốc. Thư mục cấp cao nhất của vụ việc, sổ đăng ký nguồn và kết luận của nhà phân tích được lưu trữ bên ngoài; mỗi bằng chứng của TgWitness đều có chữ ký và quy trình xác minh riêng.

## Thích ứng với quá trình điều tra

| Trường hợp | Trace | Gửi |
| --- | --- | --- |
| Tranh chấp về đơn hàng/thanh toán do bot xử lý | Thông báo đăng ký → xem trước liên kết đã lưu → tham số khởi động bot → phiên bản tin nhắn và bàn phím → biên nhận gọi lại trên bảng điều khiển → theo dõi tin nhắn riêng tư/nhóm | Dòng thời gian đề nghị/phản hồi được ghi nhận và các nguồn tin đã được xác minh; riêng một liên kết thanh toán không đủ để chứng minh việc thanh toán đã diễn ra |
| Các tin nhắn đã bị xóa sau khi xảy ra sự cố | Tất cả các cuộc trò chuyện bị ảnh hưởng → bản gốc/bản chỉnh sửa đã được lưu trữ → kết quả xóa hoặc không còn tồn tại khi kiểm tra lại → phương tiện truyền thông được bảo toàn → phạm vi bao quát và các góc nhìn khác từ tài khoản | Các phiên bản được lưu giữ và các khoảng thời gian không xác định được nêu rõ; không có đối tượng xóa tin nhắn nào được giả định |
| Một người tham gia thay đổi tên trong các cuộc trò chuyện | ID người gửi dạng số → lịch sử tên/tên người dùng → các phản hồi → các cuộc trò chuyện khác được ghi nhận → các đích đến/tệp tin được trích dẫn | Dòng thời gian hoạt động của tài khoản Telegram được trích dẫn, trong đó các giả thuyết về danh tính và mối quan hệ trong thế giới thực được tách biệt rõ ràng |

[Tham chiếu bộ sưu tập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/collection/) · [Xác minh hồ sơ cá nhân](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#people-profiles) · [Việc chuyển giao bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#investigation-handoff) · [Đã hoàn tất quá trình xác thực](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/)
