# Telegram · Quản lý một nhóm tài khoản

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/groups/

Chạy nhiều tài khoản cùng nhau, mỗi tài khoản vẫn có bản ghi và khóa riêng.

Nhóm đặt trạng thái kết nối, bắt đầu/tạm dừng, cài đặt dùng chung và bản xuất trên một màn hình. Tiện khi nhiều tài khoản cùng làm một vụ việc.

## Mở tổng quan về nhóm

Mở nhóm trong **Tài khoản**. Mỗi tài khoản hiển thị trạng thái, tuyến, độ trễ và tin nhắn được lưu gần nhất. **Cần chú ý** liệt kê những cái đang lỗi, **Sửa** đưa bạn thẳng tới đó.

**Bắt đầu tất cả** / **Tạm dừng tất cả** sẽ hỏi trước khi thực hiện. **Cài đặt nhóm** được dùng chung, nhưng giá trị riêng của tài khoản vẫn giữ cho đến khi bạn thay.

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

1. **Thay đổi lộ trình nhóm**, chọn loại và cài đặt.
2. **Xem lại lựa chọn**: xem tài khoản nào thay đổi và tài khoản nào có tuyến riêng.
3. **Chuẩn bị và kiểm tra** thử một kết nối Telegram mới, cùng IP thoát nếu có thể.
4. **Áp dụng kết nối đã kiểm tra** và xem từng kết quả. Tài khoản đang chạy tiếp tục, tài khoản đang nghỉ vẫn nghỉ.

Độ trễ là thời gian thiết lập kết nối Telegram, IP thoát là IP mà tuyến hiển thị lúc kiểm tra. Kết quả có thể khác nhau giữa các tài khoản.

## Sử dụng quyền truy cập chồng chéo

**Trò chuyện mà nhiều tài khoản thấy** liệt kê các nguồn chung và phạm vi của chúng. Kênh và siêu nhóm có thể được nhiều tài khoản xuất cùng lúc bằng **Xuất với … tài khoản**. Trò chuyện riêng và nhóm thường thì không, vì số tin nhắn của chúng tính theo từng tài khoản.

## Xuất nhóm dưới dạng gói

**Xuất nhóm** cho một ZIP chứa bản xuất có chữ ký của mọi tài khoản và danh sách có chữ ký của chúng. Mỗi bản giữ dấu vân tay riêng để xác minh. Dòng thời gian gộp thì bạn vẫn phải tự dựng.

Tiếp theo: [báo cáo](https://phishdestroy.github.io/TgWitness/vi/docs/reports/), [Case Board](https://phishdestroy.github.io/TgWitness/vi/docs/case-board/), [xác minh bản xuất](https://phishdestroy.github.io/TgWitness/vi/docs/exports/).
