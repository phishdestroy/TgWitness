# Phân tích kho lưu trữ

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/analysis/

Tìm kiếm các tin nhắn đã lưu, xem lại các đầu vào từ AI và lưu giữ các báo cáo phân tích kèm theo nguồn tham khảo.

**Phiên bản chính hiện tại:** sử dụng bản checkout từ kho nguồn; phiên bản xem trước di động 0.7.0 ra mắt trước khi tính năng này được triển khai.

[Hướng dẫn quy trình làm việc](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Dùng **Sổ nhật ký** để tìm kiếm cục bộ mà không cần AI. Để dùng **Hỏi kho lưu trữ**, trước tiên hãy bật và cấu hình một nhà cung cấp trong **Tích hợp**. Trình chọn không gian làm việc dùng để chọn tài khoản; biểu mẫu dùng để chọn các cuộc trò chuyện và khoảng thời gian quan sát. Việc truy xuất được thực hiện cục bộ. Một cụm từ chính xác hoặc tên miền sẽ thu hẹp phạm vi truy xuất; ID tin nhắn sẽ yêu cầu các phiên bản đã lưu. Hãy xem lại các đoạn trích và mở bản ghi nhật ký hoặc ngữ cảnh của chúng. Không có cơ sở dữ liệu vectơ hay hành động tự động nào trên Telegram.

## Nhà cung cấp và sự đồng ý

Tính năng AI được tắt mặc định trong mọi không gian làm việc. Chỉ quản trị viên chính mới có thể cấu hình mô hình, điểm cuối, khóa API được mã hóa, giới hạn bối cảnh/đầu ra, thời gian chờ và hạn mức yêu cầu hàng ngày. Khóa API sẽ không bao giờ được gửi trở lại trình duyệt. Để giữ nguyên khóa hiện tại, hãy để trống trường khóa hoặc xóa nó một cách rõ ràng.

Ollama sử dụng [điểm cuối `/api/chat`](https://docs.ollama.com/api/chat) đã được ghi chép với đầu ra JSON không theo luồng. Địa chỉ mặc định của nó là `http://127.0.0.1:11434` trên máy chủ TgWitness. Người vận hành có thể thay đổi địa chỉ này bằng cách sử dụng `TGWITNESS_AI_LOCAL_ENDPOINT`; đây không phải là địa chỉ do mô hình kiểm soát. Hãy tự cài đặt mô hình đã chọn. TgWitness không tự động tải xuống mô hình này.

Nhà cung cấp tương thích phải có URL cơ sở kết thúc bằng `/v1` và hỗ trợ [giao thức Chat Completions](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages` (chế độ phản hồi JSON), `max_completion_tokens` và `choices[0].message.content`. Các dịch vụ thiếu các trường này sẽ không được hỗ trợ. Việc kiểm tra kết nối sẽ gửi văn bản tổng hợp và được tính vào hạn mức yêu cầu.

Mỗi yêu cầu đều sử dụng tuyến đường bên ngoài đã được cấu hình trong không gian làm việc. Tuyến đường bị chặn hoặc MTProxy chỉ dành cho Telegram sẽ gây ra lỗi; không có cơ chế thử lại trực tiếp. Một địa chỉ Ollama cục bộ được cấu hình có chủ đích cho phép đích đến riêng tư, trong khi vẫn sử dụng tuyến đường đã chọn. Đối với các dịch vụ riêng tư khác, tùy chọn tham gia đích đến riêng tư ở cấp máy chủ hiện có sẽ được áp dụng. Bảng điều khiển hiển thị điểm cuối thực tế đã được cấu hình.

Trước khi tạo, **dữ liệu được gửi đến mô hình** hiển thị yêu cầu: câu hỏi, các đoạn trích đã được kiểm tra, loại sự kiện, thời gian quan sát và các dấu hiệu phạm vi. Các phiên Telegram, các trường dữ liệu thô, khóa nhà cung cấp, byte tệp đính kèm và nhật ký đầy đủ không thuộc bối cảnh đó. Hủy chọn các nguồn không mong muốn, sau đó chấp thuận rõ ràng việc xử lý. Các nhà cung cấp bên ngoài có thể lưu giữ nội dung được gửi theo chính sách riêng của họ. Thực thi cục bộ có nghĩa là điểm cuối nằm tại địa phương; điều này không đảm bảo hành vi của một dịch vụ được cấu hình độc lập.

Tối đa có hai yêu cầu đồng thời từ nhà cung cấp trên toàn cầu và một yêu cầu cho mỗi không gian làm việc. Bản xem trước hết hạn sau mười phút và chỉ có thể tạo ra một kết quả. Số lượng token được báo cáo của nhà cung cấp sẽ được hiển thị; ước tính chi phí chỉ xuất hiện khi cả biểu giá đầu vào và đầu ra đã được cấu hình. Các lần thử không thành công cũng tiêu tốn ngân sách yêu cầu hàng ngày. Các lần thử lại tự động không tiêu tốn thêm ngân sách.

## Nguồn và giới hạn

Chức năng truy xuất kiểm tra văn bản tin nhắn đã lưu bằng tìm kiếm từ vựng có giới hạn. Chức năng này trả về tối đa 24 nguồn và đánh dấu các đoạn trích bị cắt ngắn hoặc các tập kết quả không đầy đủ. Khoảng thời gian này đề cập đến **thời gian quan sát**, không phải là tuyên bố rằng lịch sử Telegram là hoàn chỉnh. Các sự kiện có phạm vi trên toàn không gian làm việc sẽ không được hiển thị khi truy cập trong phạm vi trò chuyện. Dữ liệu thiếu được mô tả là không tìm thấy trong kho lưu trữ hiện có.

Mô hình không nhận bất kỳ công cụ nào. Các ID nguồn của nó được đối chiếu với các bản ghi đã chọn, các giá trị băm được kiểm tra lại, và các chuỗi trích dẫn phải xuất hiện trong các bản ghi đó. Các ID không xác định, trích dẫn bị thay đổi và các tuyên bố không có nguồn dẫn sẽ khiến câu trả lời bị từ chối. Ứng dụng tạo ra các liên kết; các URL do mô hình tạo ra không được sử dụng làm nguồn trích dẫn. Các kiểm tra này xác định sự tồn tại của nguồn và độ chính xác của trích dẫn, chứ không phải tính đúng đắn của một suy luận. Hãy kiểm tra lại các suy luận so với các bản ghi trước khi dựa vào chúng.

## Báo cáo

Lưu câu trả lời đã được xem xét dưới dạng một báo cáo phân tích riêng biệt. Báo cáo này bao gồm tóm tắt mô hình, thứ tự thời gian quan sát được, các liên kết và handle được trích xuất, bản ghi chỉnh sửa/xóa, giới hạn phạm vi bao phủ và các giá trị băm sự kiện nguồn. Thông tin về nhà cung cấp, mô hình, điểm cuối, thời gian và phiên bản mẫu lời nhắc cũng được kèm theo. Không có thông tin nhận dạng nào được tự động hợp nhất.

Các bản sửa đổi và ghi chú của nhà phân tích được lưu trữ riêng biệt với bản tóm tắt của mô hình. Các báo cáo được lưu trữ trong các tệp phái sinh được mã hóa, với chỉ mục nằm ngoài luồng sự kiện đã ký; các sự kiện và phương tiện gốc không bị thay đổi. Chỉ chủ sở hữu hoặc quản trị viên mới có thể mở báo cáo, và quyền truy cập nguồn sẽ được kiểm tra lại. Việc tải xuống cũng yêu cầu quyền xuất dữ liệu. Phiên bản 1 không ký số các báo cáo cũng như không ngụ ý rằng các kết luận của mô hình là bằng chứng đã được xác minh. Giới hạn: 100 báo cáo cho mỗi không gian làm việc và 100 bản sửa đổi của nhà phân tích cho mỗi báo cáo.

Để biết thêm về OCR thủ công và bản chép lời, xem [phần xử lý phương tiện truyền thông](https://phishdestroy.github.io/TgWitness/vi/docs/reference/media-analysis/). Để biết thêm về quyền truy cập của khách hàng, xem [MCP](https://phishdestroy.github.io/TgWitness/vi/docs/reference/mcp/).
