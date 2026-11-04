# Tìm hiểu cách thức hoạt động của bằng chứng

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/concepts/

Tin nhắn thay đổi. Bản ghi về những gì bạn đã thấy thì không nên đổi, và ai cũng phải kiểm tra được điều đó.

Bên dưới là hai thí nghiệm nhỏ. Tin nhắn giả, mọi thứ chạy trong trình duyệt của bạn, không gì được gửi tới Telegram.

## Từ bản xuất cuộc trò chuyện đến bản ghi có thể xác minh

[Bản xuất của Telegram Desktop](https://telegram.org/blog/export-and-more) lưu lịch sử bạn thấy lúc này dưới dạng HTML hoặc JSON. TgWitness bổ sung một sổ nhật ký thay đổi liên tục, chữ ký trên mọi bản ghi và các điểm kiểm tra mà người khác có thể đối chiếu.

| Nhiệm vụ | Xuất dữ liệu từ Telegram Desktop | TgWitness |
| --- | --- | --- |
| Đọc các cuộc trò chuyện đã lưu | HTML hoặc JSON kèm theo các tệp phương tiện đã chọn | Các cuộc trò chuyện đã lưu, nhật ký có thể tìm kiếm và báo cáo ngoại tuyến |
| Theo dõi sự thay đổi theo thời gian | Lịch sử có sẵn khi xuất | Phiên bản cũ, các lần sửa sau và lần xóa, giữ lại tất cả |
| Kiểm tra các tệp sau khi bàn giao | Các tệp xuất chuẩn HTML/JSON không có chữ ký | Bản kê có chữ ký, bản ghi có chữ ký và báo cáo niêm phong, kiểm tra bằng khóa tin cậy |
| So sánh với trạng thái được lưu giữ trước đó | Giữ một bản sao tham khảo riêng biệt hoặc mã băm | Các điểm kiểm tra đã ký, một nhân chứng riêng biệt và dấu thời gian bên ngoài tùy chọn |

Phần so sánh dựa trên [mã xuất của Telegram Desktop](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) tính đến ngày 2 tháng 11 năm 2026.

## Một tin nhắn, ba nhận định

Một tin nhắn mới, một lần sửa và một lần xóa trở thành ba bản ghi riêng biệt. Lần sửa không ghi đè bản đầu, và lần xóa không xóa sạch nó.

01 / QUÁ TRÌNH DI CHUYỂN CỦA TIN NHẮNTrình tự minh họa

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Trình thu thập · Sổ ghi chép · cập nhật → · thêm vào →

XEM CUỘC TRÒ CHUYỆN HIỆN TẠI Tin nhắn số 42

Tin nhắn đã bị xóa

Tin nhắn đã biến mất khỏi giao diện trò chuyện.

SỔ NHẬT KÝ QUAN SÁT 3 bản ghi

1. 01

   `message.new`

   Hẹn gặp lúc 10:00

   ✓
2. 02

   `message.edited`

   Hẹn gặp lúc 11:00

   ✓
3. 03

   `message.deleted`

   Thông báo xóa đối với #42

   ✓

Cả ba quan sát đã nhận được đều được lưu giữ trong sổ ghi chép.

Quy trình đơn giản hóa dành cho một nguồn đã được chọn sẵn. Các bản ghi hoạt động cũng được chia sẻ trong sổ nhật ký thực tế. Việc ghi lại phụ thuộc vào những gì tài khoản có thể xem được và những gì Telegram cung cấp.

Telegram không cho biết ai đã xóa tin nhắn hay chính xác là khi nào. TgWitness để trống các trường đó thay vì đoán.

## Thay đổi một bản ghi. Theo dõi mã băm.

Mỗi bản ghi chứa mã băm của bản ghi trước nó. Một điểm kiểm tra lưu ở nơi khác cố định độ dài sổ nhật ký và mã băm cuối cùng.

02 / HASH-CHAIN SANDBOXSHA-256 thực · các bản ghi mẫu

GHI CHÉP 01**Đã nhận được tin nhắn**`h₁ = SHA-256(e₁)`Liên kết đến 64 số 0

GHI CHÉP 02**Hẹn gặp lúc 11:00**`h₂ = SHA-256(e₂)`Bao gồm thẻ h₁

GHI CHÉP 03**Đã ghi nhận hành vi xóa tin nhắn**`h₃ = SHA-256(e₃)`Bao gồm h₂

ĐƯỢC LƯU TRỮ TẠI NƠI KHÁC**3 bản ghi · tiêu đề `h₃`**Hãy so sánh ranh giới cố định này với nhật ký được cung cấp.

Việc thay đổi một sự kiện sẽ làm thay đổi giá trị băm của nó. Việc tái tạo chuỗi sẽ thay đổi phần đầu của chuỗi. Việc xóa phần cuối sẽ khiến chuỗi ngắn hơn so với điểm kiểm tra được lưu giữ.

**Xem bản ghi số 2 và các giá trị băm đầy đủ**

Đây chính là dữ liệu JSON định dạng UTF-8 đã được băm trong ví dụ này. Các giá trị trong đây là hư cấu; chín trường dữ liệu và cách tuần tự hóa đều phù hợp với định dạng sổ nhật ký.

```

```

Bản ghi đã lưu 2 hash

``

Băm của bản ghi số 2 đã được tính toán lại

``

Môi trường thử nghiệm này chỉ tính toán các giá trị băm, không phải chữ ký. Công cụ xác minh thực tế cũng kiểm tra chữ ký Ed25519, trình tự và liên kết của từng sự kiện. Việc chỉ tái tạo các giá trị băm không thể tạo ra các chữ ký hợp lệ dưới khóa tin cậy.

## Các quy tắc cụ thể, tóm tắt trong vài dòng

HASH + CHỮ KÝ

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** là chín trường sự kiện dưới dạng JSON UTF-8: khóa được sắp xếp, không có khoảng trắng thừa, không thoát ASCII, không NaN/vô cực. `previous_hash` là hi−1, h0 là 64 số không, chữ ký bao phủ 32 byte thô của bản tóm lược.

Các trường: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. Đặc tả đầy đủ: [mã hóa sự kiện](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#event-canonicalization).

ĐIỂM KIỂM TRA ĐƯỢC GIỮ LẠI

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Kiểm tra chữ ký điểm kiểm tra bằng khóa đã ghim, rồi so sánh với sổ nhật ký. Bản xuất sau có thể dài hơn, nhưng phải khớp tại điểm kiểm tra.

## Ba câu hỏi, ba bước kiểm tra khác nhau

[01 / TÍNH TOÀN VẸN**Bản ghi này có thay đổi không?** Mã băm và chữ ký đối chiếu với khóa bạn tin cậy.](https://phishdestroy.github.io/TgWitness/vi/docs/exports/)[02 / TÍNH LIÊN TỤC**Những nội dung nào đã được lưu giữ trước đó?** So sánh bản xuất với các điểm kiểm tra mà nhân chứng đã lưu.](https://phishdestroy.github.io/TgWitness/vi/docs/witness/)[03 / PHƯƠNG THỨC CUNG CẤP**Các sự kiện thử nghiệm này đã được gửi đến chưa?** Gửi, sửa và xóa tin nhắn thử, rồi xem mỗi tài khoản bắt được gì.](https://phishdestroy.github.io/TgWitness/vi/docs/cases/)

Chữ ký trả lời "có bị thay đổi không", điểm kiểm tra trả lời "có khớp với những gì có trước đó không", tin nhắn thử trả lời "chúng ta có bắt được hết không". [Xác minh chứng minh được gì và không chứng minh được gì.](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#verification-scope)

Tiếp theo: một [cuộc điều tra toàn bộ tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/cases/) từ đầu đến gói hồ sơ vụ việc.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
