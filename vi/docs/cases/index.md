# Điều tra trên tất cả các cuộc trò chuyện

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/cases/

Một vụ việc trọn vẹn qua kênh, nhóm, trò chuyện riêng và bot: thu thập, nối các manh mối, dựng lại dòng thời gian, bàn giao.

Một sự cố bịa, từ đầu đến cuối. Thu thập, tìm kiếm và hồ sơ người tìm ra các bản ghi, [Case Board](https://phishdestroy.github.io/TgWitness/vi/docs/case-board/) sắp xếp chúng, [Report studio](https://phishdestroy.github.io/TgWitness/vi/docs/reports/) trình bày chúng.

TRƯỜNG HỢP ĐÃ XỬ LÝ / ĐỊA CHỈ NHẬN THANH TOÁN ĐÃ ĐƯỢC THAY ĐỔI

### Một sự cố. Bốn cuộc trò chuyện. Một dấu vết cần được tái hiện.

Một bài đăng trên kênh trỏ tới một bot. Một nhóm bàn về liên kết thanh toán mới và bot hiển thị nó. Bài đăng bị sửa, một cuộc trò chuyện riêng lặp lại liên kết, một tin nhắn trong nhóm biến mất.

Ai là người đã đăng tải từng phiên bản?Liên kết này xuất hiện ở đâu?Tệp nào đã được lưu giữ?Điều gì đã thay đổi và vào thời điểm nào?

Tải lịch sử, AI, MCP, OCR và webhook: [Làm việc với kho lưu trữ](https://phishdestroy.github.io/TgWitness/vi/docs/archive/).

## 1. Đảm bảo phạm vi bao quát toàn bộ tài khoản

Phạm vi toàn tài khoản chỉ dùng cho tài khoản chuyên dụng. Tài khoản chính chỉ dùng các cuộc trò chuyện được chọn hoặc một thư mục.

1. [Kết nối tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/accounts/) trong không gian làm việc riêng. Ghi lại mã vụ việc, ID tài khoản, không gian làm việc và dấu vân tay khóa.
2. **Nguồn → Phạm vi quan sát → Chế độ điều tra**: **Toàn bộ tài khoản**, cả bốn loại nguồn, **Hành động của chính mình**. Mỗi cuộc trò chuyện mới được lưu hồ sơ và **200 tin nhắn hiển thị** gần nhất. **Lưu phạm vi** và xác nhận.
3. **Tải các cuộc trò chuyện** và so sánh với danh sách trò chuyện của tài khoản. Giới hạn là 1.000 hội thoại (tối đa 20.000 trong **Tham số → Các cuộc trò chuyện được đọc từ danh sách tài khoản**); những cuộc vượt giới hạn sẽ hiện ra khi chúng có hoạt động.
4. **Cài đặt ghi lại** → **Tất cả hoạt động hiển thị**, kiểm tra giới hạn tệp đính kèm và dung lượng đĩa. Khởi động, rồi thử bằng một tin nhắn, một lần sửa và một lần xóa.

Các kênhCác nhómCác cuộc trò chuyện riêng tưCác bot

MỘT TÀI KHOẢN / MỘT KHÓA KÝ**Tất cả các hoạt động có thể nhìn thấy trên tài khoản đã được chọn → một sổ ghi chép duy nhất**

Tin nhắn · các thao tác chỉnh sửa · thông báo xóa · phản ứng hiển thị · các sự kiện liên quan đến tư cách thành viên · các hành động của chính người dùng

"Toàn bộ tài khoản" nghĩa là mọi cuộc trò chuyện tài khoản này mở được, trừ các mục loại trừ. Không gồm trò chuyện bí mật. Cuộc trò chuyện mới được thêm khi xuất hiện; lịch sử cũ không tự động tải xuống.

## 2. Thu thập lịch sử và bảo quản các tệp tin

Tạo một bộ sưu tập Case Board và đánh dấu những gì quan trọng. Giữ sổ đăng ký nguồn: ID trò chuyện, tiêu đề, tài khoản, vai trò, thời điểm bắt đầu ghi trực tiếp, kết quả lịch sử, kết quả phương tiện, khoảng trống.

| Yêu cầu | Thao tác trên bảng điều khiển | Các tính năng mà công cụ này cung cấp |
| --- | --- | --- |
| Lịch sử trong các cuộc trò chuyện đã kích hoạt | Nguồn → Tải lịch sử đầy đủ | Các tin nhắn trước đây có sẵn sẽ được đưa vào nhật ký không gian làm việc, kèm theo tính năng tạm dừng/tiếp tục và báo cáo tiến độ có chữ ký. [Hướng dẫn lịch sử](https://phishdestroy.github.io/TgWitness/vi/docs/reference/history/). |
| Bối cảnh cuộc trò chuyện hiện có trong sổ ghi chép | Nguồn → Cài đặt ghi lại → Bản chụp lịch sử | Các tin nhắn gần đây dưới dạng bản ghi có chữ ký. Mặc định 500, tối đa 10.000 trong **Tham số → Bản chụp lịch sử lớn nhất**. |
| Lịch sử đầy đủ hiện có của một cuộc trò chuyện | Xuất toàn bộ cuộc trò chuyện → Xuất toàn bộ cuộc trò chuyện, hoặc Cuộc trò chuyện → Xuất cuộc trò chuyện | Một gói có chữ ký riêng chứa `chat.json` và `chat.html`, mỗi cuộc trò chuyện một gói. |
| Bối cảnh khi một cuộc trò chuyện mới xuất hiện | Phạm vi quan sát → Khi một cuộc trò chuyện hoặc bot mới xuất hiện | Hồ sơ của nó và tối đa 1.000 tin nhắn gần đây (200 trong Chế độ điều tra). Không áp dụng cho các cuộc trò chuyện đã có. |
| Dung lượng tệp đính kèm | Tải xuống các tệp đính kèm có thể xem được + giới hạn theo từng loại | Tìm `media.saved` kèm SHA-256 và kích thước. Đang chờ, bị bỏ qua hoặc thất bại nghĩa là chưa được lưu. |

Bản xuất trò chuyện không đi vào sổ nhật ký hay hồ sơ người. Để tìm lịch sử cũ bên trong TgWitness, hãy dùng **Tải toàn bộ lịch sử** hoặc bản chụp.

Ở đây: kênh, nhóm, cuộc trò chuyện với bot và cuộc trò chuyện riêng, cùng tệp hóa đơn và mã băm của nó. Những gì bị xóa trước khi ghi đã mất.

## 3. Theo dõi diễn biến cuộc trò chuyện và các hành động của chính quý vị

Cứ để nó chạy. Gắn sao cho các cuộc trò chuyện nóng để ưu tiên, chỉnh việc kiểm tra lại trong **Cài đặt ghi lại → Kiểm tra lại**, và theo dõi `recheck.completed`, FloodWait cùng kết quả phương tiện.

**Trò chuyện → Hồ sơ → Lưu hồ sơ ngay** lưu phần mô tả của cuộc trò chuyện, lệnh bot và siêu dữ liệu khác.

**Theo dõi một bot hoặc lời mời trong khuôn khổ vụ việc**

1. **Trò chuyện → Mở liên kết Telegram**, lưu bản xem trước trước. Liên kết và bản xem trước trở thành bản ghi có chữ ký.
2. Nếu cần, **Tham gia / mở và quan sát** sẽ tham gia cuộc trò chuyện hoặc khởi động bot với tham số khởi động của nó.
3. Để ghi lại một hành động, hãy trả lời hoặc dùng **Nhấn nút** từ bảng điều khiển. Bạn nhận được `interaction.requested` và `interaction.result` kèm câu trả lời của bot.

Đây là những hành động thật. Nút được nhấn trong ứng dụng khác không nhìn thấy được, chỉ thấy câu trả lời của bot. Không hỗ trợ ứng dụng web, thanh toán hay điện thoại/vị trí.

## 4. Theo dõi các cá nhân, liên kết và tệp tin trong các cuộc trò chuyện

1. **Sổ nhật ký**, **Tất cả nguồn**, tìm một cụm từ, tên miền hoặc tên người dùng. Mở kết quả và gửi chúng **Vào bảng**.
2. **Trò chuyện → Mọi người → Bật hồ sơ**, chọn một người: lịch sử tên, các lần trả lời, hoạt động, **Cũng có trong…**, liên kết, ví, số điện thoại. Mở các bản ghi được trích dẫn.
3. Lần theo cùng một ID người dùng dạng số sang các cuộc trò chuyện khác. Trùng tên, ví hay ảnh đại diện là manh mối, không phải bằng chứng.
4. So sánh mã băm tệp. Cùng SHA-256 = cùng byte. Ai đã chia sẻ chúng là một câu hỏi khác.

BẢN ĐỒ VỤ VIỆC / THEO DÕI CÁC THAM CHIẾUTrường hợp giả định · không phải biểu đồ thực tế

KÊNH / THÔNG BÁO**Bản gốc → bản đích đã chỉnh sửa**

Bản ghi số 101, số 188 – Tin nhắn số 84 · không xác định người gửi

NHÓM / HOẠT ĐỘNG**Người dùng 71001 đã đăng liên kết mới**

Bản ghi số 146 · tin nhắn số 309 · Biên nhận tệp đã lưu số 151

BOT / CUỘC TRÒ CHUYỆN ĐẶT HÀNG**Một nút bấm dẫn đến trang đích đó**

Bản ghi số 173 · tin nhắn số 12: Dữ liệu meta của nút “Quay lại”

RIÊNG TƯ / THEO DÕI**Người dùng 71001 lặp lại địa chỉ đích**

Bản ghi số 205 · tin nhắn số 922 · Biên nhận tệp đã lưu số 209

Bốn cuộc trò chuyện cung cấp các quan sát khác nhau. Theo dõi các bản ghi nguồn cho mọi kết nối; bài đăng trên kênh không có người gửi được xác định.

Các ID số và tham chiếu bản ghi được tạo ra riêng cho hướng dẫn này. Bản đồ giải thích này cho thấy cách kết nối kết quả tìm kiếm, hồ sơ và các bản ghi đã kiểm tra; Case Board lưu trữ các thẻ tương ứng và tham chiếu nguồn.

| Kết nối | Quan sát bổ sung | Kết luận cần giữ lại |
| --- | --- | --- |
| Cùng một tài khoản Telegram | ID người dùng 71001 trong nhóm #146 và cuộc trò chuyện riêng tư #205 | Cùng ID người gửi ở cả hai cuộc trò chuyện. Người đó ngoài đời là ai là một câu hỏi khác. |
| Địa chỉ đích lặp lại | `pay.example.invalid/new` tại #146, siêu dữ liệu nút #173, bài đăng đã chỉnh sửa #188 và #205 | Cùng một liên kết ở bốn nơi. Ai kiểm soát nó thì cần nguồn khác. |
| Cùng số byte tệp | Các giá trị SHA-256 hoàn toàn trùng khớp trong các biên nhận phương tiện đã hoàn tất số #151 và #209 | Hai tệp giống hệt nhau đến từng byte. |

Hồ sơ chỉ bao gồm những người đã viết gì đó trong *không gian làm việc này*, không phải danh sách thành viên. Số trích dẫn mỗi dữ kiện: **Tham số → Số bản ghi được trích dẫn mỗi dữ kiện**.

## 5. Phục dựng trình tự và đánh dấu các khoảng trống

Xem phiên bản trong **Trò chuyện**, rồi **Sổ nhật ký** với **Tất cả nguồn** + **Lần sửa**, **Lần xóa**, **Phạm vi**. Ghi cả hai mốc thời gian vào dòng thời gian: ngày của Telegram và lúc được quan sát.

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

Thứ tự trong sổ nhật ký là thứ tự đến, không nhất thiết là thứ tự xảy ra. Hãy tách riêng bản ghi trực tiếp, bản chụp, tin nhắn khôi phục, lần xóa và "không thấy khi kiểm tra lại", và đánh dấu mọi khoảng trống là không rõ.

## 6. Mở rộng phạm vi áp dụng sang các tài khoản thu thập khác

Mỗi tài khoản một không gian làm việc, các bước như cũ. Ghi lại vai trò và dấu vân tay của từng cái. Số tin nhắn tính theo từng tài khoản, nên luôn nói rõ không gian làm việc và cuộc trò chuyện nào.

Một [nhóm tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/groups/) hiển thị trạng thái, chia sẻ cài đặt và xuất tất cả cùng lúc, mỗi tài khoản vẫn có sổ nhật ký và khóa riêng. Dòng thời gian xuyên tài khoản thì bạn tự dựng trong ghi chú.

Vụ việc kéo dài? Hãy thêm một [nhân chứng độc lập](https://phishdestroy.github.io/TgWitness/vi/docs/witness/), và thử xem mỗi tài khoản thực sự bắt được gì.

## 7. Cung cấp một gói hồ sơ vụ việc có thể kiểm tra được

Một ZIP có chữ ký từ mỗi không gian làm việc (luôn là toàn bộ sổ nhật ký, bộ lọc không ảnh hưởng), cùng hồ sơ người, bản xuất trò chuyện và tệp.

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

Gửi dấu vân tay riêng. Xác minh mọi thứ với chính không gian làm việc của nó:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Giữ kết quả của công cụ xác minh, bản gốc, phạm vi và biên bản chuyển giao cùng các phát hiện của bạn. Viết thành báo cáo trong Report studio. Nếu người nhận cần ít hơn, hãy làm một [bản bàn giao rút gọn](https://phishdestroy.github.io/TgWitness/vi/docs/handover/).
