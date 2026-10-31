# Webhook đi

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/webhooks/

Gửi các sự kiện trong phạm vi đến các máy chủ nhận HTTPS kèm theo chữ ký HMAC, tính năng thử lại và trạng thái giao nhận.

**Phiên bản chính hiện tại:** sử dụng bản checkout từ kho nguồn; phiên bản xem trước di động 0.7.0 ra mắt trước khi tính năng này được triển khai.

[Hướng dẫn quy trình làm việc](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Mở **Tích hợp → Webhook đi** trong không gian làm việc đã chọn. Thêm một bộ thu HTTPS, chọn các sự kiện thu thập/phương tiện/xuất dữ liệu, và tùy chọn chọn các cuộc trò chuyện cho các quan sát mới và thay đổi. Văn bản tin nhắn bị tắt theo mặc định. Việc bật trích đoạn sẽ thêm tối đa 1.000 ký tự vào các sự kiện thay đổi tin nhắn; các trường Telegram thô và thông tin đăng nhập không bao giờ được gửi đi.

Sao chép khóa bí mật HMAC một lần vào cấu hình được bảo vệ của máy nhận. Khóa này được mã hóa trong kho lưu trữ của TgWitness và không thể truy xuất từ bảng điều khiển. Xóa và tạo lại đích đến để luân phiên sử dụng. **Gửi** một thử nghiệm không chứa nội dung trò chuyện đến hàng đợi**thử nghiệm tổng hợp**; làm mới trạng thái gửi để xem kết quả.

Chức năng gửi thông báo mở rộng vòng lặp thông báo hiện có cùng với Apprise. Nó sử dụng tuyến đường bên ngoài của không gian làm việc và các hạn chế về đích riêng tư hiện có. Không có cơ chế dự phòng trực tiếp hoặc chuyển hướng nào sau đó. Các URL không được chứa thông tin đăng nhập, chuỗi truy vấn hoặc đoạn URL; các địa chỉ riêng tư yêu cầu sự đồng ý ở cấp độ mạng máy chủ, không phải là cài đặt mà người dùng bảng điều khiển có thể bỏ qua.

## Dữ liệu và chữ ký

Cấu trúc: [`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json). Mỗi gói dữ liệu chứa `event_id`, `timestamp`, `workspace`, `type`, `synthetic` và các bộ đếm. Các sự kiện dựa trên nhật ký bao gồm thứ tự và giá trị băm của chúng. Việc hoàn tất xuất toàn bộ và các bài kiểm tra tổng hợp là các sự kiện giao nhận, không có tham chiếu nhật ký đã ký được tạo ra. Thông báo xóa trên Telegram và `missing_on_recheck` vẫn là các loại riêng biệt.

Tiêu đề `X-TgWitness-Signature` là `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`. Tính toán HMAC trên các byte chính xác `timestamp + "." + raw_request_body`, sử dụng khóa bí mật được hiển thị dưới dạng byte UTF-8. So sánh chữ ký trong thời gian hằng số trước khi phân tích hoặc thực hiện thao tác trên nội dung. Từ chối các dấu thời gian cách xa hơn năm phút so với đồng hồ của bạn. Dấu thời gian được làm mới ở mỗi lần cố gắng gửi.

Sử dụng `event_id` làm khóa idempotency trong bộ nhớ bền vững, kèm theo ràng buộc duy nhất nguyên tử trước khi xảy ra tác dụng phụ. Một chữ ký hợp lệ đơn thuần không ngăn chặn được việc một yêu cầu gần đây bị tái phát. Giữ lại các ID đã xử lý ít nhất trong toàn bộ khoảng thời gian thử lại; lưu giữ chúng lâu hơn nếu người nhận có thể xử lý lại các sự kiện đã lưu trữ.

## Thử lại

Việc gửi dữ liệu được xếp hàng bền vững trước các yêu cầu HTTP. Chúng sử dụng ngữ nghĩa "ít nhất một lần" : việc mất xác nhận hoặc khởi động lại có thể gửi lại một sự kiện với cùng một ID. Có tám lần thử với thời gian chờ theo cấp số nhân, bắt đầu từ 15 giây và giới hạn tối đa là một giờ. Để thành công, cần có phản hồi 2xx. Các tác vụ đã hết hạn sẽ để lại một lỗi hiển thị; việc gửi không được đảm bảo sau khi kết thúc các lần thử lại.

Hàng đợi chứa 1.000 lần gửi. Khi đầy, quá trình quét các sự kiện trong nhật ký sẽ tạm dừng và tiếp tục sau khi có dung lượng trống. Việc hoàn tất xuất toàn bộ dữ liệu mà không thể xếp vào hàng đợi sẽ hiển thị lỗi hàng đợi. Mỗi lần thông báo sẽ thực hiện tối đa năm lần gửi và 100 bản ghi thử gửi gần nhất sẽ được lưu giữ. Việc xóa một đích đến cũng sẽ xóa các bản gửi đang chờ xử lý của đích đó.

## Ví dụ về n8n

Nhập [quy trình làm việc mẫu](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json). Quy trình này hiện không hoạt động và không chứa thông tin bí mật hay các hành động tiếp theo. Đặt `TGWITNESS_WEBHOOK_SECRET` trong môi trường n8n worker, cho phép truy cập vào môi trường đó và cho phép hàm tích hợp `crypto` cho nút Code. Ví dụ này sử dụng tùy chọn raw-body của nút Webhook, kiểm tra chữ ký/độ mới và xác nhận các sự kiện đã được xác thực. Điều này phù hợp với [cách triển khai được ghi trong tài liệu](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts) của nút.

Trước khi thêm các lệnh ghi hoặc thông báo SIEM, hãy thêm bộ lưu trữ bền vững và idempotent được mã hóa bằng khóa `event_id`. Hạn chế việc chỉnh sửa quy trình làm việc n8n và thời gian lưu trữ nhật ký thực thi theo dữ liệu mà bạn đã chọn để gửi. TgWitness không thêm bất kỳ lệnh nào từ bên ngoài.
