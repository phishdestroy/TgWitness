# Quản lý một nhóm tài khoản

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/groups/

Quản lý nhiều tài khoản thu thập cùng lúc đồng thời đảm bảo tính riêng biệt của các bản ghi và danh tính ký tên của từng tài khoản.

Nhóm tài khoản tập hợp trạng thái kết nối, các điều khiển quan sát, cài đặt chung và tính năng xuất dữ liệu vào một giao diện làm việc duy nhất. Tính năng này hữu ích khi nhiều tài khoản liên quan đến cùng một cuộc điều tra hoặc cần một cấu hình hoạt động nhất quán.

## Mở tổng quan về nhóm

Trong phần **Tài khoản**, hãy mở nhóm. Mỗi tài khoản hiển thị trạng thái quan sát, đường dẫn kết nối, độ trễ đường dẫn được đo gần nhất khi kiểm tra hiện tại thành công và tin nhắn được lưu gần nhất. Các liên kết **“Cần chú ý”** dẫn đến các tài khoản cần xử lý; **nút “Sửa”** mở không gian làm việc và bảng điều khiển liên quan.

**Các tùy chọn “Bắt đầu tất cả”** và **“Tạm dừng tất cả”** sẽ áp dụng cho các tài khoản đủ điều kiện sau khi xác nhận. **Cài đặt nhóm** chia sẻ các thiết lập đã chọn; các tài khoản có giá trị riêng sẽ giữ nguyên các thiết lập đó cho đến khi bạn quyết định thay thế chúng.

### Kiểm tra thay đổi lộ trình trong một nhóm

Ví dụ tổng hợp · các kiểm tra minh họa và kết quả

1. **Chọn.** Chọn nhóm và xem xét các tài khoản nào sẽ thay đổi.
2. **Chuẩn bị.** Giữ nguyên lộ trình riêng của tài khoản khi cần tách biệt.
3. **Kiểm tra.** Thử nghiệm kết nối được đề xuất và kiểm tra các kết quả đo lường.
4. **Áp dụng.** Kiểm tra lại trước khi lưu và xem xét kết quả cho từng tài khoản.

#### Nhóm điều tra

Trình thu thập kênh · Trình thu thập nhóm · Tài khoản tham chiếu

3 không gian làm việc riêng biệt

#### Danh sách đã được xem xét

2 tài khoản sẽ thực hiện theo lộ trình đề xuất.

Tài khoản tham chiếu duy trì lộ trình riêng của mình.

#### Kiểm tra chuẩn bị

Trình thu thập kênh: Thời gian truyền dữ liệu Telegram 84 ms

Trình thu thập nhóm: Thời gian truyền dữ liệu Telegram 91 ms

Các con số này là số liệu giả định dùng cho ví dụ.

#### Kết quả ứng dụng

Trình thu thập kênh: đã định tuyến bản lưu, tiếp tục quan sát.

Trình thu thập nhóm: kiểm tra lại không thành công, các cài đặt trước đó đã được khôi phục.

Tài khoản tham chiếu: giữ nguyên đường dẫn hiện tại.

## Thay đổi quy trình bằng cách thêm bước xem xét

1. Chọn **“Thay đổi lộ trình nhóm”**, sau đó chọn loại kết nối và cài đặt.
2. Chọn **tùy chọn “Review**”. Kiểm tra các tài khoản được liệt kê và các thiết lập đường dẫn tùy chỉnh riêng lẻ của từng tài khoản.
3. Chọn **“Chuẩn bị và kiểm tra**”. Quá trình kiểm tra sử dụng kênh truyền tải Telegram mới; các tuyến HTTP được hỗ trợ cũng báo cáo kết quả kiểm tra cổng ra HTTPS của chúng.
4. Chọn **“Áp dụng kết nối đã chọn”** và kiểm tra kết quả của từng tài khoản. Quá trình quan sát đang chạy trước đó sẽ tiếp tục từ điểm ứng dụng thành công; các tài khoản không hoạt động sẽ vẫn ở trạng thái không hoạt động.

Độ trễ mô tả quá trình thiết lập kết nối Telegram đã được đo lường. Kiểm tra địa chỉ IP đầu ra mô tả tuyến đường đó tại thời điểm kiểm tra được ghi lại. Tình trạng ủy quyền tài khoản và tình trạng hoạt động giám sát có các chỉ số riêng; việc thay đổi nhóm có thể dẫn đến các kết quả khác nhau tùy theo từng tài khoản.

## Sử dụng quyền truy cập chồng chéo

**Tính năng “Chats several accounts see”** hiển thị các nguồn được chia sẻ và phạm vi quan sát không gian làm việc hiện có. Các kênh và siêu nhóm đủ điều kiện có thể sử dụng **tính** **năng** **“Export with … accounts”** để chia nhỏ quá trình thu thập lịch sử của một cuộc trò chuyện. Các cuộc trò chuyện riêng tư và nhóm thông thường vẫn thuộc về tài khoản ban đầu vì số tin nhắn của chúng thuộc về lịch sử của tài khoản đó.

## Xuất nhóm dưới dạng gói

**Tính năng xuất nhóm** tạo ra một tệp ZIP chứa bản xuất đã được ký của từng tài khoản và danh sách các tệp đó cũng đã được ký. Danh tính và dấu vân tay của không gian làm việc gốc vẫn có sẵn để xác minh. Xây dựng một câu chuyện xuyên suốt các tài khoản bằng cách sử dụng các tham chiếu đó; một dòng thời gian hợp nhất duy nhất vẫn được lập riêng biệt.

Tiếp tục với [thiết kế báo cáo](https://phishdestroy.github.io/TgWitness/vi/docs/reports/), [Case Board trong không gian làm việc](https://phishdestroy.github.io/TgWitness/vi/docs/case-board/) hoặc [xuất dữ liệu để xác minh](https://phishdestroy.github.io/TgWitness/vi/docs/exports/).
