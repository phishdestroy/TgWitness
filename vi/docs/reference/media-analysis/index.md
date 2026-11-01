# Nhận dạng ký tự quang học (OCR) và chuyển đổi văn bản tại địa phương

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/media-analysis/

Nhận diện hình ảnh và âm thanh đã thu thập bằng một worker cục bộ; duy trì liên kết giữa văn bản được trích xuất và tệp nguồn tương ứng.

[Hướng dẫn quy trình làm việc](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Mở bản ghi nhật ký `media.saved`, chọn **“Nhận diện tệp đính kèm**”, sau đó chọn “OCR” hoặc “chuyển đổi văn bản” trong mục **“Yêu cầu từ kho lưu trữ**”. Quá trình xử lý được thực hiện thủ công và tại địa phương. Không có chế độ phương tiện đám mây hay tải lên tự động. Dữ liệu gốc của tệp đính kèm và bản ghi `media_sha256` vẫn giữ nguyên; văn bản được nhận diện được đánh dấu rõ ràng là kết quả nhận diện bằng máy và được lưu trữ riêng biệt cùng với mã băm nguồn, phiên bản công cụ/mô hình, ngôn ngữ, các tham số và thời gian hoàn thành. Bản chép lại vẫn giữ nguyên dấu thời gian được trả về.

Tìm kiếm các kết quả này bằng cách sử dụng **tính năng "Tìm kiếm văn bản được nhận diện**" và bộ lọc OCR/bản chép lại. Đây là một tìm kiếm dữ liệu phái sinh riêng biệt; nó không tự động chuyển đổi kết quả nhận diện bằng máy thành văn bản gốc của Telegram hoặc thêm nó vào các sự kiện đã được ký xác thực.

## Cài đặt worker tùy chọn

Phiên bản 1 yêu cầu máy chủ Linux có daemon Docker cục bộ. Đối với các hệ thống Windows, có thể chạy TgWitness trong môi trường máy ảo Linux (VM) hoặc WSL với daemon cục bộ riêng. Bảng điều khiển không bao giờ tự giải mã tệp đính kèm không đáng tin cậy.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

Đặt các biến này trong môi trường dịch vụ TgWitness và khởi động lại dịch vụ. Socket daemon mặc định là `/var/run/docker.sock`; các triển khai không cần quyền root có thể đặt là `TGWITNESS_DOCKER_SOCKET`. Worker sử dụng rõ ràng socket Unix đó thay vì một bối cảnh Docker từ xa. Không được tiết lộ API Docker cho người dùng bảng điều khiển hoặc gắn socket của nó vào bên trong container nhận dạng.

Để chuyển đổi văn bản, hãy cài đặt riêng một mô hình Whisper tương thích với CTranslate2, sau đó đặt `TGWITNESS_WHISPER_MODEL_DIR` thành thư mục chứa mô hình đó. Công cụ sẽ tải mô hình này bằng `local_files_only=True`; mô hình đã chọn và dữ liệu đầu vào sẽ được gắn ở chế độ chỉ đọc. Xem [tài liệu hướng dẫn tải mô hình](https://github.com/SYSTRAN/faster-whisper) của công cụ. Hình ảnh OCR được cung cấp bao gồm dữ liệu huấn luyện bằng tiếng Anh và tiếng Nga. Tích hợp thêm một ngôn ngữ khác vào hình ảnh của bạn khi cần thiết; mã ngôn ngữ tuân theo [CLI của Tesseract](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).

Không có mô hình nào được tải về trong quá trình xử lý. Quá trình xây dựng/tải xuống có thể sử dụng mạng; mỗi container nhận dạng thực tế đều bị vô hiệu hóa kết nối mạng. Hãy cài đặt hình ảnh trước khi kích hoạt nó; môi trường chạy sử dụng `--pull=never`.

## Giới hạn và khôi phục

Container chạy dưới quyền người dùng không có đặc quyền với quyền root chỉ đọc, các khả năng bị giới hạn, `no-new-privileges` , một CPU, 2 GiB bộ nhớ, giới hạn PID và hệ thống tệp tạm thời có giới hạn. Chỉ bản sao đã được xác minh của tệp đã chọn và thư mục mô hình tùy chọn mới được gắn vào. Cơ sở dữ liệu, kho lưu trữ và phiên làm việc của bộ thu thập không được gắn vào. Các [cờ thời gian chạy Docker](https://docs.docker.com/reference/cli/docker/container/run/) áp đặt các giới hạn này; đây vẫn là ranh giới của container, không phải là vùng an toàn phần cứng.

Các tệp được giới hạn ở 50 MiB, hình ảnh ở 20 triệu pixel, âm thanh ở 30 phút với thời lượng đã biết và thời gian xử lý là năm phút. Mỗi lần chỉ có một công nhân chạy, với tối đa 20 công việc đang xếp hàng/đang chạy và 100 công việc được lưu giữ cho mỗi không gian làm việc. Lệnh "Cancel" sẽ dừng container; lệnh "retry" sẽ tạo một tác vụ mới liên kết với lần thử trước đó. Các tác vụ bị gián đoạn sẽ được đánh dấu sau khi khởi động lại. Quá trình xử lý có thể thất bại khi mô hình không phù hợp với các giới hạn đã cấu hình; nó sẽ không chạy âm thầm mà không có sự cách ly.
