# Cách thức hoạt động của bằng chứng

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/how-it-works/

Các khái niệm về chuỗi băm, chữ ký, điểm kiểm tra và nhân chứng được giải thích kèm theo các công thức chính xác mà bên xác minh sử dụng.

TgWitness lưu giữ những gì tài khoản thu thập đã quan sát được, liên kết các quan sát đó vào một nhật ký có chữ ký và cho phép người khác xác minh bản xuất dữ liệu dựa trên một khóa đáng tin cậy cùng với một điểm kiểm tra đã được lưu giữ trước đó.

[Trang web tài liệu địa phương](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally) này bổ sung các ví dụ tương tác tại `/docs/concepts/`, cùng công cụ khám phá quyết định tại các điểm kiểm tra tại `/docs/witness/`. Tất cả các tin nhắn ví dụ, số lượng và thời gian trễ đều là hư cấu. Các giá trị băm trong môi trường thử nghiệm chuỗi được tính toán bằng SHA-256 ngay trong trình duyệt. Không có dữ liệu nào được gửi đến Telegram.

## Một tin nhắn thay đổi; các quan sát được tích lũy

Sơ đồ trình tự · Telegram → Trình thu thập: Tin nhắn mới: Hẹn gặp lúc 10:00; Trình thu thập → Sổ nhật ký có chữ ký: Thêm tin nhắn.new; Telegram → Trình thu thập: Chỉnh sửa: Hẹn gặp lúc 11:00; Trình thu thập → Sổ nhật ký có chữ ký: Thêm tin nhắn.đã chỉnh sửa; Telegram → Trình thu thập: Thông báo về việc xóa nội dung; Trình thu thập → Sổ nhật ký có chữ ký: Thêm tin nhắn.đã xóa; Ghi chú về Sổ nhật ký có chữ ký: Các thông tin về nội dung gốc, nội dung đã chỉnh sửa và các thao tác xóa vẫn được lưu giữ · Telegram · Trình thu thập · Sổ nhật ký có chữ ký · Tin nhắn mới: Hẹn gặp lúc 10:00 · Thêm tin nhắn.new · Chỉnh sửa: Hẹn gặp lúc 11:00 · Thêm tin nhắn.đã chỉnh sửa · Thông báo về việc xóa nội dung · Thêm tin nhắn.đã xóa · Các thông tin về nội dung gốc, nội dung đã chỉnh sửavà các thao tác xóa vẫn được lưu giữ

**Sơ đồ dưới dạng văn bản**

1. Telegram → Trình thu thập: Tin nhắn mới: Hẹn gặp lúc 10:00
2. Trình thu thập → Sổ nhật ký có chữ ký: Thêm tin nhắn.new
3. Telegram → Trình thu thập: Chỉnh sửa: Hẹn gặp lúc 11:00
4. Trình thu thập → Sổ nhật ký có chữ ký: Thêm tin nhắn.đã chỉnh sửa
5. Telegram → Trình thu thập: Thông báo về việc xóa nội dung
6. Trình thu thập → Sổ nhật ký có chữ ký: Thêm tin nhắn.đã xóa
7. Ghi chú về Sổ nhật ký có chữ ký: Các thông tin về nội dung gốc, nội dung đã chỉnh sửa và các thao tác xóa vẫn được lưu giữ

Quy trình đơn giản hóa này giả định rằng Telegram đã gửi thành công mỗi bản cập nhật và tài khoản được chọn có thể xem được nội dung đó. Các sự kiện vận hành cũng được ghi lại trong sổ nhật ký. Thông báo xóa không cung cấp thông tin về người xóa hoặc thời gian xóa chính xác. Các lần gửi lặp lại được xem là các quan sát riêng biệt; không có cơ chế loại bỏ bản sao trùng lặp trên toàn bộ sổ nhật ký.

## Phạm vi bao phủ của một giá trị băm

![Quan sát, mã hóa, tính băm và ký số: mỗi sự kiện mới đều bao gồm giá trị băm của sự kiện trước đó.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

Hãy đọc công thức từ trong ra ngoài: **C** chuyển chín trường dữ liệu thành các byte chính xác; **SHA-256** tạo ra giá trị băm của chúng; **hex** là định dạng lưu trữ giá trị băm đó. Giá trị băm trước đó đã có sẵn trong sự kiện. **unhex** chuyển giá trị băm đã lưu trữ trở lại thành 32 byte mà Ed25519 dùng để ký.

[Sơ đồ chuỗi tĩnh](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

Giả sử C(ei) là định dạng JSON chuẩn UTF-8 của chín trường sự kiện. Bản ghi đầu tiên `previous_hash` gồm 64 ký tự số 0. Mỗi bản ghi tiếp theo đều chứa mã băm thập lục phân của bản ghi trước đó:

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

Chữ ký bao phủ 32 byte băm thô. Dữ liệu đầu vào băm chứa chính xác các giá trị `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` và `previous_hash`. Các khóa đối tượng được sắp xếp theo thứ tự; khoảng trắng và ký tự ASCII được loại bỏ; các giá trị NaN và vô cực bị từ chối. Vui lòng tham khảo cách [mã hóa chính xác](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#event-canonicalization).

Sơ đồ quy trình · 64 ký tự số 0 → Bản ghi 1 / băm h1; Bản ghi 1 / băm h1 → Bản ghi 2 bao gồm h1 / hash h2; Bản ghi 2 bao gồm h1 / hash h2 → Bản ghi số 3 bao gồm h2 / hash h3; Bản ghi số 3 bao gồm h2 / hash h3 → Điểm kiểm tra có chữ ký: số 3, tiêu đề h3 (lưu trữ ở nơi khác) · 64 ký tự số 0 · Bản ghi 1 / băm h1 · Bản ghi 2 bao gồm h1 /hash h2 · Bản ghi số 3 bao gồmh2 / hash h3 · Điểm kiểm tra có chữký: số 3, tiêu đề h3 · lưu trữ ở nơi khác

**Sơ đồ dưới dạng văn bản**

1. 64 ký tự số 0 → Bản ghi 1 / băm h1
2. Bản ghi 1 / băm h1 → Bản ghi 2 bao gồm h1 / hash h2
3. Bản ghi 2 bao gồm h1 / hash h2 → Bản ghi số 3 bao gồm h2 / hash h3
4. Bản ghi số 3 bao gồm h2 / hash h3 → Điểm kiểm tra có chữ ký: số 3, tiêu đề h3 (lưu trữ ở nơi khác)

| Thay đổi thành sổ nhật ký được cung cấp | Yếu tố nhận diện |
| --- | --- |
| Sửa đổi bản ghi số 2 trong khi vẫn giữ nguyên giá trị băm đã lưu trữ | Giá trị băm sự kiện được tính lại có sự khác biệt; chữ ký của nó không còn bao phủ sự kiện đã thay đổi nữa |
| Phục hồi bản ghi đã bị thay đổi cùng mọi giá trị băm được tạo ra sau đó | Các chữ ký ban đầu không hợp lệ; một điểm kiểm tra được lưu giữ tại ranh giới bị ảnh hưởng cũng cho kết quả không khớp |
| Loại bỏ phần đuôi nhưng giữ nguyên phần tiền tố còn lại | Một điểm kiểm tra được lưu giữ trước đó, nằm ngoài tiền tố được cung cấp, cho thấy tệp xuất ra quá ngắn |
| Ký lại một sổ ghi chép thay thế bằng một khóa khác | Dấu vân tay khóa được xác thực độc lập sẽ từ chối danh tính thay thế |

![Việc thay đổi một trường dữ liệu đã lưu sẽ làm thay đổi giá trị băm của trường đó; việc tính toán lại các giá trị băm sẽ không khôi phục được các chữ ký ban đầu.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**Hãy thử áp dụng logic này vào bản ghi số 2:** thay đổi `Meet at 11:00` thành `Meet at 12:00` trong sự kiện đã lưu. Giá trị băm được tính lại của nó sẽ không còn khớp nữa. Việc tính lại chuỗi sau đó có thể khôi phục các liên kết, nhưng không thể khiến các chữ ký ban đầu bao phủ các giá trị băm mới. Ngược lại, một thao tác chỉnh sửa được ghi nhận trên Telegram sẽ trở thành một bản ghi mới trong sổ nhật ký.

[Sơ đồ thay đổi tĩnh](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

Chỉ riêng các liên kết băm (hash) không thể ngăn chặn việc ai đó tính toán lại một chuỗi thay thế. Sự tin cậy xuất phát từ việc kiểm tra các chữ ký dưới một khóa được tin cậy độc lập và so sánh với các bản tham chiếu được lưu giữ bên ngoài hệ thống thu thập dữ liệu.

## Những gì điểm kiểm tra trước đó bổ sung

![Giữ nguyên số đếm 3 và tiêu đề h3; việc xuất 4 bản ghi sau đó sẽ được kiểm tra tại vị trí số 3.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**Điểm tham chiếu sẽ giữ nguyên trong khi nhật ký tiếp tục mở rộng.** Nếu điểm kiểm tra ghi là “3 bản ghi, tiêu đề h3”, thì việc xuất ra bốn bản ghi vẫn có thể thành công bằng cách khớp với h3 tại vị trí thứ 3. Tiêu đề mới nhất của nhật ký là h4, và dự kiến sẽ có sự khác biệt. Việc xuất ra chỉ hai bản ghi sẽ không thành công.

[Sơ đồ điểm kiểm tra tĩnh](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

Sau khi xác minh chữ ký tại điểm kiểm tra, yêu cầu:

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

Quá trình xuất dữ liệu có thể vượt ra ngoài một điểm kiểm tra. Dữ liệu xuất ra phải khớp với ranh giới được lưu giữ. Công cụ xác minh thực tế cũng kiểm tra trình tự của từng sự kiện, liên kết trước đó, giá trị băm và chữ ký. Việc chỉ so sánh phần đầu cuối cùng được lưu trữ sẽ bỏ sót một bản ghi bên trong đã bị thay đổi mà giá trị băm đã lưu của nó chưa được cập nhật.

## Vị trí thích hợp của một nhân chứng

Sơ đồ quy trình · Trình thu thập / phiên tài khoản / khóa A → Điểm cuối kiểm tra chỉ đọc; Witness / khóa thu thập được ghim / khóa riêng B → Sổ nhật ký chứng cứ có chữ ký riêng biệt; Witness / khóa thu thập được ghim / khóa riêng B → Điểm cuối kiểm tra chỉ đọc (Yêu cầu kiểm tra); Điểm cuối kiểm tra chỉ đọc → Witness / khóa thu thập được ghim / khóa riêng B (Câu trả lời đã được ký xác nhận); Witness / khóa thu thập được ghim / khóa riêng B → Kênh với các bài đăng TGW1 đã được ký điện tử (API Bot / mã thông báo riêng) · Máy chủ A · Máy chủ B · Trình thu thập / phiên tàikhoản / khóa A · Điểm cuối kiểm tra chỉ đọc · Witness / khóa thu thậpđược ghim / khóa riêng B · Sổ nhật ký chứng cứ có chữký riêng biệt · Kênh với các bài đăng TGW1đã được ký điện tử · Yêu cầu kiểm tra · Câu trả lời đã được ký xác · nhận · API Bot / mã thông báo riêng

**Sơ đồ dưới dạng văn bản**

1. Trình thu thập / phiên tài khoản / khóa A → Điểm cuối kiểm tra chỉ đọc
2. Witness / khóa thu thập được ghim / khóa riêng B → Sổ nhật ký chứng cứ có chữ ký riêng biệt
3. Witness / khóa thu thập được ghim / khóa riêng B → Điểm cuối kiểm tra chỉ đọc (Yêu cầu kiểm tra)
4. Điểm cuối kiểm tra chỉ đọc → Witness / khóa thu thập được ghim / khóa riêng B (Câu trả lời đã được ký xác nhận)
5. Witness / khóa thu thập được ghim / khóa riêng B → Kênh với các bài đăng TGW1 đã được ký điện tử (API Bot / mã thông báo riêng)

TgWitness ghi lại các thao tác khôi phục, sự thay đổi người đứng đầu tại cùng một số đếm, các khóa bị thay đổi, các câu trả lời không hợp lệ và các phản hồi bị thiếu. Chỉ riêng số đếm lớn hơn không đủ để khẳng định rằng mọi bản ghi trước đó vẫn giữ nguyên; quý vị hãy so sánh tệp xuất với các điểm kiểm tra được lưu giữ. Việc triển khai TgWitness trên một máy chủ khác giúp tránh ảnh hưởng từ sự cố ngừng hoạt động của máy chủ thu thập dữ liệu; việc có một nhà điều hành riêng biệt mang lại sự độc lập bổ sung.

Witness xác nhận trạng thái nhật ký được báo cáo bởi bộ thu thập. Công cụ này không quan sát độc lập tất cả các tin nhắn trên Telegram. Vui lòng tham khảo [phần thiết lập Witness](https://phishdestroy.github.io/TgWitness/vi/docs/reference/witness/).

## Kiểm tra khả năng xử lý các hành động đã biết

Sử dụng một nhóm kiểm soát, các tài khoản thu thập riêng biệt và một dấu hiệu mới. Gửi, chỉnh sửa và xóa một cách có chủ đích, đồng thời kiểm tra việc ghi lại dữ liệu giữa các giai đoạn. Xác định các hành động dự kiến và thời điểm kết thúc trước khi kiểm tra kết quả.

R = |observed∩expected| / |expected| Δ t = treceipt - taction

Chỉ các hành động phù hợp với dự kiến mới được tính; các biên nhận trùng lặp sẽ không làm tăng tử số. Mẫu số phải khác không. Một biên nhận bị thiếu sẽ không có thời gian trễ được đo lường. Hãy ghi nhận độ không chắc chắn về thời gian; hãy sử dụng thời gian thực hiện hành động xóa có kiểm soát của riêng quý vị, vì Telegram không cung cấp thời gian xóa chính xác. Một kết quả như 5/6 (83,3%) mô tả các hành động thử nghiệm, chứ không phải mức độ đầy đủ của toàn bộ lưu lượng Telegram.

## Chọn quy trình làm việc

[Quy trình điều tra đầy đủ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/investigation/) được trình bày theo diễn biến của một sự cố xảy ra trên kênh, nhóm, bot và cuộc trò chuyện riêng tư:

1. Kích hoạt Chế độ điều tra toàn bộ tài khoản và lập danh mục tất cả các cuộc trò chuyện có thể truy cập được.
2. Lấy các bản chụp nhanh nhật ký, lịch sử đầy đủ theo từng cuộc trò chuyện và các tệp đính kèm được lưu giữ.
3. Lưu lại các thay đổi theo thời gian thực và mọi tương tác có chủ đích trên bảng điều khiển kèm theo biên nhận tương ứng.
4. Theo dõi các ID người gửi dạng số, mối quan hệ trả lời, các địa chỉ nhận lặp lại và băm tệp thông qua các bản ghi được trích dẫn và hồ sơ cá nhân.
5. Tái tạo dòng thời gian liên cuộc trò chuyện với cả dấu thời gian và các khoảng trống rõ ràng.
6. So sánh các không gian làm việc của các tài khoản khác nhau trong khi vẫn giữ nguyên nguồn gốc và khóa của từng tài khoản.
7. Tổng hợp và xác minh các nhật ký có chữ ký, hồ sơ người dùng cũng như các bản xuất lịch sử cùng với các ghi chú vụ việc.

Hướng dẫn `/docs/cases/` trên trang web này bao gồm bản đồ vụ việc tương tác cùng các trường hợp cụ thể liên quan đến tranh chấp giữa các bot, tin nhắn bị xóa và việc người tham gia thay đổi tên. Ghi chú vụ việc và phân tích liên không gian làm việc được thực hiện bên ngoài; ứng dụng không tự động tạo ra sơ đồ điều tra tổng thể hay kho lưu trữ vụ việc hợp nhất.

[Các công việc đã hoàn tất và các công việc còn lại](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/) · [Xuất và xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#investigation-handoff) · [Bắt đầu với một tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/quickstart/)
