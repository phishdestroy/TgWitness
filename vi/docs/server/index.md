# Hãy duy trì hoạt động của nó

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/server/

Đảm bảo công cụ thu thập dữ liệu luôn sẵn sàng hoạt động và dữ liệu của nó được giữ nguyên vẹn sau mỗi lần khởi động lại.

## Vui lòng chọn phương thức triển khai

Đối với việc cài đặt bản gốc, vui lòng sử dụng trình [khởi chạy](https://phishdestroy.github.io/TgWitness/vi/docs/start/) và các ví dụ về dịch vụ trong [thư mục `deploy/`.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Đối với Docker, hãy cài đặt Docker cùng với Compose và chạy từ thư mục dự án:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Bảng điều khiển mặc định lắng nghe tại địa chỉ loopback của máy chủ, cổng 8787. Quý vị có thể mở bảng điều khiển này tại máy cục bộ hoặc thông qua đường hầm SSH. Vui lòng sử dụng mã thông báo từ lệnh thứ hai để mở khóa bảng điều khiển.

## Giữ nguyên toàn bộ thư mục dữ liệu

Các bản cài đặt gốc sử dụng `data/live`. Docker sử dụng khối lượng lưu trữ liên tục `tgwitness-data`. Hãy lưu trữ nhật ký, phiên tài khoản, khóa và trạng thái hoạt động cùng nhau. Bản xuất có chữ ký là bằng chứng hữu ích, nhưng nó không phải là bản sao lưu cài đặt đầy đủ.

1. Vui lòng dừng quá trình thu thập dữ liệu trước khi thực hiện sao lưu đầy đủ.
2. Sao chép toàn bộ thư mục dữ liệu riêng tư vào bộ nhớ được bảo vệ bên ngoài máy chủ.
3. Hãy thử khôi phục dữ liệu trên một môi trường cài đặt độc lập trước khi dựa vào bản sao lưu.

## Vui lòng kiểm tra lại sau khi khởi động lại

Xác nhận không gian làm việc và khóa dự kiến, kết nối Telegram, các nguồn đã chọn và tính năng thu thập tin nhắn mới. Trạng thái MTProto đã lưu và tính năng đồng bộ hóa giúp khôi phục các bản cập nhật mà Telegram vẫn còn lưu giữ. Công cụ này không thể tái tạo mọi bản cập nhật đã hết hạn hoặc các thao tác chỉnh sửa bị xóa trước khi được thu thập.

Tình trạng hoạt động của container có nghĩa là máy chủ web đang phản hồi. Vui lòng sử dụng tin nhắn kiểm soát và kiểm tra chứng thực để đánh giá quá trình thu thập dữ liệu cũng như việc công bố ra bên ngoài.

## Chỉ công bố những thông tin mà quý vị dự định công bố

Tài liệu tham khảo triển khai bao gồm các ví dụ về HTTPS, lệnh quản lý khối lượng lưu trữ bền vững (persistent-volume), các bước cập nhật và khôi phục. Các lệnh Docker được cung cấp để triển khai; bản [ghi xác thực](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/) hiện tại nêu rõ các môi trường đã được kiểm thử thực tế.
