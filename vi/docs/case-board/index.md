# Tạo Case Board

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/case-board/

Chuyển các quan sát Telegram đã lưu thành một vụ việc mà nhóm của bạn có thể cùng nhau xem xét.

Case Board lưu trữ các dấu trang, đoạn văn bản được đánh dấu chính xác, các phần trích xuất đã lưu và các cuộc thảo luận bên cạnh các tham chiếu nguồn tương ứng. Một bộ sưu tập (collection) cung cấp cấu trúc làm việc cho vụ án; các bản sửa đổi đã ký tên ghi lại quá trình phát triển của nhóm.

## Từ một tin nhắn đến một thẻ vụ án

1. Mở **Investigation → Case Board** ở chế độ Standard hoặc Expert. Tạo bộ sưu tập cho vụ việc và chọn phạm vi trò chuyện của nó.
2. Trong **Nhật ký** hoặc một cuộc trò chuyện đã lưu, chọn **“Thêm vào bảng**” hoặc chọn bản ghi và nhấn phím **B**. Thẻ sẽ được chuyển vào Hộp thư đến; đặt cho nó một tiêu đề hữu ích và di chuyển nó vào bộ sưu tập của bạn.
3. Chọn một đoạn trong tin nhắn trò chuyện đã lưu và chọn **Highlight → board** để giữ nguyên trích dẫn và phiên bản tin nhắn chính xác. Thêm ghi chú giải thích lý do tại sao điều đó lại quan trọng.
4. Thảo luận về thẻ, gán trạng thái xem xét và quay lại bối cảnh nguồn bất cứ khi nào cần kiểm tra một tuyên bố. Sử dụng **Presentation** để trình bày quá trình thu thập dữ liệu cùng đồng nghiệp.

### Sử dụng một liên kết thanh toán đã được cập nhật

Ví dụ tổng hợp · minh họa địa phương

1. **Ghi lại.** Mở bản ghi quan sát đã lưu #142 và phiên bản tin nhắn của nó.
2. **Đánh dấu trang.** Lưu lại trích dẫn, nguồn tham khảo và câu hỏi của bạn vào một thẻ.
3. **Xem xét.** Thêm bình luận của nhóm và chuyển thẻ sang trạng thái “Xem xét”.
4. **Trình bày.** Hướng dẫn quy trình thu thập và mở bối cảnh nguồn được trích dẫn.

#### Ghi chú đã lưu #142

“Sử dụng liên kết thanh toán mới.”

Trò chuyện vận hành · tin nhắn 38 · quan sát lúc 09:12 UTC

#### Thẻ: đã thay đổi đích đến

> Sử dụng liên kết thanh toán mới.

Câu hỏi: đích đến nào đã xuất hiện trong phiên bản trước đó?

#### Kiểm duyệt của nhóm

Chuyên viên phân tích: so sánh với quan sát số 101.

Trạng thái: Đang xem xét · bản sửa đổi được giữ nguyên

#### Bối cảnh nguồn

Thẻ → phiên bản đã lưu → quan sát trước đó

Chú thích và quá trình quan sát Telegram vẫn có thể được nhận diện riêng biệt.

## Lưu một phạm vi hữu ích một lần

Nhấn Shift và nhấp vào hai bản ghi trong một cuộc trò chuyện để tạo **"Slice" giữa chúng**, chọn **"Slice theo thời gian**" hoặc lưu các bộ lọc hiện tại của "Journal". Kiểm tra số lượng trước khi lưu. Mở lại "Slice" để áp dụng truy vấn đã lưu; Chức năng **"Hiển thị các bản ghi được thêm kể từ khi đánh dấu"** sẽ hiển thị các bản ghi được thêm sau đó.

Một khoảng thời gian được xác định theo thời gian quan sát của trình thu thập. Một khoảng thời gian theo ID tin nhắn có thể theo dõi các tin nhắn đã chọn khi có các thay đổi sau này. Ranh giới thời điểm tạo được lưu trữ cho phép người nhận so sánh lựa chọn ban đầu với trạng thái sau này của nó.

## Gán vai trò phù hợp cho từng đồng nghiệp

**Người kiểm duyệt** đọc bảng điều khiển; **Nhà phân tích** thêm thẻ và bình luận; **Người vận hành** cũng quản lý các bộ sưu tập và quyết định kiểm duyệt. Quyền truy cập vào không gian làm việc và cuộc trò chuyện áp dụng cho các thẻ, bối cảnh nguồn và các cuộc thảo luận. Sử dụng các quyền truy cập được đặt tên để xác định rõ nguồn gốc.

## Hoàn thiện công việc thành sản phẩm đầu ra

Xuất một phần dữ liệu dưới dạng JSON đã ký, hoặc sử dụng CSV cho bảng tính. Cài đặt báo cáo có thể bao gồm dấu trang và các phần dữ liệu, kèm theo bình luận của nhóm khi được chọn. Chọn các nội dung này trong [Report Studio](https://phishdestroy.github.io/TgWitness/vi/docs/reports/); một phần dữ liệu đã lưu không tự động cấu hình báo cáo. Đối với người nhận bị hạn chế, hãy sử dụng các [tùy chọn bàn giao](https://phishdestroy.github.io/TgWitness/vi/docs/handover/) riêng biệt.

Vui lòng tham khảo tài liệu [hướng dẫn](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-board/) về [Case Board](https://phishdestroy.github.io/TgWitness/vi/docs/reference/case-board/) để biết thêm thông tin về các bản sửa đổi đã ký, việc khớp chính xác các trích dẫn, xác minh lựa chọn và quyền truy cập.
