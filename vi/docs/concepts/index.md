# Tìm hiểu cách thức hoạt động của bằng chứng

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/concepts/

Một tin nhắn có thể thay đổi. Tuy nhiên, bản ghi chép về những gì quý vị đã quan sát được phải luôn đảm bảo tính kiểm chứng được.

Hãy khám phá hai thí nghiệm nhỏ dưới đây. Các thí nghiệm này sử dụng các tin nhắn hư cấu, chỉ hoạt động trong trình duyệt của quý vị và tuyệt đối không kết nối với Telegram.

## Một tin nhắn, ba nhận định

Khi Telegram gửi một tin nhắn mới, một thông báo chỉnh sửa hoặc một thông báo xóa, ứng dụng thu thập dữ liệu sẽ bổ sung ba ghi nhận riêng biệt. Việc chỉnh sửa không thay thế bản ghi ban đầu. Thông báo xóa cũng không làm mất bản ghi đó.

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

Thông báo xóa tin nhắn không cung cấp thời gian xóa đáng tin cậy cũng như danh tính của người đã xóa tin nhắn đó. Việc giữ kín các thông tin này giúp duy trì sự phân biệt rõ ràng giữa một quan sát thực tế và một phỏng đoán.

## Thay đổi một bản ghi. Theo dõi mã băm.

Mỗi bản ghi đều chứa mã băm của bản ghi trước đó. Mã băm của chính bản ghi đó bao phủ các trường sự kiện, bao gồm cả liên kết đó. Một điểm kiểm tra được lưu trữ bên ngoài sẽ cố định độ dài cụ thể của sổ nhật ký và mã băm đầu sổ.

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

**C** tuần tự hóa chín trường sự kiện dưới dạng JSON UTF-8: các khóa được sắp xếp theo thứ tự, không có khoảng trắng thừa, không có mã hóa ASCII và không có giá trị NaN/vô cực. Giá trị `previous_hash` của sự kiện là hi−1. Giá trị h0 được hiển thị có nghĩa là 64 ký tự số 0; các chữ ký bao phủ 32 byte bản tóm tắt thô.

Chín trường dữ liệu bao gồm `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` và `previous_hash`. Đây là [định dạng mã hóa JSON được TgWitness ghi chép](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#event-canonicalization); bản thân các giá trị băm và chữ ký không phải là các trường nhập liệu băm.

ĐIỂM KIỂM TRA ĐƯỢC GIỮ LẠI

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Hãy xác minh chữ ký của điểm kiểm tra dưới khóa thu thập được ghim, sau đó so sánh phạm vi của nó với nhật ký đã được xác minh. Một bản xuất sau này có thể chứa nhiều bản ghi hơn; tuy nhiên, nó vẫn phải khớp với điểm kiểm tra trước đó.

## Ba câu hỏi, ba bước kiểm tra khác nhau

[01 / TÍNH TOÀN VẸN**Bản ghi này có thay đổi không?** Xác minh các giá trị băm và chữ ký so với một khóa đáng tin cậy được lưu trữ riêng biệt.](https://phishdestroy.github.io/TgWitness/vi/docs/exports/)[02 / TÍNH LIÊN TỤC**Những nội dung nào đã được lưu giữ trước đó?** So sánh tệp xuất có chữ ký với các điểm kiểm tra được lưu giữ bởi một bên chứng kiến độc lập.](https://phishdestroy.github.io/TgWitness/vi/docs/witness/)[03 / PHƯƠNG THỨC CUNG CẤP**Các sự kiện thử nghiệm này đã được gửi đến chưa?** So sánh các hành động gửi, chỉnh sửa và xóa được kiểm soát với nhật ký của từng tài khoản.](https://phishdestroy.github.io/TgWitness/vi/docs/cases/)

Một chuỗi băm khớp sẽ trả lời câu hỏi về tính toàn vẹn. Nó không xác nhận việc Telegram đã gửi tin nhắn thành công, tính xác thực của tin nhắn hay thời điểm quan sát được xác nhận độc lập.

Theo dõi [toàn bộ quá trình điều tra tài khoản,](https://phishdestroy.github.io/TgWitness/vi/docs/cases/) từ giai đoạn thu thập dữ liệu cho đến khi hoàn thiện hồ sơ vụ việc.
