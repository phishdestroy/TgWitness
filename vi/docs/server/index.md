# Hãy duy trì hoạt động của nó

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/server/

Giữ máy thu thập luôn chạy và dữ liệu an toàn qua các lần khởi động lại.

## Vui lòng chọn phương thức triển khai

Cài đặt trực tiếp: [trình khởi chạy](https://phishdestroy.github.io/TgWitness/vi/docs/start/) cùng các mẫu dịch vụ trong [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker, từ thư mục dự án:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Bảng điều khiển lắng nghe trên localhost:8787. Mở nó cục bộ hoặc qua đường hầm SSH, với token từ lệnh thứ hai.

## Giữ nguyên toàn bộ thư mục dữ liệu

Cài đặt trực tiếp: `data/live`. Docker: volume `tgwitness-data`. Sổ nhật ký, phiên và khóa phải đi cùng nhau. Bản xuất có chữ ký là bằng chứng, không phải bản sao lưu.

1. Dừng thu thập trước.
2. Sao chép toàn bộ thư mục dữ liệu tới một nơi an toàn, ngoài máy chủ.
3. Thử khôi phục trên một bản cài riêng trước khi tin tưởng nó.

## Vui lòng kiểm tra lại sau khi khởi động lại

Kiểm tra không gian làm việc và khóa, kết nối, nguồn và xem tin nhắn mới có vào không. TgWitness bắt kịp những gì Telegram vẫn còn giữ, không phải mọi thứ đã xảy ra khi nó ngừng chạy.

Container "healthy" nghĩa là máy chủ web có phản hồi. Việc thu thập có chạy không thì tin nhắn thử và nhân chứng sẽ cho biết.

## Chỉ công bố những thông tin mà quý vị dự định công bố

HTTPS, volume, cập nhật và khôi phục có trong tài liệu triển khai. Những gì đã thực sự được kiểm thử: [hồ sơ kiểm định](https://phishdestroy.github.io/TgWitness/vi/docs/reference/verification/).
