# Dấu thời gian

Canonical page: https://phishdestroy.github.io/TgWitness/vi/docs/reference/timestamp/

Dấu thời gian theo tiêu chuẩn RFC 3161 cho các điểm kiểm tra có chữ ký: những thông tin nào được gửi đến cơ quan có thẩm quyền và cách thức xác minh phản hồi.

TgWitness chuẩn bị các yêu cầu theo tiêu chuẩn RFC 3161 và xác minh các phản hồi từ Cơ quan Chứng thực Dấu thời gian (TSA). Quy trình thủ công này không thực hiện việc lựa chọn TSA cũng như không gửi dữ liệu; chế độ bằng chứng sẽ thực hiện cả hai tác vụ này theo lịch trình ([định dạng bằng chứng](https://phishdestroy.github.io/TgWitness/vi/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)). Một yêu cầu đã được chuẩn bị **vẫn chưa** phải **là bằng chứng dấu thời gian**.

## Những gì bằng chứng này ghi nhận

Sơ đồ quy trình · Nhận định về tài khoản → Chuỗi SHA-256 và chữ ký Ed25519; Chuỗi SHA-256 và chữ ký Ed25519 → Điểm kiểm tra có chữ ký; Điểm kiểm tra có chữ ký → Hàm băm chính xác đến từng byte và giá trị ngẫu nhiên (nonce); Hàm băm chính xác đến từng byte và giá trị ngẫu nhiên (nonce) → Yêu cầu theo RFC 3161; Yêu cầu theo RFC 3161 → TSA độc lập; TSA độc lập → Phản hồi có chữ ký của TSA; Điểm kiểm tra có chữ ký → Xác minh dữ liệu, mã ngẫu nhiên (nonce) và sự tin cậy rõ ràng đối với CA; Phản hồi có chữ ký của TSA → Xác minh dữ liệu, mã ngẫu nhiên (nonce) và sự tin cậy rõ ràng đối với CA · Nhận định về tài khoản · Chuỗi SHA-256 và chữký Ed25519 · Điểm kiểm tra có chữký · Hàm băm chính xác đếntừng byte và giá trịngẫu nhiên (nonce) · Yêu cầu theo RFC 3161 · TSA độc lập · Phản hồi có chữ ký củaTSA · Xác minh dữ liệu, mãngẫu nhiên (nonce) vàsự tin cậy rõ ràng đốivới CA

**Sơ đồ dưới dạng văn bản**

1. Nhận định về tài khoản → Chuỗi SHA-256 và chữ ký Ed25519
2. Chuỗi SHA-256 và chữ ký Ed25519 → Điểm kiểm tra có chữ ký
3. Điểm kiểm tra có chữ ký → Hàm băm chính xác đến từng byte và giá trị ngẫu nhiên (nonce)
4. Hàm băm chính xác đến từng byte và giá trị ngẫu nhiên (nonce) → Yêu cầu theo RFC 3161
5. Yêu cầu theo RFC 3161 → TSA độc lập
6. TSA độc lập → Phản hồi có chữ ký của TSA
7. Điểm kiểm tra có chữ ký → Xác minh dữ liệu, mã ngẫu nhiên (nonce) và sự tin cậy rõ ràng đối với CA
8. Phản hồi có chữ ký của TSA → Xác minh dữ liệu, mã ngẫu nhiên (nonce) và sự tin cậy rõ ràng đối với CA

Chữ ký của bộ thu thập sẽ liên kết các bản ghi với khóa của nó. Một phản hồi đáng tin cậy từ TSA có thể xác nhận rằng một trạm kiểm tra cụ thể đã tồn tại vào thời điểm mà TSA đã công bố. Sau đó, trạm kiểm tra này có thể liên kết tiền tố của sổ nhật ký. Điều này không xác định thời điểm diễn ra mỗi hành động trên Telegram cũng như tính xác thực của nội dung được ghi lại.

## Quy trình

1. Lưu giữ dấu vân tay khóa của bộ thu thập thông qua một kênh đáng tin cậy riêng biệt. Một khóa chỉ được cung cấp bởi tệp ZIP đang được kiểm tra là không đủ để xác định bộ thu thập.
2. Trong **phần Xuất → Chuẩn bị yêu cầu dấu thời gian**, hãy tải xuống tệp ZIP yêu cầu của không gian làm việc đã chọn. Giải nén các tệp `checkpoint.json`, `timestamp.tsq`, `SHA256SUMS` và `README.txt`. Không được thay đổi các byte điểm kiểm tra.
3. Vui lòng chọn TSA phù hợp với cuộc điều tra. Gửi yêu cầu `timestamp.tsq` theo phương pháp đã được ghi chép, kèm theo `application/timestamp-query` cho dịch vụ HTTP. Lưu phản hồi nhị phân gốc dưới dạng `timestamp.tsr`, cùng với điểm cuối, thời gian truy xuất và kết quả yêu cầu. Yêu cầu này chứa mã băm và giá trị ngẫu nhiên (nonce) thay vì nội dung tin nhắn; dữ liệu siêu dữ liệu mạng vẫn tiết lộ thông tin về yêu cầu.
4. Hãy lấy chứng chỉ gốc đáng tin cậy một cách độc lập với nội dung phản hồi, cùng với bất kỳ chứng chỉ trung gian nào cần thiết. Một chứng chỉ có trong phản hồi sẽ không tự động trở thành chứng chỉ đáng tin cậy chỉ vì nó được bao gồm trong đó.
5. Từ một bản cài đặt TgWitness đáng tin cậy, hãy xác minh:

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

Vui lòng thêm `--intermediates tsa-intermediates.pem` hoặc `--openssl /path/to/openssl` nếu cần thiết. OpenSSL phải hỗ trợ `ts`. Trên hệ điều hành Windows, trình xác minh cũng sẽ tìm kiếm trong bản cài đặt Git tiêu chuẩn. OpenSSL phiên bản 3.5.9 đã được thử nghiệm tại địa phương với một CA/TSA tổng hợp.

1. Xuất tệp ZIP chứa nhật ký đã được ký sau điểm kiểm tra để tệp này bao gồm tiền tố đó. Xác minh bằng cách sử dụng dấu vân tay đã được xác nhận độc lập:

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. Bảo toàn tệp ZIP, điểm kiểm tra, yêu cầu, phản hồi, chuỗi chứng chỉ, kết quả xác minh và bản ghi chuyển giao bên ngoài bộ thu thập. Tiến hành xác minh lại khi nhận được.

Để chuẩn bị một yêu cầu từ điểm kiểm tra đã lưu:

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

Quá trình chuẩn bị sẽ chuẩn hóa định dạng JSON và bao gồm điểm kiểm tra tương ứng trong tệp lưu trữ. Vui lòng sử dụng các **byte điểm kiểm tra từ tệp lưu trữ đó** để xác minh TSA, ngay cả khi tệp đầu vào có các khoảng trắng khác nhau.

## Phạm vi xác minh

| Kiểm tra | Hành vi hiện tại |
| --- | --- |
| Dữ liệu | Giá trị SHA-256 của các byte điểm kiểm tra chính xác phải trùng khớp với giá trị trả về |
| Yêu cầu | Với `--request`, truy vấn gốc và giá trị ngẫu nhiên (nonce) sẽ được xác minh |
| Chữ ký TSA | OpenSSL xác minh chữ ký và chuỗi chứng chỉ đến Cơ quan Chứng nhận (CA) được chỉ định rõ ràng |
| Chữ ký của bộ thu thập | Được xác minh độc lập bởi đơn vị xác minh nhật ký thông qua khóa được ghim |
| Việc thu hồi | Không có tính năng truy xuất OCSP/CRL tự động |
| Tính hợp lệ lâu dài | Không thực hiện xác thực lưu trữ sau khi chứng chỉ hết hạn |
| Lịch trình gửi bài | Chế độ bằng chứng, mặc định là tắt |

`--request` về mặt kỹ thuật là tùy chọn, nhưng việc bỏ qua nó sẽ ngăn cản việc xác minh nonce gốc. Đối với quy trình đầy đủ này, giá trị `request_checked` của kết quả phải là true. Việc xác minh chứng chỉ tuân theo các quy tắc và thời gian xác minh của OpenSSL đã cài đặt. Việc lưu trữ lâu dài cần có chính sách chứng chỉ/bằng chứng thu hồi riêng biệt.

Một chữ ký mật mã hợp lệ không tự động đồng nghĩa với một dấu thời gian đủ điều kiện hoặc một quyết định về tính hợp lệ pháp lý. Nếu người vận hành bịa đặt các quan sát trước khi gắn dấu thời gian, TSA sẽ cố định các byte đó; điều này không chứng minh tính xác thực của chúng.

## Bản ghi chuyển giao

Ghi lại mã định danh vụ việc, người gửi và người nhận, thời gian chuyển tiếp theo múi giờ UTC cùng nguồn gốc của nó, mục đích, tên tệp/giá trị SHA-256, dấu vân tay của bộ thu thập, phạm vi chuỗi, các khoảng trống đã biết, phiên bản trình xác minh và kết quả xác minh. Hãy ký tên và lưu giữ độc lập bản ghi này theo quy trình của tổ chức quý vị. Hệ thống lưu giữ bản ghi đa người dùng không được triển khai trong TgWitness.

Trong quá trình phát triển, chúng tôi không liên hệ với bất kỳ TSA độc lập nào đang hoạt động. Các thử nghiệm nội bộ tạo ra một CA/TSA tổng hợp để kiểm tra tính tương thích cũng như khả năng từ chối dữ liệu đã bị thay đổi, nonce hoặc CA.
