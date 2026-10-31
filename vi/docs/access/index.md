# Chia sẻ một trường hợp

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/access/

Hãy chia sẻ những trường hợp mà người khác cần. Đồng thời, hãy giữ quyền kiểm soát đối với phần còn lại.

01**Chọn bằng chứng**

Quý vị có thể chọn toàn bộ không gian làm việc của tài khoản hoặc các cuộc trò chuyện riêng lẻ đã được ghi lại.

02**Chọn các hành động**

Cho phép xem, xuất dữ liệu hoặc cấp các quyền truy cập cụ thể mà người dùng cần.

03**Đặt các giới hạn**

Phát hành mã thông báo cá nhân có thời hạn hiệu lực, giới hạn phiên và các hạn chế về địa chỉ IP (tùy chọn).

Phạm vi thu thập quyết định những nội dung nào sẽ được ghi lại. Phạm vi truy cập quyết định những gì một người có thể xem và thực hiện.

## Cấp quyền truy cập cho ai đó

1. Vui lòng đăng nhập với tư cách quản trị viên và mở **mục Truy cập**.
2. Hãy nêu tên quyền truy cập và chọn các không gian làm việc cũng như các cuộc trò chuyện.
3. Giữ lại **tùy chọn “Xem”** dành cho người đánh giá. Thêm tùy chọn **“Xuất”** trong trường hợp họ cần tải xuống các bản ghi.
4. Vui lòng thiết lập các giới hạn, sau đó nhấn vào nút **“Tạo quyền truy cập**”.
5. Vui lòng sao chép mã thông báo được hiển thị một lần duy nhất. Gửi mã này một cách riêng tư kèm theo địa chỉ bảng điều khiển.
6. Vui lòng kiểm tra chế độ xem được phép trong một phiên trình duyệt riêng biệt trước khi chuyển giao.

## Hãy bắt đầu từ nhiệm vụ mà họ cần thực hiện

| Người | Truy cập | Kết quả |
| --- | --- | --- |
| Người đánh giá | Các cuộc trò chuyện được chọn lọc; chỉ xem | Quý vị có thể đọc nội dung cuộc trò chuyện đã được ghi lại mà không làm thay đổi dữ liệu thu thập. |
| Chuyên viên phân tích | Các cuộc trò chuyện được chọn lọc; xem và xuất | Xem xét và tải xuống các bản ghi cần thiết cho vụ việc. |
| Người vận hành | Các không gian làm việc được chọn lọc; nguồn và bộ sưu tập | Quản lý các nội dung được theo dõi và khởi động hoặc dừng các trình thu thập dữ liệu. |

Đây là các cấu hình do quý vị lựa chọn, không phải các vai trò cố định. Cài đặt chung cho toàn tài khoản và tính năng xuất toàn bộ nhật ký vẫn bị giới hạn ở mức truy cập theo từng cuộc trò chuyện, ngay cả khi một quyền khác đã được kích hoạt. Quyền truy cập toàn bộ không gian làm việc bao gồm cả các tài khoản trong tương lai.

## Quý vị có thể thay đổi quyết định bất cứ lúc nào

Quý vị có thể chỉnh sửa quyền truy cập để điều chỉnh các thao tác mà các yêu cầu tiếp theo có thể thực hiện. Kết thúc một phiên làm việc hoặc thu hồi toàn bộ quyền truy cập để chấm dứt tất cả các phiên đang hoạt động. Các tệp đã được tải xuống không thể thu hồi lại. Việc kết thúc một phiên làm việc trên bảng điều khiển sẽ không làm ngừng quá trình thu thập dữ liệu.

**Giới hạn phiên và địa chỉ IP**

Hạn chế số phiên làm việc song song và số lần đăng nhập thành công, đặt ngày kết thúc tuyệt đối, cho phép các địa chỉ IP hoặc mạng con, hoặc ràng buộc quyền truy cập với địa chỉ đăng nhập lần đầu tiên. Thời hạn phiên được tính dựa trên thời gian không hoạt động; việc tải trang trên một bảng điều khiển đang mở được tính là hoạt động. Kiểm tra địa chỉ máy khách được ứng dụng hiển thị khi ứng dụng chạy qua proxy hoặc đường hầm.

**Khóa chính và nhật ký hoạt động**

Quản trị viên giữ mã thông báo (token) của bảng điều khiển chính. Quyền truy cập được cấp không thể quản lý quyền truy cập của người khác hoặc mở bảng điều khiển quản trị viên. Bảng điều khiển hiển thị hoạt động của quy trình hiện tại trên các không gian làm việc; các bản ghi truy cập có chữ ký lưu giữ các sự kiện cấp quyền và phiên làm việc mà không cần mã thông báo. Các không gian làm việc chia sẻ quy trình máy chủ và không cách ly dữ liệu khỏi quản trị viên máy chủ.

Vui lòng tham khảo tài liệu [tham chiếu đầy đủ](https://phishdestroy.github.io/TgWitness/vi/docs/reference/access/) về tất cả bảy quyền truy cập, các quy tắc phiên làm việc và phạm vi quyền hạn của quản trị viên.
