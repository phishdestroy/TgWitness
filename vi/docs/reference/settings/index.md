# Cài đặt ban đầu và cấu hình

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/settings/

Trình hướng dẫn thiết lập, mục tiêu, cấp độ giao diện, đường dẫn kết nối và các cài đặt được chia sẻ bởi một nhóm tài khoản.

[Tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/) · [Kết nối](https://phishdestroy.github.io/TgWitness/vi/docs/reference/connection/) · [Truy cập](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/)

Một không gian làm việc mới sẽ mở ra `/first-run`: ngôn ngữ và múi giờ, mức độ giao diện, mục tiêu, kết nối, Telegram và các cuộc trò chuyện. Mỗi câu trả lời được lưu trên máy chủ ngay khi có thay đổi, do đó việc tải lại trang sẽ tiếp tục từ bước đó. Màn hình cuối cùng liệt kê các câu trả lời và cho phép bạn quay lại bất kỳ câu trả lời nào trong số đó.

Ngôn ngữ, múi giờ IANA, chủ đề và mức độ được lưu trữ theo từng người vận hành và từng không gian làm việc. Các giá trị mặc định là ngôn ngữ trình duyệt, múi giờ thiết bị, chủ đề hệ thống và giao diện đơn giản. Việc thay đổi ngôn ngữ sẽ giữ nguyên phiên làm việc trên bảng điều khiển. Thời gian trong nhật ký đã ký kết không bao giờ thay đổi.

`/settings` chỉnh sửa cùng các bản ghi với trình hướng dẫn. Tính năng tìm kiếm bao gồm các trường chính, tham số và các biểu mẫu mở rộng; một trường ẩn có thể được mở mà không cần thay đổi cấp độ. Cấp độ chỉ thay đổi những gì được hiển thị: máy chủ tự động kiểm tra quyền truy cập. Cài đặt bộ sưu tập và kết nối đầu tiên thuộc về quản trị viên không gian làm việc.

| Cấp độ | Các trường | Thanh bên |
| --- | --- | --- |
| Đơn giản | Chỉ những yếu tố cần thiết | Trang chủ, Cuộc trò chuyện, Thay đổi, Lưu trữ, Cài đặt |
| Tiêu chuẩn | Các cài đặt chung kèm theo giải thích | Thêm Case Board, Tài khoản và Quyền truy cập |
| Chuyên gia | Tất cả các trường, giới hạn và chi tiết kỹ thuật | Thêm các mục: Nguồn, Tiện ích bổ sung, Hỏi kho lưu trữ, Thông số, Tài khoản, Nhật ký hệ thống và Tích hợp |

[Hướng dẫn bảng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/panel/) điều khiển mô tả từng phần.

## Mục tiêu

| Mục tiêu | Bộ sưu tập | Tệp tin | Các dịch vụ bên ngoài | Địa chỉ máy chủ |
| --- | --- | --- | --- | --- |
| Bản sao lưu trữ | Tắt; **Bắt đầu** thực hiện xuất dữ liệu | Ảnh có dung lượng tối đa 20 MB | Tắt | Tự động |
| Theo dõi các cuộc trò chuyện | Liên tục | Ảnh và video có thời lượng tối đa 60 giây / dung lượng tối đa 20 MB | Dấu thời gian và thông báo sự cố | Tự động |
| Bằng chứng | Liên tục | Tất cả các tệp có dung lượng tối đa 1 GB | Dấu thời gian, drand, thông báo | Không, ẩn đi |

Bản sao ngoài nền tảng, bot chứng thực và tính năng kiểm tra mã được khuyến nghị để làm bằng chứng. Địa chỉ lưu trữ và thông báo cần có đích đến trước tiên. Một tính năng kết nối với dịch vụ bên ngoài sẽ yêu cầu cho phép các yêu cầu bên ngoài Telegram; việc tắt tính năng này sẽ đồng thời tắt các dấu thời gian, thông báo và bản sao ngoài nền tảng.

Việc thay đổi mục tiêu sẽ hiển thị sự khác biệt trước tiên, và các thay đổi thủ công có thể được giữ lại. Một trường khác với mục tiêu sẽ được đánh dấu **là “Đã được bạn thay đổi”** và có thể được khôi phục. Bản sửa đổi cài đặt ngăn không cho sự khác biệt đã được xem xét ghi đè lên một thay đổi được thực hiện trong một tab khác.

## Kết nối

**Automatic** sẽ thử các máy chủ công khai MTProxy trước, sau đó là WARP, rồi đến kết nối trực tiếp, phương án cuối cùng chỉ được sử dụng khi địa chỉ máy chủ có thể được hiển thị. Automatic và WARP có thể cài đặt các thành phần đã được kiểm tra băm và đăng ký máy chủ với Cloudflare. WARP sử dụng trình quản lý wgcf/wireproxy hiện có và cổng SOCKS5 cục bộ; bảng định tuyến hệ thống không bị thay đổi. Khi cần sử dụng các dịch vụ bên ngoài, Automatic ưu tiên WARP hơn MTProxy.

Proxy của riêng bạn chấp nhận `tg://proxy`, `socks5://`, `http://` và `https://`. Chứng chỉ của một proxy HTTPS sẽ được kiểm tra trước khi thông tin đăng nhập được gửi đến nó.

Kiểm tra kết nối có hiệu lực trong năm phút và gắn liền với lộ trình, chính sách và các câu trả lời trong trình hướng dẫn; việc thay đổi bất kỳ yếu tố nào trong số đó đều yêu cầu kiểm tra lại. Tùy chọn **“Tiếp tục mà không kiểm tra”** có sẵn nhưng không thay thế cho việc đăng nhập Telegram. Lộ trình đã chọn sẽ được kiểm tra lại ở chế độ nền, và chế độ Tự động sẽ chạy lại chuỗi của nó sau khi mất kết nối. Khi không có proxy công khai nào phản hồi, chỉ số sẽ chuyển sang màu đỏ kèm theo các hành động WARP và kiểm tra lại .

## Nhóm tài khoản

Các tài khoản trong một nhóm sẽ chia sẻ cài đặt với nhau. Mở **Tài khoản → Nhóm và cài đặt chung → Cài đặt chung**, hoặc **Cài đặt nhóm** trên trang Cài đặt của tài khoản.

Nhóm chia sẻ mục tiêu, tệp đã lưu, dấu thời gian, drand, thông báo sự cố, bản sao ngoài nền tảng, yêu cầu bên ngoài Telegram, chế độ IP, nội dung cần ghi lại, lịch trình kiểm tra lại, quy tắc thông báo, cài đặt báo cáo, tham số và đường dẫn kết nối. Địa chỉ nhận thông báo, thông tin đăng nhập proxy và thông tin đăng nhập được lưu riêng cho từng tài khoản, cũng như việc bắt đầu và tạm dừng quá trình thu thập dữ liệu.

- Mọi thành viên đều theo dõi nhóm. Cài đặt cho phép chọn giá trị 🔗 **Từ nhóm** hoặc ✏️ **Giá trị riêng**; **Chọn “Quay lại giá trị của nhóm”** để khôi phục giá trị ban đầu.
- Một thay đổi sẽ liệt kê các tài khoản mà nó ảnh hưởng (**Áp dụng cho 2 trong số 3 tài khoản**) và hỏi từng tài khoản trước khi thay thế giá trị hiện tại của tài khoản đó. Các tài khoản chưa được chọn sẽ giữ nguyên giá trị của mình.
- Một tham số mà nhóm không chia sẻ sẽ vẫn ở trạng thái **"Chưa chia sẻ": mỗi tài khoản sẽ giữ giá trị riêng của mình** cho đến khi bạn nhấn **"Chia sẻ giá trị này**".
- **Việc sao chép cài đặt từ một tài khoản** sẽ lấy các giá trị của tài khoản được chọn làm cài đặt chung cho nhóm.
- Khi một tài khoản được chuyển vào nhóm, hệ thống sẽ hỏi: **“Có muốn áp dụng các giá trị của nhóm không?”.** Nếu không, tài khoản đó sẽ giữ nguyên các giá trị của riêng mình, được đánh dấu bằng ✏️. Các tài khoản được thêm vào sau đó sẽ bắt đầu với các giá trị của nhóm.
- Một tài khoản quan sát sẽ duy trì chế độ IP của mình cho đến khi bị tạm dừng.

Mỗi thay đổi đều được ghi lại trong nhật ký đã được ký số của không gian làm việc chính và của mọi thành viên mà thay đổi đó ảnh hưởng đến. Việc xóa một nhóm sẽ giữ lại các tài khoản trong nhóm và các giá trị hiện tại của chúng.

Trang nhóm `/groups/<id>` hiển thị danh sách thành viên, những nội dung cần chú ý và các cuộc trò chuyện mà nhiều tài khoản cùng theo dõi. Xem [phần Nhóm tài khoản](https://phishdestroy.github.io/TgWitness/vi/docs/reference/accounts/#bulk-import-and-account-groups).

## Các không gian làm việc hiện có

Một không gian làm việc có phiên làm việc hoặc đã được thiết lập trước đó sẽ không hiển thị trình hướng dẫn. Các giá trị của nó sẽ không bị thay thế bởi mục tiêu khi trang được tải. Việc ẩn một trường không tắt tính năng này hoặc xóa giá trị của nó.

Ước tính về dung lượng và thời gian dựa trên tối đa ba cuộc trò chuyện được chọn và tối đa 20 tin nhắn từ mỗi cuộc trò chuyện. Đây chỉ là ước tính: nó không dự đoán các giới hạn của Telegram, tốc độ của một máy chủ cụ thể hoặc các tệp trong mỗi cuộc trò chuyện.

```
python tools/test_settings_hub.py
python tools/test_group_settings.py
python tools/check_group_settings_browser.py
python tools/check_first_run.py
```
